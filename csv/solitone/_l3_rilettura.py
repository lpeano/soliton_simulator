# -*- coding: utf-8 -*-
r"""**L3 RILETTA SUGLI INVILUPPI** *(Luca `2026-11-07` `18:02`, che corregge il criterio punto per punto delle `17:55`: l'errore `n.117` del guardiano)*:
**solo lettura del referto** `doc/referti_l2/libreria_solitoni.txt` *(`libreria.py` `27a897f1`, `9eda4121`)*, **le righe dei tre bracci ai tempi stampati** *(ogni `1000` tick)*.

    python csv/solitone/_l3_rilettura.py > doc/referti_l2/libreria_l3_rilettura.txt

### **Il criterio** *(Luca `18:02`)*: **per ciascuna delle SEI grandezze** *(la massa e l'energia del cuore, della corona, della fascia)* **l'INVILUPPO** *(il massimo corrente da `t 0`
fino a `t`)* **col `D` intero non supera di piu' di un fattore `2` l'inviluppo del braccio del caos, a ogni tempo stampato.** **DICHIARATO:** la soglia fissata dopo i numeri,
ancorata al braccio del caos misurato prima. **In piu' stampati, senza verdetto:** i valori, gli inviluppi, e lo stesso per il `D` ritagliato.
### ⚠ **I tempi stampati sono `7` per braccio** *(la carta campionava ogni `100` tick ma stampava una riga ogni `10` campioni)*: **la rilettura vale su QUEI tempi.**
"""
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401

FATTORE = 2.0   # ### Luca 17:55-18:02 (dopo i numeri, ancorato al braccio del caos: dichiarato)
REFERTO = os.path.join(solitone.RADICE, "doc", "referti_l2", "libreria_solitoni.txt")
REFERTO_LOC = os.path.join(solitone.RADICE, "doc", "referti_l2", "libreria_caos_locale.txt")   # ### Luca 18:22: il braccio del caos solo fuori da R_t
NOMI = ("M cuore", "M corona", "M fascia", "E cuore", "E corona", "E fascia")


def main():
    import numpy as np
    import _presidio
    _presidio.avvia(__file__)
    righe = open(REFERTO, encoding="utf-8").read().splitlines()
    if os.path.exists(REFERTO_LOC):
        righe += open(REFERTO_LOC, encoding="utf-8").read().splitlines()
    bracci, cur = {}, None
    for r in righe:
        m = re.match(r"\s+(D intero|D ritagliato|caos locale|caos)\s+il massimo", r)
        if m:
            cur = m.group(1)
            bracci[cur] = []
            continue
        m = re.match(r"\s+t\s+([0-9.]+)\s+M cuore ([0-9.e+-]+) corona ([0-9.e+-]+) fascia ([0-9.e+-]+)\s+E ([0-9.e+-]+) ([0-9.e+-]+) ([0-9.e+-]+)", r)
        if m and cur is not None:
            bracci[cur].append([float(x) for x in m.groups()])
    assert {"D intero", "D ritagliato", "caos"} <= set(bracci), "le righe dei tre bracci NON si leggono"
    A = {k: np.array(v) for k, v in bracci.items()}
    t = A["D intero"][:, 0]
    assert np.array_equal(t, A["caos"][:, 0]) and np.array_equal(t, A["D ritagliato"][:, 0])
    vecchio = A["caos"]
    if "caos locale" in A:
        # ### Luca 18:22: il riferimento e' il braccio LOCALIZZATO, alle STESSE t stampate (il nuovo referto ha tutte le righe, ogni 100 tick)
        loc = A["caos locale"]
        idx = [int(np.argmin(np.abs(loc[:, 0] - x))) for x in t]
        assert np.allclose(loc[idx, 0], t), "i tempi del braccio localizzato NON coincidono con quelli stampati"
        A["caos"] = loc[idx]
        print("### IL RIFERIMENTO E' IL BRACCIO DEL CAOS LOCALIZZATO (Luca 18:22, %s); accanto il braccio vecchio su tutto il toro (dichiarato)" % os.path.basename(REFERTO_LOC))
    A["caos vecchio"] = vecchio
    inv = {k: np.maximum.accumulate(v[:, 1:], axis=0) for k, v in A.items()}
    print("L3 RILETTA SUGLI INVILUPPI (Luca 18:02): per ciascuna grandezza l'inviluppo (il massimo corrente) col D intero / quello del caos <= %g a ogni tempo; dal referto %s; %d tempi stampati"
          % (FATTORE, os.path.basename(REFERTO), len(t)))
    peggio, sopra = 0.0, []
    for q, nome in enumerate(NOMI):
        print("### %s" % nome)
        print("  %-8s %-11s %-11s %-11s %-11s %-9s %-11s %-11s %-11s" % ("t", "D intero", "caos", "inv intero", "inv caos", "rapporto", "D ritagl.", "inv ritagl.", "rap. vecchio"))
        for i in range(len(t)):
            r_ = inv["D intero"][i, q] / inv["caos"][i, q]
            peggio = max(peggio, r_)
            if r_ > FATTORE:
                sopra.append((nome, t[i], r_))
            print("  %-8.1f %.3e   %.3e   %.3e   %.3e   %7.3f%s  %.3e   %.3e   %7.3f" % (t[i], A["D intero"][i, q + 1], A["caos"][i, q + 1], inv["D intero"][i, q], inv["caos"][i, q], r_,
                                                                       " ###" if r_ > FATTORE else "    ", A["D ritagliato"][i, q + 1], inv["D ritagliato"][i, q],
                                                                       inv["D intero"][i, q] / inv["caos vecchio"][i, q]))
    print("ESITO: il rapporto massimo degli inviluppi %.3f; sopra %g: %d %s -> %s" % (peggio, FATTORE, len(sopra), ["%s t %.1f %.3f" % x for x in sopra], "PASSA" if not sopra else "### FALLISCE"))
    return 0 if not sopra else 1


if __name__ == "__main__":
    sys.exit(main())
