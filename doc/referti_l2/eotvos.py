# -*- coding: utf-8 -*-
r"""**[M1446-Q] EÖTVÖS: DUE SOLITONI DI NORMA DIVERSA CADONO UGUALE?** *(il mandato di Luca [M1446], corsia Q; la carta `doc/CARTA_E_mc2.md`, sez. `Q`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/eotvos.py tenuta --scala 0.8          (N = 1, 1000 tick, la fase a ogni tick)
    E:\python\py3132\python.exe doc/referti_l2/eotvos.py orologio --scala 0.8 --var Nm   (la forma V2: cs = s N, la fase (a) spenta; Nm 0.9965, Np 1.0035; 1000 tick)
    E:\python\py3132\python.exe doc/referti_l2/eotvos.py calcio --scala 0.8          (massa_calcio: k 0.010 lungo A1, 1000 tick)
    E:\python\py3132\python.exe doc/referti_l2/eotvos.py caduta --scala 0.8          (la caduta in V2: la scena e il gradiente di [M0908], 2000 tick)
    E:\python\py3132\python.exe doc/referti_l2/eotvos.py lettura > doc/referti_l2/eotvos.txt

**Il solitone:** `caduta_libera.prepara`, poi `psi_h x sqrt(scala)` *(la norma x scala, la stessa forma)*, poi `porto.campi` *(`massa_calcio.scena_calciata`)*. **La lettura:** la tenuta *(il picco di `rho` a `k 1000` entro il `20%` di `k 0`; il residuo del fit della fase sotto `1` rad)*, `omega`, `d omega/dN` *(V2)*, `m*` *(il calcio)*, `a` *(la caduta, il baricentro lungo `y`)*; `eta = 2 (a_1 - a_2)/(a_1 + a_2)`; **la previsione** `a_i = -(d omega_i/dN) g_N / |m*_i|` *(il pacchetto `a = -grad omega/m*` con `m* < 0`; `g_N = |dN/dy|` allo zero, `dN/dy = -g_N`)*.
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
import chi_parametri_v2 as CP2  # noqa: E402
import girandola_chi_v3 as GC  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402
import massa_calcio as MC  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1446", "eotvos")
SCALE = (0.8, 1.2)
VAR = {"N1": 1.0, "Nm": 0.9965, "Np": 1.0035}
K_FINO, K_DA_FIT, R_OROLOGIO = 1000, 100, 15.0
TENUTA = 0.20                   # ### la carta: il picco entro il 20% (mio)
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "massa_calcio.py", "triangolo_chi_v4.py", "girandola_chi_v3.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def d_out(scala, cosa):
    d = os.path.join(BASE, "x%.1f" % scala, cosa)
    os.makedirs(d, exist_ok=True)
    return d


def orologio(scala, var):
    """### la fase media pesata con rho entro r 15 a ogni tick; `var` N1 (la tenuta), Nm, Np (la forma V2)."""
    avvia()
    _G20, _ia, e0, MT = CL.parametri()
    Nv = VAR[var]
    dd = d_out(scala, "tenuta" if var == "N1" else "orologio_" + var)
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy = MC.scena_calciata(Z, 0.0, 1, scala)
        s = float(Z["s"])
        N = np.full(n, Nv)
        dentro = np.hypot(dxy[:, 0], dxy[:, 1]) < R_OROLOGIO
        pn = GC.fase_dei_nodi(Z["st"]["psi_h"], nodo)
        comp = int(np.argmax([np.sum(np.abs(pn[dentro, j]) ** 2) for j in (0, 1)]))
        print("### Eötvös x %g, %s: N %.4f, la forma V2 (cs = s N, la fase spenta); la componente %d; l'impronta %s" % (scala, var, Nv, comp, CL.impronta(Z, C)[:12]))

        def fase():
            r_ = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            p = GC.fase_dei_nodi(Z["st"]["psi_h"], nodo)[:, comp]
            return complex(np.sum(r_[dentro] * p[dentro])), float(r_.max()), float(r_.sum())
        F, picco, norma = [], [], []
        f0 = fase()
        F.append(f0[0]); picco.append(f0[1]); norma.append(f0[2])
        t1 = time.time()
        for k in range(1, K_FINO + 1):
            CS.tick_var(Z["z"], C.campo, s, e0, N, True, 0)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            fk = fase()
            F.append(fk[0]); picco.append(fk[1]); norma.append(fk[2])
            if k % 250 == 0:
                print("    k %d: il picco %.4e (%.0f s)" % (k, fk[1], time.time() - t1))
                sys.stdout.flush()
        f = os.path.join(dd, "fase.npz")
        np.savez(f, F=np.array(F), picco=np.array(picco), norma=np.array(norma))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    return 0


def calcio(scala):
    return MC.corsa(0.010, 1, scala, base=os.path.join(BASE, "x%.1f" % scala), etichetta="calcio")


def caduta(scala):
    """### `caduta_libera.corsa` riga per riga con la variante V2 e il solitone riscalato."""
    avvia()
    G20, _ia, e0, MT = CL.parametri()
    dd = d_out(scala, "caduta_V2")
    with TC.scena() as Z:
        mot, L = Z["mot"], Z["L"]
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        C, info, _dxy = MC.scena_calciata(Z, 0.0, 1, scala)
        s = float(Z["s"])
        chi, N = CL.campo_N(Z, info, A, 1.0)
        meta = dict(info, variante="V2", scala=scala, cs_N=True, segno_fase=0, segno_chi=1.0, acceso=True, A=A, G20=G20, L_y=Ly, kappa=CP2.KAPPA, s=s, e0=e0)
        print("### la caduta in V2, x %g: A %.6e; l'impronta %s" % (scala, A, CL.impronta(Z, C)[:12]))

        def salva(k):
            fz = os.path.join(dd, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, chi=chi, N=N)
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(CL.sha1(fz) + "\n")
        salva(0)
        t1 = time.time()
        for k in range(1, 2001):
            CS.tick_var(Z["z"], C.campo, s, e0, N, True, 0)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % 250 == 0:
                salva(k)
                print("    [stato] k %d (%.0f s)" % (k, time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    return 0


def omega_di(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f)
    z = np.load(f)
    ph = np.unwrap(np.angle(z["F"]))
    k = np.arange(len(ph), dtype=float)
    m = k >= K_DA_FIT
    A = np.stack([np.ones(m.sum()), k[m]], axis=1)
    b, *_ = np.linalg.lstsq(A, ph[m], rcond=None)
    r = ph[m] - A @ b
    s2 = float(r @ r) / (m.sum() - 2)
    return -float(b[1]), math.sqrt(s2 * np.linalg.inv(A.T @ A)[1, 1]), math.sqrt(s2), z["picco"], z["norma"]


def lettura():
    avvia()
    from solitone import toro as TO
    print("=" * 130)
    print("[M1446-Q] EÖTVÖS (la carta sez. Q): le norme x %s; eta = 2 (a1 - a2)/(a1 + a2)" % (SCALE,))
    print("=" * 130)
    R = {}
    for sc in SCALE:
        b = os.path.join(BASE, "x%.1f" % sc)
        out = {}
        f = os.path.join(b, "tenuta", "fase.npz")
        if os.path.exists(f + ".sha1"):
            w, sw, rms, picco, norma = omega_di(f)
            regge = abs(picco[-1] / picco[0] - 1.0) <= TENUTA and rms < 1.0
            out["omega"] = (w, sw)
            print("  x %g la tenuta: omega %.10f +- %.1e (il residuo %.3e rad); il picco da %.4e a %.4e (%+.1f%%); la norma da %.6e a %.6e: %s" % (
                sc, w, sw, rms, picco[0], picco[-1], 100.0 * (picco[-1] / picco[0] - 1.0), norma[0], norma[-1], "REGGE" if regge else "### NON REGGE"))
            out["regge"] = regge
        om = {}
        for v in ("Nm", "Np"):
            f = os.path.join(b, "orologio_" + v, "fase.npz")
            if os.path.exists(f + ".sha1"):
                om[v] = omega_di(f)[:2]
        if len(om) == 2:
            out["dwdN"] = (om["Np"][0] - om["Nm"][0]) / (VAR["Np"] - VAR["Nm"])
            print("  x %g la forma V2: omega(Nm) %.10f, omega(Np) %.10f; d omega/dN %+.8f; (q - 1)/(N - 1) %+.5f" % (sc, om["Nm"][0], om["Np"][0], out["dwdN"], out["dwdN"] / out["omega"][0] if "omega" in out else float("nan")))
        f = os.path.join(b, "calcio", "serie.json")
        if os.path.exists(f + ".sha1"):
            v, sv, _r = MC.velocita(json.load(open(f, encoding="utf-8"))["serie"])
            out["mstar"] = (0.010 / v, abs(0.010 / v) * sv / abs(v))
            print("  x %g il calcio k 0.010 lungo A1: v %+.6e +- %.1e; m* %+.3f +- %.3f" % (sc, v, sv, out["mstar"][0], out["mstar"][1]))
        d = os.path.join(b, "caduta_V2")
        fs = [os.path.join(d, "stato_%06d.npz" % k) for k in range(0, 2001, 250)]
        if all(os.path.exists(x + ".sha1") for x in fs):
            yb, gN = [], None
            for x in fs:
                X, meta = GM.leggi(x)
                if gN is None:
                    c = meta["centro"]
                    with TC.scena() as Z:
                        dxy = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"])[:, :2]
                        nodo = np.asarray(Z["mot"].inc.nodo)
                        n = Z["n"]
                        Z["metti"]()
                    gN = float(meta["kappa"]) * float(meta["A"]) * 2.0 * math.pi / float(meta["L_y"])
                rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
                yb.append(float(((dxy * rho[:, None]).sum(axis=0) / rho.sum())[1]))
            fy = GM.fit(list(range(0, 2001, 250)), np.array(yb))
            out["a"], out["gN"] = (fy[2], fy[3]), gN
            print("  x %g la caduta in V2: a lungo y %+.4e +- %.1e (il residuo %.2e); g_N %.6e" % (sc, fy[2], fy[3], fy[4], gN))
        R[sc] = out
    print("-" * 130)
    if all("a" in R.get(sc, {}) for sc in SCALE):
        a1, a2 = R[SCALE[0]]["a"], R[SCALE[1]]["a"]
        eta = 2.0 * (a1[0] - a2[0]) / (a1[0] + a2[0])
        se = abs(eta) * math.hypot(math.hypot(a1[1], a2[1]) / abs(a1[0] - a2[0]), math.hypot(a1[1], a2[1]) / abs(a1[0] + a2[0]))
        print("  ETA = %+.4e +- %.1e (%.1f sigma); K5: %s" % (eta, se, abs(eta) / se, "VIOLA" if (abs(eta) > 3 * se and abs(eta) > 0.01) else "non viola"))
        pr = {}
        for sc in SCALE:
            o = R[sc]
            if "dwdN" in o and "mstar" in o:
                pr[sc] = -o["dwdN"] * o["gN"] / abs(o["mstar"][0])
                print("  x %g la previsione a = -(d omega/dN) g_N/|m*| = %+.4e (la misura %+.4e: il rapporto %.3f)" % (sc, pr[sc], o["a"][0], o["a"][0] / pr[sc]))
        if len(pr) == 2:
            ep = 2.0 * (pr[SCALE[0]] - pr[SCALE[1]]) / (pr[SCALE[0]] + pr[SCALE[1]])
            print("  eta prevista %+.4e; eta misurata contro prevista: %+.4e (%.1f sigma)" % (ep, eta - ep, abs(eta - ep) / se))
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("tenuta", "calcio", "caduta"):
        p = sub.add_parser(c)
        p.add_argument("--scala", type=float, required=True)
    p = sub.add_parser("orologio")
    p.add_argument("--scala", type=float, required=True)
    p.add_argument("--var", choices=("Nm", "Np"), required=True)
    sub.add_parser("lettura")
    x = ap.parse_args(argv)
    if x.cmd == "tenuta":
        return orologio(x.scala, "N1")
    if x.cmd == "orologio":
        return orologio(x.scala, x.var)
    if x.cmd == "calcio":
        return calcio(x.scala)
    if x.cmd == "caduta":
        return caduta(x.scala)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
