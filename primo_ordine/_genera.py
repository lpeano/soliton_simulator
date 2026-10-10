# -*- coding: utf-8 -*-
"""IL GENERATORE — **dalla tabella al codice e alla scheda.**

> ### ⛔ **LA TABELLA E' L'UNICA FONTE.** Questo attrezzo legge
> `primo_ordine/leggi/leggi.yaml` e scrive ### **un modulo numerico per termine** in
> `primo_ordine/termini/` e ### **una scheda** in `doc/leggi_era2/`.
> ### **I file generati NON si modificano a mano**, e `P-E2` lo impedisce.

### **I QUATTRO PASSI, come il mandato li chiede**

| | |
|---|---|
| `(a)` | i simboli liberi dell'espressione sono ### **DENTRO l'ambito**, e ### **`pos` non esiste** *(`A17` per costruzione)*. ### **Un termine di nodo non vede i vicini** |
| `(b)` | ### **`dH/dpsi*` per differenziazione simbolica**, con `psi` e `psi*` ### **simboli INDIPENDENTI** *(derivata di Wirtinger)* |
| `(c)` | il ### **modulo numerico** *(`numpy` vettorizzato)* con in testa `LEGGE = "<id>"` e ### **l'IMPRONTA della riga di tabella** |
| `(d)` | la ### **scheda** `doc/leggi_era2/<id>.md` |

### ⭐ **COME `psi` DIVENTA SIMBOLI, e perché così:** una variabile
`complesso_c2_nodo` chiamata `psi` diventa ### **quattro simboli** — `psi_0`, `psi_1` e i
### **coniugati INDIPENDENTI** `psi_0c`, `psi_1c`. ### ⛔ **Indipendenti e non
`conjugate(psi_0)`:** la derivata che serve è ### **quella di Wirtinger**, e `sympy` su
`conjugate()` darebbe ### **zero o una forma inutilizzabile.**

### ⚠ **E I NOMI DEI SIMBOLI SONO I NOMI DELLE VARIABILI LOCALI DEL MODULO GENERATO**, di
proposito: così l'espressione stampata da `sympy` ### **è già il codice**, e non c'è
### **nessuna sostituzione testuale** fra la derivata e il file — ### **una sostituzione è
un posto dove la formula può cambiare senza che nessuno lo veda.**

Gira con:  python primo_ordine/_genera.py            # genera tutto
           python primo_ordine/_collauda_genera.py   # il collaudo (24/24)

### ⚠ **E `--prova` NON C'E' PIU'.** Il collaudo sta in
`primo_ordine/_collauda_genera.py` perche' ### **`P-MOD` ha rifiutato il commit:** questo
file era arrivato a ### **`738` righe** sul tetto di `700`, e il presidio dice *<<oltre
### **SI DIVIDE, NON SI ALLUNGA**>>*. ### ⭐ **Alzare il tetto sarebbe stato
esattamente la manopola che `A1` vieta.**
"""
import hashlib
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
# ### ⛔ **IL COSTRUTTO `@rif`** *(punto `14`)*: ### **byte-inerte**, e
# ### ### **collaudato tale** -- `rif(...)` torna ### **la funzione STESSA**, non un
# ### involucro, e il collaudo lo verifica con `is`.
from _rif import rif                                         # noqa: E402
import schema as SCH                                         # noqa: E402
import _genera_stato as GS                                   # noqa: E402

NL = chr(10)
Q3 = chr(34) * 3
TABELLA = os.path.join(_QUI, "leggi", "leggi.yaml")
TERMINI = os.path.join(_QUI, "termini")
OSSERVATORI = os.path.join(_QUI, "osservatori")
SCHEDE = os.path.join(RADICE, "doc", "leggi_era2")


# =====================================================================================
#   I SIMBOLI -- e l'IMPRONTA
# =====================================================================================

def impronta(riga):
    """### L'IMPRONTA di una riga di tabella: `sha1` del `json` ### **a chiavi ordinate.**

    ### ⛔ **A chiavi ordinate perche- l-ordine di un dizionario NON E- UN DATO:** se
    l-impronta dipendesse dall-ordine, ### **riordinare lo yaml rifiuterebbe ogni file** --
    e il presidio accuserebbe ### **una modifica che non c-e- stata.**
    """
    return hashlib.sha1(json.dumps(riga, sort_keys=True, ensure_ascii=False)
                        .encode("utf-8")).hexdigest()[:16]


def simboli_di(nome, tipo, lato=""):
    """### I nomi dei simboli di una variabile. ### **Sono anche i nomi delle locali.**

    `lato` e- `""` per un termine di nodo, `"i"`/`"j"` per i due capi di un arco.
    """
    s = nome + (("_" + lato) if lato else "")
    if tipo == "complesso_c2_nodo":
        return [s + "_0", s + "_1", s + "_0c", s + "_1c"]
    if tipo == "coppia_coniugata":
        # ### ⚠ **AMMESSA E NON USATA** *(decisione `13`, aperta)*: i simboli esistono, e
        # ### ### **nessuna legge li nomina.**
        return [s + "_q", s + "_p"]
    return [s]


def coniugati_di(nome, tipo, lato=""):
    """### I soli simboli ### **CONIUGATI**: sono quelli ### **rispetto a cui si deriva.**"""
    if tipo != "complesso_c2_nodo":
        return []
    s = nome + (("_" + lato) if lato else "")
    return [s + "_0c", s + "_1c"]


def ambiente(legge, variabili):
    """### `(simboli, coniugati)`: i nomi che l-espressione di questa legge puo- usare.

    ### ⛔ **Un `termine_nodo` NON ha il lato `i`/`j`**, e questo e- il secondo presidio
    contro ### **<<un termine di nodo che vede i vicini>>**: il primo e- l-ambito nello
    schema, il secondo e- che ### **i simboli dei vicini NON ESISTONO** nell-ambiente.
    """
    sim, con = [], []
    lati = ("i", "j") if legge["tipo"] == "termine_arco" else ("",)
    for v in legge["ambito"]:
        t = variabili[v]
        for lato in lati:
            if t == "reale_arco" or t == "fase_arco":
                # ### una variabile d-ARCO non ha due capi: e- dell-arco.
                if lato in ("", "i"):
                    sim += simboli_di(v, t)
            else:
                sim += simboli_di(v, t, lato)
                con += coniugati_di(v, t, lato)
    for k in (legge.get("parametri") or {}):
        sim.append(k)
    return (sorted(set(sim)), sorted(set(con)))


# =====================================================================================
#   (a) IL CONTROLLO, (b) LA DERIVATA
# =====================================================================================

# ### ⭐ **E QUESTO E- UN RIFERIMENTO VERO, non prosa:** `controlla()` ### **E- la
# ### guardia** dei tre assiomi, e il `@rif` lo dice ### **all-AST** invece che a chi
# ### legge un commento. ### **Il verso opposto si GENERA**
# ### *(`doc/RIFERIMENTI_era2.md`)*.
@rif("A11", "A17", "A12", ruolo="guardia")
def controlla(legge, variabili):
    """### `(a)`: i simboli liberi ### **dentro l-ambiente**, e ### **`pos` mai.**"""
    import sympy
    fuori = []
    idv = legge["id"]
    viet = SCH.simboli_vietati(legge["espressione"])
    if viet:
        fuori.append("`%s`: l-espressione nomina %s, ### VIETATO (`A17`: una posizione non "
                     "entra nella fisica, e la decisione 9 e- APERTA)" % (idv, viet))
    # ### ⛔ **I RAMI: UN LIMITE E- UNA LEGGE, non una toppa** *(vedi il `@rif`)*.
    # ### Un `Max(x, 0)` dentro un termine di `H` ### **viola la CONSERVAZIONE per costruzione**
    # ### *(non esiste una lagrangiana che lo contenga)*, e ### **la cura non e-
    # ### tararlo: e- DERIVARE la legge** che produce quel comportamento.
    rami = SCH.rami_vietati(legge["espressione"])
    if rami:
        fuori.append("`%s`: l-espressione nomina %s, ### VIETATO (`A11`: un limite e- una "
                     "LEGGE, non una toppa; `A8`: un ramo silenzioso non e- un ramo). "
                     "### Non si tara: si DERIVA la legge che produce quel "
                     "comportamento (`A12`)" % (idv, rami))
    sim, _con = ambiente(legge, variabili)
    try:
        e = sympy.sympify(legge["espressione"], locals={k: sympy.Symbol(k) for k in sim})
    except Exception as exc:
        fuori.append("`%s`: l-espressione non si legge: %s" % (idv, exc))
        return fuori, None
    liberi = sorted(str(x) for x in e.free_symbols)
    extra = [x for x in liberi if x not in sim]
    if extra:
        fuori.append("`%s`: i simboli %s sono FUORI DALL-AMBITO (ammessi: %s). "
                     "### Un termine di nodo NON VEDE I VICINI, e i simboli dei vicini "
                     "NON ESISTONO nel suo ambiente" % (idv, extra, sim))
    # ### ⛔ **E L-ESPRESSIONE DEVE ESSERE REALE, verificato SIMBOLICAMENTE.**
    # ### Senza questo il modulo faceva `np.real(...)` e ### **scartava in silenzio**
    # ### la parte immaginaria: ### **un `H` non hermitiano avrebbe girato senza dire
    # ### niente** *(`A8`)*.
    if not extra:
        reale, d = e_reale(e, legge, variabili)
        if not reale:
            fuori.append("`%s`: l-espressione NON E- REALE. `expr - conj(expr)` = `%s`, "
                         "e non si riduce a zero. ### Un `H` non hermitiano non conserva "
                         "la norma, e un `np.real()` lo scarterebbe IN SILENZIO (`A8`)"
                         % (idv, str(d)[:120]))
    return fuori, e


def conjuga(e, coppie):
    """### L-espressione CONIUGATA, scambiando ogni simbolo con il suo coniugato.

    ### ⛔ **`sympy.conjugate()` NON SERVE QUI:** i coniugati sono ### **simboli
    INDIPENDENTI** *(Wirtinger)*, quindi `conjugate(psi_0)` non e- `psi_0c` -- e-
    ### **un-espressione che sympy non sa ridurre.** ### ➜ **Si SCAMBIA**, con la mappa
    che il generatore conosce.
    """
    import sympy
    m = {}
    for a_, b_ in coppie:
        m[sympy.Symbol(a_)] = sympy.Symbol(b_)
        m[sympy.Symbol(b_)] = sympy.Symbol(a_)
    # ### ⛔ **E ANCHE L-UNITA- IMMAGINARIA SI CONIUGA, ed era un BUCO VERO del mio
    # ### ### controllo:** scambiare i soli simboli lasciava `I*(psi^dag psi)`
    # ### ### **invariato**, quindi `expr - conj(expr)` faceva ### **zero** e un termine
    # ### ### **IMMAGINARIO PURO passava per reale.**
    # ### ⭐ **L-ha trovato un braccio di collaudo che ho scritto per un ALTRO motivo**
    # ### *(provare che <<col c.c.>> non basta)*: ### **il braccio cercava una cosa e ne
    # ### ha trovata un-altra.**
    return e.xreplace(m).xreplace({__import__("sympy").I: -__import__("sympy").I})


def coppie_di(legge, variabili):
    """### Le coppie `(simbolo, suo coniugato)` dell-ambiente di questa legge."""
    fuori = []
    lati = ("i", "j") if legge["tipo"] == "termine_arco" else ("",)
    for v in legge["ambito"]:
        if variabili[v] != "complesso_c2_nodo":
            continue
        for lato in lati:
            s = v + (("_" + lato) if lato else "")
            fuori += [(s + "_0", s + "_0c"), (s + "_1", s + "_1c")]
    return fuori


def e_reale(e, legge, variabili):
    """### `(True/False, la differenza)`: l-espressione e- ### **REALE?**

    ### ⛔ **E QUESTO E- UN DIFETTO CHE IL GUARDIANO HA TROVATO NEL MIO GENERATORE:** il
    modulo faceva `np.real(np.sum(_e))`, e ### **scartava in SILENZIO la parte
    immaginaria.** ### **`A8`: un ramo silenzioso non e- un ramo** -- e un `H` non
    hermitiano ### **avrebbe girato senza dire niente**, dando una dinamica che
    ### **non conserva la norma** e sembrando funzionare.

    ### ✔ **IL CONTROLLO VA SULLA TABELLA, non nel modulo:** si verifica
    ### **SIMBOLICAMENTE** che `expr - conj(expr) == 0`, e ### **si RIFIUTA la legge** se
    non lo e-. ### **Nel modulo resta un `assert` sulla tolleranza**, che e- la rete
    ### **sotto** la verifica, non ### **al posto** di essa.
    """
    import sympy
    d = sympy.simplify(sympy.expand(e - conjuga(e, coppie_di(legge, variabili))))
    return (d == 0, d)


def derivata(e, coniugati):
    """### `(b)`: `dH/dpsi*` per ogni coniugato. ### **Wirtinger, e per questo i coniugati
    sono simboli INDIPENDENTI.**"""
    import sympy
    return {c: sympy.simplify(sympy.diff(e, sympy.Symbol(c))) for c in coniugati}


# =====================================================================================
#   (c) IL MODULO NUMERICO
# =====================================================================================

def _npy(e):
    """L-espressione in sintassi `numpy`. ### **I nomi sono quelli delle locali.**"""
    from sympy.printing.numpy import NumPyPrinter
    return NumPyPrinter({"fully_qualified_modules": False}).doprint(e)


def _locali(legge, variabili):
    """Le righe che legano i ### **simboli** alle ### **fette degli array.**"""
    fuori = []
    arco = legge["tipo"] == "termine_arco"
    for v in legge["ambito"]:
        t = variabili[v]
        if t == "complesso_c2_nodo":
            for lato in (("i", "j") if arco else ("",)):
                s = v + (("_" + lato) if lato else "")
                sorg = ("st[%r][%s]" % (v, {"i": "ii", "j": "jj"}[lato])) if lato \
                    else "st[%r]" % v
                fuori += ["    %s_0 = %s[:, 0]" % (s, sorg),
                          "    %s_1 = %s[:, 1]" % (s, sorg),
                          "    %s_0c = np.conj(%s_0)" % (s, s),
                          "    %s_1c = np.conj(%s_1)" % (s, s)]
        elif t in ("reale_arco", "fase_arco"):
            fuori.append("    %s = st[%r]" % (v, v))
        else:
            fuori.append("    %s = st[%r]" % (v, v))
    for k, d in (legge.get("parametri") or {}).items():
        fuori.append("    %s = PARAMETRI[%r]" % (k, k))
    return fuori


def modulo(legge, variabili, e, grad, imp):
    """### `(c)`: il modulo numerico, ### **con `LEGGE` e l-IMPRONTA in testa.**"""
    idv = legge["id"]
    arco = legge["tipo"] == "termine_arco"
    L = ["# -*- coding: utf-8 -*-",
         Q3 + "GENERATO da `primo_ordine/leggi/leggi.yaml` — "
         "### **NON si modifica a mano.**",
         "",
         "### ⛔ **`P-E2` confronta l-IMPRONTA qui sotto con la riga di tabella e "
         "RIFIUTA il commit** se non corrispondono. ### **Per cambiare questo file si "
         "cambia LA TABELLA e si rigenera.**",
         "",
         "### **La scheda:** `doc/leggi_era2/%s.md`." % idv,
         Q3,
         "import numpy as np",
         "",
         "# ### L-ID DELLA LEGGE: un presidio lo legge ### **via AST**, non per regex.",
         "LEGGE = %r" % idv,
         "# ### L-IMPRONTA della riga di tabella *(`sha1` del `json` a chiavi ordinate)*.",
         "IMPRONTA = %r" % imp,
         "TIPO = %r" % legge["tipo"],
         "AMBITO = %r" % (tuple(legge["ambito"]),),
         "PROVA = %r" % bool(legge["prova"]),
         "# ### LA TOLLERANZA su |Im(H)|: DICHIARATA, non scelta nel momento.",
         "# ### 1e-10 relativo: l-espressione e- VERIFICATA REALE SIMBOLICAMENTE, quindi",
         "# ### qui resta solo l-ERRORE DI VIRGOLA MOBILE -- e 1e-10 e- mille volte",
         "# ### l-epsilon di float64 accumulato su una somma di qualche migliaio di",
         "# ### termini.",
         "TOLL_IM = 1e-10",
         "PARAMETRI = %r" % {k: d["valore"]
                             for k, d in (legge.get("parametri") or {}).items()},
         "",
         ""]
    # ------------------------------------------------------------------ l'energia
    # ### ⛔ **NESSUN DEFAULT NELLA FIRMA** *(punto `15(b)`)*: `ii` e `jj` si
    # ### passano SEMPRE, anche a un termine di nodo che non li usa.
    # ### ⭐ **La firma UNIFORME e- cio- che permette a `hamiltoniana.py` di
    # ### chiamare tutti i termini NELLO STESSO MODO**, senza uno smistamento su
    # ### `TIPO` -- e uno smistamento in meno e- ### **un ramo in meno** (`A8`).
    L += ["def energia(st, ii, jj):",
          '    """### Il contributo di questa legge a `H`. ### **Reale.**"""']
    L += _locali(legge, variabili)
    L += ["    _e = %s" % _npy(e),
          "    _s = np.sum(_e)",
          "    # ### " + chr(0x26D4) + " NON `np.real`: un troncamento SILENZIOSO non e-",
          "    # ### un ramo (`A8`). L-espressione e- VERIFICATA REALE SIMBOLICAMENTE dal",
          "    # ### generatore; questo `assert` e- la rete SOTTO quella verifica, non AL",
          "    # ### POSTO di essa -- e scatta se l-aritmetica in virgola mobile va oltre",
          "    # ### la tolleranza dichiarata.",
          "    _im = abs(float(np.imag(_s)))",
          "    assert _im <= TOLL_IM * max(abs(float(np.real(_s))), 1.0), (",
          "        '%s: |Im(H)| = ' % LEGGE + repr(_im)",
          "        + ' oltre la tolleranza ' + repr(TOLL_IM)",
          "        + ': l-espressione NON e- reale su questi dati')",
          "    return float(np.real(_s))",
          "",
          ""]
    # ------------------------------------------------------------------ il gradiente
    L += ["def gradiente(st, fuori, ii, jj):",
          '    """### `dH/dpsi*`, ### **accumulato in `fuori`**.',
          "",
          "    ### ⚠ **Si ACCUMULA** *(`+=`)*: `hamiltoniana.py` somma i termini",
          "    ### **in un solo posto**, e un termine che SCRIVESSE invece di accumulare",
          "    ### **cancellerebbe i termini prima di lui.**",
          '    """']
    L += _locali(legge, variabili)
    for c, g in sorted(grad.items()):
        # ### il nome del coniugato dice ### **la variabile, il lato e la componente.**
        m = re.match(r"^(.+?)(?:_(i|j))?_([01])c$", c)
        assert m, c
        nome, lato, comp = m.group(1), m.group(2), int(m.group(3))
        if arco and lato:
            L += ["    _g = %s" % _npy(g),
                  "    np.add.at(fuori[%r][:, %d], %s, _g * np.ones_like(%s_%s_%dc))"
                  % (nome, comp, {"i": "ii", "j": "jj"}[lato], nome, lato, comp)]
        else:
            L += ["    fuori[%r][:, %d] += %s" % (nome, comp, _npy(g))]
    L += ["    return fuori", ""]
    return NL.join(L) + NL


# =====================================================================================
#   (d) LA SCHEDA
# =====================================================================================

def modulo_osservatore(legge, variabili, e, imp):
    """### Il modulo di un ### **osservatore**: ### **`misura()`, e NIENTE ALTRO.**

    ### ⛔ **Non ha `gradiente()`, e non per dimenticanza:** un osservatore
    ### **non entra in `H`**, quindi ### **non ha derivata** -- e se un giorno la
    avesse, vorrebbe dire che ### **non era uno strumento** *(`A17`)*.
    """
    idv = legge["id"]
    L = ["# -*- coding: utf-8 -*-",
         Q3 + "GENERATO da `primo_ordine/leggi/leggi.yaml` — "
         "### **NON si modifica a mano.**",
         "",
         "### ⛔ **UN OSSERVATORE LEGGE.** `P-E5` fa girare `misura()` e "
         "confronta lo stato ### **AL BYTE** prima e dopo: ### **una scrittura, "
         "anche involontaria, e- un ERRORE** *(`A17`)*.",
         "",
         "### **La scheda:** `doc/leggi_era2/%s.md`." % idv,
         Q3,
         "import os",
         "import sys",
         "",
         "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))",
         "",
         "import numpy as np",
         "",
         "from _rif import rif",
         "",
         "# ### L-ID: un presidio lo legge ### **via AST**, non per regex.",
         "LEGGE = %r" % idv,
         "IMPRONTA = %r" % imp,
         "TIPO = %r" % legge["tipo"],
         "AMBITO = %r" % (tuple(legge["ambito"]),),
         "PROVA = %r" % bool(legge["prova"]),
         "# ### LA VOCE che questo osservatore MISURA: un presidio la verifica.",
         "VOCE = %r" % legge["voce"],
         "TOLL_IM = 1e-10",
         "",
         ""]
    # ### ⭐ **E L-OSSERVATORE DICHIARA, con un `@rif`, CHE MISURA LA SUA VOCE.**
    # ### ### **E- un riferimento vero**: la voce e- una `MISURA`, e questo codice la
    # ### ### **calcola.** Prima la stessa cosa stava ### **in un commento**, e il punto
    # ### `14(c)` dice che ### **un riferimento nella prosa non e- un riferimento.**
    L += ['@rif(%r, ruolo="misura")' % legge["voce"],
          "def misura(st):",
          '    """### Il valore misurato. ### **Reale, e NON tocca `st`.**"""']
    L += _locali(legge, variabili)
    L += ["    _e = %s" % _npy(e),
          "    _s = np.sum(_e)",
          "    # ### " + chr(0x26D4) + " NON `np.real`: lo stesso motivo dei",
          "    # ### termini (`A8`). L-espressione e- VERIFICATA REALE",
          "    # ### SIMBOLICAMENTE dal generatore, e questo assert e- la rete",
          "    # ### SOTTO quella verifica.",
          "    _im = abs(float(np.imag(_s)))",
          "    assert _im <= TOLL_IM * max(abs(float(np.real(_s))), 1.0), (",
          "        '%s: |Im| = ' % LEGGE + repr(_im)",
          "        + ' oltre la tolleranza ' + repr(TOLL_IM))",
          "    return float(np.real(_s))",
          ""]
    return NL.join(L) + NL

def scheda(legge, e, grad, imp):
    idv = legge["id"]
    L = ["# `%s`%s" % (idv, "  — ### ⚠ **PROVA: NON E' FISICA DECISA**"
                       if legge["prova"] else ""),
         "",
         "> ### ⛔ **QUESTA SCHEDA E' GENERATA** da `primo_ordine/leggi/leggi.yaml` "
         "*(`primo_ordine/_genera.py`)*: ### **non si modifica a mano.**",
         ""]
    if legge["prova"]:
        L += ["> ### ⚠ **E LA LEGGE E' DICHIARATA `prova: true`:** serve a "
              "### **collaudare la catena**, non a dire come va il mondo. "
              "### **Nessuna fisica e' decisa qui.**", ""]
    L += ["| | |", "|---|---|",
          "| **tipo** | `%s` |" % legge["tipo"],
          "| **espressione** | `%s` |" % legge["espressione"],
          "| **ambito** | %s |" % " · ".join("`%s`" % x for x in legge["ambito"]),
          "| **impronta della riga** | `%s` |" % imp,
          "| **assiomi soddisfatti** | %s |"
          % (" · ".join("`%s`" % x for x in legge["assiomi"])
             if legge["assiomi"] else "### ⚠ **nessuno dichiarato**"),
          ""]
    if legge.get("parametri"):
        L += ["## I PARAMETRI", "",
              "> ### ⛔ **`A1`: LA LEGGE, NON IL NUMERO.** Ogni parametro porta "
              "### **il valore E l'origine** — e un numero senza origine e' "
              "### **una manopola.**", "",
              "| | valore | origine |", "|---|--:|---|"]
        for k, d in sorted(legge["parametri"].items()):
            L += ["| `%s` | `%s` | %s |" % (k, d["valore"], d["origine"])]
        L += [""]
    if legge["tipo"] == "osservatore":
        L += ["| **la voce che misura** | `%s` |" % legge["voce"], ""]
    # ### \u26d4 **LA SEZIONE DELLA DERIVATA SOLO SE C-E- UNA DERIVATA:** un
    # ### osservatore non entra in `H`, quindi ### **non ne ha** -- e una tabella
    # ### vuota sotto un titolo che promette una derivata ### **direbbe il falso.**
    if grad:
        L += ["## LA DERIVATA, GENERATA", "",
              "> ### ⭐ **`dH/dpsi*` per differenziazione simbolica**, con `psi` e `psi*` "
              "### **simboli INDIPENDENTI** *(Wirtinger)*. ### **Non e' scritta a mano "
              "in nessun posto.**", "",
              "| rispetto a | `dH/d(...)` |", "|---|---|"]
        for c, g in sorted(grad.items()):
            L += ["| `%s` | `%s` |" % (c, g)]
    L += ["", "## LA SCHEDA, dalla tabella", "", str(legge["scheda"]).strip(), ""]
    return NL.join(L) + NL


# =====================================================================================
#   IL GIRO
# =====================================================================================

def carica():
    import yaml
    d = yaml.safe_load(io.open(TABELLA, encoding="utf-8").read()) or {}
    leggi = d.get("leggi") or []
    varia = d.get("variabili") or []
    return leggi, varia


def genera(verboso=True):
    leggi, varia = carica()
    err = []
    for v in varia:
        err += SCH.valida_variabile(v)
    vocab = {v["nome"]: v["tipo"] for v in varia}
    # ### ⛔ **E LE DIMENSIONI, PASSATE A PARTE** *(punto `2`)*: `vocab` porta
    # ### ### **il TIPO**, e la dimensione sta ### **sulla variabile** -- due cose
    # ### diverse, e il controllo ha bisogno di entrambe.
    # ### ⚠ **Prima le leggevo da `vocab`, e il controllo SALTAVA IN SILENZIO:** il
    # ### generatore accettava `K` di dimensione `E^2`. ### **Visto solo rompendo la
    # ### tabella a posta e guardando il codice d-uscita.**
    dimens = {v["nome"]: v.get("dimensione") for v in varia}
    for lg in leggi:
        err += SCH.valida_legge(lg, vocab, dimens)
    assert not err, ("### LA TABELLA NON PASSA LO SCHEMA, e NON SI GENERA NIENTE:" + NL
                     + NL.join(err[:12]))
    os.makedirs(SCHEDE, exist_ok=True)
    # ### `stato.py` SI GENERA, con l-impronta del blocco `variabili`: la tabella e-
    # ### ### **l-unica fonte**, e una variabile dichiarata in due posti DIVERGEREBBE.
    imp_var = impronta({'variabili': varia})
    io.open(os.path.join(_QUI, 'stato.py'), 'w', encoding='utf-8',
            newline=NL).write(GS.stato_py(varia, imp_var))
    if verboso:
        print('   %-18s primo_ordine/stato.py   impronta %s, %d variabili'
              % ('(lo stato)', imp_var, len(varia)))
    fatti = []
    for lg in leggi:
        if lg["tipo"] not in ("termine_nodo", "termine_arco"):
            continue
        guai, e = controlla(lg, vocab)
        assert not guai, ("### IL CONTROLLO (a) RIFIUTA LA LEGGE, e NON SI GENERA:" + NL
                          + NL.join(guai))
        _sim, con = ambiente(lg, vocab)
        grad = derivata(e, con)
        imp = impronta(lg)
        p1 = os.path.join(TERMINI, lg["id"].lower().replace("-", "_") + ".py")
        io.open(p1, "w", encoding="utf-8", newline=NL).write(
            modulo(lg, vocab, e, grad, imp))
        p2 = os.path.join(SCHEDE, lg["id"] + ".md")
        io.open(p2, "w", encoding="utf-8", newline=NL).write(scheda(lg, e, grad, imp))
        fatti.append((lg["id"], p1, p2, imp, len(grad)))
        if verboso:
            print("   %-18s %s" % (lg["id"], os.path.relpath(p1, RADICE)))
            print("   %-18s %s   impronta %s, %d derivate"
                  % ("", os.path.relpath(p2, RADICE), imp, len(grad)))
    # ### \u26d4 **GLI OSSERVATORI, DALLA STESSA TABELLA.** Non sono un secondo
    # ### formato: ### **sono una riga con `tipo: osservatore`**, e passano dagli
    # ### ### **stessi** controlli `(a)` -- simboli vietati, ambito, REALTA-.
    # ### \u26a0 **Non hanno derivata**, e il generatore ### **non gliene calcola una.**
    os.makedirs(OSSERVATORI, exist_ok=True)
    for lg in leggi:
        if lg["tipo"] != "osservatore":
            continue
        guai, e = controlla(lg, vocab)
        assert not guai, ("### IL CONTROLLO (a) RIFIUTA L-OSSERVATORE, e NON SI GENERA:"
                          + NL + NL.join(guai))
        imp = impronta(lg)
        p1 = os.path.join(OSSERVATORI, lg["id"].lower().replace("-", "_") + ".py")
        io.open(p1, "w", encoding="utf-8", newline=NL).write(
            modulo_osservatore(lg, vocab, e, imp))
        p2 = os.path.join(SCHEDE, lg["id"] + ".md")
        io.open(p2, "w", encoding="utf-8", newline=NL).write(scheda(lg, e, {}, imp))
        fatti.append((lg["id"], p1, p2, imp, 0))
        if verboso:
            print("   %-18s %s" % (lg["id"], os.path.relpath(p1, RADICE)))
            print("   %-18s %s   impronta %s, OSSERVATORE (nessuna derivata)"
                  % ("", os.path.relpath(p2, RADICE), imp))
    return fatti


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    # ### ⚠ **`--prova` NON C-E- PIU-: il collaudo sta in
    # ### `primo_ordine/_collauda_genera.py`**, e il perche- sta nel DOCSTRING di
    # ### questo modulo -- ### **non qui**, perche- nomina un presidio e un assioma, e
    # ### un riferimento che una macchina deve seguire ### **non vive nella prosa di un
    # ### commento.**
    del argv
    fatti = genera()
    print("  generati: %d file di legge (termini e osservatori)" % len(fatti))
    return 0


# =====================================================================================
#   IL COLLAUDO DEL GENERATORE -- i casi che DEVONO fallire
# =====================================================================================

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
