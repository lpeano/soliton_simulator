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

## 4. [M1052-S] DOVE NASCE LA SPINTA: L'IMPULSO DELLA MATERIA PER REGIONE *(la richiesta di Luca delle `10:40` e il mandato [M1052] delle `10:52`, fase 1; scritta PRIMA del codice `doc/referti_l2/caduta_libera_misure_v2.py` e dei numeri)*

### 4.1 La richiesta *(copiata)*

> «[M1052-S] Aggiungi alle misure [M0908-M], sola lettura: in V0, V1, V2, V3, V4 e V1m, la variazione dell'impulso della materia lungo il gradiente (dal flusso J o dalla derivata del momento di ρ), separata per anelli dal baricentro: nucleo (r < 15), guscio (15–21), bordo (21–25), fuori (> 25); a ogni stato salvato e cumulata. Il confronto già previsto fra baricentro e ρ massimo, letto come «nucleo contro tutto il mattone». Il caso noto: in V0 la spinta per regione è zero entro il rumore; la somma delle regioni = la spinta totale entro l'1%.» **IL BIVIO** *(scritto da Luca)*: «la spinta sta all'interfaccia» se in V1 il bordo + il guscio danno più del `50%` della spinta cumulata *(in valore assoluto)* con il `26%` della massa, oppure se il baricentro e il `rho` massimo accelerano con segni opposti.

### 4.2 Le premesse e le definizioni *(fissate QUI)*

- **Lo script delle misure di [M0908-M]** *(`caduta_libera_misure.py`, 54b1ab48)* **non e' ancora girato:** la v2 *(file nuovo)* e' la v1 riga per riga **piu' la spinta per regione**; la v1 non gira piu'.
- **L'impulso: dal flusso `J`** *(lo strumento gia' nella v1: `spostamento_trasporto` a `0.5` su una copia, il `cs` e la fase della variante; `Jy` per nodo)*. **`P_R(k) = somma_{v in R(k)} Jy(v)`**, le regioni per distanza dal baricentro di `rho` DELLO STATO *(non dal centro di `k 0`)*: **nucleo** `r < 15`, **guscio** `15 <= r < 21`, **bordo** `21 <= r < 25`, **fuori** `r >= 25`. **La variazione** `dP_R(k) = P_R(k) - P_R(k - 250)`; **la cumulata** `P_R(k) - P_R(0)`. Accanto, la massa di ogni regione.
- **Al netto di V0:** V0 parte dallo STESSO stato *(l'impronta del caso noto)*, quindi per V1-V4 e V1m **la spinta di `N`** in una regione = la cumulata della variante **meno** quella di V0 nella stessa regione. Stampo le due.
- ### ⚠ **Che cosa la misura NON separa:** **le regioni sono anelli fissi attorno al baricentro**, e la materia che attraversa un confine porta con se' il suo impulso: **la variazione dell'impulso di un anello e' la forza su quell'anello PIU' il flusso d'impulso attraverso i suoi confini.** Lo dichiaro: e' la quantita' che il mandato chiede, non la forza locale.
- **Il caso noto** *(il mandato)*: **(i)** in V0 la spinta per regione e' zero entro il rumore = per ogni regione la media delle `8` variazioni `dP_R` entro `3` errori standard *(`std/sqrt(8)`)* da `0`; **(ii)** la somma delle regioni = la spinta totale entro l'`1%`. ### ⚠ **(ii) e' vera PER COSTRUZIONE** *(le quattro regioni sono una partizione dei nodi)*: **controlla il codice, non la fisica** *(FALSO-UNO, dichiarato)*. **Accanto, un controllo che PUO' fallire** *(una lettura, non un DEVE)*: l'impulso totale `somma Jy` diviso la massa contro la velocita' del baricentro dalle differenze finite *(`(y(k+250) - y(k-250))/500`)*: devono avere lo stesso segno e lo stesso ordine di grandezza, se `J` misura davvero l'impulso.
- **Il bivio, in numeri:** in V1, al netto di V0, a `k 2000`: **`quota = (|C_guscio| + |C_bordo|) / (|C_nucleo| + |C_guscio| + |C_bordo| + |C_fuori|)`** *(«in valore assoluto»)*; **«interfaccia» se `quota > 0.5`**, oppure se `a - a(V0)` del baricentro e del `rho` massimo hanno segni opposti **e tutti e due fuori dall'incertezza** *(il mio: un segno dentro l'incertezza non e' un segno)*. Accanto, `|C_guscio + C_bordo| / |C_totale|` e la quota di massa del guscio e del bordo.

### 4.3 Le previsioni

- **Del guardiano** *(copiate)*: **P-S1:** V1 cade VERSO il `N` piu' basso, piano (come l'11/11). `70%`. **P-S2:** la spinta di V1 sta all'interfaccia (il bivio: bordo + guscio oltre il `50%`). `55%`.
- **Mie:** P-S1 `40%` *(il solitone di G1 andava VIA; la mia scommessa di cb23b30a: V1 VIA `60%`)*; P-S2 `50%`.

### 4.4 Annotazione dopo i numeri *(e72044df; le premesse sopra NON si riscrivono)*

- **Il controllo che PUO' fallire e' fallito:** `P/M` *(l'impulso del flusso `J` diviso la massa)* **ha il segno OPPOSTO alla velocita' del baricentro in TUTTE le varianti** *(V1 a `k 2000`: `+1.10e-03` contro `-2.37e-03`)*. **La ripartizione da `J` non e' la ripartizione della spinta che muove il baricentro:** **non la uso per il bivio.**

### 4.5 La ripartizione dal MOMENTO di `rho` *(l'altra via del mandato; scritta PRIMA del codice `doc/referti_l2/caduta_regioni_momento.py` e dei numeri)*

- **Per stato e per regione** *(gli stessi anelli dal baricentro dello stato)*: **`m_R(k) = somma_{v in R(k)} rho_v y_v`** *(`y` dal centro del `meta` di `k 0`, `rho` dal film di [M0908-M], lo sha1 stampato)*; **il fit `m_R(k) = m0 + v k + a_R k^2/2`** *(`gravita_due_corpi_misure.fit`)*; **al netto di V0**; la quota `(|a_guscio| + |a_bordo|)/somma |a_R|` **e il bivio di Luca con questa quota.**
- ### ⚠ **Che cosa NON separa, come prima:** la materia che passa un confine porta il suo momento; **e `somma_R a_R = M a_bari` PER COSTRUZIONE** *(un controllo del codice, dichiarato; `M` cambia poco: lo stampo)*. **Accanto:** lo stesso con le regioni FISSE ai nodi di `k 0` *(gli anelli attorno al baricentro di `k 0`)*: se le due quote dicono cose diverse, il passaggio di materia fra gli anelli conta.

## 5. [M1253-C] IL MATTONE E' UNA BOLLA? IL GALLEGGIAMENTO E L'OROLOGIO-MATTONE *(la richiesta di Luca delle `12:53`; scritta PRIMA del codice e dei numeri)*

### 5.1 La richiesta *(in breve; il testo intero nella relazione del ramo principale)*

- **L'idea di Luca:** il mattone, in cima alla banda, potrebbe essere una LACUNA nel vuoto pieno, o una BOLLA che sale perche' il mezzo attorno cade. **Due prove:** (1) mentre il mattone va via, il vuoto attorno cade verso il `N` piu' basso? (2) un orologio fatto di mattone, nel tempo piu' lento, batte piu' piano *(come in natura)* o piu' veloce?
- **[M1253-G] il galleggiamento** *(sola lettura, V0-V4 e V1m, al netto di V0)*: (a) il baricentro lungo `y` del disturbo del vuoto *(pesato con `|phi - phi0|^2`)* e dell'energia del vuoto per nodo, nel disco `r < 40` e nell'anello `25-40`; (b) l'impulso della materia e del vuoto, separati, e la somma; (c) **GALLEGGIA** se in V1 il baricentro del vuoto va VERSO il `N` piu' basso fuori dall'incertezza mentre il mattone va VIA, **e** se i due impulsi hanno segni opposti. **Il caso noto:** in V0 il baricentro del vuoto fermo entro `3 sigma`; il vuoto F3 PURO col gradiente di V1, `500` tick: come cade il vuoto da solo; **il deve-fallire:** il vuoto puro a `N = 1` non si muove.
- **[M1253-O] l'orologio-mattone:** il mattone fermo in `N` uniforme `0.9965` e `1.0035` *(cs `= s N` e la forma (a), come V1)*, piu' `N = 1`; `1000` tick; **la frequenza propria** = la velocita' di rotazione della fase media di `psi` pesata con `rho` entro `r 15`; il rapporto con `N = 1`. **COME IN NATURA** se il rapporto vale `~N`; **AL CONTRARIO** se `~1/N` o cresce dove `N` cala. In piu' V2 e V3 a `N = 0.9965`. **Il caso noto:** a `N = 1` al bit con V0; l'energia del cuore dalla frequenza `= e0 + 0.1493` *(G1)* entro l'`1%`.
- **Le previsioni del guardiano** *(copiate)*: **P-B1:** in V1 il disturbo del vuoto va VERSO il `N` piu' basso mentre il mattone va via (galleggia). `45%`. **P-B2:** la somma degli impulsi della materia e del vuoto si conserva meglio di quello della sola materia. `50%`. **P-B3:** l'orologio-mattone batte come `N`, cioe' piu' piano nel tempo lento, come in natura (con `cs = s N` tutte le frequenze scalano con `N`). `70%`. **P-B4:** se P-B3 e' vera, la lettura «lacuna» con la sorgente rovesciata NON regge da sola; se P-B3 e' falsa, la lettura «lacuna» diventa coerente e va messa sulla carta come candidata. `60%` che P-B3 vera.

### 5.2 Le premesse dal codice e le definizioni *(fissate QUI)*

- ### ⚠ **Il vuoto si sfasa tutto insieme dove `N` non e' `1`** *(l'anemometro, a8c8760a)*: con `cs = s N` `phi` gira di `pi s N` per tick, e `|phi - phi0|` con `phi0 = c(t0 + k) F3` cresce col tempo dove `|N - 1|` e' grande. **Nella caduta `N - 1 ~ -kappa A sin(2 pi (y - y_c)/L_y)` e' DISPARI in `y` attorno al mattone, ma `|phi - phi0|^2` e' PARI:** lo sfasamento da solo non sposta il baricentro del disturbo. **Pero' lo sporca.** **Quindi il riferimento giusto e' la corsa del vuoto PURO col gradiente:** **(a) si legge AL NETTO DEL VUOTO PURO** *(lo stesso tick, lo stesso `N`, senza mattone: la parte del disturbo che non viene dal mattone)*, **oltre che al netto di V0.** **Il vuoto puro col gradiente si corre solo per V1** *(il mandato)*: per V2 e V4, che hanno lo stesso `cs`, vale lo stesso vuoto *(la fase (a) agisce solo su `psi`, e sul vuoto puro `psi = 0`)*; per V3 *(`cs = s`)* il vuoto puro e' quello di `N = 1`. **Lo dichiaro.**
- **Il baricentro del disturbo:** `y_D = somma w y / somma w`, `w = |phi - phi0|^2` per nodo *(`porto.dphi_nodi` al quadrato)*, `y` dal baricentro del mattone A `k 0` *(fisso: se il centro seguisse il mattone, il baricentro del vuoto lo seguirebbe per costruzione)*, nel disco `r < 40` e nell'anello `25 <= r < 40` *(gli stessi raggi dal centro fisso)*; il fit `y0 + v k + a k^2/2`.
- **L'energia del vuoto per nodo** *(«i termini di H del solo `phi`, con lo zero dichiarato»)*: `_libro_dei_conti.conti_per_nodo(...)["tot"]` **su una COPIA dello stato con `psi = 0`** *(cosi' restano solo i termini di `phi`: niente materia, niente accoppiamento)*, **meno lo stesso conto sul vuoto F3 puro allo stesso tick** *(lo zero: il vuoto indisturbato vale `0`)*; il baricentro con peso `|E_v|` e, accanto, con segno.
- **L'impulso:** **della materia** `P_m = somma Jy` *(lo strumento di [M0908-M])* ### ⚠ **col difetto gia' trovato: `P_m/M` ha il segno OPPOSTO alla velocita' del baricentro** *(e72044df)*; **accanto, `M v_bari`** *(dalle differenze finite)*; **del vuoto** `P_v = somma J_phi_y` con `J_phi` dal gemello dello strumento: l'operatore del motore **`spostamento_scalare`** *(quello del termine CAMM-SPOSTAMENTO-VUOTO, `AMBITO phi_h`, senza `U`)* a `0.5` su una copia, `J_phi` = la variazione di `|phi_h|^2` sul primo semiarco di ogni arco, poi per nodo coi vettori dei tre archi **come per la materia** *(dichiarato: un gemello, non uno strumento collaudato)*. **«Si conserva meglio»:** la deviazione standard delle variazioni fra stati di `P_m + P_v` contro quella di `P_m`.
- **L'orologio:** la fase `Phi(k) = arg somma_{r < 15} rho psi_c` *(`psi_c` la componente del primo semiarco con la norma piu' grande, `girandola_chi_v3.fase_dei_nodi`; il centro fisso a `k 0`)* **A OGNI TICK** *(gli stati ogni `250` non bastano: la fase gira di `~0.6` per tick)*, srotolata; **`omega = -dPhi/dk`** *(la convenzione `e^{-i E}` di [M0908-L])* dal fit lineare su `k 100 ... 1000` *(i primi `100` tick fuori: il mattone si assesta; dichiarato)*, con l'errore del fit. **Le corse** *(file nuovo `doc/referti_l2/orologio_mattone.py`, il tick `caduta_segno_v2.tick_var`)*: `N1` *(`N = 1`)*, `N-` *(`0.9965`)*, `N+` *(`1.0035`)*, `N-V2`, `N-V3`; `1000` tick; **i valori `0.9965` e `1.0035` sono del mandato** *(il minimo e il massimo di `N` della caduta, arrotondati)*. **Il caso noto «al bit con V0»:** lo stato di `N1` a `k 250, 500, 750, 1000` = quello di `caduta/V0` agli stessi `k`. **Il caso noto «e0 + 0.1493 entro l'1%»:** `omega(N1)` contro `0.4767266286 + 0.1493 = 0.6260`.
- **La lettura dell'orologio, in numeri:** `q = omega(N)/omega(1)`; **COME IN NATURA** se `q - 1` ha il segno di `N - 1` e `|q - 1|` e' entro il `30%` di `|N - 1|`; **AL CONTRARIO** se `q - 1` ha il segno opposto. *(Il `30%` e' mio: una soglia per dire «circa `N`». Lo stampo comunque.)*

### 5.3 Che cosa NON so

- Se `porto.dphi_nodi` vede il disturbo del mattone sopra lo sfasamento globale *(il vuoto puro col gradiente lo dira')*.
- Se la frequenza della fase media e' una frequenza sola *(il mattone respira: il residuo del fit lineare lo dira')*.

### 5.4 Le previsioni mie

- P-B1 `35%`; P-B2 `40%`; **P-B3 `75%`** *(con `cs = s N` la camminata scala col tempo; la forma (a) aggiunge `-e0 (N - 1)`, che va CONTRO: la somma per il mattone, dalla caduta, e' `V2/V3 = -1.30`, quindi la camminata dovrebbe vincere)*.

### 5.5 TODO

- [ ] committare questa sezione; [M1253-G] `doc/referti_l2/galleggiamento.py` *(il vuoto puro col gradiente e a `N = 1`, `500` tick, poi la lettura)*; [M1253-O] `doc/referti_l2/orologio_mattone.py` *(cinque corse da `1000` tick, quando la CPU lo consente)*; i referti; la relazione nel ramo principale; **FERMO**.

## 6. [M1310-P] IL POUND-REBKA DI G+U *(il mandato di Luca [M1310] delle `13:10`, fase B; scritta PRIMA del codice `doc/referti_l2/pound_rebka_GU.py` e dei numeri)*

### 6.1 La richiesta *(copiata)*

> «[M1310-P] Sugli stati salvati delle coppie del 14–16/11 senza lapse (B2 in fase a 35, coppia-d50, coppia-d65, e B2-pi in antifase): la frequenza propria di ciascun mattone (la rotazione della fase media di ψ pesata con ρ entro r 15, fra stati successivi) in funzione della distanza dall'altro. La domanda: G+U rallentano l'orologio di un mattone quando l'altro è vicino, nello stesso verso in cui lo attirano? IL CASO NOTO: il mattone da solo (lo stampo, stessi tick) ha frequenza costante entro il rumore.» **La previsione del guardiano** *(copiata)*: **P-O2:** nel Pound–Rebka di G+U l'orologio di un mattone rallenta quando l'altro (in fase) è più vicino. `50%`.

### 6.2 Le premesse dal codice

- **Gli stati** *(`E:\soliton_simulator\mattone\`, `mattone_coppia_L162.py` e `coppia_distanze.py`)*: `coppiaGU_L162` *(B2, `d 35`)*, `coppiaGUd50_L162`, `coppiaGUpi_L162` *(B2-pi)* a `k 500, 1000, 1500, 2000`; `coppiaGUd65_L162` a `k 500, 1000, 1500`, **sul toro di `L 243`** *(il nome dice `L162` perche' e' lo stampo)*. **Solo ogni `500` tick, e `k 0` non c'e'.** Le chiavi `psi_h`, `phi_h`, `rho`, `campo_A`, `campo_E`; **nessun `.sha1` accanto**: lo stampo al momento della lettura.
- ### ⚠ **LA FASE FRA DUE STATI A `500` TICK E' AMBIGUA:** il mattone gira di `~0.6` rad per tick, cioe' `~300` rad in `500` tick; la differenza di fase misurata e' nota **a meno di `2 pi`**, quindi la frequenza **a meno di `2 pi/500 = 0.01257` per tick**. **Si scioglie con una frequenza di riferimento** `omega_ref`, se la vera e' entro `+-0.0063` da essa: `omega = omega_ref + wrap(-dPhi - omega_ref 500)/500`. **`omega_ref` = la frequenza dell'orologio-mattone `N1`** *([M1253-O], il mattone da solo col tick V0, la fase a OGNI tick: nessuna ambiguita')*. ### **E' anche il caso noto del mandato** *(«il mattone da solo, stessi tick»)*, **con una differenza dichiarata:** **la scena non e' la stessa** *(l'orologio sta su S162 senza bordo; le coppie su `C35-pi` col bordo da `R_A 60`, d65 su `L 243`)*, **e il tick** *(`mattone_cottura.Corsa.passo` del mondo GU, contro `tick_U` dei due mattoni)* **lo do per uguale perche' Luca scrive «G+U senza lapse»: NON l'ho verificato al bit.** **Il controllo che PUO' fallire:** le frequenze sciolte delle due meta' di una coppia, e dei tre intervalli, devono stare entro `+-0.006` da `omega_ref` *(se no, l'ambiguita' non e' sciolta: FERMO su quel numero)*.
- **I due mattoni:** le due meta' divise dal piano per il punto medio fra i due massimi della materia, perpendicolare a `A1` *(la direzione delle coppie)*; **il centro di ognuno** = il baricentro di `rho` della sua meta'; **la fase** `Phi = arg somma_{r < 15} rho psi_c` *(`psi_c` la componente del primo semiarco con la norma piu' grande nel mattone, `girandola_chi_v3.fase_dei_nodi`; i semiarchi del toro di `243` con `girandola_chi_v3.toro_nodo`, controllati sulla forma di `psi_h`)*; **la distanza** fra i due baricentri.
- **La lettura** *(fissata qui)*: per ogni coppia e intervallo, `omega_A`, `omega_B`, la media, `omega - omega_ref`, e la distanza media; **«rallenta quando l'altro e' vicino»** se `omega - omega_ref` e' piu' NEGATIVO a `d 35` che a `d 50` e a `d 65` *(in fase)*, **oltre lo scarto fra le due meta'**; **«nello stesso verso in cui lo attirano»:** il segno di `d''` di ogni coppia dai referti del `14-16/11` *(B2 in fase attrae, B2-pi respinge: la premessa del mandato)*, confrontato col segno di `omega - omega_ref`.

- **La soglia del caso noto** *(mia, dichiarata)*: «frequenza costante entro il rumore» = **il residuo rms del fit lineare della fase di `N1` sotto `1` rad** su `900` tick *(una frequenza che deriva di `2e-3` in `900` tick darebbe un residuo di `~100` rad)*.

### 6.3 Le previsioni mie

- P-O2 `40%`; **il controllo dell'ambiguita' passa** `70%` *(le scene diverse possono spostare la frequenza di piu' di `0.006`)*.

## 7. [M1417] L'OROLOGIO RELATIVO AL VUOTO *(la decisione di Luca, dopo le `14:01`; scritta PRIMA del codice `doc/referti_l2/orologio_relativo.py` e dei numeri)*

> **Dichiarato da Luca:** la lettura e' **POST-HOC** *(l'idea e' nata dopo aver visto il segno di [M1310-P])*.

### 7.1 Le scelte e i criteri *(copiati)*

- **S1:** sola lettura degli stati gia' usati da `pound_rebka_GU.py` *(le stesse coppie, gli stessi `k 500-2000`)* e dell'orologio N1; nessuna corsa, nessun file del nucleo.
- **S2:** `omega_phi` = il ritmo della fase di `phi - phi0` *(o di `phi`, quello che la carta giustifica)*, la media pesata con lo stesso peso di `psi` entro `r 15` da ciascun mattone, e nel vuoto lontano *(`r > 40` da tutti e due)*.
- **S3:** `omega_rel = omega_phi(locale) - omega_psi`; `Delta omega_rel` rispetto alla base *(d 50 e d 66)*, per coppia.
- **K1:** l'orologio N1 da solo, `omega_rel` costante *(il residuo del fit come in [M1310-P])*. **K2:** `omega_phi` nel vuoto lontano uguale fra le coppie entro `1e-5`; se no la scena non e' confrontabile: dirlo e fermarsi. **K3:** il segno di `Delta omega_rel` per la coppia che si attrae: NEGATIVO = come la natura; POSITIVO = come prima. E il segno di `omega_phi - omega_psi` di base.
- **Le previsioni del guardiano** *(copiate)*: **P1** K1 e K2 passano. **P2** il segno di `omega_phi - omega_psi` di base: `50%`. **P3** `omega_phi` locale vicino ai mattoni cambia fra la coppia a `d 34` e la base meno di `|Delta omega_psi| = 1.26e-4`.

### 7.2 Le definizioni *(fissate QUI)*

- **Quale fase:** **la fase di `phi` RISPETTO A `phi0`**, `theta_v = arg somma_v w_v somma_{h in v} conj(phi0_h) phi_h`, **e poi `omega_phi = omega_F3 + omega_v`**, con `omega_v = -d theta_v/dk` e **`omega_F3` il ritmo del vuoto indisturbato** *(`-arg c(t + 1)/c(t)`, srotolato tick per tick sull'intervallo, dalla tabella `bordo.c_di` della scena)*. **Il perche':** `phi` da solo gira di `~0.47` rad per tick *(`pi s`)*, quindi fra due stati a `500` tick ha la stessa ambiguita' di `psi`; **`phi - phi0` gira lento** *(`|omega_v| << 2 pi/500`)*, e l'ambiguita' non c'e': la parte veloce `omega_F3` e' nota esattamente dalla tabella. **I due numeri sono la stessa cosa** *(`omega_phi`)*, solo misurati senza ambiguita'.
- **`phi0(t) = c(t) F3`** con la tabella e il vuoto F3 della scena delle coppie *(`mattone.scena(CORSA_C, T_C)` di `mattone_coppia_L162`; per d 65 `convergenza.scena_L(243, 100.5)`, come `coppia_distanze`)*, `t` dal `meta` dello stato; per N1 la scena di `chi` *(`triangolo_chi_v4.scena`)*, `t = G2.T0 + k`.
- **I pesi:** **locale** = `rho` entro `r 15` dal baricentro di ciascun mattone *(lo stesso di `psi` in [M1310-P])*; **lontano** = `1` per nodo dove `r > 40` da tutti e due i baricentri.
- **`omega_psi`:** come `pound_rebka_GU.py` *(la fase di `psi` sciolta con `omega_ref` dell'orologio N1)*.
- **`omega_v`:** `-wrap(theta_v(k2) - theta_v(k1))/(k2 - k1)`; **il controllo:** `|wrap(.)| < pi/2` *(se no, anche `omega_v` e' ambiguo)*.
- **K1, il criterio numerico:** la fase relativa `Psi(k) = theta_v(k) + somma omega_F3 - Phi_psi(k)` di N1 *(gli stati `250 ... 1000`, `psi` dalla fase di ogni tick)*, **il residuo del fit lineare sotto `1` rad** *(come [M1310-P])*.
- **La base** = la media di d 50 e d 66 *(in fase, lontane)*.
