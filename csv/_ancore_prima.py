# -*- coding: utf-8 -*-
"""**OGNI CONFRONTO CHE PRENDE «IL CODICE DI PRIMA» DA `HEAD` DIVENTA VUOTO APPENA LA CURA E'
COMMITTATA.** (mandato di Luca, 2026-09-25, punto 3)

> ### Il difetto, misurato oggi su `A1` del sigillo di `CURA 4`:
> il braccio «prima» prendeva il codice precedente da **`HEAD:soliton_simulator.py`**. Era
> giusto **finche' la cura non era committata**; **dal commit in poi HEAD LA CONTIENE**, e il
> braccio «prima» e' diventato **il braccio OFF di se stesso**.
> **La prova non e' un argomento:** ancorato al blob giusto (`900fe603^`), quel braccio muore
> con `AttributeError: no attribute '_tempo_rampa'` -- un metodo **che la cura ha introdotto**.
> **Un braccio che non poteva nemmeno GIRARE sul codice vero stava passando da giorni.**

**⚠ E C'E' UN USO DI `HEAD` CHE E' LEGITTIMO, e confonderli sarebbe un allarme falso:**
confrontare il **proprio** blob con `HEAD` per verificare che il codice che gira **sia
committato** e' il presidio del **par.5-quinquies**, e va lasciato in pace. Il difetto e' **usare
`HEAD` come "il codice PRIMA della cura"**.

**COME LI DISTINGUE, e il limite e' dichiarato:** si guarda **dove finisce** il contenuto
estratto. Se va in una variabile o in un file il cui nome dice *vecchio / prima / old / pre*,
e' un **riferimento «prima»** -> **SCADE**. Se serve solo a un confronto di hash, e' una
**guardia** -> legittima. **E' un'EURISTICA SUL NOME:** non e' una dimostrazione, e i casi
incerti si stampano come **DA GUARDARE A MANO** invece di essere assolti.

ASCII puro. Sola lettura.
"""
# ESENTE-H-P5: strumento di analisi STATICA. Non importa il simulatore e non lo fa girare:
#   legge SORGENTI per AST. **Non esiste una «configurazione» in cui questa misura sia stata
#   presa**, quindi dichiararla sarebbe una riga vuota -- e `P5` esiste per impedire le
#   dichiarazioni vuote, non per aggiungerne una. *(Il presidio ha rifiutato per primo questo
#   file, il 2026-09-25, ed era il caso giusto da guardare: la differenza fra «misura del
#   sistema» e «lettura del codice» non la puo' fare un euristico su `DEST`.)*
import ast
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "ANCORE_prima_da_HEAD.md")
NL = chr(10)

# le spie di un'estrazione da git, e le spie del ruolo «codice di prima»
SPIE = ("HEAD:", "rev-parse HEAD", "cat-file", "git show")
NOMI_PRIMA = ("vecchi", "prima", "_old", "old_", "pre_", "_pre", "precedent", "senza_cura")
CURATO = "sim_prima_del_flag"


def sorgenti():
    fuori = []
    for base, _dd, ff in os.walk(os.path.join(RADICE, "csv")):
        b = base.replace(chr(92), "/")
        if "/_tmp" in b or "/__pycache__" in b:
            continue
        for f in ff:
            if not f.endswith(".py"):
                continue
            if f.startswith("_old_sim_pre_") or f.endswith("._sim.py") or "_sim_vecchio" in f:
                continue                      # COPIE del simulatore: non sono strumenti
            fuori.append(os.path.join(base, f))
    return sorted(fuori)


def esamina(p):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    try:
        arb = ast.parse(t)
    except SyntaxError:
        return [("NON ANALIZZABILE", 0, "SyntaxError", "")]
    curato = CURATO in t
    fuori = []
    for nd in ast.walk(arb):
        if not (isinstance(nd, ast.Constant) and isinstance(nd.value, str)):
            continue
        s = nd.value
        if not any(x in s for x in SPIE):
            continue
        # il RUOLO: si guarda la riga intera e le due dopo, dove finisce cio' che si estrae
        righe = t.split(NL)
        # ⚠ ANCHE INDIETRO (corretto il 2026-09-25): guardando solo in avanti questo
        #   strumento **sottocontava**, perche' `VECCHIO = ...` sta tipicamente **PRIMA**
        #   dell'estrazione. L'ha trovato il **collaudo** di `csv/_hook_presidi.py`, sul caso
        #   sintetico che DEVE bloccare (`P1-sexies`).
        i = max(0, (nd.lineno or 1) - 1)
        intorno = NL.join(righe[max(0, i - 3):i + 4]).lower()
        if any(x in intorno for x in NOMI_PRIMA):
            ruolo = "CURATO (ancorato al padre del commit)" if curato else "RIFERIMENTO «PRIMA»"
        elif "sha1" in intorno or "blob" in intorno or "hash" in intorno or "==" in intorno:
            ruolo = "guardia del par.5-quinquies"
        else:
            ruolo = "DA GUARDARE A MANO"
        fuori.append((ruolo, nd.lineno, s.strip()[:64], os.path.basename(p)))
    return fuori


R = []


def P(s=""):
    R.append(s)


tutti, conta = [], {}
for p in sorgenti():
    for ruolo, lin, s, f in esamina(p):
        rel = os.path.relpath(p, RADICE).replace(chr(92), "/")
        tutti.append((ruolo, rel, lin, s))
        conta[ruolo] = conta.get(ruolo, 0) + 1

ORD = ["RIFERIMENTO «PRIMA»", "DA GUARDARE A MANO", "CURATO (ancorato al padre del commit)",
       "guardia del par.5-quinquies", "NON ANALIZZABILE"]

P("# LE ANCORE «CODICE DI PRIMA» PRESE DA `HEAD` — **elenco generato**")
P()
P("*(`csv/_ancore_prima.py`. Mandato di Luca, 2026-09-25, punto 3. Sola lettura.)*")
P()
P("> ### UN CONFRONTO CONTRO `HEAD` DIVENTA VUOTO APPENA LA CURA E' COMMITTATA.")
P("> `A1` del sigillo di `CURA 4` lo ha fatto per giorni: il braccio «prima» era **il braccio")
P("> OFF di se stesso**, e ancorandolo al blob giusto (`900fe603^`) **non gira nemmeno**")
P("> (`AttributeError: no attribute '_tempo_rampa'`, un metodo che la cura ha introdotto).")
P(">")
P("> **E c'e' un uso LEGITTIMO di `HEAD`:** confrontare il PROPRIO blob per verificare che il")
P("> codice che gira sia committato (par.5-quinquies). **Quello si lascia in pace.**")
P()
P("```")
for k in ORD:
    if k in conta:
        P("%-42s %d" % (k, conta[k]))
P("%-42s %d" % ("TOTALE occorrenze", len(tutti)))
P("%-42s %d" % ("file di csv/ esaminati", len(sorgenti())))
P("```")
P()
for k in ORD:
    righe = [x for x in tutti if x[0] == k]
    if not righe:
        continue
    P("## %s — %d" % (k, len(righe)))
    P()
    P("| file | riga | stringa |")
    P("|---|---|---|")
    for _r, rel, lin, s in righe:
        P("| `%s` | %s | `%s` |" % (rel, lin, s.replace("|", "\\|")))
    P()

P("## LA CURA, E PERCHE' NON SI PINNA A MANO")
P()
P("`_cli_flag.sim_prima_del_flag(nome_flag, dest)` trova **il commit che ha INTRODOTTO il**")
P("**flag** (`git log -S`, la voce piu' vecchia), ne prende **il PADRE**, estrae in **BINARIO**")
P("(trappola CRLF, par.5-quinquies) e **ASSERISCE che il file estratto NON contenga il flag**.")
P("**Quell'assert e' il punto:** se l'ancora fosse sbagliata **si ferma invece di misurare")
P("niente** (`A9`).")
P()
P("## COSA QUESTO ELENCO **NON** E'")
P()
P("- **non e' un presidio** (`A9`): non impedisce di scrivere domani un altro confronto contro")
P("  `HEAD`. **Va fra i presidi automatici** come controllo del `pre-commit` — richiesta di")
P("  Luca nello stesso mandato, ed e' la voce **`P8 ANCORA «PRIMA» NON SCADUTA`**.")
P("- **la classificazione e' un'EURISTICA SUL NOME** della variabile/file vicino")
P("  all'estrazione. I casi incerti stanno sotto **DA GUARDARE A MANO**: non sono assolti.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
