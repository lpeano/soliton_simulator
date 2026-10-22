# LA PROVA DI GROVER: LA STESSA `S3` CON UNA MONETA DI MESCOLAMENTO SENZA BANDE PIATTE (FOURIER)

> **Il mandato:** decisione di Luca del `2026-10-22` alle `09:10`, dopo `6b2f332b`. ### **Una PROVA DIAGNOSTICA, non una
> cura scelta.** ### **`leggi.yaml` e l'impronta `2e7f795d2a52fbe7` INTATTI.** ### **La corsa di `R1T` non si tocca:**
> la macchina ha ### **`12` processori logici** e `R1T` e' ### **un processo solo** *(`python csv/_stato_finale.py --braccio
> R1T`)*: ### **questa prova gira IN PARALLELO, un processo, un core** *(dichiarato)*.

**LIVELLO:** `L2`, una prova diagnostica.

## 0. LA STELLA POLARE

1. **`A14`:** ### **la moneta di Fourier e' per nodo** *(raggio `0`)* e ### **unitaria**: conserva la norma come Grover.
2. **Il gradino:** `(a)` ### **il caso che deve fallire** e' il test delle bande piatte su Grover; `(b)` ### **togliere
   Grover e metterlo di nuovo** *(con Grover lo strumento ridà `594417f6` e `bb0ef057` al bit)*; `(c)` non si applica.
3. **Aggiunge un numero o una legge?** ### **Nessun numero:** la matrice di Fourier e' ### **fissata da `d`** *(`w =
   e^{2 pi i/d}`)* e ### **dall'ordine ciclico delle direzioni** *(un dato del grafo regolare)*; ### **il suo flusso usa
   lo stesso angolo di Grover** *(`theta = pi s frazione`)*. ### **Una legge di PROVA, in memoria:** non entra nel passo.
4. **Tocca `rho`, `c_s` o il segno?** ### **No:** cambia la moneta di mescolamento; `cs` spento *(`R2`)*.
5. **Emergente o imposto?** ### **E' una DIAGNOSI, non una cura scelta:** ### **sostituire Grover nel passo vero e' una
   decisione di Luca, e va DERIVATA.**

## 1. RAGIONAMENTO PRELIMINARE

- ### **IL CONTESTO** *(dal mandato, e dai commit)*: ### **le bande piatte della camminata di oggi** *(il guardiano: due
  fasi uguali a ogni `k`, `-pi/4` e `-pi/8` per tick a lato `32`, e rami quasi piatti)*; ### **`S-E`** *(`642dee6f`)*: il modo
  che cresce ### **per il `45%` sul ramo lento**; ### **la materia diluita instabile per il logaritmo** *(`07083f09`)*; ###
  **lo stato finale fisso in archi** su quadrato e triangoli *(`07ca006e`, `3c540740`, `6b2f332b`)*.
- ### **LA SCELTA, dichiarata:** ### **la SOSTITUZIONE SOLO IN MEMORIA nello strumento** *(non una legge `prova: true` in
  `leggi.yaml`)*: ### **l'operatore `grover` del motore** *(e `grover_scalare` per `F2`)* ### **si rimpiazza nella scena
  costruita dallo strumento**; ### **nessun file del passo si tocca, l'impronta resta.** ### **Il perche':** una legge in
  tabella cambierebbe `leggi.yaml` *(il mandato lo vuole intatto)* e la catena di generazione, per una prova.
- ### **IL FLUSSO DI FOURIER, senza numeri:** Grover e' `G(theta) = P_u + e^{i theta}(I - P_u)`, ### **il flusso di
  `pi P_perp`**, e a `theta = pi` e' la moneta. ### **Fourier:** `F = sum_j e^{i phi_j} P_j` *(ramo principale, `-1 ->
  +pi` come in Grover)*, ### **`F(theta) = sum_j e^{i phi_j theta/pi} P_j`**: ### **a `theta = pi` e' `F`**, ### **lo stesso
  angolo** `theta = pi s frazione` *(`s` uniforme in `R2`: lo si ASSERISCE)*.
- ### **L'ORDINE CICLICO** *(dichiarato)*: ### **le `d` estremita' del nodo ordinate per angolo della loro direzione**
  *(`atan2` dei versori di `_triangoli.versori`)*: ### **quadrato `0, 90, 180, 270` gradi; triangoli ogni `60`.**
- ### ⚠ **UNA CONSEGUENZA DA DIRE PRIMA:** ### **la camminata sola NON mescola `psi` e `phi`** *(due settori)*; ### **in `F1`
  il vuoto resta con Grover, quindi LE BANDE PIATTE DEL SETTORE `phi` RESTANO PER COSTRUZIONE.** ### **Il controllo
  «nessuna banda piatta» si fa PER SETTORE:** ### **la materia in `F1`, materia e vuoto in `F2`.**
- ### ⭐ **LA PREVISIONE, scritta prima dei numeri:** ### **dalla lettura «a rami»** *(`S3_RIPENSATA` `3.2`)*, ### **il
  guadagno lo limita la camminata**: ### **togliere le bande piatte toglie il ramo lento su cui il modo pesa per il `45%`**,
  ### **ma la fase locale di `S3` trova altri rami.** ### **Credo PARZIALE:** il massimo ### **fra `0.15` e `0.35`** con
  Fourier *(non sotto `0.04`, non sopra `0.2` del quadrato per il caso innocente)*, ### **e la materia diluita resta
  INSTABILE** *(il logaritmo e' un colpevole indipendente)*. ### **Non so** se Fourier rompe l'isotropia `C6`.

## 2. LA PROGETTAZIONE, I CONTROLLI E LE LETTURE *(copiati dal mandato)*

- ### **I BRACCI:** `F1` *(Fourier solo per la materia)*, `F2` *(materia e vuoto)*; ### **quadrato `Q` e triangoli `SE`**;
  ### **`F2` a `x 1e-4` sul QUADRATO** *(dove la materia diluita fu misurata, `07083f09`)*.
- ### **I CONTROLLI SULLA CAMMINATA SOLA, PRIMA DI `S3`** *(`A(k)` di `_triangoli.matrice_tick`, nei due settori)*:
  - ### **DEVE RIUSCIRE:** unitaria ed esatta con Fourier: `|lambda(A(k)^N)| = 1` ### **entro `N * 64` ulp** *(`N dtau 100`)*;
  - ### **DEVE RIUSCIRE: NESSUNA BANDA PIATTA con Fourier** *(nei settori che Fourier tocca)*: ### **nessuna fase**
    *(`angle(lambda)`, per tick)* ### **uguale a ogni `k` entro `1e-8`**; e ### **l'ampiezza di variazione di ogni ramo**
    *(i rami ordinati per fase a ogni `k`)* ### **stampata: la minima `> 1e-3`**;
  - ### **DEVE FALLIRE: lo stesso test con Grover trova le bande piatte** *(le due fasi `-pi/4` e `-pi/8` a lato `32`,
    `dtau 0.125`, in uno dei due segni)*. ### **Se non le trova, il test e' cieco: STOP.**
  - ### **L'ISOTROPIA della dispersione con Fourier** *(`C4` sul quadrato `(m_x, m_y) -> (-m_y, m_x)`, `C6` sui triangoli
    `_triangoli.ruota60`)*: ### **lo scarto massimo delle fasi stampato** *(e quello di Grover accanto)*; ### **se Fourier la
    rompe, lo si dice: e' un costo della prova.**
- ### **LA STABILITA' LINEARE** `R2` *(`S3` sola, lato `32`, `dtau 0.125`, `x 0.1`, base proiettata, `N dtau 100`, la norma,
  la seconda meta')*: `F1` e `F2` su `Q` e `T`, `F2` a `x 1e-4` su `Q`. ### **DEVE RIUSCIRE:** con Grover lo strumento
  ### **ridà AL BIT `594417f6` `R2` e `bb0ef057`** *(`SE`)*.
- ### **LE LETTURE, sul massimo di `gamma` su tutti i `k`:**
  - ### **GROVER COLPEVOLE** se il massimo con Fourier e' ### **`<= 0.1`** di quello con Grover *(`0.402` quadrato, `0.377`
    triangoli)* ### **su ENTRAMBE le geometrie**;
  - ### **GROVER INNOCENTE** se ### **`>= 0.5`** *(su entrambe)*;
  - ### **altrimenti PARZIALE**, coi numeri, e dove sta il massimo;
  - ### **STABILE** se `<= 1e-3` del massimo con Grover;
  - ### **`F2` a `x 1e-4`:** ### **se resta instabile** *(oltre `1e-3` del Grover a `x 0.1`)*, ### **il logaritmo resta un
    colpevole indipendente.**

### ⛔ **COSA MI FA FERMARE:** il test delle bande piatte cieco su Grover; ### **Grover che non ridà i referti al bit**; ### **un
bisogno di toccare il passo vero.**

## 3. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_prova_grover.py`: commit, la corsa IN PARALLELO a `R1T`, il referto `doc/referti_l2/prova_grover.txt` e `.jsonl`,
   la relazione. ### **NESSUNA CURA SCELTA.**
