# IL CONTO DEL VUOTO *(la parte C3, l'aggiunta di Luca delle 20:53 al mandato delle 20:44)*: LA NASCITA E IL FLIP PAGATI DAL VUOTO?

> **Il mandato:** di Luca, `2026-10-25`, `20:53`, la parte `C3` *([[PROGETTO-MITOSI]], la sezione `3(c)` e `3(c-bis)`; [[D-BILANCIO-NASCITA]])*: ### **l'orientamento «lo spazio paga sempre col vuoto», messo alla prova sulla carta.**
> ### **Sulla carta: nessuna dinamica, nessun file del nucleo, nessuna regola di mitosi nel nucleo.** ### **Lo script `csv/_conto_del_vuoto.py`, il referto `doc/referti_l2/conto_del_vuoto.{txt,jsonl}`.**

**LIVELLO:** un conto d'energia su due mosse del grafo.

## 0. LA STELLA POLARE

1. **`A14`:** ### **e' la domanda:** ### **la mossa conserva le norme** *(`M`, `V`)*; ### **chi paga `Delta H_tot`?** 2. **Il gradino:** ### **il bilancio di una mossa, su `H_tot`.** 3. **Aggiunge un numero o una legge?** ### **No: misura due regole DICHIARATE, che non sono decise.** 4. **Tocca `rho`, `c_s` o il segno?** ### **Misura di quanto la rotazione del vuoto cambierebbe `cs`.** 5. **Emergente o imposto?** ### **Le regole di trasporto sono imposte dalla misura; il conto e' cio' che si misura.**

## 1. LE GRANDEZZE *(dal codice)*

- ### **`H_tot` = `energia_pesata.termini_di_h`, sommati** *(a forma spenta, `cs = None`: `G = H_tot`)*: ### **per nodo `-pi [(|psi|^2 - |S psi|^2/d) + (|phi|^2 - |S phi|^2/d)] + eps h + N`, per arco `-pi [|psi_0 - U psi_1|^2/2 + |phi_0 - phi_1|^2/2]`** *(`OMEGA_H = pi`; `N = rho ln(rho/(rho + Lambda))`)*.
- ### **LA SEPARAZIONE:** ### **la MATERIA = `H(psi, 0)`** *(con `phi = 0` `N` vale `0`)*; ### **il VUOTO = `H(0, phi)`; il LEGAME `N` = `H(psi, phi) - H(psi, 0) - H(0, phi)`.**
- ### ⭐ **UN FATTO DELLA FORMA, prima dei numeri:** ### **la parte del vuoto e' `-pi <phi|(I - P_u) + P_-|phi>`, e il generatore e' >= 0: il vuoto UNIFORME ne e' il MASSIMO** *(vale `0`)*. ### **Una rotazione del vuoto uniforme puo' solo ABBASSARE la sua energia quadratica:** ### **se una mossa ABBASSA `H_tot`, il vuoto da solo non la puo' restituire** *(lo misura `(iii)`, con il legame `N` incluso)*.

## 2. LA SCENA E LE REGOLE DI TRASPORTO *(DICHIARATE QUI: sono della misura, non della fisica)*

- ### **IL TORO PERFETTO `L x L`** *(`_massa_nei_difetti.toro`)*, ### **`L = 24` e `36`** *(la convergenza: il conto e' locale)*.
- ### **LA MATERIA:** ### **la coppia a `K`, il livello ALTO** *(`mu = +1/2`, l'autovettore di `_u1_terzo.H_gen(2pi/3, 2pi/3)`)*, ### **spin su, `rho = X = 0.1` per nodo** *(`_triangoli.X`, la densita' delle scene)*; ### **`eps 0`, `U = I`.** ### **IL VUOTO: `VUOTO_PER_ESTREMITA = 1` a ogni estremita'** *(`Lambda_k = 6`)*.
- ### **`(i)` LA NASCITA `(b1)`** *(la scena di `_massa_nei_difetti.sdoppia`: l'arco `i -> j` tolto, `n` legato a `i, j, k, l`)*: ### **IL PADRE E' `i`, il capo di PARTENZA dell'arco tolto.** ### **Il trasporto:** ### **l'estremita' dell'arco tolto in `i` diventa quella dell'arco `n-i` in `i`; quella in `j` diventa quella di `n-j` in `j`** *(la stessa direzione: `n` e' al punto medio)*; ### **`D7`: ogni estremita' del padre `x 1/sqrt(2)`; le `4` estremita' del figlio prendono `(1/sqrt 2) sqrt(N_p/4) chi/|chi|`** *(`N_p` la norma del padre prima, `chi` la SOMMA dello spinore sulle sue estremita': «la stessa fase»; la norma del figlio e' meta' di quella del padre)*; ### **le estremita' NUOVE in `k` e in `l`** *(verso `n`)* ### **partono da `0`** *(nessuna regola le assegna: la norma resta)*; ### **per `phi` lo stesso** *(con `phi` scalare)*.
- ### **`(ii)` IL FLIP** *(sul toro perfetto: l'arco `i -> j` tolto, l'arco `l -> k` messo)*: ### **i gradi `6, 6, 6, 6 -> 5, 5, 7, 7`;** ### **il trasporto: ogni estremita' che sopravvive tiene la sua ampiezza; quella dell'arco girato in `i` va in `l`, quella in `j` va in `k`** *(l'arco ruotato di `+90` gradi attorno al suo punto medio: `i` va verso `l`, `j` verso `k`)*. ### **E' una PERMUTAZIONE: le norme restano AL BIT.**
- ### **`(iii)` LA CAPACITA' DEL VUOTO:** ### **il sottospazio `S` = le estremita' dei nodi della mossa** *(`n` per la nascita; `i, j, k, l` per il flip)* ### **e dei loro vicini a un passo;** ### **la forma quadratica del vuoto ristretta a `S`, `A = -pi H_SS`** *(e il termine incrociato `b = -pi H_SO phi_O` con il vuoto fuori)*; ### **a norma `|phi_S|^2` data:** ### **LO SPETTRO** *(come chiede il mandato: `[lambda_min, lambda_max] |phi_S|^2`)* ### **E L'INTERVALLO ESATTO** *(con `b`: il problema della sfera, l'equazione secolare)*. ### **`|Delta H_tot|` della mossa contro la capacita', nel VERSO giusto** *(se la mossa alza `H_tot`, il vuoto deve abbassarsi, e viceversa)*.
- ### **`(iv)` L'OROLOGIO:** ### **la rotazione che annulla `Delta H_tot`, se esiste:** ### **sul cerchio massimo di `|phi_S|^2` dato fra `phi_S` e il punto estremo nel verso giusto** *(il piu' piccolo angolo che porta `H_tot` dopo la mossa e la rotazione al valore di prima, con `N` incluso)*: ### **la scelta della rotazione di norma minima, DICHIARATA** *(minima su QUEL cerchio, non su tutte le rotazioni)*. ### **`Delta Lambda_k` sui nodi di `S`, e `cs = Lambda/(Lambda + Lambda_c)`, per nodo e per estremita', a `Lambda_c/Lambda_6` in `(0.1, 1, 10)`** *(una scansione, `Lambda_c` non e' deciso)*.

## 3. I CRITERI *(fissati qui, prima dei numeri)*

| | il criterio | il tipo |
|---|---|---|
| `1` | ### **la NASCITA conserva `M` e `V` entro `1e-14` relativo** *(⚠ NON «al bit», come chiedeva la previsione: la nota di `DEC-D7-DIVISIONE` ha gia' misurato che `(1/sqrt 2)^2 - 1/2 = -1.11e-16`, e la somma di `rho` coincide al bit solo nel `23.7%` dei casi)*; ### **il FLIP AL BIT** *(una permutazione)*; ### **la rotazione `(iv)` entro `1e-14`** *(coseno e seno)* | DEVE |
| `2` | ### **il controllo: `H_tot` della scena prima della mossa = `energia_pesata.g_dello_stato` sul `Motore` della scena** *(a forma spenta)* ### **e `H_tot` per nodo uguale a ogni nodo del toro perfetto** *(lo stato e' di Bloch)* ### **entro `1e-12`** | DEVE |
| `3` | ### **la capacita' del vuoto locale basta per `(i)` e per `(ii)`** *(l'intervallo ESATTO contiene il valore che annulla `Delta H_tot`)* | PUO' FALLIRE |
| `4` | ### **`Delta H_tot` converge in `L`** *(lo scarto fra `24` e `36` sotto il `1%` del valore)* | DEVE |
| `5` | ### **«la mossa non cambia l'energia»** | ### **DEVE FALLIRE, PER LA CHIAVE GIUSTA: `|Delta H_tot| > 1e-6` per la nascita E per il flip** |

### **LA LETTURA, nessuna soglia:** ### **la variazione di `cs` per mossa contro quella che `gamma = 1` chiederebbe** *(la sezione `3(d)`: `|Phi|` per le lunghezze e per il tempo)*.

### **Mi FERMO** ### **se `1` o `2` fallisce.**

## 4. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice.
