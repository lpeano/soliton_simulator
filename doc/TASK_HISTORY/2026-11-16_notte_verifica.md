# LA NOTTE DI LAVORO: LE FASI 1 E 3 IN PARALLELO, LA RIPRESA PROVATA PRIMA *(Luca `2026-11-16` `20:35`)*

> **Il mandato:** le prove partono stanotte, anche in parallelo; **alle `08:00` si fermano in modo ordinato dopo un salvataggio**; la notte dopo si **RIPRENDONO dagli stati, mai da capo**. **Prima di lanciare: la PROVA che la ripresa funziona** *(R1-R5)*. **VIA ALLA FASE 3** *(`20:34`)*: V-B2 su `L 297` (`12000` tick), V-B2pi su `L 321` (`10000`), V-T120 su `L 339` (`12000`); le previsioni P-V3..P-V6 sono in `106158f8`, **nessuna soglia nuova**. Il piano: `doc/PIANO_VERIFICA_SCATOLA.md`.
> **L'ordine delle due versioni** *(PRECEDENZA-IN-CODA)*: la correzione delle `20:19` *(ripresa della fase 0 da `k 1000`)* e' superata dal mandato delle `20:35` *(«la fase 0 gia' partita resta com'e'»)*: **`prova-scatola5-L186-b` da `0` continua** *(la carta `2026-11-16_scatola5.md`, sez. `11`)*.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di scrivere una riga; cosa NON so)*

- **Gli strumenti delle corse su `L 162` sono CATENE DI DUE:** le coppie `mattone_coppia_L162.main` *(`k 0`-`2000`, lo stato ogni `500`, NESSUN `--da`)* poi `legati.coppia --da`; il triangolo `triangolo_120.corsa` *(che chiama `mattone_triangolo.main` con sostituzioni in memoria, `0`-`2000`)* poi `legati.triangolo --da`.
- **`legati` sa ripartire** *(`carica`: le chiavi `Z["chiavi"]` + `campo_A`, `campo_E`; un `MT.Campi` nuovo; `U` dal campo con `_u1_prototipo.scrivi_U`)* **e lo prova AL BIT con un DEVE di `50` tick** *(esclusa `h_int`, `CU.CHIAVI_SERVIZIO`)*. **Ma scrive la serie e le mappe SOLO A FINE CORSA, e lo stato ogni `1000`:** una corsa fermata o morta perde la serie del suo pezzo *(e' successo stasera alla fase 0)*. **Nessuno dei due passa R1-R3 cosi' com'e'.**
- **Il cammino che lo stato NON contiene:**
  - **il triangolo: i CENTRI seguiti** *(`mattone_triangolo.centri_pezzi(Z, rho, cen)` dipende dai centri del tick prima)*; `legati` li salva nel `meta` dello stato *(`centri`)*;
  - **le ETICHETTE dei conti** *(`R.etichette(centri)` ogni `CT.OGNI = 10` tick; in `legati` la cadenza e' RELATIVA a `k_da`)*: credo che servano SOLO ai conti *(`registra`)*, non al tick; **non lo so: R2 lo dice**;
  - **gli accumulatori del modulo `triangolo_120.GIRO`** *(misure, non stato)*.
- **Le misure delle coppie:** `mattone_coppia_L162` misura `d` **ogni `10` tick** *(`OGNI = CT.OGNI`)*, ed e' su quella serie che `d''` dei referti di `L 162` si calcola *(`carta_coppia.curvatura` sui tick `250`-`2000`)*; `legati.coppia` misura `d` ogni `50` *(e il raggio, `A2`, la massa, oltre `R_A`, i centri delle culle)*.
- **Le scene:** `convergenza.scena_L(L, R_A)` *(come `prova_scatola5` e `verifica_coppie`)*; il francobollo del mattone `L162_MGU_03000` *(lo stesso di `L 162`)*. **Il triangolo:** `MT.scena(MT.CORSA_162, ...)` e' chiamata sia per IL FRANCOBOLLO *(la scena vera di `L 162`)* sia per LA CORSA *(qui `L 339`)*: la sostituzione deve distinguerle.
- **Non so:** il tempo per tick vero su `L 297`-`402` *(la stima `2.95 s` su `L 186` per `L^2`: `7.5`, `8.8`, `9.8`, `13.8` s su `297`, `321`, `339`, `402`)*; la memoria per processo; se `R_ogg` misurato al `5%` sulla coppia e sul triangolo a `k 0` sta dentro i tori stretti *(su `L 297` la regola chiede `R_ogg <= 42.87`; il piano lo stima `42.5`)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### 2.1 Lo strumento della notte: `csv/solitone/notte.py` *(un file NUOVO: gli strumenti in uso non si toccano)*

- **`avvio`** *(lo stato a `k 0`)*: **la costruzione di `mattone_coppia_L162.main`** *(coppia: le sostituzioni di `verifica_coppie`: la scena di `L`, il bordo, i centri a `d/2`, l'antifase)* **o di `triangolo_120.corsa`** *(triangolo: la scena di `L` per la corsa e la scena VERA per il francobollo, `MTR.R_A_SCENA` = il bordo nuovo)*, **intercettata in `Corsa.inizio(0)`**: **la regola R-SCATOLA al `5%` a tre clausole** *(N5: se cade, la corsa NON parte)*, **poi lo stato a `k 0` salvato, e lo strumento esce** *(nessun tick fatto dal codice vecchio)*.
- **`corsa`** *(da uno stato, `--da k` o `--da ultimo`)*: **il ciclo di `legati.coppia` / `legati.triangolo` COPIATO** *(le stesse misure)*, con:
  - **lo stato completo ogni `250` tick** *(N2)* nell'archivio `E:\soliton_simulator\notte\<nome>\`: `Z["chiavi"]` + `campo_A`, `campo_E` + il `meta` *(il `k`, il `t`, i centri seguiti, i centri DELLE ULTIME ETICHETTE)*; **accanto, lo sha1 dei byte** *(R3)*; **tenuti gli ultimi due e i multipli di `1000`**;
  - **a ogni salvataggio, i PEZZI della serie e delle mappe e dei conti dall'ultimo salvataggio** *(i tick in `(k_prima, k]`)*: **una corsa morta perde al piu' `250` tick, e la serie unita e' la catena dei pezzi**;
  - **le etichette alla cadenza ASSOLUTA** *(`k % CT.OGNI == 0`)* **e alla ripresa quelle del `meta`**;
  - **la fermata a ora** *(`--ferma-alle`: dopo il tick in cui scatta, lo stato a QUEL `k` e i pezzi, poi la voce del registro chiusa «SOSPESA per ordine di Luca (20:33), da riprendere», col `k`, il percorso e lo sha1)*; **la stessa cosa sotto `MEM_MIN_GB`**;
  - **alla ripresa: lo sha1 ricalcolato; se non coincide, lo scrive e prende lo stato prima** *(R3)*;
  - **a ogni salvataggio, R-SCATOLA al `5%`** *(N5: scritta, la corsa continua)*; **alle tappe il `k` e il percorso dell'ultimo stato** *(N2)*.
- **Le misure:** la coppia `d` OGNI `10` tick *(come `mattone_coppia_L162`: la fase 1 legge `d''` con lo stesso codice)* e il resto di `legati.coppia` ogni `50`; il triangolo quelle di `legati.triangolo` *(e di `triangolo_120`: il giro ogni `100`)*. **Le mappe ogni `100`** *(N3: `rho`, `dphi`, `E` in `float32`: circa `1.4`-`1.9` MB per fotogramma su `L 339`-`402`, circa `120` fotogrammi per `12000` tick, **sotto `250` MB per corsa** compressi; su E: `200` GB liberi)*.
- **I DEVE della corsa:** **Gauss sotto `10` volte il residuo iniziale** *(la regola del porto e di `prova_scatola5`: su un toro nuovo `1e-10` di `L 162` non e' tarato)*; **la massa persa = la massa uscita dal bordo entro `1e-6`** *(sui conti uniti)*.
- **I bordi** *(`R_A = 2 R_ogg`, `R_ogg = r_scena + 25`)*: **la fase 1 `R_A = d + 50`** *(il piano, `verifica_coppie`)*; **la fase 3 con la `d` PIU' GRANDE di `L 162`** *(come i tori)*: **V-B2 `85.06`, V-B2pi `92.42`, V-T120 `97.16`** *(`2 (40.84/sqrt 3 + 25)`)*. **Mio, dichiarato.**

### 2.2 La prova della ripresa *(R2: `csv/solitone/notte_prova.py`)*

- **Per ogni strumento, sulla SCENA VERA:** **la coppia** su V-B2 *(`d 35`, in fase, `L 297`: e' anche la scena di F-35)*; **il triangolo** su V-T120 *(`L 339`)*. **Uno stato a `k 0` (`avvio`), poi da quello: (a) un processo `0 -> 40`; (b) un processo `0 -> 20` che salva e si ferma, e un PROCESSO NUOVO `--da 20 -> 40`.** *(Gli stati ogni `20` per la prova: la cadenza e' un argomento.)* **`20` e' multiplo di `CT.OGNI` (`10`): la fermata FUORI dal passo** *(come quella delle `08:00`)* **la prova un caso in piu', `(c)`: `0 -> 25` fermata a `25`, poi un processo nuovo `--da 25 -> 40`.**
- ### **IL CRITERIO, PRIMA DEI NUMERI:** **lo stato a `k 40` di (a), (b), (c): OGNI chiave, la differenza massima = `0`** *(`h_int` compresa: se differisce lo scrivo a parte, e decide il tick: le altre chiavi `0`)*; **le serie unite di (b) e (c) = la serie di (a) da `0` a `40`, AL BIT**; **lo sha1 di ogni stato scritto e ricontrollato; un caso che DEVE FALLIRE: uno stato con un byte cambiato -> la ripresa lo RIFIUTA e prende quello prima.**
- **Cosa mi farebbe FERMARE:** una differenza diversa da `0` in una chiave che il tick legge *(quella corsa non parte: R4)*; un caso che deve fallire e passa.

### 2.3 I lanci *(N1)*

- **Dopo il commit del referto R5:** la fase 0 *(gia' in corsa)* + V-T120 + V-B2 + V-B2pi + F-66: **5 processi, un filo ciascuno** *(`OMP`, `MKL`, `OPENBLAS`, `NUMEXPR` a `1`; numba spento)*. **Quando la fase 0 finisce: la fase 1 nell'ordine F-66, A-66, F-51, A-51, A-45, F-35, A-35.** **Dalle `07:30` nessuna corsa parte** *(F1)*; **`--ferma-alle 2026-11-17T08:00`** *(F2)*.
- **Chi lancia la corsa dopo:** io, alla notifica della fine di una corsa.

## 3. TODO DEL NEXT STEP

1. `notte.py` *(avvio, corsa)* e `notte_prova.py`; la suite; commit.
2. R2 sulla coppia *(`L 297`)* e sul triangolo *(`L 339`)*, in parallelo *(con la fase 0: al piu' `5` processi)*; R3 col caso che deve fallire; **il referto `doc/referti_l2/prova_ripresa.txt`; commit.**
3. I lanci *(N1)*; le voci nel registro; commit.
4. La fase 0 alla fine *(il referto, la sez. `9` della carta scatola5)*; la fase 1 una dopo l'altra; la fase 2; alle `08:00` F1-F3.
