# -*- coding: utf-8 -*-
r"""**IL CAMPO U(1) CON L'ORIENTAMENTO EREDITATO** *(D2 di Luca `2026-11-21` `23:13`; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md`, sez. `4.2`)*. [[PROGETTO-MITOSI]]

**`CampoOrientato`** = `u1_generico.CampoGenerico` *(importato, NON toccato: e' in uso)* **con UNA differenza:** il ciclo di ogni triangolo **NON si ricava dal prodotto vettoriale dei vettori d'arco: si LEGGE da `self.ori`** *(`{la terna ordinata: il ciclo canonico}`, lo STATO)*; **da li' in poi le righe di `_placchetta` di oggi** *(la sorgente, il primo arco, i segni)*. **Un triangolo senza orientamento ALZA** *(nessun default)*. **`cresci` vuole l'orientamento NUOVO intero** *(`ori=`: i triangoli del grafo dopo la crescita)*.
**`orientamento_da_vec(g)`:** l'orientamento di un `CampoGenerico` costruito coi vettori d'arco *(i suoi `cicli`: il verso antiorario)*: **si usa UNA volta, sul toro regolare** *(dove non ci sono degeneri)*.
**`vec` resta nel campo SOLO per il disegno:** nessuna riga di questo file lo legge.
"""
import os
import sys

import numpy as np

_RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for _p in (os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "csv", "solitone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import u1_generico as UG  # noqa: E402


def canonico(c):
    c = [int(x) for x in c]
    r = c.index(min(c))
    return tuple(c[r:] + c[:r])


def contiene(cyc, a, b):
    """### il ciclo `cyc` percorre `a -> b`?"""
    q = cyc.index(a)
    return cyc[(q + 1) % 3] == b


def orientamento_da_vec(g):
    """### l'orientamento dai cicli antiorari di un `CampoGenerico` *(UNA volta, sul toro regolare)*."""
    return {tuple(sorted(c)): canonico(c) for c in g.cicli}


class CampoOrientato(UG.CampoGenerico):
    def __init__(self, ii, jj, n, vec, e, forma, s_a, hodge_a, area_di, ori):
        self.ori = {tuple(sorted(k)): canonico(v) for k, v in ori.items()}
        UG.CampoGenerico.__init__(self, ii, jj, n, vec, e, forma, s_a, hodge_a, area_di)

    def _placchetta(self, x, y, z, adj):
        """### le righe di `CampoGenerico._placchetta` dopo la scelta del ciclo; ### il ciclo dallo STATO, non dal prodotto vettoriale."""
        ii = self.ii
        chiave = tuple(sorted((x, y, z)))
        assert chiave in self.ori, "il triangolo %s NON ha un orientamento: nessun default" % (chiave,)
        cyc = list(self.ori[chiave])
        archi = [adj[cyc[q]][cyc[(q + 1) % 3]] for q in range(3)]
        esce = [int(ii[archi[q]] == cyc[q]) for q in range(3)]
        sorg = [q for q in range(3) if esce[q] and not esce[(q - 1) % 3]]
        if sorg:
            r = sorg[0]
        else:
            r = int(np.argmin(archi))
        cyc = cyc[r:] + cyc[:r]
        archi = archi[r:] + archi[:r]
        segni = [1.0 if ii[archi[q]] == cyc[q] else -1.0 for q in range(3)]
        return tuple(cyc), archi, segni

    def _topologia(self, aree_vecchie, area_di):
        UG.CampoGenerico._topologia(self, aree_vecchie, area_di)
        assert len(self.ori) == len(self.cicli), "l'orientamento ha %d triangoli, il grafo %d" % (len(self.ori), len(self.cicli))

    def cresci(self, dove, ii, jj, n, vec_nuovi, A_nuovi, E_nuovi, s_a_nuovi, hodge_nuovi, area_di, ori=None):
        assert ori is not None, "la crescita vuole l'orientamento NUOVO (nessun default)"
        self.ori = {tuple(sorted(k)): canonico(v) for k, v in ori.items()}
        UG.CampoGenerico.cresci(self, dove, ii, jj, n, vec_nuovi, A_nuovi, E_nuovi, s_a_nuovi, hodge_nuovi, area_di)

    def ori_cicli(self):
        """### l'orientamento per lo stato salvato: i cicli canonici, ordinati."""
        return np.array(sorted(self.ori.values()), dtype=np.int64).reshape(-1, 3)


def da_cicli(arr):
    return {tuple(sorted(int(x) for x in c)): canonico(c) for c in np.asarray(arr)}


def orientato_da(g, ori):
    """### un `CampoGenerico` -> un `CampoOrientato` con gli STESSI archi, `A`, `E`, `s_a`, `hodge_a`, aree, `vec` *(il disegno)* e l'orientamento `ori`."""
    aree = {tuple(sorted(c)): a for c, a in zip(g.cicli, g.area)}
    h = CampoOrientato(g.ii, g.jj, g.n, g.vec, g.e, g.forma, g.s_a, g.hodge_a, lambda *c: aree[tuple(sorted(c))], ori)
    h.A[...] = g.A
    h.E[...] = g.E
    return h
