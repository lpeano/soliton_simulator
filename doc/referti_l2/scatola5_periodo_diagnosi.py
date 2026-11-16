# -*- coding: utf-8 -*-
r"""**PERCHE' IL PERIODO DEL RESPIRO DI `L 186` NON E' QUELLO DI `L 324`?** *(la diagnosi DOPO il verdetto: il verdetto NON cambia, le soglie non si rivedono)*.

    E:\python\py3132\python.exe doc/referti_l2/scatola5_periodo_diagnosi.py > doc/referti_l2/scatola5_periodo_diagnosi.txt

**Lo stesso calcolo di `prova_scatola5.periodo`** *(il picco meno la media mobile su `101` tick, la FFT sui tick `250`-`1750`)*, **ma invece del solo argmax: le prime `6` componenti con la loro ampiezza** *(e il rapporto fra la seconda e la prima)*, **per `L 186` e `L 324`; e il periodo sulla finestra `1000`-`2500` di `L 186`** *(la stessa lunghezza; `L 324` ha la serie solo fino a `2000`, dichiarato)*.
"""
import os
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(QUI))
REF = os.path.join(QUI, "mattone")


def spettro(k, p, da, a):
    k = np.asarray(k)
    p = np.asarray(p, dtype=float)
    m = (k >= da - 50) & (k <= a + 50)
    k, p = k[m], p[m]
    o = np.argsort(k)
    k, p = k[o], p[o]
    assert np.all(np.diff(k) == 1)
    mm = np.convolve(p, np.ones(101) / 101.0, mode="same")
    q = (p - mm)[(k >= da) & (k <= a)]
    F = np.abs(np.fft.rfft(q - q.mean()))
    f = np.fft.rfftfreq(len(q), 1.0)
    j = 1 + np.argsort(F[1:])[::-1][:6]
    return len(q), [(1.0 / f[i], float(F[i]), int(i)) for i in j]


def main():
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    s5 = np.load(os.path.join(QUI, "prova_scatola5_L186_serie_00000.npz"))
    s3 = np.load(os.path.join(REF, "porto_cottura_serie_00000.npz"))
    print("=" * 110)
    print("IL PERIODO DEL RESPIRO, LA DIAGNOSI (lo stesso calcolo di prova_scatola5.periodo; le prime 6 componenti invece del solo argmax)")
    print("=" * 110)
    for nome, s, da, a in (("L 186", s5, 250, 1750), ("L 324", s3, 250, 1750), ("L 186", s5, 1000, 2500)):
        n, top = spettro(s["pk_k"], s["picco"], da, a)
        print("### %s, i tick %d-%d (%d campioni; la risoluzione: i periodi %d/n):" % (nome, da, a, n, n))
        for T, A, i in top:
            print("    n %3d  il periodo %8.2f tick  l'ampiezza %.4e  (%.3f della prima)" % (i, T, A, A / top[0][1]))
    print("=" * 110)
    return 0


if __name__ == "__main__":
    sys.exit(main())
