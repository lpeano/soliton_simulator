# -*- coding: utf-8 -*-
"""REPERTO: il sigillo E4-LAM fallisce 4/5, e i due difetti sono MIEI."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

N = 0


def s1(t, v, nu):
    global N
    assert t.count(v) == 1, "occ=%d per %r" % (t.count(v), v[:70])
    N += 1
    return t.replace(v, nu)


# ---------------------------------------------------------------- RAMIFICAZIONI
P = "doc/RAMIFICAZIONI.md"
t = io.open(P, encoding="utf-8", newline="").read()
A = "\n| **Z136** \U0001f7e9`CHIUSA PER DIMOSTRAZIONE`"
i0 = t.index(A)
riga = t[i0:t.index("\n", i0 + 1)]
Z = ("\n| **Z142** \U0001f7e5`REPERTO, DIFETTI MIEI` ⏳`[archivi delle cure · SIGILLO FALLITO]` | "
     "**IL SIGILLO DI `E4-LAM` FALLISCE `4/5`, E I DUE DIFETTI SONO MIEI: un CRITERIO che cerca "
     "nel TESTO invece che nel CODICE, e una CHIAVE DUPLICATA nei `DOMINI` perche' avevo "
     "concluso un'assenza da una ricerca PARZIALE** (2026-09-24, "
     "`csv/_seal_fork/_sig_e4lam/REFERTO.txt`) | "
     "**IL CODICE DELLA CURA E' GIUSTO:** `T2` `PASS` *(`cs` e' un invariante)*, `T3` `PASS` "
     "*(un arco sotto `LAM` a flag SPENTI **ferma il run**, col messaggio "
     "`̀d̀ VIOLA ̀>= LAM (= 0.800000) -- LEGGE, non opzionè`, gli INDICI e l'ARCO)*, `T4` `PASS` "
     "*(con `d >= LAM` non si ferma — il controllo che rende `T3` leggibile)*, **`T5` `PASS`: "
     "`206` campi identici, `0` diversi** contro `_cura1_corto`. **E dall'AST i riferimenti di "
     "CODICE a `_lam_attivo` sono `[]`: ZERO.** | "
     "**❌ DIFETTO MIO N.1 — `T1` E' UN CRITERIO SCRITTO MALE.** Cercava `\"_lam_attivo\" not in "
     "sorg`, cioe' **nel TESTO**: e trova le sue **DUE occorrenze nei MIEI COMMENTI** "
     "*(`:3666` e `:3715`, dove SPIEGO che il gate e' stato tolto)*. **Il codice è corretto, il "
     "criterio no.** E' esattamente il presidio *«un criterio di sigillo si scrive DA UNA "
     "MISURA, non dal proprio modello mentale del codice»*: la misura giusta e' **l'AST**, non "
     "un `in`. **Un `FAIL` falso costa piu' di un sigillo mancante, perche' si porta dietro una "
     "diagnosi.** | "
     "**❌ DIFETTO MIO N.2 — `_cs_nodo_prev` ERA GIA' NEI `DOMINI`, e io ne ho aggiunta una "
     "SECONDA copia.** Sta a **`:257`** *(`'velocita delle onde metriche: una VELOCITA e "
     "positiva'`)*, e la mia e' a **`:226`**. **In un letterale di dict la chiave duplicata "
     "vince l'ULTIMA**, quindi la mia e' **CODICE MORTO** — e `T2` lo ha mostrato stampando una "
     "descrizione **che non e' la mia**. **`cs > 0` era gia' un invariante: la mia "
     "affermazione «si aggiunge» era falsa.** | "
     "**PERCHE' NON L'HO VISTO, ed è la parte da non rifare:** avevo cercato con "
     "`sed -n '213,240p' | grep cs`, e la voce sta a **`:257`, FUORI da quella finestra**. "
     "**Ho concluso un'ASSENZA da una ricerca PARZIALE.** E' `P1`: *prima di proporre, "
     "rileggere dal disco cio' che e' gia' stabilito* — **e una finestra di 28 righe non e' "
     "«il disco».** *(La cura resta buona: la duplicazione era inerte, quindi `T5` è "
     "byte-identico comunque. Ma una chiave duplicata è un difetto, e va togliata.)* |")
t = s1(t, riga, riga + Z)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- RELAZIONE
P = "RELAZIONE_PER_CLAUDE.md"
t = io.open(P, encoding="utf-8", newline="").read()
REL = u"""
### ㉧ **REPERTO: il sigillo di `E4-LAM` fallisce `4/5`, e i due difetti sono MIEI**

> **Committo il fallimento prima di correggerlo**, come par.5 e il tuo mandato chiedono.
> `csv/_seal_fork/_sig_e4lam/REFERTO.txt`.

### ✅ **Il codice della cura è giusto, e i test che contano passano**

| | | |
|---|---|---|
| `T3` | **un arco sotto `LAM` a flag SPENTI FERMA IL RUN** | **PASS** |
| `T4` | e con `d ≥ LAM` **non** si ferma *(il controllo che rende `T3` leggibile)* | **PASS** |
| `T5` | **byte-inerte: `206` campi identici, `0` diversi** contro `_cura1_corto` | **PASS** |

**Il messaggio della legge esce così, ed è quello che volevi:**

```
[INVARIANTE] `d` VIOLA `>= LAM (= 0.800000) -- LEGGE, non opzione` al passo 1
  indici (primi 8): 1     valori: 4.000000e-01     arco=1-2
```

**E dall'AST i riferimenti di CODICE a `_lam_attivo` sono `[]`: zero.**

### ❌ **Difetto mio n.1: `T1` è un criterio scritto male**

Cercava **`"_lam_attivo" not in sorg`**, cioè **nel TESTO** — e trova le sue **due occorrenze
nei MIEI COMMENTI** (`:3666`, `:3715`), dove **spiego** che il gate è stato tolto.

> **Il codice è corretto. Il criterio no.** È esattamente il presidio *«un criterio di sigillo
> si scrive DA UNA MISURA, non dal proprio modello mentale del codice»*: la misura giusta è
> **l'AST**, non un `in`. **E un `FAIL` falso costa più di un sigillo mancante, perché si porta
> dietro una diagnosi.**

### ❌ **Difetto mio n.2: `_cs_nodo_prev` ERA GIÀ nei `DOMINI`**

Sta a **`:257`**, e la mia copia è a **`:226`**. **In un letterale di dict la chiave duplicata
vince l'ULTIMA**, quindi **la mia è codice morto** — e **`T2` lo ha mostrato** stampando una
descrizione **che non è la mia**.

**Quindi la mia affermazione «`cs > 0` si aggiunge ai `DOMINI`» era FALSA: c'era già.**

**E perché non l'ho visto, che è la parte da non rifare:** avevo cercato con
`sed -n '213,240p' | grep cs`, e la voce sta a **`:257`, fuori da quella finestra**.
**Ho concluso un'ASSENZA da una ricerca PARZIALE.** È `P1`, e **una finestra di 28 righe non è
«il disco».**

> **La cura resta buona** — la duplicazione era inerte, e `T5` è byte-identico comunque.
> **Ma una chiave duplicata è un difetto e va tolta**, e la derivazione che `cs > 0` è un
> invariante resta valida: **era già stata fatta da qualcun altro prima di me.**

### **Cosa faccio ora**

**Mi fermo qui col commit del reperto**, poi: togliere la chiave duplicata, riscrivere `T1`
sull'**AST**, e rigirare. **Nessuna delle due è una modifica alla cura.**
"""
assert "il sigillo di `E4-LAM` fallisce" not in t
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + "\n" + REL)
N += 1
print("%d sostituzioni. Z142 e relazione." % N)
