# REFERTO -- **IL SIGILLO DELLA CURA (2) DI `MEM-HEBB-VERSO`: il flag `MEM_FASE`**

*(decisione di Luca del 2026-10-04, confermata dal referto `2717308`; i **cinque
criteri** furono fissati **prima del codice** in `634762c`, e il codice e' in `7a03063`.)*

> ### ✅ **IL SIGILLO PASSA, tutti e cinque i criteri.**

| | |
|---|---|
| simulatore | `e2940b3c` **->** `1feb9b0a` |
| patch del braccio 0 | `8b9c0c1a` |
| sigillo | `a5cb4c60` |
| bracci | **tre**: `A` il blob **vecchio**, `B` il nuovo con `MEM_FASE = True`, `C` il nuovo col **DEFAULT** |
| passi | `150` · attributi per passo **`236`** |
| configurazione | dichiarata su **`C`**, il braccio al DEFAULT: ### **`ZERO` differenze dal driver** |
| piattaforma | `python 3.13.2` · `numpy 2.3.0` · Windows 11 · AMD64 |

## IL BRACCIO 0: il *prima* non si asserisce, SI RICOSTRUISCE

| | |
|---|---|
| commit che ha cambiato il simulatore | `7a03063` |
| suo **PADRE** *(`H-P8`)* | `634762c` |
| blob estratto dal padre | `e2940b3c` |
| blob che **la patch dichiara** | `e2940b3c` |
| **il *prima* e' quello atteso** | ### **`True`** |
| blob patchato | `1feb9b0a` |
| blob sul disco oggi | `1feb9b0a` |
| **coincide** | ### **`True`** |

## ✅ CRITERIO 1: **`A` contro `B` -- ZERO differenze, al byte**

> ### **`0` differenze su `150` passi e `236` attributi per passo.**

### **Il flag ACCESO e' byte-inerte: riproduce `e2940b3c` esattamente.**
### 📌 **E QUESTO E' IL CRITERIO CHE RENDE LEGGIBILI GLI ALTRI:** se `B` non fosse
identico ad `A`, le differenze fra `B` e `C` ### **non si potrebbero attribuire al
flag** -- potrebbero venire dalla patch. ### **Zero su 150 passi dice che la patch non
ha toccato nient'altro.**

## ✅ CRITERI 2 e 3: **al passo 1 differisce SOLO `phi`, e DIFFERISCE**

| | |
|---|--:|
| differenze al passo 1 | ### **`1`** |
| l'attributo | ### **`phi`** |
| nodi diversi | `12 623` |
| **max scarto** | ### **`1.256349e+01`** |
| ALTRO che differisce | ### **`0`** |

### ✅ **IL CRITERIO 2 PASSA:** al passo 1 ### **nient'altro** si muove. E non e' un
colpo di fortuna: ### **era PREVISTO da una catena censita dall'AST** e scritta nel task
history *(`:9578` e' l'**unica** scrittura di `phi` nella funzione **e** l'**ultima
scrittura di stato**; `memoria_hebbiana_moto` e' l'**ultima legge** della composizione; e
il freno su `d0`, che gira dopo, **non legge `phi`**)*.
### **Se fosse differito altro, la prima cosa da rivedere sarebbe stata QUELLA LETTURA.**

### ✅ **IL CRITERIO 3 -- IL CASO CHE DEVE FALLIRE -- FALLISCE:** `phi` ### **differisce
su `12 623` nodi.** ### **Lo spegnimento spegne.**

## ⛔ **E UN NUMERO CONFERMA UNA TRAPPOLA CHE AVEVO DICHIARATO PRIMA DI MISURARE**

Nel task history, **prima del codice**, avevo scritto: *<<il sito applica anche
`% self._dphi()`, non solo la somma. Spegnerlo toglie ANCHE la normalizzazione modulo
`4pi` ... quindi se `phi` uscisse dal dominio la differenza al passo 1 sarebbe PIU'
GRANDE di `shift`, e il sigillo deve RIPORTARE la differenza, non solo contarla>>*.

| | |
|---|--:|
| max scarto misurato su `phi` | **`1.256349e+01`** |
| `4*pi`, cioe' `_dphi()` | **`1.256637e+01`** |
| ### **rapporto** | ### **`0.999770`** |
| mediana di `abs(shift)` *(referto `2717308`)* | `4.262912e-03` |
| ### **quante volte lo scarto e' piu' grande** | ### **`2947`** |

> ### **LO SCARTO MASSIMO E' `0.9998` VOLTE `4pi`: e' il MODULO, non lo shift.**
> ### **Su almeno un nodo l'effetto dominante del sito NON era il trascinamento di fase:
> ### era la NORMALIZZAZIONE.** Quel nodo aveva `phi` **fuori dal dominio**, e il
> `% _dphi()` lo riportava dentro ### **a ogni passo.**
> ### ⚠ **E IL SIGILLO LO VEDE SOLO PERCHE' RIPORTA LO SCARTO E NON SOLO IL
> ### CONTEGGIO** -- che e' esattamente cio' che avevo scritto di fare.

### 📌 **CHE COSA QUESTO APRE, e NON lo decido io:** se `phi` esce dal dominio, allora
### **c'e' una scrittura di `phi` che non normalizza**, e il `% _dphi()` del sito della
fase la stava ### **coprendo per caso.** ### **Spegnere il sito ha scoperto il buco,
non lo ha creato.** ### ⛔ **E' una DOMANDA NUOVA, da portare a Luca con questo numero:
quale scrittura di `phi` lascia il dominio?** *(Le scritture sono `10`, censite
dall'AST.)*

## CRITERIO 4: **la crescita delle differenze, RIPORTATA e NON giudicata**

| passo | attributi diversi |
|--:|--:|
| `1` | `1` |
| `2` | `46` |
| `3` | `56` |
| `5` | `57` |
| `10` | `58` |
| `20` | `58` |
| `40` | `59` |
| `60` | `132` |
| `80` | `144` |
| `100` | `148` |
| `120` | `146` |
| `150` | `145` |

### **La propagazione e' quella attesa dal criterio del mandato** *(«dal passo 2 in poi
le differenze si propagano»)*: `phi` entra in `calcola_psi`, quindi in `psi`, `|psi|^2`,
`rho` e `cs` ### **dal passo dopo.** Al passo 2 sono gia' `46`; poi la crescita ### **rallenta** fra il `3` e il `40`
*(`56` -> `59`)* e ### **riprende dopo il `60`.**

### ⛔ **NON LO GIUDICO, e il mandato lo dice esplicitamente.** Riporto che il salto
dopo il `40` coincide con l'epoca in cui le **nascite** cominciano a divergere fra i due
bracci — e ### **che questa e' una correlazione, non una spiegazione.**

## CHE COSA CAMBIA A VALLE, riportato e non giudicato

| | `B` *(flag acceso)* | `C` *(il DEFAULT)* | differenza |
|---|--:|--:|--:|
| `n` finale | `14 000` | `14 124` | ### **`+124`** |
| archi finali | `473 022` | `473 143` | ### **`+121`** |

### **Col sito SPENTO la rete cresce di PIU': `+124` nodi e `+121` archi** su `150` passi.
### ⛔ **NON LO GIUDICO.** Riporto il numero e dico che ### **non so se sia un bene o
un male**, perche' ### **questo repo non ha un criterio su quanto la rete DEBBA
crescere.**

## ⚠ IL SIGILLO E' MORTO UNA VOLTA, E NON ERA LA FISICA

Il primo giro si e' fermato al **passo 61** con `FloatingPointError: invalid value
encountered in subtract`, ### **dentro il MIO comparatore:** la riga
`np.nanmax(np.abs(af - bf))` ### **alza** quando entrambi i valori sono `inf`, perche' il
simulatore mette `np.seterr` a **raise** sull'invalido.

### **LA FORMA GIUSTA, ora cablata:** lo scarto massimo si misura ### **solo dove
entrambi sono FINITI**, e le celle non finite che differiscono si ### **contano a parte**
-- perche' `inf` contro `1e300` e' una differenza **vera** e ### **non ha uno scarto.**

### ⛔ **E UN SECONDO DIFETTO MIO, che avrebbe dato un FERMO PER LA RAGIONE SBAGLIATA:**
il sigillo dichiarava la configurazione su **`B`**, che ha `MEM_FASE = True` e quindi e'
### **fuori configurazione PER COSTRUZIONE.** Avrebbe letto quella differenza come un
**guasto**. ### **Ora la dichiara su `C`**, il braccio al **default**, cioe' ### **la
fisica decisa** -- ed e' su quello che la domanda *<<dove si e' misurato>>* ha senso.
### **L'ho trovato leggendo l'uscita del run morto**, non ragionando.

### ⚠ **E UNA MIA AFFERMAZIONE FALSA, smentita dalla verifica:** avevo scritto che lo
stesso difetto era **latente** nell'altra copia del comparatore
*(`_sigillo_veleno_keep.py`)*. ### **NON E' VERO:** quel comparatore ### **non calcola
affatto lo scarto massimo** -- conta le celle e torna `(d == 0, d, "")` **senza
sottrarre** *(`:183-188`)*. ### **Il difetto e' MIO soltanto, e nasce dall'aver AGGIUNTO
`max_scarto`.** L'avevo affermato **senza verificarlo** *(`P1`)*, e ### **la correzione e'
scritta, non cancellata** *(`13fe302`)*.

## CHE COSA QUESTA CURA **NON** FA

1. ### **non cura il sito: lo SPEGNE.** Gli altri due difetti restano — *<<solo
   l'estremo `ii` riceve>>* in `MEM-HEBB-VERSO`, e `dir_laterale = (-y, x, 0)` in
   ### **`FASE-TRASCINAMENTO-3D`, CHE RESTA APERTA.** ### **La legge in 3D NON si scrive
   ora** *(decisione di Luca)*;
2. ### **non dice che cosa si perde:** la frazione di contributi che veniva **applicata** *(il complemento del `0.9728` scartato, misurato in `2717308`)*
   ### **era un contributo vero alla fase**, e spegnerlo lo toglie. ### **I numeri a
   valle dicono QUANTO cambia, non se sia giusto;**
3. ### **non tocca `MEM_MOTO` ne' `MEM_MOTO_TUTTO`**, e `mem_mot` ### **continua ad
   aggiornarsi.**

## E UNA COSA CHE QUESTO COMMIT CAMBIA PER TUTTO IL REPO

> ### ⛔ **`MEM_FASE` E' IL PRIMO FLAG DI QUESTO REPO IL CUI DEFAULT CAMBIA LA FISICA.**
> Tutti gli altri del `README` § 9-bis nascono **OFF e inerti** oppure **ON**.
> ### **Quindi da `7a03063` ogni sigillo e ogni rigiocata che RI-ESEGUE il simulatore
> ### da' numeri diversi dai suoi referti.**
> ### ✅ **E non e' un difetto: i referti sono legati al loro BLOB** *(par.6: un
> sigillo si rigira con `git checkout` del commit che ha sigillato)*.

## I CINQUE CRITERI, IN UNA TABELLA

| | che cosa pretendeva | numero | esito |
|---|---|--:|---|
| **0** | la patch su `e2940b3c` ridA' `1feb9b0a` al byte | `True` | ### **PASSA** |
| **1** | `A` contro `B`: identita' al byte su `150` passi | `0` | ### **PASSA** |
| **2** | al passo 1 differisce **solo** `phi` | `1` differenza, `phi` | ### **PASSA** |
| **3** | ### **il caso che DEVE fallire:** `phi` deve differire | `12 623` nodi | ### **PASSA** |
| **4** | la crescita riportata, non giudicata | da `1` a `145` | ### **FATTO** |
