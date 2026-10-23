# LA SCALA E LO ZERO: IL PRINCIPIO DI EQUIVALENZA A `s` PICCOLO, IL SOLITONE CON `c` PROPORZIONALE A `s`, LA RELAZIONE DI EINSTEIN COME DIAGNOSI DELLA CONVENZIONE DELLO ZERO

> **Il mandato:** di Luca, dopo `c4efc937`. ### **Una MISURA su spettri a `cs` uniforme e sul risolutore radiale, in memoria: non sceglie niente.** ### **`leggi.yaml`, l'impronta
> `2e7f795d2a52fbe7`, LA CONVENZIONE DEI PEZZI e il nucleo intatti**; ### **`soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE; git `e96ca41a`)*. ### **Importati, non copiati:**
> `matrice()`, `rami_seguiti()` *(`_massa_vicino_al_cono`)*, `rami()`, `spazio_del_ramo()`, `avvolgi()` *(`_forza_da_cs`)*, `dproprio()`, `convenzione_alternativa()`, `solitone()`,
> `gruppi()`, `c_di()` *(`_gravita_collettiva`, blob `9c34fb6a`)*. ### **L'errore del guardiano n.46:** ### **il controllo a `c` costante di `c4efc937` era mal posto** ### **-- il
> termine di moto non scalava con `s`; il controllo giusto e' `c` proporzionale a `s`.** ### **La domanda «quale `2 pi k`» RESTA APERTA: qui la diagnosi, non la decisione.**

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*.
2. **Il gradino:** ### **`(a)` i controlli** *(un pezzo solo: `delta = 0`; `c` proporzionale a `s`: `D = 0`; il passo intero a `s 0.99`: deve fallire)*; ### **`(b)` la scala** *(l'esponente
   della violazione a `s` piccolo)*; ### **`(c)` la relazione di Einstein nelle tre convenzioni.**
3. **Aggiunge un numero o una legge?** ### **No.** ### **I punti `s`, il cammino fine in `s` e lo zero «a meta'» sono SCELTE DI MISURA o di LETTURA, dichiarate qui.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` SI'** *(uniforme a mano, `s = cs`, `dtau = 1`)*: ### **e' la variabile.** ### **E la convenzione dei pezzi SOLO in memoria, per mostrarla**
   *(`convenzione_alternativa`)*.
5. **Emergente o imposto?** ### **E' la domanda:** ### **il passo e' `exp(-i s H)` con `H` fisso** *(il principio di equivalenza)*, ### **o `exp(-i s [H0 + s H1 + ...])`** *(Baker-Campbell-
   Hausdorff: violato come `s`)*?

## 1. IL METODO

### PARTE A -- LA SCALA

- ### **`s` in `(0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99)`, `eps` in `(0, 0.25, 0.5, 1.0)`**; ### **i rami massivi** *(`_forza_da_cs.rami`, le definizioni di `44d4963d`)*
  ### **raggruppati** *(`_gravita_collettiva.gruppi`, per fasi proprie)*, ### **lati `32` e `64`** *(`_forza_da_cs.L_SPETTRO` impostato in memoria e rimesso)*.
- ### **`omega(0)` SEGUITA CON CONTINUITA' DA `s` PICCOLO** *(dichiarato)*: ### **il blocco `8 x 8` della materia a `k = 0`** *(`matrice()` al lato `16`: il blocco e' lo stesso al bit a
  ogni lato, verificato)*, ### **su un CAMMINO FINE `s = 0.02, 0.025, ..., 0.99`** *(passo `0.005`, piu' i punti `s (1 +- h)` della griglia)*: ### **a `s 0.02` le fasi proprie
  principali** *(sono piccole: `|omega| <= 2 pi s = 0.126`)*, ### **poi a ogni passo gli autovalori seguiti per SOVRAPPOSIZIONE dei vettori propri** *(l'assegnamento ungherese, come
  `rami_seguiti` lungo `k`)* ### **e le fasi SROTOLATE lungo `s`.** ### **Un salto di fase fra due passi oltre `0.2` si segnala** *(il cammino non e' fine abbastanza)*. ### **Il ramo massivo
  della griglia prende la fase continua del livello seguito con la sua fase principale** *(entro `1e-9`)*; ### **se i candidati hanno fasi continue diverse: AMBIGUO.**
- ### **`omega''(0)` DALLE FASI ESATTE** *(non dal fit)*: ### **le fasi di `rami_seguiti` a `k = 0, k_1, 2 k_1`** *(`k_1 = 2 pi/L`)*, ### **`phi(k) = phi0 + a k^2 + b k^4`** ### **->
  `a = (16 Delta_1 - Delta_2)/(12 k_1^2)`, `omega'' = 2 a`** *(Richardson: l'errore e' `O(k_1^4)`, confrontato fra i due lati)*. ### **`v`** ### **il coefficiente del fit di `51f45268`.**
- ### **`E0 = omega(0)/s`, `M = omega''(0)/s`, `D = d(omega/s)/ds`** *(`dproprio`, con la fase continua a `s (1 +- h)`, `h = 1e-3`)*.
- ### **IL GENERATORE EFFICACE:** ### **`H_eff(s) = i log(U)/s`** ### **sul blocco della materia a `k = 0` e a `k = pi/8`** *(`m = 1` al lato `16`)*, ### **in DUE versioni:** ### **col
  logaritmo PRINCIPALE** *(`V diag(i log lambda) V^-1`)* ### **e con le fasi CONTINUE del cammino fine** *(`V diag(omega_cont) V^-1 / s`)*. ### **`delta(s) = ||H_eff(s) - H_eff(0.02)||_F /
  ||H_eff(0.02)||_F`.**
- ### **L'UNIVERSALITA':** ### **le specie = i gruppi massivi a `s 0.02`, ogni `eps`, seguiti lungo il cammino fine** *(il livello seguito)*; ### **per ogni coppia `i, j`: `R_ij(s) =
  E0_i/E0_j` e `M_i/M_j`, `Vi(s) = |R_ij(s) - R_ij(0.02)| / |R_ij(0.02)|`** *(coppie con `|denominatore(0.02)| > 1e-6`)*.
- ### **IL FIT:** ### **`log delta` e `log Vi` contro `log(s - 0.02)`, su `s <= 0.3`** *(il riferimento e' `0.02`, non `0`: contro `log s` l'esponente sarebbe falsato; lo stampo anche contro `log s`)*.

### PARTE B -- IL SOLITONE CON `c` PROPORZIONALE A `s`

- ### **`solitone()` di `c4efc937`** *(`dr = sigma/640`, `R = 12 sigma`)*, ### **`c(s) = c0 s`, `c0 = c(0.9)/0.9` del ramo basso di `eps 0`** *(`c_di`, lato `64`)*, ### **`S1`, `S3`, `S4`,
  `N` in `(1, 10, 100)`, `s` in `(0.85, 0.9, 0.95, 0.99, 1.0)`**, ### **`omega0 = 0`** *(il ramo basso)*; ### **`D = d(mu/s)/ds`.**
- ### **ACCANTO: `D` col `c(s)` MISURATO** ### **letto dal `jsonl` committato di `c4efc937`** *(le righe `livello2` del ramo basso di `eps 0`)*: ### **la differenza e' la violazione dovuta al moto.**

### PARTE C -- LA RELAZIONE DI EINSTEIN

- ### **`Q = omega(0) omega''(0) / v^2`** *(per tick)*, ### **per ogni ramo massivo e `(s, eps)`, lato `64`**, ### **con `omega(0)` in:**
  - ### **`(i)` la convenzione di oggi**, ### **in due letture:** ### **la fase PRINCIPALE** *(quella di `c4efc937`)* ### **e quella CONTINUA da `s` piccolo**;
  - ### **`(ii)` l'alternativa `exp(-i theta P)`: `omega(0) + 2 pi s`** *(principale e continua)*;
  - ### **`(iii)` LO ZERO A META'** ### **fra i due rami di una COPPIA** ### **= due gruppi allo stesso `s` col `Dt` del fit uguale entro `1e-6` relativo e la curvatura di segno OPPOSTO**:
    ### **`omega_mezzo = omega_a + avvolgi(omega_b - omega_a)/2`, e ciascuno `omega - omega_mezzo`.** ### **Dove la coppia non c'e': «NESSUNA COPPIA».**
- ### **NESSUNA CONVENZIONE SI CAMBIA NEL CODICE.**

## 2. LE PREVISIONI *(scritte prima dei numeri)*

- ### ⭐ **DALL'ESPLORAZIONE IN MEMORIA** *(nessun file scritto; i numeri li ristampa lo strumento)*: ### **a `s 0.02, eps 0` le fasi a `k = 0` sono `-2 pi s` (quattro), `-pi s` (due), `0` (due)**;
  ### **a `s 0.99` il ramo ALTO ha fase principale `+0.0628 = 2 pi (1 - s) = -2 pi s + 2 pi`.** ### **QUINDI, SEGUITA CON CONTINUITA' DA `s` PICCOLO, la fase del ramo alto e' `-2 pi s`:**
  ### **`E0 = -2 pi` costante, `D = 0`.** ### ⭐ **LA PREVISIONE: a `eps 0` TUTTI E DUE i rami hanno `D = 0` con la fase continua** *(il basso `E0 = 0`, l'alto `E0 = -2 pi`)*, ### **e il
  `D = -2 pi/s^2` di `c4efc937` sul ramo alto e' UN ARTEFATTO DELLA FASE RIPORTATA in `(-pi, pi]`.** ### **A `eps > 0` non lo so.**
- ### **PARTE A, la scala:** ### **un pezzo solo: `delta = 0`** *(`exp(i pi s P)` ha `H = -pi P` fisso)*; ### **il passo intero: `delta ~ (s - 0.02)^1`** *(BCH: il primo commutatore)*, ### **e
  d'ordine `1` vicino al cono**; ### **ma se a `eps 0` le fasi sono ESATTAMENTE `-2 pi s`, `-pi s`, `0`** *(lineari in `s`)*, ### **gli AUTOVALORI di `H_eff` a `k = 0` non dipendono da
  `s`**: ### **`delta` a `k = 0` viene allora solo dai VETTORI PROPRI** *(se cambiano)*. ### **A `k = pi/8` e a `eps > 0`: esponente `1`.**
- ### **PARTE A, l'universalita':** ### **`Vi` per `E0`: a `eps 0` nullo** *(se `E0` e' costante)*; ### **per `M`: NON nullo** *(`Dt ~ pi s (1 - s)` fa `M = v^2/(Dt s) ~ 1/(s^2 (1 - s))`)*:
  ### **la massa INERZIALE non scala come quella a riposo.**
- ### **PARTE B:** ### **`D = 0` per costruzione** *(`mu = s mu_1`: la griglia in unita' di `sigma = sqrt(|c0|)` e' la stessa a ogni `s`)*, ### **entro il risolutore** *(previsto `<= 1e-9`)*;
  ### **col `c(s)` misurato: i `D` di `c4efc937`** *(`-8.46`, `-5.76`, `-2.58`)*.
- ### **PARTE C** *(la previsione del guardiano, da verificare)*: ### **`(iii)` vicino a `1`**, ### **`(i)` e `(ii)` no.** ### **La mia** *(sulla carta, col Dirac `omega'' = v^2/Dt`)*: ### **`(iii)`
  `Q = pi (1 - s)/Dt ~ 1/s`** *(`1.11` a `s 0.9`)*; ### **`(i)` continua: `Q = 0` sul basso, `-2 pi s/Dt ~ -2/(1 - s)` sull'alto**; ### **NESSUNA delle tre ha `Q` costante a `s` piccolo**
  *(`(iii)` va come `1/s`)*.

## 3. I CRITERI, FISSATI ORA *(copiati dal mandato)*

- ### **DEVE PASSARE:** ### **un pezzo solo acceso** *(solo `CAMM-GROVER`, oppure solo `CAMM-SPOSTAMENTO`: gli altri tolti con `salta`, `matrice()` riusata avvolgendo
  `_stabilita_lineare.passo` in memoria)*: ### **`delta(s) < 1e-12` a ogni `s`**, ### **a `k = 0` e `pi/8`**, ### **col logaritmo principale.**
- ### **DEVE PASSARE:** ### **parte B, `c = c0 s`: `|D| < 1e-6`** per ogni forma e norma dove lo stato e' legato ai tre `s`.
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«`delta(0.99) < 1e-6`» sul passo intero** *(`delta` finito e stampato)*, ### **a `k = pi/8`, `eps 0.5`, col logaritmo principale.**
- ### **PUO' FALLIRE:** ### **l'esponente di `delta` su `s <= 0.3` fra `0.8` e `1.2`** *(passo intero, `k = pi/8`, ogni `eps`, contro `log(s - 0.02)`, continuo)*.
- ### **PUO' FALLIRE:** ### **in `(iii)`, `|Q - 1| < 0.2` a `s 0.9, 0.95, 0.99` per `eps 0`.**
- ### **DI SERVIZIO:** ### **il blocco a `k = 0` e `pi/8` uguale ai lati `16`, `32`, `64` entro `1e-12`**; ### **nessun salto di fase oltre `0.2` sul cammino fine.**
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE:** ### **le tabelle di `delta`, `Vi`, `D`, `Q` e gli esponenti.** ### **A parte: la lettura in tre righe; una riga sulle tre strade della
  regola di scala** *(`s -> 0`, `s` fisso, `s -> 1`)*; ### **una riga su che cosa dice la parte `C` per «quale `2 pi k`».** ### **Informazione per Luca, non scelte.**

## 4. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_scala_e_zero.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima dei numeri;
3. la corsa, il referto `doc/referti_l2/scala_e_zero.txt` e `.jsonl`, la relazione, e la sezione `5` qui sotto.

## 5. I RISULTATI *(scritti dopo la corsa, sotto)*
