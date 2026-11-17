# -*- coding: utf-8 -*-
r"""**LA PROVA DELLA SIMMETRIA C DI G+U** *(Luca `2026-11-17` `09:49`, il mandato unico, C2; la carta `doc/TASK_HISTORY/2026-11-17_mitosi_primo_passo.md`, sez. `2.3`; sul modello di `doc/referti_l2/mattone/specchio_carta.py`)*.

    E:\python\py3132\python.exe doc/referti_l2/simmetria_C.py > doc/referti_l2/simmetria_C.txt     (PYTHONNOUSERSITE=1, 1 filo, numba spento)

**L'operatore C** *(per estremita', nessuna permutazione dei nodi)*: `psi_h -> conj(psi_h) T^T` *(e `psi` per nodo allo stesso modo)*, `phi_h -> f(phi_h)`, `campo_A -> s A`, `campo_E -> s E`, le altre chiavi *(reali: `Lambda`, `rho`, `h_int`)* invariate, il lapse invariato.
**I candidati** *(`32`, scritti nella carta PRIMA)*: `T` in `{I, sigma_x, sigma_y, sigma_z}`; `f` in `{phi, -phi, conj(phi), -conj(phi)}`; `s` in `{+1, -1}`.
**(K) IL CASO NOTO, prima** *(Q-A4)*: **K1** `C(C(x)) = x` per ogni candidato *(`sigma_y` da' `-x` su `psi`: una fase globale)*; **K2** il vortice `+1` costruito a mano *(come `segni_vortice.py`)* coniugato da' il giro `-1` e L della corrente di fase col segno opposto; **DEVE FALLIRE**: senza coniugio il giro resta `+1`.
**(P) LA PROVA:** dallo stato `L162_MGU_03000` *(la scena S162, i campi `MGU`, `e = PB.E_DECISO`)* **e da uno stato a caso** *(seme `11`: `psi_h` con una fase casuale per elemento; `A`, `E` piu' un rumore `1e-3` del loro massimo)*: `C(tick^N(x))` contro `tick^N(C(x))`; `1` tick per i `32`; `10` tick per i due migliori; la differenza relativa per chiave, **entro `40` nodi dal baricentro del mattone** *(il bordo rompe C per costruzione: la carta, sez. `1`)* e sul toro intero.
**LA LETTURA** *(fissata nella carta)*: **C ESISTE se il migliore, dopo `10` tick, sta sotto `1e-12` entro `40` nodi PER ENTRAMBI gli stati** *(la previsione del guardiano)*.
"""
import itertools
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_SOL, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
from solitone import toro as TO  # noqa: E402

N_LUNGO = 10
R_VICINO = 40.0
SOGLIA = 1e-12
SEME = 11
RUMORE = 1e-3
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
TS = (("I", np.eye(2, dtype=complex)), ("sigma_x", SX), ("sigma_y", SY), ("sigma_z", SZ))
FS = (("phi", lambda p: p), ("-phi", lambda p: -p), ("conj(phi)", np.conj), ("-conj(phi)", lambda p: -np.conj(p)))
SS = (+1.0, -1.0)


def coniuga(X, A, E, T, f, s, coniugio=True):
    """### C sullo stato: `psi_h`, `psi` per `T` dopo il coniugio; `phi_h` per `f`; `A`, `E` per `s`; il resto invariato."""
    Y = {}
    for k, a in X.items():
        if k in ("psi_h", "psi"):
            b = np.conj(a) if coniugio else a
            Y[k] = b @ T.T
        elif k == "phi_h":
            Y[k] = f(a)
        else:
            assert not np.iscomplexobj(a), "la chiave %s e' complessa e C non sa trattarla: FERMO" % k
            Y[k] = a.copy()
    return Y, s * A, s * E


def main():
    import _presidio
    import _u1_prototipo as U1
    import triangolo_120 as T120
    _presidio.avvia(os.path.join(_SOL, "mattone.py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(os.path.join(_SOL, "triangolo_120.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("LA PROVA DELLA SIMMETRIA C DI G+U (Luca 2026-11-17 09:49, C2); sys.executable %s; e %r; la soglia %.0e dopo %d tick entro %.0f nodi" % (sys.executable, e, SOGLIA, N_LUNGO, R_VICINO))
    print("=" * 130)
    esiti = []
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        mot = Z["mot"]
        nodo = np.asarray(mot.inc.nodo)
        f0 = os.path.join(MT.DIR_E, "L162_MGU_03000.npz")
        with np.load(f0) as d:
            X0 = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
            t0 = int(json.loads(str(d["meta"]))["t"])
        print("### LO STATO: %s (t %d); le chiavi %s" % (f0, t0, {k: (X0[k].shape, str(X0[k].dtype)) for k in X0}))
        print("    max |A| %.4e, max |E| %.4e" % (float(np.max(np.abs(A0))), float(np.max(np.abs(E0)))))
        rho = np.sum(np.abs(X0["psi_h"][Z["righe"]].reshape(n, -1)) ** 2, axis=1)   # la materia per nodo dalle sue 6 estremita'
        w = rho / rho.sum()
        # il baricentro sul toro: la media circolare per coordinata di indice
        c1 = (math.atan2(float(np.sum(w * np.sin(2 * math.pi * m1 / L))), float(np.sum(w * np.cos(2 * math.pi * m1 / L)))) % (2 * math.pi)) * L / (2 * math.pi)
        c2 = (math.atan2(float(np.sum(w * np.sin(2 * math.pi * m2 / L))), float(np.sum(w * np.cos(2 * math.pi * m2 / L)))) % (2 * math.pi)) * L / (2 * math.pi)
        r_n = np.hypot(*TO.scarti(m1, m2, c1, c2, L).T[:2])
        vic_n = r_n <= R_VICINO
        vic_h = vic_n[nodo]
        C0 = MT.Campi(Z, "MGU", rho_c, e)
        ci, cj = np.asarray(C0.campo.ii), np.asarray(C0.campo.jj)
        vic_a = vic_n[ci] & vic_n[cj]
        print("### il baricentro della materia (%.3f, %.3f); entro %.0f nodi: %d nodi, %d estremita', %d archi del campo; la materia entro: %.6f del totale" % (
            c1, c2, R_VICINO, int(vic_n.sum()), int(vic_h.sum()), int(vic_a.sum()), float(w[vic_n].sum())))

        # ---------------------------------------------------------------- K1
        print("-" * 130)
        print("### K1 (il caso noto): C(C(x)) contro x, per ogni candidato (al bit)")
        for (tn, T), (fn, f), s in itertools.product(TS, FS, SS):
            Y, A1_, E1_ = coniuga(X0, A0, E0, T, f, s)
            Y2, A2_, E2_ = coniuga(Y, A1_, E1_, T, f, s)
            dmax = max([float(np.max(np.abs(Y2[k] - X0[k]))) for k in X0] + [float(np.max(np.abs(A2_ - A0))), float(np.max(np.abs(E2_ - E0)))])
            dneg = float(np.max(np.abs(Y2["psi_h"] + X0["psi_h"])))
            ok = dmax == 0.0 or (tn == "sigma_y" and dneg == 0.0)
            if (fn, s) == ("phi", 1.0) or not ok:
                print("    T %-8s f %-11s s %+.0f: max |C(C(x)) - x| %.3e%s" % (tn, fn, s, dmax, ("; C(C(psi_h)) = -psi_h al bit (%.1e): una fase globale" % dneg) if tn == "sigma_y" else ""))
            esiti.append(("K1. C(C(x)) = x (sigma_y: -x su psi) per T %s, f %s, s %+.0f" % (tn, fn, s), ok))
        print("    (stampati i soli f = phi, s = +1 e gli eventuali che NON passano; i 32 sono tutti nei DEVE)")

        # ---------------------------------------------------------------- K2
        print("-" * 130)
        print("### K2 (il caso noto): il vortice +1 costruito a mano (come segni_vortice.py), coniugato")
        CEN, RA, WA, RL = (81.0, 81.0), 15.0, 5.0, 40.0
        D = TO.scarti(m1, m2, CEN[0], CEN[1], L)
        dx, dy = D[:, 0], D[:, 1]
        r = np.hypot(dx, dy)
        th = np.arctan2(dy, dx)
        psin = X0["psi_h"][Z["righe"]].reshape(n, -1)
        jm = int(np.argmax(np.sum(np.abs(psin) ** 2, axis=1)))
        Am = float(np.linalg.norm(psin[jm]))
        u = (psin[jm] / Am).reshape(Z["righe"].shape[1], -1)
        fr = np.exp(-((r - RA) / WA) ** 2)
        ii, jj = np.asarray(mot.inc.ii), np.asarray(mot.inc.jj)
        de = TO.scarti(m1[jj], m2[jj], m1[ii], m2[ii], L)
        ex, ey = dx[ii] + 0.5 * de[:, 0], dy[ii] + 0.5 * de[:, 1]
        dentro = np.hypot(ex, ey) <= RL
        ph = np.zeros_like(X0["psi_h"])
        ph[Z["righe"]] = (Am * fr * np.exp(1j * th))[:, None, None] * u[None, :, :]

        def giro_e_L(psi_h):
            ps = psi_h[Z["righe"]].reshape(n, -1)
            g = T120.giro_di(np.concatenate([ps, ps.sum(axis=1, keepdims=True)], axis=1), m1, m2, L, CEN, RA)
            jf = np.imag(np.sum(np.conj(ps[ii]) * ps[jj], axis=1))
            return g, float(np.sum((jf * (ex * de[:, 1] - ey * de[:, 0]))[dentro]))
        g0, L0 = giro_e_L(ph)
        print("    il vortice: il giro della somma %+.3f; L della corrente di fase %+.6e" % (g0[-1], L0))
        for tn, T in TS:
            gC, LC = giro_e_L(np.conj(ph) @ T.T)
            print("    C con T %-8s: il giro della somma %+.3f; L %+.6e (il rapporto con quello del vortice %+.6f)" % (tn, gC[-1], LC, LC / L0))
            esiti.append(("K2. T %s: il vortice +1 coniugato ha il giro -1 (entro 0.1) e L col segno opposto" % tn, abs(gC[-1] + 1) < 0.1 and LC * L0 < 0))
        gN, LN = giro_e_L(ph @ SX.T)
        print("    DEVE FALLIRE (sigma_x SENZA coniugio): il giro %+.3f; L %+.6e" % (gN[-1], LN))
        esiti.append(("K2. DEVE FALLIRE: senza coniugio il giro NON e' -1 (resta +1)", abs(gN[-1] + 1) >= 0.1))

        # ---------------------------------------------------------------- P
        def corri(X, A, E, N):
            Z["metti"]({k: v_.copy() for k, v_ in X.items()})
            Cx = MT.Campi(Z, "MGU", rho_c, e)
            Cx.campo.A[...] = A
            Cx.campo.E[...] = E
            Cx.campo.e = e
            Cx.e_prec = e
            U1.scrivi_U(Z["mot"], Cx.campo)
            for k in range(1, N + 1):
                Cx.tick(k, t0 + k, 1.0, e)
            return {k: Z["st"][k].copy() for k in X}, Cx.campo.A.copy(), Cx.campo.E.copy()

        def diff(P, Q):
            out = {}
            for k, m in (("psi_h", vic_h), ("phi_h", vic_h)):
                sc = float(np.max(np.abs(Q[0][k])))
                out[k] = float(np.max(np.abs(P[0][k] - Q[0][k]))) / sc
                out[k + "@40"] = float(np.max(np.abs(P[0][k][m] - Q[0][k][m]))) / sc
            for nome, i_, m in (("A", 1, vic_a), ("E", 2, vic_a)):
                sc = max(float(np.max(np.abs(Q[i_]))), 1e-300)
                out[nome] = float(np.max(np.abs(P[i_] - Q[i_]))) / sc
                out[nome + "@40"] = float(np.max(np.abs(P[i_][m] - Q[i_][m]))) / sc
            out["max@40"] = max(out[k] for k in out if k.endswith("@40"))
            return out

        rng = np.random.default_rng(SEME)
        Xr = {k: a.copy() for k, a in X0.items()}
        Xr["psi_h"] = X0["psi_h"] * np.exp(2j * math.pi * rng.random(X0["psi_h"].shape))
        Ar = A0 + RUMORE * max(float(np.max(np.abs(A0))), 1e-12) * rng.standard_normal(A0.shape)
        Er = E0 + RUMORE * max(float(np.max(np.abs(E0))), 1e-12) * rng.standard_normal(E0.shape)
        stati = (("il mattone", X0, A0, E0), ("lo stato a caso (seme %d)" % SEME, Xr, Ar, Er))
        verdetti = []
        for nome, X, A, E in stati:
            print("-" * 130)
            print("### P: %s -- C(tick(x)) contro tick(C(x)), 1 tick, i 32 candidati (la differenza relativa al massimo della chiave; @40 = entro %.0f nodi)" % (nome, R_VICINO))
            t1 = time.time()
            Y1 = corri(X, A, E, 1)
            print("    un tick: %.1f s" % (time.time() - t1))
            ris = []
            for (tn, T), (fn, f), s in itertools.product(TS, FS, SS):
                R1 = coniuga(Y1[0], Y1[1], Y1[2], T, f, s)
                Y2 = corri(*coniuga(X, A, E, T, f, s), 1)
                dd = diff(Y2, R1)
                ris.append((dd["max@40"], tn, fn, s, dd))
                print("    T %-8s f %-11s s %+.0f: psi_h %.3e (@40 %.3e)  phi_h %.3e (%.3e)  A %.3e (%.3e)  E %.3e (%.3e)" % (
                    tn, fn, s, dd["psi_h"], dd["psi_h@40"], dd["phi_h"], dd["phi_h@40"], dd["A"], dd["A@40"], dd["E"], dd["E@40"]))
                sys.stdout.flush()
            ris.sort(key=lambda x: x[0])
            print("### %s: i due migliori su %d tick" % (nome, N_LUNGO))
            YL = corri(X, A, E, N_LUNGO)
            lungo = []
            for _m, tn, fn, s, _d in ris[:2]:
                T, f = dict(TS)[tn], dict(FS)[fn]
                RL_ = coniuga(YL[0], YL[1], YL[2], T, f, s)
                Y2 = corri(*coniuga(X, A, E, T, f, s), N_LUNGO)
                dd = diff(Y2, RL_)
                lungo.append((dd["max@40"], tn, fn, s, dd))
                print("    T %-8s f %-11s s %+.0f: dopo %d tick psi_h %.3e (@40 %.3e)  phi_h %.3e (%.3e)  A %.3e (%.3e)  E %.3e (%.3e)" % (
                    tn, fn, s, N_LUNGO, dd["psi_h"], dd["psi_h@40"], dd["phi_h"], dd["phi_h@40"], dd["A"], dd["A@40"], dd["E"], dd["E@40"]))
            verdetti.append((nome, min(lungo, key=lambda x: x[0]), ris[0]))
        Z["metti"]()
    print("-" * 130)
    for nm, ok in esiti:
        if not ok or nm.startswith("K2"):
            print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    k_ok = all(ok for _n, ok in esiti)
    print("  K1: %d su %d PASSANO; K2: %s" % (sum(1 for nm, ok in esiti if nm.startswith("K1") and ok), sum(1 for nm, _ in esiti if nm.startswith("K1")), "tutti come devono" if all(ok for nm, ok in esiti if nm.startswith("K2")) else "### NO"))
    print("=" * 130)
    tutti = True
    for nome, (m, tn, fn, s, dd), (m1_, tn1, fn1, s1, _d1) in verdetti:
        print("### %s: il migliore dopo %d tick T %s, f %s, s %+.0f: entro %.0f nodi %.3e (dopo 1 tick il migliore era T %s, f %s, s %+.0f: %.3e)" % (nome, N_LUNGO, tn, fn, s, R_VICINO, m, tn1, fn1, s1, m1_))
        tutti = tutti and m < SOGLIA
    print("### C2, LA LETTURA (fissata prima: C esiste se il migliore dopo %d tick sta sotto %.0e entro %.0f nodi per ENTRAMBI gli stati): %s" % (
        N_LUNGO, SOGLIA, R_VICINO, ("C ESISTE" if tutti else "### C NON ESISTE FRA I 32 CANDIDATI (la previsione del guardiano CADE)") if k_ok else "### IL CASO NOTO NON PASSA: LA PROVA NON SI LEGGE"))
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0 if (k_ok and tutti) else 1


if __name__ == "__main__":
    sys.exit(main())
