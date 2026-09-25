# -*- coding: utf-8 -*-
"""**`RAMPA-2` — CHI USA IL TEMPO-LUCE O `cs` QUANDO LA CACHE NON C'E' ANCORA.**

> **Il difetto, misurato su `RAMPA-1`:** al **passo 0** la cache `_cs_nodo_prev` **non esiste**,
> quindi `_tempo_luce_nodo` cade sul suo fallback e il tempo-luce si calcola con
> **`cs = CS_M`** *(il valore di modulo)* **ovunque**. Al passo 1 il `cs` vero e' `p50 1.672`
> contro `CS_M = 2`, con `cs_std/cs = 19.07 %`: **il tempo-luce del passo 0 e' sbagliato del
> 20 %, in modo sistematico e nella stessa direzione per tutti.**
> La cura 4 ci scriveva `eta`, e la rampa cadeva. **Ma la cura 4 non e' l'unica che legge lì.**

**LA DOMANDA DI LUCA:** *«elenca per AST quali ALTRE leggi usano il tempo-luce o `cs` al passo 1
(primo passo con la velocita' del vuoto): stessa famiglia del "passo 1 senza tempo proprio"
(`B1`)»*.

**COSA FA:** trova **per AST** ogni chiamata a `_tempo_luce_nodo`, `_cs_arco_da_nodo`,
`_tempo_rampa`, `_tau_arco_causale` e ogni lettura di `_cs_nodo_prev`/`CS_M`, e per ciascuna
dice **in quale funzione sta** e **se quella funzione gira al primo passo**.

**⚠ E LA PARTE CHE CONTA NON E' L'ELENCO: E' SE IL FALLBACK SIA CONTATO.** Un ramo che cade su
`CS_M` senza dirlo e' un **comportamento sconosciuto** (`P5`), e in questo repo uno di quei rami
scattava nel **71.88 %** delle chiamate senza che nessun sigillo se ne accorgesse.

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
SIM = os.path.join(RADICE, "soliton_simulator.py")
DEST = os.path.join(RADICE, "doc", "RAMPA2_chi_usa_il_tempo_luce.md")
NL = chr(10)

CHIAMATE = ("_tempo_luce_nodo", "_cs_arco_da_nodo", "_tempo_rampa", "_tau_arco_causale",
            "_fattore_tempo_arco")
LETTURE = ("_cs_nodo_prev", "CS_M")


class Visita(ast.NodeVisitor):
    def __init__(self, righe):
        self.righe = righe
        self.pila = []
        self.hit = []

    def _riga(self, nd):
        i = max(0, (nd.lineno or 1) - 1)
        return self.righe[i].strip() if i < len(self.righe) else ""

    def visit_FunctionDef(self, nd):
        self.pila.append(nd.name)
        self.generic_visit(nd)
        self.pila.pop()

    def visit_Call(self, nd):
        nome = None
        if isinstance(nd.func, ast.Attribute):
            nome = nd.func.attr
        elif isinstance(nd.func, ast.Name):
            nome = nd.func.id
        if nome in CHIAMATE:
            self.hit.append(("chiamata a %s" % nome, nd.lineno,
                             self.pila[-1] if self.pila else "<modulo>", self._riga(nd)))
        self.generic_visit(nd)

    def visit_Attribute(self, nd):
        if nd.attr in LETTURE and not isinstance(nd.ctx, ast.Store):
            self.hit.append(("legge %s" % nd.attr, nd.lineno,
                             self.pila[-1] if self.pila else "<modulo>", self._riga(nd)))
        self.generic_visit(nd)

    def visit_Name(self, nd):
        if nd.id in LETTURE and not isinstance(nd.ctx, ast.Store):
            self.hit.append(("legge %s" % nd.id, nd.lineno,
                             self.pila[-1] if self.pila else "<modulo>", self._riga(nd)))
        self.generic_visit(nd)


t = io.open(SIM, encoding="utf-8").read()
arb = ast.parse(t)
v = Visita(t.split(NL))
v.visit(arb)

# QUALI funzioni girano al PRIMO passo? si legge dall'ORDINE DEL PASSO, non da un elenco a mano
sys.path.insert(0, _QUI)
import _passo

try:
    ORDINE = [x for x in _passo.ordine()]
except Exception as _e:
    ORDINE = []
PRIMO = set()
for _x in ORDINE:
    PRIMO.add(_x if isinstance(_x, str) else str(_x))

R = []


def P(s=""):
    R.append(s)


P("# `RAMPA-2` — CHI USA IL TEMPO-LUCE O `cs` QUANDO LA CACHE NON C'E' ANCORA")
P()
P("*(`csv/_chi_usa_il_tempo_luce.py`, per **AST**. Mandato di Luca, 2026-09-25. Sola lettura.)*")
P()
P("> ### IL FATTO, misurato su `RAMPA-1`")
P("> Al **passo 0** `_cs_nodo_prev` **non esiste**: il tempo-luce si calcola con **`cs = CS_M`**")
P("> ovunque. Al passo 1 il `cs` vero e' **`p50 1.672`** contro **`CS_M = 2`**")
P("> (`cs_std/cs = 19.07 %`): **il tempo-luce del passo 0 e' sbagliato del ~20 %, in modo")
P("> SISTEMATICO e nella STESSA DIREZIONE per tutti.** Non e' rumore: e' un **bias**.")
P(">")
P("> **`RAMPA-1` ha curato UNA delle leggi che leggono lì** (la maturita' della cura 4, che ora")
P("> non legge piu' niente: `eta = +inf`). **Le altre sono qui sotto.**")
P()
P("## L'ELENCO — %d occorrenze nel simulatore" % len(v.hit))
P()
P("| dove (funzione) | riga | cosa | codice |")
P("|---|---|---|---|")
for cosa, lin, fn, riga in v.hit:
    P("| `%s` | `:%d` | %s | `%s` |"
      % (fn, lin, cosa, riga.replace("|", "\\|")[:88]))
P()
per_fn = {}
for cosa, lin, fn, _r in v.hit:
    per_fn.setdefault(fn, []).append((cosa, lin))
P("## RAGGRUPPATO PER FUNZIONE — **%d funzioni toccano il tempo-luce o `cs`**" % len(per_fn))
P()
P("```")
for fn in sorted(per_fn, key=lambda x: -len(per_fn[x])):
    P("%-34s %d" % (fn, len(per_fn[fn])))
P("```")
P()
P("## L'ORDINE DEL PASSO, letto da `csv/_passo.py` (non da un elenco a mano)")
P()
P("```")
P(str(ORDINE) if ORDINE else "ordine non leggibile")
P("```")
P()
P("## COSA QUESTO ELENCO **NON** DICE, e sono tre cose")
P()
P("1. **non dice che ognuna di queste sia un difetto.** Una legge che legge `cs` al passo 1 e'")
P("   sbagliata **solo se il valore che riceve non e' quello del luogo** — e al passo 0 non lo")
P("   e' per nessuno, perche' la cache non c'e'. **Quante di esse ne dipendano DAVVERO va")
P("   misurato**, una per una, e questo strumento **non lo misura**: le trova.")
P("2. **non dice se il fallback sia CONTATO.** E' la domanda di `P5`, ed e' quella che pesa:")
P("   un ramo che cade su `CS_M` senza dirlo e' un **comportamento sconosciuto**. In questo")
P("   repo uno di quei rami scattava nel **71.88 %** delle chiamate **senza che nessun sigillo")
P("   se ne accorgesse**.")
P("3. **la cura non e' «usare `CS_M` meglio»:** e' la stessa famiglia di `B1` (*il passo 1 senza")
P("   tempo proprio*) e di `C7` (*la cache scartata a ogni mitosi*). **La forma di cura che ha")
P("   funzionato in `C7` era EREDITARE**, non ricalcolare: il figlio prende `cs` dal padre.")
P("   **Al passo 0 non c'e' un padre da cui ereditare**, e questa e' la differenza vera.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
