# `(b)2` — **`SYNC_UPDATE` archiviato, `--sync` no-op. Sigillo a CINQUE bracci** *(2026-09-27)*

> **Mandato:** *«(A) driver byte-identico; (B) con `--sync` ACCESO, confronto fra prima e dopo:
> dichiara cosa ti aspetti e perché (dopo l'archiviazione `--sync` non fa più niente, quindi B DEVE
> differire da "prima con `--sync`"); (C) il caso che deve fallire.»*
>
> ### ✅ **CINQUE BRACCI SU CINQUE.** **Blob: `f845d30d` → `7439d5c3`.**
> Tag **`pre-archivio-sync`**, archivio `csv/_archivio/_sync_update.py`.

---

# 1. IL SIGILLO

**Condizioni:** scena `(ii)(a)`, seme `11`, `n = 2107`, `m = 70199`, **3 passi pieni**, ordine
canonico, nessuna iniezione di `rng`, nessun presidio. **Referto:**
`csv/_seal_fork/_sig_arch_sync.json`.

| | confronto | atteso | **esito** |
|---|---|---|---|
| **A** | `prima` senza `--sync` vs `dopo` senza `--sync` *(il driver)* | IDENTICO | ### **0 diverse** |
| **B** | `prima` **con** `--sync` vs `dopo` **con** `--sync` | ### **DIVERSO** | ### **19 grandezze** |
| **C** | `dopo` senza vs `dopo` **con** `--sync` | IDENTICO | ### **0 diverse** — **la prova del no-op** |
| **D** | `prima` senza vs `prima` **con** `--sync` | ### **DIVERSO** | ### **19 grandezze** — **il caso che deve fallire** |
| **E** | `prima` senza `--sync` vs `dopo` **con** `--sync` | IDENTICO | ### **0 diverse** |

## 1.1 — **Cosa mi aspettavo da B, e perché** *(dichiarato prima di guardare)*

**Dopo l'archiviazione `--sync` non fa più niente**, quindi `dopo`+`--sync` **deve** valere quanto
il percorso vivo. Ma `prima`+`--sync` valeva **un'altra cosa** — il ramo sincrono. ### **Quindi B
DEVE differire, e differire è il SUCCESSO, non il fallimento.**
**Le 19 grandezze:** `d` `d0` `phi` `phi_s` `phivel` `psi` `psi_spin` `_psi_spinor` `_psi_prec`
`_spinor_lift` `omega_s` `_nb` `_nb_prec` `tw` `twp` `vd` `peq` `mem_mot` `perc_chi`.
*(Identiche restano `eta`, `perc_geom`, `i`, `j`.)*

## 1.2 — **Il braccio D è il caso che deve fallire, e va misurato PRIMA di toccare**

**L'ho misurato prima di scrivere una riga**, ed è la precondizione di tutto il resto:
### **`--sync` AGIVA davvero in questa scena — 19 grandezze su 23.**

> ### 📌 **Se D fosse stato «identico», i bracci B e C non avrebbero provato niente.** *«Adesso
> `--sync` non fa nulla»* è un'affermazione vuota se **non faceva nulla nemmeno prima**. **D è
> quello che rende l'archiviazione una DECISIONE e non una pulizia.**

## 1.3 — ⚠ **E una dipendenza fra i bracci, che dichiaro invece di far sembrare cinque prove**

### **B e D sono la STESSA comparazione travestita.** Poiché **E** prova che
`dopo`+`--sync` `==` `prima` senza `--sync`, il confronto **B** *(`prima`+sync vs `dopo`+sync)*
**coincide** con **D** *(`prima` senza vs `prima`+sync)*. **E infatti danno le stesse 19
grandezze** — verificato, non supposto: gli elenchi sono **identici**.

### **I bracci INDIPENDENTI sono quattro: A, C, D, E.** **B è una conseguenza**, e chiamarlo
«quinta prova» gonfierebbe il conto.

## 1.4 — E il braccio **E** è quello che dice la cosa più forte

> **`--sync` acceso, sul codice nuovo, dà ESATTAMENTE ciò che il percorso vivo ha sempre dato.**
> Non «qualcosa di simile»: **byte per byte**. È la definizione operativa di *no-op*, misurata
> invece di asserita.

---

# 2. CHE COSA È USCITO

**Tolto per AST e non per testo** — i rami di `SYNC_UPDATE` sono **blocchi**, e trascriverli a mano
nell'ancora è il modo più facile di sbagliare l'indentazione o **perdere una riga in silenzio**.
Ogni `if` si individua **dal suo test e dalla funzione**, si asserisce **unico**, e la
trasformazione è **dichiarata**: `via` / `tieni-else` / `tieni-elif` / `togli-test`.

| dove | che cosa |
|---|---|
| `_passo_spinoriale` | le copie `nb_t` / `nb_prec_t` / `omega_t` della snapshot; i **due** rami `SYNC_UPDATE and SCUOTIMENTO` del rumore *(primario complesso e Bloch ruotato)*; il ramo `nb_vic = nb_prec_t` *(l'`elif` diventa `if`)* |
| `step` | il calcolo di `psi_t`; il ramo della **materia della metrica** *(resta il percorso storico `F = Mw @ exp(i·phi)`)*; i ternari su `psi_forces` ×2, `psi_sync`, `_psi_ct`, `psi_snapshot`, `_peq_src` |

### **7 blocchi e 9 ternari. `9-ter`: il numero delle leggi SCENDE, zero aggiunte.**

**⚠ E una trappola dell'AST:** `ast.unparse` normalizza `not X` in `(not X)`, quindi il test atteso
`"SCUOTIMENTO and not SYNC_UPDATE"` **non combaciava**. La sostituzione nel **sorgente** usa la
forma **senza** parentesi, il confronto **AST** quella **con**.

---

# 3. DUE COSE TROVATE RILEVANDO

## 3.1 — ### Lo scuotimento del vuoto sullo spinore **ora agisce SEMPRE**

`if SCUOTIMENTO and not SYNC_UPDATE` → `if SCUOTIMENTO`.
**Non è una legge nuova: è la stessa legge senza l'eccezione** — e il suo commento **lo chiedeva
già**: *«le due leggi devono essere identiche — il vuoto è lo stesso vuoto»*.

## 3.2 — `_peq_t` non aveva più lettori

La fotografia di `peq` esisteva **solo** per il ramo sincrono. Dopo la rimozione era **assegnata e
mai letta**: è uscita anche lei. *(Un'assegnazione morta non dà errore: si trova solo cercandola.)*

---

# 4. DUE COSE CHE **RESTANO**, e non sono dimenticanze

| | |
|---|---|
| **`_phi_t`** | la fotografia della **fase** la legge **il percorso vivo** — `z = np.exp(1j*_phi_t)`. **Non era parte di `SYNC_UPDATE`** |
| ### **`SYNC_SPINORE` ≠ `SYNC_UPDATE`** | `_forza_sync`, `_wI_sync`, `_uno_sync` sono gli ingredienti del **torque `SU(2)`** e **restano vivi**. ### **Due flag con `SYNC` nel nome, due leggi diverse** — confonderli avrebbe rotto una legge viva |

---

# 5. E UN SECONDO AVVISO CADUTO COL RAMO

`--rumore-colorato` avvisava di agire *«solo sul percorso VIVO (`not SYNC_UPDATE`)»* e di essere
quindi **inerte sotto `--sync`**. **Ora il percorso vivo è l'UNICO**, quindi il rumore colorato
agisce **sempre** e quell'avviso **non ha più oggetto**: sostituito da un commento che dice perché.

> **Non l'avevo cercato: l'ha trovato il rilievo dei 19 usi.** Un avviso che resta dopo che la sua
> condizione è sparita **è una falsità che si stampa a ogni run**.

---

# 6. LA FISICA: `H-REG-R` ha imposto una scheda che non c'era

**Il presidio ha rifiutato il commit due volte.** La seconda diceva una cosa precisa:
### **`SYNC_UPDATE` non aveva una scheda propria**, e prima di archiviarlo bisognava scriverla.

**Creata: `aggiornamento-sincrono`** — la **forma** che dichiarava, le **dimensioni** *(nessuna
grandezza nuova: è una regola sull'ordine di lettura)*, i **limiti** *(nessun `clip`)*, e il
**raggio misurato**.

> ### **E la scheda dice la cosa che conta: la FORMA era giusta, il RAGGIO era un quinto del passo.**
> Delle **56** letture miste `t`/`t+1` misurate nella FASE 0, ### **tutte e 56 stavano FUORI** dal
> suo raggio — compresa l'unica di `step`, che viene da `scuoti_vuoto`.
> **Quindi `--sync` non era una cura parziale del difetto: era la cura di un difetto DIVERSO.**
> `ETC-PASSO` **non lo estende: lo sostituisce sul passo intero**, e archiviarlo non lascia scoperta
> nessuna proprietà.

**Aggiornate anche quattro schede esistenti:** `inerzia-spinoriale`, `torsione-spinore`, `fase-phi`,
`tempo-proprio`.

> ### ⚠ **Una scheda che nasce nel commit che archivia la sua legge è una scheda che arriva TARDI.**
> `SYNC_UPDATE` è vissuto nel simulatore **senza forma chiusa scritta**, e nessuno ha dovuto
> derivarla. **È esattamente il modo in cui — dice il presidio — sono nati `D01`-`D33`.**

---

# TODO DEL NEXT STEP

> ### 🛑 **STOP, un pezzo alla volta.**

1. **(b)3 — gli altri rami che `CLIP-INVENTARIO` trova morti col driver**, **uno alla volta**,
   ognuno col suo sigillo byte-identico.
   ⚠ **E col criterio imparato in `(b)1`:** un sigillo su **una** configurazione **non certifica una
   precedenza fra due flag**. Dove un ramo morto convive con un altro flag, serve **anche il braccio
   in cui quell'altro è acceso**.
2. Poi **(c) la cura**.

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`ARCH-SYNC` · `ARCH-PAVIMENTI` · `CLIP-INVENTARIO` · `ETC-PASSO` · `CENS-B7` · `A8` · `A9` · `A11`
