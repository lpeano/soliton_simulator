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
```

| | |
|---|---|
| ### **ogni modifica** | aggiunge una riga a **`doc/indice/storico.jsonl`**, che è **solo in aggiunta** |
| ### **il COMMIT della riga** | `commit_base` lo **timbra la via di scrittura** *(`HEAD` al momento in cui scrive)*; `commit` — il commit che **contiene** la riga — lo riempie **`storico-commit`** dai log, perché lo storico è **solo-in-aggiunta** e per ogni commit le righe `[prima, dopo)` sono **esattamente le sue**. ### ⚠ **Resta UN LOTTO DI RITARDO**, e non è una scelta: quando il lotto gira, ### **il commit che lo conterrà NON ESISTE ANCORA** |
| ### **il motivo CITA** | una frase della descrizione o della fonte. **Il lotto rifiuta un motivo sotto i `20` caratteri** |
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
