# `2026-09-29` — **IL CONTROLLO UNICO DELLO SCHEDULATORE** *(la cura di `RIPIEGHI-ZERO`)*

> ### 📌 **Questo file si committa e si pusha PRIMA del lavoro** (`par.8`), cosi' l'ordine e'
> **verificabile da git** invece che asserito da me: il commit di questo task history dev'essere
> **antenato** dei commit del piano e del codice.

**IL MANDATO DI LUCA, 2026-09-29, alla lettera:**

> *«La cura dei ripieghi e' il **CONTROLLO UNICO** dello schedulatore, non guardie sparse. Nella
> fase "apri" di ogni passo e subito dopo mitosi: ogni grandezza del **REGISTRO** delle grandezze
> per nodo ha lunghezza **ESATTAMENTE `n`** (ne' corta ne' lunga), altrimenti
> `CacheCorta`/`CacheLunga` **con il nome**. Il registro dichiara per ogni grandezza la **regola di
> nascita** (eredita / media / zero / estrazione nuova). Poi le guardie di **sostituzione** dentro
> le leggi si **TOLGONO**; restano solo le vere **inizializzazioni**, separate dagli `OR`.
> Prima del codice: il **PIANO** (elenco del registro dalle 31 grandezze trovate piu' quelle per
> arco, regola di nascita per ciascuna, punti dello schedulatore dove si controlla) e i **criteri
> del sigillo**: la prova a guasto rifatta deve dare **PROTETTO** su CORTA e LUNGA per tutte e 31;
> passi senza nascite **byte-identici** sulla scena grande fino al passo **72**. STOP dopo il
> piano.»*

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare*

### Le premesse su cui poggio, e da dove vengono

| premessa | da dove |
|---|---|
| **31** grandezze per nodo, trovate **in automatico** *(`len == n` allo stato BASE)* | **misurato**, `f173050` |
| **`0` su `31`** sono «a posto»; **10** ripiegano in silenzio su **tutta la rete** | **misurato**, `f173050` |
| una guardia **dentro** una legge arriva **a valle di una riscrittura** *(`:4462` esegue e non spara perche' `:4421` ha gia' riscritto `psi_spin`)* o viene **aggirata da un estensore a monte** *(`:2264`)* | **misurato**, `f173050` |
| `n` **E'** `len(phi)` *(property `:2063`)*, e **nessuna legge toglie nodi**: `phi` ha cinque scritture, tutte init/`concatenate`/modulo | **verificato sul codice**, `3b57e4d` |
| la classe **(b)** *«estensione dei soli nuovi»* **non e' sicura**: `mem_mot` estende **davvero** la coda e cambia **12611** nodi, perche' l'elemento inventato appartiene a un nodo **che esisteva gia'** | **misurato**, `f173050` |

### Cosa mi aspetto di trovare

1. ### **Il registro in gran parte NON si inventa: si REGISTRA.**
   Le regole di nascita **esistono gia'** nel codice, ai siti di `concatenate`/`vstack` di
   **mitosi** *(`:6641` e dintorni)*, **Schwinger** *(`:6803`)*, **semina** *(`:3139`)* e
   **`_allaccia`**. Mi aspetto che il registro sia in larga parte una **trascrizione** di cio' che
   il codice fa oggi. ### **Se dovessi SCEGLIERE una regola di nascita, e' un `A1`: mi fermo e
   chiedo.**
2. **Mi aspetto dei BUCHI**, e sono proprio la causa dei ripieghi: una grandezza che **non viene
   estesa** a uno dei quattro siti di nascita arriva **corta** al passo dopo. ### **Il buco e' il
   difetto; il ripiego e' solo cio' che lo nasconde.**
3. **Mi aspetto INCOERENZE fra i quattro siti** *(una grandezza estesa in mitosi e non in
   Schwinger, o estesa con regole diverse)*. Per `9-ter`, **la cura non aumenta il numero delle
   leggi**: se due siti fanno cose diverse per la stessa grandezza, ### **una delle due e' un
   difetto, non una seconda legge.**
4. **Mi aspetto che togliere le guardie di sostituzione sia byte-inerte** su un run sano —
   **MA NON PER TUTTE.** ### ⚠ **Un contro-esempio GIA' MISURATO:** `_xi_rumore` a `:3570` non e'
   un ripiego, e il codice lo dice: *«questo NON e' un fallback: e' il percorso normale della
   mitosi; `xi` e' l'AMBIENTE, non una proprieta' del nodo, quindi il figlio NON lo eredita»*.
   ### ➜ **Quella «guardia» E' una regola di nascita**, e nel registro diventa **estrazione
   nuova**. **Togliere quel ramo cambierebbe la fisica.**

### ⚠ Cosa NON so — e lo scrivo prima, non dopo

| # | il «non so» | perche' conta |
|---|---|---|
| **1** | ### **la fase «apri» esiste oggi nello schedulatore, o va creata?** So che c'e' `PASSO_COMPOSIZIONE`, `esegui_passo(net, composizione=None)`, `valida_composizione` e `_PASSO_TIPI`. **Non so** se fra i tipi ci sia gia' un posto «prima delle cinque leggi» | se va creata, e' **una fase nuova**: va contata come legge in piu' o no? *(`9-ter`)* |
| **2** | ### **due punti di controllo BASTANO?** ### ⚠ **Ho una ragione MISURATA per dubitarne:** `calcola_psi` riscrive `psi_spin` a `:4421` e `_estendi_psi_spinor` allunga a `:2264`, ### **entrambi A META' PASSO**. Se una cache va corta **fra** «apri» e «dopo mitosi», o **dopo** «dopo mitosi», ### **il controllo non la vede** | e' il **limite** della cura, e va detto **prima** di misurarla, non dopo |
| **3** | ### **«assente» e' diverso da «di lunghezza sbagliata»**, ed e' la distinzione che Luca mi ha imposto in `lambda_nodi`. Al primo passo alcune cache sono **legittimamente `None` o di lunghezza `0`** *(`Rete.__init__` fa `self.psi = np.zeros(0, complex)`)*. **Non so** quali | ### **se il controllo non distingue i due casi, si ferma alla COSTRUZIONE DELLA SCENA** — e' **esattamente** l'errore che ho fatto in `d14892a5` |
| **4** | **quante sono le grandezze PER ARCO**, e quale sia il loro riferimento. Presumo `m = len(i) == len(j)`, con `i`/`j` **riferimento** come `phi` lo e' per `n` — **ma non l'ho verificato** | il mandato le chiede nel registro |
| **5** | **le grandezze a 2 assi** *(`pos` `(n,3)`, `_nb` `(n,3)`, `_psi_spinor` `(n,2)`, `mem_mot` `(n,3)`)*: il controllo su `len` guarda **il primo asse**. **Non so** se esista una grandezza dove il **secondo** asse possa sbagliare | un controllo che guarda un asse e non l'altro e' un presidio **parziale**, e va dichiarato |
| **6** | ### **`eta` e' `inf` su tutti i nodi** *(legittimo, `nonneg_inf`)*: **non so** se ci siano altre grandezze il cui **valore** di nascita sia una **sentinella** e non un numero | una regola di nascita *«zero»* scritta dove il codice mette `nan` o `inf` **di proposito** sarebbe un cambio di fisica travestito da uniformita' |

### Cosa credo che il sigillo dira'

- ### **PROTETTO su CORTA e LUNGA per tutte e 31: ce la credo, ed e' il punto.** Un controllo che
  esige `len == n` **esattamente** copre entrambi i lati **per costruzione** — e chiude il buco che
  la prova a guasto ha trovato *(`if quanta >= n: return`, il lato LUNGA scoperto)*.
- ### ⚠ **Byte-identico fino al passo 72: qui NON sono tranquillo, e dico perche'.** Togliere le
  guardie di sostituzione e' byte-inerte **solo se nessuna di esse scatta in un run sano**. E
  ### **una MISURA dice che DUE scattano** al passo dopo una nascita *(`_rho_sorgente` e
  `_xi_rumore`, referto `de9c12ed`)*. Una delle due e' **dichiaratamente legittima**.
  ### ➜ **Quindi mi aspetto che «togliere le guardie» NON sia byte-inerte se lo faccio alla cieca**,
  e che la parte difficile del piano sia **distinguere la guardia dalla regola di nascita.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci*

**Le letture si fissano QUI, prima di vedere i numeri.**

| passo | che cosa decide | che cosa mi FERMA |
|---|---|---|
| **① l'elenco, MISURATO** | le grandezze **per nodo** *(`len == n`)* e **per arco** *(`len == m`)* allo stato BASE, **trovate in automatico** come nella prova a guasto | una grandezza con `len == n == m` *(ambigua)*: **mi fermo e la dichiaro**, non scelgo io |
| **② i siti di NASCITA, dall'AST** | per ogni grandezza, **tutte** le scritture `self.X = ...` con l'espressione, e **in quale funzione** stanno. I siti dentro `semina` / `mitosi` / `Schwinger` / `_allaccia` sono i **candidati a regola di nascita** | — |
| **③ la regola di nascita, PROPOSTA dal codice** | dall'espressione: indicizzazione dal genitore → **eredita** · `mean`/`+/2` → **media** · `zeros`/`full` → **zero** · `rng`/`normal` → **estrazione nuova** | ### **una grandezza che NON ha scrittura ad alcun sito di nascita**: e' un **BUCO**, e va nel piano come difetto, non come regola |
| **④ le INCOERENZE fra siti** | due siti che trattano la stessa grandezza in modo diverso | ### **se per decidere quale vince devo SCEGLIERE, mi fermo e chiedo a Luca** (`A1`, `9-ter`) |
| **⑤ i punti dello schedulatore** | dove sta «apri» *(o dove va messo)* e dove sta «subito dopo mitosi», **letti da `PASSO_COMPOSIZIONE` / `esegui_passo`**, mai da un commento | se «apri» **non esiste** e crearla e' una **legge in piu'**: lo dichiaro e **non decido** |
| **⑥ le guardie da TOGLIERE** | la lista dei siti di **sostituzione** *(dalla tabella `doc/RIPIEGHI_classi.md`)*, **separata** dalle **vere inizializzazioni** e dalle **regole di nascita travestite** | ### **`_xi_rumore` `:3570` NON si tocca** — e se ne trovo altre come quella, ognuna va **dichiarata**, non rimossa |
| **⑦ i criteri del sigillo** | si scrivono **ora**, prima del codice | — |

**LE LETTURE, FISSATE ORA:**

1. **la prova a guasto rifatta** *(`_guasto_ripieghi.py`, stesso comando, stessa scena, stesso
   passo 30)* deve dare ### **PROTETTO su CORTA E SU LUNGA per tutte e 31**. **Zero eccezioni**, e
   **«INERTE» non conta come PROTETTO**.
2. **byte-identico fino al passo 72** sulla scena grande, ### **nei passi SENZA nascite**, contro
   il blob di oggi `f7541d03`. *(Il confronto per passo va fatto **sul dominio comune**: e' il
   braccio `E` che ho gia' sbagliato una volta sommando su domini diversi.)*
3. ### **il caso che DEVE fallire** *(`P1-sexies`)*: con il controllo unico **disattivato**, la
   prova a guasto deve tornare a dare **ZERO su 31** — senno' il sigillo non sta misurando il
   controllo.
4. ### **il controllo positivo:** un guasto su una grandezza **PER ARCO** deve dare **PROTETTO**
   *(oggi la prova a guasto non le tocca affatto)*.

---

## 3. TODO DEL NEXT STEP — operativo

1. `csv/_test_fork/_registro_grandezze.py` **nuovo**: elenco per nodo e per arco **misurato**, e
   per ogni grandezza **tutte** le scritture dall'AST con la funzione che le contiene. Genera
   `doc/REGISTRO_grandezze.md`. **Committato prima di girare.**
2. **Il PIANO**, `doc/PIANO_controllo_unico.md`: il registro con la **regola di nascita** per
   ciascuna, i **punti dello schedulatore**, le **guardie da togliere** *(separate dalle
   inizializzazioni e dalle regole di nascita)*, i **criteri del sigillo**, e ### **l'elenco
   esplicito di cio' che NON decido io**.
3. **STOP.** *(Mandato: «STOP dopo il piano».)*

### In CODA, e non lo faccio adesso (`L-UN-PROMPT`)

| voce | che cosa e' |
|---|---|
| ### **`RELAZIONE_PER_CLAUDE.md` tiene TRE giorni** *(26, 27, 28)* invece del **solo giorno corrente**: l'ultimo chiuso in `doc/relazioni/` e' il **2026-09-25** | e' una **violazione in corso** della regola del par.4. **6764 righe** nel file vivo. Va chiuso il 26, il 27 e il 28 in `doc/relazioni/`, ed e' un commit **a se'** |
| `DT-CONVERGENZA` e *«stesso path, vince l'ultimo»* *(che copre `_flash_scomposizione.json` **e** `_hashseed_prova.json`)* | **solo registrazione**, nessun codice: erano gia' in coda |
| `massa_critica_adattiva` ricalcolata ~7 volte per passo; i numeri `C` con la ritaratura `389/484`, `DENS_CRIT_B`, `DENS_CRIT_THETA` nell'inventario dei numeri non derivati | voce nuova chiesta da Luca il 2026-09-28 |
| ### **`_guasto_ripieghi.py` non chiama `dichiara_configurazione`** *(`P5`)*, e la colonna «riga responsabile» ha i **tre difetti** dichiarati in `f173050` | va curata **quando** la prova a guasto si rifa' per il sigillo |
