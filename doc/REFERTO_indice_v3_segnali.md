# IL REFERTO DELLA CHIUSURA DEI SEGNALI DEI PRESIDI

> ### ⭐ **Il guardiano ha letto i `103` segnali uno per uno, e il verdetto e' stato: «la maggior parte e' rumore, ### E IN PARTE PER COLPA MIA».** Questo referto e' la chiusura, e ### **i numeri sono `103` -> `15`.**

| | |
|---|---|
| **quando** | `2026-10-09`, ramo `primo-ordine` |
| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_chiusura_segnali.md`, ### **committato PRIMA del lavoro** *(`f2e950f`)* |
| **i commit** | `a8107b2` *(`1`)* · `0ef62f6` *(`2`)* · `0c4cb57` *(`3`)* · `1d34bc0` *(`4`)* · `c24eb66` *(`5`)*, piu' questo |
| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |
| **il collaudo** | ### **`20` su `20`** *(erano `15`: ### **`5` bracci nuovi**, `2` su `F1` e `3` su `F4`)* |

---

## ① I SEGNALI, PRIMA E DOPO

| presidio | prima | dopo | come si sono chiusi |
|---|--:|--:|---|
| ### **`F1`** | `49` | ### **`11`** | ### **la formulazione era MIA:** `F1` ignora le voci citate `STANDARD`, `PRESIDIO` e `NON_DEFINITA`. ### ⚠ **Ma il punto `2` ne ha CREATI `6` nuovi**, e restano ### **elencati, non chiusi** |
| ### **`F2`** | `9` | ### **`1`** | `8` eccezioni che ### **citano la frase del «sostituisce»**; `ENERGIA-NON-DEFINITA` ### **non si tocca** e il suo segnale ### **resta acceso** |
| ### **`F3`** | `15` | ### **`0`** | `5` `CRITERIO` sono uscite da `FISICA` col punto `2`; `9` chiuse con l'eccezione; `1` *(`W5`)* ### **spostata** |
| ### **`F4`** | `30` | ### **`3`** | ### **la regola dell'intestazione**; `7` ripristinate, `6` omonimi, `1` resta etichetta. I `3` che restano sono ### **il QUARTO CASO** |
| ### **`F5`** | `0` | ### **`0`** | ### **zero prima e zero adesso.** `storico-commit` tiene il campo pieno |
| ### **`F6`** | `0` | ### **`0`** | ### **zero prima e zero adesso**, dal blocco `G3` |
| ### **in tutto** | ### **`103`** | ### **`15`** | |

---

## ② PUNTO `1` — **`F1` era MIO**

> ### ⛔ **«Citare un assioma non vuol dire essere gemelle»**, scrive il guardiano. `D24` dice *«`A2` e' VIOLATO da `Lam = mean(I)` — una media GLOBALE dentro una legge locale»*: `D24` e' un difetto dell'era `1`, `A2` e' uno ### **`STANDARD` che vale per ENTRAMBE le ere**, e ### **«differiscono» e' GIUSTO che sia vero.**

### ⚠ **E nel referto dei presidi avevo dichiarato `12` segnali verso i segnaposto, presentandoli come «da decidere»:** era ### **la meta' del problema vista per un quarto.** Non avevo guardato che altri `30` puntavano ad ### **assiomi e presidi** — cose che ### **per definizione valgono per entrambe le ere.** ### **`42` su `49`**, e la misura l'ho fatta ### **solo dopo che il guardiano me l'ha detto.**

### ✔ **E la restrizione si prova con DUE bracci, non col numero:** un presidio che segnala meno ### **non e' per questo giusto.** `D24` non deve scattare *(`A2` e' uno `STANDARD`)*, ### **e con `A2` finto `DIFETTO` deve tornare a scattare** — cosi' si sa che ### **e' LA CLASSE a zittirlo**, non un effetto collaterale.

### **`C5` e' un OMONIMO**, e il guardiano l'ha visto leggendo `F1`:

| | il significato |
|---|---|
| | doc/RAMIFICAZIONI.md -- la VOCE `C5`, una MISURA: <<tauluce = d/cs e' PIATTO => la sostituzione rompe la...>> |
| | doc/STATO_RUN.md e doc/RAMIFICAZIONI.md -- il <<mandato C5>>, cioe' GLI INVARIANTI: <<INVARIANTI (C5): il programma si ferma quando una grandezza esce...>> |

`Z100` e `C5-INVARIANTI` chiudono con l'eccezione: il `C5` che citano e' ### **il mandato degli invarianti**, non la voce `C5`.

### **I `11` segnali di `F1` che restano** — il mandato chiede di elencarli, ### **non di chiuderli:**

| id | `classe`/`dominio`/era | il segnale | la mia lettura |
|---|---|---|---|
| `AB-CONTROLLI` | `DIFETTO`/`METODO`/`ENTRAMBE` | cita `W5`, che e- `METODO`/era `1` | un DIFETTO che nomina la voce di cui parla |
| `COER-4PI` | `CRITERIO`/`METODO`/`1` | cita `Z120`, che e- `FISICA`/era `1` | ### **un CRITERIO che cita la legge che verifica** — e' la categoria che il punto `2` ha creato |
| `COER-4PI` | `CRITERIO`/`METODO`/`1` | cita `Z118`, che e- `FISICA`/era `1` | ### **un CRITERIO che cita la legge che verifica** — e' la categoria che il punto `2` ha creato |
| `COLLAUDO-NON-ESEGUITO` | `DIFETTO`/`METODO`/`ENTRAMBE` | cita `C4`, che e- `FISICA`/era `1` | un DIFETTO che nomina il controllo di cui parla |
| `E3` | `CURA`/`FISICA`/`1` | cita `M1`, che e- `FISICA`/era `2` | una CURA che nomina le misure da leggere durante la corsa |
| `ETICHETTA-A13` | `DIFETTO`/`DOCUMENTAZIONE`/`ENTRAMBE` | cita `A3-DISEGNO`, che e- `FISICA`/era `2` | un difetto di DOCUMENTAZIONE che nomina la regola giusta |
| `M-MASSA` | `CURA`/`FISICA`/`2` | cita `MASSA-ID`, che e- `METODO`/era `ENTRAMBE` | una CURA che dichiara ### **da che cosa DIPENDE** |
| `REGISTRO_FISICA:E3` | `CRITERIO`/`METODO`/`1` | cita `D33`, che e- `FISICA`/era `1` | ### **un CRITERIO che cita la legge che verifica** |
| `REGISTRO_FISICA:E3` | `CRITERIO`/`METODO`/`1` | cita `E3`, che e- `FISICA`/era `1` | ### **un CRITERIO che cita la legge che verifica** |
| `REGISTRO_FISICA:S6` | `CRITERIO`/`METODO`/`1` | cita `D02`, che e- `FISICA`/era `1` | ### **un CRITERIO che cita la legge che verifica** |
| `REGISTRO_FISICA:U2` | `CRITERIO`/`METODO`/`1` | cita `U2`, che e- `FISICA`/era `1` | ### **un CRITERIO che cita la legge che verifica** |

### ⛔ **LA RESTRIZIONE CANDIDATA, e NON l'ho applicata:** ### **un `CRITERIO` in `METODO` che cita una voce `FISICA` non e' una gemella** — e' ### **la relazione normale fra un controllo e la sua legge**, la stessa forma del rumore che il punto `1` ha tolto. Coprirebbe `6` dei `11`. ### **Restringere `F1` una seconda volta e' una decisione di Luca.**

---

## ③ PUNTO `2` — **la classe `CRITERIO` e' una cosa sola**

> ### ⭐ **Un criterio DICE COME SI GIUDICA, quindi e' `METODO`.** Era ### **spaccata in due**: `71` voci in `FISICA` e `35` in `METODO`, e ### **gli stessi tipi di criterio** — *«caso che deve fallire»*, *«byte-identico»* — stavano ### **da tutte e due le parti.**

### **`58` a `METODO`, `13` a classe `MISURA` restando `FISICA`**, `era` e `stato` ### **invariati.** ### ⚠ **Non e' una decisione di fisica**, e il guardiano lo dichiara; tutte restano `SOSPESE` o `CHIUSE`, quindi ### **non cambia nulla per l'era `2`, solo l'ordine.**

### ✔ **I `13` ESITI MISURATI, con LA FRASE CHE L'HA DECISO** — il mandato la chiede:

| id | la frase |
|---|---|
| `COMPONENTI:D1` | fallback 71.88 % -> ... | 5/5 PASS: e- IL NUMERO MISURATO di una componente sigillata |
| `COMPONENTI:D2` | guardia 4pi fallita nel 95.33 % | 6/6 PASS: idem, un numero misurato |
| `COMPONENTI:S3b` | l-orologio rallenta dove cs e- basso | 0.0100 volte a cs = 0.1*CSM: un VALORE, non una prescrizione |
| `COMPONENTI:S3c` | a cs = CSM il fattore e- 1 esatto | 1.000000000000000: un valore misurato al bit |
| `REGISTRO_FISICA:C3` | frazione di impacchettamento 0.384 NELLA SFERA INTERNA: una frazione MISURATA |
| `REGISTRO_FISICA:D33` | Il segno si inverte oltre 3.5pi: un FATTO misurato sul difetto, non un criterio di giudizio |
| `REGISTRO_FISICA:P1` | somma dei pesi per nodo | 50 | 9 | 0.18: una riga di TAVOLA di misure (prima | dopo | valore) |
| `REGISTRO_FISICA:P2` | contrasto Imassa / Ivuoto | 13 | 27 | 2.1: idem |
| `REGISTRO_FISICA:P3` | Lambda | 140 | 5 | 0.036: idem |
| `REGISTRO_FISICA:P3b` | ampiezza dello scuotimento | - | 5x piu- bassa | 0.2: idem |
| `REGISTRO_FISICA:P4` | csfloor dentro le masse | 0.9 | 0.55 | 0.61: idem |
| `REGISTRO_FISICA:P5` | lambdanodi | - | quasi COSTANTE, 0.74-0.76 LAM ovunque | -: e- L-ESEMPIO CHE IL MANDATO DA- |
| `REGISTRO_FISICA:T2` | -0.15 ... +0.44 | fa cio- che la geometria impone: un INTERVALLO misurato |

### ⛔ **E `4` CANDIDATI CHE LA REGOLA AVEVA PRESO E CHE LEGGENDO SONO CONTROLLI:**

| id | perche' NON e' un esito |
|---|---|
| `REGISTRO_FISICA:A3` | un nodo nato da MITOSI parte da ramp = 0 e arriva a 1 nel suo tempo-luce: <<parte da ... e arriva a>> e- CIO- CHE SI VERIFICA, non cio- che si e- misurato |
| `REGISTRO_FISICA:A4` | contrasto massa/vuoto e Lam al passo 1, CONTRO P2 = 27 e P3 = 5: <<contro>> dice che 27 e 5 sono i valori DI RIFERIMENTO, cioe- il criterio |
| `REGISTRO_FISICA:S3` | passo ZERO: sum(d < LAM) == 0 E sum(d == LAM) == 0: due CONTROLLI, e `==` non e- una misura |
| `REGISTRO_FISICA:S5` | nodi isolati == 0: un CONTROLLO |

### **Il numero c'e', ma non e' una misura: e' il valore CONTRO CUI si confronta.** Due *(`S3`, `S5`)* venivano da ### **un difetto della mia regola** — `==` non e' una misura, e' ### **un confronto** — e la regola e' corretta nel sorgente; gli altri due ### **passano solo per la lettura.**

### ⭐ **E il controllo `C3` conosce LA REGOLA, non i `6` ID** che oggi la esercitano: una voce `CRITERIO` si aspetta in `METODO` ### **qualunque cosa dicesse la lista del guardiano.** ### **Il punto `2` non e' una lista di ID: e' una regola**, e si scrive come tale — mentre `W5` *(punto `4`)* ### **l'ho deciso leggendo**, e un ID deciso leggendo ### **si scrive come ID.**

---

## ④ PUNTO `3` — **`F2`: segnali veri, voci al posto giusto**

`F2` vede l'era `1` e ### **ha ragione a vederla**: sono voci ### **di programma** che nominano il vecchio codice ### **per dire che cosa sostituiscono.** ### ⛔ **Un segnale vero su una voce giusta NON si chiude spostando la voce: si chiude DICHIARANDO perche'.**

| id | il marcatore che ho scelto nel testo |
|---|---|
| `CONSERVAZIONE-LOCALE` | *«SI CONSERVANO LOCALMENTE»* |
| `FRECCE-IMPOSTE` | *«deve EMERGERE dalla dinamica»* |
| `GRAVITA-POTENZIALE` | *«Poisson e un VINCOLO DI SCALA»* |
| `INVARIANZA-LOCALE-CS` | *«MISURA LA SUA c_s COSTANTE SUL POSTO»* |
| `M-FLUSSO` | *«al posto di mem_mot»* |
| `M-ISTERESI` | *«COMPLEMENTO di MEM-VERSO»* |
| `MASSE-PESI-SOVRAPPOSTE` | *«E UNA CONFIGURAZIONE DEL CAMPO»* |
| `VUOTO-LOCALE-DETERMINISTICO` | *«UNA legge per nodo»* |

### ✔ **LA CITAZIONE NON SI RICOPIA: SI ESTRAE DAL TESTO VIVO.** Per ogni voce ho ### **letto** il testo e scelto ### **un marcatore**; la frase la ritaglia il codice ### **attorno a quel marcatore, dal testo della voce.** Cosi' e' letterale ### **per costruzione**, non per mia diligenza nel copiare — e ### **se il marcatore non c'e', il codice si ferma** invece di scrivere un'eccezione falsa.

### ⛔ **`ENERGIA-NON-DEFINITA`: il segnale RESTA ACCESO, ed e' voluto.** Il mandato dice di non toccarla; prende ### **solo la nota** *«da decidere da Luca: superata da `A16` (`H` definita)?»*. Il guardiano scrive che ### **secondo lui e' superata**, e lo dice ### **come opinione, non come decisione.** ### ⭐ **Un'eccezione dice «guardato, va bene cosi'»; una nota dice «da decidere». Chiuderlo sarebbe stato decidere al posto di Luca.**

---

## ⑤ PUNTO `4` — **`F3`: il commento e' IL CONTRASTO, non il difetto**

### ⭐ **La regolarita' che viene fuori leggendo, e non l'avevo prevista:** in ### **quattro dei cinque** letti il commento o il docstring e' ### **il contrasto**, non il difetto — la voce dice *«il codice fa `X` e il commento dice `Y`»*, e ### **il difetto e' `X`.**

| id | esito | perche' |
|---|---|---|
| `A2-DXD` | resta `FISICA` *(legge)* | il <<criterio>> del titolo e- IL CRITERIO DI RIAPERTURA DI  QUESTA VOCE, non il suo argomento: cio- di cui parla e- |dx|/d  del freno-legge, da RIMISURARE nel regime nuovo. E- una  grandezza della legge |
| `D02` | resta `FISICA` *(legge)* | il docstring e- IL CONTRASTO, non il difetto: il difetto e-  che pozzo_grafo calcola L da self.pos, cioe- DAL DISEGNO, dove  servirebbe la distanza reale. E- la gravita- che legge il  disegno, ed e- fisica |
| `G3` | resta `FISICA` *(sigillo)* | idem: cura chiusa col sigillo |
| `POTENZE-1` | resta `FISICA` *(sigillo)* | e- una CURA CHIUSA COL SIGILLO: il titolo nomina il sigillo  perche- il sigillo e- cio- che l-ha chiusa |
| `RAMPA-1` | resta `FISICA` *(sigillo)* | idem: cura chiusa col sigillo |
| `S08` | resta `FISICA` *(legge)* | la domanda aperta e- <<se phi non e- l-azimut del Bloch, CHE  COS-E-?>>, e il docstring e- nominato perche- Z121 lo ha  REFUTATO. L-oggetto e- phi, non il docstring |
| `SCHERMATURA-LEGGE-REVISIONE` | resta `FISICA` *(legge)* | il commento e- UNO DEI TRE PUNTI, e gli altri due sono della  legge: una rho_c GLOBALE (viola A2) e un numero NON DERIVATO  (viola A1). Due su tre sono fisica |
| `SCHWINGER-UN-NODO` | resta `FISICA` *(legge)* | il commento e- IL CONTRASTO: il fatto misurato e- che lo  Schwinger crea UN SOLO nodo e LA CARICA CAMBIA di +-1. Una  conservazione violata e- fisica |
| `Z124` | resta `FISICA` *(sigillo)* | idem: cura chiusa col sigillo |
| `W5` | ### **spostata a `METODO`** | il testo e- INTERAMENTE UN PROTOCOLLO DI VERIFICA --  <<CRITERIO di POZZO-D: A/B nel driver, scena (ii)(a), 4 semi,  120 passi, con la barra fra semi>> -- e NON dice niente su che  cosa la legge faccia. E- il COME SI GIUDICA, quindi METODO |

### ⚠ **E una cosa che lascio a Luca:** la ### **classe** di `W5` resta `DIFETTO`, e il suo testo e' ### **un criterio.** Il mandato dice *«sposta»*, cioe' il dominio, e il dominio l'ho spostato; ### **cambiare anche la classe sarebbe applicare il punto `2` a una voce che il punto `2` non toccava.**

---

## ⑥ PUNTO `5` — **`F4`, e il FALSO-UNO per la terza volta**

### ⛔ **LA REGOLA DELL'INTESTAZIONE: l'ID deve essere il SOGGETTO, e ci deve essere CONTENUTO.** La distinzione e' ### **grammaticale**: in `## APERTO CURA1-CORTO` l'ID e' il soggetto; in `### 1.2 ⚠ E LA LETTURA CHE DECIDE DAVVERO — dichiarata POST-HOC, non era fissata prima` ### **`POST-HOC` e' un aggettivo**, e `RI-LETTO`, `RI-VERIFICATI`, `SOVRA-CORREGGE` sono ### **verbi.**

### ✔ **Il collaudo ha TRE bracci, non i due che il mandato fissa:** `POST-HOC` non deve scattare, `TW-1` a `6e5e75b` deve, ### **e con la regola SPENTA `POST-HOC` deve tornare a scattare** — senza il terzo, *«`POST-HOC` non scatta»* potrebbe essere vero ### **per la ragione sbagliata.**

### ⛔ **IL FALSO-UNO PER LA TERZA VOLTA, E STAVOLTA I FILE ERANO MIEI**

| | il file che ELENCA e sembrava DEFINIRE | chi l'ha preso |
|---|---|---|
| `1` | `doc/INDICE.md`, letto dal controllo `C4` — ### **un file che `C4` genera lui** | il controllo dell'idempotenza |
| `2` | `doc/LISTA_CHIUSA.md`, ### **la lista degli ID** | il ripasso del blocco `C` |
| `3` | ### **I MIEI REFERTI** — `doc/REFERTO_indice_v3_presidi.md` scrive `| ID | … |` per ogni segnale | ### **io, guardando i nomi dei file nell'uscita** |

> ### ⭐ **IL PRINCIPIO, scritto una volta per tutte in `doc/REGOLE/par9.md`:** ### **un file che PARLA DELL'INDICE ELENCA gli ID; non li DEFINISCE.**

### **E `F4` SI FERMA AL PRIMO FILE**, quindi ### **non puo' dire se un ID e' un omonimo.** Per quello c'e' `python csv/_cerca_definizioni.py`, che cerca ### **TUTTE** le definizioni in ### **`1527` file tracciati.**

### ✔ **I QUATTRO ESITI, voce per voce**

| id | esito | definizioni | perche' |
|---|---|--:|---|
| `CURA1-CORTO` | ### **ripristinata** `MISURA`/`FISICA`/era `1`/`APERTA` | `1` | UNA CORSA: l-intestazione `## APERTO CURA1-CORTO` apre una sezione con avvio, blob, HEAD e il comando che la rigira. E lo stato APERTA non l-ho scelto: lo dice l-intestazione |
| `CURA2-CORTO` | ### **ripristinata** `MISURA`/`FISICA`/era `1`/`APERTA` | `1` | UNA CORSA: stessa forma di CURA1-CORTO, stessa sezione di doc/STATO_RUN.md |
| `DE-ACCOPPIABILITA` | ### **ripristinata** `MISURA`/`FISICA`/era `1`/`SOSPESA` | `1` | UNA MISURA: `## 4. DE-ACCOPPIABILITA- -- analisi, non piano`, e il contenuto e- un FATTO letto dal codice -- <<la legge GIA- GIRA in entrambi gli schemi>> |
| `H1` | ### **ripristinata** `MISURA`/`FISICA`/era `1`/`SOSPESA` | `4` | UNA MISURA, e in QUATTRO POSTI CON UN SOLO SIGNIFICATO: <<la scena NON tocca phivel>>, confermata per struttura |
| `H3` | ### **ripristinata** `MISURA`/`FISICA`/era `1`/`SOSPESA` | `4` | UNA MISURA, e in QUATTRO POSTI CON UN SOLO SIGNIFICATO: <<chi scalda il vuoto, il termostato o lo scuotimento>> -- il fatto regge, la causa no |
| `SIGILLO-CURA2` | ### **ripristinata** `MISURA`/`FISICA`/era `1`/`APERTA` | `1` | UN SIGILLO: `## APERTO SIGILLO-CURA2` in doc/STATO_RUN.md, con la corsa che lo esegue |
| `SIGILLO-CURA2-RIPARATO` | ### **ripristinata** `MISURA`/`FISICA`/era `1`/`APERTA` | `1` | UN SIGILLO: idem, il ri-giro riparato |
| `D3` | ### **OMONIMO**, `NON_DEFINITA` | `8` in `6` file | le stesse DUE TAVOLE di D4, D5 e D6: doc/CENSIMENTO_intenzioni.md (una voce del censimento) e doc/MAPPA_accoppiamenti_spin.md (un TERMINE di accoppiamento), piu- la forma U(2) della coppia |
| `D4` | ### **OMONIMO**, `NON_DEFINITA` | `2` in `2` file | le stesse DUE TAVOLE: doc/CENSIMENTO_intenzioni.md (l-evoluzione SU(2) congelata) e doc/MAPPA_accoppiamenti_spin.md (il RUMORE DEL VUOTO, `_nb`) |
| `H2` | ### **OMONIMO**, `NON_DEFINITA` | `3` in `3` file | DUE oggetti: l-ipotesi dello scioglimento (<<la coppia non legge la fase corrente>>) e un CRITERIO LOCALE del sigillo del twist (<<H2 e H3: forma algebrica>>) |
| `S1` | ### **OMONIMO**, `NON_DEFINITA` | `22` in `19` file | e- UN CRITERIO LOCALE DI SIGILLO, e ogni sigillo gli da- un senso suo: <<il controllo forte, il blob nuovo riproduce AL BIT>>, <<riduzione al limite: allineati -> U = I>>, <<controlli positivi sintetici>>, <<FAIL ATTESO>> |
| `S3` | ### **OMONIMO**, `NON_DEFINITA` | `21` in `19` file | idem: <<`d` sotto LAM>>, <<riduzione DETERMINISTICA: spengo il rumore del vuoto>>, <<0 differenze non spiegate>> |
| `T1` | ### **OMONIMO**, `NON_DEFINITA` | `34` in `23` file | idem: <<lo SCHEDULATORE DEL PASSO>>, <<T1 e- BYTE-IDENTICO>>, <<la nascita conserva -- RESTRINGE A14.2>> |
| `GLOBALE-DIS` | resta etichetta, con l'eccezione | `1` | la sua UNICA definizione dice che l-ID NON ESISTE: doc/relazioni/2026-09-26.md:1068, <<GLOBALE-DIS NON ESISTE: L-HO INVENTATO IO TRONCANDO>>. Ripristinarla come voce sarebbe dare un posto nell-indice a UN TRONCAMENTO |
| `AUTO-MANUTENZIONE` | ### ⚠ **il QUARTO CASO**: nota, e ### **segnale ACCESO** | `1` | da decidere da Luca: definita in UN SOLO POSTO (doc/STORIA_REGOLE.md:479) ma il contenuto e- UNA REGOLA DI LAVORO, non una corsa ne- un sigillo ne- una legge ne- una misura. Il mandato non dice che farne |
| `F4` | ### ⚠ **il QUARTO CASO**: nota, e ### **segnale ACCESO** | `1` | da decidere da Luca: definita in UN SOLO POSTO (doc/relazioni/2026-09-21.md:3572) ma il contenuto e- UNA FAMIGLIA DI DIFETTI che punta a un-altra voce (<<scritture di stato senza traccia | D04>>), non una corsa ne- un sigillo ne- una legge ne- una misura |
| `F5` | ### ⚠ **il QUARTO CASO**: nota, e ### **segnale ACCESO** | `1` | da decidere da Luca: idem, <<fasi col periodo sbagliato | D34>> |
| `TEMPO-LUCE` | resta etichetta | ### **`0`** | il guardiano la dava per ### **candidata al ripristino**; nel repo ### **non e' definita da nessuna parte**, e con la regola nuova `F4` non la segnala piu' |
| `MASSE-COERENTI` | resta etichetta | ### **`0`** | il guardiano la dava per ### **candidata al ripristino**; nel repo ### **non e' definita da nessuna parte**, e con la regola nuova `F4` non la segnala piu' |

### ⚠ **DUE LETTURE MIE, e le dichiaro:**

| | la lettura |
|---|---|
| ① | il primo esito dice *«in un solo ### **POSTO**»*; `H1` e `H3` sono definite in ### **quattro posti con UN SOLO SIGNIFICATO**. ### **Il cancello esiste per non FAR SCEGLIERE**, e con un solo significato ### **non c'e' niente da scegliere** |
| ② | il contenuto deve essere *«una corsa, un sigillo, una legge, una misura»*. ### **Una REGOLA DI LAVORO non e' una legge** *(`AUTO-MANUTENZIONE`)*, e ### **una FAMIGLIA di difetti che punta a un'altra voce non e' nessuna delle quattro** *(`F4`, `F5`)*: ### **quarto caso**, e l'avevo previsto nel task history |

### ⭐ **`D3`, `D4`, `D5`, `D6`: QUATTRO OMONIMI DALLA STESSA COPPIA DI TAVOLE** — `doc/CENSIMENTO_intenzioni.md` *(voci del censimento)* e `doc/MAPPA_accoppiamenti_spin.md` *(termini di accoppiamento)*. ### **E' un fatto sull'indice, non su quelle quattro voci.**

### ⚠ **E DUE SEGNALI CHE HO CREATO IO, chiusi nello stesso giro:** ripristinando `SIGILLO-CURA2` e `SIGILLO-CURA2-RIPARATO` come voci `FISICA`, `F3` e' risalito da `0` a `2` — ### **il segnale scattava SUL LORO STESSO NOME**, perche' *«sigillo»* e' ### **nell'ID.**

---

## ⑦ I CONTEGGI E I CONTROLLI

> **PRIMA** = `git show 433d215`. **DOPO** = il disco. ### **Nessun numero ricopiato.**

| `dominio` | prima | dopo | |
|---|--:|--:|---|
| FISICA | `439` | `387` | ### **-52** |
| METODO | `136` | `195` | ### **+59** |
| DA_CLASSIFICARE | `181` | `187` | ### **+6** |
| INFRASTRUTTURA | `47` | `47` |  |
| DOCUMENTAZIONE | `27` | `27` |  |

| `classe` | prima | dopo | |
|---|--:|--:|---|
| DIFETTO | `210` | `210` |  |
| NON_DEFINITA | `181` | `187` | ### **+6** |
| FRONTE | `169` | `169` |  |
| CRITERIO | `107` | `94` | ### **-13** |
| MISURA | `55` | `75` | ### **+20** |
| CURA | `46` | `46` |  |
| PRESIDIO | `34` | `34` |  |
| STANDARD | `28` | `28` |  |

| `era` | prima | dopo | |
|---|--:|--:|---|
| 1 | `451` | `458` | ### **+7** |
| DA_CLASSIFICARE | `182` | `188` | ### **+6** |
| ENTRAMBE | `172` | `172` |  |
| 2 | `25` | `25` |  |

| `stato` | prima | dopo | |
|---|--:|--:|---|
| SOSPESA | `280` | `283` | ### **+3** |
| DA_CLASSIFICARE | `182` | `188` | ### **+6** |
| CHIUSA | `187` | `187` |  |
| APERTA | `156` | `160` | ### **+4** |
| AGENDA | `25` | `25` |  |

| | prima | dopo |
|---|--:|--:|
| voci | `830` | ### **`843`** |
| etichette rimosse | `122` | ### **`109`** |
| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |

```
  C1 CONSERVAZIONE: ogni ID vecchio in UNO E UNO SOLO posto PASSA   persi 0, doppi 0
  C2 la TRACCIA copre ogni ID vecchio, con la REGOLA       PASSA   senza traccia 0
  C3 LE LISTE DEL GUARDIANO: classificazione come indicata PASSA   fuori posto 0
  C4 IDEMPOTENZA (NON si rilancia: c'e' lavoro di dopo)    PASSA   storico.jsonl ha 1201 righe -> verificata al commit 6b8cb90; e la migrazione ha un PRESIDIO che la ferma
  C5 `indice.py valida` passa                              PASSA     ### i PRESIDI contro le mescolanze: 15 segnali (F1=11  F2=
  C6 la VISTA passa IL VALIDATORE VECCHIO (quello del pre-commit) e la domanda PASSA   12 bloccanti su 843 voci
  F1  DEVE scattare: B2 cita Z31, e Z31 era FISICA/era 1         PASSA   il titolo di B2 dice <<Z31 -- i sigilli non ri-girabili | Z31, ...>>
  F1  NON deve scattare: con Z31 corretta (METODO/ENTRAMBE)      PASSA
  F1  NON deve scattare: D24 cita A2, che e- uno STANDARD (entrambe le ere) PASSA   il titolo di D24 dice <<A2 e- VIOLATO da Lam = mean(I)>>
  F1  DEVE scattare: con A2 finto DIFETTO -- e- LA CLASSE che lo zittisce PASSA
  F2  DEVE scattare: D35 era era 2 e nel titolo ha (:5443)       PASSA   era `2` a 6e5e75b
  F2  NON deve scattare: D35 corretta (era 1)                    PASSA
  F3  DEVE scattare: C28 era FISICA e il titolo dice <<ALCUN SIGILLO>> PASSA   dominio `FISICA` a 6e5e75b
  F3  NON deve scattare: C28 corretta (METODO)                   PASSA
  F4  DEVE scattare: TW-1 era un'etichetta, ed e' DEFINITA in un documento PASSA   doc/SCALE_TW_lettura.md la definisce con una riga di tabella
  F4  NON deve scattare: TW-1 oggi NON e' fra le etichette       PASSA
  F4  NON deve scattare: POST-HOC, l-ID sta DENTRO LA PROSA dell-intestazione PASSA   `### 1.2 ... -- dichiarata POST-HOC, non era fissata prima`
  F4  DEVE scattare: TW-1 a 6e5e75b -- una RIGA DI TABELLA lo definisce PASSA   la regola dell-intestazione NON tocca le righe di tabella
  F4  DEVE scattare: con la REGOLA SPENTA, POST-HOC torna a segnalare PASSA
  F5  DEVE essere un ERRORE: riga 2 GIA' COMMITTATA e senza commit PASSA   n_head=2 -> la riga 2 e' committata, la 3 e' IL RITARDO e NON si segnala
  F5  NON deve scattare: le righe oltre HEAD sono il RITARDO dichiarato PASSA
  F6  DEVE scattare: la nota dice lista 3 (FISICA/1/SOSPESA), la voce e' DOCUMENTAZIONE PASSA
  F6  NON deve scattare: con la nota della correzione v3         PASSA
  ECCEZIONE  DEVE essere un ERRORE: non cita il testo alla lettera PASSA
  ECCEZIONE  NON deve essere un errore: cita 40 caratteri del titolo PASSA
  ECCEZIONE  DEVE essere un ERRORE: fuori forma (manca `F<n>:`)  PASSA
```

| | |
|---|---|
| `python csv/_controlli_indice_v2.py` | ### **6 su 6** |
| `python csv/_collaudo_presidi_indice.py` | ### **20 su 20** |
| `python csv/indice.py valida` | ### **passa** |
| `python csv/indice.py collaudo` | ### **21 su 21** |
| `python csv/_indice_id.py` *(il validatore del `pre-commit`)* | ### **passa** |

---

## ⑧ CHE COSA RESTA A LUCA

| | che cosa, e perche' non l'ho deciso io |
|---|---|
| ### **gli `15` segnali che restano** | `11` di `F1` *(di cui `6` sono la categoria che il punto `2` ha CREATO)*, `1` di `F2` *(`ENERGIA-NON-DEFINITA`)*, `3` di `F4` *(il QUARTO CASO)*. ### **Sono ELENCATI, non chiusi** |
| ### **`ENERGIA-NON-DEFINITA`** | *«superata da `A16` (`H` definita)?»*. Il guardiano dice che ### **secondo lui si'**; la voce porta la nota e ### **il segnale acceso** |
| ### **la restrizione `2` di `F1`** | *un `CRITERIO` in `METODO` che cita una voce `FISICA` non e' una gemella*. ### **Coprirebbe `6` segnali, e NON l'ho applicata** |
| ### **la classe di `W5`** | resta `DIFETTO`, e il testo e' ### **un criterio** |
| ### **il QUARTO CASO** | `AUTO-MANUTENZIONE` *(una regola di lavoro)*, `F4` e `F5` *(una famiglia di difetti)*: ### **nessuno dei tre esiti del mandato** |
| ### **le `7` ripristinate** | portano una ### **classificazione che ho letto io** dal testo che le definisce. Lo ### **stato** `APERTA` non l'ho scelto *(lo dice l'intestazione)*; ### **classe e dominio sono MIEI** |
| ### **`S1`, `S3`, `T1`** | `22`, `21` e `34` definizioni: `meta.omonimo` ne porta ### **sei piu' il conteggio**, e la lista intera sta in `doc/indice/_definizioni.json` |

> ### ⭐ **Il criterio, lo stesso di tutto il giro:** dove il mandato ### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, ### **ho lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un difetto.**

