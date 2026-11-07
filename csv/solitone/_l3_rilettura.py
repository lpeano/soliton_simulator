# -*- coding: utf-8 -*-
r"""**L3 RILETTA COL CRITERIO DI LUCA DEL `2026-11-07` `17:55`** *(la differenza col `D` intero non piu' di `2` volte quella del braccio del caos, a OGNI tempo campionato)*:
**solo lettura del referto** `doc/referti_l2/libreria_solitoni.txt` *(`libreria.py` `27a897f1`, `9eda4121`)*, **le righe dei tre bracci ai tempi stampati** *(ogni `1000` tick)*.

    python csv/solitone/_l3_rilettura.py > doc/referti_l2/libreria_l3_rilettura.txt

### **La grandezza per tempo:** **il massimo sulle tre regioni** *(cuore, corona, fascia)* **della differenza in massa e in energia** *(le sei colonne della riga)*, **come `d` di `libreria.py`.**
### ⚠ **I tempi stampati sono `7` per braccio** *(la carta campionava ogni `100` tick ma stampava una riga ogni `10` campioni)*: **la rilettura vale su QUEI tempi; tutti i tempi vogliono la carta rigirata.**
"""
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401

FATTORE = 2.0   # ### Luca 17:55, il criterio 1 (fissato DOPO i numeri, ancorato al braccio del caos: dichiarato)
REFERTO = os.path.join(solitone.RADICE, "doc", "referti_l2", "libreria_solitoni.txt")


def main():
    import _presidio
    _presidio.avvia(__file__)
    righe = open(REFERTO, encoding="utf-8").read().splitlines()
    bracci, cur = {}, None
    for r in righe:
        m = re.match(r"\s+(D intero|D ritagliato|caos)\s+il massimo", r)
        if m:
            cur = m.group(1)
            bracci[cur] = []
            continue
        m = re.match(r"\s+t\s+([0-9.]+)\s+M cuore ([0-9.e+-]+) corona ([0-9.e+-]+) fascia ([0-9.e+-]+)\s+E ([0-9.e+-]+) ([0-9.e+-]+) ([0-9.e+-]+)", r)
        if m and cur is not None:
            bracci[cur].append((float(m.group(1)), max(float(x) for x in m.groups()[1:])))
    assert set(bracci) == {"D intero", "D ritagliato", "caos"} and len({len(v) for v in bracci.values()}) == 1, "le righe dei tre bracci NON si leggono"
    print("L3 RILETTA (Luca 17:55, il criterio 1: D intero / caos <= %g a ogni tempo campionato) dal referto %s; %d tempi stampati per braccio" % (FATTORE, os.path.basename(REFERTO), len(bracci["caos"])))
    print("  %-8s %-11s %-12s %-11s %-10s" % ("t", "D intero", "D ritagliato", "caos", "intero/caos"))
    peggio, n_sopra = 0.0, 0
    for (t, a), (_t2, b), (_t3, c) in zip(bracci["D intero"], bracci["D ritagliato"], bracci["caos"]):
        q = a / c
        peggio = max(peggio, q)
        n_sopra += 1 if q > FATTORE else 0
        print("  %-8.1f %.3e   %.3e    %.3e   %.3f%s" % (t, a, b, c, q, "   ### SOPRA %g" % FATTORE if q > FATTORE else ""))
    print("ESITO: il rapporto massimo %.3f; tempi sopra %g: %d su %d -> %s" % (peggio, FATTORE, n_sopra, len(bracci["caos"]), "PASSA" if n_sopra == 0 else "### FALLISCE"))
    return 0 if n_sopra == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
