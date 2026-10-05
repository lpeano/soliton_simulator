# `VELENO-ARCHI-KEEP`, **passo (2): LA CURA, via `(i)`**

> ### **DECISIONE DI LUCA (2026-10-05): la nascita applica `keep` a TUTTE le derivate
> ### d'arco PRIMA del veleno.** **La via `(ii)` e' SCARTATA** — curava **un lettore solo**,
> ### lasciava `_sin2_vir` col difetto, e aggiungeva **una seconda scrittura** della legge di
> ### `dt_e`. ### **La decisione e' sua: non la reinterpreto.**

*Referto del passo (1): `doc/REFERTO_veleno_archi_keep_2026-10-05.md`, in **`cb24b95`**.*
*Il simulatore di partenza e' **`0f060670`**.*
**Scritto e committato PRIMA del codice** *(par.8)*.

---

## LA STELLA POLARE — **le cinque risposte, PRIMA del codice** *(`L-STELLA`)*

**① `A14` — conserva energia e carica LOCALMENTE?**
### **LA CURA NON TOCCA NESSUN BILANCIO, e il perche' e' strutturale:** `_dt_e_ultimo` e
`_sin2_vir` sono **derivate**, cioe' **cache** — il `REGISTRO_DERIVATE` le dichiara tali, e
per questo il veleno le tratta. ### **Una cache non entra in nessun bilancio: la sua unica
proprieta' e' essere ALLINEATA.**
### ✅ **E LA CURA VA NEL VERSO DI `A14`, non contro:** oggi una legge che leggesse
`_dt_e_ultimo` dopo la nascita userebbe **il valore di un altro arco**, e un bilancio locale
calcolato col valore del vicino ### **non e' locale.** La cura **toglie** quella possibilita'.

**② A quale dei TRE GRADINI arriva il risultato?**
### **Al gradino `(a)`, e in forma di IDENTITA' AL BYTE, non di statistica.** Il sigillo
confronta **tutti gli attributi di `net`** passo per passo: uno scarto e' `0` o non lo e'.
### ⛔ **NON arriva al `(b)`** — non tolgo nessuna legge pratica — ### **ne' al `(c)`**: non
c'e' un limite noto con cui confrontare un riallineamento di indici.
### **E il gradino basso qui NON e' un limite della misura: e' la forma giusta della
domanda.** Una cura che riallinea una cache **non ha una barra d'errore**.

**③ Aggiunge un numero o una legge? Di che tipo?**
### **ZERO numeri. E il conto delle leggi, per `9-ter`, va in DIMINUZIONE.**
Oggi ci sono **due comportamenti** alla nascita: le **colonne d'arco** si riallineano
*(`concat(x[keep], ...)`)*, le **derivate d'arco** no *(`concat(v, NaN)`)*.
### **Dopo la cura ce n'e' UNO: tutto cio' che e' per arco si riallinea.**
### ⛔ **Quindi la cura TOGLIE UN'ECCEZIONE, e non e' una formula in piu':** e' la **stessa**
operazione `x[keep]` che venti regole del registro fanno gia'.
### ⚠ **E DUE CONTATORI SI AGGIUNGONO** *(`_g_keep_riallineate`, `_g_keep_salti`)*: non sono
leggi, sono **misura di un invariante** — e `A9` dice che *un invariante che nessuno misura
non e' un invariante*. ### **Lo dichiaro perche' il sigillo li vedra' come attributi nuovi.**

**④ Tocca `rho`, `c_s` o il SEGNO? In quale verso dell'accoppiamento?**
### **NON tocca nessuno dei tre, e non ha un verso:** riallineare indici non ha un segno.
### ⚠ **E la conseguenza vera e' un'altra, che vale la pena scrivere:** dopo la cura gli
archi **NATI** nel passo hanno **`dt_e = NaN`** invece di un valore finito preso da un altro
arco. ### **Il veleno smette di essere mezzo-cieco e diventa intero** — e questo e'
**l'oggetto della nota** che il mandato chiede di mettere accanto a
`TETTO-CAUSALE-TEMPO-COORDINATO`.

**⑤ Emergente o imposto: sopravvive se si toglie la legge pratica?**
### **LA LEGGE PRATICA E' IL VELENO, e la cura NON lo toglie: lo COMPLETA.**
Il passo (1) ha misurato che il veleno copriva **`0.5000`** degli archi nuovi in una
divisione e **`1.0000`** nello Schwinger, e che l'unica differenza era `keep`.
### ✅ **Dopo la cura la copertura e' `1.0000` in ENTRAMBI** — cioe' il veleno fa **in tutti
i casi** cio' che gia' faceva in uno. ### **Non e' un comportamento nuovo imposto: e'
l'estensione di uno esistente al caso che gli sfuggiva.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di scrivere*

### **LA FORMA DELLA CURA, e i vincoli del mandato**

Una funzione nuova, chiamata **immediatamente prima** di `_avvelena_derivate(net)` *(che
resta dov'e', a `:1707`, dopo le regole)*:

| vincolo del mandato | come lo rispetto |
|---|---|
| `keep` dal **contesto**, mai ricostruito | `c.get("keep")`, come fanno `_rn_div_i` *(`:1744`)* e le altre colonne d'arco |
| solo le derivate **d'arco** con classe **`avvelena`** | lette dal **`REGISTRO_DERIVATE`**, ### **non da un elenco a mano** |
| solo gli eventi **che hanno `keep`** | se `c.get("keep")` e' `None` la funzione **esce subito** *(e' lo Schwinger)* |
| lunghezza sbagliata: **non si indovina** | ### **`_ferma_registro`**, con le eccezioni esistenti `CacheCorta`/`CacheLunga` |
| **nessun flag** | la cura **agisce sempre**, come il veleno che dichiara *«il veleno agisce sempre»* |
| il veleno resta dov'e' | la cura sta **prima** di lui, non al suo posto |

### **E PERCHE' FUNZIONA, col conto** *(e il conto e' quello del passo 1, al rovescio)*

Oggi: `len(v) = m`, `bersaglio = m + s`, quindi il veleno appende `s` celle su `2s` archi
nuovi. ### **Dopo la cura:** `len(v) = sum(keep) = m - s`, `bersaglio = m + s`, quindi
appende `(m+s) - (m-s) = `**`2s`** celle. ### **Esattamente gli archi nuovi, e la copertura
passa da `0.5000` a `1.0000`.**

### ⛔ **IL PUNTO PIU' DELICATO, e non e' il codice: e' il `_veleno_registro`**

`_avvelena_derivate` tiene un registro delle celle avvelenate, e ricorda **l'inizio**:

```
_prec = _vreg.get(nome)
_inizio = len(v)
if _prec is not None and _prec["arr"] is v:
    _inizio = min(int(_prec["inizio"]), len(v))
```

La mia cura **sostituisce l'array con un oggetto NUOVO** *(`v[np.flatnonzero(keep)]`)*,
quindi `_prec["arr"] is v` sara' **falso** e `_inizio` diventera' `m - s` invece di `m`.
### ✅ **Ed e' GIUSTO: le celle avvelenate ora cominciano a `m - s`**, perche' sono `2s`.
### ⚠ **Ma lo scrivo PRIMA perche' e' il punto in cui una cura puo' rompere un presidio:**
`verifica_invarianti` usa quel registro per **non segnalare** le celle avvelenate, e se
l'inizio fosse sbagliato ### **segnalerebbe un dominio violato su celle legittime, oppure
tacerebbe su celle che non lo sono.**

### ⛔ **E IL CASO DEI DUE EVENTI NELLO STESSO PASSO, che va guardato per la stessa ragione**

In un passo con **divisione E Schwinger** il veleno gira **due volte**, e il codice unisce le
code *«se la coda precedente e' ancora VIVA»* — col test `_prec["arr"] is v`.
### **La mia cura non gira per lo Schwinger** *(non ha `keep`)*, quindi fra il primo e il
secondo veleno l'oggetto **non cambia**, e l'unione **continua a funzionare**.
### **Il passo (1) ha misurato che questo caso ESISTE: ai passi `70`, `82`, `84`, `86`.**

## 2. L'ATTESA SUL SIGILLO, e **una conseguenza che il criterio del mandato non elenca**

### ✅ **CIO' CHE MI ASPETTO IDENTICO AL BYTE:** tutto lo **stato**. Il passo (1) ha
stabilito che ### **nessun lettore vivo legge queste due derivate dopo la nascita nello
stesso passo** — `decidi_divisione` gira **prima** di `nascita`, e `batch_condensazione`
**non gira** col driver. ### **Quindi la dinamica non deve muoversi di un bit.**

### ⛔ **E CIO' CHE NON PUO' ESSERE IDENTICO, PER COSTRUZIONE DELLA CURA**

Il mandato dice: *«lockstep su TUTTI gli attributi di `net`. Le sole eccezioni ammesse sono
`_dt_e_ultimo` e `_sin2_vir`, e solo negli eventi di divisione»*.
### **Scrivo ORA, prima di misurare, che ne prevedo ALTRE TRE** — e sono tutte
**conseguenze aritmetiche della cura**, non effetti collaterali:

| attributo | perche' cambia | e' stato? |
|---|---|---|
| `_g_veleno_celle` | conta le celle avvelenate: passa da `s` a `2s` per evento | ### **no: e' un CONTATORE** |
| `_veleno_registro[...]["inizio"]` | l'inizio delle celle avvelenate passa da `m` a `m - s` | ### **no: e' il REGISTRO del veleno** |
| `_g_keep_riallineate`, `_g_keep_salti` | **non esistono** nel blob vecchio | ### **no: contatori NUOVI** |

> ### ⚠ **NON LO CHIAMO UN PROBLEMA DEL CRITERIO, E NON LO AGGIUSTO DA SOLO.** Il sigillo
> li **misurera'** e il referto li **elenchera' uno per uno**, separando
> ### **<<differenza di STATO>>** da ### **<<differenza di CONTATORE o di REGISTRO DEL
> VELENO>>**. ### **Se Luca ritiene che l'elenco delle eccezioni vada esteso, e' una sua
> decisione**, e il referto gliela mette davanti coi numeri.
> ### ⛔ **Se invece divergesse un attributo di STATO, vale il FERMO del mandato:** vorrebbe
> dire che la conclusione di `cb24b95` — *«nessun lettore vivo le legge dopo la nascita»* —
> ### **era sbagliata.**

### **E DUE ATTESE SUI CONTROLLI INCROCIATI che il mandato chiede**

| | l'attesa | perche' |
|---|---|---|
| lo strumento `425b8d47` sul blob **nuovo** | ### **`0` differenze** sui `166` confronti | la cura riallinea: `vecchio[flatnonzero(keep)]` **diventa** cio' che l'array contiene |
| lo strumento `425b8d47` sul blob **vecchio** `0f060670` | ### **`166` differenze**, come oggi | ### **il caso che DEVE fallire: verifica che lo strumento VEDA ancora il difetto** |
| lo strumento del tetto `19d08753` sul blob **nuovo** | ### **`0` passi invalidi** in `(A)` | ### **e' la conferma che il `FERMO` di `eeb54be` nasceva da QUI** |

### ⚠ **E IL TERZO E' IL PIU' INFORMATIVO, perche' puo' SMENTIRE una conclusione mia:** se
dopo la cura il controllo `(A)` del tetto causale **continuasse** a trovare passi invalidi,
allora ### **il disallineamento di `_dt_e_ultimo` aveva ANCHE un'altra causa**, e il referto
del passo (1) avrebbe attribuito tutto a `keep` sbagliando.
### **Lo dichiaro come esito possibile, non come rischio remoto.**

## 3. I CRITERI DEL SIGILLO

*(Quelli fissati in **`923e396`** restano; qui sono riscritti insieme ai nuovi del mandato,
in un posto solo, perche' il sigillo li deve leggere tutti.)*

| | il criterio | che cosa lo fa FALLIRE |
|---|---|---|
| **`0`** | **braccio 0**: *prima* + patch committata = **`0f060670`** | un blob diverso: la patch non riproduce il punto di partenza |
| ### **`1`** | ### **STATO IDENTICO AL BYTE su tutti i 150 passi**, lockstep prima/dopo su **tutti** gli attributi di `net` | ### **una divergenza di STATO in un punto qualunque -> FERMO** |
| **`2`** | le eccezioni ammesse sono **`_dt_e_ultimo`** e **`_sin2_vir`**, e **solo** negli eventi di **divisione** | una differenza su quelle due in un evento **Schwinger** |
| **`3`** | negli eventi **Schwinger** anche le due derivate sono **identiche al byte** | qualsiasi differenza li' |
| **`4`** | **copertura**: dopo la cura le celle `NaN` sugli archi nuovi di una divisione sono **`2s`**, non `s` | una copertura `< 1.0000` |
| **`5`** | **controllo POSITIVO**: lo strumento `425b8d47` sul blob nuovo da' **`0`** differenze sui `166` confronti | differenze residue |
| ### **`6`** | ### **CASO CHE DEVE FALLIRE**: lo strumento `425b8d47` sul blob **vecchio** ridà **`166`** differenze | ### **se desse `0`, lo strumento non vedrebbe piu' il difetto e il criterio `5` non proverebbe niente** |
| **`7`** | lo strumento del tetto `19d08753` sul blob nuovo da' **`0`** passi invalidi in `(A)` | passi invalidi residui: il `FERMO` di `eeb54be` aveva **un'altra** causa |

### ⛔ **E IL CRITERIO CHE NON POSSO SCRIVERE, come al passo (1):** *byte-identico sulle
**DERIVATE*** **non si puo' chiedere** — il `COMMIT 4` lo ha gia' dichiarato per se stesso,
e ### **una cura che riallinea le derivate le cambia PER DEFINIZIONE.** Il criterio e' sullo
**STATO**.

## 4. TODO DEL NEXT STEP

1. **il codice della cura** nel simulatore, e **lo strumento del sigillo**, nello stesso
   commit *(e l'inventario, par.6 ①)*;
2. **il blob nuovo** citato in `doc/INVENTARIO_strumenti.md` e nella voce d'indice;
3. la voce **`VELENO-ARCHI-KEEP`** passa a **`curato`** col commit e il blob nuovo;
4. nel **`REGISTRO_FISICA`**, accanto a `TETTO-CAUSALE-TEMPO-COORDINATO`, la nota: ### **dopo
   la cura gli archi NATI nel passo hanno `dt_e = NaN`**, e il passo (2) del tetto avra'
   bisogno di **una regola per loro** — ### ⛔ **DECISIONE DI LUCA, da prendere ALLORA e non
   adesso**;
5. **il sigillo gira DOPO il commit del codice**, e il referto e' un commit a se';
6. ### **se un criterio fallisce: si committa lo stato + il fallimento e si FERMA** *(par.5)*.

## 5. L'ESITO — **ANNOTATO, non riscritto** *(par.8)*

> ### ✅ **E IL SIGILLO E' APPROVATO: decisione di Luca del 2026-10-05 su
> ### `c4e9fd5`.** La classificazione dei sei contatori e' **approvata**, e il
> guardiano l'ha verificata con un **lockstep indipendente su Linux**.
> ### **Quindi il criterio 1 resta `0`, e quello zero vale su DUE piattaforme.**

> ### **GLI OTTO CRITERI PASSANO. Il numero e' `0`: le divergenze di
> ### STATO su 150 passi, 290 attributi per passo.**
> Il referto e' `doc/REFERTO_veleno_archi_keep_cura_2026-10-05.md`.

### **LE PREVISIONI DELLA SEZIONE 2, UNA PER UNA — e una NON ha tenuto**

| previsto in sezione 2 | misurato | |
|---|---|---|
| tutto lo **STATO** identico al byte | ### **`0` divergenze** | ✅ **TENUTA** |
| `_g_veleno_celle` cambia | `109` passi | ✅ **TENUTA** |
| `_veleno_registro` cambia | `83` passi | ✅ **TENUTA** |
| `_g_keep_riallineate` cambia | `109` passi | ✅ **TENUTA** |
| `_g_keep_salti` cambia | ### **`0` — mai** | ⚠ **PREVISTA E NON AVVENUTA** |
| *(non previsti per nome)* `_g_keep_celle_tolte`, `_g_keep_senza` | `109` e `81` passi | ⚠ **sono contatori MIEI, nella classe che avevo previsto, ma non li avevo NOMINATI** |
| — | ### **`_g_inv_veleno_ok`, `109` passi** | ### ⛔ **NON PREVISTO** |

### ⚠ **`_g_keep_salti` PREVISTO E MAI SCATTATO, e vuol dire una cosa precisa:**
quel contatore cresce quando una derivata d'arco **non e'** un `float` a una dimensione
e la cura la **salta**. ### **Zero su 150 passi significa che tutte e due le
derivate d'arco sono sempre state `float64` monodimensionali** — cioe' che il
**ripiego** che avevo messo nella cura ### **non e' mai servito.** Lo dichiaro perche'
un ramo che non gira mai e' `A11`: se protegge da un **errore**, l'errore va cercato.
### **Qui protegge da una FORMA che il `REGISTRO_DERIVATE` non garantisce**, quindi
resta; ma il numero e' `0`, e va saputo.
### **E LO STESSO VALE PER `_g_keep_assenti`**, l'altro ripiego della cura *(una
derivata del registro che non esiste sulla rete)*: ### **non compare fra gli attributi
diversi, quindi non e' mai stato creato — `0`.** ### **I DUE RIPIEGHI DELLA CURA SONO
### ENTRAMBI A ZERO**, e lo dico insieme invece di nominarne uno solo.

### ⛔ **`_g_inv_veleno_ok` E' LA PREVISIONE CHE MI E' MANCATA, e il suo significato
### e' il risultato migliore di questo sigillo**

Conta le celle **avvelenate E `nan`**, cioe' quelle che il controllo d'invariante
**ESENTA** dal dominio *(`:6647`)*. Cresce perche' le celle avvelenate sono passate da
`s` a `2s`. ### **E il commento a `:6612` dice che, prima del veleno, l'invariante
<<verificava il dominio di derivate che portavano VALORI VECCHI, e che passavano PERCHE'
ERANO POSITIVI PER CASO>>.**

> ### **Quindi fino a ieri META' DEGLI ARCHI NUOVI DI OGNI DIVISIONE era ANCORA in quel
> ### caso**, e nessuno lo sapeva. ### **Ora il veleno li copre tutti e l'invariante li
> ### esenta tutti: il presidio e' diventato ONESTO sul doppio delle celle.**
> ### ⚠ **Non l'avevo previsto perche' avevo elencato i contatori DELLA CURA, e non
> ### mi ero chiesto chi LEGGE il registro del veleno.**

### **LE TRE ATTESE SUI CONTROLLI INCROCIATI: TUTTE E TRE TENUTE**

| | attesa | misurato |
|---|---|---|
| `425b8d47` sul blob **nuovo** | `0` su `166` | ### **`0`**, e `63 802 623` -> **`0`** elementi |
| `425b8d47` sul blob **vecchio** | `166`, come prima | ### **`166` su `166`**, numeri identici a `cb24b95` |
| `19d08753` sul blob **nuovo** | `0` passi invalidi in (A) | ### **`0` su `300` verifiche** |

### ✅ **E IL TERZO, che avevo dichiarato <<il piu' informativo perche' puo' SMENTIRE
### una conclusione mia>>, NON l'ha smentita:** ogni numero del controllo del tetto e'
**identico** fra blob vecchio e nuovo — archi confrontati `141 541 432`, esclusi
`4 792`, inverificabili `4` — ### **tranne `con_differenze`, che passa da `166` a
`0`**. ### **Il `FERMO` di `eeb54be` nasceva da qui, e da nient'altro.**

### **CHE COSA RESTA DAVANTI A LUCA, e non lo decido io**

1. ### **La lista delle eccezioni del criterio 2:** il criterio nomina due **derivate**;
   le `6` differenze che restano sono **contatori e un registro**. Io li ho
   classificati `contatore/registro` e **non** `STATO`, ### **ma la classificazione l'ho
   scritta io** — va approvata o corretta.
   ### ✅ **APPROVATA da Luca il 2026-10-05**, sul sigillo `c4e9fd5`, con DUE motivi:
   ### **ogni altro attributo resta identico al byte** *(quindi nessuno dei sei rientra
   in una legge)* e ### **`_veleno_registro` e' letto solo da `verifica_invarianti`,
   che e' un PRESIDIO**. ### **E verificato dal guardiano con un lockstep INDIPENDENTE
   su LINUX** *(150 passi, tutti gli attributi di `net`)*: ### **una seconda misura su
   un'altra piattaforma, non un'approvazione sulla parola.**
2. ### **La regola per gli archi nati** nel passo (2) del tetto causale, che ora hanno
   `dt_e = NaN`: ### **registrata, non decisa.**
