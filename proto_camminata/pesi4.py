# -*- coding: utf-8 -*-
r"""LA VARIANTE `(iv)` — **tutti i vicini collegati, e un PESO che non viene dalle posizioni.**

> ## ⛔ **IL VINCOLO DI LUCA, ED E' QUELLO CHE DECIDE LA FORMA:** i pesi ### **NON devono
> ## rimettere le posizioni nella fisica** *(`[[DOMANDA-D9-GEOMETRIA]]`)*. ### **Un peso
> ## calcolato da distanze o aree EUCLIDEE e' una copia della geometria messa a mano**, anche
> ## se i punti vengono poi scartati.

| | il braccio | il peso | legge le posizioni? |
|---|---|---|---|
| `U` | **UGUALI** | tutti `1` — ### **il RIFERIMENTO** | ### ✅ **no** |
| `R` | **RELAZIONALI** | `w_ij = \|N(i) ∩ N(j)\|` *(i vicini comuni, cioe' i triangoli che contengono l'arco)* | ### ✅ **no** |
| `Rn` | **RELAZIONALI normalizzati** | `w_ij = \|N(i) ∩ N(j)\| / sqrt(d_i d_j)` | ### ✅ **no** |
| `V` | **VORONOI** | area della faccia comune / distanza | ### ⛔ **SI'** — e per questo e' ### **un CONTROLLO dichiarato, non il riferimento** |

### ⭐ **IL GROVER PESATO, e la matematica e' VERIFICATA** *(task history del `2026-10-11`)*:
`G_w = 2|w⟩⟨w|/⟨w|w⟩ − I` con `w_a = sqrt(peso)`.

| | misurato |
|---|---|
| **reale** *(quindi `C` regge)* | `max\|Im M\|` = **`0`** |
| **ermitiana**, **involuzione**, **unitaria** | **`0`** .. **`4.5e-16`** |
| **locale** | elementi fra nodi diversi: ### **`0` ESATTO** |
| a pesi **uguali** = il Grover del `v3` | ### ⭐ **`0`, AL BIT** *(nessun cortocircuito serve)* |
| un peso **nullo** stacca l'uscita | colonna con ### **UN SOLO** elemento, diagonale ### **`−1`** |
| la **`C`** | **`0`** con pesi uguali ### **e** casuali |

### ⛔ **E IL FATTO CHE CAMBIA IL QUADRO, misurato: LA DELAUNAY `3D` HA GRADO MEDIO `15.5`**,
non `2..6`. ### **Quindi questa variante NON aggiunge solo pesi: TRIPLICA IL GRADO**, e
### **Grover dipende dal grado** — e' una scena ### **diversa**, non la stessa con dei
pesi. ### **La scelta fra le varianti e' di Luca.**

### ⚠ **E `scipy.spatial` ENTRA SOLO QUI, nel COSTRUTTORE DI SCENA:** e' una
### **condizione iniziale**, e ### **mai il passo** — un braccio del collaudo lo
verifica sul sorgente.

### ⚠ **NESSUN `clip`, NESSUNA costante tarata.** I pesi entrano **solo come rapporti dentro
il nodo**, e un braccio verifica che ### **scalare tutti i pesi di un nodo non cambi
niente.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import scena as SC                                             # noqa: E402

BRACCI = ("U", "R", "Rn", "V")
# ### ⛔ **QUALI BRACCI LEGGONO LE POSIZIONI:** dichiarato, e un braccio del collaudo lo
# ### verifica ### **sul sorgente** invece di crederci.
LEGGE_POSIZIONI = {"U": False, "R": False, "Rn": False, "V": True}


def grover_pesato(psi, sc, peso):
    """### `G_w = 2|w><w|/<w|w> - I` **a blocchi per nodo**, su scalare o spinore.

    ### ⭐ **Una sola passata sugli archi**, e ### **a pesi uguali da' il Grover del `v3`
    AL BIT** *(misurato)*.
    """
    w = np.sqrt(np.asarray(peso, dtype=float))
    den = np.zeros(sc["n"], dtype=float)
    np.add.at(den, sc["nodo"], w * w)
    k = sc["nodo"]
    v = np.asarray(psi)
    ww = w.reshape((-1,) + (1,) * (v.ndim - 1))
    num = np.zeros((sc["n"],) + v.shape[1:], dtype=complex)
    np.add.at(num, sc["nodo"], ww * v)
    dk = den[k].reshape((-1,) + (1,) * (v.ndim - 1))
    out = -v.copy()
    buoni = den[k] > 0.0
    out[buoni] = (2.0 * ww[buoni] * (num[k][buoni] / dk[buoni])) - v[buoni]
    return out


# =====================================================================================
#   LA DELAUNAY PERIODICA  --  e le posizioni SI SCARTANO
# =====================================================================================
def delaunay_periodica(n, seme=11):
    """### Gli archi della **Delaunay periodica** di `n` punti nel cubo, e i punti con loro.

    ### ⛔ **LE POSIZIONI ESCONO SOLO PER COSTRUIRE I PESI E PER L'OSSERVATORE:** la scena
    che si costruisce da questi archi ### **non le contiene**, ed e' ### **una condizione
    iniziale dichiarata** — le posizioni decidono ### **solo CHI e' collegato**, come
    gia' oggi.

    ### ⚠ **PERIODICA con le `27` copie:** si triangola il blocco `3x3x3` e si tengono gli
    archi che ### **toccano la cella centrale**. ### **Senza la periodicita' i nodi di bordo
    avrebbero un grado diverso, e quello non e' <<`3D` uniforme>>: e' un BORDO.**
    """
    from scipy.spatial import Delaunay
    p = np.random.default_rng(seme).random((n, 3))
    off = np.array([[i, j, k] for i in (-1, 0, 1) for j in (-1, 0, 1)
                    for k in (-1, 0, 1)], dtype=float)
    centro = int(np.flatnonzero((off == 0).all(axis=1))[0])
    P = (p[None, :, :] + off[:, None, :]).reshape(-1, 3)
    tri = Delaunay(P)
    archi = set()
    for s in tri.simplices:
        for u in range(4):
            for v in range(u + 1, 4):
                a, b = int(s[u]), int(s[v])
                if (a // n == centro) or (b // n == centro):
                    x, y = a % n, b % n
                    if x != y:
                        archi.add((min(x, y), max(x, y)))
    return sorted(archi), p


def scena_delaunay(n, seme=11):
    """### La scena della variante `(iv)`: ### **senza nessun campo di posizione.**"""
    archi, _p = delaunay_periodica(n, seme)
    return SC.costruisci(n, archi, "delaunay(n=%d,seme=%d)" % (n, seme))


def punti_delaunay(n, seme=11):
    """### I punti, **per l'OSSERVATORE**: si ricostruiscono dal seme, identici."""
    return np.random.default_rng(seme).random((n, 3))


# =====================================================================================
#   I PESI
# =====================================================================================
def peso_di(sc, braccio, seme=11):
    """### Il peso **per ESTREMITA' d'arco**, secondo il braccio scelto.

    ### ⛔ **`U`, `R` e `Rn` NON toccano `pos`:** si vede dalla firma, e il braccio del
    collaudo lo verifica ### **sul sorgente.**
    """
    assert braccio in BRACCI, "### braccio `%r` sconosciuto" % (braccio,)
    ne = 2 * sc["m"]
    if braccio == "U":
        return np.ones(ne, dtype=float)
    if braccio in ("R", "Rn"):
        vic = [set(x) for x in sc["vicini"]]
        g = sc["grado"].astype(float)
        w = np.empty(sc["m"], dtype=float)
        for a, (u, v) in enumerate(sc["archi"]):
            com = float(len(vic[u] & vic[v]))
            w[a] = com if braccio == "R" else com / math.sqrt(g[u] * g[v])
        return np.repeat(w, 2)
    # ### ⛔ **`V`: il CONTROLLO <<geometria a mano>>**, e legge le posizioni
    return _peso_voronoi(sc, seme)


def _peso_voronoi(sc, seme=11):
    """### `w = area della faccia comune / distanza`. ### **CONTROLLO: legge le posizioni.**

    ### ⚠ **L'area della faccia di Voronoi in `3D` non si calcola a mano in due righe:** si
    usa l'approssimazione ### **dichiarata** `area ~ (distanza fra i vicini comuni)^2`, cioe'
    il numero di vicini comuni come proxy del numero di spigoli della faccia, moltiplicato
    per la ### **distanza media** fra loro. ### ⛔ **E' un'approssimazione, e si dichiara:**
    il braccio `V` serve a ### **misurare quanto guadagna una geometria messa a mano**, non
    a essere esatto.
    """
    p = punti_delaunay(sc["n"], seme)
    vic = [set(x) for x in sc["vicini"]]
    w = np.empty(sc["m"], dtype=float)
    for a, (u, v) in enumerate(sc["archi"]):
        d = p[v] - p[u]
        d = d - np.round(d)
        dist = float(np.linalg.norm(d))
        com = sorted(vic[u] & vic[v])
        if len(com) < 3 or dist <= 0:
            w[a] = 0.0 if dist <= 0 else 1.0 / dist
            continue
        # ### il raggio medio dei vicini comuni dal punto medio dell-arco
        mezzo = p[u] + 0.5 * d
        rr = []
        for c in com:
            e = p[c] - mezzo
            e = e - np.round(e)
            rr.append(float(np.linalg.norm(e)))
        area = math.pi * (float(np.mean(rr)) ** 2)
        w[a] = area / dist
    return np.repeat(w, 2)


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    import vuoto3 as V3
    SC._niente_simulatore()
    print("  %-18s %-7s %-7s %-12s %s"
          % ("la scena", "n", "m", "gradi", "grado medio"))
    for n in (200, 1000):
        sc = scena_delaunay(n)
        print("  %-18s %-7d %-7d %-12s %.2f"
              % (sc["nome"], sc["n"], sc["m"],
                 "%d..%d" % (sc["grado"].min(), sc["grado"].max()),
                 float(sc["grado"].mean())))
    print()
    sc = scena_delaunay(200)
    ne = 2 * sc["m"]
    rng = np.random.default_rng(3)
    phi = rng.normal(size=ne) + 1j * rng.normal(size=ne)
    print("  %-6s %-10s %-10s %-10s %-12s %s"
          % ("brac", "min", "mediana", "max", "= v3 al bit?", "scala-invariante?"))
    for br in BRACCI:
        w = peso_di(sc, br)
        a = grover_pesato(phi, sc, w)
        b = grover_pesato(phi, sc, 3.0 * w)
        v3 = V3.grover_scalare(phi, sc)
        print("  %-6s %-10.4g %-10.4g %-10.4g %-12s %.3g"
              % (br, w.min(), float(np.median(w)), w.max(),
                 ("%.3g" % float(np.max(np.abs(a - v3)))) if br == "U" else "--",
                 float(np.max(np.abs(a - b)))))
