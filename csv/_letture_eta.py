# -*- coding: utf-8 -*-
"""**OGNI LETTURA DI `eta`, PER AST** — la verifica che PRECEDE `RAMPA-1` strada (3).

> **DECISIONE DI LUCA, 2026-09-25 — `RAMPA-1`, strada (3): IL VUOTO DATO HA ETA' INFINITA.**
> I nodi della semina iniziale (`maturi=True`) ricevono **`eta = +inf`** invece di
> `eta = _tempo_rampa()`. **Nessun numero nuovo, nessun array nuovo.**
> `ramp = min(1, inf/tr) = 1` **per sempre, qualunque `cs`.** I nati in dinamica restano con
> `eta = 0` e la rampa del tempo-luce.

**PERCHE' QUESTA VERIFICA VIENE PRIMA:** `+inf` non e' un numero grande, e' un **valore
speciale**. `inf/inf = nan`, `inf - inf = nan`, una **media** che contiene `inf` vale `inf`, una
**mediana** puo' restare finita, un `np.sum` diventa `inf`, un istogramma si rompe.
**Quindi si cerca OGNI posto che legge `eta`, e si guarda cosa ci fa** -- e i posti si trovano
**per AST**, non con un `grep` (`STANDARD 9`): `grep eta` prende `_theta`, `beta`, `meta`,
`etichetta`.

**COSA SEGNALA, per ogni lettura:** se e' un accesso **nudo** (indicizzazione, confronto,
divisione) o se finisce in una **RIDUZIONE** (`mean`, `sum`, `std`, `median`, `percentile`,
`max`, `min`, `histogram`, `mean` di numpy o builtin). **Le riduzioni sono i punti che `inf`
rompe**, e vanno dichiarate una per una.

**IL GUARDIANO DI LUCA DICE: `eta` e' letta solo a `:3419` e `:3684`, piu' l'incremento a
`:4976`. Questo strumento lo VERIFICA invece di crederlo.**

ASCII puro. Sola lettura.
"""
import ast
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "LETTURE_eta.md")
NL = chr(10)

RIDUZIONI = ("mean", "sum", "std", "var", "median", "percentile", "quantile", "average",
             "histogram", "max", "min", "argmax", "argmin", "cumsum", "prod", "nanmean",
             "bincount", "sort", "any", "all", "count_nonzero")


class Trova(ast.NodeVisitor):
    """Ogni `X.eta` (Attribute) e ogni nome `eta`, col CONTESTO."""

    def __init__(self, righe):
        self.righe = righe
        self.hit = []

    def _ctx(self, nd):
        i = max(0, (nd.lineno or 1) - 1)
        return self.righe[i].strip() if i < len(self.righe) else ""

    def visit_Attribute(self, nd):
        if nd.attr == "eta":
            scrittura = isinstance(nd.ctx, (ast.Store, ast.AugStore))
            self.hit.append((nd.lineno, "scrittura" if scrittura else "lettura",
                             self._ctx(nd)))
        self.generic_visit(nd)

    def visit_Name(self, nd):
        if nd.id == "eta":
            scrittura = isinstance(nd.ctx, (ast.Store, ast.AugStore))
            self.hit.append((nd.lineno, "scrittura (nome)" if scrittura else "lettura (nome)",
                             self._ctx(nd)))
        self.generic_visit(nd)


def ruolo(riga):
    """La riga contiene una RIDUZIONE? (e' `inf` che la rompe)"""
    fuori = [r for r in RIDUZIONI if (r + "(") in riga]
    return fuori


def esamina(p):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    try:
        arb = ast.parse(t)
    except SyntaxError:
        return None
    v = Trova(t.split(NL))
    v.visit(arb)
    return v.hit


def sorgenti():
    fuori = [os.path.join(RADICE, "soliton_simulator.py")]
    for base, _dd, ff in os.walk(os.path.join(RADICE, "csv")):
        b = base.replace(chr(92), "/")
        if "/_tmp" in b or "/__pycache__" in b:
            continue
        for f in ff:
            if not f.endswith(".py"):
                continue
            if f.startswith("_old_sim_pre_") or f.endswith("._sim.py") or "_sim_vecchio" in f:
                continue
            fuori.append(os.path.join(base, f))
    return fuori


R = []


def P(s=""):
    R.append(s)


P("# OGNI LETTURA DI `eta`, **PER AST** — la verifica che precede `RAMPA-1`")
P()
P("*(`csv/_letture_eta.py`. Decisione di Luca, 2026-09-25: `RAMPA-1` strada (3), il vuoto dato")
P("ha **eta infinita**. Sola lettura: nessuna riga del simulatore cambia qui.)*")
P()
P("> **`+inf` non e' un numero grande, e' un VALORE SPECIALE.** `inf/inf = nan`,")
P("> `inf - inf = nan`, una **media** che lo contiene vale `inf`, un `sum` diventa `inf`.")
P("> **Quindi la domanda non e' «dove sta scritto `eta`»: e' «chi lo RIDUCE».**")
P()

# ---------------------------------------------------------------- il simulatore
sim = os.path.join(RADICE, "soliton_simulator.py")
hs = esamina(sim)
P("## ① IL SIMULATORE — `soliton_simulator.py`")
P()
P("| riga | cosa | codice | **riduzione?** |")
P("|---|---|---|---|")
rid_sim = []
for lin, tipo, riga in hs:
    rr = ruolo(riga)
    if rr:
        rid_sim.append((lin, riga, rr))
    P("| `:%d` | %s | `%s` | %s |"
      % (lin, tipo, riga.replace("|", "\\|")[:96],
         ("⚠ **%s**" % ", ".join(rr)) if rr else "—"))
P()
P("```")
P("occorrenze di `eta` nel simulatore   %d" % len(hs))
P("letture                              %d" % len([x for x in hs if x[1].startswith("lettura")]))
P("scritture                            %d" % len([x for x in hs if x[1].startswith("scrittura")]))
P("CON UNA RIDUZIONE sulla stessa riga  %d" % len(rid_sim))
P("```")
P()
P("### IL GUARDIANO DICEVA `:3419`, `:3684` e l'incremento a `:4976`")
P()
_att = {3419, 3684, 4976}
_vis = set(x[0] for x in hs)
P("```")
P("righe attese dal guardiano   %s" % sorted(_att))
P("righe TROVATE per AST        %s" % sorted(_vis))
P("attese e NON trovate         %s" % (sorted(_att - _vis) or "nessuna"))
P("trovate e NON attese         %s" % (sorted(_vis - _att) or "nessuna"))
P("```")
P()

# ---------------------------------------------------------------- gli strumenti
P("## ② GLI STRUMENTI DI `csv/`")
P()
P("| file | riga | codice | **riduzione?** |")
P("|---|---|---|---|")
tot, rid_tool = 0, 0
for p in sorgenti()[1:]:
    hh = esamina(p)
    if not hh:
        continue
    rel = os.path.relpath(p, RADICE).replace(chr(92), "/")
    for lin, tipo, riga in hh:
        tot += 1
        rr = ruolo(riga)
        if rr:
            rid_tool += 1
        P("| `%s` | `:%d` | `%s` | %s |"
          % (rel, lin, riga.replace("|", "\\|")[:80],
             ("⚠ **%s**" % ", ".join(rr)) if rr else "—"))
P()
P("```")
P("occorrenze negli strumenti           %d" % tot)
P("CON UNA RIDUZIONE sulla stessa riga  %d" % rid_tool)
P("```")
P()
P("## ③ IL VERDETTO")
P()
if not rid_sim:
    P("**NEL SIMULATORE NESSUNA LETTURA DI `eta` FINISCE IN UNA RIDUZIONE**: `+inf` non ha")
    P("niente da rompere nella FISICA.")
else:
    P("**⚠ NEL SIMULATORE ci sono %d letture di `eta` dentro una riduzione**, e ognuna va")
    P("guardata: `+inf` le cambia. Sono elencate nella tabella ① con la loro riga.")
P()
P("**NEGLI STRUMENTI le riduzioni sono %d**: non rompono la fisica, **rompono i REFERTI** --")
P("una `median(eta)` che diventa `inf` stampa `inf` invece di un numero, e un referto che")
P("stampa `inf` va **dichiarato**, non lasciato passare. *(E la stessa famiglia del `PASS`")
P("su `inf` gia' catalogata: un verdetto vacuo.)*")
P()
P("## COSA QUESTO ELENCO **NON** DICE")
P()
P("- **la riduzione si cerca SULLA STESSA RIGA.** Un `eta` messo in una variabile e ridotto")
P("  **tre righe dopo** NON viene visto. **E' il limite vero di questo strumento**, e si")
P("  dichiara invece di far sembrare l'elenco completo.")
P("- **non e' un presidio:** non impedisce a nessuno di scrivere domani una `mean(eta)`.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
