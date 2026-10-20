# LA MAPPA DELLE DIPENDENZE — **tutto si interseca, ma le intersezioni hanno un VERSO**

> **Regola di lavoro decisa da Luca, 2026-10-13 ore 19:17.**
>
> *«In due giorni energia, tempo proprio, `cs`, vuoto, materia/antimateria e crescita dello
> spazio si sono intrecciati, e il lavoro e' andato su tutti i fronti insieme. Il modello sta
> diventando UNA teoria sola, ed e' giusto che tutto si tocchi. **Ma «tutto si interseca» non
> vuol dire «tutto insieme»: le dipendenze hanno un VERSO.** Intanto il cuore del disegno
> dell'era `2` — «prima lo spazio, poi la materia» — e' rimasto fermo.»*

> ### ⛔ **QUESTO DOCUMENTO SI LEGGE PRIMA DI LAVORARE.** ### **E ogni task history, ogni
> relazione e ogni ripresa cominciano dicendo IL LIVELLO CORRENTE.**

---

## 1. ⭐ I CINQUE LIVELLI — *ognuno serve ai successivi, non viceversa*

### `L1` — **IL TEMPO PROPRIO IN OGNI LEGGE** *(la strada `(B)`)*

| | |
|---|---|
| **le voci** | `[[DECISIONE-STRADA-B-FLUSSI]]` · `[[TEMPO-PROPRIO-LOCALE]]` · `[[DECISIONE-TICK-OROLOGIO-MASSIMO]]` |
| **lo stato** | ### ⛔ **FERMO SU DUE DOMANDE DI LUCA.** La **derivazione e' FATTA** *(`697953a`, `c5deb5e`)*, le registrazioni fatte *(`a2fffbc`, `bbd7fee`)*; ### **manca il CODICE**, e la forma la decidono le due domande |
| **le domande che lo bloccano** | `[[DOMANDA-QUALE-TEMPO-PROPRIO-USA-L-ARCO]]` *(`B-3`)* · `[[DOMANDA-OMEGA-E-UNITA-O-COSTANTE]]` *(`B-4`)* |
| ### ⭐ **il criterio di uscita** | **tre numeri, tutti misurabili:** ① `python primo_ordine/_collauda_tempo_proprio.py` con ### **ZERO violatori** *(oggi **`4` su `7`**, e il collaudo c'e' gia')*; ② **`M-B1` AL BIT** *(ad angolo `pi` il motore nuovo riproduce quello attuale — e' **un'identita' algebrica**, non una tolleranza)*; ③ **`M-B2`**: l'errore su `H_tot` scala come `(omega dtau)^2`, **rapporto `4` a ogni dimezzamento** |
| ### ⚠ **l'ipotesi provvisoria che usa** | ### **`cs` UNIFORME**, cioe' il valore di oggi, **finche' `L2` non e' chiuso.** ### ⛔ **E non e' un dettaglio: `L1` MUOVE `cs` dentro tutte le leggi, ma la sua FORMA e' `L2`** — quindi `L1` si implementa **con `cs` costante**, e il codice **deve avere il posto dove `cs` varia** |

### 📌 **SOTTO `L1`: UNA DOMANDA PER LUCA (`2026-10-20`, `10:27`) -- «IL MODELLO E' L'AUTOMA AL PASSO DI PLANCK, O IL SUO LIMITE CONTINUO?»** *(nessuna decisione; rimandi: `L2` qui sotto, e la variante `(c)` della sez.`26`)*

**Le considerazioni del guardiano, scritte come tali:**
- per la regola di `L1` ### **l'angolo per tick e' `theta = pi * cs * dtau`**;
- ### **a `dtau = 1` e `cs = 1` l'angolo e' `pi`**: e' il passo che riproduce AL BIT il motore vecchio *(`M-B1`)*; ### **a `dtau < 1` si fanno sotto-passi verso il limite continuo**;
- ### **SE IL MODELLO E' L'AUTOMA:** il passo fisico e' `dtau = 1`, ### **l'oscillazione di `H` non e' un errore ma la dinamica dell'automa**, e la grandezza conservata ### **va cercata fra quelle che l'automa conserva ESATTAMENTE a ogni scatto**;
- ### **SE E' IL LIMITE CONTINUO:** `dtau` e' un parametro numerico, ### **e va scelto piccolo quanto basta**;
- ### **finora si e' lavorato nel secondo modo**; ### **la visione di automa di Luca e la variante `(c)` vanno nel primo.**
- ### ⛔ **DA DECIDERE PRIMA DI CHIUDERE `L2`.** *(Il fatto che l'ha sollevata: sulla materia uniforme `H` salta nel termine della moneta, e il salto va come `dtau^2` -- `doc/referti_l2/scala_salto.txt`.)*

### `L2` — **LA MATERIA MODIFICA IL VUOTO, e quindi LA FORMA DI `cs`** — *la «gravita'» del modello*

| | |
|---|---|
| **le voci** | `[[CS-LOCALE-DAL-VUOTO]]` *(punto `3`)* · `[[DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA]]` · `[[DOMANDA-LA-FORMA-DI-CS-CHE-SATURA]]` |
| **lo stato** | ### ⛔ **FERMO SU UNA DOMANDA DI LUCA**, e adesso e' **UNA** *(il verso di `cs` e' stato accorpato)*. La derivazione di `1dcf315` e' fatta; ### **due candidate sono GIA' MISURATE nel `v4`** *(`SCATTER` e `TRASMISSIONE`)* ### ✅ **AGGIORNAMENTO DEL `2026-10-19`** *(la storia qui sopra resta)*: ### **la decisione e' arrivata, e `L2` HA CODICE NEL PASSO** -- `S3` *(`CAMM-MATERIA-VUOTO`, `b4972a78`, `2026-10-16`)*, la forma `cs` *(`6aba7fe6`, `2026-10-17`, e `D1`-`D3`)*, `CAMM-FASE-VUOTO` *(la strada `(d)`, `7aaeb907`, `2026-10-18`)*. ### **Resta aperto il VALORE di `Lambda_c`** *(`[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`, coi numeri di `D4`: `doc/referti_l2/d4_verso_e_profilo.txt`)*. Vedi sez.`4`. |
| **la domanda che lo blocca** | `[[DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA]]` *(`CRITICA`)*; `[[DOMANDA-LA-FORMA-DI-CS-CHE-SATURA]]` e' **sospesa** e `dipende_da` quella |
| ### ⭐ **il criterio di uscita** | ① `Lambda` **non e' piu' invariante** sotto il tick *(oggi: **`8.88e-16`**, cioe' **il vuoto e' PASSIVO**)*; ② l'effetto si vede **FUORI dal grumo** — ### **l'ALONE** *(oggi: **nessun anello oltre `3` sigma**, misurato nel `v4`)*; ③ gli orologi **rallentano INTORNO** al grumo, non solo dentro *(punto `1` dell'`11` ottobre)* |
| **l'ipotesi provvisoria che usa** | ### **nessuna verso l'alto:** `L2` chiede solo `L1`, che e' **sotto** |

### 📌 **RIMANDO** *(`2026-10-20`)*: ### **la domanda «automa al passo di Planck, o limite continuo?» sta sotto `L1`**, qui sopra, ed ### **e' da decidere prima di chiudere `L2`.**

### 📌 **SOTTO `L2`: UN VINCOLO DI `L2` SU `L3`** *(domanda di Luca del `2026-10-19`, `20:02`-`20:06`; ### **non e' lavoro di `L3`**)*

> *«L'instabilita', se c'e', dipende dal fatto che lo spazio non si espande ancora? Sul grafo
> fisso `V` e' conservato e manca il canale di dissipazione globale della crescita (la legge
> generale del 3 ottobre). Non si tratta di fare `L3` prima di `L2`, ma di stimare da `L2` come
> `L3` si deve comportare: tutti i livelli sono collegati, e le misure di un livello diventano
> requisiti per gli altri.»*

**LE CONSIDERAZIONI DEL GUARDIANO, scritte come tali:**
- se `gamma` e' ### **FISICA**, il vincolo che `L2` consegna a `L3` e' ### **UN NUMERO**: la crescita della rete deve avere un tasso ### **almeno dell'ordine di `gamma`** *(in tempo proprio)* alla scala della lunghezza d'onda misurata -- ### **col suo valore e le sue barre**;
- se `gamma` e' ### **NUMERICA**, l'espansione non c'entra, e il difetto e' dello schema di `L2`;
- ### **il vincolo NON chiude `L2` da solo:** `L2` si chiude coi suoi criteri, e il vincolo resta ### **un requisito verificabile per `L3`.** ### **La decisione su come chiudere `L2` e' di Luca.**

### ✅ **L'ESITO DEL TEST** *(`c2dd6453`, `doc/referti_l2/instabilita_vuoto.txt`)*: ### **il vuoto uniforme NON e' instabile** -- `gamma` compatibile con zero in tutti e sette i bracci *(il piu' vicino: rapporto `10`, `+1.0e-04 +- 5.5e-05` per tick, `+1.8` barre)*, `V` conservato, nessun modo dominante. ### **Quindi oggi il vincolo e' VUOTO:** non c'e' un'instabilita' che la crescita di `L3` debba compensare, ### **entro le barre riportate nel referto** *(a rapporto `1`: `-2.0e-05 +- 1.5e-04` per unita' di tempo proprio)*. ### **E lo svuotamento di `D4` a sorgente debole non e' un'instabilita' del vuoto: e' una risposta alla materia, da indagare.**

### `L3` — **LA MITOSI E LO SPAZIO CHE NASCE** — *«prima lo spazio, poi la materia»*

| | |
|---|---|
| **le voci** | `[[SPAZIO-CHE-NASCE]]` · `[[D-BILANCIO-NASCITA]]` · `[[MITOSI-QUANTO-OLONOMIA]]` *(e la domanda del `2026-10-19`: la quantizzazione dal quanto di olonomia, sotto `L4`)* · `[[PRIMA-LO-SPAZIO-POI-LA-MATERIA]]` |
| **lo stato** | ### ⛔ **FERMO, ed e' IL CUORE DEL DISEGNO rimasto indietro.** Le derivazioni di `P5` *(la mitosi)* ci sono; ### **le quattro forme aspettano Luca** |
| ### ⭐ **il criterio di uscita** | ### **LA PRIMA CORSA CON LO SPAZIO CHE CRESCE DA UN SEME**, con ① le **norme conservate attraverso le nascite** *(`CARTA-FISICA-SIMULATORE/F10`)*, ② il **bilancio locale** che chiude attorno all'arco che si divide *(`D-BILANCIO-NASCITA`)*, ③ e **nessun parametro nuovo** |
| ### ⚠ **le ipotesi provvisorie che usa** | ### **`cs` UNIFORME finche' `L2` non e' chiuso** *(altrimenti un nodo nuovo non saprebbe che `cs` ha)*; e ### **`D-BILANCIO-NASCITA` si scrivera' su `H_tot` di `(B)`**, quindi **aspetta `L1`** |

### `L4` — **LA `U` DINAMICA** — *la via del campo per legare la materia*

| | |
|---|---|
| **le voci** | `[[U-ARCO-DINAMICA]]` · `[[DOMANDA-U-DINAMICA-LE-FORME]]` |
| **lo stato** | ### **derivazione FATTA** *(`60f869c`)*; **quattro forme a Luca** |
| ### ⭐ **il criterio di uscita** | la `U` **evolve** e la sua **olonomia su un ciclo** e' misurabile e **invariante di gauge** |
| ### ⚠ **l'ipotesi provvisoria che usa** | ### **la REGOLA DI CONNESSIONE di `L3`:** la nota del `2026-10-13` dice che **se il nato chiude triangoli coi vicini comuni dei genitori**, allora i cicli piu' corti sono **triangoli**, cioe' **plaquette locali** — e la **localita' del termine magnetico dipende da questo.** ### **Quindi `L4` aspetta `L3`** |
| ### ⭐ **la domanda che SI DECIDE QUI** *(`2026-10-16`)* | `[[DOMANDA-LA-GERARCHIA-GRAVITA-EM]]`: ### **prima di `L4` il campo di gauge `U` e' FERMO** *(`U = I`)*, quindi l'accoppiamento elettromagnetico ### **non esiste nel modello** e il rapporto con la gravita' ### **non e' calcolabile.** ### **Resta collegata alla scelta di `Lambda_c`, che sta in `L2`** *(`[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`)* |

### 📌 **SOTTO `L4`: UNA DOMANDA DI LUCA DEL `2026-10-19` (`12:03`-`12:05`) -- IL QUANTO DI OLONOMIA E LA QUANTIZZAZIONE** *(con le considerazioni del guardiano, scritte come tali; ### **nessuna conclusione: e' una domanda con i suoi criteri**)*

"DOMANDA: la quantizzazione puo' emergere dal QUANTO DI OLONOMIA (2 pi su un ciclo, gia' deciso per la mitosi) quando U sara' dinamica?
(i) QUANTIZZAZIONE TOPOLOGICA (attesa per costruzione, da verificare in L4): l'olonomia si misura modulo 2 pi, quindi il numero di giri e' un intero. Ne seguirebbero flussi e cariche quantizzati, come in Dirac, Aharonov-Bohm e nel quanto di flusso dei superconduttori, anche in un campo classico se psi e' a un solo valore.
(ii) QUANTI DI RADIAZIONE (ipotesi): h = 2 pi hbar, cioe' un giro completo di fase e' un quanto d'azione. Se gli scambi di U avvenissero a giri interi, ogni scambio porterebbe un'azione h, e un processo a frequenza nu scambierebbe energia a pacchetti h*nu. NON segue da solo; restano da verificare: l'indivisibilita' (il quanto si rivela intero in un punto), una costante unica per tutte le frequenze, e le statistiche (solo in L6, con lo stato quantistico).
(iii) TENSIONE DA DECIDERE (Luca): oggi il quanto 2 pi fa scattare la mitosi. Se fosse anche il quanto della radiazione, o le due cose sono distinte e serve una regola che dica quando un giro diventa nodo e quando radiazione, oppure sono la stessa cosa: ogni quanto d'azione completato crea spazio ('prima lo spazio, poi la materia'). Nessuna delle due e' scelta.
Legame con la variante (c) della sez.26: gli scambi a scatti sugli archi sono il posto dove questi quanti viaggerebbero."

### ⛔ **Nessuna delle due strade di `(iii)` e' scelta: la decisione e' di Luca.** *(Rimandi: la voce `MITOSI-QUANTO-OLONOMIA` in `L3`, e `L6`.)*

### `L5` — **I DOMINI DI MATERIA/ANTIMATERIA** — *la strada `(3)`*

| | |
|---|---|
| **le voci** | `[[IPOTESI-DOMINI-SEPARATI]]` · `[[DECISIONE-DIREZIONE-STRADA-3]]` · `[[DOMANDA-BANDE-O-SEGNO-LOCALE]]` *(chiusa)* e le **quattro forme** di `(P-b)` |
| **lo stato** | ### ⚠ **MOLTO LAVORO SU CARTA FATTO, E L'IMPLEMENTAZIONE SI FERMA.** `(P-a)`, `(P-b)`, `(R1)`, `(R2)`, il piano `(D1)`–`(D4)`, il parametro d'ordine **deciso**; e lo strumento `primo_ordine/segno.py` **esiste ed e' validato** |
| ### ⭐ **il criterio di uscita** | ### **`(D3)`/`(D4)` col termine ACCESO contro SPENTO**, e la **lunghezza di correlazione** dei domini che **cresce** *(coarsening)* con un esponente **`> 0`** dichiarato col suo errore |
| ### ⛔ **l'ipotesi provvisoria che usa** | ### **HA BISOGNO DELLA CRESCITA DI `L3`**: `(R2)` dice che un sistema chiuso **non si ordina** senza raffreddamento, e il raffreddamento **e' la crescita dello spazio.** ### **Quindi `L5` non si puo' MISURARE prima di `L3`** |

#### `L5` — ⭐ **SECONDA CANDIDATA: L'ASIMMETRIA NELLA LEGGE** *(strada `A`, alla
Sakharov)*, **accanto ai domini** *(strada `B`, decisa il `2026-10-13`)*

> ### ⛔ **COLLOCATA, NON OPERATIVA** *(decisione di Luca, `2026-10-15` alle `15:25`)*.
> ### **Non si apre prima di `L5`**, e `L5` non si apre prima di `L1`-`L4`.
> ### **La voce e' `[[L5-ASIMMETRIA-NELLA-LEGGE]]`.**

### **LE TRE CONDIZIONI DI SAKHAROV** *(1967)* per avere **piu' materia che antimateria**:

| | la condizione |
|---|---|
| `1` | **un processo che CAMBI il bilancio** materia/antimateria |
| `2` | **leggi che DISTINGUANO** materia e antimateria — *rottura di `C` e di `CP`* |
| `3` | **uscita dall'EQUILIBRIO** |

### ⭐ **I CANDIDATI NEL MODELLO, uno per condizione**

| | il candidato | dove sta oggi |
|---|---|---|
| `1` | **la saturazione che MESCOLA le bande**, e **la carica che non si conserva localmente** | ### ⚠ **oggi e' UNA DELLE DUE TENSIONI col disegno** *(par. `3.2`, punto `(ii)`: la saturazione mescola `N+` e `N-` localmente, `corr = -1.0000`)*. ### **Qui non e' una tensione: e' UN INGREDIENTE** |
| `2` | **lo spettro del passo NON APPAIATO `eps <-> -eps`** | ### **trovato in `L1` il `2026-10-15`** *(`8bf0ded` e la misura della terza parte, `5219e1b`)*: col tempo proprio nelle leggi, ### **la legge stessa tratta materia e antimateria in modo diverso** |
| `3` | **la CRESCITA DELLO SPAZIO** *(mitosi)*, la freccia fondamentale ammessa | ### **e' il congelamento per diluizione, GIA' nel piano di `L5`** — e `(R2)` dice che senza raffreddamento un sistema chiuso **non si ordina** |

### ⚠⚠ **E SUL CANDIDATO `2` DEVO METTERE I NUMERI ESATTI, perche' la frase <<non appaiato
a `dtau < 1`>> e' piu' grossolana di cio' che la misura dice:**

| `dtau` | appaiamento *(collo di bottiglia)* | il CASO *(minimo su `20` tiri)* | la lettura |
|---|---|---|---|
| `1` | **`0.0820`** | `0.248` | ### ⚠ **NON appaiato** *(l'esatto e' `~1e-15`)*, **ma `3` volte sotto il caso**: c'e' struttura |
| `0.5` | `1.379` | `0.280` | **NON appaiato**, e **sopra** il caso |
| `0.25` | `1.776` | `1.486` | **NON appaiato** |

### ⛔ **Quindi l'asimmetria c'e' anche a `dtau = 1`**, non solo sotto; ### **e a `dtau = 1`
e' PICCOLA ma non nulla.** ### ⭐ **E senza la moneta di spin l'appaiamento a `dtau = 1`
torna ESATTO** *(`4.133e-15`)*: ### **cioe' il candidato `2` e', piu' precisamente, LA
MONETA DI SPIN.**

### ⭐⭐ **LE DUE PREVISIONI, E SONO DIVERSE — ed e' questo che le rende due strade e non
due parole**

| | la strada | la previsione |
|---|---|---|
| `A` | **l'asimmetria nella legge** | ### **un eccesso dello STESSO SEGNO OVUNQUE** |
| `B` | **i domini** *(decisa il `2026-10-13`)* | ### **domini con PARETI e carica totale ZERO** — e **domini piu' grandi dell'universo osservabile**, perche' dalle pareti non arrivano raggi gamma di annichilazione |

### ⛔ **CHE COSA NON E' ANCORA STABILITO, e va MISURATO quando `L5` si apre**

| | la domanda aperta |
|---|---|
| `1` | **l'asimmetria della legge rompe anche `CP`?** *(oggi si sa che rompe `C`, nel senso che `C W C^-1 != W`)* |
| `2` | **ha un SEGNO preferito?** ### ⚠ **Senza un segno preferito, l'asimmetria c'e' e non produce un eccesso** |
| `3` | **sopravvive quando il tempo proprio VARIA DAVVERO** *(dopo `L2`)*? ### **Oggi `cs` e' UNIFORME**, quindi l'asimmetria misurata nasce dal `dtau` **come angolo**, non da una sua variazione |
| `4` | ### ⭐⭐ **come la cambia la scelta <<`n` = DIREZIONI DI MOTO>>?** E qui c'e' un fatto **misurato nella terza parte di `L1`, e va letto come un AVVERTIMENTO a questa idea:** con `n` **GEOMETRICI** e `U = I` esiste una simmetria antiunitaria **ESATTA** del passo *(`(P Theta)`, scarto `5.5e-16`)*, **con Kramers** *(molteplicita' `2`)*. ### ⛔ **Cioe' quella scelta POTREBBE RESTITUIRE la simmetria, e togliere il candidato `2`.** ### **Non e' detto che lo faccia** *(la' `U = I`, e il gauge rompe la mappa: `1.218` con `U` casuale)*, **ma e' la prima cosa da misurare.** |

### 📌 **E UNA COSA CHE QUESTA COLLOCAZIONE RENDE VISIBILE, e che prima non si vedeva:**
### **le due strade NON sono alternative esclusive per costruzione** — la `1` e la `3` sono
**ingredienti comuni**, e cio' che le separa e' ### **la condizione `2`.** ### **Quindi
quando `L5` si apre, la prima misura utile e' sulla `2`**, non sulle altre due.


---

## 2. LE REGOLE OPERATIVE

| | la regola |
|---|---|
| **`(a)`** | ### **OGNI idea, mandato o domanda nuova SI COLLOCA nella mappa PRIMA di lavorarci:** a quale livello appartiene, da cosa dipende, cosa sblocca. ### ⚠ **Se non si colloca, si dice PERCHE' e si chiede a Luca** |
| **`(b)`** | ### ⛔ **IL CODICE E LE MISURE si fanno sul livello PIU' BASSO NON CHIUSO.** I livelli superiori si possono **derivare su carta**, ### **ma non si implementano e non si DECIDONO** finche' quelli sotto non hanno il loro criterio di uscita. ### **ECCEZIONE: solo se Luca lo dice esplicitamente, e la mappa lo registra** |
| **`(c)`** | ### **LE IPOTESI PROVVISORIE SONO DICHIARATE:** un livello che ha bisogno di qualcosa di un livello **superiore** usa un'ipotesi **scritta** *(per esempio «`L3` con `cs` uniforme finche' `L2` non e' chiuso»)*. ### **Ogni ipotesi ha una riga in questa mappa e un rimando nel task history che la usa, e quando il livello superiore si chiude SI RIVEDE** |
| **`(d)`** | ### **OGNI TASK HISTORY dichiara IN TESTA la sua CASELLA** *(livello)* **e le sue ipotesi provvisorie.** ### ⚠ **Un presidio lo verifica, col suo caso che DEVE fallire** *(un task history senza casella)* |
| **`(e)`** | ### **`doc/indice/DA_DECIDERE_LUCA.md` SI ORDINA PER LIVELLO:** prima le domande del **livello piu' basso aperto**. ### **E si portano a Luca in quell'ordine, UNA ALLA VOLTA** |
| **`(f)`** | ### **RIPRESA E VERIFICA PARTONO DA QUI:** `doc/RIPRESA_*.md` e ogni relazione cominciano con ### **«livello corrente: `Lx`, stato, prossimo passo»** |

---

## 3. ⭐ LA COLLOCAZIONE DI CIO' CHE E' IN CORSO — *primo uso della regola*

| il pezzo | il livello | lo stato |
|---|---|---|
| `B-3` **la media armonica sull'arco** | ### **`L1`** | ### ⛔ **domanda per Luca, E' LA PRIMA** |
| `B-4` **`omega` dal raccordo** | ### **`L1`** | ### ⛔ **domanda per Luca, la SECONDA** |
| la **regola materia → vuoto**, il **verso di `cs`**, `(C-A)`/`(C-B)` | ### **`L2`** | ⛔ **una domanda sola** *(accorpate)* |
| le **`4` forme della mitosi**, il **vuoto alla nascita**, il **seme minimo** | ### **`L3`** | ⛔ fermo |
| le **`4` forme della `U` dinamica**, il **segno della sorgente** | ### **`L4`** | ⛔ fermo |
| `(P-a)`, `(P-b)` e le loro **`4` forme**, `(D1)`–`(D4)`, l'**ipotesi dei domini** | ### **`L5`** | ### ⚠ **il lavoro su carta RESTA VALIDO: si ferma l'IMPLEMENTAZIONE** |

### `3.1` ⛔ UNA COSA DA DICHIARARE SU ME STESSO, e la regola e' nuova ma il fatto e' di ieri

### ⛔ **HO IMPLEMENTATO UNO STRUMENTO DI `L5` MENTRE `L1` E' APERTO:**
`primo_ordine/segno.py` *(il punto `(D1)`, commit `0ab42bb`)*, e anche `bande.py`,
`bande_floquet.py`, `deriva.py`. ### **Secondo la regola `(b)` non avrei dovuto**, e lo dico
invece di lasciarlo scoprire.

### ⚠ **CHE COSA NE FACCIO, e non lo decido da solo:** quegli strumenti sono **misure**, non
**fisica** — non toccano la tabella e non promuovono niente. ### ✅ **Li tengo**, perche'
hanno **validato `q_h`** che e' poi stato **deciso**; ### ⛔ **ma il loro USO su `L5` aspetta
`L3`**, e questa riga e' la loro **ipotesi provvisoria registrata**.

### `3.2` ⛔⛔ LE DUE TENSIONI COL DISEGNO — *punti aperti, da dire a Luca quando si arriva a `L5`*

| | la tensione | perche' e' una tensione |
|---|---|---|
| `(i)` | ### **il termine di ordinamento e' UNA LEGGE IN PIU'** | `CARTA-FISICA-SIMULATORE/F1` dice **UNA SOLA REGOLA**, e `9-ter` che una cura **non aumenta il numero delle leggi.** ### ⛔ **Se `(D3)`/`(D4)` NON mostrasse un effetto netto, VA TOLTO** — e questo e' **il suo criterio di abbandono, scritto prima** |
| `(ii)` | ### **LA CARICA** | la decisione del `2026-10-03` la voleva conservata **anche localmente**; ### ⛔ **oggi la saturazione la MESCOLA localmente** *(misurato: `corr(Delta N+, Delta N-) = -1.0000`, cioe' coppie esatte)*, e la strada `(3)` la salva ### **solo GLOBALMENTE.** ### ⚠ **Va detto a Luca in modo ESPLICITO quando si arriva a `L5`** |

---

## 4. ⭐ IL LIVELLO CORRENTE

> ### ⭐⭐ **`L2` — LA MATERIA MODIFICA IL VUOTO, e quindi `cs`** *(dal `2026-10-15`)*.
> ### ⛔ **Stato: FERMO SU UNA DECISIONE DI FISICA DI LUCA** —
> `[[DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA]]`: ### **con che REGOLA, e con che SEGNO, la
> materia modifica la densita' del vuoto `Lambda`.**
> ### 📌 **Luca la sta decidendo col guardiano**, e finche' non c'e' ### **nessun codice di
> `L2` si scrive**: la regola `(b)` vale anche qui.
> ### ⭐ **Prossimo passo, quando la decisione arriva:** il **costruttore della scena di
> riferimento** *(`n` GEOMETRICI, `U = I`)*, che e' **il primo pezzo di `L2`** — e la scena
> oggi ### **non esiste in nessun file.**
>
> ### ✅ **AGGIORNAMENTO DEL `2026-10-19`** *(la storia qui sopra resta)*: ### **la decisione e' arrivata, e `L2` HA CODICE NEL PASSO** -- `S3` *(`CAMM-MATERIA-VUOTO`, `b4972a78`, `2026-10-16`)*, la forma `cs` *(`6aba7fe6`, `2026-10-17`, e `D1`-`D3`)*, `CAMM-FASE-VUOTO` *(la strada `(d)`, `7aaeb907`, `2026-10-18`)*. ### **Resta aperto il VALORE di `Lambda_c`** *(`[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`, coi numeri di `D4`: `doc/referti_l2/d4_verso_e_profilo.txt`)*.
> ### ⚠ **Quindi le due righe qui sopra (<<FERMO>>, <<nessun codice di `L2` si scrive>>) sono STORIA**: valevano fino al `2026-10-15`.

### ✅✅ **E `L1` E' CHIUSO** *(il `2026-10-15`)*, col criterio di merito **misurato**:
### **`0` violatori su `12`** *(e il collaudo e' **nel `.githooks/pre-commit`**, con la
prova su un commit vero in `f46d854`)*; ### **`M-B1` pezzo per pezzo al bit, `12`/`12`**;
### **`M-B2` pendenza `2.006`** *(controprova dell'ordine vecchio: `1.183`)*.
### 📌 **Il lascito di `L1` — cio' che lascia aperto e DOVE VA — sta nel paragrafo `12`.**

### ⚠ **E IL CRITERIO DI USCITA DI `L1` RESTA UN COMANDO, non un ricordo:**
`python primo_ordine/_collauda_tempo_proprio.py` ### **oggi dice `0` su `12`, e se un
giorno tornasse a dire `1` FERMEREBBE UN COMMIT.** ### **Un criterio chiuso che resta
eseguibile e' la differenza fra un livello chiuso e un livello dimenticato.**

---

## 5. ⛔ GLI STRUMENTI DI `L5`, **CONGELATI** *(decisione di Luca, 2026-10-15)*

> *«Gli strumenti di `L5` che hai dichiarato in `784976d` restano **CONGELATI**: nessun
> codice e nessuna misura finche' `L1`–`L4` non sono chiusi.»*

| il file | che cosa fa | perche' e' `L5` |
|---|---|---|
| `primo_ordine/segno.py` | lo **squilibrio locale `q`**, e la sua validazione contro `Q` | e' **il parametro d'ordine** della strada `(3)` |
| `primo_ordine/bande.py` | le **due bande spettrali** di `W`, il controllo `C`, le grandezze per banda | e' **materia/antimateria** |
| `primo_ordine/bande_floquet.py` | il **riscaldamento di Floquet** sulla scena grande | misura la **termalizzazione delle bande** |
| `primo_ordine/deriva.py` *(+ `deriva_referto.py`)* | la **deriva di `E`**, la scansione in `x`, la **sorgente per nodo** | dichiarato con gli altri in `784976d` |

### ⛔ **NESSUNO DI QUESTI SI TOCCA E NESSUNO GIRA** per produrre misure nuove, finche'
`L1`–`L4` non sono chiusi. ### ⚠ **I loro COLLAUDI restano nel `pre-commit`**
*(`_collauda_corrente.py`, `_collauda_deriva.py`)*: ### **girano per NON LASCIARLI
IMPUTRIDIRE, non per misurare** — e se un collaudo cominciasse a fallire, ### **quello e'
un fatto da riportare, non un lavoro da riprendere.**

### ⚠ **E UNA DOMANDA DI PERIMETRO CHE NON DECIDO IO, e la segnalo invece di risolverla a
mio favore:** `deriva.py` contiene la macchina che serve a **`M-B2`**, che e' **un criterio
di uscita di `L1`** — la scansione in `x`, le escursioni relative, il rapporto fra
dimezzamenti. ### ⛔ **Il congelamento di `L5` BLOCCA anche il riuso di quella macchina per
una misura di `L1`?** ### ✅ **Finche' non c'e' una risposta la tratto come BLOCCATA**, e
quando `M-B2` servira' lo chiedo: ### **riscrivere la stessa macchina altrove per aggirare
il congelamento sarebbe aggirarlo, non rispettarlo.**

### 📌 **E DUE FILE CHE NON SONO NELL'ELENCO, e dico perche':** `corrente.py` e il suo
collaudo costruiscono **la corrente locale dell'energia**, che serve a `H_tot` di `(B)` —
### **cioe' sono `L1`/`L2`, non `L5`.** ### ⚠ **Non li aggiungo ai congelati e non li uso:
li classifico, e la classificazione e' una mia lettura.**

---

## 6. ⭐ IDEE COLLOCATE, **NON OPERATIVE**

> ### ⛔ **Qui stanno le idee che hanno gia' una CASELLA e NON si lavorano:** la regola
> `(a)` dice che ogni idea si colloca **prima** di lavorarci, e ### **collocare non e'
> cominciare.**

### `6.1` **`MISURA-DOPPIONI`** — *dopo `L1`*

| | |
|---|---|
| **la casella** | ### **dopo `L1`** — si apre **solo quando `L1` e' chiuso** |
| **che cosa e'** | calcolare la **relazione di dispersione** del passo della camminata **sul toro** *(senza bordi)* e **contare i minimi** della curva: ### **uno o due coni?** |
| **la domanda** | ### **la camminata ha <<DOPPIONI>>?** *(Nielsen–Ninomiya)* |
| **perche' non e' un effetto dei bordi** | si misura **sul toro**, che **non ha bordi**: ### **sono una proprieta' del RETICOLO ALL'INTERNO** |
| **perche' dopo `L1`** | la dispersione e' quella di `W`, e ### **in `(B)` `W` CAMBIA** *(`hop(theta)` e `Grover(theta)` invece delle involuzioni)*: ### ⛔ **misurarla adesso darebbe la dispersione di un passo che sta per essere sostituito** |
| ### ⚠ **che cosa NON faccio** | nessun codice, nessuna misura. ### **E non la registro nemmeno come voce dell'indice**, perche' il mandato dice *«solo collocazione»* — ### **quando si apre, la voce e' il primo passo** |

### `6.2` **`L6` — IL TEMA QUANTISTICO** — *dopo `L1`–`L5`, decisione di Luca del 14 ottobre*

| | |
|---|---|
| **la casella** | ### **`L6`, dopo `L1`–`L5`** |
| **che cosa e'** | la **seconda quantizzazione di `psi`** — un **automa cellulare quantistico** — ### **con la STESSA tabella delle leggi** |
| ### ⭐ **il legame col simulatore di oggi** | il simulatore attuale ne sarebbe ### **IL CAMPO MEDIO** |
| **i quanti** | **spinoriali FERMIONICI** |
| ### ⭐ **i bosoni** | **figure d'interferenza** *(la materia)*, ### **NON coppie** |
| **il primo passo** | a **grafo FISSO** |
| ### ⭐ **il controllo di raccordo** | con **`1` quanto** deve dare ### **AL BIT** lo stesso risultato di `primo_ordine/motore.py` |
| **lo stato** | ### ⛔ **SOLO TEORIA fino all'apertura di `L6`** |
| ### 📌 **la domanda dal quanto di olonomia** *(`2026-10-19`)* | sotto `L4`: la quantizzazione **topologica** *(attesa per costruzione)*, i **quanti di radiazione** come ipotesi -- e ### **le statistiche, che solo `L6` puo' dire** |

### ⚠ **E NOTO UNA COSA SUL CONTROLLO DI RACCORDO, perche' e' la sua forza:** *«con `1`
quanto, AL BIT come `motore.py`»* e' ### **un criterio che non si puo' addolcire** — come
`M-B1` per `(B)`. ### **E ha una conseguenza sull'ordine:** il raccordo e' con `motore.py`,
che in `(B)` **cambia** ⟹ ### **`L6` aspetta `L1` non per comodita', ma perche' il suo
criterio di raccordo PUNTA a un oggetto che sta per cambiare.**

### ⛔ **E CHE COSA NON FACCIO:** nessuna derivazione, nessun task history, nessuna voce.
### **La collocazione e' questa riga, e basta.**

### 📌 **SOTTO `L6`: UN'IDEA COLLOCATA DI LUCA DEL `2026-10-20` (`09:19`-`09:23`) -- LA QUANTIZZAZIONE COME TAGLIO ULTRAVIOLETTO** *(discussa col guardiano; le considerazioni del guardiano sono scritte come tali. ### **Nessun codice, nessuna decisione.** Rimandi: la sez.`27`, l'osservazione sull'era `1`, e la sez.`24`, il solitone a due lunghezze di Planck)*

> *«LA QUANTIZZAZIONE COME TAGLIO ULTRAVIOLETTO: il modo a scala di griglia (la scacchiera
> a `k = pi`, il doppione) potrebbe essere spento dalla quantizzazione, come Planck spense
> la catastrofe ultravioletta nel 1900.»*

**Le considerazioni del guardiano, scritte come tali:**
1. ### **IL MECCANISMO DI PLANCK:** un modo di frequenza `nu` si eccita solo a pacchetti di energia `h nu`; ### **i modi troppo cari restano spenti** perche' non si possono riempire a frazioni. ### **Nel modello il modo a `k = pi` ha l'energia d'arco MASSIMA per una data densita':** sarebbe il piu' caro.
2. ### **DUE IDEE GIA' REGISTRATE nella stessa direzione:**
   - **il quanto d'azione**: un giro di fase per scambio, ### **la domanda sotto `L4` sul quanto di olonomia** *(`E = h nu`)*;
   - **il tetto di Pauli di `L6`**: al massimo `2d` quanti per nodo, che ### **LIMITEREBBE** l'ammucchiarsi della materia a scacchiera, ### **senza impedirlo.**
3. ### **LE DUE CONDIZIONI:**
   - **(a)** ### **serve lo stato quantistico vero di `L6`.** Il simulatore di oggi ha ampiezze continue, quindi ### **anche frazioni di quanto entrano nella scacchiera**, come nel caso classico;
   - **(b)** ### **prima va escluso un difetto del passo** *(`C1` e `C2`, task history `2026-10-20_controllo_passo_materia_uniforme.md`)*: se il passo non conserva `H` sulla materia uniforme, l'instabilita' ### **e' un errore da correggere, e la quantizzazione non va invocata.**
4. ### **IL RISCHIO DI METODO:** *«la quantizzazione lo sistemera' in `L6`»* ### **NON chiude `L2`.**
   - Il simulatore di oggi ### **e' il CAMPO MEDIO**: dove i quanti per modo sono molti, i due devono coincidere;
   - ### **quindi la quantizzazione salverebbe solo dove i quanti per modo sono MENO DI UNO.**
5. ### **IL CRITERIO, quando `L6` si aprira'** *(fissato qui)*:
   - sul **controllo di raccordo gia' previsto** *(grafo piccolo, campo medio contro stato quantistico)*, ### **il modo a `k = pi` si spegne nello stato quantistico e NON nel campo medio, a parita' di energia e di norma**;
   - ### **se si accende in entrambi, l'idea cade.**

---

## 7. ✅ `L1` — **LE DUE DECISIONI DI LUCA DEL `2026-10-15`**

### `B-3` — **IL TEMPO PROPRIO DELL'ARCO E' LA MEDIA ARMONICA**

> ### ⭐ **`dtau_arco = 2 · dtau_i · dtau_j / (dtau_i + dtau_j)`**

**Il motivo:** e' **la somma dei tempi di attraversamento delle due meta' dell'arco**,
ciascuna alla velocita' del proprio nodo.
### ⚠ **E L'IPOTESI RESTA DICHIARATA, registrata CON la decisione: <<DUE META' UGUALI>>.**
### **E' un MODELLO della geometria dell'arco, non un fatto** — se il tempo proprio
cambiasse lungo l'arco in un altro modo, **il conto cambierebbe.**

### `B-4` — **`omega` DAL RACCORDO, E UN SOLO `omega`**

> ### ⭐ **`omega · dtau_rif = pi`**, con **`dtau_rif` = il tempo proprio dell'orologio
> PIU' VELOCE** *(`cs` al massimo)*. ### **UN SOLO `omega`** per lo spostamento **e** per
> il Grover.

### ✅ **Quindi `omega` NON e' una costante tarata: e' una CONDIZIONE DI RACCORDO** — al
passo di riferimento il motore nuovo **riproduce quello di oggi**. E siccome compaiono
**solo i prodotti `omega · dtau`**, un fattore comune **si assorbe**: ### **e' una SCELTA
DI UNITA'**, e `CARTA-FISICA-SIMULATORE/F10` e' rispettato.

### ⚠ **E IL PUNTO DEBOLE RESTA DICHIARATO, registrato CON la decisione:** l'uguaglianza
dei due `omega` e' ### **UN FATTO STORICO DEL MOTORE, NON UN PRINCIPIO.** Oggi sono
entrambi involuzioni *(entrambi all'angolo `pi`)*, e tenerli uguali **non aggiunge niente**;
### **ma nessun argomento dice che debbano esserlo**, e separarli aggiungerebbe **un numero
puro** da derivare.

### ⭐⭐ **E UNA CONSEGUENZA OPERATIVA, che e' cio' che rende `theta <= pi` vero PER
COSTRUZIONE:** posto **`s = dtau / dtau_rif`** con `dtau_rif` ### **IL MASSIMO** dei
`dtau`, si ha **`s <= 1` SEMPRE**, quindi `theta = pi·s <= pi`.
### ✅ **NESSUN TETTO E NESSUN CLIP** *(`A11`)*: ### **il limite viene dalla DEFINIZIONE di
`dtau_rif`.**

### ⭐ **E UNA PRECISAZIONE SU `B-3`:** siccome `dtau_k = cs_k · dt`, la media armonica dei
`dtau` **equivale** a quella dei `cs` — ### **`cs_arco` = media armonica di `cs_i` e
`cs_j`** — perche' ### **il `dt` globale si cancella nel rapporto.** ### ✅ **Quindi la
decisione si legge sui tempi propri o sulle velocita', e sono LA STESSA COSA:** e' ### **indipendente
da come si misura il tick.**

---

## 8. ✅ IL **PERIMETRO DEL CONGELAMENTO** — *scelta di Luca, `2026-10-15`*

> ### ⭐ **E' LA RISPOSTA ALLA DOMANDA CHE AVEVO FATTO IN `717bb60`**, e la riporto perche'
> era mia: *«il congelamento di `L5` blocca anche il riuso di `deriva.py` per una misura di
> `L1`?»*

| | la regola | |
|---|---|---|
| ✅ **ammesso** | `primo_ordine/deriva.py` **IN SOLA LETTURA** per i criteri di uscita di `L1` — **`M-B2`** e **`_collauda_tempo_proprio.py`**, che ### **lo importa gia'** |
| ⛔ **vietato** | ### **nessuna misura NUOVA di `L5`**, e ### **nessuna modifica alle sue parti di `L5`** *(la **sorgente per nodo**)* |
| ⚠ **e se una parte che serve a `L1` va toccata** | ### **si dichiara UNA PER UNA nel commit** |

### ⚠ **E NOTO CHE LA DOMANDA ERA GIUSTA A MONTE, non solo utile:** `_collauda_tempo_proprio.py`
### **importa gia' `deriva.py`** *(per `DV.scena` e `DV.OPERATORE`)*, quindi
### **il congelamento preso alla lettera avrebbe bloccato il criterio di uscita di `L1`**
— cioe' ### **si sarebbe bloccato da solo.**

---

## 9. ⚠ `L1` — **IL CODICE E' FATTO, E IL LIVELLO NON E' CHIUSO** *(`2026-10-15`)*

> ### ⛔ **`L1` RESTA IL LIVELLO CORRENTE**, e non per lavoro mancante: ### **per due
> criteri di uscita che non passano, e che chiedono una decisione di fisica.**

| | il criterio di uscita | esito |
|---|---|---|
| `1` | `_collauda_tempo_proprio.py`: `0` violatori su `7` | ### ✅ **PASSA**, e il presidio **impedisce** *(dimostrato)* |
| `2` | `M-B1`: identita' AL BIT con `717bb60` | ### ✅ **PASSA** *(`eff92bbd8622`, `250` tick, `psi` e `phi`)* |
| `3` | `M-B2`: fattore `4` a ogni dimezzamento | ### ⛔ **NO: `2.540`, `2.204`, `2.111`** — e la causa e' misurata: **la composizione non e' simmetrica** |
| `4` | la `C`-simmetria resta verde | ### ⛔ **NO: da `0.000e+00` a `5.343`** — e la causa e' derivata: **`G^* = G(-theta)`** |

### ⛔ **LE DUE DECISIONI CHE SERVONO A LUCA, e non le prendo io:**
### ① **`[[DECISIONE-COMPOSIZIONE-SIMMETRICA]]`** — l'`ordine` palindromo darebbe
`O(dtau^2)` *(misurato: `5.342`, `3.691`, `4.291`)*, ma ### **cambia IL PASSO**, e
### ⚠ **`M-B1` e `M-B2` cosi' come sono scritti non possono valere insieme.**
### ② **`[[DECISIONE-LA-C-VUOLE-IL-TEMPO-ROVESCIATO]]`** — la simmetria che sopravvive e'
una **`CT`**, non una `C`.

### 📌 **E DUE COSTI REGISTRATI:** `[[COSTO-MEMORIA-DEI-FLUSSI-PARZIALI]]`
*(`4.39x` -> `5.56x`, soglia `5x`)* e
`[[DIFETTO-LAMBDA-NON-PIU-INVARIANTE-SOTTO-IL-VUOTO]]`.

### ⭐ **E CIO' CHE `L1` HA GIA' CONSEGNATO A `L2`, qualunque sia la decisione:**
### **il PUNTO UNICO di lettura del tempo proprio** *(`flussi_parziali.dtau_nodo`)* —
### **nessuna legge calcola il suo `dtau` da se'**, e quello e' il posto da cui `L2` fara'
variare `cs`.

---

## 10. ✅ `L1` — **IL PALINDROMO E' IN TABELLA** *(`2026-10-15`, sera)*

### ✅ **`[[DECISIONE-COMPOSIZIONE-SIMMETRICA]]` E' CHIUSA**: l'ordine e' palindromo,
`12` pezzi, impronta `871a7b37dab75b06` → **`f1fca71b952bb8c8`**, e l'errore di `H_tot`
passa da **primo** a **secondo** ordine *(pendenza `1.183` → `2.006`)*.

### ⚠ **E RESTA APERTA UNA SOLA DECISIONE, piu' precisa di prima:**
`[[DECISIONE-LA-C-VUOLE-IL-TEMPO-ROVESCIATO]]` — ### **non <<la `C` o la `CT`?>> ma
<<la MONETA DI SPIN deve rovesciarsi sotto la `C`?>>**, perche' ### **senza la moneta
l'inversione del tempo del passo e' ESATTA** *(`3.9e-16`)* e **Kramers c'e'**.

### 📌 **E cio' che `L1` ha consegnato a `L2` resta quello:** ### **il punto UNICO di
lettura del tempo proprio.** Adesso con, in piu', ### **un passo reversibile per
costruzione** — che e' cio' che rende sensato chiedersi, a `L2`, **da dove venga
l'irreversibilita'** *(`A15.3`)*.

---

## 11. ⭐⭐ `L1` — **UNA SIMMETRIA ANTIUNITARIA ESATTA, CON GLI `n` GEOMETRICI**
*(`2026-10-15`, terza parte)*

### ✅ **MISURATO:** `Theta W[n] Theta^-1 = W[-n]^-1` **all'ulp** *(`2`-`3` ulp, `n`
casuali)*; e con `n` **GEOMETRICI** e `U = I` l'inversione spaziale del toro da'
`P W[n] P^-1 = W[-n]` *(`0.000e+00`)*, quindi
### **`(P Theta) W (P Theta)^-1 = W^-1`** *(`5.5e-16`)* ### **con Kramers**
*(molteplicita' `2`)*.

### ⛔ **E il limite e' derivato, non trovato dopo:** l'inversione **rovescia l'arco**, e
la' **`U` va in `U^dagger`** — con `U` casuale la simmetria **non puo'** esistere, e la
misura lo conferma *(`1.218`)*.

### ⚠ **E questo cambia la forma della decisione aperta**
`[[DECISIONE-LA-C-VUOLE-IL-TEMPO-ROVESCIATO]]`: non piu' solo *«la moneta deve
rovesciarsi?»*, ma anche ### **«gli `n` del modello devono essere le DIREZIONI DI MOTO?»**
— e quella e' una domanda che ### **tocca `L2` e `L4`**, perche' gli `n` vivono sulle
estremita' e il gauge sugli archi.

### 📌 **E una cosa che il censimento ha trovato, e che va detta qui perche' riguarda tutti
i livelli:** ### **nessuna scena del motore costruisce `n` GEOMETRICI** — sono casuali in
`8` file e `z` uniforme in `3`. ### **Quindi la scena <<naturale>> del modello, oggi, non
esiste.**

---

## 12. ✅✅ `L1` **E' CHIUSO** — *e `L2` e' il livello corrente* *(`2026-10-15`)*

> ### ⭐ **IL CRITERIO DI MERITO E' MISURATO, non asserito**, e sta tutto in tre righe.

| | il criterio di uscita | il numero | dove |
|---|---|---|---|
| `1` | **`_collauda_tempo_proprio.py`: `0` violatori su `12`** — e ### **E' NEL `.githooks/pre-commit`** | `0`/`12`, `3`/`3` bracci | la prova su **un commit VERO** sta in **`f46d854`**: su un ramo usa-e-getta, col Grover a tick fisso, `git commit` e' tornato `1` e `HEAD` non si e' mosso |
| `2` | **`M-B1` PEZZO PER PEZZO al bit** contro `717bb60` | **`12`/`12`** *(6 pezzi x 2 scene)* | `5219e1b`, referto `doc/referti_l1/mb1_palindromo.txt` |
| `3` | **`M-B2`: pendenza `2.006`** su `5` dimezzamenti *(fattore `854.9`, e `4^5 = 1024`)* | e la **CONTROPROVA**: l'ordine vecchio da' **`1.183`**, cioe' **primo** ordine | `8bf0ded`, e la lettura sulla pendenza e' `[[DECISIONE-M-B2-SI-LEGGE-SULLA-PENDENZA]]` |

### ✅ **E CIO' CHE `L1` HA CONSEGNATO, oltre ai tre numeri:**
### ① **il PUNTO UNICO di lettura del tempo proprio** *(`flussi_parziali.dtau_nodo`)* —
### **nessuna legge calcola il suo `dtau` da se'**, ed e' da li' che `L2` fara' variare
`cs`;
### ② **un passo REVERSIBILE per costruzione** *(palindromo)*, che e' cio' che rende
sensato chiedersi **da dove venga l'irreversibilita'** *(`A15.3`)*;
### ③ **`0` leggi nuove e `0` parametri nuovi** — `7` leggi prima, `7` dopo *(`9-ter`)*.

### ⛔⛔ **E CIO' CHE `L1` LASCIA APERTO, con il livello a cui VA.** *(Questa tabella e' il
lascito: niente di cio' che sta qui si decide dentro `L1`.)*

| | che cosa resta aperto | dove va | perche' la' |
|---|---|---|---|
| `1` | **la simmetria materia/antimateria e l'appaiamento `eps <-> -eps`** | ### **`L5`** — `[[L5-ASIMMETRIA-NELLA-LEGGE]]` | e' la **seconda candidata** di `L5` *(strada `A`, alla Sakharov)*, e l'appaiamento e' **il suo candidato `2`** |
| `2` | **l'ORIGINE delle `n`**: da dove vengono le direzioni in un grafo **nato dalla mitosi**, senza posizioni | ### **`L3`-`L4`** — `[[N-DIREZIONI-DI-MOTO]]`, punto `(a)` | `R2` **vieta** di prendere le direzioni dalle posizioni, e un grafo che **nasce** non ha coordinate: e' la mitosi *(`L3`)* e il trasporto *(`L4`)* |
| `3` | **i due bracci rossi di `_collauda_deriva.py`** *(`Lambda_k` non piu' invariante: `1.078e+00`; la sorgente per nodo: `4.625`)* | ### **`L5`** *(perimetro)* | `deriva.py` e' uno **strumento di `L5`** e si usa **IN SOLA LETTURA** *(scelta di Luca del `2026-10-15`)* |
| `4` | **il GAUGE `P`-SIMMETRICO**: `U_{P(a)} = U_a^dagger` | ### **`L4`** — `[[N-DIREZIONI-DI-MOTO]]`, punto `(b)` | e' una **condizione sulla CONFIGURAZIONE di gauge**, e il gauge dinamico e' `L4` |

### ⚠ **E SUL PUNTO `4` C'E' UNA CORREZIONE A UNA MIA FRASE, che il guardiano ha trovato
e che accetto:** avevo scritto che la simmetria col gauge *«richiederebbe `U^dagger = U`
su ogni arco»*. ### ⛔ **Non e' vero, ed era una condizione PIU' FORTE del necessario:**
l'inversione porta l'arco `a` nell'arco **`P(a)` percorso al contrario**, quindi la
condizione e' ### **`U_{P(a)} = U_a^dagger`** — **sulla configurazione, non sull'arco
singolo.** ### 📌 **E la condizione giusta e' DERIVATA e NON ancora misurata:** la misura
di `5219e1b` usa `U = I` *(che la soddisfa banalmente)* e `U` casuale *(che non la
soddisfa, `1.218`)*. ### **Costruire una configurazione `P`-simmetrica non banale e
misurarla e' un pezzo di `L4`.**

---

### ⭐⭐ **LA SCENA DI RIFERIMENTO DI `L2`** — *solo dichiarazione, il costruttore e' il
primo pezzo di `L2`*

> ### ⛔ **OGGI NESSUNA SCENA DEL MOTORE USA `n` GEOMETRICI**, e il censimento lo dice:
> **`8` file** con `n` **casuali gaussiani**, **`3`** con **`z` uniforme**, ### **`0` con
> `n` GEOMETRICI.** ### **Cioe' la scena <<naturale>> del modello, oggi, NON ESISTE.**

| | la scena di riferimento di `L2` |
|---|---|
| **le `n`** | ### **GEOMETRICHE: direzioni di moto** *(`[[N-DIREZIONI-DI-MOTO]]`)* — l'`n` di un'estremita' e' la direzione dell'arco uscente, e i due capi di un arco hanno `n` **opposti** |
| **il gauge** | ### **`U = I`** |
| ### ⚠ **e le scene con `n` CASUALI** | ### **restano, come PROVE DI ROBUSTEZZA DICHIARATE** — ### ⛔ **non come fisica.** Un `n` casuale fisso e' **un campo magnetico**, cioe' **un termine di Zeeman che il vuoto non deve avere**: va bene per scuotere un collaudo, **non per dire come va il mondo** |
| **quando si scrive** | ### **il costruttore e' il PRIMO PEZZO di `L2`**, non adesso: qui c'e' **solo la dichiarazione** |

### 📌 **E una conseguenza pratica che vale scrivere, perche' si paghera':** tutti i numeri
misurati finora *(la deriva, le bande, il segno, `M-B2`)* vengono da scene con `n`
**casuali**. ### ⚠ **Quando la scena di riferimento esistera', quei numeri andranno RIFATTI
la', e NON si potranno confrontare con i vecchi come se fossero la stessa misura.**

---

## 13. ⛔ `L2` — **IL PRIMO PEZZO E' FATTO, E IL VERSO NON ESCE** *(`2026-10-15`)*

### ✅ **La scena di riferimento ESISTE** *(`primo_ordine/scena_l2.py`)*, con **tre grumi**
*(elicita' `+1`, `-1`, isotropo)*, e con lei **tre fatti che non erano nel disegno:**
### ① **`h_k` e' l'ELICITA', non la densita'** *(correzione del guardiano a una mia frase)*,
e `G` e' **dispari**, quindi ### **`beta` cambia segno con `h`**;
### ② **il vuoto uniforme e' stazionario a `0` ulp** *(previsione mia sbagliata in meglio)*;
### ③ ⛔ **l'elicita' NASCE:** un grumo isotropo ha `h(0) = 0` e **`max|h(t)| = 2.16`.**

### ⛔⛔ **E DUE TRAPPOLE DI SCENA CHE VALGONO PER TUTTI I LIVELLI, e stanno qui per
questo:**
### ⭐ **(i) `dtau = 1` E' UN CASO CIECO:** la' il hop del vuoto a `theta = pi` e'
### **una permutazione pura**, quindi ### **ogni misura che dipenda dall'interferenza del
vuoto NON LA VEDE** *(`dispari/pari = 1.6e-13`)*. ### **Ed e' il caso che si prende per
primo, perche' e' l'unita'.**
### ⭐ **(ii) UN GRUMO ISOTROPO NON E' UN CONTROLLO NULLO:** `h = 0` vale **solo a
`t = 0`**. ### **Chi costruisce un controllo deve guardare `h(t)`, non `h(0)`.**

### 📌 **E la decisione `[[DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA]]` resta in piedi come
DECISIONE e non come fatto misurato:** il verso e' ### **deciso da Luca e NON ancora
uscito dalla dinamica** — e il mandato diceva esattamente questo: ### **se non esce, si
riporta e si ferma.**

---

## 14. ⛔⛔ `L2` — **IL VERSO E' OPPOSTO, E L'ESPONENTE E' `6`** *(`2026-10-15`)*

### ⛔ **MISURATO, con la barra d'errore:** `E` *(la parte PARI di `dLambda`, che e'
quella che ha un verso)* e' ### **POSITIVA in tutti e sei i casi**, e a `dtau = 0.5` e
`0.25` a ### **`8`-`9` barre**. ### **Il vuoto si ACCUMULA sulla materia: il verso
OPPOSTO alla decisione.**

### ⛔⛔ **E L'ESPONENTE E' LA COSA CHE PESA DI PIU' SU TUTTO IL DISEGNO:** `E ~ x^6`
*(pendenza locale `6.013` dove `x` e' piu' piccolo)*. ### **Una <<gravita'>> che va come
`x^6` NON ESISTE PER POCA MATERIA**, mentre quella newtoniana e' **lineare nella massa.**
### ⚠ **E riguarda IL BERSAGLIO DEL PROGETTO:** la prova `②` di
`doc/IPOTESI_gravita_a_spinta.md` chiede **con che legge** due masse si avvicinano, e la
prova `③` chiede ### **il principio di equivalenza.** ### **Questo numero parla a
entrambe.**

### ⚠ **E un SECONDO problema per l'equivalenza, nel canale DISPARI:** a `dtau = 0.25`
`|O|` e' **dello stesso ordine** di `|E|`, e `O` ### **cambia segno con l'elicita'** —
cioe' ### **c'e' un trasporto NETTO che distingue lo spin.**

### 📌 **E cio' che REGGE:** il vuoto **si sposta e non nasce** *(media su tutti i nodi
`~0`, e l'anello `3` NEGATIVO mentre il centro e' positivo)*, e il controllo nullo
`beta = 0` da' **`0.000e+00`** esatto.

### ⛔ **Il livello resta `L2`, e la prossima mossa e' una DECISIONE DI LUCA**, non una
misura: ### **che fare di un verso opposto e di un esponente `6`.**

---

## 15. ⛔⛔ `L2` — **LA SORGENTE E' `rho`, E NON RIPARA L'EQUIVALENZA** *(`2026-10-15`)*

### ⭐⭐ **IL CONTO, DIMOSTRATO:** con `N = Lambda F(rho/Lambda)`, `sympy` **RISOLVE**
`F - xF' = -cx` e da' `F = x(C1 + c ln x)`. ### **Quindi `beta` esattamente lineare ⟺
`alpha` LOGARITMICA**: non e' un «obbliga», e' un ### **se e solo se.**
### 📌 **E il verso inverso con l'ipotesi DICHIARATA:** `alpha` limitata **e Lipschitz**
→ `beta' = -x alpha' → 0` → `beta` non puo' essere lineare fino a zero.

### ⭐ **E IL FLUSSO CAMBIA NATURA:** con `rho` come sorgente il flusso su `psi` e'
### **UNA FASE** *(`d rho / d psi* = psi`, stesso segno nelle due componenti)*, non una
rotazione attorno a `n`. ### **E una fase NON cambia `rho`: il termine conserva la sua
sorgente** — mentre la rotazione `h` **lo cambiava**.

### ⛔⛔ **MA LA MISURA DICE CHE NON BASTA:** al **primo** tick le tre elicita' danno lo
stesso `dLambda` *(`8.9e-17`)* — con `h` era **impossibile** — e a `2000` tick la
differenza fra `+1` e isotropo e' ### **`7.4` BARRE.**
### **Cambiare sorgente ripara l'ACCOPPIAMENTO, non la DINAMICA:** la materia **si muove**
in modo diverso per spinori diversi, e il moto ### **cambia `rho(t)`.**

### ⛔⛔ **E L'ESPONENTE MISURATO E' IL DOPPIO DI QUELLO DI `beta`** *(`6.0` per `S1`, dove
`beta ~ x^3`; `2.8`-`3.7` per `S4`, dove `beta ~ x^1.64`)*, perche' ### **la risposta e'
QUADRATICA in `beta`.** ### ⛔ **Quindi anche una `beta` ESATTAMENTE lineare non da' un
effetto lineare nella massa:** ### **la linearita' chiesta su `beta` non basta.**

### ✅ **IL CONO, nei due modi:** la **fase** per tick supera `pi` gia' a `rho = 1e-12` per
`S2` e `S3`, ### **mai per `S1` e `S4`**; ma il ### **cambiamento di STATO** per tick dice
che solo ### **`S2`** cambia lo stato **piu' del passo libero** *(`1.886x`)*.
### ⭐ **Cioe' la correzione del guardiano serve:** una fase grande ### **non basta** a dire
che il cono e' violato — ### **va misurato lo STATO.**

### 📌 **E nessuna forma tiene la figura meglio di quella di oggi:** larghezza finale
`3.61`-`4.07` per `S1`-`S4` contro ### **`3.616` dell'ATTUALE**, da `0.894`.

### ⛔ **Il livello resta `L2`. Nessuna forma e' in tabella, il motore non e' stato
toccato, e la forma dell'accoppiamento e' una DECISIONE DI LUCA** — con tre fatti in mano:
### **la sorgente `rho` non ripara l'equivalenza**, ### **la linearita' di `beta` non da'
un effetto lineare**, e ### **`beta` lineare ⟺ `alpha` logaritmica**, che il vincolo `L6`
dice ### **sperimentalmente limitato in meccanica quantistica** *(da confrontare in `L6`)*.

---

## 16. ⭐⭐ `L2` — **CON LA SORGENTE FERMA IL VERSO SI ROVESCIA, E LA RISPOSTA E' LINEARE**
*(`2026-10-15`)*

> ### ⛔⛔ **E LA CAUSA DI ENTRAMBI I ROVESCIAMENTI E' UNA SOLA: nei tre pezzi precedenti
> la sorgente NON ERA FERMA.** Il grumo si disperde, e ### **la risposta di primo ordine di
> una sorgente che si muove e' un'onda che si media a zero: resta `beta^2`.**
> ### ⭐ **La gravita' di una massa e' il suo campo STATICO.**

### ⛔ **IL VERSO:** `dLambda` sulla sorgente e' ### **NEGATIVA in tutti e `24` i casi**
*(`4` forme x `2` `dtau` x `3` accensioni)*, da `85` a ### **`1560` barre.**
### **IL VUOTO SI RITIRA: LA MATERIA CONSUMA IL VUOTO** — cioe' ### **il verso che Luca
aveva DECISO**, e che la misura a sorgente libera dava **al contrario.**
### 📌 **Non e' che una delle due sia sbagliata: misurano DUE COSE DIVERSE** — la
### **scia** *(canale `beta^2`, segno positivo)* e il ### **campo** *(primo ordine, segno
negativo)*.

### ⭐⭐ **LA LINEARITA', e questo e' il numero che pesa di piu' su tutto il disegno:**
la pendenza `log`-`log` di `|dLambda|` in `x` e' ### **`3.000` per `S1`** *(dove
`beta ~ x^3`)* e ### **`1.645` per `S4`** *(dove `beta ~ x^1.6366`)* — ### **tre cifre.**
### ⛔ **Cioe' LA RISPOSTA STATICA E' LINEARE IN `beta`, e l'esponente di `beta` E'
l'esponente dell'effetto.** ### **L'`x^6` del secondo pezzo era un ARTEFATTO.**

### ⚠ **E riguarda IL BERSAGLIO DEL PROGETTO:** la prova `②` di
`doc/IPOTESI_gravita_a_spinta.md` chiede ### **con che legge** due masse si avvicinano, e
questo numero dice che ### **la legge dell'effetto e' quella di `beta`** — quindi
### **la linearita' chiesta su `beta` TORNA a essere la cosa giusta da chiedere**, al
contrario di quello che avevo concluso nel terzo pezzo.

### ⭐ **LA SOVRAPPOSIZIONE VALE** dove la risposta non e' satura: a `x = 0.01` lo scarto
relativo e' ### **`< 1e-4` per `S1`**, `0.003` per `S4`, `0.02` per `S2` e `S3`.
### ⚠ **A `x = 0.1` tre forme su quattro sono GIA' SATURE** *(`|dLambda| = 3.8` su `4`)*, e
la' il confronto ### **non distingue <<non si sovrappone>> da <<e' satura>>.**

### 📌 **IL PROFILO e' monotono e cambia segno a `r = 14`-`15`, che e' MEZZO TORO:**
### **non e' una lunghezza fisica, e' la compensazione delle immagini periodiche.**
### ⛔ **Quindi il toro `31x31` non basta a leggere la legge di decadimento**, e `log r`
### **non si adatta** — ne' si potrebbe.

### ⛔⛔ **E DUE COSE CHE QUESTA MISURA NON DICE, e che vanno lette con lei:**
### **① niente sul verso `vuoto -> materia`** *(il congelamento esclude la retroazione per
costruzione)*; ### **② niente sul principio di equivalenza** *(la sorgente e' di una sola
elicita')*.
### ⚠ **E la sorgente congelata VIOLA la conservazione per costruzione: e' uno STRUMENTO**
*(la «massa di prova»)*, ### **non una legge, e non entra in nessuna tabella.**

### ⛔ **Il livello resta `L2`, e la scelta della forma e' una DECISIONE DI LUCA**, da
prendere con questi quattro fatti: ### **il verso statico e' quello deciso**;
### **l'esponente dell'effetto E' quello di `beta`**; ### **la sovrapposizione vale fuori
dalla saturazione**; ### **`S1` e' l'unica che resta perturbativa oltre `x = 0.1`.**

---

## 17. ⛔ `L2` — **LA FORMA E' DECISA, E RESTANO DUE COSE APERTE** *(`2026-10-16`)*

### ✅✅ **IN TABELLA dal `2026-10-16`** *(`b4972a7`)*: `CAMM-MATERIA-VUOTO`,
`N_k = rho_k ln(rho_k/(rho_k + Lambda_k))`, col flusso ### **esatto a `0.8` ulp** e
### **l'Eulero che fallisce come deve** *(`3.3e-03`)*. ### **`L1` resta chiuso**
*(`0` violatori, `M-B1` `12`/`12` al bit, `M-B2` `1.965`)*, la simmetria `(P Theta)`
### **regge col termine non lineare** *(`2` ulp)*, e la `C` sul flusso da'
`C Op C^-1 = Op^-1` ### **esattamente** *(`0` ulp)*.
### 📌 **E la risposta statica col motore COINCIDE con `S3`**, e dal `2026-10-16`
### **a parita' di accensione**: pendenza ### **`1.106` contro `1.106`**, medie a
### **`0.000` barre**, traiettorie a ### **`2.0e-13` su `2000` tick**, cono ### **`0.805`**
contro `0.80`. ### ⚠ **I numeri di prima** *(`1.108`, `3.53` barre)* ### **erano misurati
con la RAMPA da una sola parte** — difetto dello strumento, errore `n.3`.

### ✅ **DECISA** *(Luca, `2026-10-15` `23:30` e `23:38`)*: la forma dell'accoppiamento e'
### **`CAMM-MATERIA-VUOTO`**, `N_k = rho_k ln(rho_k/(rho_k + Lambda_k))`, che
### **SOSTITUISCE `CAMM-SATURAZIONE`** — e ### **le leggi che GIRANO erano `6` e restano
`6`** *(la saturazione RESTA in tabella come scheda SUPERATA, e le righe non di prova sono
`8`)*. ### ✅ **Il <<restano `7`>> era un conto sbagliato: errore `n.1` del guardiano,
corretto il `2026-10-16`, e il punto si chiude SENZA decisione.**

### ⛔⛔ **APERTA `1`: IL PRINCIPIO DI EQUIVALENZA.** La sostituzione chiude il canale di
dipendenza dallo spin ### **della SORGENTE** *(al primo tick `8.9e-17` fra le tre
elicita')*, ### **non quello della DINAMICA**: a `2000` tick la differenza fra `+1` e
isotropo e' ### **`7.4` barre** *(`74ba200`)*, perche' la materia ### **si muove** in modo
diverso per spinori diversi. ### **Da rimisurare quando la materia sara' STABILE**, e il
posto dove si chiude e' la coesione *(`DEC-FC-COESIONE`, non presa)*.

### ⛔ **APERTA `2`: LA FORMA DI `cs(Lambda)`** — come la velocita' locale della luce
dipende dal vuoto. ### **E' la prossima decisione di Luca** *(voce
`DOMANDA-LA-FORMA-DI-CS`)*, e il suo POSTO e' cablato da `F7` mentre ### **la FORMA e'
aperta** *(`A1`)*.

## 18. ✅ `L2` — **UN SOLO POSTO PERCORRE IL TICK, E `deriva` SI DIVIDE IN TRE**
*(`2026-10-16`)*

### ⭐⭐ **LA DIPENDENZA NUOVA CHE CONTA: `percorri_tick`**

```
deriva.tick              -> deriva.percorri_tick     (l'ordine INTERO dalla tabella)
deriva.sorgente_per_nodo -> deriva.percorri_tick     (+ deriva.fotografo come callback)
```

### ⛔ **Prima erano DUE percorsi**, e il secondo applicava ### **un pezzo per nome.**
### ✅ **Con un solo posto il passo MISTO non si puo' piu' scrivere**, e questa e' la
differenza fra ### **una regola** e ### **una struttura che la fa rispettare.**

### ⭐ **LA DIVISIONE DI `deriva.py`** *(era `763` righe, tetto `P-MOD` `700`)*

| modulo | righe | che cosa ci sta | `importa` |
|---|---|---|---|
| `deriva.py` | ### **`687`** | la scena, il tick, le misure, `corri` | *(come prima, piu' `deriva_serie` e `deriva_variabile`)* |
| `deriva_serie.py` | `48` | `rapporti`, `escursioni`, `secolare` — ### **statistica PURA** | ### **niente** |
| `deriva_variabile.py` | `75` | `flusso_che_gira`, `CONOSCIUTI`, `satura`, `satura_elicita` | `motore`, `composizione` |

### ⚠ **E `m0` E' TORNATA IN `deriva.py`:** messa in `deriva_serie.py` faceva
### **un CICLO di import** *(`_collauda_deriva -> deriva -> deriva_serie -> deriva`)*, e
`P-MOD` ### **l'ha rifiutato.** ### **Il ciclo e' il criterio, non il numero di righe.**

### 📌 **E I TRE CHE LA DIVISIONE HA ROTTO:** `bande.py`, `bande_floquet.py` e `segno.py`
chiamavano ### **`DV.satura`**, che e' andata in `deriva_variabile`.
### ⛔ **`P-MOD` NON li ha visti**, perche' guarda ### **gli import dichiarati**, non
### **gli attributi usati**: li ha trovati un `grep` del censimento.

## 19. 📌 `L2`/`L4` — **`Lambda_c` E LA COSTANTE DI STRUTTURA FINE** — *una domanda di
Luca, e quattro considerazioni del guardiano* *(`2026-10-16`, `13:10`)*

> ### ⛔ **QUI NON SI DECIDE NIENTE, e non c'e' nessun numero mio:** il mandato chiedeva
> ### **di registrare**, e le quattro considerazioni sono ### **del guardiano**, scritte
> ### **come considerazioni e non come risultati.**

### ⭐ **LA DOMANDA, di Luca:** *«`Lambda_c` c'entra con la costante di struttura fine?»*
### **La voce e' `[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`** — aperta adesso, perche' la
### **forma** di `cs` e' decisa *(`cs_k = Lambda_k/(Lambda_k + Lambda_c)`)* e il
### **valore** di `Lambda_c` ### **no.**

| | la considerazione *(del guardiano)* | dove tocca la mappa |
|---|---|---|
| `1` | ### **NO, non e' la struttura fine.** `alpha ~ 1/137` misura l'accoppiamento della **carica** al campo elettromagnetico; nel modello l'analogo e' ### **il campo di gauge `U` sugli archi**, che oggi e' ### **FERMO** *(`U = I`)*. ### **Oggi NON esiste una costante che faccia da `alpha`** | nascera' in ### **`L4`**, come intensita' dell'accoppiamento `psi`-`U` |
| `2` | `Lambda_c/Lambda_medio` e' ### **UN FATTORE** della `G` del modello, che e' il prodotto di ### **due anelli**: *(i)* quanto vuoto toglie la materia *(la risposta statica della legge nuova — il guardiano la cita come pendenza `~1.1`)*; *(ii)* quanto rallenta la luce per unita' di vuoto tolto *(`dcs/dLambda`, che dipende da `Lambda_c/Lambda_medio`)* | ### **`L2`**: e' il punto `D` |
| `3` | ### **IL CONFRONTO CHE DIVENTA UNA PREVISIONE:** in natura `alpha_G/alpha ~ 1e-36` *(il problema della gerarchia)*. Quando esisteranno ### **tutti e due** gli accoppiamenti, il loro rapporto ### **nel modello** va confrontato con quel numero | ### **dopo `L4`** |
| `4` | ### **L'EFFETTO SULLA SCELTA:** con `Lambda_c` ### **parametro scelto**, la debolezza della gravita' e' ### **messa a mano** *(come nella fisica di oggi)*; con `Lambda_c` come ### **memoria di nascita** del nodo, `Lambda_c/Lambda_medio ~ 1` e la gravita' esce ### **dello stesso ordine degli altri effetti** — e se anche l'accoppiamento di `U` uscisse di ordine `1`, il modello sarebbe in contrasto con la natura di ### **circa `36` ordini**, a meno che una scala enorme emerga altrove *(la crescita, il numero dei nodi, la mitosi)* | ### **`L2` adesso**, ### **`L3` per la scala che potrebbe emergere** |

### ⚠ **E IL GUARDIANO DICE CHE NON E' UN ARGOMENTO PER SCARTARE LA MEMORIA DI NASCITA:**
e' ### **la domanda da tenere ACCANTO ai numeri di `D4`** — *«una gravita' forte nel
simulatore e' un difetto o una tappa?»*

### ⛔⛔ **LA DOMANDA APERTA PER LUCA, registrata e da spuntare quando risponde:**
`[[DOMANDA-LA-GERARCHIA-GRAVITA-EM]]` — *«la gerarchia gravita'/elettromagnetismo deve
### **EMERGERE** dal modello *(e da dove)*, o ### **si accetta come parametro**?»*
### **Livello: si decide DOPO `L4`**, e resta collegata alla scelta di `Lambda_c` *(`L2`)*.

## 20. ⛔⛔ `L2` — **`Lambda_c`: LE TRE STRADE, E PERCHE' DUE SONO SCARTATE**
*(`2026-10-17`, su osservazione di Luca delle `15:14`)*

> ### ⛔⛔ **IL VINCOLO, e viene da Luca:** ### **NESSUNA COSTANTE GLOBALE NELLA
> DINAMICA.** `cs_k = Lambda_k/(Lambda_k + Lambda_c)` usa ### **solo grandezze del nodo
> `k`** e ### **un NUMERO FISSO.** ### **`Lambda_c` non si calcola MAI dallo stato durante
> la corsa** — niente `Lambda_medio`, niente `V/N`, nessuna media, nessun massimo, nessuna
> somma sul grafo ### **dentro il passo.**

| | la strada | lo stato |
|---|---|---|
| `1` | ### **`Lambda_c` PARAMETRO SCELTO**, fisso, uguale per tutti i nodi | ### ✅ **E' quella attuata in `D0`**, ed e' ### **LOCALE** per costruzione. ### ⚠ **Il valore NON e' deciso** — `[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]` |
| `2` | ### **`Lambda_c` MEMORIA DI NASCITA del nodo** *(ogni nodo il suo valore, fissato alla nascita)* | ### ✅ **E' LOCALE, e resta una candidata:** un nodo porta il suo numero e ### **non guarda nessun altro.** ### 📌 **Oggi non c'e' la mitosi, quindi non c'e' una nascita** *(`L3`)* |
| `3` | ### **`Lambda_c = Lambda_medio` DINAMICO** *(ricalcolato dallo stato)* | ### ⛔⛔ **SCARTATA, per NON LOCALITA'** — e il motivo e' ### **MISURATO** |

### ⭐⭐ **E LA NON LOCALITA' DELLA STRADA `3` E' UN NUMERO, non un'opinione**
*(braccio `(l2)` di `primo_ordine/_collauda_cs.py`)*:

| | si cambia `Lambda` in ### **UN SOLO nodo**… | quanti `cs` cambiano |
|---|---|---|
| la forma ### **LOCALE** *(strada `1`)* | …e `cs` cambia ### **solo la'** | ### **`1` su `16`** |
| `Lambda_c = V/N` ### **dinamico** *(strada `3`)* | …e `cs` cambia ### **in TUTTI** | ### **`16` su `16`** |

### ⛔ **E I DUE MOTIVI DELLO SCARTO, scritti per intero:** ### ① **NON LOCALE** — un nodo
dovrebbe ### **conoscere la media del grafo**, e nessuna legge di questo simulatore lo fa;
### ② **con la mitosi di `L3` `Lambda_medio` cambierebbe**, e ### **la luce rallenterebbe
OVUNQUE** per una nascita avvenuta ### **da qualche altra parte.**

### 📌 **E NELLE MISURE DI `D4` IL RAPPORTO `Lambda_c/Lambda_medio` E' SOLO UN'ETICHETTA:**
`Lambda_c` si calcola ### **UNA VOLTA alla costruzione della scena**, si stampa
### **come numero**, e da li' ### **resta costante.** ### **Il referto riporta IL NUMERO,
non la formula.**

### ⭐ **E UNA QUARTA STRADA, SOTTO `L6`: <<LA STRADA QUANTISTICA PER `Lambda_c`>>**
*(nota di mappa chiesta dal mandato del `2026-10-16`, da SCRIVERE e non attuare)*

Nell'automa quantistico c'e' ### **una scala naturale** — ### **un quanto per mezzo-arco,
al massimo `2d` quanti per nodo** — e la' `Lambda_c` potrebbe ### **smettere di essere
scelta** e diventare ### **<<un quanto>>.**
### ⛔ **Oggi il simulatore e' IL CAMPO MEDIO, e quella scala NON C'E'.**
### ⚠ **Quindi non e' una via disponibile: e' il posto dove la domanda potrebbe chiudersi
da sola**, e sta scritta perche' ### **non si perda.**

## 21. ⛔ `L3` — **UN NODO CHE NASCE DEVE AVERE `Lambda > 0`** *(`2026-10-17`)*

> ### ⛔ **Viene da una decisione di Luca** *(il vuoto nullo ### **non e' uno stato
> fisico**, lettura `B`)*, e ### **e' un VINCOLO su una domanda che `L3` ha gia' aperta:**
> ### **con che `phi` nasce un'estremita' di un arco nuovo**
> *(`[[DOMANDA-ESTREMITA-NUOVE-INIZIALI]]`)*.

### ⚠ **Oggi il divieto vive ### **alla costruzione della scena** e al
### **caricamento** *(un solo posto: il costruttore del motore)*. ### **Alla nascita non
c'e' ancora niente, perche' la mitosi e' `L3`** — e quando ci sara',
### **`Lambda > 0` sara' una condizione sul nato**, non una verifica a posteriori.

### 📌 **E il motivo e' lo stesso:** un nodo con `Lambda = 0` avrebbe `cs = 0`, e con lui
### **gli archi che lo toccano** *(media armonica `B-3`)*: ### **una cella sigillata per
sempre.** ### **Far NASCERE un pozzo murato sarebbe peggio che trovarne uno.**

## 22. ⭐⭐ `L2`/`L4` — **DUE CANDIDATE DOPO `H_w`: L'ACCOPPIAMENTO HAMILTONIANO E LA RIGIDITA' DEL VUOTO** *(`2026-10-17`, `22:08`)*

> ### ⛔⛔ **SI COLLOCANO, NON SI ATTUANO.** Nessuna delle due e' decisa, nessuna
> e' scritta in codice: ### **vivono qui perche' la misura di `H_w` dice che valgono una
> prova**, e ### **la scelta e' di Luca** *(`[[DOMANDA-QUALE-INVARIANTE-CON-CS]]`)*.

### 📌 **IL FATTO DA CUI NASCONO, misurato** *(`doc/referti_l2/hw_energia_pesata.txt`,
blob `578b3d69`)*: con `cs` ### **non uniforme ma CONGELATO** il passo conserva
### **l'energia PESATA `H_w`** al secondo ordine *(pendenza ### **`2.030`**)*, mentre
`H_tot` ### **non pesato e' piatto** *(`-0.003`)*; con `cs` ### **DINAMICO** anche `H_w`
si perde *(`-0.001`)*.
### ✅ **Quindi il pesaggio e' COERENTE col modo in cui il passo usa `cs`, e cio' che
rompe la conservazione e' SOLO LA DINAMICA di `cs`.**

### ⛔ **`(d)` L'ACCOPPIAMENTO HAMILTONIANO** *(proposta del guardiano)*

Il passo ### **si deriva dal generatore**

```
G = somma_k  cs(Lambda_k) * H_k            (gli archi col loro peso: la media armonica B-3)
```

e da quella derivazione ### **nasce un termine in piu' sul vuoto**: una ### **FASE su
`phi`** proporzionale a `cs'(Lambda_k) * H_k`.
### ✅ **E' una fase PURA** *(nessun modulo cambia)*, ### **flusso esatto come `S3`**,
e ### **non introduce nessuna costante nuova**: `cs'` ### **viene dalla forma gia'
scelta.**
### ⭐ **LA LETTURA FISICA, ed e' il suo interesse:** il vuoto sentirebbe
### **l'ENERGIA della materia**, non solo la sua ### **densita'** — cioe'
### **l'energia gravita.**
### ⚠ **DA DERIVARE E VERIFICARE**, e la misura di `H_w` dice ### **che ha senso
provarla** *(il pesaggio regge: manca la dinamica coerente)*. ### ⛔ **Non e' attuata,
e non la attuo.**

### ⛔ **`(e)` LA RIGIDITA' DEL VUOTO** *(proposta di Luca)*

Una dinamica che ### **rende simili i nodi vicini.**
### ⛔⛔ **LA CONDIZIONE, SCRITTA, e non e' negoziabile:** deve essere
### **REVERSIBILE** — ### **un termine di energia del GRADIENTE nel generatore** — e
### **MAI una diffusione che smorza.** ### ⚠ **Una diffusione romperebbe la simmetria
`PTheta` e la reversibilita', cioe' RIAPRIREBBE `L1`** *(che e' chiuso dal `2026-10-15`, e
la `PTheta` col termine non lineare sta a `2`-`3` ulp)*.
### 📌 **I COLLEGAMENTI:** ### **la LEGGE DEL PROFILO del campo**
*(Newton/Poisson: i vicini si somigliano ### **salvo dove c'e' materia**)* e
### **`[[PERCHE-NON-LEGA]]`.**
### ⚠⚠ **E LA NOTA DEL GUARDIANO, che va tenuta:** ### **NON risolve da sola il
criterio `(2)` di `D3`**, perche' ### **la non uniformita' di `cs` E' la gravita'** — una
rigidita' ### **non la toglie**, la ### **modella.** ### **E' un ingrediente diverso, non
una cura.**

### ⛔ **E LE CINQUE STRADE, ADESSO, SONO IN UN SOLO POSTO:** le tre letture
`(a)` `(b)` `(c)` della voce piu' queste due. ### **Il loro costo e i numeri stanno nella
voce**, e ### **la scelta e' di Luca.**

## 23. ⛔⛔ `L3` — **IL VUOTO PER ESTREMITA', E LA SCALA CHE SEGUE LA TOPOLOGIA** *(`2026-10-18`, `00:22`)*

> ### 📌 **Osservazione di Luca, integrazione del guardiano**, e
> ### **si colloca QUI: accanto a *«un nodo che nasce deve avere `Lambda > 0`»***
> *(la sezione `21`)*. ### ⛔ **Nessun codice, nessuna decisione.**

### `1)` ### **IL FATTO:** `Lambda_k` e' ### **la somma del vuoto sulle `d_k` ESTREMITA'
del nodo `k`.** ### **Oggi il grafo e' REGOLARE e la cosa non si vede**; con la
### **mitosi** i gradi diventano diversi, e ### **un nodo con piu' archi avrebbe <<piu'
vuoto>>** -- quindi ### **luce piu' veloce PER TOPOLOGIA, non per fisica.**

### ✅ **E CHE OGGI IL GRADO SIA UNIFORME NON LO DICO: L'HO CONTATO** *(`2026-10-18`)*:

| la scena | nodi | grado min | grado max | uniforme? |
|---|---|---|---|---|
| `deriva` `nn=16` *(quella di `M-B2`)* | `16` | `2` | `2` | ### **SI'** |
| `deriva` `nn=12` | `12` | `2` | `2` | ### **SI'** |
| `scena_l2` `31x31` *(la statica)* | `961` | `4` | `4` | ### **SI'** |

### ⛔ **Quindi la cura candidata, OGGI, NON CAMBIEREBBE NESSUN NUMERO** -- e questo
e' ### **il momento giusto per deciderla**, perche' ### **dopo la mitosi
cambierebbe tutto.**

### `2)` ### **LA CURA CANDIDATA:** la forma guarda il vuoto ### **PER ESTREMITA'**

```
cs_k = (Lambda_k/d_k) / (Lambda_k/d_k + lambda_c)      equivalente a   Lambda_c,k = d_k * lambda_c
```

### ✅ **E' una scala che SI AUTOREGOLA quando cambia la topologia**, ed e'
### **LOCALE** *(`d_k` e' del nodo)*. ### ⛔ **Va decisa PRIMA di `L3`.**

### `3)` ### **I DUE VINCOLI DA SCRIVERE ACCANTO:**
### `(a)` ### **`lambda_c` resta UN NUMERO PURO:** per la simmetria di scala
### **cio' che si deriva dallo stato scala con lo stato**, e le strade per il suo valore
restano ### **costante**, ### **memoria di nascita del nodo**, ### **scala dei quanti di
`L6`** *(`[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`)*.
### `(b)` ### **SE `Lambda_c` DIPENDESSE DALLO STATO DURANTE LA CORSA** *(vuoto, vicini,
`cs`)*, ### **quella dipendenza dovrebbe entrare nel generatore `G` della strada
`(d)`** -- altrimenti ### **la conservazione si rompe di nuovo**, ed e' ### **la lezione
di `D3`.** ### ✅ **E `d_k` e una memoria di nascita NON cambiano a grafo fisso**,
quindi ### **non portano termini nuovi**; ### ⚠ **con la mitosi andra' riguardato.**

### `4)` ### **E UNA NOTA CHE CHIUDE UNA STRADA:** far dipendere `Lambda_c` da `cs`
*(la <<metrica>>)* sarebbe ### **CIRCOLARE**, perche' ### **`cs` e' definita da
`Lambda_c`.**

## 24. ⭐⭐ `L2` — **IL SOLITONE A DUE LUNGHEZZE DI PLANCK** *(`2026-10-18`, `00:29`)*

> ### 📌 **Domanda di Luca, integrazione del guardiano**, e si colloca
> ### **accanto alle misure che chiudono `L2`.** ### ⛔ **Nessun codice, nessuna
> decisione**, e ### **la misura si fa quando `(d)` e' nel codice** -- che da oggi
> ### **lo e'** *(`CAMM-FASE-VUOTO`, `2026-10-18`)*.

### `1)` ### **IL MODO:** la lunghezza d'onda di ### **DUE ARCHI** *(fase alternata
`+,-,+,-` fra nodi vicini, `k = pi`)* e' ### **il piu' corto che il grafo rappresenta**,
ed e' ### **il modo del DOPPIONE** della camminata.
### ✅ **E la nota del guardiano e' GIA' registrata:** i doppioni
### **non sono un effetto di bordo**, e l'affermazione *«velocita' di gruppo
zero»* e' ### **RITIRATA.**

### `2)` ### **LA PREVISIONE DA VERIFICARE, e sono due meta':**
### `(a)` con ### **`S3` sola** la sorgente e' ### **`rho`**, e `rho` di un modo a fasi
alternate e' ### **LISCIA** -> il vuoto deve ritirarsi ### **ALLO STESSO MODO** attorno a
un solitone ### **fermo** *(`k = 0`)* e a uno ### **a fasi alternate** *(`k = pi`)*
### **con la STESSA densita'**;
### `(b)` con ### **la strada `(d)`** il vuoto sente anche ### **l'ENERGIA**, e il modo a
`k = pi` ha ### **l'energia d'arco MASSIMA** per una data densita' -> la risposta
### **deve DIFFERIRE** da quella a `k = 0`, e ### **la differenza E' la misura
dell'effetto dell'energia** *(<<l'energia gravita>>)*.

### `3)` ### **LA MISURA, e adesso si puo' fare:** due sorgenti con la ### **stessa
`rho`**, una a `k = 0` e una a `k = pi`, ### **stesso protocollo statico** *(accensione
dichiarata e uguale)*, e il confronto di ### **verso, pendenza e profilo** del ritiro;
### **prima con `S3` sola** *(deve COINCIDERE: e' il CONTROLLO)*, ### **poi con `(d)`**
*(deve DIFFERIRE, e si riporta ### **di quanto e con che segno**)*.
### ⚠ **E anche se il modo a `k = pi` resta COESO con `cs` dinamico o si disperde.**

### 📌 **E IL PROTOCOLLO E' PRONTO:** `statica_protocollo.corri` sa
### **accendere la forma** *(`lambda_c`, dal `2026-10-18`)*, e `C4` l'ha gia' usato --
### **con la stessa accensione nelle due corse.** ### **Quello che manca e' la SORGENTE a
`k = pi`.**

### `4)` ### **E UNA NOTA COME OSSERVAZIONE, NON come ipotesi da perseguire:** a grana
grossa ### **l'ampiezza media del modo a `k = pi` si annulla mentre la sua densita' no**
-- cioe' ### **da lontano si vedrebbe la sua gravita' ma non la sua onda.**
### ⛔ **Nessuna conclusione prima della misura.**

### 📌 **RIMANDO** *(`2026-10-20`)*: ### **la quantizzazione come taglio ultravioletto** del modo a `k = pi`, un'idea collocata di Luca, ### **sta sotto `L6`** *(sez.`6.2`)*.

## 25. ⭐⭐ `L3` — **LA `G` DEL MODELLO: UNIVERSALITA', STABILITA', E IL VUOTO ALLA NASCITA** *(`2026-10-18`, `00:55`-`01:04`)*

> ### 📌 **Ragionamento di Luca, integrazione del guardiano**, e si colloca
> ### **sotto `L3`, accanto alla domanda del vuoto alla nascita.**
> ### ⛔ **Nessun codice, nessuna decisione.**
> ### ⚠⚠ **E OGNI PUNTO PORTA LA SUA ETICHETTA**, perche' ### **pesano in modo
> diverso:** ### **FATTO DERIVATO** · ### **IPOTESI DI LUCA** ·
> ### **CONSIDERAZIONE DEL GUARDIANO** · ### **VALORE DI LETTERATURA DA
> VERIFICARE.**

### `1)` ⭐ **FATTO DERIVATO** *(dalla strada `(d)`, ### **da riverificare ora che e'
nel codice**)*: il termine nuovo accoppia al vuoto ### **l'ENERGIA TOTALE del nodo**, con
un coefficiente che nel tempo proprio vale

```
d ln cs / d Lambda  =  Lambda_c / (Lambda (Lambda + Lambda_c))
```

### `(a)` ⭐ **UNIVERSALITA' PER SPECIE** *(FATTO DERIVATO)*: ### **lo stesso
coefficiente moltiplica OGNI forma di energia del nodo** -- camminata della materia,
moneta di spin, accoppiamento materia-vuoto, energia del vuoto.
### ✅ **Nessun coefficiente per specie: e' il PRINCIPIO DI EQUIVALENZA ALLA
SORGENTE, per STRUTTURA.** ### ⚠ **Da verificare con una misura**, ora che `(d)`
gira: ### **due sorgenti con la STESSA energia e composizione DIVERSA.**
### 📌 **E il codice lo dice:** `Omega_k` moltiplica ### **`H_k(nodo)` INTERO**
*(i due Grover, la moneta, `N`)* piu' i contributi d'arco -- ### **non un termine scelto.**
### `(b)` **STESSA LEGGE IN OGNI NODO** *(FATTO DERIVATO)*: ### **nessun parametro per
nodo**, la formula e' ### **locale.**
### `(c)` ⛔ **IL VALORE DIPENDE DAL VUOTO DI FONDO** *(FATTO DERIVATO)*: la `G`
efficace ### **segue `Lambda` locale.** Dove il fondo e' uguale ### **`G` e' uguale**; con
fondo diverso ### **`G` diversa**; se il fondo medio ### **cambia nel tempo**,
### **`G` cambia nel tempo.**
### 📌 **CONSIDERAZIONE DEL GUARDIANO:** e' il comportamento delle teorie
### **scalare-tensore** *(tipo Brans-Dicke)*, col ### **vuoto come campo di fondo.**

### `2)` ⭐ **IPOTESI DI LUCA:** se la mitosi produce un vuoto ### **LOCALMENTE
UNIFORME A GRAPPOLI**, e un grappolo e' ### **piu' grande dello spazio osservabile**,
dentro il grappolo ### **`G` e' la stessa ovunque**; le differenze stanno
### **solo ai confini**, oltre l'orizzonte.
### 📌 **CONSIDERAZIONE DEL GUARDIANO:** il ragionamento e' ### **coerente**, ed
e' ### **la stessa logica con cui in cosmologia una regione uniforme piu' grande
dell'orizzonte spiega l'omogeneita' osservata.** ### **Regge a DUE condizioni:**
### `(i)` ### **UNIFORMITA' NELLO SPAZIO:** il grappolo deve ### **superare le scale dove
`G` e' misurata** *(sistema solare, galassie, radiazione di fondo)*;
### `(ii)` ### **UNIFORMITA' NEL TEMPO:** `G` ### **non deve derivare** mentre il
grappolo cresce.
### ⚠⚠ **VALORI DI LETTERATURA DA VERIFICARE con le fonti PRIMA di usarli come
criterio:** la deriva di `G` oggi e' vincolata a ### **circa una parte su `1e12`-`1e13`
all'anno** *(misure Terra-Luna)*, e ### **dall'epoca della nucleosintesi a qualche decina
di percento al massimo.**

### `3)` 📌 **CONSEGUENZA DELLA CONDIZIONE `(ii)`** *(CONSIDERAZIONE DEL
GUARDIANO)*: perche' `G` resti stabile mentre lo spazio cresce, ### **il vuoto PER
ESTREMITA' del nodo che nasce deve essere quello dei vicini** -- cioe' ### **la DENSITA'
di vuoto deve restare costante durante l'espansione.**
### ⭐ **E' il comportamento di una COSTANTE COSMOLOGICA** *(energia oscura)*: il
modello ### **ne sarebbe SPINTO, non lo si mette a mano.**
### ⛔ **Nessuna conclusione prima della misura.**

### `4)` ⛔⛔ **LA TENSIONE DA RISOLVERE IN `L3`** *(domanda per Luca, registrata
come voce aperta: `[[DOMANDA-LA-MITOSI-CREA-VUOTO]]`)*: ### **oggi `V` si conserva
ESATTAMENTE.** Se i nodi si moltiplicano ### **a densita' di vuoto costante**,
### **`V` totale CRESCE** -- quindi ### **la mitosi dovrebbe CREARE vuoto.**
### ⚠ **E la decisione del `2026-10-12` sul bilancio della nascita** *(genitori +
vuoto, la materia non paga)* ### **va riletta**, perche' il vuoto del figlio:
### `(a)` ### **si PRELEVA dai vicini** -- allora ### **la densita' si diluisce e `G`
deriva**; oppure
### `(b)` ### **NASCE** -- allora ### **`V` non si conserva nella mitosi**, e la
conservazione di `V` vale ### **solo a grafo fisso**; oppure
### `(c)` ⭐ **IPOTESI DI LUCA** *(aggiunta delle `01:04`)*: ### **`V` CONSERVATO
GLOBALMENTE**, grappoli ### **omogenei ma a densita' DIVERSE fra loro.**
### 📌 **CONSIDERAZIONE DEL GUARDIANO sulla `(c)`:** ### **nello spazio regge**;
### **nel tempo**, perche' `G` resti stabile in un grappolo che ### **CRESCE**
*(l'espansione osservata)*, ### **il vuoto deve ENTRARE nel grappolo dai vicini allo
stesso ritmo della nascita dei nodi** -- gli altri grappoli ### **si svuotano**, e `V`
totale ### **resta.** ### ⚠ **E' coerente ma richiede un MECCANISMO di trasporto
legato alla crescita**, e ### **il vincolo sulla deriva di `G`** *(valore di letteratura
da verificare)* ### **misura quanto preciso deve essere quel ritmo.**
### ⛔ **E LE ALTERNATIVE NON REGGONO:** *(1)* il grappolo ### **non cresce** -- non
da' l'espansione; *(2)* `G` ### **poco sensibile alla densita'** -- ### **esclusa dalla
FORMA**, perche' `d ln cs/d Lambda` ### **dipende SEMPRE da `Lambda`.**
### ✅ **LE TRE LETTURE PORTANO A CODICE DIVERSO, e la differenza e' FISICA.**

### `5)` 📌 **RIMANDO A `L5`** *(CONSIDERAZIONE DEL GUARDIANO)*: i confini fra
grappoli di vuoto diverso sarebbero ### **pareti di dominio dove `G` cambia**, ed e'
### **un'eco della strada `(3)` dei domini di materia/antimateria.**
### ⛔ **Solo un rimando, nessuna ipotesi da perseguire.**

### `6)` **LE MISURE, quando arrivera' `L3`:** `(a)` ### **`G` efficace contro il vuoto di
fondo**, su una scena con ### **due regioni uniformi a fondo diverso**; `(b)` ### **la
deriva del vuoto medio PER ESTREMITA' sotto mitosi**, per ### **le tre letture del punto
`4`.**

### ⭐ `7)` **UNA SOLA IPOTESI, ACCANTO AI GRAPPOLI OMOGENEI: LE COSTANTI DI OMOGENEITA'** *(idea di Luca del `2026-10-19`, `20:09`-`20:16`, discussa col guardiano)*

> *«LE COSTANTI DI OMOGENEITA': `G` e `Lambda` non sono costanti vere. Sono costanti DENTRO
> domini omogenei generati dalla crescita della rete; se i domini sono piu' grandi
> dell'orizzonte, chi sta dentro le vede costanti, ma su scala piu' grande possono variare.»*
> Luca: *«la costante cosmologica la notiamo come costante localmente, ma oltre l'universo
> osservabile potrebbe non esserlo: e' una costante di omogeneita'.»*

**LE CONSIDERAZIONI DEL GUARDIANO, scritte come tali:**
1. **Storia:** Einstein introdusse `Lambda` *(1917)* per tenere fermo l'universo, cioe' per far tornare i conti. Oggi l'accelerazione dell'espansione e' osservata *(supernove dal 1998, fondo cosmico, oscillazioni barioniche)*, ma il valore di `Lambda` non ha una spiegazione *(il problema della costante cosmologica)*, e dati recenti *(DESI)* discutono una possibile variazione nel tempo, ### **non consolidata**. Che l'energia del vuoto vari oltre l'orizzonte e' gia' in alcuni scenari inflazionari *(e' la base della stima di Weinberg del 1987)*: ### **nel modello potrebbe invece USCIRE dalla crescita.**
2. ### **La distinzione da non perdere:** il `Lambda` del modello e' ### **la densita' LOCALE del vuoto**, una variabile per nodo; la «costante cosmologica» sarebbe al piu' ### **il comportamento MEDIO di quel vuoto mentre la rete cresce.** Legame con l'idea gia' registrata qui: un vuoto a densita' costante durante la crescita si comporterebbe come una costante cosmologica.
3. In natura una variazione oltre l'orizzonte ### **non si osserva direttamente**; nel simulatore ### **si', perche' la rete si vede tutta.**
4. ### **I CRITERI, quando `L3` fara' crescere lo spazio** *(fissati qui, prima di qualunque misura)*:
   `(a)` il vuoto si organizza in ### **DOMINI omogenei**? *(la lunghezza di correlazione di `Lambda`, e di `G` efficace, sulla rete cresciuta)*;
   `(b)` quanto sono grandi i domini rispetto all'### **ORIZZONTE CAUSALE** della rete *(la distanza percorsa con `cs` nel tempo trascorso)*;
   `(c)` ### **DENTRO** un dominio `Lambda` e `G` costanti entro le barre, ### **FRA** domini diversi no.
   ### **Se `(b)` da' domini piu' grandi dell'orizzonte, l'ipotesi e' sostenuta; se piu' piccoli, un osservatore interno vedrebbe le «costanti» variare, e l'ipotesi CADE per questo modello.**
5. **Collegamenti:** il test di instabilita' del vuoto *(il vincolo di `L2` su `L3`, sez.`1`: oggi vuoto)*, `[[DOMANDA-LA-MITOSI-CREA-VUOTO]]`, e il vuoto per estremita' *(sez.`23`)*.

### ⛔ **E' UNA SOLA IPOTESI, NON UNA DECISIONE**: si misura quando `L3` fara' crescere lo spazio.

## 26. ⭐⭐ `L3` — **IL SECONDO ORDINE CON UNA MEMORIA, INVECE DEL PUNTO FISSO** *(idea di Luca, `2026-10-18`)*

> ### 📌 **Punto `5` del mandato del punto medio per pezzo.**
> ### ⛔ **Solo la voce, SENZA CODICE**, e ### **la decisione e' di Luca.**

### ⛔ **DA DOVE VIENE:** il secondo ordine di `G` oggi si cerca ### **con dei punti
fissi** *(`cs` al centro del palindromo, e il peso d'arco al punto medio)*, e
### **un punto fisso costa giri** -- misurati: ### **`8.4` medi e `19` massimi** per il
peso, ### **`7`-`19`** per `cs`. ### **L'idea di Luca e' di prendere il secondo ordine
DALLA MEMORIA invece che dall'iterazione.**

### ⭐ **LE DUE VARIANTI, e NON sono equivalenti:**

| | la variante | che cos'e' | il difetto |
|---|---|---|---|
| `(a)` | ### **ESTRAPOLAZIONE dal passo precedente** | il peso del tick nuovo si stima dai pesi dei tick passati | ### **ESPLICITA e NON simmetrica**, e porta ### **MODI PARASSITI** *(una ricorrenza a due passi ha una seconda soluzione, che puo' crescere)* |
| `(b)` | ### **PESO SFALSATO a meta' tick** *(alla maniera del `leapfrog`)* | il peso vive ### **a meta' tick**, e i campi ai tick interi | ### **SIMMETRICA**, ed e' la variante che vale la pena guardare |
| `(c)` | ### **LA MEMORIA COME INERZIA** *(idea di Luca, `2026-10-19`)* | ogni nodo avanza a **scatti del proprio tempo proprio** e conserva il **RESTO**; cio' che e' in transito resta in **coda sull'arco**; l'assorbimento a **sotto-tick pesati** | ### **IDEA COLLOCATA, NON OPERATIVA**: i punti aperti sono scritti sotto |


### ⭐ **(c) LA MEMORIA COME INERZIA: SCATTI DI TEMPO PROPRIO, CODA SULL'ARCO, SOTTO-TICK PESATI** *(idea di Luca del `2026-10-19`, `11:39`-`12:02`, discussa col guardiano; registrata come ### **idea collocata e NON operativa**, testo del mandato)*

### 📌 **RIMANDO** *(`2026-10-20`)*: ### **la variante `(c)` sta nel lato «automa» della domanda «automa al passo di Planck, o limite continuo?»**, sotto `L1` *(sez.`1`)*.

1) Ogni nodo avanza a passi del proprio tempo proprio e conserva da un tick all'altro il RESTO di tempo proprio non ancora speso. Quel resto e' una memoria locale, deterministica e senza numeri scelti (A15); Luca la descrive come una forma di INERZIA. Anche l'arco ha il suo tempo proprio (la media armonica dei due capi, B-3) e il suo resto.
   Parentela da annotare, non da perseguire ora: il tempo proprio come NUMERO DI SCATTI e' l'idea degli insiemi causali (causal sets: il tempo proprio fra due eventi e', a meno di una scala, la lunghezza della catena piu' lunga che li collega). E i pacchetti in coda sull'arco sono il posto naturale dove, in L6, entrerebbero i quanti (un quanto per pacchetto). Oggi cio' che si rende discreto sono gli EVENTI di scambio, non le ampiezze: il modello resta un'onda classica e deterministica.
2) Con cs che decide QUANDO un nodo avanza, e non quanto tempo scorre dentro il passo, il punto fisso di cs al centro non serve piu'.
3) La conservazione: cio' che un nodo manda e il vicino non ha ancora assorbito resta IN TRANSITO sull'arco, come in una coda. Il totale conservato e' nodi piu' code. I pacchetti in coda restano separati: sommarli romperebbe la norma (|a+b|^2 != |a|^2+|b|^2).
4) L'assorbimento: il nodo assorbe nel suo tick tutto cio' che e' arrivato, con un SOTTO-PASSO PER OGNI ARRIVO. Ogni sotto-passo ha un angolo pesato; la proposta del guardiano e' che il peso sia il tempo proprio trascorso fra un arrivo e il successivo, in modo che la somma degli angoli sia il tempo proprio del nodo: Sum(theta_i) = pi * cs * dt. Cosi' l'orologio del nodo resta lento, ogni pacchetto e' trattato da solo e la norma si conserva perche' ogni sotto-passo e' unitario. La risoluzione si adatta da sola al traffico.
5) I CRITERI, fissati prima di qualunque misura:
   - la norma conservata al bit (nodi piu' code);
   - in un campo fermo la coda resta LIMITATA, non cresce col tempo;
   - il rapporto delle frequenze fra due nodi e' cs_A/cs_B: il redshift gravitazionale come contabilita' della coda, legato al criterio (3) di L2.
6) I PUNTI APERTI:
   - l'ordine dei sotto-passi conta (le rotazioni non commutano), e la simmetria nel tempo richiede di percorrere la sequenza al contrario, quindi di ricordarla;
   - M-B1 al bit non vale piu' come braccio 0, e serve un controllo di raccordo diverso (senza differenze di cs deve ridare il passo di oggi);
   - la stabilita' nel nodo 10 della scena 32/0.01 (il guadagno -1.02);
   - il costo, che cresce col traffico;
   - l'eredita' del resto alla mitosi.
   - ### 📌 **LA TENSIONE CON `[[MEMORIA-DENTRO-H]]`** *(lettura del guardiano, scritta come tale; integrazione alla verifica fino a `8d63be67`)*: la decisione di Luca del `2026-10-10` dice ### **«nessun buffer di storia»**. ### **Il RESTO accumulato e' una variabile dinamica, e va bene;** ### **la CODA di pacchetti separati e la SEQUENZA degli arrivi da ricordare sono un buffer di storia.** Sono compatibili con la decisione ### **solo se il contenuto in transito sull'arco diventa una variabile di stato dell'arco dentro `H`, con la sua energia.** ### **Da decidere da Luca quando `(c)` si aprira'.** *(La stessa tensione e' registrata per `(a)` nella voce `DOMANDA-LO-STATO-CONTIENE-IL-PASSATO`.)*
7) LA PROVA MINIMA, quando sara' il momento: due nodi, un arco, cs diversi. Si verificano norma, coda limitata e rapporto delle frequenze.
8) La decisione "lo stato contiene il passato" resta UNA e di Luca. La variante (c) entra nel confronto con i punti fissi dopo il passo C e la misura della non convergenza.

### 📌 *(La frase qui sotto e' stata scritta per `(a)` e `(b)`; la `(c)` porta il passato nel RESTO e nelle CODE.)*
### ⛔⛔ **E IN ENTRAMBE IL PASSATO DIVENTA PARTE DELLO STATO: LO STATO NON E'
PIU' MARKOVIANO.** ### ⚠ **Non e' un dettaglio di implementazione:** oggi
### **lo stato e' `(psi, phi)` e basta**, e tutto cio' che serve al tick dopo
### **sta li' dentro.** ### **Con la memoria servirebbe anche il peso** *(o `cs`)*
### **a meta' tick**, e ### **quello diventa una variabile di stato a tutti gli
effetti** -- da salvare nel checkpoint, da confrontare in `M-B1`, da far nascere alla
mitosi.

### ⛔ **E DUE PROBLEMI CHE LA MEMORIA PORTA CON SE', e vanno scritti PRIMA di
provarla:**
### `1)` ### **L'EREDITA' ALLA MITOSI** *(`L3`)*: un nodo che ### **nasce** non ha un
passato. ### **Con che memoria nasce?** ### ✅ **E' la stessa domanda della
`[[DOMANDA-ESTREMITA-NUOVE-INIZIALI]]`**, e ### **la stessa famiglia della <<memoria di
nascita del nodo>>** -- la strada `2` di `[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`.
### ⚠ **Se la risposta fosse <<la media dei vicini>>, la memoria smetterebbe di
essere locale**, ed e' il difetto che ha fatto scartare la strada `3` di `Lambda_c`.
### `2)` ### **IL PRIMO TICK:** al tick `0` ### **il passato non c'e'.** Un avvio
### **esplicito** *(un tick di primo ordine per partire)* ### **rompe la simmetria
all'inizio**, e ### **un errore di avvio `O(dtau)` costa l'ordine a tutta la corsa** se
non si cura.

### ⛔⛔ **CORREZIONE DEL `2026-10-18` (errore `n.12`): LA MOTIVAZIONE DI PRIMA
ERA SBAGLIATA, E LA SCRIVO QUI INVECE DI CANCELLARLA.** Avevo scritto che l'idea vale la
pena perche' *«il punto medio non e' bastato (`C1 = 0.973`)»*: ### **quel
`0.973` era un artefatto della MIA OSSERVABILE** *(`g_pesata` dopo un tick legge i pesi
del CENTRO)*, e ### **col conto giusto il passo da' `2.091`** -- cioe'
### **il punto medio non serviva, e il secondo ordine c'era gia'.**

### ✅ **E LA VOCE RESTA, PERCHE' IL SUO OGGETTO C'E' COMUNQUE:** il punto fisso di
### **`cs` al CENTRO del palindromo** *(`D2`)* ### **esiste e costa** -- misurato,
### **`7`-`19` giri per tick**, e ### **fino a `74` nella spazzata di `D2`.**
### ⛔ **Quello e' il punto fisso che una memoria potrebbe togliere**, e
### **la domanda <<lo stato contiene il passato?>> resta intera.**
### ⚠ **E resta registrato anche questo:** col ramo del punto medio ### **ACCESO**,
il punto fisso di `cs` ### **non converge a rapporto `0.1` e `0.3`** *(`4` casi su `8`)* --
e ### **quel ramo e' SPENTO di default, e non si toglie: toglierlo e' una decisione di
Luca.**
### ✅ **SUPERATO IL `2026-10-19`: IL RAMO E' TOLTO** *(decisione di Luca del `2026-10-18`, `21:48`; commit `3b467aa4`, prove in `b9edb2be`: braccio `0` al bit su due scene, `C1 = 2.091`)*. ### **Il codice e i numeri restano nella storia** *(`2c95af13`)* e nel referto `doc/referti_l2/punto_medio_per_pezzo.txt` *(`880955bb`)*.

### ⛔ **E LA DECISIONE E' UNA SOLA, E DI LUCA:** ### **<<lo stato contiene il
passato: SI' o NO>>.** ### **Vale per il modello INTERO**, non per un pezzo -- e
### **si decide dopo l'esito di `C1`**, che adesso c'e'.

### ⛔ **OSSERVAZIONE DEL `2026-10-19`, SENZA CURE E SENZA SCELTE: IL PUNTO FISSO DI `cs` NON CONVERGE A TAGLIA `32` E `Lambda_c/Lambda_medio = 0.01`, COL SCHEMA DI DEFAULT** *(ramo del punto medio SPENTO)*

**Trovata** dal passo `B` *(`ec0d5f7f`)*, **riprodotta dal guardiano**, e **riprodotta da me** con `csv/_ciclo_cs.py` *(referto `doc/referti_l2/ciclo_cs.txt`, blob `d89f81f5`)*, sulla scena e lo stato di `C5`, `Lambda_c = 0.08`:
- il punto fisso alza al **tick `7` contato da `1`** *(il `6` del guardiano, contato da `0`)*, dopo `120` giri;
- all'ultimo giro **`max|x_n - x_{n-1}| = 6.206e-02`** e **`max|x_n - x_{n-2}| = 0`** esatto *(il guardiano: `7.9e-12`)*: ### **un CICLO DI PERIODO `2`**, esatto al bit nella mia corsa;
- **oscillano `10` nodi** sopra la tolleranza di `cs_al_centro` *(`1.8e-15` relativa)*, e **`4` sopra `1e-6`** *(nodi `10`, `9`, `11`, `8`: i `4` del guardiano)*; ### **il peggiore e' il nodo `10`, con `Lambda = 0.0340`, SOTTO `Lambda_c = 0.08`**, ed e' **il `Lambda` minimo della rete** in quel tick; i due valori fra cui oscilla `cs` sono `0.606` e `0.544`;
- ### **a taglia `16`, allo stesso rapporto, tutti gli `8` tick CONVERGONO.**

### 📌 **LA LETTURA DEL GUARDIANO, scritta come tale:** *e' l'ITERAZIONE SEMPLICE a non convergere dove `Lambda` scende sotto `Lambda_c` (`cs` ripido); NON e' dimostrato che il punto fisso non esista.*
### ⚠ **Riguarda `D4` e la domanda sulla memoria** *(«lo stato contiene il passato?»)*: ### **la decisione e' di Luca, e qui non si cura niente.**
### 📌 **LA LETTURA DEL GUARDIANO, scritta come tale** *(`2026-10-19`, `12:36`; ### **una lettura, non una misura**)*: la matrice del passo `C` *(`e989872d`)* dice che ### **l'unico pezzo che muove `Lambda` e' `CAMM-SPOSTAMENTO-VUOTO`** *(`S3` e `CAMM-FASE-VUOTO` cambiano solo fasi)*. Quindi ### **l'anello «`cs` -> `Lambda`» del ciclo al nodo `10` passa per il trasporto del vuoto**: e' ### **la stessa auto-dipendenza che esclude la variante `(b)`.** Per la variante `(c)` *(in coda)* ### **la memoria del resto accumulato renderebbe esplicita questa dipendenza senza punto fisso**; ### **resta aperta la simmetria nel tempo**, la stessa domanda su cui cade `(b)`.

### ⭐⭐ **IL CENSIMENTO CONTATO DEI PUNTI FISSI E DELLE DIPENDENZE** *(passi `A`-`D` del task history `2026-10-18_memoria_e_punti_fissi.md`, `2026-10-19`)* -- ### **la voce e' `[[DOMANDA-LO-STATO-CONTIENE-IL-PASSATO]]`**

| | il passo | il numero | il referto |
|---|---|---|---|
| `A` | ### **i punti fissi** | ### **`3` nel percorso del tick** *(`cs_al_centro`, la fase del vuoto, il peso al punto medio SPENTO)*, `4` nel nucleo *(piu' `passo.mezzo_implicito`, via di `H`)*. ### **Dopo la rimozione del ramo** *(in coda)* ### **nel tick ne restano `2`** | `censimento_punti_fissi.txt` |
| `B` | ### **il costo** | ### **`cs_al_centro` `76`-`92%` del tick, `Omega` `69`-`84%`**, di cui `52`-`77%` dentro i giri di `cs`; il modello `giri * c(giro)` ### **non spiegato, non bloccante** | `costo_punti_fissi.txt` |
| `C` | ### **la matrice** | tutti e `7` i pezzi leggono `cs`; ### **muove `Lambda` solo `CAMM-SPOSTAMENTO-VUOTO`, AUTO-DIPENDENTE**; incrociate ### **solo per l'auto-dipendenza** | `matrice_dipendenze.txt` |
| `D` | ### **`ambito`** | ### **`7` letture di `cs` su `7` non dichiarate**, e `cs` non e' nel vocabolario | `ambito_contro_matrice.txt` |

### ✅ **E LA RIMOZIONE E' FATTA** *(`3b467aa4`)*: il censimento rifatto dopo *(`censimento_punti_fissi.txt`, blob `bcfae04a`)* da' ### **`2` punti fissi nel percorso del tick e `3` nel nucleo**, come la previsione dichiarata prima.

### ⛔ **QUESTO CORREGGE IL NUMERO DELL'INIZIO DELLA SEZIONE**, che parlava di punti fissi *«`cs` al centro e il peso d'arco al punto medio»*: ### **quello che gira davvero a ogni tick con `cs` dinamico e' la fase del vuoto dentro `cs`**, ed e' li' il costo. ### **E per le varianti** *(lettura, non decisione)*: `(a)` resta esplicita ma non simmetrica, ### **ed e' un buffer di storia, in tensione con `[[MEMORIA-DENTRO-H]]`**; `(b)` non e' disponibile come esplicita simmetrica; `(c)` porta il passato nel resto e nelle code, con la simmetria nel tempo aperta.
### ⛔ **LA DECISIONE «lo stato contiene il passato» RESTA UNA E DI LUCA.**

## 27. 📌 `L2`/`L3` — **NELL'ERA `2` L'UNICA LUNGHEZZA E' IL PASSO DELLA GRIGLIA** *(osservazione, `2026-10-20`)*

> ### ⛔ **UN'OSSERVAZIONE: e' una LETTURA DEL GUARDIANO, scritta come tale. Nessuna decisione.**
> Registrata su mandato di Luca del `2026-10-20` *(`09:12`)*, ### **insieme ai due controlli
> del passo** *(`doc/TASK_HISTORY/2026-10-20_controllo_passo_materia_uniforme.md`)*.

**Il fatto da cui nasce:** l'instabilita' della materia uniforme di `29b997da` cresce ### **su
tutti gli anelli**, e il modo dominante e' `(15, 15)` su `31x31`: ### **`k` circa `pi`, la scala
della griglia.**

**L'era `1` aveva cose che tagliavano le scale corte PER COSTRUZIONE** *(verificate nel sorgente,
`soliton_simulator.py`)*:
- ### **una lunghezza fisica piu' grande della griglia:** `LAM = 0.8`, la larghezza del solitone nel nucleo `exp(-|x-p|/LAM)`;
- ### **il taglio del rumore:** un processo di Ornstein-Uhlenbeck correlato su `tau_c = LAM/CS_M`, il tempo-luce del solitone;
- ### **le saturazioni.**

**L'era `2` e' invariante di scala per scelta:**
- ### **l'unica lunghezza e' il passo della griglia**, quindi ### **nessuna legge protegge il modo a `k = pi`**;
- con la norma conservata esattamente non e' una catastrofe a energia infinita: ### **e' un trasferimento verso la scala della griglia.**

### 📌 **LA DOMANDA PER LUCA, SE `C1` E `C2` CONFERMANO CHE IL PASSO E' SANO:**
### **quale legge, o quale scala emergente, stabilizza il modo piu' corto?** I collegamenti da
guardare allora:
- ### **il solitone a due lunghezze di Planck** *(sez.`24`)*;
- ### **il tetto di Pauli di `L6`**: un'esclusione da' ### **una densita' massima, non una lunghezza** *(`doc/STATO_RUN.md`, e `doc/REGISTRO_FISICA.md`, candidata `(C)`)*, e il passaggio densita' → lunghezza ### **va derivato.**

### ⛔ **Se invece `C1` o `C2` trovano un difetto del passo, questa domanda NON si apre:** prima si cura il passo.

### 📌 **RIMANDO** *(`2026-10-20`, `09:19`-`09:23`)*: ### **un'idea collocata di Luca sul modo a `k = pi`, la quantizzazione come taglio ultravioletto**, sta ### **sotto `L6`** *(sez.`6.2`)*, con le sue due condizioni e il criterio per quando `L6` si aprira'.
