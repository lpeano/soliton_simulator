# -*- coding: utf-8 -*-
r"""**[M1052-S] LA SPINTA PER REGIONE DAL MOMENTO DI `rho`** *(il mandato di Luca [M1052], fase 1; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `4.5`: la ripartizione da `J` di `caduta_libera_misure_v2` ha `P/M` col segno opposto alla velocita' del baricentro, e72044df; SOLA LETTURA dei film)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_regioni_momento.py > doc/referti_l2/caduta_regioni_momento.txt

**Per variante e per stato:** `m_R(k) = somma_{v in R} rho_v y_v` negli anelli dal baricentro DELLO STATO *(nucleo `< 15`, guscio `15-21`, bordo `21-25`, fuori `>= 25`)* e, accanto, negli anelli FISSI di `k 0`; il fit `m0 + v k + a_R k^2/2`; al netto di V0; la quota del guscio e del bordo; il bivio di Luca.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402,F401  (i percorsi)
import caduta_libera as CL  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402

ORDINE = ("V0", "V1", "V2", "V3", "V4", "V1m")
REGIONI = ((0.0, 15.0, "nucleo"), (15.0, 21.0, "guscio"), (21.0, 25.0, "bordo"), (25.0, float("inf"), "fuori"))      # ### Luca 10:40
FILM = os.path.join(_QUI, "film")


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "caduta_libera_misure_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1052-S] LA SPINTA PER REGIONE DAL MOMENTO DI rho (la carta sez. 4.5): m_R = somma rho y; il fit; al netto di V0")
    print("=" * 130)
    A = {}
    for V in ORDINE:
        f = os.path.join(FILM, "caduta_%s.npz" % V)
        F = np.load(f)
        ks = [int(k) for k in F["k"]]
        L = int(F["L"])
        m1, m2 = F["m1"].astype(float), F["m2"].astype(float)
        X0, meta0 = GM.leggi(os.path.join(CL.BASE, V, "stato_000000.npz"))
        c = meta0["centro"]
        dxy = TO.scarti(m1, m2, c[0], c[1], L)[:, :2]
        y = dxy[:, 1]
        mom = {"stato": [], "fisse": []}
        Ms, yb = [], []
        r0 = None
        for k in ks:
            rho = F["rho_%06d" % k].astype(float)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            r = np.hypot(*(dxy - b).T)
            if r0 is None:
                r0 = r
            mom["stato"].append([float((rho * y)[(r >= a) & (r < bb)].sum()) for a, bb, _n in REGIONI])
            mom["fisse"].append([float((rho * y)[(r0 >= a) & (r0 < bb)].sum()) for a, bb, _n in REGIONI])
            Ms.append(float(rho.sum()))
            yb.append(float(b[1]))
        fy = GM.fit(ks, np.array(yb))
        A[V] = {}
        for q in ("stato", "fisse"):
            m = np.array(mom[q])
            A[V][q] = [GM.fit(ks, m[:, j]) for j in range(4)]
        print("  %s (il film sha1 %s): la massa da %.6e a %.6e; a del baricentro %+.4e; M a_bari %+.4e; somma a_R (anelli dello stato) %+.4e, (fissi) %+.4e" % (
            V, GM.sha1(f)[:8], Ms[0], Ms[-1], fy[2], Ms[0] * fy[2], sum(x[2] for x in A[V]["stato"]), sum(x[2] for x in A[V]["fisse"])))
        for q in ("stato", "fisse"):
            print("      gli anelli %-6s: %s" % (q, "; ".join("%s a %+.4e +- %.1e" % (n_[2], x[2], x[3]) for n_, x in zip(REGIONI, A[V][q]))))
    print("=" * 130)
    print("AL NETTO DI V0 (l'errore in quadratura); la quota (|a_guscio| + |a_bordo|) / somma |a_R|; il bivio di Luca: INTERFACCIA se la quota > 0.5")
    print("=" * 130)
    for V in ORDINE[1:]:
        for q in ("stato", "fisse"):
            net = [(x[2] - y_[2], float(np.hypot(x[3], y_[3]))) for x, y_ in zip(A[V][q], A["V0"][q])]
            quota = (abs(net[1][0]) + abs(net[2][0])) / sum(abs(x[0]) for x in net)
            print("  %-3s anelli %-6s: %s; la quota %.4f%s" % (V, q, "; ".join("%s %+.4e +- %.1e" % (n_[2], x[0], x[1]) for n_, x in zip(REGIONI, net)), quota,
                                                         ("  -> IL BIVIO: %s" % ("INTERFACCIA" if quota > 0.5 else "VOLUME")) if V == "V1" else ""))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
