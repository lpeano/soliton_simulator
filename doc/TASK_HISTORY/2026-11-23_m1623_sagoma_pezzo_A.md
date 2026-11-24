# [M1623] PARTE 1: LA CHIUSURA DEL PEZZO A NELLA SAGOMA E NEL PROGETTO DEI VINCOLI *(Luca, 2026-11-23, «sì va bene»; il mandato letto alle `16:24` da `date`)* [[PROGETTO-MITOSI]]

> **Solo documenti:** nessuna corsa, il nucleo non si tocca. **[M0528] e' FERMO e non si riapre.** `git log --all --fixed-strings --grep "[M1623"` alle `16:24`: **nessun commit** -- nessun pezzo gia' fatto.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di scrivere, e cosa NON so)*

- **Le fonti dei numeri:** `doc/referti_l2/lapse_vincolo.txt`, `lapse_vincolo_v2.txt`, `lapse_vincolo_giudizio.md` *(`dac9aecb`)*. **Nessun numero nuovo:** la sagoma si aggiorna solo con numeri misurati e la loro fonte *(`doc/SAGOMA.md` sez. `5`)*.
- **«M5 della stella polare»:** `doc/STELLA_POLARE.md` **non ha un M5**; **M5 e' la riga della sagoma, sez. `3`** *(«il tempo e la caduta dalla STESSA grandezza (N da vincolo)»)*. La leggo cosi', e lo dico.
- ### **UNA PREMESSA DEL MANDATO CHE NON TORNA COI NUMERI:** il mandato scrive *«il corpo pesante che si scava il pozzo piu' profondo cade MENO»*. **Dai referti:** `scena_calciata` moltiplica `psi_h` per `sqrt(scala)` *(`massa_calcio.py`)*, quindi `x1.2` e' il corpo con piu' norma; **col vincolo** V2 `|a|` `3.15e-6` a `x0.8`, **`4.37e-6` a `x1.2`**; V3 `2.21e-6`, **`3.11e-6`**: **il corpo piu' pesante si muove DI PIU'** *(V2 VIA, V3 VERSO)*; **senza vincolo il contrario** *(V2 `5.53e-6`, `4.90e-6`)*. **Nella sagoma scrivo i numeri, non la frase;** la discrepanza va a Luca.
- **S19 come la scrive Luca:** *«con N risolto Eotvos raddoppia e cambia segno»*: **raddoppia** = `|eta| x2.70` V2, `x2.45` V3; **ma V2V3 `x1.35` e SENZA cambio di segno.** La riga porta i tre numeri.
- **Cosa NON so:** se la sagoma su `primo-ordine` e' la stessa di `lapse-u` *(la verifico prima di copiarla)*.

## 2. PROGETTAZIONE

- **1a** `doc/SAGOMA.md` su `lapse-u`: S4 e S5 con la riga del lapse risolto; **S19 nuova**; **M5** col testo di Luca; **una sezione `4-bis`** con la tabella del giudizio del pezzo A copiata da `lapse_vincolo_giudizio.md`. Ogni sostituzione con l'ancora asserita unica. Commit, push. **Poi la stessa sagoma su `primo-ordine`** nel giro della relazione *(se il file e' identico; se no, FERMO e lo dico)*.
- **1b** sul ramo `vincoli`, `doc/PROGETTO_VINCOLI.md` sez. `6`: **G2 NON si apre** *(G2 chiede Eotvos sotto l'`1%` senza peggiorare S2, S3, S5: Eotvos va a `0.325`/`0.338`/`0.178`, S5 PEGGIORA contro F0)*; l'ordine: il pezzo C e Q2 i prossimi; Z1-Z4 restano a costo zero. Commit, push.
- **Cosa mi fa FERMARE:** la sagoma diversa fra i rami; un numero del mandato che non trovo nei referti *(lo scrivo e non lo copio)*.

## 3. TODO

1. questo task history, commit;
2. 1a la sagoma su `lapse-u`, la relazione, commit;
3. 1b `PROGETTO_VINCOLI.md` su `vincoli`, commit;
4. la sagoma e la relazione su `primo-ordine`, commit;
5. la Parte 2 sul ramo `mitosi` *(il suo task history e la carta)*.

## 4. ANNOTAZIONI *(le premesse non si riscrivono)*

- **`16:30`** *(da `date`)*: **la sagoma su `primo-ordine` NON e' identica** *(sha1 `7c515bee` contro `bdbea146` di `lapse-u`)*: **e' INDIETRO di tre aggiornamenti** *(S4 e S5 con FH, S16 chiusa, S17, S18, M2)*, ogni differenza nello stesso verso. **Il FERMO della sez. 2 lo avevo scritto per un conflitto; questo non lo e'**: si copia il file di `lapse-u` con lo sha1, e lo dico a Luca.
