# -*- coding: utf-8 -*-
r"""**[M0015-02] LA LETTURA DELLE TENUTE DI [M2305]** *(il mandato dice `tenuta_fondo_v2.py lettura`: quello script e' usato e non ha `lettura`; un file nuovo, le righe di `tenuta_fondo.lettura` sulle cartelle di `tenuta_fondo_v2`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/tenuta_fondo_v2_lettura.py > doc/referti_l2/tenuta_fondo_v2.txt

**Per le sei corse** *(`M1658/tenuta_v2/<forma>_a<f>_l<s>`)*: `w` e i pezzi ogni `250` *(`torneo_tenuta.misura`)*; **K-T v2** `w(3000)/w(1500)` in `[0.7, 1.3]` e un pezzo a `3000`; `omega` su `[2500, 3000]` e se e' nel gap `(0.011870, 0.245338)`; la massa a `k 3000`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import tenuta_fondo as TF  # noqa: E402
import tenuta_fondo_v2 as TF2  # noqa: E402

CORSE = ("L-1_a0.5_l1.0", "L-1_a2.0_l1.0", "L-1_a1.0_l0.7", "L-1_a1.0_l1.4", "L0_a0.5_l1.0", "L0_a2.0_l1.0")


def main():
    import _presidio
    import gravita_due_corpi_misure as GM
    _presidio.avvia(os.path.join(_QUI, "tenuta_fondo.py"))
    _presidio.avvia(os.path.join(_QUI, "tenuta_fondo_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0015-02] LE TENUTE DI [M2305] (K-T v2: w(3000)/w(1500) in [0.7, 1.3] e un pezzo a 3000; omega su [2500, 3000] nel gap %s)" % (TF.GAP,))
    print("=" * 130)
    with TF.TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()
    for nome in CORSE:
        d = os.path.join(TF2.DIR2, nome)
        if not os.path.exists(os.path.join(d, "stato_003000.npz.sha1")):
            print("  %s: NON FINITA" % nome)
            continue
        _X, meta = GM.leggi(os.path.join(d, "stato_000000.npz"))
        om = np.load(os.path.join(d, "omega.npy"))
        print("  %s: l'ampiezza %s, la larghezza %s; la frazione proiettata %.6f" % (nome, meta.get("ampiezza"), meta.get("larghezza"), meta.get("frazione_proiettata", float("nan"))))
        ks = {}
        for k in range(0, 3001, 250):
            w, p, mx, M = TF.TT.misura(os.path.join(d, "stato_%06d.npz" % k), nodo, n, L)
            ks[k] = (w, p, mx, M)
            if k % 750 == 0:
                print("    k %5d: w %.3f, i pezzi %d, il picco lisciato %.4e, la massa %.6f" % (k, w, p, mx, M))
        r = ks[3000][0] / ks[1500][0]
        regge = 0.7 <= r <= 1.3 and ks[3000][1] == 1
        o = om[2499:3000]
        om_m, om_s = float(o.mean()), float(o.std() / math.sqrt(len(o)))
        nel = TF.GAP[0] < om_m < TF.GAP[1]
        print("    K-T v2: w(3000)/w(1500) %.3f, i pezzi a 3000 %d: %s; omega [1, 500] %+.7f, [2500, 3000] %+.7f +- %.1e: %s; la massa a k 3000 %.6f (a k 0 %.6f)" % (
            r, ks[3000][1], "REGGE" if regge else "### NON REGGE", float(om[:500].mean()), om_m, om_s, "NEL GAP" if nel else "fuori dal gap", ks[3000][3], ks[0][3]))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
