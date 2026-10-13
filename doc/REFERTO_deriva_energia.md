# LA DERIVA DI `E` SUL TICK INTERO — **il `4.20` non si riproduce, e il perche' e' STRUTTURALE**

> ### ⛔ **IL NUMERO VECCHIO ERA ORFANO** *(`L-NUMERI-DERIVA-ORFANA`)*: nessuno script lo
> produceva. ### **Questo referto lo sostituisce con numeri che escono da un comando.**

Lo rigira:  `python primo_ordine/deriva.py --scrivi`

## 1. LA CONFIGURAZIONE INTERA

| la voce | il valore |
|---|---|
| seme | `7` |
| eps della moneta di spin | `0.5` |
| sommatoria | `numpy` |
| psi iniziale | `gaussiano complesso dal seme, NORMALIZZATO a 1` |
| phi iniziale | `modulo 1, fasi uniformi dal seme` |
| versori n per estremita' | `gaussiani dal seme, normalizzati a 1` |
| U per arco | `U(2) casuale via QR, COMPAGNA = coniugata trasposta` |
| il tick | `l'ORDINE INTERO di composizione.py, 7 applicazioni` |
| il flusso N | `ACCESO, in due mezzi (Strang)` |
| piattaforma | `Windows`, python `3.13.2`, numpy `2.3.0` |

## 2. `D-ENERGIA:M0` — la deriva a **tempo totale fisso** `T = 2.0`, nei **DUE REGIMI**

### ⛔ **E IL REGIME NON E' UN DETTAGLIO:** con `||psi|| = 1` su tutto il grafo si ha
`h_k/Lambda_k ~ 1/(2m)`, e `G(x) = x - arctan x` va come `x^3/3` — ### **la saturazione e'
praticamente SPENTA, e misurare la sua sorgente la' sarebbe un FALSO-ZERO.**

### ✅ **regime `locale`:** `primo = 5.9100e-01`, `vuoto = 5.6930e+00`, ### **`max|h/Lambda| = 3.8799`**

| `dtau` | tick | `|Delta E|` | `|Delta` primo`|` | `|Delta` vuoto`|` |
|---|--:|--:|--:|--:|
| `0.20000` | 10 | `3.171458e+00` | `2.329e+00` | `8.423075e-01` |
| `0.10000` | 20 | `1.253841e+01` | `1.741e-01` | `1.236432e+01` |
| `0.05000` | 40 | `8.340958e+00` | `4.407e-02` | `8.296891e+00` |
| `0.02500` | 80 | `1.554518e+00` | `1.539e+00` | `3.093343e+00` |
| `0.01250` | 160 | `1.911865e+00` | `1.510e+00` | `4.019356e-01` |

| i rapporti fra dimezzamenti, su | |
|---|---|
| `|Delta E|` | `0.253`  `1.503`  `5.366`  `0.813` |
| il **primo** termine | `13.379`  `3.951`  `0.029`  `1.019` |
| il termine del **vuoto** | `0.068`  `1.490`  `2.682`  `7.696` |

### ⭐ **`4` sarebbe l'esponente `2`; `1` vuol dire CHE NON SCENDE.**

### ⛔ **regime `globale`:** `primo = 5.0096e-03`, `vuoto = 1.6108e-05`, ### **`max|h/Lambda| = 0.0329`**

| `dtau` | tick | `|Delta E|` | `|Delta` primo`|` | `|Delta` vuoto`|` |
|---|--:|--:|--:|--:|
| `0.20000` | 10 | `4.748057e-05` | `2.134e-05` | `2.613844e-05` |
| `0.10000` | 20 | `2.635960e-05` | `5.550e-06` | `2.080975e-05` |
| `0.05000` | 40 | `6.582676e-05` | `2.734e-05` | `3.848529e-05` |
| `0.02500` | 80 | `2.142632e-05` | `1.484e-05` | `6.590740e-06` |
| `0.01250` | 160 | `3.571108e-05` | `1.628e-05` | `1.943283e-05` |

| i rapporti fra dimezzamenti, su | |
|---|---|
| `|Delta E|` | `1.801`  `0.400`  `3.072`  `0.600` |
| il **primo** termine | `3.846`  `0.203`  `1.843`  `0.911` |
| il termine del **vuoto** | `1.256`  `0.541`  `5.839`  `0.339` |

### ⭐ **`4` sarebbe l'esponente `2`; `1` vuol dire CHE NON SCENDE.**


## 3. `D-ENERGIA:M0-bis` e `D-ENERGIA:M0-ter` — **DOVE** sta la deriva

*(regime `locale`, quello in cui la saturazione e' accesa)*

| il termine | `max |Delta|` | la sua SCALA | relativo |
|---|--:|--:|--:|
| il **primo**, `Re<psi\|W psi>` | `2.3292e+00` | `5.9100e-01` | `3.94e+00` |
| il **vuoto**, `somma_k Lambda_k G(h_k/Lambda_k)` | `1.2364e+01` | `5.6930e+00` | `2.17e+00` |

## 4. `D-ENERGIA:M1a` — il **run lungo**: `20000` tick

| la grandezza | il valore |
|---|--:|
| `E(0)` | `5.856899` |
| `max|h/Lambda|` all'inizio | `3.8799` |
| la **pendenza** della retta adattata | `-1.502e-05` per tick |
| l'**ampiezza** dei residui | `7.608e+01` |
| il **rapporto** *(spiegata dalla retta / ampiezza)* | **`0.004`** |
| `E(t) - E(0)` sta fra | `-45.279796` e `30.832277` |

### ⭐ **IL CRITERIO, fissato PRIMA:** `rapporto >> 1` = **SECOLARE**, `rapporto << 1` = **OSCILLANTE**.

## 5. `D-ENERGIA:M1b` — **tre taglie**, fattore `4` fra gli estremi

### ⚠ **A STATO LOCALE UGUALE** *(regime `locale`)*: con la normalizzazione globale
le tre taglie ### **non avrebbero lo stesso stato locale**, e il confronto non direbbe
niente sull'estensivita'.

| `n` | `E(0)` | **escursione** di `E` su `200` tick | **per nodo** |
|--:|--:|--:|--:|
| 8 | `2.4693` | `2.633582e+01` | `3.291977e+00` |
| 16 | `5.8569` | `4.632517e+01` | `2.895323e+00` |
| 32 | `-22.4834` | `7.917428e+01` | `2.474196e+00` |

## 6. `D-ENERGIA:M1c` — per **lunghezza d'onda**, `n = 32`

| lo stato iniziale | `max|h/Lambda|` | **escursione** di `E` su `200` tick |
|---|--:|--:|
| CASUALE (il piu' ruvido) | `5.3969` | `7.917428e+01` |
| periodo 2 nodi | `1.0133` | `1.089401e+01` |
| periodo 4 nodi | `1.0133` | `4.914975e+00` |
| periodo 8 nodi | `1.0133` | `7.928537e+00` |
| periodo 32 nodi (il piu' liscio) | `1.0133` | `1.015950e+01` |

## 7. **LA SCANSIONE IN `x = |h_k|/Lambda_k`** — dal regime **vacuo** a quello che **lavora**

> **Mandato della verifica esterna, 2026-10-13:** *<<Un `M0` nel regime `x ~ 1e-3` e'
> VACUO: non distingue "`E` conservata" da "il termine non c'e'".>>*

### ⭐ **E' LO STESSO DIFETTO CHE AVEVO TROVATO MISURANDO**, un'ora prima che il mandato
arrivasse: col `psi` normalizzato su tutto il grafo `x ~ 1/(2m)`, e `G(x) = x - arctan x`
va come `x^3/3` — ### **il termine del vuoto valeva `~1e-5`: la saturazione era SPENTA.**

### ⚠ **`x` SI SCANSIONA COL MODULO DEL VUOTO**, e non e' una costante nuova:
`Lambda_k = somma |phi_h|^2`, quindi `x` scala come `1/|phi|^2`. ### **Un vuoto piu' debole
porta `x` verso `1`, cioe' ACCENDE la saturazione.**

| `|phi|` | `x` max | `x` medio | scala **primo** | scala **vuoto** | esc. **primo** | esc. **vuoto** | esc. **SOMMA** | esc./scala NATURALE: primo | vuoto | **SOMMA** |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| `16.00` | `0.01516` | `0.005176` | `0.04965` | `0.0004038` | `1.175e-02` | `6.078e-03` | **`1.641e-02`** | `9.96e-05` | `4.71e-07` | **`1.26e-06`** |
| `8.00` | `0.06062` | `0.0207` | `0.04965` | `0.006447` | `1.849e-01` | `9.737e-02` | **`2.594e-01`** | `1.57e-03` | `2.99e-05` | **`7.68e-05`** |
| `4.00` | `0.2425` | `0.08282` | `0.04965` | `0.09989` | `2.167e+00` | `1.507e+00` | **`3.223e+00`** | `1.84e-02` | `1.78e-03` | **`3.34e-03`** |
| `2.00` | `0.97` | `0.3313` | `0.04965` | `1.123` | `1.551e+01` | `1.120e+01` | **`2.084e+01`** | `1.31e-01` | `4.60e-02` | **`5.77e-02`** |
| `1.00` | `3.88` | `1.325` | `0.04965` | `5.693` | `3.802e+01` | `3.760e+01` | **`5.840e+01`** | `3.22e-01` | `4.06e-01` | **`2.77e-01`** |
| `0.50` | `15.52` | `5.3` | `0.04965` | `12.09` | `2.889e+01` | `5.872e+01` | **`7.260e+01`** | `2.45e-01` | `1.07e+00` | **`4.20e-01`** |
| `0.25` | `62.08` | `21.2` | `0.04965` | `15.37` | `2.060e+01` | `6.907e+01` | **`7.200e+01`** | `1.75e-01` | `1.52e+00` | **`4.40e-01`** |

### ⛔ **LA CONDIZIONE DI STOP DEL MANDATO**, sul punto con `x` piu' vicino a `1` *(`x = 0.97`)*:

| | il numero |
|---|--:|
| escursione della **SOMMA** | `2.084e+01` |
| la **maggiore** dei due termini | `1.551e+01` |
| ### ⛔ **il verdetto** | ### **LA SOMMA NON SI CONSERVA: VA A LUCA** |

## 8. `(c)` — **LA SORGENTE PER NODO**, con `N` acceso

`s_k = Delta E_k - (div J)_k`, con `J` la corrente locale **costruita** per il pezzo
lineare, valutata sullo stato che **entra** nel pezzo lineare *(dopo il primo mezzo
flusso)*.

### ⛔ **E SI DECOMPONE, perche' il residuo MESCOLA DUE COSE:** il mio `J` copre il
pezzo lineare **dello spinore**, e la **camminata del vuoto** muove `phi` fra i nodi,
cioe' ### **trasferisce energia di vuoto senza che io la modelli.** ### ⚠ **Quello e' una
CORRENTE CHE MANCA, non una sorgente** — e chiamarlo sorgente sarebbe attribuire al
fenomeno un buco del mio strumento. ### **Lo stesso errore della candidata di ieri.**

### ⛔ **MA LA DECOMPOSIZIONE E' VACUA PER QUESTO VUOTO, e si PROVA invece di dedurlo:**

| `|phi|` | `max_k |Delta Lambda_k|` sotto la **sola** camminata del vuoto | |
|---|--:|---|
| **uniforme** *(il vuoto del banco)* | `4.441e-16` | ### ⛔ **ESATTAMENTE invariante** |
| **non uniforme** *(controllo positivo)* | `2.164e+00` | ### ✅ **cambia: la misura SA vedere** |

### ⭐ **E IL PERCHE' E' STRUTTURALE:** su un grafo **`2`-regolare** il Grover scalare e'
`(2/2)(phi_a + phi_b) - phi_h`, cioe' **uno SCAMBIO**, e lo spostamento e' una
**permutazione**: con `|phi|` uniforme permutano **moduli tutti uguali**, quindi
### **`Lambda_k` non cambia e la camminata del vuoto NON PORTA ENERGIA DI VUOTO.**
### ⚠ **Percio' le due righe qui sotto coincidono A TUTTE LE CIFRE**, e non e' un errore:
### **e' che qui non c'e' niente da decomporre.** ### ⛔ **Su un grafo di grado `> 2`
la decomposizione tornerebbe a dire qualcosa, e NON l'ho misurata.**

### ✅ **SENZA la camminata del vuoto (la sorgente VERA di `N`)**

| `dtau` | `max_k |s_k|` | `somma_k s_k` | `max_k |Delta E_k|` | `s/Delta E` | rapporto col precedente |
|---|--:|--:|--:|--:|--:|
| `0.20000` | `4.104323e+00` | `+1.953e+00` | `9.181e+00` | `4.47e-01` | `--` |
| `0.10000` | `4.099264e+00` | `+2.977e+00` | `8.856e+00` | `4.63e-01` | `1.001` |
| `0.05000` | `4.166298e+00` | `+3.397e+00` | `8.658e+00` | `4.81e-01` | `0.984` |
| `0.02500` | `4.194306e+00` | `+3.570e+00` | `8.558e+00` | `4.90e-01` | `0.993` |

### ⭐ **`4` sarebbe `O(dtau^2)`; `1` vuol dire `O(1)`, cioe' CHE NON SCENDE.**

### ⚠ **col tick INTERO (sorgente + corrente del vuoto che manca)**

| `dtau` | `max_k |s_k|` | `somma_k s_k` | `max_k |Delta E_k|` | `s/Delta E` | rapporto col precedente |
|---|--:|--:|--:|--:|--:|
| `0.20000` | `4.104323e+00` | `+1.953e+00` | `9.181e+00` | `4.47e-01` | `--` |
| `0.10000` | `4.099264e+00` | `+2.977e+00` | `8.856e+00` | `4.63e-01` | `1.001` |
| `0.05000` | `4.166298e+00` | `+3.397e+00` | `8.658e+00` | `4.81e-01` | `0.984` |
| `0.02500` | `4.194306e+00` | `+3.570e+00` | `8.558e+00` | `4.90e-01` | `0.993` |

### ⭐ **`4` sarebbe `O(dtau^2)`; `1` vuol dire `O(1)`, cioe' CHE NON SCENDE.**


