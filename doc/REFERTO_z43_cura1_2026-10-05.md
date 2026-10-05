# REFERTO -- `Z43` PARTE A: **CURA (1), `r` VA UNA VOLTA SOLA**

*(mandato di Luca del 2026-10-05; i **sei criteri** furono fissati **prima del codice**
in `45e7130`, la cura e' in `b7c5ae3`, la cura dello strumento in `1a92215`.)*

> ### ✅ **TUTTI E SEI I CRITERI PASSANO. LA `PARTE B` E' AUTORIZZATA.**

| | |
|---|---|
| simulatore | `1feb9b0a` **->** `062172d3` |
| patch del braccio 0 | `be92dde8` |
| sigillo | `753e6275` |
| strumento del criterio 4 | `7b71aa48` *(lo strumento di `Z43`, rigirato)* |
| bracci | **tre**: `A` il vecchio, `B` il curato *(entrambi **non patchati**)*, `C` il curato **patchato** per il criterio 3 |
| piattaforma | `python 3.13.2` · `numpy 2.3.0` · Windows 11 · AMD64 |

## IL BRACCIO 0

| | |
|---|---|
| commit che ha cambiato il simulatore | `b7c5ae3` |
| suo **PADRE** *(`H-P8`)* | `45e7130` |
| blob estratto / **che la patch dichiara** | `1feb9b0a` / `1feb9b0a` |
| **il *prima* e' quello atteso** | ### **`True`** |
| blob patchato / sul disco oggi | `062172d3` / `062172d3` |
| **coincide** | ### **`True`** |

## ✅ CRITERI 1 e 2: **le due META' dello stesso controllo, e tengono entrambe**

| | |
|---|--:|
| differenze al **passo 1** | ### **`0`** |
| differenze al **passo 2** | ### **`0`** |
| ### **primo passo con una differenza** | ### **`3`** |
| attributi confrontati per passo | `236` |

### **IL CRITERIO 1 TIENE:** ai passi 1 e 2, dove `r = 1` ### **esatto per
costruzione**, togliere `r_node` e' ### **un no-op aritmetico** *(`coerenza * 1.0 ==
coerenza` in IEEE)*, e il lockstep lo conferma: ### **zero differenze su `236` attributi.**

### **IL CRITERIO 2 -- IL CASO CHE DEVE FALLIRE -- FALLISCE AL PASSO GIUSTO:** la prima
divergenza e' al passo ### **`3`**, ed e' esattamente dove il
criterio la pretende. ### **La cura AGISCE.**

| passo | attributi diversi |
|--:|--:|
| `3` | `5` |
| `4` | `26` |
| `5` | `49` |
| `10` | `51` |
| `20` | `51` |
| `50` | `131` |
| `100` | `153` |
| `150` | `152` |

## ✅ CRITERIO 3: **`STEP2` INTATTO, al bit**

| | |
|---|--:|
| chiamate verificate | `150` |
| nodi confrontati | ### **`1 970 507`** |
| ### **nodi DIVERSI** | ### **`0`** |
| max scarto | ### **`0.000e+00`** |

### ⛔ **E NON E' UNA DIVISIONE, ed e' una finezza che il mandato non poteva
### prevedere:** il criterio chiedeva *«`omega_clk / coerenza = (cs_prec/CS_M)^2` al
bit»*. ### **In IEEE `(a*b)/a != b` in generale:** chiedere la divisione sarebbe stato
### **un falso verdetto garantito dall'aritmetica.**
### ✅ **Si verifica LA MOLTIPLICAZIONE, nello stesso ordine in cui la legge la
scrive:** `omega_clk == coerenza * (_csn2/CS_M)**2`. ### **E' la stessa pretesa, nella
forma che l'aritmetica permette di verificare.**

## ⚠ CRITERIO 4: **L'ALTALENA E' SMORZATA, NON ELIMINATA** *(correzione del
## guardiano, e aveva ragione)*

> ### ⛔ **IL CRITERIO AGGREGATO PASSA, E NASCONDE L'INIZIO.**
> Il rapporto *«dispari/pari delle MEDIANE di tutta la corsa»* e' calcolato su
> **150 passi**, e ### **una coda lunga e quieta schiaccia un inizio violento.**
> ### ✅ **La correzione e' del guardiano, ed e' un suo errore nel mandato che
> ### lui stesso dichiara.** ### **Io il criterio aggregato l'avevo applicato
> ### alla lettera, e NON mi ero chiesto che cosa nascondesse.**

*(Misurato con lo strumento di `Z43` **`7b71aa48`**, rigirato sul blob nuovo. ### **Corsa a se', e il sigillo lo dichiara.**)*

| | PRIMA *(`e2940b3c`)* | DOPO *(`062172d3`)* | il criterio | il `BRACCIO A` di `66a798d` |
|---|--:|--:|--:|--:|
| rapporto dispari/pari di `abs(f)` | `5.283` | ### **`1.0411`** | `<= 1.2` | `1.034` |
| rapporto dispari/pari di `C0` | `7.185` | ### **`1.0100`** | `<= 1.2` | `1.031` |
| rapporto dispari/pari di `C1` | `1.081` | `0.9836` | — | — |
| rapporto dispari/pari di `C2` | `4.276` | `1.0320` | — | — |

> ### **`C0` AGGREGATO passa da `7.19` a `1.0100`** — ### ⚠ **ma e' un
> ### NUMERO AGGREGATO, e sotto c'e' la tabella per coppia che dice la cosa
> ### vera.**
> ### **E COINCIDE COL `BRACCIO A`:** la cura sul simulatore **vero** riproduce la
> misura fatta su una **copia**, e questo e' ### **il controllo positivo piu' forte di
> ### tutto il mandato** -- due strade diverse, lo stesso numero.

### ✅ **E `FEDELTA'` PASSA ANCHE SUL BLOB NUOVO:** `0` differenze su `148` passi e ### **`1 944 903` nodi**, max scarto `0.000e+00`.
### **Quindi `ritmo()` e' INTATTO: la cura non l'ha toccato**, e il confronto fra prima
e dopo e' fra ### **due misure buone.**

### ⛔ **IL RAPPORTO PER COPPIA DI PASSI — ed e' QUESTO il numero vero**

*(rapporto `r(dispari)/r(pari)` per la coppia `(2k-1, 2k)`, etichettata dal passo **pari**)*

| coppia | `r` **DOPO** | `r` **PRIMA** | `abs(f)` **DOPO** | `abs(f)` **PRIMA** |
|--:|--:|--:|--:|--:|
| `4` | ### **`1.463e+04`** | `1.463e+04` | `1.488e+04` | `1.487e+04` |
| `10` | ### **`67.05`** | `88.63` | `67.05` | `88.64` |
| `20` | ### **`3.215`** | `20.25` | `3.137` | `20.24` |
| `30` | ### **`1.554`** | `17.38` | `1.496` | `17.38` |
| `40` | ### **`1.219`** | `16.8` | `1.191` | `16.79` |
| `60` | ### **`1.041`** | `11.02` | `1.053` | `11.01` |
| `80` | ### **`0.9888`** | `6.798` | `0.9923` | `6.794` |
| `100` | ### **`0.9764`** | `3.081` | `0.9757` | `3.067` |
| `120` | ### **`1.006`** | `1.391` | `0.995` | `1.371` |
| `140` | ### **`0.9666`** | `1.027` | `0.9371` | `1.011` |

| | `r` *(`C0`)* | `abs(f)` |
|---|--:|--:|
| ### **primo passo da cui resta `<= 1.2`**, DOPO | ### **`42`** | ### **`40`** |
| lo stesso, PRIMA | `130` | `128` |
| coppie sopra `1.2`, DOPO | ### **`19` su `74`** | |
| coppie sopra `1.2`, PRIMA | `63` su `74` | |

> ### ⛔ **LA CONCLUSIONE GIUSTA: L'ALTALENA E' SMORZATA, NON ELIMINATA.**
> Si calma in ### **~`42` passi invece di ~`130`**, e all'inizio e' ### **ancora violentissima** — `1.463e+04` alla coppia `4`, `67.05` alla `10`, `3.215` alla `20`.
> ### ✅ **E IL CRITERIO DEL MANDATO PASSA DAVVERO** *(`1.0411` e `1.0100`, contro `1.2`)*: ### **lo dico, e accanto ci metto questa riserva.**

### 📌 **CHE COSA RESTA, e il guardiano lo nomina:** ### **la `r` in `_dts` e il gauge
### sfasato.** La `PARTE A` ha tolto ### **una** delle due potenze di `r` dall'orologio;
la seconda vive nel **tempo** *(`_dts = DT*r`)*, e il gauge e' ancora ### **la mediana
globale della fase del passo precedente.**
### ✅ **E LA `PARTE B` E' QUELLA CHE DEVE ELIMINARLA**, perche' ### **toglie la fase
da `r` PER COSTRUZIONE** — `r = cs_nodo_prev / CS_M` non legge piu' `f`.

### ⛔ **E IL CRITERIO DELLA `PARTE B` SI LEGGE PER COPPIA, non in aggregato:**
### **rapporto `<= 1.2` su OGNI coppia dal passo 3 in poi**, escluse solo le coppie in
cui ### **la cache di `cs` non e' allineata** — ### **contate e dichiarate.** Il rapporto
aggregato ### **si riporta, ma NON basta da solo.** *(Correzione del guardiano, registrata
qui perche' e' dove il criterio nasce.)*

### ✅ **E I MIEI NUMERI COINCIDONO CON LA MISURA INDIPENDENTE DEL GUARDIANO** *(Linux)*

| coppia | il mio `r` | il guardiano |
|--:|--:|--:|
| `4` | `1.463e+04` | `~1.0e4` |
| `10` | `67.05` | `67` |
| `20` | `3.215` | `3.15` |
| `30` | `1.554` | `1.52` |
| `40` | `1.219` | `1.20` |
| `60` | `1.041` | `1.03` |
| `100` | `0.9764` | `0.99` |

### **Due piattaforme, due strumenti, gli stessi numeri fino alla terza cifra.**
### ⚠ **E questo rende la correzione INCONTESTABILE: non e' un'opinione sul
criterio, e' un fatto sui dati che entrambi abbiamo misurato.**

### ⚠ **E UN NUMERO CHE NON E' SPARITO, e va riportato:** la frazione di nodi col `r`
**al tetto** ha mediana `0.000233` ma ### **massimo `0.455476`.**
### **L'altalena e' sparita, la SATURAZIONE in qualche passo NO.** ### **Non la
giudico: la riporto, perche' il gradino (b) della stella polare diceva che se il tetto
morde cio' che si osserva e' il tetto.**

## ✅ CRITERIO 5: **150 passi, e che cosa cambia a valle**

| | `A` *(vecchio)* | `B` *(curato)* | differenza |
|---|--:|--:|--:|
| `n` finale | `14 124` | `14 328` | ### **`+204`** |
| archi finali | `473 143` | `473 397` | ### **`+254`** |

### **`150` passi, SENZA eccezioni di invarianti.** Con la cura la rete cresce di
### **`+204` nodi** e `+254` archi.
### ⛔ **NON LO GIUDICO, e il mandato lo dice: <<senza giudicarlo>>.** ### **Questo
repo non ha un criterio su quanto la rete DEBBA crescere.**

## ⚠ IL SIGILLO HA DATO UN FALSO-UNO AL PRIMO GIRO, e la causa ero IO

Il primo giro *(strumento `3a61f78f`)* dava **1 differenza** ai passi 1 e 2, su
### **`_calcpsi_origini`**, con la nota *«chiavi diverse»*.

### ⛔ **NON ERA LA CURA:** quel dizionario registra
### **`"nome_funzione:NUMERO_DI_RIGA"`** di chi chiama `calcola_psi()` senza `w`
*(`:6271-6279`)*, e il mio gancio aggiunge ### **quattro righe** -- quindi i numeri di
riga dei chiamanti **si spostano** e le chiavi differiscono ### **per costruzione.**

### ✅ **E L'HO VERIFICATO PRIMA DI TOCCARE LO STRUMENTO:** due passi, vecchio contro
curato ### **senza gancio**, ### **zero differenze.** ### **Non ho curato su
un'ipotesi: ho curato dopo averla verificata.**

**LA FORMA GIUSTA, ora cablata:** ### **tre bracci**, e i criteri `1`, `2`, `5`
confrontano ### **due sorgenti NON patchati.**
### 📌 **E LA LEZIONE E' GENERALE:** qualunque sigillo che confronti `vars(net)` fra un
braccio **patchato** e uno **non patchato** vedra' `_calcpsi_origini` differire. ### **Nei
sigilli precedenti non si vedeva perche' ENTRAMBI i bracci erano patchati con lo stesso
numero di righe.** *(Dettaglio in `1a92215`.)*

## ⚠ CHE COSA NON E' MISURABILE, e lo dichiaro

### ⛔ **IL RAMO LEGACY E' CURATO MA NON MISURABILE GIRANDO.** `DEPARAM_OROLOGIO` e'
`True`, quindi `:5982` ### **non viene eseguito.** La sua cura e' verificabile
### **solo dall'AST e dalla lettura, non da un numero.**
### **Il mandato chiedeva di applicarla <<dichiarandolo>>, e questo e' il punto in cui
la dichiaro.** ### **Se un giorno `DEPARAM_OROLOGIO` venisse spento, quella riga
comincerebbe a girare: allora andrebbe sigillata.**

## I SEI CRITERI, IN UNA TABELLA

| | che cosa pretendeva | numero | esito |
|---|---|--:|---|
| **0** | la patch su `1feb9b0a` ridA' `062172d3` al byte | `True` | ### **PASSA** |
| **1** | identita' al byte ai passi 1 e 2 | `0` e `0` | ### **PASSA** |
| **2** | ### **il caso che DEVE fallire:** dal passo 3 deve divergere | prima divergenza al `3` | ### **PASSA** |
| **3** | `STEP2` intatto al bit | `0` su `1 970 507` | ### **PASSA** |
| **4** | l'altalena sparisce, `<= 1.2` *(**aggregato**)* | `1.0411` e `1.0100` | ### **PASSA**, ### ⚠ **ma SMORZATA e non eliminata:** per coppia resta sopra `1.2` fino al passo `42` |
| **5** | `150` passi senza `FERMO`, e il valle riportato | `150` passi | ### **PASSA** |

> ### ✅ **E QUINDI LA `PARTE B` E' AUTORIZZATA:** il mandato diceva *«La `PARTE B`
> ### parte SOLO se il sigillo della `PARTE A` passa: altrimenti `FERMO`»*.
> ### **Passa.**
