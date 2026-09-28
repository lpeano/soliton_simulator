# -*- coding: utf-8 -*-
"""**LE QUATTRO CLASSI DEI 100 CONFRONTI `len(x) < n`** *(punto ① di `RIPIEGHI-ZERO`)*

**Mandato:** *«CLASSIFICA tutti i 100 confronti, sito per sito, leggendo cosa restituisce il ramo di
scorta: (a) inizializzazione; (b) estensione dei SOLI nuovi senza toccare gli esistenti; (c)
diagnostica o disegno, non fisica; (d) SOSTITUZIONE DI LEGGE o di valore per tutta la rete. Tabella
nel doc, con la riga di codice che giustifica ogni classe.»*

### ⚠ CHE COSA E' AUTOMATICO E CHE COSA E' UNA MIA LETTURA, e va separato

| | criterio | com'e' deciso |
|---|---|---|
| **(c)** | il sito **NON e' raggiungibile** dalle cinque leggi ne' dalle fasi del passo | ### **OGGETTIVO**: se non lo si raggiunge in un passo, **non puo' cambiare la fisica di quel passo**. Nessun giudizio |
| **(b)** | il ramo di scorta **ESTENDE** *(`concatenate`, `vstack`, `resize`, `append`, `full` su una fetta)* | ### **quasi oggettivo**: si legge la forma dell'istruzione |
| **(a)** | la condizione porta anche `is None`, `not hasattr` o `len(...) == 0` | ### **quasi oggettivo**: sono i modi di dire <<non esiste ancora>> |
| **(d)** | ### **tutto il resto** | ### **NON deciso dallo strumento: e' un CANDIDATO da LEGGERE.** Lo strumento lo dice, non lo giudica |

### **Quindi (d) non e' una classe assegnata: e' la lista di cio' che va letto a mano.** *(E' il
contrario di come mi sarebbe venuto naturale: la classe piu' grave e' quella che lo strumento
**rifiuta** di assegnare.)*

COMANDO:  python csv/_test_fork/_classi_ripieghi.py
USCITA:   0 sempre: e' una classificazione, non un sigillo. Scrive la tabella in
          `doc/RIPIEGHI_classi.md` e il referto in `_classi_ripieghi.json`.
"""
import ast
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
SRC = io.open(SIM, encoding="utf-8").read()
RIG = SRC.split(chr(10))
ARB = ast.parse(SRC)
NL = chr(10)

ESTENDE = ("concatenate", "vstack", "hstack", "resize", "append", "pad", "tile", "full",
           "zeros", "ones", "empty")
NONESISTE = ("is None", "not hasattr", "== 0", "is not None")

METODI, FUNZIONI = {}, {}
for _n in ast.walk(ARB):
    if isinstance(_n, ast.ClassDef) and _n.name == "Rete":
        for _k in _n.body:
            if isinstance(_k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                METODI[_k.name] = _k
for _n in ARB.body:
    if isinstance(_n, ast.FunctionDef):
        FUNZIONI[_n.name] = _n


def _fn_di(ln):
    q = [(b.end_lineno - b.lineno, n) for n, b in list(METODI.items()) + list(FUNZIONI.items())
         if b.lineno <= ln <= b.end_lineno]
    return min(q)[1] if q else "(modulo)"


def raggiungibili(radici):
    visti, coda = set(), list(radici)
    while coda:
        x = coda.pop()
        if x in visti:
            continue
        visti.add(x)
        c = METODI.get(x) or FUNZIONI.get(x)
        if c is None:
            continue
        for n in ast.walk(c):
            if isinstance(n, ast.Call):
                f = n.func
                nm = f.attr if isinstance(f, ast.Attribute) else (
                    f.id if isinstance(f, ast.Name) else None)
                if nm and (nm in METODI or nm in FUNZIONI) and nm not in visti:
                    coda.append(nm)
    return visti


def _confronti():
    """Ogni confronto fra un `len(...)` e `n` / `self.n`, con l'`if` che lo contiene."""
    padre = {}
    for nd in ast.walk(ARB):
        for figlio in ast.iter_child_nodes(nd):
            padre[figlio] = nd
    fuori, visti = [], set()
    for nd in ast.walk(ARB):
        if not isinstance(nd, ast.Compare) or len(nd.ops) != 1:
            continue
        for a, b in ((nd.left, nd.comparators[0]), (nd.comparators[0], nd.left)):
            if not (isinstance(a, ast.Call) and isinstance(a.func, ast.Name)
                    and a.func.id == "len" and a.args):
                continue
            try:
                tb, ta = ast.unparse(b), ast.unparse(a.args[0])
            except Exception:
                continue
            if tb not in ("n", "self.n"):
                continue
            k = (nd.lineno, ta)
            if k in visti:
                break
            visti.add(k)
            # ⚠⚠ LA FAMIGLIA DEL CONFRONTO, e la prima stesura le MESCOLAVA TUTTE E TRE:
            #   CORTA  `len(x) < n` oppure `len(x) >= n` -> la cache e' PIU' CORTA di `n`, e il
            #          ramo di scorta e' quello che si prende QUANDO LO E'. E' la famiglia del
            #          mandato.
            #   LUNGA  `len(x) > n` -> la cache e' PIU' LUNGA: quello e' un TRONCAMENTO, un'altra
            #          cosa, e non sostituisce nessuna legge.
            #   ALTRO  `==`, `!=` -> ne' l'uno ne' l'altro.
            # ### E IL RAMO DI SCORTA NON STA SEMPRE NELLO STESSO POSTO: con `<` sta nel CORPO
            #   dell'`if`, con `>=` sta nell'`else` (o FUORI dall'`if`). La prima stesura prendeva
            #   SEMPRE il corpo, quindi per i `>=` riportava IL RAMO BUONO spacciandolo per il ramo
            #   di scorta. **Trovato leggendo la sua uscita, non da un'asserzione.**
            _op = type(nd.ops[0]).__name__
            _corta_se_vero = _op in ("Lt", "LtE", "NotEq")
            # ⚠⚠ `==` E `!=` NON SONO <<FUORI DAL MANDATO>>, e su questo il guardiano ha ragione
            #   su SEI siti piu' uno: `len(x) != n` **INCLUDE** `len(x) < n`, quindi il ramo
            #   scatta ANCHE quando la cache e' corta; e `len(x) == n` protegge IL RAMO BUONO,
            #   quindi il suo `else` scatta ANCHE quando e' corta.
            #   ### Era la TERZA volta che una mia regola di famiglia nascondeva i siti cercati.
            fam = "ALTRO"
            if _op in ("Lt", "LtE", "GtE", "NotEq"):
                fam = "CORTA"
            elif _op == "Eq":
                fam = "CORTA"          # il ramo di scorta e' l'`else` del confronto di uguaglianza
            elif _op == "Gt":
                fam = "LUNGA"
                fam = "LUNGA"
            su, cond, ramo, dove_ramo = nd, None, None, None
            for _ in range(8):
                su = padre.get(su)
                if su is None:
                    break
                if isinstance(su, (ast.If, ast.While)):
                    cond = ast.unparse(su.test)
                    corpo = su.body if _corta_se_vero else (su.orelse or [])
                    dove_ramo = ("corpo dell'if" if _corta_se_vero
                                 else ("else dell'if" if su.orelse
                                       else "FUORI dall'if (nessun else)"))
                    # ⚠ IL CORPO INTERO PER LE REGOLE, troncato SOLO per la tabella: col
                    #   taglio a 220 caratteri il `vstack` di `:3620` cadeva FUORI, e il
                    #   sito finiva fra le SOSTITUZIONI mentre ALLUNGA la coda.
                    #   ### Una regola che legge un testo TRONCATO giudica cio' che non vede.
                    ramo = (NL.join(ast.unparse(x) for x in corpo) if corpo
                            else "(nessun else: si continua dopo l'if)")
                    break
                if isinstance(su, ast.IfExp):
                    cond = ast.unparse(su.test)
                    # ⚠⚠ ERA INVERTITO, e l'incrocio col guardiano l'ha smascherato: in
                    #   `A if len(x) < n else B` il caso CORTA e' **A**, non B; in
                    #   `A if len(x) >= n else B` e' **B**, non A. ### Con l'inversione riportavo
                    #   IL RAMO BUONO come se fosse il ramo di scorta, PER TUTTI gli IfExp -- e da
                    #   li' e' nata una mia <<famiglia 3>> che NON ESISTE. La prova e' :7394,
                    #   dove il ramo vero e' `np.ones(n)`: densita' a UNO per tutta la rete.
                    ramo = ast.unparse(su.body if _corta_se_vero else su.orelse)
                    dove_ramo = "espressione condizionale"
                    break
                if isinstance(su, ast.BoolOp):
                    continue
            fuori.append({"riga": nd.lineno, "dentro": _fn_di(nd.lineno), "cosa": ta,
                          "contro": tb, "op": type(nd.ops[0]).__name__,
                          "condizione": (cond or "")[:200],
                          "ramo_di_scorta": (ramo or "(non trovato)"),
                          "famiglia": fam, "dove_e_il_ramo": dove_ramo or "(?)",
                          "sorgente": RIG[nd.lineno - 1].strip()[:150]})
            break
    # ⚠⚠ E I SITI GIA' CURATI SPARISCONO DALLA SCANSIONE, e il guardiano l'ha notato:
    #   `_rho_sorgente` NON compariva in tabella. La ragione e' che la cura ha SPOSTATO il
    #   confronto DENTRO `_ferma_se_cache_corta`, dove non e' piu' un `len(...)` contro `n`:
    #   ### CURARE UN SITO LO RENDEVA INVISIBILE ALLO STRUMENTO CHE LI CONTA.
    #   Quindi si cercano ANCHE le chiamate ai controlli che sollevano, e sono classe (e).
    #   ### E questo e' un requisito per il PRESIDIO del punto 3: deve vedere ENTRAMBE le
    #   forme, il confronto in chiaro e la chiamata all'helper.
    # ⚠ SOLO `_ferma_se_cache_corta`: `_ferma_se_oltre_max_nodi` guarda il NUMERO DI NODI
    #   contro `MAX_NODI`, che e' un'ALTRA FAMIGLIA -- non una cache piu' corta di `n`.
    #   Contarlo qui gonfiava le (e) da 3 a 5.
    GUARDIE = ("_ferma_se_cache_corta",)
    for nd in ast.walk(ARB):
        if not (isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name)
                and nd.func.id in GUARDIE):
            continue
        _arg = "?"
        for a in nd.args:
            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                _arg = a.value
                break
        fuori.append({"riga": nd.lineno, "dentro": _fn_di(nd.lineno), "cosa": _arg,
                      "contro": "n", "op": "(guardia)", "condizione": "(nessuna: il"
                      " controllo e' UNA CHIAMATA, non un `if`)",
                      "ramo_di_scorta": ast.unparse(nd)[:200],
                      "famiglia": "CORTA", "dove_e_il_ramo": "dentro la guardia",
                      "sorgente": RIG[nd.lineno - 1].strip()[:150]})
    return sorted(fuori, key=lambda x: x["riga"])


COPERTE = set()


def classifica(v, perimetro):
    """La classe, e **la regola che l'ha decisa**. `(d)` non si assegna: si SEGNALA."""
    if v["famiglia"] != "CORTA":
        return "x", ("FUORI DAL MANDATO: famiglia %s -- `len(x) > n` e' un TRONCAMENTO, e "
                     "`==`/`!=` non e' ne' l'uno ne' l'altro" % v["famiglia"])
    r = v["ramo_di_scorta"]
    if "raise " in r or "_ferma_se_cache_corta" in r:
        return "e", "GIA' CURATO: il ramo di scorta SOLLEVA (o chiama il controllo che solleva)"
    # ⚠ E UN CONFRONTO NELLA STESSA FUNZIONE DI UNA GUARDIA E' GIA' COPERTO: in `_nb_grav`
    #   il `len(_ps) >= n` e' RIDONDANTE, perche' la guardia sopra ha gia' sollevato se la
    #   cache era corta. Senza questa regola lo stesso sito compariva DUE VOLTE, una in (e)
    #   e una in (d).
    if v["dentro"] in COPERTE:
        return "e", ("GIA' CURATO: nella stessa funzione c'e' la guardia che solleva, quindi"
                     " questo confronto e' RIDONDANTE")
    if v["dentro"] not in perimetro:
        return "c", "NON raggiungibile dalle cinque leggi ne' dalle fasi del passo"
    # ⚠⚠ (b) CORRETTA (rilievo del guardiano, 2026-09-28): **`np.full(n, ...)`, `zeros(n)`,
    #   `ones(n)` NON ESTENDONO LA CODA: SOSTITUISCONO IL VALORE DI TUTTA LA RETE**, e sono la
    #   stessa famiglia del flash. La mia prima regola li contava come <<estende>> perche'
    #   guardava solo il NOME della chiamata: ### cosi' la regola NASCONDEVA i difetti cercati.
    #   ### (b) VALE SOLO SE SI ALLUNGA LA CODA lasciando intatti i primi `len(x)`, e la firma di
    #   quello e' che il ramo di scorta **rinomina la cache stessa** dentro l'estensione
    #   (`concatenate([x, ...])`, `vstack([x, ...])`).
    ALLUNGA = ("concatenate", "vstack", "hstack", "append", "pad", "resize")
    _usate = [e for e in ALLUNGA if ("." + e + "(") in r or (" " + e + "(") in r
              or r.startswith(e + "(")]
    _tiene_testa = _usate and (v["cosa"] in r or (v["cosa"].split(".")[-1] in r))
    if _tiene_testa:
        return "b", ("il ramo di scorta ALLUNGA LA CODA (%s) e RINOMINA la cache, quindi i primi "
                     "len(x) restano" % ", ".join(_usate))
    _sostituisce = [e for e in ("full", "zeros", "ones", "empty") if (e + "(") in r]
    if _sostituisce:
        return "d", ("DA LEGGERE -- **SOSTITUZIONE**: `%s(n, ...)` non allunga la coda, SCRIVE "
                     "TUTTA LA RETE" % _sostituisce[0])
    # ⚠⚠ (a) CORRETTA: la regola <<c'e' anche `not hasattr` / `is None`>> RIPETEVA L'ERRORE di
    #   `e3fda4b`. Una condizione che mette **la non-esistenza IN OR con la lunghezza** non e'
    #   un'inizializzazione: e' ### **DUE CASI DIVERSI IN UN SOLO RAMO** -- e il secondo e' il
    #   ricalcolo a meta' passo, cioe' il flash. ### VA SEPARATA, come in `lambda_nodi`.
    #   **Quindi (a) NON si assegna piu' a macchina:** si assegna LEGGENDO.
    if any(x in v["condizione"] for x in NONESISTE):
        return "d", ("DA LEGGERE -- **CONDIZIONE FUSA**: la non-esistenza (%s) sta IN OR con la "
                     "lunghezza. Due casi in un ramo: VA SEPARATA come in `lambda_nodi`"
                     % ", ".join(x for x in NONESISTE if x in v["condizione"]))
    return "d", "DA LEGGERE: nel perimetro della fisica, e il ramo di scorta NON allunga la coda"


def principale():
    conf = _confronti()
    leggi = [n for _t, n in _passo.ordine()]
    fasi = ["apri", "chiudi", "verifica_invarianti"]
    perimetro = raggiungibili(leggi + fasi)
    # ---- IL GIUNTO COL RUNTIME: e' MAI SCATTATO nei 72 passi della scena grande? ----
    #   Si legge il referto della sonda (`_ripieghi_len_n.json`), che ha girato sullo STESSO
    #   blob: quindi i numeri di riga combaciano. ### Senza questo, la tabella dice che un
    #   sito POTREBBE mordere e non dice se ha morso.
    RT = os.path.join(_QUI, "_ripieghi_len_n.json")
    scattate, blob_rt = None, None
    if os.path.isfile(RT):
        _d = json.load(io.open(RT, encoding="utf-8"))
        scattate = {(x["riga"], x["cosa"]) for x in _d.get("runtime_corte", [])}
        blob_rt = _d.get("passo_nascita")
    COPERTE.update(v["dentro"] for v in conf if v["op"] == "(guardia)")
    for v in conf:
        v["classe"], v["regola"] = classifica(v, perimetro)
        if scattate is None:
            v["scattato_72"] = None
        else:
            v["scattato_72"] = bool(any(k[0] == v["riga"] for k in scattate))
    conta = {}
    for v in conf:
        conta[v["classe"]] = conta.get(v["classe"], 0) + 1
    print("confronti trovati: %d, in %d funzioni"
          % (len(conf), len({v["dentro"] for v in conf})))
    print("perimetro della fisica (dalle cinque leggi e dalle fasi): %d funzioni" % len(perimetro))
    print("")
    for k, nome in (("a", "inizializzazione"), ("b", "estensione dei soli nuovi"),
                    ("c", "diagnostica o disegno, NON fisica"),
                    ("e", "GIA' CURATO: il ramo di scorta SOLLEVA"),
                    ("x", "FUORI DAL MANDATO (troncamento, oppure ==/!=)"),
                    ("d", "DA LEGGERE (candidati a sostituzione di legge)")):
        print("  (%s) %-46s %d" % (k, nome, conta.get(k, 0)))
    print("")
    # ⚠ RIGHE E SITI NON SONO LA STESSA COSA, e il guardiano l'ha chiesto sui SITI:
    #   `_nb_grav` compare DUE VOLTE in (e) -- la guardia e il confronto ormai ridondante --
    #   quindi le (e) sono 4 RIGHE ma 3 SITI. Si stampano entrambi i numeri.
    print("  %-4s %-8s %s" % ("cl.", "righe", "SITI DISTINTI (funzione)"))
    for k in ("a", "b", "c", "e", "x", "d"):
        q = [v for v in conf if v["classe"] == k]
        print("  (%s)  %-8d %d" % (k, len(q), len({v["dentro"] for v in q})))
    print("")
    print("  della famiglia CORTA (quella del mandato): %d su %d"
          % (sum(1 for v in conf if v["famiglia"] == "CORTA"), len(conf)))
    print("")
    print("=" * 108)
    print("I CANDIDATI (d): nel perimetro della fisica, e il ramo di scorta NON estende")
    print("=" * 108)
    for v in [x for x in conf if x["classe"] == "d"]:
        print("  :%-6d %-28s cosa=%-20s" % (v["riga"], v["dentro"], v["cosa"][:20]))
        print("      cond:  %s" % v["condizione"][:96])
        print("      scorta: %s" % v["ramo_di_scorta"].replace(NL, " ; ")[:96])
        print("")

    # ---- la TABELLA, generata: `L-NUMERI` ----------------------------------------------
    NOMI = {"a": "**(a)** inizializzazione", "b": "**(b)** estensione dei soli nuovi",
            "c": "**(c)** diagnostica o disegno", "d": "### **(d) DA LEGGERE**",
            "e": "**(e)** GIA' CURATO: il ramo di scorta SOLLEVA",
            "x": "*(fuori dal mandato: troncamento oppure ==/!=)*"}
    # ⚠ IL TITOLO SI GENERA DAL CONTO: la prima stesura diceva "100" a mano, e sono 99.
    R = ["# I %d CONFRONTI FRA UN `len(...)` E `n`, NELLE CLASSI" % len(conf), "",
         "> ### **Generato da** `csv/_test_fork/_classi_ripieghi.py`. **Non si modifica a mano:** si",
         "> rigira lo strumento. *(Punto ① di `RIPIEGHI-ZERO`.)*", "",
         "**Confronti: %d, in %d funzioni.** Perimetro della fisica *(raggiungibile dalle cinque"
         " leggi e dalle fasi del passo)*: **%d** funzioni."
         % (len(conf), len({v["dentro"] for v in conf}), len(perimetro)), "",
         "| classe | quanti |", "|---|---|"]
    for k in ("a", "b", "c", "e", "x", "d"):
        R.append("| %s | **%d** |" % (NOMI[k], conta.get(k, 0)))
    R += ["", "## ⚠ Che cosa e' automatico e che cosa non lo e'", "",
          "| classe | com'e' deciso |", "|---|---|",
          "| **(c)** | ### **OGGETTIVO**: il sito **non e' raggiungibile** in un passo, quindi"
          " **non puo' cambiare la fisica di quel passo** |",
          "| **(b)** | si legge **la forma** dell'istruzione: il ramo di scorta **estende** |",
          "| **(a)** | la condizione porta anche `is None` / `not hasattr` / `len(...) == 0` |",
          "| ### **(d)** | ### **NON assegnata dallo strumento: e' la lista di cio' che va LETTO"
          " a mano.** La classe piu' grave e' quella che lo strumento **rifiuta** di assegnare |",
          "", "## La tabella, sito per sito", "",
          "| riga | funzione | cache | fam. | classe | la regola, e la RIGA che la giustifica |",
          "|---|---|---|---|---|---|"]
    for v in conf:
        R.append("| `:%d` | `%s` | `%s` | %s | %s | %s <br> *(%s)* `%s` |"
                 % (v["riga"], v["dentro"], v["cosa"][:26], v["famiglia"],
                    NOMI[v["classe"]], v["regola"], v["dove_e_il_ramo"],
                    v["ramo_di_scorta"].replace(NL, " ; ").replace("|", chr(92) + "|")[:150]))
    R.append("")
    OUTMD = os.path.join(RADICE, "doc", "RIPIEGHI_classi.md")
    io.open(OUTMD, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    OUT = os.path.join(_QUI, "_classi_ripieghi.json")
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(json.dumps(
        {"confronti": conf, "conta": conta, "perimetro": sorted(perimetro),
         "funzioni_con_confronti": sorted({v["dentro"] for v in conf})},
        indent=1, ensure_ascii=False, sort_keys=True))
    print("scritto: " + OUTMD)
    print("scritto: " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
