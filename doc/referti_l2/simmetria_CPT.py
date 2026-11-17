# -*- coding: utf-8 -*-
r"""**LA PROVA CPT DEL TICK G+U SENZA IL BORDO, PREVISTA PRIMA** *(Luca `2026-11-17` `13:16`, parte 1; la carta e la previsione `doc/TASK_HISTORY/2026-11-17_CPT_F3_soglia.md`, `815a7fba`)*.

    E:\python\py3132\python.exe doc/referti_l2/simmetria_CPT.py > doc/referti_l2/simmetria_CPT.txt     (PYTHONNOUSERSITE=1, 1 filo, numba spento)

**L'operatore `Theta`** *(trovato in `ebe6dcf0`)*: **la mappa dei nodi** `sigma`: l'inversione `x -> -x` attorno al nodo `p0` piu' vicino al baricentro della materia del mattone *(`M = -I` sul reticolo)*; **le estremita'** permutate con l'arco rovesciato *(`specchio_carta.mappa_archi`)*; **`psi_h -> sigma_y conj(psi_h)`** *(e `psi` per nodo)*; **`phi_h -> -conj(phi_h)`**; **`A -> -(verso) A`, `E -> +(verso) E`** *(il verso: `-1` sugli archi che la mappa rovescia)*; **le chiavi reali permutate coi nodi.** **`cs` NON si tocca: `tick_GU` lo calcola dal suo stato.**
**Il tick `Q`:** `p6_bracci.tick_GU` *(G+U col lapse pieno, SENZA `bordo.assorbi` e SENZA la correzione di Gauss del bordo)*.
**La prova** *(la forma di `ebe6dcf0`)*: **`Q^N(Theta(Q^N(x)))` contro `Theta(x)`**, `N = 10` e `N = 100`, dal mattone `L162_MGU_03000` e dallo stato a caso *(seme `11`, come `simmetria_C.py`)*, **la differenza relativa per chiave sul toro INTERO.** *(La forma del mandato, `Theta(Q^N(Theta(Q^N(x))))` contro `x`, e' la stessa a meno di un `Theta`; ma `Theta^2 = -1` su `psi`: `sigma_y sigma_y^* = -I`, una fase globale.)*
**Q-A4:** **K1** `Theta(Theta(x))` contro `x` *(e contro `-x` su `psi`)*; **il controllo positivo** *(il determinismo: `Q^N(x)` due volte, differenza `0`)*; **il caso che DEVE fallire:** lo stesso operatore SENZA il coniugio, `N = 10`.
**LA PREVISIONE DEL GUARDIANO** *(committata in `815a7fba`)*: **sotto `1e-12` per `N = 10`, sotto `1e-10` per `N = 100`, per ogni chiave, sul toro intero, dai due stati.**
"""
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

SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SOGLIE = {10: 1e-12, 100: 1e-10}
SEME = 11
RUMORE = 1e-3


def main():
    import _presidio
    import _u1_prototipo as U1
    import specchio_carta as SPC
    _presidio.avvia(os.path.join(_SOL, "mattone.py"))
    _presidio.avvia(os.path.join(_SOL, "p6_bracci.py"))
    _presidio.avvia(os.path.join(_QUI, "mattone", "specchio_carta.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("LA PROVA CPT DEL TICK G+U SENZA IL BORDO (Luca 2026-11-17 13:16, parte 1); sys.executable %s; e %r; le soglie %s" % (sys.executable, e, SOGLIE))
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
        rho = np.sum(np.abs(X0["psi_h"][Z["righe"]].reshape(n, -1)) ** 2, axis=1)
        cb = TO.centro(rho, m1, m2, L)[:2]
        p0 = (int(round(cb[0])) % L, int(round(cb[1])) % L)
        C0 = MT.Campi(Z, "MGU", rho_c, e)
        ci, cj = np.asarray(C0.campo.ii), np.asarray(C0.campo.jj)
        A1v, A2v = TO.vettori()
        P = np.outer(m1 - p0[0], A1v) + np.outer(m2 - p0[1], A2v)
        q = (P @ (-np.eye(2)).T) @ np.linalg.inv(np.column_stack([A1v, A2v])).T
        qi = np.rint(q)
        sig = ((qi[:, 0].astype(int) + p0[0]) % L) * L + (qi[:, 1].astype(int) + p0[1]) % L
        assert float(np.max(np.abs(q - qi))) < 1e-9 and np.array_equal(np.sort(sig), v) and np.array_equal(sig[sig], v), "l'inversione non e' una involuzione del reticolo: FERMO"
        ap, rov = SPC.mappa_archi(ii, jj, sig)
        hp = np.empty(2 * len(ap), dtype=int)
        hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
        hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
        assert np.array_equal(nodo[hp], sig[nodo]), "la mappa delle estremita' non porta il nodo giusto: FERMO"
        cap, crov = SPC.mappa_archi(ci, cj, sig)
        verso = np.where(crov, -1.0, 1.0)
        print("### L'OPERATORE: l'inversione attorno a p0 = %s (il baricentro della materia (%.3f, %.3f)); gli archi della passeggiata rovesciati %d su %d, quelli del campo %d su %d" % (p0, cb[0], cb[1], int(rov.sum()), len(ap), int(crov.sum()), len(cap)))
        print("    psi_h -> sigma_y conj(psi_h); phi_h -> -conj(phi_h); A -> -(verso) A; E -> +(verso) E; le chiavi reali permutate; cs non toccato (tick_GU lo calcola)")

        def theta(X, A, E, cj=True):
            Y = {}
            for k, a in X.items():
                b = np.conj(a) if (cj and np.iscomplexobj(a)) else a
                if k in ("psi_h", "psi"):
                    b = b @ SY.T
                elif k == "phi_h":
                    b = -b
                y = np.empty_like(b)
                if a.shape[0] == n:
                    y[sig] = b
                elif a.shape[0] == len(hp):
                    y[hp] = b
                else:
                    raise RuntimeError("la chiave %s di forma %s: non so trasformarla" % (k, a.shape))
                Y[k] = y
            Ar, Er = np.empty_like(A), np.empty_like(E)
            Ar[cap] = -verso * A
            Er[cap] = verso * E
            return Y, Ar, Er

        def corri(X, A, E, N):
            Z["metti"]({k: v_.copy() for k, v_ in X.items()})
            Cx = MT.Campi(Z, "MGU", rho_c, e)
            Cx.campo.A[...] = A
            Cx.campo.E[...] = E
            Cx.campo.e = e
            Cx.e_prec = e
            U1.scrivi_U(mot, Cx.campo)
            for _k in range(N):
                MT.PBR.tick_GU(Z["z"], Z["s"], Cx.legge, Cx.e0, Cx.campo)
            return {k: Z["st"][k].copy() for k in X}, Cx.campo.A.copy(), Cx.campo.E.copy()

        def diff(Pp, Q):
            out = {}
            for k in Q[0]:
                sc = float(np.max(np.abs(Q[0][k])))
                out[k] = float(np.max(np.abs(Pp[0][k] - Q[0][k]))) / sc if sc > 0 else float(np.max(np.abs(Pp[0][k])))
            out["A"] = float(np.max(np.abs(Pp[1] - Q[1]))) / max(float(np.max(np.abs(Q[1]))), 1e-300)
            out["E"] = float(np.max(np.abs(Pp[2] - Q[2]))) / max(float(np.max(np.abs(Q[2]))), 1e-300)
            return out

        def fmt(dd):
            return "  ".join("%s %.3e" % (k, dd[k]) for k in sorted(dd))

        # ---------------------------------------------------------------- K1
        print("-" * 130)
        Y = theta(*theta(X0, A0, E0))
        k1 = {k: float(np.max(np.abs(Y[0][k] - X0[k]))) for k in X0}
        k1m = {k: float(np.max(np.abs(Y[0][k] + X0[k]))) for k in ("psi_h", "psi") if k in X0}
        print("### K1: Theta(Theta(x)) contro x: %s; A %.3e; E %.3e; su psi contro -x: %s" % (
            ", ".join("%s %.3e" % kv for kv in sorted(k1.items())), float(np.max(np.abs(Y[1] - A0))), float(np.max(np.abs(Y[2] - E0))), ", ".join("%s %.3e" % kv for kv in sorted(k1m.items()))))
        ok1 = all(k1[k] == 0.0 for k in X0 if k not in k1m) and all(x == 0.0 for x in k1m.values()) and float(np.max(np.abs(Y[1] - A0))) == 0.0 and float(np.max(np.abs(Y[2] - E0))) == 0.0
        esiti.append(("K1. Theta^2 = x (e -x su psi: sigma_y sigma_y^* = -I) al bit", ok1))
        # ---------------------------------------------------------------- il controllo positivo
        t1 = time.time()
        a1 = corri(X0, A0, E0, 10)
        a2 = corri(X0, A0, E0, 10)
        ctrl = max(diff(a1, a2).values())
        print("### IL CONTROLLO POSITIVO (il determinismo): Q^10(x) due volte, la differenza massima %.3e (%.0f s per 10 tick)" % (ctrl, time.time() - t1))
        esiti.append(("il controllo positivo: Q^10(x) due volte uguale al bit", ctrl == 0.0))
        rng = np.random.default_rng(SEME)
        Xr = {k: a.copy() for k, a in X0.items()}
        Xr["psi_h"] = X0["psi_h"] * np.exp(2j * math.pi * rng.random(X0["psi_h"].shape))
        Ar = A0 + RUMORE * max(float(np.max(np.abs(A0))), 1e-12) * rng.standard_normal(A0.shape)
        Er = E0 + RUMORE * max(float(np.max(np.abs(E0))), 1e-12) * rng.standard_normal(E0.shape)
        # ---------------------------------------------------------------- il caso che deve fallire
        Yf = corri(*theta(*a1, cj=False), 10)
        dfail = max(diff(Yf, theta(X0, A0, E0, cj=False)).values())
        print("### DEVE FALLIRE: lo stesso operatore SENZA il coniugio, N = 10, il mattone: la differenza massima %.3e" % dfail)
        esiti.append(("DEVE FALLIRE: senza il coniugio la differenza NON sta sotto 1e-12", dfail >= 1e-12))
        # ---------------------------------------------------------------- la prova
        verd = []
        for nome, X, A, E in (("il mattone", X0, A0, E0), ("lo stato a caso (seme %d)" % SEME, Xr, Ar, Er)):
            for N in (10, 100):
                t1 = time.time()
                av = a1 if (N == 10 and nome == "il mattone") else corri(X, A, E, N)
                dd = diff(corri(*theta(*av), N), theta(X, A, E))
                m = max(dd.values())
                verd.append((nome, N, m, dd))
                print("### %s, N = %d: Q^N(Theta(Q^N(x))) contro Theta(x): il massimo %.3e (la soglia %.0e: %s) -- %s  (%.0f s)" % (
                    nome, N, m, SOGLIE[N], "SOTTO" if m < SOGLIE[N] else "### SOPRA", fmt(dd), time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-100s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    k_ok = all(ok for _n, ok in esiti)
    passa = all(m < SOGLIE[N] for _nm, N, m, _d in verd)
    print("=" * 130)
    print("### LA LETTURA (la previsione del guardiano, 815a7fba): %s" % (("PASSA: CPT ESATTA sul tick G+U senza bordo per N = 10 e N = 100 dai due stati" if passa else
          "### CADE: " + "; ".join("%s N %d %.3e" % (nm, N, m) for nm, N, m, _d in verd if m >= SOGLIE[N])) if k_ok else "### IL CASO NOTO O IL CONTROLLO NON PASSANO: LA PROVA NON SI LEGGE"))
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0 if (k_ok and passa) else 1


if __name__ == "__main__":
    sys.exit(main())
