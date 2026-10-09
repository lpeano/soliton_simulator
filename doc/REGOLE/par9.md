# dettaglio di `CLAUDE.md` par.9 — **l'indice dei difetti** *(schema `3`, 2026-10-09)*

> ### ⛔ **LA FONTE E' `doc/indice/voci.jsonl`.** Lo schema sta in **`doc/INDICE_SCHEMA.md`**,
> e questo file ne spiega il **perché**. *(Aggiornato allo schema in vigore su
> **autorizzazione di Luca**; il dettaglio dello schema `1` vive nel tag `pre-indice-v2`.)*

---

## PERCHE' NON SI LEGGE INTERO

`867` voci. **Leggerle tutte per trovarne una è il modo di non trovarla**, e di citarne una
che non c'entra. **Si interroga col comando**, che filtra su **campi**, non su testo.

### **I COMANDI**

```
python csv/indice.py cerca --stato SOSPESA --dominio FISICA --era 1
python csv/indice.py cerca --legge L-LA-SINCRONIZZAZIONE      # chi parla di quella legge
python csv/indice.py cerca --variabile V-PHIVEL --assioma A16
python csv/indice.py cerca --blocca SI
python csv/indice.py cerca --meta priorita=ALTA
python csv/indice.py mostra --stato DA_CLASSIFICARE --quante 50   # per LEGGERE il contenuto
```

### ⚠ **`--cerca`, `--dettaglio`, `--blocca SI` del vecchio `csv/_indice_id.py` **VIVONO
ANCORA**, e leggono **la vista compatibile** `doc/INDICE_ID.tsv`. **Non sono stati
riscritti**, ed è lo scopo della vista.

---

## LA REGOLA CHE TIENE IN PIEDI TUTTO

> ### ⛔ **NESSUNO STRUMENTO LEGGE `titolo` O `descrizione` PER DECIDERE QUALCOSA.**
> ### **Se una decisione serve a un programma, serve un CAMPO.**

**Perché è scritta:** lo schema `1` teneva in **testo libero** che cosa fosse una voce, a quale
ambito appartenesse e in che stato fosse. La sospensione dell'era `1` classificò
`METODO`/`FISICA` **con parole chiave nel titolo**, e sbagliò in quattro modi — `317`
segnaposto trattati come voci, ~`50` «metodo» che erano fisica, ~`45` lezioni di metodo
sospese, ~`40` voci dell'era `2` sospese. ### ➜ **La causa non era l'euristica: era che
l'indice NON AVEVA UN CAMPO per dirlo.**

---

## I VOCABOLARI, e perché sono CHIUSI

| campo | i valori | |
|---|---|---|
| `classe` | `DIFETTO` `CURA` `MISURA` `CRITERIO` `PRESIDIO` `STANDARD` `TEORIA` `DECISIONE` `FRONTE` `NON_DEFINITA` | che cosa **è** |
| `dominio` | `FISICA` `METODO` `INFRASTRUTTURA` `DOCUMENTAZIONE` `DA_CLASSIFICARE` | di che cosa **parla** |
| `era` | `1` `2` `ENTRAMBE` `DA_CLASSIFICARE` | **quando** vale |
| `stato` | `APERTA` `IN_CORSO` `CHIUSA` `SOSPESA` `SUPERATA` `AGENDA` `DA_CLASSIFICARE` | **dove** è |

### 📌 **E quando il vocabolario non ha il valore che serve, NON si inventa:** si **aggiunge
al vocabolario**, con `schema_version` che sale e **una migrazione riseguibile**. È quello che
è successo a **`NON_DEFINITA`** *(schema `3`)*: i segnaposto avevano classe `DIFETTO`, e **un
segnaposto non è un difetto**.

### ⛔ **`DA_CLASSIFICARE` è TRANSITORIO:** **nessuna transizione lo raggiunge** — ci si entra
solo con una migrazione — e **si esce solo con una decisione registrata**.

### ⚠ **E UN ERRORE DI FORMA DA NON RIFARE, perché è già stato fatto:** nell'indice dell'era
`1` **`teoria` era uno STATO**, e voleva dire *«questa è una regola o un assioma, non un
difetto»*. La migrazione allo schema `2` lo trasportò come **CLASSE**, e nacquero `51` voci
`TEORIA` **di cui nessuna era una teoria** *(erano assiomi, presidi, standard e criteri di
sigillo)*. ### ➜ **Un campo usato per dire un'altra cosa è esattamente ciò che i vocabolari
chiusi esistono per impedire.**

---

## I RIFERIMENTI SI VALIDANO

`leggi`, `variabili`, `assiomi` non sono testo: sono **ID dei registri** in `doc/indice/`
*(`leggi.jsonl`, `variabili.jsonl`, `assiomi.jsonl`, `decisioni.jsonl`)*, e i registri si
**GENERANO dalle fonti** *(`csv/_registri_indice.py`)*. ### ➜ **Una voce che cita una legge
sparita FALLISCE la validazione**, ed è voluto.

### ⚠ **E `si_riferisce_a_era1` NON è un riferimento:** era riempito **cercando nomi nel
testo**, quindi **per difetto**. Vive come metadato, e **non si usa per decidere**.

---

## UNA VOCE NUOVA, E LA SPIEGAZIONE IN `STATO_RUN`

Un difetto nuovo è **una voce**, più la spiegazione lunga in `doc/STATO_RUN.md` **con lo
stesso ID**. **Mai il contrario:** un ID citato e **non definito** è **un RAPPORTO**
*(`indice.py citazioni`)*, **non una voce**.

### ⛔ **NESSUN SEGNAPOSTO AUTOMATICO, mai più.** Lo schema `1` ne creò `320` su `953`, con il
titolo *«(CITATO N volte, MAI definito in un registro)»*: **un terzo dell'indice era un
effetto collaterale di uno strumento.**

### **Negli scritti NUOVI un ID si cita `[[ID]]`.** Le etichette **locali** — `H1`, `D1`,
`T1`, `PT-7`, `S4` — **non sono ID**: vivono dentro il loro documento.

---

## SI SCRIVE IN UN SOLO MODO

```
python csv/indice.py aggiorna ID --campo stato=SOSPESA --motivo "...cita il testo..."
python csv/indice.py aggiorna-lotto doc/indice/_lotti/<nome>.jsonl
python csv/indice.py crea-lotto    doc/indice/_lotti/<nome>.jsonl   # NASCE
python csv/indice.py storico-commit                              # il campo `commit`
python csv/indice.py segnali                                      # i PRESIDI
python csv/indice.py etichette-lotto doc/indice/_lotti/<nome>.jsonl  # le ETICHETTE
```

| | |
|---|---|
| ### **ogni modifica** | aggiunge una riga a **`doc/indice/storico.jsonl`**, che è **solo in aggiunta** |
| ### **il COMMIT della riga** | `commit_base` lo **timbra la via di scrittura** *(`HEAD` al momento in cui scrive)*; `commit` — il commit che **contiene** la riga — lo riempie **`storico-commit`** dai log, perché lo storico è **solo-in-aggiunta** e per ogni commit le righe `[prima, dopo)` sono **esattamente le sue**. ### ⚠ **Resta UN LOTTO DI RITARDO**, e non è una scelta: quando il lotto gira, ### **il commit che lo conterrà NON ESISTE ANCORA** |
| ### **il motivo CITA** | una frase della descrizione o della fonte. **Il lotto rifiuta un motivo sotto i `20` caratteri** |
| ### **si TOGLIE un metadato** | con **`meta_togli`** nel lotto, e **non svuotandolo**: `nota_guardiano` ha regex `^.{1,300}$` e **non ammette la stringa vuota**. ### ⭐ **Una domanda a cui si è risposto non si riscrive: si TOGLIE**, e la risposta vive nel campo che la porta *(`superata_da`)*. ### ⚠ **Togliere una chiave che non c'è è un ERRORE**, perché nasconderebbe uno sbaglio |
| ### **una voce NASCE** | solo con `crea-lotto`, e la sua riga di storico ha **`prima: null`**. ### ⚠ **Prima del 2026-10-09 non c'era**, e le voci nascevano **dentro la migrazione** — che gira una volta sola, dal tag: far nascere una voce dopo voleva dire **scrivere a mano in `voci.jsonl`**, cioè ### **una seconda via di scrittura** |
| ### **togliere da `etichette_rimosse`** | fa parte dello **stesso atto** di `crea-lotto`, perché `C1` pretende che ogni ID vecchio stia in ### **UNO E UNO SOLO** posto. ### **Non è pulizia: è la conservazione** |
| ### ⛔ **a mano, MAI** | e il validatore se ne accorge: le **viste** si confrontano con la fonte |
| ### **le viste** | `doc/INDICE_ID.tsv` *(compatibile, `15` colonne)*, `doc/INDICE.md`, `doc/indice/_indice_meta.json` *(indice invertito)*. **Tutte DERIVATE** |

**IL VALIDATORE:** `python csv/indice.py valida` *(e `collaudo`)*, e **gira da solo nel
`pre-commit`** — ma **solo se `voci.jsonl` esiste**, così si accende da sé.

---

## I METADATI, E LA REGOLA DI CONFINE

> **CAMPO FISSO** = serve a **OGNI** voce. **METADATO** = serve **ad alcune**.

Il registro è `doc/indice/metadati.jsonl`, e una voce usa in `meta` **solo** chiavi `ATTIVO`,
**col tipo giusto**, e **solo se rientra in `si_applica_a`**. Si tocca **solo** con
`meta-aggiungi`, `meta-depreca`, `meta-rinomina` — e **deprecare o rinominare MIGRA tutte le
voci** e lo registra.

### ⚠ **Un tetto di lunghezza su un testo CONSERVATO lo troncherebbe**, cioè farebbe la perdita
che il metadato esiste per evitare: `motivo_era1` e `revisione_era1` **non hanno tetto**, e il
primo che avevo scritto *(`1200`)* era **un numero scelto** *(`A11`)* che una voce da `1333`
caratteri ha fatto scattare.

---

## DOVE STA IL «PERCHE'» DI OGNI `SI`

`blocca = true` **non si dichiara a vuoto**: la prova vive in `meta.motivo_era1` per le voci
dell'era `1`, e **il validatore della vista la pretende**. ### ⚠ **E questo vincolo oggi vive
nel VALIDATORE, non nello schema:** se la vista cambiasse forma si perderebbe senza che nessuno
se ne accorga — **è un `A9` in attesa**, e sta scritto.

---

## UN ID NON E' UN NOME: E' UNA CHIAVE

Un **assioma** e uno **standard** non si rinominano mai; le etichette **locali** vivono col
namespace *(`REGISTRO_FISICA:V8`)*.

### ⛔ **E I REPERTI NON SI RISCRIVONO:** nei task history, nei referti, nei `json` e nei
messaggi il nome vecchio **resta**, e si risolve con l'**`alias`**. ### ➜ **La migrazione lo ha
fatto `10` volte**, sugli ID che contenevano **uno spazio** *(`STANDARD 6` → `STANDARD-6`, col
nome vecchio come alias)*; e ha scoperto che `STANDARD 5` e `STANDARD ⑤` erano **lo stesso
standard scritto in due modi**.

### ⚠ **E la colonna `alias` dell'era `1` NON conteneva alias:** `21` valori erano **ID di
altre voci** *(un **collegamento**, non un alias)* e `6` erano **condivisi fra due voci**
*(allora non è l'alias di nessuna)*. **Tutto tracciato in
`doc/indice/migrazione_era1.jsonl`.**

---

## I PRESIDI CONTRO LE MESCOLANZE — **segnalano, NON decidono** *(dal 2026-10-09)*

> ### ⛔ **Sono DETERMINISTICI e SEGNALANO: la decisione è di chi legge.** `python csv/indice.py segnali` dà la lista; `valida` ne stampa **il conteggio** e ### ⚠ **NON cambia il codice d'uscita** — un segnale che blocca **non è un segnale.**

| id | che cosa segnala |
|---|---|
| **`F1`** | **GEMELLE:** il **titolo** di una voce cita l'**ID di un'altra**, e **dominio o era differiscono** |
| **`F2`** | **ERA `2` PULITA:** una voce dell'era `2` che nomina **simboli dell'era `1`** *(`phivel`, `M_PH`, `mem_mot`, `Nose-Hoover`, `sync`…)*, **un numero di riga `:NNNN`**, o **un flag `--…`** |
| **`F3`** | **`FISICA` CHE PARLA DI STRUMENTI:** il **titolo** di una voce `FISICA` dice *sigillo, criterio, controllo positivo, caso che deve fallire, commento, docstring, README, hook, presidio, CRLF* |
| **`F4`** | **ETICHETTA CON DEFINIZIONE:** un'etichetta rimossa che un documento **DEFINISCE** *(riga di tabella o intestazione)*. ### ⚠ **Le VISTE GENERATE sono escluse**, perché una riga in `doc/LISTA_CHIUSA.md` **elenca** un ID, non lo definisce |
| ### ⛔ **`F5`** | **STORICO SENZA COMMIT: È UN ERRORE**, non un segnale, e sta in `valida`. ### ⚠ **Solo per le righe GIÀ COMMITTATE** *(quelle in `HEAD`)*: le altre sono **il ritardo** — nella forma letterale **bloccherebbe ogni commit di un lotto** |
| ⛔ **`F7`** | **LO STATO DI UNA VOCE DELL'ERA `1`: È UN ERRORE**, non un segnale, e sta in `valida`. `FISICA` + era `1` + stato diverso da `SOSPESA`/`CHIUSA`/**`SUPERATA`** *(### **`SUPERATA` sta con `CHIUSA`:** una voce superata da una decisione **non è aperta**, è risolta **da fuori**)* ⇒ **la validazione fallisce**. ### ⚠ **Nasce da un errore mio**, e il perché sta nel suo sorgente |
| **`F6`** | **NOTE COERENTI:** una `nota_guardiano` che **nomina una lista del guardiano** e la voce **non è più ciò che quella lista diceva**. ### ⚠ **Non legge la prosa**, e una nota che si dichiara *«correzione»* **non si guarda** |

### **UN SEGNALE SI CHIUDE IN DUE MODI SOLI:** **correggendo la voce**, oppure con ### **`meta.eccezione_presidio`** — forma obbligata **`F<n>: <motivo>`**, e il motivo deve contenere **un pezzo LETTERALE di almeno `20` caratteri** del testo della voce. ### ⛔ **La forma la impone `valida`:** senza quel controllo l'eccezione sarebbe **una via di fuga a costo zero.**

### **IL COLLAUDO:** `python csv/_collaudo_presidi_indice.py`, **`15` su `15`** — ogni presidio si è visto **SCATTARE** sul suo caso a risposta nota *(`P1-sexies`)* e **non scattare** sulla voce corretta. ### ⛔ **Su una COPIA letta con `git show`, mai sull'indice vero.**

---

## LA CLASSE `CRITERIO` È **UNA COSA SOLA** *(criterio del guardiano, 2026-10-09)*

> ### ⭐ **Un criterio DICE COME SI GIUDICA, quindi è `METODO`.**

Era **spaccata in due**: `71` voci `CRITERIO` in `FISICA` e `35` in `METODO`, e **gli stessi tipi di criterio** — *«caso che deve fallire»*, *«byte-identico»* — stavano **da tutte e due le parti.**

| | |
|---|---|
| ### **la regola** | `classe = CRITERIO` ⇒ `dominio = METODO`. ### ⚠ **`era` e `stato` NON si toccano** |
| ### **l'unica eccezione** | una voce il cui testo **non è un criterio ma un ESITO MISURATO** — *es. `REGISTRO_FISICA:P5`, «quasi COSTANTE, `0.74`-`0.76` LAM»* ⇒ classe **`MISURA`**, dominio **`FISICA`** |
| ### **come si riconosce un esito** | un numero o un intervallo **come risultato**, e ### **nessun verbo prescrittivo** *(«DEVE», «si verifica», «basta», «byte-identico», una soglia)*. ### ⛔ **`==` non è una misura: è un CONFRONTO** |
| ### ⛔ **la regola SELEZIONA, la lettura DECIDE** | i candidati li dà `python csv/_segnali_chiusura.py 2`; **la decisione sta nelle tabelle `DECISO_ESITO` e `DECISO_CRITERIO`**, e ### **ogni riga porta la frase che l'ha decisa.** `4` candidati sono stati **rifiutati leggendo** |
| ### **non è fisica** | è **un criterio di CLASSIFICAZIONE**, e il guardiano lo dichiara. Tutte le voci restano `SOSPESE` o `CHIUSE` ⇒ ### **non cambia nulla per l'era `2`, solo l'ordine** |
| ### ⚠ **il prezzo** | `FISICA` perde `58` voci *(da `439` a `381`)*, e chi legge i conteggi di ieri e di domani **deve trovare scritto perché** |

### **E il controllo `C3` conosce LA REGOLA, non i `6` ID** che oggi la esercitano: una voce `CRITERIO` si aspetta in `METODO` **qualunque cosa dicesse la lista del guardiano**, altrimenti il controllo andrebbe riscritto ogni volta che una voce diventa un criterio.

---

## QUANDO UN'INTESTAZIONE **DEFINISCE** UN ID *(regola di `F4`, 2026-10-09)*

> ### ⭐ **L'ID deve essere il SOGGETTO, e ci deve essere CONTENUTO.**

Si toglie dall'inizio della riga, **ripetutamente**: i `#`, gli spazi, i **simboli non alfanumerici** *(`⛔` `✅` `⚠` `⭐` `➜` `①` `*` backtick `—` `§`)*, la **numerazione** *(`5.`, `1.2`, `5-bis.`, `§38`)* e **una parola di stato** *(`APERTO`, `CHIUSO`, `APERTA`, `CHIUSA`, `RISOLTO`, `SOSPESO`)*.

| | |
|---|---|
| ### ✔ **è una definizione** | il resto **comincia con l'ID** *(e l'ID finisce dove finisce il token: `S1` non definisce `S10`)* ### **e c'è contenuto** — `3` caratteri dopo l'ID **oppure** una riga non vuota e non-intestazione **SOTTO** |
| ### ⚠ **il «**sotto**» serve** | `## APERTO CURA1-CORTO` ha l'intestazione **nuda** e il contenuto **nel paragrafo che segue**: *«senza contenuto»* vuol dire **niente, né accanto né sotto** |
| ### ⛔ **non è una definizione** | l'ID **dentro la prosa**: `### 1.2 ⚠ E LA LETTURA CHE DECIDE DAVVERO — dichiarata POST-HOC, non era fissata prima`. ### **`POST-HOC` è un aggettivo**, e `RI-LETTO`, `RI-VERIFICATI`, `SOVRA-CORREGGE` sono **verbi** |
| ### **le righe di tabella** | **non cambiano:** `\| `ID` \| …` resta una definizione |

### **Il collaudo ha i due casi che il mandato fissa** — `POST-HOC` **non deve** scattare, `TW-1` a `6e5e75b` **deve** — piu' **il braccio che prova che è LA REGOLA a zittirlo**: con la regola spenta, `POST-HOC` torna a segnalare.

### ⛔ **E `F4` SI FERMA AL PRIMO FILE**, quindi **non può dire se un ID è un OMONIMO.** Per quello c'è **`python csv/_cerca_definizioni.py`**, che cerca **TUTTE** le definizioni in **tutto il repo** — e che esclude i file che **parlano dell'indice** *(referti, task history, attrezzi, `par9.md`)*: ### ⭐ **un file che parla dell'indice ELENCA gli ID, non li DEFINISCE**, ed è **la terza volta** che questo falso-uno si presenta — dopo `doc/INDICE.md` *(il controllo `C4`)* e `doc/LISTA_CHIUSA.md` *(il ripasso del blocco `C`)*.

### **Un'etichetta NON ha un `meta`**, perché non è una voce: la sua eccezione e la sua nota stanno in **campi suoi**, scritti con **`etichette-lotto`** — la stessa via, con la sua riga di storico.

---

## LO STATO DI UNA VOCE DELL'ERA `1` *(regola in vigore, 2026-10-09)*

> ### ⭐ **La fisica dell'era `1` non chiusa è `SOSPESA`.**

| | |
|---|---|
| ### **`stato`** | lo stato **DI OGGI**: per una voce `FISICA`/era `1` può essere solo **`SOSPESA`**, **`CHIUSA`** o **`SUPERATA`** |
| ### **`stato_era_1`** | lo stato **che la voce aveva nell'era `1`**: è lì che va l'*«APERTO»* di un'intestazione come `## APERTO CURA1-CORTO` |
| ### ⛔ **il presidio** | **`F7`**, e **è un ERRORE, non un segnale**: `FISICA` + era `1` + stato diverso da `SOSPESA`/`CHIUSA`/**`SUPERATA`** *(### **`SUPERATA` sta con `CHIUSA`:** una voce superata da una decisione **non è aperta**, è risolta **da fuori**)* ⇒ **la validazione fallisce** |

### ⚠ **Da dove viene la regola:** nel giro del punto `5` avevo ripristinato `4` voci leggendo lo stato da `## APERTO <ID>`, e avevo **dichiarato la provenienza del dato** — ma l'avevo messo nel campo **sbagliato**. ### **Dichiarare da dove viene un dato non basta se lo si mette nel campo sbagliato**, e per questo la regola ha un presidio e non solo una riga.

---

## CIÒ SU CUI L'INDICE ASPETTA LUCA — **un elenco solo, e si GENERA** *(2026-10-09)*

> ### ⛔ **`python csv/indice.py da-decidere` → `doc/indice/DA_DECIDERE_LUCA.md`. NON si scrive a mano.**

| | il criterio | la domanda |
|---|---|---|
| ① | la `nota_guardiano` dice *«da decidere / confermare da Luca»* | **ciò che la nota stessa chiede** |
| ② | la voce ha **`meta.omonimo`** | **quale dei `N` significati?** |
| ③ | `stato = DA_CLASSIFICARE` **e la classe NON è `NON_DEFINITA`** | che classe, dominio, era e stato? |

### ⚠ **I segnaposto `NON_DEFINITA` NON ci vanno**, e sono `187`: non sono una domanda, sono **il lavoro che resta.**

### ⭐ **Perché GENERATO e non scritto:** nel codice **non c'è nessuna lista di ID**, ci sono **i tre criteri**, e l'elenco è ciò che trovano. ### ⛔ **Un elenco mezzo generato è peggio di nessun elenco, perché SEMBRA COMPLETO.**

---

## `F7` VALE PER **QUALSIASI DOMINIO** *(2026-10-09)*

> ### ⭐ **La regola non parlava di fisica: una voce dell'era `1` NON CHIUSA è `SOSPESA`**, e vale per `METODO`, `INFRASTRUTTURA` e `DOCUMENTAZIONE` come per `FISICA`.

### ⚠ **Violava su `16` voci** — le `14` `CENS-*`, `D32-CONTATORE` e `RAMI-OFF-CURA2` — e ### **sono state curate PRIMA che il presidio si accendesse**: ### ⛔ **un presidio bloccante acceso prima della cura rende inapplicabile il lotto che lo curerebbe**, perché la validazione gira **dentro `aggiorna-lotto`.**

---

## L'ERA DI UNA VOCE DI **METODO** O DI **STRUMENTI** *(criterio del guardiano, 2026-10-09)*

> ### ⛔ **Il guardiano dichiara che la regola precedente — «metodo = era `ENTRAMBE`» — era TROPPO GROSSA.**

| | |
|---|---|
| ### **`ENTRAMBE`** | una **REGOLA DI LAVORO** *(le `P*`, i presidi `H-*`)* o **uno strumento che SOPRAVVIVE** alla riscrittura |
| ### **era `1`** | ciò che riguarda un **OGGETTO CONCRETO dell'era `1`**: un **sigillo di una cura**, la **scena `(ii)`**, il **pilota**, un **`.pkl`**, il blob **`b8c21049`**, **una funzione o un flag di `soliton_simulator.py`** |

### ⚠ **`35` voci erano `ENTRAMBE` per INERZIA**, non per lettura: `era ENTRAMBE` passa da `173` a **`138`**. ### **Non è una decisione di fisica**, e tutte restano `SOSPESE`: **non cambia nulla per l'era `2`, solo l'ordine.**

### **Il presidio che lo guarda è `F8`, e SEGNALA**: una voce `ENTRAMBE` non `CHIUSA` che **nomina un oggetto concreto dell'era `1`**.
