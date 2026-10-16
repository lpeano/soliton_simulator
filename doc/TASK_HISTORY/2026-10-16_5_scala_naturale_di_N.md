# `5` — **LA SCALA NATURALE DI `N` NON ERA UNA DOMANDA: HA UNA RISPOSTA**

*(integrazione del guardiano, verifica di `0237603` e `627d434`. Base: `4df8fd8b`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE**, e il suo commit dev'essere
> **ANTENATO** dei commit del lavoro *(`CLAUDE.md` §8)*.

---

## 1. RAGIONAMENTO PRELIMINARE — *e comincia con un mio errore*

### ⛔⛔ **L'ERRORE: <<NESSUNA FUNZIONE AFFINE LIMITA `N`>> E' FALSO**

Avevo aperto la voce `[[DOMANDA-LA-SCALA-NATURALE-DI-N]]` scrivendo che
`N = -rho ln(1 + Lambda/rho)` *«diverge come un logaritmo»* e che quindi
### **nessuna funzione affine di `rho` e `Lambda` la limita.**

> ### ⛔ **E' FALSO, e il conto sta in due righe:**
>
> ```
> |N_k| = rho_k ln(1 + Lambda_k/rho_k) <= rho_k * (Lambda_k/rho_k) = Lambda_k
>                                         perche'  ln(1 + y) <= y   per ogni y > -1
> quindi   somma_k |N_k| <= somma_k Lambda_k = V
> ```

### ⚠ **DOVE AVEVO SBAGLIATO, esattamente:** avevo guardato l'asintoto
`Lambda/rho -> infinito`, dove `N/rho` ### **diverge** come `ln(Lambda/rho)` — e ne avevo
concluso che `N` non fosse limitata. ### **Ma la divergenza e' in `N/rho`, e il limite che
serviva era in `Lambda`:** `rho` va a zero ### **piu' in fretta** di quanto il logaritmo
cresca, e il prodotto resta sotto `Lambda`.

### ⭐⭐ **E `V` NON E' SOLO UN LIMITE: E' CONSERVATA ESATTAMENTE**

`V = somma_k Lambda_k` e' ### **la norma del vuoto**, e i pezzi del tick la conservano
*(misurato: `|Delta V| = 0.000e+00` nei bracci `(4a)` e `(4b)` di `_collauda_deriva`)*.
### ✅ **Quindi la scala naturale del termine del vuoto esiste, ed e' per di piu'
COSTANTE** — che e' meglio di quello che la saturazione aveva.

### ⭐ **E L'HO GIA' RIMISURATA, in modo indipendente dal guardiano**

`1e6` coppie `(rho, Lambda)` log-uniformi in `[1e-8, 1e8]`, seme `7`:

| la forma | `max |N|/Lambda` |
|---|---|
| `rho * log1p(Lambda/rho)` | ### **`1.0000000000000002`** — ### **lo stesso numero del guardiano, cifra per cifra** |
| `-rho * log(rho/(rho+Lambda))` *(la forma che GIRA)* | `1.9761410820732366` |

### ⛔ **E il secondo numero NON smentisce la disuguaglianza: e' la PRECISIONE.**
A `rho/Lambda = 1e15`: `log1p` da' `0.9999999999999997`, la forma che gira
`0.9992007221626414`. ### **E' la nota `2` del mandato.**

### ⛔⛔ **E UNA COSA CHE DICO PRIMA DI MISURARE, perche' potrebbe smentirmi:**
### **il caso che DEVE fallire chiesto dal mandato E' IMPOSSIBILE.**

Il mandato chiede *«un caso che DEVE fallire: la vecchia scala `nat2` della saturazione
applicata a uno stato dove viene superata»*. ### **Ma `nat2` non si puo' superare:**

```
nat2 = somma|h| + (pi/2) * somma Lambda  >=  (pi/2) * V  ~  1.5708 * V
somma|N| <= V                            quindi   somma|N|/nat2 <= 2/pi ~ 0.6366
```

> ### ⛔ **Cioe' `nat2` e' un limite VALIDO ma LASCO**, di un fattore `pi/2` almeno.
> ### **Un caso che lo supera non esiste**, e scrivere un braccio che *«deve fallire»* su
> una cosa impossibile ### **darebbe un FALSO-UNO: passerebbe sempre, senza dire niente.**
> ### ✅ **QUINDI NE METTO DUE CHE POSSONO FALLIRE DAVVERO, e lo dico al guardiano**
> invece di far finta.

### **I DUE CASI CHE SOSTITUISCONO QUELLO IMPOSSIBILE**

### ① **`rho` COME SCALA DEVE FALLIRE:** `somma|N| <= somma rho` e' ### **FALSA**, perche'
`|N|/rho = ln(1 + Lambda/rho)` ### **non e' limitata.** *(A `rho = 1e-8`, `Lambda = 1e8`:
`|N|/rho ~ 36.8`.)* ### **E' una scala PLAUSIBILE che non e' un limite**, quindi il braccio
di `V` non e' verde per costruzione.
### ② **LA FORMA FLOAT CHE GIRA DEVE SUPERARE `V` a `rho/Lambda` enorme** — ed e' la nota
`2`, misurata: ### **`1.976`.** ### **Il limite e' della MATEMATICA, non del codice**, e un
braccio che non lo distinguesse ### **attribuirebbe alla legge un difetto del float.**

### ⭐ **CHE COSA NON SO, e lo dico adesso**

| | non so… |
|---|---|
| `a` | quanto e' ### **stretta** la stima sulle scene VERE *(non su coppie casuali)*: se `rho/Lambda` fosse piccolo su tutti i nodi, `somma|N|/V` sarebbe ### **molto sotto `1`**, e `V` sarebbe una scala ### **lasca** — valida, ma lasca |
| `b` | se cambiare `nat2` sposti qualche numero ### **gia' pubblicato** in un referto: i numeri `relnat_*` della deriva nascono da la', e ### **vanno rimisurati, non riscritti** |

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i criteri, fissati QUI*

| | il passo | il criterio, e cosa mi FERMA |
|---|---|---|
| `1` | la ### **derivazione** scritta: `ln(1+y) <= y` ⟹ `|N_k| <= Lambda_k` ⟹ `somma|N| <= V` | — |
| `2` | un braccio che la ### **MISURA su stati casuali**, con `log1p` | ### **`max |N|/Lambda <= 1 + 8 ulp`** |
| `3` | il caso ### **`rho >> Lambda`**, dove il rapporto ### **tende a `1`** | ### **`>= 0.99`**: se fosse molto sotto, la stima non sarebbe stretta e lo direi |
| `4` | il caso che DEVE fallire ### **①**: `rho` come scala | ### **`max |N|/rho > 10`** |
| `5` | il caso che DEVE fallire ### **②**: la forma float che gira, a `rho/Lambda` enorme | ### **`> 1`**, e il braccio dice che e' ### **la PRECISIONE e non la legge** |
| `6` | `nat2` diventa ### **`V`** in `deriva.corri`, e i `relnat_*` si ### **RIMISURANO** | ### ⛔ **i numeri vecchi NON si riscrivono:** si riportano accanto |
| `7` | la voce si ### **CHIUDE** col criterio scritto, e il motivo e' *«non serviva una decisione di Luca: era un conto»* | ### ⛔ **se trovo un controesempio, RELAZIONO e non chiudo** |
| `8` | la ### **nota di precisione** nella scheda della legge, come limite noto | — |

### ⛔⛔ **E `log1p` NON SI TOCCA IN QUESTO PEZZO.** Il mandato e' esplicito: passare a
`log1p` e' ### **una modifica della FORMA FLOAT della legge**, quindi
### **`M-B1` al bit non reggerebbe piu'** e ### **va dichiarato prima.**
### ✅ **Lo dichiaro qui come PROPOSTA, e non lo faccio:** la legge resta
`ln(rho/(rho+Lambda))`, e il limite va ### **scritto nella scheda.**

---

## 3. TODO

1. `primo_ordine/_collauda_materia_vuoto.py`: i ### **quattro bracci** *(la
   disuguaglianza, il caso `rho >> Lambda`, e i due che devono fallire)*.
2. `primo_ordine/deriva.py`: `nat2 = V`, e la prosa di `nat2` ### **riscritta col
   motivo**; `SAT` e `elicita` ### **escono** da `corri` se non servono piu'.
3. i `relnat_*` ### **RIMISURATI**, coi vecchi accanto.
4. `primo_ordine/leggi/leggi.yaml`: la ### **nota di precisione** nella scheda della legge
   *(e la scheda si ### **rigenera**)*.
5. la voce `[[DOMANDA-LA-SCALA-NATURALE-DI-N]]` ### **CHIUSA**, col criterio e col motivo;
   e la voce `[[STRUMENTI-SULLA-LEGGE-VECCHIA]]` aggiornata, perche' una delle sue
   `8` SCADUTE ### **e' curata qui.**
6. `csv/_strumento_dalla_tabella.py`: l'eccezione di `deriva.py`/`saturazione`
   ### **TOLTA se l'import sparisce** — e se non la togliessi, ### **`P-TAB` la
   chiamerebbe ORFANA e il commit fallirebbe.** ### ⭐ **Il presidio lavora per me il
   giorno dopo essere nato.**
7. il referto, la RIPRESA, la relazione — e ### **il caso impossibile DETTO al guardiano.**
