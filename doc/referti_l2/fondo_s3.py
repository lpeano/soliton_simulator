# -*- coding: utf-8 -*-
r"""**[M2305] S3: LA LEGGE `a = -grad omega / m*` SULL'OGGETTO AL FONDO A K** *(Luca, 2026-11-23 23:05; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-sexies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_s3.py caduta --scala 0.5        (scala 0.5, 2.0: l'ampiezza A di campo_N rispetto a 1c)
    E:\python\py3132\python.exe doc/referti_l2/fondo_s3.py lettura > doc/referti_l2/fondo_s3.txt

**La caduta V2** di `fondo_1c.caduta` riga per riga col gradiente `scala x A` *(le uscite `M1658/c1/caduta_V2_x<scala>`)*; **la lettura:** coi `x1` e V0 di 1c, `grad omega = (d omega/dN)(dN/dy)` *(`d omega/dN` dall'orologio V2 di 1c; `dN/dy = -kappa A 2 pi / L_y` al centro)*, `K_i = (a_i - a(V0)) / (-grad omega_i / m*)`, `m*` dal calcio di 1c.
"""
import argparse
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402

TC, CL, MC, TT, FS = F1.TC, F1.CL, F1.MC, F1.TT, F1.FS


def caduta(scala):
    F1.avvia()
    import _presidio
    _presidio.avvia(__file__)
    MV, P0 = TT.nucleo()
    G20, _ia, _e0, _MT = CL.parametri()
    import chi_parametri_v2 as CP2
    nome = "caduta_V2_x%.1f" % scala
    t1 = time.time()
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = FS.carica(Z, "K", 3000)
        Ly = L * math.sqrt(3.0) / 2.0
        A = float(scala) * G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        _chi, N = CL.campo_N(Z, info, A, +1.0)
        print("### %s: %s; y_c %.6f; A %.6e (x%.1f); N da %.10f a %.10f; l'impronta %s" % (nome, info["file"], info["y_c"], A, scala, float(N.min()), float(N.max()), TT.impronta(Z, C)[:12]))
        serie = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b[0]), float(b[1]), float(rho.sum())))

        def dopo(kk, prima):
            if kk % MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: y %+.5f (%.0f s)" % (kk, serie[-1][2], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        F1.ciclo(Z, C, F1.K_CADUTA, dopo, MV, P0, N, True, 0)
        F1.scrivi(nome, {"coll": "V2", "scala": scala, "serie": serie, "info": info, "G20": G20, "A": A})
        Z["metti"]()
    print("### %d tick in %.0f s" % (F1.K_CADUTA, time.time() - t1))
    return 0


def lettura():
    F1.avvia()
    import _presidio
    import chi_parametri_v2 as CP2
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2305] S3: LA LEGGE a = -grad omega / m* SULL'OGGETTO AL FONDO A K (la carta sez. 2-sexies)")
    print("=" * 130)
    r0, r1 = F1.leggi("calcio_%s" % MC.nome(0.0, 1)), F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    v0, _s0, _ = MC.velocita(r0["serie"])
    v1, _s1, _ = MC.velocita(r1["serie"])
    mstar = 0.010 / (v1 - v0)
    D = {}
    for Nv in (0.9965, 1.0035):
        x = F1.leggi("orologio_V2_N%.4f" % Nv)
        D[Nv] = float((np.array(x["omega"]) - np.array(x["omega_phi"])).mean())
    dw_dN = (D[1.0035] - D[0.9965]) / 0.007
    c0 = F1.leggi("caduta_V0")
    a0, sa0, _ = F1.fit_a(c0["serie"])
    print("  m* %+.4f (il calcio di 1c); d omega/dN %+.6f (l'orologio V2 di 1c); a(V0) %+.4e +- %.1e" % (mstar, dw_dN, a0, sa0))
    K = []
    for nome, sc in (("caduta_V2_x0.5", 0.5), ("caduta_V2", 1.0), ("caduta_V2_x2.0", 2.0)):
        c = F1.leggi(nome)
        if c is None:
            print("  %s: NON FINITA" % nome)
            continue
        a, sa, dn = F1.fit_a(c["serie"])
        L = 162
        Ly = L * math.sqrt(3.0) / 2.0
        dNdy = -CP2.KAPPA * float(c["A"]) * 2.0 * math.pi / Ly
        gw = dw_dN * dNdy
        pred = -gw / mstar
        k_ = (a - a0) / pred
        sk = abs(math.hypot(sa, sa0) / pred)
        K.append(k_)
        print("  x%.1f: A %.6e; dN/dy %+.4e; grad omega %+.4e; -grad omega/m* %+.4e; a - a(V0) %+.4e +- %.1e; K %+.4f +- %.4f; la norma %.1e" % (sc, float(c["A"]), dNdy, gw, pred, a - a0, math.hypot(sa, sa0), k_, sk, dn))
    if len(K) == 3:
        m, s = float(np.mean(K)), float(np.std(K, ddof=1))
        print("### K: la media %+.4f, lo scarto %.4f (%.2f%% della media); il criterio: lo scarto/la media < 10%% e |media - 1| < 0.15: %s" % (
            m, s, 100 * s / abs(m), "VALE" if (s / abs(m) < 0.10 and abs(m - 1) < 0.15) else "NON VALE"))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("caduta", "lettura"))
    ap.add_argument("--scala", type=float)
    a = ap.parse_args(argv)
    if a.cosa == "caduta":
        return caduta(a.scala)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
