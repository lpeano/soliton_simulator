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
