# LE DUE BANDE DI `W` — **il controllo `C` passa, ma SOLO in `SU(2)`**

Lo rigira:  `python primo_ordine/bande.py --scrivi`

## 1. LA CONFIGURAZIONE INTERA

| la voce | il valore |
|---|---|
| seme | `7` |
| scena | `anello di 16 nodi` |
| dtau | `0.25` |
| tick | `200` |
| eps della moneta di spin | `0.5` |
| psi iniziale | `gaussiano complesso dal seme, ampiezza ~1 per estremita'` |
| phi iniziale | `modulo |phi| = vuoto_modulo, fasi uniformi dal seme` |
| U per arco | `SU(2) casuale -- det U = 1, OBBLIGATORIO per la C` |
| il tick | `l'ORDINE INTERO di composizione.py` |
| soglia del settore 0 | `1e-09` |

## 2. ⭐ **IL CONTROLLO DELLA LETTURA** — e il suo esito dipende da `det U`

`C` e' **antilineare**, quindi se `W v = e^{-i omega} v` e `C W = W C` allora `C v`
e' autovettore con `e^{+i omega}`: ### **`omega -> -omega`, cioe' le bande si
scambiano.** ### ⛔ **Percio' il controllo e' `||C(W psi) - W(C psi)||`**, e non una
somiglianza a occhio.

| `U` | `|CW - WC|` | spettro simmetrico | `|P+C - CP-|` | |
|---|--:|--:|--:|---|
| **U(2) generico** | `4.327e+00` | `8.852e-03` | `2.175e+00` | ### ⛔ **FALLISCE** |
| **SU(2)** | `8.006e-16` | `2.220e-15` | `1.061e-14` | ### ✅ **PASSA** |

### ⛔ **ECCO IL FATTO, ED E' UNA CONDIZIONE DI FISICA:** la `C` chiede
`sigma_y U* sigma_y^-1 = U`, che vale ### **se e solo se `det U = 1`.**
### ⚠ **E `motore.Geometria` valida SOLO l'unitarieta', NON il determinante** —
quindi la tabella **permette** un trasporto che **rompe la `C`**, che e' una legge
della carta. ### **Non lo decido io: va a Luca.**

| | il numero |
|---|--:|
| dimensione dello spazio *(`4m`)* | `64` |
| banda `+` / banda `-` | `32` / `32` |
| ### ⭐ **SETTORE `0`** *(autovalori a `+-1`)* | **`0`** |
| il **peso** dello stato nel settore `0` | `0.0000` |
| i proiettori sommano all'identita' | `2.434e-15` |
| e sono idempotenti | `2.220e-16` |
| memoria della matrice | `0.062` MB |

### ⭐ **IL SETTORE `0` E' VUOTO su questa scena**, e il mandato chiedeva di
guardarlo: le bande piatte dei Grover ### **non compaiono qui**, quindi
`Q = N+ - N-` e' definita ### **senza un pezzo di stato che non ha segno.**

## 2-bis. ⭐ **LA CORREZIONE DEL 2026-10-13: LA `C` COMPLETA**

### ⛔ **LA CONCLUSIONE DEL PARAGRAFO `2` E' SBAGLIATA, e l'errore e' MIO.** Avevo scritto
che *<<la `C` chiede `det U = 1`, il trasporto deve stare in `SU(2)`>>*. ### ⚠ **La misura
era giusta, la conclusione no:** avevo applicato la `C` ### **alla sola MATERIA, su una `U`
TENUTA FISSA.** ### ⛔ **La coniugazione di carica INVERTE ANCHE IL CAMPO DI GAUGE** --
in elettrodinamica `C` manda `A` in `-A` -- e la `C` e' una simmetria della **TEORIA
INTERA**, non della materia su un campo fisso. ### ✅ **Particella e antiparticella
nello stesso campo `U(1)` NON hanno lo stesso spettro, e questa E' FISICA, non un difetto.**

La `C` completa: **`psi -> i sigma_y psi*`**, **`phi -> phi*`**, **`U -> sigma_y U* sigma_y^-1`**
*(cioe' `theta -> -theta` per la parte `U(1)`, che e' proprio cio' che la derivazione
della `U` dinamica aveva trovato)*.

| `U` | `|det U - 1|` | `|C W(U) C^-1 - W(C U)|` | spettro ribaltato | ### ⛔ **DEVE FALLIRE:** la `C` della **sola materia** |
|---|--:|--:|--:|--:|
| **U(2) generico** | `0.8243` | ### ✅ **`0.000e+00`** | `3.553e-15` | `3.799e+00` |
| **SU(2)** | `0.0000` | ### ✅ **`0.000e+00`** | `2.276e-15` | `1.343e-15` |

### ⭐ **LA `C` COMPLETA E' UNA SIMMETRIA DELLA TEORIA INTERA, ANCHE CON `U(2)` GENERICO**
*(residuo **esattamente `0`**)*, e lo spettro di `W(C U)` e' **l'opposto** di quello di `W(U)`.
### ⚠ **E IL CASO CHE DEVE FALLIRE SPIEGA COMPLETAMENTE I NUMERI DEL PARAGRAFO `2`:** la `C`
della sola materia da' **`O(1)`** con `U(2)` e **ulp** con `SU(2)` -- ### **perche' in `SU(2)`
`C U = U`, quindi li' il controllo sbagliato COINCIDE con quello giusto.**

### ✅ **QUINDI LE BANDE COME MATERIA/ANTIMATERIA SONO LETTE CORRETTAMENTE in due casi,
e lo dichiaro:** su `U` in **`SU(2)`** *(dove `C U = U`)*, oppure con la `C` **che
trasforma anche `U`**. ### ⚠ **E la scelta del parametro `su2` resta un CONTROLLO DI
MISURA, non una legge.**

### ⚠ **CHE COSA QUESTO RESIDUO NON VERIFICA:** `phi -> phi*` non entra, perche' `W` non
tocca `phi`. ### **Lo dichiaro invece di lasciar credere che sia verificato qui.**

## 3. `B1` — **LE POPOLAZIONI**

### ✅ **IL CONTROLLO:** con `N` **spento** le popolazioni devono essere
**costanti**, perche' `W` commuta coi suoi proiettori spettrali. ### ⛔ **Se non lo
fossero, i proiettori sarebbero sbagliati e tutto il resto non si leggerebbe.**

| `N` | `|phi|` | `x` max | esc. `N+` | esc. `N-` | esc. `N0` | esc. rel. `N+` |
|---|--:|--:|--:|--:|--:|--:|
| spento | `2.00` | `0.97` | `1.478e-12` | `8.598e-13` | `0.000e+00` | `2.02e-14` |
| **ACCESO** | `16.00` | `0.01516` | `2.517e-03` | `2.517e-03` | `0.000e+00` | `3.45e-05` |
| **ACCESO** | `4.00` | `0.2425` | `6.036e-01` | `6.036e-01` | `0.000e+00` | `8.27e-03` |
| **ACCESO** | `2.00` | `0.97` | `1.012e+01` | `1.012e+01` | `0.000e+00` | `1.39e-01` |
| **ACCESO** | `1.00` | `3.88` | `1.408e+01` | `1.408e+01` | `0.000e+00` | `1.93e-01` |
| **ACCESO** | `0.50` | `15.52` | `2.910e+01` | `2.910e+01` | `0.000e+00` | `3.99e-01` |

## 4. `B2` — **L'ENERGIA PER BANDA**, e le correlazioni **MISURATE**

*(`|phi| = 2`, cioe' `x = 0.97`: il regime in cui la saturazione lavora)*

| la grandezza | scala | escursione | relativa |
|---|--:|--:|--:|
| `E+` | `2.468` | `9.441e+00` | `3.83e+00` |
| `E-` | `3.073` | `9.230e+00` | `3.00e+00` |
| `E0` | `0` | `0.000e+00` | `0.00e+00` |
| `Re<psi|W psi>` | `0.6049` | `1.661e+01` | `2.75e+01` |
| il termine del **vuoto** | `1.123` | `1.100e+01` | `9.80e+00` |
| `N+` | `73.03` | `1.012e+01` | `1.39e-01` |
| `N-` | `44.95` | `1.012e+01` | `2.25e-01` |
| `Q = N+ - N-` | `28.08` | `2.024e+01` | `7.21e-01` |
| `Im<psi|W psi>` | `9.888` | `1.180e+01` | `1.19e+00` |
| `somma_k h_k` | `16.82` | `6.314e+01` | `3.75e+00` |
| `||psi||^2` | `118` | `2.416e-12` | `2.05e-14` |

### ⭐ **LE CORRELAZIONI FRA LE VARIAZIONI** — ### **misurate, non inventate:**

| fra | e | correlazione |
|---|---|--:|
| `Re<psi|W psi>` | il **vuoto** | `+0.1049` |
| `E+` | `E-` | `-0.0468` |
| `E+` | `N+` | `+0.3926` |
| `N+` | `N-` | `-1.0000` |
| `Q` | `somma_k h_k` | `+0.1881` |
| `Im<psi|W psi>` | `somma_k h_k` | `-0.1699` |
| `Im<psi|W psi>` | `Q` | `-0.9438` |

### ⛔ **FRA LE VARIAZIONI e non fra i valori:** due grandezze che derivano insieme
hanno **valori** correlati ### **anche quando le loro variazioni non c'entrano niente.**

## 5. `B3` — **LA CANDIDATA CARICA**

| la candidata | scala | escursione | relativa | |
|---|--:|--:|--:|---|
| `Q = N+ - N-` | `28.08` | `2.024e+01` | `7.21e-01` | ### ⛔ **NON conservata** |
| `Im<psi|W psi>` | `9.888` | `1.180e+01` | `1.19e+00` | ### ⛔ **NON conservata** |
| `somma_k h_k` | `16.82` | `6.314e+01` | `3.75e+00` | ### ⛔ **NON conservata** |

## 6. ⚠ IL LIMITE, DICHIARATO

### ⛔ **Tutto cio' che e' <<per banda>> e' definito GLOBALMENTE:** `P+` e `P-` sono
**proiettori spettrali**, e si ottengono **diagonalizzando `W` su tutta la scena**.
### **Trovarne una forma locale e' un passo successivo, da proporre a Luca e non da
fare qui** — e il mandato lo dice.

