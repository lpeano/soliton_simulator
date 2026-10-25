# IL CENSIMENTO DELLE DECISIONI DI LUCA: NEL NUCLEO, NEGLI STRUMENTI, NEI DOCUMENTI *(sola lettura, `2026-10-25`)*

> **Il mandato:** di Luca, `2026-10-25` *(«abbiamo gia' regole che dovrebbero essere embeddate direttamente nel simulatore e che invece sono ancora in memoria», `15:52`)*; ### **il task history `doc/TASK_HISTORY/2026-10-25_censimento_decisioni.md`** *(`5f7099b7`)*; ### **la voce [[CENSIMENTO-DECISIONI]].** ### **Ogni riga col codice e' letta dal sorgente al blob di oggi** *(i numeri di riga invecchiano: si cerca per nome)*.

## 0. LA TABELLA RIASSUNTIVA

| | quante | nel nucleo | giustamente fuori | mancanze |
|---|---|---|---|---|
| le voci `DECISIONE` dell'indice *(decise, dopo le fusioni)* | `29` | `13` | `9` | ### **`7`** *(`1` libera, `6` bloccate)* |
| i nodi presi dell'albero | `5` | `4` | `1` | `0` |
| il registro della fisica dal `2026-10-08` *(non gia' nell'indice)* | `3` | `2` | `0` | `1` *(bloccata)* |
| i task history dal `2026-10-08` *(non gia' sopra)* | `11` | `6` | `5` | `0` |
| ### **IN TUTTO** | ### **`48`** | ### **`25`** | ### **`15`** | ### **`8`: `2` LIBERE, `6` BLOCCATE da una decisione aperta** |

### **E un gruppo a parte:** ### **le decisioni di PROCEDURA sugli STOP** *(una lettura, un criterio di un controllo, un braccio diagnostico: in `20` task history dal `2026-10-18` al `2026-10-23`)*: ### **stanno giustamente nei task history** *(sezione `4`)*.

### ⭐ **L'ORDINE PROPOSTO PER COLMARLE** *(una PROPOSTA, non una decisione; un interruttore alla volta)*:
1. ### **[[DECISIONE-SOLO-TRIANGOLI]]: la scena a triangoli nel nucleo** *(nessuna decisione aperta da cui dipende; sezione `5`)*;
2. ### **il criterio di [[DECISIONE-L1-NATURA-A-SIMULATORE-B]]** *(«e' fisico solo cio' che CONVERGE raffinando»)* ### **in `doc/PATTERN_DI_PROVA.md`**: ### **oggi sta solo in `doc/MAPPA_DIPENDENZE.md`** *(un documento, nessun codice)*;
3. ### **le sei bloccate, nell'ordine in cui si sbloccano:** ### **[[DECISIONE-LINEARE]]** *(dopo `S1` contro `S4`)*; ### **[[DOMANDA-VIA-DEL-CAMPO]]** *(dopo le scelte del `U(1)`, [[PROGETTO-U1]])*; ### **[[DECISIONE-DIREZIONE-STRADA-3]], [[DOMANDA-BANDE-O-SEGNO-LOCALE]] e la coesione** *(dopo le forme dell'ordinamento)*; ### **[[D-BILANCIO-NASCITA]]** *(dopo le forme della mitosi)*.

## 1. LE FONTI, LE QUERY, I NUMERI VISTI

| | il comando | il numero |
|---|---|---|
| `(F1)` | `python csv/indice.py cerca --classe DECISIONE` *(e la lettura di `doc/indice/voci.jsonl` per la descrizione e la chiusura)* | ### **`91` voci** *(`65` `AGENDA`, `16` `CHIUSA`, `6` `SUPERATA`, `4` `APERTA`)*: ### ⚠ **il task history diceva `93`: contavo due righe dell'intestazione. Si annota.** |
| `(F2)` | `doc/ALBERO_era2.yaml` letto con `yaml`, i nodi con `presa` | ### **`5` presi su `14`** *(`grep -c "presa: true"` da' `6`: una riga in piu' e' fuori da un nodo)* |
| `(F3)` | i task history dal `2026-10-08`, `grep -i "DECISIONE DI LUCA\|DECISA DA LUCA\|decisione di Luca d\|SCELTA DI LUCA"` | ### **`109` menzioni in `70` file** *(su `125` dal `2026-10-08`)* |
| `(F4)` | `doc/REGISTRO_FISICA.md`, lo stesso `grep` e le date dal `2026-10-08` | ### **`83` menzioni, di cui `6` decisioni dell'era `2`** *(le altre sono dell'era `1`, prima del `2026-10-08`)* |

### ⚠ **LA TRAPPOLA, scritta nel task history e confermata:** ### **la classe `DECISIONE` dice «serve una decisione», non «c'e' una decisione»:** ### **delle `91` voci `32` portano una decisione di Luca** *(`29` dopo le fusioni)* ### **e le altre `59` sono domande, conflitti o proposte ancora aperte** *(«DOMANDA APERTA PER LUCA», «TROVATO»)*, ### **e la decisa [[DECISIONE-SOLO-TRIANGOLI]] e' `AGENDA`.** ### **La classificazione decisa/aperta l'ho fatta LEGGENDO la descrizione e la chiusura** *(«DECISIONE DI LUCA», «DECISA DA LUCA», «SCELTA DI LUCA», «SCARTATA DA LUCA»)*, ### **dichiarato:** ### **un programma non potrebbe farlo** *([[DECISIONE-VUOLE-UN-CAMPO]]: lo stato «presa» di una voce dell'indice NON E' UN CAMPO)*. ### **E le fusioni:** ### **`DOMANDA-IL-LIMITE-DELLA-LUCE-SI-RAGGIUNGE` in [[DECISIONE-TICK-OROLOGIO-MASSIMO]]; `PROMOZIONE-CONSERVAZIONE-MODIFICATA` in [[D-ENERGIA]]; `DOMANDA-E-NON-SI-CONSERVA-A-X-UNO` in [[DECISIONE-VUOTO-MEDIATORE]]; la decisione `(A)` del registro sulla nascita in [[D-BILANCIO-NASCITA]]; la sorgente del `2026-10-15` in `DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA`.**

## 2. LE DECISIONI, UNA PER RIGA

### 2.1 Dall'indice *(`29`)*

| | la voce, la data | che cosa chiede | dove sta | giudizio |
|---|---|---|---|---|
| `1` | [[BASTA-PROTOTIPI]], `2026-10-12` | una regola di lavoro *(il banco congelato, si lavora in `primo_ordine`)* | `doc/CODA_2026-10-09.md` | giusto |
| `2` | [[BUDGET-COLLAUDI-500]], `2026-10-12` | un parametro dell'infrastruttura | ### **NEL NUCLEO:** `primo_ordine/collauda.py` | giusto |
| `3` | [[CS-LOCALE-DAL-VUOTO]], `2026-10-11` | una legge *(il tempo proprio dal vuoto)* | ### **NEL NUCLEO:** `primo_ordine/flussi_parziali.py`, `cs` *(riga `102`)*, `dtau_nodo` *(`76`)* | giusto |
| `4` | [[D-BILANCIO-NASCITA]], `2026-10-12` *(con la decisione `(A)` del `2026-10-08`)* | una legge *(chi paga la nascita)* | ### **DA NESSUNA PARTE:** `primo_ordine/crescita.py` e' di `11` righe; `motore.cresci` *(`280`)* permuta lo stato e basta | ### **MANCANZA BLOCCATA** *(`DEC-NASCITA-PSI`, `DOMANDA-MITOSI-LE-FORME`; il nodo `D7` non e' preso)* |
| `5` | [[D-ENERGIA]], `2026-10-12` *(superata da `DEC-QC-CONSERVATA`)* | una grandezza conservata | ### **NEL NUCLEO:** `primo_ordine/energia.py`, `totale` | giusto |
| `6` | [[DEC-Z47-TRANSIZIONE]], `2026-10-10` | l'indice | l'indice | giusto |
| `7` | [[DECISIONE-COMPOSIZIONE-SIMMETRICA]], `2026-10-15` | una legge *(il palindromo)* | ### **NEL NUCLEO:** `composizione.ORDINE`, `leggi.yaml` *(`14` pezzi, l'impronta `2e7f795d2a52fbe7`)* | giusto |
| `8` | [[DECISIONE-DIREZIONE-STRADA-3]], `2026-10-13` | un principio *(la `C` esatta nelle leggi, rotta nello stato)* | ### **IN PARTE:** la `C` si MISURA *(`primo_ordine/bande.py`)* ma ### **non e' dichiarata in tabella** *(`DOMANDA-DOVE-STA-LA-C-IN-TABELLA`)*; nessun termine d'ordinamento | ### **MANCANZA BLOCCATA** *(`DOMANDA-L-ORDINAMENTO-IN-H-O-NON-H`, `DOMANDA-DOVE-STA-LA-C-IN-TABELLA`)* |
| `9` | [[DECISIONE-L1-NATURA-A-SIMULATORE-B]], `2026-10-22` | un criterio di prova *(fisico e' cio' che converge raffinando)* | ### **`doc/PATTERN_DI_PROVA.md` dal `2026-10-25`**, la sezione «UN NUMERO E' FISICO SOLO SE CONVERGE RAFFINANDO» | ### **COLMATA** |
| `10` | [[DECISIONE-LINEARE]], `2026-10-22` | un criterio su una legge | ### **IL NUCLEO HA LA FORMA CHE LA DECISIONE ESCLUDE:** `CAMM-MATERIA-VUOTO` *(`leggi.yaml`, riga `506`)* e' `S3` | ### **MANCANZA BLOCCATA** *(`S1` contro `S4`, `doc/DOSSIER_S1_S4.md`)* |
| `11` | [[DECISIONE-M-B2-SI-LEGGE-SULLA-PENDENZA]], `2026-10-15` | una lettura di un collaudo | i collaudi *(la chiusura di `L1`, `de89549`)* | giusto |
| `12` | [[DECISIONE-SOLO-TRIANGOLI]], `2026-10-23` | una SCENA | ### **NEL NUCLEO dal `36040a07`:** `corrente.toro_spostamenti`, `scena_l2.scena_toro`, `GRIGLIA_DEL_MODELLO = "triangoli"` *(il sigillo `13/13`)*; ### **il driver resta sulla catena** *(una domanda)* | ### **COLMATA** *(gli strumenti di `csv/` usano ancora la loro funzione: il passaggio e' un lavoro a se', dopo)* |
| `13` | [[DECISIONE-STRADA-B-FLUSSI]], `2026-10-13` | una legge | ### **NEL NUCLEO:** `flussi_parziali.grover` *(`317`)*, `hop_psi` *(`378`)* | giusto |
| `14` | [[DECISIONE-TICK-OROLOGIO-MASSIMO]], `2026-10-13` *(`B-5`)* | un principio | ### **NEL NUCLEO:** `flussi_parziali._nel_cono` *(`226`)*, `dtau_rif` *(`61`)* | giusto |
| `15` | [[DECISIONE-VUOTO-MEDIATORE]], `2026-10-13` | una strada, FALLITA | niente | giusto |
| `16` | [[DOMANDA-BANDE-O-SEGNO-LOCALE]], `2026-10-13` | una forma *(il segno locale `q_h`)* | DA NESSUNA PARTE | ### **MANCANZA BLOCCATA** *(il termine d'ordinamento)* |
| `17` | `DOMANDA-OMEGA-E-UNITA-O-COSTANTE`, `2026-10-15` *(`B-4`)* | una legge *(`omega dtau_rif = pi`)* | ### **NEL NUCLEO:** `flussi_parziali.espi` *(`246`)* | giusto |
| `18` | `DOMANDA-PHI-REALE-O-COMPLESSO`, `2026-10-12` | una variabile | ### **NEL NUCLEO:** `leggi.yaml`, `phi_h` *(`97`-`98`, `complesso_estremita`)* | giusto |
| `19` | `DOMANDA-QUALE-TEMPO-PROPRIO-USA-L-ARCO`, `2026-10-15` *(`B-3`)* | una legge | ### **NEL NUCLEO:** `flussi_parziali.s_arco` *(`184`)* | giusto |
| `20` | `DOMANDA-QUALE-SCENA-3D-PRINCIPALE`, `2026-10-11` | un principio *(nessuna scena costruita per il simulatore: solo banchi)* | le scene del nucleo sono banchi *(`scena_l2`, `driver`)* | giusto ⚠ *(sezione `6`, contrasto `2`)* |
| `21` | [[DOMANDA-VIA-DEL-CAMPO]], `2026-10-12` | una legge *(la `U` d'arco dinamica)* | ### **SOLO NEGLI STRUMENTI:** `csv/_u1_prototipo.py` *(`U = I` nel nucleo)* | ### **MANCANZA BLOCCATA** *(`DOMANDA-U-DINAMICA-LE-FORME`; le scelte di [[PROGETTO-U1]])* |
| `22` | [[N-DIREZIONI-DI-MOTO]], `2026-10-15` | una legge della geometria | ### **NEL NUCLEO per il quadrato:** `scena_l2.versori_geometrici` *(`66`)*; ### **per i triangoli solo** `csv/_triangoli.versori` *(`97`)* | giusto *(va con la `12`)* |
| `23` | [[PIANO-2D-3D]], `2026-10-23` | un piano | `doc/PIANO_2D_3D.md` | giusto |
| `24` | [[SPIN-LEGATO-AL-MOTO]], `2026-10-10` | una legge | ### **NEL NUCLEO:** `leggi.yaml` `CAMM-MONETA-SPIN` *(`334`)*; `motore._moneta_spin` *(`464`)* | giusto |
| `25`-`27` | `SCARTATA-ECCESSO-NEL-SEME`, `SCARTATA-SAKHAROV-C-ESPLICITA`, `SCARTATA-SPOSTAMENTO-PIENO-SOLO-GROVER`, `2026-10-13` | niente *(scartate)* | niente | giusto |
| `28` | `DOMANDA-UN-NODO-SENZA-VUOTO-HA-L-OROLOGIO-FERMO`, `2026-10-17` | una regola sullo stato *(il vuoto nullo si rifiuta alla costruzione)* | ### **NEL NUCLEO:** `motore._vieta_vuoto_nullo` *(`210`)* | giusto ⚠ *(la voce non dice se la «lettura B» e' di Luca)* |
| `29` | `DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA`, `2026-10-16` *(con la sorgente del `2026-10-15`)* | una legge | ### **NEL NUCLEO:** `leggi.yaml` `CAMM-MATERIA-VUOTO` *(`506`)*; `motore.densita_materia` | giusto |

### 2.2 Dall'albero *(`5` nodi presi)*

| | il nodo | dove sta | giudizio |
|---|---|---|---|
| `30` | `DEC-CAM-CAMMINATA` *(`2026-10-10`)* | ### **NEL NUCLEO:** la camminata *(`motore.py`, `flussi_parziali.py`, `leggi.yaml`)* | giusto |
| `31` | `DEC-QC-CONSERVATA` *(`2026-10-16`)* | ### **NEL NUCLEO:** `energia.py`; il collaudo `_collauda_energia.py` | giusto |
| `32` | `DEC-D6-VUOTO` | ### **NEL NUCLEO:** `CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO` *(`leggi.yaml` `426`, `446`)* | giusto |
| `33` | `DEC-D6F-FORME-VUOTO` | ### ⚠ **`presa: true` ma la sua nota dice «queste sono le forme, e restano aperte»** | giusto *(contrasto `3`)* |
| `34` | `DEC-INT-INTEGRATORE` *(`2026-10-10`, «il LOCALE A STRATI»)* | ### **NEL NUCLEO:** la composizione dei pezzi *(`tick.percorri_tick`)* | giusto |

### 2.3 Dal registro della fisica, dal `2026-10-08` *(`3` non gia' sopra)*

| | la decisione | dove sta | giudizio |
|---|---|---|---|
| `35` | ### **`A16` e la riscrittura al primo ordine** *(`2026-10-08`)* | ### **NEL NUCLEO:** `primo_ordine/` intero | giusto |
| `36` | ### **il freno della coesione e' la `(c)`, entrambi** *(`2026-10-08`)* | DA NESSUNA PARTE | ### **MANCANZA BLOCCATA** *(`DEC-FC-COESIONE`, `presa: false`)* |
| `37` | ### **si toglie la sincronizzazione, perche' emergera'** *(`2026-10-08`)* | ### **NEL NUCLEO per assenza:** nessun termine di sincronizzazione | giusto |

### 2.4 Dai task history *(`11` non gia' sopra)*

| | la decisione, la data | dove sta | giudizio |
|---|---|---|---|
| `38` | la forma `cs = Lambda/(Lambda + Lambda_c)`, `2026-10-16` *(il valore di `Lambda_c` NON deciso)* | ### **NEL NUCLEO:** `flussi_parziali.cs` *(`102`)*; `Lambda_c` solo passato *(nessun valore predefinito)* | giusto |
| `39` | [[STRUMENTO-LEGGE-DALLA-TABELLA]], `2026-10-16` | ### **UN PRESIDIO:** `P-TAB` | giusto |
| `40` | `P-R1` ristretto al nucleo, `2026-10-16` | ### **UN PRESIDIO:** `P-R1` | giusto |
| `41` | la strada `(d)`, `2026-10-18` | ### **NEL NUCLEO:** `CAMM-FASE-VUOTO` *(`leggi.yaml` `577`)*; `energia_pesata.applica` | giusto |
| `42` | il punto medio per pezzo *(`2026-10-18`, `12:07`)* e la sua rimozione *(`21:48`)* | ### **NEL NUCLEO:** `tick.cs_al_centro` *(`130`)* | giusto |
| `43` | la tolleranza di `Omega`, strada `(b)`, `2026-10-19` | ### **NEL NUCLEO:** `energia_pesata.py` | giusto |
| `44` | `GIRI_MAX_OMEGA` da `120` a `200`, `2026-10-21` | ### **NEL NUCLEO:** `energia_pesata.py` *(`76`)* | giusto |
| `45` | `eps = 0.5` sui triangoli, `2026-10-21` | ### **NEL NUCLEO:** `leggi.yaml` *(`341`-`342`)*; `csv/_triangoli.EPS_MONETA` | giusto |
| `46` | lo specchio sul differenziale, `2026-10-23` | `doc/PATTERN_DI_PROVA.md` | giusto |
| `47` | il tempo dell'arco nel campo `F1`, `2026-10-25` | `csv/_u1_secondo.py`, `csv/_u1_prototipo.py` *(in memoria: la legge del campo NON e' decisa)* | giusto |
| `48` | il criterio di gauge contro la stima, `2026-10-25` | `doc/PATTERN_DI_PROVA.md` | giusto |

## 3. LE MANCANZE: CHE COSA SERVIREBBE

| | la mancanza | i file | il sigillo di riduzione al bit | la suite e l'impronta | dipende da |
|---|---|---|---|---|---|
| `12` | ### **la scena a triangoli** | `primo_ordine/corrente.py`, `scena_l2.py`, `driver.py`, lo schema della configurazione, `csv/_file_fisica.py` | sezione `5` | `collauda.py`; ### **l'impronta NON cambia** *(la scena non e' nell'ordine)* | ### **niente** |
| `9` | il criterio della convergenza raffinando | `doc/PATTERN_DI_PROVA.md` | -- | -- | niente |
| `10` | la forma `S1` o `S4` al posto di `S3` | `leggi.yaml` *(`CAMM-MATERIA-VUOTO`)*, i termini generati | il passo con la forma nuova al posto di `S3`: ### **il bit NON si conserva** *(cambia la legge)*: ### **la prova e' la riproduzione degli strumenti in memoria** *(`csv/_screening_forme_s3.py`)* | `collauda.py`; ### **l'impronta NO** *(lo stesso id)*; `H-REG-R` | ### **`S1` contro `S4`** |
| `21` | la `U` d'arco dinamica | `leggi.yaml` *(due pezzi nuovi)*, `stato.py` *(`A`, `E`)*, `motore.py` | ### **`A = E = 0`, `e = 0`: il passo di oggi al bit** *(`(a1)` di `0b6bfde8`)* | ### **l'impronta CAMBIA** *(`18` pezzi)* | ### **le scelte di [[PROGETTO-U1]]** |
| `8`, `16`, `36` | la `C` in tabella, il termine d'ordinamento, la coesione | `leggi.yaml`, lo schema | a termine spento, al bit | ### **l'impronta cambia se entra un pezzo** | ### **`DOMANDA-L-ORDINAMENTO-IN-H-O-NON-H`, `DEC-FC-COESIONE`** |
| `4` | chi paga la nascita | `crescita.py`, `motore.cresci` | a crescita spenta, al bit | -- | ### **`DEC-NASCITA-PSI`, le forme della mitosi, `D7`** |

## 4. LE DECISIONI DI PROCEDURA SUGLI STOP *(il gruppo a parte)*

### **Nei task history dal `2026-10-18` al `2026-10-23`** *(`memoria_e_punti_fissi`, `jeans_del_modello`, `tolleranza_omega`, `controllo_passo_materia_uniforme`, `instabilita_a_dtau_piccolo`, `stabilita_lineare`, `stabilita_intervallo_lungo`, `raffinamento`, `cure_candidate_s3`, `presidio_era_stato`, `base_proiettata`, `d0_risonanza`, `regressione_d0`, `moneta_gruppo_finito`, `s3_ripensata`, `s3_due_misure`, `screening_forme_s3`, `prova_grover`, `forza_da_cs`, `segno_gravita`)*: ### **un criterio di un controllo, una lettura di un verdetto, un braccio diagnostico, «si nominano e non si lavorano».** ### **Non chiedono niente al simulatore: stanno giustamente nei task history** *(e quando diventano un criterio di un TIPO di misura, in `doc/PATTERN_DI_PROVA.md`, come lo specchio, la `46`)*.

## 5. IL CASO DEI TRIANGOLI

- ### **OGGI, NEL NUCLEO:**
  - ### **`primo_ordine/driver.py`, `grafo`** *(riga `51`)*: ### **due scene a vocabolario chiuso, `catena` e `anello`** *(1D)*; ### **la configurazione `primo_ordine/config/prova.yaml`** *(righe `17`-`18`)*: ### **`scena: catena`.**
  - ### **`primo_ordine/scena_l2.py`, `scena`** *(`168`)*: ### **il toro QUADRATO** *(`corrente.toro`, `corrente.py` `237`: «grado `2 d`»)* ### **coi versori sugli assi** *(`versori_geometrici`, `66`)*; ### **la usano `_misura_forme_l2.py`, `_misura_pari_l2.py`, `_misura_statica_d.py`, `_misura_statica_l2.py`, `_misura_verso_l2.py`, `statica_protocollo.py`.**
  - ### **IL MOTORE E' GIA' GENERALE:** ### **`Incidenza` e `Motore` lavorano su un grafo qualunque** *(`csv/_triangoli.py` lo dice e lo usa: «il passo NON si tocca»)*.
- ### **OGGI, NEGLI STRUMENTI:** ### **`csv/_triangoli.py`:** ### **`toro_spostamenti(lati, spostamenti)`** *(`74`, generale in dimensione)*, ### **`versori(m, direzioni)`** *(`97`)*, ### **`scena_toro`** *(`112`)*, ### **`TRIANGOLI`** *(`60`)*. ### ⚠ **La trappola nota: `zip(c, s, lati)` TRONCA in silenzio se `lati` e gli spostamenti hanno dimensioni diverse.**
- ### **CHE COSA SERVIREBBE** *(una proposta di metodo; il codice in un mandato a se')*:
  1. ### **`corrente.toro` diventa il caso particolare di un `toro_spostamenti` nel nucleo** *(gli spostamenti = gli assi)*, ### **con l'assert sulle dimensioni** *(la trappola dello `zip`)*;
  2. ### **`versori_geometrici` diventa il caso particolare di `versori(m, direzioni)`;**
  3. ### **una scena `triangoli` nel vocabolario di `driver.grafo` e dello schema della configurazione, coi `lati`;** ### **`scena_l2.scena` con la griglia ESPLICITA** *(nessun `default`: `P-R1` ha il tetto ZERO, quindi ogni chiamante la passa)*;
  4. ### **il file nella LISTA di `csv/_file_fisica.py`** *(`H-FISICA-FUORI-LISTA`)* ### **e i rami dichiarati** *(`P-R1`)*.
- ### **IL SIGILLO CHE LO PROVA:** ### **`(i)` il quadrato AL BIT:** ### **`corrente.toro(lati)` = `toro_spostamenti(lati, assi)` byte per byte, e ogni scena di oggi identica** *(ogni attributo, come `_triangoli_forza.byte_attr`)*; ### **`(ii)` i triangoli AL BIT contro lo strumento:** ### **la scena del nucleo = `csv/_triangoli.scena_toro(TRIANGOLI, (32, 32), ...)`, ogni attributo, e un tick identico;** ### **`(iii)` DEVE FALLIRE per la chiave giusta:** ### **`lati` di due elementi con spostamenti di tre: l'assert alza** *(la trappola chiusa)*; ### **`(iv)` `collauda.py` intero; l'impronta `2e7f795d2a52fbe7` INTATTA.**

## 6. I CONTRASTI *(riportati, NON corretti)*

1. ### **Il numero del task history:** ### **`93` voci `DECISIONE`; sono `91`** *(sezione `1`)*.
2. ### **`DOMANDA-QUALE-SCENA-3D-PRINCIPALE`** *(«niente scena costruita per il simulatore»)* ### **contro le scene del nucleo** *(il quadrato di `scena_l2`, la catena del driver)*: ### **le leggo come BANCHI, e la decisione lo permette;** ### **ma [[DECISIONE-SOLO-TRIANGOLI]] dice che la fisica si misura sui triangoli, e i banchi del nucleo sono quadrati e 1D.**
3. ### **`DEC-D6F-FORME-VUOTO` e' `presa: true`, e la sua nota dice che le forme «restano aperte».**
4. ### **[[DECISIONE-LINEARE]] esclude `S3`, e `S3` e' la legge che gira nel nucleo:** ### **e' corretto finche' `S1` contro `S4` e' aperta** *(nessuna delle due e' derivata)*, ### **ma vuol dire che il nucleo gira con una forma che una decisione di Luca ha escluso.**
5. ### **[[DEC-ALBERO-CINQUE-SENZA-ARGOMENTO]]:** ### **«la lista numerata delle decisioni di Luca NON E' NEL REPO»** *(le decisioni `1`, `3`, `10` citate dai mandati)*: ### **il censimento la conta dove si trova, e non la ricostruisce.**

## 7. GLI AGGIORNAMENTI

- ### **`2026-10-25`: la mancanza `12` colmata in `36040a07`** *(la scena a triangoli nel nucleo)*; ### **il passaggio degli strumenti di `csv/` alla funzione del nucleo, e la rinomina di `scena_l2.scena`, sono un lavoro a se', da fare dopo.** ### **La parte C** *(`S1` provvisoria)* ### **NON eseguita** *(la precisazione di Luca delle `17:38`)*: ### **la mancanza `10` resta.**
- ### **`2026-10-25`: la mancanza `9` colmata** *(il criterio della convergenza in `doc/PATTERN_DI_PROVA.md`, col caso di [[V-MAX-DIREZIONI]])*.
