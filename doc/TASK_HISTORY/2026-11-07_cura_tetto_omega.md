# 2026-11-07 — LA CURA DELL'`assert` DEL TETTO DI `Omega` *(`energia_pesata.controlla_tetto`; Luca `2026-11-07` `10:06`, la decisione `1`)*: [[TETTO-OMEGA-SENZA-ARROTONDAMENTO]]

**Il mandato** *(nella sostanza)*: **l'`assert` che ha fermato IS3** *(`max_k(|Omega_k| - tetto_k) = 2.220e-16 > 0`, «Omega finale», dentro `tick.cs_al_centro`)* ### **e' un DIFETTO DEL NUCLEO DA CURARE**: **una tolleranza di arrotondamento sulla scala del tetto** *(qualche ulp, DERIVATA e dichiarata, come chiede l'errore `n.17` citato nel messaggio)*. **Un commit del nucleo a se'**, **la suite intera**, **un DEVE: tutte le corse e le carte vecchie identiche al bit.** **Si apre la voce del difetto.** ### **Quando:** **fra `C35-pi` e `C50-0`** *(la decisione `6`)*: ### **`energia_pesata` e' nel percorso della corsa** *(`motore._fase_vuoto` la importa a ogni tick)*, **e ogni pezzo e' un processo nuovo**: **il codice si tocca a `C35-pi` finita.**

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

1. **Il controllo:** `eccesso = max(|omega_k| - tetto_k)`, `assert eccesso <= 0.0` *(nessuna tolleranza)*. **Lo chiama `applica` due volte:** «Omega di partenza» e «Omega finale» *(sullo stato del punto medio)*.
2. **Il tetto e `Omega` sono calcolati da `termini_di_h` nello stesso passaggio, ma con DUE catene di operazioni diverse:**
   - `Omega_k = cs'_k (per_nodo_k + somma_h dw_h per_arco_a(h))`, con `per_nodo = -pi((nrm_psi - pu_psi) + (nrm_phi - pu_phi)) + eps h + N`, e `per_arco = -pi(arco_psi + arco_phi)`, `arco_phi = (|f0|^2 + |f1|^2 - 2 Re(f0* f1)) / 2`;
   - `tetto_k = |cs'_k| (tn_k + somma_h |dw_h| ta_a(h))`, con `tn = pi(nrm_psi + pu_psi + nrm_phi + pu_phi) + |eps| |h| + |N|`, e `ta = pi((nrm_a + 2 |incro|) / 2 + (|f0|^2 + |f1|^2 + 2 |f0| |f1|) / 2)`.
   ### **In aritmetica esatta `|Omega_k| <= tetto_k`** *(la disuguaglianza triangolare, termine per termine)*; ### **in virgola mobile le due catene arrotondano in modo diverso**, quindi **dove la disuguaglianza e' STRETTA o quasi** l'arrotondamento la puo' rompere di qualche ulp.
3. ### **Dove e' quasi stretta: sul vuoto `F3` disturbato** *(IS3, `AMP 1e-7`)*: **`psi = 0`**, quindi restano i termini di `phi`; **`arco_phi` = `ta` di `phi` quando le due estremita' dell'arco hanno fasi OPPOSTE** *(`Re(f0* f1) = -|f0| |f1|`)*, **e `nrm_phi - pu_phi` = `nrm_phi + pu_phi` quando `pu_phi = 0`.** ### **Se `F3` ha la somma nulla sul nodo e fasi opposte sugli archi, il tetto e' ESATTO, e un ulp lo supera.** **Da MISURARE, non da supporre** *(il passo `P1`)*.
4. ### **Le corse vecchie NON passano mai di qui:** **`applica` ritorna subito se `mot.cs is None or mot.lambda_c is None`** *(la forma spenta)*, ### **e TUTTE le corse dell'era `2` col solitone girano a forma spenta** *(`mot.lambda_c` `None`: `tick_con_cs` lo imposta, `percorri_tick` no)*. ### ⚠ **Quindi «le corse vecchie al bit» e' VERO PER COSTRUZIONE:** ### **un FALSO-UNO, se lo si presenta come un DEVE.** **Il DEVE che ha materia e' sui percorsi con `cs` acceso:** **i collaudi di `cs` della suite** *(`_collauda_cs.py`, `_collauda_cs_centro.py`, e gli altri che passano da `EP.applica`)* **e la carta IS3** *(`--cs-onde`)*.
5. ### **Una premessa che pesa su `TCS`, e che NON e' questa cura:** **[[PUNTO-FISSO-CS-SOLITONE]]** *(AGENDA dal `2026-10-27`)*: **il punto fisso di `cs` (`tick.tick_con_cs`) NON CONVERGE col solitone `S1`, gia' al tick `0`** *(`120` giri, lo scarto `0.217` e `0.265`)*. ### **`TCS` e' esattamente `tick_con_cs` col solitone:** **curare il tetto non basta per `TCS`.** **Lo segnalo a Luca: da riprendere prima di `TCS`.**
6. **Che cosa NON so:** **quanti ulp servono davvero** *(la derivazione dice un tetto superiore; la misura dice quanto vale dove alza)*; **se l'eccesso nasce in `Omega` o nel tetto.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO *(le letture si fissano QUI, prima dei numeri)*

- ### **LA FORMA DELLA CURA** *(la proposta)*: **`max_k(|Omega_k| - tetto_k - TOLL_k) <= 0`**, ### **`TOLL_k = c u tetto_k`**, **`u = eps / 2`** *(l'unita' di arrotondamento)* **e `c` CONTATO dal codice**: ### **`c = p + q`**, **`p` e `q` le profondita' delle due catene** *(il numero massimo di operazioni arrotondate fra un ingresso e il risultato, in `Omega` e nel tetto)*. **La giustificazione:** *(l'analisi dell'errore in avanti, `|fl(S) - S| <= gamma_m somma |x_i|`, `gamma_m = m u / (1 - m u)`)*: **`|fl(Omega) - Omega| <= gamma_p tetto`** e **`|fl(tetto) - tetto| <= gamma_q tetto`**, ### **quindi `|fl(Omega)| - fl(tetto) <= (gamma_p + gamma_q) tetto`**, **un tetto PER COSTRUZIONE** *(l'errore `n.17`)*. **`c` e' un intero contato, non scelto**: **va contato nel codice** *(le somme per nodo con `np.add.at` hanno profondita' pari al GRADO)*, e ### **il conto si scrive qui prima del codice** *(sez. `4`, a corsa chiusa)*.
- ### **Un'ALTERNATIVA da non prendere senza dirlo:** **calcolare `Omega` e il tetto con la STESSA catena** *(cambiare la formula del tetto)*: **cambia `tetto_omega`, quindi la SCALA del criterio d'arresto del punto fisso** *(`entro_tolleranza`, `8` ulp del tetto)*: ### **cambierebbe la dinamica con `cs` acceso.** **Scartata: la cura tocca solo il controllo, non la scala.**
- **I DEVE** *(a corsa chiusa, sul codice curato)*:
  - **`TT-M`** *(la misura, prima della cura)*: **sulla scena di IS3, al tick che alzava: `|Omega_k| - tetto_k` in unita' di `u tetto_k`, il nodo peggiore, e se l'eccesso nasce dove `pu_phi = 0` e le fasi sono opposte** *(la premessa `3`)*;
  - **`TT-D`** *(DEVE PASSARE)*: **l'eccesso misurato sta sotto `c u tetto_k`** *(la derivazione contiene la misura)*;
  - **`TT-F`** *(DEVE FALLIRE: il caso dell'errore `n.17`)*: **la prova di `csv/_tolleranza_omega.py`** *(il tetto vecchio, «messa APPOSTA», sulla scena di `C5` a `Lambda_c = 0.8`)* ### **deve continuare ad ALZARE col controllo curato**: **la tolleranza di qualche ulp non deve nascondere un tetto sbagliato di un fattore `3`.**
  - **`TT-0`** *(il braccio `0`)*: **la suite intera al bit** *(`primo_ordine/collauda.py`)*, **e i collaudi con `cs` acceso identici** *(un controllo piu' largo di prima ALZA in meno casi, non cambia un numero)*; **IS3 gira oltre l'`assert`.**
  - **le corse vecchie:** **dichiarate al bit PER COSTRUZIONE** *(la premessa `4`)*, **non come DEVE.**
- **Che cosa mi farebbe FERMARE:** **un eccesso misurato sopra la derivazione** *(allora la causa non e' l'arrotondamento: la formula del tetto non segue piu' quella di `omega()`, cioe' proprio l'errore `n.17`)*; **`TT-F` che non alza piu'**; **la suite che cambia un numero.**

## 3. TODO DEL NEXT STEP

1. **Questo task history, la voce [[TETTO-OMEGA-SENZA-ARROTONDAMENTO]], la sezione in `STATO_RUN.md`, la relazione: un commit** *(nessun file del nucleo toccato)*.
2. **A `C35-pi` finita** *(e dopo il referto della coppia, l'ordine di Luca)*: **`TT-M`** *(una misura in un file nuovo, fuori dal nucleo)*; **il conto di `c`** *(sez. `4`)*; **il commit del nucleo** *(`controlla_tetto`, il task history con LA STELLA POLARE, `REGISTRO_FISICA` se la legge cambia scheda -- non cambia: e' un controllo)*; **la suite intera** *(la riga `SUITE:`)*; **`TT-D`, `TT-F`, `TT-0`**; **la voce chiusa col commit.**
3. **Poi IS2 e IS3.**

## 4. LA STELLA POLARE *(le cinque domande; la cura non cambia la fisica, ma tocca il nucleo)*

1. **`A14`:** **nessuna legge nuova, nessun termine:** **un controllo dell'arrotondamento.**
2. **Il gradino di ROBUSTEZZA-FISICA:** **nessuno** *(la dinamica non cambia: un controllo che alzava a torto smette di alzare)*.
3. **Numeri aggiunti:** **`c`, un INTERO CONTATO** *(le profondita' delle due catene)*, **non tarato.**
4. **Verso EM-curvatura:** **sblocca `cs` sul vuoto** *(IS3, poi `TCS`)*, **il canale della gravita' nell'ipotesi del progetto.**
5. **Emergente o imposto:** **non e' fisica: e' la verifica di un tetto vero per costruzione.**

## 5. `TT-M`, L'ESITO *(`csv/solitone/_tetto_tt_m.py` `454712c5`, `doc/referti_l2/tetto_omega_tt_m.txt`; `energia_pesata.py` `cecd2c90`)*: **LA PREMESSA `3` CONFERMATA**

- **`16` chiamate di `controlla_tetto`** sulla scena di IS3; **l'`assert` alza alla `16`-esima** *(«Omega finale», `2.220e-16`, come nel referto di IS3)*; **una sola chiamata con eccesso positivo**, su **`2` nodi**.
- **Il nodo peggiore** *(`6481`)*: **`tetto_k = 8.011061e-01`** *(= il tetto massimo: il vuoto e' uniforme)*, ### **l'eccesso `2.497 u tetto_k`** *(`u = eps/2 = 1.110e-16`: un ulp del valore)*.
- ### **Dove nasce:** **`nrm_phi = 6` esatto, `pu_phi = 0`** *(la somma di `F3` sul nodo e' nulla)*, **`|per_nodo| / tn = 1` esatto**, ### **e su TUTTI E SEI gli archi del nodo il coseno della fase relativa e' `-1`** *(fasi opposte)*: **il tetto e' ESATTO** *(la disuguaglianza triangolare e' un'uguaglianza)*. ### **L'eccesso nasce nel termine d'ARCO:** **`|arco| / ta = 1.00000000000000022`** su due dei sei archi *(un ulp sopra)*. **`psi = 0`.**
- ### **Quindi:** **non e' l'errore `n.17`** *(una formula del tetto che non segue `omega()` darebbe un fattore, non un ulp)*: **e' arrotondamento dove il tetto e' esatto.**

## 6. IL CONTO DI `c` *(scritto PRIMA del codice; la sez. `2`)*

### 6.1 IL PRINCIPIO: **CONTANO SOLO LE OPERAZIONI DOPO LE FOGLIE COMUNI**

- **`Omega` e il tetto partono da FOGLIE CALCOLATE UNA VOLTA SOLA** *(gli stessi bit)*: `nrm_psi`, `pu_psi`, `nrm_phi`, `pu_phi` *(tutte `>= 0`)*, `h`, `N`, `eps`; sugli archi `nrm_a`, `incro`, `S = |f0|^2 + |f1|^2` *(la stessa espressione, nello stesso ordine, in `arco_phi` e in `ta`)*, `dw`; **`csp` e' calcolato due volte con gli stessi ingressi e le stesse operazioni: stessi bit.**
- ### **Sulle foglie comuni la disuguaglianza e' ESATTA in aritmetica reale:** **`|Omega_e| <= T_e`**, dove `Omega_e` e `T_e` sono le due espressioni valutate in aritmetica esatta SUI VALORI CALCOLATI delle foglie, e **`T_e` e' la somma dei valori assoluti dei termini di `Omega_e`**. Le due coppie non comuni: **`|Re(incro)| <= |incro|`** e **`|Re(conj f0 f1)| <= |f0| |f1|`**.
- **L'errore in avanti** *(Higham, `|fl(E) - E| <= gamma_m sum |x_i|`, `gamma_m = m u / (1 - m u)`, `m` la PROFONDITA' della catena)*: **`|fl(Omega)| <= |Omega_e| + gamma_p T_e`**, **`fl(T) >= (1 - gamma_q) T_e`** ### **=> `|fl(Omega)| - fl(T) <= (gamma_p + gamma_q) / (1 - gamma_q) fl(T)`**: **un tetto PER COSTRUZIONE, non un numero scelto.**

### 6.2 LE PROFONDITA', DAL CODICE *(`termini_di_h`, `omega`, `tetto_omega`; `d` il grado del nodo)*

- **`p`, la catena di `Omega`:** **il ramo d'arco e' il piu' lungo**: `R = Re(conj f0 f1)` *(`2` operazioni: due prodotti e una somma, profondita' `2`)*, `S - 2R` *(`3`; `2R` e `/2` esatti)*, `arco_psi + arco_phi` *(`4`)*, `x (-pi)` *(`5`)*, `x dw` *(`6`)*, **la somma sul nodo con `np.add.at`** *(sequenziale, `d - 1` somme che arrotondano: la prima e' `0 + x`)*, `+ per_nodo` *(`d + 6`)*, `x csp` *(`d + 7`)*. **Il ramo di nodo:** `5` operazioni, piu' corto. ### **`p = d + 7`.**
- **`q`, la catena del tetto:** **il ramo d'arco:** `|f0|`, `|f1|` *(`np.abs` di un complesso, `hypot`: ### **contato come `2`** -- un ulp, cioe' `<= 2u`, la garanzia della libm, **dichiarata**)*, `|f0| |f1|` *(`3`)*, `S + 2 |f0||f1|` *(`4`)*, `psi + phi` *(`5`)*, `x pi` *(`6`)*, `x |dw|` *(`7`)*, `np.add.at` *(`d - 1`)*, `+ tn` *(`d + 7`)*, `x |csp|` *(`d + 8`)*. ### **`q = d + 8`.**
- ### **Con `d = 6`** *(i triangoli, ogni nodo)*: **`p = 13`, `q = 14`, `c = p + q = 27`**: **la tolleranza `(gamma_13 + gamma_14) / (1 - gamma_14) tetto_k ~ 27 u tetto_k ~ 3.0e-15 tetto_k`.** **`TT-M` misura `2.497 u tetto_k`: la derivazione la contiene di un fattore `~11`.**

### 6.3 LA FORMA DELLA CURA, NEL CODICE

- **`controlla_tetto(omega_k, tetto_k, grado_max, dove)`** *(un argomento in piu', OBBLIGATORIO: niente `default`, `P-R1`)*: **`eccesso = max_k(|Omega_k| - tetto_k - TOLL_k)`**, **`TOLL_k = (gamma_p + gamma_q) / (1 - gamma_q) tetto_k`**, **`p = grado_max + 7`, `q = grado_max + 8`** *(una funzione `ulp_del_tetto(grado_max)` che restituisce il fattore, per poterla collaudare)*. **`applica` passa `int(mot.inc.grado.max())`.** ### **`tetto_omega` e `entro_tolleranza` NON cambiano** *(la scala del punto fisso resta)*.
- ### ⚠ **Due script vecchi chiamano `controlla_tetto` o lo sostituiscono** *(`csv/_diagnosi_d0.py`, `csv/_tolleranza_omega.py` `Q7`)*: **si rigirano al LORO commit** *(l'INVENTARIO)*; **`TT-F` copia la scala vecchia di `Q7`** *(dichiarato)* **con la firma nuova.**
- ### **Il collaudo nel nucleo** *(se c'e' un collaudo di `controlla_tetto` lo estendo; se no, uno nuovo in `collauda.py`)*: **un eccesso di `1` ulp su un tetto esatto PASSA; un fattore `1 + 1e-12` ALZA.**

### 6.4 I DEVE, FISSATI ADESSO *(la sez. `2`, coi numeri)*

- **`TT-D`** *(DEVE PASSARE)*: **sulla scena di IS3 l'eccesso massimo `2.497 u tetto_k` `<=` la tolleranza** *(`~27 u`)*, ### **e IS3 gira OLTRE l'`assert`** *(fin dove arriva: se si ferma per un'ALTRA ragione, lo dico)*.
- **`TT-F`** *(DEVE FALLIRE)*: **la scala vecchia di `7395cd9a`, messa APPOSTA, sulla scena di `C5` a `Lambda_c = 0.8`: il controllo curato ALZA**, **e l'eccesso stampato in unita' di `u tetto`** *(atteso `~10^15`: un fattore, non un ulp)*.
- **`TT-0`** *(il braccio `0`)*: **la suite intera** *(`primo_ordine/collauda.py`)* **prima e dopo, le uscite IDENTICHE tolte le righe dei tempi**; **le corse vecchie al bit PER COSTRUZIONE** *(la premessa `4`: non e' un DEVE)*.
- **Che cosa mi fa FERMARE:** **`TT-D` che non passa; `TT-F` che non alza; la suite che cambia una riga.**

## 7. LA CURA NEL NUCLEO *(`energia_pesata.py`; il collaudo `primo_ordine/_collauda_tetto.py`, `D2-T`)*

- **`ulp_del_tetto(grado_max)`** *(il fattore della sez. `6.1`, `p = d + 7`, `q = d + 8`: `27.000000 u` a `d = 6`)* e **`controlla_tetto(omega_k, tetto_k, grado_max, dove)`** *(l'argomento nuovo, obbligatorio; `applica` passa `int(mot.inc.grado.max())`)*. **`tetto_omega`, `entro_tolleranza`, `omega`: invariati.**
- **`D2-T` `7/7`:** il fattore `27.000000 u`; **un ulp sopra un tetto esatto NON alza**; **un fattore `1 + 1e-12` ALZA** *(DEVE FALLIRE)*; il confine a `0.5` e `2` volte la tolleranza; **il controllo vecchio sullo stesso caso alzava** *(il caso ha materia)*; il messaggio nomina la tolleranza e il grado. **Registrato in `collauda.py`, nella LISTA di `csv/_file_fisica.py` e nella mappa `primo_ordine/_mappa.yaml`.**
- ### ⚠ **Un mio errore, preso dalla suite:** **la prima suite dopo la cura dava `P-MOD` FALLITO** *(il collaudo nuovo sul disco e non in mappa, poi la responsabilita' oltre una riga)*: **curato prima del commit** *(`P-MOD` `10/10`, `0` errori)*.
- ### **`TT-0`, il braccio `0`:** **i tre collaudi con `cs` acceso** *(`_collauda_cs.py`, `_collauda_cs_centro.py`, `_collauda_cs_l1.py`)* **IDENTICI riga per riga prima e dopo** *(tolti i timbri)*; **la suite intera: prima `65/65`, dopo `66/66`; tolte le cifre dei tempi, l'unica differenza e' la riga di `D2-T`** *(e il conto)*. **Le corse vecchie: al bit PER COSTRUZIONE** *(la premessa `4`)*. **`TT-D` e `TT-F`: il commit dopo** *(lo script `_tetto_tt_d.py`, committato prima di girarlo)*.
