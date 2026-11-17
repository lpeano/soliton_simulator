# LA MITOSI DELL'ERA 2: LA CARTA *(Luca `2026-11-17` `09:49`, il mandato unico, C3; SOLO CARTA, FERMO prima di ogni codice)*

> **Che cosa e':** il progetto del primo passo della mitosi -- **un nodo nasce dividendo un arco, sul reticolo triangolare, con una DISLOCAZIONE** *(la via (B) di [[DEC-D9-GEOMETRIA]])*. **Che cosa NON e':** codice, una decisione nuova, una corsa. **Le decisioni** sono nelle note dell'albero *(C1, `938fa9dc`)*; **la prova della simmetria C** *(C2)* decide [[DEC-FC-COESIONE]].
> **Le fonti dei fatti dal codice:** letti da un agente in sola lettura e **ricontrollati da me sul sorgente** dove scritto *«[codice]»*; *«[doc]»* = letto in un documento o referto. **Si cerca per nome di funzione, mai per riga.** **Le regole che valgono qui:** R-QUALITA' *(la ROTTA, `c076265a`)*, A11 *(nessun clip senza cercare l'errore)*, `9-ter` *(una cura non aumenta le leggi)*.
> **I documenti di prima che questa carta NON sostituisce:** `doc/PROGETTO_MITOSI.md` *(l'era `1`, l'era `2`, le scelte aperte)*; `doc/CONTRATTO_nascita.md` *(il contratto della nascita dell'era `1`: l'ordine degli estratti casuali e delle somme, generato da `csv/_contratto_nascita.py`)*.

> ### ⛔ **L'ESITO DI C2, PRIMA DI LEGGERE IL RESTO** *(`doc/referti_l2/simmetria_C.txt`, `simmetria_C_pezzi.txt`; `92948daf`, `7782ef70`)*: **la coniugazione di carica antiunitaria NON e' una simmetria di G+U** *(fra `32` candidati, dopo `10` tick il migliore `2.976e-01` sul mattone; la rompono Grover e lo spostamento della materia, la fase materia-vuoto, `fase_a`, la reazione)*. **Quindi [[DEC-FC-COESIONE]] RESTA APERTA, e [[DEC-D7-DIVISIONE]] non si puo' prendere** *(P-ALB)*. **Questa carta NON dipende da FC per il disegno** *(la geometria, lo stato, i costi)*, **ma la regola della nascita resta non presa finche' Luca non decide che cosa vuol dire «la stessa azione sulle due bande» per questa camminata.**

## 0. CIO' CHE IL CODICE DI OGGI GIA' SA FARE, E CIO' CHE NO

- **[codice] Il NUCLEO non assume ne' il grado `6` ne' `n = L x L`.** `primo_ordine/incidenza.py`, `Incidenza`: gli archi in `_ii`, `_jj` con capacita' che RADDOPPIA *(`CRESCITA = 2`, `_allarga`)*; **l'arco `k` possiede le estremita' `2k` e `2k+1`**; `_derivati` costruisce `nodo`, `offset` e la CSR `estremita`; **il grado e' `diff(offset)`**. **`Incidenza.cresci(tieni, nuovi_ii, nuovi_jj, nodi_nuovi)`** e' **l'unico punto di scrittura**: gli archi nuovi in coda, `n += nodi_nuovi`, `GR.controlla` *(P-GRAFO)*, e **restituisce la permutazione delle estremita' `dove`** *(`-1` per quelle morte)*.
- **[codice] `Motore.cresci(tieni, nuovi_ii, nuovi_jj, nodi_nuovi, iniziali)`**: dentro un tick aperto, **al piu' una volta per tick**; chiama `inc.cresci`; **permuta SOLO `psi_h` e `phi_h`**, e **le estremita' nuove prendono `iniziali`** *(senza: `assert`, nessun default di fisica)*. ### **NON fa crescere:** `psi`, `Lambda`, `rho`, `h_int` *(per nodo)*, `mot.dtau`, `mot.cs`, `geo.n`, `geo.U`, e non rifa' i controlli di `Geometria`. **`primo_ordine/crescita.py`: SOLO L'INTESTAZIONE** *(«TAPPA 1»; chiede `ingressi`, `uscite`, `bilancio` dichiarati)*, **non importato da nessuno.**
- **[codice] FUORI dal nucleo il grado `6` e il reticolo sono CABLATI:**
  - `csv/_u1_prototipo.py`, `Campo.__init__`: **`m = 3 n`**, gli archi ESATTAMENTE `a1`, `a2`, `a1 + a2` da ogni nodo, le placchette da `3 v + a`, `ingressi = reshape(n, 3)`, `div` con `E.reshape(n, 3)`: **la U(1) di oggi NON PUO' crescere** *(e `_u1_oggi.campo_della_scena` eredita l'assert)*;
  - `csv/solitone/mattone.py`, `scena`: `righe = argsort(nodo).reshape(n, 6)`, `m1 = v // L`, `m2 = v % L`; `ritaglia`/`incolla` con l'aritmetica degli indici e i passi multipli di `3` *(il motivo di F3)*; **sei strumenti usano `Z["righe"]`** *(`convergenza`, `convergenza_243`, `coppia_lunga`, `fase_nel_tempo`, `legame`, `legati`)*;
  - `csv/solitone/bordo.py`, `g_estremita`: la distanza dagli indici del toro *(`v // L`, `v % L`, `9` immagini)*;
  - `csv/_solitone_dal_fondo.py`, `fondo_con_fasi`: **il vuoto F3 per classe di direzione d'arco** *(`DIREZIONI = ((0,1),(1,0),(1,1))`; un arco fuori reticolo e' un `ValueError`)*;
  - `primo_ordine/scena_l2.py`: `versori` assume l'arco `k = v d + a`.
- **[codice] Le coordinate:** **lo stato NON ha posizioni** *(«il simbolo `pos` non esiste»)*; `toro.posizioni`/`scarti` le ricavano dagli INDICI. **Un nodo nuovo NON ha coordinate**: servira' un array di posizioni FUORI dal nucleo.

### ⭐ **LA CONSEGUENZA PER IL PIANO:** **il nucleo e' gia' quasi pronto** *(la CSR, `cresci`)*; **cio' che non cresce sono i dati PER NODO del motore** *(`psi`, `Lambda`, `rho`, `h_int`, `dtau`, `cs`, `geo`)* **e TUTTO lo strato della U(1) e degli strumenti, cablato sul reticolo.** **Il primo codice della mitosi tocca il nucleo** *(far crescere i dati per nodo in `Motore.cresci`)*, **e il nucleo e' CONGELATO** *(`doc/NUCLEO_CONGELATO.md`)*: ### **serve una decisione di Luca per scongelarlo, prima di ogni riga.**

## 1. LA DIVISIONE D'ARCO SULLA VIA (B): LA DISLOCAZIONE

- **La mossa elementare** *(proposta; la divisione d'arco)*: **un arco `(i, j)` si divide; nasce il nodo `n` al suo punto medio.** Sul reticolo triangolare, perche' la rete resti fatta di TRIANGOLI *(R-SOLO-TRIANGOLI: [[DECISIONE-SOLO-TRIANGOLI]])*, **`n` si lega a `i`, a `j` e ai due vertici opposti `k`, `l` dei due triangoli che avevano `(i, j)` come lato.** **Il bilancio dei gradi:** `n` nasce di grado `4`; `i` e `j` restano di grado `6` *(perdono `j`/`i`, guadagnano `n`)*; **`k` e `l` passano da `6` a `7`.** **E' esattamente la mossa misurata nell'era `2` sulla carta** *(`doc/referti_l2/divisione_vuoto.txt`: «n (grado 4) ... k (grado 7), l (grado 7)»)*.
- ### **IL DIFETTO: un `4` e due `7` non sono una dislocazione.** **Una dislocazione e' una coppia `5`-`7`.** **La via (B) chiede «i difetti con `5` e `7` vicini, concentrati»**: **la mossa minima che la produce e' la divisione d'arco SEGUITA da un FLIP** *(lo scambio della diagonale di un rombo che tocca `n`: `n` sale a `5`, un vicino scende da `7` a `6`)*. **Il flip e' gia' misurato sulla carta** *(stesso referto: «il flip», `Delta H -0.2603` per tutte le regole)*. **Quale flip, fra quelli possibili attorno a `n`: una SCELTA da derivare, non da tarare** *(A1)*: **la proposta e' il flip che minimizza `|Delta H|` del vuoto, con una regola di parita' DETERMINISTICA** *(vincolo (c) di [[DEC-D7-DIVISIONE]])* **per i pari merito.** ### **DA DECIDERE (Luca):** la mossa e' «divisione + flip» oppure la sola divisione con il `4` e i due `7` lasciati, da rilassare poi.
- **Il disegno** *(una dislocazione, prima e dopo)*:

```
   prima (tutti di grado 6)              dopo la divisione di (i,j)          dopo il flip k-n -> (i,l)?  (da derivare)
          k                                     k(7)                                   k(6)
         / \                                   /|\                                    /  \
        /   \                                 / | \                                  /    \
       i-----j                               i--n--j          ->   un 5 (n) e un 7 vicini: la dislocazione
        \   /                                 \ | /
         \ /                                   \|/
          l                                     l(7)
```

- **LA NUMERAZIONE DEI NODI NUOVI senza rompere i buffer:** **[codice] `Incidenza.cresci` mette gli archi nuovi IN CODA e `n += nodi_nuovi`**: **i nodi nuovi prendono gli indici `n, n+1, ...`**, **gli archi tolti** *(`tieni = False`)* **escono e le estremita' si rinumerano con `dove`.** **Nessun nodo esistente cambia indice.** **I buffer del motore** *(`_b(nome, forma, tipo)`, chiave la forma)* **si rifanno alla forma nuova: `Motore.cresci` svuota `_buf`.** **[codice] Le capacita' raddoppiano** *(`CRESCITA = 2`)*: **la copia avviene `log2` volte, non a ogni nascita** *(sez. `6`)*.

## 2. LO STATO DEL NODO NUOVO, GRANDEZZA PER GRANDEZZA *(A7b)*

| la grandezza | la regola | la fonte | la prova |
|---|---|---|---|
| `psi` *(del padre e del figlio)* | **`psi -> psi / sqrt(2)` al padre e al figlio, la stessa fase** | [[DEC-D7-DIVISIONE]] *(la regola confermata da Luca, `2026-10-25`)* | **la norma della materia** conservata alla soglia della NORMA *(passi x eps: la nota di D7 misura `(1/sqrt 2)^2 - 0.5 = -1.11e-16`, non al bit)* |
| `psi_h` sulle estremita' nuove | **da derivare dalla `psi` del nodo** *(il motore lavora per estremita')*: **la proposta: la stessa `psi_h` per ogni estremita' del nodo, scalata** -- **ma la camminata NON ha `psi` per nodo come fonte:** `psi` e' DERIVATA *(da verificare nel codice prima della regola)* | da scrivere | il giro `+1` conservato attorno a ogni anello *(vincolo (a))* |
| `phi_h` sulle estremita' nuove | **la parte APERTA:** la regola v1 *(D7 applicata a `phi`)* **libera `Delta H = -8.548`** *(sul reticolo `L 24` della carta)* **e il vuoto uniforme non lo assorbe** *(`d999cca7`; la via (3) di Luca del `2026-10-26`)*; **v2-v5 fra `-0.0453` e `-0.3008`, e nessuna conserva insieme `V` e `Delta H = 0`** *(`doc/referti_l2/divisione_vuoto.txt`)* | [[DEC-D6F-FORME-VUOTO]] *(le forme di oggi: F3, un flusso con una fase per direzione)* | il vuoto lontano invariato *(la prova di D6f)* |
| `A`, `E` sugli archi nuovi | **Gauss VERO dopo la nascita** *(`div E = e (rho - media)` sul grafo nuovo)*; **il flusso attorno ai triangoli nuovi conservato** *(la somma di `A` sul bordo dei due triangoli divisi = quella dei triangoli vecchi)*; **il giro conservato** | QC *(la carica di U: C1)* | **Gauss AL BIT dopo ogni nascita** |
| il lapse, `dtau`, `cs` | **dalla legge, sul nodo nuovo** *(il lapse `N(rho)` e' funzione locale: si ricalcola, non si eredita)* | il motore | **[codice] oggi `Motore.cresci` NON fa crescere `dtau` e `cs`: va aggiunto** |
| `Lambda`, `rho`, `h_int` | **derivate:** si ricalcolano dopo la nascita | il motore | lo stesso |
| i pesi d'arco *(`w_a`, la media armonica B-3)* | **dalla legge** | QC *(il generatore pesato)* | il secondo ordine dell'energia conservato *(la nota di QC)* |

- **[doc] Il vincolo della carta nella sez. `1` del referto `divisione_vuoto.txt`:** **la materia perde `-0.0648` con D7 su `psi`, e NESSUNA regola su `phi` la tocca.**
- ### ⚠ **UN DIFETTO DI PROVENIENZA, scritto qui** *(Q-A1)*: **il referto `divisione_vuoto.txt` porta in testa «`_divisione_vuoto.py` ... !! MODIFICATO rispetto a HEAD -- i byte che girano NON sono quelli committati»**: **i suoi numeri sono di un sorgente non committato.** **Prima di usarli in un sigillo: rigirarli dal commit.**

## 3. CHI PAGA, IN NUMERI

- **La decisione `10`** *(PRESA in `3e8375b6`)*: **il calore paga la nascita, e LA SOGLIA E' IL BILANCIO.** **QC:** il bilancio si scrive **sulle NORME** *(esatte)* **e sull'energia** *(al secondo ordine: il generatore pesato `G`)* -- **un bilancio che pretenda l'esattezza va scritto sulle norme, o dichiarato approssimato** *(la nota di QC)*.
- **Le voci del bilancio di una nascita** *(da misurare, non da scegliere)*: **(i) la tensione dell'arco diviso** *(il quanto di olonomia: la fase della `U` d'arco, che sull'arco diviso si spartisce fra due archi)*; **(ii) il termine `Lambda` del vuoto** *(la densita' locale del vuoto, che la v1 dimezza: `6 -> 3` al nodo `n` e a `i`, referto)*; **(iii) la materia** *(`-0.0648` con D7, referto)*; **(iv) il campo** *(l'energia di `E` e di `B` sugli archi nuovi)*.
- **IL BILANCIO A OGNI NASCITA:** `Delta H_tot = materia + vuoto + legame + campo` **stampato con le sue parti** *(come `divisione_vuoto.txt`)*, **e la norma `M`, `V` e la carica di Gauss AL BIT** *(la loro soglia)*.

## 4. LA SOGLIA

- **La grandezza locale** *(proposta, da derivare)*: **l'energia del vuoto per nodo `vuo`** *(`_libro_dei_conti.conti_per_nodo`)* **sull'arco** -- **dove il vuoto e' TESO, la tensione paga la nascita.** **[doc] Il dato:** `doc/referti_l2/mattone/porto_alone_vuoto.txt`: **il massimo di `vuo` per anello all'anello `13` o `14`** *(su `L 162` fra `3.99` e `4.40`; su `L 243` `3.67`; su `L 324` fra `3.98` e `4.12`)*, **al centro `0.23`-`1.43`, all'anello `60` fra `2e-3` e `5e-3` (le righe stampate).**
- **Il valore:** **NON si sceglie** *(A1, «zero manopole»)*: **la soglia e' il bilancio** *(la decisione `10`)*: **un arco si divide quando l'energia che la nascita libera** *(la tensione dell'arco piu' il `Lambda` locale)* **copre il costo** *(il `Delta H` delle parti della sez. `3`)*. **La carta lo deve scrivere come una disuguaglianza fra grandezze del modello, senza un numero libero.** ### **Se servisse un numero, FERMO e chiedo** *(CLAUDE.md, par. `3`)*.
- **Perche' il vuoto puro NON la supera** *(la prova di D7: «nessuna nascita in un toro di solo vuoto»)*: **nel vuoto uniforme F3 la tensione d'arco e' la stessa su ogni arco** *(un flusso uniforme, `13466107`)* **e `vuo` e' minima** *(l'anello `60` a `2e-3`-`5e-3`)*: **il bilancio della nascita e' negativo ovunque.** **E' una IPOTESI da provare** *(la prova (P2) sotto)*, **non un fatto.**

## 5. COSA SI ROMPE NEGLI STRUMENTI E COME SI RIPARA

| lo strumento | che cosa assume | la riparazione proposta |
|---|---|---|
| **la U(1)** *(`_u1_prototipo.Campo`)* | `m = 3n`, gli archi `a1`, `a2`, `a1 + a2`, le placchette `3v + a` | **una U(1) sul grafo GENERICO:** `div` dalla matrice di incidenza *(come gia' `matrice_div_sparsa`)*, **le placchette dai TRIANGOLI del grafo** *(un elenco, non una formula)*; **e' il lavoro piu' grande** |
| **Gauss** *(`p6_u_breve.gauss_sparso`, `gauss_riuso`)* | **[codice]** la divergenza sparsa `D` `n x m`, il laplaciano `D D^T` senza il nodo `0`, `spsolve`; il riuso della fattorizzazione SuperLU finche' `campo` e' lo stesso | **la fattorizzazione si RIFA dopo ogni nascita** *(la matrice cambia)*, **oppure un aggiornamento LOCALE** *(sez. `6`)* |
| **il vuoto F3** *(`fondo_con_fasi`)* | una fase per CLASSE di direzione del reticolo | **sulle zone regolari resta com'e'** *(il vincolo della via (B): al bit)*; **attorno a un difetto le direzioni non sono tre: la fase si definisce dal TRASPORTO lungo il grafo** *(da derivare)* |
| **il bordo** *(`bordo.g_estremita`)* | la distanza dagli indici del toro | **dalle POSIZIONI** *(l'array fuori dal nucleo)* |
| **R-SCATOLA** | le distanze dagli indici | **dalle posizioni; e per i composti e' gia' da ridefinire** *(Q2)* |
| **le mappe e i video** *(`mappe.scrivi`: `m1`, `m2`)* | le coordinate dagli indici | **l'array delle posizioni: il nodo nuovo al punto medio dell'arco diviso** |
| **`Z["righe"]`** *(`n x 6`)* e i sei strumenti che lo usano | il grado `6` | **la CSR del nucleo** *(`offset`, `estremita`)* al posto del `reshape` |
| **numba** *(`primo_ordine/motore_numba.py`)* | **[codice]** nessun grado fisso, le forme lette a runtime; la cache `_ordine_di` per `id(idx)` | **sicuro:** un `inc.nodo` nuovo manca la cache; **ma le voci vecchie si ACCUMULANO**: va svuotata a ogni crescita |
| **il registro dei rami** *(P-R1, `csv/_rami_era2.py`)* | il nucleo = la chiusura degli import da `tick`, `passo`, `motore`, `materia_vuoto`, `saturazione` | **un modulo della crescita importato da `motore` ENTRA nel nucleo:** nessun default nelle firme, una voce in `RAMI` per ogni ramo, la voce in `_mappa.yaml` *(P-MOD)* |

## 6. LE PRESTAZIONI *(Q-P1, Q-P6)*

- **[doc] Il costo di oggi** *(`doc/referti_l2/mattone/profilo_nucleo.txt`, `L 162` MGU, `20` tick)*: **`4.177` s per tick** *(macchina carica)*; **`termini_di_h` `25.8` s cumulati su `83.6`** *(`480` chiamate, `24` per tick)*; **`gauss_sparso` `11.9` s cumulati** *(circa il `14%`)*; **`elicita` `7.1` s.** **A macchina ferma `2.138` s per tick** *(`motore_numba_tempi_v5.txt`)*.
- **LA COMPLESSITA' DI UNA NASCITA** *(dichiarata, da misurare)*:
  - **la topologia:** `Incidenza.cresci` **rifa' la CSR** *(`_derivati`: un `argsort` su `2m` estremita')*: **`O(m log m)` per nascita: GLOBALE.** ### **Con una nascita per tick e' circa il costo di un `argsort` di `6n` interi** *(`157464` su `L 162`)*: **da misurare contro `2.1` s del tick.** **Se pesa, il rimedio e' un inserimento LOCALE nella CSR** *(il nucleo, da decidere)*;
  - **le capacita':** raddoppiano *(`CRESCITA = 2`)*: **`O(log N)` copie in tutta la corsa, non una per nascita**;
  - **lo stato:** la permutazione `dove` di `psi_h`, `phi_h`: **`O(m)` per nascita** *(una copia per array)*: **GLOBALE**, e come sopra va misurata;
  - **Gauss:** **rifattorizzare il laplaciano** *(SuperLU, `n x n` sparso)* **a ogni nascita costa come la prima fattorizzazione** *(non misurata da sola: va misurata)*; **l'aggiornamento LOCALE** *(un nodo e `4` archi in piu': un aggiornamento di rango basso, o una correzione di `E` col solo `Delta rho` locale risolta con la fattorizzazione VECCHIA piu' una correzione)* **e' `O(dimensione del difetto)` ma NON e' al bit con la rifattorizzazione: va dichiarata la sua tolleranza** *(Q-A5)*;
  - **i buffer del motore:** `_buf` si svuota a ogni `cresci` **[codice]**: **le allocazioni si rifanno al tick dopo** *(costo da misurare; il rimedio: buffer con capacita', come `Incidenza`)*.
- **IL COSTO ATTESO PER TICK** *(Q-P2: oltre il `10%` decide Luca)*: **senza nascite, NESSUNO** *(il vincolo: le zone regolari al bit, il codice della crescita non gira)* -- **da misurare: il tick con il codice della crescita presente e spento contro il motore di oggi, sullo stesso stato** *(Q-P1)*; **con nascite: la somma dei termini sopra per il numero di nascite per tick.**
- **I cicli compilati** *(Q-P6)*: **[codice] numba legge le forme a runtime e non assume il grado**: **compatibile**, con la cache da svuotare; **le funzioni della crescita stesse restano in numpy** *(rare: una per tick al piu', `Motore.cresci`)*.

## 7. L'ACCURATEZZA *(Q-A1..Q-A6)*: LE PROVE DELLA MITOSI, PRIMA DEL CODICE

| | la prova | la soglia *(scritta prima)* | il caso che DEVE fallire |
|---|---|---|---|
| **P1** | la norma della materia `M` e del vuoto `V` dopo una nascita | la soglia della NORMA *(passi x eps; la nota di D7)* | una nascita con `psi` NON scalato *(la norma cresce)* |
| **P2** | **il vuoto puro non cresce:** un toro di solo vuoto F3 per `N` tick col codice della crescita acceso | **nessuna nascita** | un vuoto con un difetto teso costruito a mano *(deve nascere)* |
| **P3** | **Gauss al bit** dopo ogni nascita *(il residuo sul grafo nuovo)* | quello di oggi *(`10` volte il residuo iniziale)* | gli archi nuovi con `E = 0` |
| **P4** | **il giro** del vortice attorno a ogni anello dopo le nascite | `+1` in tutte le componenti a ogni controllo | una nascita che non trasporta la fase |
| **P5** | **lo specchio** dopo le nascite *(`6faa1a3d`)* | come C2 dello specchio *(sotto `1e-10` entro `40` nodi)* | una regola di flip NON simmetrica |
| **P6** | **le zone regolari AL BIT:** lontano dai difetti il tick e' identico a quello di oggi | **la differenza `0`** | -- *(e' un braccio 0)* |
| **P7** | **la curvatura contro il lapse:** attorno a un mattone, la curvatura dalle nascite *(in 2D `(6 - k) x 60` gradi per difetto, Regge)* **e il profilo `N(rho)` in un rapporto FISSO lungo il raggio** | **da scrivere PRIMA della corsa, con la barra** *(Q-A5)* | -- |
| **P8** | **la ripresa al bit con un grafo che cresce:** lo stato completo **comprende la geometria** *(`ii`, `jj`, le posizioni, il contatore delle nascite)* | come `notte_prova.py` *(R2: ogni chiave, differenza `0`)* | un byte cambiato *(rifiutato)* |

- **L'ORDINE DELLE OPERAZIONI DICHIARATO** *(come il contratto della nascita dell'era `1`)*: **dentro il tick:** (1) la soglia valutata su TUTTI gli archi con lo stato del tick prima; (2) **gli archi che la superano ordinati per indice** *(determinismo: vincolo (c))*; (3) **al piu' una nascita per tick** *(oggi `Motore.cresci` lo impone)*, oppure piu' nascite NON adiacenti in un solo `cresci` *(da decidere)*; (4) la divisione, il flip, lo stato nuovo *(sez. `2`)*; (5) Gauss; (6) il bilancio stampato. **Nessun estratto casuale** *(la mitosi e' deterministica)*.

## 8. LA STIMA DEL LAVORO *(per Luca; ordini di grandezza, non promesse)*

| | il pezzo | dove | la stima |
|---|---|---|---|
| `0` | **la decisione di SCONGELARE il nucleo** *(`Motore.cresci` deve far crescere i dati per nodo)* | Luca | -- |
| `1` | la carta delle regole aperte: `psi_h` e `phi_h` sulle estremita' nuove *(la via (3) di D7)*, il flip, la soglia come disuguaglianza | carta | `1`-`2` sessioni |
| `2` | `Motore.cresci` completo *(i dati per nodo, `dtau`, `cs`, `geo`)* + la cache di numba | nucleo | `1` sessione, con la suite |
| `3` | **la U(1) sul grafo generico** *(div, placchette dai triangoli, Gauss)* | `csv/` | **`2`-`3` sessioni: il pezzo piu' grande** |
| `4` | le posizioni fuori dal nucleo; il bordo, le mappe, `righe` -> CSR nei sei strumenti | `csv/solitone/` | `1`-`2` sessioni |
| `5` | le prove P1-P8 *(P6 per prima: il braccio 0)* | `csv/_test_fork/`, referti | `2` sessioni |
| `6` | la misura del costo *(Q-P1)*: con la crescita spenta e accesa | referto | `1` sessione |

### ⛔ **FERMO PRIMA DI OGNI CODICE.** **Le decisioni che servono da Luca:** **(D-M1)** lo scongelamento del nucleo per `Motore.cresci`; **(D-M2)** la mossa: «divisione + flip» *(la dislocazione)* o la sola divisione; **(D-M3)** la regola di `phi_h` sulle estremita' nuove *(la parte aperta della via (3), con i numeri di `divisione_vuoto.txt` da rigirare dal commit)*; **(D-M4)** una o piu' nascite per tick.

## 9. LE DECISIONI DI LUCA DEL `2026-11-17` `11:33` *(sulle proposte del guardiano)*

- **D-M1 -- SI', SU UN RAMO NUOVO `mitosi`** *(da `primo-ordine` a `306fd07b`; il worktree `C:/Users/lpeano/wt_mitosi`; pushato)*: **lo scongelamento del nucleo per `Motore.cresci` vale SOLO sul ramo**; **la riunione solo con un mandato di Luca** *(R-NAVI)*; ### **il CANCELLO e' P6** *(le zone regolari AL BIT)*: **se P6 non passa, nulla si riunisce.** **La tabella del nucleo congelato si aggiorna SUL RAMO, file per file, con la decisione scritta** *(in questo mandato nessun file del nucleo e' cambiato: niente da aggiornare)*.
- **D-M2 -- LA DIVISIONE D'ARCO PIU' IL FLIP** *(la dislocazione, la via (B))*, **CON LA CONDIZIONE che la scelta del flip sia SIMMETRICA ALLO SPECCHIO** *(la regola sotto, sez. `10.3`; la prova P5)*.
- **D-M3 -- la regola di `phi_h` sulle estremita' nuove SI DECIDE SUI NUMERI** *(la proposta sotto, sez. `10.2`; ### **FERMO per Luca**)*.
- **D-M4 -- UNA nascita per tick**, per cominciare; **piu' nascite dopo, con una prova dedicata.**
- ### ⛔ **IL CODICE DEL NUCLEO SUL RAMO PARTE SOLO DOPO D-M3 E CON FC PRESA** *(il mandato, C4)*.

## 10. LE REGOLE APERTE *(il punto `1` della stima; SOLO CARTA)*

### 10.1 I NUMERI, RIGIRATI DAL LORO COMMIT *(Q-A1)*

- **`doc/referti_l2/divisione_vuoto_rigirato.txt`**: **lo script di `aac33f2f` nel worktree staccato `C:/Users/lpeano/wt_divisione_f7ee87a9`** *(il commit del referto, `f7ee87a9`)*, con l'interprete di E:: **«committato e pulito»** *(sha1 dei byte `07b75ba1`)*.
- ### **LA PROVENIENZA DEL REFERTO DI ALLORA E' CHIARITA:** **il timbro «MODIFICATO rispetto a HEAD» era la TRAPPOLA CRLF** *(par. `7`)*: **i byte che girarono, sha1 `aa0384b6`, sono ESATTAMENTE il contenuto committato con i fine riga CRLF** *(il contenuto LF, `07b75ba1`, convertito in CRLF da' `aa0384b6`)*. **Lo stesso codice.**
- **Il confronto riga per riga col referto di `f7ee87a9`:** **identico tranne il timbro, la riga dei blob e tre termini dell'ordine di `1e-14`** *(il `vuoto` del flip `v5`: `+1.674177e-14` allora, `+7.673311e-15` ora; un `legame` `+2.842171e-14` -> `0`; un `dcs/cs` `4.219e-15` -> `4.441e-15`)*: **l'estremo della sfera di `v5` e' un conto numerico** *(il DEVE (2) lo tollera a `1e-12`)*. **Tutti i numeri sotto vengono dal referto rigirato.**

### 10.2 `psi_h` E `phi_h` SULLE ESTREMITA' NUOVE -- LA PROPOSTA PER D-M3

- **`psi`:** **D7** *(`psi/sqrt(2)` al padre e al figlio, la stessa fase)*: **la materia `-6.480149e-02` per TUTTE le regole** *(il referto, la parte `materia` della nascita)*. **Sulle estremita' nuove: `psi_h` = lo spinore del nodo, come sulle altre estremita' del nodo** *(da verificare nel codice della camminata prima della regola)*.
- **`phi_h`, le cinque regole** *(la nascita; `L 24` e `L 36` danno gli stessi numeri, tranne `v3`)*:

| | la regola | `Delta H_tot` | il vuoto | il legame | `V` | locale |
|---|---|---|---|---|---|---|
| `v1` | D7 anche per `phi` | `-8.548213678` | `-8.483412` | `~1e-13` | conservata | si' |
| `v2` | le nuove al valore uniforme, il padre intero | `-0.1435872887` | `0` | `-0.0787858` | ### **cresce di `6`** | si' |
| `v3` | `v2`, poi TUTTO il vuoto diluito | `-0.04531145615` *(L 24)* | `~0` | `+0.01949003` | conservata | ### **NO** *(ogni estremita' del toro)* |
| `v4` | il vuoto di `S` *(n, i, j, k, l e i vicini)* ridistribuito UNIFORME | `-0.300804079` | `-0.2451049` | `+0.00910235` | conservata | si' |
| `v5` | il MASSIMO della parte quadratica su `S`, alla norma | `-0.2334053164` | `-0.1775461` | `+0.008942222` | conservata | si' |

- ### **I DUE VINCOLI CHE SCELGONO:** **(a) la LOCALITA'** *(il cancello P6 di D-M1: lontano dai difetti il tick resta AL BIT; `v3` cambia ogni estremita' del toro: ESCLUSA)*; **(b) `V` conservata** *(QC, la norma del vuoto esatta: `v2` la viola: ESCLUSA)*. **Restano `v1`, `v4`, `v5`; `v1` libera `-8.548`, circa `30` volte le altre: ESCLUSA** *(e' gia' la ragione della via (3) di Luca)*.
- ### **LA PROPOSTA: `v4`** *(il vuoto di `S` ridistribuito uniforme fra le sue estremita', il fattore `sqrt(24/30)`)*: **locale, `V` ESATTA, DETERMINISTICA e SIMMETRICA ALLO SPECCHIO PER COSTRUZIONE** *(uniforme su un insieme simmetrico)*, **una formula chiusa senza ottimizzazione** *(`9-ter`: a parita' di effetto, meno leggi)*. **`v5` libera di meno** *(`-0.233` contro `-0.301`, la differenza `0.067`)*, **ma e' un ESTREMO NUMERICO** *(un problema agli autovalori: la scelta del segno dell'autovettore e' una preferenza nascosta, e il referto la rende entro `1e-12`, non al bit)*. ### **Le due differiscono di `0.067` su `0.3`: senza una barra non si puo' dire «parita'»** *(Q-A5)*: **la scelta e' di Luca.**
- ### ⚠ **DUE COSE DA SAPERE PRIMA DI DECIDERE:**
  1. **I numeri sono SULLA CARTA, col vuoto UNIFORME `stato_K`** *(il conto del vuoto di `C3`)*, **non col vuoto F3 delle corse** *(un flusso con una fase per direzione: D6f, «le forme di oggi»)*. **La regola va RIMISURATA sul vuoto F3 prima del codice** *(la stessa mossa sullo stato di una corsa)*.
  2. ### **IL SEGNO:** **la nota di D7 dice «la divisione ALZA H, quindi va PAGATA»**; **il referto da' `Delta H_tot` NEGATIVO per TUTTE le regole** *(la nascita ABBASSA `H`)*. **O la nota e' scaduta, o il segno di `H` e' una convenzione diversa: NON lo so, e decide come si scrive la soglia** *(sez. `10.4`)*.

### 10.3 IL FLIP SIMMETRICO ALLO SPECCHIO *(D-M2)*

- **Dopo la divisione di `(i, j)`:** `n` di grado `4`, `k` e `l` di grado `7`. **I flip che portano a una dislocazione:** **i quattro lati del rombo `i, k, j, l` attorno a `n`** *(`(i,k)`, `(k,j)`, `(j,l)`, `(l,i)`: ognuno, girato, collega `n` al vertice opposto e `n` sale a `5`)*. **I quattro sono immagine l'uno dell'altro per i due specchi della mossa** *(la retta `i-j` e la retta `k-l`)*: **nessuno, scelto A PRIORI, e' simmetrico.**
- ### **LA REGOLA PROPOSTA:** **si sceglie il flip che rende massima una grandezza LOCALE dello STATO** *(la proposta: la tensione del vuoto sull'arco che nasce dal flip, la stessa grandezza della soglia)*; ### **se il massimo NON e' unico** *(un pari merito entro la tolleranza della norma: uno stato simmetrico)*, **NESSUN flip a questo tick** *(la `4`-`7`-`7` resta, e il primo tick in cui lo stato rompe la parita' decide)*. **E' simmetrica allo specchio per costruzione:** **lo specchio dello stato sceglie lo specchio del flip** *(equivariante)*, **e uno stato simmetrico non sceglie.** **Deterministica:** nessun estratto, nessun ordine di indice usato fra pari merito. **La prova: P5.**

### 10.4 LA SOGLIA COME DISUGUAGLIANZA DEL BILANCIO

- **La decisione `10`:** il calore paga la nascita; **la soglia E' il bilancio.** **La forma proposta** *(nessun numero libero)*: **l'arco `a` si divide quando il bilancio locale della nascita su `a` e' coperto: `Delta H_nascita(a) <= Q(a)`**, con `Q(a)` **il calore disponibile sull'arco** *(una grandezza del modello da DEFINIRE: oggi nel nucleo non esiste un «calore»)*.
- ### ⚠ **IL CONFLITTO CHE LA CARTA NON RISOLVE** *(scritto, non aggirato)*: **sulla carta `Delta H_tot < 0` su un vuoto UNIFORME** *(`v4`: `-0.301`)*: **se la soglia fosse «la nascita abbassa `H`», il vuoto puro crescerebbe ovunque** -- **contro «il vuoto puro non cresce»** *(la nota di D7, C1)*. **Quindi o la soglia NON e' il segno di `Delta H` ma un confronto con una grandezza che nel vuoto puro e' nulla** *(la tensione d'arco, nulla nel vuoto UNIFORME; `vuo` all'anello `60` fra `2e-3` e `5e-3`)*, **o il segno della sez. `10.2`, punto 2, va chiarito prima.** ### **E' una domanda per Luca, insieme a D-M3.**

### 10.5 LE REGOLE SUL VUOTO F3 *(Luca `2026-11-17` `13:16`, parte 3; `doc/referti_l2/divisione_vuoto_F3.txt`)*

- ### ⚠ **I NUMERI DELLA SEZ. `10.2` SONO DEL NUCLEO DI ALLORA** *(annotazione, il testo sopra resta com'era)*: **`divisione_vuoto_rigirato.txt` e' rigirato nel worktree di `f7ee87a9`, col nucleo di quel giorno**; **dopo sono entrati S1 nel nucleo** *(`c7ad2238`, `00821633`)* **e lo zero simmetrico** *(`7c181cc4`)*. **Col nucleo di OGGI, sul vuoto uniforme `stato_K(24)`:** **v1 `-8.548213678`** *(uguale)*, **v2 `+18.78474403`** *(era `-0.1436`)*, **v3 `-0.06479340335`** *(era `-0.0453`)*, **v4 `-0.3099018648`** *(era `-0.3008`)*, **v5 `-0.2423431548`** *(era `-0.2334`)*. **v4 contro v5 oggi: `1.28` volte, non ordini di grandezza.**
- **SUL VUOTO F3:**
  - **(a) il vuoto F3 puro:** ### **D7 SU `phi` E' INDEFINITA** -- **la somma di `phi` sulle sei estremita' del padre e' `0`** *(F3 e' un flusso)*, **e D7 mette sulle estremita' nuove `chiv/|chiv| = 0/0`.** **v1, e la v4-F3 che ne prende le fasi, NON esistono sul vuoto puro.**
  - **(b) il mattone, l'arco all'anello `13.81`:** la somma relativa `0.109`; **v1 `-905.96`, v4-F3 `-898.03`** *(la materia `-916.32`: D7 su `psi` dove la materia e' grande; il vuoto `+10.36` e `+18.29`)*.
  - **(c) il mattone, l'arco all'anello `59.81`** *(quasi vuoto)*: la somma relativa `9.5e-03`; **v1 `+17.26`, v4-F3 `+26.11`** *(il vuoto `+17.26` e `+26.12`)*.
  - **Locali e con `V` esatta tutte e due** *(nessuna estremita' cambiata fuori da `S`; `V` relativa `0`)*.
- ### **IL SEGNO SUL VUOTO VERO: POSITIVO.** **Sul vuoto F3 la nascita COSTA** *(`+17`/`+26` all'anello `60`)*: **la nota di D7 («la divisione ALZA H») e' VERA sul vuoto delle corse**; **il segno negativo della sez. `10.2` veniva dal vuoto UNIFORME della carta**, che non e' il vuoto delle corse.
- ### **LA CONDIZIONE DI LUCA PER D-M3 (= v4) NON SI CHIUDE:** **locale e `V` esatta: si'; deterministica: si'; ma su F3 la sua fase viene da v1, che sul vuoto puro e' INDEFINITA** *(e vicino al vuoto e' fissata da un residuo: la somma relativa `9.5e-03` all'anello `60`)*; **v5 su F3 non si misura** *(lo strumento e' reale e denso)*. ### **FERMO coi numeri: serve una regola della FASE del vuoto sulle estremita' nuove che non passi per D7** *(la parte del vuoto della via (3) di Luca)*.

### 10.6 LA SOGLIA: LE CANDIDATE PER IL «CALORE» *(parte 4; `doc/referti_l2/soglia_nascita.txt`; sola lettura; ### LA SCELTA E' DI LUCA)*

- **4.1 IL SEGNO** *(dal codice, `energia_pesata.termini_di_h`, e dal referto)*: **nodo** `-Omega (0.5 nrm - |S|^2/d)` per materia e vuoto *(lo zero simmetrico, Luca `2026-11-08`)*, `+ eps h`, `+ N`; **arco** `Omega Re(incro)` *(la materia)* e `Omega Re(conj(phi_coda) phi_testa)` *(il vuoto)*. **Sul vuoto F3 puro:** `|S_phi| = 0` *(un flusso)*: **il nodo del vuoto vale `-Omega nrm/2 = -9.4248` e l'arco `-Omega |phi|^2 = -3.1416`: il vuoto F3 e' NEGATIVO** *(il totale `-4.946877e+05`)*. **Sul mattone:** la materia e `N` sono POSITIVI *(il Grover di `psi` `+1.54e6`, `N` `+9.84e5`, l'arco di `psi` `+1.54e6`)*, **il vuoto negativo.** ### **«Alzare H» = rendere il totale meno negativo / piu' positivo.** **Una nascita sul vuoto F3 lo alza** *(sez. `10.5`)*.
- **4.2 LA TENSIONE D'ARCO** *(la definizione, MIA: il termine d'arco del vuoto)*: **sul vuoto F3 puro e' UNIFORME, `-3.141592654` su ogni arco** *(`-Omega |phi|^2`)*; **attorno al mattone sale verso lo zero nel guscio** *(`-0.553` all'anello `15`, `-0.792` al `20`)* **e torna a `-3.14` oltre `25`.**
- **4.3 LE TRE CANDIDATE** *(ognuna: il valore nel vuoto puro; il massimo attorno al mattone; gli archi sopra il costo `C = 26.11`, SCELTA MIA, il `Delta H` di v4-F3 all'anello `60`)*:

| | `Q(a)` | il vuoto F3 puro | il massimo attorno al mattone | attorno al triangolo | attorno alla coppia | gli archi `>= C` |
|---|---|---|---|---|---|---|
| **Q1** | la tensione d'arco sopra il fondo F3 | **`0` esatto** | `+6.14` a `14.85` nodi | `+7.75` | `+6.66` | **`0`** *(in tutti e quattro gli stati)* |
| **Q2** | l'energia del vuoto per nodo *(la media sui due nodi)* sopra il fondo | **`0` esatto** | `+9.23` a `20.54` nodi | `+9.18` | `+9.30` | **`0`** |
| **Q3** | `|J(a)|`, la corrente di energia sull'arco | **`0` esatto** | `+6.13` a `9.21` nodi | `+9.71` | `+6.98` | **`0`** |

- ### **LA LETTURA:** **tutte e tre sono NULLE nel vuoto puro** *(il vuoto puro non cresce, per costruzione)* **e massime nel GUSCIO attorno alla materia** *(l'anello `13`-`20`: dove `vuo` e' massimo, `ee7b8215`)*; **nessuna, con il costo `C`, fa nascere un nodo in nessuno degli stati letti** *(i massimi sono `3`-`4` volte sotto `C`)*: **o il costo vero e' piu' basso** *(il costo dove la nascita accadrebbe -- nel guscio -- e' quello della sez. `10.5`, (b), dominato dalla materia: `-898`, NEGATIVO)*, **o la soglia non e' «Q >= costo»**. ### **FERMO per Luca: la scelta di `Q` e della forma della soglia.**

## 11. DOVE, QUANTO E CHI PAGA *(il mandato di Luca del `2026-11-17` `14:27`)*

### 11.1 LE DECISIONI DI LUCA *(`14:23`-`14:27`)* E LA VALUTAZIONE DEL GUARDIANO

- **(1) Lo spazio cresce VICINO alla materia ma FUORI; (2) la crescita e' CONTINUA; (3) il «calore» che paga la nascita e' il FLUSSO USCENTE di energia, FUORI dalla materia.**
- **Il guardiano:** **(a)** FUORI impedisce che D7 diluisca la materia e toglie il termine della materia che fa scappare la crescita; **il confine si MISURA**; **(b)** il calore USCENTE, non l'energia ferma *(Q1-Q3 sono legate al mattone e farebbero crescere spazio anche attorno a un oggetto immobile)*: **il flusso uscente fa crescere spazio solo dove arriva energia staccata dalla materia e solo finche' arriva**; **si ACCUMULA sull'arco, la nascita quando l'accumulato copre il costo, poi si riparte da zero**; **(c)** la velocita' la fissa la fisica *(il flusso / il costo)*, al piu' una nascita per tick; **(d)** se il flusso uscente paga la nascita, il bordo potrebbe non servire piu'; **una nascita irreversibile rompe CPT come il bordo.**

### 11.2 I NUMERI *(i referti: `nascita_dentro_fuori.txt`, `flusso_uscente.txt`, `simmetria_CPT_cache.txt`)*

- ### **IL CONFINE: `23.81` nodi = `1.92` raggi della materia** *(il raggio rms `12.376`)*: **da li' in poi il termine della materia sta sotto l'`1%` di `|Delta H|`** *(e sotto il `10%`: lo stesso anello)*. **Dentro: `Delta H` NEGATIVO e grande** *(`-1472` a `7.81` nodi, `-898` a `13.81`, `-292` a `18.81`)*, **quasi tutto dalla materia; fuori: POSITIVO** *(`+22.5` a `23.85` sullo stato di `L 186`; `+26.0`-`+26.5` da `28.85` a `58.85`)*, **quasi tutto dal vuoto.**
- **IL PERCHE' dentro** *(all'anello `13.81`)*: **la materia `-916.32` = il Grover di `psi` `-574.78` + l'arco di `psi` `-341.54`**; `N` `-3.3e-04` *(D7 conserva `N`: e' omogenea di grado 1)*. **Il codice** *(`energia_pesata.termini_di_h`)*: **il nodo `-Omega (0.5 nrm - |S|^2/d)`**: **D7 dimezza `psi` sul padre e ne mette meta' sul nodo nuovo di grado `4`**: **`|S|^2/d` del padre e del figlio cambia, e dove la materia e' grande la somma dei due termini scende** *(il Grover)*; **e gli archi nuovi portano il prodotto `Re(incro)` fra estremita' ora piu' piccole** *(l'arco)*.
- **LE NASCITE IN FILA** *(`20`, ognuna sull'arco del nodo nato per ultimo col termine d'arco del vuoto piu' alto)*: **all'anello del confine `23.81`: tutte POSITIVE, decrescenti** *(da `+27.38` a `+0.45`)*: **nessun cambio di segno**; **all'anello `13.81`: negative per `14`** *(da `-898.0` a `-51.6`)*, **positiva la `15`a** *(`+0.61`)*, **poi negative piccole** *(`-0.07`... `-0.05`)*. **Con U** *(A a meta' flusso, E da Gauss vero)*: **`Delta H` cambia alla quarta o quinta cifra** *(la prima: `-898.0334` -> `-898.0179`)*, **l'energia `E^2/2` di `1e-02`**, Gauss dopo la nascita `<= 6.3e-15`.
- **IL TRIANGOLO E LA COPPIA:** **lo stesso quadro** *(dentro `-909`, `-1291` a `10` nodi; fuori `+26.1`, `+25.8` a `60`)*.
- **IL FLUSSO USCENTE** *(la corsa su `L 186`, sei istanti `950`-`3000`)*: **positivo a tutti gli anelli `15`-`45` in tutti e sei** *(a `30` e `45` nodi `0.19`-`0.28` per tick, anche il NETTO positivo; a `15` e `20` il netto oscilla di segno)*; **la massa assorbita dal bordo `0.12`-`0.17` per tick**; **NON si esaurisce** *(a `3000` contro `950`: `0.74`-`1.04`)*.
- **IL CASO NOTO del flusso:** **il pacchetto con la fase che cresce verso fuori si muove VERSO DENTRO** *(`-0.128` nodi in `5` tick)* **e il suo flusso e' entrante; l'altro il contrario**: **l'onda all'indietro della domanda Q8, misurata su un pacchetto** -- **la definizione segue lo SPOSTAMENTO, non la fase.**
- **L'ACCUMULO** *(fuori dal confine, il trapezio sui sei istanti)*: **il primo arco a nascere a `23.89` nodi dopo circa `2515` tick** *(il ritmo `8.95e-03` per tick contro il costo `22.50`)*; **al ritmo medio `0.50` nascite per tick, cioe' circa `5040` in `10000` tick** *(sotto il tetto di una per tick)*; **nessun arco copre il costo entro i `2050` tick misurati.** ### ⚠ **UN LIMITE DELLA MISURA:** **la parte POSITIVA arco per arco RADDRIZZA le oscillazioni** *(a `15` e `20` il netto cambia segno)*: **il ritmo vero e' piu' basso: e' un MASSIMO.** **Il costo di calcolo:** una `energia.corrente` `0.117` s *(su `L 186`)*, l'accumulo `O(m)` per tick.
- **FC** *(`simmetria_CPT_cache.txt`)*: **le cache ricalcolate tornano all'arrotondamento** *(il commit di FC)*.

### 11.3 LA PROPOSTA DI SOGLIA *(che segue dai numeri; LA DECIDE LUCA)*

- **La nascita sull'arco FUORI dal confine** *(oltre `~1.9` raggi della materia, dove il termine della materia e' sotto l'`1%`)* **quando il FLUSSO USCENTE ACCUMULATO sull'arco copre il COSTO della nascita li'** *(`+22`-`+26` sul vuoto vicino)*; **poi l'accumulo riparte da zero; al piu' una nascita per tick.**
- **Da definire prima del codice:** **(i)** l'accumulo della parte positiva o del NETTO *(il netto non raddrizza; il positivo si')*; **(ii)** il confine come grandezza LOCALE *(la materia sull'arco sotto l'`1%` del costo?)* e non come raggio dal baricentro *(un oggetto composto non ha un solo centro)*; **(iii)** la corrente del VUOTO *(oggi `J` e' della sola materia)*.

### 11.4 LE DOMANDE PER LUCA

- **LA REVERSIBILITA':** **una nascita irreversibile rompe CPT come il bordo.** **Esiste l'anti-nascita** *(la fusione di due nodi quando il flusso ENTRA)*? **Se si', la crescita e' reversibile e CPT potrebbe restare; se no, la crescita e' una freccia del tempo dichiarata.**
- **IL BORDO:** **se il flusso uscente paga la nascita, il bordo assorbente serve ancora?** *(oggi il bordo prende `0.12`-`0.17` di massa per tick; le nascite prenderebbero ENERGIA)*.
- **LE PREVISIONI DEL GUARDIANO** *(`831e8d52`)*: **P-E1 CADE** *(il confine a `1.92` raggi, non entro `1.5`)*; **P-E2 CADE** *(al confine nessun cambio di segno in `20`: la crescita NON si frena da sola li')*; **P-E3 REGGE** *(positivo a `15`-`45`, non si esaurisce)*; **P-E4 e' vera PER COSTRUZIONE** *(un falso zero: la corrente e' della materia)*.
