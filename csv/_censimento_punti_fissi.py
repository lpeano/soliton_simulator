# -*- coding: utf-8 -*-
r"""**I PUNTI FISSI DEL PASSO, CONTATI** — *il passo `A` del task history della memoria.*

> ### ⛔ **PERCHE' ESISTE** *(`2026-10-19`)*: il mandato della memoria chiede
> ### **un censimento di TUTTI i punti fissi e le iterazioni implicite** che il passo ha
> oggi, ### **contato con uno script** e non elencato a mano. La previsione del task
> history `2026-10-18_memoria_e_punti_fissi.md` e' ### **`3`**: `cs` al centro, la fase
> del vuoto a punto medio implicito, i pesi al punto medio *(spenti)*.

## ⭐ CHE COSA CONTA, E LA DEFINIZIONE E' SCRITTA PRIMA

### ✅ **UN PUNTO FISSO E' un ciclo (`for` o `while`) che contiene un `if` il cui test
e' un CONFRONTO DI ORDINE (`<`, `<=`, `>`, `>=`), e dentro quell'`if` un `break` o un
`return`** -- cioe' ### **un ciclo che si ferma quando qualcosa converge**, non quando
ha finito di contare ### **ne' quando ha TROVATO qualcosa** *(la cura di `bde7a07a`: la
prima versione accettava ogni `Compare`, e contava `passo.strati`)*.
### 📌 Per ognuno riporta ### **file, funzione, riga**, i ### **nomi** che compaiono nel
confronto *(la tolleranza)* e quelli del `range` *(il tetto dei giri)*.

## ⛔ E IL PERIMETRO E' IL NUCLEO, NON UNA LISTA MIA

### **Il nucleo e' la chiusura degli import dalle radici** *(`csv/_rami_era2.nucleo`)*:
un punto fisso fuori dal nucleo ### **non e' nel passo.**

## ⭐ I DUE CONTROLLI, sul codice SINTETICO, prima di guardare il nucleo

### ✅ **DEVE ESSERE CONTATO:** un ciclo con tetto e uscita su tolleranza.
### ⛔ **NON DEVE ESSERE CONTATO:** un ciclo che somma e basta, un ciclo con un `if`
che fa `continue` *(e' il ramo del nodo isolato di `_somma_per_nodo`)*, e ### **una
RICERCA** che esce con `break` su un `not in` *(e' `passo.strati`)*.
### **Se uno dei due sbaglia, lo strumento e' rotto e il numero non vale niente.**

## ⛔ E IL CASO CHE DEVE RIUSCIRE SUL NUCLEO

### **`>= 3`, e i tre previsti per nome.** ### **Se ne trova meno, lo strumento e' cieco
su uno che SO che c'e'** -- ed ESCE con errore invece di stampare un numero bello.

Gira con:  python csv/_censimento_punti_fissi.py
"""
import ast
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
RADICE = os.path.dirname(_QUI)

# ### ⛔ **I TRE PREVISTI dal task history**, PRIMA della misura: `(file, funzione)`.
PREVISTI = (
    ("primo_ordine/tick.py", "cs_al_centro"),
    ("primo_ordine/energia_pesata.py", "applica"),
    ("primo_ordine/flussi_parziali.py", "hop_phi_punto_medio"),
)

_SINTETICO_SI = '''
def risolvi(x):
    for giri in range(1, GIRI_MAX + 1):
        nuovo = f(x)
        if abs(nuovo - x) <= EPS * abs(nuovo):
            return nuovo
        x = nuovo
'''
_SINTETICO_NO = '''
def somma(v):
    t = 0
    for k in range(len(v)):
        if v[k] == 0:
            continue
        t += v[k]
    return t


def strato_libero(occupati, a, b):
    for s in range(len(occupati)):
        if a not in occupati[s] and b not in occupati[s]:
            break
    return s
'''
# ### ⛔⛔ **LA RICERCA NEL CONTROLLO NEGATIVO** *(`2026-10-19`, cura di `bde7a07a`)*:
# ### la prima versione contava ### **`passo.strati`** *(la colorazione golosa degli
# ### archi)*, perche- `a not in occupati[s]` ### **per l-AST e- un `Compare`.** Un ciclo
# ### che si ferma quando ### **TROVA** qualcosa non e- un ciclo che si ferma quando
# ### qualcosa ### **CONVERGE**: `strato_libero` qui sopra ### **e- quel caso**, e deve
# ### risultare ### **non contato.**
# ### ✅ **IL CONFRONTO DI CONVERGENZA E- DI ORDINE:** uno scarto ### **sotto** una
# ### tolleranza. `==`, `!=`, `in`, `is` ### **non lo sono.**
ORDINE_OP = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)


def _nomi(nodo):
    """### I nomi (`Name` e `Attribute`) dentro un nodo, ### **in ordine.**"""
    fuori = []
    for n in ast.walk(nodo):
        if isinstance(n, ast.Name):
            fuori.append(n.id)
        elif isinstance(n, ast.Attribute):
            fuori.append(n.attr)
    return fuori


def _esce_su_confronto(ciclo):
    """### Il primo `if` con test di CONFRONTO che contiene `break`/`return`, o `None`."""
    for n in ast.walk(ciclo):
        if n is ciclo or not isinstance(n, ast.If):
            continue
        confronto = any(isinstance(t, ast.Compare)
                        and any(isinstance(o, ORDINE_OP) for o in t.ops)
                        for t in ast.walk(n.test))
        if not confronto:
            continue
        if any(isinstance(b, (ast.Break, ast.Return))
               for s in n.body for b in ast.walk(s)):
            return n
    return None


def punti_fissi(sorgente, rel):
    """### `[(rel, funzione, riga, tolleranza, tetto)]` ### **per un sorgente.**"""
    arb = ast.parse(sorgente)
    fuori = []
    for f in ast.walk(arb):
        if not isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for c in ast.walk(f):
            if not isinstance(c, (ast.For, ast.While)):
                continue
            uscita = _esce_su_confronto(c)
            if uscita is None:
                continue
            toll = sorted(set(x for x in _nomi(uscita.test)
                              if x.upper() == x and len(x) > 1))
            tetto = sorted(set(x for x in _nomi(c.iter if isinstance(c, ast.For)
                                                 else c.test)
                               if x.upper() == x and len(x) > 1))
            fuori.append((rel, f.name, c.lineno, toll, tetto))
    # ### ⚠ **una funzione annidata vede il ciclo DUE volte** (dalla esterna e dalla
    # ### sua): si conta ### **la piu' interna**, cioe' una riga una volta sola.
    per_riga = {}
    for r in fuori:
        per_riga[(r[0], r[2])] = r
    return sorted(per_riga.values(), key=lambda r: (r[0], r[2]))


def cicli_tutti(sorgente):
    """### Quanti cicli ci sono in tutto, ### **per dire quanti NON sono punti fissi.**"""
    return sum(1 for n in ast.walk(ast.parse(sorgente))
               if isinstance(n, (ast.For, ast.While)))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _rami_era2 as R
    print("=" * 100)
    print("I PUNTI FISSI DEL PASSO, CONTATI CON L'AST -- il passo `A` della memoria")
    print("=" * 100)
    print("  la definizione: un ciclo con un `if` di CONFRONTO DI ORDINE che contiene"
          " `break`/`return`")
    print("-" * 100)
    print("### I DUE CONTROLLI SUL CODICE SINTETICO")
    si = len(punti_fissi(_SINTETICO_SI, "<si>"))
    no = len(punti_fissi(_SINTETICO_NO, "<no>"))
    print("     deve essere contato      %d   %s" % (si, "PASSA" if si == 1 else
                                                     "### FALLISCE"))
    print("     NON deve essere contato  %d   %s" % (no, "PASSA" if no == 0 else
                                                     "### FALLISCE"))
    if si != 1 or no != 0:
        print("### ⛔ LO STRUMENTO E' ROTTO: il numero sul nucleo NON si stampa.")
        return 1
    nucleo = R.nucleo()
    print("-" * 100)
    print("### IL NUCLEO (chiusura degli import dalle radici %s): %d file"
          % (" ".join(R.RADICI), len(nucleo)))
    trovati, cicli = [], 0
    for rel in nucleo:
        src = io.open(os.path.join(RADICE, rel), encoding="utf-8").read()
        cicli += cicli_tutti(src)
        trovati += punti_fissi(src, rel)
    print("-" * 100)
    print("### I PUNTI FISSI TROVATI, e sono %d (su %d cicli del nucleo):"
          % (len(trovati), cicli))
    print("     %-34s %-22s %-6s %-30s %s"
          % ("file", "funzione", "riga", "tolleranza", "tetto dei giri"))
    for rel, fn, riga, toll, tetto in trovati:
        print("     %-34s %-22s %-6d %-30s %s"
              % (rel, fn, riga, ",".join(toll) or "-", ",".join(tetto) or "-"))
    print("-" * 100)
    chiavi = set((r[0], r[1]) for r in trovati)
    mancano = [p for p in PREVISTI if p not in chiavi]
    nuovi = sorted(k for k in chiavi if k not in PREVISTI)
    print("### IL CASO CHE DEVE RIUSCIRE: >= %d, e i %d previsti per nome"
          % (len(PREVISTI), len(PREVISTI)))
    for p in PREVISTI:
        print("     %-34s %-22s %s" % (p[0], p[1], "trovato" if p in chiavi
                                         else "### MANCA"))
    print("     e quelli NON previsti: %s" % (", ".join("%s:%s" % k for k in nuovi)
                                              or "nessuno"))
    ok = len(trovati) >= len(PREVISTI) and not mancano
    print("     %s" % ("PASSA" if ok else
                       "### FALLISCE: lo strumento e' cieco su uno che so che c'e'"))
    print("-" * 100)
    print("### ⚠ QUESTO E' IL CENSIMENTO STATICO: dice DOVE sono, non se GIRANO ne'")
    print("###   quanto COSTANO. Acceso o spento, giri e quota: il passo `B`.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
