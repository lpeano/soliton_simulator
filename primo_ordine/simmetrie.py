# -*- coding: utf-8 -*-
"""PUNTO `3` DELLA TERZA PARTE — **SIMMETRIE (simboliche) E CONSERVAZIONI (numeriche).**

> ### ⛔ **Il mandato, alla lettera:** *«ogni termine dichiara le simmetrie *(almeno la
> fase globale `U(1)`)* e **ciò che conserva**; il generatore verifica
> **simbolicamente** le simmetrie, il collaudo **numericamente** le conservazioni. Un
> termine che rompe una simmetria dichiarata → **rifiutato**»*.

### ⭐ **E IL PUNTO DIFFICILE NON E' LA SIMMETRIA: E' LA SOGLIA DELLA CONSERVAZIONE.**
Una conservazione numerica non è mai esatta, quindi serve un numero — e
### ⛔ **un numero scelto per far passare la misura è UNA MANOPOLA** *(`A1`)*.
### ✅ **Quindi le due soglie sono DERIVATE dall'ordine del metodo, e la derivazione è
scritta qui accanto. Nessuna delle due è stata tarata.**

| | che cosa si dichiara | come si verifica |
|---|---|---|
| `simmetrie` | ### **almeno `U1-FASE-GLOBALE`** | ### **SIMBOLICAMENTE**: si sostituisce `psi -> psi e^{i theta}` *(e `psi* -> psi* e^{-i theta}`)* e si pretende che la differenza ### **sia ZERO in sympy** |
| `conserva` | `NORMA`, `ENERGIA`, o ### **nulla** | ### **NUMERICAMENTE**, su una corsa vera, ### **contro una soglia DERIVATA** |

### **LE DUE SOGLIE, e la loro derivazione**

### 📌 **`NORMA`: la soglia è `passi * eps`.** La norma è ### **un invariante quadratico**,
e il punto medio implicito ### **conserva esattamente gli invarianti quadratici in
aritmetica esatta** — quindi l'unico errore è ### **l'arrotondamento**, e in `N` passi non
può superare ### **`N` volte un epsilon relativo.** ### ⭐ **Con `200` passi:
`200 * 2.22e-16 = 4.44e-14`.** ### **Non è un numero scelto: è il numero di passi per la
precisione della macchina.**

### 📌 **`ENERGIA`: la soglia è `dt^2`.** Il punto medio implicito è ### **simmetrico e
del secondo ordine**, e un metodo simmetrico ### **non ha deriva secolare dell'energia**:
l'errore resta ### **limitato e di ordine `dt^2`.** ### ⭐ **Con `dt = 0.01`:
`1.0e-4`.** ### **Anche questo è l'ordine del metodo, non una taratura.**

### ⚠ **E LA DIFFERENZA FRA LE DUE SOGLIE NON E' UN DETTAGLIO: è di ELEVEN ordini di
grandezza**, e dice una cosa vera — ### **la norma è conservata DALLA STRUTTURA del
metodo, l'energia solo APPROSSIMATA.** ### ⛔ **Dichiararle con la stessa soglia
nasconderebbe esattamente questo.**

### ⛔ **E CIO' CHE QUESTO MODULO NON DICE, perché le leggi di oggi sono di PROVA:** una
simmetria verificata su `PROVA-HOPPING` ### **non dice niente sulla fisica** — dice che
### **la macchina funziona.** ### **Il referto lo scriverà così.**
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

PRESIDIO = "P-SIM"

NL = chr(10)

# ### ⛔ **IL VOCABOLARIO E- CHIUSO**, come tutti in questo repo: una simmetria nuova
# ### ### **si dichiara qui con il suo controllo**, e non si scrive a parole in una
# ### scheda. ### **Una simmetria senza un controllo e- una frase.**
SIMMETRIE = ("U1-FASE-GLOBALE", "SCAMBIO-DEI-CAPI")

CONSERVAZIONI = ("NORMA", "ENERGIA")

# ### ⚠ **LE SOGLIE SONO DERIVATE, e la derivazione sta nel docstring.** Qui stanno
# ### ### **le formule**, non i numeri: un numero scritto qui ### **sarebbe una manopola**
# ### *(`A1`)*, una formula ### **e- una legge.**
EPS = 2.220446049250313e-16            # ### `numpy.finfo(float).eps`, non un numero mio


def soglia(che, passi, dt):
    """### La soglia di una conservazione, ### **DERIVATA.**

    * `NORMA`   -> `passi * EPS`  *(invariante quadratico: solo arrotondamento)*
    * `ENERGIA` -> `dt**2`        *(metodo simmetrico del secondo ordine)*
    """
    if che == "NORMA":
        return passi * EPS
    if che == "ENERGIA":
        return dt ** 2
    raise AssertionError("### `%s` non e- in `CONSERVAZIONI`: %s"
                         % (che, list(CONSERVAZIONI)))


def _sost_u1(e, sympy):
    """`psi -> psi e^{i theta}`, ### **e il coniugato prende il segno opposto.**"""
    th = sympy.Symbol("_theta_", real=True)
    sost = {}
    for s in e.free_symbols:
        n = s.name
        if not n.startswith("psi"):
            continue
        # ### ⛔ **IL CONIUGATO SI RICONOSCE DAL SUFFISSO `c`**, che e- la convenzione
        # ### che il generatore usa per costruire i simboli -- e ### **se cambiasse, questo
        # ### controllo direbbe INVARIANTE per la ragione sbagliata.**
        sost[s] = s * sympy.exp(-sympy.I * th) if n.endswith("c") \
            else s * sympy.exp(sympy.I * th)
    return e.subs(sost), len(sost)


def _sost_scambio(e, sympy):
    """`_i <-> _j`: ### **i due capi di un arco si scambiano.**"""
    sost = {}
    for s in e.free_symbols:
        n = s.name
        if "_i" in n:
            sost[s] = sympy.Symbol(n.replace("_i", "_j", 1))
        elif "_j" in n:
            sost[s] = sympy.Symbol(n.replace("_j", "_i", 1))
    return e.subs(sost, simultaneous=True), len(sost)


def rompe(legge):
    """### Gli errori delle simmetrie DICHIARATE, o `[]`. ### **Simbolico.**"""
    import sympy
    err = []
    idv = legge.get("id", "<senza id>")
    esp = legge.get("espressione")
    dichiarate = legge.get("simmetrie")
    if legge.get("tipo") not in ("termine_nodo", "termine_arco", "osservatore"):
        return err
    if not isinstance(dichiarate, list) or not dichiarate:
        err.append("`P-SIM` `%s`: NON DICHIARA `simmetrie`. ### Il mandato chiede ALMENO "
                   "la fase globale `U1-FASE-GLOBALE`, e una simmetria non dichiarata "
                   "e- una simmetria CHE NESSUNO VERIFICA" % idv)
        return err
    fuori = [x for x in dichiarate if x not in SIMMETRIE]
    if fuori:
        err.append("`P-SIM` `%s`: simmetrie fuori vocabolario %s. ### Il vocabolario e- "
                   "CHIUSO: una simmetria nuova si dichiara in `SIMMETRIE` CON IL SUO "
                   "CONTROLLO, e una simmetria senza controllo e- UNA FRASE"
                   % (idv, fuori))
        return err
    if "U1-FASE-GLOBALE" not in dichiarate:
        err.append("`P-SIM` `%s`: non dichiara `U1-FASE-GLOBALE`, che il mandato chiede "
                   "come MINIMO" % idv)
    e = sympy.sympify(str(esp))
    for s in dichiarate:
        if s == "U1-FASE-GLOBALE":
            nuova, quanti = _sost_u1(e, sympy)
        else:
            nuova, quanti = _sost_scambio(e, sympy)
        # ### ⛔ **ZERO SOSTITUZIONI: DUE CASI DIVERSI, e il collaudo me l-ha
        # ### insegnato.**
        # ### ✅ **`U1-FASE-GLOBALE` con zero sostituzioni e- INVARIANTE DAVVERO:**
        # ### vuol dire che la legge ### **non contiene `psi`**, quindi
        # ### ### **non coinvolge la fase** -- e- vero, non vacuo.
        # ### ⛔ **`SCAMBIO-DEI-CAPI` con zero sostituzioni e- PRIVO DI SENSO:** la
        # ### legge ### **non ha due capi**, quindi dichiarare quella simmetria
        # ### ### **non dice niente** e sembra verificata. ### **Quello e- il FALSO-UNO.**
        if quanti == 0:
            if s == "U1-FASE-GLOBALE":
                continue
            err.append("`P-SIM` `%s`: dichiara `%s` e la sostituzione NON TOCCA NESSUN "
                       "SIMBOLO -- la legge NON HA DUE CAPI. ### Dichiarare lo scambio "
                       "dei capi su un termine di NODO e- un FALSO-UNO: sembra "
                       "verificato e non ha guardato niente" % (idv, s))
            continue
        d = sympy.simplify(sympy.expand(nuova - e))
        if d != 0:
            err.append("`P-SIM` `%s`: dichiara `%s` e NON LA RISPETTA -- la differenza "
                       "e- `%s`. ### Una simmetria dichiarata e non vera e- PEGGIO di "
                       "una non dichiarata: la prima SEMBRA verificata"
                       % (idv, s, str(d)[:120]))
    return err


def conservazioni_valide(legge):
    """Gli errori del campo `conserva`, o `[]`."""
    err = []
    idv = legge.get("id", "<senza id>")
    if legge.get("tipo") not in ("termine_nodo", "termine_arco", "osservatore"):
        return err
    c = legge.get("conserva")
    if not isinstance(c, list):
        err.append("`P-SIM` `%s`: `conserva` deve essere una LISTA (anche vuota, e "
                   "allora LO DICE). ### <<non dichiarato>> e <<non conserva niente>> "
                   "non sono la stessa cosa" % idv)
        return err
    fuori = [x for x in c if x not in CONSERVAZIONI]
    if fuori:
        err.append("`P-SIM` `%s`: conservazioni fuori vocabolario %s: %s"
                   % (idv, fuori, list(CONSERVAZIONI)))
    return err


def controlla(leggi):
    """Gli errori di simmetria e conservazione di ### **tutte** le leggi, o `[]`."""
    err = []
    for lg in leggi:
        err += rompe(lg)
        err += conservazioni_valide(lg)
    return err
