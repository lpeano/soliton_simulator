# -*- coding: utf-8 -*-
r"""**IL TICK CON IL CAMPO CHI** *(il mandato di Luca `2026-11-21` `15:57`, con le decisioni delle `16:05` (fa1) e `16:39` (la massa); il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `5`, `9`)*. [[PROGETTO-MITOSI]]

**Un modulo NUOVO, fuori dal nucleo** *(come le regole della mitosi in `doc/referti_l2/`)*: **usa** `p6_bracci.tick_GU` *(la forma del tick: lo spinta del campo, il palindromo avvolto)*, `energia_pesata` *(`termini_di_h`, `d_peso_arco`, `pesi`)*, `tick_lapse.energia` *(per il confronto)*, **senza toccarli.**
**Il campo:** `chi`, `pi` per nodo; **la forza** `F = c2 (Delta chi) - m2 chi + kappa N (s Q - e0 rho) - c0`, `Delta = - L` *(`L = D D^T`, la `D` di Gauss)*, `N = exp(- kappa chi)`, `Q` la parentesi di `omega_psi` coi pesi di `cs = s N` *(calcolata su una COPIA dello stato: le cache dello stato non si muovono)*.
**Il tick** *(sez. `9.2`)*: `campo.spinta(1/2)`; `pi += F/2`; `chi += pi/2`; `cs = s N(chi)`; la fase (a) mezza `e^{+i e0 (N - 1)/2}`; il palindromo avvolto; la fase (a) mezza; `chi += pi/2`; `pi += F/2`; `campo.spinta(1/2)`; **il contatore** `Theta += pi (dtau cs_i - dtau cs_j)` *(la riga di `contatore.ritmo` del ramo `mitosi`, `i, j` = `inc.nodo[0::2]`, `[1::2]`)*.
**L'energia** `H = somma w_k H_k + somma w_a H_a - e0 somma (N - 1) rho + K + V + H_chi`; `H_chi = 1/2 somma pi^2 + 1/2 c2 somma_archi (chi_i - chi_j)^2 + 1/2 m2 somma chi^2 + c0 somma chi`.
**I parametri si CALCOLANO** *(`parametri`)*: `m0` = la media di `u = s Q - e0 rho` allo stato di partenza; `kappa` dal profilo statico con la massa sullo stato di C2 a `k 3000` *(`kappa^2 psi_m,c = - ln(1 - a)`, `a = 1 - N(rho)` al centro)*; `c0 = kappa m0`.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

C_CHI = 0.5                    # ### D-CHI-VELOCITA' (Luca 15:57)
PORTATA = 100.0                # ### la portata 1/m (Luca 16:39): UN NUMERO, la scelta di Luca (A1)
F_C2_3000 = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "C2", "stato_03000.npz")
CHIAVI_CHI = ("chi", "pi", "theta_a")


class Parametri(object):
    def __init__(self, kappa, c0, s, e0, c2=C_CHI ** 2, m2=(1.0 / PORTATA) ** 2):
        self.kappa, self.c0, self.s, self.e0, self.c2, self.m2 = float(kappa), float(c0), float(s), float(e0), float(c2), float(m2)

    def __repr__(self):
        return "kappa %.10e, c0 %+.10e, s %.12f, e0 %.6e, c2 %.4f, m2 %.1e" % (self.kappa, self.c0, self.s, self.e0, self.c2, self.m2)


class Laplaciano(object):
    """### `L = D D^T` sul grafo del motore *(la `D` della divergenza di Gauss: `D[jj, a] = +1`, `D[ii, a] = -1`)*; il solutore di `(c2 L + m2)`."""

    def __init__(self, mot):
        import scipy.sparse as sp
        nodo = np.asarray(mot.inc.nodo, dtype=np.int64)
        self.ii, self.jj, n = nodo[0::2], nodo[1::2], mot.inc.n
        m = len(self.ii)
        a = np.arange(m)
        D = sp.csr_matrix((np.concatenate([np.ones(m), -np.ones(m)]), (np.concatenate([self.jj, self.ii]), np.concatenate([a, a]))), shape=(n, m))
        self.L = (D @ D.T).tocsr()
        self.n = n
        self._solv = None

    def delta(self, chi):
        return -(self.L @ chi)

    def statico(self, P, sorgente):
        """### `(c2 L + m2)^{-1} sorgente`."""
        import scipy.sparse as sp
        import scipy.sparse.linalg as spl
        if self._solv is None:
            self._solv = spl.factorized((P.c2 * self.L + P.m2 * sp.identity(self.n, format="csr")).tocsc())
        return self._solv(np.asarray(sorgente, dtype=float))


def rho_di(mot, st):
    r = np.zeros(mot.inc.n)
    np.add.at(r, mot.inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    return r


def Q_di(mot, st, par, cs):
    """### `Q_k = H_k + somma_{h in k} dw_h H_a(h)` coi pesi di `cs`, su una COPIA dello stato."""
    import energia_pesata as EP
    copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
    salvo, lc = mot.cs, getattr(mot, "lambda_c", None)
    mot.cs = np.asarray(cs, dtype=float)
    mot.lambda_c = None
    try:
        pn, pa = EP.termini_di_h(mot, copia, par)
        dw = EP.d_peso_arco(mot)
        arco = np.zeros(mot.inc.n)
        np.add.at(arco, mot.inc.nodo, dw * np.repeat(pa, 2))
        return pn + arco
    finally:
        mot.cs, mot.lambda_c = salvo, lc


def u_di(mot, st, par, s, e0):
    """### `u = s Q - e0 rho` a `chi = 0` *(`cs = s` uniforme)*: la sorgente senza `kappa`."""
    return s * Q_di(mot, st, par, np.full(mot.inc.n, float(s))) - e0 * rho_di(mot, st)


def forza(mot, st, par, P, Lp, chi):
    N = np.exp(-P.kappa * chi)
    cs = P.s * N
    Q = Q_di(mot, st, par, cs)
    rho = rho_di(mot, st)
    return P.c2 * Lp.delta(chi) - P.m2 * chi + P.kappa * N * (P.s * Q - P.e0 * rho) - P.c0


def fase_a(mot, st, e0, N):
    """### la fase della forma (a) con `N(chi)` *(fa1)*: `e^{+i e0 (N - 1)/2}` per nodo *(le righe di `tick_lapse.fase_a` col termine in `N'` caduto)*."""
    g = N - 1.0
    st["psi_h"][...] = st["psi_h"] * np.exp(0.5j * float(e0) * g)[mot.inc.nodo][:, None]


def tick_chi(z, campo, P, Lp, X):
    """### UN tick con `chi`. `X` = `{"chi", "pi", "theta_a"}` *(aggiornati sul posto)*."""
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    mot, st, par = z["mot"], z["st"], z["par"]
    dt = float(mot.dtau[0])
    assert np.all(mot.dtau == mot.dtau[0]), "dtau non uniforme: il salto di rana di chi vuole un dtau solo"
    campo.spinta(0.5)
    X["pi"] += (0.5 * dt) * forza(mot, st, par, P, Lp, X["chi"])
    X["chi"] += (0.5 * dt) * X["pi"]
    N = np.exp(-P.kappa * X["chi"])
    mot.cs = P.s * N
    mot.lambda_c = None
    fase_a(mot, st, P.e0, N)
    with UO.avvolto(mot, campo, True):
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    fase_a(mot, st, P.e0, N)
    d = np.asarray(mot.dtau, dtype=float) * np.asarray(mot.cs, dtype=float)
    nodo = np.asarray(mot.inc.nodo)
    X["theta_a"] += math.pi * (d[nodo[0::2]] - d[nodo[1::2]])
    X["chi"] += (0.5 * dt) * X["pi"]
    X["pi"] += (0.5 * dt) * forza(mot, st, par, P, Lp, X["chi"])
    campo.spinta(0.5)


def energia_chi(mot, st, par, P, Lp, X, campo):
    """### `(H totale, H_chi)` coi pesi di `cs = s N(chi)`."""
    import energia_pesata as EP
    chi, pi = X["chi"], X["pi"]
    N = np.exp(-P.kappa * chi)
    copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
    salvo, lc = mot.cs, getattr(mot, "lambda_c", None)
    mot.cs = P.s * N
    mot.lambda_c = None
    try:
        pn, pa = EP.termini_di_h(mot, copia, par)
        wn, wa = EP.pesi(mot)
        G = float(np.sum(wn * pn)) + float(np.sum(wa * pa))
    finally:
        mot.cs, mot.lambda_c = salvo, lc
    rho = rho_di(mot, st)
    Fa = -P.e0 * float(np.sum((N - 1.0) * rho))
    dch = chi[Lp.ii] - chi[Lp.jj]
    Hc = 0.5 * float(np.sum(pi * pi)) + 0.5 * P.c2 * float(np.sum(dch * dch)) + 0.5 * P.m2 * float(np.sum(chi * chi)) + P.c0 * float(np.sum(chi))
    return G + Fa + campo.K() + campo.V() + Hc, Hc


def energia_oggi(mot, st, par, s, legge, e0, campo):
    """### l'energia del tick di oggi *(`tick_lapse.energia` + la forma (a) con `N(rho)` + il campo)*: lo stesso codice di `energia_chi` per i pesi."""
    from solitone import tick_lapse as TL
    rho = rho_di(mot, st)
    N = TL.N_di(rho, legge)
    return TL.energia(mot, st, par, s, legge) - e0 * float(np.sum((N - 1.0) * rho)) + campo.K() + campo.V()


def parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, partenza="C2"):
    """### `(P, m0, a)`: `m0` dallo stato di partenza *(`"C2"`: il `k 0` di C2, `prepara` senza bordo; `"vuoto"`: `vuoto_fresco`)*, `kappa` da C2 `k 3000`, `c0 = kappa m0`. ### Lascia `Z` sullo stato di C2 a `k 3000`."""
    import hashlib
    mot = Z["mot"]
    if partenza == "C2":
        CSB.prepara(Z, 186, False, rho_c, e, t0)
    else:
        PS.MT.vuoto_fresco(Z, t0)
    m0 = float(u_di(mot, Z["st"], Z["par"], s, e0).mean())
    with open(F_C2_3000, "rb") as fh:
        h = hashlib.sha1(fh.read()).hexdigest()
    assert open(F_C2_3000 + ".sha1", encoding="utf-8").read().split()[0] == h, "lo sha1 di C2 k 3000 NON coincide"
    with np.load(F_C2_3000) as d:
        Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
        meta = json.loads(str(d["meta"]))
    from solitone import toro as TO
    c = [float(x) for x in meta["centro"]]
    r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"]).T[:2])
    c0n = int(np.argmin(r))
    m0_c2 = m0 if partenza == "C2" else None
    if partenza != "C2":
        # ### kappa si tara sempre col m0 del k 0 di C2 (la regola della 16:39); qui serve anche quello
        Zst = {k: v.copy() for k, v in Z["st"].items() if isinstance(v, np.ndarray)}
        CSB.prepara(Z, 186, False, rho_c, e, t0)
        m0_c2 = float(u_di(mot, Z["st"], Z["par"], s, e0).mean())
        Z["metti"](Zst)
    u3 = u_di(mot, Z["st"], Z["par"], s, e0)
    Pt = Parametri(1.0, 0.0, s, e0)
    pm = Lp.statico(Pt, u3 - m0_c2)
    rho = rho_di(mot, Z["st"])
    a = 1.0 - 1.0 / (1.0 + rho[c0n] / rho_c)
    assert pm[c0n] > 0.0, "psi_m al centro NON positivo: kappa non esiste (FERMO)"
    kappa = math.sqrt(-math.log(1.0 - a) / pm[c0n])
    return Parametri(kappa, kappa * m0, s, e0), m0, a, kappa * m0_c2


def chi_statico(mot, st, par, P, Lp, m0):
    """### il profilo statico `chi = kappa (c2 L + m2)^{-1} (u - m0)` sullo stato `st`."""
    return P.kappa * Lp.statico(P, u_di(mot, st, par, P.s, P.e0) - m0)


def nuovo_X(n, m, chi=None):
    return {"chi": (np.zeros(n) if chi is None else np.array(chi, dtype=float)), "pi": np.zeros(n), "theta_a": np.zeros(m)}


def copia_X(X):
    return {k: v.copy() for k, v in X.items()}
