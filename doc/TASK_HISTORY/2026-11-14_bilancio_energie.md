# 2026-11-14 — IL BILANCIO DELLE ENERGIE E DELLE FORZE *(Luca `2026-11-13` `23:47`; le scelte B1-B4 e i dettagli della regola del guardiano, su delega)*: LA CARTA, PRIMA DEL CODICE

> **La voce `15` della coda** *(sul principale, dopo il referto dei bracci di P6 -- fatto, `8ca61a34` -- e PRIMA della voce `7-bis`)*. **Ora SOLO la carta; il codice quando la voce arriva.**

## 0. IL MANDATO

- **La decisione di Luca:** **costruire il bilancio delle energie** *(dove sta l'energia, tick per tick, e quanta ne manca)* **e tenere da ora, come REGOLA, la contabilita' di energie e forze in ogni corsa.**
- **Il perche'** *(del guardiano)*: **in `Grampa` la repulsione di G parte quando i solitoni finiscono di allargarsi** *(il referto dei bracci: `d - d_0` scende fino a `-0.018` a `900` tick, poi sale)*; **allargandosi l'energia interna cambia; l'ipotesi: una parte diventa MOTO** *(il «colpetto»)*. **Senza un bilancio non si puo' dire.**
- **Quello che gia' si sa** *(del guardiano)*: **G** *(il lapse)* **e' una legge ISTANTANEA `N(rho)`, senza un campo suo: non immagazzina energia e non irradia; durante una rampa le leggi cambiano nel tempo: l'energia NON deve conservarsi** *(la differenza e' il lavoro della rampa)*; **la massa si conserva salvo quella che il bordo assorbe.**

## 1. LE DEFINIZIONI CHE ESISTONO *(lette dal codice, per nome di funzione)*

- **Il nucleo, `primo_ordine/energia_pesata.py`, `termini_di_h(mot, st, par)`:** **`(per_nodo, per_arco)`, i termini di `H` NON sommati e NON pesati** *(il nodo: la moneta; l'arco: lo spostamento)*; **`pesi(mot)`: i pesi che il passo usa.**
- **`csv/_energia_del_legame.py`, `per_nodo(inc, mot, st, campo_zero, par)`:** **`H` per nodo col campo `campo_zero` messo a zero: i termini di NODO, piu' META' di ogni termine d'ARCO a ciascuno dei suoi due nodi** *(una convenzione dichiarata: la divisione dell'arco a meta')*.
- **`csv/_libro_dei_conti.py`, `conti_per_nodo(inc, mot, st, e_K, lam_z, par)`:** **per nodo:**
  - **`cost` = `rho (e_K + 2 pi lam_z)`** *(i costituenti)*;
  - **`cin` = `em - cost`, `em` = `per_nodo(.., "phi_h")` + `2 pi lam_z rho`** *(la materia: `H` col vuoto a zero)*;
  - **`vuo` = `per_nodo(.., "psi_h")` + `2 pi lam_z Lambda`** *(il vuoto: `H` con la materia a zero)*;
  - **`leg` = `Lambda F1(rho / Lambda)`** *(il legame `S1`)*; **`tot` = `em + vuo + leg`; `M` = `rho`, `V` = `Lambda`.**
- **La U(1)** *(`csv/_u1_prototipo.py`, `Campo.K`, `Campo.V`)*: **`K = somma w E^2 / 2`, `V = somma B^2 / (2 AREA)`** *(non compatta)*.
- **Il lapse** *(`csv/solitone/tick_lapse.py`, `energia(mot, st, par, s, legge)`)*: **l'energia della dinamica col lapse** *(la forma (a) col suo termine)*.
- ### **CHE COSA SI CONSERVA, E QUANDO** *(dai referti di prima, non rimisurato qui)*:
  - **la norma** *(`M + V`)*: **esatta nel tick** *(al rumore)*; **il bordo la toglie** *(misurabile: prima e dopo `bordo.assorbi`)*;
  - **`tot`** *(il libro dei conti)*: **conservata dal tick di oggi entro l'arrotondamento** *(U4, la riunione: la deriva circa `4e-10` su un milione di tick)*; **il bordo la cambia;**
  - **col lapse:** **si conserva `tick_lapse.energia`** *(con le leggi fisse)*, **NON `tot`;** ### **durante una rampa niente si conserva** *(la legge cambia nel tempo)*;
  - **con la U:** **`tot + K + V`** *(la sorgente accoppia materia e campo)*.
- ### ⚠ **LA DIVISIONE PER REGIONI DIPENDE DALLO ZERO** *(Luca `13:43`: «solo il toro intero, non le regioni»; l'unificazione: lo zero simmetrico di v2 sposta energia fra archi e nodi)*: **i conti per nodo ESISTONO** *(non si inventa niente)*, **ma il valore in una regione cambia con lo zero e con la divisione dell'arco a meta'.** ### **La mia lettura** *(per Luca)*: **non e' il caso del FERMO** *(«le definizioni non permettono di dividere senza inventarne di nuove»)*: **si dividono; si DICHIARA che i pezzi per regione dipendono dallo zero, e si leggono soprattutto le VARIAZIONI nel tempo e i totali.**

## 2. I PEZZI B1, SCRITTI CON QUELLE DEFINIZIONI

| il pezzo | la definizione | da dove |
|---|---|---|
| **(a) la materia per solitone e fuori** | **`cost + cin + leg`** *(i conti per nodo)* **sommati entro `R_t` dal centro di ciascun solitone** *(i semipiani per la coppia)*, **e fuori** | `_libro_dei_conti.conti_per_nodo` |
| **(b) il moto** | ### **il codice NON ha una definizione di energia del moto di un solitone:** **la velocita' del centro** *(la differenza dei centri fra due controlli)* **e la STIMA `M_in v^2 / 2`, dichiarata come IPOTESI;** ⚠ **`M_in` e' l'inerzia, NEGATIVA** *(`-mu N`, `mu = 1/|eps''|`: la sez. `3` del documento sull'inerzia)*, **quindi la stima e' NEGATIVA** | i centri |
| **(c) il campo U** | **`K + V`** *(`Campo.K() + Campo.V()`, AL BIT coi referti)* | `_u1_prototipo.Campo` |
| **(d) il vuoto** | **`vuo`** *(i conti per nodo)* **entro `R_t` di ciascun solitone e lontano** | `conti_per_nodo` |
| **(e) il bordo** | **la massa e l'energia `tot` prima e dopo `bordo.assorbi`, a ogni tick** | la differenza |
| **(f) il RESIDUO** | **`(tot + K + V)(t) - (tot + K + V)(t0) + (l'energia tolta dal bordo fra t0 e t)`** | la somma |

- ### **IL DEVE della somma:** **la somma dei pezzi per regione = `tot` del toro in un colpo solo AL BIT** *(la stessa somma per nodo, solo raggruppata: la divisione non perde niente; l'ordine della somma si fissa)*.

## 3. IL PIANO B3, COI COSTI

- ### **`Grampa.npz` NON ha gli stati completi** *(ha `rho` float32 ogni `50`, `|phi_j|^2` e `dLambda` ogni `250`, non `psi` e `phi` complessi)*: **i pezzi B1 non si calcolano dagli npz.**
- **Si RIFA' `Grampa` con lo stato completo ogni `250` tick** *(lo stesso codice, `2000` tick, un file nuovo che lo importa)*: ### **il costo: circa `2.25`-`3.0` s per tick, `75`-`100` minuti; gli stati `9` x circa `9` MB su E:.** **DEVE: le serie gia' salvate di `Grampa` AL BIT.**
- **`(0)_2000` rifatto allo stesso modo** *(senza lapse)*: **circa `16` minuti.**
- ### **I DEVE del mandato:** **la somma dei pezzi = il totale AL BIT; la massa: `Delta M + la massa tolta dal bordo = 0` entro `1e-12` relativo a ogni controllo** *(in `(0)_2000`)*; **`K + V` di `conti.py` = quello dei referti AL BIT sugli stessi stati;** **DEVE FALLIRE: in `Grampa` il residuo durante la rampa diverso da zero oltre il rumore del dopo-rampa.**
- **Le letture B4:** **dove va l'energia interna durante la rampa** *(`0`-`500`)* **e l'allargamento** *(`500`-`1250`)*; **se il moto relativo cresce quando l'allargamento finisce, di quanto, e se torna coi numeri; il residuo durante e dopo la rampa.**

## 4. LA REGOLA R-CONTI *(Luca: per sempre; i dettagli del guardiano)*

- **R-CONTI-1:** **ogni corsa NUOVA** *(il codice scritto dopo che `conti.py` esiste)* **stampa la tabella dei conti** *(i pezzi B1 all'inizio, ogni `500` tick e alla fine; il residuo; la massa uscita dal bordo)*.
- **R-CONTI-2:** **due o piu' solitoni: la tabella delle forze** *(per ogni coppia la distanza e l'accelerazione relativa in finestre di `500` tick; il confronto col braccio senza campi; la lettura: l'ultima finestra almeno il `70%` della prima dopo il transitorio «forza costante», sotto il `30%` «colpetto», in mezzo «indeciso»)*.
- **R-CONTI-3:** **un solo solitone: la deriva del centro, il picco e il raggio ogni `500` tick.**
- **R-CONTI-4:** **le corse gia' scritte o in fila NON si riscrivono.**
- **R-CONTI-5:** **nella ROTTA e nella skill del registro: una corsa nuova senza le tabelle si chiude «FINITA SENZA CONTI», col motivo.** ### **Il registro oggi conosce solo `FINITO`, `FERMATO`, `FALLITO`:** **fino a un cambio del modulo** *(con la voce `15`)* **si chiude `FINITO` col punto che COMINCIA con «SENZA CONTI:» e il motivo** *(dichiarato)*.

## 5. TODO

1. **Questa carta; la regola nella ROTTA e nella skill; la voce `15` nella coda** *(adesso)*.
2. **Quando arriva la voce `15`:** **`csv/solitone/conti.py`, il collaudo, la suite, il commit; l'esito `FINITO_SENZA_CONTI` nel modulo del registro.**
3. **Il bilancio di `Grampa` e di `(0)_2000`** *(rifatti con gli stati ogni `250`)*; **il referto con le letture B4; FERMO.**

## 6. IL CODICE, ARRIVATA LA VOCE `15` *(Luca `2026-11-14` `00:53`, B1-B2: subito)*

- **`csv/solitone/conti.py`:** **i pezzi per solitone: i nodi entro `R_PEZZO = 28` dal centro PIU' VICINO** *(una partizione: ogni nodo in un pezzo; i due dischi si toccano, `d ~ 37.6`)*, **fuori: `-1`;** **la somma ESATTA dei pezzi con `fractions.Fraction`** *(il DEVE «al bit» della divisione)*; ### **`tot` per nodo e' `em + vuo + leg` e `cost + cin = em` solo a meno dell'arrotondamento: la differenza `tot - pezzi` si STAMPA** *(dichiarato)*; **`scena` COPIATA da `mattone.scena`** *(il ramo mattone non e' ancora riunito)*.
- **`csv/solitone/bilancio_corsa.py`:** **`Grampa` e `(0)_2000` rifatti** *(il ciclo di `p6_bracci` COPIATO; `rho_c` dal meta di `Grampa.npz`)*, **la massa e `tot` prima e dopo il bordo a ogni tick, lo stato ogni `250` su E:; DEVE: `d` e `M` = `p6_bracci` AL BIT.** ### **Il costo: due conti per nodo a ogni tick** *(per l'energia tolta dal bordo)*: **la corsa piu' lenta dei bracci** *(da misurare)*.
- **Il residuo:** **`tot(t) - tot(0) + l'energia tolta dal bordo`** *(Grampa non ha U)*; **la variazione di `tot` DENTRO ogni tick** *(senza il bordo)*: **nella rampa contro il rumore del dopo-rampa** *(il DEVE FALLIRE)*.
- **`csv/solitone/test_conti.py`:** **`K + V` al bit con la serie di (MGU) del ramo** *(`git show strumento-mattone:...`)* **sullo stato `MGU_05000.npz`.**

## 7. IL REFERTO: `2/4`, FERMO

- **Il referto `doc/referti_l2/bilancio_grampa.txt`** *(il codice a `db57e4df`; le corse: `(0)_2000` `1370` s, `Grampa` `5242` s, entrambe = `p6_bracci` AL BIT su `41` punti)*: ### **`2/4`: DUE DEVE NON VANNO COME DEVONO. FERMO, senza correggere.**
  - **PASSA:** **la somma dei pezzi = il totale ESATTA, a ogni stato** *(`9` + `9`)*.
  - ### **FALLISCE: la massa in `(0)_2000`:** **`Delta M + la massa tolta dal bordo` entro `1.17e-12` relativo, la soglia `1e-12`** *(di poco: l'arrotondamento accumulato su `2000` tick, una lettura NON verificata)*.
  - ### **FALLISCE IL DEVE FALLIRE della rampa:** **la variazione di `tot` DENTRO i tick nella rampa** *(`0`-`500`)* **`-1124`, contro il «rumore» del dopo-rampa `595`** *(la deviazione per tick `26.6` per `sqrt(500)`)*: **entro `3` volte il rumore: il bilancio, cosi' misurato, NON separa il lavoro della rampa dal rumore.**
- ### **UNA PREMESSA DELLA MIA CARTA CADE** *(sez. `1`: «`tot` conservata dal tick entro l'arrotondamento»)*: **anche in `(0)_2000`, SENZA lapse, il residuo `tot(t) - tot(0) + l'energia del bordo` oscilla fra `-229` e `+141`** *(su `1.65e+07`, circa `1e-5` relativo)*: **il tick NON conserva `tot` dei conti per nodo tick per tick a quel livello.** **Il «rumore» del DEVE FALLIRE e' quello.** **Da capire prima di qualunque bilancio fine:** **quale energia il tick conserva davvero** *(i pesi `pesi(mot)` di `energia_pesata`? l'energia di una forma diversa?)*.
- ### **LE LETTURE B4** *(descrittive)*: **in `Grampa` `tot` scende di `-1124` nella rampa, poi di altri `-3463` fra `500` e `1000`, di `-736` fra `1000` e `1250`, poi resta circa ferma** *(`-5322` a `1250`, `-5275` a `2000`)*: **la perdita e' nell'ALLARGAMENTO** *(`500`-`1250`)*. **Il vuoto attorno ai due solitoni CRESCE** *(A `2890 -> 3393`, B `2782 -> 3295`)*; **la materia di A sale, quella di B scende** *(`+38900`, `-45900`)*.
  - ### **IL MOTO:** **le velocita' dei centri crescono dopo `1250`** *(`4.0e-04` e `4.3e-04` a `2000`)*, **ma la stima `M_in v^2 / 2` vale `-2.9`** *(con l'inerzia negativa)*: ### **l'energia persa nell'allargamento** *(circa `5000`)* **NON torna come moto secondo quella stima** *(mille volte piu' piccola)*. **La stima e' un'IPOTESI dichiarata: con un'altra inerzia il conto cambierebbe.**
- ### **FERMO per la voce `15`** *(un DEVE non va come deve; e il mandato: FERMO dopo il referto)*. **Le domande per Luca:** **(1) quale energia il tick conserva tick per tick** *(e quindi su che cosa fare il bilancio)*; **(2) la soglia della massa** *(`1e-12` su `2000` tick o una stima dell'arrotondamento accumulato)*; **(3) come misurare il lavoro della rampa** *(un confronto con lo stesso braccio senza rampa? la variazione della SOLA parte del lapse?)*.

## 8. LA CHIUSURA DELLA VOCE `15` (Luca `2026-11-14` `09:34`, C1-C6): LE PREMESSE E IL PROGETTO, PRIMA DEL CODICE

- **Il FERMO della voce `15`** *(`003dd8de`)* **e' SCIOLTO dal mandato delle `09:34`.** **Solo lettura delle serie gia' salvate, nessuna corsa.**
- ### **L'ERRORE DEL GUARDIANO n.157:** **la tolleranza della massa `1e-12` e' troppo stretta per una somma di circa `1e5` numeri in doppia precisione.** **C1: `1e-11` relativo, RIVISTA DOPO il risultato** *(dichiarato cosi' nel referto)*.

### 8.1 LE PREMESSE DAL CODICE *(cosa credo, e cosa NON so)*

- **`doc/referti_l2/bilancio/<braccio>_corsa.npz` ha, per OGNI tick, `E_pt = (tot prima del bordo, tot dopo)` e `M_pt` uguale per la massa** *(`bilancio_corsa.corsa`)*: **bastano per la media su `100` tick, il residuo, il rumore e la differenza fra i due bracci; nessuno stato in piu'.**
- **`tot(0)` e la massa all'inizio vengono dallo stato `0` su E:** *(`bilancio/<braccio>_00000.npz`, coi conti per nodo, come il referto)*.
- **I pezzi per solitone ci sono solo ogni `250` tick** *(gli stati)*: **NON si possono mediare su `100` tick; restano istantanei, dichiarato.**
- ### **COSA NON SO:** **se il «rumore» di `(0)_2000` mediato su `100` tick e' piccolo** *(se l'oscillazione e' veloce rispetto a `100` tick la media la toglie; se e' lenta, no)*. **Lo dice il numero.**

### 8.2 IL PROGETTO *(`csv/solitone/bilancio_chiusura.py`, nuovo; `bilancio_corsa.py` resta com'e', il suo referto si rigira al suo commit)*

- **C2:** **il residuo per tick `r(k) = tot(k) - tot(0) + l'energia tolta dal bordo fino a k`; la MEDIA in `20` finestre di `100` tick** *(`1`-`100`, ..., `1901`-`2000`)*, **per i due bracci.** ### **MIA SCELTA, il rumore di UNA media:** **`s_w` = la deviazione standard delle `20` medie di `(0)_2000`** *(senza lapse; la deriva, se c'e', finisce nel rumore: dichiarato)*.
- **C3:** **il lavoro dell'accensione, finestra per finestra: `D_w` = la media di `Grampa` meno quella di `(0)_2000`.** ### **IL DEVE FALLIRE riletto sui tick `500`-`1250`** *(dove avviene; dichiarato come riletto DOPO il risultato)*: **`W = D(1250) - D(500)`, con `D(c)` la media sui tick `c - 49` ... `c + 50`; il rumore di `W` = `2 s_w`** *(due finestre, ciascuna differenza di due bracci: MIA SCELTA, dichiarata)*; **DEVE FALLIRE: «`|W|` entro `3` volte il rumore».**
- **C1:** **la massa di `(0)_2000`: `Delta M` + la massa tolta dal bordo, entro `1e-11` relativo a ogni tick** *(il DEVE riletto; tick per tick, NON mediato: la massa si conserva per costruzione)*.
- **C4:** **il referto chiude con la frase del mandato: il bilancio non risolve l'energia del moto** *(sotto il rumore)*; **la domanda forza/colpetto passa alla coppia B1** *(il ramo mattone)*.
- **C5:** **R-CONTI: l'energia nelle tabelle dei conti e' la MEDIA su `100` tick** *(una riga nella ROTTA e nella skill `registro-corse`)*.
- **C6:** **il paragrafo del raggio va sul ramo mattone** *(il referto `rhoc.txt` e' li': sez. `15` del task history del ramo)*.

### 8.3 COSA MI FAREBBE FERMARE

- **la massa oltre `1e-11`; il DEVE FALLIRE che passa** *(`W` dentro il rumore)*: **referto, senza correggere, FERMO della voce.**

### 8.4 TODO

1. questo task history e la relazione, commit e push;
2. `bilancio_chiusura.py`, l'inventario, la suite, commit e push;
3. il referto `doc/referti_l2/bilancio_chiusura.txt`, la relazione, la ROTTA, la skill: commit e push.

## 9. LA CHIUSURA: `2/2` *(il codice a `81b14985`; alle `10:37`; `doc/referti_l2/bilancio_chiusura.txt`)*

- **C1, la massa di `(0)_2000`:** **il peggiore `1.17e-12`, entro `1e-11`** *(n.157, rivista DOPO il risultato)*: **PASSA.** **In `Grampa` il peggiore `9.01e-15`** *(descrittivo)*.
- **C2, il rumore:** **per tick `123.78`; la deviazione delle `20` medie su `100` tick di `(0)_2000` `s_w = 2.09`** *(il rapporto `0.017`: l'oscillazione e' VELOCE rispetto a `100` tick, la media la toglie)*. **La premessa «cosa NON so» della sez. `8.1`: risolta.** **Le medie di `(0)_2000` stanno ferme attorno a `-46`** *(fra `-50.4` e `-42.96`: uno scarto COSTANTE dal primo tick, non una deriva; il perche' NON l'ho guardato)*.
- **C3, il lavoro dell'accensione di G** *(`Grampa` meno `(0)_2000`, finestra per finestra)*: **`+0.05` nei primi `100` tick, `-780` a `401`-`500`, `-4308` a `901`-`1000`, il minimo `-5433` a `1501`-`1600`, poi risale piano a `-5286` a `1901`-`2000`.** **`W = D(1250) - D(500) = -4175.6`, il rumore `2 s_w = 4.18`: `998` volte. Il DEVE FALLIRE fallisce come deve.** **Nella rampa `D(500) - D(50) = -1097.7`; dopo l'allargamento `D(1950) - D(1250) = -12.6`.**
- ### **C4:** **il bilancio non risolve l'energia del moto** *(qualche unita', sotto il rumore anche mediato? il rumore della media e' `2.1`: la stima del moto `-2.9` a `2000` e' DELL'ORDINE del rumore)*; **la domanda forza/colpetto passa alla coppia.** ### ⚠ **ERRORE MIO:** **la frase stampata dice «la coppia B1»** *(il mandato delle `09:34`)*; **dopo la decisione delle `09:38` la coppia e' B2** *(G+U)*: **il codice non e' stato aggiornato; il referto resta com'e', la correzione e' scritta qui.** **E la coppia oggi e' FERMA** *(la cottura di (MGU) fallita sul ramo)*.
- **C5:** **R-CONTI-6 nella ROTTA e la riga `5-ter` nella skill `registro-corse`.** **C6:** **sul ramo mattone** *(le letture)*.
- ### **LA VOCE `15` E' CHIUSA.**
