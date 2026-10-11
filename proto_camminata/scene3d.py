# -*- coding: utf-8 -*-
r"""LE SCENE A DIMENSIONE `3`, e **LA DIMENSIONE SPETTRALE MISURATA** *(rilievo del guardiano)*.

> ## ⛔ **LE DUE SCENE DEL BANCO NON HANNO DIMENSIONE `3`, e il rilievo e' giusto:**
> ## `scena.regolare(n, salti=(1,2))` collega `i` a `i±1` e `i±2` ⟹ ### **un ANELLO con
> ## corde, cioe' UNA dimensione**; `scena.irregolare` e' ### **albero casuale piu' archi
> ## casuali** ⟹ ### **un grafo CASUALE**, col diametro `~ log n`.

### ⛔ **E IL LEGAME DIPENDE DALLA DIMENSIONE:** in `1D` un pozzo attrattivo ### **lega
sempre**; in `3D` serve una ### **forza minima**; in un grafo casuale le onde scappano
### **esponenzialmente.** ### **Quindi un verdetto sulle due scene del banco NON dice che
cosa succede in uno spazio a tre dimensioni.**

| | la famiglia | che cos'e' | il diametro |
|---|---|---|---|
| `cubico(L)` | **reticolo cubico PERIODICO** `L×L×L`, grado `6`, deterministico | ### **`3D`, e un CRISTALLO** | **`3⌊L/2⌋`** |
| `geometrico3d(n)` | grafo **geometrico** da punti `3D` deterministici, gradi in `[2, 6]` | ### **`3D` IRREGOLARE** | si misura |
| *(il banco)* | `scena.regolare` | ### **`1D`** | `~ n/4` |
| *(il banco)* | `scena.irregolare` | ### **CASUALE** | `~ log n` |

> ## ⛔ **E LE POSIZIONI DEL GEOMETRICO SERVONO *SOLO* A COSTRUIRE GLI ARCHI, E POI SI
> ## SCARTANO:** la scena che esce ### **non ha nessun campo di posizione**, e la fisica
> ## ### **non le vede** *(`[[DOMANDA-D9-GEOMETRIA]]`, `A17`)*. ### **Il geometrico serve a
> ## distinguere <<`3D`>> da <<reticolo perfetto>>:** se il cubico lega e questo no, il
> ## legame e' ### **della periodicita'**, non della dimensione.

### ⭐ **LA DIMENSIONE SPETTRALE SI MISURA, non si dichiara:** dalla probabilita' di ritorno
di una passeggiata **CLASSICA**, `p(t) ~ t^(-d_s/2)` ⟹ `d_s = -2 * d(log p)/d(log t)`.

### ⛔ **E LA PASSEGGIATA E' *PIGRA* (meta' ferma, meta' si muove), PER UNA RAGIONE PRECISA:**
il reticolo cubico e' ### **BIPARTITO** *(la parita' di `x+y+z`)*, quindi una passeggiata
semplice ha `p(t) = 0` ### **a ogni `t` dispari** — e una legge di potenza adattata su quello
### **sarebbe un artefatto della parita'.** ### **La pigrizia la toglie, e non cambia `d_s`.**

### ⚠ **NESSUN `clip`, NESSUNA costante tarata.** La finestra della regressione e'
### **derivata**: `t` sotto `diametro²`, cioe' sotto il tempo in cui una diffusione
raggiunge il bordo.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import scena as SC                                             # noqa: E402

FAMIGLIE = ("cubico", "geometrico3d", "anello", "casuale")
# ### ⛔ **LA SOGLIA FRA LE DUE VIE, e il motivo e- la MEMORIA:** la matrice `n x n` costa
# ### `8 n²` byte, cioe- ### **`0.5` GB a `n = 8000`** e ### **`5.4` GB a `n = 26000`.**
# ### **Sotto la soglia si fanno tutte le coppie** *(ed e- la via che la regressione
# ### verifica)*, sopra si usa un ### **albero spaziale periodico.**
MAX_N2 = 4000
# ### ⚠ **E `K_ALBERO` NON E- UNA COSTANTE DI UNA LEGGE: e- un BUDGET di candidati**, e
# ### ### **la regressione a `n = 512` dimostra che basta** -- un nodo di grado `<= 6` non
# ### si collega mai oltre il suo ventesimo vicino.
K_ALBERO = 20


def cubico(L):
    """### Il reticolo **cubico PERIODICO** `L×L×L`: grado `6`, ### **deterministico.**

    ### ⚠ **`L >= 3`**: a `L = 2` i due vicini lungo un asse ### **sono lo stesso nodo**, e
    il grafo non avrebbe grado `6`.
    """
    assert L >= 3, "### `cubico` vuole `L >= 3`: a `L = 2` i vicini collassano"
    def idx(x, y, z):
        return (x % L) + L * (y % L) + L * L * (z % L)
    archi = set()
    for x in range(L):
        for y in range(L):
            for z in range(L):
                u = idx(x, y, z)
                for v in (idx(x + 1, y, z), idx(x, y + 1, z), idx(x, y, z + 1)):
                    if u != v:
                        archi.add((min(u, v), max(u, v)))
    return SC.costruisci(L ** 3, sorted(archi), "cubico(L=%d)" % L)


def punti_cubico(L):
    """### Le posizioni del reticolo, **per l-OSSERVATORE**: `(x, y, z)/L`."""
    p = np.zeros((L ** 3, 3), dtype=float)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                p[x + L * y + L * L * z] = (x / L, y / L, z / L)
    return p


def diametro_cubico(L):
    """### `3⌊L/2⌋`, **dal conto**: per asse la distanza e' `min(|d|, L-|d|) <= ⌊L/2⌋`."""
    return 3 * (L // 2)


def punti3d(n, seme=11):
    """### I punti di costruzione di `G3`: ### **deterministici dal seme**, nel cubo `[0,1)³`.

    ### ⛔ **ESCONO da questa funzione SOLO per l-OSSERVATORE** *(l-isotropia, il disegno
    `3D`)*, e ### **mai per la fisica** *(`[[DOMANDA-D9-GEOMETRIA]]`, `A17`)*.
    """
    return np.random.default_rng(seme).random((n, 3))


def punti3d_rilassati(n, seme=11, giri=20):
    """### `(ii)` **PUNTI CHE SI RESPINGONO**: rilassamento di Lloyd **sul toro**.

    ### \u26d4 **E LA FORMA SI DICHIARA, perche' non e' il Lloyd esatto:** il Lloyd vero
    sposta ogni punto nel ### **baricentro della sua cella di Voronoi**, che in `3D`
    periodico vuole il diagramma. ### **Qui si sposta ogni punto nel baricentro dei suoi
    vicini piu' prossimi**, sul toro, per un numero di giri ### **dichiarato** -- e
    l'effetto si ### **MISURA** *(la distribuzione della distanza al primo vicino)* invece
    di affermarlo.

    ### \u26a0 **E il baricentro si calcola CON LE DIFFERENZE PERIODICHE**, altrimenti due
    punti ai lati opposti del cubo si attirerebbero ### **attraverso il centro.**
    """
    p = np.random.default_rng(seme).random((n, 3))
    k = 12
    # ### ⛔ **SOPRA `MAX_N2` LA MATRICE `n x n` NON SI FA:** `8 n²` byte sono
    # ### ### **`5.4` GB a `n = 26000`.** ### ⚠ **E LA VIA VECCHIA RESTA INTATTA SOTTO
    # ### LA SOGLIA**, perche- i numeri di `0a2fd13` sono misurati a `n = 1728` e ###
    # ### **devono restare riproducibili AL BIT** -- la via nuova somma in un ### **ORDINE
    # ### DIVERSO**, quindi ### **non e- bit-identica**, e il braccio del banco ###
    # ### **MISURA la differenza** invece di dichiararla nulla.
    if n > MAX_N2:
        return _rilassa_albero(p, n, k, giri)
    for _ in range(giri):
        d2 = _d2_periodica(p)
        np.fill_diagonal(d2, np.inf)
        vic = np.argpartition(d2, k, axis=1)[:, :k]
        nuovo = np.empty_like(p)
        for i in range(n):
            dv = p[vic[i]] - p[i]
            dv = dv - np.round(dv)
            nr = np.linalg.norm(dv, axis=1)
            buoni = nr > 0
            if not np.any(buoni):
                nuovo[i] = p[i]
                continue
            # ### ⛔ **SI RESPINGONO, E AL PRIMO GIRO AVEVO IL SEGNO SBAGLIATO:**
            # ### muovere ogni punto ### **VERSO** il baricentro dei vicini e-
            # ### ### **CONTRAZIONE**, non repulsione -- i punti si ammassano, e la scena
            # ### diventava ### **una catena** *(`d_s = 1.214`, diametro `40`)*.
            # ### ⭐ **E L-HA PRESO LA SOGLIA `s5` CHE AVEVO SCRITTO PRIMA**
            # ### *(`|d_s - 3| <= 0.3`)*: ### **la dimensione e- il controllo della
            # ### costruzione.**
            # ### ✅ **La repulsione: la somma dei versori che vanno DAI vicini A `i`**,
            # ### pesata come `1/distanza` *(i piu- vicini spingono di piu-)*, e un passo
            # ### proporzionale alla distanza media -- cosi- ### **non c-e- una lunghezza
            # ### scelta a mano.**
            u = -dv[buoni] / nr[buoni, None]
            spinta = (u / nr[buoni, None]).sum(axis=0)
            sn = np.linalg.norm(spinta)
            passo = 0.2 * float(np.mean(nr[buoni]))
            nuovo[i] = p[i] + (passo * spinta / sn if sn > 0 else 0.0)
        p = np.mod(nuovo, 1.0)
    return p


def _rilassa_albero(p, n, k, giri):
    """### Lo stesso rilassamento, ### **con l-albero spaziale e SENZA cicli per punto.**

    ### ⭐ **LA LEGGE E- LA STESSA, riga per riga:** i `k` vicini piu- prossimi sul
    toro, la spinta `somma dei versori DAI vicini A i`, pesata `1/distanza`, e il passo
    ### **`0.2` volte la distanza media** -- ### **nessuna lunghezza scelta a mano.**
    """
    from scipy.spatial import cKDTree
    for _ in range(giri):
        _dd, ii = cKDTree(p, boxsize=1.0).query(p, k=min(k + 1, n))
        vic = ii[:, 1:]
        dv = p[vic] - p[:, None, :]
        dv = dv - np.round(dv)
        nr = np.linalg.norm(dv, axis=2)
        buoni = nr > 0
        inv = np.where(buoni, 1.0 / np.where(buoni, nr, 1.0), 0.0)
        u = np.where(buoni[:, :, None], -dv * inv[:, :, None], 0.0)
        spinta = (u * inv[:, :, None]).sum(axis=1)
        sn = np.linalg.norm(spinta, axis=1)
        quanti = buoni.sum(axis=1)
        # ### ⛔ **NESSUN `np.maximum` NEANCHE QUI:** la media si calcola ### **solo
        # ### dove ci sono vicini**, con una maschera -- ### **non con un pavimento sul
        # ### denominatore** *(`A11`: un pavimento vuole un errore trovato)*.
        media = np.zeros(n, dtype=float)
        ha = quanti > 0
        media[ha] = (nr * buoni).sum(axis=1)[ha] / quanti[ha]
        muove = sn > 0
        delta = np.zeros_like(p)
        delta[muove] = ((0.2 * media[muove]) / sn[muove])[:, None] * spinta[muove]
        p = np.mod(p + delta, 1.0)
    return p


def _d2_periodica(p):
    """### Le distanze al quadrato **SUL TORO**: `min(|d|, 1-|d|)` per asse.

    ### ⛔ **PERIODICA, e non e' un dettaglio: e- <<per non avere bordi>>** -- il mandato
    lo chiede alla lettera. ### **Un cubo con bordi ha i nodi d-angolo con grado basso**, e
    quelli ### **non sono <<3D isotropo in media>>: sono un bordo.**
    """
    d = np.abs(p[:, None, :] - p[None, :, :])
    d = np.minimum(d, 1.0 - d)
    return (d ** 2).sum(axis=2)


def geometrico3d(n, gmin=2, gmax=6, seme=11, rilassati=False):
    """### `G3`, **LA SCENA PRINCIPALE**: grafo geometrico `3D` **PERIODICO**, posizioni SCARTATE.

    ### ⛔ **Le posizioni vivono SOLO dentro questa funzione:** la scena che esce
    ### **non ha nessun campo di posizione**, e nessuno le puo' leggere. ### **Per
    l-osservatore si richiamano con `punti3d(n, seme)`**, che le ricostruisce
    ### **identiche** perche' il seme e' lo stesso.
    """
    p = punti3d_rilassati(n, seme) if rilassati else punti3d(n, seme)
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

    # ### ⭐ **TUTTE le coppie CANDIDATE, ordinate per DISTANZA**: cosi- il grafo e-
    # ### ### **geometrico** *(i vicini sono vicini)*, e ### **deterministico** *(l-ordine
    # ### e- quello delle distanze, e i pari merito si rompono con l-indice)*.
    # ### ⛔ **E SOPRA `MAX_N2` LE COPPIE NON SI FANNO TUTTE:** la matrice `n x n` costa
    # ### ### **`5.4` GB a `n = 26000`**, e un albero spaziale periodico da- gli stessi
    # ### archi ### **perche- un nodo di grado `<= gmax` non si collega mai oltre il suo
    # ### `K_ALBERO`-esimo vicino.** ### ✅ **E LA REGRESSIONE LO VERIFICA:** a `n = 512` le
    # ### due vie danno ### **lo STESSO insieme di archi.**
    if n <= MAX_N2:
        d2 = _d2_periodica(p)
        iu = np.triu_indices(n, 1)
        ordine = np.lexsort((iu[1], iu[0], d2[iu]))
        coppie = [(int(iu[0][q]), int(iu[1][q])) for q in ordine]

        def dist2(x, y):
            return float(d2[x, y])
    else:
        from scipy.spatial import cKDTree
        tr = cKDTree(p, boxsize=1.0)
        dd, ii = tr.query(p, k=min(K_ALBERO + 1, n))
        cand = {}
        for x in range(n):
            for j in range(1, ii.shape[1]):
                y = int(ii[x, j])
                if y == x:
                    continue
                a2, b2 = (x, y) if x < y else (y, x)
                cand[(a2, b2)] = float(dd[x, j]) ** 2
        chiavi = sorted(cand, key=lambda k2: (cand[k2], k2[0], k2[1]))
        coppie = list(chiavi)

        def dist2(x, y):
            a2, b2 = (x, y) if x < y else (y, x)
            return cand.get((a2, b2), float("inf"))

    for u, v in coppie:
        if grado.min() >= gmin and len(archi) >= n:
            # ### si continua solo finche- serve: ### **gradi almeno `gmin`**
            if grado[u] >= gmin and grado[v] >= gmin:
                continue
        aggiungi(u, v)
        if grado.min() >= gmin and len(archi) >= 2 * n:
            break
    # ### ⛔ **E IL GRAFO DEVE ESSERE CONNESSO**, altrimenti ### **meta- delle letture non
    # ### vorrebbe dire niente** -- si attacca il resto al piu- vicino gia- connesso.
    nome = "geometrico3d(n=%d,seme=%d%s%s)" % (
        n, seme, ",rilassati" if rilassati else "",
        ",gradi=%d-%d" % (gmin, gmax) if (gmin, gmax) != (2, 6) else "")
    sc = SC.costruisci(n, sorted(archi), nome)
    d = SC.distanze(sc, 0)
    giro = 0
    while int(np.sum(d < 0)) > 0 and giro < 64:
        giro += 1
        fuori = [k for k in range(n) if d[k] < 0]
        dentro = [k for k in range(n) if d[k] >= 0]
        best = None
        for u in fuori:
            j = min(dentro, key=lambda w: dist2(u, w))
            if best is None or dist2(u, j) < dist2(best[0], best[1]):
                best = (u, j)
        if best is None or not aggiungi(best[0], best[1]):
            # ### se non si puo- attaccare, si alza il tetto SOLO per quell-arco e
            # ### ### **si dichiara**: un grafo sconnesso sarebbe peggio
            u, j = best
            archi.add((min(u, j), max(u, j)))
            grado[u] += 1
            grado[j] += 1
        sc = SC.costruisci(n, sorted(archi), nome)
        d = SC.distanze(sc, 0)
    # ### ⛔ **E QUI LE POSIZIONI MUOIONO:** `sc` non le contiene, e `p` esce di scope.
    del p
    return sc


# =====================================================================================
#   LA DIMENSIONE SPETTRALE
# =====================================================================================
def ritorno(sc, da, passi, pigra=True):
    """### `p(t)`: la probabilita' di ritorno di una passeggiata **CLASSICA** su `da`.

    ### ⛔ **PIGRA:** meta' ferma, meta' si muove — perche' il cubico e' ### **BIPARTITO**
    e una passeggiata semplice darebbe `p(t) = 0` a ogni `t` dispari.
    """
    n = sc["n"]
    nodo = sc["nodo"]
    g = sc["grado"].astype(float)
    p = np.zeros(n, dtype=float)
    p[da] = 1.0
    fuori = []
    for _t in range(1, passi + 1):
        # ### ogni nodo manda `p/grado` a ogni vicino: si passa dalle ESTREMITA-
        manda = (p / g)[nodo]
        # ### l-estremita- `2a` sta su `u` e manda a `v` = il nodo di `2a+1`
        part = nodo.reshape(-1, 2)[:, ::-1].reshape(-1)
        q = np.zeros(n, dtype=float)
        np.add.at(q, part, manda)
        p = 0.5 * p + 0.5 * q if pigra else q
        fuori.append(float(p[da]))
    return fuori


def dimensione_spettrale(sc, diam, semi_nodi=(0,), passi=None):
    """### `d_s` da `p(t) ~ t^(-d_s/2)`, sulla finestra **derivata** `t < diametro²`.

    Ritorna anche ### **la bonta' della legge di potenza**: se `log p` contro `log t` non
    e' una retta, ### **non c'e' una potenza** — e si scrive cosi' invece di dare un numero
    finto.
    """
    tmax = passi if passi is not None else max(16, min(600, 4 * diam * diam))
    pend, r2, serie = [], [], []
    for da in semi_nodi:
        p = ritorno(sc, int(da), tmax)
        t = np.arange(1, tmax + 1, dtype=float)
        # ### la finestra: si scarta il transitorio iniziale *(`t < 4`)* e si sta sotto
        # ### ### **`diametro²`**, cioe- sotto il tempo in cui una diffusione tocca il bordo
        # ### ⛔ **LA FINESTRA FINISCE DOVE LA PASSEGGIATA SATURA, e il valore di
        # ### saturazione NON E- UNA COSTANTE SCELTA: e- `1/n`**, la distribuzione
        # ### uniforme. ### ⚠ **Al primo giro la finestra era `t <= diametro²`**, e su
        # ### un cubico `L = 5` quello vuol dire `t <= 36` mentre la potenza vale solo
        # ### finche- la diffusione sta DENTRO la cella *(`t ~ L²/4 ~ 6`)*: il resto era
        # ### ### **la saturazione**, e appiattiva la pendenza *(`d_s = 2.477`, `r² =
        # ### 0.977`)*. ### ✅ **Adesso si ferma a `p(t) >= 4/n`**, cioe-
        # ### ### **quattro volte il valore uniforme.**
        pa = np.asarray(p)
        dove = (t >= 4) & (pa >= 4.0 / sc["n"]) & (pa > 0)
        x = np.log(t[dove])
        y = np.log(np.asarray(p)[dove])
        if x.size < 4:
            continue
        a, b = np.polyfit(x, y, 1)
        yy = a * x + b
        ss = float(np.sum((y - yy) ** 2))
        st = float(np.sum((y - y.mean()) ** 2))
        pend.append(float(a))
        r2.append(1.0 - ss / st if st > 0 else 0.0)
        serie.append({"nodo": int(da), "pendenza": float(a),
                      "r2": (1.0 - ss / st if st > 0 else 0.0),
                      "finestra": [float(t[dove][0]), float(t[dove][-1])],
                      "punti": int(x.size)})
    if not pend:
        return {"d_s": float("nan"), "r2": float("nan"), "potenza": False,
                "nota": "finestra troppo corta", "per_nodo": []}
    ds = -2.0 * float(np.mean(pend))
    rq = float(np.mean(r2))
    return {"d_s": ds, "r2": rq,
            # ### ⛔ **<<C-E- UNA POTENZA>> E- UNA SOGLIA DICHIARATA:** `r² >= 0.98`.
            # ### Sotto quella, `log p` contro `log t` ### **non e- una retta**, e un
            # ### `d_s` sarebbe ### **un numero finto.**
            "potenza": bool(rq >= 0.98),
            "soglia_r2": 0.98,
            "per_nodo": serie,
            "nota": ("legge di potenza" if rq >= 0.98
                     else "NESSUNA legge di potenza: il decadimento non e- una potenza")}


# =====================================================================================
#   L-ISOTROPIA DELLA PROPAGAZIONE  --  e le posizioni sono SOLO DA OSSERVATORE
# =====================================================================================
# ### ⛔ **LE DIREZIONI SONO UN INSIEME FISSO E DICHIARATO:** i `26` vettori del cubo
# ### *(`6` assi, `12` spigoli, `8` diagonali)*, normalizzati. ### **Non sono scelti
# ### guardando i numeri**, e sono gli stessi per ogni scena.
def _direzioni():
    v = []
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            for c in (-1, 0, 1):
                if (a, b, c) != (0, 0, 0):
                    u = np.array([a, b, c], dtype=float)
                    v.append(u / np.linalg.norm(u))
    return np.array(v)


DIREZIONI = _direzioni()


def nodi_a_caso(sc, quanti=40, seme=1):
    """### I nodi di partenza, **deterministici dal seme**: il mandato dice `40`, seme `1`."""
    return np.random.default_rng(seme).choice(sc["n"], size=min(quanti, sc["n"]),
                                              replace=False)


def isotropia(sc, pos, passi=6, nodi=(0,), versori_uguali=False, eps=0.5, peso=None):
    """### La dispersione della velocita' del fronte **fra DIREZIONI**.

    ### ⛔ **LE POSIZIONI SERVONO SOLO A LEGGERE:** si usano per dire *«in che direzione
    sta questo nodo»*, e ### **la camminata non le vede** — un braccio del banco lo
    verifica sul sorgente.

    ### ⭐ **E I DUE BRACCI SEPARANO DUE EFFETTI, come il mandato chiede:** l-anisotropia
    del `~14%` misurata nel `v3` viene dai ### **VERSORI assegnati per indice d-arco**
    *(`[[PROVV-VERSORI-NON-RELAZIONALI]]`)*, ### **non dal grafo** — quindi si misura
    ### **con i versori del `v3`** e ### **con i versori TUTTI UGUALI**, e la differenza
    ### **e- il contributo dei versori.**
    """
    import camminata as CM
    import camminata2 as C2
    import geometria as GE
    geo = GE.scena_identita(sc)
    if versori_uguali:
        geo = dict(geo)
        u = np.zeros_like(geo["n"])
        u[:, 2] = 1.0
        geo["n"] = u
    uno_r = np.ones(sc["n"], dtype=float)

    def passo(v):
        """### Il passo lineare `v2`, col Grover ### **PESATO** se `peso` c-e-."""
        if peso is None:
            return C2.passo2(v, sc, geo, uno_r, 1.0, eps)
        import pesi4 as P4
        x = C2.moneta_spin(v, geo, eps, uno_r * 1.0, sc)
        x = P4.grover_pesato(x, sc, peso)
        return C2.spostamento_trasporto(x, geo, sc)
    per_nodo = []
    for da in nodi:
        da = int(da)
        d = SC.distanze(sc, da)
        # ### la direzione di ogni nodo, **sul toro**, e il cono a cui appartiene
        dv = pos - pos[da]
        dv = dv - np.round(dv)
        nr = np.linalg.norm(dv, axis=1)
        buoni = nr > 0
        cono = np.full(sc["n"], -1, dtype=int)
        cono[buoni] = np.argmax((dv[buoni] / nr[buoni, None]) @ DIREZIONI.T, axis=1)
        psi = CM.stato_zero(sc)
        for e in range(2 * sc["m"]):
            if int(sc["nodo"][e]) == da:
                psi[e, 0] = 1.0
        psi = psi / math.sqrt(CM.norma(psi))
        for _ in range(passi):
            psi = passo(psi)
        rho = CM.rho_nodo(psi, sc)
        # ### \u26d4 **DUE MISURANDI, E RISPONDONO A DUE DOMANDE DIVERSE:**
        # ### \u2b50 **`grafo`**: la distanza DI GRAFO media per cono. ### **E- isotropa
        # ### per costruzione su un reticolo** *(la distanza di grafo del cubico E- la `L1`)*,
        # ### quindi dice ### **se il GRAFO e- regolare**, non se le onde lo sono.
        # ### \u2b50 **`euclideo`**: la distanza EUCLIDEA media per cono. ### **E- QUESTO il
        # ### fatto del mandato:** una palla in distanza di grafo sul cubico e- un
        # ### ### **OTTAEDRO nello spazio**, quindi il fronte va piu' lontano ### **lungo
        # ### gli assi** -- gli <<spigoli>> che il rilievo nomina.
        # ### \u26a0 **Riportarne uno solo sarebbe rispondere a una domanda diversa da
        # ### quella posta**, e il primo giro l-ho fatto.
        # ### \u26d4 **IL PROFILO PER DIREZIONE SI CONSERVA, allineato alle `26`
        # ### direzioni**, con `nan` dove il cono e- VUOTO: ### **senza l-allineamento il
        # ### profilo MEDIO non si puo- fare.**
        pg = np.full(len(DIREZIONI), np.nan)
        pe = np.full(len(DIREZIONI), np.nan)
        for j in range(len(DIREZIONI)):
            dove = (cono == j) & (d >= 0)
            w = float(np.sum(rho[dove]))
            if w <= 0:
                continue
            pg[j] = float(np.sum(rho[dove] * d[dove]) / w) / passi
            pe[j] = float(np.sum(rho[dove] * nr[dove]) / w) / passi
        vel_g = pg[np.isfinite(pg)]
        vel_e = pe[np.isfinite(pe)]
        if vel_g.size < 4:
            continue

        def disp(v):
            m = float(np.mean(v))
            return (float(np.std(v, ddof=1) / m) if m > 0 else float("nan"))
        per_nodo.append({"nodo": da, "coni_usati": int(vel_g.size),
                         "velocita_media_grafo": float(np.mean(vel_g)),
                         "velocita_media_euclidea": float(np.mean(vel_e)),
                         "relativa": disp(vel_g),
                         "relativa_euclidea": disp(vel_e),
                         "profilo_grafo": pg.tolist(),
                         "profilo_euclideo": pe.tolist()})
    if not per_nodo:
        return {"irregolarita": float("nan"), "anisotropia": float("nan"),
                "rumore": float("nan"), "nota": "coni troppo pochi", "per_nodo": []}
    # ### \u26d4 **LE TRE GRANDEZZE, E SONO TRE COSE DIVERSE** *(correzione del guardiano,
    # ### `2026-10-11`)*:
    # ### \u2b50 **`irregolarita`** = la media delle dispersioni ### **PER NODO**. Su un
    # ### grafo irregolare misura ### **quanto e- irregolare il vicinato di quel nodo**,
    # ### non una dipendenza dalla direzione. ### **E- quello che misuravo prima, e lo
    # ### chiamavo <<anisotropia>>: era il difetto.**
    # ### \u2b50 **`anisotropia`** = la dispersione del ### **PROFILO MEDIO**: si media il
    # ### profilo per direzione ### **su tutti i nodi**, e POI si guarda la dispersione.
    # ### **Questa e- l-anisotropia**, cioe- una dipendenza ### **SISTEMATICA** dalla
    # ### direzione.
    # ### \u2b50 **`rumore`** = il livello atteso dal solo rumore: la dispersione per nodo
    # ### ### **diviso la radice del numero di nodi.** ### **Senza di lui l-anisotropia non
    # ### si sa leggere.**
    def tre(chiave, prof):
        rel = [x[chiave] for x in per_nodo]
        # ### il profilo MEDIO per direzione: `nanmean` perche- un cono puo- essere VUOTO
        M = np.array([x[prof] for x in per_nodo], dtype=float)
        with np.errstate(invalid="ignore"):
            medio = np.nanmean(M, axis=0)
        buoni = np.isfinite(medio)
        mm = float(np.mean(medio[buoni])) if np.any(buoni) else float("nan")
        aniso = (float(np.std(medio[buoni], ddof=1)) / mm
                 if (np.sum(buoni) > 1 and mm > 0) else float("nan"))
        irr = float(np.mean(rel))
        return {
            "irregolarita": irr,
            "sigma_irregolarita": (float(np.std(rel, ddof=1)) / math.sqrt(len(rel))
                                   if len(rel) > 1 else 0.0),
            "anisotropia": aniso,
            "rumore": irr / math.sqrt(len(per_nodo)),
            "coni_usati": int(np.sum(buoni)),
            # ### \u26d4 **IL VERDETTO E- UN RAPPORTO, non un numero nudo:** l-anisotropia
            # ### ### **contro il rumore atteso.** Sopra `3` e- sistematica.
            "aniso_su_rumore": (aniso / (irr / math.sqrt(len(per_nodo))))
            if (aniso == aniso and irr > 0) else float("nan"),
            "sistematica": bool(aniso == aniso and irr > 0
                                and aniso > 3.0 * irr / math.sqrt(len(per_nodo)))}
    g = tre("relativa", "profilo_grafo")
    e = tre("relativa_euclidea", "profilo_euclideo")
    return {"grafo": g, "euclideo": e,
            # ### le vecchie chiavi restano, per non rompere chi le legge
            "irregolarita": g["irregolarita"], "anisotropia": e["anisotropia"],
            "rumore": e["rumore"],
            "nodi": len(per_nodo), "passi": passi,
            "versori_uguali": bool(versori_uguali),
            "pesato": bool(peso is not None),
            "direzioni": int(len(DIREZIONI)), "per_nodo": per_nodo}


def sbilanciamento(sc, pos, peso=None):
    """### Lo SBILANCIAMENTO direzionale delle uscite, **per nodo**.

    `|somma dei versori geometrici degli archi, PESATI come la variante li pesa| / somma
    dei pesi`. ### **Zero vuol dire uscite perfettamente bilanciate**; uno vuol dire tutte
    nella stessa direzione.

    ### ⛔ **LE POSIZIONI SONO SOLO DA OSSERVATORE**, e il mandato lo dice: servono a
    sapere *«in che direzione va questo arco»*, e ### **la camminata non le vede.**
    """
    ne = 2 * sc["m"]
    w = np.ones(ne) if peso is None else np.asarray(peso, dtype=float)
    part = sc["nodo"].reshape(-1, 2)[:, ::-1].reshape(-1)
    dv = pos[part] - pos[sc["nodo"]]
    dv = dv - np.round(dv)
    nr = np.linalg.norm(dv, axis=1)
    buoni = nr > 0
    u = np.zeros_like(dv)
    u[buoni] = dv[buoni] / nr[buoni, None]
    som = np.zeros((sc["n"], 3), dtype=float)
    tot = np.zeros(sc["n"], dtype=float)
    np.add.at(som, sc["nodo"], w[:, None] * u)
    np.add.at(tot, sc["nodo"], w)
    out = np.zeros(sc["n"], dtype=float)
    dove = tot > 0
    out[dove] = np.linalg.norm(som[dove], axis=1) / tot[dove]
    return out


def correlazione(sc, pos, r, peso=None):
    """### La correlazione fra lo **sbilanciamento** di un nodo e l'**irregolarita'** del
    fronte che parte da la'. ### **Serve a dire se lo sbilanciamento SIA la causa.**"""
    sb = sbilanciamento(sc, pos, peso)
    xs, ys = [], []
    for q in r.get("per_nodo", []):
        v = q.get("relativa_euclidea")
        if v == v:
            xs.append(float(sb[int(q["nodo"])]))
            ys.append(float(v))
    if len(xs) < 4:
        return {"pearson": float("nan"), "nodi": len(xs),
                "nota": "troppi pochi nodi"}
    x = np.array(xs)
    y = np.array(ys)
    rho = float(np.corrcoef(x, y)[0, 1])
    # ### ⛔ **LA `sigma` DI UN PEARSON, dalla forma di Fisher:** `1/sqrt(N-3)` sulla
    # ### `z`, e si riporta ### **in quante `sigma`** sta il coefficiente.
    nn = len(xs)
    sz = 1.0 / math.sqrt(max(nn - 3, 1))
    z = 0.5 * math.log((1 + rho) / (1 - rho)) if abs(rho) < 1 else float("inf")
    return {"pearson": rho, "nodi": nn, "sigma_z": sz,
            "in_sigma": abs(z) / sz if sz > 0 else float("inf"),
            "significativa": bool(abs(z) > 3.0 * sz),
            "sbilanciamento_medio": float(np.mean(x)),
            "sbilanciamento_sigma": float(np.std(x, ddof=1) / math.sqrt(nn))}


def etichetta(nome, aniso=None, soglia=3.0):
    # ### \u26d4 **L-ETICHETTA USA L-ANISOTROPIA DEL PROFILO MEDIO CONTRO IL RUMORE
    # ### ATTESO** *(correzione del guardiano)*: `aniso` e- il ### **rapporto
    # ### `anisotropia / rumore`**, e la soglia e- ### **`3`.**
    # ### \u26a0 **Prima era <<il `10%` della dispersione per nodo>>, e quella e-
    # ### IRREGOLARITA- LOCALE, non anisotropia.**
    """### `1D` / `3D isotropa` / `3D anisotropa` / `casuale`.

    ### ⛔ **E <<isotropa>> E- UNA SOGLIA DICHIARATA**, non un giudizio: anisotropia
    relativa ### **`<= 10%`** coi versori del `v3`. ### **Senza la misura si dice <<3D, da
    misurare>>**, non si indovina.
    """
    if nome.startswith("regolare"):
        return "1D"
    if nome.startswith("cubico") or nome.startswith("geometrico3d"):
        if aniso is None or aniso != aniso:
            return "3D, da misurare"
        return "3D isotropa" if aniso <= soglia else "3D anisotropa"
    return "casuale"


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    SC._niente_simulatore()
    print("  LE TRE GRANDEZZE: irregolarita- per nodo, anisotropia del PROFILO MEDIO,")
    print("  e il RUMORE ATTESO. ### **La terza e- quella che fa leggere la seconda.**")
    print()
    print("  %-30s %-7s %-6s %-7s %-9s %-9s %-9s %s"
          % ("la scena", "n", "diam", "d_s", "irregol.", "aniso", "rumore",
             "aniso/rumore"))
    for nome, sc in (("cubico L=8", cubico(8)),
                     ("cubico L=12", cubico(12)),
                     ("(i) geometrico n=512", geometrico3d(512)),
                     ("(i) geometrico n=1728", geometrico3d(1728)),
                     ("(ii) rilassati n=512", geometrico3d(512, rilassati=True)),
                     ("(iii) gradi 4-6 n=512", geometrico3d(512, gmin=4, gmax=6)),
                     ("regolare n=120", SC.regolare(120))):
        diam = max(int(SC.distanze(sc, k).max())
                   for k in range(0, sc["n"], max(1, sc["n"] // 24)))
        ds = dimensione_spettrale(sc, diam, semi_nodi=(0, sc["n"] // 3, sc["n"] // 2))
        pos = None
        if sc["nome"].startswith("cubico"):
            pos = punti_cubico(int(round(sc["n"] ** (1.0 / 3.0))))
        elif sc["nome"].startswith("geometrico3d"):
            pos = (punti3d_rilassati(sc["n"], 11) if "rilassati" in sc["nome"]
                   else punti3d(sc["n"], 11))
        if pos is None:
            print("  %-30s %-7d %-6d %-7.3f %-9s %-9s %-9s %s"
                  % (nome, sc["n"], diam, ds["d_s"], "--", "--", "--", "1D"))
            continue
        r = isotropia(sc, pos, nodi=nodi_a_caso(sc, 40, 1))
        e = r["euclideo"]
        print("  %-30s %-7d %-6d %-7.3f %-9.3f %-9.4f %-9.4f %.2f  %s"
              % (nome, sc["n"], diam, ds["d_s"], e["irregolarita"], e["anisotropia"],
                 e["rumore"], e["aniso_su_rumore"],
                 "### SISTEMATICA" if e["sistematica"] else "al livello del rumore"))
