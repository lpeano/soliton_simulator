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
