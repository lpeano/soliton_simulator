# REFERTO — **Il numero c'è. E la legge NON si può cablare: `median(|f|)` è anche il ROMPI-ANELLO**

**Data:** 2026-09-18 · **Blob** `f8f46683` · 1 seme (5), 120 passi, ramo **4pi** su 124/126
**Task history pushato PRIMA:** `b6308d1` · **Sonde:** `8088ce4`, `_retroazione_r` (committate prima
di girarle) · **NESSUNA CURA CABLATA, NESSUN NUMERO NEL SIMULATORE**

---

## 0. IL VERDETTO

1. **Il numero c'è** (§1): passando da `median(|f|)` a `cs_nodo/d_nodo`, **`x` si moltiplica per
   `0.0150`** — il nodo tipico passa da `x = 1` a `x ≈ 0.015`, e **`r` da `1.000` a `≈ 0.021`.**
2. **`CS_M/LAM` è squalificato senza bisogno di girare niente:** `LAM` è **fisso** (`:146`), dunque
   `CS_M/LAM = 2.5` è **un numero**, con varianza nel tempo **0 esatta**.
3. **Nessun candidato è pinnato** (vincolo 3): solo il riferimento **ATTUALE** lo è, e lo è
   **esattamente**.
4. **⚠ MA NESSUN RIFERIMENTO ASSOLUTO È CABLABILE, e la ragione è STRUTTURALE:**
   **`median(|f|)` non fa due mestieri — ne fa TRE.** È normalizzazione, è gauge, **ed è il
   ROMPI-ANELLO di una retroazione che senza di lui fermerebbe l'orologio.**
5. **E ho sbagliato il disegno di una misura, lo dico prima di usarla:** la regressione parziale
   `E3` è **degenere per costruzione**, e la ritiro come prova.

---

## 1. LA TABELLA — **il numero che serve a sapere dove siamo**

Tutti in **`[1/tempo]`**, tutti letti come *«mediana ATTRAVERSO I NODI, per passo»* (A3c).

| riferimento | p05 nodi | **mediana** | p95 nodi | t=primo | t=1/4 | t=metà | t=ultimo | **std/med nel TEMPO** |
|---|---|---|---|---|---|---|---|---|
| `median(\|f\|)` **ATTUALE** | *cost.* | **0.0394** | *cost.* | 1e-09 | 0.0327 | 0.0195 | 0.0650 | **0.6234** |
| `cs_nodo/d_nodo` tempo-luce | 1.061 | **1.776** | 2.307 | 1.129 | 1.890 | 1.792 | 1.830 | **0.0974** |
| `CS_M/d_nodo` vuoto+locale | 1.110 | **2.271** | 2.896 | 1.129 | 2.259 | 2.256 | 2.280 | **0.0986** |
| `CS_M/LAM` costante | 2.5 | **2.5** | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | **0 esatto** |

*(`median(|f|)` è **uno scalare per passo**: la sua distribuzione attraverso i nodi è **costante per
costruzione**. Non è una cella vuota — **è il punto**.)*

> **⚠ E IL DATO PIÙ INFORMATIVO DELLA TABELLA NON È QUELLO CHE IL MANDATO CERCAVA: è che IL
> RIFERIMENTO ATTUALE È SEI VOLTE PIÙ VOLATILE DEI CANDIDATI.** `std/med = 0.62` contro `0.097`.
> **Oggi `r` è misurato contro un metro che oscilla del 62 % da un passo all'altro — e quella
> oscillazione viene divisa via per costruzione.** È **un argomento a favore del mandato che nessuno
> aveva messo sul tavolo**, ed è misurato.

### (C) Di quanto si sposterebbe `r` — **il numero chiesto**

| verso | `median(\|f\|)/R` mediano | min | max | std/med |
|---|---|---|---|---|
| `cs_nodo/d_nodo` | **0.01503** | 0 | 0.0617 | 0.703 |
| `CS_M/d_nodo` | **0.01228** | 0 | 0.0479 | 0.711 |
| `CS_M/LAM` | **0.01111** | 0 | 0.0433 | 0.623 |

**`x` si moltiplicherebbe per `0.015`**, e — poiché **`TAU_LOC = 1.0`** (`:251`, **nessuno
smorzamento**) — **`r` del nodo tipico passerebbe da `1.000` a `≈ 0.021`**, cioè **`dt_n = DT·r`
scenderebbe di ~47 volte.** **E non è un riscalamento costante: il fattore varia di 4 volte fra
passi** (`std/med = 0.70`).

### (D) `d_nodo` si muove — il candidato non è `CS_M/LAM` travestito

```
d_nodo MEDIANO : 1.771 -> 0.885 -> 0.887 -> 0.877      std/med fra passi 0.197   max/min 2.019
d_nodo fra i NODI (30 passi): p05 0.691   mediana 0.881   p95 1.802      (LAM = 0.8)
```

**Si muove di un fattore 2 nel tempo e di 2.6 fra i nodi. `CS_M/d_nodo` non è una costante
travestita.** *(E `cs` aggiunge variazione **propria**: il rapporto fra le due traiettorie va da
`0.79` a `0.84`.)*

### ⚠ E la riserva del giro scorso è CHIUSA

**Nodi isolati (`d_nodo → LAM`, il ramo che il mandato vieta): `0` invocazioni su `124`.**
**Il ramo `LAM` non è mai scattato in questa scena.** *(P5: contato, non assunto.)*

---

## 2. I SEI VINCOLI, UNO PER UNO

| vincolo | `cs_nodo/d_nodo` | `CS_M/d_nodo` | `CS_M/LAM` |
|---|---|---|---|
| **1 dimensionale** `[1/tempo]` | **✓** `(L/T)/L` | **✓** | ✓ |
| **2 A1 nessun numero scelto** | **✓✓ nessuna costante: tutto stato** | **~** `CS_M` è fisso, ma è il **limite** di un campo calcolato | **✗ SQUALIFICATO** — `LAM` fisso (`:146`), varianza **0** |
| **3 A3 nessun punto fisso** | **✓** `median(x)` = `0.0171/0.0110/0.0321` | **✓** `0.0138/0.0084/0.0265` | ✓ |
| **4 A2 locale** | **✗ tensione** — `cs` importa `mean(I)` (**già dichiarata: `Z40`**) | **✓✓ interamente locale** | ✓ |
| **5 A10 un solo ponte** | **✓ vedi §2.1 — ed è il contrario di quel che sembra** | **✗ vedi §2.1** | — |
| **6 A6 stato precedente** | **✓✓** `_tempo_luce_nodo` legge `_cs_nodo_prev`, cioè **il `cs` di t-1**, e `d` a `ritmo()` è ancora quello di t-1 | **✓** solo via `d` | ✓ |

### (B) Il vincolo 3, con le cifre — **e solo l'ATTUALE è pinnato**

```
riferimento             median(x) a t=primo / 1/4 / meta' / ultimo
median(|f|) ATTUALE     0            1              1              1
cs_nodo/d_nodo          0            0.0171494778   0.01097883113  0.03211666255
CS_M/d_nodo             0            0.01378116042  0.0084363883   0.02647152823
```

**`median(x) = 1` a DIECI CIFRE per l'attuale**, e non è un caso: è **l'identità**
`median(f/median(f)) = 1`. **I candidati fluttuano di un fattore 3: nessun punto fisso.** ✓

**⚠ E UN DIFETTO DELLA MIA COLONNA RIASSUNTIVA, che dichiaro:** avevo stampato `max|med-1|`, e vale
**1 per tutte e quattro le righe** — **perché è dominata dai passi degeneri di `Z33`**, dove
`median(x) = 0`. **La colonna che avevo scelto non separa niente: separano le cifre per passo.**
*(È la classe di errore già catalogata: un criterio scritto dal modello mentale invece che dalla
misura.)*

### 2.1 ⚠ A10 dice il CONTRARIO di quel che il vincolo 5 suggerisce

Il mandato scrive: *«il riferimento di `r` e quello di `omega_clk` devono essere LA STESSA COSA»*, e
letteralmente questo indicherebbe `CS_M/d_nodo`, che condivide `CS_M`. **Ma seguendo la catena
completa si vede che produrrebbe un DOPPIO CONTEGGIO:**

```
omega_clk = coerenza * r_node          (:2458)
omega_clk = omega_clk * (cs/CS_M)^2    (:2502)   <- IL confronto col vuoto
```

| con `r` costruito su… | la catena diventa | verdetto |
|---|---|---|
| **`cs_nodo/d_nodo`** | (coerenza) × (**ritmo proprio del nodo**, nessun riferimento esterno) × (**dilatazione vs vuoto**) | **UN SOLO ponte verso il vuoto** ✓ |
| `CS_M/d_nodo` | (coerenza) × (**ritmo vs vuoto**, lineare in `CS_M/d`) × (**dilatazione vs vuoto**, quadratica in `cs/CS_M`) | **DUE confronti col vuoto moltiplicati** ✗ |

> **`f·d/cs` è un invariante PROPRIO del nodo — «di quanto avanza la fase per attraversamento-luce
> locale» — e non contiene nessun riferimento esterno. Il confronto col vuoto resta UNO SOLO, ed è
> quello che `STEP2_OROLOGIO` fa già.**
> **`f·d/CS_M` misura già il vuoto, e poi `STEP2` lo misura di nuovo: sono due rotte indipendenti
> dalla geometria al tempo, entrambe ancorate al vuoto — esattamente ciò che A10 vieta.**

**Quindi `cs_nodo/d_nodo` vince su A1 (nessuna costante), su A6 (già costruito sullo snapshot) e su
A10 (un solo ponte); perde solo su A2, con una tensione GIÀ dichiarata e registrata (`Z40`).**
**E il ginocchio `x = 1` diventa una CONDIZIONE FISICA derivata — *«la fase avanza di un radiante
per attraversamento-luce locale»* — non un numero.**

**⚠ E questo è un riscontro su A10 stesso, aggiunto ieri:** l'assioma **non dice se il «ponte» sia
l'ANCORA o la GRANDEZZA che attraversa. Le due letture portano a candidati opposti.** *(A10 andrà
disambiguato, e questo è il primo caso che lo costringe.)*

---

## 3. ⚠ E QUI LA STRADA SI CHIUDE — **`median(|f|)` è anche il ROMPI-ANELLO**

**`TAU_LOC = 1.0`** (`:251`): **nessuno smorzamento**, `r = r_normalized`, e **`dt_n = DT·r`**
(`:2972`). Quindi se `r` scende, **il tic locale scende con lui**.

**E il tic locale determina l'avanzamento di fase — VERIFICATO DAL SORGENTE, non dedotto:**

```python
:3389   self.phi = (_phi_t + (dt_n_s * self.phivel) + delta_sync_phi) % (4*np.pi)
:3333   delta_phivel = dt_n_s * (coppia - xi_termo*_phivel_t) / M_PH
```

**`Δphi = dt_n · phivel`.** E `psi_spin` è costruito dalle fasi dei vicini, mentre
**`f = Δangle(psi_spin)/DT`** — **diviso per il tempo di COORDINATA, non per `dt_n`.** Dunque, al
prim'ordine:

```
f  ∝  dt_n  =  DT · r          ==>       f ∝ r
```

### L'anello, e perché oggi non si chiude

| | il guadagno dell'anello |
|---|---|
| **oggi**, `x = f/median(\|f\|)` | se tutti gli `f` si riscalano di λ, **`x` NON cambia**: `median` si riscala con loro → **guadagno esattamente 1, PER COSTRUZIONE** |
| con un riferimento **assoluto** `R` | `x = f/R`, e nel tratto lineare `r ≈ √2·x` → `x' ≈ √2·(f/R)·x` → **guadagno `√2 · x_misurato`** |

**E `x_misurato` è nella tabella: `0.015` – `0.024`.** Guadagno **`≈ 0.021 – 0.035`**, cioè
**≪ 1**:

> **`x → 0` geometricamente, ~50 volte per passo. L'orologio si fermerebbe in pochi passi, e
> `r` cadrebbe sul pavimento `1.4e-06`.**

**E l'alternativa non è migliore:** un `R` scelto perché il guadagno valga **1** sarebbe **un filo di
rasoio** — e sarebbe **un numero tarato**, cioè A1. **Solo un riferimento normalizzato sulla
popolazione dà guadagno 1 PER COSTRUZIONE.**

> **Ecco il terzo mestiere: `median(|f|)` non è solo normalizzazione (adimensionalità) e gauge
> (il punto di riferimento). È il ROMPI-ANELLO che rende `r` indipendente dalla deriva comune di
> `f`.** *(Nel mio verdetto su `e342ae8` avevo scritto «la mediana è ENTRAMBE». **Sono TRE.**)*

### ⚠ E LA VIA D'USCITA ESISTE, ma cambia una cosa che Luca aveva escluso

L'anello esiste **perché `f` è misurato in tempo di COORDINATA**:
`f = Δangle/DT`, con `Δangle ∝ dt_n`. **Se `f` fosse misurato in tempo PROPRIO** —
`f = Δangle/dt_n` — **`f` non dipenderebbe più da `r`, l'anello si taglierebbe alla radice, e un
riferimento assoluto diventerebbe cablabile.**

**Ed è esattamente la regola permanente di CLAUDE.md par.9:** *«IL TIC DEI PROCESSI LOCALI È
`dt_n = DT·r`, NON `DT`… usarlo dentro un processo locale cancella la dipendenza dall'orologio del
luogo»*. **`f` usa `DT`.**

**Ma è un CAMBIO DELLA DEFINIZIONE DI `f`, che Luca ha escluso nel mandato `Z36`** (*«si cuce lo
SNAPSHOT, NON si cambia la definizione di `f`»*). **Quella esclusione era in un altro contesto, ma
non la riapro da solo: la metto sul tavolo.**

---

## 4. LA MISURA CHE HO SBAGLIATO, e la ritiro prima di usarla

Avevo disegnato tre pendenze per decidere l'anello **dai dati** invece che dal codice:

```
             E1  f(t+1) vs r(t)      E2  NULLO: vs f(t)      E3  PARZIALE
MEDIANA        +0.4755  sd 0.174       +0.4727  sd 0.129       -0.9193  sd 0.409
```

**E1 ed E2 coincidono** (`+0.476` contro `+0.473`): **la correlazione grezza con `r` è spiegata
INTERAMENTE dall'autocorrelazione di `f`** — il controllo nullo ha fatto il suo mestiere.

**⚠ E `E3` NON SI PUÒ LEGGERE, per un difetto del mio disegno:** dentro un passo,
**`r` è una funzione DETERMINISTICA di `f`** (`r = r_norm(f/med)`, con `med` costante nel passo).
**A `f(t)` fissato, `r(t)` non ha varianza residua: la regressione a due regressori è degenere per
costruzione**, e il `−0.92` con `sd 0.41` (valori da `−1.51` a `−0.18`) **è l'impronta della
collinearità, non un effetto fisico.**

> **Ritiro `E3` come prova.** La domanda **non è decidibile trasversalmente dentro un passo** — `r`
> non porta informazione oltre `f` — **e la decide il codice (`:3389`), non una regressione.**
> **Il costo di non dirlo sarebbe stato una diagnosi sbagliata con numeri giusti** *(A3c)*.

---

## 5. COSA PROPONGO — **e non è un cablaggio**

**Non esiste oggi un riferimento assoluto cablabile**, e **non è una questione di scelta fra
candidati: è la retroazione.** Il mandato prevede questo esito — *«"nessun riferimento derivabile" è
un esito valido»* — **ma la formulazione esatta è più precisa e più utile:**

> **Il riferimento derivabile ESISTE ed è `cs_nodo/d_nodo`** — passa `A1`, `A3`, `A6`, `A10`, ed è
> **già calcolato** da `_tempo_luce_nodo` (`1/tempo_luce`), **già sigillato** (`S8`,
> `max|err| = 2.55e-15`), con la sola tensione `A2` **già registrata** (`Z40`).
> **Ma NON è sostituibile a `median(|f|)` finché `f` è misurato in tempo di coordinata**, perché
> `median(|f|)` sta facendo **un terzo lavoro** che nessuno gli aveva attribuito.

**LE DUE STRADE, e sono decisioni tue:**
1. **Si taglia l'anello alla radice:** `f = Δangle/dt_n`. **Rende A1 realizzabile** e allinea `f`
   alla regola permanente sul tic locale. **Ma cambia la definizione di `f`.**
2. **Si tiene `median(|f|)`** e si accetta che **il gauge di `r` resti relativo**, dichiarando che
   **il difetto `A10` resta aperto per una ragione ora NOTA** — non per distrazione.

**Non ho un criterio, scritto prima, che scelga fra le due. La differenza è di fisica, non di
metodo.**

## 6. COSA NON HO FATTO

**Nessun numero nel simulatore, nemmeno per il test** — tutto nelle sonde. **Nessuna cura cablata.**
Non toccati: `median(|f|)`, il `+1e-6`, `x/sqrt(1+x²)`, `psi_spin`, il gauge. **`LAM` non usato.**
**`TAU_A`/`TAU_DIFF`/`PHI_CRIT`/`TAU_BG` non corretti** *(N8 li prevede **dopo** una cura, e la cura
non c'è; ma il numero che li riguarda è nel §1: `dt_n` scenderebbe di ~47 volte, e sono tutti
espressi in quella convenzione)*.

## 7. I LIMITI, dichiarati

Un seme, 120 passi, una scena. **Il guadagno dell'anello è un conto al prim'ordine** su
(a) `:3389` — fatto di codice — (b) `x` misurato, (c) `TAU_LOC = 1.0`, (d) il tratto lineare del
bottleneck. **Non ho girato il codice curato: non potevo, e non dovevo.** **La catena
`Δangle(psi_spin) ∝ Δphi` è al prim'ordine**, perché `psi_spin` è una combinazione satura delle fasi
dei vicini — **ciascuna col PROPRIO `dt_n`**: la proporzionalità vale sulla scala comune, non nodo
per nodo. **Il dato di riferimento per `N6`:** `r` oggi ha `min 1.293e-04`, `p05 0.1108`,
`mediana 1`, `p95 1.4095`, `max 1.41419` — **il pavimento assoluto `1.414e-06` non viene raggiunto
in questa scena.**
