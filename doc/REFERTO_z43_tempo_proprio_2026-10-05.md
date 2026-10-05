# REFERTO -- `Z43`, PASSO (1): **LA DEFINIZIONE DEL TEMPO PROPRIO `r`**

*(mandato di Luca del 2026-10-05, sul blob **`e2940b3c`**; `LA STELLA
POLARE`, i controlli e le due previsioni sono in
`doc/TASK_HISTORY/2026-10-05_z43-definizione-tempo-proprio-misura.md`, committato
**prima** in `12ab7f4`; lo strumento in `d190dd5`.)*

> ### ⛔ **E' UNA MISURA, NON UNA CURA.** Il simulatore **non e' stato toccato**, e
> ### **nessuna legge nuova e' scritta: la forma la decide Luca.** Le sei vie sono
> ### riportate **tutte**, e **nessuna e' scelta.**

| | |
|---|---|
| simulatore | `e2940b3c` *(non toccato)* |
| strumento | `c5ab986a` |
| copia patchata | `7dd1e336`, **4 ancore** |
| copia `BRACCIO A` | `2fb32f5f`, **5 ancore** |
| scena | `--nmasse 3 --sep 6.1158`, seme `11`, **150** passi |
| configurazione | **`81`** booleani, ### **`ZERO` differenze dal driver** |
| piattaforma | `python 3.13.2` · `numpy 2.3.0` · Windows 11 · AMD64 |

## IL CONTROLLO CHE RENDE LEGGIBILE TUTTO IL RESTO: `FEDELTA'`

> ### ✅ **Il mio `C0` coincide AL BIT col `r` di `ritmo()` su `1 925 384` NODI, in `148` passi,
> ### con max scarto `0.000e+00`.**

**E i `2` passi saltati sono esattamente quelli
attesi:** i **rami di sicurezza** di `ritmo()` *(`_ritmo_sicurezza` al passo 1,
`_ritmo_med_assente` al passo 2)*, che tornano `np.ones` ### **senza passare dalla
formula**. ### **Lo strumento li riconosce DAI CONTATORI e non dal numero del passo**,
come il task history prescriveva.

### **PERCHE' QUESTO VIENE PRIMA DI TUTTO:** la formula che ricalcolo a lato
### **non e' una mia versione di `ritmo()`: E' `ritmo()`**, bit per bit. ### **Senza
questo, `C1`, `S1`, `V1` e `C6` sarebbero confronti con un modello MIO**, e il referto
non direbbe niente sul simulatore.

## L'ALTALENA: **riprodotta su Windows, e il fatto del guardiano TORNA**

| | |
|---|--:|
| mediana di `abs(f)` sui passi **DISPARI** | `3.0010e-02` |
| mediana di `abs(f)` sui passi **PARI** | `5.6808e-03` |
| ### **rapporto dispari/pari** | ### **`5.28`** |

**E L'ANDAMENTO, che e' cio' che conta** *(il rapporto fra passi consecutivi; dove e'
`< 1` il passo e' quello BASSO, e si riporta il reciproco)*:

| passo | `med|f|(k)/med|f|(k+1)` | il rapporto **alto/basso** | il guardiano, su Linux |
|--:|--:|--:|--:|
| `3` | `1.487e+04` | ### **`1.487e+04`** | `~1.5e4` |
| `20` | `4.556e-02` | ### **`2.195e+01`** | `~18` |
| `60` | `8.896e-02` | ### **`1.124e+01`** | `~10` |
| `100` | `3.322e-01` | ### **`3.011e+00`** | `~3` |
| `140` | `9.825e-01` | ### **`1.018e+00`** | `~1` |

> ### ✅ **IL FATTO DEL GUARDIANO E' RIPRODOTTO, e su un'ALTRA PIATTAFORMA.**
> Il task history aveva scritto, **prima di girare**, che *«il confronto che conta e' il
> RAPPORTO pari/dispari e il suo ANDAMENTO, non la terza cifra»*. ### **L'andamento
> coincide ordine per ordine: `1.5e4` -> `~20` -> `~11` -> `~3` -> `~1`.**

## ⛔ IL RISULTATO CENTRALE: **l'altalena NON e' nella ROTAZIONE, e' nella BASE**

> ### **Questo e' il numero che risponde alla domanda di `Z43`, e non me l'aspettavo
> ### cosi' netto.**

| | mediana sui passi | **dispari** | **pari** | ### **disp/pari** |
|---|--:|--:|--:|--:|
| `C0` -- il `r` di OGGI | `1.008e+00` | `1.400e+00` | `1.949e-01` | ### **`7.19`** |
| `C1` -- lo **SPOSTAMENTO DEL BLOCH** (Fubini-Study) | `1.412e-01` | `1.498e-01` | `1.386e-01` | ### **`1.08`** |
| `C2` -- la **fase globale** | `2.304e-02` | `2.996e-02` | `7.007e-03` | ### **`4.28`** |
| `C3` -- la fase della **componente 0** | `-1.309e-02` | `-2.652e-02` | `-2.869e-03` | ### **`9.24`** |
| `C3` -- la fase della **componente 1** | `-3.192e-02` | `-4.344e-02` | `-7.505e-03` | ### **`5.79`** |
| `S1` -- riferimento a **se stesso** | `4.150e-01` | `4.276e-01` | `4.002e-01` | ### **`1.07`** |
| `V1` -- riferimento ai **vicini** | `1.027e+00` | `1.030e+00` | `1.024e+00` | ### **`1.01`** |
| `C6` -- la via di `Z41` | `3.755e-02` | `1.567e-01` | `4.394e-03` | ### **`35.67`** |

> ### ⛔ **`C1`, L'ANGOLO INVARIANTE, HA UN RAPPORTO DI `1.08`: NON ALTERNA.**
> ### **Mentre `C0` alterna `7.19` e la fase della componente 0 alterna `9.24`.**

### **CHE COSA SIGNIFICA, detto senza interpretare oltre il numero**

`C1` misura **di quanto il VETTORE DI BLOCH si e' spostato** -- ### **NON l'angolo
di una rotazione** -- in modo indipendente dalla base
e dalla fase globale** *(e il collaudo lo verifica: una `SU(2)` comune lo lascia a
`3.75e-12`, e **`C3` invece cambia di `6.28e+02`**)*. `ritmo()` usa ### **la fase della
componente 0**, cioe' `C3`.

> ### **Lo SPOSTAMENTO DEL BLOCH non alterna** *(`1.08`)*.
> ### **Alterna cio' che `ritmo()` guarda: la fase di UNA componente, in UNA base** *(`9.24`)*,
> ### **e la fase globale** *(`4.28`)*.

### 📌 **E QUESTO E' ESATTAMENTE IL DIFETTO `(D3)` DEL MANDATO** -- *«dipende dalla
BASE dello spinore (componente 0) e contiene la fase globale»* -- ### **misurato invece
che argomentato.**

### ⚠ **CHE COSA QUESTO NON DICE, e va detto:** ### **non dice che `C1` sia il tempo
proprio.** Dice che ### **l'alternanza vive nella parte che `C1` scarta.** Se `r` fosse
definito da `C1`, l'alternanza **non ci sarebbe** -- ### **ma se `r` DEBBA essere `C1`
e' una decisione di Luca, non un risultato di questa misura.**

### ✅ **E DUE RISCONTRI INDIPENDENTI DICONO LA STESSA COSA**

| | |
|---|--:|
| `psi_spin`: distanza mediana a **1 passo** | `5.8988e-03` |
| `psi_spin`: distanza mediana a **2 passi** | `1.3767e-02` |
| ### rapporto **2 passi / 1 passo** | ### **`2.3339`** |

### **`2.33 > 1`: `psi_spin` NON TORNA
### INDIETRO.** Lo stato a `t` e' **piu' lontano** da quello a `t-2` che da quello a
`t-1`, cioe' ### **si allontana in modo monotono.** ### **Un'altalena DELLO STATO
darebbe un rapporto `<< 1`: non c'e'.** ### **E' coerente con `C1` che non alterna.**

| autocorrelazione a **ritardo 1** degli incrementi di fase *(componente 0)*, per nodo | |
|---|--:|
| nodi | `13 884` |
| mediana | `-0.0068` |
| `p5` / `p95` | `-0.0354` / `0.1531` |
| ### **frazione NEGATIVA** | ### **`0.8948`** |

### **Il `89.5%` dei nodi ha autocorrelazione NEGATIVA a ritardo 1**, che e' ### **la firma di un
periodo 2.** ### ⚠ **Ma la mediana e' `-0.0068`, cioe' PICCOLA in modulo:** l'alternanza e' ### **sistematica nel SEGNO e debole
nell'AMPIEZZA per nodo**, mentre e' **forte nella MEDIANA GLOBALE** *(`5.28`)*.
### 📌 **Le due cose insieme indicano un effetto COLLETTIVO, non per-nodo** -- ed e'
coerente col fatto che il gauge ### **E' una mediana GLOBALE** *(`(D2)`)*.

## ⛔ `BRACCIO A`: **LA MIA PREVISIONE ERA SBAGLIATA, e lo dico per primo**

> ### **Nel task history, PRIMA di girare, avevo scritto:** *<<mi aspetto che il
> ### rapporto CALI MA NON CROLLI, cioe' il terzo caso>>*, e avevo aggiunto *<<se mi
> ### sbaglio, lo scrivo>>*.
> ### ⛔ **MI SONO SBAGLIATO: IL RAPPORTO E' CROLLATO.**

| | PRINCIPALE | `BRACCIO A` |
|---|--:|--:|
| mediana di `abs(f)`, passi **dispari** | `3.0010e-02` | `1.7173e-02` |
| mediana di `abs(f)`, passi **pari** | `5.6808e-03` | `1.6603e-02` |
| ### **rapporto dispari/pari** | ### **`5.283`** | ### **`1.034`** |

**IL RAPPORTO ALTO/BASSO, passo per passo:**

| passo | PRINCIPALE | `BRACCIO A` |
|--:|--:|--:|
| `3` | `1.487e+04` | ### **`1.487e+04`** |
| `5` | `2.103e+02` | ### **`1.661e+02`** |
| `20` | `2.195e+01` | ### **`2.814e+00`** |
| `40` | `1.724e+01` | ### **`1.230e+00`** |
| `60` | `1.124e+01` | ### **`1.017e+00`** |
| `80` | `6.769e+00` | ### **`1.013e+00`** |
| `100` | `3.011e+00` | ### **`1.025e+00`** |
| `120` | `1.355e+00` | ### **`1.013e+00`** |
| `140` | `1.018e+00` | ### **`1.013e+00`** |

**E PER OGNI GRANDEZZA:**

| | PRINCIPALE | `BRACCIO A` |
|---|--:|--:|
| `C0` | `7.185` | ### **`1.031`** |
| `C1` | `1.081` | ### **`0.995`** |
| `C2_abs` | `4.276` | ### **`1.031`** |
| `C3_comp0` | `9.245` | ### **`1.133`** |
| `S1` | `1.068` | ### **`1.003`** |
| `V1` | `1.006` | ### **`1.000`** |
| `C6` | `35.670` | ### **`1.191`** |

> ### ✅ **E' IL PRIMO CASO DELLA TABELLA CHE AVEVO SCRITTO:** *<<il rapporto
> ### CROLLA verso `1` -> l'anello CONTRIBUISCE>>*. ### **E non solo contribuisce:
> ### `C0` passa da `7.19` a `1.031`, cioe' l'altalena SPARISCE.**

### ⛔ **PERCHE' IL MIO RAGIONAMENTO ERA SBAGLIATO, e vale piu' del numero**

Avevo scritto: *<<il gauge sfasato basta da solo a produrre periodo 2 -- se `f` e' alta,
il `med` del passo dopo e' alto, quindi `x = f/med` del passo dopo e' basso>>*.

> ### **LA MISURA DICE CHE NON BASTA.** Nel `BRACCIO A` il gauge sfasato e'
> ### **IDENTICO** -- non l'ho toccato -- e ### **l'altalena non c'e'.**
> ### **IL MIO ERRORE:** una retroazione che **normalizza** *(dividere per la mediana)*
> ### e' **contrattiva**: da sola ### **CONVERGE, non oscilla.** Perche' oscilli serve
> ### ### **un'AMPLIFICAZIONE**, e l'amplificazione e' la potenza `r^2` dell'orologio.
> ### **Avevo confuso <<ritardo>> con <<instabilita'>>: un ritardo di uno e' condizione
> ### NECESSARIA per un periodo 2, non SUFFICIENTE.**

### ✅ **E UN CONTROLLO POSITIVO E' VENUTO GRATIS, che rende il confronto solido**

Al **passo 3** il rapporto e' ### **`1.4872e+04` in ENTRAMBI i rami,
identico.** ### **E deve esserlo PER COSTRUZIONE:** ai passi 1-2 `r = 1` per tutti *(i
rami di sicurezza)*, quindi al passo 3 `r_node` **vale `1` comunque** e la patch del
braccio ### **non cambia nulla.** ### **Se il passo 3 fosse differito, la patch avrebbe
toccato qualcosa che non doveva.**

### ✅ **E `FEDELTA'` PASSA ANCHE NEL BRACCIO:** `0` differenze su `148` passi e `1 937 298` nodi, max scarto `0.000e+00`.
### **La mia ricostruzione di `ritmo()` resta fedele anche nel ramo modificato**, quindi
il confronto e' fra ### **due misure buone**, non fra una buona e una sospetta.

### ⚠ **E IL LIMITE DEL BRACCIO RESTA QUELLO DICHIARATO PRIMA:** `r` e' ancora in
`_dts` *(`:5939`, `:5971`)*, quindi il braccio ### **toglie UNA potenza, da `r^2` a
`r^1` -- NON spezza l'anello.** ### **Il numero dice che BASTA togliere una potenza**,
non che l'anello sia stato eliminato.

## ⛔ COERENZA DI COMPTON **CON `C1`: IPOTESI NULLA -- MA IL TEST CERCA
## NELLA GRANDEZZA SBAGLIATA**, e lo dice il GUARDIANO

> ### ⛔ **CORREZIONE DEL GUARDIANO, 2026-10-05, e la registro come SUA:** il
> ### mandato chiamava `C1` *<<l'angolo di rotazione>>* e chiedeva che uno spinore
> ### ruotato di un angolo NOTO lo restituisse. ### **E' SBAGLIATO -- e l'ha scoperto
> ### IL MIO COLLAUDO** *(`d190dd5`)*: `C1` *(Fubini-Study)* misura lo **spostamento
> ### del VETTORE DI BLOCH**, e ### **una rotazione attorno al Bloch stesso e' pura
> ### FASE e lascia `C1` a ZERO.**
> ### ⛔ **E L'OROLOGIO DI COMPTON E' ESATTAMENTE UNA FASE:** `_phc = exp(-0.5j *
> ### `s_k` * `omega_clk` * `dt`)` *(`:5971`)*. ### **Vive in `C2`, NON in `C1`.**
> ### ⚠ **QUINDI IL NUMERO QUI SOTTO NON SMENTISCE L'IPOTESI DI COMPTON:**
> ### **la smentisce PER `C1`, che e' il posto SBAGLIATO dove cercarla.**
> ### **La misura con `C2` arriva nel commit successivo, come il mandato corretto
> ### prescrive. Questo referto NON si butta: si ANNOTA.**

| | |
|---|--:|
| nodi con almeno 3 misure di `C1` | `13 912` |
| nodi con almeno 3 misure del rapporto | `12 813` |
| `CV(C1)` mediana | `3.5824` |
| `CV(C1/C4s)` mediana | `4.6944` |
| ### **`CV(rapporto)/CV(C1)`** | ### **`1.3104`** |

> ### **IL VALORE SOTTO IPOTESI NULLA ERA SCRITTO PRIMA** *(task history `12ab7f4`)*:
> *<<se `C1` e `C4s` sono indipendenti, `CV(rapporto)^2 ~ CV(C1)^2 + CV(C4s)^2`, quindi
> il rapporto delle due `CV` e' **`>= 1`**>>*.
> ### ⛔ **MISURATO: `1.3104`. E' `>= 1`.**
> ### **Dividere `C1` per `C4s` AGGIUNGE rumore invece di cancellarlo.**
> ### ⚠ **E LA CONCLUSIONE GIUSTA E' PIU' STRETTA DI QUELLA CHE AVREI
> ### SCRITTO:** ### **lo SPOSTAMENTO DEL BLOCH non racconta la stessa storia
> ### della densita' spinoriale.** ### **Sull'OROLOGIO DI COMPTON questo NON DICE
> ### NIENTE**, perche' l'orologio e' una **fase**, e lo spostamento del Bloch e'
> ### esattamente cio' che una fase LASCIA INVARIATO.**

### ✅ **E IL MODO IN CUI QUESTO TEST POTEVA MENTIRE E' ESCLUSO DAI NUMERI**

Avevo scritto che *<<se `C1` e `C4s` saturassero entrambi, il rapporto sarebbe costante
perche' sono due costanti>>*, e che il referto doveva riportare ### **la frazione in
saturazione.** Eccola:

| | mediana | max |
|---|--:|--:|
| `C4` al tetto *(`cs` da `|psi|^2`)* | `0.000000` | `0.000468` |
| `C4s` al tetto *(`cs` da `rho_spin`)* | `0.000000` | `0.000468` |
| `C0` al tetto `1.414212977` | `0.000078` | `0.383768` |

### **Le frazioni in saturazione sono ~`0`.** ### **Il `1.31` e' un risultato, non un artefatto** -- e
### **non puo' essere un FALSO-UNO, perche' quello sarebbe stato nel verso OPPOSTO**
*(una `CV` **bassa** per saturazione)*, e la `CV` ### **non e' bassa.**

## LE DUE LEGGI PRATICHE: **quanto MORDONO** *(il gradino (b))*

| | mediana sui passi | max |
|---|--:|--:|
| `r` **AL TETTO** *(`1.414212977`)* | `0.000078` | ### **`0.383768`** |
| `r` **AL PAVIMENTO** *(`1.414e-06`)* | `0.000000` | ### **`0.052804`** |
| nodi con `x > 1` *(oltre il gauge)* | ### **`0.504553`** | |

### ✅ **IL GRADINO (b) NON E' FALLITO: in MEDIANA le due leggi pratiche NON
### mordono.**
### ⚠ **MA IL MASSIMO DICE UN'ALTRA COSA, e va riportato:** in qualche passo il
### **`38.4%` dei nodi e' AL TETTO**
e il **`5.3%` AL PAVIMENTO.**
### **Sono i passi dell'altalena**, e li' cio' che le leggi ricevono ### **e' la
saturazione, non la legge.**

### 📌 **E `x > 1` sta su `0.5046`, cioe' META' DEI NODI, ed e' una PROPRIETA' del gauge.** Se il gauge fosse dello
**stesso** passo, sarebbe `0.5` ### **per IDENTITA'** -- ed e' il punto fisso `A3` che
la cura del 2026-09-18 ha rotto *(`max|median(x) - 1| = 0.000e+00` **prima** della
cura)*. ### **Qui e' `0.5046` e NON `0.5` esatto: la cura TIENE, e questo numero dice di quanto.**

## `cs`: **LE DUE DENSITA' NON DANNO LA STESSA COSA**

| | passi | mediana | `p5` | `p95` | ### `p95/p5` |
|---|--:|--:|--:|--:|--:|
| `C4` -- `cs` da **`|psi|^2`** | `66` | `0.799608` | `0.519028` | `0.971246` | ### **`1.871`** |
| `C4s` -- `cs` da **`rho_spin`** | `66` | `0.746862` | `0.695445` | `0.863575` | ### **`1.242`** |
| `C4` dalla **CACHE che l'orologio usa** | `148` | `0.803536` | `0.506957` | `0.972914` | ### **`1.919`** |

> ### ⛔ **LA DISPERSIONE E' DIVERSA, e di molto:** `cs` da `|psi|^2` ha
> `p95/p5 = ` ### **`1.871`**, `cs` da `rho_spin` ### **`1.242`**.
> ### **La densita' SPINORIALE da' un `cs` molto piu' UNIFORME: un fattore `1.51` di dispersione in meno.**
> ### **E' il numero che la via `(d')` deve avere davanti: passare a `rho_spin` non e'
> ### solo <<togliere un'eccezione>>, CAMBIA LA DISPERSIONE DI `cs`.**

### **I DUE ESPONENTI, `C5` -- e' una DECISIONE DI LUCA: li riporto ENTRAMBI**

| | `(cs/CS_M)^2` *(`STEP2`)* | `(cs/CS_M)^0.5` *(rel. generale, coord. isotrope)* |
|---|--:|--:|
| `cs` da `|psi|^2` | `0.639374` *(`p5` `0.2694`, `p95` `0.9433`)* | `0.894208` *(`p5` `0.7204`, `p95` `0.9855`)* |
| `cs` da `rho_spin` | `0.557803` *(`p5` `0.4836`, `p95` `0.7458`)* | `0.864212` *(`p5` `0.8339`, `p95` `0.9293`)* |
| dalla **cache dell'orologio** | `0.645670` *(`p5` `0.2570`, `p95` `0.9466`)* | `0.896402` *(`p5` `0.7120`, `p95` `0.9864`)* |

### ⛔ **NON scelgo: il mandato dice che l'esponente e' una DECISIONE DI LUCA.** Il
fattore mediano e' `0.6457` con l'esponente `2` e `0.8964` con `0.5` *(dalla cache che l'orologio usa davvero)*.

### ⚠ **UN LIMITE DEL MIO STRUMENTO, dichiarato invece che taciuto**

`C4` e `C4s` **allo stesso istante** escono su ### **`66` passi su `148`**, mentre `C4` **dalla cache** c'e' su
tutti e `148`. ### **IL PERCHE' E' UN DIFETTO MIO:** la copia di
`cs` che il mio gancio conserva ### **non si estende con la mitosi**, quindi quando `n`
cresce fra il sito di `cs` e `ritmo()` la lunghezza non torna e il passo si salta.
### **La cache del simulatore invece SI estende** *(`_cs_nodo_prev` ha le sue regole di
nascita)*. ### **E' la stessa classe di difetto di `_cs_nodo_prev` e `_psi_spin_prec`
che il file documenta -- l'ho fatta io, in piccolo, e la dichiaro. VA IN CODA.**
### ✅ **E NON falsa il confronto `C4` contro `C4s`:** sono calcolati ### **nello
stesso istante e sugli stessi passi**, quindi il rapporto fra le dispersioni e' buono.

## LA DISPERSIONE: **`V1` NON e' il caso `Z37`**

| | passi | mediana | `p5` | `p95` | ### `p95/p5` |
|---|--:|--:|--:|--:|--:|
| `C0` | `148` | `1.008e+00` | `1.011e-01` | `1.398e+00` | ### **`13.83`** |
| `C1` | `148` | `1.412e-01` | `3.128e-02` | `5.860e-01` | ### **`18.73`** |
| `S1` | `147` | `4.150e-01` | `9.636e-02` | `1.523e+00` | ### **`15.80`** |
| `V1` | `148` | `1.027e+00` | `2.554e-01` | `3.578e+00` | ### **`14.01`** |
| `C6` | `148` | `3.755e-02` | `4.919e-03` | `2.148e-01` | ### **`43.66`** |

> ### ✅ **`V1` ha mediana `1.0273` MA `p95/p5 = ` ### **`14.01`**.
> ### **Il rischio `Z37` che avevo scritto PRIMA -- *<<se i vicini hanno `C1` quasi
> ### uguale, `V1 ~ 1` per tutti e il segnale sparisce>>* -- NON si e' verificato.**
> La **dispersione di `C1` fra vicini** e' `7.0263e-02`, ### **non zero.**
> ### ⚠ **E la mediana `~1` NON e' <<il segnale che sparisce>>: e' COME `V1` E'
> ### COSTRUITO** *(si divide per la mediana dei vicini)*. ### **Guardare la mediana di
> `V1` e concludere <<nessun segnale>> sarebbe stato un errore mio, e il task history mi
> ### aveva detto di guardare la DISPERSIONE.**

## LA RELAZIONE DI MASSA: pendenza log-log

| | mediana | `p5` | `p95` | passi |
|---|--:|--:|--:|--:|
| `C1` contro `|psi|^2` | ### **`-0.1421`** | `-0.1717` | `-0.1112` | `148` |
| `C1` contro `rho_spin` | ### **`-0.4988`** | `-1.3152` | `-0.2312` | `148` |
| `abs(C2)` contro `|psi|^2` | ### **`0.1732`** | `-0.1664` | `0.5467` | `148` |
| `abs(C2)` contro `rho_spin` | ### **`-0.2240`** | `-0.6666` | `0.3749` | `148` |

> ### ⛔ **LE PENDENZE SONO NEGATIVE O PICCOLE: nessuna somiglia a una legge di
> ### Compton.** Per una frequenza propria `~ massa` servirebbe ### **`+1`**; per
> `omega ~ m c^2/hbar` con `c -> cs` servirebbe comunque un esponente **positivo**.
> ### **Misurato `-0.1421` contro `|psi|^2` e `-0.4988` contro `rho_spin`:**
> ### **nei dati di oggi la rotazione dello spinore CALA al crescere della densita'.**

### ⚠ **CHE COSA QUESTO NON DICE:** ### **non dice che non esista una `f0`.** Dice
che ### **non e' una POTENZA di `|psi|^2` ne' di `rho_spin`** in questa scena.
### **Quindi la via `(c)` NON e' sostenuta dalla relazione misurata** -- ed e'
esattamente la condizione che il mandato poneva *(<<se la relazione misurata lo
sostiene>>)*.

## MATERIA CONTRO VUOTO, e i NODI NEL LORO PRIMO PASSO

| | materia *(top 5% di `|psi|^2`)* | vuoto | nodi al **primo passo** |
|---|--:|--:|--:|
| `C0` | `1.354e+00` | `1.006e+00` | `1.060e+00` |
| `C1` | `9.635e-02` | `1.441e-01` | `2.533e-01` |
| `C2_abs` | `5.893e-02` | `2.252e-02` | `2.864e-02` |
| `S1` | `5.079e-01` | `4.104e-01` | `n/d` |
| `V1` | `8.654e-01` | `1.038e+00` | `1.090e+00` |
| `C6` | `8.176e-02` | `3.749e-02` | `n/d` |

### **`C0` di materia e' `1.354e+00` contro `1.006e+00` del vuoto:** ### **la materia ha un tempo proprio piu'
veloce**, nel senso di `r`. ### **E' il verso che il guardiano aveva trovato.**

### ⚠ **E UNA DIFFERENZA COL NUMERO DEL GUARDIANO, che dichiaro e NON spiego:**
i nodi nel loro primo passo hanno `C0` mediano `1.060e+00`, mentre il guardiano riportava `r ~1.2-1.4`.
### **Per spiegarla servirebbe separare i nati da DIVISIONE dai nati da SCHWINGER**
*(l'eredita' di `_psi_spin_prec` viene dal genitore in entrambi i casi, ma le due
nascite non danno gli stessi vicini)*, e ### **questo strumento non lo fa. VA IN CODA.**

## LE SEI VIE -- **riportate, NON scelte**

> ### ⛔ **NESSUNA LEGGE NUOVA: la forma la decide Luca.** Qui ci sono i numeri.

| via | l'altalena sparisce? | `A6`? | locale? | materia / vuoto | strada chiusa? |
|---|---|---|---|---|---|
| **(a)** `S1`, a **se stesso** | ### **SI'** -- `1.068` | ✅ **si'**, se la finestra e' sui passi precedenti | ### ✅ **SI'** | `5.08e-01` / `4.10e-01` | **no** |
| **(b)** `V1`, ai **vicini** | ### **SI'** -- `1.006` | ### ⚠ **dipende:** i vicini dello **stesso** istante violerebbero `A6`; serve lo snapshot | ### ✅ **SI'** | `8.65e-01` / `1.04e+00` | ### **`Z37`, MA `p95/p5 = 14.0` dice che NON e' quel caso** |
| **(c)** `f0` dalla **massa** | non misurabile qui | ✅ **si'** | ✅ **si'** | -- | ### ⛔ **NON SOSTENUTA: pendenza `-0.142`, non `+1`** |
| **(d)** da `cs` con `|psi|^2` | non misurato direttamente | ✅ `cs` e' del passo precedente | ### ⚠ **`cs` e' locale, MA la sua scala `_Lam = mean(I)` e' GLOBALE** | `cs/CS_M` `0.7996` | ### ⚠ **apre l'anello `r <-> cs`** |
| **(d')** da `cs` con `rho_spin` | non misurato direttamente | ✅ come `(d)` | ### ⚠ come `(d)` | `cs/CS_M` `0.7469`, ### **dispersione `1.24` contro `1.87`** | come `(d)`, ### **e toglie l'eccezione delle due densita'** |
| **(e)** da **`omega_clk`** | ### ✅ **SI', PER COSTRUZIONE** -- e `BRACCIO A` lo MISURA: `1.031` | ✅ **si'** | ### ⚠ la coerenza d'arco e' locale, `cs` come sopra | i due esponenti `0.6457` e `0.8964` | **no**, ### **ma l'ESPONENTE e' di LUCA** |
| **(f)** `C6`, via di `Z41` | ### ⛔ **NO -- `35.67`, il PEGGIORE di tutti** | ### ⛔ **da decidere:** `f = delta/(DT*r)` mette `r` nel denominatore di cio' che definisce `r` | ✅ **si'** | `8.18e-02` / `3.75e-02` | ### **`Z41`, e il numero NON la aiuta** |

### ⛔ **IL NUMERO CHE SORPRENDE, riportato senza interpretarlo oltre:** `C6` --
### **la via nominata da `Z41`** -- ha rapporto dispari/pari ### **`35.67`, PIU' ALTO di `C0` stesso** *(`7.19`)*.
### **Misurare `f` in tempo proprio PEGGIORA l'altalena invece di curarla**, e il
perche' e' aritmetico: `f/(DT*r)` divide per un `r` che ### **alterna anche lui**,
quindi le due alternanze ### **si moltiplicano.**
### ⚠ **NON concludo che `(f)` sia da scartare -- lo decide Luca.** Dico che
### **il numero non la aiuta, e che `Z41` resta chiusa anche da questo lato.**

## CHE COSA QUESTA MISURA **NON** DICE

1. ### ⛔ **NON DICE NIENTE SULL'OROLOGIO DI COMPTON:** il test di coerenza
   e' stato fatto con `C1`, e ### **l'orologio e' una FASE: vive in `C2`.**
   ### **Correzione del guardiano, e la misura giusta e' nel commit dopo;**
2. ### **non dice che `r` DEBBA essere `C1`:** dice che l'altalena vive nella parte che
   `C1` scarta. ### **La definizione e' una decisione di Luca** -- `Z43` e'
   `da-decidere` dal 2026-09-18 proprio per questo;
3. ### **non misura l'effetto a valle** sulla traiettoria: misura `r` e i suoi
   ingredienti, ### **non le conseguenze di cambiarlo**;
4. ### **`BRACCIO A` non spezza l'anello**, ne toglie **una potenza**:
   ### **non so se eliminarlo del tutto farebbe di piu' o di meno**;
5. ### **non separa i nati da divisione dai nati da Schwinger**, e la differenza col
   numero del guardiano sui nodi nuovi resta ### **non spiegata.**

## CHE COSA RESTA IN CODA

1. ### **la copia di `cs` del mio gancio non si estende con la mitosi:** `C4`/`C4s`
   allo stesso istante escono su `66` passi su `148`. ### **Difetto MIO, stessa classe di `_cs_nodo_prev`**;
2. **separare i nodi nuovi per TIPO di nascita** *(divisione contro Schwinger)*;
3. ### **il quanto di `A3`:** `x > 1` sta su `0.5046`, vicino a `0.5` ### **ma non
   esatto** -- la cura del 2026-09-18 tiene, e questo numero dice **di quanto**.

## IL CENSIMENTO: **per PROVENIENZA, non per nome**

Consumatori **veri** del ritmo: ### **`13`**. Scartati perche' ### **NON sono il ritmo**: `12`.

| scartato | perche' |
|---|---|
| `r@_accresci` | NON ASSEGNATO qui |
| `r@_celle_vive` | NON ASSEGNATO qui |
| `r@_diag_completa` | ALTRO (non il ritmo) |
| `r@_git` | ALTRO (non il ritmo) |
| `r@_gusci_esterni` | ALTRO (non il ritmo) |
| `r@_massa` | NON ASSEGNATO qui |
| `r@_semina_lam` | NON ASSEGNATO qui |
| `r@_semina_masse_coerenti` | ALTRO (non il ritmo) |
| `r@batch_condensazione` | NON ASSEGNATO qui |
| `r@chiralita_core_locale` | ALTRO (non il ritmo) |
| `r@ritmo` | ALTRO (non il ritmo) |
| `r@semina` | ALTRO (non il ritmo) |

### ⛔ **UN CENSIMENTO PER NOME AVREBBE CONTATO `25` VOCI INVECE DI `13`.** In quelle funzioni `r` e' un **raggio** o una **riga di
CSV**. ### **E' il par.2 applicato a se stesso: non si cerca per riga, e non si conta
per nome.**

## LA SCENA E LA PIATTAFORMA

`--nmasse 3 --sep 6.1158`, seme `11`. A `150` passi: `n = 14 000`, archi `473 022`. Passi **misurati** `148` su `150` *(i due saltati sono i rami di sicurezza)*.

`python 3.13.2` · `numpy 2.3.0` · Windows 11 · AMD64.
### ✅ **Il fatto del guardiano era su LINUX, e i due andamenti coincidono ordine
per ordine** *(`PIATTAFORMA-NON-TIMBRATA`)*.
