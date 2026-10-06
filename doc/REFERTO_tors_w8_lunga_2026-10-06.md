# REFERTO -- **`TORS-W8-AVVOLGIMENTO`: LA MISURA LUNGA, `1000` passi**

*(Mandato di Luca del 2026-10-06. Previsioni, **limite della curva** e criterio sono fissati in `doc/TASK_HISTORY/2026-10-06_tors-w8-misura-lunga.md`, committato ### **prima** in `7d3ae67`.)*

| | |
|---|---|
| **simulatore** | `cf2a1ac8` -- ### **verificato all'avvio** contro `cf2a1ac8`, e su un blob diverso lo strumento **si ferma** |
| **strumento** | `bc62bcaa` *(piu' `_mitosi_soglia_grad` `1279c6fb`)* |
| **copia patchata** | `2a7fa5a8`, **3** ancore, ### **due ganci di SOLA LETTURA** |
| **piattaforma** | Windows 11, python `3.13.2`, numpy `2.3.0` |
| **configurazione del driver** | dichiarata INTERA: `True` |
| **scena** | `n` iniziale, archi e `DT` come il driver; un braccio, seme `11` |

## ⛔ IL CRITERIO, **letto SOLO dove si puo' leggere**

Il task history ha fissato ### **prima della corsa** che il rapporto `|tw| mediano / 2π·(1 − e^(−t/300))` si legge ai passi ### **`300`, `600`, `1000`**, dove `τ` e' vicino a `300`, e che ai passi `50` e `150` ### **si riporta ma NON decide** -- perche' li' il `τ` vero vale `309`-`1491` e il rapporto e' gonfiato ### **per costruzione.**

| passo | `|tw|` mediano | la curva | ### **rapporto** | lettura | |
|--:|--:|--:|--:|---|---|
| `50` | `1.3967` | `0.9646` | ### **`1.4479`** | *(DENTRO)* | non decide |
| `150` | `2.2829` | `2.4722` | ### **`0.9234`** | *(DENTRO)* | non decide |
| `300` | `2.7026` | `3.9717` | ### **`0.6805`** | ### **DENTRO** | ### **DECIDE** |
| `600` | `3.4243` | `5.4328` | ### **`0.6303`** | ### **DENTRO** | ### **DECIDE** |
| `1000` | `3.9151` | `6.0590` | ### **`0.6462`** | ### **DENTRO** | ### **DECIDE** |

> ### ✔ **I 3 PASSI CHE DECIDONO DANNO LA STESSA LETTURA: `DENTRO` -- accumula come previsto.**

| il rapporto | la lettura, fissata PRIMA |
|---|---|
| sotto `0.5` | **la deriva NON e' coerente: la torsione NON accumula** |
| fra `0.5` e `1.5` | **accumula come previsto** |
| sopra `1.5` | **c'e' una spinta che il conto non vede** |

## LA CURA TIENE? **i tre contatori dei calci**

| | | |
|---|--:|---|
| **calci SPURI** dalla legge curata *(`|spinta|` oltre il bound `4π`)* | `0` | ### **ZERO** |
| **la FIRMA del difetto vecchio** *(spinta `> 3π` **senza** un dipolo che cambi)* | `0` | ### **ZERO** |
| **calci EVITATI** *(quanti la legge **vecchia** avrebbe dato)* | ### **`1586016`** | *un CONTROFATTUALE: il suo valore giusto **non** e' zero* |
| archi con `|tw| >= 4π`, somma su tutti i passi | `29357` | ### **⚠ NON ZERO: una SCOPERTA, non un guasto -- vedi sotto** |

> ### ⛔ **E I PRIMI DUE ZERI SONO ALGEBRICI, non misure, e va detto:** il bound `|spinta| <= |_w4(Δdph)| + |Δdipolo| <= 4π` vale ### **per costruzione**, misurato su `10^6` casi *(massimo `12.566155` contro `4π = 12.566371`: il bound e' **stretto**)*. ### **Quello che certificano e' che l'IMPLEMENTAZIONE segue l'algebra**, non che la fisica non e' cambiata -- ### **la stessa famiglia e lo stesso potere di `S3` del sigillo.**
>
> ### ✔ **IL NUMERO CHE DICE QUALCOSA E' <<calci EVITATI>>:** `1586016` calci di modulo `~4π` che la legge vecchia avrebbe dato e la curata ### **non da'.**

## IL CONFRONTO con `f7237563` *(i numeri GIA' committati)*

| | legge **vecchia** a `150` passi | legge **curata** |
|---|--:|--:|
| divisioni | `18` | `0` a `150`, ### **`3496` a `1000`** |
| Schwinger | `7` | `0` a `150`, ### **`1265` a `1000`** |
| `|tw|` mediano al passo `140` | `2.11` | ### **`2.2223`** |
| archi oltre `4π` ### **all'ULTIMO passo** *(non la somma)* | `~108` a `150` | ### **`368` a `1000`** |
| ### **la FRAZIONE** sugli archi esistenti | `0.000229` *(a `150`)* | ### **`0.000771`** |
| la **somma** su tutti i passi | *(non misurata)* | `29357` |
| calci di modulo `~4π` | `142114` in `150` passi | ### **`0` dati, `1586016` EVITATI** |

## LE NASCITE, **per finestre di `50` passi**

### **Non il totale:** con `1000` passi un totale nasconderebbe ### **QUANDO** la rete cresce, e *«quando»* e' la domanda.

| finestra | divisioni | Schwinger | `n` a fine | archi a fine |
|---|--:|--:|--:|--:|
| `1`-`50` | **`0`** | `0` | `12802` | `471564` |
| `51`-`100` | **`0`** | `0` | `12802` | `471564` |
| `101`-`150` | **`0`** | `0` | `12802` | `471564` |
| `151`-`200` | **`0`** | `0` | `12802` | `471564` |
| `201`-`250` | **`25`** | `8` | `12835` | `471601` |
| `251`-`300` | **`75`** | `35` | `12945` | `471746` |
| `301`-`350` | **`99`** | `30` | `13074` | `471905` |
| `351`-`400` | **`127`** | `42` | `13243` | `472114` |
| `401`-`450` | **`119`** | `39` | `13401` | `472312` |
| `451`-`500` | **`152`** | `64` | `13617` | `472590` |
| `501`-`550` | **`224`** | `86` | `13927` | `472984` |
| `551`-`600` | **`252`** | `87` | `14266` | `473415` |
| `601`-`650` | **`207`** | `56` | `14529` | `473734` |
| `651`-`700` | **`273`** | `92` | `14894` | `474185` |
| `701`-`750` | **`286`** | `109` | `15289` | `474690` |
| `751`-`800` | **`297`** | `97` | `15683` | `475178` |
| `801`-`850` | **`267`** | `108` | `16058` | `475657` |
| `851`-`900` | **`333`** | `128` | `16519` | `476246` |
| `901`-`950` | **`362`** | `135` | `17016` | `476879` |
| `951`-`1000` | **`398`** | `149` | `17563` | `477575` |

### ➜ **Le prime tre finestre danno `0` divisioni, le ultime tre `1093`:** ### **la crescita ACCELERA**

## ⛔ QUANDO: **il primo arco oltre `4π`, e le prime nascite**

| | il passo |
|---|--:|
| la prima **divisione** | `214` |
| il primo **Schwinger** | `215` |
| ### **il primo arco oltre `4π`** | ### **`218`** |
| il **massimo** di archi oltre `4π`, e dove | `368`, al passo `1000` |


### E COME CRESCE, perche' un massimo da solo non dice se si e' fermato

| passo | archi oltre `4π` | la **frazione** | archi |
|--:|--:|--:|--:|
| `100` | ### **`0`** | `0.000000` | `471564` |
| `200` | ### **`0`** | `0.000000` | `471564` |
| `218` | ### **`1`** | `0.000002` | `471569` |
| `300` | ### **`6`** | `0.000013` | `471746` |
| `400` | ### **`1`** | `0.000002` | `472114` |
| `500` | ### **`3`** | `0.000006` | `472590` |
| `600` | ### **`7`** | `0.000015` | `473415` |
| `700` | ### **`13`** | `0.000027` | `474185` |
| `800` | ### **`23`** | `0.000048` | `475178` |
| `900` | ### **`100`** | `0.000210` | `476246` |
| `1000` | ### **`368`** | `0.000771` | `477575` |

### ➜ ⛔ **IL MASSIMO E' L'ULTIMO PASSO: la misura si ferma MENTRE la popolazione SALE**, quindi ### **non si sa se si assesti.** ### **Dire <<il massimo e' `368`>> senza dire QUESTO sarebbe far credere che la curva si sia appiattita.** ### **Quanti passi servano e' una DECISIONE DI LUCA.**

> ### ⚠ **E IL CONFRONTO CON LA LEGGE VECCHIA NON SI PUO' FARE A `1000` PASSI:** i `~108` della legge vecchia sono misurati a ### **`150` passi**, e la legge vecchia ### **non e' mai stata girata a `1000`.** ### **A PARITA' DI ORIZZONTE il confronto e' `0` contro `~108`, e QUELLO e' pulito** -- un rapporto fra `1000` passi e `150` ### **non dimostra che la cura abbia peggiorato le cose.**

### ➜ **IL PRIMO ARCO OLTRE `4π` ARRIVA `4` PASSI DOPO LA PRIMA NASCITA**, e ### **non prima.** ⚠ **E' una COINCIDENZA, non una prova:** servirebbero gli ### **INDICI** degli archi sopra `4π` contro quelli ### **nati**, e questa misura non li registra.

## `M2`: **il tetto calcolato ordina gli archi?**

| passo | `M2` *(con `|twist_dip|`)* | `M2b` *(senza)* | `|tw*|` mediano | frazione oltre `3π` | frazione oltre la **soglia modulata** |
|--:|--:|--:|--:|--:|--:|
| `50` | `0.0092` | `0.0092` | `6.3404` | `0.067138` | `0.083287` |
| `150` | `-0.0310` | `-0.0310` | `6.2899` | `0.072151` | `0.086847` |
| `300` | `-0.0246` | `-0.0278` | `6.3068` | `0.092826` | `0.114556` |
| `600` | `-0.0014` | `-0.0197` | `6.3191` | `0.105230` | `0.128588` |
| `1000` | `0.0112` | `-0.0204` | `6.3116` | `0.112635` | `0.132193` |

### ➜ **La `Spearman` sta fra `-0.0310` e `0.0112`:** ### **il tetto calcolato NON ordina gli archi**, ed e' lo stesso risultato di `eebe24f` *(`0.031` / `0.020` / `0.017`)* ### **con la legge CURATA e su `1000` passi.**

## `τ_tw/dt_e`: **il tempo di scarica, in PASSI**

| passo | `q25` | ### **`q50`** | `q75` | il `τ` della curva |
|--:|--:|--:|--:|--:|
| `50` | `151.2` | ### **`285.6`** | `659.3` | `300` |
| `150` | `144.6` | ### **`262.6`** | `572.4` | `300` |
| `300` | `128.2` | ### **`228.4`** | `492.4` | `300` |
| `600` | `98.5` | ### **`177.1`** | `385.7` | `300` |
| `1000` | `89.0` | ### **`161.5`** | `352.0` | `300` |

### ➜ ⚠ **E QUESTO E' IL LIMITE DELLA CURVA, misurato:** il `τ` vero va da `162` a `286` passi, mentre la curva assume ### **`300` FISSO.** ### **Dove il `τ` misurato si allontana da `300`, il rapporto non si legge** -- ed e' la ragione che il task history ha scritto per NON decidere ai passi `50` e `150`.

> ### ⛔ **E QUELLA RAGIONE, MISURATA, E' CONTRADDETTA:** lo scarto da `300` vale `-14.4`, `-37.4` ai passi che ### **NON decidono** e `-71.6`, `-122.9`, `-138.5` a quelli che ### **DECIDONO.** ### **Il criterio escludeva i passi dove il `τ` misurato e' PIU' VICINO a `300`.**
>
> ### **E IL CRITERIO NON SI SPOSTA PER QUESTO:** era fissato PRIMA della corsa, e cambiarlo adesso ### **sarebbe spostare una soglia dopo aver visto i dati.** ### **Si dice, e si aggiunge il controllo qui sotto.**

### IL CONTROLLO DI SENSIBILITA': **la stessa lettura, col `τ` MISURATO**

| passo | `|tw|` mediano | curva con `τ = 300` | rapporto | curva col `τ` **misurato** | ### **rapporto** | lettura |
|--:|--:|--:|--:|--:|--:|---|
| `50` | `1.3967` | `0.9646` | `1.4479` | `1.0091` | ### **`1.3840`** | *(DENTRO)* |
| `150` | `2.2829` | `2.4722` | `0.9234` | `2.7343` | ### **`0.8349`** | *(DENTRO)* |
| `300` | `2.7026` | `3.9717` | `0.6805` | `4.5940` | ### **`0.5883`** | ### **DENTRO** |
| `600` | `3.4243` | `5.4328` | `0.6303` | `6.0708` | ### **`0.5641`** | ### **DENTRO** |
| `1000` | `3.9151` | `6.0590` | `0.6462` | `6.2703` | ### **`0.6244`** | ### **DENTRO** |

### ➜ ✔ **LA LETTURA NON DIPENDE DALL'ASSUNZIONE: col `τ` MISURATO i passi che decidono restano ### **tutti `DENTRO`.** ### **Il rapporto si avvicina al bordo `0.5` e non lo passa**, e questo e' piu' forte di una lettura sola.

## `twist_dip`: **il dipolo e' ancora zero?**

| passo | a `0` | a `π/2` | a `π` |
|--:|--:|--:|--:|
| `50` | ### **`1.0000`** | `0.0000` | `0.0000` |
| `150` | ### **`1.0000`** | `0.0000` | `0.0000` |
| `300` | ### **`0.9979`** | `0.0000` | `0.0021` |
| `600` | ### **`0.9892`** | `0.0000` | `0.0108` |
| `1000` | ### **`0.9790`** | `0.0000` | `0.0210` |

## LA GUARDIA DI `TAU_TW` *(rilievo `E4` del guardiano)*

| | |
|---|--:|
| invocazioni di `_tau_tw_locale` | `1000` |
| ### **SALTI** *(il `return TAU_TW` della guardia)* | ### **`0`** |

> ### ✔ **LA GUARDIA NON SCATTA MAI in `1000` passi**, e ora e' ### **MISURATO** invece che assunto: era un fallback ### **non contato** *(`P5`, `A8`)*, e se scattasse `τ_tw` passerebbe da `~2`-`6` a ### **`20`** -- un fattore `3`-`10` sul tetto di equilibrio.
>
> ### ⚠ **E <<non scatta in questa scena>> NON e' <<non scatta mai>>:** resta un ramo raggiungibile, e il contatore ora lo vede.

## ⚠ LO SFASAMENTO DI UN PASSO, **dichiarato nel sigillo** *(`c17e518`)*

> Il `|tw|` si legge ### **all'INGRESSO** del blocco della torsione, quindi il valore *«al passo `p`»* e' quello accumulato in ### **`p-1` passi.** ### **Sul rapporto alla curva lo scarto e' dell'ordine di `1/300`, cioe' lo `0.3 %`: non cambia nessuna lettura, e si dichiara invece di lasciarlo dedurre.**

## IL VERDETTO

> ### ⚠ **LA CURA TIENE, E C'E' UNA SCOPERTA.** Il meccanismo che la cura ha tolto e' ### **quello che portava un arco oltre `4π` IN UN PASSO SOLO**, e quello resta tolto: ### **`calci_spuri_curata` e `spinta_senza_causa` sono ZERO a ogni passo.** Ma ### **`29357` passi-arco hanno raggiunto `4π` ACCUMULANDO**, e ### **non e' la stessa cosa.**
>
> ### ⛔ **E QUESTA LETTURA E' FISSATA PRIMA DELLA CORSA, non adesso:** il task history `7d3ae67` (riga `123`, committato ### **prima**) dice *<<se ne comparisse UNO, sarebbe una ### **scoperta**, non un difetto della cura>>*. ### **Il generatore la contraddiceva e il generatore e' stato corretto** -- ### **non il criterio**, e la differenza e' verificabile da git: il task history e' ### **ANTENATO** di questo referto.
>
> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** ### **la soglia di mitosi `3π`, il `0.3` e `κ` si decidono su questi numeri, e sono DECISIONI DI LUCA.**

---

*Referto **generato** da `csv/_test_fork/_referto_lunga.py` dal `lunga.json`: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`), e il criterio e' letto **dal `json`** invece di essere riscritto qui.*
