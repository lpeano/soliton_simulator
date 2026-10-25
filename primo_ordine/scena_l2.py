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
h_k = + somma_h |psi_h|^2        con elicita' +1
h_k = - somma_h |psi_h|^2        con elicita' -1
```

### ⛔⛔ **E QUI UNA MIA AFFERMAZIONE ERA SBAGLIATA, e la correzione e' del guardiano
*(2026-10-15)*:** avevo scritto che `h_k` **E'** la densita' di materia. ### **Non lo e':
`h_k` e' L'ELICITA', CON IL SUO SEGNO** — e coincide con la densita' ### **solo per
elicita' `+1`.**
### ⚠⚠ **E il segno conta, perche' `G(x) = x - arctan x` e' DISPARI:** quindi `N` e
`beta = dN/dLambda` ### **cambiano segno con `h`**, e ### **la materia a elicita' `-1` da'
al vuoto la FASE OPPOSTA.**

### 📌 **Percio' la misura del verso si fa su TRE grumi** *(a elicita' `+1`, `-1`, e
isotropo)*, **con la stessa densita' `|psi|^2` e la stessa scena** — e il grumo isotropo e'
### **il controllo che la misura non vede rumore.**

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



def _direzione(gradi):
    a = np.deg2rad(gradi)
    return (float(np.cos(a)), float(np.sin(a)), 0.0)


# ### ⭐ **LE GRIGLIE, PER NOME** *([[DECISIONE-SOLO-TRIANGOLI]], Luca `2026-10-23`; portate da `csv/_triangoli.py` il `2026-10-25`)*: ### **gli spostamenti interi dell'arco e la direzione
# ### di ciascuno** *(il versore della moneta, [[N-DIREZIONI-DI-MOTO]])*. ### ⛔ **LA GRIGLIA DEL MODELLO SONO I TRIANGOLI; il quadrato esiste SOLO come controllo di servizio, e il nome
# ### lo dice.** ### ⚠ **`scena` qui sotto e' ANCORA il quadrato** *(la usano `12` strumenti di `csv/`: la rinomina va col loro passaggio, un lavoro a se')*.
GRIGLIE = {
    "triangoli": (((1, 0), (0, 1), (1, 1)), (_direzione(0.0), _direzione(120.0), _direzione(60.0))),
    "quadrato_di_servizio": (((1, 0), (0, 1)), ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0))),
}
GRIGLIA_DEL_MODELLO = "triangoli"
VUOTO_PER_ESTREMITA = 1.0
EPS_MONETA = 0.5


def versori(m, direzioni):
    """### Il versore di ogni estremita': ### **`+e_a` sul lato `2k`, `-e_a` sul lato `2k + 1`** *(le direzioni di moto, [[N-DIREZIONI-DI-MOTO]])*."""
    d = len(direzioni)
    nv = np.zeros((2 * m, 3), dtype=float)
    for k in range(m):
        e = np.asarray(direzioni[k % d], dtype=float)
        nv[2 * k] = e
        nv[2 * k + 1] = -e
    return nv


def scena_toro(griglia, lati, dtau, x):
    """### **LA SCENA SU UN TORO DELLA GRIGLIA DATA PER NOME** *(`"triangoli"`, o `"quadrato_di_servizio"`)*: `(inc, mot, st, par)`, ### **la materia uniforme allineata `sqrt(x)`, il
    vuoto uniforme `VUOTO_PER_ESTREMITA`, `U = I`.** ### **Lati diversi ammessi; `dtau` scalare o per nodo.** ### **E' la scena di `csv/_triangoli.scena_toro`, AL BIT** *(il sigillo
    `csv/_sigillo_scena_triangoli.py`)*. ### ⛔ **La griglia non ha un valore di comodo: si NOMINA.**"""
    assert griglia in GRIGLIE, "la griglia %r non e' nel vocabolario %s" % (griglia, sorted(GRIGLIE))
    import corrente as CO
    import incidenza as IN
    import motore as MO
    import stato as ST
    spost, direz = GRIGLIE[griglia]
    ii, jj, nn = CO.toro_spostamenti(lati, spost)
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE), np.asarray(jj, dtype=IN.INDICE), nn, capacita=len(ii))
    nv = versori(inc.m, direz)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    st["phi_h"][...] = VUOTO_PER_ESTREMITA
    st["psi_h"][...] = float(np.sqrt(x)) * spinore_allineato(nv)
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.broadcast_to(np.asarray(dtau, dtype=float), (nn,)).copy(), "numpy")
    return inc, mot, st, {"eps": EPS_MONETA}


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


def spinore_antiallineato(nv):
    """### Lo spinore **ANTI-allineato**: l'autovettore `-1` di `sigma.n`.

    ### ⭐ **E si ottiene allineandolo a `-n`**, che e' la stessa cosa: l'autovettore `+1`
    di `sigma.(-n)` ### **e' l'autovettore `-1` di `sigma.n`.** ### ✅ **Cosi' non c'e' una
    seconda costruzione da tenere d'accordo con la prima.**
    """
    chi = spinore_allineato(-np.asarray(nv, dtype=float))
    # ### il controllo: `(sigma.n) chi = -chi`
    for h in range(chi.shape[0]):
        nx, ny, nz = nv[h]
        S = np.array([[nz, nx - 1j * ny], [nx + 1j * ny, -nz]], dtype=complex)
        sb = float(np.max(np.abs(S.dot(chi[h]) + chi[h])))
        assert sb <= 1e-12, ("lo spinore dell'estremita' %d non e' autovettore `-1`:"
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
          elicita, lati=LATI):
    """### La scena: `(inc, mot, st, par, centro, per_anello)`.

    ### ⛔ **Nessun argomento ha un valore di comodo:** una scena con un default sarebbe
    ### **una scelta mia che nessuno vede**, e qui ogni scelta cambia un numero.
    ### 📌 **`materia = False` da' la scena GEMELLA senza grumo**, con **lo stesso `phi` e
    lo stesso grafo**: e' cio' che rende la misura **DIFFERENZIALE.**
    ### ⭐ **E `elicita` vale `+1`, `-1` o `0`:** `+1` e `-1` sono gli spinori allineato e
    anti-allineato *(e danno `h` opposti)*, `0` e' ### **il grumo ISOTROPO**, che da'
    `h = 0` e serve da **controllo**. ### ⚠ **La densita' `|psi|^2` e' LA STESSA in tutti
    e tre**: cambia **solo la direzione dello spinore.**
    """
    assert elicita in (1, -1, 0), (
        "`elicita` vale `+1`, `-1` o `0` (isotropo), e non ha un valore di comodo: e' la"
        " cosa che cambia il SEGNO di `h`, cioe' il segno di `beta` (%r)" % (elicita,))
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
        if elicita == 1:
            chi = spinore_allineato(nv)
        elif elicita == -1:
            chi = spinore_antiallineato(nv)
        else:
            # ### ⛔ **ISOTROPO: lo STESSO spinore su tutte le estremita-**, che con `n`
            # ### geometrici da- ### **`h = 0` esatto.**
            chi = np.zeros((2 * inc.m, 2), dtype=complex)
            chi[:, 0] = 1.0
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
