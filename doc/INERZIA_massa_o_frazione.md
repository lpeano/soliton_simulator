# `inerzia`: MASSA o FRAZIONE? — **FASE A: la lettura dimensionale**

> **Scritto per Claude web** (regola `CLAUDE.md` §5-ter: a ogni riscontro, una relazione).
> Branch `fork-su2`, 2026-09-15. Blob sul disco **`f5887254`** (gate §0 su `c0803713`:
> disallineamento voluto). **Nessuna modifica alla fisica.** Stato: **FASE A chiusa**, B e C da fare.

---

## 0. IL RISCONTRO IN UNA RIGA

> **Nessuna delle due ipotesi del mandato descrive il codice.** Non è una *frazione normalizzata*
> (nessuna normalizzazione esiste) e non è una *massa* (nessuna massa compare). È una **terza cosa**:
> un'**intensità di campo adimensionale** usata dove la dinamica richiede una massa — e il suo
> valore dipende soprattutto dall'**età dei nodi**, non da `N`.

---

## 1. LA CATENA DA CUI VENIAMO (contesto, già stabilito)

`inerzia ≈ 1e-7` → `omega = coppia/inerzia` esplode → `omega_eq ≈ 7.3e4` → **112 giri/passo** →
il settore di spin è **aliasato** → i Bloch sono casuali **per risoluzione, non per fisica**.
Il Gilbert/FDT è stato testato e **cade** (`doc/ANALISI_gilbert_fdt.md`). La diagnosi residua era:
*«il problema è l'INGRESSO (coppia/inerzia)»*. Questo lavoro guarda **dentro** quell'ingresso.

---

## 2. A.1 — Dove nasce `inerzia`, e cosa c'è a destra dell'uguale

[`soliton_simulator.py:1891`](../soliton_simulator.py#L1891) — **l'unica** assegnazione che entra in
`correzione/inerzia`:

```python
inerzia = np.maximum(self._rho_sorgente(), 1e-6)
```

A destra: **solo** il modulo quadro del campo, più il pavimento. Letto dal **sorgente**, non dai
commenti — oggi i docstring hanno ingannato tre volte (riga 2196; «`omega_s` conservativo»; «il
calcio alimenta ogni passo»).

## 3. A.2 — È **letteralmente** `|Psi|²`, senza alcun fattore

`_rho_sorgente()` restituisce `rho_spin` (con `--campo-spinoriale`) oppure `np.abs(self.psi)**2`.

> **Nessuna massa. Nessun volume. Nessuna normalizzazione.** L'unico fattore è il floor `1e-6`,
> attivo sul **99.7 %** dei nodi (misurato, `doc/BILANCIO_ordine_spin.md` §6.1).

## 4. A.3 — `psi` **non è normalizzato**: la firma (1) non è prevista dal codice

```python
F = self._mat(w) @ (amp * np.exp(1j * self.phi))     # amp = SCALA_AMP = 1.0
self.psi = self.satura(F)                            # f / (1 + GAMMA*|f|)
```

È una **somma pesata sui vicini**. **Non c'è** divisione per `N`, **non esiste** alcun vincolo
`sum|psi|² = cost` in tutto il file, e `satura` è un **tetto morbido** (asintoto `1/GAMMA = 20`),
non una normalizzazione.

> Il codice prevede il **contrario** della firma (1): `|psi|` dovrebbe **crescere** col numero di
> vicini, non calare con `N`.

### 4.1 E allora perché vale ~1e-7? **L'età, non la normalizzazione**

In `_pesi()` [`:2124`](../soliton_simulator.py#L2124):

```python
ramp = np.minimum(1.0, self.eta / TAU_A)
base = np.exp(-self.d / self._lam_archi()) * ramp[self.i] * ramp[self.j]
```

- `eta += dt_n` (≈ 0.01) per passo — [`:2571`](../soliton_simulator.py#L2571);
- `TAU_A = 50` nel regime **deterministico** (contro 2.0 nello stocastico);
- ⇒ un nodo raggiunge **peso pieno solo dopo ~5000 passi**.

Al passo 150: `ramp ≈ 0.03`, quindi `w ∝ ramp_i·ramp_j ≈ 9e-4`. In più le fasi sono incoerenti,
quindi la somma è un **random walk** (`√k`, non `k`).

**E i figli della mitosi nascono con `eta = 0`** ([`:3119`](../soliton_simulator.py#L3119); gli
antinodi Schwinger [`:3236`](../soliton_simulator.py#L3236)): con mitosi continua una frazione
stabile della popolazione resta **permanentemente immatura**.

> Questo è **coerente con la crescita misurata** di `Lam` (energia del vuoto) durante un run:
> **7.45e-14** al passo 1 → **1.32e-4** al passo 150 (`csv/_test_fork/_crescita_omega.txt`).
> Nove ordini di grandezza in 150 passi: il campo **si sta accendendo**, non è a regime.

## 5. A.4 — L'analisi dimensionale, **ed è qui il reperto**

| pezzo | dimensioni |
|---|---|
| `w = exp(−d/λ)·ramp·ramp` | **1** |
| `F = Σ w·e^{iφ}`, `psi = satura(F)` | **1** |
| **`inerzia = \|psi\|²`** | **1** |
| `B` (media pesata di versori), `nb` (versore) | **1** |
| `correzione = cross(B, nb)` | **1** |
| **`correzione / inerzia`** | **1 — ADIMENSIONALE** |

Ma [`:1918`](../soliton_simulator.py#L1918) è `omega += dt_n·(correzione/inerzia − omega/tau)`, e
`theta = |omega|·dt_n` deve essere un **angolo**. Perché torni serve
**`[correzione/inerzia] = 1/T²`**.

> **Non ce l'ha.** In un corpo rigido `dω/dt = τ/I` dà `1/T²` *da sé*, perché coppia e momento
> d'inerzia portano entrambi `M·L²`. Qui il numeratore è un **puro prodotto vettoriale geometrico**
> e il denominatore una **pura intensità di campo**: nessuno dei due porta dimensioni, e il rapporto
> non produce `1/T²`.

### 5.1 Come va letto, **onestamente**

`CLAUDE.md` dice che `DT` **non** è un passo temporale continuo ma un **contatore di tick**. Quindi
il modello **potrebbe** lavorare di proposito in unità adimensionali, e in quel caso l'analisi
dimensionale **non può dichiarare un errore**. Ma allora resta la conseguenza, che è il punto:

> **non c'è alcuna protezione dimensionale, e il valore numerico di `omega` è libero.**
> Nulla, in `correzione/inerzia`, lo lega a una frequenza propria del modello — per esempio
> `cs/LAM`. Il «4000× il tetto di Planck» non è quindi un'affermazione fisica: **non c'è alcuna
> scala di frequenza nel rapporto**, e l'unico tempo che entra in `omega` è il tick stesso.

Ed è anche il motivo per cui **riparametrizzare non può aiutare** — il presidio che il mandato pone:
non ci sono unità da riscalare, la quantità è **unit-free per costruzione**.

---

## 6. COSA CAMBIA PER LA FASE B (una firma che il mandato non prevedeva)

Il mandato chiede tre firme sull'istogramma delle masse **contro `N`**. La lettura dimensionale dice
che la variabile giusta è un'altra:

> **`|Psi|²` contro `eta` (l'ETÀ del nodo), non contro `N`.**
> Se i valori piccoli sono i nodi **giovani**, il `1e-7` è un effetto di **maturazione** —
> **transitorio**, se non fosse che la mitosi ne rigenera di continuo.

Procedo quindi con gli istogrammi ai quattro istanti richiesti **più** la stratificazione per `eta`,
dichiarando che è una **quarta firma**, aggiunta e non sostitutiva.

---

## 7. STATO E COSA NON È STATO TOCCATO

| fase | stato |
|---|---|
| **A** — lettura dimensionale | **chiusa** |
| **B** — istogrammi + stratificazione per `eta` | da fare |
| **C** — verdetto incrociato | da fare |

`soliton_simulator.py` **non è stato modificato**: blob `f5887254`, `git status` pulito. La FASE A è
**sola lettura del sorgente**: nessun run è stato lanciato per produrla. I numeri di contorno
(`Lam` che cresce, floor attivo sul 99.7 %) vengono da misure **già committate**, non da run nuovi.
