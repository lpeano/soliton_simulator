# LA LEGGE DELLA DURATA DEL SOLITONE: IL PROGETTO *(Luca `2026-11-09` `12:08`)* [[PIANO-2D-3D]]

> ### **SOLO PROGETTO:** **nessuna corsa nuova ora.** **Le sole misure sono L1, L2 e L4, sui dati GIA' raccolti, come prove corte, una alla volta, dopo la prova sul cuore delle `12:02`** *(e dopo (r-D5) sul laterale, che era gia' in coda: l'ordine nella relazione)*. **L3 e' solo progetto.** **Sul principale.**
> **Il bersaglio** *(Luca)*: **non una vita sola, ma DA CHE COSA DIPENDE.**

## 1. LE PREMESSE DAL CODICE *(cosa credo, e cosa NON so)*

- **Il «cuore» delle carte e' `M_dentro`**, **dal campione del bordo** *(`c["bordo"]["M_dentro"]`, `stazionarieta.serie_singolo`)*.
  - ### ⚠ **NON SO, e va letto dal codice prima di L1:** **se `M_dentro` e' la massa dentro il raggio del bordo** *(cioe' cuore PIU' alone)* **o del solo cuore.** **Il nome «cuore» viene dalle carte, non dalla definizione.** **Se e' «tutto cio' che non e' ancora assorbito», la sua perdita e' l'emissione, non il cuore che si svuota.**
- **I dati:** **`TB3` e `TBS` fino a `30000`** *(i jsonl, ogni `10` tick)*; **`C35-0` fino a `30000`**; **`C35-pi` in corsa.**
- **Gia' misurato** *(`f3dd15b1`)*: **il cuore NON e' stazionario a `30000` in tutte e due**; **il suo periodo e' `311` in `TB3`, nessuno in `TBS`.** **La vita estrapolata** *(versione `2`, `M_dentro / dM_ass/dt`)*: **`TB3` `4.1e7`, `TBS` `4.3e7` unita'** *(una estrapolazione lineare)*.

- ### **ANNOTAZIONE, dopo `f5e10f4b`** *(la prova del cuore, scritta prima di questo commit)*: **`M_dentro` vale `9.95e5`, quasi tutta la massa: e' la massa DENTRO IL BORDO, e la sua pendenza e' il ritmo di emissione.** **Il dubbio qui sopra e' confermato: L1 e L2 vogliono il cuore VERO** *(una massa dentro un raggio legato al solitone)*, **da leggere dal codice prima di scriverne lo script.**

## 2. IL PROGETTO

### L1. LA FORMA DEL DECADIMENTO *(una prova corta, sui dati che ci sono)*

- **I tre modelli, sul cuore di `TB3` e di `TBS` fino a `30000`, da `t 1000`** *(dopo la rampa, come la stazionarieta')*:
  - **esponenziale** `M = M0 e^{-t/tau}`;
  - **a potenza** `M = M0 (1 + t/t0)^{-a}`;
  - **lineare** `M = M0 - r t`.
- **Le oscillazioni si tolgono mediando su finestre di `P`** *(`311` per `TB3`; per `TBS`, che non ha un periodo, la STESSA finestra di `311`, dichiarata)*.
- ### **IL CRITERIO, scritto prima** *(mio, dichiarato)*: **l'AIC coi residui delle medie, e il numero EFFETTIVO di punti `N_eff = N / (2 tau_int)`** *(la `tau_int` di Sokal dei residui: i punti non sono indipendenti)*.
  - **Un modello VINCE se il suo AIC e' piu' basso degli altri due di almeno `10`** *(la soglia standard di Burnham e Anderson per «nessun sostegno» al perdente)*.
  - **Fra `2` e `10`: «preferito, non deciso».** **Sotto `2`: «nessuno vince».**
- **Le letture, scritte prima:** **(f1) vince l'esponenziale** *(una vita propria `tau`, come un decadimento)*; **(f2) vince la potenza** *(nessuna scala propria: rallenta invecchiando)*; **(f3) vince il lineare** *(un ritmo costante: la perdita non dipende da quanto resta)*; **(f4) nessuno vince: lo si scrive, col margine.**
- **E' la stessa forma in `TB3` e in `TBS`?** **Si stampa.**

### L2. LA VITA E LA SUA DEFINIZIONE *(una prova corta, dopo L1)*

- ### **LA DEFINIZIONE, scritta prima** *(mia, dichiarata; Luca ne proponeva due)*:
  - **la «fine» primaria: il cuore sotto META' del suo valore a `t 1000`** *(una vita media, che non dipende dalla frazione per l'esponenziale e si puo' confrontare fra i modelli)*;
  - **la seconda, stampata accanto: il cuore che non si distingue piu' dall'alone** *(il cuore uguale all'alone entro il suo errore)*.
- **La vita estrapolata col modello che vince L1** *(se nessuno vince: con tutti e tre, e la dispersione e' l'errore di modello)*, **con l'errore dei parametri** *(dalla matrice di covarianza del fit, con `N_eff`)*, **per `TB3` e `TBS`.**
- ### ⚠ **E' UNA ESTRAPOLAZIONE** *(sempre scritta cosi')*: **se la vita e' `~1e7`, e' `300` volte oltre la finestra osservata.**

### L3. LA DIPENDENZA DALLA MASSA *(SOLO PROGETTO DELLE CORSE: nessuna corsa)*

- **`3` o `4` solitoni di massa diversa, con le leggi di oggi:** **la stessa ricetta di `TBS`, con un'AMPIEZZA o un RAGGIO diverso.**
  - ### **Da leggere dal codice prima di proporre i numeri** *(non lo so oggi)*: **dove la ricetta di `TBS` fissa l'ampiezza e il raggio** *(`_vuoto_vivo_B.CORSE`, la larghezza di `rec`, `partenza`)*, **e se una massa diversa nasce con le stesse leggi o chiede un parametro nuovo** *(`A1`: se chiede un numero scelto a mano, FERMO)*.
- **La durata di ogni corsa e il tempo macchina:** **dai tempi dei pezzi di `TBS`** *(i jsonl)*, **scalati col numero di nodi.**
- ### **LA PREVISIONE:** **la vita come potenza della massa, `tau ~ M^b`; `b` e' il numero da trovare.**

### L4. LA DIPENDENZA DALLA FASE NELLE COPPIE *(una prova corta, dopo L2)*

- **Il ritmo di perdita del cuore di CIASCUN solitone:** **nella coppia in fase** *(`C35-0`, `30000`)*, **in opposizione** *(`C35-pi`, fin dove c'e')* **e da solo** *(`TBS`)*, **sulle STESSE finestre di tempo.**
  - ### **Da leggere dal codice prima** *(non lo so oggi)*: **se le carte della coppia danno il cuore di ciascun solitone separato** *(`carta_coppia`)*, **o solo il totale.**
- **Le letture, scritte prima:** **(m1) la molecola in fase vive PIU' a lungo del solitone da solo** *(il ritmo per solitone piu' basso di quello di `TBS` oltre `2` errori)*; **(m2) MENO** *(piu' alto)*; **(m3) UGUALE** *(entro `2` errori)*. **E lo stesso per l'opposizione.**

### L5. I PARALLELI *(come CONFRONTO, non come previsione)*

- **Il decadimento radioattivo:** **esponenziale**, una vita propria.
- **La regola di Sargent:** **`tau ~ E^-5`** *(il decadimento beta: la vita come potenza dell'energia liberata)*.
- **Le stelle:** **`tau ~ M^-2.5`** *(le piu' massicce bruciano prima)*.
- **Gli oscilloni:** **le vite lunghe e i decadimenti lenti dei solitoni di campo scalare**, **spesso non esponenziali.**

### L6. LE DOMANDE A LUCA *(il criterio di chiusura: la sua risposta, registrata qui)*

1. **Quante e quali corse nuove per L3?**
2. **Quando in coda?** *(dopo gli allungamenti: `C35-pi`, poi `S162`, poi `C50-0`)*

## 3. TODO

1. **Questo task history, committato.** **La riga nella MAPPA e nella voce `35`.**
2. **Dopo la prova sul cuore e (r-D5):** **L1** *(prima la lettura del codice su `M_dentro`)*, **L2, L4**, **ciascuno col suo script e il suo referto, committati prima di girarli.**

## 4. ANNOTAZIONE PRIMA DEL CODICE DI L1 *(`2026-11-10`)*: **IL CUORE VERO, DAL CODICE, E IL CRITERIO PRECISATO**

### 4.1 IL CUORE VERO

- **Letto dal codice:** **`csv/solitone/misure.campione`** *(chiamato dalla corsa a ogni campione, ogni `10` tick)* **da' `f_liscia`:**
  - **la frazione della massa `rho` entro `w_in` dal BARICENTRO del momento** *(che si muove col solitone)*,
  - **con una rampa larga un arco** *(`clip((w_in + h/2 - d)/h, 0, 1)`: senza i salti di un nodo che attraversa il bordo)*,
  - **`w_in` la larghezza iniziale** *(`DC.forma(z, w0)[0]`, `corsa_accensione`)*.
- ### **E' gia' il «cuore» della corsa:** **la tabella a blocchi di `corsa_accensione.tabella` lo stampa con quel nome.**
- **`f_liscia` e' una FRAZIONE di `M`, la massa sul toro** *(che cala con l'assorbimento al bordo)*. ### **Il cuore vero, in massa: `M_cuore(t) = f_liscia(t) · bordo.M(t)`**, **dagli stessi campioni** *(`campioni[i]["f_liscia"]` e `campioni[i]["bordo"]["M"]` dei jsonl)*.
- **`M_dentro`** *(la prova del cuore)* **resta quello che e': la massa dentro il bordo, cioe' tutto cio' che non e' ancora assorbito.**

### 4.2 IL CRITERIO, PRECISATO PRIMA DEI NUMERI *(la sez. `2`, L1, resta: qui solo cio' che mancava)*

- **I dati:** **`TB3` e `TBS`, i jsonl `doc/referti_l2/accensione_lenta/<nome>_<tick>.jsonl`** *(`20` pezzi ciascuno, `t` da `0` a `200000` tick, `s 0.15`: `30000` unita')*; **il tempo in unita' `t · s`.**
- **Le medie su finestre consecutive di `P = 311` unita'** *(per tutti e due, come scritto)*, **da `t 1000`:** **ogni finestra intera dentro i dati; il punto e' (la media del tempo, la media di `M_cuore`).**
- **I tre fit:** **minimi quadrati sulle medie** *(`scipy.optimize.curve_fit`; il lineare in forma chiusa)*; **`k` = `2` per l'esponenziale e il lineare, `3` per la potenza.**
- ### **`N_eff`:** **`tau_int` di Sokal** *(la finestra automatica: il primo `W` con `W >= 5 tau_int(W)`)* **dei residui di CIASCUN modello;** **`N_eff = N / (2 tau_int)`, e per il confronto si usa il PIU' PICCOLO dei tre** *(il piu' prudente: AIC piu' vicini)*.
- ### **`AIC_m = N_eff · ln(RSS_m / N) + 2 k_m`** *(l'AIC dei minimi quadrati, coi punti efficaci)*. **Le soglie `10` e `2` come scritte.**
- ### **IL CONTROLLO DI SCALA E I DEVE** *(per «una misura vuole un controllo di scala»)*:
  - **(L1-P) DEVE PASSARE:** **una serie SINTETICA esponenziale** *(sugli stessi tempi delle medie, `tau` = un terzo della finestra osservata, piu' i residui del fit esponenziale dei dati come rumore)*: **il criterio dichiara vincitore l'esponenziale;**
  - **(L1-F) DEVE FALLIRE:** **una serie sintetica LINEARE** *(stessa pendenza iniziale, stessi residui)*: **«vince l'esponenziale» deve fallire;**
  - **(L1-S, stampato)** **la sensibilita':** **lo scarto massimo fra il fit esponenziale e quello lineare dei dati, in unita' della deviazione dei residui:** **se e' sotto `1`, la finestra NON PUO' distinguere le forme, e lo si scrive accanto alla lettura.**
- **Lo script `csv/solitone/durata_l1.py`** *(nuovo, non nel percorso di S162)*, **il referto `doc/referti_l2/durata_l1.txt`.**
