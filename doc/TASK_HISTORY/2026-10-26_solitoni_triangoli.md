# I SOLITONI ESISTONO SUI TRIANGOLI? *(la parte 2 del mandato della massa collettiva)*

> **Il mandato:** di Luca, `2026-10-26` *([[PROGETTO-MASSA-COLLETTIVA]], [[INDIRIZZO-MASSA-COLLETTIVA]], [[DECISIONE-LINEARE]], [[DECISIONE-SOLO-TRIANGOLI]])*: ### **rifare sui triangoli la misura dei solitoni larghi di `9a6955f3`, con `S1` e `S4` in memoria** *(`S3` per controllo)*, ### **agli stessi `s` e `N` di allora;** ### **si forma un oggetto legato e stabile? la larghezza, `mu`, il tempo di vita, la norma.**
> ### **In memoria, nessun file del nucleo; `S3` resta nel nucleo.** ### **Lo script `csv/_solitoni_triangoli.py`, il referto `doc/referti_l2/solitoni_triangoli.{txt,jsonl}`.**

**LIVELLO:** una misura statica e una dinamica.

## 0. LA STELLA POLARE

1. **`A14`:** ### **le norme del tick si conservano** *(si controllano)*. 2. **Il gradino:** ### **l'esistenza di un oggetto collettivo.** 3. **Aggiunge un numero o una legge?** ### **No: `S1`, `S4` sono OPZIONI in memoria.** 4. **Tocca `rho`, `c_s` o il segno?** ### **Il legame materia-vuoto e' cio' che lega.** 5. **Emergente o imposto?** ### **Il legame e' emergente o no: e' la misura.**

## 1. CHE COSA ERA LA MISURA DI ALLORA *(dal file)*

- ### **`9a6955f3`, la parte `C` di `csv/_modi_pi_e_solitoni.py`** *(`largo`)*: ### **il RISOLUTORE STATICO D'INVILUPPO `_gravita_collettiva.profilo`** *(`mu u = -c lap u + s alpha(u^2, Lambda0) u`, radiale, la scatola `R = 10 w`, `dr = w/640`, ripetuto finche' la larghezza cambia meno di `1e-3`)*; ### **`c = GC.c_di(g)` dal ramo a curvatura NEGATIVA del QUADRATO** *(`_forza_da_cs.rami(s, 0)`)*; ### **`LAM0 = 4`; `s` in `0.3, 0.5, 0.7, 0.9, 0.95, 0.99`; `N` in `10 ... 1e7`; `S1`, `S3`, `S4`; «largo» = almeno `4` archi.** ### **NESSUNA dinamica: il tempo di vita non fu misurato.**

## 2. LE DUE MISURE *(fissate qui)*

### **`(A)` L'ESISTENZA, il risolutore di allora sui triangoli:**
- ### **lo stesso `largo` di `_modi_pi_e_solitoni`** *(importato)*, ### **con `c` dei TRIANGOLI:** ### **`c = (1/2) d^2 w/dk^2` del ramo BASSO della coppia a `K`** *(`w = -arg(lambda)`, la fase per tick dei blocchi `_triangoli_forza.blocchi(0, s)`, cinque punti a `h = 1e-3` lungo `x` e lungo `y`: l'isotropia)*; ### **gli stessi `s`, `N`, forme.**
- ### **`LAM0`: `6`** *(il vuoto uniforme dei triangoli, `VUOTO_PER_ESTREMITA` su `6` estremita')* ### **E `4`** *(quello di allora, per il confronto diretto)*: ### **tutte e due riportate.**

### **`(B)` LA STABILITA' E IL TEMPO DI VITA, la dinamica sul reticolo** *(cio' che `9a6955f3` non fece)*:
- ### **per ogni forma, il PRIMO caso largo `>= 4` archi di `(A)` a `LAM0 6`** *(e, se esiste, uno STRETTO della stessa forma e `s`, per i solitoni incastrati)*;
- ### **lo stato: il profilo `u(r)` del risolutore sul toro a triangoli** *(`scena_l2.scena_toro("triangoli", (L, L), 1.0, x)`, `cs = s` a ogni nodo, `lambda_c None`)*, ### **`psi` della cella = `u(r_v) Q_basso e^{i K.r}`** *(`Q` il vettore del ramo basso di `_triangoli_forza.coppia_K(0, s)`, la costruzione di `_u1_prototipo.scena_materia`)*, ### **`sum rho = N`; il vuoto uniforme `VUOTO_PER_ESTREMITA`;**
- ### **il tick INTERO `tick.tick`** *(il legame ACCESO, la forma in memoria con `_screening_forme_s3.forma`; la moneta a `eps 0`)*;
- ### **le misure ogni `20` tick:** ### **la larghezza quadratica media, il picco di `rho`, la frazione entro `3 w0` dal centro, `M` e `V`;** ### **`mu` dalla rotazione di fase al centro contro `w0 + mu` del risolutore** *(una lettura)*.
- ### **IL TORO: `L = 12 w0` e `18 w0`** *(arrotondati a multipli di `3`: due taglie, la regola della convergenza)*; ### **`T_MAX = 2000` tick.**
- ### **STABILE, fissato prima:** ### **fino a `T_MAX` la larghezza entro `+-20%` di quella iniziale E la frazione entro `3 w0` `>= 0.8`;** ### **il tempo di vita = il primo tick che viola una delle due** *(o `> T_MAX`)*; ### **CONVERGE se le due taglie danno lo stesso verdetto e il tempo di vita entro il `20%`.**

## 3. I CRITERI

| | il criterio | il tipo |
|---|---|---|
| `1` | ### **il risolutore sul QUADRATO riproduce `9a6955f3`** *(le righe del jsonl di allora: `S1`, `S3`, `S4` a ogni `s` e `N`, `mu` e la larghezza entro `1e-12` relativo, il verdetto uguale)* | DEVE |
| `2` | ### **la dinamica conserva `M` e `V` entro `1e-10` relativo** | DEVE |
| `3` | ### **con `S1` a `s 0.3` si forma un solitone largo almeno `4` archi sui triangoli** *(`(A)`, `LAM0 6`)*, ### **STABILE** *(`(B)`)* | PUO' FALLIRE |
| `4` | ### **con `S4` solo da `s 0.7`, come sul quadrato** *(`(A)`)* | PUO' FALLIRE |
| `5` | ### **«il solitone e' un'onda libera»: a `N 10` `S1` lega** | ### **DEVE FALLIRE, PER LA CHIAVE GIUSTA: a `N 10` `S1` DISPERDE anche sui triangoli** *(come sul quadrato)* |

### **LA LETTURA, nessuna soglia:** ### **le larghezze e `mu` sui triangoli contro il quadrato.** ### **Mi FERMO** ### **se `1` o `2` fallisce.**

## 3-bis. ANNOTAZIONE, PRIMA DEL COMMIT DELLO SCRIPT *(le prove di costruzione, NON il referto)*

- ### **I NUMERI GIA' VISTI:** ### **`c` dei triangoli `-0.058270` a `s 0.3`** *(il quadrato `-0.063761`)*, ### **`-0.124403` a `s 0.7`** *(il quadrato `-0.245921`)*; ### **isotropa** *(`x` e `y` uguali a `1e-9`)*; ### **`S1`, `s 0.3`, `LAM0 6`: `N 10` DISPERDE, `N 1e3` `1.291` archi, `N 1e5` `3.754`, `N 1e6` `6.600`** *(il primo largo sara' a `N 1e6`, non `1e5`)*; ### **la dinamica di `S1`, `N 1e6`, `L 81`, `60`-`100` tick: `M` e `V` a `1e-14`, la larghezza respira del `2`-`3%`, e LA ROTAZIONE PER TICK al centro `-1.102086` contro la prevista `-1.102150` con lo zero di OGGI** *(il tick gira nella convenzione di oggi; il risolutore prende `w0` dai blocchi nello zero simmetrico: `w0_oggi = w0_simm - pi s`)*. ### **Le soglie del §2 restano.**
- ### **LA MISURA DELLA ROTAZIONE, corretta prima del commit:** ### **la prima scrittura campionava ogni `20` tick, e la fase si avvolgeva** *(`~22` rad in `20` tick)*: ### **ora si segue a OGNI tick.**
- ### ⚠ **UN MIO ERRORE DI METODO, da registrare:** ### **la scratchpad contiene COPIE VECCHIE di strumenti** *(`_gravita_collettiva.py`, `_modi_pi_e_solitoni.py`, `_forza_da_cs.py`, `_triangoli_forza.py` e altri, di sessioni precedenti)*, ### **e uno script provato da li' le importa al posto di quelle di `csv/`** *(cosi' e' nato un `AttributeError` falso)*. ### **Le CORSE committate girano tutte da `csv/` e non ne sono toccate;** ### **le prove di costruzione di oggi fatte dalla scratchpad sono letture da prendere con questa riserva.** ### **Da qui: le prove da una cartella PULITA** *(`prova_pulita/`, solo lo script in prova)*.

## 4. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice; ### **e la parte `3` SOLO se `(B)` trova un solitone stabile.**

## 5. IL RISULTATO *(dopo `7b27cb32`)*

### **IL REFERTO:** `doc/referti_l2/solitoni_triangoli.{txt,jsonl}` *(`csv/_solitoni_triangoli.py` al commit `7b27cb32`; il task history `836370cd`)*. ### **`3/5`, nessun DEVE fallito; i due PUO' FALLIRE FALLISCONO.** ### ⛔ **NESSUN SOLITONE STABILE: la parte `3` NON si esegue** *(la condizione del mandato)*.

- ### **IL CONTROLLO:** ### **il risolutore sul quadrato riproduce `9a6955f3` ESATTAMENTE** *(il verdetto, `mu`, la larghezza: lo scarto peggiore `0.0`)*.
- ### **`(A)` L'ESISTENZA, il risolutore d'inviluppo sui triangoli** *(la curvatura della coppia, isotropa)*: ### **`S1`, `s 0.3`: `c = -0.058270`** *(il quadrato `-0.063761`)*, ### **il primo largo a `N 1e6`, `6.600` archi, `mu +0.2983`** *(`LAM0 6`; con `LAM0 4` a `N 1e5`, `4.144`, come sul quadrato)*; ### **`N 10` DISPERDE a ogni `s`** *(la chiave)*. ### ⚠ **`S3` e `S4`: NESSUNO stato largo `>= 4` archi** *(`S4`, `s 0.7`, `N 1e7`: `3.022` archi; `s 0.99`: `2.840`; `S3` largo e' «non rappresentabile»)*: ### **la ragione e' la curvatura: vicino a `s = 1` sul quadrato `c` diverge** *(`-8.632` a `s 0.99`: il modo senza massa a `(pi, pi)`)*, ### **sui triangoli NO** *(`-0.144`)*: ### **i solitoni di `S4` e `S3` restano STRETTI.**
- ### ⭐ **`(B)` LA DINAMICA: IL SOLITONE DI `S1` NON E' STABILE.** ### **Messo sul toro a triangoli col tick intero, il legame acceso:** ### **`N 1e6`: la larghezza va da `6.63` a `20.0` / `23.8` archi in `2000` tick, la frazione entro `3 w0` scende a `0.54` / `0.41`; il TEMPO DI VITA `320` tick a tutte e due le taglie** *(`L 81`, `120`: CONVERGE)*; ### **`N 1e5`: da `3.81` a `8.7`, vita `140` tick, a tutte e due le taglie.** ### **`M` e `V` conservati a `3e-13`.**
- ### **LA ROTAZIONE AL CENTRO conferma che lo stato di partenza E' lo stazionario dell'inviluppo** *(`-1.10109` per tick contro `-1.10215` previsti con lo zero di oggi, `N 1e6`)*: ### **l'oggetto c'e' all'istante zero, e si disfa.** ### **La differenza fra il risolutore e la dinamica e' cio' che il risolutore TRASCURA: il vuoto FISSO** *(la retroazione del vuoto: il task history di `c4efc937`)*; ### **nel tick il vuoto risponde, e il legame che teneva il solitone non tiene piu'.** ### **E' una lettura, non una misura separata: la prova** *(il tick col vuoto congelato)* ### **e' il passo successivo.**
- ### **LE PREVISIONI DEL GUARDIANO DELLE `09:04`:** ### **`P2` «`S1` forma un solitone stabile sui triangoli a `s 0.3`» (`65%`): NO** *(esiste statico, non stabile)*; ### **«le larghezze entro un fattore `1.5` dal quadrato»: SI'** *(`6.60` contro `7.46` a `N 1e6`)*; ### **«`S4` solo da `s` grande» (`55%`): `S4` NON forma solitoni larghi a nessun `s`.**
