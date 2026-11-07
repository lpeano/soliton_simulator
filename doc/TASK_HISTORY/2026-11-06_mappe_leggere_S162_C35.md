# 2026-11-06 — LE MAPPE LEGGERE DI `S162` E DI `C35-0` *(Luca `2026-11-06` `23:38`)*

**Il mandato** *(Luca, verbatim nella sostanza)*: **fra la fine di `C35-0` e l'inizio di `C35-pi`** *(solo lettura da `E:`, nessuna corsa)*, `doc/referti_l2/campo_S162/` e `doc/referti_l2/campo_C35-0/`, **`mappe_leggere.npz` e `profili.npz` come `campo_TB3`** *(`float16`, una mappa ogni `150` unita' di tempo, le stesse chiavi, lo stesso riferimento di `dLambda`)*, **col controllo `F1`** *(la massa delle mappe contro i campioni)*. **Su `L 162`: le chiavi `d1`, `d2`, `L` adeguate al reticolo, e il centro del bordo nel file.** **Il byte e il numero delle mappe nel commit.**

**In coda:** arriva **durante il FERMO di IS2** *(`eb8fcf05`, le tre domande a Luca aperte)*. **`[[L-DOPO-STOP]]`: lavoro solo la coda, e non decido al posto di Luca.** **L'ordine e' di Luca: le mappe DOPO `C35-0`** -- **e `C35-0` non e' partita** *(e' la domanda `3` del FERMO)*. **Quindi ora: le premesse, il codice, `D6`, la cassetta; le mappe NON le faccio girare prima del tempo che Luca ha scritto**, neanche quelle di `S162` che si potrebbero gia' fare.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

1. **Lo strumento c'e':** `csv/solitone/carta_campo.py --corsa TB3` *(`PARTI`, `INDICI`)*. **Scrive** `profili.npz` *(`float32`, anelli intorno al centro di `rho`)* **e** `mappe_leggere.npz` *(una ogni `OGNI_LEGGERA = 10` istantanee, `rho` e `dLambda = Lambda - Lambda(t 0)` per nodo in `float16`, `centro`, `d1`, `d2`, `L`, `ogni`)*.
2. **La cadenza torna:** le mappe di `S162` su `E:` sono **`667` istantanee, una ogni `100` tick** *(`15` unita' di tempo; i `7` file contigui, `0 .. 66600`, nessun doppione al confine: letto dai file)*. **Una ogni `10` = una ogni `150` unita' di tempo: `67` mappe** *(`0 .. 9900`)*. **Per `C35-0` lo stesso, se la corsa fa le stesse istantanee** *(lo so solo a corsa finita)*.
3. **La scena: `carta_campo` usa `V.scena` su `V.L` = `81`.** **Su `L 162` va costruita sotto `carta_statiche.scena_con(V.N, 162)`** *(come `carta_s162.py`)*: **`d1`, `d2` vengono dalla scena di `L 162`** *(`int16`, `-81 .. 80`)*, **`L = 162`**, e l'`assert` che l'ordine dei nodi della mappa sia quello della scena **resta**. **E' cosi' che le chiavi sono «adeguate al reticolo»:** dal reticolo, non scritte a mano.
4. **Gli indici `doc/referti_l2/mappe_indice_S162.txt` e `mappe_indice_C35-0.txt` NON esistono.** **`F0` li vuole:** si fanno con `python csv/solitone/corsa_accensione.py --indice S162` *(sola lettura di `E:`)*, **e si committano col referto.**
5. **`dLambda`: lo stesso riferimento di `TB3`** = **`Lambda` della PRIMA istantanea della corsa** *(per nodo)*. **`F2`** *(`Lambda(t 0)` uniforme)* **dovrebbe passare anche per la coppia:** la partenza tocca solo `psi` *(il vuoto `F3` e' lo stesso; `C0` lungo l'ha gia' visto uniforme su `L 162`)*.
6. ### ⚠ **`F3` NON SI PUO' FARE COME IN `TB3`:** `TB3` ricalcola `V.partenza` su `L 81`; **la partenza della coppia** *(la copia traslata di `d`, col segno)* **la costruisce la corsa dentro `corsa_accensione.py`, e non c'e' una funzione da chiamare.** **La mia scelta, dichiarata:** **per le corse di `L 162`, `F3` confronta `rho(t 0)` della mappa con la densita' dello STATO COMPLETO a `t 0` su `E:`** *(il file degli stati, col suo `sha` registrato nel jsonl)*: **e' lo stato vero, piu' forte del ricalcolo.**
7. ### ⚠ **I PROFILI DI `C35-0` SONO INTORNO AL PUNTO MEDIO:** `TO.centro(rho)` di una coppia e' **il centro della coppia**, dove `rho` e' piccola: **gli anelli non sono il profilo di un solitone, e la portata** *(relativa all'anello `0`, la `rho` al centro)* **perde il senso.** **Tengo la definizione di `campo_TB3`** *(Luca: «come `campo_TB3`»)*, **e lo stampo; la portata di `C35-0` non la leggo.**
8. **La dimensione:** `TB3` `201` mappe di `6561` nodi = `4832348` byte *(compressione `0.916`)*; **`S162` `67` mappe di `26244` nodi: `7033392` byte grezzi, `~6.4e6` compressi: sotto il tetto `TETTO_MB = 10`.** ### ⚠ **Il codice sopra il tetto DIMEZZA** *(una ogni `20`)*: **Luca ha scritto «una ogni `150`»**, **quindi per queste corse sopra il tetto la carta FALLISCE e mi fermo, non dimezza.**
9. **Il centro del bordo:** nel jsonl, `bordo.c0` *(per `S162`: `[98.874, 81.363]`)*, **nelle stesse coordinate di `centro`** *(gli indici `m1`, `m2` della scena; `bordo.c` = `c0 + X` e' il solitone, `X = -17.28`)*. **Nel file: `centro_bordo`, e in piu' `R_A` e `g_max`** *(mie, dichiarate: il centro senza il raggio non dice dov'e' la fascia)*.
10. **Cosa NON so:** **se `C35-0` scrivera' le stesse `667` istantanee**; **se il centro di `TO.centro` della coppia e' stabile** *(due solitoni uguali a `35` nodi: dovrebbe; con `C35-pi`, che qui non c'e', potrebbe non esserlo)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

- **Il codice:** in `carta_campo.py`, **`PARTI`, `INDICI` per `S162` e `C35-0`**; **per i nomi in `CA.LCORSA`:** la scena sotto `scena_con(V.N, L)`; **`F3` contro lo stato a `t 0`** *(e lo `sha` dello stato = quello del jsonl, prima)*; **le chiavi `centro_bordo`, `R_A`, `g_max`**; **sopra il tetto: `F-TETTO` fallisce** *(niente dimezzamento)*. **`TB3`, `TBS`, `TM3`, `TM1000` restano identici** *(un `if` sul nome)*.
- **I DEVE** *(come `campo_TB3`)*: **`F0`, `F0-F`, `F1`, `F1-F`, `F2`, `F3`**; **in piu' `F-TETTO`** *(il file sotto `10` MB a una ogni `10`)* **e `F-B`** *(il `centro_bordo` scritto = `bordo.c0` del jsonl, e la distanza da `centro` della prima mappa = `d/2` per `S162` *(il solitone e' a `d/2` dal centro del bordo)* e `0` per la coppia *(il centro della coppia e' il punto medio)*, entro `0.5` nodi: la soglia e' mia; e' un controllo che il riferimento delle coordinate sia lo stesso)*. **`F-B-F`** *(deve fallire)*: lo stesso col centro del bordo spostato di `L/2`.
- **Il commit delle mappe:** i due `.npz` per corsa, l'indice, il referto, **e nel messaggio i byte e il numero delle mappe** *(dal referto, non ricopiati: `[[L-NUMERI]]`)*.
- **Cosa mi farebbe FERMARE:** `F1` o `F3` che falliscono; il file sopra il tetto; `C35-0` con istantanee diverse da `S162`.

## 3. TODO

1. Questo task history, un commit.
2. Il codice in `carta_campo.py` *(e l'INVENTARIO: i due comandi, il blob)*, un commit; `D6` ripuntato, un commit; la cassetta, un commit.
3. **A `C35-0` finita** *(dopo la risposta di Luca al FERMO)*: gli indici `S162`, `C35-0`; `carta_campo.py --corsa S162`, poi `--corsa C35-0`, una alla volta; i referti `doc/referti_l2/campo_S162.txt`, `campo_C35-0.txt`; il commit coi byte e il numero delle mappe; la relazione, la MAPPA. **Poi `C35-pi`.**

## 4. L'ESITO *(`carta_campo.py` `a58ee6b9`, `e45b8170`; gli indici da `corsa_accensione.py --indice`)*: **`S162` `9/9`, `C35-0` `9/9`**

| | `S162` | `C35-0` |
|---|---|---|
| **`F1`** *(667 istantanee, il peggiore)* | `M 3.33e-09`, `V 4.68e-10` | `M 2.44e-09`, `V 5.47e-10` |
| **`F1-F`** *(deve fallire)* | `5.07e-03` | `2.54e-03` |
| **`F3`** *(contro lo stato a `t 0` su `E:`)* | `2.642e-08` | `2.642e-08` |
| **`F-B`** *(atteso `d/2` = `17.5` il singolo, `0` la coppia)* | `17.5000` | `0.0000` |
| **`F-B-F`** *(deve fallire)* | `63.5000` | `81.0000` |
| **il centro del bordo** *(`c1`, `c2`; `R_A`, `g_max`)* | `98.8738 81.3625`; `47.5`, `0.03` | `98.8738 81.3625`; `47.5`, `0.03` |
| **`mappe_leggere.npz`** *(`F-TETTO`, sotto `10` MB)* | **`5467506` byte, `67` mappe** | **`5785427` byte, `67` mappe** |
| **`profili.npz`** | `761119` byte | `785874` byte |
| **il massimo di `rho`** *(float16, tetto `65504`)* | `5.0640e+03` | `7.6200e+03` |

- **Il punto di arresto «istantanee diverse» non scatta:** `667` per tutte e due. **Il centro del bordo e' lo stesso** *(il bordo di `C35` per `S162`, come deciso)*: **il controllo `F-B` dice che `S162` sta a `d/2` dal centro, e la coppia ci sta sopra.**
- **Gli `.npz` sono sotto il `*.npz` di `.gitignore`:** **si aggiungono a forza** *(`git add -f`)*, **come quelli di `campo_TB3` e `campo_TBS`**.
- **Avanti:** **`C35-pi`** *(lo stesso driver, lo stesso blob di `corsa_accensione.py`)*.
