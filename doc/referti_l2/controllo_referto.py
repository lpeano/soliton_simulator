# -*- coding: utf-8 -*-
r"""**IL REFERTO DEL CONTROLLO SENZA BORDO** *(Luca `2026-11-17` `15:22`, TODO 4; la carta `doc/TASK_HISTORY/2026-11-17_controllo_senza_bordo.md`)*.

    E:\python\py3132\python.exe doc/referti_l2/controllo_referto.py > doc/referti_l2/controllo_senza_bordo.txt

**Le serie** *(scritte a fine corsa da `controllo_senza_bordo.py`: `doc/referti_l2/controllo_C1_serie.npz`, `controllo_C2_serie.npz`; una misura ogni `50` tick)*: **C1** `L 186` col bordo, **C2** `L 186` senza bordo. **Le previsioni P-SB1..P-SB5** *(copiate nella carta PRIMA delle corse)* **VERE o FALSE coi numeri**; **la parte di P-SB4 su C3 DECADE** *(C3 annullata da Luca alle `16:02`)*. **La figura:** il flusso netto e la parte positiva agli anelli `30` e `45` nel tempo, C1 contro C2 *(`controllo_senza_bordo.png`)*.
**I criteri, come scritti nella carta:** P-SB1 la norma di C2 entro `1e-12` relativo su tutti i tick; P-SB2 il flusso NETTO di C2 agli anelli `30` e `45`, medio sugli ultimi `500` tick *(`k >= 2500`)*, sotto il `20%` di quello di C1; P-SB3 la parte POSITIVA di C2 sopra il `50%` di C1 *(stessi tick)*; P-SB4 il primo tick in cui il flusso netto all'anello `45` di C2 e di C1 differisce oltre il `10%` *(di `|C1|`)* sta prima di `400`; P-SB5 la massa entro `12.4` a `k 3000` piu' alta in C2, e R_ogg al `5%` di C2 oltre `25`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv")):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def carica(nome):
    with np.load(os.path.join(_QUI, "controllo_%s_serie.npz" % nome)) as d:
        return {x: np.asarray(d[x], dtype=float) for x in d.files}


def main():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL CONTROLLO SENZA BORDO, IL REFERTO (Luca 2026-11-17 15:22): C1 L 186 col bordo, C2 L 186 senza bordo")
    print("=" * 130)
    S1, S2 = carica("C1"), carica("C2")
    assert np.array_equal(S1["k"], S2["k"]), "le due serie non hanno gli stessi tick"
    k = S1["k"]
    print("### le serie: %d misure, da k %d a k %d" % (k.size, int(k[0]), int(k[-1])))
    print("-" * 130)
    print("%6s | %15s %15s | %13s %13s | %6s %6s | %12s %12s | %11s %11s | %11s %11s" % (
        "k", "M C1", "M C2", "Min12.4 C1", "Min12.4 C2", "R5 C1", "R5 C2", "E C1", "E C2", "J30n C1", "J30n C2", "J45n C1", "J45n C2"))
    for q in range(k.size):
        if int(k[q]) % 250 == 0:
            print("%6d | %.9e %.9e | %.7e %.7e | %6.1f %6.1f | %+.5e %+.5e | %+.4e %+.4e | %+.4e %+.4e" % (
                int(k[q]), S1["M"][q], S2["M"][q], S1["Min_12.4"][q], S2["Min_12.4"][q], S1["R5"][q], S2["R5"][q], S1["E"][q], S2["E"][q],
                S1["Jn_30"][q], S2["Jn_30"][q], S1["Jn_45"][q], S2["Jn_45"][q]))
    print("-" * 130)
    esiti = []
    # P-SB1
    dM = float(np.max(np.abs(S2["M"] - S2["M"][0]))) / float(S2["M"][0])
    dE = (float(S2["E"][-1]) - float(S2["E"][0])) / abs(float(S2["E"][0]))
    print("P-SB1: C2, la norma: max |M - M(0)| / M(0) = %.3e; l'energia (nessuna previsione): (E(3000) - E(0)) / |E(0)| = %+.3e" % (dM, dE))
    esiti.append(("P-SB1: la norma di C2 conservata entro 1e-12 relativo su tutti i tick misurati", dM <= 1e-12))
    # P-SB2, P-SB3
    ult = k >= 2500
    for R in (30, 45):
        n1, n2 = float(np.mean(S1["Jn_%d" % R][ult])), float(np.mean(S2["Jn_%d" % R][ult]))
        p1, p2 = float(np.mean(S1["Jp_%d" % R][ult])), float(np.mean(S2["Jp_%d" % R][ult]))
        print("P-SB2/3: l'anello %d, gli ultimi 500 tick (%d misure): il netto C1 %+.5e, C2 %+.5e (C2/C1 %+.4f); il positivo C1 %.5e, C2 %.5e (C2/C1 %.4f)" % (R, int(ult.sum()), n1, n2, n2 / n1, p1, p2, p2 / p1))
        esiti.append(("P-SB2: all'anello %d il netto di C2 sotto il 20%% di C1 (|C2/C1| %.4f)" % (R, abs(n2 / n1)), abs(n2 / n1) < 0.20))
        esiti.append(("P-SB3: all'anello %d il positivo di C2 sopra il 50%% di C1 (%.4f)" % (R, p2 / p1), p2 / p1 > 0.50))
    # P-SB4
    rel = np.abs(S2["Jn_45"] - S1["Jn_45"]) / np.maximum(np.abs(S1["Jn_45"]), 1e-300)
    oltre = np.where((rel > 0.10) & (k > 0))[0]
    k4 = int(k[oltre[0]]) if oltre.size else None
    print("P-SB4: il primo tick misurato in cui il netto all'anello 45 di C2 differisce da C1 oltre il 10%% di |C1|: %s (la risoluzione: una misura ogni %d tick); la parte su C3 DECADE" % (k4, int(k[1] - k[0])))
    esiti.append(("P-SB4: il primo scarto oltre il 10%% all'anello 45 prima del tick 400 (%s)" % k4, k4 is not None and k4 < 400))
    # P-SB5
    m1, m2 = float(S1["Min_12.4"][-1]), float(S2["Min_12.4"][-1])
    r2 = float(S2["R5"][-1])
    print("P-SB5: k %d, la massa entro 12.4: C1 %.7e, C2 %.7e (C2 - C1 %+.4e); R_ogg al 5%% di C2 %.1f (C1 %.1f)" % (int(k[-1]), m1, m2, m2 - m1, r2, float(S1["R5"][-1])))
    esiti.append(("P-SB5: la massa entro 12.4 a k 3000 piu' alta in C2", m2 > m1))
    esiti.append(("P-SB5: R_ogg al 5%% di C2 oltre 25 (%.1f)" % r2, r2 > 25.0))
    figura(k, S1, S2)
    print("### la figura: controllo_senza_bordo.png (il netto e il positivo agli anelli 30 e 45, C1 contro C2)")
    print("-" * 130)
    for nm, ok in esiti:
        print("  PREVISIONE: %-105s %s" % (nm, "VERA" if ok else "FALSA"))
    print("=" * 130)
    return 0


def figura(k, S1, S2):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 2, figsize=(11, 7), sharex=True)
    for i, R in enumerate((30, 45)):
        for j, (ch, nm) in enumerate((("Jn", "il netto"), ("Jp", "la parte positiva"))):
            a = ax[i][j]
            a.plot(k, S1["%s_%d" % (ch, R)], color="#3b6fb6", lw=1.2, label="C1 (col bordo)")
            a.plot(k, S2["%s_%d" % (ch, R)], color="#c4522b", lw=1.2, label="C2 (senza bordo)")
            a.axhline(0.0, color="#888888", lw=0.6)
            a.set_title("%s del flusso all'anello %d" % (nm, R), fontsize=10)
            a.grid(alpha=0.3)
            if i == 1:
                a.set_xlabel("tick")
    ax[0][0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(_QUI, "controllo_senza_bordo.png"), dpi=110)


if __name__ == "__main__":
    sys.exit(main())
