# IL PROTOTIPO DEL CAMPO U(1) SUI TRIANGOLI, IN MEMORIA: LA CATENA DEI SIGILLI E LA VELOCITA' DELLA LUCE

> **Il mandato:** di Luca, «il prototipo del campo `U(1)` sui triangoli, in memoria» *([[PROGETTO-U1]], `doc/PROGETTO_U1.md`; [[LUCE-VINCOLO-LAMPI-GAMMA]], [[LORENTZ-MATERIA-INTERFERENZA]], [[DECISIONE-SOLO-TRIANGOLI]])*.
> ### **NESSUN CAMBIAMENTO DEL NUCLEO, NESSUNA DECISIONE DI LUCA PRESA.** ### **Lo script sara' `csv/_u1_prototipo.py`, il referto `doc/referti_l2/u1_prototipo.{txt,jsonl}`.**

### ⚠ **LA LEZIONE DI `4bc491e4`:** ### **questo task history entra DA SOLO, e prima di scrivere lo script controllo la lista dei file del suo commit leggendo TUTTA l'uscita.**

**LIVELLO:** un prototipo in memoria *(il campo fuori da `stato.py`, il passo di oggi AVVOLTO e non modificato)*.

## 0. LA STELLA POLARE

1. **`A14`:** ### **la carica si conserva LOCALMENTE per costruzione** *(la norma passa fra due nodi SOLO nello spostamento, e lo stesso pezzo aggiorna `E` dello stesso `J`: la legge di Gauss e' il sigillo `(c)`)*; ### **l'energia di materia piu' campo si MISURA** *(il sigillo `(e)`)*: ### **la conservazione dell'energia e' al secondo ordine, non esatta** *(una composizione di flussi esatti che non commutano, come `H_tot` oggi)*.
2. **Il gradino:** ### **`(a)` robusto al rumore numerico** *(i sigilli `(a)`-`(e)` sono identita' entro l'arrotondamento)*; ### **`(c)` un limite noto** *(la velocita' `c = 1` per tempo proprio contro il conto sulla carta di `doc/PROGETTO_U1.md`)*.
3. **Aggiunge un numero o una legge?** ### **Un campo con gradi di liberta' propri** *(due pezzi del passo: la spinta magnetica e la deriva elettrica, piu' la sorgente dentro lo spostamento)* ### **e UNA COSTANTE DI ACCOPPIAMENTO `e`** *(di tipo «costante di accoppiamento», legittima e da dichiarare; qui DUE VALORI DI PROVA dichiarati come tali, sezione `2.3`)*. ### **Nessuna toppa, nessun clip.** ### **I pesi** *(`l = 1`, `A_p = sqrt3/4`, `l* = 1/sqrt3`)* ### **sono la geometria del triangolo, non numeri scelti.**
4. **Tocca `rho`, `c_s` o il segno?** ### **Usa `c_s`:** ### **il tempo del campo e' il `dtau` dell'arco** *(`B-3`)*, ### **quindi la luce rallenta dove `cs` e' basso** *(il sigillo `(g)`: il verso curvatura -> EM)*. ### **Il verso EM -> curvatura NON c'e'** *(il campo non entra in `cs`)*: ### **dichiarato.**
5. **Emergente o imposto?** ### **La velocita' della luce NON si impone:** ### **esce dai pesi del calcolo esterno discreto e dal passo** *(la si MISURA dal passo del codice, non dalla formula)*; ### **il ritardo di Shapiro esce dal tempo dell'arco, che nessun pezzo del campo sa essere un «potenziale».**

## 1. IL RAGIONAMENTO PRELIMINARE *(che cosa credo, prima di guardare un numero)*

### 1.1 Dal codice *(letto, non dai commenti)*

- ### **Il passo** *(`tick.percorri_tick`)* ### **percorre `composizione.ORDINE`: `14` pezzi, palindromo, tutti a frazione `0.5`;** ### **lo spostamento della materia** *(`CAMM-SPOSTAMENTO`, `motore._spostamento_trasporto` -> `flussi_parziali.hop_psi`)* ### **e' alle posizioni `4` e `9`, i due `CAMM-SPOSTAMENTO-VUOTO` al centro** *(`6` e `7`)*.
- ### **`hop_psi`: lato `0` nuovo `alpha v0 + beta U^dagger v1`, lato `1` nuovo `alpha v1 + beta U v0`** *(`alpha = (1+z)/2`, `beta = (1-z)/2`, `z = e^{i theta}`, `theta = pi s_arco f`)*. ### **Il motore legge `FP.hop_psi` dal modulo A OGNI CHIAMATA** *(e' cosi' che `_zero_simmetrico.convenzione_simmetrica` la avvolge)*, ### **e `mot.operatori` si legge a ogni pezzo** *(`percorri_tick`)*: ### **il passo si avvolge in memoria senza toccare un file.**
- ### **`Geometria` asserisce solo che `U` sia unitaria** *(`motore.py`, la classe `Geometria`)*: ### **`U = e^{i e A} I_2` e' unitaria, e a `A = 0` e' `I` AL BIT** *(`exp(0j) = 1 + 0j` esatto)*.
- ### **La scena degli strumenti dei triangoli** *(`_triangoli.scena_toro` a `dtau 1.0`, `mot.cs = s`, `mot.lambda_c = None`, il vuoto `phi = 0`, la materia un pacchetto)* ### **e la camminata `_triangoli.camminata`** *(l'ordine intero SENZA `CAMM-MATERIA-VUOTO`: «la camminata sola», come in tutti gli strumenti dei triangoli)*: ### **qui la stessa, dichiarata.** ### **`CAMM-FASE-VUOTO` con `lambda_c = None` non fa niente** *(`energia_pesata.applica`, il primo ramo)*.

### 1.2 Le grandezze *(dalla carta, `doc/PROGETTO_U1.md` sezioni `4`-`6`)*

- ### **`A_a` reale sull'arco, `E_a` il coniugato; `U_a = e^{i e A_a} I_2`.** ### **Le placchette per nodo `v`:** ### **«su» `B = A(v,0) + A(v+a1,1) - A(v,2)`, «giu'» `B = A(v,2) - A(v+a2,0) - A(v,1)`** *(antiorarie, con gli archi `0`, `1`, `2` lungo `a1`, `a2`, `a1+a2`)*: ### **ogni arco sta in DUE placchette.**
- ### **L'energia del campo per tick:** ### **`H_F = somma_a s_a^2 (l/l*) E_a^2/2 + V(A)`**, con ### **`V = somma_p (1 - cos(e B_p))/(e^2 A_p)` compatto, `somma_p B_p^2/(2 A_p)` non compatto.**
- ### **Il passo del campo, il leapfrog:** ### **la spinta `E <- E - f dV/dA`** *(il rotore trasposto di `sin(e B)/(e A_p)` o `B/A_p`)* ### **e la deriva `A <- A + f s_a^2 (l/l*) E`.**

### 1.3 Le DUE PREMESSE DEL PROGETTO CHE CADONO *(dalla carta, prima dei numeri)*

- ### ⛔ **`(a)` «`A = 0`, `E = 0`, accoppiamento acceso: il passo uguale a quello di oggi AL BIT» NON E' VERO con `e != 0` e la materia che si muove:** ### **il primo spostamento porta la corrente `J`, la sorgente fa `E = -e J`, la deriva al centro fa `A != 0`, e il SECONDO spostamento vede `U != I`.** ### **Vale fino alla deriva** *(la prima meta' del tick)*, ### **e dopo lo scarto e' di ordine `e^2`** *(`e A ~ e^2 J`)*. ### **Quindi il sigillo diventa due:** ### **`(a1)` con `e = 0` e il campo acceso** *(tutta la macchina del campo presente, `A`, `E` nulli)*: ### **la materia e OGNI ATTRIBUTO uguali AL BIT per `50` tick**; ### **`(a2)` con `e` dei due valori: la prima meta' del tick uguale AL BIT, e lo scarto dopo un tick `~ e^2`** *(la lettura: il rapporto fra i due scarti contro `(e_2/e_1)^2`)*.
- ### ⛔ **«il tempo del campo e' il `dtau` dell'arco» preso alla lettera** *(spinta E deriva per `s_a`)* ### **ROMPE GAUSS dove `cs` varia:** ### **`div(s_a (rot^T g)) != 0`.** ### **La forma che tiene Gauss esatto, il passo simplettico e la luce locale `c = 1` per tempo proprio dell'arco:** ### **la spinta SENZA `s`, la deriva con `s_a^2`** *(cioe' `H_F` qui sopra: in `(A, E)` canonica; a `s` uniforme e' la lettura alla lettera con `E -> s E`, la STESSA dispersione)*. ### ⚠ **NON E' L'UNICA:** ### **la forma «adattata in impedenza»** *(spinta con `s_p` della placchetta, deriva con `s_a`: `epsilon = mu = 1/s`, come la luce nella metrica isotropa)* ### **tiene anche lei Gauss, ma vuole una REGOLA per `s_p`** *(`B-3` e' per due nodi, la placchetta ne ha tre)*. ### **Scelgo la prima perche' non aggiunge una regola** *(`CLAUDE.md` par.`9-ter`)*, ### **e la scelta fra le due VA A LUCA** *(conta solo in `(g)`, dove `cs` varia: a `s` uniforme coincidono)*.

### 1.4 Le PREVISIONI *(sulla carta)*

- ### **`(f)` LA LUCE:** ### **il leapfrog da' `cos(omega_tick) = 1 - s^2 lambda/2`, `lambda` gli autovalori di `M = (l/l*) C^dagger diag(1/A_p) C`** *(`4` volte `C^dagger C`)*; ### **a `k` piccolo `omega_tick = s k (1 + O(k^2) + O(s^2 k^2))`: `c = 1` arco per unita' di tempo proprio, ISOTROPA** *(la `C6` del reticolo)*; ### **a `Gamma` la banda ottica `sqrt 24 = 4.899`, a `K` e a `M` i valori di `M`** *(calcolati dallo script dalla carta e confrontati col passo)*. ### **La banda di gauge: `lambda = 1` doppio** *(`A = d chi` fermo, ed `E = d chi` con `A` che cresce linearmente: un BLOCCO DI JORDAN, che Gauss vieta)*.
- ### **IL LIMITE DI COURANT:** ### **`s sqrt 24 <= 2`, cioe' `s <= 0.40825`:** ### **`s 0.3` stabile, `s 0.45` instabile** *(`cos omega = 1 - 0.45^2 12 = -1.43`, `|lambda| = 2.45` per tick sulla banda ottica a `Gamma`)*.
- ### **COMPATTO CONTRO NON COMPATTO:** ### **linearizzati sono IDENTICI** *(`sin(eB)/e = B + O(e^2 B^3)`)*; ### **la differenza e' all'ampiezza finita, `~ (e B)^2/8` sulla velocita'.** ### ⚠ **IL CONFINAMENTO DI POLYAKOV E' QUANTISTICO** *(gli istantoni-monopoli: un'ampiezza di tunnel)*: ### **un campo CLASSICO compatto in `2+1` NON lo mostra** *(il fotone classico resta senza massa)*. ### **Quindi la previsione per «la stessa cosa nel compatto» e': PASSA, e cio' NON dice niente su Polyakov** *(dichiarato prima)*.
- ### **`(g)` SHAPIRO:** ### **la velocita' locale `v/s_locale` costante entro l'`1%`** *(la dispersione spaziale a `k` fino a `0.5` e quella temporale a `s k/2` fino a `0.08`)*; ### **la deflessione verso `cs` piu' basso** *(l'ottica dei raggi: `d^2 u/dt^2 = -s ds/du`)*.
- ### **I TRE NUMERI:** ### **`c/s = 1`, `v_b/s = 0.785`, `v_max/s = 0.60`:** ### **la luce del campo sara' PIU' VELOCE del cono della materia** *(`v_max`)*: ### **se cosi', la materia vive dentro un cono piu' stretto di quello della luce, e la relativita' ristretta del modello ha DUE coni** *(il guardiano lo segnava gia' in [[LORENTZ-MATERIA-INTERFERENZA]])*.

### 1.5 NON SO

- ### **se la reversibilita' col rovesciamento del tempo regge AL `1e-12`** *(sezione `2.4`: dipende da `n_z = 0` dei versori dei triangoli)*;
- ### **se l'energia di materia piu' campo non deriva** *(la materia gira a passi FINITI, `theta = pi s/2` per pezzo: un riscaldamento di Floquet del campo e' possibile)*;
- ### **se `e` derivato** *(la sezione `7` del progetto: «il vuoto come scala»)* ### **si estende allo spostamento parziale:** ### **sulla carta NON ancora** *(la derivazione del `2026-10-12` e' per lo spostamento intero, `theta = pi`, e la scena dei triangoli ha il vuoto NULLO, dove `sigma -> 0` e l'inerzia diverge: dichiarato la')*. ### **QUINDI IL VALORE DERIVATO SI SALTA, e lo si dice nel referto.**

## 2. LA PROGETTAZIONE *(le letture si fissano QUI)*

### 2.1 La griglia e i parametri, dichiarati in ogni riga

- ### **gli zeri:** `simm` *(`_zero_simmetrico.convenzione_simmetrica`)* e `oggi`; ### **`s` in `(0.05, 0.1, 0.3)`**, ### **la prova dichiarata a `s 0.45`** *(solo per Courant)*; ### **compatto e non compatto**; ### **la carica e' la norma** *(`DEC-QC`)*; ### **il tempo del campo: l'arco** *(`B-3`, nella forma della sezione `1.3`)*; ### **la moneta `eps = 0.5`** *(`_triangoli.EPS_MONETA`)*.
- ### **la scena della materia:** ### **il toro dei triangoli `24 x 24`, il pacchetto gaussiano `W = 3` celle sul primo vettore della coppia a `K`** *(`_triangoli_forza.coppia_K(0.5, s)`, la fase `e^{i K.r}`)*, ### **il vuoto nullo** *(come gli strumenti dei triangoli)*.

### 2.2 Il passo del campo, AVVOLTO

### **`spinta(1/2)` -> la camminata con `mot.operatori` avvolti** *(lo spostamento della materia: `J_a = |v0'|^2 - |v0|^2`, poi `E_a <- E_a - e J_a`; dopo il PRIMO `CAMM-SPOSTAMENTO-VUOTO` del tick: `deriva(1/2)`, `deriva(1/2)`, e `U` rifatta da `A`)* ### **-> `spinta(1/2)`.** ### **Palindromo.**
### **IL SEGNO della sorgente, sulla carta:** ### **lo spostamento e' il flusso esatto di `h = c <P_-(eA)>`; `dE/dt = -dh/dA = c e Im(v0^dagger U^dagger v1)`, e `d|v0|^2/dt = -c Im(...)`:** ### **`Delta E = -e J` ESATTO, qualunque `c`.** ### **La legge di Gauss:** ### **`D_i = somma_{a entra in i} E_a - somma_{a esce da i} E_a = e (rho_i - rho_media)`** *(sul toro la carica totale va neutralizzata da un fondo uniforme)*; ### **`E(0)` la soluzione di norma minima** *(`lstsq` sulla matrice d'incidenza)*.

### 2.3 La costante `e`: due valori di prova, dichiarati

### **`e = 0.1` e `e = sqrt(4 pi/137) = 0.3028`** *(il secondo e' il valore di `alpha = 1/137` nelle unita' naturali: UN RIFERIMENTO DICHIARATO, non una taratura)*. ### **Il perche': l'accoppiamento debole** *(`e^2 << 1`: il compatto e il non compatto coincidono a meno di `(eB)^2`)*, ### **e due valori per leggere la dipendenza da `e`** *(`(a2)`)*. ### **Il valore derivato: saltato** *(sezione `1.5`)*.

### 2.4 I sigilli, e come si misurano

| | la misura | il criterio, fissato QUI |
|---|---|---|
| `(a1)` | `e = 0`, `A = E = 0`, il campo acceso, `50` tick, per zero | **DEVE: la materia e OGNI attributo di `st` e di `mot` uguali AL BIT** *(`_triangoli_forza.byte_attr`; `mot.operatori` rimesso prima del confronto)* |
| `(a2)` | `e` dei due valori, un tick | **DEVE: la prima meta' del tick AL BIT**; lettura: lo scarto dopo un tick e il rapporto contro `(e_2/e_1)^2` |
| `(b)` | una `chi` casuale per nodo in `[-pi, pi)` *(seme dichiarato)*, `psi -> e^{i chi} psi` su ogni estremita' del nodo, `A <- A + (chi_jj - chi_ii)/e`; `100` tick | **DEVE: `rho` per nodo, `E`, `e B_p` uguali entro `1e-12` relativo** |
| `(b-)` | trasformare solo `psi` | **DEVE FALLIRE** *(lo scarto `>> 1e-12`)* |
| `(c)` | `max_i |D_i - e(rho_i - rho_media)|` a OGNI tick, `1000` tick | **DEVE: entro `1e-12` relativo** a `e max(rho(0))` |
| `(c-)` | la sorgente tolta, la materia presente | **DEVE FALLIRE, PER LA CHIAVE GIUSTA:** lo scarto `> 1e-9`, **e** `G(t) - G(0) = -e (rho(t) - rho(0))` entro `1e-12` *(la carica si e' mossa senza il campo)* |
| `(d)` | `500` tick avanti, il rovesciamento `T`, `500` avanti, `T` | **DEVE: `psi`, `phi`, `A`, `E` di partenza entro `1e-12` relativo** |
| `(e)` | `E_tot` a ogni tick, `1000` tick | **DEVE: nessuna deriva:** **`|pendenza| 1000 <= ampiezza/2`** *(la pendenza del fit lineare, l'ampiezza = massimo meno minimo dei residui)* |
| `(f)` | la dispersione, la velocita' di gruppo, Courant | sotto |
| `(g)` | Shapiro | sotto |

- ### **IL ROVESCIAMENTO `T`** *(sulla carta)*: ### **`psi -> sigma_x psi^*` per estremita', `phi -> phi^*`, `A -> -A`, `E -> E`.** ### **Il Grover e lo spostamento del vuoto sono reali, quindi `K G K = G^{-1}`; lo spostamento con `U = e^{ieA}` va in `hop(theta, -A)^{-1}`; la moneta `exp(-i a sigma.n)` va nella sua inversa con `sigma_x K` PERCHE' `n_z = 0`** *(i versori dei triangoli sono nel piano)*; ### **la spinta e' dispari in `A`, la deriva lineare; la sorgente `-e J` cambia segno perche' `J` e' la differenza prima/dopo.** ### **E l'ordine e' palindromo:** `T U T^{-1} = U^{-1}`.
- ### **LE SOGLIE, dall'arrotondamento atteso:** ### **un tick fa `~14` pezzi da `~10` operazioni, `~1.1e-16` l'una:** ### **in `1000` tick, `~4e-14` a passeggiata casuale e `~1.5e-11` nel caso peggiore lineare.** ### **`1e-12` (la soglia del mandato) e' `25` volte sopra la stima tipica:** ### **se una DEVE fallisse fra le due stime, il referto lo dice come tale e mi fermo.** ### **Per `e B_p`** *(con `chi` fino a `pi`, `A` fino a `pi/e`)* ### **la scala e' l'angolo, `2 pi`:** ### **lo scarto atteso `~3 pi eps = 2e-15`.** ### **Il relativo: `max|x - x'|/max|x|` per osservabile; per `A` in `(d)` il massimo lungo la corsa** *(`A(0) = 0`)*.
- ### **L'ENERGIA `E_tot`, la definizione:** ### **la somma dei generatori dei pezzi, per tick:** ### **`-pi somma_k s_k <I - P_u>_k`** *(Grover, materia e vuoto)* ### **`-pi somma_a s_a <P_-(eA)>_a`** *(spostamento, il vuoto senza `U`)* ### **`+ somma_h a_h <sigma.n>_h`** *(la moneta, `a_h = eps dtau_nodo`)* ### **`+ H_F`.** ### **Con lo zero simmetrico il generatore del Grover e dello spostamento ha `- P + I/2` invece di `-(I - P)`: una costante per la norma, che si conserva** *(lo script usa il generatore della convenzione che gira)*.

### 2.5 `(f)` e `(g)`: come si misurano

- ### **IL PASSO DEL CAMPO SOLO** *(senza materia)*: ### **la mappa del tick su un toro `8 x 8`, applicata ai `384` vettori di base; i blocchi in spazio reale** *(come `_triangoli_forza.blocchi`)*; ### **il blocco `6 x 6` a un `k` qualunque.** ### **Controllo di servizio: gli autovalori dai blocchi sulla griglia `8 x 8` contro quelli della matrice intera** *(entro `1e-12`)*, ### **e contro la carta `cos omega = 1 - s^2 lambda/2`** *(entro `1e-12`)*.
- ### **A `Gamma`, `K`, `M`: le `6` fasi;** ### **la velocita' di gruppo a `|k| = 1e-3`** *(differenza centrata, `12` direzioni da `0` a `165` gradi)*, ### **per unita' di tempo proprio** *(`/s`)*; ### **l'isotropia** *(massimo meno minimo sulle direzioni, la lettura contro `1e-3` del progetto)*.
- ### **COURANT:** ### **`max |lambda|` sulla griglia `48 x 48` di `k`, togliendo gli autovalori con `|lambda - 1| < 1e-6`** *(il blocco di Jordan della gauge: numericamente si apre a `~sqrt(eps)`)*; ### **instabile se `> 1 + 1e-6`.** ### **DEVE FALLIRE PER LA CHIAVE GIUSTA a `s 0.45`:** ### **il `k` piu' instabile e' `Gamma`, sulla banda piu' alta.** ### **E a `s 0.3` stabile.** ### **`s` critico per bisezione** *(la lettura contro `0.40825`)*.
- ### **IL PACCHETTO DEL CAMPO** *(per il compatto e per ogni `e`)*: ### **toro `96 x 96`, il fotone a `k0 = 2 pi 4/96` lungo `a1`, largo `W = 12`, reale** *(il modo piu' il coniugato)*, ### **l'ampiezza con `max |B| = 1`** *(l'unita' del campo, dichiarata)*; ### **il baricentro dell'energia per `30` archi; la velocita' contro `v_g(k0)` del blocco** *(non compatto: il controllo di servizio entro l'`1%`)* ### **e il compatto contro il non compatto.**
- ### **I PUO' FALLIRE del mandato:** ### **`|v_g/s - 1| <= 0.01` a `k 1e-3`, non compatto, `s 0.05`** *(dal blocco)*; ### **lo stesso nel compatto** *(dal pacchetto: `|v_compatto/v_noncompatto - 1|` sommato allo scarto del non compatto)*.
- ### **`(g)` SHAPIRO:** ### **toro `192 x 48` *(lati diversi)*, `cs = s0 (1 + eta cos(2 pi m1/L1))` con `s0 = 0.2`, `eta = 0.5`** *(`cs` fra `0.1` e `0.3`: dentro Courant)*; ### **il pacchetto a `k0 = 2 pi/24`, lungo la normale al gradiente** *(`30` gradi sul toro `A`)*, ### **`800` tick:** ### **la velocita' del baricentro** *(la differenza centrata su `+-10` tick)* ### **contro `cs` mediato sull'energia: PUO' FALLIRE `v/cs` costante entro il `2%`.** ### **La deflessione:** ### **un pacchetto lungo le strisce** *(lungo `a2`)* ### **nel punto di gradiente massimo, `400` tick: l'accelerazione trasversa dal fit contro `-s ds/du`** *(una lettura)*.

### 2.6 Mi FERMO se

### **una DEVE fallisce** *(committo lo stato e il fallimento, e mi fermo)*; ### **una DEVE FALLIRE passa** *(il controllo negativo non sa distinguere)*; ### **un controllo di servizio fallisce** *(lo strumento e' rotto)*.

### 2.7 Le domande sugli assiomi, NON risolte qui *(il mandato)*

### **la carica: la norma** *(`DEC-QC`)* ### **contro la carica di rotazione di `A14.3`;** ### **`A16` «niente inerzie aggiunte» contro l'energia `E^2/2`** *(la lettura del guardiano: `E` un grado di liberta', una «memoria» permessa da `A16(3)`)*.

## 3. TODO DEL NEXT STEP

1. questo task history, da solo, e il controllo della lista dei file del commit leggendo tutta l'uscita;
2. `csv/_u1_prototipo.py` e la sua voce in `doc/INVENTARIO_strumenti.md`, committati PRIMA dei numeri;
3. la corsa, `doc/referti_l2/u1_prototipo.{txt,jsonl}`;
4. il referto con la relazione e i legami nell'indice *(`PROGETTO-U1`, `LUCE-VINCOLO-LAMPI-GAMMA`, `LORENTZ-MATERIA-INTERFERENZA`)*; ### **se una DEVE fallisce, FERMO.**
