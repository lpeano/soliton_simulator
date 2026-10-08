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
