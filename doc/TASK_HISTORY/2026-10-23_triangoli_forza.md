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

> **La corsa:** ### **strumento `csv/_triangoli_forza.py` sha1-BYTE `19d5663e`** *(`000bb095`)*; ### **referto `doc/referti_l2/triangoli_forza.txt` sha1-BYTE `8c9dbb6f`, `.jsonl` `8d0241cf`.** ### **Le
> tabelle sono GENERATE dal `.jsonl`.**

### ⛔ 8.0 I CONTROLLI -- **UN DEVE-PASSARE FALLISCE, come avevo previsto nell'annotazione 1: MI FERMO**

| criterio | esito | il numero |
|---|---|---|
| parte `0`: la scena a lati uguali al bit; `matrice_tick` al bit | **PASSA** | `102` attributi, nessuno diverso; lo spettro `0.0` |
| parte `0`: `scarto_c6` uguale dove era giusto; giusto dove sbagliava; il quadrato resta fuori | **PASSA** | `7.4e-16` su `36` casi; `<= 2.77e-15` sui `4` casi sbagliati; `0.284` |
| di servizio: `corsa()` del quadrato al bit; il fronte dentro il toro; `3/4 h11`; `a_H/a_RG` = `8781162c`; le due convenzioni a `eta 0`; `lambda*_RG` = `8781162c` | **PASSA** | `1.9e-4`; `6.6e-8`; `1.4e-14`; `4.7e-9` |
| DEVE PASSARE: `eta 0`, `|a| <= 2 sigma_a` *(toro `A`)* | **PASSA** | il peggiore `|a|/sigma = 1.28` |
| DEVE PASSARE: lo specchio, `|a|` uguale entro il `5%` *(toro `A`, `128` casi)* | ### **FALLISCE** | ### **`4` casi su `128`, tutti a `s0 0.5`, `eta 1e-3`, banda `1`: `5.97%`, `10.74%`, `6.60%`, `5.88%`** *(lo specchio DIFFERENZIALE, una lettura: il peggiore `0.13%`)* |
| DEVE FALLIRE: con lo zero di oggi le due bande hanno la stessa accelerazione | **fallisce, come deve** | vera `0` volte su `16`; `a_1/a_0` da `-0.33` a `-0.44` |
| PUO' FALLIRE: `eps 0, s0 0.05`, simmetrico: `a/a_H` fra `0.9` e `1.1`, verso `cs` basso | **PASSA** | da `0.9516` a `0.9808` *(`8` corse)* |
| PUO' FALLIRE: la stessa portata, `a/a_RG(v_max)` fra `0.8` e `1.2` | ### **FALLISCE** | da `1.6329` a `1.6829` |

### **IL FALLIMENTO, letto:** ### **a `eta 1e-3` il segnale e' `10` volte piu' piccolo, e la deriva a `eta 0`** *(sotto il rumore: `|a|/sigma <= 1.28`)* ### **pesa sulla differenza fra `+eta` e
`-eta`**; ### **col differenziale** *(`x(eta) - x(0)`)* ### **lo specchio tiene entro lo `0.13%` ovunque.** ### **La correzione** *(lo specchio sul differenziale, o una durata piu' lunga a `s0` grande)*
### **cambierebbe un criterio dopo averlo visto fallire: E' UNA DECISIONE DI LUCA, non mia.**

### 8.1 LE VELOCITA' *(divise per `s`; archi per tick)* E `a_H/a_RG` CON CIASCUNA *(zero simmetrico; tra parentesi quello di oggi)*

| `eps` | `s` | banda | `v_max/s` | `v_fit/s` | `v_fronte/s` *(1e-2, 1e-4, 1e-6)* | `a_H/a_RG` con `v_fit` | con `v_max` | con `v_fronte` *(1e-2, 1e-4, 1e-6)* |
|---|---|---|---|---|---|---|---|---|
| `0` | `0.05` | `0` | `0.5989` | `0.5216` | `0.5436` `0.6895` `0.7678` | `+2.2620` *(`+6.7966`)* | `+1.7159` *(`+5.1555`)* | `+2.0827` `+1.2942` `+1.0437` |
| `0` | `0.05` | `1` | `0.5989` | `0.5216` | `0.5436` `0.6895` `0.7678` | `+2.2620` *(`-2.2725`)* | `+1.7159` *(`-1.7238`)* | `+2.0827` `+1.2942` `+1.0437` |
| `0` | `0.1` | `0` | `0.6000` | `0.5219` | `0.5704` `0.6913` `0.7849` | `+2.2419` *(`+6.7677`)* | `+1.6959` *(`+5.1195`)* | `+1.8764` `+1.2776` `+0.9911` |
| `0` | `0.1` | `1` | `0.6000` | `0.5219` | `0.5704` `0.6913` `0.7849` | `+2.2419` *(`-2.2839`)* | `+1.6959` *(`-1.7277`)* | `+1.8764` `+1.2776` `+0.9911` |
| `0` | `0.3` | `0` | `0.6120` | `0.5243` | `0.5989` `0.6500` `0.6685` | `+2.0309` *(`+6.4706`)* | `+1.4907` *(`+4.7496`)* | `+1.5567` `+1.3217` `+1.2493` |
| `0` | `0.3` | `1` | `0.6120` | `0.5243` | `0.5989` `0.6500` `0.6685` | `+2.0309` *(`-2.4088`)* | `+1.4907` *(`-1.7681`)* | `+1.5567` `+1.3217` `+1.2493` |
| `0` | `0.5` | `0` | `0.6351` | `0.5246` | `0.6334` `0.6568` `0.6827` | `+1.6313` *(`+5.9473`)* | `+1.1128` *(`+4.0570`)* | `+1.1187` `+1.0404` `+0.9630` |
| `0` | `0.5` | `1` | `0.6351` | `0.5246` | `0.6334` `0.6568` `0.6827` | `+1.6313` *(`-2.6847`)* | `+1.1128` *(`-1.8314`)* | `+1.1187` `+1.0404` `+0.9630` |
| `0.5` | `0.05` | `0` | `0.5854` | `0.5089` | `0.5436` `0.6895` `0.7678` | `+2.3772` *(`+6.9158`)* | `+1.7962` *(`+5.2256`)* | `+2.0833` `+1.2946` `+1.0440` |
| `0.5` | `0.05` | `1` | `0.5854` | `0.5089` | `0.5436` `0.6895` `0.7678` | `+2.3751` *(`-2.1631`)* | `+1.7951` *(`-1.6348`)* | `+2.0820` `+1.2937` `+1.0433` |
| `0.5` | `0.1` | `0` | `0.5864` | `0.5089` | `0.5282` `0.6165` `0.7211` | `+2.3604` *(`+6.8916`)* | `+1.7776` *(`+5.1899`)* | `+2.1909` `+1.6085` `+1.1756` |
| `0.5` | `0.1` | `1` | `0.5864` | `0.5092` | `0.5282` `0.6165` `0.7211` | `+2.3519` *(`-2.1774`)* | `+1.7729` *(`-1.6414`)* | `+2.1852` `+1.6043` `+1.1725` |
| `0.5` | `0.3` | `0` | `0.5969` | `0.5086` | `0.5953` `0.6313` `0.6565` | `+2.1844` *(`+6.6441`)* | `+1.5864` *(`+4.8251`)* | `+1.5946` `+1.4179` `+1.3113` |
| `0.5` | `0.3` | `1` | `0.5969` | `0.5109` | `0.5953` `0.6313` `0.6565` | `+2.1077` *(`-2.3353`)* | `+1.5445` *(`-1.7113`)* | `+1.5525` `+1.3805` `+1.2768` |
| `0.5` | `0.5` | `0` | `0.6166` | `0.5031` | `0.6161` `0.6423` `0.6665` | `+1.8526` *(`+6.2202`)* | `+1.2333` *(`+4.1409`)* | `+1.2353` `+1.1369` `+1.0557` |
| `0.5` | `0.5` | `1` | `0.6166` | `0.5095` | `0.6161` `0.6423` `0.6665` | `+1.6357` *(`-2.6858`)* | `+1.1169` *(`-1.8339`)* | `+1.1186` `+1.0295` `+0.9561` |

### 8.2 LA CORSA SUL TORO `A` *(`eta 1e-2`; `a/a_H` ai due `Lx`, e a `Lx 192` `a/a_RG` con `v_max` e `v_fit`; `v0` e `a` a `eta 0`; il tremolio e la norma fuori a `eta 1e-2, Lx 192`)*

| `eps` | `s0` | conv | banda | `a/a_H` `Lx 96` | `a/a_H` `Lx 192` | `a/a_RG(v_max)` | `a/a_RG(v_fit)` | verso | `eta 0`: `v0`, `a/sigma` | tremolio | fuori |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0` | `0.05` | simm | `0` | `+0.9516` | `+0.9682` | `+1.6613` | `+2.1901` | cs BASSO | `-4.8e-08`, `+0.51` | `4.1e-03` | `3.1e-03` |
| `0` | `0.05` | simm | `1` | `+0.9582` | `+0.9765` | `+1.6755` | `+2.2088` | cs BASSO | `-1.0e-07`, `+0.60` | `7.1e-03` | `6.3e-03` |
| `0` | `0.05` | oggi | `0` | `+0.9420` | `+0.9616` | `+4.9575` | `+6.5355` | cs BASSO | `-4.8e-08`, `+0.51` | `4.1e-03` | `3.8e-03` |
| `0` | `0.05` | oggi | `1` | `+0.9203` | `+0.9416` | `-1.6232` | `-2.1398` | cs ALTO | `-1.0e-07`, `+0.60` | `7.6e-03` | `6.1e-03` |
| `0` | `0.1` | simm | `0` | `+0.9503` | `+0.9672` | `+1.6403` | `+2.1684` | cs BASSO | `-1.6e-07`, `+0.62` | `4.0e-03` | `3.1e-03` |
| `0` | `0.1` | simm | `1` | `+0.9570` | `+0.9756` | `+1.6545` | `+2.1871` | cs BASSO | `-2.9e-07`, `+0.60` | `7.4e-03` | `6.3e-03` |
| `0` | `0.1` | oggi | `0` | `+0.9412` | `+0.9612` | `+4.9206` | `+6.5048` | cs BASSO | `-1.6e-07`, `+0.62` | `3.9e-03` | `3.7e-03` |
| `0` | `0.1` | oggi | `1` | `+0.9209` | `+0.9426` | `-1.6284` | `-2.1527` | cs ALTO | `-2.9e-07`, `+0.60` | `7.9e-03` | `6.1e-03` |
| `0` | `0.3` | simm | `0` | `+0.9465` | `+0.9627` | `+1.4352` | `+1.9552` | cs BASSO | `-3.4e-07`, `+0.34` | `1.1e-03` | `2.9e-03` |
| `0` | `0.3` | simm | `1` | `+0.9540` | `+0.9729` | `+1.4503` | `+1.9758` | cs BASSO | `-1.5e-06`, `+0.61` | `8.5e-03` | `6.2e-03` |
| `0` | `0.3` | oggi | `0` | `+0.9408` | `+0.9601` | `+4.5599` | `+6.2121` | cs BASSO | `-3.4e-07`, `+0.34` | `1.2e-03` | `2.9e-03` |
| `0` | `0.3` | oggi | `1` | `+0.9245` | `+0.9469` | `-1.6742` | `-2.2809` | cs ALTO | `-1.5e-06`, `+0.61` | `8.8e-03` | `6.2e-03` |
| `0` | `0.5` | simm | `0` | `+0.9511` | `+0.9662` | `+1.0752` | `+1.5762` | cs BASSO | `-5.3e-07`, `+0.25` | `2.2e-03` | `2.7e-03` |
| `0` | `0.5` | simm | `1` | `+0.9580` | `+0.9759` | `+1.0860` | `+1.5921` | cs BASSO | `-2.6e-06`, `+0.48` | `7.4e-03` | `6.4e-03` |
| `0` | `0.5` | oggi | `0` | `+0.9430` | `+0.9612` | `+3.8994` | `+5.7163` | cs BASSO | `-5.3e-07`, `+0.25` | `2.3e-03` | `2.9e-03` |
| `0` | `0.5` | oggi | `1` | `+0.9266` | `+0.9487` | `-1.7375` | `-2.5471` | cs ALTO | `-2.6e-06`, `+0.48` | `7.4e-03` | `6.4e-03` |
| `0.5` | `0.05` | simm | `0` | `+0.9526` | `+0.9681` | `+1.7389` | `+2.3014` | cs BASSO | `-2.6e-08`, `+0.41` | `3.7e-03` | `2.8e-03` |
| `0.5` | `0.05` | simm | `1` | `+0.9583` | `+0.9754` | `+1.7509` | `+2.3167` | cs BASSO | `-1.1e-07`, `+0.62` | `6.9e-03` | `5.6e-03` |
| `0.5` | `0.05` | oggi | `0` | `+0.9435` | `+0.9619` | `+5.0264` | `+6.6522` | cs BASSO | `-2.6e-08`, `+0.41` | `3.7e-03` | `3.4e-03` |
| `0.5` | `0.05` | oggi | `1` | `+0.9214` | `+0.9417` | `-1.5396` | `-2.0370` | cs ALTO | `-1.1e-07`, `+0.62` | `6.8e-03` | `5.5e-03` |
| `0.5` | `0.1` | simm | `0` | `+0.9525` | `+0.9680` | `+1.7206` | `+2.2848` | cs BASSO | `-6.8e-08`, `+0.37` | `3.6e-03` | `2.7e-03` |
| `0.5` | `0.1` | simm | `1` | `+0.9575` | `+0.9747` | `+1.7281` | `+2.2924` | cs BASSO | `-2.9e-07`, `+0.61` | `6.5e-03` | `5.6e-03` |
| `0.5` | `0.1` | oggi | `0` | `+0.9435` | `+0.9618` | `+4.9918` | `+6.6286` | cs BASSO | `-6.8e-08`, `+0.37` | `3.5e-03` | `3.4e-03` |
| `0.5` | `0.1` | oggi | `1` | `+0.9219` | `+0.9426` | `-1.5472` | `-2.0525` | cs ALTO | `-2.9e-07`, `+0.61` | `6.4e-03` | `5.5e-03` |
| `0.5` | `0.3` | simm | `0` | `+0.9463` | `+0.9614` | `+1.5251` | `+2.1000` | cs BASSO | `-8.5e-08`, `+0.16` | `1.4e-03` | `2.6e-03` |
| `0.5` | `0.3` | simm | `1` | `+0.9527` | `+0.9714` | `+1.5004` | `+2.0474` | cs BASSO | `-8.0e-07`, `+0.43` | `7.3e-03` | `6.1e-03` |
| `0.5` | `0.3` | oggi | `0` | `+0.9425` | `+0.9597` | `+4.6307` | `+6.3764` | cs BASSO | `-8.5e-08`, `+0.16` | `1.6e-03` | `2.6e-03` |
| `0.5` | `0.3` | oggi | `1` | `+0.9264` | `+0.9477` | `-1.6219` | `-2.2132` | cs ALTO | `-8.0e-07`, `+0.43` | `7.5e-03` | `6.0e-03` |
| `0.5` | `0.5` | simm | `0` | `+0.9421` | `+0.9570` | `+1.1803` | `+1.7729` | cs BASSO | `-1.5e-06`, `+0.78` | `2.4e-03` | `2.5e-03` |
| `0.5` | `0.5` | simm | `1` | `+0.9401` | `+0.9559` | `+1.0677` | `+1.5636` | cs BASSO | `-2.5e-06`, `+1.28` | `6.1e-03` | `6.0e-03` |
| `0.5` | `0.5` | oggi | `0` | `+0.9413` | `+0.9586` | `+3.9697` | `+5.9629` | cs BASSO | `-1.5e-06`, `+0.78` | `2.3e-03` | `2.7e-03` |
| `0.5` | `0.5` | oggi | `1` | `+0.9429` | `+0.9616` | `-1.7636` | `-2.5827` | cs ALTO | `-2.5e-06`, `+1.28` | `6.2e-03` | `5.9e-03` |

### 8.3 L'UNIVERSALITA' E L'ISOTROPIA *(`eta 1e-2`, `Lx 96`; `a_1/a_0` fra le bande, `(a/a_H)[eps 0.5]/(a/a_H)[eps 0]`, e il toro `B` sul toro `A` col differenziale)*

| conv | `s0` | `a_1/a_0` `eps 0` | `a_1/a_0` `eps 0.5` | `eps 0.5 / eps 0` *(banda 0, 1)* | `B/A` `eps 0` *(banda 0, 1)* | `B/A` `eps 0.5` | `B`: `v0` a `eta 0` *(banda 0)* |
|---|---|---|---|---|---|---|---|
| simm | `0.05` | `+1.0068` | `+1.0053` | `1.0011` `1.0002` | `0.9783` `0.9122` | `0.9817` `0.9131` | `+1.0e-03` |
| simm | `0.1` | `+1.0071` | `+1.0026` | `1.0023` `1.0005` | `0.9782` `0.9118` | `0.9818` `0.9128` | `+2.0e-03` |
| simm | `0.3` | `+1.0079` | `+0.9803` | `0.9998` `0.9987` | `0.9762` `0.9120` | `0.9829` `0.9105` | `+6.1e-03` |
| simm | `0.5` | `+1.0073` | `+0.9036` | `0.9905` `0.9812` | `0.9737` `0.9161` | `0.9769` `0.9234` | `+9.9e-03` |
| oggi | `0.05` | `-0.3267` | `-0.3055` | `1.0016` `1.0012` | `1.0153` `0.9695` | `1.0187` `0.9709` | `+1.0e-03` |
| oggi | `0.1` | `-0.3302` | `-0.3090` | `1.0025` `1.0012` | `1.0160` `0.9704` | `1.0189` `0.9717` | `+2.0e-03` |
| oggi | `0.3` | `-0.3658` | `-0.3486` | `1.0019` `1.0021` | `1.0191` `0.9758` | `1.0246` `0.9797` | `+6.1e-03` |
| oggi | `0.5` | `-0.4436` | `-0.4436` | `0.9982` `1.0175` | `1.0175` `0.9810` | `1.0251` `0.9858` | `+9.9e-03` |

### 8.4 IL LIMITE A `s0 -> 0` *(toro `A`, `Lx 192`, `eta 1e-2`; la lineare dai due `s0` piu' piccoli, la quadratica dai tre)*

| conv | `eps` | banda | che | `s0 0.05, 0.1, 0.3, 0.5` | lineare | quadratica |
|---|---|---|---|---|---|---|
| simm | `0` | `0` | `a/a_H` | `+0.9682` `+0.9672` `+0.9627` `+0.9662` | `+0.9692` | `+0.9691` |
| simm | `0` | `0` | `a/a_RG(v_max)` | `+1.6613` `+1.6403` `+1.4352` `+1.0752` | `+1.6822` | `+1.6701` |
| simm | `0` | `1` | `a/a_H` | `+0.9765` `+0.9756` `+0.9729` `+0.9759` | `+0.9774` | `+0.9775` |
| simm | `0` | `1` | `a/a_RG(v_max)` | `+1.6755` `+1.6545` `+1.4503` `+1.0860` | `+1.6965` | `+1.6845` |
| simm | `0.5` | `0` | `a/a_H` | `+0.9681` `+0.9680` `+0.9614` `+0.9570` | `+0.9682` | `+0.9676` |
| simm | `0.5` | `0` | `a/a_RG(v_max)` | `+1.7389` `+1.7206` `+1.5251` `+1.1803` | `+1.7572` | `+1.7450` |
| simm | `0.5` | `1` | `a/a_H` | `+0.9754` `+0.9747` `+0.9714` `+0.9559` | `+0.9761` | `+0.9760` |
| simm | `0.5` | `1` | `a/a_RG(v_max)` | `+1.7509` `+1.7281` `+1.5004` `+1.0677` | `+1.7737` | `+1.7601` |
| oggi | `0` | `0` | `a/a_H` | `+0.9616` `+0.9612` `+0.9601` `+0.9612` | `+0.9620` | `+0.9621` |
| oggi | `0` | `0` | `a/a_RG(v_max)` | `+4.9575` `+4.9206` `+4.5599` `+3.8994` | `+4.9943` | `+4.9730` |
| oggi | `0` | `1` | `a/a_H` | `+0.9416` `+0.9426` `+0.9469` `+0.9487` | `+0.9406` | `+0.9407` |
| oggi | `0` | `1` | `a/a_RG(v_max)` | `-1.6232` `-1.6284` `-1.6742` `-1.7375` | `-1.6179` | `-1.6203` |
| oggi | `0.5` | `0` | `a/a_H` | `+0.9619` `+0.9618` `+0.9597` `+0.9586` | `+0.9619` | `+0.9618` |
| oggi | `0.5` | `0` | `a/a_RG(v_max)` | `+5.0264` `+4.9918` `+4.6307` `+3.9697` | `+5.0611` | `+5.0388` |
| oggi | `0.5` | `1` | `a/a_H` | `+0.9417` `+0.9426` `+0.9477` `+0.9616` | `+0.9408` | `+0.9410` |
| oggi | `0.5` | `1` | `a/a_RG(v_max)` | `-1.5396` `-1.5472` `-1.6219` `-1.7636` | `-1.5319` | `-1.5363` |

### 8.5 LA MONETA E LO ZERO *(la coppia a `K` seguita in `eps`)*

| `eps` | `s` | `lambda*_RG` | `lambda*_H` | `(a_H1 - a_H0)/media` a `lambda 1/2` | centro/`s` |
|---|---|---|---|---|---|
| `0.25` | `0.05` | `0.50003066` | `0.50002234` | `-1.769e-04` | `-0.00006` |
| `0.25` | `0.1` | `0.50012282` | `0.50008979` | `-7.159e-04` | `-0.00024` |
| `0.25` | `0.3` | `0.50112378` | `0.50085038` | `-7.334e-03` | `-0.00218` |
| `0.25` | `0.5` | `0.50324287` | `0.50261420` | `-2.722e-02` | `-0.00627` |
| `0.5` | `0.05` | `0.50011709` | `0.50008414` | `-6.429e-04` | `-0.00022` |
| `0.5` | `0.1` | `0.50046922` | `0.50033836` | `-2.602e-03` | `-0.00087` |
| `0.5` | `0.3` | `0.50430773` | `0.50321922` | `-2.671e-02` | `-0.00796` |
| `0.5` | `0.5` | `0.51248195` | `0.50993671` | `-9.908e-02` | `-0.02298` |
| `1` | `0.05` | `0.50040404` | `0.50027669` | `-1.871e-03` | `-0.00064` |
| `1` | `0.1` | `0.50162143` | `0.50111499` | `-7.589e-03` | `-0.00256` |
| `1` | `0.3` | `0.51510869` | `0.51082502` | `-7.929e-02` | `-0.02372` |
| `1` | `0.5` | `0.54484762` | `0.53433110` | `-3.021e-01` | `-0.06970` |

| il fit di `|...| = e^c s^p eps^q` | `p` | `q` | residuo in `ln`, massimo |
|---|---|---|---|
| `lambda*_RG - 1/2` | `2.030` | `1.873` | `0.044` |
| `lambda*_H - 1/2` | `2.072` | `1.831` | `0.069` |
| `(a_H1 - a_H0)/media` | `2.177` | `1.714` | `0.159` |
| `centro/s` | `2.027` | `1.721` | `0.079` |

### 8.6 LA LETTURA *(tre righe)*

1. ### **LA DINAMICA CONFERMA HAMILTON:** ### **`a_mis/a_H` fra `0.92` e `0.98` in OGNI caso** *(`eps 0` e `0.5`, ogni `s0`, le due bande, le due convenzioni)*, ### **piatto in `s0`** *(il limite a
   `s0 -> 0`: `0.969` e `0.977` simmetrico, lineare e quadratica d'accordo entro `6e-4`)* ### **e crescente con `Lx`** *(`0.952 -> 0.968` da `96` a `192`: un effetto della larghezza `W = Lx/16`)*.
2. ### **CON LO ZERO SIMMETRICO le due bande cadono insieme verso `cs` BASSO** *(`a_1/a_0 = 1.007` a `eps 0`)*; ### **CON QUELLO DI OGGI in versi OPPOSTI** *(`a_1/a_0` da `-0.33` a `-0.44`)*, ### **come
   dice Hamilton.** ### **A `eps 0.5` la moneta separa le bande come `s^2`** *(`a_1/a_0`: `1.005`, `1.003`, `0.980`, `0.904` a `s0 0.05`-`0.5`; Hamilton `(a_H1 - a_H0)/media = -9.9e-2` a `s 0.5`)*.
3. ### **IL TORO `B`** *(il gradiente lungo un legame)*: ### **il pacchetto non e' fermo** *(la deformazione trigonale, `v0` fino a `9.9e-3`)*, ### **e col differenziale `B/A` sta fra `0.91` e `1.03`: l'isotropia
   NON e' verificata al `5%` su quella direzione, e la ragione e' la deriva, non la curvatura** *(isotropa entro `7.7e-4`, `8781162c`)*.

### 8.7 IL FATTORE `2.26`

### **Non viene dalla velocita' usata in `a_RG`:** ### **con `v_max`** *(`0.60 s`, `1.15` volte `v_fit`)* ### **`a_mis/a_RG` scende a `1.63`-`1.68` a `s0 0.05`, non a `1`** *(il secondo PUO'-FALLIRE
fallisce, come avevo previsto)*; ### **solo il fronte alla soglia `1e-6` lo porta a `~1.04`, ma quel fronte cresce con la soglia** *(`0.54`, `0.69`, `0.77` volte `s`)* ### **e non e' una velocita'
definita.** ### **Il fattore viene dalla FORMA della banda a `K`:** ### **`a_H/a_RG = s omega'' (d omega/ds)/v^2`, e `omega''` e' piu' grande di `v_fit^2/Delta`: la banda non e' un Dirac.**

### 8.8 CHE COSA VUOL DIRE PER LA SCELTA DELLO ZERO *(informazione per Luca, non una scelta)*

### **Sui triangoli la dinamica distingue le due convenzioni:** ### **con lo zero simmetrico la coppia massiva a `K` ha la caduta universale** *(le due bande insieme, entro lo `0.7%` a `eps 0`)*;
### **con quello di oggi no** *(versi opposti)*; ### **e a `eps 0.5` la moneta rompe l'universalita' come `s^2.18 eps^1.71`** *(`6.4e-4` a `s 0.05`, `9.9e-2` a `s 0.5`)*: ### **piccola a `s` piccolo,
d'ordine `10%` a `s 0.5`.**

### 8.9 PARTE C, LETTA

### **`lambda* - 1/2` va come `s^2.03 eps^1.87`** *(`lambda*_RG`; `lambda*_H` come `s^2.07 eps^1.83`)*: ### **la previsione `s^2 eps^2` regge in `s`, in `eps` l'esponente e' `1.87`, non `2`.**
### **Il centro della coppia/`s` va come `s^2.03 eps^1.72`, negativo.**

## 9. LA DECISIONE DI LUCA SULLO SPECCHIO *(`2026-10-23`, dopo `cbcb99c7`)*

- ### **I `4` casi su `128` che falliscono lo specchio** *(`s0 0.5`, `eta 1e-3`, banda `1`: `5.97%`, `10.74%`, `6.60%`, `5.88%`)* ### **sono NON LEGGIBILI PER LO SPECCHIO.** ### **Il criterio di
  questa corsa NON cambia, e quei casi NON passano a posteriori:** ### **il DEVE-PASSARE della sezione `8.0` resta FALLITO.**
- ### **DA ORA, nelle corse della forza:** ### **lo specchio si fissa PRIMA sul DIFFERENZIALE `(a(+eta) - a(-eta))/2`, entro il `5%`; lo specchio grezzo si stampa come lettura.** ### **Il
  criterio e' scritto in `doc/PATTERN_DI_PROVA.md`, sezione «LE CORSE DELLA FORZA: I CRITERI».**
- ### **LA LETTURA DI FISICA DI `cbcb99c7` RESTA:** ### **Hamilton confermato dalla dinamica; le due bande uguali col SOLO zero simmetrico; il fattore `a/a_RG(v_max)` `1.63`-`1.68` da spiegare.**

### ⚠ **UN MIO ERRORE, e i numeri del referto** *(dal `.jsonl`, toro `A`)*: ### **in `8.6` e nella relazione ho scritto «`a_mis/a_H` fra `0.92` e `0.98` in OGNI caso»: vale per le corse
a `eta 1e-2`** *(`0.920`-`0.976`, `128` corse)*. ### **Con quelle a `eta 1e-3`: `0.882`-`0.988`** *(`256` corse)*; ### **senza le `8` corse dei `4` casi non leggibili per lo specchio: `0.905`-`0.988`**;
### **il differenziale: `0.921`-`0.977`.** ### **Il `0.952`-`0.981` del mandato e' la portata del primo PUO'-FALLIRE** *(`eps 0`, `s0 0.05`, simmetrico: `0.9516`-`0.9808`)*. ### **La lettura non
cambia: il minimo grezzo `0.882` e' una corsa a `eta 1e-3` di un caso non leggibile per lo specchio** *(`eps 0.5`, `s0 0.5`, `Lx 96`, banda `1`, `-eta`; il differenziale li' `0.935`)*.
