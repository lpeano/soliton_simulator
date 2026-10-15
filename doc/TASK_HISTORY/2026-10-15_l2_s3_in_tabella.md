# `L2`, QUINTO PEZZO — **`S3` ENTRA IN TABELLA AL POSTO DELLA SATURAZIONE**

*(decisioni di Luca del `2026-10-15`, `23:30` e `23:38`. Ultimo commit verificato dal
guardiano: `723cb5b`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE**, e il commit del codice ha questo
> come ### **antenato.** ### **E qui dentro c'e' anche la STELLA POLARE**, perche' questo
> e' ### **il primo commit del progetto che cambia una legge VERA della tabella.**

---

## 0. LA DECISIONE, COME LUCA L'HA PRESA — *e i cinque motivi sono MISURATI*

### **LA FORMA:** `N_k = rho_k · ln(rho_k / (rho_k + Lambda_k))`, con
`rho_k = somma_h |psi_h|^2` e `Lambda_k = somma_h |phi_h|^2`. Da cui:

```
alpha = dN/drho    = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)
beta  = dN/dLambda = -rho/(rho+Lambda) = -x/(1+x)        con x = rho/Lambda
```

### 📌 **E IL CONTO TORNA CON `S3` DEI PEZZI PRECEDENTI**, che e' la stessa funzione
scritta con `x`: `N = Lambda F(x)` con `F(x) = x ln(x/(1+x))`, e allora
`alpha = F'(x) = ln(x/(1+x)) + 1/(1+x)` e `beta = F - xF' = -x/(1+x)`.
### ✅ **Cioe' la legge che entra in tabella e' ESATTAMENTE quella che ho misurato**, non
una sua parente.

**I CINQUE MOTIVI, tutti con il loro numero e il loro commit:**

| | il motivo | il numero | dove |
|---|---|---|---|
| `a` | **lineare per poca materia** — il regime della materia reale se il vuoto e' planckiano | pendenza statica **`1.11`** | `ebf5317` |
| `b` | **satura per molta materia** | `beta -> -1` per `x -> infinito` | il conto |
| `c` | **rispetta il cono** nel senso del cambio di stato | **`0.80`** del passo libero *(`S2` lo VIOLA: `1.89`)* | `74ba200` |
| `d` | **il verso statico e' quello deciso**: la materia CONSUMA il vuoto | **`24` casi su `24`**, da `85` a `1560` barre | `ebf5317` |
| `e` | **la sovrapposizione vale** fuori dalla saturazione | scarto **`~2%`** a `x = 0.01` | `ebf5317` |

### **LA SOSTITUZIONE:** `S3` ### **SOSTITUISCE** `CAMM-SATURAZIONE`, ### **non le si
affianca.** I due motivi di Luca:
### **(a)** la saturazione con l'elicita' da' ### **per forza una fase anche al vuoto**
*(l'unica `H`)*, quindi lasciarla vorrebbe dire ### **lasciare un canale di gravita' che
dipende dallo spin** — in conflitto col principio di equivalenza;
### **(b) parsimonia:** ### **le leggi restano `7`.**

### ⚠⚠ **E UNA COSA CHE DEVO DIRE SUL MOTIVO (a), perche' il mio numero la dice:**
cambiare sorgente ### **toglie la dipendenza dallo spin DELLA SORGENTE, non della
DINAMICA.** Al primo tick le tre elicita' danno lo stesso `dLambda` *(`8.9e-17`,
`74ba200`)*, ### **ma a `2000` tick la differenza fra `+1` e isotropo era `7.4` barre**,
perche' la materia ### **si muove** in modo diverso per spinori diversi.
### ⛔ **Quindi la sostituzione CHIUDE un canale, e NON chiude la questione
dell'equivalenza.** ### **Lo scrivo qui perche' nessuno possa leggere questo commit come
<<l'equivalenza e' sistemata>>.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⭐⭐ **LA COSA CHE CREDO PIU' FORTE, e si DIMOSTRA invece di misurarsi:** questo
flusso e' ### **esatto per un motivo strutturale**, non per fortuna.
### **`N` dipende SOLO da `rho` e da `Lambda`**; il flusso mette ### **una FASE** su `psi`
e ### **una FASE** su `phi`; e ### **una fase non cambia ne' `rho` ne' `Lambda`.**
### ✅ **Quindi `alpha` e `beta` sono COSTANTI durante il pezzo**, e
`exp(-i a dtau/2) exp(-i a dtau/2) = exp(-i a dtau)` ### **in aritmetica esatta.**
### ⛔ **E' questo che rende `esatto: true` una DICHIARAZIONE VERIFICABILE e non una
promessa** — e il collaudo *«due mezzi fanno l'intero»* ### **misura gli ulp**, non
l'ordine.

### 📌 **E IL CONFRONTO CON LA SATURAZIONE DICE PERCHE' E' PIU' SEMPLICE:** la saturazione
mette su `psi` ### **una ROTAZIONE attorno a `n`** *(perche' la sua sorgente `h` e'
`s . n`, e `dh/dpsi*` ha segni opposti nelle due componenti)*; qui la sorgente e' `rho`, e
`drho/dpsi* = psi` ### **con lo stesso segno** → ### **una FASE.**
### ⚠ **E una rotazione attorno a `n` CAMBIA `h`** *(era il «l'elicita' nasce» che avevo
misurato)*, mentre ### **una fase NON cambia `rho`: il termine nuovo CONSERVA LA SUA
SORGENTE.**

### ⭐ **COSA MI ASPETTO DAI CONTROLLI DEL PUNTO 2, scritto PRIMA:**
1. **`L1` resta chiuso**: `_collauda_tempo_proprio.py` a ### **`0` violatori** — la legge
   nuova prende `dtau` ### **da `FP.dtau_nodo`**, come tutte;
2. **`M-B1`**: le leggi non toccate restano ### **identiche AL BIT**; la saturazione
   ### **NO, e non deve**, perche' il pezzo e' cambiato — ### **e se risultasse identica
   sarebbe il segnale che la legge nuova non e' entrata.**
3. **`M-B2`**: pendenza ### **`~2`**, perche' il palindromo non cambia e il pezzo nuovo
   e' ### **ancora un flusso esatto spezzato a meta';**
4. **la simmetria `(P Theta) W (P Theta)^-1 = W^-1`**: ### **deve REGGERE**, e il motivo
   e' che `alpha` e `beta` sono ### **funzioni REALI di grandezze INVARIANTI** sotto
   `P` e sotto `Theta` *(`rho` e `Lambda` sono moduli quadri)* — ### ⚠ **ma col termine
   NONLINEARE incluso non l'ho mai misurata, e il mandato ha ragione a chiederlo:**
   una simmetria che valeva sulla parte lineare ### **non e' la simmetria del passo.**
5. **la risposta statica DEVE coincidere con `S3` di `ebf5317`**: segno, pendenza a `x`
   piccolo, sovrapposizione. ### ⛔ **E se NON coincide, la legge in tabella non e' la
   legge che ho misurato** — e allora mi fermo.

### ⚠ **CIO' CHE NON SO:** quali collaudi cambiano esito *(il punto `2e` lo chiede, e
### **non lo indovino: lo misuro e li elenco con il motivo di ciascuno**)*; e se
`_collauda_energia.py` regga, perche' ### **l'energia cambia DEFINIZIONE** — `N` non e'
piu' la stessa funzione.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### ⛔⛔ **UN CONFLITTO CON LA GUIDA, E LO DICHIARO PRIMA DI TOCCARE UN FILE**

**`doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`, passo `1`:** *«la DECISIONE che governa la legge e'
`presa` nell'albero? Se il nodo NON e' `presa: true`, FERMATI»*.
### **Il nodo che governa questa legge e' `DEC-D6F-FORME-VUOTO`** — *«le TRE forme del
vuoto locale: tipo, quanti per nodo, **accoppiamento**»*, punto `(c)`: *«la forma
dell'accoppiamento con la fase, DA DERIVARE»*. ### ⛔ **E NON E' `presa`, perche' dipende
da `DEC-QC-CONSERVATA`** *(«esiste una quantita' conservata?»)*, che non e' presa —
e ### **`P-ALB` RIFIUTA** un nodo `presa` con una dipendenza non `presa`.

> ### ⭐ **COSA FACCIO, e seguo un PRECEDENTE DEL REPO invece di inventare:** nel nodo
> `DEC-D7-DIVISIONE` la stessa cosa e' gia' capitata, e la cura e' scritta la':
> ### **il CONTENUTO della decisione si registra nel nodo, verificabile, e `presa` resta
> `false` finche' le sue dipendenze non lo sono.**
> ### ⛔ **Quindi: registro il contenuto nella nota di `DEC-D6F-FORME-VUOTO`, lascio
> `presa: false`, e LO DICO A LUCA** — perche' la via d'uscita non e' mia: o si decide
> `QC`, o si dichiara che questa legge e' governata da un altro nodo.
> ### ⚠ **E la guida stessa dice che questo buco NON HA UN PRESIDIO:** *«nessuno verifica
> che una LEGGE non sia scritta prima della sua DECISIONE»*. ### **Non lo uso come
> permesso: lo uso come motivo per scriverlo in tre posti.**

### **E DUE COSE CHE LA TABELLA NON SA DIRE, e le dichiaro:**
### **(i) una LEGGE non ha un campo `stato` ne' `superata_da`** — lo schema dei campi di
un `flusso` e' chiuso *(`generatore`, `ambito`, `parametri`, `esatto`, `simmetrie`,
`conserva`, piu' `posto`/`voce_decisione`)*. ### **Quindi <<`CAMM-SATURAZIONE` passa a
SUPERATA>> si scrive dove un programma lo legge: nella VOCE `MOTORE-SATURAZIONE`**
*(`stato: SUPERATA`, `superata_da: CAMM-MATERIA-VUOTO`)*, piu' la scheda della legge.
### ⚠ **E lo riporto come un buco** *(`DECISIONE-VUOLE-UN-CAMPO`)*: ### **lo stato di una
legge oggi vive in prosa.**
### **(ii) l'ID della legge:** ### **`CAMM-MATERIA-VUOTO`** — descrittivo *(dice le due
cose che accoppia)*, `[A-Z][A-Z0-9-]{3,}`, unico nel vocabolario, e ### **nella famiglia
`CAMM-` come tutte le leggi della camminata.**

### **I PASSI, e cosa decide ciascuno**

| | il passo | che cosa DECIDE | che cosa mi FERMA |
|---|---|---|---|
| `1` | la **variabile `rho`** in tabella *(`reale_nodo`)*, e `stato.py` **generato** | che la sorgente sia **una variabile di stato**, non un calcolo di passaggio | se `P-E3`/`P-E10` rifiutano: **leggo il motivo e lo scrivo**, non aggiro |
| `2` | la **legge** `CAMM-MATERIA-VUOTO`, e `CAMM-SATURAZIONE` **fuori dall'ordine** | che le leggi restino **`7`** e che la sostituzione sia **nella tabella**, non nel motore | se il generatore rifiuta: **si cambia la TABELLA**, non il controllo |
| `3` | `primo_ordine/materia_vuoto.py`: `F`, `alpha`, `beta` **pure**, col caso `rho = 0` | che la singolarita' sia **ELIMINABILE e dichiarata**, non un pavimento | se mi trovo a scrivere un pavimento su `rho > 0`: **mi fermo** *(`A11`)* |
| `4` | l'operatore nel **motore**: **due fasi**, e nient'altro | che il flusso sia **esatto** | se non e' esatto: **`esatto: true` sarebbe una bugia** |
| `5` | il collaudo **«due mezzi fanno l'intero»**, con il caso che **DEVE fallire** | che `esatto` sia **verificato**, non promesso | se gli ulp non sono pochi: **mi fermo** |
| `6` | l'**energia** con la `N` nuova | che `E` sia **l'energia della legge che gira** | — |
| `7` | i **controlli** `(a)`-`(e)` del punto `2` | se la legge in tabella **E'** quella misurata | se la risposta statica **non coincide** con `S3` di `ebf5317`: **mi fermo** |
| `8` | i **documenti** e le schede | — | — |

### ⛔ **E NON TOCCO NESSUNA SOGLIA PER FAR PASSARE UN COLLAUDO** *(il mandato lo dice, e
l'ho appena fatto nel quarto pezzo lasciando rosso il braccio della conservazione)*: un
collaudo che cambia esito ### **si elenca col suo motivo.**

---

## 3. LA STELLA POLARE — *le cinque domande, PRIMA del codice*

### **`1` — `A14`: conserva energia e carica LOCALMENTE?**
### ✅ **LA NORMA SI': ESATTAMENTE E LOCALMENTE.** Il flusso moltiplica ogni `psi_h` e
ogni `phi_h` per ### **un numero di modulo `1`**, quindi `|psi_h|^2` e `|phi_h|^2`
### **non cambiano affatto** — ne' per nodo ne' per estremita'.
### ⭐ **E DI PIU': il flusso CONSERVA LE PROPRIE SORGENTI**, `rho_k` e `Lambda_k`, cioe'
### **conserva `N_k` stesso.** ### **E' la cosa che rende il flusso esatto.**
### ⚠ **L'ENERGIA NO, e non e' una novita' di questa legge:** `E` si conserva
### **all'ordine della composizione** *(`M-B2`, pendenza `~2`)*, perche' il passo e' una
composizione di Strang e non il flusso di `H` intera. ### **Questa legge non peggiora
quel conto, e il punto `2a` lo MISURA.**
### ⛔ **E LA CARICA: questa legge NON LA MUOVE AFFATTO** — `rho_k` e' invariante sotto il
suo flusso. ### **Il canale `materia -> vuoto` passa per `Lambda`, non per `rho`.**
*(`A14`, `CONSERVAZIONE-LOCALE`)*

### **`2` — a quale dei TRE GRADINI arriva?**
### **(a) robusto al rumore numerico: SI'**, ed e' il gradino a cui mi fermo — barre a
blocchi nei pezzi `3` e `4`, controlli al bit, `beta = 0` esatto, e il collaudo del flusso
agli ulp.
### **(b) regge togliendo la legge pratica: QUI IL CONFRONTO E' LA SOSTITUZIONE STESSA** —
la saturazione ### **viene TOLTA**, e il punto `2c` verifica che la risposta statica
### **sia la stessa misurata per sostituzione a runtime.** ### **Se coincide, il risultato
non dipendeva dal modo di applicare il termine.**
### **(c) coincide con un limite noto: PARZIALMENTE, e dico quanto.** La risposta statica
e' ### **LINEARE nella materia per `x` piccolo** *(pendenza `1.11`)*, che e' il regime
newtoniano ### **nella massa** — ### ⛔ **ma la LEGGE IN DISTANZA non e' misurata**: il
toro `31x31` non basta *(il profilo cambia segno a mezzo toro)*. ### **Non dichiaro un
limite noto che non ho verificato.** *(`ROBUSTEZZA-FISICA`)*

### **`3` — aggiunge un numero o una legge?**
### ⛔ **ZERO numeri: `parametri: {}`.** La scala e' ### **il vuoto locale**, come nella
saturazione — `x = rho/Lambda` e' ### **relazionale**, e non c'e' nessuna `g`.
### ⭐ **E ZERO leggi: le leggi restano `7`**, perche' questa ### **SOSTITUISCE** la
saturazione *(il criterio `9-ter`: «una cura non aumenta il numero delle leggi»)*.
### ✅ **Nessun clip, nessun pavimento, nessun tetto.** ### 📌 **L'unico caso speciale e'
`rho_k = 0`**, e ### **la' `psi = 0`: la fase di un vettore nullo non vuol dire niente**,
quindi `alpha = 0` e' ### **il valore che l'espressione PRENDE**, non una protezione —
### **una singolarita' ELIMINABILE, dichiarata nel codice e nella scheda.**
### ⛔ **E NESSUN PAVIMENTO SU `rho > 0`:** dove `rho` e' piccolo ma non nullo, `alpha` e'
grande e ### **si usa com'e'.** *(`A1-COSTANTI`, `CLIP-INVENTARIO`)*

### **`4` — tocca `rho`, `c_s` o il SEGNO? In quale VERSO?**
### ⛔⛔ **TOCCA `rho` NEL MODO PIU' FORTE POSSIBILE: `rho` DIVENTA LA SORGENTE**, e
entra nella tabella ### **come variabile di stato.** E il ### **SEGNO** e' quello
misurato: ### **la materia CONSUMA il vuoto** *(`24` casi su `24`)*.
### ⭐ **E IL VERSO E' BIDIREZIONALE NELLA LEGGE, al contrario della misura:** `beta` da'
al vuoto una fase che dipende dalla materia *(`materia -> vuoto`)*, e ### **`alpha` da'
alla materia una fase che dipende dal vuoto** *(`vuoto -> materia`)* — e quella fase
### **conta**, perche' il Grover e lo spostamento che seguono ### **interferiscono.**
### ⚠ **Cioe': la misura del quarto pezzo ESCLUDEVA la retroazione per costruzione
*(sorgente congelata)*, ma LA LEGGE CE L'HA.** ### **Due cose diverse, e non vanno
confuse.** *(`EM-CURVATURA-BIDIREZIONALE`)*

### **`5` — emergente o imposto?**
### ✅ **EMERGENTE, e c'e' un motivo meccanico oltre al controllo:** il termine scrive
### **SOLO FASI**, e una fase ### **non puo' cambiare `Lambda`** — quindi
### **nessuna riga di questa legge scrive un profilo di vuoto.** Il profilo nasce
### **dall'interferenza del hop.** ### **E `beta = 0` da' `0` ESATTO.**
### ⛔ **CIO' CHE E' IMPOSTO E' LA FORMA**, e lo dico senza girarci intorno: `S3` e'
### **una SCELTA DI LUCA fra quattro candidate misurate**, non una derivazione da un
principio. ### **La scheda lo scrive, e il posto dove si derivera' e' `D6f` dell'albero.**
*(`ROBUSTEZZA-FISICA`, gradino `b`)*

---

## 4. TODO DEL NEXT STEP — *la lista operativa*

1. **punto `0`**: la voce `[[DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA]]` con la decisione; la
   voce ### **nuova** per la collocazione in `L4` *(elicita' → torsione, NON operativa)*;
   `[[MOTORE-SATURAZIONE]]` a ### **`SUPERATA`** con `superata_da`; la nota in
   `DEC-D6F-FORME-VUOTO` col ### **conflitto dichiarato.**
2. **punto `1`**: `rho` in tabella · `CAMM-MATERIA-VUOTO` · l'ordine · `_genera.py` ·
   `materia_vuoto.py` · l'operatore nel motore · ### **il collaudo del flusso esatto** ·
   l'energia · la riga del registro dell'era `2` *(`P-E6`, STESSO COMMIT)* · la scheda in
   `REGISTRO_FISICA` *(`H-REG-R`)*.
3. **punto `2`**: i cinque controlli, ### **ognuno col suo numero**, e l'elenco dei
   collaudi che cambiano esito ### **col motivo di ciascuno.**
4. **punto `3`**: RIPRESA, mappa *(la forma decisa; resta aperta `cs(Lambda)`)*,
   inventario, schede.
5. ### **STOP.**
