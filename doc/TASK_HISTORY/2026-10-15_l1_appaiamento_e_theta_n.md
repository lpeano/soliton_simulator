# `L1` — TERZA PARTE: **l'appaiamento misurato bene, e `Theta` contro le direzioni `n`**

> **Mandato di Luca del 2026-10-15, terza parte.** Ultimo commit verificato dal guardiano:
> `f46d854`. ### ⛔ **MISURE, NESSUNA DECISIONE DI FISICA.**
>
> ### **E si scrive prima del codice**, come il paragrafo 8 pretende.

---

## 0. ⛔ **UN TERZO ERRORE MIO, E QUESTA VOLTA E' UNA MISURA SBAGLIATA**

### ⚠ **`accoppia` era un accoppiamento GOLOSO**, e un goloso ### **accoppia per forza gli
ultimi rimasti, anche se lontanissimi**: il numero che ne esce **non e' la distanza fra i
due multinsiemi**, e' **la distanza del peggior residuo di una scelta miope.**

### 📌 **Il guardiano ha rifatto il conto sulla stessa scena** *(`72` autovalori)*:

| `dtau` | goloso *(mio)* | **ottimo** | spaziatura media |
|---|---|---|---|
| `1` | `1.99` | **`0.082`** | `0.088` |
| `0.5` | `2.00` | **`1.40`** | `0.088` |
| `0.25` | `1.94` | **`2.00`** | `0.024` |

### ⛔⛔ **E GUARDA LA PRIMA RIGA: `0.082` CONTRO UNA SPAZIATURA DI `0.088`.** Cioe' a
`dtau = 1` ### **lo spettro E' appaiato entro la spaziatura dei livelli**, e io avevo
scritto *«distanza `~2`, cioe' il diametro del cerchio: NON appaiato»*.
### **Il mio numero non era impreciso: diceva il contrario del vero.**

### ⚠ **E avevo scritto il goloso DOPO aver curato un altro difetto della stessa misura**
*(il raggruppamento per angolo invece che per autovalore)*: ### **ho curato
l'avvolgimento e ho lasciato in piedi un errore piu' grosso.**

### ⭐ **E LA LEZIONE, che vale piu' del numero: un accoppiamento fra multinsiemi E' UN
PROBLEMA DI OTTIMIZZAZIONE**, e il goloso non lo risolve. ### **E senza la SPAZIATURA DEI
LIVELLI accanto, una distanza fra spettri non si puo' leggere:** `0.082` e' *«appaiato»* o
*«no»* ### **solo rispetto a qualcosa.**

---

## 1. RAGIONAMENTO PRELIMINARE

### ⭐ **PUNTO 2: L'IDENTITA' CHE IL GUARDIANO PROPONE SI DERIVA, e la scrivo prima**

### **`Theta: psi -> i sigma_y psi^*` e' l'inversione del tempo dello spin `1/2`**
*(`Theta^2 = -1`, da cui Kramers)*. Per i pezzi:

```
Theta exp(-i a sigma.n) Theta^-1 = exp(-i a sigma.n)        <- MISURATO: 0.000e+00
   ma la STESSA riga, letta su -n:
Theta exp(-i a sigma.(-n)) Theta^-1 = exp(+i a sigma.n) = [moneta con n]^-1
```

### ⭐⭐ **Cioe': la moneta con `n` va nell'INVERSA della moneta con `-n`.** E gli altri
pezzi vanno nel loro inverso *(misurato, `16`/`16`)*, e **il palindromo rimette l'ordine**
*(misurato: pendenza `2.006` contro `1.183`)*. ### ✅ **Quindi, per OGNI `n`:**

> ### **`Theta · W[n] · Theta^-1 = W[-n]^-1`**

### 📌 **E questo spiega perche' la mia misura di stamattina trovava `6.68e-01`:** stavo
confrontando `Theta W[n] Theta^-1` con ### **`W[n]^-1`**, cioe' con il `-n` **mancante**.
### ⚠ **Non era un difetto del modello: era il confronto sbagliato.**

### ⛔ **COSA NON SO, e lo scrivo per non chiamarlo <<previsto>> dopo**

1. **se `(a)` vale all'ulp.** La derivazione dice si'; ### **ma la stessa derivazione mi
   aveva fatto scrivere <<per ogni pezzo>> dimenticando la moneta**, quindi
   ### **la misura decide, non il conto.**
2. **se esiste la mappa del reticolo di `(c)`.** L'inversione spaziale del toro manda
   l'arco `v -> v+e_d` nell'arco `-v-e_d -> -v` **percorso all'indietro**, quindi
   ### **rovescia l'orientamento**: e con un'orientamento rovesciato ### **`U` va in
   `U^dagger`.** ### ⚠ **Allora con `U` CASUALE la mappa NON PUO' essere una simmetria**
   *(servirebbe `U^dagger = U` per ogni arco)*, e la domanda ha senso ### **solo con `U = I`
   o con una `U` scelta simmetrica.** ### **Lo misuro con `U = I`, e lo DICHIARO.**
3. **se gli `n` geometrici esistono da qualche parte.** ### **CENSITO DAL CODICE, e la
   risposta e' NO:**

| come si costruiscono gli `n` | dove |
|---|---|
| **casuali gaussiani, normalizzati per estremita'** | `deriva.scena`, `corrente._scena`, `_collauda_checkpoint`, `_collauda_energia`, `_collauda_saturazione`, `bande_floquet.scena_toro`, `_misura_spettro_l1.scena` |
| **`z` uniforme** *(`nv[:,2] = 1`)* | `_collauda_memoria`, `_collauda_motore` — e la' e' **dichiarato come banco di CONTROLLO**, non come fisica |
| ### ⛔ **GEOMETRICI** *(dalla direzione dell'arco)* | ### **NESSUNA SCENA.** Li costruisco io, nello script nuovo |

---

## 2. PROGETTAZIONE — *i passi, cosa decide ciascuno, cosa mi FERMA*

| | il passo | **che cosa decide** | **cosa mi FERMA** |
|---|---|---|---|
| `1` | **`accoppia` → OTTIMO** *(`scipy.optimize.linear_sum_assignment`)*, **piu' Hausdorff**, **piu' la spaziatura** | se la misura dell'appaiamento dice qualcosa | `scipy` assente → si riscriverebbe un assegnamento a mano, e **non e' il caso**: `scipy 1.17.1` c'e' |
| `2` | **un caso che DEVE passare** *(uno spettro appaiato PER COSTRUZIONE)* e **uno che DEVE fallire** | che il numero nuovo **non sia un altro artefatto** | il caso che deve passare **che non passa** → la misura e' ancora rotta |
| `3` | **il referto nuovo ACCANTO al vecchio** *(nessuna sovrascrittura)*, e **il `~2` corretto** nella `RIPRESA` e nella voce | che il numero sbagliato **non resti in giro** | — |
| `4` | **`_misura_theta_n.py`**, script NUOVO: `(a)` l'identita', `(b)` il caso che deve fallire, `(c)` gli `n` geometrici e la mappa del reticolo | la fisica di `Theta` *(che **non decido**)* | `(a)` che non vale all'ulp → **FERMO e riporto**: la derivazione sarebbe smentita |
| `5` | **il braccio dei ripieghi** misura la **PROPRIETA'** *(allocazioni nuove dopo il primo tick `= 0`)*, **senza alzare il `13`** | che un braccio misuri **cio' che dichiara** | — |
| `6` | **la prova del braccio**: un'allocazione al tick `5` **deve** farlo fallire | che il braccio nuovo **impedisca** *(`A9`)* | non fallisce → e' **una tenda** |

### ⛔ **E UNA COSA CHE NON FACCIO:** `_misura_theta_n.py` e' **un file suo** e non entra in
`_misura_spettro_l1.py`. ### **Non e' per la lunghezza** *(`365` righe su `700`)*: e'
perche' ### **sono due domande diverse** — una e' *«che forma ha lo spettro»*, l'altra
*«quale trasformazione e' una simmetria»*, e `P-MOD` dice che un modulo che non si descrive
in una riga **ne fa due.**

---

## 3. LA STELLA POLARE — **cinque risposte, e questo commit NON cambia una legge**

| | la risposta |
|---|---|
| **1. `A14`, conserva localmente?** | ### **Non si applica alla FISICA, e il motivo e' che nessuna legge cambia:** qui si cambiano **due misure e un braccio di collaudo**. ### ⭐ **E vale la pena dirlo al rovescio:** la misura di `Theta` **guarda** una conservazione *(quella della struttura sotto inversione del tempo)*, e non ne introduce nessuna. |
| **2. a quale GRADINO arriva?** | **`(a)`, robusto al rumore numerico**, e per `(a)` del punto 2 **all'ulp**. ### ⛔ **NON `(c)`**, e la cosa va detta forte: `Theta^2 = -1` e Kramers sono **la teoria standard dello spin `1/2`**, ma ### **che QUESTO passo sia una teoria di spin `1/2` e' cio' che non e' dimostrato.** |
| **3. aggiunge un numero o una legge?** | ### ✅ **NIENTE.** `0` leggi, `0` parametri. ### ⚠ **E una SOGLIA NON SI ALZA:** il `13` dei ripieghi **resta `13`** — si cambia **cio' che il braccio MISURA**, non il suo tetto. ### 📌 **E le tolleranze nuove sono DERIVATE o DICHIARATE:** `1024 eps` per l'ulp, e **la spaziatura dei livelli** come metro dell'appaiamento *(che e' una grandezza MISURATA, non scelta)*. |
| **4. tocca `rho`, `c_s` o il SEGNO?** | **Il SEGNO si', e solo per MISURARLO:** l'appaiamento `eps <-> -eps` e la degenerazione sono cio' su cui materia/antimateria si appoggia. ### ⛔ **Nessuna decisione, e nessun verso EM↔curvatura.** |
| **5. emergente o imposto?** | ### ⭐ **L'identita' `Theta W[n] Theta^-1 = W[-n]^-1` e' IMPOSTA dall'algebra** *(e' un conto, non un fenomeno)*. ### ⭐⭐ **Cio' che sarebbe EMERGENTE e' la mappa del reticolo di `(c)`:** se esiste, allora **esiste una simmetria antiunitaria ESATTA del passo** — e ### **quella non l'ha messa nessuno:** nasce dalla geometria del toro. ### **E il punto 3 del mandato precedente ha mostrato che una simmetria si puo' PERDERE senza accorgersene, quindi non la do per buona: la misuro.** |

---

## 4. TODO DEL NEXT STEP

1. `_misura_spettro_l1.py`: `accoppia_ottima`, `hausdorff`, `spaziatura`, i due casi
   *(deve passare / deve fallire)*, e il referto **accanto** al vecchio.
2. `RIPRESA` e `[[DECISIONE-LA-C-VUOLE-IL-TEMPO-ROVESCIATO]]`: **il `~2` corretto**, col
   numero giusto e con la spaziatura accanto.
3. `_misura_theta_n.py`: `(a)`, `(b)`, `(c)`, e **il censimento degli `n` LETTO DAL CODICE**
   dentro il referto.
4. `_collauda_memoria.py`: il braccio misura la **proprieta'**, e la prova dell'allocazione
   al tick `5`.
5. `RIPRESA` e mappa: i risultati, e **la CI rossa residua** *(dovrebbero restare i soli due
   bracci della deriva)*. Poi **STOP**.
