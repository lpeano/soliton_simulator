# -*- coding: utf-8 -*-
"""PUNTO `11` — **LA MODULARITA' NON SI DEGRADA.**

> ### ⛔ `(a)` **nessuna fisica scritta a mano**: `hamiltoniana`, `passo` e lo
> schedulatore ### **solo sommano, integrano, ordinano** *(controllo AST)*.
> ### ⛔ `(b)` **`primo_ordine/_mappa.yaml`**: chi importa chi, e ### **un import
> fuori mappa, un CICLO o un modulo non in mappa → RIFIUTATO.**
> ### ⛔ `(c)` **un tetto di righe** per file non generato: oltre, ### **si divide,
> non si allunga.**
> ### ⛔ `(d)` ogni modulo dichiara ### **la sua responsabilita' in UNA RIGA.**

### ⭐ **PERCHE' UNA MAPPA E NON SOLO UN DIVIETO:** `P-E4` vieta ### **due** import
*(`osservatori/`, `driver`)* perche' ### **lo strumento non e' fisica.** Una mappa dice
invece ### **la cosa POSITIVA** — cio' che e' ### **previsto** — e
### **un import che nessuno ha previsto e' esattamente quello che degrada la modularita'
senza che nessuno lo decida.**

### ⚠ **E `(d)` HA UN CRITERIO, non e' un adempimento:** se la responsabilita'
### **non si riesce a scrivere in una riga**, ### **il modulo fa due cose** — e
quella e' l'informazione.

### ⛔ **IL TETTO E' DICHIARATO SUL MISURATO** *(`700`, e il piu' lungo e'
`_genera.py` con `684`)*, non scelto a caso. ### **E i generati non hanno tetto:** la
loro lunghezza ### **la decide la tabella**, non chi scrive.
"""
import ast
import glob
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
PRESIDIO = "P-MOD"

MAPPA = os.path.join(RADICE, "primo_ordine", "_mappa.yaml")

# ### ⛔ **CIO- CHE `hamiltoniana` e `passo` POSSONO FARE** *(punto `11(a)`)*: le
# ### funzioni di `numpy` e `math` che ### **sommano, integrano, ordinano** -- e
# ### ### **niente altro.** Una funzione fuori lista e- ### **fisica scritta a mano.**
AMMESSE_SOMMA = (
    # ### sommare e mediare
    "sum", "fsum", "add", "zeros_like", "zeros", "copy", "asarray", "conj",
    # ### ordinare
    "sorted", "sort", "argsort", "max", "min", "len", "range", "enumerate", "zip",
    # ### misurare lo scarto di un punto fisso
    "abs", "float", "int", "bool", "repr", "str", "tuple", "list", "dict", "set",
    # ### la struttura
    "items", "keys", "values", "append", "update", "insert", "join", "replace",
    "split", "startswith", "endswith", "strip", "lower", "upper", "format",
    "isinstance", "getattr", "hasattr", "vars", "print", "AssertionError",
    "NotImplementedError", "all", "any", "isfinite", "real", "imag", "ones_like",
    "arange", "permutation", "default_rng", "normal", "shape", "dirname", "abspath",
    "basename", "listdir", "exists", "isdir", "spec_from_file_location",
    "module_from_spec", "exec_module", "rif", "controlla_domini", "strati",
    "valida_composizione", "composizione_locale", "mezzo_implicito", "carica_termini",
    "energia", "gradiente", "_per_tipo", "_costanti_di_modulo", "senza_cache",
    "nuovo", "reversed", "setdefault", "pop", "count", "index", "tobytes",
    "FunctionType", "ModuleType", "add_at",
    # ### ✅ **`controlla` e- il controllo del GRAFO** *(punto `4`)*: guarda indici,
    # ### doppioni e auto-archi, e ### **non calcola nessuna grandezza fisica.**
    # ### ⚠ **E se un giorno calcolasse, questa riga sarebbe la bugia che lo
    # ### nasconde** -- per questo il nome e- qui ### **con il suo perche-**, e non in
    # ### fondo a un elenco.
    "controlla",
    # ### ⚠ **E QUESTE DUE LE HA TROVATE IL PRESIDIO, al primo giro:** `array`
    # ### *(costruisce un array dagli strati: ### **struttura**, non fisica)* e
    # ### `azione` *(### **il callable che `senza_cache` fa girare**: e- un argomento,
    # ### non una funzione di `numpy`)*. ### **Dichiarate invece di allargare la regola.**
    "array", "azione",
)

# ### ⛔ **E QUESTE SONO FISICA, se stanno in `hamiltoniana` o `passo`:** una
# ### funzione che ### **calcola una grandezza** invece di sommarla.
VIETATE_FISICA = ("exp", "log", "sin", "cos", "tan", "sqrt", "tanh", "arctan",
                  "arcsin", "arccos", "power", "angle", "sign", "clip", "where",
                  "maximum", "minimum", "piecewise", "heaviside")

SOLO_SOMMANO = ("hamiltoniana.py", "passo.py")


def mappa():
    import yaml
    return yaml.safe_load(io.open(MAPPA, encoding="utf-8").read()) or {}


def file_era2():
    f = sorted(glob.glob(os.path.join(RADICE, "primo_ordine", "**", "*.py"),
                         recursive=True))
    base = os.path.join(RADICE, "primo_ordine").replace(os.sep, "/")
    return [x.replace(os.sep, "/")[len(base) + 1:] for x in f
            if "__pycache__" not in x]


def _import(rel):
    p = os.path.join(RADICE, "primo_ordine", rel)
    arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
    fuori = set()
    for n in ast.walk(arb):
        if isinstance(n, ast.Import):
            for a in n.names:
                fuori.add(a.name.split(".")[0])
        if isinstance(n, ast.ImportFrom) and n.module:
            fuori.add(n.module.split(".")[0])
    return fuori


def _nomi_moduli(m):
    return {x["nome"] for x in (m.get("moduli") or [])}


def _locali(m):
    """I nomi di modulo ### **dell-era `2`**, come si scrivono in un `import`."""
    fuori = set()
    for x in (m.get("moduli") or []):
        fuori.add(os.path.basename(x["nome"])[:-3])
    return fuori


def controlla():
    err = []
    m = mappa()
    per = {x["nome"]: x for x in (m.get("moduli") or [])}
    sul_disco = set(file_era2())
    tetto = m.get("tetto_righe")
    if not isinstance(tetto, int) or tetto < 50:
        err.append("`P-MOD`: `tetto_righe` %r: serve un intero >= 50" % tetto)
    # ------------------------------------------------------------------ `(b)`
    for rel in sorted(sul_disco - set(per)):
        err.append("`P-MOD` `%s`: e- sul disco e NON E- IN MAPPA. ### Un modulo che "
                   "nessuno ha previsto e- esattamente quello che degrada la modularita- "
                   "senza che nessuno lo decida" % rel)
    for rel in sorted(set(per) - sul_disco):
        err.append("`P-MOD` `%s`: e- IN MAPPA e non sul disco" % rel)
    locali = _locali(m)
    for rel in sorted(sul_disco & set(per)):
        prev = set(per[rel].get("importa") or [])
        vero = _import(rel) & (locali | {"_presidio", "schema", "schema_config"})
        for i in sorted(vero - prev):
            err.append("`P-MOD` `%s`: importa `%s`, che NON E- IN MAPPA. ### La mappa "
                       "dice cio- che e- PREVISTO: un import in piu- si DICHIARA, o non "
                       "si fa" % (rel, i))
        for i in sorted(prev - vero):
            err.append("`P-MOD` `%s`: la mappa prevede `%s` e il file NON LO IMPORTA. "
                       "### Una dipendenza dichiarata e non usata resta come un permesso "
                       "che nessuno ha chiesto" % (rel, i))
        # ------------------------------------------------------------------ `(d)`
        resp = str(per[rel].get("responsabilita") or "")
        if not resp.strip():
            err.append("`P-MOD` `%s`: NESSUNA responsabilita- dichiarata" % rel)
        elif NL in resp or len(resp) > 100:
            err.append("`P-MOD` `%s`: la responsabilita- non sta in UNA RIGA (%d "
                       "caratteri). ### Se non si riesce a scriverla in una riga, IL "
                       "MODULO FA DUE COSE" % (rel, len(resp)))
        # ------------------------------------------------------------------ `(c)`
        if not per[rel].get("generato"):
            n = len(io.open(os.path.join(RADICE, "primo_ordine", rel),
                            encoding="utf-8").read().split(NL))
            if n > tetto:
                err.append("`P-MOD` `%s`: %d righe, oltre il tetto di %d. ### Oltre SI "
                           "DIVIDE, NON SI ALLUNGA" % (rel, n, tetto))
    # ------------------------------------------------------------------ i CICLI
    g = {rel: set(per[rel].get("importa") or []) for rel in per}
    nomi = {os.path.basename(r)[:-3]: r for r in per}
    stato = {}

    def gira(r):
        if stato.get(r) == 1:
            return [r]
        if stato.get(r) == 2:
            return None
        stato[r] = 1
        for i in sorted(g.get(r, ())):
            if i in nomi:
                c = gira(nomi[i])
                if c:
                    return [r] + c
        stato[r] = 2
        return None

    for r in sorted(per):
        c = gira(r)
        if c:
            err.append("`P-MOD`: CICLO di import: %s. ### Due moduli che si importano a "
                       "vicenda NON SONO DUE MODULI" % " -> ".join(c))
            break
    # ------------------------------------------------------------------ `(a)`
    for rel in SOLO_SOMMANO:
        if rel not in sul_disco:
            continue
        p = os.path.join(RADICE, "primo_ordine", rel)
        arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
        for n in ast.walk(arb):
            if not isinstance(n, ast.Call):
                continue
            nome = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
            if nome in VIETATE_FISICA:
                err.append("`P-MOD` `%s`: chiama `%s`, che CALCOLA UNA GRANDEZZA. "
                           "### Il punto 11(a): `hamiltoniana` e `passo` SOLO sommano, "
                           "integrano, ordinano -- ### la fisica sta nella TABELLA e "
                           "### SI GENERA" % (rel, nome))
            elif nome and nome not in AMMESSE_SOMMA and not nome.startswith("_"):
                err.append("`P-MOD` `%s`: chiama `%s`, che NON E- in `AMMESSE_SOMMA`. "
                           "### O somma/integra/ordina -- e allora va nella lista, "
                           "DICHIARATA -- o e- fisica scritta a mano" % (rel, nome))
    return err


def _sabota(testo, a, b, che):
    """### Una sabotatura SI ASSERISCE, come ogni altra sostituzione (`P1-quater`).

    ### ⛔ **IL DIFETTO, trovato il `2026-10-10` da un referto che e- diventato
    rosso:** i bracci che DEVONO fallire sabotavano la mappa con un `t.replace` su
    ### **un letterale**, e il mio controllo del grafo ha aggiunto `grafo` alla riga
    `importa` di `passo.py`. ### **La sostituzione e- diventata un NO-OP SILENZIOSO**, e
    ### **due bracci che devono fallire NON fallivano piu-** -- `P-MOD` da `10`/`10` a
    ### **`8`/`10`**, e ### **nessuno se ne e- accorto per un commit intero.**

    ### ⭐ **E NON E- UN CASO ISOLATO: in questo collaudo le sabotature erano SEI,
    tutte su un letterale.** ### **Due erano gia- morte.** ### ✅ **Quindi
    l-ancora si CONTA, e se non e- unica il collaudo MUORE invece di passare.**
    """
    k = testo.count(a)
    if k != 1:
        raise AssertionError(
            "### LA SABOTATURA DI <<%s>> NON MORDE: l-ancora compare %d volte, non 1. "
            "### Un braccio che DEVE fallire e che sabota NIENTE passerebbe per "
            "vacuita- -- ed e- il difetto che ha portato `P-MOD` a 8 su 10." % (che, k))
    return testo.replace(a, b)


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    m = mappa()
    print("=" * 100)
    print("IL COLLAUDO DI `P-MOD` -- nei DUE VERSI")
    print("=" * 100)
    n = len(m.get("moduli") or [])
    esito("sul disco: `P-MOD` TACE", controlla() == [],
          "%d moduli in mappa, tetto %d righe" % (n, m.get("tetto_righe")))
    esito("### il braccio sopra HA MATERIA (la mappa non e- vuota)", n >= 15,
          "%d moduli: se fosse 0 il braccio sarebbe un FALSO-UNO" % n)
    gen = len([1 for x in (m.get("moduli") or []) if x.get("generato")])
    esito("### e i GENERATI sono dichiarati tali (niente tetto)", gen >= 4,
          "%d generati: ### la loro lunghezza la decide LA TABELLA" % gen)
    # --- un modulo NON in mappa
    p2 = os.path.join(RADICE, "primo_ordine", "_finto_modulo.py")
    try:
        io.open(p2, "w", encoding="utf-8", newline=NL).write("# -*- coding: utf-8 -*-" + NL)
        esito("### DEVE scattare: un modulo sul disco e NON in mappa",
              any("NON E- IN MAPPA" in e for e in controlla()),
              "### un modulo che nessuno ha previsto degrada la modularita-")
    finally:
        if os.path.exists(p2):
            os.remove(p2)
    # --- un import in piu'
    per = {x["nome"]: x for x in (m.get("moduli") or [])}
    salva = list(per["passo.py"]["importa"])
    t = io.open(MAPPA, encoding="utf-8").read()
    # ### ✅ **E L-ANCORA SI CALCOLA DALLA MAPPA VERA, non si scrive a mano:** la
    # ### riga di `passo.py` e- cambiata una volta (e- arrivato `grafo`), e un letterale
    # ### ### **sarebbe morto di nuovo.**
    _imp = "    importa: [%s]" % ", ".join(salva)
    _senza = "    importa: [%s]" % ", ".join(
        x for x in salva if x != "hamiltoniana")
    try:
        io.open(MAPPA, "w", encoding="utf-8", newline=NL).write(
            _sabota(t, _imp, _senza, "un import togliato dalla mappa"))
        esito("### DEVE scattare: un import NON in mappa",
              any("NON E- IN MAPPA" in e for e in controlla()),
              "`passo.py` importa `hamiltoniana`, e la mappa non lo prevede piu-")
        io.open(MAPPA, "w", encoding="utf-8", newline=NL).write(
            _sabota(t, _imp, "    importa: [%s]" % ", ".join(salva + ["timbro"]),
                    "un permesso in piu- nella mappa"))
        esito("### DEVE scattare: una dipendenza DICHIARATA e NON USATA",
              any("NON LO IMPORTA" in e for e in controlla()),
              "### un permesso che nessuno ha chiesto")
        io.open(MAPPA, "w", encoding="utf-8", newline=NL).write(
            _sabota(t, "tetto_righe: %d" % m.get("tetto_righe"),
                    "tetto_righe: 60", "il tetto abbassato"))
        esito("### DEVE scattare: un file oltre il TETTO",
              any("oltre il tetto" in e for e in controlla()),
              "### oltre SI DIVIDE, NON SI ALLUNGA")
        io.open(MAPPA, "w", encoding="utf-8", newline=NL).write(
            _sabota(t, "    responsabilita: " + per["passo.py"]["responsabilita"],
                    "    responsabilita: \"" + "x" * 130 + "\"",
                    "una responsabilita- che non sta in una riga"))
        esito("### DEVE scattare: una responsabilita- che NON sta in una riga",
              any("non sta in UNA RIGA" in e for e in controlla()),
              "### se non ci sta, IL MODULO FA DUE COSE")
    finally:
        io.open(MAPPA, "w", encoding="utf-8", newline=NL).write(t)
    del salva
    # --- `(a)`: una funzione di FISICA in `passo.py`
    pp = os.path.join(RADICE, "primo_ordine", "passo.py")
    src = io.open(pp, encoding="utf-8").read()
    try:
        io.open(pp, "w", encoding="utf-8", newline=NL).write(
            _sabota(src, "    nuovo = {k: v.copy() for k, v in st.items()}",
                    "    nuovo = {k: np.exp(v) for k, v in st.items()}",
                    "`exp` dentro `passo.py`"))
        esito("### DEVE scattare: `passo.py` che chiama `exp` (FISICA a mano)",
              any("CALCOLA UNA GRANDEZZA" in e for e in controlla()),
              "### il punto 11(a): somma, integra, ordina -- ### la fisica SI GENERA")
    finally:
        io.open(pp, "w", encoding="utf-8", newline=NL).write(src)
    esito("NON deve scattare: rimesso tutto a posto, `P-MOD` TACE", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    print("=" * 100)
    print("IL COLLAUDO DI `P-MOD`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    m = mappa()
    print("  `P-MOD`: %d moduli in mappa, tetto %d righe, %d generati"
          % (len(m.get("moduli") or []), m.get("tetto_righe"),
             len([1 for x in (m.get("moduli") or []) if x.get("generato")])))
    for e in err[:14]:
        print("  ### %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
