# -*- coding: utf-8 -*-
r"""**LA DISTANZA IN PASSI** *(Luca `2026-11-20` `10:41` e `10:47`, D1 ed E1; la carta `doc/TASK_HISTORY/2026-11-20_nascita_energia_nulla.md`, sez. `6.1`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/distanza_passi.py > doc/referti_l2/distanza_passi.txt

**Lo strumento** *(da importare nelle corse MITOSI e C2-EXT)*: `passi(ii, jj, n, sorgente)` *(una visita in ampiezza: `scipy.sparse.csgraph`, i cammini non pesati)*; `anello(m1, m2, c, L, R)` *(i nodi ORIGINARI con la distanza dal centro in `[R - 0.5, R + 0.5)`, dalle POSIZIONI: fissati una volta)*; `misura(...)` -> **D1** *(per gli anelli `40` e `60`: la mediana, il minimo, il massimo dei passi)* **ed E1** *(il raggio in passi che contiene il `50%` e il `90%` della massa; la larghezza `w = sqrt(somma rho d^2 / somma rho)`: la MIA definizione, dichiarata)*. **La sorgente:** il nodo piu' vicino al baricentro della materia *(`toro.centro`)*.
**I casi noti** *(Q-A4)*: **(1) sul toro piatto `L 186` senza nascite i passi dal nodo centrale = la distanza esagonale** *(per lo scarto `(d1, d2)`: `max(|d1|, |d2|)` se `d1 d2 >= 0`, altrimenti `|d1| + |d2|`; il minimo sulle immagini del toro)* **AL PASSO, su TUTTI i nodi**; **(2) dopo una nascita FORZATA nel guscio** *(la divisione di `nascita_dentro_fuori.nasci` su un arco a circa `15` nodi dal centro)* **i passi verso l'anello `40` crescono di `0` o di `1`, mai di piu', e mai calano**; **(3) il caso che DEVE FALLIRE:** un arco TOLTO senza nodo nuovo *(il grafo perde un lato)*: i passi verso qualche nodo vicino crescono -- **con un arco in meno su un cammino minimo deve cambiare qualcosa** *(se non cambia niente la prova non vede la crescita)*.
**Accanto** *(nessuna attesa)*: D1 ed E1 sullo stato di C2 a `k 3000`.
"""
import os
import sys

import numpy as np
import scipy.sparse as sp
from scipy.sparse import csgraph

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "mattone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import nascita_dentro_fuori as ND  # noqa: E402  (aggiunge al percorso csv/, csv/solitone/)

ANELLI = (40.0, 60.0)


def passi(ii, jj, n, sorgente):
    A = sp.csr_matrix((np.ones(2 * len(ii)), (np.concatenate([ii, jj]), np.concatenate([jj, ii]))), shape=(n, n))
    d = csgraph.shortest_path(A, unweighted=True, indices=int(sorgente))
    assert np.all(np.isfinite(d)), "il grafo non e' connesso"
    return d.astype(np.int64)


def raggio(m1, m2, c, L):
    from solitone import toro as TO
    return np.hypot(*TO.scarti(m1, m2, c[0], c[1], L).T[:2])


def anello(m1, m2, c, L, R):
    r = raggio(m1, m2, c, L)
    return np.where((r >= R - 0.5) & (r < R + 0.5))[0]


def sorgente(m1, m2, rho, L):
    from solitone import toro as TO
    c = TO.centro(rho, m1, m2, L)[:2]
    return int(np.argmin(raggio(m1, m2, c, L))), c


def scala(d, rho):
    """### E1: il raggio in passi del `50%` e del `90%` della massa, e `w`."""
    o = np.argsort(d, kind="stable")
    cum = np.cumsum(rho[o]) / float(np.sum(rho))
    r50, r90 = int(d[o][np.searchsorted(cum, 0.5)]), int(d[o][np.searchsorted(cum, 0.9)])
    w = float(np.sqrt(np.sum(rho * d.astype(float) ** 2) / np.sum(rho)))
    return r50, r90, w


def misura(ii, jj, n, src, anelli, rho):
    d = passi(ii, jj, n, src)
    out = {}
    for R, nodi in anelli.items():
        x = d[nodi]
        out[R] = (float(np.median(x)), int(x.min()), int(x.max()))
    out["E1"] = scala(d, rho)
    return out, d


def esagonale(m1, m2, c1, c2, L):
    best = None
    for s1 in (-L, 0, L):
        for s2 in (-L, 0, L):
            d1 = ((np.asarray(m1) - c1 + L // 2) % L) - L // 2 + s1
            d2 = ((np.asarray(m2) - c2 + L // 2) % L) - L // 2 + s2
            h = np.where(d1 * d2 >= 0, np.maximum(np.abs(d1), np.abs(d2)), np.abs(d1) + np.abs(d2))
            best = h if best is None else np.minimum(best, h)
    return best


def main():
    import _presidio
    import _massa_nei_difetti as MD
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA DISTANZA IN PASSI (Luca 2026-11-20 10:41, 10:47): lo strumento e i suoi casi noti")
    print("=" * 130)
    esiti = []
    L = 186
    ii, jj, nn, dirs = MD.toro(L)
    v = np.arange(nn)
    m1, m2 = v // L, v % L
    c0 = (L // 2, L // 2)
    src0 = c0[0] * L + c0[1]
    d0 = passi(ii, jj, nn, src0)
    he = esagonale(m1, m2, c0[0], c0[1], L)
    ok1 = bool(np.array_equal(d0, he))
    print("### (1) il toro piatto L %d, la sorgente il nodo %s: i passi = la distanza esagonale su TUTTI i %d nodi: %s (il massimo %d)" % (L, c0, nn, ok1, int(d0.max())))
    esiti.append(("il caso noto (1): sul toro piatto i passi = la distanza esagonale AL PASSO su tutti i nodi", ok1))
    an = {R: anello(m1, m2, c0, L, R) for R in ANELLI}
    for R in ANELLI:
        x = d0[an[R]]
        print("    l'anello %.0f (%d nodi): i passi mediana %.1f, min %d, max %d" % (R, len(an[R]), np.median(x), x.min(), x.max()))
    # ------------------------------------------------------------------ (2) la nascita forzata nel guscio
    G = (ii, jj, nn, np.asarray(dirs, dtype=float))
    psi0 = np.zeros((2 * len(ii), 2), dtype=complex)
    phi0 = np.ones(2 * len(ii), dtype=complex)
    rm = raggio(m1, m2, c0, L)
    i0 = int(np.argmin(np.abs(rm - 15.0) + 10.0 * (m2 != c0[1])))
    a = 3 * i0
    with np.errstate(invalid="ignore", divide="ignore"):
        out = ND.nasci(G, psi0, phi0, a)
    ii2, jj2, nn2 = out[0][0], out[0][1], out[0][2]
    d2 = passi(ii2, jj2, nn2, src0)
    dd = d2[an[40.0]] - d0[an[40.0]]
    dtutti = d2[:nn] - d0
    ok2 = bool(np.all((dd == 0) | (dd == 1))) and bool(np.all(dtutti >= 0)) and bool(np.all(dtutti <= 1))
    print("### (2) la nascita forzata sull'arco %d (%d -> %d, a %.2f nodi dal centro): l'anello 40, i passi cambiati di %s; su tutti i nodi originari da %d a %d" % (
        a, ii[a], jj[a], rm[i0] + 0.5, {int(k): int(c) for k, c in zip(*np.unique(dd, return_counts=True))}, int(dtutti.min()), int(dtutti.max())))
    esiti.append(("il caso noto (2): dopo una nascita nel guscio i passi crescono di 0 o 1, mai di piu', mai calano", ok2))
    # ------------------------------------------------------------------ (3) DEVE FALLIRE: un arco tolto senza nodo nuovo
    keep = np.ones(len(ii), dtype=bool)
    keep[3 * src0] = False
    d3 = passi(ii[keep], jj[keep], nn, src0)
    cambia = int(np.sum(d3 != d0))
    print("### (3) DEVE FALLIRE: l'arco %d tolto (dalla sorgente): i nodi coi passi cambiati %d (cresciuti di al piu' %d)" % (3 * src0, cambia, int((d3 - d0).max())))
    esiti.append(("DEVE FALLIRE (3): un arco tolto sul cammino dalla sorgente cambia i passi di qualche nodo", cambia > 0))
    # ------------------------------------------------------------------ accanto: C2 a k 3000
    with np.load(os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "C2", "stato_03000.npz")) as d:
        rho = d["rho"].copy()
    s, cb = sorgente(m1.astype(float), m2.astype(float), rho, L)
    anC = {R: anello(m1, m2, cb, L, R) for R in ANELLI}
    M, _d = misura(ii, jj, nn, s, anC, rho)
    print("### accanto (nessuna attesa): C2 a k 3000, il baricentro (%.3f, %.3f), la sorgente il nodo %d; D1: %s; E1 (r50, r90, w in passi): %s" % (
        cb[0], cb[1], s, ", ".join("anello %.0f mediana %.1f [%d, %d]" % (R, *M[R]) for R in ANELLI), M["E1"]))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-118s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
