# -*- coding: utf-8 -*-
"""**LE DUE SEZIONI DI `CLAUDE.md` CHE NON ERANO REGOLE DI LAVORO, portate dove vivono.**
*(mandato di Luca 2026-09-26, dall'inventario della proposta: posto 5)*

| sezione di allora | dove va | perche' |
|---|---|---|
| **`par.4` — le regole fisiche da non violare** | `doc/REGISTRO_FISICA.md` | **sono FISICA**: SU(2) nell'algebra di Lie, Verlet solo sul second'ordine, niente medie globali. Il posto delle leggi e' il registro della fisica. |
| **`par.6` — stato e ordine del lavoro** | `doc/STATO_RUN.md` | **e' STATO, non una regola:** dice **dove siamo**, e cambia col lavoro. |

**La fonte e' il tag `regole-pre-riordino`**, non il disco: `CLAUDE.md` e' stato riscritto.
**IDEMPOTENTE:** una sezione gia' portata **non si duplica** (si riconosce dal marcatore).
**In `STATO_RUN.md` l'innesto e' PRIMA delle voci di run**, subito dopo l'INDIRIZZO: quel file e'
letto da `csv/_stato_run.py`, che cerca `## APERTO` e `**chiuso`, e un innesto in coda
confonderebbe **la voce aperta**.

    python csv/_riordino_sposta.py --prova
    python csv/_riordino_sposta.py

ASCII puro.
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Sposta prosa fra documenti.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
sys.path.insert(0, _QUI)
import _riordino_storia as ST                                          # noqa: E402

MARCA = "<!-- DA-CLAUDE-MD-2026-09-26:%s -->"
CAPPELLO = ("> *(Era **`CLAUDE.md` %s** fino al riordino del 2026-09-26. **Verbatim**, "
            "dal tag `regole-pre-riordino`. La storia di quella sezione sta in "
            "`doc/STORIA_REGOLE.md`.)*")


def sezione(cerca):
    for tit, righe in ST.sezioni(ST.dal_tag("CLAUDE.md")):
        if tit.startswith("## " + cerca):
            while righe and not righe[-1].strip():
                righe.pop()
            return righe
    raise SystemExit("sezione non trovata nel tag: %s" % cerca)


def innesto(par, righe):
    m = MARCA % par
    return [m, "", CAPPELLO % par, ""] + righe + ["", m.replace("-->", "FINE -->"), ""]


def in_coda(dest, par, righe, scrivi):
    p = os.path.join(RADICE, dest)
    t = io.open(p, encoding="utf-8", newline="").read()
    if (MARCA % par) in t:
        return "gia' presente"
    nuovo = t.rstrip(NL) + NL + NL + "---" + NL + NL + NL.join(innesto(par, righe)) + NL
    if scrivi:
        io.open(p, "w", encoding="utf-8", newline=NL).write(nuovo)
    return "in coda, %d righe" % len(righe)


def dopo_indirizzo(dest, par, righe, scrivi):
    p = os.path.join(RADICE, dest)
    t = io.open(p, encoding="utf-8", newline="").read()
    if (MARCA % par) in t:
        return "gia' presente"
    ancora = "<!-- INDIRIZZO:FINE -->"
    n = t.count(ancora)
    if n != 1:
        raise SystemExit("%s: ancora `%s` trovata %d volte, ne serve UNA" % (dest, ancora, n))
    blocco = NL + NL + NL.join(innesto(par, righe)) + NL + "---" + NL
    t = t.replace(ancora, ancora + blocco)
    if scrivi:
        io.open(p, "w", encoding="utf-8", newline=NL).write(t)
    return "dopo l'INDIRIZZO, %d righe" % len(righe)


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    print("=" * 92)
    print("LE DUE SEZIONI DI `CLAUDE.md` CHE NON ERANO REGOLE%s"
          % ("" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 92)
    print("  par.4 -> doc/REGISTRO_FISICA.md   %s"
          % in_coda("doc/REGISTRO_FISICA.md", "par.4", sezione("4."), scrivi))
    print("  par.6 -> doc/STATO_RUN.md         %s"
          % dopo_indirizzo("doc/STATO_RUN.md", "par.6", sezione("6."), scrivi))
    sys.exit(0)
