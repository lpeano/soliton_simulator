# -*- coding: utf-8 -*-
"""LA DISTINZIONE CHE DECIDE, presa al livello giusto -- i due capi finiscono nello STESSO
addensamento o in DUE DIVERSI?

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_topologia.md (f6d54e9).

PERCHE' QUESTO SCRIPT ESISTE, e va detto: `_topologia.py` (a3bc6a22) ha misurato che il 100 % delle
catene ha DUE punti d'appoggio DISTINTI. Ma il mandato chiedeva un'altra cosa -- se i due capi
stanno in addensamenti DIVERSI (allora la catena UNISCE) o nello stesso (allora e' una CODA che
torna da dove viene). Due nodi distinti possono benissimo stare nello stesso addensamento: la mia
misura non distingueva i due casi. Questo script lo fa, ed e' una correzione a una misura mia.

LE MISURE
 1  gli ADDENSAMENTI: componenti connesse del sottografo indotto sui nodi di grado >= SOGLIA.
    Quante sono, quanto grandi, quanto dense (archi / possibili);
 2  gli ARCHI DIRETTI fra addensamenti diversi: gli addensamenti si toccano DA SOLI, o solo
    attraverso le catene?
 3  OGNI CATENA: i suoi due capi stanno nello STESSO addensamento o in DUE DIVERSI? E se un capo
    non appartiene a nessun addensamento, si conta a parte e NON si forza in una delle due caselle;
 4  se le catene uniscono addensamenti diversi: QUALI COPPIE, e quante catene per coppia.

LA SOGLIA NON E' SCELTA A MANO: l'istogramma misurato ha una VALLE VUOTA fra i gradi 11 e 40 (zero
nodi) e un'altra fra 226 e 495. Si prende il bordo della prima valle, cioe' grado >= 11, e si
RIPETE con >= 41 e >= 101 per mostrare che il risultato non dipende dalla soglia. Se dipendesse,
sarebbe quello il reperto.

NESSUN NOME. Si riportano componenti, dimensioni, densita' e conteggi.
ASCII PURO.
"""
import gzip
import os
import pickle
import sys

import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
ARCHIVIO = os.path.join(RADICE, "csv", "_test_fork", "_g6000")
PASSI = [600, 2700]
SOGLIE = [11, 41, 101]


def matrice(passo):
    p = os.path.join(ARCHIVIO, "scena_%06d.pkl.gz" % passo)
    with gzip.open(p, "rb") as f:
        at = pickle.load(f)["attrs"]
    n = len(at["eta"])
    i = np.asarray(at["i"])
    j = np.asarray(at["j"])
    del at
    A = sp.coo_matrix((np.ones(len(i), np.float32), (i, j)), shape=(n, n)).tocsr()
    A = ((A + A.T) > 0).astype(np.float32)
    A.setdiag(0)
    A.eliminate_zeros()
    deg = np.asarray(A.sum(1)).ravel().astype(np.int64)
    return A, deg, n


def pct(a, p):
    return float(np.percentile(a, p)) if len(a) else float("nan")


def main():
    for passo in PASSI:
        A, deg, n = matrice(passo)
        print("=" * 118)
        print("PASSO %d   n = %d   archi = %d" % (passo, n, A.nnz // 2))
        print("=" * 118)

        for soglia in SOGLIE:
            D = np.flatnonzero(deg >= soglia)
            if len(D) == 0:
                continue
            S = A[D][:, D]
            nc, lab = connected_components(S, directed=False)
            dim = np.bincount(lab)
            blocco = np.full(n, -1, np.int64)
            blocco[D] = lab
            print("-- 1  ADDENSAMENTI a soglia grado >= %d: %d nodi, %d componenti" % (soglia, len(D), nc))
            print("   %-6s %-8s %-11s %-11s %-9s %-9s" %
                  ("comp", "nodi", "archi int.", "possibili", "densita'", "grado p50"))
            ordine = np.argsort(-dim)
            for c in ordine[:12]:
                m = (lab == c)
                sub = S[m][:, m]
                e = sub.nnz // 2
                poss = m.sum() * (m.sum() - 1) // 2
                print("   %-6d %-8d %-11d %-11d %-9.4f %-9.0f"
                      % (c, int(m.sum()), e, poss, e / poss if poss else float("nan"),
                         pct(deg[D[m]], 50)))
            if nc > 12:
                print("   ... e altre %d componenti, dimensioni p50 = %.0f, max = %d"
                      % (nc - 12, pct(dim, 50), int(dim.max())))

            # -- 2  archi DIRETTI fra addensamenti diversi
            ii, jj = A.nonzero()
            sel = (ii < jj) & (blocco[ii] >= 0) & (blocco[jj] >= 0)
            fra = int(np.sum(sel & (blocco[ii] != blocco[jj])))
            dentro = int(np.sum(sel & (blocco[ii] == blocco[jj])))
            print("-- 2  archi DIRETTI fra nodi di addensamenti DIVERSI: %d   (dentro lo stesso: %d)"
                  % (fra, dentro))

            # -- 3  ogni catena: stesso addensamento o due diversi?
            idx = np.flatnonzero(deg == 2)
            if len(idx):
                Sc = A[idx][:, idx]
                ncc, labc = connected_components(Sc, directed=False)
                app = [set() for _ in range(ncc)]
                Ac = A.tocsr()
                d2 = np.zeros(n, bool)
                d2[idx] = True
                for pos, nodo in enumerate(idx):
                    for v in Ac.indices[Ac.indptr[nodo]:Ac.indptr[nodo + 1]]:
                        if not d2[v]:
                            app[labc[pos]].add(int(v))
                stesso = diversi = fuori = altro = 0
                coppie = {}
                for a in app:
                    b = sorted(set(blocco[list(a)].tolist())) if a else []
                    if len(a) != 2:
                        altro += 1
                    elif -1 in b:
                        fuori += 1
                    elif len(b) == 1:
                        stesso += 1
                    else:
                        diversi += 1
                        k = tuple(b)
                        coppie[k] = coppie.get(k, 0) + 1
                tot = ncc
                print("-- 3  LE %d CATENE, soglia >= %d:" % (tot, soglia))
                print("      capi nello STESSO addensamento : %-7d (%.4f)" % (stesso, stesso / tot))
                print("      capi in DUE addensamenti DIVERSI: %-7d (%.4f)" % (diversi, diversi / tot))
                print("      almeno un capo FUORI da ogni addensamento: %-7d (%.4f)"
                      % (fuori, fuori / tot))
                if altro:
                    print("      catene senza esattamente due capi: %-7d (%.4f)" % (altro, altro / tot))
                if coppie:
                    print("-- 4  le COPPIE di addensamenti unite, e quante catene ciascuna:")
                    for k in sorted(coppie, key=lambda x: -coppie[x])[:10]:
                        print("      %s : %d catene" % (str(k), coppie[k]))
                    print("      coppie distinte unite: %d" % len(coppie))
            print("")
        del A, deg
    print("UN SEME, UNA SCENA. Nessun nome: si riportano componenti, densita' e conteggi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
