# dettaglio di `CLAUDE.md` par.9 — **l'indice dei difetti**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col
loro numero. Non rimanda ad altri file di `doc/REGOLE/`.)*

## PERCHE' NON SI LEGGE INTERO

`doc/INDICE_ID.tsv` e' **171 KB**. ### **Leggerlo tutto non fa risparmiare contesto, lo
consuma** — e non serve: la domanda e' quasi sempre su **una** voce.

### **I COMANDI**

`python csv/_indice_id.py` con:

| | |
|---|---|
| `--cerca ID` | **uguaglianza ESATTA** sull'id intero, **mai un prefisso** |
| `--aperti` · `--blocca SI` · `--famiglia X` | le viste |
| `--dettaglio ID` | le **colonne lunghe** di UNA voce |
| `--testo PAROLA` | ricerca sul testo **COMPLETO** di tutte le colonne |

### ⚠ **Il troncamento a 80 caratteri e' SOLO DI STAMPA, mai di confronto:** una ricerca che
non trova nulla ha cercato nel testo intero.

## LE TREDICI COLONNE, e i vocabolari

`id` · `alias` · `titolo_breve` · `fonte_principale` · `stato` · `blocca_run_base` · `tipo` ·
`famiglia` · `stato_da` · `avanzamento` · `revisione` · `motivo` · `nota`

| colonna | valori ammessi |
|---|---|
| `stato` | `aperto` · `chiuso` · `non-difetto` · `teoria` · `da-decidere` |
| `blocca_run_base` | `SI` · `NO` · `DA-DECIDERE` · `DA VERIFICARE` |
| `tipo` | `difetto` · `sospetto` · `fronte` · `misura` · `cura` · `presidio` · `assioma` · `standard` · `criterio-locale` · `altro` |
| `famiglia` | `A`-`G` oppure `?` |
| `avanzamento` | `FATTO` · `IN CORSO` · `IN CODA` · `BLOCCATO` · `CON RISERVA` · *(senza marcatore)* |

**`titolo_breve` e' `<= 100` caratteri e UNICO**, e il validatore lo impone: la frase intera
vive in `stato_da`.

### 📌 **E quando il vocabolario non ha il valore che serve, NON si inventa:** il mandato della
stella polare diceva *«`AUDIT-CURE` (audit)»*, e `audit` **non e' fra i `tipo`** — mappato su
`fronte` **e dichiarato**, perche' un valore nuovo lo **rifiuta il validatore**.

## UNA RIGA NELL'INDICE, E LA SPIEGAZIONE IN `STATO_RUN`

**UN DIFETTO NUOVO = UNA RIGA NELL'INDICE**, piu' la spiegazione lunga in
`doc/STATO_RUN.md` **con lo STESSO ID**. ### ⛔ **MAI IL CONTRARIO:** un ID nuovo in un
documento vivo **senza la sua riga** viene **RIFIUTATO da `H-INDICE`**.

### **E il hook guarda anche i MESSAGGI di commit**, non solo i documenti: tre volte in due
giorni ha fermato un commit perche' il messaggio citava un id che non esisteva ancora —
`FALSO-UNO`, `L-STELLA`, `H-NON-TRACCIATI`. ### **In due casi la cura giusta era aggiungere la
riga** *(e `L-STELLA` l'ha avuta perche' le altre quattro regole `L-` ce l'hanno)*; in uno era
**mettere in minuscolo una parola** che il hook leggeva come un id *(`ri-eseguibile`)*.

**`blocca_run_base = SI` RICHIEDE `motivo`** *(la prova in una frase)*: ### **una decisione
senza prova non passa il validatore.**

## LE VISTE SI GENERANO

`python csv/_lista_chiusa.py` · `python csv/_vista_smistamento.py` ·
`python csv/_punto_della_situazione.py`. ### **Non si modificano a mano.**

**IL VALIDATORE:** `python csv/_indice_id.py` *(e `--collaudo`)*, e **gira da solo nel
`pre-commit`**: schema, vocabolari, ID unici, coerenza `stato`/`blocca`, `motivo` dove serve,
**e nessuna voce persa rispetto al tag**.

## LA LISTA E' CONGELATA

Al tag `lista-chiusa-v1`: ### **SI SPUNTA, NON SI RIGENERA.** L'importatore che la costruiva
dal Markdown e' in `csv/_archivio/_indice_id_importatore.py` e **NON si rilancia** —
### **rilanciarlo sovrascriverebbe la fonte con una RICOSTRUZIONE, buttando via le decisioni
scritte nelle colonne.**

## DOVE STA IL «PERCHE'» DI OGNI `SI`

**COSA BLOCCA IL RUN BASE** si legge in `doc/SMISTAMENTO_run_base.md` *(gli `SI`, in ordine di
lavoro)*; **il PERCHE' di ogni `SI`** sta in `doc/REVISIONE_SI_2026-09-26.md`, che separa
✅ *verificato sul codice* da 🟨 *misura di Luca* da 🧠 *inferenza*.

## UN ID NON E' UN NOME: E' UNA CHIAVE

Un **assioma** e uno **standard** **non si rinominano mai**; le etichette **locali** a una
scheda o a un sigillo vivono col namespace *(`REGISTRO_FISICA:V8`)*, e la forma nuda e' un
`alias` **solo se univoca**.

### ⛔ **E I REPERTI NON SI RISCRIVONO:** nei task history, nei referti, nei `json` e nel
codice il nome vecchio **resta**, e si risolve con l'`alias`. ### **Riscrivere un reperto per
allinearlo a un nome nuovo cancella la prova di quando il nome era un altro.**
