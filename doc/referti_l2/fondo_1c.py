# -*- coding: utf-8 -*-
r"""**[M1658-U] 1c: L'OGGETTO AL FONDO A K MISURATO COME F0: IL CALCIO, L'OROLOGIO, LA CADUTA** *(Luca, 2026-11-23, [M1658]; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-quater`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_1c.py calcio --k 0.010
    E:\python\py3132\python.exe doc/referti_l2/fondo_1c.py orologio --coll V2 --N 0.9965        (coll V2, V3; N 0.9965, 1.0, 1.0035)
    E:\python\py3132\python.exe doc/referti_l2/fondo_1c.py caduta --coll V3                       (coll V0, V2, V3)
    E:\python\py3132\python.exe doc/referti_l2/fondo_1c.py lettura > doc/referti_l2/fondo_1c.txt

**L'oggetto:** `M1658/tenuta/L-1_proiezione_K/stato_003000.npz`, la forma `L-1`; **`fondo_suite_v2.carica`** con `stato_di` e `FORMA` di quel modulo puntati qui IN MEMORIA. **Il ciclo:** `fondo_suite_v2._tick_loop` riga per riga col `segno` passato. Le uscite in `E:/soliton_simulator/controllo/M1658/c1/<nome>/serie.json` *(con lo sha1)*.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import massa_calcio as MC  # noqa: E402
import torneo_tenuta as TT  # noqa: E402
import fondo_suite_v2 as FS  # noqa: E402

OGGETTO = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658", "tenuta", "L-1_proiezione_K", "stato_003000.npz")
BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658", "c1")
FORMA_OGG = "L-1"
K_OROLOGIO, K_CADUTA, K_FIT = 500, 2000, 200
R_LONTANO = 60.0
COME_N = (0.98, 1.02)        # ### «l'orologio come N»: Luca [M2145] 21:45 (era [0.9, 1.1], mia): la differenza V2/V3 e' il 2%
COLL = {"V0": (False, 0), "V2": (True, 0), "V3": (False, 1)}


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "massa_calcio.py", "torneo_tenuta.py", "fondo_suite_v2.py", "ripresa_F0_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    FS.FORMA["K"] = FORMA_OGG
    FS.stato_di = lambda sorgente, kstato: OGGETTO


def ciclo(Z, C, quanti, dopo, MV, P0, N, cs_N, segno):
    """### `fondo_suite_v2._tick_loop` riga per riga, col `segno` passato."""
    import ripresa_F0_v2 as RF
    _G20, _ia, e0, MT = CL.parametri()
    s = float(Z["s"])
    with RF.col_nucleo(MV, P0), MV.forma_esplicita(FORMA_OGG):
        assert MV.ATTIVA == FORMA_OGG and MV.pezzi is P0
        for kk in range(1, quanti + 1):
            prima = Z["st"]["psi_h"].copy()
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            dopo(kk, prima)


def scrivi(nome, dati):
    d = os.path.join(BASE, nome)
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "serie.json")
    open(f, "w", encoding="utf-8").write(json.dumps(dati))
    open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
    return f


def calcio(k):
    avvia()
    MV, P0 = TT.nucleo()
    nome = "calcio_%s" % MC.nome(k, 1)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = FS.carica(Z, "K", 3000)
        assert forma == FORMA_OGG
        u = MC.asse_u(1)
        if k:
            Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * np.exp(1j * float(k) * (dxy @ u))[nodo][:, None]
        print("### %s: %s, la forma %s; il centro %s; l'impronta %s" % (nome, info["file"], forma, info["centro"], TT.impronta(Z, C)[:12]))
        serie, om = [], []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b @ u), float(b[0]), float(b[1]), float(rho.sum()), float(rho.max())))

        def dopo(kk, prima):
            om.append(float(-np.angle(np.vdot(prima, Z["st"]["psi_h"]))))
            if kk % MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: lungo l'asse %+.5f, omega %+.6f (%.0f s)" % (kk, serie[-1][1], om[-1], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        ciclo(Z, C, MC.K_FINO, dopo, MV, P0, np.ones(n), False, 0)
        scrivi(nome, {"k": k, "serie": serie, "omega": om, "info": info})
        Z["metti"]()
    print("### %d tick in %.0f s" % (MC.K_FINO, time.time() - t1))
    return 0


def orologio(coll, Nval):
    avvia()
    MV, P0 = TT.nucleo()
    cs_N, segno = COLL[coll]
    nome = "orologio_%s_N%.4f" % (coll, Nval)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = FS.carica(Z, "K", 3000)
        r = np.hypot(dxy[:, 0], dxy[:, 1])
        ii, jj = nodo[0::2], nodo[1::2]
        lont = np.repeat((r[ii] > R_LONTANO) & (r[jj] > R_LONTANO), 2)
        print("### %s: %s; %d mezzi archi del vuoto lontano (r > %g); l'impronta %s" % (nome, info["file"], int(lont.sum()), R_LONTANO, TT.impronta(Z, C)[:12]))
        om, omf = [], []

        def dopo(kk, prima):
            om.append(float(-np.angle(np.vdot(prima, Z["st"]["psi_h"]))))
            ph = Z["st"]["phi_h"]
            omf.append(float(-np.angle(np.vdot(stato["phi"][lont], ph[lont]))))
            stato["phi"] = ph.copy()
            if kk % 250 == 0:
                print("    k %d: omega_psi %+.7f, omega_phi lontano %+.7f (%.0f s)" % (kk, om[-1], omf[-1], time.time() - t1))
                sys.stdout.flush()
        stato = {"phi": Z["st"]["phi_h"].copy()}
        ciclo(Z, C, K_OROLOGIO, dopo, MV, P0, np.full(n, float(Nval)), cs_N, segno)
        scrivi(nome, {"coll": coll, "N": Nval, "omega": om, "omega_phi": omf, "info": info})
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_OROLOGIO, time.time() - t1))
    return 0


def caduta(coll):
    avvia()
    MV, P0 = TT.nucleo()
    G20, _ia, _e0, _MT = CL.parametri()
    import chi_parametri_v2 as CP2
    cs_N, segno = COLL[coll]
    nome = "caduta_%s" % coll
    t1 = time.time()
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = FS.carica(Z, "K", 3000)
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        if coll == "V0":
            N = np.ones(n)
        else:
            _chi, N = CL.campo_N(Z, info, A, +1.0)
        print("### %s: %s; y_c %.6f; A %.6e; N da %.10f a %.10f; l'impronta %s" % (nome, info["file"], info["y_c"], A, float(N.min()), float(N.max()), TT.impronta(Z, C)[:12]))
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
        ciclo(Z, C, K_CADUTA, dopo, MV, P0, N, cs_N, segno)
        scrivi(nome, {"coll": coll, "serie": serie, "info": info, "G20": G20, "A": A})
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_CADUTA, time.time() - t1))
    return 0


def leggi(nome):
    f = os.path.join(BASE, nome, "serie.json")
    if not os.path.exists(f + ".sha1"):
        return None
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f)
    return json.load(open(f, encoding="utf-8"))


def fit_a(serie):
    s = np.array(serie)
    m = s[:, 0] >= K_FIT
    k, y = s[m, 0], s[m, 2]
    A = np.stack([np.ones_like(k), k, 0.5 * k * k], axis=1)
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - A @ c
    cov = float(np.sum(r ** 2) / (len(k) - 3)) * np.linalg.inv(A.T @ A)
    return float(c[2]), math.sqrt(cov[2, 2]), float(abs(s[-1, 3] / s[0, 3] - 1.0))


def lettura():
    avvia()
    print("=" * 130)
    print("[M1658-U] 1c: L'OGGETTO AL FONDO A K (L-1_proiezione_K, k 3000) MISURATO COME F0 (la carta sez. 2-quater)")
    print("=" * 130)
    r0, r1 = leggi("calcio_%s" % MC.nome(0.0, 1)), leggi("calcio_%s" % MC.nome(0.010, 1))
    if r0 and r1:
        v0, s0, _ = MC.velocita(r0["serie"])
        v1, s1, _ = MC.velocita(r1["serie"])
        sg = math.hypot(s0, s1)
        print("  IL CALCIO: v0 %+.4e +- %.1e, v(k 0.010) %+.4e +- %.1e; m* = 0.010/(v - v0) = %+.3f (|v - v0| %.1f sigma); omega (k 0) %+.7f" % (
            v0, s0, v1, s1, 0.010 / (v1 - v0), abs(v1 - v0) / sg, float(np.mean(r0["omega"]))))
        print("  K4: m* %s" % ("POSITIVA" if (v1 - v0) > 2 * sg else ("NEGATIVA" if (v1 - v0) < -2 * sg else "NON SI DECIDE (entro 2 sigma)")))
    else:
        print("  IL CALCIO: NON FINITO")
    Ds = {}
    for coll in ("V2", "V3"):
        R = {}
        for Nv in (0.9965, 1.0, 1.0035):
            x = leggi("orologio_%s_N%.4f" % ("V2" if Nv == 1.0 else coll, Nv))
            if x:
                o, f = np.array(x["omega"]), np.array(x["omega_phi"])
                R[Nv] = (float(o.mean()), float(f.mean()), float((o - f).mean()))
        if len(R) == 3:
            d1 = R[1.0][2]
            dl = (R[1.0035][2] - R[0.9965][2]) / (2 * 0.0035) / d1
            Ds[coll] = dl
            print("  L'OROLOGIO %s: Delta = omega_psi - omega_phi(lontano) a N 0.9965, 1, 1.0035: %+.7f, %+.7f, %+.7f; d ln Delta/dN %+.4f (%s)" % (
                coll, R[0.9965][2], R[1.0][2], R[1.0035][2], dl, "COME N" if COME_N[0] <= dl <= COME_N[1] else "non come N"))
        else:
            print("  L'OROLOGIO %s: NON FINITO" % coll)
    c0 = leggi("caduta_V0")
    for coll in ("V2", "V3"):
        c = leggi("caduta_%s" % coll)
        if c and c0:
            a, sa, dn = fit_a(c["serie"])
            a0, sa0, _ = fit_a(c0["serie"])
            da, sd = a - a0, math.hypot(sa, sa0)
            verso = da > 0
            nat = verso and coll in Ds and COME_N[0] <= Ds[coll] <= COME_N[1]
            print("  LA CADUTA %s: a %+.4e +- %.1e; V0 %+.4e +- %.1e; a - a(V0) %+.4e +- %.1e (%.1f sigma): %s; la norma %.1e%s" % (
                coll, a, sa, a0, sa0, da, sd, abs(da) / sd, "VERSO N piu' basso" if verso else "VIA", dn, "; ### NATURA" if nat else ""))
        else:
            print("  LA CADUTA %s: NON FINITA" % coll)
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("calcio", "orologio", "caduta", "lettura"))
    ap.add_argument("--k", type=float)
    ap.add_argument("--coll", choices=("V0", "V2", "V3"))
    ap.add_argument("--N", type=float)
    a = ap.parse_args(argv)
    if a.cosa == "calcio":
        return calcio(a.k)
    if a.cosa == "orologio":
        return orologio(a.coll, a.N)
    if a.cosa == "caduta":
        return caduta(a.coll)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
