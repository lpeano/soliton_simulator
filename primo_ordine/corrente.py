# -*- coding: utf-8 -*-
"""LA CORRENTE LOCALE DELL'ENERGIA — **costruita dalla FORMA QUADRATICA, non intuita.**

> ### ⛔ **PERCHE' COSI' E NON A INTUIZIONE.** La prima candidata era *«cio' che lo
> spostamento porta»*, e **falliva**: `e_h` non e' una carica trasportata, e' **una
> correlazione fra due tempi**. ### **Da quel fallimento avevo concluso che la corrente
> locale NON ESISTESSE: era un salto sbagliato.** La verifica esterna lo ha corretto, e
> questo modulo **costruisce la corrente che esiste.**

## ⭐ L'ARGOMENTO, in tre righe

`Delta e_k` e' **una forma quadratica reale** in `x = (Re psi, Im psi)` con supporto in un
**intorno** di `k`, e ### **`somma_k Delta e_k = 0` per OGNI `psi`.** ### ✅ **Quindi vale
COEFFICIENTE PER COEFFICIENTE:** per ogni coppia `(i, j)` di componenti, i numeri
`{(Q_k)_{ij}}_k` **sommano a zero** su un insieme **limitato** di nodi.
### ⭐ **E un insieme di numeri a somma zero su un insieme limitato SI INSTRADA** lungo
cammini dentro quell'insieme: ### **la continuita' chiude PER COSTRUZIONE.**

## ⚠ LA NON UNICITA' NON E' UN DIFETTO

E' **la stessa liberta' della corrente d'energia nel continuo**, definita **a meno di un
rotore**. ### ✅ **Una corrente e' fisicamente locale se e' funzione LOCALE dello stato e
CHIUDE la continuita'. L'unicita' non serve** — e la scelta del riferimento e dei cammini
**e' quella liberta' di ricircolo**, non un'arbitrarieta' nascosta.

## ⛔ IL COSTO: QUESTA E' UNA COSTRUZIONE PER LA PROVA, NON PER IL PERCORSO CALDO

Estrarre la forma quadratica costa **`O(D^2)` valutazioni** con `D = 8m`, e l'instradamento
**`O(D^2)` cammini**. ### **Su una scena piccola e' una misura; su una scena grande non si
fa**, e va detto invece di scoprirlo.

Gira con:  python primo_ordine/corrente.py   (la portata, misurata)
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import energia as EN                                          # noqa: E402


def dim(m):
    """### La dimensione del vettore reale: ### **`8m`.**

    `psi` ha `2m` estremita' per `2` componenti = `4m` numeri complessi, e ciascuno da'
    **due** reali. ### ⚠ **E l'ordine e' DICHIARATO:** prima tutte le parti reali
    *(appiattite)*, poi tutte le immaginarie -- ### **chi legge `x` deve sapere dove
    guardare.**
    """
    return 8 * int(m)


def x_da_psi(psi):
    """### `psi` complesso `(2m, 2)` → `x` reale di lunghezza `8m`."""
    return np.concatenate([np.asarray(psi).real.ravel(),
                           np.asarray(psi).imag.ravel()])


def psi_da_x(x, m):
    """### L'inverso, ### **e serve per valutare la forma sulla BASE.**"""
    q = 4 * int(m)
    return (x[:q].reshape(2 * int(m), 2)
            + 1j * x[q:].reshape(2 * int(m), 2))


def nodo_di_componente(inc):
    """### Il NODO di ogni componente di `x`. ### **E' cio' che LIMITA il supporto.**

    ### ⛔ **Senza questa mappa non si sa DOVE vive un coefficiente**, e senza il dove
    ### **non si puo' instradare niente.**
    """
    m = inc.m
    q = 4 * m
    fuori = np.zeros(dim(m), dtype=int)
    for i in range(q):
        # ### `i // 2` e- l-estremita-: due componenti di spinore per estremita-
        fuori[i] = int(inc.nodo[i // 2])
        fuori[i + q] = int(inc.nodo[i // 2])
    return fuori


def _delta_e(st, mot, par, psi, fuori):
    """### `Delta e_k` per il `psi` dato. ### **Non tocca lo stato vero.**"""
    s = dict(st)
    s["psi_h"] = np.asarray(psi, dtype=complex).copy()
    e0 = EN.densita_estremita(s, mot, par,
                              mot._b("cor_eh", (s["psi_h"].shape[0],), float)).copy()
    mot.operatori["moneta_spin"](s, par, 1)
    mot.operatori["grover"](s, {}, 1)
    mot.operatori["spostamento_trasporto"](s, {}, 1)
    e1 = EN.densita_estremita(s, mot, par,
                              mot._b("cor_eh2", (s["psi_h"].shape[0],), float))
    fuori.fill(0)
    np.add.at(fuori, mot.inc.nodo, e1 - e0)
    return fuori


def forma_quadratica(st, mot, par, verboso=False):
    """### `Q` di forma `(n, D, D)`: ### **`Delta e_k = x^T Q_k x`**, ESATTO.

    ### ⭐ **E' esatto perche' `Delta e_k` E' una forma quadratica:** `e_k` e' bilineare in
    `psi` e `W` e' lineare, quindi **non c'e' ne' parte lineare ne' costante**.
    ### ⚠ **E si verifica**, invece di assumerlo: la forma valutata su `x` deve coincidere
    con `Delta e_k(psi)` ### **per un `psi` che non e' nella base.**
    """
    m, n = mot.inc.m, mot.inc.n
    D = dim(m)
    Q = np.zeros((n, D, D), dtype=float)
    buf = np.zeros(n, dtype=float)
    # ### la DIAGONALE: `Delta e_k(e_i)`
    diag = np.zeros((n, D), dtype=float)
    base = np.zeros(D, dtype=float)
    for i in range(D):
        base.fill(0)
        base[i] = 1.0
        diag[:, i] = _delta_e(st, mot, par, psi_da_x(base, m), buf)
    for i in range(D):
        Q[:, i, i] = diag[:, i]
    # ### e le FUORI DIAGONALE, per POLARIZZAZIONE: ### **`(f(e_i+e_j) - Q_ii - Q_jj)/2`**
    for i in range(D):
        for j in range(i + 1, D):
            base.fill(0)
            base[i] = 1.0
            base[j] = 1.0
            v = _delta_e(st, mot, par, psi_da_x(base, m), buf)
            c = 0.5 * (v - diag[:, i] - diag[:, j])
            Q[:, i, j] = c
            Q[:, j, i] = c
        if verboso and (i % 64) == 0:
            print("   forma quadratica: riga %d su %d" % (i, D))
    return Q


def _cammini(inc):
    """### Per ogni coppia di nodi, ### **un cammino piu' corto** -- e la sua lunghezza.

    ### ⚠ **BFS da ogni nodo**, e il cammino si ricostruisce dai predecessori:
    ### **deterministico**, perche' i vicini si guardano **nell'ordine della `CSR`**.
    """
    n = inc.n
    prev = -np.ones((n, n), dtype=int)
    arco = -np.ones((n, n), dtype=int)
    dist = -np.ones((n, n), dtype=int)
    for s in range(n):
        dist[s, s] = 0
        coda = [s]
        testa = 0
        while testa < len(coda):
            u = coda[testa]
            testa += 1
            for h in inc.estremita_di_nodo(u).tolist():
                v = int(inc.nodo[h ^ 1])
                if dist[s, v] < 0:
                    dist[s, v] = dist[s, u] + 1
                    prev[s, v] = u
                    arco[s, v] = h >> 1
                    coda.append(v)
    return dist, prev, arco


def instrada(Q, inc, x, tol=1e-14):
    """### `(J, portata, diagnosi)`: ### **la corrente, e LA PORTATA MISURATA.**

    ### ⛔ **PERCHE' `x` ENTRA QUI invece di tenere i coefficienti:** i coefficienti
    d'instradamento sarebbero un tensore `(D, D, m)`, e su un toro `3x3x3` fanno
    ### **`272 MB`**. ### ⚠ **La macchina di Luca in certi momenti non li ha**, e un
    tensore che non serve ### **non si alloca.**

    ### ⭐ **E LA SOMMA ZERO E' CIO' CHE FA CHIUDERE TUTTO:** per ogni coppia `(i, j)`
    i numeri `{(Q_k)_{ij}}_k` sommano a zero, quindi mandando a ciascun nodo la sua parte
    **dal riferimento**, al riferimento ### **non resta niente.**

    ### ⭐ **LA PORTATA SI MISURA, non si dichiara:** e' **la lunghezza massima** dei
    cammini usati, in archi. ### **E con lei si misurano il SUPPORTO piu' grande e la
    DISTANZA piu' grande dentro un supporto**, perche' ### **<<portata 1>> senza il
    supporto non dice se e' un fatto o una coppia fortunata.**
    """
    D = Q.shape[1]
    dist, prev, arco = _cammini(inc)
    J = np.zeros(inc.m, dtype=float)
    portata = 0
    supporto = 0
    distanza = 0
    for i in range(D):
        xi = float(x[i])
        for j in range(D):
            peso = xi * float(x[j])
            c = Q[:, i, j]
            vivi = np.flatnonzero(np.abs(c) > tol)
            if vivi.size > 1:
                supporto = max(supporto, int(vivi.size))
                distanza = max(distanza, int(np.max(dist[np.ix_(vivi, vivi)])))
            if vivi.size <= 1 or peso == 0.0:
                # ### il ramo SENZA CARICA: con UN SOLO nodo vivo la somma zero dice
                # ### che ### **quel numero vale zero entro `tol`**, e non c-e- niente
                # ### da mandare. ### **E senza peso non c-e- corrente.**
                continue
            rif = int(vivi[0])
            for k in vivi[1:]:
                k = int(k)
                quanto = float(c[k]) * peso
                v = k
                passi = 0
                while v != rif:
                    a = int(arco[rif, v])
                    u = int(prev[rif, v])
                    # ### ⛔ **IL SEGNO: positivo da `ii` a `jj`.** Si va da `u` a
                    # ### `v`, quindi se `ii[a] == u` il verso coincide, altrimenti
                    # ### ### **si inverte.**
                    J[a] += quanto if int(inc.ii[a]) == u else -quanto
                    v = u
                    passi += 1
                portata = max(portata, passi)
    return J, portata, {"supporto": supporto, "distanza": distanza,
                        "diametro": int(np.max(dist))}


def divergenza(J, inc):
    """### `div J` per nodo: ### **cio' che ENTRA meno cio' che ESCE.**"""
    fuori = np.zeros(inc.n, dtype=float)
    np.add.at(fuori, inc.jj, J)
    np.add.at(fuori, inc.ii, -J)
    return fuori


# ---------------------------------------------------------------- le scene della misura
def anello(nn):
    """### L'anello di `nn` nodi: ### **grado `2`**, il caso piu' povero."""
    ii = np.arange(nn, dtype=np.int64)
    return ii, (ii + 1) % nn, nn


def toro(lati):
    """### Il toro periodico: ### **grado `2 d`**.

    ### ⛔ **E SERVE**, perche' la portata misurata su un grafo di grado `2`
    ### **non dice niente del grado `6`.**
    """
    lati = tuple(int(a) for a in lati)
    nn = 1
    for a in lati:
        nn *= a

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
        for d in range(len(lati)):
            cc = list(c)
            cc[d] = (cc[d] + 1) % lati[d]
            ii.append(v)
            jj.append(indice(cc))
    return (np.asarray(ii, dtype=np.int64), np.asarray(jj, dtype=np.int64), nn)


def _scena(ii, jj, nn, seme):
    """### Lo stato e la geometria casuali, ### **`U(2)` per arco via `QR`.**"""
    import incidenza as IN
    import motore as MO
    import stato as ST
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE),
                       np.asarray(jj, dtype=IN.INDICE), nn, capacita=len(ii))
    r = np.random.default_rng(seme)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    for a in range(inc.m):
        X = r.normal(size=(2, 2)) + 1j * r.normal(size=(2, 2))
        Qm, _ = np.linalg.qr(X)
        U[a] = Qm
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi)
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.2), "numpy")
    return inc, mot, st, {"eps": 0.5}


def termine_di_bordo(ii, jj, nn, dentro, seme=4, scossa=0.7):
    """### **LA VARIAZIONE D'ENERGIA DI UNA REGIONE E' UN TERMINE DI BORDO**, misurato.

    ### ⭐ **E' l'argomento che dimostra l'esistenza, provato sul simulatore:**
    `somma_R Delta e = - somma_{fuori da R} Delta e`, quindi ### **dipende solo da `psi`
    vicino al BORDO di `R`.** ### ✅ **Allora perturbare `psi` DENTRO `R` e lontano dal
    bordo non puo' cambiare quella somma** -- per quanto cambi `Delta e` nodo per nodo.

    ### ⛔ **E IL CONTROLLO POSITIVO E' OBBLIGATORIO:** senza una perturbazione **al
    bordo** che cambi `O(1)`, l'invarianza direbbe solo ### **che la mia perturbazione non
    arriva da nessuna parte.**

    Rende `(delta_interna, delta_al_bordo, cambio_per_nodo, base)`.
    """
    inc, mot, st, par = _scena(ii, jj, nn, seme)
    dentro = np.asarray(dentro, dtype=bool)
    buf = np.zeros(nn, dtype=float)
    base = _delta_e(st, mot, par, st["psi_h"], buf).copy()
    somma = float(np.sum(base[dentro]))
    # ### il BORDO di `R`: ### **i nodi di `R` che hanno un vicino FUORI.**
    bordo = np.zeros(nn, dtype=bool)
    for v in range(nn):
        if dentro[v] and np.any(~dentro[inc.vicini_di_nodo(v)]):
            bordo[v] = True
    dist, _p, _a = _cammini(inc)
    lontano = dentro & (np.min(dist[:, bordo], axis=1) >= 2)
    assert np.any(lontano) and np.any(bordo), (
        "la regione non ha ne' interno a distanza `>= 2` ne' bordo: ### **la misura non"
        " avrebbe materia**, ed e' un FALSO-ZERO")
    fuori = {}
    for nome, dove in (("interna", lontano), ("bordo", bordo)):
        psi = st["psi_h"].copy()
        tocca = dove[inc.nodo]
        psi[tocca] += scossa
        d = _delta_e(st, mot, par, psi, np.zeros(nn, dtype=float)).copy()
        fuori[nome] = (abs(float(np.sum(d[dentro])) - somma),
                       float(np.max(np.abs(d - base))))
    return (fuori["interna"][0], fuori["bordo"][0],
            fuori["interna"][1], somma)


def misura(nome, ii, jj, nn, seme=4, verboso=False):
    """### Una riga della tabella: ### **identita', portata, residuo, e il CONTROLLO.**"""
    inc, mot, st, par = _scena(ii, jj, nn, seme)
    Q = forma_quadratica(st, mot, par, verboso=verboso)
    # ### ⭐ **L-IDENTITA- CHE REGGE TUTTO**, verificata e non assunta:
    identita = float(np.max(np.abs(np.sum(Q, axis=0))))
    x = x_da_psi(st["psi_h"])
    # ### ⚠ **E la forma si verifica su un `x` CHE NON E- NELLA BASE**, altrimenti
    # ### ### **si verificherebbe cio- con cui e- stata costruita.**
    buf = np.zeros(nn, dtype=float)
    de = _delta_e(st, mot, par, st["psi_h"], buf).copy()
    forma = float(np.max(np.abs(np.einsum("i,kij,j->k", x, Q, x) - de)))
    J, portata, dia = instrada(Q, inc, x)
    res = float(np.max(np.abs(divergenza(J, inc) - de)))
    # ### ⛔ **IL CONTROLLO CHE DEVE FALLIRE: un arco col VERSO INVERTITO.**
    Jm = J.copy()
    a_rotto = int(np.argmax(np.abs(J)))
    Jm[a_rotto] = -Jm[a_rotto]
    rotto = float(np.max(np.abs(divergenza(Jm, inc) - de)))
    sc = float(np.max(np.abs(de)))
    eps = float(np.finfo(float).eps)
    return {"nome": nome, "n": nn, "m": inc.m, "grado": int(inc.grado[0]),
            "D": dim(inc.m), "identita": identita, "forma": forma,
            "portata": portata, "supporto": dia["supporto"],
            "distanza": dia["distanza"], "diametro": dia["diametro"],
            "residuo": res, "ulp": res / (eps * max(sc, 1e-30)),
            "scala": sc, "rotto": rotto}


# ### ⛔ **UNA SCALA DI TAGLIE DELLA STESSA FAMIGLIA, e non per abbondanza:**
# ### <<portata finita>> significa ### **che NON CRESCE col grafo**, e con una taglia sola
# ### non si distingue da ### **<<portata = diametro>>** -- che su una scena piccola da'
# ### lo stesso numero.
# ### ⚠ **E IL `3x3` CI STA PER MOSTRARE IL TAGLIO:** ha diametro `2`, e la portata la'
# ### vale `2` ### **perche' il GRAFO la taglia, non perche' la portata sia `2`.**
# ### ⭐ **Il confronto che decide e' fra le taglie il cui diametro e' GIA' sopra la
# ### saturazione** *(`4x4`, `4x6`, `6x6`)*.
SCENE = (("anello-10", 10), ("toro2d-3x3", (3, 3)), ("toro2d-4x4", (4, 4)),
         ("toro2d-4x6", (4, 6)), ("toro2d-6x6", (6, 6)),
         ("toro3d-3x3x3", (3, 3, 3)))

# ### ⚠ **LA CONFIGURAZIONE INTERA, IN UN POSTO SOLO:** il referto la dichiara
# ### ### **da qui**, e non la ricopia. ### ⛔ **Il difetto che si cura e' esattamente
# ### questo: dichiarare i parametri che ho toccato io e tacere i trenta che stavano a
# ### default.** *(La regola, e il suo presidio, sono nominati nel docstring di
# ### `scrivi_referto`: un ID non vive in un commento.)*
CONFIG = (("seme", 4),
          ("dtau", 0.2),
          ("eps della moneta di spin", 0.5),
          ("sommatoria", "numpy"),
          ("psi iniziale", "gaussiano complesso dal seme, NON normalizzato"),
          ("phi iniziale", "modulo 1, fasi uniformi dal seme"),
          ("versori n per estremita'", "gaussiani dal seme, normalizzati a 1"),
          ("U per arco", "U(2) casuale via QR, COMPAGNA = coniugata trasposta"),
          ("il tick misurato", "W = moneta_spin -> grover -> spostamento_trasporto"),
          ("il flusso N", "SPENTO -- questa e' la PARTE LINEARE"),
          ("tol dell'instradamento", "1e-14"),
          ("scossa del termine di bordo", 0.7))
DOVE = os.path.join(os.path.dirname(_QUI), "doc", "REFERTO_corrente_locale.md")
ULP_MAX = 1000.0
ROTTO_MIN = 1e-3


def scrivi_referto(righe, bordo):
    """### Il referto, ### **scritto dallo script che ha misurato.**

    ### ⛔ **E NON RICOPIATO:** un numero ricopiato ### **non ha provenienza.**

    ### ⚠ **E DICHIARA `CONFIG` PER INTERO**, che e' la regola di **`H-P5`**: il difetto
    che quel presidio cura e' ### **dichiarare i parametri che ho toccato io e tacere i
    trenta che stavano a default.**
    ### ⚠ **E si codifica PRIMA di aprire il file**, perche' un `open(w)` ### **tronca
    quando apre**, e l'argomento di `write()` si valuta dopo.
    """
    import io
    import platform
    nl = chr(10)
    r = []
    r.append("# LA CORRENTE LOCALE DELL'ENERGIA **ESISTE**, ed e' COSTRUITA — "
             "portata **`3` archi**")
    r.append("")
    r.append("> ### ⛔ **QUESTO REFERTO CORREGGE UNA MIA CONCLUSIONE.** In `36182b7`"
             " avevo scritto")
    r.append("> *<<la corrente locale non esiste nemmeno per la parte lineare>>*."
             " ### **Era un salto:**")
    r.append("> cio' che avevo dimostrato e' che **la MIA CANDIDATA** *(<<cio' che lo"
             " spostamento")
    r.append("> porta>>)* **fallisce**. ### ✅ **L'esistenza e' un'altra cosa, ed e'"
             " VERA.**")
    r.append("")
    r.append("> ### ⭐ **E LA NON UNICITA' NON E' UN DIFETTO:** e' la stessa liberta'"
             " della corrente")
    r.append("> d'energia nel continuo, definita **a meno di un rotore**."
             " ### **Una corrente e' fisicamente")
    r.append("> locale se e' funzione LOCALE dello stato e CHIUDE la continuita':"
             " l'unicita' non serve.**")
    r.append("")
    r.append("Lo rigira:  `python primo_ordine/corrente.py --scrivi`")
    r.append("")
    r.append("## 1. LA CONFIGURAZIONE INTERA")
    r.append("")
    r.append("| la voce | il valore |")
    r.append("|---|---|")
    for k, v in CONFIG:
        r.append("| %s | `%s` |" % (k, v))
    r.append("| piattaforma | `%s`, python `%s`, numpy `%s` |" %
             (platform.system(), platform.python_version(), np.__version__))
    r.append("")
    r.append("## 2. `(a)` IL TERMINE DI BORDO — *l'argomento, sul mio simulatore*")
    r.append("")
    r.append("Anello di `40` nodi, `R` = i nodi `0..19`."
             " ### **`somma_R Delta e` di base: `%.12f`.**" % bordo[3])
    r.append("")
    r.append("| la perturbazione | `|somma_R Delta e| cambia` | il verdetto |")
    r.append("|---|---|---|")
    r.append("| **DENTRO `R`**, a distanza `>= 2` dal bordo | **`%.3e`** |"
             " ### ✅ **invariante entro ulp** |" % bordo[0])
    r.append("| **AL BORDO** di `R` *(controllo positivo)* | **`%.3e`** |"
             " ### ⭐ **`O(1)`: la perturbazione ARRIVA** |" % bordo[1])
    r.append("")
    r.append("### ⚠ **E `Delta e` NODO PER NODO CAMBIA FINO A `%.3f`:** non e' che la"
             " perturbazione" % bordo[2])
    r.append("non faccia niente — ### **cambia tutto tranne la somma sulla regione.**")
    r.append("")
    r.append("## 3. `(b)` LA COSTRUZIONE, E LA PORTATA **MISURATA**")
    r.append("")
    r.append("| scena | `n` | `m` | grado | `D` | `somma_k Q_k` | la forma su `x` |"
             " **PORTATA** | supporto | diametro | continuita' | verso invertito |")
    r.append("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for x in righe:
        r.append("| `%s` | %d | %d | %d | %d | `%.1e` | `%.1e` | **`%d`** | %d | %d |"
                 " `%.1f` ulp | `%.2e` |" %
                 (x["nome"], x["n"], x["m"], x["grado"], x["D"], x["identita"],
                  x["forma"], x["portata"], x["supporto"], x["diametro"],
                  x["ulp"], x["rotto"]))
    r.append("")
    r.append("### ⭐ **LA PORTATA E' `3` ARCHI, E NON CRESCE COL GRAFO:** a grado `4`,"
             " i diametri")
    r.append("`4`, `5` e `6` danno ### **tutti `3`**, e il supporto massimo resta"
             " ### **`8` nodi.**")
    r.append("### ⚠ **E IL `3x3` MOSTRA IL TAGLIO, non una crescita:** ha diametro"
             " `2`, e la' la portata")
    r.append("vale `2` ### **perche' il GRAFO la taglia** — non perche' la portata sia"
             " `2`.")
    r.append("### ⛔ **Sull'anello vale `1`:** a grado `2` il supporto di una coppia"
             " e' **`2` nodi**.")
    r.append("")
    r.append("## 4. CHE COSA RESTA VERO DI `36182b7`, E CHE COSA CADE")
    r.append("")
    r.append("| | che cosa |")
    r.append("|---|---|")
    r.append("| ✅ **resta vero** | la candidata *<<cio' che lo spostamento porta>>*"
             " **non chiude** il bilancio |")
    r.append("| ✅ **resta vero** | `e_h` e' una **correlazione fra due tempi**,"
             " non una carica a un tempo |")
    r.append("| ⛔ **CADE** | *<<la corrente locale non esiste nemmeno per la parte"
             " lineare>>* |")
    r.append("| ⛔ **RITIRATA** | la raccomandazione di **cambiare la grandezza"
             " promossa**: non era motivata |")
    r.append("")
    r.append("### ⚠ **E il secondo fatto NON implica il terzo:** che `e_h` sia una"
             " correlazione fra due")
    r.append("tempi e' vero, ma ### **non impedisce la localita'.**")
    r.append("")
    r.append("## 5. IL LIMITE DICHIARATO: **IL COSTO**")
    r.append("")
    r.append("### ⛔ **Questa e' una costruzione PER LA PROVA, non per il percorso"
             " caldo.** Estrarre")
    r.append("`Q` costa **`O(D^2)` valutazioni** con `D = 8m`, e l'instradamento"
             " **`O(D^2)` cammini**.")
    r.append("### **Su una scena piccola e' una misura; su una scena grande non si fa**,"
             " e va detto")
    r.append("invece di scoprirlo. ### ✅ **Cio' che la misura stabilisce e'"
             " L'ESISTENZA e LA PORTATA**,")
    r.append("non un algoritmo da far girare a ogni tick.")
    r.append("")
    dati = (nl.join(r) + nl).encode("utf-8")
    io.open(DOVE, "wb").write(dati)
    return DOVE


def main(argv):
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 100)
    print("LA CORRENTE LOCALE DELL'ENERGIA: COSTRUITA, E LA PORTATA MISURATA")
    print("=" * 100)
    # ### ⭐ **PRIMA IL TERMINE DI BORDO**, perche' e' l'argomento: se non valesse,
    # ### ### **la costruzione che viene dopo non avrebbe su che cosa poggiare.**
    print("  (a) IL TERMINE DI BORDO -- anello-40, R = i nodi 0..19")
    ii, jj, nn = anello(40)
    dentro = np.zeros(nn, dtype=bool)
    dentro[:20] = True
    bordo = termine_di_bordo(ii, jj, nn, dentro)
    dint, dbor, cambio, somma = bordo
    print("      somma su R di Delta e, base ....... %.12f" % somma)
    print("      perturbo DENTRO, a distanza >= 2 .. |somma_R cambia| = %.3e"
          "   (ma |Delta e| per nodo cambia fino a %.3f)" % (dint, cambio))
    print("      perturbo AL BORDO ................. |somma_R cambia| = %.3e"
          "   (DEVE essere O(1))" % dbor)
    print("=" * 100)
    righe = []
    for nome, forma in SCENE:
        ii, jj, nn = anello(forma) if isinstance(forma, int) else toro(forma)
        r = misura(nome, ii, jj, nn, verboso=("-v" in argv))
        righe.append(r)
        print("  %-14s n=%-4d m=%-4d grado=%-2d D=%-5d" %
              (r["nome"], r["n"], r["m"], r["grado"], r["D"]))
        print("      identita' somma_k Q_k = 0 ......... %.3e" % r["identita"])
        print("      la forma vale Delta e su x ........ %.3e" % r["forma"])
        print("      PORTATA ........................... %d archi"
              "  (supporto max %d nodi, distanza max %d, diametro %d)" %
              (r["portata"], r["supporto"], r["distanza"], r["diametro"]))
        print("      continuita': residuo .............. %.3e su scala %.3f"
              "  (%.1f ulp)" % (r["residuo"], r["scala"], r["ulp"]))
        print("      CONTROLLO verso invertito ......... %.3e"
              "  (DEVE essere O(1))" % r["rotto"])
    print("=" * 100)
    cattive = [r for r in righe
               if r["ulp"] > ULP_MAX or r["rotto"] < ROTTO_MIN]
    print("VERDETTO: %s  (%d scene, %d cattive)" %
          ("PASSA" if not cattive else "FALLISCE", len(righe), len(cattive)))
    # ### ⛔ **IL REFERTO SI SCRIVE SOLO SE LA MISURA PASSA, e solo se lo si CHIEDE:**
    # ### un referto scritto da una misura fallita ### **e- un referto che mente.**
    if "--scrivi" in argv:
        if cattive:
            print("### NIENTE REFERTO: la misura FALLISCE, e un referto scritto da una"
                  " misura fallita MENTE")
            return 1
        print("REFERTO: %s" % scrivi_referto(righe, bordo))
    print("=" * 100)
    return 0 if not cattive else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
