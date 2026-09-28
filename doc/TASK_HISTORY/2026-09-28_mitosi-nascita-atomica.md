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

---

# ✗ **CORREZIONE: ho letto RAPPORTI dove contava il LIVELLO** *(annotazione del 2026-09-28)*

> **Rilievo del guardiano:** *«leggi la TUA tabella per livelli, non per rapporti: dal passo 62
> `mean(phi_g)` resta stabilmente al livello del flash (~340, e scende a 215 al passo 120) contro
> ~135 del regime senza nascite. Il flash NON smette: diventa lo stato permanente.»*
> ### **Aveva ragione, e l'errore è nello STRUMENTO che ho scritto io:** il rapporto coi vicini è
> **cieco a uno spostamento di livello** — se anche i vicini sono alti, il rapporto fa `1.000` mentre
> il campo è **permanentemente gonfiato**.

## I numeri, per LIVELLO *(generati, `csv/_test_fork/_flash_passo01.py`)*

**Riferimento: il regime SENZA nascite, passi `4`–`40`: `mean(phi_g) = 130.22`.**

| passo | `n` | `mean(phi_g)` | **su base** | **su `\|psi\|`** |
|---|---|---|---|---|
| 40 | 12802 | 138.68 | 1.065 | 1.032 |
| ### 42 | 12803 | ### 366.17 | ### **2.812** | ### **1.677** |
| 44 | 12803 | 139.72 | 1.073 | 1.036 |
| 58 | 12805 | 352.94 | 2.710 | 1.646 |
| ### 60 | 12806 | ### 118.26 | ### **0.908** | 0.953 |
| 62 | 12811 | 346.58 | 2.662 | 1.631 |
| ### 66 | 12816 | ### 113.28 | ### **0.870** | 0.933 |
| 68 | 12822 | 333.97 | 2.565 | 1.601 |
| 80 | 12879 | 292.44 | 2.246 | 1.499 |
| 100 | 13090 | 233.24 | 1.791 | 1.338 |
| ### 120 | 13444 | ### 215.02 | ### **1.651** | ### **1.285** |

### ➜ **Dal passo 62 al 120 il livello medio è `1.994×` la base, cioè `1.412×` su `|psi|`. E al passo
120 è ancora `1.651×`: NON TORNA GIÙ.**

> ### 📌 **Il flash non è un picco: è una TRANSIZIONE DI STATO.** Fino al passo 56 il sistema torna
> sempre a ~`135`; nella finestra `58`–`68` **alterna** fra il livello alto (~`2.6×`) e uno
> **leggermente SOTTO** la base (`0.87`–`0.91×`); dal `68` in poi ### **resta sul livello alto e
> decade lentamente senza mai tornare.**
> **L'alternanza sotto/sopra è un fatto nuovo che nessuna delle due ipotesi precedenti spiega**, né
> la mia *(parità dei fotogrammi)* né quella caduta.

**⚠ E una cosa che NON ho verificato, e la voce `PSI-FLASH` fa la stessa assunzione:** il passaggio
`2.6 → 1.6` assume che **`pozzo_grafo` sia LINEARE in `I = |psi|²`**. ### **Va verificato, non
ereditato.**

---

# ✗ **CORREZIONE: la scena del video è `sep = 6.1158`, non `3.0`**

**Cercando di riprodurre la finestra del passo 42 ho trovato una discrepanza:** i fotogrammi dicono
`n = 12802`, e la scena che costruivo io dava ### **`n = 2107`** — con la **stessa** chiamata
`avvia_test("MASSE-COERENTI")`.

| | |
|---|---|
| **la causa** | ### **scrivevo `sep = 3.0` A MANO.** Il pilota fa `float(getattr(a, "sep", 3.0))`, e il driver passa ### **`--sep 6.1158`**. E `nmasse` non è 2 ma ### **3** *(`max(2, a.nmasse)`)* |
| **la verifica** | con `sep = 6.1158`: ### **`n = 12802` esatto**, `m = 471564` archi |
| **il falso allarme che ho evitato** | avevo già scritto che *«la scena del video non è riproducibile sul blob di oggi»*. ### **È FALSO:** costruita sul blob `e203f9a8` **e** su quello di oggi dà **`2107` in entrambi**, quindi non era il simulatore. **Era il mio `sep`** |

> ### 📌 **La lezione, e vale oltre questo caso:** ### **un parametro di scena scritto a mano è la
> stessa famiglia di `H-P3`** — *«non configurare il modulo a mano, passa dal CLI»*. **I sigilli
> precedenti usavano `sep = 3.0` per una scena PICCOLA di proposito**, e ho ricopiato quel valore
> dentro una misura che aveva bisogno della scena GRANDE. ### **Da qui in poi `nmasse` e `sep` si
> leggono da `a`, come fa il pilota.**

**E questo spiega i «40 passi con zero nascite»:** erano sulla scena **piccola** *(`2107` nodi)*.
### **La scena del video ha `12802` nodi e partorisce al passo 42.**

**Costo confermato:** `471564` archi contro i `70199` della scena piccola. Dal registro del run che
ha prodotto i fotogrammi: ### **~21 s per passo → ~15 min per arrivare al passo 44.**

---

# 🔬 **LA SCOMPOSIZIONE DEL FATTORE: i criteri, FISSATI PRIMA DEI NUMERI**

> **Mandato:** *«ψ ricalcolato subito prima e subito dopo mitosi, sostituendo UN ingrediente alla
> volta (`w`, `_mat(w)`, `φ`, archi e nodi del nato) per identificare quale produce il 2.6×. Se il
> fattore viene da uno stato a metà costruzione, dillo: cambia la forma della cura.»*

## Le due formule, lette dal codice — e **una differenza che va guardata per prima**

```
calcola_psi :4250-4251   amp = SCALA_AMP
                         F = self._mat(w) @ (amp * np.exp(1j * self.phi))
step        :5750-5753   Mw = self._mat(w)
                         F = Mw @ np.exp(1j * self.phi)
```

### ⚠ **`calcola_psi` moltiplica per `SCALA_AMP`, `step` NO.** `SCALA_AMP = 1.0` di default
*(`:301`)* e vale `sqrt(SCALA_B)` — ### **quindi se il driver non cambia `SCALA_B` è inerte, ma va
LETTO E RIPORTATO prima di tutto il resto**: se non fosse `1.0`, spiegherebbe il fattore da solo e
la scomposizione andrebbe riletta.

## Gli ingredienti, e come si sostituiscono senza barare sulle DIMENSIONI

**Il problema:** prima della mitosi il grafo ha `m` archi e `n` nodi, dopo `m+1` e `n+1`.
### **Quindi «sostituire un ingrediente» non è sempre definito**, e lo dichiaro invece di far finta.
**La misura si fa sui NODI VECCHI e sugli ARCHI SOPRAVVISSUTI** *(`keep`)*, così ogni variante ha le
stesse dimensioni:

| | variante | che cosa isola |
|---|---|---|
| **V0** | `w` pre · `φ` pre · struttura pre | ### **deve coincidere con `psi` di `step`**: se no, il banco è rotto |
| **V1** | ### **`w` POST** · `φ` pre · struttura pre | i **pesi**: `d` cambiata dalla mitosi e dal rilassamento, `eta` incrementata |
| **V2** | `w` pre · ### **`φ` POST** · struttura pre | la **fase**: il **rinculo dei genitori** |
| **V3** | `w` pre · `φ` pre · ### **struttura POST** *(ristretta a `keep`)* | la **matrice**: la cache `_S`/`_perm` |
| **V4** | tutto POST, **ma senza il nodo e gli archi nati** | ### **l'interazione** fra i tre |
| **V5** | tutto POST, **col nato** | ### **il valore del flash**: deve riprodurre `366.17` |

## ### **I CRITERI, e sono fissati ORA**

| | |
|---|---|
| ### **①** | un ingrediente è ### **LA CAUSA** se da solo porta `mean\|psi\|` sui nodi vecchi a ### **≥ 1.30×** di `V0`, **e gli altri due restano sotto `1.10×`** |
| ### **②** | se ### **nessuno** arriva a `1.30×` ma `V4` sì, la causa è ### **un'INTERAZIONE**, e lo dico invece di attribuirla a uno |
| ### **③** | se il fattore compare ### **solo in `V5`** *(cioè solo col nato dentro)*, allora **un nodo su 12802 muove il campo di tutti** — e ### **quella è la cosa che il guardiano dice essere impossibile a stato coerente**: allora il fattore viene da ### **uno stato a METÀ COSTRUZIONE**, e ### **CAMBIA LA FORMA DELLA CURA** |
| ### **④** | se `V0` ### **non coincide** con `psi` di `step` entro `1e-12` relativo, ### **MI FERMO**: il banco non misura ciò che dice |
| ### **⑤** | `SCALA_AMP` ### **si riporta come primo numero.** Se `≠ 1.0`, tutto il resto si rilegge |

**E una lettura in più che costa zero:** ### **`pozzo_grafo` è lineare in `I`?** Si verifica
chiamandolo su `I` e su `2·I` e guardando se `phi_g` raddoppia. ### **Serve a sapere se il `2.6` su
`phi_g` è davvero `1.62` su `|psi|`** — l'assunzione che io e la voce abbiamo ereditato senza
verificare.

---

# 🔬 **I NUMERI DELLA SCOMPOSIZIONE** *(2026-09-28)* — ### **`V5` passa, il CRITERIO ④ FALLISCE**

## ✅ `V5`: **ordine e scena sono quelli dei fotogrammi**

| passo | atteso *(fotogrammi)* | ottenuto | |
|---|---|---|---|
| 38 | — | `138.6407` | |
| **40** | **`138.68`** | ### **`138.6832`** | ### **PASSA** |
| **42** | **`366.17`** | ### **`366.1746`** | ### **PASSA** |

### **E la prima nascita è al passo 42**, `n 12802 → 12803`, come i fotogrammi. Il ripiego usa
**l'ordine di oggi** su un blob di ieri, e riprodurre quei numeri è **la prova che ordine e scena
sono i loro.** *(311 s per arrivarci.)*

## ✅ **Punto ② del guardiano: il flash c'è ANCORA sul blob di oggi, identico**

**I due referti differiscono in TRE righe, e sono il nome del simulatore, la riga dell'esecutore e
un secondo di cronometro.** ### **Tutti i numeri di fisica sono identici all'ultima cifra.**

| | blob **vecchio** `e203f9a8` | blob **di oggi** `05691d41` |
|---|---|---|
| esecutore | **assente** → ripiego | **`esegui_passo`** |
| passo 40 | `138.6832` | ### **`138.6832`** |
| passo 42 | `366.1746` | ### **`366.1746`** |
| prima nascita | passo **42** | passo **42** |

> ### 📌 **Quindi il flash non è stato toccato da nessuna delle cure di oggi** — `MAX-NODI-FERMA`,
> `L_CONSERVA`, `SYNC_UPDATE`, i pavimenti: ### **sulla scena grande sono byte-inerti anche qui.**
> **Ed è anche la prova che il ripiego pre-`T1` riproduce il passo di allora**, perché i due blob,
> per strade diverse, danno lo stesso stato.

## ⛔ **IL CRITERIO ④ FALLISCE, e i numeri della scomposizione NON VALGONO**

| | `mean\|psi\|` sui 12802 nodi vecchi |
|---|---|
| **P0** — `psi` che `step` ha lasciato | `1.544777` |
| **V0** — **il mio ricalcolo sullo STATO PRE** | ### **`1.082039`** |
| **rapporto** | ### **`0.700450`** — e doveva essere `1.000000` entro `1e-9` |

### ➜ **Il banco NON riproduce il `psi` di `step`, quindi non misura ciò che dice.** Il criterio ④
diceva *«se `V0` non coincide, MI FERMO»*, ed è quello che faccio. **I numeri qui sotto si
riportano, e NON si interpretano:**

| | | |
|---|---|---|
| **P5** ricalcolo POST completo | `1.477078` | `0.9562 × P0` |
| **Pw** pesi dei sopravvissuti al PRE | `1.073072` | `0.6946 × P0` |
| **Pf** fase dei nodi vecchi al PRE | `1.477104` | `0.9562 × P0` |
| **Pn** archi del nato a peso zero | `1.477078` | `0.9562 × P0` |

## ⚠ **DUE DIFETTI DEL BANCO, e sono miei**

### **① Il banco misura L'ISTANTE SBAGLIATO.**

`P0` e le varianti stanno **al confine della mitosi**. Il flash — `366.17` — è misurato **alla fine
del passo**, dopo che `rilassa_disegno` e `memoria_hebbiana_moto` hanno girato. ### **Sono due
istanti diversi**, e infatti `P5` dà `0.96 × P0` mentre `phi_g` salta di `2.64×`: **non possono
riferirsi allo stesso `psi`.**

> ### 📌 **E questo RESTRINGE dove sta il flash:** se al confine della mitosi `mean|psi|` non si
> muove, ### **il salto nasce DOPO**, nel ricalcolo che una legge successiva fa — e `PSI-FLASH`
> indica proprio `:6821` in `memoria_hebbiana_moto`. **Non è una conclusione: è dove guardare.**

### **② Il rapporto `0.700` è il numero più interessante del giro, e non so ancora di chi sia.**

**Due candidati, e nessuno dei due è dimostrato:**

| | candidato |
|---|---|
| **(i)** | ### **`eta`.** `step` fa `w = self._pesi(); self.eta += dt_n` — **prima calcola i pesi, POI incrementa l'età.** Un `_pesi()` rifatto dopo `step` usa `eta + dt`, quindi un `ramp` diverso, quindi **pesi diversi**. Se è questo, ### **`calcola_psi(w=None)` NON PUÒ MAI riprodurre il `psi` di `step`** — e la «lettura mista» non è solo su `d`: è **anche su `eta`** |
| **(ii)** | **il mio banco**: chiamo `net._grado()` e forzo `net._S = None` per ricostruire la struttura. Se `satura` o `_pesi` dipendono da `_deg`, l'ho spostato io |

### **Non scelgo fra i due: la distinzione è UNA misura, e va fatta prima di qualunque cura.**

## 🗒 Due cose di forma, dichiarate

| | |
|---|---|
| **①** | **i due run hanno scritto sullo STESSO `.json`**, quindi quello committato è ### **l'ultimo, cioè il blob di oggi.** I due `.txt` sono entrambi committati e sono il record. **È un difetto del banco**: l'uscita deve dipendere dal blob |
| **②** | **la copia resta un debito:** `_flash_scomposizione_copia.py` si fonde con `_flash_scomposizione.py` appena i due processi bloccati sono chiusi |
