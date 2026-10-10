# IL REFERTO DELL'INFRASTRUTTURA DELL'ERA `2`

> ### ⭐ **CHE COSA E' STATO COSTRUITO:** ### **la tabella delle leggi e' l'UNICA fonte**, il codice e la scheda ### **si GENERANO**, e ### **la macchina verifica** che *legge ↔ file ↔ riga di registro ↔ scheda* siano ### **in biiezione** — e che ### **niente cambi senza che cambi la tabella.**

### ⛔ **E NESSUNA DECISIONE DI FISICA E' STATA PRESA.** Le due leggi in tabella sono `prova: true` *(valori ### **da niente**, e la scheda lo dice)*, l'osservatore e' ### **uno strumento** *(`A17`)*, e ### **la scelta dell'integratore e' di Luca** — i due candidati stanno ### **nella stessa tavola, senza una raccomandazione travestita da misura.**

**Il simulatore dell'era `1`: `b8c21049`, NON toccato** *(verificato per `sha1` in ogni commit di questo mandato)*.

---

## `0.` IL CONTO DELLE LEGGI — ### **`3`** *(punto `10`)*

> ### ⛔ **OGNI REFERTO LO STAMPA, e un commit che lo AUMENTA deve DICHIARARLO** *(`STANDARD-10`, `AUDIT-CURE`)*: ### **una cura non aumenta il numero delle leggi**, e a parita- di effetto ### **si preferisce togliere un-eccezione.**

| | quante |
|---|--:|
| `osservatore` | `1` |
| `termine_arco` | `1` |
| `termine_nodo` | `1` |
| **in tutto** | ### **`3`** |
| di cui ### **`prova: true`** | ### **`3`** |
| le **variabili** | `1` |

### ⚠ **E `3` SU `3` SONO DI PROVA**, cioe- ### **non sono fisica decisa**: valori che vengono ### **da niente**, e la scheda di ognuna lo dice. ### **Il conto delle leggi VERE dell-era `2` e- `0`.**

---

## `1.` CHE COSA BLOCCA, E DOVE

> ### ⚠ **LA DISTINZIONE CHE CONTA, e che ho dovuto correggere in corsa:** ### **blocca** significa *«il commit NON si fa»*. ### **Segnala** significa *«qualcuno lo legge, se guarda»*. ### ⛔ **`A9`: un presidio che non impedisce NON E' UN PRESIDIO.**

| | che cosa impedisce | dove | via d'uscita |
|---|---|---|---|
| **`P-E1`** | la **BIIEZIONE** *(tabella ↔ file generato ↔ riga di registro ↔ scheda)*, e `LEGGE` si legge **via AST** | `pre-commit` | ### ⛔ **NESSUNA** |
| **`P-E2`** | **l'IMPRONTA**: un file generato ritoccato a mano, o una tabella cambiata senza rigenerare | `pre-commit` | ### ⛔ **NESSUNA** |
| **`P-E3`** | le **VARIABILI nei due versi** *(tabella ↔ `stato.py` ↔ registro)* | `pre-commit` | ### ⛔ **NESSUNA** |
| **`P-E4`** | le **IMPORTAZIONI**: la fisica non importa `osservatori/` ne' `driver` *(`A17`)* | `pre-commit` | ### ⛔ **NESSUNA** |
| **`P-E5`** | gli **OSSERVATORI in sola lettura**, ### **misurato AL BYTE** | `pre-commit` | ### ⛔ **NESSUNA** |
| **`P-E6`** | la tabella che cambia **senza** la riga di registro e **senza** l'ID nel messaggio | `commit-msg` | ### ⛔ **NESSUNA** |
| **`P-E7`** | i **RIFERIMENTI**: la scheda esiste, e ### **la `voce` di un osservatore risolve nell'indice** | `pre-commit` | ### ⛔ **NESSUNA** |
| **`H-FISICA-FUORI-LISTA`** | un `.py` sotto `primo_ordine/` che non e' ### **dichiarato** in `FILE_FISICA` | `pre-commit` | dichiarata |
| **`H-ID-OBBLIGATORIO`** | un commit che tocca un file di fisica **senza** nominare un ID | `commit-msg` | dichiarata |

### ⭐ **E L'ASSENZA DELLA VIA D'USCITA E' ESSA STESSA UN PRESIDIO, COLLAUDATO:** un braccio di `csv/_presidi_era2.py --collaudo` ### **ispeziona l'AST del proprio file** e verifica che ### **non esista nessun pattern di fuga che qualcuno legga.** *(La prima stesura ne definiva uno `_FUGA` ### **senza leggerlo mai** — codice morto che ### **INVITA** una scappatoia che il mandato vieta. Cancellato.)*

### ⛔ `2.` LA CI **NON E' UN PRESIDIO**, ed e' una correzione a me stesso

`.github/workflows/era2.yml` fa girare ### **tutti i collaudi a ogni push**. ### ⚠ **Ma Luca ha deciso: NESSUNA protezione del ramo su GitHub** *(2026-10-09)*. ### ⛔ **Quindi la CI gira DOPO il push e NON PUO' IMPEDIRE NIENTE: e' una RETE CHE SEGNALA.**

Io avevo scritto, nell'intestazione di quel file, *«LA CI NON SI PUO' DIMENTICARE … e NON HA VIA D'USCITA»*, e stavo per dichiararla ### **il gradino di robustezza di questo mandato.** ### ⛔ **ERA FALSO, E LO ERA SEMPRE STATO:** non mi serviva la decisione di Luca per vederlo — bastava chiedermi *«questa CI PUO' impedire un commit?»*. ### **Avevo trasferito alla CI una proprieta' vera dei presidi di `primo_ordine/`** *(che davvero non hanno fuga, perche' il loro codice non legge nessuna fuga)*, ### **dove non vale.** Il commento e' corretto nello stesso commit di questo referto.

### ⚠ **E UN `--no-verify` NON E' IMPEDIBILE IN LOCALE.** Lo scrivo perche' e' ### **il limite vero** dell'intera impalcatura: tutti i presidi di sopra vivono in `.githooks/`, e ### **valgono solo se qualcuno ha dato `git config core.hooksPath .githooks`.** ### ⛔ **Finche' quel comando non e' dato, questo repo NON HA PRESIDI** *(`A9`)*, e ### **chi clona non lo sa.** *(La cura — ogni strumento che verifica all'avvio che i hook siano attivi e ### **si rifiuta di partire** — e' in coda.)*

## `3.` CHE COSA RESTA **REGOLA SCRITTA**, e perche'

| | perche' non e' un presidio |
|---|---|
| **l'INVENTARIO** *(par.`6`①)* e il **README** *(par.`6`②)* | nessun hook li guarda: un file nuovo in `csv/` **senza** la sua voce passa. ### **Lo dico invece di contarli fra i presidi** |
| **`L-STELLA`** *(le cinque domande)* | e' scritta, e in questo mandato ### **ha funzionato comunque**: la domanda `3` mi ha fatto trovare un difetto *(vedi `6.`)*. ### ⚠ **Ma ha funzionato perche' l'ho applicata, non perche' qualcosa me l'ha imposta** |
| **il tipo `regola`** *(le leggi di crescita e di vuoto)* | lo **schema** lo valida, e il **generatore NON lo genera ancora**. ### ⛔ **Dichiarato, non risolto:** una `regola` in tabella oggi farebbe scattare `P-E1` *(manca il file)*, ### **che e' il comportamento giusto** ma non e' il pezzo finito |
| **la decisione `9`** *(la geometria)* e la **`13`** *(i coniugati delle memorie)* | ### **APERTE, e il formato le AMMETTE senza scegliere** — vedi `7.` |

## `4.` I NUMERI DEI COLLAUDI — ### **presi dall'uscita dei comandi**

| il collaudo | il comando, ### **verbatim** | esito |
|---|---|---|
| la catena | `python primo_ordine/_collauda_passo.py` | ### ✅ **`46`/`46`** |
| i presidi dell-era 2 | `python csv/_presidi_era2.py --collaudo` | ### ✅ **`22`/`22`** |
| lo schema della tabella | `python primo_ordine/leggi/schema.py` | ### ✅ **`34`/`34`** |
| il generatore | `python primo_ordine/_collauda_genera.py` | ### ✅ **`24`/`24`** |
| la lista dei file di fisica | `python csv/_collaudo_file_fisica.py` | ### ✅ **`17`/`17`** |
| i presidi dell-indice | `python csv/_collaudo_presidi_indice.py` | ### ✅ **`67`/`67`** |
| i controlli della migrazione | `python csv/_controlli_indice_v2.py` | ### ✅ **`6`/`6`** |

## `5.` QUALI PERMUTAZIONI SONO **BYTE-IDENTICHE**, E QUALI NO — ### **con il perche' FISICO**

| | che cosa si permuta | byte-identico? | il perche' |
|---|---|---|---|
| `1` | i **termini di `H`** | ### ✅ **SI**, `H` **e** il gradiente | `H` con `math.fsum`: la somma ### **ad arrotondamento esatto** non dipende dall'ordine. Il gradiente perche' `gradiente()` ### **impone l'ordine canonico per ID** — `fsum` non si puo' usare, gli addendi sono **array complessi** |
| `1-bis` | gli stessi, con la somma **GREZZA** | ### ⛔ **NO** | ### ⭐ **ed e' il controllo che rende il braccio sopra una MISURA e non un FALSO-UNO:** se anche la somma grezza fosse identica, l'ordine canonico sarebbe ### **un ornamento** |
| `2` | gli **archi dentro UNO strato** | ### ✅ **SI** | sono ### **DISGIUNTI**: ogni nodo riceve ### **UN SOLO** contributo d'arco, quindi ### **non c'e' nessuna somma da riordinare**. Con `8` archi in `2` strati |
| `3` | **gli STRATI, fra loro** | ### ⛔ **NO** | ### **NON COMMUTANO.** Due operatori che non commutano danno ### **un RISULTATO diverso, non un arrotondamento diverso** — e ### ⛔ **nessuna somma esatta puo' aggiustarlo.** ### ⭐ **L'unica cura e' la SIMMETRIA** *(alla Strang)*, che annulla l'errore di ordine pari |

### **E LA COMPOSIZIONE E' VALIDATA, con quattro controlli** *(e ognuno ha il suo caso che DEVE fallire)*: i **nomi** nel vocabolario · i nomi **e i pesi** un ### **PALINDROMO** · nessun ### **DOPPIONE consecutivo** · i pesi di ogni operazione che ### **sommano a `1`** *(altrimenti ### **si integrerebbe un tempo diverso da `dt`, e il codice non lo direbbe**)*.

## `6.` I DUE INTEGRATORI — ### ⛔ **LA TAVOLA, SENZA SCEGLIERE**

> ### **LA SCELTA E' DI LUCA** *(il nodo `INT` del piano)*. Qui ci sono ### **le misure**, e ### **una cosa che non sapevo prima di misurare.**

| | il cono | deriva **NORMA** | deriva **ENERGIA** | il costo |
|---|---|--:|--:|---|
| **GLOBALE** | `5` su `8` archi, ### ⚠ **NON dichiarato: ARTEFATTO della tolleranza** | `1.191e-15` | `3.939e-05` | `3`-`6`-`9` iterazioni di punto fisso |
| **LOCALE** | `3` su `8` archi, ### ✅ **ESATTO e DICHIARATO** | `1.986e-15` | `3.979e-05` | `5` sotto-passi × le sue iterazioni |

**Il cono, misurato** *(catena di `8` archi, `2` strati, perturbo UN nodo, `dt` dichiarato nel collaudo)*:

- **per STRATO:** ### **`1` arco**, e oltre ### ✅ **ESATTAMENTE ZERO** — e' cio' che uno strato **significa**.
- **per PASSO, LOCALE:** ### **`3` archi**, e oltre ### ✅ **ESATTAMENTE ZERO**. ### ⚠ **E NON L'AVEVO PREVISTO:** credevo `2`, il **numero di strati**. ### **La composizione simmetrica visita gli strati `2L-1` volte**, quindi il cono per passo e' ### **il numero di operazioni d'arco** *(`3`)*, non `L`.
  - `d=0:9.999e-04  d=1:1.005e-05  d=2:4.997e-08  d=3:2.514e-10  d=4:0.000e+00  d=5:0.000e+00  d=6:0.000e+00  d=7:0.000e+00  d=8:0.000e+00`
- **per PASSO, GLOBALE:** `5` archi su `8`.
  - `d=0:9.999e-04  d=1:1.005e-05  d=2:5.022e-08  d=3:2.526e-10  d=4:1.261e-12  d=5:6.233e-15  d=6:0.000e+00  d=7:0.000e+00  d=8:0.000e+00`

### ⛔ **E QUI LA MISURA HA CORRETTO UN BRACCIO CHE AVEVO SCRITTO IO.** Avevo asserito *«il GLOBALE a distanza massima NON e' zero»*: ### **falso** — oltre un certo raggio e' ### **esattamente zero**, per ### **underflow relativo allo stato.** ### ⭐ **E la ragione vera e' PEGGIORE di quella che credevo:**

| la tolleranza del punto fisso | il raggio del cono | le iterazioni |
|---|---|---|
| `1e-14` | ### **`5` archi** | `9` |
| `1e-08` | ### **`5` archi** | `6` |
| `0.0001` | ### **`3` archi** | `3` |

### ⛔ **IL CONO DELL'INTEGRATORE GLOBALE DIPENDE DA UNA MANOPOLA DEL RISOLUTORE.** Quindi ha un orizzonte che ### **ASSOMIGLIA a una causalita' e non lo e'.** ### ⭐ **Ed e' PEGGIO di un cono infinito, non meglio: un cono infinito si vedrebbe; questo si nasconde.** ### **E' la ragione piu' forte contro il globale**, e ### **non l'avrei trovata se non avessi misurato il cono A TRE TOLLERANZE** — cosa che ho fatto ### **perche' la domanda `3` della stella polare pretende di dire DI CHE TIPO e' un numero**, e non mi lasciava chiudere con *«parametro del risolutore, `A17`»*.

### ⚠ **E LA NORMA NON E' CONSERVATA AL BIT DA NESSUNO DEI DUE**, e lo dico invece di prometterlo: il punto medio implicito conserva gli invarianti ### **quadratici** ### **in aritmetica esatta**, non in virgola mobile. I numeri di sopra, su `200` passi, ### **sono MISURE, non garanzie.**

### `A8b` — **nessuna cache nascosta fra i passi**

`senza_cache()` confronta ### **tutte le costanti di modulo** dei moduli di fisica prima e dopo tre passi: ### **`5` moduli, nessuno si ricorda niente** — e ### **il presidio SCATTA** se gliene si fa ricordare uno. ### ⚠ **IL SUO LIMITE, dichiarato:** guarda le costanti di **MODULO**, e ### **non vedrebbe uno stato nascosto in un attributo di OGGETTO o in una chiusura.** Oggi i moduli di fisica non hanno ne' classi ne' chiusure; ### **se un giorno le avranno, il presidio VA ALLARGATO.**

## `7.` LE DOMANDE APERTE PER LUCA

| | la domanda | perche' e' TUA e non mia |
|---|---|---|
| **`1`** | ### **QUALE INTEGRATORE** *(nodo `INT`)*: il **GLOBALE** o il **LOCALE**? | i due non sono *«lo stesso metodo fatto meglio»*: ### **integrano cose diverse** *(il locale e' un prodotto di esponenziali di strato)*. ### **La norma e l'energia sono quasi identiche**; il cono ### **no** — e un cono esatto e' ### **un impegno di fisica**, non una proprieta' numerica |
| **`2`** | la **dipendenza del cono globale dalla tolleranza** e' un ### **DIFETTO da registrare nell'indice**? | io l'ho ### **misurata e dichiarata**, e ### **non le ho dato una voce**: dipende da se il globale resta un candidato. ### ⚠ **Se resta, la voce serve** |
| **`3`** | la **decisione `9`** *(la geometria)*: oggi `pos`, `x`, `y`, `z`, `coord` sono ### **SIMBOLI VIETATI**, e il generatore ### **rifiuta** un'espressione che li nomina | il formato ### **non anticipa la `9`**, e la direzione che hai dichiarato — *«lo spazio emerge grazie alla mitosi»*, la `9(b)` — ### **non e' ancora una decisione presa.** ### ⛔ **Se diventa la `9(a)`, il divieto va TOLTO dallo schema**, non aggirato |
| **`4`** | la **decisione `13`** *(i coniugati delle memorie)*: il tipo `coppia_coniugata` e' ### **AMMESSO dal vocabolario e NON USATO** | e' ### **la forma dell'ammissione senza la scelta**: `stato.py` solleva `NotImplementedError` se qualcuno lo usa, quindi ### **la tabella puo' dichiararlo e il codice dice che non sa ancora farlo** — invece di fingere |

### ⭐ **E CHE COSA LE DECISIONI `9` E `13` CAMBIERANNO NEL FORMATO** *(cosi' non si scopre dopo)*

- **la `9`** toccherebbe ### **`VIETATI` nello schema** e ### **`TIPI_VARIABILE`** *(servirebbe un tipo per una coordinata, che oggi **non esiste di proposito**)*. ### ✅ **Non toccherebbe il generatore**: i simboli vengono ### **dai tipi**, quindi un tipo nuovo ### **si propaga da solo** a `stato.py`, all'ambiente e alla derivata.
- **la `13`** toccherebbe ### **`DOVE`** *(nodo o arco)* e ### **`coppie_di()`** nel generatore, che e' ### **la mappa fra un simbolo e il suo coniugato**: una memoria con un coniugato ### **entrerebbe nella derivata di Wirtinger** come `psi`. ### ✅ **La forma c'e' gia'**, e il `NotImplementedError` e' ### **il segnaposto ONESTO.**

---

### ⚠ **E UNA COSA CHE QUESTO MANDATO NON HA FATTO, perche' non gliel'ho chiesto io:** la **CI non e' mai stata osservata girare**. E' scritta, i suoi passi sono gli stessi comandi della tavola `4.`, ### **ma non ho la prova che il server li abbia eseguiti** — e ### **per `A9` la differenza fra <<scritto>> e <<osservato>> e' la stessa che fra una tenda e un muro.**

*(Referto generato da `csv/_referto_infrastruttura_era2.py`: ### **ogni numero esce dall'uscita dei comandi della tavola `4.`** — `L-NUMERI`.)*
