# -*- coding: utf-8 -*-
"""La scheda 9: IL TEMPO NELLA MITOSI. CURA 2, prima del codice."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()
assert "nome=tempo-nella-mitosi" not in t

SCHEDA = u"""

---

<!-- SCHEDA nome=tempo-nella-mitosi funzioni=mitosi flag=TEMPO_UNICO_MITOSI,MITOSI_DIR -->

# ⑨ IL TEMPO NELLA MITOSI — **`CURA 2`**, la scheda **prima** del codice

> **Mandato di Luca, 2026-09-24.** Flag previsto: **`TEMPO_UNICO_MITOSI`**, spento di default.
> **Questa scheda non contiene codice.** Serve a decidere **che cosa** cambia, e a far vedere
> **due cose che l'elenco fa emergere** e che non erano nel mandato.

## 1. OGNI USO DI `tau_pp` DENTRO `mitosi()`, CLASSIFICATO

**La sorgente, e il punto di partenza è che NON è un tempo:**

| riga | espressione | che cos'è **davvero** |
|---|---|---|
| **`:5233`** | `tau_pp = 1.0 + avv / PHI_CRIT`, con `avv = \|tw\|` | **una MISURA DI TORSIONE chiamata «tempo proprio locale»**. Non legge nessun orologio: legge `tw` |

**E da lì si biforca in due usi che NON sono la stessa cosa:**

| riga | espressione | **classe** | perché |
|---|---|:--:|---|
| **`:5240`** | `tau_locale = 1.0 / tau_pp` | **`TEMPO`** | è chiamato *«ritmo»* nel commento, e **si comporta come un ritmo**: entra moltiplicando l'ampiezza |
| **`:5241`** | `ampiezza = salita * discesa * tau_locale` | **`TEMPO`** *(via `tau_locale`)* | l'ampiezza della campana è modulata da un **ritmo** |
| **`:5280`** | `self._rep += _dte * (rep − self._rep) / max(tau_pp, 1e-12)` | **`TEMPO`** | `tau_pp` è qui la **costante di tempo** di un rilassamento |
| **`:5234`** | `tau_soglia = 1.0 + soglia / PHI_CRIT` | **`TORSIONE`** | è **la soglia**, espressa in unità di `tw`. Non è un tempo: è una posizione sull'asse della torsione |
| **`:5235`** | `tau_tetto = 1.0 + TW_TETTO / PHI_CRIT` *(`= 3`)* | **`TORSIONE`** | il tetto `4π`, idem |
| **`:5238`** | `centro = 0.5 * (tau_soglia + tau_tetto)` | **`TORSIONE`** | il punto medio **fra due posizioni sull'asse di `tw`** |
| **`:5239`** | `segno = −tanh(3.0 * (tau_pp − centro))` | **`TORSIONE`** | **l'INVERSIONE**: usa `tau_pp` come **coordinata sull'asse della torsione**, non come tempo. `crea` sotto il centro, `respinge` sopra |
| **`:5277-5279`** | il clamp `1e-12` su `tau_pp`, **contato** | **presidio** | `A11`: protegge da una divisione per zero. Vedi §4 |

**E il quarto uso, quello che Luca chiama *la modulazione della soglia col gradiente di tempo
proprio*, sta PRIMA e non usa `tau_pp` ma un suo gemello:**

| riga | espressione | **classe** |
|---|---|:--:|
| **`:5189-5193`** | `tau_nodo = 1.0 + mean(\|tw\|)/PHI_CRIT` **per nodo** | **`TEMPO` per INTENZIONE, `TORSIONE` per IMPLEMENTAZIONE** |
| **`:5194`** | `grad_tau = \|tau_nodo[i] − tau_nodo[j]\|` | idem |
| **`:5196`** | `soglia = soglia0 * (1.0 − 0.3 * tanh(grad_tau))` | idem |

> ### ⚠ **`tau_nodo` È LA STESSA FORMULA DEL RAMO MORTO DI `ritmo()`**
> `tau_nodo = 1 + mean(\|tw\|)/PHI_CRIT` è **identico** a
> `r = 1 + mean(\|tw\|)/PHI_CRIT`, il ramo **`TEMPO_SEGNO`** di `ritmo()` — **che non gira**
> *(`TEMPO_SEGNO = False` in 9 run su 11, `Z130`)*.
> **Quindi la mitosi usa, come «tempo proprio», esattamente la definizione di tempo che il
> resto del sistema ha SCARTATO.** Non è un dettaglio di stile: è **due orologi diversi nello
> stesso passo**, ed è il difetto che `CURA 2` deve togliere.

**IL CRITERIO CHE SEPARA LE DUE CLASSI, in una riga:** *un uso è `TEMPO` se la grandezza entra
**come durata o come ritmo** (se la si potesse misurare con un cronometro); è `TORSIONE` se
entra **come posizione su un asse** (se la si potesse misurare con un goniometro).*
`segno` confronta `tau_pp` con `centro`, che è una posizione: **goniometro**.
`tau_locale` moltiplica un'ampiezza per unità di tempo: **cronometro**.

## 2. COME SI OTTIENE IL RITMO DI UN **ARCO** DAGLI `r` DEI SUOI DUE NODI

**Candidata, ed è quella che scelgo: `r_arco = min(r_i, r_j)` — il più LENTO dei due.**

**La derivazione, e non è un'analogia:** `r` è un **ritmo** *(`dt_n = DT · r`, quindi `r` grande
= orologio veloce)*. Un processo che vive **sull'arco** coinvolge **entrambi** i nodi, quindi
non può avanzare più in fretta del **più lento dei due**: altrimenti l'estremo lento
riceverebbe, nel proprio tempo proprio, più di quanto il suo orologio ha battuto. **È
causalità, non prudenza.**

**E ha un PRECEDENTE NEL CODICE, non inventato qui:** `COES_CAUSALE` *(scheda ④)* usa
**`cs` del nodo PIÙ LENTO** per il tetto del cono d'arco, con lo stesso argomento.

**LE ALTERNATIVE, e perché no** *(si dichiarano, non si nascondono)*:

| candidata | perché NO |
|---|---|
| **media** `(r_i + r_j)/2` | **non è causale**: un nodo veloce accelera l'arco oltre il battito del nodo lento. E una media è una **statistica**, non una legge locale *(`A2`)* |
| **media armonica** `2/(1/r_i + 1/r_j)` | naturale per **rate in serie**, ma l'arco **non è** due processi in serie: è **uno** processo fra due estremi |
| **media geometrica** `√(r_i·r_j)` | **nessuna derivazione**: sarebbe scelta perché «sta in mezzo» |
| **max** | **anti-causale**: l'arco andrebbe più veloce del suo estremo lento |
| `r` del nodo `i` *(orientato)* | **rompe l'antisimmetria**: `r_ij ≠ r_ji`, e un arco non ha un verso privilegiato |

## 3. COSA DIVENTA OGNI USO `TEMPO`

| oggi | con `TEMPO_UNICO_MITOSI` | nota dimensionale |
|---|---|---|
| `tau_locale = 1/tau_pp` | **`tau_locale = r_arco`** | `r` **è già** un ritmo: non si inverte. Invertirlo darebbe un tempo dove serve un ritmo |
| `/max(tau_pp, 1e-12)` *(costante di tempo)* | **`· r_arco`** | la costante di tempo è `1/r_arco`, quindi dividerci equivale a **moltiplicare per `r_arco`** |
| `grad_tau` da `tau_nodo` | **`grad_r = \|r_i − r_j\|`** | lo stesso gradiente, sull'orologio **vero** invece che sul proxy di torsione |

**E cosa NON cambia:** `tau_soglia`, `tau_tetto`, `centro`, `segno`. **Restano in unità di `tw`**,
perché sono posizioni sull'asse della torsione. **Il nome `tau_` su quelle quattro è
fuorviante** e va cambiato in `tw_`-qualcosa, ma **il rinominare è un cambiamento a parte**: qui
si cambia la fisica, non i nomi *(un commit = un cambiamento logico)*.

## 4. I LIMITI, CLASSIFICATI CON `A11`

| limite | oggi | con la cura |
|---|---|---|
| `max(tau_pp, 1e-12)` *(`:5280`)* | **clamp che protegge da una divisione per zero** → `A11` dice di **cercare l'errore** | **SPARISCE PER COSTRUZIONE:** `r` ha un **pavimento derivato** *(`1.4142e-6`, dalla formula `x/√(1+x²) + 10⁻⁶` normalizzata)*, quindi `1/r ≤ 707107` e non c'è niente da proteggere. **Un clamp che sparisce è meglio di un clamp giustificato** |
| `0.3 * tanh(grad_tau)` *(`:5196`)* | **tetto al `30 %`** sulla modulazione della soglia | **RESTA, e resta un numero SCELTO.** Non so derivarlo *(§6)*. Con `grad_r` cambia la **scala** del suo argomento, quindi **il `30 %` morde in modo diverso** — ed è una cosa da misurare, non da assumere |

## 5. ⚠ DUE COSE CHE L'ELENCO FA EMERGERE, e che non erano nel mandato

### ① **LA SCALA DELL'AMPIEZZA CAMBIA, E NON SO DERIVARE CHE RESTI LA STESSA**

`tau_locale = 1/tau_pp` vive in **`(0, 1]`** *(perché `tau_pp ≥ 1`)*. **`r` vive in
`[1.4142e-6, 1.4142]`**, e nel giro corto di `CURA 1` la sua **mediana è `0.68`**.

**`ampiezza` entra in `prob = clip(resp, 0, 1)`**, quindi **la scala decide il tasso di mitosi**.
Sostituire `r` a `1/tau_pp` cambia quella scala di un fattore `O(1)` **che non so dimostrare
essere `1`**.

> **NON metto un fattore di normalizzazione**, perché sarebbe un **numero scelto** *(`A1`)* e
> peggiorerebbe le cose. **Lo dichiaro come il rischio principale della cura**, e **`E1` — *la
> mitosi non muore e non esplode* — è esattamente il suo giudice.** È lo stesso posto in cui
> `FASE_2PI` è caduta *(`Z127`)*, per un motivo diverso.

### ② **IL RILASSAMENTO DI `:5280` È UN EULERO ESPLICITO, E `par.4` LO VIETA**

```python
self._rep = self._rep + _dte * (rep - self._rep) / np.maximum(tau_pp, 1e-12)
```

**`CLAUDE.md` par.4 è esplicito:** *«per il RILASSAMENTO di primo ordine usa il passo ESATTO
`U(t+dt) = U_target + (U−U_target)·e^{−dt/tau}`, NON Verlet»* — e un Eulero esplicito è **peggio
di Verlet** su questo punto. **È la stessa famiglia che `PEQ_ESATTO` (`C1`) ha curato per `peq`**,
dove l'Eulero **scavalcava sotto zero** per `dt_e/tau > 1` *(misurato `1.2018`)*.

> **QUESTO NON È PARTE DI `CURA 2`, e non lo tocco:** un commit = un cambiamento logico, e
> mescolare *«quale tempo»* con *«quale integratore»* renderebbe il risultato ininterpretabile
> *(par.1)*.
> **MA È UNA DOMANDA PER LUCA, e va posta adesso perché `CURA 2` TOCCA QUELLA RIGA:** curare il
> tempo e lasciare l'integratore sbagliato è **mezzo lavoro sulla stessa riga**.
> **→ registrato nella coda come difetto candidato.**

## 6. COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **che la scala dell'ampiezza resti la stessa** *(§5 ①)*. È il rischio principale;
2. **il `0.3` della modulazione della soglia.** Era già un numero scelto prima della cura, e la
   cura **non lo migliora né lo peggiora**: lo **sposta su un'altra scala**;
3. **se `grad_r` sia il gradiente giusto**, o se il gradiente vada preso su `1/r` *(il tempo)*
   invece che su `r` *(il ritmo)*. `\|r_i − r_j\|` e `\|1/r_i − 1/r_j\|` **non sono monotoni
   l'uno nell'altro** quando gli `r` sono piccoli, e la differenza **non è cosmetica**;
4. **il `3.0` dentro `tanh(3.0·(tau_pp − centro))`.** Resta `TORSIONE` e resta com'è, ma è un
   numero scelto: **lo dichiaro qui perché la scheda lo deve dire**, non perché `CURA 2` lo tocchi.

## 7. IL PROBLEMA DELLA PROVENIENZA DI `r` DENTRO `mitosi()`

**`r` per nodo sta in `self._r_corrente`, scritto in `step()` a `:4397` — ma solo
`if FORK_SU2_MEM`.**

| questione | risposta, **dal codice** |
|---|---|
| è disponibile quando `mitosi()` gira? | **sì**: il ciclo del driver è `step(); mitosi(); rilassa_disegno(); memoria_hebbiana_moto()`, quindi `mitosi()` segue **immediatamente** `step()` |
| la lunghezza è giusta? | **sì in quel punto**: `n` non è ancora cresciuto. **Ma è un array per-nodo attraversato da un punto di crescita**, cioè la classe **`A8b`** di `_cs_nodo_prev` *(71.88 %)* e `_psi_spin_prec` *(95.33 %)* |
| e se `FORK_SU2_MEM` è spento? | **`_r_corrente` è `None`**. Nei run del fork è **acceso**, ma **una dipendenza va DICHIARATA**: `TEMPO_UNICO_MITOSI` **richiede `--fork-su2-mem`**, e senza deve **rifiutare** o **contare**, non cadere in silenzio |

> **LA GUARDIA SI CONTA, NON SI TACE** *(`A8`)*: invocazioni, salti, **la forma al fallimento**
> *(le due lunghezze)* e **quando** *(l'indice dell'ultima invocazione saltata)*. **Quattro
> numeri, non uno** — perché `20 %` di salti nelle prime dieci invocazioni e `20 %` sparsi su
> tutto il run **danno lo stesso conteggio e sono due diagnosi opposte.**

## 8. I CRITERI DELLA PROVA, fissati qui

| | criterio | origine |
|---|---|---|
| **`E1a`** | la mitosi **non muore**: nascite `> 0`, eventi **dello stesso ordine** del riferimento | di Luca. Il nullo: se la scala dell'ampiezza crollasse, le nascite andrebbero a `0` — **è successo con `FASE_2PI`** |
| **`E1b`** | la mitosi **non esplode**: `n` finale **`< 10×`** il riferimento | **misurata**: `178` archi per nodo, quindi `10× n` ≈ `5.3M` archi = `10×` memoria e tempo |
| **`B`** | il **bilancio di `d0` CHIUDE** | il criterio di `G4`, invariato |
| **`G`** | **dove nasce la materia rispetto al gradiente di `r`** | richiesta di Luca. **Si RIPORTA**, non si giudica: non ho un'attesa derivata su questo |
| **`C`** | la **guardia** di `_r_corrente`: quante volte salta, e **quando** | `A8`. Se salta **fuori dal transitorio**, la cura gira su un fallback e **il referto non si legge** |

**Riferimento: `csv/_test_fork/_cura1_corto`** — *stessa configurazione, `CURA 1` accesa, flag
`TEMPO_UNICO_MITOSI` spento*. **È il confronto giusto perché differisce per UN interruttore.**
"""
io.open(P, "w", encoding="utf-8", newline="\n").write(t.rstrip("\n") + SCHEDA + "\n")
print("scheda 9 (tempo-nella-mitosi) scritta")
