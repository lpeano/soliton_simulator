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
