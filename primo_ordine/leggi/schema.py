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
        if not str(d.get("bilancio") or "").strip():
            _err(fuori, idv, "`bilancio` vuoto: una regola SPOSTA energia, e "
                             "CIO- CHE ESCE DA H DEVE ANDARE DA QUALCHE PARTE -- "
                             "senza quel campo la regola NON si scrive")
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
#   IL COLLAUDO DELLO SCHEMA -- nei due versi, su righe costruite in memoria
# =====================================================================================

def collaudo():
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-66s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    VAR = {"psi": "complesso_c2_nodo", "w": "reale_arco", "theta": "fase_arco",
           "rho": "reale_nodo", "qp": "coppia_coniugata"}

    def base(**kw):
        d = {"id": "PROVA-UNO", "tipo": "termine_nodo", "espressione": "rho**2",
             "ambito": ["rho"], "parametri": {}, "assiomi": [], "prova": True,
             "scheda": "una scheda",
             # ### ⚠ **`rho` NON E- `psi`**, quindi la sostituzione di `U(1)`
             # ### ### **non tocca nessun simbolo** -- ed e- ### **invariante
             # ### davvero**, non per vacuita-: la legge NON COINVOLGE LA FASE.
             "simmetrie": ["U1-FASE-GLOBALE"], "conserva": []}
        d.update(kw)
        return {k: v for k, v in d.items() if v is not None}

    print("=" * 100)
    print("IL COLLAUDO DELLO SCHEMA DELLA TABELLA -- nei DUE VERSI")
    print("=" * 100)
    esito("il caso SANO", valida_legge(base(), VAR) == [])
    esito("### id troppo corto (`AB`)", valida_legge(base(id="AB"), VAR) != [],
          "almeno 4 caratteri")
    esito("### `tipo` fuori vocabolario", valida_legge(base(tipo="PIPPO"), VAR) != [])
    esito("### una chiave NON prevista", valida_legge(base(zzz=1), VAR) != [],
          "il vocabolario e- CHIUSO")
    esito("### `scheda` vuota", valida_legge(base(scheda=" "), VAR) != [],
          "una legge senza scheda NON si genera")
    esito("### `prova` non booleano", valida_legge(base(prova="si"), VAR) != [])
    esito("### l-ambito nomina una variabile INESISTENTE",
          valida_legge(base(ambito=["non-esiste"]), VAR) != [])
    # ### ⛔ **IL CASO CHE IL MANDATO NOMINA: un termine di nodo che legge un vicino.**
    esito("### un `termine_nodo` con una variabile d-ARCO nell-ambito",
          any("NON VEDE I VICINI" in e
              for e in valida_legge(base(ambito=["w"]), VAR)),
          "una variabile d-ARCO collega due nodi: leggerla E- vedere il vicino")
    esito("NON deve scattare: un `termine_arco` con la STESSA variabile d-arco",
          valida_legge(base(tipo="termine_arco", ambito=["w"]), VAR) == [],
          "un termine d-arco PUO- leggere l-arco: e- il suo mestiere")
    # ### ⛔ **I PARAMETRI: `A1` pretende valore E ORIGINE.**
    esito("### un parametro SENZA `origine`",
          any("MANOPOLA" in e
              for e in valida_legge(base(parametri={"K": {"valore": 1.0}}), VAR)),
          "`A1`: la legge, NON il numero")
    esito("### un parametro senza `dimensione`",
          any("CHE COSA SIA" in e
              for e in valida_legge(base(parametri={"K": {
                  "valore": 1.0, "origine": "valore di prova"}}), VAR)),
          "### un numero senza dimensione e- un numero di cui non si sa CHE COSA SIA")
    esito("NON deve scattare: un parametro con `valore`, `origine` E `dimensione`",
          valida_legge(base(parametri={"K": {"valore": 1.0,
                                             "origine": "valore di prova",
                                             "dimensione": "E^1"}}), VAR) == [])
    # ### ⛔ **IL BILANCIO di una regola.**
    reg = {"id": "PROVA-REG", "tipo": "regola", "ingressi": [], "uscite": [],
           "bilancio": "", "assiomi": [], "prova": True, "scheda": "s"}
    esito("### una `regola` col `bilancio` VUOTO",
          any("DA QUALCHE PARTE" in e for e in valida_legge(reg, VAR)),
          "cio- che esce da `H` deve andare da qualche parte")
    reg2 = dict(reg, bilancio="l-energia va nel vuoto")
    esito("NON deve scattare: la stessa regola col bilancio dichiarato",
          valida_legge(reg2, VAR) == [])
    # ### ⛔ **L-OSSERVATORE dichiara la sua VOCE.**
    oss = {"id": "PROVA-OSS", "tipo": "osservatore", "espressione": "rho",
           "ambito": ["rho"], "voce": "", "assiomi": [], "prova": True, "scheda": "s",
           "dimensione": "E^0", "simmetrie": ["U1-FASE-GLOBALE"], "conserva": []}
    esito("### un `osservatore` senza `voce`",
          any("MISURA/CRITERIO" in e for e in valida_legge(oss, VAR)))
    esito("NON deve scattare: lo stesso osservatore con la `voce`",
          valida_legge(dict(oss, voce="Z999-PROVA"), VAR) == [])
    print()
    print("  (b) LE DUE DECISIONI APERTE: AMMESSE, NON SCELTE")
    # ### ⭐ **LA `coppia_coniugata` E- AMMESSA E NON USATA, e il braccio lo PROVA:** un tipo
    # ### che nessuno usa ### **non e- collaudato dall-uso**, solo dallo schema.
    esito("la `coppia_coniugata` e- NEL VOCABOLARIO (decisione `13`, aperta)",
          "coppia_coniugata" in TIPI_VARIABILE)
    esito("e lo schema ACCETTA una legge che la legge",
          valida_legge(base(ambito=["qp"]), VAR) == [],
          "AMMESSA, e NESSUNA legge della tabella la usa: non e- SCELTA")
    esito("### e `pos` NON e- un tipo di variabile (decisione `9`, aperta)",
          not any("pos" in k for k in TIPI_VARIABILE),
          "il formato NON PUO- esprimere una geometria, quindi non ne sceglie una")
    esito("### e un-espressione che nomina `pos` si RICONOSCE",
          simboli_vietati("K * pos_x + rho") == ["pos_x"],
          "`A17` per costruzione")
    esito("NON deve scattare: un-espressione che nomina `rho`",
          simboli_vietati("K * rho**2") == [])
    # ### ⚠ **E `x` dentro una parola NON conta:** `max`, `xi`, `index`.
    esito("NON deve scattare: `x` DENTRO una parola (`max`, `xi`, `index`)",
          simboli_vietati("max(xi) + index") == [],
          "i confini di parola: e- la quarta volta che una parola dentro un-altra inganna")
    print()
    print("  (c) IL VOCABOLARIO DELLE VARIABILI")
    esito("una variabile SANA",
          valida_variabile({"nome": "rho", "tipo": "reale_nodo", "voce": "V-X",
                            "scheda": "s", "dimensione": "E^1"}) == [])
    esito("### una variabile SENZA `dimensione`",
          any("`hbar = 1`" in e for e in valida_variabile(
              {"nome": "rho", "tipo": "reale_nodo", "voce": "V-X", "scheda": "s"})),
          "### e la dimensione sta SULLA VARIABILE, non sul tipo: due `reale_nodo` "
          "possono essere UN-ENERGIA E UN TEMPO")
    # ===================================================================================
    #   ### ⭐ **IL CONTROLLO DIMENSIONALE, provato DIRETTAMENTE** *(punto `2`)*
    # ===================================================================================
    # ### ⚠ **E si prova QUI e non attraverso `valida_legge`, per una ragione che
    # ### dichiaro:** `valida_legge` prende `variabili` in ### **DUE FORME** -- la tabella
    # ### vera gli passa ### **una lista di dizionari** *(che portano la `dimensione`)*,
    # ### questo collaudo gli passa ### **un dizionario `nome -> tipo`** *(che non la
    # ### porta)*. ### **Quindi il controllo dimensionale li- NON GIRA**, e provarlo
    # ### attraverso quella via ### **direbbe PASSA senza aver guardato niente.**
    # ### ✅ **`dimensioni_incoerenti` e- PURA: si prova su righe costruite a mano.**
    print()
    print("  (e) LE DIMENSIONI -- punto 2 della terza parte")
    DIM = {"psi": "E^0"}
    HOP = {"id": "PROVA-DIM", "tipo": "termine_arco",
           "espressione": "-K*(psi_i_0c*psi_j_0 + psi_j_0c*psi_i_0)",
           "parametri": {"K": {"dimensione": "E^1"}}}
    esito("NON deve scattare: un termine d-arco con `K` di dimensione `E^1`",
          dimensioni_incoerenti(HOP, DIM) == [],
          "### `psi` e- ADIMENSIONALE (`psi^dag psi` e- un CONTEGGIO), quindi `K` deve "
          "essere un-energia perche- il termine entri in `H`")
    esito("### DEVE scattare: lo stesso termine con `K` di dimensione `E^2`",
          any("NON E- UN TERMINE DI `H`" in e for e in dimensioni_incoerenti(
              dict(HOP, parametri={"K": {"dimensione": "E^2"}}), DIM)),
          "### `H` E- UN-ENERGIA: un termine che non lo e- non e- un termine di `H`")
    MIX = {"id": "PROVA-MIX", "tipo": "termine_nodo",
           "espressione": "K*psi_0c*psi_0 + g*psi_0c*psi_0*psi_1c*psi_1",
           "parametri": {"K": {"dimensione": "E^1"}, "g": {"dimensione": "E^2"}}}
    esito("### DEVE scattare: DUE ADDENDI di dimensione diversa",
          any("UN-ALTRA FISICA" in e for e in dimensioni_incoerenti(MIX, DIM)),
          "### sommare un-energia e un-energia al quadrato NON e- un errore di "
          "battitura: e- un-altra fisica")
    esito("NON deve scattare: gli stessi addendi con `g` di dimensione `E^1`",
          dimensioni_incoerenti(
              dict(MIX, parametri={"K": {"dimensione": "E^1"},
                                   "g": {"dimensione": "E^1"}}), DIM) == [],
          "### e- il braccio che dice che il controllo NON rifiuta OGNI somma")
    OSS = {"id": "PROVA-OSSD", "tipo": "osservatore", "espressione": "psi_0c*psi_0",
           "dimensione": "E^0", "parametri": {}}
    esito("NON deve scattare: un osservatore `E^0` che misura la NORMA",
          dimensioni_incoerenti(OSS, DIM) == [],
          "### pretendere `E^1` da ogni osservatore VIETEREBBE DI MISURARE LA NORMA, "
          "che e- la prima cosa che si misura")
    esito("### DEVE scattare: lo stesso osservatore che dichiara `E^1`",
          any("dichiara" in e for e in dimensioni_incoerenti(
              dict(OSS, dimensione="E^1"), DIM)),
          "### l-espressione da- `E^0`: una dichiarazione che non coincide e- PEGGIO di "
          "nessuna dichiarazione")
    esito("### DEVE scattare: un simbolo che non risale a nessuna variabile",
          any("non risale" in e for e in dimensioni_incoerenti(
              dict(HOP, espressione="-K*zeta_0c*zeta_0"), DIM)),
          "### non la indovino: un controllo che riempie i buchi da se- NON CONTROLLA "
          "NIENTE")
    esito("### una variabile col `tipo` fuori vocabolario",
          valida_variabile({"nome": "rho", "tipo": "PIPPO", "voce": "V-X",
                            "scheda": "s"}) != [])
    esito("### una variabile chiamata `pos`",
          any("A17" in e for e in valida_variabile({"nome": "pos",
                                                    "tipo": "reale_nodo",
                                                    "voce": "V-X", "scheda": "s"})))
    esito("### una variabile senza `voce`",
          valida_variabile({"nome": "rho", "tipo": "reale_nodo", "voce": "",
                            "scheda": "s"}) != [],
          "ogni variabile ha una voce in `doc/indice/variabili.jsonl` (`P-E3`)")
    print("=" * 100)
    print("IL COLLAUDO DELLO SCHEMA: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1]
             else "### QUALCUNO FALLISCE"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(collaudo())
