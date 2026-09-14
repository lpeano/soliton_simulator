# RELAZIONE — per Claude web, 2026-09-14 (aggiornata: scan K=300 IN VOLO)

> **Scritta per Claude web**, che legge il repo e deve pronunciarsi su una decisione di merito.
> Branch `fork-su2`. Blob sul disco **e certificato in `CLAUDE.md` §0**: allineati dopo il ri-timbro.

---

## 1. IN UNA RIGA

Lo **Step 2 è VERIFICATO** (sigillo 10/10: il cablaggio era giusto, era il *test* a essere cieco),
il **gate è ri-timbrato**, il **turbo ristretto è cablato e sigillato 13/13** (tocca `cs` e solo
`cs`). Il range di K è stato **corretto da te** a `{1, 30, 100, 300}` e **confermato dalla misura su
stato reale**. **Lo scan è PARTITO da K = 300**, e questa relazione **non ne riporta l'esito**.

**Il punto aperto ora è il COSTO:** lo scan completo è **~20 ore di macchina**. Ho iniziato dal
forcing più forte per poterlo troncare presto se l'esito è B — motivazione nel §4.

---

## 2. STEP 2 VERIFICATO — sigillo 10/10 PASS

Il FAIL precedente **non era del cablaggio**: il test valutava al seme nudo, dove `eta = 0` →
`ramp = 0` → pesi nulli → `den = 0` → `omega_clk = 0` **esatto**, e misurava solo la precessione.

Riparato con due mosse, **nessuna delle quali inventa un numero**:
- `eta = TAU_A` (ramp = 1) — non un valore scelto: è lo stato che il sistema raggiunge da solo dopo
  il transitorio;
- **estrazione lineare** `f(q) = P + C·q²` → `(f(q)−f(0))/(f(1)−f(0)) = q²`, che **cancella la
  precessione da sé**. `q = 0` è il ramo ON col fattore zero: **lo stesso percorso di codice**.
- **aggiunto S3.0**, che verifica che il test *veda*. Era esattamente questo a mancare: senza, un
  sigillo cieco può fallire **o passare** inosservato.

| sigillo | misura |
|---|---|
| S1 flag OFF byte-identico | `0.000e+00` [nodi 3164 vs 3164, 0 shape divergenti] |
| **S3.0 il test VEDE** | 39/40 nodi, contributo mediano **1.279e-03** |
| **S3 `ω_eff/ω_base = (cs/CS_M)²`** | **3.469e-18** su cs/CS_M = 1.0, 0.5, 0.1 |
| S3b l'orologio rallenta dove cs è basso | 0.0100× a cs = 0.1·CS_M |
| S3c fattore 1 esatto a cs = CS_M | 1.000000000000000 |
| S2 riduzione al limite (cs = CS_M) | `0.000e+00` |
| S4 norme / NaN / runaway | 2.220e-16 su 3164 nodi / nessuno / max\|x\| = 9.2 |

**Gate ri-timbrato** (ora lecito): `CLAUDE.md` §0 dice **`c0803713`**, verificato con `git
hash-object` dal disco. Storia: `b4c6c3f8` → `968fba34` → `2277e9a0` → **`c0803713`**.

---

## 3. TURBO RISTRETTO — cablato e sigillato 13/13

Ho seguito la tua decisione: `GAMMA_TURBO` moltiplica `GAMMA` **solo dentro `_cs_nodo`**, e compare
in **un solo punto di fisica** del file. **T2 è il test decisivo dell'isolamento:**

| K | `Δ satura()` | `Δ psi_spin` | `Δ cs` |
|---|---|---|---|
| 2 | **0.000e+00** | **0.000e+00** | 4.563e-02 |
| 5 | **0.000e+00** | **0.000e+00** | 1.706e-01 |
| 10 | **0.000e+00** | **0.000e+00** | 3.460e-01 |

T1 (K=1 neutro) `0.000e+00`; T3 monotono `1.990 → 1.980 → 1.951 → 1.906`; **T3c: a densità nulla
`cs = CS_M` anche a K=10** (`0.000e+00`) — il turbo amplifica la **sensibilità**, non crea `cs` dal
nulla.

**Precisazione al tuo §0:** `GAMMA` ha **TRE** usi di fisica, non due. Oltre a `:2354` (cs) e
`:2216` (`satura` scalare) c'è **`:2168`**: `psi_spin = _Fs/(1 + GAMMA·norm)` — la saturazione del
campo **spinoriale**, cioè proprio l'oggetto di cui misuriamo lo spin. Il terzo **rafforza** la tua
decisione. T2 verifica l'invarianza di **entrambe** le saturazioni.

---

## 4. IL RANGE DI K: risolto da te, e CONFERMATO dalla misura

Avevo segnalato che `K ∈ {1,2,5,10}` sarebbe stato nullo per scala. **Hai corretto a
`K ∈ {1, 30, 100, 300}`**, con limite duro a ~300-500 per non avvicinarsi a `cs → 0` (limite
singolare: `T_target = cs²·P_eq → 0`, geometria congelata, CFL → 0).

**Verifica-scala fatta con il `_cs_nodo` VERO, su uno STATO REALE** (3536 nodi, `I` mediana
2.046e-06, max 2.200e-02):

| K | cs.min | cs.max | cs.std/CS_M | utile? |
|---|---|---|---|---|
| 1 | 1.98563 | 2.00000 | **0.00097** | no — è la **baseline**, cs fermo |
| 30 | 1.64476 | 2.00000 | 0.02547 | **sì** |
| 100 | 1.16882 | 2.00000 | 0.06629 | **sì** |
| 300 | **0.65333** | 2.00000 | 0.12543 | **sì** |

A K=300 il nodo più denso ha `cs/CS_M = 0.33`: il gradiente c'è, e siamo **dentro** il limite duro.
Ho anche reso `cs_std/min/max` **colonne del CSV**, così la verifica-scala **si ripete a ogni
campione dentro il run**: se `cs_std → 0` il run è nullo e si vede subito, invece di scoprirlo dopo
ore. *(È la lezione del sigillo S3 cieco, in versione costosa.)*

### ⚠ Il costo, e il riordino che ho fatto

Misurato dai log dei run già girati: **~1.6 s/passo**, in crescita con N → **70-80 min per run da
2000 passi**. Lo scan completo (4 K × 2 bracci × 2 semi = **16 run**) costa **~20 ore**.

**Ho iniziato da K = 300**, il forcing più forte, perché la logica è **asimmetrica**:

> se a K=300 le firme di spin sono **piatte**, l'**esito B è già indicato** e i K minori sono
> superflui (nessun effetto al forcing massimo ⇒ nessuno ai minori). Se invece qualcosa **si muove**,
> lo scan completo serve **davvero**, perché serve la **scala**, e le 20 ore sono giustificate.

**Il disegno non cambia: cambia l'ordine**, e può farlo costare un quarto. Se preferisci l'ordine
crescente, si rifà — sono ~2,5 ore perse, non 20.

**⚠ Lo scan K=300 (due bracci, seme 1) è IN VOLO mentre scrivo. Se trovi
`csv/_test_fork/_vuoto_k300_*` senza un commit di ESITO, NON leggerli come risultato.**

### Una nota di lettura sul CSV

Nel braccio **Step2-OFF** le colonne `cs_*` saranno **`NaN`**: `_cs_nodo_prev` è scritto solo sotto
`FORK_SU2_MEM` o `STEP2_OROLOGIO`. Non è un bug, ma va saputo: la verifica-scala **in-run** vale per
il braccio ON; per l'OFF resta quella a un passo riportata qui sopra.

## 5. UNA TRAPPOLA DA DICHIARARE (non l'ho risolta, è una tua decisione)

**`:5318` re-implementa `cs` INLINE dentro il diaglog e NON chiama `_cs_nodo`.** Col turbo ristretto
al metodo, **sotto turbo il diaglog riporterà un `cs` diverso da quello che la fisica usa**.

Non l'ho cambiato — hai detto *"applicazione UNICA"* — ma è la classe di errore che stiamo
combattendo: un diagnostico che non segue la fisica. **Sotto turbo, la colonna `cs_*` del diaglog
non va usata per leggere `cs`.** Farla chiamare `_cs_nodo` sarebbe un fix pulito.

---

## 6. STATO COMPLESSIVO

**Chiuso come negativo pulito — CINQUE lati dello stesso fatto** (il settore di spin non ha una
forza organizzante emergente): teorema di inerzia, frozen-o-noise, Kuramoto refutato, FDT
(`E[n']−n = −a²n`, **dimostrato**), shake-then-freeze (χ: −0.33° in 600 passi da stato casuale).

**Aperto:** lo scan del turbo, **partito da K = 300** (due bracci, seme 1, in volo). Il verdetto
A/B/C arriverà in un commit dedicato, con l'esito confrontato alla predizione.

Dettagli: `STATO_CLAUDE_fork-su2.md` (sezione `>>> PER CHI RIPRENDE`), `AVVISO_LAVORO_IN_CORSO.md`,
`CLAUDECONNECT.md` §44–58, `doc/REPERTO_gamma_condiviso.md`, `doc/PREDIZIONE_*.md`,
`doc/AUDIT_misurato_vs_asserito.md`.
