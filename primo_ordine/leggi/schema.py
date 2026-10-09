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
CHIAVI_TERMINE = ("espressione", "ambito", "parametri")
CHIAVI_REGOLA = ("ingressi", "uscite", "bilancio")
CHIAVI_OSSERVATORE = ("espressione", "ambito", "voce")

_ID = re.compile(r"^[A-Z][A-Z0-9-]{3,}$")


# =====================================================================================
#   LA VALIDAZIONE
# =====================================================================================

def _err(fuori, idv, che):
    fuori.append("`%s`: %s" % (idv, che))


def valida_legge(d, variabili):
    """### Gli errori di UNA riga di tabella, o `[]`.

    ### ⛔ **Pura:** prende il dizionario e il vocabolario delle variabili, ### **non legge
    il disco** -- cosi- il collaudo la prova ### **su righe costruite in memoria.**
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
             "scheda": "una scheda"}
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
    esito("NON deve scattare: un parametro con `valore` E `origine`",
          valida_legge(base(parametri={"K": {"valore": 1.0,
                                             "origine": "valore di prova"}}), VAR) == [])
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
           "ambito": ["rho"], "voce": "", "assiomi": [], "prova": True, "scheda": "s"}
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
                            "scheda": "s"}) == [])
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
