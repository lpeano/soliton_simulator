# 2026-11-22 -- LA CADUTA LIBERA: DA CHE PARTE CADE UN MATTONE IN UN TEMPO CHE RALLENTA *(il mandato di Luca [M0908], `09:08`)* [[PROGETTO-MITOSI]]

> **Le regole di questo file:** cio' che dice Luca e' scritto come SUO; le letture del guardiano sono IPOTESI; **le premesse non si riscrivono quando si rivelano sbagliate: si annotano.** **Nessuna fisica cambia nelle corse in corso**; il nucleo non si tocca; i file sono nuovi.

## 1. [M0908-L] LA LETTURA DEL SEGNO *(scritta PRIMA del codice `doc/referti_l2/caduta_segno.py` e dei suoi numeri)*

### 1.1 Le premesse dal codice *(che cosa ho letto PRIMA di scrivere questa carta: lo dichiaro, perche' cercare la riga della carta dove la forma (a) fu decisa E' parte del mandato, e l'ho fatto prima)*

- **La fase (a) nel tick di `chi`** *(`chi_tick.fase_a`, usata da `chi_tick_v2.tick_chi_v2` mezza prima e mezza dopo il palindromo)*: `psi_h *= exp(0.5j e0 (N - 1))` per nodo, `N = exp(- kappa chi)`. **Nell'energia** *(`energia_chi`, `energia_chi_v2`)* il termine `Fa = - e0 somma (N - 1) rho`. **`e0 = 0.4767266286`** *(il meta dello stato `k 3000` di `chi-mattone-v2`; e' `eps_top` di T-L4b, `s5_coppia_lapse.eps_top_tl4b`)*.
- **La convenzione delle quasi-energie nel repo:** `csv/solitone/s5_caduta_segno.py` *(T-L4b)* scrive `E = -np.angle(lam)`, cioe' **gli autovalori del tick sono `e^{-i E}`**: `psi <- e^{-i H dtau} psi`. **Con questa convenzione la fase `e^{+i e0 (N - 1)}` per tick e' un potenziale `V_a = - e0 (N - 1)` per unita' di norma: POSITIVO dove `N < 1`.** E' coerente con `Fa`.
- **Dove fu decisa la forma (a)** *(`doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.22`, «LA FORMA (a) (del guardiano)»)*: **«l'energia della materia contata DALLA CIMA della sua banda»**, `E_N = somma N_k h_k - eps_top somma (N_k - 1) rho_k`, **col vincolo (iv): «il peso della materia, `h - eps_top rho`, e' `<= 0` nella banda: il segno dell'inerzia»**. La prova: **T-L4b** *(`f16cadf8`, il referto `doc/referti_l2/s5_caduta_segno.txt`)*. **Il passaggio a `chi`:** **D-CHI-FORMA-A = (fa1)** *(Luca `2026-11-21` `16:05`, `doc/TASK_HISTORY/2026-11-21_lapse_u.md`)*: «la forma (a) era accesa in tutte le corse G+U legate» *(`p6_bracci.tick_GU`, `eps_a = e0`)*.
- ### ⚠ **QUELLO CHE L'IPOTESI DEL MANDATO NON CONTIENE, ed e' gia' MISURATO:**
  - **T-L4** *(stesso referto)*: **la banda dei solitoni sta in CIMA**, `d2 eps/dk2 = -5.923e-02`: **una massa efficace NEGATIVA**. **Con la sola `cs = s N` il pacchetto va verso `N` piu' ALTO** *(`a = +2.19e-05` a `gamma +0.01`)*.
  - **T-L4b:** **con la forma (a) i pacchetti vanno verso `N` piu' BASSO**, `~670` volte piu' piano *(`s d eps/d cs = 0.475826` contro `eps_top = 0.476727`: la differenza `-9.0e-04`)*: **la forma (a) e' stata costruita per CANCELLARE quasi tutto l'effetto di `cs = s N` e lasciare il segno dell'inerzia.**
  - **G1** *(`f0affd34`, `doc/referti_l2/s5_caduta_solitone.txt`)*: **il solitone VERO, con la forma (a), va verso `N` piu' ALTO** *(`+5.14e-06` a `gamma 0.01`)*; il suo cuore sta `0.1493` SOPRA la cima della banda.
- **Quindi la mia premessa, PRIMA dei numeri:** **P-C6 e' vera alla lettera** *(l'energia del termine (a) e' positiva nel pozzo)*, **ma l'ipotesi della lente non regge per i pacchetti**: con la massa efficace negativa un potenziale piu' alto nel pozzo ATTIRA, e la camminata piu' lenta RESPINGE. **Il segno della caduta e' il PRODOTTO di due segni** *(l'energia e l'inerzia)*, non il primo da solo.

### 1.2 Che cosa NON so

- **Se la cima della banda nel vuoto della scena di `chi`** *(S162, il vuoto fresco MGU, il campo `U`, `g_e = 0`)* **e' la stessa di T-L4** *(un'altra scena, `L 81`)*: `e0` fu copiato da li'.
- **Se il mattone `L162_MGU_03000` si comporta come il pacchetto o come il solitone di G1.**
- **Il segno della frequenza del vuoto da UN tick:** una fase per tick e' definita a meno di `2 pi`; **a `~pi` per tick, `+omega` e `-(2 pi - omega)` danno lo stesso numero.** **Da un tick si legge solo `e^{-i omega}`, non il segno di `omega`:** lo scrivo prima, e la prova lo deve mostrare.

### 1.3 La progettazione *(`caduta_segno.py`, sola lettura, nessuna corsa lunga)*

1. **Le righe del codice**, stampate dai sorgenti *(non ricopiate)*: `chi_tick.fase_a`, la riga di `Fa`, la riga `E = -np.angle` di T-L4b, e le righe delle carte sopra *(cercate per testo, coi numeri di riga di OGGI)*.
2. **(a) Il vuoto, UN tick:** sulla scena di `chi` *(`triangolo_chi_v4.scena`, `mattone.vuoto_fresco`, `porto.campi`, `g_e = 0`)*, il tick U con `cs = s` *(`gravita_due_corpi.tick_U`)*; `e^{-i omega} = <phi_0, phi_1> / |.|`; **stampo `omega` e `omega - 2 pi`.**
3. **(b) L'onda piana, la risposta lineare di UN tick** *(il metodo di T-L4b, le stesse costanti importate da `s5_caduta_segno`: `A_IMP`, `DK`, `H_CS`)*: `12` impulsi `+-` su `psi` in un nodo; `A(k) = somma_x R(x) e^{-i k.d(x)}`; **la coppia piu' alta a `Gamma`, `E = -angle`**, `d2 E/dk2` lungo `B_0`; **la C-linearita'** *(la risposta a `i e_j` contro `i R e_j`)*.
4. **(c) Le varianti a `N` uniforme `1 - H_CS`**, la risposta di un tick per ciascuna: **V2** *(`cs = s N`)*, **V3** *(la sola fase)*, **V1** *(tutte e due)*, **V4** *(`cs = s N`, la fase col segno opposto)*: `dE_top/dN` di ognuna.
5. **La lettura, fissata QUI:** con `d2 E/dk2 < 0` un pacchetto va verso `E_top` piu' ALTO; **`dE_top/dN < 0` = verso `N` piu' basso** *(VERSO)*, `> 0` = VIA.

**Che cosa mi farebbe FERMARE:** la coppia piu' alta a `Gamma` lontana da `e0` piu' del `5%` *(il vuoto della scena di `chi` non e' quello di T-L4: `e0` andrebbe riletto, e lo decide Luca)*; la C-linearita' rotta sopra `1e-6` *(il metodo non vale)*.

**Le previsioni del guardiano, prima dei numeri:** `d2 E/dk2 < 0` *(85%)*; `dE/dN`: V2 `~ +0.476`, V3 `-0.477`, V1 `~ -1e-03`, V4 `~ +0.95` *(70%: il vuoto e' diverso, i numeri possono spostarsi)*.

### 1.4 TODO

- [ ] committare questa sezione e `caduta_segno.py` *(il codice prima della corsa)*;
- [ ] girarlo, il referto `doc/referti_l2/caduta_segno.txt`, commit e push col referto e la relazione;
- [ ] poi [M0908-C]: le previsioni di Luca P-C0 ... P-C6 riconciliate con T-L4/T-L4b/G1 **scritte accanto, non al posto**.

### 1.5 Annotazione dopo i numeri di [M0908-L] *(`f3281dfd`, `doc/referti_l2/caduta_segno_v2.txt`; le premesse sopra NON si riscrivono)*

- **Le previsioni della 1.3 tornano tutte:** `d2 E/dk2 = -5.923495e-02` *(la cima)*; la coppia piu' alta a `Gamma` `= e0` a `5.9e-11`; `dE_top/dN` V2 `+0.4758`, V3 `-0.4767`, V1 `-9.0e-04`, V4 `+0.9526`.
- **Una premessa del MANDATO cade:** il vuoto della scena di `chi` non gira di `pi` per tick ma di **`e^{+i pi s}`** *(`omega = -0.4712388980 = -pi s` nella convenzione `e^{-i omega}`)*.
- **Il primo giro** *(`2eb5d196`)* **cadde sul MIO assert** dei semiarchi *(ordinati per arco, non per nodo)*: `ac0ac357`, la cura nella v2.

## 2. [M0908-C] LA CADUTA LIBERA -- LA CARTA *(scritta PRIMA del codice `doc/referti_l2/caduta_libera.py` e dei numeri)*

### 2.1 Le premesse dal codice

- **La scena** *(le righe di `gravita_due_corpi.prepara_coppia` con UN francobollo)*: `triangolo_chi_v4.scena()` *(S162, `L 162`, `n 26244`)*, `g_e = 0` *(niente bordo)*, `mattone.vuoto_fresco` a `G2.T0`, **UN** francobollo `triangolo_video.francobollo_L162(0)` *(lo stampo `L162_MGU_03000`)* incollato sul nodo buono *(lo spostamento multiplo di `3`)* **piu' vicino al centro del toro** `(L/2, L/2)` nelle coordinate del codice; `porto.campi` *(`A = 0`, `E` da Gauss)*.
- **Il tick** *(`caduta_segno_v2.tick_var`, gia' committato e usato in [M0908-L])*: le righe di `chi_tick_v2.tick_chi_v2` **senza le righe di `chi` e `pi`** *(`chi` IMPOSTO e FERMO: nessuna forza, nessuna sorgente, `pi = 0`)*, `N` dato per nodo; `cs = s N` o `s`; la fase (a) col segno `+1`, `-1` o spenta. **Il contatore `Theta` non serve e non si tiene.** Gauss ogni `mattone.OGNI_GAUSS` *(come la corsa dei due mattoni)*.
- ### ⚠ **UNA PREMESSA DEL MANDATO NON SI PUO' FARE ALLA LETTERA, e lo scelgo io** *(da confermare da Luca)*: **su questo toro** *(`A1 = (1, 0)`, `A2 = (-1/2, sqrt(3)/2)`, i periodi `L A1` e `L A2`)* **`sin(2 pi x / L)` lungo `(1, 0)` NON e' una funzione sul toro**: lo spostamento `L A2` porta `x` in `x - L/2`, e il seno cambia segno. **Lungo `(1, 0)` il periodo piu' lungo possibile e' `L/2 = 81`** *(sul mattone, a `r 18` dallo zero, `cos(2 pi 18/81) = 0.17`: il gradiente NON e' quasi uniforme)*. **Lungo `(0, 1)` ci sta UN periodo intero, `L_y = L sqrt(3)/2 = 140.30`** *(una funzione della sola `m2`; a `r 18`, `cos = 0.69`; a `r 10`, `0.90`)*. **SCELGO `(0, 1)`:** `chi(y) = A sin(2 pi (y - y_c)/L_y)`, `y_c` la `y` del baricentro di `rho` del mattone a `k 0` *(lo zero esatto sotto il mattone)*. **Non e' una manopola:** `L_y` e' il periodo del toro, `y_c` la posizione del mattone. **Le due direzioni `(1, 0)` e `(0, 1)` non sono equivalenti sul reticolo** *(la prima lungo un legame, la seconda fra due)*: lo dichiaro; **se Luca vuole `(1, 0)` con `L/2`, e' un file nuovo.**
- **L'ampiezza `A`** *(il mandato)*: `|grad N|` al mattone **=** `|grad N|` a `r 20` nel mattone con `chi` *(lo stato `k 3000` di `chi-mattone-v2`, `E:\soliton_simulator\controllo\CHI\mattone_v2\stato_03000.npz`, lo sha1 controllato; `L 186`; il centro e `kappa` dal suo `meta`)*: **`G20 = |N(21) - N(19)| / 2`** dalle medie di `N = exp(-kappa chi)` sugli anelli larghi `1` attorno a `r 19, 20, 21`; **`A = G20 L_y / (2 pi kappa)`** *(al primo ordine `|dN/dy| = kappa A 2 pi / L_y` allo zero)*; `kappa = chi_parametri_v2.KAPPA`. **Il controllo:** il massimo di `chi` di quello stato a meno di `3` dal centro del `meta` *(se no la convenzione delle coordinate e' sbagliata: FERMO)*. **I valori si stampano.**
- **Le varianti** *(il mandato, copiato)*: **V0** `N = 1`; **V1** `cs = s N` e la fase (a); **V2** solo `cs = s N`; **V3** solo la fase (a) *(`cs = s`)*; **V4** `cs = s N` e la fase (a) col segno OPPOSTO; **V1m** come V1 con `chi -> -chi`. **`2000` tick ciascuna, gli stati ogni `250`.**
- **Il caso noto** *(il mandato)*: **V1 con `A = 0` AL BIT con V0** dopo `50` tick *(`psi_h`, `phi_h`, ogni chiave, `A`, `E`)*, **e V0 AL BIT con il tick U** *(`gravita_due_corpi.tick_U`, il riferimento dei due mattoni)*; **il deve-fallire:** V1 con `A` vero diversa da V0 dopo `50` tick.

### 2.2 Che cosa NON so

- **Se il vuoto si muove:** con `cs = s N` anche `phi` gira di `pi s N` per tick *(sez. 1.5)*, quindi **in V1, V2, V4 il vuoto si sfasa lungo `y`** *(`~ pi s |N - 1| 2000` radianti agli estremi)*. **E' fisica della variante, non un errore;** ma **non so quanto pesa sul mattone.** Lo leggero' nel film.
- **Se il mattone e' un pacchetto o il solitone di G1** *(sez. 1.5)*.
- **La deriva propria del mattone solo su S162 in `2000` tick** *(V0 la misura)*.

### 2.3 Le misure *(il mandato, [M0908-M])*

- **Il baricentro di `rho`** *(su tutto il toro, l'immagine piu' vicina al centro di `k 0`)* **e il nodo di `rho` massimo lisciato sui `7` nodi**, **la componente lungo `(0, 1)`**; **il fit `y(k) = y0 + v k + a k^2/2`** con l'errore standard di `a` *(la funzione di `gravita_due_corpi_misure.fit`)*; **`a - a(V0)`** con l'errore in quadratura.
- **Il verso:** **VERSO `N` piu' basso** *(`chi` piu' alto: con `A > 0`, `+y` in V1-V4, `-y` in V1m)* **= la caduta come in natura; VIA = la repulsione.** **Fuori dall'incertezza se `|a - a(V0)| > 2 sigma`** *(come [M0417])*.
- **Il confronto** *(ordine di grandezza, dichiarato)*: `|a|` contro `c^2 |dN/dy|` per `c = 0.588 s` e `c = s`.
- **Il film leggero:** `rho`, `Jx`, `Jy` per stato *(lo strumento del flusso di `gravita_due_corpi_misure`, con il `cs` e la fase della variante)*, `chi` una volta: `doc/referti_l2/film/caduta_<V>.npz`. **Il referto:** `doc/referti_l2/caduta_libera.txt`.

### 2.4 I criteri *(il mandato, copiati)*

- **Il caso noto V1(`A = 0`) = V0 al bit prima delle corse; V1 e V1m opposti entro l'incertezza** *(lo specchio)*.
- **Ogni numero dai referti, con l'incertezza del fit.**

### 2.5 Le previsioni

**Del guardiano** *(il mandato, copiate)*:
- **P-C0:** V0 non accelera (`a` entro `3 sigma` da `0`). `90%`.
- **P-C1:** V1 accelera VIA dal `N` piu' basso (repulsione), come le coppie. `65%`.
- **P-C2:** V2 (solo la camminata piu' lenta) accelera VERSO il `N` piu' basso. `65%`.
- **P-C3:** V3 (solo la fase (a)) accelera VIA. `70%`.
- **P-C4:** V4 (il segno opposto) accelera VERSO, piu' di V2. `60%`.
- **P-C5:** V1m opposto a V1. `90%`.
- **P-C6:** la lettura del segno [M0908-L] dice che la forma (a) ha energia positiva nel pozzo (il contrario della relativita'). `60%`. ### **-> VERA alla lettera** *(f3281dfd: `dE_top/dN = -e0` per V3)*.

**Mie, ACCANTO** *(Claude, dai numeri di [M0908-L] e di G1; non al posto di quelle del guardiano)*:
- **Se il mattone fosse un PACCHETTO:** V2 VIA, V3 VERSO, V1 VERSO `~530` volte piu' piano di V2, V4 VIA col doppio di V2 *(dal prodotto dei segni, sez. 1.5)*: **P-C2, P-C3, P-C4 false.**
- **Se e' come il solitone di G1** *(che con la forma (a) andava VIA, `+5.14e-06`, e senza la forma (a) `+5.87e-06` a `gamma +0.01`)*: **V1 VIA e V2 VIA con ampiezze vicine; la fase (a) conta poco sul mattone.**
- **La mia scommessa:** **V1 VIA** `60%`; **V2 VIA** `60%`; **V3 VERSO** `55%`; **V4 VIA** `60%`; **V1m opposto a V1** `90%`; **V0 dentro `3 sigma`** `70%` *(G1 falli' la caduta nulla a `N = 1`: `-1.36e-08`, `137` errori)*.

### 2.6 Che cosa mi farebbe FERMARE

- **il caso noto non al bit** *(non si corre)*; **il deve-fallire che passa**;
- **il massimo di `chi` dello stato di `chi-mattone-v2` lontano dal centro del suo `meta`** *(la convenzione delle coordinate)*;
- **meno di `4 GB` liberi o il tetto pieno** *(si aspetta, non si forza)*.

### 2.7 TODO

- [ ] committare questa sezione *([M0908-C])*;
- [ ] [M0908-K] `caduta_libera.py` *(la scena, `A`, il caso noto, la corsa di una variante)*, il caso noto girato e committato;
- [ ] [M0908-R] le sei corse *(nel tetto: al piu' `3` nuove insieme con `7` processi vivi; una alla volta se la CPU e' sopra il `90%`)*, le voci nel registro;
- [ ] [M0908-M] `caduta_libera_misure.py`, il referto, il film; la relazione nel ramo principale; **FERMO**.

## 3. [M2357-T4] LO SBLOCCO DEL CASO NOTO VERO *(la DECISIONE di Luca delle `09:08`; scritta PRIMA del codice `doc/referti_l2/t4_sblocco.py` e dei numeri)*

### 3.1 La decisione *(copiata)*

> «SBLOCCO DEL CASO NOTO VERO (DECISIONE DI LUCA, 09:08; l'errore n.215 del guardiano: «16 su 20» era troppo rigido con archi a pari merito): passa se la correlazione di rango fra |Θ| e la media nel tempo di |Δ(dtau·cs)| sui 1000 archi più maturi è ≥ 0,9 (misurato 0,9999), E i 20 archi scelti dalla media hanno |Θ| entro l'1% della soglia dei 20 più maturi. Il deve-fallire resta quello con il solo stato di k 3000. Se passa, T4 riprende.»

### 3.2 Le premesse dal codice

- **I dati e le righe** sono quelli di `notte_m0428_v3.t4` *(9f9f2e49, il referto `doc/referti_l2/triangolo_chi_t4_caso_noto.txt`)*: `CHI/mattone`, gli stati `250 ... 3000` *(`k 0` non salvato)*, `|Theta|` a `k 3000`, `d = dtau s exp(-kappa chi)` per stato, `|d_i - d_j|` per arco, la media sui `12` stati.
- ### ⚠ **«0,9999» del mandato e' il rango su TUTTI i `103788` archi**, non sui `1000` piu' maturi: **il criterio nuovo e' su un insieme diverso, e il numero puo' cambiare.** Lo dichiaro.
- **Le definizioni, fissate QUI:** **i `1000` piu' maturi** = i `1000` archi con `|Theta|` piu' alto a `k 3000`; **il rango** = Pearson fra i ranghi *(`argsort(argsort)`, come la v3)* ristretto a quei `1000`; **la soglia** `T20` = il `20`-esimo `|Theta|` piu' alto; **«entro l'`1%`»** = il minimo di `|Theta|` sui `20` archi con la media piu' alta *(su tutti gli archi)* `>= 0.99 T20`.
- **Il deve-fallire:** gli stessi due controlli con il solo stato di `k 3000` al posto della media: **almeno uno dei due deve cadere.**

### 3.3 Le previsioni *(mie, prima dei numeri)*

- **la media:** il rango sui `1000` `>= 0.9` `80%`; i `20` scelti entro l'`1%` `70%` *(la v3: `14` su `20` in comune, i primi archi quasi alla pari)*;
- **il solo `k 3000`:** cade `85%` *(la v3: `0` su `20` in comune)*.

### 3.4 Se passa

**T4 riprende:** il giro delle misure in corsa dei tronchi *(sez. `2` e `5` della carta del triangolo)* col caso noto NUOVO al posto del guscio `17-20` *(che la mia premessa sbagliata aveva fissato: 06a9fadb)*, in un file nuovo `triangolo_chi_misure_v2.py`, al `k 8000` *(il primo `k 3000 + 5000`)*. **Se non passa: FERMO su T4, coi numeri.**

**I processi:** il tetto e' pieno *(le tre catene della caduta, 10 python)*; **lo sblocco parte quando si libera un posto.**
