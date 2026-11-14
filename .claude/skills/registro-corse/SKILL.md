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

## Il commit del registro

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
