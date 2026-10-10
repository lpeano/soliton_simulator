# 🔬 **IL PROTOTIPO `v2` — SPIN LEGATO AL MOTO, CON `U(2)` SUGLI ARCHI**

> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un ### **REPERTO**, cioe' ### **che cosa si e' misurato A UN ISTANTE** — la CI ### **non lo rigenera**, e il presidio verifica ### **il suo BLOB.**

*(**Generato** da `python proto_camminata/_referto2.py`, che legge `proto_camminata/uscite/letture_v2.json` prodotto da `python proto_camminata/_letture2.py`. Criteri, previsioni e soglie: `doc/TASK_HISTORY/2026-10-10_prototipo_camminata_v2.md`, **committato PRIMA del codice**. Decisione: `SPIN-LEGATO-AL-MOTO`.)*

**LA SCENA:** `irregolare(n=120,gmin=2,gmax=6,seme=11)` — **120** nodi, **208** archi, **416** estremita-, gradi **[2, 3, 4, 5, 6]**; `eps` di riferimento **0.5**; semi **[11, 23, 37, 53]**; **200** tick per cluster e conservazione.

### ⭐ **E IL `v1` ERA DUE CAMMINATE SCALARI:** la lettura `B` qui sotto dice che nel `v2` le due componenti ### **si equilibrano** — e- la differenza che rende la lettura `5` ### **una prova fisica invece di un'algebra.**

## ⭐ **I DIECI VERDETTI**

| | la lettura | la PREVISIONE *(scritta prima)* | il verdetto |
|---|---|---|---|
| `G` | **GAUGE** | le osservabili invarianti **non cambiano** | ### ✅ **CONFERMA** |
| `G!` | **IL BRACCIO CHE DEVE FALLIRE: i versori** | coi versori **non ruotati** le osservabili **DEVONO** cambiare | ### ✅ **FALLISCE, E DEVE** |
| `1` | **ISOTROPIA** | rinumerare **non cambia niente** | ### ✅ **CONFERMA** |
| `2` | **CONO** | oltre il cono, **zero al bit** | ### ✅ **CONFERMA** |
| `B` | **BANDE ACCOPPIATE** | `eps = 0` e identita': **zero**; `eps > 0`: **> 0** | ### ✅ **CONFERMA** |
| `M` | **MASSA O NO** | ### **NIENTE GAP** *(D'Ariano-Perinotti: `C^2` + versori isotropi)* | ### ✅ **CONFERMA** |
| `3` | **QUANTITA- CONSERVATA** | **non lo so** — nessuna previsione da smentire | ### ⛔ **NESSUNA TROVATA** *(criterio di RIAPERTURA)* |
| `4` | **CLUSTER** | **non ho conti** che prevedano un cluster stabile | ### ⚠ **NON DECIDIBILE** |
| `5` | **MATERIA / ANTIMATERIA** | `(A)` **DEVE** rompere `C`; `(B)` **no** | ### ✅ **CONFERMA** |
| `O` | **OLONOMIA (controllo)** | **non cambiano**: le `U` sono fisse | ### ✅ **CONFERMA** |

## 📌 **I NUMERI, lettura per lettura**

### `G` **GAUGE** — ### ✅ **CONFERMA**

densita' per nodo **5.55e-17**, olonomie **1.48e-15**, spettro **1.02e-14** — tutte sotto la soglia **5.33e-14**

### `G!` **IL BRACCIO CHE DEVE FALLIRE: i versori** — ### ✅ **FALLISCE, E DEVE**

coi versori **NON ruotati** la densita' differisce di **0.0123**, cioe' **11 ordini di grandezza** sopra la soglia. ### ⭐ **E- la PROVA che i riferimenti locali NON sono ridondanti**, e il punto `1` del mandato regge

### `1` **ISOTROPIA** — ### ✅ **CONFERMA**

il peggiore delle tre scene e' **1.21e-16**, su soglia **5.33e-14** — e la rinumerazione **porta i versori e le `U`**, non li rigenera

### `2` **CONO** — ### ✅ **CONFERMA**

oltre **3** archi, nelle **tre** scene e **col trasporto acceso**: **0** su **178** estremita'

### `B` **BANDE ACCOPPIATE** — ### ✅ **CONFERMA**

nella scena **identita'** con `eps = 0` il peso nell'altra componente e' **0** *(zero esatto, come il `v1`)*, e con `eps > 0` arriva a **0.5033** — cioe' **le due componenti si EQUILIBRANO**. ### ⭐ **E con `eps = 0` ma trasporto curvo e' gia' **0.3528**: mescola anche il TRASPORTO**

### `M` **MASSA O NO** — ### ✅ **CONFERMA**

il **gap massimo diviso la spaziatura media** va da **64.9** a `eps = 0` a **3.24** a `eps = 1`, **in modo MONOTONO**. ### ⭐ **Quindi `eps` NON apre un gap: lo CHIUDE** — e la previsione *(nessuna massa con `C^2` e versori isotropi)* **regge**. ### ⚠ **E il gap grosso a `eps = 0` non e' una massa: e' lo spettro della camminata SCALARE di Grover**, cioe' **esattamente il `v1`**

### `3` **QUANTITA- CONSERVATA** — ### ⛔ **NESSUNA TROVATA** *(criterio di RIAPERTURA)*

per la camminata **LINEARE** le quattro candidate sono **tutte CONSERVATE** nelle due scene *(ed e' il controllo positivo: la quasi-energia di un passo unitario e' conservata **per una ragione esatta**)*; per le **12** varianti non lineari la **norma** e' sempre conservata e delle tre candidate oltre la norma ****NESSUNA si conserva****. ### ⚠ **Ma in 16 casi l'esito e' <<OSCILLANTE LIMITATA>>**, che e' **meno che conservata e piu' che deriva** — e nel `v1` non era cosi' netto

### `4` **CLUSTER** — ### ⚠ **NON DECIDIBILE**

nella scena **identita'** la dispersione **cresce in ogni variante** *(da **+0.372** a **+0.503**)*: la coerenza **si perde**, e la formula del piano e' *«la non linearita' scelta NON BASTA»*. ### ⛔ **Nella scena CURVA la lettura NON E' DECIDIBILE, e il motivo e' nei numeri:** la dispersione **PARTE da 1.491** *(contro `0.65` nell'identita')*, cioe' **vicina alla saturazione**, perche' il trasporto casuale **scompiglia le fasi subito** — quindi la crescita piccola *(+0.092)* **non vuol dire piu' coerenza**

### `5` **MATERIA / ANTIMATERIA** — ### ✅ **CONFERMA**

**`(A)` ROMPE la coniugazione in 6 varianti su 6** *(fino a **0.198**, asimmetria dell'intrappolamento fino a **0.0474**)* — ### ed e' **il braccio che DEVE fallire**; **`(B)`, l'elicita', la rispetta in 6 su 6** *(al massimo **7.1e-16**, cioe' virgola mobile)*. ### ⭐ **E QUESTA VOLTA E- UNA PROVA FISICA, non un'algebra:** la lettura `B` dice che le due componenti **si equilibrano**, quindi la simmetria **non passa per costruzione**

### `O` **OLONOMIA (controllo)** — ### ✅ **CONFERMA**

le olonomie **non cambiano** durante la corsa nelle tre scene: **0** — ed e' **un CONTROLLO**, perche' le `U` sono fisse *(se cambiassero, il banco non sarebbe quello che dichiara)*

## ⛔ **LE QUATTRO COSE CHE QUESTO REFERTO DICE E CHE NON ERANO NEL MANDATO**

### `1` **IL GAP C'E', MA A `eps = 0` — E NON E' UNA MASSA.** Il rapporto gap/spaziatura e' **64.9** a `eps = 0` e **3.24** a `eps = 1`: ### **`eps` CHIUDE il gap invece di aprirlo.** ### ⭐ **E il gap grosso a `eps = 0` e' lo spettro della camminata di Grover SCALARE**, cioe' **esattamente il `v1`** — quindi ### **quel gap era nel `v1` e non era una massa nemmeno la'.**

### `2` **LA TENDENZA MONOTONA DEL `v1` NON SOPRAVVIVE.** Nel `v1` la crescita della dispersione **scendeva monotona** con `g`, e ci avevo costruito una proposta *(`PROPOSTA-SCANSIONE-FORZA-NONLINEARE`)*. ### ⛔ **Qui no:** nella scena identita' va **+0.488, +0.503, +0.499** al crescere di `g`. ### ✅ **Quella tendenza era una proprieta' della camminata SCALARE**, e la proposta va **annotata.**

### `3` **NELLA SCENA CURVA LA LETTURA `4` NON E' DECIDIBILE, e il motivo e' nei numeri:** la dispersione **parte** da `~1.47` contro `~0.65` dell'identita', cioe' ### **vicina alla saturazione** — il trasporto casuale **scompiglia le fasi subito.** ### ⚠ **Quindi la crescita piccola NON vuol dire piu' coerenza**, e chiamarla <<il cluster tiene>> sarebbe **leggere un artefatto.**

### `4` **`(B)` DA' <<OSCILLANTE LIMITATA>> DOVE IL `v1` DAVA <<DERIVA>>.** Non e' una conservazione, ### **ma non e' la stessa cosa di una deriva** — e con l'elicita' succede **piu' spesso** che con la densita'. ### ⛔ **Non lo chiamo un risultato: lo chiamo un INDIZIO**, e la differenza fra le due parole e' **quante volte l'ho visto.**

## ✅ **CHE COSA SBLOCCA O RIAPRE NELL-ALBERO** *(e nessuna decisione e' mia)*

| il nodo | che cosa dicono i numeri | che cosa NON dicono |
|---|---|---|
| **[[MATERIA-ANTIMATERIA-SPAZIO]]**, condizione `(b)` | ### ⭐ **ADESSO E' UNA PROVA FISICA:** le componenti **si equilibrano** *(lettura `B`)* e l'elicita' tiene la coniugazione **a virgola mobile** su **tutte** le varianti | non dicono che l'elicita' sia **la** forza di coesione: la lettura `4` dice che **non tiene il cluster** |
| **la forza di COESIONE** *(il nodo `FC`)* | una candidata **ammissibile** e **invariante di gauge** esiste, ed e' **l'elicita'** | ### ⛔ **non basta a tenere un cluster**, e **da dove viene `g`** resta `A1` |
| **[[DOMANDA-QUANTITA-CONSERVATA]]** *(la prossima)* | ### **nessuna** delle tre candidate oltre la norma si conserva, **in nessuna delle due scene** | non dicono che non esista: dicono che **non l'ho trovata fra le candidate dichiarate**, e in alcuni casi l'esito e' **oscillante limitata** |
| **[[DOMANDA-D9-GEOMETRIA]]** | ### ⭐ **i versori NON sono ridondanti, MISURATO** *(lettura `G!`)*: senza ruotarli la densita' cambia di `1.2e-2` | non dicono **da dove vengano**: e' `PROVV-VERSORI-NON-RELAZIONALI`, e la risposta e' `D9` |
| **`C^2` contro `C^4`** *(`A16`)* | con **`C^2`** e versori isotropi ### **nessun gap si apre con `eps`** | non dicono che `C^4` ne aprirebbe uno: **non l'ho provato**, ed e' una proposta per Luca |
| **[[D13]]** e **[[M-SPINORE]]** | con le `U` **fisse** tutto e' coerente, e le olonomie **non cambiano** *(controllo)* | ### ⛔ **niente sulle `U` DINAMICHE**: in questo banco sono **una memoria congelata**, ed e' `PROVV-U-FISSE-TRE-SCENE` |

## ⛔ **ANNOTAZIONE DEL 2026-10-11 — LA LETTURA `M` MISURAVA LA COSA SBAGLIATA**

> ### ⛔ **E IL VERDETTO <<CONFERMA>> RESTA, ma per un ALTRO MOTIVO** — e i numeri qui sopra ### **non si riscrivono.**

### 📌 **CHE COSA MISURAVA:** il ### **gap MASSIMO ovunque sul cerchio** delle quasi-energie — non il gap ### **dove le bande si incontrano.** ### ⭐ **E il `64.9` a `eps = 0` veniva dalle BANDE PIATTE della camminata di Grover**, cioe- ### **dagli stati INTRAPPOLATI sui cicli.**

### ✅ **IL CONTO, rifatto con `python proto_camminata/_spettro.py` e con DUE METODI INDIPENDENTI** *(autovalori e ### **rango** di `U ∓ I`, che danno ### **gli stessi numeri**)*, su `832` stati e `89` cicli indipendenti:

| la scena | `+1` | `-1` | in tutto | per ciclo |
|---|---|---|---|---|
| identita-, `eps = 0` | **180** | **176** | **356** su `832` = **42.8%** | ### **4.00** |
| curva, `eps = 0` | **176** | **176** | **352** | ### **3.96** |
| **qualunque scena, `eps > 0`** | ### **0** | ### **0** | ### **0** | ### **0** |

### ⭐ **E IL NUMERO NON E- <<CIRCA>>: E- ESATTO, e vale su DUE GRAFI.** Con `c = m - n + 1` cicli indipendenti: nella scena ### **identita-** le molteplicita- sono ### **`2(m-n)+4` e `2(m-n)`** *(cioe- `4c` in tutto)*, nella ### **curva** sono ### **`2(m-n)` e `2(m-n)`** *(`4c-4`)*. ### ✅ **Verificato sul grafo irregolare *(`356` e `352`)* e sul REGOLARE *(`484 = 4x121` e `480`)*.**

### ⛔ **CHE COSA VUOL DIRE:** l-interferenza ### **intrappola il `43%` degli stati** — stati che ### **non vanno da nessuna parte**, `4` per ciclo — e il ### **legame spin-direzione li DISTRUGGE TUTTI**, gia- a `eps = 0.25`.

### ✅ **E IL GAP VERO, misurato DOVE LE BANDE SI INCONTRANO** *(`omega = 0` e `omega = pi`)*, con la ### **scala di taglia** sul grafo regolare: a `eps = 1` il gap assoluto e- ### **`3.7e-5`, `1.5e-3`, `1.2e-4`** per `n = 60, 120, 240` — cioe- ### **NON cresce con la taglia**, e in spaziature resta ### **O(0.1)**. ### ⭐ **Un gap VERO sarebbe `O(1)` in quasi-energia, quindi crescerebbe come `dim` in spaziature: questo NON lo fa.** ### ✅ **Quindi <<nessuna massa>> REGGE**, ma il motivo e- ### **che il gap al punto d-incontro e- nullo**, non che ### **`eps` chiuda un gap.**

## ⚠ **I LIMITI, dichiarati**

| | il limite |
|---|---|
| `1` | ### **`cs_k = 1` ovunque:** il `v2` **non prova la `cs` locale** |
| `2` | ### **`r_k`, `eps`, `g`, i versori e le `U` sono SONDE o scelte provvisorie**, e ognuna ha la sua voce |
| `3` | ### **un solo grafo irregolare**: non e' uno scaling di taglia finita *([[TAGLIA-FINITA]])* |
| `4` | ### **il verso curvatura ↔ EM non e' misurabile qui**, perche' `theta` e `V` sono **entrambi fissi** |
| `5` | la lettura `4` guarda **un cluster costruito da me**, e nella scena curva **satura subito** |

