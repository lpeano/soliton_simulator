# DOVE VA L'ENERGIA DEL LEGAME? IL CONTO DELL'ENERGIA NEL TEMPO DEL SOLITONE COL TICK INTERO *(il mandato del 2026-10-27, dopo le 10:58)*

> **Il mandato:** di Luca, `2026-10-27` *([[SOLITONE-VUOTO-CONGELATO]], [[SCOMPOSIZIONE-ZERO-LAMBDA]], [[VUOTO-DISTURBATO]], [[PROGETTO-MASSA-COLLETTIVA]])*: ### **l'idea di Luca delle `10:54`: «l'interazione col vuoto dovrebbe essere disturbata dall'energia rilasciata»;** ### **un oggetto si lega davvero solo se l'energia di legame viene portata via.** ### **In che VERSO va lo scambio fra la materia e il vuoto?** ### **La decisione delle `10:58`: su griglia fissa, niente mitosi.**
> ### **In memoria; nessun file del nucleo; B-4, B-5 e l'impronta `2e7f795d2a52fbe7` intatte.** ### **Lo script `csv/_energia_del_legame.py`, il referto `doc/referti_l2/energia_del_legame.{txt,jsonl}`.** ### ⚠ **Il processore e' condiviso con la corsa di `C2`.**

**LIVELLO:** una misura dinamica, coi riferimenti.

## 0. LA STELLA POLARE

1. **`A14`:** ### **`M`, `V` si conservano; e l'ENERGIA e' cio' che si conta.** 2. **Il gradino:** ### **dove va l'energia del legame.** 3. **Aggiunge un numero o una legge?** ### **No:** ### **le regioni sono una scelta di LETTURA, dichiarata qui.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No** *(`cs` spento come in `74f99039`)*. 5. **Emergente o imposto?** ### **Il verso dello scambio e' cio' che si misura.**

## 1. QUALE ENERGIA IL TICK CONSERVA *(letto dal codice, dichiarato prima)*

- ### **I pezzi del tick e le loro fasi** *(letto da `flussi_parziali` e `materia_vuoto.applica`)*: ### **i pezzi della camminata applicano `exp(i pi s g)` col generatore `g` di un proiettore;** ### **il legame `CAMM-MATERIA-VUOTO` applica `exp(-i alpha dtau f)` a `psi` e `exp(-i beta dtau f)` a `phi`.** ### **In tutti e due la fase per tick e' `-s` volte la derivata di un'energia** *(per la camminata `0fb93b8c` lo ha misurato: `-arg/s = -4.64` contro `e_K = -4.71`;* ### *per il legame `alpha = F_1'`, `beta = F_1 - x F_1'`, cioe' le derivate di `Lambda F_1(rho/Lambda)` rispetto a `rho` e a `Lambda`)*.
- ### **QUINDI L'ENERGIA E':** ### **`H_tot = H_cam(psi) + H_cam(phi) + sum_k Lambda_k F_1(rho_k / Lambda_k)`** *(`H_cam` da `energia_pesata.termini_di_h` con l'altro campo a zero: cosi' l'`N` `S3` scritto li' vale `0`, e il legame e' quello di `S1`)*, ### **coefficiente `1` fra i pezzi.**
- ### **OGNI PEZZO CONSERVA ESATTAMENTE IL SUO TERMINE** *(la camminata e' unitaria col suo generatore; il legame e' una fase che non cambia `rho` ne' `Lambda`)*; ### **la COMPOSIZIONE no:** ### **il passo e' palindromo, quindi `H_tot` si conserva a meno di termini di ordine `s^2` per i commutatori, LIMITATI, senza deriva secolare.** ### ⚠ **COSA NON SO:** ### **il prefattore** *(la taglia dei commutatori con questa materia)*: ### **il riferimento e' la corsa `(b)`.**
- ### **Nella corsa `(b)`** *(il vuoto congelato: i suoi pezzi saltati e `phi` rimesso)* ### **l'energia del vuoto e' costante AL BIT** *(lo stesso `phi`)*, ### **e la materia gira in un potenziale fisso:** ### **`H_cam(psi) + legame` si conserva allo stesso ordine.**

## 2. LO ZERO *(dichiarato prima)*

- ### **Lo zero SIMMETRICO** *(`lambda 1/2`, `_triangoli_bassa_energia.conv("simm")`, la stessa convenzione di `74f99039`)* ### **e' il principale; lo zero di oggi il controllo.**
- ### **Le energie a `lambda`:** ### **`termini_di_h` scrive lo zero di oggi;** ### **a `lambda` si aggiunge `2 pi lambda` per unita' di norma, alla materia E al vuoto** *(lo spostamento MISURATO in `0fb93b8c`: `2 pi lambda` entro `8.9e-15` per la materia, e lo stesso per la rotazione del vuoto)*. ### **Le DIFFERENZE fra i tempi, per pezzo e per regione, cambiano solo di `2 pi lambda` volte la differenza di norma della regione** *(`M` e `V` totali si conservano)*: ### **la dinamica nelle due convenzioni differisce di una fase globale per pezzo.**

## 3. LA MISURA *(fissata qui)*

- ### **Il solitone `S1` di `74f99039`:** ### **`s 0.3`, `N 1e6` a `L 81` e `120`, `N 1e5` a `L 48` e `69`** *(i fattori `12` e `18` della larghezza)*, ### **lo stato del risolutore** *(le righe di `_solitone_vuoto_congelato.corsa`, copiate col parametro `N`;* ### *il criterio `0` le confronta col jsonl)*, ### **`T_MAX 2000`, le energie ogni `10` tick.**
- ### **Due corse:** ### **`(a)` il tick intero; `(b)` il vuoto congelato.** ### **Ognuna coi due zeri:** ### **`16` corse.**
- ### **I PEZZI:** ### **la materia** *(i costituenti `M e_K(lambda)` e la cinetica `H_cam(psi) - M e_K`, con `e_K(0)` dello stato uniforme del ramo come in `dc4a1437`)*, ### **il legame, il vuoto** *(`H_cam(phi)`)*, ### **`H_tot`.**
- ### **LE REGIONI, dichiarate qui:** ### **VICINO = i nodi entro `2` larghezze iniziali** *(`2 w_in`, la larghezza quadratica media a `t 0`)* ### **dal centro iniziale; LONTANO = il resto; e il totale.** ### **I termini d'arco a meta' fra i due nodi dell'arco.**
- ### **LE GRANDEZZE:** ### **`Delta E` di ogni pezzo e di ogni regione fra `t 0` e la vita** *(`320` per `N 1e6`, `140` per `N 1e5`: `VITA_RIF` di `74f99039`)* ### **e a `T_MAX`;** ### **il FLUSSO** *(l'energia che arriva lontano, `Delta H_tot(LONTANO)`, nel tempo)*; ### **il segno dello scambio fra il legame e il vuoto vicino.**
- ### **IL FRONTE** *(per la velocita')*: ### **il raggio del nodo piu' lontano dal centro iniziale con `|Lambda_e(t) - Lambda_e(0)| > 1e-6`** *(per estremita'; il vuoto da solo resta sotto, [[VUOTO-DISTURBATO]])*; ### **la velocita' dal fit lineare del raggio nel tempo, fra il bordo della materia iniziale e `0.8` della meta' del toro;** ### **contro `v_max` della coppia** *(`_triangoli_forza.v_max(matrice_L(0, s))`)*. ### ⚠ **La velocita' della luce sui triangoli in queste unita' non la ho da uno strumento committato:** ### **il confronto e' con `v_max` sola** *(e con `1` arco per tick, il cono)*.

| | il criterio | il tipo |
|---|---|---|
| `0` | ### **lo stato a `t 0` = quello di `74f99039`** *(la larghezza al bit col jsonl)*, ### **e la vita** *(campionata ogni `20` tick come allora)* ### **uguale a quella del suo jsonl, per ogni `N`, `L`, modo e zero** | DEVE |
| `1` | ### **`M` e `V` conservati entro `1e-10` relativo; nella corsa `(b)` l'energia del vuoto costante AL BIT** | DEVE |
| `2` | ### **le differenze nel tempo dei pezzi** *(il totale di ogni pezzo, alla vita e a `T_MAX`)* ### **alle due taglie entro `1e-3` di `N |e_K(0)|`** *(la regola di `0fb93b8c`, sulle energie)* | DEVE |
| `3` | ### **le differenze nel tempo dei pezzi coi due zeri uguali entro `1e-6` di `N |e_K(0)|`, tolto `2 pi lambda` volte la differenza di norma** | DEVE |
| `4` | ### **`H_tot` nella corsa `(a)` conservato entro `10` volte la deriva della corsa `(b)`** *(il massimo di `|H_tot(t) - H_tot(0)|` su `2000` tick)* | PUO' FALLIRE |

### **LA LETTURA** *(nessuna soglia; il guardiano non sa)*: ### **`(1)` se il vuoto VICINO cresce mentre il legame cala, la materia cede energia al vuoto;** ### **`(2)` se il vuoto cala mentre la cinetica cresce, il vuoto restituisce energia alla materia e la scalda;** ### **`(3)` quanta energia arriva LONTANO e in che tempo, e la velocita' del fronte.** ### **Mi FERMO** ### **se un DEVE fallisce.**

## 3-bis. ANNOTAZIONE DOPO LA PROVA A VUOTO *(prima della corsa; il paragrafo `3` resta)*

- ### ⚠ **IL FRONTE:** ### **sul toro il profilo della materia del risolutore NON HA BORDO** *(il nodo piu' lontano con materia e' a `37` archi, oltre la meta' del toro `L 48`)*: ### **la finestra del fit «dal bordo della materia» era vuota.** ### **La finestra comincia al bordo di VICINO** *(`2 w_in`, gia' dichiarato)* ### **e finisce a `0.8` della meta' del toro.**

## 4. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa *(in binario, senza `CRLF`)*; 3. la corsa; 4. il referto, la relazione, l'indice.
