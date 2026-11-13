# 2026-11-13 — IL REGISTRO DELLE CORSE DELL'ERA 2, LE DUE SKILL, LA CODA *(il mandato di ripresa di Luca delle `10:20`; la ripresa delle `11:50`)*

## 0. LA RIPRESA *(punto `1` e la decisione delle `11:50`)*

- **Il controllo della ripresa** *(solo lettura, `9ad7489a`)*: **tutto come atteso, tranne la catena del commit-graph di git che citava un file mancante** *(`graph-1c8287af`)*: **FERMO.**
- **Luca `11:50`:** **l'anomalia e' attesa dopo un riavvio forzato;** **prima `git fsck --no-dangling` (solo lettura), poi, se pulito, `git commit-graph write --reachable`.**
- ### **L'ESITO:** **`git fsck --no-dangling`: uscita `0`, nessuna riga stampata** *(nessun errore)*; **`git commit-graph write --reachable`: uscita `0`;** **`git commit-graph verify`: uscita `0`;** ### **l'avviso `unable to find all commit-graph files` e' SPARITO** *(`git log`, `git status` non lo stampano piu')*; **ora c'e' un solo file `.git/objects/info/commit-graph`, nessuna catena.**

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di scrivere; cosa NON so)*

- **Il registro dell'era 1** *(`csv/_stato_run.py`, `doc/STATO_RUN.md`)* **NON si tocca** *(Luca)*: **i suoi tre limiti** *(una sola voce aperta; il blob del simulatore dell'era 1; un file che e' diventato un elenco di voci di lavoro)* **sono le ragioni del registro nuovo.**
- **Il nucleo di oggi** *(per l'impronta)*: **i `12` file della tabella di `doc/NUCLEO_CONGELATO.md`** *(la colonna «il nucleo unificato», `sha1-BYTE`)*. **Il registro li legge DALLA TABELLA** *(non da una lista scritta nel modulo)*, **calcola lo `sha1-BYTE` di ciascuno dal disco e scrive se coincidono tutti con la tabella.**
- ### **I presidi che il registro deve rispettare:**
  - **`H-NON-TRACCIATI`** *(un file non tracciato sotto `doc/` o `csv/` blocca i commit)*: **il lucchetto e il file temporaneo della scrittura atomica stanno FUORI dal repo, o nella stessa cartella solo per l'istante di `os.replace`** *(il temporaneo nasce accanto al registro: `os.replace` e' atomico solo sullo stesso disco; vive per un istante e non e' mai committato)*;
  - **`niente file tracciati durante la suite`**: **il registro e' un file TRACCIATO; scriverlo mentre gira la suite la farebbe uscire con `1`.** ### **Quindi: niente `apri`, `tappa`, `chiudi` mentre gira la suite** *(regola scritta nella skill)*.
- ### **COSA NON SO:** **se Claude Code carica da solo le skill di `.claude/skills/` del progetto** *(il mandato lo dice; non l'ho verificato dal codice dell'estensione)*.

## 2. LA PROGETTAZIONE

- **Il modulo `csv/solitone/_registro_corse.py`** *(nessun `default` nelle firme)*:
  - **il formato del registro:** **un'intestazione in prosa, poi UNA RIGA PER EVENTO, `- {json}`** *(un oggetto JSON su una riga: `ev` in `APERTO`, `TAPPA`, `CHIUSO`; `nome`, `ora`, e i campi dell'evento)*. **Leggibile a occhio, e il controllo legge SOLO le righe `- {`.**
  - **`apri(nome, tipo, comando, note, forza)`:** **`tipo` in `lunga`, `breve`;** **scrive `APERTO` con l'ora, `HEAD`** *(e se l'albero e' pulito)*, **l'impronta del nucleo, il comando VERBATIM, le note;**
    - ### **RIFIUTA** *(alza `Rifiuto`)* **se:** **una voce APERTA con lo stesso nome;** **una `lunga` aperta e si apre una `lunga`;** **una `breve` aperta e si apre una `breve`;**
    - **`forza`:** **`None`, oppure il TESTO della decisione di Luca** *(non vuoto)*, **scritto nella voce;** **con `forza` le regole sui tipi non bloccano** *(lo stesso nome aperto due volte resta vietato anche con `forza`)*.
  - **`tappa(nome, punto)`:** **solo su una voce APERTA.** **`chiudi(nome, esito, punto)`:** **`esito` in `FINITO`, `FERMATO`, `FALLITO`.**
  - **`chiudi_dopo_riavvio(nome, visto_da_luca)`:** **`FERMATO (riavvio)`, al punto dell'ULTIMA tappa;** **`visto_da_luca` e' il testo** *(non vuoto)* **di quando e come Luca l'ha vista: senza, ALZA.**
  - **`aperte()`:** **le voci aperte, dal SOLO registro.**
  - **La scrittura ATOMICA e APPEND-ONLY:** **si legge il file, si aggiunge la riga, si scrive un temporaneo accanto e `os.replace`;** ### **prima di scrivere si controlla che il nuovo contenuto COMINCI col vecchio** *(se no, ALZA)*; **un lucchetto `O_EXCL` nella cartella temporanea del sistema** *(due processi non scrivono insieme)*.
  - **La riga di comando:** `python csv/solitone/_registro_corse.py apri|tappa|chiudi|aperte ...` *(per i driver bash)*.
- **Il registro `doc/REGISTRO_CORSE.md`:** **l'intestazione con le regole in breve e nessun evento.**
- **Il collaudo `csv/solitone/test_registro_corse.py`** *(su un registro TEMPORANEO, mai quello vero: lo sha del vero prima e dopo)*:
  - **DEVE PASSARE:** **la prova a secco** *(una `lunga` finta di `10` tick: `APERTO`, una tappa a `5`, `FINITO` a `10`; poi nessuna voce aperta)*; **una `breve` aperta mentre una `lunga` e' aperta: ACCETTATA;** **il file cresce solo in coda** *(ogni contenuto comincia col precedente)*; **il registro vero NON toccato.**
  - **DEVE FALLIRE** *(cioe' `apri` deve RIFIUTARE)*: **una seconda `lunga` con una `lunga` aperta;** **lo stesso nome aperto due volte.**
  - **In piu', come controlli:** **`forza` senza testo rifiuta;** **`chiudi_dopo_riavvio` senza `visto_da_luca` rifiuta.**
- **Le due skill:** **`.claude/skills/registro-corse/SKILL.md`, `.claude/skills/ripresa-dopo-riavvio/SKILL.md`**, **col frontmatter e le descrizioni del mandato.**
- **Il commit:** **il modulo, il registro, il collaudo e il suo referto, le skill, l'inventario, la relazione; con la suite.**
- ### **MI FERMO SE:** **un DEVE non va come deve** *(referto e FERMO, senza correggere)*; **la suite non passa.**

## 3. TODO DEL NEXT STEP

1. **Questo file, committato prima del codice.**
2. **Il modulo, il registro, il collaudo; il referto del collaudo; le skill; l'inventario; la suite; il commit.**
3. **La coda in `doc/ROTTA.md`** *(le voci `7`-`13` del mandato)*: **un commit a se'.**
4. **I bracci di P6** *(la voce `7`)*: **il task history, il codice, la suite, i bracci UNO ALLA VOLTA nel registro.**
