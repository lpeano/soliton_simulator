# -*- coding: utf-8 -*-
"""`P3` — **L'ENERGIA COME SOMMA DI DENSITA' LOCALI, E LA CORRENTE SUGLI ARCHI.**

> `E = Re <psi | W psi> + somma_k Lambda_k G(h_k / Lambda_k)`

### ⛔ **MAI COME PRODOTTO GLOBALE, e il mandato lo dice:** `E` **non e'** un numero da cui
si ricavano le densita' — ### **le densita' sono la definizione, e `E` e' la loro
somma.**

| | la densita' | dove vive |
|---|---|---|
| la parte **lineare** | `e_h = Re[ conj(psi_h) . (W psi)_h ]` | **per ESTREMITA'** |
| il **vuoto** | `e_k = Lambda_k G(h_k / Lambda_k)` | **per NODO** |

### ⚠ **E L'ENERGIA DI UN NODO attribuisce al nodo le sue estremita':** ogni estremita'
appartiene a **un nodo solo**, quindi l'attribuzione e' **l'unica possibile senza spezzare
un'estremita'**. ### **Non c'e' arbitrio, ma e' un passo e va detto.**

## ⭐ LA CORRENTE: UNICA, E L'UNICITA' VIENE DA UN CAMPO DELLA TABELLA

### ✅ **Il campo `azione` dice quali pezzi attraversano fra nodi:** `estremita` **no**
*(agisce su una estremita' e non legge il vicino)*, `nodo` **no** *(mescola le estremita'
di uno stesso nodo)*, ### **`arco` SI'** — ed e' **uno solo**, lo spostamento con
trasporto.

### ⛔ **QUINDI TUTTO IL TRASFERIMENTO FRA NODI DI UN TICK LINEARE PASSA PER LO
SPOSTAMENTO**, e la corrente di un arco e' **cio' che lo spostamento porta su quell'arco**.
### ⭐ **L'unicita' NON e' una mia scelta: viene dalla TABELLA** -- e se un giorno una
legge nuova avesse `azione: arco`, ### **la corrente cambierebbe da sola.**

### ⚠ **IL VERSO:** `J[k] > 0` vuol dire **energia che va da `ii[k]` a `jj[k]`**.
### **Scambiare `ii` e `jj` cambia il SEGNO e non il bilancio**, ed e' il caso che il
collaudo **deve far fallire**.

## ⛔ CON `N` IL BILANCIO NON CHIUDE, E NON E' UN DIFETTO DI QUESTO FILE

`N` **non attraversa** *(il suo generatore dipende solo da grandezze di nodo)*, quindi la
sua corrente e' **zero**; ma **cambia `e_h`**, perche' cambia `psi` e **non commuta** col
Grover ne' con lo spostamento. ### **Quindi `Delta E_k` da `N` non e' la somma dei flussi**,
e questo modulo **lo MISURA invece di nasconderlo**: `residuo()` torna il numero.

## ⭐ ANNOTAZIONE DEL 2026-10-13 — **DUE COSE QUI SOPRA SONO SBAGLIATE**

### ⛔ **NON SI RISCRIVE, SI ANNOTA:** cio' che era scritto resta leggibile, e la
correzione ### **si vede accanto.**

| | che cosa dice il paragrafo qui sopra | la correzione |
|---|---|---|
| `1` | *<<la corrente di un arco e' cio' che lo spostamento porta>>* | ### ⛔ **quella candidata NON CHIUDE il bilancio**, ed e' misurato |
| `2` | *<<LA CORRENTE: UNICA>>* | ### ⛔ **non e' unica, e la non unicita' NON E' UN DIFETTO:** e' la stessa liberta' della corrente d'energia nel continuo, definita **a meno di un rotore** |

### ✅ **E UNA CORRENTE LOCALE ESISTE**, per la parte lineare: ### **portata MISURATA `3` archi**,
costruita in **`primo_ordine/corrente.py`** dalla forma quadratica di `Delta e_k`.
### ⚠ **Il referto e' `doc/REFERTO_corrente_locale.md`.**

### ⛔ **E DA <<la mia candidata non funziona>> avevo inferito <<la corrente locale non
esiste>>:** ### **il salto non si fa**, e questa annotazione esiste per ricordarlo.

### 📌 **La derivazione sta in `doc/TASK_HISTORY/2026-10-12_energia_corrente.md`**, e il
limite va a Luca.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import saturazione as SAT                                     # noqa: E402


def densita_estremita(st, mot, par_moneta, fuori):
    """### `e_h = Re[ conj(psi_h) . (W psi_h) ]`, ### **dentro `fuori`.**

    ### ⛔ **`W` SI APPLICA A UNA COPIA, e non allo stato:** l'energia e' **una lettura**,
    e una lettura che cambia lo stato ### **non e' una lettura.**

    ### ⛔ **`par_moneta` ARRIVA DA CHI CHIAMA, cioe' DALLA TABELLA, e NON ha un valore di
    comodo:** `W` contiene la moneta di spin, che vuole `eps` -- e ### **un `eps` scelto
    da questo modulo sarebbe un numero senza origine.** ### ✅ **La stessa regola del motore: nessun default di
    fisica.**
    """
    assert par_moneta and par_moneta.get("eps") is not None, (
        "`densita_estremita` vuole i parametri della moneta DALLA TABELLA: `W` la"
        " contiene, e un `eps` scelto da qui sarebbe un numero senza origine")
    psi = st["psi_h"]
    # ### la copia su cui `W` gira: ### **un buffer con la taglia addosso**, come tutti
    lavoro = mot._b("en_W", psi.shape, psi.dtype)
    lavoro[...] = psi
    finto = dict(st)
    finto["psi_h"] = lavoro
    # ### ⭐ **`W` E- IL TICK LINEARE, e i suoi tre pezzi stanno in TABELLA:** qui si
    # ### applicano ### **nell-ordine della composizione**, e ### **nient-altro.**
    mot.operatori["moneta_spin"](finto, par_moneta, 1)
    mot.operatori["grover"](finto, {}, 1)
    mot.operatori["spostamento_trasporto"](finto, {}, 1)
    np.sum(np.real(np.conj(psi) * lavoro), axis=1, out=fuori)
    return fuori


def densita_nodo(st, mot, fuori):
    """### `e_k = Lambda_k G(h_k / Lambda_k)`, ### **col LIMITE.**

    ### ⛔ **Dove `Lambda == 0` esatto, `N -> h - (pi/2) Lambda sign(h)`**, che a
    `Lambda = 0` fa **`h`**: ### **e' il valore che la funzione PRENDE la'**, non un
    pavimento.
    """
    h = mot.elicita(st)
    lam = mot.densita_vuoto(st)
    buoni = lam > 0.0
    fuori[...] = h
    if np.any(buoni):
        fuori[buoni] = lam[buoni] * SAT.G(h[buoni] / lam[buoni])
    return fuori


def per_nodo(st, mot, par_moneta):
    """### `E_k`: le estremita' del nodo **piu'** il suo vuoto. ### **E `E = somma`.**"""
    n = mot.inc.n
    eh = densita_estremita(st, mot, par_moneta,
                           mot._b("en_h", (st["psi_h"].shape[0],), float))
    ek = densita_nodo(st, mot, mot._b("en_k", (n,), float))
    fuori = mot._b("en_nodo", (n,), float)
    fuori.fill(0)
    # ### ⚠ **L-ATTRIBUZIONE: ogni estremita- va al SUO nodo**, e ne ha uno solo
    np.add.at(fuori, mot.inc.nodo, eh)
    fuori += ek
    return fuori


def totale(st, mot, par_moneta):
    """### `E`, ### **come SOMMA delle densita' e non come prodotto globale.**"""
    return float(per_nodo(st, mot, par_moneta).sum())


def corrente(st, mot, par_moneta, verso):
    """### `J[k]`: l'energia che lo spostamento porta **sull'arco `k`**, da `ii` a `jj`.

    ### ⛔ **E' lo SPOSTAMENTO e nient'altro**, perche' e' **il solo pezzo con
    `azione: arco`** — gli altri due del tick lineare **non attraversano**.

    ### ⚠ **`verso` serve AL COLLAUDO, e NON ha un valore di comodo: `None` vuol dire
    il verso VERO, e si scrive.** ### **Un array di `+1`/`-1` per arco inverte il verso di quegli archi**, e il
    collaudo lo usa per il caso che **DEVE fallire**: ### **una corrente col verso
    sbagliato deve rompere il bilancio.**
    """
    psi = st["psi_h"]
    m = mot.inc.m
    # ### lo stato DOPO moneta e Grover: e- cio- che lo spostamento prende in mano
    lavoro = mot._b("cor_W", psi.shape, psi.dtype)
    lavoro[...] = psi
    finto = dict(st)
    finto["psi_h"] = lavoro
    mot.operatori["moneta_spin"](finto, par_moneta, 1)
    mot.operatori["grover"](finto, {}, 1)
    v = lavoro.reshape(m, 2, 2)
    U = mot.geo.U
    # ### ⭐ **CHE COSA ATTRAVERSA: il lato `0` va sul lato `1` trasportato da `U`.**
    # ### L-energia che passa e- ### **la parte reale del prodotto fra cio- che ARRIVA e
    # ### cio- che C-ERA**, cioe- il termine di `e_h` che lo spostamento crea sull-altro
    # ### capo.
    arriva1 = np.einsum("aij,aj->ai", U, v[:, 0, :])
    arriva0 = np.einsum("aji,aj->ai", np.conj(U), v[:, 1, :])
    pre = psi.reshape(m, 2, 2)
    e01 = np.sum(np.real(np.conj(pre[:, 1, :]) * arriva1), axis=1)
    e10 = np.sum(np.real(np.conj(pre[:, 0, :]) * arriva0), axis=1)
    J = mot._b("cor_J", (m,), float)
    # ### ⚠ **IL VERSO: positivo vuol dire da `ii` a `jj`.** La differenza fra cio- che
    # ### arriva su `jj` e cio- che arriva su `ii` e- ### **il flusso NETTO.**
    np.subtract(e01, e10, out=J)
    if verso is not None:
        # ### il ramo del COLLAUDO: ### **inverte il verso di alcuni archi**, e il
        # ### bilancio ### **DEVE rompersi.**
        J *= np.asarray(verso, dtype=float)
    return J


def bilancio(e_prima, e_dopo, J, ii, jj, n):
    """### Il residuo per nodo: `|Delta E_k - (cio' che entra - cio' che esce)|`.

    ### ✅ **E' PURA: nessuno stato, nessun motore, nessun buffer.** Cosi' il
    collaudo la prova ### **sui numeri**, e il caso che deve fallire *(il verso
    invertito)* ### **si costruisce cambiando UN SEGNO**, non costruendo un'altra scena.

    ### ⛔ **IL SEGNO: un arco `k` TOGLIE a `ii[k]` e DA' a `jj[k]`**, perche'
    `J[k] > 0` vuol dire **energia che va da `ii` a `jj`**.
    """
    flusso = np.zeros(n, dtype=float)
    np.add.at(flusso, jj, J)
    np.add.at(flusso, ii, -J)
    return np.abs((e_dopo - e_prima) - flusso)
