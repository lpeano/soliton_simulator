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

### 📝 **ANNOTAZIONE 1** *(prima della corsa dello strumento committato, nel commit dello strumento)*:
- ### **`s 0.95` AGGIUNTO alla griglia della parte `A`**: ### **il controllo `(iii)` del mandato lo chiede, e la lista della parte `A` non lo aveva.** ### **Il fit su `s <= 0.3` non
  cambia.**
- ### **La prova a vuoto in memoria** *(lo strumento negli appunti, `eps` `0` e `0.5`, lato `64`, `S3`, `N 10`; il `jsonl` negli appunti)* ### **ha stampato dei numeri; li dichiaro e
  NON correggo le previsioni:** ### **a `eps 0, k = 0` il `delta` continuo e' `~1e-14` a ogni `s`** *(come previsto: `H_eff` a `k = 0` non dipende da `s`)*; ### **a `k = pi/8` l'esponente
  contro `log(s - 0.02)` e' `~1.7` e contro `log s` `~2.1`, NON `1`** ### **-- il che si leggerebbe col PALINDROMO: una composizione simmetrica cancella i termini dispari di BCH, e la
  correzione e' `O(s^2)`, non `O(s)`.** ### **La previsione «`1`» resta scritta, e il controllo che puo' fallire fallira'.** ### **Il `(iii)` a `s 0.99` vale `~0.68`: fallira' anche lui.**
- ### **Un difetto della prova a vuoto, non dello strumento:** ### **dagli appunti la `RADICE` dello strumento puntava fuori dal repo** *(il `jsonl` di `c4efc937` «non committato»)*:
  ### **nel repo il percorso e' quello giusto.**

## 4. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_scala_e_zero.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima dei numeri;
3. la corsa, il referto `doc/referti_l2/scala_e_zero.txt` e `.jsonl`, la relazione, e la sezione `5` qui sotto.

## 5. I RISULTATI *(scritti dopo la corsa, sotto)*

### **LA CORSA:** `python csv/_scala_e_zero.py`, strumento sha1-BYTE `0629c68e` *(`53f06cff`, committato e pulito)*. ### **`6` controlli su `8`.**

- ### **DEVE PASSARE, un pezzo solo: PASSA** *(`delta <= 4.3e-15` a ogni `s`, Grover e spostamento, `k = 0` e `pi/8`)*.
- ### **DEVE PASSARE, `c = c0 s`: PASSA** *(`|D| <= 2.0e-8` su `30` punti legati)*.
- ### **DEVE FALLIRE, «`delta(0.99) < 1e-6`»: FALLISCE per la chiave giusta** *(`delta = 0.954`)*.
- ### ⚠ **PUO' FALLIRE, l'esponente di `delta` fra `0.8` e `1.2`: FALLISCE** ### **-- `1.70`-`1.72` contro `s - 0.02`, `2.12`-`2.14` contro `s`, a ogni `eps`**: ### **la correzione e'
  `O(s^2)`, non `O(s)`** *(la mia lettura, scritta nell'annotazione `1` prima della corsa: il passo PALINDROMO cancella i termini dispari di BCH)*.
- ### ⚠ **PUO' FALLIRE, `(iii)` `|Q - 1| < 0.2`: FALLISCE a `s 0.99`** ### **-- `1.096`, `1.046`, `0.680` a `s 0.9`, `0.95`, `0.99` al lato `64`; `1.087`, `0.979`, `0.431` al lato `32`**:
  ### **a `s 0.99` `Q` DIPENDE DAL LATO** *(`Dt = 0.028`, `v k_1/Dt ~ 2.4` al lato `64`: la curvatura a `k = 0` non e' risolta dalle fasi a `k_1` e `2 k_1`)*.
- ### **DI SERVIZIO: tutti** *(i salti di fase sul cammino fine `<= 3.3e-2`; i blocchi uguali ai tre lati `0.0`; l'alternativa `1.3e-15`)*; ### **nessun ramo AMBIGUO.**

### 5.1 `delta(s)` *(il passo intero; `||H_eff(s) - H_eff(0.02)|| / ||H_eff(0.02)||`)* E GLI ESPONENTI *(su `s <= 0.3`)*

| `eps` | `k` | versione | `0.05` | `0.1` | `0.2` | `0.3` | `0.5` | `0.7` | `0.9` | `0.95` | `0.99` | `p` contro `s - 0.02` | `p` contro `s` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `0` | k=0 | principale | `8.8e-15` | `8.7e-15` | `8.1e-15` | `8.5e-15` | `9.5e-01` | `1.3e+00` | `1.0e+00` | `9.9e-01` | `9.5e-01` | `-0.025` | `-0.031` |
| `0` | k=0 | continua | `8.8e-15` | `8.7e-15` | `8.1e-15` | `8.4e-15` | `8.2e-15` | `8.3e-15` | `8.3e-15` | `8.8e-15` | `8.0e-15` | `-0.031` | `-0.038` |
| `0` | k=pi/8 | principale | `1.7e-04` | `7.7e-04` | `3.3e-03` | `7.8e-03` | `2.6e-02` | `1.4e+00` | `1.1e+00` | `1.0e+00` | `9.6e-01` | `1.716` | `2.140` |
| `0` | k=pi/8 | continua | `1.7e-04` | `7.7e-04` | `3.3e-03` | `7.8e-03` | `2.6e-02` | `7.4e-02` | `2.7e-01` | `4.1e-01` | `5.5e-01` | `1.716` | `2.140` |
| `0.25` | k=0 | principale | `2.7e-04` | `1.2e-03` | `5.2e-03` | `1.2e-02` | `1.6e+00` | `1.3e+00` | `1.0e+00` | `9.9e-01` | `9.5e-01` | `1.703` | `2.123` |
| `0.25` | k=0 | continua | `2.7e-04` | `1.2e-03` | `5.2e-03` | `1.2e-02` | `3.8e-02` | `9.8e-02` | `3.1e-01` | `4.7e-01` | `6.3e-01` | `1.703` | `2.123` |
| `0.25` | k=pi/8 | principale | `3.1e-04` | `1.4e-03` | `6.0e-03` | `1.4e-02` | `1.3e+00` | `1.3e+00` | `1.1e+00` | `1.0e+00` | `9.6e-01` | `1.706` | `2.127` |
| `0.25` | k=pi/8 | continua | `3.1e-04` | `1.4e-03` | `6.0e-03` | `1.4e-02` | `4.6e-02` | `1.2e-01` | `3.6e-01` | `4.9e-01` | `6.0e-01` | `1.706` | `2.127` |
| `0.5` | k=0 | principale | `5.3e-04` | `2.5e-03` | `1.0e-02` | `2.4e-02` | `1.9e+00` | `1.3e+00` | `1.0e+00` | `9.9e-01` | `9.5e-01` | `1.703` | `2.123` |
| `0.5` | k=0 | continua | `5.3e-04` | `2.5e-03` | `1.0e-02` | `2.4e-02` | `7.6e-02` | `1.9e-01` | `4.7e-01` | `5.8e-01` | `6.5e-01` | `1.703` | `2.123` |
| `0.5` | k=pi/8 | principale | `5.5e-04` | `2.5e-03` | `1.1e-02` | `2.5e-02` | `1.3e+00` | `1.3e+00` | `1.0e+00` | `9.9e-01` | `9.5e-01` | `1.704` | `2.124` |
| `0.5` | k=pi/8 | continua | `5.5e-04` | `2.5e-03` | `1.1e-02` | `2.5e-02` | `7.9e-02` | `2.0e-01` | `4.7e-01` | `5.6e-01` | `6.3e-01` | `1.704` | `2.124` |
| `1` | k=0 | principale | `1.1e-03` | `4.9e-03` | `2.1e-02` | `4.8e-02` | `1.9e+00` | `1.3e+00` | `1.0e+00` | `9.8e-01` | `9.4e-01` | `1.703` | `2.124` |
| `1` | k=0 | continua | `1.1e-03` | `4.9e-03` | `2.1e-02` | `4.8e-02` | `1.5e-01` | `3.4e-01` | `5.9e-01` | `6.3e-01` | `6.6e-01` | `1.703` | `2.124` |
| `1` | k=pi/8 | principale | `1.1e-03` | `4.9e-03` | `2.1e-02` | `4.8e-02` | `1.3e+00` | `1.3e+00` | `1.0e+00` | `9.9e-01` | `9.5e-01` | `1.703` | `2.124` |
| `1` | k=pi/8 | continua | `1.1e-03` | `4.9e-03` | `2.1e-02` | `4.8e-02` | `1.5e-01` | `3.4e-01` | `5.8e-01` | `6.2e-01` | `6.5e-01` | `1.703` | `2.124` |

### 5.2 I RAMI *(lato `64`)*: `E0 = omega_cont/s`, `M = omega''/s`, `D = d(omega_cont/s)/ds`

| `eps` | `s` | ramo | `omega(0)` principale | `omega(0)` continua | `E0` | `M` | `D` | ambiguo |
|---|---|---|---|---|---|---|---|---|
| `0` | `0.02` | Dt 0.0341 w0 +0.0000 | `+0.00000` | `-0.00000` | `-0.00000` | `-0.3928` | `-5.551e-13` | no |
| `0` | `0.02` | Dt 0.0341 w0 -0.1257 | `-0.12566` | `-0.12566` | `-6.28319` | `+0.3928` | `-4.219e-10` | no |
| `0` | `0.05` | Dt 0.0852 w0 -0.0000 | `-0.00000` | `-0.00000` | `-0.00000` | `-0.3935` | `-8.882e-14` | no |
| `0` | `0.05` | Dt 0.0852 w0 -0.3142 | `-0.31416` | `-0.31416` | `-6.28319` | `+0.3935` | `-3.553e-11` | no |
| `0` | `0.1` | Dt 0.1696 w0 +0.0000 | `+0.00000` | `-0.00000` | `-0.00000` | `-0.3960` | `+2.220e-11` | no |
| `0` | `0.1` | Dt 0.1696 w0 -0.6283 | `-0.62832` | `-0.62832` | `-6.28319` | `+0.3960` | `-1.776e-11` | no |
| `0` | `0.2` | Dt 0.3326 w0 -0.0000 | `-0.00000` | `-0.00000` | `-0.00000` | `-0.4061` | `+5.551e-15` | no |
| `0` | `0.2` | Dt 0.3326 w0 -1.2566 | `-1.25664` | `-1.25664` | `-6.28319` | `+0.4061` | `+4.441e-12` | no |
| `0` | `0.3` | Dt 0.4807 w0 +0.0000 | `+0.00000` | `+0.00000` | `+0.00000` | `-0.4246` | `+2.467e-15` | no |
| `0` | `0.3` | Dt 0.4807 w0 -1.8850 | `-1.88496` | `-1.88496` | `-6.28319` | `+0.4246` | `+2.961e-12` | no |
| `0` | `0.5` | Dt 0.6858 w0 -0.0000 | `-0.00000` | `-0.00000` | `-0.00000` | `-0.5000` | `-8.882e-13` | no |
| `0` | `0.5` | Dt 0.6858 w0 -3.1416 | `-3.14159` | `-3.14159` | `-6.28319` | `+0.5000` | `+0.000e+00` | no |
| `0` | `0.7` | Dt 0.6563 w0 +0.0000 | `+0.00000` | `+0.00000` | `+0.00000` | `-0.7009` | `+4.532e-16` | no |
| `0` | `0.7` | Dt 0.6563 w0 +1.8850 | `+1.88496` | `-4.39823` | `-6.28319` | `+0.7009` | `+0.000e+00` | no |
| `0` | `0.9` | Dt 0.2836 w0 +0.0000 | `+0.00000` | `-0.00000` | `-0.00000` | `-1.7520` | `-2.741e-13` | no |
| `0` | `0.9` | Dt 0.2836 w0 +0.6283 | `+0.62832` | `-5.65487` | `-6.28319` | `+1.7520` | `-9.869e-13` | no |
| `0` | `0.95` | Dt 0.1454 w0 +0.0000 | `+0.00000` | `+0.00000` | `+0.00000` | `-3.3046` | `-2.460e-13` | no |
| `0` | `0.95` | Dt 0.1454 w0 +0.3142 | `+0.31416` | `-5.96903` | `-6.28319` | `+3.3046` | `-1.402e-12` | no |
| `0` | `0.99` | Dt 0.0280 w0 +0.0628 | `+0.06283` | `-6.22035` | `-6.28319` | `+10.5752` | `+0.000e+00` | no |
| `0` | `0.99` | Dt 0.0280 w0 -0.0000 | `-0.00000` | `-0.00000` | `-0.00000` | `-10.5752` | `-2.266e-16` | no |
| `0.25` | `0.02` | Dt 0.0339 w0 +0.0002 | `+0.00020` | `+0.00020` | `+0.00992` | `-0.3916` | `-1.306e-03` | no |
| `0.25` | `0.02` | Dt 0.0341 w0 -0.1259 | `-0.12586` | `-0.12586` | `-6.29310` | `+0.3912` | `+1.306e-03` | no |
| `0.25` | `0.05` | Dt 0.0846 w0 +0.0005 | `+0.00049` | `+0.00049` | `+0.00985` | `-0.3923` | `-3.273e-03` | no |
| `0.25` | `0.05` | Dt 0.0878 w0 -0.3147 | `-0.31465` | `-0.31465` | `-6.29304` | `+0.3900` | `+3.273e-03` | no |
| `0.25` | `0.1` | Dt 0.1684 w0 +0.0010 | `+0.00096` | `+0.00096` | `+0.00960` | `-0.3947` | `-6.613e-03` | no |
| `0.25` | `0.1` | Dt 0.1961 w0 -0.6293 | `-0.62928` | `-0.62928` | `-6.29279` | `+0.3857` | `+6.613e-03` | no |
| `0.25` | `0.2` | Dt 0.3303 w0 +0.0017 | `+0.00172` | `+0.00172` | `+0.00859` | `-0.4048` | `-1.379e-02` | no |
| `0.25` | `0.2` | Dt 0.7072 w0 -1.2584 | `-1.25836` | `-1.25836` | `-6.29178` | `+0.3691` | `+1.379e-02` | no |
| `0.25` | `0.3` | Dt 0.4776 w0 +0.0020 | `+0.00204` | `+0.00204` | `+0.00680` | `-0.4230` | `-2.226e-02` | no |
| `0.25` | `0.5` | Dt 0.6823 w0 +0.0000 | `+0.00000` | `+0.00000` | `+0.00000` | `-0.4969` | `-4.902e-02` | no |
| `0.25` | `0.7` | Dt 0.6580 w0 -0.0111 | `-0.01105` | `-0.01105` | `-0.01579` | `-0.6888` | `-1.258e-01` | no |
| `0.25` | `0.9` | Dt 0.3327 w0 -0.0701 | `-0.07008` | `-0.07008` | `-0.07787` | `-1.4540` | `-7.563e-01` | no |
| `0.25` | `0.9` | Dt 0.6021 w0 +0.6984 | `+0.69840` | `-5.58479` | `-6.20532` | `+0.9962` | `+7.563e-01` | no |
| `0.25` | `0.95` | Dt 0.2444 w0 -0.1268 | `-0.12685` | `-0.12685` | `-0.13352` | `-1.9218` | `-1.590e+00` | no |
| `0.25` | `0.95` | Dt 0.3467 w0 +0.4410 | `+0.44101` | `-5.84218` | `-6.14966` | `+1.4448` | `+1.590e+00` | no |
| `0.25` | `0.99` | Dt 0.2052 w0 -0.2180 | `-0.21803` | `-0.21803` | `-0.22023` | `-2.1924` | `-2.810e+00` | no |
| `0.25` | `0.99` | Dt 0.2717 w0 +0.2809 | `+0.28086` | `-6.00232` | `-6.06295` | `+1.7032` | `+2.810e+00` | no |
| `0.5` | `0.02` | Dt 0.0332 w0 +0.0008 | `+0.00079` | `+0.00079` | `+0.03949` | `-0.3879` | `-5.174e-03` | no |
| `0.5` | `0.02` | Dt 0.0335 w0 -0.1265 | `-0.12645` | `-0.12645` | `-6.32267` | `+0.3876` | `+5.174e-03` | no |
| `0.5` | `0.05` | Dt 0.0829 w0 +0.0020 | `+0.00196` | `+0.00196` | `+0.03922` | `-0.3886` | `-1.297e-02` | no |
| `0.5` | `0.05` | Dt 0.0887 w0 -0.3161 | `-0.31612` | `-0.31612` | `-6.32240` | `+0.3862` | `+1.297e-02` | no |
| `0.5` | `0.1` | Dt 0.1650 w0 +0.0038 | `+0.00382` | `+0.00382` | `+0.03824` | `-0.3909` | `-2.622e-02` | no |
| `0.5` | `0.1` | Dt 0.2233 w0 -0.6321 | `-0.63214` | `-0.63214` | `-6.32142` | `+0.3814` | `+2.622e-02` | no |
| `0.5` | `0.2` | Dt 0.3237 w0 +0.0068 | `+0.00684` | `+0.00684` | `+0.03422` | `-0.4006` | `-5.474e-02` | no |
| `0.5` | `0.3` | Dt 0.4684 w0 +0.0081 | `+0.00813` | `+0.00813` | `+0.02711` | `-0.4181` | `-8.857e-02` | no |
| `0.5` | `0.5` | Dt 0.6718 w0 +0.0000 | `+0.00000` | `-0.00000` | `-0.00000` | `-0.4877` | `-1.953e-01` | no |
| `0.5` | `0.7` | Dt 0.6622 w0 -0.0434 | `-0.04338` | `-0.04338` | `-0.06197` | `-0.6543` | `-4.813e-01` | no |
| `0.5` | `0.9` | Dt 0.0132 w0 +0.6126 | `+0.61257` | `-5.67062` | `-6.30068` | `+0.4390` | `+1.587e-01` | no |
| `0.5` | `0.9` | Dt 0.4253 w0 -0.2284 | `-0.22843` | `-0.22843` | `-0.25381` | `-1.0516` | `-1.773e+00` | no |
| `0.5` | `0.95` | Dt 0.0163 w0 +0.3054 | `+0.30545` | `-5.97774` | `-6.29235` | `+0.4562` | `+1.747e-01` | no |
| `0.5` | `0.95` | Dt 0.3735 w0 -0.3413 | `-0.34133` | `-0.34133` | `-0.35929` | `-1.1441` | `-2.464e+00` | no |
| `0.5` | `0.95` | Dt 1.0325 w0 +0.6555 | `+0.65549` | `-5.62770` | `-5.92389` | `+0.6611` | `+2.464e+00` | no |
| `0.5` | `0.99` | Dt 0.0189 w0 +0.0609 | `+0.06095` | `-6.22224` | `-6.28509` | `+0.4667` | `+1.886e-01` | no |
| `0.5` | `0.99` | Dt 0.3448 w0 -0.4645 | `-0.46450` | `-0.46450` | `-0.46919` | `-1.1673` | `-3.019e+00` | no |
| `0.5` | `0.99` | Dt 0.7162 w0 +0.5273 | `+0.52733` | `-5.75586` | `-5.81400` | `+0.6708` | `+3.019e+00` | no |
| `1` | `0.02` | Dt 0.0308 w0 +0.0031 | `+0.00310` | `+0.00310` | `+0.15512` | `-0.3743` | `-1.997e-02` | no |
| `1` | `0.02` | Dt 0.0310 w0 -0.1288 | `-0.12877` | `-0.12877` | `-6.43830` | `+0.3739` | `+1.997e-02` | no |
| `1` | `0.05` | Dt 0.0768 w0 +0.0077 | `+0.00770` | `+0.00770` | `+0.15407` | `-0.3749` | `-5.009e-02` | no |
| `1` | `0.05` | Dt 0.0813 w0 -0.3219 | `-0.32186` | `-0.32186` | `-6.43725` | `+0.3724` | `+5.009e-02` | no |
| `1` | `0.1` | Dt 0.1529 w0 +0.0150 | `+0.01503` | `+0.01503` | `+0.15029` | `-0.3768` | `-1.014e-01` | no |
| `1` | `0.1` | Dt 0.1964 w0 -0.6433 | `-0.64335` | `-0.64335` | `-6.43347` | `+0.3672` | `+1.014e-01` | no |
| `1` | `0.2` | Dt 0.3000 w0 +0.0269 | `+0.02694` | `+0.02694` | `+0.13470` | `-0.3850` | `-2.130e-01` | no |
| `1` | `0.2` | Dt 2.1157 w0 -1.2836 | `-1.28358` | `-1.28358` | `-6.41788` | `+0.3472` | `+2.130e-01` | no |
| `1` | `0.3` | Dt 0.4347 w0 +0.0321 | `+0.03208` | `+0.03208` | `+0.10694` | `-0.3993` | `-3.473e-01` | no |
| `1` | `0.5` | Dt 0.6309 w0 +0.0000 | `+0.00000` | `+0.00000` | `+0.00000` | `-0.4515` | `-7.692e-01` | no |
| `1` | `0.7` | Dt 0.0796 w0 +1.7683 | `+1.76833` | `-4.51485` | `-6.44979` | `+0.3000` | `+4.058e-01` | no |
| `1` | `0.7` | Dt 0.6668 w0 -0.1620 | `-0.16204` | `-0.16204` | `-0.23149` | `-0.5389` | `-1.654e+00` | no |
| `1` | `0.9` | Dt 0.1724 w0 +0.5686 | `+0.56863` | `-5.71455` | `-6.34950` | `+0.3742` | `+6.056e-01` | no |
| `1` | `0.9` | Dt 0.5818 w0 -0.6241 | `-0.62411` | `-0.62411` | `-0.69345` | `-0.5940` | `-2.915e+00` | no |
| `1` | `0.95` | Dt 0.1904 w0 +0.2813 | `+0.28127` | `-6.00191` | `-6.31780` | `+0.3821` | `+6.628e-01` | no |
| `1` | `0.95` | Dt 0.5609 w0 -0.8017 | `-0.80170` | `-0.80170` | `-0.84389` | `-0.5866` | `-3.084e+00` | no |
| `1` | `0.99` | Dt 0.2028 w0 +0.0557 | `+0.05574` | `-6.22744` | `-6.29035` | `+0.3849` | `+7.101e-01` | no |
| `1` | `0.99` | Dt 0.5463 w0 -0.9589 | `-0.95891` | `-0.95891` | `-0.96859` | `-0.5747` | `-3.139e+00` | no |
| `1` | `0.99` | Dt 1.0565 w0 +1.0217 | `+1.02174` | `-5.26145` | `-5.31459` | `+0.0777` | `+3.139e+00` | no |

### **Ambigui: `0`.** ### **`|D|` massimo per `eps` (lato `64`):** `eps 0` `4.22e-10`; `eps 0.25` `2.81e+00`; `eps 0.5` `3.02e+00`; `eps 1` `3.14e+00`.


### 5.3 L'UNIVERSALITA' `Vi(s)`, per `E0` e per `M` *(le coppie di specie seguite da `s 0.02`, lato `64`)*

| specie `i` | specie `j` | grandezza | `R0` | `Vi(0.1)` | `Vi(0.3)` | `Vi(0.9)` | `Vi(0.99)` | esponente |
|---|---|---|---|---|---|---|---|---|
| `eps 0, liv 0` | `eps 0, liv 1` | M | `-1.0000` | `1.30e-11` | `1.17e-11` | `1.08e-11` | `1.07e-11` | `0.477` |
| `eps 0, liv 0` | `eps 0.25, liv 0` | M | `+1.0032` | `6.46e-05` | `7.18e-04` | `2.01e-01` | `3.81e+00` | `1.757` |
| `eps 0, liv 0` | `eps 0.25, liv 4` | M | `-1.0041` | `2.24e-02` | -- | `7.52e-01` | `5.18e+00` | `1.661` |
| `eps 0, liv 0` | `eps 0.5, liv 0` | M | `+1.0126` | `2.66e-04` | `2.96e-03` | `6.45e-01` | `7.95e+00` | `1.756` |
| `eps 0, liv 0` | `eps 0.5, liv 4` | M | `-1.0136` | `2.43e-02` | -- | -- | `1.46e+01` | `1.558` |
| `eps 0, liv 0` | `eps 1, liv 0` | M | `+1.0495` | `1.19e-03` | `1.32e-02` | `1.81e+00` | `1.65e+01` | `1.756` |
| `eps 0, liv 0` | `eps 1, liv 4` | M | `-1.0506` | `2.64e-02` | -- | -- | `1.29e+02` | `1.665` |
| `eps 0, liv 1` | `eps 0.25, liv 0` | E0 | `-633.4856` | `3.28e-02` | `4.58e-01` | `1.13e+00` | `1.05e+00` | `1.853` |
| `eps 0, liv 1` | `eps 0.25, liv 0` | M | `-1.0032` | `6.46e-05` | `7.18e-04` | `2.01e-01` | `3.81e+00` | `1.757` |
| `eps 0, liv 1` | `eps 0.25, liv 4` | E0 | `+0.9984` | `5.01e-05` | -- | `1.41e-02` | `3.80e-02` | `1.650` |
| `eps 0, liv 1` | `eps 0.25, liv 4` | M | `+1.0041` | `2.24e-02` | -- | `7.52e-01` | `5.18e+00` | `1.661` |
| `eps 0, liv 1` | `eps 0.5, liv 0` | E0 | `-159.1156` | `3.27e-02` | `4.56e-01` | `1.16e+00` | `1.08e+00` | `1.853` |
| `eps 0, liv 1` | `eps 0.5, liv 0` | M | `-1.0126` | `2.66e-04` | `2.96e-03` | `6.45e-01` | `7.95e+00` | `1.756` |
| `eps 0, liv 1` | `eps 0.5, liv 4` | E0 | `+0.9938` | `1.98e-04` | -- | -- | `8.75e-02` | `1.555` |
| `eps 0, liv 1` | `eps 0.5, liv 4` | M | `+1.0136` | `2.43e-02` | -- | -- | `1.46e+01` | `1.558` |
| `eps 0, liv 1` | `eps 1, liv 0` | E0 | `-40.5064` | `3.21e-02` | `4.51e-01` | `1.22e+00` | `1.16e+00` | `1.855` |
| `eps 0, liv 1` | `eps 1, liv 0` | M | `-1.0495` | `1.19e-03` | `1.32e-02` | `1.81e+00` | `1.65e+01` | `1.756` |
| `eps 0, liv 1` | `eps 1, liv 4` | E0 | `+0.9759` | `7.51e-04` | -- | -- | `2.11e-01` | `1.654` |
| `eps 0, liv 1` | `eps 1, liv 4` | M | `+1.0506` | `2.64e-02` | -- | -- | `1.29e+02` | `1.665` |
| `eps 0.25, liv 0` | `eps 0.25, liv 4` | E0 | `-0.0016` | `3.17e-02` | -- | `8.96e+00` | `2.40e+01` | `1.650` |
| `eps 0.25, liv 0` | `eps 0.25, liv 4` | M | `-1.0009` | `2.24e-02` | -- | `4.58e-01` | `2.86e-01` | `1.660` |
| `eps 0.25, liv 0` | `eps 0.5, liv 0` | E0 | `+0.2512` | `1.43e-04` | `1.08e-03` | `2.21e-01` | `8.69e-01` | `1.587` |
| `eps 0.25, liv 0` | `eps 0.5, liv 0` | M | `+1.0094` | `2.02e-04` | `2.24e-03` | `3.70e-01` | `8.61e-01` | `1.756` |
| `eps 0.25, liv 0` | `eps 0.5, liv 4` | E0 | `-0.0016` | `3.16e-02` | -- | -- | `2.51e+01` | `1.555` |
| `eps 0.25, liv 0` | `eps 0.5, liv 4` | M | `-1.0104` | `2.43e-02` | -- | -- | `2.23e+00` | `1.558` |
| `eps 0.25, liv 0` | `eps 1, liv 0` | E0 | `+0.0639` | `6.79e-04` | `5.08e-03` | `7.56e-01` | `2.56e+00` | `1.584` |
| `eps 0.25, liv 0` | `eps 1, liv 0` | M | `+1.0462` | `1.12e-03` | `1.24e-02` | `1.34e+00` | `2.65e+00` | `1.756` |
| `eps 0.25, liv 0` | `eps 1, liv 4` | E0 | `-0.0015` | `3.11e-02` | -- | -- | `2.79e+01` | `1.652` |
| `eps 0.25, liv 0` | `eps 1, liv 4` | M | `-1.0473` | `2.63e-02` | -- | -- | `2.60e+01` | `1.665` |
| `eps 0.25, liv 4` | `eps 0.5, liv 0` | E0 | `-159.3667` | `3.26e-02` | -- | `1.15e+00` | `1.08e+00` | `1.725` |
| `eps 0.25, liv 4` | `eps 0.5, liv 0` | M | `-1.0085` | `2.17e-02` | -- | `6.07e-02` | `4.47e-01` | `1.613` |
| `eps 0.25, liv 4` | `eps 0.5, liv 4` | E0 | `+0.9953` | `1.48e-04` | -- | -- | `4.77e-02` | `1.555` |
| `eps 0.25, liv 4` | `eps 0.5, liv 4` | M | `+1.0095` | `1.85e-03` | -- | -- | `1.52e+00` | `1.533` |
| `eps 0.25, liv 4` | `eps 1, liv 0` | E0 | `-40.5703` | `3.21e-02` | -- | `1.22e+00` | `1.15e+00` | `1.726` |
| `eps 0.25, liv 4` | `eps 1, liv 0` | M | `-1.0452` | `2.08e-02` | -- | `6.04e-01` | `1.84e+00` | `1.612` |
| `eps 0.25, liv 4` | `eps 1, liv 4` | E0 | `+0.9774` | `7.01e-04` | -- | -- | `1.67e-01` | `1.654` |
| `eps 0.25, liv 4` | `eps 1, liv 4` | M | `+1.0463` | `3.84e-03` | -- | -- | `2.00e+01` | `1.643` |
| `eps 0.5, liv 0` | `eps 0.5, liv 4` | E0 | `-0.0062` | `3.15e-02` | -- | -- | `1.39e+01` | `1.555` |
| `eps 0.5, liv 0` | `eps 0.5, liv 4` | M | `-1.0010` | `2.41e-02` | -- | -- | `7.38e-01` | `1.558` |
| `eps 0.5, liv 0` | `eps 1, liv 0` | E0 | `+0.2546` | `5.36e-04` | `4.01e-03` | `4.38e-01` | `9.03e-01` | `1.584` |
| `eps 0.5, liv 0` | `eps 1, liv 0` | M | `+1.0364` | `9.20e-04` | `1.02e-02` | `7.08e-01` | `9.60e-01` | `1.755` |
| `eps 0.5, liv 0` | `eps 1, liv 4` | E0 | `-0.0061` | `3.09e-02` | -- | -- | `1.54e+01` | `1.652` |
| `eps 0.5, liv 0` | `eps 1, liv 4` | M | `-1.0375` | `2.61e-02` | -- | -- | `1.35e+01` | `1.664` |
| `eps 0.5, liv 4` | `eps 1, liv 0` | E0 | `-40.7609` | `3.19e-02` | -- | -- | `1.15e+00` | `1.581` |
| `eps 0.5, liv 4` | `eps 1, liv 0` | M | `-1.0354` | `2.26e-02` | -- | -- | `1.27e-01` | `1.539` |
| `eps 0.5, liv 4` | `eps 1, liv 4` | E0 | `+0.9820` | `5.53e-04` | -- | -- | `1.14e-01` | `1.557` |
| `eps 0.5, liv 4` | `eps 1, liv 4` | M | `+1.0365` | `1.99e-03` | -- | -- | `7.33e+00` | `1.567` |
| `eps 1, liv 0` | `eps 1, liv 4` | E0 | `-0.0241` | `3.04e-02` | -- | -- | `8.56e+00` | `1.654` |
| `eps 1, liv 0` | `eps 1, liv 4` | M | `-1.0010` | `2.51e-02` | -- | -- | `6.39e+00` | `1.662` |

### **Gli esponenti di `Vi`: da `0.477` a `1.855`, mediana `1.654`, su `49` coppie.**


### 5.4 IL SOLITONE: `D` con `c = c0 s` *(il controllo corretto)* E `D` col `c(s)` misurato *(`c4efc937`)*

| forma | `N` | `s` | legato | `D` (`c = c0 s`) | `D` (`c` misurato) |
|---|---|---|---|---|---|
| S1 | `1` | `0.85` | no | -- | -- |
| S1 | `1` | `0.9` | no | -- | -- |
| S1 | `1` | `0.95` | no | -- | -- |
| S1 | `1` | `0.99` | no | -- | -- |
| S1 | `1` | `1` | no | -- | -- |
| S1 | `10` | `0.85` | no | -- | -- |
| S1 | `10` | `0.9` | no | -- | -- |
| S1 | `10` | `0.95` | no | -- | -- |
| S1 | `10` | `0.99` | no | -- | -- |
| S1 | `10` | `1` | no | -- | -- |
| S1 | `100` | `0.85` | si' | `-1.22e-08` | `-1.7221` |
| S1 | `100` | `0.9` | si' | `-1.65e-08` | `-3.7011` |
| S1 | `100` | `0.95` | si' | `+3.16e-09` | -- |
| S1 | `100` | `0.99` | si' | `+3.53e-09` | -- |
| S1 | `100` | `1` | si' | `+3.43e-09` | -- |
| S3 | `1` | `0.85` | si' | `-1.77e-08` | `-5.1851` |
| S3 | `1` | `0.9` | si' | `-1.32e-08` | `-8.4577` |
| S3 | `1` | `0.95` | si' | `+2.73e-09` | `-18.5754` |
| S3 | `1` | `0.99` | si' | `+1.34e-10` | `-105.8408` |
| S3 | `1` | `1` | si' | `-7.11e-09` | -- |
| S3 | `10` | `0.85` | si' | `-1.84e-08` | `-3.2817` |
| S3 | `10` | `0.9` | si' | `-1.21e-08` | `-5.7639` |
| S3 | `10` | `0.95` | si' | `+8.56e-09` | `-14.3074` |
| S3 | `10` | `0.99` | si' | `+2.99e-09` | `-98.4418` |
| S3 | `10` | `1` | si' | `-9.64e-10` | -- |
| S3 | `100` | `0.85` | si' | `-1.78e-08` | `-1.4053` |
| S3 | `100` | `0.9` | si' | `-1.26e-08` | `-2.5789` |
| S3 | `100` | `0.95` | si' | `+7.06e-09` | `-7.0609` |
| S3 | `100` | `0.99` | si' | `+3.29e-09` | `-66.9607` |
| S3 | `100` | `1` | si' | `-3.94e-09` | -- |
| S4 | `1` | `0.85` | no | -- | -- |
| S4 | `1` | `0.9` | no | -- | -- |
| S4 | `1` | `0.95` | no | -- | -- |
| S4 | `1` | `0.99` | no | -- | -- |
| S4 | `1` | `1` | no | -- | -- |
| S4 | `10` | `0.85` | si' | `-2.05e-08` | `-5.2948` |
| S4 | `10` | `0.9` | si' | `-1.68e-08` | `-7.8400` |
| S4 | `10` | `0.95` | si' | `+5.84e-09` | `-12.8771` |
| S4 | `10` | `0.99` | si' | `+5.38e-09` | -- |
| S4 | `10` | `1` | si' | `-9.57e-11` | -- |
| S4 | `100` | `0.85` | si' | `-1.83e-08` | `-4.5122` |
| S4 | `100` | `0.9` | si' | `-1.33e-08` | `-7.6144` |
| S4 | `100` | `0.95` | si' | `+4.85e-09` | `-17.6205` |
| S4 | `100` | `0.99` | si' | `+6.62e-09` | `-91.4926` |
| S4 | `100` | `1` | si' | `-5.98e-11` | -- |

### 5.5 LA RELAZIONE DI EINSTEIN `Q = omega(0) omega''(0)/v^2` *(lato `64`)*

| `eps` | `s` | ramo | `(i)` principale | `(i)` continua | `(ii)` principale | `(ii)` continua | `(iii)` a meta' | coppia |
|---|---|---|---|---|---|---|---|---|
| `0` | `0.02` | Dt 0.0341 w0 +0.0000 | `-0.0000` | `+0.0000` | `-3.6782` | `-3.6782` | `-1.8391` | Dt 0.0341 w0 -0.1257 |
| `0` | `0.02` | Dt 0.0341 w0 -0.1257 | `-3.6782` | `-3.6782` | `-0.0000` | `+0.0000` | `-1.8391` | Dt 0.0341 w0 +0.0000 |
| `0` | `0.05` | Dt 0.0852 w0 -0.0000 | `+0.0000` | `+0.0000` | `-3.6830` | `-3.6830` | `-1.8415` | Dt 0.0852 w0 -0.3142 |
| `0` | `0.05` | Dt 0.0852 w0 -0.3142 | `-3.6830` | `-3.6830` | `-0.0000` | `-0.0000` | `-1.8415` | Dt 0.0852 w0 -0.0000 |
| `0` | `0.1` | Dt 0.1696 w0 +0.0000 | `-0.0000` | `+0.0000` | `-3.7005` | `-3.7005` | `-1.8502` | Dt 0.1696 w0 -0.6283 |
| `0` | `0.1` | Dt 0.1696 w0 -0.6283 | `-3.7005` | `-3.7005` | `+0.0000` | `+0.0000` | `-1.8502` | Dt 0.1696 w0 +0.0000 |
| `0` | `0.2` | Dt 0.3326 w0 -0.0000 | `+0.0000` | `+0.0000` | `-3.7749` | `-3.7749` | `-1.8874` | Dt 0.3326 w0 -1.2566 |
| `0` | `0.2` | Dt 0.3326 w0 -1.2566 | `-3.7749` | `-3.7749` | `-0.0000` | `-0.0000` | `-1.8874` | Dt 0.3326 w0 -0.0000 |
| `0` | `0.3` | Dt 0.4807 w0 +0.0000 | `-0.0000` | `-0.0000` | `-3.9169` | `-3.9169` | `-1.9584` | Dt 0.4807 w0 -1.8850 |
| `0` | `0.3` | Dt 0.4807 w0 -1.8850 | `-3.9169` | `-3.9169` | `+0.0000` | `+0.0000` | `-1.9584` | Dt 0.4807 w0 +0.0000 |
| `0` | `0.5` | Dt 0.6858 w0 -0.0000 | `+0.0000` | `+0.0000` | `+4.5747` | `-4.5747` | `-2.2873` | Dt 0.6858 w0 -3.1416 |
| `0` | `0.5` | Dt 0.6858 w0 -3.1416 | `-4.5747` | `-4.5747` | `+0.0000` | `+0.0000` | `+2.2873` | Dt 0.6858 w0 -0.0000 |
| `0` | `0.7` | Dt 0.6563 w0 +0.0000 | `-0.0000` | `-0.0000` | `+2.8652` | `-6.6856` | `+1.4326` | Dt 0.6563 w0 +1.8850 |
| `0` | `0.7` | Dt 0.6563 w0 +1.8850 | `+2.8652` | `-6.6856` | `+0.0000` | `+0.0000` | `+1.4326` | Dt 0.6563 w0 +0.0000 |
| `0` | `0.9` | Dt 0.2836 w0 +0.0000 | `-0.0000` | `+0.0000` | `+2.1914` | `-19.7228` | `+1.0957` | Dt 0.2836 w0 +0.6283 |
| `0` | `0.9` | Dt 0.2836 w0 +0.6283 | `+2.1914` | `-19.7228` | `+0.0000` | `+0.0000` | `+1.0957` | Dt 0.2836 w0 +0.0000 |
| `0` | `0.95` | Dt 0.1454 w0 +0.0000 | `-0.0000` | `-0.0000` | `+2.0925` | `-39.7570` | `+1.0462` | Dt 0.1454 w0 +0.3142 |
| `0` | `0.95` | Dt 0.1454 w0 +0.3142 | `+2.0925` | `-39.7570` | `+0.0000` | `+0.0000` | `+1.0462` | Dt 0.1454 w0 +0.0000 |
| `0` | `0.99` | Dt 0.0280 w0 +0.0628 | `+1.3609` | `-134.7269` | `+0.0000` | `+0.0000` | `+0.6804` | Dt 0.0280 w0 -0.0000 |
| `0` | `0.99` | Dt 0.0280 w0 -0.0000 | `+0.0000` | `+0.0000` | `+1.3609` | `-134.7269` | `+0.6804` | Dt 0.0280 w0 +0.0628 |
| `0.25` | `0.02` | Dt 0.0339 w0 +0.0002 | `-0.0058` | `-0.0058` | `-3.7102` | `-3.7102` | -- | NESSUNA COPPIA |
| `0.25` | `0.02` | Dt 0.0341 w0 -0.1259 | `-3.6865` | `-3.6865` | `-0.0058` | `-0.0058` | -- | NESSUNA COPPIA |
| `0.25` | `0.05` | Dt 0.0846 w0 +0.0005 | `-0.0058` | `-0.0058` | `-3.7150` | `-3.7150` | -- | NESSUNA COPPIA |
| `0.25` | `0.05` | Dt 0.0878 w0 -0.3147 | `-3.5675` | `-3.5675` | `-0.0056` | `-0.0056` | -- | NESSUNA COPPIA |
| `0.25` | `0.1` | Dt 0.1684 w0 +0.0010 | `-0.0057` | `-0.0057` | `-3.7323` | `-3.7323` | -- | NESSUNA COPPIA |
| `0.25` | `0.1` | Dt 0.1961 w0 -0.6293 | `-3.1537` | `-3.1537` | `-0.0048` | `-0.0048` | -- | NESSUNA COPPIA |
| `0.25` | `0.2` | Dt 0.3303 w0 +0.0017 | `-0.0052` | `-0.0052` | `-3.8061` | `-3.8061` | -- | NESSUNA COPPIA |
| `0.25` | `0.2` | Dt 0.7072 w0 -1.2584 | `-1.6642` | `-1.6642` | `-0.0023` | `-0.0023` | -- | NESSUNA COPPIA |
| `0.25` | `0.3` | Dt 0.4776 w0 +0.0020 | `-0.0043` | `-0.0043` | `-3.9469` | `-3.9469` | -- | NESSUNA COPPIA |
| `0.25` | `0.5` | Dt 0.6823 w0 +0.0000 | `-0.0000` | `-0.0000` | `+4.5981` | `-4.5981` | -- | NESSUNA COPPIA |
| `0.25` | `0.7` | Dt 0.6580 w0 -0.0111 | `+0.0168` | `+0.0168` | `+2.8747` | `-6.6517` | -- | NESSUNA COPPIA |
| `0.25` | `0.9` | Dt 0.3327 w0 -0.0701 | `+0.2089` | `+0.2089` | `+2.0818` | `-16.6469` | -- | NESSUNA COPPIA |
| `0.25` | `0.9` | Dt 0.6021 w0 +0.6984 | `+0.9919` | `-7.9320` | `+0.0995` | `+0.0995` | -- | NESSUNA COPPIA |
| `0.25` | `0.95` | Dt 0.2444 w0 -0.1268 | `+0.5127` | `+0.5127` | `+1.7826` | `-23.6143` | -- | NESSUNA COPPIA |
| `0.25` | `0.95` | Dt 0.3467 w0 +0.4410 | `+1.1839` | `-15.6833` | `+0.3405` | `+0.3405` | -- | NESSUNA COPPIA |
| `0.25` | `0.99` | Dt 0.2052 w0 -0.2180 | `+1.0509` | `+1.0509` | `+1.3538` | `-28.9312` | -- | NESSUNA COPPIA |
| `0.25` | `0.99` | Dt 0.2717 w0 +0.2809 | `+1.0008` | `-21.3887` | `+0.7769` | `+0.7769` | -- | NESSUNA COPPIA |
| `0.5` | `0.02` | Dt 0.0332 w0 +0.0008 | `-0.0238` | `-0.0238` | `-3.8058` | `-3.8058` | -- | NESSUNA COPPIA |
| `0.5` | `0.02` | Dt 0.0335 w0 -0.1265 | `-3.7641` | `-3.7641` | `-0.0235` | `-0.0235` | -- | NESSUNA COPPIA |
| `0.5` | `0.05` | Dt 0.0829 w0 +0.0020 | `-0.0236` | `-0.0236` | `-3.8105` | `-3.8105` | -- | NESSUNA COPPIA |
| `0.5` | `0.05` | Dt 0.0887 w0 -0.3161 | `-3.5508` | `-3.5508` | `-0.0220` | `-0.0220` | -- | NESSUNA COPPIA |
| `0.5` | `0.1` | Dt 0.1650 w0 +0.0038 | `-0.0232` | `-0.0232` | `-3.8275` | `-3.8275` | -- | NESSUNA COPPIA |
| `0.5` | `0.1` | Dt 0.2233 w0 -0.6321 | `-2.8023` | `-2.8023` | `-0.0170` | `-0.0170` | -- | NESSUNA COPPIA |
| `0.5` | `0.2` | Dt 0.3237 w0 +0.0068 | `-0.0211` | `-0.0211` | `-3.8997` | `-3.8997` | -- | NESSUNA COPPIA |
| `0.5` | `0.3` | Dt 0.4684 w0 +0.0081 | `-0.0173` | `-0.0173` | `-4.0375` | `-4.0375` | -- | NESSUNA COPPIA |
| `0.5` | `0.5` | Dt 0.6718 w0 +0.0000 | `-0.0000` | `+0.0000` | `+4.6696` | `-4.6696` | -- | NESSUNA COPPIA |
| `0.5` | `0.7` | Dt 0.6622 w0 -0.0434 | `+0.0654` | `+0.0654` | `+2.9056` | `-6.5619` | -- | NESSUNA COPPIA |
| `0.5` | `0.9` | Dt 0.0132 w0 +0.6126 | `+31.6758` | `-293.2259` | `-0.8144` | `-0.8144` | -- | NESSUNA COPPIA |
| `0.5` | `0.9` | Dt 0.4253 w0 -0.2284 | `+0.5344` | `+0.5344` | `+2.0044` | `-12.6953` | -- | NESSUNA COPPIA |
| `0.5` | `0.95` | Dt 0.0163 w0 +0.3054 | `+13.4851` | `-263.9073` | `-0.3845` | `-0.3845` | -- | NESSUNA COPPIA |
| `0.5` | `0.95` | Dt 0.3735 w0 -0.3413 | `+0.9094` | `+0.9094` | `+1.7465` | `-14.9945` | -- | NESSUNA COPPIA |
| `0.5` | `0.95` | Dt 1.0325 w0 +0.6555 | `+0.6190` | `-5.3146` | `+0.3223` | `+0.3223` | -- | NESSUNA COPPIA |
| `0.5` | `0.99` | Dt 0.0189 w0 +0.0609 | `+2.4079` | `-245.8286` | `-0.0745` | `-0.0745` | -- | NESSUNA COPPIA |
| `0.5` | `0.99` | Dt 0.3448 w0 -0.4645 | `+1.3423` | `+1.3423` | `+1.5238` | `-16.6327` | -- | NESSUNA COPPIA |
| `0.5` | `0.99` | Dt 0.7162 w0 +0.5273 | `+0.7260` | `-7.9242` | `+0.6395` | `+0.6395` | -- | NESSUNA COPPIA |
| `1` | `0.02` | Dt 0.0308 w0 +0.0031 | `-0.1008` | `-0.1008` | `-4.1830` | `-4.1830` | -- | NESSUNA COPPIA |
| `1` | `0.02` | Dt 0.0310 w0 -0.1288 | `-4.1451` | `-4.1451` | `-0.0999` | `-0.0999` | -- | NESSUNA COPPIA |
| `1` | `0.05` | Dt 0.0768 w0 +0.0077 | `-0.1002` | `-0.1002` | `-4.1876` | `-4.1876` | -- | NESSUNA COPPIA |
| `1` | `0.05` | Dt 0.0813 w0 -0.3219 | `-3.9512` | `-3.9512` | `-0.0946` | `-0.0946` | -- | NESSUNA COPPIA |
| `1` | `0.1` | Dt 0.1529 w0 +0.0150 | `-0.0982` | `-0.0982` | `-4.2040` | `-4.2040` | -- | NESSUNA COPPIA |
| `1` | `0.1` | Dt 0.1964 w0 -0.6433 | `-3.2641` | `-3.2641` | `-0.0762` | `-0.0762` | -- | NESSUNA COPPIA |
| `1` | `0.2` | Dt 0.3000 w0 +0.0269 | `-0.0897` | `-0.0897` | `-4.2736` | `-4.2736` | -- | NESSUNA COPPIA |
| `1` | `0.2` | Dt 2.1157 w0 -1.2836 | `-0.6007` | `-0.6007` | `-0.0126` | `-0.0126` | -- | NESSUNA COPPIA |
| `1` | `0.3` | Dt 0.4347 w0 +0.0321 | `-0.0737` | `-0.0737` | `-4.4044` | `-4.4044` | -- | NESSUNA COPPIA |
| `1` | `0.5` | Dt 0.6309 w0 +0.0000 | `-0.0000` | `-0.0000` | `+4.9726` | `-4.9726` | -- | NESSUNA COPPIA |
| `1` | `0.7` | Dt 0.0796 w0 +1.7683 | `+21.3612` | `-54.5386` | `-1.4088` | `-1.4088` | -- | NESSUNA COPPIA |
| `1` | `0.7` | Dt 0.6668 w0 -0.1620 | `+0.2426` | `+0.2426` | `+3.0642` | `-6.3412` | -- | NESSUNA COPPIA |
| `1` | `0.9` | Dt 0.1724 w0 +0.5686 | `+3.2377` | `-32.5374` | `-0.3398` | `-0.3398` | -- | NESSUNA COPPIA |
| `1` | `0.9` | Dt 0.5818 w0 -0.6241 | `+1.0706` | `+1.0706` | `+2.1484` | `-8.6297` | -- | NESSUNA COPPIA |
| `1` | `0.95` | Dt 0.1904 w0 +0.2813 | `+1.4545` | `-31.0373` | `-0.1701` | `-0.1701` | -- | NESSUNA COPPIA |
| `1` | `0.95` | Dt 0.5609 w0 -0.8017 | `+1.4268` | `+1.4268` | `+1.9860` | `-9.1967` | -- | NESSUNA COPPIA |
| `1` | `0.99` | Dt 0.2028 w0 +0.0557 | `+0.2711` | `-30.2817` | `-0.0345` | `-0.0345` | -- | NESSUNA COPPIA |
| `1` | `0.99` | Dt 0.5463 w0 -0.9589 | `+1.7527` | `+1.7527` | `+1.8676` | `-9.6170` | -- | NESSUNA COPPIA |
| `1` | `0.99` | Dt 1.0565 w0 +1.0217 | `+0.9656` | `-4.9723` | `+0.9062` | `+0.9062` | -- | NESSUNA COPPIA |

### 5.6 LA LETTURA, IN TRE RIGHE *(nessuna conclusione oltre le tabelle)*

1. ### **A `eps 0` IL PRINCIPIO DI EQUIVALENZA DEI RAMI TIENE, con la fase seguita da `s` piccolo:** ### **`|D| <= 4.2e-10` su ogni ramo** *(`E0 = 0` e `-2 pi` costanti)*, ### **e
   `H_eff` a `k = 0` non dipende da `s`** *(`delta ~ 1e-14`)*: ### **il `D = -2 pi/s^2` di `c4efc937` sul ramo alto era LA FASE RIPORTATA.** ### **Ma a `k != 0` e a `eps > 0` no:**
   ### **`delta ~ s^2`** *(non `s`: il palindromo)*, ### **`0.55`-`0.66` vicino al cono**; ### **`|D|` fino a `~3` a `eps > 0`**; ### **e `M` non scala come `E0`** *(gli esponenti di `Vi`
   da `0.48` a `1.85`, mediana `1.65`)*.
2. ### **IL SOLITONE CON `c = c0 s` OBBEDISCE AL BIT** *(`|D| <= 2.0e-8`)*: ### **la sua violazione in `c4efc937`** *(`-8.46` .. `-2.58`)* ### **e' TUTTA nel termine di moto**
   *(`c(s)` misurato non e' proporzionale a `s`: `c ~ v^2/(2 Dt)`, `Dt ~ pi s (1 - s)`)*. ### **L'errore n.46 del guardiano e' confermato: il controllo giusto era questo.**
3. ### **LA RELAZIONE DI EINSTEIN SCEGLIE LO ZERO A META', MA NON LONTANO DAL CONO E SOLO DOVE C'E' UNA COPPIA:** ### **`(iii)` `Q = 1.10`, `1.05` a `s 0.9`, `0.95`** *(e `0.68` a `0.99`,
   dove la curvatura non si risolve)*; ### **`(i)` e `(ii)` danno `0` su un ramo e `~2.2` (principale) o `-3.7`..`-135` (continua) sull'altro**; ### **a `eps > 0` NESSUNA COPPIA** *(`0` su `54` righe)*: ### **lo zero a
   meta' li' non e' definito.**

### **PER LE TRE STRADE DELLA REGOLA DI SCALA** *(informazione, non una scelta)*: ### **`s -> 0`: la violazione si spegne come `s^2`** *(il passo diventa `exp(-i s H)` con `H` fisso; e il
solitone con `c ~ s` obbedisce)*; ### **`s` fisso: resta una violazione FISSA, `delta(s)` e i `Vi(s)` di quel `s`** *(a `s 0.3`: `delta` continua `7.8e-3`-`4.8e-2`)*; ### **`s -> 1`: d'ordine `1`**
*(`delta 0.55`-`0.66` continua, `Vi` fino a `~129` a `s 0.99`)*.

### **PER «QUALE `2 pi k`»** *(diagnosi, non decisione)*: ### **fra le tre letture, solo lo zero A META' di una coppia da' `Q ~ 1` la' dove la curvatura si risolve** *(`s 0.9`-`0.95`, `eps 0`)*;
### **la fase CONTINUA da `s` piccolo da' invece `D = 0` a `eps 0` su tutti e due i rami, ma `Q = 0` o `~ -2/(1 - s)`.** ### **Le due proprieta' della relativita' generale** *(`D = 0` e
Einstein)* ### **la convenzione di oggi non le da' insieme in nessuna lettura** *(e a `eps > 0` lo zero a meta' manca)*.
