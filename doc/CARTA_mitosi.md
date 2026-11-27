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
