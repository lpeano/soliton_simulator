# -*- coding: utf-8 -*-
r"""**[M0037-01bis] LA CADUTA A FINESTRE -- LA V2** *(`caduta_finestre.py` cadde, `9aef7cb1`: le nette leggevano `R["caduta_V0"]` prima che fosse calcolato; errore mio di ordine)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_finestre_v2.py > doc/referti_l2/caduta_finestre.txt

**Una sola differenza:** le finestre di TUTTE le cadute si calcolano prima di stampare; `fit`, `vel`, la soglia e i casi noti sono quelli della v1 *(importati)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import caduta_finestre as CF  # noqa: E402

F1, FINESTRE, CADUTE, fit, vel = CF.F1, CF.FINESTRE, CF.CADUTE, CF.fit, CF.vel


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_1c.py"))
    _presidio.avvia(os.path.join(_QUI, "caduta_finestre.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0037-01bis] LA CADUTA A FINESTRE, LA V2 (la carta sez. 2-octies): a per finestra (estremi compresi), v(k) su [k-50, k+50]")
    print("=" * 130)
    S = {c: F1.leggi(c) for c in CADUTE}
    for c in CADUTE:
        assert S[c] is not None, "%s NON c'e'" % c
    print("  IL CASO NOTO:")
    a_f, s_f, _ = F1.fit_a(S["caduta_V2"]["serie"])
    a_w, s_w, n_w = fit(S["caduta_V2"]["serie"], 200, 2000)
    ok = a_w == a_f and s_w == s_f
    print("    DEVE: [200, 2000] della V2 x1 = fondo_1c.fit_a AL BIT: %s (a %+.4e, fit_a %+.4e; contro +6.2969e-07: %s)" % (
        "PASSA" if ok else "### FALLISCE", a_w, a_f, "COINCIDE" if "%+.4e" % a_w == "+6.2969e-07" else "### NON COINCIDE"))
    a_x, _s, _n = fit(S["caduta_V2"]["serie"], 200, 1990)
    ko = a_x != a_f
    print("    DEVE FALLIRE: [200, 1990] diversa al bit: %s (a %+.4e)" % ("PASSA (e' diversa)" if ko else "### FALLISCE (uguale)", a_x))
    R = {c: [fit(S[c]["serie"], *w) for w in FINESTRE] for c in CADUTE}
    for c in CADUTE:
        se = S[c]["serie"]
        print("  %s (A %s):" % (c, S[c].get("A")))
        for w, (a, sa, n) in zip(FINESTRE, R[c]):
            print("    [%4d, %4d]: a %+.4e +- %.1e (%d punti)" % (w[0], w[1], a, sa, n))
        if c != "caduta_V0":
            for w, (a, sa, n), (a0, sa0, _n0) in zip(FINESTRE, R[c], R["caduta_V0"]):
                print("    [%4d, %4d] NETTA (a - a(V0) nella stessa finestra): %+.4e +- %.1e" % (w[0], w[1], a - a0, math.hypot(sa, sa0)))
        vs = ["k %d: %+.3e" % (kc, vel(se, kc)[0]) for kc in range(200, 1801, 200)]
        s = np.array(se)
        m = s[:, 0] >= 1900
        cc = np.polyfit(s[m, 0], s[m, 2], 1)
        vs.append("k 2000 [1900, 2000]: %+.3e" % float(cc[0]))
        print("    v(k): " + "; ".join(vs))
    print("  (b) LA SOGLIA (la carta: sulla V2 x1 NETTA, a[1400, 2000] > 1.2 a[200, 800]):")
    n1 = R["caduta_V2"][0][0] - R["caduta_V0"][0][0]
    n3 = R["caduta_V2"][2][0] - R["caduta_V0"][2][0]
    g1, g3 = R["caduta_V2"][0][0], R["caduta_V2"][2][0]
    dn, dg = n3 > 1.2 * n1, g3 > 1.2 * g1
    print("    NETTA: ultima/prima %.4f -> %s; GREZZA: ultima/prima %.4f -> %s" % (n3 / n1, "SUPERA" if dn else "non supera", g3 / g1, "SUPERA" if dg else "non supera"))
    if dn != dg:
        print("### LA NETTA E LA GREZZA DECIDONO DIVERSAMENTE: FERMO (la carta)")
    else:
        print("### (b): %s" % ("SI LANCIA M0037_caduta_lunga" if dn else "NON SI LANCIA: [M0037-01] resta la pista"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
