# `D2-TER`: LA SINCRONIZZAZIONE COME SORGENTE — LA MISURA DIRETTA E IL BRACCIO SENZA `K_SYNC`

> **Mandato di Luca, 2026-10-08 (`D2-TER`).** ### ⛔ **Solo diagnosi: il simulatore resta
> `b8c21049`, `doc/ASSIOMI.md` non si tocca, nessuna legge si tocca.**
> Il punto `0` *(la correzione del referto)* è chiuso in **`05c0f76`**, committato **da solo**.

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo prima di guardare*

### **DA DOVE VIENE.** Nel punto `0` ho verificato l'aritmetica del guardiano: la differenza
`W_tot − voce_coppia` vale **`−21170.0985`** su `1..215`, e con il secondo ordine quantificato
*(`+1081.1243`, che lui non aveva messo)* `W_sync` **stimato** è **`−22251.2229`** — il
**`93.56 %`** della crescita di `H`. ### ⛔ **Ma è DEDOTTO da una differenza, non misurato.**
Qui si misura.

### **E LA DERIVAZIONE È ESATTA, non approssimata.** Dal commit atomico *(`:7831`)*:

```
phi(t+1) = (phi_t + dt_n_s * phivel(t+1) + delta_sync_phi)  %  _dphi()
```

### ➜ **quindi `delta_sync_phi = Dphi − dt_n_s·phivel(t+1)`**, con `Dphi` l'incremento
**avvolto** e `dt_n_s = dt_n` *(perché `TEMPO_SEGNO = False`, e lo strumento FERMA se non lo è)*.
### **Non serve toccare il simulatore: la legge stessa dà il termine.**

### ⚠ **CHE COSA NON SO, e lo scrivo prima:**

| | |
|---|---|
| se le masse ### **si sciolgono** senza sincronizzazione | non lo so. La coerenza di `B-SCAL-TS` potrebbe venire dalla coppia *(che è `−∂U/∂φ`, quindi ORDINA le fasi)* oppure dalla sincronizzazione *(che è un `Kuramoto`, e ordina per mestiere)*. ### **La corsa lo dice** |
| quanto vale `W_sync` sulla coppia ### **DELL'INTERFERENZA** | la stima del guardiano è sulla coppia ### **TOTALE**. Sono due numeri diversi, e non so di quanto |
| se `K_SYNC = 0` sia ### **un solo interruttore** | il censimento qui sotto dice che l'unico altro effetto è ### **un `calcola_psi(w)` saltato**, e che quella chiamata ### **dovrebbe** essere byte-inerte. ### **«Dovrebbe» non basta: si MISURA** |

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### 2.1 ⭐ **IL CENSIMENTO DI `K_SYNC`: CHI LEGGE `forza`, E IN CHE STATO È**

### **Tutte** le occorrenze di `K_SYNC` nel simulatore, e i tre flag che riusano `forza`:

| dove | che cos'è | stato ### **a runtime nel driver** |
|---|---|---|
| `:394` | `K_SYNC = 1.0`, la ### **scala della legge** | ### **`1.0`** — ### ⛔ **e NON ha un flag CLI:** è una costante di modulo |
| `:7767` | `if K_SYNC != 0.0 and self.n > 2:` — ### **il cancello di tutto il blocco** | il blocco ### **gira** |
| `:7799` | `forza = K_SYNC * forza` | — |
| `:7805` | `delta_sync_phi = dt_n_s * forza * sin(media − phi_t)` | ### **l'UNICO effetto che esce dal blocco** |
| `:7800`-`:7801` | `_forza_sync` si popola ### **solo se** `SYNC_SPINORE or SYNC_FASE_OROLOGIO or KURAMOTO_SU2` | ### ✔ **tutti e tre `False`** *(`:3706`, `:3719`, `:3743`, e misurati a runtime)* → `_forza_sync` resta ### **`None`** |
| `:5946` · `:6053` · `:6067` | le ### **tre** leggi che leggono `forza_sync` *(`SYNC_SPINORE`, `SYNC_FASE_OROLOGIO`, `KURAMOTO_SU2`)* | ### ⛔ **non girano**, perché ricevono `None` |

### ⚠ **E `--sync` NON È `K_SYNC`**, e vale dirlo perché il nome inganna: `--sync` è un flag CLI
a sé *(`:11600`)*, conservato per decisione di Luca *(`:3205`)*, e ### **non tocca `K_SYNC`**.
*(La voce bloccante `CENS-A6` riguarda il commento del `README` su `--sync`, non questa legge.)*

### ⛔ **L'UNICO ALTRO EFFETTO DI `K_SYNC = 0`, E LO DICHIARO:** il blocco contiene
**`psi_sync = self.calcola_psi(w)`** *(`:7771`)*, e `calcola_psi` ### **SCRIVE** `self.psi`,
`self.psi_spin`, `self.rho_spin` *(`:6301`, `:6308`, `:6322`, `:6323`)*. Saltare il blocco salta
quella scrittura.
### ➜ **DOVREBBE essere byte-inerte**, perché l'ultima `calcola_psi` prima è `:7592` ### **con
lo STESSO `w`** *(sotto `REPULS_LEGGE`, che è `True`; il `:7633` è sotto `elif MU_PSI` e
### **non gira**)*, e fra le due ### **niente di ciò che `calcola_psi` legge cambia**:
`self.phi` è committata solo a `:7831`, e `_psi_spinor` solo a `:7826`.
### ⛔ **Ma «dovrebbe» non è una misura:** un involucro su `calcola_psi` ### **conta le chiamate
e firma `psi` prima e dopo ciascuna**, e il referto dice se quella a `:7771` ### **cambia mai
qualcosa**. ### **Se cambia, `B-SCAL-TS-NOSYNC` differisce per DUE cose e lo scrivo.**

### 2.2 **LE QUANTITÀ NUOVE, A OGNI PASSO E PER CLASSE**

| | |
|---|---|
| `delta_sync_phi` | `Dphi − dt_n·phivel(t+1)`, ### **esatto dalla legge di `:7831`** |
| ### **`W_newton`** | `Σ coppia_interf · (dt_n·phivel(t+1))` |
| ### **`W_sync`** | `Σ coppia_interf · delta_sync_phi` |
| gli stessi due sulla coppia ### **TOTALE** | `W_newton_tot`, `W_sync_tot` — ### **servono a confrontare con la stima del guardiano, che è sulla TOTALE** |
| la taglia | `rms` e `max` di `delta_sync_phi`, per classe |

### 2.3 ⛔ **IL CONTROLLO CHE IL MANDATO CHIEDE, E PERCHÉ NON BASTA DA SOLO**

Il mandato chiede che **`W_sync + W_newton` ricomponga `W_interferenza`**. ### ⚠ **Quella
somma è TAUTOLOGICA PER COSTRUZIONE**, e lo dico invece di spacciarla per un controllo: siccome
`delta_sync_phi` è *definito* come `Dphi − dt_n·p2`, allora
`(Dphi − dt_n·p2) + (dt_n·p2) = Dphi` ### **per algebra**. Si riporta *(il mandato la chiede)*,
e si dichiara tale.

### ⭐ **IL CONTROLLO VERO, CHE PUÒ FALLIRE:** nel braccio `B-SCAL-TS-NOSYNC`, con `K_SYNC = 0`,
`delta_sync_phi` deve essere ### **ESATTAMENTE `0` su ogni nodo e ogni passo**. ### **Se la mia
derivazione avesse il `dt` sbagliato, o la `phivel` sbagliata, o l'avvolgimento sbagliato, lì
NON uscirebbe zero.** ### ➜ **È il controllo che valida la formula, e non costa niente.**

### **E IL CASO CHE DEVE FALLIRE, nel collaudo:** la ricomposizione di `W_interferenza` con
### **un termine TOLTO** *(solo `W_newton`)* ### **NON deve chiudere.**

### 2.4 **IL BRACCIO `B-SCAL-TS-NOSYNC`**

Come `B-SCAL-TS` *(coppia scalare, `scuoti_vuoto` inerte, `xi_termo` azzerata)*, ### **più
`K_SYNC = 0` messo DALLO STRUMENTO sul modulo e ripristinato in un `finally`.**
### ⛔ **Nel simulatore non si tocca niente.** `500` passi, stessa scena, seme `11`, le stesse
misure.

### **E `B-SCAL-TS` SI RIGIRA PER INTERO, invece di una corsa più corta — dichiarato e con la
ragione:** il mandato permette una corsa più corta, ma una corsa a `230` passi lascerebbe
### **la finestra `216..500` senza la misura diretta**, dove la stima del guardiano dà
l'`84.38 %`. ### ➜ **E il tempo d'orologio non cambia:** le due corse girano
### **in parallelo**, quindi il muro è la più lunga *(`500` passi)* in ogni caso.
### ⭐ **E la ri-esecuzione dà GRATIS un controllo in più:** i contatori di `B-SCAL-TS` dal blob
nuovo contro quelli già committati devono coincidere ### **passo per passo**.

## 3. I CRITERI, FISSATI ADESSO *(quelli di Luca, verbatim)*

| | il criterio |
|---|---|
| ### **`LA SINCRONIZZAZIONE È LA SORGENTE`** | se nel braccio `2` la crescita di `H` fra il passo `1` e il `215` è ### **meno di un quarto** di quella di `B-SCAL-TS` *(`23782.6394`, quindi la soglia è ### **`5945.66`**)* |
| ### **`NON È LEI`** | se è ### **più della metà** *(cioè oltre ### **`11891.32`**)* |
| fra i due | ### **la curva** |

### **IN PIÙ, come il mandato chiede:** `AUC` al `230` e al `400`, coerenza ### **per massa**,
### **nascite**, `T` e `U` ### **per classe**. ### ⭐ **E se le masse si sciolgono senza
sincronizzazione è UN RISULTATO:** vorrebbe dire che ### **la sincronizzazione le teneva insieme
POMPANDO energia.**

### ⚠ **E LE DUE FINESTRE RESTANO SEPARATE** *(`FINESTRA-PRE-NASCITA`)*, anche se in questi
bracci la frontiera del `216` potrebbe non separare nessuna nascita: in quel caso il referto
### **lo dice** invece di lasciare l'etichetta mentire.

## 4. LE PREVISIONI, PRIMA DI VEDERE I NUMERI

| id | la previsione |
|---|---|
| **`PS-1`** | in `NOSYNC` `delta_sync_phi` è ### **esattamente `0`** su tutti i passi e tutti i nodi — e questo ### **valida la derivazione** |
| **`PS-2`** | in `B-SCAL-TS` `\|W_sync\|` è la parte ### **dominante** di `\|W_interferenza\|` *(oltre il `50 %`)* |
| **`PS-3`** | `W_sync` sulla coppia ### **dell'interferenza** sta ### **entro un fattore `2`** dalla stima del guardiano *(`−22251`, che è sulla TOTALE)* |
| **`PS-4`** | ### **`LA SINCRONIZZAZIONE È LA SORGENTE` è soddisfatto:** la crescita di `H` in `NOSYNC` sta sotto `5945.66`. ### **Se la stima del `93.56 %` è giusta, deve** |
| **`PS-5`** | ### ⛔ **le masse NON si sciolgono:** `AUC` al `400` resta ### **`>= 0.85`**, perché la coerenza viene dalla coppia *(che È `−∂U/∂φ`, quindi ordina le fasi)* e non dalla sincronizzazione. ### **Scritta per poter PERDERE: se l'`AUC` crolla, la sincronizzazione teneva le masse pompando** |
| **`PS-6`** | ### **zero nascite anche in `NOSYNC`**: il bagno resta spento, ed è lui che porta alla soglia *(il punto `0`)* |
| **`PS-7`** | la `calcola_psi` di `:7771` è ### **byte-inerte**: ### **zero** chiamate che cambiano `psi`, quindi `K_SYNC = 0` è ### **un solo interruttore** |
| **`PS-8`** | la ri-esecuzione di `B-SCAL-TS` dal blob nuovo dà ### **zero differenze** sui contatori già committati |

### **COSA MI FAREBBE FERMARE:** `delta_sync_phi` ### **non nullo** in `NOSYNC`; la `calcola_psi`
di `:7771` che ### **cambia `psi`** *(allora il braccio cambia DUE cose, e la cura è un'altra
misura, non questa)*; `phivel` non finito; `n` che cala.

## 5. LA STELLA POLARE — *le cinque risposte, per iscritto*

| | la risposta |
|---|---|
| **1 `A14`** | ### **non si applica al commit** *(nessuna legge cambia)*, ### ⭐ **e è il CUORE della misura:** si misura ### **quanta energia una legge di sincronizzazione IMMETTE**, cioè una violazione di conservazione ### **già nota e non ancora quantificata**. ### **Contributo ad `A14`, non esenzione** |
| **2 i tre gradini** | ### **(a) robusto al rumore numerico**, e non oltre: ### **un braccio, un seme** *(`P3` non soddisfatta)*. ### ⛔ **Il gradino (b) non è raggiunto:** togliere `K_SYNC` è ### **spegnere** una legge pratica, non mostrare che il fenomeno sopravvive senza di essa — ### **ed è esattamente ciò che la corsa decide** |
| **3 numeri o leggi** | ### **nessuno dei due.** `delta_sync_phi` si ### **DERIVA** dalla legge di `:7831`, non si stima; `K_SYNC = 0` è ### **spegnere**, non tarare. ### ⚠ **E `K_SYNC` stesso è un numero di modulo senza flag CLI** — ma è ### **già nell'inventario di `A1-COSTANTI`**, e qui non si ritara: si porta a zero per vedere |
| **4 `rho`, `c_s`, il SEGNO** | ### **nessuno toccato.** La sincronizzazione muove `φ`, non `rho` né `c_s`, e il verso `EM ↔ curvatura` non è in gioco |
| **5 emergente o imposto** | ### ⭐ **È LA DOMANDA.** La coerenza delle masse in `B-SCAL-TS` è ### **emergente dalla coppia** oppure ### **imposta da un `Kuramoto`** che la tiene pompando energia? ### **Togliere la legge pratica è il gradino (b), e la risposta la dà la corsa — non io** |

## 6. TODO DEL NEXT STEP

1. ### **questo file**, committato e pushato ### **PRIMA** del codice;
2. `W_sync`, `W_newton` *(interferenza e totale)* e la taglia di `delta_sync_phi` in `_energia`;
3. l'involucro su ### **`calcola_psi`** che firma `psi` prima/dopo ogni chiamata;
4. il braccio `B-SCAL-TS-NOSYNC` *(`K_SYNC = 0` solo nello strumento, `finally`)*;
5. il collaudo col ### **caso che deve fallire** *(solo `W_newton` NON ricompone)*;
6. la ### **byte-inerzia** dell'osservatore: tocco il percorso comune, quindi si rigira;
7. commit ### **prima** delle corse; ### **due** corse in background, interrogate, senza
   chiudere il turno;
8. ### **un referto** coi numeri dai json; poi ### ⛔ **FERMO: la cura è di Luca.**
