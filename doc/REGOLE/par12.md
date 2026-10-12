# dettaglio di `CLAUDE.md` par.12 — **i presidi automatici**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col
loro id. Non rimanda ad altri file di `doc/REGOLE/`.)*

## L'INSTALLAZIONE, e perche' va detta

```
git config core.hooksPath .githooks        # oppure: python csv/_hook_presidi.py --installa
```

Gli script stanno in **`.githooks/`**, che **e' TRACCIATO da git**; `.git/hooks/` **non lo e'**
e **non viaggia col repo**. `core.hooksPath` **SOSTITUISCE** quella cartella.
### ⚠ **Finche' quel comando non e' dato, i presidi NON impediscono niente** — e
`python csv/_hook_presidi.py` **lo dice a ogni invocazione** *(`A9`)*.

## I UNDICI HOOK, uno per uno

| id | stadio | che cosa **impedisce** |
|---|---|---|
| `H-P3` | `pre-commit` | un **sigillo** che configura il modulo **a mano** invece di passare dal CLI |
| `H-P5` | `pre-commit` | un **referto** che non dichiara **la configurazione INTERA** |
| `H-P7` | `pre-commit` | un **flag** il cui commento cambia senza nominare quel flag |
| `H-P8` | `pre-commit` | un confronto che prende **«il codice di prima» da `HEAD`** invece che dal PADRE |
| `H-VALIDATORE` | `pre-commit` | un **indice** mal formato, o con una voce persa rispetto al tag |
| `H-RIGHE` | `pre-commit` | **`CLAUDE.md` oltre le 400 righe** |
| `H-P1-bis` | `commit-msg` | un **referto** committato **senza toccare la relazione** |
| `H-REG-R` | `commit-msg` | una **legge** che cambia **senza la sua scheda** in `REGISTRO_FISICA` |
| `H-INDICE` | `commit-msg` | un **ID** aggiunto a un documento vivo o citato nel messaggio **che non e' nell'indice** |
| `H-FILE` | `commit-msg` | una lista **`FILE CAMBIATI`** che **non coincide** con `git diff --cached --name-only`, **o che manca** |
| `H-NON-TRACCIATI` | `commit-msg` | **file NON TRACCIATI e NON ignorati** sotto `csv/` o `doc/` |

## DA QUALE ERRORE E' NATO CIASCUNO

### **`H-FILE`** *(decisione di Luca, 2026-10-03)*: la regola *«la lista si genera da
`git diff --cached --name-only`»* era scritta da **due recidive** — `2ab4ce2` e `1d58764`,
entrambe con `doc/INDICE_ID_ESCLUSI.tsv` omesso. ### **E una regola scritta non e' un
presidio.** Il suo **primo atto** e' stato **scagionare** un commit: `1927b45` era stato
contestato come terza recidiva, e la lista del messaggio coincideva — `6` e `6`.

### **`H-NON-TRACCIATI`** *(decisione di Luca, 2026-10-04)*: il caso ha un nome,
**`_sonda_scherm`** — una sonda girata **fuori dal repo**, il referto committato e **lo
strumento no**. Il censimento ha misurato quanto sia comune: su **484** non tracciati, **98**
erano **CITATI** da un documento, da un referto o dall'inventario, cioe' **98 riferimenti al
vuoto**. ### **BLOCCA e non avvisa, perche' un avviso che nessuno legge e' `A9`.**

### **`H-P3`/`H-P5` e il prefisso `H-`:** il prefisso dice *«questo lo impedisce una
macchina»*, e cura una collisione reale — `P3` e `P5` erano **due regole diverse con lo stesso
nome**, la regola di metodo e il presidio del hook. ### **Lo stesso difetto che l'indice ha
curato per i difetti** *(`A3` era tre voci)*. **I nomi vecchi restano nell'indice** come
righe di rinomina, col rimando.

## LE VIE D'USCITA

| via d'uscita | dove si scrive |
|---|---|
| `[SENZA-RELAZIONE: …]` · `[SENZA-INDICE: …]` · `[CLAUDE-OLTRE-400: …]` · `[SENZA-FILE-CAMBIATI: …]` · `[SENZA-NON-TRACCIATI: …]` | nel **messaggio** di commit, **a INIZIO RIGA** |
| `# ESENTE-H-P5: <motivo>` *(e simili)* | in un **commento del file**, **e** elencata in `doc/ESENZIONI_presidi.md` (`python csv/_hook_presidi.py --elenca`) |

### ⛔ **A INIZIO RIGA, e per un difetto MISURATO:** cercando la stringa d'uscita in **tutto**
il testo, il commit che introduceva `H-FILE` e' passato **senza controllo** — il messaggio la
**CITAVA** nella tabella del collaudo. ### **Un presidio che si disarma parlando di se' non e'
un presidio.**

### ⚠ **E un'esenzione NON elencata fa fallire il commit comunque:** cosi' non se ne
accumulano di invisibili.

## `H-STASH`, che non e' un hook

| id | dove | che cosa **impedisce** |
|---|---|---|
| `H-STASH` | `.claude/settings.json` — `permissions.deny` | **`git stash`**, qualunque sua forma |

**Non ha il prefisso di un hook per caso:** e' una regola di **permesso**, quindi impedisce
**prima** che il comando parta, non al commit. ### **E non ha via d'uscita dichiarabile:** se
serve davvero, lo toglie **Luca**. ### **Caso che deve fallire, provato:** `git stash list`
risponde *«Permission to use Bash with command git stash list has been denied»*.

## IL LIMITE, per `A9`

I hook **non impediscono** cio' che **non guardano**. `H-P1-bis` guarda **i file toccati**,
non la chat: sulla forma allargata del par.4 **non puo' impedire nulla** — il presidio li' e'
la riga **`PUSHATO:`**, che Luca vede a colpo d'occhio.

---

## `H-FISICA-FUORI-LISTA`, e **la cartella che non scelgo io** *(2026-10-09)*

| | |
|---|---|
| ### **la LISTA** | `csv/_file_fisica.py::FILE_FISICA`, ### **l'unica fonte**: chi sorveglia la fisica la legge da lì. Prima **ogni presidio scriveva il nome a mano** |
| ### ⛔ **il perché** | il giorno in cui la fisica vive in due file, un presidio che scrive il nome a mano ### **guarda ancora UN FILE SOLO — e PASSA**, perché un presidio che guarda il posto sbagliato ### **non trova niente e tace** |
| ### **la CARTELLA dell'era `2`** | ### **VUOTA**, *«da decidere da Luca»*. ### ⚠ **Finché è vuota `H-FISICA-FUORI-LISTA` non impedisce niente** *(`A9`: è una tenda)*, e il collaudo gira ### **su una cartella di PROVA in una COPIA** |
| ### ⭐ **e mettere un file nella LISTA costa** | ciò che è nella lista è ### **soggetto a `H-REG-R`** *(nessuna legge senza la sua scheda)* ### **e a `H-P7`** *(il commento di ogni flag)*: ### **due presidi addosso** |
| ### ⚠ **il numero dei hook NON sta nel titolo del §`12`** | ce lo avevo messo, e il titolo ### **andava riscritto a ogni presidio nuovo** — e `csv/_struttura_regole.py` ### **vedeva un titolo sparire** |

---

## `H-ID-OBBLIGATORIO`: **il rovescio di `H-INDICE`** *(2026-10-09)*

| | |
|---|---|
| ### **la regola** | un commit che tocca ### **un file della LISTA** di `csv/_file_fisica.py`, o un ### **`doc/REFERTO_*` / `doc/REPERTO_*`**, ### **cita almeno un ID** dell'indice |
| ### **il perché** | la fisica che cambia ### **ha UNA VOCE che la spiega**, e un referto è ### **la risposta a una domanda** — e la domanda è una voce. ### **Un commit che cambia una legge senza citare un ID dice «ho cambiato una legge» e non dice quale problema stava risolvendo** |
| ### ⛔ **«un referto» è SOLO due prefissi** | `doc/REFERTO_*` e `doc/REPERTO_*`. ### **La mia definizione era «un file sotto `doc/`», cioè LARGA** — e una definizione larga in un presidio ### **rifiuta commit che nessuno voleva rifiutare** |
| ### **la via d'uscita** | `[SENZA-INDICE: <motivo>]`, ### **a inizio riga** — ### **la stessa di `H-INDICE`**, di proposito: chi dichiara di non avere ID da citare lo dichiara ### **una volta** |

---

## LA CARTELLA DELL'ERA `2` E' `primo_ordine/` *(decisione di Luca, 2026-10-09)*

| | |
|---|---|
| ### **la costante** | `csv/_file_fisica.py::CARTELLA_ERA_2 = "primo_ordine/"` |
| ### ✔ **e da questo momento `H-FISICA-FUORI-LISTA` IMPEDISCE** | finché la costante era `""` era ### **una TENDA** *(`A9`)*, e l'avevo dichiarato in ### **quattro posti** |
| ### ⚠ **la cartella NON esiste ancora, e NON l'ho creata** | il mandato dà ### **il nome**, non l'ordine di crearla — e creare la cartella del codice dell'era `2` è ### **un atto di FISICA**, non di indice |
| ### ⭐ **e il presidio funziona comunque** | guarda ### **i percorsi staged, non il disco**: impedisce ### **dal primo `.py` che qualcuno metta là** |
| ### **il collaudo** | sulla cartella ### **VERA**, nei due versi, piu' ### **una copia con la costante VUOTA** che conserva ### **la misura del vecchio stato** |

---

## `primo_ordine/`, E LA LISTA CHE SI SDOPPIA *(2026-10-09)*

| | |
|---|---|
| ### **`FILE_FISICA`** | ### **tutti** i file di fisica *(`13`)*. La leggono ### **`H-FISICA-FUORI-LISTA`** *(un `.py` sotto `primo_ordine/` fuori lista → commit rifiutato)* e ### **`H-ID-OBBLIGATORIO`** *(un ID nel messaggio)* |
| ### **`SCHEDA_NEL_REGISTRO`** *(nuova)* | ### **solo i file la cui SCHEDA vive in `doc/REGISTRO_FISICA.md`** *(`1`)*. La leggono ### **`H-REG-R`** e ### **`H-P7`** |
| ### ⛔ **perché due liste e non un sottoinsieme** | la scheda di una legge dell'era `2` ### **si GENERA in `doc/leggi_era2/<id>.md`**: pretendere che stia ### **anche** nel registro vorrebbe dire ### **DUE posti per la stessa scheda**, e ### **due copie divergono** |
| ### ⭐ **e l'`assert` chiedeva questo** | *«va esteso, non adattato»* — ### **un ciclo sarebbe stato l'adattamento**, la distinzione è ### **l'estensione** |

---

## `H-STOP-CODA`: IL PRESIDIO SULLO STOP *(mandato di Luca, 2026-10-12)*

| | |
|---|---|
| ### ⛔ **l'incidente, ed e' MIO** | la regola **`L-NON-FERMARSI-AL-CHECKPOINT`** era **scritta**, e **nello stesso giorno** mi sono fermato **due volte** dopo un commit senza proseguire. ### **Una regola scritta che non impedisce non e' un presidio** *(`A9`)* |
| ### **che cos'e', tecnicamente** | un **hook `Stop` di Claude Code** *(non un hook di git)*, registrato in **`.claude/settings.json`** -- lo stesso file di `H-STASH`, che e' **tracciato** |
| ### ⭐ **la decisione** | se c'e' **lavoro PRONTO** che **non aspetta una decisione di Luca**, **blocca la chiusura del turno NOMINANDO il pezzo successivo** |
| ### ✅ **il contratto, VERIFICATO e non supposto** | dalle stringhe del binario, **alla lettera**: *«For Stop/SubagentStop hooks, **check `stop_hook_active` in the input and return success while it's true**. Set `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` to raise this limit»* |
| ### ⛔ **e quel contratto mi ha trovato un DIFETTO** | la prima stesura **ignorava `stop_hook_active`**: il braccio `(3-ter)` del collaudo **sarebbe stato rosso**, ed e' il motivo per cui quel braccio esiste |
| ### ⚠ **DUE protezioni dai cicli, e sono DISTINTE** | `stop_hook_active` e' **del TURNO** ed e' il contratto; il promemoria del presidio e' **del COMMIT** *(la chiave e' `HEAD`)*, ed e' quello che il mandato chiede: **mai due volte senza un commit nuovo** |
| ### ⛔ **e il promemoria vive FUORI dal repo** | il mandato dice **<<legge soltanto>>**, e uno stato dentro il repo sarebbe **un file scritto a ogni turno** |
| ### ⛔ **perche' NON chiama `_presidio.avvia()`** | `avvia()` **STAMPA il timbro su stdout**, e qui **stdout e' il canale JSON del hook**: un timbro davanti alla graffa **romperebbe il JSON a ogni turno**. ### Quindi: **la riconfigurazione si', il timbro solo nel collaudo**, e l'uscita resta **ASCII puro per costruzione** -- **provato dal braccio `(5)`** |
| ### ⭐ **il braccio che vale piu' degli altri** | il `(7)` legge **`.claude/settings.json`** e pretende che la registrazione punti a **un file che ESISTE**: un percorso sbagliato sarebbe **un hook che falliva a vuoto a ogni turno senza dirlo**, cioe' **ancora `A9`** |
| ### ⚠ **il POSTO APERTO, dichiarato** | `args` e' forma **exec**, quindi **nessuna shell espande `CLAUDE_PROJECT_DIR`**, e che Claude Code lo espanda **li'** **non e' verificabile dai file installati**. ### Percio' la registrazione usa il **percorso relativo**, e lo script risolve la radice da **`__file__`** |
| ### ⚠ **IL LIMITE CHE RESTA** | **non ho trovato il nome esatto del campo d'uscita che blocca uno `Stop`** *(le occorrenze di `stopReason` nel bundle JS sono **lo schema MCP di sampling**)*. Lo script **emette le forme note insieme** piu' **il codice d'uscita `2`**, e ### **il collaudo prova che lo script DECIDE bene, non che Claude Code onori quel campo** |
| ### **il collaudo** | `python csv/_stop_coda.py --collaudo`, **9 bracci**, dichiarato in `primo_ordine/collauda.py` nel **`pre-commit`** |

---

## `P-E10`: UNA VARIABILE NON ENTRA SENZA LA SUA RIGA DI CONFRONTO *(mandato di Luca, 2026-10-12)*

| | |
|---|---|
| ### ⛔ **l'incidente, e sono TRE** | era il **terzo** disallineamento della stessa famiglia fra la tabella e il banco congelato. I primi due in `9429351` *(lo stato vive sulle **estremita'** e non sul nodo; i pezzi del passo **si compongono** invece di sommarsi)*, il terzo **`phi` reale contro `phi` complesso**. ### **Tutti e tre sono usciti UNO ALLA VOLTA mentre si scriveva il codice che li usava** |
| ### ⚠ **e la riga che lo chiede mi e' arrivata TRONCATA** | *<<Il presidio deve imp>>*. ### **L'ho segnalata invece di inventarla** *(in `doc/CODA_2026-10-12.md`)*, e Luca l'ha ridetta: *<<deve **IMPEDIRE** che una variabile nuova entri in tabella senza la sua riga di confronto, oppure senza la dichiarazione **NUOVA** con il punto della carta che la decide>>* |
| ### ⭐ **e <<IMPEDIRE>> E' la parola che conta** | e' la differenza fra **un collaudo** e **un presidio**: un collaudo dice *<<e' sbagliato>>* a chi lo fa girare, un presidio del `pre-commit` ### **rifiuta il commit**. ### **Era la cosa che non potevo indovinare** |
| **che cosa pretende** | per ogni variabile di `leggi.yaml`, una riga in `doc/CONFRONTO_tabella_banco.md` con uno dei **quattro** esiti del vocabolario **chiuso** *(`COINCIDE`, `ERRORE DI TRASCRIZIONE`, `CONFLITTO`, `MANCANTE`)*, **oppure** `NUOVA` **col punto della carta**, **oppure** `ORFANA` |
| ### ⛔ **perche' il punto della carta e non una frase** | *<<nuova>>* senza il punto che la decide e' **una variabile che nessuno ha deciso**, e `[[DECISIONE-VUOLE-UN-CAMPO]]` dice che una decisione che serve a un programma **vuole un CAMPO**. ### Qui il campo e' **il punto `F`/`A`**, e il presidio **lo cerca nella riga** |
| ### ✅ **e `ORFANA` si AMMETTE** | il mandato dice *<<si segnala e **non si toglie**: la decide Luca>>* |
| **il collaudo, nei DUE versi** | dentro il collaudo dei presidi dell'era `2`: il verso **sano** *(tace oggi)* e **TRE** casi che **devono scattare** -- una variabile **finta senza riga**, una `NUOVA` **senza il punto**, e il **documento che non c'e'** |
| ### ⭐ **e i casi cattivi si provano IN MEMORIA** | un presidio provato **modificando la fonte** lascerebbe danno se il collaudo morisse a meta'. ### E un braccio verifica che **il documento vero sia tornato al suo posto**: un collaudo che lasciasse il presidio **puntato altrove lo SPEGNEREBBE** |
| **il compagno eseguibile** | `primo_ordine/_collauda_confronto.py`: costruisce lo stato iniziale **con le funzioni del banco** e confronta `dtype`, forma e dove-vive. ### **`15`/`15`**, di cui **`4`** casi che devono fallire |
