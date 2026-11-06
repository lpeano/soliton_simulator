# 2026-11-07 — LA LIBRERIA DEI SOLITONI MATURI E I CLUSTER *(Luca `2026-11-07` `00:32`)*

**Il mandato** *(nella sostanza)*: **oggetti riutilizzabili** -- solitoni maturi da non ricalcolare, **da incollare in un vuoto nuovo per fare cluster** e vedere come si comporta l'aggregato. **Le quattro attenzioni** *(la fase del vuoto, il ritaglio, le copie troppo identiche, la fase relativa fra vicini)*; **`LIB0`** *(il ritaglio)*, **`LIB1`** *(la riutilizzabilita', coi DEVE)*, **`LIB2`** *(il transitorio)*; **la proposta dei cluster** *(il triangolo, la fila di tre, l'esagono piu' il centrale)*; **FERMO su `R_t` e sui cluster.** **Un calcolo alla volta, il nucleo non si tocca, nessun peso si regola; la libreria fra una corsa e l'altra, i cluster DOPO la coppia.**

**In coda:** arriva con **`C35-0` in corsa** *(lanciata alle `~00:10`)* e **il FERMO sulle carte IS2 e IS3** *(`b9b9ce7f`)*. **Ora: questo task history, la MAPPA, la relazione; il codice dopo, committato prima di girarlo; `D6`, la cassetta e `LIB0`-`LIB2` FRA `C35-0` e `C35-pi`** *(insieme alle mappe leggere)*.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

1. **Gli stati completi di `TBS`:** **`21` su `E:\soliton_simulator\stati\TBS\`**, ai tick `0, 10000, ..., 200000` *(ogni `1500` unita' di tempo, `s 0.15`)*, **col loro `sha` per chiave nel jsonl** *(letti)*. **`L 81`; il bordo di `TBS`: centro `(40.5, 40.5)`, `R_A 28`** *(il jsonl)*. **Le corse della coppia ne salvano `7` ciascuna** *(`0 .. 9000`, `L 162`)*.
2. **La tecnica di `carta_statiche.coppia_matura` NON ritaglia:** **incolla il toro INTERO di `L 81`** *(`psi` e `phi`)* **nel rombo `[:81, :81]` di `L 162`**, e **il vuoto e' `phi0 + D1 + D2`** con `D = phi - c(t) F3`. **Il ritaglio a `R_t` e' quindi NUOVO.** **E la fase `pi` cambia segno SOLO a `psi2`** *(il disturbo del vuoto `D2` resta col suo segno: dal commento della carta)*.
3. ### ⚠ **LA GRIGLIA PROPOSTA DA LUCA (`28, 32, 36, 40`) STA TUTTA NELLA FASCIA DI `TBS`:** il bordo di `TBS` comincia a **`R_A = 28`** e satura a **`R_B = 40.5`** *(la meta' del periodo di `L 81`)*. **Oltre `28` lo stato e' gia' smorzato dal bordo a ogni tick** *(`psi -> psi (1 - g)`, `phi -> phi0 + (phi - phi0)(1 - g)`)*. **Quindi un ritaglio a `28 .. 40` taglia quasi niente: il bordo ha gia' tagliato.** **Propongo di estendere la griglia verso l'interno: `16, 20, 24, 28, 32, 36, 40`** *(dove il taglio morde)*. **Decide Luca.**
4. **Il bordo NON sta nel nucleo:** e' **`BO.assorbi(st, g_e, c(t) F3)` dopo ogni `AC.tick(z, t, K)`**, nel ciclo di `corsa_accensione.py`, con `g_e` intorno al **centro iniziale** *(`BO.g_estremita`)*. **Quindi `LIB1` puo' rifare lo STESSO ciclo fuori dalla corsa**, con le stesse funzioni *(nessuna copia della fisica)*.
5. **`c(t)`:** `BO.c_di(t, tab_c, K, omega)` dalla tabella di `fase_F3.npz` *(`omega = 3 pi / 20` per tick dopo la rampa)*. **Lo stato salvato al tick `t` vive nel vuoto `c(t) F3`.**
6. **La circolazione `Gamma(12)`** *(la misura B)*: **`carta_statiche._circola`** *(usata da `_serie_verso` su tutti gli stati di `TBS`)*. **L'energia: `carta_statiche.energia(z, psi, phi, e_K)`.** **`w`, il cuore** *(`f_liscia`)*, **il centro: dai campioni del jsonl allo stesso tick** *(e ricalcolati dallo stato, come controllo)*.
7. ### ⚠ **LE ATTENZIONI (1) E (3) SI SCONTRANO, e va detto prima:** **stati di TEMPI DIVERSI** *(l'attenzione 3)* **vivono in vuoti a FASI DIVERSE** *(`c(t_i) F3`: `omega` per tick, quindi fra `t 15000` e `16500` la fase differisce di `omega x 10000` mod `2 pi`)*. **In un cluster il vuoto e' UNO.** **Le due vie:** **(i)** ruotare ogni oggetto *(psi e il disturbo `D`)* di `c(T) / c(t_i)` **prima** di incollarlo -- **vale solo se il tick e' covariante per una fase globale comune di `psi` e `phi`** *(che e' da VERIFICARE, non da credere: un DEVE `LIB1-U`)*; **(ii)** scegliere stati di tick con la stessa fase di `c(t)` *(i tick `t_i` con `omega t_i` uguali mod `2 pi`: `omega = 3 pi / 20` ha periodo `40/3` tick, non intero, quindi la stessa fase torna ogni `40` tick: `t_i - t_j` multiplo di `40`)* -- **gli stati salvati sono a multipli di `10000`: `10000 = 250 x 40`, quindi TUTTI gli stati di `TBS` dopo la rampa hanno la STESSA fase `c(t)`** *(da verificare dal numero: `c_di` ai loro tick)*. ### **Se e' cosi', le attenzioni (1) e (3) NON si scontrano per gli stati di `TBS`**, e la via (i) serve solo per stati di altri tick.
8. **La fase relativa `0` / `pi`** *(l'attenzione 4)*: **come in `coppia_matura` e nelle corse della coppia, un segno sulla `psi` della copia** *(il disturbo del vuoto resta)*. **Con stati di tempi diversi «fase 0» non vuol dire «stessa fase interna»**: vuol dire **«nessun segno aggiunto»**. **Lo dico, perche' la statica della coppia matura era fatta con DUE COPIE DELLO STESSO STATO.**
9. **Cosa NON so:** **(a)** se il tick e' covariante per una fase globale comune *(la via (i))*; **(b)** quanto vale il salto al bordo del ritaglio dentro la fascia *(la premessa 3: credo piccolo oltre `28`)*; **(c)** se `TBS` rigirato da uno stato salvato riproduce i campioni AL BIT anche col bordo fuori dalla corsa *(i DEVE `ST-M` lo dicono per il centro e `M` dello stato, non per l'evoluzione)*; **(d)** il costo vero di `LIB1` e `LIB2` *(sotto, stimato)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO *(le letture e i DEVE fissati PRIMA dei numeri)*

### 2.1 LA LIBRERIA *(dopo la scelta di `R_t`)*

- **`doc/referti_l2/libreria_solitoni/indice.json`** *(nel repo)* **e gli oggetti su `E:\soliton_simulator\libreria\<nome>.npz`.** **Ogni oggetto:** `psi` e `D = phi - c(t) F3` **dentro `R_t`** dal centro *(zero fuori)*, **in coordinate RELATIVE al centro** *(`d1`, `d2` interi dal nodo del centro arrotondato, e lo scarto sub-nodo)*; **e i dati:** la corsa di origine, il tick, lo `sha` dello stato, `c(t)`, il centro, `R_t`, `M`, `E`, `w`, il cuore, `Gamma(12)`, `L` di origine, **e lo `sha` del file dell'oggetto.**
- **Il primo lotto proposto:** **gli stati di `TBS` a `t 15000, 16500, 18000, ..., 24000`** *(i tick `100000 .. 160000`: sette, abbastanza per l'esagono piu' il centrale)*. **Il perche':** maturi *(dopo `t 15000` il cuore e `w` cambiano lentamente)* e di tempi diversi *(l'attenzione 3)*.

### 2.2 `LIB0`, IL RITAGLIO *(uno stato: `TBS` a `t 15000`, il tick `100000`)*

- **Per `R_t` della griglia** *(la premessa 3: `16 .. 40`)*: **la massa fuori** `M_fuori / M`; **l'energia fuori** `1 - E[ritagliato] / E[intero]` *(`E` col vuoto `c(t) F3` fuori)*; **il salto al bordo:** **`max |psi|` sull'anello `[R_t - 1, R_t)` diviso `max |psi|`**, e **lo stesso per `|D|`**; **e la norma relativa del pezzo tolto** `|psi - psi_t| / |psi|`, `|D - D_t| / |D|` *(e' il numero che `LIB1` confronta al tick `1`)*.
- **Il criterio di scelta di `R_t`, proposto PRIMA** *(decide Luca)*: **il piu' piccolo `R_t` della griglia con la massa fuori, l'energia fuori e i due salti TUTTI sotto `1e-6`** *(il `TOLL` delle carte del campo, `float32`)*. **Il perche' del piu' piccolo:** **un oggetto piccolo si incolla piu' vicino** *(i cluster vogliono `d` di `24 .. 50`)*. ### ⚠ **Se nessun `R_t <= 28` passa, l'oggetto e' piu' grande della distanza dei cluster** *(e le corone si sovrappongono: e' la fisica, non un difetto)*: **lo si dice, non lo si nasconde.**

### 2.3 `LIB1`, LA RIUTILIZZABILITA' *(`L 81`, il bordo di `TB3` sul centro di `TBS`; `2000` tick)*

- **L'originale:** lo stato di `TBS` al tick `T0 = 100000`, **evoluto col ciclo della corsa** *(`AC.tick`, poi `BO.assorbi` con `c(t) F3`)* per `2000` tick. ### **`LIB1-0`** *(DEVE PASSARE, il braccio 0)*: **l'originale rigirato riproduce i campioni di `TBS`** *(`M`, il centro, `w`)* **ai tick dei campioni entro `1e-12` relativo** *(credo AL BIT; se no lo scarto si stampa e la tolleranza e' mia)*. **Senza questo, «evolve come l'originale» non ha un originale.**
- **L'incollato:** l'oggetto a `R_t` nello **stesso posto**, in un vuoto nuovo `c(T0) F3` *(la stessa fase)*, **lo stesso bordo**, lo stesso ciclo. **Stampati nel tempo:** `|psi_i - psi_o| / |psi_o|`, `|phi_i - phi_o| / |phi_o - c F3|`, la distanza dei centri, `w`, il cuore.
- **I DEVE** *(di Luca, con le soglie)*: **`LIB1-1`** lo scarto relativo di `psi` al tick `1` **entro il pezzo tolto di `LIB0`** *(la norma relativa di `psi - psi_t`)* **per `(1 + 1e-2)`** *(il fattore e' MIO: un tick quasi lineare e unitario conserva la norma della differenza, il bordo la riduce; decide Luca)*; **`LIB1-C`** la distanza dei centri **entro `0.2` nodi** *(Luca: l'oscillazione del singolo)* **per `2000` tick**; **`LIB1-F`** *(DEVE FALLIRE)*: **lo stesso oggetto nel vuoto `c(T0 + 7) F3`** *(`7 omega = 21 pi / 20`: il tick intero piu' vicino alla fase opposta, una scelta mia)* **dà lo scarto di `psi` al tick `1` entro lo stesso limite** -- **deve fallire.**
- **`LIB1-U`** *(DEVE PASSARE, per la premessa 7 (i))*: **lo stato di `TBS` ruotato di una fase globale `e^{i a}`** *(`psi` e `phi` insieme)* **evoluto un tick col vuoto di riferimento ruotato = l'originale evoluto e ruotato, entro `1e-12`**; **`LIB1-U-F`** *(deve fallire)*: **solo `psi` ruotata.** **Se `LIB1-U` fallisce, la via (i) e' chiusa** *(e restano solo gli stati alla stessa fase: la premessa 7 (ii))*.
- **La fase degli stati salvati:** **`c_di` ai tick `100000 .. 160000` stampati**, e **`LIB1-P`** *(DEVE PASSARE)*: **tutti alla stessa fase entro `|omega - 3 pi / 20| x (t_max - t_min)`** *(la premessa 7 (ii); la soglia DERIVATA: `omega` e' MISURATO, `corsa_accensione` lo vuole entro `1e-14` da `3 pi / 20`, e su `60000` tick quello scarto fa fino a `~6e-10` di fase -- **una soglia di `1e-12` sarebbe sotto la risoluzione, l'errore di IS2**)*.

### 2.4 `LIB2`, IL TRANSITORIO

- **L'incollato evoluto `1000` unita' di tempo** *(`6667` tick)* **col bordo**; **la materia assorbita per blocchi di `100`** contro **quella di `TBS` negli stessi tick** *(dal jsonl: `M_ass` dei campioni, nessuna corsa in piu')*. **Stampato: quanto produce il ritaglio** *(la differenza, per blocco)*. **Nessun verdetto** *(la lettura e' di Luca)*.

### 2.5 IL COSTO *(stimato PRIMA, dal codice e dalle corse)*

- **`L 81`:** **`~0.099` s per tick** *(`S162` su `L 162` `4707` s per `10000` tick, `4.75` volte `TB3`)*. **`LIB1`:** l'originale `2000` + l'incollato `2000` + `LIB1-F` `2000` *(basta anche meno, ma lo stesso numero e' piu' semplice)*; **`LIB2`:** `6667` *(l'incollato prosegue)*; **`LIB1-U`:** `2` tick. **Totale `~12700` tick, `~21` minuti**, piu' le misure. ### ⚠ **Luca ha scritto «pochi minuti»: sono `~20`-`30`.** **Lo dico prima; si fa comunque fra due corse, da solo.** **`LIB0`:** secondi.
- **Lo spazio:** gli oggetti `~R_t^2` nodi, `< 1` MB l'uno; **sette, `< 10` MB su `E:`.**

### 2.6 I CLUSTER *(la proposta; DOPO la coppia, ciascuno col suo FERMO prima del codice)*

| | la forma | `L` | il bordo | le fasi relative | gli stati |
|---|---|---|---|---|---|
| **(a)** | **il triangolo** di lato `d` | `162` | quello di `TB3`, centro sul baricentro; `R_A = d / sqrt 3 + 30` *(`d 35`: `50.2`)* | **tutte `0`** *(il caso piu' semplice; con tre vicini l'alternanza `0, pi` non si chiude: un triangolo e' «frustrato»)* | `t 15000, 16500, 18000` |
| **(b)** | **la fila di tre**, passo `d` | `162` | centro sul centrale; `R_A = d + 30` *(`d 35`: `65`)* | **alternate `0, pi, 0`** *(se la coppia dice che `pi` lega)* **o tutte `0`** | gli stessi tre |
| **(c)** | **l'esagono di sei piu' il centrale** | `162` | centro sul centrale; `R_A = d + 30` | **tutte `0`** *(l'esagono con il centrale e' fatto di triangoli: frustrato anche lui)* | `t 15000 .. 24000` *(sette)* |

- **`d` si sceglie DOPO le corse della coppia** *(Luca)*. **Con `R_B = 81` la rampa del bordo e' `81 - R_A`: a `d 35` per (b) e (c) `16` nodi** *(`TB3`: `12.5`)*: **basta.** **Per `d > 50` (b) e (c) non ci stanno su `L 162`** *(`R_A > 80`)*.
- **Il costo:** **come una corsa della coppia** *(il costo scala coi nodi, non coi solitoni)*: **`~8.7` ore per `10000` unita' di tempo su `L 162`**; **lo spazio:** **come `S162`** *(le mappe `~112` MB, gli stati `~63` MB su `E:`)*.
- **Le misure** *(di Luca)*: i centri di ciascuno, le distanze, il baricentro, **la rotazione dell'aggregato** *(il momento angolare dai centri)*, la forma, **l'emissione totale contro la somma dei singoli**, **la circolazione di ciascuno** *(se si sincronizzano)*, il campo del vuoto fra loro; mappe e stati come `TBS`.
- ### **LE LETTURE** *(di Luca, scritte qui PRIMA)*: **(k1)** l'aggregato si tiene insieme *(legato)*; **(k2)** si disfa; **(k3)** si fonde in un solitone solo; **(k4)** ruota o si sincronizza; **(k5)** altro.

### 2.7 COSA MI FAREBBE FERMARE

- **`LIB1-0` che fallisce** *(l'originale non si riproduce fuori dalla corsa: non c'e' un originale)*; **`LIB1-1` o `LIB1-C` che falliscono** *(l'oggetto non e' riutilizzabile a quell'`R_t`)*; **`LIB1-F` che passa** *(l'attenzione 1 non e' vera, o il controllo non legge la fase)*; **`LIB1-P` che fallisce** *(le fasi degli stati diverse: si torna alla via (i))*; **un `assert` del nucleo** *(come IS3)*.

## 3. TODO

1. **Questo task history, la MAPPA** *(la voce «la libreria dei solitoni maturi e i cluster»)*, **la relazione: un commit.** ### **FERMO su `R_t` e sui cluster** *(le domande in fondo)*.
2. **Il codice** *(`csv/solitone/libreria.py`, nuovo: `--lib0`, `--lib1 R_t`, `--lib2 R_t`, `--costruisci R_t`)* **committato prima di girarlo, con l'INVENTARIO; `D6`, la cassetta, `LIB0` FRA `C35-0` E `C35-pi`** *(con le mappe leggere: un calcolo alla volta)*; **`LIB1`, `LIB2` e la libreria DOPO la scelta di `R_t`.**
3. **I cluster: dopo la coppia, ciascuno col suo FERMO prima del codice.**

## 4. LE DOMANDE A LUCA *(il criterio di chiusura: le sue risposte, scritte qui)*

1. **La griglia di `R_t`:** **`16, 20, 24, 28, 32, 36, 40`** *(la tua `28 .. 40` sta tutta nella fascia di `TBS`: la premessa 3)*?
2. **Il criterio:** **il piu' piccolo `R_t` con massa fuori, energia fuori e salti sotto `1e-6`**?
3. **`LIB1-1`:** **il fattore `1 + 1e-2`** sul pezzo tolto?
4. **I cluster:** quali, e con quali fasi *(la tabella 2.6)*?
