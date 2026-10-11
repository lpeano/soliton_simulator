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


def _d2_periodica(p):
    """### Le distanze al quadrato **SUL TORO**: `min(|d|, 1-|d|)` per asse.

    ### ⛔ **PERIODICA, e non e' un dettaglio: e- <<per non avere bordi>>** -- il mandato
    lo chiede alla lettera. ### **Un cubo con bordi ha i nodi d-angolo con grado basso**, e
    quelli ### **non sono <<3D isotropo in media>>: sono un bordo.**
    """
    d = np.abs(p[:, None, :] - p[None, :, :])
    d = np.minimum(d, 1.0 - d)
    return (d ** 2).sum(axis=2)


def geometrico3d(n, gmin=2, gmax=6, seme=11):
    """### `G3`, **LA SCENA PRINCIPALE**: grafo geometrico `3D` **PERIODICO**, posizioni SCARTATE.

    ### ⛔ **Le posizioni vivono SOLO dentro questa funzione:** la scena che esce
    ### **non ha nessun campo di posizione**, e nessuno le puo' leggere. ### **Per
    l-osservatore si richiamano con `punti3d(n, seme)`**, che le ricostruisce
    ### **identiche** perche' il seme e' lo stesso.
    """
    p = punti3d(n, seme)
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

    # ### ⭐ **TUTTE le coppie, ordinate per DISTANZA**: cosi- il grafo e- ### **geometrico**
    # ### *(i vicini sono vicini)*, e ### **deterministico** *(l-ordine e- quello delle
    # ### distanze, e i pari merito si rompono con l-indice)*.
    d2 = _d2_periodica(p)
    iu = np.triu_indices(n, 1)
    ordine = np.lexsort((iu[1], iu[0], d2[iu]))
    for q in ordine:
        u, v = int(iu[0][q]), int(iu[1][q])
        if grado.min() >= gmin and len(archi) >= n:
            # ### si continua solo finche- serve: ### **gradi almeno `gmin`**
            if grado[u] >= gmin and grado[v] >= gmin:
                continue
        aggiungi(u, v)
        if grado.min() >= gmin and len(archi) >= 2 * n:
            break
    # ### ⛔ **E IL GRAFO DEVE ESSERE CONNESSO**, altrimenti ### **meta- delle letture non
    # ### vorrebbe dire niente** -- si attacca il resto al piu- vicino gia- connesso.
    sc = SC.costruisci(n, sorted(archi), "geometrico3d(n=%d,seme=%d)" % (n, seme))
    d = SC.distanze(sc, 0)
    giro = 0
    while int(np.sum(d < 0)) > 0 and giro < 64:
        giro += 1
        fuori = [k for k in range(n) if d[k] < 0]
        dentro = [k for k in range(n) if d[k] >= 0]
        best = None
        for u in fuori:
            j = min(dentro, key=lambda w: d2[u, w])
            if best is None or d2[u, j] < d2[best[0], best[1]]:
                best = (u, j)
        if best is None or not aggiungi(best[0], best[1]):
            # ### se non si puo- attaccare, si alza il tetto SOLO per quell-arco e
            # ### ### **si dichiara**: un grafo sconnesso sarebbe peggio
            u, j = best
            archi.add((min(u, j), max(u, j)))
            grado[u] += 1
            grado[j] += 1
        sc = SC.costruisci(n, sorted(archi),
                           "geometrico3d(n=%d,seme=%d)" % (n, seme))
        d = SC.distanze(sc, 0)
    # ### ⛔ **E QUI LE POSIZIONI MUOIONO:** `sc` non le contiene, e `p` esce di scope.
    del p, d2
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


def isotropia(sc, pos, passi=6, nodi=(0,), versori_uguali=False, eps=0.5):
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
            psi = C2.passo2(psi, sc, geo, uno_r, 1.0, eps)
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
        vel_g, vel_e = [], []
        for j in range(len(DIREZIONI)):
            dove = (cono == j) & (d >= 0)
            w = float(np.sum(rho[dove]))
            if w <= 0:
                continue
            vel_g.append(float(np.sum(rho[dove] * d[dove]) / w) / passi)
            vel_e.append(float(np.sum(rho[dove] * nr[dove]) / w) / passi)
        if len(vel_g) < 4:
            continue

        def disp(v):
            m = float(np.mean(v))
            return (float(np.std(v, ddof=1) / m) if m > 0 else float("nan"))
        per_nodo.append({"nodo": da, "coni_usati": len(vel_g),
                         "velocita_media_grafo": float(np.mean(vel_g)),
                         "velocita_media_euclidea": float(np.mean(vel_e)),
                         "relativa": disp(vel_g),
                         "relativa_euclidea": disp(vel_e)})
    if not per_nodo:
        return {"anisotropia": float("nan"), "nota": "coni troppo pochi",
                "per_nodo": []}
    rel = [x["relativa"] for x in per_nodo]
    rel_e = [x["relativa_euclidea"] for x in per_nodo]
    return {"anisotropia": float(np.mean(rel)),
            "anisotropia_euclidea": float(np.mean(rel_e)),
            "sigma": (float(np.std(rel, ddof=1)) / math.sqrt(len(rel))
                      if len(rel) > 1 else 0.0),
            "sigma_euclidea": (float(np.std(rel_e, ddof=1)) / math.sqrt(len(rel_e))
                               if len(rel_e) > 1 else 0.0),
            "nodi": len(per_nodo), "passi": passi,
            "versori_uguali": bool(versori_uguali),
            "direzioni": int(len(DIREZIONI)), "per_nodo": per_nodo}


def etichetta(nome, aniso=None, soglia=0.10):
    # ### \u26d4 **L-ETICHETTA USA IL MISURANDO *EUCLIDEO*, perche- e- quello che il
    # ### rilievo nomina** *(<<il fronte ha spigoli lungo gli assi>>)*. ### **La soglia e-
    # ### `10%`, dichiarata PRIMA della corsa** *(sta in questa firma, scritta col codice)*.
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
    print("  (aniso: dispersione della velocita- del fronte fra 26 direzioni;")
    print("   `graf` = distanza di GRAFO, `eucl` = distanza EUCLIDEA; `=` = versori uguali)")
    print("  %-22s %-7s %-10s %-7s %-7s %-9s %-9s %-9s %-9s %s"
          % ("la scena", "n", "gradi", "diam", "d_s", "graf v3", "eucl v3",
             "graf =", "eucl =", "etichetta"))
    # ### ⭐ **LA DIMENSIONE SI MISURA SU SCENE GRANDI, e il motivo e- la FINESTRA:**
    # ### la potenza vale finche- la diffusione non satura, e su un reticolo piccolo quella
    # ### finestra e- ### **di pochi punti.** ### **La dimensione e- una proprieta- della
    # ### FAMIGLIA**, non della taglia usata per lo spettro -- e la passeggiata classica
    # ### costa ### **`O(m)` per passo**, quindi `n = 8000` e- gratis.
    for nome, sc in (("cubico L=5", cubico(5)),
                     ("cubico L=8", cubico(8)),
                     ("cubico L=12", cubico(12)),
                     ("cubico L=20", cubico(20)),
                     ("geometrico3d n=512", geometrico3d(512)),
                     ("geometrico3d n=4000", geometrico3d(4000)),
                     ("regolare n=120", SC.regolare(120)),
                     ("regolare n=2000", SC.regolare(2000)),
                     ("irregolare n=120", SC.irregolare(120)),
                     ("irregolare n=2000", SC.irregolare(2000))):
        diam = max(int(SC.distanze(sc, k).max())
                   for k in range(0, sc["n"], max(1, sc["n"] // 24)))
        ds = dimensione_spettrale(sc, diam, semi_nodi=(0, sc["n"] // 3, sc["n"] // 2))
        pos = None
        if sc["nome"].startswith("cubico"):
            pos = punti_cubico(int(round(sc["n"] ** (1.0 / 3.0))))
        elif sc["nome"].startswith("geometrico3d"):
            pos = punti3d(sc["n"], 11)
        ag = ae = agu = aeu = float("nan")
        if pos is not None:
            nodi = (0, sc["n"] // 3, sc["n"] // 2, 2 * sc["n"] // 3)
            r1 = isotropia(sc, pos, nodi=nodi)
            r2 = isotropia(sc, pos, nodi=nodi, versori_uguali=True)
            ag, ae = r1["anisotropia"], r1["anisotropia_euclidea"]
            agu, aeu = r2["anisotropia"], r2["anisotropia_euclidea"]
        print("  %-22s %-7d %-10s %-7d %-7.3f %-9s %-9s %-9s %-9s %s"
              % (nome, sc["n"],
                 "%d..%d" % (sc["grado"].min(), sc["grado"].max()), diam, ds["d_s"],
                 ("%.1f%%" % (100 * ag)) if ag == ag else "--",
                 ("%.1f%%" % (100 * ae)) if ae == ae else "--",
                 ("%.1f%%" % (100 * agu)) if agu == agu else "--",
                 ("%.1f%%" % (100 * aeu)) if aeu == aeu else "--",
                 etichetta(sc["nome"], ae)))
