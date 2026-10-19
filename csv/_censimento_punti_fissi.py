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

### **dal `2026-10-19`: `2` nel percorso del tick e `3` nel nucleo, e i previsti per
nome.** ### **Se ne trova meno, lo strumento e' cieco su uno che SO che c'e'; se ne trova
di piu', c'e' un punto fisso che non conosco** -- ed ESCE con errore invece di stampare un numero bello.

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

# ### ⛔⛔ **LA PREVISIONE, DICHIARATA PRIMA DELLA CORSA** *(`2026-10-19`, annotazione del
# ### task history `2026-10-19_rimozione_punto_medio.md`)*: col ramo del punto medio per
# ### pezzo ### **TOLTO dal passo**, nel percorso del tick restano ### **`2`** punti fissi,
# ### e nel nucleo ### **`3`** *(piu' il punto medio implicito della via di `H`)*.
# ### ⚠ **La previsione di prima** *(`3` nel tick, col peso al punto medio)* ### **e' quella
# ### del referto `censimento_punti_fissi.txt` a `95c81e97`, che resta valido al suo
# ### commit.**
PREVISTI = (
    ("primo_ordine/tick.py", "cs_al_centro"),
    ("primo_ordine/energia_pesata.py", "applica"),
)
PREVISTI_NUCLEO = PREVISTI + (("primo_ordine/passo.py", "mezzo_implicito"),)

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
# ### ⛔⛔ **IL CICLO ESTERNO NON EREDITA L'USCITA DI QUELLO INTERNO** *(integrazione
# ### del guardiano, `2026-10-19`)*: un ciclo che ### **contiene** un punto fisso e'
# ### ### **UN** punto fisso, non due. ### **Deve dare `1`.**
_SINTETICO_ANNIDATO = '''
def molti_passi(x, n):
    for t in range(n):
        for giri in range(1, GIRI_MAX + 1):
            nuovo = f(x)
            if abs(nuovo - x) <= EPS * abs(nuovo):
                break
            x = nuovo
    return x
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


_CHIUDONO = (ast.For, ast.While, ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
             ast.ClassDef)


def _propri(ciclo):
    """### I nodi del CORPO del ciclo, ### **senza scendere in un ciclo o in una funzione
    annidati.**

    ### ⛔⛔ **UN `if` APPARTIENE AL CICLO PIU' INTERNO CHE LO CONTIENE** *(integrazione
    del guardiano, `2026-10-19`)*: la versione di `82b92eba` camminava ### **tutto**
    l'albero del ciclo, e un ciclo esterno ### **ereditava l'uscita di quello interno** --
    e' per questo che `passo.strati` era contato ### **due volte** *(righe `109` e `111`)*.
    ### ⚠ **E l'`else` del ciclo non e' il corpo:** gira ### **dopo** l'ultimo giro, quindi
    un suo `if` non ferma l'iterazione.
    """
    coda = list(ciclo.body)
    while coda:
        n = coda.pop()
        yield n
        if isinstance(n, _CHIUDONO):
            continue
        coda.extend(ast.iter_child_nodes(n))


def _esce_su_confronto(ciclo):
    """### Il primo `if` con test di CONFRONTO che contiene `break`/`return`, o `None`."""
    for n in _propri(ciclo):
        if not isinstance(n, ast.If):
            continue
        confronto = any(isinstance(t, ast.Compare)
                        and any(isinstance(o, ORDINE_OP) for o in t.ops)
                        for t in ast.walk(n.test))
        if not confronto:
            continue
        # ### ⚠ **E il `break` deve essere DEL CICLO:** un `break` dentro un ciclo
        # ### annidato nell'`if` esce da quello. Il `return` invece esce da tutto.
        if _esce(n.body, True):
            return n
    return None


def _esce(corpo, break_vale):
    """### C'e' un'uscita DAL CICLO in `corpo`? ### **`break` solo fuori dai cicli
    annidati, `return` solo fuori dalle funzioni annidate.**"""
    for s in corpo:
        if isinstance(s, ast.Break) and break_vale:
            return True
        if isinstance(s, ast.Return):
            return True
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
                          ast.ClassDef)):
            continue
        dentro = break_vale and not isinstance(s, (ast.For, ast.While))
        figli = [x for x in ast.iter_child_nodes(s) if isinstance(x, ast.stmt)]
        if _esce(figli, dentro):
            return True
    return False


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


# ### ⛔⛔ **IL PERCORSO DEL TICK DELLA CAMMINATA: le sue radici** *(integrazione del
# ### guardiano, `2026-10-19`)*. `tick.py` percorre l-ordine, e i pezzi sono
# ### ### **operatori del motore** -- che `tick.py` riceve e ### **non importa**: per
# ### questo le radici sono ### **DUE.** ### ⚠ **La colonna si DERIVA dagli import**,
# ### non si scrive a mano.
RADICI_TICK = ("tick", "motore")


def chiusura_import(radici):
    """### I moduli raggiunti dagli import di `radici`, ### **dalla mappa del codice.**

    ### ⚠ **LEGGE LA STESSA MAPPA di `_rami_era2.nucleo`** *(`primo_ordine/_mappa.yaml`,
    che `P-MOD` tiene allineata al codice)*, con radici ### **diverse**: quella funzione
    ha le radici scritte dentro, e questo censimento non la tocca.
    """
    import yaml
    mappa = yaml.safe_load(io.open(os.path.join(RADICE, "primo_ordine", "_mappa.yaml"),
                                   encoding="utf-8").read())
    per = {r["nome"][:-3]: list(r.get("importa") or [])
           for r in mappa["moduli"] if str(r["nome"]).endswith(".py")}
    visti, coda = set(), list(radici)
    while coda:
        x = coda.pop()
        if x in visti:
            continue
        visti.add(x)
        coda.extend(y for y in per.get(x, []) if y not in visti)
    # ### ⛔⛔ **SOLO I FILE CHE ESISTONO SOTTO `primo_ordine/`** *(cura del
    # ### `2026-10-19`)*: la mappa elenca anche `_presidio`, che vive in `csv/` ed e- ### **il
    # ### timbro del blob, non fisica** -- e la versione di `6dbc6a3f` lo contava,
    # ### stampando ### **`10` file invece di `9`.** E- lo stesso filtro di
    # ### `_rami_era2.nucleo`, che ### **avrei dovuto copiare con la lettura.**
    return set(rel for rel in ("primo_ordine/%s.py" % x for x in visti)
               if os.path.exists(os.path.join(RADICE, rel)))


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
    print("### I TRE CONTROLLI SUL CODICE SINTETICO")
    si = len(punti_fissi(_SINTETICO_SI, "<si>"))
    an = len(punti_fissi(_SINTETICO_ANNIDATO, "<annidato>"))
    no = len(punti_fissi(_SINTETICO_NO, "<no>"))
    print("     deve essere contato                     %d   %s"
          % (si, "PASSA" if si == 1 else "### FALLISCE"))
    print("     un punto fisso dentro un ciclo: 1, NON 2 %d   %s"
          % (an, "PASSA" if an == 1 else "### FALLISCE"))
    print("     NON deve essere contato (e una ricerca) %d   %s"
          % (no, "PASSA" if no == 0 else "### FALLISCE"))
    if si != 1 or an != 1 or no != 0:
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
    percorso = chiusura_import(RADICI_TICK)
    print("     %-34s %-22s %-6s %-18s %-16s %s"
          % ("file", "funzione", "riga", "tolleranza", "tetto dei giri",
             "nel percorso del tick"))
    nel_tick = 0
    for rel, fn, riga, toll, tetto in trovati:
        dentro = rel in percorso
        nel_tick += 1 if dentro else 0
        print("     %-34s %-22s %-6d %-18s %-16s %s"
              % (rel, fn, riga, ",".join(toll) or "-", ",".join(tetto) or "-",
                 "si" if dentro else "no"))
    print("     ### il percorso del tick = la chiusura degli import di %s: %d file"
          % (" e ".join(RADICI_TICK), len(percorso)))
    print("     ### NEL PERCORSO DEL TICK: %d punti fissi su %d" % (nel_tick,
                                                                   len(trovati)))
    print("     ### ⚠ <<nel percorso>> vuol dire RAGGIUNGIBILE dagli import, non ACCESO:")
    print("     ###   un ramo spento e' nel percorso. Acceso o spento: il passo `B`.")
    print("-" * 100)
    chiavi = set((r[0], r[1]) for r in trovati)
    mancano = [p for p in PREVISTI_NUCLEO if p not in chiavi]
    nuovi = sorted(k for k in chiavi if k not in PREVISTI_NUCLEO)
    print("### IL CASO CHE DEVE RIUSCIRE (la previsione del 2026-10-19): %d nel percorso"
          " del tick, %d nel nucleo, e i previsti per nome"
          % (len(PREVISTI), len(PREVISTI_NUCLEO)))
    for p in PREVISTI_NUCLEO:
        print("     %-34s %-22s %s" % (p[0], p[1], "trovato" if p in chiavi
                                         else "### MANCA"))
    print("     e quelli NON previsti: %s" % (", ".join("%s:%s" % k for k in nuovi)
                                              or "nessuno"))
    print("     nel percorso del tick: %d (previsti %d)   nel nucleo: %d (previsti %d)"
          % (nel_tick, len(PREVISTI), len(trovati), len(PREVISTI_NUCLEO)))
    ok = (not mancano and not nuovi and nel_tick == len(PREVISTI)
          and len(trovati) == len(PREVISTI_NUCLEO))
    print("     %s" % ("PASSA" if ok else
                       "### FALLISCE: lo strumento e' cieco su uno che so che c'e'"))
    print("-" * 100)
    print("### ⚠ QUESTO E' IL CENSIMENTO STATICO: dice DOVE sono, non se GIRANO ne'")
    print("###   quanto COSTANO. Acceso o spento, giri e quota: il passo `B`.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
