# -*- coding: utf-8 -*-
r"""**LE PROVE DEL TICK CON CHI (PARTE B: K1-K5, IL DETERMINISMO, LA RIPRESA, IL COSTO)** *(il mandato di Luca `2026-11-21` `15:57`; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `9.3`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_prove.py > doc/referti_l2/chi_prove.txt

**Le soglie** *(fissate nella sez. `9.3`)*: **K1** il vuoto *(`c0` del vuoto)*: `chi`, `pi` a `0` e lo stato = `tick_GU` con `("uno",)` AL BIT per `20` tick; **K2** `kappa = 0` dal mattone di C2 `k 3000`: = `tick_GU` con `("uno",)` AL BIT per `20` tick; **K3** la sorgente ferma: dal profilo statico `2000` passi entro `1e-10`; da `0` la media sui passi `2000-8000` al centro entro il `10%`; **K4** l'impulso: `chi = 0` esatto oltre `t` passi e non zero a `t`, `t = 1..30`; **K5** la deriva di `H` in `100` tick non oltre `10` volte quella del tick di oggi, piu' `1e-12`; **il determinismo** e **la ripresa** AL BIT; **B3 il costo:** oltre `+10%` FERMO.
"""
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT              # ### il modulo nuovo

DIR_PROVA = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "prova")
N_BIT = 20


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    import _u1_prototipo as U1
    from solitone import tick_lapse as TL
    MT, CV, PO, LC = PS.MT, PS.CV, PS.PO, PS.LC
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    t00 = time.time()
    esiti = {}
    print("=" * 150)
    print("LE PROVE DEL TICK CON CHI, LA PARTE B (Luca 2026-11-21 15:57; il task history del ramo lapse-u, sez. 9.3)")
    print("=" * 150)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        s = float(Z["s"])
        Lp = CT.Laplaciano(mot)

        def fotografa():
            return {k: Z["st"][k].copy() for k in Z["chiavi"]}

        def metti(S, A=None, E=None):
            Z["metti"]({k: v.copy() for k, v in S.items()})
            C = PO.campi(Z, rho_c, e, None if A is None else A.copy(), None if E is None else E.copy())
            return C

        def uguali(S1, A1, E1, S2, A2, E2):
            diverse = [k for k in S1 if not np.array_equal(S1[k], S2[k])]
            if not np.array_equal(A1, A2):
                diverse.append("A")
            if not np.array_equal(E1, E2):
                diverse.append("E")
            return diverse

        # ------------------------------------------------------------------ i parametri
        C = metti(fotografa())
        e0 = float(C.e0)
        P, m0, a, c0_c2 = CT.parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, "C2")
        print("### i parametri (CALCOLATI): %r; m0 %+.12e; a %.10e" % (P, m0, a))
        print("    il controllo contro chi_massa.txt (238de05e): kappa 2.5289441539e-04, c0 +3.8058988126e-04 -> %s" % (
            "COINCIDONO" if "%.10e" % P.kappa == "2.5289441539e-04" and "%+.10e" % P.c0 == "+3.8058988126e-04" else "NON coincidono"))
        print("    e0 = C.e0 %.6e; G2.eps_top_tl4b %.6e" % (e0, float(MT.G2.eps_top_tl4b())))
        with np.load(CT.F_C2_3000) as d:
            S3 = {x: d[x].copy() for x in Z["chiavi"]}
            A3, E3 = d["campo_A"].copy(), d["campo_E"].copy()
            cs3 = d["cs_prec"].copy()
        # ------------------------------------------------------------------ K1 il vuoto
        Pv, m0v, _a, _c = CT.parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, "vuoto")
        MT.vuoto_fresco(Z, t0)
        Sv = fotografa()
        C = metti(Sv)
        Av, Ev = C.campo.A.copy(), C.campo.E.copy()
        X = CT.nuovo_X(n, m)
        zeri = True
        for _k in range(N_BIT):
            CT.tick_chi(Z["z"], C.campo, Pv, Lp, X)
            zeri &= bool(np.all(X["chi"] == 0.0) and np.all(X["pi"] == 0.0))
        R1 = (fotografa(), C.campo.A.copy(), C.campo.E.copy())
        C = metti(Sv, Av, Ev)
        for _k in range(N_BIT):
            MT.PBR.tick_GU(Z["z"], s, ("uno",), e0, C.campo)
        R2 = (fotografa(), C.campo.A.copy(), C.campo.E.copy())
        dv = uguali(*R1, *R2)
        esiti["K1"] = zeri and not dv
        print("### K1 IL VUOTO (c0 del vuoto %+.10e, kappa di C2): chi e pi a 0 al bit per %d tick: %s; lo stato contro tick_GU con ('uno',): %s -> %s" % (
            Pv.c0, N_BIT, zeri, "AL BIT" if not dv else "DIVERSE: %s" % dv, "PASSA" if esiti["K1"] else "NON PASSA"))
        # ------------------------------------------------------------------ K2 kappa = 0
        P0 = CT.Parametri(0.0, 0.0, s, e0)
        C = metti(S3, A3, E3)
        X = CT.nuovo_X(n, m)
        for _k in range(N_BIT):
            CT.tick_chi(Z["z"], C.campo, P0, Lp, X)
        R1 = (fotografa(), C.campo.A.copy(), C.campo.E.copy())
        C = metti(S3, A3, E3)
        for _k in range(N_BIT):
            MT.PBR.tick_GU(Z["z"], s, ("uno",), e0, C.campo)
        R2 = (fotografa(), C.campo.A.copy(), C.campo.E.copy())
        dv = uguali(*R1, *R2)
        esiti["K2"] = not dv
        print("### K2 KAPPA = 0 (il mattone di C2 a k 3000, %d tick) contro tick_GU con ('uno',): %s -> %s" % (N_BIT, "AL BIT" if not dv else "DIVERSE: %s" % dv, "PASSA" if esiti["K2"] else "NON PASSA"))
        # ------------------------------------------------------------------ K3 la sorgente ferma (solo il salto di rana di chi)
        Z["metti"]({k: v.copy() for k, v in S3.items()})
        sig0 = P.kappa * (CT.u_di(mot, Z["st"], Z["par"], s, e0) - m0)
        chi_s = Lp.statico(P, sig0)

        def salta(chi, pi, passi, media_da=None):
            acc, cnt = 0.0, 0
            from solitone import toro as TO
            for t in range(1, passi + 1):
                pi += 0.5 * (P.c2 * Lp.delta(chi) - P.m2 * chi + sig0)
                chi += pi
                pi += 0.5 * (P.c2 * Lp.delta(chi) - P.m2 * chi + sig0)
                if media_da is not None and t >= media_da:
                    acc += chi[c_nodo]
                    cnt += 1
            return chi, pi, (acc / cnt if cnt else math.nan)
        with np.load(CT.F_C2_3000) as d:
            cc = [float(x) for x in json.loads(str(d["meta"]))["centro"]]
        from solitone import toro as TO
        rr = np.hypot(*TO.scarti(Z["m1"], Z["m2"], cc[0], cc[1], Z["L"]).T[:2])
        c_nodo = int(np.argmin(rr))
        ch, _p, _ = salta(chi_s.copy(), np.zeros(n), 2000)
        e3a = float(np.max(np.abs(ch - chi_s))) / float(np.max(np.abs(chi_s)))
        _c, _p, med = salta(np.zeros(n), np.zeros(n), 8000, media_da=2000)
        e3b = abs(med - chi_s[c_nodo]) / abs(chi_s[c_nodo])
        esiti["K3"] = e3a <= 1e-10 and e3b <= 0.10
        print("### K3 LA SORGENTE FERMA: dal profilo statico, 2000 passi: %.3e (la soglia 1e-10); da 0, la media sui passi 2000-8000 al centro %.6e contro lo statico %.6e: %.4f (la soglia 0.10) -> %s" % (
            e3a, med, chi_s[c_nodo], e3b, "PASSA" if esiti["K3"] else "NON PASSA"))
        # ------------------------------------------------------------------ K4 l'impulso
        import scipy.sparse as sp
        from scipy.sparse import csgraph
        Adj = sp.csr_matrix((np.ones(2 * len(Lp.ii)), (np.concatenate([Lp.ii, Lp.jj]), np.concatenate([Lp.jj, Lp.ii]))), shape=(n, n))
        dist = csgraph.shortest_path(Adj, unweighted=True, indices=c_nodo)
        chi = np.zeros(n)
        chi[c_nodo] = 1.0
        pi = np.zeros(n)
        k4 = True
        for t in range(1, 31):
            pi += 0.5 * (P.c2 * Lp.delta(chi) - P.m2 * chi)
            chi += pi
            pi += 0.5 * (P.c2 * Lp.delta(chi) - P.m2 * chi)
            fuori = bool(np.all(chi[dist > t] == 0.0))
            fronte = bool(np.any(chi[dist == t] != 0.0))
            k4 &= fuori and fronte
        esiti["K4"] = k4
        print("### K4 L'IMPULSO (chi = 1 al nodo %d): per t = 1..30, chi = 0 esatto oltre t passi e non zero a t: %s -> %s" % (c_nodo, k4, "PASSA" if k4 else "NON PASSA"))
        # ------------------------------------------------------------------ K5 l'energia, il determinismo, la ripresa, il costo
        C = metti(S3, A3, E3)
        chi0 = CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0)
        X = CT.nuovo_X(n, m, chi0)
        H0, Hc0 = CT.energia_chi(mot, Z["st"], Z["par"], P, Lp, X, C.campo)
        Hs = [H0]
        t1 = time.time()
        for k in range(1, 101):
            CT.tick_chi(Z["z"], C.campo, P, Lp, X)
            if k == N_BIT:
                t_chi = (time.time() - t1) / N_BIT
                D1 = (fotografa(), C.campo.A.copy(), C.campo.E.copy(), CT.copia_X(X))
            if k % 10 == 0:
                Hs.append(CT.energia_chi(mot, Z["st"], Z["par"], P, Lp, X, C.campo)[0])
        d_chi = max(abs(h - H0) for h in Hs) / abs(H0)
        C = metti(S3, A3, E3)
        PO.accendi(cs3)
        try:
            Ho0 = CT.energia_oggi(mot, Z["st"], Z["par"], s, C.legge, e0, C.campo)
            Ho = [Ho0]
            t1 = time.time()
            for k in range(1, 101):
                MT.PBR.tick_GU(Z["z"], s, C.legge, e0, C.campo)
                if k == N_BIT:
                    t_oggi = (time.time() - t1) / N_BIT
                if k % 10 == 0:
                    Ho.append(CT.energia_oggi(mot, Z["st"], Z["par"], s, C.legge, e0, C.campo))
        finally:
            LC.spegni()
        d_oggi = max(abs(h - Ho0) for h in Ho) / abs(Ho0)
        esiti["K5"] = d_chi <= 10.0 * d_oggi + 1e-12
        print("### K5 L'ENERGIA (100 tick dal mattone di C2 a k 3000; chi al profilo statico, H_chi iniziale %+.6e): la deriva relativa con chi %.3e, il tick di oggi %.3e (il rapporto %.2f; la soglia 10 volte + 1e-12) -> %s" % (
            Hc0, d_chi, d_oggi, d_chi / d_oggi if d_oggi else math.nan, "PASSA" if esiti["K5"] else "NON PASSA"))
        print("    H con chi: %s" % " ".join("%+.10e" % h for h in Hs[:4]))
        print("    H di oggi: %s" % " ".join("%+.10e" % h for h in Ho[:4]))
        # il determinismo
        C = metti(S3, A3, E3)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0))
        for _k in range(N_BIT):
            CT.tick_chi(Z["z"], C.campo, P, Lp, X)
        D2 = (fotografa(), C.campo.A.copy(), C.campo.E.copy(), CT.copia_X(X))
        dd = uguali(D1[0], D1[1], D1[2], D2[0], D2[1], D2[2]) + [k for k in CT.CHIAVI_CHI if not np.array_equal(D1[3][k], D2[3][k])]
        esiti["determinismo"] = not dd
        print("### IL DETERMINISMO (due volte %d tick dallo stesso stato): %s" % (N_BIT, "AL BIT" if not dd else "DIVERSE: %s" % dd))
        # la ripresa: 10 + salva + riprendi + 10 contro i 20 di fila (D2)
        C = metti(S3, A3, E3)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0))
        for _k in range(N_BIT // 2):
            CT.tick_chi(Z["z"], C.campo, P, Lp, X)
        os.makedirs(DIR_PROVA, exist_ok=True)
        f = os.path.join(DIR_PROVA, "ripresa_%05d.npz" % (N_BIT // 2))
        dati = {x: Z["st"][x] for x in Z["chiavi"]}
        dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{k: X[k] for k in CT.CHIAVI_CHI})
        np.savez(f, **dati)
        with np.load(f) as d:
            Sr = {x: d[x].copy() for x in Z["chiavi"]}
            Ar, Er = d["campo_A"].copy(), d["campo_E"].copy()
            Xr = {k: d[k].copy() for k in CT.CHIAVI_CHI}
        C = metti(Sr, Ar, Er)
        for _k in range(N_BIT // 2):
            CT.tick_chi(Z["z"], C.campo, P, Lp, Xr)
        D3 = (fotografa(), C.campo.A.copy(), C.campo.E.copy(), Xr)
        dd = uguali(D2[0], D2[1], D2[2], D3[0], D3[1], D3[2]) + [k for k in CT.CHIAVI_CHI if not np.array_equal(D2[3][k], D3[3][k])]
        esiti["ripresa"] = not dd
        print("### LA RIPRESA (%d + salva + riprendi + %d contro %d di fila): %s (il file %s)" % (N_BIT // 2, N_BIT // 2, N_BIT, "AL BIT" if not dd else "DIVERSE: %s" % dd, f))
        # il costo
        esiti["costo"] = t_chi <= 1.10 * t_oggi
        print("### B3 IL COSTO (i primi %d tick, lo stesso stato, lo stesso processo): con chi %.3f s per tick, il tick di C2 %.3f s per tick: il rapporto %.3f -> %s" % (
            N_BIT, t_chi, t_oggi, t_chi / t_oggi, "ENTRO +10%" if esiti["costo"] else "OLTRE +10%: FERMO"))
        Z["metti"]()
    print("=" * 150)
    print("### GLI ESITI: %s -> %s   (il tempo %.0f s)" % (esiti, "TUTTE PASSANO" if all(esiti.values()) else "NON TUTTE: FERMO", time.time() - t00))
    print("=" * 150)
    return 0 if all(esiti.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
