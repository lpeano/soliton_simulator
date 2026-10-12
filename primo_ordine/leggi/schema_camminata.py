# -*- coding: utf-8 -*-
r"""L'ESTENSIONE DELLO SCHEMA PER LA CAMMINATA — **i pezzi unitari, i flussi, l'ordine.**

> ### ⛔ **QUESTO FILE NASCE DA UN PRESIDIO, non da un'idea di eleganza.** L'estensione
> stava dentro `schema.py`, e `P-MOD` l'ha portato a **`731` righe** contro un tetto di
> **`700`** — e la sua regola e' *«oltre SI DIVIDE, NON SI ALLUNGA»*. ### **Quindi si
> divide per SOGGETTO:** `schema.py` tiene la forma generale di una legge, questo file
> tiene **cio' che la camminata aggiunge.**

### ⭐ **E LA DIVISIONE NON ROMPE <<UNA SOLA FONTE>>:** i vocabolari estesi
*(`TIPI`, `TIPI_VARIABILE`, `DOMINI`, `DOVE`)* restano **in `schema.py`**, perche' sono
**una sola lista chiusa**; qui stanno **i vocabolari NUOVI** *(gli operatori, le azioni)*
e **i controlli propri** dei due tipi nuovi.

### ⚠ **E NON IMPORTA `schema.py`, per non fare un ciclo:** le funzioni qui sono **pure** e
ricevono gli aiuti che servono *(`_err`, i divieti)* **come argomenti**. ### **Un ciclo di
import fra due moduli dello stesso soggetto e' il modo piu' rapido di rendere l'ordine di
caricamento una proprieta' della fisica.**

### ⛔ **PERCHE' UN OPERATORE SI SCEGLIE E NON SI SCRIVE** *(il posto `P4` del piano)*: un
operatore come il Grover **somma sulle estremita' del nodo**, e un termine di nodo **non
puo' vedere i vicini** — quindi quell'operatore **non e' esprimibile** nel formato delle
espressioni, e si prende da un **elenco chiuso**. La via alternativa *(un operatore
simbolico «somma sulle estremita' del nodo»)* resta **aperta**.
"""

# ### ⛔ **IL VOCABOLARIO CHIUSO DEGLI OPERATORI UNITARI**, ed e' il contenuto del tipo
# ### `pezzo_unitario`. ### **Ogni voce dice che cosa fa, e quale punto della carta della
# ### fisica la pretende.**
OPERATORI = {
    "moneta_spin": ("exp(-i eps dtau sigma.n) per ESTREMITA-: e- qui che spin e "
                    "direzione si legano (punto F1 della carta)"),
    "grover": ("(2/d) Somma - I nel NODO: mescola le estremita- di uno stesso nodo "
               "(punto F1)"),
    "spostamento_trasporto": ("psi-primo[partner(h)] = U[h] psi[h]: e- il CONO, un arco "
                              "per tick (punti F1 e F2)"),
    "grover_scalare": "il Grover sul vuoto phi, che e- uno SCALARE NEUTRO (punto F4)",
    "spostamento_scalare": ("lo spostamento del vuoto, SENZA U perche- phi e- neutro "
                            "(punto F4)"),
}

# ### ⭐ **DOVE AGISCE UN PEZZO, e i tre valori NON sono decorativi: dicono QUANTE
# ### estremita- il pezzo mescola.** ### **`estremita`** puntuale *(una per volta)* ·
# ### **`nodo`** mescola le estremita- di uno stesso nodo · **`arco`** scambia le due
# ### estremita- dello stesso arco. ### ⛔ **E un pezzo che dichiara `estremita` e poi
# ### legge il vicino sarebbe LOCALE SOLO A PAROLE.**
AZIONI = ("estremita", "nodo", "arco")

# ### ⛔ **UN `pezzo_unitario` NON HA `espressione`: ha un `operatore` e un`azione`.**
# ### **E non ha `conserva`:** un unitario ### **conserva la norma per costruzione**, e
# ### scriverlo sarebbe ### **ripetere una cosa che il tipo garantisce.**
CHIAVI_PEZZO = ("operatore", "azione", "ambito", "parametri", "simmetrie")

# ### ⛔ **UN `flusso` DICHIARA IL SUO GENERATORE E CHE E- ESATTO.** ### ⭐ **Il campo
# ### `esatto` non e- una promessa: e- una DICHIARAZIONE che un collaudo verifica** --
# ### un flusso <<esatto>> che sbaglia all-ordine `dtau^2` ### **e- un flusso approssimato
# ### che mente.**
CHIAVI_FLUSSO = ("generatore", "ambito", "parametri", "esatto", "simmetrie", "conserva")


def errori_pezzo(d, idv, err):
    """### Gli errori propri di un `pezzo_unitario`. ### **`err(che)` li raccoglie.**"""
    op = d.get("operatore")
    if op not in OPERATORI:
        err("`operatore` %r fuori vocabolario: %s. ### Il vocabolario e- CHIUSO perche- "
            "un operatore come il Grover NON si puo- scrivere come espressione in questo "
            "formato (somma sulle estremita- del nodo), e allora si SCEGLIE da un elenco "
            "invece di essere inventato riga per riga" % (op, sorted(OPERATORI)))
    az = d.get("azione")
    if az not in AZIONI:
        err("`azione` %r fuori vocabolario: %s. ### Dice QUANTE estremita- il pezzo "
            "mescola, e un pezzo che dichiara `estremita` e poi legge il vicino sarebbe "
            "LOCALE SOLO A PAROLE" % (az, list(AZIONI)))


def errori_flusso(d, idv, err, simboli_vietati, rami_vietati):
    """### Gli errori propri di un `flusso`.

    ### ⛔ **E IL `generatore` PASSA DAI DIVIETI, perche' E' UNA FORMULA.** ### ⭐ **Questo
    buco l'ho aperto io con l'estensione, e il collaudo nei due versi l'ha preso AL PRIMO
    GIRO:** il divieto delle posizioni guardava `espressione`, e un `flusso` ha
    `generatore` — quindi un generatore che nominava una coordinata **passava**.
    """
    if not str(d.get("generatore") or "").strip():
        err("un `flusso` senza `generatore` NON si genera: il flusso e- DI QUALCOSA, e "
            "quel qualcosa va scritto")
    if not isinstance(d.get("esatto"), bool):
        err("`esatto` deve essere un booleano. ### Non e- una promessa: e- una "
            "DICHIARAZIONE che un collaudo verifica -- un flusso <<esatto>> che sbaglia "
            "all-ordine dtau^2 e- un flusso APPROSSIMATO CHE MENTE")
    gen = str(d.get("generatore") or "")
    for q, v, a in (("simboli", simboli_vietati(gen), "l-assioma sulle posizioni"),
                    ("rami", rami_vietati(gen), "l-assioma sui limiti")):
        if v:
            err("il `generatore` nomina i %s VIETATI %s (%s): un generatore e- una "
                "formula, e vale per lui cio- che vale per un termine dell-hamiltoniana"
                % (q, v, a))


def errori_ordine(ordine, leggi, err):
    """### Gli errori dell'ORDINE DI COMPOSIZIONE.

    > ### ⭐ **E' UNA LISTA, e il posto `P2` del piano si e' CHIUSO su questo argomento**
    > *(del guardiano)*: la composizione di Strang usa ### **LO STESSO PEZZO DUE VOLTE** —
    > mezzo flusso, passo lineare, mezzo flusso — e ### **un campo per pezzo non puo'
    > esprimere un pezzo che compare due volte**, perche' vorrebbe ### **due valori nello
    > stesso campo.** ### **Una lista ammette ripetizioni.**

    ### ⛔ **E OGNI ELEMENTO PORTA LA SUA FRAZIONE DI PASSO**, perche' Strang applica lo
    stesso pezzo a **MEZZO** passo due volte: senza la frazione la lista **direbbe l'ordine
    e non il passo.**

    ### ⭐ **E IL CONTROLLO CHE VALE PIU' DI TUTTI: LA SOMMA DELLE FRAZIONI DI UNA LEGGE
    DEVE FARE `1`.** Una composizione dove le due meta' fanno `0.9` **non integra il passo
    intero** — e **non e' un errore di stile: e' un passo SBAGLIATO**, che nessun altro
    controllo vedrebbe.
    """
    if not isinstance(ordine, list) or not ordine:
        err("l-`ordine` di composizione MANCA o non e- una lista. ### Senza ordine il "
            "passo NON ESISTE: i pezzi non si sommano, si COMPONGONO, e una composizione "
            "senza ordine non e- definita")
        return
    per_id = {str(x.get("id")): x for x in (leggi or []) if isinstance(x, dict)}
    somme = {}
    for k, el in enumerate(ordine):
        dove = "[%d] " % k
        if not isinstance(el, dict):
            err(dove + "ogni elemento e- un dizionario `{legge, frazione}`, e questo e- "
                       "%r" % type(el).__name__)
            continue
        extra = sorted(set(el) - {"legge", "frazione"})
        if extra:
            err(dove + "chiavi NON previste %s: il vocabolario e- CHIUSO" % extra)
        idl = str(el.get("legge") or "")
        if idl not in per_id:
            err(dove + "la legge `%s` NON ESISTE in tabella. ### Un ordine che nomina una "
                       "legge che non c-e- e- un passo che chiama una cosa inesistente"
                % idl)
            continue
        tl = per_id[idl].get("tipo")
        if tl not in ("pezzo_unitario", "flusso"):
            err(dove + "la legge `%s` e- di tipo `%s`, e nell-ordine di composizione "
                       "entrano SOLO `pezzo_unitario` e `flusso`. ### Un termine sta "
                       "DENTRO un generatore, non nella composizione" % (idl, tl))
            continue
        fr = el.get("frazione")
        if not isinstance(fr, (int, float)) or isinstance(fr, bool) or not 0 < fr <= 1:
            err(dove + "`frazione` deve essere un numero in `(0, 1]`, e e- %r. ### E- la "
                       "frazione di passo a cui il pezzo si applica" % (fr,))
            continue
        somme[idl] = somme.get(idl, 0.0) + float(fr)
    for idl, s in sorted(somme.items()):
        # ### ⛔ **ESATTO, non <<vicino>>:** le frazioni di una composizione sono
        # ### ### **numeri scritti a mano in tabella** *(`0.5`, `1`)*, non il risultato di
        # ### un conto -- quindi ### **la loro somma si confronta con `1` ESATTAMENTE**, e
        # ### una tolleranza qui ### **nasconderebbe un `0.9` scritto per sbaglio.**
        if s != 1.0:
            err("le frazioni di `%s` sommano a %r e NON a 1. ### La composizione non "
                "integra il passo intero, e questo non e- uno stile: e- un PASSO "
                "SBAGLIATO" % (idl, s))
