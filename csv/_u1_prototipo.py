# -*- coding: utf-8 -*-
r"""**IL PROTOTIPO DEL CAMPO `U(1)` SUI TRIANGOLI, IN MEMORIA: LA CATENA DEI SIGILLI E LA VELOCITA' DELLA LUCE** *([[PROGETTO-U1]], [[LUCE-VINCOLO-LAMPI-GAMMA]],
[[LORENTZ-MATERIA-INTERFERENZA]], [[DECISIONE-SOLO-TRIANGOLI]])*.

> ### ⛔ **Il task history e' `2026-10-24_u1_prototipo.md`** *(`7757a137`: il metodo, le previsioni, i criteri e le soglie, fissati prima)*. ### **`leggi.yaml`, l'impronta e il nucleo intatti.**
> ### **IL CAMPO VIVE FUORI DA `stato.py`** *(la classe `Campo`: `A`, `E` per arco)* ### **e il passo di oggi si AVVOLGE in memoria** *(`mot.operatori` e `mot.geo.U`, rimessi a fine corsa)*: ### **nessun file del nucleo cambia.**
> ### **Importati, non copiati:** `_triangoli` *(`scena_toro`, `camminata`, `toro_spostamenti`, `TRIANGOLI`)*, `_triangoli_forza` *(`coppia_K`, `conv`, `byte_attr`)*, `_zero_simmetrico` *(attraverso `conv`)*,
> `_triangoli_bassa_energia` *(`J`)*, `_triangoli_fattore` *(la convenzione dei blocchi in spazio reale, qui per il campo)*, `_universalita_massa.blob`.

## ⭐ IL CAMPO *(`doc/PROGETTO_U1.md` sezioni `4`-`6`; la forma del tempo dell'arco: il task history, sezione `1.3`)*

| | la forma |
|---|---|
| le variabili | `A_a` reale, `E_a` il coniugato; `U_a = e^{i e A_a} I_2` nello spostamento della materia |
| le placchette | «su» `A(v,0) + A(v+a1,1) - A(v,2)`, «giu'» `A(v,2) - A(v+a2,0) - A(v,1)` |
| l'energia per tick | `H_F = somma_a s_a^2 (l/l*) E_a^2/2 + V`; `V = somma (1 - cos eB)/(e^2 A_p)` *(compatto)*, `somma B^2/(2 A_p)` *(non compatto)* |
| il tick | `spinta(1/2)` · la camminata *(la sorgente `E <- E - e J` nello spostamento; `deriva(1/2) deriva(1/2)` dopo il primo `CAMM-SPOSTAMENTO-VUOTO`)* · `spinta(1/2)` |

Gira con:  python csv/_u1_prototipo.py > doc/referti_l2/u1_prototipo.txt
"""
import contextlib
import io
import json
import math
import os
import sys
import time
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

CONV = ("simm", "oggi")
S_GRIGLIA = (0.05, 0.1, 0.3)
S_COURANT = 0.45                # ### la prova DICHIARATA: deve essere instabile
S_STABILE = 0.3
FORME = ("compatto", "noncompatto")
E_PROVA = (0.1, math.sqrt(4.0 * math.pi / 137.0))  # ### due valori di prova: l'accoppiamento debole; il secondo e' alpha = 1/137 (un riferimento, non una taratura)
L_SU_LS = math.sqrt(3.0)        # ### l/l* del triangolo: l = 1, l* = 1/sqrt3
AREA = math.sqrt(3.0) / 4.0     # ### A_p del triangolo di lato 1
L_MAT = 24
W_MAT = 3.0
N_A1 = 50
N_B = 100
N_C = 1000
N_D = 500
SEME_CHI = 11
TOLL_REL = 1e-12
TOLL_ROTTA = 1e-9
L_BLOCCHI = 8
SUPPORTO = 2                    # ### il tick del campo arriva a +-2 celle: oltre, i blocchi devono essere ZERO
L_COURANT = 48
K_PICCOLO = 1e-3
H_K = 1e-4
DIREZIONI_V = 12
GAUGE_VICINO = 1e-6
INSTABILE = 1e-6
TOLL_SERV = 1e-12
L_PACC = 96
N_K0 = 4                        # ### k0 = 2 pi 4/96 lungo a1
W_PACC = 12.0
TRATTO = 30.0
TOLL_PACC = 0.01
TOLL_UNO = 0.01
LG = (192, 48)
S0_G = 0.2
ETA_G = 0.5
N1_G = 7                        # ### il k lungo la normale al gradiente piu' vicino a 2 pi/24 sulla griglia: t1 = 2 pi 7/192
N_DEF = (-4, 2)                 # ### il k lungo a2 per la deflessione: t1 = 2 pi (-4)/192, t2 = 2 pi 2/48 (lunghezza d'onda 24)
W_G = 12.0
T_G = 800
T_DEF = 400
FIN_G = 10
TOLL_G = 0.02
JSONL = os.path.join(RADICE, "doc", "referti_l2", "u1_prototipo.jsonl")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-96s %s   %s" % (che[:96], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def f_(x, fm="%.3e"):
    return "--" if x is None else fm % x


def rel(a, b, scala=None):
    """### `max|a - b| / scala` *(la scala: `max|a|`, o quella data)*."""
    d = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
    sc = float(np.max(np.abs(a))) if scala is None else float(scala)
    return d / sc if sc > 0 else d


# =====================================================================================
#   IL CAMPO
# =====================================================================================
class Campo(object):
    """### `A`, `E` per arco, fuori da `stato.py`. ### **`ii`, `jj` gli archi di `_triangoli.toro_spostamenti(lati, TRIANGOLI)`** *(l'arco `3 v + a`)*; ### **`s_a` il tempo dell'arco.**"""

    def __init__(self, ii, jj, lati, e, forma, s_a):
        L1, L2 = int(lati[0]), int(lati[1])
        n = L1 * L2
        m = 3 * n
        assert len(ii) == m and len(jj) == m, "gli archi non sono 3 per nodo"
        self.n, self.m, self.lati, self.e, self.forma = n, m, (L1, L2), float(e), forma
        assert forma in FORME
        v = np.arange(n)
        m1, m2 = v // L2, v % L2

        def nb(d1, d2):
            return ((m1 + d1) % L1) * L2 + (m2 + d2) % L2
        assert np.array_equal(jj[0::3], nb(1, 0)) and np.array_equal(jj[1::3], nb(0, 1)) and np.array_equal(jj[2::3], nb(1, 1)), "gli archi non sono a1, a2, a1+a2"
        assert np.array_equal(ii, np.repeat(v, 3)), "l'arco 3v+a non parte da v"
        su = np.stack([3 * v, 3 * nb(1, 0) + 1, 3 * v + 2], axis=1)
        giu = np.stack([3 * v + 2, 3 * nb(0, 1), 3 * v + 1], axis=1)
        self.P = np.concatenate([su, giu])
        self.S = np.concatenate([np.tile([1.0, 1.0, -1.0], (n, 1)), np.tile([1.0, -1.0, -1.0], (n, 1))])
        # ### ogni arco in DUE placchette: (placchetta, segno), nell'ordine delle placchette
        coppie = [[] for _ in range(m)]
        for p in range(2 * n):
            for c in range(3):
                coppie[self.P[p, c]].append((p, self.S[p, c]))
        assert all(len(x) == 2 for x in coppie), "un arco non sta in due placchette"
        self.ap = np.array([[x[0][0], x[1][0]] for x in coppie])
        self.asg = np.array([[x[0][1], x[1][1]] for x in coppie])
        self.ii, self.jj = np.asarray(ii), np.asarray(jj)
        ordine = np.argsort(self.jj, kind="stable")
        self.ingressi = ordine.reshape(n, 3)
        assert np.all(self.jj[self.ingressi] == v[:, None])
        self.s_a = np.asarray(s_a, dtype=float).copy()
        self.w = self.s_a ** 2 * L_SU_LS
        self.A = np.zeros(m)
        self.E = np.zeros(m)

    def B(self):
        A, P, S = self.A, self.P, self.S
        return A[P[:, 0]] * S[:, 0] + A[P[:, 1]] * S[:, 1] + A[P[:, 2]] * S[:, 2]

    def g(self, B):
        if self.forma == "compatto":
            return np.sin(self.e * B) / (self.e * AREA)
        return B / AREA

    def forza(self):
        """### `dV/dA`: il rotore trasposto di `g(B)`."""
        g = self.g(self.B())
        return self.asg[:, 0] * g[self.ap[:, 0]] + self.asg[:, 1] * g[self.ap[:, 1]]

    def spinta(self, f):
        self.E -= f * self.forza()

    def deriva(self, f):
        self.A += f * self.w * self.E

    def V(self):
        B = self.B()
        if self.forma == "compatto":
            return float(np.sum((1.0 - np.cos(self.e * B)) / (self.e * self.e * AREA)))
        return float(np.sum(B * B / (2.0 * AREA)))

    def K(self):
        return float(np.sum(self.w * self.E * self.E / 2.0))

    def div(self, E=None):
        """### `D_i = somma_{entra in i} E - somma_{esce da i} E`."""
        E = self.E if E is None else E
        return E[self.ingressi].sum(axis=1) - E.reshape(self.n, 3).sum(axis=1)

    def u(self):
        return np.exp(1j * (self.e * self.A))

    def matrice_div(self):
        D = np.zeros((self.n, self.m))
        D[self.jj, np.arange(self.m)] += 1.0
        D[self.ii, np.arange(self.m)] -= 1.0
        return D

    def matrice_rot(self):
        C = np.zeros((2 * self.n, self.m))
        for c in range(3):
            np.add.at(C, (np.arange(2 * self.n), self.P[:, c]), self.S[:, c])
        return C


def scrivi_U(mot, campo):
    u = campo.u()
    mot.geo.U[:, 0, 0] = u
    mot.geo.U[:, 1, 1] = u


@contextlib.contextmanager
def avvolto(mot, campo, sorgente):
    """### **Il passo di oggi AVVOLTO:** ### **lo spostamento della materia porta la sorgente** *(`J_a = |v0'|^2 - |v0|^2`, `E <- E - e J`)*, ### **e dopo il PRIMO
    `CAMM-SPOSTAMENTO-VUOTO` del tick la deriva `(1/2)(1/2)` e `U` rifatta.** ### **`mot.operatori` rimesso all'uscita.**"""
    op = mot.operatori
    vero_sp, vero_sv = op["spostamento_trasporto"], op["spostamento_scalare"]
    conta = [0]
    m = campo.m

    def sp(st, par, fr):
        v = st["psi_h"].reshape(m, 2, 2)
        prima = np.sum(np.abs(v[:, 0, :]) ** 2, axis=1)
        out = vero_sp(st, par, fr)
        J = np.sum(np.abs(v[:, 0, :]) ** 2, axis=1) - prima
        if sorgente:
            campo.E -= campo.e * J
        return out

    def sv(st, par, fr):
        out = vero_sv(st, par, fr)
        conta[0] += 1
        if conta[0] % 2 == 1:
            campo.deriva(0.5)
            campo.deriva(0.5)
            scrivi_U(mot, campo)
        return out
    op["spostamento_trasporto"], op["spostamento_scalare"] = sp, sv
    try:
        yield
    finally:
        op["spostamento_trasporto"], op["spostamento_scalare"] = vero_sp, vero_sv


def tick(st, mot, par, campo):
    import _triangoli as T
    campo.spinta(0.5)
    T.camminata(st, mot, par)
    campo.spinta(0.5)


def tick_campo(campo):
    campo.spinta(0.5)
    campo.deriva(0.5)
    campo.deriva(0.5)
    campo.spinta(0.5)


# =====================================================================================
#   LA SCENA DELLA MATERIA
# =====================================================================================
_Q = {}


def u_K(s):
    import _triangoli as T
    import _triangoli_forza as TF
    if s not in _Q:
        _Q[s] = TF.coppia_K(T.EPS_MONETA, s)[0]["Q"][:, 0]
    return _Q[s]


def scena_materia(s, L, e, forma):
    """### Il toro `L x L` dei triangoli *(`_triangoli.scena_toro`, `dtau 1.0`, `cs = s`, `lambda_c None`, il vuoto nullo)*, ### **il pacchetto gaussiano `W_MAT` sul primo vettore
    della coppia a `K`**, ### **e il campo `A = E = 0`.**"""
    import _triangoli as T
    import flussi_parziali as FP
    inc, mot, st, par = T.scena_toro(T.TRIANGOLI, (L, L), 1.0, T.X)
    n = inc.n
    mot.cs = np.full(n, float(s))
    mot.lambda_c = None
    for k in st:
        st[k][...] = 0
    v = np.arange(n)
    m1, m2 = v // L, v % L
    d1 = (m1 - L // 2 + L // 2) % L - L // 2
    d2 = (m2 - L // 2 + L // 2) % L - L // 2
    x, y = d1 - 0.5 * d2, d2 * math.sqrt(3.0) / 2.0
    g = np.exp(-(x * x + y * y) / (2.0 * W_MAT * W_MAT))
    cel = g[:, None] * u_K(s)[None, :] * np.exp(2j * np.pi * (m1 + m2) / 3.0)[:, None]
    cel /= np.sqrt(np.sum(np.abs(cel) ** 2))
    st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
    ii, jj = inc.nodo[0::2].astype(np.int64), inc.nodo[1::2].astype(np.int64)
    s_a = FP.s_arco(mot).copy()
    campo = Campo(ii, jj, (L, L), e, forma, s_a)
    return inc, mot, st, par, campo


def rho_nodi(st, mot):
    r = np.zeros(mot.inc.n)
    np.add.at(r, mot.inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    return r


def energia(st, mot, campo, conv, s_n):
    """### `E_tot` per tick *(il task history, `2.4`)*: ### **i generatori dei pezzi** *(Grover e spostamento, materia e vuoto; la moneta)* ### **piu' `H_F`.**"""
    import _triangoli as T
    inc = mot.inc
    nodo, n, m = inc.nodo, inc.n, inc.m
    d = inc.grado.astype(float)
    delta = 0.5 if conv == "simm" else 0.0
    tot = 0.0
    u = campo.u()
    for x, con_U in ((st["psi_h"], True), (st["phi_h"].reshape(-1, 1), False)):
        c = x.shape[1]
        Nh = np.sum(np.abs(x) ** 2, axis=1)
        Nk = np.zeros(n)
        np.add.at(Nk, nodo, Nh)
        Sk = np.zeros((n, c), dtype=complex)
        np.add.at(Sk, nodo, x)
        Pk = np.sum(np.abs(Sk) ** 2, axis=1) / d
        tot += -math.pi * float(np.sum(s_n * (Nk - Pk - delta * Nk)))
        v = x.reshape(m, 2, c)
        v1 = v[:, 1, :] * (np.conj(u)[:, None] if con_U else 1.0)
        w = np.sum(np.conj(v[:, 0, :]) * v1, axis=1)
        Na = np.sum(np.abs(v[:, 0, :]) ** 2 + np.abs(v[:, 1, :]) ** 2, axis=1)
        tot += -math.pi * float(np.sum(campo.s_a * (0.5 * Na - np.real(w) - delta * Na)))
    psi = st["psi_h"]
    a, b = psi[:, 0], psi[:, 1]
    nv = mot.geo.n
    ab = np.conj(a) * b
    sn = 2.0 * np.real(ab) * nv[:, 0] + 2.0 * np.imag(ab) * nv[:, 1] + (np.abs(a) ** 2 - np.abs(b) ** 2) * nv[:, 2]
    tot += float(np.sum(T.EPS_MONETA * s_n[nodo] * sn))
    return tot + campo.K() + campo.V()


def rovescia(st, mot, campo):
    """### **`T`:** `psi -> sigma_x psi^*` per estremita', `phi -> phi^*`, `A -> -A`, `E -> E`."""
    psi = st["psi_h"]
    psi[...] = np.conj(psi[:, ::-1]).copy()
    st["phi_h"][...] = np.conj(st["phi_h"]).copy()
    campo.A[...] = -campo.A
    scrivi_U(mot, campo)


def base(conv, s, forma, e):
    import _triangoli as T
    return {"conv": conv, "s": s, "forma": forma, "e": e, "carica": "norma (DEC-QC)", "tempo_campo": "arco (B-3), deriva s_a^2, spinta senza s",
            "eps_moneta": T.EPS_MONETA, "L": L_MAT, "W": W_MAT, "vuoto": "nullo", "passo_materia": "_triangoli.camminata (senza CAMM-MATERIA-VUOTO)"}


# =====================================================================================
#   PARTE A -- (a1), (a2)
# =====================================================================================
def parte_A():
    import _triangoli as T
    import _triangoli_forza as TF
    import tick as TK
    print("### PARTE A -- (a1) e = 0, A = E = 0, il campo acceso: la materia e OGNI attributo AL BIT per %d tick; (a2) e != 0: la prima meta' del tick AL BIT, lo scarto dopo un tick" % N_A1)
    s = S_GRIGLIA[1]
    for nome in CONV:
        with TF.conv(nome):
            _, motR, stR, parR, _ = scena_materia(s, L_MAT, 0.0, "noncompatto")
            for _ in range(N_A1):
                T.camminata(stR, motR, parR)
            _, motF, stF, parF, campo = scena_materia(s, L_MAT, 0.0, "noncompatto")
            with avvolto(motF, campo, True):
                for _ in range(N_A1):
                    tick(stF, motF, parF, campo)
        ba, bb = TF.byte_attr(motR), TF.byte_attr(motF)
        diversi = sorted(k for k in set(ba) | set(bb) if ba.get(k) != bb.get(k))
        st_div = sorted(k for k in stR if stR[k].tobytes() != stF[k].tobytes())
        esito("DEVE PASSARE (a1) %s: e = 0, %d tick: st e mot uguali AL BIT (%d attributi di mot)" % (nome, N_A1, len(ba)), not diversi and not st_div,
              "diversi: mot %s, st %s; campo max|A| %.1e max|E| %.1e" % (diversi[:4], st_div, float(np.max(np.abs(campo.A))), float(np.max(np.abs(campo.E)))))
        scrivi(dict(base(nome, s, "noncompatto", 0.0), tipo="a1", tick=N_A1, mot_diversi=diversi, st_diversi=st_div, n_attributi=len(ba)))
        dev = {}
        for e in E_PROVA:
            with TF.conv(nome):
                _, motR, stR, parR, _ = scena_materia(s, L_MAT, e, "compatto")
                TK.percorri_tick(stR, motR, parR, (T.S3,), None, 7)
                _, motF, stF, parF, campo = scena_materia(s, L_MAT, e, "compatto")
                with avvolto(motF, campo, True):
                    campo.spinta(0.5)
                    TK.percorri_tick(stF, motF, parF, (T.S3,), None, 7)
                meta = sorted(k for k in stR if stR[k].tobytes() != stF[k].tobytes())
                _, motR, stR, parR, _ = scena_materia(s, L_MAT, e, "compatto")
                T.camminata(stR, motR, parR)
                _, motF, stF, parF, campo = scena_materia(s, L_MAT, e, "compatto")
                with avvolto(motF, campo, True):
                    tick(stF, motF, parF, campo)
            dev[e] = rel(stR["psi_h"], stF["psi_h"])
            esito("DEVE PASSARE (a2) %s e %.4f: i primi 7 pezzi (fino alla deriva) uguali AL BIT" % (nome, e), not meta, "diversi %s; dopo un tick: scarto psi %.3e" % (meta, dev[e]))
            scrivi(dict(base(nome, s, "compatto", e), tipo="a2", meta_diversi=meta, scarto_un_tick=dev[e]))
        r = dev[E_PROVA[1]] / dev[E_PROVA[0]] if dev[E_PROVA[0]] > 0 else None
        print("  (a2) LETTURA %s: scarto dopo un tick %.3e / %.3e = %s contro (e2/e1)^2 = %.4f" % (nome, dev[E_PROVA[1]], dev[E_PROVA[0]], f_(r, "%.4f"), (E_PROVA[1] / E_PROVA[0]) ** 2))
        scrivi({"tipo": "a2_lettura", "conv": nome, "rapporto": r, "atteso": (E_PROVA[1] / E_PROVA[0]) ** 2})


# =====================================================================================
#   PARTE B-E -- gauge, Gauss, reversibilita', energia
# =====================================================================================
def gauge(conv, s, forma, e, modo):
    """### `modo`: `"chi"` *(la trasformazione intera)*, `"solo_psi"` *(il controllo negativo)*, ### **`"globale"`** *(`chi` UNIFORME, `A` invariato: una simmetria ESATTA, quindi lo scarto
    e' SOLO arrotondamento -- la diagnosi della scala, non un criterio)*."""
    import _triangoli_forza as TF
    rng = np.random.default_rng(SEME_CHI)
    with TF.conv(conv):
        _, mot1, st1, par1, c1 = scena_materia(s, L_MAT, e, forma)
        _, mot2, st2, par2, c2 = scena_materia(s, L_MAT, e, forma)
        chi = rng.uniform(-math.pi, math.pi, mot2.inc.n)
        if modo == "globale":
            chi[...] = chi[0]
        st2["psi_h"] *= np.exp(1j * chi[mot2.inc.nodo])[:, None]
        if modo == "chi":
            c2.A += (chi[c2.jj] - chi[c2.ii]) / e
        scrivi_U(mot2, c2)
        with avvolto(mot1, c1, True):
            for _ in range(N_B):
                tick(st1, mot1, par1, c1)
        with avvolto(mot2, c2, True):
            for _ in range(N_B):
                tick(st2, mot2, par2, c2)
    r = rel(rho_nodi(st1, mot1), rho_nodi(st2, mot2))
    eE = rel(c1.E, c2.E)
    eB = rel(e * c1.B(), e * c2.B(), 2.0 * math.pi)
    # ### ⭐ **LA STIMA dell'arrotondamento su `E` che viene dalla gauge** *(annotazione `1` del task history)*: ### **`A'` vale fino a `pi/e`, quindi `B'` ha un errore `~3 eps max|A'|`,
    # ### la spinta lo porta in `E` `x 2/A_p` per tick:** `N_B 6 eps max|A'| / A_p`.
    stima = N_B * 6.0 * float(np.finfo(float).eps) * float(np.max(np.abs(c2.A))) / AREA
    dE = float(np.max(np.abs(c1.E - c2.E)))
    return {"rho": r, "E": eE, "eB": eB, "max": max(r, eE, eB), "dE_assoluto": dE, "stima_dE": stima, "dE_su_stima": dE / stima if stima > 0 else None, "E_max": float(np.max(np.abs(c1.E)))}


def gauss_energia(conv, s, forma, e, sorgente, con_energia):
    import _triangoli_forza as TF
    with TF.conv(conv):
        _, mot, st, par, c = scena_materia(s, L_MAT, e, forma)
        rho0 = rho_nodi(st, mot)
        b = e * (rho0 - rho0.mean())
        c.E[...] = np.linalg.lstsq(c.matrice_div(), b, rcond=None)[0]
        G0 = c.div() - e * (rho0 - rho0.mean())
        scala = e * float(np.max(rho0))
        s_n = mot.cs.copy()
        peg, chiave, en = 0.0, 0.0, []
        if con_energia:
            en.append(energia(st, mot, c, conv, s_n))
        with avvolto(mot, c, sorgente):
            for _ in range(N_C):
                tick(st, mot, par, c)
                rho = rho_nodi(st, mot)
                G = c.div() - e * (rho - rho.mean())
                peg = max(peg, float(np.max(np.abs(G - G0))) / scala)
                chiave = max(chiave, float(np.max(np.abs((G - G0) + e * (rho - rho0)))) / scala)
                if con_energia:
                    en.append(energia(st, mot, c, conv, s_n))
    out = {"gauss": peg, "chiave": chiave, "G0": float(np.max(np.abs(G0))) / scala}
    if con_energia:
        en = np.array(en)
        t = np.arange(len(en), dtype=float)
        p = np.polyfit(t, en, 1)
        res = en - np.polyval(p, t)
        amp = float(res.max() - res.min())
        out.update(E_media=float(en.mean()), pendenza=float(p[0]), deriva=float(abs(p[0]) * N_C), ampiezza=amp, rel_ampiezza=amp / abs(float(en.mean())),
                   campo_fine=c.K() + c.V())
    return out


def reversibile(conv, s, forma, e):
    import _triangoli_forza as TF
    with TF.conv(conv):
        _, mot, st, par, c = scena_materia(s, L_MAT, e, forma)
        rho0 = rho_nodi(st, mot)
        c.E[...] = np.linalg.lstsq(c.matrice_div(), e * (rho0 - rho0.mean()), rcond=None)[0]
        psi0, phi0, A0, E0 = st["psi_h"].copy(), st["phi_h"].copy(), c.A.copy(), c.E.copy()
        amax = 0.0
        with avvolto(mot, c, True):
            for _ in range(N_D):
                tick(st, mot, par, c)
                amax = max(amax, float(np.max(np.abs(c.A))))
            rovescia(st, mot, c)
            for _ in range(N_D):
                tick(st, mot, par, c)
            rovescia(st, mot, c)
    out = {"psi": rel(psi0, st["psi_h"]), "phi_abs": float(np.max(np.abs(phi0 - st["phi_h"]))), "A": rel(A0, c.A, amax), "E": rel(E0, c.E), "A_max": amax}
    out["max"] = max(out["psi"], out["A"], out["E"], out["phi_abs"])
    return out


def parte_BE():
    print("### PARTE B-E -- (b) gauge %d tick, (c) Gauss %d tick, (d) reversibilita' %d+%d, (e) energia %d tick; per conv, s, forma, e" % (N_B, N_C, N_D, N_D, N_C))
    righe = []
    for conv in CONV:
        for s in S_GRIGLIA:
            for forma in FORME:
                for e in E_PROVA:
                    t0 = time.time()
                    g = gauge(conv, s, forma, e, "chi")
                    g["globale"] = gauge(conv, s, forma, e, "globale")
                    ge = gauss_energia(conv, s, forma, e, True, True)
                    rv = reversibile(conv, s, forma, e)
                    r = dict(base(conv, s, forma, e), tipo="sigilli", gauge=g, gauss=ge, rev=rv, secondi=time.time() - t0)
                    scrivi(r)
                    righe.append(r)
                    print("  %-4s s %.2f %-11s e %.4f | (b) rho %.1e E %.1e eB %.1e [fase globale: E %.1e; |dE| / stima %s] | (c) %.1e | (d) psi %.1e A %.1e E %.1e | (e) E %.6f deriva %.2e ampiezza %.2e (rel %.1e) campo %.2e | %.0fs"
                          % (conv, s, forma, e, g["rho"], g["E"], g["eB"], g["globale"]["E"], f_(g["dE_su_stima"], "%.2f"), ge["gauss"], rv["psi"], rv["A"], rv["E"], ge["E_media"], ge["deriva"], ge["ampiezza"], ge["rel_ampiezza"],
                             ge["campo_fine"], r["secondi"]))
                    sys.stdout.flush()
    neg = []
    for conv in CONV:
        for s in S_GRIGLIA:
            gn = gauge(conv, s, "compatto", E_PROVA[0], "solo_psi")
            cn = gauss_energia(conv, s, "compatto", E_PROVA[0], False, False)
            r = dict(base(conv, s, "compatto", E_PROVA[0]), tipo="negativi", gauge_solo_psi=gn, gauss_senza_sorgente=cn)
            scrivi(r)
            neg.append(r)
            print("  NEGATIVI %-4s s %.2f | (b-) solo psi: rho %.1e E %.1e eB %.1e | (c-) senza sorgente: Gauss %.1e, la chiave G - G0 + e(rho - rho0) %.1e"
                  % (conv, s, gn["rho"], gn["E"], gn["eB"], cn["gauss"], cn["chiave"]))
    return righe, neg


# =====================================================================================
#   PARTE F -- le onde libere
# =====================================================================================
def campo_toro(lati, s, e, forma):
    import _triangoli as T
    ii, jj, nn = T.toro_spostamenti(lati, T.TRIANGOLI[0])
    return Campo(ii, jj, lati, e, forma, np.full(len(ii), float(s)))


def blocchi_campo(s):
    """### La mappa del tick del campo *(non compatto)* sul toro `L_BLOCCHI`, ### **applicata ai vettori di base**; ### **i blocchi `T(R)` `6 x 6`** *(gli `A` e gli `E` dei tre archi della cella)*."""
    L = L_BLOCCHI
    c = campo_toro((L, L), s, 1.0, "noncompatto")
    m = c.m
    M = np.zeros((2 * m, 2 * m))
    for j in range(2 * m):
        c.A[...] = 0
        c.E[...] = 0
        (c.A if j < m else c.E)[j % m] = 1.0
        tick_campo(c)
        M[:m, j] = c.A
        M[m:, j] = c.E

    def dof(v, i):
        return (i // 3) * m + 3 * v + (i % 3)
    bl = {}
    for v in range(L * L):
        r1, r2 = v // L, v % L
        R = (r1 - L if r1 > L // 2 else r1, r2 - L if r2 > L // 2 else r2)
        bl[R] = np.array([[M[dof(v, i), dof(0, j)] for j in range(6)] for i in range(6)])
    fuori = max(float(np.max(np.abs(B))) for R, B in bl.items() if max(abs(R[0]), abs(R[1])) > SUPPORTO)
    # ### la ricostruzione: M[r, r'] = T(r - r')
    Mr = np.zeros_like(M)
    for v in range(L * L):
        for w in range(L * L):
            d1, d2 = (v // L - w // L) % L, (v % L - w % L) % L
            R = (d1 - L if d1 > L // 2 else d1, d2 - L if d2 > L // 2 else d2)
            B = bl[R]
            for i in range(6):
                Mr[dof(v, i), [dof(w, j) for j in range(6)]] = B[i]
    return [(R, B) for R, B in bl.items() if max(abs(R[0]), abs(R[1])) <= SUPPORTO], fuori, float(np.max(np.abs(M - Mr)))


def blocco_k(bl, t1, t2):
    return sum(B * np.exp(-1j * (t1 * R[0] + t2 * R[1])) for R, B in bl)


def carta(t1, t2):
    """### `M = (l/l*) C^dagger diag(1/A) C` sulla carta: gli autovalori `lambda`."""
    C = np.array([[1.0, np.exp(1j * t1), -1.0], [-np.exp(1j * t2), -1.0, 1.0]])
    return np.sort(np.linalg.eigvalsh(L_SU_LS / AREA * C.conj().T @ C))


def t_di(kx, ky):
    import _triangoli_bassa_energia as BE
    J = BE.J
    return J[0, 0] * kx + J[0, 1] * ky, J[1, 0] * kx + J[1, 1] * ky


def fasi_k(bl, t1, t2):
    lam = np.linalg.eigvals(blocco_k(bl, t1, t2))
    return lam


def omega_fotone(bl, t1, t2):
    lam = fasi_k(bl, t1, t2)
    w = np.abs(np.angle(lam[np.abs(lam - 1.0) > GAUGE_VICINO]))
    return float(np.min(w))


def max_instabile(bl, L):
    peg, dove = 0.0, None
    for n1 in range(L):
        for n2 in range(L):
            lam = fasi_k(bl, 2 * np.pi * n1 / L, 2 * np.pi * n2 / L)
            lam = lam[np.abs(lam - 1.0) > GAUGE_VICINO]
            if lam.size and float(np.max(np.abs(lam))) > peg:
                peg, dove = float(np.max(np.abs(lam))), (n1, n2)
    return peg, dove


def pacchetto_campo(c, bl, t0, W, r0, ndir):
    """### **Il fotone reale:** `2 Re sum_k g(k) e^{i k.(r - r0)} u(k)` sulla griglia del toro, ### `g` la gaussiana di larghezza `1/W` attorno a `t0`; ### **`u(k)` l'autovettore del
    fotone a fase negativa** *(`e^{-i omega}`), ### **la fase fissata da `<u(k0)|u(k)>` reale.** ### `ndir` le direzioni della griglia lungo cui si somma *(`1` o `2`)*."""
    L1, L2 = c.lati
    import _triangoli_bassa_energia as BE
    Jinv = np.linalg.inv(BE.J)
    v = np.arange(c.n)
    m1, m2 = v // L2, v % L2
    n1c = int(round(t0[0] * L1 / (2 * np.pi)))
    n2c = int(round(t0[1] * L2 / (2 * np.pi)))
    r = int(math.ceil(4.0 * max(L1, L2) / (2 * np.pi * W)))
    x = np.zeros(2 * c.m, dtype=complex)
    u0 = None
    spettro = []

    def fotone(t1, t2):
        lam, V = np.linalg.eig(blocco_k(bl, t1, t2))
        ph = np.angle(lam)
        ok = [i for i in range(6) if abs(lam[i] - 1.0) > GAUGE_VICINO and ph[i] < 0]
        i = min(ok, key=lambda i: abs(ph[i]))
        return V[:, i]
    for d1 in range(-r, r + 1):
        for d2 in (range(-r, r + 1) if ndir == 2 else (0,)):
            t1, t2 = 2 * np.pi * (n1c + d1) / L1, 2 * np.pi * (n2c + d2) / L2
            dk = Jinv @ np.array([t1 - t0[0], t2 - t0[1]])
            g = math.exp(-W * W * float(dk @ dk) / 2.0)
            if g < 1e-8:
                continue
            uk = fotone(t1, t2)
            if u0 is None:
                u0 = fotone(*t0)
            ov = np.vdot(u0, uk)
            uk = uk * (np.conj(ov) / abs(ov))
            spettro.append((t1, t2, g, uk))
            fase = np.exp(1j * (t1 * (m1 - r0[0]) + t2 * (m2 - r0[1])))
            for i in range(6):
                x[(i // 3) * c.m + 3 * v + (i % 3)] += g * fase * uk[i]
    x = 2.0 * np.real(x)
    c.A[...] = x[:c.m]
    c.E[...] = x[c.m:]
    sc = float(np.max(np.abs(c.B())))
    c.A /= sc
    c.E /= sc
    return spettro


def v_prevista(spettro, bl, w, s):
    """### ⭐ **LA VELOCITA' PREVISTA DEL BARICENTRO** *(annotazione `2` del task history)*: ### **la media di `d omega/d k_x` sullo spettro del pacchetto, pesata con l'energia di ogni
    componente** *(`w |u_E|^2/2 + |C(k) u_A|^2/(2 A_p)` per cella, per `g^2`)*, ### **per tempo proprio.** ### **`v_g(k0)` da sola ignora la larghezza in ANGOLO del pacchetto.**"""
    num = den = 0.0
    h = 1e-5
    for t1, t2, g, uk in spettro:
        C = np.array([[1.0, np.exp(1j * t1), -1.0], [-np.exp(1j * t2), -1.0, 1.0]])
        H = g * g * (w * float(np.sum(np.abs(uk[3:]) ** 2)) / 2.0 + float(np.sum(np.abs(C @ uk[:3]) ** 2)) / (2.0 * AREA))
        vx = (omega_fotone(bl, t1 + h, t2 - h / 2) - omega_fotone(bl, t1 - h, t2 + h / 2)) / (2 * h) / s
        num += H * vx
        den += H
    return num / den


def energia_nodi(c):
    eA = c.w * c.E * c.E / 2.0
    B = c.B()
    eV = (1.0 - np.cos(c.e * B)) / (c.e * c.e * AREA) if c.forma == "compatto" else B * B / (2.0 * AREA)
    return eA.reshape(c.n, 3).sum(axis=1) + eV[:c.n] + eV[c.n:]


def baricentro(c, prec):
    """### Il baricentro dell'energia in coordinate di reticolo, ### **seguito** *(l'immagine minima attorno al precedente)*."""
    L1, L2 = c.lati
    w = energia_nodi(c)
    v = np.arange(c.n)
    m1, m2 = (v // L2).astype(float), (v % L2).astype(float)
    d1 = (m1 - prec[0] + L1 / 2.0) % L1 - L1 / 2.0
    d2 = (m2 - prec[1] + L2 / 2.0) % L2 - L2 / 2.0
    return (prec[0] + float(np.sum(w * d1) / np.sum(w)), prec[1] + float(np.sum(w * d2) / np.sum(w))), w


def corsa_pacchetto(s, forma, e, bl):
    L = L_PACC
    c = campo_toro((L, L), s, e, forma)
    t0 = (2 * np.pi * N_K0 / L, -2 * np.pi * (N_K0 // 2) / L)
    r0 = (L / 2.0, L / 2.0)
    spettro = pacchetto_campo(c, bl, t0, W_PACC, r0, 2)
    vp = v_prevista(spettro, bl, s * s * L_SU_LS, s)
    H0 = c.K() + c.V()
    T = int(math.ceil(TRATTO / s))
    pos, tt, xx = r0, [], []
    for t in range(T + 1):
        if t:
            tick_campo(c)
        pos, _ = baricentro(c, pos)
        tt.append(t * s)
        xx.append((pos[0] - r0[0]) - 0.5 * (pos[1] - r0[1]))
    p = np.polyfit(np.array(tt), np.array(xx), 1)
    return {"v": float(p[0]), "v_prevista": vp, "deriva_energia": (c.K() + c.V() - H0) / H0, "tick": T, "eB_max": float(np.max(np.abs(e * c.B())))}


def parte_F():
    print("### PARTE F -- le onde libere: i blocchi del tick del campo, la dispersione a Gamma K M, la velocita' di gruppo a k %g, l'isotropia, Courant, il pacchetto" % K_PICCOLO)
    righe = {}
    for s in S_GRIGLIA + (S_COURANT,):
        bl, fuori, ricostr = blocchi_campo(s)
        esito("SERVIZIO s %.2f: i blocchi oltre +-%d celle nulli, e la mappa ricostruita dai blocchi = la mappa" % (s, SUPPORTO), fuori == 0.0 and ricostr <= TOLL_SERV,
              "fuori %.1e, ricostruzione %.1e" % (fuori, ricostr))
        peg_carta = 0.0
        for n1 in range(1, L_BLOCCHI):
            for n2 in range(L_BLOCCHI):
                t1, t2 = 2 * np.pi * n1 / L_BLOCCHI, 2 * np.pi * n2 / L_BLOCCHI
                lam = fasi_k(bl, t1, t2)
                lam = lam[np.abs(lam - 1.0) > GAUGE_VICINO]
                atteso = np.sort(np.repeat(1.0 - s * s * carta(t1, t2)[1:] / 2.0, 2))
                if len(lam) == 4:
                    peg_carta = max(peg_carta, float(np.max(np.abs(np.sort(lam.real) - atteso))))
                else:
                    peg_carta = float("inf")
        if s != S_COURANT:
            esito("SERVIZIO s %.2f: Re(lambda) del passo = 1 - s^2 lambda_carta/2 sulla griglia %dx%d (fuori Gamma)" % (s, L_BLOCCHI, L_BLOCCHI), peg_carta <= TOLL_SERV, "%.1e" % peg_carta)
        punti = {"Gamma": (0.0, 0.0), "K": (2 * np.pi / 3, 2 * np.pi / 3), "M": (np.pi, 0.0)}
        disp = {}
        for nome, (t1, t2) in punti.items():
            lam = fasi_k(bl, t1, t2)
            disp[nome] = {"omega_su_s": sorted(float(abs(np.angle(x))) / s for x in lam), "mod": sorted(float(abs(x)) for x in lam),
                          "carta_sqrt_lambda": [float(math.sqrt(max(x, 0.0))) for x in carta(t1, t2)]}
        vg = []
        for k in range(DIREZIONI_V):
            a = np.pi * k / DIREZIONI_V
            wp = omega_fotone(bl, *t_di((K_PICCOLO + H_K) * math.cos(a), (K_PICCOLO + H_K) * math.sin(a)))
            wm = omega_fotone(bl, *t_di((K_PICCOLO - H_K) * math.cos(a), (K_PICCOLO - H_K) * math.sin(a)))
            vg.append((wp - wm) / (2 * H_K) / s)
        inst, dove = max_instabile(bl, L_COURANT)
        righe[s] = {"bl": bl, "disp": disp, "vg": vg, "instabile": inst, "dove": dove}
        r = {"tipo": "dispersione", "s": s, "forma": "noncompatto (linearizzato: compatto identico)", "tempo_campo": "arco", "dispersione": disp, "v_g_su_s": vg,
             "v_g_media": float(np.mean(vg)), "isotropia": float((max(vg) - min(vg)) / np.mean(vg)), "max_lambda": inst, "k_max": dove, "servizio_carta": peg_carta}
        scrivi(r)
        print("  s %.2f | Gamma omega/s %s | K %s | M %s" % (s, " ".join("%.4f" % x for x in disp["Gamma"]["omega_su_s"]), " ".join("%.4f" % x for x in disp["K"]["omega_su_s"]),
                                                            " ".join("%.4f" % x for x in disp["M"]["omega_su_s"])))
        print("         carta sqrt(lambda): Gamma %s K %s M %s" % tuple(" ".join("%.4f" % x for x in disp[p]["carta_sqrt_lambda"]) for p in ("Gamma", "K", "M")))
        print("         v_g/s a k %g: media %.6f, min %.6f, max %.6f, isotropia %.2e | max|lambda| (fuori dalla gauge) %.6f a k %s" % (K_PICCOLO, np.mean(vg), min(vg), max(vg), r["isotropia"], inst, dove))
    # ### Courant
    a = righe[S_COURANT]
    if S_STABILE not in righe:
        bl, _, _ = blocchi_campo(S_STABILE)
        righe[S_STABILE] = {"bl": bl, "instabile": max_instabile(bl, L_COURANT)[0]}
    b = righe[S_STABILE]
    lam_g = fasi_k(a["bl"], 0.0, 0.0)
    alta = float(np.max(np.abs(lam_g)))
    esito("DEVE FALLIRE (la stabilita' a s %.2f), PER LA CHIAVE GIUSTA: max|lambda| > 1 + %g, il k peggiore Gamma, la banda piu' alta" % (S_COURANT, INSTABILE),
          a["instabile"] > 1.0 + INSTABILE and a["dove"] == (0, 0) and abs(alta - a["instabile"]) <= 1e-12, "max|lambda| %.6f a %s" % (a["instabile"], a["dove"]))
    esito("DEVE PASSARE: stabile a s %.2f (max|lambda| fuori dalla gauge <= 1 + %g)" % (S_STABILE, INSTABILE), b["instabile"] <= 1.0 + INSTABILE, "%.12f" % b["instabile"])
    lo, hi = S_STABILE, S_COURANT
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        bl, _, _ = blocchi_campo(mid)
        if max_instabile(bl, 6)[0] > 1.0 + INSTABILE:
            hi = mid
        else:
            lo = mid
    print("  COURANT MISURATO: s critico fra %.8f e %.8f (bisezione sulla griglia 6x6, Gamma compreso), contro 2/sqrt(24) = %.8f" % (lo, hi, 2.0 / math.sqrt(24.0)))
    scrivi({"tipo": "courant", "s_critico": [lo, hi], "carta": 2.0 / math.sqrt(24.0)})
    vg05 = float(np.mean(righe[S_GRIGLIA[0]]["vg"]))
    esito("PUO' FALLIRE: la velocita' del fotone entro %g da 1 per tempo proprio, non compatto, s %.2f (dal blocco, k %g)" % (TOLL_UNO, S_GRIGLIA[0], K_PICCOLO), abs(vg05 - 1.0) <= TOLL_UNO,
          "v_g/s %.6f" % vg05, deve=False)
    # ### il pacchetto
    pacc = []
    for s in S_GRIGLIA:
        bl = righe[s]["bl"]
        t0 = (2 * np.pi * N_K0 / L_PACC, -2 * np.pi * (N_K0 // 2) / L_PACC)
        h = 1e-5
        vgk0 = (omega_fotone(bl, t0[0] + h, t0[1] - h / 2) - omega_fotone(bl, t0[0] - h, t0[1] + h / 2)) / (2 * h) / s
        nc = corsa_pacchetto(s, "noncompatto", 1.0, bl)
        esito("SERVIZIO s %.2f: il pacchetto non compatto alla velocita' prevista dallo spettro (i blocchi) entro %g" % (s, TOLL_PACC), abs(nc["v"] / nc["v_prevista"] - 1.0) <= TOLL_PACC,
              "v %.5f contro la prevista %.5f (v_g(k0) %.5f); energia %.1e" % (nc["v"], nc["v_prevista"], vgk0, nc["deriva_energia"]))
        for e in E_PROVA:
            co = corsa_pacchetto(s, "compatto", e, bl)
            crit = abs(co["v"] / nc["v"] - 1.0) + abs(float(np.mean(righe[s]["vg"])) - 1.0)
            r = {"tipo": "pacchetto", "s": s, "e": e, "k0": t0, "W": W_PACC, "v_noncompatto": nc["v"], "v_prevista": nc["v_prevista"], "v_compatto": co["v"], "v_g_k0": vgk0, "eB_max": co["eB_max"],
                 "energia_nc": nc["deriva_energia"], "energia_c": co["deriva_energia"], "criterio": crit}
            scrivi(r)
            pacc.append(r)
            print("  pacchetto s %.2f e %.4f | v/s non compatto %.5f, compatto %.5f (max|eB| %.3f), v_g(k0)/s %.5f | il criterio %.2e" % (s, e, nc["v"], co["v"], co["eB_max"], vgk0, crit))
            if s == S_GRIGLIA[0]:
                esito("PUO' FALLIRE: lo stesso nel compatto (Polyakov), s %.2f e %.4f: |v_c/v_nc - 1| + |v_g/s - 1| <= %g" % (s, e, TOLL_UNO), crit <= TOLL_UNO, "%.2e" % crit, deve=False)
    return righe, pacc


# =====================================================================================
#   PARTE G -- Shapiro
# =====================================================================================
def campo_gradiente(e, forma):
    import _triangoli as T
    import flussi_parziali as FP
    L1, L2 = LG
    inc, mot, st, par = T.scena_toro(T.TRIANGOLI, LG, 1.0, T.X)
    m1 = np.arange(inc.n) // L2
    cs = S0_G * (1.0 + ETA_G * np.cos(2.0 * np.pi * m1 / L1))
    mot.cs = cs
    mot.lambda_c = None
    s_a = FP.s_arco(mot).copy()
    c = Campo(inc.nodo[0::2].astype(np.int64), inc.nodo[1::2].astype(np.int64), LG, e, forma, s_a)
    return c, cs


def parte_G(bl0):
    print("### PARTE G -- Shapiro: il toro %dx%d, cs = %.2f (1 + %.2f cos(2 pi m1/L1)), non compatto; la velocita' locale contro cs locale, e la deflessione" % (LG + (S0_G, ETA_G)))
    L1, L2 = LG
    c, cs = campo_gradiente(1.0, "noncompatto")
    pacchetto_campo(c, bl0, (2 * np.pi * N1_G / L1, 0.0), W_G, (L1 / 4.0, 0.0), 1)
    H0 = c.K() + c.V()
    pos, uu, ss = (L1 / 4.0, 0.0), [], []
    for t in range(T_G + 1):
        if t:
            tick_campo(c)
        pos, w = baricentro(c, pos)
        uu.append(pos[0] * math.sqrt(3.0) / 2.0)
        ss.append(float(np.sum(w * cs) / np.sum(w)))
    uu, ss = np.array(uu), np.array(ss)
    v = (uu[2 * FIN_G:] - uu[:-2 * FIN_G]) / (2 * FIN_G)
    rr = v / ss[FIN_G:-FIN_G]
    var = float((rr.max() - rr.min()) / rr.mean())
    tempo_atteso = float(np.sum(np.diff(uu) / (0.5 * (ss[1:] + ss[:-1]))))
    r = {"tipo": "shapiro", "lati": LG, "s0": S0_G, "eta": ETA_G, "t1": 2 * np.pi * N1_G / L1, "W_u": W_G, "tick": T_G, "v_su_cs_media": float(rr.mean()), "v_su_cs_min": float(rr.min()),
         "v_su_cs_max": float(rr.max()), "variazione": var, "cs_min_visto": float(ss.min()), "cs_max_visto": float(ss.max()), "tratto_u": float(uu[-1] - uu[0]),
         "tempo_integrale_ds_su_cs": tempo_atteso, "tempo_vero": T_G, "energia": (c.K() + c.V() - H0) / H0, "forma_tempo": "deriva s_a^2, spinta senza s (il task history, 1.3)"}
    scrivi(r)
    print("  lungo il gradiente: v/cs media %.5f, min %.5f, max %.5f: variazione %.2e (cs visto %.3f..%.3f, tratto u %.1f); int du/(v/cs . cs) %.1f tick contro %d; energia %.1e"
          % (rr.mean(), rr.min(), rr.max(), var, ss.min(), ss.max(), uu[-1] - uu[0], tempo_atteso / rr.mean(), T_G, r["energia"]))
    esito("PUO' FALLIRE (g): la velocita' locale proporzionale a cs entro %g" % TOLL_G, var <= TOLL_G, "%.2e" % var, deve=False)
    c, cs = campo_gradiente(1.0, "noncompatto")
    u0m = L1 / 4.0
    pacchetto_campo(c, bl0, (2 * np.pi * N_DEF[0] / L1, 2 * np.pi * N_DEF[1] / L2), W_G, (u0m, 0.0), 1)
    pos, uu = (u0m, 0.0), []
    for t in range(T_DEF + 1):
        if t:
            tick_campo(c)
        pos, _ = baricentro(c, pos)
        uu.append(pos[0] * math.sqrt(3.0) / 2.0)
    tt = np.arange(T_DEF + 1, dtype=float)
    p = np.polyfit(tt, np.array(uu), 2)
    a = 2.0 * float(p[0])
    u0 = u0m * math.sqrt(3.0) / 2.0
    ds_du = -S0_G * ETA_G * 2.0 * np.pi / L1 * math.sin(2.0 * np.pi * u0m / L1) / (math.sqrt(3.0) / 2.0)
    a_att = -S0_G * (1.0 + ETA_G * math.cos(2.0 * np.pi * u0m / L1)) * ds_du
    r = {"tipo": "deflessione", "u0": u0, "a": a, "a_raggi": a_att, "rapporto": a / a_att, "v0": float(p[1]), "tick": T_DEF}
    scrivi(r)
    print("  la deflessione (lungo a2, nel gradiente massimo): d2u/dt2 %.3e contro l'ottica dei raggi -s ds/du %.3e: rapporto %.3f (verso cs %s)"
          % (a, a_att, a / a_att, "piu' basso" if a > 0 else "piu' alto"))


def main(argv):
    del argv
    import _presidio
    import _triangoli as T
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 120)
    print("IL PROTOTIPO DEL CAMPO U(1) SUI TRIANGOLI, IN MEMORIA: la catena dei sigilli e la velocita' della luce")
    print("=" * 120)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_triangoli.py", "csv/_triangoli_bassa_energia.py", "csv/_triangoli_forza.py", "csv/_triangoli_fattore.py",
                                     "csv/_zero_simmetrico.py", "csv/_universalita_massa.py", "csv/_u1_prototipo.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: CONV %s; S %s; S_COURANT %.2f; S_STABILE %.2f; FORME %s; E_PROVA %s (il derivato: SALTATO, il task history 1.5); la carica: la norma; il tempo del campo: l'arco"
          % (CONV, S_GRIGLIA, S_COURANT, S_STABILE, FORME, tuple(round(e, 6) for e in E_PROVA)))
    print("    l/l* %.6f, A_p %.6f; eps moneta %.2f; L_MAT %d, W_MAT %.1f, il vuoto nullo, la camminata senza CAMM-MATERIA-VUOTO; N_A1 %d N_B %d N_C %d N_D %d; SEME_CHI %d"
          % (L_SU_LS, AREA, T.EPS_MONETA, L_MAT, W_MAT, N_A1, N_B, N_C, N_D, SEME_CHI))
    print("    TOLL_REL %g TOLL_ROTTA %g TOLL_SERV %g; L_BLOCCHI %d SUPPORTO %d L_COURANT %d; K_PICCOLO %g H_K %g DIREZIONI_V %d; GAUGE_VICINO %g INSTABILE %g; L_PACC %d N_K0 %d W_PACC %.1f TRATTO %.1f TOLL_PACC %g TOLL_UNO %g"
          % (TOLL_REL, TOLL_ROTTA, TOLL_SERV, L_BLOCCHI, SUPPORTO, L_COURANT, K_PICCOLO, H_K, DIREZIONI_V, GAUGE_VICINO, INSTABILE, L_PACC, N_K0, W_PACC, TRATTO, TOLL_PACC, TOLL_UNO))
    print("    LG %s S0_G %.2f ETA_G %.2f N1_G %d N_DEF %s W_G %.1f T_G %d T_DEF %d FIN_G %d TOLL_G %g" % (LG, S0_G, ETA_G, N1_G, N_DEF, W_G, T_G, T_DEF, FIN_G, TOLL_G))
    print("-" * 120)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    # ### il servizio della geometria: div rot = 0 negli interi
    c = campo_toro((6, 6), 0.1, 1.0, "noncompatto")
    dc = float(np.max(np.abs(c.matrice_div() @ c.matrice_rot().T)))
    esito("SERVIZIO: div rot^T = 0 ESATTO negli interi (toro 6x6), ogni arco in due placchette", dc == 0.0, "%.1e" % dc)
    # ### ⛔ **la coppia a `K` si calcola FUORI da ogni convenzione:** `coppia_K` mette gia' lo zero simmetrico, e dentro `conv("simm")` lo metterebbe DUE volte
    for s in S_GRIGLIA:
        u_K(s)
    print("-" * 120)
    parte_A()
    print("-" * 120)
    righe, neg = parte_BE()
    print("### I CONTROLLI DI B-E")
    pb = max(r["gauge"]["max"] for r in righe)
    pg = max(r["gauge"]["globale"]["max"] for r in righe)
    esito("DEVE PASSARE (b): le osservabili invarianti uguali entro %g relativo, ogni riga" % TOLL_REL, pb <= TOLL_REL,
          "il peggiore %.2e (rho %.1e, E %.1e, eB %.1e); la diagnosi, la fase globale (solo arrotondamento): il peggiore %.2e" % (
              pb, max(r["gauge"]["rho"] for r in righe), max(r["gauge"]["E"] for r in righe), max(r["gauge"]["eB"] for r in righe), pg))
    pc = max(r["gauss"]["gauss"] for r in righe)
    esito("DEVE PASSARE (c): Gauss a ogni tick per %d tick entro %g relativo, ogni riga" % (N_C, TOLL_REL), pc <= TOLL_REL, "il peggiore %.2e" % pc)
    pd = max(r["rev"]["max"] for r in righe)
    esito("DEVE PASSARE (d): %d avanti, T, %d avanti, T: lo stato di partenza entro %g relativo, ogni riga" % (N_D, N_D, TOLL_REL), pd <= TOLL_REL, "il peggiore %.2e" % pd)
    de = [r for r in righe if r["gauss"]["deriva"] > r["gauss"]["ampiezza"] / 2.0]
    esito("DEVE PASSARE (e): nessuna deriva dell'energia: |pendenza| %d <= ampiezza/2, ogni riga" % N_C, not de,
          "%d righe con deriva; la peggiore deriva/ampiezza %.2e" % (len(de), max(r["gauss"]["deriva"] / r["gauss"]["ampiezza"] for r in righe)))
    nb = min(r["gauge_solo_psi"]["max"] for r in neg)
    esito("DEVE FALLIRE (b-): trasformando solo psi le osservabili cambiano (> %g)" % TOLL_ROTTA, nb > TOLL_ROTTA, "il minimo %.2e" % nb)
    nc = min(r["gauss_senza_sorgente"]["gauss"] for r in neg)
    nk = max(r["gauss_senza_sorgente"]["chiave"] for r in neg)
    esito("DEVE FALLIRE (c-), PER LA CHIAVE GIUSTA: senza sorgente Gauss si rompe (> %g) e G - G0 = -e(rho - rho0) entro %g" % (TOLL_ROTTA, TOLL_REL), nc > TOLL_ROTTA and nk <= TOLL_REL,
          "Gauss minimo %.2e, la chiave peggiore %.2e" % (nc, nk))
    print("-" * 120)
    rf, _ = parte_F()
    print("-" * 120)
    parte_G(blocchi_campo(S0_G)[0])
    print("-" * 120)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
