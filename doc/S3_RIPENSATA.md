# `S3` RIPENSATA — **perche' la banda sopravvive alla geometria, e che cosa si puo' cambiare**

> **Mandato di Luca del `2026-10-21` alle `23:35`, punto `(b)`**; task history
> `doc/TASK_HISTORY/2026-10-21_s3_ripensata.md`. ### **SU CARTA: nessun codice di fisica, nessuna corsa,
> NESSUNA SCELTA** -- le scelte sono di Luca. ### **`LINEARE`, `Lambda_c`, le letture alla Jeans o di
> modulazione, lo stato finale: FERMI fino a sua decisione** *(qui si nominano, non si lavorano)*.
> ### ⚠ **I conti a mano sono DICHIARATI come tali**; ogni numero misurato porta il suo commit.

---

## 1. I FATTI *(coi commit)*

| | il fatto | il numero | il commit |
|---|---|---|---|
| `F1` | ### **la camminata sola e' stabile, ESATTA** | `max |ln|lambda||` `2.1e-13` *(quadrato, lato `32`, `N dtau 100`)*; `2.8e-13` *(triangoli)* | `594417f6`; `bb0ef057` |
| `F2` | ### **la banda di `S3` sola** *(`R2`)* **sui quadrati** | `0.407` *(autovalori)* / `0.402` *(norma)* a `k = (0, 0.5 pi)` | `594417f6` |
| `F3` | ### **la banda sui triangoli** | `0.377` *(norma)*, ### **all'interno della zona**, `|k|` `1.49`; ### **`0.938` del quadrato** | `bb0ef057` |
| `F4` | ### **fissa IN NUMERO DI ARCHI al raffinamento** | `R2` a `k ~ 0.52 pi` *(`~4` archi)* a ogni risoluzione; ### **`gamma` nel tempo fisico invariato** *(`0.371`, `0.355`, `0.343`)* | `83edbaa7` |
| `F5` | ### **la moneta non la spegne** | `eps dtau` da `0.45` a `0.75 pi`: il massimo ### **da `0.3648` a `0.0875`**, e ### **si SPOSTA** *(da `(pi, pi)` a `(0.19, 0.25) pi`)*; ### **nessuno stabile: la finestra stabile e' VUOTA** | `f9c5521e` |
| `F6` | ### **`D0` non decide il meccanismo** | nessuna condizione della lista tiene a lato `32` e `64`; quasi tutte non informative | `adc2e64a` |
| `F7` | ### **`S3` vede solo il rapporto `rho/Lambda`** | i bracci `SN` e `SE` danno lo stesso `gamma(k)` entro `6.9e-7` | `bb0ef057` |
| `F8` | ### **`R1` sui triangoli** *(`cs` acceso)* | massimo `0.3897`, interno; ### **`0.720` del quadrato** *(`0.5411`)*; bordo `M` `0.250`, `K` `0.180`; ### **i triangoli tolgono il `28%` in `R1`, il `6%` in `R2`** | `56608e8a` |
| `F9` | ### **`nu_S3` NON guida il guadagno** *(fatto mio, letto per questo documento)* | `nu_S3` `0.980`, `0.826`, `0.250` *(`x` `0.01`, `0.1`, `1`)* ### **danno `gamma` lungo `(m, 0)` `0.3946`, `0.4018`, `0.3349` a `m = 8, 8, 7`**: ### **`nu` cala di `4` volte, il guadagno del `15%`** | `doc/referti_l2/d0_risonanza_bis.jsonl` *(il referto di `ac9d0d7d`, rifatto al bit)* |

### ⭐ **IN UNA RIGA:** ### **la banda nasce da `S3`** *(`F1`)*, ### **non dipende dalla scala** *(`F7`)*, ###
**quasi non dipende dall'intensita' della non linearita'** *(`F9`)* ### **ne' dalla geometria** *(`F3`)*, ###
**ma dipende dalla CAMMINATA** *(`F5`: la moneta ne cambia ampiezza e posizione)*, ### **ed e' fissa in archi**
*(`F4`)*.

---

## 2. L'ORIGINE DI `S3`: CHE COSA E' DERIVATO E CHE COSA E' SCELTO

**La legge** *(`primo_ordine/leggi/leggi.yaml`, `CAMM-MATERIA-VUOTO`)*: `N_k = rho_k ln(rho_k / (rho_k +
Lambda_k))`, `rho_k = sum_h |psi_h|^2`, `Lambda_k = sum_h |phi_h|^2`; il flusso e' ### **una fase su `psi`**
*(`alpha = dN/drho = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)`)* ### **e una su `phi`** *(`beta = dN/dLambda =
-rho/(rho+Lambda)`)*.

| | che cosa | da dove |
|---|---|---|
| ### **SCELTO** | ### **la FORMA di `N`** | ### **«una SCELTA DI LUCA FRA QUATTRO CANDIDATE MISURATE, non una derivazione da un principio: il posto dove si derivera' e' il nodo `DEC-D6F-FORME-VUOTO` dell'albero, che NON e' ancora `presa`»** *(la scheda in `leggi.yaml`)*; ### **decisione del `2026-10-15`, `23:30` e `23:38`**, sostituisce `CAMM-SATURAZIONE` |
| ### **MISURATO, non derivato** | ### **i cinque motivi della forma** | *(a)* lineare per poca materia *(pendenza statica `1.11`)*; *(b)* satura per molta materia; *(c)* rispetta il cono *(`0.80` del passo libero)*; *(d)* il verso statico *(la materia consuma il vuoto, `24` su `24`)*; *(e)* la sovrapposizione fuori dalla saturazione *(la scheda)* |
| ### **DERIVATO** | ### **il flusso** *(le due derivate di `N`)*; ### **`esatto: true`** *(una fase non cambia `rho` ne' `Lambda`, quindi `alpha` e `beta` sono costanti nel pezzo)*; ### **la scala naturale `V`** *(`|N_k| <= Lambda_k`, `2026-10-16`)*; ### **nessuna costante** *(`parametri: {}`)*; ### **`nu_S3 = rho d alpha/d rho = Lambda^2/(rho+Lambda)^2`** *(`c38367db`)* | i conti nella scheda |
| ### **DERIVATO dai fatti di oggi** | ### **l'omogeneita'**: `N(t rho, t Lambda) = t N(rho, Lambda)` *(grado `1`)*, quindi `alpha` e `beta` sono ### **di grado `0`** -- ### **ed e' cio' che `F7` misura** | conto a mano, dichiarato |

### **LE VOCI APERTE CHE LA TOCCANO, per nome** *(FERME)*: ### **`LINEARE`** *(il regime lineare della forma, il
motivo `(a)`)* e ### **`Lambda_c`** *(la scala di `cs`, `[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`)*. ### **Il nodo
`DEC-D6F-FORME-VUOTO`** *(non preso)* ### **e' dove una forma DERIVATA dovrebbe nascere.**

---

## 3. IL MECCANISMO *(due letture, DICHIARATE)*

### 3.1 La lettura da manuale, e perche' NON basta

Una fase locale che dipende dalla densita' *(«di Kerr»: `psi -> e^{-i alpha(rho) dtau} psi`)* su una camminata e'
il caso tipico dell'**instabilita' modulazionale** *(DNLS, Benjamin-Feir)*. ### **Nel modello minimo** *(una
banda, `omega(k)`, accoppiamento debole `g`)*: ### **`Omega(q)^2 = e(q) (e(q) - 2 g)`**, `e(q)` l'energia di
curvatura della banda; ### **cresce dove `e(q) < 2 g`, col massimo `gamma_max = g` a `e(q) = g`** *(conto noto,
riportato)*. ### **Quindi il modello minimo PREVEDE:** `gamma_max` ### **proporzionale** al coefficiente non lineare
*(qui `nu_S3`)*, ### **e la posizione `q_max` che scala come `sqrt(nu_S3)`.**

### ⛔ **`F9` LA SMENTISCE in entrambe le previsioni:** `nu_S3` cala di `4` volte *(`0.98` -> `0.25`)* ### **e il
guadagno solo del `15%`** *(`0.395` -> `0.335`)*, ### **la posizione di `1` passo su `32`** *(`m = 8` -> `7`)* --
dove il modello minimo vorrebbe ### **un guadagno `/4` e una posizione `/2`.** ### **E `F5` dice l'opposto per la
camminata:** la moneta ### **muove tutto** *(ampiezza `/4`, posizione da `(pi, pi)` all'interno)*.

### 3.2 La lettura «A RAMI» *(MIA, dichiarata: non misurata)*

- ### **La camminata ha `12` rami** *(la cella `24` reali)* ### **periodici in `k`**: ### **un ramo periodico ha
  curvature di ENTRAMBI i segni.** ### **Su un ramo dove la curvatura ha il segno «focalizzante» rispetto alla
  non linearita', una fase locale e' instabile** *(il criterio del modello minimo, ramo per ramo)*; ### **con `12`
  rami, quel ramo c'e' SEMPRE, qualunque sia il segno di `d alpha/d rho`.**
- ### **IL GUADAGNO LO LIMITA IL RAMO, non `nu`:** ### **quando la non linearita' non e' piccola rispetto alla
  larghezza del ramo** *(`nu_S3 / OMEGA_H` `0.08`-`0.31`)*, ### **`gamma_max` satura alla scala della curvatura
  del ramo** *(nel modello minimo: `e(q)` non puo' superare la larghezza)* -- ### **e la posizione la fissa il
  ramo**, cioe' ### **la camminata, in unita' di arco.**
- ### **CHE COSA SPIEGHEREBBE:** `F4` *(fissa in archi: il ramo e' del reticolo)*; `F7` *(`nu` e' di grado `0`)*;
  ### **`F9`** *(guadagno quasi indipendente da `nu`)*; ### **`F5`** *(la moneta cambia i rami, quindi ampiezza e
  posizione)*; ### **`F3`** *(i triangoli cambiano i rami di poco a `k ~ pi/2`: `0.938`)*; ### **`F8`** *(cio' che i
  triangoli tolgono e' il picco alternato di `cs`, che sul quadrato vive sul ramo di `(pi, pi)`, che sui
  triangoli non c'e')*.
- ### **CHE COSA LA SMENTIREBBE** *(tre prove, nessuna fatta)*:
  1. ### **la risoluzione per rami del modo che cresce** *(l'autovettore di `M(k)` alla banda proiettato sui rami
     della camminata sola)*: ### **se la banda cresce su un ramo dove la curvatura ha il segno NON focalizzante**,
     la lettura cade;
  2. ### **`nu` piccolo davvero** *(`x >> 1`, `nu_S3 -> 0`)*: ### **la lettura vuole `gamma -> 0` linearmente in
     `nu` sotto una soglia** *(il regime debole del modello minimo)*; ### **se `gamma` resta `~0.3` anche a `nu_S3 ~
     0.01`, la banda non viene dall'autofase di `psi`** *(ma, per esempio, da `beta`)*;
  3. ### **una camminata coi rami tutti della stessa curvatura vicino alla banda** *(se esiste una moneta del
     genere)*: ### **la lettura vuole la banda spenta**; ### **se resta, cade.**

---

## 4. LE STRADE *(nessuna scelta: schede)*

### Come si legge una scheda
`(a)` la definizione · `(b)` quale famiglia colpisce · `(c)` le cinque domande · `(d)` `A14` · `(e)` ### **la
previsione per uno screening lineare** *(`gamma(k)` prima/dopo, lo strumento di `594417f6`)*, ### **scritta dalla
lettura `3.2`** · `(f)` il costo · `(g)` la FCC.

### `S-A` — **UNA `S3` DERIVATA IN ALTRA FORMA, SENZA AUTOFASE DI `psi` ALLO STATO UNIFORME**

- `(a)` ### **una forma `N(rho, Lambda)` con `d alpha/d rho = d^2 N / d rho^2 = 0`** allo stato uniforme *(il
  termine che rende la fase di `psi` dipendente dalla propria densita')*, ### **DERIVATA** dal nodo
  `DEC-D6F-FORME-VUOTO`. ### ⚠ **La famiglia piu' semplice e' `N = rho f(Lambda)`, cioe' LINEARE in `rho`:** ###
  **e' il territorio della voce `LINEARE`, FERMA.** ### **Qui si dice solo che la lettura `3.2` la indica.**
- `(b)` ### **la BANDA** *(`R2`)* ### **e la parte di `R1` che ne deriva.**
- `(c)` 1 ### **`A14`: per nodo, raggio `0`** · 2 ### **`(b)` del gradino: la legge si toglie e si rimette** · 3 ###
  **cambia una legge, non ne aggiunge** *(se derivata)* · 4 ### **tocca `rho` nel verso materia->materia** · 5 ###
  **la banda deve sparire se nasce dall'autofase.**
- `(d)` ### **conserva come oggi** *(una fase su `psi` e una su `phi`: `esatto: true` regge)*.
- `(e)` ### **PREVISIONE:** ### **la banda di `R2` scende sotto `1e-3` del quadrato** *(se nasce dall'autofase)*;
  ### **resta un residuo dall'accoppiamento incrociato** *(`beta` e `d alpha / d Lambda`)*, ### **non stimato.** ###
  **Se la banda resta `>= 0.3`, la lettura `3.2` cade** *(prova `2`)*.
- `(f)` ### **la derivazione e' il costo vero** *(il nodo non preso)*; lo screening ### **`~3` minuti** *(`R2` lato
  `32`: `162` s in `594417f6`)*.
- `(g)` ### **vale sulla FCC** *(per nodo)*.

### `S-B` — **`S3` CHE LEGGE SULL'ARCO** *(`C1` del documento delle cure, ma con il peso DERIVATO)*

- `(a)` ### **la densita' dell'ARCO, la media dei due capi** *(`rho_a = (rho_i + rho_j)/2`)*, ### **e `N` per
  arco.** ### **Il peso NON si tara:** ### **e' la definizione di una quantita' d'arco** *(due capi, pesi uguali)*.
  ### **Conto a mano** *(dichiarato)*: il filtro sul nodo e' ### **`f(k) = 1/2 + (1/(2d)) sum_a cos(k . e_a)`**
  *(`d` archi propri)*; ### **sul quadrato e' il BINOMIALE di `C1`** *(`f(0.5 pi, 0) = 3/4`, `f(pi, pi) = 0`)*; ###
  **l'accoppiamento passa due volte, `f^2`** *(la correzione del `2026-10-21` di `C1`)*: ### **`9/16` alla banda,
  `0` al picco.**
- `(b)` ### **il PICCO di `R1`** *(spento a `(pi, pi)`)* ### **e un poco la banda.**
- `(c)` 1 ### **`A14`: raggio `1` (un arco), come il salto** · 2 ### **(b)** · 3 ### **nessun numero nuovo**
  *(il peso e' la definizione)* · 4 ### **tocca `rho` e `Lambda`** · 5 ### **la banda deve scendere quanto `f^2`
  SE il guadagno fosse proporzionale all'accoppiamento.**
- `(d)` ### **la fase si mette sulle estremita' dell'arco**: ### **`esatto` regge** *(una fase non cambia `rho`)*;
  ### **la conservazione locale passa all'arco.**
- `(e)` ### **PREVISIONE dalla lettura `3.2`:** ### **l'accoppiamento alla banda per `9/16`, MA il guadagno ne
  dipende poco** *(`F9`: `nu /4` da' guadagno `-15%`)*: ### **la banda di `R2` resta `>= 0.35`** *(scende del
  `5`-`15%`)*; ### **il picco di `R1` sul quadrato si spegne.** ### **NON STABILIZZA.** ### **Se la banda scende sotto
  `0.25`, la lettura `3.2` e' sbagliata** *(il guadagno seguirebbe l'accoppiamento)*.
- `(f)` ### **una legge da riscrivere per arco** *(il generatore, la scheda, il collaudo `esatto`)*; screening `~3`
  minuti.
- `(g)` ### **sulla FCC** `f(k) = 1/2 + (1/24) sum cos`: ### **ma la FCC non ha `(pi, pi)` alternato**, quindi il
  vantaggio sul picco ### **non c'e'**.

### `S-C` — **UN TERMINE CHE RENDE COSTOSE LE ONDE CORTE** *(`C2`)*, ### **col suo numero**

- `(a)` ### **un termine d'arco tipo Wilson** *(`r sum_a |psi_i - U_a psi_j|^2`)* ### **o un gradiente nella legge**,
  ### **che alza l'energia dei `k` grandi.**
- ### ⛔ **IL NUMERO `r`: NON LO SO DERIVARE.** ### **I candidati SENZA manopola sono due, nessuno derivato:**
  ### **`OMEGA_H = pi`** *(il coefficiente dei generatori di Grover e di salto: `r = OMEGA_H` vuol dire «lo stesso
  peso del salto»)* ### **e `r = 1` in unita' di reticolo** *(il valore di Wilson: una convenzione, non una
  derivazione)*. ### **Scritto qui come buco, non nascosto.**
- `(b)` ### **entrambe le famiglie** *(la banda a `~pi/2` e il picco)*.
- `(c)` 1 ### **`A14` raggio `1`** · 2 ### **(b)** · 3 ### ⛔ **AGGIUNGE UNA LEGGE E UN NUMERO** *(`9-ter`: deve
  dire perche' non si toglie niente)* · 4 ### **tocca la camminata, non `rho`** · 5 ### **la banda dovrebbe sparire
  se il costo supera il guadagno.**
- `(d)` ### **una legge nuova di `H`**: ### **va dimostrato che conserva** *(e' un termine hermitiano: si')*.
- `(e)` ### **PREVISIONE dalla lettura `3.2`:** ### **e' la strada con LEVA**, perche' ### **cambia i rami**
  *(`F5`: i rami muovono il guadagno di `/4`)*; ### **ma `F5` dice anche che cambiare i rami SPOSTA la banda invece
  di toglierla** *(la finestra vuota)*: ### **prevedo un guadagno piu' basso e spostato, NON zero.**
- `(f)` ### **una legge nuova + la derivazione del numero**; screening `~3` minuti per valore.
- `(g)` ### **vale sulla FCC** *(per arco)*.

### `S-D` — **`S3` PER ESTREMITA'** *(STRADA MIA, dichiarata, e la scrivo per scartarla)*

- `(a)` ### **la fase di `psi_h` da `|psi_h|^2` della sola estremita'** invece che da `rho` del nodo.
- `(e)` ### **PREVISIONE dalla lettura `3.2`:** ### **e' ancora un'autofase locale**: ### **la banda RESTA**, e ###
  **forse cresce** *(a scala piu' fine)*. ### **Non la propongo: la scrivo perche' i fatti la escludono.**
- `(g)` ### **FCC: identico.**

### `S-E` — **PRIMA LA PROVA, POI LA STRADA** *(MIA, dichiarata: non e' una cura)*

- ### **la prova `1` della sez. `3.2`** *(la risoluzione per rami del modo che cresce)*, ### **con lo strumento che
  c'e'** *(gli autovettori di `M(k)` e quelli della camminata sola, gia' calcolati in `594417f6` e in
  `_stabilita_lineare.py --risonanza`)*: ### **nessuna fisica nuova, un'ora di codice e minuti di corsa.** ### **Decide
  la lettura**, e con lei ### **quale strada ha leva** *(`S-A` se la banda e' l'autofase su un ramo focalizzante;
  `S-C` se e' la forma dei rami)*.

---

## 5. LA SINTESI

- ### **La banda non e' della geometria** *(`F3`)*, ### **non e' della scala** *(`F7`)*, ### **non e' di `nu`**
  *(`F9`)*: ### **e' dell'AUTOFASE LOCALE di `S3` sui rami della camminata** *(lettura `3.2`, MIA, non misurata)*.
- ### **Prevedo** *(dalla lettura)*: ### **i filtri** *(`S-B`)* ### **abbassano poco**; ### **i costi sui rami**
  *(`S-C`)* ### **spostano**; ### **solo togliere l'autofase** *(`S-A`)* ### **la toglie** -- ### **e `S-A` sta nel
  territorio di `LINEARE`, FERMO.**
- ### **La forma di `S3` e' una SCELTA**, non una derivazione *(la sua scheda)*; ### **il nodo per derivarla e'
  `DEC-D6F-FORME-VUOTO`, non preso.**

## 6. LE DOMANDE PER LUCA *(una alla volta, nella relazione)*

1. ### **Si fa prima `S-E`** *(la prova per rami, che decide la lettura `3.2` senza fisica nuova)*, ### **o si va
   direttamente a uno screening** *(`S-B` e' il solo senza numeri nuovi e fuori da `LINEARE`)*?
2. *(dopo)* ### **Se la lettura regge: si riapre `LINEARE`** *(la strada `S-A`)* ### **o il nodo
   `DEC-D6F-FORME-VUOTO`?**
3. *(dopo)* ### **Il numero di `S-C`:** ### **`OMEGA_H`, `1`, o da derivare.**
