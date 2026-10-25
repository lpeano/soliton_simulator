# IL PROTOTIPO DELLA CURVATURA DELLO SPAZIO SUI TRIANGOLI, IN MEMORIA (LA STRADA A1): PRIMA L'OBIEZIONE DI LUCA DAGLI SPETTRI, POI LA LUCE E LA CADUTA

> **Il mandato:** di Luca, `2026-10-25` *([[PROGETTO-CURVATURA]], [[U1-PROTOTIPO-TRIANGOLI]], [[PROGETTO-U1]], [[LORENTZ-MATERIA-INTERFERENZA]], [[DECISIONE-SOLO-TRIANGOLI]])*. ### **NESSUN CAMBIAMENTO DEL NUCLEO; `B-4` intatta.** ### **Il progetto: `doc/PROGETTO_CURVATURA.md`** *(`dc56d417`)*. ### **Lo script `csv/_curvatura_prototipo.py`; i referti `doc/referti_l2/curvatura_x_r.{txt,jsonl}` (la parte `0`) e `curvatura_prototipo.{txt,jsonl}` (la parte `1`).**
> ### **L'ERRORE DEL GUARDIANO `n.64`** *(nel mandato)*: ### **aveva sostenuto che a `cs` uniforme la curvatura non puo' cambiare il rapporto; in `A1` le lunghezze dipendono da `cs/cs_rif` anche dove `cs` e' uniforme, e la materia sente sia l'arco sia il nodo.**

**LIVELLO:** un prototipo in memoria.

## 0. LE SCELTE DI PROVA DI LUCA *(`2026-10-25`, `16:26`: per il PROTOTIPO, NON leggi del modello)*

### **la strada `A1`; il riferimento `cs_rif` = il vuoto imperturbato; l'area della placchetta con Erone dalle tre lunghezze; i versori fissi.**

## 1. LA STELLA POLARE

1. **`A14`:** ### **`A1` cambia l'angolo dello spostamento e l'area della placchetta, non la forma dei pezzi:** ### **norma, carica e Gauss come oggi** *(il sigillo `(b)`)*.
2. **Il gradino:** ### **`(c)` limiti noti:** ### **`gamma = 1`** *(Einstein)* ### **e la caduta di `g_00`.**
3. **Aggiunge un numero o una legge?** ### **Una legge di prova** *(le lunghezze `l = cs_rif/cs`)* ### **e un riferimento** *(il vuoto imperturbato; nelle scene col `cs` a mano, il valore di fondo della scena)*: ### **scelte di prova, non leggi.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`c_s`: entra ANCHE nelle lunghezze** *(il verso curvatura -> materia e luce)*.
5. **Emergente o imposto?** ### **IMPOSTO** *(`A1` mette `cs` nelle lunghezze per costruzione)*: ### **la domanda e' se ne esce la struttura della relativita' generale DA SOLA** *(la massa dal nodo, la cinetica dall'arco)*.

## 2. IL RAGIONAMENTO PRELIMINARE

### 2.1 La variante in memoria, dal codice

- ### **L'angolo dello spostamento** *(della materia e del vuoto)* ### **passa da `flussi_parziali.z_arco`, che legge `s_arco`** *(`flussi_parziali.py`, `s_arco` e `z_arco`)*: ### **la variante avvolge `s_arco` e restituisce `s_a (s_a/s_rif)`** *(`theta_a = pi s_a r_a f`, `r_a = s_a/s_rif`)*; ### **a `s_a = s_rif`: `s_a x 1.0`, ESATTO.** ### **Il Grover e la moneta** *(il nodo)* ### **non leggono `s_arco`: restano a `pi s_n`.** ### ⚠ **Chi altro legge `s_arco`:** ### **`energia_pesata`** *(`CAMM-FASE-VUOTO`, spenta con `lambda_c = None`)* ### **e il campo** *(`Campo.s_a`, calcolato PRIMA, fuori dalla variante: il tempo del campo resta `F1`)*.
- ### **Il campo:** ### **`Campo` con l'area per placchetta `A_p = (sqrt3/4) Erone(l)/Erone(1,1,1)`** *(una sottoclasse, come `CampoF2`)*; ### **con tre lati uguali a `1` e' `sqrt3/4` ESATTO.**

### 2.2 La parte `0`, sulla carta

- ### **Il generatore a `s -> 0`:** ### **`H_r = (I - P_u) + r P_-`** *(`fa7ee993`: `_u1_terzo.H_gen` e' `r = 1`; `P_- = H_gen - (I - P_u)`)*. ### ⚠ **LO ZERO SIMMETRICO:** ### **ogni pezzo porta lo scarto `-theta/2`, quindi `omega_simm = pi s [(1 + r)/2 - lambda(H_r)]`:** ### **`mu(r) = (1 + r)/2 - lambda`, e `x(r) = sqrt(2 mu0 a)`** *(la curvatura fine di `fa7ee993`)*. ### **La coppia a `K` si segue in `r` per continuita' dai livelli `mu0 = +-1/2` di `r = 1`.**
- ### **LE DUE IPOTESI, e che cosa le distingue:** ### **se la massa viene SOLO dal nodo, `mu0` non dipende da `r` e la cinetica scala col salto: `x(r) = r/4` diventa possibile** *(la previsione del guardiano)*; ### **se la massa viene anche dall'arco, `mu0(r)` cambia e `x(r) != r/4`.** ### **LA MISURA DI DA DOVE VIENE LA MASSA: `d ln mu0/d ln r` a `r = 1`** *(`0` = solo il nodo)*.
- ### **NON so** ### **quale delle due:** ### **la coppia a `K` di `H` ha `mu0 = +-1/2` a `r = 1`, e il conto di come `mu0` dipenda da `r` non l'ho fatto.**

### 2.3 La parte `1`, le previsioni

- ### **`(c)` la luce in `A1`:** ### **`omega^2 ~ s^2/A_p ~ s^4/s_rif^2`: la velocita' coordinata `cs^2/cs_rif`, `gamma = 1`, la curvatura del fascio `kappa_R2 = 2 kappa_R1`.** ### **`gamma` misurato DUE volte:** ### **dalla deflessione** *(`kappa/kappa_R1 - 1`)* ### **e dalla pendenza `d ln v/d ln cs - 1` lungo il gradiente** *(Shapiro: il tempo d'arrivo contro `int du/(c cs^2/cs_rif)`)*.
- ### **`(d)` la caduta:** ### **col pacchetto di banda di `7daa8840`, `cs_rif` = `s0`** *(il fondo della scena; a `eta -> 0` la coppia e' quella di oggi)*: ### **il differenziale con `A1` contro quello di oggi alla stessa scena** *(il rapporto)*.
- ### **`(e)` nel gradiente:** ### **il rapporto delle due `c` dal generatore al `r` locale** *(l'approssimazione localmente uniforme, DICHIARATA: la `c` della materia in un gradiente non si misura con un solo pacchetto)*.
- ### **`B`** *(solo il campo)*: ### **il rapporto delle due `c` va come `1/r` per costruzione** *(la materia non sente `r`)*.

## 3. LA PROGETTAZIONE E I CRITERI *(fissati QUI, insieme a quelli del progetto)*

| | la misura | il criterio |
|---|---|---|
| `0.1` | `x(r)`, `r` in `(0.5, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.25, 2.0)`, lo zero simmetrico | ### **DEVE: `x(1) = 1/4` entro `1e-9`**; ### **PUO' FALLIRE: `x(r) = r/4` entro `1e-6` a ogni `r`** |
| `0.2` | `pi x(r)/r` contro `pi/4`; `mu0(r)` e `d ln mu0/d ln r` | la tabella *(e una forma chiusa, se c'e')* |
| `0.3` | gli spettri completi con `A1`, `s 0.01`, `r` in `(0.8, 1.0, 1.25)`: la coppia a `K` *(la piu' vicina a `pi s mu0(r)`)*, `v_b/s` dal fit di `fa7ee993` | ### **DEVE: `v_b/s` contro `pi x(r)` entro `1e-3` relativo** *(`s 0.01`: le correzioni `O(s^2)`)* |
| `0.4` | `B`: il rapporto delle due `c` contro `r` | ### **DEVE FALLIRE PER LA CHIAVE GIUSTA: l'universalita'** *(il rapporto costante)*; ### **la chiave: `pi x(1)/r` entro `1e-6`** |
| `(a)` | `cs = cs_rif` ovunque, la variante accesa | ### **DEVE: il passo di oggi AL BIT** *(materia e campo; ogni attributo)*; ### **DEVE FALLIRE: `cs` uniforme `= 1.1 cs_rif` non e' il passo di oggi, ED e' il passo di oggi con l'angolo dello spostamento `pi s r`** *(la chiave: il blocco del tick contro quello costruito con `s_arco` moltiplicato per `r`, entro `1e-12`)* |
| `(b)` | Gauss *(`200` tick, la materia in un gradiente)*, la gauge *(`|dE| <=` stima, `rho` ed `e B` a `1e-12`)*, la reversibilita' *(`100 + 100` col rovesciamento `T`)*, l'energia *(`500` tick)*, ### **col campo `F1` e `A1`** | ### **DEVE** *(i criteri di `0b6bfde8` e di `doc/PATTERN_DI_PROVA.md`)* |
| `(c)` | la scena di `64bb2328` *(`384 x 48`, `s0 0.2`, `eta 0.2`, `cs_rif = s0`)*: `v/(cs^2/cs_rif)`; il fascio `W` in `(12, 16, 24)`, `kappa/kappa_R2`, Ehrenfest col fattore d'angolo, l'estrapolazione contro `X`; il tempo d'arrivo | ### **PUO' FALLIRE: `gamma` entro il `5%` da `1`** *(dalla deflessione estrapolata)*; ### **DEVE FALLIRE: la deflessione entro il `10%` da `R1`** *(deve venire `~2`)* |
| `(d)` | le corse di `7daa8840` *(`Lx 96`, i due rami, `eta +-1e-3`, `+-1e-2`, `0`)* a `s0 0.05`, `0.1`, `0.3`, ### **con `A1` e senza** | ### **PUO' FALLIRE: il differenziale con `A1` uguale a quello di oggi entro il `2%`** |
| `(e)` | il rapporto delle due `c` al `r` locale lungo il gradiente di `(c)` | la tabella |
| `(f)` | la caduta dei due rami; `eps 0.5` contro `eps 0` *(`s0 0.1`)* | ### **PUO' FALLIRE: entro il `2%`** |

### **Mi FERMO se** ### **una DEVE fallisce** *(committo lo stato col fallimento e mi fermo)*.

## 4. TODO DEL NEXT STEP

1. questo task history, da solo; 2. lo script e l'inventario, prima dei numeri *(una prova a vuoto ridotta)*; 3. la parte `0` e il suo referto *(un commit, con le scelte di prova nella voce `PROGETTO-CURVATURA`)*; 4. la parte `1` e il suo referto; ### **se una DEVE fallisce, FERMO.**

## 5. IL RISULTATO DELLA PARTE 0 *(dopo `7a489f2c`)*

### **IL REFERTO DELLA PARTE `0`:** `doc/referti_l2/curvatura_x_r.{txt,jsonl}` *(`csv/_curvatura_prototipo.py` `sha1-BYTE fa3d3353` al commit `7a489f2c`; il task history `f4fb6582`)*. ### **`3/4`: le DEVE passano, la PUO' FALLIRE del guardiano FALLISCE.**

| `r` | `0.5` | `0.8` | `0.9` | `0.95` | `1.0` | `1.05` | `1.1` | `1.25` | `2.0` |
|---|---|---|---|---|---|---|---|---|---|
| `mu0` | `0.43301270` | `0.45825757` | `0.47696960` | `0.48798053` | `0.50000000` | `0.51295711` | `0.52678269` | `0.57282196` | `0.86602540` |
| `x(r)` | `0.17677670` | `0.22360680` | `0.23717082` | `0.24366986` | `0.25000000` | `0.25617377` | `0.26220221` | `0.27950850` | `0.35355339` |
| `x/(r/4)` | `1.414214` | `1.118034` | `1.054093` | `1.025978` | `1.000000` | `0.975900` | `0.953463` | `0.894427` | `0.707107` |
| `pi x/r` | `1.110721` | `0.878102` | `0.827882` | `0.805802` | `0.785398` | `0.766470` | `0.748848` | `0.702481` | `0.555360` |

- ### **`x(1) = 0.250000000154` e `0.250000000070`** *(DEVE entro `1e-9`: PASSA)*.
- ### **LA FORMA: `ln x` contro `ln r` ha la pendenza `0.500000` e l'intercetta `0.250000`, il residuo `7.55e-10`: `x(r) = sqrt(r)/4`.** ### **E `mu0(r)`:** ### **la forma `(1/2) sqrt(1 - r + r^2)` coincide con la tabella a `8` cifre a ogni `r`** *(UNA LETTURA mia della tabella, controllata a mano, NON uscita dallo script)*.
- ### **DA DOVE VIENE LA MASSA: `d ln mu0/d ln r = +0.500000` a `r = 1`, i due rami:** ### **META' dal nodo e META' dall'arco** *(`0` vorrebbe dire solo il nodo)*.
- ### **GLI SPETTRI COMPLETI con `A1`** *(`s 0.01`, `r` `0.8`, `1.0`, `1.25`)*: ### **`v_b/s` `0.70246990`, `0.78538199`, `0.87807925` contro `pi x(r)` `0.70248147`, `0.78539816`, `0.87810184`: entro `2.6e-5`** *(DEVE entro `1e-3`: PASSA)*.
- ### **LA VARIANTE `B`** *(solo il campo)*: ### **il rapporto varia del `141%` sulla lista di `r`, e il rapporto per `r` e' `v_b/s` di oggi entro `1.4e-16`** *(DEVE FALLIRE per la chiave giusta: PASSA)*.

### **LA LETTURA:** ### **in `A1` il rapporto fra la `c` della materia e quella della luce in una regione uniforme e' `pi/(4 sqrt(r))`, NON `pi/4`:** ### **la luce va come `r`, la materia come `sqrt(r)`.** ### **L'OBIEZIONE DI LUCA E' FONDATA, ma nel verso opposto all'allineamento:** ### **i due orologi NON si allineano da soli; dove `cs` scende sotto il riferimento** *(`r < 1`)* ### **la materia diventa RELATIVAMENTE piu' veloce della luce** *(a `r 0.5` il rapporto e' `1.11`: oltre la luce)*, ### **dove sale, piu' lenta.** ### **La previsione del guardiano** *(`x(r) = r/4`)* ### **cade** *(errore `n.64` confermato dai numeri)*. ### **E la ragione e' la massa: per meta' viene dall'arco, quindi la materia sente `r` a meta'.**
