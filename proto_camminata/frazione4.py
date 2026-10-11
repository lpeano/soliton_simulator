# -*- coding: utf-8 -*-
r"""LA FRAZIONE DI UN'INVOLUZIONE — **UNA famiglia per TUTTI E QUATTRO i pezzi discreti.**

> ## ⭐ **E IL MANDATO NE CHIEDEVA DUE: una per Grover e una per lo spostamento.**
> ## ### **Non servono.** Misurato *(task history del `2026-10-11`, `2.1`)*: tutti e quattro
> ## i pezzi discreti del `v3` sono ### **INVOLUZIONI ERMITIANE** — `max|M^2 - I|` da **`0`**
> ## a **`5.55e-16`**, `max|M - M^dag|` ### **`0` per tutti e quattro.**

Un'involuzione ermitiana `X` si scrive `X = 2Q - I` con `Q = (I + X)/2` **proiettore**, e
allora la frazione si costruisce **una volta sola**:

| | la forma | `X(0)` | `X(1)` |
|---|---|---|---|
| `A` | **del mandato**: `e^{i pi cs} e^{i pi cs Q}` = `z (psi + (z-1) Q psi)` | `I` | `X` |
| `B` | **senza fase globale**: `Q + e^{i pi cs}(I - Q)` = `Q psi + z (psi - Q psi)` | `I` | `X` |

### ⭐ **E SERVE UNA SOLA APPLICAZIONE DI `X`:** `Q psi = (psi + X psi)/2`. ### **Quindi la
frazione e' LOCALE esattamente come il pezzo che frazione** — niente matrici, niente
autovettori.

> ## ⛔ **IL CORTOCIRCUITO NON E' UN'OTTIMIZZAZIONE: E' `W1`.** A `cs = 1` la famiglia da'
> ## `X` a **`2e-16`**, e ### **`2e-16` NON E' `0`**: il vincolo `W1` pretende il `v3`
> ## ### **AL BIT**. ### **Quindi a `cs` identicamente `1` si restituisce `X psi`**, e a
> ## `cs` identicamente `0` si restituisce `psi`. ### ⚠ **E con un `cs` MISTO non c'e'
> ## cortocircuito**: dove `cs == 1` il risultato e' `X psi` a meno di `~1e-16`, e
> ## ### **questo si misura invece di tacerlo** *(`scarto_a_uno`)*.

### ⛔ **E LA `C` SI ROMPE, per un conto e non per un difetto** *(task history, `2.3`)*: `C`
e' **antiunitaria**, quindi `C e^{i t} = e^{-i t} C` — una fase scalare commuta con `C`
### **solo se `t` e' dispari sotto `C`**, e qui `t = pi cs` con `cs` **pari sotto `C`**,
perche' `W5` lo pretende. ### **Le due richieste sono incompatibili per costruzione**, e
`(B)` rompe **meno** di `(A)`.

### ⚠ **NESSUN `clip`, NESSUN pavimento, NESSUNA costante in questo file**, e un braccio lo
verifica sul sorgente.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)

# ### ⛔ **LE DUE FAMIGLIE SI NOMINANO**, e il nome entra nelle uscite: una lettura che
# ### non dice ### **quale famiglia** non si puo' confrontare con un'altra.
FAMIGLIE = ("A", "B")


def _z(cs):
    """`e^{i pi cs}`, elemento per elemento."""
    return np.exp(1j * np.pi * np.asarray(cs, dtype=float))


def frazione(X, psi, cs, famiglia="B"):
    """### `X(cs) psi` con **UNA sola** applicazione di `X`.

    `X` e' un **callable** `psi -> X psi`: cosi' la frazione non sa **quale** pezzo sta
    frazionando, e ### **lo stesso codice serve Grover, lo spostamento, e il vuoto.**

    `cs` e' un array **per estremita'** *(la stessa forma della prima dimensione di `psi`)*,
    oppure uno scalare. ### ⚠ **Dev'essere costante dentro il blocco di `X`** — il nodo per
    Grover, l'arco per lo spostamento — altrimenti `Q` mescolerebbe estremita' con `z`
    diversi, e ### **la forma non sarebbe piu' unitaria.** *(`blocco_costante` lo verifica,
    e un braccio del collaudo lo esercita.)*

    ### ⛔ **IL CORTOCIRCUITO E' `W1`:** `cs` identicamente `1` ⟹ **`X psi` AL BIT**;
    `cs` identicamente `0` ⟹ **`psi` AL BIT.**
    """
    assert famiglia in FAMIGLIE, "### famiglia `%r` sconosciuta" % (famiglia,)
    c = np.asarray(cs, dtype=float)
    if c.size and np.all(c == 1.0):
        return X(psi)
    if c.size and np.all(c == 0.0):
        return psi
    z = _z(c)
    # ### la forma dell-ampiezza: `cs` e- per ESTREMITA-, `psi` puo- avere le componenti
    while z.ndim < psi.ndim:
        z = z.reshape(z.shape + (1,))
    Q = 0.5 * (psi + X(psi))
    if famiglia == "A":
        return z * (psi + (z - 1.0) * Q)
    return Q + z * (psi - Q)


def frazione_inversa(X, psi, cs, famiglia="B"):
    """### L'INVERSA ESATTA: ### **`cs -> -cs`**, e il conto e' lo stesso.

    ### ⭐ **Perche' funziona:** su `Q` la famiglia vale `1` *(per `B`)* o `z^2` *(per `A`)*,
    e su `I - Q` vale `z`; mandare `cs` in `-cs` manda `z` in `z^{-1}` ### **su entrambi i
    rami**, e il prodotto e' l'identita'. ### **Non e' un'approssimazione.**
    """
    return frazione(X, psi, -np.asarray(cs, dtype=float), famiglia)


def blocco_costante(cs, blocco):
    """### `max` della variazione di `cs` **dentro** un blocco: ### **dev'essere `0`.**

    `blocco` e' l'indice del blocco per ogni estremita' *(`sc["nodo"]` per Grover,
    `arange(2m) // 2` per lo spostamento)*.
    """
    c = np.asarray(cs, dtype=float).reshape(-1)
    b = np.asarray(blocco).reshape(-1)
    if c.size == 1:
        return 0.0
    peggio = 0.0
    for q in np.unique(b):
        v = c[b == q]
        peggio = max(peggio, float(v.max() - v.min()))
    return peggio


def scarto_a_uno(X, psi, cs, famiglia="B"):
    """### Dove `cs == 1`, **quanto** la famiglia si discosta da `X psi`.

    ### ⛔ **SERVE PERCHE' IL CORTOCIRCUITO NON SCATTA SU UN `cs` MISTO:** la- il risultato
    e' `X psi` a meno di `~1e-16`, e ### **un numero dichiarato non e' un difetto nascosto.**
    """
    c = np.asarray(cs, dtype=float).reshape(-1)
    dove = (c == 1.0)
    if not np.any(dove) or np.all(c == 1.0):
        return 0.0
    a = frazione(X, psi, cs, famiglia)
    b = X(psi)
    return float(np.max(np.abs((a - b)[dove])))


def cs_da_arco(cs_nodo, sc, forma="min"):
    """### Il `cs` di un **ARCO** dalle sue **due estremita'**, con una forma SIMMETRICA.

    ### ⛔ **`W8` lo permette e pretende che la forma sia DICHIARATA:** *«o `cs` dell'arco,
    derivato dalle sue due estremita' con una forma simmetrica dichiarata»*.

    | | la forma | perche' |
    |---|---|---|
    | `min` | `min(cs_u, cs_v)` | ### **l'estremita' LENTA fa da collo**, ed e' la scelta
      ### **causale**: il cono e' un tetto *(`W7`)*, e il lato lento non puo' essere spinto |
    | `armonica` | `2 cs_u cs_v / (cs_u + cs_v)` | ### **liscia**, e domina il piu' lento |
    | `media` | `(cs_u + cs_v)/2` | ### ⚠ **la piu' permissiva**: un lato veloce ALZA il
      lato lento, e questo va dichiarato |

    ### ⚠ **NON SCELGO IO fra le tre:** la scelta sta in `[[DOMANDA-LAMBDA-GRANDEZZA]]`, e
    il banco le accende ### **separatamente.**
    """
    v = np.asarray(cs_nodo, dtype=float)[sc["nodo"]].reshape(-1, 2)
    a, b = v[:, 0], v[:, 1]
    if forma == "min":
        out = np.minimum(a, b)
    elif forma == "armonica":
        s = a + b
        out = np.where(s > 0.0, 2.0 * a * b / np.where(s > 0.0, s, 1.0), 0.0)
    elif forma == "media":
        out = 0.5 * (a + b)
    else:
        raise AssertionError("### forma `%r` sconosciuta" % (forma,))
    return np.repeat(out, 2)


if __name__ == "__main__":
    import camminata as CM
    import camminata2 as C2
    import geometria as GE
    import scena as SC
    import vuoto3 as V3
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    SC._niente_simulatore()
    sc = SC.irregolare()
    geo = GE.scena_curva(sc, 11)
    rng = np.random.default_rng(11)
    psi = CM.stato_casuale(sc, 11)
    phi = (rng.normal(size=2 * sc["m"]) + 1j * rng.normal(size=2 * sc["m"]))
    pezzi = (("Grover dello spinore", lambda v: CM.moneta_grover(v, sc), psi, sc["nodo"]),
             ("spostamento, curva", lambda v: C2.spostamento_trasporto(v, geo, sc), psi,
              np.arange(2 * sc["m"]) // 2),
             ("Grover del vuoto", lambda v: V3.grover_scalare(v, sc), phi, sc["nodo"]),
             ("spostamento del vuoto", lambda v: V3.spostamento_scalare(v), phi,
              np.arange(2 * sc["m"]) // 2))
    uno = np.ones(2 * sc["m"])
    print("  %-24s %-4s %-12s %-12s %-12s %s"
          % ("il pezzo", "fam", "cs=1 al bit", "cs=0 al bit", "inversa", "norma a cs=0.5"))
    for nome, X, v, bl in pezzi:
        for fa in FAMIGLIE:
            a1 = float(np.max(np.abs(frazione(X, v, uno, fa) - X(v))))
            a0 = float(np.max(np.abs(frazione(X, v, 0.0 * uno, fa) - v)))
            c = 0.37 * uno
            inv = float(np.max(np.abs(
                frazione_inversa(X, frazione(X, v, c, fa), c, fa) - v)))
            m = frazione(X, v, 0.5 * uno, fa)
            nm = abs(float(np.sum(np.abs(m) ** 2)) - float(np.sum(np.abs(v) ** 2)))
            print("  %-24s %-4s %-12.3g %-12.3g %-12.3g %.3g"
                  % (nome, fa, a1, a0, inv, nm))
    print()
    # ### il `cs` dell-arco, e le tre forme
    csn = rng.random(sc["n"])
    for forma in ("min", "armonica", "media"):
        ca = cs_da_arco(csn, sc, forma)
        print("  cs dell-arco, forma `%-9s`: dentro l-arco varia di %.3g   "
              "min %.4f max %.4f"
              % (forma, blocco_costante(ca, np.arange(2 * sc["m"]) // 2),
                 ca.min(), ca.max()))
