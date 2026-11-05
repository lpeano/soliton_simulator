# 2026-11-05 — `TBS`: LA PARTENZA SIMMETRIZZATA DI `TS` COL BORDO DI `TB3` *(il mandato di Luca del `2026-11-04` `18:31`, la voce `2` della coda)*

> **La domanda** *(Luca)*: `TS`, senza bordo, e' la corsa che partiva PRIMA di tutte *(`~4000`)*. **Col bordo e' la conferma piu' severa della lettura (b1) di `TB3`** *(il moto veniva dalla scatola chiusa)*, al prezzo di una corsa *(`~5.4` ore)*.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*
- **La corsa** *(`csv/solitone/corsa_accensione.py`)*: `TBS` = la partenza di `TS` *(`SIMMETRIZZATE`: `partenza_ts`, `q+` e l'inviluppo sul nodo simmetrizzato, l'asimmetria in ogni campione)* **piu' il bordo di `TB3`** *(`BORDO`: `g_max 0.03`, `R_A 28`, `phi0(t) = c(t) F3` dalla stessa tabella `fase_F3.npz`, l'arresto (i), la fase della fascia, i conti del bordo)*; `VUOTI` `F3`; `CORSE` `(1000, 30000)`. ### **Niente cambia nel codice della corsa se non le quattro voci di configurazione:** il bordo e la simmetrizzazione sono gia' due rami indipendenti *(`if nome in BORDO`, `if nome in SIMMETRIZZATE`)*, e qui si accendono insieme per la prima volta.
- ### ⚠ **UNA PREMESSA DA CONTROLLARE PRIMA DELLA CORSA: IL BORDO RISPETTA LA SIMMETRIA DI `TS`?** Il profilo `g` e' radiale attorno a `c0`, **il centro periodico del campione `0`**; la simmetria di `TS` e' **`R180` attorno a `m2 / 2`** *(`dove_simm`, piu' `sigma_z` su psi)*. **Se `c0` non cade esattamente sul centro di `R180`, l'assorbimento rompe la simmetria** e l'asimmetria di `TBS` crescerebbe per il bordo, non per il caos. **Il controllo** *(una sonda, `doc/referti_l2/accensione_lenta/diag_tbs_bordo.txt`, committata prima della corsa)*: sulla partenza di `TBS`, **l'asimmetria del profilo `g`** sotto `R180`, e **l'asimmetria dello stato dopo un tick col bordo contro un tick senza**. ### **Se il bordo aggiunge un'asimmetria sopra il pavimento dell'arrotondamento** *(`~1e-15`, il primo campione di `TS`: `8.3e-16` psi, `1.1e-16` phi)*: **FERMO, decide Luca.**
- **Che cosa ci si aspetta dalla simmetria, da `TS`** *(`ts_corsa.txt`)*: senza bordo **l'asimmetria di psi supera `1e-12` a `565.5`, `1e-6` a `1092.0`, `1e-2` a `1381.5`** *(phi: `486`, `1005`, `1290`)*: **il caos amplifica l'arrotondamento in `~1400` unita'.** Se il bordo e' simmetrico al pavimento, `TBS` deve rompere la simmetria **negli stessi tempi entro qualche e-fold** *(`~25`-`35` unita' l'uno, `D0R`)*.
- **Il riferimento del bilancio `BM`:** il gemello SENZA bordo di `TBS` e' **`TS`** *(la stessa partenza)*, non `TF3`: **`BM` di `TBS` = il bilancio meno la deriva di `M` di `TS` agli stessi tick** *(il criterio di Luca del `2026-11-04` `18:31` per `TB3`, applicato al gemello giusto: lo dichiaro qui, e' la sua lettura naturale, non una scelta nuova)*; **`BM-F`** con la deriva per `2`.
- **Il costo:** **`~5.4` ore** *(come `TB3`: `978` s il primo pezzo; l'asimmetria in ogni campione costa poco in `TS`)*; la stima vera dopo il primo pezzo. **I dischi** *(prima della corsa, `shutil.disk_usage`)*: nel commit della stima. **Il repo:** `~43` MB di jsonl *(come `TB3`)*.
- ### **NIENTE MAPPE, NIENTE STATI** *(come nel mandato delle `18:31`)*: **la domanda mia a Luca** *(salvarli? il task history `2026-11-05_forma_isotropia_corona`, 5.1)* **e' stata rifiutata col menu e resta APERTA.** **Quindi su `TBS` la carta della forma e la parte (c) della corona NON si potranno fare.**
- **Cosa NON so:** se l'asimmetria della partenza di `TBS` sara' quella di `TS` al bit *(la stessa `partenza_ts`, la stessa scena: deve)*; se il bordo, togliendo l'alone, cambia la crescita del caos *(un fatto da misurare, non da prevedere)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO
| | il passo | cosa decide | cosa mi farebbe FERMARE |
|---|---|---|---|
| `1` | il codice della corsa *(le quattro voci)* e la sonda, committati | -- | -- |
| `2` | **la sonda del bordo sulla simmetria** | se il bordo rispetta la simmetria di `TS` al pavimento | il bordo aggiunge un'asimmetria sopra il pavimento: **FERMO** |
| `3` | `D6`, la cassetta, i dischi, la corsa *(un pezzo alla volta finche' dice «finita»)* | -- | `C:` sotto `6` GB **FERMO** |
| `4` | **la carta del referto `carta_tbs.py`** *(committata prima di girarla, durante la corsa)*: come `tb3_corsa.txt`, **contro `TS` e `TB3`**; i DEVE `P0` *(il primo campione di `TBS` = quello di `TS`, `per` ed `E`, al bit)*, `P0-F` *(deve fallire: = quello di `TB3`)*, `BR`, `BM` e `BM-F` contro `TS`, `BV`, `A4`; **quando la simmetria si rompe, contro `TS`** | le letture di Luca | un DEVE fallito |

### LE LETTURE DI LUCA *(scritte prima di girare; il mandato delle `18:31`)*
- **(t1)** `TBS` non parte entro `30000`: due casi su due col bordo, **il solitone isolato e' fermo**.
- **(t2)** `TBS` parte: **il bordo non basta a fermare il moto**. Il caso di `TB3` era di un seme fortunato, e la lettura (b1) non regge da sola.
- **(t3)** altro, da descrivere.
- ### **Le due cautele di (b1), sempre accanto** *(Luca `18:31`)*: ① una corsa sola per caso, e senza bordo le partenze erano sparse *(`~4000`, `~9500`, `~16000`)*; ② il bordo toglie INSIEME il rientro dal toro e l'accumulo dell'alone.

## 3. TODO
1. Questo task history, un commit.
2. Le quattro voci di `TBS` in `corsa_accensione.py` e la sonda `diag_tbs_bordo.py.txt`, un commit; la sonda girata, un commit col suo esito *(FERMO se il bordo rompe la simmetria)*.
3. `D6`, la cassetta; i dischi nel commit della stima; la corsa in background.
4. Durante la corsa: `carta_tbs.py` committata; il task history della coppia *(il mandato di Luca del `2026-11-05` `12:49`, solo scrittura)*.
5. A corsa finita: il referto, l'esito qui, la relazione.

## 4. L'ESITO DELLA SONDA DEL BORDO SULLA SIMMETRIA *(`doc/referti_l2/accensione_lenta/diag_tbs_bordo.txt`)*: **IL BORDO RISPETTA LA SIMMETRIA DI `TS`, AL BIT**
- **Il centro periodico `c0` = il centro di `R180` `m2 / 2` = `(40.5, 40.5)` al bit** *(lo scarto `0`)*; ### **il profilo `g` per estremita' e' simmetrico ESATTAMENTE** *(`|R g - g| / |g| = 0`, su `22326` estremita' con `g > 0`)*.
- **L'asimmetria della partenza:** psi `8.3e-16`, phi `1.1e-16` *(quella di `TS`, `ts_corsa.txt`)*.
- ### ⚠ **UN FALSO-ZERO, dichiarato:** **al primo tick il bordo non assorbe niente** *(`M` e `V` assorbite `0`: nella fascia la materia e' `0` e il vuoto e' gia' `c(1) F3`)*, **quindi il confronto «un tick con e senza bordo» (`+0`) non poteva vedere nulla.** **La prova e' la simmetria esatta di `g`**, insieme a quella del vuoto di riferimento *(`F3`, l'asimmetria di phi `1.1e-16`)*. **Nessun FERMO:** la corsa parte.

## 5. `TBS` FERMA PRIMA DI PARTIRE *(`2026-11-05`)*: **ATTENDE LA DECISIONE DI LUCA SU MAPPE E STATI**
- **Pronta:** la sonda passa *(4)*; `D6` a `a75b7343`, la cassetta `105/105`; **i dischi `C:` `24.36` GB, `E:` `228.03` GB.**
- ### **NON PARTE:** Luca mi ha girato il rapporto del guardiano, che **consiglia** di salvare in `TBS` le mappe *(come `TB3`, `~90` MB)* e gli stati completi *(con la fase, ogni `1500` unita' piu' `t 0`)*, **con una decisione scritta come PROPOSTA** *(«se sei d'accordo, manda»)*. **Non la tratto come una decisione di Luca:** partire ora senza mappe ne' stati perderebbe l'occasione, partire con renderebbe mia una scelta sua. **Il criterio di chiusura:** Luca manda la decisione, o dice di partire come scritto.

## 6. LA DECISIONE DI LUCA *(`2026-11-05` `13:16`, confermata alle `13:27`; non mia)*: **`TBS` SALVA LE MAPPE E GLI STATI COMPLETI**
- **`TBS` non era partita** *(5)*: **vale la decisione delle `13:16`** *(quella delle `13:27` -- fermarla e ripartire, coi pezzi vecchi come confronto -- valeva solo se fosse partita)*.
- **Le mappe come `TB3`** *(`rho` e `Lambda`, ogni `100` tick, su `E:`, con l'indice nel repo)*.
- **Gli stati completi** *(psi e phi, tutte le componenti, complessi: la fase compresa)* **ogni `1500` unita' di tempo, piu' lo stato a `t 0`**: `0, 1500, ..., 30000`, **`21` stati**, su `E:`, con l'indice e lo sha nel repo.
- **Lo spazio su `C:` ed `E:` nel commit della stima**, prima di partire.
- ### **DEVE** *(nella carta del referto)*: **lo stato salvato a un tempo, ricaricato e confrontato col campione della corsa allo stesso tick, da' `M` e il centro AL BIT.**
- **Il resto invariato** *(la sonda del bordo sulla simmetria, gia' passata: 4)*.
- ### **UNA PREMESSA DAL CODICE:** `corsa_accensione` salva gli stati **dentro il ciclo, dopo un tick** *(e dopo l'assorbimento del bordo: lo stato del campione)*: ### **lo stato a `t 0` non lo salverebbe mai.** **Serve un ramo nel blocco del campione `0`**, che salva nello stesso modo *(lo stesso file, `%s_stato_%06d.npz`, le stesse chiavi, lo sha nella riga)*: **inerte per le corse senza `0` in `STATI`** *(oggi nessuna)*.

## 7. `TBS` IN VOLO: LA STIMA E IL PRIMO PEZZO *(`doc/referti_l2/accensione_lenta/diag_tbs_volo.txt`: `carta_tbs.py` girata sul primo pezzo, un controllo e non un referto; PROVVISORIO)*
- **Il primo pezzo** *(`0 -> 10000` tick)*: **`923` s**; `20` pezzi: **`~5.1` ore**. **I dischi** dopo il primo pezzo: `C:` `24.53` GB, `E:` `228.02` GB; **su `E:` la prima mappa e gli stati a `t 0` e `1500`** *(`4517388` byte i due)*.
- **`9/10`:** `P0`, `P0-F`, `BR`, `BM` *(`2.4e-14`)*, `BV`, `A4`, `ST-L`, **`ST-M`** *(`t 0` e `1500` al bit)*, `ST-M-F`. ### **`BM-F` «fallisce» sul primo pezzo, come scritto prima** *(1 e 5.12 di `TB3`)*: **la deriva di `TS` a `1500` vale `5.8e-12`, sotto `1e-10`: `BM-F` puo' fallire solo verso la fine** *(a `30000` `~1.16e-10`)*. **Non e' un errore della carta.**
- ### **LA SIMMETRIA SI ROMPE NEGLI STESSI TEMPI DI `TS`:** psi sopra `1e-12` a `528` *(`TS` `565.5`)*, `1e-6` a `1081.5` *(`1092`)*, `1e-2` a `1441.5` *(`1381.5`)*; phi `454.5`, `963`, `1314` *(`486`, `1005`, `1290`)*. **Il bordo non anticipa la rottura.**
