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

---

# ✅ **LE TRE CORREZIONI DEL GUARDIANO, e le misure dei passi 0-1** *(annotazione del 2026-09-28)*

> **Piano approvato nella sostanza** *(perimetro dopo il `return`, decisione invariata in questo
> pezzo)*. ### **Le sezioni sopra NON sono riscritte: qui sotto ci sono le correzioni e i numeri.**

## ✗ **Correzione 1 — `psi`/`psi_spin` dei nati: NIENTE forma 3**

**Quello che avevo scritto** *(par.1.3)*: *«forma **7** per il valore di partenza, forma **3** per il
ricalcolo dei soli nati»*. ### **La forma 3 è sbagliata**, e la ragione è quella che la cura combatte:

> Un ricalcolo **a metà passo** leggerebbe **il grafo DOPO la mitosi**. ### **È di nuovo una lettura
> mista.** Il nato **EREDITA** dai genitori *(forma **7**)*, e **il valore vero arriva al passo dopo**,
> dal ricalcolo normale di `step`.

### ➜ **E la REGOLA di eredità la PROPONGO, non la scelgo.** Le tre che il codice già usa alla nascita:

| | regola | chi la usa già alla nascita | conseguenza su `psi` |
|---|---|---|---|
| **(a)** | ### **media dei genitori** `0.5·(psi[a] + psi[b])` | `phivel` *(`:6469`)*, e **`phi` del figlio è `fm`, la fase MEDIA** | **coerente con `fm`**. ⚠ Somma **complessa**: genitori in antifase danno un figlio con `\|psi\| ≈ 0` — che è **interferenza distruttiva**, cioè fisica, non un errore |
| **(b)** | **eredità da un genitore** `psi[a]` | `phi_s`, `perc_chi`, `perc_geom` *(`:6468`, `:6473`, `:6476`)* | **rompe la simmetria** fra i due genitori: `a` e `b` non sono interscambiabili |
| **(c)** | **zero** | `eta`, `tw`, `perc_tw` *(`:6470`, `:6558`, `:6484`)* | il nato è **invisibile al campo** per un passo |

### **La mia raccomandazione: (a) per `psi`, e (b) per `psi_spin`** — e l'asimmetria ha una ragione,
non è una svista: ### **il compagno di `psi` è `phi`, che alla nascita prende la MEDIA (`fm`); il
compagno di `psi_spin` è `phi_s`, che alla nascita EREDITA da `a`.** **Dare a ciascuno la regola del
proprio compagno è l'unica scelta che non aggiunge una convenzione nuova** *(`9-ter`)*.
### ⚠ **Ma è una PROPOSTA: decide Luca.**

## ✅ **Correzione 2 — il criterio `C` passa per costruzione: serve il FENOMENO**

**Aveva ragione:** *«`calcola_psi` chiamata zero volte»* è ### **una tautologia** — se estendo `psi`
la guardia non scatta **per costruzione**, e un criterio che non può fallire non misura nulla
*(`A9`)*. **Il criterio nuovo, e sostituisce `C`:**

| | ### **`C-bis`, IL FENOMENO** |
|---|---|
| **cosa** | il **salto locale** di `mean(phi_g)` al passo di nascita **rispetto ai due passi vicini** |
| **oggi** | ### **`2.631×` su `phi_g`, cioè `1.622×` su `\|psi\|`** *(riprodotto dai fotogrammi: `138.68 → 366.17 → 139.72` ai passi 40/42/44)* |
| **dopo** | ### **`≈ 1.0`** |
| **il caso che DEVE fallire** | ### **sul blob VECCHIO il salto DEVE vedersi.** Senza, `C-bis` non distingue la cura da niente |

## ✅ **Correzione 3 — la scena: quella del video, e non se ne cerca un'altra**

**Accettato, e ho cancellato la sonda che cercava scene.** ### **La finestra è il passo 42 coi vicini
40 e 44**, e le misure qui sotto dicono **perché deve essere quella e non un'altra.**

---

# 📏 **LE MISURE DEI PASSI 0-1**
*(`csv/_test_fork/_flash_passo01.py`, **sola lettura**: AST + i 61 fotogrammi locali del pilota)*

## ① ### **IL FLASH SMETTE, ed è il fatto che nessuno aveva**

| passi col flash | ### **SOLO `2`, `42`, `58`, `62`, `68`** |
|---|---|
| passi con nascite | ### **dal 42 al 120, QUASI TUTTI** — e dal 70 in poi **ogni** fotogramma, fino a **`+56` nodi ogni due passi** |
| il salto dal passo 70 al 120 | ### **`1.000`** |

> ### 📌 **La spiegazione candidata non è «il flash sparisce»: è «il flash diventa la NORMA».**
> Quando **ogni** passo ha nascite, **ogni** passo ricalcola, e ### **non esiste più un passo vicino
> NON ricalcolato con cui fare il rapporto.** **Sparisce il CONTRASTO, non il meccanismo.**
>
> ### ➜ **E questo è il motivo per cui la finestra del passo 42 è OBBLIGATORIA:** è l'unica in cui i
> vicini sono passi **senza** nascite. **La prescrizione del guardiano non è una comodità: è la sola
> finestra in cui il fenomeno è misurabile.**

## ② **I casi «nascite ma nessun flash» hanno un'ipotesi nuova**

I fotogrammi sono **ogni due passi**: un `dn > 0` fra `k−2` e `k` **non dice** se la nascita è al
passo `k−1` o al passo `k`. Se il flash dura **un solo passo** — e il meccanismo lo prevede, perché
al passo dopo `len(psi) == n` — ### **una nascita al passo DISPARI ha il flash al passo DISPARI, che
non è fotografato.**
### ⚠ **NON è dimostrato, e la granularità non permette di dimostrarlo:** serve un run che guardi
**ogni** passo. **Ma è l'ipotesi che mancava**, e sostituisce quella caduta *(«ha ricalcolato l'altro
sito»)*.

## ③ ⚠ **I siti sono SETTE, non otto — e DUE sono raggiungibili dopo `mitosi`, non uno**

**Avevo contato `calcola_psi` stessa: è il BERSAGLIO, non una guardia.** E dei 7:

| | |
|---|---|
| ### **`:6821` in `memoria_hebbiana_moto`** | raggiungibile dopo `mitosi` — **è quello che la voce conosceva** |
| ### **`:3256` in `lambda_nodi`** | ### **raggiungibile dopo `mitosi`, e la voce NON lo aveva** |

### ➜ **Quale dei due arriva PRIMO è da verificare**, e cambia dove scatta il flash.

## ④ ### **I fotogrammi NON permettono di ripartire**

Contengono `pos`, `phi`, `phi_g`, `dpozzo`, `ii`, `jj`, `n`, `na`, `dphi`, `blob`, `seme`, `passo`.
### **Mancano `d`, `d0`, `vd`, `peq`, `tw`, `twp`, `psi`, `psi_spin`, `eta`, `phivel`.**

> ### ➜ **Quindi il sigillo deve RIFARE il run fino al passo 44, su DUE blob.** Il costo, **dal
> registro del run che li ha prodotti** *(avvio `10:46:43`, chiuso `11:29:11`, 4 semi in parallelo,
> 120 passi)*: ### **~21 s per passo su un seme → ~15 minuti per braccio, ~30 minuti in tutto.**
> ### **È UN RUN LUNGO, e come tale lo decide Luca.**

## ⑤ **Il rinculo a indici ripetuti: voce `RINCULO-RIPETUTI`, e NON si corregge qui**

**Il mio «non so» n. 5 è confermato fondato dal guardiano** — non da una mia misura. **Perché morda
servono DUE archi che si dividono nello stesso passo e condividono un nodo:** con una sola divisione
`a` e `b` sono distinti e ### **al passo 42 NON morde.** **Ma il caso esiste:** dal passo 70 al 120 le
nascite sono **decine** per fotogramma, quindi divisioni che condividono un nodo sono **attese**.
### **Voce a sé, fuori da questo sigillo, per decisione di Luca.**

---

# 🔁 **IL TODO, AGGIORNATO**

| | |
|---|---|
| ☑ | passo 0: la scena è prescritta, la finestra è il passo 42, **e ora si sa perché deve essere quella** |
| ☑ | passo 1: i siti *(7, due dopo `mitosi`)* e il rinculo *(voce `RINCULO-RIPETUTI`)* |
| ☐ | ### **la REGOLA DI EREDITÀ: aspetta Luca** *(proposta: (a) per `psi`, (b) per `psi_spin`)* |
| ☐ | ### **il RUN LUNGO del sigillo (~30 min): aspetta Luca** |
| ☐ | poi il confine dell'evento atomico, il codice, il sigillo |
