# -*- coding: utf-8 -*-
r"""COME IL VUOTO FISSA `cs` — **tre candidate, e NON scelgo io** *(punto `A2` del mandato)*.

> ## ⛔ **LA FORMA PIU' OVVIA E' ESCLUSA DA UN NUMERO, PRIMA DI PROVARLA:** col fondo del
> ## `v3` ### **`Lambda_k = grado_k * lambda_0`** — misurato `min 2.000`, `max 6.000` su
> ## gradi da `2` a `6`, e ### **correlazione col grado `1.0000` ESATTA.** ### **Quindi
> ## `cs_k = f(Lambda_k)` non e' il vuoto: e' il GRADO**, cioe' la geometria del grafo.

| | la candidata | la grandezza | il costo, **misurato** |
|---|---|---|---|
| `dispersione` | `cs_k = 1/(1 + D_k)` con `D_k` = ### **varianza NON distorta di `\|phi\|²` sulle estremita' del nodo, diviso la media al quadrato** | ### **adimensionale**, e la sua **attesa non dipende dal grado** | ### ⚠ **correlazione col grado `-0.17`** *(tre semi: `-0.189`, `-0.154`, `-0.169`)*, e la ragione e' ### **Jensen**: l'attesa di `D` e' senza bias, ma quella di `1/(1+D)` no |
| `contrasto` | `cs_k = min/max` di `\|phi\|²` sulle estremita' | adimensionale | ### ⛔ **correlazione col grado `-0.45`**: con piu' estremita' il `min` scende e il `max` sale, quindi ### **e' un artefatto degli ESTREMI**, non fisica |
| `densita` | `cs_k = f(Lambda_k / grado_k)` | ### ⛔ **ha una SCALA** *(serve `lambda_0`)* | ### **IL BRACCIO DI CONTROLLO**, e dichiara il difetto |

### ⭐ **E LA `dispersione` SODDISFA `W1` AL BIT, che e' la cosa che non mi aspettavo:** sul
fondo del `v3` *(modulo uniforme)* la dispersione vale ### **`2.47e-31`**, e
`1/(1 + 2.47e-31)` ### **E' ESATTAMENTE `1.0` in `float64`** — misurato su tutti i `120`
nodi. ### ⚠ **Il `contrasto` NO:** da' `0.99999999999999933`, cioe' ### **`7e-16` sotto
`1`** — e quello si propagherebbe nella frazione.

> ## ⛔ **NON SCELGO IO fra le tre:** la scelta sta in `[[DOMANDA-LAMBDA-GRANDEZZA]]`, e
> ## questo modulo le tiene ### **tutte e tre, accendibili separatamente.**

### ✅ **E TUTTE E TRE SONO PARI SOTTO `C` E INVARIANTI DI GAUGE PER COSTRUZIONE**, perche'
leggono ### **solo `|phi|²`** — e `phi` e' **neutra** *(`W5`, `W6`)*.

### ⚠ **NESSUN `clip`, NESSUNA costante tarata in questo file.** L'unico `np.where` protegge
una divisione per uno **zero esatto**, e la' il valore e' ### **quello che la funzione
PRENDE**, non un pavimento: `Lambda_k = 0` vuol dire ### **niente vuoto**, e un nodo senza
vuoto non ha ne' dispersione ne' contrasto ⟹ `cs = 1` *(il `v3`)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)

# ### ⛔ **I NOMI ENTRANO NELLE USCITE:** una lettura che non dice ### **quale forma**
# ### non si puo' confrontare con un'altra.
FORME = ("dispersione", "contrasto", "densita")


def _per_nodo(d, sc):
    """`(somma, media)` di `d` sulle estremita' di ogni nodo."""
    s = np.zeros(sc["n"], dtype=float)
    np.add.at(s, sc["nodo"], d)
    return s, s / sc["grado"]


def dispersione(phi, sc):
    """### `D_k` = **varianza NON distorta / media²** di `|phi|²` sulle estremita'.

    ### ⭐ **L'ATTESA DI `D` NON DIPENDE DAL GRADO**, perche' il divisore e' `d - 1` e non
    `d`: e' la ragione per cui questa forma esiste. ### ⚠ **La sua FLUTTUAZIONE si'** —
    meno estremita' vuol dire piu' rumore — e questo ### **si misura e si dichiara.**
    """
    d = np.abs(phi) ** 2
    _s, md = _per_nodo(d, sc)
    r = d - md[sc["nodo"]]
    s2 = np.zeros(sc["n"], dtype=float)
    np.add.at(s2, sc["nodo"], r * r)
    g = sc["grado"].astype(float)
    # ### ⚠ **un nodo di grado `1` non ha varianza**, e la- `D = 0` e- il valore che la
    # ### funzione PRENDE: una sola estremita- non puo' essere disuniforme.
    var = np.where(g > 1.0, s2 / np.where(g > 1.0, g - 1.0, 1.0), 0.0)
    return np.where(md > 0.0, var / np.where(md > 0.0, md * md, 1.0), 0.0)


def contrasto(phi, sc):
    """### `1 - min/max` di `|phi|²` sulle estremita': ### **l'artefatto degli ESTREMI.**"""
    d = np.abs(phi) ** 2
    mn = np.full(sc["n"], np.inf, dtype=float)
    mx = np.zeros(sc["n"], dtype=float)
    np.minimum.at(mn, sc["nodo"], d)
    np.maximum.at(mx, sc["nodo"], d)
    buoni = mx > 0.0
    out = np.zeros(sc["n"], dtype=float)
    out[buoni] = 1.0 - mn[buoni] / mx[buoni]
    return out


def densita(phi, sc, lam0=1.0):
    """### **IL CONTROLLO CHE DICHIARA IL SUO DIFETTO:** `Lambda_k / (grado_k * lam0) - 1`.

    ### ⛔ **HA UNA SCALA** *(`lam0`)*, quindi ### **NON e' relazionale**, e sul fondo del
    `v3` da' ### **`0` per costruzione** perche' la' `Lambda_k = grado_k * lam0`. ### **Serve
    a misurare quanto le altre due siano diverse da <<il grado>>**, non a essere usata.
    """
    d = np.abs(phi) ** 2
    s, _md = _per_nodo(d, sc)
    g = sc["grado"].astype(float)
    return np.abs(s / (g * lam0) - 1.0)


def cs_nodo(phi, sc, forma="dispersione", lam0=1.0):
    """### `cs_k` in `(0, 1]`, dalla forma scelta: ### **`cs = 1/(1 + grandezza)`.**

    ### ⭐ **LA RIDUZIONE A `1` NON E' UN CASO:** tutte e tre le grandezze valgono
    ### **`0` su un vuoto UNIFORME**, e `1/(1+0) = 1` ### **esatto** — cioe' il `v3`.
    ### ⚠ **Ma solo la `dispersione` arriva a `1.0` AL BIT sul fondo del `v3`**
    *(`2.47e-31` contro `7e-16` del `contrasto`)*, ed e' misurato.
    """
    assert forma in FORME, "### forma `%r` sconosciuta" % (forma,)
    if forma == "dispersione":
        q = dispersione(phi, sc)
    elif forma == "contrasto":
        q = contrasto(phi, sc)
    else:
        q = densita(phi, sc, lam0)
    return 1.0 / (1.0 + q)


def cs_imposto(sc, zone=None, valore=1.0):
    """### **IL `cs` IMPOSTO, che e' il CONTROLLO di `L0`:** `valore` dentro `zone`, `1` fuori.

    ### ⛔ **E SERVE A `W1`:** il vincolo dice *«con `cs` identicamente `1` ogni pezzo e'
    esattamente quello di `v3`»*, e per provarlo ### **`cs` dev'essere `1.0` IMPOSTO**, non
    derivato — perche' un `cs` derivato da un vuoto reale puo' valere `1 - 1e-16`.
    ### ⚠ **E la differenza fra i due casi SI MISURA**, invece di tacerla.
    """
    out = np.ones(sc["n"], dtype=float)
    if zone:
        out[list(zone)] = float(valore)
    return out


def cs_casuale(sc, seme=11):
    """### **IL CONTROLLO DI `A6`:** un `cs` CASUALE, per mostrare che l'invarianza locale
    ### **non viene da QUALUNQUE campo di ritmi.** ### **Senza questo, un verde di `L0`
    sarebbe un FALSO-UNO.**"""
    return np.random.default_rng(seme + 4004).random(sc["n"])


if __name__ == "__main__":
    import scena as SC
    import vuoto3 as V3
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    SC._niente_simulatore()
    sc = SC.irregolare()
    g = sc["grado"].astype(float)
    phi = V3.vuoto_fondo(sc, V3.LAMBDA0, 11)
    print("  SUL FONDO DEL v3 (modulo uniforme): la riduzione a `cs = 1`")
    print("  %-14s %-14s %-22s %s" % ("la forma", "grandezza max", "cs min", "tutti == 1.0?"))
    for f in FORME:
        c = cs_nodo(phi, sc, f)
        q = {"dispersione": dispersione, "contrasto": contrasto,
             "densita": densita}[f](phi, sc)
        print("  %-14s %-14.3g %-22.17g %s"
              % (f, float(np.max(q)), float(np.min(c)), bool(np.all(c == 1.0))))
    print()
    print("  SU UN VUOTO NON UNIFORME: il `cs`, e la CORRELAZIONE COL GRADO")
    print("  %-14s %-8s %-8s %-8s %s" % ("la forma", "min", "max", "media", "corr. grado"))
    for f in FORME:
        righe = []
        for seme in (3, 17, 101):
            rng = np.random.default_rng(seme)
            p = rng.normal(size=2 * sc["m"]) + 1j * rng.normal(size=2 * sc["m"])
            c = cs_nodo(p, sc, f)
            righe.append((c.min(), c.max(), c.mean(), float(np.corrcoef(c, g)[0, 1])))
        m = np.mean(np.array(righe), axis=0)
        print("  %-14s %-8.4f %-8.4f %-8.4f %+.4f   (tre semi: %s)"
              % (f, m[0], m[1], m[2], m[3],
                 ", ".join("%+.3f" % r[3] for r in righe)))
