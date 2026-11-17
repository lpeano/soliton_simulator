# -*- coding: utf-8 -*-
r"""**LA PROVA CP E CPT DI G+U** *(Luca `2026-11-17` `11:33`, parte B; la carta `doc/TASK_HISTORY/2026-11-17_misure_CP_mitosi.md`, sez. `2.2`; sul modello di `simmetria_C.py` e `mattone/specchio_carta.py`)*.

    E:\python\py3132\python.exe doc/referti_l2/simmetria_CP.py > doc/referti_l2/simmetria_CP.txt     (PYTHONNOUSERSITE=1, 1 filo, numba spento)

**Gli operatori `Theta`** *(ANTIUNITARI: sempre il coniugio)*: **la mappa spaziale `P`** in `{inv: l'inversione x -> -x attorno al nodo p0 (M = -I), spec: lo specchio a 30 gradi per p0 (la M di specchio_carta.py), id: nessuna}`; **lo spinore** `psi -> T conj(psi)` con `T` in `{I, sx, sy, sz}` *(e `sigma.l M`, `sigma.l_perp M` con `M` in `{I, sx, sy, sz}` per lo specchio: `12`)*; **`phi`** in `{phi, -phi, conj, -conj}`; **`A -> sA (verso) A`, `E -> sE (verso) E`** con `sA`, `sE` in `{+1, -1}` *(separati: la carta, sez. `1`)*; le chiavi reali permutate.
**CP** *(`inv`, `spec`: `256` operatori)*: `Theta(tick(x))` contro `tick(Theta(x))`. **CPT** *(`inv`, `spec`, `id`: `320`)*: `tick(Theta(tick(x)))` contro `Theta(x)` *(un antiunitario che rovescia il tempo: `U Theta U = Theta`)*.
**IL PROTOCOLLO** *(scritto nella carta)*: **lo schermo** a `1` tick sul mattone per tutti; **i due migliori di CP e di CPT** a `10` tick sul mattone e sullo stato a caso *(seme `11`, come C2)*; **entro `40` nodi dal baricentro della materia** e sul toro.
**Q-A4 prima:** **K1** `Theta(Theta(x))` contro `x`; **K2** un pacchetto con il gradiente di fase verso `+x`: la corrente `J_x` cambia segno sotto P *(inv, senza coniugio)* e sotto C, **NON sotto CP** *(il caso che DEVE fallire: «sotto CP cambia segno»)*; **il controllo positivo:** l'identita' *(nessuna mappa, nessun coniugio)* da' `0`.
**LA LETTURA** *(fissata prima)*: **CP (o CPT) ESISTE se il migliore, dopo `10` tick, sta sotto `1e-12` entro `40` nodi per ENTRAMBI gli stati.**
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
for _p in (_QUI, os.path.join(_QUI, "mattone"), _SOL, _CSV):
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
I2 = np.eye(2, dtype=complex)
FS = (("phi", lambda p: p), ("-phi", lambda p: -p), ("conj(phi)", np.conj), ("-conj(phi)", lambda p: -np.conj(p)))
SEGNI = tuple(itertools.product((1.0, -1.0), (1.0, -1.0)))


def main():
    import _presidio
    import _u1_prototipo as U1
    import specchio_carta as SPC
    _presidio.avvia(os.path.join(_SOL, "mattone.py"))
    _presidio.avvia(os.path.join(_QUI, "mattone", "specchio_carta.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("LA PROVA CP E CPT DI G+U (Luca 2026-11-17 11:33, B); sys.executable %s; e %r; la soglia %.0e dopo %d tick entro %.0f nodi" % (sys.executable, e, SOGLIA, N_LUNGO, R_VICINO))
    print("=" * 130)
    esiti = []
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        mot = Z["mot"]
        nodo = np.asarray(mot.inc.nodo)
        ii, jj = nodo[0::2], nodo[1::2]
        with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
            X0 = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
            t0 = int(json.loads(str(d["meta"]))["t"])
        rho = np.sum(np.abs(X0["psi_h"][Z["righe"]].reshape(n, -1)) ** 2, axis=1)
        cb = TO.centro(rho, m1, m2, L)[:2]
        p0 = (int(round(cb[0])) % L, int(round(cb[1])) % L)
        r_n = np.hypot(*TO.scarti(m1, m2, p0[0], p0[1], L).T[:2])
        vic_n = r_n <= R_VICINO
        vic_h = vic_n[nodo]
        C0 = MT.Campi(Z, "MGU", rho_c, e)
        ci, cj = np.asarray(C0.campo.ii), np.asarray(C0.campo.jj)
        vic_a = vic_n[ci] & vic_n[cj]
        print("### il baricentro della materia (%.3f, %.3f); il centro delle mappe p0 = %s; entro %.0f nodi da p0: %d nodi, la materia %.6f del totale" % (cb[0], cb[1], p0, R_VICINO, int(vic_n.sum()), float(rho[vic_n].sum() / rho.sum())))
        # ---------------------------------------------------------------- le mappe spaziali
        A1v, A2v = TO.vettori()
        d30 = 2 * A1v + A2v
        ang = math.atan2(d30[1], d30[0])
        c2, s2 = math.cos(2 * ang), math.sin(2 * ang)
        MAPPE = {"inv": -np.eye(2), "spec": np.array([[c2, s2], [s2, -c2]])}
        geo = {"id": (v.copy(), np.arange(len(ii)), np.zeros(len(ii), bool), np.arange(2 * len(ii)), np.arange(len(ci)), np.zeros(len(ci), bool))}
        for nome, M in MAPPE.items():
            P = np.outer(m1 - p0[0], A1v) + np.outer(m2 - p0[1], A2v)
            q = (P @ M.T) @ np.linalg.inv(np.column_stack([A1v, A2v])).T
            qi = np.rint(q)
            scarto = float(np.max(np.abs(q - qi)))
            sig = ((qi[:, 0].astype(int) + p0[0]) % L) * L + (qi[:, 1].astype(int) + p0[1]) % L
            assert scarto < 1e-9 and np.array_equal(np.sort(sig), v) and np.array_equal(sig[sig], v), "la mappa %s non e' una involuzione del reticolo: FERMO" % nome
            ap, rov = SPC.mappa_archi(ii, jj, sig)
            hp = np.empty(2 * len(ap), dtype=int)
            hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
            hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
            assert np.array_equal(nodo[hp], sig[nodo]), "la mappa delle estremita' non porta il nodo giusto: FERMO"
            cap, crov = SPC.mappa_archi(ci, cj, sig)
            geo[nome] = (sig, ap, rov, hp, cap, crov)
            print("### la mappa %s: lo scarto %.1e; gli archi della passeggiata rovesciati %d su %d; gli archi del campo rovesciati %d su %d" % (nome, scarto, int(rov.sum()), len(ap), int(crov.sum()), len(cap)))
        lv = np.array([math.cos(ang), math.sin(ang)])
        lp = np.array([-math.sin(ang), math.cos(ang)])
        TS = {"inv": (("I", I2), ("sx", SX), ("sy", SY), ("sz", SZ)),
              "spec": (("I", I2), ("sx", SX), ("sy", SY), ("sz", SZ)) + tuple(
                  ("%s.%s" % (ln, mn), Lm @ Mm) for (ln, Lm) in (("s.l", lv[0] * SX + lv[1] * SY), ("s.lp", lp[0] * SX + lp[1] * SY))
                  for (mn, Mm) in (("I", I2), ("sx", SX), ("sy", SY), ("sz", SZ))),   # ### con il coniugio servono i prodotti sigma.l M (la carta ne aveva 6: scostamento dichiarato)
              "id": (("I", I2), ("sx", SX), ("sy", SY), ("sz", SZ))}

        def theta(X, A, E, mp, T, f, sA, sE, cj=True):
            sig, _ap, _rov, hp, cap, crov = geo[mp]
            Y = {}
            for k, a in X.items():
                b = np.conj(a) if (cj and np.iscomplexobj(a)) else a
                if k in ("psi_h", "psi"):
                    b = b @ T.T
                elif k == "phi_h":
                    b = f(a)
                y = np.empty_like(b)
                if a.shape[0] == n:
                    y[sig] = b
                elif a.shape[0] == len(hp):
                    y[hp] = b
                else:
                    raise RuntimeError("la chiave %s di forma %s: non so trasformarla" % (k, a.shape))
                Y[k] = y
            segno = np.where(crov, -1.0, 1.0)
            Ar = np.empty_like(A)
            Er = np.empty_like(E)
            Ar[cap] = sA * segno * A
            Er[cap] = sE * segno * E
            return Y, Ar, Er

        CAND = {"CP": [], "CPT": []}
        for mp in ("inv", "spec", "id"):
            for (tn, T), (fn, f), (sA, sE) in itertools.product(TS[mp], FS, SEGNI):
                c = (mp, tn, T, fn, f, sA, sE)
                if mp != "id":
                    CAND["CP"].append(c)
                CAND["CPT"].append(c)
        print("### i candidati: CP %d (inv %d, spec %d); CPT %d (con id %d)" % (len(CAND["CP"]), 4 * 4 * 4, len(TS["spec"]) * 4 * 4, len(CAND["CPT"]), 4 * 4 * 4))

        # ---------------------------------------------------------------- K1
        print("-" * 130)
        print("### K1: Theta(Theta(x)) contro x")
        k1 = {}
        for (mp, tn, T, fn, f, sA, sE) in CAND["CPT"]:
            Y = theta(*theta(X0, A0, E0, mp, T, f, sA, sE), mp, T, f, sA, sE)
            dmax = max([float(np.max(np.abs(Y[0][k] - X0[k]))) for k in X0] + [float(np.max(np.abs(Y[1] - A0))), float(np.max(np.abs(Y[2] - E0)))])
            dneg = float(np.max(np.abs(Y[0]["psi_h"] + X0["psi_h"])))
            k1.setdefault((mp, tn), []).append(min(dmax, dneg))
        for (mp, tn), vals in k1.items():
            print("    %-5s T %-8s: max |Theta^2(x) - x| (o + x su psi: la fase globale) %.3e" % (mp, tn, max(vals)))
            if tn in ("I", "sx", "sy", "sz"):
                esiti.append(("K1. %s T %s: Theta^2 = x (o -x su psi) al bit" % (mp, tn), max(vals) == 0.0))

        # ---------------------------------------------------------------- K2
        print("-" * 130)
        D = TO.scarti(m1, m2, p0[0], p0[1], L)
        g = np.exp(-(np.hypot(D[:, 0], D[:, 1]) / 8.0) ** 2) * np.exp(1j * 0.3 * D[:, 0])
        psin = X0["psi_h"][Z["righe"]].reshape(n, -1)
        u = (psin[int(np.argmax(rho))] / np.linalg.norm(psin[int(np.argmax(rho))])).reshape(Z["righe"].shape[1], -1)
        pk = np.zeros_like(X0["psi_h"])
        pk[Z["righe"]] = g[:, None, None] * u[None, :, :]
        de = TO.scarti(m1[jj], m2[jj], m1[ii], m2[ii], L)

        def Jx(ph):
            ps = ph[Z["righe"]].reshape(n, -1)
            return float(np.sum(np.imag(np.sum(np.conj(ps[ii]) * ps[jj], axis=1)) * de[:, 0]))
        Xk = dict(X0)
        Xk["psi_h"] = pk
        j0 = Jx(pk)
        jP = Jx(theta(Xk, A0, E0, "inv", I2, FS[0][1], 1.0, 1.0, cj=False)[0]["psi_h"])
        jC = Jx(theta(Xk, A0, E0, "id", I2, FS[0][1], 1.0, 1.0)[0]["psi_h"])
        jCP = Jx(theta(Xk, A0, E0, "inv", I2, FS[0][1], 1.0, 1.0)[0]["psi_h"])
        print("### K2: il pacchetto verso +x: J_x %+.6e; sotto P (inv, senza coniugio) %+.6e; sotto C %+.6e; sotto CP %+.6e" % (j0, jP, jC, jCP))
        esiti.append(("K2. il pacchetto va verso +x (J_x > 0)", j0 > 0))
        esiti.append(("K2. sotto P J_x cambia segno (al rapporto -1 entro 1e-12)", abs(jP / j0 + 1) < 1e-12))
        esiti.append(("K2. sotto C J_x cambia segno", abs(jC / j0 + 1) < 1e-12))
        esiti.append(("K2. DEVE FALLIRE: sotto CP J_x cambia segno", not (jCP * j0 < 0)))

        # ---------------------------------------------------------------- la prova
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

        def diff(Pp, Q):
            out = {}
            for k in ("psi_h", "phi_h"):
                sc = float(np.max(np.abs(Q[0][k])))
                out[k] = float(np.max(np.abs(Pp[0][k] - Q[0][k]))) / sc
                out[k + "@40"] = float(np.max(np.abs(Pp[0][k][vic_h] - Q[0][k][vic_h]))) / sc
            for nome, i_ in (("A", 1), ("E", 2)):
                sc = max(float(np.max(np.abs(Q[i_]))), 1e-300)
                out[nome] = float(np.max(np.abs(Pp[i_] - Q[i_]))) / sc
                out[nome + "@40"] = float(np.max(np.abs(Pp[i_][vic_a] - Q[i_][vic_a]))) / sc
            out["max@40"] = max(out[k] for k in out if k.endswith("@40"))
            return out

        def riga(c, dd, N, fam):
            mp, tn, _T, fn, _f, sA, sE = c
            return "    %-3s %-5s T %-8s f %-11s sA %+.0f sE %+.0f, %2d tick: psi_h %.3e (@40 %.3e)  phi_h %.3e (%.3e)  A %.3e (%.3e)  E %.3e (%.3e)" % (
                fam, mp, tn, fn, sA, sE, N, dd["psi_h"], dd["psi_h@40"], dd["phi_h"], dd["phi_h@40"], dd["A"], dd["A@40"], dd["E"], dd["E@40"])

        def prova(fam, c, X, A, E, N, base):
            mp, _tn, T, _fn, f, sA, sE = c
            if fam == "CP":
                return diff(corri(*theta(X, A, E, mp, T, f, sA, sE), N), theta(*base, mp, T, f, sA, sE))
            return diff(corri(*theta(*base, mp, T, f, sA, sE), N), theta(X, A, E, mp, T, f, sA, sE))

        print("-" * 130)
        print("### IL CONTROLLO POSITIVO: l'identita' (nessuna mappa, nessun coniugio), 1 tick")
        b1 = corri(X0, A0, E0, 1)
        ctrl = diff(corri(*theta(X0, A0, E0, "id", I2, FS[0][1], 1.0, 1.0, cj=False), 1), theta(*b1, "id", I2, FS[0][1], 1.0, 1.0, cj=False))
        print("    la differenza %.3e" % ctrl["max@40"])
        esiti.append(("il controllo positivo: l'identita' da' 0", ctrl["max@40"] == 0.0 and max(ctrl.values()) == 0.0))
        print("-" * 130)
        print("### LO SCHERMO: il mattone, 1 tick, tutti i candidati")
        sch = {}
        for fam in ("CP", "CPT"):
            sch[fam] = []
            t1 = time.time()
            for c in CAND[fam]:
                dd = prova(fam, c, X0, A0, E0, 1, b1)
                sch[fam].append((dd["max@40"], c, dd))
            sch[fam].sort(key=lambda x: x[0])
            print("    %s: %d candidati in %.0f s; i primi 6:" % (fam, len(sch[fam]), time.time() - t1))
            for m, c, dd in sch[fam][:6]:
                print(riga(c, dd, 1, fam))
            print("    %s: il peggiore %.3e; la mediana %.3e" % (fam, sch[fam][-1][0], sch[fam][len(sch[fam]) // 2][0]))
            sys.stdout.flush()
        rng = np.random.default_rng(SEME)
        Xr = {k: a.copy() for k, a in X0.items()}
        Xr["psi_h"] = X0["psi_h"] * np.exp(2j * math.pi * rng.random(X0["psi_h"].shape))
        Ar = A0 + RUMORE * max(float(np.max(np.abs(A0))), 1e-12) * rng.standard_normal(A0.shape)
        Er = E0 + RUMORE * max(float(np.max(np.abs(E0))), 1e-12) * rng.standard_normal(E0.shape)
        verd = {}
        for nome_s, X, A, E in (("il mattone", X0, A0, E0), ("lo stato a caso (seme %d)" % SEME, Xr, Ar, Er)):
            print("-" * 130)
            print("### %s: i due migliori di CP e di CPT, %d tick" % (nome_s, N_LUNGO))
            bN = corri(X, A, E, N_LUNGO)
            for fam in ("CP", "CPT"):
                for _m, c, _d in sch[fam][:2]:
                    dd = prova(fam, c, X, A, E, N_LUNGO, bN)
                    print(riga(c, dd, N_LUNGO, fam))
                    verd.setdefault(fam, {}).setdefault(nome_s, []).append(dd["max@40"])
                    sys.stdout.flush()
        Z["metti"]()
    print("-" * 130)
    for nm, ok in esiti:
        if not ok or not nm.startswith("K1"):
            print("  DEVE: %-100s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("  K1: %d su %d come devono" % (sum(1 for nm, ok in esiti if nm.startswith("K1") and ok), sum(1 for nm, _ in esiti if nm.startswith("K1"))))
    k_ok = all(ok for _n, ok in esiti)
    print("=" * 130)
    esiste = {}
    for fam in ("CP", "CPT"):
        m = {s: min(vv) for s, vv in verd[fam].items()}
        esiste[fam] = all(x < SOGLIA for x in m.values())
        print("### %s: il migliore dopo %d tick entro %.0f nodi: %s -> %s" % (fam, N_LUNGO, R_VICINO, ", ".join("%s %.3e" % (s, x) for s, x in m.items()), "ESISTE" if esiste[fam] else "### NON ESISTE fra i candidati"))
    print("### LA LETTURA (fissata prima: esiste se il migliore dopo %d tick sta sotto %.0e entro %.0f nodi per ENTRAMBI gli stati): %s" % (
        N_LUNGO, SOGLIA, R_VICINO, ("CP ESISTE" if esiste["CP"] else ("CP NO; CPT ESISTE" if esiste["CPT"] else "### NE' CP NE' CPT fra i candidati (la previsione del guardiano CADE)")) if k_ok else "### IL CASO NOTO O IL CONTROLLO NON PASSANO: LA PROVA NON SI LEGGE"))
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0 if (k_ok and (esiste["CP"] or esiste["CPT"])) else 1


if __name__ == "__main__":
    sys.exit(main())
