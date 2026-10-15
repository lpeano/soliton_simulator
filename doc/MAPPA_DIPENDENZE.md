# LA MAPPA DELLE DIPENDENZE — **tutto si interseca, ma le intersezioni hanno un VERSO**

> **Regola di lavoro decisa da Luca, 2026-10-13 ore 19:17.**
>
> *«In due giorni energia, tempo proprio, `cs`, vuoto, materia/antimateria e crescita dello
> spazio si sono intrecciati, e il lavoro e' andato su tutti i fronti insieme. Il modello sta
> diventando UNA teoria sola, ed e' giusto che tutto si tocchi. **Ma «tutto si interseca» non
> vuol dire «tutto insieme»: le dipendenze hanno un VERSO.** Intanto il cuore del disegno
> dell'era `2` — «prima lo spazio, poi la materia» — e' rimasto fermo.»*

> ### ⛔ **QUESTO DOCUMENTO SI LEGGE PRIMA DI LAVORARE.** ### **E ogni task history, ogni
> relazione e ogni ripresa cominciano dicendo IL LIVELLO CORRENTE.**

---

## 1. ⭐ I CINQUE LIVELLI — *ognuno serve ai successivi, non viceversa*

### `L1` — **IL TEMPO PROPRIO IN OGNI LEGGE** *(la strada `(B)`)*

| | |
|---|---|
| **le voci** | `[[DECISIONE-STRADA-B-FLUSSI]]` · `[[TEMPO-PROPRIO-LOCALE]]` · `[[DECISIONE-TICK-OROLOGIO-MASSIMO]]` |
| **lo stato** | ### ⛔ **FERMO SU DUE DOMANDE DI LUCA.** La **derivazione e' FATTA** *(`697953a`, `c5deb5e`)*, le registrazioni fatte *(`a2fffbc`, `bbd7fee`)*; ### **manca il CODICE**, e la forma la decidono le due domande |
| **le domande che lo bloccano** | `[[DOMANDA-QUALE-TEMPO-PROPRIO-USA-L-ARCO]]` *(`B-3`)* · `[[DOMANDA-OMEGA-E-UNITA-O-COSTANTE]]` *(`B-4`)* |
| ### ⭐ **il criterio di uscita** | **tre numeri, tutti misurabili:** ① `python primo_ordine/_collauda_tempo_proprio.py` con ### **ZERO violatori** *(oggi **`4` su `7`**, e il collaudo c'e' gia')*; ② **`M-B1` AL BIT** *(ad angolo `pi` il motore nuovo riproduce quello attuale — e' **un'identita' algebrica**, non una tolleranza)*; ③ **`M-B2`**: l'errore su `H_tot` scala come `(omega dtau)^2`, **rapporto `4` a ogni dimezzamento** |
| ### ⚠ **l'ipotesi provvisoria che usa** | ### **`cs` UNIFORME**, cioe' il valore di oggi, **finche' `L2` non e' chiuso.** ### ⛔ **E non e' un dettaglio: `L1` MUOVE `cs` dentro tutte le leggi, ma la sua FORMA e' `L2`** — quindi `L1` si implementa **con `cs` costante**, e il codice **deve avere il posto dove `cs` varia** |

### `L2` — **LA MATERIA MODIFICA IL VUOTO, e quindi LA FORMA DI `cs`** — *la «gravita'» del modello*

| | |
|---|---|
| **le voci** | `[[CS-LOCALE-DAL-VUOTO]]` *(punto `3`)* · `[[DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA]]` · `[[DOMANDA-LA-FORMA-DI-CS-CHE-SATURA]]` |
| **lo stato** | ### ⛔ **FERMO SU UNA DOMANDA DI LUCA**, e adesso e' **UNA** *(il verso di `cs` e' stato accorpato)*. La derivazione di `1dcf315` e' fatta; ### **due candidate sono GIA' MISURATE nel `v4`** *(`SCATTER` e `TRASMISSIONE`)* |
| **la domanda che lo blocca** | `[[DOMANDA-COME-LA-MATERIA-CAMBIA-LAMBDA]]` *(`CRITICA`)*; `[[DOMANDA-LA-FORMA-DI-CS-CHE-SATURA]]` e' **sospesa** e `dipende_da` quella |
| ### ⭐ **il criterio di uscita** | ① `Lambda` **non e' piu' invariante** sotto il tick *(oggi: **`8.88e-16`**, cioe' **il vuoto e' PASSIVO**)*; ② l'effetto si vede **FUORI dal grumo** — ### **l'ALONE** *(oggi: **nessun anello oltre `3` sigma**, misurato nel `v4`)*; ③ gli orologi **rallentano INTORNO** al grumo, non solo dentro *(punto `1` dell'`11` ottobre)* |
| **l'ipotesi provvisoria che usa** | ### **nessuna verso l'alto:** `L2` chiede solo `L1`, che e' **sotto** |

### `L3` — **LA MITOSI E LO SPAZIO CHE NASCE** — *«prima lo spazio, poi la materia»*

| | |
|---|---|
| **le voci** | `[[SPAZIO-CHE-NASCE]]` · `[[D-BILANCIO-NASCITA]]` · `[[MITOSI-QUANTO-OLONOMIA]]` · `[[PRIMA-LO-SPAZIO-POI-LA-MATERIA]]` |
| **lo stato** | ### ⛔ **FERMO, ed e' IL CUORE DEL DISEGNO rimasto indietro.** Le derivazioni di `P5` *(la mitosi)* ci sono; ### **le quattro forme aspettano Luca** |
| ### ⭐ **il criterio di uscita** | ### **LA PRIMA CORSA CON LO SPAZIO CHE CRESCE DA UN SEME**, con ① le **norme conservate attraverso le nascite** *(`CARTA-FISICA-SIMULATORE/F10`)*, ② il **bilancio locale** che chiude attorno all'arco che si divide *(`D-BILANCIO-NASCITA`)*, ③ e **nessun parametro nuovo** |
| ### ⚠ **le ipotesi provvisorie che usa** | ### **`cs` UNIFORME finche' `L2` non e' chiuso** *(altrimenti un nodo nuovo non saprebbe che `cs` ha)*; e ### **`D-BILANCIO-NASCITA` si scrivera' su `H_tot` di `(B)`**, quindi **aspetta `L1`** |

### `L4` — **LA `U` DINAMICA** — *la via del campo per legare la materia*

| | |
|---|---|
| **le voci** | `[[U-ARCO-DINAMICA]]` · `[[DOMANDA-U-DINAMICA-LE-FORME]]` |
| **lo stato** | ### **derivazione FATTA** *(`60f869c`)*; **quattro forme a Luca** |
| ### ⭐ **il criterio di uscita** | la `U` **evolve** e la sua **olonomia su un ciclo** e' misurabile e **invariante di gauge** |
| ### ⚠ **l'ipotesi provvisoria che usa** | ### **la REGOLA DI CONNESSIONE di `L3`:** la nota del `2026-10-13` dice che **se il nato chiude triangoli coi vicini comuni dei genitori**, allora i cicli piu' corti sono **triangoli**, cioe' **plaquette locali** — e la **localita' del termine magnetico dipende da questo.** ### **Quindi `L4` aspetta `L3`** |

### `L5` — **I DOMINI DI MATERIA/ANTIMATERIA** — *la strada `(3)`*

| | |
|---|---|
| **le voci** | `[[IPOTESI-DOMINI-SEPARATI]]` · `[[DECISIONE-DIREZIONE-STRADA-3]]` · `[[DOMANDA-BANDE-O-SEGNO-LOCALE]]` *(chiusa)* e le **quattro forme** di `(P-b)` |
| **lo stato** | ### ⚠ **MOLTO LAVORO SU CARTA FATTO, E L'IMPLEMENTAZIONE SI FERMA.** `(P-a)`, `(P-b)`, `(R1)`, `(R2)`, il piano `(D1)`–`(D4)`, il parametro d'ordine **deciso**; e lo strumento `primo_ordine/segno.py` **esiste ed e' validato** |
| ### ⭐ **il criterio di uscita** | ### **`(D3)`/`(D4)` col termine ACCESO contro SPENTO**, e la **lunghezza di correlazione** dei domini che **cresce** *(coarsening)* con un esponente **`> 0`** dichiarato col suo errore |
| ### ⛔ **l'ipotesi provvisoria che usa** | ### **HA BISOGNO DELLA CRESCITA DI `L3`**: `(R2)` dice che un sistema chiuso **non si ordina** senza raffreddamento, e il raffreddamento **e' la crescita dello spazio.** ### **Quindi `L5` non si puo' MISURARE prima di `L3`** |

---

## 2. LE REGOLE OPERATIVE

| | la regola |
|---|---|
| **`(a)`** | ### **OGNI idea, mandato o domanda nuova SI COLLOCA nella mappa PRIMA di lavorarci:** a quale livello appartiene, da cosa dipende, cosa sblocca. ### ⚠ **Se non si colloca, si dice PERCHE' e si chiede a Luca** |
| **`(b)`** | ### ⛔ **IL CODICE E LE MISURE si fanno sul livello PIU' BASSO NON CHIUSO.** I livelli superiori si possono **derivare su carta**, ### **ma non si implementano e non si DECIDONO** finche' quelli sotto non hanno il loro criterio di uscita. ### **ECCEZIONE: solo se Luca lo dice esplicitamente, e la mappa lo registra** |
| **`(c)`** | ### **LE IPOTESI PROVVISORIE SONO DICHIARATE:** un livello che ha bisogno di qualcosa di un livello **superiore** usa un'ipotesi **scritta** *(per esempio «`L3` con `cs` uniforme finche' `L2` non e' chiuso»)*. ### **Ogni ipotesi ha una riga in questa mappa e un rimando nel task history che la usa, e quando il livello superiore si chiude SI RIVEDE** |
| **`(d)`** | ### **OGNI TASK HISTORY dichiara IN TESTA la sua CASELLA** *(livello)* **e le sue ipotesi provvisorie.** ### ⚠ **Un presidio lo verifica, col suo caso che DEVE fallire** *(un task history senza casella)* |
| **`(e)`** | ### **`doc/indice/DA_DECIDERE_LUCA.md` SI ORDINA PER LIVELLO:** prima le domande del **livello piu' basso aperto**. ### **E si portano a Luca in quell'ordine, UNA ALLA VOLTA** |
| **`(f)`** | ### **RIPRESA E VERIFICA PARTONO DA QUI:** `doc/RIPRESA_*.md` e ogni relazione cominciano con ### **«livello corrente: `Lx`, stato, prossimo passo»** |

---

## 3. ⭐ LA COLLOCAZIONE DI CIO' CHE E' IN CORSO — *primo uso della regola*

| il pezzo | il livello | lo stato |
|---|---|---|
| `B-3` **la media armonica sull'arco** | ### **`L1`** | ### ⛔ **domanda per Luca, E' LA PRIMA** |
| `B-4` **`omega` dal raccordo** | ### **`L1`** | ### ⛔ **domanda per Luca, la SECONDA** |
| la **regola materia → vuoto**, il **verso di `cs`**, `(C-A)`/`(C-B)` | ### **`L2`** | ⛔ **una domanda sola** *(accorpate)* |
| le **`4` forme della mitosi**, il **vuoto alla nascita**, il **seme minimo** | ### **`L3`** | ⛔ fermo |
| le **`4` forme della `U` dinamica**, il **segno della sorgente** | ### **`L4`** | ⛔ fermo |
| `(P-a)`, `(P-b)` e le loro **`4` forme**, `(D1)`–`(D4)`, l'**ipotesi dei domini** | ### **`L5`** | ### ⚠ **il lavoro su carta RESTA VALIDO: si ferma l'IMPLEMENTAZIONE** |

### `3.1` ⛔ UNA COSA DA DICHIARARE SU ME STESSO, e la regola e' nuova ma il fatto e' di ieri

### ⛔ **HO IMPLEMENTATO UNO STRUMENTO DI `L5` MENTRE `L1` E' APERTO:**
`primo_ordine/segno.py` *(il punto `(D1)`, commit `0ab42bb`)*, e anche `bande.py`,
`bande_floquet.py`, `deriva.py`. ### **Secondo la regola `(b)` non avrei dovuto**, e lo dico
invece di lasciarlo scoprire.

### ⚠ **CHE COSA NE FACCIO, e non lo decido da solo:** quegli strumenti sono **misure**, non
**fisica** — non toccano la tabella e non promuovono niente. ### ✅ **Li tengo**, perche'
hanno **validato `q_h`** che e' poi stato **deciso**; ### ⛔ **ma il loro USO su `L5` aspetta
`L3`**, e questa riga e' la loro **ipotesi provvisoria registrata**.

### `3.2` ⛔⛔ LE DUE TENSIONI COL DISEGNO — *punti aperti, da dire a Luca quando si arriva a `L5`*

| | la tensione | perche' e' una tensione |
|---|---|---|
| `(i)` | ### **il termine di ordinamento e' UNA LEGGE IN PIU'** | `CARTA-FISICA-SIMULATORE/F1` dice **UNA SOLA REGOLA**, e `9-ter` che una cura **non aumenta il numero delle leggi.** ### ⛔ **Se `(D3)`/`(D4)` NON mostrasse un effetto netto, VA TOLTO** — e questo e' **il suo criterio di abbandono, scritto prima** |
| `(ii)` | ### **LA CARICA** | la decisione del `2026-10-03` la voleva conservata **anche localmente**; ### ⛔ **oggi la saturazione la MESCOLA localmente** *(misurato: `corr(Delta N+, Delta N-) = -1.0000`, cioe' coppie esatte)*, e la strada `(3)` la salva ### **solo GLOBALMENTE.** ### ⚠ **Va detto a Luca in modo ESPLICITO quando si arriva a `L5`** |

---

## 4. ⭐ IL LIVELLO CORRENTE

> ### **`L1` — IL TEMPO PROPRIO IN OGNI LEGGE.**
> ### ⛔ **Stato: FERMO su due domande di Luca** — `[[DOMANDA-QUALE-TEMPO-PROPRIO-USA-L-ARCO]]`
> e `[[DOMANDA-OMEGA-E-UNITA-O-COSTANTE]]`.
> ### ⭐ **Prossimo passo:** quelle due risposte, poi **il codice di `(B)`** con `cs` uniforme
> *(ipotesi provvisoria dichiarata)*, poi **`M-B1` al bit** e **`M-B2`**.

### ⚠ **E IL CRITERIO DI USCITA DI `L1` E' GIA' MISURABILE OGGI:**
`python primo_ordine/_collauda_tempo_proprio.py` dice **`4` violatori su `7`**.
### ✅ **Quando saranno `0`, `L1` e' chiuso** — e quel collaudo **esiste e gira nel
`pre-commit`**, quindi ### **il criterio non e' una promessa: e' un comando.**

---

## 5. ⛔ GLI STRUMENTI DI `L5`, **CONGELATI** *(decisione di Luca, 2026-10-15)*

> *«Gli strumenti di `L5` che hai dichiarato in `784976d` restano **CONGELATI**: nessun
> codice e nessuna misura finche' `L1`–`L4` non sono chiusi.»*

| il file | che cosa fa | perche' e' `L5` |
|---|---|---|
| `primo_ordine/segno.py` | lo **squilibrio locale `q`**, e la sua validazione contro `Q` | e' **il parametro d'ordine** della strada `(3)` |
| `primo_ordine/bande.py` | le **due bande spettrali** di `W`, il controllo `C`, le grandezze per banda | e' **materia/antimateria** |
| `primo_ordine/bande_floquet.py` | il **riscaldamento di Floquet** sulla scena grande | misura la **termalizzazione delle bande** |
| `primo_ordine/deriva.py` *(+ `deriva_referto.py`)* | la **deriva di `E`**, la scansione in `x`, la **sorgente per nodo** | dichiarato con gli altri in `784976d` |

### ⛔ **NESSUNO DI QUESTI SI TOCCA E NESSUNO GIRA** per produrre misure nuove, finche'
`L1`–`L4` non sono chiusi. ### ⚠ **I loro COLLAUDI restano nel `pre-commit`**
*(`_collauda_corrente.py`, `_collauda_deriva.py`)*: ### **girano per NON LASCIARLI
IMPUTRIDIRE, non per misurare** — e se un collaudo cominciasse a fallire, ### **quello e'
un fatto da riportare, non un lavoro da riprendere.**

### ⚠ **E UNA DOMANDA DI PERIMETRO CHE NON DECIDO IO, e la segnalo invece di risolverla a
mio favore:** `deriva.py` contiene la macchina che serve a **`M-B2`**, che e' **un criterio
di uscita di `L1`** — la scansione in `x`, le escursioni relative, il rapporto fra
dimezzamenti. ### ⛔ **Il congelamento di `L5` BLOCCA anche il riuso di quella macchina per
una misura di `L1`?** ### ✅ **Finche' non c'e' una risposta la tratto come BLOCCATA**, e
quando `M-B2` servira' lo chiedo: ### **riscrivere la stessa macchina altrove per aggirare
il congelamento sarebbe aggirarlo, non rispettarlo.**

### 📌 **E DUE FILE CHE NON SONO NELL'ELENCO, e dico perche':** `corrente.py` e il suo
collaudo costruiscono **la corrente locale dell'energia**, che serve a `H_tot` di `(B)` —
### **cioe' sono `L1`/`L2`, non `L5`.** ### ⚠ **Non li aggiungo ai congelati e non li uso:
li classifico, e la classificazione e' una mia lettura.**

---

## 6. ⭐ IDEE COLLOCATE, **NON OPERATIVE**

> ### ⛔ **Qui stanno le idee che hanno gia' una CASELLA e NON si lavorano:** la regola
> `(a)` dice che ogni idea si colloca **prima** di lavorarci, e ### **collocare non e'
> cominciare.**

### `6.1` **`MISURA-DOPPIONI`** — *dopo `L1`*

| | |
|---|---|
| **la casella** | ### **dopo `L1`** — si apre **solo quando `L1` e' chiuso** |
| **che cosa e'** | calcolare la **relazione di dispersione** del passo della camminata **sul toro** *(senza bordi)* e **contare i minimi** della curva: ### **uno o due coni?** |
| **la domanda** | ### **la camminata ha <<DOPPIONI>>?** *(Nielsen–Ninomiya)* |
| **perche' non e' un effetto dei bordi** | si misura **sul toro**, che **non ha bordi**: ### **sono una proprieta' del RETICOLO ALL'INTERNO** |
| **perche' dopo `L1`** | la dispersione e' quella di `W`, e ### **in `(B)` `W` CAMBIA** *(`hop(theta)` e `Grover(theta)` invece delle involuzioni)*: ### ⛔ **misurarla adesso darebbe la dispersione di un passo che sta per essere sostituito** |
| ### ⚠ **che cosa NON faccio** | nessun codice, nessuna misura. ### **E non la registro nemmeno come voce dell'indice**, perche' il mandato dice *«solo collocazione»* — ### **quando si apre, la voce e' il primo passo** |

### `6.2` **`L6` — IL TEMA QUANTISTICO** — *dopo `L1`–`L5`, decisione di Luca del 14 ottobre*

| | |
|---|---|
| **la casella** | ### **`L6`, dopo `L1`–`L5`** |
| **che cosa e'** | la **seconda quantizzazione di `psi`** — un **automa cellulare quantistico** — ### **con la STESSA tabella delle leggi** |
| ### ⭐ **il legame col simulatore di oggi** | il simulatore attuale ne sarebbe ### **IL CAMPO MEDIO** |
| **i quanti** | **spinoriali FERMIONICI** |
| ### ⭐ **i bosoni** | **figure d'interferenza** *(la materia)*, ### **NON coppie** |
| **il primo passo** | a **grafo FISSO** |
| ### ⭐ **il controllo di raccordo** | con **`1` quanto** deve dare ### **AL BIT** lo stesso risultato di `primo_ordine/motore.py` |
| **lo stato** | ### ⛔ **SOLO TEORIA fino all'apertura di `L6`** |

### ⚠ **E NOTO UNA COSA SUL CONTROLLO DI RACCORDO, perche' e' la sua forza:** *«con `1`
quanto, AL BIT come `motore.py`»* e' ### **un criterio che non si puo' addolcire** — come
`M-B1` per `(B)`. ### **E ha una conseguenza sull'ordine:** il raccordo e' con `motore.py`,
che in `(B)` **cambia** ⟹ ### **`L6` aspetta `L1` non per comodita', ma perche' il suo
criterio di raccordo PUNTA a un oggetto che sta per cambiare.**

### ⛔ **E CHE COSA NON FACCIO:** nessuna derivazione, nessun task history, nessuna voce.
### **La collocazione e' questa riga, e basta.**

---

## 7. ✅ `L1` — **LE DUE DECISIONI DI LUCA DEL `2026-10-15`**

### `B-3` — **IL TEMPO PROPRIO DELL'ARCO E' LA MEDIA ARMONICA**

> ### ⭐ **`dtau_arco = 2 · dtau_i · dtau_j / (dtau_i + dtau_j)`**

**Il motivo:** e' **la somma dei tempi di attraversamento delle due meta' dell'arco**,
ciascuna alla velocita' del proprio nodo.
### ⚠ **E L'IPOTESI RESTA DICHIARATA, registrata CON la decisione: <<DUE META' UGUALI>>.**
### **E' un MODELLO della geometria dell'arco, non un fatto** — se il tempo proprio
cambiasse lungo l'arco in un altro modo, **il conto cambierebbe.**

### `B-4` — **`omega` DAL RACCORDO, E UN SOLO `omega`**

> ### ⭐ **`omega · dtau_rif = pi`**, con **`dtau_rif` = il tempo proprio dell'orologio
> PIU' VELOCE** *(`cs` al massimo)*. ### **UN SOLO `omega`** per lo spostamento **e** per
> il Grover.

### ✅ **Quindi `omega` NON e' una costante tarata: e' una CONDIZIONE DI RACCORDO** — al
passo di riferimento il motore nuovo **riproduce quello di oggi**. E siccome compaiono
**solo i prodotti `omega · dtau`**, un fattore comune **si assorbe**: ### **e' una SCELTA
DI UNITA'**, e `CARTA-FISICA-SIMULATORE/F10` e' rispettato.

### ⚠ **E IL PUNTO DEBOLE RESTA DICHIARATO, registrato CON la decisione:** l'uguaglianza
dei due `omega` e' ### **UN FATTO STORICO DEL MOTORE, NON UN PRINCIPIO.** Oggi sono
entrambi involuzioni *(entrambi all'angolo `pi`)*, e tenerli uguali **non aggiunge niente**;
### **ma nessun argomento dice che debbano esserlo**, e separarli aggiungerebbe **un numero
puro** da derivare.

### ⭐⭐ **E UNA CONSEGUENZA OPERATIVA, che e' cio' che rende `theta <= pi` vero PER
COSTRUZIONE:** posto **`s = dtau / dtau_rif`** con `dtau_rif` ### **IL MASSIMO** dei
`dtau`, si ha **`s <= 1` SEMPRE**, quindi `theta = pi·s <= pi`.
### ✅ **NESSUN TETTO E NESSUN CLIP** *(`A11`)*: ### **il limite viene dalla DEFINIZIONE di
`dtau_rif`.**

### ⭐ **E UNA PRECISAZIONE SU `B-3`:** siccome `dtau_k = cs_k · dt`, la media armonica dei
`dtau` **equivale** a quella dei `cs` — ### **`cs_arco` = media armonica di `cs_i` e
`cs_j`** — perche' ### **il `dt` globale si cancella nel rapporto.** ### ✅ **Quindi la
decisione si legge sui tempi propri o sulle velocita', e sono LA STESSA COSA:** e' ### **indipendente
da come si misura il tick.**

---

## 8. ✅ IL **PERIMETRO DEL CONGELAMENTO** — *scelta di Luca, `2026-10-15`*

> ### ⭐ **E' LA RISPOSTA ALLA DOMANDA CHE AVEVO FATTO IN `717bb60`**, e la riporto perche'
> era mia: *«il congelamento di `L5` blocca anche il riuso di `deriva.py` per una misura di
> `L1`?»*

| | la regola | |
|---|---|---|
| ✅ **ammesso** | `primo_ordine/deriva.py` **IN SOLA LETTURA** per i criteri di uscita di `L1` — **`M-B2`** e **`_collauda_tempo_proprio.py`**, che ### **lo importa gia'** |
| ⛔ **vietato** | ### **nessuna misura NUOVA di `L5`**, e ### **nessuna modifica alle sue parti di `L5`** *(la **sorgente per nodo**)* |
| ⚠ **e se una parte che serve a `L1` va toccata** | ### **si dichiara UNA PER UNA nel commit** |

### ⚠ **E NOTO CHE LA DOMANDA ERA GIUSTA A MONTE, non solo utile:** `_collauda_tempo_proprio.py`
### **importa gia' `deriva.py`** *(per `DV.scena` e `DV.OPERATORE`)*, quindi
### **il congelamento preso alla lettera avrebbe bloccato il criterio di uscita di `L1`**
— cioe' ### **si sarebbe bloccato da solo.**

---

## 9. ⚠ `L1` — **IL CODICE E' FATTO, E IL LIVELLO NON E' CHIUSO** *(`2026-10-15`)*

> ### ⛔ **`L1` RESTA IL LIVELLO CORRENTE**, e non per lavoro mancante: ### **per due
> criteri di uscita che non passano, e che chiedono una decisione di fisica.**

| | il criterio di uscita | esito |
|---|---|---|
| `1` | `_collauda_tempo_proprio.py`: `0` violatori su `7` | ### ✅ **PASSA**, e il presidio **impedisce** *(dimostrato)* |
| `2` | `M-B1`: identita' AL BIT con `717bb60` | ### ✅ **PASSA** *(`eff92bbd8622`, `250` tick, `psi` e `phi`)* |
| `3` | `M-B2`: fattore `4` a ogni dimezzamento | ### ⛔ **NO: `2.540`, `2.204`, `2.111`** — e la causa e' misurata: **la composizione non e' simmetrica** |
| `4` | la `C`-simmetria resta verde | ### ⛔ **NO: da `0.000e+00` a `5.343`** — e la causa e' derivata: **`G^* = G(-theta)`** |

### ⛔ **LE DUE DECISIONI CHE SERVONO A LUCA, e non le prendo io:**
### ① **`[[DECISIONE-COMPOSIZIONE-SIMMETRICA]]`** — l'`ordine` palindromo darebbe
`O(dtau^2)` *(misurato: `5.342`, `3.691`, `4.291`)*, ma ### **cambia IL PASSO**, e
### ⚠ **`M-B1` e `M-B2` cosi' come sono scritti non possono valere insieme.**
### ② **`[[DECISIONE-LA-C-VUOLE-IL-TEMPO-ROVESCIATO]]`** — la simmetria che sopravvive e'
una **`CT`**, non una `C`.

### 📌 **E DUE COSTI REGISTRATI:** `[[COSTO-MEMORIA-DEI-FLUSSI-PARZIALI]]`
*(`4.39x` -> `5.56x`, soglia `5x`)* e
`[[DIFETTO-LAMBDA-NON-PIU-INVARIANTE-SOTTO-IL-VUOTO]]`.

### ⭐ **E CIO' CHE `L1` HA GIA' CONSEGNATO A `L2`, qualunque sia la decisione:**
### **il PUNTO UNICO di lettura del tempo proprio** *(`flussi_parziali.dtau_nodo`)* —
### **nessuna legge calcola il suo `dtau` da se'**, e quello e' il posto da cui `L2` fara'
variare `cs`.

---

## 10. ✅ `L1` — **IL PALINDROMO E' IN TABELLA** *(`2026-10-15`, sera)*

### ✅ **`[[DECISIONE-COMPOSIZIONE-SIMMETRICA]]` E' CHIUSA**: l'ordine e' palindromo,
`12` pezzi, impronta `871a7b37dab75b06` → **`f1fca71b952bb8c8`**, e l'errore di `H_tot`
passa da **primo** a **secondo** ordine *(pendenza `1.183` → `2.006`)*.

### ⚠ **E RESTA APERTA UNA SOLA DECISIONE, piu' precisa di prima:**
`[[DECISIONE-LA-C-VUOLE-IL-TEMPO-ROVESCIATO]]` — ### **non <<la `C` o la `CT`?>> ma
<<la MONETA DI SPIN deve rovesciarsi sotto la `C`?>>**, perche' ### **senza la moneta
l'inversione del tempo del passo e' ESATTA** *(`3.9e-16`)* e **Kramers c'e'**.

### 📌 **E cio' che `L1` ha consegnato a `L2` resta quello:** ### **il punto UNICO di
lettura del tempo proprio.** Adesso con, in piu', ### **un passo reversibile per
costruzione** — che e' cio' che rende sensato chiedersi, a `L2`, **da dove venga
l'irreversibilita'** *(`A15.3`)*.
