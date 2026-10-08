# IL PROTOTIPO AL PRIMO ORDINE — **un banco fuori dal simulatore, per vedere se un solitone nasce su un grafo**

> **Mandato di Luca, 2026-10-08 (punto 2 di `A16`).** ### ⛔ **Il simulatore NON si tocca
> *(`b8c21049`)*, e il prototipo NON lo importa:** vive in `proto_primo_ordine/`, da solo.
> ### **`A16` è committato in `e17a334`, il piano in `89ad8cd`.**

## 1. RAGIONAMENTO PRELIMINARE

### **CHE COSA SI VUOLE SAPERE.** Se la forma di `A16` — ### **primo ordine, una sola `H`,
unitaria** — su un grafo 3D ### **tenga un pacchetto localizzato** invece di disperderlo. Se sì,
la riscrittura ha un punto d'appoggio; se no, lo sapremo ### **prima** di riscrivere il
simulatore.

### ⚠ **CHE COSA NON SO, e lo scrivo prima:**

| | |
|---|---|
| se un solitone ### **nasca** su un grafo geometrico casuale | non lo so. Su una catena `1D` il solitone di Schrödinger non lineare è ### **noto** *(ed è il controllo positivo)*, ma un grafo 3D ha ### **grado alto** e ### **disordine**: la localizzazione potrebbe venire dal disordine *(Anderson)* e ### **non** dalla non linearità, e sarebbe un falso positivo |
| quale `g` | ### **non lo scelgo: lo SCANDISCO.** Cinque valori dichiarati prima |
| se l'integratore tenga | il punto medio implicito conserva norma ed energia ### **per costruzione**, ma su un grafo serve un'iterazione: ### **si misura la deriva**, non si promette |

### ⛔ **E IL FALSO POSITIVO CHE MI PREOCCUPA, scritto adesso:** un pacchetto che
### **non si allarga** può essere ### **localizzazione di Anderson** del grafo disordinato,
### **non** un solitone. ### ➜ **Per questo il criterio di Luca chiede il confronto con
`g = 0`:** se anche a `g = 0` il pacchetto resta stretto, ### **non è la non linearità**, ed è
un `NON NASCE` travestito. ### **Lo riporto come tale.**

## 2. PROGETTAZIONE

### 2.1 **IL GRAFO** *(i valori si dichiarano, non si scelgono dopo)*

| | |
|---|---|
| nodi | ### **`400`** *(nell'intervallo `300`-`500` che il mandato dà)* |
| posizioni | uniformi in un cubo di lato ### **`1.0`**, con `rng` dal seme |
| connessione | ### **per distanza**, come nel simulatore: arco se `d_ij <= R` |
| `R` | ### **`0.22`**, scelto perché dà un grado medio ### **`~16`** su `400` nodi in `3D` — e il grado medio ### **si MISURA e si STAMPA**, non si assume |
| `w_ij` | ### **`exp(-d_ij / LAM_P)`** con `LAM_P = R/2 = 0.11`: un peso che decade con la distanza, ### **FISSO** |
| `U_ij ∈ SU(2)` | una rotazione ### **casuale ma FISSA** per arco, dal seme, con `U_ji = U_ij†` ### **imposta per costruzione** |

### ⛔ **`w` e `U` SONO FISSI, ED È UNA VIOLAZIONE DI `A16.3`, DICHIARATA:** sono memorie
congelate. ### **`A16.3` vuole memorie come gradi di libertà lenti DENTRO `H`**, e il mandato
dice che questa è la ### **prima** versione e che la memoria dinamica è ### **il passo
successivo, deciso da Luca.**

### 2.2 **`H`, E L'EVOLUZIONE**

```
H(psi) = - somma_archi w_ij * ( <psi_i| U_ij |psi_j> + c.c. )  +  (g/2) * somma_k |psi_k|^4
i * dpsi_k/dt = dH/dpsi_k*  =  - somma_{j vicini} w_kj * U_kj psi_j  +  g * |psi_k|^2 psi_k
```

### ✔ **E `H` è REALE perché `U_ji = U_ij†`:** il termine d'arco è `z + conj(z)`, e la
### **somma su archi orientati con il coniugato** è esattamente l'hermitianità. ### **Lo verifica
il collaudo, non la mia parola.**

### **`φ_k` SI LEGGE DA `ψ_k`**, e non è una variabile: `φ_k = 2 · arg(prima componente non
nulla di ψ_k)`, nel dominio ### **`[0, 4π)`**. ### ⚠ **La convenzione si dichiara**, come in
`D3`.

### 2.3 ⭐ **L'INTEGRATORE: IL PUNTO MEDIO IMPLICITO, e PERCHÉ proprio lui**

```
psi(t+dt) = psi(t) - i*dt * F( (psi(t) + psi(t+dt))/2 )      risolto per iterazione
```

| | |
|---|---|
| perché ### **il punto medio implicito** | per la parte ### **lineare** è la trasformata di Cayley, che è ### **unitaria ESATTAMENTE** *(norma conservata al bit, non a meno di `O(dt^p)`)*; e per una `H` reale conserva l'energia ### **al second'ordine**, con la deriva che ### **non cresce** *(simmetrico nel tempo)* |
| perché ### **non** Runge-Kutta | `RK4` ### **non** conserva la norma: la fa derivare monotonamente, e su `10^4` passi la deriva sarebbe il risultato invece dell'errore |
| perché ### **non** lo split-step | sarebbe altrettanto buono *(unitario a pezzi)*, ma su un grafo il pezzo lineare ### **non** è diagonale in nessuna base nota a priori: servirebbe un'esponenziale di matrice sparsa. ### **Il punto medio costa un'iterazione e non una diagonalizzazione** |
| ### ⚠ **il costo dichiarato** | l'iterazione va a convergenza con una tolleranza, e ### **la tolleranza è un numero**: si dichiara, si mette ### **molto** sotto la soglia del collaudo, e ### **il numero di iterazioni si MISURA** |

### 2.4 **IL COLLAUDO, PRIMA DI OGNI CORSA** *(i quattro che il mandato chiede)*

| | che cosa deve venire |
|---|---|
| ### **(a)** | norma ed energia conservate: deriva relativa ### **`< 1e-8`** su ### **`10^4`** passi |
| ### **(b)** | ### **CONTROLLO POSITIVO NOTO:** catena `1D`, `U = I`, ### **una** componente — il solitone `sech` della `NLS` focalizzante si propaga ### **intatto** *(profilo entro `1e-3` dopo `10` tempi caratteristici)* |
| ### **(c)** | ### ⛔ **IL CASO CHE DEVE FALLIRE:** con `g = 0` lo stesso profilo ### **si DISPERDE** |
| ### **(d)** | ### **doppia copertura:** `φ_k → φ_k + 2π` cambia segno a `ψ_k`, e ### **`H` ne misura l'effetto** |

### ⚠ **E SULLA (b) UNA COSA SI DICHIARA PRIMA:** la `NLS` continua ha il solitone
`psi = A sech(A(x-x0)/sqrt(2)) e^{i...}`; su un ### **reticolo** la `DNLS` ### **non** ha un
solitone esatto — ha un ### **solitone discreto** che si propaga solo se è abbastanza largo
rispetto al passo. ### ➜ **Quindi la larghezza si sceglie LARGA rispetto al passo del reticolo,
e il numero si dichiara.** ### **Se il profilo si deformasse per la discretizzazione e non per
la fisica, sarebbe un falso negativo, e il collaudo deve poterlo distinguere.**

### 2.5 **L'ESPERIMENTO**

| | |
|---|---|
| lo stato iniziale | ### **pacchetto gaussiano** centrato sul nodo più vicino al centro del cubo: `psi_k = exp(-(d_k/sigma)^2) * chi_0` con `sigma = 2R = 0.44` e `chi_0 = (1, 0)`, poi ### **normalizzato** a `somma \|psi\|^2 = 1` |
| `g` | ### **cinque valori, dichiarati ADESSO: `0`, `-2`, `-5`, `-10`, `-20`** *(negativo = focalizzante, perché il termine è `+g/2 \|psi\|^4`)* |
| semi | ### **`3`**: `11`, `12`, `13`. ### ⛔ **`P3` NON è soddisfatta**, e il referto lo dirà |
| la misura | il ### **rapporto di partecipazione** `PR = 1 / somma_k \|psi_k\|^4` *(con `somma \|psi\|^2 = 1`)*: è ### **il numero di nodi su cui lo stato è spalmato** |
| il tempo | ### **dichiarato nel collaudo**, e la corsa deve stare ### **sotto i 20 minuti**: se li supera, ### **FERMO e lo scrivo** |

## 3. I CRITERI, FISSATI ADESSO *(quelli di Luca)*

| | il criterio |
|---|---|
| ### **`NASCE UN SOLITONE SUL GRAFO`** | se per ### **almeno un `g`** il rapporto di partecipazione resta ### **entro un fattore `2`** dal valore iniziale fino al tempo finale, in ### **tutti e `3`** i semi, ### **MENTRE** con `g = 0` cresce di ### **più di un fattore `5`** |
| ### **`NON NASCE`** | se ### **nessun `g`** tiene |
| in più | la ### **frequenza dell'orologio** del solitone *(`dφ/dt` al centro)* contro ### **l'energia per particella**: ### **l'orologio di de Broglie (`A16.2`) si MISURA** |

## 4. LE PREVISIONI, PRIMA DI VEDERE I NUMERI

| id | la previsione |
|---|---|
| **`PP-1`** | il collaudo ### **(a)** chiude: norma ### **al bit** *(il punto medio è unitario esatto sul lineare)* e energia con deriva ### **`< 1e-10`**, meglio della soglia |
| **`PP-2`** | il collaudo ### **(b)** chiude: il `sech` si propaga entro `1e-3` |
| **`PP-3`** | ### **il caso che DEVE fallire fallisce:** a `g = 0` il profilo si allarga di ### **oltre il `50 %`** |
| **`PP-4`** | ### **`NASCE UN SOLITONE SUL GRAFO`**, e il `g` che tiene è fra i ### **due più negativi** *(`-10`, `-20`)*: su un grafo di grado `~16` serve più non linearità che su una catena |
| **`PP-5`** | ### ⛔ **e a `g = 0` il `PR` cresce di MENO di `5`**, perché il grafo è ### **disordinato** e la localizzazione di Anderson lo frena. ### **Scritta per poter PERDERE: se è così, il criterio di Luca NON si può soddisfare come scritto, e lo dirò invece di aggirarlo** |
| **`PP-6`** | ### **l'orologio di de Broglie si vede:** `dφ/dt` al centro correla con l'energia per particella, col segno giusto, ### **entro il `30 %`** |

### **COSA MI FAREBBE FERMARE:** il collaudo `(a)` che non chiude *(allora l'integratore è
sbagliato e non c'è esperimento)*; il `(b)` che non chiude; una corsa oltre i ### **`20`
minuti**.

## 5. LA STELLA POLARE — *le cinque risposte, per iscritto*

| | la risposta |
|---|---|
| **1 `A14`** | ### ⭐ **conserva PER COSTRUZIONE, ed è il punto:** una sola `H` reale e un integratore unitario danno norma ed energia conservate, e il collaudo `(a)` ### **le misura**. ### **È `A16.4` messo alla prova** |
| **2 i tre gradini** | ### **(c) coincide con un limite noto** — il solitone `sech` della `NLS` è il controllo positivo — e ### **(a) robusto al rumore numerico**. ### ⛔ **Il gradino (b) NON è raggiunto:** `3` semi, `P3` non soddisfatta |
| **3 numeri o leggi** | ### ⚠ **AGGIUNGE NUMERI, e li dichiaro TUTTI:** `R = 0.22`, `LAM_P = 0.11`, `sigma = 0.44`, la tolleranza dell'iterazione, i cinque `g`. ### **Sono numeri DI BANCO, non di legge:** fissano la scena, non la forma di `H`. ### ⛔ **E `w` e `U` FISSI sono una violazione di `A16.3`, dichiarata provvisoria** |
| **4 `rho`, `c_s`, il SEGNO** | ### **nessuno:** nel prototipo non c'è metrica. ### **Resta fuori, e resta una decisione di Luca** |
| **5 emergente o imposto** | ### ⭐ **È LA DOMANDA DEL BANCO.** Il solitone, se c'è, ### **emerge** da `H`: nessuna legge lo mette lì. ### ⚠ **Ma il confronto con `g = 0` è ciò che distingue l'emergenza dalla localizzazione del DISORDINE**, e `PP-5` dice che potrebbe non bastare |

## 6. TODO DEL NEXT STEP

1. ### **questo file**, committato e pushato ### **PRIMA** del codice;
2. `proto_primo_ordine/` con: il grafo, `H`, l'integratore, le misure. ### ⛔ **Senza importare
   il simulatore**, e il prototipo lo ### **asserisce**;
3. il ### **collaudo coi quattro controlli**, committato ### **PRIMA** delle corse;
4. le corse: ### **`5` valori di `g` × `3` semi**, ### **brevi** — e se una supera i `20` minuti
   ### **FERMO e lo scrivo**;
5. ### **un referto** coi numeri dai json;
6. poi ### ⛔ **FERMO: la memoria dinamica dentro `H`, le nascite e il vuoto sono decisioni
   successive di Luca.**

---

# ⭐ **ANNOTAZIONE DEL 2026-10-08, PRIMA DELLE CORSE** *(par.8: si annota, non si riscrive)*

## ⛔ **① IL BRACCIO `U = I`, CHIESTO DAL GUARDIANO — E HA RAGIONE**

> **«Un campo `SU(2)` casuale localizza da sé (Anderson con flusso di gauge casuale), e il
> confronto a `g = 0` non distinguerebbe il disordine del grafo da quello di `U`.»**

### ✔ **E IL RILIEVO COLPISCE ESATTAMENTE IL PUNTO DEBOLE CHE AVEVO SCRITTO IO** *(par.1: «un
pacchetto che non si allarga può essere localizzazione di Anderson»)*, ### **ma io avevo
nominato UNA sola fonte di disordine — il grafo — e ce ne sono DUE.** Il flusso di gauge
casuale su un grafo di grado `~14` è un disordine ### **a sé**, e il controllo `g = 0` da solo
### **non li separa.**

### **IL BRACCIO CHE SI AGGIUNGE:** ### **`U_ij = I` su tutti gli archi**, stessi grafi, stessi
semi, stessi `5` valori di `g`. ### **Due bracci, quindi:**

| braccio | `U_ij` | che cosa isola |
|---|---|---|
| ### **`U-CASO`** | `SU(2)` casuale ma ### **fissa** *(quello di prima)* | disordine del grafo ### **+** flusso di gauge |
| ### **`U-UNO`** | ### **identità** su tutti gli archi | ### **solo** il disordine del grafo |

### ➜ **LA LETTURA, fissata adesso:** si riporta il rapporto di partecipazione ### **a
`g = 0`** nei due bracci. ### **Se resta stretto SOLO in `U-CASO`, la localizzazione viene da
`U`** — e un `PR` che non cresce a `g ≠ 0` ### **non** sarebbe un solitone. ### **Se resta
stretto in ENTRAMBI, viene dal GRAFO.** ### **Se in nessuno dei due, il controllo è pulito e il
criterio di Luca si può applicare.**

### **E I CRITERI SONO GLI STESSI PER I DUE BRACCI**, come il mandato dice: `NASCE UN SOLITONE
SUL GRAFO` se per almeno un `g` il `PR` resta entro un fattore `2` in tutti e `3` i semi
mentre a `g = 0` cresce di oltre `5`; `NON NASCE` se nessun `g` tiene.

### ⚠ **E LA PREVISIONE `PP-5` SI RAFFORZA, non cambia:** avevo scritto che a `g = 0` il `PR`
crescerà di ### **meno** di `5` per il disordine. ### **Ora ho due bracci per vedere di QUALE
disordine si tratta**, e la previsione nuova è: ### **`U-UNO` cresce PIÙ di `U-CASO`**, perché
ha una sorgente di disordine in meno.

## ⛔ **② IL MIO DISCRIMINANTE DI `(b)` CONFLATAVA DUE CAUSE, E L'HA MOSTRATO DA SÉ**

Avevo scritto che il residuo del solitone *(`1.903e-03` contro una soglia di `1e-3`)* fosse
### **della discretizzazione spaziale**, e avevo messo un test: ### **se il solitone si allarga,
lo scarto deve CALARE.**

### ⛔ **MISURATO: NON CALA.** `1.903e-03` a `LARG = 8` contro ### **`2.193e-03`** a
`LARG = 12`, un fattore `0.87` — cioè ### **cresce appena.**

### ➜ **E LA CAUSA È NEL DISEGNO DEL MIO TEST:** scalavo `dt ∝ LARG²` *(perché la frequenza del
solitone va come `η²`)*, e così ### **l'errore TEMPORALE resta FISSO per costruzione** — il
test non poteva vedere il reticolo. ### **Il mio discriminante non discriminava, e il numero me
lo ha detto.**

### ⭐ **IL DISEGNO NUOVO, che separa le due cause una per volta:**

| | che cosa varia | che cosa dice |
|---|---|---|
| ### **(b-i)** | `LARG = 8`, `dt = 0.002` | il riferimento |
| ### **(b-ii)** | `LARG = 8`, ### **`dt` DIMEZZATO** | se lo scarto ### **cala di ~`4`** *(secondo ordine)*, il residuo è ### **DEL PASSO TEMPORALE** |
| ### **(b-iii)** | `LARG = 12`, `dt ∝ LARG²` | ### **lo scarto RESTA**, e questo ### **conferma** che non è spaziale: quella scalatura tiene l'errore temporale fisso |

### **E LA SOGLIA SI APPLICA A `(b-ii)`:** se con `dt` dimezzato lo scarto va ### **sotto
`1e-3`**, il controllo passa e il residuo è ### **spiegato**. ### ⛔ **Se non ci va, NON lo
chiamo discretizzazione: lo riporto come residuo NON SPIEGATO, e le corse non partono.**

---

# ⭐ **ANNOTAZIONE ②, PRIMA DELLE CORSE: L'ESPERIMENTO DEL MARE** *(2026-10-08)*

> ### ⛔ **L'IDEA DI LUCA, e il rilievo che mi coglie in pieno:**
> **«I solitoni alla scala di Planck fanno dei campi, e i campi per interferenza generano le
> masse. L'esperimento del pacchetto singolo prova solo che una massa GIÀ FORMATA si sostiene,
> NON che nasce.»**

### ✔ **HA RAGIONE, E IL DIFETTO ERA NEL DISEGNO, NON NEI NUMERI.** Il mio esperimento parte da
un ### **pacchetto già localizzato**: qualunque cosa misuri, misura ### **la persistenza**, non
### **la genesi**. ### ➜ **E il bersaglio del progetto è la genesi** *(`doc/IPOTESI_gravita_a_spinta.md`,
`doc/REGISTRO_FISICA.md`: «l'aggregazione di spazio-tempo-materia»)*. ### **Il mare è
l'esperimento giusto, e il pacchetto resta come controllo di persistenza.**

## **LO STATO INIZIALE DEL MARE** *(i valori si dichiarano ADESSO)*

| | |
|---|---|
| `\|ψ_k\|` | ### **uguale su tutti i nodi**, con ### **`ρ_0 = \|ψ_k\|² = 1`** — quindi norma totale `= n = 400` |
| ### ⚠ **perché `ρ_0 = 1` e non la norma `1`** | con norma totale `1` si avrebbe `ρ_0 = 1/400 = 0.0025`, e il termine non lineare `g·ρ_0` sarebbe ### **`0.05` a `g = -20`** contro una scala di salto `~5`: ### **la non linearità sarebbe NEGLIGIBILE e non succederebbe niente, per costruzione.** Con `ρ_0 = 1` il confronto è `g` contro `~5`. ### **È un numero di banco, ed è dichiarato** |
| `χ_k` | ### **uguale** su tutti i nodi: `(1, 0)` |
| `φ_k` | `φ_0 + disturbo`, con disturbo uniforme in `[-ε, +ε]` e ### **`ε = 0.01` rad** |
| ### ⛔ **nessuna concentrazione iniziale** | ed è il punto: il mare è ### **uniforme in modulo** |

## **IL TEMPO, E PERCHÉ QUESTA SCALA**

Il tempo caratteristico del mare ### **non** è quello del pacchetto: è il tempo
dell'### **instabilità modulazionale**, che per la `NLS` focalizzante cresce come
### **`1/(\|g\|·ρ_0)`**.

| | |
|---|---|
| `t_c` | ### **`1/(\|g\|·ρ_0)`** per `g ≠ 0`; per `g = 0` ### **non è definito**, e si usa quello di `\|g\| = 5` ### **dichiarandolo** |
| la corsa | ### **`5000` passi** con `dt = 0.002`, cioè `T = 10` — e `T` si riporta ### **in unità di `t_c`** per ciascun `g` *(`50 t_c` a `g = -5`, `20 t_c` a `g = -2`, `200 t_c` a `g = -20`)* |

## **LE MISURE**

| | come |
|---|---|
| il ### **rapporto di partecipazione** globale | `PR = 1/Σρ̂²` con `ρ̂` normalizzata |
| i ### **GRUMI** | i nodi con `ρ_k > 3·⟨ρ⟩`, raggruppati in ### **componenti connesse SUL GRAFO** |
| la ### **vita** di un grumo | un grumo ### **sopravvive** al campione successivo se esiste un grumo che ne sovrappone ### **almeno il `50 %`** dei nodi; le catene di sopravvivenze danno la vita, ### **in unità di `t_c`** |
| la ### **norma** di un grumo | `Σρ_k` sui suoi nodi |
| la ### **energia** di un grumo | il termine non lineare sui suoi nodi ### **più** i salti con ### **entrambi** gli estremi dentro. ### ⚠ **I salti che ATTRAVERSANO il bordo NON si attribuiscono a nessuno**, e si riportano a parte: metterli d'autorità in un grumo falserebbe il bilancio — ### **la stessa regola delle tre classi di `D3`** |
| l'### **orologio** *(`A16.2`)* | `dφ/dt` al nodo di `ρ` massimo del grumo, contro la sua ### **energia per unità di norma** |

## **I CRITERI, FISSATI ADESSO** *(quelli di Luca)*

| | il criterio |
|---|---|
| ### **`LE MASSE NASCONO DALL'INTERFERENZA`** | se per ### **almeno un `g` focalizzante**, in ### **tutti e `3`** i semi si formano grumi che durano ### **più di `10 t_c`**, ### **MENTRE** con `g = 0` il mare resta uniforme ### **entro un fattore `2`** della densità media |
| ### **`NON NASCONO`** | se ### **nessun `g`** produce grumi duraturi |
| ### ⛔ **IL CASO CHE DEVE FALLIRE** | con ### **`ε = 0`** *(mare perfettamente uniforme)* ### **non deve nascere niente**: la simmetria ### **non si rompe da sola** |
| e ### **i due bracci separati** | se i grumi nascono ### **solo** con `U` casuale, potrebbe essere ### **localizzazione di Anderson** e non interferenza non lineare |

## **LE PREVISIONI, PRIMA DI VEDERE I NUMERI**

| id | la previsione |
|---|---|
| **`PM-1`** | ### **i grumi NASCONO** per i `g` più negativi: l'instabilità modulazionale è ### **il meccanismo standard** della `NLS` focalizzante, e qui c'è |
| **`PM-2`** | ### ⛔ **il caso `ε = 0` NON produce niente**, e il residuo resta al livello dell'### **arrotondamento**: la simmetria non si rompe da sola, e se si rompesse sarebbe ### **un difetto del mio codice**, non fisica |
| **`PM-3`** | i grumi nascono ### **in ENTRAMBI i bracci**, perché l'instabilità modulazionale ### **non ha bisogno di disordine** — le basta la non linearità. ### **Scritta per poter PERDERE: se nascono solo in `U-CASO`, è Anderson e lo dirò** |
| **`PM-4`** | a `g = 0` il mare ### **resta uniforme entro un fattore `2`** in `U-UNO`, ### **ma NON in `U-CASO`**: il flusso di gauge casuale localizza da sé *(ed è il rilievo del guardiano)*. ### ➜ **In quel caso il criterio di Luca si applica SOLO al braccio `U-UNO`, e lo dirò** |
| **`PM-5`** | ### ⭐ **l'orologio di de Broglie si vede**: `dφ/dt` del grumo correla con la sua energia per unità di norma, col segno giusto, entro il `30 %` |
| **`PM-6`** | la ### **vita** dei grumi è ### **lunga** *(oltre `10 t_c`)* per i `g` grandi e ### **corta** per `g = -2`: più non lineare, più stabile |

### **COSA MI FAREBBE FERMARE:** il caso `ε = 0` che ### **produce grumi** *(sarebbe un difetto
del codice: una rottura di simmetria senza causa)*; la norma o l'energia che ### **derivano**;
una corsa oltre i ### **`20` minuti**.

### ⚠ **E UNA COSA CHE QUESTO ESPERIMENTO NON PUÒ DIRE, dichiarata prima:** se i grumi nascono,
### **non** sono ancora «masse» nel senso del bersaglio — sono ### **grumi di `\|ψ\|²` che
durano**. Che si attraggano, con che legge, e se tutti cadano allo stesso modo sono
### **le tre prove di `doc/IPOTESI_gravita_a_spinta.md`**, e ### **restano fuori.**
