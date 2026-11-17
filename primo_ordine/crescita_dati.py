# -*- coding: utf-8 -*-
"""### LA CRESCITA DEI DATI DEL MOTORE oltre lo spinore *(il ramo `mitosi`, D-M1;
mandato di Luca `2026-11-17` `16:38`, B2)*.

### ⭐ **PERCHE' UN FILE A SE':** `motore.py` col corpo di queste funzioni arrivava a
**`760` righe**, oltre il tetto di `700` -- ### **oltre, SI DIVIDE, NON SI ALLUNGA.**

Prima di questo file `Motore.cresci` permutava SOLO `psi_h` e `phi_h`: ### **la
geometria (`n` per estremita', `U` per arco), `dtau`, `cs` e le chiavi PER NODO dello
stato restavano della taglia VECCHIA**, e un motore cresciuto le aveva sbagliate.

### ⛔ **NESSUN DEFAULT DI FISICA:** i valori dei posti NUOVI arrivano da chi chiama
*(`iniziali`: `geo_n`, `geo_U`, `dtau`, `cs`, `nodo:<nome>`)*, e ### **si controllano
TUTTI PRIMA di toccare qualunque cosa** -- una crescita rifiutata non lascia niente a
meta'. ### **Lo zero degli allocatori qui sotto NON e' una scelta:** ogni posto nuovo
e' scritto subito dopo.
"""
import sys

import numpy as np


def _attese(nome, nuove, nodi):
    """### Quante righe vuole la chiave `nome` di `iniziali`: un'estremita' per riga,
    salvo il trasporto `geo_U` *(un ARCO per riga)* e i dati PER NODO *(`dtau`, `cs`,
    `nodo:<nome>`: un nodo nuovo per riga)*."""
    if nome == "geo_U":
        return nuove // 2
    if nome in ("dtau", "cs") or nome.startswith("nodo:"):
        return nodi
    return nuove


def controlla(st, n, m, cs, nuove, nodi, iniziali):
    """### I controlli di `iniziali`, ### **PRIMA della crescita** *(`n`, `m`: il grafo
    di prima)*: la taglia di ogni chiave, la geometria nuova se nascono archi, e i dati
    per nodo *(ogni chiave per nodo dello stato, `dtau`, `cs` se il motore lo ha)* se
    nascono nodi."""
    if nuove:
        for nome in sorted(iniziali):
            a = np.asarray(iniziali[nome])
            attese = _attese(nome, nuove, nodi)
            assert a.shape[0] == attese, (
                "`iniziali[%r]` ha %d righe e ne servono %d: un valore iniziale della"
                " taglia sbagliata si propagherebbe in silenzio" % (nome, a.shape[0], attese))
        for nome in ("geo_n", "geo_U"):
            assert iniziali.get(nome) is not None, (
                "`iniziali` non porta %r: la geometria delle estremita' e degli archi nuovi"
                " e' una DECISIONE della legge, il motore non ha un default" % nome)
    if nodi:
        assert iniziali is not None, (
            "`cresci()` fa nascere %d nodi e `iniziali` e' `None`: i dati per nodo sono una"
            " DECISIONE, e `None` vuol dire <<nessuno ha deciso>>" % nodi)
        assert n != 2 * m, (
            "tanti nodi quante estremita': una chiave dello stato non dice se e' per nodo"
            " o per estremita'")
        for nome in sorted(st):
            if _per_nodo(st[nome], n):
                assert iniziali.get("nodo:" + nome) is not None, (
                    "`iniziali` non porta %r: la chiave per nodo %r DEVE dire con che valore"
                    " nasce sul nodo nuovo" % ("nodo:" + nome, nome))
        assert iniziali.get("dtau") is not None, (
            "`iniziali` non porta 'dtau': il tempo proprio del nodo nuovo e' un dato della"
            " legge")
        assert cs is None or iniziali.get("cs") is not None, (
            "`iniziali` non porta 'cs' e il motore ne ha uno: `cs` del nodo nuovo e' un dato"
            " della legge")


def _per_nodo(v, n):
    """### Una chiave dello stato e' PER NODO se e' un array con `n` righe *(il caso
    ambiguo `n = 2 m` e' rifiutato da `controlla`)*."""
    return isinstance(v, np.ndarray) and v.ndim >= 1 and v.shape[0] == n


def geometria(geo_n, geo_U, dove, vecchio, m, nuove, iniziali):
    """### Il versore `n` per estremita' e il trasporto `U` per arco ### **seguono la
    permutazione** `dove` *(di `Incidenza.cresci`; `vecchio` = le estremita' di prima,
    `m` = gli archi DOPO)*; i posti nuovi *(gli ULTIMI)* da `iniziali`."""
    vive = dove >= 0
    n_v = np.zeros((2 * m, 3))
    n_v[dove[vive]] = geo_n[:vecchio][vive]
    U_v = np.zeros((m, 2, 2), dtype=complex)
    arco_vivo = dove[0::2] >= 0
    U_v[dove[0::2][arco_vivo] // 2] = geo_U[:vecchio // 2][arco_vivo]
    if nuove:
        base = 2 * m - nuove
        n_v[base:base + nuove] = np.asarray(iniziali["geo_n"], dtype=float)
        U_v[base // 2:] = np.asarray(iniziali["geo_U"], dtype=complex)
    return n_v, U_v


def nodi(st, dtau, cs, n_dopo, nodi_nuovi, iniziali):
    """### I dati PER NODO *(i nodi nuovi sono gli ULTIMI: `Incidenza.cresci` aggiunge,
    non toglie)*: le chiavi per nodo dello stato **in posto nel dizionario**, e `dtau`,
    `cs` tornati."""
    prima = n_dopo - nodi_nuovi
    for nome in sorted(st):
        v = st[nome]
        if _per_nodo(v, prima):
            val = np.asarray(iniziali["nodo:" + nome], dtype=v.dtype)
            st[nome] = np.concatenate([v, val.reshape((nodi_nuovi,) + v.shape[1:])])
    dtau = np.concatenate([dtau, np.asarray(iniziali["dtau"], dtype=float)])
    if cs is not None:
        cs = np.concatenate([np.asarray(cs, dtype=float), np.asarray(iniziali["cs"], dtype=float)])
    return dtau, cs


def svuota_numba():
    """### La cache di `motore_numba` *(per `id` dell'indice)*: un indice nuovo la manca
    comunque, ma le voci vecchie si accumulerebbero. ### Il modulo assente e' legittimo
    *(numba spento)*."""
    mn = sys.modules.get("motore_numba")
    if mn is not None:
        mn._STATO["cache"].clear()
