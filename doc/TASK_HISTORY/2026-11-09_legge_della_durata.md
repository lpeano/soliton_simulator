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

## 5. L1, L'ESITO: **IL CONTROLLO POSITIVO L1-P FALLISCE: FERMO SU L1** *(la corsa a `ac8d6755`, dalle `01:24:56` alle `01:25:01` del `2026-11-10`; il referto `doc/referti_l2/durata_l1.txt`)*

- **I dati:** **`TB3` e `TBS`, `20001` campioni ciascuno** *(da `0` a `30000`)*, **`93` finestre di `311`.** **`M_cuore`:** **`TB3` da `5.916360e+05` a `3.367760e+05`; `TBS` da `5.917844e+05` a `3.293141e+05`.**
- **I fit, `TB3`:**
  - esponenziale: `M0 397450`, `tau 141109`; AIC `+199.897`;
  - potenza: `1.28568e+06`, `t0 0.00180223`, `a 0.0815467`; AIC `+175.826`;
  - lineare: `395168`, la pendenza `2.4791`; AIC `+200.758`;
  - `N_eff 10.6`; il margine `24.071`: «vince potenza».
- **I fit, `TBS`:**
  - esponenziale: `394793`, `142727`; AIC `+184.920`;
  - potenza: `1.20194e+06`, `0.00348523`, `0.0810101`; AIC `+169.661`;
  - lineare: `392540`, `2.43575`; AIC `+185.627`;
  - `N_eff 9.8`; il margine `15.259`: «vince potenza».
- ### **L1-P DEVE PASSARE e FALLISCE:** **sulla sintetica esponenziale** *(`tau 9537.5`, i residui di `TBS` come rumore)* **il criterio da' «potenza preferito, non deciso»** *(il margine `7.05`)*. **L1-F si comporta come deve** *(«vince lineare», il margine `31.81`)*.
- ### **L1-S:** **`0.189` (`TB3`) e `0.177` (`TBS`):** **la differenza fra il fit esponenziale e quello lineare sta sotto la deviazione dei residui: la finestra NON PUO' distinguere le forme.**
- ### **Quindi il «vince potenza» dei dati NON e' una lettura:** **il criterio non riconosce nemmeno un esponenziale sintetico ben curvo.** **Il fit a potenza ha `t0 ~ 0.002-0.003` unita': e' degenere** *(la potenza diventa `~ t^-a` con `a ~ 0.08`, che segue la curva iniziale dopo la rampa, non una legge)*. **Questa e' una lettura mia, da verificare.**
- ### **FERMO su L1** *(la regola: un sigillo che fallisce si committa e ci si ferma; la correzione e' un commit a se')*. **Le cure possibili, a Luca:**
  1. **la potenza con `t0` vincolato** *(`t0 >= T_DA`)*: **cambia un modello, e' una scelta;**
  2. **AIC coi punti efficaci e' troppo severo con `N_eff ~ 10`:** **un altro criterio** *(la validazione incrociata a blocchi)*.
- **E l'ordine:** **L1 e' girato PRIMA che arrivasse il mandato delle `01:22`** *(che lo mette ultimo nella coda)*. **Era la voce successiva della coda di prima.**

## 6. LA DECISIONE DI LUCA *(`2026-11-10` `08:42`)*: **L1 NON DECIDIBILE SU `30000` UNITA'**

### 6.1 L1.a, LA DECISIONE, REGISTRATA

> ### **«L1 non decidibile su `30000` tick (`TB3`, `TBS`); nessuna forma della durata si sceglie su questi dati; nessun cambio di modello o di criterio.»** *(Luca, `08:42`)*

- **Il «vince potenza» della sez. `5` resta scritto come NON-LETTURA:** **il criterio non riconosce un esponenziale sintetico** *(L1-P fallito)*, **e la differenza fra le forme sta sotto il rumore dei residui** *(L1-S `0.189`, `0.177`)*.
- **Le due cure della sez. `5`** *(la potenza con `t0` vincolato; la validazione incrociata a blocchi)* **NON si fanno:** **nessuna crea l'informazione che manca** *(Luca)*.
- *(Nota sulla parola: la finestra e' di `30000` UNITA' di tempo, `t · s`, cioe' `200000` tick a `s 0.15`; la decisione di Luca dice «tick», e si intende la stessa finestra.)*

### 6.2 L1.b, QUANTO DOVREBBE ESSERE LUNGA UNA CORSA PERCHE' L1-S PASSI `1` *(UNA STIMA, nessuna corsa)*

- **Le supposizioni** *(dichiarate)*: **i dati oltre `30000` seguono il fit esponenziale di adesso** *(`tau 141109` `TB3`, `142727` `TBS`, dal referto)*; **la deviazione dei residui resta quella di adesso;** **le medie su finestre di `311` da `t 1000`, come in L1.**
- **Il conto:** **L1-S(T) = L1-S(oggi) · D(T) / D(oggi)**, **`D(T)` lo scarto massimo fra `e^{-t/tau}` e la sua retta dei minimi quadrati sui centri delle finestre fino a `T`** *(`M0` si semplifica)*. **Lo script** *(nel solo scratchpad, perche' e' aritmetica sui numeri del referto; il testo intero qui sotto, per rifarlo)*:

```python
import numpy as np
P, DA, S = 311.0, 1000.0, 0.15
CASI = {"TB3": (141109.0, 0.1894), "TBS": (142727.0, 0.1769)}   # tau del fit esponenziale, L1-S
def D(tau, nfin):
    t = DA + P * (np.arange(nfin) + 0.5)
    y = np.exp(-t / tau)
    a, b = np.polyfit(t, y, 1)
    return float(np.max(np.abs(y - (a * t + b))))
for nome, (tau, s0) in CASI.items():
    d0 = D(tau, 93); n = 93
    while s0 * D(tau, n) / d0 < 1.0:
        n += 1
    print(nome, n, DA + P * n, (DA + P * n) / S)
```

- **L'uscita** *(girato alle `08:49:48`, dall'uscita di `date`)*:
  - **`TB3`:** **L1-S `>= 1` a `224` finestre: la fine a `t 70664` unita'** *(`471093` tick a `s 0.15`)*, **`2.41` volte la finestra di oggi;**
  - **`TBS`:** **`233` finestre: `t 73463`** *(`489753` tick)*, **`2.51` volte.**
  - *(La sola legge `T^2` della curvatura darebbe `67459` e `69767`: il resto e' l'ordine superiore di `e^{-t/tau}` a `T/tau ~ 0.5`.)*
- ### ⚠ **E' UNA STIMA, e solo una CONDIZIONE NECESSARIA:** **L1-S `>= 1` dice che la finestra POTREBBE distinguere esponenziale e lineare;** **non dice che L1-P passerebbe** *(il criterio AIC con `N_eff ~ 10` resta da provare su una sintetica alla nuova lunghezza)*, **ne' che la potenza si distinguerebbe** *(non stimato)*. **Se i dati futuri curvano meno del fit esponenziale, la corsa dovrebbe essere piu' lunga.**

### 6.3 L1.c, L2 E L4: LE LORO PREMESSE, RILETTE

- ### **L2 SI FERMA:** **presuppone una forma.** **La sez. `2`, L2: «la vita estrapolata col modello che vince L1 (se nessuno vince: con tutti e tre, e la dispersione e' l'errore di modello)».** **La fine primaria** *(il cuore sotto meta' del valore a `t 1000`)* **non e' dentro la finestra** *(`M_cuore` di `TBS` finisce a `3.293e+05`, sez. `5`; la meta' di quello a `t 1000` sta sotto)*: **e' un'estrapolazione, e su questi dati le tre forme si estrapolano a vite che non hanno niente in comune** *(il tempo in cui il fit scende a meta' del suo valore a `t 1000`, dai parametri della sez. `5`; lo script `l1c.py` qui sotto, girato alle `08:50:51`):* **`TB3`: esponenziale `t 9.881e+04`, lineare `8.02e+04`, potenza `4.915e+06`;** **`TBS`: `9.993e+04`, `8.108e+04`, `5.199e+06` unita'** *(un fattore `~60` fra le forme)*. **Con la decisione di Luca** *(«nessuna forma si sceglie»)* **la «dispersione come errore di modello» non e' una misura, e' la decisione mancante.** **L2 resta FERMO finche' una forma non e' decidibile** *(il criterio di chiusura: una corsa lunga come in 6.2, decisa da Luca, o un'altra definizione della vita che non estrapoli)*.
  - **Lo script `l1c.py`** *(aritmetica sui parametri del referto)*:

```python
import math
# L2 estrapolata coi fit di L1 (sez. 5): il tempo in cui M_cuore scende a meta' del valore del fit a t 1000.
FIT = {"TB3": ((397450.0, 141109.0), (1.28568e+06, 0.00180223, 0.0815467), (395168.0, 2.4791)),
       "TBS": ((394793.0, 142727.0), (1.20194e+06, 0.00348523, 0.0810101), (392540.0, 2.43575))}
for n, ((M0e, tau), (M0p, t0, a), (M0l, r)) in FIT.items():
    te = 1000.0 + tau * math.log(2.0)
    tp = (1.0 + 1000.0 / t0) * 2.0 ** (1.0 / a) * t0 - t0
    ml = M0l - r * 1000.0
    tl = (M0l - 0.5 * ml) / r
    print("%s: la meta' del valore a t 1000: esponenziale t %.4g, lineare t %.4g, potenza t %.4g (unita')" % (n, te, tl, tp))
```

- ### **L4 E' INDIPENDENTE, e resta in coda** *(dopo i test gia' ordinati: B1 sul laterale prima)*: **confronta i ritmi di perdita del cuore** *(in fase, in opposizione, da solo)* **SULLE STESSE FINESTRE di tempo:** **non estrapola, e un ritmo misurato su una finestra comune non chiede la forma.** **Due cose da scrivere PRIMA del suo codice:**
  1. **il ritmo senza modello** *(la pendenza media di `M_cuore` sulla finestra comune, con l'errore dai residui e `N_eff`)*: **NON il parametro di un fit di L1;**
  2. **la lettura dal codice gia' scritta nella sez. `2`:** **se le carte della coppia danno il cuore di ciascun solitone separato** *(`carta_coppia`)*.
