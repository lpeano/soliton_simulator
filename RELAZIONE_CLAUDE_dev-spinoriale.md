# RELAZIONE per Claude — branch `dev-spinoriale` (2026-09-09)

> **BRANCH: `dev-spinoriale`** (diramato da `dev-dof`). D'ora in poi OGNI relazione e OGNI
> commit specifica ESPLICITAMENTE il branch. Non confondere i branch:
> - **`dev-dof`** = ricerca spin-½ sul sistema ATTUALE (campo scalare U(1) abeliano). Verdetto:
>   il core è ABELIANO, lo stato a segno ordinato è un repulsore (§40–48, vedi `main` + memoria repo).
> - **`dev-spinoriale`** = REFACTORING RIFONDATIVO (questo branch): lo spinore diventa
>   FONDAMENTALE e il campo Ψ è ciò che esso emette. Progetto parallelo di settimane.

---

## 0. TL;DR

- Nuovo branch **`dev-spinoriale`** (da `dev-dof`, commit fondazione). Contiene SOLO la
  fondazione documentale — **NIENTE codice ancora**. Il sistema attuale resta intatto.
- **Idea (visione di Luca dai 12 anni):** il solitone è uno **spinore SU(2) che EMETTE un
  campo** (la "sfera con l'otto"), non una fase scalare con lo spinore aggiunto.
  L'inversione ontologica: **campo → spinore** diventa **spinore → campo**.
- **Perché:** il sistema attuale è abeliano perché il *fondamentale* (Ψ, campo U(1)) è
  abeliano. Se il fondamentale è lo spinore (SU(2)), il non-abeliano è **incorporato**,
  non innestato. Le vie fallite su `dev-dof` testavano meccanismi non-abeliani sopra un
  fondamentale abeliano; qui si cambia l'OGGETTO.
- **Ipotesi da testare:** la materia = interferenza NON distruttiva del campo spinoriale
  richiede accordo di direzione **E** di segno di doppia-copertura → la densità ρ stessa
  **seleziona** i segni concordi → lo spin ½ diventa costitutivo della materia, non
  un'etichetta.

## 1. Documentazione (tutta sotto `doc/`)

- **`doc/FONDAZIONE_SPINORIALE.md`** — SCIENTIFICO: fisica + Leggi I–X (campo emesso,
  materia=interferenza non distruttiva, saturazione, overlap, forze, schermatura, gravità
  bifase, evoluzione SU(2), tempo proprio, coppie) + Parte III geometria di contatto
  (forma α, campo di Reeb=orologio de Broglie, distribuzione ξ=grafo di adiacenza,
  non-integrabilità=non-abeliano=spin ½).
- **`doc/REFACTORING_SPINORIALE.md`** — TECNICO: il punto di rottura (`calcola_psi`, riga
  ~1905: `F` dallo spinore invece di `e^{iφ}`), campo `(n,2)`, flag master
  `--campo-spinoriale` (default OFF = byte-identico), mappa dell'intreccio (cosa toccare /
  cosa preservare), fasi 1–4 con sigilli di **riduzione-al-limite**, linea rossa.
- **`doc/ONTOLOGIA_SPINORIALE.md`** — ONTOLOGIA: entità fondamentali (spinore, grafo) vs
  emergenti (campo, materia, direzione, segno, forze, gravità, tempo, spin ½); le tre
  categorie (fondamentale/relazionale/emergente); l'ontologia della geometria di contatto
  (Reeb=tempo, ξ=spazio, non-integrabilità=spin ½); il contrasto col sistema scalare.

## 2. La linea rossa (rispettata)

- Il cambio nasce dal **principio** (il solitone È uno spinore che emette), NON dal
  desiderio dello spin ½.
- Ogni legge nuova deve **ridursi al vecchio** nel limite (spinori tutti in fase
  `ψ=(e^{iφ/2},0)` → campo scalare `Ψ=e^{iφ}`). Il **sigillo riduzione-al-limite**
  distingue "l'inversione" da "un sistema arbitrario".
- **Zero parametri nuovi**: stesso kernel `_mat(w)`, stessa λ, stesso K. Cambia l'oggetto
  (scalare→spinore), non le costanti.

## 3. Piano (fasi, ognuna con sigillo)

- **Fase 1**: `calcola_psi` spinoriale dietro `--campo-spinoriale` (campo `(n,2)`,
  `ρ=ψ†ψ`). Sigillo: spinori in fase → torna il campo scalare (byte-identico nel limite).
- **Fase 2**: gravità + densità sul nuovo campo. Sigillo: gravità ∝ nb·nb invariata.
- **Fase 3**: forze di fase → overlap spinoriale ⟨ψ_i|ψ_j⟩. Sigillo: si riduce a cos(Δφ).
- **Fase 4**: mitosi/twist/chiralità nativi; creazione coppie a segno opposto.
- **Test finale (la visione)**: la densità (materia) segue i segni concordi? Se sì →
  spin ½ nativo, non aggiunto.

## 3-bis. Sigilli OBBLIGATORI (fissati dalla fondazione, in `doc/REFACTORING_SPINORIALE.md`)

- **S1 — Causalità (ETC rigoroso)**: nel nuovo sistema il loop emitter-campo è PIÙ stretto
  (il campo Ψ *è* fatto degli spinori). Campo da snapshot t−1, commit atomico, sigillo
  **no-loop-istantaneo** (Jacobi non Gauss-Seidel), convergenza-dt come prova di causalità.
- **S2 — Tempo proprio = campo di Reeb**: la geometria di contatto dà il criterio ESATTO
  (α(R)=1, dα(R,·)=0), il **battito sull'otto (4π non 2π)**, convergenza-dt covariante
  N-appaiato. Molto più forte del vago "converge?" del vecchio.
- **S3 — Riduzione al limite**: spinori in fase → campo/causalità/tempo-proprio del vecchio.
  Se non si riduce, è un sistema arbitrario, non l'inversione.
- **Perché fin d'ora**: implementare *per essere verificabile*. Causalità e tempo proprio
  sono al CUORE del nuovo sistema (struttura emitter-campo; geometria di contatto), non ai margini.

## 4. Stato repo (branch-specifico) — tutto allineato e pushato

- **`dev-spinoriale`** (`81241d0`): fondazione documentale (3 doc sotto `doc/`) + sigilli
  S1/S2/S3 in `doc/REFACTORING_SPINORIALE.md`. **FASE 1 FATTA**: flag `--campo-spinoriale`
  (default OFF byte-identico) + campo Psi spinoriale (n,2) in `calcola_psi` (in PARALLELO,
  non ancora agganciato). Sigilli PASSATI: **S3 riduzione-al-limite ESATTO** (`ψ=(e^{iφ},0)`
  → comp0 == scalare, max|Δ|=0.000e+00; comp1=0), S1 causalità (Jacobi/no-mutazione), OFF
  byte-identico, coerenza (ρ≥0), e **GENUINAMENTE spinoriale** (test deterministico A/B:
  ψ=(e^{iφ},0)→solo comp0; ψ=(0,e^{iφ})→solo comp1; componenti INDIPENDENTI). NB: con spinori
  casuali il campo è ~1e-7 (si cancellano per interferenza distruttiva, Legge II) → il test
  giusto è l'INDIPENDENZA delle componenti, non l'ampiezza (un primo test con soglia assoluta
  dava falso "degenere", corretto). Backup `soliton_simulator.backup_2026-09-09_campo-spinoriale.py`,
  sigillo `csv/_seal_fase1/_sigillo_fase1.py`.
  **FASE 2 FATTA** (`59af724`): il campo spinoriale PILOTA densità e gravità (dietro
  `--campo-spinoriale`). Helper `_rho_sorgente` (|ψ|² off / rho_spin on) in `lambda_nodi`;
  `_nb_grav` (_nb off / **nb NATIVO** = ψ†σψ/rho_spin on) nella gravità bifase. Sigilli PASSATI:
  OFF byte-identico (bk vs off max|A-B|=0); **S3 riduzione-al-limite** in-process (densità 3.8e-29,
  nb 0.000e+00 esatto); **STABILITÀ** (300p spinore-vivo: N 824→1940, n_naninf=0, no blow-up);
  coerenza; controprova fuori limite (spinori inclinati → nb pilota direzione diversa = nuova
  fisica). **BUG stanato dal sigillo S3**: normalizzazione nb floor 1e-12 falliva per campo piccolo
  (~1e-7 cancellazione, |nbn|~1e-14) → FIX per rho_spin floor 1e-30. **PRIMO SGUARDO** (NON verdetto):
  spin_overlap_arco~0.5, segno_arco_coer~0 → segno NON ancora ordinato, ATTESO (Fase 2 = solo
  densità/gravità, non le forze; il canale è la Fase 3). Backup `soliton_simulator.backup_2026-09-09_fase2.py`,
  sigillo `csv/_seal_fase2/_sigillo_fase2.py`. **PROSSIMO: Fase 3** (forze/overlap ⟨ψ_i|ψ_j⟩) =
  dove si decide se la visione dà il non-abeliano.
- **`dev-dof`** (`5a4e754`): tracing per-passo §48 + **conferma 2 semi** del meccanismo
  repulsore. Pushato. **Capitolo CHIUSO**: core abeliano con meccanismo.
- **`main`** (`eab5db5`): doc canonica allineata §47/§48/§49. Pushato. Per lo stato del
  lavoro di qualunque branch, guarda `main`.
- **REGOLA d'ora in poi**: ogni relazione/commit dichiara il BRANCH. `dev-dof` (spin-½ sul
  vecchio, CHIUSO: abeliano con meccanismo repulsore) ≠ `dev-spinoriale` (rifondazione,
  IN CORSO: fondazione fatta, Fase 1 da implementare).

## 5. Il collegamento §48 ↔ §49 (perché la visione è la soluzione giusta)

Il tracing su `dev-dof` (§48) ha trovato il MECCANISMO del fallimento: nel sistema attuale
l'ordine del segno è un **repulsore dinamico** (segno = grado aggiunto, niente lo
stabilizza). Nel sistema spinoriale (`dev-spinoriale`), la **materia** richiede accordo di
segno (interferenza non distruttiva, Legge II) → l'ordine diventerebbe un **attrattore**
*per fisica*, non per un termine imposto. **Non è "proviamo il nuovo per disperazione": è
"l'attuale fallisce per un meccanismo preciso, e il nuovo lo risolve per costruzione".**
Il fallimento dell'uno è la mappa per l'altro.
