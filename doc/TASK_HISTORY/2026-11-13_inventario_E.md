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
