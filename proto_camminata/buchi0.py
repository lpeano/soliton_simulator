# -*- coding: utf-8 -*-
r"""`M0` — **I BUCHI SU TUTTO IL CERCHIO**, e le spigole di `±1` escluse e riportate a parte.

> ## ⛔ **UN GRUMO LEGATO E STAZIONARIO PUO' ESISTERE SOLO SE LA SUA QUASI-ENERGIA CADE
> ## FUORI DALLO SPETTRO CONTINUO** della camminata lineare: altrimenti ### **risuona con le
> ## onde libere e si irradia via.** ### **Quindi la prima domanda del legame e': c'e' un
> ## buco?**

### ⛔ **E LA TRAPPOLA STA SCRITTA NEL REPO, nella testa di `_spettro.py`:** la lettura `M`
del `v2` misurava *«il gap MASSIMO ovunque sul cerchio»* e otteneva **`64.9`** a `eps = 0` —
### **dalle BANDE PIATTE di Grover**, cioe' dalle **spigole di `±1`** degli stati
intrappolati sui cicli. ### **Questo modulo cerca i buchi su TUTTO il cerchio, quindi ci
cadrebbe di nuovo.**

| | che cosa si riporta | perche' |
|---|---|---|
| `a` | i buchi ### **con le spigole `±1` ESCLUSE** | e' **il buco nel CONTINUO**, e gli stati a `±1` sono ### **localizzati sui cicli**: non portano via niente |
| `b` | i buchi ### **con TUTTO dentro** | e' il numero che la lettura `M` del `v2` guardava, e ### **sta accanto al primo per far vedere la differenza** |
| `c` | la ### **molteplicita' di `±1`**, a parte | e' una grandezza sua, e `_spettro.py` la misura ### **in due modi** |

### ⭐ **E UN BUCO SI RICONOSCE DALLA TAGLIA, non dalla larghezza:** un buco VERO e'
**`O(1)` in quasi-energia**, quindi ### **CRESCE in unita' di spaziatura media** quando
`dim` cresce; un buco che resta **`O(1)` in spaziature** ### **non e' un buco: e' la
spaziatura.**

### ⚠ **NESSUN `clip`, NESSUNA costante tarata.** Le tolleranze di degenerazione sono quelle
### **gia' dichiarate** in `_spettro.TOLLERANZE`, e la soglia di un buco e'
### **`3 * spaziatura_media`**, cioe' derivata dalla dimensione.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))

import camminata2 as C2                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import scena as SC                                             # noqa: E402
import _spettro as SP                                          # noqa: E402

# ### ⛔ **LA GRIGLIA DI `eps`, DICHIARATA:** e- ### **la stessa del `v3`**, cosi- i numeri
# ### sono confrontabili con quelli gia- misurati.
EPS_GRIGLIA = (0.0, 0.125, 0.25, 0.375, 0.5, 0.75, 1.0)
# ### ⭐ **LA SOGLIA DI UN BUCO: `3` spaziature medie.** Un salto di `1`..`2` spaziature
# ### ### **non e- un buco: e- la spaziatura.**
SOGLIA_BUCO = 3.0
TOL_DEG = SP.TOLLERANZE[1]


def quasi_energie(sc, geo, eps):
    """Le quasi-energie del passo **lineare `v2`**, e gli autovalori."""
    uno = np.ones(sc["n"], dtype=float)
    M = C2.matrice_passo(sc, geo, uno, 1.0, eps)
    lam = np.linalg.eigvals(M)
    return np.angle(lam), lam, M.shape[0]


def _salti(om, dim):
    """I salti fra quasi-energie consecutive **sul CERCHIO**, col punto di mezzo."""
    o = np.sort(np.asarray(om, dtype=float))
    if o.size < 2:
        return np.array([]), np.array([])
    d = np.diff(o)
    centri = 0.5 * (o[:-1] + o[1:])
    # ### il cerchio si chiude: l-ultimo salto passa per `pi`
    ultimo = (o[0] + 2.0 * math.pi) - o[-1]
    d = np.append(d, ultimo)
    c = np.angle(np.exp(1j * (o[-1] + 0.5 * ultimo)))
    centri = np.append(centri, c)
    del dim
    return d, centri


def buchi(om, dim, quanti=5):
    """### I buchi piu' grandi, **in quasi-energia E in DUE metri di spaziatura.**

    ### ⛔ **E I DUE METRI NON SONO UN ABBELLIMENTO: SONO UN TERZO MODO DI CADERE
    NELLA STESSA TRAPPOLA.** A `eps = 0` il ### **`43%`** degli stati sta a `± 1`, e
    allora `2π/dim` ### **non e' il metro giusto per i rimanenti**: con meta' degli
    stati togliati, i salti fra quelli che restano sono ### **grandi per costruzione.**
    ### ⭐ **Il metro che decide e' `2π/stati_usati`**, e l'altro si riporta
    ### **accanto**, perche' e' quello con cui i numeri del `v2` sono confrontabili.
    """
    media = 2.0 * math.pi / dim
    usati = int(np.asarray(om).size)
    media_u = (2.0 * math.pi / usati) if usati > 0 else float("inf")
    d, c = _salti(om, dim)
    if d.size == 0:
        return {"spaziatura_media": media, "spaziatura_media_usati": media_u,
                "stati_usati": usati,
                "lista": [], "piu_grande": 0.0, "piu_grande_in_spaziature": 0.0,
                "piu_grande_in_spaziature_usati": 0.0, "quanti_oltre_soglia": 0}
    ordine = np.argsort(d)[::-1]
    lista = [{"larghezza": float(d[j]),
              "in_spaziature": float(d[j] / media),
              "in_spaziature_usati": float(d[j] / media_u),
              "posizione": float(c[j]),
              "oltre_soglia": bool(d[j] / media_u > SOGLIA_BUCO)}
             for j in ordine[:quanti]]
    return {"spaziatura_media": media, "spaziatura_media_usati": media_u,
            "stati_usati": usati,
            "lista": lista,
            "piu_grande": float(d[ordine[0]]),
            "piu_grande_in_spaziature": float(d[ordine[0]] / media),
            "piu_grande_in_spaziature_usati": float(d[ordine[0]] / media_u),
            # ### ⛔ **LA SOGLIA USA IL METRO DEGLI STATI USATI**, non quello di `dim`
            "quanti_oltre_soglia": int(np.sum(d / media_u > SOGLIA_BUCO))}


def senza_spigole(om, lam, tol=TOL_DEG):
    """### Le quasi-energie **senza** gli autovalori degeneri a `±1`.

    ### ⛔ **E' LA CURA DELLA TRAPPOLA:** gli stati a `±1` sono ### **intrappolati sui
    cicli**, quindi ### **non fanno parte del continuo** — e tenerli dentro fa apparire un
    <<buco>> che e' solo ### **la spigola della banda piatta.**
    """
    tieni = (np.abs(lam - 1.0) >= tol) & (np.abs(lam + 1.0) >= tol)
    return np.asarray(om)[tieni], int(np.sum(~tieni))


def analizza(sc, geo, eps):
    """### Tutto cio' che `M0` legge da uno spettro, per una scena e un `eps`."""
    om, lam, dim = quasi_energie(sc, geo, eps)
    om_s, togliti = senza_spigole(om, lam)
    fuori = {
        "dim": dim, "eps": eps,
        "unitaria": float(np.max(np.abs(lam * np.conj(lam) - 1.0))),
        "piu_uno": SP.conta_autovalori(lam, 1.0, TOL_DEG),
        "meno_uno": SP.conta_autovalori(lam, -1.0, TOL_DEG),
        "spigole_togliate": togliti,
        # ### (a) ### **IL NUMERO CHE RISPONDE ALLA DOMANDA**
        "senza_spigole": buchi(om_s, dim),
        # ### (b) ### **IL NUMERO CHE LA LETTURA `M` DEL `v2` GUARDAVA**, accanto
        "con_tutto": buchi(om, dim),
        # ### i due punti d-incontro, come li misura `_spettro.py`: ### **il limite noto**
        "a_zero": SP.vicino_al_punto(om, dim, 0.0),
        "a_pi": SP.vicino_al_punto(om, dim, math.pi)}
    return fuori


def verdetto(per_taglia):
    """### Il verdetto di `M0`, **dalle soglie del task history e non a occhio.**

    `per_taglia` e' `{nome: {eps: analisi}}` per la **stessa famiglia** di scene, in ordine
    di taglia crescente.

    | | la soglia |
    |---|---|
    | `s1` | un buco esiste se la larghezza e' **`> 3 * spaziatura_media`** |
    | `s2` | regge con la taglia se la larghezza **in quasi-energia** non cala piu' del **`50%`** |
    """
    nomi = list(per_taglia)
    fuori = {"criterio_s1": "larghezza > %g spaziature" % SOGLIA_BUCO,
             "criterio_s2": "la larghezza in quasi-energia non cala oltre il 50%",
             "per_eps": {}}
    tutti_no = True
    for eps in EPS_GRIGLIA:
        k = "%g" % eps
        righe = [per_taglia[n].get(k) for n in nomi]
        if any(r is None for r in righe):
            continue
        larg = [r["senza_spigole"]["piu_grande"] for r in righe]
        spaz = [r["senza_spigole"]["piu_grande_in_spaziature"] for r in righe]
        oltre = [r["senza_spigole"]["quanti_oltre_soglia"] for r in righe]
        regge = (len(larg) < 2) or (larg[-1] >= 0.5 * larg[0])
        c_e = bool(oltre[0] > 0 and oltre[-1] > 0 and regge)
        if c_e:
            tutti_no = False
        fuori["per_eps"][k] = {
            "larghezze": larg, "in_spaziature": spaz, "quanti_oltre_soglia": oltre,
            "regge_con_la_taglia": bool(regge),
            "buco": c_e,
            "rapporto_larghezza": float(larg[-1] / larg[0]) if larg[0] > 0 else 0.0}
    # ### ⛔ **IL VERDETTO E- PER `eps`, E IL MIO <<OR>> ERA UN DIFETTO:** collassando
    # ### gli `eps` con un OR, ### **un solo `eps` degenere decideva per tutta la
    # ### famiglia** -- e a `eps = 0` ### **il `43%` degli stati sta a `± 1`** e non
    # ### c-e- ### **nessuna moneta di spin.** ### ⚠ **Trovato leggendo i numeri:**
    # ### sul cubico il <<buco>> veniva ### **tutto da `eps = 0`** *(rapporto `0.643`)*,
    # ### mentre a `eps = 0.5` e `1` le larghezze calano del ### **`71%` e `69%`** con la
    # ### taglia, cioe- scalano come ### **la spaziatura della griglia di momenti.**
    con = [k for k, v in fuori["per_eps"].items() if v["buco"]]
    senza = [k for k, v in fuori["per_eps"].items() if not v["buco"]]
    fisico = fuori["per_eps"].get("0.5", {}).get("buco")
    fuori["eps_col_buco"] = sorted(con, key=float)
    fuori["eps_senza_buco"] = sorted(senza, key=float)
    fuori["buco_all_eps_della_fisica"] = bool(fisico)
    fuori["eps_degenere"] = "0"
    fuori["nota_eps_zero"] = ("a `eps = 0` non c-e- moneta di spin e metà degli stati "
                              "sta a +-1: un buco la- e- la struttura a BANDE PIATTE di "
                              "Grover, non un gap in cui uno stato legato possa vivere")
    if fisico:
        v = "BUCO PRESENTE E STABILE a `eps = 0.5`"
    elif con == ["0"]:
        v = "NESSUN BUCO ai `eps` della fisica (solo a `eps = 0`, che e- degenere)"
    elif not con:
        v = "NESSUN BUCO"
    else:
        v = "BUCO solo a `eps` = " + ", ".join(sorted(con, key=float))
    fuori["verdetto"] = v
    fuori["taglie"] = nomi
    return fuori


if __name__ == "__main__":
    import _presidio
    _presidio.avvia(__file__)
    SC._niente_simulatore()
    print("=" * 100)
    print("M0 -- I BUCHI SU TUTTO IL CERCHIO, e le spigole di +-1 a parte")
    print("=" * 100)
    for nome, sc in (("irregolare n=120", SC.irregolare(120)),
                     ("regolare n=120", SC.regolare(120))):
        geo = GE.scena_identita(sc)
        print("  --- %s (dim %d, spaziatura media %.4g) ---"
              % (nome, 4 * sc["m"], 2.0 * math.pi / (4 * sc["m"])))
        print("    %-7s %-9s %-9s %-24s %-24s %s"
              % ("eps", "mult +1", "mult -1", "buco SENZA spigole", "buco CON tutto",
                 "oltre soglia"))
        for eps in (0.0, 0.5, 1.0):
            a = analizza(sc, geo, eps)
            print("    %-7.3f %-9d %-9d %-24s %-24s %d"
                  % (eps, a["piu_uno"], a["meno_uno"],
                     "%.4g (%.2f sp_u)" % (
                         a["senza_spigole"]["piu_grande"],
                         a["senza_spigole"]["piu_grande_in_spaziature_usati"]),
                     "%.4g (%.2f sp)" % (a["con_tutto"]["piu_grande"],
                                         a["con_tutto"]["piu_grande_in_spaziature"]),
                     a["senza_spigole"]["quanti_oltre_soglia"]))
    print("=" * 100)
