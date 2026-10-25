# IL PROGETTO DELLA CURVATURA DELLO SPAZIO *(sulla carta: nessun codice, nessuna decisione)*

> **Il mandato:** di Luca, `2026-10-25`, parte `2` *([[PROGETTO-CURVATURA]], [[PROGETTO-U1]], [[U1-PROTOTIPO-TRIANGOLI]], [[SPAZIOTEMPO-3PIU1]], [[DOMANDA-D9-GEOMETRIA]], [[LORENTZ-MATERIA-INTERFERENZA]])*. ### **Il piano: `83f6a8bd`; il task history: `doc/TASK_HISTORY/2026-10-25_progetto_curvatura.md` (`4e0272d7`).**
> ### **Ogni affermazione sul codice e' letta dal sorgente** *(file e riga del blob di oggi; i numeri di riga invecchiano: si cerca per nome di funzione)*. ### **Ogni `[RACCOMANDAZIONE]` e' mia; la scelta e' di Luca.**

## 1. LO SCOPO E IL CRITERIO

- ### **In relativita' generale, campo debole, coordinate isotrope:** ### **`ds^2 = cs^2 dt^2 - cs^-2 dx^2`** *(`cs ~ 1 + Phi`)*: ### **il tempo va come `cs`, le lunghezze proprie come `1/cs`; la velocita' COORDINATA della luce va come `cs^2`; la deflessione e' quella di Einstein** *(`R2`, doppia di Soldner)*; ### **il ritardo di Shapiro ha il fattore `1 + gamma`, `gamma = 1`.**
- ### **La particella lenta:** ### **`H = cs sqrt(m^2 + cs^2 p^2) ~ cs m + cs^3 p^2/(2m)`** *(la massa pesata dal TEMPO, la cinetica da tempo e LUNGHEZZE)*: ### **la caduta dipende solo da `g_00`** *(a campo debole)*.
- ### **Oggi il modello ha `gamma = 0`:** ### **`cs` solo nel tempo** *(`64bb2328`: `0.84` di `R1`, `0.42` di `R2`; `fa7ee993`: col fascio largo fino a `0.875` di `R1`)*.
- ### ⭐ **IL CRITERIO DI SUCCESSO:** ### **`gamma = 1` misurato dalla deflessione E dal ritardo, con la caduta delle particelle lente INVARIATA** *(rispetto a `cbcb99c7` e `7daa8840`)* ### **e il rapporto fra la `c` della materia e quella della luce MISURATO** *(l'obiezione di Luca, il passo `2` del piano)*.

## 2. CHE COSA C'E' OGGI *(dal codice)*

| | dove | che cosa |
|---|---|---|
| `cs` nel tempo del nodo | `primo_ordine/flussi_parziali.py`, `dtau_nodo` *(riga `76`)*, `s_nodo` *(`171`)* | `dtau_k = cs_k dt`, `s = dtau/dtau_rif`, `dtau_rif = 1` |
| `cs` nel tempo dell'arco | `flussi_parziali.py`, `s_arco` *(`184`)* | la media armonica `B-3` dei due nodi |
| l'angolo | `flussi_parziali.py`, `espi` *(`246`)*, `z_arco` *(`305`)* | `theta = pi s f` *(`B-4`)* |
| lo spostamento | `flussi_parziali.py`, `hop_psi` *(`378`)*; `motore.py`, `_spostamento_trasporto` *(`520`)* | `alpha I + beta S_U`: ### **TOPOLOGICO** *(`ii`, `jj`; nessuna lunghezza)* |
| la geometria | `motore.py`, `Geometria` *(`102`)*: `n` per estremita', `U` per arco | ### **SOLO direzioni e trasporti, nessuna lunghezza**; `n` entra nella moneta *(`_moneta_spin`, `464`; `_ruota_attorno_a_n`, `484`)* e nell'elicita' |
| i versori dei triangoli | `csv/_triangoli.py`, `TRIANGOLI` *(`60`)*, `versori` *(`97`)* | `0`, `120`, `60` gradi: ### **il triangolo EQUILATERO per costruzione** |
| il campo `U(1)` | `csv/_u1_prototipo.py`, `L_SU_LS` *(`45`)*, `AREA` *(`46`)*; `Campo.forza` *(`162`)*, `deriva` *(`170`)* | `l = 1`, `l* = 1/sqrt3`, `A_p = sqrt3/4` FISSI *(`0074d9f9`)*; `F1`: la deriva `s_a^2 (l/l*)` |

### ⚠ **QUINDI:** ### **nell'era `2` NESSUNA lunghezza entra nel passo:** ### **la camminata e' topologica, gli angoli sono tempi, il campo ha i pesi di un triangolo fisso.** ### **La curvatura dello spazio deve entrare da UNA delle tre porte: l'angolo dello spostamento, i pesi del campo, o una variabile nuova sull'arco.**

### 2.1 L'ERA `1` *(`soliton_simulator.py`, blob `b8c21049`)*

| | dove | si prende? |
|---|---|---|
| ### **la metrica dinamica** `d'' = c_s^2 Lap(d - d0) + a (rho - P_eq)/P_eq - b d'` | ### **l'intestazione** *(riga `23`)*; ### **`Rete.step`** *(`7485`)*, ### **il Verlet di `d` e `vd`** *(`~8160`-`8211`)* | ### **L'IDEA SI'** *(le lunghezze sono variabili dell'arco, la materia le sorgente: «corr. materia-deformazione misurata: da `+0.34` a `+0.79`», riga `26`)*; ### **LA FORMA NO:** ### **lo smorzamento `beta` rompe la reversibilita'** *(`A14`)*; ### **`c_s^2` della metrica e' una costante** *(`CS_M`)*; ### **i sotto-passi CFL sono un numero** |
| ### **`d0`, la lunghezza di riposo** | ### **`d0`** *(il registro, riga `256`)*; ### **la memoria plastica `TAU_P`** | ### **NO, per ora:** ### **i pavimenti di `d0` sono stati archiviati** *(righe `194`-`195`: `A11`)*; ### **la plasticita' e' un'altra legge** |
| ### **`PLAST_DIN`** | ### **riga `3117`** *(OFF)* | ### **NO:** ### **e' una legge dell'era `1` su `d0`, con `tanh` e torsione** |
| ### **le coordinate** `pos` | ### **riga `2114`; l'intestazione `12`-`15`** *(«servono solo al disegno»)* | ### **NO:** ### **l'era `2` non ha coordinate** |
| ### **la mitosi** *(il criterio `2 pi`)* | ### **l'intestazione `29`-`34`** | ### **PIU' AVANTI** *(la strada `(C)`, [[DOMANDA-D9-GEOMETRIA]])* |

### ⚠ **IL CONTRASTO, riportato:** ### **il mandato cita «il capitolo "la metrica viva" nella memoria del progetto»:** ### **NON l'ho trovato nel repo** *(cercato in `doc/`, nei `.md`, `.py`, `.yaml`)* ### **ne' nella mia memoria:** ### **se e' nella memoria di Luca, va portato nel repo.**

## 3. LE STRADE

### **`(A)` `cs` NELLE LUNGHEZZE PER COSTRUZIONE:** ### **ogni arco ha la lunghezza propria `l_a = cs_rif/cs_a`.**
- ### **NELLA CAMMINATA:** ### **l'angolo dello spostamento e' (tempo proprio)/(lunghezza propria): `theta_a = pi s_a (s_a/s_rif) f`.** ### **DUE VARIANTI:**
  - ### **`(A1)` solo i pezzi dell'ARCO** *(gli spostamenti, della materia e del vuoto)* ### **sentono la lunghezza; il Grover e la moneta** *(il nodo, l'orologio)* ### **restano a `pi s_n`.** ### **E' la struttura di `H = cs m + cs^3 p^2/(2m)` SE la massa viene dal nodo e il salto dall'arco:** ### **la massa `~ s`, la cinetica `~ t^2/Delta ~ s r^2`** *(`r = s/s_rif`)*.
  - ### **`(A2)` TUTTI i pezzi scalati di `r`:** ### **il generatore diventa `r H`, quindi il rapporto delle due `c` resta `pi/4` PER COSTRUZIONE** *(un cambio di scala, come la variante `theta = s/x` di `fa7ee993`)* ### **ma la massa va come `s r = s^2/s_rif`: la caduta RADDOPPIA** *(contro `g_00`)*.
- ### **NEL CAMPO:** ### **i pesi del calcolo esterno discreto con le lunghezze `l_a`:** ### **in 2D la stella dei `1`-forme e' INVARIANTE CONFORME** *(`l*/l` fisso)*, ### **quella dei `2`-forme va come `1/A_p`:** ### **`omega^2 ~ s^2/A_p ~ s^4/s_rif^2`: la velocita' coordinata `s^2/s_rif`, `gamma = 1`.** ### **`A_p` dalle TRE lunghezze dell'arco** *(Erone, normalizzato a `sqrt3/4` quando i tre lati sono `1`)*: ### **nessuna regola per la placchetta** *(a differenza di `F2`)*.
- ### ⚠ **IL PUNTO CHE NON SO, e che decide:** ### **la massa della coppia a `K` viene dal nodo, dall'arco, o da entrambi?** ### **Il generatore `H_r = (I - P_u) + r P_-`** *(`fa7ee993`: `x = 1/4` a `r = 1`)* ### **lo dice SENZA NESSUNA CORSA:** ### **in `(A1)` il rapporto delle due `c` in una regione uniforme a `r != 1` e' `pi x(r)/r`;** ### **la previsione del guardiano** *(«il rapporto resta `pi/4`»)* ### **vale se e solo se `x(r) = r/4`.**

### **`(B)` `cs` NEI PESI DEL SOLO CAMPO** *(`l`, `l*`, `A_p`)*, ### **la materia col tempo dell'arco di oggi:** ### **la luce va a `s^2/s_rif` e devia come Einstein, la materia no:** ### **il rapporto delle due `c` va come `1/r`** *(l'obiezione di Luca realizzata PER COSTRUZIONE)*: ### **VIOLA l'universalita' fra materia e luce** *(il principio di equivalenza)*. ### **Utile solo come CONTROLLO.**

### **`(C)` UNA GEOMETRIA DINAMICA** *(gli archi che si allungano secondo la materia; la mitosi; `D9`)*: ### **le lunghezze `l_a` diventano VARIABILI con una loro legge** *(una sorgente dalla densita', come `d''` dell'era `1`, ma reversibile)*: ### **la strada lunga, emergente;** ### **`gamma` non si prevede: si MISURA;** ### **vuole il canale di `cs`** *(il passo `4` del piano)* ### **e una decisione su `A16`** *(un'inerzia nuova)*.

| | `gamma` previsto | il rapporto delle due `c` *(l'obiezione)* | l'universalita' materia/luce | Gauss, gauge | reversibile | `A1` | a `cs = cs_rif` uniforme |
|---|---|---|---|---|---|---|---|
| `(A1)` | `1` | ### **`pi x(r)/r`: da MISURARE** | ### **se `x(r) = r/4`** | ### **esatti** *(la sorgente e' la norma che passa; la spinta e' `rot^T` di una grandezza per placchetta)* | si' *(flussi esatti, leapfrog)* | ### **un riferimento `s_rif`** *(la scelta `2` sotto)* | ### **il passo di oggi AL BIT** *(`s/s_rif = 1.0` esatto; Erone normalizzato)* |
| `(A2)` | `1` | ### **`pi/4` per costruzione** | si', ma ### **la caduta raddoppia** | esatti | si' | come `(A1)` | al bit |
| `(B)` | `1` per la luce, `0` per la materia | ### **`~ 1/r`** | ### **NO** | esatti | si' | come `(A1)` | al bit |
| `(C)` | da misurare | da misurare | da misurare | da progettare | ### **da progettare** *(l'era `1` era smorzata)* | ### **la legge della lunghezza** | se la sorgente e' nulla |

### **`[RACCOMANDAZIONE]` `(A1)` per il prototipo, `(B)` come controllo che DEVE FALLIRE l'universalita', `(A2)` come confronto; `(C)` dopo il canale di `cs`.**

## 4. LE MISURE DEL PROTOTIPO SUI TRIANGOLI *(in memoria; in ordine; i criteri fissati QUI)*

| | la misura | DEVE | DEVE FALLIRE *(la chiave giusta)* | PUO' FALLIRE |
|---|---|---|---|---|
| `(0)` | ### **`x(r)` dal generatore `H_r`** *(nessuna corsa)*, `r` in `(0.8, 0.9, 1, 1.1, 1.25)`; ### **la massa** *(il salto a `K`)* ### **contro `r`** | `x(1) = 1/4` entro `1e-9` | -- | ### **`x(r)/r` costante entro `1e-3`** *(la previsione del guardiano)* |
| `(a)` | `cs = cs_rif` ovunque | ### **il passo di oggi AL BIT** *(ogni attributo; il campo e la materia)* | ### **`cs` uniforme `!= cs_rif`: NON e' il passo di oggi, ED e' il passo con l'angolo dello spostamento `pi s r`** *(entro `1e-12`)* | -- |
| `(b)` | Gauss, gauge *(contro la stima, `doc/PATTERN_DI_PROVA.md`)*, reversibilita', energia, in un gradiente | entro `1e-12` *(Gauss, `T`)*; `|dE| <=` stima; nessuna deriva | togliere la sorgente: Gauss si rompe *(la chiave: `G - G0 = -e(rho - rho0)`)* | -- |
| `(c)` | ### **la luce in un gradiente** *(la scena di `64bb2328`, F1 coi pesi nuovi)*: la velocita' coordinata contro `cs^2/cs_rif`; ### **la deflessione contro `R2`** *(il fascio largo e l'estrapolazione di `fa7ee993`)*; il ritardo di Shapiro | -- | ### **la deflessione entro il `10%` da `R1`** *(deve venire `~2`)* | ### **`v/(cs^2/cs_rif)` costante entro il `2%`; la deflessione entro il `10%` da `R2`; il ritardo entro il `2%` da `int du/(cs^2/cs_rif)`** |
| `(d)` | ### **la caduta della particella lenta** *(il pacchetto di banda, il differenziale: le corse di `7daa8840`)* | -- | ### **`(A2)`: la caduta doppia** *(`dif/a_H` contro quello di oggi: `~2`)* | ### **`(A1)`: `dif/a_H` uguale a quello di oggi entro il `2%`** |
| `(e)` | ### **LA PROVA DELL'OBIEZIONE DI LUCA:** il rapporto `v_b/c` in una regione uniforme a `r` in `(0.9, 1, 1.1)` e nel gradiente, ### **con la previsione del guardiano accanto** *(`pi/4` costante)* | a `r = 1`: `pi/4` *(`64bb2328`)* entro `1e-6` | ### **`(B)`: il rapporto varia come `1/r`** *(entro `1e-3`)* | ### **`(A1)`: `pi/4` entro `1e-3` a ogni `r`** |
| `(f)` | l'universalita' fra le bande e fra `eps 0` e `0.5` | -- | -- | ### **la caduta dei due rami uguale entro il `2%`; `eps 0.5` contro `eps 0` entro il `2%`** |

### **NOTE SUL METODO:** ### **`(A1)` si fa in memoria avvolgendo `flussi_parziali.z_arco`** *(come le convenzioni dello zero)* ### **e sostituendo i pesi di `Campo`** *(una sottoclasse, come `CampoF2` di `csv/_u1_secondo.py`)*; ### ⚠ **LE TRE TRAPPOLE di `fa7ee993`** *(`pi` scritto a mano in `_triangoli_forza.modo`, in `_triangoli_bassa_energia.main`, in `_triangoli_forza.coppia_K`)* ### **valgono anche qui:** ### **lo scarto fra i due zeri e i livelli esclusi si MISURANO.**

## 5. LE SCELTE DI LUCA

| la scelta | le alternative | `[RACCOMANDAZIONE]` |
|---|---|---|
| `1` la strada | `(A1)` / `(A2)` / `(B)` / `(C)` | ### **`(A1)` per il prototipo; `(B)` e `(A2)` come controlli; `(C)` dopo il canale di `cs`** |
| `2` il riferimento `s_rif` | ### **`(i)` il `cs` del vuoto imperturbato** *(come `Phi = 0` all'infinito; nelle scene dei triangoli col `cs` a mano, il valore uniforme della scena)*; ### **`(ii)` `dtau_rif = 1`** *(`B-5`: le lunghezze `1` all'orologio piu' veloce; NESSUN numero nuovo, ma a `s` uniforme `< 1` il passo cambia: tutti i risultati di oggi sui triangoli, a `s 0.05`-`0.3`, sarebbero in un potenziale profondo)* | ### **`(i)`**, ### **perche' tiene `(a)`: i risultati di oggi restano quelli del vuoto di riferimento** |
| `3` l'area della placchetta | ### **Erone dalle tre lunghezze degli archi** / la media dei tre nodi *(la regola di prova di `F2`)* | ### **Erone: nessuna regola nuova** |
| `4` i versori della moneta | fissi *(il triangolo equilatero)* / dalla metrica *(gli angoli dei triangoli con le lunghezze `l_a`)* | ### **FISSI, prima** *(un interruttore alla volta)* |
| `5` quali pezzi | `(A1)` l'arco / `(A2)` tutti | ### **decide la misura `(0)` e `(d)`** |
| `6` sulla FCC | in 3D anche la stella dei `1`-forme scala *(`l*/l ~ cs`)* | ### **da rifare sulla carta prima della FCC** |

## 6. IL COSTO E L'ORDINE *(un mandato alla volta)*

1. ### **IL PROTOTIPO, parte `1`:** ### **`(0)`** *(il generatore `H_r`: minuti)*, ### **`(a)`, `(b)`** *(come `0b6bfde8`: `~5` minuti)*; ### **SE `(0)` dice che `x(r)/r` NON e' costante, lo si riporta PRIMA di andare oltre** *(e' la risposta sulla carta all'obiezione di Luca)*.
2. ### **IL PROTOTIPO, parte `2`:** ### **`(c)`** *(la scena di `64bb2328`, la scansione dei fasci di `fa7ee993`: `~3` minuti)*, ### **`(d)`, `(f)`** *(le corse di `7daa8840`: `~2` minuti a variante)*, ### **`(e)`** *(gli spettri: `~3` minuti)*; ### **le varianti `(A1)`, `(A2)`, `(B)`.**
3. ### **LA DECISIONE DI LUCA sugli orologi** *(il passo `3` del piano)*.
4. ### **IL CANALE DI `cs`, poi `(C)`** *(se serve)*.

### ⚠ **E PRIMA DEL NUCLEO** *(`doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`)*: ### **una legge che porti `cs` nelle lunghezze vuole la sua decisione presa** *(un nodo dell'albero)*: ### **il prototipo resta IN MEMORIA finche' Luca non decide.**

## 7. I CONTRASTI CON IL REPO *(riportati, NON corretti)*

1. ### **Il mandato dice «la deflessione, estrapolata a fascio largo, e' `0.957` di quella di Soldner»:** ### **in `fa7ee993` l'estrapolazione fissata** *(contro `X`, grado `1`)* ### **da' `0.9569` e FALLISCE il suo criterio** *(il `2%`)*; ### **il referto dice che `X` non e' monotono in `W` e che un `6%` resta NON attribuito** *(`a/(a_E <cos^2>) = 0.940` a `W 24`)*: ### **la conclusione «`gamma = 0`» regge** *(e' lontana da `R2` in ogni caso: `0.42`-`0.44`)*, ### **il `0.957` come numero no.**
2. ### **«il capitolo "la metrica viva"»: non trovato** *(sezione `2.1`)*.
3. ### **Il criterio `(a)` del mandato** *(«a `cs` uniforme il passo identico a quello di oggi al bit»)* ### **vale per la strada `(A)` SOLO a `cs = cs_rif`:** ### **a `cs` uniforme diverso dal riferimento il passo CAMBIA, ed e' giusto** *(un potenziale uniforme cambia le velocita' coordinate)*; ### **il progetto lo scrive come DEVE + DEVE FALLIRE** *(sezione `4`, riga `(a)`)*.
4. ### **La previsione del guardiano** *(«il rapporto resta `pi/4`, perche' materia e luce corrono sugli stessi archi»)*: ### **sulla carta e' vera per `(A2)` per costruzione, e per `(A1)` solo se `x(r) = r/4`** *(la misura `(0)`)*: ### **non e' garantita dal fatto che corrano sugli stessi archi, perche' la materia sente ANCHE il nodo.**
