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

## 5. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_modi_pi_e_solitoni.py` *(parti `A`, `B`, `C.1`-`C.2`)*, la `PORTANTE` in `csv/_forza_da_cs.py` e le voci dell'inventario, committati prima dei numeri;
3. la corsa, il referto, la relazione, la sezione `6`;
4. la parte `C.3` *(la dinamica dei solitoni larghi)*: il suo task history, il suo strumento, la sua corsa, il suo referto -- a se'.

## 6. I RISULTATI *(scritti dopo la corsa, sotto)*
