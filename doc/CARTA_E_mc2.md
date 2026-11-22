# E = m c² SUL RETICOLO, LA LEGGE DELLA CADUTA, EÖTVÖS *(il mandato di Luca [M1446]; scritta PRIMA del codice di ogni corsia)* [[PROGETTO-MITOSI]]

> **Le regole:** nucleo intatto; file nuovi; carta e previsioni prima del codice; **POST-HOC dichiarato** *(la lettura del guardiano, «la materia va dove omega e' piu' alta», e' nata dopo [M0908] e [M1310-P])*; un commit e un push per pezzo; il tetto `10` processi con `1` filo, attese comprese; il freno `4 GB`; niente lanci con la CPU sopra il `90%`.

## 0. LE PREMESSE E LE SCELTE *(copiate in breve)*

- **[M1253-O]** *(1a63daf6)*: `(q - 1)/(N - 1)` = V1 `+0.238`, V2 `+0.999`, V3 `-0.761` *(= `-e0/omega`)*; **[M0908]** la caduta *(a in unita' di `c^2 |grad N|`, `c = 0.588 s`, positivo = VIA)*: V1 `+1.03`, V2 `+4.15`, V3 `-3.19`, V4 `+7.0`.
- **La lettura del guardiano:** `a/(d ln omega/dN) = 4.33, 4.15, 4.19, 3.98`; il moto del pacchetto `a = -grad omega/m*`, `m* = 1/(d2E/dk2) = 1/(-0.059) < 0`; `K_th = omega/(|m*| c^2) ~ 4.8`; in natura `-1`; `E^2 = Delta^2 + c^2 p^2` contando `E` dal centro del gap: `m* = Delta/c^2`.
- **S1** `c`: sempre `c_m = 0.588 s` e `c = s = 0.15`. **S2** `m*` dalla banda *(S)* e del solitone col calcio *(M)*; la legge usa quella del solitone. **S3** `omega` e `d omega/dN` misurati. **S4** tutti i centri dei gap, anche attraverso `+-pi`; nessun centro scelto dopo. **S5** Eötvös: la norma `x0.8` e `x1.2`, la stessa forma riscalata, la scena e il gradiente di [M0908], la forma V2. **S6** la coda *(sez. K)*.
- **I criteri:** **K1** S: B1 ridà `d2E/dk2 = -0.059` e `v_max = 0.588 s` entro l'`1%`; M: a `k = 0` fermo entro `3 sigma`; V e Q: a `N = 1` ridanno `omega(N1)` entro `1e-6`. **K2** `m*_sol` NEGATIVA *(se positiva la lettura cade: scritto per primo)*. **K3** le `K_i` uguali entro il `10%`, la media contro `K_th` entro il `20%`. **K4** «VALE» se `0.9 < R_E < 1.1` per ogni centro e ogni `c`; il segno. **K5** «VIOLA» se `eta > 3 sigma` e `eta > 1%`; `eta` contro la previsione entro `2 sigma`.
- **Le previsioni del guardiano** *(copiate)*: **P1** K1 passa; `m*_sol` negativa `90%`, `|m*_sol|` entro il `30%` di `16.9` `60%`. **P2** K3: `K_i` entro il `10%` `80%`; la media contro `K_th` entro il `20%` `60%`. **P3** K4: non VALE con `c = s` `75%`; con `c_m` `50%`. **P4** K5: VIOLA `65%`. **P5** V4: il rapporto fra `1.6` e `1.9` `75%`.

## K. LA CODA *(S6)* -- `doc/referti_l2/coda_m1446.py`

- ### ⚠ **UN CONFLITTO CON CLAUDE.md, DICHIARATO:** S6 chiede «controlla ogni `60 s`»; **CLAUDE.md par. 5: «Niente `Start-Sleep` ne' polling in run o script».** **La via che rispetta tutte e due:** un **dispatcher** che lancia le corse come processi figli e **ASPETTA in modo bloccante la fine di un figlio** *(`os.waitpid` via `subprocess`, nessun `sleep`)*; a ogni fine **ricontrolla** le condizioni e lancia la prossima. **Le condizioni:** i processi python totali **contati dalla riga di comando** *(Get-CimInstance)* `< 10` col dispatcher compreso; la memoria libera `> 4 GB` *(`GlobalMemoryStatusEx`)*; **la CPU: la lettura del carico mi e' negata** *(Get-Counter)*: **la stimo dal conto dei processi** *(un filo ciascuno su `12` logici: `< 10` processi = `< 83%`)*, dichiarato. **Se le condizioni non permettono di lanciare e nessun figlio gira** *(i posti li occupano corse non sue)*, **il dispatcher si ferma e lo scrive** *(non aspetta a vuoto: un'attesa a intervalli sarebbe polling)*; lo rilancio io.
- **La lista** in ordine di PRIORITA' *(a parita', l'ordine scritto da Luca)*: `1`: M k=0; M k=0.010 a1; V4 Nm; V4 Np; Q tenuta x0.8; Q tenuta x1.2 *(piu', mia, `V4 N1` per il caso noto di V, `250` tick: sez. V)*; `2`: M k=0.010 a2; M k=0.005 a1; M k=0.005 a2; `3`: Q Nm, Np, calcio, caduta per x0.8, poi per x1.2. **Le corsie aggiungono le corse** a `doc/referti_l2/coda_m1446.json` *(committato)*; **il dispatcher legge il file a ogni lancio**.
- **Ogni corsa ha la sua voce** APERTA/CHIUSO nel registro *(`_registro_corse.py apri`/`chiudi`: lo uso, non lo modifico)*. **Lo stato della coda** in `E:\soliton_simulator\controllo\M1446\coda_stato.json`, **copiato e committato da me a ogni mio passaggio** *(il dispatcher non committa: due commit insieme bloccano il lucchetto di git, dichiarato)*.

## S. LO SPETTRO *(corsia S)* -- `doc/referti_l2/spettro_gap.py`

- **Il codice:** ### ⚠ `s4_spettro` *(il referto `s4_spettro_materia_mrho*.txt`)* **e' lo spettro di STABILITA' di M-rho, non le bande.** **Il codice delle bande del repo e' la risposta lineare di T-L4b** *(`s5_caduta_segno.py`)*, **rifatta sulla scena di `chi` in `caduta_segno_v2.py`** *(f3281dfd)*: la corsia S parte da li' *(le stesse funzioni, file nuovo)*.
- **Le bande:** `A(k) = somma_x R(x) e^{-i k.d(x)}` *(`R` dai `12` impulsi `+-`, UNA volta)*, gli autovalori `e^{-i E}` su una griglia `48 x 48` della zona di Brillouin *(`k = (i B_0 + j B_1)/48`)*; **le bande** = i `12` autovalori ordinati; **i bordi** = `[min, max]` di ogni banda sul cerchio; **i gap** = il complemento dell'unione sul cerchio *(anche attraverso `+-pi`)*; **i centri** = i punti medi dei gap sul cerchio.
- **La banda e il `k` della materia:** `omega(N1)` *(l'orologio, 1a63daf6)* sta in una banda o in un gap? e `k = 0` *(il mattone fermo)*.
- **`d2E/dk2` e `v_max`** lungo i due assi *(`B_0`, `B_1`)*: `d2E/dk2` a `Gamma` della banda di `q` *(B1, la cima)* con `dk = 0.02` *(di T-L4b)*; **`v_max` = il massimo di `|dE/dk|`** sulla griglia lungo i due assi *(differenze centrate)*, in nodi per tick, contro `0.588 s`.
- **K1-S:** `d2E/dk2 = -0.059` e `v_max = 0.588 s` entro l'`1%`. **FERMATA S:** se non passa, FERMO solo la corsia S.
- **E_mc2** *(S-b)*: per ogni centro `E0`: `Delta_mat = |omega - E0|` contro `|m*_banda| c^2`, `m*_banda = 1/(d2E/dk2)`; `R_E = Delta_mat/(|m*_banda| c^2)` per `c_m` e `s`; **il segno** *(omega sotto il centro = particella; sopra = lacuna)*.

## M. LA MASSA DEL SOLITONE COL CALCIO *(corsia M)* -- `doc/referti_l2/massa_calcio.py`

- **La scena:** `caduta_libera.prepara` *(il mattone al centro di S162)*, `N = 1`, il tick V0 *(`tick_var` con `N = 1`)*; **il calcio:** `psi_h <- psi_h e^{i k . x_nodo}` *(la fase per nodo, `x` dal centro del mattone, l'immagine piu' vicina)*, **`k` lungo l'asse `a`** *(`a1` = `A1 = (1, 0)`, `a2` = `A2`)*; `1000` tick; **il baricentro di `rho` ogni `10` tick**.
- **La velocita':** il fit lineare del baricentro lungo l'asse su `k 200 ... 1000` *(il transitorio: i primi `200`, mio, dichiarato)*, con l'errore; **`m*_sol = k/v` col segno** *(`v` lungo `+k`: `m* > 0`; contro: `m* < 0`)*.
- **K1-M:** a `k = 0` la velocita' entro `3 sigma` da `0`. **K2:** `m*_sol` NEGATIVA; se positiva, scritto PER PRIMO.

## V. L'OROLOGIO V4 *(corsia V)* -- `doc/referti_l2/orologio_V4.py`

- **Le righe di `orologio_mattone_v2.py`** con le varianti `V4Nm` *(`0.9965`, `cs = s N`, la fase col segno `-1`)*, `V4Np` *(`1.0035`)* e `V4N1` *(`N = 1`: il caso noto)*. **K1-V:** ### ⚠ a `N = 1` V4 e' il tick V0 AL BIT *(`exp(0) = 1`)*: **il caso noto e' `V4N1` al bit con `N1` a `k 250`** *(`250` tick, non `1000`: basta il bit)*, e quindi `omega` identica.
- **Il rapporto:** `(q - 1)/(N - 1)` di V4 contro quello ricavato `1.76` *(V2 - V3, [M1427])*.

## Q. EÖTVÖS *(corsia Q)* -- `doc/referti_l2/eotvos.py`

- **I solitoni:** il mattone con `psi_h x sqrt(0.8)` e `x sqrt(1.2)` *(la norma `x0.8`, `x1.2`, la stessa forma; il vuoto e il campo come `caduta_libera.prepara`, `porto.campi` DOPO il riscalamento)*. **La tenuta** *(`N = 1`, `1000` tick, la fase a ogni tick come l'orologio)*: «regge» se il picco di `rho` a `k 1000` sta entro il `20%` di quello a `k 0` *(mio, dichiarato)* e la frequenza ha il residuo del fit sotto `1` rad. **Se uno non regge:** `x0.9`/`x1.1`, detto.
- **Per ciascuno che regge** *(priorita' `3`)*: `Nm`, `Np` *(la forma V2, `1000` tick: `d omega/dN`)*; il calcio `k = 0.010` `a1` *(`m*`)*; **la caduta in V2** *(la scena e il gradiente di [M0908], `2000` tick)*. **`eta = 2 (a_1 - a_2)/(a_1 + a_2)`** con l'errore; **la previsione di ciascuno:** `a_i = K (d ln omega_i/dN) c^2 |grad N|` *(la legge, sez. L)* con le sue `omega_i`, `m*_i`.
- **K1-Q:** a `N = 1` `omega(N1)` entro `1e-6` **solo per la norma `x1`** *(c'e' nella scena: e' `N1` stesso)*.

## L. LA LEGGE E LA SINTESI *(corsia L)* -- `doc/referti_l2/legge_caduta.py`

- **`K_i = (a_i / (c^2 |grad N|)) / (d ln omega/dN)_i`** per V1, V2, V3 subito *(`a` dai referti della caduta, `d ln omega/dN = (q - 1)/(N - 1)` dall'orologio: letti, non ricopiati)*, per `c_m` e `s`; V4 quando arriva la corsia V; **`K_th = omega/(|m*| c^2)`** con `m*_banda` *(S)* e `m*_sol` *(M)*. **K3.** Ogni aggiornamento e' un commit.
- **La sintesi** nella relazione quando S, M, V e Q hanno i referti.

## 1. LA VERSIONE NUOVA DEL MANDATO *(Luca, dopo le `15:15`; vale l'ultima; scritta PRIMA dei file nuovi)*

**Gia' fatti e NON rifatti** *(citati)*: la carta *(2a6f1415)*, la coda e le corse di priorita' `1` *(2899cdb6, 2d52a8b4: lanciate alle `15:06`)*, il codice di M *(`massa_calcio.py`)*, V *(`orologio_V4.py`)*, S-a *(`spettro_gap.py bande`)*, Q per la forma V2 *(`eotvos.py`)*, L per la parte assoluta *(`legge_caduta.py`)*. **Le differenze della versione nuova, e dove vanno:**

- **S4, gli zeri candidati `E0`, TUTTI, scritti qui prima dei numeri** *(il file nuovo `doc/referti_l2/emc2_v2.py`, che legge `spettro.npz` della corsia S e `orologio_zero.txt` di [M1427])*: **(a)** i centri di tutti i gap del cammino *(anche attraverso `+-pi`; dallo spettro)*; **(b)** i bordi della banda della materia: **la banda della materia = le due bande piu' alte a `Gamma`** *(la coppia di `q`, la cima `0.4767`)*, **i bordi = il minimo sulla griglia della penultima banda ordinata e il massimo dell'ultima** *(l'ordine per valore a ogni `k`: dichiarato, perche' le bande non sono seguite)*; **(c)** gli zeri `omega0` di V1, V2, V3, V4 di [M1427-R] *(cc5a336e, letti da `orologio_zero.txt`)*. **Per ciascuno** `Delta_mat = |omega - E0|` *(sul cerchio)* contro `|m*| c^2` con `m*_banda` e, quando c'e', `m*_sol`; `c_m` e `s`; `R_E`; sopra o sotto.
- **S5, Eötvös in V2 E in V3** *(il file nuovo `doc/referti_l2/eotvos_v2.py`: le righe di `eotvos.py` con la forma come argomento; la tenuta e il calcio restano quelli di `eotvos.py`, che non dipendono dalla forma)*: **in coda, priorita' `3`, per ciascun solitone che regge:** Nm, Np in V2 e in V3; il calcio `k 0.010 a1`; la caduta in V2 e in V3. **`eta` per forma**, e la previsione di ciascuno *(`a = -(d omega/dN) g_N/|m*|`)*.
- **L, le `K_i` anche DALLO ZERO di ciascuna forma** *(il file nuovo `doc/referti_l2/legge_caduta_v2.py`)*: **dallo zero `omega0_i = omega(1) - (d omega/dN)_i`**, `|omega - omega0_i| = |d omega/dN|_i` *(per costruzione)*, quindi `d ln|omega - omega0|/dN = 1` e **`K0_i = a_i/(c^2 |grad N|)` col segno**; contro **`K0_th = Delta_i/(|m*| c^2)`**, `Delta_i = |omega - omega0_i|`. **Lo scrivo prima:** con questa definizione `K0_i/K0_th` e' la stessa cosa del rapporto assoluto `K_i/K_th` moltiplicato per `omega/Delta_i`: **non e' una misura nuova, e' la stessa misura contata da un altro zero.**
- **V, lo zero di V4 contro `-e0`:** il referto `orologio_V4.txt` *(`orologio_V4.py lettura`, il file non si tocca)* da' il rapporto `(q - 1)/(N - 1)` contro `1.76`; **`omega0(V4) = omega(1) (1 - rapporto)` contro `-e0`** lo calcola `legge_caduta_v2.py` dal referto.
- **Le previsioni del guardiano nuove** *(copiate)*: **P4** K5: VIOLA in V2 `65%`; in V3 non lo so `50%`. **P6** K4 con `E0` = lo zero di V3 *(`1.103`)* e `c = s`: `R_E` fra `0.7` e `0.95` `60%`.
