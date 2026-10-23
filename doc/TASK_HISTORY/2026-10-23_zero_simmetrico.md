> ### ⛔ **GRIGLIA QUADRATA -- risultato da rifare sui triangoli (DECISIONE-SOLO-TRIANGOLI)**

# LO ZERO SIMMETRICO IN MEMORIA: LA FORZA, EINSTEIN E L'UNIVERSALITA' COI PEZZI PARZIALI A GENERATORE SIMMETRICO

> **Il mandato:** di Luca, dopo `05055fc6`. ### **Una MISURA in memoria: non cambia il nucleo, non sceglie la convenzione** *(la scelta e' di Luca)*. ### **`leggi.yaml`, l'impronta
> `2e7f795d2a52fbe7` e il nucleo intatti; `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE; git `e96ca41a`)*. ### **Importati, non copiati:** `_gravita_collettiva.convenzione_alternativa`
> *(il meccanismo)*, `_forza_da_cs` *(`rami`, `catena_principale`, `bersaglio`, `righe_del_ramo`, `spazio_del_ramo`, `segui`, `avvolgi`, `corsa`)*, `_scala_e_zero` *(`cammino`, `rami_a`,
> `curvatura`, `livelli`, `a_`)*, `_massa_vicino_al_cono.matrice`, `_universalita_massa.blob`. ### **L'errore del guardiano n.47:** ### **aveva previsto la violazione del moto come `s`;
> `05055fc6` ha misurato `s^2`** *(il palindromo)*.

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica** *(nessuna legge cambia nel repo; la convenzione simmetrica vive solo in memoria)*.
2. **Il gradino:** ### **`(a)` i controlli** *(la convenzione simmetrica = oggi per `e^{-i pi s}` a `cs` uniforme; la dinamica uguale a `eta = 0`, diversa nel gradiente)*; ### **`(b)` Einstein e
   l'universalita'**; ### **`(c)` LA FORZA, la prova che conta.**
3. **Aggiunge un numero o una legge?** ### **No.** ### **E' la stessa legge scritta con un'altra fase per pezzo** ### **-- che nel gradiente diventa un POTENZIALE: la convenzione e' FISICA.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` SI'** *(a mano, uniforme o col profilo di `_forza_da_cs`)*: ### **e' la variabile.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **con lo zero simmetrico i due rami di `eps 0` cadono insieme, e verso dove?**

## 1. LE VERIFICHE NEL CODICE *(fatte prima, cercando per nome; le righe sono del blob di oggi)*

- ### **`(i)` HANNO LA FORMA `exp(i theta (I - P))`** *(i pezzi PARZIALI di `B`)*:
  - ### **`CAMM-GROVER` e `CAMM-GROVER-VUOTO`:** ### **`flussi_parziali.grover`** *(riga `317`)*, ### **`G(theta) = P_u + e^{i theta} (I - P_u) = exp(i theta (I - P_u))`** *(l'intestazione,
    riga `20`)*; ### **chiamata da `motore._grover`** *(riga `446`)* ### **e `_grover_scalare`** *(riga `460`)*;
  - ### **`CAMM-SPOSTAMENTO` e `CAMM-SPOSTAMENTO-VUOTO`:** ### **`flussi_parziali.hop_psi`** *(riga `378`)* ### **e `hop_phi`** *(riga `411`)*, ### **`I + (e^{i theta} - 1) P- = exp(i theta P-)`**,
    `P- = (I - S_U)/2` *(`_alfa_beta`, riga `355`; l'intestazione, riga `19`)*; ### **chiamate da `motore._spostamento_trasporto`** *(riga `538`)* ### **e dal pezzo del vuoto** *(riga `688`)*.
- ### **NON hanno quella forma:**
  - ### **`CAMM-MONETA-SPIN`:** ### **`exp(-i a sigma.n)`** *(`motore._moneta_spin`, riga `464`; `_ruota_attorno_a_n`, riga `484`)*: ### **`sigma.n` ha TRACCIA NULLA, fasi proprie `+-a`: e' gia' nella
    forma simmetrica**;
  - ### **`CAMM-MATERIA-VUOTO`** *(il legame)*: ### **`materia_vuoto.applica`** *(riga `116`)*: ### **due FASI, `exp(-i alpha dtau_nodo)` e `exp(-i beta dtau_nodo)`**, ### **non un pezzo parziale**;
  - ### **`CAMM-FASE-VUOTO`:** ### **`energia_pesata.applica`** *(riga `361`)*: ### **una fase sul vuoto**, ### **ASSENTE con `lambda_c = None`** *(riga `375`)*.
- ### **`(ii)` LA CONVENZIONE SIMMETRICA, e il suo meccanismo:** ### **`exp(i theta (I - 2P)/2) = exp(-i theta P/2) exp(i theta (I - P)/2)`** *(i due fattori commutano: stesso `P`)*:
  ### **il pezzo di oggi a META' frazione, seguito dal pezzo dell'ALTERNATIVA a meta' frazione** ### **-- e l'alternativa e' quella di `convenzione_alternativa()`, IMPORTATA.**
  ### **Prova a vuoto in memoria** *(lato `16`, la matrice di un tick intera, `12 x 12`, ogni `k`)*: ### **`A_simm = e^{-i pi s} A_oggi` entro `6.8e-16`** *(materia e vuoto, `eps 0` e
  `0.5`, `s 0.3`, `0.9`, `1.0`)*: ### **a `theta = pi`** *(`s = 1`)* ### **torna al passo di oggi a meno della fase `-1`**; ### **a `cs` uniforme `omega_simm(0) = omega(0) + pi s`**
  *(lo strumento lo ri-controlla, DI SERVIZIO, entro `1e-12`)*.

## 2. LE PREVISIONI *(scritte prima dei numeri)*

- ### ⚠ **L'IDENTIFICAZIONE DEL GUARDIANO NON E' ESATTA:** ### **lo zero simmetrico sposta di `pi s`** *(sulla carta e nella prova a vuoto)*; ### **a `eps 0`, con la fase CONTINUA da `s`
  piccolo:** ### **il ramo a curvatura NEGATIVA** *(il «basso» di oggi, `omega = 0`)* ### **va a `+pi s`**, ### **quello a curvatura POSITIVA** *(l'«alto», `-2 pi s`)* ### **a `-pi s`.**
  ### **Lo zero A META' di `05055fc6` dava `-pi (1 - s)` e `+pi (1 - s)`**: ### **= lo zero simmetrico `+- pi` per tick** *(mod `2 pi`)*. ### **Le due differiscono per una COSTANTE `pi`.**
- ### **PARTE A, EINSTEIN:** ### **`Q = omega omega''/v^2`, col Dirac `omega'' ~ +- v^2/Dt`:** ### **zero simmetrico: `Q ~ -pi s/Dt` per tutti e due i rami** *(il segno di `omega` e' OPPOSTO a
  quello della curvatura)*; ### **con `Dt ~ pi s (1 - s)`: `Q ~ -1/(1 - s)`, cioe' `~ -10` a `s 0.9`, `~ -20` a `0.95`.** ### ⛔ **LA PREVISIONE DEL GUARDIANO** *(«`Q` come lo zero a meta',
  `~ 1`»)* ### **LA PREVEDO FALSA**: ### **`Q` cambia segno e scala con una costante `pi` che lo zero a meta' aggiunge e quello simmetrico no.** ### **`D` non cambia** *(`pi s/s = pi`)*.
- ### **PARTE B, LA FORZA:** ### **`a_H/a_RG = s (omega''/v^2) (d omega(0)/ds)`**, ### **e lo zero simmetrico aggiunge `pi` a `d omega(0)/ds`** *(il potenziale `pi s(x)`)*:
  - ### **`eps 0`, i DUE rami:** ### **curvatura `-`: `s (-1/Dt)(0 + pi)`; curvatura `+`: `s (+1/Dt)(-2 pi + pi)`**: ### **TUTTI E DUE `-pi s/Dt ~ -1/(1 - s)`**: ### **LO STESSO VERSO**
    *(come prevede il guardiano)* ### **MA VERSO `cs` ALTO: REPULSIVA** *(il guardiano diceva verso `cs` basso)*; ### **in modulo `~ 1/(1 - s)`: `-1.4` a `s0 0.3`, `-2` a `0.5`, `-10` a `0.9`**,
    ### **che tende a `-1` per `s0 -> 0`** *(il modulo giusto, il segno sbagliato)*.
  - ### ⭐ **E LO ZERO A META' DAREBBE LA STESSA FORZA** *(una costante `pi` non e' un potenziale)*: ### **il suo `Q ~ 1` NON implica la forza della relativita' generale**, ### **perche' la sua
    `omega(0)` non e' proporzionale a `s`.** ### **La relativita' generale per un pacchetto fermo vuole `omega(0) = s E0`** *(allora `a_H/a_RG = Q`)* ### **E `Q = 1` INSIEME.**
  - ### **convenzione di oggi:** ### **i numeri di `557d94d6`** *(basso `0`, alto `-17.5`..`-35.8`; `eps 0.5` `+3.65`..`+9.55`)*, ### **rifatti con lo stesso strumento a `s0 0.3` e `0.5`.**
  - ### **`eps 0.5`:** ### **nessuna previsione** *(lo spostamento `pi` aggiunto a `d omega(0)/ds = -1.85` a `s 0.9` lo porta a `+1.29`: col segno della curvatura `-`, `a_H` CAMBIA VERSO, verso `cs`
    ALTO; e' un conto, non una previsione del mandato)*.
- ### **PARTE C, L'UNIVERSALITA':** ### **`E0_simm = E0 + pi`** *(continua)*, ### **`M` uguale**: ### **i `Vi` di `E0` cambiano** *(i rapporti di numeri spostati di `pi`)*, ### **quelli di `M` no**;
  ### **`Q` per specie** *(Einstein come universalita': `E0/m_inerziale`)* ### **dipende da `s` come `-1/(1 - s)` a `eps 0`.**

## 3. IL METODO

- ### **LA CONVENZIONE SIMMETRICA, in memoria:** ### **`flussi_parziali.grover`, `hop_psi`, `hop_phi` sostituite da: il pezzo di oggi a frazione `f/2`, poi il pezzo dell'alternativa
  a `f/2`** *(le funzioni dell'alternativa prese DENTRO `convenzione_alternativa()` e usate fuori; il nucleo non si tocca)*.
- ### **PARTE A:** ### **`s` in `(0.3, 0.5, 0.7, 0.9, 0.95)`, `eps` in `(0, 0.25, 0.5, 1.0)`, lato `64`**; ### **la fase continua da `s` piccolo con `_scala_e_zero.cammino`** *(la sua griglia
  `S_LISTA` impostata in memoria per avere i punti `s (1 +- h)`)*, ### **`omega''` con `_scala_e_zero.curvatura`** *(Richardson)*, ### **`v` dal fit, `D`, `Q`**, ### **NELLE DUE CONVENZIONI.**
- ### **PARTE B:** ### **la previsione di Hamilton e la corsa di `_forza_da_cs`** *(`corsa()`: il pacchetto `e * gaussiana`, `W = Lx/16`, `x0 = Lx/4`, la finestra `|<x> - x0| < Lx/32`, `T <= Lx/4`,
  almeno `6` punti, la norma fuori `<= 10%`)*, ### **NELLE DUE CONVENZIONI**, ### **`s0` in `(0.3, 0.5, 0.9)`, `eta` in `(0, +5e-4, +1e-3, -1e-3, +5e-3, +1e-2, -1e-2)`, `eps` in `(0, 0.5)`, la
  catena principale** *(`catena_principale`, `righe_del_ramo`)* ### **coi rami NOMINATI PER LA CURVATURA** *(«curv -», «curv +»: a `s0 0.3` la fase principale del ramo alto, `-2 pi s = -1.885`,
  sta SOTTO lo `0` del basso, e il nome per `omega(0)` di `righe_del_ramo` li scambierebbe)*, ### **`Lx` in `(128, 256)`.** ### **La linearita': `a(eta)/a(eta/2) = 2` entro il `5%`.**
  ### **`a_H` coi DUE spettri** *(oggi e simmetrico)* ### **a `s0 (1 +- eta)`.** ### **Accanto: `557d94d6` a `s0 0.9`** *(deve coincidere coi numeri rifatti)*.
- ### **PARTE C:** ### **le specie seguite da `s 0.02`** *(`_scala_e_zero`, le stesse `s` di `05055fc6`)*, ### **`Vi` di `E0` e di `M`, e `Q` per specie, NELLA CONVENZIONE SIMMETRICA.**

## 4. I CRITERI, FISSATI ORA *(dal mandato)*

- ### **DEVE PASSARE:** ### **`(ii)`: `A_simm = e^{-i pi s} A_oggi` entro `1e-12`** *(la matrice intera, ogni `k`, `s` della parte `A`, `eps` della parte `A`, e `s = 1`)*.
- ### **DEVE PASSARE:** ### **`eta = 0`: la dinamica uguale a meno di una fase globale** *(`|psi|^2` e `|phi|^2` al tick `100` uguali entro `1e-12`, relativo al massimo)*, ### **`Lx 128, s0 0.5, eps 0.5`.**
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«la dinamica nel gradiente** *(`eta = 1e-2`)* ### **e' uguale a quella di oggi»** *(la stessa misura: la differenza FINITA e stampata)*.
- ### **PUO' FALLIRE:** ### **`eps 0, s0 0.3`, i due rami con `a_mis/a_RG > 0` e entro il `20%` di `1`** *(convenzione simmetrica, `eta` `1e-3` e `1e-2`, le due `Lx`, le righe leggibili)*.
  ### **LA MIA PREVISIONE: FALLISCE, per il segno** *(sez. `2`)*.
- ### **DI SERVIZIO:** ### **i numeri di oggi rifatti a `s0 0.9` uguali a `557d94d6`** *(entro `1e-12` relativo)*.
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE:** ### **le tabelle di `Q`, `a_mis/a_RG`, `a_mis/a_H` e `Vi` nelle due convenzioni.** ### **A parte: la lettura in tre righe e una riga per
  la decisione di Luca** *(informazione, non scelta)*.

### 📝 **ANNOTAZIONE 1** *(prima della corsa dello strumento committato, nel commit dello strumento)*: ### **la prova a vuoto in memoria** *(griglia ridotta: `eps 0`, `s0 0.3` e
`0.9`, `Lx 128`; il `jsonl` negli appunti)* ### **ha stampato dei numeri; li dichiaro e NON correggo le previsioni:** ### **nella simmetrica, a `eps 0`, i due rami vanno VERSO `cs` ALTO**
*(`a_mis/a_RG ~ -1.85` a `s0 0.3`, contro `a_H/a_RG = -1.96`)*; ### **`Q = -1.96` a `s 0.3`, `-9.86` a `0.9`.** ### ⚠ **E una mia stima della sez. `2` era sbagliata nel numero:** ### **`Dt(0.3)`
e' `0.481`, non `pi 0.3 0.7 = 0.66`** *(la forma `pi s (1 - s)` vale vicino al cono, non a `s 0.3`)*: ### **`-pi s/Dt` a `s0 0.3` e' `-1.96`, non `-1.4`.** ### **Il verso previsto resta.**
### **E la convenzione di oggi rifatta a `s0 0.9` coincide con `557d94d6` al bit.**

## 5. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_zero_simmetrico.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima dei numeri;
3. la corsa, il referto `doc/referti_l2/zero_simmetrico.txt` e `.jsonl`, la relazione, e la sezione `6` qui sotto.

## 6. I RISULTATI *(scritti dopo la corsa, sotto)*

### **LA CORSA:** `python csv/_zero_simmetrico.py`, strumento sha1-BYTE `b400d76e` *(`809c213f`, committato e pulito)*. ### **`4` controlli su `5`.**

- ### **DEVE PASSARE `(ii)`: PASSA** *(`A_simm = e^{-i pi s} A_oggi` entro `7.0e-16`, la matrice intera a ogni `k`, `s 0.3`-`0.95` e `1`, ogni `eps`)*.
- ### **DEVE PASSARE, `eta = 0`: PASSA** *(`|psi|^2` e `|phi|^2` al tick `100` uguali entro `2.3e-14`)*.
- ### **DEVE FALLIRE, la dinamica nel gradiente uguale: FALLISCE per la chiave giusta** *(lo scarto `9.9e-2`)*: ### **nel gradiente la convenzione e' FISICA.**
- ### ⚠ **PUO' FALLIRE, `eps 0, s0 0.3`, `a/a_RG > 0` entro il `20%` di `1`: FALLISCE** ### **-- per il SEGNO, come previsto:** ### **`-1.84`..`-1.90` sui due rami.**
- ### **DI SERVIZIO: la convenzione di oggi rifatta a `s0 0.9` = `557d94d6` al bit** *(`0.0`)*.

### 6.1 LA FORZA NELLE DUE CONVENZIONI *(`a/a_RG > 0` = verso `cs` BASSO)*

| `eps` | `s0` | ramo | `Lx` | `eta` | oggi `a/a_RG` | oggi `a/a_H` | simm `a/a_RG` | simm `a/a_H` | simm `a_H/a_RG` | si legge *(oggi / simm)* |
|---|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.3` | curv + Dt 0.4807 | `128` | `0.001` | `-3.762` | `+0.959` | `-1.879` | `+0.958` | `-1.961` | si' / si' |
| `0` | `0.3` | curv + Dt 0.4807 | `128` | `0.01` | `-3.765` | `+0.960` | `-1.883` | `+0.960` | `-1.961` | si' / si' |
| `0` | `0.3` | curv + Dt 0.4807 | `256` | `0.001` | `-3.783` | `+0.965` | `-1.895` | `+0.967` | `-1.961` | si' / si' |
| `0` | `0.3` | curv + Dt 0.4807 | `256` | `0.01` | `-3.779` | `+0.964` | `-1.892` | `+0.965` | `-1.961` | si' / si' |
| `0` | `0.3` | curv - Dt 0.4807 | `128` | `0.001` | `+0.037` | -- | `-1.847` | `+0.942` | `-1.961` | **no** / si' |
| `0` | `0.3` | curv - Dt 0.4807 | `128` | `0.01` | `+0.042` | -- | `-1.842` | `+0.939` | `-1.961` | si' / si' |
| `0` | `0.3` | curv - Dt 0.4807 | `256` | `0.001` | `-0.009` | -- | `-1.897` | `+0.968` | `-1.961` | si' / si' |
| `0` | `0.3` | curv - Dt 0.4807 | `256` | `0.01` | `-0.008` | -- | `-1.896` | `+0.967` | `-1.961` | si' / si' |
| `0` | `0.5` | curv + Dt 0.6858 | `128` | `0.001` | `-4.401` | `+0.961` | `-2.206` | `+0.963` | `-2.291` | si' / si' |
| `0` | `0.5` | curv + Dt 0.6858 | `128` | `0.01` | `-4.392` | `+0.959` | `-2.198` | `+0.960` | `-2.291` | si' / si' |
| `0` | `0.5` | curv + Dt 0.6858 | `256` | `0.001` | `-4.410` | `+0.963` | `-2.206` | `+0.963` | `-2.291` | si' / si' |
| `0` | `0.5` | curv + Dt 0.6858 | `256` | `0.01` | `-4.408` | `+0.962` | `-2.205` | `+0.962` | `-2.291` | si' / si' |
| `0` | `0.5` | curv - Dt 0.6858 | `128` | `0.001` | `+0.064` | -- | `-2.130` | `+0.930` | `-2.291` | **no** / si' |
| `0` | `0.5` | curv - Dt 0.6858 | `128` | `0.01` | `+0.015` | -- | `-2.178` | `+0.951` | `-2.291` | **no** / si' |
| `0` | `0.5` | curv - Dt 0.6858 | `256` | `0.001` | `+0.006` | -- | `-2.198` | `+0.960` | `-2.291` | **no** / si' |
| `0` | `0.5` | curv - Dt 0.6858 | `256` | `0.01` | `+0.003` | -- | `-2.201` | `+0.961` | `-2.291` | **no** / si' |
| `0` | `0.9` | curv + Dt 0.2836 | `128` | `0.001` | `-17.806` | `+0.893` | `-8.850` | `+0.888` | `-9.969` | si' / si' |
| `0` | `0.9` | curv + Dt 0.2836 | `128` | `0.01` | `-17.486` | `+0.877` | `-8.699` | `+0.873` | `-9.969` | si' / si' |
| `0` | `0.9` | curv + Dt 0.2836 | `256` | `0.001` | `-18.612` | `+0.933` | `-9.249` | `+0.928` | `-9.969` | si' / si' |
| `0` | `0.9` | curv + Dt 0.2836 | `256` | `0.01` | `-18.442` | `+0.925` | `-9.278` | `+0.931` | `-9.969` | si' / si' |
| `0` | `0.9` | curv - Dt 0.2836 | `128` | `0.001` | `+0.471` | -- | `-8.488` | `+0.851` | `-9.969` | **no** / si' |
| `0` | `0.9` | curv - Dt 0.2836 | `128` | `0.01` | `+0.254` | -- | `-8.684` | `+0.871` | `-9.969` | **no** / si' |
| `0` | `0.9` | curv - Dt 0.2836 | `256` | `0.001` | `+0.121` | -- | `-9.244` | `+0.927` | `-9.969` | si' / si' |
| `0` | `0.9` | curv - Dt 0.2836 | `256` | `0.01` | `+0.063` | -- | `-9.280` | `+0.931` | `-9.969` | **no** / si' |
| `0.5` | `0.3` | curv - Dt 0.4684 | `128` | `0.001` | `+0.018` | `-51.383` | `-1.916` | `+0.952` | `-2.013` | **no** / si' |
| `0.5` | `0.3` | curv - Dt 0.4684 | `128` | `0.01` | `+0.039` | `-112.167` | `-1.895` | `+0.942` | `-2.013` | **no** / si' |
| `0.5` | `0.3` | curv - Dt 0.4684 | `256` | `0.001` | `-0.010` | `+27.972` | `-1.948` | `+0.968` | `-2.013` | **no** / si' |
| `0.5` | `0.3` | curv - Dt 0.4684 | `256` | `0.01` | `-0.016` | `+46.687` | `-1.954` | `+0.971` | `-2.013` | si' / si' |
| `0.5` | `0.5` | curv - Dt 0.6718 | `128` | `0.001` | `+0.108` | `+1.486` | `-2.134` | `+0.942` | `-2.265` | **no** / si' |
| `0.5` | `0.5` | curv - Dt 0.6718 | `128` | `0.01` | `+0.092` | `+1.260` | `-2.149` | `+0.949` | `-2.265` | si' / si' |
| `0.5` | `0.5` | curv - Dt 0.6718 | `256` | `0.001` | `+0.071` | `+0.977` | `-2.179` | `+0.962` | `-2.265` | si' / si' |
| `0.5` | `0.5` | curv - Dt 0.6718 | `256` | `0.01` | `+0.072` | `+0.988` | `-2.178` | `+0.962` | `-2.265` | si' / si' |
| `0.5` | `0.9` | curv - Dt 0.4253 | `128` | `0.001` | `+3.005` | `+0.768` | `-3.206` | `+1.173` | `-2.735` | **no** / **no** |
| `0.5` | `0.9` | curv - Dt 0.4253 | `128` | `0.01` | `+3.651` | `+0.932` | `-2.553` | `+0.934` | `-2.732` | si' / si' |
| `0.5` | `0.9` | curv - Dt 0.4253 | `256` | `0.001` | `+3.743` | `+0.956` | `-2.594` | `+0.948` | `-2.735` | si' / si' |
| `0.5` | `0.9` | curv - Dt 0.4253 | `256` | `0.01` | `+3.726` | `+0.951` | `-2.601` | `+0.952` | `-2.732` | si' / si' |

### 6.2 EINSTEIN `Q = omega(0) omega''(0)/v^2` E `D` *(lato `64`, la fase continua)*

| `eps` | `s` | ramo | oggi `omega(0)` | oggi `Q` | oggi `D` | simm `omega(0)` | simm `Q` | simm `D` |
|---|---|---|---|---|---|---|---|---|
| `0` | `0.3` | curv + Dt 0.4807 | `-1.8850` | `-3.9169` | `+2.96e-12` | `-0.9425` | `-1.9584` | `+2.22e-12` |
| `0` | `0.3` | curv - Dt 0.4807 | `+0.0000` | `-0.0000` | `+2.47e-15` | `+0.9425` | `-1.9584` | `+0.00e+00` |
| `0` | `0.5` | curv + Dt 0.6858 | `-3.1416` | `-4.5747` | `+0.00e+00` | `-1.5708` | `-2.2873` | `-1.78e-12` |
| `0` | `0.5` | curv - Dt 0.6858 | `-0.0000` | `+0.0000` | `-8.88e-13` | `+1.5708` | `-2.2873` | `-8.88e-13` |
| `0` | `0.7` | curv + Dt 0.6563 | `-4.3982` | `-6.6856` | `+0.00e+00` | `-2.1991` | `-3.3428` | `+0.00e+00` |
| `0` | `0.7` | curv - Dt 0.6563 | `+0.0000` | `-0.0000` | `+4.53e-16` | `+2.1991` | `-3.3428` | `+6.34e-13` |
| `0` | `0.9` | curv + Dt 0.2836 | `-5.6549` | `-19.7228` | `-9.87e-13` | `-2.8274` | `-9.8614` | `-9.87e-13` |
| `0` | `0.9` | curv - Dt 0.2836 | `-0.0000` | `+0.0000` | `-2.74e-13` | `+2.8274` | `-9.8614` | `+4.93e-13` |
| `0` | `0.95` | curv + Dt 0.1454 | `-5.9690` | `-39.7570` | `-1.40e-12` | `-2.9845` | `-19.8785` | `-4.67e-13` |
| `0` | `0.95` | curv - Dt 0.1454 | `+0.0000` | `-0.0000` | `-2.46e-13` | `+2.9845` | `-19.8785` | `+2.34e-13` |
| `0.25` | `0.3` | curv - Dt 0.4776 | `+0.0020` | `-0.0043` | `-2.23e-02` | `+0.9445` | `-1.9756` | `-2.23e-02` |
| `0.25` | `0.5` | curv - Dt 0.6823 | `+0.0000` | `-0.0000` | `-4.90e-02` | `+1.5708` | `-2.2991` | `-4.90e-02` |
| `0.25` | `0.7` | curv - Dt 0.6580 | `-0.0111` | `+0.0168` | `-1.26e-01` | `+2.1881` | `-3.3175` | `-1.26e-01` |
| `0.25` | `0.9` | curv + Dt 0.6021 | `-5.5848` | `-7.9320` | `+7.56e-01` | `-2.7574` | `-3.9162` | `+7.56e-01` |
| `0.25` | `0.9` | curv - Dt 0.3327 | `-0.0701` | `+0.2089` | `-7.56e-01` | `+2.7574` | `-8.2190` | `-7.56e-01` |
| `0.25` | `0.95` | curv + Dt 0.3467 | `-5.8422` | `-15.6833` | `+1.59e+00` | `-2.8577` | `-7.6714` | `+1.59e+00` |
| `0.25` | `0.95` | curv - Dt 0.2444 | `-0.1268` | `+0.5127` | `-1.59e+00` | `+2.8577` | `-11.5508` | `-1.59e+00` |
| `0.5` | `0.3` | curv - Dt 0.4684 | `+0.0081` | `-0.0173` | `-8.86e-02` | `+0.9506` | `-2.0274` | `-8.86e-02` |
| `0.5` | `0.5` | curv - Dt 0.6718 | `-0.0000` | `+0.0000` | `-1.95e-01` | `+1.5708` | `-2.3348` | `-1.95e-01` |
| `0.5` | `0.7` | curv - Dt 0.6622 | `-0.0434` | `+0.0654` | `-4.81e-01` | `+2.1557` | `-3.2483` | `-4.81e-01` |
| `0.5` | `0.9` | curv + Dt 0.0132 | `-5.6706` | `-293.2259` | `+1.59e-01` | `-2.8432` | `-147.0201` | `+1.59e-01` |
| `0.5` | `0.9` | curv - Dt 0.4253 | `-0.2284` | `+0.5344` | `-1.77e+00` | `+2.5990` | `-6.0804` | `-1.77e+00` |
| `0.5` | `0.95` | curv + Dt 0.0163 | `-5.9777` | `-263.9073` | `+1.75e-01` | `-2.9932` | `-132.1459` | `+1.75e-01` |
| `0.5` | `0.95` | curv + Dt 1.0325 | `-5.6277` | `-5.3146` | `+2.46e+00` | `-2.6432` | `-2.4961` | `+2.46e+00` |
| `0.5` | `0.95` | curv - Dt 0.3735 | `-0.3413` | `+0.9094` | `-2.46e+00` | `+2.6432` | `-7.0425` | `-2.46e+00` |
| `1` | `0.3` | curv - Dt 0.4347 | `+0.0321` | `-0.0737` | `-3.47e-01` | `+0.9746` | `-2.2390` | `-3.47e-01` |
| `1` | `0.5` | curv - Dt 0.6309 | `+0.0000` | `-0.0000` | `-7.69e-01` | `+1.5708` | `-2.4863` | `-7.69e-01` |
| `1` | `0.7` | curv + Dt 0.0796 | `-4.5149` | `-54.5386` | `+4.06e-01` | `-2.3157` | `-27.9737` | `+4.06e-01` |
| `1` | `0.7` | curv - Dt 0.6668 | `-0.1620` | `+0.2426` | `-1.65e+00` | `+2.0371` | `-3.0493` | `-1.65e+00` |
| `1` | `0.9` | curv + Dt 0.1724 | `-5.7146` | `-32.5374` | `+6.06e-01` | `-2.8871` | `-16.4386` | `+6.06e-01` |
| `1` | `0.9` | curv - Dt 0.5818 | `-0.6241` | `+1.0706` | `-2.92e+00` | `+2.2033` | `-3.7796` | `-2.92e+00` |
| `1` | `0.95` | curv + Dt 0.1904 | `-6.0019` | `-31.0373` | `+6.63e-01` | `-3.0174` | `-15.6037` | `+6.63e-01` |
| `1` | `0.95` | curv - Dt 0.5609 | `-0.8017` | `+1.4268` | `-3.08e+00` | `+2.1828` | `-3.8849` | `-3.08e+00` |

### 6.3 `Q` PER SPECIE *(simmetrica; le specie seguite da `s 0.02`)*

| specie | `0.02` | `0.05` | `0.1` | `0.2` | `0.3` | `0.5` | `0.7` | `0.9` | `0.95` | `0.99` |
|---|---|---|---|---|---|---|---|---|---|---|
| `eps 0, liv 0` | `-1.84` | `-1.84` | `-1.85` | `-1.89` | `-1.96` | `-2.29` | `-3.34` | `-9.86` | `-19.88` | `-67.36` |
| `eps 0, liv 1` | `-1.84` | `-1.84` | `-1.85` | `-1.89` | `-1.96` | `-2.29` | `-3.34` | `-9.86` | `-19.88` | `-67.36` |
| `eps 0.25, liv 0` | `-1.86` | `-1.86` | `-1.87` | `-1.91` | `-1.98` | `-2.30` | `-3.32` | `-8.22` | `-11.55` | `-13.94` |
| `eps 0.25, liv 4` | `-1.85` | `-1.79` | `-1.58` | `-0.83` | -- | -- | -- | `-3.92` | `-7.67` | `-10.31` |
| `eps 0.5, liv 0` | `-1.91` | `-1.92` | `-1.93` | `-1.96` | `-2.03` | `-2.33` | `-3.25` | `-6.08` | `-7.04` | `-7.65` |
| `eps 0.5, liv 4` | `-1.89` | `-1.79` | `-1.41` | -- | -- | -- | -- | -- | `-2.50` | `-3.64` |
| `eps 1, liv 0` | `-2.14` | `-2.14` | `-2.15` | `-2.18` | `-2.24` | `-2.49` | `-3.05` | `-3.78` | `-3.88` | `-3.93` |
| `eps 1, liv 5` | `-2.12` | `-2.02` | `-1.67` | `-0.31` | -- | -- | -- | -- | -- | `-2.03` |

### 6.4 L'UNIVERSALITA' `Vi` *(simmetrica)*: ### **`E0`: `28` coppie, esponenti `-0.10`-`1.72` (mediana `1.66`), `Vi(0.99)` fino a `0.52`; `M`: `28` coppie, esponenti `-0.17`-`1.76` (mediana `1.66`), `Vi(0.99)` fino a `1.3e+02`** *(le righe intere nel `jsonl`)*.


### 6.5 LA LETTURA, IN TRE RIGHE *(nessuna conclusione oltre le tabelle)*

1. ### **CON LO ZERO SIMMETRICO TUTTE LE SPECIE MISURATE CADONO NELLO STESSO VERSO, VERSO `cs` ALTO:** ### **a `eps 0` i due rami insieme** *(`a/a_RG` `-1.84`..`-1.90` a `s0 0.3`, `-2.13`..`-2.21` a
   `0.5`, `-8.5`..`-9.3` a `0.9`)*, ### **e `eps 0.5` con loro** *(`-1.9`, `-2.2`, `-2.6`)*: ### **a `s0 0.3` e `0.5` le due specie coincidono entro pochi per cento.** ### **Oggi invece i versi sono
   OPPOSTI** *(`eps 0` alto verso `cs` alto, basso nullo, `eps 0.5` verso `cs` basso a `s0 0.9`)*. ### **Hamilton tiene in tutte e due** *(`a/a_H` `0.85`-`0.97`)*.
2. ### **MA E' UNA SPINTA, NON UN'ATTRAZIONE, E NON HA IL MODULO DELLA RELATIVITA' GENERALE:** ### **`a/a_RG ~ -2` a `s0` piccolo** *(non `+1`)*, ### **che cresce verso il cono come `Q`**; ### **e `Q`
   simmetrico e' `a_H/a_RG`** *(`-1.96`, `-2.29`, `-3.34`, `-9.86`, `-19.9` a `s 0.3`-`0.95`, `eps 0`)*: ### **con `omega(0)` proporzionale a `s` la forza E' Einstein, e Einstein non vale.**
3. ### **LO ZERO A META' DI `05055fc6` NON E' LO ZERO SIMMETRICO:** ### **differiscono di `pi` per tick** *(una costante, che non e' un potenziale: la stessa forza)*; ### **il suo `Q ~ 1` veniva da quella
   costante, e non diceva niente sulla forza.** ### **`D = 0` a `eps 0` resta in tutte e due** *(`|D| <= 2.2e-12`)*.

### **PER LA DECISIONE DI LUCA SULLA CONVENZIONE** *(informazione, non scelta)*: ### **lo zero simmetrico realizza il PRINCIPIO DI EQUIVALENZA nel VERSO** *(tutte le specie cadono insieme, a `s`
piccolo anche nel modulo)* ### **ma col SEGNO di una SPINTA verso `cs` alto e `|a/a_RG| ~ 2`, non `1`**; ### **lo zero di oggi da' versi opposti fra specie.** ### **Nessuna delle due da' la
relativita' generale** *(verso `cs` basso, `a/a_RG = 1`)* ### **per i rami lineari della camminata.**
