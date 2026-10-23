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

## 3-bis. LA VERSIONE NUOVA DEL MANDATO *(arrivata dopo questo task history; vale l'ultima, [[PRECEDENZA-IN-CODA]])*: ### **LA PARTE `D`, IL SOLITONE IN UN GRADIENTE, e i controlli nuovi**

### **Le parti `A`, `B`, `C` restano come sopra.** ### **Una cosa vista nella prova a vuoto in memoria delle funzioni `A`-`C`** *(nessun file del repo scritto)*: ### **a `eps 0.5, s0 0.05` lo spazio del
ramo principale NON e' definito** *(rango `1` per `2` copie: l'asserzione di `spazio_del_ramo`)*: ### **si scrive «RAMO NON DEFINITO» e non si misura** *(come in `27df8e79`)*. ### **E a `s0` piccolo
i nomi «basso/alto» di `righe_del_ramo` si SCAMBIANO** *(a `s0 0.05`-`0.5` il «basso» ha curvatura `+`)*: ### **per questo i rami si nominano per CURVATURA.** ### **La prova a vuoto ha stampato
anche dei numeri di `A`: li dichiaro** *(a `s0 0.3`: `lambda* = 0.500000026`, residuo `1.4e-13`)* ### **e non tocco le previsioni.**

### PARTE D -- IL METODO

- ### **LA SCENA:** ### **la camminata INTERA col legame acceso** *(il passo coi `14` pezzi, `salta = ()`; la forma `S1`, `S3`, `S4` con `_screening_forme_s3.forma`)*, ### **`eps 0`, il ramo a curvatura
  NEGATIVA, `s0` in `(0.3, 0.5)`, le DUE convenzioni.** ### **Il toro `Lx x Ly = 128 x 64`** *(il solitone e' RADIALE in `2d`: il toro `Lx x 4` di `_forza_da_cs` non lo contiene; `Ly = 64` e' piu'
  di otto volte la larghezza minima)*, ### **il vuoto `phi = VUOTO`** *(`Lambda0 = 4` per nodo: senza vuoto il legame non c'e')*, ### **`dtau = 1`, `mot.cs` il profilo, `lambda_c = None`.**
- ### **LO STATO INIZIALE:** ### **il profilo radiale `u(r)` del solitone di `_gravita_collettiva.solitone`** *(con `c = c_di` del ramo a `s0`)*, ### **la densita' per nodo `u(r)^2` sul vettore del ramo
  a `k = 0`** *(`spazio_del_ramo`)*, ### **centrato a `(Lx/4, Ly/2)`, fermo**, ### **la norma riportata a `N`.** ### ⚠ **`solitone()` oggi NON RESTITUISCE il profilo**: ### **lo strumento lo
  chiede a una funzione `_profilo` estratta da `solitone()` in un commit a se'** *(il comportamento di `solitone()` resta lo stesso, verificato al bit)*.
- ### **LE NORME** *(dichiarate)*: ### **sulla griglia `N` in `(1, 3, 10, 30, 100, 300, 1000, 3000, 10000)`** ### **le DUE piu' piccole con lo stato LEGATO e larghezza `>= 4` archi a TUTTI E DUE gli
  `s0`.** ### **Se per una forma non ce ne sono: si scrive, e quella forma non si corre.**
- ### **LA TENUTA** *(prima del gradiente)*: ### **`eta = 0`, per tutto il tempo della misura** *(`T = Lx/4 = 32` tick)*: ### **la larghezza** *(rms attorno al baricentro, immagine minima sul toro)* ### **entro
  il `10%` della iniziale a ogni tick**, ### **e il baricentro fermo** *(`|a| <= 2 sigma_a`)*. ### **Se non tiene: «NON TIENE» col tick in cui la larghezza esce, e quel punto non si misura.**
- ### **LA FORZA:** ### **`eta` in `(1e-3, -1e-3, 1e-2, -1e-2)`**, ### **il baricentro circolare in `x` del modulo quadro della materia, il fit `x0 + v0 t + a t^2/2` sulla finestra di
  `_forza_da_cs`** *(`|<x> - x0| < Lx/32`, `T <= Lx/4`, almeno `6` punti)*, ### **`a_RG = -v^2 (ds/dx)/s0`** *(`v` del ramo)*, ### **`a_mis/a_RG`, il verso, e il confronto fra le due norme.**
- ### **LA SCOMPOSIZIONE:** ### **`E_ramo = omega0/s0`** *(oggi `0`, simmetrica `+pi` sul ramo a curvatura `-`)* ### **e `E_legame = mu/s0`** *(`mu` di `solitone()`)*: ### **quale domina in modulo.**

### PARTE D -- LE PREVISIONI *(prima dei numeri)*

- ### **HAMILTON PER UN SOLITONE FERMO** *(la stessa formula dei rami, con `omega_sol = omega0 + mu(s)`)*: ### **`a/a_RG = s (omega''/v^2) d omega_sol/ds`**, ### **e col `c` proporzionale a `s`** *(`mu = s mu_1`,
  `05055fc6`)*: ### **`d omega_sol/ds = d omega0/ds + mu/s`.**
- ### **ZERO SIMMETRICO** *(`d omega0/ds = pi`, `omega'' < 0`)*: ### **`a/a_RG = -(s/Dt)(pi + mu/s)`**: ### **verso `cs` BASSO solo se `-mu/s > pi`** *(il legame domina sull'energia del ramo)*.
  ### **Per solitoni larghi `>= 4` archi la densita' e' bassa e `|mu|` piccolo: PREVEDO verso `cs` ALTO per tutte le forme** ### **-- il guardiano: `S3` e `S4` verso `cs` basso SE il legame domina.**
- ### **CONVENZIONE DI OGGI** *(`d omega0/ds = 0` sul ramo a curvatura `-`)*: ### **`a/a_RG = -mu/Dt`**: ### **`S3` e `S4`** *(`mu < 0`)* ### **verso `cs` BASSO, `S1`** *(`mu > 0`)* ### **verso `cs`
  ALTO**; ### **e il modulo dipende da `N`** *(attraverso `mu`)*: ### **due solitoni della stessa forma NON accelerano uguale.** ### **Nessuna delle due convenzioni da' `a/a_RG = 1` a ogni `N`.**
- ### ⚠ **E I LIMITI della previsione:** ### **`c(s)` misurato non e' proporzionale a `s`** *(la parte di moto di `c4efc937`)*; ### **il vuoto reagisce** *(`beta` non uniforme lo fa camminare)*;
  ### **il solitone puo' non tenere sul reticolo.**

### I CONTROLLI NUOVI *(fissati ora, dal mandato)*

- ### **DEVE PASSARE:** ### **parte `D` a `cs` uniforme: `|a|` sotto il rumore del fit** *(la tenuta)*.
- ### **DEVE PASSARE:** ### **parte `D`, il profilo specchiato** *(`eta -> -eta`)*: ### **`a` cambia segno, `|a|` uguale entro il `5%`.**
- ### **PUO' FALLIRE:** ### **parte `D`, almeno un solitone `S3` o `S4` con lo zero simmetrico e `a_mis/a_RG > 0`.** ### **La mia previsione: FALLISCE.**
- ### **Se la parte `D` e' lunga, il suo referto si committa a parte.**

### 📝 **ANNOTAZIONE 1** *(prima della corsa dello strumento committato, nel commit dello strumento)*:
- ### **LA PARTE `D` SI FERMA ALLA SCELTA DELLE NORME, e lo dico prima:** ### **la prova a vuoto in memoria** *(`solitone()` sulla griglia `N`, `s0 0.3` e `0.5`)* ### **non trova NESSUNA forma con
  uno stato legato largo `>= 4` archi**: ### **sul ramo a curvatura `-` `sigma = sqrt(|c|/s)` vale `0.46` e `0.50` archi** *(`c = -0.064` e `-0.125`)*, ### **e gli stati legati sono larghi `0.5`-`1.2`
  archi.** ### ⚠ **E UN LIMITE DEL RISOLUTORE, dichiarato:** ### **la sua scatola e' `12 sigma` = `5.5`-`6.0` archi e la «dispersione» scatta oltre `R/5 = 1.1`-`1.2` archi**: ### **uno stato largo
  `>= 4` archi QUESTO strumento non lo puo' dire legato.** ### **Allargare la scatola porta la coda sotto il doppio** *(`d222af13`, annotazione `1` di `gravita_collettiva`)*: ### **non lo faccio
  qui.** ### **Quindi: i controlli della parte `D` NON SONO ESEGUIBILI e non si contano**, ### **e l'estrazione del profilo da `solitone()`** *(sez. `3-bis`)* ### **NON SERVE e non si fa.**
- ### **La prova a vuoto delle parti `A`-`C`** *(griglia ridotta)* ### **ha stampato dei numeri: li dichiaro** *(`a_H/a_RG -1.84` a `s0 0.05`, `E0 M < 0` su tutti i rami visti, il salto a `k = pi` vicino a `0` a
  `s 0.1` e a `k = 0` vicino a `pi` a `s 0.9`; il controllo `eta = 0` a `s0 0.1` vi fallisce)* ### **e non tocco ne' le previsioni ne' i criteri.**

## 4. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_segno_gravita.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati prima dei numeri;
3. la corsa, il referto `doc/referti_l2/segno_gravita.txt` e `.jsonl`, la relazione, e la sezione `5` qui sotto.

## 5. I RISULTATI *(scritti dopo la corsa, sotto)*

### **LA CORSA:** `python csv/_segno_gravita.py`, strumento sha1-BYTE `2a763b39` *(`8aaad8f3`, committato e pulito)*. ### **`4` controlli su `5`** *(quelli della parte `D` NON eseguibili, non contati)*.

- ### **DEVE PASSARE, `lambda 0` e `0.5` = `6e022419`: PASSA** *(`3.3e-16`, `36` valori)*.
- ### **DEVE FALLIRE, i due rami uguali a `lambda 0`: FALLISCE per la chiave giusta** *(`-3.92`/`0` a `s0 0.3`, `-4.58`/`0` a `0.5`, `0`/`-19.9` a `0.9`)*.
- ### **PUO' FALLIRE, la linearita' `< 1e-6`: PASSA** *(`1.4e-13`)*. ### **PUO' FALLIRE, `lambda* = 1/2` entro `1e-6`: PASSA** *(il peggiore `2.6e-8`)*: ### **L'OSSERVAZIONE `(1)` DEL GUARDIANO E'
  CONFERMATA** *(come previsto sulla carta: `lambda* = 1/2` e' un'identita' per i due rami di `eps 0`)*.
- ### ⚠ **DEVE PASSARE, `eta = 0` a `s0 0.1`: FALLISCE** ### **-- sulle righe di `eps 0.5`** *(`a = 2.2e-7` contro `sigma 1.2e-8` a `Lx 256`; `5.1e-8` contro `7.8e-10` a `512`)*: ### **a `s0 0.1` la
  catena principale di `eps 0.5` prende un ramo a curvatura `+`** *(`Dt 0.2233`)* ### **e il pacchetto DERIVA anche senza gradiente**; ### **le righe di `eps 0` passano.** ### **Il criterio non cambia.**
- ### **TROPPO LENTO: no** *(a `eta 1e-2`, `|a|/sigma` `13`-`47` a `s0 0.05`, fino a `219` a `0.2`)*: ### **`s0 0.05` si misura.**
- ### **LA PARTE `D` SI FERMA ALLA SCELTA DELLE NORME** *(nessun solitone legato largo `>= 4` archi, per nessuna forma: annotazione `1`)*.

### 5.1 PARTE A: `a_H/a_RG` NELLA FAMIGLIA `lambda` *(`eta 1e-3`)*

| `eps` | `s0` | ramo | `lambda 0` | `0.25` | `0.5` | `0.75` | `1` | pendenza | residuo |
|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.3` | curv + Dt 0.4807 | `-3.9212` | `-2.9409` | `-1.9606` | `-0.9803` | `+0.0000` | `+3.9212` | `1.4e-13` |
| `0` | `0.3` | curv - Dt 0.4807 | `-0.0000` | `-0.9803` | `-1.9606` | `-2.9409` | `-3.9212` | `-3.9212` | `9.4e-14` |
| `0` | `0.5` | curv + Dt 0.6858 | `-4.5810` | `-3.4358` | `-2.2905` | `-1.1453` | `+0.0000` | `+4.5810` | `9.2e-14` |
| `0` | `0.5` | curv - Dt 0.6858 | `-0.0000` | `-1.1453` | `-2.2905` | `-3.4358` | `-4.5810` | `-4.5810` | `9.2e-14` |
| `0` | `0.9` | curv - Dt 0.2836 | `-0.0000` | `-4.9845` | `-9.9690` | `-14.9535` | `-19.9380` | `-19.9380` | `8.2e-14` |
| `0` | `0.9` | curv + Dt 0.2836 | `-19.9380` | `-14.9535` | `-9.9690` | `-4.9845` | `+0.0000` | `+19.9380` | `6.3e-14` |
| `0.5` | `0.3` | curv - Dt 0.4684 | `-0.0003` | `-1.0065` | `-2.0127` | `-3.0188` | `-4.0250` | `-4.0246` | `2.2e-16` |
| `0.5` | `0.5` | curv - Dt 0.6718 | `+0.0727` | `-1.0963` | `-2.2654` | `-3.4344` | `-4.6034` | `-4.6761` | `1.0e-13` |
| `0.5` | `0.9` | curv - Dt 0.4253 | `+3.9128` | `+0.5891` | `-2.7345` | `-6.0582` | `-9.3818` | `-13.2946` | `5.6e-14` |
| `0.5` | `0.9` | curv + Dt 0.0132 | `-420.6702` | `-313.3617` | `-206.0532` | `-98.7447` | `+8.5638` | `+429.2339` | `8.8e-14` |

### 5.2 `lambda*` E `eps 0.5` A `lambda*`

| `s0` | `eta` | `lambda*` | `|lambda* - 1/2|` | `a_H/a_RG` di `eps 0` | `eps 0.5` *(scarto relativo)* |
|---|---|---|---|---|---|
| `0.3` | `0.001` | `0.500000026` | `2.6e-08` | `-1.9606` | curv - Dt 0.4684 `-2.0127` (`0.027`) |
| `0.3` | `0.01` | `0.500000026` | `2.6e-08` | `-1.9606` | curv - Dt 0.4684 `-2.0127` (`0.027`) |
| `0.5` | `0.001` | `0.500000006` | `5.5e-09` | `-2.2905` | curv - Dt 0.6718 `-2.2654` (`0.011`) |
| `0.5` | `0.01` | `0.500000006` | `5.5e-09` | `-2.2905` | curv - Dt 0.6718 `-2.2653` (`0.011`) |
| `0.9` | `0.001` | `0.500000000` | `1.1e-11` | `-9.9690` | curv - Dt 0.4253 `-2.7345` (`0.726`); curv + Dt 0.0132 `-206.0532` (`19.669`) |
| `0.9` | `0.01` | `0.500000000` | `1.1e-11` | `-9.9690` | curv - Dt 0.4253 `-2.7317` (`0.726`); curv + Dt 0.0132 `-206.0519` (`19.669`) |

### 5.3 PARTE B: LA FORZA A `s0` PICCOLO *(zero simmetrico)*

| `eps` | `s0` | ramo | `Lx` | `eta` | `a_mis/a_RG` | `a_mis/a_H` | `a_H/a_RG` | `|a|/sigma` | lin | si legge |
|---|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.05` | curv + Dt 0.0852 | `256` | `0.001` | `-2.512` | `+1.363` | `-1.8433` | `6.3` | `1.570` | **no** |
| `0` | `0.05` | curv + Dt 0.0852 | `256` | `0.01` | `-1.893` | `+1.027` | `-1.8433` | `16.3` | `1.929` | si' |
| `0` | `0.05` | curv + Dt 0.0852 | `512` | `0.001` | `-1.853` | `+1.005` | `-1.8433` | `36.0` | `1.980` | si' |
| `0` | `0.05` | curv + Dt 0.0852 | `512` | `0.01` | `-1.835` | `+0.996` | `-1.8433` | `47.2` | `1.998` | si' |
| `0` | `0.05` | curv - Dt 0.0852 | `256` | `0.001` | `-1.966` | `+1.066` | `-1.8433` | `2.3` | `1.989` | si' |
| `0` | `0.05` | curv - Dt 0.0852 | `256` | `0.01` | `-1.956` | `+1.061` | `-1.8433` | `12.9` | `1.999` | si' |
| `0` | `0.05` | curv - Dt 0.0852 | `512` | `0.001` | `-1.663` | `+0.902` | `-1.8433` | `17.1` | `2.254` | **no** |
| `0` | `0.05` | curv - Dt 0.0852 | `512` | `0.01` | `-1.831` | `+0.994` | `-1.8433` | `30.5` | `2.020` | si' |
| `0` | `0.1` | curv + Dt 0.1696 | `256` | `0.001` | `-1.879` | `+1.015` | `-1.8521` | `17.4` | `1.961` | si' |
| `0` | `0.1` | curv + Dt 0.1696 | `256` | `0.01` | `-1.845` | `+0.996` | `-1.8521` | `34.2` | `1.996` | si' |
| `0` | `0.1` | curv + Dt 0.1696 | `512` | `0.001` | `-1.774` | `+0.958` | `-1.8521` | `84.3` | `2.002` | si' |
| `0` | `0.1` | curv + Dt 0.1696 | `512` | `0.01` | `-1.776` | `+0.959` | `-1.8521` | `93.4` | `2.000` | si' |
| `0` | `0.1` | curv - Dt 0.1696 | `256` | `0.001` | `-1.484` | `+0.801` | `-1.8521` | `6.4` | `2.695` | **no** |
| `0` | `0.1` | curv - Dt 0.1696 | `256` | `0.01` | `-1.827` | `+0.987` | `-1.8521` | `21.3` | `2.042` | si' |
| `0` | `0.1` | curv - Dt 0.1696 | `512` | `0.001` | `-1.796` | `+0.970` | `-1.8521` | `53.3` | `2.009` | si' |
| `0` | `0.1` | curv - Dt 0.1696 | `512` | `0.01` | `-1.804` | `+0.974` | `-1.8521` | `65.6` | `2.001` | si' |
| `0` | `0.2` | curv + Dt 0.3326 | `256` | `0.001` | `-1.809` | `+0.957` | `-1.8894` | `54.6` | `1.999` | si' |
| `0` | `0.2` | curv + Dt 0.3326 | `256` | `0.01` | `-1.808` | `+0.957` | `-1.8894` | `73.4` | `2.000` | si' |
| `0` | `0.2` | curv + Dt 0.3326 | `512` | `0.001` | `-1.822` | `+0.964` | `-1.8894` | `203.5` | `2.000` | si' |
| `0` | `0.2` | curv + Dt 0.3326 | `512` | `0.01` | `-1.822` | `+0.964` | `-1.8894` | `219.0` | `2.000` | si' |
| `0` | `0.2` | curv - Dt 0.3326 | `256` | `0.001` | `-1.818` | `+0.962` | `-1.8894` | `28.0` | `2.022` | si' |
| `0` | `0.2` | curv - Dt 0.3326 | `256` | `0.01` | `-1.836` | `+0.972` | `-1.8894` | `49.4` | `2.002` | si' |
| `0` | `0.2` | curv - Dt 0.3326 | `512` | `0.001` | `-1.818` | `+0.962` | `-1.8894` | `132.3` | `1.999` | si' |
| `0` | `0.2` | curv - Dt 0.3326 | `512` | `0.01` | `-1.817` | `+0.962` | `-1.8894` | `144.0` | `2.000` | si' |
| `0.5` | `0.1` | curv + Dt 0.2233 | `256` | `0.001` | `+0.385` | `-0.270` | `-1.4231` | `8.2` | `0.540` | **no** |
| `0.5` | `0.1` | curv + Dt 0.2233 | `256` | `0.01` | `-0.551` | `+0.387` | `-1.4231` | `32.4` | `2.463` | **no** |
| `0.5` | `0.1` | curv + Dt 0.2233 | `512` | `0.001` | `-0.164` | `+0.115` | `-1.4231` | `47.4` | `-1.027` | **no** |
| `0.5` | `0.1` | curv + Dt 0.2233 | `512` | `0.01` | `-0.599` | `+0.421` | `-1.4231` | `91.4` | `2.174` | **no** |
| `0.5` | `0.2` | curv - Dt 0.3237 | `256` | `0.001` | `-1.861` | `+0.952` | `-1.9557` | `27.0` | `2.047` | si' |
| `0.5` | `0.2` | curv - Dt 0.3237 | `256` | `0.01` | `-1.899` | `+0.971` | `-1.9557` | `47.6` | `2.004` | si' |
| `0.5` | `0.2` | curv - Dt 0.3237 | `512` | `0.001` | `-1.888` | `+0.966` | `-1.9557` | `123.0` | `1.997` | si' |
| `0.5` | `0.2` | curv - Dt 0.3237 | `512` | `0.01` | `-1.886` | `+0.964` | `-1.9557` | `133.1` | `2.000` | si' |

### **RAMO NON DEFINITO:** `eps 0.5`, `s0 0.05`, curv + Dt 0.0887 *(lo spazio del ramo ha rango 1, le copie sono 2 (valori singolari [1.31103717 0.49265251]))*.

### 5.4 IL LIMITE `s0 -> 0`

| `eps` | curvatura | `a_H/a_RG` ai sei `s0` | limite grado `2` | limite grado `1` | `a_mis/a_RG` grado `2` *(punti)* |
|---|---|---|---|---|---|
| `0` | `+` | `0.05`:`-1.8433` `0.1`:`-1.8521` `0.2`:`-1.8894` `0.3`:`-1.9606` `0.4`:`-2.0829` `0.5`:`-2.2905` | `-1.8671` | `-1.7439` | `-2.6811` *(`11`)* |
| `0` | `-` | `0.05`:`-1.8433` `0.1`:`-1.8521` `0.2`:`-1.8894` `0.3`:`-1.9606` `0.4`:`-2.0829` `0.5`:`-2.2905` | `-1.8671` | `-1.7439` | `-2.6019` *(`11`)* |
| `0.5` | `-` | `0.2`:`-1.9557` `0.3`:`-2.0127` `0.4`:`-2.1087` `0.5`:`-2.2654` | `-2.0010` | `-1.7269` | `-1.6808` *(`8`)* |

### 5.5 PARTE C: ENERGIA CONTRO INERZIA *(zero simmetrico, lato `64`)* e IL SALTO

| `eps` | `s` | ramo | `E0` | `M` | segno di `E0 M` | `E0 M/v_p^2` |
|---|---|---|---|---|---|---|
| `0` | `0.05` | curv + Dt 0.0852 | `-3.1416` | `+0.3935` | **negativo** | `-1.8415` |
| `0` | `0.05` | curv - Dt 0.0852 | `+3.1416` | `-0.3935` | **negativo** | `-1.8415` |
| `0` | `0.1` | curv + Dt 0.1696 | `-3.1416` | `+0.3960` | **negativo** | `-1.8502` |
| `0` | `0.1` | curv - Dt 0.1696 | `+3.1416` | `-0.3960` | **negativo** | `-1.8502` |
| `0` | `0.2` | curv + Dt 0.3326 | `-3.1416` | `+0.4061` | **negativo** | `-1.8874` |
| `0` | `0.2` | curv - Dt 0.3326 | `+3.1416` | `-0.4061` | **negativo** | `-1.8874` |
| `0` | `0.3` | curv + Dt 0.4807 | `-3.1416` | `+0.4246` | **negativo** | `-1.9584` |
| `0` | `0.3` | curv - Dt 0.4807 | `+3.1416` | `-0.4246` | **negativo** | `-1.9584` |
| `0` | `0.5` | curv + Dt 0.6858 | `-3.1416` | `+0.5000` | **negativo** | `-2.2873` |
| `0` | `0.5` | curv - Dt 0.6858 | `+3.1416` | `-0.5000` | **negativo** | `-2.2873` |
| `0` | `0.9` | curv + Dt 0.2836 | `-3.1416` | `+1.7520` | **negativo** | `-9.8614` |
| `0` | `0.9` | curv - Dt 0.2836 | `+3.1416` | `-1.7520` | **negativo** | `-9.8614` |
| `0.5` | `0.05` | curv + Dt 0.0887 | `-3.1808` | `+0.3862` | **negativo** | `-1.7864` |
| `0.5` | `0.05` | curv - Dt 0.0829 | `+3.1808` | `-0.3886` | **negativo** | `-1.9171` |
| `0.5` | `0.1` | curv + Dt 0.2233 | `-3.1798` | `+0.3814` | **negativo** | `-1.4097` |
| `0.5` | `0.1` | curv - Dt 0.1650 | `+3.1798` | `-0.3909` | **negativo** | `-1.9253` |
| `0.5` | `0.2` | curv - Dt 0.3237 | `+3.1758` | `-0.4006` | **negativo** | `-1.9604` |
| `0.5` | `0.3` | curv - Dt 0.4684 | `+3.1687` | `-0.4181` | **negativo** | `-2.0274` |
| `0.5` | `0.5` | curv - Dt 0.6718 | `+3.1416` | `-0.4877` | **negativo** | `-2.3348` |
| `0.5` | `0.9` | curv + Dt 0.0132 | `-3.1591` | `+0.4390` | **negativo** | `-147.0201` |
| `0.5` | `0.9` | curv - Dt 0.4253 | `+2.8878` | `-1.0516` | **negativo** | `-6.0804` |

| `eps` | `s` | coppia | `k` del minimo | distanza | fase del punto medio | vicino a |
|---|---|---|---|---|---|---|
| `0` | `0.05` | curv + Dt 0.0852 / curv - Dt 0.0852 | `1.000 pi` | `0.22203` | `+0.00000` | `0` |
| `0` | `0.1` | curv + Dt 0.1696 / curv - Dt 0.1696 | `1.000 pi` | `0.44337` | `+0.00000` | `0` |
| `0` | `0.2` | curv + Dt 0.3326 / curv - Dt 0.3326 | `1.000 pi` | `0.88114` | `+0.00000` | `0` |
| `0` | `0.3` | curv + Dt 0.4807 / curv - Dt 0.4807 | `1.000 pi` | `1.30722` | `+0.00000` | `0` |
| `0` | `0.5` | curv + Dt 0.6858 / curv - Dt 0.6858 | `1.000 pi` | `2.09440` | `+0.00000` | `0` |
| `0` | `0.9` | curv + Dt 0.2836 / curv - Dt 0.2836 | `0.000 pi` | `0.62832` | `-3.14159` | `pi` |
| `0.5` | `0.05` | curv + Dt 0.0887 / curv - Dt 0.0829 | `1.000 pi` | `0.22758` | `-0.00001` | `0` |
| `0.5` | `0.1` | curv + Dt 0.2233 / curv - Dt 0.1650 | `1.000 pi` | `0.45445` | `-0.00009` | `0` |
| `0.5` | `0.9` | curv + Dt 0.0132 / curv - Dt 0.4253 | `0.000 pi` | `0.84100` | `+3.01950` | `pi` |

### 5.6 PARTE D: LA SCELTA DELLE NORME *(larghezza `>= 4` archi, legato, a `s0 0.3` e `0.5`)*

- `s0 0.3`: `c -0.06376`, `sigma 0.461` archi, la scatola `R = 5.53` archi *(la dispersione oltre `1.11`)*.
- `s0 0.5`: `c -0.12517`, `sigma 0.500` archi, la scatola `R = 6.00` archi *(la dispersione oltre `1.20`)*.

| forma | `N` | `s0 0.3`: esiste, larghezza | `s0 0.5`: esiste, larghezza |
|---|---|---|---|
| S1 | `1` | DISPERSIONE `2.58` | DISPERSIONE `2.80` |
| S1 | `3` | DISPERSIONE `2.58` | DISPERSIONE `2.80` |
| S1 | `10` | DISPERSIONE `2.55` | DISPERSIONE `2.78` |
| S1 | `30` | LEGATO `0.95` | LEGATO `1.09` |
| S1 | `100` | LEGATO `0.96` | LEGATO `1.02` |
| S1 | `300` | DISPERSIONE `1.13` | LEGATO `1.19` |
| S1 | `1000` | DISPERSIONE `1.44` | DISPERSIONE `1.51` |
| S1 | `3000` | DISPERSIONE `1.84` | DISPERSIONE `1.93` |
| S1 | `10000` | DISPERSIONE `2.37` | DISPERSIONE `2.50` |
| S3 | `1` | LEGATO `0.50` | LEGATO `0.53` |
| S3 | `3` | LEGATO `0.54` | LEGATO `0.58` |
| S3 | `10` | LEGATO `0.63` | LEGATO `0.66` |
| S3 | `30` | LEGATO `0.75` | LEGATO `0.79` |
| S3 | `100` | LEGATO `0.95` | LEGATO `0.99` |
| S3 | `300` | DISPERSIONE `1.20` | DISPERSIONE `1.25` |
| S3 | `1000` | DISPERSIONE `1.57` | DISPERSIONE `1.64` |
| S3 | `3000` | DISPERSIONE `2.02` | DISPERSIONE `2.11` |
| S3 | `10000` | DISPERSIONE `2.50` | DISPERSIONE `2.68` |
| S4 | `1` | LEGATO `0.88` | LEGATO `1.04` |
| S4 | `3` | LEGATO `0.59` | LEGATO `0.67` |
| S4 | `10` | LEGATO `0.51` | LEGATO `0.55` |
| S4 | `30` | LEGATO `0.50` | LEGATO `0.54` |
| S4 | `100` | LEGATO `0.54` | LEGATO `0.58` |
| S4 | `300` | LEGATO `0.60` | LEGATO `0.64` |
| S4 | `1000` | LEGATO `0.70` | LEGATO `0.74` |
| S4 | `3000` | LEGATO `0.82` | LEGATO `0.87` |
| S4 | `10000` | LEGATO `1.00` | LEGATO `1.05` |

### 5.7 LA LETTURA, IN TRE RIGHE *(nessuna conclusione oltre le tabelle)*

1. ### **LO ZERO UNIVERSALE E' UNICO:** ### **nella famiglia `lambda` `a_H/a_RG` e' lineare** *(`1.4e-13`)* ### **e i due rami di `eps 0` coincidono SOLO a `lambda* = 1/2`** *(`2.6e-8`)*; ### **a
   quel `lambda` anche `eps 0.5` coincide quasi a `s0` piccolo** *(scarto `2.7%` a `0.3`, `1.1%` a `0.5`; `73%` a `0.9`)*. ### **Lo zero simmetrico E' quello fissato dall'universalita'.**
2. ### **E CON QUELLO ZERO IL SEGNO E' SBAGLIATO A OGNI `s`, ANCHE NEL LIMITE:** ### **`a_H/a_RG -> -1.84`..`-1.87`** *(grado `2` e `1`: `-1.87`, `-1.74` a `eps 0`; `-2.00`, `-1.73` a `eps 0.5`)*,
   ### **misurata `-1.78`..`-1.97` su `25` righe leggibili, `a_mis/a_H` `0.95`-`1.07`**: ### **verso `cs` ALTO, con modulo `~ 1.85`, non `1`.** ### **`E0 M < 0` su TUTTI i rami** *(`21` righe)*:
   ### **energia e inerzia di segno opposto** *(l'osservazione `(2)` confermata nel segno)*.
3. ### **IL SALTO NON STA VICINO A `pi` A `s` PICCOLO:** ### **fra i due rami di `eps 0` il minimo e' a `k = pi`, fase `~ 0`, per `s <= 0.5`**, ### **e a `k = 0`, fase `~ pi`, solo a `s 0.9`**:
   ### **l'osservazione `(2)` sul salto vale vicino al cono, non a `s` piccolo.** ### **I solitoni** *(parte `D`)* ### **non si sono potuti misurare: sul ramo a curvatura `-` gli stati legati sono
   larghi `0.5`-`1.2` archi** *(`sigma = 0.46`-`0.50`)*.

### **PER «DA DOVE VIENE LA MASSA»** *(ritardo, moneta, legame; informazione)*: ### **a `eps 0` la massa dei rami e' TUTTA ritardo** *(il generatore a `theta = pi s < pi`)*, ### **e
con lo zero universale cade con `a/a_RG -> -1.85`: il RITARDO da' una spinta, non un'attrazione**; ### **la moneta** *(`eps 0.5`)* ### **a `s` piccolo cade come il ritardo** *(lo stesso segno, entro
pochi per cento)*; ### **il LEGAME resta la sola strada non misurata per il verso** *(la parte `D`)*, ### **e lo strumento per solitoni larghi non c'e' ancora.**

### **PER LA SCELTA FRA `S1` E `S4`** *(informazione)*: ### **nessuna delle tre forme da' un solitone legato largo `>= 4` archi sul ramo a curvatura `-` a `s0 0.3`-`0.5`** *(`S4` lega a ogni `N`
ma largo `0.5`-`1.05` archi; `S1` lega solo a `N 30`-`300`, largo `~1`)*: ### **su questa domanda le forme non si distinguono ancora.**
