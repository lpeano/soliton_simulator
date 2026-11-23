# IL LAPSE COME MOLTIPLICATORE: N DAL VINCOLO, NON DA CHI *(il pezzo A del progetto dei vincoli; il mandato di Luca [M0528] Parte 2, 2026-11-23 dopo le `05:20`; scritta PRIMA del codice; il task history `doc/TASK_HISTORY/2026-11-23_torneo_finale_e_lapse_vincolo.md`)* [[PROGETTO-MITOSI]]

> ### **IN TESTA** *(Luca, 2026-11-23, le risposte a D1-D4)*: **«il lapse-moltiplicatore derivato dalle righe e' chi statico senza portata; la domanda del pezzo A e' se un N autoconsistente cambia Eotvos; il segno della caduta non puo' cambiare qui».**

> **Le scelte A1-A5 sono del guardiano su delega di Luca.** **La carta le deriva dalle righe, e dove le righe dicono un'altra cosa lo scrive (sez. 3): TRE PREMESSE DEL MANDATO CADONO, e la decisione e' di Luca.** **Il codice fuori dal nucleo** *(come `doc/referti_l2/chi_tick.py`)*; **2b-2d solo col via di Luca.**

## 0. LE RIGHE DA CUI SI PARTE *(lette il 2026-11-23, prima delle 05:47 da `date`)*

- **Il libro dei conti** *(`csv/_libro_dei_conti.conti_per_nodo`, usato da `csv/solitone/conti.py`)*: **un'energia PER NODO esiste** -- `cost`, `cin`, `leg`, `vuo`, `tot = em + ev + el`. **Non contiene `N`:** e' il conto a `N = 1`.
- **Come l'energia della materia dipende da `N`, nelle righe di `chi`** *(`doc/referti_l2/chi_tick.py`)*: `H = somma w_k H_k + somma w_a H_a - e0 somma (N - 1) rho + K + V + H_chi`, con i pesi `w` da `cs = s N` *(V2)* e il termine `-e0 (N - 1) rho` dalla fase (a) *(V3)*; la forza `F = c2 Delta chi - m2 chi + kappa N (s Q - e0 rho) - c0`, `N = e^{-kappa chi}`, `Q_i = H_k + somma dw H_a` *(`Q_di`)*. **Da `F = -dH/dchi` e `dN/dchi = -kappa N`:** ### **`dH_materia/dN_i = u_i = s Q_i - e0 rho_i`** *(`u_di`)*: **`s Q_i` viene da V2, `-e0 rho_i` da V3.**
- **La tensione di chi:** `H_chi` contiene `1/2 c2 somma_archi (chi_i - chi_j)^2`, `c2 = C_CHI^2 = 0.25` *(D-CHI-VELOCITA', Luca 21/11)*; `kappa = 2.528944153922671e-04` *(chi_parametri_v2, O8)*. **In `N`:** `chi = -ln N / kappa`, quindi la tensione e' `(c2 / 2 kappa^2) somma_archi (ln N_i - ln N_j)^2`, **`c2/kappa^2 = 3.909e+06`** *(python -c prima delle 05:47)*; al primo ordine in `N - 1` e' `(c2 / 2 kappa^2) somma (N_i - N_j)^2`, la forma del mandato.
- **La massa di chi** `m2 = 1/PORTATA^2`, `PORTATA = 100` *(la scelta di Luca del 21/11, A1)*, e **`c0 = kappa m0`**, `m0` = la media di `u` allo stato di partenza: ### **`c0` E' GIA' la sottrazione della media della sorgente.**

## 1. IL VINCOLO, DERIVATO *(A1, A2)*

- **L'energia** *(il mandato A2: la materia per tempo proprio piu' la tensione del lapse, nessuna costante nuova)*: `E[N] = H_materia(N) + (c2 / 2 kappa^2) somma_archi (ln N_i - ln N_j)^2`. **La stazionarieta' rispetto a `N_i`:** `u_i + (c2 / kappa^2) (L ln N)_i / N_i = 0`, con `L = D D^T` *(il `Laplaciano` di `chi_tick`)*. **In `chi`** *(`ln N = -kappa chi`)*: ### **`c2 (L chi)_i = kappa N_i u_i`** -- **e' l'equazione STATICA di chi con `m2 = 0` e senza `c0`.**
- ### **QUINDI, DETTO PRIMA DI TUTTO:** **il lapse-moltiplicatore che si deriva dalle righe e' chi senza inerzia** *(`pi -> 0`: `N` segue la materia istantaneamente)* **e senza portata** *(`m2 -> 0`)*. **La differenza da chi e' esattamente questa, e niente altro:** A1 *(niente inerzia, niente velocita' di chi)* e' rispettato; **«niente sorgente scritta a mano»:** la sorgente `u_i` e' quella delle righe.
- **La soluzione** *(il codice, 2b)*: **diretta**, non per rilassamento *(sez. 3, D4)*: `L` non cambia, si fattorizza UNA volta *(come `Laplaciano.statico`)*; il termine `N_i = e^{-kappa chi_i}` a destra si itera al punto fisso *(`kappa chi ~ 1e-2`: poche iterazioni)*; **la convergenza:** il residuo relativo `< 1e-10`; **K2 conta le iterazioni del punto fisso.**

## 2. I DUE COLLEGAMENTI E LO ZERO *(A3, A4)*

- **Dalle righe, lo zero NON si sceglie: lo fissa il collegamento** -- `dH/dN_i` e' `s Q_i` con V2 *(lo zero a `0`: `eps_i = s Q_i / rho_i`)*, **`-e0 rho_i` con V3** *(nessuna `omega`: `eps_i = -e0`, costante e NEGATIVO)*, **`s Q_i - e0 rho_i` con tutti e due** *(lo zero `e0`: **e' Z1**, ed e' il collegamento di `chi_tick`)*.
- **Z2** *(lo zero `omega_phi = -pi s`, `1.10` di [M1427])*: **non esce dal libro con nessun collegamento**: `-pi s rho_i` sarebbe un termine NUOVO nell'energia *(una legge in piu': `par. 9-ter`)*.
- **`omega_i` misurata su `50` tick** *(A3)* **contro `s Q_i / rho_i`** *(la riga)*: **la riga e' istantanea** *(nessun ritardo: A1 «a ogni tick»)*; `omega_i` media su `50` tick porta un ritardo di `~25` tick. **La mia raccomandazione: la riga** *(`u_di`)*, e `omega_i` come CONTROLLO *(il rapporto `s Q_i / (rho_i omega_i)` nel cuore, stampato)*.

## 3. LE PREMESSE DEL MANDATO CHE CADONO -- ### **LE DOMANDE A LUCA** *(FERMO qui)*

| | la premessa | cosa dicono le righe | le strade | la mia raccomandazione |
|---|---|---|---|---|
| **D1** | «`N -> 1` al bordo» | **la scena della caduta e' un TORO SENZA BORDO** *(`caduta_libera.prepara`: «UN francobollo, SENZA bordo»)*; **su un toro `c2 L chi = kappa N u` NON HA SOLUZIONE se `somma N u != 0`** *(`L` e' singolare; `somma u` del mattone `~ rho_tot (omega - e0) ~ 1.5e+05`, python -c prima delle 05:47)* | **(a)** la media tolta *(`N u -> N u - <N u>` a ogni tick: e' la mossa di `c0 = kappa m0` di chi, che pero' toglie una costante fissata alla partenza; qui la condizione di solvibilita' la obbliga a ogni tick; nessun numero nuovo)* e `somma chi = 0`; **(b)** `N = 1` su un anello a distanza `R` *(un numero nuovo: `R`, e in 2D la profondita' va come `ln(R/w)`)*; **(c)** tenere `m2` di chi *(la portata `100`: allora e' chi statico)* | **(a)**: e' gia' nelle righe di chi; **ma** con (a) `N` lontano e' `> 1` *(la media di `N` e' `1`)*, e in 2D il profilo e' logaritmico fino a `L/2` |
| **D2** | Z1 e Z2 «tutte e due», per V2 e V3 | **lo zero lo fissa il collegamento** *(sez. 2)*: V2 da' lo zero a `0`, V3 da' `eps = -e0` *(N > 1 al centro: un anti-lapse)*, V2+V3 da' Z1; **Z2 non viene dal libro** | **(i)** le tre righe del libro *(V2, V3, V2+V3 = Z1)*; **(ii)** il mandato alla lettera *(Z1 e Z2 incollati su V2 e su V3: quattro leggi scritte a mano)* | **(i)**, e Z2 solo come POSTULATO dichiarato, se Luca lo vuole |
| **D3** | la caduta e Eotvos «con N risolto» | **`N` risolto viene dal mattone stesso: da solo non da' una forza netta sul mattone** *(il campo che uno si fa da se' non lo sposta)*: **la caduta di [M0908] cade in un gradiente IMPOSTO** *(`campo_N`)* | **(i)** `N = N_imposto x N_risolto` *(il gradiente di [M0908] resta, il vincolo si aggiunge: si misura se il vincolo cambia `eta`)*; **(ii)** la sorgente e' un secondo corpo pesante *(e' la coppia, K5)* | **(i)** per confrontare con `eta 0.120 / 0.138` dalla stessa scena, **dichiarando che il gradiente resta imposto**; (ii) e' gia' in K5 |
| **D4** | «per rilassamento, `1e-10` in meno di `200` iterazioni» | **Jacobi o Gauss-Seidel sul laplaciano del toro vogliono `O(L^2)` iterazioni** *(migliaia)* | la fattorizzazione diretta *(sez. 1)*; il gradiente coniugato partito dal tick prima | **la diretta**, e K2 sulle iterazioni del punto fisso |

### 3-bis. LE DECISIONI DI LUCA *(2026-11-23, prima delle `08:31` da `date`; il task history `doc/TASK_HISTORY/2026-11-23_lapse_vincolo_codice.md`)*

- **D1 (a):** la media di `N u` tolta a ogni tick, **`somma chi = 0`**; nessun `R`. **Dichiarato in ogni referto:** `N` lontano dal mattone e' `> 1` e il profilo e' logaritmico.
- **D2 (i):** **le tre righe del libro:** **V2** *(`cs = s N`: lo zero a `0`)*, **V3** *(la fase (a): `eps = -e0`, l'anti-lapse)*, **V2+V3** *(lo zero `e0` = Z1)*. ### **Z2 NON SI FA:** sarebbe una legge nuova; **resta qui come «postulato non adottato».**
- **D3 (i):** **`N = N_imposto x N_risolto` nella scena di [M0908]**; **il gradiente resta imposto, detto in ogni referto**; **la coppia (K5) e' il solo caso con la sorgente vera** *(`N_imposto = 1`)*.
- **D4:** la fattorizzazione diretta e il punto fisso; **K2 sulle iterazioni del punto fisso: `< 20`.**
- **La riga che ne segue** *(mia, dalle righe, scritta prima del codice)*: con `N = N_imp N_ris`, `dH_materia/dN_ris,i = N_imp,i u_i(N)` *(`u_i = s Q_i - e0 rho_i` coi pesi di `cs = s N`, come `chi_tick.forza`; con V3 solo `u_i = -e0 rho_i`, con V2 solo `u_i = s Q_i`)*; la tensione e' solo su `ln N_ris`: ### **`c2 L chi = kappa (N_imp N_ris u - <N_imp N_ris u>)`, `N_ris = e^{-kappa chi}`, `somma chi = 0`.**
- **Il tick:** **all'inizio di ogni tick** `N_ris` si risolve dallo stato a `k`, poi `caduta_segno_v2.tick_var` con `N_imp N_ris` *(V2 `(cs_N, segno) = (True, 0)`, V3 `(False, +1)`, V2+V3 `(True, +1)`: il V1 di [M0908])*. **Non e' palindromo in `N`** *(il vincolo e' letto a inizio tick)*: dichiarato. Il punto fisso parte dal `chi` del tick prima; K2 conta a ogni tick, e al primo **da freddo**.

## 4. I CASI NOTI E I CRITERI *(copiati dal mandato; adattati SOLO dove la sez. 3 lo obbliga, e detto)*

- **A5 / K1:** senza materia `u = 0` e `chi = 0`, `N = 1` ovunque AL BIT *(con (a) anche col vuoto: `u` del vuoto e' uniforme, tolta la media e' zero -- da verificare: il vuoto fresco ha `u` uniforme al bit?)*; il mattone fermo: `N(r)` stazionario *(la variazione `< 1e-6` fra `1500` e `2000`)* e `N(centro) < 1` con Z1; **il profilo contro quello di chi a `2000` tick** *([M1310], il test pulito)*: forma e profondita', la differenza dichiarata; la norma a `1e-12`. **Il caso noto in piu' (mio):** con `m2` e `c0` di chi rimessi, il solutore deve ridare `Laplaciano.statico` di chi AL `1e-12` *(lo stesso stato)*.
- **K2** il punto fisso converge a `1e-10` in meno di `200` iterazioni a ogni tick; se no, dirlo e FERMO.
- **K3** la caduta VERSO / VIA per collegamento; «NATURA» se VERSO e il mattone al centro batte piu' piano del bordo *(il Pound-Rebka interno)*.
- **K4** Eotvos `eta` con `2 sigma`: `< 1%` = la porta G2; fra `1%` e `12%` = MIGLIORA; `>= 12%` = LASCIA / PEGGIORA.
- **K5** la coppia a `d 36`: `Delta a` in fase e in antifase; A e B contro F0 senza lapse e contro chi; **il riferimento a parita' di stato** *(l'errore n.235: F-off o lo stato compatto riscalati, non `coppia_GU_L162`)*.
- **K6** la tabella del giudizio contro chi.
- ### **ADATTATI DALLE DECISIONI** *(3-bis)*: «Z1 e Z2» diventa **le tre righe** *(V2, V3, V2+V3)* in K1 *(il mattone)*, K3, K4; **«`N(centro) < 1` con Z1» vale per V2+V3**; **K2 `< 20`**; **il confronto con chi a parita' di stato e' solo per V2+V3** *(il collegamento di `chi_tick`, la stessa partenza: il `k 0` di C2)*.
- **I CASI NOTI DEL CODICE** *(committati prima delle corse)*: **CN1** il solutore con `m2`, `c0` di chi e `N = 1` ridà `chi_tick.chi_statico` al `1e-12`; **CN2** il vincolo SPENTO ridà lo stato `k 250` della caduta V2 x0.8 di [M1446] AL BIT; **CN3** il vincolo spento ridà `D(k)` della coppia in fase di [M0326-K] AL BIT fino a `k 250`; **DEVE FALLIRE:** CN2 con la scala cambiata nell'ultimo bit.
- **LE CORSE IN PIU' CHE IL MANDATO NON NOMINA** *(le dico)*: **il riferimento V2+V3 SENZA vincolo a x0.8 e x1.2** *(Eotvos fu misurato solo per V2 e V3: senza, il cambio di `eta` per V2+V3 non ha base)*; **la coppia F0 in ANTIFASE a `d 36` senza vincolo** *(c'e' solo in fase)*. **Chi in antifase non esiste:** K5 contro chi solo in fase *(`gravita-F-on`, `d 39`, riscalato `1/d`)*. **Il Pound-Rebka interno si legge dalle corse del mattone fermo** *(non due corse a parte)*: `omega` per anello pesata con `rho` su finestre di `50` tick; **il centro `r < 5`, il bordo `5 <= r < 10`** *(il raggio del mattone `~9.7`: la scelta e' mia, fissata qui)*. **In tutto `22` corse.**

## 5. LE PREVISIONI *(copiate dal mandato, prima dei numeri; e le mie, separate)*

- **DEL GUARDIANO:** **P1** K1 e K2 passano `75%`; il profilo `N(r)` risolto piu' stretto di quello di chi `60%`. **P2** la caduta: V2 VIA `70%`; V3 VERSO `65%`, con l'orologio interno come natura solo con Z2 `55%`. **P3** Eotvos `< 1%` con almeno una combinazione `35%`; fra `1%` e `12%` `40%`; `>= 12%` `25%`. **P4** la coppia: A e B come F0 entro il `20%` `65%`. **P5** il giudizio: TOPPA o NULLA `55%`, CURA `30%`, DANNO `15%`.
- **DEL GUARDIANO, AGGIUNTA CON LE DECISIONI** *(Luca, 2026-11-23)*: **`eta` cambia meno del `20%` in relativo `60%`; sotto l'`1%` `10%`; sale `30%`.** *(La mia lettura, dichiarata: «sotto l'`1%`» e' il cambio relativo `|eta_vinc/eta_rif - 1| < 1%`; nel referto si dice anche se `eta < 1%`, la porta G2.)* **P2 «V3 VERSO con l'orologio interno come natura solo con Z2»** non e' piu' giudicabile come scritta *(Z2 non si fa)*: si giudica la parte senza Z2.
- **LE MIE SU `eta`** *(prima dei numeri)*: il cambio relativo `< 20%` per tutte e tre le righe `70%` *(il campo che il mattone si fa da se' cambia `cs` e la fase dentro di lui di `~kappa chi ~ 1e-2`: un effetto del secondo ordine su una differenza del `12%`)*; `eta` sale con V3 `55%` *(l'anti-lapse e' piu' profondo per il mattone piu' pesante)*.
- **LE MIE** *(dalla sez. 1, prima dei numeri)*: **il profilo risolto e' PIU' LARGO di quello di chi, non piu' stretto** `75%` *(togliere `m2` toglie la portata: la coda di `K0` diventa un logaritmo)*; **con V3 da solo `N(centro) > 1`** `90%` *(la sorgente `-e0 (rho - <rho>)` e' negativa nel cuore)*; **il rilassamento semplice NON passerebbe K2** `90%` *(D4)*.

## 6. LA STELLA POLARE *(le cinque risposte, prima del codice)*

1. **A14:** l'energia `E[N]` e' stazionaria in `N`: `N` non porta energia propria *(non ha `pi`)*; **la conservazione LOCALE non vale** *(`N` risponde istantaneamente a tutto il toro: un vincolo ellittico e' non locale nel tempo)*: **e' una violazione da dichiarare**, come nella relativita' generale per il lapse.
2. **Il gradino:** nessuno ancora *(la carta)*.
3. **Numeri e leggi:** **nessun numero nuovo** con D1(a) *(`c2`, `kappa` di chi)*; **una legge tolta** *(l'equazione del moto di chi)* **e una forma cambiata** *(chi statico, `m2 = 0`)*; **Z2 sarebbe una legge in piu'** *(D2)*: **Luca non l'adotta** *(3-bis)*.
4. **Il verso:** materia -> curvatura *(`u` fa `N`)* e curvatura -> materia *(`N` in `cs` o nella fase (a))*: **tutti e due, a ogni tick**; tocca `c_s` *(V2)*.
5. **Emergente o imposto:** `N` non si impone *(si risolve)*; ### **ma la caduta e Eotvos restano in un gradiente imposto** *(D3)*.

## 7. LA TABELLA DEL GIUDIZIO *(vuota: si riempie coi referti, contro chi e contro F0 senza lapse)*

| riga | F0 senza lapse | chi | il lapse risolto | giudizio |
|---|---|---|---|---|
| S1-S18 | | | | |
