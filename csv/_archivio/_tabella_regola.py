# -*- coding: utf-8 -*-
"""GENERA il par.6 di `doc/CURE_fisica_ordine.md`: la tabella delle 23 `CENS-*`.

**A COSA SERVE:** i numeri e i motivi della tabella **escono da qui**, letti da
`doc/INDICE_ID.tsv` -- non sono ricopiati a mano (`L-NUMERI`).

**DUE MODI:**
  `python csv/_archivio/_tabella_regola.py`              appende il par.6 se non c'e'
  `python csv/_archivio/_tabella_regola.py --rigenera`   taglia quello vecchio e lo riscrive

**IL MOTIVO DI CIASCUNA VOCE si legge dalla NOTA d'indice, e si prende L'ULTIMA decisione:**
prima la `REGOLA DI LUCA applicata il 2026-09-27` *(la mia applicazione della regola)*, poi,
se c'e', la `DECISIONE DI LUCA del 2026-09-27 (risposte a bf15c0c)` *(le sue risposte sulle
dieci che la regola non decideva)*. **La seconda vince**, perche' e' quella che ha deciso.

**Girato il 2026-09-27**, due volte: dopo `_regola_blocca.py` e dopo `_decisioni_luca_10.py`.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAD = r"C:\Users\lpeano\soliton_simulator"
TAB, NL = chr(9), chr(10)
SPUNTA, ATTENZIONE, PUNTO = chr(0x2705), chr(0x26A0), chr(0xB7)
DOC = os.path.join(RAD, "doc", "CURE_fisica_ordine.md")
TITOLO = "# 6. **LA REGOLA DI LUCA APPLICATA ALLE 23 `CENS-*`**"

MARCA_REGOLA = "REGOLA DI LUCA applicata"
MARCA_LUCA = "DECISIONE DI LUCA del 2026-09-27 (risposte a bf15c0c)"

# ------------------------------------------------------------------ il par.6 precedente
_T = io.open(DOC, encoding="utf-8").read()
if TITOLO in _T:
    if "--rigenera" not in sys.argv:
        raise SystemExit("[tabella] il par.6 c'e' GIA': usa --rigenera per rifarlo")
    _i = _T.index(TITOLO)
    _testa = _T[:_i].rstrip(NL)
    _k = _testa.rfind(NL + "---")
    if _k > 0:
        _testa = _testa[:_k]
    io.open(DOC, "w", encoding="utf-8", newline=NL).write(_testa + NL)
    print("[tabella] par.6 precedente RIMOSSO, lo riscrivo")


def motivo_da_nota(nota):
    """L'ULTIMA decisione scritta nella nota: quella di Luca se c'e', altrimenti la regola."""
    if MARCA_LUCA in nota:
        coda = nota.split(MARCA_LUCA, 1)[1]
        if ". " in coda:
            return coda.split(". ", 1)[1].strip()
        return coda.strip(": .")
    i = nota.rfind(MARCA_REGOLA)
    coda = nota[i:] if i > 0 else ""
    if "MOTIVO: " in coda:
        return coda.split("MOTIVO: ", 1)[1]
    if "LA DECIDE LUCA: " in coda:
        return coda.split("LA DECIDE LUCA: ", 1)[1]
    return ""


righe = io.open(os.path.join(RAD, "doc", "INDICE_ID.tsv"), encoding="utf-8").read().split(NL)
capi = righe[0].split(TAB)
K = {k: i for i, k in enumerate(capi)}
si, no, am = [], [], []
for r in righe:
    c = r.split(TAB)
    if not c or not c[0].startswith("CENS-") or len(c) != len(capi):
        continue
    v = c[K["blocca_run_base"]]
    voce = (c[0],
            c[K["titolo_breve"]].replace("[A] ", "").replace("[B] ", "")[:58],
            motivo_da_nota(c[K["nota"]]),
            MARCA_LUCA in c[K["nota"]])
    (si if v == "SI" else no if v == "NO" else am).append(voce)

# ------------------------------------------------------------------ il testo
B = ["", "---", "", TITOLO + " *(2026-09-27)*", ""]
B.append("> **La regola, verbatim:** `SI` = **la falsita' cambia i NUMERI della fisica del run**;")
B.append("> `NO` = **si risolve riscrivendo un commento o un documento**.")
B.append("> **Applicata a TUTTE e 23, non solo alle cinque nominate.** L'ho applicata io alla")
B.append("> classe (A) e alle (B) non attive; **le dieci che la regola NON decideva le ha decise")
B.append("> Luca** *(risposte a `bf15c0c`)*. Esito: **%d `SI` %s %d `NO` %s %d ancora aperte**."
         % (len(si), PUNTO, len(no), PUNTO, len(am)))
B.append("")
B.append("*(La colonna **chi** dice se la riga porta una decisione esplicita di Luca %s oppure"
         % chr(0x2014))
B.append("l'applicazione della regola da parte mia.)*")
B.append("")


def tabella(titolo, voci, terza):
    fuori = [titolo, "", "| ID | che cos'e' | chi | %s |" % terza, "|---|---|---|---|"]
    for a, b, c, luca in voci:
        fuori.append("| `%s` | %s | %s | %s |"
                     % (a, b, "**LUCA**" if luca else "regola", c))
    fuori.append("")
    return fuori


B += tabella("## %s `SI` %s %d voci" % (SPUNTA, chr(0x2014), len(si)), si, "motivo")
B += tabella("## `NO` %s %d voci" % (chr(0x2014), len(no)), no, "motivo")

if am:
    B.append("## %s **ANCORA APERTE %s %d voci**" % (ATTENZIONE, chr(0x2014), len(am)))
    B += tabella("", am, "perche'")[1:]
else:
    B.append("## %s **LE DIECI CHE ERANO AMBIGUE SONO DECISE**" % SPUNTA)
    B.append("")
    B.append("> **La regola non le decideva, e invece di forzarla l'ho detto.** Le ha decise Luca:")
    B.append("> `CENS-A1` **`SI`** *(si chiude con la decisione **(e)** sul legame `phi`-spinore)*;")
    B.append("> `CENS-B1 B2 B5 B8 B13 B14` **`NO`** *(leggi **attive**, restano attive %s"
             % chr(0x2014))
    B.append("> decisione (3) %s e **da misurare dopo il run base**)*;" % chr(0x2014))
    B.append("> `CENS-B3 B4` **`NO`**, e la cura e' **dichiarare che il ramo OFF non esiste**;")
    B.append("> `CENS-B6` **`NO`** *(progetto)*.")
    B.append(">")
    B.append("> ### %s **E UNA CORREZIONE DEL GUARDIANO SU UN MIO `SI`: `CENS-B12`" % ATTENZIONE)
    B.append("> ### (`KERNEL_ALPHA`) E' `NO`.**")
    B.append("> Non blocca il **run base**: **blocca la PROVA 3** *(universalita')*, e la misura")
    B.append("> del principio di equivalenza va fatta **prima della PROVA 3**.")
    B.append("> **Il mio `SI` avrebbe bloccato il run base con una misura SOSPESA** dalla")
    B.append("> decisione (1) %s cioe' esattamente la conseguenza che avevo segnalato come aperta,"
             % chr(0x2014))
    B.append("> **applicata alla voce sbagliata**.")
    B.append("")

io.open(DOC, "a", encoding="utf-8", newline=NL).write(NL.join(B) + NL)
print("tabella scritta: %d SI, %d NO, %d aperte" % (len(si), len(no), len(am)))
