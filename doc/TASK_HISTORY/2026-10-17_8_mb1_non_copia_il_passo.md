# `8` — **`M-B1` NON COPIA IL PASSO NELL'ALBERO VECCHIO** *(un falso-uno in attesa)*

*(integrazione del guardiano del `2026-10-16`, verifica di `26f5f24`, `ff26981`, `8c7b928`.
Base: `8c7b9288`. Da fare **PRIMA del punto `D`**, che cambia il passo.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE** *(`CLAUDE.md` §8)*.

---

## 1. RAGIONAMENTO PRELIMINARE — *il difetto, e perche' oggi non si vede*

### ⛔⛔ **IL DIFETTO, ED E' MIO: L'HO INTRODOTTO IERI**

Per far girare `M-B1` dopo aver spostato `percorri_tick`, ho dichiarato
`VIAGGIANO = ("_misura_mb1.py", "tick.py")` — e `contro()` copia quei file
### **nell'albero vecchio, SEMPRE.**

> ### ⛔ **QUINDI IL <<PRIMA>> GIRA COL CICLO DEL PASSO DI OGGI.** `il_passo()` usa
> `TK.tick`, e `TK` e' ### **il `tick.py` di oggi, copiato dentro.**
> ### ⚠ **Oggi e' innocuo** perche' lo spostamento era ### **verbatim** *(provato al
> carattere)*: il passo di oggi e' ### **lo stesso** di quello di prima.
> ### ⛔⛔ **MA IL PUNTO `D` CAMBIERA' `tick.py`**, e da allora `M-B1` confronterebbe
> ### **il passo nuovo col passo nuovo** — cioe' ### **un FALSO-UNO**, e sarebbe
> ### **verde per costruzione.**

### ⭐ **E LA COSA CHE RENDE IL DIFETTO PERICOLOSO:** `M-B1` e' ### **il criterio** con cui
ho giustificato lo spostamento *(«`M-B1` AL BIT»)*, e con cui ogni mandato chiede di
provare che una cura ### **non ha mosso un bit.** ### **Un criterio che non puo' fallire
non e' un criterio.**

### 📌 **E IL GUARDIANO REGISTRA IL SUO ERRORE `n.6`**, che va nella RIPRESA: nel mandato
del `19:33` due premesse erano sbagliate *(i `default` nel nucleo *«gia' zero»*: erano
`3` in `grafo.py`; `energia.py` elencato nel nucleo: ### **nessuna radice lo importa**)*,
e le aveva prese ### **dal censimento PER NOME DI FILE senza derivare il nucleo.**
### ✅ **Le ho segnalate PRIMA del codice, e lui dice che era giusto.**

### ⭐ **CHE COSA CREDO, PRIMA DI GUARDARE**

| | credo che… | e ### **NON LO SO** |
|---|---|---|
| `a` | il passo si possa prendere ### **dall'albero in cui la misura gira**: `import tick` la' dentro trova ### **il `tick.py` di QUEL commit**, e dove non c'e' si cade su `deriva` | ### ⚠ **non so se `sys.path` lo garantisca:** `python primo_ordine/_misura_mb1.py` mette `primo_ordine/` ### **primo**, ma se lo mettesse dopo l'import prenderebbe un altro albero |
| `b` | gli ### **altri** strumenti che confrontano col *«prima»* siano ### **pochi** | ### **non so quanti**: `worktree` lo usa ### **solo `_misura_mb1.py`**, ma *«o simili»* include `git show <commit>:<file>` ### **piu' una corsa** |
| `c` | il caso che DEVE fallire costi ### **una corsa in piu'** | ### ⚠ **non so quanto duri un `contro()`**: se tre confronti sfondassero il budget, il collaudo va ### **`solo-CI`** e lo dico |

---

## 2. PROGETTAZIONE — *i passi, i criteri, e cosa mi FERMA*

| | il passo | il criterio |
|---|---|---|
| `1` | ### **nell'albero vecchio NON si copia MAI codice del passo**: `VIAGGIANO = ("_misura_mb1.py",)` | — |
| `2` | la misura ### **prende il passo dall'albero in cui gira**: `tick.py` se c'e', ### **altrimenti `deriva`** *(`DV.tick`, `DV.OPERATORE`)*, con il ramo ### **DICHIARATO** e il motivo scritto | il ramo si vede ### **in entrambi i versi**: `8c7b928` usa `tick.py`, `b150003` usa `deriva` |
| `3` | un ### **assert** che la misura ### **non DEFINISCE** nessuna funzione del passo *(`tick`, `percorri_tick`, `OPERATORE`)* | gira ### **a ogni confronto**, non solo nel collaudo |
| `4` | ### ⛔ **IL CASO CHE DEVE FALLIRE:** con un `tick.py` di oggi ### **MODIFICATO** *(un pezzo in ordine diverso, su una COPIA fuori dal repo)*, il confronto contro `8c7b928` ### **DEVE DIVERGERE** | ### **e col difetto di ieri PASSEREBBE**, e il braccio lo mostra ### **copiando il `tick.py` modificato anche nell'albero vecchio** |
| `5` | ### **il controllo positivo:** contro ### **`b150003`** *(PRIMA dello spostamento)* e contro ### **`8c7b928`**, `M-B1` resta ### **`12` su `12` AL BIT** | se uno dei due si muove, ### **STOP e relaziono** |
| `6` | il ### **censimento** degli altri strumenti che confrontano col *«prima»*, e ### **un braccio che lo tiene** | la lista e' ### **DICHIARATA**, e uno nuovo ### **fa fallire** invece di passare |

### ⛔⛔ **E IL BRACCIO DEL PUNTO `4` E' LA COSA CHE CONTA DI PIU' DEL PEZZO:** prova
### **che `M-B1` PUO' FALLIRE.** ### ⚠ **Finora non l'avevo mai provato** — e un criterio
di cui nessuno ha mostrato il fallimento ### **e' una promessa, non un presidio.**

---

## 3. TODO

1. `primo_ordine/_misura_mb1.py`: `VIAGGIANO` ridotto, il passo ### **dall'albero**,
   l'assert del punto `3`, e un `--collaudo` coi bracci `4`, `5`, `6`.
2. `primo_ordine/collauda.py`: il collaudo nella lista *(### **`solo-CI` se costa**)*.
3. il ### **censimento** degli strumenti che confrontano col *«prima»*, nella relazione.
4. l'### **errore `n.6` del guardiano** nella RIPRESA.
5. il referto, e la relazione coi numeri.
