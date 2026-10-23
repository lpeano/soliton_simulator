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
