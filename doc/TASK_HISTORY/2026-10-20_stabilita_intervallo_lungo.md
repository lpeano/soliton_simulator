# L'ANALISI DI STABILITA' LINEARE SU UN INTERVALLO LUNGO, A LATI PARI

> **Il mandato:** decisione di Luca del `2026-10-20` alle `15:57`, sulla domanda `1` della
> relazione di `c38367db` *(«il conto va rifatto su un intervallo piu' lungo?»)*. ### **Un conto,
> nessuna cura.** ### **Il passo NON cambia:** impronta `2e7f795d2a52fbe7`, `leggi.yaml`
> intatto. ### **Lo strumento `csv/_stabilita_lineare.py` (blob `0cb4ec58`) SI ESTENDE, non si
> riscrive:** il conto di `c38367db` resta riproducibile AL BIT coi parametri vecchi.
> ### **`LINEARE`, `Lambda_c`, le letture «alla Jeans» o di modulazione, lo stato finale restano
> FERMI; `D4` resta da rileggere.**

**LIVELLO CORRENTE:** `L2`.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica**, perche' ### **nessuna legge cambia**: e' una misura della
   crescita lineare di un passo che resta quello di `c38367db`.
2. **Il gradino:** `(a)` ### **la riproduzione al bit del conto vecchio**, la linearita' a due
   ampiezze, la camminata sola esatta; `(b)` ### **`R2` toglie `cs`**; `(c)` ### **non si
   applica**: nessun limite noto per la crescita di `S3`.
3. **Aggiunge un numero o una legge?** ### **Non si applica alla fisica:** l'intervallo, le
   soglie del `5%` e il budget sono ### **parametri del conto, dati dal mandato.**
4. **Tocca `rho`, `c_s` o il segno?** ### **Non si applica:** nessuna legge si tocca; ### **si
   misura** come `S3` e `cs` fanno crescere le perturbazioni.
5. **Emergente o imposto?** ### **Non si applica come domanda su una legge:** il conto dice ###
   **QUALE famiglia di modi domina** quando il transitorio e' finito.

## 1. RAGIONAMENTO PRELIMINARE

- ### **Le correzioni del guardiano alla relazione di `c38367db`** *(annotate nella relazione, non riscritte)*:
  - **(a)** ### **il picco a `(pi, pi)` c'e' gia' con `S3` SOLA**: il guardiano, `R2` a lato `32`, `dtau 0.125`, `N dtau 25`, `eps 1e-7`: gamma intero `0.3754` a `(10, 0)`; ### **seconda meta' `0.585` a `(16, 16)`**, ### **picco ISOLATO** *(diagonale, seconda meta': `m = 14` `-0.028`, `15` `0.107`, `16` `0.585`)*. ### **`cs` e la fase lo ALZANO, non lo creano**; a lato dispari `(pi, pi)` non e' un modo della griglia.
  - **(b)** ### **«le tendenze sono le stesse nelle due meta'» e' FALSO per `R2`**: a lato `62` il massimo e' a `(19, 0)` sull'intervallo intero e a `(pi, pi)` sulla seconda meta'.
- **Cosa credo:** che sull'intervallo lungo ### **il picco isolato a `(pi, pi)` vinca**, e che ### **`k = 0` sia un transitorio.** ### **Ma e' esattamente cio' che il conto deve dire.**
- **Cosa NON so:** se `N dtau = 100` basta; per questo ### **i quattro quarti**.

## 2. LA CONFIGURAZIONE *(dichiarata qui)*

- ### **lati PARI:** `32` a `dtau 0.125`, `64` a `dtau 0.0625` *(regola di scala di Luca)*;
- `x 0.1`, `RAPPORTO 1`, la scena di `c38367db`;
- ### **`N dtau = 100`** *(`N 800` a lato `32`, `N 1600` a lato `64`)*;
- ### **`R1`** *(`cs` acceso)* e ### **`R2`** *(`S3` sola, `cs` spento)* a entrambi i lati;
- ### **LA MONODROMIA RINORMALIZZATA:** a ogni tick, ### **per ogni `k`**, `M(k)` si divide per la sua norma di Frobenius e se ne accumula il logaritmo. ### **Nessun overflow, nessun cambio degli autovalori relativi.** *(Per `k` e non globale: i `k` crescono a ritmi diversi, e uno scalare unico farebbe sottoflusso ai lenti.)*
- ### **le istantanee del prodotto a `N/4`, `N/2`, `3N/4`, `N`:** `L_q(k) = ln |lambda_max|` cumulato; ### **gamma di ognuno dei QUATTRO quarti** `= (L_q - L_(q-1)) / (tempo proprio del quarto)` *(la stessa normalizzazione di `c38367db`)*;
- ### **la linearita'** *(`eps 1e-7` contro `1e-6`)* ### **SOLO a lato `32`, `R1` e `R2`**, sul gamma dell'intervallo intero, con la banda `1e-3` del massimo;
- ### **il budget: `3` h per braccio**; se lo supera, si ferma e lo dichiara *(`fine = BUDGET`)*.
- ### **Il comando:** `python csv/_stabilita_lineare.py --lungo`; ### **senza argomenti lo strumento fa il conto di `c38367db`**, invariato.

## 3. I CRITERI, FISSATI QUI *(copiati dal mandato prima di vedere i numeri)*

- ### **I TRE PUNTI:**
  - ### **`(pi, pi)`**: `k = (L/2, L/2)`;
  - ### **la BANDA**: il massimo del gamma dell'ULTIMO quarto ### **lungo gli assi** *(`(m, 0)` e `(0, m)`)* ### **e la diagonale** *(`(m, m)`)*, ### **esclusi `k = 0` e l'intorno di `(pi, pi)`** *(`|kx - pi|` e `|ky - pi|` entrambi `<= 0.1 pi`)*; ### **il punto si sceglie sull'ultimo quarto**, e se ne leggono tutti e quattro;
  - ### **`k = 0`.**
- ### **ASINTOTICO**, per ognuno dei tre punti: ### **il gamma del QUARTO quarto coincide con quello del TERZO entro il `5%` del massimo assoluto** *(il massimo su tutti i `k` del gamma dell'ultimo quarto)*. ### **Altrimenti NON ASINTOTICO**, e lo si scrive.
- ### **CHI VINCE:** quale delle due famiglie *(il picco a `(pi, pi)` o la banda)* ha il gamma piu' alto ### **nell'ULTIMO quarto**, a ogni lato e braccio. ### **Se la differenza e' sotto il `5%` del massimo: NON DECIDIBILE.**
- ### **`k = 0`:** ### **CRESCITA VERA** se il gamma dell'ultimo quarto e' `>= 0.5` volte quello della seconda meta' ### **E** `> 0.02`; ### **altrimenti TRANSITORIO** *(una lettura: deriva di fase che pesa `ln t / t`)*, e ### **la frase «nessuna lunghezza minima» si ritira.**
- ### **LA LARGHEZZA DEL PICCO:** gamma dell'ultimo quarto lungo la diagonale ### **negli ultimi `4` `m` prima di `pi`**, a lato `32` e `64`. ### **La semi-larghezza** e' il numero di passi `m` da `pi` a cui gamma scende sotto la meta' del picco. ### **Se e' la stessa in NUMERO DI ARCHI** *(stessi `m`, entro `1`)* ### **a `32` e `64`, il picco SEGUE LA GRIGLIA**; se raddoppia *(entro `1`)*, segue `k`; altrimenti ne' l'una ne' l'altra.

## 4. I CASI DI CONTROLLO

- ### **IL CONTO VECCHIO AL BIT:** `R2` a lato `31` coi parametri di `c38367db` ### **ridà la matrice gamma del `jsonl` di `c38367db` AL BIT** *(`0.3749` a `(9, 0)`)*. ### **Se no: STOP.**
- ### **DEVE FALLIRE:** la camminata sola *(`C2` esatta)* ### **a lato `32`, `N dtau 100`**: `max |ln|lambda|| <= N * 64 ulp` su ogni `k`. ### **Se cresce: STOP, il metodo e' rotto.**
- ### **DEVE RIUSCIRE:** `R2` a lato `32`, `N dtau 25`, ### **i numeri del guardiano** *(intero `0.3754` a `(10, 0)`; seconda meta' `0.585` a `(16, 16)`)* ### **entro `1e-3`**. ### **Se no: STOP.**

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. Le correzioni del guardiano annotate nella relazione: un commit.
3. Lo strumento esteso *(`--lungo`)*, con la voce d'inventario: ### **un commit a se'.**
4. Il conto dal blob committato e pulito, in background: `python csv/_stabilita_lineare.py --lungo > doc/referti_l2/stabilita_intervallo_lungo.txt`, con `doc/referti_l2/stabilita_intervallo_lungo.jsonl`.
5. Il referto e la relazione: un commit, `PUSHATO`, `FERMO` *(le domande sono di Luca; nessuna cura scelta)*.
