# L'INFRASTRUTTURA DELL'ERA `2`, TERZA PARTE — **il mandato `4` di `6`**

> ### 📌 **IL RITO:** questo file si committa e si pusha ### **PRIMA del lavoro**, così
> l'ordine è ### **verificabile da git** invece che **asserito da me**.

> **I sette punti:** `1` determinismo · `2` dimensioni · `3` simmetrie e conservazioni ·
> `4` il grafo valido · `5` hook come barriera, CI come rete · `6` i tempi ·
> `7` la guida. ### ⛔ **Nessuna fisica nuova; simulatore `b8c21049` intatto;
> commit+push a OGNI punto; ogni presidio collaudato NEI DUE VERSI; ogni controllo con la
> sua voce nell'indice.**

---

## `1.` RAGIONAMENTO PRELIMINARE — ### **cosa credo PRIMA di guardare, e cosa NON so**

### **LA FORMA DI QUESTO MANDATO**

I tre precedenti erano ### **uno di scrittura** *(il piano)*, ### **uno di applicazione**
*(le `43` decisioni)*, ### **uno di costruzione** *(l'infrastruttura)*. ### ⭐ **Questo è
di IRRIGIDIMENTO: prende cose che oggi FUNZIONANO PER ABITUDINE e le rende
OBBLIGATORIE.** ### 📌 **E il piano che ho appena scritto lo dice già di una di esse:**
la forma bilineare è *«già vera senza essere una regola»*, e ### **finché il generatore non
la pretende è un'abitudine.** ### **Questo mandato fa, su sette fronti, quel passaggio.**

### **DUE TRAPPOLE CHE VEDO GIA', e che scrivo PRIMA di toccare niente**

| | la trappola | perché conta |
|---|---|---|
| `a` | ### ⛔ **IL PUNTO `5` PUO' ROMPERE LA CI.** Il mandato dice che ogni strumento dell'era `2` *«verifica all'avvio che i hook siano ATTIVI … e ### **si RIFIUTA di partire** se non lo sono»*. ### ⚠ **Ma nella CI i hook NON SONO ATTIVI** — `core.hooksPath` non è impostato in un `checkout` pulito — ### **quindi ogni strumento si rifiuterebbe di partire e la CI fallirebbe SEMPRE.** | ### **Non è un dettaglio di configurazione: è una contraddizione dentro il mandato.** ### ✅ **La lettura che fisso: la barriera è LOCALE, e il controllo deve riconoscere di NON essere in locale** *(`CI=true` lo dichiara GitHub)*. ### ⛔ **E lo dichiaro come MIA INFERENZA, perché il mandato non lo dice** |
| `b` | ### ⛔ **IL PUNTO `1` CHIEDE DUE PROCESSI <<BYTE-IDENTICI>>, e i dati di oggi sono in `.npz`** — che è ### **un ZIP**, e un'intestazione ZIP porta ### **la data e l'ora.** ### **Quindi due processi NON daranno file byte-identici**, e non per colpa del determinismo. | ### ⭐ **Se non lo guardo prima, misuro il formato del contenitore e lo chiamo non-determinismo.** ### ✅ **La lettura che fisso: l'identità si misura sui CONTENUTI** *(gli array, confrontati al bit)* ### **e sul TIMBRO**, non sui byte del file — ### **e se è così, lo DICO invece di far finta che il criterio fosse quello** |

### **CHE COSA CREDO PRIMA DI GUARDARE**

| | quello che credo | perché potrebbe essere falso |
|---|---|---|
| `c` | il punto `4` *(il grafo valido)* è ### **il più facile**: `passo.py::strati` usa già una chiave canonica `(min,max)`, e il driver costruisce il grafo da `grafo(scena,nodi)` | potrei scoprire che ### **nessuno controlla il grafo DOPO la costruzione**, e che il controllo va messo ### **a ogni passo**, come il punto chiede — e <<a ogni passo>> ### **costa**, quindi il budget del punto `6` lo vedrà |
| `d` | il punto `2` *(le dimensioni)* si appoggia a `FORME_DOMINIO`, che ### **c'è già** | ### ⚠ **ma `FORME_DOMINIO` dice il DOMINIO** *(`finito`, `finito-pos`, `fase-2pi`)*, ### **non la DIMENSIONE** — sono due cose diverse, e confonderle sarebbe ### **dichiarare un controllo che non c'è** |
| `e` | il punto `3` *(le simmetrie)* è ### **il più difficile**, perché *«verifica SIMBOLICAMENTE»* vuol dire ### **sympy su `psi -> psi e^{i theta}`** | e la mia tabella ha ### **`3` leggi, tutte di PROVA**: una simmetria verificata su una legge finta ### **non dice niente sulla fisica** — dice solo che ### **la macchina funziona**, e il referto deve scriverlo così |
| `f` | il punto `6` *(un solo comando, `collauda.py`)* è ### **mezzo fatto**: i collaudi ci sono tutti, e so già che ### **i lenti superano i `120` secondi** | potrei scoprire che ### **la somma dei veloci** supera già il budget, e allora ### **il budget va DICHIARATO, non scelto per far passare il numero** *(`A1`: la legge, non il numero)* |

### **CHE COSA NON SO, e lo scrivo adesso**

1. ### **se esista un RNG globale da qualche parte in `primo_ordine/`.** Credo di no — il
   driver passa un `seme` — ### **ma non l'ho verificato con l'AST**, e il punto `1` lo
   chiede proprio così.
2. ### **quanto costa il controllo del grafo A OGNI PASSO.** Il punto `4` lo chiede, il
   punto `6` dà un budget, e ### **i due punti si parlano**: potrei dover misurare il
   costo e ### **dichiararlo**.
3. ### **se `doc/COME_SI_AGGIUNGE_UNA_LEGGE.md` si possa davvero ESEGUIRE.** Il punto `7`
   chiede un collaudo che *«LA ESEGUE passo per passo»*: ### ⚠ **se la guida contiene un
   passo che richiede una DECISIONE** *(«scegli la forma del termine»)*, quel passo
   ### **non è eseguibile** — e allora la guida va scritta in modo che
   ### **ogni passo eseguibile sia MECCANICO**, e i passi di decisione siano
   ### **dichiarati tali.**

---

## `2.` PROGETTAZIONE DEL RAGIONAMENTO

### **L'ORDINE, e perché**

| | il punto | perché qui |
|---|---|---|
| `1` | ### **`4` il grafo valido** | ### **il più contenuto**, e dà subito la misura del costo che il punto `6` dovrà mettere in budget |
| `2` | ### **`1` il determinismo** | ### **viene prima delle simmetrie** perché un collaudo di simmetria su un sistema non deterministico ### **non si può ripetere** |
| `3` | ### **`2` le dimensioni** | si appoggia allo schema delle leggi, ed è ### **indipendente** dagli altri |
| `4` | ### **`3` simmetrie e conservazioni** | il più difficile, e ### **pretende `1`** |
| `5` | ### **`5` hook e CI** | ### **tocca OGNI strumento**, quindi va fatto quando gli strumenti nuovi ci sono già |
| `6` | ### **`6` i tempi** | ### **misura tutto il resto**: deve venire dopo |
| `7` | ### **`7` la guida** | ### **descrive il rito finito**, e un rito che cambia mentre lo scrivi si scrive due volte |

### **LE LETTURE, FISSATE ADESSO**

| | la misura | la lettura che fisso PRIMA |
|---|---|---|
| il determinismo | due processi, stessa configurazione | ### **gli ARRAY devono coincidere AL BIT** e il ### **timbro** deve essere lo stesso. ### ⛔ **I byte del `.npz` NO, e il perché va scritto: è un ZIP e porta la data** |
| l'RNG globale | l'AST su `primo_ordine/` | ### **`0` usi di `numpy.random.<funzione>`**; solo `Generator` con seme. ### **Se ne trovo, è un difetto e si cura** |
| il grafo a ogni passo | il costo | ### **si MISURA e si dichiara.** Se costa più del `10%` del passo, ### **lo dico invece di nasconderlo** |
| le dimensioni | un termine sbagliato | ### **DEVE essere rifiutato**, e ### **per la chiave giusta** — non per un errore qualsiasi |
| le simmetrie | `U(1)` su ogni termine | ### **verificata SIMBOLICAMENTE.** ### ⚠ **E su `3` leggi di PROVA: il referto dirà che misura LA MACCHINA, non la fisica** |
| i tempi | la somma dei collaudi | ### **il budget si DICHIARA su ciò che si misura**, non si scegle per far passare il numero (`A1`) |
| la guida | il collaudo che la esegue | ### **ogni passo MECCANICO si esegue**; un passo che richiede una ### **decisione** è ### **dichiarato tale** e non si esegue |

### **CHE COSA MI FAREBBE FERMARE**

| | il caso | che faccio |
|---|---|---|
| `a` | il controllo dei hook del punto `5` ### **rompe la CI** | ### ✅ **l'ho previsto sopra:** il controllo riconosce di non essere in locale. ### **Lo DICHIARO come mia inferenza** e proseguo |
| `b` | un controllo a ogni passo costa ### **più del passo stesso** | ### **FERMO e lo scrivo**: un presidio che decuplica il costo ### **si spegne il primo giorno**, e `A9` dice che allora non è un presidio |
| `c` | una simmetria dichiarata ### **non è vera** per un termine di prova | ### ⛔ **NON cambio il termine per far passare il presidio.** Il termine è di PROVA: ### **o la simmetria si dichiara come NON soddisfatta, o il presidio ha ragione** — e in entrambi i casi si scrive |
| `d` | la guida ha un passo che ### **non si può eseguire** | ### **lo dichiaro passo di DECISIONE**, e il collaudo verifica che ### **sia dichiarato**, non che si esegua |

### **LA STELLA POLARE** *(`L-STELLA`)*

### ⚠ **NON SI APPLICA, e il perché è parte della risposta:** questo mandato
### **non aggiunge nessuna legge alla tabella** e ### **non fa girare nessuna scena di
fisica** — irrigidisce la macchina. ### ⛔ **Ma tocca il GENERATORE** *(punti `2` e `3`)*,
e un generatore che rifiuta una forma ### **restringe la fisica che si potrà scrivere**:
### ✅ **quindi la quinta domanda — <<emergente o imposto?>> — ha una risposta che
scrivo adesso: ogni rifiuto di questo mandato è IMPOSTO, ed è imposto SULLA FORMA, non sul
risultato.** ### **Un presidio che rifiutasse un RISULTATO sarebbe un'altra cosa, e non ce
n'è.**

---

## `3.` TODO DEL NEXT STEP

- [ ] punto **`4`**: il **grafo valido a ogni passo**, col **costo MISURATO**
- [ ] punto **`1`**: **determinismo** — AST sull'RNG, BLAS a un thread **e timbrato**, versioni bloccate, due processi
- [ ] punto **`2`**: le **dimensioni**, e un termine sbagliato **rifiutato per la chiave giusta**
- [ ] punto **`3`**: **simmetrie** *(simboliche)* e **conservazioni** *(numeriche)*
- [ ] punto **`5`**: i **hook come barriera**, col caso **CI** dichiarato
- [ ] punto **`6`**: **`primo_ordine/collauda.py`**, i tempi, e il **budget dichiarato**
- [ ] punto **`7`**: **`doc/COME_SI_AGGIUNGE_UNA_LEGGE.md`**, e il collaudo **che la esegue**
- [ ] il **referto** `doc/REFERTO_infrastruttura_era2_terza.md`, e `_avanzamento.md`

---

## `4.` ANNOTAZIONI — ### **scritte DOPO, e il sopra NON si riscrive** *(par. `8`)*

| | che cosa avevo scritto sopra | che cosa ho MISURATO |
|---|---|---|
| `b` | la trappola `(b)`: *«il punto `1` chiede due processi ### **byte-identici**, e i dati sono in `.npz` — che è ### **uno ZIP**, e un'intestazione ZIP porta ### **la data e l'ora**. Quindi due processi ### **NON daranno file byte-identici**»* | ### ⛔ **ERA SBAGLIATA, e il perché è MISURATO:** `numpy.savez` scrive `date_time = (1980, 1, 1, 0, 0, 0)` nell'intestazione dello ZIP — ### **AZZERA l'ora.** ### ✅ **Quindi l'identità al byte è STRUTTURALE, non fortuna, e il criterio del mandato vale COME E' SCRITTO:** `548` byte di dati e `1442` di timbro, ### **identici fra due processi.** ### ⭐ **E l'ho verificato invece di assumerlo in ENTRAMBE le direzioni: prima ho confrontato due corse, poi ho letto l'intestazione dello ZIP per sapere se l'identità era FORTUNA** *(due corse a meno di `2` secondi starebbero nella stessa finestra dello ZIP)*. ### **Era struttura.** |
| `g` | *(nulla: non l'avevo previsto)* | ### ⚠ **IL TIMBRO STAVA PER MENTIRE.** `avvia()` restituisce *«ero in tempo?»*, e il timbro lo richiama — ### **quando `numpy` c'è già.** Il driver lo chiama ### **prima** di `import numpy`, e il timbro diceva `in_tempo: false`. ### ✅ **Curato: il verdetto è quello della PRIMA chiamata del processo** *(`_PRIMO`)*. ### **L'ho visto perché ho guardato il timbro dopo averlo scritto, non perché l'avessi previsto.** |
| `h` | *(nulla)* | ### ⚠ **NON POSSO VERIFICARE IL NUMERO DI THREAD: `threadpoolctl` non è installato.** ### ⛔ **Quindi lo DICHIARO nel docstring invece di far finta** — e la cosa che conta si misura altrimenti: ### ✅ **se due processi danno byte identici, i thread NON stanno rompendo il determinismo, qualunque sia il loro numero.** ### **Quello è il controllo vero, e c'è.** |
| `i` | l'ordine dei punti: `4` prima, poi `1` | ### ✅ **rispettato**, e il punto `4` ha dato subito il numero che il punto `6` dovrà mettere in budget: ### **`5.70%` di un passo.** |
