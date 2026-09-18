# TASK HISTORY — **allineare `r` al gauge del vuoto. E un'obiezione alla premessa del §0**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `bff8523`
**Blob:** `f8f46683` · **Nessuna cura cablata finché il §1 non è chiuso.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### 1.1 Cosa il mandato dice, e che parte ho verificato dal sorgente

Verificato, e **è vero**:

```python
# ritmo()  (:2076-2081)
med = max(float(np.median(np.abs(f))), 1e-9)       # <- il riferimento e' la MEDIANA di |f|
x   = f / med
r   = x/np.sqrt(1+x**2) + 1e-6
r_unit = 1/np.sqrt(2) + 1e-6                        # il valore a x = 1
return 1.0 + TAU_LOC*(r/r_unit - 1.0)

# STEP2_OROLOGIO  (:2502)
omega_clk = omega_clk * (_csn2 / CS_M) ** 2         # <- il riferimento e' CS_M

# e si moltiplicano a :2458:   omega_clk = coerenza * r_node
```

**Il range di `r_normalized` è confermato per costruzione:** `x=0 → 1.4142e-06`, `x=1 → 1` esatto,
`x→∞ → (1+1e-6)/(1/√2+1e-6) ≈ √2`. **Il tetto √2 è relativo al nodo mediano.**

### 1.2 ⚠ L'OBIEZIONE: **`cs/CS_M` NON è ancorato al vuoto. È ancorato a `mean(I)`.**

Il mandato dice: *«`CS_M` è il valore di `cs` NEL VUOTO. Non è un parametro arbitrario»*, e ne
deduce che spostare `r` su quel riferimento lo porterebbe **dalla materia al vuoto**.

**Ho letto `_cs_nodo` (`:2913-2924`), e il vuoto sta solo nel NUMERATORE:**

```python
_Lam  = float(np.mean(_I))                                   # <- MEDIA SULLA PROPRIA POPOLAZIONE
_scala = max(_Lam, 1e-30) / (GAMMA_TURBO*GAMMA_TURBO)
cs_floor = CS_M / (1.0 + np.sqrt(_I) * np.sqrt(1.0/_scala))  # <- I/mean(I)
transizione = 0.5*(1.0 + np.tanh(1.0 - u_nodo))              # u_nodo = I/media_VICINI
return cs_floor + (CS_M - cs_floor)*transizione
```

> **`cs/CS_M` è `1/(1 + sqrt(I/mean(I)))` modulato da `I/media_vicini`.**
> **Il rapporto che decide il valore è `I` contro la MEDIA DELLA STESSA POPOLAZIONE.**

**E ha un punto fisso della famiglia C12, esatto:** nel nodo dove `I = mean(I)`,
`sqrt(I)*sqrt(1/mean(I)) = 1` **sempre**, quindi `cs_floor = CS_M/2` **a qualunque maturazione**.
*(Il `transizione` lo smorza, non lo toglie: è un secondo rapporto, alla media dei vicini.)*

**COSA NE SEGUE, e va detto prima di misurare:** spostare `r` su `cs/CS_M` **non lo porterebbe
«dalla materia al vuoto»**. Lo porterebbe **da `median(|f|)` a `mean(I)`** — **da una statistica
sulla propria popolazione a un'altra.** **Se lo scopo è togliere l'auto-normalizzazione, questa non
la toglie.**

**Non lo do per certo come bocciatura:** resta vero che **`CS_M` è un'ancora ASSOLUTA che
`median(|f|)` non ha**, e che il fattore `(cs/CS_M)²` **vale esattamente 1 nel vuoto** mentre
`r_normalized` vale 1 **nel nodo mediano** — e quella differenza **è reale**. Ma la frase *«è
ancorato al vuoto»* **è vera solo a metà**, e la misura del §1 deve dirlo.

### 1.3 E una distinzione dimensionale che il mandato ha già preso, e che va tenuta

`median(|f|)` normalizza una **frequenza**; `CS_M` normalizza una **velocità**. **Non sono due gauge
della stessa grandezza**: sono due riferimenti in due fattori adimensionali che **si moltiplicano**.
Moltiplicare due fattori adimensionali con riferimenti diversi **non è di per sé un difetto** — lo
è **solo se entrambi pretendono di essere LA STESSA dilatazione.** Ed è esattamente ciò che
pretendono: `r_node` è *«il ritmo del tempo proprio locale»*, `(cs/CS_M)²` è *«l'orologio di
Compton»*. **Il difetto c'è, ma è nella PRETESA, non nella dimensione.**

### 1.4 ⚠ E il rischio che il mandato non nomina: **la mediana è ANCHE la normalizzazione**

È il mio verdetto su `e342ae8`, e vale qui: `median(|f|)` **fa due mestieri**. Toglierlo per
`CS_M/d_nodo` rende `x` un **numero assoluto**, e il ginocchio del bottleneck `x/sqrt(1+x²)` sta a
`x = 1`. **Se il valore tipico di `f·d/CS_M` non è O(1), il bottleneck non è più un bottleneck:**
tutti sul pavimento (`r → 1.41e-06`) o tutti in saturazione (`r → √2`), **cioè `r` degenere per
TUTTI, sempre** — molto peggio di `Z33`, che è 1 passo su 31.

> **Questa è la stessa forma della trappola di `Z36`: un solo numero (M4, «la scala si apre»)
> PASSEREBBE anche nel caso catastrofico**, perché una scala tutta appiattita su `√2` **ha aperto il
> tetto**. **Serve la coppia: dove si apre E dove finisce la popolazione.**

### Cosa NON so

- **dove sta il nodo mediano** — è il §1;
- **quanto vale `cs_std/cs` sul blob attuale** — il registro dice `0.0086 %` prima di `cs_floor`, il
  mandato dice `11 %` **oggi**. **Non lo trasporto: lo misuro** (P1);
- **se `f·d/CS_M` sia O(1)** — ed è il numero che decide se la cura è **cablabile**, non se è giusta.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO

**Passo A — `cs/CS_M`: distribuzione.** p05, mediana, p95, min, max, **frazione > 0.99** e
`cs_std/cs`. *Decide:* la terza lettura del mandato (*varianza trascurabile → la via cade*).

**Passo B — dove sta il nodo mediano di `f`.** Si prendono i nodi con `x ∈ [0.9, 1.1]` e si
riportano **il loro `cs/CS_M` e il loro `rho/peq`**, contro la distribuzione completa **nello stesso
istante e sulla stessa popolazione** (A3c). *Decide:* le prime due letture del mandato.

**Passo C — ⚠ `cs/CS_M` È ESSO STESSO ANCORATO? (la mia obiezione, §1.2)** Si misura `I/mean(I)`
del nodo mediano di `I`, **a due istanti diversi**: se vale **1 a entrambi**, il presunto gauge del
vuoto ha lo **stesso** punto fisso che si vuole togliere. *Decide:* se la cura sposta il problema
invece di risolverlo.

**Passo D — ⚠ `f·d/CS_M` è O(1)? (il rischio §1.4)** Distribuzione di `f·d_nodo/CS_M` e di
`f·d_nodo/cs_nodo`, con **la frazione che finirebbe sul pavimento** (`x < 1e-3`) **e in saturazione**
(`x > 1e3`). *Decide:* **se la cura è cablabile**, indipendentemente da se sia giusta.

**LE LETTURE, FISSATE ADESSO:**
- **`cs/CS_M` mediano ~ 1** → i due gauge quasi coincidono: **cura cosmetica. Si dice e ci si ferma.**
- **`cs/CS_M` mediano << 1** → il gauge è nella materia: **l'allineamento vale, si passa al §2 del
  mandato.**
- **`cs_std/cs` trascurabile** → `cs` non può fare da gauge: **la via cade.**
- **⚠ `I/mean(I)` del nodo mediano = 1 a entrambi gli istanti** → **il gauge proposto ha il proprio
  punto fisso: si riporta, e la cura va RIFORMULATA, non eseguita.**
- **⚠ `f·d/CS_M` fuori da O(1) di più di tre ordini** → **non cablabile così: il bottleneck
  degenererebbe per tutti.** **M4 da solo PASSEREBBE lo stesso, e sarebbe un falso PASS.**

**COSA MI FA FERMARE:** qualunque delle ultime due. **Si riporta e non si cabla**, anche se le prime
due letture dessero via libera.

**E una cosa che NON farò:** non uso `LAM`, non tocco il `+1e-6` né la forma `x/sqrt(1+x²)`, non
cucio `f`, non correggo `TAU_A`/`TAU_DIFF`/`PHI_CRIT`/`TAU_BG`.

---

## 3. TODO DEL NEXT STEP

- [x] **A** — distribuzione di `cs/CS_M` e `cs_std/cs` sul blob **attuale**
- [x] **B** — dove sta il nodo mediano di `f`: il suo `cs/CS_M` e il suo `rho/peq`
- [x] **C** — ⚠ `I/mean(I)` del nodo mediano a due istanti: il gauge proposto è ancorato a sé?
- [x] **D** — ⚠ `f·d/CS_M` è O(1)? frazione a pavimento e in saturazione
- [x] **STOP e riporta** col verdetto contro le cinque letture
- [ ] **IN ATTESA DI LUCA** — *(solo con via libera)* §2 del mandato — i candidati, **derivati**

---

## 4. ESITO — *cosa il ragionamento preliminare aveva preso, e cosa no*

**NON PRESO, ed e' la cosa piu' importante del giro: LA MIA OBIEZIONE E' REFUTATA.**
Avevo scritto che `cs/CS_M`, essendo costruito su `mean(I)`, avrebbe avuto **un punto fisso della
famiglia C12** e che la cura avrebbe **spostato il problema invece di risolverlo**.
**Misurato: `median(I)/mean(I)` varia di un fattore 4.5 fra istanti.** Il nodo **tipico** non e'
inchiodato.

**E la ragione dell'errore e' precisa, non generica:** avevo trasportato la forma di C12
(*«normalizzare sulla propria statistica inchioda il nodo tipico»*) **senza guardare QUALE
statistica**. `median(|f|)` inchioda **la mediana**, che **e'** il nodo tipico, per identita'.
`mean(I)` inchioda **la media**, che su una distribuzione asimmetrica **non e' il nodo tipico**.
**E' P1 applicato a un'identita' algebrica — lo stesso errore della voce su `_tau`, e l'avevo
scritto io stesso in CLAUDE.md due giorni fa.**

**PRESO, e serviva:** la parte **strutturale** dell'obiezione resta vera e va nel referto — la scala
**e'** `mean(I)`, il vuoto sta **solo nel numeratore**. Ma **la conseguenza operativa era sbagliata**,
ed e' la conseguenza che decideva.

**PRESO, e questo ha retto:** il rischio §1.4 (*la mediana e' ANCHE la normalizzazione*). **La banda
utile passa da `87.1 %` a `15.1 %`.** **Se avessi guardato solo M4 («la scala si apre») avrei letto
un PASS**, perche' il tetto e' quasi identico (`1.358` contro `1.414`) — **mentre l'`84.9 %` dei
nodi scivola nel decimo inferiore.**

**MA LA SOGLIA CHE AVEVO SCRITTO NON SCATTA:** avevo fissato *«piu' di 3 ordini»*, e sono **1.7**.
**Non la sposto a posteriori.** **Il numero che decide l'ho trovato DOPO averlo cercato, e questo
va detto: la lettura pre-fissata era la coppia giusta ma la soglia sbagliata.**

**E una cosa che non cercavo:** **`cs_std/cs = 17.6 %`** — **un fatto stabile di CLAUDE.md e'
caduto**, e la causa e' **una cura di categoria D fatta due giorni fa**. *(`Z39`.)*

## 5. TODO DEL PROSSIMO PASSO

- [ ] **DECIDE LUCA, e non io:** le due letture del §4 — **degenerazione** o **fisica** — e non ho
      un criterio scritto prima che le separi
- [ ] **se via libera:** `CS_M/d_nodo` (il principio), **ma PRIMA contare il ramo `d_nodo -> LAM`**
      (`:3041`, `:3043`): il mandato vieta `LAM` e per quella via rientrerebbe. **P5.**
- [ ] **`Z39` apre un fronte suo:** rifare `tau = d/cs` contro `tau ∝ d` su >= 4 semi, ora che `cs`
      ha varianza. **Tocca il fronte `A`.**
- [ ] **⚠ NON toccato:** `median(|f|)`, il `+1e-6`, `x/sqrt(1+x^2)`, `psi_spin`, il gauge, e nessun
      numero tarato (`TAU_A`/`TAU_DIFF`/`PHI_CRIT`/`TAU_BG`)
