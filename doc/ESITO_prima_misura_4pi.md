# ESITO — prima misura del settore spinoriale su sistema PULITO — **BRACCIO OFF: (A)**

> **⚠ DOCUMENTO PARZIALE — copre il solo braccio `--tau-luce` OFF.** Il mandato è stato corretto
> **a metà lavoro**: la misura va fatta a **DUE bracci** (gradiente di risoluzione), perché
> `--tau-luce` non è un forzante ma una **correzione di legge**, ed è l'unica cosa che abbassa
> `theta`. **Il braccio ON è in corso.** La lettura a due bracci è fissata in
> `doc/PREDIZIONE_prima_misura_4pi.md` §3-bis, **scritta prima del run ON**.
> Qui sotto: il braccio OFF, che resta la **baseline certificata** (i sigilli della FASE 2 non sono
> passati, il gate non è ri-timbrato).

**Data:** 2026-09-15 · **Branch:** `fork-su2` · **Blob:** `08784685` (dal disco) · **2 semi, 500 passi**
Predizione committata **prima** del run: `doc/PREDIZIONE_prima_misura_4pi.md` (`c547294`).
Soglie in codice, committate **prima** di girare: `csv/_test_fork/_verdetto_4pi.py` (`c8cd9d1`).
Dati: `csv/_test_fork/_vuoto_pulito{1,2}_s{1,2}.vuoto.csv` · Verdetto: `_verdetto_4pi.txt`.

---

## 0. IL VERDETTO IN UNA RIGA

> **BRACCIO OFF — ESITO (A) su entrambi i semi. Nessuna firma si stacca dal valore casuale.**
> **E `theta` è a 92.8–98.7 GIRI per passo: il settore è ALIASATO, e queste cure non lo risolvono.**
> **Per la lettura a due bracci serve il braccio ON: (A) su un solo braccio non è il verdetto.**

---

## 1. LE FIRME, col valore-null accanto

**Valore-null di `chi`** (direzioni di Bloch casuali, `CLAUDE.md` §9): **`90.000° ± 39.171°`**.

| | seme 1 | seme 2 |
|---|---|---|
| `chi` **materia** | **89.9682°**, `std 39.1119`, `n 209846`, `SE 0.0854` → **`z = −0.37`** | **90.0639°**, `std 39.1950`, `n 209120`, `SE 0.0857` → **`z = +0.75`** |
| `chi` **p90** | **90.0210°**, `SE 0.1499` → **`z = +0.14`** | **90.1174°**, `SE 0.1677` → **`z = +0.70`** |
| `chi` **vuoto** | 93.0216°, `n 869`, `SE 1.34` → `z = +2.25` | 91.7664°, `n 808`, `SE 1.43` → `z = +1.23` |
| frazione `chi < 10°` | 0.00745 | 0.00763 |
| frazione `chi > 170°` | 0.00744 | 0.00773 |

Le due frazioni ai poli degeneri sono **uguali fra loro entro il terzo decimale** su entrambi i semi:
è la firma di una distribuzione **simmetrica attorno a 90°**, cioè isotropa. Un ordinamento
produrrebbe un eccesso a `<10°`; un'antiallineazione a `>170°`. **Nessuno dei due.**

**Autocorrelazione spaziale `<n_i·n_j>` — la firma che DISCRIMINA.**
Dieci bin di distanza, `max|z| = 1.80` (seme 1) e `1.09` (seme 2), **su dieci bin ciascuno**: con 20
bin totali, un `|z| ~ 1.8` è quello che il caso produce. **Piatta a zero a ogni distanza, da 0.57 a
15.0.** Non decade a scala finita (sarebbe **B**), non resta alta (sarebbe **C**): **non c'è.**

---

## 2. L'UNICA COSA CHE PENDE — e non raggiunge la significatività

`|<n>|` è sopra il valore casuale su **entrambi** i semi: rapporti **1.741** e **1.374**.

**Ma il valore-null che l'osservatore stampa è `1/√N`, che è la SCALA, non l'ATTESA.**
Misurato (non asserito) con 4000 estrazioni di `N` versori casuali per ciascun `N` reale:

```
N = 3143   |<n>|*sqrt(N):  media 0.9138  std 0.3830  p95 1.5806
N = 3708   |<n>|*sqrt(N):  media 0.9168  std 0.3854  p95 1.5954
```

> **L'attesa vera è `0.921/√N`, con `std 0.389/√N`.** Contro quella: **`z = +2.11`** (seme 1, sopra il
> **p95** del nullo) e **`z = +1.16`** (seme 2, dentro). **Media `z = +1.64`.**

**Non è un risultato.** Due semi, uno sopra il p95 e uno dentro, con `z` medio sotto 2. È **l'unica
firma che pende sempre dallo stesso lato**, e per questo va **annotata e riguardata**, non annunciata.
*(La soglia della predizione — «rapporto `< 2`» — era tarata su `1.0` invece che su `0.921`: un po'
generosa. (A) regge comunque, perché richiede `z < 3` e qui siamo a `1.64`.)*

---

## 3. ⚠ UNA CORREZIONE ALLA MIA PREDIZIONE: l'aliasing è il DOPPIO di quanto avevo scritto

La predizione dice *«`theta` resta a ~43 giri/passo»*. **Misurato: 98.65 e 92.81.**

**L'errore:** il `43` viene dal braccio `ON` di T3, cioè **con `--tau-luce` cablato**. Questi run —
come il mandato chiede — girano il sistema **naturale**, senza `--tau-luce`. **Il valore naturale è
~96 giri/passo, più del doppio.** Avevo trasportato un numero da una configurazione a un'altra.

**Non cambia il verdetto, peggiora il caveat**, e va detto nella stessa riga:

| | seme 1 | seme 2 |
|---|---|---|
| `theta` mediana | **98.65 giri/passo** | **92.81 giri/passo** |
| frazione nodi `> 30°/passo` | **0.9978** | **0.9997** |
| frazione nodi `> 360°/passo` (oltre il giro intero) | **0.9841** | **0.9943** |

**Il 98–99 % dei nodi compie più di un giro intero per passo.**

---

## 4. CHE COSA (A) RENDE DICIBILE — e cosa no

Il caveat era scritto **prima dei dati** (`PREDIZIONE` §1) e resta:

> **(A) è l'esito che l'aliasing produrrebbe DA SOLO.** Sotto sotto-campionamento di un fattore ~96,
> due nodi appaiono scorrelati **anche se la dinamica li sta ordinando**. (A) è compatibile con
> *«non c'è ordine»* **e** con *«c'è ordine e non lo vediamo»*: **non separa le due.**

**La frase dicibile, per intero:**

> *«Con la doppia copertura a 4π attiva per la prima volta, e il settore campionato a ~96 giri per
> passo, nessuna delle firme misurabili — `chi` in materia e nel p90, le frazioni ai poli,
> l'autocorrelazione su dieci bin — si stacca dal valore casuale. Resta indeciso se ciò dipenda
> dall'assenza di ordine o dall'impossibilità di vederlo a questa risoluzione.»*

**E ciò che (A) SÌ toglie di mezzo:** l'obiezione *«ma la FASE 5 non era attiva»* — quella che
rendeva i sei lati precedenti **non conclusivi** — **è chiusa.** La doppia copertura ora gira
(95.33 % → 0.00 %). Il negativo è **più pulito di prima**; non è **conclusivo**.

**E resta l'asimmetria dichiarata prima:** l'aliasing **distrugge** segnale, non lo crea. Se fosse
uscito (B), sarebbe stato vero e sottostimato. Un'assenza, no.

---

## 5. LA BARRA CHE CONTA — quella FRA SEMI, non quella interna

Per **C10** (`doc/RAMIFICAZIONI.md`), su questo sistema caotico la `SE` interna sottostima.

| grandezza | seme 1 | seme 2 | media | **dev.std FRA SEMI** |
|---|---|---|---|---|
| `chi` materia (gradi) | 89.96822 | 90.06393 | 90.01608 | **0.0677** |
| `\|<n>\|` | 0.02859 | 0.02450 | 0.02655 | **0.00289** |
| `theta` (giri/passo) | 98.652 | 92.813 | 95.733 | **4.129** |
| dispersione di `r` | 0.47494 | 0.42181 | 0.44838 | **0.03757** |

**Su `chi` la dispersione fra semi (0.068°) è ~0.8 volte la `SE` interna (0.085°)** — qui le due
coincidono, perché `n_archi ~ 210 000` rende la `SE` interna già piccolissima. **Non è una smentita
di C10:** C10 riguardava una **pendenza** su ~2500 nodi, non una media su 210 000 archi.
**La regola resta: si guarda quale delle due è più grande, non si sceglie la più comoda.**

---

## 6. `r`: si riporta la DISPERSIONE, mai la mediana

`r_mediana = 1.000000` su entrambi i semi — **come deve essere, per costruzione**: `ritmo()` fa
`x = f/median(|f|)` con mappa monotona (presidio in `CLAUDE.md` §9). È stampata **solo come
controllo che il presidio sia vero**, non come misura.

Le misure sono: **`std` 0.4749 / 0.4218**, **`IQR` 0.8799 / 0.7658**. `r` **varia molto** fra i nodi
— i tempi propri locali sono tutt'altro che uniformi — e questo **con la FASE 5 attiva**.

---

## 7. COSA QUESTA MISURA NON DICE

- **⚠ `--cs-dinamico` era SPENTO, e ora è DIMOSTRATO, non dedotto** (`doc/REPERTO_cs_dinamico_spento.md`,
  rilievo di Luca). Prova dai dati: `cs_std = cs_min = cs_max = **nan**` su tutti gli 11 campioni di
  entrambi i semi — e `nan` è più forte di `0`: significa che la cache `_cs_nodo_prev` **non esiste
  affatto**, e quella cache è scritta **solo** dentro `if CS_DINAMICO:`. Seconda prova indipendente:
  `CS_DIN=False` nella riga `[osserva-flag]` letta **in-run** su entrambi i semi.
  **Quindi `cs = CS_M` costante**, la cura della cache `cs` è **inerte** in questi run, e si è
  esercitato **l'orologio a 4π**, non il tempo-luce.
  **MA ATTENZIONE, e vale anche per i run futuri:** accendere il flag **non cambierebbe la sostanza**.
  Dove `cs` era acceso, `cs ∈ [1.99954, 2.0]` mentre `tau = d/cs ∈ [0.0271, 1.0509]`: **`cs` pesa
  `0.00629 %` della dispersione di `tau`, una parte su 15 898.** `tau = d/cs` è **`tau ∝ d`** a due
  parti su diecimila, **anche col flag acceso**.
- **Non dice che l'aliasing sia risolto.** Non lo è: ~96 giri/passo.
- **Non chiude il fronte R** (l'anello di retroazione: forse è il bersaglio `−0.69` a essere mal
  calcolato). Richiede `sigma` misurato nello stesso run.
- **500 passi**, non 2000: è il limite scelto per avere **due semi** invece di uno lungo, dato che
  §2.7 vieta le conclusioni su un solo seme. **Dichiarato, non nascosto.**
