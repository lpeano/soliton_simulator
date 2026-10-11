# -*- coding: utf-8 -*-
r"""COME LA MATERIA SCRIVE SUL VUOTO — **due candidate, e NON scelgo io** *(punto `A1`)*.

> ## ⛔ **IL PUNTO DI PARTENZA, VERIFICATO E NON ASSUNTO:** `Lambda_k` e' conservata da
> ## Grover ### **PER TEOREMA** — Grover e' a blocchi **per nodo**, quindi unitario
> ## ### **dentro** il nodo — e misurato: `max|dLambda|` = **`7.11e-15`** su un vuoto
> ## **non** uniforme. ### ⭐ **La densita' del vuoto si sposta fra i nodi SOLO nello
> ## spostamento** *(`56.5` sullo stesso vuoto)*.

> ## ⚠ **E IL MIO PRIMO GIRO ERA UN FALSO-ZERO:** col fondo del `v3`, che ha ### **modulo
> ## uniforme**, lo spostamento dava `8.88e-16` — perche' ### **scambia estremita' di
> ## modulo UGUALE**, e `Lambda` ### **non PUO' cambiare, qualunque sia la legge.**
> ## ### **Avrei concluso il contrario del vero.**

| | la candidata | che cosa cambia | la grandezza |
|---|---|---|---|
| `scatter` | la **moneta del vuoto** va da Grover verso l'### **IDENTITA'** *(riflessione totale)* in funzione della materia | ### **la distribuzione del vuoto FRA le estremita' del nodo** | `s_k = Lambda_k / (Lambda_k + rho_k)` — ### **la QUOTA del vuoto** sulla densita' totale del nodo |
| `trasmissione` | lo **spostamento del vuoto** diventa **parziale** | ### **il FLUSSO del vuoto fra i nodi** — cioe' l'unico pezzo che muove `Lambda` | `t_a` dalle **due estremita' dell'arco**, con la forma simmetrica dichiarata |

### ⭐ **ENTRAMBE USANO LA *STESSA* FAMIGLIA FRAZIONARIA DI `frazione4.py`**, quindi
### **non aggiungono una legge nuova sulla forma**: aggiungono ### **una grandezza** *(la
quota del vuoto)* e nient'altro. ### **E' `9-ter`.**

### ⛔ **`scatter` DA SOLO NON PUO' MUOVERE `Lambda`, ed e' un TEOREMA e non un difetto:**
Grover e l'identita' sono ### **entrambe a blocchi per nodo**, quindi ### **ogni** loro
interpolazione conserva `Lambda_k`. ### ⭐ **Il meccanismo e' in DUE tempi:** `scatter` cambia
**dove** sta il vuoto dentro il nodo, e lo ### **spostamento** trasforma quello in un
### **flusso netto**. ### **Quindi `scatter` si misura SUL TICK, non sul pezzo.**

### ✅ **E LA GRANDEZZA E' PARI SOTTO `C` E INVARIANTE DI GAUGE:** `rho` e `Lambda` lo sono
entrambe *(`W5`, `W6`)*, quindi ### **materia e antimateria scrivono la STESSA cosa.**

### ⛔ **E LA TERZA CANDIDATA DEL MANDATO E' ESCLUSA DA UN VINCOLO, non da un gusto:** lo
### **scambio di NORMA fra `psi` e `phi`** romperebbe il gauge *(`W6`)*, perche' `psi` si
trasforma con `e^{i f_k} g_k` e `phi` ### **no** — mescolarle vorrebbe dire ### **sommare due
cose che si trasformano diversamente**, ed e' il motivo per cui `vuoto3.py` lo vieta
*(«si scambiano ENERGIA, non ampiezza»)*. ### **La dichiaro e NON la implemento.**

### ⚠ **NESSUN `clip`, NESSUNA costante tarata.** I `np.where` proteggono divisioni per uno
**zero esatto**, e la' il valore e' ### **quello che la funzione PRENDE.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402
import frazione4 as F4                                         # noqa: E402
import vuoto3 as V3                                            # noqa: E402

# ### ⛔ **I NOMI ENTRANO NELLE USCITE.** `None` vuol dire ### **SPENTO**, e a spento
# ### questo modulo e' ### **l'identita' AL BIT** — un braccio lo verifica.
CANDIDATE = ("scatter", "trasmissione")


def quota_vuoto(psi, phi, sc):
    """### `s_k = Lambda_k / (Lambda_k + rho_k)`: ### **la QUOTA del vuoto nel nodo.**

    ### ⭐ **E' un RAPPORTO, quindi non porta nessuna scala** *(`W2`)*, ed e' ### **`1` dove
    non c'e' materia** — cioe' il `v3`. ### ⚠ **E dove non c'e' NE' vuoto NE' materia vale
    `1`**, che e' il valore che la funzione prende nel limite, non un pavimento.
    """
    lam = V3.lambda_nodo(phi, sc)
    rho = CM.rho_nodo(psi, sc)
    tot = lam + rho
    return np.where(tot > 0.0, lam / np.where(tot > 0.0, tot, 1.0), 1.0)


def scatter(phi, psi, sc, famiglia="B", forza=1.0):
    """### `scatter`: la moneta del vuoto da Grover verso l'### **IDENTITA'**.

    `s_k = 1` ⟹ Grover pieno *(il `v3`)*; `s_k = 0` ⟹ ### **identita'**, cioe'
    ### **riflessione totale** — il vuoto torna indietro per l'arco da cui e' venuto.

    ### ⚠ **`forza` NON e' una costante tarata: e' L'INTERRUTTORE** *(`forza = 0` ⟹ `v3` al
    bit)*, e le letture la tengono a `1`. ### **Serve al braccio di regressione**, che e'
    `W1`.
    """
    s = quota_vuoto(psi, phi, sc)
    if forza != 1.0:
        # ### `forza = 0` riporta `s` a `1`, cioe- il Grover pieno: ### **e- lo spegnimento**
        s = 1.0 - forza * (1.0 - s)
    X = lambda v: V3.grover_scalare(v, sc)                     # noqa: E731
    return F4.frazione(X, phi, s[sc["nodo"]], famiglia)


def trasmissione(phi, psi, sc, famiglia="B", forma="min", forza=1.0):
    """### `trasmissione`: lo spostamento del vuoto diventa ### **PARZIALE.**

    `t_a = 1` ⟹ spostamento pieno *(il `v3`)*; `t_a = 0` ⟹ ### **niente trasporto.**
    La frazione dell'arco viene dalle sue ### **due estremita'**, con la forma simmetrica
    dichiarata di `frazione4.cs_da_arco`.
    """
    s = quota_vuoto(psi, phi, sc)
    if forza != 1.0:
        s = 1.0 - forza * (1.0 - s)
    t = F4.cs_da_arco(s, sc, forma)
    X = lambda v: V3.spostamento_scalare(v)                    # noqa: E731
    return F4.frazione(X, phi, t, famiglia)


def passo_vuoto(phi, psi, sc, candidata=None, famiglia="B", forma="min", forza=1.0):
    """### UN TICK DEL VUOTO, con la candidata scelta ### **oppure SPENTA.**

    ### ⛔ **`candidata = None` e' il `v3` AL BIT:** Grover pieno e spostamento pieno, con
    ### **lo stesso codice** di `vuoto3._lineare` — non una seconda implementazione.
    """
    if candidata is None:
        return V3.spostamento_scalare(V3.grover_scalare(phi, sc))
    assert candidata in CANDIDATE, "### candidata `%r` sconosciuta" % (candidata,)
    if candidata == "scatter":
        return V3.spostamento_scalare(scatter(phi, psi, sc, famiglia, forza))
    return trasmissione(V3.grover_scalare(phi, sc), psi, sc, famiglia, forma, forza)


if __name__ == "__main__":
    import geometria as GE
    import scena as SC
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    SC._niente_simulatore()
    sc = SC.irregolare()
    geo = GE.scena_identita(sc)
    del geo
    # ### un grumo su un nodo, e il vuoto del `v3`
    import _letture3 as L3
    st, _z, _d = L3.grumo(sc, GE.scena_identita(sc), 0, 1, 8.0, seme=11)
    phi = V3.vuoto_fondo(sc, V3.LAMBDA0, 11)
    psi = st["psi"]
    print("  la QUOTA del vuoto: min %.6f  max %.6f  (e- `1` dove non c-e- materia: %d nodi)"
          % (float(quota_vuoto(psi, phi, sc).min()),
             float(quota_vuoto(psi, phi, sc).max()),
             int(np.sum(quota_vuoto(psi, phi, sc) == 1.0))))
    print()
    # ### ⛔ **IL NUMERO CHE CONTA E- LA DIFFERENZA DAL `v3`, non `|dLambda|` di
    # ### ognuna:** al primo giro stampavo `max|Lambda(dopo) - Lambda(prima)|` e veniva
    # ### ### **`3.63` per TUTTE**, spenta compresa -- perche- il `max` cadeva su un nodo
    # ### ### **senza materia**, dove le candidate non fanno niente. ### **Un riepilogo
    # ### sbagliato nascondeva la risposta.**
    l0 = V3.lambda_nodo(phi, sc)
    n0 = V3.norma_vuoto(phi)
    rif = passo_vuoto(phi, psi, sc, None)
    lrif = V3.lambda_nodo(rif, sc)
    print("  il `v3`: max|Lambda(dopo) - Lambda(prima)| = %.3g, norma %.12g"
          % (float(np.max(np.abs(lrif - l0))), V3.norma_vuoto(rif)))
    print()
    print("  %-16s %-8s %-18s %-18s %s"
          % ("la candidata", "forza", "max|phi - phi_v3|", "max|Lam - Lam_v3|",
             "norma del vuoto"))
    for cand in CANDIDATE:
        for forza in (0.0, 1.0):
            f = passo_vuoto(phi, psi, sc, cand, forza=forza)
            print("  %-16s %-8.1f %-18.3g %-18.3g %.12g"
                  % (cand, forza, float(np.max(np.abs(f - rif))),
                     float(np.max(np.abs(V3.lambda_nodo(f, sc) - lrif))),
                     V3.norma_vuoto(f)))
    print()
    # ### ⛔ **E IL PEZZO SOLO, per mostrare il TEOREMA:** `scatter` da solo NON muove
    # ### `Lambda`, perche- e- a blocchi per nodo.
    sc_solo = scatter(phi, psi, sc)
    print("  il solo `scatter`, SENZA spostamento: max|dLambda| = %.3g   "
          "### **e- il TEOREMA: a blocchi per nodo**"
          % float(np.max(np.abs(V3.lambda_nodo(sc_solo, sc) - l0))))
    print("  e la norma: %.12g -> %.12g" % (n0, V3.norma_vuoto(sc_solo)))
