# IL PROTOTIPO `v3` — **IL VUOTO LOCALE DETERMINISTICO E LA NON LINEARITA' SATURANTE**

> ### ⛔ **SCRITTO E COMMITTATO *PRIMA* DEL CODICE** *(par. `8`)*: il commit di questo
> documento e' **antenato** dei commit del banco `v3`.

**Il mandato:** Luca, `2026-10-11`. **Il punto `0`** *(l'analisi del guardiano sulla lettura
`M`, rifatta con due metodi)* e' nel commit `bb44687`. ### ⭐ **E LA LETTURA `(S)` — la
velocita' delle eccitazioni rispetto al cono — e' ARRIVATA DOPO**, mentre lavoravo al punto
`0`: **entra qui dentro e non come annotazione**, perche' questo documento **non era ancora
committato** — e il mandato dell'aggiunta lo dice.

> ## ⛔ **LA REGOLA DI FONDO, e governa tutto il resto: LA FISICA DEL `v2` NON SI INVALIDA.**
> Ogni pezzo nuovo passa **gli stessi collaudi** del `v2` *(gauge, isotropia, cono, `C`)*, e
> ### **con la non linearita' spenta il `v3` COINCIDE AL BIT col `v2`** — ed e' la lettura
> `(R)`, la prima che si misura.

---

## `1` RAGIONAMENTO PRELIMINARE — **che cosa credo, e che cosa NON SO**

### ⭐ **CIO' CHE SO PER CONTO FATTO, cioe' che mi aspetto di VERIFICARE e non di scoprire**

La non linearita' del mandato e' **hamiltoniana**, e il flusso e' **in forma chiusa**. Il conto
e' corto e lo scrivo per intero, perche' **se e' giusto non c'e' niente da tarare**:

| | il conto | l'esito |
|---|---|---|
| `a` | `N = Λ G(x)`, `x = h/Λ`, `G(x) = x − arctan x` | `G'(x) = x²/(1+x²)`: ### **PARI e LIMITATA in `[0,1)`** — e' **la saturazione** |
| `b` | `∂N/∂h` | `= Λ G'(x)·(1/Λ) =` ### **`G'(x)`** |
| `c` | `∂N/∂Λ` | `= G(x) − x G'(x) =` ### **`x/(1+x²) − arctan x`**, che e' ### **DISPARI** |
| `d` | il flusso sullo spinore | `i dψ/dt = ∂N/∂ψ* = G'(x)(σ·n)ψ` ⟹ ### **rotazione attorno a `n` di `G'(x)·dτ`** |
| `e` | il flusso sul vuoto | `i dφ/dt = ∂N/∂φ* = b·φ` ⟹ ### **fase `exp(-i b dτ)`** |
| `f` | ### ⭐ **E I DUE INVARIANTI** | una rotazione **attorno a `n`** lascia `s·n` **invariante** ⟹ **`h` costante**; una fase lascia `|φ|²` ⟹ **`Λ` costante** |

### ⛔ **DA `(f)` SEGUE TUTTO:** se `h` e `Λ` **non cambiano durante il flusso**, allora `x`,
`G'(x)` e `b` **sono COSTANTI** ⟹ ### **il flusso si integra ESATTAMENTE**, ed e' **unitario**
*(una rotazione e una fase)* e **reversibile** *(`dτ → −dτ`)*. ### ✅ **Nessun integratore,
nessun passo, nessun errore di troncamento.**

### 📌 **IL LIMITE `Λ → 0`, e si gestisce col LIMITE, non con un pavimento** *(`A11`)*:
`x → ±∞` da' `G' → 1` e `b → −(π/2)·sign(h)`, quindi `N → h − (π/2)Λ·sign(h)`. ### ⚠ **Tutto
finito.** ### ✅ **Nel codice: `Λ == 0.0` ESATTO usa la forma limite**, e per `Λ > 0` la
formula e' esatta — ### **nessun epsilon, nessun clip.**

### ⭐ **E LA `C` ESTESA COMMUTA, per lo stesso motivo in due pezzi:** `C: ψ → iσ_y ψ*`,
`φ → φ*` manda `h → −h` e `Λ → Λ`, quindi `x → −x`; ### **`G'` e' PARI** ⟹ l'angolo della
rotazione **non cambia** e la rotazione *(che sta in `SU(2)`)* **commuta**; ### **`b` e'
DISPARI** ⟹ `b → −b` ⟹ la fase del vuoto **commuta** *(una fase scalare commuta con `C` se e
solo se e' dispari — e' il conto del `v2`)*.

### ⚠ **CHE COSA NON SO — scritto adesso**

| | non so | e come lo sapro' |
|---|---|---|
| `1` | **se ci sia autointrappolamento**, e a quale `x₀` | lettura `(T)`. ### **La saturazione lo rende POSSIBILE, non NECESSARIO** |
| `2` | **se il grumo stia FERMO** o si trascini | lettura `(F)`: la distanza del nodo di massima ampiezza |
| `3` | **se la frequenza del grumo cada in un BUCO** delle bande lineari | lettura `(F)`. ### **Se cade dentro, si mescola col continuo e non e' un modo legato** |
| `4` | **se esista un'energia conservata** adesso | lettura `(3)`. ### **Il `v1` e il `v2` dicono NO per le non linearita' NON hamiltoniane**; questa **lo e'**, quindi ### **e' la prima volta che la domanda ha una speranza** |
| `5` | **quanto il vuoto RISPONDE** | lettura `(Λ)`: si **legge**, e **non si interpreta oltre** |
| `6` | **se gli stati intrappolati sui cicli tornino** per qualche olonomia | lettura `(C)`: li distrugge `eps`, ma **non so se qualche connessione li rimetta** |
| `7` | ### ⛔ **a che frazione del cono si muovono le eccitazioni** | lettura `(S)`. ### **So che il cono e' `1` per costruzione**; ### **non so quanto ci si avvicini**, ne' se esista un `eps` che ci porta vicino |

---

## `2` PROGETTAZIONE — **le forme, le soglie, e cosa mi FERMA**

### **IL VUOTO, forma PROVVISORIA dichiarata** *(`VUOTO-LOCALE-DETERMINISTICO`)*

| | che cosa | perche' |
|---|---|---|
| `a` | un'ampiezza **SCALARE complessa `φ_h`** per **estremita' d'arco** | **neutra**: niente spin, niente `U(1)` |
| `b` | **Grover la mescola** sulle estremita' del nodo, come lo spinore | e' la stessa moneta: **non una legge in piu'** |
| `c` | lo **spostamento la porta SENZA la matrice `U`** | e' **neutra** ⟹ ### **invariante di gauge per COSTRUZIONE** |
| `d` | `Λ_k = Σ_{estremita' di k} \|φ_h\|²` | la **densita' del vuoto** del nodo |
| `e` | la localita' caratteristica e' ### **IL CONO** | **nessun raggio scelto**: un arco per tick |
| `f` | condizione iniziale: `\|φ_h\|² = λ₀` **uniforme**, **fasi dal seme** | `Λ_k > 0` **ovunque**, e il caso **solo** nelle condizioni iniziali |
| `g` | ### ⛔ **`φ` NON si mescola con `ψ`** | mescolarle **romperebbe il gauge**: si scambiano **ENERGIA**, non ampiezza |

### ⚠ **E LA STATISTICA DEI VICINI RESTA SOLO COME BRACCIO DI CONFRONTO** *(`Λ_k` = media di
`ρ` sui vicini, l'`u_nodo` dell'era `1`)*, **dichiarando che richiede di leggere i vicini
dentro la moneta** — cioe' **una cosa che la camminata non fa.**

### **LA NON LINEARITA', e NON HA `g`**

`N_k = Λ_k·G(h_k/Λ_k)`, `G(x) = x − arctan x`. ### ⭐ **Conta SOLO il rapporto `h/Λ`**, e
### **`eps`** *(spin-direzione)* resta, **scansionato**.

| | il controllo | che cosa deve fare |
|---|---|---|
| `i` | la **stessa saturazione su `ρ`** invece che su `h` | ### ⛔ **`ρ` e' PARI sotto `C`** ⟹ **DEVE rompere `C`** |
| `ii` | la fase **NON hamiltoniana** `exp(-i g h)` del `v2` | ### ⛔ **DEVE far DERIVARE** l'energia *(lettura `3`)* |

### **IL PASSO: composizione SIMMETRICA (Strang)**

```
N(dtau/2)  ->  passo lineare del v2 (vuoto mescolato da Grover e spostato)  ->  N(dtau/2)
```

### ⚠ **`dτ_k = r_k dt` dappertutto**, e nel banco **`r = 1`** — cosi' la lettura `(R)` puo'
essere **al bit**.

### **LE SOGLIE, FISSATE ADESSO — e ognuna DERIVATA**

| | la soglia | la forma |
|---|---|---|
| `S1` | gauge, isotropia, `C` | `T · g_max · ε · ‖ψ‖` *(conteggio di operazioni)* |
| `S2` | cono, e la **regressione `(R)`** | ### **`0.0` AL BIT** |
| `S3` | norme di `ψ` e di `φ` | `passi · n_est · ε` |
| `S4` | pendenza nulla | `\|pendenza\| ≤ 3σ_pendenza` |
| `S5` | reversibilita' `(V)` | `2k · n_est · ε` — **andata e ritorno, `2k` passi** |
| `S7` | risoluzione di una serie | `passi · n_est · ε · scala`, ### **PRIMA della statistica** |
| `S8` | **intrappolamento** | il ### **fondo UNIFORME** del grafo: la frazione di nodi entro `R` archi. ### **Non e' una soglia scelta: e' il valore che un'ampiezza SPARSA darebbe** |

### **LE LETTURE, con PREVISIONE e CRITERIO** *(fissati qui, prima dei numeri)*

| | la lettura | la previsione | il criterio |
|---|---|---|---|
| **`R`** | **REGRESSIONE** | con `N` spento e il vuoto presente, `ψ` evolve **come nel `v2`** | ### **`0.0` AL BIT** *(`S2`)*. ### ⛔ **Se non e' al bit, il `v3` ha INVALIDATO il `v2`: STOP** |
| **`G`** | **GAUGE** | invariante anche col vuoto e `N` accesi | `≤ S1` |
| **`1`** | **ISOTROPIA** | invariante | `≤ S1` |
| **`2`** | **CONO** | zero oltre un arco per tick | ### **`0.0` AL BIT** |
| **`5`** | **`C`** | coniugati evolvono coniugati; il controllo su `ρ` **DEVE rompere** | `≤ S1`, e il controllo `> 1e-6` |
| **`V`** | **REVERSIBILITA'** | `k` avanti e `k` indietro **tornano** | `≤ S5` |
| **`3`** | **QUANTITA' CONSERVATE** | le **norme** esatte; l'**energia modificata** *(quasi-energia lineare `+ Σ N_k`)* ### **non lo so** | i **tre esiti** *(conservata / oscillante limitata / deriva)*, con `S7` **prima** della statistica; il controllo non hamiltoniano **deve DERIVARE** |
| **`T`** | **AUTOINTRAPPOLAMENTO** | sotto `x₀ ~ 1` **si disperde come il lineare**; sopra, ### **un SALTO**; e ### **NESSUN collasso** su un nodo | la frazione entro `R ∈ {1,2,3}` archi dopo `T = 40` tick, **contro il fondo uniforme `S8`**; e la frazione massima **su un singolo nodo** resta **limitata** |
| **`F`** | **LA MASSA DEL GRUMO** | se c'e' intrappolamento, la frequenza interna cade **in un BUCO** delle bande | la fase nel tempo, e la distanza dallo spettro lineare; e il **nodo di massima ampiezza** resta entro `R` archi |
| **`A`** | **MATERIA/ANTIMATERIA nell'intrappolamento** | il grumo con `h>0` e il suo coniugato **si intrappolano uguale** | la differenza delle frazioni `≤ S1` |
| **`Λ`** | **IL VUOTO RISPONDE** | **non lo so** | si **legge** `Λ` attorno al grumo nel tempo, e l'energia che passa fra `N` e il resto. ### ⛔ **Non si interpreta oltre** |
| **`C`** | **RISONANZA DEI CICLI** *(controllo lineare)* | **non lo so** | si scansiona l'**olonomia di un ciclo** e si contano gli stati a `±1` e la **partecipazione** |
| **`S`** | ### ⭐ **LA VELOCITA' RISPETTO AL CONO** | esiste un **`eps*`** che porta il fronte **piu' vicino al cono**, e/o rende la propagazione **isotropa** | la **pendenza** di `distanza(t)` nel tratto lineare, in **archi per tick**, col suo `σ`; e <<isotropa>> = le velocita' da **nodi e direzioni diversi** coincidono entro **`3σ`** |

### ⭐ **LA LETTURA `(S)`, in dettaglio, perche' e' arrivata dopo e non deve restare vaga**

**La precisazione di Luca:** ### **la velocita' della luce del sistema E' IL CONO**, un arco
per tick, ed e' fissata dallo **SPOSTAMENTO**; ### **`eps` NON la fissa** — decide **quanto
vicino al cono** si muovono le eccitazioni, perche' **la moneta rimescola le direzioni** e un
pacchetto avanza a una **frazione** del massimo.

| | che cosa si misura | come |
|---|---|---|
| `a` | la **distanza sul grafo** dal nodo di partenza nel tempo | **media pesata** dall'ampiezza, e il **FRONTE** *(il raggio entro cui sta il `95%` dell'ampiezza)* |
| `b` | la **velocita'** | la **pendenza** nel tratto lineare, in **archi per tick** |
| `c` | su quale scena | **identita'** e **curva**, piu' ### **il grafo REGOLARE come controllo** |
| `d` | ### ⚠ **e il tratto lineare dove c'e' spazio** | sull'irregolare l'eccentricita' e' **`6`**, quindi il fronte **satura in `6` tick**: ### **la scena principale della `(S)` e' il REGOLARE** *(eccentricita' `30`)*, e l'irregolare e' un confronto corto |
| `e` | l'**isotropia della propagazione** | sul regolare, **da nodi diversi** e **nelle direzioni diverse** del reticolo |

### ⛔ **E SE LA VELOCITA' NON DIPENDE DA `eps`, O NESSUN `eps` LA AVVICINA AL CONO, SI
SCRIVE: E' UN RISULTATO.** ### ⭐ **Se invece un `eps*` esiste, e' il candidato per DERIVARE
`eps`** *(`A1`)*: ### **<<la luce viaggia al limite causale>>** — e diventa **una proposta per
Luca**, non una decisione mia.

### **I PASSI, e cosa mi FERMA**

| | il passo | che cosa decide | che cosa mi FERMA |
|---|---|---|---|
| `0` | il vuoto, e la **lettura `(R)`** | se il `v3` **non ha invalidato il `v2`** | ### ⛔ **se `(R)` non e' al bit: STOP** |
| `1` | il flusso di `N`, e **le sue derivate verificate** | se il flusso e' **quello che ho derivato** | se `h` o `Λ` **cambiano durante il flusso**, la forma chiusa **non esiste**: STOP |
| `2` | `C` estesa, e il controllo su `ρ` | se la lettura `5` **si puo' formulare** | se il controllo su `ρ` **non rompe** `C`, non ho capito la simmetria: STOP |
| `3` | `(G)`, `(1)`, `(2)`, `(V)` | se l'implementazione e' **quella che credo** | un rosso qui e' **un difetto mio** |
| `4` | `(3)`, `(T)`, `(F)`, `(A)`, `(Λ)` | **se la saturazione serve** | — |
| `5` | `(C)` e `(S)` | la **risonanza** e la **velocita'** | — |
| `6` | il referto | che cosa **sblocca** o **riapre** | — |

---

## `3` LA STELLA POLARE — **le cinque risposte** *(`[[L-STELLA]]`)*

| | la domanda | la risposta per il `v3` |
|--:|---|---|
| `1` | **`A14`: conserva energia e carica LOCALMENTE?** | ### ✅ **LE NORME SI', e per costruzione:** il flusso di `N` e' **una rotazione** sullo spinore e **una fase** sul vuoto; il passo lineare e' unitario. ### ⭐ **E L'ENERGIA ADESSO HA UNA CANDIDATA VERA**, perche' `N` e' **hamiltoniana**: e' la lettura `(3)`, e ### **nel `v1` e nel `v2` non c'era nemmeno la candidata** |
| `2` | **a quale dei TRE GRADINI arriva?** | **(a) robusto: SI'** *(al bit, `4` semi)*. **(c) coincide con un limite noto: SI', e tre volte** — `(R)` ricade **al bit** nel `v2`, `(V)` e' la **reversibilita'**, e `G'→1` per `Λ→0` e' **il limite analitico**. ### ⛔ **(b) regge togliendo la legge pratica: SI', ED E' LA LETTURA `(T)`** — con `N` spento il grumo **si disperde**, e questa volta il confronto **esiste** |
| `3` | **aggiunge un numero o una legge?** | ### ⭐ **TOGLIE un numero: `g` NON C'E' PIU'.** Conta solo `h/Λ`, che e' **un rapporto fra due grandezze locali**. ### **Restano `eps`** *(scansionato, e la `(S)` cerca di DERIVARLO)* e **`λ₀`** *(il fondo del vuoto, scansionato via `x₀`)*. ### ✅ **Nessun clip, nessun pavimento: il limite `Λ→0` e' ANALITICO** |
| `4` | **tocca `rho`, `c_s` o il SEGNO?** | ### **IL SEGNO SI'** *(`C` e l'elicita')*. ### ⛔ **`c_s` NO:** `cs_k = 1`, dichiarato. ### 📌 **E il VERSO curvatura↔EM resta non misurabile**, perche' `θ` e `V` sono **ancora fissi** |
| `5` | **emergente o imposto?** | ### ✅ **DUE controlli, e sono entrambi <<spegnere la legge>>:** `N` spento *(lettura `R` e `T`)* e **`x₀` piccolo** *(sotto la saturazione)*. ### ⚠ **Se il grumo si intrappolasse anche con `N` spento, sarebbe della CONDIZIONE INIZIALE** |

---

## `4` TODO DEL NEXT STEP

| | che cosa | dove |
|---|---|---|
| `1` | il vuoto `φ`, `Λ_k`, e il braccio di confronto sui vicini | `proto_camminata/vuoto3.py` |
| `2` | `G`, `G'`, `b`, il flusso esatto, il limite `Λ→0` | `proto_camminata/saturazione3.py` |
| `3` | il passo Strang, `C` estesa, il passo INVERSO | `proto_camminata/camminata3.py` |
| `4` | il collaudo: `(R)` al bit, le derivate, gli invarianti, `C`, i due controlli | `proto_camminata/_collauda_banco3.py` |
| `5` | le dodici letture | `proto_camminata/_letture3.py` |
| `6` | il referto generato | `proto_camminata/_referto3.py` |
| `7` | le proposte per Luca **come voci** | `csv/indice.py crea-lotto` |

### ⛔ **E QUATTRO COSE CHE NON FARO':** non tocchero' **`leggi.yaml`**; non derivero' `eps`
*(la `(S)` dice **se si puo'**, e la decisione e' di Luca)*; non rendero' **dinamiche le `U`**
*(e' `D13`)*; e non **mescolero' `φ` con `ψ`** — ### **romperebbe il gauge, ed e' scritto nel
mandato.**
