# 2026-11-07 — IL REFERTO DELLA COPPIA `C35-0` (e poi `C35-pi`, `C50-0`): LA CARTA, PRIMA DEL CODICE *(`csv/solitone/carta_coppia.py`, nuova)*

> **Il mandato:** il piano delle corse della coppia *(`2026-11-06_coppia_corse`, sez. `2`, riga `4`)*: «**`C35-0`, `C35-pi`, `C50-0`, un referto ciascuna; i DEVE di `A`, `C`**», con le misure `A`..`G` di **`2026-11-05_coppia_forza_e_campi`**, sez. `3`, e la decisione di Luca delle `15:28` *(le soglie dei DEVE **come proposte**, `tau` `35`)* e delle `16:28` *(`E_int = E[p1 + p2] - E[p1] - E[p2] + E[0]`, il vuoto una volta)*. **Si scrive con `C35-pi` in corsa: solo scrittura, nessun calcolo.**

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

1. **La partenza della coppia** *(`corsa_accensione.py`, `COPPIA`)*: **`p0 + segno x roll(p0, d lungo l'indice 1)`**, con **`p0` la partenza FRESCA `BG`** *(non uno stato maturo)*; **`S162` e' `p0` da solo, nella posizione `1`**, col bordo di `C35` *(il centro nel punto medio, `R_A 47.5`)*. **Il secondo solitone e' `p0` traslato di `35` nodi lungo `A1`, intero: nessuna interpolazione.**
2. **I dati:**
   - **le mappe** su `E:` *(`rho`, `Lambda` float32 ogni `100` tick, `667` istantanee; il `centro` della DENSITA' TOTALE, in `(x, y)`)*;
   - **i campioni** nei jsonl *(`6667`, ogni `10` tick, **agli stessi `t` di `S162`**: verificato; `E` per `totale`, `vicino`, `lontano`; il `bordo` con `E_ass`, `M_ass`)*;
   - **gli stati completi** *(`7`, ogni `1500` unita' di tempo: `psi`, `psi_h`, `phi_h`, `Lambda`)*.
   - **`S162` ha gli stessi tre**, agli stessi tempi.
3. ### ⚠ **LA SIMMETRIA DI SCAMBIO NON E' ESATTA A `t 0`:** lo scambio dei due *(la rotazione di `180` gradi attorno al punto medio)* **porta `p0` in `R180 p0`, non in `p0` traslato**; e **`p0` non e' simmetrico per `R180`** *(per `rho(t 0)` di una partenza `BG`, `3.67e-2`, `impulso_partenza.txt`: **da rimisurare su questa**)*. **Quindi `A-S` non parte da zero:** ### **il suo riferimento e' l'asimmetria a `t 0`**, e la crescita si misura **rispetto a quella**.
4. **La traslazione invece e' esatta:** **la seconda copia e' `roll(p0, 35)`**, e il tick sul toro **commuta con una traslazione di reticolo** *(il vuoto `F3` e' uniforme sugli archi: **da verificare**, `C-T` qui sotto)* -- **tranne il bordo**, che e' centrato nel punto medio. ### **Quindi il riferimento singolo del solitone `2` e' `S162` traslato di `35`, ma col bordo nel posto sbagliato** *(a `d` dal suo)*: **lontano dalla fascia conta poco, e lo dico; vicino alla fascia no.**
5. **`E_int`** *(Luca `16:28`)*: **`E[p1 + p2] = E` di `C35`, `E[p1] = E[p2] = E` di `S162`** *(l'energia e' invariante per traslazione sul toro: la stessa del punto `4`)*, **`E[0]` il vuoto `c(t) F3` su `L 162`** *(da calcolare, come `E8_0` in `coppia_matura`)*. ### **Il bordo toglie energia, e piu' alla coppia** *(alla fine `E_ass` `2.656e+04` contro `5.841e+03` di `S162`)*: **la forma conservata e' `E + E_ass`**, e la stampo **accanto** a quella senza.
6. **Le misure del log della corsa** *(`f_liscia`, `w`, l'alone)* **sono attorno al centro della densita' TOTALE**: **non servono qui** *(sez. `12` del task history della coppia)*.
7. **Cosa NON so:** se **l'adattamento a due gobbe** converge con `rho` sovrapposte nelle corone; **quanto rumore ha `d''(t)`** su istantanee ogni `15` unita' di tempo; **se `D(t)` del vuoto si distingue dal bordo mal posto** del solitone `2`.

## 2. PROGETTAZIONE DEL RAGIONAMENTO *(le letture si fissano QUI, prima dei numeri)*

### I passi e cosa decide ciascuno
1. **`A0`, `A0-F`** *(decise come proposte)*: **su una coppia SINTETICA** *(`rho` di `S162` + la stessa traslata di `35`, a ogni istantanea)* **i due metodi** *(il centro periodico di ciascun semipiano; l'adattamento a due gobbe)* **ridanno `d = 35` entro `0.05` nodi**; **`A0-F`:** l'asse di separazione spostato di `5` nodi, `d` **NON** entro `0.05`. **Il semipiano** *(dichiarato)*: **un nodo e' del solitone `1` se il suo scarto lungo `A1` dal punto medio, riportato in `[-L/2, L/2)`, e' negativo**; **sul toro la seconda linea di separazione e' a `L/2` dal punto medio**, e il semipiano e' la meta' del toro fra le due.
2. **`d(t)`, la velocita', l'accelerazione; `F = mu d''`, `mu = M / 2`; il baricentro; l'angolo dell'asse.** **Contro il riferimento:** ### **la deriva del centro di `S162`** *(la stessa misura sul singolo: `d_S(t) = 2 |X_S(t) - X_S(0)|` lungo `A1`)*, **che e' cio' che il singolo fa da solo.**
3. **`A-S`** *(`tau 35`, Luca)*: **l'asimmetria di scambio** `|rho - R180 rho| / |rho|` attorno al punto medio, **dal suo valore a `t 0`** *(premessa `3`)*: **cresce non piu' di un e-fold ogni `35`.**
4. **`E_int(t)`** *(premessa `5`)*, per termini *(`cin`, `vuo`, `leg`, `cost`)*, **ai `6667` campioni**; **`E[0]` una volta** *(il vuoto a `|c|` costante: **se l'energia del vuoto dipende da `t`, la calcolo agli stati e lo dico**)*.
5. **`C0`, `C0-F`, `C-T`** *(decise come proposte)*: **`D(t) = dLambda_C35 - (dLambda_S162 + roll(dLambda_S162, 35))`**, la norma relativa a `|dLambda_C35|`; **sulla coppia sintetica `D = 0` alla macchina** *(`C0`)*; **con lo spostamento sbagliato di `1` nodo `D` sotto `1e-3`** *(`C0-F`, deve fallire)*. ### **`C-T` (nuovo, mio):** **il tick commuta con la traslazione di `35`** *(un tick dallo stato di `S162` a `t 0` traslato = il traslato del tick, al bit **senza** il bordo)*: **senza questo, `S162` traslato non e' il riferimento del solitone `2`.**
6. **I profili** di `Lambda` lungo l'asse fra i due e di traverso al punto medio; **la materia fra i due** *(`rho_C35 - rho_S162 - roll(rho_S162)` nella lente)*; **lo scambio** *(la massa di ciascun semipiano nel tempo)*.
7. **`D` in parte:** **`w` e il cuore di ciascuno sul suo semipiano** contro `S162`; **la fase relativa** *(agli `7` stati: l'argomento della proiezione di ciascuno sullo spinore di `p0`, sul cuore)*.
- **`E` *(la legge di forza)* e `F` *(il segno con la fase)* NON sono di questo referto:** vogliono `C50-0` e `C35-pi`. **`G`:** una corsa per caso, **indicativa**.

### Le letture *(di Luca, `2026-11-05`, sez. `4`; per `C35-0` da sola si legge solo cio' che `C35-0` puo' dire)*
- **(p1)** **nessuna forza oltre l'oscillazione del singolo a `35`** -> *(con `C50-0`)* **il vuoto non porta niente a questa distanza.**
- **una forza a `35`** -> **la prima meta' di (p1)**; **il segno con `C35-pi`** (p3); **se anche a `50`, (p2).**
- **(p4)** **`D(t)` non zero e il campo fra i due che si stringe** -> **un ponte.**
- **(p5)** altro, da descrivere.

### Cosa mi farebbe FERMARE
- **`A0` o `C0` che falliscono**, o i loro rovesci che passano;
- **`C-T` che fallisce** *(il riferimento del solitone `2` cade, e con lui `D(t)`)*;
- **l'adattamento a due gobbe che non converge** su piu' del `10%` delle istantanee *(lo dico, non lo nascondo)*.

## 3. TODO DEL NEXT STEP
1. Questo task history, un commit *(con `C35-pi` in corsa: sola scrittura)*.
2. **Il codice** `csv/solitone/carta_coppia.py` *(nuovo: `--corsa C35-0`; legge le mappe, i jsonl, gli stati di `C35-0` e di `S162`; `_presidio.avvia`)* e la voce nell'INVENTARIO, un commit -- **ancora durante `C35-pi`** *(un file che la corsa non importa)*.
3. **A `C35-pi` finita:** `D6` ripuntato, la cassetta; **`carta_coppia.py --corsa C35-0`**, il referto `doc/referti_l2/coppia_C35-0.txt`, la relazione, questo task history; **poi `--corsa C35-pi`**; **poi `C50-0`**.
4. ### **Le domande a Luca** *(il criterio di chiusura: le sue risposte, scritte qui; **il codice si scrive comunque, perche' nessuna risposta cambia cio' che si MISURA, solo come si LEGGE**)*:
   - **(q1)** **«una forza»:** quanto deve uscire `d(t) - 35` dalla deriva di `S162` per leggersi come forza? ### **Propongo:** **lo scarto medio sull'ultimo terzo, oltre `3` volte la deviazione standard di `d_S(t)` sullo stesso tratto** *(un numero mio: decide Luca)*.
   - **(q2)** **`A-S` dal valore a `t 0`** *(premessa `3`)*: **va bene, o si vuole la partenza simmetrizzata** *(come `TBS`: un'altra corsa)*?
   - **(q3)** **il riferimento del solitone `2`:** **`S162` traslato** *(il bordo nel posto sbagliato, premessa `4`)*, **oppure `S162` ruotato di `180` attorno al punto medio** *(il bordo giusto, ma la partenza `R180 p0` non e' `p0`: lo stesso difetto della premessa `3`)*? ### **Propongo il traslato**, con `C-T` che lo sigilla, **e dico dove il bordo pesa** *(la distanza dalla fascia)*.

## 4. IL CODICE *(`csv/solitone/carta_coppia.py`, `sha1-BYTE 8a922011`; committato prima di girarlo, con `C35-pi` in corsa: un file che la corsa NON importa)*

- **Le scelte dichiarate nel codice:**
  - **la finestra di `A-S`:** `FIN_AS = 3 TAU` *(MIA)*;
  - **`C-T` ed `E-0` entro `n eps`** *(`n` i nodi: il limite dell'errore di una somma riordinata di `n` termini, derivato)*;
  - **`FA0` entro le code incrociate** *(`|<ref|roll ref>| / |ref|^2` su ciascun semipiano, misurate)*;
  - **`A-S-I`** *(`R180` due volte = l'identita', entro `1e-10` del massimo)*: un numero mio, solo un controllo della mia rotazione.
- **Il metodo:**
  - lo spostamento frazionario e la rotazione `R180` attorno al punto medio **per trasformata sul toro per indice**;
  - **l'adattamento a due gobbe** con `scipy.optimize.least_squares` *(`lm`)*, il singolo **allo stesso `t`**.
- **`E-0`, il controllo positivo mio:** il libro ricalcolato sullo stato della coppia a `t 0` deve ridare `E` del campione. **Senza, `E[0]` calcolato nello stesso modo non avrebbe un aggancio.**
- ### ⚠ **Una premessa nuova, per `C50-0`:** **non c'e' un singolo col bordo di `C50`** *(`R_A 55`; `S162` ha quello di `C35`)*: **la carta rifiuta `--corsa C50-0`.** **Il referto di `C50-0` vuole una decisione di Luca** *(un `S162` col bordo di `C50`, cioe' un'altra corsa, oppure `S162` col bordo sbagliato, dichiarato)*.
- **Avanti:** **a `C35-pi` finita**, `D6` ripuntato e la cassetta, poi la carta su `C35-0`.

## 5. IL MANDATO DI LUCA DEL `2026-11-07` `10:20`: **IL REFERTO DI `C35-0` SUBITO** *(un'ECCEZIONE DICHIARATA da Luca alla regola «un calcolo alla volta»: una carta di lettura sui dati gia' salvati, pochi minuti, mentre `C35-pi` gira)*; **`C35-pi` a corsa finita, come previsto.** **In piu': I DUE CENTRI DEL VUOTO DISTURBATO**

- **Il mandato:** **i centri delle zone con `dLambda > 0` dentro l'ovale, per semipiano, accanto ai centri della materia, nel tempo.** ### **La lettura del guardiano, dalle mappe** *(di Luca, scritta qui PRIMA dei numeri)*: **i due «nuclei» del vuoto restano quasi fermi** *(da `+-17.5` a circa `+-15`)*, **la materia oscilla fra loro e il centro.**
- ### **Le premesse dal codice:**
  1. **«L'ovale» lo leggo come la zona SENZA assorbimento:** **`r < R_A`** dal centro del bordo, **con la stessa distanza del bordo** *(`campo.anelli`, esatta in indici, come `bordo.g_estremita`)*; **sulla mappa per indice un disco del reticolo triangolare appare un ovale.** ### **Un'interpretazione MIA, dichiarata.** **Il centro del bordo `c0` e' il punto medio della coppia** *(`F-B` `0`)*.
  2. **`dLambda` e' quello che la carta gia' usa:** **`Lambda(t) - Lambda(t 0)` della stessa corsa** *(le mappe float16)*.
  3. **Il centro di una zona:** **la media di `X`** *(lo scarto cartesiano dal punto medio, `toro.scarti`)* **pesata con `max(dLambda, 0)`**, sui nodi dell'ovale nel semipiano *(`x < 0` per il solitone `1`, `x >= 0` per il `2`: la stessa maschera di `centri_semipiani`)*. **Dentro l'ovale `|X| < 47.5 < L/2`, quindi la media non piega sul toro.**
  4. **I centri della materia:** **quelli dei semipiani gia' calcolati per `d(t)`** *(`cA`, `cB`)*, **portati in `X` dal punto medio.**
  5. ### **In piu', MIO, dichiarato:** **anche i centri delle zone con `dLambda < 0`** *(il vuoto svuotato, il cuore)*: **`dLambda > 0` e' l'anello gonfio attorno, e le due zone possono muoversi in modo diverso.** **E la stessa colonna per `S162`** *(il semipiano `x < 0`, dove sta il singolo)*: **cio' che il singolo fa da solo.**
- ### **I DEVE** *(il metodo, su mappe sintetiche)*:
  - **`A-V`** *(DEVE PASSARE)*: **una mappa sintetica con due punte di valore `1` ai nodi piu' vicini a `(-15, 0)` e `(+15, 0)`**: **i due centri del vuoto = le `X` di quei nodi, entro `1e-12`.**
  - **`A-V-F`** *(DEVE FALLIRE)*: **la stessa con una terza punta FUORI dall'ovale** *(il nodo piu' vicino a `(-60, 0)`, `r > R_A`)*, ### **il centro calcolato SENZA la maschera dell'ovale = la punta dentro, entro `1e-12`**: **deve fallire, perche' senza la maschera la punta fuori lo sposta.** **E' il controllo che la maschera fa qualcosa.**
- ### **Le letture** *(fissate qui, PRIMA dei numeri)*:
  - **(v1)** **i nuclei del vuoto quasi fermi** *(il loro `x` cambia meno di quello della materia)*, **la materia fra loro e il centro**: **la lettura del guardiano confermata;**
  - **(v2)** **i nuclei si muovono quanto la materia** *(seguono il solitone)*;
  - **(v3)** **altro** *(i due segni di `dLambda` raccontano storie diverse, o un nucleo sparisce)*.
  **Il criterio:** **nessuna soglia mia;** **si stampano le escursioni** *(il minimo e il massimo dell'`x` per blocco)*, **e la lettura si dichiara.**
- ### **D6 e la cassetta:** **l'eccezione di Luca copre UNA carta di lettura;** **la cassetta e' un calcolo in piu', quindi la giro a `C35-pi` finita** *(prima del referto di `C35-pi`)*, **dichiarato.** **Il timbro di `_presidio` controlla comunque che il blob della carta sia quello committato.**
- **I passi:** questa sezione, un commit; **il codice** *(i centri del vuoto, `A-V`, `A-V-F`, l'INVENTARIO)*, un commit; **la carta su `C35-0`**; **il referto** `doc/referti_l2/coppia_C35-0.txt`, la relazione, questa sezione con l'esito.

## 6. LA CARTA SU `C35-0` *(`carta_coppia.py` `3c250c46`, `doc/referti_l2/coppia_C35-0.txt`; `24` minuti, exit `1`)*: **UN DEVE FALLISCE, LA CARTA SI FERMA A META', E TRE ERRORI MIEI** -- **FERMO**

- **Passano:** `R0`, `A0`, `A0-F`, `A-V`, `A-V-F`, `A-S`, `C0`, `C0-F`, `C-T`, `C-T-F`, `E-0`. **Fallisce `A-S-I`.** **Poi la carta si FERMA nella fase relativa** *(una divisione per zero)*: **`FA0` non e' girato.**
- ### ⛔ **ERRORE MIO (1), LE UNITA' DEL TEMPO: le mappe portano `t` in TICK, non in unita' di tempo** *(verificato sul file: `0, 100, 200 .. 10000` nel primo pezzo di `S162`)*. **La carta usa `tm` come se fosse il tempo**, quindi:
  - **le tabelle «a blocchi di `500`» sono a blocchi di `500` TICK** *(`75` unita')*, e la colonna «il tempo» va da `0` a `66600` tick *(`t 9990`)*;
  - ### **`A-S` e' SBAGLIATO, non solo mal etichettato:** **la finestra `FIN_AS = 105` e' di `105` tick** *(`15.75` unita', non `3 TAU`)*, **e la pendenza e' PER TICK contro `1 / TAU` per unita' di tempo**: **il massimo `2.334e-02` per tick sarebbe `0.156` per unita' di tempo, sopra `1 / TAU = 2.857e-02`** -- ### **in unita' giuste `A-S` potrebbe FALLIRE** *(su una finestra diversa: va rifatto, non riconvertito)*;
  - **«dopo la rampa (`t >= 1000`)»** e' `>= 1000` tick *(la rampa finisce a `6667`)*; **`d''` e `F` sono per tick al quadrato**; **i tempi dei profili** *(`0, 3330, 6660, 9990`)* **sono tick.**
  - **Corretti:** **`E_int`** *(usa `tC * s`)* e **`C-T`** *(lo stato a `10000` TICK, come scritto)*.
- ### ⛔ **ERRORE MIO (2), LA FASE RELATIVA:** **la chiave `psi` degli stati e' NULLA** *(`|psi| = 0` sullo stato di `S162` a `t 0`, `|psi_h| = 1000`)*: **lo stato vero e' `psi_h`, per estremita'**. **La carta ha diviso per `<ref|psi>_A = 0`.**
- ### **IL DEVE CHE FALLISCE: `A-S-I`** *(`R180` due volte = l'identita', entro `1e-10`, MIO)*: **`1.237e-06`.** **L'ipotesi** *(da verificare, non verificata)*: **lo spostamento frazionario per trasformata di un campo reale su `L = 162` pari lascia una parte immaginaria alla frequenza di Nyquist, che `.real` butta**: **la rotazione non e' esattamente invertibile.** **L'asimmetria misurata a `t 0` e' `2.398e-04`, `200` volte sopra `1.237e-06`**: **il numero non sarebbe dominato da questo, ma la soglia era mia e il controllo e' fallito.**
- ### **Cio' che resta leggibile, con l'asse del tempo in tick** *(da riscrivere nelle unita' giuste dopo la cura, quindi NON una lettura chiusa)*:
  - **la materia:** **`d` dai semipiani da `35.0` a `6.83` nel blocco di tick `12500 .. 13000`** *(`t ~1900`)*, **poi un'oscillazione fra `~10` e `~33`** fino alla fine; **le due gobbe seguono la stessa forma dove convergono** *(`1` non convergente su `667`)*;
  - ### **i nuclei del vuoto (`v+`):** **da `+-17.5` a `~16.5`-`17.4`, con un'escursione per blocco di qualche decimo**, ### **mentre la materia va da `+-17.5` fino a `+-3.5` e torna**: **dopo il tick `1000` l'escursione di `x` della materia `14.48` / `14.16`, dei nuclei `v+` `4.35` / `3.74`, di `v-` `2.10` / `2.54`.** ### **E' la lettura `v1` del guardiano** *(i nuclei quasi fermi, la materia fra loro e il centro)*, **con la riserva delle unita'.**
  - **`E_int`** *(in unita' giuste)*: **a `t 0` `+4.02e-04`** *(`8.6e-11` di `E[S]`)*; **poi scende fino a `-1.47e+04` nel blocco `9500 .. 10000`** *(per termini: `cin` `-6.0e+04`, `vuo` `+3.2e+04`, `leg` `-4.3e+03`, `cost` `+1.8e+04`)*; **con `E_ass` resta fra `-38` e `+31`.**
- ### **LA CURA PROPOSTA** *(un commit a se'; le DUE prime sono errori di codice, la terza e' una soglia cambiata dopo il numero, quindi decide Luca)*:
  1. **le unita':** **`tm` in unita' di tempo** *(`t * s`)* **ovunque**, coi tempi dei profili, `FIN_AS`, il blocco, la rampa e `d''` per unita' al quadrato;
  2. **la fase relativa da `psi_h`** *(la maschera del semipiano per estremita': `np.repeat` della maschera per nodo sulle `6` estremita')*;
  3. **`A-S-I`:** **la verifica dell'ipotesi di Nyquist** *(il residuo con la componente di Nyquist tolta)*; **se e' quella, la rotazione si fa in modo esatto** *(tolto il modo di Nyquist prima, dichiarato)*, **oppure la soglia diventa derivata** *(il peso del modo di Nyquist nel campo)*: ### **la scelta e' di Luca.**
- **Criterio di chiusura:** **la decisione di Luca sul punto `3`; poi la cura, un commit, e la carta rifatta su `C35-0`.**

## 7. LA CURA DEGLI ERRORI (1) E (2) *(`carta_coppia.py` `54459239`, committata, NON girata)*: **IL TEMPO IN UNITA' DI TEMPO, LA FASE DA `psi_h`**

- **(1)** **`tm, tmS = tm * s, tmS * s`** subito dopo il controllo che le mappe siano agli stessi `t`: **i blocchi, la rampa, `FIN_AS`, `TAU`, `d''` e i profili ora in unita' di tempo.**
- **(2)** **`psi_h` invece di `psi`** per lo stato di riferimento e per gli stati della coppia; **le maschere dei semipiani per ESTREMITA'** *(il semipiano del nodo dell'estremita', `inc.nodo`)*; **la traslazione e' `rolla`, la stessa della partenza della coppia** *(`roll` di `(L, L, -1, ...)`)*.
- ### **NESSUNA SOGLIA CAMBIATA.** **`A-S-I` resta con `1e-10`: decide Luca** *(la sez. `6`, punto `3`)*. **La carta si rigira su `C35-0` e poi su `C35-pi` DOPO la sua decisione.**

## 8. LA DECISIONE DI LUCA DEL `2026-11-07` `16:25` SU `A-S-I`: **LA VIA (a)** *(ribadisce le `11:52`)*

- **(1) si VERIFICA l'ipotesi di Nyquist:** **il residuo di `A-S-I` col modo di Nyquist tolto.** ### **La lettura, scritta prima** *(Luca)*: **se e' Nyquist, il residuo cade sotto `1e-10`.** **(2) se confermata: la rotazione si fa ESATTA, togliendo il modo di Nyquist prima di ruotare, dichiarato; e si scrive quanto pesa quel modo nel campo, accanto all'asimmetria a `t 0` (`2.398e-04`).** **(3) se NON confermata: FERMO; la soglia `1e-10` NON si cambia.**
- ### **Il perche', dal codice** *(la mia ipotesi della sez. `6`)*: **`r180` e' un'inversione esatta degli indici** *(`g[::-1, ::-1]` e un `roll`)* **seguita da uno spostamento FRAZIONARIO di `2 c` per trasformata**; **su `L = 162` pari, i modi a `k = L/2` sono REALI per un campo reale**, **e lo spostamento frazionario li rende complessi**: **`.real` butta la loro parte immaginaria** *(lo spostamento non e' piu' invertibile)*; ### **senza quei modi lo spettro resta coniugato-simmetrico e lo spostamento conserva la realta': `R180` due volte e' l'identita' all'arrotondamento** *(l'interpolazione a banda limitata esatta)*.
- **Il codice** *(`carta_coppia.py`)*: **`senza_nyquist(g)`** *(la riga e la colonna `L/2` della trasformata a zero)*; **`A-S-I` sul campo senza Nyquist** *(DEVE PASSARE, entro `1e-10`)*; **`A-S-I-F` sul campo intero** *(DEVE FALLIRE: torna a `~1.2e-06`)*; **il peso `|g - g_N| / |g|`** *(stampato accanto all'asimmetria)*; ### **l'asimmetria di scambio misurata sul campo senza Nyquist** *(dichiarato)*.
- **Poi, in sequenza:** **l'indice delle mappe di `C35-pi`; la carta su `C35-0`** *(il referto ufficiale, sostituisce il parziale)*; **la carta su `C35-pi`; il confronto; le mappe leggere di `C35-pi` per il video** *(`carta_campo --corsa C35-pi`)*. ### ⚠ **`D6` e la cassetta NON girate prima** *(il mandato: «subito, in sequenza»)*: **`carta_coppia` non e' nella cassetta; lo dichiaro.**

## 9. I REFERTI UFFICIALI DI `C35-0` E `C35-pi` *(`carta_coppia.py` `255e2d02`; `doc/referti_l2/coppia_C35-0.txt`, `coppia_C35-pi.txt`; exit `1` tutti e due)*: **`13/14`; `A-S-I` CONFERMA NYQUIST; FALLISCE `A-S`** -- **FERMO su `A-S`**

- ### **NYQUIST CONFERMATO** *(la lettura scritta prima)*: **`A-S-I` sul campo senza Nyquist `8.982e-16` (`C35-0`) e `1.078e-15` (`C35-pi`)**, **`A-S-I-F` sul campo intero `1.237e-06`** *(fallisce come deve)*. **Il peso del modo nel campo: a `t 0` `4.856e-06`, il massimo `3.316e-03` (`C35-0`) e `2.928e-03` (`C35-pi`)**, **accanto all'asimmetria a `t 0` `2.397e-04`.**
- ### **FALLISCE `A-S`** *(la pendenza di `log` dell'asimmetria di scambio su finestre di `105` unita' sotto `1/TAU = 2.857e-02`, `TAU = 35` Luca `2026-11-05`)*: **il massimo `2.975e-02` (`C35-0`) e `2.965e-02` (`C35-pi`), tutti e due alla PRIMA finestra** *(`t 0 .. 105`)*: ### **`4%` sopra la soglia**; **un e-fold ogni `~33.6` unita' di tempo all'inizio** *(dall'asimmetria iniziale `2.4e-04`)*: **la stessa scala del caos gia' misurato** *(`D5`: `TBS` `~40`; `D0R` `~25`)*. **Non lo leggo: e' un DEVE fallito, la soglia e' di Luca.** **Il resto della corsa: l'asimmetria finisce a `1.03e-01` (`C35-0`, il massimo `4.16e-01`) e `1.04e-01` (`C35-pi`, il massimo `1.40e-01`).**
- **Passano:** `R0`, `A0`, `A0-F`, `A-V`, `A-V-F`, `C0`, `C0-F`, `C-T` *(`1.346e-16`)*, `C-T-F`, `E-0` *(`0`)*, ### **`FA0`** *(la fase relativa a `t 0` = `0` e `pi`, `0.000e+00`)*.
- ### **IL CONFRONTO, coi numeri delle carte** *(in unita' di tempo; da leggere con la riserva di `A-S`)*:

| | `C35-0` *(in fase)* | `C35-pi` *(in opposizione)* |
|---|---|---|
| **`d` dai semipiani** | **da `35.0` a `~13` a `t 1500 .. 2000`, poi oscilla fra `~12` e `~32`** *(un ritmo di `~2000`-`2500`)* | ### **da `35.0` CRESCE piano: `36.0` a `2000`, `37.0` a `5000`, `36.9`-`37.4` alla fine** |
| **l'ultimo terzo, `d - 35`** *(q1, nessun verdetto)* | **`-11.6`** *(semipiani)*, **`-12.1`** *(due gobbe)* | **`+2.17`**, **`+2.18`** |
| **3 volte la deviazione di `2 dx` del singolo** | `0.698` | `0.698` |
| **i nuclei del vuoto `v+`** *(l'escursione di `x` dopo la rampa)* | **`4.35` / `3.74`**, alla fine `~-16.4` / `+17.3` | **`1.40` / `1.14`**, alla fine `~-18.0` / `+17.8` |
| **la materia** *(l'escursione)* | **`14.18` / `14.16`** | **`1.48` / `1.25`** |
| **`E_int` per termini** *(l'ultimo blocco, `9500 .. 10000`)* | **`tot -1.472e+04`**, con `E_ass` `-37.8` | **`tot -2.308e+03`**, con `E_ass` `+3.30` |
| **la fase relativa** *(agli stati)* | da `0` a `-0.20`, `+0.09` | **resta vicina a `pi`** *(`3.082`, `3.119`)* |
| **`(M1 - M2) / M`** *(l'ultimo blocco)* | `+7.7e-03` | **`+5.2e-02`** *(cresce: `1e-05` -> `5e-02`)* |
| **l'assorbito al bordo** *(dalle corse)* | **`M 1.002e-02`, `V 1.016e-01`, `E 2.705e-03`** | **`M 4.645e-03`, `V 4.198e-02`, `E 1.429e-03`** |

- ### **La forma dell'involucro** *(ovale o no)*: **NON e' misurata da questa carta** *(nessuna misura della forma: da aggiungere, `carta_forma` sul singolo)*. **Lo dico invece di stimarla.**
- ### **LA LETTURA, NON MIA MA DA SCRIVERE COME FATTO MISURATO** *(con la riserva di `A-S`)*: **in fase i due si avvicinano fino a `~13` e oscillano; in opposizione si allontanano di `~2` nodi in `10000` unita', la fase relativa resta `pi`, e la massa si sbilancia fra i due** *(`5%`)*. **Le letture di Luca sono sue.**
- **Le mappe di `C35-pi` per il video NON sono fatte:** **`carta_campo --corsa C35-pi` alza `KeyError: 'C35-pi'`** *(le tabelle `PARTI` e `INDICI` della carta conoscono solo `C35-0`)*: **un errore mio, la cura e' un commit a se'** *(`doc/referti_l2/campo_C35-pi.txt` col traceback)*. **L'indice delle mappe di `C35-pi` e' fatto** *(`mappe_indice_C35-pi.txt`)*.

## 10. LA DECISIONE DI LUCA DEL `2026-11-07` `17:55` SU `A-S` *(il FERMO della sez. `9` CHIUSO)*

- ### **(3) `A-S` PASSA se la crescita del `log` dell'asimmetria non supera la crescita piu' rapida del caos gia' misurata, `1/25` per unita' di tempo** *(`D0R`)*, **invece di `1/TAU = 1/35`.** **DICHIARATO: la soglia fissata DOPO i numeri, ancorata al caos misurato PRIMA** *(`D0R`, `D5`)*. **La finestra resta `FIN_AS = 105`.** **Nel referto:** **«la simmetria della coppia si rompe alla velocita' del caos, a partire dall'asimmetria iniziale (`2.4e-04`), e non piu' in fretta».**
- **Il codice:** **`TAU_CAOS = 25`** *(il limite di `A-S`; `TAU` resta per la finestra)*; **le due carte rigirate** *(i referti ufficiali)*.
- **K3, la cura di `carta_campo`:** **`C35-pi` in `PARTI` e `INDICI`**; **il controllo: la carta rigirata su `C35-0` ridà AL BIT i file di prima** *(lo `sha1` di `mappe_leggere.npz` e `profili.npz` di `6ddd1bd3`)*; **poi `C35-pi`.**
