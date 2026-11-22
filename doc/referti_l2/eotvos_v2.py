# -*- coding: utf-8 -*-
r"""**[M1446-Q] EÖTVÖS -- LA V2: LA FORMA V2 E LA FORMA V3** *(la versione nuova del mandato di Luca [M1446]; la carta `doc/CARTA_E_mc2.md`, sez. `1`: le righe di `eotvos.py` -- in uso dalla tenuta, non si tocca -- con la forma come argomento; la tenuta e il calcio restano quelli di `eotvos.py`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/eotvos_v2.py orologio --scala 0.8 --forma V3 --var Nm      (Nm 0.9965, Np 1.0035; 1000 tick)
    E:\python\py3132\python.exe doc/referti_l2/eotvos_v2.py caduta --scala 0.8 --forma V3                (la scena e il gradiente di [M0908], 2000 tick)
    E:\python\py3132\python.exe doc/referti_l2/eotvos_v2.py lettura > doc/referti_l2/eotvos.txt

**Le forme:** V2 *(`cs = s N`, la fase (a) spenta)*, V3 *(`cs = s`, la fase (a) `+`)*. **La lettura:** per forma, `omega(Nm)`, `omega(Np)`, `d omega/dN`, la caduta `a` lungo `y`; `eta = 2 (a_1 - a_2)/(a_1 + a_2)`; la previsione `a_i = -(d omega_i/dN) g_N/|m*_i|` con `m*_i` dal calcio di `eotvos.py`.
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
import eotvos as EV  # noqa: E402

FORME = {"V2": (True, 0), "V3": (False, +1)}          # ### (cs = s N, il segno della fase (a))


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "massa_calcio.py", "triangolo_chi_v4.py", "girandola_chi_v3.py", "eotvos.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def orologio(scala, forma, var):
    avvia()
    _G20, _ia, e0, MT = CL.parametri()
    cs_N, segno = FORME[forma]
    Nv = EV.VAR[var]
    dd = EV.d_out(scala, "orologio_%s_%s" % (forma, var))
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy = MC.scena_calciata(Z, 0.0, 1, scala)
        s = float(Z["s"])
        N = np.full(n, Nv)
        dentro = np.hypot(dxy[:, 0], dxy[:, 1]) < EV.R_OROLOGIO
        pn = GC.fase_dei_nodi(Z["st"]["psi_h"], nodo)
        comp = int(np.argmax([np.sum(np.abs(pn[dentro, j]) ** 2) for j in (0, 1)]))
        print("### Eötvös x %g, %s, %s: N %.4f; la componente %d; l'impronta %s" % (scala, forma, var, Nv, comp, CL.impronta(Z, C)[:12]))

        def fase():
            r_ = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            p = GC.fase_dei_nodi(Z["st"]["psi_h"], nodo)[:, comp]
            return complex(np.sum(r_[dentro] * p[dentro])), float(r_.max()), float(r_.sum())
        F, picco, norma = [], [], []
        x = fase()
        F.append(x[0]); picco.append(x[1]); norma.append(x[2])
        t1 = time.time()
        for k in range(1, EV.K_FINO + 1):
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            x = fase()
            F.append(x[0]); picco.append(x[1]); norma.append(x[2])
            if k % 250 == 0:
                print("    k %d (%.0f s)" % (k, time.time() - t1))
                sys.stdout.flush()
        f = os.path.join(dd, "fase.npz")
        np.savez(f, F=np.array(F), picco=np.array(picco), norma=np.array(norma))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    return 0


def caduta(scala, forma):
    avvia()
    G20, _ia, e0, MT = CL.parametri()
    cs_N, segno = FORME[forma]
    dd = EV.d_out(scala, "caduta_" + forma)
    with TC.scena() as Z:
        L = Z["L"]
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        C, info, _dxy = MC.scena_calciata(Z, 0.0, 1, scala)
        s = float(Z["s"])
        chi, N = CL.campo_N(Z, info, A, 1.0)
        meta = dict(info, variante=forma, scala=scala, cs_N=cs_N, segno_fase=segno, segno_chi=1.0, acceso=True, A=A, G20=G20, L_y=Ly, kappa=CP2.KAPPA, s=s, e0=e0)
        print("### la caduta in %s, x %g: A %.6e; l'impronta %s" % (forma, scala, A, CL.impronta(Z, C)[:12]))

        def salva(k):
            fz = os.path.join(dd, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, chi=chi, N=N)
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(CL.sha1(fz) + "\n")
        salva(0)
        t1 = time.time()
        for k in range(1, 2001):
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % 250 == 0:
                salva(k)
                print("    [stato] k %d (%.0f s)" % (k, time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    return 0


def a_caduta(d):
    from solitone import toro as TO
    fs = [os.path.join(d, "stato_%06d.npz" % k) for k in range(0, 2001, 250)]
    if not all(os.path.exists(x + ".sha1") for x in fs):
        return None
    yb, gN = [], None
    for x in fs:
        X, meta = GM.leggi(x)
        if gN is None:
            c = meta["centro"]
            with TC.scena() as Z:
                dxy = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"])[:, :2]
                nodo, n = np.asarray(Z["mot"].inc.nodo), Z["n"]
                Z["metti"]()
            gN = float(meta["kappa"]) * float(meta["A"]) * 2.0 * math.pi / float(meta["L_y"])
        rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
        yb.append(float(((dxy * rho[:, None]).sum(axis=0) / rho.sum())[1]))
    fy = GM.fit(list(range(0, 2001, 250)), np.array(yb))
    return fy, gN


def lettura():
    avvia()
    print("=" * 130)
    print("[M1446-Q] EÖTVÖS, LA V2 (la carta sez. 1): le norme x %s; le forme V2 e V3; eta = 2 (a1 - a2)/(a1 + a2)" % (EV.SCALE,))
    print("=" * 130)
    R = {}
    for sc in EV.SCALE:
        b = os.path.join(EV.BASE, "x%.1f" % sc)
        o = {}
        f = os.path.join(b, "tenuta", "fase.npz")
        if os.path.exists(f + ".sha1"):
            w, sw, rms, picco, norma = EV.omega_di(f)
            o["omega"] = w
            o["regge"] = abs(picco[-1] / picco[0] - 1.0) <= EV.TENUTA and rms < 1.0
            print("  x %g la tenuta: omega %.10f +- %.1e (il residuo %.3e); il picco da %.4e a %.4e (%+.1f%%); %s" % (sc, w, sw, rms, picco[0], picco[-1], 100 * (picco[-1] / picco[0] - 1.0), "REGGE" if o["regge"] else "### NON REGGE"))
        f = os.path.join(b, "calcio", "serie.json")
        if os.path.exists(f + ".sha1"):
            v, sv, _r = MC.velocita(json.load(open(f, encoding="utf-8"))["serie"])
            o["mstar"] = 0.010 / v
            print("  x %g il calcio: v %+.6e +- %.1e; m* %+.3f" % (sc, v, sv, o["mstar"]))
        for forma in FORME:
            om = {}
            for var in ("Nm", "Np"):
                f = os.path.join(b, "orologio_%s_%s" % (forma, var), "fase.npz")
                if os.path.exists(f + ".sha1"):
                    om[var] = EV.omega_di(f)[0]
            if len(om) == 2:
                o["dwdN_" + forma] = (om["Np"] - om["Nm"]) / (EV.VAR["Np"] - EV.VAR["Nm"])
                print("  x %g %s: omega(Nm) %.10f, omega(Np) %.10f; d omega/dN %+.8f; (q - 1)/(N - 1) %+.5f" % (sc, forma, om["Nm"], om["Np"], o["dwdN_" + forma], o["dwdN_" + forma] / o["omega"] if "omega" in o else float("nan")))
            ac = a_caduta(os.path.join(b, "caduta_" + forma))
            if ac:
                o["a_" + forma], o["gN"] = (ac[0][2], ac[0][3]), ac[1]
                print("  x %g %s la caduta: a lungo y %+.4e +- %.1e (il residuo %.2e)" % (sc, forma, ac[0][2], ac[0][3], ac[0][4]))
        R[sc] = o
    print("-" * 130)
    for forma in FORME:
        k = "a_" + forma
        if all(k in R.get(sc, {}) for sc in EV.SCALE):
            a1, a2 = R[EV.SCALE[0]][k], R[EV.SCALE[1]][k]
            eta = 2.0 * (a1[0] - a2[0]) / (a1[0] + a2[0])
            se = 2.0 * math.hypot(a1[1], a2[1]) * math.hypot(1.0, (a1[0] - a2[0]) / (a1[0] + a2[0])) / abs(a1[0] + a2[0])
            print("  %s: ETA = %+.4e +- %.1e (%.1f sigma): K5 %s" % (forma, eta, se, abs(eta) / se, "VIOLA" if (abs(eta) > 3 * se and abs(eta) > 0.01) else "non viola"))
            pr = {}
            for sc in EV.SCALE:
                oo = R[sc]
                if ("dwdN_" + forma) in oo and "mstar" in oo:
                    pr[sc] = -oo["dwdN_" + forma] * oo["gN"] / abs(oo["mstar"])
                    print("    x %g la previsione -(d omega/dN) g_N/|m*| %+.4e; la misura %+.4e; il rapporto %.3f" % (sc, pr[sc], oo[k][0], oo[k][0] / pr[sc]))
            if len(pr) == 2:
                ep = 2.0 * (pr[EV.SCALE[0]] - pr[EV.SCALE[1]]) / (pr[EV.SCALE[0]] + pr[EV.SCALE[1]])
                print("    eta prevista %+.4e; la misurata meno la prevista %+.4e (%.1f sigma)" % (ep, eta - ep, abs(eta - ep) / se))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("orologio")
    p.add_argument("--scala", type=float, required=True)
    p.add_argument("--forma", choices=tuple(FORME), required=True)
    p.add_argument("--var", choices=("Nm", "Np"), required=True)
    p = sub.add_parser("caduta")
    p.add_argument("--scala", type=float, required=True)
    p.add_argument("--forma", choices=tuple(FORME), required=True)
    sub.add_parser("lettura")
    x = ap.parse_args(argv)
    if x.cmd == "orologio":
        return orologio(x.scala, x.forma, x.var)
    if x.cmd == "caduta":
        return caduta(x.scala, x.forma)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
