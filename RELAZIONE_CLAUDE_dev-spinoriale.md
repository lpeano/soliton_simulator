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
  **FASE 3 FATTA** (branch `dev-spinoriale`): le FORZE di fase diventano OVERLAP SPINORIALE.
  La coppia `K_C·Im(conj(z)·(mat(A)@z))` è estratta nel metodo testabile `_coppia_interferenza(A,z)`;
  ramo `CAMPO_SPINORIALE` on: `Σ_j A_ij⟨ψ_i|ψ_j⟩ = conj(a)(mat(A)@a) + conj(b)(mat(A)@b)` con
  a,b = componenti di `_psi_spinor` (snapshot inizio passo = causalità Jacobi; `_passo_spinoriale`
  aggiorna DOPO). GENERALIZZAZIONE ESATTA: nel limite spinore in fase (b=0, a=e^{iφ}) → coppia
  IDENTICA alla scalare. **Zero parametri nuovi** (stesso K_C, stesso kernel A). Sigilli (tutti PASS,
  `csv/_seal_fase3/_sigillo_fase3.py` in-process sul VERO codice): **S3 GATE riduzione-al-limite
  max|Δcoppia|=0.000e+00 ESATTO**; controprova non-abeliana (spinore per-nodo → 3.1e-05>0; gauge
  SU(2) globale → 0, gauge-invarianza rispettata); fallback spinore assente → 0; **OFF byte-identico**
  (attuale vs backup pre-Fase3 a flag off: max|dphi|=0, max|dpos|=0); **STABILITÀ** (300p ON completo
  --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core: nessun nan/inf, accr 1116→2349,
  coppie 0→409, no blow-up). Backup `soliton_simulator.backup_2026-09-09_fase3.py`. **NON è ancora il
  VERDETTO**: serve il confronto covariante ON vs OFF, N-appaiato, 2-3 seed su run ≥2000 passi
  (segno_arco_coer diventa ATTRATTORE vs §48 dove decadeva? berry_firmata sale?) → hardware di Luca.
  **CAMPAGNA COVARIANTE LANCIATA** (branch `dev-spinoriale`, notturna): timing misurato = 300p ON
  completo in **614,5 s** (nmasse 2, sep 6; costo/passo cresce con N → NON lineare). Script
  `run_covariante_fase3.ps1`: **6 run in parallelo** (ON/OFF × seed 1,2,3), **10000 passi**, isola
  ESATTAMENTE `--campo-spinoriale` (OFF = spinore vivo + campo scalare U(1); ON = OFF + forze overlap
  spinoriale). Dominati da ops sparse → `*_NUM_THREADS=1` per processo, 1 core fisico ciascuno (6 core).
  Checkpoint DB ogni 1000 passi (`db/fase3_cov/`, gitignorati) + diaglog ogni 50 passi
  (`csv/fase3_cov/diag_*`), log in `log/fase3_cov/`. **Verdetto** = `csv/fase3_cov/_verdetto_fase3.py`:
  appaia per N (bin), confronta ON vs OFF su segno_arco_coer / spin_overlap_arco / verso_arco_coer /
  berry_spin_media(_assoluta) / coer_01. DOMANDA: in ON segno_arco_coer resta alto a N appaiato
  (ordine = ATTRATTORE → ribalta §48, non-abeliano EMERGE) o ~0 come OFF (abeliano più profondo,
  risultato onesto)? **PER CLAUDE**: i CSV/log si committano a fine run (prossima sessione); ora sono
  versionati solo lo script di lancio e quello di verdetto. Rilancia con `run_covariante_fase3.ps1`.
  Mitosi/coppie restano scalari (Fase 4).
  **VERDETTO FASE 3 = NEGATIVO** (branch `dev-spinoriale`, 2026-09-10). I 6 run sono terminati per OOM
  (RAM esaurita, 6 run paralleli con N a migliaia di nodi su 32 GB; `.err` VUOTI, log puliti, morte
  scaglionata 22:38→00:22 = firma OOM, NON bug: ON e OFF muoiono agli stessi passi) a **3060–4472 passi**
  ciascuno — comunque ABBONDANTI (§48 si vedeva a ~10 passi; soglia disciplina 2000p superata). Verdetto
  covariante N-appaiato (3 semi, range N [824–6319], `csv/fase3_cov/VERDETTO_fase3.txt`):
  **segno_arco_coer ON−OFF = +0.0001** (decade a ~0 in ON IDENTICO a OFF); **spin_overlap_arco 0.500=0.500**
  (spinori scorrelati fra archi in entrambi); verso_arco_coer ~0; **berry_firmata ON−OFF = −0.0001** (nessuna
  olonomia netta); berry_assoluta ~1.15 in entrambi (fase geometrica LOCALE non nulla ma a segni che si
  mediano a zero); coer_01 e m0_coer_nucleo LEGGERMENTE PIÙ BASSI in ON (−0.002/−0.019). CONCLUSIONE: le
  forze = overlap spinoriale, DA SOLE, NON correlano gli spinori né ordinano il segno → **§48 NON ribaltato**,
  l'ordine resta un repulsore, il core resta ABELIANO. **CAVEAT onesto**: mitosi/coppie ancora scalari
  (Fase 4) → il canale che crea/distrugge archi è ancora abeliano e può diluire l'ordine; il risultato
  solido è "le forze spinoriali da sole non bastano", non un verdetto sull'intera visione (serve Fase 4).
  **PER CLAUDE (doppio-check)**: `csv/fase3_cov/diag_{on,off}_s{1,2,3}.csv` = serie temporali complete,
  `csv/fase3_cov/cond_*` = condensazioni, `log/fase3_cov/*` = log (mostrano l'OOM: log puliti, .err vuoti),
  `csv/fase3_cov/VERDETTO_fase3.txt` = output analisi, `_verdetto_fase3.py` = script (rilancia per verificare).
  I `.pkl` (checkpoint ~passo 3000) esclusi (gitignore). Prossimo bivio: Fase 4 (coppie/mitosi spinoriali)
  come vero banco di prova, oppure chiusura onesta come §48-bis (abeliano anche nel canale forze).
  **FASE 4 IMPLEMENTATA** (branch `dev-spinoriale`, 2026-09-10): chiuso il LOOP dell'EVOLUZIONE dello
  spinore (`_passo_spinoriale`), dietro `--campo-spinoriale`, per ARRICCHIMENTO (deciso da Luca: mantenere
  i generatori chirali, non sostituirli). **MOD 4.1** inerzia = `_rho_sorgente()` (rho_spin ON / |psi|² OFF)
  invece di |self.psi|². **MOD 4.2** `correzione = cross(B,nb) + cross(nb_campo, nb)` con nb_campo = `_nb_grav()`
  (Bloch del campo EMESSO); identità `cross(nb_campo,nb)=cross(nb_campo−nb,nb)` → **0 nel limite** (nb_campo=nb=polo),
  **zero parametri** (peso 1.0). Mantiene B (chirale) e AGGIUNGE il canale spinoriale. Rimossa una garanzia di
  freschezza invasiva (ricalcolava self.psi → scollegava rho_spin): `_rho_sorgente`/`_nb_grav` hanno già il
  fallback, e REPULS_LEGGE chiama calcola_psi nel passo. Sigilli TUTTI PASS (`csv/_seal_fase4/_sigillo_fase4.py`):
  **S3 GATE riduzione-al-limite 0.000e+00 ESATTO** (deterministico, senza rumore); OFF byte-identico (vs backup
  pre-Fase4: dphi=0,dpos=0,dψ=0); controprova non-abeliana per-nodo 1.992>0; **STABILITÀ** 400p ON+rumore (N
  1196→2757, n_naninf=0, no blow-up). **REPERTO chiave** (`csv/_seal_fase4/_diag_gate.py`): il gate falliva a
  2e-3 SOLO col rumore del vuoto (SCUOTIMENTO) attivo — il nuovo termine `cross(nb_campo,nb)` REAGISCE al Bloch
  perturbato (riallineamento fisico corretto), quindi S3 va testato sul limite DETERMINISTICO (senza rumore);
  la parte deterministica si riduce ESATTA. Backup `soliton_simulator.backup_2026-09-10_fase4.py`. Primo sguardo
  400p (NON verdetto): segno_arco 0.000, overlap 0.5001 — formazione, serve la campagna covariante lunga.
  **NON è il VERDETTO Fase 4**: serve ON vs OFF N-appaiato 2-3 seed su run lunghi (ora il LOOP È CHIUSO: inerzia
  + evoluzione spinoriali). **NB REGRESSIONE stanata**: soliton_simulator.py era stato sovrascritto con un backup
  pre-Fase1 (perse 206 righe committate); ripristinato da HEAD (`git restore`), sigillo Fase 3 riverificato OK.
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

## 6. MOD 5.3a + 5.3b — il tempo proprio DEPURATO (verso dal segno, magnitudine dalla torsione)

**Contesto.** Fase 5 aggancia il campo spinoriale alla dinamica ma il tempo proprio (`ritmo()`)
usava la magnitudine **de Broglie del campo emesso**. Serie di test-GRATIS (`csv/_seal_53rel/`):

- **S3b NEGATIVO**: l'orologio de Broglie (`|Δα|/DT ~162`, veloce) è **scorrelato** dalla
  dilatazione torsionale `1+|tw|/PHI_CRIT ~1.55` (corr +0.008, scala ~100×). Il de Broglie
  **non** è la dilatazione → magnitudine e verso sono ruoli DIVERSI.
- **PHI_CRIT=4π globale**: soffoca la mitosi (N ×1.00 vs ×2.35) — il 4π doppia-copertura è
  già presente come `2·PHI_CRIT` dove serve. **MOD 5.3c saltata.**

**Teorema segno-da-fase-istantanea impossibile.** Il segno di doppia-copertura deve essere
(i) +1 nel limite, (ii) stabile, (iii) sensibile all'antimateria. Con un riferimento di fase
SINGOLA le tre sono **mutuamente esclusive** (misurato su 3 varianti): **A** letterale
`sign(Re⟨canon|ψ⟩)` vede l'antimateria (60/60) ma oscilla (49.9% flip); **B′** rif. fase propria
è stabile (0%) ma **CIECO** all'antimateria (0/60, invariante sotto ψ→−ψ perché il flip di
antimateria È una fase globale π); **B″** rif. campo emesso vede l'antimateria (60/60) ma oscilla
(49.4%). De Broglie (continuo) e antimateria (π discreto) vivono ENTRAMBI nella fase globale.

**Osservazione di Luca (decisiva).** Il verso del tempo (Feynman-Stückelberg) è proprietà delle
**PARTICELLE** (materia/antimateria = addensamenti COERENTI), NON dello **spaziotempo vuoto**.
Il vuoto non ha un verso da invertire: è la SCENA, non gli attori. → il segno va **modulato dalla
materialità**: `s_k = 1 + (perc_chi − 1)·m_k`, materia coerente inverte col segno, vuoto → +1 avanti.

**Materialità dalla COERENZA** (non peq/massa_critica, misurate INERTI: `peq~1e-8` vs
`massa_critica~621` incommensurabili → `m_k≈0` ovunque → segno inerte). `m_k = clip(cos(φ − arg(Ψ)),0,1)`
= coerenza col campo locale (Legge II: materia = interferenza costruttiva). **Lenta** (|Δm|/passo
0.0017, NON contaminata dal de Broglie — la radice di tutti i fallimenti), stabile (flip 0.2%),
locale, zero-param, vuoto-neutro (s_k 0.943), materia segue perc_chi (100%).

**MOD 5.3a (verso)** `s_k=1+(perc_chi−1)·m_coer` firma SOLO l'evoluzione interna
(`dt_n_s = s_k·dt_n` su delta_phivel, delta_sync_phi, `_passo_spinoriale`, self.phi termine
`dt_n·phivel`); eta/termostato usano `|dt_n|`; `dt_e` (geometria) intatto. **MOD 5.3b (magnitudine)**
`ritmo() = 1+|tw_nodo|/PHI_CRIT` (torsione esplicita, sostituisce il de Broglie bocciato).
Da stato committato t-1 (causale). Flag `--tempo-segno`, richiede `--campo-spinoriale`+`--spinore-corretto`.

**SIGILLI (S3a byte-identico SOSTITUITO da conservazione+stabilità, perché Feynman-Stückelberg è
un cambio fisico deliberato) — TUTTI PASS** (`csv/_seal_53a/_sigillo_53a.py`, evidenza `_out_sigillo_53a.txt`):
1. **OFF byte-identico** (flag-off vs HEAD Fase5): `max|Δ|=0.00e+00` su phi/psi/tw/pos.
2. **RIDUZIONE-VUOTO**: `max|s_k−1|=0` esatto sul vuoto (m<0.1) → il vuoto non inverte.
3. **CONSERVAZIONE (gate)**: Σperc_chi ON=−45/2447 (bilanciato = coppie somma-zero); olonomia netta
   ON=−10420 vs OFF=−15263, drift ON=−480 vs OFF=−2853 → ON **non diverge** (drift minore di OFF).
4. **STABILITÀ (gate)**: 300p ON, N 1196→2447, `n_naninf=0`, `min(eta)=0` (≥0). No blow-up.
5. **CAUSALITÀ** (strutturale): s_k da stato t-1 prima di ogni commit; ordine ETC invariato.
6. **COMPLETEZZA** (strutturale): firmato solo #3-6; magnitudine su eta+termostato; geometria intatta.
7. **CONTROPROVA non-abeliana**: ON≠OFF (`max|dphi|=12.4`) → il flag cambia la dinamica.

**PER CLAUDE (doppio-check senza rilanciare):** evidenze in `csv/_seal_53a/_out_sigillo_53a.txt`
e `csv/_seal_53rel/_out_*.txt`; rigenera con `python csv/_seal_53a/_sigillo_53a.py`. Punti da
ricontrollare: (a) `dt_n_s` firmato SOLO su #3-6 (grep `dt_n_s` in step); (b) `m_coer` da `self.psi`
committato a inizio step (t-1, no mutazione); (c) il teorema segno-da-fase (3 varianti mutuamente
esclusive) — verificare `_verifica_cecita_antimateria.py` (B′ invariante sotto ψ→−ψ).

**PROSSIMO: test covariante** `--tempo-segno` ON vs OFF, N-appaiato, 2-3 semi, run lunghi. DOMANDA:
con la materia/antimateria coerente che controlla il verso del tempo (antimateria indietro), l'ordine
del segno diventa ATTRATTORE (`segno_arco_coer` sale e RESTA, vs §48 dove decadeva) o resta 0.5?


---

## AGGIORNAMENTO 2026-09-10 (sera) — contaminazione CALORE VETTORIALE + FONDAZIONE 3+1

**Reperto (Luca):** il calore vettoriale-chirale (surrogato di spin PRE-spinore) contaminava il segno:
`SCUOTIMENTO=True` default -> `scuoti_vuoto` iniettava ogni passo un calcio firmato da `perc_chi` in
`phivel` (riga 539); `--calore-scal` NON lo toglieva (gate solo il calcio iniziale). FIX (dev `3fb5143`):
`scuoti_vuoto` rispetta `CALORE_VETTORIALE` -> con `--calore-scal` il calcio e' SCALARE/isotropo.
OFF byte-identico (CV=True: max|dphi|=max|dpsi|=max|dphivel|=0). Principio: VUOTO ISOTROPO (simmetrico)
+ VERSO solo nella materia/antimateria (rottura spontanea di simmetria: l'asimmetria vive nello stato).
Il pilota §54 (NO-GO) era su dati contaminati -> RIFATTO pulito (`csv/_test_53a/{off,on}_scal_s1.csv`).

**Accenno (NON scoperta, 1 seme -> dentro il rumore):** `Sigma perc_chi` OFF +87 vs ON -45 (con
`--tempo-segno` vira all'antimateria); `Sigma tw` netto negativo. Da confermare 2-3 semi/2000 passi.

**FONDAZIONE 3+1** (`doc/FONDAZIONE_3+1.md`): proposta di Luca — il tempo proprio come QUARTA dimensione
firmata dal segno (R^3 -> R^{3,1}), Feynman-Stuckelberg geometrico, split materia/antimateria EMERGENTE
via `dt_e = 0.5(s_i|r_i|+s_j|r_j|)~0` fra opposti (non imposto). RAFFINATO con due presidi guardiano:
(1) AGGANCIO SELETTIVO (dt_e firmato per il segno/dinamica, |dt_e| magnitudine per la GEOMETRIA -> la
gravita' materia-antimateria NON si congela); (2) LOCALITA' TEMPORALE TOPOLOGICA (|T_i-T_j|>soglia ->
nessun arco -> costo O(N), non solo arco inerte). Sigilli aggiornati (3=localita' topologica GATE COSTO,
7=gravita' intatta). NON ancora implementato: e' la fondazione teorica del prossimo capitolo.

**PROSSIMO:** valutare il pilota pulito (incluso materia/antimateria); poi braccio `--cs-dinamico`
(metrica completamente locale: c_s locale <-> dilatazione = stessa metrica); poi eventualmente 3+1.
