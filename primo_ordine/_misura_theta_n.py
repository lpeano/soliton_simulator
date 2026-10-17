# -*- coding: utf-8 -*-
r"""**`Theta` CONTRO LE DIREZIONI `n`** — *una misura, nessuna decisione di fisica.*

> **Punto 2 del mandato di Luca del 2026-10-15, terza parte** *(misura proposta dal
> guardiano)*: *«la `C` del modello, `psi -> i sigma_y psi^*`, e' l'inversione del tempo
> standard dello spin `1/2` (`Theta^2 = -1`, Kramers). Una moneta `sigma.n` con `n` FISSO si
> comporta come un campo magnetico, che rompe `Theta`. Ma algebricamente, per OGNI `n` e col
> passo palindromo, deve valere `Theta W[n] Theta^-1 = W[-n]^-1`.»*

## ⭐ LA DERIVAZIONE, scritta prima di misurare

```
Theta exp(-i a sigma.n) Theta^-1 = exp(-i a sigma.n)          <- MISURATO: 0.000e+00
   perche'  sigma_y (sigma.n)^* sigma_y^-1 = -(sigma.n)  con n reale
e la STESSA riga, letta su -n:
Theta exp(-i a sigma.(-n)) Theta^-1 = exp(+i a sigma.n) = [moneta con n]^-1
```

### ⭐⭐ **Cioe': la moneta con `n` va nell'INVERSA della moneta con `-n`.** Gli altri pezzi
vanno nel loro inverso *(misurato, `16`/`16`)*, e **il palindromo rimette l'ordine**
*(misurato: pendenza `2.006` contro `1.183`)*. ### ✅ **Quindi, per OGNI `n`:**

> ### **`Theta · W[n] · Theta^-1 = W[-n]^-1`**

### ⛔ **E QUESTO SPIEGA IL `6.68e-01` CHE AVEVO RIPORTATO:** confrontavo
`Theta W[n] Theta^-1` con **`W[n]^-1`**, cioe' ### **col `-n` mancante.** ### **Non era un
difetto del modello: era il confronto sbagliato.**

## ⭐ E IL PEZZO `(c)`: LA MAPPA DEL RETICOLO

### **Con `n` GEOMETRICI** *(l'`n` dell'estremita' = la direzione dell'arco uscente dal
nodo, quindi le due estremita' di un arco hanno `n` opposti)*, l'**inversione spaziale** del
toro `v -> -v` manda l'arco `(v, d)` nell'arco `(-v-e_d, d)`, e ### **scambia le due
estremita'**: `2k -> 2k'+1` e `2k+1 -> 2k'`.

### ✅ **E porta `n` in `-n`**, perche' l'`n` geometrico dell'estremita' immagine e'
l'opposto. ### ⭐ **Quindi, se `P W[n] P^-1 = W[-n]`, allora**

```
(P Theta) W[n] (P Theta)^-1 = P W[-n]^-1 P^-1 = (P W[-n] P^-1)^-1 = W[n]^-1
```

### ⭐⭐ **cioe' `P Theta` e' una simmetria ANTIUNITARIA ESATTA del passo** — e
`(P Theta)^2 = P^2 Theta^2 = -1`, ### **quindi Kramers.**

### ⛔⛔ **MA C'E' UN <<SE>>, E L'HO DERIVATO PRIMA DI MISURARE:** l'inversione
### **rovescia l'orientamento dell'arco**, e con l'orientamento rovesciato ### **`U` va in
`U^dagger`.** ### **Allora con `U` CASUALE la mappa NON PUO' essere una simmetria**
*(servirebbe `U^dagger = U` su ogni arco)*. ### ✅ **Percio' `(c)` si misura con `U = I`, e
lo DICHIARO** — e si misura **anche** con `U` casuale, come **caso che deve fallire.**

## 📌 COME SI COSTRUISCONO GLI `n` NELLE SCENE DEL MOTORE

### **Censito DAL CODICE a ogni corsa** *(non ricopiato)*: lo script scandisce
`primo_ordine/*.py` e stampa l'elenco. ### ⚠ **E la risposta che conta e' una: gli `n`
GEOMETRICI non esistono in nessuna scena**, quindi li costruisce questo file.

Gira con:  python primo_ordine/_misura_theta_n.py
"""
import os
import re
import sys

import numpy as np
import tick as TK

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA**
LATI = (3, 3)
SEME = 7
DTAU = (1.0, 0.5, 0.25)
EPS = 0.5
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-60s %s   %s" % (che[:60], "PASSA" if passa else "### FALLISCE", nota))


# ====================================================================== il censimento
def censimento():
    """### Come si costruiscono gli `n`, ### **LETTO DAL CODICE e non a memoria.**"""
    casuali, zeta, altri = [], [], []
    for nome in sorted(os.listdir(_QUI)):
        if not nome.endswith(".py"):
            continue
        t = open(os.path.join(_QUI, nome), encoding="utf-8", errors="replace").read()
        if re.search(r"nv\s*=\s*r\.normal", t):
            casuali.append(nome)
        elif re.search(r"nv\[:,\s*2\]\s*=\s*1\.0", t):
            zeta.append(nome)
        elif re.search(r"\bnv\s*=", t):
            altri.append(nome)
    print("### IL CENSIMENTO DEGLI `n`, letto dal codice adesso:")
    print("  casuali gaussiani (poi normalizzati): %s" % ", ".join(casuali))
    print("  `z` uniforme (nv[:,2] = 1.0):         %s" % ", ".join(zeta))
    print("  altri modi:                           %s"
          % (", ".join(altri) if altri else "nessuno"))
    print("  ### ⛔ GEOMETRICI (dalla direzione dell'arco): NESSUNA SCENA DEL MOTORE."
          " Li costruisce questo file.")
    return casuali, zeta, altri


# ====================================================================== le scene
def _versori_geometrici(lati, ii, jj):
    """### `n` **GEOMETRICI**: la direzione dell'arco uscente dal nodo.

    ### ⭐ **Le due estremita' di un arco hanno `n` OPPOSTI**, ed e' il punto: e' cio' che
    rende l'inversione spaziale una mappa che porta `n` in `-n`.
    """
    m = len(ii)
    nv = np.zeros((2 * m, 3), dtype=float)
    d = len(lati)
    for k in range(m):
        asse = k % d
        nv[2 * k, asse] = 1.0
        nv[2 * k + 1, asse] = -1.0
    return nv


def _inversione(lati, ii, jj):
    """### La permutazione delle ESTREMITA' indotta dall'inversione spaziale `v -> -v`.

    ### ⚠ **E si VERIFICA che sia una biiezione e un'INVOLUZIONE**, invece di assumerlo:
    `P^2 = 1` e' cio' che serve alla derivazione, e ### **un conto sugli indici e' il posto
    tipico dove si sbaglia un segno.**
    """
    d = len(lati)
    nn = 1
    for a in lati:
        nn *= a

    def coord(v):
        c, r = [], v
        for a in reversed(lati):
            c.append(r % a)
            r //= a
        return list(reversed(c))

    def indice(c):
        v = 0
        for a, cc in zip(lati, c):
            v = v * a + cc
        return v

    # ### l-arco `k` e- `(v, asse)` con `v = k // d` e `asse = k % d`
    P = np.zeros(2 * len(ii), dtype=np.int64) - 1
    for k in range(len(ii)):
        v, asse = k // d, k % d
        c = coord(v)
        meno = [(-x) % lati[t] for t, x in enumerate(c)]
        # ### l-arco immagine parte da `-v - e_asse`
        part = list(meno)
        part[asse] = (part[asse] - 1) % lati[asse]
        k2 = indice(part) * d + asse
        # ### e le due estremita- SI SCAMBIANO
        P[2 * k] = 2 * k2 + 1
        P[2 * k + 1] = 2 * k2
    assert sorted(P.tolist()) == list(range(2 * len(ii))), "`P` non e' una biiezione"
    assert np.all(P[P] == np.arange(2 * len(ii))), "`P` non e' un'involuzione"
    return P


def scena(dtau, geometrici, identita):
    """### Il toro `LATI`, con `n` casuali o GEOMETRICI e `U` casuale o `I`."""
    import corrente as CO
    import incidenza as IN
    import motore as MO
    import stato as ST
    ii, jj, nn = CO.toro(LATI)
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE),
                       np.asarray(jj, dtype=IN.INDICE), nn, capacita=len(ii))
    r = np.random.default_rng(SEME)
    if geometrici:
        nv = _versori_geometrici(LATI, ii, jj)
    else:
        nv = r.normal(size=(2 * inc.m, 3))
        nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    for a in range(inc.m):
        if identita:
            U[a] = np.eye(2)
        else:
            X = r.normal(size=(2, 2)) + 1j * r.normal(size=(2, 2))
            Qm, _ = np.linalg.qr(X)
            U[a] = Qm / np.sqrt(np.linalg.det(Qm))
    st = ST.nuovo(nn, inc.m)
    # ### ⛔⛔ **IL VUOTO SI ACCENDE PRIMA DI COSTRUIRE IL MOTORE** *(`2026-10-17`)*:
    # ### `ST.nuovo` da- ### **`phi = 0` su OGNI nodo**, e dal `1902e0a9` ### **quello
    # ### non e- uno stato fisico** *(decisione di Luca)* -- quindi il costruttore ALZAVA,
    # ### e ### **TRE strumenti non partivano piu-**: questo, `_misura_theta_nonlineare.py`
    # ### e `_misura_completa_l2.py`.
    # ### ✅ **E IL NUMERO NON E- UNA MANOPOLA** *(`A1`)*: ogni chiamante SOVRASCRIVE
    # ### `phi` subito dopo *(`stato_di_prova`, o i vettori di base)*, quindi questo e-
    # ### ### **il vuoto di COSTRUZIONE e non entra in nessun numero** -- e il controllo
    # ### e- MISURATO: gli esiti dei tre strumenti sono ### **IDENTICI a quelli del PADRE
    # ### del commit del divieto**, dove la costruzione era `phi = 0`.
    st["phi_h"][...] = 1.0
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, dtau), "numpy")
    return inc, mot, st


# ====================================================================== la matrice
def ordine_lineare():
    """### L'ordine della TABELLA **senza i FLUSSI**: la parte LINEARE.

    ### ⛔⛔ **E IL FILTRO E' PER TIPO, NON PER `id`, e il motivo e' un difetto
    pagato:** fino al `2026-10-15` questa riga escludeva ### **`CAMM-SATURAZIONE` per
    nome**, e quando la legge e' stata ### **sostituita da `CAMM-MATERIA-VUOTO`** il
    filtro ### **non escludeva piu' niente** -- cioe' <<la parte lineare>> avrebbe
    incluso ### **un termine NON lineare.**
    ### ⚠ **E non si vedeva, per un ACCIDENTE:** la matrice si costruisce con
    `phi = 0`, e la' `alpha = ln(rho/(rho+0)) + 0 = 0` ### **esattamente** -- quindi il
    termine era ### **l'identita' su `psi`** e il numero non cambiava.
    ### ✅ **Un filtro che dipende da un accidente non e' un filtro:** adesso si legge
    ### **`motore.FLUSSI`**, cioe' ### **il tipo**, e una legge nuova entra da sola.
    """
    import composizione as CM
    import motore as MO
    return [(idl, fr) for idl, fr, _t in CM.ORDINE if idl not in MO.FLUSSI]


def matrice(mot, st, ordine):
    """### `W` sulla parte `psi`, ### **applicando il passo ai vettori di base.**"""
    import deriva as DV
    forma = st["psi_h"].shape
    d = forma[0] * forma[1]
    W = np.zeros((d, d), dtype=complex)
    for k in range(d):
        st["psi_h"].fill(0)
        st["phi_h"].fill(0)
        st["psi_h"].reshape(-1)[k] = 1.0
        mot.apri_tick()
        for idl, fr in ordine:
            nome, vuole_par = TK.OPERATORE[idl]
            mot.operatori[nome](st, {"eps": EPS} if vuole_par else {}, fr)
        mot.chiudi_tick()
        W[:, k] = st["psi_h"].reshape(-1)
    return W


def _S(nest):
    """### La parte LINEARE di `Theta`: `i sigma_y` su ogni estremita'."""
    return np.kron(np.eye(nest), 1.0j * SY)


def _P(perm):
    """### La permutazione delle estremita', **alzata allo spinore** *(che non tocca)*."""
    n = len(perm)
    M = np.zeros((n, n), dtype=float)
    M[perm, np.arange(n)] = 1.0
    return np.kron(M, np.eye(2))


def theta_di(W, S):
    """### `Theta W Theta^-1 = S conj(W) S^-1`. ### **Il segno di `Theta^2` si cancella.**"""
    return S.dot(np.conj(W)).dot(np.linalg.inv(S))


# ====================================================================== le prove
def prove(dtau):
    """### `(a)`, `(b)` e `(c)` a un `dtau` dato."""
    eps_m = float(np.finfo(float).eps)
    toll = 1024 * eps_m
    print("-" * 96)
    print("  dtau = %.4f   (con l'ordine palindromo OGNI pezzo sta a frazione 0.5,"
          " quindi un pezzo agisce a theta = pi*dtau/2)" % dtau)
    ordine = ordine_lineare()
    # ---------------------------------------------------- (a) l'identita', n CASUALI
    inc, mot, st = scena(dtau, geometrici=False, identita=False)
    nest = st["psi_h"].shape[0]
    S = _S(nest)
    Wn = matrice(mot, st, ordine)
    mot.geo.n[...] = -mot.geo.n
    Wm = matrice(mot, st, ordine)
    sa = float(np.max(np.abs(theta_di(Wn, S) - np.linalg.inv(Wm))))
    esito("(a) `Theta W[n] Theta^-1 = W[-n]^-1`, n CASUALI", sa <= toll,
          "scarto %.3e, cioe' %.0f ulp" % (sa, sa / eps_m))
    # ---------------------------------------------------- (b) il caso che DEVE fallire
    sb = float(np.max(np.abs(theta_di(Wn, S) - np.linalg.inv(Wn))))
    esito("### (b) DEVE FALLIRE: confrontato con `W[+n]^-1` (n NON rovesciato)",
          sb > toll,
          "scarto %.3e: ### e' il confronto che avevo fatto io, e dava 6.68e-01" % sb)
    # ---------------------------------------------------- (c) n GEOMETRICI, U = I
    import corrente as CO
    ii, jj, _nn = CO.toro(LATI)
    perm = _inversione(LATI, ii, jj)
    Pm = _P(perm)
    inc, mot, st = scena(dtau, geometrici=True, identita=True)
    Wg = matrice(mot, st, ordine)
    mot.geo.n[...] = -mot.geo.n
    Wgm = matrice(mot, st, ordine)
    sc1 = float(np.max(np.abs(Pm.dot(Wg).dot(np.linalg.inv(Pm)) - Wgm)))
    esito("(c1) `P W[n] P^-1 = W[-n]` con n GEOMETRICI e `U = I`", sc1 <= toll,
          "scarto %.3e, cioe' %.0f ulp" % (sc1, sc1 / eps_m))
    PT = Pm.dot(S)
    sc2 = float(np.max(np.abs(PT.dot(np.conj(Wg)).dot(np.linalg.inv(PT))
                              - np.linalg.inv(Wg))))
    esito("(c2) `(P Theta) W (P Theta)^-1 = W^-1`: UNA SIMMETRIA ESATTA", sc2 <= toll,
          "scarto %.3e, cioe' %.0f ulp" % (sc2, sc2 / eps_m))
    # ### ⭐ **e la conseguenza che si puo- GUARDARE: `(P Theta)^2 = -1`, quindi Kramers**
    lam = np.linalg.eigvals(Wg)
    g = _gruppi(lam, 1e-8)
    esito("(c3) e la DEGENERAZIONE di Kramers c'e', come `(P Theta)^2 = -1` chiede",
          min(g) >= 2, "molteplicita' minima %d su %d gruppi" % (min(g), len(g)))
    # ---------------------------------------------------- (c-bis) con U CASUALE: deve ROMPERSI
    inc, mot, st = scena(dtau, geometrici=True, identita=False)
    Wu = matrice(mot, st, ordine)
    mot.geo.n[...] = -mot.geo.n
    Wum = matrice(mot, st, ordine)
    sd = float(np.max(np.abs(Pm.dot(Wu).dot(np.linalg.inv(Pm)) - Wum)))
    esito("### (c4) DEVE ROMPERSI: lo stesso con `U` CASUALE", sd > toll,
          "scarto %.3e: ### l'inversione ROVESCIA l'arco, e la' `U` va in `U^dagger`" % sd)
    return sa, sb, sc1, sc2, min(g), sd


def _gruppi(lam, toll):
    n = len(lam)
    usato = np.zeros(n, dtype=bool)
    fuori = []
    for i in range(n):
        if usato[i]:
            continue
        vv = [j for j in range(n) if not usato[j] and abs(lam[j] - lam[i]) <= toll]
        for j in vv:
            usato[j] = True
        fuori.append(len(vv))
    return fuori


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 96)
    print("`Theta` CONTRO LE DIREZIONI `n` -- una misura, nessuna decisione di fisica")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s   seme = %d   dtau = %s   eps = %.1f"
          % (LATI, SEME, DTAU, EPS))
    print("-" * 96)
    censimento()
    tab = []
    for dtau in DTAU:
        tab.append((dtau,) + prove(dtau))
    print("=" * 96)
    print("  LA TABELLA:")
    print("  %-8s %-12s %-12s %-12s %-12s %-7s %s"
          % ("dtau", "(a) n/-n", "(b) deve !=", "(c1) P", "(c2) P Theta", "molt.",
             "(c4) U casuale, deve !="))
    for dtau, sa, sb, sc1, sc2, mm, sd in tab:
        print("  %-8.4f %-12.3e %-12.3e %-12.3e %-12.3e %-7d %.3e"
              % (dtau, sa, sb, sc1, sc2, mm, sd))
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E NESSUNA CONCLUSIONE DI FISICA: la simmetria del modello -- la `C`, il")
    print("###   ruolo di `n` -- e' una decisione di Luca. Qui ci sono solo numeri.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
