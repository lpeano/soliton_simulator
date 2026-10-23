# -*- coding: utf-8 -*-
r"""**TRIANGOLI, PRIMO GRADINO: LA SCENA A 6 VICINI E LA CAMMINATA SOLA, VERIFICATE.**

> ### ⛔ **Il task history e' `2026-10-21_triangoli_gradino1.md`** *(`ec9de266`)*; il progetto e'
> `doc/PROGETTO_TRIANGOLI.md` *(`a840e8f7`)*. Decisione di Luca del `2026-10-21` alle `17:53`:
> ### **`eps = 0.5`, la stessa di oggi: cambia UNA SOLA COSA, la connettivita'.**
> ### **SOLO LA CAMMINATA:** nessuna legge della materia gira sui triangoli qui.

## ⭐ IL COSTRUTTORE, GENERALE

Un toro su `lati` con ### **una lista di SPOSTAMENTI INTERI** *(gli archi propri del nodo)* e ### **un
versore 3D per spostamento.** L'arco `k = v d + a`; le estremita' `2k` *(sul nodo `v`, `+e_a`)* e
`2k + 1` *(sul vicino, `-e_a`)*: ### **la convenzione di `corrente.toro` e del progetto.**
### **Il passo NON si tocca:** `Incidenza`, `Motore` e i pezzi sono gia' per un grafo qualunque.

| | gli spostamenti | le direzioni |
|---|---|---|
| quadrato | `(1,0)`, `(0,1)` | `0`, `90` gradi |
| triangoli | `(1,0)`, `(0,1)`, `(1,1)` | `0`, `120`, `60` gradi |
| FCC *(base primitiva)* | `(1,0,0)`, `(0,1,0)`, `(0,0,1)`, `(1,-1,0)`, `(1,0,-1)`, `(0,1,-1)` | le `(+-1,+-1,0)/sqrt 2` |

Gira con:  python csv/_triangoli.py
"""
import io
import json
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

EPS = float(np.finfo(float).eps)
EPS_MONETA = 0.5               # la decisione di Luca delle 17:53: quella di oggi
LATO = 32
DTAU = 0.125
X = 0.1
VUOTO = 1.0
N_ESATTA = 800                 # N dtau = 100
N_NORMA = 200
SEME = 7
S3 = "CAMM-MATERIA-VUOTO"
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_gradino1.jsonl")
OK = [0, 0]


def _dir(gradi):
    a = np.deg2rad(gradi)
    return (float(np.cos(a)), float(np.sin(a)), 0.0)


QUADRATO = (((1, 0), (0, 1)), ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)))
TRIANGOLI = (((1, 0), (0, 1), (1, 1)), (_dir(0.0), _dir(120.0), _dir(60.0)))


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-72s %s   %s" % (che[:72], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


# =====================================================================================
#   IL COSTRUTTORE
# =====================================================================================
def toro_spostamenti(lati, spostamenti):
    """### `(ii, jj, nn)`: per ogni nodo, nell'ordine degli spostamenti, l'arco verso il vicino."""
    lati = tuple(int(a) for a in lati)
    nn = int(np.prod(lati))

    def indice(c):
        v = 0
        for a, cc in zip(lati, c):
            v = v * a + cc
        return v
    ii, jj = [], []
    for v in range(nn):
        c, r = [], v
        for a in reversed(lati):
            c.append(r % a)
            r //= a
        c = list(reversed(c))
        for s in spostamenti:
            ii.append(v)
            jj.append(indice([(cc + ds) % a for cc, ds, a in zip(c, s, lati)]))
    return (np.asarray(ii, dtype=np.int64), np.asarray(jj, dtype=np.int64), nn)


def versori(m, direzioni):
    d = len(direzioni)
    nv = np.zeros((2 * m, 3), dtype=float)
    for k in range(m):
        e = np.asarray(direzioni[k % d], dtype=float)
        nv[2 * k] = e
        nv[2 * k + 1] = -e
    return nv


def scena(griglia, lato, dtau, x):
    """### `(inc, mot, st, par)`: la materia uniforme allineata, il vuoto uniforme, `U = I`, ### **sul toro `lato x lato`** *(`scena_toro` a lati uguali)*."""
    return scena_toro(griglia, (lato, lato), dtau, x)


def scena_toro(griglia, lati, dtau, x):
    """### La scena su un toro con ### **lati DIVERSI lungo i due spostamenti di base** *(`lati = (L1, L2)`, via `toro_spostamenti`)*: ### **a lati uguali e' la
    `scena` di prima AL BIT** *(il controllo di servizio sta in `csv/_triangoli_forza.py`)*. ### **`dtau` scalare o per nodo.**"""
    import incidenza as IN
    import motore as MO
    import scena_l2 as SC
    import stato as ST
    spost, direz = griglia
    ii, jj, nn = toro_spostamenti(lati, spost)
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE), np.asarray(jj, dtype=IN.INDICE), nn,
                       capacita=len(ii))
    nv = versori(inc.m, direz)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    st["phi_h"][...] = VUOTO
    st["psi_h"][...] = float(np.sqrt(x)) * SC.spinore_allineato(nv)
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.broadcast_to(np.asarray(dtau, dtype=float), (nn,)).copy(), "numpy")
    return inc, mot, st, {"eps": EPS_MONETA}


def camminata(st, mot, par):
    import composizione as CM
    import tick as TK
    TK.percorri_tick(st, mot, par, (S3,), None, len(CM.ORDINE))


# =====================================================================================
#   LA CELLA E LA MATRICE DI UN TICK
# =====================================================================================
def celle(st, n, d):
    """### `(n, 6d)` complessi: le `2d` estremita' del nodo, `psi` (`4d`) e `phi` (`2d`)."""
    return np.concatenate([st["psi_h"].reshape(n, 4 * d), st["phi_h"].reshape(n, 2 * d)], axis=1)


def matrice_tick(griglia, lato, dtau):
    """### `A(k)` `(L, L, 6d, 6d)` della camminata sola, ESATTA (impulsi su base nulla)."""
    d = len(griglia[0])
    inc, mot, st, par = scena(griglia, lato, dtau, X)
    n = inc.n
    for k in st:
        st[k][...] = 0
    nc = 6 * d
    A = np.empty((lato, lato, nc, nc), dtype=complex)
    for c in range(nc):
        p = {k: v.copy() for k, v in st.items()}
        if c < 4 * d:
            p["psi_h"][c // 2, c % 2] = 1.0
        else:
            p["phi_h"][c - 4 * d] = 1.0
        camminata(p, mot, par)
        z = celle(p, n, d)
        A[:, :, :, c] = np.fft.fft2(z.reshape(lato, lato, nc), axes=(0, 1))
    return A


def ruota60(A):
    """### `A` ai `k` ruotati di `60` gradi: `(m_x, m_y) -> (-m_y, m_x + m_y)`."""
    L = A.shape[0]
    mx, my = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    return A[(-my) % L, (mx + my) % L]


def fasi(A):
    return np.sort(np.angle(np.linalg.eigvals(A)), axis=-1)


def scarto_c6(A):
    """### Lo scarto massimo fra le fasi per tick a `k` e a `k` ruotato (scala `pi`), ### **confrontate SUL CERCHIO.**

    ### ⛔ **LA CORREZIONE del difetto di `1e2437a9`:** ### **prima le fasi si ORDINAVANO, e un autovalore a `-1` esatto** *(fase `+-pi`)* ### **cambiava posto fra `-pi`
    e `+pi`: `3.14` invece di `~1e-15`.** ### **Ora gli autovalori a `k` e a `k` ruotato si accoppiano con l'assegnamento ungherese sulla distanza nel piano complesso**, ### **e lo
    scarto e' la fase relativa della coppia, avvolta** *(la stessa scala di prima: dove l'ordinamento accoppiava giusto, lo stesso numero entro l'arrotondamento, `<= 1e-14`)*."""
    from scipy.optimize import linear_sum_assignment
    la, lb = np.linalg.eigvals(A), np.linalg.eigvals(ruota60(A))
    peg = 0.0
    for i in np.ndindex(la.shape[:-1]):
        r, c = linear_sum_assignment(np.abs(la[i][:, None] - lb[i][None, :]))
        peg = max(peg, float(np.max(np.abs(np.angle(la[i][r] * np.conj(lb[i][c]))))))
    return peg


# =====================================================================================
#   IL GRAFO: BIPARTIZIONE E UN CICLO DISPARI
# =====================================================================================
def bipartito(ii, jj, nn):
    """### `(True, None)` se si colora in due; altrimenti `(False, un ciclo dispari)`."""
    vic = [[] for _ in range(nn)]
    for a, b in zip(ii.tolist(), jj.tolist()):
        vic[a].append(b)
        vic[b].append(a)
    col = [-1] * nn
    pad = [-1] * nn
    col[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        for w in vic[u]:
            if col[w] < 0:
                col[w] = 1 - col[u]
                pad[w] = u
                q.append(w)
            elif col[w] == col[u]:
                # ### il ciclo dispari: i due cammini fino all'antenato comune
                a_, b_ = [u], [w]
                while a_[-1] != 0:
                    a_.append(pad[a_[-1]])
                while b_[-1] != 0:
                    b_.append(pad[b_[-1]])
                sa = set(a_)
                comune = next(z for z in b_ if z in sa)
                ciclo = a_[:a_.index(comune) + 1] + list(reversed(b_[:b_.index(comune)]))
                return False, ciclo
    return True, None


# =====================================================================================
#   MAIN
# =====================================================================================
def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    import corrente as CO
    import scena_l2 as SC
    print("=" * 100)
    print("TRIANGOLI, PRIMO GRADINO: LA SCENA A 6 VICINI E LA CAMMINATA SOLA, VERIFICATE")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  il passo: %d pezzi, impronta %s (NON toccato); la camminata sola = senza %s, cs spento"
          % (len(CM.ORDINE), CM.IMPRONTA, S3))
    print("  lato %d, dtau %g, eps %g (decisione di Luca, 17:53); N %d (esattezza, invarianza),"
          " N %d (norma, seme %d); materia uniforme x %g, vuoto %g" % (LATO, DTAU, EPS_MONETA,
                                                                       N_ESATTA, N_NORMA, SEME,
                                                                       X, VUOTO))
    print("  triangoli: spostamenti %s, direzioni 0/120/60 gradi; quadrato: (1,0), (0,1)"
          % (TRIANGOLI[0],))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    fuori = {}

    print("### IL COSTRUTTORE SUL QUADRATO = scena_l2 AL BIT")
    ii_q, jj_q, nn_q = toro_spostamenti((LATO, LATO), QUADRATO[0])
    ii_o, jj_o, nn_o = CO.toro((LATO, LATO))
    nv_q = versori(len(ii_q), QUADRATO[1])
    nv_o = SC.versori_geometrici((LATO, LATO), len(ii_o))
    esito("il quadrato: ii, jj, nn e nv identici a corrente.toro e versori_geometrici",
          np.array_equal(ii_q, ii_o) and np.array_equal(jj_q, jj_o) and nn_q == nn_o
          and np.array_equal(nv_q, nv_o))
    print("-" * 100)

    print("### LA BIPARTIZIONE (deve fallire sui triangoli)")
    ii_t, jj_t, nn_t = toro_spostamenti((LATO, LATO), TRIANGOLI[0])
    bq, _cq = bipartito(ii_q, jj_q, nn_q)
    bt, ct = bipartito(ii_t, jj_t, nn_t)
    esito("il quadrato (lato %d pari) SI colora in due" % LATO, bq)
    esito("DEVE FALLIRE: i triangoli NON si colorano in due (un ciclo dispari)", not bt,
          "ciclo di %d nodi: %s" % (len(ct), ct) if ct else "")
    if bt:
        print("### STOP: il grafo triangolare risulta bipartito")
        return 1
    tri = [0, 1, LATO + 1]          # (0,0) -> (0,1) -> (1,1): un triangolo del grafo
    lati_tri = {(int(a), int(b)) for a, b in zip(ii_t, jj_t)}
    ha = lambda a, b: (a, b) in lati_tri or (b, a) in lati_tri
    esito("il triangolo (0,0)-(0,1)-(1,1) e' un ciclo di 3 archi del grafo",
          ha(tri[0], tri[1]) and ha(tri[1], tri[2]) and ha(tri[2], tri[0]),
          "nodi %s" % tri)
    print("-" * 100)

    print("### LO STATO DI MATERIA")
    inc, mot, st, par = scena(TRIANGOLI, LATO, DTAU, X)
    nv = mot.geo.n
    chi = st["psi_h"] / np.sqrt(X)
    sn = np.empty((nv.shape[0], 2, 2), dtype=complex)
    sn[:, 0, 0], sn[:, 0, 1] = nv[:, 2], nv[:, 0] - 1j * nv[:, 1]
    sn[:, 1, 0], sn[:, 1, 1] = nv[:, 0] + 1j * nv[:, 1], -nv[:, 2]
    dev = float(np.max(np.abs(np.einsum("hij,hj->hi", sn, chi) - chi)))
    esito("lo spinore allineato: sigma.n_h chi = chi entro 64 ulp", dev <= 64 * EPS, "%.3e" % dev)
    somma = np.zeros((inc.n, 3))
    np.add.at(somma, inc.nodo, nv)
    gradi = np.bincount(np.asarray(inc.nodo), minlength=inc.n)
    sz = float(np.max(np.abs(somma)))
    esito("le direzioni uscenti di ogni nodo (grado %s) sommano a zero" % sorted(set(gradi.tolist())),
          sz <= 64 * EPS, "max |somma| %.3e" % sz)
    print("-" * 100)

    print("### L'UNITARIETA' E L'ESATTEZZA DELLA CAMMINATA SOLA (triangoli)")
    rng = np.random.default_rng(SEME)
    st["psi_h"][...] = rng.normal(size=st["psi_h"].shape) + 1j * rng.normal(size=st["psi_h"].shape)
    st["phi_h"][...] = rng.normal(size=st["phi_h"].shape) + 1j * rng.normal(size=st["phi_h"].shape)
    n0 = float(np.sum(np.abs(st["psi_h"]) ** 2) + np.sum(np.abs(st["phi_h"]) ** 2))
    for _t in range(N_NORMA):
        camminata(st, mot, par)
    n1 = float(np.sum(np.abs(st["psi_h"]) ** 2) + np.sum(np.abs(st["phi_h"]) ** 2))
    dn = abs(n1 - n0) / n0
    esito("la norma su uno stato casuale, %d tick: entro N * 64 ulp" % N_NORMA,
          dn <= N_NORMA * 64 * EPS, "%.3e contro %.3e" % (dn, N_NORMA * 64 * EPS))
    t0 = time.time()
    A_t = matrice_tick(TRIANGOLI, LATO, DTAU)
    lam = np.linalg.eigvals(np.linalg.matrix_power(A_t, N_ESATTA))
    dev = float(np.max(np.abs(np.log(np.abs(lam)))))
    esito("ESATTA: ogni autovalore di A(k)^N (cella %d reali) ha modulo 1 entro N * 64 ulp"
          % (2 * A_t.shape[-1]), dev <= N_ESATTA * 64 * EPS,
          "%.3e contro %.3e  [%.0f s]" % (dev, N_ESATTA * 64 * EPS, time.time() - t0))
    print("-" * 100)

    print("### L'INVARIANZA PER TRASLAZIONE (la base uniforme, camminata sola, %d tick)" % N_ESATTA)
    inc, mot, st, par = scena(TRIANGOLI, LATO, DTAU, X)
    d = len(TRIANGOLI[0])
    peggio = 0.0
    for _t in range(N_ESATTA):
        camminata(st, mot, par)
        c = celle(st, inc.n, d)
        s = float(np.max(np.abs(c))) or 1.0
        peggio = max(peggio, float(np.max(np.abs(c - c[0]))) / (EPS * s))
    esito("la base uniforme resta uniforme entro 1e3 ulp", peggio <= 1e3, "%.1f ulp" % peggio)
    print("-" * 100)

    print("### L'ISOTROPIA C6 (la rotazione di 60 gradi di k)")
    s_t = scarto_c6(A_t)
    esito("i triangoli: le fasi a k e a k ruotato coincidono entro 64 ulp (scala pi)",
          s_t <= 64 * EPS * np.pi, "%.3e contro %.3e" % (s_t, 64 * EPS * np.pi))
    A_q = matrice_tick(QUADRATO, LATO, DTAU)
    s_q = scarto_c6(A_q)
    cieco = s_q <= 1e6 * 64 * EPS * np.pi
    esito("DEVE FALLIRE: il quadrato NON ha la simmetria di 60 gradi (scarto > 1e6 soglie)",
          not cieco, "%.3e" % s_q)
    if cieco:
        print("### STOP: il test di isotropia e' cieco")
        return 1
    om = -np.angle(np.linalg.eigvals(A_t)) / DTAU
    h = LATO // 2
    fuori.update({"lati": LATO, "dtau": DTAU, "eps": EPS_MONETA, "scarto_c6_triangoli": s_t,
                  "scarto_c6_quadrato": s_q, "esatta_dev": dev,
                  "omega_m0": [np.sort(om[m, 0]).tolist() for m in range(h + 1)],
                  "omega_mm": [np.sort(om[m, m]).tolist() for m in range(h + 1)]})
    print("  la dispersione dei triangoli (omega per unita' di tempo), lungo (m,0), m = 0, 4, .., %d:" % h)
    for m in range(0, h + 1, 4):
        print("     m %2d  %s" % (m, " ".join("%+.3f" % v for v in np.sort(om[m, 0]))))
    with io.open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(fuori) + "\n")
    print("=" * 100)
    print("### %d/%d prove passate. NESSUNA LEGGE DELLA MATERIA SUI TRIANGOLI." % tuple(OK))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
