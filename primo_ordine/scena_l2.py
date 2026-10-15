# -*- coding: utf-8 -*-
r"""**LA SCENA DI RIFERIMENTO DI `L2`** — *`n` geometrici, `U = I`, vuoto uniforme.*

> **Dichiarata in `de89549`, decisa da Luca il `2026-10-15`:** la scena di riferimento usa
> **`n` GEOMETRICI** *(direzioni di moto)* e **`U = I`**, e le scene con `n` casuali restano
> come **prove di robustezza DICHIARATE**, non come fisica.

## ⛔ PERCHE' UN GRUMO <<ISOTROPO>> NON SATURA — *e perche' il grumo ha elicita' `+1`*

`h_k = somma_{h in k} psi_h^dagger (sigma.n_h) psi_h`, e ### **la FASE di `psi` non conta**
*(`psi^dagger A psi` e' invariante per fase)*. Quindi se le estremita' di un nodo hanno
**lo stesso spinore** e **lo stesso modulo**, le direzioni uscenti — che su un toro
### **sommano a zero** — danno ### **`h_k = 0` ESATTO.**

> ### ⚠⚠ **Cioe' un grumo definito sul NODO, con un solo spinore, NON TOCCA IL VUOTO PER
> NIENTE:** `x = 0`, `al = be = 0`.

### ✅ **E LA VIA D'USCITA NON E' UN TRUCCO: E' `sigma.p`.** Con lo spinore di ogni
estremita' **allineato con la sua direzione** *(autovettore `+1` di `sigma.n_h`)*:

```
h_k = somma_h |psi_h|^2   =   la densita' di materia del nodo
x   = h/Lambda            =   il rapporto materia/vuoto, esatto
```

### 📌 **E' UNA SCELTA DI SCENA, DICHIARATA, non una legge.** ### **Chi rifa' la misura con
un altro grumo deve sapere che il risultato dipende da questa scelta.**

## 📌 IL VUOTO DI RIFERIMENTO

### **`phi` UNIFORME**, lo **stesso valore complesso** su tutte le estremita'.
### ⭐ **E senza materia dev'essere STAZIONARIO, e si deriva:** `h = 0` spegne la
saturazione; il **Grover** lascia fermo il vettore uniforme *(ne e' l'autovettore)*; e il
**hop** da' `(alpha + beta) phi = phi`, perche' `alpha + beta = 1`.
### ⚠ **Ma in virgola mobile `(1+z)/2` e `(1-z)/2` ARROTONDANO**, quindi una deriva di
**qualche ulp per tick** c'e' — ### **e il numero si misura, non si assume**
*(`_misura_verso_l2.py`)*.

Non si gira da solo: e' il modulo che `_misura_verso_l2.py` usa.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

# ### ⛔ **LA TAGLIA DEL TORO, DICHIARATA E SCELTA PER IL BUDGET:** `7x7 = 49` nodi, `98`
# ### archi, `196` estremita-, grado `4`. ### **Serve che ci stiano almeno TRE anelli
# ### attorno al centro** *(la distanza massima su `7x7` e- `6`)*, e che `400` tick su piu-
# ### scene stiano in pochi secondi.
LATI = (7, 7)


def versori_geometrici(lati, m):
    """### `n` **GEOMETRICI**: la direzione dell'arco uscente dal nodo.

    ### ⭐ **Le due estremita' di un arco hanno `n` OPPOSTI**, ed e' la cosa che conta:
    e' cio' che rende `n` una **direzione di moto** e non un campo esterno.
    ### 📌 **La convenzione degli indici e' quella di `corrente.toro`:** l'arco `k` e'
    `(nodo = k // d, asse = k % d)`, e le sue estremita' sono `2k` *(su `ii`)* e `2k+1`
    *(su `jj`)*.
    """
    d = len(lati)
    nv = np.zeros((2 * m, 3), dtype=float)
    for k in range(m):
        asse = k % d
        nv[2 * k, asse] = 1.0
        nv[2 * k + 1, asse] = -1.0
    return nv


def spinore_allineato(nv):
    """### Lo spinore **allineato** con `n`: l'autovettore `+1` di `sigma.n`.

    ### ⭐ **Si costruisce PROIETTANDO**, non con una formula per casi: `(I + sigma.n)/2`
    e' il proiettore, e si proietta un vettore di prova. ### ✅ **Cosi' vale per QUALUNQUE
    `n` unitario**, non solo per gli assi — e il giorno che le `n` verranno da un grafo
    che nasce *(la domanda aperta di `L3`-`L4`)* **questa funzione non cambia.**
    ### ⚠ **E si verifica che l'autovalore sia `+1`**, invece di assumerlo.
    """
    nv = np.ascontiguousarray(nv, dtype=float)
    ne = nv.shape[0]
    chi = np.zeros((ne, 2), dtype=complex)
    for h in range(ne):
        nx, ny, nz = nv[h]
        # ### `(I + sigma.n)/2` applicato a un vettore di prova
        P = 0.5 * (np.eye(2, dtype=complex)
                   + np.array([[nz, nx - 1j * ny], [nx + 1j * ny, -nz]], dtype=complex))
        for prova in (np.array([1.0, 0.0], dtype=complex),
                      np.array([0.0, 1.0], dtype=complex)):
            v = P.dot(prova)
            nn = float(np.linalg.norm(v))
            if nn > 1e-8:
                chi[h] = v / nn
                break
        else:
            raise AssertionError("nessuna proiezione non nulla per n = %r" % (nv[h],))
    # ### il controllo: `(sigma.n) chi = +chi`
    for h in range(ne):
        nx, ny, nz = nv[h]
        S = np.array([[nz, nx - 1j * ny], [nx + 1j * ny, -nz]], dtype=complex)
        sb = float(np.max(np.abs(S.dot(chi[h]) - chi[h])))
        assert sb <= 1e-12, ("lo spinore dell'estremita' %d non e' autovettore `+1`:"
                             " scarto %.3e" % (h, sb))
    return chi


def coord(v, lati):
    c, r = [], v
    for a in reversed(lati):
        c.append(r % a)
        r //= a
    return list(reversed(c))


def anelli(lati, centro):
    """### I nodi raggruppati per **distanza toroidale** dal centro.

    ### ⚠ **La distanza e' quella del RETICOLO** *(somma delle distanze per asse, ognuna
    presa nel verso piu' corto per la periodicita')*, e ### **non una distanza euclidea:**
    su un grafo la distanza e' il numero di archi.
    """
    nn = 1
    for a in lati:
        nn *= a
    cc = coord(centro, lati)
    per = {}
    for v in range(nn):
        c = coord(v, lati)
        dist = 0
        for t, a in enumerate(lati):
            dd = abs(c[t] - cc[t])
            dist += min(dd, a - dd)
        per.setdefault(dist, []).append(v)
    return per


def scena(dtau, vuoto, ampiezza, raggio, materia, geometrici, fasi_casuali, seme,
          lati=LATI):
    """### La scena: `(inc, mot, st, par, centro, per_anello)`.

    ### ⛔ **Nessun argomento ha un valore di comodo:** una scena con un default sarebbe
    ### **una scelta mia che nessuno vede**, e qui ogni scelta cambia un numero.
    ### 📌 **`materia = False` da' la scena GEMELLA senza grumo**, con **lo stesso `phi` e
    lo stesso grafo**: e' cio' che rende la misura **DIFFERENZIALE.**
    """
    import corrente as CO
    import incidenza as IN
    import motore as MO
    import stato as ST
    ii, jj, nn = CO.toro(lati)
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE),
                       np.asarray(jj, dtype=IN.INDICE), nn, capacita=len(ii))
    r = np.random.default_rng(seme)
    if geometrici:
        nv = versori_geometrici(lati, inc.m)
    else:
        nv = r.normal(size=(2 * inc.m, 3))
        nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    # ---------------------------------------------------------------- il vuoto
    if fasi_casuali:
        st["phi_h"][...] = (float(vuoto)
                            * np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi))
    else:
        # ### ⭐ **UNIFORME: lo STESSO valore complesso**, e la fase e- `0` per scelta --
        # ### ### **una fase globale non cambia niente** *(`U1-FASE-GLOBALE`)*, e metterla
        # ### a zero rende la scena ### **riproducibile a mente.**
        st["phi_h"][...] = float(vuoto)
    # ---------------------------------------------------------------- la materia
    centro = 0
    per = anelli(lati, centro)
    if materia:
        chi = spinore_allineato(nv)
        dentro = set()
        for d, nodi in per.items():
            if d <= raggio:
                dentro.update(nodi)
        for h in range(2 * inc.m):
            if int(inc.nodo[h]) in dentro:
                st["psi_h"][h] = float(ampiezza) * chi[h]
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, dtau), "numpy")
    return inc, mot, st, {"eps": 0.5}, centro, per


def grumo_isotropo(st, inc, per, raggio, ampiezza):
    """### Il grumo **ISOTROPO**: lo **stesso** spinore su tutte le estremita'.

    ### ⛔ **E' il CONTROLLO che fa vedere perche' il grumo di riferimento e' allineato:**
    qui `h_k` deve venire ### **esattamente `0`**, e la materia **non tocca il vuoto.**
    """
    st["psi_h"].fill(0)
    dentro = set()
    for d, nodi in per.items():
        if d <= raggio:
            dentro.update(nodi)
    chi = np.array([1.0, 0.0], dtype=complex) / np.sqrt(1.0)
    for h in range(st["psi_h"].shape[0]):
        if int(inc.nodo[h]) in dentro:
            st["psi_h"][h] = float(ampiezza) * chi
    return st
