# IL `v4` — **`cs` LOCALE DAL VUOTO, IN TUTTE LE LEGGI** *(mandato di Luca, `2026-10-11`, terza versione)*

> ### ⛔ **QUESTO FILE SI COMMITTA E SI PUSHA *PRIMA* DEL CODICE** *(par. `8`)*, cosi' l'ordine
> e' **verificabile da git** invece che asserito da me. ### **E non si riscrive quando una
> previsione si rivela sbagliata: si ANNOTA.**

### ✅ **IL CONTROLLO DI IDEMPOTENZA, FATTO PER PRIMO**

| | che cosa ho cercato | c'era? |
|---|---|---|
| `a` | `doc/TASK_HISTORY/*_camminata_v4_cs_locale.md` | ### **NO** |
| `b` | file del banco `v4` sotto `proto_camminata/` | ### **NESSUNO** |
| `c` | `doc/REFERTO_prototipo_camminata_v4.md` | ### **NO** |
| `d` | le voci che il mandato cita | `INVARIANZA-LOCALE-CS` *(`FRONTE`/`2`/`AGENDA`)*, `DOMANDA-LAMBDA-GRANDEZZA` *(`DECISIONE`)*, `CS-LOCALE-DAL-VUOTO` *(`DECISIONE`)* — ### **tutte e tre CI SONO** |

### ✅ **E LA CONDIZIONE D'INGRESSO E' VERIFICATA:** `v3` concluso *(referto committato, `25886ea`)*
**e** voce ⑮ conclusa *(`9184913` + `7fa74f5`, verifica su clone pulito verde)*. ### **E va
PRIMA della voce ⑭**, che non e' partita.

---

## 1. RAGIONAMENTO PRELIMINARE — **cosa credo PRIMA di guardare, e cosa NON SO**

### **COSA CREDO** *(e ognuna di queste puo' cadere)*

| | quello che credo | perche' |
|---|---|---|
| `c1` | il pezzo **facile** e' quello delle rotazioni: moneta di spin, `N`, `(D)`, e la scrittura sul vuoto prendono `cs_k` ### **semplicemente come `dtau_k = cs_k dt`** | nel `v3` `dtau` e' **gia'** un array per nodo *(`r * dt`)*, e i tre pezzi lo usano gia' |
| `c2` | il pezzo **duro** sono i due pezzi **DISCRETI**: Grover e lo spostamento. ### **Non hanno un tempo dentro**: sono involuzioni, e un'involuzione non si rallenta, ### **si frazione** | il mandato lo dice e da' la forma, e `A4` dice che il prezzo esiste |
| `c3` | ### **La `C` sara' il problema, non l'unitarieta'** | una frazione di un'involuzione passa per **fasi complesse**, e una fase scalare commuta con `C` ### **solo se e' `C`-DISPARI** — ma `cs` deve essere `C`-PARI *(`W5`)*, e queste due cose ### **tirano in direzioni opposte** |
| `c4` | ### **`Lambda` si muove solo nello spostamento** | Grover e' **a blocchi per nodo**, quindi unitario **dentro** il nodo, quindi conserva `Lambda_k` ### **per teorema, non per caso** |
| `c5` | ### **`L1`, `L2` e `L5` erediteranno il limite di `G1`:** il mandato dice *«partendo da un grumo `v3` auto-intrappolato»*, e il ### **`v3` non ne ha trovato nessuno** | misurato nel referto `v3` e ripetuto in `G1`: il rapporto col fondo uniforme resta quello del lineare a ogni ampiezza provata |
| `c6` | ### **`(S)` sara' piu' pulita di `(F)` sull'invarianza locale e piu' sporca su tutto il resto** | `(S)` esegue **tick interi di `v3`**, quindi dentro un nodo la fisica e' **esattamente** quella del `v3`; il prezzo si sposta tutto sugli **archi fra ritmi diversi** |

### ⛔ **COSA NON SO, e lo scrivo perche' e' la parte che conta**

| | la cosa che non so | come la decidero' |
|---|---|---|
| `n1` | se esista una forma di `A1` *(la materia cambia `Lambda`)* che sia ### **locale, unitaria, `C`-pari e senza costanti nuove** tutte insieme | derivandole, non provandole: ogni candidata contro `W1`..`W9`, **una tabella** |
| `n2` | se `cs_k` possa venire da una grandezza ### **relazionale** senza una scala globale. ### **`Lambda_k` NON e' adimensionale**, e il fondo uniforme da' `Lambda_k = grado_k * lambda_0` — quindi ### **`Lambda_k` da sola porta dentro il GRADO**, che e' geometria, non vuoto | serve un **rapporto**: candidate in `A2`, e ciascuna dichiara **cosa fa da riferimento** |
| `n3` | se la rottura di `C` delle frazioni sia ### **un difetto curabile** o ### **una proprieta' della camminata discreta** | il conto del determinante, qui sotto — ed e' **gia' fatto** |
| `n4` | se `(S)` si chiuda in modo **unitario** sugli archi | si deriva; e il mandato dice: ### **«se non si chiude in modo unitario, SCRIVILO»** |
| `n5` | se la gravita' si veda **affatto** a queste taglie | `L5` contro `G2`, con la soglia fissata **prima** |

---

## 2. L'ALGEBRA, VERIFICATA **PRIMA** DI SCRIVERE LA DERIVAZIONE

> ### ⛔ **Un regalo non verificato e' un debito**, e il mandato me ne fa due. ### **Qui ci
> sono i numeri**, misurati sul codice `v3` che gira — non su come me lo ricordo.

### ⭐ **` 2.1 ` TUTTI E QUATTRO I PEZZI DISCRETI SONO INVOLUZIONI *ERMITIANE* — e questo rende la frazione UNICA**

| il pezzo | `max\|M^2 - I\|` | ermitiana? |
|---|---|---|
| Grover scalare *(il vuoto)* | **`0`** | **`0`** |
| spostamento scalare *(il vuoto)* | **`0`** | **`0`** |
| Grover dello spinore | **`2.22e-16`** | **`0`** |
| spostamento con trasporto, scena **identita'** | **`0`** | **`0`** |
| spostamento con trasporto, scena **CURVA** | **`5.55e-16`** | **`0`** |

### ⭐ **E QUESTA E' LA PRIMA COSA CHE CAMBIA IL PIANO:** il mandato chiede una forma frazionaria
**per Grover** e un'altra **per lo spostamento**. ### **Non servono due forme.** Un'involuzione
ermitiana `X` si scrive `X = 2Q - I` con `Q = (I+X)/2` proiettore, e allora ### **UNA SOLA
famiglia** copre tutti e quattro i pezzi. ### ✅ **E' `9-ter` applicato prima di scrivere il
codice: una legge invece di due.**

### **` 2.2 ` LE DUE FAMIGLIE, E ENTRAMBE FUNZIONANO**

| | la forma | `\|X(0) - I\|` | `\|X(1) - X\|` | unitaria *(peggiore su `cs = 0.17/0.5/0.83`)* |
|---|---|---|---|---|
| `(A)` | **del mandato**: `X(cs) = e^{i pi cs} e^{i pi cs Q}` | ### **`0` ESATTO** | `1.84e-16` .. `2e-16` | `2.2e-16` .. `5.6e-16` |
| `(B)` | **senza fase globale**: `X(cs) = Q + e^{i pi cs}(I - Q)` | ### **`0` ESATTO** | `6.1e-17` .. `1.6e-16` | `6.2e-17` .. `5.6e-16` |

### ✅ **E il regalo del mandato e' confermato alla lettera:** `P^2 = P` a **`2.78e-17`**, e
`max|G + e^{i pi P}|` = **`6.12e-17`** — ### **per il Grover scalare E per quello dello spinore,
lo stesso numero.**

### ⛔ **` 2.3 ` E ADESSO LA COSA CHE CAMBIA TUTTO: *OGNI* FRAZIONE ROMPE LA `C`**

| il pezzo | `\|C X - X C\|` a `cs = 1` *(cioe' il `v3`)* | `(A)` a `cs = 0.25 / 0.5 / 0.75` | `(B)` a `cs = 0.25 / 0.5 / 0.75` |
|---|---|---|---|
| Grover scalare | ### ✅ **`0`** | `0.230` / `0.252` / `0.218` | `0.178` / `0.252` / `0.178` |
| spostamento scalare | ### ✅ **`0`** | `0.261` / `0.192` / `0.261` | `0.135` / `0.192` / `0.135` |
| Grover dello spinore | ### ✅ **`0`** | `0.178` / `0.183` / `0.198` | `0.129` / `0.183` / `0.129` |
| spostamento, scena **CURVA** | ### ⚠ **`0.183`** *(e questo e' **GIA' COSI' NEL `v3`**: e' la fase `U(1)`, che manda la camminata nell'ANTI-camminata — misurato nel `v2`)* | `0.186` / `0.199` / `0.162` | `0.104` / `0.165` / `0.191` |

### ⛔ **QUINDI: i tre pezzi che nel `v3` commutano con `C` AL BIT, frazionati NON commutano piu'.**
### ⚠ **E non e' un errore di implementazione: e' il conto.** `C` e' **antiunitaria**, quindi
`C e^{i t} = e^{-i t} C`: una fase scalare commuta con `C` ### **solo se `t` e' `C`-DISPARI** — e
`t = pi cs` con `cs` ### **`C`-PARI per `W5`**. ### **Le due richieste sono incompatibili per
costruzione.**

### ⭐ **E `(B)` ROMPE MENO DI `(A)`, e in modo SIMMETRICO in `cs`** *(`0.178 / 0.252 / 0.178`
contro `0.230 / 0.252 / 0.218`)*: ### **non e' un dettaglio estetico** — `(B)` non ha la fase
globale, e ### **a `cs = 0.5` le due coincidono** perche' la' differiscono per `e^{-i pi/2}`, che
su `C` pesa quanto l'altra.

### ⭐ **` 2.4 ` LA TERZA CANDIDATA, CHE IL DETERMINANTE APRE — E CHE LA *LOCALITA'* CHIUDE**

Se la rottura viene dalle **fasi complesse**, allora un cammino **REALE** da `I` a `X` darebbe
`C` ### **esatta**, perche' una matrice reale commuta con la coniugazione. ### **E un cammino
reale esiste, se e solo se il determinante non lo vieta.** Misurato: `det(X) = +1` per tutti e
quattro i pezzi, e sulla matrice intera **la `(R)` funziona**: ortogonale a `2e-15`, reale a `0`,
`I` a `cs = 0`, `X` a `cs = 1` *(`1.11e-15`)*, e ### **`|C M - M C| = 0` ESATTO.**

### ⛔ **MA LA `(R)` *GLOBALE* NON E' UNA LEGGE: VIOLA `W3`.** Gli autovettori del `-1` che
`eigh` mi restituisce toccano **`30, 96, 85, 97, 115, 120, 37, 101, 117, 7, 25, 48` nodi** — cioe'
### **mezzo grafo**. ### ⚠ **E questa prima lettura era MIA E SBAGLIATA**, perche' Grover e' a
blocchi per nodo: una base ### **locale** del `-1` esiste, e `eigh` me l'aveva solo delocalizzata.
### ⭐ **La domanda vera e' se il BLOCCO di un nodo ammetta un cammino reale**, e la risposta e'
### **un teorema esatto:**

| grado `d` | nodi | `dim` del `-1` | `det(G_k)` | cammino **reale** nel blocco? |
|---|---|---|---|---|
| `2` | `31` | `1` | **`-1`** | ### ⛔ **NO** |
| `3` | `38` | `2` | `+1` | ### ✅ **SI** |
| `4` | `26` | `3` | **`-1`** | ### ⛔ **NO** |
| `5` | `14` | `4` | `+1` | ### ✅ **SI** |
| `6` | `11` | `5` | **`-1`** | ### ⛔ **NO** |

### ⛔ **`det(G_k) = (-1)^(d-1)` ESATTAMENTE**, perche' il `+1` ha molteplicita' `1` e il `-1` ne
ha `d-1`. ### **Un cammino reale continuo non cambia il determinante**, quindi: ### **la `(R)`
LOCALE e' IMPOSSIBILE su ogni nodo di grado PARI** — ### **`68` dei `120`, il `57%` di questa
scena.**

### ⛔ **E PER LO SPOSTAMENTO E' PEGGIO:** il blocco e' `2x2` **su ogni arco**, e `det = -1`
### **sempre** ⟹ ### **la `(R)` locale non esiste su NESSUN arco.** ### ⭐ **Una via c'e', e la
dichiaro senza scegliere:** accoppiando le **due componenti di spin** il blocco diventa `4x4` con
`det = +1` e il cammino reale esiste *(misurato)* — ### ⛔ **ma mescolerebbe le componenti in un
pezzo che nel `v3` non le mescola per conto suo**, cioe' sarebbe ### **una legge nuova sullo
spin, non una frazione del tempo.**

> ## ⛔ **IL RISULTATO STRUTTURALE, E VA NEL REFERTO ANCHE SE NESSUNA LETTURA GIRASSE:**
> ## ### **`C` ESATTA *oppure* LOCALITA'. ### Non entrambe**, in questa famiglia di costruzioni.
> ## ### ⭐ **E non e' un'opinione: e' `det(G_k) = (-1)^(d-1)`.**

### ⚠ **` 2.5 ` E `A4` E' ANCORA PIU' SECCO DI COME IL MANDATO LO SCRIVE**

Il mandato dice `sqrt(G) sqrt(S) != sqrt(G S)`. ### **Misurato, il fatto e' piu' forte:** il
prodotto `spostamento * Grover` ### **NON E' UN'INVOLUZIONE** *(`max|M^2 - I| = 1`, non `~1e-16`)*
⟹ ### **«la frazione del tick intero» NON ESISTE** in questa famiglia: non c'e' niente da
confrontare. ### ⛔ **Quindi in una zona a `cs` uniforme `< 1` la camminata `(F)` non e' «una
copia rallentata con un errore piccolo»: e' una dinamica DIVERSA**, e `L0` ne misura la distanza.

### ✅ **` 2.6 ` E IL VUOTO: `Lambda` SI MUOVE SOLO NELLO SPOSTAMENTO — con un FALSO-ZERO MIO in mezzo**

| | Grover scalare | spostamento scalare |
|---|---|---|
| vuoto di modulo **UNIFORME** *(il mio primo giro)* | `max\|dLambda\| = 2.66e-15` | ### ⛔ **`8.88e-16`** |
| vuoto **NON uniforme** | `7.11e-15` ### **(teorema)** | ### ⭐ **`56.5`** |

### ⛔ **IL PRIMO GIRO ERA UN FALSO-ZERO, E GARANTITO DALL'INSIEME CHE AVEVO SCELTO:** il fondo
del `v3` ha ### **modulo uniforme**, e lo spostamento ### **scambia estremita' di modulo
uguale** ⟹ `Lambda` ### **non PUO' cambiare**, qualunque sia la legge. ### ⚠ **Avrei concluso
«lo spostamento non muove `Lambda`», che e' il contrario del vero.** ### ✅ **E la nota di
partenza del mandato e' confermata nella sua forma forte:** `Lambda_k` e' conservata da Grover
### **per teorema** *(Grover e' a blocchi per nodo ⟹ unitario DENTRO il nodo)*, e la densita'
del vuoto ### **si sposta fra i nodi SOLO nello spostamento.**

---

## 3. PROGETTAZIONE DEL RAGIONAMENTO — **i passi, cosa decide ciascuno, e cosa mi FERMA**

### `A1` **COME LA MATERIA CAMBIA `Lambda`** — tre candidate, e nessuna e' mia da scegliere

| | la candidata | la forma | `W1`..`W9` |
|---|---|---|---|
| `A1-scatter` | la materia cambia lo **SCATTERING del vuoto nel nodo**: la moneta del vuoto va da Grover verso la **riflessione** in funzione di `x_k = rho_k / Lambda_k` | ### **la STESSA famiglia frazionaria del `2.2`**, con `cs` sostituito da un `s_k` che dipende da `x_k`: `Grover_vuoto(s_k)` | ### ⭐ **`W2` OK** *(`x_k` e' un RAPPORTO, nessuna costante)* · ### **`W3` OK** · **`W4` OK** *(unitaria per costruzione)* · ### ⛔ **`W5`: `x_k` e' `C`-PARI** *(`rho` e `Lambda` lo sono)* ### **ma la famiglia frazionaria rompe `C` — il difetto del `2.3`, ereditato** |
| `A1-trasmissione` | la materia cambia la **frazione TRASMESSA del vuoto sull'arco**: lo spostamento del vuoto diventa parziale, con frazione da `x` dell'arco | la stessa famiglia, sullo **spostamento scalare** | ### ⭐ **E' il pezzo che DAVVERO muove `Lambda`** *(`2.6`)*, quindi e' la via piu' diretta · stessi pro e contro di sopra |
| `A1-scambio` | **scambio di NORMA fra `psi` e `phi`** *(il mandato chiede di dichiararla a parte)* | una rotazione unitaria nello spazio `(psi, phi)` del nodo | ### ⛔ **ROMPE IL GAUGE** *(`W6`)*: `psi` si trasforma con `e^{i f_k} g_k` e `phi` **no** ⟹ mescolarle somma due cose che si trasformano diversamente. ### **E' il motivo per cui `vuoto3.py` lo VIETA** *(«si scambiano ENERGIA, non ampiezza»)*. ### **La dichiaro e la escludo PER UN VINCOLO, non per gusto** |

### ⛔ **COSA MI FERMA SU `A1`:** se **nessuna** delle due prime candidate produce un `dLambda`
misurabile fuori dal grumo ⟹ ### **FERMO**, e lo scrivo: *«la materia non riesce a scrivere sul
vuoto con queste forme»*. ### **Non invento una terza forma per far uscire il risultato.**

### `A2` **COME IL VUOTO FISSA `cs_k`** — e il problema vero e' che `Lambda_k` **porta dentro il GRADO**

### ⛔ **MISURATO, E DA SCRIVERE PRIMA DI TUTTO:** col fondo uniforme `Lambda_k = grado_k *
lambda_0`, cioe' ### **`min 2.000`, `max 6.000` su gradi da `2` a `6`.** ### **Quindi `cs_k =
f(Lambda_k)` NON e' relazionale: sarebbe `cs` che dipende dal GRADO**, cioe' dalla geometria del
grafo e non dal vuoto. ### ⭐ **E questo esclude la forma piu' ovvia PRIMA di provarla.**

| | la candidata | il riferimento | il costo |
|---|---|---|---|
| `A2-grado` | `cs_k = f(Lambda_k / grado_k)` | il **grado del nodo** | ### ⛔ **il grado non e' vuoto: e' geometria.** La dichiaro e la tengo come ### **braccio di controllo** |
| `A2-contrasto` | `cs_k = f(Lambda_k / media delle estremita' del nodo)` ... che e' **identicamente `1`** | ### ⛔ **NIENTE: e' un FALSO-ZERO per costruzione**, e lo scrivo per non riproporlo | — |
| `A2-arco` | `cs` dell'**ARCO** dal **contrasto fra le sue due estremita'**: `cs_a = f(\|phi_h\|^2, \|phi_h'\|^2)` con una forma **simmetrica** dichiarata | le **due estremita' dello stesso arco**: ### **l'unica coppia che la camminata legge** | ### ⭐ **relazionale e locale per costruzione**, e da' `cs` dove serve *(lo spostamento)*. ### ⚠ **Ma per i pezzi di NODO serve un `cs_k`**, e allora si deriva dalle estremita' del nodo con la stessa forma |
| `A2-ritmo` | `cs_k = f(Lambda_k / Lambda_k(iniziale))` | lo **stato iniziale** | ### ⛔ **un riferimento al PASSATO non e' locale nel tempo**, e porta una memoria. ### **La dichiaro e la escludo** |

### ⛔ **COSA MI FERMA SU `A2`:** se ogni forma locale richiede una scala ⟹ ### **FERMO**, e la
domanda va a Luca: ### **`[[DOMANDA-LAMBDA-GRANDEZZA]]` esiste gia' ed e' esattamente questa.**

### `A3` **OGNI PEZZO CON `cs`** — la tabella `W8`, pezzo per pezzo

| il pezzo | dove vive | come prende `cs` | si riduce al `v3` a `cs = 1`? |
|---|---|---|---|
| moneta di spin | estremita' | `dtau_k = cs_k dt` nell'angolo `eps dtau` | ### ✅ **identicamente** |
| flusso `N` | nodo | `dtau_k` nei due mezzi passi di Strang | ### ✅ **identicamente** |
| interferenza `(D)` | nodo | `dtau_k` | ### ✅ **identicamente** |
| **Grover dello spinore** | nodo | ### **famiglia frazionaria** `(A)` o `(B)` con `cs_k` | ### ✅ **`1.84e-16`** *(misurato)* |
| **spostamento con trasporto** | arco | ### **famiglia frazionaria** con `cs` dell'**arco** | ### ✅ **`2e-16`** *(misurato, scena curva)* |
| **Grover del vuoto** | nodo | ### **stessa famiglia**, `cs_k` | ### ✅ **`1.84e-16`** |
| **spostamento del vuoto** | arco | ### **stessa famiglia**, `cs` dell'arco | ### ✅ **`1.84e-16`** |
| scrittura della materia sul vuoto *(`A1`)* | nodo o arco | ### **la stessa famiglia** | — *(e' nuova: a novita' spenta e' l'identita')* |
| ### ⛔ `C`, gauge | — | ### **NON prendono `cs`** | sono **simmetrie**, non dinamica |
| ### ⛔ il CONO | — | ### **NON prende `cs`** | e' un **tetto** |

### ⭐ **E `W8` SI VERIFICA SUL SORGENTE, PEZZO PER PEZZO:** un braccio che cerca ### **ogni
chiamata** dei pezzi elencati e pretende che l'argomento del tempo sia ### **la stessa
variabile** — e che ### **nessun pezzo usi `1.0` o `dt` nudo.**

### `A4` **LA COMPOSIZIONE** — `(F)` e `(S)`, e il prezzo di ciascuna **derivato**

| | `(F)` pezzi frazionari, sincroni | `(S)` tick asincroni |
|---|---|---|
| la dinamica | ### **liscia e unitaria** | ### **a scatti**, e unitaria dentro il nodo |
| l'invarianza locale | ### ⚠ **APPROSSIMATA**, e `L0` misura quanto | ### ✅ **ESATTA per costruzione** |
| `C` | ### ⛔ **ROTTA** *(`2.3`: `0.13`..`0.26`)* | ### ✅ **al bit dentro il nodo** *(e' il `v3`)*, ### ⚠ **da verificare sugli archi** |
| il problema aperto | ### **la frazione del tick non esiste** *(`2.5`)* | ### **la regola degli archi fra ritmi diversi** |
| `W7` *(il cono)* | ### ✅ per costruzione *(la frazione trasmessa `<= 1`)* | ### ⚠ **da derivare**: un nodo veloce non deve spingere due volte sullo stesso arco |
| `W4` *(inverso)* | ### ✅ la famiglia si inverte con `cs -> -cs`... ### ⚠ **da verificare** | ### ⚠ **da derivare**: l'inverso richiede di ricordare **chi ha scattato** |

### ⛔ **LA REGOLA DEGLI ARCHI DI `(S)`, E IL SOSPETTO CHE SCRIVO PRIMA DI DERIVARLA:** se il
nodo `u` scatta e il nodo `v` no, lo scambio sull'arco `uv` ### **non puo' essere unitario sul
solo lato di `u`** — uno scambio e' una rotazione **su due lati**. ### **Quindi o scatta
l'arco** *(e allora il «tick del nodo» non e' piu' del nodo)*, ### **o si accumula un debito**
*(e allora serve una memoria, che e' uno stato nuovo)*. ### ⚠ **Previsione: `(S)` NON si chiude
in modo unitario con tick per NODO**, e il mandato chiede esplicitamente di scriverlo se e' cosi'.

### `A5` **LA VELOCITA' DI GRUPPO** in una zona a `cs` uniforme `< 1`

### **La previsione del mandato, che adotto come previsione mia:** in **archi per tick** la
velocita' e' ### **`cs`**; in **archi per tempo proprio** e' ### **`1`**. ### ⚠ **E per `(F)` me
l'aspetto VIOLATA**, per il `2.5`: la frazione del tick non esiste, quindi non c'e' ragione per cui
una zona lenta sia una copia rallentata. ### **Lo scarto E' il risultato di `L0`**, non un errore.

### `A6` **I RITMI CASUALI** di `scena.ritmi` restano ### **solo come braccio di CONTROLLO**, e il
loro ruolo e' preciso: ### **mostrare che `cs` casuale NON produce l'invarianza locale**, cosi' un
`L0` verde non e' un **falso-uno** dovuto a *qualunque* campo di ritmi.

---

## 4. LE SOGLIE E LE PREVISIONI — **fissate ADESSO, prima di qualunque numero**

### ⛔ **E SI APPLICANO A `(F)` *E* A `(S)`, SEPARATAMENTE.** `n_est = 2m = 416`,
`eps = 2.22e-16`.

| | la lettura | la soglia, **derivata** | la mia previsione |
|---|---|---|---|
| `W1` | **regressione**: `cs = 1` ovunque e novita' spente | ### **`0.0` AL BIT**, `max\|psi4 - psi3\|` e `max\|phi4 - phi3\|` | ### ✅ **passa**: la famiglia da' `X(1) = X` a `2e-16`, quindi ### ⚠ **ATTENZIONE: `2e-16` NON E' `0`** ⟹ a `cs = 1` il codice deve ### **cortocircuitare sul pezzo del `v3`**, non valutare la famiglia |
| `W7` | **cono** | nessuna ampiezza oltre **un arco per tick**: `max` della distanza di grafo del supporto `<= t`, ### **esatto** | ### ✅ **passa** per `(F)`; ### ⚠ **da verificare** per `(S)` |
| `W5` | **`C` sul campo di `cs`** | `max\|cs(C psi) - cs(psi)\|` ### **`<= passi * n_est * eps`** = `~1e-13` a `passi = 40` | ### ✅ **passa**: `rho` e `Lambda` sono `C`-PARI |
| `W5-bis` | **`C` sul PASSO** | — | ### ⛔ **PREVEDO CHE FALLISCA per `(F)`** *(`2.3`)*, e il numero atteso e' ### **`0.1`..`0.3`**, non `1e-16`. ### **Lo riporto come COSTO, non come difetto** |
| `W6` | **gauge** `U(2)` sul passo intero | `<= passi * n_est * eps` | ### ✅ **passa**: `cs` viene da grandezze **gauge-invarianti** |
| `W4` | **inverso** | `max\|psi(andata+ritorno) - psi0\| <= 2 * passi * n_est * eps` | ### ✅ per `(F)`; ### ⚠ per `(S)` |
| `W9` | **norme** | `\|psi\|` e `\|phi\|` separatamente, `<= passi * n_est * eps` | ### ✅ **passano** se ogni pezzo e' unitario |
| `L0` | **invarianza locale della luce** | in **archi per tempo proprio**: ### **`\|v - 1\| <= 3 sigma`** della regressione, con `sigma` dalla pendenza. ### ⛔ **E il `sigma` SI RIPORTA SEMPRE** — e' la lezione di `G2(b)` | ### **`(S)`: `v = 1` entro `3 sigma`** · ### ⛔ **`(F)`: NON entro `3 sigma`**, e lo scarto cresce quando `cs` scende |
| `L1` | **l'impronta** | `dLambda(r)` fuori dal grumo **significativo** se `> 3 sigma` sui `4` semi; il **fronte** `<= t` archi *(esatto, `W7`)* | ### ⚠ **PREVEDO UN'IMPRONTA DEBOLE**, perche' `A1` agisce su `x = rho/Lambda` e il `v3` non ha grumi concentrati |
| `L2` | **collettivo contro passaggio** | la differenza fra impronta **stabile** e **transitoria** e' significativa se `> 3 sigma` | ### ⛔ **PREVEDO CHE NON SI DISTINGUANO**, ed e' il punto `1` della decisione di Luca: ### **se non si distinguono, `rho` di nodo non basta — e la sua tesi e' confermata nel verso che la motiva** |
| `L3` | **la luce sente la massa** | ritardo d'arrivo `> 3 sigma` contro lo **stesso lancio senza grumo**, stesso seme | ### ⚠ **debole, e forse sotto la barra**: dipende da `L1` |
| `L4` | **materia e antimateria** | `max\|Lambda(C) - Lambda\|` e `max\|cs(C) - cs\|` ### **`<= passi * n_est * eps`** | ### ✅ **passa**, e ### **DEVE**: sono grandezze `C`-PARI |
| `L5` | **due grumi con `cs`** | la pendenza della separazione differisce da `G2` di ### **`> 3 sigma`**, con `sigma` ### **combinato** delle due | ### ⛔ **PREVEDO NESSUNA DIFFERENZA MISURABILE** a queste taglie: `G2` ha dato `0.69 sigma` fra `N` e lineare, e ### **un effetto di gravita' sara' piu' piccolo di quello** |

### ⛔ **E IL LIMITE CHE DICHIARO ADESSO, NON DOPO:** `L1`, `L2` e `L5` dicono *«partendo da un
grumo `v3` auto-intrappolato»*, e il ### **`v3` non ne ha trovato nessuno** *(misurato due volte:
referto `v3`, e di nuovo in `G1`)*. ### **Quindi useranno un PACCHETTO, non un grumo legato**, e
ogni risultato va letto come ### **«l'impronta di un pacchetto»** — non come *«l'impronta di una
massa»*. ### ⚠ **Chiamarlo altrimenti sarebbe leggere un artefatto**, ed e' lo stesso errore che
`G1` mi ha fatto correggere.

---

## 5. LA STELLA POLARE — **le cinque risposte, PRIMA del codice** *(`L-STELLA`)*

| | la domanda | la risposta |
|---|---|---|
| `1` | **`A14`: conserva energia e carica LOCALMENTE?** | ### **La CARICA si': ogni pezzo e' unitario**, e `\|psi\|` e `\|phi\|` si conservano **separatamente** *(`W9`, misurato a `1e-13`)*. ### ⛔ **L'ENERGIA NO, e la violazione la dichiaro:** la *conservazione modificata* del `v3` ### **non e' derivata per un `cs` non uniforme** — e non la chiamo energia *(`W9`: quella scelta e' di Luca)*. ### **Va fra le violazioni note** |
| `2` | **a quale dei TRE GRADINI arriva?** | ### **`(a)` robusto al rumore numerico: SI** *(tutto e' unitario, e le soglie sono `n_est * eps`)*. ### **`(b)` regge togliendo la legge pratica: E' ESATTAMENTE CIO' CHE `W1` MISURA** *(a novita' spente, `v3` al bit)*. ### ⛔ **`(c)` coincide con un limite noto: NON ANCORA** — il limite sarebbe *«la luce locale vale `1`»*, ed e' `L0`, che per `(F)` ### **prevedo FALLISCA** |
| `3` | **aggiunge un numero o una legge?** | ### ⭐ **NESSUN NUMERO** *(`W2`)*: `cs` e' un **rapporto**, e la famiglia frazionaria non ha parametri. ### ✅ **E AGGIUNGE UNA LEGGE SOLA, non due:** i quattro pezzi discreti sono ### **tutti involuzioni ermitiane** *(misurato, `2.1`)*, quindi ### **UNA famiglia** li copre — e `9-ter` e' rispettato ### **prima** di scrivere il codice. ### ⚠ **E la legge di `A1`** *(la materia scrive sul vuoto)* ### **e' una legge in piu', e si dichiara come tale** |
| `4` | **tocca `rho`, `c_s` o il SEGNO?** | ### ⛔ **TOCCA `c_s`, ed e' il punto del mandato.** Il verso dell'accoppiamento e' ### **materia → vuoto → `cs` → tutta la dinamica**, cioe' ### **«curvatura ← EM»** nella direzione *«la materia piega il tempo»*; ### ⚠ **il verso opposto** *(`cs` che retroagisce su come la materia si aggrega)* ### **c'e' automaticamente**, perche' `cs` entra in `N` — e questo rende il ciclo ### **chiuso**, che e' `[[EM-CURVATURA-BIDIREZIONALE]]` |
| `5` | **emergente o imposto?** | ### **Il test e' `L2` e `A6`.** `A6` **e' il controllo che puo' fallire**: se un campo di `cs` ### **casuale** producesse la stessa invarianza locale, `L0` sarebbe un ### **falso-uno**. ### ⛔ **E `L5` e' il test di <<emergente>> per la gravita': se la differenza con `G2` sta dentro la barra, NON si e' visto niente** — e lo scrivo come niente |

---

## 6. TODO DEL NEXT STEP — **operativo**

| | il passo | cosa decide | cosa mi FERMA |
|---|---|---|---|
| `1` | committare e pushare **questo file** | l'ordine verificabile da git | — |
| `2` | `proto_camminata/frazione4.py`: ### **la famiglia frazionaria `(A)` e `(B)`** su un'involuzione, col ### **cortocircuito esatto a `cs = 1`** e a `cs = 0` | la base di tutto `A3` | se il cortocircuito non da' `0.0` al bit ⟹ **FERMO** |
| `3` | `proto_camminata/vuoto4.py`: ### **`A1-scatter` e `A1-trasmissione`**, accendibili separatamente, spente = identita' | come la materia scrive su `Lambda` | se nessuna produce `dLambda` fuori dal grumo ⟹ **FERMO**, e si scrive |
| `4` | `proto_camminata/cslocale.py`: ### **`A2-arco` e `A2-grado`** *(il secondo come CONTROLLO)* | come il vuoto fissa `cs` | se ogni forma vuole una scala ⟹ **FERMO**, e la domanda va a Luca |
| `5` | `proto_camminata/camminata4.py`: ### **`(F)`**, e il tentativo di derivare ### **`(S)`** | il passo | se `(S)` non si chiude unitaria ⟹ **si SCRIVE**, come il mandato chiede, e si prosegue con `(F)` sola dichiarandolo |
| `6` | `proto_camminata/_collauda_banco4.py` nella suite | i bracci `W1`..`W9`, nessun clip, nessun import del simulatore, determinismo fra due processi | ogni braccio rosso senza cura ovvia ⟹ **FERMO** |
| `7` | `proto_camminata/_letture4.py` → `uscite/letture_v4.json` → `doc/REFERTO_prototipo_camminata_v4.md` | `L0`..`L5`, per `(F)` e per `(S)` | — |
| `8` | le **voci**: una per decisione e una per lettura, piu' le domande in `DA_DECIDERE_LUCA.md` ### **una per scelta** *(`A1`, `A2`, `(F)`/`(S)`)* | la registrazione | — |

### ⛔ **E LA COSA CHE NON FARO': SCEGLIERE.** Fra `A1-scatter` e `A1-trasmissione`, fra le forme
di `A2`, e fra `(F)` e `(S)` ### **decide Luca** — io porto ### **il confronto misurato**, una
voce per scelta. ### ⭐ **E il risultato del `2.4` e' il primo pezzo di quel confronto, ed e' gia'
pronto: `C` esatta OPPURE localita', e il conto e' `det(G_k) = (-1)^(d-1)`.**
