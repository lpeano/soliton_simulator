# LA CHIUSURA DELL'ERA `1` — **il simulatore del SECONDO ordine, fotografato**

> ### ⛔ **DECISIONE DI LUCA, 2026-10-08.** Questo documento ### **non cambia niente**: ### **fotografa** cio' che l'era `1` ha prodotto, e dice ### **perche'** lo si cambia.
>
> *Ogni numero esce da un'uscita committata o si ### **estrae dal referto con un'espressione** — e in quel caso il generatore ### **ASSERISCE che ci sia**: se il referto cambiasse, questo documento ### **non si scriverebbe** invece di scrivere un numero vecchio.* *(`L-NUMERI`)*

---

# 📌 `①` **CHE COSA FOTOGRAFA**

| | |
|---|---|
| il ### **simulatore** | `soliton_simulator.py`, blob ### **`b8c21049b85ba36a828f49dfa225d42419f3baf5`** *(sha1 dei byte grezzi, dal DISCO)* |
| la ### **forma** | ### **SECONDO ordine**: `phivel` con l'inerzia `M_PH`, un passo a ### **piu' settori**, e le leggi ### **non derivate da una sola `H`** |
| la ### **scena di riferimento** | `12802` nodi, `471564` archi, `DT = 0.01`; l'argv del driver con ### **`32` flag cambiati** rispetto ai default del sorgente |
| i suoi ### **sigilli** | tutti quelli di `csv/_seal_fork/` e `csv/_test_fork/`, con i blob nell'inventario. ### **Un sigillo si rigira AL SUO COMMIT** |
| le sue ### **leggi** | ### **`419` scritture di stato** su `339` nomi, da `68` funzioni *(`csv/_test_fork/_censimento_leggi.py`)* |

# ⛔ `②` **I DOCUMENTI CHE SPIEGANO PERCHE' LO SI CAMBIA**

| | |
|---|---|
| ### **`A16`** *(`doc/ASSIOMI.md`, in testa)* | ### **primo ordine, UNO stato, UNA `H`**: `i·dψ/dt = ∂H/∂ψ*`, e `φ` ### **si legge** da `ψ` |
| ### **`A17`** *(in testa, prima di `A16`)* | ### **ogni comportamento e' determinato solo dal suo ambito:** ### **niente `pos` nella fisica** |
| `doc/RISCRITTURA_PRIMO_ORDINE.md` | che cosa ### **sparisce**, che cosa ### **rinasce in forma nuova**, e il banco |
| `doc/TRADUZIONE_IN_H.md` | le ### **leggi in cinque classi**, la `H` candidata, la regola di crescita ### **a parte**, e l'### **elenco delle decisioni** |
| `doc/REGISTRO_FISICA.md` | le ### **schede delle decisioni PRESE** di Luca |

# ⭐ `③` **I NUMERI DI RIFERIMENTO** — *dai referti, non ricopiati*

## `③.1` **`D1`: la coppia POMPA**

| | |
|---|--:|
| passi con `P_coppia` ### **positiva** | ### **`230 su 230`** |

### ➜ **La coppia d'interferenza immette energia a OGNI passo misurato.** Non e' una tendenza: e' ### **tutti**.

## `③.2` **`D2` e `D2-BIS`: la coppia che LEGGE LA FASE tiene le masse**

| braccio | che cosa prova | ### **`AUC` materia/vuoto** |
|---|---|--:|
| `base` | il riferimento, con tutto acceso | ### **`0.7371`** *(al passo `300`)* |
| `B-TS` | ### **senza la coppia che legge la fase** *(bagno + scuotimento, coppia spinoriale)* | ### **`0.4848`** *(al passo `400`)* |
| `B-SCAL` | la coppia ### **SCALARE** *(che legge la fase)*, col bagno | ### **`0.9020`** *(al passo `400`)* |
| `B-SCAL-TS` | la coppia ### **SCALARE** ### **senza bagno** | ### **`0.9394`** *(al passo `400`)* |
| `B-SCAL-TS-NOSYNC` | lo stesso, ### **senza sincronizzazione** | ### **`0.9333`** *(al passo `400`)* |

### ➜ **IL FATTO CHE HA DECISO:** il braccio con la coppia ### **spinoriale** *(che ### **non** legge la fase che muove)* sta a `0.4848`; quelli con la coppia ### **scalare** *(che la legge)* stanno sopra `0.90`. ### **Cio' che tiene le masse coerenti e' LA FORMA DELLA COPPIA**, non la quantita' di energia immessa.

## `③.3` **`D2-TER`: senza sincronizzazione**

| | |
|---|--:|
| `AUC` al `400` ### **senza** sincronizzazione | ### **`0.9333`** |
| `AUC` al `400` ### **con** | `0.9394` |
| la ### **cinetica** cresce di | ### **`×2.4862`** *(da `1000.5497` a `2487.5607`)* |
| la sincronizzazione toglieva, ### **a `A` fissa** | ### **`93.44 %`** della crescita di `H` *(da `23782.6394` a `1559.4201`)* |

### ➜ **La sincronizzazione «pompava senza ordinare»:** toglieva il ### **`93.44 %`** della crescita di `H` e costava ### **`0.0061`** di `AUC`. ### ⚠ **E le DUE letture della cinetica sono RICONCILIATE nel referto, non scelte:** `×2.4862` *(prima del passo)* contro `×2.0376` *(dopo)* — la differenza e' il primo passo, che inietta `222.3697`, e ### **la clausola `< ×3` passa in entrambe.**

## `③.4` ### ⛔ **I DUE «NO» DIMOSTRATI** — *non «non l'ho trovata»: DIMOSTRATI*

| | il numero | |
|---|--:|---|
| la ### **SINCRONIZZAZIONE** e' ### **asimmetrica** | ### **`1.0641`** contro un pavimento ### **calcolato** di `1.438e-10` | ### **nove ordini sopra**, e identica ai tre passi `h` ⇒ ### **nessuna `E(φ)` esiste** di cui `K_SYNC` sia il gradiente |
| la ### **COPPIA DEL DRIVER** ### **non legge `φ`** | ### **`0.000e+00`** | scrive una coppia su `φ` leggendo ### **lo spinore** ⇒ spazio d'ingresso ≠ spazio d'uscita |
| *(il controllo positivo)* | `5.178e-12` contro `4.936e-09` | la coppia ### **scalare** e' ### **simmetrica**: il banco ### **funziona** |
| *(il caso che deve fallire)* | `1.463e-02` | una coppia ### **sintetica** col prefattore di nodo risulta ### **asimmetrica**: il banco ### **DISCRIMINA** |

## `③.5` **IL MARE `v1` e `v2`**

| | esito | il numero |
|---|---|---|
| ### **`v1`** | ### ⛔ **NON DECIDIBILE come era scritto** | `Σ_j w_kj` varia di un fattore ### **`39.8`**, quindi il «mare uniforme» e' uniforme ### **solo in modulo**: lo stato costante ### **non era stazionario**, e la localizzazione a `g = 0` era ### **del GRAFO**. ### **E il tetto dei `20` minuti fu superato** *(`1274.2` s = `21.24` minuti)* |
| ### **`v2`** | ### ⛔ **LO STATO PIU' BASSO E' GIA' UNA MASSA** | a `g = -5`: un nodo ### **`-400000.0`** contro il mare esteso `-18533.8`. ### **E nessun `ρ_0` salva:** alla soglia `\|g\|ρ_0` vale `0.02944` e `0.00501` contro `λ_max` `5.6494` e `1.0000` |
| ### ⭐ **e il numero che resta in mano** | la ### **geometria da sola** concentra | il `PR` del Perron a `g = 0`: ### **`24.6`** su `400` senza normalizzazione, ### **`348.2`** con |

## `③.6` **IL BILANCIO DELLA NASCITA, e lo SPARTIACQUE**

| | |
|---|--:|
| la concentrazione ### **libera** | ### **`381466.2`** |
| la ### **prima divisione** costa | ### **`199600.0`** *(il `52.32 %`)* |
| la cascata ### **si ferma da sola** al livello | ### **`4`** — cioe' a ### **`16` nodi** |
| ### ⭐ **LO SPARTIACQUE delle due fermate** | ### **`ρ = 25.0` per nodo** |

### ➜ **Sopra `ρ = 25.0` prevale il CALORE** *(e la barriera ### **non lavora**)*; ### **sotto prevale il TETTO** *(e la materia ### **resta compressa**)*. ### ⛔ **Sono due REGIMI FISICI diversi**, e quale sia il nostro dipende dall'### **unita' di stato**, che e' ### **aperta**.

# ✔ `④` **LE DECISIONI PRESE** *(schede in `doc/REGISTRO_FISICA.md`)*

| | la decisione | il motivo in un numero |
|---|---|--:|
| ### **`(B)`** | ### **la SINCRONIZZAZIONE SI TOGLIE**, perche' ### **emergera'** | asimmetria `1.0641`; e toglierla costa `0.0061` di `AUC` |
| ### **`(A)`** | ### **il CALORE del vuoto locale PAGA LA NASCITA** | `381466.2` liberati contro `199600.0` richiesti |
| ### **`(C)`** | ### **il FRENO della coesione e' la `(c)`: nascita PIU' degenerazione con BARRIERA PER NODO in `H`** | senza barriera, al livello `4` il calore finisce e ### **non resta nessun freno** |

### ⚠ **E DUE CAUTELE che stanno nelle schede:** *«Pauli»* e' un'### **ANALOGIA** *(la doppia copertura e' necessaria ma ### **non sufficiente** per la statistica di Fermi)*, e la barriera e' derivata ### **dalla struttura** — due componenti, `LAM` — ### **non dalla statistica**.

# ⛔ `⑤` **LE DECISIONI APERTE E LE TENSIONI, nell'ordine delle DIPENDENZE**

### **La catena** *(e l'ordine non e' una preferenza: e' la chiusura delle dipendenze di `25858a9`)*:

| | che cosa manca | ### **perche' viene prima** |
|--:|---|---|
| ### **`1`** | ### ⭐ **L'UNITA' DI STATO** — quanta `ρ` vale ### **uno** stato | ### **decide IL REGIME:** sopra `ρ = 25.0` lavora il calore, sotto lavora il tetto. ### **Finche' e' aperta non si sa se la barriera lavora** |
| ### **`2`** | il ### **VUOTO LOCALE** in forma ### **relazionale** | lo chiedono ### **tutte e tre** le decisioni prese: senza di esso la cura di `A16` ### **reintrodurrebbe `pos` dal lato del vuoto** |
| ### **`3`** | la ### **GEOMETRIA dentro `H`** *(decisione `9`)* | `d ≥ LAM` come ### **barriera d'energia** ha senso solo se `d` ha una dinamica che ### **sente** la barriera |
| ### **`4`** | l'### **AGGANCIO degli orologi COME MISURA** | e' il criterio che ### **puo' riaprire** la decisione `(B)`, e richiede il vuoto locale |

> ### ⚠ **E UNA NOTA SULL'UNITA' DI STATO CHE CAMBIA COME SI LEGGE LA CANDIDATA:** la candidata `(2)` — `ρ₁ = λ_max/\|g\|` = ### **`1.1299`**, quindi `C = 2.2598` — e' derivata ### ⛔ **DENTRO LA SONDA**, cioe' da un termine ### **`\|ψ\|⁴` di SITO** e dallo ### **spettro di un grafo costruito con `pos`** *(`A17`!)*. ### ➜ **Va RICALCOLATA sulla `H` di Luca, dove la coesione e' un termine D'ARCO** — e lì `λ_max` e il significato stesso di `ρ₁` ### **cambiano**. ### **Il numero di oggi e' un ORDINE DI GRANDEZZA, non il valore.**

## **E FUORI DALLA CATENA** *(non si sbloccano a vicenda)*

| | la tensione | ### **la decisione che richiede** |
|---|---|---|
| ### **`T1`** | ### **la CRESCITA come POSTULATO o come TEOREMA.** Col margine ### **zero** il bilancio e' ### **simmetrico nel tempo**: la fusione restituirebbe esattamente quel calore, e ### **sarebbe permessa dall'energia** ⇒ `A14.2` resta un ### **postulato in piu'** | ### ⭐ **CANDIDATA DEL GUARDIANO, e il conto torna:** la ### **lunghezza minima `LAM`** vieta la fusione, perche' due nodi che si fondono dovrebbero ### **scendere sotto `LAM`**, mentre la nascita ### **spezza un arco `≥ 2·LAM` in due pezzi `≥ LAM`**. ### ➜ **L'asimmetria sarebbe GEOMETRICA, non energetica** — e `A13` diventerebbe la ragione di `A14.2`. ### ⛔ **DA VERIFICARE, non assunta** |
| ### **`T2`** | ### **UN SERBATOIO, PIU' USI:** nascita, aggancio degli orologi, freno vero — e il margine e' ### **zero** | ### **DI LUCA:** una ### **priorita'**; una contabilita' ### **separata**; oppure l'ipotesi che siano ### **LO STESSO processo** |
| ### **la SCENA INIZIALE** | `semina`, `_semina_lam`, `_semina_masse_coerenti` costruiscono la ### **topologia iniziale DAL DISEGNO** | ### **DI LUCA: e' ammessa da `A17` o va costruita in modo relazionale?** La scena fissa ### **quali nodi sono vicini**, e quella topologia ### **sopravvive per tutta la corsa** |
| ### **l'EREDITA' di `pos` ALLA NASCITA** | `_rn_div_pos`, `_rn_sch_pos`: il `pos` del nato ### **si eredita** | ### ⛔ **VIOLA `A17`**: un'eredita' di `pos` e' `pos` ### **dentro una legge di crescita**. Non e' rendering e non e' una condizione iniziale |
| ### **il default `POZZO_D = False`** | nel driver e' ### **ACCESO** *(`--pozzo-d`)*, quindi la violazione ### **non e' viva** — ma il ### **default del modulo** e' `False` | ### ⛔ **chi importa il simulatore senza il driver ha la GRAVITA' CHE LEGGE `pos`.** Per `A17` quel default e' ### **sbagliato**, e ribaltarlo e' ### **una decisione di Luca** |

### 📌 **E LO STATO DI `A17` MISURATO, perche' l'era `2` parta da un numero e non da un'impressione:** ### **`22` funzioni** leggono `pos` *(`66` occorrenze)*; delle ### **`6`** classificate ### **LEGGE FISICA**, ### **`9` su `13`** delle letture «dirette» sono ### **UN SOLO blocco** *(il centro di massa della sincronizzazione)*, ### **che la decisione `(B)` toglie.**

# 📌 `⑥` **IL RAMO DEL PRIMO ORDINE, e il patto sul flag**

| | |
|---|---|
| il ### **tag** | `era-1-secondo-ordine`, ### **annotato**, su questo commit |
| il ### **ramo** | `primo-ordine`, a partire ### **dal tag** |
| ### ⛔ **il flag `PRIMO_ORDINE`** | ### **NON si introduce qui.** Entra con la ### **PRIMA legge portata** |
| ### ⭐ **IL PATTO** | ### **a flag SPENTO il simulatore deve restare IDENTICO AL BIT all'era `1`** — e ### **non e' una promessa: lo dimostrano i SIGILLI VECCHI**, che girano sul ramo nuovo e devono dare ### **gli stessi numeri** |

### ⚠ **E IL TAG CONSERVA GLI STATI ORIGINALI DELL'INDICE:** la ### **sospensione** delle voci avviene ### **sul ramo nuovo**, non qui. ### **Chi vuole lo stato dell'era `1` lo trova al tag.**

---

# ⛔ **CHE COSA QUESTO DOCUMENTO NON DICE**

| | |
|---|---|
| che l'era `1` sia ### **sbagliata** | ### ⛔ **NO.** L'era `1` ha prodotto i ### **fatti misurati** che hanno deciso `A16` e `A17`. ### **Si chiude perche' ha risposto, non perche' ha mancato** |
| che la ### **`H` di Luca** sia scritta | ### ⛔ **no:** `doc/TRADUZIONE_IN_H.md` ha ### **termini candidati** e ### **`13` decisioni**, di cui ### **`3` prese** |
| che i difetti dell'era `1` siano ### **chiusi** | ### ⛔ **no: SOSPESI.** Il piano del triage e' in `doc/TRIAGE_ERA_1.md`, ### **scritto e NON eseguito** |
| che il prototipo sia ### **relazionale** | ### ⛔ **no**, e `A17` lo dichiara: grafo da punti in un ### **cubo**, pesi con distanza ### **euclidea** |
| le ### **scale e i semi** | `P3` ### **non e' soddisfatta** da nessuna delle misure del `2026-10-08`: uno snapshot, una scena, `3` semi nel prototipo |
