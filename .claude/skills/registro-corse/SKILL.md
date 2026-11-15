---
name: registro-corse
description: Usare a ogni corsa del simulatore: aprire, aggiornare e chiudere la voce in doc/REGISTRO_CORSE.md, cosi' dopo un riavvio lo stato si legge dal disco
---

# Il registro delle corse dell'era 2

*(Luca, 2026-11-13 10:20. Il modulo: `csv/solitone/_registro_corse.py`; il registro: `doc/REGISTRO_CORSE.md`; il task history: `doc/TASK_HISTORY/2026-11-13_registro_corse.md`.)*

**Ogni corsa del simulatore** — un braccio, un video, una prova, una corsa lunga — **ha una voce nel registro.** Gli orari nello scratchpad non bastano: dopo un riavvio lo stato si legge **dal disco, nel repo**.

## Le regole

1. **Si apre PRIMA di lanciare**, con il tipo e il comando **verbatim**:
   ```
   python csv/solitone/_registro_corse.py apri --nome <nome> --tipo lunga|breve --comando "<il comando esatto>" --note "<cosa misura, il mandato>"
   ```
   L'apertura scrive l'ora, `HEAD`, l'impronta dei file del nucleo elencati in `doc/NUCLEO_CONGELATO.md` *(e se coincidono con la tabella)*, il comando.
2. **`apri` RIFIUTA** *(ed esce con `2`)* se:
   - c'e' gia' una voce APERTA con lo **stesso nome**;
   - c'e' gia' una **`lunga`** aperta e si apre un'altra **`lunga`**;
   - c'e' gia' una **`breve`** aperta e si apre un'altra **`breve`**.
   **Quindi al piu' una lunga e una breve insieme.** Un rifiuto **non si aggira**: si chiude la voce giusta, o si chiede a Luca.
3. **`--forza "<testo>"` SOLO con una decisione di Luca**, e il testo e' **la decisione stessa** *(chi, quando, cosa)*: resta scritto nella voce. Con `forza` le regole sui tipi non bloccano; **lo stesso nome due volte resta vietato.**
4. **Le tappe:** a **ogni pezzo salvato**, o **ogni circa 10 minuti**. ### **Vanno in un file FUORI dal repo** *(la decisione (b) di Luca, `12:58`: `E:/soliton_simulator/registro_tappe/<nome>.txt`)*: **il registro del repo NON si tocca;** **alla chiusura il modulo le COPIA nel registro.**
   ```
   python csv/solitone/_registro_corse.py tappa --nome <nome> --punto "tick <t>"
   ```
5. **La chiusura**, col **punto esatto**:
   ```
   python csv/solitone/_registro_corse.py chiudi --nome <nome> --esito FINITO|FERMATO|FALLITO --punto "tick <t>"
   ```
5-bis. ### **LA REGOLA DEI CONTI** *(R-CONTI, Luca `2026-11-13` `23:47`; la ROTTA, «La regola dei conti»)*: **una corsa NUOVA** *(il codice scritto dopo che `csv/solitone/conti.py` esiste)* **stampa la tabella dei conti** *(i pezzi all'inizio, ogni `500` tick e alla fine; il residuo; la massa uscita dal bordo)*, **e con due o piu' solitoni la tabella delle forze** *(finestre di `500` tick)*, **con uno solo la deriva, il picco e il raggio.** ### **SENZA le tabelle non si chiude `FINITO`:** **si chiude «FINITA SENZA CONTI», col motivo** *(finche' il modulo non ha l'esito apposito: `--esito FINITO --punto "SENZA CONTI: <il motivo>; ..."`)*. **Le corse gia' scritte o in fila prima della regola NON si riscrivono.**
5-ter. ### **L'ENERGIA NELLE TABELLE DEI CONTI E' LA MEDIA SU `100` TICK** *(R-CONTI-6, Luca `2026-11-14` `09:34`; la ROTTA)*: **il valore di un solo tick oscilla troppo** *(`+-200` su `1.65e7` anche senza campi)*.
6. **Le voci aperte** si leggono **SOLO** dal registro: `python csv/solitone/_registro_corse.py aperte`.
7. **Dopo un riavvio**, una voce rimasta APERTA **si chiude come `FERMATO (riavvio)` all'ultima tappa SOLO dopo che Luca l'ha vista**:
   ```
   python csv/solitone/_registro_corse.py riavvio --nome <nome> --visto-da-luca "<quando e come Luca l'ha vista>"
   ```
   **Fino ad allora la voce blocca le corse del suo tipo, come deve.**

## LA REGOLA DELLA SCATOLA *(R-SCATOLA; Luca `2026-11-15` `12:01`, da ora per sempre; anche nella ROTTA)*

- ### **R-SCATOLA-1:** **la scatola deve essere ALMENO `3` VOLTE l'oggetto piu' grande che contiene, compresa la sua deformazione del vuoto:** **il raggio dell'oggetto `R_ogg` e' il raggio oltre il quale `|phi - phi0|` medio per anello scende sotto il `2%` del suo massimo;** **la distanza dal centro al lato piu' vicino del toro `>= 3 R_ogg`, e il bordo** *(`R_A`)* **che comincia oltre `2 R_ogg`.**
- **R-SCATOLA-2:** **ogni corsa NUOVA stampa all'inizio e alla fine i due rapporti** *(il lato piu' vicino / `R_ogg`, `R_A` / `R_ogg`)* **e se la regola e' rispettata.**
- **All'`apri` di una corsa nuova, nelle note:** **`R_ogg`, il lato piu' vicino e `R_A`, coi due rapporti.**

## L'AMBIENTE DELLE CORSE NUOVE *(R-AMBIENTE; Luca `2026-11-15` `15:46`; anche nella ROTTA)*

- ### **R-AMBIENTE-1:** **DA ORA tutte le corse NUOVE girano con l'interprete di E:** *(`E:\python\py3132\python.exe`)*; **le corse gia' in corsa e le loro PROSECUZIONI** *(`legati-GU`, `legati-GUpi`, `legati-t120` e le ripartenze dal tetto o dal riavvio)* **restano sull'ambiente di C: con cui sono nate** *(dichiarato)*. **La CONDIZIONE: la suite con l'interprete di E: `67/67` e AL BIT; finche' non c'e', le corse nuove restano su C:.**
- **R-AMBIENTE-2:** **ogni corsa nuova scrive nel registro, all'apertura** *(nelle note di `registro apri`)*, **l'interprete** *(il percorso, la versione, numpy e scipy)* **e l'ambiente** *(`PYTHONNOUSERSITE=1`, `TMP`/`TEMP`)*.
- ### **R-AMBIENTE-3:** **se E: non c'e' o l'interprete di E: non parte, la corsa NON parte** *(FERMO di quella corsa, scritto)*: **MAI un ripiego silenzioso su C:.**

## Il commit del registro

- ### **R-COMMIT** *(Luca `2026-11-15` `15:30`, da ora per sempre, tutti e due i rami)*: **R1** prima: nessun `index.lock`; il lucchetto di `committa` o assente o del processo VIVO (residuo: si toglie e si scrive nel messaggio); mai due commit insieme. **R2** l'ambiente: `TMP`/`TEMP` su C:, nessuna `GIT_CONFIG_*` (solo per la suite su E:), stampato. **R3** il limite `15` minuti, i hook in un log, l'ultima riga leggibile; se scade: si ferma, si scrive, R5, e si chiede a Luca. **R4** mai interrompere un commit a meta'. **R5** dopo: HEAD cambiato, push fatto, `HEAD == origin/<ramo>`, lo stage vuoto, nessun lucchetto, nessun `git.exe` del commit vivo: «COMMIT OK: <sha>, origin uguale, stage vuoto». *(Lo strumento: `committa2.py` nello scratchpad, fuori dal repo: i controlli R1, R2, R3, R5.)*


- **Subito dopo `apri` e subito dopo `chiudi`:** commit e push **del solo registro**:
  ```
  git add doc/REGISTRO_CORSE.md      # SOLO questo file
  ```
  ### ⛔ **MAI `git add -A` o `git add .` con una corsa attiva:** si committerebbero file a meta'.
- **Le tappe non si committano:** **stanno fuori dal repo, ed entrano nel registro con la chiusura** *(quindi col commit dopo `chiudi`)*.
- ### ⚠ **La suite** *(`primo_ordine/collauda.py`)* **RIMETTE con `git checkout --` i file tracciati che cambiano mentre gira** *(ed esce con `1`)*. **Le tappe sono fuori dal repo, quindi una corsa puo' scriverle mentre gira la suite** *(il DEVE della suite vera, `csv/solitone/prova_suite_registro.py`)*; ### **ma `apri` e `chiudi` scrivono il registro del repo: MAI mentre gira la suite.**
- **Il registro e' APPEND-ONLY:** si scrive **solo col modulo**, mai a mano; il modulo controlla che ogni scrittura **aggiunga in coda**.

## Che cosa NON si tocca

`csv/_stato_run.py` e `doc/STATO_RUN.md` *(il registro dell'era 1)*.
