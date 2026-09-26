# -*- coding: utf-8 -*-
"""TRIAGE — ogni voce `CODICE` di `RAMIFICAZIONI.md` ha un ESITO. Tabella GENERATA, non scritta.

⚠ NESSUNA VOCE RESTA SENZA ESITO, e non e' una promessa: e' un'ASSERZIONE. Se anche una sola
  voce dell'elenco autorevole non ha una classificazione, **lo script FALLISCE e non scrive
  niente**. E' il collaudo `K3`.

⚠ DA DOVE VIENE L'ELENCO, e va detto perche' NON e' riproducibile da un filtro meccanico:
  **nessun criterio automatico da' 36.** Sul file di oggi il **tag** `⏳[... · CODICE]`
  ne marca **11**, la parola `CODICE` in maiuscolo **20**, `codice` senza distinzione di
  maiuscole **49**. **L'elenco autorevole e' quello ESPLICITO di Luca**: le **15** voci gia'
  coperte da `D01`-`D19` **piu' le 21** che ha nominato. **Sta scritto qui sotto, e lo script
  verifica che ognuna ESISTA davvero nel registro** *(se un ID non c'e', fallisce: `K2`)*.

I TRE ESITI AMMESSI, e nessun altro:
  **DIFETTO**        entra nella sezione con un ID nuovo, la prova e lo stato *(se gia' curato,
                     stato `CURATO` col commit della cura)*;
  **NON E' UN DIFETTO**  col motivo -- una scelta dichiarata, una domanda aperta, un'osservazione,
                     un difetto di CRITERIO che vive altrove;
  **GIA' COPERTA**   dall'`ID` del difetto che la contiene.
ASCII PURO.
"""
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
REG = os.path.join(RADICE, "doc", "RAMIFICAZIONI.md")
CODA = os.path.join(RADICE, "doc", "STATO_RUN.md")

# ---------------------------------------------------------------- LE 15 GIA' COPERTE
GIA = {
    "Z7": "D06", "Z10": "D07", "Z9-bis": "D07", "Z14": "D08", "Z73": "D09", "Z75": "D10",
    "Z87": "D11", "Z89": "D12", "Z11": "D13", "Z41": "D14", "Z71": "D15", "Z91": "D16",
    "Z94": "D17", "Z92": "D18", "Z88": "D19", "Z104": "D03",
}

# ---------------------------------------------------------------- LE 21 DA CLASSIFICARE
# (esito, ID nuovo o rimando, la riga che lo spiega, stato)
TRIAGE = {
    "Z1": ("DIFETTO", "D20",
           "La correzione (1) su `inerzia` NON e' stata cablata, e **il gate che la autorizzava "
           "aveva misurato UN'ALTRA GRANDEZZA**", "APERTO"),
    "Z4": ("DIFETTO", "D21",
           "`_floor_d0` e' SOSPESA, e **i due rami violano assiomi DIVERSI**: la scelta non e' "
           "stata fatta", "APERTO"),
    "Z24": ("DIFETTO", "D22",
            "Il DENOMINATORE PER GRADO: la misura non distingue (A) da (B), ma **(B) cade per "
            "DIMOSTRAZIONE**, e lo stesso schema e' in **almeno quattro punti**", "CURATO"),
    "Z25": ("GIA' COPERTA", "D22",
            "E' la CHIUSURA di `Z24`: il denominatore per grado era un errore ed e' stato TOLTO, "
            "sigillo `12/12`", ""),
    "Z33": ("GIA' COPERTA", "D14",
            "La mediana di `ritmo()` fa DUE mestieri; `Z41` **la supera sullo stesso oggetto** "
            "dicendo che ne fa TRE ed e' anche il rompi-anello", ""),
    "Z36": ("NON E' UN DIFETTO", "",
            "**Ri-letta da `Z37`**: il `64.7 %` e' **un rapporto su una grandezza minuscola**, e "
            "gli stati consecutivi hanno overlap `> 0.99` nel `100 %` dei casi. **E' una lettura "
            "corretta di un numero, non un difetto del codice**", ""),
    "Z37": ("DIFETTO", "D23",
            "**La cucitura dello snapshot FALLISCE su entrambi i fronti**, e si DIMOSTRA perche'. "
            "**NON CABLATA**", "APERTO"),
    "Z38": ("NON E' UN DIFETTO", "",
            "Il gauge attuale sta NELLA MATERIA e **la mia obiezione e' REFUTATA**. Una premessa "
            "che cade non e' un difetto: e' un riscontro", ""),
    "Z39": ("NON E' UN DIFETTO", "",
            "**Un fatto stabile di `CLAUDE.md` e' caduto** *(`cs` e' vivo)*, e `CLAUDE.md` e' "
            "gia' stato corretto. **Il lavoro che ne discende e' il fronte `A`, non un difetto "
            "del codice**", ""),
    "Z40": ("DIFETTO", "D24",
            "**`A2` e' VIOLATO da `Lam = mean(I)`** -- una media GLOBALE dentro una legge locale "
            "-- **e la violazione e' la ragione per cui il pezzo funziona**", "APERTO"),
    "Z46": ("DIFETTO", "D25",
            "**Il gauge del tempo e' la costante `1e-9`**, e il `93 %` dei nodi non invecchia: "
            "sono sempre gli stessi, e sono le tre masse", "APERTO"),
    "Z53": ("DIFETTO", "D26",
            "Le coorti **non sopravvivevano allo SNAPSHOT**: dopo un salva/ricarica il lignaggio "
            "ripartiva VUOTO", "CURATO"),
    "Z65": ("DIFETTO", "D27",
            "**Il grafo e' in QUATTRO COMPONENTI che non si toccano mai**, e la bimodalita' del "
            "grado e' la semina. **Una distanza SUL GRAFO fra componenti diverse non esiste**, e "
            "le tre prove dell'ipotesi la usano", "APERTO"),
    "Z70": ("NON E' UN DIFETTO", "",
            "**Corregge una lettura precedente**: l'anello `A6` c'e', ma non e' istantaneo e non "
            "passa dalla riga che era stata citata. **La correzione di una lettura non e' un "
            "difetto del codice**", ""),
    "Z74": ("DIFETTO", "D28",
            "**`nsub` esplode e lo tira `max(|vd|)` su POCHISSIMI archi**: il costo dell'intero "
            "sistema e' governato da una manciata di archi", "APERTO"),
    "Z77": ("DIFETTO", "D29",
            "**CINQUE NODI DI VUOTO sono i piu' connessi dell'intero sistema**: il vuoto ha degli "
            "HUB, e non dovrebbe averne", "APERTO"),
    "Z79": ("GIA' COPERTA", "D18",
            "Il clip della coesione **scalava con `d0` stesso** *(`A11` cor.2)*; `COES_ADIM` lo "
            "ha sostituito col passo causale. **⚠ DA RIVERIFICARE sul blob corrente**", ""),
    "Z83": ("NON E' UN DIFETTO", "",
            "E' una **DOMANDA dichiarata** *(`d0` deve stare sopra `LAM`?)*, e la decisione "
            "spetta a Luca. **Una domanda aperta non e' un difetto**", ""),
    "Z84": ("NON E' UN DIFETTO", "",
            "**Descrive un MECCANISMO** -- `d` e `d0` sono un anello, ed e' `cs^2*lap` ad "
            "allungare l'arco. **Alimenta il sospetto `S01`**, non e' un difetto di per se'", ""),
    "Z86": ("NON E' UN DIFETTO", "",
            "**E' un difetto di CRITERIO, non di codice**, e l'errore era mio. Vive in "
            "`doc/PATTERN_DI_PROVA.md` e in `P1-sexies`, non fra i difetti del simulatore", ""),
    "Z90": ("GIA' COPERTA", "D17",
            "La divergenza del ramo D *(`nsub = 22591`)* risaliva a **`peq` negativo**, curato da "
            "`PEQ_ESATTO`: `Z101` misura che **l'esplosione e' sparita**", ""),
}

# ---------------------------------------------------------------- L'ELENCO AUTOREVOLE
# ⚠ COSTANTE A SE', e NON derivato da `GIA`/`TRIAGE`: e' l'unica forma in cui una voce puo'
#   risultare NON CLASSIFICATA, ed e' cio' che il collaudo `K2` esercita.
#   Sono le 15 gia' coperte da `D01`-`D19` piu' le 21 nominate da Luca il 2026-09-22.
ELENCO = ("Z7 Z9-bis Z10 Z11 Z14 Z41 Z71 Z73 Z75 Z87 Z88 Z89 Z91 Z92 Z94 Z104 "
          "Z1 Z4 Z24 Z25 Z33 Z36 Z37 Z38 Z39 Z40 Z46 Z53 Z65 Z70 Z74 Z77 Z79 Z83 Z84 Z86 "
          "Z90").split()

INIZIO = "<!-- TRIAGE-INIZIO -->"
FINE = "<!-- TRIAGE-FINE -->"
D_INIZIO = "<!-- DIFETTI-NUOVI-INIZIO -->"
D_FINE = "<!-- DIFETTI-NUOVI-FINE -->"


def voci_registro(percorso):
    """Ogni voce del registro, dai CONFINI DI RIGA. ⚠ NON si cerca l'ultimo `**Zxx**` prima di
    una parola: le righe CITANO altre voci nel corpo, e l'ID pescato sarebbe quello citato --
    e' il difetto che ha fatto perdere meta' dell'elenco il 2026-09-22."""
    t = io.open(percorso, encoding="utf-8", errors="replace").read()
    out = {}
    for p in re.split(r"\n(?=\| \*\*Z)", t):
        m = re.match(r"\| \*\*(Z[0-9]+(?:-[a-z]+)?)\*\*", p)
        if m and m.group(1) not in out:
            out[m.group(1)] = p
    return out


def verifica(esistenti, elenco, gia, triage, W=None):
    """Ritorna la lista dei guai. Vuota = si puo' scrivere.

    L'ELENCO e' l'autorita', ed e' una COSTANTE A SE': se coincidesse con `gia + triage`, una
    voce non classificata NON POTREBBE ESISTERE per costruzione, e il collaudo sarebbe vuoto.
    E' un difetto che ho avuto in questo stesso script, e il collaudo `K2` lo tiene chiuso."""
    guai = []
    tutte = sorted(set(elenco))
    for k in tutte:
        if k not in esistenti:
            guai.append("%s: citata nell'elenco ma NON ESISTE nel registro" % k)
    for k in tutte:
        if (k not in gia) and (k not in triage):
            guai.append("%s: NESSUN ESITO" % k)
    for k, v in triage.items():
        if v[0] not in ("DIFETTO", "NON E' UN DIFETTO", "GIA' COPERTA"):
            guai.append("%s: esito non ammesso (%s)" % (k, v[0]))
        if v[0] == "DIFETTO" and not re.match(r"^D[0-9]{2}$", v[1] or ""):
            guai.append("%s: DIFETTO senza ID nuovo" % k)
        if v[0] == "GIA' COPERTA" and not re.match(r"^D[0-9]{2}$", v[1] or ""):
            guai.append("%s: GIA' COPERTA senza l'ID che la copre" % k)
        if not (v[2] or "").strip():
            guai.append("%s: esito senza MOTIVO" % k)
    return guai


def collaudo(W):
    """`P1-sexies`. **Il caso che DEVE fallire: una voce `CODICE` finta, NON classificata.**"""
    W("COLLAUDO (`P1-sexies`), PRIMA di scrivere\n")
    W("-" * 96 + "\n")
    e = []
    finto = {"Z7": "| **Z7** x", "ZFINTA": "| **ZFINTA** x"}
    g = verifica(finto, ["Z7"], {"Z7": "D06"}, {})
    ok1 = (len(g) == 0)
    W("K1 un elenco COMPLETO -> nessun guaio -> %s  %s\n"
      % ("OK" if ok1 else "*** FALSO ALLARME ***", g if g else ""))
    e.append(ok1)

    # IL CASO CHE DEVE FALLIRE: una voce `CODICE` FINTA, presente nel registro e NON
    # classificata. `verifica` la deve trovare: e' il caso che il mandato chiede per nome.
    g2 = verifica(finto, ["Z7", "ZFINTA"], {"Z7": "D06"}, {})
    ok2 = any("ZFINTA" in x and "NESSUN ESITO" in x for x in g2)
    W("K2 IL CASO CHE DEVE FALLIRE: una voce dell'elenco SENZA esito -> %s\n"
      % ("OK: lo script si fermerebbe" if ok2 else "*** PASSEREBBE: l'elenco sarebbe bugiardo ***"))
    e.append(ok2)

    # e il caso che deve fallire: un ID citato che NON esiste nel registro
    g3 = verifica({"Z7": "x"}, ["Z7", "Z999"], {"Z7": "D06", "Z999": "D99"}, {})
    ok3 = any("Z999" in x for x in g3)
    W("K3 IL CASO CHE DEVE FALLIRE: un ID citato che NON esiste nel registro -> %s\n"
      % ("OK" if ok3 else "*** un ID inventato passerebbe ***"))
    e.append(ok3)

    # e un esito senza motivo
    g4 = verifica({"Z7": "x"}, ["Z7"], {}, {"Z7": ("DIFETTO", "D99", "   ", "APERTO")})
    ok4 = any("senza MOTIVO" in x for x in g4)
    W("K4 IL CASO CHE DEVE FALLIRE: un esito SENZA motivo -> %s\n"
      % ("OK" if ok4 else "*** un esito muto passerebbe ***"))
    e.append(ok4)

    ok = all(e)
    W("-" * 96 + "\n")
    W("  -> i criteri %s\n\n" % ("PASSANO" if ok else "*** NON PASSANO: NON scrivo ***"))
    return ok


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    esistenti = voci_registro(REG)
    guai = verifica(esistenti, ELENCO, GIA, TRIAGE)
    if guai:
        W("*** IL TRIAGE NON E' COMPLETO: %d guai. NON scrivo niente. ***\n" % len(guai))
        for g in guai:
            W("   %s\n" % g)
        return 1

    tutte = sorted(set(ELENCO),
                   key=lambda s: (int(re.sub(r"[^0-9]", "", s) or 0), s))
    righe = ["| voce | esito | ID | perche' |", "|---|---|---|---|"]
    n_dif = n_no = n_gia = 0
    for k in tutte:
        if k in TRIAGE:
            es, idn, perche, stato = TRIAGE[k]
            if es == "DIFETTO":
                n_dif += 1
                righe.append("| **`%s`** | **DIFETTO** | **`%s`** *(%s)* | %s |"
                             % (k, idn, stato, perche))
            elif es == "GIA' COPERTA":
                n_gia += 1
                righe.append("| **`%s`** | GIA' COPERTA | `%s` | %s |" % (k, idn, perche))
            else:
                n_no += 1
                righe.append("| **`%s`** | NON E' UN DIFETTO | — | %s |" % (k, perche))
        else:
            n_gia += 1
            righe.append("| **`%s`** | GIA' COPERTA | `%s` | gia' nella sezione DIFETTI APERTI "
                         "dal recupero di `ccf1f73` |" % (k, GIA[k]))

    testa = [
        "",
        "### ESITO DI OGNI VOCE `CODICE` DI `RAMIFICAZIONI.md` — **tabella GENERATA**",
        "",
        "> **GENERATA DA CODICE** (`P1-ter`) da `csv/_seal_fork/_triage_difetti.py`. **Nessuna "
        "voce resta senza esito**, e non e' una promessa: se una sola ne fosse priva, **lo "
        "script fallisce e non scrive niente**.",
        ">",
        "> **⚠ L'ELENCO NON E' RIPRODUCIBILE DA UN FILTRO MECCANICO, e va detto:** sul file "
        "di oggi il **tag** `[... · CODICE]` marca **11** voci, la parola `CODICE` in "
        "maiuscolo **20**, `codice` senza distinzione di maiuscole **49**. **Nessuno di questi "
        "da' 36.** L'elenco autorevole e' quello **esplicito di Luca**: le **15** gia' coperte da "
        "`D01`-`D19` **piu' le 21** che ha nominato. Lo script **verifica che ognuna esista** nel "
        "registro.",
        ">",
        "> **⚠ E IL MIO ERRORE DI ESTRAZIONE, dichiarato:** cercavo l'ultimo `**Zxx**` "
        "*prima* della parola `CODICE`, ma **le righe CITANO altre voci nel corpo**, quindi l'ID "
        "pescato era spesso quello **citato**. Ora si parte dai **confini di riga**.",
        "",
        "**%d DIFETTI nuovi · %d gia' coperte · %d non sono difetti — %d voci in "
        "tutto.**" % (n_dif, n_gia, n_no, len(tutte)),
        "",
    ]
    blocco = "\n".join(testa + righe) + "\n"

    # le righe dei DIFETTI nuovi, nella tabella DIFETTI APERTI
    nuovi = []
    for k in sorted(TRIAGE, key=lambda s: TRIAGE[s][1] or "zz"):
        es, idn, perche, stato = TRIAGE[k]
        if es != "DIFETTO":
            continue
        nuovi.append("| **%s** | %s | `%s` | — | `%s` |" % (idn, perche, k, stato))
    t = io.open(CODA, encoding="utf-8", newline="").read()
    if D_INIZIO in t and D_FINE in t:
        _a = t.index(D_INIZIO) + len(D_INIZIO)
        _b = t.index(D_FINE)
        t = t[:_a] + "\n" + "\n".join(nuovi) + "\n" + t[_b:]
        io.open(CODA, "w", encoding="utf-8", newline="\n").write(t)
    else:
        W("*** mancano i marcatori dei DIFETTI nuovi: righe D20-D29 NON inserite ***\n")
        return 1
    if INIZIO not in t or FINE not in t:
        W("*** mancano i marcatori %s / %s in %s ***\n" % (INIZIO, FINE, CODA))
        return 1
    a = t.index(INIZIO) + len(INIZIO)
    b = t.index(FINE)
    io.open(CODA, "w", encoding="utf-8", newline="\n").write(t[:a] + "\n" + blocco + t[b:])
    W("scritte %d righe in %s: %d DIFETTI nuovi, %d gia' coperte, %d non difetti\n"
      % (len(tutte), os.path.relpath(CODA, RADICE), n_dif, n_gia, n_no))
    for k in sorted(TRIAGE):
        if TRIAGE[k][0] == "DIFETTO":
            W("   DIFETTO ACCLARATO: %s (da %s) - %s\n"
              % (TRIAGE[k][1], k, TRIAGE[k][2][:70].replace("**", "")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
