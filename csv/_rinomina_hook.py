# -*- coding: utf-8 -*-
"""**IL PREFISSO `H-` AI PRESIDI DEI HOOK** *(mandato di Luca 2026-09-26, punto `d`)*.

**Perche':** `P3` e `P5` erano **DUE REGOLE DIVERSE CON LO STESSO NOME** -- la regola di metodo di
`CLAUDE.md` e il presidio del hook. **E' lo stesso difetto che l'indice ha curato per i difetti**
*(`A3` era tre voci)*: **chi citava `P3` non diceva quale**. Il prefisso `H-` dice *«questo lo
impedisce una macchina»*.

**LA FORMA E' QUELLA CHE HA SCRITTO LUCA: `H-P3`, `H-P5`, ...** -- cioe' **il nome di prima col
prefisso**, non un nome nuovo. Cosi' ogni citazione storica (`P5` in un referto del 25/9) resta
**leggibile** e si risolve con l'`alias` nell'indice. *(La proposta aveva suggerito nomi semantici
-- `H-CLI`, `H-CONFIG`, `H-ANCORA` -- e li ho scartati per questa ragione.)*

**OGNI SOSTITUZIONE E' ASSERITA PER SE' (`P1-quater`):** l'ancora si conta, e se non e' unica --
o se non c'e' -- lo script **si ferma**. Nessun `assert` globale del tipo *«il testo e' cambiato»*,
che sarebbe soddisfatto dalle ALTRE sostituzioni.

    python csv/_rinomina_hook.py --prova    # dice cosa farebbe, non scrive
    python csv/_rinomina_hook.py            # scrive

ASCII puro.
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Rinomina etichette in sorgenti.
# ESENTE-H-P8: la stringa `HEAD:soliton_simulator.py` qui dentro NON e' un'ancora al codice di
#   prima: e' il TESTO DA SOSTITUIRE dentro il messaggio di `csv/_presidio_commenti_flag.py`.
#   Questo script non fa girare git e non confronta due versioni: fa `replace` su file.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
CANC = chr(35)

# (file, [(vecchio, nuovo, quante_volte_attese)])
LAVORO = [
    ("csv/_hook_presidi.py", [
        ("**I PRESIDI CHE IMPEDISCONO** " + chr(8212) + " `P3`, `P5`, `P8` come hook",
         "**I PRESIDI CHE IMPEDISCONO** " + chr(8212) + " `H-P3`, `H-P5`, `H-P8` come hook", 1),
        ("| **`P3`** | un **sigillo**", "| **`H-P3`** | un **sigillo**", 1),
        ("| **`P5`** | un referto", "| **`H-P5`** | un referto", 1),
        ("| **`P8`** | un confronto", "| **`H-P8`** | un confronto", 1),
        ("`ESENTE-P3: <motivo>` in un commento", "`ESENTE-H-P3: <motivo>` in un commento", 1),
        ('ESENTE = re.compile(r"' + CANC + r'\s*ESENTE-(P\d)\s*:\s*(.+)")',
         'ESENTE = re.compile(r"' + CANC + r'\s*ESENTE-(H-P\d)\s*:\s*(.+)")', 1),
        ('g.append(("P3", "sigillo che configura', 'g.append(("H-P3", "sigillo che configura', 1),
        ('g.append(("P5", "scrive un referto', 'g.append(("H-P5", "scrive un referto', 1),
        ('g.append(("P8", "prende', 'g.append(("H-P8", "prende', 1),
        ('    # --- P3: DEVE bloccare / NON deve', '    # --- H-P3: DEVE bloccare / NON deve', 1),
        ('    # --- P5: DEVE bloccare / NON deve', '    # --- H-P5: DEVE bloccare / NON deve', 1),
        ('    # --- P8: DEVE bloccare / NON deve', '    # --- H-P8: DEVE bloccare / NON deve', 1),
        ('"blocca_P3":', '"blocca_H-P3":', 1),
        ('"passa_P3":', '"passa_H-P3":', 1),
        ('"blocca_P5":', '"blocca_H-P5":', 1),
        ('"passa_P5":', '"passa_H-P5":', 1),
        ('"blocca_P8":', '"blocca_H-P8":', 1),
        ('"passa_P8":', '"passa_H-P8":', 1),
        ('rel, t = SORG["blocca_P3"]', 'rel, t = SORG["blocca_H-P3"]', 1),
        ('" ESENTE-P3: motivo di prova"', '" ESENTE-H-P3: motivo di prova"', 1),
        ('elenco="%s|P3" % rel', 'elenco="%s|H-P3" % rel', 1),
        ("Un commit che viola `P3`, `P5` o `P8`", "Un commit che viola `H-P3`, `H-P5` o `H-P8`", 1),
        ("'ESENTE-<Pn>: <motivo>'", "'ESENTE-<H-Pn>: <motivo>'", 1),
        ("#  PRE-COMMIT VERSIONATO", "#  PRE-COMMIT VERSIONATO", 0),
    ]),
    ("csv/_presidio_commenti_flag.py", [
        ('print("[P7] `HEAD:soliton_simulator.py`', 'print("[H-P7] `HEAD:soliton_simulator.py`', 1),
        ('NL + "[P7] *** COMMIT RIFIUTATO', 'NL + "[H-P7] *** COMMIT RIFIUTATO', 1),
    ]),
    ("csv/_hook_relazione.py", [
        ('"[REG-R] il controllo NON e\' girato', '"[H-REG-R] il controllo NON e\' girato', 1),
        ('"[INDICE] eccezione DICHIARATA nel messaggio.', '"[H-INDICE] eccezione DICHIARATA nel messaggio.', 1),
        ('"\\n[INDICE] *** COMMIT RIFIUTATO ***', '"\\n[H-INDICE] *** COMMIT RIFIUTATO ***', 1),
        ('"[INDICE] il controllo NON e\' girato', '"[H-INDICE] il controllo NON e\' girato', 1),
        ('"[P1-bis] eccezione DICHIARATA:', '"[H-P1-bis] eccezione DICHIARATA:', 1),
        ('"\\n[P1-bis] *** COMMIT RIFIUTATO', '"\\n[H-P1-bis] *** COMMIT RIFIUTATO', 1),
    ]),
    ("csv/_hook_fisica.py", [
        ('"[REG-R] eccezione DICHIARATA:', '"[H-REG-R] eccezione DICHIARATA:', 1),
        ('"\\n[REG-R] *** COMMIT RIFIUTATO', '"\\n[H-REG-R] *** COMMIT RIFIUTATO', 1),
    ]),
    ("csv/_presidio_indice.py", [
        ('"[INDICE] eccezione DICHIARATA nel messaggio: non controllo."',
         '"[H-INDICE] eccezione DICHIARATA nel messaggio: non controllo."', 1),
        ('NL + "[INDICE] *** COMMIT RIFIUTATO ***"', 'NL + "[H-INDICE] *** COMMIT RIFIUTATO ***"', 1),
    ]),
    (".githooks/pre-commit", [
        ("presidi `P3` / `P5` / `P8`", "presidi `H-P3` / `H-P5` / `H-P8`", 1),
    ]),
    (".githooks/commit-msg", [
        ("`P1-bis` (la relazione) + `REG-R` (la scheda di fisica)",
         "`H-P1-bis` (la relazione) + `H-REG-R` (la scheda) + `H-INDICE` + `H-RIGHE`", 1),
    ]),
]

MARCATORE = re.compile(r"(" + CANC + r"\s*ESENTE-)(P\d)(\s*:)")


def sostituisci(rel, coppie, scrivi):
    p = os.path.join(RADICE, rel)
    t = io.open(p, encoding="utf-8", newline="").read()
    fatte = 0
    for vecchio, nuovo, attese in coppie:
        n = t.count(vecchio)
        if n != attese:
            raise SystemExit("%s: ancora attesa %d volte, trovata %d: %s"
                             % (rel, attese, n, vecchio[:70]))
        if attese:
            t = t.replace(vecchio, nuovo)
            fatte += 1
    if scrivi:
        io.open(p, "w", encoding="utf-8", newline=NL).write(t)
    return fatte


def marcatori(scrivi):
    """I `ESENTE-P5:` sparsi nei sorgenti diventano `ESENTE-H-P5:`. Uno per riga, contati."""
    tocchi = []
    for base, dd, ff in os.walk(os.path.join(RADICE, "csv")):
        b = base.replace(chr(92), "/")
        if "/_tmp" in b or "__pycache__" in b:
            continue
        for f in sorted(ff):
            if not f.endswith(".py") or f == "_rinomina_hook.py" or f == "_hook_presidi.py":
                continue
            p = os.path.join(base, f)
            t = io.open(p, encoding="utf-8", newline="").read()
            n = len(MARCATORE.findall(t))
            if not n:
                continue
            t2 = MARCATORE.sub(lambda m: m.group(1) + "H-" + m.group(2) + m.group(3), t)
            if len(MARCATORE.findall(t2)):
                raise SystemExit("%s: restano marcatori vecchi dopo la sostituzione" % f)
            if scrivi:
                io.open(p, "w", encoding="utf-8", newline=NL).write(t2)
            tocchi.append((os.path.relpath(p, RADICE).replace(chr(92), "/"), n))
    return tocchi


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    print("=" * 92)
    print("PREFISSO `H-` AI PRESIDI DEI HOOK%s" % ("" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 92)
    tot = 0
    for rel, coppie in LAVORO:
        n = sostituisci(rel, coppie, scrivi)
        tot += n
        print("  %-34s %2d sostituzioni asserite" % (rel, n))
    tocchi = marcatori(scrivi)
    print("  marcatori ESENTE-Pn -> ESENTE-H-Pn: %d file, %d marcatori"
          % (len(tocchi), sum(n for _r, n in tocchi)))
    for r, n in tocchi:
        print("       %-56s %d" % (r, n))
    print("  TOTALE sostituzioni nei sorgenti dei hook: %d" % tot)
    sys.exit(0)
