# `D3`: LA FORMA `U(2)` DELLA COPPIA, NELLO STRUMENTO — LA DERIVAZIONE E IL BRACCIO

> **Mandato di Luca, 2026-10-08 (`D3`).** ### ⛔ **Solo diagnosi: il simulatore resta
> `b8c21049`, `doc/ASSIOMI.md` non si tocca, nessuna legge del simulatore si tocca. La forma
> `U(2)` vive SOLO nello strumento.**
> ### ⚠ **E la forma è una DIREZIONE CANDIDATA di Luca, NON decisa.**

## 1. RAGIONAMENTO PRELIMINARE

### **DA DOVE VIENE.** `D2-BIS` e `D2-TER` hanno mostrato che una coppia che **legge la fase
che muove** tiene le masse coerenti *(`AUC` al `400` `0.9333` senza nessun forzante)*, ma la
prova era sul **principio**: il ramo scalare usa `cos(φ_k − φ_j)`, ### **non**
`cos((φ_k − φ_j)/2)`. ### ➜ **`D3` prova la FORMA.**

### ⚠ **CHE COSA NON SO, e lo scrivo prima:**

| | |
|---|---|
| se la forma `U(2)` ### **tenga** le masse | non lo so. Il `½` dimezza la forza per lo stesso salto di fase, e il peso `\|N\|/2 = cos(χ/2)` ### **spegne** gli archi fra spin disallineati: due ragioni per cui potrebbe tenere ### **meno** del ramo scalare |
| quanto pesi la ### **precessione di `χ`** | `χ` evolve per conto suo *(`_passo_spinoriale`)*, e quella evoluzione ### **non viene da `E`**. Se `dU_χ` è grande, la forma è ### **incompleta** come legge |
| se la fase comune dello spinore ### **sia** `φ/2` | ### ⛔ **questa è la domanda vera**, e la misuro: la forma ### **assume** che lo sia, e se non lo è la forma ### **butta via** informazione che il simulatore usa oggi |

## 2. LA DERIVAZIONE, PER ISCRITTO

### 2.1 **LA FORMA**

```
psi_k   = e^{i phi_k / 2} * chi_k
chi_k   = ( cos(theta_k/2) ,  sin(theta_k/2) * e^{i varphi_k} )      la DIREZIONE di Bloch
E       = - K_C * somma_archi A_ij * Re< psi_i | N_ij | psi_j >
coppia_k = - dE / dphi_k
```

con la **stessa `A`** *(`:7566`)* e la **stessa `N`** del ramo `FORK_SU2`, ### **`½`
compreso**: nel codice `_N = self._link_su2_N(nb_i, nb_j) * 0.5` *(`:7471`)*, e il docstring di
`_link_su2_N` *(`:4190`)* dice che ### **`N/2 = I` ad allineati**, cioè che il `½` è la
normalizzazione che dà la riduzione esatta allo scalare.

### 2.2 ⭐ **LA DERIVATA, PASSO PER PASSO**

Posto `ov_ij := <psi_i| N_ij |psi_j>` e `M_ij := <chi_i| N_ij |chi_j>`:

```
ov_ij = e^{-i phi_i/2} * e^{+i phi_j/2} * M_ij  =  e^{i (phi_j - phi_i)/2} * M_ij
```

### **`M_ij` NON dipende da `phi`:** dipende solo dalle direzioni e da `N`. Quindi

```
d(ov)/dphi_j = +(i/2) ov           d(ov)/dphi_i = -(i/2) ov
d Re(ov)/dphi_j = Re(+(i/2) ov) = -(1/2) Im(ov)
d Re(ov)/dphi_i = Re(-(i/2) ov) = +(1/2) Im(ov)
```

e con `E = -K_C somma A Re(ov)`:

```
dE/dphi_j = +(1/2) K_C A Im(ov)         dE/dphi_i = -(1/2) K_C A Im(ov)
```

### ➜ **Quindi, posto `s_ij := K_C * A_ij * Im(ov_ij)`:**

```
coppia_i  +=  + (1/2) * s_ij
coppia_j  +=  - (1/2) * s_ij
```

### **La coppia `U(2)` è la META' della parte immaginaria dell'overlap trasportato, accumulata
in modo ANTISIMMETRICO sull'arco.**

### 2.3 ✔ **`E` È REALE E SIMMETRICA, e il perché è `N_ji = N_ij†`**

Il docstring di `_link_su2_N` dichiara `N_ji = N_ij^dag` ### **esattamente** *(polinomiale,
nessun arrotondamento)*. Allora

```
<psi_j| N_ji |psi_i>  =  <psi_j| N_ij^dag |psi_i>  =  coniugato di  <psi_i| N_ij |psi_j>
```

### ➜ **`Re` è INVARIANTE allo scambio degli estremi** *(quindi il termine d'arco è
### **simmetrico** e `E` non dipende da come si orienta l'arco)*, e ### **`Im` CAMBIA SEGNO**
*(quindi l'accumulo antisimmetrico del par. 2.2 è ### **l'azione-reazione**, non una scelta)*.
### **E `E` è reale per costruzione, perché si prende `Re`.**

### 2.4 ⭐ **IL LIMITE `U(1)`: che cosa deve venire**

Con `chi` ### **uguale su tutti i nodi** e `N = I` *(spin allineati)*: `M_ij = <chi|chi> = 1`,
quindi `ov = e^{i(phi_j - phi_i)/2}` e `Im(ov) = sin((phi_j - phi_i)/2)`.

### ➜ **`coppia_k = (1/2) * K_C * somma_{j vicini} A_kj * sin((phi_j - phi_k)/2)`** — che è
### **esattamente** la forma che il mandato chiede. ### **È il collaudo `(3)`.**

### 2.5 ⭐ **LA DOPPIA COPERTURA, e si vede su `E`**

`phi_k -> phi_k + 2pi` dà `e^{i(phi_k + 2pi)/2} = e^{i phi_k/2} * e^{i pi} = - e^{i phi_k/2}`,
cioè ### **`psi_k -> - psi_k`**: i termini d'arco che toccano `k` ### **cambiano segno**, e
`E` ### **cambia**. Con `4 pi` il fattore è `e^{i 2 pi} = 1` e ### **`E` torna identico**.
### ➜ **`E` DISTINGUE `2 pi` da `4 pi`**, ed è il collaudo `(2)`.
*(E il dominio di `phi` è già `4 pi`, perché `FASE_2PI = False` — `:3601`, `:6392`.)*

### 2.6 ⛔ **LA GAUGE, E PERCHÉ NON È UN DETTAGLIO**

`chi_k` si ottiene da `_psi_spinor[k]` ### **privandolo della fase comune**:
`chi_k = psi_spinor_k * e^{-i alpha_k}` con `alpha_k = arg(prima componente)`, così la prima
componente è ### **reale `>= 0`** — ed è esattamente la parametrizzazione
`(cos(theta/2), sin(theta/2) e^{i varphi})` che il mandato scrive.

| | |
|---|---|
| ### ⚠ **il caso degenere** | se `\|a\| -> 0` *(lo spinore è al ### **polo `b`**)*, `arg(a)` non è definito. ### **COME LO TRATTO, dichiarato:** sotto una soglia la gauge si fissa sulla ### **SECONDA** componente *(`b` reale `>= 0`)*, e ### **si CONTANO i nodi che prendono quel ramo, a ogni passo** |
| ### ✔ **`N` non è toccata dalla gauge** | il Bloch si costruisce da `conj(a)*b` e `\|a\|^2-\|b\|^2`, che sono ### **invarianti** per fase comune. Quindi `N` è la stessa: la gauge entra ### **solo** in `M_ij` |
| ### ⛔ **MA LA FORMA BUTTA VIA LA FASE DELLO SPINORE** | `_psi_spinor` ### **ha** una sua fase comune `alpha_k`; la forma `U(2)` la ### **sostituisce** con `phi_k/2`. ### **È un'ASSUNZIONE del modello, non una riscrittura**, e si misura: `rms( wrap(alpha_k - phi_k/2) )`. ### **Se è grande, la forma è un modello DIVERSO, e va detto** |

## 3. CHE COSA SI MISURA, E IL BRACCIO

### 3.1 **IL BRACCIO `B-U2-TS-NOSYNC`**

Come `B-SCAL-TS-NOSYNC` *(senza termostato, senza scuotimento, `K_SYNC = 0`)*, ### **ma con la
coppia `U(2)` al posto di quella scalare**, calcolata ### **nello strumento** e restituita da un
involucro su `_coppia_interferenza`. Seme `11`, `500` passi.

### ⛔ **E UN VINCOLO CHE IL CODICE IMPONE, dichiarato:** `_bloch_ritardato` *(`:7223`)*
### **SCRIVE `self._nb_ret`** — ha memoria. Quindi va chiamata ### **esattamente una volta per
passo**: il mio involucro ### **sostituisce** l'originale *(non la chiama)*, e chiama
`_bloch_ritardato` ### **una volta sola**, come faceva lei. ### **`_link_su2_N` è pura**
*(censito: zero scritture su `self`)*, quindi la posso chiamare anche due volte.

### 3.2 ⭐ **LA SPARTIZIONE DI `ΔE` IN TRE PEZZI ESATTI**

```
DE(k -> k+1) = [ E(M_k,     phi_{k+1}, A_k    ) - E(M_k, phi_k, A_k) ]      <- dU_phi
             + [ E(M_{k+1}, phi_{k+1}, A_k    ) - E(M_k, phi_{k+1}, A_k) ]  <- dU_chi
             + [ E(M_{k+1}, phi_{k+1}, A_{k+1}) - E(M_{k+1}, phi_{k+1}, A_k) ]  <- dU_A
```

### **I tre termini sommano a `DE` per costruzione**, e ciascuno è ### **esatto**. Gli ultimi
due si chiudono con ### **un passo di ritardo** *(servono `M_{k+1}` e `A_{k+1}`)*, ed è
### **dichiarato**. ### ⚠ **Se gli archi cambiassero, `dU_chi` e `dU_A` sui vecchi archi non
sono definiti: lo strumento lo ASSERISCE e, se cade, mette `None` con la ragione.**

### ⭐ **E `dU_chi` È IL NUMERO CHE VALE:** `chi` precede per conto suo, e quella precessione
### **non viene da `E`**. ### **Se `dU_chi` è grande, la forma `U(2)` è incompleta come legge** —
e il mandato dice che è un risultato.

### 3.3 **E LE MISURE DI `D2-TER`, tutte**

`T` *(`= ½ M_PH Σ phivel²`)*, `W_newton`, `W_sync`, `W_extra`, `delta_sync_phi`, `AUC`,
coerenza per massa, nascite — ### **per classe**, con le due finestre `1..215` e `216..500`
separate.

## 4. I CRITERI, FISSATI ADESSO *(quelli di Luca)*

| | il criterio | il confronto |
|---|---|---|
| ### **`LA FORMA U(2) TIENE LE MASSE`** | `AUC` al `400` ### **`>= 0.85`** ### **E** la cinetica al `500` cresce ### **meno di `×3`** | `B-SCAL-TS-NOSYNC`: `AUC` `0.9333`, cinetica ### **`×2.49`** |
| ### **`NON TIENE`** | `AUC` al `400` ### **`< 0.6`** | — |
| fra i due | ### **la curva** | — |

### **DA DICHIARARE NEL REFERTO, e il mandato lo impone:** l'energia per legame va come
### **`cos(Δφ/2)`** e ### **non** come `cos(Δφ)`; e il campo scalare *(`calcola_psi`)*
### **resta a `e^{iφ}`** — ### ⚠ **è una scelta di Luca ancora APERTA**, e questo braccio
### **non la tocca**.

## 5. LE PREVISIONI, PRIMA DI VEDERE I NUMERI

| id | la previsione |
|---|---|
| **`PU-1`** | il collaudo `coppia = −∂E/∂φ` ### **chiude** con scarto relativo `< 1e-12`, e la differenza finita locale conferma: la derivazione del par. 2.2 è ### **algebra** |
| **`PU-2`** | la ### **doppia copertura** si vede: `E(φ+2π) ≠ E(φ)` e `E(φ+4π) = E(φ)` al bit |
| **`PU-3`** | il ### **limite `U(1)`** torna: con `χ` uguale e `N = I` la coppia è `½ K_C Σ A sin(Δφ/2)` entro `1e-12` |
| **`PU-4`** | ### **il caso che DEVE fallire fallisce:** la coppia spinoriale del driver ### **non** è `−∂E/∂φ` |
| **`PU-5`** | ### ⛔ **`dU_χ` è GRANDE** *(almeno come `dU_φ` in modulo)*: `χ` precede per conto suo, e la forma non la governa. ### **Scritta per poter PERDERE: se fosse piccola, la forma sarebbe quasi completa** |
| **`PU-6`** | la fase comune dello spinore ### **NON è** `φ/2`: `rms(wrap(α − φ/2))` è ### **oltre `1` radiante**. ### **Se fosse piccola, la forma sarebbe una riscrittura e non un modello nuovo** |
| **`PU-7`** | ### **`LA FORMA U(2) TIENE LE MASSE`**: `AUC` al `400` `>= 0.85` ### **e** cinetica `< ×3`. ### ⚠ **Ci credo MENO che per il ramo scalare**, per due ragioni scritte nel par.1 *(il `½` dimezza la forza, e il peso `cos(χ/2)` spegne gli archi disallineati)* |
| **`PU-8`** | ### **zero nascite**, come nei due bracci precedenti: il bagno resta spento |

### **COSA MI FAREBBE FERMARE:** il collaudo `(1)` che ### **non chiude** *(allora la mia
derivata è sbagliata, e la corsa non parte)*; il limite `U(1)` che non torna; `_bloch_ritardato`
chiamata ### **più di una volta per passo**; `phivel` non finito.

## 6. LA STELLA POLARE — *le cinque risposte, per iscritto*

| | la risposta |
|---|---|
| **1 `A14`** | ### ⭐ **QUI SI APPLICA DAVVERO, ed è il punto:** la forma `U(2)` è ### **per costruzione** `−∂E/∂φ` di un'energia ### **scritta**, quindi sul settore `φ` ### **conserva per definizione**. ### ⛔ **Ma NON conserva su `χ`:** la precessione dello spinore non viene da `E`, e `dU_χ` ### **misura la violazione che resta** |
| **2 i tre gradini** | ### **(a)** robusto al rumore numerico, e ### **(c) coincide con un limite noto**: il limite `U(1)` del par. 2.4 è ### **un controllo di collaudo**, non un'aspettativa. ### ⛔ **Il gradino (b) NON è raggiunto:** un seme, un braccio |
| **3 numeri o leggi** | ### **nessun numero nuovo.** `K_C`, `A` e `N` sono ### **quelli del simulatore**, `½` compreso. ### ⚠ **MA SI AGGIUNGE UNA SCELTA, e la dichiaro:** la ### **gauge** che priva `χ` della fase comune *(par. 2.6)*. ### **Non è un parametro, è una convenzione — e entra in `E`** |
| **4 `rho`, `c_s`, il SEGNO** | ### **nessuno toccato.** La forma cambia ### **come `φ` entra nella coppia**, non `rho` né `c_s`. ### ⚠ **E il campo scalare resta a `e^{iφ}`:** scelta di Luca ### **aperta**, dichiarata e non toccata |
| **5 emergente o imposto** | ### ⛔ **IMPOSTO, e lo dico:** la forma `U(2)` è ### **scritta da Luca**, non emersa da una misura. ### **Quello che la corsa può dire è se REGGE**, non se nasce. ### **E `dU_χ` dice quanto resta FUORI dall'energia** |

## 7. TODO DEL NEXT STEP

1. ### **questo file**, committato e pushato ### **PRIMA** del codice;
2. la coppia `U(2)` nello strumento, con l'involucro che ### **sostituisce**
   `_coppia_interferenza` e chiama `_bloch_ritardato` ### **una volta sola**;
3. la gauge col ### **conteggio** del ramo degenere, e `rms(wrap(α − φ/2))`;
4. la spartizione `dU_φ` / `dU_χ` / `dU_A` del par. 3.2;
5. ### ⛔ **IL COLLAUDO SULLA FUNZIONE VERA, coi QUATTRO controlli** *(gradiente, doppia
   copertura, limite `U(1)`, e il caso che deve fallire)*. ### **Se il primo non chiude: FERMO**;
6. la ### **byte-inerzia** se tocco il percorso comune;
7. commit ### **prima** della corsa; corsa in background, interrogata, senza chiudere il turno;
8. ### **un referto** coi numeri dai json; poi ### ⛔ **FERMO: la cura nel simulatore è una
   decisione di Luca.**

## LA CHIUSURA DI `D3` — **ABBANDONATO PER DECISIONE** *(`A16`, 2026-10-08)*

*(Annotazione, come vuole il par.8: ### **sopra non si riscrive niente.**)*

> ### ⛔ **`D3` NON si chiude perche' e' riuscito ne' perche' e' fallito: si chiude perche'
> LA DOMANDA NON E' PIU' QUELLA.** `D3` chiedeva *«la forma `U(2)` regge DENTRO la dinamica
> del SECONDO ordine?»*. ### **`A16` dice che quella dinamica non c'e' piu'**, e la decisione
> e' di Luca.

### **COM'ERA RIMASTO.** La corsa `B-U2-TS-NOSYNC` si e' fermata ### **al primo passo**, su
una ### **mia guardia**: `_psi_spinor` ### **non esiste ancora al passo `1`** *(lo scrive
`_passo_spinoriale`, che gira DOPO la coppia)*. La correzione — ridurre la forma al suo limite
`U(1)` e ### **contare quei passi** — e' ### **scritta e NON applicata**, perche' il file era
importato dal processo in volo *(par.5)*.

### ✔ **CHE COSA DI `D3` RESTA VALIDO E PASSA ALL'ERA `2`** *(il collaudo e' su `9` controlli
su `9`, e il suo output e' committato in questo commit)*:

| | il fatto | il numero |
|---|---|--:|
| ### ⭐ **la DERIVATA della forma** | `coppia = −∂E/∂φ`, e la forma `\|M\| sin(Δφ/2 + arg M)` da' ### **la STESSA coppia**: la derivata ### **non poggia su una sola scrittura** | ### **`3.494e-16`** |
| ### **la DOPPIA COPERTURA sul segno RELATIVO** | uno spostamento ### **globale** di `2π` ### **non cambia `E`**, perche' `E` dipende dalle ### **DIFFERENZE** ⇒ ### **la doppia copertura si vede sul segno RELATIVO, non su quello assoluto** | `9.095e-13` |
| ### **il LIMITE `U(1)` ESATTO** | la coppia si riduce a `(1/2)·K_C·Σ A sin((φ_j − φ_k)/2)` | ### **`0.000e+00`** |
| ### ⭐ **e IL FATTO MISURATO che vale di piu'** | ### **i due orologi dell'era `1` sono SCOLLEGATI:** la fase comune `α` dello spinore e `φ/2` ### **non sono la stessa cosa** | ### **`rms(wrap(α − φ/2)) = 1.9716` rad** *(mediana `1.7377`)* |

### ⛔ **CHE COSA NON PASSA, e appartiene al SECONDO ordine:**

| | |
|---|---|
| ### **la corsa `B-U2-TS-NOSYNC`** | misurava la forma ### **dentro `phivel`**, cioe' dentro l'inerzia che `A16` ### **toglie** |
| ### **il criterio sull'`AUC`** | confrontava due ### **traiettorie del secondo ordine**. ### **Nell'era `2` la coerenza si misura su uno stato stazionario, non su un transitorio** |
| ### ⚠ **e la mia guardia stessa** | *«`_psi_spinor` non esiste al passo `1`»* e' un difetto ### **dell'ordine di esecuzione** di un passo a piu' settori: con ### **una sola `H`** quel problema ### **non esiste** |

### ⚠ **E UNA COSA CHE NON ERA UN RISULTATO DI `D3` MA LO E' DIVENTATA:** lo scarto
### **`1.054`** fra la coppia del driver e la forma `U(2)` era nato come *«quanto la forma
differisce»*. ### ➜ **Con il criterio del «no» di Luca** *(soglia del `10 %` per chiamare una
riscrittura «traduzione»)* ### **quel numero dice che la forma `U(2)` NON E' UNA TRADUZIONE: e'
UNA LEGGE NUOVA**, e sta nell'elenco delle decisioni di `doc/TRADUZIONE_IN_H.md` *(la `11`)*.
### **Il numero non e' cambiato: e' cambiato che cosa significa.**
