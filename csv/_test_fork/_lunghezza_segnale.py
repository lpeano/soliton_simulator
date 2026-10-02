# -*- coding: utf-8 -*-
"""**CHI USA LA LUNGHEZZA DI UN ARRAY COME SEGNALE DI <<NODO NUOVO>>?**

Rilievo di Luca *(2026-10-03, voce `LUNGHEZZA-COME-SEGNALE`)*: usare `len(x) < n`
come segnale di *<<c'e' un nodo nuovo>>* e' ### **una toppa implicita.** La forma
pulita e' una ### **REGOLA DI NASCITA esplicita.**

### ⚠ **E UNA PARTE DI QUESTA RICERCA NON E' RIMANDABILE AL COMMIT 5, ed e' il
motivo per cui questo strumento esiste PRIMA del commit 4:** il veleno ### **ESTENDE**
le derivate avvelenabili alla lunghezza giusta, quindi ### **ogni guardia che usa la
lunghezza come segnale CAMBIA COMPORTAMENTO.** I due siti `AUTO-RINFRESCO` sono esenti
per questo — ### **ma se ce ne fosse un TERZO su una derivata avvelenabile, il veleno
lo romperebbe senza che nessuno l'abbia previsto.**

### \U0001f4cc **Quindi la domanda di questo strumento e' una domanda sul COMMIT 4**, non
solo sulla coda: ### **esiste una guardia di lunghezza su una delle derivate che il
registro dichiara avvelenabili?**

## Che cosa cerca, e la forma e' dichiarata

Un confronto fra una ### **lunghezza** *(`len(...)` o `.shape[0]` o `.size`)* e
### **`self.n`** o ### **`len(self.<altra>)`**, dove uno dei due lati e' una grandezza
### **del registro**. Gli operatori che contano sono ### **`<`, `>`, `<=`, `>=`, `==`,
`!=`** — tutti, perche' un *<<segnale>>* puo' essere scritto in entrambi i versi.

**COMANDO:** `python csv/_test_fork/_lunghezza_segnale.py`
**USCITA:** `csv/_test_fork/_lunghezza_segnale/`
"""
import ast
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_lunghezza_segnale")
NL = chr(10)
OPERATORI = {ast.Lt: "<", ast.Gt: ">", ast.LtE: "<=", ast.GtE: ">=",
             ast.Eq: "==", ast.NotEq: "!="}


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def registri(albero):
    """Tutti i `REGISTRO_*` col loro contenuto, piu' le derivate con la loro CLASSE."""
    fuori, derivate = {}, []
    for n in ast.walk(albero):
        if not (isinstance(n, ast.Assign) and len(n.targets) == 1
                and isinstance(n.targets[0], ast.Name)
                and n.targets[0].id.startswith("REGISTRO")):
            continue
        nome = n.targets[0].id
        voci = []
        if isinstance(n.value, (ast.Tuple, ast.List)):
            for e in n.value.elts:
                if (isinstance(e, (ast.Tuple, ast.List)) and e.elts
                        and isinstance(e.elts[0], ast.Constant)):
                    campi = [c.value if isinstance(c, ast.Constant) else None
                             for c in e.elts]
                    voci.append(campi)
        fuori[nome] = [v[0] for v in voci]
        if nome == "REGISTRO_DERIVATE":
            derivate = voci
    return fuori, derivate


def _grandezza_di(nodo, tutte):
    """Il nodo e' una LUNGHEZZA di una grandezza del registro? Restituisce il nome."""
    # `len(self.x)` / `len(x)` dove x e' un attributo
    if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
            and nodo.func.id == "len" and nodo.args):
        a = nodo.args[0]
        if (isinstance(a, ast.Attribute) and isinstance(a.value, ast.Name)
                and a.value.id in ("self", "net") and a.attr in tutte):
            return a.attr, "len"
        if isinstance(a, ast.Name):
            return "<locale:%s>" % a.id, "len"
    # `self.x.shape[0]` / `self.x.size`
    if isinstance(nodo, ast.Subscript) and isinstance(nodo.value, ast.Attribute):
        b = nodo.value
        if (b.attr == "shape" and isinstance(b.value, ast.Attribute)
                and isinstance(b.value.value, ast.Name)
                and b.value.value.id in ("self", "net") and b.value.attr in tutte):
            return b.value.attr, "shape[0]"
    if (isinstance(nodo, ast.Attribute) and nodo.attr == "size"
            and isinstance(nodo.value, ast.Attribute)
            and isinstance(nodo.value.value, ast.Name)
            and nodo.value.value.id in ("self", "net") and nodo.value.attr in tutte):
        return nodo.value.attr, "size"
    return None, None


def _e_un_conteggio(nodo, tutte):
    """Il nodo e' `self.n`, una lunghezza, o un intero: cioe' un CONTEGGIO."""
    if (isinstance(nodo, ast.Attribute) and isinstance(nodo.value, ast.Name)
            and nodo.value.id in ("self", "net") and nodo.attr in ("n", "m")):
        return "self.%s" % nodo.attr
    g, come = _grandezza_di(nodo, tutte)
    if g:
        return "%s(%s)" % (come, g)
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, int):
        return str(nodo.value)
    if isinstance(nodo, ast.Name):
        return "<locale:%s>" % nodo.id
    return None


def cerca(albero, tutte):
    """I confronti di lunghezza, con funzione, riga, grandezza e operatore."""
    trovati = []

    def scendi(nodo, funzione):
        for figlio in ast.iter_child_nodes(nodo):
            f2 = figlio.name if isinstance(figlio, ast.FunctionDef) else funzione
            if isinstance(figlio, ast.Compare) and len(figlio.ops) == 1:
                op = OPERATORI.get(type(figlio.ops[0]))
                if op:
                    sx, csx = _grandezza_di(figlio.left, tutte)
                    dx, cdx = _grandezza_di(figlio.comparators[0], tutte)
                    altro_sx = _e_un_conteggio(figlio.comparators[0], tutte)
                    altro_dx = _e_un_conteggio(figlio.left, tutte)
                    if sx and not sx.startswith("<locale") and altro_sx:
                        trovati.append({"grandezza": sx, "come": csx, "operatore": op,
                                        "contro": altro_sx, "funzione": f2,
                                        "riga": figlio.lineno,
                                        "codice": ast.unparse(figlio)[:110]})
                    elif dx and not dx.startswith("<locale") and altro_dx:
                        trovati.append({"grandezza": dx, "come": cdx, "operatore": op,
                                        "contro": altro_dx, "funzione": f2,
                                        "riga": figlio.lineno,
                                        "codice": ast.unparse(figlio)[:110]})
            scendi(figlio, f2)

    scendi(albero, "<modulo>")
    visti, puliti = set(), []
    for x in trovati:
        k = (x["grandezza"], x["funzione"], x["riga"])
        if k in visti:
            continue
        visti.add(k)
        puliti.append(x)
    return sorted(puliti, key=lambda x: x["riga"])


def principale():
    righe = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        righe.append(s)
        print(s)

    src = io.open(SIM, encoding="utf-8").read()
    albero = ast.parse(src)
    regs, derivate = registri(albero)
    tutte = sorted({x for v in regs.values() for x in v})
    nomi_der = [d[0] for d in derivate]
    # la CLASSE di nascita, se il registro ce l'ha (dal commit 4 in poi)
    classe = {}
    for d in derivate:
        classe[d[0]] = d[2] if len(d) >= 4 and isinstance(d[2], str) else None

    stampa("=" * 104)
    stampa("CHI USA LA LUNGHEZZA DI UN ARRAY COME SEGNALE DI <<NODO NUOVO>>?")
    stampa("=" * 104)
    stampa("  simulatore .. %s (sha1 byte grezzi)" % blob(SIM)[:8])
    stampa("  grandezze dei registri: %d   derivate: %d" % (len(tutte), len(nomi_der)))
    if any(classe.values()):
        stampa("  ### il registro DICHIARA la classe di nascita delle derivate:")
        for k in nomi_der:
            stampa("      %-18s %s" % (k, classe[k]))
    else:
        stampa("  ### il registro NON dichiara ancora la classe di nascita (pre-commit 4)")
    stampa("")
    stampa("  ### CHE COSA CERCA, e la forma e' DICHIARATA: un confronto fra una LUNGHEZZA")
    stampa("      (`len(...)`, `.shape[0]`, `.size`) di una grandezza DEL REGISTRO e un")
    stampa("      CONTEGGIO (`self.n`, un'altra lunghezza, un intero). Gli operatori sono")
    stampa("      tutti e sei (`<`,`>`,`<=`,`>=`,`==`,`!=`): un <<segnale>> si puo' scrivere")
    stampa("      in entrambi i versi, e cercarne uno solo sarebbe un FALSO-ZERO.")
    stampa("")

    trovati = cerca(albero, tutte)
    stampa("-" * 104)
    stampa("### TROVATI: %d confronti di lunghezza su grandezze del registro" % len(trovati))
    stampa("")
    sulle_derivate = [x for x in trovati if x["grandezza"] in nomi_der]
    stampa("### E LA DOMANDA CHE RIGUARDA IL COMMIT 4: quanti sono su una DERIVATA? %d"
           % len(sulle_derivate))
    for x in sulle_derivate:
        cl = classe.get(x["grandezza"])
        marca = ("ESENTE (auto-rinfresco)" if cl == "auto-rinfresco"
                 else "### AVVELENABILE" if cl == "avvelena"
                 else "classe non dichiarata")
        stampa("    %-18s `%s` :%-6d %-24s  %s"
               % (x["grandezza"], x["funzione"], x["riga"], marca, x["codice"][:60]))
    pericolosi = [x for x in sulle_derivate if classe.get(x["grandezza"]) == "avvelena"]
    non_dich = [x for x in sulle_derivate if classe.get(x["grandezza"]) is None]
    stampa("")
    if pericolosi:
        stampa("### ⛔ %d GUARDIE DI LUNGHEZZA SU DERIVATE AVVELENABILI: il veleno le"
               % len(pericolosi))
        stampa("###   CAMBIEREBBE, e vanno decise PRIMA del commit 4.")
    elif non_dich:
        stampa("### %d guardie su derivate la cui CLASSE NON E' ANCORA DICHIARATA (pre-commit 4):"
               % len(non_dich))
        stampa("###   sono proprio quelle che la classe deve coprire.")
    else:
        stampa("### ✅ NESSUNA guardia di lunghezza su una derivata AVVELENABILE:")
        stampa("###   il veleno non puo' cambiare il comportamento di una guardia che non c'e'.")
    stampa("")
    stampa("-" * 104)
    stampa("E LE ALTRE, sulle grandezze NON derivate: %d -- sono la coda di `LUNGHEZZA-COME-SEGNALE`"
           % (len(trovati) - len(sulle_derivate)))
    for x in trovati:
        if x["grandezza"] in nomi_der:
            continue
        stampa("    %-18s `%s` :%-6d %s %s   %s"
               % (x["grandezza"], x["funzione"], x["riga"], x["come"], x["operatore"],
                  x["contro"]))
    stampa("=" * 104)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    esito = {"blob_sim_sha1_byte": blob(SIM), "derivate": nomi_der,
             "classe_dichiarata": classe, "totale": len(trovati),
             "sulle_derivate": sulle_derivate, "pericolosi": pericolosi,
             "classe_non_dichiarata": non_dich,
             "sulle_altre": [x for x in trovati if x["grandezza"] not in nomi_der]}
    io.open(os.path.join(FUORI, "_lunghezza_segnale.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(righe) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
