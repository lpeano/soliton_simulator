# LA CORRENTE LOCALE DELL'ENERGIA **ESISTE**, ed e' COSTRUITA — portata **`3` archi**

> ### ⛔ **QUESTO REFERTO CORREGGE UNA MIA CONCLUSIONE.** In `36182b7` avevo scritto
> *<<la corrente locale non esiste nemmeno per la parte lineare>>*. ### **Era un salto:**
> cio' che avevo dimostrato e' che **la MIA CANDIDATA** *(<<cio' che lo spostamento
> porta>>)* **fallisce**. ### ✅ **L'esistenza e' un'altra cosa, ed e' VERA.**

> ### ⭐ **E LA NON UNICITA' NON E' UN DIFETTO:** e' la stessa liberta' della corrente
> d'energia nel continuo, definita **a meno di un rotore**. ### **Una corrente e' fisicamente
> locale se e' funzione LOCALE dello stato e CHIUDE la continuita': l'unicita' non serve.**

Lo rigira:  `python primo_ordine/corrente.py --scrivi`

## 1. LA CONFIGURAZIONE INTERA

| la voce | il valore |
|---|---|
| seme | `4` |
| dtau | `0.2` |
| eps della moneta di spin | `0.5` |
| sommatoria | `numpy` |
| psi iniziale | `gaussiano complesso dal seme, NON normalizzato` |
| phi iniziale | `modulo 1, fasi uniformi dal seme` |
| versori n per estremita' | `gaussiani dal seme, normalizzati a 1` |
| U per arco | `U(2) casuale via QR, COMPAGNA = coniugata trasposta` |
| il tick misurato | `W = moneta_spin -> grover -> spostamento_trasporto` |
| il flusso N | `SPENTO -- questa e' la PARTE LINEARE` |
| tol dell'instradamento | `1e-14` |
| scossa del termine di bordo | `0.7` |
| piattaforma | `Windows`, python `3.13.2`, numpy `2.3.0` |

## 2. `(a)` IL TERMINE DI BORDO — *l'argomento, sul mio simulatore*

Anello di `40` nodi, `R` = i nodi `0..19`. ### **`somma_R Delta e` di base: `2.341102084070`.**

| la perturbazione | `|somma_R Delta e| cambia` | il verdetto |
|---|---|---|
| **DENTRO `R`**, a distanza `>= 2` dal bordo | **`2.665e-15`** | ### ✅ **invariante entro ulp** |
| **AL BORDO** di `R` *(controllo positivo)* | **`7.144e-01`** | ### ⭐ **`O(1)`: la perturbazione ARRIVA** |

### ⚠ **E `Delta e` NODO PER NODO CAMBIA FINO A `6.183`:** non e' che la perturbazione
non faccia niente — ### **cambia tutto tranne la somma sulla regione.**

## 3. `(b)` LA COSTRUZIONE, E LA PORTATA **MISURATA**

| scena | `n` | `m` | grado | `D` | `somma_k Q_k` | la forma su `x` | **PORTATA** | supporto | diametro | continuita' | verso invertito |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `anello-10` | 10 | 10 | 2 | 80 | `3.9e-16` | `8.9e-15` | **`1`** | 2 | 5 | `2.9` ulp | `1.71e+01` |
| `toro2d-3x3` | 9 | 18 | 4 | 144 | `1.5e-16` | `1.1e-14` | **`2`** | 7 | 2 | `35.3` ulp | `1.89e+01` |
| `toro2d-4x4` | 16 | 32 | 4 | 256 | `1.7e-16` | `1.2e-14` | **`3`** | 8 | 4 | `25.2` ulp | `1.86e+01` |
| `toro2d-4x6` | 24 | 48 | 4 | 384 | `1.7e-16` | `5.6e-15` | **`3`** | 8 | 5 | `26.4` ulp | `2.81e+01` |
| `toro2d-6x6` | 36 | 72 | 4 | 576 | `1.8e-16` | `8.9e-15` | **`3`** | 8 | 6 | `16.9` ulp | `2.53e+01` |
| `toro3d-3x3x3` | 27 | 81 | 6 | 648 | `2.4e-16` | `1.2e-14` | **`3`** | 11 | 3 | `70.4` ulp | `2.36e+01` |

### ⭐ **LA PORTATA E' `3` ARCHI, E NON CRESCE COL GRAFO:** a grado `4`, i diametri
`4`, `5` e `6` danno ### **tutti `3`**, e il supporto massimo resta ### **`8` nodi.**
### ⚠ **E IL `3x3` MOSTRA IL TAGLIO, non una crescita:** ha diametro `2`, e la' la portata
vale `2` ### **perche' il GRAFO la taglia** — non perche' la portata sia `2`.
### ⛔ **Sull'anello vale `1`:** a grado `2` il supporto di una coppia e' **`2` nodi**.

## 4. CHE COSA RESTA VERO DI `36182b7`, E CHE COSA CADE

| | che cosa |
|---|---|
| ✅ **resta vero** | la candidata *<<cio' che lo spostamento porta>>* **non chiude** il bilancio |
| ✅ **resta vero** | `e_h` e' una **correlazione fra due tempi**, non una carica a un tempo |
| ⛔ **CADE** | *<<la corrente locale non esiste nemmeno per la parte lineare>>* |
| ⛔ **RITIRATA** | la raccomandazione di **cambiare la grandezza promossa**: non era motivata |

### ⚠ **E il secondo fatto NON implica il terzo:** che `e_h` sia una correlazione fra due
tempi e' vero, ma ### **non impedisce la localita'.**

## 5. IL LIMITE DICHIARATO: **IL COSTO**

### ⛔ **Questa e' una costruzione PER LA PROVA, non per il percorso caldo.** Estrarre
`Q` costa **`O(D^2)` valutazioni** con `D = 8m`, e l'instradamento **`O(D^2)` cammini**.
### **Su una scena piccola e' una misura; su una scena grande non si fa**, e va detto
invece di scoprirlo. ### ✅ **Cio' che la misura stabilisce e' L'ESISTENZA e LA PORTATA**,
non un algoritmo da far girare a ogni tick.

