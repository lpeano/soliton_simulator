# IL PROTOTIPO `v2` — **SPIN LEGATO AL MOTO, CON `U(2)` SUGLI ARCHI**

> ### ⛔ **SCRITTO E COMMITTATO *PRIMA* DEL CODICE** *(par. `8`)*: il commit di questo documento
> e' **antenato** dei commit del banco `v2`, e l'ordine e' **verificabile da git.**

**Il mandato:** Luca, `2026-10-10`, *«IL PROTOTIPO `v2`: SPIN LEGATO AL MOTO, CON `U(2)` SUGLI
ARCHI»*. **Il punto `0`** *(la lettura del guardiano sul `v1`, annotata e **misurata**)* e' nel
commit `09bc987`; **il punto `6`** *(la piattaforma del collaudo della pulizia)* in `2c43e05`.

---

## `1` RAGIONAMENTO PRELIMINARE — **che cosa il `v1` NON poteva dire, e perche'**

### ⛔ **IL PUNTO DI PARTENZA E' UN LIMITE MISURATO, non un sospetto:** nel `v1` le due
componenti dello spinore **non si mescolano mai** — Grover e' uguale sulle due, la moneta di
banda e' **diagonale**, lo spostamento non le distingue. ### **Un pacchetto nella componente
`0` lascia l'altra a ZERO ESATTO dopo `200` tick, anche con le non linearita' accese.**

### 📌 **QUINDI IL `v1` E' DUE CAMMINATE SCALARI**, e tre cose che sembravano risultati sono
**altro**: la lettura `5` passava **per costruzione** *(vale l'algebra, non la fisica)*; la `7`
parlava della **non linearita'**, non della **massa**; la `3` e la `4` riguardavano **una
camminata scalare**.

### ⭐ **CHE COSA CAMBIA NEL `v2`, in una riga:** la moneta di spin
`exp(-i eps dτ_k σ·n_{k,a})` **NON e' diagonale** *(a meno che `n` sia `±ẑ`)*, quindi
**mescola le componenti** — e il trasporto `U(2)` sugli archi le mescola **anche durante lo
spostamento.** ### **Da qui in avanti <<banda>> non e' piu' una proprieta' globale.**

### **CIO' CHE CREDO PER COSTRUZIONE, e che mi aspetto di VERIFICARE**

| | che cosa | perche' lo credo |
|---|---|---|
| `a` | **`C ψ = i σ_y ψ*` commuta con OGNI `V ∈ SU(2)`** | per `V = aI + i b·σ` con `a, b` reali vale `V* = σ_y^{-1} V σ_y`, perche' `σ_x` e `σ_z` sono **reali** e `σ_y` e' **immaginaria**: il conto e' qui sotto |
| `b` | **la moneta di spin e' `C`-simmetrica** | `exp(-i α σ·n) = cos α I − i sin α (σ·n)` e' **della stessa forma** `aI + i b·σ` con `a, b` reali ⟹ sta in `SU(2)` ⟹ vale `(a)` |
| `c` | **Grover e' `C`-simmetrica** | e' **reale** e **scalare nello spinore**: commuta con `σ_y` e con la coniugazione |
| `d` | ### ⛔ **la fase `U(1)` NON commuta con `C`: la INVERTE** | `C(e^{iθ}ψ) = e^{-iθ} Cψ`. ### **E- il senso stesso di <<coniugazione di CARICA>>**: `C` manda la camminata con `θ` in quella con `−θ` |
| `e` | **l'elicita' e' l'invariante `C`-dispari che cerco** | `s_h = ψ†σψ` e' `C`-**dispari** e **ruota** col gauge; `n_h` ruota **allo stesso modo**; quindi **`s·n` e' invariante di gauge e `C`-dispari.** La derivazione e' qui sotto |

### 📌 **LA DERIVAZIONE DI `C`, per intero** *(e il conto e' corto)*

Con `C = i σ_y K` *(`K` = coniugazione)*, per una matrice `M` qualunque:
`C M ψ = iσ_y M* ψ*` e `M C ψ = M iσ_y ψ*`, quindi **`C M = M C ⟺ M* = σ_y^{-1} M σ_y`**.

Per `M = aI + i(b_x σ_x + b_y σ_y + b_z σ_z)` con `a, b` **reali**:

| | il conto |
|---|---|
| `M*` | `aI − i(b_x σ_x − b_y σ_y + b_z σ_z)` *(perche' `σ_y* = −σ_y`, le altre sono reali)* |
| `σ_y^{-1} M σ_y` | `aI + i(−b_x σ_x + b_y σ_y − b_z σ_z)` *(perche' `σ_y` anticommuta con `σ_x` e `σ_z`)* |

### ⭐ **SONO LA STESSA MATRICE**, quindi **`C` commuta con tutto `SU(2)`** — e con la moneta
di spin, che sta in `SU(2)`. ### ⛔ **E con `e^{iθ}` non commuta: lo coniuga.**

### ⚠ **PERCIO' IL BRACCIO `0` SI DICE IN DUE PEZZI, e lo scrivo PRIMA di misurare:**
**`(i)`** nelle scene **senza `U(1)`** *(identita', e la parte `SU(2)` da sola)* **`C` commuta
AL BIT**; **`(ii)`** con `θ ≠ 0`, `C` manda la camminata in **quella con `−θ`**, e la
*«simmetria»* e' **`C(U_θ ψ) = U_{−θ}(C ψ)` AL BIT.**
### ⛔ **NON E' UN FALLIMENTO: e' che la coniugazione di carica INVERTE LA CARICA**, quindi e'
una simmetria **della coppia** camminata/anti-camminata, non della singola camminata con un
campo acceso. ### **Se nessuna delle due forme e' esatta, MI FERMO e lo scrivo.**

### 📌 **LA DERIVAZIONE DELLA NON LINEARITA' `(B)`** *(il punto `4` del mandato)*

Serve una grandezza **locale**, **invariante di gauge** *(`SU(2)` e `U(1)`)*, e **dispari sotto
`C`**. Partendo da cio' che si costruisce da uno spinore su un'estremita':

| la grandezza | `U(1)` | `SU(2)` locale | sotto `C` | serve? |
|---|---|---|---|---|
| `ρ_h = ψ†ψ` | **invariante** | **invariante** | ### **PARI** | ### ⛔ no: e' la `(A)` |
| `s_h = ψ†σψ` | **invariante** | ### **RUOTA** *(non invariante)* | ### **DISPARI** | ### ⛔ no da sola |
| ### **`s_h · n_h`** | **invariante** | ### ✅ **INVARIANTE**: `s` e `n` ruotano **insieme** | ### ✅ **DISPARI** | ### ⭐ **SI'** |

### ⭐ **E QUELLA GRANDEZZA HA UN NOME: E' L'ELICITA'** — **lo spin proiettato sulla direzione
del moto.** ### ✅ **Quindi `(B)` e' la fase `exp(-i g h_k dτ_k)` con
`h_k = Σ_{estremita' di k} (ψ†σψ)·n`**, e `(A)` resta `exp(-i g ρ_k dτ_k)`, **pari sotto `C`**,
cioe' **il braccio che DEVE fallire.**

### ⚠ **E IL MOTIVO PER CUI I VERSORI SERVONO SI VEDE PROPRIO QUI:** senza `n` **non esiste**
uno scalare `SU(2)`-invariante e `C`-dispari costruito **localmente** dallo spinore — ### **la
direzione e' cio' che rende l'elicita' una grandezza.**

### ⚠ **CHE COSA NON SO — scritto adesso**

| | non so | e come lo sapro' |
|---|---|---|
| `1` | **se ci sia un GAP fra le bande** *(la massa)* | lettura `M`. ### **Previsione di D'Ariano-Perinotti: con `C²` e versori isotropi NIENTE gap** — un Weyl **senza massa**. ### ⚠ **Se un gap c'e', da dove viene** e' la domanda `C²` contro `C⁴` di `A16` |
| `2` | **quanta ampiezza passa all'altra banda** | lettura `B`: con `eps = 0` e trasporto identita' **zero esatto**; con `eps > 0` **non lo so** |
| `3` | **se l'elicita' basti a tenere un cluster** | letture `4` e `5`. ### **Non ho nessun conto che lo preveda** |
| `4` | **se la quantita' conservata esista adesso** | lettura `3`. ### **Nel `v1` non c'era fra le candidate dichiarate**, e il `v2` e' un'altra dinamica |
| `5` | ### ⛔ **se la gauge-invarianza regga NUMERICAMENTE** | lettura `G`. ### **In aritmetica esatta e' un teorema**; in virgola mobile e' **una misura**, e la soglia e' derivata |

---

## `2` PROGETTAZIONE — **le scene, le scelte, le soglie, e cosa mi FERMA**

### **LA SCENA, dichiarata** *(e le scelte PROVVISORIE sono marcate tali)*

| | che cosa | il valore | stato |
|---|---|---|---|
| grafo | lo stesso del `v1` | **`120` nodi, `208` archi, gradi `2`-`6`**, senza `pos` | **fissa** |
| stato | per **estremita' d'arco** | un'ampiezza **`C²`** | **fissa** |
| versori `n_{k,a}` | uno per **estremita' uscente** | **sfera di Fibonacci** per ogni grado, assegnati **in ordine di indice d'arco crescente** | ### ⚠ **PROVVISORIA** *(punto `2a`)*: l'origine **relazionale** e' `DOMANDA-D9-GEOMETRIA` |
| le `U` | **FISSE**, tre scene | **identita'** · **gauge puro** `V = g_k g_j^†`, `θ_kj = φ_k − φ_j` · **curvatura vera** *(olonomie non banali)* | ### ⚠ **PROVVISORIA** *(punto `2b`)*: le `U` **dinamiche** sono `D13` e `M-SPINORE` |
| `eps` | accoppiamento spin-direzione | **scansionato** su `{0, 1/4, 1/2, 1}` | ### ⚠ **PROVVISORIA** *(punto `2c`)*: **non tarato**, potenze di due |
| `g` | forza della non linearita' | **scansionato** su `{0, 1/4, 1/2, 1, 2}` | ### ⚠ **PROVVISORIA** *(punto `2c`)* |
| `r_k` | il ritmo locale | **dato**, in `[1/2, 1]`, col seme | come nel `v1` |
| nascita di `U` e `n` | su un arco nuovo | ### ⛔ **NON in questo banco** *(punto `2d`)*: nessuna mitosi | **fuori perimetro** |
| semi | — | **`11, 23, 37, 53`** | **fissi** |

### **L'ORDINE DEL PASSO, dichiarato** *(e non c'e' nessun ordine fra nodi o archi)*

```
psi' = SPOSTAMENTO_CON_TRASPORTO( NONLINEARE( GROVER( MONETA_DI_SPIN( psi ) ) ) )
```

| | il pezzo | la forma |
|---|---|---|
| `1` | **moneta di spin**, per estremita' | `exp(-i eps dτ_k σ·n_{k,a}) = cos α I − i sin α (σ·n)`, `α = eps·dτ_k` |
| `2` | **Grover**, per nodo | `(2/d)Σ − I`, **uguale sulle due componenti** |
| `3` | **non linearita'** | una fase per nodo: `(A)` con `ρ_k`, `(B)` con l'**elicita'** `h_k` |
| `4` | **spostamento con TRASPORTO** | `ψ'[partner(h)] = U[h] ψ[h]`, **tutti gli archi insieme**, con `U[2a+1] = U[2a]^†` |

### **LE SOGLIE, FISSATE ADESSO — e ognuna DERIVATA**

| | la soglia | la forma | da dove viene |
|---|---|---|---|
| `S1` | isotropia e **gauge** | `T · g_max · ε · ‖ψ‖` | il **conteggio delle operazioni**, come nel `v1` |
| `S2` | cono | ### **`0.0` AL BIT** | oltre il cono l'ampiezza **non e' mai stata toccata** |
| `S3` | norma | `passi · n_est · ε` | lo stesso conteggio |
| `S4` | pendenza nulla | `|pendenza| ≤ 3·σ_pendenza` | **l'errore della stima stessa** |
| `S6` | `C` e olonomie | ### **`0.0` AL BIT** | sono **identita' algebriche**: se non sono esatte, **l'implementazione ha un'asimmetria** |
| `S7` | **risoluzione** di una serie | `passi · n_est · ε · scala` | ### ⚠ **la lezione del `v1`**: un test di pendenza su cio' che varia **solo per arrotondamento** trova **sempre** una tendenza |

### **LE NOVE LETTURE, con PREVISIONE e CRITERIO** *(fissati qui, prima dei numeri)*

| | la lettura | la previsione | il criterio |
|---|---|---|---|
| **`G`** | **GAUGE** | le osservabili invarianti della scena di **gauge puro** *(con i versori RUOTATI)* sono **identiche** a quelle dell'identita' | `≤ S1` su **densita' per nodo**, **olonomie**, **spettro** |
| **`G!`** | ### ⛔ **IL BRACCIO CHE DEVE FALLIRE** | gauge puro **coi versori NON ruotati** da' osservabili **DIVERSE** | la differenza **` S1`**. ### ⭐ **E- la PROVA che i versori non sono ridondanti** |
| **`1`** | **ISOTROPIA** | rinumerare nodi e archi **coi loro versori** non cambia niente | `≤ S1`, e **`0.0` con `fsum`** |
| **`2`** | **CONO** | oltre `T` archi, **zero** | ### **`0.0` AL BIT** *(`S2`)*, con `T = eccentricita' // 2` |
| **`B`** | **BANDE ACCOPPIATE** | con `eps = 0` **e** trasporto identita': **zero esatto**; con `eps > 0`: **> 0** | il **trasferimento** fra le componenti. ### ⚠ **E con `eps = 0` ma trasporto `SU(2)`: `> 0` lo stesso**, perche' **e' il trasporto a mescolare** |
| **`M`** | **MASSA O NO** | ### **NIENTE GAP** *(D'Ariano-Perinotti: `C²` + versori isotropi ⟹ Weyl senza massa)* | il **gap massimo** nello spettro di quasi-energia, diviso la **spaziatura media**; <<c'e' un gap>> se **cresce con `eps`** e supera il valore a `eps=0` di **`3σ`** sui `4` semi |
| **`3`** | **QUANTITA' CONSERVATA** | **non lo so** | le candidate **dichiarate**, classificate coi **tre esiti** del `v1`, con `S7` **prima** della statistica |
| **`4`** | **CLUSTER** | **non ho conti** che lo prevedano | dispersione **pesata**, come nel `v1` |
| **`5`** | **MATERIA / ANTIMATERIA** | `(A)` **DEVE** rompere `C`; `(B)` **no** | ### ⭐ **E ADESSO E' UNA PROVA FISICA**, perche' le componenti **si mescolano davvero** |
| **`O`** | **OLONOMIA** | le olonomie **non cambiano** durante la corsa *(le `U` sono fisse)* | ### **`0.0` AL BIT** — e' **un controllo**, non una scoperta |

### **I PASSI, e cosa mi FERMA**

| | il passo | che cosa decide | che cosa mi FERMA |
|---|---|---|---|
| `0` | **`C` ridefinita, e il braccio `0` nelle tre scene** | se la lettura `5` **si puo' formulare** | ### ⛔ **se NESSUNA delle due forme** *(`C` commuta, oppure `C` manda `θ` in `−θ`)* **e' esatta: STOP e lo scrivo** |
| `1` | **la geometria**: versori, le tre scene, le olonomie | se la scena e' **quella che dico** | se un'olonomia della scena <<gauge puro>> **non e' banale**, la scena **non e' di gauge puro**: STOP |
| `2` | **lettura `G` e `G!`** | se i versori **servono** | ### ⚠ **se `G!` NON fallisce**, i versori sono **ridondanti** e il punto `1` del mandato **cade**: STOP e lo scrivo |
| `3` | **letture `1`, `2`, `O`** | se l'implementazione e' **quella che credo** | un rosso qui e' **un difetto mio** |
| `4` | **letture `B` e `M`** | **se e come lo spin si lega al moto**, e **se c'e' una massa** | — |
| `5` | **letture `3`, `4`, `5`** | se l'elicita' **serve** | ### ⚠ **se `(A)` non rompe `C`**, non ho capito la simmetria: STOP |
| `6` | **il referto** | che cosa **sblocca** o **riapre** | — |

---

## `3` LA STELLA POLARE — **le cinque risposte** *(`[[L-STELLA]]`)*

| | la domanda | la risposta per il `v2` |
|--:|---|---|
| `1` | **`A14`: conserva energia e carica LOCALMENTE?** | ### ✅ **LA NORMA SI', e adesso per DUE ragioni:** la moneta di spin e' **unitaria** *(sta in `SU(2)`)*, Grover e' **unitaria**, il trasporto e' **unitario** *(`U ∈ U(2)`, e `U_jk = U_kj^†` rende lo spostamento una **permutazione unitaria**)*, le fasi non cambiano i moduli. ### ⛔ **L'ENERGIA: non lo so**, ed e' la lettura `3`. ### 📌 **E LA CARICA `U(1)` ADESSO ESISTE**: e' la grandezza che `C` inverte |
| `2` | **a quale dei TRE GRADINI arriva?** | **(a) robusto al rumore: SI'** *(bracci al bit, `4` semi)*. **(c) coincide con un limite noto: SI', in due punti** — la **gauge-invarianza** e' un teorema che la misura deve ritrovare, e con `eps = 0` **e** identita' il `v2` **ricade nel `v1`**. ### ⛔ **(b) regge togliendo la legge pratica: NO** — la legge pratica **e' l'oggetto in prova** |
| `3` | **aggiunge un numero o una legge?** | ### ⛔ **NESSUNA LEGGE in `leggi.yaml`** *(un braccio lo verifica)*. ### **I numeri sono SONDE: `eps`, `g`, `r_k`, piu' i versori e le `U`** — e ### **tutti e cinque sono DICHIARATI PROVVISORI**, con la loro domanda aperta. ### ✅ **Nessun clip, nessun pavimento** *(un braccio cerca `6` forme)* |
| `4` | **tocca `rho`, `c_s` o il SEGNO?** | ### **IL SEGNO SI', ed e' il centro:** `C` inverse la carica `U(1)` e **gira lo spin**. ### ⛔ **`c_s` NO:** `cs_k = 1` ovunque, **dichiarato** — il `v2` **non prova la `cs` locale**. ### 📌 **E IL VERSO curvatura↔EM ADESSO HA UN SENSO**, perche' `θ` **e'** l'elettromagnetismo e `V` **e'** la geometria: ma in questo banco ### **sono entrambi FISSI**, quindi il verso **non e' misurabile** — e lo dichiaro invece di lasciarlo credere |
| `5` | **emergente o imposto?** | ### ✅ **IL CONTROLLO E' `eps = 0`**, ed e' esattamente *«togliere la legge pratica»*: se lo spin si lega al moto **solo** con `eps > 0`, il legame e' **dovuto alla moneta di spin**. ### ⚠ **E il secondo controllo e' la scena IDENTITA'**: se un effetto c'e' **anche la'**, non e' della geometria |

---

## `4` TODO DEL NEXT STEP

| | che cosa | dove |
|---|---|---|
| `1` | versori di Fibonacci, le tre scene di `U`, le olonomie, la trasformazione di gauge | `proto_camminata/geometria.py` |
| `2` | il passo `v2`, `C = iσ_y K`, lo spettro | `proto_camminata/camminata2.py` |
| `3` | `(A)` e `(B)` con l'**elicita'** | `proto_camminata/nonlineare2.py` |
| `4` | il collaudo: braccio `0` nelle tre scene, `G` e `G!`, determinismo, niente simulatore, niente clip | `proto_camminata/_collauda_banco2.py` |
| `5` | le nove letture | `proto_camminata/_letture2.py` |
| `6` | il referto generato | `proto_camminata/_referto2.py` → `doc/REFERTO_prototipo_camminata_v2.md` |
| `7` | le proposte per Luca **come voci** | `csv/indice.py crea-lotto` |

### ⛔ **E TRE COSE CHE NON FARO', scritte perche' non diventino una sorpresa:** non tocchero'
**`leggi.yaml`**; non derivero' `r_k`, `eps`, `g`, i versori ne' le `U` — ### **sono tutte
sonde o decisioni di Luca**; e non fara' nascere **nessun arco** *(punto `2d`)*.
