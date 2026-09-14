# REPERTO — `GAMMA` non è il parametro di `cs`: è CONDIVISO con la saturazione del campo

> Trovato il 2026-09-14 mentre si preparava il **turbo su γ** (`--gamma-turbo K`).
> **Cambia il disegno dell'esperimento**, e va deciso prima di girare.
> Branch `fork-su2`, verificato dal sorgente sul blob `c0803713`.

---

## 1. IL FATTO

Il mandato del turbo dice: *"Amplifica γ (la **sensibilità di cs a ρ**), NON l'effetto sullo spin.
γ è il parametro che accende cs; cs poi fa il resto per la sua strada."*

**Ma `GAMMA` non è il parametro di `cs`.** Compare in quattro punti, e due sono fisica:

| riga | espressione | cosa governa |
|---|---|---|
| **`:2354`** | `cs_floor = CS_M / (1 + GAMMA*sqrt(I))` | **`cs`** — quello che si vuole svegliare |
| **`:2216`** | `satura(f) = f / (1 + GAMMA*sqrt(\|f\|^2 + 1e-9))` | **la SATURAZIONE del campo Ψ stesso** |
| `:3288` | `s = sign(interf)*\|interf\| / (1 + GAMMA*sqrt(\|interf\|))` | rendering volumetrico (non fisica) |
| `:5318` | copia di `cs_floor` | diagnostica |

`satura()` non è un dettaglio: è la saturazione che il campo subisce **ovunque** — in
`calcola_psi`, nella mitosi, nella torsione. È fisica centrale.

---

## 2. PERCHÉ CAMBIA L'ESPERIMENTO

Un `--gamma-turbo K` applicato **globalmente** a `GAMMA` moltiplicherebbe **anche `satura()`**.
Non sarebbe *"amplificare la sensibilità di cs a ρ"*: sarebbe **cambiare la dinamica del campo**,
cioè un esperimento diverso — e, peggio, **inattribuibile**.

Il braccio di controllo previsto (Step2-ON vs Step2-OFF a parità di `K`) **non lo isolerebbe**:
entrambi i bracci avrebbero il campo alterato allo stesso modo, quindi la differenza fra i due
misurerebbe ancora solo lo Step 2 — ma **su un sistema che non è più quello di riferimento**, e
l'estrapolazione verso `K=1` (il test di forma del §3 del mandato) confronterebbe **due fisiche
diverse**, non due scale della stessa.

---

## 3. LA VIA PULITA

> **Il turbo deve moltiplicare `GAMMA` SOLO dentro `_cs_nodo` (`:2354`)**, lasciando `satura()`
> intatta. Più `:5318`, che è la copia diagnostica di `cs_floor`, per coerenza fra la fisica e ciò
> che il diaglog riporta.

Così `--gamma-turbo K` fa **letteralmente** quello che il mandato chiede: alza la sensibilità di
`cs` alla densità, e nient'altro. `cs` poi fa il resto per la sua strada, e il braccio di controllo
isola davvero lo Step 2.

**Nota sul par.3 (zero manopole):** il turbo **è** un parametro nuovo, e non si finge che non lo
sia. È legittimo solo perché è dichiarato **amplificatore diagnostico**, OFF di default, mai nel
percorso certificato, e perché il criterio non è *"l'effetto appare"* ma **"l'effetto scala in modo
ordinato con `K` ed estrapola con continuità verso `K=1`"**. Un effetto che esiste solo a `K` grande
e cambia forma togliendo il turbo è un **artefatto**, ed è l'esito C previsto.

---

## 4. COSA RESTA DA DECIDERE (non lo decide l'esecutore)

Applicare il turbo solo a `:2354` è la lettura fedele del mandato, **ma è una deviazione da come era
scritto** ("amplifica γ"), e va confermata. L'alternativa — turbo globale su `GAMMA` — è un
esperimento **diverso e legittimo in sé** (*"cosa succede se il campo satura più forte E cs si
sveglia?"*), ma **non è quello che il mandato voleva testare** e non sarebbe attribuibile con il
controllo previsto.

**Finché non c'è conferma, il turbo non viene acceso.**
