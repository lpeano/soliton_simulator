# `2-quater` — **`deriva.satura` MISURA LA VARIABILE DELLA LEGGE VECCHIA**

*(integrazione del guardiano del `2026-10-16`, verifica di `3bd2b75`. Base: `f70300c`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE**, come il punto `1` del mandato
> chiede: *«Prima del codice, nel task history: che cosa deve affermare il braccio di
> materialita' con la legge di OGGI, e che cosa garantisce il regime «globale» con `S3`»*.

---

## 1. RAGIONAMENTO PRELIMINARE — *e un SESTO caso che il censimento ha fatto uscire*

### ⭐⭐ **IL BRACCIO `(1)`: CHE COSA DEVE AFFERMARE OGGI**

`deriva.satura()` misura ### **`max_k |h_k / Lambda_k|`** — cioe'
### **la variabile della SATURAZIONE**, che dal `2026-10-15` ### **non e' piu'
nell'ordine.** ### **La legge che gira e' `CAMM-MATERIA-VUOTO`, e la sua variabile e'
### `x = rho/Lambda`.**

> ### ✅ **L'AFFERMAZIONE GIUSTA:** *«nel regime di misura ### **`x = rho/Lambda`** e' di
> ordine `1`»* — cioe' ### **c'e' materia abbastanza perche' il termine agisca**, e il
> numero si legge ### **sulla variabile della legge che gira.**
> ### ⛔ **E il controllo NON deve sapere QUALE legge gira:** il flusso ### **si legge
> dall'ordine di composizione** *(come `statica_protocollo` dopo `371731f`)*, e se non e'
> quello che il controllo sa misurare ### **ALZA.**

### ⭐⭐ **IL BRACCIO `(1-bis)`: IL REGIME <<GLOBALE>> NON E' VACUO CON `S3`**

L'affermazione di ieri — *«il regime `globale` E' quello vacuo: la' `G ~ x^3/3 ~ 0`»* —
### **e' FALSA con `S3`, e il conto lo dice.** A `x = 0.03289` *(il `x_max` del regime
globale, misurato)*:

| | la saturazione *(`b(x)`)* | `S3` *(`beta = -x/(1+x)`)* | rapporto |
|---|---|---|---|
| `x = 0.03289` | `-2.368846e-05` | ### **`-3.184269e-02`** | ### **`1344`** |
| `x = 0.10000` | `-6.587515e-04` | `-9.090909e-02` | `138` |
| `x = 0.97000` | `-2.704028e-01` | `-4.923858e-01` | `1.8` |

### ⛔ **Cioe' a `x` piccolo `S3` e' MILLE VOLTE PIU' GRANDE della saturazione**, perche'
`beta ~ -x` e' ### **LINEARE** dove `b ~ -x^3/3` e' ### **CUBICA.**
### ⚠ **E `alpha` va nella direzione opposta:** a `x = 0.03289` vale ### **`-2.4788`**
*(diverge come `ln x`)*, dove `G'` della saturazione vale `1.08e-03`.

> ### ✅ **L'AFFERMAZIONE GIUSTA, e si misura:** *«nel regime `globale` il termine
> ### **NON e' spento**: `beta` e' ### **lineare** in `x` e vale `~1e-2`, cioe'
> ### **tre ordini di grandezza** sopra quello che la saturazione dava la'»*.
> ### ⛔ **Quindi `(1-bis)` NON si riscrive con una banda adattata: si CAPOVOLGE**, e il
> numero che la giustifica e' ### **il rapporto `1344`.**
> ### 📌 **E il motivo per cui il braccio serve ancora:** diceva *«qui il termine e'
> spento, quindi una misura fatta qui sarebbe un FALSO-ZERO»*. ### **Con `S3` quel
> pericolo NON C'E' PIU'**, e il braccio diventa ### **la prova che non c'e'.**

### ⛔⛔ **E IL SESTO CASO, che il censimento ha fatto uscire e che il mandato non
nominava:** `deriva.sorgente_per_nodo` ### **applica
`mot.operatori["CAMM-SATURAZIONE"]` A MANO** *(riga `~396`)*, e poi fa `CM.ORDINE[1:]` —
che ### **contiene `CAMM-MATERIA-VUOTO` alla posizione `11`.**

> ### ⛔ **Quindi quella misura applica MEZZA SATURAZIONE + i pezzi lineari + MEZZO
> MATERIA-VUOTO: un passo che non e' NESSUNA delle due leggi.**
> ### ⚠⚠ **E i numeri del braccio `(6)` di `3bd2b75`** *(esponenti `0.8436` e `0.9891`)*
> ### **sono misurati su QUEL passo misto**: ### **vanno RIMISURATI**, e il verdetto di
> allora non si puo' tenere come se fosse della legge che gira.
> ### ✅ **La cura e' la stessa: `id` e `frazione` SI LEGGONO da `CM.ORDINE[0]`**, e il
> controllo ### **ALZA** se quel posto non e' un `flusso`.

---

## 2. PROGETTAZIONE — *i passi, i criteri, e cosa mi FERMA*

| | il passo | il criterio, e cosa mi FERMA |
|---|---|---|
| `1` | `deriva.satura` legge ### **`rho/Lambda`** *(il flusso dall'ordine, e ALZA se non lo conosce)* | se il flusso nell'ordine non e' `CAMM-MATERIA-VUOTO`: ### **ALZA**, e lo dico |
| `2` | `deriva.sorgente_per_nodo` applica ### **`CM.ORDINE[0]`**, non un id a mano | — |
| `3` | il braccio `(1)` sulla variabile GIUSTA | `x >= 0.10` *(la banda di prima, `X_MINIMO`, NON si tocca)* |
| `4` | il braccio `(1-bis)` ### **CAPOVOLTO**: nel regime globale il termine ### **NON e' spento** | `|beta|` la' ### **`> 1e-2`**, e il rapporto con la saturazione ### **`> 100`** |
| `5` | il braccio `(6)` ### **RIMISURATO** sul passo giusto | l'esponente in ### **`[0.75, 1.25]`**, la banda del task history di `B`: ### **se ne esce, il braccio si RITIRA col motivo** |
| `6` | i ### **tre casi che devono fallire** del mandato | se uno non fallisce, il braccio e' ### **vacuo** e lo dico |

### **I TRE CASI CHE DEVONO FALLIRE, come il mandato li chiede:**
### ① **`rho = 0` su tutti i nodi** *(nessuna materia)* ⟹ il braccio `(1)` ### **deve
fallire**; ### ② **la variabile VECCHIA `|h|/Lambda` su uno stato a `h = 0` ma `rho > 0`**
*(spinori a elicita' nulla)* ⟹ il controllo vecchio direbbe ### **<<nessuna materia>>**,
ed e' ### **la prova che la variabile vecchia era sbagliata**; ### ③ un flusso
nell'ordine che il controllo ### **non sa misurare** ⟹ ### **ALZA.**

### ⛔ **E NESSUNA BANDA SI ADATTA:** `X_MINIMO` resta `0.10` e la banda dell'esponente
resta `[0.75, 1.25]`. ### **Se un numero ne esce, si riporta e si ritira il braccio.**

---

## 3. TODO

1. `deriva.py`: `satura` su `rho/Lambda` col flusso ### **dall'ordine**;
   `sorgente_per_nodo` su `CM.ORDINE[0]`; la tabella di `corri` *(`x_max`, `x_med`)* sulla
   variabile giusta; e la prosa che dice `x^3/3` ### **corretta o ritirata.**
2. `_collauda_deriva.py`: `(1)`, `(1-bis)` e `(6)`, coi tre casi che devono fallire.
3. il **CENSIMENTO** *(`43` coppie file/simbolo su `22` file)* classificato
   ### **LEGITTIMO** o ### **SCADUTO**, in tabella nella relazione.
4. la suite: ### **`53` ok, `0` rossi**, e i numeri nuovi del `(6)`.
