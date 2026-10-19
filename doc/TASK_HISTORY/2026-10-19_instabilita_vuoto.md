# IL TEST DI INSTABILITA' DEL VUOTO UNIFORME

> **Il mandato:** decisione di Luca del `2026-10-19` alle `20:02`, ### **prima** della
> sistemazione di `LINEARE` e della scelta di `Lambda_c`, che ### **restano FERME** fino
> all'esito. ### **Nessun codice di fisica: una misura.**
> **Il fatto, dai bracci salvati di `D4`** *(`963535bc`)*, riletti dal guardiano blocco per
> blocco: ### **la variazione del vuoto nel grumo NON cresce con la sorgente** -- a `x = 0.01`
> il grumo si svuota quasi del tutto, a rapporto `1` lo svuotamento ### **CALA** al crescere
> di `x`, a rapporto `10` e' non monotono, e a rapporto `10`, `x = 0.01` ### **CRESCE lungo i
> blocchi.** ### **La lettura del guardiano, un'ipotesi:** un'### **INSTABILITA'** del vuoto
> uniforme con `cs` dinamico *(un equilibrio esatto ma forse instabile)*, non una risposta
> alla materia. Senza `cs` e senza `CAMM-FASE-VUOTO` *(mappa sez.`16`)* la risposta era
> lineare.

**LIVELLO CORRENTE:** `L2`.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica come domanda su una legge**: nessuna legge cambia. ### ⚠ **E
   la perturbazione conserva `V` totale per costruzione** *(somma zero pesata)*, quindi il
   test non cambia il vuoto medio.
2. **Il gradino:** `(a)` le barre fra blocchi, un seme dichiarato, due ampiezze e due `dtau`;
   `(b)` ### **il braccio `(3)` a `cs` SPENTO e' il caso che DEVE fallire** per «instabile»
   -- se l'instabilita' c'e', ### **sparisce togliendo cio' che la produrrebbe**; `(c)` ### **non
   raggiunto**.
3. **Aggiunge un numero o una legge?** ### **No.** L'ampiezza `1e-6` e il seme sono ###
   **parametri della MISURA**, dichiarati, e `1e-9` c'e' apposta per dire se il risultato ne
   dipende.
4. **Tocca `rho`, `c_s` o il segno?** ### **Misura come `cs` dinamico reagisce a una
   perturbazione del vuoto**; nessun verso dell'accoppiamento cambia. ### **Senza materia**
   *(`psi = 0`)*: e' il vuoto con se stesso.
5. **Emergente o imposto?** ### **E' la domanda stessa:** se il vuoto uniforme si rompe da
   solo, cio' che `D4` vedeva ### **non era una risposta alla materia.**

## 1. LA SCENA E I BRACCI, fissati qui

- **La scena:** quella di `D4` *(`statica_protocollo`: toro `31x31`, `VUOTO = 1`, `SEME = 7`,
  `Lambda_medio = 4`)*, ### **SENZA sorgente** *(`psi = 0`)*.
- ### **LA PERTURBAZIONE, e come conserva `V`:** per ogni estremita' `h`, con `w_h = |phi_h|^2`
  e `r_h` normale standard *(### **seme `20261019`**, dichiarato)*, si toglie a `r` la sua media
  pesata, `r <- r - (somma w r)/(somma w)`, e ### **`phi_h <- phi_h * sqrt(1 + a r_h)`**: la
  fase non cambia, e `somma_h w_h (1 + a r_h) = V` ### **esattamente in aritmetica esatta.**
  ### **`a = 1e-6`** *(il braccio `(5)`: `1e-9`)*. ### **`Lambda_medio` resta `V/N`.**
- **I bracci**, `dtau = 0.5` e ### **`2000` tick** salvo dove detto:

| | il braccio | che cosa dice |
|---|---|---|
| `(1)` | `cs` acceso, il passo di oggi, ### **ai tre rapporti** `0.1`, `1`, `10` | c'e' l'instabilita'? |
| `(2)` | `cs` acceso ### **SENZA `CAMM-FASE-VUOTO`**, rapporto `1` | e' quel termine a farla? |
| `(3)` | ### **`cs` SPENTO**, rapporto `1` *(il passo di default)* | ### **il controllo: NON deve crescere** |
| `(4)` | come `(1)` a rapporto `1`, ### **`dtau = 0.25`, `4000` tick** *(lo stesso tempo)* | ### **fisica o numerica?** |
| `(5)` | come `(1)` a rapporto `1`, ### **ampiezza `1e-9`** | ### **il regime e' lineare?** |

## 2. LA MISURA, E COME SI SCEGLIE IL TRATTO *(dichiarato prima)*

- ### **`m(t) = max_k |Lambda_k(t) - Lambda_medio|`**, a ogni tick.
- ### **IL TRATTO:** da ### **`T0 = 20` tick** *(il transitorio della perturbazione casuale)*
  al primo tick in cui ### **`m(t) >= 1e-2 * Lambda_medio`** *(la perturbazione non e' piu'
  piccola)*, o alla fine della corsa. ### **Se il tratto e' piu' corto di `50` tick, `gamma`
  e' «non misurabile».**
- ### **`gamma`:** il tratto si divide in ### **`5` blocchi uguali**; in ognuno la pendenza di
  `ln m(t)` coi minimi quadrati; ### **`gamma` e' la media dei `5`, la barra la loro deviazione
  standard diviso `sqrt(5)`** *(`P3`: almeno `4` per una barra)*.
- ### **In tick e in TEMPO PROPRIO:** il tempo proprio per tick dello stato uniforme e'
  `dtau * cs_m`, con `cs_m = Lambda_m/(Lambda_m + Lambda_c)` *(`1` a `cs` spento)*:
  `gamma_tau = gamma_tick / (dtau * cs_m)`.

## 3. I CRITERI, fissati qui

- ### **«instabile» se `gamma > 0` con `>= 3` barre.**
- ### **il braccio `(3)` deve dare `gamma < 3` barre** *(cioe' NON instabile)*: e' il caso
  che DEVE fallire per «instabile».
- ### **`(4)`:** FISICA se `|gamma_tau(0.5) - gamma_tau(0.25)| <= 3 sqrt(b1^2 + b2^2)`;
  ### **altrimenti NUMERICA** *(e si riporta come scala con `dtau`)*.
- ### **`(5)`:** LINEARE se `|gamma(1e-9) - gamma(1e-6)| <= 3 sqrt(b1^2 + b2^2)` *(in tick, a
  pari `dtau`)*.
- ### **Se il punto fisso di `cs` non converge:** si registra *(tick, `Lambda` minimo,
  `Lambda_c`)* e si va avanti. ### **Niente cure.**

**ANNOTAZIONE, PRIMA DEL CODICE: LA SECONDA VERSIONE DEL MANDATO** *(arrivata dopo `027a3f70`; `PRECEDENZA-IN-CODA`: vale l'ultima)*. *(Si annota, non si riscrive.)* Due cose cambiano:
- ### **SI RIPORTA ANCHE LA LUNGHEZZA D'ONDA DEL MODO CHE CRESCE.** **Come, dichiarato qui:** al tick in cui finisce il tratto *(`T1`)*, il campo `delta Lambda_k = Lambda_k - Lambda_medio` si dispone sul toro `31x31` *(l'indice del nodo e' `statica_protocollo.nodo_di`, riga per riga)*, se ne prende ### **la trasformata di Fourier 2D**, e il modo dominante e' ### **il massimo di `|FFT|^2` escluso `k = 0`**, con `kx, ky` riportati in `[-15, 15]`. ### **`lambda = 1/sqrt((kx/31)^2 + (ky/31)^2)` in ARCHI.** Si riporta anche ### **la frazione di `|FFT|^2` che quel modo porta** *(se e' piccola, «il modo dominante» non dice molto, e lo si dice)*.
- ### **LA DOMANDA DI LUCA VA NELLA MAPPA COME VINCOLO DI `L2` SU `L3`**, non come lavoro di `L3`: se `gamma` e' FISICA, ### **il vincolo e' UN NUMERO** *(il tasso di crescita della rete almeno dell'ordine di `gamma`, in tempo proprio, alla scala della lunghezza d'onda misurata)*; se e' NUMERICA, l'espansione non c'entra; ### **e il vincolo NON chiude `L2` da solo.**

## 4. TODO

1. `csv/_instabilita_vuoto.py`, un processo per braccio, le serie salvate mentre corrono;
   commit prima della corsa.
2. la corsa dal blob pulito, il referto, la relazione.
3. la DOMANDA di Luca nella mappa, sotto `L2` con rimando a `L3`, con le considerazioni del
   guardiano scritte come tali.
4. ### **`LINEARE` e `Lambda_c` restano FERMI.**
