# ERA `2`, L'INFRASTRUTTURA: **codice generato da una tabella di leggi**

> **Mandato di Luca del 2026-10-09**, sei tappe. ### **Nessuna fisica nuova**; simulatore
> `b8c21049` intatto, ### **non si tocca.**
>
> ### ⚠ **Si committa e si pusha PRIMA del lavoro** *(par.8)*, e ### **a OGNI tappa**: il PC
> si riavvia fra `00:00` e `02:00`, quindi ### **ogni tappa deve lasciare il repo valido.**

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⭐ **IL PRINCIPIO, COME L'HA SCRITTO LUCA**
> *«La tabella delle leggi è l'UNICA fonte. Codice e scheda si GENERANO; la macchina verifica
> che legge ↔ file ↔ voce dell'indice ↔ scheda siano in biiezione, e che nulla cambi senza
> che cambi la tabella.»*

### **CIÒ CHE HO VERIFICATO PRIMA DI CREDERCI**

| | il fatto, misurato |
|---|---|
| `doc/indice/leggi.jsonl` | ### **esiste**, `21` righe, chiavi `id titolo ancora variabile classe_traduzione fonte`. ### ⛔ **NON ha il campo `era`**, e le `21` sono ### **ancore di traduzione dell'era `1`** |
| `doc/indice/variabili.jsonl` | ### **esiste**, `44` righe, chiavi `id nome censita_in scritta_da scritture` |
| `sympy` | ### **c'è**, `1.14.0`. `numpy` `2.3.0`, `yaml` `6.0.3` — ### **nessuna dipendenza da installare** |
| `primo_ordine/` | ### **NON esiste**, e `H-FISICA-FUORI-LISTA` la sorveglia già *(nome dato da Luca stamattina)* |

### ⛔ **E IL PRIMO OSTACOLO È UN PRESIDIO CHE HO SCRITTO IO STAMATTINA**

*«Aggiungi ogni file alla LISTA di `csv/_file_fisica.py` nel commit in cui nasce»* —
### **e `csv/_hook_fisica.py` e `csv/_presidio_commenti_flag.py` hanno
`assert len(FILE_FISICA) == 1`**, con il commento *«va esteso, non adattato»*.

### ✔ **Lo estendo, e la via è una DISTINZIONE, non un ciclo:** la LISTA ha
### **due consumatori con scopi diversi**, e li separo dichiarandolo —

| | chi legge | che cosa |
|---|---|---|
| `FILE_FISICA` | ### **`H-FISICA-FUORI-LISTA`** e ### **`H-ID-OBBLIGATORIO`** | ### **tutti** i file di fisica: è lo scopo di quei due |
| **`SCHEDA_NEL_REGISTRO`** *(nuova)* | ### **`H-REG-R`** e ### **`H-P7`** | ### **solo i file la cui SCHEDA vive in `doc/REGISTRO_FISICA.md`** — oggi `soliton_simulator.py` |

### ⭐ **Il perché non è una comodità:** la scheda di una legge dell'era `2`
### **si GENERA in `doc/leggi_era2/<id>.md`** *(tappa `3`)*. ### ⛔ **Pretendere che stia
anche in `REGISTRO_FISICA.md` vorrebbe dire DUE posti per la stessa scheda, e due copie
divergono** — è il difetto che ho pagato due volte in tre giorni *(la regola di `superata_da`
duplicata, e il numero dei hook nel titolo del §`12`)*.

### **COSA CREDO, TAPPA PER TAPPA**

| | cosa credo PRIMA di guardare |
|---|---|
| `1` **la struttura** | nessuna difficoltà: file vuoti con intestazioni. ### ⚠ **Il punto delicato è la LISTA** *(sopra)*, e va fatto ### **nello stesso commit**, altrimenti `H-FISICA-FUORI-LISTA` ### **rifiuta il commit che crea i file** |
| `2` **il formato** | `yaml` con uno schema validato. ### ⭐ **Le decisioni `9` e `13` sono APERTE, quindi il formato le AMMETTE senza scegliere:** il tipo `coppia_coniugata (q,p)` ### **esiste nel vocabolario e NESSUNA legge lo usa**; la geometria ### **non è rappresentabile**, perché `pos` non è un simbolo ammesso *(`A17`)* |
| `3` **il generatore** | `sympy` con `psi` e `psi*` ### **simboli indipendenti** — è l'unico modo di avere `dH/dpsi*` come derivata di Wirtinger. ### ⚠ **Non so come sympy si comporti con `Dagger` su matrici `C^2`**: lo misuro |
| `4` **i presidi** | `P-E1`…`P-E8`. ### ⛔ **Senza via d'uscita per `primo_ordine/`**, e il mandato lo dice: ### **la prima volta che un presidio non ha scappatoia** |
| `5` **il collaudo** | i due termini di PROVA. ### **L'integratore è una DECISIONE APERTA**, e il mandato chiede di dichiarare quale uso e perché |
| `6` **il referto** | cosa blocca, cosa è regola scritta, i numeri, e le domande |

### ⭐ **L'INTEGRATORE: dichiaro la scelta e il perché, e resta di Luca**

### **Uso il PUNTO MEDIO IMPLICITO** *(implicit midpoint)*:
`psi_{n+1} = psi_n - i·dt·(dH/dpsi*)((psi_n + psi_{n+1})/2)`, risolto per
### **punto fisso**.

| | perché |
|---|---|
| ### **è SIMMETRICO** | quindi ### **non ha deriva SECOLARE** dell'energia: l'errore oscilla, non cresce |
| ### **conserva ESATTAMENTE gli invarianti QUADRATICI** | e la ### **norma** è quadratica: `|psi|²` si conserva ### **al bit**, non entro tolleranza |
| ### ⛔ **l'alternativa `RK4` DERIVA** | è più accurato per passo e ### **perde energia monotonamente**: su una corsa lunga è la cosa sbagliata |
| ### ⚠ **il prezzo** | è ### **implicito**: serve un'iterazione per passo, e ### **va dichiarato quante** |

### **COSA NON SO**

1. ### **se `sympy` deriva `dH/dpsi*` come voglio** su un `psi` che è un vettore `C^2`
   *(`A16`)*. Se non lo fa, ### **lo riduco a componenti** — e lo dico;
2. ### **quante iterazioni di punto fisso** serva il punto medio implicito;
3. ### **quanto deriva l'energia**, e la tolleranza la dichiaro ### **prima** di misurarla:
   ### **norma entro `1e-13` relativo** *(deve essere esatta)*, ### **energia entro `1e-6`
   relativo su `1000` passi**;
4. ### **se `leggi.jsonl` tollera il campo `era`** sulle righe nuove senza che il validatore
   rifiuti le `21` vecchie.

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, e cosa mi FERMA*

| tappa | cosa decide | cosa mi FERMA |
|---|---|---|
| `1` | la struttura, e ### **la LISTA estesa** | ### ⛔ **se `H-FISICA-FUORI-LISTA` rifiuta il commit che crea i file**, l'ordine è sbagliato e va rifatto: ### **i file e la LISTA nello STESSO commit** |
| `2` | il formato, e ### **che le decisioni `9` e `13` siano AMMESSE e non scelte** | ### ⛔ **se mi trovo a scegliere la geometria o i coniugati, MI FERMO**: il mandato dice *«nessuna decisione di fisica»* |
| `3` | il generatore, e ### **`dH/dpsi*` simbolica** | ### ⛔ **se la derivata generata non coincide con la differenza finita**, il generatore è sbagliato: ### **non si aggiusta la tolleranza** |
| `4` | gli otto presidi, ### **bloccanti e senza via d'uscita** | ### ⛔ **se un presidio non ha un caso che DEVE fallire, non è un presidio** *(`P1-sexies`)* |
| `5` | il collaudo della catena, e ### **i sei casi che DEVONO fallire** | ### ⛔ **se UNO dei sei passa, mi fermo**: un presidio che non impedisce ### **è una tenda**, e l'ho già scritto quattro volte |
| `6` | il referto e le domande | — |

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | la lettura, fissata adesso |
|---|---|
| ### **la norma** | `sum(|psi|²)` si conserva entro ### **`1e-13` relativo** su `1000` passi. ### **È un invariante quadratico del punto medio implicito: deve essere ESATTA** |
| ### **l'energia** | `H(psi)` entro ### **`1e-6` relativo** su `1000` passi, e ### **senza tendenza monotona** *(si stampa la deriva, non solo il massimo)* |
| ### **`dH/dpsi*`** | la derivata generata contro la ### **differenza finita centrata** con `h = 1e-6`: concordanza entro ### **`1e-7` relativo** |
| ### **«un termine di nodo non vede i vicini»** | i simboli liberi dell'espressione sono ### **dentl'ambito dichiarato**, e per un `termine_nodo` l'ambito ### **non può contenere variabili d'arco né indici di vicino** |
| ### **`pos`** | il simbolo `pos` *(e `pos_x`, `pos_y`, `pos_z`)* ### **non esiste**: il generatore lo rifiuta ### **per costruzione** *(`A17`)* |
| ### **«PROVA»** | i due termini portano ### **`prova: true` nella tabella** e ### **una voce dell'indice che lo dice nel titolo**: ### **non sono fisica decisa** |

### ⛔ **E UNA COSA CHE NON FARÒ, dichiarata prima:** ### **non scrivo una legge che non sia
uno dei due termini di PROVA.** Il mandato dice *«nessuna fisica nuova»*, e
### **l'infrastruttura si collauda con due termini dichiarati finti** — non con la fisica
vera, che ### **non è decisa.**

---

## ③ TODO DEL NEXT STEP — *la lista operativa*

- [ ] `1` — la struttura + ### **la LISTA estesa** *(`SCHEDA_NEL_REGISTRO`)*
- [x] `2` — `leggi/leggi.yaml`, ~~`leggi/osservatori.yaml`~~, lo schema validato

  > ### ⚠ **ANNOTAZIONE DELLA TAPPA `5b`** *(e NON una riscrittura: il par.`8` dice che un ragionamento rivelato sbagliato ### **si ANNOTA**)*. ### ⛔ **`leggi/osservatori.yaml` E- STATO TOLTO.** L-avevo progettato ### **separato** perche- *«un osservatore non e- fisica, e tenerlo con le leggi inviterebbe a scriverci una legge travestita da misura»*. ### **Il ragionamento era buono e la forma sbagliata:** quella separazione decide ### **dalla posizione del file** cio- che va deciso ### **da un campo** *(`tipo: osservatore`)* — ed e- ### **la stessa forma dell-errore** che il principio della coda nomina. ### **Costava DUE fonti e DUE biiezioni, e il file era VUOTO e nessuno lo leggeva.** `PROVA-NORMA` sta in `leggi.yaml`, con gli altri.
- [ ] `3` — `_genera.py`: ambito, `dH/dpsi*`, modulo numerico, scheda
- [ ] `4` — `P-E1`…`P-E8`, e ### **la CI su GitHub**
- [ ] `5` — il collaudo della catena e ### **i sei casi che DEVONO fallire**
- [ ] `6` — `doc/REFERTO_infrastruttura_era2.md`

### **LE CINQUE DOMANDE DI `doc/STELLA_POLARE.md`** *(`L-STELLA`)*

| | la risposta |
|---|---|
| `A14` *(una cura non aumenta le leggi)* | ### **le leggi passano da `0` a `2`, e le DUE sono dichiarate PROVA**: non sono fisica. ### **La tabella ne conta `2` e l'indice le marca `PROVA` in biiezione** |
| il gradino di `ROBUSTEZZA-FISICA` | ### **sale**, e si misura: `8` presidi nuovi ### **bloccanti e senza via d'uscita**, piu' la ### **CI** — e la CI e' la prima volta che un presidio gira ### **fuori dal PC di Luca** |
| numeri o leggi aggiunti, e di che tipo | ### **due parametri**: `K` *(hopping)* e `g` *(locale)*, ### **entrambi dichiarati `PROVA` con origine «valore di prova, NON derivato»** — e `A1` lo pretende scritto |
| verso `EM`-curvatura | ### **niente**: nessuna legge di fisica entra. ### **L'infrastruttura e' neutra** |
| emergente o imposto | ### **nessuno dei due**: non c'e' fisica. ### ⭐ **Ma il FORMATO e' costruito perche' la fisica sia IMPOSTA IN UN SOLO POSTO** *(la tabella)* e ### **derivata altrove** — e questo e' il contrario di come l'era `1` e' cresciuta |

## LA STELLA POLARE — ### **le cinque risposte, PER LA TAPPA `5`** *(`L-STELLA`)*

> ### ⚠ **`passo.py` E- UN FILE DI FISICA**, e il mandato dice *«nessuna fisica nuova»*. ### **Le due cose stanno insieme solo se le cinque domande hanno una risposta scritta**, e *«non si applica»* senza il perche- ### **non e- una risposta.**

| | la risposta |
|---|---|
| **`1` `A14`, conservazione LOCALE** | ### **NON SI APPLICA ALLE LEGGI, E SI APPLICA ALLO SCHEDULATORE** — e il perche-: le due leggi in tabella sono `prova: true` e ### **non pretendono di conservare niente.** ### ⭐ **Ma lo SCHEDULATORE puo- rompere una conservazione che le leggi avrebbero**, e questa e- la ragione della composizione simmetrica. ### **MISURATO:** la norma si conserva a ### **`1.2e-15`** *(globale)* e ### **`2.0e-15`** *(locale)* su `200` passi, l-energia a ### **`3.9e-5`** per entrambi |
| **`2` quale dei TRE GRADINI** | ### **(a) ROBUSTO AL RUMORE NUMERICO, e SOLO quello.** ### ⛔ **Non (b) e non (c):** non c-e- nessuna legge pratica da togliere, e ### **nessun limite noto da ritrovare** — le leggi sono di prova. ### **Il gradino (a) e- raggiunto nel senso preciso che le permutazioni dichiarate byte-identiche LO SONO AL BYTE**, misurato, e quelle dichiarate diverse ### **differiscono** |
| **`3` aggiunge un numero o una legge?** | ### **AGGIUNGE DUE NUMERI, e sono di un tipo che la domanda `3` non elenca:** `iterazioni=64` e `toll=1e-14` del punto fisso. ### ⛔ **NON sono costanti di accoppiamento, non sono toppe, non sono clip: sono PARAMETRI DEL RISOLUTORE** — `A17`, lo strumento non e- fisica. ### ⚠ **MA UNO DEI DUE SI E- RIVELATO VISIBILE NELLA FISICA:** ### **il cono dell-integratore GLOBALE dipende da `toll`** *(`3` archi a `1e-4`, `5` a `1e-8` e a `1e-14`)*. ### ⭐ **Quindi `toll` NON e- innocuo**, ed e- ### **la ragione piu- forte contro il globale** nella tavola della tappa `6` |
| **`4` tocca `rho`, `c_s` o il SEGNO?** | ### **NO**, e il perche-: lo stato dell-era `2` e- ### **solo `psi`** *(`stato.py`, una variabile)*. `rho` e `c_s` ### **non esistono ancora**, e il segno che c-e- — il `-i` di `dpsi/dt = -i dH/dpsi*` — ### **non e- una scelta: e- l-equazione del moto** |
| **`5` emergente o imposto** | ### **NON SI APPLICA, e il perche-: non si afferma nessun FENOMENO.** ### ⛔ **Questa tappa non misura un comportamento del mondo: misura CHE LO STRUMENTO FACCIA CIO- CHE DICE** — cono, permutazioni, deriva. ### ⚠ **E la domanda `5` tornera- VERA e OBBLIGATORIA** al primo risultato di fisica dell-era `2`, che ### **non e- questo** |

### ⭐ **E LA DOMANDA `3` HA FATTO IL SUO LAVORO:** ### **mi ha fatto trovare che `toll` si vede nella fisica.** Avevo in testa di dichiararlo *«parametro del risolutore, `A17`, non e- fisica»* e ### **chiudere li-.** ### ⛔ **E- la risposta che ha preteso di dire DI CHE TIPO e- il numero a costringermi a guardare, e guardando il cono del globale si e- rivelato DIPENDENTE DA LUI.**
