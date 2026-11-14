# -*- coding: utf-8 -*-
r"""**A CHE DISTANZA STAVA IL BORDO DALLA CODA DEL SOLITONE, SU `L 81`** *(Luca `2026-11-14` `15:49`, in coda, SOLO LETTURA; l'errore del guardiano n.161)*.

    python csv/solitone/bordo_coda_L81.py > doc/referti_l2/bordo_coda_L81.txt

**Le corse su `L 81` nella scena di TBS** *(il bordo di TBS: `R_A = 28` dal suo centro, la rampa `sin^2` fino a `R_B` = la meta' del periodo, `40.5`)*: **G1** *(`campo_g1`, `campo_g1_lunga`, `campo_g1_lunghissima`)* **e il «pendolo»** *(il video triplo, `campo_g1_tre` A, B, C)*.
**Per ogni mappa di `rho` salvata:** **la distanza del centro del solitone dal centro del bordo; i raggi `R99` e `R999`** *(dal centro del solitone, la massa entro il `99%` e il `99.9%`)*; **la coda verso il bordo: `d + R99` e `d + R999`** *(il punto
piu' lontano dal centro del bordo, nella direzione peggiore)*; **la massa OLTRE `R_A` dal centro del bordo** *(relativa)*. **Nessuna corsa.**
### **E (Luca `17:02`, (2); l'errore del guardiano n.162): la scena di C35-pi dei bracci di P6 e quella di S162: i loro `R_A` e `R_B` VERI; per `Grampa` e `(0)_2000` la massa dei due solitoni oltre `R_A` a `0`, `1000`, `2000` tick.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import solitone  # noqa: E402,F401

RADICE = os.path.dirname(_CSV)
REF = os.path.join(RADICE, "doc", "referti_l2")
FILE = (("G1 gamma 0", "campo_g1/g1_campo_gamma000.npz"), ("G1 gamma 0.2", "campo_g1/g1_campo_gamma020.npz"), ("G1 lunga", "campo_g1_lunga/g1_lunga.npz"),
        ("G1 lunghissima", "campo_g1_lunghissima/g1_lunghissima.npz"), ("pendolo (A)", "campo_g1_tre/g1_tre_A.npz"), ("pendolo (B)", "campo_g1_tre/g1_tre_B.npz"),
        ("pendolo (C)", "campo_g1_tre/g1_tre_C.npz"))


def main():
    import _presidio
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    _presidio.avvia(__file__)
    L = 81
    bor = CA.serie("TBS")[0][-1]["bordo"]
    c0 = bor["c0"]
    R_A, R_B = float(bor["R_A"]), TO.meta_periodo(L)
    v = np.arange(L * L)
    m1, m2 = v // L, v % L
    r_c0 = np.hypot(*TO.scarti(m1, m2, c0[0], c0[1], L).T[:2])
    print("=" * 130)
    print("IL BORDO E LA CODA DEL SOLITONE SU L 81 (Luca 15:49, solo lettura): il bordo di TBS, il centro %s, R_A %g, R_B %g, g_max %g" % (c0, R_A, R_B, bor["g_max"]))
    print("=" * 130)
    print("    %-16s %8s %8s %8s %8s %10s %10s %12s" % ("la corsa", "t", "d", "R99", "R999", "d + R99", "d + R999", "M oltre R_A"))
    for nome, f in FILE:
        p = os.path.join(REF, f)
        if not os.path.exists(p):
            print("    %-16s manca %s" % (nome, f))
            continue
        with np.load(p) as dd:
            t = dd["t_rho"] if "t_rho" in dd.files else dd["t"]
            rho = dd["rho"]
            idx = sorted(set([0, len(t) // 4, len(t) // 2, 3 * len(t) // 4, len(t) - 1]))
            peggio = None
            for i in range(len(t)):
                r = np.asarray(rho[i], dtype=float).ravel()
                cc = TO.centro(r, m1, m2, L)[:2]
                d = float(np.hypot(*TO.scarti(np.array([cc[0]]), np.array([cc[1]]), c0[0], c0[1], L)[0][:2]))
                rs = np.hypot(*TO.scarti(m1, m2, cc[0], cc[1], L).T[:2])
                o = np.argsort(rs)
                cum = np.cumsum(r[o]) / r.sum()
                R99, R999 = float(rs[o][np.searchsorted(cum, 0.99)]), float(rs[o][np.searchsorted(cum, 0.999)])
                fuori = float(r[r_c0 > R_A].sum() / r.sum())
                if peggio is None or d + R999 > peggio[1]:
                    peggio = (float(t[i]), d + R999, fuori)
                if i in idx:
                    print("    %-16s %8.0f %8.3f %8.3f %8.3f %10.3f %10.3f %12.3e" % (nome, float(t[i]), d, R99, R999, d + R99, d + R999, fuori))
            print("    %-16s il peggiore: t %.0f, d + R999 %.3f (R_A %g: %s), la massa oltre R_A %.3e" % ("", peggio[0], peggio[1], R_A, "DENTRO la rampa" if peggio[1] > R_A else "fuori dalla rampa", peggio[2]))
    # ---------------------------------------------------------------- Luca 17:02 (2): le scene di L 162
    print("-" * 130)
    for corsa in ("C35-pi", "S162"):
        b = CA.serie(corsa)[0][-1]["bordo"]
        print("### la scena di %s (L 162): il centro del bordo %s, R_A VERO %g, R_B %g (la meta' del periodo), g_max %g" % (corsa, b["c0"], float(b["R_A"]), TO.meta_periodo(162), b["g_max"]))
    b = CA.serie("C35-pi")[0][-1]["bordo"]
    L2 = 162
    v2 = np.arange(L2 * L2)
    r2 = np.hypot(*TO.scarti(v2 // L2, v2 % L2, b["c0"][0], b["c0"][1], L2).T[:2])
    for nome in ("Grampa", "0_2000"):
        with np.load(os.path.join(REF, "p6_bracci", nome + ".npz")) as dd:
            tt, rho = dd["t"], dd["rho"]
            for k in (0, 1000, 2000):
                i = int(np.nonzero(tt == tt[0] + k)[0][0])
                r = np.asarray(rho[i], dtype=float).ravel()
                fuori = float(r[r2 > float(b["R_A"])].sum() / r.sum())
                rmax_fuori = float(r[r2 > float(b["R_A"])].max() / r.max())
                print("    (%-6s) k %4d: la massa dei due solitoni oltre R_A %g dal centro del bordo %.3e (relativa); rho massimo oltre R_A / rho massimo %.3e" % (nome, k, float(b["R_A"]), fuori, rmax_fuori))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
