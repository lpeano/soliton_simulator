# I TRIANGOLI, SECONDO GRADINO: LA FORZA SUL MODO A K (IL TORO RETTANGOLARE, LA VELOCITA' DEL CONO, LA CORSA, L'UNIVERSALITA')

> **Il mandato:** di Luca, «I TRIANGOLI, SECONDO GRADINO -- LA FORZA SUL MODO A K» *([[DECISIONE-SOLO-TRIANGOLI]]; il primo gradino e' `8781162c`)*. ### **Solo misure in memoria:
> non sceglie niente.** ### **`leggi.yaml`, l'impronta `2e7f795d2a52fbe7`, la convenzione nel repo e il nucleo intatti; `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE; git `e96ca41a`)*.
> ### **Importati, non copiati:** `_triangoli` *(`toro_spostamenti`, `matrice_tick`, la scena)*, `_triangoli_bassa_energia` *(`matrice`, `curvatura`, `continua`)*, `_forza_da_cs`
> *(il pacchetto, il fit, la norma fuori: senza la parte sul quadrato)*, `_zero_simmetrico.convenzione_simmetrica`.

**LIVELLO:** `L2`, una misura *(piu' la parte `0`, due strumenti di servizio in `csv/_triangoli.py`)*.

### ⚠ **L'ORDINE DEI COMMIT:** ### **il mandato elenca «parte `0`; task history; script; referto»**; ### **`CLAUDE.md` par.`8` vuole il task history PRIMA di ogni codice, e prevale.** ### **L'ordine
qui: questo task history *(che progetta anche la parte `0`)*; la parte `0`; lo script; il referto.**

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica:** nessuna legge cambia.
2. **Il gradino:** ### **`(0)` gli strumenti** *(il toro rettangolare; `scarto_c6` sul cerchio)*; ### **`(A)` la velocita' del cono**; ### **`(B)` la corsa nel gradiente di `cs`**; ### **`(C)` la
   moneta e lo zero.**
3. **Aggiunge un numero o una legge?** ### **No.** ### **I lati dei tori, `W`, `x0`, `eta`, le soglie del fronte e la regola della durata sono SCELTE DI MISURA, dichiarate qui sotto.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` per nodo SOLO nella scena, in memoria** *(`mot.cs`, `mot.lambda_c = None`)*; ### **il segno della forza e' una delle domande.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **il modo massivo a `K` cade nel gradiente di `cs` come dice Hamilton, e con quale velocita' nel limite di Newton?**

## 1. PARTE 0 -- GLI STRUMENTI *(commit a se', prima delle misure)*

- **`_triangoli.scena_toro(griglia, lati, dtau, x)`**: ### **la scena su un toro con lati diversi lungo i due spostamenti di base** *(via `toro_spostamenti`)*; ### **`scena(griglia, lato,
  dtau, x)` diventa `scena_toro(griglia, (lato, lato), dtau, x)`.** ### **`dtau` scalare o per nodo.**
- **`_triangoli.scarto_c6` sul cerchio:** ### **gli autovalori a `k` e a `k` ruotato accoppiati con l'assegnamento ungherese sulla distanza nel piano complesso, lo scarto la fase
  relativa della coppia, avvolta** *(il difetto di `1e2437a9`: le fasi ordinate scambiano `-pi` e `+pi`)*.
- **`_forza_da_cs`, riordino senza cambiare i numeri:** ### **il pacchetto, il fit e la norma fuori escono da `corsa()` come funzioni** *(`pacchetto`, `fit_moto`, `norma_fuori`)*, ### **perche'
  la corsa sui triangoli le IMPORTI invece di copiarle.** ### **`corsa()` le chiama nello stesso ordine.**

### **I CONTROLLI DELLA PARTE 0** *(girano nello script della misura, sezione `0`; il codice di prima si legge con `git show 8781162c:<file>`, in memoria)*:
- ### **DEVE PASSARE:** ### **a lati uguali la scena nuova e' quella di prima AL BIT** *(i byte di OGNI attributo di `inc`, `mot`, `st`, `par`, triangoli e quadrato, lato `12`)*, ### **e
  `matrice_tick` uguale al bit; lo spettro a `k` uguali entro `1e-14`.**
- ### **DEVE PASSARE:** ### **`scarto_c6` nuovo uguale al vecchio entro `1e-14` dove il vecchio dava `< 1e-12`; a `s 0.5` il nuovo `< 1e-12`** *(il vecchio `~3.1`)*; ### **e il quadrato
  resta oltre la soglia del caso che deve fallire di `_triangoli`** *(`> 1e6 x 64 ulp x pi`)*.
- ### **DI SERVIZIO** *(il quadrato, esplicito, mai come risultato)*: ### **`_forza_da_cs.corsa()` dopo il riordino uguale al bit a quella di `8781162c`** *(un caso corto, `Q` dato)*.

### **VISTO IN MEMORIA, prima di scrivere questo** *(i numeri li ristampa lo strumento)*: ### **`51` attributi, nessuno diverso; la matrice uguale al bit; `scarto_c6` vecchio `1.30e-15`, nuovo
`1.50e-15`; a `s 0.5` vecchio `3.10`, nuovo `1.58e-15`.**

## 2. PARTE A -- LA VELOCITA' DEL CONO

- **`v_max`:** ### **la velocita' di gruppo massima su tutte le `12` bande della materia e tutta la zona** *(lato `48`, `2304` punti)*, ### **dal teorema di Hellmann-Feynman:** ### **`dA/dtheta_j`
  esatta dalla matrice in spazio reale** *(la camminata arriva a `+-2` celle)*; ### **per un livello semplice il gradiente cartesiano esatto, per un gruppo degenere gli autovalori della
  derivata proiettata su `61` direzioni.** ### **In archi per tick** *(la lunghezza del legame e' `1`)*. ### **Il blocco materia-vuoto e' nullo** *(verificato in memoria: `0.0`)*.
- **`v_fronte`:** ### **dalla dinamica:** ### **toro `128 x 128`, un impulso su un nodo** *(la sovrapposizione uniforme dei `12` complessi della materia)*, ### **`100` tick**; ### **il raggio
  cartesiano `r_thr(t)` oltre il quale resta meno di `thr` della norma**, ### **`v_fronte = (r(100) - r(50))/50`, a `thr` in `(1e-2, 1e-4, 1e-6)`: TUTTE E TRE riportate** *(il fronte di
  una camminata non e' netto: la soglia e' una scelta di misura, e lo dichiaro invece di sceglierne una)*.
- **`v_fit`:** ### **la `v` del fit della coppia a `K`** *(`_triangoli_bassa_energia.curvatura`, lungo `theta_1`)*, ### **in cartesiano `x sqrt3/2`** *(muoversi in `theta_1` a `theta_2` fermo e'
  muoversi lungo la normale ad `a2`)*.
- **`a_H/a_RG = s omega''_cart (d omega/ds) / v^2`** ### **con ciascuna velocita'**, ### **le due convenzioni, le due bande, accanto al valore di `8781162c`.**
- **`eps` in `(0, 0.5)`, `s` in `(0.05, 0.1, 0.3, 0.5)`.**
- ### **DI SERVIZIO:** ### **l'autovalore cartesiano della curvatura = `3/4 h11` entro `1e-3`** *(la conversione delle unita')*; ### **`a_H/a_RG` ricalcolato con `v_fit` = quello di `8781162c`
  entro `1e-6` relativo, dove `8781162c` aveva la coppia a `K`.**

## 3. PARTE B -- LA CORSA

- **IL TORO `A`:** ### **lati `(Lx, 6)` lungo `(a1, a2)`, `Lx` in `(96, 192)`;** ### **`cs = cs0 (1 + eta cos(2 pi m1/Lx))`**: ### **il gradiente e' NORMALE ad `a2`** *(a `30` gradi: normale a
  una famiglia di legami)*; ### **la distanza lungo il gradiente e' `f m1`, `f = sqrt3/2`.**
- **IL TORO `B`** *(l'isotropia)*: ### **la base `(u, w) = (a1, a2 - a1)`** *(primitiva: determinante `1`)*, ### **gli spostamenti `(1, 0)`, `(1, 1)`, `(2, 1)` con le stesse direzioni `0`, `120`,
  `60` gradi**, ### **lati `(96, 6)`, il profilo in `m_u`: il gradiente e' normale a `w`, a `60` gradi -- PARALLELO a un legame, e a `30` gradi da quello del toro `A`**; ### **`f = 1/2`.**
- **IL PACCHETTO** *(il mandato)*: ### **`G(m) u_K e^{i K.r}`, `G` gaussiana in `m` a `x0 = Lx/4`, `W = Lx/16`, `u_K = Q[:, 0]`, `Q` lo spazio proprio della banda a `K`** *(dal blocco al lato
  `6`; tutte le bande sono doppie su tutta la zona: visto in memoria)*; ### **`e^{i K.r} = e^{2 pi i (m1 + m2)/3}` sul toro `A`, `e^{2 pi i m_u/3}` sul toro `B`** *(`K.w = 0`)*. ### **Solo la
  materia; `x0` dove il gradiente e' massimo.**
- **LA COPPIA A `K`** *(non sempre la piu' stretta: a `eps 0.5, s >= 0.3` il minimo e' a `Gamma`)*: ### **a `eps 0` i due livelli doppi DIVERSI da `0` e da `-pi s`** *(i quattro piatti)*; ### **a
  `eps > 0` seguiti in `eps` a passi di `0.05` per sovrapposizione dello spazio.**
- **LA DURATA:** ### **`T = max(Lx/4, ceil(10 x 2 pi/delta_min))`, `delta_min` la distanza minima a `K` fra il livello della banda e ogni altro livello** *(il battimento piu' lento: la regola
  dei `10` periodi data da Luca nella parte D del «segno della gravita'»)*; ### **la finestra `|<m> - x0| < Lx/32` di `_forza_da_cs` resta.**
  ### 📝 **E' UNA CORREZIONE DEL METODO, VISTA IN MEMORIA** *(prima di questo testo)*: ### **con `T = Lx/4`** *(`24` tick a `s 0.05`)* ### **la corsa a `eta 0` derivava QUANTO il segnale**
  *(`1.4e-6` contro `1.3e-6`)*; ### **con `10` periodi del salto della COPPIA** *(non del battimento)* ### **lo specchio era asimmetrico del `15%` a `eps 0.5`**; ### **con `10` periodi di
  `delta_min` il nullo e' entro `1 sigma` e lo specchio entro il `3%`.** ### **Il battimento lento e' col livello PIATTO a `0`, a meta' del salto.**
- **IL FIT** *(`_forza_da_cs.fit_moto`)*: ### **`x0 + v0 t + a t^2/2` sul baricentro circolare in `m`**, ### **`sigma_a`, il residuo massimo** *(il tremolio)*, ### **la norma fuori dallo spazio
  `Q`** *(`_forza_da_cs.norma_fuori`, leggibile se `<= 0.10`)*.
- **LE PREVISIONI NELLE UNITA' DI `m`:** ### **`a_H = -omega''_cart (d omega/ds) (ds/dm)/f^2`, `a_RG(v) = -v^2 (d ln s/dm)/f^2`**, ### **`ds/dm = -cs0 eta 2 pi/Lx` a `x0`.** ### **`a > 0`
  e' VERSO `cs` BASSO** *(per `eta > 0`).*
- **LA GRIGLIA:** ### **`eps` in `(0, 0.5)`, `s0` in `(0.05, 0.1, 0.3, 0.5)`, `eta` in `(0, +-1e-3, +-1e-2)`, `Lx` in `(96, 192)`, le due convenzioni, le due bande** *(toro `A`)*; ### **il toro
  `B` a `Lx 96`, `eta` in `(0, +-1e-2)`.**
- **LE LETTURE:** ### **`a_mis/a_H`, `a_mis/a_RG` con le tre velocita'**, ### **il verso, la norma fuori, il tremolio, `v0`** *(fermo: `v0` a `eta 0`, e `v_g` a `K` dalla curvatura)*; ### **l'universalita'
  fra le bande** *(`a_1/a_0`)* ### **e fra `eps 0` e `0.5`** *(`a/a_H`)*; ### **il limite a `s0 -> 0`: l'estrapolazione lineare in `s0` dai due `s0` piu' piccoli e quella quadratica dai tre,
  riportate tutte e due** *(«senza imporre la forma»: se non coincidono, il limite NON e' letto)*.

## 4. PARTE C -- LA MONETA E LO ZERO

- ### **`eps` in `(0.25, 0.5, 1.0)`, `s` in `(0.05, 0.1, 0.3, 0.5)`, la coppia a `K` seguita in `eps`:** ### **`lambda*_RG`** *(la definizione di `8781162c`: uguali gli `a_H/a_RG` col `v_fit` di
  ciascuna banda)* ### **e `lambda*_H`** *(uguali le `a_H`: e' quella che conta per la caduta)*; ### **`(a_H,1 - a_H,0)/media` a `lambda = 1/2`; il centro della coppia/`s`.**
- ### **IL FIT:** ### **`ln|lambda* - 1/2| = c + p ln s + q ln eps`** *(minimi quadrati, `12` punti)*, ### **lo stesso per la differenza delle `a_H`**; ### **`p`, `q` e il residuo massimo.**

## 5. LE PREVISIONI *(prima dei numeri dello strumento; i numeri VISTI in memoria li dichiaro)*

- ### **`v_max/s` fra `0.59` e `0.64`** *(visto)*; ### **`v_fit/s ~ 0.52`** *(dal `v 0.0301` di `8781162c` a `s 0.05`, `x sqrt3/2`)*; ### **`v_fronte` fra `v_max` e il `15%` sopra, crescendo col
  rigore della soglia** *(visto a `s 0.3`: `0.60`, `0.64`, `0.68`)*.
- ### **CON `v_max` IN `a_RG`: `a_H/a_RG ~ 2.26 x (0.52/0.60)^2 ~ 1.7`** ### **-- la previsione del guardiano** *(«si avvicina a `1`»)* ### **va nel verso giusto ma NON ci arriva**: ### **prevedo
  che il secondo PUO'-FALLIRE FALLISCA.** ### **Il fattore `2.26` viene piu' dalla forma della banda** *(`omega''` grande rispetto a `v_fit^2/Delta`: non e' un Dirac)* ### **che dalla
  velocita'.**
- ### **`a_mis/a_H ~ 0.95` a `s0 0.05`, sulle due bande, verso `cs` basso** *(visto, `Lx 96`)*: ### **il primo PUO'-FALLIRE PASSA** *(al margine: `0.95` contro `0.9`)*.
- ### **Con lo zero di oggi le due bande vanno in versi OPPOSTI** *(Hamilton `+6.8` e `-2.3`; visto a `s0 0.3`: `+1.3e-4` e `-4.7e-5`)*: ### **il DEVE-FALLIRE fallisce come deve.**
- ### **Il toro `B` come il toro `A` entro pochi `%`** *(la curvatura a `K` e' isotropa)*; ### **`eps 0.5` come `eps 0` entro pochi `%`.**
- ### **PARTE C: `|lambda* - 1/2|` va come `s^2 eps^2`** *(da `8781162c`: raddoppiando `s` x`4`, raddoppiando `eps` x`3.5`-`3.9`)*.
- ### **Il limite a `s0 -> 0` di `a_mis/a_H`: NON lo prevedo** *(fra `0.95` e `1`)*.

## 6. I CRITERI, FISSATI ORA *(dal mandato; dove il mandato non dice la portata, la fisso qui)*

- ### **DEVE PASSARE:** ### **la parte `0`** *(sopra)*.
- ### **DEVE PASSARE:** ### **`eta 0`: `|a|` sotto il rumore del fit** *(`_forza_da_cs.nullo`: `|a| <= 2 sigma_a`)*, ### **per ogni `(eps, s0, banda)`, e anche per ogni `Lx`, convenzione e
  toro.**
- ### **DEVE PASSARE:** ### **il profilo specchiato** *(`-eta`)*: ### **`a` cambia segno, `|a|` uguale entro il `5%`** *(del piu' grande)*, ### **ogni caso.**
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«con lo zero di oggi le due bande hanno la stessa accelerazione»** *(entro il `5%`)* ### **a `eps 0`, ogni `s0`, `Lx`, `eta > 0`, toro `A`:
  deve essere FALSA ogni volta, con le due corse leggibili e non nulle.**
- ### **PUO' FALLIRE:** ### **a `eps 0`, `s0 0.05`, zero simmetrico** *(le due bande, i due `Lx`, `eta > 0`, toro `A`)*: ### **`a_mis/a_H` fra `0.9` e `1.1`, lo stesso verso, verso `cs` basso.**
- ### **PUO' FALLIRE:** ### **la stessa portata, `a_mis/a_RG(v_max)` fra `0.8` e `1.2`** *(«la velocita' del cono» e' `v_max`: il fronte ne e' la misura dinamica)*.
- ### **DI SERVIZIO:** ### **a `eta 0` la traccia nelle due convenzioni uguale entro `1e-10`** *(a `cs` uniforme la simmetrica e' una fase globale)*; ### **e quelli delle parti `0` e `A`.**
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE: le tabelle.** ### **A parte: la lettura in tre righe; una riga sul fattore `2.26`; una riga su che cosa vuol dire per la scelta della
  convenzione dello zero** *(informazione per Luca, non una scelta)*.

### 📝 **ANNOTAZIONE 1** *(prima della corsa dello strumento committato, nel commit dello strumento)*: ### **la prova a vuoto in memoria** *(ridotta: `s` in `(0.1, 0.3, 0.5)`, `Lx 96`,
`eps_C 0.5`; il `txt` negli appunti)* ### **ha mostrato due difetti del MIO METODO, corretti prima della corsa:**
- ### **(a) IL TORO `B` NON E' FERMO, e per una ragione di FISICA:** ### **a `eta 0` il pacchetto deriva** *(`v0 = +-2e-3` sulle due bande, `a = -+2.6e-6 +- 4e-8` a `s0 0.1`)* ### **e lo
  specchio e' asimmetrico fino al `17%`.** ### **La causa, verificata sullo spettro:** ### **lungo `(1, 1)` in `theta`** *(la direzione `Gamma-K`, quella del toro `B`)* ### **`omega(K + q) != omega(K -
  q)`** *(`0.1578270` contro `0.1580277` al primo passo, `eps 0, s 0.1`)*, ### **lungo `(1, 0)`** *(il toro `A`)* ### **sono uguali al bit**: ### **`K` ha la simmetria `C3`, non l'inversione, e il
  termine cubico** *(la deformazione trigonale)* ### **da' una velocita' media `~ <q^2>` a un pacchetto gaussiano lungo `Gamma-K`.** ### **LA CORREZIONE:** ### **`(1)` ogni corsa a `eta != 0` si
  legge anche DIFFERENZIALE, `x(eta) - x(0)` dalla stessa partenza** *(toglie la deriva libera)*; ### **`(2)` il nullo e lo specchio DEVE-PASSARE restano sul toro `A`** *(la corsa del mandato:
  «per ogni `(eps, s0, banda)`»; il toro `B` l'avevo aggiunto io alla portata, e lo tolgo dichiarandolo)*; ### **`(3)` il toro `B` si LEGGE** *(la deriva, il grezzo, il differenziale e il suo
  specchio)*, ### **e l'isotropia si confronta col differenziale su tutti e due i tori.** ### **Sul toro `A` la curvatura e' isotropa e il cubico non entra: e' l'unico dei due dove il pacchetto e'
  davvero fermo.**
- ### **(b) IL FRONTE A `s 0.5` girava intorno al toro** *(a `64` di lato: `v_fronte` NEGATIVA)*: ### **il toro del fronte e' `192`** *(non `128`)*, ### **e un controllo DI SERVIZIO pretende che
  il fronte resti dentro il cerchio inscritto** *(`0.9 x L sqrt3/4`)*.
- ### **(c) LO SPECCHIO SUL TORO `A` a `eta 1e-3, s0 0.5` e' asimmetrico del `6%`** *(`+9.65e-6` contro `-9.07e-6`, banda `1`, `Lx 96`)*: ### **la deriva a `eta 0`, sotto il rumore,
  pesa su un segnale dieci volte piu' piccolo.** ### **IL CRITERIO NON SI CAMBIA:** ### **prevedo che quel DEVE-PASSARE FALLISCA, e se fallisce mi FERMO.** ### **Lo strumento stampa anche lo
  specchio DIFFERENZIALE** *(una lettura, non un controllo)*.
- ### **I NUMERI VISTI** *(non li uso; le previsioni restano)*: ### **`v_max/s` `0.600`, `0.612`, `0.635`** *(`eps 0`)*; ### **`v_fit/s ~ 0.52`**; ### **`a_H/a_RG` simmetrico con `v_max`: `+1.70`,
  `+1.49`, `+1.11`** *(`s 0.1, 0.3, 0.5`)*; ### **`lambda*_RG - 1/2 ~ s^2.0 eps^1.4`** *(un solo `eps` nella prova: `q` non e' misurato)*.

## 7. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. la parte `0` *(`csv/_triangoli.py`, `csv/_forza_da_cs.py`, l'inventario)*, committata;
3. `csv/_triangoli_forza.py` e la sua voce nell'inventario, committati prima dei numeri;
4. la corsa: `python csv/_triangoli_forza.py > doc/referti_l2/triangoli_forza.txt`;
5. il referto, la relazione, la sezione `8`, committati e pushati.

## 8. I RISULTATI *(scritti dopo la corsa, sotto)*
