# LA LUCE SUI TRIANGOLI: I MODI SENZA MASSA DEL SETTORE DEL VUOTO (E DEL SISTEMA ACCOPPIATO), E LA LORO VELOCITA' CONTRO v_b

> **Il mandato:** di Luca, «la luce sui triangoli» *([[DECISIONE-SOLO-TRIANGOLI]]; [[LUCE-VINCOLO-LAMPI-GAMMA]]; il gradino prima e' `7daa8840`: il fattore e' `L`, `v_b = 0.785 s`)*. ### **Solo misure in
> memoria.** ### **`leggi.yaml`, l'impronta `2e7f795d2a52fbe7`, la convenzione nel repo e il nucleo intatti; `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE)*. ### **Importati, non copiati:**
> `_triangoli`, `_triangoli_bassa_energia`, `_triangoli_forza`, `_triangoli_fattore`, `_stabilita_triangoli` *(`green`, la cella di `36` reali)*, `_stabilita_lineare` *(`passo`, `copia`)*,
> `_screening_forme_s3.forma`, `_scala_e_zero.H_eff`, `_zero_simmetrico`. ### **L'errore del guardiano `n.58`** *(`L ~ 1/1.37`)* ### **e' nel mandato.**

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una MISURA: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica.**
2. **Il gradino:** ### **`(A)` il vuoto da solo; `(B)` il sistema accoppiato; `(C)` il cono di tutti i settori.**
3. **Aggiunge un numero o una legge?** ### **No.** ### **I lati, le `s`, le `x`, le soglie del fronte sono scelte di misura, dichiarate.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No: `cs` uniforme.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **c'e' un segnale senza massa che definisca la «luce», e va a `v_b`?**

## 1. DAL CODICE, PRIMA DI SCRIVERE *(il mandato lo chiede; dal sorgente eseguibile)*

- ### **L'ORDINE** *(`composizione.ORDINE`, `14` pezzi, palindromo, tutti a frazione `0.5`)*: ### **`MATERIA-VUOTO`, `FASE-VUOTO`, `MONETA-SPIN`, `GROVER`, `SPOSTAMENTO`, `GROVER-VUOTO`, `SPOSTAMENTO-VUOTO`,
  `SPOSTAMENTO-VUOTO`, `GROVER-VUOTO`, `SPOSTAMENTO`, `GROVER`, `MONETA-SPIN`, `FASE-VUOTO`, `MATERIA-VUOTO`.**
- ### **I PEZZI CHE AGISCONO SU `phi`:**
  - ### **`CAMM-GROVER-VUOTO`** *(`termini/camm_grover_vuoto.py`, operatore `grover_scalare`, azione `nodo`)*: ### **la STESSA `flussi_parziali.grover` dello spinore, `G(theta) = P_u + e^{i theta}(I - P_u)` sulle `2d =
    6` estremita' del nodo, su una vista a UNA componente**; ### **l'angolo per nodo `theta = pi dtau cs x frazione`** *(`z_nodo`)*.
  - ### **`CAMM-SPOSTAMENTO-VUOTO`** *(`camm_spostamento_vuoto.py`, `spostamento_scalare`, azione `arco`)*: ### **`flussi_parziali.hop_phi`, `alpha I + beta S` con `S` la permutazione PURA delle due estremita'
    dell'arco, SENZA `U`** *(il vuoto e' neutro)*; ### **`alpha = (1 + e^{i theta})/2`, `beta = (1 - e^{i theta})/2`, l'angolo d'arco `z_arco`** *(la media armonica dei `dtau` dei due nodi)*.
  - ### **`CAMM-MATERIA-VUOTO`** *(il legame, `N_k = rho_k ln(rho_k/(rho_k + Lambda_k))`)*: ### **una FASE su `phi` con `beta = dN/dLambda = -rho/(rho + Lambda)`** ### **-- NULLA se la materia e' nulla**; ### **e
    una fase su `psi` con `alpha = ln(rho/(rho + Lambda)) + Lambda/(rho + Lambda)`.** ### ⚠ **A `rho -> 0` `alpha` diverge come `ln rho`:** ### **la linearizzazione della MATERIA attorno a `psi = 0`
    e' singolare** *(il codice mette `alpha = 0` solo a `psi = 0` ESATTO)*.
  - ### **`CAMM-FASE-VUOTO`** *(`motore._fase_vuoto` -> `energia_pesata.applica`)*: ### **«A FORMA SPENTA NON FA NIENTE: `mot.cs is None`»** ### **-- nelle scene di questa misura `cs` e' spento: NON agisce.**
- ### **IL VUOTO DA SOLO E' DUNQUE UNA CAMMINATA DI GROVER SCALARE** *(lineare)*: ### **il blocco `12:18` della matrice del tick** *(la materia e il vuoto NON si mescolano nella camminata: il blocco
  materia-vuoto e' `0.0`)*.

## 2. VISTO IN MEMORIA *(i numeri li ristampa lo strumento)*

- ### **Il vuoto, `s 0.05`, zero di oggi:** ### **a `Gamma` `0` (semplice), `-pi s` (doppio, PIATTO), `-2 pi s`; la banda che parte da `0` va come `k^2`** *(`-0.000225`, `-0.000896`, `-0.003555` ai primi
  passi `1, 2, 4`: `x4` raddoppiando)*. ### **Col simmetrico: due bande PIATTE a `0`, due a `-pi s`, e una coppia DISPERSIVA `+-pi s` a `Gamma`, `+-pi s/2` a `K`** *(la stessa struttura della coppia della
  materia)*. ### **NESSUNA pendenza lineare.**
- ### **L'accoppiato:** ### **lo spinore allineato della scena NON e' stazionario** *(`0.31`)*: ### **la base dev'essere un AUTOSTATO uniforme** *(un vettore della materia a `Gamma`)*: ### **il livello `0`
  di oggi** *(doppio: la banda ALTA della coppia a `Gamma`, `+pi s` col simmetrico)* ### **e' stazionario entro `2.5e-15`.**

## 3. IL METODO

### **PARTE A** *(materia nulla; `s` in `(0.02, 0.05, 0.1, 0.3, 0.5)`; zero simmetrico e di oggi)*
- ### **Il blocco del vuoto `A_v(k)`** *(`6 x 6`, da `_triangoli_bassa_energia.matrice` al lato `48`)*; ### **i livelli a `Gamma`, `K`, `K'`, `M`; le bande PIATTE** *(variazione su tutta la zona `< 1e-9`)*;
  ### **i TOCCHI** *(due livelli distinti entro `1e-9` a un punto speciale, o un livello a `0`)* ### **e, per ogni tocco, la dispersione lungo `16` direzioni da quel punto:** ### **`delta omega(k)` a `k`
  in `(1, 2, 4) x 1e-3`** *(cartesiano, `A_v` esatta dai blocchi in spazio reale)*, ### **l'esponente** *(`ln` del rapporto: `1` lineare, `2` quadratico)* ### **e, se lineare, `v_luce` = la pendenza,
  l'anisotropia, `v_luce/s`.**
- ### **La `v` di Einstein del vuoto** *(come la materia in `7daa8840`)*: ### **per la banda dispersiva a `Gamma` col simmetrico, `v_b,vuoto = sqrt(omega(0) omega'')`.**
- ### **Il fronte del solo vuoto:** ### **un impulso su `phi` a un nodo** *(le `6` estremita' uguali)*, ### **toro `192 x 192`, `100` tick, le tre soglie di `7daa8840`.**
- ### **Il confronto con `v_b/s = 0.785` e `v_max/s = 0.599`.**

### **PARTE B** *(il sistema accoppiato; `eps 0`; `s` in `(0.05, 0.1, 0.3)`; `x` in `(1e-4, 1e-3, 1e-2)`; le forme `S1`, `S3`, `S4` con `_screening_forme_s3.forma`)*
- ### **LA BASE:** ### **`psi` = il vettore della banda alta della coppia a `Gamma`** *(oggi `0`, doppio: il primo)*, ### **uniforme, riscalato a `rho/Lambda = x`; `phi = 1`** *(`Lambda0 = 6`)*; ### **la
  stazionarieta' controllata** *(un tick, le due fasi globali)*.
- ### **LA FUNZIONE DI GREEN di un tick** *(`_stabilita_triangoli.green`, `eps_rel 1e-6`)* ### **nel riferimento che ruota con le due fasi** *(come `_gravita_collettiva.stabilita`)*, ### **lato `48`:** ### **gli
  angoli degli autovalori ai `k` lungo `theta_1` da `Gamma`** *(`m = 0..6`)*, ### **i modi che vanno a `0` a `Gamma`, il loro esponente in `k` e, se lineari, la velocita'** *(un SUONO)*; ### **il tasso
  `max ln|lambda|/s`.**
- ### **A materia nulla:** ### **il blocco `phi -> phi` della Green** *(con `eps_rel = 1`: la mappa e' ESATTAMENTE lineare)* ### **contro la rappresentazione reale di `A_v`** *(il controllo DEVE)*; ### **il blocco della
  materia NO: e' singolare** *(sezione `1`)*.

### **PARTE C** *(`s` in `(0.05, 0.3, 0.5)`)*: ### **`v_max` della materia** *(`_triangoli_forza.v_max`)* ### **e del vuoto** *(la stessa funzione, col blocco del vuoto messo al posto della materia e un
blocco identita' nel resto: velocita' nulla, non cambia il massimo)*; ### **il cono vero = il massimo dei due; contro `v_b`, `v_luce`, `v_max` della materia.**

## 4. LE PREVISIONI *(prima dei numeri dello strumento)*

- ### **IL VUOTO NON HA UN MODO SENZA MASSA LINEARE:** ### **il generatore a `s` piccolo e' `pi s [(I - P_u) + (I - S)/2] >= 0`, col nucleo di dimensione `1` a `Gamma`: la banda che lo tocca va come `k^2`.**
  ### **IL PRIMO PUO'-FALLIRE FALLISCE** *(«esiste un modo senza massa del vuoto»: c'e' un modo a frequenza nulla, ma quadratico)*, ### **e il SECONDO non si puo' leggere** *(senza `v_luce`, fallisce
  per assenza)*.
- ### **`v_b,vuoto/s ~ 1.1`** *(un conto a mano dai numeri visti)*.
- ### **IL CONO DI TUTTI I SETTORI:** ### **non lo prevedo con sicurezza;** ### **se il vuoto ha la stessa struttura della materia, `~0.6 s` -- sotto `v_b`: il terzo PUO'-FALLIRE FALLIREBBE.**
- ### **L'ACCOPPIATO:** ### **due modi a frequenza nulla a `Gamma`** *(le fasi globali di `psi` e di `phi` sono simmetrie del passo)*; ### **un SUONO alla Bogoliubov con velocita' `~ sqrt(x)`:
  molto sotto `v_b` a `x <= 1e-2`**; ### **`S3` instabile, `S1` stabile** *(come la materia diluita sul quadrato)*.

## 5. I CRITERI, FISSATI ORA *(dal mandato; la portata dove non la dice)*

- ### **DEVE PASSARE: lo spettro del vuoto invariante per `60` gradi** *(`_triangoli.scarto_c6`, sul cerchio)* ### **entro `1e-12`, ogni `s` e convenzione.**
- ### **DEVE PASSARE: un pezzo solo** *(`CAMM-GROVER-VUOTO` o `CAMM-SPOSTAMENTO-VUOTO`)*, ### **sul blocco del vuoto: `delta(s) = ||H_eff(s) - H_eff(0.02)||/||H_eff(0.02)|| < 1e-12`** *(il generatore `exp(i pi s P)` lineare in
  `s`; `Gamma` e `k(1,0)`, lato `16`)*.
- ### **DEVE PASSARE: a materia nulla il blocco `phi -> phi` della Green = `A_v` entro `1e-12`.**
- ### **DEVE FALLIRE, per la chiave giusta:** ### **«il settore della materia a `eps 0` ha un modo senza massa»** *(il salto della coppia a `K` `< 1e-6`)*: ### **la chiave: la coppia c'e', e il salto e' quello
  di `8781162c` entro `1e-9`.**
- ### **PUO' FALLIRE: esiste un modo senza massa LINEARE del vuoto a `s 0.05`.**
- ### **PUO' FALLIRE: `|v_luce/s - 0.785|/0.785 < 0.05` a `s 0.05`.**
- ### **PUO' FALLIRE: il cono di tutti i settori `>= v_b`** *(ogni `s` della parte `C`)*.
- ### **IL VERDETTO DI FISICA: le tabelle.** ### **A parte: tre righe di lettura; quale e' la luce del modello sui triangoli, se c'e'; che cosa vuol dire per la relativita' ristretta e per la prova di
  Lorentz** *(`doc/SPAZIOTEMPO_3PIU1.md`, `G`)*: ### **informazione per Luca, non una scelta.**

## 6. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_triangoli_luce.py` e la sua voce nell'inventario, committati prima dei numeri;
3. la corsa, il referto, la relazione *(e il collegamento a `LUCE-VINCOLO-LAMPI-GAMMA`)*, la sezione `7`.

## 7. I RISULTATI *(scritti dopo la corsa, sotto)*
