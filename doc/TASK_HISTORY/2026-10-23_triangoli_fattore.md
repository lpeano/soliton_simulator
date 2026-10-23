# IL FATTORE 1.63-1.68 SUI TRIANGOLI: IL PACCHETTO NON FERMO E L'IMPULSO INIZIALE, E LA SCOMPOSIZIONE DEL FATTORE IN OROLOGIO, EINSTEIN E LUCE

> **Il mandato:** di Luca, «il fattore `1.63`-`1.68` sui triangoli» *([[DECISIONE-SOLO-TRIANGOLI]]; [[PACCHETTO-K-NON-FERMO]]; il gradino prima e' `cbcb99c7`, la causa dello specchio `d26a7e1e`)*.
> ### **Solo misure in memoria: non sceglie niente.** ### **`leggi.yaml`, l'impronta `2e7f795d2a52fbe7`, la convenzione nel repo e il nucleo intatti; `soliton_simulator.py` al blob `b8c21049`**
> *(sha1-BYTE)*. ### **Importati, non copiati:** `_triangoli`, `_triangoli_bassa_energia`, `_triangoli_forza`, `_forza_da_cs`, `_zero_simmetrico`. ### **Lo specchio sul differenziale, con la
> semisomma contro `eta 0`** *(`doc/PATTERN_DI_PROVA.md`)*. ### **L'errore del guardiano `n.57`** *(i numeri di `a/a_H`)* ### **e' nel mandato.**

**LIVELLO:** `L2`, una misura *(piu' la correzione di uno strumento, in un commit a se')*.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica:** nessuna legge cambia.
2. **Il gradino:** ### **`(0)` perche' il pacchetto non e' fermo, e l'impulso iniziale** *(l'ipotesi di Luca)*; ### **`(A)` la scomposizione `F = R_t Q_b L` dagli spettri**; ### **`(B)` la conferma dinamica col
   pacchetto corretto.**
3. **Aggiunge un numero o una legge?** ### **No.** ### **I `k_max` del fit, la durata della rampa, le varianti del pacchetto sono SCELTE DI MISURA, dichiarate qui.** ### **Il fattore di larghezza
   `gamma` sotto e' DERIVATO** *(la media del gradiente sul pacchetto)*, ### **non tarato.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` per nodo solo nella scena, in memoria.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **la «velocita' della luce» che il modo a `K` vede nella sua relazione di Einstein e' quella del cono della camminata?**

## 1. IL RAGIONAMENTO PRELIMINARE *(che cosa credo, e che cosa NON so)*

- ### **LA SCOMPOSIZIONE** *(del guardiano)*: ### **`F = s omega'' (d omega/ds)/c^2 = R_t Q_b L`, con `R_t = s (d omega/ds)/omega`, `Q_b = omega omega''/v_b^2`, `L = (v_b/c)^2`: e' un'IDENTITA'.**
- ### ⚠ **UNA COSA CHE IL MANDATO NON DICE, e che conta:** ### **col fit `omega^2 = omega(0)^2 + v_b^2 k^2 + b k^4` a `omega(0)` FISSO, `omega''(0) = v_b^2/omega(0)` ESATTAMENTE** *(il termine `b`
  entra a `k^4`)*: ### **quindi `Q_b -> 1` per costruzione quando `k_max -> 0`; la sua informazione e' nel termine `k^4` e nella qualita' del fit, non nel suo valore a `k` piccolo.**
  ### **Allora `v_b = sqrt(omega(0) omega'')` e il fattore e' quasi tutto `R_t L`.**
- ### **I NUMERI DI `8781162c`/`cbcb99c7` LO DICONO GIA'** *(un conto a mano, che lo strumento rifa')*: ### **a `eps 0, s 0.05`: `omega(0) = 0.0785`, `omega''_cart = 0.0196`: `v_b = 0.0392 = 0.784 s`**,
  ### **contro `v_max = 0.599 s` e `v_fit = 0.522 s`.** ### **Quindi `L(v_max) = (0.784/0.599)^2 = 1.71` e `L(v_fit) = 2.26`: ### **il fattore e' `L`, e `v_b` SUPERA il cono.** ### **E' il contrario
  della previsione del guardiano** *(«`L ~ 1/1.37`»)*: ### **`v_b > v_max`, non `<`.**
- ### **IL PACCHETTO NON FERMO:** ### **sul toro `A` credo che venga dalla COSTRUZIONE** *(`u_K` per tutto il pacchetto: le componenti a `K + q` hanno un pezzo sulle ALTRE bande, che batte)*; ### **sul
  toro `B` dalla deformazione trigonale** *(una velocita' media vera)* ### **piu' un difetto della MISURA:** ### **il baricentro CIRCOLARE sente il terzo cumulante di un pacchetto che si deforma.**
- ### **LO SCARTO DI `a_mis/a_H` DA `1`** *(`0.95`-`0.97`)*: ### **credo che sia la LARGHEZZA:** ### **la forza e' `-dV/dx` con `cs ~ cos(2 pi x/Lx)`, e mediata su una densita' gaussiana di larghezza `sigma`
  vale `F(x0) exp(-(2 pi sigma/Lx)^2/2)`**; ### **con `sigma = W/sqrt2`** *(la densita' di `G^2`)* ### **e `W = Lx/16`: `gamma = exp(-(2 pi/(16 sqrt2))^2/2) = 0.962`, lo stesso a ogni `Lx`.** ### **E il pacchetto si
  allarga nel tempo: `gamma(t)` cala.** ### **L'impulso iniziale** *(l'ipotesi di Luca)* ### **non lo credo responsabile di questo scarto.**
- ### **NON SO:** ### **quale delle velocita' sia «la luce» del modello** *(nessuna definizione di luce nel modello: `LUCE-VINCOLO-LAMPI-GAMMA`)*; ### **il residuo di `a_mis/a_H` dopo la larghezza.**

## 2. VISTO IN MEMORIA, prima di scrivere il metodo *(i numeri li ristampa lo strumento)*

- ### **Toro `A`, `eps 0, s0 0.1`:** ### **col pacchetto di BANDA** *(gli stati di Bloch della banda a ogni `k`)* ### **e il baricentro LINEARE: `v0 = 4e-16`, `a(eta 0) = 3e-18`** ### **-- FERMO;** ### **col pacchetto
  di `cbcb99c7`: `v0 = -6.9e-7`, `a(eta 0)/differenziale = 0.75%`-`1.75%`.**
- ### **Toro `B`:** ### **col baricentro circolare anche il pacchetto di banda ha `a(eta 0) = 2.6e-6`; col LINEARE `3.9e-10`** *(lo `0.03%` del segnale)*; ### **la deriva `v0 = 1.8e-3` RESTA** *(fisica)*.
- ### **La larghezza:** ### **`gamma0` misurato `0.9622` = la formula `0.9622`;** ### **`a_mis/(a_H <gamma(t)>)`: `0.983`-`0.997` col brusco, `0.984`-`0.992` col graduale -- UGUALI**, ### **mentre `a_mis/a_H` grezzo
  cala col graduale** *(`0.946 -> 0.919`: si misura piu' tardi, col pacchetto piu' largo)*.

## 3. IL METODO

### **PARTE 0** *(il toro `A` e il `B`, `Lx 96`; `eps` in `(0, 0.5)`, `s0` in `(0.1, 0.5)`, le due bande; zero simmetrico)*
- ### **LE VARIANTI** *(a `eta 0` e `+-1e-3`)*: ### **`(base)` il pacchetto di `cbcb99c7`, baricentro circolare; `(centro)` centrato al centro di un triangolo** *(`x0 + 2/3` in `m1`: il baricentro del
  triangolo `(0,0)`, `(1,0)`, `(1,1)` lungo il gradiente)*; ### **`(2W)` largo il doppio; `(lineare)` il baricentro lineare; `(banda)` il pacchetto di banda, baricentro lineare.** ### **LA SIMMETRIA DI `120`
  GRADI DELL'INVILUPPO: NON SI APPLICA** *(sui tori a striscia l'inviluppo dipende solo da `m1`, e la rotazione non e' una simmetria del toro)*: ### **lo dichiaro invece di inventare una variante.**
  ### **LA PORTANTE:** ### **`|e^{i K.T} - 1|` per i due periodi `T` di ciascun toro.**
- ### **IL PACCHETTO DI BANDA** *(la correzione)*: ### **`psi = sum_q g(q) e^{i (K + q).r} u(q)`, `g` la trasformata dell'inviluppo, `u(q) = P_banda(q) u_K/|.|`** *(`P_banda` il proiettore sui due vettori della
  banda a `K + q`, seguita per sovrapposizione da `q = 0`)*; ### **`A(k)` a un `k` qualunque dai blocchi in spazio reale** *(la camminata arriva a `+-2` celle)*.
- ### **IL TREMOLIO DI DIRAC** *(l'ipotesi di Luca, `a`)*: ### **la frazione di norma sull'ALTRA banda della coppia e sul resto, a `t = 0` e alla fine** *(proiezione in `k`)*; ### **il periodo del residuo
  del fit** *(il picco della trasformata)* ### **contro `2 pi/salto` e `2 pi/delta_min`; il fit con un termine oscillante a `Omega = salto` e a `Omega = delta_min`, e quanto cambia `a`.**
- ### **L'AVVIO BRUSCO CONTRO IL GRADUALE** *(l'ipotesi di Luca, `b`)*: ### **`eta(t) = eta min(1, t/T_r)`, `T_r = 10 x 2 pi/delta_min`** *(dieci battimenti: piu' lungo del tremolio)*, ### **il fit
  sui `T` tick dopo la rampa;** ### **`a_mis/a_H` e `a_mis/(a_H <gamma(t)>)` nei due casi;** ### **`a_H/a_RG` e' dagli spettri: invariato per costruzione, e lo si stampa.**
- ### **`gamma(t) = exp(-(2 pi/Lx)^2 var(t)/2)`, `var(t)` la varianza LINEARE della densita' in `m1` a ogni tick; `<gamma>` la media sul tratto del fit.**

### **PARTE A** *(dagli spettri, zero simmetrico; `eps` in `(0, 0.5)`, `s` in `(0.02, 0.05, 0.1, 0.2, 0.3, 0.5)`, le due bande della coppia a `K`)*
- ### **`omega(0)`, `d omega/ds`, `omega''`, l'anisotropia: `_triangoli_forza.modo`** *(gli stessi di `cbcb99c7`)*; ### **`omega(0)` anche dalla fase continua** *(`omega_cont + pi s`: un controllo di
  servizio)*.
- ### **IL FIT IPERBOLICO:** ### **lungo la normale ad `a2` da `K`** *(`k = q 2/sqrt3`)*, ### **`omega^2 - omega(0)^2 = v_b^2 k^2 + b k^4` ai minimi quadrati, `k <= k_max`, `k_max` in `(0.1, 0.3)`** *(due, per
  la stabilita')*, ### **`200` punti; la qualita': il residuo relativo massimo.** ### **`A(k)` dai blocchi, la banda seguita per fase.**
- ### **LE VELOCITA' CANDIDATE:** ### **`v_max`** *(`_triangoli_forza.v_max`, ogni `s`)*; ### **`v_fronte` alle tre soglie** *(da `cbcb99c7` dove c'e', nuove a `s 0.02, 0.2`)*; ### **`v_ramo`: la
  velocita' di gruppo massima DEL RAMO lungo la stessa linea, fino al bordo della zona**; ### **`v_fit`** *(`cbcb99c7`)*; ### **`v_b`.**
- ### **`R_t`, `Q_b`, `L(c)` per ogni `c`, il prodotto, `F(c)`; il limite a `s -> 0`: lineare dai due `s` piu' piccoli, quadratica dai tre.**

### **PARTE B** *(toro `A`, `eps 0`, `s0` in `(0.05, 0.1, 0.3)`, `eta` in `(0, +-1e-3, +-1e-2)`, `Lx` in `(96, 192)`, zero simmetrico, il pacchetto di banda, il baricentro lineare, l'avvio
brusco)*: ### **il differenziale, `a/a_H`, `a/(a_H <gamma>)`, `a/a_RG` per ogni `c`, la semisomma contro `eta 0`.** ### **L'avvio graduale non serve: la parte `0` lo mostra equivalente una volta
tolta la larghezza** *(visto in memoria; se la corsa lo smentisce, lo scrivo)*.

## 4. LE PREVISIONI *(prima dei numeri dello strumento)*

- ### **`R_t` entro `0.01` da `1` a `s <= 0.1`** *(`E0 = omega/s` quasi costante: `1.5696`, `1.5659` a `s 0.05, 0.1`)*.
- ### **`Q_b` entro `0.05` da `1` a `s <= 0.1`, piu' vicino a `k_max` piccolo** *(per costruzione: l'informazione e' in `b`)*.
- ### **`L(v_max) ~ 1.7`, `L(v_fit) ~ 2.26`: il fattore e' `L`, `v_b ~ 1.3 v_max`; `F(v_b) = R_t Q_b ~ 1`: il terzo PUO'-FALLIRE PASSA.**
- ### **`v_ramo`: fra `v_fit` e `v_max`** *(non la prevedo meglio)*.
- ### **PARTE 0: il pacchetto di banda col baricentro lineare e' fermo** *(il DEVE della parte `B` PASSA)*; ### **l'avvio graduale NON porta `a_mis/a_H` entro `0.02` da `1`** *(il quarto PUO'-FALLIRE
  FALLISCE)*: ### **porta solo un pacchetto piu' largo; con `<gamma>` brusco e graduale coincidono.**
- ### **PARTE B: `a/(a_H <gamma>)` fra `0.98` e `1.00`.**

## 5. I CRITERI, FISSATI ORA *(dal mandato; la portata dove il mandato non la dice)*

- ### **DEVE PASSARE: `F = R_t Q_b L` entro `1e-9` relativo, ogni riga e ogni `c`.**
- ### **DEVE PASSARE: a `s 0.3, 0.5`, `eps 0`: `F(v_max)` e `F(v_fit)` = gli `a_H/a_RG` simmetrici di `cbcb99c7` entro `1e-6` relativo** *(le due bande)*.
- ### **DEVE PASSARE: parte `B`, il pacchetto corretto: `|a(eta 0)|` sotto l'`1%` del differenziale a `eta 1e-3`, ogni `s0`, banda, `Lx`** *(e la parte `0` lo stesso sui due tori)*.
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«`v_fit` e `v_max` coincidono entro l'`1%` a `s 0.3`»** *(`eps 0`, le due bande; la chiave: tutte e due finite e positive)*.
- ### **PUO' FALLIRE: `R_t` entro `0.01` da `1` a `s <= 0.1`** *(ogni `eps`, banda)*.
- ### **PUO' FALLIRE: `Q_b` entro `0.05` da `1` a `s <= 0.1`** *(col `k_max` piccolo)*.
- ### **PUO' FALLIRE: con `c = v_b`, `F` entro `0.05` da `1` a `s <= 0.1`.**
- ### **PUO' FALLIRE: parte `0`, con l'avvio graduale `a_mis/a_H` entro `0.02` da `1`** *(il pacchetto di banda, toro `A`)*, ### **mentre `a_H/a_RG` resta invariato.**
- ### **DI SERVIZIO: `omega(0)` principale = continua `+ pi s` entro `1e-9`; `v_max` a `s 0.3` = quella di `cbcb99c7` al bit; la portante periodica sui tori entro `1e-12`.**
- ### **IL VERDETTO DI FISICA: le tabelle dei tre fattori, il loro limite, il confronto brusco/graduale.** ### **A parte: tre righe di lettura; una sull'impulso iniziale; una su quale fattore porta il
  `1.63`-`1.68`; una sulla «velocita' della luce»** *(informazione per Luca, non una scelta)*.

### 📝 **ANNOTAZIONE 1** *(prima della corsa, nel commit dello strumento)*: ### **la prova a vuoto ridotta** *(`Lx 48`, `eps 0`, `s0 0.5`; `s` in `(0.05, 0.1, 0.3)`; il `txt` negli
appunti)* ### **ha trovato UN mio difetto, corretto nel commit della correzione:** ### **in `frazioni()` la riga della striscia sul toro `A` e' `LY/3`, non `2 LY/3`** *(le frazioni uscivano tutte
«resto»)*. ### **E due cose che non sono difetti, e le dichiaro:** ### **`(a)` il toro `B` a `Lx 48` ha `W = 3`: la deformazione trigonale cresce come `1/W^2`** *(`v0 = 8e-2`)*: ### **la corsa e' a
`Lx 96`, come in memoria**; ### **`(b)` il tremolio del pacchetto di `cbcb99c7` ha il periodo del BATTIMENTO col livello piatto** *(`8.8` contro `2 pi/delta_min = 8.7`)*, ### **non quello della coppia**
*(`2 pi/salto = 4.3`)*. ### **I NUMERI VISTI** *(non li uso; le previsioni restano)*: ### **`R_t = 0.998`, `Q_b = 1.0002`, `v_b/v_max = 1.31`, `F(v_b) = 0.999` a `s 0.05`; l'identita' `4.3e-16`.**

## 6. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. la correzione dello strumento in `csv/_triangoli_forza.py` *(il pacchetto di banda, il baricentro lineare, la rampa, `gamma(t)`: funzioni NUOVE, `corsa()` di `cbcb99c7` intatta)*, l'inventario;
3. `csv/_triangoli_fattore.py` e l'inventario, committati prima dei numeri;
4. la corsa, il referto, la relazione, la sezione `7`; ### **la voce `PACCHETTO-K-NON-FERMO` chiusa se la parte `0` la risolve.**

## 7. I RISULTATI *(scritti dopo la corsa, sotto)*

> **La corsa:** ### **strumento `csv/_triangoli_fattore.py` sha1-BYTE `577c349a`; la correzione del pacchetto in `63f3ffa6`; referto `doc/referti_l2/triangoli_fattore.txt` sha1-BYTE `a0efff1d`,
> `.jsonl` `73d27af8`.** ### **Le tabelle sono GENERATE dal `.jsonl`.** ### **`11` controlli su `12`: fallisce solo il PUO'-FALLIRE dell'avvio graduale, come avevo previsto.**

### 7.0 I CONTROLLI

| criterio | esito | il numero |
|---|---|---|
| di servizio: la portante periodica; `omega(0)` principale = continua `+ pi s`; `v_max` a `s 0.3` = `cbcb99c7` al bit | **PASSA** | `7.8e-15`; `1.6e-15`; al bit |
| DEVE: la prova della correzione, il pacchetto di banda, `|a(eta 0)|` sotto l'`1%` del differenziale, i due tori | **PASSA** | il peggiore `1.07e-3` *(toro `B`)* |
| DEVE: `F = R_t Q_b L` entro `1e-9` | **PASSA** | `5.3e-16` |
| DEVE: `F(v_max)`, `F(v_fit)` = `cbcb99c7` a `s 0.3, 0.5`, `eps 0` | **PASSA** | `0.0` *(`8` valori)* |
| DEVE: parte `B`, `|a(eta 0)|` sotto l'`1%` | **PASSA** | il peggiore `2.0e-11` |
| DEVE FALLIRE: `v_fit` = `v_max` entro l'`1%` a `s 0.3` | **fallisce, come deve** | `v_fit/v_max = 0.8568` |
| PUO': `R_t` entro `0.01` da `1` a `s <= 0.1` | **PASSA** | da `0.99304` a `0.99981` |
| PUO': `Q_b` entro `0.05` da `1` a `s <= 0.1` | **PASSA** | `1.00014`-`1.00016` |
| PUO': `F(v_b)` entro `0.05` da `1` a `s <= 0.1` | **PASSA** | da `0.99318` a `0.99994` |
| PUO': l'avvio graduale porta `a_mis/a_H` entro `0.02` da `1` | ### **FALLISCE** *(previsto)* | `0.9167`-`0.9262` *(col fattore di larghezza: `0.9840`-`0.9872`)* |

### 7.1 PARTE 0 -- IL PACCHETTO NON FERMO *(`Lx 96`, `eta 1e-3`, zero simmetrico; `dif` il differenziale; `<g>` la media di `gamma(t)`)*

| toro | `eps` | `s0` | banda | variante | frazioni *(banda, altra, resto)* | `v0` | `a(eta 0)/dif` | periodo del residuo *(`2pi/salto`, `2pi/delta_min`)* | `dif/a_H` | `dif/(a_H <g>)` | graduale: `dif/a_H`, `dif/(a_H <g>)` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | `0` | `0.1` | `0` | base | `0.9970` `1.2e-06` `3.0e-03` | `-6.4e-07` | `+7.1e-03` | `40.3` *(`20.1`, `40.1`)* | `0.9506` | `0.9930` | `0.9359`, `1.0028` |
| A | `0` | `0.1` | `0` | centro | `0.9970` `1.2e-06` `3.0e-03` | `-6.4e-07` | `+7.1e-03` | `40.3` *(`20.1`, `40.1`)* | `0.9487` | `0.9911` | -- |
| A | `0` | `0.1` | `0` | 2W | `0.9991` `5.3e-07` `9.3e-04` | `+2.3e-07` | `+1.3e-01` | `40.3` *(`20.1`, `40.1`)* | `0.8977` | `1.0467` | -- |
| A | `0` | `0.1` | `0` | lineare | `0.9970` `1.2e-06` `3.0e-03` | `-6.9e-07` | `+7.5e-03` | `40.3` *(`20.1`, `40.1`)* | `0.9462` | `0.9885` | -- |
| A | `0` | `0.1` | `0` | banda | `1.0000` `2.3e-30` `-6.7e-16` | `-4.0e-16` | `+5.3e-12` | `403.0` *(`20.1`, `40.1`)* | `0.9416` | `0.9833` | `0.9186`, `0.9840` |
| A | `0` | `0.1` | `1` | base | `0.9939` `1.1e-05` `6.1e-03` | `-1.5e-06` | `+1.7e-02` | `40.3` *(`20.1`, `40.1`)* | `0.9565` | `1.0002` | `0.9403`, `1.0082` |
| A | `0` | `0.1` | `1` | centro | `0.9939` `1.1e-05` `6.1e-03` | `-1.5e-06` | `+1.7e-02` | `40.3` *(`20.1`, `40.1`)* | `0.9547` | `0.9983` | -- |
| A | `0` | `0.1` | `1` | 2W | `0.9982` `7.2e-06` `1.8e-03` | `+3.9e-08` | `+1.2e-01` | `40.3` *(`20.1`, `40.1`)* | `0.9039` | `1.0550` | -- |
| A | `0` | `0.1` | `1` | lineare | `0.9939` `1.1e-05` `6.1e-03` | `-1.6e-06` | `+1.8e-02` | `40.3` *(`20.1`, `40.1`)* | `0.9530` | `0.9965` | -- |
| A | `0` | `0.1` | `1` | banda | `1.0000` `1.9e-30` `-6.7e-16` | `-4.9e-16` | `+6.1e-12` | `403.0` *(`20.1`, `40.1`)* | `0.9427` | `0.9848` | `0.9195`, `0.9854` |
| A | `0` | `0.5` | `0` | base | `0.9973` `5.0e-07` `2.7e-03` | `-2.4e-06` | `+5.3e-03` | `8.8` *(`4.3`, `8.7`)* | `0.9512` | `0.9940` | `0.9272`, `0.9960` |
| A | `0` | `0.5` | `0` | centro | `0.9973` `5.0e-07` `2.7e-03` | `-2.4e-06` | `+5.3e-03` | `8.8` *(`4.3`, `8.7`)* | `0.9494` | `0.9921` | -- |
| A | `0` | `0.5` | `0` | 2W | `0.9992` `1.6e-07` `8.3e-04` | `+1.8e-06` | `+1.7e-01` | `8.8` *(`4.3`, `8.7`)* | `0.8971` | `1.0461` | -- |
| A | `0` | `0.5` | `0` | lineare | `0.9973` `5.0e-07` `2.7e-03` | `-2.6e-06` | `+5.5e-03` | `8.8` *(`4.3`, `8.7`)* | `0.9467` | `0.9893` | -- |
| A | `0` | `0.5` | `0` | banda | `1.0000` `3.0e-31` `-2.2e-16` | `-2.9e-14` | `+9.4e-11` | `88.0` *(`4.3`, `8.7`)* | `0.9420` | `0.9840` | `0.9167`, `0.9846` |
| A | `0` | `0.5` | `1` | base | `0.9936` `1.2e-05` `6.4e-03` | `-1.2e-05` | `+3.1e-02` | `8.8` *(`4.3`, `8.7`)* | `0.9558` | `0.9999` | `0.9390`, `1.0094` |
| A | `0` | `0.5` | `1` | centro | `0.9936` `1.2e-05` `6.4e-03` | `-1.2e-05` | `+3.1e-02` | `8.8` *(`4.3`, `8.7`)* | `0.9540` | `0.9980` | -- |
| A | `0` | `0.5` | `1` | 2W | `0.9981` `7.0e-06` `1.9e-03` | `-4.3e-07` | `+1.5e-01` | `8.8` *(`4.3`, `8.7`)* | `0.9038` | `1.0550` | -- |
| A | `0` | `0.5` | `1` | lineare | `0.9936` `1.2e-05` `6.4e-03` | `-1.2e-05` | `+3.2e-02` | `8.8` *(`4.3`, `8.7`)* | `0.9521` | `0.9961` | -- |
| A | `0` | `0.5` | `1` | banda | `1.0000` `6.6e-31` `0.0e+00` | `-3.5e-14` | `+1.1e-10` | `88.0` *(`4.3`, `8.7`)* | `0.9432` | `0.9858` | `0.9179`, `0.9864` |
| A | `0.5` | `0.1` | `0` | base | `0.9971` `1.3e-04` `2.7e-03` | `-2.6e-07` | `+2.5e-03` | `36.5` *(`19.1`, `39.9`)* | `0.9533` | `0.9954` | `0.9444`, `1.0088` |
| A | `0.5` | `0.1` | `0` | centro | `0.9971` `1.3e-04` `2.7e-03` | `-2.6e-07` | `+2.5e-03` | `36.5` *(`19.1`, `39.9`)* | `0.9515` | `0.9935` | -- |
| A | `0.5` | `0.1` | `0` | 2W | `0.9991` `3.8e-05` `8.3e-04` | `+2.6e-07` | `+1.2e-01` | `36.5` *(`19.1`, `39.9`)* | `0.8986` | `1.0476` | -- |
| A | `0.5` | `0.1` | `0` | lineare | `0.9971` `1.3e-04` `2.7e-03` | `-2.9e-07` | `+2.6e-03` | `36.5` *(`19.1`, `39.9`)* | `0.9491` | `0.9911` | -- |
| A | `0.5` | `0.1` | `0` | banda | `1.0000` `5.3e-30` `-8.9e-16` | `-9.0e-17` | `+1.3e-12` | `401.0` *(`19.1`, `39.9`)* | `0.9430` | `0.9842` | `0.9222`, `0.9849` |
| A | `0.5` | `0.1` | `1` | base | `0.9944` `1.3e-04` `5.4e-03` | `-1.6e-06` | `+1.8e-02` | `40.3` *(`19.1`, `40.2`)* | `0.9569` | `1.0000` | `0.9420`, `1.0072` |
| A | `0.5` | `0.1` | `1` | centro | `0.9944` `1.3e-04` `5.4e-03` | `-1.6e-06` | `+1.8e-02` | `40.3` *(`19.1`, `40.2`)* | `0.9551` | `0.9982` | -- |
| A | `0.5` | `0.1` | `1` | 2W | `0.9984` `4.1e-05` `1.6e-03` | `+1.0e-08` | `+1.1e-01` | `40.3` *(`19.1`, `40.2`)* | `0.9034` | `1.0541` | -- |
| A | `0.5` | `0.1` | `1` | lineare | `0.9944` `1.3e-04` `5.4e-03` | `-1.7e-06` | `+1.9e-02` | `40.3` *(`19.1`, `40.2`)* | `0.9534` | `0.9964` | -- |
| A | `0.5` | `0.1` | `1` | banda | `1.0000` `5.5e-30` `-4.4e-16` | `-1.5e-16` | `+1.8e-12` | `403.0` *(`19.1`, `40.2`)* | `0.9438` | `0.9856` | `0.9227`, `0.9861` |
| A | `0.5` | `0.5` | `0` | base | `0.9974` `1.9e-04` `2.4e-03` | `-6.4e-06` | `+2.0e-02` | `8.0` *(`4.1`, `7.8`)* | `0.9405` | `0.9815` | `0.9370`, `0.9974` |
| A | `0.5` | `0.5` | `0` | centro | `0.9974` `1.9e-04` `2.4e-03` | `-6.4e-06` | `+2.0e-02` | `8.0` *(`4.1`, `7.8`)* | `0.9388` | `0.9797` | -- |
| A | `0.5` | `0.5` | `0` | 2W | `0.9992` `5.8e-05` `7.4e-04` | `+1.9e-07` | `+1.5e-01` | `8.0` *(`4.1`, `7.8`)* | `0.8898` | `1.0371` | -- |
| A | `0.5` | `0.5` | `0` | lineare | `0.9974` `1.9e-04` `2.4e-03` | `-6.8e-06` | `+2.1e-02` | `8.0` *(`4.1`, `7.8`)* | `0.9358` | `0.9766` | -- |
| A | `0.5` | `0.5` | `0` | banda | `1.0000` `9.4e-31` `-4.4e-16` | `-8.8e-17` | `+4.6e-13` | `80.0` *(`4.1`, `7.8`)* | `0.9444` | `0.9852` | `0.9262`, `0.9857` |
| A | `0.5` | `0.5` | `1` | base | `0.9939` `1.3e-04` `5.9e-03` | `-8.5e-06` | `+5.7e-02` | `9.1` *(`4.1`, `8.9`)* | `0.9352` | `0.9780` | `0.9276`, `0.9959` |
| A | `0.5` | `0.5` | `1` | centro | `0.9939` `1.3e-04` `5.9e-03` | `-8.5e-06` | `+5.7e-02` | `9.1` *(`4.1`, `8.9`)* | `0.9335` | `0.9763` | -- |
| A | `0.5` | `0.5` | `1` | 2W | `0.9982` `3.9e-05` `1.7e-03` | `-1.4e-07` | `+1.6e-01` | `9.1` *(`4.1`, `8.9`)* | `0.8882` | `1.0366` | -- |
| A | `0.5` | `0.5` | `1` | lineare | `0.9939` `1.3e-04` `5.9e-03` | `-9.3e-06` | `+6.1e-02` | `9.1` *(`4.1`, `8.9`)* | `0.9302` | `0.9728` | -- |
| A | `0.5` | `0.5` | `1` | banda | `1.0000` `9.5e-31` `-6.7e-16` | `-2.9e-14` | `+9.4e-11` | `91.0` *(`4.1`, `8.9`)* | `0.9443` | `0.9867` | `0.9200`, `0.9872` |
| B | `0` | `0.1` | `0` | base | `0.9926` `2.5e-05` `7.4e-03` | `+2.0e-03` | `-1.8e+00` | `40.3` *(`20.1`, `40.1`)* | `0.9030` | `0.9751` | `1.0341`, `1.3827` |
| B | `0` | `0.1` | `0` | centro | `0.9926` `2.5e-05` `7.4e-03` | `+2.0e-03` | `-1.8e+00` | `40.3` *(`20.1`, `40.1`)* | `0.8994` | `0.9712` | -- |
| B | `0` | `0.1` | `0` | 2W | `0.9978` `2.8e-05` `2.1e-03` | `+5.4e-04` | `+1.1e-01` | `40.3` *(`20.1`, `40.1`)* | `0.8872` | `1.0447` | -- |
| B | `0` | `0.1` | `0` | lineare | `0.9926` `2.5e-05` `7.4e-03` | `+1.8e-03` | `-1.7e-02` | `40.3` *(`20.1`, `40.1`)* | `0.8810` | `0.9513` | -- |
| B | `0` | `0.1` | `0` | banda | `1.0000` `4.0e-30` `-2.2e-16` | `+1.8e-03` | `-2.8e-04` | `403.0` *(`20.1`, `40.1`)* | `0.8805` | `0.9504` | `0.7173`, `0.9629` |
| B | `0` | `0.1` | `1` | base | `0.9837` `1.1e-04` `1.6e-02` | `-2.0e-03` | `+1.8e+00` | `40.3` *(`20.1`, `40.1`)* | `0.9026` | `0.9762` | `0.9948`, `1.3240` |
| B | `0` | `0.1` | `1` | centro | `0.9837` `1.1e-04` `1.6e-02` | `-2.0e-03` | `+1.8e+00` | `40.3` *(`20.1`, `40.1`)* | `0.9010` | `0.9745` | -- |
| B | `0` | `0.1` | `1` | 2W | `0.9953` `4.7e-05` `4.6e-03` | `-5.2e-04` | `+3.6e-01` | `40.3` *(`20.1`, `40.1`)* | `0.8927` | `1.0551` | -- |
| B | `0` | `0.1` | `1` | lineare | `0.9837` `1.1e-04` `1.6e-02` | `-1.7e-03` | `+9.0e-02` | `40.3` *(`20.1`, `40.1`)* | `0.8858` | `0.9581` | -- |
| B | `0` | `0.1` | `1` | banda | `1.0000` `3.8e-30` `-4.4e-16` | `-1.8e-03` | `+2.0e-04` | `403.0` *(`20.1`, `40.1`)* | `0.8881` | `0.9597` | `0.7241`, `0.9723` |
| B | `0` | `0.5` | `0` | base | `0.9935` `1.6e-05` `6.5e-03` | `+9.9e-03` | `-2.4e+00` | `7.3` *(`4.3`, `8.7`)* | `0.9036` | `0.9789` | `1.0573`, `1.4461` |
| B | `0` | `0.5` | `0` | centro | `0.9935` `1.6e-05` `6.5e-03` | `+9.9e-03` | `-2.4e+00` | `7.3` *(`4.3`, `8.7`)* | `0.9000` | `0.9750` | -- |
| B | `0` | `0.5` | `0` | 2W | `0.9981` `2.2e-05` `1.9e-03` | `+2.6e-03` | `+1.2e-01` | `7.3` *(`4.3`, `8.7`)* | `0.8879` | `1.0462` | -- |
| B | `0` | `0.5` | `0` | lineare | `0.9935` `1.6e-05` `6.5e-03` | `+8.6e-03` | `-3.5e-02` | `7.3` *(`4.3`, `8.7`)* | `0.8790` | `0.9523` | -- |
| B | `0` | `0.5` | `0` | banda | `1.0000` `2.0e-30` `-2.2e-16` | `+8.7e-03` | `-1.1e-03` | `88.0` *(`4.3`, `8.7`)* | `0.8791` | `0.9521` | `0.6984`, `0.9590` |
| B | `0` | `0.5` | `1` | base | `0.9827` `1.1e-04` `1.7e-02` | `-9.6e-03` | `+2.4e+00` | `8.8` *(`4.3`, `8.7`)* | `0.9008` | `0.9778` | `1.0168`, `1.3826` |
| B | `0` | `0.5` | `1` | centro | `0.9827` `1.1e-04` `1.7e-02` | `-9.6e-03` | `+2.4e+00` | `8.8` *(`4.3`, `8.7`)* | `0.8992` | `0.9760` | -- |
| B | `0` | `0.5` | `1` | 2W | `0.9951` `3.7e-05` `4.9e-03` | `-2.5e-03` | `+4.5e-01` | `8.8` *(`4.3`, `8.7`)* | `0.8925` | `1.0561` | -- |
| B | `0` | `0.5` | `1` | lineare | `0.9827` `1.1e-04` `1.7e-02` | `-8.3e-03` | `+1.2e-01` | `8.8` *(`4.3`, `8.7`)* | `0.8831` | `0.9586` | -- |
| B | `0` | `0.5` | `1` | banda | `1.0000` `2.2e-30` `-4.4e-16` | `-8.7e-03` | `+7.6e-04` | `88.0` *(`4.3`, `8.7`)* | `0.8876` | `0.9627` | `0.7074`, `0.9720` |
| B | `0.5` | `0.1` | `0` | base | `0.9931` `3.8e-04` `6.5e-03` | `+1.9e-03` | `-1.5e+00` | `40.1` *(`19.1`, `39.9`)* | `0.9078` | `0.9768` | `1.0137`, `1.3236` |
| B | `0.5` | `0.1` | `0` | centro | `0.9931` `3.8e-04` `6.5e-03` | `+1.9e-03` | `-1.5e+00` | `40.1` *(`19.1`, `39.9`)* | `0.9040` | `0.9727` | -- |
| B | `0.5` | `0.1` | `0` | 2W | `0.9980` `1.3e-04` `1.9e-03` | `+5.1e-04` | `+1.2e-01` | `40.1` *(`19.1`, `39.9`)* | `0.8888` | `1.0454` | -- |
| B | `0.5` | `0.1` | `0` | lineare | `0.9931` `3.8e-04` `6.5e-03` | `+1.7e-03` | `-1.4e-02` | `40.1` *(`19.1`, `39.9`)* | `0.8883` | `0.9559` | -- |
| B | `0.5` | `0.1` | `0` | banda | `1.0000` `6.1e-30` `-4.4e-16` | `+1.7e-03` | `-1.1e-04` | `401.0` *(`19.1`, `39.9`)* | `0.8857` | `0.9525` | `0.7357`, `0.9635` |
| B | `0.5` | `0.1` | `1` | base | `0.9849` `4.4e-04` `1.5e-02` | `-1.9e-03` | `+1.6e+00` | `40.3` *(`19.1`, `40.2`)* | `0.9054` | `0.9761` | `0.9766`, `1.2733` |
| B | `0.5` | `0.1` | `1` | centro | `0.9849` `4.4e-04` `1.5e-02` | `-1.9e-03` | `+1.6e+00` | `40.3` *(`19.1`, `40.2`)* | `0.9040` | `0.9745` | -- |
| B | `0.5` | `0.1` | `1` | 2W | `0.9957` `1.4e-04` `4.2e-03` | `-4.9e-04` | `+3.2e-01` | `40.3` *(`19.1`, `40.2`)* | `0.8930` | `1.0541` | -- |
| B | `0.5` | `0.1` | `1` | lineare | `0.9849` `4.4e-04` `1.5e-02` | `-1.6e-03` | `+8.4e-02` | `40.3` *(`19.1`, `40.2`)* | `0.8906` | `0.9600` | -- |
| B | `0.5` | `0.1` | `1` | banda | `1.0000` `6.3e-30` `-4.4e-16` | `-1.7e-03` | `+8.6e-05` | `403.0` *(`19.1`, `40.2`)* | `0.8926` | `0.9613` | `0.7400`, `0.9717` |
| B | `0.5` | `0.5` | `0` | base | `0.9939` `4.7e-04` `5.6e-03` | `+8.7e-03` | `-1.7e+00` | `7.3` *(`4.1`, `7.8`)* | `0.8960` | `0.9599` | `0.9770`, `1.2400` |
| B | `0.5` | `0.5` | `0` | centro | `0.9939` `4.7e-04` `5.6e-03` | `+8.7e-03` | `-1.7e+00` | `7.3` *(`4.1`, `7.8`)* | `0.8922` | `0.9559` | -- |
| B | `0.5` | `0.5` | `0` | 2W | `0.9982` `1.5e-04` `1.6e-03` | `+2.4e-03` | `+1.4e-01` | `7.3` *(`4.1`, `7.8`)* | `0.8807` | `1.0344` | -- |
| B | `0.5` | `0.5` | `0` | lineare | `0.9939` `4.7e-04` `5.6e-03` | `+7.8e-03` | `-1.9e-02` | `8.0` *(`4.1`, `7.8`)* | `0.8795` | `0.9423` | -- |
| B | `0.5` | `0.5` | `0` | banda | `1.0000` `2.2e-30` `-4.4e-16` | `+7.9e-03` | `-4.1e-05` | `80.0` *(`4.1`, `7.8`)* | `0.8920` | `0.9552` | `0.7570`, `0.9628` |
| B | `0.5` | `0.5` | `1` | base | `0.9837` `5.3e-04` `1.6e-02` | `-9.2e-03` | `+2.3e+00` | `8.3` *(`4.1`, `8.9`)* | `0.8901` | `0.9645` | `1.0055`, `1.3541` |
| B | `0.5` | `0.5` | `1` | centro | `0.9837` `5.3e-04` `1.6e-02` | `-9.2e-03` | `+2.3e+00` | `8.3` *(`4.1`, `8.9`)* | `0.8887` | `0.9630` | -- |
| B | `0.5` | `0.5` | `1` | 2W | `0.9953` `1.6e-04` `4.5e-03` | `-2.4e-03` | `+4.3e-01` | `9.1` *(`4.1`, `8.9`)* | `0.8826` | `1.0436` | -- |
| B | `0.5` | `0.5` | `1` | lineare | `0.9837` `5.3e-04` `1.6e-02` | `-8.0e-03` | `+1.1e-01` | `8.3` *(`4.1`, `8.9`)* | `0.8739` | `0.9469` | -- |
| B | `0.5` | `0.5` | `1` | banda | `1.0000` `2.4e-30` `-2.2e-16` | `-8.3e-03` | `+6.0e-04` | `91.0` *(`4.1`, `8.9`)* | `0.8909` | `0.9646` | `0.7148`, `0.9713` |

### 7.2 PARTE A -- I TRE FATTORI *(zero simmetrico; `L` e `F` per `v_max`, `v_fit`, `v_b`, `v_ramo` e il fronte a `1e-6`; le velocita' divise per `s`)*

| `eps` | `s` | banda | `R_t` | `Q_b` *(k_max `0.1`, `0.3`)* | `b` | `v_b/s` | `v_max/s` | `v_fit/s` | `v_ramo/s` | `v_fronte(1e-6)/s` | `L(v_max)` | `F(v_max)` | `L(v_fit)` | `F(v_fit)` | `F(v_b)` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.02` | `0` | `0.99975` | `1.00016` `1.00016` | `-1.54e-05` | `0.7853` | `0.5985` | `0.5215` | `0.3588` | `1.3944` | `1.7216` | `1.7215` | `2.2679` | `2.2677` | `0.99991` |
| `0` | `0.02` | `1` | `0.99975` | `1.00016` `1.00016` | `-1.54e-05` | `0.7853` | `0.5985` | `0.5215` | `0.3588` | `1.3944` | `1.7216` | `1.7215` | `2.2679` | `2.2677` | `0.99991` |
| `0` | `0.05` | `0` | `0.99846` | `1.00016` `1.00016` | `-9.61e-05` | `0.7850` | `0.5989` | `0.5216` | `0.3589` | `0.7678` | `1.7182` | `1.7159` | `2.2652` | `2.2620` | `0.99861` |
| `0` | `0.05` | `1` | `0.99846` | `1.00016` `1.00016` | `-9.61e-05` | `0.7850` | `0.5989` | `0.5216` | `0.3589` | `0.7678` | `1.7182` | `1.7159` | `2.2652` | `2.2620` | `0.99861` |
| `0` | `0.1` | `0` | `0.99379` | `1.00016` `1.00016` | `-3.81e-04` | `0.7838` | `0.6000` | `0.5219` | `0.3590` | `0.7849` | `1.7062` | `1.6959` | `2.2555` | `2.2419` | `0.99395` |
| `0` | `0.1` | `1` | `0.99379` | `1.00016` `1.00016` | `-3.81e-04` | `0.7838` | `0.6000` | `0.5219` | `0.3590` | `0.7849` | `1.7062` | `1.6959` | `2.2555` | `2.2419` | `0.99395` |
| `0` | `0.2` | `0` | `0.97471` | `1.00015` `1.00016` | `-1.47e-03` | `0.7788` | `0.6046` | `0.5230` | `0.3596` | `0.6864` | `1.6590` | `1.6173` | `2.2177` | `2.1619` | `0.97487` |
| `0` | `0.2` | `1` | `0.97471` | `1.00015` `1.00016` | `-1.47e-03` | `0.7788` | `0.6046` | `0.5230` | `0.3596` | `0.6864` | `1.6590` | `1.6173` | `2.2177` | `2.1619` | `0.97487` |
| `0` | `0.3` | `0` | `0.94137` | `1.00015` `1.00016` | `-3.09e-03` | `0.7701` | `0.6120` | `0.5243` | `0.3602` | `0.6685` | `1.5833` | `1.4907` | `2.1571` | `2.0309` | `0.94151` |
| `0` | `0.3` | `1` | `0.94137` | `1.00015` `1.00016` | `-3.09e-03` | `0.7701` | `0.6120` | `0.5243` | `0.3602` | `0.6685` | `1.5833` | `1.4907` | `2.1571` | `2.0309` | `0.94151` |
| `0` | `0.5` | `0` | `0.82147` | `1.00015` `1.00015` | `-6.92e-03` | `0.7391` | `0.6351` | `0.5246` | `0.3596` | `0.6827` | `1.3545` | `1.1128` | `1.9855` | `1.6313` | `0.82159` |
| `0` | `0.5` | `1` | `0.82147` | `1.00015` `1.00015` | `-6.92e-03` | `0.7391` | `0.6351` | `0.5246` | `0.3596` | `0.6827` | `1.3545` | `1.1128` | `1.9855` | `1.6313` | `0.82159` |
| `0.5` | `0.02` | `0` | `0.99981` | `1.00014` `1.00014` | `-1.54e-05` | `0.7853` | `0.5851` | `0.5088` | `0.3475` | `0.9770` | `1.8016` | `1.8015` | `2.3820` | `2.3819` | `0.99994` |
| `0.5` | `0.02` | `1` | `0.99972` | `1.00014` `1.00014` | `-1.54e-05` | `0.7853` | `0.5851` | `0.5088` | `0.3475` | `0.9770` | `1.8015` | `1.8013` | `2.3819` | `2.3816` | `0.99986` |
| `0.5` | `0.05` | `0` | `0.99880` | `1.00014` `1.00014` | `-9.61e-05` | `0.7850` | `0.5854` | `0.5089` | `0.3475` | `0.7678` | `1.7981` | `1.7962` | `2.3797` | `2.3772` | `0.99893` |
| `0.5` | `0.05` | `1` | `0.99827` | `1.00014` `1.00014` | `-9.60e-05` | `0.7849` | `0.5854` | `0.5089` | `0.3475` | `0.7678` | `1.7979` | `1.7951` | `2.3789` | `2.3751` | `0.99841` |
| `0.5` | `0.1` | `0` | `0.99516` | `1.00014` `1.00014` | `-3.81e-04` | `0.7837` | `0.5864` | `0.5089` | `0.3474` | `0.7211` | `1.7859` | `1.7776` | `2.3715` | `2.3604` | `0.99530` |
| `0.5` | `0.1` | `1` | `0.99304` | `1.00014` `1.00014` | `-3.80e-04` | `0.7835` | `0.5864` | `0.5092` | `0.3476` | `0.7211` | `1.7851` | `1.7729` | `2.3680` | `2.3519` | `0.99318` |
| `0.5` | `0.2` | `0` | `0.98031` | `1.00013` `1.00014` | `-1.47e-03` | `0.7785` | `0.5905` | `0.5090` | `0.3471` | `0.6762` | `1.7382` | `1.7042` | `2.3394` | `2.2937` | `0.98045` |
| `0.5` | `0.2` | `1` | `0.97155` | `1.00013` `1.00014` | `-1.46e-03` | `0.7777` | `0.5905` | `0.5100` | `0.3479` | `0.6762` | `1.7348` | `1.6856` | `2.3255` | `2.2597` | `0.97168` |
| `0.5` | `0.3` | `0` | `0.95443` | `1.00013` `1.00014` | `-3.12e-03` | `0.7694` | `0.5969` | `0.5086` | `0.3463` | `0.6565` | `1.6619` | `1.5864` | `2.2884` | `2.1844` | `0.95456` |
| `0.5` | `0.3` | `1` | `0.93360` | `1.00013` `1.00013` | `-3.07e-03` | `0.7677` | `0.5969` | `0.5109` | `0.3482` | `0.6565` | `1.6542` | `1.5445` | `2.2573` | `2.1077` | `0.93372` |
| `0.5` | `0.5` | `0` | `0.86224` | `1.00013` `1.00013` | `-7.10e-03` | `0.7374` | `0.6166` | `0.5031` | `0.3408` | `0.6665` | `1.4302` | `1.2333` | `2.1483` | `1.8526` | `0.86234` |
| `0.5` | `0.5` | `1` | `0.79299` | `1.00012` `1.00012` | `-6.73e-03` | `0.7318` | `0.6166` | `0.5095` | `0.3462` | `0.6665` | `1.4083` | `1.1169` | `2.0624` | `1.6357` | `0.79308` |

### 7.3 IL LIMITE A `s -> 0` *(la lineare dai due `s` piu' piccoli, la quadratica dai tre; banda `0`)*

| `eps` | che | lineare | quadratica |
|---|---|---|---|
| `0` | R_t | `1.00062` | `0.99999` |
| `0` | Q_b | `1.00016` | `1.00016` |
| `0` | L(v_max) | `1.72387` | `1.72227` |
| `0` | L(v_fit) | `2.26971` | `2.26843` |
| `0` | F(v_max) | `1.72520` | `1.72255` |
| `0` | v_b/v_max | `1.31296` | `1.31235` |
| `0.5` | R_t | `1.00048` | `1.00000` |
| `0.5` | Q_b | `1.00014` | `1.00014` |
| `0.5` | L(v_max) | `1.80384` | `1.80222` |
| `0.5` | L(v_fit) | `2.38357` | `2.38248` |
| `0.5` | F(v_max) | `1.80495` | `1.80248` |
| `0.5` | v_b/v_max | `1.34307` | `1.34247` |

### 7.4 PARTE B -- LA CONFERMA DINAMICA *(toro `A`, `eps 0`, il pacchetto di banda, il baricentro lineare)*

| `s0` | `Lx` | banda | `eta` | `a(eta 0)/dif` | semisomma | `dif/a_H` | `dif/(a_H <g>)` | `dif/a_RG(v_b)` | `dif/a_RG(v_max)` | `dif/a_RG(v_fit)` | specchio grezzo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0.05` | `96` | `0` | `0.001` | `+4.5e-12` | `-4.2e-12` | `0.9417` | `0.9833` | `0.9404` | `1.6158` | `2.1301` | `0.0001` |
| `0.05` | `96` | `0` | `0.01` | `+4.5e-13` | `-4.2e-10` | `0.9411` | `0.9827` | `0.9398` | `1.6148` | `2.1288` | `0.0007` |
| `0.05` | `96` | `1` | `0.001` | `+5.2e-12` | `-5.9e-12` | `0.9426` | `0.9848` | `0.9413` | `1.6174` | `2.1323` | `0.0001` |
| `0.05` | `96` | `1` | `0.01` | `+5.2e-13` | `-5.9e-10` | `0.9421` | `0.9841` | `0.9408` | `1.6164` | `2.1310` | `0.0009` |
| `0.05` | `192` | `0` | `0.001` | `+5.1e-14` | `-7.5e-13` | `0.9575` | `0.9955` | `0.9562` | `1.6429` | `2.1659` | `0.0000` |
| `0.05` | `192` | `0` | `0.01` | `+5.1e-15` | `-7.5e-11` | `0.9573` | `0.9954` | `0.9560` | `1.6427` | `2.1656` | `0.0002` |
| `0.05` | `192` | `1` | `0.001` | `+4.7e-13` | `-1.2e-12` | `0.9578` | `0.9959` | `0.9564` | `1.6434` | `2.1665` | `0.0000` |
| `0.05` | `192` | `1` | `0.01` | `+4.7e-14` | `-1.2e-10` | `0.9576` | `0.9958` | `0.9563` | `1.6432` | `2.1662` | `0.0004` |
| `0.1` | `96` | `0` | `0.001` | `+5.3e-12` | `-1.6e-11` | `0.9416` | `0.9833` | `0.9359` | `1.5969` | `2.1110` | `0.0001` |
| `0.1` | `96` | `0` | `0.01` | `+5.3e-13` | `-1.6e-09` | `0.9411` | `0.9827` | `0.9354` | `1.5960` | `2.1098` | `0.0006` |
| `0.1` | `96` | `1` | `0.001` | `+6.1e-12` | `-2.3e-11` | `0.9427` | `0.9848` | `0.9370` | `1.5987` | `2.1133` | `0.0001` |
| `0.1` | `96` | `1` | `0.01` | `+6.1e-13` | `-2.3e-09` | `0.9421` | `0.9842` | `0.9364` | `1.5977` | `2.1121` | `0.0009` |
| `0.1` | `192` | `0` | `0.001` | `-2.1e-13` | `-2.9e-12` | `0.9574` | `0.9955` | `0.9516` | `1.6237` | `2.1465` | `0.0000` |
| `0.1` | `192` | `0` | `0.01` | `-2.1e-14` | `-2.9e-10` | `0.9573` | `0.9953` | `0.9515` | `1.6235` | `2.1462` | `0.0002` |
| `0.1` | `192` | `1` | `0.001` | `-1.5e-13` | `-4.7e-12` | `0.9578` | `0.9960` | `0.9520` | `1.6244` | `2.1473` | `0.0000` |
| `0.1` | `192` | `1` | `0.01` | `-1.5e-14` | `-4.7e-10` | `0.9577` | `0.9958` | `0.9519` | `1.6241` | `2.1470` | `0.0004` |
| `0.3` | `96` | `0` | `0.001` | `+1.7e-11` | `-1.1e-10` | `0.9419` | `0.9838` | `0.8868` | `1.4042` | `1.9130` | `0.0001` |
| `0.3` | `96` | `0` | `0.01` | `+1.7e-12` | `-1.1e-08` | `0.9414` | `0.9832` | `0.8864` | `1.4034` | `1.9119` | `0.0006` |
| `0.3` | `96` | `1` | `0.001` | `+2.0e-11` | `-1.7e-10` | `0.9429` | `0.9852` | `0.8877` | `1.4055` | `1.9148` | `0.0001` |
| `0.3` | `96` | `1` | `0.01` | `+2.0e-12` | `-1.7e-08` | `0.9424` | `0.9847` | `0.8872` | `1.4048` | `1.9138` | `0.0008` |
| `0.3` | `192` | `0` | `0.001` | `+4.3e-14` | `-1.9e-11` | `0.9578` | `0.9958` | `0.9018` | `1.4278` | `1.9452` | `0.0000` |
| `0.3` | `192` | `0` | `0.01` | `+4.3e-15` | `-1.9e-09` | `0.9576` | `0.9957` | `0.9016` | `1.4276` | `1.9449` | `0.0002` |
| `0.3` | `192` | `1` | `0.001` | `-1.3e-13` | `-3.4e-11` | `0.9580` | `0.9961` | `0.9019` | `1.4281` | `1.9455` | `0.0000` |
| `0.3` | `192` | `1` | `0.01` | `-1.3e-14` | `-3.4e-09` | `0.9578` | `0.9960` | `0.9018` | `1.4279` | `1.9452` | `0.0003` |

### 7.5 LA LETTURA *(tre righe)*

1. ### **IL FATTORE `1.63`-`1.68` E' `L`:** ### **`R_t -> 1.0000` e `Q_b = 1.00016`** *(per costruzione: l'informazione e' nel `b` piccolo e negativo)*, ### **mentre `L(v_max) -> 1.722`** *(`eps 0`; `1.802` a `eps 0.5`)*:
   ### **`v_b = sqrt(omega(0) omega'') = 0.785 s`, cioe' `1.31` volte `v_max = 0.599 s`.** ### **Con `c = v_b` il fattore torna `1`** *(`F(v_b) -> 1.0000`)*; ### **la dinamica lo conferma: `a/a_RG(v_b)` `0.956`-`0.958`
   a `Lx 192`, `s0 0.05`, e col fattore di larghezza `~1`.** ### **Il fattore NON viene dall'orologio** *(`R_t`)* ### **ne' dalla forma iperbolica** *(`Q_b`)*.
2. ### **LO SCARTO DI `a_mis/a_H` DA `1` E' LA LARGHEZZA, non l'impulso:** ### **il pacchetto di banda e quello di `cbcb99c7` danno lo stesso `a/a_H`** *(`0.94`-`0.96`)*; ### **col fattore di larghezza
   `<gamma(t)>`: `0.983`-`0.987` a `Lx 96`, `0.995`-`0.996` a `Lx 192`** *(parte `B`)*; ### **il graduale e il brusco coincidono una volta tolta la larghezza** *(`0.984`-`0.987` contro `0.983`-`0.987`)*. ### ⚠ **Col
   pacchetto largo il doppio la correzione ECCEDE** *(`1.04`-`1.06`)*: ### **il modello di `gamma` e' approssimato.**
3. ### **IL TORO `B` NON E' FERMO PER FISICA:** ### **col pacchetto di banda `v0` resta** *(`1.7e-3`-`8.7e-3`: la deformazione trigonale lungo `Gamma-K`)*; ### **l'`a(eta 0)` di `cbcb99c7` era del baricentro
   CIRCOLARE** *(`a0/dif` da `+-1.5` a `+-2.4` col circolare, `<= 1.1e-3` col lineare)*; ### **sul toro `B` il pacchetto di banda col fattore di larghezza da' `0.950`-`0.965`, contro `0.983`-`0.987` sul toro `A`: l'isotropia NON e' verificata lungo `Gamma-K`.**

### 7.6 CHE COSA SPIEGA L'IMPULSO INIZIALE *(l'ipotesi di Luca)*

### **Spiega il pacchetto NON FERMO del toro `A`:** ### **lo stato di partenza mette dallo `0.24%` allo `0.64%` della norma su ALTRI livelli** *(sull'altra banda della coppia solo da `5e-7` a `1.9e-4`)*, ### **e il
battimento col livello piu' vicino** *(il periodo del residuo e' `2 pi/delta_min`, `40.3` contro `40.1`; NON `2 pi/salto`, `20.1`)* ### **da' `v0` e `a(eta 0)`** *(dallo `0.25%` al `5.7%` del segnale)*; ### **il
pacchetto di banda lo toglie** *(`v0 <= 3.5e-14`, `a0/dif <= 1.1e-10`)*. ### **NON spiega lo scarto di `a_mis/a_H`** *(la larghezza)* ### **ne' il fattore `a_H/a_RG`** *(dagli spettri)*. ### **Il tremolio di Dirac DELLA
COPPIA e' trascurabile.**

### 7.7 QUALE FATTORE PORTA IL `1.63`-`1.68`

### **`L = (v_b/v_max)^2`:** ### **`1.722` nel limite** *(`F(v_max) -> 1.7226`)*; ### **`R_t` lo abbassa a `s` finito** *(`1.6173` a `s 0.2`, `1.4907` a `0.3`: e' il calo del `1.63`-`1.68` misurato con `s0`)*.

### 7.8 CHE COSA VUOL DIRE PER LA «VELOCITA' DELLA LUCE» *(informazione per Luca, non una scelta)*

### **Il modo massivo a `K` ha una relazione di Einstein `omega(0) omega'' = v_b^2` con `v_b = 1.31 v_max`** *(e `1.5 v_fit`, `2.2 v_ramo`)*: ### **nessun segnale della camminata viaggia a `v_b`.** ### **Rispetto al
cono della camminata, la particella e' «piu' leggera» di quanto la sua energia a riposo direbbe** *(`omega'' > v_max^2/omega(0)`)*: ### **e' un problema di LORENTZ** *(la dispersione non e' invariante rispetto al cono)*,
### **non di gravita': la gravita' segue Hamilton e, con la `c` del modo, il limite di Newton** *(`F(v_b) -> 1`)*. ### **Quale sia la «luce» del modello resta NON DEFINITO** *(`LUCE-VINCOLO-LAMPI-GAMMA`)*. ### ⚠ **Il fronte
a `1e-6` a `s 0.02` vale `1.39 s`: in `100` tick a `s` cosi' piccolo il fronte non e' una velocita'.**
