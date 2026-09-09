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

## 4. Stato repo (branch-specifico)

- **`dev-spinoriale`**: fondazione documentale committata (3 doc sotto `doc/`). NIENTE codice.
- **`dev-dof`**: commit `97c4586` (tracing per-passo §48) — verifica se pushato.
- **`main`**: doc canonica fino a §46-ter; §47 (fix chi-basc/tre freni) + §48 (tracing) da
  allineare a valle (vivono in memoria repo + relazione su `dev-dof`).
- **REGOLA d'ora in poi**: ogni relazione/commit dichiara il branch. `dev-dof` (spin-½ sul
  vecchio, chiuso: abeliano) ≠ `dev-spinoriale` (rifondazione, in corso).
