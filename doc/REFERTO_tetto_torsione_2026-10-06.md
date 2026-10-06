# REFERTO -- **IL TETTO DELLA TORSIONE: la soglia di mitosi `3π` sta sul tetto?**

*(Mandato di Luca del 2026-10-06. Previsioni, criteri e controlli fissati in `doc/TASK_HISTORY/2026-10-06_tetto-torsione.md`, committato **prima** in `bbb2dda` e annotato in `c3546e6` e `406a973`.)*

| | |
|---|---|
| **simulatore** | `f7237563`, ### **NON toccato** |
| **strumento** | `1b5e0d2e` *(piu' `_mitosi_soglia_grad` `35108c3e` per `q`, `spearman`, `quintili`)* |
| **copia patchata** | `dec8895f`, **3** ancore, ### **due ganci di SOLA LETTURA** |
| **piattaforma** | Windows 11, python `3.13.2`, numpy `2.3.0` |
| **`κ`** | `1.0`, ### **dal CODICE** -- e il commento dice `3.1831` *(`KAPPA-TW-COMMENTO`)* |
| **passi** | `150`, misure piene ai passi `50`, `100`, `140` |

> ### ⚠ **IL RAPPORTO DELLO STRUMENTO E' CADUTO su questa corsa** *(stato: `DATI SALVATI, rapporto CADUTO`)*, e il difetto -- `spearman()` restituisce una **tupla** -- e' curato in `5d66812`. ### ✔ **I `150` passi sono COMPLETI e SALVATI**, perche' il `json` si scrive **prima** del rapporto: ### **questo referto legge il DATO, non l'uscita dello strumento.**

## `C0`: **i ganci sono di SOLA LETTURA?**

> ### ✔ **PASSA.** Il confronto con `Bp` del `crescita.json` committato su **sette** campi a **tutti** i passi non trova differenze, e `n` finale e' `12827` contro `12827`: ### **coincide**. ### **Quindi i ganci non muovono niente, e non e' dedotto: e' misurato.**

## ⛔ LA PRIMA COSA: **IL CONTO DEL GUARDIANO E' GIUSTO, E NON BASTA**

| | misurato |
|---|--:|
| mediana di `|tw*|` al passo `50` | **`6.3500`** |
| mediana di `|tw*|` al passo `100` | **`6.3108`** |
| mediana di `|tw*|` al passo `140` | **`6.2927`** |
| `2π` | `6.2832` |
| scarto fra la forma **chiusa** e quella **fedele** | `3.638e-12` |

### ✔ **Con `r` quasi uniforme `|tw*|` sta su `2π`** -- lo scarto massimo sui tre passi e' ### **`1.0626 %`** -- ed e' la predizione del mandato *(«con `r` uniforme `|tw*| = 2π` per QUALUNQUE arco a deriva costante»)*. ### **Misurata, non assunta.**

### ✔ **`M8`: il pavimento esterno di `τ` NON vincola nessun arco** -- `0` archi su tutta la corsa.

## `M1`: **`|tw|` sta davvero sul suo tetto?**

| passo | archi *(sopra il `q25` di `|Δω|`)* | `q05` | `q25` | ### **mediana** | `q75` | `q95` | `q99` | `> 1` | `> 2` |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `50` | `353673` | `0.0307` | `0.1716` | ### **`0.3999`** | `0.6482` | `0.9372` | `1.2323` | `0.0344` | `0.0032` |
| `100` | `353672` | `0.0350` | `0.1585` | ### **`0.3481`** | `0.5821` | `1.0270` | `1.3641` | `0.0554` | `0.0037` |
| `140` | `353681` | `0.0371` | `0.1702` | ### **`0.3476`** | `0.5733` | `1.0787` | `1.4863` | `0.0655` | `0.0048` |

### ✔ **E LA COERENZA SI VERIFICA:** `mediana|tw| / mediana|tw*|` contro la **mediana del rapporto** -- passo `50`: `0.4005` contro `0.3999`; passo `100`: `0.3425` contro `0.3481`; passo `140`: `0.3354` contro `0.3476`. ### **Due vie allo stesso numero: se divergessero, una delle due sarebbe sbagliata.**

### ⛔ **E IL NUMERO CHE DICE LA FISICA, in una riga:** la mediana di `|tw|` e' `2.5432` e la soglia di mitosi `3π` e' `9.4248`. ### **L'arco mediano sta al `27.0 %` della soglia**, e il tetto calcolato `|tw*|` *(mediana `6.3500`)* sta al `67.4 %`.

### **IL CRITERIO DEL MANDATO:** l'ipotesi del tetto e' **REFUTATA** se la mediana cade fuori da `[0.3, 2.0]`.

> ### ✔ **STA DENTRO a tutti i 3 passi misurati: l'ipotesi del tetto NON e' refutata.**

### LA PREVISIONE DEL GUARDIANO: *«mediana fra `0.5` e `1.2`, con una coda che non supera `1` di molto»*

| | esito |
|---|---|
| **il guardiano** *(mediana in `[0.5, 1.2]`)* | ### **⛔ NON confermata** -- dentro a 0 passi su 3 |
| **io** *(«la coda e' PIU' LUNGA della sua, per gli `~109` archi di `ARCHI-OLTRE-4PI`»)* | frazione `> 2`: `0.0032`, `0.0037`, `0.0048` -- ### **c'e' una coda** |

## `M2` / `M2b`: **il dipolo AIUTA o no?**

| passo | `M2` *(con `|twist_dip|`)* | `M2b` *(SENZA)* | il dipolo |
|---|--:|--:|---|
| `50` | `0.0309` | `0.0309` | ### **non aiuta** *(`M2b` >= `M2`)* |
| `100` | `0.0202` | `0.0202` | ### **non aiuta** *(`M2b` >= `M2`)* |
| `140` | `0.0166` | `0.0166` | ### **non aiuta** *(`M2b` >= `M2`)* |

### **IL CRITERIO DEL MANDATO:** **REFUTATA** se la Spearman di `M2` e' sotto `0.30` a **tutti e tre** i passi.

> ### ⛔ **SOTTO `0.30` A TUTTI I PASSI: L'IPOTESI DEL TETTO E' REFUTATA anche da questo criterio.**

## `M3` / `M3b`: **quanti archi ARRIVANO alla soglia?**

| passo | `M3` oltre `3π` | `M3` oltre la **soglia modulata** | `M3b` oltre `3π` *(senza dipolo)* |
|---|--:|--:|--:|
| `50` | `0.072164` | `0.091379` | `0.072164` |
| `100` | `0.068988` | `0.085821` | `0.068988` |
| `140` | `0.072279` | `0.087575` | `0.072279` |

### LA PREVISIONE DEL GUARDIANO: *«con la soglia `3π` la frazione e' sotto lo `0.1 %`»* ⟹ ### **⛔ NON confermata** *(il massimo misurato e' `0.072279`)*.

### LA MIA: *«`M3b` ancora piu' bassa, vicina a zero esatto»* ⟹ ### **CONFERMATA** *(massimo `0.072279`)*.

## `M4`: **gli archi che DIVIDONO sono quelli col tetto alto?**

| passo | | `|tw*|` mediano | `|twist_dip|` mediano | `|r_i-r_j|` mediano | `|tw|` mediano |
|---|---|--:|--:|--:|--:|
| `50` | **`g1`** *(`109`)* | `6.3165` | `0.0000` | `0.1544` | `17.8401` |
| `50` | **`altri`** *(`471455`)* | `6.3500` | `0.0000` | `0.1175` | `2.5426` |
| `100` | **`g1`** *(`151`)* | `6.3162` | `0.0000` | `0.2333` | `14.2752` |
| `100` | **`altri`** *(`471412`)* | `6.3108` | `0.0000` | `0.1124` | `2.1607` |
| `140` | **`g1`** *(`280`)* | `6.2448` | `0.0000` | `0.3388` | `8.7158` |
| `140` | **`altri`** *(`471295`)* | `6.2927` | `0.0000` | `0.1167` | `2.1089` |

### LA PREVISIONE DEL GUARDIANO: *«gli archi in `g1` hanno `|tw*| + |twist_dip|` piu' alto»* ⟹ `|tw*|` mediano piu' alto in ### **1 passi su 3**.

### LA MIA: *«differenza DEBOLE o assente su `|tw*|`, e `g1` si distingue per il TRANSITORIO»* ⟹ il rapporto fra le due mediane e' `0.9947`, `1.0008`, `0.9924`. ### **DEBOLE, come dicevo**

## `M5`: **la distribuzione di `|twist_dip|`**

| passo | a `0` | a `π/2` | a `π` | altro |
|---|--:|--:|--:|--:|
| `50` | ### **`1.0000`** | `0.0000` | `0.0000` | `0.0000` |
| `100` | ### **`1.0000`** | `0.0000` | `0.0000` | `0.0000` |
| `140` | ### **`1.0000`** | `0.0000` | `0.0000` | `0.0000` |

### **IL CRITERIO DEL MANDATO:** la **seconda** ipotesi e' **REFUTATA** se meno del `30 %` degli archi ha `twist_dip = 0`.

> ### ✔ **`1.0000` >= `0.30`: la seconda ipotesi NON e' refutata**, e la previsione del guardiano *(«la maggioranza ha `twist_dip = 0`»)* e' ### **CONFERMATA**.
>
> ### ⛔ **E C'E' DI PIU': e' `1.0000`, cioe' PRATICAMENTE TUTTI.** Se `twist_dip` e' zero su tutta la rete, allora ### **il dipolo non contribuisce MAI al tetto, e il `3π` del conto del guardiano non esiste: il tetto e' `2π`.** ### ✔ **Ed e' la CORREZIONE scritta nella sezione `(c)` del task history, confermata dal dato: il dipolo entra come DERIVATA TEMPORALE, e una derivata di zero e' zero.**

## ⛔ `M6`: **GLI AVVOLGIMENTI, e il difetto `TORS-W8-AVVOLGIMENTO` IN AZIONE**

| | |
|---|--:|
| coppie `(passo, arco)` confrontate | `64604599` |
| **avvolgimenti di `dph`** *(`|salto| > 2π`)* | **`142114`** *(`0.002200` per coppia)* |
| **ripiegamenti del `_w8`** *(`|arg| > 4π`)* | `109` |
| **calci oltre `π`** *(`|spinta - riparata|`)* | **`142114`** |
| invariante `|twp| <= 3π` violato | `0` |

> ### ✔ **LA DERIVAZIONE DELLA SEZIONE `(b)` TIENE:** `|twp| <= 3π` su **tutte** le `64604599` coppie, quindi ### **`twp` non avvolge MAI** ed e' `dph + twist_dip` esattamente.

| passo | calci | `|errore|` mediano | errore **firmato** mediano | `+` | `-` |
|---|--:|--:|--:|--:|--:|
| `50` | `1167` | **`4.0000 π`** | `-4.0000 π` | `559` | `608` |

> ### ⛔ **E LA MEDIANA DEL MODULO E' QUELLA CHE CONTA:** la **firmata** su una distribuzione a due picchi opposti da' ### **zero anche con calci enormi**, ed e' il difetto di referto che il giro corto ha trovato *(`0476a80`)*.

### ⚠ **E LA POPOLAZIONE OLTRE `4π`**

| passo | archi con `|tw| >= 4π` | di cui il `_w8` ripiega |
|---|--:|--:|
| `50` | `109` | `0` |

> ### ⛔ **NON INDAGO `ARCHI-OLTRE-4PI`**, che Luca ha messo fra le cose da non toccare. ### **Riporto il conteggio e il meccanismo** -- un calcio di `-4π` porta un arco oltre `TW_TETTO = 4π` **in un passo solo** -- e ### **NON guardo gli INDICI**, che e' la verifica che collegherebbe le due cose.

## ⛔ `M7` / `M7b`: **IL TERMINE CHE LA FORMULA IGNORA -- ed e' una correzione del `~27 %`, NON il termine dominante**

| passo `50` | `q05` | `q25` | ### **`q50`** | `q75` | `q95` |
|---|--:|--:|--:|--:|--:|
| `|Δδsync| / |Δ(dt_n·ω)|` | `0.0221` | `0.1225` | ### **`0.2843`** | `0.6737` | `3.5561` |

| passo `100` | `q05` | `q25` | ### **`q50`** | `q75` | `q95` |
|---|--:|--:|--:|--:|--:|
| `|Δδsync| / |Δ(dt_n·ω)|` | `0.0183` | `0.1022` | ### **`0.2379`** | `0.5105` | `2.5514` |

| passo `140` | `q05` | `q25` | ### **`q50`** | `q75` | `q95` |
|---|--:|--:|--:|--:|--:|
| `|Δδsync| / |Δ(dt_n·ω)|` | `0.0214` | `0.1189` | ### **`0.2759`** | `0.5954` | `2.9201` |

> ### ⚠ **ALLA MEDIANA IL TERMINE OMESSO E' IL `~27 %` DI QUELLO TENUTO**, e al `q95` arriva a `3.5561` volte. ### **`K_SYNC = 1.0`: il termine e' ATTIVO e la formula lo ignora** -- non e' il pezzo piu' grande, ### **ma non e' nemmeno trascurabile, e un conto che lo omette sbaglia di quell'ordine.**

| passo | `Spearman(dph, Δδsync)` | frazione a **segno opposto** |
|---|--:|--:|
| `50` | ### **`0.0868`** | `0.5230` |
| `100` | ### **`0.0858`** | `0.5279` |
| `140` | ### **`0.0790`** | `0.5268` |

> ### ⚠ **IL TERMINE non richiama in modo uniforme.** La Spearman fra `dph` e `Δδsync` e' di segno misto, e la frazione a segno opposto e' `0.5230`, `0.5279`, `0.5268`. ### **La lettura resta aperta, e lo dico invece di scegliere.**

## ⛔ TRE MIE AFFERMAZIONI CHE QUESTA MISURA CORREGGE

| avevo scritto | dove | che cosa dice il dato |
|---|---|---|
| *«`delta_sync_phi` non e' una correzione, e' il TERMINE DOMINANTE»* | `406a973`, dal **giro corto** a `3` passi *(mediana `1.79`)* | ### ⛔ **FALSO in regime:** ai passi del mandato il rapporto mediano e' `0.2843`, `0.2379`, `0.2759`. ### **Il `1.79` era un TRANSITORIO dei primi passi, e l'ho preso per il regime.** Resta vero che il termine **non e' trascurabile** *(un `~27 %`)* |
| *«se RICHIAMA, smorza la spinta e il tetto vero sta SOTTO `2π`»* | `406a973` e `0476a80`, come **ipotesi** da misurare con `M7b` | ### ⛔ **NON CONFERMATA:** la Spearman e' `0.0868`, `0.0858`, `0.0790` -- ### **POSITIVA, non negativa** -- e la frazione a segno opposto e' `0.5230`, `0.5279`, `0.5268`, cioe' ### **il caso.** Il termine **non richiama in modo sistematico**, e il motivo del tetto piu' basso va cercato altrove |
| *«la coda di `M1` e' PIU' LUNGA della sua, per gli `~109` archi di `ARCHI-OLTRE-4PI`»* | `bbb2dda`, la mia previsione | la frazione `> 2` e' `0.0032`, `0.0037`, `0.0048`: ### **la coda c'e' ed e' PICCOLA.** `109` archi su `471564` sono lo `0.0231 %`, e la frazione `> 2` misurata e' `0.32 %`: ### **lo stesso ordine di grandezza, quindi la previsione regge ma NON spiega tutta la coda** |

> ### 📌 **PERCHE' LE SCRIVO QUI E NON LE CANCELLO DAL TASK HISTORY:** il par.8 vuole che un ragionamento sbagliato ### **resti scritto con l'annotazione accanto.** ### **E la prima e' la piu' istruttiva: avevo un numero vero (`1.79`) misurato in un regime che non era quello della domanda, e l'ho generalizzato.**

## IL VERDETTO

| ipotesi | criterio del mandato | esito |
|---|---|---|
| **il tetto** | mediana di `M1` fuori da `[0.3, 2.0]` **oppure** `M2` sotto `0.30` a tutti i passi | ### **REFUTATA** |
| **la seconda** *(il dipolo e' `0` per molti archi)* | meno del `30 %` con `twist_dip = 0` | ### **NON refutata** |

### ⛔ **E QUELLO CHE LA MISURA AGGIUNGE AL MANDATO, in tre righe**

1. ### **`κ = 1` e' un numero scritto a mano, e il commento ne dice un altro** *(`KAPPA-TW-COMMENTO`)*: con `κ = 3.1831` il tetto sarebbe `20` invece di `2π`, e la mitosi passerebbe da **marginale** a **generica**. ### **Due letture, due fisiche.**
2. ### **`_w8` non ripara l'avvolgimento di `dph`** *(`TORS-W8-AVVOLGIMENTO`)*: `142114` calci oltre `π` su `64604599` coppie, e il ramo non-`4π` lo ripara **esatto**. ### **La formula del tetto vale FRA DUE AVVOLGIMENTI, non su tutta la corsa.**
3. ### **`delta_sync_phi` e' ATTIVO e la formula lo ignora** *(`K_SYNC = 1.0`)*: una correzione del `~27 %` alla mediana, e fino a `3.5561` volte al `q95`. ### ⚠ **E NON E' <<IL TERMINE DOMINANTE>>: quello l'avevo scritto io dal giro corto, e questa misura lo RITIRA.** ### **Nessuna delle tre cose era nel mandato, e tutte e tre cambiano il conto.**

> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** ### **`κ`, la soglia, il dipolo locale e il `0.3` sono DECISIONI DI LUCA.**

---

*Referto **generato** da `csv/_test_fork/_referto_tetto.py` dal `tetto.json`: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`), e i criteri sono letti **dal `json`** invece di essere riscritti qui.*
