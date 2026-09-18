# TASK HISTORY — **la frequenza di riferimento: prima il numero, poi la legge**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `df7d373`
**Blob:** `f8f46683` · **Nessuna cura cablata finché §2 non ha la via libera di Luca.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 ⚠ Il vincolo 2 si decide DAL DISCO, e si decide adesso: **`LAM` È FISSO**

```
:146   LAM      = 0.8
:147   LAM_BASE = 0.8
:5512  LAM = a.lam                       # da riga di comando
:5723  LAM = a.lam * fattore_lam         # coarse-graining, una volta all'avvio
```

**`LAM` non è mai riassegnato durante un run: è un parametro, settabile da CLI e poi costante.**
Quindi **`CS_M/LAM = 2.0/0.8 = 2.5` è LETTERALMENTE UN NUMERO** — non «un numero travestito»: un
numero. **La sua varianza nel tempo è ZERO per costruzione, e il criterio del §1 lo squalifica senza
bisogno di girare niente.** **Squalificato per il vincolo 2. → Lo riporto in tabella col suo zero,
perché il valore-null è il punto.**

### 1.2 ⚠ Ma allora va detta anche l'altra metà: **`CS_M` è fisso pure lui**

```
:261   CS_M, ALPHA_M, BETA_M = 2.0, 0.05, 0.8
```

**`CS_M/d_nodo` ha TUTTA la sua variazione temporale in `d_nodo`.** **Se lo dico di `LAM`, devo
dirlo di `CS_M`: sarebbe disonesto squalificare l'uno e non nominare l'altro.**

**E la distinzione che li separa esiste, ma è di significato, non di forma:**

> **`CS_M` è il LIMITE DI UN CAMPO CALCOLATO** — `cs_floor = CS_M/(1 + …)` → `cs → CS_M` dove
> `I → 0` (`:2921-2924`). **È il valore che una grandezza dinamica assume nel vuoto**, e il sistema
> lo raggiunge davvero: misurato, `max(cs/CS_M) = 0.9998`.
> **`LAM` non è il limite di niente: nessuna grandezza del sistema converge a `LAM`.** È una
> lunghezza messa a mano.

**La distinzione regge, ma è argomentativa. La dichiaro come tale, e non la spaccio per misura.**
*(Precedente: `STEP2_OROLOGIO` usa già `CS_M` in questo ruolo ed è l'unica voce della sezione A.)*

### 1.3 ⚠ IL CRITERIO DEL §1 TAGLIA IN DUE DIREZIONI, e va affilato prima di usarlo

Il mandato dice: *«un riferimento che non si muove fra passi È UN NUMERO TRAVESTITO»*.
**È giusto, ma da solo condannerebbe anche un riferimento BUONO.** Un orologio di riferimento che
sobbalza a ogni passo è un cattivo orologio: **la stabilità non è di per sé un difetto.**

**La distinzione che conta non è «si muove / non si muove», è:**

| | costante **PER COSTRUZIONE** | costante **PER STATO** |
|---|---|---|
| esempio | `median(x) = 1` — identità algebrica | un regime stazionario che fluttua |
| come si riconosce | **ESATTO**, cifra per cifra, a ogni passo | **fluttua**, e la fluttuazione ha una scala |
| verdetto | **punto fisso: A3 violato** | **legittimo** |

> **È esattamente l'errore che ho fatto due giri fa** (`Z38`): avevo dedotto un punto fisso dalla
> FORMA (`mean(I)`) senza guardare se il nodo tipico fosse davvero inchiodato. **Non lo era.**
> **Quindi qui misuro la traiettoria E la sua dispersione, non solo «cambia sì/no».**

### 1.4 ⚠ E un terzo riferimento che NESSUNO ha ancora nominato: **il GINOCCHIO**

```python
r = x/np.sqrt(1+x**2) + 1e-6
r_unit = 1.0/np.sqrt(2.0) + 1e-6      # il valore a x = 1
```

**Il ginocchio del bottleneck sta a `x = 1`. Oggi non è un numero perché `x = f/median(|f|)`: il
ginocchio sta DOVE STA LA POPOLAZIONE, per costruzione.**

**Se il riferimento diventa assoluto, `x = 1` diventa una CONDIZIONE FISICA** — *«l'avanzamento di
fase eguaglia il tasso di attraversamento-luce locale»* — **e questo è buono: è derivata, non
scelta.** **Ma è un ponte in più che va dichiarato**, e `A10` chiede appunto di contarli.

**⚠ E c'è una conseguenza già misurata** (`Z38` D): il tipico sta a `x ≈ 0.02`, cioè **la condizione
`f = CS_M/d` non è quasi mai soddisfatta** — i nodi avanzano di fase ~50 volte più lentamente del
tasso di luce locale. **Il bottleneck lavorerebbe nel tratto LINEARE per il tipico e SATUREREBBE
solo per la coda** (`max x = 3.43`). **Questo non è di per sé un difetto** — è ciò che una risposta
relativistica fa — **ma è un cambio di regime, e va detto, non nascosto.**

### Cosa NON so

- **se `f·d/cs` sia pinnato** — è il vincolo 3 sul candidato forte, e **non ho la traiettoria**;
- **se `d_nodo` si muova abbastanza** da rendere `CS_M/d_nodo` una legge e non un numero lento;
- **quanto si sposterebbe `r`** — è il numero che Luca ha chiesto, e non ce l'ho.

---

## 2. PROGETTAZIONE

**Tutto nella STESSA unità `[1/tempo]`, e tutto confrontato come «mediana ATTRAVERSO I NODI, per
passo»** — così le quattro righe sono commensurabili (A3c). *(`median(|f|)` è già uno scalare per
passo: è la stessa cosa, e la sua distribuzione attraverso i nodi è **costante per costruzione**.
Lo dichiaro invece di lasciare celle vuote.)*

**Passo A — la tabella del §1.** Per ciascun candidato: `p05 / mediana / p95` **attraverso i nodi**
(aggregati sugli ultimi 30 passi) **e** la **traiettoria della mediana per passo** a quattro istanti,
**con `std/mediana` fra passi** = la colonna che decide.

**Passo B — il test del punto fisso, e distingue le due colonne del §1.3.** Per ciascun candidato
`R`: la mediana per passo di `x = f/R`. **Se vale `1` ESATTO a ogni passo → punto fisso (A3).
Se fluttua → libero.** *Riporto anche quante cifre coincidono*, perché «1.000000» e «1» non sono la
stessa affermazione.

**Passo C — il numero che Luca ha chiesto:** il rapporto `median(|f|) / R_candidato`, **mediana e
dispersione fra passi** = di quanto si sposterebbe `r`.

**Passo D — `d_nodo` si muove?** La sua traiettoria. **Se `d_nodo` fosse quasi costante,
`CS_M/d_nodo` sarebbe `CS_M/LAM` con un travestimento**, e allora il candidato forte resta uno solo.

**LE LETTURE, FISSATE ADESSO:**
- **`x` esattamente 1 a ogni passo** → **punto fisso: il candidato CADE** (vincolo 3);
- **`R` con `std/mediana` sotto ~1 %** → **è un numero lento: si dichiara e si valuta come tale**
  *(non lo boccio automaticamente: vedi §1.3, la stabilità non è di per sé un difetto — ma il
  mandato chiede il criterio di A1, e un riferimento che non risponde allo stato non è una legge)*;
- **`d_nodo` quasi costante** → **`CS_M/d_nodo` è `CS_M/LAM` travestito: cade**;
- **nessun candidato passa i sei vincoli** → **«nessun riferimento derivabile», e lo dico.**

**COSA MI FA FERMARE:** qualunque delle prime tre sul candidato forte. **Si riporta e non si cabla**,
e comunque **non si cabla nulla prima della via libera di Luca sul §2.**

**E una cosa che NON farò:** nessun numero nel simulatore — **nemmeno per il test**: quel che serve
alla misura sta **nella sonda**. Non tocco `median(|f|)` senza sostituirlo, né il `+1e-6`, né
`x/sqrt(1+x²)`, né cucio `f`, né correggo `TAU_A`/`TAU_DIFF`/`PHI_CRIT`/`TAU_BG`.

---

## 3. TODO DEL NEXT STEP

- [x] **A** — la tabella del §1, quattro righe, stessa unità, con la varianza nel tempo
- [x] **B** — il test del punto fisso per ciascun candidato, con le cifre
- [x] **C** — il rapporto fra i riferimenti: di quanto si sposterebbe `r`
- [x] **D** — `d_nodo` si muove?
- [x] **riporta la tabella a Luca** *(è il numero che ha chiesto: dove siamo)*
- [x] **§2 — la legge, coi sei vincoli verificati UNO PER UNO** → **STOP e riporta**
- [x] **⚠ NON cablato** prima della via libera; **nessun numero nel simulatore**

---

## 4. ESITO

**PRESO, e ha deciso un vincolo senza girare niente:** **`LAM` è fisso** (`:146`). `CS_M/LAM = 2.5`
non è «un numero travestito»: **è un numero**, e la sua varianza nel tempo è **0 esatta**.

**PRESO, ed era la cosa giusta da dire:** ho nominato **anche** che `CS_M` è fisso, invece di
squalificare `LAM` e tacere sull'altro. La distinzione che li separa (`CS_M` è **il limite di un
campo calcolato**, `LAM` non è il limite di niente) **regge, ma è argomentativa**, e l'ho dichiarata
come tale.

**PRESO, §1.3:** avevo scritto che *«si muove / non si muove»* **taglia in due direzioni**, e che la
distinzione vera è **costante-per-costruzione contro costante-per-stato**. **Serviva:** solo
l'ATTUALE è pinnato, **a dieci cifre**, e i candidati fluttuano di un fattore 3.

**PRESO, §1.4 — il ginocchio:** con un riferimento assoluto `x = 1` diventa **una condizione
fisica**, non un numero. Regge.

**NON PRESO, ed è il risultato del giro: la RETROAZIONE.** Non l'avevo vista scrivendo il
ragionamento preliminare — è emersa **leggendo `TAU_LOC = 1.0` mentre controllavo tutt'altro**, e si
è chiusa su `:3389`. **`median(|f|)` fa TRE mestieri, non due.** **Se avessi eseguito il mandato
alla lettera avrei raccomandato un riferimento che ferma l'orologio.**

**E UN ERRORE MIO, nella sonda che avevo disegnato per decidere proprio quello:** la regressione
parziale `E3` è **degenere per costruzione** — dentro un passo `r` è funzione deterministica di `f`.
**Il controllo nullo `E2` ha funzionato** (E1 ≈ E2: tutta autocorrelazione), **il regressore
parziale no.** L'ho ritirato invece di usarlo, ed è la differenza fra una diagnosi e un numero.

## 5. TODO DEL PROSSIMO PASSO

- [ ] **DECIDE LUCA:** *(1)* `f = Δangle/dt_n` — taglia l'anello, **ma cambia la definizione di `f`**
      *(esclusa in `Z36`, in un altro contesto)*; *(2)* si tiene `median(|f|)` e **A10 resta aperto
      per una ragione ora NOTA**
- [ ] **`A10` va DISAMBIGUATO:** ancora o grandezza? Le due letture danno candidati **opposti**
- [ ] **`Z40` resta:** `cs` importa `mean(I)`, e il candidato forte ne eredita la tensione
- [ ] **⚠ NON toccato:** `median(|f|)`, `+1e-6`, `x/sqrt(1+x^2)`, `psi_spin`, il gauge, `LAM`, e i
      numeri tarati (`TAU_A`/`TAU_DIFF`/`PHI_CRIT`/`TAU_BG`)
