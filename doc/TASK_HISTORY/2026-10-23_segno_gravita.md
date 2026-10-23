# IL SEGNO DELLA GRAVITA' DEI RAMI: IL LIMITE A `s` PICCOLO, L'UNICITA' DELLO ZERO UNIVERSALE, ENERGIA CONTRO INERZIA

> **Il mandato:** di Luca, dopo `6e022419`. ### **Solo misure, in memoria: non sceglie niente.** ### **`leggi.yaml`, l'impronta `2e7f795d2a52fbe7`, la convenzione nel repo e il nucleo intatti;
> `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE; git `e96ca41a`)*. ### **Importati, non copiati:** `_zero_simmetrico` *(`convenzione_simmetrica`, `righe_rami`, `nome_curv`)*,
> `_forza_da_cs` *(`rami`, `catena_principale`, `bersaglio`, `righe_del_ramo`, `spazio_del_ramo`, `segui`, `avvolgi`, `corsa`, `nullo`, `committata`)*, `_scala_e_zero` *(`rami_a`)*,
> `_gravita_collettiva` *(`convenzione_alternativa`, `gruppi`)*. ### **Gli errori del guardiano n.48 e n.49** *(lo zero a meta' non e' il simmetrico; `Q` con `omega(0)` assoluto non e' dinamico)*
> ### **sono nel mandato: li riporto, non li rifaccio.**

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica.**
2. **Il gradino:** ### **`(a)` i controlli** *(`lambda 0` e `0.5` = `6e022419`; `eta = 0` a `s0 0.1`; i due rami diversi a `lambda 0`)*; ### **`(b)` l'unicita' di `lambda*`**; ### **`(c)` il limite a `s`
   piccolo e il segno di energia contro inerzia.**
3. **Aggiunge un numero o una legge?** ### **No.** ### **`lambda` e' una famiglia di letture in memoria**; ### **i punti `s0` e la finestra del pacchetto sono SCELTE DI MISURA, dichiarate.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` SI'** *(a mano)*; ### **IL SEGNO della forza e' la domanda.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **lo zero universale e' UNICO** *(lo fissa l'universalita')*, ### **e il segno sbagliato e' STRUTTURALE?**

## 1. LA FAMIGLIA DEGLI ZERI, SULLA CARTA *(prima dei numeri)*

- ### **`exp(i theta (I - P)) e^{-i lambda theta} = exp(i (1 - lambda) theta (I - P)) exp(-i lambda theta P)`** *(i due fattori commutano)*: ### **il pezzo di oggi a frazione `(1 - lambda) f`,
  poi il pezzo dell'ALTERNATIVA a `lambda f`** ### **-- lo stesso meccanismo di `convenzione_simmetrica()`** *(che e' `lambda = 1/2`)*; ### **a `lambda = 0` e `1` si applica un pezzo solo**
  *(una frazione nulla non e' un pezzo: `flussi_parziali._frazione_valida` la rifiuterebbe)*.
- ### **A `cs` uniforme:** ### **`omega_lambda(0) = omega(0) + 2 pi lambda s`** *(due mezzi Grover e due mezzi spostamenti per tick)*; ### **nel gradiente `2 pi lambda s(x)` e' un POTENZIALE.**
- ### **HAMILTON:** ### **`a_H/a_RG = s (omega''/v^2) (d omega(0)/ds + 2 pi lambda)`: LINEARE IN `lambda`, ESATTAMENTE.** ### **A `eps 0`, i due rami** *(stesso `Dt`, curvature opposte, `omega''
  = +- v^2/Dt`)*: ### **curvatura `-`: `-(s/Dt) 2 pi lambda`; curvatura `+`: `(s/Dt)(-2 pi + 2 pi lambda)`** ### **-> UGUALI se e solo se `lambda = 1/2`, a OGNI `s`.** ### **L'osservazione `(1)`
  del guardiano la PREVEDO VERA**, ### **col solo limite del rumore del fit fra le due copie** *(`Dt` e `v` del fit differiscono fra rami degeneri fino a `~1e-7`-`1e-6`: `lambda*` a `1e-6` puo' NON
  tenere per quello)*.
- ### **A `lambda* = 1/2`, `eps 0.5` coincide con `eps 0`?** ### **La mia previsione: NO esattamente** *(da `6e022419`: a `s0 0.3` `-1.96` contro `~ -2.0`, a `0.9` `-9.97` contro `~ -2.7`)*: ### **quasi
  a `s0` piccolo, lontano vicino al cono.**
- ### **IL LIMITE A `s` PICCOLO:** ### **`a_H/a_RG = -pi s/Dt` a `eps 0`, `lambda 1/2`**; ### **`Dt(0.3) = 0.481`, `Dt(0.5) = 0.686`** *(`6e022419`)*: ### **`-1.96`, `-2.29`.** ### **Se `Dt ~ k s`
  per `s -> 0`, il limite e' `-pi/k`, finito e NEGATIVO.** ### **Non conosco `k`: lo misuro** *(previsione debole: fra `-1.5` e `-2`)*.
- ### **ENERGIA CONTRO INERZIA** *(l'osservazione `(2)`)*: ### **zero simmetrico, `eps 0`: `E0 = +pi` col ramo a curvatura `-`, `E0 = -pi` con quello a curvatura `+`** *(`6e022419`)*: ### **`E0 M < 0`
  su tutti e due: LA PREVEDO VERA.** ### **A `eps 0.5`: non lo so.**
- ### **DOVE STA IL SALTO:** ### **a `k = 0` i due rami di `eps 0` stanno a `+- pi s`**: ### **separati di `2 pi s` passando per `0` e di `2 pi (1 - s)` passando per `pi`.** ### **E dato che
  energia e curvatura hanno segno OPPOSTO, le due bande si AVVICINANO andando verso `k != 0` passando per `0`.** ### **La mia previsione: per `s > 1/2` il salto minimo sta vicino a `pi`**
  *(il guardiano: vicino a `pi`)*; ### **per `s < 1/2` non lo so.**

## 2. IL METODO

### PARTE A -- L'UNICITA' (dagli spettri)

- ### **`lambda` in `(0, 0.25, 0.5, 0.75, 1.0)`, `s0` in `(0.3, 0.5, 0.9)`, `eps` in `(0, 0.5)`, lato `64`.** ### **Per OGNI ramo massivo** *(`gruppi` di `_forza_da_cs.rami`, nella lettura `lambda`)*:
  ### **`d omega(0)/ds` per differenza centrata a `s0 (1 +- eta)`, `eta` in `(1e-3, 1e-2)`** *(il ramo seguito con `segui`, l'`omega(0)` bersaglio spostato di `2 pi lambda s`)*, ### **`omega''
  = segno v^2/Dt`** *(il fit: le stesse formule di `557d94d6` e `6e022419`)*, ### **`a_H/a_RG = s0 (omega''/v^2) (d omega(0)/ds)`.**
- ### **I rami nominati per CURVATURA** *(`nome_curv`, come `6e022419`)*.
- ### **La linearita':** ### **fit lineare in `lambda` sui cinque punti, il residuo relativo** *(`max |res| / max |valore|`)*. ### **`lambda*`:** ### **l'intersezione delle due rette di `eps 0`.**
  ### **A `lambda*`:** ### **`eps 0.5` dalla sua retta, e lo scarto relativo da `eps 0`.**

### PARTE B -- IL LIMITE A `s` PICCOLO

- ### **Zero simmetrico** *(`convenzione_simmetrica` importata)*, ### **`s0` in `(0.05, 0.1, 0.2)`, `eps` in `(0, 0.5)`** *(a `eps 0` i due rami)*, ### **`eta` in `(0, +5e-4, +1e-3, +5e-3, +1e-2)`**
  *(`0` per il controllo, i mezzi per la linearita')*, ### **`Lx` in `(256, 512)`.**
- ### **Il pacchetto e la finestra:** ### **quelli di `_forza_da_cs.corsa`, senza cambiarli: `W = Lx/16`** *(`16` e `32` archi)*, ### **`T <= Lx/4`** *(`64` e `128` tick)*, ### **la finestra
  `|<x> - x0| < Lx/32`**, ### **almeno `6` punti, la norma fuori `<= 10%`.** ### **Il criterio semiclassico si STAMPA: `Dt/v` contro `1/W`.**
- ### **«TROPPO LENTO»** *(dichiarato)*: ### **a un `s0`, se a `eta 1e-2` su TUTTE le righe `|a| < 2 sigma_a`** *(la forza non si distingue dal rumore nella finestra)*, ### **quel `s0` si scrive
  TROPPO LENTO** ### **e, se e' `0.05`, ci si ferma a `0.1`.**
- ### **IL LIMITE:** ### **`a_H/a_RG` contro `s0` sui SEI punti `0.05, 0.1, 0.2, 0.3, 0.4, 0.5`** *(`0.4` aggiunto, dalla sola previsione di Hamilton, perche' i punti siano sei fino a `0.5`)*,
  ### **fit polinomiale di grado `2`** *(non impone una forma: la contiene)*, ### **estrapolato a `s0 = 0`** *(e accanto il grado `1`, per vedere quanto il limite dipende dal fit)*. ### **Lo stesso
  per `a_mis/a_RG` sulle righe leggibili.**

### PARTE C -- ENERGIA CONTRO INERZIA

- ### **Zero simmetrico:** ### **`_zero_simmetrico.righe_rami("simm", eps)`** *(la fase continua da `s 0.02`, `omega''` dalle fasi esatte, `v`)* ### **ai `s` `0.05, 0.1, 0.2, 0.3, 0.5, 0.9`**:
  ### **`E0`, `M`, il loro segno, e `E0 M / v_p^2 = omega omega''/v^2`** *(`v_p = v/s`: in tempo proprio)*.
- ### **IL SALTO:** ### **per ogni COPPIA di rami massivi allo stesso `(s, eps)`** *(lato `64`, le fasi di `rami_seguiti` lungo `(m, 0)`, zero simmetrico)*: ### **la distanza `|avvolgi(phi_a(k) -
  phi_b(k))|`, il suo MINIMO lungo `k`, il `k` del minimo, e la fase per tick del punto medio** *(`phi_a + avvolgi(phi_b - phi_a)/2`)*: ### **«vicino a `0`» se `|fase| < pi/2`, «vicino a `pi`»
  se no.**

## 3. I CRITERI, FISSATI ORA *(dal mandato)*

- ### **DEVE PASSARE:** ### **a `lambda 0` e `0.5`, `a_H/a_RG` della parte `A` = `6e022419` entro `1e-9`** *(il `H_su_RG` del suo `jsonl`, stesse `(eps, s0, ramo, eta)`)*.
- ### **DEVE PASSARE:** ### **`eta = 0` a `s0 0.1`: `|a|` sotto il rumore del fit** *(`_forza_da_cs.nullo`: `|a| <= 2 sigma_a` o `< 1e-12`)*.
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«a `lambda 0` i due rami di `eps 0` hanno lo stesso `a_H/a_RG`»** *(entro `1e-6` relativo; i valori finiti e stampati)*.
- ### **PUO' FALLIRE:** ### **la linearita' in `lambda`, residuo relativo `< 1e-6`.**
- ### **PUO' FALLIRE:** ### **`|lambda* - 1/2| < 1e-6` a ogni `s0`.**
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE:** ### **le tabelle e il limite.** ### **A parte: la lettura in tre righe e una riga su «da dove viene la massa»** *(ritardo, moneta, legame)*:
  ### **informazione, non scelta.**

## 4. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_segno_gravita.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima dei numeri;
3. la corsa, il referto `doc/referti_l2/segno_gravita.txt` e `.jsonl`, la relazione, e la sezione `5` qui sotto.

## 5. I RISULTATI *(scritti dopo la corsa, sotto)*
