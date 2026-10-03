# `COMMIT 6a` DEL RIORDINO — **LA FRAZIONE `t` ESPLICITA, `t = 0.5`, IN UN SOLO POSTO**

*(mandato del guardiano, 2026-10-03; `doc/PIANO_riordino_mitosi.md` par. «Come la struttura si
prepara». **Un commit alla volta: STOP dopo il referto del sigillo.**)*

> ### **Oggi il *<<punto medio>>* e' scritto in QUATTRO formule indipendenti che per caso dicono
> ### tutte *<<meta'>>*. Diventano UN valore dichiarato, `t = 0.5`, letto da tutte e quattro.**
> Il figlio sta a **`t·d` da `a`** e a **`(1−t)·d` da `b`**, e ### **lo STESSO `t`** vale per
> **dove nasce** *(`pos`)* e per **quanto sono lunghi i nuovi archi** *(`d`, `d0`)*.

### ⚠ **NON si decide qui quale grandezza sceglierà `t`:** e' `DIVISIONE-AUTOCONSISTENTE`,
decisione di Luca. ### **E `MITOSI_2LAM` NON si tocca:** la forma generale `t·d >= LAM` e
`(1−t)·d >= LAM` e' il **`6b`**.

---

## ⚠ **CIO' CHE HO GIA' GUARDATO PRIMA DI SCRIVERE QUESTO FILE**

**Lo dichiaro invece di far finta che il ragionamento sia tutto a priori** *(par.8)*. Ho letto
**dal disco**: il par. del piano, i quattro siti *(`pos_figlio`, `dh`, `_rn_sch_pos`, il `dd` dello
Schwinger)*, il ramo `d0new`/`d0h`, e ### **`_nasce` per intero, contatori compresi.**
### **Tre cose trovate li' VINCOLANO il disegno**, e stanno sotto.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

1. i quattro siti sono **formule separate** che valgono `0.5` per **coincidenza storica**, non per
   una legge;
2. con `t = 0.5` ### **non cambia un bit**: e' un riordino, non una cura;
3. mi aspetto che la cosa difficile sia ### **la FORMA della formula**, non il valore.

### ⛔ **COSA NON SO, prima di guardare:**

- se i siti sono ### **esattamente quattro** *(il mandato dice: se sono di piu', **fermati**)*;
- se `(1−t)·x + t·y` e' ### **identica al bit** a `0.5·(x+y)`;
- se sdoppiare `dh` in `t·d` e `(1−t)·d` ### **tocca i contatori** di `_nasce`.

---

## ⛔ **1-bis. LE TRE COSE CHE VINCOLANO IL DISEGNO**

### ① **I CONTATORI DI `_nasce` DECIDONO LA FORMA DEL CODICE, non io**

`_nasce(v, dove, md, md0)` fa `_g_sm_nascite += 1` *(### **conta le INVOCAZIONI**)* e poi, per
ogni grandezza, `_m * _fab`, `_m * _ntr`, `_m * v.size`.

### ➜ **Quindi DUE chiamate al posto di una romperebbero `_g_sm_nascite`** — e il criterio `(A)`
dice **contatori compresi.**

### ✅ **LA FORMA CHE REGGE, e si verifica dall'aritmetica del codice:** ### **UNA sola chiamata**,
su un array ### **gia' raddoppiato**, con `md` dimezzato:

| | oggi | col `6a` |
|---|---|---|
| `dh` | `_nasce(dh, 'mitosi', **2**, 0)`, `v.size = n` | `_nasce(concatenate([t·d, (1−t)·d]), 'mitosi', **1**, 0)`, `v.size = 2n` |
| `_ntr` | `2 · ntr(n)` | `1 · ntr(2n)` = ### **`2 · ntr(n)`** a `t = 0.5` *(le due meta' sono identiche)* |
| `_fab` | `2 · fab(n)` | ### **`2 · fab(n)`**, stessa ragione |
| `vis` | `2 · n` | ### **`2n`** |
| `_g_sm_nascite` | `+1` | ### **`+1`** |

### ⭐ ② **LA FORMA DELL'INTERPOLAZIONE NON E' COSMETICA, ED E' MISURATA**

Su **2 milioni** di coppie di `float64` casuali, contro `0.5·(x+y)`:

| la forma | identica al bit? | differenze |
|---|---|---|
| ### **`(1−t)·x + t·y`** | ### **SI'** | ### **0 su 2 000 000** |
| `x + t·(y−x)` *(lerp)* | ### **NO** | ### **576 135 su 2 000 000** *(29 %)* |
| `t·d` contro `d/2` | ### **SI'** | 0 |

### ➜ **Scegliere la forma lerp avrebbe fatto FALLIRE il braccio `A`, e sarebbe sembrato un
difetto del riordino invece di una scelta di scrittura.** ### **Misurato PRIMA di scrivere il
codice.**

### ③ **`d0h` NON E' UN QUINTO SITO**

`d0h = dh · (1 + fattore_plastico)` ### **deriva da `dh`**: non e' una formula di punto medio.
Col `6a` diventa `d0h_a` e `d0h_b` dai due `dh`, e `d0new = concatenate([d0h_a, d0h_b])` — la
### **stessa dimensione**, quindi `_nasce(d0new, 'mitosi', 0, 1)` ### **non cambia.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### **PASSO 1 — IL CENSIMENTO, prima del codice.** Uno strumento committato che trova
### **dall'AST** ogni formula di punto medio nel perimetro della nascita — `0.5*(x+y)`,
`(x+y)/2`, `x*0.5`, ### **e `x/2`**, che il mandato non elenca ma e' ### **la forma del sito
`dh`** *(`self.d[sel] / 2`)*.
### **COSA DECIDE:** se i siti sono ### **piu' di quattro**, ### **si FERMA** e lo dico.
### **I quattro che mi aspetto:** `pos_figlio` *(prep. di `mitosi`)*, `dh` *(prep.)*,
`_rn_sch_pos` *(regola)*, il `dd` dello Schwinger *(ramo)*.

### **PASSO 2 — IL CODICE.** Una costante di modulo ### **dichiarata una volta**, letta dai quattro
siti. ### **Nessun flag:** `t` non e' un'opzione, e' ### **un valore della legge** *(un flag
rifarebbe il difetto `E4-LAM`)*.

### ⚠ **E DUE COSE SI DICHIARANO, NON SI RISOLVONO:**

| | |
|---|---|
| ### **`SCHW-CORTI`** | nello Schwinger la lunghezza viene da ### **`pos`** *(`norm(pos[aa]−pos[bb])/2`)*, nella divisione da ### **`d`**. Il `6a` mette `t` in ### **entrambe senza cambiare la sorgente**, e lo SCRIVE |
| il pavimento ### **`0.05`** | sta ### **dentro** la formula dello Schwinger *(`np.maximum(…, 0.05)`)*. E' un `A11`, ### **non mio in 6a** |

### **PASSO 3 — IL SIGILLO**, coi criteri **del mandato** piu' il braccio `0`:

| | braccio | che cosa decide |
|---|---|---|
| **`0`** | la patch committata applicata al *prima* da' ### **il blob di oggi** | la cura e' ### **recuperabile per costruzione** *(par.7)* |
| **`A`** | ### **BYTE-IDENTICO** sulle tre scene del commit 4, ### **grandezze E contatori** | e' un riordino |
| **`B`** | ### **dall'AST**: nessun `0.5` letterale resta nelle formule censite, ### **tutte leggono `t`** | il valore e' davvero in **un solo posto** |
| **`C`** | una copia con ### **`t = 0.4`** deve differire nelle ### **QUATTRO** grandezze, e il referto ### **le nomina tutte e quattro** | `t` arriva davvero a tutti e quattro |
| **`C-bis`** | una seconda copia dove ### **UNA sola formula resta a `0.5` letterale** con `t = 0.4` deve essere ### **SCOPERTA da `(B)` e dalla differenza MANCANTE in `(C)`** | ### **il controllo del controllo**: prova che `C` sa accorgersi di un sito sfuggito |

### ⛔ **COSA MI FAREBBE FERMARE:**

1. il censimento trova ### **piu' di quattro** siti → **mi fermo e lo dico**, come dice il mandato;
2. il braccio `A` ### **non** e' byte-identico → non e' un riordino, e va capito **prima** di
   proseguire;
3. un contatore di `_nasce` cambia → la forma del punto ① e' sbagliata;
4. il braccio `C` con `t = 0.4` ### **non** nomina tutte e quattro → `t` **non** arriva dove deve;
5. il `C-bis` ### **non scopre** il sito lasciato a `0.5` → ### **il braccio `C` non discrimina**,
   e il sigillo non prova quello che dice.

---

## 3. TODO DEL NEXT STEP

1. ☐ **committare e pushare QUESTO FILE** *(par.8: prima del lavoro)*
2. ☐ `csv/_test_fork/_censimento_punto_medio.py` + voce d'inventario, **committato**, poi girato
3. ☐ **il verdetto del censimento**: quattro o piu'? *(se piu', **STOP**)*
4. ☐ il **codice**: `t` dichiarato + i quattro lettori; `REGISTRO_FISICA`, `TABELLA_nascita`
   rigenerata, `CONTRATTO_nascita` se l'ordine cambia, inventario
5. ☐ il **sigillo** a cinque bracci *(`0`, `A`, `B`, `C`, `C-bis`)* e il **referto**
6. ☐ **STOP** — e il guardiano verifica

### ⚠ **E `MITOSI_2LAM` NON SI TOCCA: e' il `6b`.**
