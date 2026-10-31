# 2026-10-31 — IL SOLITONE SU `B` A `Gamma` REGGE: CONSOLIDARE *(UNA PROVA IN `csv/`, NESSUNA MODIFICA AL NUCLEO; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `15:58`, sull'esito di `a8e0e43b`)*

> **Lo script:** `csv/_consolida_B.py` *(importa `_coppia_di_B` e `_massimo_di_B`: la scena a `eps`, la coppia, la partenza, le righe della corsa)*. **I dati:** `doc/referti_l2/consolida_B/`; gli stati in `db/consolida_B/` *(ignorato: il dato E' il comando)*. **Il referto:** `doc/referti_l2/consolida_B.txt`.

## 1. LE PREMESSE DAL CODICE

### Da `a8e0e43b`

- A `eps 0.5`, in `3000` unita' di tempo, **il cuore di `B` a `Gamma` `0.620 -> 0.629`**, l'alone `0`; **quello di `A` a `K` `0.589 -> 0.446`**. `D` di `B` cresce LINEARE ed e' tutto in `B`: **(q3)**, con la riserva delle partenze diverse.

### Dal codice *(letto in questa sessione)*

- **Le bande di `D`, ogni `20` tick, sono gia' nei `.jsonl`** *(`lunga_B_*.jsonl`, il campo `D`: `nD = |D|/|psi0|` e la FRAZIONE di `|D|^2` per gruppo `Ppi`, `A`, `P0`, `B`)*. ### **Le ho gia' guardate** *(lo dico: non sono letture alla cieca)*: **a `t 20` la frazione `P0` e' `5.5e-3`, `Ppi` `2.3e-4`, `A` `6.1e-3`, con `nD 1.1e-3`; a `t 20000` `P0 3.4e-6`, `Ppi 1.4e-7`, `A 3.1e-6`, con `nD 0.179`.**
- ### ⚠ **Una premessa del mandato non torna alla lettera: la FRAZIONE scende, perche' `D` cresce lineare in `B`.** `ln(frazione finale/iniziale)/3000` **e' NEGATIVO** e non limita niente. **L'AMPIEZZA nella banda** *(`a = sqrt(frazione) nD`, in unita' di `|psi0|`)* **cresce invece** *(a mano dai due campioni sopra, `~8e-5 -> ~3e-4`: ### **un numero senza provenienza, il conto lo fa il punto `1`**)*. ### **E i tassi noti sono tassi dell'AMPIEZZA:** `modo_di_R.txt` usa `t_vita = ln(1e-2/seme)/gamma` con la soglia su `|D|/|psi0|`. **Quindi il limite si fa sull'ampiezza; la formula alla lettera si stampa accanto.**
- **La fine della corsa di `a8e0e43b`:** `db/coppia_di_B/lunga_B.npz` *(`t 20000`)*, **lo sha1 DEVE essere `sha_fine` di `lunga_B_16000.jsonl`.** `psi0` e `mu` per `D` sono quelli di `_coppia_di_B.partenza_corsa("B")` *(lo sha1 DEVE essere `sha_partenza` dei pezzi)*: ### **`D` continua la stessa serie, al bit.**
- **La partenza della robustezza:** `_massimo_di_B.partenza` costruisce l'inviluppo *(la norma per nodo dello stato di `A` a `K` della scena)* **a `N 1e6` fisso**. **Per `N` diversi** l'inviluppo e' quello della scena a quel `N` *(`_livelli_piatti.scena(N, L)`: `_diagnosi_s4.configura(FORMA, S, N)`)*, **per lo stesso `q`**: la scelta migliore della griglia a `eps 0.5` *(`theta pi/4`, `phi 5 pi/4`, `griglia.json`)*, **costruita sulla scena di riferimento** *(`N 1e6`, `L 81`)*, ### **e verificata autovettore di `A(Gamma)` della scena nuova** *(un DEVE)*.
- **Newton:** `_livelli_piatti.newton` *(GMRES precondizionato, `30` passi, `1e-9`)*. ### **Non ha vincoli: per il punto `4` lo COPIO con un bordo** *(sotto)*, **nello script, non nel nucleo.**

### Cosa NON so

- **Se il tick a `eps 0` lascia invariato il sottospazio di spin su** *(`sigma_z` commuta col tick libero, `e92a7f9c`; col legame sulla densita' totale credo di si', non l'ho misurato)*: **lo stampo** *(il peso di spin giu' dello stato finale)*.
- **Se `N 3e5` e `N 3e6` superano `L/6`:** lo decide la misura sulla partenza.
- **Se l'aggiunta di un controllo** *(la stessa costruzione a `N 1e6`, `L 81`, SENZA Newton)* **sia voluta:** ### **la aggiungo e la DICHIARO** -- senza, una differenza fra `N 1e6, L 120` e `a8e0e43b` non si attribuisce a `L` o a Newton.

## 2. I CRITERI

| il punto | il criterio, scritto prima |
|---|---|
| `1` | **Dai `.jsonl` di `a8e0e43b`, nessuna corsa.** Per `piatte = P0 + Ppi` e per `A`: la frazione `f(t)` e l'ampiezza **`a(t) = sqrt(f) nD`**; il primo campione, il massimo, la fine. **I limiti superiori del tasso, coi semi dichiarati:** **(lett)** `ln(f_fine/f_0)/T` *(la formula di Luca, alla lettera)*; **(a0)** `ln(a_fine/a_0)/T`, il seme `a_0` il primo campione *(`t 20`)*; **(amin)** `ln(a_fine/a_min)/(T - tau_min)`, il seme il minimo dell'ampiezza; **(pend)** la pendenza di `ln a` contro `tau` sulla seconda meta' *(minimi quadrati)*. ### **Il limite dichiarato e' il PIU' GRANDE fra (a0), (amin), (pend).** **Il confronto:** la mista `0.0079` *(`modo_di_R`)*, la coppia di piatte `0.139`-`0.151`, il modo lento `0.0331`. |
| `2` | **`B` a `Gamma`, `eps 0.5`, dalla fine di `a8e0e43b` al bit, fino a `tau 20000`** *(`133334` tick, cioe' `113334` in piu'; Luca ha scritto `113000`: arrotondo a `20000` pieni e lo dico)*, **a pezzi di `10000` tick, ogni pezzo committato;** le stesse righe *(ogni `10` il cuore, `w`, l'alone, il picco; ogni `20` `nD` e le frazioni per banda; le rotazioni a fine pezzo)*. **DEVE:** lo sha1 della partenza e della ripresa; `M` entro `1e-10` relativo **dal tick `0`**. **Il limite del punto `1` si ricalcola su `0 .. 20000`.** |
| `3` | **`3000` unita' di tempo** *(`20000` tick)* **dalla costruzione dell'inviluppo, SENZA Newton, `eps 0.5`:** `N 3e5`, `N 3e6` *(`L 120` se la `w` della partenza a `L 81` supera `81/6`)*, `N 1e6` su `L 120`; **e il controllo dichiarato `N 1e6`, `L 81`.** `mu` di Rayleigh della partenza. Le stesse righe, pezzi di `10000`. **DEVE:** `q` autovettore di `A(Gamma)` della scena entro `1e-10`; la norma della partenza `= N` entro `1e-12`; `M` entro `1e-10`. Per ciascuna: le finestre di `500` *(il cuore, la pendenza, `w`, l'alone, le bande di `D`)* e il limite del punto `1`. |
| `4` | **Dopo `1`-`3`.** Newton **col bordo:** le incognite `(psi, mu, lambda)`, `lambda` complesso; le equazioni `T psi - e^{-i mu s} psi + lambda u = 0`, la norma, **`<u, psi> = 0`**, con `u` il campo UNIFORME del partner nella coppia *(a `eps 0`: `q2`, lo spin giu' -- lo stato tutto spin su; a `eps 0.5`: `q_perp = -sin(theta) q1 + e^{i phi} cos(theta) q2`, ortogonale alla scelta migliore)*. **La partenza:** a `eps 0` `q1` *(`sigma_z +1` entro `1e-10`, DEVE)*; a `eps 0.5` la scelta migliore. **FERMO** se il residuo SENZA `lambda` *(`norm(T psi - e^{-i mu s} psi)/norm(psi)`)* `< 1e-9`; si stampano `norm(lambda)`, `<u, psi>`, e a `eps 0` il peso di spin giu'. **DEVE:** il vincolo vale alla partenza entro `1e-12`. |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **(k1)** regge in tutte le prove, **il limite superiore del tasso sotto quello dell'uscita mista**: il solitone su `B` a `Gamma` e' protetto dall'energia; ### **si scrive come il primo risultato di `doc/CHIUDERE_LE_USCITE.md`**;
- **(k2)** una prova decade: **quale, e quale uscita** *(le bande di `D`)*;
- **(k3)** altro.
- **La nota, senza lettura:** la banda `B` era stata letta come «antimateria» *(MAPPA voce `9`)*; `A` e `B` sono speculari rispetto a `P0`, le piatte no: **quale bordo e' protetto lo decide la posizione delle piatte**; il nome e' una convenzione, **da decidere** *(Luca)*. ### ⚠ **Dal codice: la voce `9` dice «la banda DI SOTTO»; con `E = -arg/s` la `B` e' la banda di quasi-energia PIU' ALTA** *(`E0 +3.178` contro `A` a `K` `-0.6`)*: **lo scrivo accanto alla nota, senza scegliere.**

## 4. LE MOTIVAZIONI

`a8e0e43b` dice che il cuore regge per `3000` unita' di tempo, da UNA partenza. **Il consolidamento chiede tre cose diverse:** **quanto e' piccolo il tasso** *(il limite, che con una deriva lineare si abbassa solo come `1/T`: per questo la corsa a `20000`)*; **se regge anche senza Newton e per altri `N` e `L`** *(che la protezione non sia una proprieta' di quello stato)*; **e se col vincolo lo stato fermo esiste** *(che il plateau sia la direzione libera)*.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_consolida_B.py` e la riga nell'inventario, committati prima di girare.
3. `--limite` *(il punto `1`)*, committato.
4. `--lunga` a pezzi *(il punto `2`)*, ogni pezzo committato.
5. `--robusta N3e5`, `N3e6`, `N1e6_L120`, `N1e6_L81` a pezzi *(il punto `3`)*, ogni pezzo committato.
6. `--vincolo e0`, `--vincolo e05` *(il punto `4`)*, ciascuno committato appena trovato.
7. `--referto`; `doc/CHIUDERE_LE_USCITE.md` e `doc/BANDE_PIATTE.md` *(l'esito)*; `RELAZIONE`; `MAPPA` *(la riga `d`; la nota sulla voce `9`)*; la sezione `6` qui.

### Annotazione *(con lo script, prima di girarlo)*

- **Solo forma:** nella riga del punto `4` dei criteri le barre `|...|` della norma spezzavano la tabella; ### **scritte `norm(...)`, il criterio NON cambia.**

## 6. L'ESITO *(`consolida_B.txt`, `20/20`; `doc/CHIUDERE_LE_USCITE.md` sez. `10` e IL PRIMO RISULTATO; `doc/BANDE_PIATTE.md` sez. `7`)*

- ### **(k1), per le letture scritte prima: REGGE IN TUTTE LE PROVE, e il limite superiore del tasso e' sotto quello dell'uscita mista** *(`eps 0.5`, `S1`, `s 0.15`, `r 1`, `g 1`; il referto `doc/referti_l2/consolida_B.txt`, `20/20`)*.
- **La corsa lunga** *(dallo stato migliore di Newton, `6.8e-5`; `133334` tick, `tau 20000`, al bit dalla fine di `a8e0e43b`; `M` entro `7.8e-11`)*: ### **il cuore `0.62039 -> 0.62367`, sempre fra `0.618` e `0.633`, nessuna deriva** *(le pendenze delle `40` finestre di `500` dei due segni, al piu' `1.1e-5`)*; `w/w_in 0.958`-`0.969`; **l'alone `0.00000` per tutta la corsa.** `D` tutto in `B`; **le rotazioni delle altre bande a fine pezzo vanno verso `0`** *(`A -0.048 -> -0.010`)*.
- ### **Il limite superiore del tasso, aggiornato a `tau 20000`:** **piatte `1.13e-4`** *(`70` volte sotto la mista `0.0079`, `1236` sotto la coppia di piatte `0.139`)*; **`A` `1.09e-4`** *(`72` volte sotto)*. L'ampiezza nelle piatte `8.7e-5 -> 8.2e-4`; la pendenza di `ln a` sulla seconda meta' `4.8e-5`. *(A `tau 3000`: `4.5e-4`, `4.2e-4`. Il limite e' quello di una crescita lineare: scende come `1/T`.)*
- **La robustezza** *(dall'inviluppo, SENZA Newton, `tau 3000`)*: ### **il cuore resta per ogni `N` e ogni `L`:** `N 3e5` *(`L 81`, `w 4.96`)* `0.605 -> 0.593` *(fra `0.573` e `0.608`)*, `w/w_in 1.014`, l'alone `<= 0.0010`; `N 3e6` *(`L 81`, `w 8.70`)* `0.592 -> 0.589`, `w/w_in 1.001`, l'alone `<= 0.0002`; `N 1e6` su `L 120` `0.592 -> 0.604`, `w/w_in 1.010`, l'alone `<= 0.0005`; **il controllo `N 1e6` su `L 81`** `0.592 -> 0.599`, `w/w_in 1.001`, l'alone `<= 0.0005`. ### **Contro `A` a `K` della stessa costruzione** *(`a8e0e43b`)*: `0.589 -> 0.446`, `w/w_in 1.27`, l'alone `0.005` in crescita.
- ### ⚠ **LA RISERVA SUL LIMITE DELLE CORSE ROBUSTE:** dall'inviluppo **`D` parte gia' per l'`80`-`93 %` nelle piatte** *(la partenza non e' pura `B`: il suo contenuto piatto BATTE, `|e^{i Delta t} - 1|`)*; **l'ampiezza nelle piatte non supera MAI quella del primo campione** *(`N 3e5` `0.126 -> 0.086`)*, e il minimo a `tau 6` e' il battimento. ### **Il limite dichiarato** *(`2.9e-4`-`4.7e-4`, il piu' grande `N 3e6` piatte, `17` volte sotto la mista)* **viene da quel minimo: e' un limite largo, non una misura.** **E in `A` la frazione di `D` sale a `0.21`-`0.26`** *(a `tau 1185`-`2331`)* **e poi ridiscende:** il resto della partenza che si ridistribuisce; **l'alone resta `<= 0.001`.**
- ### **Lo stato fermo NON si trova nemmeno col vincolo:** a `eps 0.5` `1.16e-5` *(contro `6.8e-5`)*, a `eps 0` `1.12e-4`, **dove il vincolo non lavora** *(il tick lascia invariato lo spin su: il peso di spin giu' `6e-24`)*. **Che cosa ferma Newton resta aperto.**
- ### **«Protetto dall'energia»: e' la lettura (k1) di Luca, e i numeri la soddisfano;** **la causa e' sostenuta, non separata:** le uscite sono chiuse sulla carta *(sez. `8`)* e il caso con le uscite aperte *(`A` a `K`)* decade; ### **ma nessuna prova qui apre un'uscita su `B` a `Gamma` per vedere il decadimento tornare.**
