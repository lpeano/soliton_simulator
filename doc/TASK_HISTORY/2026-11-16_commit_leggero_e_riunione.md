# 2026-11-16 -- IL COMMIT PIU' LEGGERO (S1 + S2) E LA RIUNIONE DELLE DUE NAVI *(Luca `2026-11-16` `08:57`, (A) e (B))*

> **La carta, scritta e committata PRIMA del codice.** La parte (C) del mandato *(la FMA esplicita)* ha la sua carta nel
> clone su E:, `doc/TASK_HISTORY/2026-11-15_motore_numba.md`, sez. `20`.
> La carta dei tempi da cui partono S1 e S2: `doc/referti_l2/tempi_hook_carta.txt` *(`c0c3b78d`)*.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

### S1 -- il `valida` di `_hook_presidi.py`

- **Dal codice** *(`csv/_hook_presidi.py::pre_commit`)*: **lancia `csv/indice.py valida` con `cwd` = la radice, cioe' sul DISCO**, se `doc/indice/voci.jsonl` esiste; **un'uscita diversa da `0` rifiuta il commit.**
- **Lo stesso `valida` gira sullo STAGE in `_stage.py --rapido`** *(l'export dell'indice di git, `RAPIDI = 1`: solo `valida`)*, **piu' avanti nello stesso `pre-commit`.**
- ### **LA DOMANDA DEL MANDATO (A1): la vista del DISCO serve a un controllo?** **La mia lettura:**
  - **la vista del disco NON si perde: `_albero_era2.py --collaudo`** *(P-ALB, nello stesso `pre-commit`, dopo)* **lancia `valida` sul DISCO e PRETENDE che passi** *(il ramo «rimessa la fonte, `valida` PASSA di nuovo»)*. **Quindi un disco che non valida fa ancora rifiutare il commit**, da P-ALB invece che da `_hook_presidi`.
  - **Cosa cambia:** **l'ORDINE.** **Fra `_hook_presidi` e P-ALB girano altri comandi che leggono il DISCO dell'indice** *(`_metodi_era2`, `_controlli_nell_indice`, `_testo_e_metadati`, `_replay_registri`, e i due generatori `_controlli_indice_v2 --scrivi` e `_presidio_indice --collaudo --scrivi`, che SCRIVONO due file e li mettono in stage)*. **Oggi, con un indice rotto sul disco, il commit si ferma PRIMA di loro; con S1 girano su un indice non validato** *(e possono fermarsi da se', o scrivere i due generati)* **e il rifiuto arriva da P-ALB o da `_stage`.**
  - ### **Questo e' «la vista del disco serve a un controllo»?** **La mia risposta: la vista SERVE, ma resta; cio' che si perde e' la GUARDIA davanti ai generatori.** **Lo misuro in A3 con un caso che DEVE fallire** *(un indice rotto sul disco, non in stage)*: **se il commit viene ancora rifiutato e i file del repo restano quelli di prima, S1 resta; se no, FERMO e scritto.**
- **Il collaudo di `_hook_presidi.py`** *(`--collaudo`)*: **non so se prova il ramo di `valida`** *(dal `grep`: nessun caso lo nomina)*. **Lo verifico girandolo.**
- **I testi che descrivono il ramo:** `csv/_doc_referto_indice.py` *(«gira ANCHE `indice.py valida`»)*, la voce `H-VALIDATORE` *(la sua `fonte` e' `csv/_indice_id.py`, che RESTA in `_hook_presidi`)*, `csv/_metodi_era2.py` *(la riga di `H-VALIDATORE`)*. **Si aggiornano nello stesso commit se diventano falsi.**

### S2 -- `_storico_da_git` con una memoria

- **Dal codice** *(`csv/indice.py::_storico_da_git`)*: **`git log --reverse --format=%h -- doc/indice/storico.jsonl`, poi UN `git cat-file --batch` di TUTTE le versioni** *(oggi `331`, circa `1.8 GB` letti)*; **per ognuna il numero di righe non vuote; `per_riga` si estende di `n - prec` volte il commit; se `n < prec` torna `([], -1, -1)`.**
- **Cio' che serve di ogni versione e' SOLO il numero di righe.** **La memoria: sha1 del BLOB -> numero di righe** *(un blob di git non cambia mai contenuto a sha1 fisso)*.
- **Come si sa lo sha1 del blob senza leggerlo:** **`git cat-file --batch-check`** *(«sha tipo dimensione», senza il contenuto)*; **poi `--batch` solo per i blob che la memoria non ha.**
- **Dove:** **dentro la cartella comune di git** *(`git rev-parse --git-common-dir`: fuori dall'albero di lavoro, mai tracciata; `C:` per il principale, `E:` per il clone)*; **file `indice_storico_righe.json`.**
- **Il controllo di coerenza a ogni lettura** *(il mandato: «mai usata se rotta»)*: **(i) il file si legge come JSON con la forma attesa e un'impronta sha1 del proprio contenuto che torna; (ii) la voce del blob PIU' RECENTE fra quelli presi dalla memoria si rilegge da git e il conto deve coincidere.** **Se una delle due cade: la memoria si BUTTA e si ricostruisce da zero, e lo si dice su `stderr`.**
- **Cosa NON so:** **se i casi limite del codice di oggi** *(un blob mancante -> `break`; una testa con meno di `3` campi -> `break`)* **hanno lo stesso comportamento con `--batch-check`** *(«`<oggetto> missing`»: due campi -> `break` uguale)*. **Lo provo con un caso costruito.**

### LA PROVA (A3) -- il mio dubbio sul costo, e la riduzione che propongo

- **Il mandato:** il `pre-commit` vecchio e quello nuovo sugli stessi `40` commit del `2026-11-15`, esito per esito. **Un `pre-commit` costa circa `330 s`: `80` corse sono circa `7.3` ore.**
- ### **LA RIDUZIONE, dichiarata qui** *(e la ragione e' verificabile)*: **S1 e S2 cambiano SOLO due file: `csv/_hook_presidi.py` e `csv/indice.py`.** **Ogni altro comando del `pre-commit` ha gli STESSI byte prima e dopo** *(lo verifico con lo sha1 di ogni file lanciato)*; **il suo esito puo' cambiare solo attraverso `indice.py`** *(chi lo importa o lo lancia)*. **Quindi la prova gira, su ogni commit, TUTTI i comandi che toccano uno dei due file** *(il censimento con `grep` di chi importa o lancia `indice.py`, scritto nel referto)*, **nei due modi, e confronta codice d'uscita e righe di rifiuto.**
  - **Piu' un CONTROLLO della riduzione: il `pre-commit` INTERO vecchio e nuovo su `3` dei `40`** *(il primo, uno in mezzo, l'ultimo)*.
  - ### **Se Luca la vuole intera: sono circa `7` ore di macchina, e lo dico nel messaggio.**
- **Il «clone di prova a quel commit con lo stesso stage»:** **un `git worktree` al PADRE del commit** *(H-P8)*, **con lo stage del commit** *(`git read-tree` del commit sull'indice del worktree: lo stage e' l'albero del commit)* **e il disco uguale allo stage.**
- **I casi che DEVONO fallire** *(su un commit dei `40`, nei due modi)*:
  - **F1:** una riga di `storico.jsonl` CAMBIATA in mezzo, in stage *(non solo aggiunte)* -> `valida` rifiuta;
  - **F2:** `voci.jsonl` cambiato in stage SENZA la riga di storico -> rifiuta;
  - **F3:** un indice rotto SOLO sul disco *(non in stage)* -> il commit rifiutato *(S1: da chi, scritto)*, **e i file del repo uguali a prima;**
  - **F4** *(S2)*: **la memoria corrotta** *(un conto sbagliato a mano)* -> **riconosciuta, buttata, ricostruita: lo stesso `per_riga`;**
  - **F5** *(S2)*: **la memoria assente** -> ricostruita, lo stesso `per_riga`.
- **La garanzia di S2, al bit:** **`per_riga`, `n_head` e `n_stage` calcolati nei due modi su tutti i `40` commit: uguali come liste Python.**
- ### **UN SOLO ESITO DIVERSO: la strada cade e si torna indietro.**

### LA RIUNIONE (B)

- **La prova a secco del mattino** *(Luca)*: **`merge-tree` senza conflitti, `189` file nuovi, nessuno sotto `primo_ordine/`.** **Si rifa' prima del merge** *(dopo (A) sul principale c'e' un commit in piu')*.
- **H-NUCLEO-CONGELATO sul commit di merge:** **i nomi in stage del merge non contengono `primo_ordine/`** *(lo verifico prima)*: **il presidio non deve avere eccezioni.**
- **Il registro del mattone resta com'e'; le corse nuove nel registro del principale con l'interprete di E:.**
- **Cosa NON so:** **dove sta «la ROTTA» con le voci `16` e `17`** *(lo cerco nel repo prima di scrivere)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

| passo | che cosa | che cosa decide | che cosa mi fa FERMARE |
|---|---|---|---|
| A1 | togliere il `valida` sul disco da `_hook_presidi` | se la vista del disco resta coperta | F3 non rifiutato, o un file del repo cambiato dopo il rifiuto |
| A2 | la memoria di `_storico_da_git` | il guadagno su ogni `valida` | `per_riga` diverso anche su UN commit |
| A3 | la prova sui `40` + F1-F5 + `3` interi | se S1 e S2 restano | un solo esito diverso |
| A4 | i tempi prima/dopo su un commit vero | il numero da dare a Luca | -- |
| B1 | i controlli prima | se si puo' fondere | una corsa aperta, un conflitto, `primo_ordine/` fra i file |
| B2-B4 | merge, suite, tag, ROTTA | -- | la suite non `67/67`; H-NUCLEO-CONGELATO che rifiuta |

**Le letture si fissano qui:** **«stesso esito» = stesso codice d'uscita E stesse righe di rifiuto** *(le righe che cominciano con `[` o con `###`, e i messaggi di `valida`)*, **a meno dei tempi e dei percorsi temporanei** *(dichiarati nel confronto)*. **Per S1 le righe di rifiuto di `_hook_presidi` sul disco SPARISCONO per costruzione: il confronto di S1 e' sul codice d'uscita del `pre-commit` e sulle righe di `valida`, da chiunque sia lanciato.**

## 3. TODO DEL NEXT STEP

1. Questa carta: commit e push.
2. A2 e A1 nel codice; il censimento di chi usa `indice.py`; la prova A3 *(`doc/referti_l2/commit_leggero_prova.py` -> `commit_leggero_prova.txt`)*.
3. Se la prova passa: il commit di S1 + S2 *(coi hook VECCHI, cioe' quelli in vigore)*; poi un commit di prova coi hook nuovi; A4 i tempi.
4. (B): B1, il merge, la suite, la relazione e la ROTTA, il tag.
