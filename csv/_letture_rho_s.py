# -*- coding: utf-8 -*-
"""**OGNI LETTURA DI `rho_s` / `_rho_sorgente`** — la verifica che PRECEDE la cura `INERZIA-1(C)`.

> **DECISIONE DI LUCA, 2026-09-25 — `INERZIA-1`: cura (C), LOCALE.**
> *Dentro `_contrasto` (e **solo** lì) `rho_s` si normalizza **per vicino**, come `_peq_nodo` è
> già una media. **`rho_s` NON cambia altrove:** la cura tocca **l'inerzia**, non **il campo**.*

**LA DOMANDA CHE QUESTO STRUMENTO DEVE CHIUDERE, e l'ha posta Luca:**
*«tutte le letture di `rho_s` / `_rho_sorgente`, per confermare che la normalizzazione non esce
da `_contrasto`».*

**⚠ E CERCA ANCHE LE STRINGHE, non solo attributi e nomi.** Il 2026-09-25 l'audit di `eta`
(`csv/_letture_eta.py`) **ha mancato una lettura** perché `verifica_invarianti` legge le
grandezze come **CHIAVI DI TABELLA**, cioè stringhe: `'eta': ('nonneg', ...)`. **L'invariante ha
fermato la cura al primo giro**, e il difetto non era suo, era del mio audit.
> ### **In un codice guidato da tabelle, un audit su chi LEGGE una grandezza deve cercare anche
> ### le stringhe.** Qui si fa, e il conto delle due famiglie è stampato separato.

**COSA SEGNALA, per ogni lettura:** la funzione in cui sta, e se è **DENTRO `_passo_spinoriale`**
*(dove vive `_contrasto`)* oppure **FUORI** — perché è esattamente la distinzione che la cura
locale richiede: una lettura fuori **non deve vedere** la normalizzazione.

ASCII puro. Sola lettura: nessuna riga del simulatore cambia qui.
"""
# ESENTE-P5: strumento di analisi STATICA. Non importa il simulatore e non lo fa girare:
#   legge UN SORGENTE per AST. **Non esiste una «configurazione» in cui questa lettura sia
#   stata presa** -- le letture di `rho_s` nel file sono le stesse con qualunque flag -- quindi
#   dichiararla sarebbe **una riga vuota**, e `P5` esiste per impedire le dichiarazioni vuote.
#   *(Stessa esenzione, e stesso motivo, di `csv/_ancore_prima.py`.)*
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
DEST = os.path.join(RADICE, "doc", "LETTURE_rho_s.md")
NL = chr(10)

NOMI = ("rho_s", "_rho_s", "_rho_sorgente", "rho_spin")


class Visita(ast.NodeVisitor):
    """Attributi, nomi E stringhe. La terza famiglia e' quella che l'audit di `eta` ha mancato."""

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

    def _dove(self):
        return self.pila[-1] if self.pila else "<modulo>"

    def visit_Attribute(self, nd):
        if nd.attr in NOMI:
            self.hit.append(("attributo", nd.attr, nd.lineno, self._dove(), self._riga(nd),
                             isinstance(nd.ctx, ast.Store)))
        self.generic_visit(nd)

    def visit_Name(self, nd):
        if nd.id in NOMI:
            self.hit.append(("nome", nd.id, nd.lineno, self._dove(), self._riga(nd),
                             isinstance(nd.ctx, ast.Store)))
        self.generic_visit(nd)

    def visit_Constant(self, nd):
        if isinstance(nd.value, str) and nd.value in NOMI:
            self.hit.append(("STRINGA", nd.value, nd.lineno, self._dove(), self._riga(nd), False))
        self.generic_visit(nd)


t = io.open(SIM, encoding="utf-8").read()
v = Visita(t.split(NL))
v.visit(ast.parse(t))

R = []


def P(s=""):
    R.append(s)


P("# OGNI LETTURA DI `rho_s` / `_rho_sorgente` — la verifica che precede `INERZIA-1(C)`")
P()
P("*(`csv/_letture_rho_s.py`, per **AST**, **stringhe incluse**. Decisione di Luca, 2026-09-25:")
P("cura **(C) LOCALE** — `rho_s` si normalizza per vicino **dentro `_contrasto` e solo lì**.")
P("Sola lettura.)*")
P()
P("> ### LA DOMANDA: **la normalizzazione esce da `_contrasto`?**")
P("> Se una lettura di `rho_s` **fuori** da `_passo_spinoriale` vedesse il valore normalizzato,")
P("> la cura non sarebbe locale e toccherebbe **il campo** invece dell'**inerzia**.")
P()
scritture = [h for h in v.hit if h[5]]
letture = [h for h in v.hit if not h[5]]
dentro = [h for h in letture if h[3] == "_passo_spinoriale"]
fuori = [h for h in letture if h[3] != "_passo_spinoriale"]
stringhe = [h for h in v.hit if h[0] == "STRINGA"]
P("```")
P("occorrenze totali                      %d" % len(v.hit))
P("  letture                              %d" % len(letture))
P("  scritture                            %d" % len(scritture))
P("  di cui trovate come STRINGA          %d   <- la famiglia che l'audit di `eta` mancava"
  % len(stringhe))
P("letture DENTRO `_passo_spinoriale`     %d" % len(dentro))
P("letture FUORI                          %d" % len(fuori))
P("```")
P()
for titolo, gruppo in (("LETTURE **DENTRO** `_passo_spinoriale` — dove vive `_contrasto`", dentro),
                       ("LETTURE **FUORI** — **queste NON devono vedere la normalizzazione**",
                        fuori),
                       ("SCRITTURE", scritture)):
    P("## %s — %d" % (titolo, len(gruppo)))
    P()
    if not gruppo:
        P("*(nessuna)*")
        P()
        continue
    P("| funzione | riga | come | nome | codice |")
    P("|---|---|---|---|---|")
    for tipo, nome, lin, fn, riga, _st in gruppo:
        P("| `%s` | `:%d` | %s | `%s` | `%s` |"
          % (fn, lin, tipo, nome, riga.replace("|", "\\|")[:76]))
    P()

per_fn = {}
for _t, _n, _l, fn, _r, _s in v.hit:
    per_fn.setdefault(fn, 0)
    per_fn[fn] += 1
P("## RAGGRUPPATO PER FUNZIONE")
P()
P("```")
for fn in sorted(per_fn, key=lambda x: -per_fn[x]):
    P("%-32s %d" % (fn, per_fn[fn]))
P("```")
P()
P("## IL VERDETTO SULLA LOCALITA' DELLA CURA")
P()
P("La cura e' LOCALE **se e solo se** la normalizzazione si applica a una variabile che vive")
P("**dentro** `_passo_spinoriale` e **non** al valore restituito da `_rho_sorgente()`.")
P("**Il punto della cura e' `_contrasto`**: `_rho_s / max(_cn, 1)` invece di `_rho_s`, con")
P("**lo STESSO `_cn`** che `_peq_nodo` usa gia' come denominatore. **Nessuna grandezza nuova**")
P("(`STANDARD 10`), e `_rho_s` **resta quello che era** per ogni altra riga del file.")
P()
P("**COSA GUARDARE NELLA TABELLA «FUORI»:** ogni riga li' e' una legge che legge il campo del")
P("nodo e **che la cura NON deve toccare**. Se dopo la cura una di quelle cambia, la cura non")
P("e' locale — e il sigillo lo misura con la byte-identita' a flag spento.")
P()
P("## COSA QUESTO ELENCO **NON** DICE")
P()
P("- **non dice che le letture FUORI siano equivalenti fra loro:** alcune usano `rho_spin`")
P("  direttamente, altre passano da `_rho_sorgente()`. La tabella distingue **come**, non")
P("  **quanto pesa** ciascuna.")
P("- **la riduzione non si cerca qui:** questo audit risponde a *«chi legge»*, non a *«chi")
P("  riduce»*. Per `eta` la domanda era l'altra, e le due non si sostituiscono.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
