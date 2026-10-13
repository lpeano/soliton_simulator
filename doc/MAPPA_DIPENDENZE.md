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
