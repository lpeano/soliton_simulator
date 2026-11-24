# -*- coding: utf-8 -*-
r"""**[M1330-B5] L'OGGETTO EFFICACE: m* IN FUNZIONE DI w** *(DECISIONE DI LUCA, 2026-11-24 13:30; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-ter`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mstar_w.py calcio --da 1500 --k 0.010      (--da 500, 1500; --k 0.0, 0.010: 1000 tick)
    E:\python\py3132\python.exe doc/referti_l2/mstar_w.py lettura >> doc/referti_l2/k_forma.txt

**`fondo_1c.calcio` cosi' com'e'**, con `fondo_1c.OGGETTO` = lo stato `k <da>` della V0 di l0.7 *(`M1658/c1_l07/caduta_V0/stato_<da>.npz`)* e `fondo_1c.BASE` = `M1330/mstar_w/k<da>`, in memoria. **La lettura:** `m*(w)` per i due stati, il rapporto, e K CIMA delle finestre di l0.7 con l'uno e con l'altro `m*`, accanto al `w` medio della finestra.
"""
import argparse
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import eotvos_fondo as EF  # noqa: E402
import k_forma as KF  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
V0_L07 = os.path.join(CTRL, "M1658", "c1_l07", "caduta_V0")
V2_L07 = os.path.join(CTRL, "M1658", "c1_l07", "caduta_V2")
BASE = os.path.join(CTRL, "M1330", "mstar_w")
DA = (500, 1500)
FINESTRE = ((200, 800), (800, 1400), (1400, 2000))


def su(da):
    F1.OGGETTO = os.path.join(V0_L07, "stato_%06d.npz" % da)
    F1.BASE = os.path.join(BASE, "k%d" % da)


def lettura():
    import _presidio
    import caduta_finestre as CF
    import fondo_s3_v2 as S3V2
    F1.avvia()
    for m in ("eotvos_fondo.py", "k_forma.py", "fondo_s3_v2.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("-" * 130)
    print("[M1330-B5] m* IN FUNZIONE DI w (la carta sez. 3-ter): i calci dagli stati k 500 e k 1500 della V0 di l0.7")
    print("-" * 130)
    with F1.TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()
    M = {}
    for da in DA:
        w = F1.TT.misura(os.path.join(V0_L07, "stato_%06d.npz" % da), nodo, n, L)[0]
        ms = EF.mstar_K(os.path.join(BASE, "k%d" % da))
        if ms is None:
            print("  da k %d (w %.3f): NON FINITA" % (da, w))
            continue
        M[da] = (w, ms[0], ms[1])
        print("  da k %d della V0 di l0.7: w %.3f; m* %+.4f +- %.4f" % (da, w, ms[0], ms[1]))
    if len(M) == 2:
        print("### m*(w %.3f)/m*(w %.3f) = %.4f" % (M[500][0], M[1500][0], M[500][1] / M[1500][1]))
    F1.BASE = KF.BASE_1C
    dD, w1 = S3V2.pendenze()
    x = KF.legge(KF.BASE_L07)
    if x is None or not M:
        print("=" * 130)
        return 0
    _ms, _sms, s2, s0, A = x
    for wd in FINESTRE:
        ws = [F1.TT.misura(os.path.join(V2_L07, "stato_%06d.npz" % k), nodo, n, L)[0] for k in range(0, 2001, 250) if wd[0] <= k <= wd[1]]
        a, sa, _ = CF.fit(s2, *wd)
        a0, sa0, _ = CF.fit(s0, *wd)
        r = []
        for da in sorted(M):
            _kv, kc, _sv, scc = S3V2.due_K(a - a0, math.hypot(sa, sa0), A, M[da][1], dD, w1)
            r.append("con m*(w %.3f) %+.4f +- %.4f" % (M[da][0], kc, scc))
        print("  l0.7 V2 [%4d, %4d]: w medio %.3f (gli stati %s); K CIMA %s" % (wd[0], wd[1], float(np.mean(ws)), " ".join("%.2f" % v for v in ws), ";  ".join(r)))
    print("=" * 130)
    return 0


def main(argv):
    import _presidio
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("calcio", "lettura"))
    ap.add_argument("--da", type=int, choices=DA)
    ap.add_argument("--k", type=float)
    a = ap.parse_args(argv)
    if a.cosa == "lettura":
        return lettura()
    su(a.da)
    _presidio.avvia(__file__)
    return F1.calcio(a.k)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
