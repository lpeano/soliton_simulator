# REFERTO — **il veleno e `keep`: le derivate d'arco leggono UN ALTRO ARCO**

*Mandato di Luca, 2026-10-05.* `VELENO-ARCHI-KEEP`, **passo (1): la misura che conferma
la causa**. *Il simulatore **`0f060670`** non e' stato toccato.*
**Task history** *(committato PRIMA, `923e396`)*:
`doc/TASK_HISTORY/2026-10-05_veleno-archi-keep-misura.md`.
**Strumento** *(committato PRIMA di ogni uscita, `15545d5`)*: blob **`425b8d47`**,
`tracciato = True`, `dirty = False`. **Copia patchata:** `e6a69e7c`, **3 ancore**.

---

## IN TESTA, come il mandato chiede: **IL DIFETTO E' LATENTE, NON ATTIVO OGGI**

*(punto `(c)`: «se un lettore VIVO le legge DOPO la nascita nello stesso passo, il
difetto e' gia' attivo oggi: dichiaralo in testa al referto»)*

| derivata | chi la scrive | chi la legge | la voce |
|---|---|---|---|
| `_dt_e_ultimo` | `step` *(`:7365`, **voce 2**)* | `_fattore_tempo_arco` *(`:7154`)* e `decidi_divisione` *(`:8382`)* | ### **voce 3, ma PRIMA della nascita** |
| `_sin2_vir` | `__init__` *(`:3849`)* e `memoria_hebbiana_moto` *(`:9179`, **voce 5**)* | `step` *(**voce 2**, molti punti)* e `batch_condensazione` *(`:12474`–`:12476`)* | ### **voce 2; e `batch_condensazione` NON GIRA** |

### **LA CATENA, letta dall'AST:** `_fattore_tempo_arco` e' chiamata **solo** da
`decidi_divisione` *(`:8323`)*, che e' chiamata **solo** da `mitosi` *(`:8549`)* —
### **e `decidi_divisione` gira all'INIZIO di `mitosi`, PRIMA di `nascita`.**
E `batch_condensazione` e' chiamata **solo** sotto `if a.batch` *(`:13118`)*:
### **il driver usa `--test`, quindi quel ramo NON esegue.**

> ### ✅ **QUINDI OGGI NESSUN LETTORE VIVO LEGGE QUESTE DUE DERIVATE DOPO LA NASCITA**
> ### **nello stesso passo: il difetto e' LATENTE.**
> ### ⛔ **E DIVENTA ATTIVO CON LA CURA DI `TETTO-CAUSALE-TEMPO-COORDINATO` passo (2),**
> che vuole far leggere `dt_e` a `memoria_hebbiana_moto` — ### **voce 5, cioe' DOPO la
> nascita.** ### **E' per questo che questa voce viene prima.**

### ⚠ **E LO SCRIVO COME L'AVEVO PREVISTO, non come una scoperta:** il task history
diceva, **prima** di misurare, *«mi aspetto che il difetto sia LATENTE, non attivo — e se
mi sbagliassi sarebbe la notizia piu' importante del referto»*. ### **Non mi sono
sbagliato, e questo vale meno che se mi fossi sbagliato.**

## 1. L'IPOTESI E' CONFERMATA, e i due controlli passano

| | |
|---|--:|
| eventi di nascita registrati | **147** |
| di cui **divisione** / **schwinger** | **83** / **64** |
| archi confrontati **IN TOTALE** | **138 784 360** |
| elementi **diversi** in totale | **63 802 623** |
| ### `(positivo)` confronti in cui l'allineamento CORRETTO non da' zero | ### **0** |
| ### `(discrimina)` eventi **senza archi tolti** con differenze | ### **0** |
| ### la 1a posizione diversa **coincide col primo arco tolto** | ### **166 su 166** |

> ### ✅ **I DUE CONTROLLI PASSANO: il positivo da' ZERO, e le differenze compaiono
> ### SOLO dove ci sono archi tolti.**
> ### **E la prima posizione diversa coincide col primo arco tolto in 166 confronti su 166:**
> ### **non in media, in TUTTI.**

## 2. LA SEPARAZIONE FRA I DUE EVENTI, che e' la prova della causa

| | **divisione** *(usa `keep`)* | **schwinger** *(NON usa `keep`)* |
|---|--:|--:|
| eventi | **83** | **64** |
| archi **tolti** | **938** | ### **0** |
| archi **aggiunti** | 1876 *(da 2 a 64 per evento)* | 520 *(da 2 a 20)* |
| ### **copertura del veleno** | ### **`0.5000`** *(min = max)* | ### **`1.0000`** *(min = max)* |
| celle non finite / archi nuovi | 1876 / 3752 | 1040 / 1040 |
| confronti **con differenze** | ### **166 su 166** | ### **0 su 128** |
| elementi diversi su archi confrontati | **63 802 623 / 78 351 652 = 81.43%** | **0 / 60 432 708 = 0.00%** |

### ⛔ **LA COPERTURA NON E' UNA MEDIA: E' UN'IDENTITA'.** `min = max = `**`0.5000`** nella
divisione e `min = max = `**`1.0000`** nello Schwinger, su **294** misure in tutto.
### **Il veleno copre META' degli archi nuovi quando si toglie un arco, e TUTTI quando
non si toglie niente — e l'unica differenza fra i due casi e' `keep`.**

### 📌 **E IL CONTO TORNA ESATTAMENTE COME L'AVEVO SCRITTO PRIMA:** con `s` archi
divisi, tolti `s` e aggiunti `2s`, il veleno appende `(m+s) - m = s` celle `NaN` su `2s`
archi nuovi. ### **`aggiunti == 2 * tolti` in OGNI evento con archi tolti** *(verificato:
`1876 = 2 x 938`)*.

## 3. QUANTO E' GRANDE IL DANNO, per evento

| la frazione di archi CONSERVATI che legge il valore di un altro arco | |
|---|--:|
| minimo | `0.0117` |
| ### **mediana** | ### **`0.9306`** |
| massimo | `0.9965` |

### ⛔ **NELLA META' DEGLI EVENTI DI DIVISIONE, PIU' DEL 93% DEGLI ARCHI CONSERVATI
### LEGGE IL VALORE DI UN ALTRO ARCO.** E il minimo e' `0.0117`, cioe' ### **non esiste un
evento in cui il danno sia nullo** — esiste solo un evento in cui il primo arco tolto sta
### **vicino alla fine** dell'array.

**Il perche' e' geometrico, non statistico:** la prima posizione diversa e' **il primo
arco tolto**, e tutte le posizioni **dopo** di esso scalano. ### **Quindi la frazione
danneggiata e' `1 - primo_tolto/m`: dipende solo da DOVE cade l'arco tolto.**

**I primi eventi, per esteso:**

| passo | evento | `m_prima` | tolti | aggiunti | 1o tolto | diversi / confrontati |
|--:|---|--:|--:|--:|--:|--:|
| 42 | divisione | 471564 | 1 | 2 | 379571 | 91 992 / 471 563 |
| 50 | divisione | 471565 | 1 | 2 | 381842 | 89 722 / 471 564 |
| 65 | divisione | 471566 | 1 | 2 | 398285 | 73 280 / 471 565 |
| 66 | divisione | 471567 | 1 | 2 | 92616 | 378 950 / 471 566 |
| 69 | divisione | 471568 | 1 | 2 | 320721 | 150 846 / 471 567 |
| 70 | divisione | 471569 | 2 | 4 | 73528 | 398 039 / 471 567 |
| 70 | schwinger | 471571 | 0 | 2 | — | 0 / 471 571 |
| 71 | divisione | 471573 | 1 | 2 | 432947 | 38 625 / 471 572 |
| 72 | divisione | 471574 | 1 | 2 | 354776 | 116 797 / 471 573 |
| 73 | divisione | 471575 | 1 | 2 | 466057 | 5 517 / 471 574 |

## 4. I NODI: **il veleno dei nodi e' CORRETTO** *(punto `(d)`)*

| | |
|---|--:|
| eventi con la testa di `phi` verificata | **147** |
| eventi in cui la testa di `phi` **e' cambiata** | ### **0** |
| eventi in cui `n` **non** e' solo cresciuto | ### **0** |
| derivate di **NODO** con la testa cambiata | ### **0** |

### ✅ **I NODI SONO SOLO AGGIUNTI, mai tolti ne' riordinati**, su **147** eventi.
### **Quindi per i nodi l'allungamento in coda E' l'allineamento giusto, e il veleno dei
nodi non ha questo difetto.** ### **Il difetto e' SOLO degli archi, e la ragione e' che
solo gli archi si TOLGONO.**

## 5. LA COINCIDENZA COL REFERTO DEL TETTO CAUSALE, e non e' un caso

Il referto `eeb54be` misurava **166** verifiche con differenze, ed erano **esattamente**
quelle dei passi con una nascita. ### **Qui i confronti con differenze sono 166, e gli
eventi di divisione sono 83.**

> ### 📌 **`83` eventi di divisione x `2` derivate d'arco = `166` confronti.**
> ### **E li' erano `83` passi x `2` siti del tetto = `166`.** ### **Lo stesso numero,
> per la stessa ragione strutturale: un evento di divisione per passo.**

### **Quindi l'ipotesi che il referto del tetto causale lasciava APERTA — *«che
`_dt_e_ultimo` non sia ri-allineato dalla ristrutturazione degli archi che `mitosi`
fa»* — e' ora MISURATA.**

## 6. LE DUE VIE DI CURA, **riportate SENZA sceglierne una**

### ⛔ **LA CURA NON SI SCRIVE: la forma la decide Luca dopo questo referto.**

| | la via | il **conto delle leggi** *(`9-ter`)* |
|---|---|---|
| **`(i)`** | la nascita applica `keep` a **TUTTE** le derivate d'arco **prima** del veleno | ### **non aggiunge leggi: ne RIPARA una**, e **toglie un'eccezione** — oggi le colonne d'arco si riallineano e le derivate d'arco **no** |
| **`(ii)`** | chi deve leggere `dt_e` dopo la mitosi lo **RICALCOLA** da `r` invece di leggerlo | ### **aggiunge una SECONDA SCRITTURA della stessa legge** — ed e' cio' che il simulatore dichiara di non voler fare, **accanto a `_dt_e_ultimo`**: *«una seconda scrittura della stessa legge e' due leggi che possono divergere»* |

### ⚠ **E DUE COSE CHE LA MISURA DICE SULLE DUE VIE, e che non sono una scelta:**
`(a)` la via `(ii)` **cura un lettore**, e la misura ne ha contati **due** per
`_dt_e_ultimo` e **molti** per `_sin2_vir`: ### **non copre `_sin2_vir`, che ha lo stesso
difetto**; `(b)` la via `(i)` **cura la causa una volta** per tutte e **2** le derivate
d'arco. ### **E' un fatto sul PERIMETRO, non una preferenza.**

## 7. CHE COSA QUESTO REFERTO **NON** DICE

1. ### **Non propone una cura** e non ne sceglie una: **decisione di Luca**.
2. ### **Non dice che il difetto muova la dinamica OGGI:** dice che **nessun lettore vivo
   legge queste derivate dopo la nascita**, quindi e' **latente**. ### **La prova e'
   dall'AST, con i rami verificati** — non da un confronto di traiettorie.
3. ### **Non copre le derivate di NODO**, che risultano corrette **su questa traiettoria**
   *(`147` eventi)*: se un giorno un evento togliesse nodi, andrebbe rimisurato.
4. ### **Non e' un sigillo.** I criteri del sigillo della cura stanno nel task history,
   fissati **prima**, e comprendono il caso che **deve fallire**.

---

**Piattaforma:** python **3.13.2** / numpy **2.3.0** / Windows 11 / AMD64.
**Scena:** `nmasse = 3`, `sep = 6.1158` — **dall'argv** *(`H-P3`)* — seme `11`, **150 passi**.
**Le due derivate d'arco** *(`_dt_e_ultimo, _sin2_vir`)* ### **sono LETTE dal `REGISTRO_DERIVATE` del modulo,
non da un elenco dello strumento** — un elenco sarebbe una **seconda fonte**.

**Comandi, verbatim:**

```
python csv/_test_fork/_veleno_archi_keep.py --collaudo
python -u csv/_test_fork/_veleno_archi_keep.py --passi=150
```

### ✅ **E LO STRUMENTO STAMPA UN BATTITO PER PASSO** *(`150` battiti, con `n`, gli archi
e gli eventi)*: ### **una richiesta di stato LEGGE il passo invece di stimarlo** — era un
debito che avevo annotato io stesso sullo strumento del tetto causale.
