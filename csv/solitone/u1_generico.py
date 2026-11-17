# -*- coding: utf-8 -*-
r"""**LA U(1) SUL GRAFO GENERICO** *(il ramo `mitosi`, B3; mandato di Luca `2026-11-17` `16:38`; la carta `doc/MITOSI_era2_carta.md`, sez. `5` e `8`, punto `3`)*.

### **PERCHE':** `_u1_prototipo.Campo` ha **`m = 3 n` cablato** *(gli archi `a1`, `a2`, `a1 + a2` da ogni nodo, le placchette `3 v + a`, `ingressi = reshape(n, 3)`)*: **la U(1) di oggi NON PUO' crescere.**
**Qui lo STESSO campo** *(`A`, `E` per arco; `B` per placchetta; `spinta`, `deriva`, `V`, `K`, `div`, `u`: le formule di `_u1_prototipo.Campo`, riga per riga)* **su un grafo QUALUNQUE:**
- **le placchette dai TRIANGOLI del grafo** *(un ELENCO, non una formula)*: **ogni terna di nodi a due a due collegati**; **il verso ANTIORARIO dai vettori d'arco** *(`vec`, il segno del prodotto vettore)*; **il primo arco esce dalla SORGENTE del triangolo** *(il nodo da cui escono due dei suoi archi; un triangolo senza sorgente -- un ciclo orientato -- comincia dall'arco di indice minore, DICHIARATO)*; **le placchette ordinate per indice del primo arco.**
  **Sul toro questo da' le placchette di `_u1_prototipo` riga per riga** *(`su`: `3v, 3(v+a1)+1, 3v+2`, segni `+ + -`; `giu`: `3v+2, 3(v+a2), 3v+1`, segni `+ - -`)* **in un ORDINE diverso** *(per primo arco, invece di tutte le `su` e poi tutte le `giu`)*: **la dinamica e' AL BIT** *(ogni arco somma DUE placchette, e con due addendi l'ordine non conta)*; **`V` e' una somma su tutte le placchette e cambia di ordine: entro pochi ulp, DICHIARATO.**
- **`div` dalla matrice di incidenza** *(gli archi entranti e uscenti per nodo, nell'ordine dell'indice d'arco: sul toro e' l'ordine di `ingressi` e di `reshape(n, 3)`, AL BIT)*;
- ### **LA GEOMETRIA DEL TRIANGOLO E' UN ARRAY, NON UNA COSTANTE:** **`area` per placchetta e `hodge_a` *(`l / l*`)* per arco.** **Sul toro valgono `AREA` e `L_SU_LS`** *(i valori di `_u1_prototipo`, AL BIT)*; **dopo una nascita i triangoli NON sono piu' equilateri** *(i mezzi triangoli hanno lati `1/2`, `sqrt(3)/2`, `1`)*, **e i valori dei triangoli e degli archi NUOVI sono una DECISIONE** *(la stella di Hodge sul reticolo irregolare)*: ### **NESSUN DEFAULT: li passa chi chiama** *(`area_di`, `hodge_nuovi`)*.
- **`cresci`**: **`A`, `E`, `s_a`, `hodge_a`, `vec` seguono la permutazione degli archi** *(`dove` di `Incidenza.cresci`)*; **i valori NUOVI SOLO da chi chiama**; **l'area dei triangoli che SOPRAVVIVONO resta quella di prima** *(per insieme di nodi: i nodi non cambiano indice)*; **la cache della fattorizzazione di Gauss** *(`gauss_riuso`)* **si SVUOTA** *(la topologia e' cambiata: la cache e' per IDENTITA' del campo)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _u1_prototipo as U1  # noqa: E402  (FORME, AREA, L_SU_LS: RIPRESI)

FORME = U1.FORME


def _verso(vec, ii, a, x):
    """### il vettore dell'arco `a` letto da `x` verso l'altro capo."""
    return vec[a] if ii[a] == x else -vec[a]


class CampoGenerico(object):
    """### `A`, `E` per arco su un grafo QUALUNQUE triangolato *(ogni arco in DUE triangoli)*. ### **Nessun default:** `area_di(x, y, z)` da' l'area di ogni triangolo, `hodge_a` il `l / l*` di ogni arco."""

    def __init__(self, ii, jj, n, vec, e, forma, s_a, hodge_a, area_di):
        assert forma in FORME, "la forma del campo va dichiarata: %s" % (FORME,)
        self.n = int(n)
        self.ii = np.asarray(ii, dtype=np.int64).copy()
        self.jj = np.asarray(jj, dtype=np.int64).copy()
        self.m = len(self.ii)
        assert len(self.jj) == self.m
        self.e, self.forma = float(e), forma
        self.vec = np.asarray(vec, dtype=float)[:, :2].copy()
        self.s_a = np.asarray(s_a, dtype=float).copy()
        self.hodge_a = np.asarray(hodge_a, dtype=float).copy()
        assert self.vec.shape[0] == self.m and self.s_a.shape == (self.m,) and self.hodge_a.shape == (self.m,), "vec, s_a, hodge_a: uno per arco"
        self.w = self.s_a ** 2 * self.hodge_a
        self.A = np.zeros(self.m)
        self.E = np.zeros(self.m)
        self._topologia({}, area_di)

    # ------------------------------------------------------------------ la topologia
    def _placchetta(self, x, y, z, adj):
        ii, vec = self.ii, self.vec
        axy, axz = adj[x][y], adj[x][z]
        dy, dz = _verso(vec, ii, axy, x), _verso(vec, ii, axz, x)
        cr = float(dy[0] * dz[1] - dy[1] * dz[0])
        assert cr != 0.0, "il triangolo (%d, %d, %d) e' degenere: i vettori d'arco sono paralleli" % (x, y, z)
        cyc = [x, y, z] if cr > 0 else [x, z, y]
        archi = [adj[cyc[q]][cyc[(q + 1) % 3]] for q in range(3)]
        esce = [int(ii[archi[q]] == cyc[q]) for q in range(3)]           # ### l'arco q va nel verso del giro
        # ### la SORGENTE: il nodo da cui escono i due archi del triangolo che lo toccano
        sorg = [q for q in range(3) if esce[q] and not esce[(q - 1) % 3]]
        if sorg:
            r = sorg[0]
        else:
            r = int(np.argmin(archi))                                     # ### un ciclo orientato: DICHIARATO
        cyc = cyc[r:] + cyc[:r]
        archi = archi[r:] + archi[:r]
        segni = [1.0 if ii[archi[q]] == cyc[q] else -1.0 for q in range(3)]
        return tuple(cyc), archi, segni

    def _topologia(self, aree_vecchie, area_di):
        n, m, ii, jj = self.n, self.m, self.ii, self.jj
        adj = [dict() for _ in range(n)]
        for a in range(m):
            x, y = int(ii[a]), int(jj[a])
            assert x != y and y not in adj[x], "l'arco %d (%d, %d) e' un cappio o un doppione" % (a, x, y)
            adj[x][y] = a
            adj[y][x] = a
        terne = set()
        for a in range(m):
            x, y = int(ii[a]), int(jj[a])
            for z in adj[x].keys() & adj[y].keys():
                terne.add(tuple(sorted((x, y, z))))
        righe = sorted((self._placchetta(*t, adj) for t in terne), key=lambda r: r[1][0])
        F = len(righe)
        self.P = np.array([r[1] for r in righe], dtype=np.int64).reshape(F, 3)
        self.S = np.array([r[2] for r in righe], dtype=float).reshape(F, 3)
        self.cicli = [r[0] for r in righe]
        self.area = np.array([aree_vecchie[tuple(sorted(c))] if tuple(sorted(c)) in aree_vecchie else float(area_di(*c)) for c in self.cicli], dtype=float)
        assert np.all(self.area > 0.0), "un'area NON positiva"
        assert F == m - n, "le placchette sono %d e m - n = %d: il grafo NON e' una triangolazione del toro" % (F, m - n)
        # ### ogni arco in DUE placchette: (placchetta, segno), nell'ordine delle placchette
        piatto = self.P.ravel()
        quale = np.repeat(np.arange(F), 3)
        segno = self.S.ravel()
        ordine = np.argsort(piatto, kind="stable")
        conta = np.bincount(piatto, minlength=m)
        assert np.all(conta == 2), "%d archi NON stanno in due placchette" % int(np.sum(conta != 2))
        self.ap = quale[ordine].reshape(m, 2)
        self.asg = segno[ordine].reshape(m, 2)
        # ### la divergenza: entranti e uscenti per nodo, nell'ordine dell'indice d'arco
        self._ord_in = np.argsort(jj, kind="stable")
        self._cnt_in = np.bincount(jj, minlength=n)
        self._ord_out = np.argsort(ii, kind="stable")
        self._cnt_out = np.bincount(ii, minlength=n)

    # ------------------------------------------------------------------ le formule di `_u1_prototipo.Campo`
    def B(self):
        A, P, S = self.A, self.P, self.S
        return A[P[:, 0]] * S[:, 0] + A[P[:, 1]] * S[:, 1] + A[P[:, 2]] * S[:, 2]

    def g(self, B):
        if self.forma == "compatto":
            return np.sin(self.e * B) / (self.e * self.area)
        return B / self.area

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
            return float(np.sum((1.0 - np.cos(self.e * B)) / (self.e * self.e * self.area)))
        return float(np.sum(B * B / (2.0 * self.area)))

    def K(self):
        return float(np.sum(self.w * self.E * self.E / 2.0))

    def _somma(self, E, ordine, conta):
        """### la somma per nodo IN SEQUENZA, posizione per posizione *(`((0 + a0) + a1) + a2`: l'ordine di `sum(axis=1)` del prototipo, AL BIT; ### `np.add.reduceat` NON lo e', misurato)*."""
        out = np.zeros(self.n)
        inizi = np.concatenate([[0], np.cumsum(conta)[:-1]])
        x = E[ordine]
        for q in range(int(conta.max()) if conta.size else 0):
            chi = conta > q
            out[chi] += x[inizi[chi] + q]
        return out

    def div(self, E=None):
        """### `D_i = somma_{entra in i} E - somma_{esce da i} E`."""
        E = self.E if E is None else E
        return self._somma(E, self._ord_in, self._cnt_in) - self._somma(E, self._ord_out, self._cnt_out)

    def u(self):
        return np.exp(1j * (self.e * self.A))

    # ------------------------------------------------------------------ la crescita
    def cresci(self, dove, ii, jj, n, vec_nuovi, A_nuovi, E_nuovi, s_a_nuovi, hodge_nuovi, area_di):
        """### **Il campo segue `Incidenza.cresci`** *(`dove` la permutazione delle ESTREMITA'; `ii`, `jj`, `n` il grafo DOPO)*. ### **I valori degli archi nuovi** *(gli ULTIMI)* **e l'area dei triangoli nuovi: SOLO da chi chiama.**"""
        dove = np.asarray(dove)
        vecchio = self.m
        assert dove.shape == (2 * vecchio,), "`dove` ha %r posti e le estremita' di prima sono %d" % (dove.shape, 2 * vecchio)
        da = dove[0::2]
        vivo = da >= 0
        dove_a = da[vivo] // 2
        m2 = len(ii)
        nuove = m2 - int(vivo.sum())
        for nome, x in (("vec_nuovi", vec_nuovi), ("A_nuovi", A_nuovi), ("E_nuovi", E_nuovi), ("s_a_nuovi", s_a_nuovi), ("hodge_nuovi", hodge_nuovi)):
            assert np.asarray(x).shape[0] == nuove, "`%s` ha %d righe e nascono %d archi" % (nome, np.asarray(x).shape[0], nuove)
        ii, jj = np.asarray(ii, dtype=np.int64), np.asarray(jj, dtype=np.int64)
        assert np.array_equal(ii[dove_a], self.ii[vivo]) and np.array_equal(jj[dove_a], self.jj[vivo]), "gli archi sopravvissuti NON sono dove `dove` li manda"
        assert set(dove_a.tolist()) == set(range(m2 - nuove)), "gli archi nuovi NON sono gli ultimi"
        aree = {tuple(sorted(c)): a for c, a in zip(self.cicli, self.area)}

        def segue(vecchio_v, nuovi_v, forma):
            out = np.zeros((m2,) + forma, dtype=float)
            out[dove_a] = vecchio_v[vivo]
            out[m2 - nuove:] = np.asarray(nuovi_v, dtype=float).reshape((nuove,) + forma)
            return out
        self.A = segue(self.A, A_nuovi, ())
        self.E = segue(self.E, E_nuovi, ())
        self.s_a = segue(self.s_a, s_a_nuovi, ())
        self.hodge_a = segue(self.hodge_a, hodge_nuovi, ())
        self.vec = segue(self.vec, np.asarray(vec_nuovi, dtype=float)[:, :2], (2,))
        self.ii, self.jj, self.n, self.m = ii.copy(), jj.copy(), int(n), m2
        self.w = self.s_a ** 2 * self.hodge_a
        self._topologia(aree, area_di)
        for nome in ("gauss_riuso", "solitone.gauss_riuso"):
            GR = sys.modules.get(nome)
            if GR is not None and GR.CACHE["campo"] is self:
                GR.CACHE.update(campo=None, D=None, risolvi=None)
