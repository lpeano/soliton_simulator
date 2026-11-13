# 2026-11-13 — L'INVENTARIO DEI DATI DEL REPO SU E: *(Luca `15:34` e `15:35`; SOLO LETTURA)*

## 0. LE DUE VERSIONI DEL MANDATO *(`[[PRECEDENZA-IN-CODA]]`)*

- **Sono arrivate due versioni, `15:34` e `15:35`:** ### **vale SOLO l'ultima** *(`15:35`)*. **La differenza:** **la `15:35` limita la lettura a `E:\soliton_simulator` e alle altre cartelle di E: che gli script del repo aprono** *(trovate con una ricerca dei percorsi `E:` nel codice)*; **del volume, solo il file system e lo spazio libero; nessun'altra cartella di E: letta.**
- **L'ordine registrato:** **la coda in corso** *(il DEVE FALLIRE del registro, chiuso in `032d7265`; i bracci di P6, il primo `(0)` in corsa)* **non si interrompe; l'inventario e' una «breve» accanto ai bracci.**

## 1. LE PREMESSE DAL CODICE *(cosa credo; cosa NON so)*

- **I percorsi `E:` nel codice** *(una ricerca nelle stringhe di `csv/` e `primo_ordine/`, `.py` `.yaml` `.json`)*: **`E:\soliton_simulator`** *(le mappe: `csv/solitone/mappe.py`, `RADICE`; il registro delle tappe)* **e `E:\soliton_archivio`** *(l'archivio dell'era 1: `video_val600`, `spostati_2026-09-22`, una cartella di `_test_fork`)*. ### **L'inventario legge queste due e NIENT'ALTRO.**
- **Gli stati delle corse** *(i file degli `stati` nel jsonl di ogni corsa)*: **NON so ancora dove stanno** *(E: o il disco del repo)*: **lo dice il percorso registrato.** ### ⚠ **Se una parte e' sul disco del repo ma IGNORATA da git** *(`db/`, `db_era2/`)*, **anche quella e' in una sola copia:** **lo scrivo come osservazione, senza inventariarla** *(il mandato chiede E:)*.
- **Gli stati di PARTENZA delle prove** *(dagli script, cercati per nome: `T0`, `T_STATO`, `x["t"] == ...`)*: **C35-pi a `60000`** *(G2, P6)*, **TBS a `10000`** *(le G1, il video triplo)*, **TM1000 a `13333`** *(`carta_d0`, `test_simmetrica`)*, **S162 a `10000`** *(`carta_coppia`)*, **e gli stati a `0` delle corse che la carta della coppia apre.** **L'elenco si stampa dal codice, dichiarato.**
- **Lo sha1 «gia' citato in un referto»:** **i referti citano di solito lo `sha` PER CHIAVE** *(`_vuoto_vivo_B.shas`, registrato nel jsonl)*, **non lo sha1 del file.** **Quindi due controlli:** **lo sha1 dei byte del file** *(cercato nei referti)*, **e gli sha per chiave ricalcolati dal file contro il jsonl** *(l'integrita')*.

## 2. LA PROGETTAZIONE

- **Lo script `csv/solitone/inventario_E.py`** *(solo lettura: `os.walk`, `os.stat`, `hashlib`; nessuna scrittura fuori dallo stdout)*:
  1. **il volume:** **`Get-Volume -DriveLetter E`**: **il file system, la dimensione, lo spazio libero** *(due righe)*;
  2. **per ogni cartella** *(fino al secondo livello, e il totale ricorsivo di ciascuna)*: **la dimensione e il numero di file;** **i file oltre `50` MB e oltre `100` MB, elencati;**
  3. **gli stati di partenza:** **il percorso, la dimensione, lo sha1 dei byte;** **lo sha1 cercato nei referti** *(i primi `8`, `12`, `40` caratteri)*; **gli sha per chiave contro il jsonl;**
  4. **la proposta** *(stampata, non eseguita)*: **(a) nel repo** *(diretto sotto `50` MB per file, o Git LFS)*, **(b) una copia fuori, (c) lo spazio di ciascuna.**
- **Il registro:** **«breve», `inventario-E`.**
- ### **MI FERMO SE:** **un file di uno stato di partenza MANCA, o gli sha per chiave non coincidono col jsonl** *(un dato perso o cambiato: FERMO e lo dico)*. **Poi FERMO comunque: la decisione e' di Luca.**

## 3. TODO

1. **Questo, committato.** 2. **Lo script, l'inventario, la suite, il commit.** 3. **La corsa nel registro; il referto `doc/referti_l2/inventario_E.txt`; la relazione; commit e push.** 4. **FERMO per Luca; i bracci continuano.**

## 4. L'ESITO E LA PROPOSTA

- **Il referto `doc/referti_l2/inventario_E.txt`** *(il codice a `a0da5ee1`, dalle `16:31` alle `16:38:04`; nel registro `inventario-E`, «breve», accanto a `p6-G`)*: **nessun problema negli stati di partenza.**
- ### **IL VOLUME E: `exFAT`, `256.0` GB, liberi `224.3` GB.** ### ⚠ **exFAT NON ha un journal** *(una scrittura interrotta da uno stacco o da un riavvio forzato puo' lasciare il file system incoerente; da verificare per questo disco)*: **una ragione in piu' per la copia.**
- **Le cartelle di E: nominate nel codice: DUE.** **`E:\soliton_simulator` `2.776` GB in `360` file** *(le mappe `1623` MB, gli stati `820` MB, `ripresa_R1` `189` MB, `due_giri` `115` MB, `libreria` `23` MB)*; **`E:\soliton_archivio` `5.313` GB in `197` file** *(l'era 1: `csv/_test_fork` `3693` MB, `csv/_seal_fork` `1511` MB, `spostati_2026-09-22` `108` MB)*. ### **Nessun file oltre `50` MB.**
- **Gli stati delle corse:** **`114` registrati, TUTTI su E:, `0.826` GB, nessuno mancante.**
- ### **GLI STATI DI PARTENZA** *(dichiarati dagli script)*: **C35-pi `60000` `9.0` MB `d5fa30ac`; TBS `10000` `2.3` MB `ae69c52d`; TM1000 `13333` `2.3` MB `b0126349`; S162 `10000` `9.0` MB `7a2bdc7e`** *(sha1 dei byte)*: **ciascuno ha gli sha per chiave UGUALI al jsonl** *(`6` chiavi)*, **e lo sha1 dei byte e' gia' citato negli indici delle mappe** *(`doc/referti_l2/mappe_indice*.txt`)*.
- ### **UN'OSSERVAZIONE FUORI DAL MANDATO** *(non inventariata: e' sul disco del repo, non su E:)*: **`db/` del repo e' IGNORATO da git e pesa `769` MB** *(fra cui `db/accensione_lenta`, da cui le corse leggono la tabella della fase `c(t)`: `corsa_accensione.DIR_NPZ`)*: **anche quello e' in UNA sola copia.**
- ### **LA PROPOSTA** *(NON eseguita; la decisione e' di Luca)*:
  - **(a) NEL REPO, DIRETTI** *(tutti sotto `50` MB: Git LFS NON serve)*: **i `4` stati di partenza** *(`22.6` MB)* **e la tabella della fase** *(`db/accensione_lenta`, il file `CA.FASE`, da misurare)*: **sono i file senza i quali i referti delle prove non si rigirano.** **Tutti i `114` stati** *(`0.826` GB)* **nel repo li porterebbe in ogni clone per sempre: NON lo propongo.**
  - **(b) FUORI DAL REPO, UNA COPIA INTERA** *(un secondo disco o un servizio esterno)*: **`E:\soliton_simulator` e `E:\soliton_archivio`** *(`8.088` GB)*, **piu' `db/` del repo** *(`0.769` GB)*.
  - **(c) LO SPAZIO:** **(a) circa `23` MB nel repo** *(piu' la fase)*; **(b) circa `8.9` GB per la copia.**
- ### **FERMO per la decisione di Luca sull'inventario;** **i bracci di P6 continuano.**

## 5. LA DECISIONE DI LUCA

- ### **LA DECISIONE DI LUCA** *(`2026-11-13` `16:55`)*: **letto; per ora NESSUNA azione** *(niente stati nel repo, niente copia, niente NTFS)*; **la proposta resta registrata nel referto per una decisione futura.** **La coda continua: i bracci di P6.**
