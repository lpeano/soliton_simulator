# `T3` pezzo ②: **LA NASCITA È UN EVENTO ATOMICO** *(2026-09-28)*

> ### 🛑 **Scritto e committato PRIMA del codice** *(par.8)*, e questa volta il par.8 serve a
> qualcosa di preciso: ### **il sigillo NON sarà byte-identico**, quindi **le letture non possono
> essere scelte dopo aver visto i numeri.**
> **Mandato di Luca:** *«la separazione della mitosi con la nascita atomica e il rinculo dei
> genitori. Il sigillo NON sarà byte-identico: prima del codice dichiara cosa ti aspetti che cambi
> (i flash di `psi` al passo di nascita) e cosa deve restare uguale nei passi senza nascite.»*
> **Blob del simulatore all'inizio: `05691d41`.** `mitosi` è **`:6138`–`:6679`, 542 righe.**

---

# 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare i numeri*

## 1.1 — Che cosa ho letto, e sono fatti non impressioni

**Le 82 scritture di stato o struttura dentro `mitosi`, con 14 alternanze fra le due.** Il quadro:

| | blocco | che cos'è |
|---|---|---|
| `:6186`–`:6381` | **contatori** *(`_g_…`, `_tum_…`, `_rep_…`)* | osservatore: **non è fisica** |
| ### `:6396` | `self.d0 = self.d0 + self._sd0(spinta)` | ### **la SPINTA REPULSIVA — è DINAMICA, e gira ANCHE NEI PASSI SENZA NASCITE** |
| `:6411`–`:6421` | `c`, `ok`, `sel` | **la decisione** |
| `:6466`–`:6485` | `pos` `phi` `phi0` `phi_s` `phivel` `eta` `perc_chi` `perc_geom` `perc_tw` `mem_mot` | ### **struttura E nascita NELLA STESSA ISTRUZIONE**: `concatenate([x, valore_del_figlio])` |
| ### `:6506`–`:6510` | `phi[a] += calcio_a` · `phi[b] += calcio_b` · `phi[g] += rumore` | ### **IL RINCULO DEI GENITORI, e sta già qui** |
| `:6533`–`:6559` | `i` `j` `d` `d0` `vd` `peq` `_rep` `tw` `twp` | **archi**: struttura e nascita **fuse** |
| `:6625`–`:6676` | il canale di **Schwinger** | **lo stesso schema, di nuovo** |

> ### 📌 **La scoperta che cambia la forma del lavoro:** ### **l'evento atomico ESISTE GIÀ, ma è
> INTERLEAVED.** Il rinculo dei genitori *(`:6506`)* sta **fra** la struttura dei nodi *(`:6466`)* e
> la struttura degli archi *(`:6533`)*. **Non manca un pezzo: manca il CONFINE.**

## 1.2 — ⚠ **E un fatto che decide tutto il sigillo**

### **`:6396` sta PRIMA del `return 0` per assenza di nascite.**

Quindi un *«passo senza nascite»* **non è un passo in cui `mitosi` non scrive**: scrive `d0` con la
spinta repulsiva. ### **Il confine fra ciò che cambia e ciò che non cambia è quel `return`.**

> ### **Dichiarazione di perimetro: NON TOCCO NIENTE PRIMA DI `if not len(c): return 0`.**
> La spinta repulsiva è la voce **`TORS-SPINTA`**, e Luca l'ha rinviata a **dopo `T3`**. Toccarla qui
> sarebbe **due cambi di fisica nello stesso sigillo**.

## 1.3 — ### 🎯 **CHE COSA MI ASPETTO CHE CAMBI**

**Uno solo, e ha un nome: `PSI-FLASH`.** La catena, letta dal codice:

```
mitosi fa crescere `n`  ->  len(self.psi) < self.n  ->  la PRIMA legge che legge `psi`
                            chiama `self.calcola_psi()`  ->  psi RICALCOLATA INTERA
```

**Ci sono `8` siti con quella guardia** *(`:2407`, `:2463`, `:2642`, `:3256`, `:3445`, `:3560`,
`:6821` e `calcola_psi` stessa)*: **il primo raggiunto dopo `mitosi` decide dove scatta il flash.**

> ### **Il flash NON riguarda i nati: riguarda TUTTI.** `calcola_psi()` riscrive `psi` per **ogni**
> nodo, con lo stato **di dopo la mitosi**. ### **Al passo di nascita, `psi` dei nodi VECCHI salta** —
> e chi legge `psi` in quel passo legge un valore che non discende dalla sua fotografia.

**La cura:** `mitosi` **ESTENDE** `psi` e `psi_spin` ai soli nuovi indici *(forma **7** per il valore
di partenza, forma **3** per il ricalcolo dei soli nati)*, così `len(psi) == n` **sempre** e
### **nessuna legge ricalcola più niente.**

### Quindi mi aspetto, al passo di nascita:

| | |
|---|---|
| **①** | ### **`psi` e `psi_spin` dei nodi VECCHI: DIVERSI da oggi** *(non saltano più)* |
| **②** | **tutto ciò che legge `psi` in quel passo**: `d`, `d0`, `peq`, `phivel`, `omega_s` … ### **diversi a valle** |
| **③** | ### **il NUMERO di nascite: IDENTICO** — vedi il perimetro qui sotto |

## 1.4 — ### 🔒 **CHE COSA DEVE RESTARE UGUALE**

| | |
|---|---|
| ### **①** | ### **OGNI PASSO SENZA NASCITE: BYTE-IDENTICO su tutte e 23 le grandezze.** Niente di ciò che tocco gira, perché sta **dopo** il `return 0` |
| **②** | ### **la DECISIONE: identica.** Quali archi si dividono, quanti, e quali nodi nascono |
| **③** | il **rinculo** dei genitori: **gli stessi valori**, solo **dentro il confine** |
| **④** | i **contatori** `_g_nati_mitosi`, `_g_nati_schwinger`: **identici** |

## 1.5 — ⚠ **IL PERIMETRO, e lo propongo invece di prenderlo per deciso**

Il piano di `T3` *(par.4.2)* mette come **fase 1** *«la decisione si prende sulla FOTOGRAFIA»*, e
dichiara che ### **gli archi che si dividono possono essere DIVERSI.**

> ### **Propongo di NON farlo in questo pezzo, e la ragione è la tua stessa su `DOPPIA-COP`:**
> sarebbero ### **due cambi di fisica nello stesso sigillo** — il riordino *e* il cambio degli
> ingressi della decisione — **e un sigillo che ne contiene due non attribuisce più un risultato a un
> pezzo preciso.**

**Con la decisione INVARIATA, il sigillo diventa affilato:** l'insieme dei nati è lo stesso, quindi
### **l'UNICA differenza al passo di nascita è `psi`/`psi_spin` e ciò che ne discende.** Con la
decisione spostata, invece, **nascerebbero nodi diversi** e non saprei più **se la differenza viene
dal riordino o dagli ingressi**.

### ➜ **Se preferisci tutto in una volta, sono due sigilli: dimmelo e li faccio in quest'ordine.**

## 1.6 — ⚠ **CHE COSA NON SO**

| | |
|---|---|
| ### **①** | ### **NON SO SE ESISTE UNA SCENA CON NASCITE A BASSO COSTO**, e questo è il rischio vero: sulla scena dei sigilli `(ii)(a)` seme `11` ho **misurato 40 passi con ZERO nascite**. ### **Su quella scena l'effetto della cura NON SI VEDE.** Serve una scena che **divide davvero** |
| **②** | non so **quale** degli 8 siti scatti primo dopo `mitosi` nel run reale. Lo so **dalla lettura**, non da una misura |
| **③** | non so se `psi_spin` si estenda con la stessa regola di `psi`: `psi_spin` nasce da `_Fs` e dallo spinore, e ### **estenderlo «come `psi`» sarebbe un'assunzione, non una lettura** |
| **④** | non so se qualcuno **CONTI** sul flash. Un ricalcolo intero è anche una **ri-normalizzazione**: se una legge si appoggia a quella, togliere il flash la cambia. **Lo cerco, ma per nome** *(`A9`)* |
| **⑤** | ### **non so se il riordino del rinculo sia byte-neutro quando un nodo è genitore DUE VOLTE** nello stesso passo: `:6506` scrive `phi[a]` e `:6507` scrive `phi[b]`, e **se un indice compare in entrambi l'ordine conta**. Nel ramo stocastico *(il default)* è **una sola** scrittura su `g = concatenate([a, b])`, e lì **un indice ripetuto prende l'ultimo valore** |

---

# 2. PROGETTAZIONE DEL RAGIONAMENTO

## 2.1 — I passi, **cosa decide ciascuno**, e ### **cosa mi FERMA**

| | passo | decide | ### **cosa mi FERMA** |
|---|---|---|---|
| **0** | ### **TROVARE UNA SCENA CON NASCITE**, e contare i passi che servono | se il sigillo è **possibile** | ### **se non la trovo a basso costo: MI FERMO e lo dico.** Una cura il cui effetto non si può misurare è `A9` |
| **1** | cercare chi **dipende dal flash**, e verificare `:6506`/`:6507` sugli **indici ripetuti** | la forma della cura | ### **se un indice è genitore due volte nel ramo deterministico: MI FERMO** |
| **2** | **il confine**: `_nascita_apri` / `_nascita_chiudi`, o un blocco unico dichiarato | — | ### **se servisse un numero nuovo: MI FERMO** *(`A1`)* |
| **3** | **l'estensione di `psi`/`psi_spin`** ai soli nati | chiude `PSI-FLASH` | ### **se `psi_spin` non ha una regola di estensione LEGGIBILE: MI FERMO e chiedo** |
| **4** | il **sigillo**, cinque bracci | — | ### **se un passo SENZA nascite non è byte-identico: MI FERMO.** Vorrebbe dire che ho toccato qualcosa prima del `return` |

## 2.2 — ### **LE LETTURE, FISSATE QUI, PRIMA DEI NUMERI**

| | braccio | passa se |
|---|---|---|
| ### **A** | **passi SENZA nascite**, driver, 3 passi, seme `11` | ### **byte-identico 23 su 23.** Nient'altro passa |
| ### **B** | **il passo di NASCITA**, sulla scena trovata al passo 0 | ### **`psi` e `psi_spin` DIVERSI**, e ### **`_g_nati_mitosi` + `_g_nati_schwinger` IDENTICI** |
| ### **C** | il **conto dei flash** | ### **`calcola_psi` chiamata da una delle 8 guardie: da `>= 1` a ZERO** al passo di nascita. **È la prova che la cura fa ciò che dice** |
| **D** | `len(psi) == n` **a ogni uscita di `mitosi`** | ### **sempre**, e **mai** `<` |
| **E** | il **caso che deve fallire** | ### **sul blob VECCHIO il braccio `C` conta `>= 1`** — senza questo, `C` non distingue la cura da niente |

> ### ⚠ **`B` non è un criterio di SUCCESSO, è una CONSTATAZIONE.** *«`psi` è diverso»* non dice
> *«meglio»*. ### **Il criterio di successo è `C`: i flash vanno a zero.** E `A` è il criterio che
> **impedisce** di aver rotto il resto.

## 2.3 — Il numero di nascite: **si riporta**

Con la decisione invariata **mi aspetto che sia identico**, e ### **se NON lo è, non è un successo
né un fallimento: è il segnale che ho toccato la decisione senza volerlo** — e allora **mi fermo**.

---

# 3. TODO DEL NEXT STEP

| | |
|---|---|
| ☐ | **passo 0**: una scena con nascite, e **quanti passi** servono. **È il passo che decide se il resto è possibile** |
| ☐ | **passo 1**: chi dipende dal flash; `:6506`/`:6507` sugli indici ripetuti |
| ☐ | **commit del passo 0-1** *(solo misure, nessun codice)*, poi valutare se fermarsi |
| ☐ | **passo 2-3**: il confine dell'evento atomico e l'estensione di `psi`/`psi_spin` |
| ☐ | **commit del codice**, col blob prima → dopo |
| ☐ | **passo 4**: il sigillo a cinque bracci, **commit a sé** *(par.5)*, poi ### **STOP** |
