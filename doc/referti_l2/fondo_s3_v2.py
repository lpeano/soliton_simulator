# -*- coding: utf-8 -*-
r"""**[M0118-00] S3 NELLE DUE CONVENZIONI** *(DECISIONE DI LUCA, 2026-11-24 01:25; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-sexies`, l'annotazione «la convenzione della cima»; `fondo_s3.py` e' usato e non si riscrive)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_s3_v2.py >> doc/referti_l2/fondo_s3.txt

**Le K di S3** (`x0.5`, `x1`, `x2`) **una accanto all'altra:** **VUOTO** *(la vecchia: `grad omega = (d Delta/dN) dN/dy`, `Delta = omega_psi - omega_phi(lontano)`, lo zero dal vuoto lontano, una scelta di CC)* e **CIMA** *(la sagoma, `legge_caduta_v2`: `grad omega = omega_psi(N1) dN/dy`, `omega_psi(N1)` dallo zero del tick = la media di `omega` dell'orologio V2 di 1c a `N = 1`)*. Sull'intera `[200, 2000]` *(= `fondo_1c.fit_a`)* e sulle finestre di `600`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402

FINESTRE = ((200, 2000), (200, 800), (800, 1400), (1400, 2000))
LY = 162 * math.sqrt(3.0) / 2.0


def pendenze():
    """### `(d Delta/dN, omega_psi(N1))` dall'orologio V2 di 1c *(`F1.BASE` deve essere quello di 1c)*."""
    D = {}
    for Nv in (0.9965, 1.0035):
        x = F1.leggi("orologio_V2_N%.4f" % Nv)
        D[Nv] = float((np.array(x["omega"]) - np.array(x["omega_phi"])).mean())
    x1 = F1.leggi("orologio_V2_N1.0000")
    return (D[1.0035] - D[0.9965]) / 0.007, float(np.mean(x1["omega"]))


def due_K(a, sa, A, mstar, dD, w1):
    """### `(K_vuoto, K_cima, s_vuoto, s_cima)` per un `a - a(V0)`."""
    import chi_parametri_v2 as CP2
    dNdy = -CP2.KAPPA * A * 2.0 * math.pi / LY
    pv, pc = -(dD * dNdy) / mstar, -(w1 * dNdy) / mstar
    return a / pv, a / pc, abs(sa / pv), abs(sa / pc)


def lettura():
    import _presidio
    import caduta_finestre as CF
    F1.avvia()
    for m in ("fondo_s3.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    MC = F1.MC
    print("=" * 130)
    print("[M0118-00] S3 NELLE DUE CONVENZIONI (la carta sez. 2-sexies, l'annotazione): VUOTO (d Delta/dN, una scelta di CC) e CIMA (omega_psi(N1), la sagoma)")
    print("=" * 130)
    r0, r1 = F1.leggi("calcio_%s" % MC.nome(0.0, 1)), F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    v0, _s0, _ = MC.velocita(r0["serie"])
    v1, _s1, _ = MC.velocita(r1["serie"])
    mstar = 0.010 / (v1 - v0)
    dD, w1 = pendenze()
    print("  m* %+.4f; d Delta/dN %+.6f (VUOTO); omega_psi(N1) %+.7f (CIMA, l'orologio V2 di 1c a N 1); il rapporto CIMA/VUOTO delle K = d Delta/dN / omega_psi(N1) = %.4f" % (mstar, dD, w1, dD / w1))
    c0 = F1.leggi("caduta_V0")
    Kc = {}
    for nome, sc in (("caduta_V2_x0.5", 0.5), ("caduta_V2", 1.0), ("caduta_V2_x2.0", 2.0)):
        c = F1.leggi(nome)
        print("  x%.1f (A %.6e):" % (sc, float(c["A"])))
        for w in FINESTRE:
            a, sa, _ = CF.fit(c["serie"], *w)
            a0, sa0, _ = CF.fit(c0["serie"], *w)
            kv, kc, sv, scc = due_K(a - a0, math.hypot(sa, sa0), float(c["A"]), mstar, dD, w1)
            if w == (200, 2000):
                Kc[sc] = (kv, kc)
            print("    [%4d, %4d]: a - a(V0) %+.4e +- %.1e;   K VUOTO %+.4f +- %.4f;   K CIMA %+.4f +- %.4f" % (w[0], w[1], a - a0, math.hypot(sa, sa0), kv, sv, kc, scc))
    for i, nome in ((0, "VUOTO"), (1, "CIMA")):
        v = [Kc[s][i] for s in (0.5, 1.0, 2.0)]
        m, s = float(np.mean(v)), float(np.std(v, ddof=1))
        print("### K %s su [200, 2000]: %s; la media %+.4f, lo scarto %.4f (%.2f%% della media)" % (nome, ", ".join("%+.4f" % x for x in v), m, s, 100 * s / abs(m)))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(lettura())
