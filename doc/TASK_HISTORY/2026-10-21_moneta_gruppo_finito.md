# LA MONETA NEL GRUPPO FINITO (`eps dtau = pi/2`): CHE COSA FA ALL'INSTABILITA' DI `S3`

> **Il mandato:** decisione di Luca del `2026-10-21` alle `15:07`, sulla prima domanda di `a840e8f7`.
> ### **Una MISURA: nessuna cura scelta, nessuna decisione sulla premessa del gruppo finito
> (e' di Luca).** `leggi.yaml` e l'impronta `2e7f795d2a52fbe7` INTATTI. ### **`eps` si cambia
> SOLO come parametro della scena del conto.** Lo strumento `csv/_stabilita_lineare.py` *(blob
> `ce645dda`)* si estende con `--moneta`; i modi esistenti al bit.

**LIVELLO CORRENTE:** `L2`.

## 0. LA CONDIZIONE DI STOP DEL MANDATO, VERIFICATA

- ### **`eps` si cambia senza toccare `leggi.yaml` ne' il passo:** l'operatore della moneta *(`motore._moneta_spin`)* lo legge da ### **`parametri.get("eps")`**, cioe' dal `par` del tick; e il `par` lo costruisce ### **la scena** *(`scena_l2.scena` torna `{"eps": 0.5}`)*. ### **Lo strumento lo sostituisce nella scena, e basta.** ### **Nessuno STOP.**
- ### ⚠ **E UN FATTO CHE DECIDE LA LETTURA DI `R1`, scritto PRIMA dei numeri:** la moneta ruota di ### **`eps * dtau_nodo`** per tick *(due mezzi pezzi a frazione `0.5`)*, e ### **con `cs` acceso `dtau_nodo = cs * dtau`** *(`cs_m = 0.5` a rapporto `1`)*. ### **Quindi in `R1` «`eps dtau = pi/2`» da' una moneta di angolo `pi/4`, che NON sta nel gruppo**, e ### **il controllo «la moneta coincide con `-i sigma.n_h`» CADRA' per `R1`.** ### **Lo prevedo qui, e i bracci `R1` del mandato si leggono come «`R1` col gruppo sul tempo coordinato», NON «`R1` nel gruppo».**
  - ### **INFORMAZIONE AGGIUNTIVA, dichiarata prima** *(non e' un numero scelto: e' la stessa premessa applicata all'angolo VERO della moneta)*: ### **`R1` con `eps cs_m dtau = pi/2`**, cioe' ### **`eps = pi`** a `dtau 1` *(`A_cs`)* e ### **`eps = 8 pi`** a `dtau 0.125` *(`B_cs`)*. ### **Il controllo del gruppo li deve far passare.**

## 1. LA STELLA POLARE

1. **`A14`:** ### **non si applica**: nessuna legge cambia; la moneta resta unitaria per costruzione, e ### **la camminata sola esatta lo controlla a ogni `eps`.**
2. **Il gradino:** `(a)` ### **`RIF` deve ridare `594417f6`**; `(b)` ### **`eps = 0`** *(nessuna moneta)* e' il braccio che toglie la legge; `(c)` ### **non si applica.**
3. **Aggiunge un numero o una legge?** ### **`eps dtau = pi/2` NON e' un numero scelto per stabilizzare: viene dalla premessa del gruppo finito** *(`a840e8f7`, sez. `c`)*. ### **I controlli `0.45 pi` e `0.55 pi` ci sono proprio per dire se `pi/2` e' speciale o un punto di una curva.**
4. **Tocca `rho`, `c_s` o il segno?** ### **Tocca la camminata** *(il legame spin-moto)*, e attraverso `dtau_nodo` ### **la moneta legge `cs`** *(sez. `0`)*.
5. **Emergente o imposto?** ### **Se stabilizza, e' un RISULTATO della premessa, non una cura.**

## 2. LE PREVISIONI, scritte PRIMA dei numeri

- ### **Sulla materia allineata `-i sigma.n_h` e' una FASE** *(`a840e8f7`)*: ### **lo stato uniforme quasi non la sente**, e ### **il termine della moneta in `H` cambia valore** *(`eps h`)*. ### **Ma la crescita la portano le PERTURBAZIONI, che non sono allineate:** su di loro la moneta ### **ruota lo spin di `pi` attorno a `n_h`**, e ### **cambia la dispersione della camminata.**
- **Che cosa credo:**
  - ### **`R2` resta INSTABILE** *(la crescita e' di `S3`, e la moneta cambia la dispersione, non l'accoppiamento)*: il massimo cambia ### **di qualche decina per cento**, non va a zero;
  - ### **`pi/2` NON e' speciale:** credo a ### **una TENDENZA CONTINUA** fra `0.45 pi` e `0.55 pi`;
  - ### **`A` e `B` DIFFERISCONO oltre il `5%`:** a `dtau 1` i pezzi della camminata stanno a `theta = pi` *(lontani dal limite continuo)*, a `dtau 0.125` a `pi/8`: ### **la condizione sul tick da sola non basta.**
  - ### **`eps = 0`:** la moneta spenta ### **cambia poco** *(credo che la banda di `S3` non nasca dalla moneta)*.
- **Cosa NON so:** se a `dtau 1` le prove del metodo reggono *(la base, la linearita')*: ### **se no, `A` NON VALE, e non si legge.**

## 3. PROGETTAZIONE *(dal mandato, con le letture fissate)*

- ### **I bracci** *(lato `32`, base proiettata, `N dtau 100`, stimatore della NORMA, pendenza della seconda meta', come `594417f6`)*, ### **`R1` e `R2` per ognuno:**

  | | `dtau` | `eps` | `eps dtau` |
  |---|---|---|---|
  | `RIF` | `0.125` | `0.5` | `0.0625` |
  | `A` *(il passo dell'automa)* | `1` | `pi/2` | ### `pi/2` |
  | `B` *(il `dtau` di oggi)* | `0.125` | `4 pi` | ### `pi/2` |
  | `C045` | `0.125` | `3.6 pi` | `0.45 pi` |
  | `C055` | `0.125` | `4.4 pi` | `0.55 pi` |
  | `C0` *(nessuna moneta)* | `0.125` | `0` | `0` |
  | `A_cs` *(solo `R1`, informazione)* | `1` | `pi` | `eps cs_m dtau = pi/2` |
  | `B_cs` *(solo `R1`, informazione)* | `0.125` | `8 pi` | `eps cs_m dtau = pi/2` |

- ### **I CONTROLLI:**
  - ### **LA MONETA E' NEL GRUPPO:** a `eps dtau_nodo = pi/2`, ### **la matrice della moneta di un tick** *(i due mezzi pezzi, misurati applicando l'operatore a `(1, 0)` e `(0, 1)` su ogni estremita')* ### **coincide con `-i sigma.n_h` entro `64` ulp** *(stampato il massimo)*; ### **per `R1` dei bracci `A` e `B` lo stampo e PREVEDO che cada** *(sez. `0`)*;
  - ### **LA CAMMINATA SOLA ESATTA a ogni `eps`:** modulo `1` entro `N * 64` ulp;
  - ### **`P3` al bit a ogni braccio;**
  - ### **la linearita'** *(`1e-7` contro `1e-6`)* ### **sui bracci `A` e `B`**, entro `1e-3` del massimo;
  - ### **`RIF` = `594417f6` entro `1e-3`** *(le pendenze della norma, su ogni `k`)*.
  - ### **Se il braccio `A` rompe una prova del metodo** *(base `> 1e3` ulp, linearita' fuori banda, camminata sola non esatta)*: ### **NON VALIDO col perche', e non si legge.**
- ### **LE LETTURE, fissate qui:**
  - ### **STABILE:** la pendenza massima su ogni `k` `<= 1e-3` del massimo di `RIF`; ### **altrimenti INSTABILE**, col massimo, dove, e il rapporto con `RIF`;
  - ### **PUNTO SPECIALE:** `pi/2` *(`B`)* e' speciale se il suo massimo differisce da QUELLO di ENTRAMBI i controlli `0.45 pi` e `0.55 pi` ### **di piu' di `3` volte la differenza fra i due controlli**; ### **altrimenti TENDENZA CONTINUA**, non un effetto del gruppo;
  - ### **`A` CONTRO `B`:** se differiscono oltre il `5%` del massimo di `RIF`, ### **la condizione sul tick NON basta**;
  - ### **per famiglia:** `(pi, pi)`; `(pi, 0)`; ### **la banda = il massimo lungo `(m, 0)` per `m` fra `h/4` e `3h/4`** *(`0.25`-`0.75 pi`; dichiarato qui)*; `k = 0`.
- ### **Il comando:** `python csv/_stabilita_lineare.py --moneta > doc/referti_l2/moneta_gruppo_finito.txt`, con `.jsonl`.

## 3-bis. ANNOTAZIONE: LA SECONDA VERSIONE DEL MANDATO (`15:08`), CORTA, SOLO `R2` -- VALE SOLO LEI *(`[[PRECEDENZA-IN-CODA]]`; si annota, la versione lunga sopra resta come era)*

- ### **La stella polare in cinque righe:** `1` `A14` non si applica *(nessuna legge cambia)*; `2` il gradino `(a)` sono i controlli; `3` ### **`eps dtau = pi/2` viene dalla premessa del gruppo finito, non e' scelto per stabilizzare**; `4` tocca la camminata, non `rho` ne' `cs` *(`R2`: `cs` spento)*; `5` ### **se stabilizza, e' un risultato della premessa.**
- ### **La previsione in due righe:** ### **`R2` resta INSTABILE**, col massimo cambiato di qualche decina per cento; ### **`pi/2` non e' speciale** *(tendenza continua)*, e ### **`A` e `B` differiscono oltre il `5%`.**
- ### **I bracci, SOLO `R2`** *(lato `32`, base proiettata, `N dtau 100`, norma, seconda meta')*: ### **`RIF` NON si rifa'**, si rilegge da `594417f6`; `A` *(`dtau 1`, `eps pi/2`)*; `B` *(`dtau 0.125`, `eps 4 pi`)*; ### **`C045` e `C055`** *(`dtau 0.125`, `eps dtau = 0.45 pi`, `0.55 pi`)*. ### **Cadono:** `C0`, `A_cs`, `B_cs` e tutti i bracci `R1` *(e con loro il problema dell'angolo `cs * dtau` della sez. `0`, che resta scritto per quando `R1` si fara')*.
- ### **I controlli:** la moneta a `pi/2` `= -i sigma.n_h` entro `64` ulp; la camminata sola esatta a ogni `eps`; ### **la linearita' SOLO su `B`.** *(E la base uniforme `<= 1e3` ulp, che lo strumento stampa comunque.)*
- ### **LE LETTURE, copiate:**
  - ### **STABILE** se la pendenza massima su ogni `k` `<= 1e-3` di `0.407`; altrimenti il massimo, dove, e il rapporto con `RIF`;
  - ### **PUNTO SPECIALE** se `pi/2` differisce da ENTRAMBI i controlli di piu' di `3` volte la loro differenza; altrimenti ### **TENDENZA CONTINUA**;
  - ### **`A` contro `B`:** differenza oltre il `5%` di `0.407` → ### **conta come si arriva a `pi/2`.**
- ### **La relazione in poche righe:** i numeri, le letture, ### **e se vale la pena fare `R1`.**

## 3-ter. ANNOTAZIONE DEL `2026-10-21`, `16:41`: LA SPAZZATA DI `eps dtau`, SOLO `R2` *(decisione di Luca: l'ultimo run prima dei triangoli; si annota)*

- ### **I bracci:** `R2`, lato `32`, `dtau 0.125`, base proiettata, `N dtau 100`, norma, seconda meta'. ### **NUOVI:** `eps dtau` = `0.60`, `0.65`, `0.70`, `0.75 pi`. ### **RILETTI da `b8197923`** *(non rifatti)*: `0.45`, `0.50` *(`B`)*, `0.55 pi`. ### **Controlli:** la camminata sola esatta a ogni `eps`; la base `<= 1e3` ulp. Nessuna linearita'.
- ### **LE LETTURE, per ogni `eps dtau`:**
  - ### **il massimo di gamma su tutti i `k`, DOVE, e la famiglia** *(la componente piu' grande di `|k|`, in unita' di `pi`)*: ### **RETICOLO** se `>= 0.75` su almeno un asse; ### **BANDA** se fra `0.25` e `0.75`; ### **ONDE LUNGHE** se sotto `0.25`;
  - ### **STABILE** se il massimo `<= 1e-3` di `0.407`; ### **la FINESTRA STABILE** e' l'insieme degli `eps dtau` stabili *(anche vuoto)*;
  - ### **SENZA RETICOLO** se tutti i `k` con `|k| >= 0.75 pi` su un asse hanno gamma `<= 1e-3` di `0.407`.
- ### **Nessuna cura:** ### **un `eps` scelto perche' stabilizza sarebbe una toppa** *(`A1`)*.
- ### **E nello stesso commit dello strumento la correzione della colonna «banda»** *(errore `C.6`: `m` fra `h/4` e `3h/4`)*.

## 4. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `--moneta` e l'inventario: ### **un commit a se'.**
3. La corsa dal blob committato *(`~1.5` h)*; il referto e la relazione: un commit, `PUSHATO`, `FERMO`.
