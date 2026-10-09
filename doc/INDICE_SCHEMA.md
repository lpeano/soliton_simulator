# LO SCHEMA DELL'INDICE — **`schema_version = 2`** *(decisione di Luca, 2026-10-08)*

> ### ⛔ **PERCHÉ ESISTE.** Lo schema `1` *(un TSV con `15` colonne)* teneva **in TESTO LIBERO**
> tre cose che gli strumenti devono **decidere**: che cosa è una voce, a quale ambito
> appartiene, e in che stato è. ### ➜ **La sospensione di `9f23313` ha classificato
> `METODO`/`FISICA` con PAROLE CHIAVE nel titolo, e ha sbagliato in quattro modi**, misurati
> dalla verifica del guardiano su tutte le `953` voci:
>
> | | |
> |---|--:|
> | segnaposto *«(CITATO N volte, MAI definito in un registro)»* trattati come voci | **`317`** |
> | «`METODO`» che sono **fisica dell'era `1`** | ~**`50`** |
> | lezioni di **metodo/infrastruttura** sospese per sbaglio | ~**`45`** |
> | voci del **programma dell'era `2`** sospese | ~**`40`** |
>
> ### ➜ **La causa non è l'euristica: è che l'indice NON AVEVA UN CAMPO per dirlo.**

---

# ⭐ `①` **IL FORMATO**

| | |
|---|---|
| ### **la FONTE** | ### **`doc/indice/voci.jsonl`** — una voce per riga, chiavi in ### **ordine fisso**, righe ordinate per `id` |
| i ### **registri dei vocabolari** | `doc/indice/leggi.jsonl` · `variabili.jsonl` · `assiomi.jsonl` · `decisioni.jsonl` · `metadati.jsonl` |
| i ### **derivati** | `doc/indice/_indice_meta.json` *(indice invertito)*, `doc/INDICE_ID.tsv` *(vista compatibile)*, `doc/INDICE.md` |
| ### ⛔ **ogni altra forma è una VISTA GENERATA** | `TSV` e `markdown` ### **non si modificano a mano**, mai. Il validatore se ne accorge |

### ⛔ **UNA SOLA VIA DI SCRITTURA:** `python csv/indice.py aggiorna …` *(o `aggiorna-lotto`, `crea-lotto` per far NASCERE una voce, `storico-commit` che riempie il campo `commit` dai log, e `segnali` per i **presidi contro le mescolanze**: ### **sono la stessa via** — stesse asserzioni, una riga di storico per voce, ### **una validazione alla fine e se non passa non si scrive niente**)*. Ogni modifica aggiunge
una riga a **`doc/indice/storico.jsonl`** *(**solo in aggiunta**: non si riscrive e non si
cancella)*.

---

# ⭐ `②` **I CAMPI FISSI** — *servono a OGNI voce*

| campo | tipo | |
|---|---|---|
| `id` | `^[A-Z0-9][A-Za-z0-9:_./()\[\]-]*$` | ### **unico**. ### ⚠ **La regex è larga PER UNA REGOLA:** *«i reperti non si riscrivono»* — `96` ID dell'era `1` hanno minuscole o punteggiatura *(`A2b`, `H-P1-bis`, `COMPONENTI:S3b`, `CONFIG-1/`, `INERZIA-1(C)`)*, e rifiutarli voleva dire ### **rinominarli**. Pretende ### **la maiuscola iniziale** e vieta ### **lo spazio** |
| `alias` | lista di id | i nomi vecchi, che ### **non si riscrivono mai** |
| `titolo` | ≤ `100` caratteri | ### ⛔ **SOLO PER UMANI** |
| `descrizione` | testo libero | ### ⛔ **SOLO PER UMANI** |
| `classe` | enum | `DIFETTO` `CURA` `MISURA` `CRITERIO` `PRESIDIO` `STANDARD` `TEORIA` `DECISIONE` `FRONTE` |
| `dominio` | enum | `FISICA` `METODO` `INFRASTRUTTURA` `DOCUMENTAZIONE` `DA_CLASSIFICARE` |
| `era` | enum | `1` `2` `ENTRAMBE` `DA_CLASSIFICARE` |
| `stato` | enum | `APERTA` `IN_CORSO` `CHIUSA` `SOSPESA` `SUPERATA` `AGENDA` `DA_CLASSIFICARE` |
| `blocca` | bool | blocca le corse base |
| `leggi` | lista di id | ### **da `leggi.jsonl`** |
| `variabili` | lista di id | ### **da `variabili.jsonl`** |
| `assiomi` | lista di id | ### **da `assiomi.jsonl`** |
| `collegate` | lista di id | altre voci |
| `padre` | id di voce *(o `""`)* | per i criteri locali |
| `superata_da` | id di decisione o assioma | ### **obbligatorio se `stato = SUPERATA`** |
| `chiusura` | `{criterio, commit, data}` | ### **obbligatorio se `stato = CHIUSA`** |
| `fonte` | `percorso::ancora` | ### **l'ancora è un NOME, mai una riga** |
| `creata`, `aggiornata` | `{data, commit}` | |
| `stato_era_1` | testo | lo stato al tag `era-1-secondo-ordine`. ### **obbligatorio se `stato = SOSPESA`** |
| `meta` | mappa | ### **solo chiavi del registro**, vedi `④` |

### ⛔ **LA REGOLA CHE TIENE IN PIEDI TUTTO:**

> ### **NESSUNO strumento legge `titolo` o `descrizione` per decidere qualcosa.**
> ### ➜ **Se una decisione serve a un programma, serve un CAMPO.**

---

# ⛔ `③` **GLI STATI: le TRANSIZIONI AMMESSE e i CAMPI OBBLIGATORI**

| da ↓ / a → | `APERTA` | `IN_CORSO` | `SOSPESA` | `AGENDA` | `CHIUSA` | `SUPERATA` | `DA_CLASSIFICARE` |
|---|---|---|---|---|---|---|---|
| `DA_CLASSIFICARE` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | — |
| `APERTA` | — | ✔ | ✔ | ✔ | ✔ | ✔ | ### ⛔ **no** |
| `IN_CORSO` | ✔ | — | ✔ | ✔ | ✔ | ✔ | ### ⛔ **no** |
| `SOSPESA` | ✔ | ✔ | — | ✔ | ✔ | ✔ | ### ⛔ **no** |
| `AGENDA` | ✔ | ✔ | ✔ | — | ✔ | ✔ | ### ⛔ **no** |
| `CHIUSA` | ✔ | — | — | — | — | ✔ | ### ⛔ **no** |
| `SUPERATA` | ✔ | — | — | — | — | — | ### ⛔ **no** |

### ⭐ **`DA_CLASSIFICARE` È TRANSITORIO, e la tavola lo impone:** ci si **entra solo alla
migrazione** *(nessuna transizione lo raggiunge)* e **si esce con una decisione registrata** —
una riga nello `storico.jsonl` col suo `--motivo`.

### **I CAMPI OBBLIGATORI PER STATO**

| stato | pretende |
|---|---|
| `CHIUSA` | `chiusura.criterio` **e** `chiusura.commit` |
| `SUPERATA` | `superata_da`, che deve essere ### **un id di `decisioni.jsonl` o di `assiomi.jsonl`** |
| `SOSPESA` | `stato_era_1` ### **non vuoto** |
| `DA_CLASSIFICARE` | ### **nessuno** — ed è il punto: è lo stato di chi ### **non sa** |

### ⚠ **E DUE COERENZE che il validatore pretende:** `blocca = true` è ### **incompatibile**
con `CHIUSA` e `SUPERATA`; `dominio = DA_CLASSIFICARE` ### **implica** `stato` o `era`
`DA_CLASSIFICARE` *(non si può sapere lo stato di una voce di cui non si sa l'ambito)*.

---

# ⭐ `④` **I METADATI** — *«l'indice deve poter ricevere metadati nuovi senza tornare al testo
libero»* *(decisione di Luca)*

### **LA REGOLA DI CONFINE, e decide da sola:**

> | | |
> |---|---|
> | ### **CAMPO FISSO** | serve a ### **OGNI** voce |
> | ### **METADATO** | serve ### **ad alcune** |

### **IL REGISTRO è `doc/indice/metadati.jsonl`**, e una voce usa in `meta` **solo** chiavi
`ATTIVO`, **col tipo giusto**, e **solo se rientra in `si_applica_a`**.

| campo del registro | |
|---|---|
| `chiave` | `^[a-z][a-z0-9_]*$` |
| `tipo` | `enum` `bool` `intero` `reale` `data` `testo_breve` `id_voce` `id_legge` `id_variabile` `id_assioma` `id_decisione` `sha_commit` `sha_blob` `lista_di:<tipo>` |
| `valori` / `regex` | il vocabolario chiuso, o la forma |
| `si_applica_a` | `{classi: [...], domini: [...]}` — ### **vuote = tutte** |
| `cercabile` | se entra nell'### **indice invertito** |
| `stato` | `ATTIVO` · `DEPRECATO` |
| `sostituito_da` | la chiave nuova, se deprecato |

### ⭐ **E LA PROMOZIONE:** un metadato usato da **quasi tutte** le voci **si promuove a campo
fisso**, con una **migrazione di versione** — cioè `schema_version` sale, e la migrazione sta in
uno script riseguibile.

### **L'INDICE INVERTITO `doc/indice/_indice_meta.json`** *(chiave → valore → lista di id)*
copre i metadati `cercabile` **e i campi a vocabolario**. ### ⛔ **È DERIVATO**, rigenerato a
**ogni** scrittura, e il validatore **confronta**: se è disallineato, **fallisce**.

---

# ⭐ `⑤` **LE CITAZIONI: `[[ID]]`**

| | |
|---|---|
| nei documenti ### **nuovi** | un ID si cita ### **`[[ID]]`** |
| ### ⛔ **le etichette LOCALI** *(`H1`, `D1`, `T1`, `PS-3`, `PT-7`, `S4`…)* | ### **NON sono ID.** Vivono dentro il loro documento, e ### **non si citano con `[[ ]]`** |
| ### ⛔ **NESSUN SEGNAPOSTO AUTOMATICO, MAI PIÙ** | lo schema `1` creava voci *«(CITATO N volte, MAI definito in un registro)»*: ### **`317` su `953`.** ### **Un ID citato e non definito è un RAPPORTO, non una voce** |

### **`python csv/indice.py citazioni`** produce quel rapporto: le `[[ID]]` che **non esistono**.

---

# 📌 `⑥` **LA TAVOLA DI CORRISPONDENZA della migrazione** — *`tipo` dell'era `1` → `classe`*

| `tipo_era1` | → `classe` | perché |
|---|---|---|
| `difetto` | `DIFETTO` | — |
| `sospetto` | `DIFETTO` | un sospetto è ### **un difetto non ancora provato**, e lo stato lo dice |
| `cura` | `CURA` | — |
| `misura` | `MISURA` | — |
| `criterio-locale` | `CRITERIO` | — |
| `presidio` | `PRESIDIO` | — |
| `standard` | `STANDARD` | — |
| `assioma` | `STANDARD` | ### ⚠ **gli assiomi VERI stanno in `assiomi.jsonl`:** una *voce* di tipo `assioma` è un ### **censimento su un assioma**, cioè uno standard di lavoro |
| `fronte` | `FRONTE` | un filone aperto |
| `altro` | `DIFETTO` | ### ⛔ **e il `dominio` resta `DA_CLASSIFICARE`:** `altro` ### **non è un'informazione**, e non si finge che lo sia |

### ⚠ **`teoria` NON è un `tipo`, è uno STATO dell'era `1`** *(`51` voci)*: diventa
`classe = TEORIA`, `stato = stato_era_1`, ### **`era = DA_CLASSIFICARE`** — alcune descrivono il
secondo ordine, e ### **non lo si indovina.**

---

# ⛔ **CHE COSA QUESTO SCHEMA NON FA**

| | |
|---|---|
| ### **non classifica per parola chiave** | ### **mai**, da nessuna parte. È l'errore che lo ha generato |
| ### **non chiude niente** | la migrazione ### **conserva** lo stato dell'era `1` e lo traduce; il ### **triage** è un lavoro a sé *(`doc/TRIAGE_ERA_1.md`)* |
| ### **non indovina** | dove non c'è ### **evidenza strutturale**, scrive `DA_CLASSIFICARE` — ed è ### **una decisione di Luca**, non un difetto dello schema |
| ### **non promette che `[[ID]]` sia già usato** | i documenti ### **vecchi** citano come citavano. La sintassi vale ### **per i nuovi** |
