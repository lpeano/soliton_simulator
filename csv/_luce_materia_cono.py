# -*- coding: utf-8 -*-
r"""**LA LUCE E LA MATERIA ATTORNO A UN CONO** *(la parte C2 del mandato delle 20:44; [[PROGETTO-MITOSI]], sezione `4`; [[LORENTZ-MATERIA-INTERFERENZA]], [[PROGETTO-U1]])*: ### **un disco a
triangoli col centro a `5` vicini** *(il difetto d'angolo `pi/3`)* ### **e il disco piatto; due fasci ai due lati del centro; la convergenza della luce** *(il campo `F1`)* ### **e della materia**
*(il generatore a `eps 0`)*.

> ### ⛔ **Il task history e' `2026-10-25_luce_materia_cono.md`.** ### **Strumenti in memoria; nessun file del nucleo.**
> ### **Importati, non copiati:** `_u1_prototipo` *(`Campo`, `campo_toro`, `blocchi_campo`, `pacchetto_campo`, `tick_campo`, `AREA`, `L_SU_LS`)*, `_u1_terzo.H_gen`, `_massa_nei_difetti` *(`H_diretto`, `toro` per i controlli)*.
> ### **La classe `CampoGrafo` ripete le operazioni di `_u1_prototipo.Campo` su placchette QUALUNQUE** *(il controllo `0` la confronta con la classe vera)*.

Gira con:  python csv/_luce_materia_cono.py > doc/referti_l2/luce_materia_cono.txt
"""
import io
import json
import math
import os
import sys
import time
from collections import deque

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

R_DISCO = 130
X0 = -65.0
BB = (24.0, 32.0, 40.0)
B_CONV = 32.0
S_LUCE = 0.3
E_LUCE = 1.0                    # ### non compatto: e entra solo in u = e^{i e A}, che qui non serve
L_TORO = 128
N_K0 = 20                       # ### k0 = 2 pi 20/128 = 0.982 lungo +x
W_LUCE = (6.0, 9.0)
Q_MAT = 0.5
W_MAT = (8.0, 11.0)
D_COPIA = 50.0
DT_MAT = 5.0
T_MAX_MAT = 4000.0
PERC_FINESTRA = 0.99
L_USCITA = 40.0
D_BORDO = 4
GUARDIA_BORDO = 1e-6
TOLL_CAMPO = 1e-13
TOLL_GEN = 1e-15
TOLL_BANDA = 1e-10
TOLL_PI3 = 0.05
TOLL_EP = 0.05
TOLL_CHIAVE = 0.10
N_TICK_CONTROLLO = 20
JSONL = os.path.join(RADICE, "doc", "referti_l2", "luce_materia_cono.jsonl")
OK = [0, 0]
FALLITE = []
A1 = np.array([1.0, 0.0])
A2 = np.array([-0.5, math.sqrt(3.0) / 2.0])


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


# =====================================================================================
#   IL DISCO A SETTORI
# =====================================================================================
def e_(s):
    a = math.radians(60.0 * s)
    return np.array([math.cos(a), math.sin(a)])


class Disco(object):
    """### `n` settori di lato `R`, incollati: ### **i nodi, gli archi** *(`ii`, `jj`, il settore, la posizione nella carta)*, ### **i triangoli** *(`P`, `S` come `_u1_prototipo.Campo`)*."""

    def __init__(self, n, R):
        self.n_sett, self.R = n, R
        ids = {}
        pos, sett, bordo = [], [], []

        def canon(s, a, b):
            if a == 0 and b == 0:
                return (0, 0, 0)
            if a == 0:
                return ((s + 1) % n, b, 0)
            return (s, a, b)

        def nodo(s, a, b):
            c = canon(s, a, b)
            if c not in ids:
                ids[c] = len(pos)
                pos.append(c[1] * e_(c[0]) + c[2] * e_(c[0] + 1))
                sett.append(c[0])
                bordo.append(c[1] + c[2] == R)
            return ids[c]
        archi = {}
        lista = []
        for s in range(n):
            for a in range(R + 1):
                for b in range(R + 1 - a):
                    nodo(s, a, b)
        for s in range(n):
            for a in range(R + 1):
                for b in range(R + 1 - a):
                    for (a2, b2) in ((a + 1, b), (a, b + 1)):
                        if a2 + b2 <= R:
                            self._arco(nodo, archi, lista, s, (a, b), (a2, b2))
                    if a + b + 1 <= R:
                        self._arco(nodo, archi, lista, s, (a + 1, b), (a, b + 1))
        self.ii = np.array([x[0] for x in lista], dtype=int)
        self.jj = np.array([x[1] for x in lista], dtype=int)
        self.sett_arco = np.array([x[2] for x in lista], dtype=int)
        self.pos_arco = np.array([x[3] for x in lista])
        self.lat_arco = [x[4] for x in lista]
        self.pos = np.array(pos)
        self.sett = np.array(sett, dtype=int)
        self.bordo = np.array(bordo)
        self.nn = len(pos)
        P, S, ps, ss = [], [], [], []
        for s in range(n):
            for a in range(R + 1):
                for b in range(R + 1 - a):
                    if a + b + 1 <= R:
                        self._tri(nodo, archi, P, S, ps, ss, s, ((a, b), (a + 1, b), (a, b + 1)))
                    if a + b + 2 <= R:
                        self._tri(nodo, archi, P, S, ps, ss, s, ((a + 1, b), (a + 1, b + 1), (a, b + 1)))
        self.P = np.array(P, dtype=int)
        self.S = np.array(S, dtype=float)
        self.pos_tri = np.array(ps)
        self.sett_tri = np.array(ss, dtype=int)

    @staticmethod
    def _p(s, ab):
        return ab[0] * e_(s) + ab[1] * e_(s + 1)

    def _arco(self, nodo, archi, lista, s, p, q):
        u, v = nodo(s, *p), nodo(s, *q)
        key = (min(u, v), max(u, v))
        if key in archi:
            return
        archi[key] = len(lista)
        pu, pv = self._p(s, p), self._p(s, q)
        lista.append((u, v, s, 0.5 * (pu + pv), (pu, pv)))

    def _tri(self, nodo, archi, P, S, ps, ss, s, tre):
        vv = [nodo(s, *x) for x in tre]
        riga, sg = [], []
        for c in range(3):
            u, v = vv[c], vv[(c + 1) % 3]
            k = archi[(min(u, v), max(u, v))]
            riga.append(k)
            sg.append(1.0 if (self.ii[k] if hasattr(self, "ii") else None) == u else -1.0)
        P.append(riga)
        S.append(sg)
        ps.append(sum(self._p(s, x) for x in tre) / 3.0)
        ss.append(s)

    def gradi(self):
        return np.bincount(self.ii, minlength=self.nn) + np.bincount(self.jj, minlength=self.nn)

    def dist_bordo(self):
        adj = [[] for _ in range(self.nn)]
        for a, b in zip(self.ii, self.jj):
            adj[a].append(b)
            adj[b].append(a)
        d = np.full(self.nn, -1, dtype=int)
        q = deque()
        for v in np.where(self.bordo)[0]:
            d[v] = 0
            q.append(v)
        while q:
            v = q.popleft()
            for w in adj[v]:
                if d[w] < 0:
                    d[w] = d[v] + 1
                    q.append(w)
        return d


# =====================================================================================
#   IL CAMPO F1 SU UN GRAFO
# =====================================================================================
class CampoGrafo(object):
    """### **Le operazioni di `_u1_prototipo.Campo`** *(non compatto)* ### **su placchette qualunque** `(P, S)`."""

    def __init__(self, P, S, m, s_a):
        import scipy.sparse as sp
        import _u1_prototipo as U
        self.P, self.S, self.m = np.asarray(P), np.asarray(S, dtype=float), int(m)
        nt = len(self.P)
        self.C = sp.csr_matrix((self.S.ravel(), (np.repeat(np.arange(nt), 3), self.P.ravel())), shape=(nt, self.m))
        self.CT = self.C.T.tocsr()
        self.area = U.AREA
        self.w = np.asarray(s_a, dtype=float) ** 2 * U.L_SU_LS
        self.A = np.zeros(self.m)
        self.E = np.zeros(self.m)

    def B(self):
        A, P, S = self.A, self.P, self.S
        return A[P[:, 0]] * S[:, 0] + A[P[:, 1]] * S[:, 1] + A[P[:, 2]] * S[:, 2]

    def forza(self):
        return self.CT @ (self.B() / self.area)

    def tick(self):
        self.E -= 0.5 * self.forza()
        self.A += 0.5 * self.w * self.E
        self.A += 0.5 * self.w * self.E
        self.E -= 0.5 * self.forza()

    def energia_arco(self):
        return self.w * self.E * self.E / 2.0

    def energia_tri(self):
        B = self.B()
        return B * B / (2.0 * self.area)


# =====================================================================================
#   IL GENERATORE SPARSO
# =====================================================================================
def H_sparso(ii, jj, nn):
    """### `H = I - P_u + P_-` sulle `2m` estremita' *(le estremita' `2k` su `ii`, `2k + 1` su `jj`)*, sparsa."""
    import scipy.sparse as sp
    m = len(ii)
    ext = [[] for _ in range(nn)]
    for k in range(m):
        ext[ii[k]].append(2 * k)
        ext[jj[k]].append(2 * k + 1)
    r, c, v = list(range(2 * m)), list(range(2 * m)), [1.0] * (2 * m)
    for e in ext:
        d = len(e)
        for a in e:
            for b in e:
                r.append(a)
                c.append(b)
                v.append(-1.0 / d)
    for k in range(m):
        a, b = 2 * k, 2 * k + 1
        r += [a, b, a, b]
        c += [a, b, b, a]
        v += [0.5, 0.5, -0.5, -0.5]
    return sp.csr_matrix((v, (r, c)), shape=(2 * m, 2 * m))


# =====================================================================================
#   LE COORDINATE DI RETICOLO E LA COPIA DAL TORO
# =====================================================================================
def reticolo(p):
    """### `p = m1 a1 + m2 a2`: `(m1, m2)` interi."""
    m2 = p[1] / A2[1]
    m1 = p[0] - m2 * A2[0]
    r = np.array([round(m1), round(m2)])
    assert np.max(np.abs(r - np.array([m1, m2]))) < 1e-9, "un punto fuori dal reticolo: %r" % (p,)
    return int(r[0]), int(r[1])


def tipo_arco(pu, pv):
    """### Il tipo `a` *(`0` a1, `1` a2, `2` a1 + a2)*, il nodo di partenza nel verso `+a` *(`0` = u, `1` = v)*, le coordinate di reticolo di quella partenza."""
    mu, mv = reticolo(pu), reticolo(pv)
    d = (mv[0] - mu[0], mv[1] - mu[1])
    tab = {(1, 0): 0, (0, 1): 1, (1, 1): 2}
    if d in tab:
        return tab[d], 0, mu
    dn = (-d[0], -d[1])
    assert dn in tab, "un arco che non e' del reticolo: %r" % (d,)
    return tab[dn], 1, mv


def carta_sorgente(p0):
    m2 = p0[1] / A2[1]
    m1 = p0[0] - m2 * A2[0]
    return m1, m2


def luce_iniziale(D, campo, W, b_y):
    """### Il pacchetto di `_u1_prototipo.pacchetto_campo` su un toro `L_TORO`, centrato; ### **copiato sugli archi del disco entro `D_COPIA` dalla sorgente.**"""
    import _u1_prototipo as U
    L = L_TORO
    ct = U.campo_toro((L, L), S_LUCE, E_LUCE, "noncompatto")
    bl = BL_LUCE[0]
    t0 = (2 * np.pi * N_K0 / L, -2 * np.pi * (N_K0 // 2) / L)
    U.pacchetto_campo(ct, bl, t0, W, (L / 2.0, L / 2.0), 2)
    p0 = np.array([X0, b_y])
    m01, m02 = carta_sorgente(p0)
    i0 = (int(round(m01)), int(round(m02)))
    campo.A[...] = 0
    campo.E[...] = 0
    for k in range(campo.m):
        if np.linalg.norm(D.pos_arco[k] - p0) > D_COPIA:
            continue
        pu, pv = D.lat_arco[k]
        a, da, mm = tipo_arco(pu, pv)
        M1 = (mm[0] - i0[0] + L // 2) % L
        M2 = (mm[1] - i0[1] + L // 2) % L
        kt = 3 * (M1 * L + M2) + a
        sg = 1.0 if da == 0 else -1.0
        campo.A[k] = sg * ct.A[kt]
        campo.E[k] = sg * ct.E[kt]
    return i0


def materia_iniziale(D, W, b_y):
    """### La busta `g e^{i k.r} u_k0` sul toro `L_TORO`, ### **proiettata ESATTAMENTE sulla banda alta** *(FFT; per ogni `k` l'autovettore di `_u1_terzo.H_gen`)*; ### **copiata sulle estremita' del disco entro `D_COPIA`.**"""
    import _u1_terzo as U3
    L = L_TORO
    # ### K in coordinate cartesiane: t1 = K.a1 = 2 pi/3, t2 = K.a2 = 2 pi/3
    Kc = np.linalg.solve(np.array([A1, A2]), np.array([2 * np.pi / 3, 2 * np.pi / 3]))
    kc = Kc + np.array([Q_MAT, 0.0])
    t0 = (float(kc @ A1), float(kc @ A2))
    lam0, V0 = np.linalg.eigh(U3.H_gen(*t0))
    u0 = V0[:, 0]                                  # ### lambda minimo = mu massimo: la banda alta
    m1, m2 = np.meshgrid(np.arange(L) - L // 2, np.arange(L) - L // 2, indexing="ij")
    r = m1[..., None] * A1 + m2[..., None] * A2
    g = np.exp(-np.sum(r * r, axis=-1) / (2 * W * W))
    fase = np.exp(1j * (t0[0] * m1 + t0[1] * m2))
    psi = g[..., None] * fase[..., None] * u0[None, None, :]
    F = np.fft.fft2(psi, axes=(0, 1))
    fuori = 0.0
    n = np.arange(L)
    for a in range(L):
        for c in range(L):
            # ### la fase di Bloch del modo (a, c) della FFT con l'origine a -L/2
            t1, t2 = 2 * np.pi * n[a] / L, 2 * np.pi * n[c] / L
            lam, V = np.linalg.eigh(U3.H_gen(t1, t2))
            u = V[:, 0]
            F[a, c] = u * np.vdot(u, F[a, c])
    psi = np.fft.ifft2(F, axes=(0, 1))
    # ### il controllo: la norma fuori dalla banda
    G = np.fft.fft2(psi, axes=(0, 1))
    tot = float(np.sum(np.abs(G) ** 2))
    for a in range(0, L, 8):
        for c in range(0, L, 8):
            lam, V = np.linalg.eigh(U3.H_gen(2 * np.pi * n[a] / L, 2 * np.pi * n[c] / L))
            fuori += float(np.sum(np.abs(V[:, 1:].conj().T @ G[a, c]) ** 2))
    fuori /= tot / 64.0
    p0 = np.array([X0, b_y])
    m01, m02 = carta_sorgente(p0)
    i0 = (int(round(m01)), int(round(m02)))
    x = np.zeros(2 * len(D.ii), dtype=complex)
    for k in range(len(D.ii)):
        if np.linalg.norm(D.pos_arco[k] - p0) > D_COPIA:
            continue
        pu, pv = D.lat_arco[k]
        a, da, mm = tipo_arco(pu, pv)
        # ### la partenza nel verso +a ha lo slot a, l'arrivo lo slot 3 + a
        mp = mm
        ma = (mm[0] + (1 if a in (0, 2) else 0), mm[1] + (1 if a in (1, 2) else 0))
        for (mx, slot) in ((mp, a), (ma, 3 + a)):
            M1 = (mx[0] - i0[0] + L // 2) % L
            M2 = (mx[1] - i0[1] + L // 2) % L
            h = 2 * k + (da if slot < 3 else 1 - da)
            x[h] = psi[M1, M2, slot]
    x /= np.linalg.norm(x)
    return x, fuori


# =====================================================================================
#   LE CORSE
# =====================================================================================
def finestre(t, xy, peso_in, peso_out):
    """### Le rette ai minimi quadrati nelle finestre: `theta_in`, `theta_out`, e i punti usati."""
    t, xy = np.asarray(t), np.asarray(xy)
    fin = np.asarray(peso_in) >= PERC_FINESTRA
    fout = (np.asarray(peso_out) >= PERC_FINESTRA) & (xy[:, 0] > 0.0)
    out = {"punti_in": int(fin.sum()), "punti_out": int(fout.sum())}
    if fin.sum() < 3 or fout.sum() < 3:
        out.update(theta_in=None, theta_out=None, delta=None)
        return out
    vin = np.polyfit(t[fin], xy[fin], 1)[0]
    vout = np.polyfit(t[fout], xy[fout], 1)[0]
    th_in, th_out = math.atan2(vin[1], vin[0]), math.atan2(vout[1], vout[0])
    out.update(theta_in=th_in, theta_out=th_out, delta=th_out - th_in, v_in=float(np.hypot(*vin)), v_out=float(np.hypot(*vout)))
    return out


def corsa_luce(D, db, b_y, W):
    campo = CampoGrafo(D.P, D.S, len(D.ii), np.full(len(D.ii), S_LUCE))
    luce_iniziale(D, campo, W, b_y)
    vicino_arco = (db[D.ii] <= D_BORDO) | (db[D.jj] <= D_BORDO)
    vicino_tri = vicino_arco[D.P].any(axis=1)
    tt, xy, pin, pout, guardia = [], [], [], [], 0.0
    H0 = float(campo.energia_arco().sum() + campo.energia_tri().sum())
    t, inizio_out, x_out0 = 0, None, None
    while True:
        ea, et = campo.energia_arco(), campo.energia_tri()
        tot = float(ea.sum() + et.sum())
        g = float((ea[vicino_arco].sum() + et[vicino_tri].sum()) / tot)
        guardia = max(guardia, g)
        c = (np.sum(ea[:, None] * D.pos_arco, axis=0) + np.sum(et[:, None] * D.pos_tri, axis=0)) / tot
        s_in = float((ea[np.isin(D.sett_arco, (2, 3))].sum() + et[np.isin(D.sett_tri, (2, 3))].sum()) / tot)
        s_out = float((ea[np.isin(D.sett_arco, (0, 1))].sum() + et[np.isin(D.sett_tri, (0, 1))].sum()) / tot)
        tt.append(t * S_LUCE)
        xy.append(c)
        pin.append(s_in)
        pout.append(s_out)
        if s_out >= PERC_FINESTRA and c[0] > 0.0:
            if inizio_out is None:
                inizio_out, x_out0 = t, c
            elif np.linalg.norm(c - x_out0) >= L_USCITA:
                break
        if g > GUARDIA_BORDO or t > 20000:
            break
        campo.tick()
        t += 1
    r = finestre(tt, xy, pin, pout)
    r.update(tick=t, guardia=guardia, deriva_energia=(tot - H0) / H0, fermata="uscita" if g <= GUARDIA_BORDO and t <= 20000 else "bordo")
    return r


def corsa_materia(D, db, Hs, b_y, W):
    import scipy.sparse.linalg as sla
    import scipy.sparse as sp
    x, fuori = materia_iniziale(D, W, b_y)
    A = (-1j) * (Hs - sp.identity(Hs.shape[0], format="csr"))
    nodo_h = np.empty(2 * len(D.ii), dtype=int)
    nodo_h[0::2] = D.ii
    nodo_h[1::2] = D.jj
    pos_h = D.pos[nodo_h]
    sett_h = D.sett[nodo_h]
    vicino = db[nodo_h] <= D_BORDO
    tt, xy, pin, pout, guardia = [], [], [], [], 0.0
    t, inizio_out, x_out0 = 0.0, None, None
    n0 = float(np.vdot(x, x).real)
    while True:
        w = np.abs(x) ** 2
        tot = float(w.sum())
        g = float(w[vicino].sum() / tot)
        guardia = max(guardia, g)
        c = np.sum(w[:, None] * pos_h, axis=0) / tot
        s_in = float(w[np.isin(sett_h, (2, 3))].sum() / tot)
        s_out = float(w[np.isin(sett_h, (0, 1))].sum() / tot)
        tt.append(t)
        xy.append(c)
        pin.append(s_in)
        pout.append(s_out)
        if s_out >= PERC_FINESTRA and c[0] > 0.0:
            if inizio_out is None:
                inizio_out, x_out0 = t, c
            elif np.linalg.norm(c - x_out0) >= L_USCITA:
                break
        if g > GUARDIA_BORDO or t >= T_MAX_MAT:
            break
        x = sla.expm_multiply(DT_MAT * A, x)
        t += DT_MAT
    r = finestre(tt, xy, pin, pout)
    r.update(tempo=t, guardia=guardia, norma=abs(tot - n0) / n0, fuori_banda=fuori, fermata="uscita" if g <= GUARDIA_BORDO and t < T_MAX_MAT else ("bordo" if g > GUARDIA_BORDO else "tempo"))
    return r


BL_LUCE = []


def controlli():
    """### Il controllo `0`."""
    import _u1_prototipo as U
    import _massa_nei_difetti as MD
    L = 12
    ct = U.campo_toro((L, L), S_LUCE, E_LUCE, "noncompatto")
    rng = np.random.default_rng(5)
    ct.A[...] = rng.normal(size=ct.m)
    ct.E[...] = rng.normal(size=ct.m)
    cg = CampoGrafo(ct.P, ct.S, ct.m, np.full(ct.m, S_LUCE))
    cg.A[...] = ct.A
    cg.E[...] = ct.E
    for _ in range(N_TICK_CONTROLLO):
        U.tick_campo(ct)
        cg.tick()
    dc = max(float(np.max(np.abs(cg.A - ct.A))), float(np.max(np.abs(cg.E - ct.E))))
    ii, jj, nn, _d = MD.toro(6)
    dg = float(np.max(np.abs(H_sparso(ii, jj, nn).toarray() - MD.H_diretto(ii, jj, nn))))
    return dc, dg


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _u1_prototipo as U
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA LUCE E LA MATERIA ATTORNO A UN CONO: il disco a settori (5 il cono, 6 il piatto), due fasci ai due lati, la convergenza")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_luce_materia_cono.py", "csv/_u1_prototipo.py", "csv/_u1_terzo.py", "csv/_massa_nei_difetti.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: R_DISCO %d X0 %g BB %s B_CONV %g S_LUCE %g L_TORO %d N_K0 %d W_LUCE %s Q_MAT %g W_MAT %s D_COPIA %g DT_MAT %g T_MAX_MAT %g PERC_FINESTRA %g L_USCITA %g D_BORDO %d GUARDIA_BORDO %g"
          % (R_DISCO, X0, BB, B_CONV, S_LUCE, L_TORO, N_K0, W_LUCE, Q_MAT, W_MAT, D_COPIA, DT_MAT, T_MAX_MAT, PERC_FINESTRA, L_USCITA, D_BORDO, GUARDIA_BORDO))
    print("  le tolleranze: TOLL_CAMPO %g TOLL_GEN %g TOLL_BANDA %g TOLL_PI3 %g TOLL_EP %g TOLL_CHIAVE %g; il piatto: |delta| <= 0.1/(|k| W)" % (TOLL_CAMPO, TOLL_GEN, TOLL_BANDA, TOLL_PI3, TOLL_EP, TOLL_CHIAVE))
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    BL_LUCE.append(U.blocchi_campo(S_LUCE)[0])
    dc, dg = controlli()
    esito("DEVE PASSARE (0): il campo su grafo = _u1_prototipo.Campo per %d tick entro %g (toro 12)" % (N_TICK_CONTROLLO, TOLL_CAMPO), dc <= TOLL_CAMPO, "%.2e" % dc)
    esito("DEVE PASSARE (0): il generatore sparso = _massa_nei_difetti.H_diretto entro %g (toro 6)" % TOLL_GEN, dg <= TOLL_GEN, "%.2e" % dg)
    dischi = {}
    for n in (6, 5):
        D = Disco(n, R_DISCO)
        g = D.gradi()
        interni = ~D.bordo
        interni[0] = False
        due = np.bincount(D.P.ravel(), minlength=len(D.ii))
        bordo_arco = D.bordo[D.ii] & D.bordo[D.jj]
        ok = g[0] == n and bool(np.all(g[interni] == 6)) and bool(np.all(due[~bordo_arco] == 2)) and bool(np.all(due[bordo_arco] == 1))
        esito("DEVE PASSARE (0): il disco a %d settori: il centro a %d, l'interno a 6, ogni arco interno in due triangoli, quelli di bordo in uno" % (n, n), ok,
              "nodi %d, archi %d, triangoli %d" % (D.nn, len(D.ii), len(D.P)))
        dischi[n] = (D, D.dist_bordo(), H_sparso(D.ii, D.jj, D.nn))
    ris = []
    casi = [(n, "luce", b, W_LUCE[0]) for n in (6, 5) for b in BB] + [(n, "luce", B_CONV, W_LUCE[1]) for n in (6, 5)]
    casi += [(n, "materia", b, W_MAT[0]) for n in (6, 5) for b in BB] + [(n, "materia", B_CONV, W_MAT[1]) for n in (6, 5)]
    for n, chi, b, W in casi:
        D, db, Hs = dischi[n]
        coppia = {}
        for lato in (+1, -1):
            t0 = time.time()
            r = corsa_luce(D, db, lato * b, W) if chi == "luce" else corsa_materia(D, db, Hs, lato * b, W)
            r.update(disco=n, chi=chi, b=b, lato=lato, W=W, secondi=time.time() - t0)
            coppia[lato] = r
            scrivi(dict(r, tipo="corsa"))
            print("  %-7s disco %d b %4g W %4g lato %+d: theta_in %s theta_out %s delta %s (punti %d/%d; fermata %s; guardia %.1e; %.0f s)"
                  % (chi, n, b, W, lato, "%+.5f" % r["theta_in"] if r["theta_in"] is not None else "-", "%+.5f" % r["theta_out"] if r["theta_out"] is not None else "-",
                     "%+.5f" % r["delta"] if r["delta"] is not None else "-", r["punti_in"], r["punti_out"], r["fermata"], r["guardia"], r["secondi"]))
            sys.stdout.flush()
        conv = (coppia[-1]["delta"] - coppia[+1]["delta"]) if coppia[-1]["delta"] is not None and coppia[+1]["delta"] is not None else None
        ris.append({"disco": n, "chi": chi, "b": b, "W": W, "sopra": coppia[+1], "sotto": coppia[-1], "convergenza": conv})
        scrivi({"tipo": "convergenza", "disco": n, "chi": chi, "b": b, "W": W, "convergenza": conv})
        print("  ### %s disco %d b %g W %g: LA CONVERGENZA %s (pi/3 = %.5f)" % (chi, n, b, W, "%+.5f" % conv if conv is not None else "-", math.pi / 3))
    print("-" * 130)
    print("### I CRITERI")
    fb = max(r[l]["fuori_banda"] for r in ris if r["chi"] == "materia" for l in ("sopra", "sotto"))
    esito("DEVE PASSARE (0): il pacchetto di materia nella banda alta entro %g (sul toro, dopo la proiezione)" % TOLL_BANDA, fb <= TOLL_BANDA, "%.1e" % fb)
    gm = max(r[l]["guardia"] for r in ris for l in ("sopra", "sotto"))
    print("  la guardia del bordo, il massimo su tutte le corse: %.2e (la soglia di fermata %g: una corsa fermata dal bordo ha la sua finestra d'uscita fino a quel tick)" % (gm, GUARDIA_BORDO))

    def trova(n, chi, b, W):
        return [r for r in ris if r["disco"] == n and r["chi"] == chi and r["b"] == b and r["W"] == W][0]
    kL = 2 * np.pi * N_K0 / L_TORO
    ok1, nota1 = True, []
    for chi, k, W in (("luce", kL, W_LUCE[0]), ("materia", Q_MAT, W_MAT[0])):
        tol = 0.1 / (k * W)
        for b in BB:
            r = trova(6, chi, b, W)
            for lato in ("sopra", "sotto"):
                d = r[lato]["delta"]
                ok1 &= d is not None and abs(d) <= tol
                nota1.append("%s %g %s %s" % (chi[0], b, lato[:2], "%+.4f" % d if d is not None else "-"))
    esito("DEVE PASSARE (1): sul PIATTO |delta| <= 0.1/(|k| W) per i due fasci, la luce e la materia, a ogni b", ok1, "; ".join(nota1))
    cl = [trova(5, "luce", b, W_LUCE[0])["convergenza"] for b in BB]
    ok2 = all(c is not None and abs(c - math.pi / 3) / (math.pi / 3) <= TOLL_PI3 for c in cl)
    esito("PUO' FALLIRE (2): la LUCE sul cono: la convergenza pi/3 entro il %g%% a ogni b" % (100 * TOLL_PI3), ok2, " ".join("%+.5f" % c if c is not None else "-" for c in cl), deve=False)
    cm = [trova(5, "materia", b, W_MAT[0])["convergenza"] for b in BB]
    ok3 = all(a is not None and c is not None and abs(a - c) / abs(c) <= TOLL_EP for a, c in zip(cm, cl))
    esito("PUO' FALLIRE (3): la MATERIA sul cono: la convergenza uguale a quella della luce entro il %g%% a ogni b" % (100 * TOLL_EP), ok3, " ".join("%+.5f" % c if c is not None else "-" for c in cm), deve=False)
    ch = []
    for cc in (cl, cm):
        ch.append(cc[0] / cc[-1] if cc[0] is not None and cc[-1] is not None and cc[-1] != 0 else None)
    ok4 = all(x is not None and abs(x - 1.0) <= TOLL_CHIAVE for x in ch)
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA (4): la convergenza va come 1/b; la chiave: conv(b %g)/conv(b %g) entro il %g%% da 1, non %g" % (BB[0], BB[-1], 100 * TOLL_CHIAVE, BB[-1] / BB[0]),
          ok4, " ".join("%.4f" % x if x is not None else "-" for x in ch))
    print("### LA CONVERGENZA IN LARGHEZZA (b %g)" % B_CONV)
    for chi, Ws in (("luce", W_LUCE), ("materia", W_MAT)):
        v = [trova(5, chi, B_CONV, W)["convergenza"] for W in Ws]
        print("  %s: W %s -> %s" % (chi, Ws, " ".join("%+.5f" % x if x is not None else "-" for x in v)))
        scrivi({"tipo": "larghezza", "chi": chi, "W": list(Ws), "convergenza": v})
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
