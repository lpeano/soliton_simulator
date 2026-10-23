> ### ⛔ **GRIGLIA QUADRATA -- risultato da rifare sui triangoli (DECISIONE-SOLO-TRIANGOLI)**

# LA MONETA DENTRO IL TICK -- SOLO IL PROGETTO, SULLA CARTA

> **Il mandato:** di Luca, in coda dopo la forza da `cs` *(`557d94d6`)*. ### **NESSUN CODICE, NESSUN FILE DEL NUCLEO.** ### **L'ipotesi di Luca, da provare e NON decisa:**
> ### **oggi il cono** *(`theta = pi s <= pi`)* ### **limita il Grover e lo spostamento, ma la moneta** *(`exp(-i eps dtau_nodo sigma.n)`, `motore._moneta_spin`)* ### **e' una rotazione IN
> PIU' che non toglie niente al movimento**; ### **nelle camminate di Dirac** *(Feynman, D'Ariano-Perinotti)* ### **movimento e massa si DIVIDONO lo stesso tick.** ### **La forma
> scelta da Luca: UNA ROTAZIONE UNICA per tick, un generatore che contiene movimento e moneta, angolo totale `<= pi`** *(non la forma `cos/sin` di Feynman)*. ### **Il modo concreto
> NON e' deciso: qui si propone, e la scelta e' di Luca.**

**LIVELLO:** `L2`, un progetto. ### **Nessuna misura, nessuna legge cambiata.**

## 0. LA STELLA POLARE *(e' un PROGETTO: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica oggi** *(niente cambia)*; ### **si applichera' alla costruzione scelta.**
2. **Il gradino:** ### **`(a)` ogni costruzione torna al passo di oggi AL BIT in un limite dichiarato**; ### **`(b)` la misura in memoria** *(le prove di `44d4963d`)*; ### **`(c)` la scelta
   di Luca.**
3. **Aggiunge un numero o una legge?** ### **Nessun numero nuovo** *(tutti gli angoli vengono da `pi`, `s` ed `eps`)*; ### **le costruzioni `C2` e `C3` FONDONO due leggi in una**
   *(il conto delle leggi SCENDE di uno, `9-ter`)*; ### **`C1` le lascia due.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No.** ### **Tocca come la moneta sente `s`.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **dividere il tick fra movimento e massa fa scalare le masse insieme?** ### **La previsione** *(sez. `3`)* ### **dice: NON del tutto.**

## 1. IL PUNTO DI PARTENZA, DAL CODICE *(letto prima di scrivere)*

- ### **L'ORDINE DI OGGI** *(`composizione.ORDINE`, impronta `2e7f795d2a52fbe7`, `14` pezzi, palindromo, ogni pezzo a frazione `0.5`)*: `MATERIA-VUOTO`, `FASE-VUOTO`,
  ### **`MONETA-SPIN`, `GROVER`, `SPOSTAMENTO`**, `GROVER-VUOTO`, `SPOSTAMENTO-VUOTO` | `SPOSTAMENTO-VUOTO`, `GROVER-VUOTO`, ### **`SPOSTAMENTO`, `GROVER`, `MONETA-SPIN`**,
  `FASE-VUOTO`, `MATERIA-VUOTO`.
- ### **L'IMPRONTA DELL'ORDINE** e' `sha1` di `{"ordine": ordine}` *(`_genera.impronta`, chiamata in `_genera.py` per `composizione.py`)*: ### **cambia SOLO se cambia la lista
  `(id, frazione, tipo)`**; ### **cambiare cio' che fa un operatore cambia l'impronta della sua RIGA, non quella dell'ordine.**
- ### **I TRE GENERATORI, tutti come PROIETTORI** *(cosi' «l'angolo» e' un numero solo)*:
  - ### **nodo, `CAMM-GROVER`:** `G(theta) = exp(i theta K_n)`, ### **`K_n = I - P_u`** *(`P_u` il vettore uniforme sulle `2d` estremita' del nodo)*, ### **`theta = pi s_nodo`**;
  - ### **arco, `CAMM-SPOSTAMENTO`:** `hop(theta) = exp(i theta K_a)`, ### **`K_a = P- = (I - S_U)/2`**, ### **`theta = pi s_arco`** *(la media armonica)*;
  - ### **spin, `CAMM-MONETA-SPIN`:** `exp(-i a sigma.n) = e^{-i a} exp(i 2a K_c)`, ### **`K_c = (I - sigma.n)/2`** *(per estremita', il proiettore sullo spin opposto a `n`)*,
    ### **`a = eps s_nodo`** *(su un tick: due meta' da `eps s/2`)*. ### **Quindi, a meno di una fase globale, LA MONETA E' UNA ROTAZIONE D'ANGOLO `2 eps s`** ### **e oggi NESSUN cono
    la limita.**
- ### ⭐ **LA FRASE DEL MANDATO, RESA PRECISA:** ### **oggi, sul nodo, l'angolo per tick e' `pi s` (Grover) PIU' `2 eps s` (moneta)**: ### **a `eps 0.5` e `s = 1` fa `pi + 1`, oltre il
  cono.** ### **«La moneta dentro il tick» vuol dire: `angolo del movimento + angolo della moneta <= pi s`.**

## 2. LE COSTRUZIONI *(quattro; la `C4` per dire perche' no)*

> **Notazione:** `mu = 2 eps / pi` ### *(la frazione d'angolo della moneta: e' il rapporto fra l'angolo di oggi della moneta, `2 eps s`, e quello del movimento, `pi s`; ### **non e'
> un numero nuovo**)*. ### **Tutte e quattro vogliono `mu <= 1`, cioe' `eps <= pi/2`**: ### **un `eps` oltre ALZA** *(`A11`: un assert, non un clip)*; ### **`eps = 0.5` da' `mu =
> 0.3183`.**

### C1 -- IL BILANCIO ALTERNATO SUL NODO *(i pezzi di oggi, gli angoli divisi)*

1. **Il passo:** ### **lo stesso ordine di oggi**; ### **cambia l'angolo del Grover della materia:** `theta_G = pi s (1 - mu) = s (pi - 2 eps)`; ### **la moneta resta `2 eps s`**
   *(`exp(-i eps s sigma.n)`)*.
   ```yaml
   - id: CAMM-GROVER            # la stessa riga, con una dipendenza nuova
     tipo: pezzo_unitario
     operatore: grover_bilancio
     azione: nodo
     ambito: [psi_h]
     parametri: {eps: {da: CAMM-MONETA-SPIN}}   # eps letto dalla moneta, NON un secondo eps
     scheda: G = exp(i pi s (1 - 2 eps/pi) (I - P_u))
   ```
2. **Il cono:** ### **gli angoli si sommano a `pi s <= pi` PER COSTRUZIONE** *(`pi s (1 - mu) + pi s mu`)*. ### ⚠ **MA IL PRODOTTO DI DUE ROTAZIONI NON E' UNA ROTAZIONE con l'angolo
   somma:** ### **che le fasi proprie di `G * moneta` stiano in `[0, pi s]` e' un TEOREMA** *(di tipo Thompson: per generatori semidefiniti con norme che sommano `< pi`)* ### **che
   NON ho verificato**: ### **e' il controllo che PUO' FALLIRE del piano** *(sez. `5`)*.
3. **Al bit:** ### **a `eps = 0` `mu = 0`, `theta_G = pi s`: E' IL PASSO DI OGGI AL BIT** *(la moneta a `eps 0` e' l'identita')*.
4. **Locale e `A1`:** ### **locale** *(nodo ed estremita' del nodo)*; ### **nessun numero nuovo**, ma ### **il Grover legge `eps`**: ### **una legge che dipende dal parametro di un'altra.**
5. **I generatori che non commutano:** ### **si ALTERNANO, come oggi** *(palindromo, Strang)*: ### **`[K_n, K_c] != 0`** *(`P_u` mescola le estremita', `sigma.n_h` e' diverso per estremita')*,
   ### **e l'errore di Strang e' `O((pi s)^3 mu (1 - mu))` per tick.**
6. **I pezzi:** ### **tocca i due `CAMM-GROVER` della materia** *(non quelli del vuoto)*; ### **l'ordine NON cambia: l'impronta `2e7f795d2a52fbe7` RESTA**, ### **cambia l'impronta della
   riga `CAMM-GROVER`.**
7. **La previsione:** ### **a `s = 1` il Grover non e' piu' una riflessione** *(`theta_G = pi - 2 eps`)*: ### **il ramo di Dirac che oggi a `eps 0` si chiude al cono** ### **a `eps > 0`
   riceve un DIFETTO D'ANGOLO `pi (1 - s) + 2 eps s`**. ### **Stima a mano** *(massa proporzionale al difetto, da misurare)*: ### **`d ln Dt/ds` a `s = 1` circa `-(pi - 2 eps)/(2 eps)`**
   ### **= `-2.14` a `eps 0.5`** *(oggi `-1.635`)*, ### **`-0.57` a `eps 1`** *(oggi `-0.612`)*. ### **Le masse per tempo proprio vanno come `pi (1 - s)/s + 2 eps`**: ### **due specie
   con `eps` diversi NON hanno rapporto costante in `s`.**

### C2 -- LA ROTAZIONE UNICA SUL NODO *(la forma di Luca, locale)* -- ⭐ **la mia raccomandazione, sez. `4`**

1. **Il passo:** ### **un pezzo solo al posto di `MONETA-SPIN` + `GROVER`**, ### **due volte a frazione `0.5`**:
   `R_nodo(s) = exp(i pi s [ (1 - mu) K_n + mu K_c ])`, ### **`K_c = (+)_h (I - sigma.n_h)/2`** *(la somma diretta sulle estremita' del nodo)*. ### **L'ordine diventa di `12`
   pezzi**: `MATERIA-VUOTO`, `FASE-VUOTO`, ### **`GROVER-MONETA`**, `SPOSTAMENTO`, `GROVER-VUOTO`, `SPOSTAMENTO-VUOTO` | `SPOSTAMENTO-VUOTO`, `GROVER-VUOTO`, `SPOSTAMENTO`,
   ### **`GROVER-MONETA`**, `FASE-VUOTO`, `MATERIA-VUOTO`.
   ```yaml
   - id: CAMM-GROVER-MONETA      # sostituisce CAMM-GROVER e CAMM-MONETA-SPIN
     tipo: pezzo_unitario
     operatore: grover_moneta
     azione: nodo
     ambito: [psi_h]
     parametri: {eps: {valore: 0.5, dimensione: E^1}}
     scheda: exp(i pi s [(1 - 2 eps/pi)(I - P_u) + (2 eps/pi) (+)_h (I - sigma.n_h)/2])
   ```
2. **Il cono:** ### **`(1 - mu) K_n + mu K_c` e' una COMBINAZIONE CONVESSA DI DUE PROIETTORI**: ### **il suo spettro sta in `[0, 1]`** *(ogni proiettore ha norma `1`, e `mu` sta in
   `[0, 1]`)*, ### **quindi le fasi proprie di `R_nodo` stanno in `[0, pi s] ⊂ [0, pi]` PER COSTRUZIONE.** ### **Nessun tetto e nessun clip** *(`A11`)*: ### **`mu <= 1` si ASSERISCE.**
3. **Al bit:** ### **a `eps = 0`: `R_nodo = exp(i pi s K_n) = G(pi s)`, E LA MONETA E' L'IDENTITA': IL PASSO DI OGGI AL BIT** *(il prodotto `moneta(0) * G` e' `G`)*.
   ### ⚠ **AL BIT anche numericamente solo se il ramo `eps = 0` chiama la stessa funzione `FP.grover`**: ### **un'esponenziale per autovalori darebbe `G` a meno di qualche ulp.**
   ### **Il progetto: a `mu = 0` si chiama `FP.grover`** *(un ramo dichiarato, `P-R1`)*.
4. **Locale e `A1`:** ### **locale** *(il nodo e le sue `2d` estremita')*; ### **nessun numero nuovo** *(`mu` da `eps` e `pi`)*; ### **un `eps` solo.**
5. **I generatori che non commutano:** ### **SI SOMMANO in un esponenziale unico** *(e' la forma di Luca)*: ### **`R_nodo` NON e' `G * moneta` ne' il loro Strang**; ### **la differenza
   e' `O((pi s)^2 mu (1 - mu) [K_n, K_c])`.** ### **Il calcolo:** ### **`K` dipende solo dalla geometria del nodo** *(i versori `n_h`)*, ### **non da `s`**: ### **si diagonalizza UNA
   VOLTA** *(`K = V Lambda V^H`, matrice `4d x 4d`: `8 x 8` sul quadrato, `12 x 12` sui triangoli)* ### **e a ogni passo `R = V e^{i pi s f Lambda} V^H`** *(con `f` la frazione)*.
   ### ⚠ **Va rifatta se la geometria cambia** *(una crescita del grafo, un `n` che ruota)*.
6. **I pezzi:** ### **fonde `CAMM-MONETA-SPIN` e `CAMM-GROVER` della materia** *(`4` posizioni -> `2`)*; ### **l'ordine cambia: L'IMPRONTA `2e7f795d2a52fbe7` CAMBIA.** ### **Le leggi
   distinte che girano: da `7` a `6`.**
7. **La previsione:** ### **come `C1` al primo ordine in `mu`** *(gli stessi angoli)*: ### **il difetto d'angolo a `s = 1` e' `pi mu = 2 eps`**, ### **e la massa del generatore NON
   sparisce** *(nasce da `pi s < pi`, non dalla moneta)*. ### **La differenza da `C1` e' di ordine `mu (1 - mu)`**: ### **a `eps 0.5` `mu (1 - mu) = 0.217`**, ### **non piccola: le pendenze
   di `C1` e `C2` possono differire anche nel segno.** ### **Non so dire quale delle due e' piu' «universale» senza misurarle.**

### C3 -- LA ROTAZIONE UNICA SULL'ARCO *(la moneta va con lo spostamento)*

1. **Il passo:** ### **un pezzo solo al posto di `MONETA-SPIN` + `SPOSTAMENTO`**: `R_arco(s_arco) = exp(i pi s_arco [ (1 - mu) K_a + mu K_c^(arco) ])`, ### **`K_c^(arco)`** ### **sulle
   DUE estremita' dell'arco** *(ciascuna col suo `sigma.n_h`, nel suo riferimento: il trasporto `U` e' dentro `S_U`)*.
   ```yaml
   - id: CAMM-SPOSTAMENTO-MONETA  # sostituisce CAMM-SPOSTAMENTO e CAMM-MONETA-SPIN
     tipo: pezzo_unitario
     operatore: spostamento_moneta
     azione: arco
     ambito: [psi_h]
     parametri: {eps: {valore: 0.5, dimensione: E^1}}
     scheda: exp(i pi s_arco [(1 - 2 eps/pi) (I - S_U)/2 + (2 eps/pi) (+)_capi (I - sigma.n_h)/2])
   ```
2. **Il cono:** ### **come `C2`: convessa di due proiettori, fasi in `[0, pi s_arco]`.**
3. **Al bit:** ### **a `eps = 0`: `hop(pi s_arco)`, il passo di oggi AL BIT** *(con lo stesso ramo dichiarato di `C2`: a `mu = 0` si chiama `FP.hop_psi`)*.
4. **Locale e `A1`:** ### **locale** *(un arco, `4` componenti complesse: le due estremita' per lo spin)*; ### **nessun numero nuovo.**
5. **I generatori:** ### **sommati**, ### **il blocco e' `4 x 4` per arco** *(dipende da `U` e dai due `n_h`)*: ### **si diagonalizza una volta**, ### **ma va rifatto se `U` cambia**
   *(il trasporto e' una variabile: l'elettromagnetismo e la geometria)*.
6. **I pezzi:** ### **fonde `CAMM-MONETA-SPIN` e `CAMM-SPOSTAMENTO`**; ### **l'impronta CAMBIA.**
7. **La previsione:** ### ⭐ **la moneta sente `s_arco`** *(la media armonica)* ### **invece di `s_nodo`**: ### **a `cs` uniforme e' la stessa cosa** *(le prove di `44d4963d` non la
   distinguono da `C2` per questo)*, ### **in un gradiente differisce al SECONDO ordine** *(la media armonica e quella del nodo coincidono al primo)*. ### **Le masse: come `C2`, a meno
   della diversa non-commutazione** *(`[K_a, K_c]` invece di `[K_n, K_c]`)*.

### C4 -- LA ROTAZIONE UNICA GLOBALE *(nodo + arco + moneta in un esponenziale)* -- **perche' NO**

1. **Il passo:** `exp(i pi [ s (1 - mu) (K_n + K_a) + s mu K_c ])` ### **su tutto il grafo.**
2. **Il cono:** ### **NON per costruzione:** ### **`K_n + K_a` ha norma fino a `2`** *(due proiettori che si sovrappongono sulle estremita')*: ### **servirebbe dividere per `2`, e il passo a
   `eps 0` NON tornerebbe piu' quello di oggi.**
3. **Al bit:** ### **no**, ### **per la ragione sopra e perche' un esponenziale unico di nodo + arco NON e' il prodotto di oggi.**
4. **Locale:** ### ⛔ **NO.** ### **I termini di nodo e d'arco si sovrappongono e non commutano**: ### **l'esponenziale della somma accoppia nodi a ogni distanza** *(decade, ma non
   si ferma)*. ### **Tagliarlo con Strang riporta all'alternanza, cioe' a `C2` + lo spostamento.**
5-7. ### **Non si misura.** ### **E' scritta perche' e' l'unica lettura LETTERALE di «un generatore che contiene movimento e moneta»**, ### **e la sua impossibilita' dice dove sta il
   limite: il movimento ha DUE generatori, e solo uno dei due puo' stare con la moneta in un pezzo locale.**

### ⚠ UNA VARIANTE SCARTATA *(scritta perche' qualcuno la proporra')*: «tutto il tempo proprio nella moneta»

### **`theta_mov = pi - 2 eps s`, moneta `2 eps s`, totale `pi` a ogni `s`.** ### **Le masse per tempo proprio sarebbero `~ 2 eps` costanti** *(scalerebbero insieme!)*, ### **ma a `eps = 0`
il movimento sarebbe a `pi` dappertutto: la materia NON sentirebbe piu' `cs`** *(la sua velocita' limite non seguirebbe quella della luce del vuoto, che resta a `pi s`)*. ### **Non torna al
bit, e rompe «la stessa luce locale»** *(`B-4`)*: ### **non la propongo.**

## 3. LA PREVISIONE CHE VALE PER TUTTE *(scritta prima di ogni misura)*

- ### ⭐ **UNA COSTRUZIONE CHE TORNA AL BIT A `eps = 0` NON CAMBIA LA SPECIE `eps = 0`.** ### **Quindi la massa del solo generatore** *(`Dt ~ pi s (1 - s)`, che si spegne al cono)*
  ### **RESTA com'e' in `C1`, `C2`, `C3`**, ### **e i `V_ij` fra `eps 0` e `eps > 0` restano sopra `1e-3`.** ### **La moneta dentro il tick puo' cambiare SOLO le specie con `eps > 0`.**
- ### **LA RADICE della non-universalita'** *(la mia lettura, da `44d4963d` e `557d94d6`)*: ### **la massa del generatore nasce da `theta = pi s < pi`**, ### **cioe' dalla regola
  `(B)` del tempo proprio, non dalla moneta**; ### **per tempo proprio va come `~ pi (1 - s)/s`, che dipende da `s`**; ### **la massa della moneta per tempo proprio e' `~ eps`, gia' oggi
  indipendente da `s`.** ### **Dividere il tick non tocca la prima.**
- ### **LE PENDENZE A `s = 1`** *(stime a mano, `C1`; `C2` e `C3` diverse di `O(mu (1 - mu))`)*: ### **`-2.14` a `eps 0.5`, `-0.57` a `eps 1`**; ### **e dopo `557d94d6`** *(Hamilton)*
  ### **la forza non le segue: segue `omega(0)` e la curvatura** ### **-- quindi la misura deve dare anche `omega(0)(s)`, non solo il `Dt` del fit.**

## 4. IL CONFRONTO, E LA MIA RACCOMANDAZIONE

| | `C1` bilancio alternato | `C2` rotazione unica sul nodo | `C3` rotazione unica sull'arco | `C4` globale |
|---|---|---|---|---|
| la forma di Luca *(un esponenziale)* | no *(prodotto)* | **si'** | **si'** | si', letterale |
| il cono per costruzione | da dimostrare *(Thompson)* | **si'** *(convessita')* | **si'** *(convessita')* | no |
| al bit a `eps = 0` | **si'** | **si'** *(col ramo `FP.grover`)* | **si'** *(col ramo `FP.hop_psi`)* | no |
| locale | si' | si' | si' | **no** |
| numeri nuovi | nessuno | nessuno | nessuno | nessuno |
| leggi che girano | `7` | **`6`** | **`6`** | -- |
| impronta `2e7f795d` | **resta** | cambia | cambia | cambia |
| la moneta sente | `s_nodo` | `s_nodo` | `s_arco` | -- |
| costo | come oggi | `eig` una volta per nodo | `eig` una volta per arco, rifatto se `U` cambia | -- |

### 💡 **RACCOMANDAZIONE** *(mia; LA SCELTA E' DI LUCA)*: ### **`C2`, misurata INSIEME a `C1` come controllo.** ### **Perche':** ### **`C2` e' l'unica che realizza la forma
scelta** *(un esponenziale)* ### **restando locale, col cono per costruzione e al bit a `eps 0`, e TOGLIE una legge**; ### **`C1` ha GLI STESSI ANGOLI e differisce SOLO per
l'esponenziale unico** ### **-> la coppia `C1`/`C2` isola l'effetto della non-commutazione** *(un interruttore alla volta, par. `3`)*. ### **`C3` dopo, se Luca vuole che la moneta senta
l'arco**: ### **a `cs` uniforme non si distingue da `C2` per la media, solo per il commutatore.** ### ⚠ **E la previsione onesta e' che NESSUNA delle tre faccia scalare insieme la specie
`eps 0` con le altre** *(sez. `3`)*.

## 5. IL PIANO DELLA MISURA CHE SEGUIRA' *(in memoria, NESSUN file del nucleo)*

- ### **Lo strumento** *(`csv/_moneta_nel_tick.py`, da scrivere SOLO se Luca sceglie)*: ### **gli operatori varianti `grover_bilancio` e `grover_moneta` sostituiti IN MEMORIA nel
  dizionario `mot.operatori` della scena** *(come `cs` e `eps` nelle misure di oggi)*, ### **`leggi.yaml`, l'impronta e il nucleo intatti.** ### ⚠ **Per `C2` l'ordine ha `12` pezzi:
  in memoria si sostituisce `MONETA-SPIN` con l'identita' e `GROVER` con `grover_moneta`** *(stessa lunghezza, `14` pezzi: e' un modo di misurare, non l'ordine proposto)*.
- ### **Le prove:** ### **quelle di `44d4963d`** *(le catene, i `V_ij`, l'orologio a `k = pi/4`, lati `32` e `64`, `eps` `0`-`1` -- ma `eps <= pi/2`, quindi `0`, `0.25`, `0.5`, `0.75`,
  `1.0` vanno tutti)*; ### **le pendenze locali `d ln Dt/ds` e `d omega(0)/ds` fra `s 0.99` e `1`**; ### **per `oggi`, `C1`, `C2`.**
- ### **I CRITERI, FISSATI ORA:**
  - ### **DEVE PASSARE, il ritorno al bit:** ### **a `eps = 0`, `A(k)` di `C1` e di `C2` UGUALE a quella di oggi AL BIT** *(differenza `0.0` su ogni `k`)*.
  - ### **DEVE PASSARE, l'unitarieta':** ### **`|A(k)^H A(k) - I| < 1e-12`** per `C1` e `C2`.
  - ### **DEVE PASSARE, il cono di `C2`:** ### **le fasi proprie di `R_nodo` in `[0, pi s]`** *(e' un teorema: se fallisce, lo strumento e' sbagliato)*.
  - ### **DEVE FALLIRE:** ### **«`C2 = C1`» a `eps 0.5`** *(i generatori non commutano: la differenza di `A(k)` deve essere `> 1e-6`, stampata; se e' `0`, l'esponenziale unico non e'
    stato costruito)*.
  - ### **PUO' FALLIRE:** ### **il cono di `C1`** *(le fasi proprie di `G(theta_G) * moneta` in `[0, pi s]`: il teorema che non ho verificato)*.
  - ### **IL VERDETTO DI FISICA:** ### **la tabella dei `V_ij`** *(soglia di lettura `1e-3`, come `44d4963d`)* ### **e quella delle pendenze, accanto alla previsione della sez. `3`**;
    ### **senza conclusioni oltre la tabella.**

## 6. TODO DEL NEXT STEP

1. questo task history, committato e pushato, con la relazione;
2. **ASPETTARE LA SCELTA DI LUCA** *(`C1`, `C2`, `C3`, o nessuna)*: ### **nessuno strumento prima** ([[L-DOPO-STOP]]);
3. poi: lo strumento della sez. `5`, il suo task history, la misura.

### ❓ **LA DOMANDA PER LUCA:** ### **quale costruzione** *(`C1`, `C2`, `C3`)*, ### **e se la misura deve comprendere `C1` come controllo di `C2`.** *(Criterio di chiusura: una tua
decisione registrata.)*
