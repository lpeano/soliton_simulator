# `A-S1` — **IL TEST `H1` DI `SCIOGLIMENTO-FASE`** *(2026-10-07 sera, mandato di Luca)*

> ### ⛔ **SOLO LA SCENA CAMBIA, NESSUNA LEGGE.** Il simulatore resta ### **`b8c21049`**, e la
> modifica è una ### **CONDIZIONE INIZIALE imposta NELLO STRUMENTO**, dichiarata.

> ### 📌 **QUESTO FILE SI COMMITTA E SI PUSHA PRIMA DELLO STRUMENTO E PRIMA DELLA CORSA**, così
> l'ordine è ### **verificabile da git** *(questo commit è antenato di quelli del lavoro)*
> invece che asserito da me.

---

## 0. ⭐ **CHE COSA ESISTE GIÀ, E CHE COSA RIUSO** — *letto PRIMA di progettare*

Il mandato dice: *«leggi `doc/TASK_HISTORY/2026-09-27_scioglimento.md` e la voce
`SCIOGLIMENTO-FASE`: riporta quali misure erano previste o già fatte, e RIUSA i loro criteri
se ci sono. Non rifare ciò che esiste.»* ### **Fatto, e l'esito è che A-S1 NON È UNA MISURA
NUOVA: è `S1b`, già progettata il 2026-09-27 e MAI eseguita.**

| misura del 2026-09-27 | che cos'è | stato |
|---|---|---|
| `S1` | dispersione di `phivel` dentro le masse al passo `0`, contro il suo **nullo** *(il VUOTO, non zero)* | ### ⛔ **mai fatta** |
| ### ⭐ **`S1b`** | ### **braccio corto, `40` passi, `4` semi: i nodi di massa partono con `phivel` = MEDIA della massa**, contro il braccio attuale | ### ⛔ **mai fatta** — ### **ed è ESATTAMENTE `A-S1`** |
| `S2` | derivata numerica `d(coppia)/d(phi)`, con lo zero atteso **ESATTO** | ### ⛔ **mai fatta** — è `A-S2` |
| `S2b` | quante volte la guardia `len(_psi_spinor) >= n` TIENE | ### ⛔ **mai fatta** |
| `S2c` | distanza dello stato vero dal limite dichiarato | ### ⛔ **mai fatta** |
| `S3` | `xi_termo` per passo, col **nullo** su un vuoto senza masse | ### ⛔ **mai fatta** |
| `S5` | scomposizione dello sfasamento fra dispersione di `phivel` e di `r_k` | ### ⛔ **mai fatta** |

### ✔ **COSA RIUSO DI `S1b`, ALLA LETTERA**

1. ### **IL METODO:** *«`phivel` si impone NELLO SCRIPT DI TEST, con `net.phivel[idx] = media`.
   Nessun file del simulatore viene toccato.»* ### **È la stessa cosa che chiede il mandato di
   oggi**, e il task history del 2026-09-27 l'aveva già corretta una volta *(la prima stesura
   diceva che serviva toccare la scena: era sbagliato)*.
2. ### **IL NULLO:** *«contro il suo NULLO — la dispersione nel VUOTO, non zero»*. ### **Lo
   porto dentro A-S1:** la coorte ### **`vuoto`** è il denominatore di ogni numero per massa.
3. ### **LA FORMA DEL CRITERIO:** *«la coerenza RISALE»*, non *«la coerenza è alta»*.

### ⛔ **E DUE COSE DI `S1b` CHE NON POSSO RIUSARE, e le DICHIARO invece di tacerle**

| | `S1b` chiedeva | `A-S1` fa | perché |
|---|---|---|---|
| i semi | ### **`4` semi** *(`P3`)*, con la barra fra semi | ### **`1` seme: `11`** | ### **il braccio di controllo è la corsa `A1`**, che il mandato dice di ### **non rigirare**, e `A1` è sul seme `11`. ### ⚠ **CONSEGUENZA: nessuna barra d'errore fra semi.** Il confronto è ### **APPAIATO** *(stessa scena, stesso seme, UNA condizione iniziale cambiata)*, che è la forma più forte di confronto appaiato ### **e non dice NIENTE sulla variabilità fra semi** |
| i passi | ### **`40`** | ### **`500`** | a `40` passi ### **non è ancora nata nessuna massa** e l'AUC del controllo vale ancora `~0.99`: ### **`40` passi misurerebbero il nulla** *(ed è `FINESTRA-PRE-NASCITA`)* |
| la grandezza | `coer_campo` | ### **AUC di `c_k` MATERIA/VUOTO** | ### **è la grandezza su cui Luca ha deciso la sospensione**, e il controllo `A1` la registra |

> ### ⛔ **`P3` NON È SODDISFATTA, E LO SCRIVO QUI E NEL REFERTO.** `A-S1` è una
> ### **DIAGNOSI**, non un sigillo: nessuna cura dipende da lei. ### **Il giorno in cui una
> cura dipendesse da questo numero, servono i quattro semi.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### `H1`, VERIFICATA DI NUOVO SUL SORGENTE DI `b8c21049` *(non ripresa dalla voce)*

`_semina_masse_coerenti` *(`:9916`)* scrive ### **`net.phi[idx]`** e ### **`net.phi0[idx]`** e
### **NIENTE ALTRO**: `phivel` ### **non compare nella funzione.** I nodi delle masse tengono
il `phivel` che la ### **semina** ha dato a tutti *(`:5068`-`:5077`: con `CALORE_VETTORIALE`,
`calcio_phi = chi * normal(_CALORE_INIT, _CALORE_INIT*0.5)`)*.
### ➜ **Le masse nascono IN FASE e con VELOCITÀ DI FASE CASUALI.**

### ✔ **E NIENTE NELLA COSTRUZIONE DIPENDE DA QUELLE `phivel`** — *la verifica che il mandato chiede*

Nel percorso di costruzione `phivel` è ### **SCRITTA** *(`:5075`/`:5077`, in coda)* e
### **mai LETTA** per derivarne un'altra grandezza immagazzinata. ### **`chi_nuovi` è assegnata
PRIMA** *(`:5062`, e il commento lo dice: «assegnato PRIMA di `phivel` perché il calcio chirale
lo usa»)*, cioè la dipendenza va ### **da `chi` a `phivel`**, non al contrario. Dopo il blocco
di `phivel`, `semina` chiama `self._allaccia(base)` e scrive la maturità: ### **nessuna delle
due legge `phivel`.**
### ➜ **Quindi sovrascrivere `phivel` DOPO la costruzione non lascia nessuno stato
incoerente**, e ### **non consuma RNG** *(si sovrascrive, non si ri-estrae)*: la scena resta
identica al bit in tutto il resto. ### **Non mi fermo.**

### ⛔ **MA DUE ACCOPPIAMENTI DINAMICI CHE LA VOCE NON AVEVA, E CHE CAMBIANO LA LETTURA**

#### ⛔ **`(1)` IL CONFONDENTE: `tau_tw` SI DERIVA DALLA DISPERSIONE DI `phivel`**

`_tau_tw_locale` *(`:610`-`:627`)*:

```
dom    = |phivel[i] - phivel[j]| + 1e-3
tau_tw = max(2 pi / dom, 1e-3)
```

### ➜ **Azzerare la dispersione di `phivel` DENTRO una massa porta `dom` al suo PAVIMENTO**
`1e-3` sugli archi ### **intra-massa**, e quindi

```
tau_tw -> 2 pi / 1e-3 = 6283.2
```

contro una mediana ### **misurata** di ### **`2.4055` al passo `50`** *(il numero è nel
commento del codice, cura `TORS-W8-AVVOLGIMENTO`)*: ### **un fattore ~`2600`.**

> ### ⛔ **QUINDI IL BRACCIO `H1` NON CAMBIA UNA COSA SOLA NELLE SUE CONSEGUENZE.** Al passo `0`
> cambia ### **solo `phivel`** *(e il controllo del passo `0` lo verifica al bit)*; ### **dal
> passo `1` cambia ANCHE il tempo di memoria della torsione dentro le masse, di tre ordini di
> grandezza.**
>
> ### ⭐ **E L'ASIMMETRIA SALVA METÀ DEL TEST, e la scrivo PRIMA:**
> ### ✔ **se l'AUC resta bassa, `H1 NON BASTA` vale LO STESSO — e vale di PIÙ:** un intervento
> che ha dato alle masse ### **sia** le velocità coerenti ### **sia** una memoria della
> torsione quasi permanente ### **non le ha salvate comunque.**
> ### ⛔ **se l'AUC risale, la causa è AMBIGUA** fra *«la coerenza di fase»* e *«il crollo del
> rilassamento della torsione»*, e ### **servirebbe un terzo braccio che NON posso costruire
> senza toccare una legge.** ### **In quel caso il referto dirà `CONFONDUTO` e la decisione
> sarà di Luca.**
>
> ### ✔ **E IL CONFONDENTE SI MISURA, non si assume:** `tau_tw` mediana sugli archi
> ### **intra-massa** e su ### **tutti**, a ogni passo misurato, nei due bracci.

#### ⚠ **`(2)` LA DISPERSIONE SI RI-INIETTA: `scuoti_vuoto` SCRIVE `phivel` A OGNI PASSO**

`PASSO_COMPOSIZIONE = ('apri', 'scuoti_vuoto', 'step', 'mitosi', …)` *(`:965`)*, e
`SCUOTIMENTO` vale ### **sempre `True`** *(`:867`)*. Il registro delle scritture dichiara
`scuoti_vuoto` → *«scrive `phivel` e nient'altro»* *(`:1010`)*, e il calcio è
`net.phivel[:net.n] += calcio` *(`:938`)* con ampiezza derivata dallo ### **stress locale** e
soppressa dalla ### **coerenza locale `|Psi|²`.**

### ➜ ### **L'EQUALIZZAZIONE È UNA CONDIZIONE INIZIALE, NON UNO STATO MANTENUTO.** La
dispersione ### **torna**, a un ritmo che la soppressione per `|Psi|²` rende ### **più lento
dove la coerenza è alta** — cioè ### **dentro le masse, all'inizio.**
### ⭐ **È la ragione principale della mia previsione.**

### ⛔ **CHE COSA NON SO**

- ### **a che ritmo** la dispersione torna: la soppressione per `|Psi|²` e lo stress locale
  sono entrambi dinamici, e ### **non ho fatto il conto**;
- se il crollo del rilassamento della torsione *(il confondente)* ### **aiuti** o
  ### **danneggi** la coerenza: una torsione che non rilassa è una memoria che non dimentica,
  e ### **non so dire il segno dell'effetto sul campo**;
- se `H2` *(nulla riallinea `phi`: la coppia non la legge, `ritmo()` non la legge, resta solo
  il Kuramoto)* renda `H1` ### **strutturalmente insufficiente**: se niente riallinea, una
  condizione iniziale coerente ### **può solo ritardare**, non riparare.

---

## 2. PROGETTAZIONE — **i criteri e le previsioni, PRIMA dei numeri**

### LA SCENA E IL BRACCIO

| | |
|---|---|
| scena | quella del ### **driver**: `--nmasse 3 --sep 6.1158 --nodi 0 --seed 11`, `argv` completo, ### **`b8c21049`** |
| l'intervento | ### **DOPO la costruzione e PRIMA del passo `1`**, per ogni massa: `net.phivel[idx] = media(net.phivel[idx])` |
| perché la MEDIA | ### **toglie SOLO la dispersione** e ### **non cambia la velocità media della massa** — ### ⭐ **e non introduce NESSUN numero nuovo** *(`A1`: la legge, non il numero)* |
| le coorti | ### **`test["dati"]["coorti"]`**, che la scena registra già: `massa_0`, `massa_1`, `massa_2`, `vuoto`. ### ⛔ **Se mancano o sono vuote: FERMO** |
| il controllo | ### **la corsa `A1` (`67f020e`)**, che ### **non si rigira** e che combacia al bit con `amp0.json` |

### ⛔ **IL CONTROLLO DELLA MODIFICA, AL PASSO `0`**

Due reti costruite ### **identicamente**, una modificata e una no, confrontate con
### **la `_firma` del presidio su TUTTO `net.__dict__`**, come la byte-inerzia.
### ✔ **DEVE differire SOLO `phivel`, e SOLO sui nodi delle masse.**
### ⛔ **Qualunque altro attributo diverso, o un nodo del VUOTO con `phivel` diversa: FERMO, e
la corsa non parte.**

### LE MISURE, ai passi **`1, 50, 150, 230, 300, 400, 500`**

| | che cosa | come |
|---|---|---|
| ### **`AUC`** di `c_k` MATERIA/VUOTO e ### **mediana di `c_k` per classe** | ### **lo STESSO calcolo di `A1`** | ### ✔ **`m2` di `_misura_verso` NON è ricopiata: è CHIAMATA.** Niente seconda formula *(`9-ter`)* |
| la ### **coerenza di fase interna di OGNI massa** | ### **`\|<e^{i phi}>\|`** sui nodi della massa | ### ⚠ **PIÙ `\|<e^{i phi/2}>\|`**, e la differenza non è pedanteria: `phi` vive su ### **`4 pi`**, quindi `e^{i phi}` identifica `phi` con `phi + 2 pi`. ### **Il campo del simulatore usa `exp(1j*phi)`** *(`:5195`)*, quindi la PRIMA è quella che il codice vede; la seconda è quella fedele al dominio. ### **Si riportano ENTRAMBE** |
| la ### **dispersione di `phivel` per massa** | `std(phivel[idx])` | ### **col NULLO: la stessa su `vuoto`** — ### ⛔ **mai contro zero** |
| le ### **nascite** | `n` per passo | il controllo ce l'ha a ### **ogni** passo |
| la frazione con ### **`\|tw\| > 2 pi`** | `mean(\|tw\| > 2 pi)` | ### **la stessa espressione di `A1`** |
| ### ⭐ **il CONFONDENTE** *(mia aggiunta, dichiarata)* | `tau_tw` mediana ### **intra-massa** e su ### **tutti** gli archi | ### **misura il fattore `~2600` invece di assumerlo** |

### ⚠ **E UNA LACUNA DEL CONTROLLO, DICHIARATA PRIMA**

### **Al passo `50` la corsa `A1` NON ha l'AUC:** i suoi passi pesanti sono
`1, 150, 230, 300, 400, 500, 700, 1000`. ### ✔ **Gli altri SEI passi misurati hanno il
controllo**, e ### **i due passi su cui i criteri decidono — `400` e `500` — ce l'hanno.**
### ➜ **Non rigiro il controllo per un passo che non decide**, e lo scrivo invece di lasciare
una cella vuota senza spiegazione. ### **`n` e la frazione `|tw| > 2π`, invece, il controllo le
ha a OGNI passo**, perché le registrava per passo.

### ⛔ **I CRITERI, FISSATI ADESSO** *(mandato di Luca)*

| esito | condizione | nel controllo |
|---|---|---|
| ### ✔ **`H1 BASTA`** | AUC al `400` ### **`>= 0.9`** ### **E** al `500` ### **`>= 0.85`** | `0.4679` e `0.4497` |
| ### ⛔ **`H1 NON BASTA`** | AUC al `400` ### **`< 0.6`** | ### **le masse si sciolgono anche con le velocità coerenti → si passa ad `A-S2`** |
| ### ⚠ **`H1 AIUTA MA NON BASTA`** | fra i due | ### **si riporta la CURVA e il passo in cui l'AUC scende sotto `0.6` nei DUE bracci** |

### ✔ **E I NUMERI DEL CONTROLLO, presi dal json e non ricopiati** *(`L-NUMERI`)*

| passo | AUC | `c_k` MATERIA | `c_k` VUOTO | `n` | nati | `\|tw\| > 2π` |
|--:|--:|--:|--:|--:|--:|--:|
| `1` | `0.9992` | `0.7904` | `0.1627` | `12802` | `0` | `0.00000` |
| `50` | ### ⚠ **ASSENTE** | — | — | `12802` | `0` | `0.00000` |
| `150` | `0.9861` | `0.6483` | `0.2430` | `12802` | `0` | `0.00109` |
| `230` | `0.9023` | `0.4847` | `0.2665` | `12813` | `11` | `0.00721` |
| `300` | `0.7371` | `0.3870` | `0.2744` | `12850` | `48` | `0.01392` |
| ### **`400`** | ### **`0.4679`** | `0.2882` | `0.2972` | `12905` | `103` | `0.02589` |
| ### **`500`** | ### **`0.4497`** | `0.2761` | `0.3019` | `13009` | `207` | `0.03770` |

### ⭐ **LE PREVISIONI, PRIMA DELLA CORSA**

| | la previsione | il perché |
|---|---|---|
| ### **`PH1-1`** | ### ⚠ **`H1 AIUTA MA NON BASTA`**: l'AUC al `400` è ### **SOPRA `0.4679`** *(il controllo)* ### **ma SOTTO `0.9`** | `scuoti_vuoto` ### **ri-inietta** la dispersione a ogni passo: l'equalizzazione è una condizione iniziale, non uno stato |
| ### **`PH1-2`** | la dispersione di `phivel` intra-massa ### **TORNA**: al passo `150` è già ### **più di metà** di quella del `vuoto` | la soppressione per `\|Psi\|²` rallenta il calcio ma non lo spegne, e la coerenza cala |
| ### **`PH1-3`** | `tau_tw` intra-massa al passo `1` è ### **almeno `100 ×`** la mediana su tutti gli archi, e ### **CALA** sui passi misurati | è il confondente, e cala al tornare della dispersione |
| ### **`PH1-4`** | ### ⚠ **il passo `1` NON è un discriminante:** la coerenza per massa è ### **`>= 0.99`** in ENTRAMBI i bracci | la scena semina con dispersione di fase `0.05` rad: la coerenza iniziale è alta ### **per costruzione.** ### **Lo scrivo adesso per non spacciare dopo una non-misura per una conferma** |
| ### **`PH1-5`** | le nascite a `500` passi stanno ### **entro il `±25 %`** delle `207` del controllo | le nascite dipendono da `rho` e dalla soglia, non direttamente da `phivel` |

### ⛔ **CHE COSA MI FAREBBE FERMARE**

1. il ### **controllo del passo `0`** trova un attributo diverso da `phivel`, o una `phivel`
   diversa su un nodo del ### **VUOTO**;
2. ### **`test["dati"]["coorti"]`** manca, è vuoto, o le tre masse non coprono i nodi attesi;
3. il ### **collaudo** non passa, o il caso che ### **DEVE fallire** non fallisce;
4. la corsa alza una guardia: ### **si committa il fallimento e la cura è un commit a sé.**

---

## 3. ⭐ **LA STELLA POLARE** *(`L-STELLA`: si risponde PER ISCRITTO, anche con «non si applica»)*

| la domanda | la risposta |
|---|---|
| `A14` *(conservazione locale / dissipazione globale)* | ### **NON SI APPLICA**, e il perché: ### **questo lavoro non aggiunge, non toglie e non cambia nessun termine di nessuna legge.** Il simulatore gira ### **identico** *(`b8c21049`)*; cambia ### **un valore dello stato iniziale**, come lo cambierebbe un altro seme |
| il gradino di ### **`ROBUSTEZZA-FISICA`** | ### **NON SI APPLICA**: nessuna legge nuova da rendere robusta. ### ⚠ **Ma c'è un gradino di robustezza della MISURA, e l'ho dichiarato:** il confondente su `tau_tw` |
| numeri o leggi aggiunti, e di che tipo | ### **ZERO leggi, ZERO numeri.** La media di un insieme ### **non è una manopola**: è determinata dai dati, non scelta da me |
| il verso ### **EM-curvatura** | ### **NON SI APPLICA**: non si tocca né l'elettromagnetismo né la metrica |
| ### **emergente o imposto** | ### ⛔ **IMPOSTO, e dichiarato tale.** La coerenza delle velocità di fase è ### **messa a mano nella condizione iniziale**, non emersa. ### ⭐ **Ed è esattamente il punto del test:** si impone per ### **vedere se basta**, non per tenerla. ### **Se bastasse, la cura vera dovrebbe farla EMERGERE** — e quella sarebbe `A-S2`, con la regola `§0` e `A15` |

---

## 4. TODO DEL NEXT STEP — *operativo, non un riassunto*

- [ ] **(a)** questo task history, ### **committato e pushato PRIMA** di tutto;
- [ ] **(b)** `csv/_test_fork/_massa_h1.py` + collaudo, col caso che ### **DEVE fallire**;
- [ ] **(c)** il ### **controllo del passo `0`**, committato col suo esito;
- [ ] **(d)** il giro a ### **`2` passi**;
- [ ] **(e)** la corsa da ### **`500` passi in background**, interrogata, ### **senza chiudere
      il turno**;
- [ ] **(f)** json e referto, con la tavola ### **previsioni contro numeri** e la dichiarazione
      del ### **confondente** e di ### **`U1` aperta**;
- [ ] **(g)** poi ### **FERMO**: ### ⛔ **se `H1` non basta NON si comincia `A-S2`** — la
      decisione è di Luca.

---

# ⛔ **AGGIUNTA DATATA — 2026-10-07 sera, DOPO il controllo del passo `0` e PRIMA della corsa** *(`par.8`: si ANNOTA; le PREVISIONI qui sopra NON si toccano)*

> ### ⭐ **LE CINQUE PREVISIONI RESTANO COME SONO.** Questa sezione aggiunge
> ### **un TERZO accoppiamento** e ### **i numeri di `S1`**, che il controllo del passo `0`
> ha prodotto gratis. ### **Nessun criterio è cambiato, e nessun numero oltre il passo `0` è
> stato visto.**

## ✔ **IL CONTROLLO DEL PASSO `0` PASSA**

| | |
|---|--:|
| attributi firmati | ### **`63`** |
| attributi ### **diversi** | ### **`1`** — ### **solo `phivel`** |
| nodi delle masse | `411 + 413 + 413 = ` ### **`1237`** *(il `9.66 %`)* |
| nodi del VUOTO con `phivel` ### **IDENTICA AL BIT** | ### **`11565`** |

## ⭐ **E `S1` È VENUTA GRATIS, col suo NULLO — e dice una cosa che non mi aspettavo**

| | `std(phivel)` |
|---|--:|
| ### **dentro le masse** | ### **`0.4131`** |
| ### **nel VUOTO** *(il NULLO, non zero)* | ### **`0.3934`** |
| `_CALORE_INIT` | `0.4` |

### ⛔ **LA DISPERSIONE DENTRO LE MASSE È SOLO IL `5 %` PIÙ ALTA DI QUELLA DEL VUOTO.**
### ➜ **Quindi le masse non sono «specialmente disperse»: sono disperse come TUTTO IL RESTO**,
e l'unica cosa che le distingue è che ### **PARTONO in fase.**
### ⚠ **`S1` non è refutata** *(la dispersione è dell'ordine di `_CALORE_INIT`, cioè NON è
trascurabile)*, ### **ma la sua lettura cambia:** `H1` non dice *«le masse hanno un difetto»*,
dice *«la coerenza iniziale non è protetta da niente»*.

## ⛔ **IL TERZO ACCOPPIAMENTO: L'INTERVENTO TOGLIE IL `10.52 %` DELL'ENERGIA CINETICA DI FASE GLOBALE**

Le medie di `phivel` per massa sono ### **`−0.0166`, `−0.0146`, `+0.0279`** — cioè
### **quasi ZERO**, come ci si aspetta da un calcio simmetrico. ### ➜ **Equalizzare alla media
non «allinea le velocità»: le AZZERA.**

| `<phivel²>` | prima | dopo | calo |
|---|--:|--:|--:|
| ### **GLOBALE** *(ciò che il termostato legge)* | `0.156311` | `0.139863` | ### **`10.52 %`** |
| dentro le masse | `0.170649` | `0.000423` | ### **`99.75 %`** |
| nel vuoto | `0.154778` | `0.154778` | ### **`0` — identico al bit** |

### **E IL TERMOSTATO LEGGE UNA MEDIA GLOBALE** *(`:7711`: `E_cin = mean(phivel[:n]**2)`)*, col
suo comportamento dichiarato nel codice: *«`xi>0` frena (energia alta), ### **`xi<0`
RIFORNISCE** (energia bassa)»*.
### ➜ **Quindi l'intervento fa partire il termostato in modo RIFORNENTE, su TUTTA la rete.**

### ⭐ **MA IL RIFORNIMENTO È MOLTIPLICATIVO, E QUESTO CAMBIA LA PREVISIONE DEL MECCANISMO**

`delta_phivel = dt_n_s * (coppia − xi_termo * phivel) / M_PH` *(`:7760`)*: il termine del
termostato è ### **proporzionale alla `phivel` del nodo stesso.**
### ➜ ### **Su un nodo a velocità ZERO il termostato non può fare NIENTE** *(`xi·0 = 0`)*:
### **amplifica le velocità che ci sono**, e quelle che ci sono stanno ### **nel VUOTO.**

| il canale | come agisce | agisce su `phivel = 0`? |
|---|---|---|
| ### **`scuoti_vuoto`** | ### **ADDITIVO** *(`phivel += calcio`)* | ### ✔ **SÌ** — è il canale da cui la dispersione intra-massa TORNA |
| ### **il termostato** | ### **MOLTIPLICATIVO** *(`− xi·phivel`)* | ### ⛔ **NO** — amplifica il VUOTO, non le masse |
| la ### **coppia** | additiva, ma ### **non legge `phi`** nel ramo del driver *(`H2`)* | ### ✔ sì, ma non per riallineare |

> ### ⭐ **CONSEGUENZA DICHIARATA PRIMA DELLA CORSA:** nei primi passi il termostato
> ### **rifornisce il VUOTO** mentre le masse restano quiete, quindi ### **il contrasto
> MATERIA/VUOTO nelle VELOCITÀ cresce.** ### ⚠ **Che cosa questo faccia a `c_k` — che è una
> coerenza di CAMPO, non di velocità — NON lo so, e non lo indovino.**

### ⛔ **E SONO TRE CONFONDENTI, NON UNO. Li conto, perché il numero conta**

| | che cosa cambia oltre alla dispersione di fase | verso |
|---|---|---|
| ### **`1`** | `tau_tw` intra-massa, ### **fattore ~`2600`** | la torsione ### **non rilassa più** dentro le masse |
| ### **`2`** | `scuoti_vuoto` ### **ri-inietta** la dispersione | l'effetto ### **svanisce** nel tempo |
| ### **`3`** | ### **`−10.52 %`** di energia cinetica globale → termostato ### **rifornente**, ma ### **solo dove c'è già velocità** | il ### **VUOTO** viene scaldato, le masse no |

> ### ⛔ **QUINDI `H1` COSÌ COM'È SPECIFICATA NON È UN ESPERIMENTO A UNA VARIABILE, E LO DICO
> PRIMA DI GIRARLO.** ### ✔ **L'asimmetria del test resta quella scritta sopra, e vale ancora
> di più con tre confondenti invece di uno:** se l'`AUC` ### **resta bassa**, `H1 NON BASTA` è
> una conclusione ### **solida** *(tre vantaggi dati alle masse e nessuno è bastato)*; se
> ### **risale**, la causa è ### **ambigua fra quattro cause** e il referto dirà
> ### **CONFONDUTO.**
>
> ### ⭐ **E LA DECISIONE SE GIRARLO COSÌ O FERMARSI È DI LUCA.** ### **Io lo giro**, perché il
> mandato è esplicito e perché ### **il ramo che il mandato vuole davvero — «le masse si
> sciolgono anche con le velocità coerenti?» — è quello NON confondibile.**
