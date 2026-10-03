# `COMMIT 5` DEL RIORDINO — `perc_geom` DEL NATO COME **DERIVAZIONE**, non come costante

*(mandato del guardiano su decisione di Luca del 2026-09-29, `doc/relazioni/2026-09-29.md` e
`doc/MITOSI_storia.md`. **Un commit alla volta: STOP dopo il referto del sigillo.**)*

> ### **LA DECISIONE:** `perc_geom` si **DERIVA dalla sua definizione** — `+1` se la media di
> `|tw|` sugli archi del nodo supera `PHI_CRIT`, altrimenti `-1` *(la stessa di `chi_basc`)*.
> Il nato ha archi con `tw = 0`, quindi **oggi** vale `-1`. ### **Scritta come DERIVAZIONE
> calcolata sugli archi del nato, NON come costante `-1`**, cosi' resta giusta quando
> `DIVISIONE-AUTOCONSISTENTE` dara' ai figli una torsione diversa da zero.

---

## ⚠ **PRIMA DI TUTTO: CIO' CHE HO GIA' GUARDATO PRIMA DI SCRIVERE QUESTO FILE**

**Lo dichiaro invece di far finta che il ragionamento sia tutto a priori** *(par.8: un ragionamento
riscritto a posteriori e' una ricostruzione, non un impegno)*. Prima di scrivere queste righe ho
letto **dal disco**: le due regole `_rn_div_perc_geom` / `_rn_sch_perc_geom`, la definizione in
`chi_basc`, i lettori del frame-drag, `ORDINE_DI_NASCITA` e `_ordine_di_nascita()`, le classi di
regola di `_deg`/`i`/`j`/`tw`/`twp`, `_grado()`, `semina`, `_allaccia`, la ricetta della scena
`MASSE-COERENTI`, e **ho misurato i flag della configurazione del driver**.
### **Quattro cose che ho trovato li' CAMBIANO il disegno, e stanno sotto.** Il resto di questa
sezione e' cio' che credevo **dal solo mandato**.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### **LE PREMESSE, dal mandato:**

1. `perc_geom` ha una **definizione** *(la media di `|tw|` sugli archi contro `PHI_CRIT`)*, e la
   regola di nascita di oggi **la ignora**: eredita dal genitore.
2. Un valore **ereditato** puo' contraddire la definizione: il nato ha `tw = 0`, quindi **la
   definizione dice `-1`** mentre l'eredita' dice *«quello che aveva il genitore»*.
3. Scriverla come **costante `-1`** sarebbe **giusto oggi e sbagliato domani**. Si scrive come
   **derivazione**.

### **COSA MI ASPETTO:**

- La derivazione sia **due righe**: la formula di `chi_basc` ristretta ai nodi nuovi.
- Il contatore `-1` / `+1` dia **sempre `-1`** *(tutti gli archi del nato a `tw = 0`)*.
- Il commit **NON** sia byte-identico: il frame-drag legge `perc_geom` prima che `chi_basc` lo
  riscriva, quindi **un passo di valore diverso entra nella dinamica.**

### ⛔ **COSA NON SO, e lo scrivo prima di guardare:**

- **se la derivazione si PUO' calcolare dentro `nascita()`**: non so in che ordine la tabella
  scrive `perc_geom` rispetto a `tw`, `i`, `j` e `_deg`.
- **quanti nati di oggi hanno un `perc_geom` ereditato diverso da `-1`.** Se fossero **zero**, il
  commit **sarebbe** byte-identico — ed e' il punto `(d)` del mandato.
- se `perc_geom` e' **letto** nella configurazione del driver: i lettori che ho visto nominare
  stanno sotto `CHI_COOP`, e **non so se e' accesa.**
- se `semina`, la scena e `_allaccia` scrivono `perc_geom`, e con quale regola.

---

## ⛔ **1-bis. LE QUATTRO COSE CHE HO TROVATO GUARDANDO, E CHE CAMBIANO IL DISEGNO**

### ① **`CHI_COOP = True` NELLA CONFIGURAZIONE DEL DRIVER — misurato, non assunto**

| flag | valore |
|---|---|
| `CHI_COOP` | ### **`True`** *(e `--chi-coop` e' nell'argv del driver)* |
| `CHI_BASC` | `True` · `CHI_CORE` `True` · `FRAME_DRAG` `True` · `TORS_4PI` `True` |
| `CHI_DA_SPINORE` | `False` · `VERSO_CHI` `False` |

### ➜ **Quindi `perc_geom` E' VIVO**, e il meccanismo del mandato tiene: `chi_basc` lo **scrive**
*(`:7560`, ramo `CHI_COOP`)* e il frame-drag lo **legge** *(`:7368`, ramo `CHI_CORE`,
`chiralita_core_locale(self.perc_geom, geom=True)`)*.
### 📌 **Se `CHI_COOP` fosse stata SPENTA, il commit sarebbe stato byte-identico per una ragione
PIU' FORTE di quella del punto `(d)`:** nessuno legge. **L'ho misurato prima di progettare il
sigillo**, perche' un criterio *«non byte-identico»* su una grandezza che nessuno legge
### **non potrebbe passare.**

### ② **IL MOMENTO IN CUI IL VALORE DEL NATO ENTRA, ed e' UNO SOLO**

`PASSO_COMPOSIZIONE` mette **`step` PRIMA di `mitosi`**. Quindi:

| | |
|---|---|
| passo `N` | `step` *(il frame-drag legge, `chi_basc` riscrive i nodi `0..n-1`)*, poi `mitosi` **crea il nato** col valore di nascita |
| passo `N+1` | `step`: il frame-drag a `:7368` legge **anche il nato**, ### **PRIMA** che `chi_basc` a `:7560` lo sovrascriva |

### ➜ **Il valore di nascita e' letto ESATTAMENTE UNA VOLTA**, all'inizio del passo dopo. Da li'
`chi_basc` lo riporta alla definizione da se'. ### **Quindi la differenza NON e' permanente: e' un
innesco**, e quanto cresce e' da misurare *(punto `(d)` del mandato)*.

### ⛔ ③ **LA DERIVAZIONE NON SI PUO' CALCOLARE DOV'E' OGGI: `tw` ARRIVA DOPO**

| posto in `ORDINE_DI_NASCITA` | grandezza |
|--:|---|
| 1 · 2 | `i` · `j` ### **(ci sono)** |
| 4 | `_deg` — ma la sua classe e' ### **`collocata`** *(`self._grado()`, che gira **DOPO** `nascita()`)*: ### **dentro la nascita `_deg` e' STANTIO** |
| ### **17** | ### **`perc_geom`** |
| ### **31** | ### **`tw`** |

### ➜ **Quando la regola di `perc_geom` gira, il `tw` dei nuovi archi NON ESISTE ANCORA**, e
`_deg` del nato **non esiste affatto**. ### **Una derivazione scritta li' leggerebbe lo stato
VECCHIO** — e darebbe `-1` **per il motivo sbagliato**, cioe' sarebbe la costante `-1` travestita.
### **Questo e' il vero contenuto del commit 5, e non era nel mandato.**

### ✅ **LA CURA, e usa il meccanismo CHE C'E' GIA':** `_ordine_di_nascita()` **deriva** l'ordine
dai registri con **un vincolo dichiarato** — `_peqn_idx` collocato subito dopo `peq`
*(vincolo 2 del contratto)*. Si aggiunge il ### **vincolo 3: `perc_geom` DOPO `tw`**, con la
stessa forma. ### 📌 **Non e' una manopola:** e' una **dipendenza di lettura** — la derivazione
legge `tw`, quindi `tw` va scritto prima.

### ④ **E LA DERIVAZIONE DEVE CALCOLARSI IL GRADO DA SE'**

`chi_basc` divide per `np.maximum(self._deg, 1)`. Dentro la nascita `_deg` e' stantio, quindi la
derivazione fa **cio' che fa `_grado()`**: `maximum(bincount(i, minlength=n) + bincount(j,
minlength=n), 1)`. ### **E LE DUE DIFFERENZE DA `chi_basc` VANNO DICHIARATE, non nascoste:**

| | `chi_basc` | la derivazione alla nascita |
|---|---|---|
| il grado | `self._deg` *(aggiornato da `_grado()`)* | ### **ricalcolato da `i`/`j`** — perche' `_grado()` non e' ancora girato |
| la torsione | `_tw_t`, ### **uno SNAPSHOT** preso prima nel passo | ### **`self.tw`** — alla nascita **non esiste** nessuno snapshot |

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci*

### **PASSO 1 — IL CENSIMENTO, prima del codice.** Uno strumento committato in
`csv/_test_fork/`, che per **ogni** sito dove nasce un valore di `perc_geom` per un nodo nuovo
riporta: **riga**, **regola di oggi**, **se gira nella configurazione del driver** *(misurato dal
runtime, non dedotto)*.
### **COSA DECIDE:** se il censimento trovasse un sito **che non ho previsto**, il commit 5 si
ferma e si ridisegna. **I siti che mi aspetto:** le due regole, `semina` *(`:4779`)*,
`Rete.__init__` *(`:3709`, array vuoto)*, `chi_basc` *(`:7560`, che non e' una nascita ma **e' la
definizione**)*. ### **E DUE CHE HO GIA' ESCLUSO LEGGENDO, e lo strumento deve CONFERMARE:**
`_allaccia` scrive solo grandezze **d'arco** *(nessuna per nodo)*, e la scena `MASSE-COERENTI`
*(`_semina_masse_coerenti`)* **non aggiunge nodi** — passa da `semina`.

### **PASSO 1-bis — LA SEMINA VA IN UN COMMIT A SE' (`5b`), e sono d'accordo col guardiano.**
**Il motivo e' quello che propone lui:** la semina cambia lo **STATO INIZIALE DI OGNI RUN**,
mentre divisione e Schwinger cambiano **solo i nati**. Mescolarle renderebbe il sigillo
### **ininterpretabile** *(par.3: un interruttore alla volta)*.
### ⚠ **E IL VINCOLO DA NON ROMPERE, che il mandato nomina:** `chi_nuovi` serve **anche** a
`perc_chi` *(`:4776`)* **e al calcio** *(`:4746`)*, quindi ### **l'estrazione da `rng` NON si
toglie** — l'ordine delle estrazioni e' un **contratto** *(`doc/CONTRATTO_nascita.md`)*. In `5b`
cambia **solo cio' che `perc_geom` riceve.**

### **PASSO 2 — LE DIFFERENZE ATTESE, scritte PRIMA del codice** *(e il criterio NON e'
«byte-identico tranne `perc_geom`»)*:

| | che cosa si pretende |
|---|---|
| **(a)** | ### **identico AL BYTE** fino al primo passo con nascita |
| **(b)** | in quel passo la ### **PRIMA** differenza e' `perc_geom` **dei nati** |
| **(c)** | la ### **SECONDA** e' dove il frame-drag la legge, e ### **si nomina con VOCE E RIGA** |
| **(d)** | da li' ### **quanto cresce** la differenza · e ### **quanti nati avevano un `perc_geom` ereditato diverso da `-1`** |

### 📌 **E `(d)` E' IL CRITERIO CHE PUO' RIBALTARE IL VERDETTO:** se quel numero fosse
### **ZERO**, il commit **sarebbe byte-identico**, e allora ### **(a)-(c) non proverebbero
niente** — andrebbe detto che il cambiamento e' **inerte in questa scena** e il sigillo si
appoggerebbe a un **controllo positivo costruito** *(un nato con eredita' `+1` iniettato)*.
### **Lo misuro PRIMA di scrivere il codice.**

### **PASSO 3 — IL CODICE, committato PRIMA del sigillo**, poi il sigillo sulle **tre scene del
commit 4** *(`72`/seme `11`, `150`/seme `11`, `72`/seme `12`)*.

### **I BRACCI CHE INTENDO METTERE:**

| | braccio | che cosa decide |
|---|---|---|
| **A** | il ### **RIORDINO DA SOLO** *(vincolo 3 attivo, eredita' invariata)* deve essere ### **BYTE-IDENTICO** | separa *«ho spostato una riga»* da *«ho cambiato una legge»*. ### **Senza questo braccio i due effetti sono mescolati** |
| **B** | le ### **tre scene**, (a)-(d) con la prima e la seconda differenza nominate | il criterio del mandato |
| **C** | il contatore ### **`-1` / `+1`** della derivazione, **misurato** | il mandato lo pretende: *«oggi atteso sempre `-1`, e il referto lo deve MISURARE»* |
| **D** | ### **IL CASO CHE DEVE FALLIRE:** una copia che ### **lascia l'eredita' in UN evento** deve essere vista dal sigillo ### **nel primo passo con nascita di QUEL evento** | e si fa ### **per i due eventi separatamente**, altrimenti un evento potrebbe coprire l'altro |
| **E** | ### **IL CONTROLLO POSITIVO della derivazione:** una copia dove un arco del nato ha ### **`tw` sopra `PHI_CRIT`** deve dare ### **`+1`** | ### **senza questo, il *«sempre -1»* non distingue una DERIVAZIONE da una COSTANTE** — ed e' `FALSO-ZERO` |

### ⛔ **COSA MI FAREBBE FERMARE:**

1. il censimento trova un sito **non previsto** → si ridisegna;
2. il riordino **da solo** NON e' byte-identico → **ho toccato qualcos'altro**, e si cerca cosa
   prima di procedere;
3. il braccio **E** da' `-1` anche con `tw` sopra soglia → ### **non e' una derivazione**, e il
   commit non va;
4. la prima differenza del passo di nascita **NON** e' `perc_geom` → l'ordine di lettura non e'
   quello che credo, e il par.2 del mandato va rifatto;
5. il punto `(d)` da' **zero** → il verdetto cambia forma *(vedi sopra)*, **non si allenta**.

---

## 3. TODO DEL NEXT STEP

1. ☐ **committare e pushare QUESTO FILE** *(par.8: prima del lavoro, cosi' l'ordine e'
   verificabile da git)*
2. ☐ `csv/_test_fork/_censimento_perc_geom.py` — il censimento, + voce d'inventario, **committato**
3. ☐ girarlo, **referto**, e **confrontare coi cinque siti che mi aspetto**
4. ☐ misurare il punto `(d)`: **quanti nati hanno eredita' diversa da `-1`**, sulle tre scene
5. ☐ scrivere le **differenze attese** nel referto, **prima** del codice
6. ☐ il **codice**: vincolo 3 in `_ordine_di_nascita()` + la derivazione nelle due regole +
   il contatore `-1`/`+1`; `doc/REGISTRO_FISICA.md`, `doc/CONTRATTO_nascita.md`,
   `doc/TABELLA_nascita.md` **rigenerata**, inventario, README se serve
7. ☐ il **sigillo** a cinque bracci, e il **referto**
8. ☐ **STOP** — e il guardiano verifica

### ⚠ **E LA SEMINA (`5b`) NON ENTRA QUI.** E' il punto `1-bis`.
