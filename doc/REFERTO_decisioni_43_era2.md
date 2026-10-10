# IL REFERTO DELLE `43` DECISIONI — **il mandato `2` di `6`**

> ### ⛔ **CONGELATO** *(la forma dichiarata il `2026-10-10`: `csv/_forma_referti.py`)*: questo e- un ### **REPERTO**, cioe- ### **che cosa si e- misurato A UN ISTANTE** — ### **la CI NON lo rigenera**, e il presidio verifica ### **il suo BLOB**. ### **Per rimisurarlo si rigira il suo comando AL SUO COMMIT**, come un sigillo *(`CLAUDE.md` par. `6`)*.

> ### ⛔ **Questo file e' GENERATO da `python csv/_referto_decisioni_43.py`: non si scrive a mano, e NESSUN numero e' ricopiato** *(`L-NUMERI`)*.
> **Il simulatore:** `b8c21049`, ### **non toccato** *(sha1 dei byte grezzi, ASSERITO da questo script)*.

---

## `1.` IL VERDETTO — ### **`42` decisioni su `43` applicate**

### ⛔ **IL MANDATO NON MI CHIEDEVA DI DECIDERE NIENTE: mi portava `43` decisioni GIA' PRESE.** ### ⭐ **Quindi il verdetto non e' <<ho scelto bene>>: e' <<ho tradito una decisione, si' o no>>** — e la difesa, dichiarata ### **prima** nel task history, era che ogni `motivo` ### **cita alla lettera** il pezzo del mandato che decide quella riga. ### **Se una riga non ha una frase di Luca da citare, non si scrive.**

| | |
|---|--:|
| decisioni ### **applicate** | ### **`42`** |
| decisioni ### **non applicabili** | ### **`1`** *(`Z47`)* |
| voci toccate dai lotti | `43` |
| ID ### **PRIMA** *(a `a7485c8`, il commit del task history)* | `990` |
| ID ### **ORA** | `1017` |
| ### **ID PERSI** | ### **`0`** |
| ID nati | `27` — `AGGIORNA-RIFIUTAVA-SE-STESSO`, `BARRIERA-ROTTA-NEL-COMMIT`, `BLOB-DAL-DISCO-NON-DAL-REPO`, `COMANDO-UNICO-INCOMPLETO`, `CONTO-BOOLEANI-P5`, `CONTROLLO-CONTRO-ATTESA-CONGELATA`, `DEC-ALBERO-CINQUE-SENZA-ARGOMENTO`, `DEC-Z47-TRANSIZIONE`, `DECISIONE-VUOLE-UN-CAMPO`, `DUE-VIE-SU-LEGGI-JSONL`, `FORMA-SPEZZA-ID`, `H-INDICE-IGNORA-I-VOCABOLARI`, `METADATI-REPERTO-PER-NECESSITA`, `P-ALB`, `P-BARRIERA`, `P-DET`, `P-DIM`, `P-GRAFO`, `P-GUIDA`, `P-ID`, `P-REG`, `P-SIM`, `P-TEMPI`, `PRECEDENZA-IN-CODA`, `REFERTO-VERDE-SU-FALLIMENTO`, `REPLAY-CIECO-ALLE-CANCELLAZIONI`, `SABOTATURA-NO-OP` |

### ✅ **NESSUN ID PERSO, e questa e' la lettura che conta.** Nel task history avevo fissato *<<deve restare `953`>>*, e ### **era una lettura SBAGLIATA:** `953` e' il conteggio delle voci dello ### **schema `1`** alla verifica del guardiano, ### **un numero storico.** ### ⭐ **L'invariante vero e' <<nessun ID si perde>>, e si misura sull'INSIEME** — non su un totale che cresce ogni volta che nasce una voce.

---

## `2.` I LOTTI — ### **uno per blocco, cosi' si vede QUALE DECISIONE ha prodotto QUALE RIGA**

| il lotto | che cosa decide | righe |
|---|---|--:|
| `dec43_pid` | il PRESIDIO `P-ID` del blocco 1 | `1` |
| `dec43_blocco1` | gli 11 OMONIMI: via la nota, il metadato RESTA | `11` |
| `dec43_blocco2` | gli ASSIOMI: 18 confermati + `A3c` che cambia | `19` |
| `dec43_blocco3a` | 10 delle 13 domande | `10` |
| `dec43_blocco3b` | `K2a` e `K2b`, con lo stato dalla riga d-origine | `2` |
| `dec43_z47` | la 43a: NON APPLICABILE, registrata come domanda | `1` |
| `p5_booleani` | un difetto trovato DI LATO | `1` |
| `forma_spezza` | il difetto di `H-INDICE`, trovato DAL PRESIDIO STESSO | `1` |
| `forma_chiusa` | la sua chiusura, col numero VERO | `1` |

### 📌 **Un lotto per blocco non e' un vezzo: e' cio' che rende VERIFICABILE la fedelta'.** Con un lotto solo un `motivo` sbagliato si perde fra gli altri; con un lotto per blocco ### **ogni riga porta la citazione del suo blocco**, e un lettore esterno puo' confrontarla col mandato ### **senza avere la conversazione.**

---

## `3.` I CONTROLLI CHE IL MANDATO CHIEDE

| il controllo | l'esito |
|---|---|
| `python csv/indice.py valida` | ### **FALLISCE** |
| i segnali *(non bloccano, `A9`)* | `19` |
| `DA_DECIDERE_LUCA.md` | ### **`5` voci** |
| il simulatore | `b8c21049`, ASSERITO |
| `P-ID` e la cura del criterio 2 | ### ✅ **`11`/`11`** |
| i presidi dell-indice, con `estendi` | ### ✅ **`16`/`16`** |
| `P-M1` i metodi | ### ✅ **`8`/`8`** |
| `P-C1` i controlli nell-indice | ### ✅ **`8`/`8`** |

### ⛔ **E `DA_DECIDERE_LUCA.md` NON E' VUOTO, e il mandato chiedeva che lo fosse.** ### ✅ **La ragione e' scritta, non aggirata**, ed e' quella che avevo fissato come lettura ### **prima di guardare:**

| chi resta | perche' |
|---|---|
| `DEC-NASCITA-PSI` | ### **l'ho aggiunta IO**, al punto `3` della seconda parte: e' una decisione di ### **fisica**, e aspetta Luca |
| `DEC-REGOLA-FORMA` | ### **l'ho aggiunta IO**, al punto `11(a)`: idem |
| `DEC-Z47-TRANSIZIONE` | la `43`a decisione ### **non si puo' applicare**: vedi la sezione `4.` |
| `Z47` | ### **e' la stessa domanda**, vista dalla voce che la subisce — ### **una domanda sola in due righe** |

---

## `4.` CHE COSA NON HO APPLICATO, e ### **perche' non l'ho aggirato**

Il blocco `3` dice: *<<`Z47` -> era `2`, `AGENDA` (e' il programma della decisione `9`)>>*. ### ⛔ **Ma `Z47` e' `CHIUSA`, e `CHIUSA -> AGENDA` NON E' NELLA TABELLA DELLE TRANSIZIONI** *(da `CHIUSA` si va solo ad `APERTA` o `SUPERATA`)*.

### ⚠ **E non si puo' aggirare cambiando solo l'era:** una voce con era `2` e stato `CHIUSA` violerebbe `PI-ERA-STATO` — ### **l'era `2` ammette solo `AGENDA`, perche' non e' cominciata.**

### ⭐ **IL TASK HISTORY LO AVEVA DICHIARATO COME CASO DI FERMO, PRIMA di incontrarlo:** *<<una transizione vietata e' una regola, e aggirarla con due passaggi sarebbe ### **barare col presidio**>>*. ### **Le tre vie sono ELENCATE nella voce `DEC-Z47-TRANSIZIONE`, e nessuna e' scelta da me.**

---

## `5.` UNA INFERENZA MIA, ### **dichiarata dentro il `motivo` di ogni riga**

| la voce | era | stato | che cosa ho inferito |
|---|---|---|---|
| `A3-DISEGNO` | `1` | `SUPERATA` | ### **l'era `1`**, che il mandato NON nomina per questa voce |
| `G4-MEMARCO` | `1` | `SUPERATA` | ### **l'era `1`**, che il mandato NON nomina per questa voce |
| `Z104` | `1` | `SUPERATA` | ### **l'era `1`**, che il mandato NON nomina per questa voce |

Queste tre voci erano era `2`, e ### **`PI-ERA-STATO` vieta era `2` con stato `SUPERATA`.** Il mandato per loro nomina ### **solo lo stato.** ### ✅ **Ho applicato era `1`, perche' una voce SUPERATA DA un assioma dell'era `2` e' per costruzione una voce dell'era `1`** — ed e' il trattamento che il mandato da' ### **esplicitamente** al gruppo `M-*` ### **nella stessa frase.** ### ⚠ **L'alternativa era non applicare la decisione, e sullo STATO il mandato e' esplicito.**

---

## `6.` CHE COSA HO SBAGLIATO, ### **e chi me l'ha detto**

| | l'errore | chi me l'ha detto |
|---|---|---|
| `1` | la lettura dei ### **`953` ID conservati**, che avevo FISSATO nel task history: e' il conteggio delle voci dello ### **schema `1`**, un numero storico | ### **il conteggio stesso**, non io rileggendo |
| `2` | ### **svuotare** la `nota_guardiano`: la sua regex e' `^.{1,300}$`, e la stringa vuota ### **non passa**. Una nota si ### **sostituisce con la decisione** | ### **il registro dei metadati**, dopo aver rifiutato `21` righe |
| `3` | `stato: APERTA` su una voce dell'era `1`: una voce dell'era `1` non chiusa e' ### **`SOSPESA`**, e lo stato che aveva nell'era `1` va in `stato_era_1` | ### **`PI-FISICA-ERA1-NON-SOSPESA`** |
| `4` | tre file da `0` byte lasciati alla radice *(`lca`, `u`, `v`)*, scarti di un comando mal digitato | ### **nessuno**: `H-NON-TRACCIATI` guarda ### **solo sotto `csv/` e `doc/`** — e questo e' un limite del presidio, non una mia scusa |
| `5` | la riga di `A3c` in `METODI` rimasta ### **orfana**: la decisione lo ha reso `CRITERIO`, che ### **non e' nel perimetro dei metodi** | ### **`P-M1`**, rifiutando il commit |
| `6` | il nome della voce nuova, che ### **cominciava con un ID esistente** *(`P5`)* e che l'estrattore di `H-INDICE` ### **spezzava** | ### **`H-INDICE`**, rifiutando il commit — ### **e dentro quel rifiuto c'era un difetto SUO**, vedi la sezione `7.` |
| `7` | `20` righe di storico committate ### **senza il loro campo `commit`** | ### **`PI-STORICO-SENZA-COMMIT`**, per la ### **quinta** volta in due giorni |

### ⭐ **7 ERRORI, E 6 ME LI HANNO DETTI I PRESIDI.** ### ⚠ **E questo e' il numero che conta piu' del `42` su `43`:** significa che ### **rileggendo non li vedo**, e che la rete regge ### **al posto della mia attenzione.** ### ⛔ **Il quarto non l'ha visto nessuno, ed e' quello da ricordare.**

---

## `7.` DUE CURE NATE DI LATO, ### **e perche' sono commit a se'**

### **(a) IL CRITERIO `②` DI `da-decidere` E' TOLTO.** La decisione di Luca dice ### **due cose che insieme non si possono soddisfare altrimenti:** *<<la domanda si chiude>>* ### **e** *<<il metadato omonimo resta>>*. ### ⭐ **Se il metadato RESTA e la domanda SI CHIUDE, allora non puo' essere il metadato a generare la domanda.** ### ✅ **E la guardia non si perde, perche' il criterio non ha piu' materia FUTURA: `P-ID` vieta la NASCITA di un omonimo nuovo** — nato nello ### **stesso blocco `1`**, per decisione di Luca. ### **Quindi la cura TOGLIE una legge invece di aggiungerne una** *(`9-ter`)*.

### ⚠ **E LA PREVISIONE `(a)` DEL TASK HISTORY AVEVA VISTO QUESTO, prima di guardare:** *<<togliere la nota potrebbe NON bastare, perche' il `2`o criterio e' `meta.omonimo`>>*. ### **Era vero: gli `11` omonimi hanno perso la nota ed erano ANCORA nell'elenco.**

### **(b) `H-INDICE` VERIFICAVA IL PREFISSO INVECE DELL'ID**, per ### **`122` ID su `887`**. `FORMA` e' un'alternanza, e Python prova le alternative ### **in ordine**: su un ID come `A1-COSTANTI` la prima matcha ### **`A1`** e vince, e poi la coda ### **non matcha nessuna alternativa e viene buttata in silenzio.** ### ⛔ **Quindi una citazione sbagliata passava** — ed e' un presidio che ### **non impediva cio' che dichiara** *(`A9`)*.

### 📌 **E L'HO TROVATO PERCHE' IL PRESIDIO MI HA RIFIUTATO UN COMMIT**, cercando la coda di una voce che avevo appena creato. ### ⭐ **Quella voce ha fatto scattare il difetto PER CASO: la sua coda AVEVA un trattino. Gli altri `122` non ce l'hanno, e per questo il difetto era MUTO.**

### ⚠ **E RIORDINARE LE ALTERNATIVE NON BASTAVA, ed e' MISURATO:** un ### **intervallo** col trattino *(quello che il blocco `2` usa per nominare gli assiomi)* diventerebbe ### **un ID solo che non esiste.** ### **La cura AGGIUNGE una legge, e il conto e' dichiarato nel suo commit: non si poteva togliere niente, perche' nessuna delle due forme DA SOLA basta.**

---

## `8.` CIO' CHE RESTA APERTO — ### **scritto, non taciuto**

| | |
|---|---|
| `DEC-NASCITA-PSI`, `DEC-REGOLA-FORMA` | le due decisioni di ### **fisica**, che ### **aspettano Luca** e che non prendo al suo posto |
| `DEC-Z47-TRANSIZIONE` | la `43`a decisione: ### **tre vie elencate, nessuna scelta** |
| `CONTO-BOOLEANI-P5` | i booleani di `P5` passati da `79` a `82` ### **col simulatore INTATTO**: ### **non l'ho spiegato**, e il modo di chiuderlo e' stampare ### **i NOMI**, non il conteggio |
| `A3b` | e' nell'intervallo del blocco `2`, esiste in `ASSIOMI.md` ### **solo come corollario in linea**, e ### **NON e' una voce.** ### ⛔ **Non l'ho creata indovinandone la classe**: suo fratello `A3c` e' stato riclassificato ### **da questo stesso mandato**, quindi la classe e' ### **genuinamente ambigua** |
| `H-NON-TRACCIATI` | guarda ### **solo sotto `csv/` e `doc/`**: tre file alla radice sono passati |
| `P-ID` | rifiuta un ID che ### **coincide** con uno esistente, non uno che ### **comincia** con uno esistente — ed e' il caso che ha rotto `H-INDICE` |

