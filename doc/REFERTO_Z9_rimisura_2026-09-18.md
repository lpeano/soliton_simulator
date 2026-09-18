# REFERTO — **`Z9` rimisurata sul blob attuale: INTATTA. E il meccanismo è bloccato da una normalizzazione**

**Data:** 2026-09-18 · **Blob** `72acd6aa` (git) / `aa84755b` (byte) · **HEAD** `93308af`+
**Task history scritto e pushato PRIMA:** `93308af` · **Strumento:** `csv/_test_fork/_rimisura_Z9.py`
**(lo stesso usato le due volte precedenti — non ne è stato scritto uno nuovo)**

---

## 0. IN DUE RIGHE

**`Z9` è intatta: `ramp = 1` a `~5680` passi (scena originale) contro `~5526` — `+2.8 %`.**
**E il meccanismo che Luca descriveva è bloccato al primo ordine da una normalizzazione dentro
`ritmo()` — verificato, non dedotto.**

---

## 1. PASSO 0 — la configurazione misurata, **stampata e non assunta**

```
SPINORE_VIVO = True   SPINORE = True   SPIN_FEEDBACK = True   FRAME_DRAG = True
CS_DINAMICO  = True   CHI_CORE = True  TEMPO_PROPRIO_ORIENTATO = False
-> il feedback GIRA in questa misura?  SI'
TAU_A = 50.0   <- la stessa delle misure storiche
```

**Nota non banale:** la lista di flag dello script **non contiene `SPIN_FEEDBACK`**. Misura la
configurazione nuova **solo perché il default è stato promosso**. È la classe di difetto che la
promozione di `STEP2_OROLOGIO` aveva insegnato — **e stavolta è stampata invece che assunta.**

E `TAU_A = 50`: le mie misure recenti erano a `2.0`, e `ramp = min(1, eta/TAU_A)`. **Confrontarle
sarebbe stato A3c puro.**

## 2. IL NUMERO — **`Z9` regge**

### Scena (A) — originale, **l'unico confronto lecito coi numeri storici**

| passo | `ramp` mediano | **storico** |
|---|---|---|
| 1 | **0.0002** | 0.0002 |
| 60 | **0.010232** | 0.0106 |
| 120 | **0.021151** | 0.0217 |

crescita di `eta` per passo **0.0088** (storico ~0.009) · **`ramp = 1` a `5680` passi** (storico
**`~5526`**) → **`+2.8 %`**

### Scena (B) — il batch, **il numero che vale per il sistema che gira davvero**

`ramp` 1/60/120 = **0.0002 / 0.0099 / 0.0199**, crescita `0.00827`, **`ramp = 1` a `6049` passi**.

> **La previsione ex ante era «invariato entro un fattore ~2». È entro il 3 %.**

## 3. PASSO 1 (P4) — **perché non si è mosso: il canale principale è PINNATO**

Luca descriveva: `eta += dt_n`, `dt_n = DT·r`, `r = ritmo()` dipende da `psi`, il feedback cambia
`psi`. **La catena esiste tutta.** Ma `ritmo()` (`:2043-2049`):

```python
med = max(median(|f|), 1e-9);  x = f/med;  r = x/sqrt(1+x²)+1e-6   # MONOTONA
r_unit = r(x=1);  return 1 + TAU_LOC*(r/r_unit − 1)                # TAU_LOC = 1
```

Con `TEMPO_PROPRIO_ORIENTATO = False` (default) **`f = |signed| ≥ 0`**, quindi `median(x) = 1`
esatto, la mappa è monotona, e **la mediana del valore restituito è `1.0`.**

**Misurato su 246 chiamate:**

```
median(r) : mediana 0.999999450   min 1.414e-06   max 1.000000000
scarto da 1.0 sulle chiamate non degeneri : MAX 8.27e-07
```

> **`median(dt_n) = DT` esattamente ⟹ l'incremento MEDIANO di `eta` per passo è PINNATO per
> costruzione.** Il meccanismo che Luca descrive **è reale ma bloccato al primo ordine.** È `C12` —
> **ma la condizione andava verificata**: con `--tempo-proprio-orientato` l'ancoraggio **cadrebbe**.

### ⚠ E due correzioni ai miei stessi criteri, in due giri consecutivi

**Prima:** avevo scritto il criterio col **MASSIMO**, e dava `scarto MAX da 1.0 = 1.000e+00` — che
letto da solo direbbe *«l'ancoraggio non c'è»*, mentre i numeri accanto lo smentivano. **Il massimo
descriveva la coda, non la popolazione**: stessa forma di `A3c` e della pendenza di `Z27`.

**Poi, e l'ho sbagliato di nuovo:** corretto in **frazione**, ho messo la soglia a `1e-6` e ho
etichettato **116 chiamate su 246 come «transitorio degenere»**. **Sono i valori
`0.999857 … 0.999919`: sono `1.0` a quattro cifre**, cioè la mediana campionaria su una popolazione
discreta — **non una rottura dell'ancoraggio.**

**La lettura corretta:** **`median(r) = 1.0` a meno di `~1.4e-4` in 245 chiamate su 246.**
L'**unica** davvero degenere è quella a `1e-6`: il primo passo, con `f` identicamente nullo, dove
`med` cade sul pavimento `1e-9`. *(E i due estremi osservati, `1.414e-06` e `1.41421`, non sono
rumore: sono `x→0` e `x→∞` della saturazione, cioè `1/√2` e `√2` normalizzati.)*

**La soglia era troppo stretta, e l'etichetta che ne è uscita era sbagliata. La correggo qui invece
di lasciarla nell'output.**

## 4. `R6` — e un numero da annotare

```
_pesi() per passo: MEDIANA 12   (riferimento 8bfcf46: 16, con 9 PRIMA e 7 DOPO)
totale PRIMA 861, DOPO 624   -> gira ANCORA A CAVALLO della scrittura della cache: R6 REGGE
per CHIAMANTE: stato_crossover 1354, step 123, calcola_psi 8
fallback su _cs_nodo_prev: 18 su 1485 = 1.2121 %
```

**`R6` regge.** E il fallback della cache è **1.21 %**, non 0: **piccolo, ma non nullo.**
**Non l'ho interpretato** — serve il confronto col valore della rimisura precedente, che non ho
sottomano. **Annotato come da verificare.**

## 5. COSA NE SEGUE

- **`Z9` non cambia nessuna conclusione**: il numero si aggiorna da `~5526` a **`~5680` (A)** /
  **`~6049` (B)**, e resta il fatto che **i run da 120-500 passi vivono nel transitorio** — a 120
  passi il sistema ha vissuto **~1/50** della maturazione.
- **La preoccupazione di Luca era legittima e la catena esiste** — ma il primo ordine è assorbito
  da una normalizzazione. **Ciò che resta libero è la forma della distribuzione di `r` e la
  popolazione**, e insieme valgono `+2.8 %`.
- **`Z9` non precludeva `Z30`**, e ora si può dire con un numero misurato sul blob attuale invece
  che su uno di due generazioni fa.

## 6. I LIMITI

Un seme (5), 120 passi, due scene. **Le due scene non si mescolano** e danno numeri diversi
(`5680` contro `6049`, **+6.5 %**): è la stessa differenza di metodo già registrata. **Il numero da
citare d'ora in poi è quello della scena (B)**, che è il sistema che gira davvero.
