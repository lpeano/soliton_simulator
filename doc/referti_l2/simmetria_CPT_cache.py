# -*- coding: utf-8 -*-
r"""**LA PROVA CPT SENZA BORDO CON LE CACHE RICALCOLATE** *(Luca `2026-11-17` `14:27`, parte 1; la carta `doc/TASK_HISTORY/2026-11-17_flusso_uscente.md`; DOPO `simmetria_CPT.txt`, `45568f37`)*.

    E:\python\py3132\python.exe doc/referti_l2/simmetria_CPT_cache.py > doc/referti_l2/simmetria_CPT_cache.txt     (PYTHONNOUSERSITE=1, 1 filo, numba spento)

**La stessa prova di `simmetria_CPT.py`** *(l'operatore, il tick `p6_bracci.tick_GU` senza il bordo, `Q^N(Theta(Q^N(x)))` contro `Theta(x)`, `N = 10` e `100`, il mattone e lo stato a caso seme `11`)*, **ma sui due lati le tre CACHE si RICALCOLANO dallo stato finale col codice del nucleo** *(`motore.elicita` -> `h_int`, `motore.densita_materia` -> `rho`, `motore.densita_vuoto` -> `Lambda`)* **prima del confronto.**
**Accanto, per `h_int`:** il ricalcolato del lato `Theta(x)` contro `h_int(x)` PERMUTATO e contro `-h_int(x)` permutato *(la carta: `h_int = s . n` puo' cambiare segno)*.
**LA LETTURA** *(la carta, sez. `3`)*: **le tre cache ricalcolate coincidono entro `1e-12` relativo per `N = 10` e entro `1e-10` per `N = 100`, dai due stati** *(le soglie di `815a7fba`)*; **e le chiavi della dinamica come in `45568f37`.**
"""
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
CACHE = ("h_int", "rho", "Lambda")


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
    print("LA PROVA CPT SENZA BORDO CON LE CACHE RICALCOLATE (Luca 2026-11-17 14:27, parte 1); sys.executable %s; le soglie %s" % (sys.executable, SOGLIE))
    print("=" * 130)
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
        qi = np.rint((P @ (-np.eye(2)).T) @ np.linalg.inv(np.column_stack([A1v, A2v])).T)
        sig = ((qi[:, 0].astype(int) + p0[0]) % L) * L + (qi[:, 1].astype(int) + p0[1]) % L
        assert np.array_equal(np.sort(sig), v) and np.array_equal(sig[sig], v)
        ap, rov = SPC.mappa_archi(ii, jj, sig)
        hp = np.empty(2 * len(ap), dtype=int)
        hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
        hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
        assert np.array_equal(nodo[hp], sig[nodo])
        cap, crov = SPC.mappa_archi(ci, cj, sig)
        verso = np.where(crov, -1.0, 1.0)
        print("### l'operatore di simmetria_CPT.py: l'inversione attorno a p0 = %s; sigma_y e il coniugio su psi; phi -> -conj(phi); A -> -(verso) A; E -> +(verso) E" % (p0,))

        def theta(X, A, E):
            Y = {}
            for k, a in X.items():
                b = np.conj(a) if np.iscomplexobj(a) else a
                if k in ("psi_h", "psi"):
                    b = b @ SY.T
                elif k == "phi_h":
                    b = -b
                y = np.empty_like(b)
                if a.shape[0] == n:
                    y[sig] = b
                else:
                    y[hp] = b
                Y[k] = y
            Ar, Er = np.empty_like(A), np.empty_like(E)
            Ar[cap] = -verso * A
            Er[cap] = verso * E
            return Y, Ar, Er

        def ricalcola(X):
            """### Le tre cache dallo stato `X` col codice del nucleo (su una copia)."""
            st = dict(Z["st"])
            for k in X:
                st[k] = X[k].copy()
            st["h_int"] = np.zeros(n)
            st["rho"] = np.zeros(n)
            st["Lambda"] = np.zeros(n)
            out = {"h_int": np.array(mot.elicita(st), copy=True), "rho": np.array(mot.densita_materia(st), copy=True), "Lambda": np.array(mot.densita_vuoto(st), copy=True)}
            return out

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

        def rel(a, b):
            sc = float(np.max(np.abs(b)))
            return float(np.max(np.abs(a - b))) / sc if sc > 0 else float(np.max(np.abs(a)))

        rng = np.random.default_rng(SEME)
        Xr = {k: a.copy() for k, a in X0.items()}
        Xr["psi_h"] = X0["psi_h"] * np.exp(2j * math.pi * rng.random(X0["psi_h"].shape))
        Ar = A0 + RUMORE * max(float(np.max(np.abs(A0))), 1e-12) * rng.standard_normal(A0.shape)
        Er = E0 + RUMORE * max(float(np.max(np.abs(E0))), 1e-12) * rng.standard_normal(E0.shape)
        verd = []
        for nome, X, A, E in (("il mattone", X0, A0, E0), ("lo stato a caso (seme %d)" % SEME, Xr, Ar, Er)):
            # h_int col suo segno: il ricalcolato su Theta(x) contro h_int(x) permutato (+ e -)
            Tx = theta(X, A, E)
            hx = ricalcola(X)["h_int"]
            hT = ricalcola(Tx[0])["h_int"]
            hperm = np.empty_like(hx)
            hperm[sig] = hx
            print("### %s: h_int ricalcolato su Theta(x) contro h_int(x) permutato: %.3e; contro MENO h_int(x) permutato: %.3e" % (nome, rel(hT, hperm), rel(hT, -hperm)))
            for N in (10, 100):
                t1 = time.time()
                lato1 = corri(*theta(*corri(X, A, E, N)), N)
                c1 = ricalcola(lato1[0])
                c2 = ricalcola(Tx[0])
                dd = {k: rel(c1[k], c2[k]) for k in CACHE}
                for k in ("psi_h", "phi_h"):
                    dd[k] = rel(lato1[0][k], Tx[0][k])
                dd["A"] = rel(lato1[1], Tx[1])
                dd["E"] = rel(lato1[2], Tx[2])
                m = max(dd.values())
                verd.append((nome, N, m))
                print("### %s, N = %d: il massimo %.3e (la soglia %.0e: %s) -- %s  (%.0f s)" % (nome, N, m, SOGLIE[N], "SOTTO" if m < SOGLIE[N] else "### SOPRA",
                      "  ".join("%s %.3e" % (k, dd[k]) for k in ("h_int", "rho", "Lambda", "psi_h", "phi_h", "A", "E")), time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    passa = all(m < SOGLIE[N] for _nm, N, m in verd)
    print("=" * 130)
    print("### LA LETTURA (la carta, sez. 3): %s" % ("PASSA: le cache ricalcolate e la dinamica coincidono entro le soglie, N = 10 e 100, dai due stati" if passa else
          "### NON PASSA: " + "; ".join("%s N %d %.3e" % (nm, N, m) for nm, N, m in verd if m >= SOGLIE[N])))
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(main())
