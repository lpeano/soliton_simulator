# -*- coding: utf-8 -*-
r"""**S4: CPT E LO SPECCHIO DEL TICK CON CHI V2 (L'INERZIA f), SENZA BORDO** *(il mandato di Luca `2026-11-21` `23:30`; la carta `doc/TASK_HISTORY/2026-11-21_lorentz_locale.md`, sez. `4.3`; `chi_simmetrie.py` riga per riga, col passo e i parametri di `chi_tick_v2`)*. **IL TITOLO DELLA V1:** **K6: CPT E LO SPECCHIO DEL TICK CON CHI, SENZA BORDO** *(il mandato di Luca `2026-11-21` `15:57`; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `9.3`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_simmetrie_v2.py > doc/referti_l2/chi_simmetrie_v2.txt

**La scena:** `L 186` senza bordo *(`CV.scena_L`)*, il mattone di C2 a `k 3000` con `chi` al profilo statico *(`chi_tick`)*, e uno stato a caso *(seme `11`: le fasi di `psi_h`, `A`, `E`, `chi`, `pi` col rumore `1e-3`)*. **`p0`** = il nodo piu' vicino al baricentro della materia *(come `simmetria_CPT.py`)*.
**CPT** *(l'operatore del `2026-11-17`, `simmetria_CPT_cache.py`)*: l'inversione attorno a `p0`; `psi_h -> sigma_y conj`; `phi_h -> -conj`; `A -> -verso A`, `E -> +verso E`; ### **in piu' `chi -> chi o sigma`, `pi -> - pi o sigma`.** `Q^N(Theta(Q^N(x)))` contro `Theta(x)` su `psi_h`, `phi_h`, `A`, `E`, `chi`, `pi` *(le cache `h_int`, `rho`, `Lambda` e il contatore `theta_a` fuori dal confronto: dichiarato)*: **`N = 10` sotto `1e-12`, `N = 100` sotto `1e-10` (il mattone); `N = 10` lo stato a caso;** **DEVE FALLIRE:** `pi` NON invertito.
**LO SPECCHIO** *(`specchio_carta.py`: la retta a `30` gradi, `2 A1 + A2`, per `p0`; sul toro intero, un automorfismo senza bordo)*: `T = sigma.l`, nessun coniugio, `phi -> -phi`, `A`, `E` col solo segno del verso; **`chi -> chi o sigma`, `pi -> pi o sigma`**; `R(Q^10 x)` contro `Q^10(R x)`: **sotto `1e-10`**; **DEVE FALLIRE:** `chi` e `pi` NON permutati.
"""
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_QUI, "mattone"), os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT
import chi_tick_v2 as CV2

SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SEME = 11
RUMORE = 1e-3
SOGLIE = {10: 1e-12, 100: 1e-10}
SOGLIA_SPECCHIO = 1e-10
CHIAVI = ("psi_h", "phi_h")


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(os.path.join(_QUI, "mattone", "specchio_carta.py"))
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    import specchio_carta as SPC
    from solitone import toro as TO
    MT, CV, PO = PS.MT, PS.CV, PS.PO
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    t00 = time.time()
    print("=" * 150)
    print("K6: CPT E LO SPECCHIO DEL TICK CON CHI, SENZA BORDO (Luca 2026-11-21 15:57; il task history del ramo lapse-u, sez. 9.3)")
    print("=" * 150)
    esiti = {}
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        L, n, m = Z["L"], mot.inc.n, mot.inc.m
        s = float(Z["s"])
        Lp = CT.Laplaciano(mot)
        C = PO.campi(Z, rho_c, e)
        e0 = float(C.e0)
        P, m0 = CV2.parametri_v2(Z, PS, CSB, rho_c, e, t0, s, e0, "C2")
        print("### i parametri: %r" % P)
        with np.load(CT.F_C2_3000) as d:
            X0 = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
        Z["metti"]({k: v.copy() for k, v in X0.items()})
        chi0 = CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0)
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        nodo = np.asarray(mot.inc.nodo)
        ii, jj = nodo[0::2], nodo[1::2]
        rho = CT.rho_di(mot, Z["st"])
        cb = TO.centro(rho, m1, m2, L)[:2]
        p0 = (int(round(cb[0])) % L, int(round(cb[1])) % L)
        Cc = PO.campi(Z, rho_c, e, A0, E0)
        ci, cj = np.asarray(Cc.campo.ii), np.asarray(Cc.campo.jj)

        def mappe(sig):
            assert np.array_equal(np.sort(sig), v), "la mappa dei nodi NON e' una permutazione del toro"
            ap, rov = SPC.mappa_archi(ii, jj, sig)
            hp = np.empty(2 * len(ap), dtype=int)
            hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
            hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
            assert np.array_equal(nodo[hp], sig[nodo])
            cap, crov = SPC.mappa_archi(ci, cj, sig)
            return hp, cap, np.where(crov, -1.0, 1.0)

        A1v, A2v = TO.vettori()
        Pm = np.outer(m1 - p0[0], A1v) + np.outer(m2 - p0[1], A2v)
        qi = np.rint((Pm @ (-np.eye(2)).T) @ np.linalg.inv(np.column_stack([A1v, A2v])).T)
        sig_i = ((qi[:, 0].astype(int) + p0[0]) % L) * L + (qi[:, 1].astype(int) + p0[1]) % L
        hp_i, cap_i, verso_i = mappe(sig_i)
        dirv = 2 * A1v + A2v
        ang = math.atan2(dirv[1], dirv[0])
        sig_s, scarto, _M = SPC.mappa_nodi(L, m1, m2, p0, ang)
        hp_s, cap_s, verso_s = mappe(sig_s)
        print("### p0 = %s; l'inversione: una permutazione del toro; lo specchio a %.1f gradi (2 A1 + A2): lo scarto %.2e" % (p0, math.degrees(ang), scarto))

        def perm(a, sig, hp):
            y = np.empty_like(a)
            if a.shape[0] == n:
                y[sig] = a
            else:
                y[hp] = a
            return y

        def theta(S, A, E, X, inverti_pi=True):
            Y = {}
            for k, a_ in S.items():
                b = np.conj(a_) if np.iscomplexobj(a_) else a_
                if k in ("psi_h", "psi"):
                    b = b @ SY.T
                elif k == "phi_h":
                    b = -b
                Y[k] = perm(b, sig_i, hp_i)
            Ar, Er = np.empty_like(A), np.empty_like(E)
            Ar[cap_i] = -verso_i * A
            Er[cap_i] = verso_i * E
            Xr = {"chi": perm(X["chi"], sig_i, hp_i), "pi": perm(-X["pi"] if inverti_pi else X["pi"], sig_i, hp_i), "theta_a": np.zeros(m)}
            return Y, Ar, Er, Xr

        Tl = math.cos(ang) * SX + math.sin(ang) * SY

        def specchio(S, A, E, X, con_chi=True):
            Y = {}
            for k, a_ in S.items():
                b = a_
                if k in ("psi_h", "psi"):
                    b = b @ Tl.T
                elif k == "phi_h":
                    b = -b
                Y[k] = perm(b, sig_s, hp_s)
            Ar, Er = np.empty_like(A), np.empty_like(E)
            Ar[cap_s] = verso_s * A
            Er[cap_s] = verso_s * E
            if con_chi:
                Xr = {"chi": perm(X["chi"], sig_s, hp_s), "pi": perm(X["pi"], sig_s, hp_s), "theta_a": np.zeros(m)}
            else:
                Xr = {"chi": X["chi"].copy(), "pi": X["pi"].copy(), "theta_a": np.zeros(m)}
            return Y, Ar, Er, Xr

        def corri(S, A, E, X, N):
            Z["metti"]({k: v_.copy() for k, v_ in S.items()})
            Cx = PO.campi(Z, rho_c, e, A.copy(), E.copy())
            Xc = CT.copia_X(X)
            for _k in range(N):
                CV2.tick_chi_v2(Z["z"], Cx.campo, P, Lp, Xc)
            return {k: Z["st"][k].copy() for k in S}, Cx.campo.A.copy(), Cx.campo.E.copy(), Xc

        def rel(a_, b):
            sc = float(np.max(np.abs(b)))
            return float(np.max(np.abs(a_ - b))) / sc if sc > 0 else float(np.max(np.abs(a_)))

        def confronta(U, V):
            d = {k: rel(U[0][k], V[0][k]) for k in CHIAVI}
            d["A"], d["E"] = rel(U[1], V[1]), rel(U[2], V[2])
            d["chi"], d["pi"] = rel(U[3]["chi"], V[3]["chi"]), rel(U[3]["pi"], V[3]["pi"])
            return max(d.values()), d

        Xb = CT.nuovo_X(n, m, chi0)
        rng = np.random.default_rng(SEME)
        Sr = {k: a_.copy() for k, a_ in X0.items()}
        Sr["psi_h"] = X0["psi_h"] * np.exp(2j * math.pi * rng.random(X0["psi_h"].shape))
        Ar = A0 + RUMORE * max(float(np.max(np.abs(A0))), 1e-12) * rng.standard_normal(A0.shape)
        Er = E0 + RUMORE * max(float(np.max(np.abs(E0))), 1e-12) * rng.standard_normal(E0.shape)
        sc_chi = float(np.max(np.abs(chi0)))
        Xr = {"chi": chi0 + RUMORE * sc_chi * rng.standard_normal(n), "pi": RUMORE * sc_chi * rng.standard_normal(n), "theta_a": np.zeros(m)}
        # ------------------------------------------------------------------ CPT
        for nome, S, A, E, X, Ns in (("il mattone", X0, A0, E0, Xb, (10, 100)), ("lo stato a caso (seme %d)" % SEME, Sr, Ar, Er, Xr, (10,))):
            for N in Ns:
                t1 = time.time()
                lato1 = corri(*theta(*corri(S, A, E, X, N)), N)
                lato2 = theta(S, A, E, X)
                mx, d = confronta(lato1, lato2)
                ok = mx < SOGLIE[N]
                esiti["CPT %s N %d" % (nome, N)] = ok
                print("### CPT, %s, N = %d: il massimo %.3e (la soglia %.0e: %s) -- %s  (%.0f s)" % (
                    nome, N, mx, SOGLIE[N], "SOTTO" if ok else "SOPRA", "  ".join("%s %.3e" % kv for kv in d.items()), time.time() - t1))
                sys.stdout.flush()
        lato1 = corri(*theta(*corri(X0, A0, E0, Xb, 10), inverti_pi=False), 10)
        lato2 = theta(X0, A0, E0, Xb, inverti_pi=False)
        mx, d = confronta(lato1, lato2)
        esiti["CPT DEVE FALLIRE"] = mx >= SOGLIE[10]
        print("### CPT DEVE FALLIRE (pi NON invertito), il mattone, N = 10: il massimo %.3e -> %s -- %s" % (mx, "FALLISCE (giusto)" if esiti["CPT DEVE FALLIRE"] else "NON fallisce: la prova non vede pi", "  ".join("%s %.3e" % kv for kv in d.items())))
        # ------------------------------------------------------------------ LO SPECCHIO
        Y = corri(X0, A0, E0, Xb, 10)
        R1 = specchio(*Y)
        R2 = corri(*specchio(X0, A0, E0, Xb), 10)
        mx, d = confronta(R2, R1)
        esiti["specchio"] = mx < SOGLIA_SPECCHIO
        print("### LO SPECCHIO (T = sigma.l, phi -> -phi, A e E col verso, chi e pi permutati), il mattone, 10 tick: il massimo %.3e (la soglia %.0e: %s) -- %s" % (
            mx, SOGLIA_SPECCHIO, "SOTTO" if esiti["specchio"] else "SOPRA", "  ".join("%s %.3e" % kv for kv in d.items())))
        R1f = specchio(*Y, con_chi=False)
        R2f = corri(*specchio(X0, A0, E0, Xb, con_chi=False), 10)
        mx, d = confronta(R2f, R1f)
        esiti["specchio DEVE FALLIRE"] = mx >= SOGLIA_SPECCHIO
        print("### LO SPECCHIO DEVE FALLIRE (chi e pi NON permutati), 10 tick: il massimo %.3e -> %s -- %s" % (mx, "FALLISCE (giusto)" if esiti["specchio DEVE FALLIRE"] else "NON fallisce", "  ".join("%s %.3e" % kv for kv in d.items())))
        Z["metti"]()
    print("=" * 150)
    print("### GLI ESITI: %s -> %s   (il tempo %.0f s)" % (esiti, "TUTTE PASSANO" if all(esiti.values()) else "NON TUTTE: FERMO", time.time() - t00))
    print("=" * 150)
    return 0 if all(esiti.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
