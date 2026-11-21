# -*- coding: utf-8 -*-
r"""**IL LAPSE DALLA `U`, COI SEGNI DELLE PROVE G+U, SUGLI STATI DEL TRONCO** *(la domanda di misura di Luca `2026-11-21` `14:47`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `20`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_lapse_U.py --base E:\soliton_simulator\controllo\mitosi_rami > doc/referti_l2/mitosi_lapse_U.txt

**Solo lettura** *(le corse non si toccano)*. **Gli stati:** `k 3000` *(C2, `E:/soliton_simulator/controllo/C2/stato_03000.npz`)*, `k 15000` e `k 29000` del tronco; **il centro** del tronco.
**La convenzione** *(20.2)*: `div_i` = gli `E` entranti meno gli uscenti; `div E = e (rho - media)`; `E = D^T phi` *(`E_a = phi(jj) - phi(ii)`)*; **`Phi` = la parte gradiente di `E`: `L Phi = D E`** *(il nodo `0` fissato, la media tolta: il solutore di `gauss_riuso`)*.
**`N(rho) = 1 / (1 + rho / rho_c)`** *(`tick_lapse.N_di`)*; **`s = cs_prec / N(rho)`** misurato *(il controllo della legge: lo stesso su ogni nodo)*; **`N_U = 1 - kappa (Phi - Phi_ref)`**, `Phi_ref` il minimo sul toro, `kappa` dall'uguaglianza al centro *(il nodo piu' vicino al centro)*.
**Il ritmo:** `s pi |N_i - N_j|` *(per `N(rho)`: `pi |cs_i - cs_j|` da `cs_prec`)*; **il primo arco a `2 pi` da `Theta = 0`; gli archi oltre `r 23.81` entro `1e5` tick.** **Il caso noto** *(20.4)*: `rho` uniforme e `E = 0` -> `Phi = 0` e `N_U = 1` AL BIT.
"""
import argparse
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(_QUI, "..", "..", "csv"), os.path.join(_QUI, "..", "..", "csv", "solitone"), _QUI):
    if p not in sys.path:
        sys.path.insert(0, p)
import mitosi_anelli as AN                   # ### usato, non riscritto: toro, polari, mezzo, leggi
import mitosi_ritmo_contatore as RT          # ### usato, non riscritto: sha1

N0 = AN.N0
F_C2 = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "C2", "stato_03000.npz")
CONFINE, ORIZZONTE, R_MAX = 23.81, 1e5, 80


class Solutore(object):
    """### `D` la divergenza della corsa sul toro, `L = D D^T`, la fattorizzazione di `L[1:, 1:]` *(come `gauss_riuso`)*."""

    def __init__(self, ii, jj):
        import scipy.sparse as sp
        import scipy.sparse.linalg as spl
        m = len(ii)
        a = np.arange(m)
        self.D = sp.csr_matrix((np.concatenate([np.ones(m), -np.ones(m)]), (np.concatenate([jj, ii]), np.concatenate([a, a]))), shape=(N0, m))
        L = (self.D @ self.D.T).tocsc()
        self.risolvi = spl.factorized(L[1:, 1:])

    def phi(self, b):
        p = np.zeros(N0)
        p[1:] = self.risolvi(np.asarray(b, dtype=float)[1:])
        p -= p.mean()
        return p


def leggi(f, ii, jj):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == RT.sha1(f), "lo sha1 di %s NON coincide" % f
    import json
    with np.load(f) as d:
        psi_h, E, cs, meta = d["psi_h"], d["campo_E"].copy(), d["cs_prec"].copy(), json.loads(str(d["meta"]))
    nodo = np.empty(2 * len(ii), dtype=np.int64)
    nodo[0::2], nodo[1::2] = ii, jj
    rho = np.bincount(nodo, weights=np.sum(np.abs(psi_h) ** 2, axis=1), minlength=N0)
    return int(meta["k"]), rho, E, cs


def per_anello(r, y):
    out = np.full(R_MAX + 1, np.nan)
    for R in range(R_MAX + 1):
        w = (r >= R - 0.5) & (r < R + 0.5)
        if w.any():
            out[R] = float(y[w].mean())
    return out


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import mattone as MT
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    x = ap.parse_args(argv)
    dT = os.path.join(x.base, "TRONCO")
    stati = [("C2 k 3000", F_C2), ("tronco k 15000", os.path.join(dT, "stato_15000.npz")), ("tronco k 29000", os.path.join(dT, "stato_29000.npz"))]
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    ii, jj, m1, m2 = AN.toro()
    _, _, _, _, _, _, centro = AN.leggi(stati[-1][1])
    r, _ = AN.polari(m1, m2, centro)
    c0 = int(np.argmin(r))
    x1, x2 = AN.mezzo(m1, m2, ii, jj)
    ra, _ = AN.polari(x1, x2, centro)
    S = Solutore(ii, jj)
    print("=" * 150)
    print("IL LAPSE DALLA U, COI SEGNI DELLE PROVE G+U (Luca 2026-11-21 14:47; la carta sez. 20): solo lettura")
    print("=" * 150)
    print("### rho_c %.10e (mattone.rho_c_assoluto), e %.6e (E_DECISO); il centro %.4f %.4f; il nodo del centro %d (r %.4f); %d archi" % (rho_c, e, centro[0], centro[1], c0, r[c0], len(ii)))
    # ------------------------------------------------------------------ IL CASO NOTO (20.4): per primo
    rho_u = np.full(N0, 1.2345)
    p_u = S.phi(e * (rho_u - rho_u.mean()))
    p_e = S.phi(S.D @ np.zeros(len(ii)))
    nu_u = 1.0 - 7.0 * (p_u - p_u.min())
    nu_e = 1.0 - 7.0 * (p_e - p_e.min())
    noto = bool(np.all(p_u == 0.0) and np.all(p_e == 0.0) and np.all(nu_u == 1.0) and np.all(nu_e == 1.0))
    print("### IL CASO NOTO (il vuoto puro: rho uniforme, e E = 0; kappa qualunque, 7): Phi max |%.3e| e |%.3e|; N_U == 1 su ogni nodo: %s -> %s" % (
        np.abs(p_u).max(), np.abs(p_e).max(), bool(np.all(nu_u == 1.0) and np.all(nu_e == 1.0)), "AL BIT" if noto else "NON AL BIT: FERMO"))
    if not noto:
        return 1
    ok = True
    for nome, f in stati:
        k, rho, E, cs = leggi(f, ii, jj)
        assert len(E) == len(ii), "il campo E non ha gli archi del toro"
        dE = S.D @ E
        res = float(np.max(np.abs(dE - e * (rho - rho.mean())))) / (e * float(rho.max()))
        Phi = S.phi(dE)
        Nr = 1.0 / (1.0 + rho / rho_c)
        s_n = cs / Nr
        s = float(np.median(s_n))
        pref = float(Phi.min())
        kap = (1.0 - Nr[c0]) / (Phi[c0] - pref)
        NU = 1.0 - kap * (Phi - pref)
        print("-" * 150)
        print("### %s (k %d): il residuo di Gauss (D E contro e (rho - media), relativo a e max rho) %.3e; Phi al centro %+.6e, il minimo %+.6e (al nodo %d, r %.2f), all'anello 80 %+.6e" % (
            nome, k, res, Phi[c0], pref, int(np.argmin(Phi)), r[int(np.argmin(Phi))], per_anello(r, Phi)[80]))
        print("    il segno: Phi al centro %s Phi_ref -> kappa %+.6e (%s: N_U < 1 sul mattone); s = cs / N(rho): la mediana %.12f, min %.12f, max %.12f (lo scarto relativo %.2e)" % (
            ">" if Phi[c0] > pref else "<=", kap, "positivo" if kap > 0 else "NEGATIVO", s, s_n.min(), s_n.max(), (s_n.max() - s_n.min()) / s))
        ok &= res < 1e-6 and kap > 0
        rU = s * math.pi * np.abs(NU[ii] - NU[jj])
        rR = math.pi * np.abs(cs[ii] - cs[jj])
        PU, PR, PP = per_anello(r, 1.0 - NU), per_anello(r, 1.0 - Nr), per_anello(r, Phi - pref)
        AU, AR = per_anello(ra, rU), per_anello(ra, rR)
        print("    il profilo per anello (r euclideo; il ritmo degli archi col punto medio nell'anello, 1e-4 per tick):")
        print("      r    Phi - Phi_ref      1 - N(rho)       1 - N_U      ritmo N(rho)   ritmo N_U")
        for R in list(range(0, 31, 2)) + list(range(35, R_MAX + 1, 5)):
            print("    %3d   %13.6e   %13.6e   %13.6e    %10.4f   %10.4f" % (R, PP[R], PR[R], PU[R], AR[R] * 1e4, AU[R] * 1e4))
        PU[0], PR[0] = 1.0 - NU[c0], 1.0 - Nr[c0]          # ### «il centro» = il nodo del centro (l'anello 0, r < 0.5, puo' essere vuoto)
        for lab, rit, P in (("N(rho)", rR, PR), ("N_U", rU, PU)):
            a = int(np.argmax(rit))
            T = 2.0 * math.pi / rit[a]
            with np.errstate(divide="ignore"):
                Ta = 2.0 * math.pi / rit
            fuori = int(np.sum((ra > CONFINE) & (Ta <= ORIZZONTE)))
            print("    ### %-6s: il ritmo massimo %.4e per tick all'arco %d (r %.2f; l'anello col ritmo medio massimo %d); il primo a 2 pi da Theta = 0 a %.0f tick; oltre r %.2f entro %.0e tick: %d archi; 1 - N all'anello 60 sul centro %.3e" % (
                lab, rit[a], a, ra[a], int(np.nanargmax(per_anello(ra, rit))), T, CONFINE, ORIZZONTE, fuori, P[60] / P[0] if P[0] else math.nan))
        aU = int(np.argmax(rU))
        TU, TR = 2.0 * math.pi / rU.max(), 2.0 * math.pi / rR.max()
        print("    ### LE PREVISIONI DEL GUARDIANO su questo stato: P-U1 (1 - N_U all'anello 60 sopra il 10%% del centro): %.4f -> %s; P-U2 (il ritmo massimo con N_U oltre 22): r %.2f -> %s; P-U3 (il primo quanto con N_U piu' tardi che con N(rho), oltre 5e4): %.0f contro %.0f -> %s" % (
            PU[60] / PU[0], "VERA" if PU[60] / PU[0] > 0.1 else "FALSA", ra[aU], "VERA" if ra[aU] > 22 else "FALSA", TU, TR, "VERA" if TU > TR and TU > 5e4 else "FALSA"))
    print("-" * 150)
    print("### I CONTROLLI (il residuo di Gauss sotto 1e-6 a ogni stato; kappa positivo): %s" % ("PASSANO" if ok else "NON PASSANO: FERMO"))
    print("=" * 150)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
