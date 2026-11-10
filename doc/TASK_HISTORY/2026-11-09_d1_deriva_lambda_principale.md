# D1, LA DERIVA DI `Lambda` DEL VUOTO SUL NUCLEO CONGELATO DEL PRINCIPALE *(Luca `2026-11-09` `23:02`)*

**Il mandato:** dopo T1 del laterale *(`81c690a8`, lettura (v3): nel vuoto F3 a `cs` spento `Lambda` cresce di `+2.228e-12` in `1000` tick, uniforme, la pendenza `0.985`)*,
**la stessa misura sul nucleo del principale, che non ha il v2.** **Si misura, non si tocca niente.**
**L'eccezione di Luca a U1** *(il divieto di porting delle `20:16`)*: **solo lo script di misura `csv/solitone/lambda_vuoto_deriva.py` del laterale** *(`141711d3`, blob `b4610021`, sha1 dei byte grezzi)* **passa sul principale, come file NUOVO** *(`csv/solitone/lambda_vuoto_deriva_principale.py`)*. **Nessun altro file.**

## 1. LE PREMESSE DAL CODICE

- **Che cosa differisce fra i due rami nel percorso dello script** *(sha1 dei byte grezzi, letti dal disco dei due worktree prima di questo task history)*:
  - `primo_ordine/tick.py` **uguale** *(`d9a59ff9` su tutti e due)*; `primo_ordine/motore.py` **uguale** *(`0e07bbfd`)*;
  - `primo_ordine/energia_pesata.py` **diverso** *(laterale `43bce8ad`, principale `cfaff204`)*; `primo_ordine/flussi_parziali.py` **diverso** *(laterale `d43b1cf8`, principale `1461182f`)*: **e' il v2**;
  - `csv/solitone/corsa_accensione.py`: **nessuna riga di differenza** fra il disco del principale e il `HEAD` del laterale;
  - `csv/solitone/__init__.py` **diverso**: **sul principale chiama `ramo.vieta_cs()`** *(P3)*.
- **`csv/solitone/carta_punto_fisso.py` NON ESISTE sul principale:** **lo script del laterale ne usa SOLO la costante `CPF.CORSA = "TBS"`** *(e il timbro del presidio)*.
- **Il divieto P3:** **alza solo se `mot.cs` e `mot.lambda_c` sono tutti e due non `None`;** **lo script mette `mot.lambda_c = None` prima di ogni tick:** **la funzione vera viene chiamata, e a `cs` spento ritorna subito.**
- ### **NON SO:** **se a `lambda_c = None` il v2 tocca il tick** *(cioe' se sul laterale il v2 entra nel vuoto a `cs` spento)*. **Se non lo tocca, i due rami fanno lo stesso tick e (w1) e' attesa;** **se lo tocca, la misura lo dice.** **Non lo leggo prima: e' la domanda della misura.**

## 2. LE MODIFICHE RISPETTO AL BLOB `b4610021`, DICHIARATE

1. **`from solitone import carta_punto_fisso as CPF` tolto;** **`CORSA = "TBS"` scritto nello script** *(il valore di `CPF.CORSA` sul laterale)*.
2. **I timbri del presidio:** **tolto `carta_punto_fisso.py`, aggiunto `ramo.py`** *(il divieto P3 sta nel percorso)*; **stampata una riga col ramo e lo stato del divieto.**
3. **La docstring:** **il comando, il referto `doc/referti_l2/lambda_vuoto_deriva_principale.txt`, questo task history.**
4. **I numeri del laterale ACCANTO** *(D1.3)*: **lo script li LEGGE dal referto committato del laterale** *(`git show zero-nel-nucleo:doc/referti_l2/lambda_vuoto_deriva.txt`, al commit `81c690a8`)* **e li stampa accanto:** **nessun numero ricopiato a mano** *(`L-NUMERI`)*. **E' una lettura, non un porting.**
5. **La lettura (w1)/(w2)/(w3) al posto di (v1)-(v3), scritta qui PRIMA della corsa** *(sez. 3)*.
- **Tutto il resto identico:** **la scena, `N_TICK 1000`, `T_INIEZIONE 500`, `DELTA_L 1e-12`, la corsa, T1-F, le stampe.**

## 3. PROGETTAZIONE DEL RAGIONAMENTO *(le letture si fissano qui)*

- **La scena** *(D1.2)*: **toro `81 x 81` del vuoto di TBS, `mot.cs` `0.15` ovunque, `Lambda` `6`, `1000` tick;** **lo script stampa `mot.cs` min/max e `Lambda` all'inizio: se non sono `0.15` e `6`, FERMO.**
- **T1-F DEVE FALLIRE** *(`1e-12` su un nodo al tick `500`)*: **se passa, la misura non vede, e nessuna lettura vale.**
- **Le letture** *(di Luca, rese operative)*, **sulla deriva media al tick `1000` del principale `d_P` e del laterale `d_L`, e sulla pendenza `p` della rms fra i tick `10` e `1000`:**
  - **(w1)** **`p >= 0.75` e `|d_P / d_L - 1| <= 0.10`**: **stessa deriva entro il `10%`: e' del tick di sempre, non del v2;**
  - **(w2)** **`p < 0.75`** *(oppure `Lambda` costante al bit)*: **nessuna deriva sistematica: l'ha introdotta il v2; da capire PRIMA dell'unificazione, e lo si scrive nella sezione U1** *(il task history `2026-11-08_zero_simmetrico_nel_nucleo.md`, sez. `10`)*;
  - **(w3)** **`p >= 0.75` e `|d_P / d_L - 1| > 0.10`** *(o il segno opposto)*: **una deriva diversa: si scrive di quanto, senza interpretare.**
- **Il costo:** **`~143` s sul laterale** *(stima: accanto a S162 forse il doppio)*. **E' l'unico test breve in corso; S162 non si tocca** *(lo script e' un file NUOVO, non nel percorso di S162)*.

## 4. TODO DEL NEXT STEP

1. Questo task history: commit e push.
2. Lo script `csv/solitone/lambda_vuoto_deriva_principale.py`; la suite in `wt_zero_padre`; commit e push.
3. La corsa; il referto `doc/referti_l2/lambda_vuoto_deriva_principale.txt`; l'esito qui (sez. 5); una riga nella RELAZIONE; se (w2), la riga nella sezione U1.
4. **Dopo D1: fermo su questo tema.** **In coda, sul laterale: D2** *(il mandato di Luca delle `23:02`, «in quale pezzo del tick nasce la deriva»)*, **che parte solo con D1 su origin.**

## 5. L'ESITO *(la corsa dalle `23:28:50` alle `23:31:29`, a `2bb45ecf`; il referto `doc/referti_l2/lambda_vuoto_deriva_principale.txt`)*

- **La scena come quella del laterale:** **`6561` nodi, `mot.cs` min e max `0.15`, `Lambda` all'inizio `6`;** **il divieto P3 attivo, e non e' scattato** *(`lambda_c = None`)*.
- **T1-F fallisce come deve** *(`9.397e-13` dopo il tick `500`)*: **la misura vede.**
- **La tabella, principale e laterale ACCANTO** *(i numeri del laterale letti dal suo referto a `81c690a8`)*: **UGUALI A TUTTE LE CIFRE STAMPATE:**
  - `|Delta Lambda|` per tick: **max `1.066e-14` (`12.0` ulp), media `2.499e-15` (`2.81` ulp); `273` tick su `1000` senza cambiamento** *(tutti e due)*;
  - la deriva al tick `1`: `+1.776e-15`; al tick `10`: `+2.400e-14`; al tick `100`: `+2.256e-13`; al tick `1000`: **`+2.228e-12` (`2508` ulp)**, **max = media = rms** *(tutti e due)*;
  - **la pendenza della rms fra i tick `10` e `1000`: `0.985`** *(tutti e due)*.
- **La deriva media per tick:** **il principale `+2.2276e-15`, il laterale `+2.2280e-15`; il rapporto `0.999799`.**
  ### ⚠ **Lo scarto `2e-4` e' l'arrotondamento del referto del laterale** *(quattro cifre: `2.228e-12`)*, **non una differenza misurata.** **Non dico «al bit»:** **i due stati non sono stati confrontati byte per byte.**
- ### **LA LETTURA: (w1)** — **la stessa deriva: e' del tick di sempre, non del v2.** **A `cs` spento il v2 non entra nel vuoto** *(la premessa NON SO della sez. `1`: la risposta e' qui, per misura)*.
- ### **La conseguenza, scritta per D2:** **la causa sta nel tick CONDIVISO** *(`tick.py` `d9a59ff9` e i pezzi del vuoto)*: **una correzione eventuale toccherebbe anche il nucleo congelato del principale. La decisione e' di Luca.**
- **Fermo su questo tema** *(il mandato)*. **D2 parte sul laterale** *(D1 e' su origin)*.

## 6. ⚠ UNA PREMESSA CADUTA, MIO ERRORE: D1 NON HA MISURATO IL PRINCIPALE «SENZA v2» *(annotazione, non riscrittura: le sez. `1` e `5` restano come erano)*

- **Lo script, come quello del laterale, gira il tick dentro `BE.conv(DC.ZERO)`** *(`_deriva_congelato.ZERO = "simm"`)*. **Letto dal codice dei due rami:**
  - **sul principale** `csv/_zero_simmetrico.conv("simm")` **= `convenzione_simmetrica()`, che AVVOLGE IN MEMORIA `flussi_parziali.grover`, `hop_psi`, `hop_phi`:** **il pezzo di oggi a `f/2`, poi quello di `convenzione_alternativa` a `f/2`;**
  - **sul laterale** **la stessa chiamata non avvolge NIENTE** *(dal `2026-11-08` lo zero simmetrico e' NEL nucleo: `flussi_parziali.grover` ecc. fanno quelle stesse operazioni, nello stesso ordine, e il braccio `0` di `zero_nel_nucleo` e' AL BIT)*.
- ### **Quindi D1 ha confrontato il v2 nel nucleo col v2 in memoria: l'uguaglianza era attesa per costruzione.** **La sez. `1` ha guardato gli sha1 dei file e NON l'avvolgimento in memoria** *(la premessa «NON SO» non lo nominava)*.
- ### **Che cosa resta vero di (w1):** **le corse del principale, che girano lo zero simmetrico in memoria, hanno la stessa deriva del laterale.** **Che cosa CADE:** **«del tick di sempre, non del v2»** **e** **«a `cs` spento il v2 non entra nel vuoto»** *(sez. `5`)*: **non e' stato misurato.** **Anche «la causa sta nel tick condiviso» non e' dimostrato.**
- ### **LA CORREZIONE, un lavoro a se': D1-bis** *(e' la domanda di Luca come l'ha scritta: «c'e' anche sul nucleo del principale, senza v2?»)*:
  - **lo stesso script con un argomento `--senza-avvolgimento`:** **la scena costruita IDENTICA** *(dentro `BE.conv(DC.ZERO)` come prima, e lo script stampa lo sha1 dei byte dello stato di partenza: deve coincidere fra le due modalita')*, **i tick girati con `contextlib.nullcontext()` al posto di `BE.conv(DC.ZERO)`:** **il tick del nucleo congelato com'e' sul disco;**
  - **il referto `doc/referti_l2/lambda_vuoto_deriva_principale_nucleo.txt`;** **le letture w1/w2/w3 con gli STESSI criteri della sez. `3`** *(scritte li', prima)*;
  - **il controllo positivo che l'avvolgimento c'e' davvero:** **lo script stampa se `FP.grover` e' la funzione del modulo o un avvolgimento, nelle due modalita'.**
- **Poi D2 sul laterale** *(che misura pezzo per pezzo anche la fase `conj(z)` del v2: risponde direttamente)*.

## 7. L'ESITO DI D1-bis *(a `77c07d04`, blob dello script `f28be212`; le due corse dalle `00:01:19` alle `00:02:49` e dalle `00:03:12` alle `00:05:46` del `2026-11-10`)*

- **I referti:** `doc/referti_l2/lambda_vuoto_deriva_principale_nucleo.txt` *(`--senza-avvolgimento`)* **e** `doc/referti_l2/lambda_vuoto_deriva_principale_controllo.txt` *(con l'avvolgimento, lo stesso blob)*.
- **I controlli della sez. `6`:**
  - **lo sha1 dei byte dello stato di partenza e' lo STESSO nelle due modalita':** `d0d6336fed005f50`;
  - **il controllo positivo:** **con l'avvolgimento `FP.grover` e `FP.hop_phi` sono `_zero_simmetrico.convenzione_simmetrica.<locals>.comp.<locals>.f`; senza, `flussi_parziali.grover` e `flussi_parziali.hop_phi`;**
  - **la modalita' con l'avvolgimento ridà i numeri di D1** *(`+2.228e-12` al tick `1000`, la pendenza `0.985`, il rapporto `0.999799`)*;
  - **T1-F fallisce come deve in tutte e due** *(senza: `9.477e-13`)*.
- **IL NUCLEO DEL PRINCIPALE, SENZA L'AVVOLGIMENTO** *(i numeri del laterale accanto, dal suo referto)*:

| | il principale, nucleo del disco | il laterale *(T1)* |
|---|---|---|
| `|Delta Lambda|` per tick, max | `7.105e-15` (`8.0` ulp) | `1.066e-14` (`12.0` ulp) |
| `|Delta Lambda|` per tick, media | `2.371e-15` (`2.67` ulp) | `2.499e-15` (`2.81` ulp) |
| i tick senza cambiamento | `114` su `1000` | `273` su `1000` |
| la deriva al tick `1` *(media; max = rms)* | `-4.441e-15` | `+1.776e-15` |
| al tick `10` | `-2.220e-14` | `+2.400e-14` |
| al tick `100` | `-2.354e-13` | `+2.256e-13` |
| al tick `1000` | **`-2.313e-12`** (`2604` ulp) | **`+2.228e-12`** (`2508` ulp) |
| la pendenza della rms, tick `10`-`1000` | `1.004` | `0.985` |
| la deriva media per tick | **`-2.3128e-15`** | **`+2.2280e-15`** |

- ### **LA LETTURA: (w3)** — **una deriva diversa: SISTEMATICA anche sul nucleo del principale** *(la pendenza `1.004`, max = media = rms: uniforme)*, **ma di SEGNO OPPOSTO** *(`Lambda` cala)*, **e il modulo il `3.8%` piu' grande** *(il rapporto `-1.038068`)*. **Senza interpretare** *(il mandato)*.
- ### **Che cosa cambia per D2:** **il fatto «la deriva c'e' anche senza il v2» e' misurato; «e' la stessa» no.** **D2 sul laterale misura i sotto-pezzi `a`, `b`** *(i mezzi pezzi)* **e `c`** *(la fase `conj(z)` del v2)* **separatamente.**
- ### ⚠ **UN ALTRO MIO ERRORE, nel commit `77c07d04`:** **la riga SUITE dice «dalle `23:59:34` alle `00:13:42`»: orari SCRITTI DA ME, non letti.** **Quelli veri, dall'uscita della suite: dalle `23:43:00` alle `23:56:53`, `67` su `67`.** **L'esito (`67` su `67`) e' quello vero.** *(`L-NUMERI`: un numero ricopiato non ha provenienza, e uno inventato meno ancora.)*

## 8. D2-bis, IL SEGNO DELLA DERIVA SUL NUCLEO DEL PRINCIPALE *(Luca `2026-11-10` `01:22`)*: **IL PROGETTO, PRIMA DEL CODICE**

### 8.1 LE PREMESSE DAL CODICE

- **L'eccezione di Luca a U1** *(la stessa di D1)*: **lo script del laterale `csv/solitone/lambda_deriva_pezzi.py`** *(`cd10786c`, blob `a6201067`)* **si copia qui come file NUOVO, `csv/solitone/lambda_deriva_pezzi_principale.py`.** **Nessun altro file.**
- **Che cosa e' diverso sul principale** *(letto: `git show primo-ordine:primo_ordine/flussi_parziali.py`)*:
  - **`grover`, `hop_psi`, `hop_phi` sono il pezzo INTERO a `f`:** **non ci sono `_grover_mezzo` ne' `_hop_phi_mezzo`, ne' la fase `conj(z)`;**
  - **lo spostamento del vuoto usa `_alfa_beta(z_arco(f))` con `f = 0.5`** *(sul laterale `h = 0.25`, due volte)*;
  - **`s_arco` a `s` uniforme e' `s` AL BIT** *(la forma `S/2 - D^2/(2S)`, il commento del codice)*; **`dtau_rif = 1`.**
- **Le modifiche rispetto al blob `a6201067`, dichiarate:**
  1. **`CORSA = "TBS"` scritto qui** *(`carta_punto_fisso` non c'e')*;
  2. **i sotto-pezzi tolti:** **le posizioni `6`-`9` sono pezzi interi** *(`6`, `9` il Grover del vuoto; `7`, `8` lo spostamento del vuoto)*;
  3. **i tick SENZA avvolgimento** *(`contextlib.nullcontext()` al posto di `BE.conv(DC.ZERO)`, come D1-bis)*, **la scena costruita come D1-bis; il controllo positivo stampato** *(`FP.grover`, `FP.hop_phi` del modulo)*;
  4. **D2.3 per il mezzo** *(`h = 0.25`)* **E per l'intero** *(`f = 0.5`)*: **il Grover** *(`z + d w`, `z`)*, **lo spostamento** *(`alpha + beta`, `alpha - beta`)*, **la fase** *(`|z|`)*; **e la tabella di `|alpha + beta|^2 - 1` per i passi delle corse in archivio** *(`_vuoto_vivo_B.CORSE`: `s` `0.075` e `0.15`)* **a `f` `0.5` e `0.25`, senza letture;**
  5. **D2.5 contro D1-bis:** **la deriva media al tick `1000` letta dal referto `doc/referti_l2/lambda_vuoto_deriva_principale_nucleo.txt` a `2bb5ee52`** *(`-2.313e-12`, cioe' `-2.3128e-15` per tick)*;
  6. **le letture z1/z2 al posto di p1-p3.**
- **Tutto il resto identico:** **`1000` tick, i nodi `0`-`8`, `Lambda` esatto in `Fraction`, D2.4 con `fl(1 + 1e-15)` dopo la posizione `1`.**

### 8.2 LE LETTURE, SCRITTE PRIMA *(quelle di Luca, rese operative)*

- **Il peso per TIPO** *(qui ogni tipo ha due posizioni: lo spostamento `7` + `8`)*.
- **(z1)** **`|alpha + beta|^2 - 1 < 0` sul `z` del principale** *(`f = 0.5`)* **E lo spostamento pesa oltre il `90%` della deriva:** **il segno opposto e' spiegato dallo stesso meccanismo** *(l'arrotondamento di `1 + z_re`)*.
- **(z2)** **altrimenti:** **lo scrivo senza interpretare.**
- **D2.5 DEVE PASSARE** *(entro il `10%`)*; **D2.4 DEVE FALLIRE.**
- **Il costo** *(stima)*: **due corse da `~2` minuti.**

### 8.3 TODO

1. **Questa sezione, commit e push.**
2. **Lo script; la suite in `wt_zero_padre`; commit e push.**
3. **La corsa; il referto `doc/referti_l2/lambda_deriva_pezzi_principale.txt`; l'esito qui (`8.4`); una riga nella RELAZIONE.**
4. **Poi, nell'ordine di Luca: T2 e T3 di F1 sul laterale.**

### 8.4 L'ESITO DI D2-bis *(la corsa dalle `02:00:03` alle `02:02:24` del `2026-11-10`, a `b550b9ba`, blob dello script `aae792bc`; il referto `doc/referti_l2/lambda_deriva_pezzi_principale.txt`)*

- **La scena di T1** *(`6561` nodi, `cs 0.15`, `Lambda 6`, grado `6`)*; **il controllo positivo: `FP.grover` e `FP.hop_phi` del modulo** *(nessun avvolgimento)*.
- **D2.3, i coefficienti esatti:**
  - **al mezzo `h 0.25`** *(il `z` del laterale, `0.993068 + 0.117537j`)*: **gli stessi numeri del laterale** *(lo spostamento `+1.110e-16`, `+1.051e-16`)*;
  - ### **all'intero `f 0.5`** *(il `z` del principale, `0.972370 + 0.233445j`)*: **il Grover `-6.939e-18`, `-9.671e-17`; la fase `|z|^2 - 1 = -9.671e-17`; lo spostamento `|alpha + beta|^2 - 1 = +0.000e+00` (ZERO ESATTO), `|alpha - beta|^2 - 1 = -9.671e-17`, `sigma_max - 1 = 0`;** **`materia_vuoto` `1` esatto;**
  - **i passi in archivio:** **`s 0.075`: `f 0.5` `+1.110e-16` / `+1.051e-16`; `f 0.25` `+1.110e-16` / `+1.932e-16`;** **`s 0.15`: `f 0.5` `+0.000e+00` / `-9.671e-17`; `f 0.25` `+1.110e-16` / `+1.051e-16`** *(`|alpha+beta|^2 - 1` / `|alpha-beta|^2 - 1`)*.
- **D2.2, per pezzo** *(esatto, `1000` tick, `9` nodi tutti uguali)*: **ZERO ESATTO nelle posizioni `1`-`5`, `10`-`14`;**
  - **`6` Grover `-9.7000e-17`** *(negativo nell'`88.7%` dei tick)*, **`9` Grover `-9.5604e-17`** *(`88.3%`)*;
  - **`7` spostamento `-9.7611e-17`** *(`77.9%`)*, **`8` spostamento `-9.5255e-17`** *(`77.4%`)*.
- **Per tipo:** **lo spostamento `-1.9287e-16`, peso `0.5003`; il Grover `-1.9260e-16`, peso `0.4997`.**
- **D2.5 PASSA:** **la somma `-2.3128e-15` per tick contro D1-bis `-2.3130e-15`** *(dal referto, a quattro cifre: il rapporto `0.999921`)*; **la deriva in float di questa corsa `-2.3128e-15`.**
- **D2.4 FALLISCE COME DEVE** *(la piu' pesante e' la `1`, l'aumento `2.2592e-15`, il rapporto `1.0175`)*.
- ### **LA LETTURA: (z2)** — **`|alpha + beta|^2 - 1 = 0` esatto sul `z` del principale, e lo spostamento porta il `50%`, non oltre il `90%`:** **non e' il meccanismo del laterale.** **Senza interpretare.**
- ### **Un'osservazione, NON una lettura** *(i numeri accostati, da verificare)*: **sul principale ogni pezzo pesante perde `~-9.6e-17`, e `|z|^2 - 1 = |alpha - beta|^2 - 1 = -9.671e-17`** *(il modulo del `z` calcolato da `espi` a `f 0.5`)*. **Il valore proprio del Grover sul sottospazio non uniforme e' `z`, quello dello spostamento sull'antisimmetrico e' `alpha - beta`.**
