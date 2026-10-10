# 🔬 **IL PROTOTIPO `v3` — IL VUOTO LOCALE E LA SATURAZIONE SENZA `g`**

> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un ### **REPERTO** — la CI ### **non lo rigenera**, e il presidio verifica ### **il suo BLOB.**

*(**Generato** da `python proto_camminata/_referto3.py`, che legge `proto_camminata/uscite/letture_v3.json` prodotto da `python proto_camminata/_letture3.py`. Criteri, previsioni e soglie: `doc/TASK_HISTORY/2026-10-11_prototipo_camminata_v3.md`, **committato PRIMA del codice**. Decisioni: `VUOTO-LOCALE-DETERMINISTICO`, `SPIN-LEGATO-AL-MOTO`.)*

**LA SCENA:** `irregolare(n=120,gmin=2,gmax=6,seme=11)` — **120** nodi, **208** archi, **416** estremita-; `eps` di riferimento **0.5**; semi **[11, 23, 37, 53]**; `x0` scansionato su **[0.125, 0.5, 1.0, 2.0, 8.0]**; **40** tick *(e **200** per la conservazione)*.

### ⭐ **E LA PRIMA RIGA DEL REFERTO E' LA REGOLA DI FONDO DEL MANDATO:** ### **la fisica del `v2` non si invalida** — e la lettura `R` lo misura ### **al bit.**

## ⭐ **I TREDICI VERDETTI**

| | la lettura | la PREVISIONE *(scritta prima)* | il verdetto |
|---|---|---|---|
| `R` | **REGRESSIONE al v2** | ### **AL BIT**: il `v3` non invalida il `v2` | ### ✅ **CONFERMA** |
| `G` | **GAUGE** | invariante col vuoto e `N` accesi | ### ✅ **CONFERMA** |
| `1` | **ISOTROPIA** | invariante | ### ✅ **CONFERMA** |
| `2` | **CONO** | zero oltre un arco per tick | ### ✅ **CONFERMA** |
| `5` | **`C`, e i due CONTROLLI** | `N` e `(D)` tengono; `rho` e `(E)` **DEVONO rompere** | ### ✅ **CONFERMA** |
| `V` | **REVERSIBILITA-** | `k` avanti e `k` indietro **tornano** | ### ✅ **CONFERMA** |
| `3` | **CONSERVAZIONE MODIFICATA** | **non lo so**, ed e- la domanda | ### ⭐ **RISPOSTA** |
| `T` | **AUTOINTRAPPOLAMENTO** | sotto `x0 ~ 1` come il lineare; sopra, **un SALTO**; e **nessun collasso** | ### ⛔ **SMENTITA** |
| `F` | **LA FREQUENZA DEL GRUMO** | se c-e- intrappolamento, la frequenza cade **in un BUCO** | ### ⚠ **NON DECIDIBILE** |
| `A` | **MATERIA / ANTIMATERIA** | il grumo e il coniugato **si intrappolano uguale** | ### ✅ **CONFERMA** |
| `L` | **IL VUOTO RISPONDE** | **non lo so** | ### 📌 **LETTO** *(non si interpreta oltre)* |
| `C` | **RISONANZA DEI CICLI** | **non lo so** | ### ⭐ **RISPOSTA** |
| `S` | **LA VELOCITA- RISPETTO AL CONO** | esiste un **`eps*`** che porta il fronte **piu- vicino al cono** | ### ⛔ **SMENTITA** |

## 📌 **I NUMERI, lettura per lettura**

### `R` **REGRESSIONE al v2** — ### ✅ **CONFERMA**

nelle **tre** scene: `curva` **0**, `gauge_puro` **0**, `identita` **0** — ### **zero esatto**, su `40` tick

### `G` **GAUGE** — ### ✅ **CONFERMA**

densita' per nodo **4.86e-17** su soglia **5.33e-14**, ### **col vuoto e `N` accesi** — e il vuoto e' **NEUTRO**: non si trasforma

### `1` **ISOTROPIA** — ### ✅ **CONFERMA**

**1.08e-16** su soglia **5.33e-14**, e la rinumerazione **porta i versori, le `U` e il vuoto**

### `2` **CONO** — ### ✅ **CONFERMA**

oltre **3** archi: **0** su **178** estremita', ### **col vuoto e `N`**

### `5` **`C`, e i due CONTROLLI** — ### ✅ **CONFERMA**

`N` **0** e `(D)` **0** *(entrambi sotto **5.33e-14**)*; e i **due controlli ROMPONO**: `(E)` **0.000111**, `rho` **3.86e-05**. ### ⭐ **Le due forme DISPARI tengono, le due PARI rompono** — e non e' una coincidenza: e' **il conto della parita'**

### `V` **REVERSIBILITA-** — ### ✅ **CONFERMA**

il peggiore delle tre non linearita' e' **2.22e-15**, su soglia **3.69e-12** *(`2k n_est eps`)*

### `3` **CONSERVAZIONE MODIFICATA** — ### ⭐ **RISPOSTA**

### ⭐ **`N` la CONSERVA** *(e con lei `(E)`, e il controllo lineare)*: e' la **PRIMA volta in tre prototipi** che una grandezza oltre le norme si conserva **con una non linearita' accesa** — ed e' quello che una costruzione **hamiltoniana** doveva dare. ### ⛔ **`(D)` invece DERIVA**, e ### **non e' splitting**: con il sotto-passo **FISSATO a `4`** l'esponente contro `dtau` resta **-0.05 ± 0.12** *(uno splitting darebbe `~2`)*. ### ⚠ **E il controllo non hamiltoniano del `v2` fa <<OSCILLANTE LIMITATA>>**, come doveva. ### **Conservate: E, N, lineare**

### `T` **AUTOINTRAPPOLAMENTO** — ### ⛔ **SMENTITA**

### ⛔ **NESSUN SALTO, e nessun intrappolamento:** il rapporto fra la frazione entro **un arco** e il **fondo uniforme** resta **1.37..1.83** per `N`, contro **1.82** del **lineare** — cioe' ### **uguale al lineare**, e a `x0 = 8` perfino **piu' basso**. ### ✅ **MA LA SECONDA META' DELLA PREVISIONE REGGE, ed e' la saturazione:** la frazione massima **su un singolo nodo** resta **0.0404** — ### **nessun collasso**

### `F` **LA FREQUENZA DEL GRUMO** — ### ⚠ **NON DECIDIBILE**

la non linearita' **sposta** la frequenza interna *(a `x0 = 1`: `N` **+0.2750**, `(D)` **+0.1044**, `(E)` **+0.1061** contro il lineare **+0.0436** rad/tick)*, e a `x0 = 8` `(E)` arriva a **+1.6727**. ### ⛔ **Ma senza intrappolamento la domanda <<cade in un buco?>> non e' decidibile**: il nodo di massima ampiezza sta a **1..3 archi** dal centro, cioe' ### **il grumo non sta fermo perche' non c'e' un grumo**

### `A` **MATERIA / ANTIMATERIA** — ### ✅ **CONFERMA**

`(D)` tiene la coniugazione ### **AL BIT** *(**0**, asimmetria **esattamente 0**)*, `N` a **1.66e-14**; e il controllo `(E)` ### **rompe** *(**2.4**, asimmetria fino a **0.0831**)*. ### ⭐ **E questa e' la lettura che il `v1` non poteva fare**

### `L` **IL VUOTO RISPONDE** — ### 📌 **LETTO** *(non si interpreta oltre)*

`Lambda` attorno al grumo **cambia**: da **-13.5%** a **+32.1%** sulla scansione. ### ⚠ **E anche col LINEARE cambia di +11.6%**, perche' il vuoto ### **evolve da solo** *(Grover e spostamento)*: quindi il segnale e' ### **la differenza dal lineare**, non il valore

### `C` **RISONANZA DEI CICLI** — ### ⭐ **RISPOSTA**

### ⛔ **NESSUNA olonomia li riporta:** scansionando la fase di un ciclo su **5** valori, a `eps = 0` gli stati a `±1` sono **352..356** e a `eps = 0.5` sono ### **ZERO, sempre**

### `S` **LA VELOCITA- RISPETTO AL CONO** — ### ⛔ **SMENTITA**

il **fronte** va da **0.768** archi/tick a `eps = 0` a **0.477** a `eps = 1`, **in modo MONOTONO** — e ### **non arriva MAI al cono** *(che e' `1` per costruzione)*. ### ⛔ **Quindi NON esiste un `eps*` che avvicini al cono: il massimo e' a `eps = 0`**, cioe' ### **senza il termine di massa.** ### ⚠ **E la propagazione NON e' isotropa**: da quattro nodi del grafo **REGOLARE** le velocita' sono **0.2436, 0.2270, 0.2271, 0.2098** — e un grafo regolare ### **dovrebbe darle uguali**

## ⛔ **LE CINQUE COSE CHE QUESTO REFERTO DICE E CHE NON ERANO NEL MANDATO**

### `1` **LA COSTRUZIONE HAMILTONIANA HA MANTENUTO LA SUA PROMESSA, E LE ALTRE DUE NO.** `N` **conserva** la conservazione modificata; `(D)` **no**, e ### **non e' un artefatto numerico** *(col sotto-passo FISSATO l'esponente contro `dtau` resta `~0`, mentre uno splitting darebbe `~2`)*. ### ⭐ **Nel `v1` e nel `v2` non c'era nemmeno la candidata: qui c'e', e per UNA delle tre forme funziona.**

### `2` **LA SATURAZIONE FA META' DI CIO' CHE PROMETTEVA, E LA META' CHE FA E' QUELLA CHE CONTA MENO.** ### ⛔ **Non lega**: il rapporto col fondo uniforme resta quello del lineare, a ogni `x0`. ### ✅ **Ma non fa collassare**: la frazione massima su un nodo resta sotto il **4%**. ### ⚠ **Era la previsione scritta, e si e' avverata ESATTAMENTE A META'.**

### `3` **IL VUOTO EVOLVE DA SOLO, E QUESTO CAMBIA COME SI LEGGE LA `(L)`.** `Lambda` attorno al grumo cambia **anche con la camminata LINEARE** *(`+11.6%`)*, perche' Grover e lo spostamento **lo mescolano**. ### ⭐ **Quindi <<il vuoto risponde>> non si legge dal valore, ma dalla DIFFERENZA dal lineare** — e lo scrivo perche' il valore da solo **sembrerebbe una risposta.**

### `4` **LA PROPAGAZIONE NON E' ISOTROPA SU UN GRAFO REGOLARE, E IL COLPEVOLE E' DICHIARATO.** Da quattro nodi dello stesso reticolo le velocita' differiscono del **~14%**. ### ⛔ **E non e' il reticolo: sono i VERSORI** — che sono `PROVV-VERSORI-NON-RELAZIONALI`, assegnati **per indice d'arco**, quindi ### **diversi da nodo a nodo anche dove la struttura e' identica.** ### ⭐ **E' la prova piu' diretta che quella scelta provvisoria SI VEDE nei numeri.**

### `5` **`eps` RALLENTA LA LUCE INVECE DI AVVICINARLA AL CONO.** Il fronte e' **piu' veloce a `eps = 0`** *(`0.768` archi/tick)* e scende **monotono** fino a `0.477` a `eps = 1`. ### ✅ **E ha senso: `eps` e' il termine di MASSA, e una massa RALLENTA** — ### **quindi la previsione <<esiste un `eps*` che avvicina al cono>> era sbagliata nel verso**, e il massimo e' **il caso senza massa.**

## ✅ **CHE COSA SBLOCCA O RIAPRE NELL-ALBERO** *(e nessuna decisione e' mia)*

| il nodo | che cosa dicono i numeri | che cosa NON dicono |
|---|---|---|
| **[[DOMANDA-QUANTITA-CONSERVATA]]** *(la prossima)* | ### ⭐ **UNA C'E':** la **conservazione modificata** di `N` *(quasi-energia lineare piu' `Sigma N_k`)* **si conserva** con la non linearita' accesa | non dicono che sia **L'ENERGIA**: la promozione e' ### **una decisione di Luca**, e il referto la chiama col nome che ha |
| **[[COESIONE-TERMINE-O-CAMPO]]** | ### ⛔ **la via `(a)` si indebolisce:** **tre** termini locali saturanti, e ### **nessuno lega** | non dicono che nessun termine locale possa: dicono che ### **questi tre non lo fanno** |
| **[[GUSCIO-ANTIFASE-EMERGENTE]]** | niente: ### **serve un grumo, e non c'e'** | e' la lettura `G1`, ### **in coda** |
| **[[PROVV-VERSORI-NON-RELAZIONALI]]** | ### ⭐ **la scelta SI VEDE:** rompe l'isotropia della propagazione su un grafo regolare *(`~14%`)* | non dicono da dove debbano venire: e' `DOMANDA-D9-GEOMETRIA` |
| **[[DOMANDA-C2-O-C4]]** | gli stati intrappolati sui cicli sono ### **`4` per ciclo** e `eps` li distrugge **tutti**, e ### **nessuna olonomia li riporta** | non dicono niente su `C^4` |
| **[[VUOTO-LOCALE-DETERMINISTICO]]** | la forma provvisoria ### **regge tutti i collaudi** *(gauge, cono, norme, reversibilita-, `C`)* e ### **il vuoto risponde** | non dicono che sia **la** forma: e' ### **dichiarata provvisoria** |

## ⚠ **I LIMITI, dichiarati**

| | il limite |
|---|---|
| `1` | ### **`cs_k = 1` ovunque**, e **`r = 1` nel banco**: il `v3` **non prova la `cs` locale** |
| `2` | ### **un solo grafo irregolare** e un regolare: **non e' uno scaling di taglia finita** *([[TAGLIA-FINITA]])* |
| `3` | il grumo e' ### **costruito da me**, su **un** centro e **un** raggio: se l'intrappolamento dipendesse dalla FORMA, questo referto **non lo vedrebbe** |
| `4` | ### **`(D)` ed `(E)` usano il punto medio implicito**, con sotto-passi **derivati** *(`{'D': 4, 'E': 4}`)*: un metodo **diverso** da quello di `N`, che e' **esatto** |
| `5` | la `(F)` misura una frequenza ### **su un grumo che si disperde**: il numero c'e', ma **il suo significato no** |

