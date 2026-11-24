# -*- coding: utf-8 -*-
r"""**[M0118-00] L'EOTVOS AL FONDO A K NELLE DUE CONVENZIONI** *(DECISIONE DI LUCA, 2026-11-24 01:25; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-sexies`, l'annotazione; `eotvos_fondo.py` e' usato e non si riscrive)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/eotvos_fondo_v2.py >> doc/referti_l2/eotvos_fondo.txt

**K(1c) e K(a2), VUOTO e CIMA** *(`fondo_s3_v2.due_K`: `omega_psi(N1)` dell'orologio V2 di 1c per entrambe, come il `grad omega` di S3; per a2, accanto, la CIMA con l'`omega` del SUO calcio a `k 0`, mia aggiunta dichiarata)*, sull'intera `[200, 2000]` e sulle finestre di `600`; **eta** non dipende dalla convenzione *(rapporto di `a`)*: ristampata.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import eotvos_fondo as EF  # noqa: E402
import fondo_s3_v2 as S3V2  # noqa: E402

F1 = EF.F1


def lettura():
    import _presidio
    import caduta_finestre as CF
    F1.avvia()
    for m in ("eotvos_fondo.py", "fondo_s3_v2.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    MC = F1.MC
    print("=" * 130)
    print("[M0118-00] L'EOTVOS AL FONDO A K NELLE DUE CONVENZIONI (la carta sez. 2-sexies, l'annotazione): VUOTO e CIMA")
    print("=" * 130)
    F1.BASE = EF.BASE_1C
    dD, w1 = S3V2.pendenze()
    print("  d Delta/dN %+.6f (VUOTO); omega_psi(N1) %+.7f (CIMA, l'orologio V2 di 1c a N 1)" % (dD, w1))
    A_ = {}
    for nome, base in (("1c (massa 1)", EF.BASE_1C), ("a2 (massa 4)", EF.BASE_A2)):
        ms = EF.mstar_K(base)
        F1.BASE = base
        c, c0 = F1.leggi("caduta_V2"), F1.leggi("caduta_V0")
        r0 = F1.leggi("calcio_%s" % MC.nome(0.0, 1))
        w_proprio = float(np.mean(r0["omega"]))
        print("  %s: m* %+.4f +- %.4f; omega del suo calcio a k 0 %+.7f" % (nome, ms[0], ms[1], w_proprio))
        for w in S3V2.FINESTRE:
            a, sa, _ = CF.fit(c["serie"], *w)
            a0, sa0, _ = CF.fit(c0["serie"], *w)
            da, sda = a - a0, math.hypot(sa, sa0)
            kv, kc, sv, scc = S3V2.due_K(da, sda, float(c["A"]), ms[0], dD, w1)
            _kv, kp, _sv, sp = S3V2.due_K(da, sda, float(c["A"]), ms[0], dD, w_proprio)
            if w == (200, 2000):
                A_[nome] = (da, sda)
            print("    [%4d, %4d]: a - a(V0) %+.4e +- %.1e;   K VUOTO %+.4f +- %.4f;   K CIMA %+.4f +- %.4f;   (CIMA con l'omega proprio %+.4f +- %.4f)" % (w[0], w[1], da, sda, kv, sv, kc, scc, kp, sp))
    (a1, s1), (a2, s2) = A_["1c (massa 1)"], A_["a2 (massa 4)"]
    eta = 2.0 * abs(a1 - a2) / (a1 + a2)
    se = 4.0 * math.hypot(a2 * s1, a1 * s2) / (a1 + a2) ** 2
    print("### eta (non dipende dalla convenzione) = %.4f +- %.4f (a_i = a - a(V0) su [200, 2000])" % (eta, se))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(lettura())
