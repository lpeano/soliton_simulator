# ROADMAP dev-spinoriale — PIANO COMPLETO (logica + matematica + todo)

> Piano pluri-sessione, da eseguire A STEP con CHECKPOINT a Luca tra ognuno.
> **Scritto ora, NON ancora eseguito** (Step 0 saltato, Step 1A da lanciare alla ripresa).
> I TODO operativi vivono anche in `/memories/repo/roadmap_todo.md` (persistenti tra sessioni).
> Lingua: italiano.

## RIPARTENZA (precondizione ferrea)
- Blob certificato: `git hash-object soliton_simulator.py` **deve** dare `4fc7a794...`
  (codice con misura Bargmann, gate PASS, commit `f29d73f`).
- Se il blob è diverso → **FERMATI e segnalalo**: si riparte da lì, non da altro.
- Verificato il 2026-09-11: blob = `4fc7a794fb5f...` ✓.

---

## CONTESTO SCIENTIFICO
Obiettivo: verificare se dal sistema relazionale emergono **EM e gravità** come due
proiezioni dello **STESSO** campo spinoriale ψ, con la giusta gerarchia.

I due canali **GAUGE-INVARIANTI** (mai Re/Im per-arco, che sono gauge-dipendenti):
- **GRAVITÀ = canale DENSITÀ**: ρ=|ψ|² → cs (metrica). GAMMA vive qui.
- **EM = canale FASE**: struttura di fase / segno di doppia-copertura.
  - NB: l'olonomia di Bargmann (`berry_segno`) è **CIECA al segno** (telescoping: le fasi
    per-nodo si cancellano sul ciclo chiuso). Il segno è gauge-relativo; la misura giusta è
    il **phase-locking TEMPORALE (SYNC/Kuramoto)**, non un invariante di ciclo chiuso.

### CHIARIMENTO CRITICO — Re/Im NON sono i due canali (correzione di Luca)
ERRORE da evitare: identificare "EM = Im⟨ψ_i|ψ_j⟩" e "segno/gravità = Re". È SBAGLIATO:
1. **Re e Im dello STESSO overlap non sono indipendenti**: ⟨ψ_i|ψ_j⟩=|ov|·e^{iΔ},
   Re=|ov|cosΔ, Im=|ov|sinΔ. Un SOLO grado di libertà (la fase Δ) li determina entrambi →
   coseno e seno dello stesso angolo NON possono avere dimensioni di scala diverse.
   Non sono due canali: sono due proiezioni di uno.
2. **La separazione Re/Im è GAUGE-dipendente**: dipende dal frame locale canon(nb); una
   rotazione di fase mescola Re↔Im. Non è fisica (stesso motivo per cui segno_arco per-arco
   è gauge-dipendente e serviva Bargmann… che però telescopa).

**SEPARAZIONE FISICA CORRETTA (gauge-invariante): MODULO vs FASE**
- **GRAVITÀ = MODULO |ψ|²** (momento quadratico): ampiezza, densità, sempre +, attrattiva, dimensionale.
- **EM = STRUTTURA DI FASE / AVVOLGIMENTO** (momento lineare): segno di doppia-copertura ±,
  carica topologica. Firmato, adimensionale.

**RUOLO DI Im NELLA FORZA (non confondere motore e carica):**
- La forza di interferenza USA Im⟨ψ|ψ⟩ come **MOTORE DINAMICO** (fa evolvere le fasi) — corretto
  nel codice, **NON va cambiato**.
- Ma la carica EM NON è "Im della forza": è l'**AVVOLGIMENTO/segno** che cavalca la fase. Vive
  nel phase-locking temporale (SYNC), non in una componente per-arco.
- Quindi nei test (Step 1 e 2): misurare come scalano **MODULO (densità)** e **FASE/segno (via
  SYNC temporale)** — **MAI Re/Im per-arco** (gauge, non separabili).

### Legge base della metrica
`cs = CS_M / (1 + GAMMA·√I)`, con `I=|ψ|²`, `CS_M=2.0`, `GAMMA=0.05`.
- Attivazione gravità nonlineare: `GAMMA·√I ~ 1` → `I ~ 1/GAMMA² = 400`.
- Run attuale: `I ~ 0.05` → gravità nonlineare **NON attiva** (fattore ~8200 sotto → serve
  GAMMA ~91× in assoluto, o ~6× col floor relazionale grazie al contrasto).

---

## GLI STEP (in ordine, con dipendenze e matematica)

### STEP 0 — [SALTATO per decisione di Luca]
- seed-2 **NON eseguito**. Il verdetto (B) di seed-1 è usato come **BASELINE INTERNA** (la "riga
  zero" per Step 2, l'accoppiamento cs↔orologio), **NON** come risultato pubblicabile/robusto.
  Motivo: serve un riferimento contro cui misurare se l'accoppiamento cambia qualcosa, non una
  statistica multi-seed.
- **TODO APERTO (non abbandonato)**: se in futuro il (B) dovrà essere presentato come risultato
  STABILITO (non solo baseline), seed-2 e seed-3 restano da fare (robustezza alla condizione
  iniziale). Per ora: rimandato.
- Si parte diretti da **Step 1A**.

### STEP 1 — COARSE-GRAINING: 3 REGIMI DI GAMMA
**Matematica:** blocco di `b` solitoni, campo fuso ψ_bloc = Σ_k ψ_k.
- coerente:   I_bloc ~ b²·I → γ·√I ~ γ·b        (rilevante)
- incoerente: I_bloc ~ b·I  → γ·√I ~ γ·√b       (rilevante più debole)
- **frustrato (il nostro caso): somma incoerente.**
- Dimensione di scala: γ_eff(b) ~ b^d ; d>0 rilevante, d~0 marginale, d<0 irrilevante.
- **Verdetto cercato**: FASE marginale (d~0) + DENSITÀ irrilevante (d<0) dallo STESSO γ =
  **gerarchia EM/gravità emersa**.
- Misurare SOLO nei due canali gauge-invarianti (modulo per densità; fase/segno via SYNC per EM).
  **MAI Re/Im per-arco.**

**Fase 1A (pure-read, NON tocca il .py) — DA LANCIARE ALLA RIPRESA:**
- `csv/_test_53c/_run_3gamma.ps1` (serie, mai parallelo) + `_analizza_3gamma.py` (fitta d nei due
  canali). **Sigillo b=1 = identità byte-identico** (se fallisce → STOP).

**Fase 1B (SOLO a run finiti, tocca il .py con flag):**
- flag `--gamma-nudo` (no `_fattori_coarse`) e `--gamma-relazionale`
  (`cs=CS_M/(1+γ·√(I/I_tipica))`, `I_tipica`=mediana stabile).
- 3 regimi: **R1** classico γ·B^(−1/2) (controllo, atteso invariante); **R2** nudo; **R3** relazionale.

**CHECKPOINT**: Luca legge d nei due canali prima di Step 2.

### STEP 2 — ACCOPPIAMENTO cs↔OROLOGIO (un solo tempo proprio)
**DIPENDE da Step 1**: serve cs ATTIVO (floor relazionale R3), sennò test NULLO.
**PROBLEMA**: oggi due tempi propri SCOLLEGATI:
- (a) metrico  `tau = d/cs`   (riga ~2610, gravità, usa cs)
- (b) orologio `dt_n = DT·r`  (riga ~2227/1839, de Broglie, NON usa cs)

**Matematica dell'accoppiamento (DERIVATA, non tarata):**
- de Broglie: ω_clk = m·c²/ħ, con c → cs (velocità luce locale) → ω_clk_locale = m·cs²/ħ ~ cs²
- → fattore (lapse): `ω_clk → ω_clk · (cs/CS_M)²`
- Solo la **MAGNITUDINE** si accoppia (gravità); il **segno s_k=±1 resta INVARIATO** (EM).

**SIGILLI (obbligatori):**
- riduzione al limite: cs=CS_M → (cs/CS_M)²=1 → **BYTE-IDENTICO** al de Broglie attuale.
- l'identificazione dt_n_clk = f(d/cs) è una **CONSTRAINT fisica, non un knob**.
- norma |ψ|=1, no NaN, **STABILITÀ** (il loop ρ→cs→orologio→fase→campo→ρ può essere instabile:
  sigillo di stabilità oltre alla norma).

**CAVEAT:** (1) telescoping regge, Bargmann resta cieco → misura = phase-locking temporale (SYNC);
(2) unificare il tempo NON basta senza SYNC (segno orfano); (3) BASELINE = il (B) frustrato del
de Broglie attuale. NON è inquinato: è la RIGA ZERO contro cui misurare. NON buttarlo.

**CHECKPOINT**: Luca legge se il segno si organizza (SYNC/phase-locking) prima di Step 3.

### STEP 3 — [ESPLORATIVO — solo tracciare, NON progettare né scrivere codice ora]
**MASSA MINIMA GRAVITANTE / α_G.** Postulato: lunghezza d'onda del solitone = 2·lunghezza di Planck.
**Matematica (struttura, da raffinare):**
- N solitoni frustrati per accendere la gravità: I_N ~ N·i_0 = 400 → N ~ 400/i_0.
- N in unità di solitone = α_G (debolezza gravità vs scala fondamentale), NON G in SI (sistema
  relazionale: dà rapporti, non metri).
- Postulato Planck + cs + ħ: ℓ_P=√(ħG/c³) VINCOLA G (adimensionale).

**⚠ AVVISO DI MAGNITUDINE (non cancellare):** il meccanismo dà la DIREZIONE giusta (aggregazione
→ gravità debole), ma la MAGNITUDINE NON torna: N~8000 → α_G~10⁻⁴, contro il reale ~10⁻³⁹.
**DIVARIO DI ~35 ORDINI** che il meccanismo attuale NON copre. Step 3 è un ORIZZONTE, NON un
traguardo. Non trattarlo come "quasi fatto". Nessun codice ora.

---

## REGOLE (non negoziabili)
- **NIENTE copia del .py**: le modalità sono FLAG sullo stesso blob.
- Modifiche al .py SOLO a campagna/run in corso finiti (un fronte alla volta sul codice verificato).
  La fase pure-read (script/analizzatore) si può fare prima.
- Ogni step: commit+push approfondito (cosa/perché/come/numeri/cosa ricontrollare), dati+script
  committati, **gate ri-timbrato sul nuovo blob**, STATO_CLAUDE + ROADMAP aggiornati.
- Ogni **sigillo b=1=identità che FALLISCE → STOP**, non proseguire.
- **Mai Re/Im per-arco** come misura fisica (vedi CHIARIMENTO CRITICO).
- I **TODO sono PERSISTENTI** e attraversano PIÙ SESSIONI: non cancellarli a fine sessione,
  spuntare solo ciò che è certificato da Luca.

## PROSSIMA AZIONE ALLA RIPRESA
1. Verifica blob = `4fc7a794` (altrimenti STOP).
2. **Step 1A (pure-read)**: scrivere+lanciare `_run_3gamma.ps1` + `_analizza_3gamma.py`,
   sigillo b=1=identità byte-id. → CHECKPOINT a Luca.
3. Tutto il resto in attesa del via esplicito di Luca.
