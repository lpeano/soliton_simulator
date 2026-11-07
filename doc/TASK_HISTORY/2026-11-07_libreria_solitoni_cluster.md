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

## 5. LA DECISIONE DI LUCA DEL `2026-11-07` `10:06` *(le domande della sez. `4` CHIUSE)*

1. ### **La griglia di `R_t`: `16, 20, 24, 28, 32, 36, 40`.**
2. ### **Il criterio: il piu' piccolo `R_t` con massa fuori, energia fuori e salti sotto `1e-6`.**
3. ### **`LIB1-1` col fattore `1 + 1e-2`.**
4. ### **I cluster: RIMANDATI a dopo `C35-pi` e `C50-0`** *(nelle parole di Luca: «`C35-0` si e' fuso: la scelta dei cluster dipende da cosa fa l'opposizione di fase»)*.
5. ### **L'ordine: `LIB0`-`LIB2` fra `C35-pi` e `C50-0`** *(un calcolo alla volta, insieme alle cure e alle carte IS2 e IS3)*.

- ### ⚠ **Una nota onesta sul punto `4`:** **«`C35-0` si e' fuso» NON e' ancora una misura del repo.** **Il log di `C35-0` porta le misure del SINGOLO attorno al centro della densita' totale** *(il punto medio)*, **non una lettura della coppia** *(`coppia_corse`, sez. `12`)*: ### **lo dira' `d(t)` nel referto della coppia** *(`carta_coppia.py`, a `C35-pi` finita)*. **La decisione di rimandare i cluster non dipende da questo, e resta.**
- **Durante `C35-pi`: il codice di `libreria.py`** *(un file nuovo, che la corsa non importa)*, **committato prima di girarlo; `LIB0` a corsa chiusa.**

## 6. L'AVVIO DI LUCA DELLE `16:01`-`16:04`: **LA LIBRERIA SUBITO, IN UN PROCESSO SEPARATO** *(un'ECCEZIONE DICHIARATA a «un calcolo alla volta», SOLO per la libreria)*; **E OGNI CORSA SALVA SEMPRE LO STATO COMPLETO**

- ### **Le premesse dal sistema, misurate prima:** **NESSUNA corsa e' in volo** *(`C35-pi` e' finita, `18fc47c3`)*: **«di quanto rallenta la corsa in volo» non si puo' misurare oggi: lo dico, non lo invento.** **Le risorse:** **`12` core, `14.0` GB liberi su `33.3`** *(`Win32_OperatingSystem`)*; **la libreria e' un processo solo, `L 81`, sotto `1` GB.**
- ### **Il codice della libreria NON c'era** *(il TODO `2` della sez. `3` aspettava `R_t`, deciso alle `10:06`)*: **lo scrivo ora** *(`csv/solitone/libreria.py`)*, **committato prima di girarlo, e lo giro SUBITO** *(Luca)*.
- **Le scelte, dichiarate:** **un processo solo, in ordine: `LIB0` -> la scelta di `R_t` col criterio di Luca -> la costruzione** *(sette oggetti, `TBS` ai tick `100000 .. 160000`)* **-> `R2` -> `LIB1` -> `LIB2`**; ### **l'oggetto si conserva nel riferimento della corsa d'origine** *(gli array interi, zero fuori da `R_t`, col centro: si trasla con `roll` esatto)* **invece che «in coordinate relative»** *(2.1)*; **`LIB1-0` contro gli `sha` di `dopo_stato`** *(`100` tick col ciclo della corsa: un confronto AL BIT, piu' forte dei campioni a `1e-12` di 2.3)*; **le chiavi derivate dello stato** *(`Lambda`, `rho`, `h_int`, `psi`)* **dell'incollato dallo stato d'origine.**
- ### **`R2` sulla libreria** *(Luca: «se I1 non e' pronta, la libreria salva nel formato di R4 e fa la prova R2 su almeno un elemento»)*: **l'oggetto riletto dal file** *(lo `sha1` contro l'indice)* **e ripartito due volte per `100` tick: gli `sha` di ogni chiave al bit; il DEVE FALLIRE: senza il disturbo del vuoto `D`.** ### ⚠ **Il formato non e' ancora quello di R4** *(il commit e l'impronta nel file: li mette I1)*: **gli oggetti si registrano in I1 senza rigirarli** *(Luca)*.
- **I1, I3, I4:** **sequenziali, dopo** *(il task history di I1 prima del codice)*.

## 7. L'ESITO DI `LIB0` *(`doc/referti_l2/libreria_solitoni.txt`, `libreria.py` `6c015f66`; `10` s, exit `2`)*: **NESSUN `R_t` PASSA IL CRITERIO: FERMO** *(Luca `10:06`: «lo si dice, non lo si nasconde»)*

| `R_t` | `M` fuori / `M` | `E` fuori | il salto di `psi` | il salto di `D` | `|psi - psi_t| / |psi|` | `|D - D_t| / |D|` |
|---|---|---|---|---|---|---|
| `16` | `2.909e-02` | `+3.330e-02` | `3.626e-01` | `6.592e-01` | `1.706e-01` | `5.599e-01` |
| `20` | `5.437e-05` | `+5.732e-05` | `1.353e-01` | `7.862e-01` | `7.374e-03` | `2.484e-01` |
| `24` | `1.113e-06` | `+9.745e-07` | `1.339e-03` | `4.827e-02` | `1.055e-03` | `1.644e-02` |
| `28` | `5.812e-07` | `+4.594e-07` | `1.269e-03` | `2.382e-02` | `7.624e-04` | `7.298e-03` |
| `32` | `1.529e-07` | `-1.836e-07` | `9.168e-04` | `8.124e-03` | `3.910e-04` | `3.501e-03` |
| `36` | `1.564e-08` | `+1.650e-08` | `3.651e-04` | `4.273e-03` | `1.250e-04` | `1.123e-03` |
| `40` | `5.765e-10` | `-3.847e-09` | `1.140e-04` | `1.082e-03` | `2.401e-05` | `2.315e-04` |

- **La massa e l'energia fuori scendono sotto `1e-6` a `R_t = 28`** *(`5.8e-07`, `4.6e-07`)*; ### **i due SALTI no, a nessun `R_t`** *(a `40`: `psi` `1.1e-04`, `D` `1.1e-03`)*.
- ### **Una cosa da dire, senza scegliere:** **il salto e' un rapporto di AMPIEZZE** *(`max |psi|` sull'anello / `max |psi|`)*, **la massa e l'energia sono QUADRATICHE**: **un salto di `1e-6` in ampiezza e' `1e-12` in densita'**: ### **il criterio scritto chiede ai salti sei ordini in piu' che alla massa.** **Con lo stesso ordine** *(il salto al quadrato sotto `1e-6`, cioe' il salto sotto `1e-3`)* **passerebbe `psi` da `R_t = 32` e `D` a nessuno** *(`1.08e-03` a `40`)*. **E `D` e' il disturbo del VUOTO**: **la corona del vuoto arriva fino al bordo di `TBS`** *(`R_A 28`, `R_B 40.5`)*: **il ritaglio taglia il vuoto disturbato, non la materia.**
- ### **FERMO** *(la costruzione, `R2`, `LIB1`, `LIB2` non sono girati)*: **la decisione e' di Luca.** **Le strade che vedo** *(nessuna scelta)*: **(a)** il criterio dei salti QUADRATICO *(il salto al quadrato sotto `1e-6`)*, con `R_t` deciso da `psi` e `D` dichiarato come corona del vuoto che si ritaglia; **(b)** `R_t = 40` *(il massimo)*, dichiarando i salti; **(c)** l'oggetto con TUTTO `D`** *(il vuoto disturbato del toro intero, come `coppia_matura`)* **e `psi` ritagliato**; **(d)** un altro criterio.

## 8. LA DECISIONE DI LUCA DEL `2026-11-07` `16:43`: **IL CRITERIO QUADRATICO PER `psi`, IL VUOTO `D` INTERO** *(il FERMO della sez. `7` CHIUSO)*

- **(a) il criterio quadratico:** **`R_t` = il piu' piccolo con la massa fuori, l'energia fuori e il SALTO AL QUADRATO di `psi` sotto `1e-6`** *(atteso `32`: a `28` `(1.269e-03)^2 = 1.61e-06`, a `32` `(9.168e-04)^2 = 8.4e-07`)*; **(c) `D` INTERO** *(il vuoto disturbato del toro, come `coppia_matura`)*. **Dichiarato:** **`D` contiene la risposta del vuoto al pezzo di `psi` tolto** *(ordine `1e-6`)*. **I cluster rimandati** *(con `D` intero due oggetti non si sommano in modo semplice: il vuoto non e' lineare -- un problema dei cluster)*.
- ### **IL DEVE PRINCIPALE di Luca, LA FISICA DEL TAGLIO:** **l'oggetto ritagliato fatto ripartire contro l'originale, `>= 1000` unita' di tempo, col ciclo della corsa: la differenza in densita' per regione** *(cuore, corona, fascia)* **al livello del taglio** *(`~1e-6`)* **e NON crescente** *(la pendenza)*; **DEVE FALLIRE: con `D` ritagliato** *(la via vecchia)* **la differenza molto piu' grande o crescente**; **se cresce con `D` intero: FERMO.**

### 8.1 ⚠ UNA PREMESSA DAL REPO CHE PESA SUL DEVE, detta PRIMA *(il promemoria «DEVE contro la propria premessa»)*

- ### **LA DINAMICA E' CAOTICA, ANCHE COL BORDO** *(`doc/TASK_HISTORY/2026-11-05_D5_semi_e_caos.md`: «il bordo NON cambia la crescita del caos nella sua finestra: `TBS` rompe la simmetria negli stessi tempi di `TS` senza bordo -- `psi` sopra `1e-12` a `528`, `1e-6` a `1081.5`»; `D0R`: un fattore `e` ogni `~25` unita' di tempo)*: ### **una differenza iniziale di `1e-6` cresce di un fattore `e` ogni `~40` unita' di tempo** *(`ln 1e6 / 553`)*, **e arriva all'ordine `1` in `~550` unita'.**
- ### **QUINDI la differenza fra l'oggetto ritagliato e l'originale CRESCERA' entro `1000` unita' di tempo PER IL CAOS, qualunque sia il taglio** *(anche un taglio innocuo)*: **il DEVE come e' scritto** *(«resti a `1e-6` e non cresca»)* ### **fallira' per costruzione**, **e il FERMO che ne segue non direbbe niente del taglio.**
- ### **IL CONTROLLO CHE SEPARA IL TAGLIO DAL CAOS** *(MIO, dichiarato, in piu')*: **un quarto braccio: l'originale con una perturbazione CASUALE della STESSA norma del pezzo tolto** *(`|psi - psi_t|`, un seme dichiarato)*, **che non toglie niente** *(la «linea del caos»)*. ### **La lettura che propongo:** **il taglio e' innocuo se la differenza col `D` intero cresce COME quella della perturbazione casuale** *(stessa pendenza, stesso livello di saturazione)*, **e non di piu'**; **la via vecchia** *(`D` ritagliato: un pezzo di `|D - D_t| / |D| = 3.5e-03` a `R_t 32`, `~10^4` volte piu' grande)* **deve partire PIU' IN ALTO.**
- **Cosa faccio:** **giro il DEVE di Luca COME E' SCRITTO** *(la soglia `1e-6` e la pendenza)*, **piu' il braccio del caos, stampato accanto senza verdetto**: ### **se il DEVE fallisce, mi fermo come vuole Luca** *(niente altri sei oggetti)*, **e riferisco la lettura col braccio del caos.**

### 8.2 IL CODICE *(`libreria.py`, modificato)*

- **Le regioni** *(dal centro dell'originale a `T0`)*: **il cuore `r < w`** *(`w` del campione a `T0`)*, **la corona `w <= r < R_A`, la fascia `r >= R_A`** *(il bordo di `TBS`, `28`)*. **Le differenze:** **`|M_reg(X) - M_reg(orig)| / M` e `|E_reg(X) - E_reg(orig)| / |E|`** *(come la massa e l'energia fuori di `LIB0`)*, **ogni `100` tick, per `6667` tick** *(`1000` unita' di tempo)*.
- **I quattro bracci, uno dopo l'altro nello stesso processo:** **l'originale; l'oggetto con `D` intero; l'oggetto con `D` ritagliato** *(DEVE FALLIRE)*; **l'originale perturbato** *(il caos)*. ### **LIB1 e LIB2 dagli stessi bracci** *(l'originale e l'oggetto con `D` intero: il centro, il tick `1`, l'assorbito)*: **nessuna corsa in piu'.**
- **Il costo:** **`4 x 6667` tick `~45` minuti** *(con la catena delle carte della coppia accanto: piu' lento; l'eccezione di Luca delle `16:01`)*. **Le risorse:** `12` core, la catena delle carte e la libreria, due processi.

## 9. L'ESITO *(`libreria.py` `27a897f1`; `doc/referti_l2/libreria_solitoni.txt`; `24` minuti, exit `1`)*: **`R_t = 32`; IL PRIMO OGGETTO; `10/12`; FALLISCONO `L3` (IL CAOS, PREVISTO) E `LIB1-P` (UN ERRORE MIO DI SOGLIA)** -- **FERMO**

- **`R_t = 32`** *(il criterio quadratico: a `32` la massa fuori `1.529e-07`, l'energia fuori `-1.836e-07`, il salto di `psi` al quadrato `8.40e-07`)*. **Il primo oggetto:** `E:\soliton_simulator\libreria\TBS_100000_R32.npz` *(`2521422` byte; l'indice `doc/referti_l2/libreria_solitoni/indice.json`)*. **Gli altri sei NON costruiti** *(L3 fallita: Luca)*.
- **Passano:** `L0-S`; ### **`R2`** *(l'oggetto riletto e ripartito due volte per `100` tick: al bit, `6` chiavi)* **e `R2-F`** *(senza `D`: diverge)*; ### **`LIB1-0`** *(il ciclo della corsa fuori dalla corsa ridà gli `sha` di `dopo_stato` AL BIT)*; **`LIB1-U`** *(`6.791e-15`)* **e `LIB1-U-F`** *(`6.858e-01`)*; **`LIB1-1`** *(`3.858e-04` contro `3.910e-04 x 1.01`)*; **`LIB1-C`** *(la distanza dei centri `0.0000` in `2000` tick)*; **`LIB1-F`** *(`5.580e-03`: fallisce come deve)*.
- ### **`LIB1-P` FALLISCE: le fasi di `c(t)` ai sette tick differiscono di `3.347e-12`, la soglia `1.000e-14`** -- ### **UN ERRORE MIO DI SOGLIA:** **avevo scritto «`|omega - 3 pi/20| x (t_max - t_min)`», e `omega` del npz E' `3 pi/20` al bit** *(la differenza `0.0`)*: **la soglia si riduce al `1e-14` aggiunto**; ### **ma `c(t)` porta l'ARROTONDAMENTO di `omega t`** *(`t ~1.6e5`: `t omega eps = 1.67e-11`)*: **la soglia era sotto la risoluzione** *(lo stesso errore di IS2)*. **Le fasi sono le stesse entro `3.3e-12` rad** *(la premessa 7 (ii) della sez. `1` regge)*; **la cura: la soglia `t_max omega eps`, un commit a se'.**
- ### **`L3` FALLISCE, COME PREVISTO PER IL CAOS** *(sez. `8.1`)*: **col `D` intero il massimo `6.446e-04`, la crescita `+4.331e-04`; col `D` ritagliato `5.082e-04`, `+3.041e-04`; il braccio del caos `6.651e-04`, `+3.749e-04`.** ### **I numeri dicono, nell'ordine:**
  1. **all'inizio** *(`t 15`)* **il taglio e' al suo livello:** **col `D` intero la fascia `7.4e-09` in massa, `5.0e-09` in energia; col `D` ritagliato l'energia nella fascia `1.16e-07`, `23` volte di piu'** *(la via vecchia parte PIU' IN ALTO, come voleva Luca)*; **il braccio del caos `2.3e-06`** *(una perturbazione su tutto il toro)*;
  2. ### **poi tutti e tre crescono allo STESSO ritmo, quello del caos:** **col `D` intero `6.1e-08` a `t 100`, `2.3e-06` a `300`, `1.4e-05` a `500`, `6.2e-04` alla fine** *(un fattore `e` ogni `~40`-`55` unita': la scala di `D5`)*: **a `t ~500` i tre bracci sono allo stesso livello** *(`1e-05`-`1e-04`)*.
  ### **LA LETTURA CHE PROPONGO** *(non una decisione)*: **il taglio e' innocuo QUANTO una perturbazione qualunque della stessa taglia**: **parte al suo livello e cresce come il caos, non di piu'**; **`D` ritagliato parte piu' in alto nella fascia, poi il caos copre la differenza.** ### **Il DEVE come e' scritto non puo' passare con NESSUN taglio** *(neanche col braccio del caos, che non taglia niente)*.
- **`LIB2`:** **nel primo blocco l'incollato assorbe `0.172` MENO di `TBS`** *(`3.964` contro `4.136`)*: ### **e' la massa tagliata** *(fuori da `R_t = 32`, nella fascia: `1.529e-07 x M = 0.152`)*, **che `TBS` avrebbe assorbito**; **poi le differenze per blocco fino a `-0.70`** *(il caos)*.
- ### **FERMO** *(Luca 16:43)*. **Le domande:** **(1) `L3`: si accetta la lettura «innocuo quanto il caos»** *(il DEVE riscritto come: la differenza col `D` intero non piu' grande di quella del braccio del caos, a ogni tempo, entro un fattore da decidere)*, **o un altro criterio?** **(2) `LIB1-P`: la soglia `t_max omega eps`** *(la cura del mio errore)*: **la rifaccio?**

## 10. LA DECISIONE DI LUCA DEL `2026-11-07` `17:55`: **IL CAOS COME RIFERIMENTO** *(i FERMI della sez. `9` CHIUSI)*

- **Il principio:** **per ogni confronto fra due evoluzioni il criterio e' «la differenza non cresce PIU' DEL CAOS»** *(un braccio di controllo, o le velocita' gia' misurate)*. **L'errore `n.116` del guardiano** *(il DEVE `L3` delle `16:43` ignorava il caos)*; **il braccio del caos della sez. `8.1` era giusto.** ### **DICHIARATO: le soglie sono fissate DOPO i numeri, ancorate a misure fatte PRIMA.**
- ### **(1) `L3` PASSA se la differenza col `D` intero non supera quella del braccio del caos di piu' di un FATTORE `2`, a OGNI tempo campionato**; **(2) `LIB1-P` con la soglia `t_max omega eps`**; **poi gli altri SEI oggetti, `R2` su ciascuno, il braccio del caos solo del primo** *(dichiarato)*.
- ### ⚠ **UNA PREMESSA DAI NUMERI GIA' STAMPATI, PRIMA DI RIGIRARE:** **il referto di `9eda4121` stampa una riga ogni `10` campioni** *(`7` tempi per braccio)*, **e a `t 615` la differenza col `D` intero e' `1.313e-04`, quella del caos `8.505e-06`** *(le energie del cuore)*: **un rapporto `~15`.** ### **Il criterio PUNTO PER PUNTO confronta due grandezze che OSCILLANO** *(la differenza fra due evoluzioni caotiche passa vicino a zero quando i due solitoni si ritrovano in fase nel respiro)*: **il rapporto di due grandezze che oscillano puo' superare `2` anche se crescono allo stesso ritmo.** **Lo misuro con uno script sui tempi stampati** *(`csv/solitone/_l3_rilettura.py`)* **prima di rigirare la libreria** *(`45` minuti)*: ### **se il rapporto supera `2`, FERMO** *(Luca)* **e riferisco, con la proposta di confrontare gli INVILUPPI** *(il massimo corrente)* **invece dei valori punto per punto.**

## 11. LA CORREZIONE DI LUCA DEL `2026-11-07` `18:02`: **L3 SUGLI INVILUPPI** *(l'errore `n.117` del guardiano: il criterio punto per punto; la premessa di `646c6620` era giusta)*

- ### **IL CRITERIO 1 CORRETTO:** **l'INVILUPPO** *(il massimo corrente da `t 0` a `t`)* **col `D` intero non supera di piu' di un fattore `2` quello del braccio del caos, a ogni tempo campionato, per la massa e l'energia di ciascuna regione.** **DICHIARATO: fissato dopo i numeri, ancorato al braccio del caos.** **Lo script:** `_l3_rilettura.py` riscritto *(i valori, i due inviluppi, il rapporto, per ciascuna delle sei grandezze; e il `D` ritagliato senza verdetto)*. **Se supera `2`: FERMO.** **Se passa:** **gli altri sei oggetti** *(un modo della libreria che NON rigira i quattro bracci: K1, il braccio del caos solo del primo)*.

## 12. L3 SUGLI INVILUPPI, L'ESITO *(`_l3_rilettura.py` `06c289bd`, `doc/referti_l2/libreria_l3_rilettura.txt`; Luca `18:02`-`18:13`)*: **PASSANO CINQUE GRANDEZZE SU SEI; FALLISCE L'ENERGIA DELLA FASCIA** -- **FERMO**

- ### **Il campionamento e' RADO** *(Luca `18:13`, E1)*: **il referto di `9eda4121` stampa SETTE tempi per braccio** *(`t 15, 165, .., 915`: una riga ogni `10` campioni)*, **e i campioni ogni `100` tick NON sono salvati altrove**: **la rilettura vale su quei sette** *(non si rigira la libreria, Luca)*.
- **I rapporti degli inviluppi `D intero / caos`, ai sette tempi:**

| | `t 15` | `165` | `315` | `465` | `615` | `765` | `915` |
|---|---|---|---|---|---|---|---|
| **`M` cuore** | `0.000` | `0.008` | `0.325` | `0.468` | `1.534` | `1.294` | `1.667` |
| **`M` corona** | `0.001` | `0.012` | `0.405` | `0.484` | `1.583` | `1.257` | `1.684` |
| **`M` fascia** | `0.551` | `0.551` | `0.551` | `0.977` | `0.865` | `0.736` | `0.835` |
| **`E` cuore** | `0.000` | `0.009` | `0.312` | `0.464` | `1.529` | `1.271` | `1.680` |
| **`E` corona** | `0.000` | `0.012` | `0.389` | `0.478` | `1.574` | `1.219` | `1.695` |
| ### **`E` fascia** | ### **`4.022`** | ### **`4.022`** | `0.251` | ### **`4.659`** | `0.996` | `0.780` | `0.780` |

- **Il conto del guardiano** *(l'energia del cuore: `0.003, 0.01, 0.31, 0.46, 1.53, 1.22, 1.68`)*: **confermato dallo script entro la terza cifra** *(`1.271` contro `1.22` a `t 765`)*.
- ### **FALLISCE L'ENERGIA DELLA FASCIA, a `t 15`, `165`, `465`** *(il massimo `4.659`)*: **col `D` intero `5.0e-09`, `5.0e-09`, `9.4e-08` contro il caos `1.3e-09`, `1.3e-09`, `2.0e-08`.** ### **Due cose da dire, senza scegliere:** **(1) il TAGLIO STA NELLA FASCIA** *(`R_t = 32 > R_A = 28`)*: **la differenza nella fascia all'inizio E' il taglio** *(il pezzo tolto e la risposta del vuoto)*, **e la perturbazione casuale del caos, sparsa su tutto il toro, ne mette meno li'**; **(2) i numeri sono a `1e-09`-`1e-07`, SOTTO la soglia del taglio di `LIB0`** *(`1e-6`)* **e sotto gli inviluppi delle altre regioni** *(`~3e-04` alla fine)*. **E il `D` ritagliato ha l'inviluppo dell'energia della fascia `1.16e-07` gia' a `t 15`** *(`23` volte quello col `D` intero)*.
- ### **FERMO** *(Luca: se supera `2`, FERMO e riferire)*: **gli altri sei oggetti NON costruiti.** **Le cautele** *(E3)*: **il braccio del caos e' UNO, con UN seme** *(un secondo seme, `~11` minuti, darebbe la dispersione del caos stesso: un'opzione, decide Luca)*; **il campionamento e' rado** *(sette tempi)*.

## 13. LA DECISIONE DI LUCA DEL `2026-11-07` `18:22`: **IL BRACCIO DEL CAOS NELLA REGIONE DEL TAGLIO** *(il FERMO della sez. `12` CHIUSO)*

- **La lettura di Luca:** **il taglio sta DENTRO la fascia; il braccio del caos su tutto il toro ne mette meno li': il confronto non e' equo** *(l'impronta del taglio a `t 15`, poi assorbita)*. ### **La via 1:** **si rigira SOLO il braccio del caos, con la STESSA norma del pezzo tolto e la STESSA distribuzione: solo fuori da `R_t`**; **il seme dichiarato; la stessa durata e gli stessi campioni.** **Il criterio NON cambia** *(gli inviluppi, il fattore `2`, le sei grandezze)*.
- ### ⚠ **Una cosa dal codice, dichiarata:** **le differenze si misurano CONTRO L'ORIGINALE, e le serie per regione dell'originale NON erano salvate** *(il referto stampava sette righe)*: ### **l'originale si rigira insieme al braccio** *(e' deterministico: `LIB1-0` lo riproduce al bit)*: **il costo `~22` minuti, non `~11`.** **Il braccio vecchio resta accanto nella rilettura, dichiarato.** **Il nuovo referto stampa TUTTE le righe** *(ogni `100` tick)*; **la rilettura usa le sette `t` di `D intero`.** **Il seme: `2`** *(il primo braccio usava `1`)*.
- **Il codice:** `libreria.py --caos-locale` *(`ed67976c`)*; `_l3_rilettura.py` *(`737e5969`: il riferimento localizzato se c'e', accanto il rapporto col vecchio)*.

## 14. IL BRACCIO DEL CAOS LOCALIZZATO, L'ESITO *(`libreria.py --caos-locale` `ed67976c`, `doc/referti_l2/libreria_caos_locale.txt`; `_l3_rilettura.py` `737e5969`)*: **FALLISCE IN PIU' PUNTI, ANCHE PIU' DI PRIMA** -- **FERMO**

- **Il braccio:** **il seme `2`, la perturbazione solo fuori da `R_t = 32`** *(`17076` estremita' su `39366`)*, **la norma `3.899937e-01`** *(relativa `3.909626e-04`, = il pezzo tolto)*; **l'originale rigirato con lui** *(`L0-S` al bit)*. **`2/2` controlli; `15` minuti.**
- **I rapporti degli inviluppi `D intero / caos localizzato`** *(accanto quelli col braccio vecchio su tutto il toro)*:

| | `t 15` | `165` | `315` | `465` | `615` | `765` | `915` |
|---|---|---|---|---|---|---|---|
| **`M` cuore** | ### `inf` | `0.587` | `1.553` | ### `4.165` | ### `3.208` | `0.981` | `0.932` |
| **`M` corona** | `1.451` | `0.769` | `1.537` | ### `4.140` | ### `3.214` | `0.983` | `0.934` |
| **`M` fascia** | `1.524` | `1.524` | `1.524` | `1.237` | ### `2.504` | ### `2.504` | `1.381` |
| **`E` cuore** | ### `4.000` | `0.601` | `1.440` | ### `4.323` | ### `3.192` | `0.970` | `0.941` |
| **`E` corona** | `0.091` | `0.673` | `1.410` | ### `4.244` | ### `3.195` | `0.967` | `0.940` |
| **`E` fascia** | ### `24.721` | ### `14.514` | ### `2.394` | `0.876` | `0.736` | `1.255` | `0.978` |

- ### **Cosa dicono i numeri, senza scegliere:**
  1. **`t 15`, il cuore:** **`inf` e `4.000` sono rapporti fra ZERI d'arrotondamento** *(`D intero` `3.5e-16` contro `0.000`: la perturbazione fuori da `R_t` non ha ancora raggiunto il cuore in `100` tick)*: **non e' fisica.**
  2. ### **la fascia all'inizio** *(`24.7`, `14.5`)*: **col `D` intero `5.0e-09`, col caos localizzato `2.0e-10`**: **il taglio toglie un pezzo COERENTE del solitone** *(la sua coda, con la sua fase)*, **il caos aggiunge rumore BIANCO della stessa norma, che si disperde**: **a parita' di norma non agiscono allo stesso modo.**
  3. ### **`t 465`-`615`, cuore e corona `~3`-`4`:** **il caos localizzato cresce PIU' PIANO del braccio vecchio** *(parte lontano dal cuore)*, **e il `D` intero lo supera di `~4` volte per qualche centinaio di unita'; a `t 765` e `915` i due tornano allo stesso livello** *(`0.93`-`0.98`)*.
  4. **col braccio vecchio** *(su tutto il toro)* **cuore e corona restavano sotto `1.7`.**
  ### **Le cautele:** **un solo seme per braccio** *(la dispersione del caos stesso NON e' misurata: un secondo seme la darebbe)*; **sette tempi** *(il `D` intero ha solo le righe stampate; gli inviluppi sono sugli stessi sette tempi per i due bracci)*.
- ### **FERMO** *(Luca: se supera `2` anche col braccio localizzato, FERMO e riferire)*: **gli altri sei oggetti NON costruiti.**

## 15. LA DECISIONE DI LUCA DEL `2026-11-07` `19:37`: **GLI STATI COMPLETI SENZA TAGLIO; IL TAGLIO RIMANDATO AI CLUSTER** *(il FERMO della sez. `14` CHIUSO)*

### 15.1 LA DECISIONE, COME L'HA SCRITTA LUCA

- **`L3` e' stata riformulata TRE volte DOPO i numeri** *(punto per punto, inviluppi, caos localizzato)*: **ogni correzione era motivata, ma continuare adatterebbe la prova al risultato. Ci si ferma.**
- ### **La lettura di `b5d132db`, come FATTO MISURATO:** **il taglio a `R_t 32` e' una perturbazione COERENTE che anticipa la divergenza caotica di circa `55` unita' rispetto a un rumore bianco della stessa norma; dopo, tutto satura allo stesso livello** *(rapporto `~0.95`)*. **Non e' un difetto: e' la differenza fra rumore coerente e rumore bianco.**
- **Il principio:** **in un sistema caotico il confronto fra due evoluzioni si fa sulle GRANDEZZE MEDIE, non sulle traiettorie.**
- **LA DECISIONE:** **(1)** la libreria conserva gli **STATI COMPLETI, NON tagliati** *(tutto il toro: `psi`, `phi`, `D` e ogni grandezza registrata)*, per i sette tick di `TBS` `100000 .. 160000`; **per ciascuno basta `R2`** *(la ripartenza al bit, con `R2-F`)*; **`L3` NON si applica**; **(2)** l'oggetto ritagliato `TBS_100000_R32.npz` **resta su `E:` e nell'indice come «ritagliato, non validato»**, dichiarato; **(3)** **il TAGLIO si riprende con i CLUSTER**, col controllo scritto PRIMA dei numeri sulle grandezze medie *(15.4)*; **(4)** **`LIB1-P` con la soglia derivata `t_max omega eps` resta** *(e' una cura, non un criterio nuovo)*.

### 15.2 LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

- **Gli stati di `TBS` ai sette tick ESISTONO GIA' completi** *(`E:\soliton_simulator\stati\TBS\TBS_stato_<tick>.npz`, con gli `sha` nel jsonl della corsa, letto con `CA.serie("TBS")`)*, **e per tutti e sette c'e' `dopo_stato`** *(gli `sha` dopo `100` tick: `LIB1-0` si fa su TUTTI e sette, non solo sul primo)*. ### **Quindi lo «stato completo» della libreria e' una COPIA di quello della corsa, piu' `D = phi - c(t) F3`, `c(t)`, il centro e il campione registrato a quel tick** *(il bordo: `M_ass`, `E_ass`, `V_ass`; la forma: `w`, `f_liscia`, l'alone)*: **dichiarato, non e' un oggetto nuovo.**
- **Le chiavi dello stato** sono tutti gli array di `z["st"]` *(il ciclo della corsa e' `AC.tick` piu' `BO.assorbi`, e `LIB1-0` al bit sul primo oggetto dice che bastano)*. ### ⚠ **I contatori del bordo** *(`M_ass` accumulato)* **NON entrano nella dinamica** *(`BO.assorbi` li RESTITUISCE, non li legge)*: **si salvano come grandezze registrate, dal campione.** *(Se mi sbaglio, `LIB1-0` sugli altri sei tick lo dira'.)*
- ### **`LIB1-P`, la soglia derivata** *(Luca `17:55`)*: **`t_max omega eps`** *(`t_max = 160000` tick, `omega` per tick dal file della fase, `eps = 2.22e-16`)*: **`~1.7e-11`.** **Il valore misurato in `9eda4121` e' `3.347e-12`** *(sotto la soglia di un fattore `~5`)*: ### **so gia' che passa** *(«DEVE contro la propria premessa»)*: **il controllo che puo' fallire e' `LIB1-P-F`** *(mio, dichiarato: un tick sfasato di `1`, la fase differisce di `omega`, `~0.47`, molto sopra la soglia)*.
- ### **`LIB1-C` su uno stato completo e' banale CONTRO L'ORIGINALE** *(lo stato e' lo stesso al bit: la distanza dei centri e' `0` per costruzione, un FALSO-ZERO)*. ### **Lo faccio CONTRO I CENTRI REGISTRATI DALLA CORSA** *(`per.c1`, `per.c2` dei campioni, ogni `10` tick: `TO.misure` sulla densita' per nodo)*, **per `2000` tick dalla ripartenza**: **e' un controllo che la ripartenza dal FILE DELLA LIBRERIA rifa' la traiettoria che la corsa ha scritto.** ### ⚠ **Cosa NON so:** se la densita' di `per` e' la stessa del mio `centro()` *(`sum |psi_h|^2` per nodo)*: **il controllo di scala e' la distanza a `t = T0`** *(attesa `~0`; se no, e' un'altra densita', e lo dico)*.
- **Non applicabili** *(riguardano il taglio o l'incollo in un vuoto diverso)*: **`LIB1-1`, `LIB1-F`, `L3`, `L3-F`, `LIB2`**: **si stampano «non applicabili», senza verdetto.** **`LIB1-U`** *(la fase globale commuta col tick)* **si fa su tutti e sette.**
- **Il costo:** **per stato `3 x 100` tick** *(`R2` due volte, `R2-F`)* **`+ 2000`** *(`LIB1-C`)* **`+ 2`** *(`LIB1-U`)*: **`~16000` tick, `~30` minuti** *(`~0.1` s per tick, misurato con `L3`)*. **Il disco:** gli stati di `TBS` sono `~` qualche MB l'uno; `E:` ha `212` GB liberi, `C:` `22` GB.

### 15.3 PROGETTAZIONE *(le letture fissate qui, PRIMA dei numeri)*

- **Lo script nuovo `csv/solitone/libreria_stati.py`** *(non tocco `libreria.py`: i suoi referti restano rigirabili al loro commit)*: **per ciascuno dei sette tick:** `L0-S` *(lo stato della corsa ha gli `sha` del jsonl)*; **la scrittura** *(`E:\soliton_simulator\libreria\TBS_<tick>_completo.npz`: tutte le chiavi, `D`, `c_t`, il centro)*; **`R2-S`** *(il file riletto ridà gli `sha` del jsonl)*; **`R2`** *(due ripartenze dal file, `100` tick col ciclo della corsa: gli `sha` coincidono al bit)*; **`LIB1-0`** *(la ripartenza dal file ridà gli `sha` di `dopo_stato`)*; **`R2-F`** *(DEVE FALLIRE: `phi = c(t) F3` senza `D`)*; **`LIB1-U`/`LIB1-U-F`**; **`LIB1-C`** *(contro i centri registrati, `0.2` nodi, la soglia di Luca `00:32`)*. **Poi `LIB1-P` e `LIB1-P-F` sui sette.**
- **L'indice** `doc/referti_l2/libreria_solitoni/indice.json`: **l'oggetto ritagliato resta, marcato «ritagliato, non validato (Luca 19:37)»; si aggiunge `stati_completi`** *(file, byte, sha1, tick, `sha` dello stato, centro, `c_t`, il campione registrato)*.
- ### **COSA MI FA FERMARE:** **un DEVE che fallisce** *(`R2`, `LIB1-0`, `LIB1-P`, `LIB1-U`, `LIB1-C`, o un DEVE FALLIRE che passa)*: **committo lo stato e il fallimento, FERMO.** **In particolare `LIB1-0` sui sei tick nuovi**: se fallisce, la premessa «le chiavi di `z["st"]` bastano» e' sbagliata, e c'e' uno stato fuori da `st`.

### 15.4 ⭐ IL TAGLIO RIMANDATO AI CLUSTER: **IL CONTROLLO SULLE GRANDEZZE MEDIE, SCRITTO ADESSO** *(Luca `19:37` (3), prima di qualunque numero)*

- **Il confronto:** **l'oggetto RITAGLIATO incollato contro l'ORIGINALE**, **e la DISPERSIONE fra l'originale e `2`-`3` bracci del caos** *(semi diversi, la perturbazione della stessa norma del pezzo tolto)*.
- **Le grandezze** *(Luca)*: **il raggio `w`; la massa del cuore; il periodo e l'ampiezza del respiro; il tasso d'assorbimento al bordo.**
- **Il criterio** *(Luca)*: **per ciascuna grandezza, `|X(ritagliato) - X(originale)|` entro la dispersione fra l'originale e i bracci del caos.**
- ### ⚠ **I PUNTI CHE IL TESTO DI LUCA NON FISSA, e che vanno decisi PRIMA della corsa dei cluster** *(numeri e scelte: di Luca; le mie sono PROPOSTE, dichiarate)*:
  - **(p1) la finestra delle medie:** **proposta:** **dopo la decorrelazione** *(da `T0 + 550` unita', dove la differenza caotica arriva all'ordine `1`: la sez. `8.1`)*, **per una durata che contenga almeno `5` periodi del respiro**;
  - **(p2) «entro la dispersione»:** **proposta:** **`|X_rit - X_orig| <= max_i |X_caos_i - X_orig|`** *(il caso peggiore dei bracci del caos; con `3` semi)* ### **contro l'alternativa** **`<= 2 sigma`** *(con `3` semi la `sigma` e' mal stimata)*;
  - **(p3) i semi:** **`3`** *(`1`, `2`, `3`)*, **e la distribuzione della perturbazione** *(su tutto il toro o solo fuori da `R_t`: entrambe gia' misurate; proposta: **solo fuori da `R_t`**, dove agisce il taglio)*;
  - **(p4) il periodo e l'ampiezza del respiro:** **da quale serie** *(`w(t)` o la massa del cuore)* **e con quale stimatore** *(la frequenza dal picco della FFT, l'ampiezza dalla deviazione standard sulla finestra)*;
  - **(p5) il tasso d'assorbimento:** **la pendenza di `M_ass(t)` sulla finestra.**
- **Il DEVE FALLIRE, proposto:** **col `D` ritagliato** *(la via vecchia, `|D - D_t| / |D| = 3.5e-03` a `R_t 32`)* **almeno una grandezza fuori dalla dispersione.** ### ⚠ **Contro la propria premessa:** **non so se fallira'** *(sulle medie il `D` ritagliato potrebbe essere innocuo)*: **se passa, il DEVE FALLIRE non separa, e va detto.**
- **Il criterio di chiusura di questa sezione:** **(p1)-(p5) decisi da Luca e scritti qui, prima che si costruisca il primo cluster.**

### 15.5 TODO

1. `libreria_stati.py`, l'INVENTARIO col blob; commit e push **prima** di girarlo.
2. Il processo separato della libreria: `python csv/solitone/libreria_stati.py > doc/referti_l2/libreria_stati.txt`.
3. Il referto, l'indice, la relazione, la MAPPA, l'esito qui *(15.6)*; commit e push.
4. Poi il successivo in coda: **la cura del tetto di `Omega`** *(il task history `2026-11-07_cura_tetto_omega`)*.
