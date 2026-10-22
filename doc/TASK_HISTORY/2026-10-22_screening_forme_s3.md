# LO SCREENING DELLE FORME CANDIDATE DI `S3` *(nessuna forma nuova, nessuna scelta)*

> **Il mandato:** decisione di Luca del `2026-10-22` alle `10:15`, dopo `52e31a41`. ### **Uno SCREENING DIAGNOSTICO:**
> `leggi.yaml` e l'impronta `2e7f795d2a52fbe7` INTATTI; ### **le forme entrano SOLO IN MEMORIA nello strumento** *(come
> Fourier in `52e31a41`)*. ### **In parallelo a `R1T`:** il controllo della macchina delle `10:15` *(`90bc8573`)* dice ### **`R1T`
> usa `~1` core su `12`**: ### **un processo in piu'.**

**LIVELLO:** `L2`, uno screening diagnostico.

## 0. LA STELLA POLARE

1. **`A14`:** ### **ogni forma e' per nodo** *(una fase su `psi` e una su `phi`)*: raggio `0`, ### **`esatto` regge per tutte**
   *(una fase non cambia `rho` ne' `Lambda`)*.
2. **Il gradino:** `(a)` ### **la forma di oggi ridà i referti al bit** *(il controllo che ripete la cosa giusta)*; `(b)` ###
   **ogni forma e' una sostituzione della stessa legge**; `(c)` non si applica.
3. **Aggiunge un numero o una legge?** ### **No: nessuna forma nuova**, solo le candidate gia' scritte; ### **`S4` porta il suo
   `p = 2/pi`**, ### **che e' nella sua definizione** *(non tarato qui)*.
4. **Tocca `rho`, `c_s` o il segno?** ### **Tocca come `rho` e `Lambda` entrano nella fase**; `cs` spento *(`R2`)*.
5. **Emergente o imposto?** ### **NESSUNA FORMA SI SCEGLIE QUI: lo screening dice solo come si comportano.**

## 1. ⛔ L'ERRORE `n.33` DEL GUARDIANO *(dal mandato)*

### **L'ipotesi delle bande piatte di Grover**, ### **SMENTITA da `52e31a41`:** Fourier toglie le bande piatte, ### **la banda di
`S3` resta all'`87`-`92%`.**

## 2. LE FORME, ALLA LETTERA

### ⚠ **DOVE SONO SCRITTE, e lo dico prima:** ### **la scheda di `CAMM-MATERIA-VUOTO` in `leggi.yaml` NON le scrive**: dice
### **«una SCELTA DI LUCA FRA QUATTRO CANDIDATE MISURATE»** *(riga `546`)* e ### **nomina `S2`** *(riga `542`: «`S2` lo VIOLA con
`1.89`»)*, ### **senza formule**; ### **il nodo `DEC-D6F-FORME-VUOTO`** *(`doc/ALBERO_era2.yaml`)* ### **riporta solo la scelta**
*(«`N_k = rho_k ln(rho_k/(rho_k + Lambda_k))` -- cioe' la forma `S3` dei pezzi `3` e `4` di `L2`»)*. ### **Le quattro formule
sono SCRITTE in `primo_ordine/_deriva_forme_l2.py`** *(la derivazione del `2026-10-15`, verificata da `sympy`, che la scheda
chiama «misurate»)*: ### **le prendo da li', ALLA LETTERA, e non ne aggiungo nessuna.** ### **Fuori: `CAMM-SATURAZIONE`**, che e' in
`leggi.yaml` ### **come legge SUPERATA, non come candidata**, e ### **la sua sorgente e' `h_int`, non `rho`** *(e' l'`S1` con `h`
al posto di `rho`)*.

### Tutte nella forma `N = Lambda F(x)`, `x = rho/Lambda` *(omogenee di grado `1`: `_deriva_forme_l2.py`, intestazione)*

`alpha = dN/drho = F'(x)`; `beta = dN/dLambda = F - x F'`; ### **l'ACCOPPIAMENTO EFFICACE `rho d alpha/d rho = x F''(x)`.**

| | `F(x)`, alla lettera | `alpha = F'` | `beta = F - x F'` | ### **`x F''(x)`** *(a mano)* | ### **per `rho -> 0`** |
|---|---|---|---|---|---|
| `S1` | `x - arctan x` *(«la saturazione di oggi, con `rho` al posto di `h`»)* | `x^2/(1+x^2)` | `x - arctan x - x^3/(1+x^2)` *(`~ -(2/3) x^3`)* | ### **`2 x^2/(1+x^2)^2`** | ### **`-> 0`** *(come `x^2`)* |
| `S2` | `x ln x` | `1 + ln x` | `-x` | ### **`1`** | ### **`1` a ogni `x`** *(costante)* |
| `S3` *(oggi)* | `x ln(x/(1+x))` | `ln(x/(1+x)) + 1/(1+x)` | `-x/(1+x)` | ### **`1/(1+x)^2`** | ### **`-> 1`** |
| `S4` | `F = pi x - 2 pi x 2F1(1, 1/p; 1+1/p; -x^p)`, `p = 2/pi` *(forma chiusa; `alpha4`, `F4`, `beta4`)* | `pi (x^p - 1)/(x^p + 1)` | `F4 - x alpha4` | ### **`4 x^p/(1+x^p)^2`** *(`2 pi p = 4`)* | ### **`-> 0`** *(come `x^0.64`)* |

### ⚠ **LE DERIVAZIONI:** ### **nessuna delle quattro e' DERIVATA da un principio** -- ### **sono le quattro forme omogenee che il
`2026-10-15` ha MISURATO** *(la scheda: «una scelta fra quattro candidate misurate, non una derivazione»)*; ### **il conto di
`sympy` in `_deriva_forme_l2.py` verifica `alpha`, `beta` e l'identita' `beta' = -x alpha'`, non le DERIVA.**

### I VALORI DELL'ACCOPPIAMENTO *(a mano, ai quattro `x` del controllo)*

| `x` | `S1` | `S2` | `S3` | `S4` |
|---|---|---|---|---|
| `1e-4` | `2.0e-8` | `1` | `0.9998` | `~0.011` |
| `1e-2` | `2.0e-4` | `1` | `0.980` | `~0.21` |
| `0.1` | `0.0196` | `1` | `0.826` | `~0.61` |
| `1` | `0.5` | `1` | `0.25` | `1` |

## 3. LE PREVISIONI, scritte prima *(dal limite dell'accoppiamento)*

- ### **`S2`: come `S3`, INSTABILE a ogni `x`**, anche a poca materia *(l'accoppiamento e' `1` ovunque)*; ### **la banda `~0.4`.**
- ### **`S1`: accoppiamento `0.02` a `x 0.1`, `2e-8` a `1e-4`**: ### **STABILE A POCA MATERIA** *(credo `gamma(1e-4)` sotto `1e-3`)*;
  ### **a `x 0.1` non so** -- ### **`F9` di `S3_RIPENSATA` dice che il guadagno e' poco sensibile all'accoppiamento sopra `0.25`**, ma
  ### **a `0.02` deve calare** *(a `0` la camminata e' stabile)*: ### **credo `gamma` fra `0.02` e `0.2`.**
- ### **`S4`: accoppiamento `0.61` a `x 0.1`** *(credo `gamma ~0.38`, come `S3`)*, ### **`0.011` a `1e-4`**: ### **STABILE A POCA
  MATERIA, o quasi** *(credo `gamma(1e-4)` sotto `0.1 gamma(0.1)`)*.
- ### **IL LEGAME:** ### **credo che TENGA**: ### **le forme con accoppiamento `-> 0`** *(`S1`, `S4`)* ### **sono quelle stabili a poca
  materia**, ### **`S2` e `S3` no.**

## 4. I CONTROLLI E LE LETTURE *(copiati dal mandato)*

- ### **LA SOSTITUZIONE:** ### **`materia_vuoto.pezzi`** *(la funzione che `materia_vuoto.applica` chiama per `(alpha, beta)`)*
  ### **si rimpiazza SOLO IN MEMORIA** con quella della forma; ### **`S3` e' la funzione del codice**, ### **`S4` usa `alpha4` e `beta4`
  di `_deriva_forme_l2.py`**, `S1` e `S2` le formule della tabella; ### **dove `rho = 0`, `alpha = 0`** *(come oggi: la fase di un
  vettore nullo)*.
- ### **DEVE RIUSCIRE:** con la forma di oggi lo strumento ### **ridà AL BIT `594417f6` `R2` *(quadrato)*, `bb0ef057` *(triangoli,
  `SE`)*, e la riga `x 1e-4` di `07083f09`** *(materia diluita, la mappa intera di `gamma`)*.
- ### **per ogni forma:** l'accoppiamento ### **dal CODICE** *(differenze finite della `alpha` sostituita)* ### **contro quello a
  mano, entro `1e-8` relativo, a `x` `1e-4`, `1e-2`, `0.1`, `1`.**
- ### **la camminata sola esatta** *(non dipende dalla forma: una volta per geometria)*; ### **la base `<= 1e3` ulp** in ogni corsa;
  ### **la linearita'** `1e-7` contro `1e-6` ### **su un braccio per forma** *(il quadrato a `x 0.1`)*.
- ### **I BRACCI:** ogni forma, `R2`, lato `32`, `dtau 0.125`, base proiettata, `N dtau 100`, la norma, la seconda meta', ### **su
  `Q` e `T` *(`SE`)*, a `x 0.1` e `1e-4`.**
- ### **LE LETTURE, per ogni forma:** ### **il massimo di `gamma`, dove, e il rapporto con `S3`** *(`0.402` `Q`, `0.377` `T`)*; ###
  **STABILE** se `<= 1e-3` del massimo di `S3`; ### **STABILE A POCA MATERIA** se `gamma(1e-4) <= 0.1 gamma(0.1)` *(per geometria)*;
  ### **IL LEGAME** tiene se le forme con accoppiamento `-> 0` sono quelle stabili a poca materia.

### ⛔ **COSA MI FA FERMARE:** ### **`S3` che non ridà i referti al bit**; ### **un bisogno di toccare il passo vero.**

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_screening_forme_s3.py`: commit, la corsa in parallelo a `R1T`, il referto `doc/referti_l2/screening_forme_s3.txt` e
   `.jsonl`, la tabella, la relazione con ### **UNA domanda: la decisione su `LINEARE`.** ### **NESSUNA FORMA SCELTA.**
