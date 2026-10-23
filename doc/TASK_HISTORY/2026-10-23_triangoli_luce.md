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

### 📝 **ANNOTAZIONE 1** *(prima della corsa, nel commit dello strumento)*: ### **la prova a vuoto ridotta** *(`s 0.05`; `S3`/`S1`, `s 0.1`, `x 1e-2`)* ### **ha trovato UN mio difetto, corretto
prima del commit:** ### **il riferimento del DEVE della parte `B`** *(la Green a materia nulla contro il blocco del vuoto)* ### **era sbagliato: la Green lavora sulle coordinate REALI, e la sua trasformata
accoppia `k` e `-k`** *(la parte reale della mappa in spazio reale e' `(V(k) + V(-k)*)/2`, non `Re V(k)`)*: ### **`5.2e-2` col riferimento sbagliato, `1.0e-15` con quello giusto.** ### **E UNA COSA CHE NON E' UN
DIFETTO, e cambia la lettura:** ### **a `eps 0` la MATERIA e' DUE COPIE della camminata del vuoto** *(`U = I`, la moneta spenta: le due componenti dello spinore non si mescolano)*: ### **il fronte e `v_max` del
vuoto sono quelli della materia** *(`0.5990` contro `0.5989`)*, ### **e la coppia a `K` del vuoto e' la stessa.** ### **I NUMERI VISTI** *(non li uso)*: ### **il vuoto senza pendenze lineari** *(esponente
`2.000` ai tocchi)*; ### **`v_b,vuoto/s = 1.11` a `Gamma`**; ### **`S1` stabile** *(il tasso `3e-6`, il rumore della differenza finita)*, ### **`S3` instabile** *(`0.90`)*; ### **i rami bassi
dell'accoppiato quadratici** *(esponente `~2`: nessun suono a `x 1e-2`)*.

## 6. TODO DEL NEXT STEP

1. questo task history, da solo, committato e pushato;
2. `csv/_triangoli_luce.py` e la sua voce nell'inventario, committati prima dei numeri;
3. la corsa, il referto, la relazione *(e il collegamento a `LUCE-VINCOLO-LAMPI-GAMMA`)*, la sezione `7`.

## 7. I RISULTATI *(scritti dopo la corsa, sotto)*

> **La corsa:** ### **strumento `csv/_triangoli_luce.py` sha1-BYTE `6d3970a3`; referto `doc/referti_l2/triangoli_luce.txt` sha1-BYTE `2ede1886`, `.jsonl` `5a93de5b`; `6` minuti.** ### **Le tabelle sono GENERATE
> dal `.jsonl`.** ### **`5` controlli su `8`: TUTTI i DEVE passano; falliscono i TRE PUO'-FALLIRE, come avevo previsto.**

### 7.0 I CONTROLLI

| criterio | esito | il numero |
|---|---|---|
| di servizio: il blocco materia-vuoto della camminata nullo | **PASSA** | `0.0` |
| DEVE: il vuoto invariante per `60` gradi | **PASSA** | `2.40e-15` |
| DEVE: un pezzo solo sul vuoto, `delta(s) < 1e-12` | **PASSA** | `6.2e-15` |
| DEVE: a materia nulla il blocco `phi -> phi` della Green = il vuoto | **PASSA** | `1.4e-15` |
| DEVE FALLIRE: la materia a `eps 0` ha un modo senza massa | **fallisce, come deve** | il salto `0.156958` = `8781162c` |
| PUO': esiste un modo senza massa LINEARE del vuoto a `s 0.05` | ### **FALLISCE** *(previsto)* | `0` rami lineari, a nessuna `s` |
| PUO': `v_luce` entro il `5%` da `v_b` | ### **FALLISCE** *(previsto: per assenza)* | nessun `v_luce` |
| PUO': il cono di tutti i settori `>= v_b` | ### **FALLISCE** *(previsto)* | cono`/v_b`: `0.7631`, `0.7949`, `0.8592` |

### 7.1 PARTE A -- IL VUOTO DA SOLO

| `s` | conv | livelli a `Gamma` *(molteplicita')* | a `K` | piatte | i tocchi *(punto, livello: i rami)* | `v_b,vuoto/s` *(a `Gamma`, `+pi s`)* | fronte`/s` *(1e-2, 1e-4, 1e-6)* |
|---|---|---|---|---|---|---|---|
| `0.02` | simm | `-0.0628`(3) `-0.0000`(2) `+0.0628`(1) | `-0.0628`(2) `-0.0314`(1) `-0.0000`(2) `+0.0314`(1) | `-0.0628` `-0.0000` | Gamma -0.0628: piatto, piatto, quadratico (2.00) | `1.1109` | `0.6458` `1.0000` `1.3944` |
| `0.02` | oggi | `-0.1257`(3) `-0.0628`(2) `-0.0000`(1) | `-0.1257`(2) `-0.0942`(1) `-0.0628`(2) `-0.0314`(1) | `-0.1257` `-0.0628` | Gamma -0.1257: piatto, piatto, quadratico (2.00); Gamma -0.0000: quadratico (2.00) | -- | `0.6458` `1.0000` `1.3944` |
| `0.05` | simm | `-0.1571`(3) `+0.0000`(2) `+0.1571`(1) | `-0.1571`(2) `-0.0785`(1) `+0.0000`(2) `+0.0785`(1) | `-0.1571` `+0.0000` | Gamma -0.1571: piatto, piatto, quadratico (2.00) | `1.1119` | `0.5436` `0.6895` `0.7678` |
| `0.05` | oggi | `-0.3142`(3) `-0.1571`(2) `+0.0000`(1) | `-0.3142`(2) `-0.2356`(1) `-0.1571`(2) `-0.0786`(1) | `-0.3142` `-0.1571` | Gamma -0.3142: piatto, piatto, quadratico (2.00); Gamma +0.0000: quadratico (2.00) | -- | `0.5436` `0.6895` `0.7678` |
| `0.1` | simm | `-0.3142`(3) `-0.0000`(2) `+0.3142`(1) | `-0.3142`(2) `-0.1566`(1) `-0.0000`(2) `+0.1566`(1) | `-0.3142` `-0.0000` | Gamma -0.3142: piatto, piatto, quadratico (2.00) | `1.1153` | `0.5704` `0.6913` `0.7849` |
| `0.1` | oggi | `-0.6283`(3) `-0.3142`(2) `+0.0000`(1) | `-0.6283`(2) `-0.4708`(1) `-0.3142`(2) `-0.1576`(1) | `-0.6283` `-0.3142` | Gamma -0.6283: piatto, piatto, quadratico (2.00); Gamma +0.0000: quadratico (2.00) | -- | `0.5704` `0.6913` `0.7849` |
| `0.3` | simm | `-0.9425`(3) `+0.0000`(2) `+0.9425`(1) | `-0.9425`(2) `-0.4580`(1) `+0.0000`(2) `+0.4580`(1) | `-0.9425` `+0.0000` | Gamma -0.9425: piatto, piatto, quadratico (2.00) | `1.1550` | `0.5989` `0.6500` `0.6685` |
| `0.3` | oggi | `-1.8850`(3) `-0.9425`(2) `-0.0000`(1) | `-1.8850`(2) `-1.4005`(1) `-0.9425`(2) `-0.4845`(1) | `-1.8850` `-0.9425` | Gamma -1.8850: piatto, piatto, quadratico (2.00); Gamma -0.0000: quadratico (2.00) | -- | `0.5989` `0.6500` `0.6685` |
| `0.5` | simm | `-1.5708`(3) `-0.0000`(2) `+1.5708`(1) | `-1.5708`(2) `-0.7227`(1) `+0.0000`(2) `+0.7227`(1) | `-1.5708` `-0.0000` | Gamma -1.5708: piatto, piatto, quadratico (2.00) | `1.2533` | `0.6334` `0.6568` `0.6827` |
| `0.5` | oggi | `-1.5708`(2) `-0.0000`(1) `+3.1416`(3) | `-3.1416`(2) `-2.2935`(1) `-1.5708`(2) `-0.8481`(1) | `-1.5708` `+3.1416` | Gamma -0.0000: quadratico (2.00); Gamma +3.1416: piatto, piatto, quadratico (2.00) | -- | `0.6334` `0.6568` `0.6827` |

### 7.2 PARTE B -- IL SISTEMA ACCOPPIATO *(la base: la banda alta della coppia a `Gamma`; il tasso per `s`, zero simmetrico e di oggi; il ramo piu' basso lungo `theta_1`: l'angolo al primo passo e l'esponente in `k`)*

| forma | `s` | `x` | tasso simm | tasso oggi | il ramo basso: angolo al passo `1`, esponente |
|---|---|---|---|---|---|
| S1 | `0.05` | `0.0001` | `+3.51e-08` | `+4.65e-08` | `2.246e-04`, `1.99` |
| S1 | `0.05` | `0.001` | `+7.08e-07` | `+3.79e-07` | `2.245e-04`, `1.99` |
| S1 | `0.05` | `0.01` | `+5.74e-08` | `+1.01e-07` | `2.143e-04`, `2.02` |
| S1 | `0.1` | `0.0001` | `+1.99e-08` | `+2.62e-08` | `4.520e-04`, `1.99` |
| S1 | `0.1` | `0.001` | `+1.30e-07` | `+2.08e-07` | `4.518e-04`, `1.99` |
| S1 | `0.1` | `0.01` | `+3.31e-06` | `+3.08e-08` | `4.313e-04`, `2.02` |
| S1 | `0.3` | `0.0001` | `+1.18e-08` | `+4.05e-09` | `1.454e-03`, `1.99` |
| S1 | `0.3` | `0.001` | `+1.52e-09` | `+5.18e-09` | `1.453e-03`, `1.99` |
| S1 | `0.3` | `0.01` | `+4.07e-08` | `+1.63e-06` | `1.392e-03`, `2.02` |
| S3 | `0.05` | `0.0001` | `+9.06e-01` | `+9.06e-01` | `2.246e-04`, `1.99` |
| S3 | `0.05` | `0.001` | `+9.06e-01` | `+9.06e-01` | `2.246e-04`, `1.99` |
| S3 | `0.05` | `0.01` | `+8.98e-01` | `+8.98e-01` | `2.246e-04`, `1.99` |
| S3 | `0.1` | `0.0001` | `+9.04e-01` | `+9.04e-01` | `4.520e-04`, `1.99` |
| S3 | `0.1` | `0.001` | `+9.03e-01` | `+9.03e-01` | `4.520e-04`, `1.99` |
| S3 | `0.1` | `0.01` | `+8.96e-01` | `+8.96e-01` | `4.520e-04`, `1.99` |
| S3 | `0.3` | `0.0001` | `+8.80e-01` | `+8.80e-01` | `1.114e-09`, `-0.17` |
| S3 | `0.3` | `0.001` | `+8.79e-01` | `+8.79e-01` | `1.454e-03`, `1.99` |
| S3 | `0.3` | `0.01` | `+8.72e-01` | `+8.72e-01` | `1.454e-03`, `1.99` |
| S4 | `0.05` | `0.0001` | `+1.11e-02` | `+1.11e-02` | `2.246e-04`, `1.99` |
| S4 | `0.05` | `0.001` | `+4.73e-02` | `+4.73e-02` | `2.246e-04`, `1.99` |
| S4 | `0.05` | `0.01` | `+1.89e-01` | `+1.89e-01` | `2.246e-04`, `1.99` |
| S4 | `0.1` | `0.0001` | `+1.10e-02` | `+1.10e-02` | `4.520e-04`, `1.99` |
| S4 | `0.1` | `0.001` | `+4.73e-02` | `+4.73e-02` | `4.520e-04`, `1.99` |
| S4 | `0.1` | `0.01` | `+1.89e-01` | `+1.89e-01` | `4.520e-04`, `1.99` |
| S4 | `0.3` | `0.0001` | `+1.08e-02` | `+1.08e-02` | `1.454e-03`, `1.99` |
| S4 | `0.3` | `0.001` | `+4.75e-02` | `+4.75e-02` | `1.454e-03`, `1.99` |
| S4 | `0.3` | `0.01` | `+1.88e-01` | `+1.88e-01` | `1.454e-03`, `1.99` |

### 7.3 PARTE C -- IL CONO DI TUTTI I SETTORI

| `s` | `v_max` materia`/s` | `v_max` vuoto`/s` | il cono`/s` | `v_b/s` *(`7daa8840`)* | cono`/v_b` |
|---|---|---|---|---|---|
| `0.05` | `0.5989` | `0.5990` | `0.5990` | `0.7850` | `0.7631` |
| `0.3` | `0.6120` | `0.6122` | `0.6122` | `0.7701` | `0.7949` |
| `0.5` | `0.6351` | `0.6351` | `0.6351` | `0.7391` | `0.8592` |

### 7.4 LA LETTURA *(tre righe)*

1. ### **IL VUOTO NON HA LUCE:** ### **nessun ramo lineare a nessuna `s`** *(i tocchi sono tutti quadratici, esponente `2.00`)*; ### **a `eps 0` la materia e' DUE COPIE della camminata del vuoto** *(`U = I`,
   moneta spenta)*, ### **quindi il vuoto ha la STESSA coppia massiva a `K`, lo stesso `v_max`** *(`0.599 s`)* ### **e lo stesso fronte.** ### **La banda dispersiva del vuoto a `Gamma` ha `v_b,vuoto = 1.11 s`.**
2. ### **IL SISTEMA ACCOPPIATO NON CREA UN SUONO:** ### **i rami bassi restano quadratici** *(esponente `1.99`-`2.02`)* ### **per `S1`, `S3`, `S4`, ogni `s` e `x` -- tranne `S3`, `s 0.3`, `x 1e-4`, dove il primo ramo ha un angolo `~1e-9` a ogni `k` *(esponente `-0.17`, `-0.09`): un modo a frequenza NULLA in piu', non lineare** *(non lo spiego)*; ### **`S1` e' stabile** *(il tasso `<= 3.3e-6`, il
   rumore della differenza finita)*, ### **`S3` instabile** *(`0.87`-`0.91`)*, ### **`S4` instabile e crescente con `x`** *(`0.011`, `0.047`, `0.19`)*.
3. ### **IL CONO DEI SEGNALI E' `v_max = 0.60`-`0.64 s` IN TUTTI I SETTORI** *(materia e vuoto uguali)*, ### **SOTTO `v_b` del modo a `K`** *(`0.76`-`0.86 v_b`)*: ### **la particella vede una `c` che nessun segnale
   raggiunge.**

### 7.5 QUAL E' LA LUCE DEL MODELLO SUI TRIANGOLI

### **NON C'E':** ### **ne' il vuoto ne' il sistema accoppiato hanno un modo senza massa lineare** *(fra `s 0.02` e `0.5`, `x` fino a `1e-2`)*. ### **Il modello ha un CONO** *(la `v_max` dei segnali, `0.60`-`0.64 s`)* ### **ma
nessun FOTONE che lo percorra.**

### 7.6 CHE COSA VUOL DIRE PER LA RELATIVITA' RISTRETTA E LA PROVA DI LORENTZ *(informazione per Luca, non una scelta)*

### **La gravita' sui triangoli e' quella della relativita' generale se la «luce» va a `v_b`** *(`7daa8840`)*; ### **ma nel modello nessun segnale va a `v_b`: il cono e' `1.3` volte piu' lento.** ### **E' un problema
di RELATIVITA' RISTRETTA, non di gravita':** ### **la dispersione del modo massivo non e' invariante rispetto al cono della camminata.** ### **Per la prova di Lorentz** *(`doc/SPAZIOTEMPO_3PIU1.md`, `G` punto `3`)*: ### **sui
triangoli fallirebbe gia' a riposo** *(la relazione di Einstein del modo non usa la velocita' del cono)*; ### **resta da vedere se la moneta** *(`eps > 0`)* ### **o la FCC cambiano il quadro.**
