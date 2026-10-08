# `B-SCAL-TS`: LA COPPIA SCALARE SENZA BAGNO, E L'ENERGIA CHE LA LEGGE RENDE GIUSTA

> **Mandato di Luca, 2026-10-08 (`D2-BIS`, punto 2).** ### ⛔ **Solo diagnosi: il simulatore
> resta `b8c21049`, `doc/ASSIOMI.md` non si tocca, nessuna legge si tocca.**
> Il punto 1 *(la correzione del referto)* e' chiuso in **`57f8ed6`**, committato **da solo**
> come il mandato chiede.

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo prima di guardare*

### **IL BRACCIO.** `B-SCAL-TS` = la coppia **scalare** *(che legge la fase corrente)*
**senza termostato** e **senza scuotimento**. E' la composizione di `B-TS` e `B-SCAL`, due
interventi **gia' sigillati**, e serve a vedere se la coerenza che `B-SCAL` ha mostrato
*(`AUC 0.9020` contro `0.4679`)* **regge quando il bagno globale non c'e' piu'**.

### **CHE COSA CREDO.** Che la coerenza regga, e che l'energia **cresca molto meno** del
`x25.29` di `B-TS`: in `B-TS` la coppia **spinoriale** pompava il `90.35 %` del riscaldamento
delle masse, e in `B-SCAL` la coppia **scalare** nelle masse e' **negativa in 499 passi su
500**. Se la coppia e' un gradiente, non puo' pompare indefinitamente: puo' solo spostare
energia fra cinetica e potenziale.

### ⚠ **CHE COSA NON SO, e lo scrivo prima:**

| | |
|---|---|
| se la coppia scalare **conserva** davvero | non lo so: ### **`A` cambia a ogni passo** *(`w` si ricalcola, e le nascite aggiungono archi)*, e un potenziale il cui coefficiente cambia **fa lavoro**. La conservazione, se c'e', e' **a `A` fisso**, non lungo la corsa |
| se senza bagno il sistema **si congela** | con la coppia negativa nelle masse l'energia cinetica potrebbe **calare** fino a fermarsi: sarebbe un esito, non un guasto |
| quanto pesa `delta_sync_phi` | il `Kuramoto` muove `phi` **fuori** dalla coppia, e non so quanta parte del bilancio si prenda |

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e cosa decide ciascuno*

### 2.1 ⭐ **L'ENERGIA CINETICA, DERIVATA DAL CODICE** *(il mandato la chiede scritta)*

Le due righe che la definiscono, e non ce ne sono altre:

```
:7760   delta_phivel = dt_n_s * (coppia - self.xi_termo * _phivel_t) / M_PH
:7830   self.phivel  = _phivel_t + delta_phivel
```

Diviso per `dt_n_s` e' ### **la seconda legge di Newton sulla coordinata `phi`:**

```
M_PH * (phivel_k(t+1) - phivel_k(t)) / dt_n_k  =  coppia_k - xi * phivel_k(t)
```

### ➜ **Quindi l'energia cinetica e' `T = (1/2) * M_PH * somma_k phivel_k^2`.**

| il ruolo di | |
|---|---|
| ### **`M_PH`** | e' ### **l'INERZIA** della coordinata `phi`, uniforme e `= 1.0` *(`:401`)*. Numericamente `T = (1/2) somma phivel^2`, ma la forma la tiene esplicita: se `M_PH` cambiasse, `T` cambia |
| ### **`dt_n`** | ### ⛔ **NON entra in `T`.** E' il passo d'integrazione, ed e' ### **PER NODO** *(`dt_n = DT * r`, `:7498`, con `r = ritmo()`)*. Entra ### **solo** negli incrementi e nei lavori: `Dphi_k = dt_n_k * phivel_k(t+1)` *(`:7831`)* |

### ⚠ **E L'`E_cin` CHE IL CODICE CHIAMA COSI' NON E' QUESTA.** A `:7711` il termostato calcola
`E_cin = mean(_phivel_t[:n]**2)`: ### **una MEDIA, senza `1/2` e senza `M_PH`.** E' una
grandezza **intensiva**, un analogo di **temperatura**, che serve al confronto con `T_target`.
### ➜ **Due cose diverse con lo stesso nome: il referto riporta ENTRAMBE e dice quale e' quale.**

### 2.2 ⭐ **IL POTENZIALE, E PERCHE' LA COPPIA SCALARE NE E' IL GRADIENTE**

I tre pezzi, dal codice:

```
:7566   A = w * np.cos(self.phi0[i] - self.phi0[j])     # per ARCO, e usa phi0 CONGELATA
:7567   z = np.exp(1j * _phi_t)                         # la fase CORRENTE, snapshot t
:7484   return K_C * np.imag(np.conj(z) * (self._mat(A) @ z))     # il RAMO SCALARE
```

e `_mat` *(`:6257`)* mette ### **lo stesso valore nelle due direzioni** dell'arco
*(`concatenate([val, val])`)*, quindi la matrice e' ### **SIMMETRICA**. Allora

```
coppia_k = K_C * somma_{j vicini di k} A_kj * sin(phi_j - phi_k)
```

e con ### **`U = - K_C * somma_{archi} A_ij * cos(phi_i - phi_j)`** si ha

```
dU/dphi_k = K_C * somma_{j} A_kj * sin(phi_k - phi_j) = - coppia_k
```

### ➜ **`coppia = -dU/dphi`, ESATTAMENTE, a meno dell'arrotondamento.** E' questo che il
collaudo deve verificare **sulla funzione vera**, non su una mia copia.

### ✔ **E L'AVVOLGIMENTO NON DA' FASTIDIO, verificato:** `phi` e' preso modulo `_dphi()`
*(`:7831`)*, che con `FASE_2PI = False` *(`:3601`)* vale **`4 pi`** *(`:6392`)*. `4 pi` e' un
multiplo di `2 pi`, quindi ### **sia `cos(phi_i - phi_j)` sia `e^{i phi}` sono invarianti**:
l'avvolgimento non puo' falsare ne' `U` ne' la coppia.

### 2.3 ⛔ **LA PREMESSA CHE CADE, E LA DICO PRIMA DI GIRARE**

### **La `coppia` che muove `phivel` a `:7760` NON e' quella che `_coppia_interferenza`
restituisce.** Con i flag del driver ne vengono sommati ### **altri tre**, e un quarto termine
muove `phi` **fuori** dalla coppia. Censiti sul codice, uno per uno:

| termine | il flag, col suo default | dove si somma |
|---|---|---|
| repulsione dell'auto-interazione | ### **`REPULS_LEGGE = True`** *(`:3073`)* | `:7621` `coppia = coppia - fattore * dHdphi` |
| feedback locale spinore -> archi | ### **`SPIN_FEEDBACK = True`** *(`:3922`)*, con `SPINORE_VIVO` e `SPINORE` `True` | `:7656` `coppia += _fb` |
| trascinamento del frame *(torsione)* | ### **`FRAME_DRAG = True`** *(`:3262`)* | `:7702` `coppia = coppia + twist_nodo` |
| ### ⚠ sincronizzazione `Kuramoto` | ### **`K_SYNC = 1.0`** *(`:394`)* | `:7805` `delta_sync_phi`, sommato a `phi` a `:7831` -- ### **non passa dalla coppia** |

### ➜ **QUINDI IL CRITERIO DI LUCA, PRESO SULLA COPPIA TOTALE, NON PUO' CHIUDERE** -- e non
perche' il simulatore sbagli, ma perche' ### **la dinamica ha quattro leggi in piu' che non
sono il gradiente di `U`.** ### **Lo scrivo PRIMA della corsa invece di far fallire il criterio
e presentarlo come una scoperta.**

### **COME LO VALUTO, DICHIARATO:** il criterio si valuta su ### **la coppia di
`_coppia_interferenza`**, che *e'* il gradiente di `U`; e gli altri tre si ### **MISURANO**
come `W_extra = W_tot - W_interf`, cosi' chi legge vede ### **quanta parte della dinamica NON
e' conservativa** invece di vederla sparire in un residuo.

### 2.4 **LE QUANTITA', A OGNI PASSO, PER CLASSE E IN TOTALE**

| | |
|---|---|
| `T` | `(1/2) * M_PH * somma phivel^2`, su **masse**, **vuoto** e **totale** |
| `U` | `-K_C * somma A_ij cos(phi_i - phi_j)`, con ### **la `A` EFFETTIVAMENTE usata in quel passo** *(catturata dall'involucro: e' il suo primo argomento)*. Per arco: **massa** se **entrambi** gli estremi sono in una massa, **vuoto** se nessuno, **misto** altrimenti |
| `H` | `T + U` |
| `W_interf` | `somma_k coppia_interf_k * Dphi_k`, con `Dphi` l'incremento **avvolto** |
| `dU_phi` | `U(A vecchia, phi nuove) - U(A vecchia, phi vecchie)` -- ### **il lavoro delle sole `phi`** |
| ### ⭐ `dU_A` | `U(A nuova, phi nuove) - U(A vecchia, phi nuove)` -- ### **il lavoro di `A` che cambia**, e si emette con ### **un passo di ritardo** perche' `A nuova` nasce alla chiamata successiva. ### **Dichiarato** |
| la spartizione di `dU_A` | fra ### **`w` che cambia** *(archi presenti in ENTRAMBI i passi, confrontati per CHIAVE `i*N+j`)* e ### **le nascite** *(archi presenti in uno solo)* |
| `residuo_rel` | `(dU_phi + W_interf) / max(abs(W_interf), tiny)` |

### ✔ **E DUE COSE SI ASSERISCONO A OGNI PASSO**, perche' `U(A vecchia, phi nuove)` ha senso
solo se gli indici dei nodi sono stabili: che ### **`n` non cali mai**, e che ### **gli indici
degli archi di `A vecchia` siano tutti `< n` del passo prima.** Se una delle due cade, lo
strumento **FERMA**.

## 3. I CRITERI, FISSATI ADESSO *(quelli di Luca, verbatim)*

| | il criterio | come lo valuto |
|---|---|---|
| ### **`LA COPPIA SCALARE CONSERVA A A FISSO`** | in almeno il ### **`95 %`** dei passi, `P_coppia + (dU/dt dovuto alle sole phi)` ha ### **residuo relativo `< 1e-2`** | sulla coppia di `_coppia_interferenza` *(par. 2.3)*, nella forma del ### **LAVORO** `somma coppia * Dphi` e non `dt * P`, perche' ### **`dt_n` e' PER NODO**: `Dphi_k = dt_n_k * phivel_k(t+1)` |
| ### **`SENZA BAGNO NON ESPLODE`** | l'energia cinetica totale al `500` cresce ### **meno di `x3`** rispetto al passo `1` | da confrontare col ### **`x25.29`** di `B-TS` |

### **IN PIU', come il mandato chiede:** quanta parte della variazione di `H` viene dal
**lavoro di `A` che cambia** *(`w` e nascite)* e quanta dalle **`phi`**; l'**`AUC`** al `230` e
al `400`; la **coerenza di fase per massa**.

### ⚠ **E LA FINESTRA SI DICHIARA** *(`FINESTRA-PRE-NASCITA`)*: una conclusione sulla
conservazione presa su `1..215` vale ### **solo prima delle nascite**. Il referto riporta
### **`1..215` e `216..500` SEPARATI**, sempre.

## 4. LE PREVISIONI, PRIMA DI VEDERE I NUMERI

| id | la previsione |
|---|---|
| **`PE-1`** | il collaudo del potenziale ### **CHIUDE** sulla funzione vera, con residuo relativo `< 1e-10`: la derivazione del par. 2.2 e' algebra, non una congettura |
| **`PE-2`** | ### **il caso che DEVE fallire fallisce:** la coppia **spinoriale** non chiude, con residuo ### **`> 1e-2`** |
| **`PE-3`** | il criterio della conservazione e' ### **soddisfatto** *(`>= 95 %` dei passi)* nella finestra `1..215`, e ### **meno** dopo il `216`: le nascite cambiano `A` |
| **`PE-4`** | ### **`SENZA BAGNO NON ESPLODE` e' soddisfatto:** la coppia scalare nelle masse era negativa in `499/500`, quindi l'energia cinetica ### **non cresce `x3`** |
| **`PE-5`** | il ### **lavoro di `A` che cambia** e' la parte ### **dominante** della variazione di `H` dopo il passo `216`: le nascite aggiungono archi, e ogni arco aggiunge potenziale |
| **`PE-6`** | l'`AUC` al `400` resta ### **`>= 0.85`**: senza bagno la coerenza che `B-SCAL` teneva non dovrebbe peggiorare |
| **`PE-7`** | ### **`W_extra` NON e' trascurabile**: i tre termini in piu' valgono almeno il `10 %` di `W_interf` in modulo. Se fosse trascurabile, il criterio di Luca chiuderebbe anche sulla coppia totale, e il par. 2.3 sarebbe stato pessimismo mio |

### **COSA MI FAREBBE FERMARE:** il collaudo del potenziale che **non chiude** *(il mandato lo
dice: FERMATI e scrivilo)*; `n` che **cala**; `phivel` **non finito**; un indice d'arco **oltre
`n`**.

## 5. LA STELLA POLARE — *le cinque risposte, per iscritto*

| | la risposta |
|---|---|
| **1 `A14`** | ### **non si applica al commit, e si applica alla MISURA:** nessuna legge cambia, quindi niente di nuovo viola la conservazione. ### ⭐ **Ma e' proprio questo che la misura GUARDA:** il par. 2.3 dice che quattro leggi non sono il gradiente di `U`, e il referto ### **quantifica** quanto non conservano. ### **E' un contributo a `A14`, non un'esenzione** |
| **2 i tre gradini** | ### **(a) robusto al rumore numerico**, e non oltre: un braccio, un seme. ### ⛔ **Il gradino (b) non e' raggiunto**, e il motivo e' scritto: il ramo scalare usa `cos(phi_k - phi_j)`, non `cos((phi_k - phi_j)/2)` della direzione candidata di Luca |
| **3 numeri o leggi** | ### **nessuno dei due.** Lo strumento ### **non aggiunge niente al simulatore**: due involucri gia' sigillati, composti. `U` e `T` sono ### **DERIVATE** dal codice *(par. 2.1 e 2.2)*, non scelte |
| **4 `rho`, `c_s`, il SEGNO** | ### **nessuno toccato.** `B-SCAL-TS` tiene `xi_termo` a `0` e rende inerte `scuoti_vuoto`: ### **spegne due forzanti, non cambia un segno.** Il verso `EM <-> curvatura` non e' in gioco |
| **5 emergente o imposto** | ### ⭐ **E' ESATTAMENTE LA DOMANDA DEL BRACCIO.** `B-SCAL` ha mostrato la coerenza ### **con** il bagno; qui si toglie il bagno. ### **Se la coerenza sopravvive, e' emergente dalla coppia; se cade, era sostenuta dal forzante.** ### **La risposta la da' la corsa, non io** |

## 6. TODO DEL NEXT STEP — *la lista operativa*

1. ### **questo file**, committato e pushato ### **PRIMA** del codice *(il rito del par. 8)*;
2. `B-SCAL-TS` nelle tre appartenenze di `_termo_h3.py` *(`B-S`/`B-TS`, `B-T`/`B-TS`,
   `B-SCAL`)*, ### **diff additivo**, e nel collaudo la verifica che faccia ### **tutte e tre**
   le cose;
3. la misura dell'energia: `T`, `U`, `H`, `dU_phi`, `dU_A`, `W_interf`, `W_tot`, `residuo_rel`,
   con le ### **due asserzioni** del par. 2.4;
4. ### ⛔ **IL COLLAUDO DEL POTENZIALE sulla funzione VERA**, con il caso che ### **deve
   fallire** *(la coppia spinoriale)*. ### **Se non chiude: FERMO, e lo scrivo**;
5. la ### **byte-inerzia** dell'osservatore *(`csv/_seal_fork/_inerzia_termo.py`)*: tocco il
   percorso comune, quindi si rigira ### **anche se la misura nuova e' chiusa dentro al braccio
   nuovo**;
6. commit ### **prima** della corsa *(par. 5)*, poi la corsa in background, ### **interrogata
   senza chiudere il turno**;
7. ### **un referto**, coi numeri ### **generati dai json** *(`L-NUMERI`)*, con `1..215` e
   `216..500` separati;
8. ### ⛔ **poi FERMO: la cura e' una DECISIONE DI LUCA.**
