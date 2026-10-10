# -*- coding: utf-8 -*-
"""LA SCENA DEL PROTOTIPO — **un grafo IRREGOLARE costruito SENZA `pos`.**

### ⛔ **NESSUNA POSIZIONE, da nessuna parte:** il grafo e' **solo liste di adiacenza**, e
l'unica nozione di distanza che esiste qui e' **il numero di archi** *(`A17`: nessun `pos`)*.

**Le due scene, dichiarate** *(`doc/TASK_HISTORY/2026-10-10_prototipo_camminata.md`)*:

| | la scena | perche' |
|---|---|---|
| `irregolare` | **`120` nodi, gradi fra `2` e `6`** | e' l'oggetto della prova |
| `regolare` | **`120` nodi, `4`-regolare** *(circolante)* | il **CONTROLLO**: dice che cosa e' colpa dell'irregolarita' e che cosa no |

### 📌 **LE ESTREMITA' D'ARCO sono la struttura portante:** l'arco `a` ha **due** estremita',
`2a` *(dal lato `u`)* e `2a+1` *(dal lato `v`)*, e lo **stato vive sulle estremita'**, non sui
nodi. ### **Lo spostamento scambia `2a` e `2a+1`**, e questo e' tutto cio' che fa.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))


def _niente_simulatore():
    """### ⛔ **IL CONTROLLO CHE IL BANCO NON IMPORTI IL SIMULATORE: guarda e FERMA.**"""
    cattivi = [m for m in sys.modules if "soliton_simulator" in m]
    if cattivi:
        raise SystemExit("[FERMO] il banco ha importato il simulatore: %r" % cattivi)
    return True


def irregolare(n=120, gmin=2, gmax=6, seme=11):
    """### Un grafo **connesso**, **irregolare**, **senza posizioni**.

    ### ⭐ **PRIMA UN ALBERO, POI GLI ARCHI IN PIU':** l'albero garantisce che il grafo sia
    ### **CONNESSO** *(e su un grafo sconnesso meta' delle letture non vorrebbe dire
    niente)*, e gli archi in piu' portano i gradi **dentro `[gmin, gmax]`**.

    ### ⚠ **E- DETERMINISTICO:** stesso `seme`, stesso grafo, **sempre**.
    """
    rng = np.random.default_rng(seme)
    archi = set()
    grado = np.zeros(n, dtype=int)

    def aggiungi(u, v):
        if u == v:
            return False
        a = (min(u, v), max(u, v))
        if a in archi or grado[u] >= gmax or grado[v] >= gmax:
            return False
        archi.add(a)
        grado[u] += 1
        grado[v] += 1
        return True

    # ------------------------------------------------- l'albero: il grafo e- CONNESSO
    for i in range(1, n):
        for _ in range(64):
            j = int(rng.integers(0, i))
            if aggiungi(i, j):
                break
        else:
            # ### ⛔ **SE NON CI RIESCE, FERMA:** un albero a meta- sarebbe
            # ### ### **un grafo sconnesso che SEMBRA una scena.**
            raise SystemExit("[FERMO] non riesco ad attaccare il nodo %d: gradi pieni" % i)

    # ------------------------------------------------- i gradi arrivano a `gmin`
    for giro in range(200):
        bassi = [int(k) for k in np.nonzero(grado < gmin)[0]]
        if not bassi:
            break
        for u in bassi:
            for _ in range(64):
                v = int(rng.integers(0, n))
                if grado[v] < gmax and aggiungi(u, v):
                    break
    assert int(grado.min()) >= gmin, ("i gradi non arrivano a %d: minimo %d"
                                      % (gmin, int(grado.min())))

    # ------------------------------------------------- un po- di archi in piu-
    # ### ⚠ **QUANTI: `n // 4`, e il numero e- DICHIARATO** -- serve solo a rendere i
    # ### gradi ### **diversi fra loro**, che e- cio- che <<irregolare>> vuol dire.
    for _ in range(n // 4):
        for _ in range(64):
            u = int(rng.integers(0, n))
            v = int(rng.integers(0, n))
            if aggiungi(u, v):
                break
    return costruisci(n, sorted(archi), "irregolare(n=%d,gmin=%d,gmax=%d,seme=%d)"
                      % (n, gmin, gmax, seme))


def regolare(n=120, salti=(1, 2)):
    """### Il CONTROLLO: un **circolante**, quindi **tutti i gradi uguali**."""
    archi = set()
    for i in range(n):
        for s in salti:
            u, v = i, (i + s) % n
            if u != v:
                archi.add((min(u, v), max(u, v)))
    return costruisci(n, sorted(archi), "regolare(n=%d,salti=%s)" % (n, salti))


def costruisci(n, archi, nome):
    """### La scena come **dizionario di array**, e nient'altro."""
    archi = [tuple(int(x) for x in a) for a in archi]
    m = len(archi)
    # ### il nodo di ogni ESTREMITA-: `2a` sta su `u`, `2a+1` sta su `v`
    nodo = np.zeros(2 * m, dtype=int)
    for a, (u, v) in enumerate(archi):
        nodo[2 * a] = u
        nodo[2 * a + 1] = v
    grado = np.bincount(nodo, minlength=n)
    assert int(grado.min()) >= 1, "c-e- un nodo senza archi: la scena non e- connessa"
    vicini = [[] for _ in range(n)]
    for u, v in archi:
        vicini[u].append(v)
        vicini[v].append(u)
    return {"nome": nome, "n": n, "m": m, "archi": tuple(archi), "nodo": nodo,
            "grado": grado, "vicini": tuple(tuple(x) for x in vicini)}


def distanze(sc, da):
    """### Le distanze **IN ARCHI** da un nodo: una `BFS`, e nessuna geometria."""
    d = np.full(sc["n"], -1, dtype=int)
    d[da] = 0
    bordo = [da]
    while bordo:
        nuovo = []
        for u in bordo:
            for v in sc["vicini"][u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    nuovo.append(v)
        bordo = nuovo
    return d


def ritmi(sc, seme):
    """### Gli `r_k`, **DATI** e non derivati, in `[1/2, 1]`.

    ### ⛔ **IL MANDATO LO DICE:** *«nel prototipo `r_k` e' dato (non derivato)»*. ### ⚠ **E
    la derivazione e' la domanda aperta** `DOMANDA-LAMBDA-GRANDEZZA`, non un pezzo di questo
    lavoro.
    """
    rng = np.random.default_rng(seme)
    return 0.5 + 0.5 * rng.random(sc["n"])


def rinumera(sc, seme):
    """### La STESSA scena con **nodi e archi rinumerati**, piu' le due mappe.

    ### ⭐ **E- la lettura `1`:** se la camminata e' isotropa, i due risultati
    ### **coincidono A MENO DELLA RINUMERAZIONE** -- e <<a meno della rinumerazione>> si
    verifica ### **applicando la mappa**, non a occhio.
    """
    rng = np.random.default_rng(seme)
    pn = rng.permutation(sc["n"])                 # nodo vecchio -> nodo nuovo
    archi_nuovi = []
    for (u, v) in sc["archi"]:
        a, b = int(pn[u]), int(pn[v])
        archi_nuovi.append((min(a, b), max(a, b)))
    pa = rng.permutation(sc["m"])                 # arco vecchio -> arco nuovo
    ordinati = [None] * sc["m"]
    for vecchio, nuovo in enumerate(pa):
        ordinati[int(nuovo)] = archi_nuovi[vecchio]
    nuova = costruisci(sc["n"], ordinati, sc["nome"] + "+rinumerata(%d)" % seme)
    # ### la mappa fra ESTREMITA-: `(arco, lato)` vecchio -> nuovo. ### ⚠ **Il lato
    # ### PUO- SCAMBIARSI**, perche- l-arco si riordina per `(min, max)`.
    mappa = np.zeros(2 * sc["m"], dtype=int)
    for vecchio, (u, v) in enumerate(sc["archi"]):
        nuovo = int(pa[vecchio])
        un, vn = int(pn[u]), int(pn[v])
        if un < vn:
            mappa[2 * vecchio] = 2 * nuovo
            mappa[2 * vecchio + 1] = 2 * nuovo + 1
        else:
            mappa[2 * vecchio] = 2 * nuovo + 1
            mappa[2 * vecchio + 1] = 2 * nuovo
    return nuova, pn, mappa


if __name__ == "__main__":
    _niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for sc in (irregolare(), regolare()):
        g = sc["grado"]
        print("  %-44s n=%d archi=%d gradi %d..%d (distinti: %d)"
              % (sc["nome"], sc["n"], sc["m"], g.min(), g.max(), len(set(g.tolist()))))
        d = distanze(sc, 0)
        print("     diametro dal nodo 0: %d archi" % int(d.max()))
