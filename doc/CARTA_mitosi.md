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
