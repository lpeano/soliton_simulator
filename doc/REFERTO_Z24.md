# REFERTO — **`Z24`: i tre punti NON sono lo stesso schema.** E una mia conclusione precedente è SBAGLIATA

**Data:** 2026-09-18 · **Branch:** `fork-su2` · **Blob** `11cf103f` (byte grezzi) / `16ea0416` (git)
**Strumento:** `csv/_test_fork/_misura_Z24.py` · **Output:** `csv/_test_fork/_misura_Z24.txt`
**Mandato §5.2: STOP e riporta la tabella. Nessuna cura in questo referto.**

> ⚠ **Le righe del mandato (`:2082`, `:2294`, `:3154`) sono PRE-CURA e shiftate:** il docstring
> aggiunto a `_feedback_spinoriale_archi` ha spostato tutto ciò che sta dopo. Sul blob attuale
> valgono **`:2116`**, **`:2328`**, **`:3188`**. Trovate per NOME (par.0).

---

## 1. LA TABELLA DEI TRE — **e non sono lo stesso schema**

| punto | accumulo | è uno scambio? | gate | `\|sum\|/max\|·\|` | verdetto |
|---|---|---|---|---|---|
| **1 — `B`** `:2114-2116` | `+` su **entrambi** | **NO**: è una **media pesata** dei Bloch dei vicini, cioè un **campo** | — | `B` **33.0** | `sum(B)` **non ha ragione** di essere zero |
| **1b — `correzione = B×nb`** `:2289` | — | l'oggetto di cui parla MAPPA | — | **2.266** / MAX 5.512 | **CRICCHETTO — ma NON per il denominatore** (§2) |
| **2 — `_otw`** `:2326-2328` | `+` su **entrambi** | **NO**, e non è nemmeno una coppia: è un **incremento di ω** aggiunto direttamente | **`TW_SPINORE = False`** | — | **LATENTE**: si dichiara, non si corregge |
| **3 — `twist_nodo`** `:3186-3188` | **`+twn` / `−twn`** | **SÌ** | **`FRAME_DRAG = True`** | **6.756** / MAX 8.483 | **⚠ CRICCHETTO ATTIVO — è ESATTAMENTE `Z25`** |
| **3-controllo** — lo stesso, **nudo** | | | | **0.000e+00 ESATTO** | **la divisione è l'INTERA causa** |

### Il punto 3 è il ritrovamento

**`FRAME_DRAG = True` di default** (`:685`): questo termine **gira in ogni run mai fatto**.
Accumulo antisimmetrico (`+twn` a `i`, `−twn` a `j`), poi divisione per il **grado del nodo**.
Finisce in `coppia` → `delta_phivel / M_PH`, con **`M_PH = 1.0` uniforme**: quindi qui
**`sum = 0` È la conservazione**, esattamente come nel caso già curato.

**E il controllo lo dimostra senza margini: il nudo dà `0.000e+00` ESATTO.**

### Il punto 1 — **la cura di `Z25` NON si applica**, e la misura lo dimostra

| variante di `B` | `\|sum(correzione)\|/max` |
|---|---|
| divisione **+** riflessione *(attuale)* | **2.266** |
| **divisione**, senza riflessione | **2.622** |
| **senza** divisione, con riflessione | **6.507** |
| denominatore **d'arco** + riflessione | **3.060** |
| **senza divisione E senza riflessione** | **1.379e-15 ← EPSILON** |

**Due rotture INDIPENDENTI**, come `doc/MAPPA_accoppiamenti_spin.md` dichiarava in forma e nessuno
aveva misurato. **Togliere solo il denominatore PEGGIORA** (2.266 → 2.622), e un **denominatore
d'arco peggiora anch'esso** (3.060).

**La seconda rottura è `refl`** — l'asse `sigma_x` invece di `sigma_z` per i legami fra chiralità
uguali. Toglierla **non è una bonifica: è una legge nuova** (par.10), e non è questo giro.

**Punto 2: latente.** `TW_SPINORE = False` per decisione di Luca, e comunque non è uno scambio.

---

## 2. ⚠ UNA MIA CONCLUSIONE PRECEDENTE È SBAGLIATA, E VA RITIRATA

Nel referto `eaa402b` / `doc/REFERTO_semi_spin_feedback.md` / §9.39 ho scritto, più volte:

> *«il ~77 % dei nodi ha grado esattamente 2 … la domanda «|out| cresce col grado?» NON HA
> RISOLUZIONE su questo grafo»*

**È FALSO, ed è un errore di POPOLAZIONE — quello che A3 chiama per nome, fatto da me sul mio stesso
conteggio.** Il `1018` era su **5410 nodi-istanza**, e io l'ho diviso per **1318**, cioè per la somma
delle **sole colonne stampate** (gradi 2..9). **Un sottoinsieme.**

### La distribuzione vera (passo 60, seme 5, 549 nodi, 22044 archi)

```
grado:  min 2   MEDIA 80.3   MEDIANA 119   p90 119   MAX 122
   grado == 2   :  109 nodi  (19.85 %)      <- i neonati della mitosi
   grado >= 100 :  360 nodi  (65.57 %)      <- il bulk maturo
```

**È BIMODALE**, non concentrata a grado 2. E il mandato aveva ragione con il suo *«grado medio
~121»*: la mediana è **119**.

**Quindi la misura aveva eccome risoluzione — un fattore 60 di escursione — e io ho guardato dove
non ce n'era** (i bin 2..9 coprono il **21 %** dei nodi).

### Rifatta sul range giusto, la domanda HA una risposta

| variante | `\|out\|` a `g=2` | `\|out\|` a `g≥100` | rapporto | pendenza implicita |
|---|---|---|---|---|
| **attuale (pre-cura)** | 0.04885 | 0.04829 | **0.989** | **−0.003 → INTENSIVA** |
| **nudo (cablata)** | 0.001694 | 0.06127 | **36.2** | **+0.878 → ESTENSIVA** |
| media | 0.002333 | 0.04406 | 18.9 | +0.719 → ESTENSIVA |
| linea | 0.001372 | 0.02313 | 16.9 | +0.691 → ESTENSIVA |

*(Non è un fit: sono **due popolazioni reali** e il rapporto fra le loro mediane.)*

> **Il vecchio `/grado` RENDEVA `out` INTENSIVA — esattamente ciò che il docstring dichiarava, e
> ci riusciva. Nessuna delle tre cure lo fa.**

---

## 3. IL COMPROMESSO, ora che è misurato

**Conservazione e intensività sono in CONFLITTO DIRETTO, e la ragione è algebrica:**

- `sum(out) = 0` richiede un denominatore **simmetrico sull'arco** (o nessuno);
- l'indipendenza dal grado richiede un denominatore **del nodo che riceve**.

**Non possono valere insieme.** Il vecchio codice aveva scelto la seconda **rompendo la prima**, e
non lo diceva.

**Cosa cambia in concreto con `nudo`:** al bulk maturo `|out|` va `0.0483 → 0.0613` (+27 %), ma **ai
neonati va `0.0489 → 0.0017`, un fattore 29 in GIÙ**. Il termine smette di agire sui nodi appena
nati e agisce quasi solo sul bulk.

### Cosa NON cambia — e resta la ragione per cui la cura è giusta

**Un cricchetto è un difetto.** `sum(out) ≠ 0` significa che il termine **inietta coppia netta** con
un verso pilotato dalla topologia: non è una scelta di modello, è una violazione di A7. **La cura
resta giusta su quel punto**, e `G1` lo certifica a `6.5e-16`.

**Ma il costo NON era «non misurabile», come avevo scritto: è misurabile, ed è grande.**

---

## 4. COSA CHIEDO A LUCA — **due decisioni, non una**

1. **Il punto 3 va curato?** È lo stesso difetto di `Z25`, **attivo di default**, e il controllo
   nudo dà `0.000e+00` esatto: la cura è nota e certa. **Ma la scelta del denominatore eredita il
   compromesso di §3**, e va fatta sapendolo — non come l'ho fatta io, credendo che la domanda non
   avesse risposta.
2. **La scelta `nudo` per `SPIN_FEEDBACK` va riconsiderata?** Con i dati veri, `linea`
   (`g_i+g_j−2w`) è **la meno estensiva** delle tre (16.9× contro 36.2×) e ha l'ampiezza più
   contenuta. **Non lo propongo: lo riporto.** La cura attuale è committata e sigillata 12/12, e
   cambiarla è una decisione, non una correzione.

**Nessuna cura eseguita in questo referto. `SPIN_FEEDBACK` resta OFF. `Z9` non toccata.**

---

## 5. IL LIMITE DI §3 DEL MANDATO — **registrato, e la sua premessa va corretta**

Il mandato dice: *«non è misurabile su questo grafo (grado medio ~121) … serve una topologia a grado
basso o variabile per rispondere»*.

**Il grado medio è 80.3 e la mediana 119 — il mandato ha ragione sull'ordine.** Ma **la topologia a
grado variabile C'È GIÀ**: è bimodale, `2` contro `119`. **La domanda era misurabile, e adesso è
misurata** (§2). **Quel limite non è più aperto: è chiuso, e la risposta è nella tabella.**

Restano aperti gli altri limiti già dichiarati: **4 semi sono il minimo** (un effetto ≤ 1 % è
invisibile), **120 passi sono ~1/50 della maturazione di `ramp`** (`Z9`), **una sola scena**.

---

## 6. AGGIORNAMENTO 2026-09-18 — **il §3 del mandato era un errore, e si chiude**

La risposta di Luca accoglie il ritiro e **corregge il mandato**: il fronte che il §3 chiedeva di
aprire — *«serve una topologia a grado basso o variabile»* — **non esiste**, perché era costruito
sulla mia conclusione sbagliata. **La topologia a grado variabile c'è già** (bimodale, `2` contro
`119`, un fattore 60 di escursione), **la domanda era misurabile ed è misurata.**
**Registrato come errore del mandato**, non come fronte: voce `Z28`.

### ⚠ Una precisazione, perché la risposta può essere letta male

Luca scrive: *«il ~77 % di grado 2 e il grado medio ~121 non sono in contraddizione: sono due
statistiche diverse su una distribuzione a coda pesante»*.

**È vero in generale — ma non salva il mio numero.** Il `77 %` era **aritmeticamente sbagliato a
prescindere**: avevo diviso `1018` per **1318** (la somma delle sole colonne che avevo stampato,
`g=2..9`) invece che per **5410**. Il valore vero è **19.85 %**.

**Le due cose vanno tenute separate:**
1. una frazione alta a grado basso **può** coesistere con una media alta — vero, ed è la ragione per
   cui la contraddizione apparente non bastava a rilevare l'errore;
2. **la mia frazione era comunque errata**, e lo sarebbe stata anche su una distribuzione uniforme.

*(Lo scrivo perché fra sei mesi «non erano in contraddizione» potrebbe leggersi come «il 77 % andava
bene». Non andava bene.)*

### Il quarto errore di popolazione in due giorni

`rho_arco`/`median(I_nodi)` = **8830** · media-di-mediane **19 contro 4089** · **`A3c`** (un rapporto
contro un massimo) · **questo**.

**E questo è il più istruttivo, perché il denominatore sbagliato era visibile nella mia stessa
tabella:** le colonne erano `g=2..9`, e io le ho sommate **come se fossero il totale**.

> **PRESIDIO: quando si calcola una frazione, il denominatore si prende dalla POPOLAZIONE, mai dalla
> somma di ciò che si è scelto di stampare.**
