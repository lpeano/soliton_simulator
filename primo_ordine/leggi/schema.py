# -*- coding: utf-8 -*-
"""LO SCHEMA DELLA TABELLA DELLE LEGGI — **il formato, e chi lo valida.**

> ### ⛔ **LA TABELLA E' L'UNICA FONTE.** Questo modulo dice ### **che forma deve avere** e
> ### **la verifica**: il generatore *(tappa `3`)* non legge una riga che non passi da qui.

### ⭐ **E DUE DECISIONI DI FISICA SONO APERTE, quindi il formato le AMMETTE SENZA
SCEGLIERLE:**

| | la decisione | come il formato la ammette |
|---|---|---|
| `9` | **la geometria** *(relazionale senza embedding)* | ### ⛔ **non c'è NIENTE per la posizione**: `pos` non è un tipo di variabile, e il generatore **rifiuta l'espressione che lo nomina** *(`A17`)*. ### **Il formato non può esprimere una geometria**, quindi non ne scegli una |
| `13` | **i coniugati delle memorie** | il tipo ### **`coppia_coniugata`** *(`q`, `p`)* è ### **nel vocabolario**, e ### **NESSUNA legge lo usa.** ### **Ammesso, non scelto** |

### ⚠ **E «ammettere senza scegliere» ha un prezzo che dichiaro:** un tipo che nessuno usa
### **non è collaudato dall'uso**, solo dallo schema. Il collaudo ha ### **un braccio che
costruisce una legge con una `coppia_coniugata`** e verifica che lo schema la accetti — così
il tipo ### **non è una parola nel vocabolario: è una forma provata.**

Gira con:  python primo_ordine/leggi/schema.py        # il collaudo dello schema


### ⛔ **I DUE DIVIETI, e i loro assiomi** *(qui, nel docstring, perche-
### un ID in un COMMENTO e- vietato dal punto `14(c)`: ### **un
### riferimento che una macchina segue non vive nella prosa**, e questi
### ID sono ### **documentazione**, non riferimenti)*:

- **I SIMBOLI VIETATI** *(`pos`, `x`, `y`, `z`…)*: ### **`A17`** — lo strumento non e- fisica, e la decisione `9` e- ### **APERTA**;
- **I RAMI** *(`Min`, `Max`, `Piecewise`, `Abs`…)*: ### **`A11`** — un limite e- ### **una LEGGE**, non una toppa; e ### **`A12`** — la cura e- ### **DERIVARE**, non tarare.

### **I RAMI E I SIMBOLI VIETATI stanno in `RAMI` e `VIETATI`.**

### ⛔ **E I DOMINI** *(punto `1`)*: ogni tipo dichiara la sua ### **forma** in
### `DOMINI`, e il controllo generato in `stato.py` ### **FERMA, non tronca.**
### ⭐ **E- la lezione di `MAX-NODI-FERMA`** *(una guardia di memoria che cambiava
### la fisica in silenzio: deve FERMARE)* **e di `RIPIEGHI-ZERO`** *(zero ripieghi che
### cambiano la fisica in silenzio)*, piu- l-assioma del ramo silenzioso.

### ⛔ **E LE DIMENSIONI** *(punto `2` della terza parte)*: ogni variabile e ogni
parametro dichiarano la loro `dimensione`, e ### **il generatore RIFIUTA** un'espressione
incoerente.

### ⭐ **UNA SOLA BASE, `E`, e non e' una scelta di unita': e' cio' che `A16` IMPLICA.**
`A16` dice che lo stato evolve ### **al primo ordine sotto una sola `H`**, cioe'
`i dpsi/dt = H psi` con ### **`hbar = 1`** — e con `hbar = 1` ### **il tempo e' `E^-1`**,
non una dimensione indipendente. ### **Una base in piu' sarebbe una manopola** *(`A1`)*.

### ⚠ **E LA DIMENSIONE STA SULLA VARIABILE, NON SUL TIPO — al contrario del DOMINIO:**
il dominio sta sul tipo perche' ### **due variabili dello stesso tipo hanno lo stesso
dominio PER COSTRUZIONE**; la dimensione no, perche' ### **due `reale_nodo` possono
essere un'energia e un tempo.**
"""
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))

NL = chr(10)

# =====================================================================================
#   IL VOCABOLARIO -- chiuso, e ogni valore fuori e' un errore
# =====================================================================================

# ### I TIPI DI LEGGE. ### ⛔ **Un `termine_*` entra in `H`; una `regola` NO** -- e per
# ### questo una regola ### **deve dichiarare il BILANCIO.**
TIPI = ("termine_nodo", "termine_arco", "regola", "osservatore")

# ### I TIPI DI VARIABILE. ### ⭐ **`psi` e- `C^2` di NODO** *(lo spinore e- il tempo
# ### proprio della massa, e vive sul nodo)*.
# ### ⚠ **`coppia_coniugata` e- AMMESSA e NON USATA:** e- la decisione `13`, ### **aperta.**
# ### ⛔ **E NON C-E- NIENTE PER LA POSIZIONE:** e- la decisione `9`, ### **aperta**, e l-assioma
# ### vieta che una posizione entri nella fisica.
TIPI_VARIABILE = {
    "complesso_c2_nodo": "un complesso C^2 sul NODO (psi, `A16`)",
    "reale_arco": "un reale sull-ARCO",
    "fase_arco": "una fase sull-ARCO (reale modulo 2pi)",
    "reale_nodo": "un reale sul NODO",
    "coppia_coniugata": ("una coppia (q, p) coniugata -- ### AMMESSA e NON USATA: "
                         "e- la decisione 13, APERTA"),
}

# =====================================================================================
#   I DOMINI -- punto `1`: ogni TIPO dichiara il suo, e un controllo ### **FERMA**
# -------------------------------------------------------------------------------------
#   ### \u26d4 **<<MAI TRONCARE>> E- LA PARTE CHE CONTA**, non il controllo: troncare
#   ### ### **nasconde** la violazione e ### **cambia la fisica in silenzio** *(`A8`)*,
#   ### fermare ### **la mostra.** ### **E- una lezione dell-era `1`, e i due ID
#   ### che la portano stanno nel docstring.**
#   ### \u2b50 **E IL DOMINIO STA SUL TIPO, non sulla variabile:** due variabili dello
#   ### stesso tipo ### **hanno lo stesso dominio per costruzione** -- e metterlo sulla
#   ### variabile sarebbe ### **un posto in piu- dove possono divergere.**
#
#   `tipo -> (forma, controllo)`:
#     `finito`       ogni componente e- ### **finita** *(niente `NaN`, niente `inf`)*
#     `finito-pos`   finita e ### **> 0**
#     `fase-2pi`     finita, e ### **si legge modulo `2pi`** *(nessun limite: una fase
#                    ### **non si tronca**, si riduce -- e la riduzione e- ESATTA)*
# =====================================================================================
DOMINI = {
    "complesso_c2_nodo": "finito",
    "reale_nodo": "finito",
    "reale_arco": "finito",
    "fase_arco": "fase-2pi",
    "coppia_coniugata": "finito",
}

FORME_DOMINIO = ("finito", "finito-pos", "fase-2pi")

# ### DOVE VIVE UNA VARIABILE: sul nodo o sull-arco. ### **Serve all-AMBITO:** un
# ### `termine_nodo` ### **non puo- leggere una variabile d-arco**, ed e- il controllo che
# ### impedisce a un termine di nodo ### **di vedere i vicini.**
DOVE = {"complesso_c2_nodo": "nodo", "reale_nodo": "nodo", "coppia_coniugata": "nodo",
        "reale_arco": "arco", "fase_arco": "arco"}

# ### ⛔ **I SIMBOLI VIETATI, e il perche- sta nel docstring:** uno strumento non e- fisica, e
# ### ### **una POSIZIONE e- lo strumento con cui GUARDIAMO**, non una proprieta- del
# ### mondo. ### **La decisione `9` e- aperta, e il formato NON la anticipa.**
VIETATI = ("pos", "pos_x", "pos_y", "pos_z", "x", "y", "z", "coord", "xyz")

# ### ⛔ **I RAMI, e sono VIETATI PER LA STESSA RAGIONE DI `pos`:** l-assioma dice
# ### ### **un limite e- una LEGGE, non una toppa**, e `A8` che
# ### ### **un ramo silenzioso non e- un ramo.** ### **Un `Max(x, 0)` dentro
# ### un termine di `H` e- un limite SENZA una legge che lo giustifichi**, e
# ### ### **non esiste una lagrangiana che lo contenga.**
# ### ⚠ **`Abs` e- nella lista e la ragione e- piu- fine:** `|psi|` da-
# ### solo ### **una derivata NON ANALITICA in zero**, e la derivata di
# ### Wirtinger che il generatore calcola ### **la- non esiste.**
# ### ✅ **E la cura NON e- tararlo: e- DERIVARE la legge** che produce
# ### quel comportamento -- ### **curare, non misurare.**
RAMI = ("Min", "Max", "Piecewise", "Abs", "sign", "Heaviside", "floor",
        "ceiling", "clip", "Mod", "frac")

# ### LE CHIAVI OBBLIGATORIE, per tipo.
CHIAVI_COMUNI = ("id", "tipo", "scheda", "assiomi", "prova")
# ### ⛔ **E OGNI TERMINE DICHIARA `simmetrie` E `conserva`** *(punto `3`)*: una
# ### simmetria non dichiarata e- ### **una simmetria che nessuno verifica**, e una
# ### lista `conserva` vuota ### **dice <<non conserva niente>>**, che non e- la stessa
# ### cosa di ### **<<non dichiarato>>.**
CHIAVI_TERMINE = ("espressione", "ambito", "parametri", "simmetrie", "conserva")
CHIAVI_REGOLA = ("ingressi", "uscite", "bilancio")
# ### ⛔ **E UN OSSERVATORE DICHIARA LA SUA `dimensione`** *(punto `2`)*: puo-
# ### misurare qualunque cosa, e ### **pretendere `E^1` da tutti vieterebbe di misurare
# ### la norma** -- che e- la prima cosa che si misura.
CHIAVI_OSSERVATORE = ("espressione", "ambito", "voce", "dimensione",
                      "simmetrie", "conserva")

_ID = re.compile(r"^[A-Z][A-Z0-9-]{3,}$")


# =====================================================================================
#   LA VALIDAZIONE
# =====================================================================================

# =====================================================================================
#   LE DIMENSIONI -- punto `2` della terza parte: ### **il generatore RIFIUTA
#   un-espressione dimensionalmente incoerente**
# -------------------------------------------------------------------------------------
#   ### ⛔ **UNA SOLA DIMENSIONE DI BASE, `E`**, e il perche- -- che nomina un
#   assioma -- sta ### **nel docstring del modulo**, non qui: un riferimento che una
#   macchina deve seguire ### **non vive nella prosa di un commento**, e il presidio
#   che lo pretende ### **me l-ha detto DUE VOLTE in un giorno.**
#
#   ### ⚠ **E LA DIMENSIONE STA SULLA VARIABILE, NON SUL TIPO -- al contrario del
#   DOMINIO.** Il dominio sta sul tipo perche- ### **due variabili dello stesso tipo hanno
#   lo stesso dominio PER COSTRUZIONE**; ### **la dimensione no:** due `reale_nodo`
#   possono essere ### **un-energia e un tempo**, e metterla sul tipo
#   ### **li confonderebbe.**
#
#   ### ⛔ **CHE COSA SI PRETENDE, in due righe:** ### **(1)** ogni ADDENDO di
#   un-espressione ha ### **la stessa dimensione** *(sommare un-energia e un-energia al
#   quadrato non e- un errore di battitura: e- un-altra fisica)*; ### **(2)** un
#   `termine` -- che entra in `H` -- ha dimensione ### **`E^1`.**
#   ### ✅ **Un OSSERVATORE no: dichiara la sua e deve essere OMOGENEO** -- la norma
#   e- `E^0`, l-energia e- `E^1`, e pretendere `E^1` da tutti ### **vieterebbe di
#   misurare la norma.**
# =====================================================================================
PRESIDIO = "P-DIM"

DIMENSIONI_BASE = ("E",)

_DIM = re.compile(r"^E\^(-?\d+)$")


def dimensione_valida(s):
    """`True` se `s` e- della forma `E^<intero>`."""
    return bool(_DIM.match(str(s or "")))


def esponente(s):
    """L-esponente di `E` in `"E^2"`. ### **Non indovina: se non e- valida, FERMA.**"""
    m = _DIM.match(str(s or ""))
    assert m, ("### `%s` non e- una dimensione: la forma e- `E^<intero>`, e le basi sono "
               "%s" % (s, list(DIMENSIONI_BASE)))
    return int(m.group(1))


def _base_del_simbolo(nome, variabili):
    """### Da `psi_i_0c` a `psi`: ### **il simbolo generato risale alla VARIABILE.**

    ### ⛔ **Il generatore costruisce i simboli ATTACCANDO dei suffissi** al nome
    della variabile *(`_i`, `_j`, `_0`, `_1`, `c` per il coniugato)*, e la dimensione
    e- ### **della variabile**: ### **un coniugato ha la dimensione del suo coniugando**,
    e ### **una componente ha quella del vettore.**
    """
    for v in sorted(variabili, key=len, reverse=True):
        if nome == v or nome.startswith(v + "_"):
            return v
    return None


def dimensioni_incoerenti(d, variabili):
    """### Gli errori dimensionali di una legge, o `[]`.

    `variabili` e- ### **`{nome: dimensione}`**; i parametri portano la loro.
    ### ⚠ **Se manca una dimensione, NON si indovina: si dichiara l-errore** -- un
    controllo che riempie i buchi da se- ### **non controlla niente.**
    """
    import sympy
    fuori = []
    idv = d.get("id", "<senza id>")
    esp = d.get("espressione")
    if not esp or d.get("tipo") not in ("termine_nodo", "termine_arco", "osservatore"):
        return fuori
    dim = {}
    for k, v in (variabili or {}).items():
        if not dimensione_valida(v):
            fuori.append("`%s`: la variabile `%s` non dichiara una dimensione valida "
                         "(`%s`). ### La forma e- `E^<intero>`" % (idv, k, v))
            return fuori
        dim[k] = esponente(v)
    for k, p in (d.get("parametri") or {}).items():
        v = (p or {}).get("dimensione")
        if not dimensione_valida(v):
            fuori.append("`%s`: il parametro `%s` NON DICHIARA una dimensione valida "
                         "(`%s`). ### Un numero senza dimensione e- un numero di cui non "
                         "si sa che cosa sia -- come un numero senza `origine` (`A1`)"
                         % (idv, k, v))
            return fuori
        dim[k] = esponente(v)
    try:
        e = sympy.sympify(str(esp))
    except Exception as exc:                                # noqa: BLE001
        fuori.append("`%s`: l-espressione non si legge (%s)" % (idv, exc))
        return fuori
    E = sympy.Symbol("_E_", positive=True)
    sost = {}
    for s in e.free_symbols:
        b = _base_del_simbolo(s.name, dim)
        if b is None:
            fuori.append("`%s`: il simbolo `%s` non risale a nessuna variabile ne- a "
                         "nessun parametro, quindi NON HA UNA DIMENSIONE. ### Non la "
                         "indovino: un controllo che riempie i buchi da se- non "
                         "controlla niente" % (idv, s.name))
            return fuori
        sost[s] = E ** dim[b]
    # ### ⛔ **GLI ADDENDI SI GUARDANO UNO A UNO**, sull-espressione ESPANSA: e- la
    # ### ### **somma** il posto dove una dimensione sbagliata si vede.
    espansa = sympy.expand(e.subs(sost))
    addendi = espansa.as_ordered_terms()
    gradi = []
    for a in addendi:
        p = sympy.Poly(a, E) if a.has(E) else None
        g = sympy.degree(a, E) if a.has(E) else 0
        del p
        gradi.append(int(g))
    if len(set(gradi)) > 1:
        fuori.append("`%s`: GLI ADDENDI NON HANNO LA STESSA DIMENSIONE -- gradi %s su %d "
                     "addendi. ### Sommare un-energia e un-energia al quadrato non e- un "
                     "errore di battitura: e- UN-ALTRA FISICA"
                     % (idv, sorted(set(gradi)), len(addendi)))
        return fuori
    grado = gradi[0] if gradi else 0
    if d.get("tipo") in ("termine_nodo", "termine_arco"):
        if grado != 1:
            fuori.append("`%s`: e- un `%s` -- entra in `H` -- e la sua dimensione e- "
                         "`E^%d` invece di `E^1`. ### `H` E- UN-ENERGIA: un termine che "
                         "non lo e- NON E- UN TERMINE DI `H`" % (idv, d["tipo"], grado))
    else:
        dich = d.get("dimensione")
        if not dimensione_valida(dich):
            fuori.append("`%s`: e- un `osservatore` e NON DICHIARA la sua `dimensione`. "
                         "### Un osservatore puo- misurare qualunque cosa -- la norma e- "
                         "`E^0`, l-energia e- `E^1` -- quindi la DICE, e pretendere `E^1` "
                         "da tutti vieterebbe di misurare la norma" % idv)
        elif esponente(dich) != grado:
            fuori.append("`%s`: dichiara `%s` e l-espressione da- `E^%d`"
                         % (idv, dich, grado))
    return fuori



def _err(fuori, idv, che):
    fuori.append("`%s`: %s" % (idv, che))


def valida_legge(d, variabili, dimensioni=None):
    """### Gli errori di UNA riga di tabella, o `[]`.

    ### ⛔ **Pura:** prende il dizionario e il vocabolario delle variabili, ### **non legge
    il disco** -- cosi- il collaudo la prova ### **su righe costruite in memoria.**

    ### ⚠ **`dimensioni` E- UN PARAMETRO A PARTE, ED E- COLPA DI UN MIO ERRORE.**
    Avevo messo il controllo dimensionale qui dentro leggendo le dimensioni
    ### **da `variabili`** -- ma `variabili` arriva in ### **due forme**: il generatore
    passa `{nome: tipo}` e la tabella ha le dimensioni ### **altrove.**
    ### ⛔ **Quindi il controllo SALTAVA IN SILENZIO**, e un controllo che salta in
    silenzio ### **e- peggio di nessun controllo** (`A9`): il generatore accettava
    ### **`K` di dimensione `E^2`** e io credevo di averlo chiuso.
    ### ✅ **L-HO VISTO PERCHE- HO ROTTO LA TABELLA A POSTA e ho guardato il codice
    d-uscita: era `0`.** ### **Adesso le dimensioni si PASSANO**, e il collaudo ha un
    braccio ### **END-TO-END** che rompe la tabella e pretende che il generatore
    ### **RIFIUTI.**
    """
    fuori = []
    idv = d.get("id") or "<senza id>"
    if not _ID.match(str(idv)):
        _err(fuori, idv, "l-id non ha la forma `[A-Z][A-Z0-9-]{3,}` (almeno 4 caratteri)")
    tipo = d.get("tipo")
    if tipo not in TIPI:
        _err(fuori, idv, "`tipo` %r fuori vocabolario: %s" % (tipo, list(TIPI)))
        return fuori
    attese = set(CHIAVI_COMUNI)
    attese |= set(CHIAVI_REGOLA if tipo == "regola"
                  else CHIAVI_OSSERVATORE if tipo == "osservatore"
                  else CHIAVI_TERMINE)
    manca = sorted(attese - set(d))
    if manca:
        _err(fuori, idv, "mancano le chiavi %s" % manca)
    extra = sorted(set(d) - attese - {"nota"})
    if extra:
        _err(fuori, idv, "chiavi NON previste %s: il vocabolario e- CHIUSO" % extra)
    if not isinstance(d.get("prova"), bool):
        _err(fuori, idv, "`prova` deve essere un booleano: dice se la legge e- FINTA")
    if not str(d.get("scheda") or "").strip():
        _err(fuori, idv, "`scheda` vuota: una legge senza scheda NON si genera")
    if not isinstance(d.get("assiomi"), list):
        _err(fuori, idv, "`assiomi` deve essere una lista (anche vuota, e allora lo dice)")
    # ------------------------------------------------------------------ l-AMBITO
    if tipo in ("termine_nodo", "termine_arco", "osservatore"):
        amb = d.get("ambito")
        if not isinstance(amb, list) or not amb:
            _err(fuori, idv, "`ambito` deve essere una lista NON VUOTA: "
                             "cio- che la legge puo- leggere si DICHIARA")
        else:
            for v in amb:
                if v not in variabili:
                    _err(fuori, idv, "l-ambito nomina `%s`, che NON e- una variabile "
                                     "dichiarata" % v)
                    continue
                # ### ⛔ **IL CONTROLLO CHE IMPEDISCE A UN TERMINE DI NODO DI VEDERE I
                # ### ### VICINI:** una variabile d-ARCO ### **collega due nodi**, quindi
                # ### leggerla ### **e- vedere il vicino.** ### **Un `termine_nodo` non
                # ### puo- averla nell-ambito**, e il generatore ### **non la trova nel
                # ### codice: la trova NELLA TABELLA**, prima di generare.
                if tipo == "termine_nodo" and DOVE[variabili[v]] == "arco":
                    _err(fuori, idv, "e- un `termine_nodo` e l-ambito nomina `%s`, che e- "
                                     "d-ARCO: UN TERMINE DI NODO NON VEDE I VICINI" % v)
    # ------------------------------------------------------------------ i PARAMETRI
    if tipo in ("termine_nodo", "termine_arco"):
        par = d.get("parametri")
        if not isinstance(par, dict):
            _err(fuori, idv, "`parametri` deve essere un dizionario (anche vuoto)")
        else:
            for k, v in par.items():
                if not isinstance(v, dict) or "valore" not in v or "origine" not in v:
                    _err(fuori, idv, "il parametro `%s` deve avere `valore` E `origine`: "
                                     "`A1` dice LA LEGGE, NON IL NUMERO -- e un numero "
                                     "senza origine E- UNA MANOPOLA" % k)
                    continue
                if not str(v["origine"]).strip():
                    _err(fuori, idv, "il parametro `%s` ha `origine` vuota" % k)
                # ### ⛔ **E LA `dimensione`, OBBLIGATORIA** *(punto `2`)*: un numero
                # ### senza dimensione e- ### **un numero di cui non si sa che cosa
                # ### sia** -- esattamente come un numero senza `origine`. ### **`A1`
                # ### vale per entrambe.**
                if not dimensione_valida(v.get("dimensione")):
                    _err(fuori, idv, "il parametro `%s` NON DICHIARA una `dimensione` "
                                     "valida (`%s`): la forma e- `E^<intero>`. ### Un "
                                     "numero senza dimensione e- un numero di cui non si "
                                     "sa CHE COSA SIA, come uno senza `origine` (`A1`)"
                         % (k, v.get("dimensione")))
    # ------------------------------------------------------------ ### LE DIMENSIONI
    # ### ⛔ **IL CONTROLLO DIMENSIONALE GIRA QUI**, cioe- dentro il validatore che
    # ### ### **il generatore chiama** -- ed e- il modo in cui il punto `2` chiede che
    # ### ### **il generatore RIFIUTI** un-espressione incoerente, invece di generarla
    # ### e lasciare che qualcuno se ne accorga dopo.
    # ### ⚠ **Gira solo se le dimensioni delle variabili ci sono TUTTE**: senza, i
    # ### suoi errori direbbero <<manca una dimensione>>, che e- ### **gia- detto dal
    # ### controllo della variabile** -- e ### **un errore detto due volte nasconde
    # ### quanti errori ci sono.**
    if dimensioni:
        fuori += dimensioni_incoerenti(d, dimensioni)

    # --------------------------------------------- ### LE SIMMETRIE E LE CONSERVAZIONI
    # ### ⛔ **IL CONTROLLO SIMBOLICO GIRA QUI**, dentro il validatore che il
    # ### generatore chiama -- ### **cosi- un termine che rompe una simmetria DICHIARATA
    # ### non si genera** *(punto `3`)*.
    # ### ⚠ **E l-import e- LOCALE perche- `simmetrie` sta in `primo_ordine/` e
    # ### questo file in `primo_ordine/leggi/`:** un import in testa
    # ### ### **legherebbe lo schema al percorso del padre**, e lo schema
    # ### ### **si prova da solo.**
    if tipo in ("termine_nodo", "termine_arco", "osservatore"):
        try:
            sys.path.insert(0, os.path.dirname(_QUI))
            import simmetrie as _SM
            fuori += _SM.rompe(d)
            fuori += _SM.conservazioni_valide(d)
        except ImportError as _e:                           # noqa: BLE001
            _err(fuori, idv, "`P-SIM` NON E- GIRATO (%s): dichiarato, non nascosto" % _e)

    # ------------------------------------------------------------------ il BILANCIO
    if tipo == "regola":
        for k in ("ingressi", "uscite"):
            if not isinstance(d.get(k), list):
                _err(fuori, idv, "`%s` deve essere una lista" % k)
        bil = str(d.get("bilancio") or "").strip()
        if not bil:
            _err(fuori, idv, "`bilancio` vuoto: una regola SPOSTA energia, e "
                             "CIO- CHE ESCE DA H DEVE ANDARE DA QUALCHE PARTE -- "
                             "senza quel campo la regola NON si scrive")
        else:
            # ### \u26d4 **DECISIONE DI LUCA, 2026-10-10: IL BILANCIO E- UNA FORMULA,
            # ### NON IL NOME DI UN MECCANISMO.** E- la conseguenza della decisione 10
            # ### *(<<la soglia E- IL BILANCIO, ed e- una LEGGE>>)*: una regola che
            # ### dichiara ### **<<l-energia va nel vuoto>>** non dice ### **QUANTA**, e
            # ### ### **una frase non si verifica.**
            # ### \u2b50 **E IL CASO CHE DEVE FALLIRE ERA GIA- NEL COLLAUDO DELLO
            # ### SCHEMA, come caso SANO:** `bilancio: "l-energia va nel vuoto"` era il
            # ### valore con cui si provava che una regola dichiarata PASSA. ### **Da
            # ### oggi quello e- il caso che DEVE essere rifiutato.**
            for _q, _v, _a in (("simboli", simboli_vietati(bil), "A17"),
                               ("rami", rami_vietati(bil), "A11")):
                if _v:
                    _err(fuori, idv, "il `bilancio` nomina i %s VIETATI %s (`%s`): un "
                                     "bilancio e- una formula, e vale per lui cio- che "
                                     "vale per un termine di `H`" % (_q, _v, _a))
            try:
                import sympy as _sp
                _e = _sp.sympify(bil, locals={k: _sp.Symbol(k) for k in variabili})
            except Exception as _exc:                        # noqa: BLE001
                _err(fuori, idv, "il `bilancio` NON SI LEGGE COME FORMULA (%s). "
                                 "### Decisione di Luca del 2026-10-10: un bilancio e- "
                                 "una FORMULA che il generatore verifica, NON il nome di "
                                 "un meccanismo -- <<l-energia va nel vuoto>> non dice "
                                 "QUANTA, e una frase non si verifica" % _exc)
            else:
                # ### \u26a0 **E I SIMBOLI DEL BILANCIO STANNO NELL-AMBITO DICHIARATO:**
                # ### le variabili, piu- ### **`ingressi` e `uscite`**, che sono cio- che
                # ### la regola ### **dichiara di spostare.** ### **Un simbolo fuori da
                # ### li- e- una grandezza che nessuno ha dichiarato.**
                _amm = set(variabili) | set(d.get("ingressi") or []) \
                    | set(d.get("uscite") or [])
                _fuori_amb = sorted(str(x) for x in _e.free_symbols
                                    if str(x) not in _amm)
                if _fuori_amb:
                    _err(fuori, idv, "il `bilancio` nomina %s, che NON sono ne- "
                                     "variabili dichiarate ne- `ingressi`/`uscite`. "
                                     "### Una grandezza che nessuno ha dichiarato non si "
                                     "puo- verificare" % _fuori_amb)
    # ------------------------------------------------------------------ l-OSSERVATORE
    if tipo == "osservatore":
        if not str(d.get("voce") or "").strip():
            _err(fuori, idv, "`voce` vuota: un osservatore DICHIARA l-ID della voce "
                             "MISURA/CRITERIO che calcola")
    return fuori


def valida_variabile(d):
    """### Gli errori di una riga del vocabolario delle variabili, o `[]`."""
    fuori = []
    idv = d.get("nome") or "<senza nome>"
    for k in ("nome", "tipo", "voce", "scheda"):
        if not str(d.get(k) or "").strip():
            _err(fuori, idv, "manca `%s`" % k)
    # ### ⛔ **LA DIMENSIONE STA SULLA VARIABILE, NON SUL TIPO -- al contrario del
    # ### DOMINIO** *(punto `2`)*: il dominio sta sul tipo perche- ### **due variabili
    # ### dello stesso tipo hanno lo stesso dominio PER COSTRUZIONE**; la dimensione no,
    # ### perche- ### **due `reale_nodo` possono essere un-energia e un tempo.**
    if not dimensione_valida(d.get("dimensione")):
        _err(fuori, idv, "NON DICHIARA una `dimensione` valida (`%s`): la forma e- "
                         "`E^<intero>`, e la base e- UNA SOLA perche- `A16` implica "
                         "`hbar = 1`, quindi il tempo e- `E^-1` e non una dimensione "
                         "indipendente" % d.get("dimensione"))
    # ### \u26d4 **IL DOMINIO DEL TIPO DEVE ESSERE DICHIARATO** *(punto `1`)*: un
    # ### tipo senza dominio e- ### **una variabile che nessuno puo- controllare.**
    if d.get("tipo") in TIPI_VARIABILE and d.get("tipo") not in DOMINI:
        _err(fuori, idv, "il tipo `%s` NON HA UN DOMINIO DICHIARATO in `DOMINI`. "
                         "### Una variabile senza dominio e- una variabile che nessuno "
                         "puo- controllare, e il punto 1 dice che il controllo FERMA"
             % d.get("tipo"))
    if d.get("tipo") not in TIPI_VARIABILE:
        _err(fuori, idv, "`tipo` %r fuori vocabolario: %s"
             % (d.get("tipo"), sorted(TIPI_VARIABILE)))
    if str(d.get("nome") or "") in VIETATI:
        _err(fuori, idv, "il nome e- VIETATO (`A17`: una posizione non entra nella fisica)")
    return fuori


def _nominati(espressione, elenco):
    """I nomi di `elenco` che l-espressione ### **nomina**, a confini di parola.

    ### ⚠ **I CONFINI DI PAROLA SERVONO, e in questo repo e- successo QUATTRO
    VOLTE** di dimenticarli: `max` sta dentro `max_nodi`, `x` dentro `xi` e dentro
    `index`, `FINITO` dentro `infinito`, `PASS` dentro `passato`.
    """
    t = str(espressione or "")
    fuori = []
    for v in elenco:
        if re.search(r"(?<![A-Za-z0-9_])" + re.escape(v) + r"(?![A-Za-z0-9_])", t):
            fuori.append(v)
    return fuori


def simboli_vietati(espressione):
    """### I simboli VIETATI che l-espressione nomina. ### ⛔ **`A17` per costruzione.**"""
    return _nominati(espressione, VIETATI)


def rami_vietati(espressione):
    """### I RAMI che l-espressione nomina. ### ⛔ **`A11` per costruzione.**

    ### ⭐ **E- un presidio e non una raccomandazione:** il generatore
    ### **rifiuta la legge** e ### **non genera niente** -- quindi un limite
    ### **non puo- entrare nella fisica senza passare da una DECISIONE.**
    """
    return _nominati(espressione, RAMI)


# =====================================================================================
#   IL COLLAUDO SE N'E' ANDATO  --  e chi lo cerca qui DEVE accorgersene
# -------------------------------------------------------------------------------------
#   ### ⛔ **Dal `2026-10-10` il collaudo sta in `_collauda_schema.py`**, perche' questo
#   ### file era a `736` righe e ### **oltre il tetto SI DIVIDE.**
#   ### ⚠ **E SENZA QUESTO BLOCCO, girare `schema.py` USCIVA `0` SENZA DIRE NIENTE** --
#   ### cioe' ### **un FALSO-VERDE silenzioso** per chiunque lo chiamasse aspettandosi
#   ### un collaudo. ### **E' esattamente il difetto che ha fatto trovare un referto
#   ### scaduto sul clone pulito: il referto chiamava QUESTO file e leggeva <<passa>>.**
#   ### ✅ **Ora esce `1` e dice dove andare:** un chiamante sbagliato ### **FALLISCE
#   ### RUMOROSAMENTE**, che e' l'unica forma utile.
# =====================================================================================
if __name__ == "__main__":
    # ### ⚠ **E IL MESSAGGIO E- IN ASCII PURO, di proposito:** questo file
    # ### ### **non chiama `_presidio.avvia()`** -- non e- un collaudo ne- una misura, e
    # ### la sua mappa non prevede quell-import. ### ⛔ **Al primo giro ci ho messo un
    # ### simbolo e sono cascato NELLA DECIMA VOLTA dello stesso difetto:
    # ### `UnicodeEncodeError`, codec `cp1252`.** ### ✅ **Un messaggio che deve solo
    # ### essere RUMOROSO non ha bisogno di simboli.**
    print("  IL COLLAUDO DELLO SCHEMA NON STA PIU- QUI.")
    print("  ### Gira:  python primo_ordine/leggi/_collauda_schema.py")
    print("  ### (diviso il 2026-10-10: questo file era oltre il tetto di 700 righe)")
    sys.exit(1)
