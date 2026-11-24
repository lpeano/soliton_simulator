# -*- coding: utf-8 -*-
r"""**[M0140] w(k) DELLA V0 DI l0.7 ACCANTO A QUELLA DELLA V2** *(DECISIONE DI LUCA, 2026-11-24 01:40; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-undecies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/forma_l07.py >> doc/referti_l2/k_forma.txt

**`torneo_tenuta.misura`** *(`w`, i pezzi, il picco lisciato, la massa)* sugli stati ogni `250` di `M1658/c1_l07/caduta_V0` e `caduta_V2`, una riga per `k`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import k_forma as KF  # noqa: E402
import torneo_tenuta as TT  # noqa: E402


def main():
    import _presidio
    for m in ("k_forma.py", "torneo_tenuta.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("-" * 130)
    print("[M0140] w(k) DI l0.7: LA V0 ACCANTO ALLA V2 (torneo_tenuta.misura sugli stati ogni 250)")
    print("-" * 130)
    with TT.TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()
    for k in range(0, 2001, 250):
        r = []
        for coll in ("V0", "V2"):
            f = os.path.join(KF.BASE_L07, "caduta_%s" % coll, "stato_%06d.npz" % k)
            if not os.path.exists(f + ".sha1"):
                r.append("%s: MANCA" % coll)
                continue
            w, p, mx, M = TT.misura(f, nodo, n, L)
            r.append("%s: w %.3f, i pezzi %d, il picco %.4e, la massa %.6f" % (coll, w, p, mx, M))
        print("  k %4d:   %s" % (k, ";   ".join(r)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
