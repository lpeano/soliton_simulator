# -*- coding: utf-8 -*-
"""**UN CAMBIO DI SOLI COMMENTI SI PROVA, NON SI ASSICURA.**

Il commit delle quattro note *(2026-10-03)* riscrive ### **cinque derivazioni** della
tabella di nascita: frasi che affermavano un ### **bilancio che nessuno ha misurato.**
Sono stringhe di documentazione, quindi ### **il blob cambia ma la fisica no** — e
questa e' ### **esattamente il genere di frase che in questo repo non si crede sulla
parola.**

## Perche' NON si rigira il sigillo, e perche' questo e' MEGLIO

Rigirare il sigillo esteso costa ### **venti minuti** e darebbe una ### **prova
EMPIRICA su una scena**. Questo confronto costa ### **secondi** e da' una prova
### **STRUTTURALE su TUTTO il file**: se gli alberi sintattici coincidono una volta
### **normalizzata la documentazione**, allora ### **nessuna istruzione e' cambiata** —
per qualunque scena, qualunque seme, qualunque flag.

### \U0001f4cc **E' la differenza fra <<non ho visto differenze dove ho guardato>> e
### <<non ci sono differenze>>.**

## CHE COSA SI NORMALIZZA, ed e' l'unica cosa che si puo' cambiare

| | |
|---|---|
| i **docstring** | il primo `Constant` di modulo, classe e funzione |
| gli **argomenti di DOCUMENTAZIONE** dei tre registratori | `_nascita_regola(evento, grandezza, ### classe, ancora, derivazione)` · `_nascita_collocata(evento, grandezza, ### chi, perche)` · `_nascita_non_si_tocca(evento, grandezza, ### perche)` |

### ⚠ **E GLI ARGOMENTI 0 e 1 NON SI NORMALIZZANO MAI:** sono ### **l'evento e la
grandezza**, cioe' ### **le CHIAVI della tabella.** Cambiarli cambierebbe quale regola
governa quale grandezza — e il caso ① del sigillo dei tre casi dimostra che il run si
ferma se una chiave sparisce. ### **Normalizzarli renderebbe questo confronto cieco
proprio al difetto piu' grave.**

### ⚠ **E i COMMENTI non si normalizzano: NON SONO NELL'AST.** Un `#` non produce
nessun nodo, quindi un cambio di commenti e' ### **invisibile per costruzione** a questo
confronto — ed e' la ragione per cui funziona.

**COMANDO:** `python csv/_seal_fork/_sigillo_inerzia_commenti.py --prima=<commit-o-blob>`
### **`--prima` e' OBBLIGATORIO**, e non ha un default di proposito: vedi dentro.
**USCITA:** `csv/_seal_fork/_sigillo_inerzia_commenti/`
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
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _cli_flag   # noqa: E402
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_sigillo_inerzia_commenti")
NL = chr(10)
# i tre registratori, e QUALI argomenti sono documentazione (gli altri sono CHIAVI).
REGISTRATORI = {"_nascita_regola": (2, 3, 4),
                "_nascita_collocata": (2, 3),
                "_nascita_non_si_tocca": (2,)}
SEGNAPOSTO = "<DOCUMENTAZIONE-NORMALIZZATA>"

# ### L'ANCORA: una frase della documentazione NUOVA, che nel <<prima>> NON c'e'.
#   E' il BERSAGLIO (la frase riscritta), non il modo in cui e' scritta -- la
#   lezione di `6ab31f7`, dove un'ancora nominava la FORMULA e si e' rotta appena
#   la formula e' cambiata.
ANCORA = "~1.2 giri persi per arco"


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def estrai(dest):
    """Il <<prima>> dal **PADRE del commit che introduce l'ancora**, via `_cli_flag`.

    ### E QUI `H-P8` HA RIFIUTATO DUE VOLTE, e la seconda aveva ragione sul MERITO.
    La prima stesura aveva `prima_ref = "HEAD^"` come default: tolto, ### nessun default.
    La seconda chiamava ### direttamente `git`, per estrarre un `ref` dato, e il
    presidio l'ha preso per la stringa `<estrazione-git>` con un *<<prima>>* a tre righe di
    distanza. ### **Il hook indica la cura nel suo stesso messaggio: <<passare dal CLI
    (`_cli_flag`), ancorare al PADRE del commit>>** — e non e' un adempimento:

    | | |
    |---|---|
    | un `ref` **passato a mano** | dice *<<confronta con QUESTO>>*, e chi lo passa puo' sbagliarlo |
    | ### l'**ANCORA** | dice *<<confronta col codice ### **PRIMA CHE QUESTA FRASE ESISTESSE**>>*, e lo trova `git log -S` |

    ### ✅ **E `sim_prima_del_flag` ASSERISCE che l'ancora NON sia nel file estratto**, che
    e' il presidio contro la vacuita' — lo stesso di `ANCORE-1`.
    """
    introduce = _cli_flag.sim_prima_del_flag(ANCORA, dest)
    return dest, introduce


class Normalizza(ast.NodeTransformer):
    """Toglie i docstring e sostituisce gli argomenti di DOCUMENTAZIONE col segnaposto."""

    def __init__(self):
        self.docstring_tolti = 0
        self.argomenti_normalizzati = 0
        self.chiavi = []

    def _senza_docstring(self, nodo):
        corpo = getattr(nodo, "body", None)
        if (corpo and isinstance(corpo[0], ast.Expr)
                and isinstance(corpo[0].value, ast.Constant)
                and isinstance(corpo[0].value.value, str)):
            self.docstring_tolti += 1
            nodo.body = corpo[1:] or [ast.Pass()]
        return nodo

    def visit_Module(self, n):
        self.generic_visit(n)
        return self._senza_docstring(n)

    def visit_ClassDef(self, n):
        self.generic_visit(n)
        return self._senza_docstring(n)

    def visit_FunctionDef(self, n):
        self.generic_visit(n)
        return self._senza_docstring(n)

    def visit_Call(self, n):
        self.generic_visit(n)
        nome = None
        if isinstance(n.func, ast.Name):
            nome = n.func.id
        if nome in REGISTRATORI:
            quali = REGISTRATORI[nome]
            chiave = []
            for k, arg in enumerate(n.args):
                if k < 2 and isinstance(arg, ast.Constant):
                    chiave.append(arg.value)
                if k in quali:
                    n.args[k] = ast.Constant(value=SEGNAPOSTO)
                    self.argomenti_normalizzati += 1
            if len(chiave) == 2:
                self.chiavi.append(tuple(chiave))
        return n


def impronta(percorso):
    t = ast.parse(io.open(percorso, encoding="utf-8").read())
    norm = Normalizza()
    t = norm.visit(t)
    ast.fix_missing_locations(t)
    return ast.dump(t, include_attributes=False), norm


def principale():
    for x in sys.argv[1:]:
        if x.startswith("--prima="):
            raise SystemExit("** `--prima` NON esiste piu', ed e' una cura di `H-P8`: il "
                             "<<prima>> si ANCORA alla frase nuova (`%s`) e si prende dal "
                             "PADRE del commit che la introduce, via `sim_prima_del_flag`. "
                             "Passare un ref a mano significa poterlo sbagliare. **" % ANCORA)
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        P.append(s)
        print(s)

    stampa("=" * 100)
    stampa("UN CAMBIO DI SOLI COMMENTI SI PROVA: gli ALBERI SINTATTICI, non una scena")
    stampa("=" * 100)
    dest = os.path.join(FUORI, "_sim_prima.py")
    dest, introduce = estrai(dest)
    prima_ref = "%s^ (il PADRE del commit che introduce l'ancora)" % introduce[:8]
    stampa("  l'ANCORA ...... %r" % ANCORA)
    stampa("  il <<prima>> .. dal PADRE di %s  ->  blob %s   (IN BINARIO)"
           % (introduce[:8], blob(dest)[:8]))
    stampa("      *(e `sim_prima_del_flag` ASSERISCE che l'ancora NON sia nel file estratto)*")
    stampa("  il <<dopo>> ... il disco           blob %s" % blob(SIM)[:8])
    stampa("")
    if blob(dest) == blob(SIM):
        stampa("  ### I DUE BLOB SONO UGUALI: non c'e' niente da provare, e lo dico invece di")
        stampa("      stampare un <<passa>> che non significherebbe nulla.")
        return 1

    a, na = impronta(dest)
    b, nb = impronta(SIM)
    stampa("  --- la NORMALIZZAZIONE, e si conta ---")
    stampa("      docstring tolti ............ prima %d   dopo %d"
           % (na.docstring_tolti, nb.docstring_tolti))
    stampa("      argomenti di doc. azzerati . prima %d   dopo %d"
           % (na.argomenti_normalizzati, nb.argomenti_normalizzati))
    stampa("      ### chiavi (evento, grandezza) .. prima %d   dopo %d"
           % (len(na.chiavi), len(nb.chiavi)))
    perse = sorted(set(na.chiavi) - set(nb.chiavi))
    nuove = sorted(set(nb.chiavi) - set(na.chiavi))
    stampa("      ### chiavi PERSE %s   chiavi NUOVE %s"
           % (perse or "nessuna", nuove or "nessuna"))
    stampa("      *(le chiavi NON si normalizzano: sono l'evento e la grandezza, cioe' QUALE")
    stampa("        regola governa QUALE grandezza. Normalizzarle renderebbe il confronto")
    stampa("        cieco proprio al difetto piu' grave.)*")
    stampa("")
    uguali = (a == b)
    stampa("  ### GLI ALBERI NORMALIZZATI COINCIDONO? %s" % ("SI" if uguali else "### NO"))
    dove = None
    if not uguali:
        # dove comincia a divergere, in caratteri del dump: e' grezzo ma INDICA il punto
        k = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        dove = {"carattere": k, "prima": a[max(0, k - 120):k + 160],
                "dopo": b[max(0, k - 120):k + 160]}
        stampa("      ### divergono al carattere %d del dump" % k)
        stampa("      PRIMA: ...%s..." % dove["prima"][-200:])
        stampa("      DOPO:  ...%s..." % dove["dopo"][-200:])
    passa = uguali and not perse and not nuove
    stampa("")
    stampa("=" * 100)
    if passa:
        stampa("### IL SIGILLO PASSA: NESSUNA ISTRUZIONE E' CAMBIATA.")
        stampa("###   I due file differiscono SOLO in commenti, docstring e stringhe di")
        stampa("###   DOCUMENTAZIONE della tabella di nascita. ### La fisica e' identica per")
        stampa("###   COSTRUZIONE -- per qualunque scena, qualunque seme, qualunque flag.")
        stampa("###   E le %d chiavi (evento, grandezza) sono le STESSE." % len(nb.chiavi))
    else:
        stampa("### IL SIGILLO FALLISCE: QUALCOSA OLTRE LA DOCUMENTAZIONE E' CAMBIATO.")
        stampa("###   Il commit NON e' <<di soli commenti>>, e dirlo sarebbe falso.")
    stampa("=" * 100)
    ref = {"passa": bool(passa), "prima_ref": prima_ref, "ancora": ANCORA,
           "commit_che_introduce_l_ancora": introduce,
           "blob_prima": blob(dest), "blob_dopo": blob(SIM),
           "blob_sigillo": blob(os.path.abspath(__file__)),
           "alberi_uguali": bool(uguali),
           "docstring_tolti": [na.docstring_tolti, nb.docstring_tolti],
           "argomenti_normalizzati": [na.argomenti_normalizzati, nb.argomenti_normalizzati],
           "chiavi": [len(na.chiavi), len(nb.chiavi)],
           "chiavi_perse": perse, "chiavi_nuove": nuove, "divergenza": dove,
           "registratori": {k: list(v) for k, v in REGISTRATORI.items()}}
    io.open(os.path.join(FUORI, "_sigillo_inerzia_commenti.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(ref, indent=1, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(principale())
