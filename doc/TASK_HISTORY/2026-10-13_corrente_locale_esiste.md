# LA CORRENTE LOCALE **ESISTE** — la mia conclusione di `36182b7` era troppo larga

> **Mandato di Luca, 2026-10-13, punto `1`:** *«`36182b7` conclude "la corrente locale non
> esiste nemmeno per la parte lineare". Cio' che hai dimostrato e' piu' stretto: **NON
> FUNZIONA LA TUA CANDIDATA** a un arco. L'esistenza di una corrente LOCALE e' un'altra
> cosa, ed e' **VERA** per la parte lineare.»*

> ### ✅ **Questo file si committa PRIMA del codice.**

---

## 1. L'ERRORE CHE HO FATTO, detto con precisione

### ⛔ **Ho inferito <<non esiste>> da <<la mia costruzione non funziona>>.** E' un salto
che non si fa: ### **fallisce la candidata, non l'esistenza.**

| | che cosa avevo misurato | che cosa avevo concluso |
|---|---|---|
| ✅ **vero** | la corrente *«cio' che lo spostamento porta»* da' residuo **`1.342e+01`** su scala `4.93` -- **peggio che senza corrente** | — |
| ✅ **vero** | `e_h` e' una **correlazione fra due tempi** *(`psi` e `W psi`)*, non una carica a un tempo | — |
| ### ⛔ **FALSO** | — | *«la corrente locale non esiste nemmeno per la parte lineare»* |

### ⚠ **E il secondo fatto NON implica il terzo**, e il mandato lo dice: che `e_h` sia una
correlazione fra due tempi **e' vero**, ma ### **non impedisce la localita'.**

---

## 2. L'ARGOMENTO CHE DIMOSTRA L'ESISTENZA — *e non e' mio*

> **`Delta e_k` e' una forma quadratica in `psi` con supporto in un INTORNO di `k`**
> *(al massimo `2` archi: `e` usa `W`, e `Delta e` usa `W` due volte)*. ### **La somma su
> tutti i nodi e' identicamente zero.**
>
> ### ⭐ **Quindi per ogni regione `R`:**
>
> **`somma_R Delta e_k = - somma_{fuori da R} Delta e_k`**
>
> La prima dipende **solo da `psi` vicino a `R`**, la seconda **solo da `psi` vicino al
> complemento** ⟹ ### **dipende SOLO DA `psi` VICINO AL BORDO di `R`.**
>
> ### ✅ **La variazione d'energia di una regione e' un TERMINE DI BORDO**, e una corrente
> locale **di portata finita esiste** — per esempio **instradando ogni termine della forma
> quadratica lungo cammini di lunghezza limitata.**

### ⭐ **E LA PROVA NUMERICA C'E' GIA', fatta indipendentemente dal mio codice:** reticolo
cubico periodico `L = 12`, monete di spin `SU(2)` casuali per nodo, Grover, `U(2)` casuali
per arco, `R` = lo strato `x in [0, 6)`. ### **Perturbando `psi` a distanza `>= 2` dal
bordo, `Delta e` cambia fino a `22` per nodo, ma `somma_R Delta e` cambia di `1e-14`.**
Perturbando **a ridosso del bordo** cambia di `O(1)`.

### ⛔ **E LA NON UNICITA' NON E' UN DIFETTO**, e qui avevo sbagliato una seconda volta:
e' ### **la stessa liberta' della corrente d'energia nel continuo**, definita **a meno di
un rotore**. ### ✅ **Una corrente e' fisicamente locale se e' funzione LOCALE dello stato
e chiude la continuita'. L'UNICITA' NON SERVE.**

### ⚠ **E questo ritira anche la mia raccomandazione:** avevo raccomandato di **cambiare la
grandezza promossa** *(una densita' funzione dello stato a un tempo)*. ### **Non e'
motivata, e il mandato me la fa ritirare.** ### **La ritiro.**

---

## 3. PROGETTAZIONE — *i quattro passi, e le previsioni PRIMA dei numeri*

### ⚠ **E LE PREVISIONI NON SONO NEUTRE, e lo dico:** l'argomento del mandato e'
**corretto** e la sua prova numerica e' **gia' fatta**. ### **Quindi mi aspetto che le
misure confermino, e scriverle come se fossi in dubbio sarebbe una finta.**
### ⭐ **Cio' che resta DAVVERO aperto e' la PORTATA della corrente che costruisco**, e
quella **non la so.**

| | il passo | la previsione, scritta PRIMA |
|---|---|---|
| `a` | **il TERMINE DI BORDO sul mio simulatore**: perturbo `psi` **dentro** `R` lontano dal bordo ⟹ `somma_R Delta e` **invariata** | ### **invariata entro ulp**; e col **controllo positivo** *(perturbazione **al bordo**)* ### **cambia di `O(1)`** |
| `b` | **COSTRUISCO la corrente locale** e verifico la continuita' **nodo per nodo** | ### **chiude entro ulp.** ### ⚠ **E la PORTATA non la so**: dall'argomento mi aspetto `<= 4` archi, ma **e' una stima e va MISURATA** |
| `c` | **con `N` acceso**: il bilancio ha una **SORGENTE** di ordine `dtau^2` | ### **la misuro per nodo**, e mi aspetto che **scali come `dtau^2`** -- coerente col rapporto `4.20` gia' misurato |
| `d` | **annoto** il task history *(non lo riscrivo)*, **correggo** la voce, **ritiro** la raccomandazione | — |

### ⛔ **CHE COSA MI FAREBBE FERMARE**

1. se `(a)` **fallisse** sul mio simulatore mentre la prova indipendente passa, allora
   ### **il difetto e' nel MIO `e_h`**, non nell'argomento — e si cerca la' *(per esempio
   `W` applicato con parametri diversi fra le due chiamate)*.
2. se `(b)` **non chiudesse entro ulp**, la mia **costruzione** e' sbagliata di nuovo —
   ### **e questa volta NON concludo che l'esistenza e' falsa.** ### **E' la lezione.**
3. se la **portata** venisse grande *(confrontabile col diametro del grafo)*, la corrente
   ### **non e' locale in senso utile**, e quello **va detto come limite della
   COSTRUZIONE**, non dell'esistenza.

---

## 4. COME COSTRUISCO LA CORRENTE — *e perche' per forma quadratica e non per intuizione*

### ⛔ **La mia prima candidata era un'INTUIZIONE** *(«cio' che lo spostamento porta»)*, e
l'intuizione **era sbagliata** perche' `e_h` non e' una carica trasportata.
### ✅ **Quindi questa volta si costruisce DALLA FORMA QUADRATICA, come il mandato
suggerisce:**

1. `Delta e_k` e' **una forma quadratica reale** in `x = (Re psi, Im psi)`: si estrae
   **la sua matrice `Q_k`** valutandola sulla base *(esatto, perche' e' quadratica)*.
2. ### ⭐ **`somma_k Q_k = 0` ESATTAMENTE, e questa e' la chiave:** vale **per ogni `psi`**,
   quindi **coefficiente per coefficiente**. ### **Allora per OGNI coppia `(i, j)` di
   componenti, i numeri `{(Q_k)_{ij}}_k` SOMMANO A ZERO.**
3. per ogni coppia, quei numeri vivono su **un insieme BOUNDED di nodi** *(il supporto)*:
   si **instradano** da un nodo di riferimento lungo **cammini piu' corti dentro quel
   supporto**, e la somma zero garantisce che **al riferimento non resti niente**.
4. la somma di tutti gli instradamenti e' **`J` sugli archi**, e la continuita' chiude
   **per costruzione**. ### ⚠ **E la PORTATA e' la lunghezza massima dei cammini usati:
   si MISURA, non si dichiara.**

### ⭐ **E IL CONTROLLO CHE DEVE FALLIRE resta quello del mandato precedente:** una
corrente **col verso di un arco invertito** ### **deve rompere la continuita'** -- e si
prova **sulla corrente VERA**, non su una costruita.

---

## 5. LA STELLA POLARE

| | la domanda | la risposta |
|--:|---|---|
| **1** | conserva **localmente**? | ### ✅ **SI', per la parte lineare, e questa e' la CORREZIONE del pezzo:** la continuita' chiude **nodo per nodo** con una corrente **locale**. ### ⚠ **Con `N` c'e' una SORGENTE `O(dtau^2)`**, che **si misura e si dichiara** |
| **2** | **quale gradino**? | ### **(a) robusto al rumore numerico**: il bilancio chiude **entro ulp**. ### ⛔ **Non piu' in su: non ho tolto nessuna legge pratica** |
| **3** | **aggiunge un numero o una legge**? | ### ✅ **Nessuno dei due.** `J` e' **un osservatore**, non una legge; e la costruzione **non porta costanti** |
| **4** | tocca `rho`, `c_s` o **il SEGNO**? | ### ⚠ **Il SEGNO si':** `J` ha un **verso**, e il controllo che deve fallire e' **proprio il verso invertito** |
| **5** | **emergente o imposto**? | ### ⭐ **L'ESISTENZA e' emergente** *(viene dall'identita' e dalla localita' di `W`)*; ### **la SCELTA della corrente e' imposta, ed e' la liberta' di ricircolo** -- che ### **NON e' un difetto**, e' la stessa del continuo |

---

## 6. TODO DEL NEXT STEP

1. `(a)` il **termine di bordo**, coi due versi.
2. `(b)` la **costruzione** e la continuita' **entro ulp**, con la **portata MISURATA**.
3. `(c)` la **sorgente `O(dtau^2)`** con `N`, per nodo.
4. `(d)` **annotazione**, **correzione della voce**, **ritiro della raccomandazione**.
