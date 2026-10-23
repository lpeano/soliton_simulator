> ### ⛔ **GRIGLIA QUADRATA -- risultato da rifare sui triangoli (DECISIONE-SOLO-TRIANGOLI)**

# I MODI A `k = pi` E I SOLITONI LARGHI: DOVE STA LA FISICA A BASSA ENERGIA, E SE UN SOLITONE CADE NEL VERSO GIUSTO

> **Il mandato:** di Luca, dopo `e31366ec`. ### **Solo misure, in memoria; zero simmetrico** *(`lambda = 1/2`)* ### **dove non detto altro.** ### **`leggi.yaml`, l'impronta `2e7f795d2a52fbe7`,
> la convenzione nel repo e il nucleo intatti; `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE; git `e96ca41a`)*. ### **Importati, non copiati:** `_segno_gravita` *(`convenzione_lambda`,
> `h_su_rg`, `righe_ramo`)*, `_zero_simmetrico` *(`convenzione_simmetrica`, `nome_curv`)*, `_forza_da_cs` *(`rami`, `spazio_proprio`, `corsa`, `nullo`, `avvolgi`, `committata`, e la `PORTANTE`
> nuova)*, `_gravita_collettiva` *(`gruppi`, `c_di`, `profilo`, `gausson`)*, `_scala_e_zero` *(`cammino`, `blocchi` avvolti)*, `_massa_vicino_al_cono` *(`matrice`, `rami_seguiti`)*,
> `_moneta_massa.fit_massa`. ### **Gli errori del guardiano n.51 e n.52 sono nel mandato.** ### **Gia' fatto, in commit a se':** ### **la correzione del ramo di `eps 0.5` a `s0 0.1`**
> *(`bfecefd0`, la prova `6c36b19a`)*; ### **`profilo()` separata da `solitone()`** *(`9d278e7e`, uguale al bit)*.

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica.**
2. **Il gradino:** ### **`(a)` i controlli; `(b)` dove sta il salto minimo e che cosa fanno i modi a `k = pi`; `(c)` i solitoni larghi e** *(in un commit a se')* ### **la loro caduta.**
3. **Aggiunge un numero o una legge?** ### **No.** ### **Le griglie in `s` e in `N`, le scatole e i tempi sono SCELTE DI MISURA, dichiarate.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` SI'** *(a mano)*; ### **il SEGNO della forza e' la domanda.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **la fisica a bassa energia sta a `k = pi`?** ### **un solitone cade verso `cs` basso?**

## 1. COSA HANNO MOSTRATO LE ESPLORAZIONI IN MEMORIA *(nessun file del repo scritto; i numeri li ristampa lo strumento)*

- ### ⭐ **A `eps 0` I DUE RAMI DELLA COPPIA SI TOCCANO A `(pi, pi)`** *(distanza `0`, fase `0`, a `s 0.3` e `0.9`)*: ### **a `(pi, pi)` la banda e' SENZA MASSA** *(un punto di Dirac: le
  «copie» del reticolo)*; ### **lungo `x` il minimo e' a `(pi, 0)`** *(distanza `1.307` a `s 0.3`, le fasi `+-0.654`)*. ### **A `eps 0.5, s 0.3` c'e' un solo gruppo massivo** *(niente coppia)*;
  ### **a `(pi, pi)` le sue fasi sono `+-0.150`.**
- ### **I SOLITONI LARGHI** *(`profilo()` con la scatola in ARCHI)*: ### **`S1` legato e largo `>= 4` archi gia' a `s 0.3`** *(`N 1e5`: `4.24`; `N 1e7`: `13.2`; `mu > 0`)*; ### **`S4` solo da `s 0.9`**
  *(`N 1e7`: `5.39`)*; ### **`S3` largo e RAPPRESENTABILE solo a `s 0.99`** *(`N 1e3`: `4.64`)*: ### **gli stati larghi di `S3` hanno la coda logaritmica sotto il doppio** *(«NON RAPPRESENTABILE»:
  nessun pavimento, come chiede il mandato)*.
- ### **Un mio errore di procedura, dichiarato:** ### **ho modificato `csv/_forza_da_cs.py` mentre una mia esplorazione che lo aveva importato girava ancora**; ### **l'ho rimesso subito ai byte di
  `HEAD`** *(`git cat-file`, blob `e8789ea9`)*; ### **la modifica** *(la `PORTANTE`)* ### **va nel commit dello strumento.**

## 2. IL METODO

### PARTE A -- I MODI A `k = pi`

- ### **`s` in `(0.1, 0.3, 0.5, 0.9)`, `eps` in `(0, 0.5)`, lato `64`, zero simmetrico.** ### **Le bande della materia lungo le TRE linee da `(0, 0)` a `(pi, 0)`, `(0, pi)`, `(pi, pi)`**
  *(`rami_seguiti` sulla matrice di `matrice()` riordinata: trasposta per `(0, m)`, la diagonale `(m, m)` messa sulla riga `(m, 0)`)*; ### **per OGNI gruppo massivo** *(da `k = 0`)*: ### **la distanza dalla
  banda piu' vicina che NON e' del suo gruppo, lungo le tre linee**; ### **il minimo, il suo `k`, la fase.**
- ### **IL PUNTO `k*` DEL MODO** *(dichiarato)*: ### **fra `(pi, 0)`, `(0, pi)`, `(pi, pi)` quello dove il gruppo ha il salto PIU' PICCOLO MA NON NULLO** *(`>= 1e-6`: un punto senza salto e' senza
  massa, e li' curvatura e pacchetto fermo non hanno senso)*; ### **in quei punti la velocita' di gruppo e' nulla per simmetria** *(verificato: la differenza centrata)*.
- ### **A `k*`, per ogni gruppo:** ### **la fase continua da `s` piccolo** *(`_scala_e_zero.cammino` con `blocchi` avvolta in memoria per restituire il blocco a `k*`, lato `16`)*; ### **il TENSORE
  della curvatura** *(`d2/dkx2`, `d2/dky2`, `d2/dkx dky`, dalle fasi esatte ai vicini `+-1`, `+-2` passi, il ramo seguito per sovrapposizione del vettore proprio)*; ### **`v`** *(il fit di
  `51f45268` lungo `x` attorno a `k*`)*; ### **`E0 = omega/s`, `M = omega''_xx/s`, il segno di `E0 M`, `D`, e `a_H/a_RG = s (omega''_xx/v^2) d omega/ds` a `lambda 0` e `1/2`.**
- ### **`lambda*`:** ### **dalle due rette** *(due punti: `a_H/a_RG` e' lineare in `lambda`, `e31366ec`)*.
- ### **A `k = 0`** *(il controllo)*: ### **`_segno_gravita.h_su_rg` a `s0 0.3`, `0.5`**, ### **contro il `jsonl` di `e31366ec`.**

### PARTE B -- LA FORZA SUI MODI A `k*`

- ### **`_forza_da_cs.corsa`** *(il pacchetto, la finestra, la norma fuori)* ### **con la `PORTANTE` `e^{i k*.x}`** *(una variabile del modulo, `None` = com'era, impostata in memoria)* ### **e il vettore
  proprio del ramo a `k*`** *(`spazio_proprio` del blocco a `k*`, la sua fase)*; ### **`s0` in `(0.3, 0.5)`, `eps` `0` e `0.5`, `eta` in `(0, 5e-4, 1e-3, 5e-3, 1e-2)`, `Lx 256`, le DUE convenzioni.**
  ### **`a_H = -omega''_xx (d omega/ds)(ds/dx)`, `a_RG = -v^2 (ds/dx)/s0`.** ### **Accanto: `k = 0` di `e31366ec`.**

### PARTE C -- I SOLITONI LARGHI

- ### **`_gravita_collettiva.profilo()` con la scatola in ARCHI:** ### **`R = 10 w`, `dr = min(w, sigma)/64`, la partenza gaussiana larga `w`**, ### **ripetuto con `w` la larghezza trovata finche' non
  cambia oltre `1e-3`** *(lo stato non dipende dalla scatola)*; ### **«DISPERSIONE» se la larghezza supera `3000` archi o la scatola**; ### **nessun pavimento: «NON RAPPRESENTABILE» resta tale.**
- ### **`S1`, `S3`, `S4`, `eps 0`, ramo a curvatura `-`, `s` in `(0.3, 0.5, 0.7, 0.9, 0.95, 0.99)`, `N` in `(10, 100, 1e3, 1e4, 1e5, 1e6, 1e7)`.**
- ### **Il controllo di servizio: la gaussiana esatta** *(il logaritmo puro, `c -0.8, s 0.9, N 10`, con la scatola nuova)* ### **entro `1e-6`.**
- ### **La tabella `larghezza(s, N, forma)` e il piu' piccolo `s` con uno stato legato largo `>= 4` archi.**
- ### ⛔ **LA DINAMICA COMPLETA** *(parte `C.3`)* ### **E' LUNGA: va in un commit e uno strumento a se'**, ### **dopo questo referto**, ### **coi punti scelti qui.**

## 3. LE PREVISIONI *(prima dei numeri)*

- ### **IL SALTO MINIMO:** ### **a `eps 0` a `(pi, pi)`, NULLO, a ogni `s`** *(la banda senza massa)*: ### **il deve-fallire «il salto minimo e' a `k = 0` a `s 0.3`» FALLIRA'.** ### **Le eccitazioni di
  energia piu' bassa** *(l'ipotesi `(1)` del guardiano)* ### **a `eps 0` sono SENZA MASSA a `(pi, pi)`.**
- ### **A `k*` = `(pi, 0)`** *(`eps 0`)*: ### **la coppia a `+-0.654` a `s 0.3`**: ### **il segno di `E0 M`, `a_H/a_RG`: non li prevedo** *(il guardiano, debole: `E0 M > 0` su almeno un ramo,
  `a_H/a_RG > 0`)*.
- ### **I SOLITONI:** ### **almeno una forma larga `>= 4` archi a `s <= 0.5`: `S1`** *(il puo'-fallire PASSERA')*; ### **la tensione dell'ipotesi `(2)`: VERA per `S3` e `S4`** *(larghi solo a
  `s >= 0.9`)*, ### **FALSA per `S1`** *(largo gia' a `s 0.3`, perche' la sua non linearita' a poca materia e' debole: `x^2`)*.

## 4. I CRITERI, FISSATI ORA *(dal mandato)*

- ### **DEVE PASSARE:** ### **a `k = 0`, `a_H/a_RG` di `s0 0.3` e `0.5`, `lambda 0` e `1/2`, = `e31366ec` entro `1e-9`.**
- ### **DEVE PASSARE:** ### **`eta = 0` nella parte `B`: `|a|` sotto il rumore** *(`_forza_da_cs.nullo`)*; ### **e `eps 0.5, s0 0.1` dopo la correzione: GIA' PROVATO** *(`6c36b19a`, `2` su `2`)*.
- ### **DEVE PASSARE:** ### **la gaussiana esatta col risolutore nuovo, errore `< 1e-6`.**
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«il salto minimo e' a `k = 0` a `s 0.3`»** *(il `k` del minimo trovato e la sua distanza, stampati)*.
- ### **PUO' FALLIRE:** ### **parte `A`: `E0 M > 0` su almeno un ramo a `k*` a `s 0.3`.**
- ### **PUO' FALLIRE:** ### **parte `C`: almeno una forma con uno stato legato largo `>= 4` archi a `s <= 0.5`.**
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE:** ### **le tabelle.** ### **A parte: la lettura in tre righe; una riga su dove sta la fisica a bassa energia; una riga sulla tensione
  larghezza / principio di equivalenza, per Luca.**

### 📝 **ANNOTAZIONE 1** *(prima della corsa dello strumento committato, nel commit dello strumento)*: ### **la prova a vuoto in memoria** *(griglia ridotta: `s 0.3`, il `jsonl` negli appunti)*
### **ha mostrato due DIFETTI DEL MIO METODO, corretti prima della corsa, e dei numeri che dichiaro:**
- ### **(a) LE BANDE DEGENERI col gruppo a `k = 0`** *(le sue copie e le bande piatte con la stessa `omega(0)`: lo spazio a `k = 0` del ramo alto ha dimensione `4`, `557d94d6`)* ### **davano un
  «salto» nullo a `k = 0`**: ### **non sono «altre bande», e si escludono.**
- ### **(b) UN PUNTO `k*` DOVE LA BANDA E' PIATTA** *(curvatura `~0`, `v ~ 0`: il ramo alto seguito lungo `y` arrivava a `(0, pi)` su una banda piatta, e `a_H/a_RG ~ 1e14`)* ### **non e' un modo
  massivo fermo**: ### **`k*` e' il primo candidato** *(in ordine di salto)* ### **con curvatura e `v` non nulli** *(`>= 1e-6`)*.
- ### **(c) IL PASSO DELLA GRIGLIA DEI SOLITONI:** ### **`dr = w/640`, non `min(w, sigma)/64`** *(sez. `2`)*: ### **con `/64` la gaussiana esatta sbaglia di `~4e-5`** *(l'ordine `2` di `8b6cca50`)*, ### **e
  `w/640` tiene la scatola a `6400` punti per ogni `w`.** ### **La gaussiana esatta, provata: `3.7e-7`.**
- ### **I NUMERI VISTI** *(non li uso; le previsioni restano)*: ### **a `eps 0, s 0.3` i due rami hanno `k* = (pi, 0)`, salto `0.654`, e nella SIMMETRICA `a_H/a_RG = +2.30` TUTTI E DUE** *(verso `cs`
  BASSO; `lambda* = 0.500000` anche li')*; ### **oggi `+5.76` e `-1.16`**; ### **misurato, simmetrica, ramo a curvatura `-`: `+2.15`..`+2.20`**; ### **`E0 M > 0` a `k*` su tutti i rami visti**;
  ### **`eta = 0` a `eps 0.5, (pi, pi)` vi fallisce** *(`7.9e-6` contro `sigma 2.9e-6`)*.

## 5. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_modi_pi_e_solitoni.py` *(parti `A`, `B`, `C.1`-`C.2`)*, la `PORTANTE` in `csv/_forza_da_cs.py` e le voci dell'inventario, committati prima dei numeri;
3. la corsa, il referto, la relazione, la sezione `6`;
4. la parte `C.3` *(la dinamica dei solitoni larghi)*: il suo task history, il suo strumento, la sua corsa, il suo referto -- a se'.

## 6. I RISULTATI *(scritti dopo la corsa, sotto)*

### **LA CORSA:** `python csv/_modi_pi_e_solitoni.py`, strumento sha1-BYTE `1ed7c073` *(`9fbfede3`; `_forza_da_cs` `1cd55ba0`)*. ### **`5` controlli su `6`.**

- ### **DEVE PASSARE, `k = 0` = `e31366ec`: PASSA** *(`0.0`)*. ### **DEVE PASSARE, la gaussiana esatta col risolutore nuovo: PASSA** *(`3.7e-7`)*.
- ### **DEVE FALLIRE, «il salto minimo e' a `k = 0` a `s 0.3`»: FALLISCE per la chiave giusta** *(i due rami di `eps 0`: il minimo a `(pi, pi)`, distanza `0`)*.
- ### **PUO' FALLIRE, `E0 M > 0` su almeno un ramo a `k*` a `s 0.3`: PASSA** *(tutti e tre, nella simmetrica)*. ### **PUO' FALLIRE, una forma larga `>= 4` archi a `s <= 0.5`: PASSA** *(`S1`)*.
- ### ⚠ **DEVE PASSARE, `eta = 0` nella parte `B`: FALLISCE** ### **sulle righe di `eps 0.5` a `(pi, pi)`** *(`a = 7.9e-6` contro `sigma 2.9e-6` a `s0 0.3`; anche a `0.5`)*: ### **il pacchetto a `(pi, pi)`
  DERIVA senza gradiente** *(la norma fuori `0.011`; e le righe col gradiente non passano la linearita')*; ### **le righe di `eps 0` passano.** ### **Il criterio non cambia; quelle righe NON SI LEGGONO.**
- ### **`eps 0.5, s0 0.1` dopo la correzione: gia' provato** *(`6c36b19a`, `2` su `2`)*.

### 6.1 IL SALTO MINIMO DI OGNI GRUPPO *(zero simmetrico; la distanza dalle bande non degeneri a `k = 0`)*

| `eps` | `s` | ramo | salto minimo | a `k` (`pi`) | fase | `(pi,0)` | `(0,pi)` | `(pi,pi)` |
|---|---|---|---|---|---|---|---|---|
| `0` | `0.1` | curv + Dt 0.1696 | `0.00000` | `(1.00, 1.00)` | `+0.0000` | `0.2217` | `0.3142` | `0.0000` |
| `0` | `0.1` | curv - Dt 0.1696 | `0.00000` | `(1.00, 1.00)` | `+0.0000` | `0.2217` | `0.2217` | `0.0000` |
| `0` | `0.3` | curv + Dt 0.4807 | `0.00000` | `(1.00, 1.00)` | `+0.0000` | `0.6536` | `0.9425` | `0.0000` |
| `0` | `0.3` | curv - Dt 0.4807 | `0.00000` | `(1.00, 1.00)` | `+0.0000` | `0.6536` | `0.6536` | `0.0000` |
| `0` | `0.5` | curv + Dt 0.6858 | `1.04720` | `(1.00, 0.00)` | `-1.0472` | `1.0472` | `1.5708` | `1.5708` |
| `0` | `0.5` | curv - Dt 0.6858 | `0.00000` | `(1.00, 1.00)` | `+0.0000` | `1.0472` | `1.0472` | `0.0000` |
| `0` | `0.9` | curv + Dt 0.2836 | `0.00000` | `(1.00, 1.00)` | `+0.0000` | `1.5463` | `1.9094` | `0.0000` |
| `0` | `0.9` | curv - Dt 0.2836 | `0.00000` | `(1.00, 1.00)` | `-0.0000` | `1.5463` | `1.5463` | `0.0000` |
| `0.5` | `0.1` | curv + Dt 0.2233 | `0.00388` | `(0.00, 0.00)` | `-0.3180` | `0.0945` | `0.0945` | `0.0577` |
| `0.5` | `0.1` | curv - Dt 0.1650 | `0.04230` | `(1.00, 1.00)` | `+0.0500` | `0.2193` | `0.2193` | `0.0423` |
| `0.5` | `0.3` | curv - Dt 0.4684 | `0.12842` | `(1.00, 1.00)` | `+0.1500` | `0.6432` | `0.6432` | `0.1284` |
| `0.5` | `0.5` | curv - Dt 0.6718 | `0.21938` | `(1.00, 1.00)` | `+0.2500` | `1.0172` | `1.0172` | `0.2194` |
| `0.5` | `0.9` | curv + Dt 0.0132 | `0.24418` | `(0.00, 0.00)` | `-2.8432` | `1.1176` | `1.1176` | `2.3932` |
| `0.5` | `0.9` | curv - Dt 0.4253 | `0.43425` | `(1.00, 1.00)` | `+0.4500` | `1.3823` | `1.3823` | `0.4343` |

### 6.2 IL MODO A `k*` *(curvatura: il tensore, `xx`, `yy`, `xy`)*, `E0`, `M`, `a_H/a_RG` NELLE DUE CONVENZIONI

| `eps` | `s` | ramo | `k*` | salto | `xx` | `yy` | `xy` | `v` | oggi `E0` | oggi `E0 M` | oggi `a_H/a_RG` | simm `E0` | simm `E0 M` | simm `a_H/a_RG` | `D` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.1` | curv + Dt 0.1696 | (pi,0) | `0.2217` | `-0.0556` | `+0.0556` | `+0.0000` | `0.0687` | `-5.3584` | **+** | `+6.3012` | `-2.2169` | **+** | `+2.6005` | `+9.21e-02` |
| `0` | `0.1` | curv - Dt 0.1696 | (0,pi) | `0.2217` | `-0.0556` | `+0.0556` | `-0.0000` | `0.1867` | `-0.9247` | **+** | `+0.1491` | `+2.2169` | - | `-0.3524` | `-9.21e-02` |
| `0` | `0.3` | curv + Dt 0.4807 | (pi,0) | `0.6536` | `-0.1695` | `+0.1695` | `+0.0000` | `0.2148` | `-5.3203` | **+** | `+5.7646` | `-2.1787` | **+** | `+2.3029` | `+2.96e-01` |
| `0` | `0.3` | curv - Dt 0.4807 | (pi,0) | `0.6536` | `+0.1695` | `-0.1695` | `-0.0000` | `0.2148` | `-0.9629` | - | `-1.1588` | `+2.1787` | **+** | `+2.3029` | `-2.96e-01` |
| `0` | `0.5` | curv + Dt 0.6858 | (pi,0) | `1.0472` | `-0.2887` | `+0.2887` | `+0.0000` | `0.3885` | `-5.2360` | **+** | `+4.7376` | `-2.0944` | **+** | `+1.7341` | `+5.61e-01` |
| `0` | `0.5` | curv - Dt 0.6858 | (0,pi) | `1.0472` | `-0.2887` | `+0.2887` | `-0.0000` | `0.7021` | `-1.0472` | **+** | `+0.3888` | `+2.0944` | - | `-0.5311` | `-5.61e-01` |
| `0` | `0.9` | curv + Dt 0.2836 | (pi,0) | `1.5463` | `-0.4879` | `+0.4879` | `+0.0000` | `0.8232` | `-4.8597` | **+** | `+2.3501` | `-1.7181` | **+** | `+0.3146` | `+1.37e+00` |
| `0` | `0.9` | curv - Dt 0.2836 | (pi,0) | `1.5463` | `+0.4879` | `-0.4879` | `+0.0000` | `0.8232` | `-1.4235` | - | `-1.7209` | `+1.7181` | **+** | `+0.3146` | `-1.37e+00` |
| `0.5` | `0.1` | curv + Dt 0.2233 | (pi,pi) | `0.0577` | `-0.2447` | `-0.2447` | `+0.0000` | `0.1013` | `-3.6416` | **+** | `+8.6896` | `-0.5000` | **+** | `+1.1931` | `+1.14e-11` |
| `0.5` | `0.1` | curv - Dt 0.1650 | (pi,pi) | `0.0423` | `+0.2438` | `+0.2438` | `+0.0000` | `0.1013` | `-2.6416` | - | `-6.2758` | `+0.5000` | **+** | `+1.1879` | `-1.11e-11` |
| `0.5` | `0.3` | curv - Dt 0.4684 | (pi,pi) | `0.1284` | `+0.6690` | `+0.6690` | `+0.0000` | `0.2955` | `-2.6416` | - | `-6.0732` | `+0.5000` | **+** | `+1.1495` | `-1.39e-12` |
| `0.5` | `0.5` | curv - Dt 0.6718 | (pi,pi) | `0.2194` | `+0.9269` | `+0.9269` | `+0.0000` | `0.4643` | `-2.6416` | - | `-5.6779` | `+0.5000` | **+** | `+1.0747` | `-1.44e-12` |
| `0.5` | `0.9` | curv + Dt 0.0132 | (0,pi) | `1.1176` | `-0.0836` | `-0.0033` | `-0.0000` | `0.0626` | `-6.2081` | **+** | `+112.7225` | `-3.0665` | **+** | `+52.2950` | `+3.86e-01` |
| `0.5` | `0.9` | curv - Dt 0.4253 | (pi,pi) | `0.4343` | `+0.8015` | `+0.8015` | `+0.0000` | `0.6644` | `-2.6416` | - | `-4.3167` | `+0.5000` | **+** | `+0.8171` | `-1.54e-13` |

### 6.3 `lambda*` A `k*`

- `eps 0`, `s 0.3`, curv + Dt 0.4807 / curv - Dt 0.4807 a (pi,0): `lambda* = 0.500000`.
- `eps 0`, `s 0.9`, curv + Dt 0.2836 / curv - Dt 0.2836 a (pi,0): `lambda* = 0.500000`.
- `eps 0.5`, `s 0.1`, curv + Dt 0.2233 / curv - Dt 0.1650 a (pi,pi): `lambda* = 0.500175`.

### 6.4 LA FORZA SUL MODO A `k*` *(`Lx 256`; `a/a_RG > 0` = verso `cs` BASSO)*

| conv. | `eps` | `s0` | ramo | `k*` | `eta` | `a_mis/a_RG` | `a_mis/a_H` | lin | fuori | si legge |
|---|---|---|---|---|---|---|---|---|---|---|
| oggi | `0` | `0.3` | curv + Dt 0.4807 | (pi,0) | `0.001` | `+5.520` | `+0.958` | `2.008` | `0.000` | si' |
| oggi | `0` | `0.3` | curv + Dt 0.4807 | (pi,0) | `0.01` | `+5.538` | `+0.961` | `2.000` | `0.000` | si' |
| simm | `0` | `0.3` | curv + Dt 0.4807 | (pi,0) | `0.001` | `+2.187` | `+0.950` | `2.021` | `0.000` | si' |
| simm | `0` | `0.3` | curv + Dt 0.4807 | (pi,0) | `0.01` | `+2.207` | `+0.958` | `2.002` | `0.000` | si' |
| oggi | `0` | `0.3` | curv - Dt 0.4807 | (pi,0) | `0.001` | `-1.188` | `+1.025` | `1.904` | `0.002` | si' |
| oggi | `0` | `0.3` | curv - Dt 0.4807 | (pi,0) | `0.01` | `-1.134` | `+0.978` | `1.989` | `0.002` | si' |
| simm | `0` | `0.3` | curv - Dt 0.4807 | (pi,0) | `0.001` | `+2.145` | `+0.931` | `2.057` | `0.002` | si' |
| simm | `0` | `0.3` | curv - Dt 0.4807 | (pi,0) | `0.01` | `+2.199` | `+0.955` | `2.005` | `0.002` | si' |
| oggi | `0` | `0.5` | curv + Dt 0.6858 | (pi,0) | `0.001` | `+4.559` | `+0.962` | `2.001` | `0.000` | si' |
| oggi | `0` | `0.5` | curv + Dt 0.6858 | (pi,0) | `0.01` | `+4.559` | `+0.962` | `1.999` | `0.000` | si' |
| simm | `0` | `0.5` | curv + Dt 0.6858 | (pi,0) | `0.001` | `+1.666` | `+0.961` | `2.003` | `0.000` | si' |
| simm | `0` | `0.5` | curv + Dt 0.6858 | (pi,0) | `0.01` | `+1.668` | `+0.962` | `2.000` | `0.000` | si' |
| oggi | `0` | `0.5` | curv - Dt 0.6858 | (0,pi) | `0.001` | `+0.376` | `+0.967` | `1.993` | `0.000` | si' |
| oggi | `0` | `0.5` | curv - Dt 0.6858 | (0,pi) | `0.01` | `+0.375` | `+0.964` | `1.999` | `0.000` | si' |
| simm | `0` | `0.5` | curv - Dt 0.6858 | (0,pi) | `0.001` | `-0.511` | `+0.962` | `2.005` | `0.000` | si' |
| simm | `0` | `0.5` | curv - Dt 0.6858 | (0,pi) | `0.01` | `-0.512` | `+0.964` | `2.001` | `0.000` | si' |
| oggi | `0.5` | `0.3` | curv - Dt 0.4684 | (pi,pi) | `0.001` | `-2.608` | `+0.430` | `-4.857` | `0.011` | **no** |
| oggi | `0.5` | `0.3` | curv - Dt 0.4684 | (pi,pi) | `0.01` | `-5.912` | `+0.974` | `2.130` | `0.011` | **no** |
| simm | `0.5` | `0.3` | curv - Dt 0.4684 | (pi,pi) | `0.001` | `+4.665` | `+4.058` | `1.118` | `0.011` | **no** |
| simm | `0.5` | `0.3` | curv - Dt 0.4684 | (pi,pi) | `0.01` | `+1.350` | `+1.175` | `1.571` | `0.011` | **no** |
| oggi | `0.5` | `0.5` | curv - Dt 0.6718 | (pi,pi) | `0.001` | `-4.421` | `+0.779` | `2.617` | `0.011` | **no** |
| oggi | `0.5` | `0.5` | curv - Dt 0.6718 | (pi,pi) | `0.01` | `-5.361` | `+0.944` | `2.040` | `0.011` | si' |
| simm | `0.5` | `0.5` | curv - Dt 0.6718 | (pi,pi) | `0.001` | `+2.050` | `+1.907` | `1.326` | `0.011` | **no** |
| simm | `0.5` | `0.5` | curv - Dt 0.6718 | (pi,pi) | `0.01` | `+1.112` | `+1.035` | `1.828` | `0.011` | **no** |

### 6.5 I SOLITONI LARGHI *(la scatola in archi; eps 0, ramo a curvatura `-`)*: la larghezza in archi, `LEGATO` / altro


**S1**

| `s` \ `N` | `10` | `100` | `1000` | `10000` | `100000` | `1e+06` | `1e+07` |
|---|---|---|---|---|---|---|---|
| `0.3` | DISPERSION | `0.96` | `1.44` | `2.44` | **`4.24`** | **`7.46`** | **`13.20`** |
| `0.5` | DISPERSION | `1.02` | `1.51` | `2.54` | **`4.42`** | **`7.78`** | **`13.76`** |
| `0.7` | DISPERSION | `1.18` | `1.67` | `2.78` | **`4.82`** | **`8.48`** | **`14.98`** |
| `0.9` | DISPERSION | `2.11` | `2.22` | `3.57` | **`6.13`** | **`10.72`** | **`18.92`** |
| `0.95` | DISPERSION | DISPERSION | `2.79` | **`4.29`** | **`7.27`** | **`12.67`** | **`22.32`** |
| `0.99` | DISPERSION | DISPERSION | **`6.57`** | **`7.00`** | **`11.25`** | **`19.30`** | **`33.77`** |

**S3**

| `s` \ `N` | `10` | `100` | `1000` | `10000` | `100000` | `1e+06` | `1e+07` |
|---|---|---|---|---|---|---|---|
| `0.3` | `0.63` | `0.95` | NON | NON | NON | NON | NON |
| `0.5` | `0.66` | `0.99` | NON | NON | NON | NON | NON |
| `0.7` | `0.75` | `1.10` | `1.80` | NON | NON | NON | NON |
| `0.9` | `1.08` | `1.47` | `2.33` | NON | NON | NON | NON |
| `0.95` | `1.42` | `1.84` | `2.81` | NON | NON | NON | NON |
| `0.99` | `3.02` | `3.39` | **`4.64`** | **`7.32`** | NON | NON | NON |

**S4**

| `s` \ `N` | `10` | `100` | `1000` | `10000` | `100000` | `1e+06` | `1e+07` |
|---|---|---|---|---|---|---|---|
| `0.3` | `0.51` | `0.54` | `0.70` | `1.00` | `1.48` | `2.24` | `3.45` |
| `0.5` | `0.55` | `0.58` | `0.74` | `1.05` | `1.56` | `2.36` | `3.63` |
| `0.7` | `0.68` | `0.66` | `0.84` | `1.18` | `1.74` | `2.63` | **`4.03`** |
| `0.9` | `1.28` | `1.02` | `1.20` | `1.63` | `2.36` | `3.53` | **`5.39`** |
| `0.95` | `2.24` | `1.42` | `1.55` | `2.05` | `2.93` | **`4.36`** | **`6.62`** |
| `0.99` | **`14.56`** | **`4.00`** | `3.19` | `3.76` | **`5.11`** | **`7.42`** | **`11.11`** |

- **S1**: il primo `s` largo `>= 4` archi: `s 0.3`, `N` [100000.0, 1000000.0, 10000000.0].

- **S3**: il primo `s` largo `>= 4` archi: `s 0.99`, `N` [1000.0, 10000.0].

- **S4**: il primo `s` largo `>= 4` archi: `s 0.7`, `N` [10000000.0].

### 6.6 LA LETTURA, IN TRE RIGHE *(nessuna conclusione oltre le tabelle)*

1. ### **A `k = pi` A `eps 0` LA BANDA PIU' BASSA E' SENZA MASSA, E I MODI MASSIVI SONO SELLE:** ### **i due rami si toccano a `(pi, pi)`** *(distanza `0` a ogni `s` tranne `0.5`, dove il minimo del
   ramo `+` e' a `(pi, 0)`)*; ### **a `(pi, 0)` il salto e' `0.22`, `0.65`, `1.05`, `1.55` a `s 0.1`-`0.9`, e la curvatura e' `xx = -yy`: L'INERZIA HA SEGNO OPPOSTO NELLE DUE DIREZIONI.**
   ### **Il verso della caduta dipende allora da come il gradiente e' orientato rispetto alla sella:** ### **col gradiente lungo `x`, il modo a `(pi, 0)` nella simmetrica cade verso `cs` BASSO**
   *(misurato `+2.15`..`+2.21` a `s0 0.3` sui DUE rami, `+1.67` a `0.5`; `a/a_H` `0.93`-`0.97`)*, ### **quello a `(0, pi)` verso `cs` ALTO** *(`-0.51` a `s0 0.5`)*.
2. ### **LO ZERO UNIVERSALE RESTA `1/2` ANCHE A `k = pi`** *(`lambda* = 0.500000` a `(pi, 0)`, `s 0.3` e `0.9`; `0.500175` a `(pi, pi)`, `eps 0.5, s 0.1`)*; ### **`E0 M > 0` a `k*` su tutti i rami di `eps 0` e
   `eps 0.5` nella simmetrica** *(tranne il ramo a curvatura `-` di `eps 0` quando `k*` e' `(0, pi)`)*; ### **a `eps 0.5` il modo a `(pi, pi)` e' ISOTROPO** *(`xx = yy`)*, ### **simmetrica `a_H/a_RG`
   `+1.07`..`+1.19`** ### **-- ma la sua corsa non si legge** *(la deriva a `eta = 0`, la linearita')*.
3. ### **I SOLITONI LARGHI ESISTONO, MA NON TUTTI A `s` PICCOLO:** ### **`S1` largo `>= 4` archi gia' a `s 0.3`** *(`N >= 1e5`, `4.2`-`13.2` archi)*, ### **`S4` da `s 0.7`** *(`N 1e7`, `4.03`)*, ### **`S3` solo a
   `s 0.99`** *(`N 1e3`, `1e4`; piu' larghi NON RAPPRESENTABILI: la coda logaritmica)*. ### **La loro caduta e' la parte `C.3`, a se'.**

### **DOVE STA LA FISICA A BASSA ENERGIA** *(informazione)*: ### **a `eps 0` le eccitazioni piu' basse sono a `(pi, pi)`, SENZA MASSA** *(i «doppioni» del reticolo)*; ### **i modi massivi a
`(pi, 0)` sono SELLE, non particelle con un'inerzia sola**; ### **a `eps 0.5` il modo piu' basso e' a `(pi, pi)`, isotropo e massivo** *(il salto `0.04`-`0.43` a `s 0.1`-`0.9`)*: ### **li' la
moneta da' una particella vera, e la sua previsione di Hamilton nella simmetrica e' vicina a `+1`.**

### **LA TENSIONE LARGHEZZA / PRINCIPIO DI EQUIVALENZA** *(per Luca)*: ### **per `S3` e `S4` l'ipotesi `(2)` del guardiano regge** *(larghi solo a `s >= 0.7`-`0.99`, dove `05055fc6` misura la
violazione d'ordine `1`)*; ### **per `S1` NO: e' largo gia' a `s 0.3`, con `mu > 0`** *(la sua non linearita' a poca materia e' debole, `x^2`)*.

## 7. LA PARTE C.3 -- LA DINAMICA DEI SOLITONI LARGHI *(scritta PRIMA del suo codice, dopo il referto `9a6955f3`)*

> ### ⛔ **GRIGLIA QUADRATA -- non eseguita (DECISIONE-SOLO-TRIANGOLI)** *(decisione di Luca del `2026-10-23`, `16:14`: si lavora SOLO sui triangoli; questa parte resta scritta, lo strumento committato, e NON si corre)*.

### IL METODO

- ### **I PUNTI** *(da `6.5`: il primo `s` con uno stato legato largo `>= 4` archi, le due norme piu' piccole se ci sono)*: ### **`S1` a `s 0.3`, `N 1e5` e `1e6`; `S4` a `s 0.7`, `N 1e7`** *(una sola)*; ### **`S3` a
  `s 0.99`, `N 1e3` e `1e4`.** ### ⚠ **`S3` a `s 0.99` e' oltre `0.9`: li' il principio di equivalenza e' gia' violato d'ordine `1`** *(`05055fc6`)* ### **e si legge SOLO IL VERSO.**
- ### **LA SCENA:** ### **la camminata INTERA** *(`salta = ()`, la forma con `_screening_forme_s3.forma`)*, ### **`eps 0`, le DUE convenzioni**, ### **il toro `Lx x Ly = 256 x 64`** *(`Ly` piu' di
  otto larghezze per il piu' largo, `7.5` archi)*, ### **`dtau = 1`, `mot.cs` uniforme `s` o il profilo, `lambda_c = None`**, ### **il vuoto `phi = VUOTO = 1` per estremita'** *(`Lambda0 = 4`: il livello
  `1` di `c4efc937`)*.
- ### **LO STATO INIZIALE:** ### **il profilo `u(r)` di `_gravita_collettiva.profilo`** *(la scatola in archi di `C.1`, alla larghezza trovata)*, ### **la densita' per nodo `u(r)^2` sul vettore del ramo a
  curvatura `-` a `k = 0`** *(`_forza_da_cs.spazio_del_ramo`)*, ### **a `(Lx/4, Ly/2)`, fermo, la norma riportata a `N`.** ### ⚠ **Il profilo e' un PUNTO DI PARTENZA** *(dall'inviluppo approssimato),
  non uno stato fermo dell'automa.*
- ### **L'ASSESTAMENTO:** ### **`T0 = max(10 * 2 pi/|mu|, 64)` tick a `cs` uniforme** *(il periodo dal `mu` di `C.1`)*; ### **la norma EMESSA = la frazione della norma della materia oltre `3 w0` dal
  baricentro, alla fine di `T0`.**
- ### **LA TENUTA:** ### **dallo stato assestato, `T = Lx/4 = 64` tick a `cs` uniforme**: ### **la larghezza** *(rms attorno al baricentro, immagine minima)* ### **entro il `10%` di quella all'inizio
  della tenuta a ogni tick**, ### **il baricentro fermo** *(`|a| <= 2 sigma_a`, il fit di `_forza_da_cs` sulla stessa finestra)*. ### **Se non tiene: un RISULTATO** *(«NON TIENE» col tick)*, ### **e
  la forza li' non si misura.**
- ### **LA FORZA:** ### **dallo stato ASSESTATO, il profilo `cs(x) = s (1 + eta cos(2 pi x/Lx))`, `eta` in `(1e-3, -1e-3, 1e-2, -1e-2)`**, ### **il baricentro circolare in `x` per `T = 64` tick, la
  finestra `|<x> - x0| < Lx/32`, il fit `x0 + v0 t + a t^2/2`**, ### **`a_RG = -v^2 (ds/dx)/s`** *(`v` del ramo a `k = 0`)*, ### **`a_mis/a_RG`, il verso.**
- ### **LA SCOMPOSIZIONE:** ### **`E_ramo = omega0/s`** *(oggi `0`, simmetrica `+pi`)* ### **e `E_legame = mu/s`** *(di `C.1`)*: ### **quale domina in modulo.**

### LE PREVISIONI *(prima dei numeri)*

- ### **Hamilton per il solitone fermo** *(la sez. `3-bis` di `2026-10-23_segno_gravita.md`)*: ### **`a/a_RG = s (omega''/v^2)(d omega0/ds + d mu/ds)`**, ### **col ramo a curvatura `-`.**
- ### **`S1` e `S4`: `mu > 0`** *(`+0.30`, `+2.7` circa)*: ### **oggi `d mu/ds > 0` con `omega'' < 0` -> verso `cs` ALTO; simmetrica `pi + d mu/ds > 0` -> verso `cs` ALTO.** ### **`S3` a `s 0.99`:
  `mu < 0`** *(`-0.63`, `-0.07`)*: ### **oggi verso `cs` BASSO se `d mu/ds < 0`; simmetrica verso `cs` ALTO** *(il legame non supera `pi`)*.
- ### **E la tenuta: NON LA SO** *(il profilo non e' uno stato dell'automa; il vuoto reagisce)*.

### I CRITERI *(dal mandato, fissati ora)*

- ### **DEVE PASSARE:** ### **a `cs` uniforme, `|a|` sotto il rumore del fit** *(la tenuta)*.
- ### **DEVE PASSARE:** ### **il profilo specchiato** *(`eta -> -eta`)*: ### **`a` cambia segno, `|a|` uguale entro il `5%`.**
- ### **PUO' FALLIRE:** ### **almeno un solitone `S3` o `S4` con lo zero simmetrico e `a_mis/a_RG > 0`.**
- ### **IL VERDETTO DI FISICA:** ### **il verso e `a_mis/a_RG` per forma, norma, convenzione; il confronto fra le due norme della stessa forma.**

### 📝 **ANNOTAZIONE 2** *(prima della corsa di `C.3`, nel commit del suo strumento)*: ### **la prova a vuoto in memoria** *(il primo punto, `S1 s 0.3 N 1e5`, con `T0 = 4` e `8` tick di misura; il `jsonl`
negli appunti)* ### **ha mostrato che la DERIVA PROPRIA del solitone** *(`a ~ -1.2e-4` a ogni `eta`, anche col segno di `eta` rovesciato)* ### **sta molto sopra la forza attesa** *(`a_RG ~ 1.5e-6` a `eta
1e-3`)* ### **-- con `8` tick; nella corsa vera il fit ha `64` tick e l'assestamento `~210`.** ### **AGGIUNGO, prima della corsa, la stima che separa le due:** ### **la parte ANTISIMMETRICA in `eta`,
`(a(+eta) - a(-eta))/2`, e' la forza; quella SIMMETRICA e' la deriva propria.** ### **Il criterio dello specchio resta com'era** *(e se la deriva domina, fallira': lo leggo come la misura dice)*.
### **I numeri della prova a vuoto non li uso.** ### **E la tenuta, con `8` tick, vi passava** *(larghezza entro `1.3%`)*.
