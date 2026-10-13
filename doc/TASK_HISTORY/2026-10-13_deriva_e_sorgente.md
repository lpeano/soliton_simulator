# LA SORGENTE `O(dtau^2)` E LA DERIVA DI `E` — **e un numero ORFANO che ho scritto io**

> **Mandato di Luca, 2026-10-13, punto `1(c)`:** *«Con `N` sul tick `E` si conserva solo a
> `O(dtau^2)` (tua misura, rapporto `4.20`), quindi il bilancio locale ha una **SORGENTE di
> ordine `dtau^2`**: misurala per nodo e dichiarala.»*
>
> **E punto `2`:** *«Il tick compone due pezzi hamiltoniani esatti, quindi e' una mappa
> **simplettica**. Allora deve conservare esattamente un'energia modificata
> `E~ = E + dtau^2 E_2 + …`, e l'errore su `E` deve **OSCILLARE con ampiezza `O(dtau^2)`,
> SENZA deriva secolare**. Ge–Marsden: un passo simplettico a `dtau` fissato **non puo'**
> conservare `E` esattamente — l'`O(dtau^2)` e' **il prezzo di qualunque passo simplettico,
> non un difetto nostro.»*

> ### ✅ **Questo file si committa PRIMA del codice.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare, e cosa NON so*

### ⛔ **PRIMA COSA, ED E' UN DIFETTO MIO: IL RAPPORTO `4.20` E' UN NUMERO ORFANO.**

Il mandato lo cita come *«tua misura»*, e **lo e'**: l'ho scritto io nel task history del
`2026-10-12` *(`36182b7`)*. ### ⚠ **Ma NESSUNO SCRIPT COMMITTATO LO PRODUCE.** Ho cercato:
in `primo_ordine/` non c'e' niente che dimezzi `dtau` a tempo totale fisso, e il numero
compare **solo in prosa**, in quel file e nel task history di stamattina che lo ha
ricopiato.

### ⛔ **E' esattamente cio' che `L-NUMERI` vieta:** *«ogni numero scritto in un commit o in
un referto esce da uno script: un numero ricopiato NON HA PROVENIENZA»*.
### **Quindi non ci costruisco sopra: lo RIMISURO.** E registro il difetto come voce
*(`[[L-NUMERI-DERIVA-ORFANA]]`)*, perche' un difetto mio che non entra nell'indice
### **e' un difetto che mi ricapita.**

### ⚠ **SECONDA COSA, E QUESTA E' UNA PREMESSA CHE CREDO FALSA — la dico PRIMA.**

Il punto `2` del mandato dice che il tick **compone due pezzi hamiltoniani esatti**.
### ⛔ **Il pezzo lineare NON E' il flusso di un'hamiltoniana per un tempo `dtau`.**
Guardo `primo_ordine/composizione.py`, che e' **generato dalla tabella**:

```
('CAMM-SATURAZIONE',        0.5, 'flusso')          <- scala con dtau
('CAMM-MONETA-SPIN',          1, 'pezzo_unitario')  <- exp(-i eps dtau sigma.n): SCALA
('CAMM-GROVER',               1, 'pezzo_unitario')  <- (2/d) J - I: NON scala
('CAMM-SPOSTAMENTO',          1, 'pezzo_unitario')  <- psi'[compagna] = U psi: NON scala
('CAMM-GROVER-VUOTO',         1, 'pezzo_unitario')  <- NON scala
('CAMM-SPOSTAMENTO-VUOTO',    1, 'pezzo_unitario')  <- NON scala
('CAMM-SATURAZIONE',        0.5, 'flusso')          <- scala con dtau
```

### ⛔ **QUATTRO PEZZI SU SETTE NON DIPENDONO DA `dtau`.** Il Grover e' **un'involuzione**
*(`(2/d)J - I`)*, lo spostamento e' **una permutazione con trasporto**: a `dtau -> 0` il
tick **non tende all'identita'**, tende a ### **una mappa fissa e non banale.**
### ⭐ **E' un CAMMINO QUANTISTICO A TEMPO DISCRETO, non un integratore di un flusso.**

### ⛔ **DA QUI SEGUE CHE <<`E` conservata a `O(dtau^2)`>> NON PUO' VOLER DIRE <<per
tick>>:** se il tick cambia `E` di `O(1)` e il numero di tick raddoppia quando `dtau` si
dimezza, ### **a tempo totale fisso la deriva DOVREBBE CRESCERE, non dividersi per `4`.**

### ✅ **E CIO' CHE SO DI ESATTO, invece, e' questo:**

| | il fatto | perche' |
|---|---|---|
| ✅ | `Re<psi\|W psi>` e' **conservato ESATTAMENTE** dal pezzo lineare *(misurato `0.6` ulp)* | `Re<W psi\|W (W psi)> = Re<psi\|W psi>` per **qualunque** `W` unitario: e' **un'identita'**, non una proprieta' di `dtau` |
| ✅ | il flusso di saturazione **conserva i suoi propri coefficienti** `h` e `Lambda` *(`1.9` ulp)* | misurato il `2026-10-12`: e' il motivo per cui **due mezzi fanno l'intero** |
| ### ⛔ | il **termine del vuoto** `somma_k Lambda_k G(h_k/Lambda_k)` cambia di **`O(1)`** sotto il pezzo lineare | il pezzo lineare cambia `h_k` *(Grover e spostamento mescolano le estremita')*, e **`G` dipende da `h_k`** -- misurato `2.633` |
| ### ⛔ | e la **camminata del vuoto** cambia `Lambda_k`, quindi cambia **anche lei** quel termine | `Lambda_k = somma \|phi_h\|^2` sulle estremita' del nodo, e lo spostamento del vuoto **le muove** |

### ⭐ **QUINDI LA MIA PREVISIONE, SCRITTA PRIMA DEI NUMERI, E' CHE LA PREMESSA CADA:**
### **non mi aspetto `dtau^2`, mi aspetto `O(1)` per tick e una deriva che NON scende.**

### ⚠ **E NON LO DICO PER CONTRADDIRE IL MANDATO:** il mandato stesso dice
*«se cresce, la mappa non e' simplettica come crediamo, **e quello e' un risultato**»*.
### **Questo e' quel ramo**, e va misurato **invece di argomentato.**

### ⛔ **CHE COSA NON SO, e lo dico:**

1. **se la deriva sia davvero `O(1)` per tick** o se qualcosa che non vedo la riduca: il
   termine del vuoto potrebbe essere **piccolo** in modulo sulla scena che userei, e
   ### **piccolo non e' zero, ma su una finestra corta si confonde.**
2. **che cosa misurava il `4.20`**, perche' **non lo so ricostruire**: non c'e' lo script,
   e ### **non invento una ricostruzione plausibile per farlo tornare.**
3. se `E` come **l'ho definita** sia la grandezza giusta da chiedere conservata.
   ### ⚠ **Questa NON E' UNA MIA DECISIONE** *(`D-ENERGIA` e' di Luca)*: se la misura dice
   che il tick non la conserva, ### **la riferisco e non cambio la grandezza.**

---

### ⛔ **E I NOMI DELLE MISURE SI CITANO QUALIFICATI, perche' le forme NUDE COLLIDONO.**
Cercandolo nell'indice: ### **`M0`, `M1`, `M1b`, `M1c` e `M2` SONO GIA' ID**, e vogliono dire
altro — `M1` e' *«la materia e' uno stato, non una sostanza»*, `M2` e' *«la mitosi, due
difetti da acclarare»*, e `M0`, `M1b`, `M1c` sono voci **`NON_DEFINITA`** nate da citazioni.
### ⚠ **E `H-INDICE` LI HA FATTI PASSARE IN SILENZIO** scrivendoli nudi, rifiutando solo
`M0-bis`, `M0-ter` e `M1a` *(che non hanno un omonimo)*. ### ⭐ **E' esattamente il
difetto del punto `3` del mandato, capitato addosso a me mentre scrivevo questo file:** la
citazione nuda ### **non e' ambigua per il lettore, e' ambigua PER IL PRESIDIO.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e le letture fissate QUI*

### ⭐ **LE PREVISIONI, SCRITTE PRIMA DI VEDERE I NUMERI**

| | il passo | che cosa DECIDE | la previsione |
|---|---|---|---|
| `D-ENERGIA:M0` | **la deriva per tick**, al variare di `dtau` su `5` dimezzamenti | se la premessa del punto `2` regge | ### ⛔ **`O(1)`, NON `O(dtau^2)`**: mi aspetto che il rapporto fra dimezzamenti consecutivi **tenda a `1`**, non a `4` |
| `D-ENERGIA:M0-bis` | la deriva **del solo primo termine** | se l'identita' regge anche sul tick INTERO | ### ✅ **ulp**: il flusso non tocca `W`, e `W` conserva il suo valore d'attesa |
| `D-ENERGIA:M0-ter` | la deriva **del solo termine del vuoto** | **dove** sta la deriva | ### ⛔ **e' qui che sta tutta**: `O(1)`, e **non scende** con `dtau` |
| `D-ENERGIA:M1a` | **run lungo**, almeno `10x` il piu' lungo fatto finora | se la deriva e' **oscillante** o **secolare** | ### ⚠ **SECOLARE, non oscillante**: se il tick non e' simplettico in `E`, ### **non c'e' nessuna `E~` da conservare** |
| `D-ENERGIA:M1b` | **tre taglie**, fattore `>= 4` fra la piu' piccola e la piu' grande | se l'errore e' **estensivo** | ### ✅ **l'errore PER NODO resta costante**, il totale cresce col numero di nodi -- ### **questa previsione la credo**, perche' la densita' e' locale |
| `D-ENERGIA:M1c` | **per lunghezza d'onda**: stati iniziali lisci contro stati ruvidi | se l'errore **cade sui modi lunghi** | ### ⚠ **NON come `(dtau omega)^2`**, perche' non c'e' `dtau` nel Grover; ### **ma mi aspetto comunque che cada**, perche' uno stato liscio cambia `h_k` di meno |
| `c` | la **SORGENTE per nodo** `s_k = Delta E_k - (div J)_k` sul tick intero | il bilancio locale **con `N`** | ### ⛔ **`O(1)` e non `O(dtau^2)`**, per lo stesso motivo; ### **e la misuro per nodo come il mandato chiede, qualunque ordine venga** |

### ⚠ **E `D-ENERGIA:M3(ii)` -- `dtau` DIPENDENTE DALLO STATO -- NON LO MISURO IN QUESTO GIRO:** il
mandato dice che la' *«una deriva secolare e' possibile e va cercata esplicitamente»*.
### ⛔ **Ma se la deriva e' secolare GIA' a `dtau` fisso**, cercarla la' ### **non
distinguerebbe niente**: prima si stabilisce il caso semplice.

### ⛔ **CHE COSA MI FAREBBE FERMARE**

1. se `D-ENERGIA:M0-bis` **non** desse ulp, allora ### **il mio `E` non e' quello che credo**, e il
   difetto sta nella mia definizione — ### **si cerca la', non nella fisica.**
2. se `D-ENERGIA:M0` desse **davvero `4`**, allora ### **il mio ragionamento qui sopra e' sbagliato**,
   e la cosa da fare e' ### **capire QUALE pezzo scala con `dtau` senza che io lo veda** —
   non festeggiare che il numero torna.
3. se la deriva venisse **oscillante** *(`D-ENERGIA:M1a`)* nonostante `D-ENERGIA:M0` dicesse `O(1)`, i due
   risultati ### **sono incompatibili e si riconciliano**, non si scegli il piu' comodo.
4. ### ⚠ **E se la misura dicesse che il tick non conserva `E`, MI FERMO PRIMA DI
   PROPORRE UNA CURA:** `D-ENERGIA` e' una decisione di Luca, e
   ### **la grandezza promossa non la cambio io** — l'ho gia' sbagliato una volta, e la
   raccomandazione **l'ho ritirata stamattina.**

---

## 3. LA STELLA POLARE

| | la domanda | la risposta |
|--:|---|---|
| **1** | conserva **localmente**? | ### ⚠ **E' PROPRIO CIO' CHE QUESTO PEZZO MISURA**, e la previsione e' **NO**: una sorgente `O(1)` per nodo. ### ⛔ **E allora `A14` chiede di DICHIARARE la violazione**, che e' quello che faro' |
| **2** | **quale gradino**? | ### **NESSUNO: questo e' un pezzo di MISURA**, non una cura. Non promuove niente |
| **3** | **aggiunge un numero o una legge**? | ### ✅ **Nessuno dei due.** Uno strumento di misura **non e' una legge**, e non porta costanti |
| **4** | tocca `rho`, `c_s` o **il SEGNO**? | ### **No.** `J` ha un verso, ma e' quello **gia' sigillato** stamattina |
| **5** | **emergente o imposto**? | ### ⚠ **Niente dei due: e' una LETTURA.** ### ⛔ **E se la lettura dice che `E` non si conserva, la risposta e' DI LUCA** -- io riferisco |

---

## 4. TODO DEL NEXT STEP

1. registrare **`[[L-NUMERI-DERIVA-ORFANA]]`**: il `4.20` senza script e' un difetto mio.
2. `primo_ordine/deriva.py`: **la deriva di `E`**, dei suoi **due termini separati**, e la
   **sorgente per nodo** — con `--scrivi` per il referto.
3. `D-ENERGIA:M0`, `D-ENERGIA:M0-bis`, `D-ENERGIA:M0-ter`: il **rapporto fra dimezzamenti**, e **dove** sta la deriva.
4. `D-ENERGIA:M1a` *(run lungo)*, `D-ENERGIA:M1b` *(tre taglie)*, `D-ENERGIA:M1c` *(lunghezza d'onda)*.
5. `(c)` la **sorgente per nodo**, dichiarata.
6. il collaudo, con **un caso che deve fallire**.

---

## 5. ⭐ L'ESITO, CONTRO LE PREVISIONI — *e DUE RITIRI, uno chiesto e uno mio*

### ✅ **PRIMO RITIRO, CHIESTO DALLA VERIFICA ESTERNA** *(2026-10-13)*: *«La tua obiezione
al punto `2` del mandato e' giusta, e la verifica esterna la accetta. [...] L'argomento
dell'energia modificata `E~ = E + dtau^2 E2 + ...` **NON si applica**. Ritira dal task
history le previsioni basate su quella premessa.»*

### ⛔ **RITIRATE, e sono DUE:** *(a)* che l'errore su `E` **oscilli con ampiezza
`O(dtau^2)` senza deriva secolare**; *(b)* che l'errore **cada sui modi lunghi come
`(dtau omega)^2`**. ### **Nessuna delle due ha piu' una base: il tick non e' un
integratore di un flusso.** ### ✅ **Restano in piedi LE MIE, scritte in `7141812`.**

### ⚠ **E `L-NUMERI-DERIVA-ORFANA` VALE PER ENTRAMBI**, e la verifica esterna lo dice da
se': *«Anche il "4.20" era riportato dalla verifica esterna come "tua misura" senza
controllarne la provenienza»*. ### **Il difetto e' MIO nell'averlo scritto senza script, e
la catena si e' chiusa perche' NESSUNO DEI DUE ha chiesto da dove venisse.**

### ⭐ **LE MIE PREVISIONI, UNA PER UNA** *(i numeri in `doc/REFERTO_deriva_energia.md`)*:

| | la previsione | il numero | |
|---|---|---|---|
| `D-ENERGIA:M0` | `O(1)`, rapporti **verso `1` e non `4`** | i rapporti sono **`0.25`, `1.50`, `5.37`, `0.81`**: erratici, e ### **non `4`** | ✅ |
| `D-ENERGIA:M0-bis` | il primo termine a **ulp** | ### ✅ **`36` ulp sotto il SOLO pezzo lineare**; ### ⛔ **ma `8.845e-02` sotto `N`** | ⚠ |
| `D-ENERGIA:M0-ter` | il vuoto `O(1)`, **non scende** | confermato, ed e' **il termine dove sta la deriva** | ✅ |
| `D-ENERGIA:M1a` | **SECOLARE**, non oscillante | ### ⛔ **SBAGLIATA: rapporto `0.004`**, cioe' **nessuna tendenza secolare** -- ma l'ampiezza e' **`76`** su un `E(0) = 5.86` | ⛔ |
| `D-ENERGIA:M1b` | l'errore **per nodo costante** | **`3.29`, `2.90`, `2.47`** su un fattore `4` di taglia | ✅ |
| `D-ENERGIA:M1c` | cade sui modi lunghi, **non** come `(dtau omega)^2` | ### ⛔ **non cade in modo monotono**: a `x` fisso il minimo e' al **periodo `4`** *(`4.91`)*, e il periodo `32` sta a `10.2` | ⛔ |
| `(c)` | la sorgente **`O(1)` e non `O(dtau^2)`** | rapporti **`1.001`, `0.984`, `0.993`** *(`O(dtau^2)` darebbe `4`)*; e `s_k` vale **circa la META'** di `Delta E_k` | ✅ |

### ⚠ **SU `M0-bis` SONO ONESTO: la mia previsione era AMBIGUA**, e me ne accorgo adesso.
Avevo scritto *«il flusso non tocca `W`, e `W` conserva il suo valore d'attesa»*: e' vero
che `W` non cambia, ### **ma `N` cambia `psi`, e quindi cambia `Re<psi|W psi>`.** ### **La
previsione vale per il pezzo lineare DA SOLO**, e sul tick intero ### **non vale.** ### ⛔
**Non la conto come confermata.**

---

## 6. ⛔ TRE DIFETTI DELLA MIA MISURA, trovati MISURANDO — *e due li ho trovati prima del mandato*

| | il difetto | come si vedeva | la cura |
|---|---|---|---|
| `1` | ### ⛔ **IL REGIME ERA VACUO:** col `psi` normalizzato su tutto il grafo `x = \|h\|/Lambda ~ 1/(2m)`, e `G(x) = x - arctan x` va come `x^3/3` | il termine del vuoto valeva **`1.6e-05`** e `max\|h/Lambda\| = 0.033` | il regime **`locale`**, dove `x` e' di ordine `1`; e la **scansione in `x`** che il mandato chiede |
| `2` | ### ⛔ **MISURAVO `fine - inizio` INVECE DELL'ESCURSIONE** | `E` oscilla di **`76`** su una scala di `6`: ### **`fine - inizio` era un CAMPIONE A CASO** di quell'oscillazione | `escursioni()`, cioe' `max - min`; ed e' cio' che la verifica esterna ha misurato sul banco |
| `3` | ### ⛔ **LA DECOMPOSIZIONE DI `(c)` ERA VACUA** | le due righe *(col vuoto che cammina e senza)* coincidevano **a TUTTE le cifre** | **provato** invece di dedotto: con `\|phi\|` uniforme `Lambda_k` e' invariante a **`4.4e-16`**, e il controllo positivo *(`\|phi\|` non uniforme)* cambia di **`2.16`** |

### ⭐ **E IL DIFETTO `1` L'HO TROVATO MISURANDO, un'ora prima che il mandato arrivasse:**
la prima corsa dava tutto a `1e-5` e ### **i rapporti erratici** -- ed era la mia stessa
condizione di stop numero `2`, scritta in `7141812`: *«che il termine del vuoto non sia
PICCOLO sulla scena che userei: piccolo non e' zero, ma su una finestra corta si confonde
con zero»*. ### ✅ **La condizione di stop ha funzionato**, ed e' il motivo per cui si
scrivono prima.

### ⚠ **E IL DIFETTO `2` SPIEGA PERCHE' `M1b` SEMBRAVA FALSA:** con `fine - inizio` dava
`0.19`, `0.55`, `0.005` per nodo *(erratico)*; con l'escursione da' **`3.29`, `2.90`,
`2.47`**. ### ⛔ **La previsione era giusta e la MISURA era sbagliata**, e senza accorgermene
avrei scritto che l'estensivita' non vale.

---

## 7. ⛔ LA CONDIZIONE DI STOP DEL MANDATO E' SCATTATA — **`[[DOMANDA-E-NON-SI-CONSERVA-A-X-UNO]]`**

> **Il mandato:** *«Se nel regime `x ~ 1` la somma non si conserva (escursione della somma
> `>=` quella dei termini), **FERMATI e porta il risultato a Luca**: e' la base della
> promozione, e la grandezza promossa non la cambi tu (lo hai scritto tu stesso).»*

### ⛔ **SCATTA, e non di poco:** a `x = 0.970` l'escursione della **somma** e' `2.084e+01`
contro `1.551e+01` del primo termine e `1.120e+01` del vuoto. ### **E scatta in OGNI punto
della scansione:** i due termini **non si compensano, si sommano.**

| `x` max | escursione della somma / **scala naturale** |
|--:|--:|
| `0.0152` | `1.26e-06` |
| `0.242` | `3.34e-03` |
| **`0.970`** | **`5.77e-02`** |
| `3.88` | `2.77e-01` |
| `62.1` | `4.40e-01` |

### ⭐ **SEI ORDINI DI GRANDEZZA, in modo monotono:** nel regime vacuo `E` sembra
conservata; ### **nel regime in cui la saturazione lavora oscilla del `5.8%` della sua
scala in `400` tick**, e a `x ~ 4` del `28%`.

### ⛔ **MI FERMO SU QUESTO PEZZO E LO PORTO A LUCA**, come il mandato dice. ### ⚠ **E NON
raccomando di cambiare la grandezza promossa:** l'ho raccomandato il `2026-10-12` su una
base sbagliata e ### **l'ho ritirato stamattina** -- non rifaccio lo stesso passo su una
base diversa. ### ✅ **Raccomando di DICHIARARE la violazione coi numeri** *(`A14` lo
chiede)* **e di tenere la domanda aperta finche' le misure delle BANDE hanno girato**: quel
mandato cerca proprio **una combinazione che torni sul tick intero**, quindi ### **puo'
rispondere a questa domanda invece di lasciarla a un giudizio.**

### ⚠ **E CHE COSA NON SO, e lo dico:** se il regime `x ~ 1` sia **FISICO**. Ci arrivo
indebolendo il vuoto a `|phi| = 2` con `psi` di ampiezza di ordine `1` per estremita', e il
banco congelato sta a `x ~ 1e-3`. ### ⛔ **Quale dei due sia il regime in cui il simulatore
deve lavorare E' UNA DECISIONE DI FISICA, non una mia scelta di misura.**
