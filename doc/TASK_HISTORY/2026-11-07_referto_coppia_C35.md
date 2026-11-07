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
