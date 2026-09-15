# REFERTO — i QUATTRO BRACCI, gradiente di risoluzione. **Esito (A), NON conclusivo.**

**Data:** 2026-09-15 · **Branch:** `fork-su2` · **Blob:** `08784685` (verificato **dentro ogni CSV**)
**4 run · 2 bracci × 2 semi · 500 passi · 11 campioni ciascuno**
Predizione e soglie committate **prima**: `c547294` (predizione), `b934445` (soglie in codice).
Dati: `csv/_test_fork/_vuoto_cs{OFF,ON}_s{1,2}.vuoto.csv` · Verdetto: `_verdetto_4bracci.txt`.

---

## 0. IN UNA RIGA

> **Nessuna firma emerge, in nessuno dei due bracci — nemmeno a risoluzione 6.4 volte migliore.**
> **Esito (A). E (A) NON è conclusivo**, perché `theta` resta a **13.7–16.5 giri/passo**: il settore
> è ancora aliasato, solo molto meno.

---

## 1. CONFORMITÀ — **PASS su tutti e quattro, ogni campo**

| campo | `OFF_s1` | `OFF_s2` | `ON_s1` | `ON_s2` |
|---|---|---|---|---|
| `blob` | `08784685` | `08784685` | `08784685` | `08784685` |
| **`CS_DINAMICO`** | **1** | **1** | **1** | **1** |
| `FORK_SU2` / `_MEM` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **`TAU_LUCE`** | **0** | **0** | **1** | **1** |
| `KURAMOTO` / `STEP2` / `TURBO` | 0/0/1.0 | 0/0/1.0 | 0/0/1.0 | 0/0/1.0 |
| `seed` / `tag` | 1 / csOFF | 2 / csOFF | 1 / csON | 2 / csON |
| campioni / passo | 11 / 500 | 11 / 500 | 11 / 500 | 11 / 500 |

**Un solo interruttore di differenza, e stavolta è scritto NEI DATI**, non nel nome del file.

---

## 2. IL GRADIENTE DI RISOLUZIONE — **6.4×, il doppio dell'atteso**

| braccio | `theta` seme 1 | seme 2 | media | frazione `> 30°/passo` |
|---|---|---|---|---|
| **OFF** | 101.22 | 91.53 | **96.37 giri/passo** | 0.9992 / 0.9996 |
| **ON** | 16.46 | 13.71 | **15.08 giri/passo** | 0.9618 / 0.9780 |

> **Fattore 6.39.** Atteso dal T3 (`129 → 39`): **3.3**. Visto al passo 300: **4.3**. **Finale: 6.39.**
> Il gradiente **cresce col tempo**, e a 500 passi è **il doppio** di quanto la lettura T3 suggerisse.

**Questo conta per come si legge (A):** l'asimmetria dichiarata prima del run — *l'aliasing distrugge
segnale, non lo crea* — è **più forte** di quanto stimato. Un (A) a risoluzione 6.4× migliore
**restringe molto** lo spazio in cui un ordine potrebbe nascondersi.

**Ma non lo chiude:** `theta = 13.7–16.5` è **ancora oltre il giro intero per passo**, e il
**96–98 %** dei nodi resta sopra i 30°/passo. *(Prima: 99.9 %.)*

---

## 3. LE FIRME — tutte al valore casuale

**Null:** `chi = 90.000° ± 39.171°` · `|<n>|·√N = 0.9213 ± 0.3888` (p95 1.60) · autocorrelazione `≈ 0`.

| | `OFF_s1` | `OFF_s2` | `ON_s1` | `ON_s2` |
|---|---|---|---|---|
| `chi` **materia** | 89.7779 (`z −2.12`) | 89.8756 (`z −1.45`) | **90.0481** (`z +0.56`) | **90.0845** (`z +0.99`) |
| `chi` **p90** | 89.9283 (`z −0.48`) | **89.2991** (`z −4.17`) | 89.9983 (`z −0.01`) | 90.2239 (`z +1.23`) |
| `\|<n>\|·√N` | 1.2373 (`z +0.81`) | 0.7596 (`z −0.42`) | 0.1467 (`z −1.99`) | 0.8130 (`z −0.28`) |
| autocorr., `max\|z\|` su 10 bin | 1.81 | 2.04 | 2.36 | 2.20 |
| frazioni `<10°` / `>170°` (mat) | .00728 / .00747 | .00765 / .00741 | .00790 / .00766 | .00755 / .00703 |

**Autocorrelazione: `max|z|` fra 1.81 e 2.36 su QUARANTA bin totali.** Sotto ipotesi nulla il massimo
di 40 gaussiane vale ~2.2–2.5. **È esattamente il rumore.** Piatta da 0.58 a 14.99.

**Frazioni ai poli: `<10°` e `>170°` coincidono entro il terzo decimale** in tutti e quattro —
distribuzione **simmetrica attorno a 90°**. È il controllo che **non dipende dalle barre d'errore**,
ed è il più robusto che abbiamo: **nessun eccesso di allineati, nessuno di antipodali.**

---

## 4. ⚠ L'UNICO `z` GRANDE **NON SI RIPRODUCE** — ed è C10 in azione

`OFF_s2` dà `chi_p90 = 89.2991`, `z = −4.17`: **|z| > 3, quindi (A) fallisce** e lo script lo marca
**INDETERMINATO**. Ma sull'**altro seme dello stesso braccio**, `OFF_s1` dà `−0.0717`.

> **I due semi dello stesso braccio differiscono di 0.63°, cioè QUATTRO VOLTE la `SE` interna.**
> Il `z = −4.17` è **dispersione di run**, non una firma. **È la terza volta oggi** che la `SE`
> interna produce un falso segnale: `16.9 %`, `11.0 %`, e ora questo.

**Verdetto per braccio: 3 × (A), 1 × INDETERMINATO** — e l'indeterminato **non si ripete**.

---

## 5. ⚠ **DUE SEMI NON BASTANO PER UNA BARRA FRA SEMI** — e questo cambia cosa si può dire

Con 2 semi la deviazione standard ha **UN grado di libertà**, e `t(0.025, 1) = 12.706`.
Conseguenza, calcolata:

| | media | dev.std | `SE` | **IC95 (t, 1 gdl)** | contiene il null? |
|---|---|---|---|---|---|
| `chi` mat **OFF** | 89.8268 | 0.0691 | 0.0489 | **[89.206, 90.448]** | **sì** |
| `chi` mat **ON** | 90.0663 | 0.0257 | 0.0182 | **[89.835, 90.298]** | **sì** |
| `chi` p90 **OFF** | 89.6137 | 0.4449 | 0.3146 | **[85.616, 93.611]** | **sì** |
| `\|<n>\|·√N` **OFF** | 0.9985 | 0.3378 | 0.2389 | [−2.04, +4.03] | sì |
| `\|<n>\|·√N` **ON** | 0.4799 | 0.4712 | 0.3332 | [−3.75, +4.71] | sì |

**C'è una regolarità che sembra un segnale, e non lo è (ancora).** `chi` materia è **sotto 90 su
entrambi i semi OFF** (89.778, 89.876) e **sopra 90 su entrambi i semi ON** (90.048, 90.084).
Preso ingenuamente darebbe `z ≈ 3.5` in entrambe le direzioni. **Ma con 1 grado di libertà l'IC95 è
largo 1.2°, e contiene lo zero.**

> **Presidio:** due semi soddisfano il minimo del §2.7 (*mai su un solo seme*) **ma non permettono di
> STIMARE una barra fra semi.** Per quello servono **≥ 4 semi** (`t(3) = 3.18`, quattro volte più
> stretto). **Il segno concorde su 2 semi non è una prova: è un'ipotesi da rifare con 4.**

**Registrato come fronte aperto**, con la sua soglia — non come risultato.

---

## 6. UNA DOMANDA APERTA SI CHIUDE: `|<n>|` **NON pende più**

Stamattina `|<n>|·√N` valeva **1.741** e **1.374** (`z +2.11`, `+1.16`), *sempre dallo stesso lato*, e
l'avevo lasciata **dichiaratamente aperta**. Ora, su quattro run: **1.237 · 0.760 · 0.147 · 0.813**,
`z` da `+0.81` a `−1.99` — **sparsi attorno al null, due sotto e due sopra**.

> **Non si riproduce. Era rumore.** La firma che pendeva **è chiusa come negativa**, e lo è per la
> ragione giusta: **più dati, non una rilettura.**

---

## 7. `cs` — il numero che va aggiornato in C13, **con l'istante**

| | `OFF_s1` | `OFF_s2` | `ON_s1` | `ON_s2` |
|---|---|---|---|---|
| `cs_std` | 0.003837 | 0.004244 | 0.003949 | 0.004847 |
| `cs` | [1.98159, 2.0] | [1.98210, 2.0] | [1.98152, 2.0] | [1.98074, 2.0] |
| **`cs_std/cs_medio`** | **0.193 %** | **0.213 %** | **0.198 %** | **0.244 %** |

**La traiettoria, ed è la lezione di metodo:**

```
passo  50  (n ~ 80)     cs_std/cs = 0.0086 %      margine sotto l'1 % :  116x
passo 300  (n ~ 3000)   cs_std/cs = 0.096  %      margine              :   10x
passo 500  (n ~ 3200)   cs_std/cs = 0.19-0.24 %   margine              :  ~4-5x
```

> **`cs_std/cs` non è una costante del sistema: CRESCE COL SISTEMA.** Un rapporto misurato senza
> dire **a quale passo** non è una soglia, è un'istantanea — e si finisce per citare la più comoda.
> **C13 resta valida** (siamo sotto l'1 %, quindi `tau = d/cs` è ancora `tau ∝ d`), **ma il margine è
> passato da 116× a ~4×**, e la traiettoria è **monotòna crescente**.
> **Conseguenza nuova:** il tempo-luce non è *«non testabile mai»*, è **«non testabile a 500 passi»**.
> A maturazione sufficiente `cs` potrebbe uscire dal regime degenere **senza turbo**.

---

## 8. IL VERDETTO, e cosa rende dicibile

**ESITO (A) — nessuna struttura in nessuno dei due bracci.** E per la lettura fissata **prima**
(`PREDIZIONE` §3-bis): *«niente in nessuno dei due → **(A) NON conclusivo**»*.

**La frase dicibile, per intero:**

> *«Con la doppia copertura a 4π attiva, `cs` dinamico cablato per la prima volta, e il settore
> campionato a 13.7–16.5 giri per passo — 6.4 volte meglio del braccio di riferimento — nessuna delle
> firme misurabili si stacca dal valore casuale: `chi` in materia e nel p90, le frazioni ai poli,
> `|<n>|` contro il null empirico, l'autocorrelazione su 40 bin. Resta indeciso se ciò dipenda
> dall'assenza di ordine o dall'impossibilità di vederlo a questa risoluzione.»*

**Ciò che (A) toglie di mezzo:** l'obiezione *«ma la FASE 5 non era attiva»* e *«ma `cs` era spento»*.
**Entrambe chiuse.** Il negativo è **il più pulito della sessione** — non perché le barre siano
grandi, ma **perché sono piccole** (`SE ≈ 0.09°` su ~210 000 archi) e un segnale sarebbe visibile.

**Ciò che NON toglie:** `theta` è ancora **oltre il giro per passo**. La frase *«lo spin non si
organizza»* **resta indicibile** finché `theta` non scende sotto il tetto `2π·cs/λ`.

---

## 9. COSA QUESTO REFERTO **NON** DICE

- **Non dice che il tempo-luce sia stato testato.** `cs_std/cs = 0.19–0.24 %` → **`tau ∝ d`** (C13).
  Il braccio ON confronta **distanza contro densità**, non tempo-luce contro densità.
- **Non dice che l'aliasing sia risolto.** 13.7–16.5 giri/passo.
- **Non stabilisce la differenza `chi` OFF-vs-ON**, per quanto il segno sia concorde: **2 semi non
  bastano** (§5).
- **Non chiude il fronte R** (l'anello di retroazione sul bersaglio `−0.69`).
