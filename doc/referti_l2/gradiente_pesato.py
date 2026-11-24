# -*- coding: utf-8 -*-
r"""**[M1330-B0] IL GRADIENTE PESATO** *(DECISIONE DI LUCA, 2026-11-24 13:30; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-ter`; solo lettura)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/gradiente_pesato.py >> doc/referti_l2/k_forma.txt

**`<dN/dy> = somma rho dN/dy / somma rho`** sugli stati ogni `250` della caduta per parti *(1c V2 `x1`, `M1658/c1_parti/caduta_V2`)*, `dN/dy = -kappa N A (2 pi/L_y) cos(2 pi (y - y_c)/L_y)` *(da `caduta_libera.campo_N`)*, contro il centro di S3 `-kappa A 2 pi/L_y`; e K CIMA di 1c per finestra riletto col gradiente pesato.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import fondo_s3_v2 as S3V2  # noqa: E402

PARTI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658", "c1_parti", "caduta_V2")
FINESTRE = ((200, 800), (800, 1400), (1400, 2000))


def dNdy(y, y_c, A, Ly, kappa):
    ph = 2.0 * np.pi * (np.asarray(y, float) - y_c) / Ly
    N = np.exp(-kappa * A * np.sin(ph))
    return -kappa * N * A * (2.0 * np.pi / Ly) * np.cos(ph)


def main():
    import _presidio
    import gravita_due_corpi_misure as GM
    import caduta_finestre as CF
    import chi_parametri_v2 as CP2
    F1.avvia()
    for m in ("fondo_s3_v2.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("-" * 130)
    print("[M1330-B0] IL GRADIENTE PESATO (la carta sez. 3-ter): <dN/dy> = somma rho dN/dy / somma rho, contro il centro di S3")
    print("-" * 130)
    c = F1.leggi("caduta_V2")
    A, y_c = float(c["A"]), float(c["info"]["y_c"])
    with F1.TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        y = np.asarray(Z["m2"], float) * math.sqrt(3.0) / 2.0
        Z["metti"]()
    Ly = L * math.sqrt(3.0) / 2.0
    k_ = CP2.KAPPA
    centro = -k_ * A * 2.0 * math.pi / Ly
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    g0 = float(dNdy(y_c, y_c, A, Ly, k_))
    esito("il caso noto: dN/dy a y = y_c = il centro di S3 entro 1e-12 relativo", abs(g0 / centro - 1.0) <= 1e-12, "%+.6e contro %+.6e" % (g0, centro))
    g4 = float(dNdy(y_c + Ly / 4.0, y_c, A, Ly, k_))
    esito("DEVE FALLIRE: a y_c + L_y/4 NON ridà il centro", abs(g4 / centro - 1.0) > 1e-12, "%+.6e" % g4)
    G = dNdy(y, y_c, A, Ly, k_)
    print("  A %.6e, y_c %.6f, L_y %.6f; il centro dN/dy %+.6e" % (A, y_c, Ly, centro))
    R = {}
    for k in range(0, 2001, 250):
        f = os.path.join(PARTI, "stato_%06d.npz" % k)
        X, _m = GM.leggi(f)
        rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
        gp = float(np.sum(rho * G) / np.sum(rho))
        w = F1.TT.misura(f, nodo, n, L)[0]
        R[k] = gp
        print("  k %4d: w %.3f; <dN/dy> %+.6e; <dN/dy>/centro %.5f (%+.2f%%)" % (k, w, gp, gp / centro, 100.0 * (gp / centro - 1.0)))
    dD, w1 = S3V2.pendenze()
    MC = F1.MC
    r0, r1 = F1.leggi("calcio_%s" % MC.nome(0.0, 1)), F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    v0, _s0, _ = MC.velocita(r0["serie"])
    v1, _s1, _ = MC.velocita(r1["serie"])
    ms = 0.010 / (v1 - v0)
    c0 = F1.leggi("caduta_V0")
    print("  K CIMA di 1c per finestra, col centro e col gradiente pesato (la media di <dN/dy> sugli stati con k nella finestra):")
    for w in FINESTRE:
        a, sa, _ = CF.fit(c["serie"], *w)
        a0, sa0, _ = CF.fit(c0["serie"], *w)
        _kv, kc, _sv, scc = S3V2.due_K(a - a0, math.hypot(sa, sa0), A, ms, dD, w1)
        ks = [k for k in R if w[0] <= k <= w[1]]
        gm = float(np.mean([R[k] for k in ks]))
        print("    [%4d, %4d]: K CIMA (centro) %+.4f +- %.4f; gli stati %s, <dN/dy>/centro %.5f; K CIMA (pesato) %+.4f" % (w[0], w[1], kc, scc, ks, gm / centro, kc * centro / gm))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
