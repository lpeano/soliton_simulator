# REFERTO — **le tre misure del 2026-10-01, rigirate su `0f060670`** *(punto 1)*

**Mandato di Luca, 2026-10-04.** Rigirare `_misure_calore --passi=72`,
`_pos_contro_d --passi=1` e `_verso_archi --passi=1` **dai blob committati e senza
modificarli** sul simulatore di oggi, e riportare **vecchio contro nuovo** grandezza per
grandezza, con **la causa piu' probabile** fra i commit del riordino per cio' che cambia.

> ### ⛔ **CRITERIO FISSATO DAL MANDATO: E' UN CONFRONTO, NON UN SIGILLO.**
> ### **Nessun `PASSA`, nessun `FALLISCE`: numeri e cause.**

## ⛔ ERRORE DEL GUARDIANO, dichiarato perche' il mandato lo chiede

Il guardiano aveva presentato a Luca **`M1`, `M2`, `M5` e `M4` come lavoro da fare.**
### **Sono gia' fatte dal 2026-10-01**, sul blob `287154f3`, coi referti in
`csv/_test_fork/_misure_calore/`, `_verso_archi/` e `_pos_contro_d/`.
### **Il buco vero e' un altro, ed e' il punto 2 del mandato: il calcio sotto lo scambio
`a<->b`, ISOLATO.**

## IL VERDETTO IN TRE RIGHE

| strumento | che cosa misura | foglie identiche | cambiate |
|---|---|--:|--:|
| **`_misure_calore`** *(72 passi)* | la **dinamica**: energia, calore, torsione | **3043** | **1** |
| **`_verso_archi`** *(1 passo)* | lo **specchio** degli archi | **279** | **1** |
| **`_pos_contro_d`** *(censimento AST)* | **chi legge** `pos`, `d`, `d0` | **129** | **35** |

> ### ✅ **LE DUE MISURE DINAMICHE SONO IDENTICHE, E L'UNICA FOGLIA CAMBIATA IN
> ### CIASCUNA E' `blob_sim_sha1_byte`: il timbro del referto stesso.**
> **3043 foglie su 3044** in `_misure_calore`, **279 su 280** in `_verso_archi`.

### 📌 **E QUESTO E' IL RISULTATO CHE CONTA, perche' TREDICI commit hanno toccato
### il simulatore fra i due blob.** Fra loro `COMMIT 3` *(la nascita e' un evento unico)*,
`COMMIT 4` *(il veleno alle derivate)*, `COMMIT 5` *(`perc_geom` derivato)*, `COMMIT 6a`
*(la frazione dichiarata una volta)*, la **correzione del bug** della quarta consumatrice
di `dd`, e `COMMIT 6b` *(il cancello che diventa legge)*.
### **Su 72 passi di dinamica, con i flag a default, NESSUNA grandezza misurata cambia.**

## 1. LA PIATTAFORMA, e un limite che va detto PRIMA dei numeri

| | |
|---|---|
| **oggi** | python **3.13.2** / numpy **2.3.0** / Windows 11 / AMD64 |
| **il 2026-10-01** | ### ⚠ **NON DICHIARATA: nessuno dei tre referti ha un campo per la piattaforma** |

### ⚠ **QUINDI, PER LE GRANDEZZE SENSIBILI ALLA PIATTAFORMA, UNO SCARTO NON SI
### POTREBBE ATTRIBUIRE AL SIMULATORE** — e la stella polare documenta che i **conteggi
assoluti** lo sono *(`16/14/6/6` su Linux/numpy 2.5.3 contro `14/12/4/4` su Windows/numpy
2.3.0)*. Lo strumento del confronto **verifica** l'assenza del campo e la **stampa**.

### ✅ **MA IN QUESTO CASO IL LIMITE NON MORDE, e si vede dal risultato:** le due misure
dinamiche sono **identiche**. ### **Un limite che renderebbe ambiguo uno SCARTO non rende
ambigua un'IDENTITA'** — se la piattaforma fosse cambiata in modo rilevante, i conteggi
sarebbero cambiati. *(L'inverso non vale: l'identita' non prova che la piattaforma sia la
stessa, prova che non ha spostato queste grandezze.)*

## 2. `_misure_calore` — 72 passi, **3043 foglie su 3044 identiche**

**L'unica foglia cambiata:** `blob_sim_sha1_byte`, cioe' **il timbro del blob**, che DEVE
cambiare. Le **4** liste di scalari sono **identiche come insieme**.

**Che cosa questo copre**, perche' <<3043 foglie>> non dice niente da solo: le **72** voci
per passo di `M1`, i sei conteggi di `M3` *(`xi_frena`, `xi_rifornisce`, `xi_nullo`,
`xi_al_clip`, `xi_min`)*, `M4` *(per passo, voci di mitosi, calcio attorno alla voce)*,
`M6` *(`d_K_fase` mediano e somma, `d_S_tw`)*, l'**attribuzione alle 8 voci**, e il
**primo** e l'**ultimo confine di voce**.

### 📌 **E LA SPIEGAZIONE DELL'IDENTITA' NON E' <<nessun commit faceva niente>>:**
il `COMMIT 6b` ha reso **legge** il cancello `FRAZ_NASCITA*d >= LAM` e
`(1-FRAZ_NASCITA)*d >= LAM`, e a **`FRAZ_NASCITA = 0.5`** *(il default)* quella condizione
e' **`0.5*d >= LAM`**, che in IEEE-754 e' **esattamente** `d >= 2*LAM` *(il fattore e' una
potenza di due: nessun arrotondamento)*. ### **Il 6b e' byte-inerte alla frazione di
default, e questo referto lo CONFERMA su 72 passi di dinamica** — che e' un controllo
indipendente da quello del suo sigillo.

## 3. `_verso_archi` — un passo, **279 foglie su 280 identiche**

**L'unica foglia cambiata e' il timbro del blob.** Le **2** liste di scalari sono identiche
come insieme. Il verdetto `il_verso_entra_nella_fisica` resta **`True`**, le **7**
differenze per nodo restano **7**.

> ### ⛔ **E QUESTO REFERTO DICHIARA DA SE' IL BUCO CHE IL PUNTO 2 DEVE COPRIRE:**
> a un passo le nascite sono **ZERO** in **entrambi** i rami *(`_g_nati_mitosi = 0`,
> `_g_nati_schwinger = 0`, `n = 12802`)*, vecchio e nuovo identici.
> ### **Con zero nascite il calcio della mitosi NON HA AGITO**, e le 7 differenze per nodo
> **non gli si possono attribuire.**

### ⚠ **E C'E' UN SECONDO MOTIVO per cui questa misura non isola il calcio, oltre alle
### zero nascite:** invertire **TUTTI** gli archi mescola `memoria_hebbiana_moto` — che
l'attribuzione di `_misure_calore` mostra attiva *(`sum d_Q2 = +3.8423e+05`, l'unica voce
che muove `Q2` oltre a `step` e `chiudi`)* — **con la mitosi**.
### **Il punto 2 inverte SOLO gli archi selezionati per la divisione, e solo quelli.**

## 4. `_pos_contro_d` — **35 cambiate per INDICE, e zero elementi TOLTI**

Questa e' l'unica delle tre che cambia, ed e' un **censimento AST**: *quali funzioni
leggono e scrivono `pos`, `d`, `d0`*. ### **Il codice e' stato rifattorizzato, quindi la
lista dei lettori cambia: e' atteso, non e' una deriva numerica.**

### ⛔ **MA IL NUMERO `35` E' FUORVIANTE, ED ERA UN DIFETTO DEL MIO COMPARATORE.**
Confrontava le liste **solo per indice**: un elemento **inserito** in una lista ordinata
**sposta ogni indice successivo**, e ogni spostamento contava come un *cambio*.
**Curato in `a043549`** con un confronto a **multinsiemi**, e il quadro vero e' questo:

| lista | prima | dopo | **aggiunti** | **tolti** |
|---|--:|--:|---|---|
| `statica.d.funzioni_legge` | 11 | 12 | decidi_divisione | **nessuno** |
| `statica.d.funzioni_non_legge` | 6 | 8 | _rn_div_d, _rn_sch_d | **nessuno** |
| `statica.d0.funzioni_legge` | 9 | 10 | decidi_divisione | **nessuno** |
| `statica.d0.funzioni_non_legge` | 6 | 8 | _rn_div_d0, _rn_sch_d0 | **nessuno** |
| `statica.pos.funzioni_non_legge` | 15 | 17 | _rn_div_pos, _rn_sch_pos | **nessuno** |

> ### ✅ **IN NESSUNA LISTA E' STATO TOLTO UN ELEMENTO.** Le `35` <<cambiate>> sono
> **quattro nomi nuovi** che spostano gli indici: `decidi_divisione`, `_rn_div_*`,
> `_rn_sch_*`.

### **LA CAUSA, letta da git e non supposta** *(`P1`)*: per ogni nome ho cercato il **primo**
commit del simulatore che lo contiene.

| nome nuovo | nasce in | il commit |
|---|---|---|
| `decidi_divisione` | **`2f129ba`** *(2026-10-01)* | *COMMIT 2 del riordino: la **DECISIONE** separata dall'**ESECUZIONE*** |
| `_rn_div_d`, `_rn_sch_d`, `_rn_div_d0`, `_rn_sch_d0`, `_rn_div_pos`, `_rn_sch_pos` | **`ff62420`** *(2026-10-02)* | *COMMIT 3 DEL RIORDINO: **LA NASCITA E' UN EVENTO UNICO*** |

## 5. LA PROVA CHE NON E' UN CAMBIO MA UN **TRASLOCO**: le somme si conservano

Le **scritture dirette** dicono quante volte ciascuna funzione **assegna** la grandezza.
Se il riordino avesse *aggiunto* o *togliere* scritture, la somma cambierebbe.

| grandezza | somma prima | somma dopo | `mitosi` prima | dove sono andate |
|---|--:|--:|--:|---|
| `d` | **8** | **8** | 2 | `_rn_div_d`, `_rn_sch_d` |
| `d0` | **9** | **9** | 3 | `_rn_div_d0`, `_rn_sch_d0`, `decidi_divisione` |
| `pos` | **7** | **7** | 2 | `_rn_div_pos`, `_rn_sch_pos` |

> ### ✅ **LE TRE SOMME SI CONSERVANO: `8→8`, `9→9`, `7→7`.** Le scritture che
> stavano in `mitosi` **non sono sparite**: stanno nei due esecutori della nascita, e per
> `d0` **una e' finita in `decidi_divisione`** — che e' **esattamente** *«la decisione
> separata dall'esecuzione»*, il titolo del `COMMIT 2`.

### ⚠ **E IL CONTEGGIO DEI LETTORI CRESCE DELL'ESATTO NUMERO DEI NOMI NUOVI:**
`d` da **17** a **20** *(+3: `decidi_divisione`, `_rn_div_d`, `_rn_sch_d`)*, `d0` da **15**
a **18** *(+3)*, `pos` da **20** a **22** *(+2)*. ### **Nessun lettore inatteso.**

## 6. CHE COSA QUESTO REFERTO **NON** DICE

1. ### **Non e' un sigillo**, per criterio del mandato: non c'e' un verdetto, e
   l'identita' su 72 passi **non promuove** niente.
2. ### **Non dice che i tredici commit siano byte-inerti IN GENERALE:** dice che lo sono
   **su questa scena, questo seme, questi 72 passi, coi flag a default.** Un flag acceso o
   una `FRAZ_NASCITA` diversa da `0.5` **non e' coperta** — e il `6b` lo dichiara da se'.
3. ### **Non attribuisce nulla alla piattaforma**, perche' i referti vecchi non la
   dichiarano. Se un giorno un conteggio cambiasse, la prima cosa da escludere sarebbe
   quella, **e oggi non si potrebbe.**

### 📌 **UNA COSA DA SISTEMARE, e non la faccio qui perche' il mandato dice <<solo
### misure>>:** i tre strumenti **non timbrano la piattaforma** nel loro json. Oggi lo fa
solo il comparatore, per se stesso. **Voce di coda, con criterio: si chiude quando i tre
scrivono `python`, `numpy`, `sistema` e `macchina` nel referto.**

---

**Comandi, verbatim:**

```
python -u csv/_test_fork/_pos_contro_d.py  --passi=1
python -u csv/_test_fork/_verso_archi.py   --passi=1
python -u csv/_test_fork/_misure_calore.py --passi=72
python -u csv/_test_fork/_confronto_blob_misure.py
```

**Blob:** simulatore **`0f060670`** *(non toccato)*; strumenti **`a9944b1a`**,
**`edb2e305`**, **`7c8b0200`** *(identici a `HEAD`, verificato PRIMA del run)*;
comparatore **`98e93b3b`**. **Tutti sha1 dei byte grezzi** *(par.2: non `git hash-object`)*.

**I reperti del 2026-10-01 restano**, col suffisso `.287154f3`, e i sei `oid` sono stati
verificati **identici** a quelli di `HEAD` prima del run *(`5ae1aa4`)*.
