# -*- coding: utf-8 -*-
"""Le due precisazioni del guardiano su e11602d, nella scheda 9."""
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


P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()

# ---------------------------------------------------------------- (1) cs_arco: UNA funzione
A = u"""### ✅ **E DUE CLAMP SPARISCONO PER COSTRUZIONE** *(`A11`)*"""
B = u"""### ⚠ **PRECISAZIONE 1 del guardiano: `cs_arco` NON È DISPONIBILE in `mitosi()`**

**È una LOCALE di `step()`** (`:4774`), **non un attributo.** Quindi `tau_arco = d/cs_arco` va
**ricostruito** dentro `mitosi()` da **`self._cs_nodo_prev`** — che è **classe `A8b`**, la stessa
di `_cs_nodo_prev` quando era **stale al `71.88 %`**.

**TRE conseguenze, tutte obbligatorie:**

#### ① **UNA SOLA FORMULA, non due copie**

Si **estrae una funzione** per la media armonica d'arco, e la chiamano **entrambi**: `step()`
(`:4774`) **e** `mitosi()`.

```
_cs_arco_da_nodo(cs_nodo, i, j)  =  2·cs_i·cs_j / max(cs_i + cs_j, 1e-12)
```

**È lo stesso argomento del docstring di `_tempo_luce_nodo`:** *«UNICO punto del file in cui
questa relazione è scritta … duplicarla avrebbe significato avere **due leggi che possono
divergere**»*. **Due copie della media armonica sarebbero due leggi.**

#### ② **LA GUARDIA SU `_cs_nodo_prev` SI CONTA** *(`A8`, quattro numeri)*

invocazioni · salti · **la forma** al fallimento *(le due lunghezze; `-1` = assente)* ·
**quando** *(l'indice dell'ultima saltata)*.

**Il fallback è `CS_M`**, e **non è una convenzione nuova**: è esattamente ciò che `step()` fa
già a `:4778` quando `CS_DINAMICO` è spento — `cs_arco = np.full(len(i), CS_M)`.

#### ③ **IL SIGILLO DEVE PROVARE CHE L'ESTRAZIONE NON CAMBIA `step()`**

**A flag SPENTO, `step()` deve restare byte-identico dopo l'estrazione della funzione.**
È la stessa prova che l'estrazione di `_tempo_luce_nodo` ha dovuto dare *(«senza cambiarne una
virgola»)*, e **non è ovvia**: un'estrazione può cambiare l'ordine delle operazioni in
virgola mobile.

### ✅ **E DUE CLAMP SPARISCONO PER COSTRUZIONE** *(`A11`)*"""
t = s1(t, A, B)

# ---------------------------------------------------------------- (2) rep: il doppio conteggio
A2 = u"""## 5. ❓ **L'UNICA DECISIONE CHE NON PRENDO: `rep`, il ramo REPULSIVO**"""
i0 = t.index(A2)
i1 = t.index(u"## 6. LA TABELLA DELLE UNITÀ")
NUOVO5 = u"""## 5. ✅ **PRECISAZIONE 2 del guardiano: SÌ, È UN DOPPIO CONTEGGIO. LO CORREGGO.**

**La domanda:** con la cura, il ritmo `dt_e/DT` entrerebbe **due volte** nel ramo repulsivo —
nel **bersaglio** `rep` *(via `ampiezza`)* e nella **velocità del rilassamento** *(via `dt_e`
nell'esponente)*.

### **LA RAGIONE, in una riga, e dice CORREGGI**

> **Un'INTENSITÀ D'EQUILIBRIO non può dipendere dalla DURATA del passo: se dipendesse, la
> stessa condizione fisica darebbe un equilibrio diverso a seconda di quanto batte l'orologio
> locale. Una PROBABILITÀ PER PASSO, invece, DEVE dipenderne.**

**`rep` è il BERSAGLIO di un rilassamento**, cioè il valore verso cui `_rep` tende: è un
**equilibrio**. **`prob` è una probabilità nel passo**: è un **conteggio**. Sono due tipi
diversi, e il tempo entra **solo nel secondo**.

### **LA CAMPANA SI LEGGE DUE VOLTE, e ciascuna lettura ha le SUE unità**

```
ampiezza_int = salita * discesa                    # INTENSITA'   [numero puro]
ampiezza_ev  = ampiezza_int * (dt_e / DT)          # EVENTI ATTESI [numero puro]

resp_int = ampiezza_int * segno                    # -> il BERSAGLIO
resp_ev  = ampiezza_ev  * segno                    # -> la PROBABILITA'

rep   = clip(-resp_int, 0, 1)                      # equilibrio: SENZA tempo
prob  = 1 - exp(-max(resp_ev, 0))                  # per passo:  CON il tempo
_rep <- rep + (_rep - rep) * exp(-dt_e / tau_arco) # il tempo entra QUI, nella VELOCITA'
```

**Il tempo compare UNA volta per ciascuna grandezza, e mai due nella stessa.**

> ### ✅ **E COSÌ LA CURA CHIUDE UN DIFETTO CHE NÉ IO NÉ IL MANDATO AVEVAMO NOMINATO**
> **Oggi** `ampiezza = salita·discesa·(1/tau_pp)` **e `rep = clip(−ampiezza·segno, 0, 1)`**:
> quindi **l'equilibrio della repulsione dipende GIÀ da un fattore che il commento chiama
> «ritmo»**. Ed è la **terza** dipendenza da `|tw|` nello stesso bersaglio, dopo `salita` e
> `discesa`. **Togliendo il fattore di tempo restano le due che sono la legge** — attivazione
> sopra soglia, spegnimento al tetto — **e l'equilibrio smette di dipendere dall'orologio.**

### ⚠ **E IL CLIP SU `rep` RESTA, perché È RAGGIUNGIBILE — VERIFICATO, non assunto**

Avevo pensato di sostituirlo con `tanh` *(la normalizzazione che `COES_ADIM` usa per una
magnitudine)*, o di dichiararlo inerte perché il suo lato superiore è inarrivabile.
**Ho controllato, e NON è inarrivabile:**

| | |
|---|---|
| `satura(f) = f/(1 + GAMMA·|f|)` | → **`1/GAMMA`** per `f → ∞` |
| **`GAMMA = 0.05`** *(letto dal sorgente e dal referto di configurazione)* | → **`salita < 20`** |
| quindi `|resp_int| < 20` | **il clip a `1` MORDE**, e non di poco |

> **Quindi il clip resta in questa cura, e la sua sostituzione si DECIDE SU UNA MISURA, non su
> un'opinione:** `tanh` e il clip **coincidono dove il clip non morde** e differiscono solo dove
> mordeva. **Si conta quante volte morde** — è il criterio `K`, esteso da `prob` anche a `rep`.
> **Se non morde mai, la sostituzione è sicura; se morde, cambia la fisica e la decisione è di
> Luca.** *(`A12` regola 4: dichiarato, non deciso.)*

"""
t = t[:i0] + NUOVO5 + t[i1:]
N += 1

# ---------------------------------------------------------------- la tabella delle unita'
A3 = u"| `ampiezza` | numero puro | numero puro | **numero atteso di eventi** |"
B3 = (u"| `ampiezza` | numero puro **(con un fattore di tempo travestito)** | **si SDOPPIA** | "
      u"vedi le due righe sotto |\n"
      u"| **`ampiezza_int`** | — | **numero puro** | `salita·discesa`: **INTENSITÀ**, senza tempo. "
      u"Va al **bersaglio** `rep` |\n"
      u"| **`ampiezza_ev`** | — | **numero puro** | `ampiezza_int·(dt_e/DT)`: **eventi attesi**, "
      u"col tempo. Va a `prob` |")
t = s1(t, A3, B3)

A4 = u"| `resp` | numero puro | — | |"
B4 = (u"| `resp` | numero puro | **si SDOPPIA in `resp_int` e `resp_ev`** | uno per il bersaglio, "
      u"uno per la probabilita' |\n"
      u"| `rep` | numero puro **con clip**, e **col fattore di tempo** | numero puro **con clip**, "
      u"**SENZA** il fattore di tempo | e' un **equilibrio**: non deve dipendere dalla durata del "
      u"passo |")
t = s1(t, A4, B4)

# ---------------------------------------------------------------- il criterio K, esteso
A5 = (u"| **`K`** | **quante volte la vecchia `prob` avrebbe richiesto il clip** *(cioè "
      u"`resp > 1`)* | richiesta di Luca: **dice quanto la forma nuova differisce dalla "
      u"vecchia**. Se è `0`, le due forme sono indistinguibili e la cura di `:5244` è "
      u"**formale** |")
B5 = (u"| **`K`** | **quante volte il clip avrebbe morso**, su `prob` **E su `rep`** | richiesta "
      u"di Luca, **estesa a `rep`**: dice **quanto la forma nuova differisce dalla vecchia**. Se "
      u"su `prob` è `0`, la cura di `:5244` è **formale**. **Su `rep` decide se il clip si può "
      u"sostituire con `tanh`**, e quella decisione è di Luca |\n"
      u"| **`H`** | **la guardia di `_cs_nodo_prev`**: invocazioni, salti, forma, quando | `A8`. "
      u"Era **stale al `71.88 %`** in passato: se salta, `tau_arco` cade su `CS_M` e **il "
      u"rilassamento non è quello dichiarato** |")
t = s1(t, A5, B5)

# ---------------------------------------------------------------- COSA NON SO DERIVARE: aggiorna
A6 = (u"1. **`rep`, il ramo repulsivo** *(par.5)*: lascio il clip e dichiaro l'incoerenza;")
B6 = (u"1. **se il clip su `rep` si possa sostituire con `tanh`** *(par.5)*: **non è una "
      u"questione di principio ma di MISURA** — le due forme coincidono dove il clip non morde, "
      u"e `GAMMA = 0.05` dice che **può mordere** *(`salita < 20`)*. **Il criterio `K` lo "
      u"conta**, e poi decide Luca;")
t = s1(t, A6, B6)

io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("%d sostituzioni. Le due precisazioni sono nella scheda 9." % N)
