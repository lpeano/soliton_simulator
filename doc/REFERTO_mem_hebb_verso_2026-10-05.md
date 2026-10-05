# REFERTO -- `MEM-HEBB-VERSO`, PASSO (1): **LA MISURA**

*(mandato di Luca del 2026-10-04, eseguito il 2026-10-05 sul blob **`e2940b3c`**; le decisioni e `LA STELLA POLARE` sono in
`doc/TASK_HISTORY/2026-10-04_mem-hebb-verso-misura.md`, committato **prima** in
`b7e5a89`; lo strumento in `f5613ba`.)*

> ### ⛔ **E' UNA MISURA, NON UNA CURA.** Nessun `PASSA`/`FALLISCE` **fuori dai
> ### controlli**, e il simulatore **non e' stato toccato**.

| | |
|---|---|
| simulatore | `e2940b3c` *(non toccato)* |
| strumento | `4f75afd8` |
| copia patchata | `7a12c21b`, **3 ancore** |
| scena | `--nmasse 3 --sep 6.1158`, seme `11` |
| corse | **`72`** e **`150`** passi |
| configurazione | **`81`** booleani di modulo, ### **`ZERO` differenze dal driver** |
| piattaforma | `python 3.13.2` · `numpy 2.3.0` · Windows 11 · AMD64 |

## I TRE CONTROLLI CHE POSSONO FALLIRE — **tutti e tre PASSANO**

*(Fissati e committati **prima** di girare, in `b7e5a89`.)*

| | | `72` passi | `150` passi |
|---|---|--:|--:|
| **`C1`** | confronti | `72` | `150` |
| | archi confrontati | `33 952 696` | ### **`70 773 112`** |
| | ### con **DIFFERENZE** | ### **`0`** | ### **`0`** |
| | max scarto | `0.000e+00` | ### **`0.000e+00`** |
| **`C2`** | la **DECISA** non e' zero in | `0` | ### **`0`** |
| | `max abs(decisa)` | `0.000e+00` | ### **`0.000e+00`** |
| | ### **IL POSITIVO:** la **VECCHIA** e' zero in | `0` | `0` |
| | il **minimo** dei suoi massimi | `4.3154` | ### **`4.3154`** |
| **`C3`** | la **DECISA** differisce in | `0` | ### **`0`** |
| | la **VECCHIA** non e' opposta in | `0` | ### **`0`** |

> ### ✅ **`C1` PASSA AL BIT su `70 773 112` ARCHI, con max
> ### scarto `0.000e+00`.**
> ### **Questo e' il numero che rende la misura leggibile:** la forma vecchia che
> ricalcolo a lato ### **non e' una mia versione della legge, E' la legge** — bit per
> bit, su settanta milioni di archi. ### **E lo avevo dichiarato come il controllo piu'
> esposto**, perche' `np.sum` su un prodotto dipende dall'ordine delle somme: ### **non
> e' stato necessario ammorbidirlo.**

### ✅ **E `C2` HA DATO ANCHE LA SUA META' POSITIVA:** la forma decisa da' `0.000e+00`
sotto traslazione rigida, e la vecchia ### **non da' mai zero** — il **minimo** dei suoi
massimi, sui `150` passi, e' `4.3154`.
### **Senza quella meta', lo zero della decisa sarebbe potuto venire da uno strumento
che non calcola niente: sarebbe stato un FALSO-ZERO.**

## (a) `d0`: LA FORMA VECCHIA CONTRO LA FORMA DECISA

### ⛔ **IL RISULTATO PRINCIPALE, e lo chiamo cosi' perche' lo avevo deciso PRIMA di
### vedere il numero: IL TAGLIO MORDE, E MOLTO**

> Nel task history, rispondendo al **gradino (b)** della stella polare, avevo scritto:
> *<<se quasi tutti gli archi SATURANO, allora cio' che si osserva non e' la legge: e'
> IL TAGLIO ... se la frazione di saturi e' alta, il referto deve dirlo come risultato
> principale, non come nota>>*. ### **Eccolo.**

| frazione di archi **SATURI** al taglio `passo_max = 0.01*mediana(d0)` | `72` passi | `150` passi |
|---|--:|--:|
| forma **vecchia** | **`0.387431`** | ### **`0.396456`** |
| forma **decisa** | **`0.519298`** | ### **`0.552806`** |

*(saturo = `abs(proj) > passo_max` **prima** del taglio; su `70 773 112` archi-passo)*

### **COME SI LEGGE, e lo scrivo senza ammorbidirlo e senza gonfiarlo:**

1. ### **NON e' `~1`:** fra il `0.4` e il `0.6` degli archi-passo. ### **Quindi
   la legge NON e' invisibile dietro il taglio**, e il gradino (b) ### **non e'
   fallito.**
2. ### ⛔ **MA NON E' NEMMENO PICCOLO: fra il `40%` e il `55%`.** Su circa meta' degli
   archi-passo ### **cio' che `d0` riceve non e' `proj`: e' `+/- passo_max`**, cioe'
   ### **il taglio, non la legge.** E su quegli archi ### **cambiare la FORMA di `proj`
   cambia SOLO IL SEGNO** del valore applicato.
3. ### **E la forma decisa satura PIU' della vecchia** *(`0.553` contro `0.396`)*, perche' i suoi valori sono piu' grandi:
   la mediana di `abs(proj)` passa da `1.362e-02` a `2.524e-02`,
   ### **circa il doppio.** ### **E' un fatto, non un difetto** — ma significa che la
   cura della decisione (1) ### **arriverebbe in un regime in cui il taglio morde di
   piu'**, e Luca deve saperlo **prima** di decidere la cura.

### **LA DISTRIBUZIONE DI `abs(proj)` PRIMA DEL TAGLIO** *(aggregata sui `150` passi)*

| forma | min dei min | mediana delle mediane | mediana dei `p99` | max dei max |
|---|--:|--:|--:|--:|
| **simulatore** | `1.229e-10` | `1.362e-02` | `5.627e-01` | `7.561e+00` |
| **vecchia** | `1.229e-10` | `1.362e-02` | `5.627e-01` | `7.561e+00` |
| **decisa** | `2.687e-11` | `2.524e-02` | `8.338e-01` | `8.224e+00` |

### ✅ **E LE PRIME DUE RIGHE SONO IDENTICHE, cifra per cifra: e' `C1` visto da
un'altra parte.** La riga <<simulatore>> e' il `proj` che il simulatore calcola, la riga
<<vecchia>> e' quello che ricalcolo io: ### **se differissero, la terza riga non
vorrebbe dire niente.**

**Il taglio, misurato:** `passo_max` va da `1.876524e-02` a `2.122035e-02`.

### **IL SEGNO: CAMBIA SU META' DEGLI ARCHI, e il numero e' STABILE**

| | `72` passi | `150` passi |
|---|--:|--:|
| archi in cui **il segno cambia** fra le due forme | `16 819 117` | `35 161 140` |
| su archi **vivi** *(entrambe non nulle)* | `33 952 696` | `70 773 112` |
| ### **frazione** | ### **`0.495369`** | ### **`0.496815`** |

> ### **`0.4968`: su circa UN ARCO SU DUE le due
> ### forme spingono `d0` in VERSI OPPOSTI.**
> E il numero ### **non si muove fra `72` e `150` passi** *(`0.4954` contro `0.4968`)*: ### **non e' un transitorio.**

### ⚠ **E <<meta'>> NON vuol dire <<a caso>>, e non lo so:** una frazione vicina a
`0.5` e' **compatibile** con due forme scorrelate, ### **ma anche con una correlazione
che non ho misurato.** ### **Non traggo la conclusione**, e dichiaro che per trarla
servirebbe un'altra misura *(p.es. la correlazione fra i due `proj`, non solo il segno)*.

### **LA SOMMA CON SEGNO DI `Delta d0`: CAMBIA SEGNO E CRESCE DI UN ORDINE**

| | `72` passi | `150` passi |
|---|--:|--:|
| forma **vecchia** | `1.5268e+03` | ### **`6.6582e+03`** |
| forma **decisa** | `-5.0866e+04` | ### **`-9.2221e+04`** |

> ### ⛔ **E' LA DIFFERENZA PIU' GROSSA DI TUTTA LA MISURA, e non e' il segno per
> ### arco: e' il BILANCIO.**
> La forma vecchia somma ### **POSITIVO**, la decisa ### **NEGATIVO**, e in modulo la
> decisa e' ### **`13.9` volte** la vecchia.
> ### **In parole: con la forma di oggi le lunghezze di riposo, nel complesso, CRESCONO;
> ### con la forma decisa CALANO, e di molto di piu'.**

### ⚠ **CHE COSA QUESTO NUMERO NON DICE, e va detto:** ### **non dice quale delle
due sia giusta.** La forma decisa e' quella che Luca ha **deciso** per le sue
**proprieta' di simmetria** *(verificate: `C2` e `C3`)*, ### **non per il segno del suo
bilancio.** ### **E una somma che cala non e' <<peggio>> ne' <<meglio>>: e' un'altra
dinamica**, e misurarla era il punto di questo passo.
### ⛔ **Ma e' il numero che dice che la cura della decisione (1) NON e' una
riscrittura cosmetica: cambia il bilancio di `d0` di un ordine di grandezza.**

## (b) LA FASE: **il `97.3%` dei contributi viene SCARTATO IN SILENZIO**

| | `72` passi | `150` passi |
|---|--:|--:|
| archi-passo | `33 952 696` | `70 773 112` |
| nodi con **piu' di un arco** come primo estremo | da `12442` a `12442` | da `12442` a `12443` |
| il massimo di archi su **UN** nodo | `90` | `90` |
| contributi **applicati** | `908 941` | `1 925 336` |
| contributi ### **SCARTATI** | `33 043 755` | ### **`68 847 776`** |
| ### **frazione scartati** | ### **`0.973229`** | ### **`0.972796`** |
| somma dei **moduli applicati** | `1.8376e+04` | `3.4531e+04` |
| somma dei **moduli SCARTATI** | `6.7661e+05` | ### **`1.2514e+06`** |
| ### **rapporto scartati/applicati** | ### **`36.82`** | ### **`36.24`** |

> ### ⛔ **IL SITO APPLICA IL `2.7%` DI CIO' CHE CALCOLA, E SCARTA IL RESTO IN SILENZIO.**
> In moduli: ### **per ogni unita' di spostamento di fase applicata, `36.2` vengono buttate.**

**PERCHE':** `self.phi[ii] = (self.phi[ii] + shift) % self._dphi()` *(`:9531`)*, con
`ii` che ### **contiene ripetizioni** — un nodo e' primo estremo di fino a **`90`** archi. In numpy l'indicizzazione fancy **in
scrittura** fa ### **vincere l'ULTIMO**, e tutti gli altri contributi ### **sparicono
senza traccia.**

### ⛔ **E QUESTO E' IL NUMERO CHE RISPONDE ALLA DOMANDA 5 DELLA STELLA POLARE, come
### l'avevo posta io stesso prima di misurare:** avevo scritto che *<<se la somma dei
moduli scartati e' molto piu' grande di quella applicata, allora cio' che il sito fa
oggi NON E' la legge che il commento descrive, ed e' un ARTEFATTO DELL'ORDINE>>*.
### **Il rapporto e' `36.2`.**

### **E NON E' UNA SOMMA MANCATA: E' UNA SCELTA FATTA DALL'ORDINE DELL'ARRAY.** Se la
legge volesse **sommare**, servirebbe `np.add.at` — che il file ### **usa altrove**,
p.es. a `:9115`, nella stessa funzione.

### **IL TAGLIO `pi/4`, INVECE, QUASI NON MORDE** — e il confronto conta

| | `72` passi | `150` passi |
|---|--:|--:|
| saturati dal taglio `pi/4` | `44 884` | `79 581` |
| ### **frazione** | **`0.001322`** | ### **`0.001124`** |
| `abs(shift)`: mediana delle mediane | `4.782e-03` | `4.263e-03` |
| `abs(shift)`: max dei max | `7.853982e-01` | `7.853982e-01` |

> ### 📌 **IL CONFRONTO FRA I DUE SITI E' IL PEZZO PIU' UTILE DI QUESTA SEZIONE:**
> nel sito di `d0` il distorsore e' ### **il TAGLIO** *(`0.396`-`0.553`)*; nel sito della fase il taglio tocca il
> ### **`0.0011`** e il distorsore e'
> ### **<<l'ultimo vince>>** *(`0.9728`)*.
> ### **Due siti, due cause diverse, e nessuna delle due e' quella che il commento del
> ### codice racconta.**

*(Il `max dei max` di `abs(shift)` e' `7.853982e-01`, cioe' esattamente `pi/4 = 7.853982e-01`: il valore **dopo** il taglio, come atteso.)*

### **E L'ASSE `z`: `dir_laterale` STA SEMPRE NEL PIANO `xy`, MISURATO**

| | `150` passi |
|---|--:|
| terza componente di `dir_laterale`, **modulo massimo** su tutti gli archi-passo | ### **`0.000000e+00`** |

> ### **`0.0e+00` ESATTO, e non e' una sorpresa: e'
> ### `np.zeros_like` per costruzione** *(`:9506`)*. ### **Il numero non SCOPRE il
> difetto: lo CONFERMA su `70 773 112` archi-passo**, e
> chiude la domanda *<<succede davvero, o e' un ramo morto?>>*. ### **Succede sempre.**
> E' la voce ### **`FASE-TRASCINAMENTO-3D`**, e ### ⛔ **la cura e' LEGGE NUOVA:
> non si scrive adesso.**

## (c) IL CENSIMENTO DALL'AST: **il sito (2) gira DAVVERO**

| flag | valore nella configurazione del driver |
|---|---|
| `MEM_HEBB` | **`True`** |
| `MEM_MOTO` | **`True`** |
| `MEM_MOTO_TUTTO` | **`True`** |
| `SCALA_MIN_PASSO` | **`True`** |
| `SCALA_MIN` | **`False`** |
| `TRACCIA_D0` | **`False`** |
| `K_FRANGE` | **`0.0`** |

> ### ✅ **`MEM_HEBB` e `MEM_MOTO_TUTTO` sono entrambi `True`: IL SITO GIRA.**
> ### **Senza questa riga, tutti i numeri di sopra potrebbero essere quelli di un ramo
> ### morto.**

**I `3` siti il cui `if` nomina `MEM_MOTO` o `MEM_MOTO_TUTTO`,
dall'AST:**

| riga nella **COPIA PATCHATA** | riga su **`e2940b3c`** | il test |
|--:|--:|---|
| `9130` | **`9129`** | `MEM_MOTO_TUTTO` |
| `9160` | **`9154`** | `MEM_MOTO, MEM_MOTO_TUTTO` |
| `9524` | **`9518`** | `MEM_MOTO_TUTTO` |

### ⚠ **E LE RIGHE DELL'AST SONO QUELLE DELLA COPIA, NON DEL BLOB: lo dichiaro
### invece di riportarle come se fossero del simulatore.** La patch inserisce `1` riga
*(il gancio di modulo)* piu' `5` nel sito di `d0` *(una riga sostituita da sei)*, e lo
scostamento e' quindi `+1` prima del sito di `d0` e `+6` dopo. ### **Verificato riga per
riga sul blob:** `:9129 if MEM_MOTO_TUTTO:`, `:9154 if MEM_MOTO and MEM_MOTO_TUTTO:`,
`:9518 if MEM_MOTO_TUTTO:`. ### **E' lo stesso errore che il par.2 vieta — i numeri di
riga di un blob diverso — commesso dal mio strumento su se stesso.**

### **E `SCALA_MIN_PASSO = True`, che e' il motivo per cui `Delta d0` E' il `proj`**

Con `SCALA_MIN_PASSO` acceso, `_sd0` e' un ### **passante** *(`:6754-6756`: incrementa
un contatore e restituisce `dx`)*. ### **Quindi `Delta d0` coincide col `proj`
post-taglio**, e la somma con segno di sopra e' quella vera.
### ✅ **E NON HO CHIAMATO `_sd0` per verificarlo: lo avrei fatto incrementare.**
Ho letto il flag dal modulo e dichiarato la conseguenza: ### **una misura non muove cio'
che misura, nemmeno un contatore.**

## CHE COSA RESTA DAVANTI A LUCA — e non lo decido io

1. ### **LA CURA DELLA DECISIONE (1) ARRIVA IN UN REGIME DOVE IL TAGLIO MORDE SU META'
   ### DEGLI ARCHI**, e la forma decisa ### **satura piu' della vecchia** *(`0.553` contro `0.396`)*. ### **Non e' un'obiezione alla
   decisione**, che poggia sulle simmetrie e quelle sono **verificate**: e' un fatto che
   va saputo **prima**.
2. ### **IL `0.01` DEL TAGLIO E' UN NUMERO SCELTO**, e con una frazione di saturi del `0.40`-`0.55` ### **diventa un candidato per `A11` e `CLIP-INVENTARIO`.**
   ### ⛔ **Non lo tocco** *(non e' in questo mandato)*, ma il numero ora c'e'.
3. ### **IL BILANCIO DI `d0` CAMBIA SEGNO** *(`6.658e+03` -> `-9.222e+04`)*: la cura
   ### **non e' cosmetica**, e questa e' l'informazione che il passo (2) deve avere.
4. ### **IL SITO DELLA FASE SCARTA IL `97.3%` DI CIO' CHE CALCOLA.** La decisione e' gia' presa
   *(si **spegne**)*; il numero dice ### **quanto si spegne**, e che ### **cio' che si
   spegne non era la legge del commento.**

## CHE COSA QUESTA MISURA **NON** DICE

1. ### **non dice quale forma sia <<giusta>>:** misura **che cosa cambia**. La forma e'
   stata **decisa da Luca** sulle **simmetrie**, non sul bilancio;
2. ### **non dice che le due forme sono SCORRELATE** perche' il segno cambia nel `0.497`:
   una frazione vicina a `0.5` ### **e' compatibile anche con una correlazione che non
   ho misurato**;
3. ### **non misura l'effetto a valle** dei due siti su `rho`, `c_s` o sulla
   traiettoria: ### **misura i siti, non le loro conseguenze.**

## I DUE GIRI, e perche' sono DUE

Il mandato chiede **`72` e `150`** passi, e le uscite restano nel repo **col numero di
passi nel nome** *(`.passi-72` e `.passi-150`)*. ### **E servono a una cosa precisa: ogni
frazione di sopra e' STABILE fra i due giri**

| | `72` | `150` |
|---|--:|--:|
| frazione saturi, vecchia | `0.3874` | `0.3965` |
| frazione in cui il segno cambia | `0.4954` | `0.4968` |
| frazione scartati dalla fase | `0.9732` | `0.9728` |
| rapporto moduli scartati/applicati | `36.82` | `36.24` |

> ### **Nessuna si muove oltre la terza cifra: NON SONO TRANSITORI.**
> ### ⚠ **E due giri non sono uno scaling** *(`TAGLIA-FINITA`)*: dicono che i numeri
> non dipendono dalla durata provata, ### **non come si comportano al continuo.**

## LA SCENA, e un numero che ho controllato invece di lasciarlo

`--nmasse 3 --sep 6.1158`, seme `11`. A `150` passi: `n = 14 000`, archi `473 022`.

### ⚠ **`n` finisce ESATTAMENTE su `14 000`, che e' un numero troppo tondo per non
### guardarlo:** ho verificato che ### **non e' un tetto.** `MAX_NODI = 4 000 000`, ed
e' una ### **guardia di MEMORIA che FERMA il run** quando morde *(`MAX-NODI-FERMA`,
`A8`)* — ### **non tronca.** Il run ha fatto tutti i `150` passi, quindi
### **nessuna guardia e' scattata**: `14 000` e'
semplicemente dove la crescita e' arrivata. ### **Lo scrivo perche' un numero tondo non
spiegato e' un difetto che aspetta.**
