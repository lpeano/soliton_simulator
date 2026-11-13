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

## 4. LA RICHIESTA DI LUCA DELLE `12:15` SULLA SUITE: IL PUNTO (1) SI FERMA SUL NUCLEO CONGELATO

- **La richiesta:** **(1) la suite IGNORA `doc/REGISTRO_CORSE.md` nel controllo dei file tracciati cambiati** *(l'unica eccezione, dichiarata nella suite e nella skill)*, **con un DEVE PASSARE** *(una riga aggiunta al registro durante la suite: uscita `0`)* **e un DEVE FALLIRE** *(una riga aggiunta a un altro file tracciato: uscita `1`)*; **(2) verificare che una sessione nuova veda le skill.**
- ### **DAL CODICE** *(`primo_ordine/collauda.py`, `main`, cercato per nome: `_sporchi`, `_sporcati`)*:
  - **la suite prende `git status --porcelain` PRIMA** *(`_prima`)* **e DOPO;** **i file sporcati DURANTE la suite** *(`_sporchi() - _prima`)* ### **si RIMETTONO con `git checkout --`** **e la suite esce con `1`.**
  - ### ⚠ **QUINDI E' PEGGIO DI UN'USCITA `1`:** **una tappa scritta nel registro mentre gira la suite verrebbe CANCELLATA** *(il `checkout` riporta il registro all'ultimo commit)*. **Se il registro era GIA' sporco quando la suite e' partita, e' in `_prima` e non si tocca.**
- ### **IL CONFLITTO:** **`collauda.py` sta in `primo_ordine/`:** **`doc/NUCLEO_CONGELATO.md` dice `stato: CONGELATO` e nomina «`collauda.py` compreso»; il presidio `H-NUCLEO-CONGELATO` rifiuta OGNI commit che tocca `primo_ordine/`, senza via d'uscita;** **e il mandato delle `10:20` dice «nessun file del nucleo cambiato in tutto il mandato».**
  - ### **Non lo sblocco da solo** *(ci vuole una decisione SCRITTA di Luca in `doc/NUCLEO_CONGELATO.md`)*: **FERMO su questo punto, la domanda a Luca.**
- ### **LE STRADE, per la decisione di Luca:**
  - **(a) lo sblocco dichiarato per UNA modifica di `collauda.py`** *(l'eccezione del registro nel calcolo di `_sporcati`, piu' il collaudo DEVE PASSARE / DEVE FALLIRE)*, **poi di nuovo `CONGELATO`;** **la proposta del guardiano;**
  - **(b) nessuna modifica, una regola scritta:** **nessuna suite mentre una corsa e' aperta nel registro** *(oggi costa poco: i bracci, il video triplo e le bande piatte non richiedono una suite mentre girano; i referti si committano senza suite)*.
- ### **INTANTO** *(fino alla decisione)*: **vale (b), come regola mia e conservativa** *(scritta nella skill `registro-corse`)*: **non decide niente al posto di Luca, evita solo di perdere una tappa.**
- **Il punto (2)** *(le skill viste da una sessione nuova)* **si fa dopo il commit, e non dipende da (1).**

## 5. GLI ESITI: IL COLLAUDO `10/10`; LE SKILL VISTE DA UNA SESSIONE NUOVA

- **Il collaudo** *(`doc/referti_l2/registro_corse_collaudo.txt`, il codice a `83907a19`)*: ### **`10/10` controlli come devono.**
  - **la prova a secco** *(una `lunga` finta di `10` tick)*: **`APERTO`, `TAPPA`, `CHIUSO` `FINITO` a `tick 10`, poi nessuna voce aperta;** **l'apertura registra `HEAD 83907a19`, `0` file modificati, il nucleo `12` file uguali alla tabella;**
  - **una `breve` accanto alla `lunga`: ACCETTATA;** ### **DEVE FALLIRE, e fallisce: una seconda `lunga` RIFIUTATA, lo stesso nome due volte RIFIUTATO;**
  - **`forza` vuota e il riavvio senza `visto_da_luca` rifiutati; il riavvio con `visto_da_luca` chiude `FERMATO` a `tick 750`** *(l'ultima tappa)*; **i rifiuti non scrivono** *(`3` eventi)*; **il registro cresce solo in coda** *(`5` scritture)*; **il registro vero non toccato** *(`088b14a3` prima e dopo)*.
- ### **Le skill viste da una sessione NUOVA** *(Luca `12:15`, punto 2)*: **una sessione `claude.exe -p` dell'estensione `2.1.323`, nel repo, senza strumenti, un turno:** ### **`registro-corse` e `ripresa-dopo-riavvio` sono le PRIME due dell'elenco delle skill disponibili** *(l'uscita intera in `skill_sessione_nuova.txt` nello scratchpad)*.
- ### **Il punto (1) delle `12:15`** *(la suite che ignora il registro)* **resta FERMO sul nucleo congelato:** **la domanda nella sez. `4`; intanto nessuna suite con una corsa aperta.**

## 6. LA DECISIONE DI LUCA (b): LE TAPPE FUORI DAL REPO *(Luca `12:58`; il messaggio delle `12:22` NON mi e' arrivato)*

- ### **LA DECISIONE:** **le TAPPE in un file FUORI dal repo** *(`E:\soliton_simulator\registro_tappe\<nome>.txt`)*, **copiate nel registro alla CHIUSURA;** **`apri()` e `chiudi()` nel repo;** **nessun file in `primo_ordine/` si tocca.** **Finche' il video triplo era aperto, nessuna suite** *(rispettato: il video e' finito alle `12:49:42`, chiuso e committato in `102814bd`; nessuna suite e' girata nel frattempo)*.
- ### ⚠ **«I DEVE delle `12:22`»: il messaggio delle `12:22` non mi e' arrivato.** **Uso quelli delle `12:15`, adattati a (b), e lo DICHIARO;** **se quelli delle `12:22` sono diversi, si rifanno.**
- ### **IL PROGETTO:**
  - **`tappa(nome, punto)`:** **la voce dev'essere APERTA nel registro;** **una riga** *(`{ora, punto}` in JSON)* **in FONDO al file delle tappe** *(apertura in append, `fsync`)*; ### **il registro del repo NON si tocca.**
  - **`chiudi(nome, esito, punto)`:** **le tappe del file esterno COPIATE nel registro** *(un evento `TAPPA` per ciascuna, col campo `copiata_alla_chiusura`)*, **poi `CHIUSO`, in UNA scrittura atomica;** **il file delle tappe spostato in `<nome>.chiuso.<ora>.txt`** *(non si cancella)*.
  - **`apri`:** **se il file delle tappe di quel nome esiste gia'** *(una chiusura caduta a meta')*, ### **RIFIUTA:** **va guardato, non sovrascritto.**
  - **`aperte()`:** **le voci aperte dal SOLO registro;** **l'ultima tappa dal file esterno** *(serve al riavvio)*. **`chiudi_dopo_riavvio`:** **copia anche lui le tappe, poi `FERMATO` all'ultima.**
  - **La cartella delle tappe si punta altrove nel collaudo** *(come il registro: `su_file`)*.
- ### **I DEVE** *(le `12:15` adattate a (b), dichiarate)*:
  - **nel collaudo** *(su un registro e una cartella TEMPORANEI)*: **una tappa NON cambia il registro** *(lo sha prima e dopo)* **e scrive nel file esterno;** **la chiusura copia le tappe nel registro, nell'ordine, e sposta il file;** **la prova a secco, la `breve` accanto alla `lunga`, i rifiuti** *(come prima)*;
  - ### **con la SUITE vera** *(un driver che lancia `primo_ordine/collauda.py`, legge la sua uscita e AGISCE appena la suite ha preso la fotografia dell'albero, la riga «TUTTI I COLLAUDI, CON I TEMPI»)*:
    - **DEVE PASSARE:** **una tappa scritta durante la suite: la suite esce con `0`, il registro del repo non cambia, la tappa e' nel file esterno;**
    - **DEVE FALLIRE:** **una riga aggiunta a un altro file TRACCIATO durante la suite: la suite esce con `1`** *(e lo rimette: si controlla che dopo l'albero sia pulito)*.
  - **L'ordine:** **il codice, l'inventario, la suite normale e il commit; poi il collaudo; poi le due corse della suite col driver** *(ciascuna circa `15` minuti, una dopo l'altra)*; **poi i bracci di P6.**
- **La regola provvisoria della sez. `4`** *(nessuna suite con una corsa aperta)* **cade quando i DEVE con la suite vera passano;** **la skill si aggiorna nello stesso commit del codice, con la regola nuova.**

## 7. IL TESTO DELLE `12:22`, ARRIVATO ALLE `13:00`: DUE DIFFERENZE DA CIO' CHE AVEVO SCRITTO, PORTATE NEL CODICE

- **Coincide con la sez. `6`:** **`apri` e `chiudi` nel registro del repo, mai durante la suite; le tappe in `E:\soliton_simulator\registro_tappe\<nome>.txt`, append-only, che la suite non vede; `chiudi` le copia insieme alla chiusura; nessun file in `primo_ordine/`.**
- ### **LE DUE DIFFERENZE:**
  1. **il DEVE FALLIRE scrive una TAPPA nel registro DEL REPO durante la suite** *(non una riga in un altro file tracciato)*: **il driver ha il modo `registro` al posto di `tracciato`** *(una riga `- {json}` `TAPPA` in fondo a `doc/REGISTRO_CORSE.md`)*;
  2. **la skill della ripresa legge, per ogni voce APERTA, anche il SUO FILE DELLE TAPPE** *(quante, la prima, l'ultima, l'ora)*; **e un file di tappe senza voce aperta e' una chiusura caduta a meta': FERMO.**
- **ERRORE DEL GUARDIANO `n.147`** *(Luca)*: **aveva consigliato la (a) senza controllare che il controllo sta nel nucleo congelato** *(nella MAPPA)*.
- ### **L'ORDINE:** **la suite girata sul codice di prima** *(`13:05:48`-`13:21:17`, `67/67`)* **non vale per il codice cambiato: si RIGIRA, poi il commit;** **poi il collaudo; poi il driver nei due modi; poi i bracci di P6.**

## 8. IL DRIVER, IL MODO TAPPA: UN FALSO PASSA (ERRORE MIO), LA CURA

- **Il referto** `doc/referti_l2/registro_suite_tappa.txt` *(il codice a `afdb29fc`, il driver dalle `13:51:23` alle `14:07:44`)*: **`3/3`, la suite `67/67` uscita `0`, il registro `5571175c` uguale, una tappa nel file esterno, l'albero pulito.**
- ### ⚠ **MA IL DEVE NON VALE:** **la tappa nel file esterno porta l'ora `14:07:44`, LA STESSA della fine della suite.** **Lo stdout di `primo_ordine/collauda.py` passa da una PIPE ed e' BUFFERIZZATO:** ### **il driver ha letto la riga «TUTTI I COLLAUDI, CON I TEMPI» solo quando la suite ha scaricato il buffer, cioe' alla FINE, DOPO il controllo dei file sporcati.** **Il DEVE «agito dopo la fotografia» passava per costruzione: un FALSO PASSA** *(non poteva fallire per la ragione giusta)*.
- ### **ERRORE MIO:** **non ho controllato che l'azione cadesse DENTRO la suite** *(il caso: una suite di `15` minuti, l'azione a `0` s dalla fine)*.
- **La voce `prova-suite-tappa` chiusa `FALLITO`** *(il punto lo dice)*.
- ### **LA CURA** *(un commit a se', con la suite)*: **la suite lanciata con `python -u`** *(lo stdout non bufferizzato)*; ### **un DEVE nuovo: l'azione almeno `60` s PRIMA della fine della suite** *(le ore registrate dal driver)*; **poi il modo tappa RIFATTO, poi il modo registro.**

## 9. IL REGISTRO (b) COLLAUDATO

- **`doc/referti_l2/registro_suite_registro.txt`** *(il codice a `d08e97e0`, la corsa a `475b018d`, dalle `15:13:03` alle `15:29:01`)*: **`5/5`:** **la tappa scritta in fondo a `doc/REGISTRO_CORSE.md` `956` s prima della fine della suite;** ### **la suite `67/67` ma «HA SPORCATO 1 FILE»: uscita `1`** *(il DEVE FALLIRE fallisce come deve)*; **il registro RIMESSO** *(`574de696` prima e dopo)*; **l'albero pulito.**
- ### **I DEVE delle `12:22`, tutti come devono:** **la prova a secco con le tappe nel file esterno e copiate alla chiusura** *(il collaudo `12/12`)*; **la suite esce con `0` mentre una corsa scrive tappe nel file esterno** *(`4/4`, la tappa `953` s prima della fine)*; **una tappa nel registro del repo durante la suite: la suite esce con `1`** *(`5/5`)*.
- **La regola provvisoria della sez. `4` cade:** **una corsa scrive le sue tappe mentre gira la suite;** **`apri` e `chiudi` mai durante la suite** *(la skill)*.
- **Poi: i bracci di P6, nell'ordine** *(il primo, (0), aperto come «lunga»)*. **La voce `9`** *(le bande piatte)* **aspetta Luca sui proiettori del vuoto** *(`6` componenti, quelli del `31` ottobre sono per la materia)*.
