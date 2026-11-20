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

> ### ⛔ **SUPERATA DALLA SEZ. `12`** *(Luca `2026-11-17` `16:02`: il calore si accumula sul NETTO, in una riserva conservata; l'accumulo arco per arco contava la stessa energia molte volte: sez. `12.2`)*. **Il testo sotto resta com'era.**

- **La nascita sull'arco FUORI dal confine** *(oltre `~1.9` raggi della materia, dove il termine della materia e' sotto l'`1%`)* **quando il FLUSSO USCENTE ACCUMULATO sull'arco copre il COSTO della nascita li'** *(`+22`-`+26` sul vuoto vicino)*; **poi l'accumulo riparte da zero; al piu' una nascita per tick.**
- **Da definire prima del codice:** **(i)** l'accumulo della parte positiva o del NETTO *(il netto non raddrizza; il positivo si')*; **(ii)** il confine come grandezza LOCALE *(la materia sull'arco sotto l'`1%` del costo?)* e non come raggio dal baricentro *(un oggetto composto non ha un solo centro)*; **(iii)** la corrente del VUOTO *(oggi `J` e' della sola materia)*.

### 11.4 LE DOMANDE PER LUCA

- **LA REVERSIBILITA':** **una nascita irreversibile rompe CPT come il bordo.** **Esiste l'anti-nascita** *(la fusione di due nodi quando il flusso ENTRA)*? **Se si', la crescita e' reversibile e CPT potrebbe restare; se no, la crescita e' una freccia del tempo dichiarata.**
- **IL BORDO:** **se il flusso uscente paga la nascita, il bordo assorbente serve ancora?** *(oggi il bordo prende `0.12`-`0.17` di massa per tick; le nascite prenderebbero ENERGIA)*.
- **LE PREVISIONI DEL GUARDIANO** *(`831e8d52`)*: **P-E1 CADE** *(il confine a `1.92` raggi, non entro `1.5`)*; **P-E2 CADE** *(al confine nessun cambio di segno in `20`: la crescita NON si frena da sola li')*; **P-E3 REGGE** *(positivo a `15`-`45`, non si esaurisce)*; **P-E4 e' vera PER COSTRUZIONE** *(un falso zero: la corrente e' della materia)*.

## 12. IL DIFETTO DELL'ACCUMULO, LA RISERVA E L'AUTOALIMENTAZIONE *(il mandato di Luca del `2026-11-17` `16:02`)*

> **Le decisioni di Luca** *(`16:02`)*: **il calore si accumula sul NETTO** *(non sulla parte positiva)*, **in una RISERVA CONSERVATA**; **C3 annullata**; **C2 del controllo e' il braccio SENZA MITOSI della prova futura.** **Questa sezione SUPERA la sez. `11.3`** *(la sez. `11` resta com'era)*.

### 12.1 LE PREVISIONI DEL GUARDIANO *(copiate PRIMA dei numeri)*

- **P-R1.** Il massimo di nascite pagabili dal netto al confine sta fra `0.005` e `0.02` per tick; il fattore di sovraconteggio fra `20` e `100`.
- **P-R2.** Con la riserva sul netto, nei `2050` tick misurati *(`k 950`-`3000`)* si pagano al piu' `25` nascite.
- **P-R3.** Sugli archi sparsi *(S3a e S3b)* il costo NON scende: l'ultima nascita entro il `10%` della prima. La discesa della sez. `11.2` *(le nascite in fila)* e' diluizione locale, non un effetto che si allarga.

### LE MIE, accanto *(dai numeri gia' nel repo, `flusso_uscente.txt`)*
- **P-R1:** **la credo VERA**: il netto a `30` e `45` nodi sta fra `0.19` e `0.27` per tick nei sei istanti, il costo fuori fra `+22.5` e `+26.5`: **circa `0.01` per tick, un fattore circa `50` sotto `0.50`**. **Ma al confine** *(`23.81` nodi)* **il netto non e' misurato, e a `15` e `20` nodi oscilla di segno**: **li' puo' venire diverso.**
- **P-R2:** **la credo VERA** *(circa `0.23 x 2050 / 26`, una ventina)*.
- **P-R3:** **NON so**: **il costo al confine dipende dall'ANGOLO** *(la materia del mattone non e' rotonda)*: **l'ultima contro la prima puo' differire di piu' del `10%` per l'angolo, non per l'accumulo**; **lo separo stampando il costo di ogni arco sparso sullo stato VERGINE** *(senza le nascite prima)* **accanto a quello in sequenza.**

### 12.2 IL DIFETTO DELL'ACCUMULO, MISURATO *(S1; `doc/referti_l2/accumulo_controllo.txt`)*

- **L'accumulo arco per arco della sez. `11.2`** *(`flusso_uscente.txt`, 3.3)* **sommava il flusso che ATTRAVERSA ogni arco: la stessa energia, uscendo, attraversa molti archi in fila e si contava molte volte.**
- **Il controllo: l'energia NETTA che esce per tick attraverso l'anello, per il costo medio di una nascita** *(`25.70 +- 1.23`, gli otto costi fuori dal confine)*:

| l'anello | il netto per tick *(la media sui sei istanti)* | le nascite pagabili per tick | il fattore contro `0.504` | la riserva in `2050` tick | le nascite che paga |
|---|---|---|---|---|---|
| il confine `23.81` | `+0.149` *(da `+0.022` a `+0.383`)* | `5.8e-03 +- 4.3e-03` | `87` | `+385` | `15.0` |
| `30` | `+0.234` | `9.1e-03` | `55` | `+474` | `18.4` |
| `45` | `+0.237` | `9.2e-03` | `55` | `+496` | `19.3` |

- **LE PREVISIONI:** **P-R1 VERA** *(fra `0.005` e `0.02`; il fattore fra `20` e `100`)*; **P-R2 VERA** *(al piu' `25`)*. **La riserva e' incerta:** al confine il netto oscilla di un ordine fra i sei istanti, e il trapezio su sei punti e' un'approssimazione *(Q-A5)*.

### 12.3 LA RISERVA *(S2: la PROPOSTA; ### LA SCELTA E' DI LUCA)*

- **(a)** entra **solo il flusso NETTO di energia attraverso il confine** *(`23.81` nodi = `1.92` raggi della materia per il mattone)*, integrato nel tempo; **(b)** ogni nascita toglie dalla riserva il suo costo `Delta H` misurato sullo stato vero, e **la riserva non va mai sotto zero**; **(c)** **l'energia della nascita deve uscire DAVVERO dal campo** *([[D-BILANCIO-NASCITA]])*: **il totale** *(il campo + la riserva + il costo dei nodi nati)* **e' conservato.**
- **LE ALTERNATIVE, coi pro e i contro** *(NON scelgo)*:
  - **(i) una riserva UNICA per oggetto** -- **pro:** semplice, un numero; il netto al confine e' gia' misurato cosi'. **contro:** serve un «oggetto» e un confine *(per un composto, quale centro?)*; **non dice DOVE nascere.**
  - **(ii) riserve LOCALI per settore angolare** -- **pro:** la nascita cade dove l'energia esce davvero; **nessun centro globale** *(un confine locale)*. **contro:** il netto per settore oscilla di piu' *(al confine gia' l'anello intero oscilla di un ordine)*; **piu' leggi da scrivere.**
  - **COME si toglie l'energia dal campo** *(da derivare)*: **la proposta: dal vuoto** *(il costo e' quasi tutto del vuoto: la sez. `11.2`)*, **con un'operazione che conserva la norma** *(una rotazione di fase locale del vuoto attorno all'arco nato, che cambia `H` senza cambiare `V`, come la «rotazione» di `_conto_del_vuoto.conto`)*; **dove: sugli archi che il flusso ha attraversato** *(contro: non locale)* **o sull'arco nato** *(contro: la riserva e' integrale, l'arco no)*.
  - **DOVE nasce il nodo:** **l'arco scelto dalla tensione** *(il termine d'arco del vuoto: misurato, sez. `10.6`)* **o dal flusso** *(l'arco col netto uscente piu' grande del settore)*. **La simmetria allo specchio** *(D-M2)* **vale per tutte e due, se la scelta e' equivariante e i pari merito non scelgono** *(sez. `10.3`)*.

### 12.4 L'AUTOALIMENTAZIONE *(S3; `doc/referti_l2/nascite_sparse.txt`)*: **UNA DILUIZIONE LOCALE, NON UN EFFETTO CHE SI ALLARGA**

- **La domanda di Luca:** **le nascite in fila della sez. `11.2`** *(sul nato per ultimo, da `+27.4` a `+0.45`)* **sono come l'espansione accelerata?**
- **Le nascite su archi SPARSI** *(lo stato di `L 186` a `k 3000`; `20` archi a `18` gradi l'uno dall'altro, uno dopo l'altro sullo stato che cresce)*: ### **ogni nascita costa ESATTAMENTE quanto costerebbe sullo stato vergine** *(la differenza relativa massima `3.9e-11` al confine, `1.8e-11` a `30` nodi)*: **le nascite lontane NON si vedono fra loro.**
- **Il rapporto ultima/prima:** **a `30` nodi `0.995`; al confine `1.201`** -- **ma al confine il costo dipende dall'ANGOLO** *(sullo stato vergine da `+17.70` a `+31.81` attorno all'anello; a `30` nodi da `+25.73` a `+26.45`)*: **il `20%` e' l'angolo, non l'accumulo** *(la sequenza = il vergine)*. **Accanto, in fila sul nato per ultimo:** `0.017`.
- ### **LA LETTURA:** **la discesa in fila e' DILUIZIONE LOCALE** *(D7 dimezza il campo sempre nello stesso punto: una crepa che si allarga in un posto solo)*, **non un effetto che si allarga** *(lo spazio nuovo non rende piu' facile lo spazio lontano)*. **Con la scelta del nodo da una grandezza dello stato** *(la tensione o il flusso)* **la crepa e' possibile: la riserva la limita** *(sotto)*.
- **P-R3 ALLA LETTERA:** **VERA a `30` nodi** *(`0.995`)*, **FALSA al confine** *(`1.201`, oltre il `10%`)* **-- per l'angolo, come scritto prima della misura** *(la mia nota in `12.1`)*; **la sostanza** *(la discesa e' locale)* **regge.**
- **QUANTE NE PAGA LA RISERVA** *(il netto al confine in `2050` tick, `+385`)*: **`16` nascite su archi sparsi al confine, `14` a `30` nodi, `20` in fila** *(in fila costano sempre meno: la riserva ne paga di piu', ed e' la crepa)*.

## 13. VERSO IL PRIMO TEST SUL MATTONE *(il mandato di Luca del `2026-11-17` `16:38`)*

> **Le decisioni di Luca** *(`16:38`, sulla sez. `12.3`)*: **D-R1** riserve LOCALI per settore angolare; **D-R2** il nodo nasce, nel settore, sull'arco oltre il confine col flusso NETTO uscente di energia piu' grande; **D-R3** l'energia della nascita si toglie dal VUOTO attorno all'arco nato, con una rotazione che conserva la norma, da derivare e provare; **D-R4** la crescita e' IRREVERSIBILE *(nessuna fusione)*: **una freccia del tempo DICHIARATA**, accanto a CPT *(che regge senza bordo e senza crescita)*; **D-R5** il codice del nucleo sul ramo `mitosi` si allenta SOLO per l'infrastruttura che non dipende dalla regola di `phi_h`; **la regola di nascita resta FERMA fino a D-M3.**

### 13.1 LE PREVISIONI DEL GUARDIANO *(copiate PRIMA delle misure)*

- **P-M1.** A3: una rotazione locale SOLO sul vuoto di `S` non basta a togliere `+26` sul vuoto F3 quasi puro *(serve un insieme piu' grande o un'altra operazione)*.
- **P-M2.** P6 passa al bit a piu' di `6` nodi dal difetto.
- **P-M3.** Il costo di una nascita *(CSR + Gauss rifattorizzato)* sta sotto `3` tick; con circa `0.01` nascite per tick, il costo medio cresce meno dell'`1%`.
- **P-M4.** Per il test futuro: sul mattone senza bordo, in `3000` tick, fra `5` e `40` nascite, tutte oltre il confine, in almeno `4` settori su `6`; la massa entro `12.4` e la larghezza `w` diverse da C2 per meno dell'`1%` *(il test mostrera' il meccanismo e la conservazione, non ancora la curvatura P7)*.
- **LE MIE, accanto** *(il perche' nella carta del mandato, `doc/TASK_HISTORY/2026-11-17_mitosi_verso_il_test.md`, sez. `1`-`2`)*: **P-M1 VERA** *(F3 e' il minimo locale dell'energia del vuoto a norma fissata)*; **P-M2: credo che FALLISCA al bit per Gauss e per il lapse** *(una nascita cambia `E` e `cs` ovunque: il confronto lontano dal difetto va fatto a parita' di `E` e di `cs`, o il cancello va riscritto)*; **P-M3: non so.**

### 13.2 A1-A2: LA FASE DEL VUOTO SULLE ESTREMITA' NUOVE SENZA D7 *(`doc/referti_l2/regole_fase_F3.txt`)*

- **Le due regole proposte** *(i moduli come v4: `V` esatta)*: **FA «antipodale»** *(gli archi nuovi con le estremita' OPPOSTE come in F3; in `i`, `j` il trasporto; in `n` verso `k`, `l` la fase del padre su `i -> k`, `i -> l`)* e **FT «trasporto del padre»** *(in `n` la fase del padre nella stessa direzione)*.

| | il vuoto F3 puro | il mattone a `23.81` | a `29.81` | a `59.81` | la sensibilita' a `1e-12` |
|---|---|---|---|---|---|
| **v4-F3** *(D7)* | `+23.58` *(solo dal ramo di riserva: la fase `0/0` sostituita)* | `+27.38` | `+26.24` | `+26.11` | **`10.7%` sul vuoto puro** |
| **FA** | **`+3.476`** | `+4.459` | `+3.495` | `+3.476` | `0` |
| **FT** | **`+3.476`** | `+6.649` | `+3.510` | `+3.481` | `<= 1.3e-10` |

- **Definite sul vuoto puro, locali, `V` esatta, deterministiche, STABILI.** **Il costo e' `7` volte piu' basso** *(il termine d'arco del vuoto da `+15`-`+20` a `+0.25`: gli archi nuovi restano antipodali come F3)*. ### **La simmetria allo specchio NON e' provata**: **il padre e' la CODA dell'arco** *(`ii`)*: **un arco riflesso puo' cambiare verso, e allora cambia padre** *(un difetto anche della `nascita` di oggi)*. **Una regola simmetrica deve scegliere il padre senza il verso dell'arco** *(per esempio: i due capi insieme)*.

### 13.3 A3: LA COMPENSAZIONE SUL VUOTO *(`doc/referti_l2/compensazione_vuoto.txt`)*: ### **TOGLIE IL `100%`**

- **L'energia del vuoto e' una forma QUADRATICA esatta** *(il codice di `termini_di_h`)*; **il minimo a norma fissata sulle estremita' di `S`** *(il resto fisso)* **e' il massimo che QUALUNQUE operazione su `S` che conserva la norma puo' togliere** *(il caso noto: F3 senza nascita e' gia' il minimo, la differenza `0`)*.
- ### **DOPO LA NASCITA IL MINIMO TORNA ESATTAMENTE ALL'ENERGIA DI PRIMA:** **sul vuoto F3 puro `-5.8e-11`, gia' a un passo** *(per FA e per v4-F3)*; **sul mattone a `59.81` nodi `-0.012` a un passo, `-0.056` a due, `-0.133` a tre** *(sotto lo zero)*.
- ### **P-M1 FALSA** *(e la mia previsione con lei)*. **La conseguenza: il costo della nascita NON e' intrinseco**: **e' il costo di una regola di fase lontana dal minimo.** **Con la regola «il vuoto di `S` al MINIMO a norma fissata»** *(un problema agli autovalori complesso, esatto)* **la nascita sul vuoto costa circa `0`, e vicino alla materia MENO di `0`.** ### **E allora l'argomento della sez. `12` («la riserva paga il costo») cade: se la nascita e' gratis, la riserva non ha niente da pagare** -- **la soglia deve venire da un'altra parte** *(una domanda per Luca)*.
- ### **E LA COSA CHE IL MANDATO NON DICEVA** *(la carta del mandato, sez. `1`)*: **la riserva conservata, riempita dal flusso che attraversa il confine, conta un'energia che RESTA nel campo**: **perche' il totale si conservi, il confine deve togliere quell'energia dal campo, cioe' ASSORBIRE come un bordo** -- **in conflitto con «la mitosi non deve fare le veci del bordo».**

### 13.4 A4: I SETTORI *(`doc/referti_l2/settori_specchio.txt`)*

- **Sei settori da `60` gradi attorno a un NODO, i bordi sulle direzioni del reticolo; gli archi col punto medio sul bordo: pari merito, nessuna nascita.** **Entro il disco INSCRITTO nel toro** *(`L sqrt(3)/4 = 70.15` su `L 162`)* **lo specchio a `30` gradi e l'inversione mandano OGNI arco nel settore immagine: `0` sbagliati su `53562`.** **Fuori dal disco** *(oltre `80.5` nodi)* **l'immagine piu' vicina sul toro e' ambigua** *(`414` e `522` sbagliati)*: **il dominio, dichiarato DOPO la prima corsa** *(post-hoc)*. **Il caso che deve fallire** *(il centro non su un nodo)*: l'inversione ne sbaglia `421` dentro il disco. ### **Il centro dei settori va arrotondato al NODO.**

### 13.5 LA FRECCIA DEL TEMPO *(D-R4)* E LE GRANDEZZE DA DEFINIRE

- ### **LA CRESCITA E' IRREVERSIBILE** *(nessuna fusione; decisione di Luca `16:38`)*: **UNA FRECCIA DEL TEMPO DICHIARATA**, **accanto a CPT** *(che regge sul tick G+U senza bordo e senza crescita: [[DEC-FC-COESIONE]])*. **Con la crescita accesa il modello NON e' piu' CPT-simmetrico**: **la rottura e' una SCELTA dichiarata, non un difetto.**
- **DA DEFINIRE** *(nessuna misura ora)*: **l'ENTROPIA** *(il numero dei nodi? la «disposizione» del grafo? l'informazione persa da una nascita irreversibile?)*.

### 13.6 FERMO PER LUCA SU D-M3 *(la parte B prosegue)*

- **Le scelte per la regola del vuoto alla nascita:** **FA o FT** *(stabili, `+3.48` sul vuoto)*, **oppure il MINIMO a norma fissata** *(il costo circa `0`)*; **e il PADRE senza il verso dell'arco** *(per la simmetria allo specchio)*.
- **E le due domande nuove:** **se la nascita al minimo e' gratis, che cosa fa la soglia?**; **la riserva conservata vuole un confine che assorbe: si accetta?**

### 13.7 D-R1, D-R2, D-R3 SOSPESE *(decisione di Luca `2026-11-17` `18:04`)*

- **Le riserve per settore, la nascita dove passa piu' flusso, l'energia tolta dal vuoto: SOSPESE, non annullate.** **D-R4** *(la crescita irreversibile, la freccia dichiarata)* **RESTA.** **La parte B** *(l'infrastruttura, D-R5)* **prosegue: B.2 `f7f3e43d`, B.3 `c2cb792b` sul ramo `mitosi`.**

## 14. IL QUANTO DI OLONOMIA COME INNESCO *(il mandato di Luca del `2026-11-17` `18:04` e l'aggiunta delle `18:48`; la carta `doc/TASK_HISTORY/2026-11-17_torsione_tempo_proprio.md`)*

### 14.1 LA STORIA

- **`2026-10-11`, la decisione di Luca** [[MITOSI-QUANTO-OLONOMIA]]: **la mitosi scatta al QUANTO di olonomia**, col tetto `4 pi` della doppia copertura, **nessun numero tarato.**
- **`2026-10-27`, l'ipotesi** *(PROGETTO_MITOSI `3(a)`)*: **la torsione e' un criterio d'energia scritto come fase; `2 pi` e' un quanto d'azione; scatta dove `cs` differisce ai capi** -- *«il tempo curvo che produce lo spazio curvo»*. **La misura del `27/10` NON LEGGIBILE** *(incrementi di fase circa `pi` per tick; il punto fisso di `cs` allora non convergeva)*.
- **`2026-11-17`, A3:** a norma fissata la nascita NON ha un costo intrinseco *(`compensazione_vuoto.txt`)*. **L'errore `n.188` del guardiano:** oggi la mitosi e' stata progettata sul «calore che paga» senza richiamare la decisione dell'`11/10`.

### 14.2 LA DEFINIZIONE *(del guardiano, letta sul codice)*

- **`Theta_a = pi * somma sui tick (dtau_nodo_i - dtau_nodo_j)`**, `dtau_nodo = mot.dtau * cs` *(`flussi_parziali.dtau_nodo`)*, `omega = pi / dtau_rif = pi`: **il nodo da' al vuoto la fase `pi s_k` per tick** *(sul vuoto `3 pi / 20` a `s = 0.15`)*. **Giusta senza fattori.** Invariante di gauge, locale, simmetrica allo specchio per costruzione.

### 14.3 I NUMERI

- **K1** *(`torsione_tempo_proprio_K1.txt`)*: sul vuoto F3 puro `cs = 0.15` uniforme al bit, Theta `0` su tutti i `103788` archi; il caso che deve fallire fallisce.
- **K3** *(`torsione_tempo_proprio_K3.txt`)*: la ripresa dagli stati AL BIT; **il trapezio fra stati ogni `250` tick sbaglia Theta del `96%` della scala** -> M3-bis *(l'errore `n.189` del guardiano: la stazionarieta' del lapse data per buona)*.
- **K2** *(`torsione_tempo_proprio_K2.txt`)*: **la fase relativa vera del vuoto NON si lega alla torsione del tempo proprio**: oltre `30` nodi la torsione in `50` tick e' al piu' `1.0e-05` rad, la fase relativa misurata si muove di `2.5e-02` *(mediana)*; **il rapporto: mediana `-10`, quartili `+-3.5e4`**; fra `10` e `20` nodi *(la torsione `1.4e-02`)* mediana `+7.5`, quartili `-334`, `+393`.

### 14.4 LE PREVISIONI DEL GUARDIANO

- **P-T5 FALSA** *(K2)*. **P-T1, P-T2, P-T3, P-T4: NON MISURATE** -- **M3-bis non e' partita per il FERMO di K2.**

### 14.5 COSA SIGNIFICA *(per «vicino ma fuori» e per il test di `3000` tick)*

- ### **NELLA FORMA LETTA DAL CODICE, LA TORSIONE DEL TEMPO PROPRIO NON E' L'OLONOMIA DEL VUOTO:** **la fase relativa delle estremita' e' dominata dalla dinamica d'arco** *(lo spostamento e il Grover mescolano i capi)*, **non dalla differenza dei due orologi.** **Quindi un innesco «a `|Theta_a| = 2 pi`» conterebbe una grandezza che il vuoto NON accumula** -- **non sarebbe il quanto di olonomia dell'`11/10`, ma un contatore del lapse.**
- **Per «vicino ma fuori»**: nessuna lettura possibile *(il ritmo per anello non e' misurato)*. **Per il test di `3000` tick**: **nessun innesco e' pronto** -- ne' D-R1-D-R3 *(sospese)*, ne' la torsione *(non legata)*.

### 14.6 FERMO PER LUCA

- **(a)** la torsione del tempo proprio **come contatore** *(un innesco dichiarato come tale, non come olonomia)* -- o no;
- **(b)** **cercare l'olonomia VERA del vuoto**: la fase relativa misurata delle estremita' *(cio' che K2 misura)*, **su finestre lunghe** o **filtrata** dell'oscillazione d'arco, con un criterio fissato prima;
- **(c)** **tornare a D-R1-D-R3**.
- **E, per la parte B:** l'area e `l/l*` dei triangoli nuovi *(la stella di Hodge sul reticolo irregolare: B.3, provvisori)*, con D-M3.

### 14.6-bis LA LETTURA DEL GUARDIANO SU K2 *(la sua, accanto alla mia della `14.5`; Luca `2026-11-17` `19:40`)*

- **Il guardiano:** **K2 era MAL POSTA** -- **un segnale di `1e-5` contro onde di `1e-2` in `50` tick** *(l'errore `n.190` del guardiano)*; **ma la conclusione REGGE per un motivo piu' forte:** **un vuoto stazionario ha UNA frequenza globale, e la somma di `(dtau_i - dtau_j)` su un ciclo e' ZERO** *(un GRADIENTE, non un'olonomia)*: **la torsione del tempo proprio e' al piu' un CONTATORE della deriva fra orologi vicini** *(l'opzione (a))*.
- **La mia, accanto:** **sono d'accordo su entrambe le cose.** **Sulla prima:** il rischio l'avevo scritto nella carta *(sez. `1.2`: «il rapporto puo' essere un quoziente di due numeri vicini allo zero»)* **ma ho fatto girare la prova com'era** *(la soglia era del mandato)*: **la scala `1.0e-05` stampata accanto lo mostrava.** **Sulla seconda:** **e' un argomento piu' forte di K2 e non dipende da nessuna misura** -- `Theta_a = pi somma_t (s_i - s_j)` e' la differenza di una funzione dei NODI, quindi **sulla chiusura di qualunque ciclo si annulla esattamente**: **non puo' essere un'olonomia per costruzione.** **Avrei dovuto vederlo leggendo la definizione** *(sez. `1.2` della carta della torsione: «uno scalare per nodo», scritto come un pregio)*.
- **M3-bis** *(i segmenti tick per tick, l'aggiunta delle `18:48`)* **gira**: **i suoi numeri sono il ritmo del CONTATORE (a)**, letto come tale *(la carta della torsione, sez. `6`)*.

### 14.7 IL FLUSSO DELLA PLACCHETTA *(il mandato di Luca del `2026-11-17` `19:40`; la carta `doc/TASK_HISTORY/2026-11-17_flusso_placchetta.md`; i referti `doc/referti_l2/flusso_placchetta.txt`, `.png`, `flusso_placchetta_K3.txt`)*

- **La definizione:** `Phi_p = e * somma +-A_a` sul bordo della placchetta antioraria, `e = 6.315414e-05`; **nel codice `Campo.B()` e' gia' la circolazione: `Phi = e * B()`** *(K4 al bit)*. ### **IL CAMPO DELLE CORSE E' NON COMPATTO** *(`p6_u_breve.FORMA`; la spinta usa `B / AREA`, non `sin B`)*: **il quanto `2 pi` qui NON ha il senso pieno** [[PROGETTO-U1]].
- **Le prove:** K1 *(`A = 0`)* `Phi = 0` su tutte le `69192` placchette; K2 la somma su tutte `3.3e-13` relativo; K4 il rotore del codice `0` al bit; **K3, la gauge a caso: `2.178e-10` contro la soglia `1e-12`: FALSA come scritta** -- **e' l'ARROTONDAMENTO, non la gauge** *(a posteriori, dichiarato)*: **`max |A| = 33.0` contro una circolazione massima `6.5e-05`** *(`A` e' quasi tutto GRADIENTE: il rapporto `5.1e+05`)*; lo scarto sta sotto il limite dell'arrotondamento a ogni ampiezza di `chi`; **in aritmetica esatta la circolazione e' invariata AL BIT** *(`0` su `69192`)*. Il caso che deve fallire *(un arco solo)* fallisce *(`1.2e+05`)*.
- ### **I NUMERI:** **in C2 `max |Phi|` fra `3.16e-09` e `5.22e-09` rad su tutti gli stati** *(da `k 250` a `3000`)*, **fra `12.8` e `21.6` nodi dal baricentro** *(nel guscio della materia, dentro il confine `23.81`)*; **`|Phi|` medio `1.4e-10`-`3.7e-10`**; **il segno medio vicino a `0`** *(`-0.008` a `k 3000`)*; **nel tempo RESTA**: la pendenza di `max |Phi|` `-1.7e-13 +- 2.1e-13` per tick; **`max |Phi| / 2 pi = 8.3e-10`**: ### **NOVE ORDINI sotto il quanto, e non cresce.** **C1 contro C2:** entro il `4.3%` *(il massimo a `k 2750`)*.
- **Le previsioni del guardiano:** **P-B1 VERA** *(`5.2e-09` contro `1e-2`)*; **P-B2 VERA** *(`12.8`-`21.6`)*; **P-B3 VERA** *(`4.3%`)*; **P-B4 FALSA come scritta** *(`2.2e-10`: l'arrotondamento, sopra)*. **Le mie:** P-B1 vera di molti ordini *(VERA: `Phi ~ e^2`)*; P-B2 non sapevo; P-B3 vera fino a `k 1000` *(VERA anche dopo)*; P-B4 vera *(FALSA come scritta: non avevo pensato alla cancellazione, con `A` cosi' grande)*.
- ### **COSA SIGNIFICA PER (d):** **il flusso della placchetta, nel campo di oggi, e' `1e-9` del quanto e NON cresce** *(e l'aliasing: gli stati ogni `250` tick non vedono un'oscillazione piu' veloce di `500`)*: **come innesco a `|Phi| = 2 pi` NON scatterebbe MAI** *(a nessun orizzonte: la pendenza e' zero entro l'errore)*. **Perche' scatti servirebbe un'altra cosa** *(un `e` diverso, il campo compatto, o un innesco a una frazione del quanto -- e quest'ultima sarebbe una MANOPOLA, `A1`)*.

### 14.8 FERMO PER LUCA: (a), (c) O (d)

- **(a) il contatore del lapse:** **un gradiente, non un'olonomia** *(14.6-bis)*; **il suo ritmo netto lo da' M3-bis, che GIRA** *(i `12` segmenti di C2; il referto quando chiudono)*.
- **(c) la riserva del calore:** **D-R1-D-R3, sospese** *(13.7)*; **e la domanda della `13.3`: la riserva conservata vuole un confine che assorbe.**
- **(d) il flusso della placchetta:** **invariante di gauge, locale, su un ciclo -- ma `1e-9` del quanto, fermo, e nel campo NON compatto** *(14.7)*.

## 15. L'INNESCO: IL CONTATORE DEL LAPSE *(il mandato di Luca del `2026-11-17` `21:00`; la carta `doc/TASK_HISTORY/2026-11-17_innesco_contatore.md`)*

### 15.1 LE DECISIONI DI LUCA *(`21:00`)*

- **L'innesco e' (a), IL CONTATORE DEL LAPSE:** `Theta_a = pi * somma sui tick (dtau_nodo_i - dtau_nodo_j)` *(14.2)*, **una memoria per arco; l'arco si divide a `|Theta_a| >= 2 pi`.** **Dichiarato come CONTATORE DELLA DERIVA FRA OROLOGI VICINI** *(la dilatazione gravitazionale del tempo)*, **NON come olonomia** *(14.6-bis)*. **`2 pi` e `omega = pi` dal modello.** **CONDIZIONATA alla deriva netta** *(il criterio di Luca, scritto prima del referto)*.
- **D-M3 = FA con la compensazione locale di A3** *(il minimo a norma fissata su `S` a `1` passo: `H` totale conservata alla nascita)*. **D-R1-D-R3 restano sospese.** **Restano** D-M1, D-M2, D-M4, D-R4, D-R5, il bordo tolto, C2 braccio senza mitosi, il mattone su `L 186`.
- **Le scelte del guardiano:** **S1** *(la materia della nascita FA sotto l'`1%` di `|DH|`: ### **l'`1%` E' UN NUMERO, `A1`: una scelta del guardiano, da rivedere con Luca**)*; **S2** *(gli archi nuovi da `Theta = 0`, l'arco diviso consumato)*; **S3** *(la compensazione deterministica e simmetrica, o una regola sulla fase, o FERMO)*; **S4** *(P7 riscritta: la FORMA del profilo della curvatura di Regge contro `N(rho)`)*.

### 15.2 LA DERIVA NETTA C'E' *(`doc/referti_l2/torsione_segmenti.txt`: i `12` segmenti di C2, tutti AL BIT con lo stato salvato successivo)*

- ### **IL CRITERIO DI LUCA PASSA:** **sull'arco del massimo** *(r `18.12`)* **la deriva netta in `3000` tick e' `0.675` rad contro un'oscillazione massima di `0.0082`** *(la pendenza a `3630 sigma`)*; **tutti i `20` archi del massimo lo passano.** **(a) VALE.**
- **Il ritmo netto massimo `2.256e-04 +- 6e-08` rad per tick a r `18.08`** *(l'anello `18`; la media per anello piu' alta al `17`)*; **oltre `24` nodi crolla** *(`7e-08` all'anello `24`, `3e-09` al `27`)*.
- **Il primo `2 pi` al tick `2.79e+04`**; entro `1e4` nessuno; ### **entro `1e5`: `2929` archi, TUTTI fra `10.0` e `22.3` nodi; entro `1e6`: `5346`, fra `2.3` e `23.45` -- TUTTI DENTRO IL CONFINE** *(`23.81`)*.

### 15.3 S1 NON NE LASCIA PASSARE NESSUNO *(`doc/referti_l2/innesco_S1.txt`)*

- ### **`0` SU `2929`:** **nel guscio della materia il termine della materia della nascita FA e' praticamente TUTTO `|DH|`** *(materia/`|DH|` fra `0.93` e `1.37`, mediana `1.003`)*, **e `DH` e' fortemente NEGATIVO** *(la mediana da `-1.2e+03` a `10`-`12` nodi a `-26` a `22`-`24`)*: **le nascite la' RILASCIANO energia della materia.** *(Lo stato di C2 a `k 3000`, non quello allo scatto: dichiarato.)*

### 15.4 LA STIMA DELLA CORSA GEMELLA *(`doc/referti_l2/innesco_stima.txt`)*: ### **IMPRATICABILE con queste scelte**

- **Perche' nascano `10` nodi oltre il confine `23.81`:** il ritmo netto massimo la' e' `1.25e-06` rad per tick; **il `10`-esimo arco a `2 pi` al tick `7.47e+06` = `7652` ore al tick misurato** *(`3.690` s, C2)*: **`0.9` anni** -- **e a `23.81` con FA la materia e' ancora il `6%` di `|DH|`** *(`regole_fase_F3.txt`)*: **S1 bloccherebbe i primi.**
- **Oltre `29.81`** *(dove FA ha la materia sotto l'`1%`: `0.24%`)*: il ritmo `1.2e-08`; **il `10`-esimo al tick `6.2e+08` = `73` anni.**
- **L'estensione di C2 alla stessa lunghezza:** lo stesso costo.

### 15.5 LE PREVISIONI DEL GUARDIANO

- **P-L1 VERA** *(il criterio passa, `20` su `20`)*; **P-L2 VERA** *(r `18.08`)*; **P-L3 VERA** *(`2.79e+04`)*; **P-L4 VERA, all'estremo** *(`0` su `2929`, non «meno della meta'»)*; **P-L5 NON MISURATA** *(la compensazione sul ramo `mitosi`: il TODO 3 non e' partito, sotto)*. **Le mie:** P-L1-P-L4 vere come le sue; su P-L5 nessun numero.

### 15.6 COSA SIGNIFICA, E FERMO PER LUCA

- ### **IL CONTATORE DEL LAPSE SCATTA SOLO NEL GUSCIO DELLA MATERIA** *(dove il gradiente di `N(rho)` e' grande)*, **e li' la nascita e' dominata dalla materia; S1, che vuole il vuoto, la vieta.** **Le due cose si escludono: con (a) piu' S1 la mitosi NON scatta in un tempo praticabile** *(il primo arco oltre il confine a `5e6` tick, i primi `10` dove S1 passa a `6e8`)*. **«Vicino ma fuori» e il contatore non stanno insieme.**
- **Le strade** *(nessuna scelta presa)*: **(i)** togliere S1 o cambiarne la natura: **le nascite nel guscio, dentro la materia** *(`DH` negativo: la compensazione di A3 conserva `H`, quindi l'energia rilasciata va nel vuoto attorno)*; **(ii)** tenere S1 e accettare che la mitosi non scatti nel mattone di `L 186` *(il test sul mattone non si fa)*; **(iii)** un altro innesco per il vuoto fuori dal confine.
- ### **IL TODO 3 NON E' PARTITO** *(B4, la memoria per arco, la regola, FA e la compensazione, le prove P6-P9 sul ramo `mitosi`)*: **B4 e la memoria per arco non dipendono da questa scelta; la REGOLA di nascita si'** *(dove si permette: S1)*, **e la corsa gemella che le prove preparano oggi non si puo' fare.** **Se Luca vuole, B4 riparte da subito.**

### 15.7 SOSPESO *(Luca `2026-11-17` `23:07`)*

- ### **SOSPESO (Luca 23:07): la ripresa da `doc/SOSPESO_2026-11-17_MITOSI_INNESCO.md`.** Nessuna corsa aperta, il ramo `mitosi` resta com'e'.

## 16. LA RIPRESA: LE NASCITE NEL GUSCIO A ENERGIA NULLA *(il mandato di Luca del `2026-11-20` `10:31`; la carta `doc/TASK_HISTORY/2026-11-20_nascita_energia_nulla.md`)*

### 16.1 LE DECISIONI DI LUCA *(`10:31`)*

- **La strada (i) della `15.6`:** lo spazio puo' nascere **NEL GUSCIO della materia**, dove scatta il contatore del lapse *(15.2: `10`-`22` nodi)*. **S1 del `2026-11-17`** *(il filtro della materia all'`1%`)* **e' TOLTA.**
- ### **IL «VICINO MA FUORI» DEL `2026-11-17` E' SUPERATO.** **La ragione** *(di Luca)*: **il contatore scatta solo dove il tempo e' curvo** *(15.2: il ritmo netto crolla oltre `24` nodi)*, **e lo spazio in se' non costa** *(A3, 13.3: a norma fissata la nascita non ha un costo intrinseco)*. **Il vincolo che lo sostituisce e' l'ENERGIA NULLA, sotto.**
- **La nascita e' A ENERGIA NULLA:** la regola della MATERIA sulle estremita' nuove si sceglie, nascita per nascita, perche' `DH` totale `= 0` *(con FA per il vuoto)*. **La compensazione di A3 resta SOLO come riserva** dove la materia e' trascurabile *(li' la famiglia non ha radice: sul vuoto puro `DH = +3.476` con FA, `regole_fase_F3.txt`)*.
- **In vigore:** l'innesco (a), D-M1, D-M2, D-M4, D-M3 = FA, D-R4, D-R5, D-R1-D-R3 sospese, il bordo tolto, C2 braccio senza mitosi, il mattone su `L 186`; S2 e S4 del `21:00`.

### 16.2 LA FAMIGLIA E LA RADICE *(del guardiano, su delega; il testo intero nella carta del mandato, sez. `1.2`-`1.4`)*

- **`alpha` = la frazione della norma del padre che passa al nodo nuovo, in unita' di D7:** le estremita' del padre `i` divise per `sqrt(2/(2 - alpha))`, le `4` di `n` a `sqrt(alpha)` volte quelle di D7. **`alpha = 1` e' D7 al bit; `alpha = 0` e' «`psi` trasportata senza dividerla».** La norma conservata, locale, deterministica.
- **La radice per bisezione a `53` passi fissi** *(la risoluzione del double: un numero di precisione, dichiarato)*.
- ### ⚠ **La premessa:** **il padre di D7 e' il SORGENTE dell'arco: lo specchio a `30` gradi rovescia una direzione su tre, e su quegli archi la famiglia, come D7, non puo' essere simmetrica.** P5 si stampa separata.

### 16.3 LE PREVISIONI *(copiate PRIMA delle misure)*

- **P-Z1.** La radice esiste su almeno il `95%` dei `2929` archi. **P-Z2.** `alpha*` strettamente dentro `(0, 1)` sulla maggior parte. **P-Z3.** Alla radice deterministica al bit e simmetrica allo specchio. **P-Z4.** Nelle `20` nascite in fila `|H(dopo) - H(prima)| / |H|` sotto `1e-10`. **P-Z5.** Una nascita costa meno di `10` tick.
- **Le mie:** P-Z1 non lo so *(serve `DH(0) > 0`)*; P-Z2 vera se la radice c'e'; **P-Z3 deterministica si', simmetrica solo sugli archi a verso conservato**; P-Z4 vera; P-Z5 qui solo in parte.

### 16.4 LE AGGIUNTE DI LUCA DELLE `10:41` E `10:47`: LA SPINTA, LA SATURAZIONE, LA MATERIA E LA METRICA *(il testo intero nella carta del mandato, sez. `6`)*

- **La domanda:** la crescita attorno alla massa si SATURA *(IPOTESI G)* o NO *(IPOTESI E)*: **alla pari, la lettura dopo i numeri.** **«Spinto in la'» = la distanza IN PASSI lungo il grafo**; lo strumento `doc/referti_l2/distanza_passi.py` *(D1-D3, E1)*, in MITOSI e C2-EXT ogni `250` tick.
- **La nota del guardiano:** **se tutto si espande insieme l'espansione non si vede; in un'espansione vera si conservano i conteggi** *(norma, carica)*, **non l'energia; l'energia nulla e' una scelta da metrica statica.** **D-PRINCIPIO** *(energia nulla o covariante)* **e' di Luca, dopo i numeri; il mandato prosegue con l'energia nulla.**
- **La covariante, solo misurata:** le estremita' di `n` = la media delle estremita' di `i` e di `j` nella stessa direzione; un fattore uniforme sulla stella per `psi` e uno per `phi`; nessun padre.
- **Le previsioni:** P-S1 *(i passi all'anello `40` crescono in MITOSI, costanti in C2-EXT)*, P-S2 *(la crescita rallenta)*, P-S3 *(le nascite restano nel guscio)*, P-E1 *(il mattone torna alla sua larghezza in passi)*, P-E2 *(`DH_cov` negativo su piu' della meta')*.

### 16.5 LA NASCITA A ENERGIA NULLA: ### **LA RADICE NON ESISTE** *(`doc/referti_l2/nascita_energia_nulla.txt`, `nascita_energia_nulla_anelli.txt`)*: **FERMO DEL MANDATO**

- ### **SU `0` DEI `2929` ARCHI:** **`DH(0)`** *(il trasporto senza divisione)* **e `DH(1)`** *(D7)* **sono TUTTI negativi** *(mediane `-566` e `-555`; da `-1.4e+03` a `10`-`12` nodi a `-22` a `22`-`24`)*, **e sugli `11` punti di `alpha` nessun cambio di segno.** **La radice manca sul `100%`: oltre il `20%` del mandato, FERMO.**
- ### **IL PERCHE': LA FAMIGLIA QUASI NON CONTA.** **`DH(1) - DH(0)` ha la mediana `+8.5`** *(da `-44` a `+69`)*, **contro un `DH` di centinaia** *(`DH(1)/DH(0)` fra `0.87` e `0.99` per anello)*. **Sui primi `50` archi, col conto pieno, a `alpha 0`:** `G_psi -313`, `a_psi -177`, `N +1.7`, il vuoto `+1.3` *(le mediane)*. **La caduta c'e' gia' SENZA spostare niente**: **la mia lettura sul codice** *(`famiglie`: il termine di nodo `-Omega (0.5 nrm - |S|^2/d)`, il termine d'arco di `a`)*: **(1) le estremita' nuove in `k` e in `l` nascono con `psi = 0`: il grado sale da `6` a `7` senza ampiezza, `|S|^2/d` scende, il termine di nodo SCENDE; (2) l'arco diviso porta via il suo termine d'arco.** **Spostare la norma del padre al nodo nuovo non ci arriva.** *(Una lettura: non scomposta per nodo.)*
- **Il resto:** il caso noto *(`alpha 1` = `regole_fase_F3` FA)* **al bit**; il determinismo *(due processi)* **al bit**; il conto a mano contro il pieno `2.7e-16` di `|H|`. ### ⚠ **LO SPECCHIO PASSA A VUOTO** *(un FALSO-UNO)*: **senza radice lo script confronta solo lo stato**, e **il caso che DEVE FALLIRE da' `0` anche lui**: **lo specchio NON e' misurato**, e **la premessa sul padre di D7** *(1.3 della carta del mandato)* **resta aperta.**
- **LE PREVISIONI:** P-Z1 FALSA *(`0%`)*; P-Z2 FALSA *(nessuna radice)*; **P-Z3: deterministica VERA; lo specchio NON misurato**; P-Z4 non misurabile *(`0` nascite in fila)*; P-Z5: il pezzo di questo script `0.36` s = `0.10` tick di C2, **senza** la CSR e Gauss.
- ### **LE STRADE, PER LUCA** *(nessuna presa)*: **(a) una famiglia piu' larga**: **la regola della materia deve mettere `psi` ANCHE sulle estremita' nuove in `k` e `l`** *(e sul nodo nuovo piu' della meta' del padre)*: e' cio' che fa la **covariante** *(6.3: le medie nella stessa direzione, la norma sulla stella)*; **(b) D-PRINCIPIO verso la covariante** *(l'energia libera)*: **la sua misura E2 e' PRONTA da scrivere e NON e' fatta** *(il FERMO viene prima)*; **(c) la compensazione di A3 sul vuoto**: **NON misurata qui**; il vuoto della stella vale decine *(la stima del guardiano)*, `DH` centinaia. ### **La mia raccomandazione: prima E2** *(la covariante sugli stessi `2929` archi: dice se la nascita che mette `psi` su `k`, `l`, `n` arriva vicino a zero o no)*, **poi la scelta.**
- **Il ramo `mitosi`, a parte:** **B4** *(`68089e6d`)* **e la memoria `Theta`** *(`c14a087b`)* committati, la suite `67/67`; **la prova di `Theta` passa** *(`11/11`)*; **la prova di B4 v1 si e' fermata su un errore della PROVA** *(la scena finta senza `righe`)*: **la v2 in un file nuovo.**

## 17. LA COVARIANTE, LA FAMIGLIA FRA D7 E LA COVARIANTE, E LO SPECCHIO VERO *(il mandato di Luca del `2026-11-20` `11:57` e la correzione delle `12:10`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_e_specchio.md`; i referti `doc/referti_l2/covariante_e_famiglia.txt`, `covariante_vuoto_F3.txt`)*

### 17.1 E2: LA COVARIANTE DA SOLA *(`psi` e `phi` covarianti; lo stato di C2 a `k 3000`, dichiarato)*

- ### **`DH_cov` mediana `-11.9`** *(da `-39.3` a `+2.9`)*, **contro `DH(D7)` mediana `-555`: il `2.15%`.** **Negativa su `2840` archi su `2929`.** Per anello *(le mediane)*: `-26.3` a `10`-`12` nodi, `-13.2` a `16`-`18`, `-1.8` a `20`-`22`, `+0.19` a `22`-`24`. **Per termine** *(mediane)*: `G_psi +1.45`, **`a_psi -13.8`**, `N +0.002`, il vuoto `+0.48`: **mettere ampiezza in `k`, `l`, `n` recupera il termine di nodo; resta quasi solo il termine d'arco.**
- **Il caso noto del codice** *(il campo uniforme: le estremita' nuove al bit)* **PASSA.** `beta = 1` *(la covariante con `phi` FA)* contro E2: la differenza di `DH` mediana `+0.58`.

### 17.2 IL VUOTO F3 PURO *(il caso corretto delle `12:10`, `covariante_vuoto_F3.txt`; la riga «`H / n`» di `covariante_e_famiglia.txt` e' SUPERATA: l'errore `n.191`)*

- ### **`DH_cov = +0.034`: vicino a `0`** *(FA sullo stesso arco: `+3.476`)*: **il caso e' LETTO, ma NON come atteso.** **L'estremita' nuova di `k`** *(la media delle estremita' di `k` verso `i` e verso `j`)* **e' ESATTAMENTE `0`**: **nel vuoto F3 le due hanno modulo `1` e fasi OPPOSTE.** **Con `k` e `l` presi da UNA direzione** *(verso `i` o verso `j`, lo stesso numero)*: **`DH = +3.583`**, come FA. ### **POST-HOC, dichiarato:** **non c'e' un «residuo dalla media che riduce l'ampiezza»: la media ANNULLA `k` e `l`, ed e' proprio cio' che tiene `DH` vicino a `0`.** **Nel vuoto la covariante lascia `k` e `l` vuoti come D7 lasciava `k` e `l` vuoti nella materia: li' non costa, qui costava.**

### 17.3 LA FAMIGLIA `beta` *(`psi` = `(1 - beta) D7 + beta COV` sulla stella, `phi` FA)*

- ### **LA RADICE SU `197` ARCHI SU `2929` (`6.73%`)**: **solo dove `DH(beta = 1) > 0`**, **e quasi tutti al bordo esterno del guscio** *(`0` fino a `18` nodi; `24` a `18`-`20`, `165` a `20`-`22`, `8` a `22`-`24`)*. **Dentro, anche la covariante con `phi` FA abbassa l'energia** *(le mediane `DH(beta = 1)` da `-21.4` a `-1.1`)*. `beta*` mediana `0.854` *(da `0.548` a `0.967`)*; i cambi di segno sugli `11` punti: `0` su `2721`, `1` su `197`, `2` su `11`.
- **Alla radice:** `|DH|` col conto pieno al piu' `1.4e-09` *(`4.1e-16` di `|H|`)*. **Il determinismo: due processi AL BIT, uguali alle parti** *(la v2, `covariante_det_v2.py`: la v1 e' caduta nella fila, sotto)*. **Le `20` nascite IN FILA:** `|H(dopo) - H(prima)| / |H|` **al piu' `4.1e-16`** *(`beta*` da `0.851` a `0.948`)*; per trovarle la fila ha saltato **`865` candidati senza radice e `2` dove la covariante NON E' DEFINITA**.
- ### ⚠ **LA COVARIANTE NON E' DEFINITA SU TUTTO IL GRAFO CRESCIUTO:** usa il vicino di `i` in `-a` e quello di `j` in `+a`, **e accanto a un difetto gia' nato quel vicino non esiste** *(la v1 della fila: `nessun vicino di 21125 nella direzione opposta`)*. **Va ridefinita sul grafo generico prima di ogni corsa** *(una decisione: quale vicino quando la direzione non c'e')*.
- **La D7 simmetrica** *(un quarto da ciascun capo, misurata accanto)*: `DH` mediana `-528`: **come D7**.

### 17.4 LO SPECCHIO VERO *(`200` archi: `132` a verso conservato, `68` ROVESCIATI; nascere e specchiare contro specchiare e nascere, array per array)*

- ### **LA PROVA VALE:** **il caso che DEVE FALLIRE** *(il padre = il nodo di indice minore)* **FALLISCE: `0.51`** *(sui `68` rovesciati)*.
- **D7: simmetrica sui conservati** *(`2e-16`)*, **NON sui rovesciati: `68` su `68`** *(`psi` `0.20`, `phi` `0.51`)*. **La COVARIANTE: simmetrica su TUTTI** *(`2e-16`)*. ### **La D7 simmetrica: `psi` simmetrico su tutti, ma `phi` NO sui rovesciati (`0.51`)**: **`phi` e' FA, e FA HA ANCHE LUI IL PADRE** *(le fasi di `n -> k`, `n -> l` dalle estremita' di `i`)*. ### **Quindi D-M3 = FA e' asimmetrica allo specchio sugli archi rovesciati, da sola** -- **e ogni regola che usa FA per `phi`** *(la famiglia `beta` compresa)* **la eredita.**
- **La radice della famiglia:** confrontabile **su `1` arco solo** *(a verso conservato; `1.8e-12`)*, **`0` rovesciati** *(la radice esiste su pochi archi)*: **il «PASSA» del referto e' QUASI A VUOTO** -- **e per la riga sopra, sui rovesciati NON puo' essere simmetrica** *(`phi` FA)*. **Dichiarato.**

### 17.5 LE PREVISIONI

- **P-C1 VERA** *(`2.15%` contro la soglia `30%`)*; **P-C2 FALSA** *(`6.73%` contro `80%`)*; **P-C3 VERA** *(D7 asimmetrica su `68` su `68` rovesciati, la covariante simmetrica su tutti)*; **P-C4 VERA** *(al bit; la fila `4.1e-16`)*; **P-E2 VERA** *(`2840` su `2929`)*. **Le mie:** P-C1 e P-C2 «non lo so»; **P-C3 vera, come la mia premessa** *(che ora tocca anche FA)*; P-C4 vera.
- **La previsione sul vuoto «`H / n`» della carta 1.4: FALSA e mal posta** *(l'errore `n.191`)*; il caso corretto e' la `17.2`.

### 17.6 LA CONDIZIONE PER RIPARTIRE: ### **NON C'E'. FERMO.**

- **Il mandato:** se la radice c'e' su almeno l'`80%` **E** la radice e' simmetrica, i TODO `4`-`5` delle `10:31` potrebbero ripartire con `beta`. **La radice c'e' sul `6.73%`, e la sua simmetria non e' stabilita** *(e con `phi` FA non puo' esserlo sui rovesciati)*. **I TODO `4`-`5` NON ripartono.**

### 17.7 D-PRINCIPIO, PER LUCA *(le due strade coi numeri; NESSUNA presa)*

- **ENERGIA NULLA** *(la famiglia `beta`)*: **PRO:** `H` conservata al bit *(`4.1e-16` in `20` nascite)*, deterministica. **CONTRO:** **la radice esiste sul `6.7%` degli archi del guscio, al suo bordo esterno**: **dove il contatore scatta di piu'** *(`10`-`18` nodi)* **non nasce niente**; usa D7 e FA, **asimmetriche allo specchio sui rovesciati**; e' una scelta da metrica statica *(la nota del guardiano delle `10:47`)*.
- **COVARIANTE** *(E2)*: **PRO:** **simmetrica allo specchio su TUTTE le classi, per costruzione e misurata** *(`2e-16`)*; norma e carica esatte; nessun padre; `DH` piccolo *(il `2%` di D7; negativo: l'energia scende come in uno spostamento verso il rosso)*. **CONTRO:** **l'energia NON si conserva** *(la mediana `-12` per nascita: dove va e' da decidere)*; **non e' definita accanto a un difetto gia' nato** *(serve la sua definizione sul grafo generico)*.
- ### **LA MIA RACCOMANDAZIONE** *(motivata; la scelta e' di Luca)*: **la COVARIANTE**, perche' e' l'unica simmetrica e nasce dove il contatore scatta; **ma prima due decisioni:** **(1) la covariante sul grafo generico** *(il vicino «opposto» quando non c'e')*; **(2) che cosa fare dell'energia che scende** *(lasciarla scendere, o una compensazione)*. **E A PARTE, PER QUALUNQUE STRADA: FA E' ASIMMETRICA ALLO SPECCHIO** *(D-M3)*: **la covariante di `phi` non lo e'.**

## 18. LA COVARIANTE DI STELLA E IL FLIP *(il mandato di Luca del `2026-11-20` `13:33`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md`; il referto `doc/referti_l2/covariante_di_stella.txt`)*

### 18.1 LE DECISIONI DI LUCA *(`13:33`)*

- **D-PRINCIPIO = COVARIANTE** *(norma e carica esatte; l'energia puo' scendere)*; **la famiglia `beta` e l'energia nulla ABBANDONATE** *(restano come misura, sez. `16`-`17`)*; **D-M3 = COVARIANTE anche per `phi`** *(FA SOSTITUITA)*; **D-COVSTELLA:** la covariante di stella *(da misurare prima di adottarla)*; **D-EPERSA:** `H + E_persa` costante, `E_persa = - somma dei DH` *(il segno, dichiarato: la carta del mandato 1.2)*.

### 18.2 LA COVARIANTE DI STELLA: ### **LA CONDIZIONE DI LUCA PASSA**

- ### **DEFINITA sul `100%`** *(`2929` su `2929`; la fila: `20` nascite in fila, NESSUNA non definita, nessun arco senza due vicini comuni)*.
- ### **SIMMETRICA ALLO SPECCHIO su TUTTE le classi:** `psi` al piu' `2.5e-16`, `phi` `2.0e-16` sui `132` conservati; **sui `68` ROVESCIATI `1.4e-16` e `1.3e-16`** *(la soglia `1e-14`)*. **Il caso che DEVE FALLIRE fallisce** *(il padre a indice minore: `0.51`)*: **la prova vale.**
- ### **DETERMINISTICA AL BIT** *(due processi, i `100` archi e la fila, uguali alle parti)*.
- ### **`H + E_persa` COSTANTE: al piu' `2.7e-16` di `|H|`** in `20` nascite *(`E_persa` arriva a `+395`)*; ### ⚠ **QUASI TAUTOLOGICO qui** *(nessuna dinamica fra le nascite: dice che il conto a mano e il pieno coincidono)*; **il controllo vero e' P9 sul ramo.**
- **`DH_SC`:** mediana **`-12.6`** *(da `-40.9` a `+0.98`; negativo su `2916` su `2929`)*; accanto E2 `-11.9`, D7 `-555`. Per anello *(mediane)*: `-28.1` a `10`-`12` nodi, `-13.7` a `16`-`18`, `-3.3` a `20`-`22`. **Per termine:** `a_psi -14.5`, `G_psi +1.36`, il vuoto `+0.31`, `N +0.0007`. **La norma della stella conservata:** materia `2.3e-12`, vuoto `1.4e-14` *(assoluti)*.
- **Il caso noto del codice** *(il campo uniforme al bit)* **PASSA. Il vuoto F3 puro** *(nessuna attesa)*: `DH_SC = +0.0338`, **lo stesso di E2** *(sul vuoto puro `n -> i`, `n -> j` della stella e della sez. `17` coincidono)*.
- **Le previsioni:** **P-SC1 VERA, P-SC2 VERA, P-SC3 VERA** *(`-12.6`)*, **P-SC4 VERA** *(quasi tautologica)*. **P-SC5: NON misurabile** *(il flip non esiste: sotto)*.

### 18.3 IL FLIP *(il TODO 3 comincia qui)*: ### **NON ESISTE; LA PROPOSTA DI STELLA; FERMO PRIMA DI ADOTTARLA**

- **[codice] Il flip DOPO LA DIVISIONE** *(D-M2)* **non esiste.** **Esiste un flip di misura:** `csv/_conto_del_vuoto.flip` *(C3, sul toro perfetto)*: **l'arco `i -> j` diventa `l -> k`, e l'estremita' in `i` va in `l`, quella in `j` va in `k`**: **una scelta con un VERSO** *(lo specchio che scambia `k` e `l` la manda nell'altra)*. **La sez. `10.3`** propone la SCELTA del flip *(«il massimo di una grandezza locale dello stato: la tensione del vuoto sull'arco che nasce»)*: **quella grandezza non e' definita sul codice.**
- ### **LA PROPOSTA DEL GUARDIANO** *(Claude Code; NON adottata)*: **IL FLIP DI STELLA**
  - **I candidati** *(10.3)*: i quattro lati del rombo attorno a `n`: `(i, k)`, `(k, j)`, `(j, l)`, `(l, i)`. **Il flip del lato `(u, v)`:** l'arco `u - v` si toglie; nasce `n - m`, con **`m` = il vicino comune di `u` e `v` diverso da `n`** *(l'altro triangolo del lato: esiste su ogni grafo di triangoli)*.
  - **Le estremita' dell'arco nato:** **in `n` = la media delle estremita' di `n` verso `u` e verso `v`; in `m` = la media delle estremita' di `m` verso `u` e verso `v`** *(fra le quali l'arco si infila: la stessa regola della covariante di stella in `k`)*; **poi un fattore UNIFORME sulla stella del flip** *(i nodi `u, v, n, m`)* **che rimette la norma, per `psi` e per `phi`.** **Nessun padre, nessuna direzione: definita su ogni grafo e simmetrica allo specchio per costruzione.**
  - **La scelta fra i quattro** *(equivariante per costruzione)*: **il flip con `H` piu' BASSO dopo** *(ognuno dei quattro col conto, con la regola sopra)*; ### **il pari merito → nessun flip a questo tick** *(10.3)*. ### ⚠ **IL PARI MERITO VUOLE UNA TOLLERANZA: E' UN NUMERO** *(`A1`)*: **la proposta `1e-12 |H|`** *(sopra l'arrotondamento del conto, `2.7e-16`)* **-- DA DECIDERE CON LUCA.** **E il `DH` del flip entra in `E_persa`.**
  - **Le alternative per la scelta** *(scritte, non scelte)*: il massimo di `|a_phi|` sull'arco nato *(una «tensione del vuoto»)*; il flip che porta `n` a `5` col vicino di grado `7` piu' vicino al centro *(geometrico: vuole le posizioni, che restano fuori dal nucleo)*.
- ### **FERMO prima di adottarlo** *(il mandato)*: **la regola delle estremita', la grandezza della scelta e la tolleranza del pari merito sono di Luca.** **I TODO `3`-`4`** *(la regola completa sul ramo, le prove P6 prima, la stima delle due corse)* **aspettano.**

### 18.4 IL FLIP DI STELLA *(l'aggiunta di Luca delle `13:54`; il referto `doc/referti_l2/flip_di_stella.txt`; la carta del mandato sez. `7`)*

- **La decisione di Luca:** **il flip di stella come regola delle ampiezze** *(le medie in `n` e in `m` verso `x` e `y`, il fattore uniforme su `n, x, m, y`)*; **`E_persa = - somma dei DH`** e conta anche il flip *(l'errore `n.192` era nel mandato)*.
- ### **F1 PASSA** *(il campo uniforme al bit)*. ### **F2: il flip di stella e' SIMMETRICO su TUTTI gli `800` flip** *(`200` nascite x `4` candidati; al piu' `3.9e-16` contro `1e-14`)*; **nessun candidato non definito.** ### **F3 PASSA su `800` su `800`** *(i gradi, Eulero, nessun arco doppio, ogni arco in due triangoli)*. **Il `DH` del flip** *(a mano, NON usato)*: mediana `+0.14`, da `-9.1` a `+7.2`.
- **Il caso che DEVE FALLIRE** *(il flip col verso, come C3)*: **fallisce, `1.15`: la prova vale.** ### ⚠ **MA NON DOVE AVEVO SCRITTO:** cade su `264` dei `528` flip delle nascite a verso CONSERVATO, e su NESSUNO di quelle ROVESCIATE. **Il perche'** *(POST-HOC, dichiarato)*: **conta il verso dell'arco GIRATO `x - y`, non quello dell'arco diviso `a`**: se `a` e' nella direzione che lo specchio rovescia, i suoi quattro lati stanno nelle altre due *(nessuno rovesciato)*; se `a` e' conservato, **due lati su quattro** stanno nella direzione rovesciata *(`264 = 528 / 2`)*. **La classe di `a` non era la classe giusta per il flip: un mio errore nella previsione P-F2** *(la seconda meta': «il flip di C3 cade sui rovesciati» -- FALSA come scritta, vera per gli archi girati rovesciati)*.
- **Le previsioni:** **P-F1 VERA; P-F2: il flip di stella simmetrico VERA, il flip col verso «sui rovesciati» FALSA come scritta** *(sopra)*; **P-F3 NON misurata** *(la scelta non si usa)*.
- ### **LA SCELTA FRA I QUATTRO: FERMO** *(la carta del mandato 7.2)*: **la grandezza della `10.3` non e' univoca** *(rimanda a una soglia mai decisa; la «tensione d'arco» ha due letture)*. **La proposta del guardiano:** **Q1 sull'arco nato `n - m`** *(`Omega Re(conj(phi_nm) phi_mn) + Omega |phi_nm| |phi_mn|`: nulla quando le due estremita' sono opposte come nel vuoto F3)*, **il pari merito entro `8` ulp del massimo** *(un NUMERO, `A1`)* **→ nessun flip.** **Da decidere da Luca prima di usarla; poi P-F3, P5 sulla regola intera, e i TODO `3`-`4`.**

### 18.5 LA REGOLA INTERA *(l'aggiunta di Luca delle `14:53`; il referto `doc/referti_l2/regola_intera.txt`; la carta del mandato sez. `8`)*

- **Le decisioni:** **D-FLIP-AMPIEZZE e D-COVSTELLA ADOTTATE; D-FLIP-SCELTA (A):** il lato che lascia `H` piu' bassa *(il conto pieno)*; **il pari merito sotto `1e-12 |H|`: nessun flip** -- ### **una GUARDIA CONTRO L'ARROTONDAMENTO** *(circa `3700` volte il `2.7e-16` del conto)*, **NON una manopola fisica** *(`A1`)*. **`E_persa = - (DH nascita + DH flip)`.** L'errore `n.193` del guardiano *(la classe giusta in P-F2 era l'arco girato)*.
- ### **P-F3 VERA: il flip c'e' su `2929` nascite su `2929`** *(nessun pari merito)*; i quattro lati scelti quasi alla pari *(`723`, `729`, `738`, `739`)*. ### **P-F4 VERA:** lo scarto fra il migliore e il secondo **mediana `7.6e-07 |H|`** *(il minimo `1.4e-10 |H|`: 136 volte la guardia; `35` sotto `1e-8 |H|`)*.
- **I `DH`** *(mediane)*: la nascita `-12.6`, **il flip scelto `-3.4`** *(da `-12.9` a `+6.7`)*; **`E_persa` per nascita `+16.2`.** Per anello il flip pesa di piu' verso l'esterno *(`-1.0` a `10`-`12` nodi, `-4.7` a `20`-`22`)*.
- ### **P-F5 VERA: la regola intera e' simmetrica allo specchio su TUTTE le classi** *(lo stesso lato su `200` archi su `200`; al piu' `3.8e-16`, sia per l'arco girato sia per l'arco diviso, conservati e rovesciati)*. **Il caso che DEVE FALLIRE** *(la regola col flip col verso)*: **cade, `26` lati diversi e `0.74`: la prova vale.** ### ⚠ **«I pari merito: nessun flip su entrambi i lati» PASSA A VUOTO** *(non c'e' nessun pari merito)*: **non e' misurato.**

### 18.6 IL TODO 3 SUL RAMO: ### **QUATTRO PUNTI CHE NON SONO CONTI, E FERMO**

**Per far nascere nella corsa VERA** *(il motore, il campo U(1), il lapse: `Motore.cresci`, B3, B4, la memoria `Theta`)* **servono quattro cose che il codice non decide e i mandati non hanno ancora deciso:**

1. ### **L'AREA E IL `l/l*` DEI TRIANGOLI E DEGLI ARCHI NUOVI** *(la domanda di Luca accodata dalle `16:38` del `2026-11-17`; B3 li vuole senza default, la sua prova usava valori PROVVISORI: le meta' geometriche e `sqrt(3)`)*. **(a) COMBINATORIA:** **ogni triangolo ha l'area del triangolo di oggi e ogni arco `l/l* = sqrt(3)`** *(il grafo e' fatto di triangoli equilateri: la curvatura sta solo nei gradi, `(6 - k) x 60` gradi, come Regge e P7)*; **(b) GEOMETRICA:** dalle POSIZIONI *(le meta' dei triangoli divisi)*. ### **La mia raccomandazione: (a)** -- **deriva dalla decisione di Luca delle `10:41`** *(«i nodi non hanno posizione; le posizioni restano solo per disegnare»)*: **(b) la contraddirebbe.** **Con (a) l'area totale CRESCE con le nascite** *(lo spazio che nasce)*.
2. ### **`A` SUGLI ARCHI NUOVI E SULL'ARCO GIRATO** *(la carta sez. `2`: «il flusso attorno ai triangoli nuovi conservato»)*: **alla nascita** la regola di B3 *(meta' flusso ai mezzi triangoli)*; **al flip** *(nessuna regola scritta)*: **la proposta di stella: il flusso del quadrilatero `n - x - m - y` spartito a META' fra i due triangoli nuovi** *(simmetrica, nessun verso)*. **`E`: Gauss VERO sul grafo nuovo** *(la carta sez. `2`)*.
3. ### **QUALE `H` PER LA SCELTA E PER `E_persa` NELLA CORSA:** **la misura usa il conto della carta** *(`famiglie`: `U = I`, `cs` spento, `eps = 0`)*; **la corsa ha la sua energia** *(`conti_nodo` + il campo, con `U` e il lapse veri)*. **La mia raccomandazione: l'energia della CORSA** *(e' quella di cui si controlla la conservazione)*; **la scelta del lato puo' cambiare rispetto alla misura** *(il campo e `cs` entrano nel conto)*.
4. ### **P9 COME SCRITTA NON SI PUO' SODDISFARE:** **la dinamica NON conserva `H` a `1e-12`**: **in C2, senza nascite, l'energia deriva di `-9.9e-06` relativo in `3000` tick** *(`doc/referti_l2/controllo_senza_bordo.txt`)*. ### **La proposta:** **P9 ALLA NASCITA** *(`H` subito prima e subito dopo la nascita e il flip, nello stesso tick: `H(dopo) - H(prima) = DH` contato in `E_persa`, entro `1e-12 |H|`)*; **e sulla corsa `H + E_persa` contro C2-EXT** *(la stessa deriva: la differenza fra le due corse dice cosa fanno le nascite)*.

- **E una quinta, minore** *(una lettura, non una scelta)*: **il lapse del nodo nuovo** *(`cs`)* **si ricalcola dalla legge** *(la carta sez. `2`)*; **la partenza a caldo del punto fisso** *(`lapse_caldo`, solo l'innesco dell'iterazione)* **per il nodo nuovo: la media di `i` e `j`** *(il risultato e' quello del punto fisso, entro `EPS_CS`)*.
- **Gia' fatto e indipendente:** **lo strumento `doc/referti_l2/distanza_passi.py`** *(`1fe8df14`: i tre casi noti PASSANO; **una nascita sposta un nodo su `288` dell'anello `40`**: **la mediana di P-S1 si muovera' solo dopo MOLTE nascite**)*.
- ### **FERMO PER LUCA sui punti `1`-`4`** *(il codice sul ramo e la stima delle due corse vengono dopo)*.
