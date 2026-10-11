# -*- coding: utf-8 -*-
r"""LA CAMMINATA `v4` — **`cs` locale IN TUTTE LE LEGGI**, nelle due candidate `(F)` e `(S)`.

**Un tick di `(F)`** — *pezzi frazionari, sincroni*:

    N(cs dt/2)  ->  [ spostamento(cs_arco) . Grover(cs_k) . moneta_spin(eps cs_k dt) ]
                    [ e il vuoto: spostamento(cs_arco) . Grover(cs_k) ]
                ->  N(cs dt/2)

### ⭐ **E `cs` ENTRA IN OGNI PEZZO CHE EVOLVE, come il mandato chiede:** moneta di spin,
`N`, Grover **dello spinore**, spostamento, Grover **del vuoto**, spostamento del vuoto, e
la scrittura della materia sul vuoto. ### ⛔ **Restano fuori `C` e il gauge** *(simmetrie)*
### **e il CONO** *(un tetto, non una dinamica)*.

**Un tick di `(S)`** — *tick asincroni*: ogni nodo accumula `tau_k += cs_k dt`, e
### **quando `tau_k >= 1` esegue UN TICK INTERO del `v3`.** ### ⛔ **LA REGOLA DEGLI ARCHI,
DICHIARATA:** l'arco si scambia ### **solo se SCATTANO ENTRAMBE le sue estremita'** —
altrimenti l'ampiezza ### **resta dov'e'**.

> ## ⭐ **E QUELLA REGOLA *SI CHIUDE* IN MODO UNITARIO, contro la mia previsione:** un arco
> ## che non scatta applica ### **l'identita'**, che e' unitaria; un nodo che scatta applica
> ## Grover, che e' unitario. ### **Avevo previsto che non si chiudesse, e il numero mi ha
> ## smentito.**
>
> ## ⛔ **MA IL PREZZO C'E', ED E' L'ALTRO RAMO DELLA MIA PREVISIONE: `(S)` HA BISOGNO DI
> ## UNA MEMORIA.** Per invertire il passo serve sapere ### **CHI HA SCATTATO**, e dal solo
> ## `tau` DOPO non si puo' dedurre *(`tau_dopo < cs dt` e' compatibile sia con <<ha
> ## scattato>> sia con <<`tau_prima` era quasi zero>>)*. ### **Quindi `(S)` porta un bit
> ## per nodo nello STATO**, e ### **uno stato nuovo e' una legge in piu'** *(`9-ter`)*.

### ⚠ **NESSUN `clip`, NESSUNA costante tarata.** Il confronto `tau >= 1` **non e' un clip**:
e' ### **la definizione di <<un'unita' di tempo proprio>>**, cioe' la legge di `(S)`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import camminata3 as C3                                        # noqa: E402
import cslocale4 as CS4                                        # noqa: E402
import frazione4 as F4                                         # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import vuoto4 as V4                                            # noqa: E402

CANDIDATE = ("F", "S")
MAX_SOTTO = 64
SOTTO_USATI = {}


class NonConverge(Exception):
    """### **FERMO**, come `W4` chiede: non si prosegue con un passo che non converge."""


# =====================================================================================
#   IL CAMPO `cs`:  IMPOSTO  oppure  DERIVATO DAL VUOTO
# -------------------------------------------------------------------------------------
def campo_cs(phi, sc, sorgente, forma="dispersione"):
    """### `cs_k` dal vuoto, ### **oppure IMPOSTO.**

    ### ⛔ **L'IMPOSTO E' IL CONTROLLO DI `L0`, e serve a `W1`:** il vincolo dice *«con `cs`
    identicamente `1` ogni pezzo e' esattamente quello di `v3`»*, e per provarlo `cs`
    dev'essere ### **`1.0` IMPOSTO** — un `cs` derivato da un vuoto reale puo' valere
    `1 - 1e-16`. ### ⚠ **E la differenza fra i due casi SI MISURA.**
    """
    if sorgente is None:
        return np.ones(sc["n"], dtype=float)
    if isinstance(sorgente, np.ndarray):
        return sorgente
    assert sorgente == "vuoto", "### sorgente `%r` sconosciuta" % (sorgente,)
    return CS4.cs_nodo(phi, sc, forma)


# =====================================================================================
#   (F)  --  I PEZZI FRAZIONARI, SINCRONI
# =====================================================================================
def _lineare4(psi, phi, sc, geo, cs_k, dt, eps, famiglia, forma_arco,
              candidata_vuoto, forza):
    """Il pezzo lineare del `v4`: ### **ogni pezzo con la sua frazione.**"""
    cs_e = cs_k[sc["nodo"]]
    cs_a = F4.cs_da_arco(cs_k, sc, forma_arco)
    # ### ① la moneta di spin: una ROTAZIONE, quindi basta `dtau = cs dt`
    x = C2.moneta_spin(psi, geo, eps, cs_k * dt, sc)
    # ### ② Grover dello spinore, FRAZIONARIO
    x = F4.frazione(lambda v: CM.moneta_grover(v, sc), x, cs_e, famiglia)
    # ### ③ lo spostamento con trasporto, FRAZIONARIO, col `cs` dell-ARCO
    x = F4.frazione(lambda v: C2.spostamento_trasporto(v, geo, sc), x, cs_a, famiglia)
    # ### ④ il vuoto: Grover e spostamento, FRAZIONARI -- e la scrittura della materia
    if candidata_vuoto is None:
        f = F4.frazione(lambda v: V3.grover_scalare(v, sc), phi, cs_e, famiglia)
    elif candidata_vuoto == "scatter":
        f = V4.scatter(phi, psi, sc, famiglia, forza)
        f = F4.frazione(lambda v: V3.grover_scalare(v, sc), f, cs_e, famiglia)
    else:
        f = F4.frazione(lambda v: V3.grover_scalare(v, sc), phi, cs_e, famiglia)
        f = V4.trasmissione(f, psi, sc, famiglia, forma_arco, forza)
    f = F4.frazione(lambda v: V3.spostamento_scalare(v), f, cs_a, famiglia)
    return x, f


def _lineare4_inverso(psi, phi, sc, geo, cs_k, dt, eps, famiglia, forma_arco,
                      candidata_vuoto, forza):
    """### L'inverso del pezzo lineare: ### **i pezzi al contrario, e ogni frazione con `-cs`.**"""
    cs_e = cs_k[sc["nodo"]]
    cs_a = F4.cs_da_arco(cs_k, sc, forma_arco)
    f = F4.frazione_inversa(lambda v: V3.spostamento_scalare(v), phi, cs_a, famiglia)
    if candidata_vuoto is None:
        f = F4.frazione_inversa(lambda v: V3.grover_scalare(v, sc), f, cs_e, famiglia)
    elif candidata_vuoto == "scatter":
        f = F4.frazione_inversa(lambda v: V3.grover_scalare(v, sc), f, cs_e, famiglia)
        # ### ⚠ **E QUI L-INVERSO NON E- ESATTO SE `scatter` LEGGE `psi`:** la quota
        # ### dipende dallo stato, e ### **si dichiara** -- il braccio lo misura.
        s = V4.quota_vuoto(psi, f, sc)
        if forza != 1.0:
            s = 1.0 - forza * (1.0 - s)
        f = F4.frazione_inversa(lambda v: V3.grover_scalare(v, sc), f, s[sc["nodo"]],
                                famiglia)
        f = F4.frazione(lambda v: V3.grover_scalare(v, sc), f, cs_e, famiglia)
    else:
        s = V4.quota_vuoto(psi, f, sc)
        if forza != 1.0:
            s = 1.0 - forza * (1.0 - s)
        f = F4.frazione_inversa(lambda v: V3.spostamento_scalare(v), f,
                                F4.cs_da_arco(s, sc, forma_arco), famiglia)
        f = F4.frazione_inversa(lambda v: V3.grover_scalare(v, sc), f, cs_e, famiglia)
    x = F4.frazione_inversa(lambda v: C2.spostamento_trasporto(v, geo, sc), psi, cs_a,
                            famiglia)
    x = F4.frazione_inversa(lambda v: CM.moneta_grover(v, sc), x, cs_e, famiglia)
    x = C2.moneta_spin(x, geo, -eps, cs_k * dt, sc)
    return x, f


def passo4_F(st, sc, geo, dt, eps, sorgente=None, flusso=None, famiglia="B",
             forma_arco="min", forma_cs="dispersione", candidata_vuoto=None, forza=1.0,
             inverso=False):
    """### UN TICK DI `(F)`, ### **composizione SIMMETRICA come il `v3`.**

    ### ⛔ **`sorgente = None` e `flusso = None` e `candidata_vuoto = None` ⟹ il `v3` AL
    BIT:** `cs = 1` ovunque cortocircuita ### **ogni** frazione sul pezzo del `v3`, e la
    moneta di spin prende `dtau = dt` come nel `v3`.
    """
    psi, phi = st["psi"], st["phi"]
    cs_k = campo_cs(phi, sc, sorgente, forma_cs)
    segno = -1.0 if inverso else 1.0
    mezzo = 0.5 * segno * cs_k * dt
    if flusso is not None:
        psi, phi = flusso(psi, phi, sc, geo, mezzo)
    if inverso:
        psi, phi = _lineare4_inverso(psi, phi, sc, geo, cs_k, dt, eps, famiglia,
                                     forma_arco, candidata_vuoto, forza)
    else:
        psi, phi = _lineare4(psi, phi, sc, geo, cs_k, dt, eps, famiglia, forma_arco,
                             candidata_vuoto, forza)
    if flusso is not None:
        psi, phi = flusso(psi, phi, sc, geo, mezzo)
    return {"psi": psi, "phi": phi}


# =====================================================================================
#   (S)  --  I TICK ASINCRONI, e la REGOLA DEGLI ARCHI dichiarata
# =====================================================================================
def stato_S(st, sc):
    """### Lo stato di `(S)`: `psi`, `phi`, ### **`tau` e il bit <<ha scattato>>.**

    ### ⛔ **IL BIT E' IL PREZZO DI `(S)`, e non e' un dettaglio di implementazione:** serve
    ### **per invertire**, perche' dal solo `tau` DOPO non si deduce chi ha scattato.
    ### **Uno stato nuovo e' una legge in piu'** *(`9-ter`)*, e va contato.
    """
    return {"psi": st["psi"], "phi": st["phi"],
            "tau": np.zeros(sc["n"], dtype=float),
            "scattato": np.zeros(sc["n"], dtype=bool)}


def passo4_S(st, sc, geo, dt, eps, sorgente=None, flusso=None,
             forma_cs="dispersione", inverso=False):
    """### UN TICK DI `(S)`: chi ha accumulato ### **un'unita' di tempo proprio** scatta.

    ### ⛔ **LA REGOLA DEGLI ARCHI, DICHIARATA:** l'arco si scambia ### **solo se scattano
    ENTRAMBE** le sue estremita'. ### ✅ **E si chiude unitaria**, perche' un arco che non
    scatta applica ### **l'identita'.**

    ### ⚠ **E IL CONO E' RISPETTATO PER COSTRUZIONE** *(`W7`)*: in un tick ogni ampiezza
    percorre ### **al piu' un arco**, e ### **puo' percorrerne ZERO** — che e' il <<moto a
    scatti>> che il mandato nomina.
    """
    psi, phi = st["psi"], st["phi"]
    tau = st["tau"].copy()
    cs_k = campo_cs(phi, sc, sorgente, forma_cs)
    if not inverso:
        tau = tau + cs_k * dt
        scatta = tau >= 1.0
        tau = np.where(scatta, tau - 1.0, tau)
    else:
        # ### ⛔ **L-INVERSO LEGGE IL BIT, e per questo il bit c-e-.**
        scatta = st["scattato"]
        tau = np.where(scatta, tau + 1.0, tau) - cs_k * dt
    e_scatta = scatta[sc["nodo"]]
    a_scatta = np.all(scatta[sc["nodo"]].reshape(-1, 2), axis=1)
    a_scatta = np.repeat(a_scatta, 2)
    segno = -1.0 if inverso else 1.0
    mezzo = 0.5 * segno * dt * scatta.astype(float)

    def solo(vecchio, nuovo, dove):
        """### Sostituisce ### **solo dove `dove`**: chi non scatta ### **resta.**"""
        d = dove.reshape((-1,) + (1,) * (nuovo.ndim - 1))
        return np.where(d, nuovo, vecchio)

    if flusso is not None:
        p2, f2 = flusso(psi, phi, sc, geo, mezzo)
        psi, phi = solo(psi, p2, e_scatta), solo(phi, f2, e_scatta)
    if not inverso:
        psi = solo(psi, C2.moneta_spin(psi, geo, eps, dt * np.ones(sc["n"]), sc),
                   e_scatta)
        psi = solo(psi, CM.moneta_grover(psi, sc), e_scatta)
        psi = solo(psi, C2.spostamento_trasporto(psi, geo, sc), a_scatta)
        phi = solo(phi, V3.grover_scalare(phi, sc), e_scatta)
        phi = solo(phi, V3.spostamento_scalare(phi), a_scatta)
    else:
        psi = solo(psi, C2.spostamento_trasporto(psi, geo, sc), a_scatta)
        psi = solo(psi, CM.moneta_grover(psi, sc), e_scatta)
        psi = solo(psi, C2.moneta_spin(psi, geo, -eps, dt * np.ones(sc["n"]), sc),
                   e_scatta)
        phi = solo(phi, V3.spostamento_scalare(phi), a_scatta)
        phi = solo(phi, V3.grover_scalare(phi, sc), e_scatta)
    if flusso is not None:
        p2, f2 = flusso(psi, phi, sc, geo, mezzo)
        psi, phi = solo(psi, p2, e_scatta), solo(phi, f2, e_scatta)
    return {"psi": psi, "phi": phi, "tau": tau, "scattato": scatta}


def passo4(st, sc, geo, dt, eps, candidata="F", **kw):
    """### LA PORTA UNICA: `(F)` oppure `(S)`, e ### **il nome entra nelle uscite.**"""
    assert candidata in CANDIDATE, "### candidata `%r` sconosciuta" % (candidata,)
    if candidata == "F":
        return passo4_F(st, sc, geo, dt, eps, **kw)
    kw.pop("famiglia", None)
    kw.pop("forma_arco", None)
    kw.pop("candidata_vuoto", None)
    kw.pop("forza", None)
    return passo4_S(st, sc, geo, dt, eps, **kw)


if __name__ == "__main__":
    import geometria as GE
    import saturazione3 as S3
    import scena as SC
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    SC._niente_simulatore()
    sc = SC.irregolare()
    geo = GE.scena_curva(sc, 11)
    uno = np.ones(sc["n"], dtype=float)
    st = C3.stato3(sc, 11)
    K = 20
    # ### (R) LA REGRESSIONE: `cs = 1` imposto, tutto spento ⟹ il `v3` AL BIT
    a = dict(st)
    b = dict(st)
    for _ in range(K):
        a = C3.passo3(a, sc, geo, uno, 1.0, 0.5, None)
        b = passo4_F(b, sc, geo, 1.0, 0.5, None, None)
    print("  (R) `cs = 1` imposto, tutto spento: max|psi4 - psi3| = %.3g   "
          "max|phi4 - phi3| = %.3g"
          % (float(np.max(np.abs(b["psi"] - a["psi"]))),
             float(np.max(np.abs(b["phi"] - a["phi"])))))
    # ### e con `N` acceso
    a, b = dict(st), dict(st)
    for _ in range(K):
        a = C3.passo3(a, sc, geo, uno, 1.0, 0.5, S3.flusso)
        b = passo4_F(b, sc, geo, 1.0, 0.5, None, S3.flusso)
    print("  (R) con `N` acceso:                 max|psi4 - psi3| = %.3g   "
          "max|phi4 - phi3| = %.3g"
          % (float(np.max(np.abs(b["psi"] - a["psi"]))),
             float(np.max(np.abs(b["phi"] - a["phi"])))))
    # ### le NORME e l-INVERSO di `(F)` con un `cs` imposto NON uniforme
    cs = 0.3 + 0.7 * np.random.default_rng(5).random(sc["n"])
    c = dict(st)
    for _ in range(K):
        c = passo4_F(c, sc, geo, 1.0, 0.5, cs)
    print("  (F) `cs` imposto non uniforme: norma psi %.3g   norma phi %.3g"
          % (abs(CM.norma(c["psi"]) - CM.norma(st["psi"])),
             abs(V3.norma_vuoto(c["phi"]) - V3.norma_vuoto(st["phi"]))))
    d = dict(c)
    for _ in range(K):
        d = passo4_F(d, sc, geo, 1.0, 0.5, cs, inverso=True)
    print("  (F) l-INVERSO su %d+%d passi: max|psi - psi0| = %.3g   max|phi - phi0| = %.3g"
          % (K, K, float(np.max(np.abs(d["psi"] - st["psi"]))),
             float(np.max(np.abs(d["phi"] - st["phi"])))))
    # ### `(S)`: le norme, e l-INVERSO col BIT
    s0 = stato_S(st, sc)
    s = dict(s0)
    for _ in range(K):
        s = passo4_S(s, sc, geo, 1.0, 0.5, cs)
    print("  (S) `cs` imposto non uniforme: norma psi %.3g   norma phi %.3g   "
          "nodi scattati nell-ultimo tick: %d"
          % (abs(CM.norma(s["psi"]) - CM.norma(st["psi"])),
             abs(V3.norma_vuoto(s["phi"]) - V3.norma_vuoto(st["phi"])),
             int(np.sum(s["scattato"]))))
    print("  (S) e il `tau` accumulato: min %.4f max %.4f" % (s["tau"].min(),
                                                              s["tau"].max()))
