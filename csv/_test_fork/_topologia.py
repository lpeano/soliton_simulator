# -*- coding: utf-8 -*-
"""LA FORMA DEL GRAFO -- istogramma, clustering, catene, regolarita'.

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_topologia.md (f6d54e9).
La QUARTA lettura e' stata misurata PRIMA (csv/_test_fork/_topologia_neonati.py, a5ec1df):
NON SCATTA -- i grado-2 non si allacciano (l'84 % e' ancora grado 2 dopo 2100 passi, mediana 2).
Quindi le misure qui sotto NON descrivono un transitorio, e si possono leggere.

NESSUN RUN: gli snapshot di _g6000 bastano. Uno alla volta in RAM.

LE MISURE
 1  ISTOGRAMMA COMPLETO dei gradi, bin logaritmici PIU' i gradi piccoli uno per uno: quanti picchi,
    quale frazione in ciascuno, e SE c'e' popolazione nella valle in mezzo;
 2  CLUSTERING (triangoli chiusi / possibili), DISTRIBUZIONE e non media, SEPARATO per gruppo di
    grado (A3c). Calcolato ESATTO su tutti i nodi, non campionato: costo misurato a parte;
 3  LE CATENE: componenti connesse del sottografo indotto sui SOLI grado-2. Per ognuna: lunghezza,
    e se i punti d'appoggio esterni sono nodi DIVERSI (ponte) o lo STESSO (coda);
 4  REGOLARITA': la lunghezza ha una scala caratteristica? quante catene per punto d'appoggio?
 5  UNA MISURA CHE LE QUATTRO LETTURE NON PREVEDEVANO, e va fatta perche' decide il significato di
    tutte: i nodi di grado alto sono ESATTAMENTE quelli presenti al primo snapshot? Se si', la
    bimodalita' non e' una forma emersa ma la CONDIZIONE INIZIALE piu' la regola di nascita.

I PRESIDI
 P0  il grado si RICALCOLA da i/j e si verifica contro `_deg`; si verifica che la matrice
     simmetrizzata dia lo STESSO grado (senno' ci sono archi doppi o auto-anelli);
 P3  A3c: mai una statistica sopra due popolazioni. Ogni gruppo di grado ha la sua riga;
 COSTO: si misura e si DICHIARA il tempo del clustering. Nessun campionamento (non serve).

NESSUN NOME. Si riporta la forma, coi numeri.
ASCII PURO.
"""
import gzip
import os
import pickle
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
ARCHIVIO = os.path.join(RADICE, "csv", "_test_fork", "_g6000")
PASSI = [600, 1800, 2700]
N_PRIMO = None            # riempito dal primo snapshot dell'archivio (passo 60)
GRUPPI = [("grado 2", 2, 2), ("grado 3-10", 3, 10), ("grado 11-100", 11, 100),
          ("grado > 100", 101, 10 ** 9)]


def carica(passo):
    p = os.path.join(ARCHIVIO, "scena_%06d.pkl.gz" % passo)
    with gzip.open(p, "rb") as f:
        at = pickle.load(f)["attrs"]
    n = len(at["eta"])
    i = np.asarray(at["i"])
    j = np.asarray(at["j"])
    deg_sal = np.asarray(at["_deg"])[:n]
    eta = np.asarray(at["eta"], float)[:n].copy()
    del at
    return n, i, j, deg_sal, eta


def matrice(n, i, j):
    A = sp.coo_matrix((np.ones(len(i), np.float32), (i, j)), shape=(n, n)).tocsr()
    A = ((A + A.T) > 0).astype(np.float32)
    A.setdiag(0)
    A.eliminate_zeros()
    return A


def triangoli(A, blocco=1000):
    """Triangoli per nodo, ESATTI: diag(A^3)/2, a blocchi di righe per non esplodere in memoria."""
    n = A.shape[0]
    t = np.zeros(n)
    for k in range(0, n, blocco):
        s = slice(k, min(k + blocco, n))
        t[s] = np.asarray(A[s].multiply(A[s] @ A).sum(1)).ravel() / 2.0
    return t


def pct(a, p):
    return float(np.percentile(a, p)) if len(a) else float("nan")


def istogramma(deg, n):
    print("   %-14s %-8s %-9s" % ("grado", "quanti", "frazione"))
    esatti = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    for d in esatti:
        c = int(np.sum(deg == d))
        if c:
            print("   %-14d %-8d %-9.4f" % (d, c, c / n))
    bordi = [11, 21, 41, 81, 161, 321, 641]
    for k in range(len(bordi) - 1):
        m = (deg >= bordi[k]) & (deg < bordi[k + 1])
        c = int(m.sum())
        print("   %-14s %-8d %-9.4f" % ("[%d, %d)" % (bordi[k], bordi[k + 1]), c, c / n))
    vuoti = [d for d in range(2, int(deg.max()) + 1) if not np.any(deg == d)]
    presenti = sorted(set(deg.tolist()))
    print("   -> gradi PRESENTI: %d valori distinti fra %d e %d"
          % (len(presenti), int(deg.min()), int(deg.max())))
    if vuoti:
        # la VALLE: il piu' lungo intervallo di gradi senza nemmeno un nodo
        best = (0, None)
        run = [vuoti[0]]
        for d in vuoti[1:]:
            if d == run[-1] + 1:
                run.append(d)
            else:
                if len(run) > best[0]:
                    best = (len(run), (run[0], run[-1]))
                run = [d]
        if len(run) > best[0]:
            best = (len(run), (run[0], run[-1]))
        print("   -> LA VALLE piu' larga senza nemmeno un nodo: gradi %d..%d (%d valori consecutivi)"
              % (best[1][0], best[1][1], best[0]))
    print("   -> frazioni: grado 2 = %.4f | 3..10 = %.4f | 11..100 = %.4f | >100 = %.4f"
          % (np.mean(deg == 2), np.mean((deg >= 3) & (deg <= 10)),
             np.mean((deg >= 11) & (deg <= 100)), np.mean(deg > 100)))


def clustering(deg, tri):
    poss = deg * (deg - 1) / 2.0
    C = np.where(poss > 0, tri / np.maximum(poss, 1e-30), np.nan)
    print("   %-14s %-8s %-9s %-9s %-9s %-9s %-11s" %
          ("gruppo", "quanti", "C p25", "C p50", "C p75", "C max", "C == 0 %"))
    for nome, lo, hi in GRUPPI:
        m = (deg >= lo) & (deg <= hi)
        if not m.any():
            continue
        c = C[m]
        c = c[np.isfinite(c)]
        print("   %-14s %-8d %-9.4f %-9.4f %-9.4f %-9.4f %-11.1f"
              % (nome, int(m.sum()), pct(c, 25), pct(c, 50), pct(c, 75),
                 float(c.max()) if len(c) else float("nan"),
                 100.0 * float(np.mean(c == 0)) if len(c) else float("nan")))
    return C


def catene(A, deg):
    """Componenti connesse del sottografo indotto sui SOLI grado-2."""
    idx = np.flatnonzero(deg == 2)
    if len(idx) == 0:
        print("   nessun nodo di grado 2")
        return None
    S = A[idx][:, idx]
    ncomp, lab = connected_components(S, directed=False)
    dim = np.bincount(lab)
    # per ogni componente, i punti d'appoggio ESTERNI (vicini non di grado 2)
    dentro = np.zeros(A.shape[0], bool)
    dentro[idx] = True
    appoggi = [set() for _ in range(ncomp)]
    Ac = A.tocsr()
    for pos, nodo in enumerate(idx):
        vic = Ac.indices[Ac.indptr[nodo]:Ac.indptr[nodo + 1]]
        for v in vic:
            if not dentro[v]:
                appoggi[lab[pos]].add(int(v))
    nappoggi = np.array([len(a) for a in appoggi])
    print("   nodi di grado 2: %d   componenti (catene): %d" % (len(idx), ncomp))
    print("   lunghezza (nodi per catena): p25 %.0f  p50 %.0f  p75 %.0f  max %d   media %.3f"
          % (pct(dim, 25), pct(dim, 50), pct(dim, 75), int(dim.max()), float(dim.mean())))
    print("   %-14s %-8s %-9s" % ("lunghezza", "quante", "frazione"))
    for L in range(1, 9):
        c = int(np.sum(dim == L))
        if c:
            print("   %-14d %-8d %-9.4f" % (L, c, c / ncomp))
    c = int(np.sum(dim >= 9))
    if c:
        print("   %-14s %-8d %-9.4f" % (">= 9", c, c / ncomp))
    print("   PUNTI D'APPOGGIO ESTERNI per catena:")
    for k in (0, 1, 2, 3):
        c = int(np.sum(nappoggi == k))
        print("      %d appoggi: %-7d (%.4f)%s" % (k, c, c / ncomp,
              "   <- DIVERSI: la catena unisce due nodi distinti" if k == 2 else
              ("   <- LO STESSO nodo su entrambi i capi" if k == 1 else "")))
    c = int(np.sum(nappoggi >= 4))
    if c:
        print("      >=4 appoggi: %d (%.4f)" % (c, c / ncomp))
    # i gradi dei punti d'appoggio
    tutti = sorted(set().union(*appoggi)) if ncomp else []
    if tutti:
        da = deg[np.array(tutti)]
        print("   i punti d'appoggio sono %d nodi distinti, grado p25/p50/p75 = %.0f / %.0f / %.0f"
              % (len(tutti), pct(da, 25), pct(da, 50), pct(da, 75)))
        quante = np.bincount([v for a in appoggi for v in a], minlength=A.shape[0])
        q = quante[np.array(tutti)]
        print("   CATENE PER PUNTO D'APPOGGIO: p25 %.0f  p50 %.0f  p75 %.0f  max %d  (regolarita')"
              % (pct(q, 25), pct(q, 50), pct(q, 75), int(q.max())))
    return dict(idx=idx, lab=lab, dim=dim, nappoggi=nappoggi, appoggi=appoggi)


def main():
    global N_PRIMO
    n0, i0, j0, _, _ = carica(60)
    N_PRIMO = n0
    ARCHI0 = len(i0)
    print("il PRIMO snapshot dell'archivio (passo 60) ha n = %d nodi e %d archi"
          % (n0, ARCHI0))
    del i0, j0
    print("")

    for passo in PASSI:
        n, i, j, deg_sal, eta = carica(passo)
        A = matrice(n, i, j)
        deg = np.asarray(A.sum(1)).ravel().astype(np.int64)
        ok = int(np.sum(deg != deg_sal))
        print("=" * 118)
        print("PASSO %d   n = %d   archi = %d   [P0: deg(matrice) != _deg su %d nodi]"
              % (passo, n, A.nnz // 2, ok))
        print("=" * 118)
        if ok:
            print("  *** P0 FALLISCE: la matrice non riproduce il grado salvato. NON si legge. ***")
            return 2

        print("-- 1  L'ISTOGRAMMA COMPLETO DEI GRADI")
        istogramma(deg, n)
        print("")

        print("-- 2  IL CLUSTERING, esatto, separato per gruppo di grado (A3c)")
        t = time.time()
        tri = triangoli(A)
        dt = time.time() - t
        C = clustering(deg, tri)
        print("   COSTO MISURATO: %.2f s per %d nodi e %d archi. NESSUN CAMPIONAMENTO."
              % (dt, n, A.nnz // 2))
        print("")

        print("-- 3  LE CATENE (componenti indotte sui soli grado-2)")
        cat = catene(A, deg)
        print("")

        print("-- 5  I NODI DI GRADO ALTO SONO QUELLI DEL PRIMO SNAPSHOT?")
        vecchi = np.zeros(n, bool)
        vecchi[:min(n0, n)] = True
        alti = deg > 100
        print("   nodi con grado > 100: %d;  di questi, indice < %d (presenti al passo 60): %d (%.4f)"
              % (int(alti.sum()), n0, int((alti & vecchi).sum()),
                 (alti & vecchi).sum() / max(1, alti.sum())))
        print("   nodi presenti al passo 60: %d;  di questi, grado > 100: %d (%.4f);  grado 2: %d (%.4f)"
              % (int(vecchi.sum()), int((alti & vecchi).sum()),
                 (alti & vecchi).sum() / max(1, vecchi.sum()),
                 int(np.sum((deg == 2) & vecchi)),
                 np.sum((deg == 2) & vecchi) / max(1, vecchi.sum())))
        nati = ~vecchi
        if nati.any():
            print("   nodi NATI dopo il passo 60: %d;  grado 2: %.4f;  grado > 100: %.4f;  "
                  "grado p50 = %.0f"
                  % (int(nati.sum()), float(np.mean(deg[nati] == 2)),
                     float(np.mean(deg[nati] > 100)), pct(deg[nati], 50)))
        print("")
        del A, tri, C, cat, deg, eta, i, j

    print("=" * 118)
    print("-- 4  LA REGOLARITA' NEL TEMPO: archi contro nodi")
    print("=" * 118)
    print("%-8s %-9s %-11s %-13s %-13s" % ("passo", "n", "archi", "d(n) dal 60", "d(archi) dal 60"))
    for passo in [60] + PASSI:
        n, i, j, _, _ = carica(passo)
        print("%-8d %-9d %-11d %-13d %-13d" % (passo, n, len(i), n - n0, len(i) - ARCHI0))
        del i, j
    print("")
    print("UN SEME, UNA SCENA. Nessun nome, nessuna identificazione: si riportano grado, clustering,")
    print("lunghezze e punti d'appoggio.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
