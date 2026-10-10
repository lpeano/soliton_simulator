# -*- coding: utf-8 -*-
"""LA GEOMETRIA DEL `v2` — **riferimenti locali, connessione `U(2)`, e OLONOMIA.**

**Decisione di Luca, 2026-10-10** *(voce `SPIN-LEGATO-AL-MOTO`)*: su ogni arco orientato una
matrice `U_kj = e^{iθ_kj} V_kj` con `V ∈ SU(2)` e `U_jk = U_kj^†`; **`θ` e'
l'elettromagnetismo `U(1)`**, **`V` e' la connessione geometrica `SU(2)`**. Ogni nodo ha un
**riferimento locale**: a ogni estremita' uscente un versore `n_{k,a}` sulla sfera.

> ## ⛔ **I DUE VERSORI DI UN ARCO NON SONO ANTIPODALI, E NON E' UNA SVISTA.**
> Senza `pos` **non esiste** <<la direzione dell'arco>>: ogni nodo ha **il suo** riferimento, e
> ### **la relazione fra i due riferimenti E' LA CONNESSIONE.** Imporre `n_{a,k} = −n_{k,a}`
> vorrebbe dire **posare un'immersione** — cioe' far rientrare dalla finestra il `pos` che
> `A17` ha buttato dalla porta.

### ⚠ **E I VERSORI SONO UNA SCELTA PROVVISORIA DICHIARATA** *(voce
`PROVV-VERSORI-NON-RELAZIONALI`)*: sono **dati**, distribuiti **isotropi** *(sfera di
Fibonacci)*, e la loro **origine relazionale** e' `DOMANDA-D9-GEOMETRIA`.

### ⭐ **LA CURVATURA E' L'OLONOMIA:** il prodotto delle `U` lungo un ciclo chiuso. **Si LEGGE**
*(la parte `SU(2)` dalla traccia, la parte `U(1)` dal determinante)*, e in questo banco
**non cambia mai**, perche' le `U` sono fisse — ed e' la lettura `O`, che e' **un controllo**.

Gira con:  python proto_camminata/geometria.py
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import scena as SC                                             # noqa: E402

# ### le tre matrici di Pauli, una volta sola
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = (SX, SY, SZ)
I2 = np.eye(2, dtype=complex)
# ### ⭐ **`i sigma_y`, cioe- l-operatore di CONIUGAZIONE DI CARICA senza il coniugio.**
ISY = 1j * SY


def versori_fibonacci(d):
    """### `d` punti **quasi uniformi** sulla sfera, **deterministici**.

    ### ⚠ **Niente `RNG`:** la sfera di Fibonacci e' una **formula**, quindi
    ### **due processi danno gli stessi byte** senza dover passarsi un seme.
    """
    fuori = np.zeros((d, 3), dtype=float)
    oro = math.pi * (3.0 - math.sqrt(5.0))
    for i in range(d):
        z = 1.0 - 2.0 * (i + 0.5) / d
        rr = math.sqrt(max(0.0, 1.0 - z * z))
        fi = oro * i
        fuori[i] = (rr * math.cos(fi), rr * math.sin(fi), z)
    return fuori


def versori(sc):
    """### Un versore per **ESTREMITA'**, assegnato in **ordine di indice d'arco.**

    ### ⛔ **L'assegnazione e' DICHIARATA, non casuale:** le estremita' di un nodo si
    prendono **in ordine crescente di indice**, e ricevono i punti di Fibonacci
    **nello stesso ordine**. ### **Cosi' la scena e' una FUNZIONE del grafo**, e due
    processi non possono divergere.
    """
    n, m = sc["n"], sc["m"]
    per = [[] for _ in range(n)]
    for e in range(2 * m):
        per[int(sc["nodo"][e])].append(e)
    fuori = np.zeros((2 * m, 3), dtype=float)
    for k in range(n):
        ee = sorted(per[k])
        punti = versori_fibonacci(len(ee))
        for i, e in enumerate(ee):
            fuori[e] = punti[i]
    return fuori


def su2_casuale(rng, quante):
    """### `SU(2)` **uniforme**: un quaternione unitario, che e' la stessa cosa.

    ### ⭐ **E- qui che la DOPPIA COPERTURA si vede** *(`DOPPIA-COP`)*: `q` e `−q` danno
    ### **la stessa rotazione di `SO(3)`** e ### **due matrici di `SU(2)` diverse**.
    """
    q = rng.standard_normal((quante, 4))
    q /= np.linalg.norm(q, axis=1).reshape(-1, 1)
    fuori = np.zeros((quante, 2, 2), dtype=complex)
    for i in range(quante):
        fuori[i] = (q[i, 0] * I2 + 1j * (q[i, 1] * SX + q[i, 2] * SY + q[i, 3] * SZ))
    return fuori


def rotazione(g):
    """### La rotazione `SO(3)` di un `g ∈ SU(2)`: `R_ij = ½ tr(σ_i g σ_j g^†)`.

    ### ⛔ **Serve a RUOTARE I VERSORI in una trasformazione di gauge**, ed e' il pezzo
    senza il quale la moneta di spin **non sarebbe covariante** — cioe' il pezzo che rende
    i riferimenti locali **necessari** invece che decorativi.
    """
    R = np.zeros((3, 3), dtype=float)
    gd = g.conj().T
    for i in range(3):
        for j in range(3):
            R[i, j] = 0.5 * float(np.real(np.trace(PAULI[i] @ g @ PAULI[j] @ gd)))
    return R


# =====================================================================================
#   LE TRE SCENE -- dichiarate, e FISSE (voce `PROVV-U-FISSE-TRE-SCENE`)
# =====================================================================================
def scena_identita(sc):
    """### `U = I` su ogni arco: ### **nessuna connessione, nessun campo.**"""
    U = np.zeros((sc["m"], 2, 2), dtype=complex)
    U[:] = I2
    return {"nome": "identita", "U": U, "n": versori(sc),
            "come": "U = I su ogni arco: nessun campo e nessuna connessione"}


def scena_gauge_puro(sc, seme):
    """### `V_kj = g_k g_j^†` e `θ_kj = φ_k − φ_j`: ### **tutte le olonomie BANALI.**

    ### ⭐ **E- la scena che PROVA una cosa invece di mostrarla:** se le osservabili
    invarianti coincidono con quelle dell'identita' **soltanto quando si ruotano anche i
    versori**, allora ### **i riferimenti locali non sono ridondanti.**
    """
    rng = np.random.default_rng(seme)
    g = su2_casuale(rng, sc["n"])
    fi = rng.random(sc["n"]) * 2.0 * math.pi
    U = np.zeros((sc["m"], 2, 2), dtype=complex)
    nn = versori(sc)
    for a, (u, v) in enumerate(sc["archi"]):
        # ### il trasporto da `u` a `v` di una trasformazione di gauge pura
        U[a] = math.e ** (1j * (fi[v] - fi[u])) * (g[v] @ g[u].conj().T)
    # ### ⛔ **E I VERSORI SI RUOTANO col gauge**, perche- il riferimento locale
    # ### ### **E- un oggetto che ruota**: `n -> R(g_k) n`.
    nruot = nn.copy()
    for e in range(2 * sc["m"]):
        k = int(sc["nodo"][e])
        nruot[e] = rotazione(g[k]) @ nn[e]
    return {"nome": "gauge_puro", "U": U, "n": nruot, "n_non_ruotati": nn,
            "g": g, "fi": fi,
            "come": "V = g_k g_j^dagger e theta = fi_k - fi_j: olonomie TUTTE banali"}


def scena_curva(sc, seme):
    """### `U` casuali in `U(2)`: ### **olonomie NON banali** — curvatura vera."""
    rng = np.random.default_rng(seme + 1000)
    V = su2_casuale(rng, sc["m"])
    th = rng.random(sc["m"]) * 2.0 * math.pi
    U = np.zeros((sc["m"], 2, 2), dtype=complex)
    for a in range(sc["m"]):
        U[a] = np.exp(1j * th[a]) * V[a]
    return {"nome": "curva", "U": U, "n": versori(sc),
            "come": "U casuali in U(2): olonomie NON banali"}


def u_di_estremita(sc, U, e):
    """### La `U` che trasporta **l'estremita' `e` verso il suo partner.**

    ### ⛔ **`U_jk = U_kj^†`**, e qui si vede: l'estremita' **pari** *(dal lato `u`)* usa
    `U`, quella **dispari** *(dal lato `v`)* usa `U^†`.
    """
    a = e // 2
    return U[a] if (e % 2 == 0) else U[a].conj().T


# =====================================================================================
#   L'OLONOMIA -- si LEGGE
# =====================================================================================
def cicli_corti(sc, quanti=12):
    """### I cicli piu' corti, uno per arco **fuori dall'albero di `BFS`.**

    ### ⚠ **Non e' <<tutti i cicli>>:** e' **una base**, e basta a dire se le olonomie
    sono banali.
    """
    n = sc["n"]
    padre = [-1] * n
    liv = [-1] * n
    liv[0] = 0
    bordo = [0]
    arco_di = {}
    for a, (u, v) in enumerate(sc["archi"]):
        arco_di[(u, v)] = a
        arco_di[(v, u)] = a
    albero = set()
    while bordo:
        nuovo = []
        for u in bordo:
            for v in sc["vicini"][u]:
                if liv[v] < 0:
                    liv[v] = liv[u] + 1
                    padre[v] = u
                    albero.add(arco_di[(u, v)])
                    nuovo.append(v)
        bordo = nuovo

    def su(k):
        c = [k]
        while padre[c[-1]] >= 0:
            c.append(padre[c[-1]])
        return c

    fuori = []
    for a, (u, v) in enumerate(sc["archi"]):
        if a in albero:
            continue
        cu, cv = su(u), su(v)
        comune = set(cv)
        taglio = next((x for x in cu if x in comune), 0)
        ciclo = cu[:cu.index(taglio) + 1] + list(reversed(cv[:cv.index(taglio)]))
        if len(ciclo) >= 3:
            fuori.append(ciclo)
        if len(fuori) >= quanti:
            break
    return fuori


def olonomia(sc, U, ciclo):
    """### `(traccia della parte SU(2), fase U(1))` del prodotto lungo il ciclo."""
    arco_di = {}
    for a, (u, v) in enumerate(sc["archi"]):
        arco_di[(u, v)] = 2 * a
        arco_di[(v, u)] = 2 * a + 1
    M = I2.copy()
    for i in range(len(ciclo)):
        u = ciclo[i]
        v = ciclo[(i + 1) % len(ciclo)]
        M = u_di_estremita(sc, U, arco_di[(u, v)]) @ M
    det = complex(np.linalg.det(M))
    fase = 0.5 * float(np.angle(det))
    V = M * np.exp(-1j * fase)
    return float(np.real(np.trace(V))), fase


def olonomie(sc, U, quanti=12):
    """### Le olonomie dei cicli corti: `[(lunghezza, traccia, fase)]`."""
    return [(len(c),) + olonomia(sc, U, c) for c in cicli_corti(sc, quanti)]


if __name__ == "__main__":
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = SC.irregolare()
    nn = versori(sc)
    print("  versori: %d, |n| = %.17g (min) .. %.17g (max)"
          % (len(nn), float(np.min(np.linalg.norm(nn, axis=1))),
             float(np.max(np.linalg.norm(nn, axis=1)))))
    for s in (scena_identita(sc), scena_gauge_puro(sc, 11), scena_curva(sc, 11)):
        ol = olonomie(sc, s["U"])
        tr = [x[1] for x in ol]
        fa = [x[2] for x in ol]
        print("  %-12s %-58s" % (s["nome"], s["come"]))
        print("     %d cicli (lunghezze %s): traccia SU(2) in [%.6f, %.6f], |fase U(1)| "
              "max %.3g" % (len(ol), sorted(set(x[0] for x in ol)),
                            min(tr), max(tr), max(abs(x) for x in fa)))
