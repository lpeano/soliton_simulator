# -*- coding: utf-8 -*-
"""Scheda 9 RISCRITTA col mandato del 2026-09-24: un solo tempo d'arco, unita' normalizzate."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()
M = "<!-- SCHEDA nome=tempo-nella-mitosi funzioni=mitosi flag=TEMPO_UNICO_MITOSI,MITOSI_DIR -->"
i = t.index(M)
testa = t[:i]

NUOVA = u"""<!-- SCHEDA nome=tempo-nella-mitosi funzioni=mitosi flag=TEMPO_UNICO_MITOSI,MITOSI_DIR -->

# ⑨ IL TEMPO NELLA MITOSI — **`CURA 2`**

> **Mandato di Luca, 2026-09-24.** Flag: **`TEMPO_UNICO_MITOSI`**, spento di default.
> **Riscritta** dopo il mandato: la prima stesura aveva **due errori**, segnati con ❌.

## 0. IL PRINCIPIO, ed è di Luca

> ### **«Si applicano le cose CORRETTE e COERENTI. Dove intenzione e implementazione
> ### divergono, si realizza l'INTENZIONE. Ogni grandezza con le sue UNITÀ giuste.»**

**Operativamente: si cura dove intenzione e implementazione DIVERGONO; dove sono coerenti non
si tocca.** L'intenzione si legge **dal commento e dal nome**, che sono ciò che la legge
*dichiara di essere*.

| riga | l'INTENZIONE, dal commento | l'IMPLEMENTAZIONE | coerenti? |
|---|---|---|:--:|
| `:5240` | *«ritmo»* | `1/(1 + |tw|/PHI_CRIT)`: reciproco di una **torsione** | **NO** |
| `:5244` | una **probabilità** | `clip(resp, 0, 1)`: un **clip** `A11` | **NO** |
| `:5280` | *«rilassa con tempo `tau_pp` — **un tempo locale dello stesso arco**»* e *«`A5` livello 1, **rilassamento esponenziale**»* | una **torsione** come costante di tempo, **e un EULERO esplicito** | **NO, due volte** |
| `:5189-5196` | *«gradiente di **tempo proprio** lungo l'arco»* | gradiente di `mean(|tw|)` | **NO** |
| `:5234-5239` | soglia, tetto, centro, **inversione**: posizioni sull'asse di `tw` | esattamente quello | **SÌ → NON SI TOCCA** |

---

## 1. UN SOLO TEMPO D'ARCO: **`dt_e`, che il sistema definisce già**

**`:4352`: `dt_e = DT * 0.5 * (r[i] + r[j])`.** È **il** tempo proprio d'arco del sistema, e la
mitosi usa **quello**, cioe' il fattore adimensionale **`dt_e/DT = 0.5(r_i + r_j)`**.

### ❌ **IL MIO PRIMO ERRORE: avevo proposto `min(r_i, r_j)`**

**Era sbagliato per la ragione più semplice: creava un SECONDO orologio d'arco**, accanto a
quello che il sistema ha già. *«Un solo tempo»* è il nome di questa cura, e la mia proposta ne
aggiungeva uno.

**E l'argomento con cui l'avevo scartata la media era anch'esso sbagliato:** avevo scritto che
una media *«viola `A2`, è una statistica in una legge locale»*. **`A2` riguarda le statistiche
GLOBALI** — una mediana su tutta la rete, una media su tutti i nodi. **La media dei DUE nodi di
un arco è locale per costruzione**, ed è la definizione che il sistema usa già.

> **L'argomento causale per `min(r)` non è privo di senso, ma se vale, vale per TUTTO il
> sistema, non per la mitosi da sola.** → va **in coda** come proposta generale, `S13`.

### ⚠ **E la media ARMONICA esisteva già, per il `cs`**

`:4774`: `cs_arco = 2·cs_i·cs_j / (cs_i + cs_j)`, col commento *«**collo di bottiglia causale:
media armonica, non media aritmetica**»*. **La mia tabella delle alternative la liquidava con
«vale per rate in serie, e l'arco non lo è»: era sbagliato**, perché il sistema la usa
esattamente per questo e la chiama col suo nome.
**Il sistema ha quindi DUE medie d'arco, ciascuna col suo dominio:** **aritmetica** per il
**tempo** (`dt_e`), **armonica** per la **velocità** (`cs_arco`). **Non se ne inventa una terza.**

---

## 2. IL GRADIENTE DI TEMPO PROPRIO — **su `r`, e la ragione è derivata**

**Oggi** (`:5189-5196`): `tau_nodo = 1 + mean(|tw|)/PHI_CRIT` per nodo, poi
`grad_tau = |tau_i − tau_j|`, poi `soglia = soglia0·(1 − 0.3·tanh(grad_tau))`.

**`tau_nodo` è IDENTICO al ramo `TEMPO_SEGNO` di `ritmo()` — quello che NON GIRA** *(`Z130`)*.
**La mitosi usa come «tempo proprio» la definizione di tempo che il resto del sistema ha
SCARTATO.** Sono **due orologi nello stesso passo**.

**Con la cura: `grad_r = |r_i − r_j|`.**

### **`r` o `1/r`? Si prende `r`, e NON è una preferenza**

`tau_nodo` oggi è una **lentezza** *(«tau_nodo alto = tempo lento», lo dice il commento)*, e
l'analogo diretto della lentezza è **`1/r`**. **Ma `1/r` È ILLIMITATO**, e il conto lo mostra:

| | intervallo | `tanh` del gradiente | la modulazione `1 − 0.3·tanh` |
|---|---|---|---|
| **`r`** | `[1.4142e-6, 1.4142]` | `tanh(grad) ≤ tanh(1.4142) = 0.8884` | **`[0.7335, 1]·soglia0` — MODULA** |
| `1/r` | `[0.707, 707107]` | `grad` fino a `~7e5` → **`tanh = 1` ESATTO** | **`0.7·soglia0` COSTANTE** |

> **Con `1/r` la modulazione diventa un RISCALAMENTO COSTANTE della soglia**, cioè **un
> parametro nascosto** *(`A1`)*, non una legge. **Con `r` resta una modulazione.**
> **`A11` cor.6: un limite che satura è un allarme** — e `1/r` lo farebbe saturare **sempre**.

---

## 3. IL RILASSAMENTO DI `_rep` — **`S12` APPROVATO DA LUCA**

**Oggi** (`:5280`): `self._rep += _dte * (rep − self._rep) / max(tau_pp, 1e-12)`.

**Tre difetti nella stessa riga, e il commento ne dichiara due:**

| | |
|---|---|
| **① la DILATAZIONE È CONTATA DUE VOLTE** | `_dte` **è già** `DT·0.5(r_i+r_j)`, cioè contiene già il tempo proprio; dividere **anche** per `tau_pp` la conta una seconda volta |
| **② `tau_pp` non è una durata** | è un numero puro *(un fattore di dilatazione)*. Una costante di tempo **deve avere le unità di un tempo** |
| **③ l'integratore è un EULERO ESPLICITO** | il commento dichiara *«`A5` livello 1, **rilassamento esponenziale**»*, e `par.4` impone la **forma esatta** |

### **LA DURATA, DERIVATA: `tau_arco = d / cs_arco`**

**È il ritardo causale dell'arco**, e **le due grandezze esistono già**:

| | | unità |
|---|---|---|
| `d` | la **lunghezza dell'arco**, `self.d` | `[LAM]` |
| `cs_arco` | la velocità d'onda d'arco, **media armonica** *(`:4774`)* | `[LAM/DT]` |
| **`tau_arco = d / cs_arco`** | **una DURATA** | **`[DT]`** ✅ |

**È la stessa legge che `FORK_SU2_MEM` usa per il ritardo dei Bloch** *(`tau = d/cs`,
`_tempo_luce_nodo`)*, **al livello dell'ARCO invece che del nodo** — e al livello dell'arco `d` e
`cs_arco` sono **direttamente disponibili**, senza la media sul grado che la versione nodale deve
fare. **Zero parametri nuovi, zero coefficienti.**

### **LA FORMA ESATTA**

```
_rep  <-  rep + (_rep - rep) * exp(-dt_e / tau_arco)
```

**L'esponente è `[DT]/[DT]` = numero puro.** È la stessa forma che `PEQ_ESATTO` (`C1`) ha imposto
a `peq` e che `par.4` impone a ogni rilassamento di primo ordine. **È una combinazione convessa**,
quindi `_rep` resta **fra `rep` e il suo valore precedente per QUALUNQUE passo**: non può
scavalcare, e il difetto che l'Eulero aveva su `peq` *(`dt/tau > 1` misurato `1.2018`)* **non può
ripresentarsi**.

### ✅ **E DUE CLAMP SPARISCONO PER COSTRUZIONE** *(`A11`)*

| clamp | perché sparisce |
|---|---|
| `max(tau_pp, 1e-12)` | `tau_pp` **esce dalla formula**: non c'è più nulla da proteggere |
| *(nuovo)* una divisione per `tau_arco` | `d ≥ LAM` per costruzione *(la scala minima)* e `cs_arco > 0`, quindi **`tau_arco > 0` derivato**. **Serve solo il contatore** del caso `cs_arco = 0`, che non deve capitare |

---

## 4. LA PROBABILITÀ DI MITOSI — **la forma di Poisson, e il clip sparisce**

**Oggi** (`:5244`): `prob = np.clip(resp, 0.0, 1.0)`. **Un clip `A11` su una probabilità.**

**Con la cura:**

```
prob = 1 - exp(-max(resp, 0))
```

**Perché è DERIVATA e non scelta:** `resp` è il **numero atteso di eventi** nel passo proprio
locale *(un tasso per unità di tempo di coordinata, moltiplicato per `dt_e/DT`)*, e la
probabilità di **almeno un evento** di un processo di Poisson con quel numero atteso è
`1 − e^{−λ}`. **Sta in `[0, 1)` per costruzione: il clip non ha più niente da tagliare.**

**E per ampiezze piccole coincide con la vecchia forma:** `1 − e^{−λ} = λ − λ²/2 + …`, quindi
**l'errore relativo è `λ/2`**: sotto `λ = 0.02` le due forme differiscono di meno dell'`1 %`.

### ⚠ **IL FATTORE DI TEMPO VA CONTATO UNA VOLTA SOLA**

`tau_locale` **non si sostituisce con `dt_e/DT` lasciando poi un secondo `dt_e/DT`
nell'esponente**: sarebbe **la dilatazione contata due volte**, lo stesso difetto del par.3 ①.
**Il fattore compare UNA volta**, dentro `ampiezza`:

```
ampiezza = salita * discesa * (dt_e / DT)        # numero atteso di eventi
resp     = ampiezza * segno
prob     = 1 - exp(-max(resp, 0))
```

### ✅ **E LA SOSTITUZIONE TOGLIE UN DOPPIO CONTO DELLA TORSIONE**

`tau_locale = 1/(1 + |tw|/PHI_CRIT)` **decresce con la torsione**. Ma `discesa =
clip(1 − |tw|/TW_TETTO, 0, 1)` **fa già esattamente questo**, e va a zero al tetto.
**Quindi oggi la soppressione ad alta torsione è contata DUE VOLTE**, una in `discesa` e una in
`tau_locale`. **Con `dt_e/DT` resta contata una volta**, in `discesa`, dove la legge la
dichiara — e il fattore di tempo fa il mestiere del tempo.

---

## 5. ❓ **L'UNICA DECISIONE CHE NON PRENDO: `rep`, il ramo REPULSIVO**

`:5249`: `rep = np.clip(-resp, 0.0, 1.0)`. **È un clip `A11`, come `prob`** — ma **`rep` non è
una probabilità: è una MAGNITUDINE**, e alimenta una spinta su `d0`.

**Quindi la forma di Poisson NON va bene per lui**: `1 − e^{−λ}` è la probabilità di almeno un
evento, e qui non si contano eventi.

| opzione | conseguenza |
|---|---|
| **(i)** lo si lascia col clip | **creazione e repulsione leggono la STESSA campana in due modi diversi**: una come *tasso*, l'altra come *magnitudine*. È **la doppia lettura che questa cura sta togliendo** |
| **(ii)** `rep = tanh(max(-resp, 0))` | è la normalizzazione che `COES_ADIM` usa per una magnitudine *(`|F| ≤ 1` per costruzione)*. **Ma cambia la SCALA della repulsione**, e **non so derivare che il cambiamento sia neutro** |

> **NON SCELGO, e non lo metto nel codice.** Il mandato copre `prob` (`:5244`); `rep` è
> `:5249`. **Faccio `(i)` — il clip resta — e lo DICHIARO come incoerenza che la cura NON
> chiude**, così il referto la porta a Luca invece di nasconderla. *(`A12` regola 4.)*

---

## 6. LA TABELLA DELLE UNITÀ

| grandezza | **prima** | **dopo** | nota |
|---|---|---|---|
| `DT` | tempo di coordinata | — | l'unità di tempo |
| `r` | numero puro | — | `dt_n = DT·r` |
| `dt_e` | `[DT]` | — | `DT·0.5(r_i+r_j)`, `:4352` |
| `dt_e/DT` | — | **numero puro** | il fattore di tempo proprio d'arco |
| `avv = |tw|` | `[rad]` | — | torsione |
| `soglia` | `[rad]` | `[rad]` | modulata da `grad_r`, non da `grad_tau` |
| `ecc = avv/soglia − 1` | numero puro | — | rapporto di due angoli |
| `salita`, `discesa` | numero puro | — | |
| `tau_locale` | numero puro *(ma **era** un reciproco di torsione)* | **`dt_e/DT`** | **ora è un tempo, come il nome dice** |
| `ampiezza` | numero puro | numero puro | **numero atteso di eventi** |
| `segno` | numero puro `(−1, 1)` | — | resta |
| `resp` | numero puro | — | |
| `prob` | numero puro **con clip** | numero puro **in `[0,1)` per costruzione** | il clip sparisce |
| `tau_pp` | numero puro, **usato come TEMPO** | **esce dagli usi TEMPO** | resta solo come coordinata di torsione |
| **`tau_arco`** | — | **`[DT]`** | `d/cs_arco`: **una durata vera** |
| `_rep` | numero puro | — | rilassa in forma **esatta** |
| `grad_tau` → `grad_r` | `[rad]`/PHI_CRIT | **numero puro** | gradiente di un **ritmo** |

**Nessuna grandezza con unità diverse viene sommata o confrontata**: gli unici confronti sono
`avv` con `soglia` *(entrambi `[rad]`)* e `tau_pp` con `centro` *(entrambi numeri puri sull'asse
di torsione)*.

---

## 7. LA PROVENIENZA DI `r` DENTRO `mitosi()`, e la guardia

`r` per nodo è in `self._r_corrente`, scritto in `step()` a `:4397` **ma solo
`if FORK_SU2_MEM`**.

| questione | risposta, **dal codice** |
|---|---|
| è disponibile? | **sì**: il ciclo è `step(); mitosi(); …`, quindi `mitosi()` segue **immediatamente** |
| la lunghezza è giusta? | **sì in quel punto** — `n` non è ancora cresciuto. Ma è un array **per-nodo attraversato da un punto di crescita**: la classe `A8b` di `_cs_nodo_prev` *(`71.88 %`)* e `_psi_spin_prec` *(`95.33 %`)* |
| se `FORK_SU2_MEM` è spento? | `_r_corrente` è `None`. **Dipendenza DICHIARATA**: nei run del fork è acceso |
| indici d'arco `≥ n`? | il codice si guarda già *(`self.i[self.i < self.n]`, `:5190-5192`)*: si fa lo stesso, **e si conta** |

**LA GUARDIA SI CONTA, NON SI TACE** *(`A8`)*: **quattro** numeri — invocazioni, salti, **la
forma** al fallimento *(le due lunghezze)*, e **quando** *(l'indice dell'ultima saltata)*.
Il fallback è **`dt_e/DT = 1`**, cioè *«nessuna dilatazione»*: la stessa convenzione che
`ritmo()` usa quando non c'è un passato *(`np.ones`)*, **non una convenzione nuova**.

---

## 8. COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **`rep`, il ramo repulsivo** *(par.5)*: lascio il clip e dichiaro l'incoerenza;
2. **il `0.3`** della modulazione della soglia: era un numero scelto **prima** della cura, e la
   cura non lo migliora né lo peggiora — **ne cambia la scala dell'argomento**, e il conto del
   par.2 dice di quanto *(`tanh ≤ 0.8884` invece di `→ 1`)*;
3. **il `3.0`** dentro `tanh(3.0·(tau_pp − centro))`: resta `TORSIONE`, resta com'è, **è un
   numero scelto** e la scheda lo deve dire;
4. **che il tasso di mitosi resti dello stesso ordine.** `1/tau_pp ∈ (0,1]` con mediana vicina a
   `1`; `dt_e/DT` ha **mediana misurata `≈ 0.68`** *(`Z135`)*. **Il tasso può calare di ~`1/3`**,
   e **`E1a` è il suo giudice**. *(Non metto un fattore di normalizzazione: sarebbe un numero
   scelto.)*

---

## 9. I CRITERI DELLA PROVA, fissati qui

| | criterio | origine |
|---|---|---|
| **`E1a`** | la mitosi **non muore**: nascite `> 0` e eventi **dello stesso ordine** del riferimento | di Luca. `FASE_2PI` è caduta qui *(`62` → `1` evento)* |
| **`E1b`** | **non esplode**: `n` finale `< 10×` il riferimento | **misurata**: `178` archi per nodo |
| **`B`** | il **bilancio di `d0` CHIUDE** | il criterio di `G4` |
| **`K`** | **quante volte la vecchia `prob` avrebbe richiesto il clip** *(cioè `resp > 1`)* | richiesta di Luca: **dice quanto la forma nuova differisce dalla vecchia**. Se è `0`, le due forme sono indistinguibili e la cura di `:5244` è **formale** |
| **`G`** | **dove nasce la materia rispetto al gradiente di `r`** | richiesta di Luca. **Si RIPORTA**, non si giudica |
| **`C`** | la **guardia** di `_r_corrente`: quante volte salta, e **quando** | `A8`. Se salta **fuori dal transitorio**, il referto **non si legge** |

**Riferimento: `csv/_test_fork/_cura1_corto`** — stessa configurazione, `CURA 1` accesa, questo
flag **spento**. **Differisce per UN interruttore.**
"""
io.open(P, "w", encoding="utf-8", newline="\n").write(testa + NUOVA)
print("scheda 9 riscritta")
