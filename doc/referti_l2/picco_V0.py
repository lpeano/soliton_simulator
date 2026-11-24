# -*- coding: utf-8 -*-
r"""**[M1446-Q] IL PICCO DEL MATTONE DI RIFERIMENTO (V0, LA NORMA x1) NEL TEMPO** *(la tenuta di `eotvos.py` misura il picco dei solitoni riscalati contro il proprio `k 0`: serve il riferimento; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/picco_V0.py > doc/referti_l2/picco_V0.txt

Il picco di `rho` *(da `psi_h`, i semiarchi `girandola_chi_v3.toro_nodo(162)`)* negli stati `0 ... 2000` di `CHI/caduta/V0` *(lo sha1 controllato)*; **la chiave `rho` dello stato NON si usa** *(a `k 0` vale `3313.6` contro `1192.7` da `psi_h`: non e' aggiornata a `k 0`)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402,F401  (i percorsi)
import caduta_libera as CL  # noqa: E402
import girandola_chi_v3 as GC  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402


def main():
    import _presidio
    _presidio.avvia(__file__)
    nodo = GC.toro_nodo(162)
    print("=" * 100)
    print("[M1446-Q] IL PICCO DI rho DEL MATTONE V0 (la norma x1, N = 1), da psi_h")
    print("=" * 100)
    p0 = None
    for k in range(0, 2001, 250):
        X, _m = GM.leggi(os.path.join(CL.BASE, "V0", "stato_%06d.npz" % k))
        r = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=162 * 162)
        p0 = p0 or float(r.max())
        print("  k %4d: il picco %.4f (%+.1f%% da k 0); la chiave rho dello stato %.4f; la norma %.6e" % (k, float(r.max()), 100 * (float(r.max()) / p0 - 1.0), float(X["rho"].max()), float(r.sum())))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
