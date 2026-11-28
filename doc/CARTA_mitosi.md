# LA CARTA DELLA MITOSI (ramo `mitosi`)

*(Nasce il 2026-11-25 con [M0237]: non c'era una `CARTA_mitosi.md`. Le carte della mitosi in uso prima erano nei task history di `primo-ordine` — per `mitosi_lunga.py`, `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md`, sez. `10`-`12` — e in `doc/MITOSI_era2_carta.md`. Questa e' la carta delle prove di [M0237] in poi.)* [[PROGETTO-MITOSI]]

## LE TRE PROVE *([M0237], DECISIONE DI LUCA `02:37`, arrivata dalla posta, `guardiano/posta/2026-11-25_0237_M0237.md`, `319cfd2f`; scritta PRIMA dei pezzi 2-4)*

- **`git log --all --fixed-strings --grep "[M0237"`:** solo il commit della posta *(`319cfd2f`)*.
- **Le tre domande** *(Luca)*: (1) l'energia totale durante la fiammata cresce, sta ferma o cala; (2) col la soglia di nascita a meta' e a doppio, il ritmo cambia come dice una formula di due righe *(e' un parametro)* o no *(e' fisica)*; (3) nasce qualcosa in un vuoto senza materia?
- **LE SCELTE DI LUCA:**
  - **S1.** il lavoro su `mitosi` in un worktree separato, fuori da `E:\soliton_simulator`: **`C:\Users\lpeano\wt_mitosi`** *(gia' esistente: e' quello del merge [M1330-A2])*;
  - **S2.** il pezzo 2 e' a costo zero; i pezzi 3 e 4 sono corse di al piu' `6000` tick, in coda DOPO quelle di [M0137];
  - **S3.** **«cresce / ferma / cala»** si giudica su `|dH|/|H|` fra l'inizio e la fine della fiammata, contro la deriva di fondo misurata prima della prima nascita sullo stesso numero di tick: **ferma = entro `3` volte la deriva di fondo**. **«Il ritmo come dice la formula»** = le nascite nei `6000` tick, a soglia `1/2` e `2`, entro il `20%` di quelle che prevede la formula scritta qui.
- **IL PEZZO 0, I DATI PRIMA DEI NUMERI** *(`mitosi_dati.py`, `mitosi_dati.txt`)*:
  - **le corse** *(`E:/soliton_simulator/controllo/mitosi_rami/`)*: **TRONCO**, senza nascite, `131` stati da `stato_03250` a `stato_35750`, piu' `prima_nascita_35976.npz`; **MITOSI**, da `35976` a `36250`, `2` stati; **MITOSI_V2**, da `36250` a `45976`, `39` stati;
  - **la corsa con la fiammata e' MITOSI_V2**: il mandato dice «MITOSI fino a k 36000», ma MITOSI si ferma a `36250` *(il suo log finisce con un triangolo degenere)* e MITOSI_V2 la continua;
  - **le nascite:** **`538`**, dal `k 35976` al `k 45949` *(9 in MITOSI, 529 in MITOSI_V2)*; le prime `35976 36001 36027 36059 36125 ...`;
  - **la fiammata** *(il primo intervallo sotto `1/10` del primo, `25` tick)*: **alla nascita 12, `k 36294`**. Per finestra di `500`: `26` nascite in `[36000, 36500)`, `45` in `[36500, 37000)`, poi da `16` a `37`;
  - **la deriva di fondo:** la fiammata dura `9656` tick *(da `36294` a `45950`, l'ultimo punto della serie)*. Sul TRONCO, sugli stessi `9656` tick prima della prima nascita: `E(26300) = +8.2679735766e+06`, `E(35750) = +8.2678172286e+06`, **`|dE|/|E| = 1.891e-05`**. **«Ferma» = entro `5.67e-05`.**
  - **`E`** e' la serie `E` di `controllo_senza_bordo.Misure`, ogni `50` tick. Il caso noto K1 del pezzo 2 la confronta con `energia_corsa` sullo stato `36000`.
- **IL PEZZO 2** *(`mitosi_energia_fiammata.py`, a costo zero)*: dagli stati e dai registri, `H(k)`, `E_persa(k)`, i nodi `n(k)`, `DH` per nascita, prima e lungo la fiammata.
  - **(K1)** `H` dello stato `36000`, rifatto da `energia_corsa`, uguale al bit a quello del meta *(se nel meta c'e'; altrimenti alla serie, dichiarato)*;
  - **(K2)** la somma dei `DH` delle nascite = `E_persa` entro `1e-9` *(se non lo e', si dichiara)*;
  - **il verdetto S3:** CRESCE / FERMA / CALA.
- **IL PEZZO 3, LA SOGLIA** *(`mitosi_soglia.py`)*: due corse da `prima_nascita_35976.npz`, `6000` tick, con la soglia `QUANTO` del contatore *(`csv/solitone/contatore.py`: un arco scatta a `|Theta| >= 2 pi`)* a **`pi`** *(meta')* e a **`4 pi`** *(doppio)*, tutto il resto uguale, stati ogni `250`, il registro delle nascite. **(K3)** a soglia `2 pi` i primi `250` tick rifanno MITOSI al bit.
- ### **LA FORMULA DEL RITMO ATTESO, SCRITTA ORA** *(Luca: «prima di guardare»)*:
  - `Theta` di ogni arco cresce di `pi (dtau_i - dtau_j)` a ogni tick, a ritmo costante se il lapse non cambia, e l'arco scatta quando `|Theta|` arriva alla soglia `s 2 pi`. **Se il ritmo per arco non dipende dalla soglia, il tempo per arrivarci e' proporzionale a `s`, e le nascite in una finestra fissa sono inversamente proporzionali a `s`:**
  - **`N(s) = N_1 / s`**, con **`N_1`** = le nascite di MITOSI e MITOSI_V2 in `[35976, 41976)` *(i `6000` tick dalla stessa partenza, a soglia `1`, contate da `mitosi_soglia.py` sui `nascite_*.json`)*. **Quindi `N(1/2) = 2 N_1`, `N(2) = N_1/2`.**
  - **Cio' che la formula ignora, detto ora:** gli archi gia' oltre `pi` alla partenza scattano subito *(una nascita per tick)*; gli archi nuovi partono da `Theta = 0`; la crescita cambia il lapse. **Se il ritmo esce dal `20%`, e' per uno di questi o per la fisica: il referto lo dice coi numeri.**
- **IL PEZZO 4, IL VUOTO** *(`mitosi_vuoto.py`)*: una corsa dal vuoto puro *(`phi` al fondo, `psi = 0`, le stesse fasi del tronco)*, nascite accese, `6000` tick. **(K4)** il vuoto senza nascite fermo `250` tick *(norma e `H` entro `1e-9`)*. Il referto: nascite si'/no, a quali `k`, la densita' locale alla prima.
- **LE PREVISIONI DEL GUARDIANO** *(dalla posta)*: P1 *(`60%`)* lungo la fiammata H CALA *(E_persa cresce, DH negativo)*; P2 *(`55%`)* a soglia `1/2` le nascite sono piu' del doppio di quelle a soglia `1`; P3 *(`70%`)* nel vuoto puro nessuna nascita in `6000` tick; P4 *(`50%`)* la somma dei DH NON torna con E_persa a `1e-9`.
- **LE MIE:** P1 `75%` *(i DH delle prime nascite nel registro sono negativi: `-25.8`)*; P2 `55%`; P3 `80%`; P4 `40%`.
- **IL PEZZO 3, le scelte dichiarate prima** *(`mitosi_soglia.py`)*:
  - la soglia si cambia in memoria su `contatore.QUANTO`, **coi due nomi dello stesso file** *(`mitosi_lunga.riprendi` fa `import contatore`, un modulo di primo livello, distinto da `solitone.contatore`)*;
  - le corse vanno in coda **col percorso assoluto dello script del worktree `mitosi`**, e lo script si porta da solo nella radice del suo worktree;
  - **(K3) e' una corsa** *(`274` tick, da `35976` a `36250`)*: va in coda insieme alle due;
  - **IL COSTO:** MITOSI_V2 ha fatto `9726` tick in `73019` s *(il suo log)*, cioe' circa `7.5` s per tick con le nascite. **Una corsa di `6000` tick dura circa `12` ore.**


## D1 E D2 *([M2034], DECISIONE DI LUCA 2026-11-26 `20:34`, arrivata dalla posta, `3ec35629`; scritta PRIMA del codice nuovo)*

- **D1, LA PROVENIENZA DI MITOSI** *(a costo zero: i TIMBRO dei log in `mitosi_rami/`, i blob di oggi, `git log`)*:
  - **MITOSI** *(da `35976` a `36250`)* viene da **`doc/referti_l2/mitosi_rami.py ramo --nome MITOSI --da primo`**: blob `6dccd9d6` *(sha1 dei byte)*, l'ultimo commit `bd2adaad` *(2026-11-20 18:49)*. Importa `mitosi_lunga.py` *(`4d484044`, `74184d78`)*. Il suo `ciclo` fa per prima cosa **«lo scatto del tronco»** *(la nascita al `k` dello stato, `nascita_iniziale`)* e tiene **`gauss_acc`**. **NON e' `mitosi_lunga.corsa`:** per questo K3 cadeva *(la prima nascita a `35977`)*. MITOSI e' caduta dopo `36250` *(il suo log finisce con un triangolo degenere)*;
  - **MITOSI_V2** *(da `36250` a `45976`)* viene da **`doc/referti_l2/mitosi_rami_v2.py riparti --da MITOSI/stato_36250.npz`**: blob `a17baaad`, l'ultimo commit `0dd4b707` *(2026-11-21 23:56)*, **con la regola `mitosi_regola_v2`**;
  - **i blob di oggi coincidono** con quelli dei TIMBRO.
  - **LA CORSA DI RIFERIMENTO A SOGLIA 1 E' QUINDI IN DUE PASSI:** la v1 da `prima_nascita_35976` a `36250`, poi la v2 da li'. **Le corse di soglia la rifanno cosi', cambiando solo `QUANTO`** *(«tutto il resto uguale»)*: fase 1 con `mitosi_rami.ciclo`, fase 2 con `mitosi_rami_v2.ciclo` dallo stato `36250` della fase 1, fino a `41976`.
  - **I CASI NOTI, RISCRITTI** *(`mitosi_soglia_v2.py noto`)*: **(K3)** la fase 1 a soglia `2 pi`, da `prima_nascita_35976` a `36250` = MITOSI agli stati `36000` e `36250` **AL BIT** *(ogni chiave)*; **(K3b)** la fase 2 a soglia `2 pi`, da `MITOSI/stato_36250` a `36500` = MITOSI_V2 a `36500` **AL BIT**.
  - **Se la fase 1 a soglia `pi` o `4 pi` cade prima di `36250`** *(il triangolo degenere della v1)*, **FERMO** per quella soglia, coi numeri.
- **D2, IL RESIDUO DI GAUSS NEL VUOTO PURO** *(dichiarato PRIMA di rifare K4)*:
  - `mattone.Campi.residuo` restituisce `max |div E - e (rho - media)| / (e max rho)`, che con `psi = 0` divide per zero;
  - **nel solo script del vuoto** *(`mitosi_vuoto_v2.py`)* **il residuo diventa assoluto:** `max |div E - e (rho - media)|`, **senza dividere** *(Luca, D2)*. Lo si sostituisce in memoria sulla classe `Campi`, con entrambi i nomi del modulo *(`mattone`, `solitone.mattone`)*. **E' una misura: il ciclo la chiama ogni `OGNI_GAUSS` e la stampa, non corregge niente;**
  - **la corsa del vuoto passa per `mitosi_rami_v2.ciclo`** *(la via vera)*, dallo stato `M0237/vuoto/vuoto_35976.npz` *(gia' preparato: `psi = 0`, `phi = a phi_v`, i campi e `theta_a` a zero)*, **con `nascita_iniziale = False`** *(nel vuoto non c'e' uno scatto del tronco)*;
  - **(K4), rifatto:** con le nascite spente *(il modo `c2ext`)*, da `35976` a `36250`: `somma |phi_h|^2` e `H` *(la serie `E`)* fermi entro `1e-9` relativo, fra `36000` e `36250`.
- **L'ORDINE** *(Luca)*: K3, K3b e K4 adesso, mentre girano d1', d2', d3'. **Le corse lunghe** *(soglia `pi`, soglia `4 pi`, il vuoto)* **DOPO** d1', d2', d3'.
- **IL COSTO:** circa `4.5`-`7.5` s per tick *(K3 della v1: `274` tick in `1242` s)*. Una corsa di `6000` tick dura **circa `8`-`12` ore.**
- **La previsione del guardiano P6** *(`60%`)*: D1 trova che MITOSI viene da un'altra via. **SI'** *(`mitosi_rami.py`)*.


## K4' E LA SOGLIA CHIUSA *([M0024], DECISIONE DI LUCA, 2026-11-27 `00:24`, arrivata dalla posta, `e609aafa`; scritta PRIMA di `mitosi_vuoto_v3.py`)*

- **K4', LA SCELTA DI LUCA:**
  - il criterio su `H` diventa ASSOLUTO: `|H(250) - H(0)| < 1e-9 |H_rif|`, con `H_rif` = l'energia del vuoto fresco sullo stesso reticolo;
  - **se anche quella e' circa `0`, vale `|Delta H| < 1e-12`, dichiarato**;
  - la norma resta com'e' gia' misurata *(`8.99e-14`)*;
  - **se K4' passa**, va in coda la corsa del vuoto puro con le nascite accese, `6000` tick.
- **LE MIE SCELTE, dichiarate prima:**
  - **`H_rif`** e' `H` dello stato di partenza `vuoto_35976.npz`. Quello stato e' gia' il vuoto fresco sullo stesso reticolo: `mitosi_vuoto.py prepara` mette `phi_h = a phi_v` e `psi = 0`. Il primo valore che la serie misura e' `k 36000`;
  - **«circa 0»** significa `|H_rif| < 1e-9`;
  - **`Delta`** e' preso fra `36000` e `36250`, come in K4;
  - **non rifaccio la corsa:** la v3 legge le uscite di K4 *(`M0237/vuoto_v2_noto`)*. Il codice della via non e' cambiato, quindi rifarla darebbe gli stessi byte.
- **### LA PREVISIONE, MIA, PRIMA DI APPLICARLO: K4' FALLISCE** *(la regola «una soglia DEVE contro la sua premessa»)*:
  - la serie `E` di K4 e' gia' sul disco, e fra un campione e il successivo *(ogni `50` tick)* salta da `3.2e-14` a `1.2e-10`. **E' il rumore di arrotondamento di una somma che vale zero;**
  - `|Delta H|` fra `36000` e `36250` e' `1.208e-10`, cioe' **oltre `100` volte `1e-12`**;
  - **la soglia di `1e-12` sta sotto il pavimento di arrotondamento di questa somma.** La applico com'e', e se fallisce la corsa del vuoto non va in coda.
- **IL GUARDIANO, P4 *(`70%`)*:** K4' passa e nel vuoto puro non nasce nulla in `6000` tick. **La mia, prima:** K4' passa al `5%`.
- **S. LA SOGLIA SI CHIUDE COSI' COM'E'** *(DECISIONE DI LUCA `00:24`)*:
  - nessuna corsa in piu';
  - la frase di Luca: **«il quanto `2 pi` non e' un parametro: a `pi` il reticolo si ingolfa, a `4 pi` non nasce nulla in `6000` tick; la domanda di Sheldon sulla formula `N(s) = N_1/s` e' mal posta, e si dichiara».** La parte ancora aperta *(il ritmo a `2 pi` contro il tempo)* resta in attesa.
- **### LA NOTA, MIA, SU CHE COSA E' STATO MISURATO** *(i log in `doc/referti_l2/mitosi_soglia_v2_{0.5,2}_log.txt`, `21745434`)*:
  - **a `pi`:** cosa misurata. Alla prima nascita `2094` archi sono in attesa sopra la soglia; tre nascite *(k `35976-35978`)*; alla quarta il triangolo `(12537, 12723, 34599)` e' degenere e la corsa si ferma *(uscita `1`)*. **«Si ingolfa» e' una lettura giusta del dato;**
  - **a `4 pi`: «non nasce nulla in `6000` tick» NON E' MISURATO.** La corsa si e' fermata **alla partenza** *(k `35976`, uscita `1`)* su «lo stato del tronco NON ha un arco scattato», e **non ha fatto nessun tick**. Il fatto misurato e' piu' debole: **nello stato in cui a `2 pi` nasce il primo nodo, a `4 pi` nessun arco ha ancora superato la soglia.** Quanto tardi arriverebbe la prima nascita a `4 pi`, e se arriverebbe, non lo sappiamo;
  - **quindi la frase di Luca sta qui come DECISIONE, e la sua seconda meta' come NON MISURATA.** Come conclusione di fisica, «`2 pi` strutturale» poggia per ora sulla sola parte a `pi`.

## K4'' E LA CORSA DEL VUOTO PURO *([M0106], DECISIONE DI LUCA, 2026-11-27 `01:06`, arrivata dalla posta, `4c973b3a`; scritta PRIMA di `mitosi_vuoto_v4.py`)*

- **L'ERRORE n.258 DEL GUARDIANO:** K4' aveva una soglia sotto il pavimento dell'arrotondamento *(`ca8ddfeb`)*.
- **K4'', LA SCELTA DI LUCA:**
  - il criterio e' la norma di `phi`, ferma entro `1e-9` in `250` tick *(gia' misurata: `8.99e-14`)*;
  - `|Delta H|` si stampa con `H_rif`, e non blocca;
  - poi la corsa del vuoto puro con le nascite accese: `6000` tick, stati ogni `250`, in coda.
- **LE MIE SCELTE, dichiarate prima:**
  - **K4''** si applica alle uscite della corsa K4 *(`M0237/vuoto_v2_noto`)*, come in K4';
  - **la corsa** e' `mitosi_vuoto_v2.py corsa`, invariata *(il modo `mitosi`, da `35976` a `41976`, in `M0237/vuoto_v2`)*: va in coda sul lanciatore di lapse-u, con il percorso assoluto;
  - **il referto** `mitosi_vuoto_v3.txt` *(il nome lo da' il mandato)* nasce da `mitosi_vuoto_v4.py lettura`: le nascite, sì o no e a quali `k`; la norma di ogni stato; `H(k)`;
  - **la densita' locale alla prima nascita**, se ce n'e' una, si legge con uno script a parte, dopo, perche' dipende da dove nasce.
- **LE PREVISIONI:**
  - **del guardiano:** P2 *(`60%`)* non nasce nulla in `6000` tick; P3 *(`55%`)* se nasce qualcosa, nasce dopo `k 3000` e sul bordo del toro;
  - **le mie:** K4'' passa *(gia' misurato)*. P2 al `75%`: il vuoto fresco e' un autostato, quindi le fasi degli archi non dovrebbero accumularsi fino a `2 pi`.


## A. LE CINQUE LETTURE A COSTO ZERO *([M2245-27], DECISIONE DI LUCA 2026-11-27 `22:45`, dalla posta, `c00aa4b3`; `23:14` e `23:21` per la suite; scritta PRIMA del codice; un processo alla volta, nessuna corsa)* [[PROGETTO-MITOSI]]

**I dati:** solo stati e registri che ci sono gia'.
- **La fiammata:** `E:/soliton_simulator/controllo/mitosi_rami`, cioe' `TRONCO`, `MITOSI` e `MITOSI_V2`, letti con `mitosi_dati.py`. Ci sono `538` nascite fra `k 35976` e `45949`, e la fiammata parte dalla nascita 12, a `k 36294`.
- **I triangoli:** `controllo/CHI/triangolo/{t120, t120r28, t000}`.
- **La coppia:** `controllo/M2034/coppia/d1`.

**Le soglie che fisso io** sono criteri dentro il mandato, dichiarati qui prima dei numeri. Quelle del guardiano, dove le adotto, lo dico.

### A1. IL COSTO DI UN NODO -> `doc/referti_l2/mitosi_costo_nodo.py`, `mitosi_costo_nodo.txt`

- **Le grandezze:** per ogni nascita `DH` (dal registro), il numero di nodi `n(k)` al momento della nascita e **la densita' locale**.
  - `n(k)` e' `n0 + i`, con `n0` dal meta di `stato_36000` meno le sue nascite e `i` il numero d'ordine della nascita: e' la stessa regola di `mitosi_energia_fiammata.py`.
  - **La densita' locale** e' la media di `rho` sui nodi entro una distanza `4` dalla `pos` della nascita (`toro.scarti`, `L 186`). La `rho` viene dallo **stato salvato piu' vicino con `k <=` quello della nascita**, ogni `250`. La risoluzione di `250` tick e' dichiarata.
- **Il fit, dichiarato prima:** minimi quadrati `DH = a + b x`, con `x = n` e poi con `x = densita'`; `sigma_b` dai residui.
  - **«COSTANTE»** se `|b| < 2 sigma_b`;
  - altrimenti si aggiunge `c x^2`: **«LINEARE»** se `|c| < 2 sigma_c`, **«ALTRO»** se no;
  - si stampa anche lo Spearman, come lettura.
- **I casi noti:**
  - **(K1)** `-somma DH` delle `538` nascite = `E_persa` finale entro `1e-9` relativo. E' gia' passato in [M0237-2] e si rifa';
  - **(K2)** il fit su dati sintetici costanti piu' rumore (seme fisso) da' COSTANTE, e su dati con una pendenza nota la ritrova entro `2 sigma`;
  - **(K3)** la densita' locale di una `rho` costante `c` e' `c` al bit.

### A2. a(k) = sqrt(n(k)) -> `doc/referti_l2/mitosi_a_di_k.py`, `mitosi_a_di_k.txt`

- **Le grandezze:** `n(k)` come in A1, letto ai bordi delle finestre di `500` da `k 36000` a `46000`, e `a = sqrt(n)`.
  - `H_i = (a_{i+1} - a_{i-1}) / (2 * 500 * a_i)`;
  - `a''_i = (a_{i+1} - 2 a_i + a_{i-1}) / 500^2`;
  - `q_i = - a''_i a_i / a'_i^2`.
- **La lettura:** la sequenza dei segni di `q`. **«C'e' una fase con `q > 0` prima di una con `q < 0`?»** La risposta e' si' se esiste un `i` tale che `q > 0` nelle finestre prima e `q < 0` in almeno `2` finestre consecutive dopo. **Nessuna ipotesi su Lambda.**
- **I casi noti:**
  - **(K1)** `a` lineare in `k` da' `q = 0` entro `1e-12`;
  - **(K2)** `a` esponenziale da' `q = -1` entro l'errore della differenza finita, stampato;
  - **(K3)** `a ∝ k^(1/2)` da' `q = +1`, con lo stesso criterio.

### A3. IL RITMO DELLE NASCITE -> `doc/referti_l2/mitosi_ritmo.py`, `mitosi_ritmo.txt`

- **Le finestre** sono di `250`, da `k 36250` a `46000`. **In ogni finestra** si contano le nascite in `10` sottofinestre di `25` tick (`25` e' il primo intervallo fra due nascite, `mitosi_dati.txt`), e si calcola **il rapporto varianza/media** di quei conteggi.
- **La soglia, quella del guardiano, che adotto:** **«A GRADINI»** se il rapporto supera `2` in **oltre meta'** delle finestre con almeno `2` nascite; **«LISCIO»** se sta fra `0.5` e `2` in oltre meta'; **«ALTRO»** se no.
  - Il rapporto per finestre di `250` su tutta la fiammata si stampa insieme.
  - Le sottofinestre di `10` e di `50` tick si stampano **come sensibilita'**: il verdetto resta quello con `25`.
- **I casi noti** (seme fisso):
  - **(K1)** nascite regolari, una ogni `25` tick, danno un rapporto `0`;
  - **(K2)** nascite di Poisson danno un rapporto mediano fra `0.5` e `2`;
  - **(K3)** pacchetti di `5` nascite nello stesso tick danno un rapporto sopra `2`.

### A4. LE TRE SFASATE -> `doc/referti_l2/triangoli_vortice.py`, `triangoli_vortice.txt` *(il pezzo 0 di [M-GM])*

- **Gli stati che ci sono, e lo dichiaro come chiede la lettera:**
  - **`t120`:** il triangolo «destro», con le fasi `0, 120, 240` in senso antiorario;
  - **`t120r28`:** il suo gemello ruotato di `15` gradi. Ha **le stesse fasi e lo stesso verso**: **non e' un «sinistro».** Un triangolo sinistro (`0, 240, 120`) con `chi` acceso **non c'e'**, e lo dichiaro;
  - **`t000`:** il triangolo in fase.
  - Per ciascuno si legge **il primo stato e l'ultimo** salvati, e uno ogni `5000` in mezzo.
- **Il numero di vortice:** il giro della fase di `psi` attorno al centro (il baricentro dei tre vertici), in unita' di `2 pi`.
  - Si calcola sulla componente di `psi` con la norma piu' grande, come in `triangolo_120`, sommando le differenze di fase ridotte in `(-pi, pi]` lungo un cerchio di `N` punti al raggio `r`.
  - **Il raggio principale e' il raggio circoscritto**, cioe' il cerchio che passa per i tre corpi, dove `psi` non e' trascurabile. Si stampano anche `0.5` e `1.5` volte il raggio.
  - **Il verdetto:** «giro intero» se il valore principale dista da un intero meno di `0.1`.
- **La corrente circolante `J_theta`** per anello `[0, R/2)`, `[R/2, R)`, `[R, 3R/2)`, con `R` il raggio circoscritto. `J` e' la corrente di `psi` sugli archi, `Im(somma_c conj(psi_i) psi_j)`, proiettata sulla direzione tangente.
- **`Theta` sommato su un giro chiuso attorno al centro** (gli archi di un cammino chiuso del grafo vicino al raggio principale, ciascuno col suo verso). **DEVE essere zero entro `1e-9`: e' il caso noto, non una misura** (l'errore n.261 del guardiano).
- **I casi noti:**
  - **(K1)** sulla `psi` di partenza (`k 0`) di `t120` il giro e' `+1`, e quello di `t000` e' `0`. E' il DEVE di `triangolo_120` al tick `0`;
  - **(K2)** **DEVE FALLIRE**: una `psi` con la fase invertita (`conj`) da' `-1`;
  - **(K3)** il giro di `Theta`.
- **Per [M-GM] (D4):** se nessuno dei tre ha un giro intero diverso da zero all'ultimo stato, **[M-GM] si ferma qui** e si dichiara.

### A5. IL VENTO A DUE CORPI -> `doc/referti_l2/vento_due_corpi.py`, `vento_due_corpi.txt`

- **Gli stati:** `M2034/coppia/d1`, da `k 0` a `6000`, ogni `250`.
- **I due corpi:** si prendono da `coppia_a0.a0`, che da' i due picchi. Gli stati che non sono DUE si stampano e restano fuori dalla media.
- **`J_phi`** e' la formula di `vuoto_giro3.py` (`rho_phi grad theta`, con `theta` la fase di `somma conj(phi_v) phi` per nodo, e i nodi giusti `(m1 +- 1, m2)` e `(m1 +- 1, m2 +- 2)`):
  - **la componente radiale attorno a ciascun corpo**, negli anelli `[8, 16)` e `[16, 32)`, **negativa se e' verso il corpo**;
  - **la componente lungo l'asse fra i due**, sui nodi a meno di `2` dal segmento che unisce i due corpi, proiettata sul versore verso il baricentro della coppia, **positiva se e' verso il baricentro**.
  - **Per finestra di `500`:** la media sugli stati della finestra.
- **I casi noti:** quelli di `vuoto_giro3` (V1):
  - sul vuoto fresco la corrente e' `0` entro `1e-9`;
  - **DEVE FALLIRE** con una fase `q y`, che da' una corrente lungo `y`.

### LE PREVISIONI *(prima dei numeri)*

- **Del guardiano** (copiate dalla lettera):
  - A1 (`50%`): `DH` cresce con la densita' locale;
  - A2 (`70%`): nessuna fase con `q > 0`;
  - A3 (`60%`): a gradini;
  - A4 (`70%`): `+-1` per le sfasate e `0` per quello in fase;
  - A5 (`60%`): vento radiale verso ciascun corpo e, lungo l'asse, verso il baricentro.
- **Le mie:**
  - **A1:** «LINEARE» o «ALTRO» contro la densita' (`55%`): i `DH` vanno da `-57.76` a `-2.50`, troppo sparsi per essere una costante;
  - **A2:** **c'e' `q > 0` per gran parte della fiammata** (`70%`). Le nascite per `500` calano da `45` a `16`, quindi `a'` cala, e un `a'` che cala e' una decelerazione: e' **contro** la previsione A2 del guardiano;
  - **A3:** «A GRADINI» (`45%`);
  - **A4:** `t120` `+1` all'ultimo stato (`60%`): la saturazione potrebbe aver rotto il giro; `t000` `0` (`80%`);
  - **A5:** radiale verso il corpo nell'anello `[16, 32)` (`65%`), come il vento del giro 3; lungo l'asse verso il baricentro (`50%`).


## C E F, PRIMA DEL CODICE: LE SCELTE CHE IL CODICE NON HA *([M2245-27], DECISIONE DI LUCA 2026-11-27 `22:45` e `22:47`; scritta il 2026-11-28 alle `00:13` (l'ora di `accoda.py`; nel commit `d61e1361` c'era scritto, sbagliato, «verso le `00:25`»), PRIMA di ogni riga di `corpo_fuso_mitosi.py` e di `vuoto_lapse_mitosi.py`)* [[PROGETTO-MITOSI]]

**Che cosa ho letto nel codice:**
- **Le nascite e `chi` non si sono mai incontrati.** Nessuno script della mitosi usa `chi_tick_v2`.
- **Le nascite** (`mitosi_lunga.Nascite.nasci`) passano da `mitosi_regola`:
  - `regola(Z, C, a, "stella")` sceglie il flip;
  - `applica` allunga gli array dei nodi;
  - `energia_corsa` da' `H` **senza `chi`**.
- **La scena delle nascite** e' `CV.scena_L(186, ...)` dentro `mitosi_rami_v2.ciclo`. Quella del corpo fuso e della coppia e' la scena del triangolo, `L 162` (`TC.scena`, `corpo_fuso.Ripresa10` con `geo.U` riscritta).
- **Il lapse dipinto di [M2210]** (`caduta_libera.campo_N`, con `chi = A sin(2 pi (y - y_c)/L_y)` e `N = exp(-kappa chi)`) entra col tick `caduta_segno_v2.tick_var(..., N, ...)` sulla scena `L 162`, **non** col tick di `mitosi_rami_v2.ciclo`.

### C: IL CORPO FUSO CON LE NASCITE ACCESE -- LE SCELTE APERTE

- **C-0, IL CONTATORE (misurato).** In `d1L/stato_018000`, la partenza scritta nella lettera:
  - `max |Theta| = 11.42`;
  - **1596 archi** hanno gia' `|Theta| > 2 pi` (7666 sopra `pi`);
  - per confronto: `0` archi a `k 0` (`d1`), `0` a `6000`, `35` a `d1L/12000`, `13309` a `d1T_r/54000`.
  - **Con le nascite accese da quello stato**, 1596 archi sono scattati al primo tick, la coda d'attesa supera 500 e il verdetto C4 e' **INGOLFAMENTO al tick 1**. Il caso noto K1 della lettera («nessun arco scattato nei primi 250 tick») non si puo' fare.
  - **Le vie:**
    - (a) il contatore `Theta` si rimette a zero a `k 18000`: le nascite contano da li', come il tronco contava dal suo inizio. **E' una scelta di fisica**;
    - (b) si parte da uno stato prima che un arco superi `2 pi` (fra `d1/6000` e `d1L/12000`), ma non e' il corpo fuso: a `k 6000` i corpi sono ancora due;
    - (c) si accetta l'ingolfamento come risultato.
- **C-1, `chi` e `pi` del nodo nato.** `chi` e' un campo dinamico (il passo v2), quindi il nato deve avere un `chi` e un `pi`. **E' un numero da scegliere**, cosa che `A1` vieta senza una derivazione. I candidati sono:
  - la media dei due estremi dell'arco che si spezza, con `pi` uguale alla loro media;
  - il profilo statico ricalcolato;
  - zero.
- **C-2, l'energia della regola.** `regola` sceglie il flip che rende minima `H` di `energia_corsa`, senza `chi`. Con `chi` acceso, la `H` della scelta e il `DH` della nascita, e quindi `E_persa`, includono `H_chi` (`chi_tick_v2.energia_chi_v2`) oppure no?
- **C-3, la scena.** Le nascite sono scritte e collaudate sulla scena `L 186`, il corpo fuso vive su `L 162`. **Non ho verificato** che `Rami`, `regola` e `applica` girino su `L 162` senza toccarli: lo verifico a secco prima di ogni corsa, ma solo dopo C-0..C-2.
- **C-4, `geo.U` del nato.** La ripresa v9 riscrive `geo.U` da `chi` (`scrivi_U`). Dopo una nascita `U` va ricalcolata sul grafo nuovo, e questo segue da C-1.

### F: LA NASCITA NEL VUOTO CON IL LAPSE DIPINTO -- LE SCELTE APERTE

- **F-1, la scena.**
  - **(a)** il vuoto della mitosi, `M0237/vuoto/vuoto_35976.npz` su `L 186`, con il tick di `mitosi_rami_v2.ciclo`: bisogna far entrare `N` dipinto in quel tick, **che oggi non lo prevede**;
  - **(b)** un vuoto equivalente su `L 162`, la scena di [M2210], con `tick_var`: bisogna far entrare le nascite in quel tick.
  - **Tutte e due sono un'integrazione nuova:** nessuno dei due tick ha l'altra meta'.
- **F-2, l'ampiezza.** «La stessa ampiezza usata per la caduta della materia»: se la scena e' `L 186` e non `L 162`, si tiene la stessa `A`, oppure lo stesso gradiente `G20`, con `A = G20 L_y / (2 pi kappa)`, che dipende da `L`?
- **F-3, `N` del nodo nato:** **la propongo derivata**, cioe' la stessa formula del seno calcolata nella posizione del nato. Non e' un numero nuovo.
- **Il controllo con il lapse piatto** (= [M0106], 0 nascite, al bit sui primi 250 tick) vale solo con la via F-1 (a). Con (b) il riferimento al bit non esiste.

**Finche' Luca non decide C-0..C-2 e F-1..F-2, non si scrive codice per C ne' per F.**


## C, LA VIA (d): LA COPPIA DA k 0 CON chi E LE NASCITE ACCESE *([M0026], DECISIONE DI LUCA 2026-11-28 `00:26`; il task history `doc/TASK_HISTORY/2026-11-28_m0026_corpo_fuso_nascite.md`; scritta PRIMA del codice)* [[PROGETTO-MITOSI]]

**La scena e la partenza sono quelle di `d1`:** la semina di `M2034/coppia/d1/stato_000000`, `chi` acceso (il passo v2), `Theta = 0` a `k 0`.
- **Le nascite:** la via vera della mitosi, con il quanto `2 pi`: `Rami.nasci` riga per riga, il campo orientato, una nascita per tick. Due cambi decisi da Luca:
  - **C-1:** `chi` e `pi` del nato sono la media dei due estremi dell'arco;
  - **C-2:** l'energia della regola, del P9 e di `DH` e' `energia_chi_v2`, cioe' con `H_chi`.
- **Le mie scelte dentro il mandato** (dichiarate):
  - il campo si converte (prototipo -> generico -> orientato dal toro) **solo alla prima nascita**, cosi' K1 non la tocca;
  - la `H` del candidato si **ricalcola** con `energia_chi_v2` sul motore e sul campo che `MR2.candidato` costruisce: la funzione si chiama com'e', e la sua `H` del libro dei conti resta come `H_libro`;
  - `H(k)` si calcola ogni 250 tick.
- **La corsa:** 18000 tick, gli stati ogni 250 in `E:/soliton_simulator/controllo/M0026/C`, la serie ogni 10 come `d1`, e `nascite.json`.

**I casi noti** (`corpo_fuso_mitosi.py noto`):
- **K-pre:** lo stato costruito a `k 0` = `d1/0` AL BIT;
- **K0:** le nascite spente, 250 tick = `d1/250` AL BIT; **K0-neg:** contro `d1/500` DEVE FALLIRE;
- **K-nascita:** da `d1L/18000`, una nascita sull'arco di `|Theta|` massimo:
  - P9 entro `1e-12` con l'energia di `chi`;
  - il grafo ha `n + 1` nodi e `m + 3` archi, e `chi`, `pi`, `theta_a` e `Lp` lo seguono;
  - `chi` e `pi` del nato sono la media AL BIT;
  - F3 regge, `C.residuo()` gira, e un tick dopo la nascita gira.
- **K1** e' dentro la corsa: a `k 6000` nessuna nascita, e lo stato = `d1/6000` AL BIT. **Altrimenti FERMO.**
- **Se un caso noto fallisce: FERMO.**

**Le letture e il verdetto** (C4 di [M2245-27], sul tratto `6000-18000`):
- sulla griglia di S1: A0, `R`, `max rho`, `w`, `chi` al centro, `H` e `H_chi`;
- **le nascite:** quante, quando (durante l'urto, intorno a `k 3000`, oppure dopo) e dove (la distanza dal baricentro della nube nel momento della nascita, per anello); `E_persa(k)` e `H + E_persa`;
- **il respiro di `R` su `[15500, 18000]`**, contro `d1L` sullo stesso tratto.

**IL VERDETTO** (le soglie sono di Luca):
- **SI RAFFREDDA FACENDO SPAZIO** se nascono nodi entro `2 R` dal baricentro **e** il respiro di `R` su `[15500, 18000]` e' sotto la meta' di quello di `d1L`;
- **FA SPAZIO MA NON SI RAFFREDDA** se nascono, ma il respiro resta sopra la meta';
- **NON FA SPAZIO** se non nasce niente;
- **INGOLFAMENTO** se gli archi in attesa superano 500 o se un triangolo degenera: **FERMO**, dichiarato.

**LE PREVISIONI:**
- **del guardiano:**
  - le prime nascite fra `k 2500` e `4000`, entro `2 R` (`65%`);
  - il respiro sotto la meta' (`45%`);
  - nessun ingolfamento (`60%`);
- **mie:**
  - **le prime nascite dopo `k 6000`** (`80%`): `max |Theta|` vale `1.50` a `k 3000` e `2.65` a `6000` in `d1`, che ha la stessa dinamica fino alla prima nascita. **E' contro la prima previsione del guardiano;**
  - **un ingolfamento prima di `k 18000`** (`40%`): in `d1L` gli archi oltre `2 pi` passano da 35 (`k 12000`) a 1596 (`k 18000`), e una nascita per tick potrebbe non stare al passo;
  - il respiro sotto la meta' (`30%`).


## F, LA VIA (a): LA NASCITA NEL VUOTO CON IL LAPSE DIPINTO DENTRO IL TICK DELLA MITOSI *([M0026], DECISIONE DI LUCA 2026-11-28 `00:26`; scritta PRIMA del codice)* [[PROGETTO-MITOSI]]

**La corsa** e' quella del vuoto di [M0106]: `mitosi_rami_v2.ciclo` da `M0237/vuoto/vuoto_35976.npz`, su `L 186`, senza materia, con `chi` spento e le nascite accese, per 6000 tick fino a `k 41976`, con gli stati ogni 250 in `controllo/M0026/F`.

**Il lapse dipinto nel tick** (la mia forma, dichiarata):
- durante la corsa `tick_lapse.N_di(rho, legge)` diventa `N_di(rho, legge) * N_dip(x)`, e `Np_di` diventa `Np_di * N_dip(x)`;
  - `N_dip = exp(-kappa chi_dip)`, con `chi_dip = A sin(2 pi (y - y_c) / L_y)`, cioe' la forma di `caduta_libera.campo_N`;
  - `y = m2 sqrt(3)/2` dei nodi della scena, che si cattura avvolgendo `convergenza.scena_L`.
- **Nel vuoto la materia e' zero, quindi `N_di = 1` e il lapse E' quello dipinto.** Con `A = 0` il fattore e' `1.0` esatto, quindi la corsa e' quella di [M0106] bit per bit (K-F0).
- **Il nodo nato** (la chiamata su un solo valore dentro `applica`): `N_dip` si calcola nella posizione di `posizioni.nuova(m1, m2, i, j, L)`, cioe' e' derivato (F-3).
- **L'ampiezza:** lo stesso gradiente `G20` di [M2210] (F-2): `A = G20 L_y / (2 pi kappa)`, con `L_y = 186 sqrt(3)/2`.
- **`y_c = 0`:** e' una fase, e la dichiaro.

**I casi noti** (`vuoto_lapse_mitosi.py noto`):
- **K-F0:** con `A = 0`, da `35976` a `36250` lo stato e' uguale AL BIT a `M0237/vuoto_v2/stato_36250` ([M0106]);
- **K-F1:** con `A` vero, DEVE FALLIRE;
- **K-F2:** `N_dip` sui nodi e' uguale AL BIT a `caduta_libera.campo_N` sulla stessa scena.
- **Se un caso noto fallisce: FERMO.**

**Le letture** (a corsa chiusa):
- nascite si' o no, a quali `k`, e **dove rispetto al seno**: il fondo del pozzo (`chi_dip` minimo, `N` massimo), i fianchi o la cima;
- `rho_phi` e `J_phi` per fascia di `y` (il vuoto cade nel seno?), la norma e `H`.

**IL VERDETTO:** NASCE (e dove) / NON NASCE.

**LE PREVISIONI:**
- **del guardiano:** nessuna nascita (`55%`); se nasce, sui fianchi;
- **mia:** **NON NASCE** (`65%`). Il lapse dipinto e' statico, e in un vuoto senza materia `Theta` cresce con le differenze di `cs` fra i due estremi di un arco, che sono piccole (il gradiente `G20` per un arco). Se nasce, nasce **sui fianchi**, dove il gradiente di `N` e' massimo (`70%` condizionato).


## G, «A E' GIA' LA FASE DI phi?»: LA LETTURA INVARIANTE SULLE PLACCHETTE *([M0037-28], DECISIONE DI LUCA 2026-11-28 `00:37`; scritta PRIMA dello script)* [[PROGETTO-MITOSI]]

**L'etichetta:** la lettera e' [M0037]. L'etichetta era gia' usata (`[M0037-03]`), quindi la scrivo **[M0037-28]**, per la regola di Luca delle 23:14.

**Le definizioni** (quelle della lettera):
- **`f = phi_h.reshape(m, 2)`**;
- **`theta_a = arg(f[a,1] conj f[a,0])`**, ridotto in `(-pi, pi]`. Gli archi con `min |f[a,.]| < 1e-6` si scartano, e si contano;
- **`Phi_p = wrap(somma_c S[p,c] theta[P[p,c]])`**: la circolazione per placchetta;
- **`eB_p = e B()[p]`**: `P`, `S` e `B()` vengono dal campo `_u1_prototipo.Campo` costruito da `porto.campi` sulla scena del triangolo, con l'`A` e l'`E` dello stato;
- **mai A nudo contro theta nudo.**

**LE DICHIARAZIONI (G-0):**
- **(a) `hop_phi` NON usa `geo.U`.**
  - `flussi_parziali.hop_phi` chiama due volte `_hop_phi_mezzo` e poi moltiplica per `conj(z_arco)` sulle due estremita';
  - `_hop_phi_mezzo` fa `v = phi.reshape(m, 2)` con `alpha I + beta S`, dove `S` e' la permutazione pura («il vuoto e' NEUTRO»);
  - `z_arco` dipende solo da `s_arco` (`theta = pi s_arco f`);
  - nel motore `_spostamento_scalare` chiama `FP.hop_phi` («senza trasporto»). **Il test ha il senso che dice la lettera.**
- **(b) L'ordine delle estremita':** `_hop_phi_mezzo` usa `phi.reshape(m, 2)` e il motore ha `inc.nodo = [ii_0, jj_0, ii_1, jj_1, ...]`, cioe' `ii = nodo[0::2]` e `jj = nodo[1::2]`. **Quindi `f[a,0]` sta all'estremita' in `ii[a]` e `f[a,1]` in `jj[a]`.** `phi_h` ha `157464 = 2 x 78732` valori.
- **(c) Gli stati** (`max |A|`, `rms A`, misurati):

  | stato | `max abs(A)` | `rms A` |
  |---|---|---|
  | (i) `M0414/puntofisso_accoppiato/giro_3/stato_006000` (l'ultimo; `partenza_giro_4` da' gli stessi numeri) | `1.0317e+03` | `1.8076e+02` |
  | (ii) `M2034/coppia/d1/stato_003250` | `8.2738e+01` | `1.7447e+01` |
  | (ii) `M2034/coppia/d1L/stato_018000` | `5.7796e+02` | `1.0569e+02` |

  - **Per (ii) la lettera chiede `k 3230`, che non e' salvato:** gli stati sono ogni 250. **Uso `3250`**, che e' dentro l'urto (A0 a 3000 e 3500 dice ALTRO, a 3250 UNO), e lo dichiaro.
  - **(iii) Il vuoto fresco senza oggetto** e' `c phi_v` della scena, con `A = 0`. **E' anche il caso noto K3** («campo nullo»); su di lui si stampa comunque `rms Phi`.
- **(d) LA MIA PREVISIONE:** **SI' al `20%`.**
  - `phi` non sente `U`, mentre `A` ha per sorgente la corrente di `psi`. Una somiglianza puo' passare solo per `psi`, che sente tutti e due: `phi` lo sente attraverso `CAMM-MATERIA-VUOTO`, `A` attraverso la sorgente.
  - Il vento del vuoto e' radiale (A5), mentre la circolazione `B` di una corrente radiale e' piccola, quindi mi aspetto correlazioni deboli.
  - Sul vuoto fresco: `rms Phi` **zero entro l'arrotondamento** (`60%`), perche' `phi_v` e' uniforme fra le estremita' di un arco. E' contro la previsione del guardiano.

**I casi noti (prima di ogni numero sugli stati):**
- **K1:** le estremita' di ogni nodo per `e^{i chi_v}` a caso lasciano `Phi_p` invariato, modulo `2 pi`, entro `1e-10`;
- **K2:** `A -> A + (chi_j - chi_i)` lascia `B` invariato entro `1e-12`;
- **K3:** con `A = 0` lo script dice «campo nullo» e non calcola la correlazione;
- **K4:** su 200 permutazioni, `|Spearman| < 0.1` almeno nel 95% dei casi.

**Le letture, in quest'ordine:**
1. per stato, PRIMA `max abs(eB)`, `rms eB`, `max abs(Phi)`, `rms Phi` e gli archi scartati;
2. poi Pearson e Spearman su tutte le placchette e per anello di 8 dal centro di massa di `rho_psi`. La posizione di una placchetta e' la media degli scarti dei nodi `ii` dei suoi tre archi;
3. il nullo con 200 permutazioni (media e 2 sigma);
4. «entro 2 raggi»: `R = sqrt(somma rho r^2 / somma rho)`, come A0.

**IL VERDETTO** (le soglie sono di Luca):
- **SI'** se `|Spearman| > 0.5` entro `2 R`, fuori dalle 2 sigma del nullo, in almeno 2 stati su 3;
- **NO** se `|Spearman| < 0.2` in tutti;
- **ALTRO** in mezzo, oppure se il segno cambia fra gli anelli, e si scrive dove.


## D-P3, PRIMA DEL CODICE: EOTVOS CON GLI AGGREGATI -- LE SCELTE APERTE *([M0026], DECISIONE DI LUCA 2026-11-28 `00:26`, punto D; scritta il 2026-11-28 alle `01:12`, PRIMA di ogni riga di codice; C ed F stanno girando)* [[PROGETTO-MITOSI]]

**Che cosa chiede la lettera:**
- il triangolo sinistro, seminato come specchio del destro (le fasi `0, -2 pi/3, -4 pi/3`). Il caso noto: a `k 0` il giro e' `-1`, e `J_theta` e' l'opposta del destro entro `1e-9`;
- destro e sinistro affiancati (carica totale zero), accanto a un oggetto M, nel seno dipinto, per 6000 tick;
- nella prima finestra la stessa accelerazione all'1%.

**Che cosa ho letto:**
- la caduta nel seno dipinto e' quella di [M2210] (`eotvos_v2.caduta`, `caduta_libera`):
  - la scena del triangolo `L 162`, senza bordo, con un francobollo `L162` incollato;
  - `chi` dipinto e statico, `N = exp(-kappa chi)`, con `y_c` sull'oggetto (lo zero del seno, dove il gradiente e' massimo);
  - il tick e' `caduta_segno_v2.tick_var(..., N, cs_N, segno)` nella forma V2 o V3;
  - l'accelerazione e' il fit di `y` del baricentro su `k 0..2000`, ogni 250;
- i triangoli di [M0333] e [M0222] hanno il lato 39 (`R` circoscritto `22.52`) sulla stessa scena.

**LE SCELTE APERTE:**
- **P3-1, lo spazio.** La scatola e' `162 x 140` nodi.
  - Due triangoli (ognuno largo circa `2 x (22.5 + 6)`) e un oggetto M **non ci stanno separati di piu' della portata delle loro forze**. Due triangoli da soli si', con i centri a `81` in `x` e circa 23 nodi di vuoto fra loro.
  - **Le vie:**
    - (a) **due corse nello stesso seno**, come `eotvos_v2` ha fatto per le masse 1 e 4: M da solo (la caduta di [M2210]) e l'aggregato destro + sinistro da solo;
    - (b) una scena piu' grande;
    - (c) triangoli piu' piccoli. **(b) e (c) sono una scena nuova.**
- **P3-2, la geometria del seno.** I francobolli di un triangolo stanno fino a `+-22` in `y` dal baricentro, e `L_y = 140`.
  - Il gradiente medio che l'aggregato sente e' `<cos(2 pi dy / L_y)>`, pesato con le masse, volte quello al centro. **E' circa qualche percento in meno**: l'avevo calcolato a mano come «0.95-0.98», e **non ha provenienza** (va calcolato dallo script).
  - **Un confronto grezzo all'1% fallirebbe per pura geometria.** Il confronto onesto e' `a_aggregato / a_M` contro la previsione geometrica, cioe' la media pesata del gradiente sulle posizioni dei francobolli, con l'1% sullo scarto da quella previsione.
- **P3-3, la forma:** V2 (`cs = s N`, senza la fase (a)) oppure V3 (`cs = s`, con la fase (a) `+`), le due di `eotvos_v2`. Quale e' «il seno dipinto» di P3?
- **P3-4, il punto fisso del sinistro:** [M0016] chiedeva il sinistro «con il suo punto fisso con `chi`», [M0026] solo «seminato come specchio». **Lo semino a `k 0` con `prepara`, le fasi rovesciate e nessun punto fisso**, a meno che Luca non dica altro.

**Finche' Luca non decide P3-1..P3-3, non si scrive codice per P3.**

### D-P3, IL SEGUITO: LE SCELTE DECISE ([M0141], DECISIONE DI LUCA 2026-11-28 `01:41`), G CALCOLATO, K1 FALLITO *(scritta DOPO lo script: e' un errore mio di ordine, dichiarato)*

- **Le scelte decise:**
  - **P3-1:** via (a), due corse nello stesso seno (M da solo, l'aggregato da solo, con i centri a 81 in `x`);
  - **P3-2:** il criterio geometrico, `|a_agg/a_M - G_agg/G_M| < 1%`;
  - **P3-3:** la forma V2;
  - **P3-4:** il sinistro seminato a `k 0` con le righe di `prepara`, le fasi `0, -120, -240` e i vertici del destro `+81` in `m1`.
- **G, calcolato** (`eotvos_aggregati.py noto`, il referto `eotvos_aggregati_noto_fallito.txt`):
  - la formula: `G = somma_i m_i dN/dy(y_i) / (somma_i m_i dN/dy(y_c))`, con `dN/dy = -kappa A (2 pi/L_y) cos(2 pi (y - y_c)/L_y) N(y)`, `y_i` il baricentro del francobollo `i` da solo e `m_i` la sua massa;
  - `A 13.89741`, `L_y 140.296115`, `y_c 68.685473`;
  - i francobolli 0, 1, 3, 4 stanno a `y - y_c = -10.0617`, con il gradiente relativo `0.901559`; i francobolli 2 e 5 a `+23.7133`, con `0.485630`;
  - **`G_agg = 0.762915668679`** e **`G_M = 1`** (K4).
- **K1 FALLISCE:**
  - i giri sono giusti: il destro `+1`, il sinistro `-1`;
  - ma `J_theta` del sinistro **non** e' l'opposta del destro: `[0, R/2)` `-10.148` contro `+13.115`, `[R/2, R)` `-4.751` contro `+4.718`, `[R, 3R/2)` `-0.155` contro `-0.112`; `max |J_s + J_d| = 2.967`, contro la soglia `1e-9`;
  - **la mia ipotesi, non verificata:** il francobollo `L162` ha una sua fase interna, e quindi una corrente sua, che il cambio di fase fra i francobolli non rovescia. Il sinistro della lettera percio' **non e' lo specchio del destro**.
- **K2 PASSA:** la carica topologica e' `+1 - 1 = 0`. `e somma rho = 373.19` e' la massa; la sorgente di Gauss somma a `5.3e-14`.
- **K3:** dichiarato, perche' il confronto AL BIT con [M0222] non e' definito.
- **La regola:** **un caso noto fallito, quindi FERMO su P3.** Le corse di P3 non vanno in coda.


## C, LA CURA DEL FLIP ILLEGALE E LA LETTURA SU 0-16250 *([M1013], DECISIONE DI LUCA 2026-11-28 `10:13`, dalla posta, guardiano `20860a72`; scritta PRIMA del codice della cura e dello script della lettura)* [[PROGETTO-MITOSI]]

### C-1, LA CURA: il caso, la condizione, perche' non cambia la fisica
- **Il caso** *(la caduta `9038a3b3`, nascita `652` a `k 16487`)*. Il nato `n` si collega a `i, j, k, l`; il flip del lato `x - y` *(uno dei quattro: `i-k`, `j-k`, `j-l`, `i-l`)* toglie `x - y` e aggiunge `n - m`, dove `m` e' l'altro vicino comune di `x` e `y`. Se `m` e' gia' vicino di `n`, oppure e' gia' collegato a un vicino di `n` diverso da `x` e `y`, il grafo nuovo ha un 3-ciclo con `n` che NON e' una faccia, e `CampoOrientato._placchetta` si ferma.
- **La condizione (esatta, puramente topologica):** il flip `x - y` e' LEGALE se e solo se **`m` non e' gia' vicino di `n`** e **i vicini comuni di `n` e `m`, dopo il flip, sono esattamente `{x, y}`**. Le uniche facce nuove che il flip crea contengono l'arco `n - m`: non serve guardare altrove.
- **Perche' non cambia la fisica** *(la DECISIONE 1)*: e' la condizione perche' il grafo resti una triangolazione, che la regola presuppone. Se tutti e quattro i flip sono legali, il codice percorso e' quello di prima, riga per riga; il controllo non calcola nessuna energia.
- **Dove sta:** una funzione pura `flip_illegale(ii2, jj2, n, x, y)` in `mitosi_regola_v2.py`, che nessuno chiama per omissione *(byte-inerte per i sigilli vecchi)*. Il controllo si fa in `corpo_fuso_mitosi.py` PRIMA di `MR2.regola`, con il contatore `rifiuti_flip_illegale` nel registro delle nascite e nello stato. **`primo_ordine/` non si tocca.**
- **I casi noti** *(un grafo piccolo costruito a mano)*:
  - (CF1) una stella regolare, tutti i flip legali: la funzione dice legale, e il candidato e' identico a quello senza controllo AL BIT;
  - (CF2) un vertice di grado 3 dopo la nascita *(il 3-ciclo separante)*: illegale;
  - (CF3) `m` gia' vicino di `n` *(l'arco doppio)*: illegale;
  - (CF4, DEVE FALLIRE) la stessa funzione con il controllo dei vicini comuni tolto non vede CF2.
- **Il contro-caso sul grafo vero:** su `stato_016250` *(602 nascite, 53692 triangoli, tutti facce, nessun arco doppio: contato con uno script in questo giro, prima della carta)* le nascite di `nascite.json` rigiocate solo nella topologia non devono avere nessun flip illegale fino a 602.

### ### LA DOMANDA APERTA PER LUCA (la premessa caduta)
**La DECISIONE 1 dice «come negli altri casi di rifiuto gia' previsti dalla regola»: nella regola NON ce n'e' nessuno.** Gli unici «rifiuta» del codice sono la ripresa con lo sha1 sbagliato. Il ciclo di C fa nascere UN arco per tick, `sc[0]` *(l'indice piu' basso fra gli scattati)*. Le tre vie:
- **(R1, la mia proposta)** la nascita intera rifiutata e contata; nello stesso tick si prova il prossimo arco in attesa (`sc[1]`, ...); l'arco rifiutato riprova ai tick dopo;
- **(R2, la lettera stretta)** un solo tentativo per tick: l'arco rifiutato resta `sc[0]` e blocca gli altri finche' il suo intorno resta illegale *(`ATTESA_MAX 500` fa da freno)*;
- **(R3)** si scarta solo il lato illegale dai quattro candidati del flip, e la nascita avviene con gli altri: l'arco NON resta in attesa.
**Fino a `k 16487` le tre vie danno lo stesso log AL BIT**: divergono solo dopo. **La ripresa (C-2) aspetta la scelta.**

### C-3, LA LETTURA SU 0-16250 (le letture fissate PRIMA dei numeri)
- **Le fonti:** `M0026/C/nascite.json` *(602 nascite fino a 16250)*, gli stati ogni 250, le righe «k ...: ... H ..., E_persa ...» del log *(ogni 250)*. `serie.json` NON c'e': la corsa e' caduta su un'asserzione, non su `Fermo`.
- **Il ritmo:** le nascite per bin di 250 tick dalla prima *(k 11588)*; due modelli a due parametri, la retta `a + b k` e l'esponenziale `A exp(k / tau)`, adattati con la verosimiglianza di POISSON *(i conteggi sono conteggi)*. Vince quello con la devianza piu' bassa; con due parametri ciascuno il confronto e' diretto. Se la differenza di devianza e' < 2, scrivo «NON DECIDIBILE».
  - (L1) dati sintetici esponenziali: vince l'esponenziale, `tau` entro il 5%;
  - (L2) dati sintetici lineari: vince la retta.
- **L'energia:** `H`, `E_persa` e `H + E_persa` ogni 250 contro il numero di nascite. La lettura: `H + E_persa` costante entro l'1% della variazione di `H` = «come nella fiammata»; altrimenti il tick non conserva e lo scrivo.
- **Il corpo, ogni 1000 dal 11000:** `R` *(il raggio quadratico medio di `rho_psi` dal centro periodico, `TO.centro`)*, `max rho_psi`, `max |chi|`. Le posizioni dei nodi vecchi sono quelle del primo stato con le nascite *(i nodi del toro non si muovono)*. (L3) `R` di `stato_011000` calcolato con le posizioni di `stato_011750` = quello con le posizioni della scena, AL BIT.
- **Il raggio della nascita:** `r` di ogni nascita contro `k`, per bin di 1000: mediana, massimo, e la frazione entro `2 R` *(il primo criterio di C4)*.
- (L4) il numero delle nascite di `nascite.json` = `meta["nascite"]` di `stato_016250` = le righe «[nascita ...]» del log con `k <= 16250`.
- **Il respiro C4 su `[15500, 18000]` NON si legge qui:** solo dopo la ripresa.

## D-P3, LA CARTA CORRETTA: IL SINISTRO VIA (b), K1 RIDOTTO *([M1013], DECISIONE DI LUCA 2026-11-28 `10:13`, punto 4, dalla posta, guardiano `20860a72`; scritta PRIMA della modifica di `eotvos_aggregati.py`)* [[PROGETTO-MITOSI]]

- **Il sinistro:** le fasi rovesciate `0, -2 pi/3, -4 pi/3` sui vertici del destro `+81` in `m1`, come in `f123414a` *(la via (b))*. **Nessuno specchio esatto.**
- **K1 ridotto:** a `k 0` il giro del destro e' `+1` e quello del sinistro `-1`, entro `0.1` *(il caso noto di `triangoli_vortice.Geo.giri`)*. **`J_theta` per anello del destro e del sinistro si STAMPA e non decide nulla** *(in `f123414a`: il sinistro -10.148 / -4.751 / -0.155 contro il destro +13.115 / +4.718 / -0.112: NON opposti, perche' i vertici traslati non sono la riflessione)*.
- **K2** *(la carica topologica 0)*, **K3** *(dichiarato)*, **K4** *(`G_M` entro `1e-3` da 1)* e **K5** *(nella corsa di M: gli stati `0..2000` = `CHI/caduta/V2` AL BIT)*: come gia' scritti.
- **G, la provenienza:** `G_agg = 0.762915668679` e `G_M = 1` sono calcolati da `eotvos_aggregati.py noto` *(`G_di`, la media pesata con le masse di `dN/dy` sui baricentri dei sei francobolli, diviso `dN/dy(y_c)`)*, nel referto `eotvos_aggregati_noto_fallito.txt` di `f123414a`. Il noto rifatto li ricalcola, e devono uscire **identici**.
- **La marea** *(UNA riga nel referto)*: per ogni francobollo `dN/dy(y_i) / dN/dy(y_c)`, con il minimo e il massimo calcolati dallo script *(la lettera dice 0.49 e 0.90: lo script li ricalcola)*. **Il test misura una media su un corpo esteso.**
- **Il verdetto:** `|a_agg / a_M - G_agg / G_M| < 1%` sulla finestra `0..2000`, come in [M0141].
- **Le corse M** *(fino a 6000)* **e agg** vanno in coda DOPO la ripresa di C, nel tetto dei 10. **La ripresa aspetta la scelta R1/R2/R3, quindi le due corse di P3 aspettano con lei.**

## C, R3 E LA RIPRESA DA 16250 *([M1056], DECISIONE DI LUCA 2026-11-28 `10:56`, dalla posta, guardiano `066e045f`; sostituisce la DECISIONE 1 di [M1013]; scritta PRIMA del codice)* [[PROGETTO-MITOSI]]

### R3, COME LO DICE IL CODICE
- **La nascita senza flip e' GIA' un esito della regola** *(`mitosi_regola_v2.regola`)*. La regola calcola il candidato `nas` *(nessun flip)* e i quattro flip; se i due flip migliori distano meno di `GUARDIA |H|` sceglie `nas` *(`scelto = -1`)*. La contabilita' *(`E_persa -= H1 - H0`)* e' la stessa per ogni esito. **Quindi il flip e' parte della regola, e la nascita senza flip e' consentita dalla regola e dalla contabilita'.** Con i quattro lati illegali la nascita si fa con `nas`. **`nascite_rifiutate` resta 0 per costruzione**, e il contatore c'e' lo stesso.
- **`regola_r3`** *(nuova in `mitosi_regola_v2`; `regola` non si tocca)*: `nas` come prima; i lati illegali *(`flip_illegale` sul grafo di `nas`)* NON si calcolano; sui legali, la stessa scelta di `regola`:
  - **con due o piu' legali:** `argsort` stabile, il `gap` fra i due migliori, `pari -> nas`;
  - **con UN solo legale:** e' quello *(non c'e' un secondo con cui fare il `gap`: una scelta di lettura, dichiarata qui)*;
  - **con nessuno:** `nas`.
  - `scelto` resta l'indice nei QUATTRO lati di sempre. Con tutti legali `regola_r3` = `regola` AL BIT.
- **I contatori nel registro:** `lati_scartati` *(quanti, e quali)* per nascita, `nascite_senza_flip` *(solo quelle con i quattro illegali)*, `nascite_rifiutate` *(0)*. Quando un lato e' scartato si stampa una riga IN PIU' dopo la riga della nascita: **la riga della nascita resta quella di sempre**, cosi' il confronto col log vecchio e' diretto.
- **Un fatto dal grafo, non una scelta** *(per CF5')*: in una triangolazione i lati illegali vengono **A COPPIE**. Un vertice `x` della stella di grado 4 dopo la nascita rende illegali i flip `x - k` e `x - l` *(il 3-ciclo)*; uno di grado 3 li rende illegali tutti e due *(l'arco doppio)*. **«Un solo lato illegale» non nasce da un grafo vero:** CF5' si prova sulla logica di scelta, con `flip_illegale` e `candidato` sostituiti da stub.
- **I casi noti** *(`regola_r3_noto.py`, con gli stub, nessun motore)*:
  - (CF5') un lato illegale: la nascita avviene, e il flip e' il migliore fra i tre legali;
  - (CF6') quattro illegali: `nas`, `nascite_senza_flip` +1;
  - (CF-eq) tutti legali: `R` e `S` di `regola_r3` = quelli di `regola` AL BIT;
  - (CF-coppie) sul grafo costruito a mano col vertice di grado 4, `flip_illegale` scarta esattamente i due lati di quel vertice.

### LA RIPRESA C-2
- **Da `M0026/C/stato_016250.npz`**, la scena di C *(`V6.GD.TC.scena`, `V6.costruisci`, `D.parametri` come a `k 0`, poi `converti`)*, e il grafo, il motore e il campo ORIENTATO ricostruiti dallo stato *(le righe di `mitosi_rami_v2.riprendi_v2`, il ramo «stato della v2»)*:
  - `mot.cresci` dei sopravvissuti del toro;
  - `CampoOrientato` da `ori_cicli`, con `A` ed `E`;
  - `chi`, `pi`, `theta_a` *(lo stesso oggetto di `cont.theta`, come nella corsa)*, `gauss_acc`;
  - `E_persa` e `nascite` da `meta`, il registro da `nascite.json`, `m1` e `m2`.
- **`mot.cs` non si salva perche' non serve:** `tick_chi_v2` lo ricalcola da `chi` all'inizio di ogni tick *(`mot.cs = P.s * N`)*. **`C.residuo()` e' una misura senza effetti.**
- **(K-R, prima della ripresa vera)** da `stato_016000` per 250 tick con `regola_r3` *(40 nascite, tutte legali)*: lo stato a `16250` = `M0026/C/stato_016250` AL BIT *(ogni chiave, `campo_A`, `campo_E`, `chi`, `pi`, `theta_a`, `gauss_acc`, `ii`, `jj`, `ori_cicli`, `m1`, `m2`)*, e le 40 nascite = quelle di `nascite.json` *(k, nodi, DH)*. **Se K-R fallisce: FERMO**, e la ripresa non parte.
- **La ripresa vera:** da 16250 a 18000 con `regola_r3`, in `M0026/C_R3` *(cartella nuova: `M0026/C` resta com'e')*, dalla coda.
  - **DEVE:** le righe «[nascita q]» per q da 603 a 651 sono IDENTICHE a quelle di `M0026_C.txt` *(il testo, senza i secondi fra parentesi)*, altrimenti FERMO; alla 652 si scrive il lato scartato e il flip fatto.
  - `serie.json` della ripresa contiene SOLO il tratto ripreso.


## IL VIDEO DI C *([M1020], DECISIONE DI LUCA 2026-11-28 `10:20`, dalla posta, guardiano `f711b008`; scritta PRIMA dello script)* [[PROGETTO-MITOSI]]

- **Lo script** `doc/referti_l2/anima_corpo_fuso_nascite.py` *(sullo schema di `anima_coppia_v4.py`; nessun tick)*. I quadri sono gli stati di `M0026/C` ogni 250, da `k 10000` a `16250` *(26 quadri)*. Con `--fino 18000 --da-r3`, a ripresa chiusa, gli stati dopo 16250 vengono da `M0026/C_R3`, con lo stesso script.
- **Tre pannelli** attorno al centro periodico di `rho_psi` *(finestra `+-32`)*:
  - `log10 rho_psi`, a scala fissa;
  - `chi`, a scala fissa;
  - il RETICOLO: gli archi con i due estremi entro `r 30`. I nati sono ACCESI *(giallo)* nel quadro in cui nascono, poi CIANO; i nodi del toro sono grigi.
- **In sovrimpressione:** `k`, le nascite cumulate al fotogramma, `R`, `max rho_psi`, `E_persa`.
- **Il tempo delle nascite:** ogni quadro dura 2 s *(60 fotogrammi a 30 fps)*. La nascita con `k_b` nell'intervallo `(k - 250, k]` si accende al fotogramma `ceil(60 (k_b - k + 250) / 250)` del quadro, quindi in ordine, e si vede il ritmo.
- **Le dichiarazioni:**
  - il reticolo del pannello e' quello dello stato a `k`: gli archi dei nati dell'intervallo ci sono gia' dal primo fotogramma *(una semplificazione)*;
  - gli archi che attraversano il bordo periodico *(lunghi piu' di 3)* non si disegnano.
- **Il formato:** `1280 x 720`, 30 fps, un fermo di 3 s sul primo e sull'ultimo quadro, la scritta in alto di Luca.
- **Che cosa va in git:** il video NO *(`*.mp4` e' in `.gitignore`)*; il PNG dell'ultimo quadro si'.
- **Il caso noto:** i nodi in evidenza nell'ultimo fotogramma *(contati sul registro, anche quelli fuori dalla finestra)* = le nascite del log con `k <=` l'ultimo `k` = `meta["nascite"]` dello stato.


## H-1, IL CONTO DEL DIFETTO DI FLUSSO DELLE NASCITE DI C *([M1058], DECISIONE DI LUCA 2026-11-28 `10:58`, punto 1, dalla posta, guardiano `d8fdb104`; scritta PRIMA dello script; a costo zero, nessun tick)* [[PROGETTO-MITOSI]]

### LE DEFINIZIONI
- **L'angolo d'arco** come in G *(`fase_vuoto_vs_A`)*: `theta_a = arg(f[a,1] conj f[a,0])`, con `f = phi_h.reshape(m, 2)`; si scartano gli archi con `min |f| < 1e-6`.
- **La placchetta** e' ogni 3-ciclo del grafo *(sul toro e sui grafi di C, con 0 flip illegali, i 3-cicli SONO le facce: `16615729`)*. `Phi_p = wrap(theta(a -> b) + theta(b -> c) + theta(c -> a))`, con `theta(x -> y) = +-theta_a` secondo il verso dell'arco.
- **Lo scarto dal flusso pi:** `delta_p = pi - |Phi_p|`, che e' **indipendente dall'orientamento** della placchetta.
- **La soglia** *(la lettera)*: `tau = 3 sigma`, con `sigma` = la rms di `delta_p` sul vuoto fresco della scena *(`phi_v`, `A = 0`; la carta fissa la rms come «sigma dello scarto da pi»)*. **Un difetto** e' una placchetta con `delta_p > tau`.

### I CASI NOTI
- **(K-H1a)** sul vuoto fresco la frazione di difetti e' 0 *(la lettera)*. Se fallisce, H-1 si ferma: la soglia della lettera non separa nemmeno il fresco.
- **(K-H1c)** il gauge su `phi` *(ogni nodo per `e^{i chi_v}` su tutte le sue estremita')* lascia `delta_p` invariato entro `1e-10`.
- **(K-H1n, DEVE FALLIRE)** una fase `pi/2` su UNA estremita' del vuoto fresco: le placchette dei due triangoli di quell'arco diventano difetti *(la frazione non e' piu' 0)*.
- **(K-H1b, STAMPATA, nessun verdetto)** una nascita costruita a mano nel vuoto fresco *(l'arco piu' vicino al centro della scena, con `k`, `l` dall'orientamento del toro)*, con le fasi del nato da `nasci_array`, poi il flip `i - k` da `flip_array`: `Phi` dei 4 triangoli nuovi, poi di quelli dopo il flip. *(`_fattore` scala solo le ampiezze, con un fattore reale: le fasi sono quelle di `nasci_array` e `flip_array`.)*

### LE MISURE
- **(M1) sugli stati salvati di `M0026/C`, da 11500 a 16250 ogni 250:**
  - la frazione di difetti sulle placchette che toccano un nato *(un vertice `>= n0`)*;
  - la frazione sul FONDO: le placchette che NON lo toccano, entro lo stesso raggio *(il centro della placchetta, dal centro di `rho_psi`, al piu' il raggio massimo di quelle che lo toccano)*; e su tutte.
- **(M2, la misura pulita) ogni nascita del registro** con `k` in `(k_s, k_s + 250]` si rigioca SOLA sullo stato `k_s` *(nessun tick)*:
  - `nasci_array`, poi `flip_array` col lato registrato;
  - la frazione di difetti sui triangoli nuovi *(quelli che contengono il nato)*, contro il fondo dello stato `k_s` entro lo stesso raggio;
  - si rigioca solo se l'arco `i - j` c'e' nello stato `k_s`, con i vicini comuni `{k, l}` e la stessa `m`; altrimenti si salta e si conta *(l'arco nato da una nascita precedente nello stesso intervallo)*.
- **La lettura** *(fissata qui)*: «la nascita singola FA difetti» se la frazione dei nuovi supera quella del fondo di piu' di 2 sigma binomiali *(`sqrt(p (1 - p) / N_nuovi)`, con `p` = il fondo)*; «NON li fa» se la supera di meno di 1 sigma o non la supera; in mezzo, NON DECIDIBILE.
- **Lo smaltimento** *(la seconda previsione del guardiano)*: la frazione sui nati negli stati salvati *(M1)* contro quella subito dopo la nascita *(M2)*.
- **Il seguito** *(la lettera)*: se M2 dice «FA difetti», H-2 si scrive in carta; se dice «NON li fa», FERMO su H-2, e si scrive al guardiano.

## H-1 CHIUSO; LA LETTURA DEI BUCHI DI phi CHE RESTANO *([M1205], DECISIONE DI LUCA 2026-11-28 `12:05`, punto 2, dalla posta, guardiano `5dec718e`; scritta PRIMA dello script)* [[PROGETTO-MITOSI]]

- **H-1 e' chiuso dal fatto, non da una soglia:** nel vuoto a flusso pi la nascita singola eredita «per media», e due archi su quattro hanno `phi = 0` *(`a092f5db`)*. La soglia `tau` si toglie.
- **Le definizioni:**
  - `|phi|` di un arco = `min(|f[a,0]|, |f[a,1]|)` *(le due estremita', `f = phi_h.reshape(m, 2)`)*;
  - un **buco** e' un arco con `|phi| < 1e-6` *(lo scarto di G)*; si conta anche `< 1e-3`, la soglia della previsione del guardiano;
  - gli **archi dei nati** sono quelli con un estremo `>= n0`; gli **archi `n - k`, `n - l`** sono quelli del registro, se ci sono ancora nello stato;
  - il **fondo** sono gli archi senza estremi nati, col punto medio entro il raggio massimo degli archi dei nati.
- **(B1) gli stati di C da 11500 a 16250 ogni 250:** la frazione dei buchi sugli archi dei nati, su `n - k` e `n - l`, e sul fondo; **KS a due campioni** *(`scipy.stats.ks_2samp`)* fra `|phi|` dei nati e del fondo, senza soglia.
- **(B2) subito dopo la nascita:** ogni nascita rigiocata SOLA sullo stato precedente *(le funzioni di `flusso_nascite.py`)*; la frazione dei buchi sui suoi archi nuovi.
- **«Il vuoto richiude i buchi col tempo?»** si legge da B2 contro B1.
- **I casi noti:**
  - (K-B1) la nascita rigiocata sola nel fresco *(l'arco 39123)*: 2 archi su 4 sotto `1e-6`, e sono `n - k`, `n - l`;
  - (K-B2) il fondo del fresco: 0 buchi;
  - (K-B3) KS su campioni sintetici: dalla stessa legge `p > 0.01`; da leggi spostate `p < 1e-6`.
