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
