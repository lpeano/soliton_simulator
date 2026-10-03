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

### ⛔ **ANNOTAZIONE DEL 2026-10-03 — LA RIGA DI `_fab` QUI SOPRA E' SBAGLIATA**

*(rilievo del guardiano. **La tabella RESTA come l'ho scritta** — par.8: un ragionamento non si
riscrive quando si rivela sbagliato, **si ANNOTA con cio' che l'ha smentito.**)*

Avevo concluso che *<<tutti e quattro i numeri coincidono a `t = 0.5`>>*.
### **Vale per i TRE INTERI e NON per il FLOAT.**

| il contatore | tipo | coincide? |
|---|---|---|
| `_g_sm_nascite` | ### **intero** | ### **SI'** |
| `_sm_tr<q>_<sito>` | ### **intero** *(`md * ntr`)* | ### **SI'** |
| `_sm_vis<q>_<sito>` | ### **intero** *(`md * v.size`)* | ### **SI'** |
| ### **`_sm_lun<q>_<sito>`** | ### **FLOAT** *(`md * sum(LAM - v)` sui troncati)* | ### **NO** |

### **LA CAUSA E' L'ASSOCIATIVITA':** `np.sum` su `2n` elementi somma in un ordine *(con una
riduzione a coppie)* che ### **non e' `2 *` la somma su `n`**. ### **Gli interi non se ne
accorgono, i float SI'.**

### ✅ **RIMISURATO DA ME, con uno strumento committato** *(`csv/_test_fork/_somma_meta.py`,
blob `e1eb2c18`; 2000 prove per sette taglie, seme `20261003`)*:

| il confronto contro `2*np.sum(x)` | differenze |
|---|---|
| `np.sum(np.concatenate([x, x]))` | ### **4043 su 14000** |
| `np.sum(x) + np.sum(x)` | ### **0 su 14000** |

### ✅ **QUINDI LA FORMA CHE REGGE E' QUELLA CHE IL GUARDIANO INDICA:** `_fab` calcolata
### **PER META'** e poi sommata — `fab_a + fab_b`. A `t = 0.5` le due meta' sono
### **identiche**, quindi e' `s + s`, e ### **`s + s == 2*s` E' ESATTO** *(il raddoppio e' uno
scalamento per una potenza di due)*.

### ⚠ **E UN DETTAGLIO CHE VALE DA SE': a `n = 128` la forma concatenata NON diverge**
*(la somma a coppie di numpy allinea i blocchi)*. ### **Un test su UNA SOLA taglia avrebbe dato
un falso *<<identica>>*** — ed e' la stessa lezione di `FALSO-ZERO`. Per questo lo strumento
prova ### **sette** taglie.

### ⛔ **E IL BRACCIO `A` PASSEREBBE COMUNQUE, MA NON PROVEREBBE NIENTE SU `_fab`:** nelle tre
scene `MITOSI_2LAM` e' ### **acceso** *(dal driver)* e la mitosi ### **non tronca nulla**, quindi
`_fab` vale ### **zero da entrambe le parti**. ### ➜ **Il numero che lo dimostra e'
`_sm_trd_mitosi` sulle tre scene, e NON L'HO ANCORA MISURATO:** richiede un run, e il mandato dice
di fermarsi dopo il censimento. ### **Va nel referto del sigillo, e finche' non c'e' il braccio `A`
su `_fab` e' VACUO.**

### 📌 **E IL DIFETTO CONTA NEL `6b`, non qui:** con `t != 0.5` le due meta' sono
### **diverse**, e `t*d` puo' scendere ### **sotto `LAM`** anche con `d >= 2 LAM`
*(`0.4 * 1.6 = 0.64 < 0.8`)*. ### **Allora i troncamenti ci sono davvero, e `_fab` non e' piu'
zero.**

---

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

## ✅ **ANNOTAZIONE DEL 2026-10-03 — IL CENSIMENTO E' GIRATO, E IL CANCELLO E' SCATTATO**

*(par.8: si ANNOTA, non si riscrive.)*

| | |
|---|---|
| ### **il verdetto** | ### **5 coppie `(evento, grandezza)` su 6 siti**, non quattro |
| la quinta | ### **`DIVISIONE/fm` (la FASE del figlio)**, ai siti `:8496` e `:8498` |
| ### **lo stato del `6a`** | ### **FERMO**, in attesa della ### **decisione di Luca** — `DIVISIONE-AUTOCONSISTENTE` |

### **E L'ERRORE DEL MANDATO E' DICHIARATO DAL GUARDIANO:** aveva ricopiato *<<quattro
formule>>* dal piano, dove si parlava della ### **sola geometria.** ### **Il censimento resta il
CANCELLO, e il cancello ha fatto il suo lavoro.**

### ⚠ **E DUE COSE DEL MIO SETACCIO ERANO LENIENTI, entrambe nella direzione sbagliata:**
partiva dalle ### **FORME** *(17 siti, e non vedeva `(0.5 + bias) * D`)* → ora cerca
### **il NUMERO** *(19 siti)*; e il cancello contava i ### **NOMI** *(4 invece di 5, collassando
`pos` dei due eventi)* → ora conta le ### **COPPIE**.

### 📌 **E LA STORIA DI `:8489` CONTRO `:8495`/`:8496` STA QUI, non in un print:** il
guardiano aveva citato il ramo `MITOSI_DIR` con la riga del ### **CANCELLO** *(`if MITOSI_DIR !=
0.0`)*; le righe del ### **NUMERO**, misurate dall'AST, sono `:8495` *(l'ampiezza del bias)* e
`:8496` *(la frazione `(0.5 + bias)`)*. ### **La lista del guardiano nello strumento e' corretta
con le due righe giuste**, e con la lista corretta la differenza calcolata risulta
### **tutta `ALTRO`** — che e' il controllo che la correzione e' giusta.

## ✅ **ANNOTAZIONE — LO STATO DEI TODO**

| | il todo | stato |
|---|---|---|
| **1** | committare il task history prima del lavoro | ### **FATTO**: `621cfbd` |
| **2** | `csv/_test_fork/_censimento_punto_medio.py` + inventario, committato e girato | ### **FATTO**: `2ab4ce2`, curato in `47cda46`, referto in `97fde1c` |
| **3** | il verdetto del censimento: quattro o piu'? | ### **FATTO: CINQUE** → ### **STOP** |
| **4** | il codice | ### **NON FATTO, e non si fa:** il cancello e' scattato |
| **5** | il sigillo | ### **NON FATTO** |
| ### **+** | la misura di `_fab` | ### **FATTO**: `csv/_test_fork/_somma_meta.py`, `2ab4ce2` |
| ### **+** | l'eredita' da ### **UN SOLO genitore** *(un `t = 0` implicito)* | ### **FATTO**: pezzo nuovo del censimento |

## ⛔ **ANNOTAZIONE — IL VINCOLO PER IL CODICE FUTURO, e vale SOLO per un percorso**

> ### **La cura *<<`_fab` per meta'>>* tocca SOLO il percorso `dh`.**

`_nasce(d0new, 'mitosi', 0, 1)` somma ### **GIA' un array `2n` in UNA sola chiamata** — perche'
`d0new` e' ### **gia'** `concatenate([d0h, d0h])`, cioe' i due figli.
### ➜ **Quel percorso DEVE RESTARE COSI'**: spezzarlo in due somme
### **cambierebbe `_sm_lund0_mitosi`**, che e' lo stesso difetto di `_fab` ### **al rovescio.**

### 📌 **E il motivo per cui non e' simmetrico:** `dh` entra con `md = 2` *(una voce →
due archi di `d`)*, `d0new` con `md0 = 1` *(e' gia' raddoppiato)*. ### **La cura serve dove `md`
MOLTIPLICA una somma, non dove la somma e' gia' sull'array intero.**

## 3. TODO DEL NEXT STEP

1. ☐ **committare e pushare QUESTO FILE** *(par.8: prima del lavoro)*
2. ☐ `csv/_test_fork/_censimento_punto_medio.py` + voce d'inventario, **committato**, poi girato
3. ☐ **il verdetto del censimento**: quattro o piu'? *(se piu', **STOP**)*
4. ☐ il **codice**: `t` dichiarato + i quattro lettori; `REGISTRO_FISICA`, `TABELLA_nascita`
   rigenerata, `CONTRATTO_nascita` se l'ordine cambia, inventario
5. ☐ il **sigillo** a cinque bracci *(`0`, `A`, `B`, `C`, `C-bis`)* e il **referto**
6. ☐ **STOP** — e il guardiano verifica

### ⚠ **E `MITOSI_2LAM` NON SI TOCCA: e' il `6b`.**
