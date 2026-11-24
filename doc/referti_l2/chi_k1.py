# -*- coding: utf-8 -*-
r"""**K1 DEL TICK CON CHI: QUANTO SI SPOSTANO CHI E PI NEL VUOTO, E LA SORGENTE IN ULP** *(la nota di Luca `2026-11-21` `17:20`; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `10`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_k1.py > doc/referti_l2/chi_k1.txt

**La scena di K1** *(come `chi_prove.py`)*: il vuoto `vuoto_fresco`, `c0` del vuoto, `kappa` di C2; `20` tick di `chi_tick.tick_chi`. **A ogni tick, PRIMA del passo:** la sorgente `sigma = kappa N (s Q - e0 rho) - c0` per nodo: il massimo, i nodi non zero, in ulp di `|c0|`; `u` per nodo: i valori distinti, `m0 - u` in ulp di `|u|`. **DOPO:** `max |chi|`, `max |pi|`, `N == 1` esatto.
**La lettura** *(sez. `10.2`)*: lo SFONDO *(`u` uniforme, `m0` diverso)* o il VUOTO NON UNIFORME *(`u` con piu' valori)*; oltre `1e-12`: FERMO.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    MT, CV, PO = PS.MT, PS.CV, PS.PO
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    print("=" * 150)
    print("K1 DEL TICK CON CHI: LO SPOSTAMENTO NEL VUOTO E LA SORGENTE IN ULP (Luca 2026-11-21 17:20; il task history del ramo lapse-u, sez. 10)")
    print("=" * 150)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        s = float(Z["s"])
        Lp = CT.Laplaciano(mot)
        C = PO.campi(Z, rho_c, e)
        e0 = float(C.e0)
        Pv, m0v, _a, _c = CT.parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, "vuoto")
        MT.vuoto_fresco(Z, t0)
        C = PO.campi(Z, rho_c, e)
        u0 = CT.u_di(mot, Z["st"], Z["par"], s, e0)
        print("### il vuoto a t = 0: u ha %d valori distinti (%+.17e); m0 = la media %+.17e; m0 - u in ulp di |u|: %s; c0 = kappa m0 %+.17e; kappa u %+.17e" % (
            len(np.unique(u0)), u0[0], m0v, np.unique((m0v - u0) / np.spacing(np.abs(u0))), Pv.c0, Pv.kappa * u0[0]))
        X = CT.nuovo_X(n, m)
        ulp = float(np.spacing(abs(Pv.c0)))
        print("    l'ulp di |c0| %.3e" % ulp)
        print("    tick   sigma: max|.|     nodi != 0   max in ulp di c0   u: valori distinti   max |m0 - u| in ulp di u   ->   max|chi|      max|pi|     N == 1 esatto")
        grande = False
        for t in range(1, 21):
            N = np.exp(-Pv.kappa * X["chi"])
            Q = CT.Q_di(mot, Z["st"], Z["par"], Pv.s * N)
            rho = CT.rho_di(mot, Z["st"])
            sig = Pv.kappa * N * (Pv.s * Q - Pv.e0 * rho) - Pv.c0
            u = CT.u_di(mot, Z["st"], Z["par"], s, e0)
            du = np.abs(m0v - u) / np.spacing(np.abs(u))
            CT.tick_chi(Z["z"], C.campo, Pv, Lp, X)
            mc, mp = float(np.max(np.abs(X["chi"]))), float(np.max(np.abs(X["pi"])))
            uno = bool(np.all(np.exp(-Pv.kappa * X["chi"]) == 1.0))
            grande |= mc > 1e-12 or mp > 1e-12
            print("    %3d    %.3e      %6d         %10.1f        %6d               %10.1f             %.3e    %.3e    %s" % (
                t, float(np.max(np.abs(sig))), int(np.sum(sig != 0.0)), float(np.max(np.abs(sig))) / ulp, len(np.unique(u)), float(du.max()), mc, mp, uno))
        Z["metti"]()
    print("=" * 150)
    print("### LO SPOSTAMENTO: %s" % ("OLTRE 1e-12: un difetto vero, FERMO" if grande else "sotto 1e-12"))
    print("=" * 150)
    return 0


if __name__ == "__main__":
    sys.exit(main())
