# -*- coding: utf-8 -*-
r"""**[M1631] LE SEI TENUTE ALLA CIMA, LA SERIE: w, IL PICCO, I PEZZI OGNI 250 TICK** *(sola lettura degli stati di `torneo_tenuta.py corsa`; nessun criterio nuovo: dice se la contrazione e' monotona o un respiro)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/torneo_serie.py > doc/referti_l2/torneo_serie.txt

**Per ogni corsa in `E:\soliton_simulator\controllo\M1631\tenuta`:** a ogni stato `w` e i pezzi *(le funzioni di `torneo_tenuta`)*, il picco lisciato; **il numero di inversioni del verso di `w`** fra stati successivi *(`0` = monotona)*; il minimo di `w` e il suo `k`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import torneo_tenuta as TT  # noqa: E402


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "torneo_tenuta.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1631] LE SEI TENUTE ALLA CIMA, LA SERIE (sola lettura)")
    print("=" * 130)
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()
    for nome in sorted(os.listdir(TT.DIR)):
        d = os.path.join(TT.DIR, nome)
        fs = sorted(f for f in os.listdir(d) if f.startswith("stato_") and f.endswith(".npz"))
        serie = []
        for f in fs:
            w, p, mx, _M = TT.misura(os.path.join(d, f), nodo, n, L)
            serie.append((int(f[6:12]), w, p, mx))
        ws = np.array([x[1] for x in serie])
        dw = np.sign(np.diff(ws))
        inv = int(np.sum(dw[1:] * dw[:-1] < 0))
        i = int(np.argmin(ws))
        print("  %s: le inversioni del verso di w %d; il minimo di w %.3f a k %d; w a k 0 %.3f, a k 3000 %.3f" % (nome, inv, ws[i], serie[i][0], ws[0], ws[-1]))
        print("    k:     %s" % " ".join("%6d" % x[0] for x in serie))
        print("    w:     %s" % " ".join("%6.2f" % x[1] for x in serie))
        print("    picco: %s" % " ".join("%6.0f" % x[3] for x in serie))
        print("    pezzi: %s" % " ".join("%6d" % x[2] for x in serie))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
