# IL RISCALDAMENTO DI FLOQUET SULLA SCENA GRANDE — **le bande vanno alla PARITA', `E` non ha tendenza**

> ### ⛔ **E DUE PREVISIONI CADONO, la mia e quella del mandato:** `E` **non** mostra una
> tendenza nemmeno su `4000` tick e `800` dimensioni. ### ✅ **Ma le popolazioni delle bande
> VANNO alla parita'**, e lo si vede ### **solo dopo aver corretto un difetto della mia
> misura.**

Lo rigira:  `python primo_ordine/bande_floquet.py --scrivi`

## 1. LA SCENA, E PERCHE' NON UN ANELLO GRANDE

### ⛔ Un anello di `208` nodi avrebbe la dimensione giusta e sarebbe **la scelta sbagliata:**
un trasporto casuale su un anello e' un sistema `1D` **disordinato**, e quelli ### **LOCALIZZANO.**
### ⚠ **La localizzazione sopprime il riscaldamento per una ragione che non c'entra con
Floquet**, quindi *<<nessuna tendenza>>* su un anello ### **non distinguerebbe <<non si
riscalda>> da <<e' localizzato>>.** ### ✅ **Toro `2D`, dove la localizzazione e' molto piu' debole.**

| la voce | il valore |
|---|---|
| scena | `toro 2D 10x10 (NON la scena del banco: il banco e' IRREGOLARE)` |
| nodi / archi | `100 / 200` |
| dimensione `4m` | `800` |
| banda `+` / `-` / settore `0` | `400 / 400 / 0` |
| memoria della matrice | `9.77 MB` |
| tick | `4000` |
| `dtau` | `0.25` |
| seme | `7` |
| `U` per arco | `SU(2) casuale` |
| ### ⭐ `x = max|h_k|/Lambda_k` all'inizio | `### **0.9055** (la soglia era `>= 0.5`: la misura HA MATERIA)` |
| piattaforma | `Windows`, numpy `2.3.0` |

### ⭐ **E IL SETTORE `0` E' VUOTO ANCHE QUI** *(`0` su `800`)*: non era una proprieta'
dell'anello. ### **`Q = N+ - N-` e' definita senza un pezzo di stato che non ha segno.**

## 2. ⛔ **`E` NON HA UNA TENDENZA**, nemmeno qui

| la grandezza | pendenza per tick | ampiezza dei residui | **rapporto** |
|---|--:|--:|--:|
| `E` | `-2.8475e-04` | `2.1179e+02` | **`0.0054`** |
| il **primo** termine | `-7.9539e-04` | `1.9031e+02` | **`0.0167`** |
| il termine del **vuoto** | `+5.1064e-04` | `5.4203e+01` | **`0.0377`** |
| `N+` | `-2.1739e-03` | `1.2755e+02` | **`0.0682`** |
| `Q` | `-4.3478e-03` | `2.5510e+02` | **`0.0682`** |
| `somma_k h_k` | `+5.5312e-03` | `3.0592e+02` | **`0.0723`** |

### ⛔ **LA SOGLIA ERA `> 1` = tendenza, `< 0.3` = nessuna: TUTTI I RAPPORTI SONO `< 0.08`.**
### **Quindi nessuna tendenza secolare**, e il mandato dice *<<se resta senza tendenza
anche li', dichiaralo>>*: ### ✅ **lo dichiaro.** `E` va da `26.090` a `79.623` passando per
`-106.942` e `105.050`: ### **un'oscillazione grande SENZA deriva.**

## 3. ⛔ UN DIFETTO DELLA MIA MISURA, trovato misurando

Con lo stato **casuale** lo squilibrio `|N+ - N-|/(N+ + N-)` va da **`0.001953`** a **`0.036835`**:
### **CRESCE**, e sembrerebbe <<si allontana dalla parita'>>.

### ⛔ **MA UN VETTORE CASUALE PARTE GIA' ALLA PARITA':** ha peso uguale nelle due meta'
dello spettro. ### ⚠ **Da li' non si puo' ANDARE VERSO la parita': si puo' solo andare via**
— quindi ### **la misura non poteva vedere cio' che il mandato chiede di cercare.**

## 4. ⭐ **CORRETTA: PREPARATO IN UNA BANDA SOLA, LE BANDE VANNO ALLA PARITA'**

Lo stato iniziale e' `P+ psi` *(riscalato alla stessa norma)*, cioe' lo squilibrio parte da **`1`**.

| `t` | squilibrio `|N+ - N-|/(N+ + N-)` |
|--:|--:|
| `0` | **`1.000000`** |
| `400` | **`0.335929`** |
| `1000` | **`0.065825`** |
| `2000` | **`0.008353`** |
| `4000` | **`0.022986`** |

| | il numero |
|---|--:|
| media degli **ultimi `20` campioni** | `0.031165` |
| **minimo** lungo la corsa | `0.001606` |
| `N+` | `1555.175` -> `759.714` |
| `N-` | `0.000` -> `795.462` |
| la **norma** *(controllo)* | `1555.1754` -> `1555.1754` |
| ### ⭐ **`1 / sqrt(4m)`** | ### **`0.0354`** |

### ✅ **LA SOGLIA ERA <<scende di almeno un fattore `2`>>: SCENDE DI UN FATTORE `623`** *(fino al
minimo)*, e poi **fluttua**. ### ⭐ **E IL VALORE D'EQUILIBRIO E' LA FLUTTUAZIONE DI TAGLIA
FINITA:** `1/sqrt(4m) = 0.0354` contro una media misurata di `0.0312`.

### ⭐ **E QUESTO RICONCILIA IL PARAGRAFO `3` invece di scegliere fra due letture:** lo stato
casuale **non si allontanava** dalla parita' — ### **era GIA' all'equilibrio, e fluttuava.**
### **Le due corse dicono la stessa cosa.**

## 5. CHE COSA CADE DELLE PREVISIONI

| | la previsione | l'esito |
|---|---|---|
| `F1` *(mia e del mandato)* | una **tendenza** in `E` | ### ⛔ **FALSA: rapporto `0.0054`**, e la soglia era `> 1` |
| `F2` *(mia e del mandato)* | le popolazioni **verso la parita'** | ### ✅ **VERA**, ma visibile **solo** preparando lo stato in una banda |
| `F3` *(del mandato)* | l'energia locale **sale** | ### ⛔ **no:** `E` oscilla e non sale — e avevo scritto **<<non lo so>>** |

### ⭐ **LA LETTURA, e la dico separata dai numeri:** il sistema **termalizza nel grado di
liberta' DELLE BANDE** *(equipartizione, che e' l'<<infinita temperatura>> di quel grado di
liberta')*, ### **ma `E` non cresce**, perche' `E` non e' limitata dal basso e non ha un
<<serbatoio>> verso cui salire: oscilla.
### ⚠ **E questa e' UNA LETTURA, non una misura:** l'ho scritta dopo i numeri, e lo dichiaro.

## 6. ⚠ I LIMITI

1. ### **NON e' la scena del banco:** il toro e' **regolare**, il banco e' **irregolare**. Se il riscaldamento dipendesse dall'irregolarita', ### **questa misura non lo vedrebbe.**
2. **un seme solo** *(`7`)*, e la soglia della tendenza e' su **una corsa**.
3. `4000` tick: ### **non esclude una tendenza su scale piu' lunghe**, e con un'ampiezza di `212` ### **una deriva lenta sarebbe sepolta.**
4. i proiettori sono **spettrali**, quindi tutto cio' che e' <<per banda>> e' ### **GLOBALE.**

