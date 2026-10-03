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

## ⛔ **ANNOTAZIONE — DUE DIFETTI DI FORMA MIEI, e il primo e' una RECIDIVA**

### ⛔ **① LA LISTA DEI FILE NEL MESSAGGIO DI COMMIT ERA SCRITTA A MEMORIA, e due volte ha
OMESSO UN FILE.** `2ab4ce2` e `1d58764` dicono *<<FILE CAMBIATI, tutti>>* e ### **non elencano
`doc/INDICE_ID_ESCLUSI.tsv`**, che in entrambi i casi era nel commit.
### ➜ **La parola *<<tutti>>* in una lista scritta a memoria e' una promessa che non posso
mantenere**, e alla seconda volta non e' una distrazione: e' ### **un metodo sbagliato.**
### ✅ **DA ORA LA LISTA SI GENERA:** `git diff --cached --name-only`, e si incolla.
### ⚠ **E non e' un presidio** *(`A9`)*: nessun hook guarda la corrispondenza fra la lista nel
messaggio e i file nel commit. ### **E' una pratica, e come tale puo' essere violata di nuovo** —
la differenza e' che ora c'e' ### **un comando** al posto della memoria.

### ⚠ **② UN NUMERO DISCORDE FRA IL MESSAGGIO E IL REFERTO.** Il messaggio di `97fde1c`
dice ### **`numpy 2.3.3`**, il referto committato dice ### **`numpy 2.3.0`**.
### **Il referto ha ragione: quel numero lo stampa lo strumento, il messaggio l'ho scritto io.**
### 📌 **Ed e' `L-NUMERI` preso alla lettera** — *ogni numero scritto in un commit esce
da uno script* — ### **violato sul numero piu' innocuo che c'era.** Un numero ricopiato a mano
non ha provenienza anche quando e' quasi giusto.

## ⭐ **LE DECISIONI DI LUCA DEL 2026-10-03 (14:01), e il cancello si apre**

*(par.8: registrate ### **PRIMA del codice**. `ASSIOMI.md` non si tocca.)*

### ✅ **① LA FRAZIONE `t` VALE PER LA GEOMETRIA ***E*** LA FASE**

| | chi legge `t` |
|---|---|
| ### **la GEOMETRIA** | `pos` e `d`/`d0` nella divisione · `pos` e `dd` nello Schwinger |
| ### **la FASE** | `fm`, ### **in tutti e due i rami** *(con e senza `MITOSI_DIR`)* |

### ⛔ **E LE EREDITA' DI STATO *NON* LEGGONO `t`:** `psi` e `phivel` come ### **media**, la
famiglia dello ### **spinore** come ### **copia**, `rho_sel` del cancello dell'antifase.
### **Restano come sono**, e si decidono nella ### **LEGGE** di `DIVISIONE-AUTOCONSISTENTE`.
### 📌 **Quindi il censimento aveva ragione a tenerle in classi SEPARATE**, e la decisione
dice ### **quale classe entra nel `6a`**: solo `FRAZIONE`. Le altre tre no.

### ✅ **② `DIVISIONE-AUTOCONSISTENTE` SI DIVIDE IN DUE**

| | che cosa | quando |
|---|---|---|
| le ### **MISURE** | torsione persa alla divisione · verso dell'arco · `pos` contro `d` · calcio non simmetrico `a`/`b` | ### **subito dopo il `6b`** |
| la ### **LEGGE** | la frazione che il sistema SCEGLIE | ### **dopo la definizione dell'energia**, perche' ### **deve rispettare `A14`** |

### ⚠ **E il passaggio di consegne del guardiano su questo punto era INCOERENTE: vale questa
versione.** *(Lo scrivo perche' chi legge due versioni sappia quale.)*

## **I SEI SITI, e la forma e' DECISA: sempre CONVESSA, mai la lerp**

| riga | che cosa diventa |
|---|---|
| `:8499` | `pos_figlio = (1-t)*pos[a] + t*pos[b]` |
| `:8561` | `dh` ### **si sdoppia**: il blocco `a`–`m` vale ### **`t*d[sel]`**, il blocco `m`–`b` vale ### **`(1-t)*d[sel]`**. ### **L'ordine e' quello di `i = [keep, a, m]` e `d = [keep, dh, dh]`: il PRIMO blocco e' `t`** |
| `:8498` | `fm = phi[a] - t*D` |
| `:8496` | `fm = phi[a] - (t + bias)*D` — il `bias` resta uno ### **scostamento SOPRA `t`**, e il suo `0.5` di ampiezza a `:8495` ### **NON si tocca** |
| `:2344` | `pos` Schwinger `= (1-t)*pos[aa] + t*pos[bb]` |
| `:8701` | `dd` ### **si sdoppia**: il blocco `aa`–`k` vale `max(t*L, 0.05)`, il blocco `k`–`bb` vale `max((1-t)*L, 0.05)`, con `L = norm(pos[aa]-pos[bb])`. ### **L'ordine e' quello di `i = [.., aa, k]`** |

### 📌 **E `d0new` deriva dai DUE MEZZI, con lo stesso ordine**, e resta calcolato dai
valori ### **PRIMA** della chiamata a `_nasce` su `dh`, ### **come oggi.**

### ⚠ **`MITOSI_2LAM` e l'antifase NON si toccano. `SCHW-CORTI` SI DICHIARA, non si risolve.**

## ⛔ **`_fab` PER META', E SU *DUE* PERCORSI — errore del guardiano, dichiarato da lui**

Il suo rilievo copriva ### **solo `dh`**, ma ### **anche lo Schwinger passa `dd` a `_nasce` con
`md = 2, md0 = 2`.**

| il sito | `md`, `md0` | che cosa cambia |
|---|---|---|
| `dh` | `2, 0` → ### **`1, 0`** | ### **UNA sola chiamata** sull'array raddoppiato *(cosi' `_g_sm_nascite` non cambia)*, e `_sm_lun` = ### **somma della meta' `a` PIU' somma della meta' `b`** |
| `dd` | `2, 2` → ### **`1, 1`** | ### **idem** |
| `d0new` | `0, 1` | ### **RESTA com'e': somma unica su `2n`**, come oggi |

### ✅ **E PRIMA DI SCRIVERE SI VERIFICA DALL'ARITMETICA** che a `t = 0.5` tutti e
### **quattro** i contatori, per tutti e ### **tre** i siti, restino ### **identici al bit.**

## **I CRITERI DEL SIGILLO, fissati QUI e prima di girare**

| | che cosa |
|---|---|
| **`0`** | la patch committata, applicata al *prima* committato, da' ### **il blob di oggi** |
| **`A`** | ### **identico al byte** sulle tre scene del commit 4: ### **stato E contatori**, coi contatori ### **separati per nome e riportati**. ### ➕ **PIU' UNA QUARTA SCENA: la stessa argv SENZA `--mitosi-2lam`.** Si riportano `_sm_trd_mitosi`, `_sm_trd0_mitosi`, `_sm_trd_schwinger`, `_sm_trd0_schwinger` per ### **TUTTE** le scene. ### ⛔ **Nessuno puo' essere zero dappertutto**: un `_fab` sempre nullo rende ### **VUOTO** il braccio sui `_sm_lun`. ### **Se uno lo e': FERMATI e dillo.** |
| **`B`** | il censimento rigirato: ### **0 siti `FRAZIONE` col numero letterale**, ### **13 occorrenze invece di 19**, e tutte e sei le formule ### **leggono `t`**, dall'AST |
| **`C`** | una copia con ### **`t = 0.4`**, verificata ### **sui VALORI** e non sul *<<differisce>>*, al ### **primo evento di ciascun tipo**: `a`–`m` = `0.4*d` e `m`–`b` = `0.6*d` *(sui valori che entrano in `_nasce`, ### **prima del pavimento**)* · `aa`–`k` = `max(0.4*L, 0.05)` e `k`–`bb` = `max(0.6*L, 0.05)` · `pos = 0.6*pos[a] + 0.4*pos[b]` *(e lo stesso per `aa`/`bb`)* · `fm = phi[a] - 0.4*D` (mod) · `i`, `j` ### **coerenti coi blocchi** · `_sm_lun` di ogni sito ### **uguale alla somma a meta' calcolata in modo INDIPENDENTE dal sigillo** |
| **`C-bis`** | per ### **CIASCUNO dei sei siti**, una copia con `t = 0.4` in cui ### **QUEL sito resta al letterale `0.5`**. Deve essere scoperta ### **da `B`** *(con la riga)* e ### **da `C`** *(con la grandezza che manca)*. ### **Sei copie, sei bocciature: se anche una passa, il sigillo non discrimina.** |

### ⛔ **E SE UN CRITERIO FALLISCE: FERMARSI E RIPORTARE, non aggiustare il criterio.**

## 3. TODO DEL NEXT STEP

1. ☐ **committare e pushare QUESTO FILE** *(par.8: prima del lavoro)*
2. ☐ `csv/_test_fork/_censimento_punto_medio.py` + voce d'inventario, **committato**, poi girato
3. ☐ **il verdetto del censimento**: quattro o piu'? *(se piu', **STOP**)*
4. ☐ il **codice**: `t` dichiarato + i quattro lettori; `REGISTRO_FISICA`, `TABELLA_nascita`
   rigenerata, `CONTRATTO_nascita` se l'ordine cambia, inventario
5. ☐ il **sigillo** a cinque bracci *(`0`, `A`, `B`, `C`, `C-bis`)* e il **referto**
6. ☐ **STOP** — e il guardiano verifica

### ⚠ **E `MITOSI_2LAM` NON SI TOCCA: e' il `6b`.**

---

## **ANNOTAZIONE del 2026-10-03, dopo `5ec4ec5` — UN BUCO NEL BRACCIO `C`**

### ⚠ **Non riscrivo i criteri qui sopra** *(par.8: un ragionamento riscritto a posteriori e'
una ricostruzione, non un impegno)*. **Il criterio `C` come e' scritto sopra ERA GIUSTO; e'
stato il RINFORZO a bucarlo.**

**CHE COS'E' IL BUCO.** Il rinforzo del guardiano su `10034c6..e69682b` chiedeva — a ragione —
di far girare il ramo del `bias`, che con `MITOSI_DIR = 0` non gira mai; e la copia di `C` e'
diventata **una sola copia, con `--mitosi-dir=1.0`**. Conseguenza non vista:

> ### ⛔ **il ramo NORMALE `fm = (self.phi[a] - FRAZ_NASCITA * D) % self._dphi()`** *(`:8554`)*
> ### **non gira in NESSUNA copia che abbia la formula giusta.**

**E i tre bracci che sembravano coprirlo non lo coprono:**

| braccio | che cosa vede davvero | perche' NON basta |
|---|---|---|
| **`B`** | che la riga **legge `FRAZ_NASCITA`** | legge la costante **anche** se la combinazione e' `(1-t)` |
| **`C`** | i valori, ma **del ramo del `bias`** | il ramo normale **non viene eseguito** |
| **`C-bis`** | che il **letterale `0.5`** viene scoperto | prova che un letterale si scopre, ### **non che la formula sia giusta** |

### 📌 **LA FORMA DELL'ERRORE, e vale oltre questo caso:** *«il sito e' coperto»* e *«il sito
e' coperto SUI VALORI da una copia con la formula giusta»* sono **due cose diverse**, e il
referto non poteva distinguerle perche' **non riportava QUALE copia aveva verificato QUALE
sito**. Un braccio che non sa dire *chi ha verificato cosa* non sa nemmeno dire *cosa e'
rimasto fuori*. **E' della famiglia `FALSO-ZERO`: lo zero era garantito dall'insieme delle
copie, non dalla legge.**

### ✅ **DI CHI E' L'ERRORE: del guardiano, e lo dichiara lui** *(il rinforzo l'ha chiesto
lui)*. **Lo scrivo come tale perche' il reperto dica da quale decisione e' nato, non per
assegnare una colpa.**

### **I CRITERI NUOVI, fissati dal guardiano PRIMA di scrivere il codice**

| | che cosa |
|---|---|
| **`C0`** | una copia con **`--t=0.4` e `MITOSI_DIR = 0`** *(il valore del sorgente, **senza** `--mitosi-dir`)*, verificata **SUI VALORI** al primo evento di ciascun tipo come `C`: in particolare **`fm = phi[a] - 0.4*D` (mod `dphi`)** dallo scatto della chiamata che **produce** la nascita, e insieme `dh_a`, `dh_b`, `pos` e `dd` |
| **copertura** | il referto dice **per ciascun sito QUALE copia** (`C0` o `C1`) lo ha verificato sui valori, e **ogni sito deve averne almeno una**: **`fm` in `C0`**, **`fm_bias` in `C1`** |
| **rovescio** | **il controllo che PUO' fallire**: una copia con `t = 0.4` in cui il ramo normale e' scritto **`(1-t)*D`** deve essere **BOCCIATA da `C0`**. Opzione nuova della patch: **`--fm-rovescio`**, solo per questa copia |

### ⛔ **E UN MODO IN CUI IL CASO ROVESCIO PASSEREBBE PER FORTUNA, trovato collaudando la
patch prima di committarla:** se `D` fosse `~0`, allora `phi[a] - 0.4*D` e `phi[a] - 0.6*D`
**coinciderebbero** — la bocciatura ci sarebbe comunque, ma **non proverebbe niente sulla
formula**, e lo stesso vale per il confronto di `C0`. **Cura: `misura_valori` esporta
`_D_max` e il referto lo DICHIARA**, cosi' un `PASSA` con `D ~ 0` si vede invece di
nascondersi. *(E' la lezione del commit 6a ripetuta: uno zero su un insieme scelto da me non
e' uno zero sulla legge.)*

### **L'ORDINE, deciso dal guardiano** *(e il run era IN CORSO quando il rilievo e' arrivato:
va in coda, `L-UN-PROMPT`)*:

1. ☐ il run in corso finisce → **il suo referto si committa COSI' COM'E', senza toccarlo**
2. ☐ **poi** un commit con `C0` e il caso rovescio — **strumento committato PRIMA di girare** (par.5)
3. ☐ **poi** il run dei soli `C0` + rovescio, **dichiarato come COMPLEMENTO** del referto
   principale, e il suo referto nel commit dopo

### ⚠ **PERCHE' LE DUE PATCH SONO STATE SCRITTE NELLO SCRATCHPAD E NON NEL REPO:** il sigillo
invoca `_frazione_t_patch.py` **come sottoprocesso**, quindi durante il run e' un file **del
percorso in uso** — modificarlo violerebbe il par.5. **Sono state collaudate su COPIE** *(le
cinque sostituzioni attaccano, l'AST di entrambi i file passa, e nessuna docstring e' una
concatenazione** — la classe d'errore che ha ucciso il run precedente)*.

---

## **ANNOTAZIONE del 2026-10-03 — LA RIPARAZIONE DEGLI STRUMENTI, prima di rigirare**

**Il sigillo e' caduto su `B` e `C`, e il guardiano ha rimisurato `B` in modo indipendente**
con un censimento AST su `c18c9bf6`: **13 occorrenze, 0 siti `FRAZIONE` al letterale,
`FRAZ_NASCITA` letta in tutti e sei i siti.** ### **Quindi la cura e' buona e gli strumenti
no.** Questa annotazione fissa **che cosa riparo e perche'**, prima di toccare il codice.

### **LE SEI RIPARAZIONI, e ciascuna nasce da un difetto MISURATO**

| | riparazione | il difetto che la causa |
|---|---|---|
| **①** | `DICHIARATI` indicizzata per **`(funzione, testo normalizzato)`**, non per numero di riga | una cura che **sposta le righe** rendeva lo strumento **impossibile da far passare** |
| **②** | il sigillo controlla il **returncode di OGNI sottoprocesso** **e** confronta il **`blob_sim` di OGNI artefatto letto** col blob del file in esame | ha citato un json di `6d306976` dichiarando un fallimento su `c18c9bf6`: **un falso-UNO** |
| **③** | `SpiaValori` mette nel contesto **gli indici** `a`, `b` *(e `aa`, `bb`)* | `misura_valori` ricostruiva `fm` da `pm["phi"][cd["a"]]` e la chiave **non c'era** |
| **④** | il braccio **`C0`** *(`MITOSI_DIR = 0`)*, la **copertura per sito**, e **`--fm-rovescio`** | il ramo normale di `fm` **non girava in nessuna copia con la formula giusta** |
| **⑤** | la frase del braccio `A` e il **conteggio degli attributi anche all'ULTIMO passo** | *«ndarray e scalari di `__dict__`»* e' **falsa** da quando `stato()` confronta anche pickle, sparse e `rng` |
| **⑥** | l'intestazione dichiara **piattaforma, Python e numpy**, e che i conteggi valgono **per quella piattaforma** | il guardiano su Linux/numpy 2.5.3 misura `_sm_tr* = 16/14/6/6`; il mio referto su Windows/numpy 2.3.0 dice `14/12/4/4` |

### ⛔ **UN RILIEVO SULLA CHIAVE CHE IL MANDATO PROPONE, e va detto PRIMA di usarla:
`(funzione, testo normalizzato)` NON E' UNICA.** Misurato sulle 13 occorrenze di `c18c9bf6`:

```
:8568  mitosi  rho_sel = 0.5 * (I[a] + I[b])      # densita' d'interferenza sull'arco
:8735  mitosi  rho_sel = 0.5 * (I[a] + I[b])      # densita' d'interferenza sull'arco
```

**Stessa funzione, stesso testo** *(differiscono solo per lo spazio prima del commento, che
la normalizzazione collassa)*. ### ✅ **Cura: la tabella non mappa una chiave su UNA voce, ma
su una voce PIU' UNA MOLTEPLICITA'**, e lo strumento verifica **che il numero di occorrenze
per chiave sia ESATTAMENTE quello dichiarato.** ### **Una chiave trovata 1 volta invece di 2
fa FALLIRE lo strumento** — che e' il comportamento voluto: `rho_sel` compare **due volte**
*(ramo divisione e ramo Schwinger)*, e se una sparisse sarebbe un fatto, non un dettaglio.

### **E I SEI SITI CURATI DIVENTANO UN CONTROLLO POSITIVO.** Le sei voci `FRAZIONE` non si
cancellano dalla tabella: passano in **`CURATI`**, e lo strumento asserisce che siano trovate
### **ZERO volte**. ### 📌 **Cosi' il censimento non dice solo *«ci sono 13 occorrenze»*: dice
*«le sei che la cura ha tolto NON SONO TORNATE»*** — e una regressione che rimettesse un
`0.5` letterale **fallirebbe con il nome del sito**, non con un conteggio diverso.

### **I CRITERI DEL RUN, fissati qui**

1. il censimento, **dopo** la cura ①, su `c18c9bf6` deve dare **13 occorrenze** e **0
   `FRAZIONE`**; `_corsa.txt` **e** `_censimento.json` si rigenerano **come COPPIA dallo
   stesso blob** *(oggi nel repo sono **incoerenti**: `_corsa.txt` e' di `c18c9bf6`, il json
   di `6d306976` — ed e' la prova visibile del difetto ②)*;
2. l'output si cattura **INTERO** *(`tee` su file)*, **mai `| tail`**: l'intestazione coi blob
   **fa parte del referto**;
3. tutti i bracci **da capo**: `0`, `A`, `A-tr`, `B`, `C0`, `C1`, `C-bis`, **rovescio**;
4. ### ⛔ **se un criterio fallisce: FERMARSI E RIPORTARE, non aggiustare il criterio.**
