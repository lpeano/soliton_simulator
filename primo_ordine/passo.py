# -*- coding: utf-8 -*-
"""IL PASSO — **lo SCHEDULATORE A STRATI, e i DUE integratori CANDIDATI.**

### ⛔ **LA SCELTA DELL-INTEGRATORE E- UNA DECISIONE DI LUCA** *(il nodo `INT` del
piano)*, e questo file ### **non la prende: ne offre DUE**, misurati nello stesso modo,
e il referto mette i numeri accanto ### **senza scegliere.**

## LA FOTOGRAFIA PER STRATO — *e perche- non e- <<lo stato di inizio passo>>*

Gli archi si spezzano in ### **STRATI DI ARCHI DISGIUNTI** *(nessun nodo in comune)*.
Dentro uno strato ### **tutte le operazioni leggono LA STESSA FOTOGRAFIA** e scrivono in
un buffer separato, quindi ### **il risultato NON dipende dall-ordine** — e il collaudo
lo misura ### **permutando gli archi dentro lo strato: byte-identico.**

### ⚠ **Fra strati l-ordine CONTA**, e allora ### **si DICHIARA** *(la composizione)* ed
e- ### **SIMMETRICO** *(alla Strang)*. ### 📌 **Per l-integratore GLOBALE lo strato e-
UNO: tutto il passo.**

## I TRE LIVELLI DELLO SCHEDULATORE

| | che cosa | commuta? | come si garantisce |
|---|---|---|---|
| `1` | i **termini di `H`** | ### **si** | `math.fsum` per `H`, ### **ordine canonico per ID** per il gradiente *(`hamiltoniana.py`)* |
| `2` | gli **archi dentro uno strato** | ### **si**, sono **disgiunti** | ogni nodo riceve ### **UN SOLO** contributo d-arco: non c-e- somma da riordinare |
| `3` | **fra strati**, e fra `H` e le **regole** | ### ⛔ **NO** | ordine ### **DICHIARATO** nella composizione, ### **SIMMETRICO**, e ### **VALIDATO** |

### ⛔ **E IL LIVELLO `3` NON SI PUO- AGGIUSTARE CON UNA SOMMA ESATTA:** due operatori che
non commutano danno ### **un risultato diverso**, non ### **un arrotondamento diverso.**
### ➜ **L-unica cura e- la SIMMETRIA**, che annulla l-errore di ordine pari.

## `A8b` — NESSUNA CACHE NASCOSTA FRA I PASSI

Un valore che una legge ### **ricorda** dev-essere ### **una variabile dichiarata** in
`stato.py` con la sua voce. ### ⛔ **Un attributo dei moduli di fisica che sopravvive fra
due passi e NON e- dichiarato E- UN ERRORE**, e `senza_cache()` ### **lo misura.**
"""
import math
import os

import numpy as np

import hamiltoniana as HAM
import stato as ST

_QUI = os.path.dirname(os.path.abspath(__file__))

# ### ⛔ **LE OPERAZIONI CHE UNA COMPOSIZIONE PUO- NOMINARE.** Vocabolario
# ### ### **CHIUSO**: un nome fuori lista fa ### **rifiutare la composizione**, e non
# ### c-e- un ramo che <<prova a indovinare>>.
# ### ⚠ **`arco:*` e- UNA FAMIGLIA**, una voce per strato: il numero di strati
# ### ### **dipende dal grafo**, quindi si scopre a tempo di esecuzione.
OPERAZIONI = ("tutto", "nodi")
PREFISSO_ARCO = "arco:"

# =====================================================================================
#   LE DUE COMPOSIZIONI CANDIDATE
# -------------------------------------------------------------------------------------
#   ### ⛔ **NON SONO DUE MANOPOLE: SONO DUE CANDIDATI**, e la scelta e- di Luca.
#   ### Stanno qui, scritte, perche- `A1` pretende che un numero dica da dove viene --
#   ### e ### **un ORDINE e- un dato come un numero.**
# =====================================================================================

# ### `(1)` IL GLOBALE: ### **un solo strato, tutto il grafo.**
COMPOSIZIONE_GLOBALE = (("tutto", 1.0),)


def composizione_locale(n_strati):
    """### `(2)` IL LOCALE: ### **uno strato per volta, alla Strang.**

    `nodi(1/2) arco:0(1/2) ... arco:L-1(1) ... arco:0(1/2) nodi(1/2)`

    ### ⭐ **E- un PALINDROMO per costruzione**, e ### **non per attenzione**: la
    seconda meta- ### **si GENERA rovesciando la prima.** ### ⛔ **Una composizione
    scritta a mano simmetrica <<a occhio>> e- esattamente il posto dove la simmetria si
    perde senza che nessuno lo veda.**
    """
    assert n_strati >= 1, n_strati
    meta = [("nodi", 0.5)] + [(PREFISSO_ARCO + str(k), 0.5)
                              for k in range(n_strati - 1)]
    centro = [(PREFISSO_ARCO + str(n_strati - 1), 1.0)]
    return tuple(meta + centro + meta[::-1])


# =====================================================================================
#   GLI STRATI -- archi DISGIUNTI
# =====================================================================================

def strati(ii, jj):
    """### Gli archi spezzati in ### **strati di archi DISGIUNTI**.

    Colorazione greedy degli archi: ogni arco prende ### **il primo strato in cui
    nessuno dei suoi due capi e- gia- occupato.** ### ⭐ **Deterministica**, perche-
    gli archi si scorrono ### **in ordine canonico `(min, max)`** e non nell-ordine in
    cui il grafo li ha messi.

    ### ⚠ **E L-ORDINE CANONICO NON INTRODUCE UNA DIREZIONE:** la chiave e-
    `(min(i,j), max(i,j))`, quindi ### **l-arco `(3,7)` e l-arco `(7,3)` hanno la STESSA
    chiave** — e lo strato non dipende da come l-arco e- stato scritto.
    """
    ii = np.asarray(ii, dtype=int)
    jj = np.asarray(jj, dtype=int)
    assert ii.shape == jj.shape, (ii.shape, jj.shape)
    ordine = sorted(range(len(ii)),
                    key=lambda k: (min(int(ii[k]), int(jj[k])),
                                   max(int(ii[k]), int(jj[k])), k))
    occupati = []          # una lista di set: i nodi gia' usati in ogni strato
    dentro = []            # una lista di liste: gli indici d'arco di ogni strato
    for k in ordine:
        a, b = int(ii[k]), int(jj[k])
        for s in range(len(occupati)):
            if a not in occupati[s] and b not in occupati[s]:
                occupati[s].update((a, b))
                dentro[s].append(k)
                break
        else:
            occupati.append({a, b})
            dentro.append([k])
    return tuple(np.array(sorted(x), dtype=int) for x in dentro)


# =====================================================================================
#   LA VALIDAZIONE DELLA COMPOSIZIONE
# =====================================================================================

def valida_composizione(comp, n_strati):
    """### Gli errori di una composizione, o `[]`. ### **Pura: non legge il disco.**

    ### ⛔ **I QUATTRO CONTROLLI, e ognuno ha il suo perche-:**

    | | che cosa | perche- |
    |---|---|---|
    | `1` | i **nomi** sono nel vocabolario | un nome ignoto ### **non si indovina** |
    | `2` | la sequenza dei nomi e dei pesi e- un **PALINDROMO** | la simmetria ### **annulla l-errore di ordine pari**: senza di essa l-energia ### **deriva SECOLARMENTE** |
    | `3` | nessun **DOPPIONE consecutivo** | due volte la stessa operazione di fila e- ### **un passo piu- lungo scritto male**, non una composizione |
    | `4` | per ogni operazione, i pesi **sommano a `1`** | altrimenti ### **si integra un tempo diverso da `dt`** -- e nessuno se ne accorgerebbe guardando il codice |
    """
    err = []
    if not comp:
        err.append("la composizione e- VUOTA: un passo che non fa niente non e- un passo")
        return err
    ammessi = set(OPERAZIONI) | {PREFISSO_ARCO + str(k) for k in range(n_strati)}
    nomi = [x[0] for x in comp]
    pesi = [x[1] for x in comp]
    # --- `1` il vocabolario
    for n in nomi:
        if n not in ammessi:
            err.append("l-operazione `%s` non e- nel vocabolario: %s"
                       % (n, sorted(ammessi)))
    # --- `2` la simmetria
    if nomi != nomi[::-1]:
        err.append("la composizione NON E- SIMMETRICA: i nomi sono %s e rovesciati "
                   "%s. ### Una composizione asimmetrica ha un errore di ordine PARI "
                   "che NON si annulla, e l-energia deriva SECOLARMENTE" % (nomi, nomi[::-1]))
    if pesi != pesi[::-1]:
        err.append("i PESI non sono simmetrici: %s contro %s. ### I nomi possono essere "
                   "un palindromo e i pesi no, e allora la simmetria E- FINTA" % (pesi, pesi[::-1]))
    # --- `3` i doppioni
    for k in range(len(nomi) - 1):
        if nomi[k] == nomi[k + 1]:
            err.append("DOPPIONE: `%s` compare DUE VOLTE DI FILA alla posizione %d. "
                       "### Due volte la stessa operazione di seguito e- un passo piu- "
                       "lungo scritto male, non una composizione" % (nomi[k], k))
    # --- `4` i pesi, per operazione
    for n in sorted(set(nomi)):
        s = math.fsum(p for m, p in comp if m == n)
        if s != 1.0:
            err.append("i pesi di `%s` sommano a %r e non a 1.0: ### si integrerebbe un "
                       "tempo DIVERSO da dt, e il codice non lo direbbe" % (n, s))
    return err


# =====================================================================================
#   IL PUNTO MEDIO IMPLICITO -- il mattone di entrambi i candidati
# =====================================================================================

def _per_tipo(termini, tipo):
    return [m for m in termini if m.TIPO == tipo]


def mezzo_implicito(st, ii, jj, dt, termini, iterazioni, toll):
    """### UN sotto-passo di ### **punto medio implicito**, su `(ii, jj)` e `termini`.

    `psi' = psi + dt * (-i) * dH/dpsi*((psi + psi')/2)`, risolto ### **per punto
    fisso.**

    ### ⭐ **PERCHE- QUESTO E NON `RK4`:** e- ### **simmetrico** *(nessuna deriva
    SECOLARE dell-energia)* e ### **conserva esattamente gli invarianti QUADRATICI** --
    e la norma e- quadratica. ### ⛔ **`RK4` perde energia MONOTONAMENTE.**

    ### ⚠ **E LA FOTOGRAFIA E- `st`:** il punto medio legge `st` *(l-inizio del
    sotto-passo)* e `nuovo`, e scrive ### **in un dizionario NUOVO** -- `st`
    ### **non si tocca mai**, e il chiamante lo verifica al byte.

    ### ⛔ **E I NODI CHE QUESTO SOTTO-PASSO NON TOCCA RESTANO IDENTICI AL BYTE:**
    il gradiente la- vale ### **esattamente zero**, e `x + dt*(-1j)*0` ### **e- `x`.**
    ### **E- cio- che rende il cono dell-integratore locale ESATTO e non <<piccolo>>.**
    """
    nuovo = {k: v.copy() for k, v in st.items()}
    scarto, usate = float("inf"), 0
    for _ in range(iterazioni):
        usate += 1
        # ### il PUNTO MEDIO. `0.5*(a+b)` e- esatto al bit e ### **simmetrico in `a`,
        # ### `b`** -- la lerp `a + t*(b-a)` NON lo sarebbe.
        meta = {k: 0.5 * (st[k] + nuovo[k]) for k in st}
        g = HAM.gradiente(meta, ii, jj, termini=termini)
        prossimo = {k: st[k] + dt * (-1j) * g[k] for k in st}
        scarto = max(float(np.max(np.abs(prossimo[k] - nuovo[k]))) for k in st) \
            if st else 0.0
        nuovo = prossimo
        if scarto <= toll:
            break
    return nuovo, scarto, usate


# =====================================================================================
#   I DUE CANDIDATI
# =====================================================================================

def passo_globale(st, ii, jj, dt, termini, iterazioni, toll):
    """### CANDIDATO `1`: ### **punto medio implicito su TUTTO IL GRAFO**, un solo strato.

    ### ⛔ **IL CONO NON E- ESATTO, e lo dico:** il punto fisso ### **itera sul grafo
    intero**, quindi dopo `m` iterazioni l-informazione ha fatto ### **`m` archi**, e a
    convergenza ### **tutto il grafo.** ### ⚠ **Non e- un difetto
    dell-implementazione: e- cio- che significa <<implicito e globale>>.**
    """
    # ### \u26d4 **NESSUN DEFAULT** *(punto `15(b)`)*: `termini`, `iterazioni` e
    # ### `toll` ### **si passano**, e vengono ### **dal file di configurazione.**
    # ### \u26a0 **E `toll` NON E- INNOCUO:** ### **il cono di questo integratore
    # ### DIPENDE DA LUI**, misurato *(`3` archi a `1e-4`, `5` a `1e-8`)*.
    T = termini
    err = valida_composizione(COMPOSIZIONE_GLOBALE, 1)
    assert not err, err
    nuovo, scarto, usate = mezzo_implicito(st, ii, jj, dt, T, iterazioni, toll)
    # ### ⛔ **IL DOMINIO SI CONTROLLA A OGNI PASSO, E FERMA** *(punto `1`)*.
    # ### ### **Non tronca:** troncare nasconderebbe la violazione e cambierebbe la
    # ### fisica ### **in silenzio** *(un ramo silenzioso non e- un ramo)*.
    ST.controlla_domini(nuovo, "dopo un passo GLOBALE")
    return nuovo, {"composizione": COMPOSIZIONE_GLOBALE, "strati": 1,
                   "scarto": scarto, "iterazioni": usate}


def passo_locale(st, ii, jj, dt, termini, iterazioni, toll, gli_strati):
    """### CANDIDATO `2`: ### **uno strato per volta**, composizione simmetrica.

    ### ⭐ **IL CONO E- ESATTO:** ogni sotto-passo tocca ### **gli archi di UNO
    strato**, quindi ### **UN arco per strato** -- e i nodi fuori restano
    ### **identici AL BYTE**, non <<quasi uguali>>.

    ### ⚠ **E NON E- <<il globale fatto meglio>>:** integra
    ### **un-altra cosa** *(un prodotto di esponenziali di strato)*, e il referto mette i
    due accanto ### **senza scegliere** — la scelta e- di Luca *(nodo `INT`)*.
    """
    # ### \u26d4 **NESSUN DEFAULT** *(punto `15(b)`)*. ### **`gli_strati` si passa**:
    # ### ricalcolarli a ogni passo sarebbe ### **un lavoro ripetuto**, e farlo
    # ### ### **solo se non arrivano** e- ### **un default travestito da comodita-.**
    T = termini
    ss = gli_strati
    L = max(len(ss), 1)
    comp = composizione_locale(L)
    err = valida_composizione(comp, L)
    assert not err, err
    nodi = _per_tipo(T, "termine_nodo")
    archi = _per_tipo(T, "termine_arco")
    vuoto = np.zeros(0, dtype=int)
    corrente = st
    tracce = []
    for nome, peso in comp:
        if nome == "nodi":
            corrente, sc, us = mezzo_implicito(corrente, vuoto, vuoto, peso * dt,
                                               nodi, iterazioni, toll)
        else:
            k = int(nome[len(PREFISSO_ARCO):])
            sel = ss[k] if k < len(ss) else vuoto
            corrente, sc, us = mezzo_implicito(corrente, np.asarray(ii)[sel],
                                               np.asarray(jj)[sel], peso * dt,
                                               archi, iterazioni, toll)
        tracce.append((nome, peso, sc, us))
    # ### ⛔ **IL DOMINIO, A OGNI PASSO, E FERMA** *(punto `1`)*.
    # ### ⚠ **A ogni PASSO e non a ogni STRATO**, e lo dichiaro: un sotto-passo
    # ### ### **intermedio** di una composizione simmetrica ### **non e- uno stato
    # ### fisico** -- e- meta- di un-operazione. ### **Controllarlo la- vorrebbe dire
    # ### fermare su uno stato che non esiste.**
    ST.controlla_domini(corrente, "dopo un passo LOCALE")
    return corrente, {"composizione": comp, "strati": L, "tracce": tuple(tracce)}


# =====================================================================================
#   `A8b` -- NESSUNA CACHE NASCOSTA FRA I PASSI
# =====================================================================================

def _costanti_di_modulo(m):
    """I nomi di modulo che ### **non sono funzioni, classi o moduli**, con il loro valore."""
    import types
    fuori = {}
    for k, v in vars(m).items():
        if k.startswith("__"):
            continue
        if isinstance(v, (types.FunctionType, types.ModuleType, type)):
            continue
        fuori[k] = repr(v)
    return fuori


def senza_cache(moduli, azione):
    """### Fa girare `azione()` e dice se un modulo ### **si e- RICORDATO qualcosa.**

    ### ⛔ **`A8b`:** un valore che una legge ricorda dev-essere
    ### **una variabile DICHIARATA in `stato.py`** con la sua voce. Un attributo di
    modulo che ### **nasce o cambia** fra due passi e- ### **una memoria nascosta** --
    e una memoria nascosta ### **rende un passo dipendente da quanti passi sono stati
    fatti prima**, cosa che nessun lettore del codice sospetta.

    ### ⚠ **Non e- una regola scritta: e- un CONFRONTO**, e torna la lista dei
    nomi che sono cambiati.
    """
    prima = {m.__name__: _costanti_di_modulo(m) for m in moduli}
    fuori = azione()
    dopo = {m.__name__: _costanti_di_modulo(m) for m in moduli}
    guai = []
    for nome in sorted(prima):
        a, b = prima[nome], dopo[nome]
        for k in sorted(set(b) - set(a)):
            guai.append("`%s.%s` E- NATO durante il passo: una memoria NON DICHIARATA "
                        "(`A8b`). ### Se la legge deve ricordarlo, va in `stato.py` con "
                        "la sua voce" % (nome, k))
        for k in sorted(set(a) - set(b)):
            guai.append("`%s.%s` E- SPARITO durante il passo" % (nome, k))
        for k in sorted(set(a) & set(b)):
            if a[k] != b[k]:
                guai.append("`%s.%s` E- CAMBIATO durante il passo: da `%s` a `%s`. "
                            "### Una costante di modulo che cambia E- uno stato, e lo "
                            "stato sta in `stato.py`" % (nome, k, a[k][:40], b[k][:40]))
    return guai, fuori
