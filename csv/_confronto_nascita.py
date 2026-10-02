# -*- coding: utf-8 -*-
"""**LA REGOLA DI CONFRONTO DI UN SIGILLO SULLA NASCITA — e parte da CIO' CHE LA GRANDEZZA E'.**

**Decisione di Luca, 2026-10-02**, passo **1** della via **(b)**: *«il PRIMO lavoro e' estendere il
sigillo»*.

## ⛔ **IL DIFETTO CHE QUESTA REGOLA CURA**

La regola di oggi *(`csv/_seal_fork/_sig_controllo_unico.py`, `_contatori`)* confronta
### **DUE insiemi**: le grandezze di `REGISTRO_NOMI`, e i **contatori** = ogni attributo che
### **comincia con `_` ED E' UN INTERO.**
### ➜ **E' una regola sul NOME e sul TIPO.** Il contratto del 2026-10-02 ha misurato che
### **TRE grandezze scritte nel perimetro della nascita sfuggono a entrambi gli insiemi:**

| | perche' sfugge |
|---|---|
| `ultima_prob_coppia` | non e' nel registro, ### **non comincia con `_`** |
| `ultima_frac_antifase` | idem |
| ### **`_g_peqn_mediana`** | ### **COMINCIA con `_`** *(e col prefisso `_g_` dei contatori, quindi un lettore la crede coperta)* ### **ma e' un `float`**, e `_contatori` prende solo gli INTERI |

### ⚠ **E non e' un dettaglio:** `_g_peqn_mediana` e' ### **l'unico blocco** al punto unico di
nascita *(`csv/_test_fork/_punto_unico_fattibile/`)*. ### **Se il sigillo non la guarda, il commit
che la cambia PASSA, e il difetto e' silenzioso.** E' `A8` applicato al sigillo.

## ⭐ **LA REGOLA NUOVA: TRE INSIEMI, e il terzo parte da CIO' CHE LA GRANDEZZA E'**

| # | l'insieme | da dove viene, e ### **non e' un elenco scritto a mano** |
|--:|---|---|
| **1** | **REGISTRO** | `REGISTRO_NOMI` del modulo |
| **2** | **CONTATORI** | attributi di `net` che cominciano con `_` e sono **interi** *(o tuple di interi, o insiemi di stringhe)* |
| ### **3** | ### **SCRITTE NELLA NASCITA** | ### **l'AST**: ogni `self.<nome>` **scritto** dalle funzioni del perimetro della nascita, ### **che non sia gia' in (1) o (2)**, ### **e di cui qualcuno si accorga** -- cioe' ### **letto altrove nel simulatore** *(fuori dal perimetro)* ### **oppure riportato in un file TRACCIATO da git** |

### ✅ **PERCHE' LA TERZA CONDIZIONE NON E' UN CAPRICCIO**
Senza di lei l'insieme (3) prenderebbe ### **anche le variabili di servizio che nessuno guarda**, e
un sigillo che confronta cio' che nessuno legge ### **fallirebbe per rumore.** Con lei, una
grandezza entra ### **se e solo se un cambiamento su di lei sarebbe VISIBILE a qualcuno** -- il
codice o un referto. ### **E' la definizione di «cio' che la grandezza E'»**, non del suo nome.

### ⚠ **I LIMITI, dichiarati**
**①** *«scritta nel perimetro»* viene dall'**AST**, quindi ### **una scrittura per MUTAZIONE IN
POSTO non si vede** *(`conc_nodi.append`)* -- ed e' lo stesso punto cieco che in questo repo ha
nascosto `conc_nodi` in **due** strumenti diversi. **②** *«riportata in un referto»* e' un `git
grep` sul **nome**: una grandezza riportata **senza nominarla** non si vede. **③** la regola
### **non dice che il perimetro sia quello giusto**: l'elenco delle funzioni e' un **dato** di
questo modulo, e si legge.

COMANDO:  python csv/_confronto_nascita.py          # elenca cosa confronta, e perche'
ASCII puro nel codice.
"""
import ast
import contextlib
import io
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

NL = chr(10)
SIM = os.path.join(RADICE, "soliton_simulator.py")
# IL PERIMETRO DELLA NASCITA, ed e' un DATO di questo modulo: si legge, non si indovina.
#   `decidi_divisione` c'e' perche' la DECISIONE e' parte dell'evento di nascita (e scrive i suoi
#   contatori); i due `_eredita_*` perche' la nascita scrive da la' 13 grandezze del registro.
PERIMETRO = ("mitosi", "decidi_divisione", "semina", "_allaccia",
             "_eredita_psi_figli", "_eredita_spinore_figli",
             "nascita")
# ### E DAL `COMMIT 3` (il PUNTO UNICO) il perimetro ha anche un PREFISSO: le regole
#   di nascita sono funzioni di modulo `_rn_<evento>_<grandezza>`, e scrivono su
#   ### **`net.<nome>`, non `self.<nome>`** -- quindi uno scanner che cercasse solo
#   `self` ### **non le vedrebbe**, e l'insieme da confrontare si restringerebbe
#   ### IN SILENZIO. E' il difetto peggiore che un sigillo possa avere: non
#   sbagliare un verdetto, ma ### **smettere di guardare.**
PREFISSI_PERIMETRO = ("_rn_",)
# ⚠ **E I DUE `_eredita_*` RESTANO NELLA LISTA anche se il simulatore di oggi non li
#   ha piu':** il braccio `D` del sigillo gira sul blob **PRIMA** della cura, dove
#   ci sono. ### **Il perimetro si ALLARGA, non si sposta** -- togliere un nome
#   renderebbe il confronto col passato piu' povero del confronto col presente.


def _nel_perimetro(nome, perimetro=PERIMETRO):
    """Il nome e' nel perimetro della nascita: per elenco **o** per prefisso."""
    return nome in perimetro or any(nome.startswith(p) for p in PREFISSI_PERIMETRO)


def _scritte_nel_perimetro(sorgente=None, perimetro=PERIMETRO):
    """`{nome: [funzioni]}` -- ogni `self.<nome>` SCRITTO dalle funzioni del perimetro."""
    t = ast.parse(io.open(sorgente or SIM, encoding="utf-8").read())
    fuori = {}
    for n in ast.walk(t):
        if not (isinstance(n, ast.FunctionDef) and _nel_perimetro(n.name, perimetro)):
            continue
        for x in ast.walk(n):
            if not isinstance(x, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                continue
            mire = x.targets if isinstance(x, ast.Assign) else [x.target]
            for m in mire:
                for y in ([m] if not isinstance(m, (ast.Tuple, ast.List)) else m.elts):
                    yy = y
                    while isinstance(yy, ast.Subscript):
                        yy = yy.value
                    # ### IL RICEVITORE PUO' ESSERE `net`: le regole di nascita sono
                    #   funzioni di modulo, non metodi, e scrivono `net.<nome>`.
                    if (isinstance(yy, ast.Attribute) and isinstance(yy.value, ast.Name)
                            and yy.value.id in ("self", "net")):
                        fuori.setdefault(yy.attr, set()).add(n.name)
    return {k: sorted(v) for k, v in fuori.items()}


def _letta_fuori_dal_perimetro(sorgente=None, perimetro=PERIMETRO):
    """I nomi `self.<x>` LETTI da una funzione che NON sta nel perimetro."""
    t = ast.parse(io.open(sorgente or SIM, encoding="utf-8").read())
    fuori = set()
    for n in ast.walk(t):
        if isinstance(n, ast.FunctionDef) and _nel_perimetro(n.name, perimetro):
            continue
        if not isinstance(n, (ast.FunctionDef, ast.Module)):
            continue
        for x in ast.walk(n):
            if (isinstance(x, ast.Attribute) and isinstance(x.ctx, ast.Load)
                    and isinstance(x.value, ast.Name) and x.value.id in ("self", "net")):
                fuori.add(x.attr)
    return fuori


def _nei_referti_tracciati(nomi):
    """`{nome: quanti file TRACCIATI lo nominano}` -- il simulatore escluso."""
    fuori = {}
    for k in nomi:
        q = subprocess.run(["git", "grep", "-l", "--", k], cwd=RADICE, capture_output=True)
        righe = [x.strip().replace(chr(92), "/") for x in q.stdout.decode("utf-8",
                                                                         "replace").split(NL)
                 if x.strip() and not x.strip().endswith("soliton_simulator.py")]
        fuori[k] = len(righe)
    return fuori


def contatore(v):
    """La regola di OGGI per un contatore: `_` piu' INTERO (o tupla di interi, o set di stringhe)."""
    if isinstance(v, bool):
        return False
    if isinstance(v, int):
        return True
    if isinstance(v, tuple) and v and all(isinstance(x, int) for x in v):
        return True
    if isinstance(v, set) and all(isinstance(x, str) for x in v):
        return True
    return False


def grandezze(S, net, sorgente=None, includi_assenti=False):
    """`{nome: {"classe","perche"}}` -- l'insieme da confrontare, **DERIVATO**.

    `sorgente` serve ai bracci che girano su una COPIA del simulatore: il perimetro si legge
    **dal sorgente che gira**, non da quello di `HEAD`.

    ### ⚠ **`includi_assenti` NON e' un dettaglio, ed e' un difetto che ho preso al primo giro.**
    Con `hasattr` da solo, una grandezza che ### **nasce solo DOPO un evento** -- `_g_peqn_mediana`
    esiste solo dopo uno Schwinger, `ultima_frac_antifase` solo con `ANTIFASE_ADD` -- ### **non
    entra nell'insieme se la foto si prende troppo presto**, e il sigillo ### **non la
    confronterebbe pur avendo la regola giusta.** Con `includi_assenti` entrano **marcate**, e il
    referto puo' dire ### **quali non sono MAI apparse** invece di tacerle *(e' il braccio `F` del
    controllo unico, applicato qui)*.
    """
    reg = set(getattr(S, "REGISTRO_NOMI", ()))
    fuori = {}
    for k in sorted(reg):
        fuori[k] = {"classe": "registro", "perche": "sta in REGISTRO_NOMI"}
    for k, v in sorted(vars(net).items()):
        if k in fuori:
            continue
        if k.startswith("_") and contatore(v):
            fuori[k] = {"classe": "contatore",
                        "perche": "comincia con `_` ed e' un intero (la regola di OGGI)"}
    scritte = _scritte_nel_perimetro(sorgente)
    lette = _letta_fuori_dal_perimetro(sorgente)
    cand = [k for k in sorted(scritte)
            if k not in fuori and (includi_assenti or hasattr(net, k))]
    ref = _nei_referti_tracciati(cand) if cand else {}
    for k in cand:
        visibile = (k in lette) or (ref.get(k, 0) > 0)
        if not visibile:
            continue
        fuori[k] = {"classe": "scritta-nella-nascita",
                    "assente_ora": not hasattr(net, k),
                    "perche": ("scritta da %s; %s"
                               % (", ".join(scritte[k]),
                                  "letta fuori dal perimetro" if k in lette
                                  else "riportata in %d file tracciati" % ref.get(k, 0)))}
    return fuori


def foto(S, net, sorgente=None):
    """`(valori, perche')` -- lo scatto di tutte le grandezze da confrontare.

    ### ⚠ **Un array di `object` NON si confronta con `array_equal`**: si riduce a `repr`, e lo
    si dichiara. Fingere un confronto numerico su una lista di dizionari darebbe un verdetto che
    non significa niente -- ed e' la famiglia degli errori di CONFRONTO di `A3c`.
    """
    import numpy as np
    quali = grandezze(S, net, sorgente, includi_assenti=True)
    v = {}
    for k in quali:
        if not hasattr(net, k):
            continue
        x = getattr(net, k)
        if x is None:
            continue
        if isinstance(x, (int, float, bool, str)):
            v[k] = x
        elif isinstance(x, (set, frozenset)):
            v[k] = sorted(x)
        else:
            try:
                a = np.asarray(x)
                v[k] = np.array(a, copy=True) if a.dtype != object else repr(x)[:4000]
            except Exception:
                v[k] = repr(x)[:4000]
    return v, quali


def confronta(a, b):
    """L'elenco delle grandezze DIVERSE. I non finiti si confrontano come ELEMENTI."""
    import numpy as np
    diff = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            diff.append({"nome": k, "come": "presente in UNO solo"})
            continue
        x, y = a[k], b[k]
        if isinstance(x, (int, float, bool, str)) and isinstance(y, (int, float, bool, str)):
            if isinstance(x, float) and isinstance(y, float):
                if not (x == y or (x != x and y != y)):
                    diff.append({"nome": k, "come": "scalare float",
                                 "a": repr(x), "b": repr(y),
                                 "ulp": int(abs(np.float64(x).view(np.int64)
                                                - np.float64(y).view(np.int64)))})
            elif x != y:
                diff.append({"nome": k, "come": "scalare", "a": repr(x), "b": repr(y)})
            continue
        if isinstance(x, list) and isinstance(y, list):
            if x != y:
                diff.append({"nome": k, "come": "lista"})
            continue
        xa, ya = np.asarray(x), np.asarray(y)
        if xa.shape != ya.shape:
            diff.append({"nome": k, "come": "forma %s contro %s" % (xa.shape, ya.shape)})
            continue
        with np.errstate(all="ignore"):
            try:
                ok = bool(np.array_equal(xa, ya, equal_nan=True))
            except TypeError:
                ok = bool(np.array_equal(xa, ya))
        if not ok:
            diff.append({"nome": k, "come": "array DIVERSO"})
    return diff


def regola_di_oggi(S, net):
    """L'insieme che il sigillo di OGGI confronta: registro piu' `_`-e-intero. Serve al confronto
    fra le due regole: ### **senza di lui non si puo' mostrare che la nuova vede cio' che la
    vecchia non vedeva.**"""
    reg = set(getattr(S, "REGISTRO_NOMI", ()))
    cont = set(k for k, v in vars(net).items() if k.startswith("_") and contatore(v))
    return reg | cont


def principale():
    import _presidio
    _presidio.avvia(__file__)
    import _cli_flag
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(RADICE, "csv", "_test_fork",
                                                                "_scarto_confronto"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="cfr_nascita")
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    net = S.net
    quali = grandezze(S, net, includi_assenti=True)
    oggi = regola_di_oggi(S, net)
    nuove = [k for k in quali if k not in oggi]
    print("=" * 100)
    print("LA REGOLA DI CONFRONTO DI UN SIGILLO SULLA NASCITA -- che cosa confronta, e perche'")
    print("=" * 100)
    print("  perimetro della nascita (un DATO di questo modulo): %s" % ", ".join(PERIMETRO))
    print("")
    for cl in ("registro", "contatore", "scritta-nella-nascita"):
        q = [k for k in quali if quali[k]["classe"] == cl]
        print("  %-24s %d" % (cl, len(q)))
    print("  " + "-" * 94)
    print("  ### TOTALE da confrontare ......... %d" % len(quali))
    print("  ### la regola di OGGI confronta ... %d" % len(oggi & set(quali)))
    print("  ### GRANDEZZE NUOVE, che oggi SFUGGONO: %d" % len(nuove))
    for k in nuove:
        print("      ### %-26s %-7s %s" % (k, "ASSENTE" if quali[k].get("assente_ora") else "c'e'",
                                          quali[k]["perche"][:58]))
    ass = [k for k in quali if quali[k].get("assente_ora")]
    print("")
    print("  ### E le ASSENTI ORA (nascono solo dopo un evento): %d" % len(ass))
    print("      %s" % ", ".join(ass))
    print("      ### Si includono MARCATE: senza, una grandezza che nasce dopo un evento")
    print("          NON entrerebbe nell'insieme se la foto si prende troppo presto, e il")
    print("          sigillo non la confronterebbe pur avendo la regola giusta.")
    return 0


if __name__ == "__main__":
    sys.exit(principale())
