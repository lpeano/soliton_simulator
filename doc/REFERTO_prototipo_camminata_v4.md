# IL REFERTO DEL PROTOTIPO `v4` — **`cs` LOCALE DAL VUOTO, IN TUTTE LE LEGGI**

> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un ### **REPERTO** — la CI ### **non lo rigenera**, e il presidio verifica ### **il suo BLOB.**

*(**Generato** da `python proto_camminata/_referto4.py`, che legge `proto_camminata/uscite/letture_v4.json` prodotto da `python proto_camminata/_letture4.py`. Criteri, previsioni e soglie: `doc/TASK_HISTORY/2026-10-11_camminata_v4_cs_locale.md`, **committato PRIMA del codice** (`db40a3c`). Decisione: `CS-LOCALE-DAL-VUOTO`.)*

> ### ⛔ **QUESTO FILE E' GENERATO da `python proto_camminata/_referto4.py`: NON si scrive a mano.** ### **Ogni numero e ogni verdetto escono da `proto_camminata/uscite/letture_v4.json`** *(`L-NUMERI`)*, e le soglie stanno nel task history `doc/TASK_HISTORY/2026-10-11_camminata_v4_cs_locale.md`, ### **scritte PRIMA dei numeri.**

## LA CONFIGURAZIONE, INTERA *(`H-P5`)*

| | |
|---|---|
| la scena | **irregolare**, `n = 120` nodi, `m = 208` archi, seme **`11`** |
| la scena di `L0` | **regolare** *(circolante)*, perche' sull'irregolare l'eccentricita' e' `6` e ### **il fronte satura in sei tick** |
| i semi | ``11`, `23`, `37`, `53`` |
| i tick | **`24`** |
| `eps` della moneta di spin | **`0.5`** |
| la geometria | `scena_identita` *(e `scena_curva` nei bracci del banco)* |
| il vuoto | `vuoto_fondo(lambda_0 = 1.0)`, modulo **uniforme**, fasi dal seme |
| la non linearita' | `saturazione3.flusso` *(`N` sull'elicita' locale)* |
| le candidate di `A1` | `scatter` e `trasmissione`, ### **una per volta** |
| la forma di `cs` | `dispersione` *(l'unica che da' `cs = 1.0` AL BIT sul fondo del `v3`)* |
| la forma del `cs` d'arco | `min` *(l'estremita' lenta fa da collo: la scelta causale)* |
| le candidate di `A4` | **`(F)`** pezzi frazionari sincroni · **`(S)`** tick asincroni |

## ⭐ **`L0` — L'INVARIANZA LOCALE DELLA LUCE: `(S)` LA RISPETTA, `(F)` NO**

> ### ⛔ **E SI LEGGE COME UN *RAPPORTO*, non come <<vale `1`>>:** la velocita' del fronte a `cs = 1` e' **`0.6193`** archi/tick, ### **non `1`** — la camminata di Grover ### **non satura il cono**, e lo stesso numero il `v3` lo ha gia' misurato. ### **Quindi la domanda giusta e': la velocita' in tempo proprio e' LA STESSA a ogni `cs`?**

### la candidata **`(F)`** — scena `regolare`, eccentricita' `30`

| `cs` | tick | fronte, archi/tick | in **tempo proprio** | rapporto al riferimento | entro `3 sigma`? |
|---|---|---|---|---|---|
| **`0.25`** | `48` | 0.1652 ± 0.0032 | **0.6609** ± 0.0130 | ### **1.0671** | ### ✅ **SI** |
| **`0.50`** | `48` | 0.3374 ± 0.0035 | **0.6748** ± 0.0071 | ### **1.0895** | ### ⛔ **NO** |
| **`0.75`** | `37` | 0.5263 ± 0.0052 | **0.7018** ± 0.0070 | ### **1.1331** | ### ⛔ **NO** |
| **`1.00`** | `28` | 0.6193 ± 0.0094 | **0.6193** ± 0.0094 | ### **1.0000** | ### ✅ **SI** |

### la candidata **`(S)`** — scena `regolare`, eccentricita' `30`

| `cs` | tick | fronte, archi/tick | in **tempo proprio** | rapporto al riferimento | entro `3 sigma`? |
|---|---|---|---|---|---|
| **`0.25`** | `48` | 0.1611 ± 0.0055 | **0.6444** ± 0.0221 | ### **1.0405** | ### ✅ **SI** |
| **`0.50`** | `48` | 0.3157 ± 0.0048 | **0.6314** ± 0.0096 | ### **1.0194** | ### ✅ **SI** |
| **`0.75`** | `37` | 0.4706 ± 0.0069 | **0.6275** ± 0.0091 | ### **1.0132** | ### ✅ **SI** |
| **`1.00`** | `28` | 0.6193 ± 0.0094 | **0.6193** ± 0.0094 | ### **1.0000** | ### ✅ **SI** |

### ✅ **CONFERMA** **`(S)` RISPETTA L'INVARIANZA LOCALE: `0` casi su `4` fuori da `3 sigma`, e lo scarto peggiore e' il `4.0%`.** ### ⛔ **SMENTITA** **`(F)` NO: `2` casi fuori, e lo scarto peggiore e' il `13.3%`.**

### ⚠ **E LA MIA PREVISIONE ERA GIUSTA SU `(S)` E GIUSTA NEL VERSO SU `(F)`, MA SBAGLIATA SU *DOVE*:** avevo scritto *<<lo scarto cresce quando `cs` scende>>*, e invece ### **cresce verso `cs` INTERMEDI** *(`1.133` a `cs = 0.75`, `1.067` a `cs = 0.25`)*. ### ⭐ **E il motivo e' il punto `A4`:** a `cs = 0` e a `cs = 1` la famiglia frazionaria e' ### **esatta**, quindi l'errore di composizione e' ### **massimo in mezzo.**

## ⛔ **`L4` — MATERIA E ANTIMATERIA: `(F)` LE FA PIEGARE IL TEMPO IN MODO DIVERSO**

| la candidata | `max\|dLambda\|` | `max\|dcs\|` | la soglia | tiene? |
|---|---|---|---|---|
| **`(F)`** | **12.5** | **0.624** | 3e-11 | ### ⛔ **NO** |
| **`(S)`** | **4.44e-15** | **1.55e-15** | 2.34e-11 | ### ✅ **SI** |

### ⭐ **E QUESTA E' LA *CONSEGUENZA FISICA* DELLA `C` ROTTA, e per questo conta piu' del numero del banco:** il vincolo `W5` esiste per far si' che ### **materia e antimateria pieghino il tempo allo stesso modo**, e `(F)` ### **non lo fa** — il grumo e il suo coniugato lasciano impronte che differiscono di **12.5** su `Lambda` e di **0.624** su `cs`. ### ✅ **`(S)` lo fa, a `4.44e-15`.**

## ⚠ **`L1`, `L2`, `L3`, `L5` — QUATTRO RISULTATI NEGATIVI, E SONO RISULTATI**

| la lettura | la domanda | il numero | il verdetto |
|---|---|---|---|
| `L1` **`(F)`**, `scatter` | si forma una zona modificata **FUORI** dal grumo? | anelli oltre `3 sigma`: **### **NESSUNO****; fronte finale `r = 6`, entro il cono: **si** | ### ⛔ **SMENTITA** |
| `L1` **`(F)`**, `trasmissione` | si forma una zona modificata **FUORI** dal grumo? | anelli oltre `3 sigma`: **### **NESSUNO****; fronte finale `r = 6`, entro il cono: **si** | ### ⛔ **SMENTITA** |
| `L1` **`(S)`**, `scatter` | si forma una zona modificata **FUORI** dal grumo? | anelli oltre `3 sigma`: **### **NESSUNO****; fronte finale `r = 6`, entro il cono: **si** | ### ⛔ **SMENTITA** |
| `L1` **`(S)`**, `trasmissione` | si forma una zona modificata **FUORI** dal grumo? | anelli oltre `3 sigma`: **### **NESSUNO****; fronte finale `r = 6`, entro il cono: **si** | ### ⛔ **SMENTITA** |
| `L2` **`(F)`** | un pacchetto di **passaggio** lascia la stessa impronta di un grumo? | differenza **0.019**, **`0.90 sigma`** *(norme pari: **si**)* | ### ⛔ **SMENTITA** |
| `L2` **`(S)`** | un pacchetto di **passaggio** lascia la stessa impronta di un grumo? | differenza **0.00418**, **`0.19 sigma`** *(norme pari: **si**)* | ### ⛔ **SMENTITA** |
| `L3` **`(F)`** | la luce **sente la massa**? | ritardo **+0.50 tick**, **`0.15 sigma`** *(lancio `58` → bersaglio `45`, il grumo e' a `2` archi dal bersaglio)* | ### ⛔ **SMENTITA** |
| `L3` **`(S)`** | la luce **sente la massa**? | ritardo **-2.00 tick**, **`0.87 sigma`** *(lancio `58` → bersaglio `45`, il grumo e' a `2` archi dal bersaglio)* | ### ⛔ **SMENTITA** |
| `L5` **`(F)`**, `D=2` | due grumi si avvicinano **piu' che nel `v3`**? | differenza **0.02615**, **`0.73 sigma`** | ### ⛔ **SMENTITA** |
| `L5` **`(F)`**, `D=4` | due grumi si avvicinano **piu' che nel `v3`**? | differenza **0.00077**, **`0.06 sigma`** | ### ⛔ **SMENTITA** |
| `L5` **`(S)`**, `D=2` | due grumi si avvicinano **piu' che nel `v3`**? | differenza **0.06154**, **`1.84 sigma`** | ### ⛔ **SMENTITA** |
| `L5` **`(S)`**, `D=4` | due grumi si avvicinano **piu' che nel `v3`**? | differenza **0.02231**, **`0.84 sigma`** | ### ⛔ **SMENTITA** |

### ⛔ **E I QUATTRO NEGATIVI VANNO LETTI INSIEME, perche' dicono una cosa sola:** a queste taglie ### **il `cs` locale non produce un effetto misurabile sulla materia.** ### **`L1`** non trova zona modificata fuori dal grumo; ### **`L2`** non distingue un grumo da un pacchetto di passaggio; ### **`L3`** non trova un ritardo della luce; ### **`L5`** non trova avvicinamento. ### ⭐ **E `L5` era previsto:** `G2` ha dato `0.69 sigma` fra `N` e lineare, e un effetto di gravita' ### **non poteva essere piu' grande di quello.**

### ⭐ **E `L2` CONFERMA IL PUNTO `1` DELLA DECISIONE DI LUCA, NEL VERSO CHE LA MOTIVA:** *<<una `rho` di nodo non distingue un grumo legato da un pacchetto di luce di passaggio>>*. ### **Misurato: non li distingue** — `0.90 sigma` per `(F)` e `0.19 sigma` per `(S)`, con le norme ### **pareggiate.**

## 📌 **IL CONFRONTO FRA `(F)` E `(S)`, COME LO CONSEGNO — E NON SCELGO IO**

| | `(F)` pezzi frazionari | `(S)` tick asincroni |
|---|---|---|
| la dinamica | **liscia** | **a scatti** *(il cono: raggio `0` al primo tick)* |
| la `C` sul passo | ### ⛔ **ROTTA**, `4.6475` | ### ⭐ **esatta**, `0` |
| materia/antimateria *(`L4`)* | ### ⛔ **NON tiene**, `12.5` | ### ✅ **tiene**, `4.44e-15` |
| l'invarianza locale *(`L0`)* | ### ⛔ **approssimata**, fino al `13.3%` | ### ✅ **entro `3 sigma`** in tutti i casi |
| lo stato | `psi`, `phi` | ### ⚠ `psi`, `phi`, **`tau` E un bit per nodo** |
| le leggi contate | la **famiglia frazionaria** | la famiglia **non serve**, ma serve ### **uno stato nuovo** *(`9-ter`)* |

### ⛔ **LE TRE SCELTE SONO DI LUCA, e stanno in `doc/indice/DA_DECIDERE_LUCA.md`, UNA per scelta:** come la materia cambia `Lambda` *(`scatter` o `trasmissione`)*, come il vuoto fissa `cs` *(`dispersione`, `contrasto` o `densita`)*, e `(F)` contro `(S)`. ### **Io porto il confronto misurato.**

## ⚠ **I LIMITI, dichiarati**

| | il limite |
|---|---|
| `1` | ### **`L1`, `L2` e `L5` usano un PACCHETTO, non un grumo legato:** il mandato dice *<<partendo da un grumo `v3` auto-intrappolato>>*, e il ### **`v3` non ne ha trovato nessuno** *(misurato due volte: referto `v3`, e di nuovo in `G1`)*. ### **Ogni risultato va letto come <<l'impronta di un pacchetto>>** |
| `2` | ### **La velocita' a `cs = 1` non e' `1`** *(e' `0.6193`)*: la camminata di Grover ### **non satura il cono**, quindi `L0` si legge come un ### **rapporto** e non come un valore assoluto |
| `3` | ### **`L0` gira sul REGOLARE**, perche' sull'irregolare l'eccentricita' e' `6` e il fronte ### **satura in sei tick** — e adattare una retta su una curva satura da' ### **una pendenza che non e' una velocita'** |
| `4` | ### **La <<conservazione modificata>> del `v3` NON e' derivata per un `cs` non uniforme**, quindi ### **non e' misurata qui**, e ### **non la chiamo energia** *(quella scelta e' di Luca)* |
| `5` | ### **Un solo grafo per la scena principale**, `n = 120`: ### **due taglie non sono uno scaling** *(`TAGLIA-FINITA`)*, e nessun limite continuo si afferma |

