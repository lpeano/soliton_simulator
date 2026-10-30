# 2026-10-30 — LA REGOLA DEI TRE INCROCI *(UNA DIAGNOSI IN `csv/`, NESSUNA MODIFICA AL NUCLEO; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `08:52`, dopo `ea8ace8f`)*

> **LIVELLO:** i pesi del tick in memoria *(`_strada_b_r.pesi`)* o ricomposti dai generatori *(`_bande_piatte.ricomposto`)*; una corsa di `4400` tick a `r 1.5247`, una corsa lunga a pezzi a `r 0.69`, un conto sulla carta e sul tick libero; nessun file del nucleo.
> **I nomi:** `a_n`, `b_a` i pesi del nodo e dell'arco per unita' di tempo; `r = b_a/a_n`; `mu0 = (1/2) sqrt(a_n^2 - a_n b_a + b_a^2)`; `alpha` il legame di `S1`, da `0` *(coda)* a `1` *(cuore)*; le frequenze sono energie per unita' di tempo, `-arg(lambda)/s`, come `mu`. `P0 = (b_a - a_n)/2`, `Ppi = -(a_n + b_a)/2` *(esatte a ogni `s`, `ea8ace8f`)*.

## 1. LE PREMESSE DAL CODICE

### Le premesse del guardiano, RILETTE DAL DISCO prima di scrivere

| la premessa | dal disco | l'esito |
|---|---|---|
| `|w - w0|` lungo la corsa lunga a `r 1.5247` ~`1e-7` fino a `420`, poi `1.1e-6` *(480)*, `5.7e-5` *(540)*, `2.7e-3` *(600)*, `2.8e-2` *(660)* | `lunga_r1.52_00000/02000.jsonl`: `6.8e-08` *(390)*, `2.8e-08` *(420)*, `7.3e-08` *(450)*, `1.08e-06` *(480)*, `7.74e-06` *(510)*, `5.74e-05` *(540)*, `4.51e-04` *(570)*, `2.71e-03` *(600)*, `1.02e-02` *(630)*, `2.79e-02` *(660)*; il cuore `0.662797` fino a `510`, `0.660017` a `660` | **confermata**: dai punti, `ln` cresce di circa `0.066` per unita' di tempo fra `480` e `600` *(una stima dai punti, non una misura: la misura e' il punto `1`)* |
| la coppia per anello a `r 1.5247` cambia segno fra gli anelli `12` e `13` *(`+0.707 -> -0.696`)* | `strada_b_lati.txt`, il conto **col SUO stato** di Newton: `12: +0.70727`, `13: -0.69613`, «gli incroci coppia fra gli anelli 12-13»; **col profilo di `r 1`**: `13: +0.15895`, `14: -1.26202`, «13-14» | **confermata**; ### **e un ERRORE MIO:** nella relazione, nella mappa e nel messaggio di `ea8ace8f` ho scritto **«`13`-`14`»**, cioe' il numero del profilo di `r 1`, **per lo stato di `r 1.5247` che e' `12`-`13`** |
| a `r 0.65` la corsa breve «esponenziale (`0.022`)» | `forma_r0.65.json`: la regola scritta prima dice esponenziale, il tasso nella finestra `0.0218` *(tempo `3`-`159`)* | **i numeri sono quelli**; la mia lettura in `ea8ace8f` era «la regola pende per un artefatto, la pendenza locale scende»: resta dichiarata, **la decisione non e' mia** |

### Un secondo errore mio, che il punto `1` mette a nudo

In `ea8ace8f` ho scritto **«nessun modo sopra `0.039`»**, col limite `ln(D_180/residuo)/180`. **Il limite presupponeva che il seme del modo fosse ~ il residuo di Newton.** Un modo a `~0.065` seminato a `~1.7e-10` sarebbe arrivato a `~2e-5` a `180`: la corsa breve l'avrebbe visto. **Non l'ha visto: dunque il seme era molto piu' piccolo del residuo** *(il residuo sta nella banda `A`, al `99.9%`)*, **e il limite di `0.039` non valeva.** La frase giusta era: *«la corsa breve non vede un modo il cui seme sia sotto `|D|` diviso `e^(gamma 180)`»*.

### Dal codice *(i fatti che il metodo usa)*

- **Lo stato del tick e' solo `psi_h`:** `CL.avanza` -> `DC.tick_congelato` rimette `phi` a `phi0` a fine tick *(`_congelato_lungo.avanza`)*. **Quindi salvare `psi_h`, analizzare, rimetterlo e' esatto.** Le analisi lo sporcano: `MI.armoniche` scrive `psi0` in `z["st"]["psi_h"]`, `DV.matrice` passa da `un_tick`. **Il controllo: la corsa del punto `1` deve ridare AL BIT i punti di `lunga_r1.52`** *(gli stessi strumenti in corsa al punto `2`)*.
- **Il tick coi pesi liberi:** `BP.ricomposto(X_G, R_S, s, a, b)` *(`G S S G`)* ridà il tick coi pesi in memoria entro `4.6e-16` a `r 1.5247` *(`ea8ace8f`)*; per `(a, b)` qualunque si controlla di nuovo, con i pesi in memoria avvolti per `a/pi` e `b/pi`.
- **Gli anelli:** `floor(distanza dal baricentro di rho dello stato fermo)`, in `MI.armoniche` *(`ANELLO 1`)* e nel conto di `ea8ace8f`: la stessa definizione.
- **Lo stato di `r 0.69`:** `cerca_r0.69.json`, residuo `1.262e-06`, **NON fermo** *(dichiarato)*; `mu -0.568233828`. Nella corsa breve `D` cresceva lineare a `8.40e-6` per unita' di tempo *(`0.998` della pendenza attesa)*: **in `3000` unita' di tempo la deriva lineare arriva a `~0.025`, sopra la saturazione `1e-2`.** Quindi un esponenziale va cercato **banda per banda**, fuori da `A` dove sta la deriva.

### Sulla carta *(le formule; i valori li dara' lo script)*

Con `mu = -mu0 + 1 + d` *(il legame vale `1` nel cuore)*, le tre condizioni sono lineari in `alpha`, e **non passano per lo zero in `[0, 1]` se e solo se hanno lo stesso segno ai due estremi**:

| la condizione | a `alpha = 0` | a `alpha = 1` |
|---|---|---|
| la coppia `P0 + Ppi + 2 alpha - 2 mu` | `2 mu0 - a_n - 2 - 2 d` | `2 mu0 - a_n - 2 d` |
| c1 `P0 + alpha - mu` | `(b_a - a_n)/2 + mu0 - 1 - d` | `(b_a - a_n)/2 + mu0 - d` |
| c1 `Ppi + alpha - mu` | `-(a_n + b_a)/2 + mu0 - 1 - d` | `-(a_n + b_a)/2 + mu0 - d` |

- **Due disuguaglianze dalla forma di `mu0`** *(per `a_n, b_a >= 0`)*: `a^2 - a b + b^2 >= (a - b)^2` da' `(b_a - a_n)/2 + mu0 >= 0`; `a^2 - a b + b^2 <= (a + b)^2` da' `mu0 <= (a_n + b_a)/2`. **Quindi** c1 su `Ppi` non incrocia se `d >= 0` *(il margine `(a_n + b_a)/2 - mu0 + d`)*; c1 su `P0` non incrocia **solo se** `(b_a - a_n)/2 + mu0 > 1 + d`; la coppia ha **due rami**: tutta negativa *(`2 mu0 < a_n + 2 d`, circa `r < 1`)* o tutta positiva *(`2 mu0 > a_n + 2 + 2 d`)*.
- **Le tre condizioni a pesi moltiplicati per `lambda`:** ogni margine e' `lambda` volte un pezzo dei pesi, piu' una costante *(`1` o `0`)*: **se esiste un punto con margine positivo, ingrandire i pesi lo allarga.** La regione, se c'e', **non e' limitata** sulla carta; il suo **costo** cresce con `mu0` *(e la massa con `a_n b_a`)*. **Lo scrivo PRIMA, perche' la lettura `(g1)` lo dira' comunque, e non deve sembrare una scoperta.**
- **Il punto `a_n 5`, `b_a 3` sulla carta** *(dalla formula, `d` trascurato)*: `mu0 = sqrt(19)/2 = 2.179`; la coppia da `-2.64` a `-0.64`; c1 `P0` da `+0.18` a `+1.18`; c1 `Ppi` da `-2.82` a `-1.82`. **Il guardiano scrive la coppia `-0.24`, `P0 +0.36`: dalla formula non tornano.** Lo script lo dira' sul tick; **non so da dove vengano i numeri del guardiano.**

### Cosa NON so

- **se `mu = -mu0 + 1 + d` regge lontano da `mu0 = pi/2`**: `d` e' misurato solo a `mu0 = pi/2` *(`r 0.65`, `0.69`, `1`, `1.5247`)*; a pesi piu' grandi l'energia cinetica del solitone cambia *(la massa cambia)*, e con lei `d`. **Il punto `3` ne dichiara la dispersione, non la estrapola.**
- **se il primo ordine regge a pesi grandi:** a `s 0.15`, `s a_n` arriva a `0.75` per `a_n 5`; lo scarto dal primo ordine e' `O(s^2)` **per unita' di peso al cubo**. Per questo il mandato chiede il tick libero.
- **se il modo di `r 1.5247` e' UNO** *(un tasso, un periodo)* o piu' d'uno.
- **dove nasce il seme del modo** *(arrotondamento?)*: non si misura qui.

## 2. I CRITERI

| il punto | il criterio *(fissato qui, prima dei numeri)* |
|---|---|
| `1`, la corsa | `4400` tick da `fermo_r1.52` col cammino di `lunga` *(`CL.avanza`, `VC.FORMA`, `DC.ZERO`)*; **DEVE PASSARE: i punti ogni `10` tick = `lunga_r1.52`, AL BIT**, con gli strumenti accesi in corsa |
| `1`, `D` | `D(t) = e^{i mu s t} psi(t) - psi0`; `|D|/|psi0|`, le frazioni di `D` nelle bande *(`DV.GRUPPI`)* e il profilo di `|D|^2` per anello, **ogni `10` tick** *(`1.5` unita' di tempo)*; `D` intero salvato fra tick `3000` e `4400` *(tempo `450`-`660`)* in `db/tre_incroci/` *(non committato: il dato e' il comando)* |
| `1`, la finestra | **da `10` volte la deriva lineare della corsa breve** *(`c + v tau` di `forma_r1.52.json`)* **a `1e-2`**; il tasso = la pendenza di `ln|D|` nella finestra; lo scarto massimo dalla retta stampato |
| `1`, il periodo | come `5f06dbfb`: i cambi di segno di `Re<D(t_rif), D(t)>` nella finestra, `t_rif` = l'ultimo campione della finestra; e `|<D, D'>|/|D||D'|` fra campioni vicini |
| `1`, la forma | a tre istanti nella finestra *(se ci sono)*: le bande, i tre anelli maggiori, le armoniche `m 0..12` di `drho` e della fase *(`MI.per_nodo`, `MI.armoniche`)* |
| `2`, la corsa | `20000` tick da `fermo_r0.69` *(NON fermo, residuo `1.262e-06`)*, a pezzi di `2000`, ogni pezzo committato appena fatto; gli stessi strumenti del punto `1`; le armoniche ogni `500` tick |
| `2`, la forma | **sulle bande fuori da `A`** *(dove la deriva non sta)*: per `P0`, `Ppi`, `B`, `|D_banda| = |D| sqrt(frazione)`; (L) contro (E) come `ea8ace8f` *(lo scarto di `ln(|D|/fit)`)*, sui campioni sotto `1e-2`; **e su `|D|` intero**, come `ea8ace8f` |
| `2`, le finestre | quelle di `ea8ace8f` *(`500` unita' di tempo: `w/w_in`, il cuore, l'alone, il picco)*, accanto a `r 1.5247` *(`lunga_r1.52`)* e a `r 1` *(`26300537`, `s 0.3`)* |
| `3`, la carta | i tre margini ai due estremi di `alpha`; `d = mu + mu0 - 1` dai quattro stati fermi, **col `mu0` della formula e col `mu0 = -A(K)` del tick**; **la regione con `d` al suo minimo E al suo massimo** *(la dispersione e' la barra)* |
| `3`, la scansione | **a `mu0` fissato, tutto il quarto `a_n, b_a > 0`** *(`a_n = 2 mu0 cos t / sqrt(1 - cos t sin t)`, `b_a = ... sin t`, `t` in `(0, pi/2)`, `9000` punti)*: il margine minimo migliore e il suo `r`, **per ramo** *(`r < 1`, `r > 1`)*; **il `mu0` minimo** per cui un ramo ha margine positivo *(bisezione)*. I `mu0`: `pi/2` *(oggi)* e quello del punto `(5, 3)` *(il guardiano)*: **nessun numero scelto da me** |
| `3`, il tick | i punti: **il migliore a `mu0 = pi/2`** *(la fettina)*; **`(5, 3)`**; **il migliore di ogni ramo a `mu0` di `(5, 3)`**; su ciascuno: le piatte *(e la loro larghezza)*, `A(K)`, la curvatura di `A` a `K` contro `r 1`, le tre condizioni con `mu = A(K) + 1 + d`; **DEVE PASSARE: il tick ricomposto = il tick coi pesi in memoria, entro `1e-10`, a `(5, 3)`** |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie)*

- **Punto `1`:** **(m1)** `D` nelle piatte `P0 + Ppi` agli anelli `12`-`13`: la coppia locale; **(m2)** altrove *(dove)*. **Come si legge, scritto qui:** (m1) se, agli istanti della finestra, `P0 + Ppi` pesa piu' di `A + B` **e** l'anello maggiore di `|D|^2` e' il `12` o il `13`; altrimenti (m2), col dove.
- **Punto `2`:** **(c1)** a `r 0.69` il cuore regge per `3000`: la fettina funziona; **(c2)** si svuota *(quando, dove, quale condizione)*. **Come si legge:** il cuore *(`f_win`)* nelle finestre di `500`, accanto a `r 1.5247` e `r 1`; e la forma banda per banda.
- **Punto `3`:** **(g1)** esiste una regione con margine *(quanto)* e il suo costo *(`mu0`, la massa)*; **(g2)** non esiste; **(g3)** altro.
- **La regola stessa:** **confermata** se il punto `1` da' (m1) *(la coppia incrocia a `r > 1` e il modo sta li')* **e** il punto `2` da' (c1) *(a `r 0.69` nessuna delle tre incrocia e il cuore regge)*; **smentita** se uno dei due va contro; **non decisa** altrimenti.

## 4. LE MOTIVAZIONI

La decisione di Luca fra `(A)`, `(B)`, `(C)` di `doc/BANDE_PIATTE.md`. **`(B)` con `mu0 = pi/2` fisso e' una fettina** *(la regola del guardiano: resta `r ~0.68`-`0.69`)*; **con i pesi liberi forse no.** Il punto `3` dice quanto costa allargarla, i punti `1`-`2` se la regola che la disegna e' vera.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_tre_incroci.py` *(`--modo`, `--lunga`, `--referto`)* con la sua riga nell'inventario; committato **prima** di girarlo.
3. `--modo`: la corsa di `4400` tick a `r 1.5247`; il `.json` committato.
4. `--lunga` dieci volte: ogni pezzo committato appena fatto.
5. `--referto` in `doc/referti_l2/tre_incroci.txt`.
6. `doc/BANDE_PIATTE.md`: la regola e la regione.
7. `RELAZIONE_PER_CLAUDE.md`; `doc/MAPPA.md` *(la riga `d`; l'errore `n.83` del guardiano)*; e **i miei due errori** *(`13`-`14` per `12`-`13`; il limite di `0.039`)*.
8. La sezione `6` qui; il checkpoint; la coda.
