# LA CORSA DI CONTROLLO SENZA BORDO E SENZA MITOSI *(il mandato unico di Luca `2026-11-17` `15:22`)*

> **Il mandato:** **nei test della mitosi il bordo assorbente si toglie** *(decisione di Luca)*; **prima, il controllo: lo stesso mattone, SENZA bordo e SENZA mitosi.** **Tre corse di `3000` tick dallo stato iniziale della fase `0`** *(`prova_scatola5`)*: **C1** `L 186` CON il bordo *(il riferimento, e la prova di determinismo contro gli stati salvati della fase `0`)*; **C2** `L 186` SENZA; **C3** `L 324` SENZA. **Le misure ogni `50` tick; gli stati ogni `250` con lo sha1; il referto con le serie affiancate, le previsioni VERE/FALSE e una figura.** **Nessun file del nucleo; nessuno script in uso modificato; al piu' `5` processi.**

## 1. LE PREMESSE DAL CODICE *(cosa credo; cosa NON so)*

- **Il cammino della fase `0`** *(`csv/solitone/prova_scatola5.py`, `corsa`, letto oggi; NON cambiato dopo quella corsa: l'ultimo commit `9aa7e7f9`, `2026-11-16` `17:45`, la corsa dalle `19:xx`)*: **lo stato da `0`** *(`C243.francobollo_L162("MGU", 0)`, `MT.vuoto_fresco`, `nodo_buono`, `MT.incolla`, `r5`, `metti_bordo(2 R_ogg)`, `PO.campi`)*; **il tick:** `mattone_cottura.Corsa.passo` *(che chiama `mattone.Campi.tick`: G+U, poi `bordo.assorbi` e la correzione di Gauss del bordo)*, col lapse «caldo» di `porto.accendi`; **le misure** *(`r5` e `raggio` ogni `50`, `dphi_nodi` ogni `100`, `residuo` di Gauss, le etichette di `Corsa` ogni `CT.OGNI`)*.
- ### **SENZA BORDO: `Z["g_e"] = 0` sullo STESSO cammino** *(la mia scelta, e il perche')*: **`bordo.assorbi` con `g = 0` moltiplica per `1`, e la correzione di Gauss del bordo con `drho = 0` somma `0`**: **il tick e' allora quello di `tick_GU`** *(il mandato: «si usa quello»)* **E C2 differisce da C1 SOLO per il bordo** *(lo stesso lapse caldo, le stesse misure)*. ### **Lo PROVO** *(il caso noto K2)*: **un tick di `Campi.tick` con `g_e = 0` contro un tick di `p6_bracci.tick_GU` dallo stesso stato: AL BIT.** **Se non e' al bit, FERMO e lo dico.**
- **C1 al bit contro la fase `0`** *(S2)*: **NON so** se le mie misure in piu' *(`energia.corrente`, `termini_di_h`)* toccano lo stato: **`termini_di_h` chiama `motore.elicita`, che RISCRIVE `st["h_int"]`**: **le misure si fanno su una COPIA** *(`h_int`, `rho`, `Lambda` nuovi)*. **E il confronto e' quello di `prova_scatola5`** *(`legati.uguale`, esclusa `h_int`)*.
- **La ripresa al bit** *(Q-A3)*: **`prova_scatola5.salva` scrive in `MT.DIR_E` coi nomi della fase `0`**: **NON lo uso** *(sovrascriverebbe)*; **gli stati in `E:/soliton_simulator/controllo/<nome>/`** con le chiavi, `campo_A`, `campo_E`, `cs_prec` e il `meta`; **la ripresa come `prova_scatola5`** *(`carica`, `porto.accendi(cs)`, `Corsa`, le etichette, `inizio`)*. **La prova** *(K3)*: **`20` tick di fila contro `10` + salva + riprendi + `10`, AL BIT** *(esclusa `h_int`)*.
- **Il caso noto K1** *(il mandato)*: **il vuoto F3 puro, senza bordo, `100` tick: la norma e l'energia costanti all'arrotondamento, il flusso di massa `0`.** ### **NON so per l'energia:** **QC dice che l'energia e' conservata al SECONDO ordine, non esattamente** *(`doc/ALBERO_era2.yaml`, `DEC-QC-CONSERVATA`)*: **se deriva, lo scrivo, e non e' un difetto.**
- **I costi** *(da misurare, S4)*: `L 186` circa `3`-`4` s per tick *(il registro della fase `0`)*; `L 324` circa `3` volte *(i nodi)*: **C3 circa `10` ore.**

## 2. LE PREVISIONI DEL GUARDIANO *(copiate dal mandato, PRIMA di ogni corsa)*

- **P-SB1.** Norma conservata entro `1e-12` relativo in C2 e C3 per tutti i `3000` tick. Energia: nessuna previsione; la deriva si misura e si dichiara.
- **P-SB2.** In C2 il flusso NETTO di energia agli anelli `30` e `45`, mediato sugli ultimi `500` tick, e' sotto il `20%` di quello di C1 negli stessi tick.
- **P-SB3.** In C2 la PARTE POSITIVA del flusso agli anelli `30` e `45` resta sopra il `50%` di quella di C1 *(il rientro aggiunge flusso entrante, non toglie l'uscente)*.
- **P-SB4.** Il primo scarto visibile fra C2 e C1 all'anello `45` *(oltre il `10%`)* arriva prima del tick `400`; in C3 piu' tardi, col rapporto dei tempi `324/186 = 1.74` entro il `20%`.
- **P-SB5.** In C2 la massa entro `12.4` al tick `3000` e' piu' alta che in C1, e R_ogg al `5%` supera `25`.

### LE MIE, accanto *(dai numeri gia' nel repo)*
- **P-SB1:** **la credo VERA** *(ogni pezzo del tick e' unitario sulla norma; senza bordo nulla esce)*.
- **P-SB4:** **NON so**: **il fronte della coda al `2%` avanza di `0.0212` nodi per tick** *(`ee7b8215`)*: **se lo scarto viaggia con lui, `400` tick non bastano**; **ma lo scarto a `45` nasce dove il bordo comincia** *(`R_A = 50`: cio' che C1 toglie e C2 no, e torna indietro da `50` a `45`)*, **non dal giro del toro**: **allora il tempo NON scala con `L`**, e il rapporto `1.74` non ci sarebbe.
- **P-SB5:** **la massa entro `12.4` piu' alta in C2: la credo VERA ma di poco** *(il bordo toglie `0.12`-`0.17` per tick, `flusso_uscente.txt`: circa `450` su `9.9e5` in `3000` tick)*; **R_ogg al `5%` oltre `25`: NON so.**

## 3. PROGETTAZIONE DEL RAGIONAMENTO

1. **Lo script** `doc/referti_l2/controllo_senza_bordo.py` *(file nuovo; importa, non modifica)*: i comandi `caso` *(K1, K2, K3)*, `costo` *(S4)*, `corsa`, `referto`.
2. **I casi noti prima di ogni corsa; poi il costo** *(`100` tick su `L 186`, `10` su `L 324`; la misura completa cronometrata)*: **se una misura costa piu' del `10%` dei `50` tick fra due misure, la cadenza va a `100`** *(dichiarato)*.
3. **Le tre corse** nel registro *(«lunga»; la seconda e la terza con `--forza` e la decisione di Luca)*, le tappe su E:, **la stima di durata misurata scritta nella voce.**
4. **Il referto**: le serie affiancate, le cinque previsioni VERE/FALSE coi numeri e le barre *(le medie su finestre: la deviazione standard e il numero di punti)*, **una figura** *(il flusso netto e positivo agli anelli `30` e `45` nel tempo, C1/C2/C3)*.
- **Cosa mi FERMEREBBE:** K2 non al bit *(il «senza bordo» non sarebbe `tick_GU`)*; K3 non al bit *(la ripresa)*; **C1 non al bit contro la fase `0`: FERMO su C1, C2 e C3 proseguono** *(S2)*.

## 4. TODO DEL NEXT STEP

1. questa carta *(con le previsioni)*: commit e push;
2. lo script; commit; i casi noti; il costo; commit;
3. le tre corse;
4. il referto e la figura; commit; **FERMO col referto.**
