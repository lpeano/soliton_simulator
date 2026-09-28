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
            # l'`if` (o l'`IfExp`, o il `while`) che CONTIENE il confronto: e' li' che sta il
            # ramo di scorta. Si risale finche' non si trova un nodo di controllo.
            su, cond, ramo = nd, None, None
            for _ in range(8):
                su = padre.get(su)
                if su is None:
                    break
                if isinstance(su, (ast.If, ast.While)):
                    cond = ast.unparse(su.test)
                    corpo = su.body if nd.lineno <= (su.body[0].lineno if su.body else 0) or True \
                        else su.orelse
                    ramo = NL.join(ast.unparse(x) for x in corpo)[:220]
                    break
                if isinstance(su, ast.IfExp):
                    cond = ast.unparse(su.test)
                    ramo = "(espressione condizionale) " + ast.unparse(su.orelse)[:180]
                    break
                if isinstance(su, ast.BoolOp):
                    continue
            fuori.append({"riga": nd.lineno, "dentro": _fn_di(nd.lineno), "cosa": ta,
                          "contro": tb, "op": type(nd.ops[0]).__name__,
                          "condizione": (cond or "")[:200],
                          "ramo_di_scorta": (ramo or "(non trovato)"),
                          "sorgente": RIG[nd.lineno - 1].strip()[:150]})
            break
    return sorted(fuori, key=lambda x: x["riga"])


def classifica(v, perimetro):
    """La classe, e **la regola che l'ha decisa**. `(d)` non si assegna: si SEGNALA."""
    if v["dentro"] not in perimetro:
        return "c", "NON raggiungibile dalle cinque leggi ne' dalle fasi del passo"
    r = v["ramo_di_scorta"]
    if any(("." + e + "(") in r or (" " + e + "(") in r or r.startswith(e + "(")
           for e in ESTENDE):
        return "b", "il ramo di scorta ESTENDE (%s)" % ", ".join(
            e for e in ESTENDE if ("." + e + "(") in r or (" " + e + "(") in r
            or r.startswith(e + "("))
    if any(x in v["condizione"] for x in NONESISTE):
        return "a", "la condizione porta anche <<non esiste ancora>> (%s)" % ", ".join(
            x for x in NONESISTE if x in v["condizione"])
    return "d", "DA LEGGERE: nel perimetro della fisica, e il ramo di scorta NON estende"


def principale():
    conf = _confronti()
    leggi = [n for _t, n in _passo.ordine()]
    fasi = ["apri", "chiudi", "verifica_invarianti"]
    perimetro = raggiungibili(leggi + fasi)
    for v in conf:
        v["classe"], v["regola"] = classifica(v, perimetro)
    conta = {}
    for v in conf:
        conta[v["classe"]] = conta.get(v["classe"], 0) + 1
    print("confronti trovati: %d, in %d funzioni"
          % (len(conf), len({v["dentro"] for v in conf})))
    print("perimetro della fisica (dalle cinque leggi e dalle fasi): %d funzioni" % len(perimetro))
    print("")
    for k, nome in (("a", "inizializzazione"), ("b", "estensione dei soli nuovi"),
                    ("c", "diagnostica o disegno, NON fisica"),
                    ("d", "DA LEGGERE (candidati a sostituzione di legge)")):
        print("  (%s) %-46s %d" % (k, nome, conta.get(k, 0)))
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
            "c": "**(c)** diagnostica o disegno", "d": "### **(d) DA LEGGERE**"}
    R = ["# I 100 CONFRONTI `len(x) < n`, NELLE QUATTRO CLASSI", "",
         "> ### **Generato da** `csv/_test_fork/_classi_ripieghi.py`. **Non si modifica a mano:** si",
         "> rigira lo strumento. *(Punto ① di `RIPIEGHI-ZERO`.)*", "",
         "**Confronti: %d, in %d funzioni.** Perimetro della fisica *(raggiungibile dalle cinque"
         " leggi e dalle fasi del passo)*: **%d** funzioni."
         % (len(conf), len({v["dentro"] for v in conf}), len(perimetro)), "",
         "| classe | quanti |", "|---|---|"]
    for k, nome in (("a", "inizializzazione"), ("b", "estensione dei soli nuovi"),
                    ("c", "diagnostica o disegno, NON fisica"),
                    ("d", "DA LEGGERE")):
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
          "| riga | funzione | cache | classe | la regola, e la RIGA che la giustifica |",
          "|---|---|---|---|---|"]
    for v in conf:
        R.append("| `:%d` | `%s` | `%s` | %s | %s <br> `%s` |"
                 % (v["riga"], v["dentro"], v["cosa"][:26], NOMI[v["classe"]],
                    v["regola"],
                    v["ramo_di_scorta"].replace(NL, " ; ").replace("|", "\\|")[:150]))
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
