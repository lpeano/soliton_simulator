# LA MASSA NEI DIFETTI *(la parte C1 del mandato delle 20:44)*: IL GENERATORE SU UN TORO A TRIANGOLI CON UNO SDOPPIAMENTO D'ARCO

> **Il mandato:** di Luca, `2026-10-25`, `20:44`, la parte `C1` *([[PROGETTO-MITOSI]], la sezione `4`, la prima misura sulla carta)*.
> ### **Sulla carta: il generatore, nessuna dinamica; nessun file del nucleo; nessuna regola di mitosi.** ### **Lo script `csv/_massa_nei_difetti.py`, il referto `doc/referti_l2/massa_nei_difetti.{txt,jsonl}`.**

**LIVELLO:** una misura sul generatore.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia; la mossa e' solo nel grafo della misura)*. 2. **Il gradino:** ### **lo spettro locale del generatore attorno a un difetto.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **Misura come il grado cambia la massa locale, e conta `Lambda_k` per `cs`.** 5. **Emergente o imposto?** ### **Il difetto e' imposto; la massa che ne viene e' cio' che si misura.**

## 1. LA SCENA *(fissata qui)*

- ### **IL TORO PERFETTO:** ### **`csv/_triangoli`/`scena_l2.GRIGLIE["triangoli"]`, `corrente.toro_spostamenti((L, L), ((1,0), (0,1), (1,1)))`** *(il nodo `v = c0 L + c1`, l'arco `3 v + a` dal nodo `v` a `v + spostamento_a`; le estremita' `2k` sul lato `ii`, `2k+1` sul lato `jj`)*.
- ### **LO SDOPPIAMENTO `(b1)`:** ### **`i = (L/2, L/2)`, `j = i + (1,0)`** *(l'arco `3 i + 0` TOLTO)*; ### **i vertici opposti `k = i + (1,1)`, `l = i + (0,-1)`** *(i triangoli `ijk` e `ijl`)*; ### **il nodo nuovo `n = L^2`, con quattro archi nuovi `n-i`, `n-j`, `n-k`, `n-l`** *(`n` sul lato `ii`)*. ### **I gradi attesi: `n` `4`, `k` e `l` `7`, `i` e `j` `6`, tutti gli altri `6`** *(si verifica)*.
- ### **IL GENERATORE:** ### **`H = (I - P_u) + P_-` sulle `2m` estremita':** ### **`P_u` nodo per nodo, il vettore uniforme sulle sue `d` estremita'** *(`1/d`)*; ### **`P_-` arco per arco, `(e_2k - e_2k+1)/sqrt(2)`**. ### **Nessuna fase di Bloch, diagonalizzazione diretta** *(`numpy.linalg.eigh`, reale simmetrica a `eps 0`)*; ### **lo zero simmetrico: `mu = 1 - lambda`.**
- ### **LA MONETA** *(il caso secondo, `eps 0.5`)*: ### **`H x I_2 - (eps/pi) somma_h sigma.n_h`** *(la forma di `_curvatura_parte2.H_moneta` a `alpha = beta = gamma = 1`)*. ### **I VERSORI, DICHIARATI PRIMA:** ### **le posizioni `p = c0 a1 + c1 a2`** *(`a1 = e(0 gradi)`, `a2 = e(120 gradi)`, le direzioni di `GRIGLIE`)*; ### **il nodo nuovo al PUNTO MEDIO `m = p_i + a1/2`;** ### **il versore di un'estremita' = la direzione dal suo nodo verso il vicino** *(`unit(p_vicino - p_nodo)`, con `m` per `n`)*: ### **per gli archi del toro e' `+-e_a` come oggi; per `n` vengono `-a1`, `+a1`, `(0,1)`, `(0,-1)`** *(sulla carta: `p_k - m = (0, sqrt(3)/2)`)*.

## 2. LE MISURE E I CRITERI *(fissati qui, prima dei numeri)*

- ### **`L = 24, 36, 48`** *(multipli di `3`: il punto `K` e' nel reticolo di Bloch)* ### **a `eps 0`;** ### **`eps 0.5` a `L = 24, 36`** *(la matrice complessa a `L 48` e' di `27648 x 27648`: `12` GB solo la matrice, non entra con gli autovettori; DICHIARATO)*.
- ### **IL PESO SU UN NODO** di uno stato: `somma_{h in v} |psi_h|^2`. ### **La distanza:** ### **la distanza di grafo da `n`** *(BFS)*.
- ### **`(i)` GLI STATI NELLA BANDA PROIBITA:** ### **il bordo `E0` = il minimo di `|mu|` sul toro perfetto alla stessa `L` e allo stesso `eps`;** ### **uno stato e' NELLA BANDA se `|mu| < E0 - 1e-8`;** ### **e' LOCALIZZATO SUL DIFETTO se il peso entro distanza `3` da `n` e' `>= 0.5` E `IPR 2m >= 50`** *(`IPR = somma_h |psi_h|^4`; uno stato esteso ha `IPR 2m ~ 1`)*, ### **a ogni `L`, e la sua energia di legame `E0 - |mu|` converge** *(sotto).*
- ### **`(ii)` IL BORDO LOCALE:** ### **lo spettro locale `w_n(v) = (somma_{h in v} |psi_{n,h}|^2)/d_v`** *(somma `1` su `n`)*; ### **`F_v(E) = somma_{|mu_n| <= E} w_n(v)`; il bordo locale `E_v(f)` = il piu' piccolo `|mu_n|` con `F_v >= f`,** ### **a `f = 0.005` e `f = 0.02`** *(due valori, dichiarati: il secondo dice se il primo dipende dalla scelta)*. ### **Lo spostamento relativo `delta_v = (E_v - E_rif)/E_rif`, con `E_rif` = lo stesso `E(f)` sul toro perfetto** *(uguale a ogni nodo; si verifica)*. ### **Riportati: `n`, `k`, `l`, `i`, `j`, un nodo lontano** *(distanza `>= L/2 - 2`)*, ### **e il massimo di `|delta_v|` per anello di distanza `r = 0..8`.**
- ### **`(iii)` LA CONVERGENZA** *(`doc/PATTERN_DI_PROVA.md`)*: ### **un numero e' FISICO se lo scarto fra `L 36` e `L 48` e' minore di quello fra `24` e `36` E minore del `10%` del valore;** ### **altrimenti si scrive «NON CONVERGE» e il numero e' una lettura dello strumento.**
- ### **`(v)` `Lambda_k`:** ### **il vuoto uniforme `VUOTO_PER_ESTREMITA` su ogni estremita' del grafo col difetto;** ### **`Lambda` per nodo `= somma_h |phi_h|^2`, per estremita' `= Lambda/d`;** ### **`cs = Lambda/(Lambda + Lambda_c)` NON ha un valore di `Lambda_c` deciso** *(`flussi_parziali.cs`: «`lambda_c` SI PASSA, SEMPRE»)*: ### **riporto il rapporto `cs_v/cs_6` a `Lambda_c/Lambda_6` in `(0.1, 1, 10)`** *(una SCANSIONE dichiarata, non una scelta)*.

| | il criterio | il tipo |
|---|---|---|
| `1` | senza difetto lo spettro diretto = l'unione su tutte le fasi di Bloch di `_u1_terzo.H_gen` *(`eps 0`)* e di `_curvatura_parte2.H_moneta(..., 1, 1, 1, 0.5)` *(`eps 0.5`)*, ### **entro `1e-12`** *(due diagonalizzazioni di matrici diverse NON possono dare gli stessi bit: `1e-12` e' l'arrotondamento di `eigh` a questa taglia, dichiarato)*; ### **i gradi del grafo col difetto come attesi** | DEVE |
| `2` | `(i)`: ### **nessuno stato LOCALIZZATO nella banda proibita** *(`eps 0`, a ogni `L`)* | PUO' FALLIRE |
| `3` | `(ii)`: ### **`max |delta_v|` a distanza `>= 3` sotto `1%`** *(`f 0.005`, `eps 0`, `L 48`)* | PUO' FALLIRE |
| `4` | `(v)`: ### **`Lambda` per nodo `4/6` e `7/6` di quello a `6` ESATTI; per estremita' uguale ovunque** | DEVE |
| `5` | ### **«il difetto non cambia niente»: lo spettro col difetto = quello perfetto entro `1e-12`** | ### **DEVE FALLIRE, PER LA CHIAVE GIUSTA: la dimensione cresce di `6` estremita'** *(`2 m` da `6 L^2` a `6 L^2 + 6`)* **e almeno un livello si sposta di `> 1e-6`** |

### **Mi FERMO** ### **se il criterio `1` o `4` fallisce** *(la scena o il generatore sono sbagliati: niente numeri di `(i)`, `(ii)`)*.

## 3. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice.
