# DA DOVE VIENE LA MASSA DELLA CAMMINATA? IL SALTO E LA CURVATURA IN FUNZIONE DELLO SPOSTAMENTO PARZIALE `s`

> **Il mandato:** decisione di Luca del `2026-10-22` alle `20:03`, dopo `e133316a`; ### **eseguito DOPO le registrazioni in coda**
> *(il canale di `cs` `d06e402c`, `L1` `80d89521`/`28b4c92d`, il triangolo `82dc6310`, i lampi gamma `63e6499f`)*. ### **MISURE E UN CONTO:
> `leggi.yaml` e l'impronta INTATTI; nessuna cura, nessuna regola cambiata.**

**LIVELLO:** `L2`, misure e un conto.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*.
2. **Il gradino:** `(a)` ### **a `eps 0.5`, `dtau 0.125` lo strumento ridà `c` di `82b40ca1`**; `(b)` ### **`eps = 0` toglie la moneta**; `(c)` ### **la
   camminata di Grover a `s = 1`** *(il limite noto: la camminata di Grover discreta)*.
3. **Aggiunge un numero o una legge?** ### **No: `dtau` varia SOLO nella scena, a griglia fissa.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No:** `cs` spento.
5. **Emergente o imposto?** ### **E' la domanda:** ### **la massa dei rami e' della discretizzazione** *(`s`)* ### **o del generatore** *(Grover)*.

## 1. ⛔ L'ERRORE `n.35` DEL GUARDIANO *(dal mandato)*

### **«La moneta e' la massa», SMENTITA da `e133316a`:** ### **il salto c'e' a `eps 0`** *(`Delta` `1.69`)*; ### **`c` cambia meno del `17%` su `eps`
`0`-`2`.**

## 2. LE IPOTESI E LA PREVISIONE, A MANO, PRIMA DEI NUMERI

- ### **L'IPOTESI DEL GUARDIANO** *(non verificata)*: ### **la massa viene dallo SPOSTAMENTO PARZIALE**: lo spostamento scambia le estremita' di un
  arco di una frazione `s = dtau cs / dtau_rif` per tick *(`e^{i pi s}`)*; ### **con `s` piccolo la camminata e' «pigra»**, e una camminata pigra a onde
  lunghe ha dispersione parabolica come una particella con massa. ### **L'ALTERNATIVA: Grover.**
- ### ⭐ **IL CONTO A MANO** *(MIO, dichiarato)*: ### **non solo lo spostamento e' parziale: ANCHE IL GROVER lo e', con lo STESSO `s`** *(`flussi_parziali.z_nodo`
  e `z_arco`: `theta = pi s frazione`, per il nodo E per l'arco)*. ### **Quindi per `s` piccolo il tick e' il prodotto di Trotter di un GENERATORE FISSO**
  *(`pi P_perp` del Grover, lo scambio d'arco, la moneta `eps`)*: ### **`U ~ exp(-i dtau H)`**, ### **e `omega` PER UNITA' DI TEMPO tende a un LIMITE FINITO**,
  ### **con correzioni `O(s^2)`** *(il palindromo e' di secondo ordine)*. ### **Allora `Delta` e `c` NON dipendono da `dtau` per `s` piccolo** -- ### **coerente
  con l'invarianza di Courant gia' misurata** *(`594417f6`, `F6` di `CURE_CANDIDATE_S3`)*. ### **La massa e' una proprieta' del GENERATORE continuo**, non
  della pigrizia: ### **in questo senso le due ipotesi non si escludono** *(lo «spostamento parziale» e' cio' che rende il tick un generatore continuo)*.
- ### **A `s = 1`** *(`dtau = 1`, `cs` spento)* ### **gli angoli sono `pi`: il Grover e' la riflessione `2P - I`, lo spostamento e' lo scambio intero** --
  ### **la camminata di Grover DISCRETA**, ### **che sul quadrato ha a `k` piccolo un CONO** *(`cos omega ~ (cos k_x + cos k_y)/2`, quindi `omega ~ |k|/sqrt2`:
  LINEARE, senza massa)* *(conto noto, riportato; con la moneta `eps` e i due settori, da verificare)*.
- ### **LA PREVISIONE:** ### **(i) a `eps 0`, `Delta` e `c` per unita' di tempo COSTANTI fra `dtau` `0.03125` e `0.125`, entro il `5%`** *(il limite continuo)*;
  ### **(ii) cambiano andando verso `s = 1`**; ### **(iii) a `s = 1` la dispersione a `k` piccolo e' LINEARE** *(`v_g(2)/v_g(1)` vicino a `1`)*.

## 3. IL CONTO DI DIMENSIONI *(su carta, da fare nel referto coi numeri della misura)*

### **Con la regola di oggi** *(valori per nodo invarianti, `dtau` proporzionale al passo, `dtau_rif = 1` come nel codice)*, ### **raffinando `a -> a/2`**:
`dtau -> dtau/2`, ### **`s -> s/2`**. ### **Se `Delta`, `c`, `gamma` sono nel limite continuo** *(punto (i))*, ### **le velocita' della camminata in ARCHI PER
UNITA' DI TEMPO restano fisse**, quindi ### **in unita' FISICHE** *(archi `x a` per unita' di tempo)* ### **si DIMEZZANO.** ### **Il cono** *(un arco per tick,
`a/dtau`)* ### **resta fisso; la velocita' a cui la camminata si muove davvero no.** ### **Se e' cosi', la regola di oggi e' dimensionalmente INCOERENTE con
`(B)`, e lo si scrive.** ### **Credo che sia cosi'.** ### **Una regola coerente terrebbe fisso `s`** *(`dtau_rif` proporzionale ad `a`)*: ### **una domanda per
Luca, non una scelta mia.**

## 4. LA MISURA, I CONTROLLI E LE LETTURE *(copiati dal mandato)*

- ### **LA MISURA:** la camminata sola, esatta; ### **lato `32` e `64`; `eps 0.5` e `0`; `dtau` `0.03125`, `0.0625`, `0.125`, `0.25`, `0.5`, `1` a lato FISSO**
  *(`s = dtau`, `cs` spento)*. ### **Sui rami dispersivi:** `Delta`, `c` *(la definizione di `82b40ca1`)*, la parabolicita', `v`. ### **A `s = 1`: lineare o
  parabolica.**
- ### **DEVE RIUSCIRE:** ### **a `eps 0.5`, `dtau 0.125`, lato `32` e `64`: `c` di `82b40ca1` entro `1e-4`.**
- ### **LE LETTURE:**
  - ### **S E' LA MASSA** se `Delta` e `c` dipendono da `s` ### **secondo la previsione** *(i)-(iii)*, ### **entro il `5%`**, e ### **a `eps 0` il salto c'e' per `s < 1`**;
  - ### **GROVER** se `Delta` e `c` ### **NON dipendono da `s`** *(entro il `5%`, a `eps 0`, su TUTTI gli `s`)*;
  - ### **altrimenti NON DECIDIBILE**, coi numeri;
  - ### **a `s = 1`: LINEARE o PARABOLICA a `k` piccolo** *(`v_g(2)/v_g(1)` entro `5%` di `1` o di `2`)*.
- ### ⚠ **CHE COSA SO GIA' DI QUESTE LETTURE, prima:** ### **la mia previsione** *(i)* ### **dice «costante a `s` piccolo»** -- ### **cioe' la parte della lettura
  GROVER** -- ### **e** *(iii)* ### **«lineare a `s = 1»**: ### **se i numeri la seguono, l'etichetta e' «S E' LA MASSA» per costruzione delle letture**, ### **ma il
  significato fisico e' quello del conto a mano:** ### **la massa e' del generatore, e `s = 1` e' il punto discreto dove sparisce.** ### **Lo scrivo prima per non
  leggere l'etichetta come piu' di quello che e'.**

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_massa_spostamento.py`: commit, corsa, referto `doc/referti_l2/massa_spostamento.txt` e `.jsonl`; ### **il conto di dimensioni coi numeri**; la relazione
   con ### **UNA domanda** *(la regola di scala)*. ### **NESSUNA REGOLA CAMBIATA.**
