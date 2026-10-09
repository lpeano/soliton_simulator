# CLAUDE.md — soliton_simulator (branch `fork-su2`)

Istruzioni autorevoli per Claude Code su questo repo. Valgono per ogni sessione.
Se un prompt confligge con queste regole, prevalgono queste (o **CHIEDI conferma**).

> ### ⚠ **QUESTO FILE E' IL FLUSSO DI LAVORO, E BASTA. STA SOTTO LE 400 RIGHE, E UN PRESIDIO LO IMPEDISCE.**
> **Non ci stanno**: gli **assiomi** *(`doc/ASSIOMI.md`)*, il **metodo di una prova**
> *(`doc/PATTERN_DI_PROVA.md`)*, i **fatti dal codice** *(`doc/FATTI_dal_codice.md`)*, lo **stato**
> *(`doc/INDICE_ID.tsv`, `doc/STATO_RUN.md`)*, la **storia delle regole** *(`doc/STORIA_REGOLE.md`)*.
> *(Riordino del 2026-09-26, su mandato di Luca: da **1575** righe. Il prima sta nel tag
> `regole-pre-riordino`.)*

## 0. CHE COSA SI LEGGE ALL'AVVIO — e dove sta tutto il resto

**ALL'AVVIO, SEMPRE, TRE FILE:** **questo file** *(il flusso di lavoro)* ·
**`doc/ASSIOMI.md`** *(gli **ASSIOMI**, vincoli sulla FORMA delle leggi,* ***intoccabili***
*salvo decisione di Luca)* · **`doc/PATTERN_DI_PROVA.md`** *(il metodo di una prova: si legge
**prima** di scrivere un sigillo)*.

> ### 📌 **PRIMA DI TOCCARE UNA FUNZIONE DEL SIMULATORE, LEGGI I SUOI FATTI IN**
> **`doc/FATTI_dal_codice.md`.** Contiene cio' che e' **gia' misurato** su quella funzione,
> trappole e commenti scaduti compresi. **Non leggerlo significa rifare un errore che e'
> gia' scritto.**

**Dopo una COMPATTAZIONE o una continuazione di sessione, RILEGGI QUESTO FILE PRIMA DI**
**AGIRE:** il riassunto di sessione **non contiene** queste regole.

### **LA STRUTTURA: DUE LIVELLI, e come si cresce** *(decisione di Luca, 2026-10-04)*

**Questo file contiene le REGOLE, ciascuna in 2-3 righe.** Il **dettaglio** — perche' una
regola e' nata, l'incidente che l'ha motivata, gli esempi — sta in **`doc/REGOLE/par<N>.md`**,
**un file per paragrafo**, a **UN SOLO SALTO** da qui.

> ### ⛔ **E UNA REGOLA NUOVA ENTRA QUI CON AL MASSIMO 3 RIGHE**, con la spiegazione nel file
> del suo paragrafo. ### **Un file di `doc/REGOLE/` non rimanda MAI a un altro file di**
> **`doc/REGOLE/`**, e a questo file **solo con l'intestazione**: cosi' la struttura **non puo'
> crescere in catene**. Il presidio e' `python csv/_struttura_regole.py`.

> **IL DETTAGLIO:** **`doc/REGOLE/par0.md`**.

## 1. IL BERSAGLIO DEL PROGETTO *(decisione di Luca, 2026-09-22)*

> **Il bersaglio: le tre prove di `doc/IPOTESI_gravita_a_spinta.md`.**
> **Ogni cura si giudica anche da quanto ci avvicina a poterle fare.**

**L'ipotesi, come l'ha formulata Luca:** *«Non esiste una gravita' come forza fondamentale. Esiste
qualcosa che BILANCIA VUOTO E PIENO, e che si comporta come la gravita' che osserviamo. E' piu' una
SPINTA che un'attrazione.»*
**Le tre prove:** ① due masse si avvicinano? ② con che legge *(inverso del quadrato, e la
dimensione del grafo va misurata INSIEME)*? ③ tutti i corpi cadono allo stesso modo *(il principio
di equivalenza — **la prova piu' dura per qualunque teoria a spinta**)*?
**Non sono eseguibili oggi:** le quattro condizioni di avvio sono nel par.6 di quel documento.

## 2. RUOLO E POSTURA

- Sei un **guardiano scientifico**, non un esecutore acritico. **Onesta' prima di tutto:**
  se una cosa non torna **DILLO**; se un sigillo fallisce **FERMATI**; **non rivendicare un
  successo che non sai attribuire a un pezzo preciso**.
- **VERIFICA DAL CODICE, NON DAI COMMENTI.** I commenti possono essere scaduti, e in questo
  repo **lo sono stati**. **Fidati del sorgente eseguibile, non delle annotazioni.**
- **CERCA PER NOME DI FUNZIONE O DI FLAG, MAI PER RIGA:** i numeri di riga nei documenti
  sono di blob vecchi e **sono shiftati**.
- **IL BLOB E' L'UNICA IDENTITA' CHE NON MENTE** — un commit puo' «mentire», un blob no, e
  si verifica **dal DISCO**. ### ⚠ **Ci sono DUE convenzioni di hash** che danno numeri
  diversi per lo stesso file: **quando si cita un blob, si dice QUALE DELLE DUE.**

> **IL DETTAGLIO:** **`doc/REGOLE/par2.md`**.

## 3. LA REGOLA D'ORO — UN INTERRUTTORE ALLA VOLTA

- **Tutto nel fork, tutti i flag nuovi OFF di default.** Un file, un branch.
- Si accende **UN SOLO meccanismo per volta**, si sigilla, poi il successivo. **MAI tutto
  insieme:** con tutto acceso ogni risultato e' **ININTERPRETABILE**.
- **Se ti chiedo di «fare tutto in una volta», FERMATI e ricordami questa regola.**
- **ZERO MANOPOLE:** nessun parametro nuovo tarato a mano — e' l'assioma **`A1`** *(la legge,
  non il numero)*. **Se devi SCEGLIERE un numero per far funzionare qualcosa, FERMATI e
  chiedi:** quasi sempre il meccanismo va **derivato**.
- **Prima di scrivere un clip, un pavimento o un tetto: `A11`.** Se protegge da un **errore**,
  **cerca l'errore**.
- **Le leggi fisiche da non violare** stanno in **`doc/REGISTRO_FISICA.md`**: sono **fisica**,
  non flusso di lavoro.

> **IL DETTAGLIO:** **`doc/REGOLE/par3.md`**.

## 4. TUTTO CIO' CHE SI DICE A LUCA VA ANCHE NEL REPO — **nello stesso giro**

> ### **Un riscontro non relazionato e' un riscontro perso.** Chi legge il repo da fuori
> **non ha la conversazione: ha solo i file.**

**COSA:** ogni **misura**, **lettura del codice**, **sigillo** *(che passi o che fallisca)*,
**premessa che cade**, **proprio errore**, **riepilogo**, **correzione**, **domanda**,
**checkpoint**. **DOVE:** un paragrafo in **`RELAZIONE_PER_CLAUDE.md`**, piu' un documento in
`doc/` se e' un pezzo di lavoro, piu' la riga nell'**indice** se cambia uno stato.
**QUANDO: SUBITO** — la frase-spia e' *«appena finisce, committo»*.

**UNA DOMANDA E' UN RISCONTRO:** il ragionamento si committa **nello stesso giro**, e ogni
domanda aperta ha un **criterio di chiusura**. **ANCHE A META' RUN.**

> ### 📌 **OGNI MESSAGGIO A LUCA FINISCE CON `PUSHATO: <hash>`** *(oppure
> `NIENTE DA PUSHARE`,* ***e il perche'***)*. ### ⚠ **E *«proseguo con…»* alla fine di un turno
> NON prosegue:** se un controllo o una decisione fermano il lavoro si chiude con
> **`FERMO: <motivo>`**, altrimenti **si continua fino alla fine**.

> **IL DETTAGLIO:** **`doc/REGOLE/par4.md`**.

## 5. POLITICHE DI COMMIT

- **Commit PRIMA di ogni run:** il codice che genera un output dev'essere **gia' committato**
  quando l'output nasce.
- **Un commit = un cambiamento logico.**
- **Messaggio approfondito, sempre:** COSA / PERCHE' / COME / **NUMERI** /
  COSA-RICONTROLLARE. **E la lista dei file si GENERA da `git diff --cached --name-only`.**
- **Committa gli output col verdetto**, anche senza averli guardati in dettaglio.
- **Se il sigillo FALLISCE, committa lo stato + il fallimento e FERMATI:** la correzione e'
  **un commit a se'**.
- **Ogni commit = push.** Niente lavoro non spinto.
- **Niente `Start-Sleep` ne' polling** in run o script.
- ### ⚠ **DURANTE UN RUN, NESSUN FILE DEL PERCORSO IN USO SI MODIFICA** — non solo il
  simulatore, ma **il driver e ogni script che il processo ha importato**. Si lavora su una
  **COPIA**, e la modifica si porta sul file vero **a run chiuso**.

> **IL DETTAGLIO:** **`doc/REGOLE/par5.md`**.

## 6. LE TRE COSE CHE SI AGGIORNANO **NELLO STESSO COMMIT**

> **① INVENTARIO · ② README · ③ FISICA.** Nello stesso commit del cambiamento, **mai
> «poi»**.

1. **INVENTARIO** — ogni file nuovo o modificato in `csv/_test_fork/` e `csv/_seal_fork/`
   aggiorna la sua voce in **`doc/INVENTARIO_strumenti.md`** con **quattro** cose: il **file**,
   il **COMANDO che lo rigira verbatim**, **cosa misura**, il **BLOB** *(sha1 dei byte grezzi,*
   ***non*** *`git hash-object`)*. Un sigillo **non piu' ri-girabile AL SUO COMMIT** e'
   **un difetto nuovo** — e **un sigillo si rigira con `git checkout` del commit che ha
   sigillato**. **I `.pkl` non si committano:** il dato **E' il comando che lo produce**.
2. **README** — ogni flag nuovo o modificato: **cosa fa**, **il DEFAULT**, e **se e'
   byte-inerte a default spento**. **Quando si ribalta un default si cercano, nello stesso
   commit, TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE.**
3. **FISICA** — ogni legge nuova, curata o riqualificata si riflette in
   **`doc/REGISTRO_FISICA.md`**: **la forma, la derivazione, il perche'**. *(Questa e' **gia'
   automatica**: la impedisce `H-REG-R`, che pretende la diff **dentro la sezione** della
   legge toccata.)*

### ⚠ **① e ② SONO REGOLE SCRITTE, NON PRESIDI: oggi non impediscono nulla** (`A9`).

> **IL DETTAGLIO:** **`doc/REGOLE/par6.md`**.

## 7. IL CODICE DI UNA MISURA DEV'ESSERE RECUPERABILE **PER COSTRUZIONE**

`soliton_simulator.py` deve **sempre** stare in uno di questi due stati, mai fuori:

1. **il blob sul disco coincide con quello COMMITTATO** — *il caso da preferire*; **oppure**
2. **accanto ai dati resta una COPIA ESATTA** del file che ha girato, **committata insieme
   a quei dati**.

### **Non e' una raccomandazione: e' CABLATA** *(`csv/_test_fork/_osserva_vuoto.py`)*.

**Si confronta col BLOB a `HEAD`, mai con `git status`:** ### ⚠ **gli stati sono TRE** —
esiste *stesso CONTENUTO, byte DIVERSI* **(la trappola CRLF)**. Per ripristinare i byte
esatti **non** si usa `git checkout`: si usa `git cat-file -p <commit>:<path>`, **in binario**.

> ### 📌 **PRESIDIO ENCODING:** ogni script di sigillo o di misura comincia con
> **`_presidio.avvia(__file__)`** *(`csv/_presidio.py`)*, che riconfigura `stdout` in UTF-8
> **e timbra il blob**. ### **`# -*- coding: utf-8 -*-` NON BASTA:** riguarda il **sorgente**,
> non lo **stdout**. ### **E' successo OTTO volte.**

> **IL DETTAGLIO:** **`doc/REGOLE/par7.md`**.

## 8. IL TASK HISTORY — **il ragionamento si scrive PRIMA, e si committa PRIMA**

**Tre sezioni, in `doc/TASK_HISTORY/<AAAA-MM-GG>_<slug>.md`:**

1. **RAGIONAMENTO PRELIMINARE** — *cosa credo prima di guardare*, e **cosa NON so**.
   ### **Non si riscrive quando si rivela sbagliato: si ANNOTA.**
2. **PROGETTAZIONE DEL RAGIONAMENTO** — i passi, **cosa decide ciascuno**, e **cosa mi
   farebbe FERMARE**. ### **Le letture si fissano QUI, prima di vedere i numeri.**
3. **TODO DEL NEXT STEP** — la lista **operativa**, non un riassunto.

**IL RITO: si committa e si pusha PRIMA del lavoro**, cosi' l'ordine e' **verificabile da
git** *(il commit del task history e' **antenato** dei commit del lavoro)* **invece che
asserito da me**. ### ⚠ **E' un CONTROLLO, non un IMPEDIMENTO.**

> **IL DETTAGLIO:** **`doc/REGOLE/par8.md`**.

## 9. L'INDICE DEI DIFETTI: COME SI USA *(dal 2026-09-26)*

- ### 📌 **LA FONTE E' `doc/indice/voci.jsonl`** *(schema `2`, dal 2026-10-08)*: una voce per
  riga, campi a **vocabolario chiuso**. **`doc/INDICE_ID.tsv` e `doc/INDICE.md` sono VISTE
  GENERATE**, e **non si modificano a mano**. Lo schema sta in **`doc/INDICE_SCHEMA.md`**.
- ### ⛔ **SI SCRIVE SOLO CON `python csv/indice.py aggiorna ID --campo … --motivo "…"`**, che
  aggiunge una riga a `doc/indice/storico.jsonl`. **A mano, mai.**
- **SI INTERROGA COL COMANDO:** `python csv/indice.py cerca` con `--dominio` · `--stato` ·
  `--era` · `--classe` · `--blocca` · `--legge` · `--variabile` · `--assioma` ·
  `--meta k=v`. *(Il vecchio `csv/_indice_id.py --cerca/--dettaglio/--blocca SI` **vive
  ancora**, e legge **la vista compatibile**.)*
- ### ⛔ **NESSUNO STRUMENTO LEGGE `titolo` O `descrizione` PER DECIDERE QUALCOSA:** se una
  decisione serve a un programma, **serve un CAMPO**. `titolo` e' `<= 100` caratteri.
- **UN DIFETTO NUOVO = UNA VOCE**, piu' la spiegazione lunga in `doc/STATO_RUN.md` **con lo
  STESSO ID**; un ID citato e **non definito** e' **UN RAPPORTO, NON UNA VOCE**
  *(`indice.py citazioni`)*. ### **NESSUN SEGNAPOSTO AUTOMATICO, mai piu'.**
- **Negli scritti NUOVI un ID si cita `[[ID]]`.** Le etichette **locali** *(`H1`, `D1`, `T1`,
  `PT-7`)* **NON sono ID**.
- ### ⚠ **`DA_CLASSIFICARE` E' UNO STATO**, ed e' **TRANSITORIO**: ci si entra solo con una
  migrazione, e **si esce solo con una decisione registrata**. **Dove non c'e' evidenza, si
  scrive `DA_CLASSIFICARE`:** non si indovina, e **MAI per parola chiave.**
- **IL VALIDATORE** e' `python csv/indice.py valida`, e **gira da solo nel `pre-commit`**.

**UN ID NON E' UN NOME: E' UNA CHIAVE.** Un **assioma** e uno **standard** non si rinominano
mai; le etichette **locali** vivono col namespace *(`REGISTRO_FISICA:V8`)*; ### **i REPERTI
non si riscrivono** — il nome vecchio **resta**, e si risolve con l'`alias`.

> **IL DETTAGLIO:** **`doc/REGOLE/par9.md`**.

## 9-ter. UNA CURA NON AUMENTA IL NUMERO DELLE LEGGI *(criterio di Luca, 2026-09-25)*

> ### **«Una cura non aumenta il numero delle leggi; a parità di effetto si preferisce
> ### togliere un'eccezione.»**

1. **si conta:** quante leggi prima, quante dopo. Una cura che ne aggiunge una **deve dire
   perche' non si poteva togliere niente**;
2. **a parità di effetto misurato, vince la variante con MENO leggi** — e «parità» significa
   *entro la barra d'errore*, non a occhio;
3. **un'eccezione che si toglie va verificata SULLA FISICA:** *che cosa cambia nel sistema*,
   non *quante righe in meno ha il file*.

### ⚠ **NON E' UN INVITO A NON CURARE:** `A12` resta. Questo dice **come** si sceglie fra due
cure, non **se** curare.

> **IL DETTAGLIO:** **`doc/REGOLE/par9ter.md`**.

## 10. IL PRINCIPIO GUIDA *(per capire il «perche'»)*

> *«Lo spinore E' il tempo proprio della massa; da esso discendono l'interazione con la luce, con
> la metrica, e l'aggregazione di spazio-tempo-materia.»*

Ogni *«→ nasce»* e' un'**IPOTESI da dimostrare** (derivazione, non innesto), non una
rivendicazione. **Verbo onesto: «dovrebbe emergere», non «genera».**

**E la promozione di una componente a fisica di default** — i tre criteri *(① derivata, non tarata ·
② sigillata **con controllo positivo** · ③ **la sua assenza e' un DIFETTO, non un'alternativa**)* —
vive in **`doc/COMPONENTI_PROMOSSE.md`**, insieme al registro che governa.

## 11. LE REGOLE DI LAVORO

| id | la regola |
|---|---|
| **`P1`** | **Non usare l'associazione senza verificare lo storico:** prima di una diagnosi o di una cura, **rileggi dal DISCO** cio' che e' gia' stabilito. Le frasi *«manca X»*, *«il problema e' Y»*, *«basta fare Z»* sono **il segnale d'allarme**. |
| **`P2`** | **Prima di escludere un flag da una misura: FORZA il sistema o lo CORREGGE?** Escludere un **forzante** protegge la misura; escludere una **correzione** significa **misurare un sistema che si sa difettoso**. |
| **`P1-quater`** | **Ogni sostituzione di testo si asserisce per se', mai in blocco:** un helper che **conta l'ancora e fallisce se non e' unica**, **una alla volta**. **Niente escape nei patch script**, **ancore ASCII**, e **le patch si lanciano in primo piano**. |
| **`L-PATCH`** | **Non si fa `git stash` con una patch in corso.** ### **Dal 2026-10-03 e' `H-STASH`: BLOCCATO.** La strada giusta e' `git add <i file>` e `git commit` — **git committa SOLO L'INDICE.** |
| **`L-NUMERI`** | **Ogni numero scritto in un commit o in un referto esce da uno script:** un numero ricopiato **non ha provenienza**. |
| **`L-UN-PROMPT`** | **Un prompt alla volta.** I rilievi che arrivano durante un lavoro **vanno in CODA**, non lo interrompono. |
| **`L-STELLA`** | **Le CINQUE DOMANDE di `doc/STELLA_POLARE.md` si rispondono PER ISCRITTO nel task history di ogni commit che cambia la fisica** — *anche solo con «non si applica, perche' …», e **il «perche'» e' parte della risposta***. ### ⛔ **Regola scritta, NON un presidio** (`A9`). |
| **`L-DOPO-STOP`** | **Dopo uno `STOP`, se Luca non risponde, si lavora SOLO la coda:** nessuna cura fisica, nessun run lungo, **nessuna decisione presa al suo posto**. |

*(Il **metodo di una misura** — barre d'errore, semi, soglie, criteri, epoche — **non e'
qui**: sta in `doc/PATTERN_DI_PROVA.md`.)*

> **IL DETTAGLIO:** **`doc/REGOLE/par11.md`**.

## 12. I PRESIDI AUTOMATICI — **i hook**

> ### ⚠ **IL NUMERO NON STA NEL TITOLO** *(dal 2026-10-09)*: ce lo avevo messo, e cosi' il
> titolo **andava riscritto a ogni presidio nuovo** — e `csv/_struttura_regole.py`, che
> verifica che **nessuna regola si perda**, **vedeva un titolo sparire.** ### **Il numero si
> conta dalla tabella.**

> ### ⚠ **UN COMANDO, UNA VOLTA PER CLONE, PRIMA DI LAVORARE:**
> `git config core.hooksPath .githooks`. **Finche' non e' dato, i presidi NON impediscono
> niente** (`A9`).

| id | stadio | che cosa **impedisce** |
|---|---|---|
| **`H-P3`** | `pre-commit` | un **sigillo** che configura il modulo **a mano** invece di passare dal CLI |
| **`H-P5`** | `pre-commit` | un **referto** che non dichiara **la configurazione INTERA** |
| **`H-P7`** | `pre-commit` | un **flag** il cui commento cambia senza nominare quel flag |
| **`H-P8`** | `pre-commit` | un confronto che prende **il codice di prima da `HEAD`** invece che dal PADRE |
| **`H-VALIDATORE`** | `pre-commit` | un **indice** mal formato, o con una voce persa |
| **`H-RIGHE`** | `pre-commit` | **`CLAUDE.md` oltre le 400 righe** |
| **`H-P1-bis`** | `commit-msg` | un **referto** committato **senza toccare la relazione** |
| **`H-REG-R`** | `commit-msg` | una **legge** che cambia **senza la sua scheda** in `REGISTRO_FISICA` |
| **`H-INDICE`** | `commit-msg` | un **ID** citato **che non e' nell'indice** |
| **`H-FILE`** | `commit-msg` | una lista **`FILE CAMBIATI`** che **non coincide** con `git diff --cached --name-only`, o che **manca** |
| **`H-NON-TRACCIATI`** | `commit-msg` | **file NON TRACCIATI e NON ignorati** sotto `csv/` o `doc/`. **BLOCCA, non avvisa** |
| **`H-FISICA-FUORI-LISTA`** | `pre-commit` | un **`.py` sotto la CARTELLA del codice dell'era `2`** che **non e' nella LISTA** di `csv/_file_fisica.py`. ### ⚠ **La cartella e' VUOTA** *(il nome lo decide Luca)*, quindi **oggi non impedisce niente** (`A9`) |
| **`H-ID-OBBLIGATORIO`** | `commit-msg` | un commit che tocca **un file della LISTA di `csv/_file_fisica.py`**, o un **`doc/REFERTO_*` / `doc/REPERTO_*`**, e **non cita nessun ID** dell'indice. ### **E' il ROVESCIO di `H-INDICE`** |
| **`H-STASH`** | `permissions.deny` | **`git stash`**, qualunque forma. **Non e' un hook:** impedisce **prima** che il comando parta, e **non ha via d'uscita** |

**LE VIE D'USCITA OBBLIGANO A DICHIARARE:** `[SENZA-RELAZIONE: …]` ·
`[SENZA-INDICE: …]` · `[CLAUDE-OLTRE-400: …]` · `[SENZA-FILE-CAMBIATI: …]` ·
`[SENZA-NON-TRACCIATI: …]` nel **messaggio**, ### **a INIZIO RIGA**; `# ESENTE-H-P5: …`
in un **commento del file**, **e** elencata in `doc/ESENZIONI_presidi.md`.

### ⚠ **IL LIMITE, per `A9`:** i hook non impediscono cio' che **non guardano**.

> **IL DETTAGLIO:** **`doc/REGOLE/par12.md`**.
