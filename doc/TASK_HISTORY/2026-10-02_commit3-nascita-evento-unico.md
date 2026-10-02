# `COMMIT 3` DEL RIORDINO — **LA NASCITA COME EVENTO UNICO**

> **Task history, scritto e committato PRIMA del lavoro** *(par.8)*. **Nessuna riga del
> simulatore in questo commit:** blob **`3ddc56d9`** *(sha1 dei byte grezzi)*.
> **Il piano è `doc/PIANO_riordino_mitosi.md`, parte (c); la storia è `doc/MITOSI_storia.md`.**

---

# 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare*

## 1.1 Le premesse, e da dove vengono

| | |
|---|---|
| **il bersaglio** | `30` grandezze del registro scritte in **UN SOLO punto**, con **una regola dichiarata per ciascuna**, al posto dei **tre** posti di oggi |
| i tre posti di oggi | `mitosi` *(16 grandezze)* · i due `_eredita_*` *(13)* · `conc_nodi` **per mutazione in posto** *(`.append`)* |
| **la tabella di partenza** | `doc/REGOLE_nascita.tsv`, **32 regole**, già verificate **per ancora cercata nel testo** |
| i **quattro eventi** | `semina` · `divisione` · `Schwinger` · `allaccio` — ### **APPROVATI da Luca**, e la registrazione è nel piano e nel registro fisica |
| **il criterio** | ### **byte-identico fino al passo 72 sulla scena grande CON nascite, grandezze E CONTATORI**, contro il blob del commit 2 |

## 1.2 ⚠ **COSA CREDO E NON HO ANCORA VERIFICATO** — e lo scrivo perché può smentirmi

| # | cosa credo | perché potrebbe essere falso |
|--:|---|---|
| **1** | **le estrazioni casuali nella nascita, nella configurazione di riferimento, sono DUE**: `rng.random(len(sel))` sotto `ANTIFASE_ADD` e `rng.random(len(sel))` sotto `COPPIA_MIT > 0` | ### **non ho verificato il DEFAULT di `ANTIFASE_ADD`.** Se è spento, l'estrazione è **una**; se è acceso, sono due **e l'ordine conta.** E `_nasce`, `_grado`, `_smp_chirurgia` potrebbero pescare: **non l'ho guardato** |
| **2** | il ramo stocastico *(`rng.normal`)* **non gira**, quindi la sua estrazione non entra nel contratto | verificato il 2026-10-01 *(`REGIME` deterministico dal modulo)*, ### **ma solo per la configurazione del driver** |
| **3** | **assorbire i due `_eredita_*` è la parte DIFFICILE, non la tabella** | i due portano **sei contatori** *(`_g_eredpsi_tot`, `_g_eredpsi_salti`, `_g_eredpsi_shape`, `_g_eredpsis_salti`, `_g_eredrho_salti`, e i salti di `_cs_nodo_prev`)* e **rami condizionali sulla LUNGHEZZA delle cache**. ### **Byte-identico sui CONTATORI vuol dire riprodurre anche i rami che NON scattano** |
| **4** | **`conc_nodi` è il punto cieco** | cresce con `.append`, ### **invisibile all'AST e alla sorveglianza** — e l'ha persa, nello stesso modo, in **due strumenti diversi** |
| **5** | **l'ordine delle SOMME conta quanto l'estrazione** | `psi` del nato è `0.5*(cur[a] + cur[b])`: una somma in virgola mobile. ### **Se la tabella la calcolasse in un ordine diverso, l'ultimo bit cambierebbe** |

## 1.3 ⛔ **IL RISCHIO CHE IL PIANO DICHIARA, e che credo sia il più probabile**

> ### **Spostare le scritture in un punto solo può cambiare l'ORDINE DELLE ESTRAZIONI e delle
> ### SOMME. E il generatore è UNO (`net.rng`): chi pesca prima cambia ciò che pescano tutti.**

### ➜ **La mia attesa, scritta prima:** ### **il byte-identico PASSA se e solo se il punto unico
mantiene l'ordine esatto delle estrazioni e delle somme.** Non è un «dovrebbe andare»: è una
condizione che ### **si può misurare prima di scrivere il codice**, ed è il passo 1.

### 🛑 **E SE CADE SOLO PER QUESTO: MI FERMO E LO DICO.** Il mandato lo dice, il piano lo dice, e
lo scrivo qui perché ### **è la tentazione più forte di questo lavoro** — allentare il criterio a
*«identico tranne l'ultimo bit»* farebbe passare il commit e ### **butterebbe via la sola prova
che la riorganizzazione non è una cura mascherata.**

## 1.4 ⚠ **E DUE COSE CHE NON SO SE SONO FATTIBILI, e le dico ora**

| | |
|---|---|
| ### **la SEMINA e l'ALLACCIO nello stesso punto della DIVISIONE** | `semina` è **151 righe** e `_allaccia` **43**, e nascono in un momento del tutto diverso *(la costruzione della scena, non il passo)*. ### **Metterli nella stessa funzione potrebbe essere la cosa giusta o un'astrazione forzata**, e non lo so prima di provarci |
| ### **se le 30 grandezze si scrivano DAVVERO tutte in quel punto** | la tabella ne dichiara **32 regole** su `grandezza x evento`, ### **ma non tutte le 30 grandezze hanno una regola per OGNI evento** *(`tw` non ha una regola alla `semina` nella tabella di oggi)*. ### **Un presidio che pretenda 30 regole per 4 eventi chiederebbe 120 righe, e la tabella ne ha 32** |

## 1.5 📌 **COSA I FATTI GIÀ SCRITTI MI DICONO** *(`doc/FATTI_dal_codice.md`, letto prima di toccare)*

| funzione | il fatto che conta per questo lavoro |
|---|---|
| `_eredita_spinore_figli` | ### **l'eredità alla mitosi è una COPIA ESATTA, senza perturbazione**, e il figlio nasce con `chi = 0` *(misurato `0.0000` esatto)*. ### **La parentela NON è registrata ma è RICOSTRUIBILE in volo** |
| `mitosi` | `PLAST_MIT = 0` in **tutti** i test committati ⇒ il ramo `d0new = [dh, dh]` è ### **quello che gira** |
| ### ⚠ **`_eredita_psi_figli`** | ### **NON HA NESSUN FATTO in `doc/FATTI_dal_codice.md`** — zero occorrenze. E nemmeno `semina`, `_allaccia`, `_nasce`, `decidi_divisione`. ### **È la stessa lacuna di `pozzo_grafo`** *(2026-09-27, `FATTI-AVVIO` allargata)*: ### **sto per toccare quattro funzioni su cui il repo non ha un solo fatto verificato** |

---

# 2. PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci*

## 2.1 I passi, in ordine, e **che cosa decide ciascuno**

| # | il passo | **che cosa DECIDE** | **che cosa mi FERMA** |
|--:|---|---|---|
| ### **1** | ### **MISURARE l'ordine delle estrazioni e delle somme** *(prima di una riga di codice)* | ### **quali estrazioni avvengono nella nascita, in che ORDINE e QUANTE volte**, e quali somme in virgola mobile dipendono dall'ordine degli addendi. ### **Diventa il CONTRATTO**, scritto nella tabella | se la sorveglianza su `net.rng` ### **PERTURBA** il passo *(cioè se lo stesso passo con e senza spia non è byte-identico)*, la misura **non vale** e mi fermo: è lo stesso controllo che il 2026-09-29 ha dato **byte-identico su 1 887 282 eventi** |
| **2** | la **tabella** estesa col contratto dell'ordine | — *(è una dichiarazione, non codice)* | — |
| ### **3** | ### **il punto unico di nascita** + il presidio *«regola di nascita non dichiarata»* | — | ### **se il byte-identico cade SOLO per l'ordine delle estrazioni o delle somme** ⇒ **STOP e lo dico.** ### **NON allento il criterio** |
| **4** | il **sigillo**, coi **tre** casi che devono fallire | se il sigillo **vede** un difetto della nascita | se un caso che deve fallire **passa** ⇒ il sigillo non sta guardando la nascita, e il verdetto non si consegna |

## 2.2 ✅ **COME MISURO L'ORDINE DELLE ESTRAZIONI — e NON leggendo il codice**

> ### **La regola di questa sessione, sei volte: non leggere il codice — GUARDARE IL RUNTIME.**

| | |
|---|---|
| **come** | si **avvolge `net.rng`** con un oggetto che **inoltra** ogni chiamata e **registra** nome del metodo, `size`, e **l'ordine di arrivo**; l'attribuzione alla VOCE viene dalla **spia sui confini di voce** del commit 1 |
| ### **perché non l'AST** | l'AST vede `self.rng.random(...)` **in cinque posti** e ### **non sa quali rami girano.** `ANTIFASE_ADD` e `COPPIA_DENSITA` sono flag: ### **un conteggio statico direbbe 5 dove il runtime dice 1 o 2** |
| ### **il controllo che rende la misura valida** | ### **lo stesso passo CON e SENZA la spia deve essere byte-identico.** Se non lo è, la spia **consuma** il generatore o ne cambia lo stato, e la misura ### **misura la spia** |
| **l'ordine delle SOMME** | si elencano le scritture della nascita **la cui espressione è una somma di due o più addendi** *(`0.5*(x[a] + x[b])`, `np.concatenate` di più pezzi)*: ### **l'ordine degli addendi E dei pezzi è parte del risultato**, e va nella tabella |

### 📌 **E una lettura fissata ORA, prima dei numeri**
### **Se le estrazioni nella nascita risultassero ZERO** nella configurazione di riferimento, allora
### **il rischio del piano NON si applica a questo commit** — e lo dirò così, invece di dichiarare
un pericolo che i numeri hanno escluso. ### **Ma le SOMME restano**, e quelle non dipendono da un
flag.

## 2.3 ✅ **I TRE CASI CHE DEVONO FALLIRE** *(dal piano, e sono il cuore del sigillo)*

| # | il caso | che cosa **deve** succedere | **se non succede** |
|--:|---|---|---|
| **①** | si **TOGLIE** una grandezza dalla tabella dell'evento | il run si **ferma**: *«regola di nascita non dichiarata per `<nome>` all'evento `<evento>`»* | il presidio **non guarda la tabella** |
| **②** | si cambia la **regola di UNA** grandezza: `psi` da **`media`** a **`eredita`** | il sigillo **vede la differenza** | il sigillo **non guarda le grandezze della nascita** |
| **③** | si lascia una **scrittura SPARSA** a valle | deve essere **impossibile**, cioè il presidio **la nomina** | il punto unico **non è unico**: è un punto in più |

### ⚠ **E il caso ② è quello che collaudo con più attenzione, per una ragione misurata**
`psi` del nato è la **media** dei genitori e `psi_spin` è **l'eredità da `a`**: ### **sono due
regole DIVERSE di proposito** *(ciascuna prende quella del proprio compagno — `phi` è la media,
`phi_s` eredita)*. ### ➜ **Scambiarle è esattamente il difetto che la tabella esiste per
impedire**, e se il sigillo non lo vedesse la tabella sarebbe **decorativa.**

## 2.4 🛑 **CHE COSA MI FA FERMARE, in un elenco secco**

1. la **spia su `net.rng` perturba** il passo ⇒ la misura dell'ordine non vale;
2. il **byte-identico cade SOLO** per l'ordine delle estrazioni o delle somme ⇒ **STOP**, e non
   allento il criterio;
3. un **caso che deve fallire PASSA** ⇒ il verdetto non si consegna;
4. ### **il punto unico richiede di RIORDINARE le scritture** *(non solo di spostarle)* ⇒ **STOP**:
   riordinare **cambia la fisica**, ed è ciò che `doc/MITOSI_non_si_spezza_per_tipo.md` ha già
   misurato una volta;
5. ### **assorbire i due `_eredita_*` richiede di cambiare un contatore** ⇒ **STOP e lo dico**: un
   contatore che cambia di uno è un difetto che le grandezze non vedrebbero.

## 2.5 ⚠ **IL LIMITE CHE QUESTO COMMIT NON TOGLIE, dichiarato prima**

Il controllo unico guarda **i confini delle voci**. ### **Dentro `mitosi` la finestra RESTA**, e
questo commit la **riduce** *(un posto solo invece di tre)* ### **senza chiuderla.** Il piano lo
dice già nel par. *«che cosa questo piano NON promette»*, e lo ripeto qui perché ### **è la cosa
che un lettore potrebbe credere risolta.**

---

# 3. TODO DEL NEXT STEP — *la lista operativa*

| # | voce | stato |
|--:|---|---|
| **0** | questo task history, **committato e pushato prima del lavoro** | ### **IN CORSO** |
| ### **1** | lo **strumento** che misura l'ordine delle estrazioni e delle somme nella nascita, ### **committato PRIMA di girarlo** *(par.5)* | **DA FARE** |
| **2** | il **run** dello strumento e il suo **referto**, col controllo *«con e senza spia, byte-identico»* | **DA FARE** |
| **3** | la **tabella** `doc/REGOLE_nascita.tsv` estesa col **contratto dell'ordine** | **DA FARE** |
| ### **4** | il **codice**: la funzione unica di nascita, i due `_eredita_*` **assorbiti**, il presidio *«regola non dichiarata»*. ### **Committato PRIMA del run del sigillo** | **DA FARE** |
| **5** | il **sigillo**: byte-identico al 72 contro `3ddc56d9` *(estratto in binario, e **verificato che NON contenga l'ancora della cura**)*, grandezze **E contatori**, più i **tre** casi che devono fallire | **DA FARE** |
| **6** | il **referto** del sigillo, e ### **STOP: il guardiano verifica prima di qualunque altro passo** | **DA FARE** |
| ### **7** | ⚠ **in CODA, e non in questo giro:** i **fatti mancanti** di `_eredita_psi_figli`, `semina`, `_allaccia`, `_nasce`, `decidi_divisione` in `doc/FATTI_dal_codice.md`. ### **Sto toccando funzioni senza un solo fatto verificato**, ed è la lacuna di `FATTI-AVVIO` | **IN CODA** |

### 📌 **E una cosa che NON faccio, per `L-UN-PROMPT`:** i rilievi che nascono durante questo
lavoro ### **vanno in coda, non lo interrompono.**
