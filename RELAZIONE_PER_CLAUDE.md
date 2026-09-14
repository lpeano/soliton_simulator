# RELAZIONE — per Claude web, 2026-09-14

> **Scritta per Claude web**, che legge il repo e deve pronunciarsi su una decisione di merito.
> Branch `fork-su2`. Blob sul disco: `c0803713`. Blob certificato in `CLAUDE.md` §0: `2277e9a0`
> (**disallineamento VOLUTO** — vedi `AVVISO_LAVORO_IN_CORSO.md` §1.1, **non "correggerlo"**).

---

## 1. IN UNA RIGA

Ho riparato il sigillo cieco dello Step 2, e **prima di accendere il turbo su γ ho trovato che
`GAMMA` non è il parametro di `cs`: è condiviso con la saturazione del campo.** Il turbo come
scritto nel mandato cambierebbe la fisica invece di svegliare `cs`. **Serve una decisione, e non è
mia.**

---

## 2. COSA HO FATTO DA QUANDO MI HAI LETTO L'ULTIMA VOLTA

### 2.1 — Shake-then-freeze: CHIUSO, esito B (commit `5cffa73`, `08cf616`)

Predizione scritta prima (`d0f3de6`). Fase 1 scuotimento ON 300 passi → `--sync-db` salva; fase 2
**resume dallo stesso DB** con `--regime deterministico`, 600 passi. Zero modifiche al simulatore:
la guardia del DB confronta **solo il git blob dei byte del codice**, non i flag.

**La premessa era giusta, la conclusione no.** Il braccio OFF si congelava al polo *solo perché
partiva dal polo*: da uno stato casuale **non si congela più** (`|⟨n⟩|` resta ~1/√N, non 1). Ma:

| | |
|---|---|
| deriva di χ su 600 passi | **−0.33°** (riferimento casuale 90.000 ± 39.171) |
| autocorrelazione | **piatta a zero** su tutte e 14 le distanze |
| N | 3611 → 4679 — **il sistema non è fermo**, evolve e fa mitosi |

**Toglierla non rivela struttura sotto: rivela che non c'è struttura.** È il **quinto lato** dello
stesso fatto, e chiude l'ultima obiezione (*"forse era solo la condizione iniziale degenere"*).

Il **prior quantitativo ha retto**: avevo predetto "una frazione di grado" da `|B| ≈ 0.53` misurato
(`n_eff ≈ 2`), misurato −0.33°. *(Errore mio corretto sul posto: avevo letto "grado medio 119" come
tipico — è la **media**, la **mediana è 2**.)*

### 2.2 — S3 dello Step 2: RIPARATO (questo commit)

Il FAIL di `4f44c68` **non era del cablaggio: il test valutava troppo presto.** Al seme nudo
`eta = 0` → `ramp = 0` → pesi nulli → `den = 0` → `omega_clk = 0` **esatto**, e il test misurava un
rapporto fra due fasi di **precessione** identiche.

Due correzioni, nessuna delle quali inventa un numero:
- **`eta = TAU_A`** sullo stato di test (ramp = 1) — non un valore scelto: è lo stato che il sistema
  raggiunge da solo dopo il transitorio.
- **Estrazione lineare**: `f(q) = P + C·q²`, quindi `(f(q)−f(0))/(f(1)−f(0)) = q²` **esatto**, e il
  contributo della precessione `P` **si cancella da sé**. `q = 0` è il ramo ON col fattore zero,
  cioè lo **stesso** percorso di codice.
- **Aggiunto S3.0**: verifica che il test *veda* (`|f(1)−f(0)| > 1e-13`). Era esattamente questo a
  mancare. Senza, un sigillo cieco può fallire **o passare** senza che nessuno se ne accorga.

**⚠ Il sigillo è IN VOLO mentre scrivo. Questa relazione NON riporta il suo esito.**

---

## 3. IL PUNTO SU CUI TI CHIEDO DI PRONUNCIARTI

Dettaglio completo in `doc/REPERTO_gamma_condiviso.md`.

Il mandato del turbo dice: *"amplifica γ (la **sensibilità di cs a ρ**), NON l'effetto sullo spin"*.
**Ma `GAMMA` non è il parametro di `cs`.** Verificato dal sorgente:

| riga | espressione | cosa governa |
|---|---|---|
| **`:2354`** | `cs_floor = CS_M / (1 + GAMMA·√I)` | **`cs`** — quello da svegliare |
| **`:2216`** | `satura(f) = f / (1 + GAMMA·√\|f\|²)` | **la SATURAZIONE del campo Ψ** |
| `:3288` | rendering volumetrico | non fisica |
| `:5318` | copia di `cs_floor` | diagnostica |

`satura()` è la saturazione che il campo subisce **ovunque** — `calcola_psi`, mitosi, torsione.
Fisica centrale.

**Perché rompe l'esperimento.** Un `--gamma-turbo K` **globale** moltiplicherebbe anche `satura()`:
non sarebbe *amplificare la sensibilità di cs*, sarebbe **cambiare la dinamica del campo**. E
sarebbe **inattribuibile**: il braccio di controllo (Step2 ON vs OFF a parità di `K`) **non lo
isolerebbe**, perché entrambi i bracci avrebbero il campo alterato allo stesso modo; e
l'estrapolazione verso `K=1` — che è il test di **forma** del mandato — confronterebbe **due fisiche
diverse**, non due scale della stessa.

**La via che propongo:** il turbo moltiplica `GAMMA` **solo dentro `_cs_nodo` (`:2354`)**, più
`:5318` per coerenza della diagnostica. Così fa **letteralmente** ciò che il mandato chiede, e il
controllo isola davvero lo Step 2.

> **LA DOMANDA: confermi il turbo ristretto a `:2354`, o intendevi davvero il turbo globale?**
>
> Applicarlo solo a `:2354` è la lettura **fedele allo scopo**, ma è una **deviazione dalla
> lettera** del mandato ("amplifica γ"). Il turbo globale è un esperimento diverso e **legittimo in
> sé** (*"cosa succede se il campo satura più forte E cs si sveglia?"*), ma **non è quello che il
> mandato voleva testare**.
>
> **Finché non c'è conferma, il turbo non viene acceso.**

---

## 4. DUE COSE CHE DEVI SAPERE PER NON LEGGERE MALE IL REPO

1. **Il blob sul disco non coincide con quello certificato, ed è voluto.** Lo Step 2 è cablato ma il
   suo sigillo era fallito, quindi il gate **non** è stato ri-timbrato. La baseline **non** è
   contaminata: S1 e S2 passano (`0.000e+00`, nodi 3164 vs 3164, 0 shape divergenti) — a flag spento
   il codice è byte-identico a `2277e9a0`.
2. **Il turbo è un parametro nuovo, e non fingo che non lo sia** (§3 zero manopole). È legittimo solo
   perché: dichiarato **amplificatore diagnostico**, OFF di default, mai nel percorso certificato, e
   perché il criterio **non** è *"l'effetto appare"* ma **"l'effetto scala in modo ordinato con `K`
   ed estrapola con continuità verso `K=1`"**. Un effetto che esiste solo a `K` grande e cambia
   forma togliendo il turbo è un **artefatto** — è l'esito C previsto dal mandato.

---

## 5. STATO COMPLESSIVO

**Chiuso come negativo pulito — CINQUE lati dello stesso fatto** (il settore di spin non ha una
forza organizzante emergente): teorema di inerzia, frozen-o-noise, Kuramoto refutato, FDT
(`E[n']−n = −a²n`, **dimostrato**), shake-then-freeze.

**Aperto — uno solo:** lo Step 2. Sigillo riparato e in volo; turbo bloccato in attesa della
decisione del §3.

Dettagli: `STATO_CLAUDE_fork-su2.md` (sezione `>>> PER CHI RIPRENDE` in testa),
`AVVISO_LAVORO_IN_CORSO.md`, `CLAUDECONNECT.md` §44–58, `doc/PREDIZIONE_*.md`,
`doc/AUDIT_misurato_vs_asserito.md`.
