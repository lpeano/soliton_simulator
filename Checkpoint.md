# CHECKPOINT — Sistema dei Solitoni Relazionali (VQT / U2)

_Ultimo aggiornamento: 2026-09-10. Progetto di Luca Peano ("Il Muratore di Planck")._
_Traccia stato, fatto, da-fare. Da aggiornare a ogni sessione. Vedi CLAUDE.md per le norme di conduzione._

---

## PUNTO DI INTERRUZIONE — 2026-09-09 (ripresa rapida)

**Filone `dev-dof` — ordinamento del SEGNO di doppia-copertura (spin 1/2?).** Cronologia delle vie tentate
(dettaglio in CLAUDECONNECT §40–46-bis e `/memories/repo/deparam_orologio.md`):
- **§41 `--spin-feedback`** (filo indiretto) → **NO-GO** (segno_arco_coer ~0, ON=OFF).
- **§42 `--chi-da-spinore`** (filo diretto) → **NO-GO** (secondo filo fallito).
- **§43 motore-unico** → **DIMOSTRATO artefatto di reticolo** (BCH O(dt²), unito==split nel continuo).
- **§44 `--sync-fase-orologio`** (Kuramoto abeliano sul segno, O(dt¹) genuino) implementato + sigilli → **§45 NO-GO**.
- **§45-bis antiferromagnetico** → smentito. → **Tre vie abeliane fallite: ipotesi ABELIANA forte.**
- **§46 `--kuramoto-su2`** (via NON-ABELIANA, l'ULTIMA carta): rotazione SU(2) piena dello spinore verso la
  media dei vicini, asse variabile `nb×nb_bar`; il verso si allinea, il SEGNO segue per **OLONOMIA** (non
  targettizzato). Se ordina → spin 1/2; se no → **teorema di assenza / abeliano definitivo**.

**FATTO oggi (§46-bis):** sigilli `--kuramoto-su2` → **SIGILLO 1** (OFF byte-identico OLD=`ff2982e` vs NEW-off)
**PASSATO** (max|A-B|=0 su 28 array); **SIGILLO 2** (unitarietà) **PASSATO** (|psi|=1, len==n); sigillo 3
(primo ordine) analitico O(dt¹); sigillo 4 (conv-dt) nella campagna. Prelim a 300 passi (formazione, non
verdetto): `spin_overlap_arco`~0.5 ON=OFF, nessun accenno. Evidenza su `dev-dof` (`6a3864a`).

**IN CORSO / GATE:** pilota go/no-go 800 passi seed 1 ON vs OFF (`csv/deparam_pilota_k2/`) = **NO-GO** (§46-ter).
A N appaiato (N 824→2231 ×2.71): `spin_overlap_arco` (SU(2) pieno) **0.500 ON=OFF** = scorrelato; `segno_arco_coer`/
`verso_arco_coer` ~0, ON=OFF; unico stacco `segno_ov_absmedia` ON<OFF −0.041 (direzione sbagliata, disordina);
`corr(segno,verso)`≈0 (non un motore unico). **L'olonomia non trasferisce coerenza al segno.** 4 vie tutte piatte
(§41/§42/§44 + §46 non-abeliano) → **ipotesi ABELIANA molto forte**. Cautele: 800p=formazione, 1 seme = NON
verdetto. **Prossimo (gate a Luca):** (A) conferma **3 semi/2000 + conv-dt covariante** → se ~0 concorde = **ABELIANO
DEFINITIVO** (chiusura formale); (B) diagnosi del perché nemmeno il non-abeliano ordina. MAI forzare verso=segno.

## CHIUSURA CAPITOLO ATTUALE + NUOVO BRANCH (2026-09-09)

**[branch `dev-dof`] §47 — Tre freni + bracci A/V/B/C: tutti NO-GO.** L'intuizione "il test ha gli agganci?" ha
stanato un freno TRIPLO: flag spenti; `CHI_BASC` rotto (soglia `median(twn)` globale invece di 2π → imponeva il
50/50 che doveva rompere — viola "la media non va qui"); `OLON_PART` inerte senza `--viriale`. Fix di legge
(median→PHI_CRIT, sigillo OFF byte-identico). Bracci A(chi-basc)/V(viriale)/B(viriale+olon)/C(tutto): **tutti
NO-GO** (`spin_overlap_arco`~0.500, `berry` firmata ~0 ovunque). `CHI_BASC` soffoca la crescita (il "372" costante
= congelamento), ma il test decisivo mostra che **il congelamento NON maschera** (il congelato C ha spin_overlap
identico ai non-congelati V/B — gli osservabili del segno sono relazionali sugli archi, a N fisso).

**[branch `dev-dof`] §48 — Tracing per-passo: il segno è un REPULSORE (reperto chiave, confermato 2 semi).** Il
segno **nasce ordinato** (`segno_arco`=0.996, semina) e **decade a 0.000 in ~10 passi**, **pre-nascite** (coppie
escluse), col **torque che collassa** (0.93→0.15). Confermato su **2 semi**. Lo stato ordinato è un **repulsore**;
l'attrattore è lo scorrelato — il sistema **relassa attivamente via dall'ordine** (feedback auto-distruttivo). →
**Teorema di assenza CON MECCANISMO**: il core è abeliano *perché* l'ordine del segno è un repulsore dinamico, non
per caso/misura. Flag `--trace-segno` (pure-read, sigillo OFF byte-identico). **Verdetto capitolo `dev-dof`:
ABELIANO, con ragione fisica.**

**[branch `dev-spinoriale`] §49 — Refactoring rifondativo (nuovo branch parallelo).** Lo spinore diventa
FONDAMENTALE, il campo Ψ è ciò che emette (inversione campo→spinore ⇒ spinore→campo; fondamentale SU(2)
non-abeliano incorporato). **Collegamento col §48**: nell'attuale l'ordine è un repulsore (segno = grado aggiunto,
niente lo stabilizza); nel spinoriale la **materia** richiede accordo di segno (interferenza non distruttiva) →
l'ordine diventerebbe un **attrattore** *per fisica*, non per trucco. Il fallimento dell'attuale è la mappa per il
nuovo. Doc sotto `doc/`: `FONDAZIONE_SPINORIALE.md`, `REFACTORING_SPINORIALE.md`, `ONTOLOGIA_SPINORIALE.md`. Solo
fondazione, niente codice. **REGOLA: d'ora in poi ogni relazione/commit dichiara il BRANCH.**

**[branch `dev-spinoriale`] §50 — Fasi 1-4 implementate + VERDETTO FASE 3 NEGATIVO + non-abelianità totale (2026-09-10).**
Quattro fasi dietro `--campo-spinoriale` (OFF byte-identico), ognuna col sigillo di riduzione-al-limite S3 (spinori
in fase → il vecchio, **esatto 0.000e+00**). **Fase 1**: campo Ψ EMESSO dallo spinore (`psi_spin`/`rho_spin`).
**Fase 2**: densità (ρ=ψ†ψ) e gravità (nb nativo) dal campo (`_rho_sorgente`, `_nb_grav`). **Fase 3**: forze =
OVERLAP `⟨ψ_i|ψ_j⟩` (`_coppia_interferenza`). **VERDETTO FASE 3 = NEGATIVO** (covariante ON vs OFF, 3 semi,
N-appaiato, ~3000-4470 passi): ON≈OFF su tutto (segno_arco ON−OFF=+0.0001, overlap 0.500=0.500, berry_firmata ~0)
→ **§48 NON ribaltato**, core ancora ABELIANO. **Reperto**: l'evoluzione (`omega_new`) usava inerzia `|ψ|²`
SCALARE → **LOOP APERTO** (sistema misto). Il verdetto Fase 3 è su loop aperto, non sulla visione completa.
**Principio di non-abelianità totale** (doc/): ovunque φ o nb → ψ o overlap, col presidio riduzione-al-limite.
**Fase 4** (ARRICCHIMENTO, scelta di Luca: mantenere i generatori chirali di B): inerzia = ρ_spin;
`correzione = cross(B,nb) + cross(nb_campo,nb)` (→ 0 nel limite, zero parametri). **Sigilli tutti PASS**: S3 gate
0.000e+00 esatto, OFF byte-identico, controprova non-abeliana per-nodo 1.992, stabilità (N 1196→2757, no nan/inf).
Il **loop è ora CHIUSO**. **NON è il verdetto Fase 4**: serve la campagna covariante lunga a loop chiuso (ON vs OFF,
N-appaiato, 2-3 semi). Commit su `dev-spinoriale`: Fase 3 `677fc80`, verdetto `a903491`, doc `a623f27`, Fase 4 `7fc637e`.
Prossimo: **campagna covariante lunga a loop chiuso** (2-3 run paralleli, evitare OOM; occhio a Windows Update notturno)
→ se il segno si ordina e RESTA = attrattore (ribaltamento); se ~0 = abeliano definitivo anche a loop chiuso. Poi Fase 5
(coppie/mitosi/tempo-proprio Reeb).

**[branch `dev-spinoriale`] §51 — FASE 5 committata + DESIGN MOD 5.3 rivista (segno nel tempo proprio) (2026-09-10).**
**FASE 5 committata** (`4ea6f0c`, backup `soliton_simulator.backup_2026-09-10_fase5.py`). Sotto `--campo-spinoriale`
(OFF byte-identico): `ritmo()` dal campo `psi_spin[:,0]` sull'OTTO (wrapping **4π**); soglia mitosi/coppie da
`_rho_sorgente`; eredità spinore ai figli attiva. Sigillo FASE 5 PASS (`csv/_seal_fase5/_sigillo_fase5.py`):
S3 riduzione-al-limite DETERMINISTICA **0.000e+00** esatto; controprova non-abeliana per-nodo ON≠OFF (1.98).
**DESIGN MOD 5.3 (rivista) proposto — IN ATTESA CONFERMA LUCA, nessun codice.** Feynman-Stückelberg: il SEGNO di
doppia-copertura entra nel tempo proprio e ne inverte il VERSO (materia→avanti, antimateria→indietro). Il 4π in
`ritmo()` è già la MAGNITUDINE del de Broglie/Reeb (segno non entra); il segno è `s_k=sign(Re⟨canon(nb)|_psi_spinor⟩)`.
Proposta (flag nuovo default OFF, richiede `--campo-spinoriale`+`--spinore-corretto`, zero parametri):
`r_signed_k = s_k · ritmo()_k`. Riduzione-al-limite ESATTA (tutta materia → s_k=+1 → identità); causalità OK
(`ritmo()` legge `_nb`/`_psi_spinor` a t-1; inversione LOCALE al `dt_n`, ordine ETC Jacobi invariato).
**Punto aperto (decide Luca)**: rischio `eta<0`/`dt_e<0` (antimateria che ringiovanisce, archi misti) → (A) inversione
piena del `dt_n` sigillando la stabilità, vs (B) invertire solo l'orologio interno lasciando `|dt_n|`. Sigilli
pre-test: OFF byte-id, S3, causalità, stabilità (eta/dt_e<0), conservazione (olonomia, coppie somma-zero),
controprova non-abeliana. Test: `segno_arco_coer` sale e RESTA (attrattore) vs §48 dove decadeva?
NOTA: `soliton_simulator.regressione_2026-09-10.py.bak` = scratch (−205 righe vs HEAD), lasciato untracked su dev.

---

## MODELLO BRANCH E TRACING — 2026-09-07 (canonico)

- **`main` = versione STABILE del codice + UNICO punto di documentazione e tracing per TUTTI i branch.**
  Tutta la parte documentale (`Checkpoint.md`, `CLAUDECONNECT.md`, `CLAUDE.md`, `FISICA.md`, i report e le
  interpretazioni, `/memories/repo/`) si aggiorna e vive **solo su `main`**. Per leggere lo stato del lavoro,
  qualunque sia il branch di sviluppo, si guarda `main`.
- **`dev-<nome-sviluppo>` = linee di sviluppo PARALLELE** (solo CODICE, non la doc). Niente più un unico `dev`
  (strozzava i paralleli). Branch attivi:
  - **`dev-infra`** (commit `aa94b29`) — infrastruttura: nuovo check DB per git-blob + layout output
    `db//csv//log/` per campagna. **Trasversale**: quando stabile va promosso su `main`.
  - **`dev-dof`** (da `dev-infra`) — **soluzione DOF**: Kuramoto sulla FASE-orologio (segno di doppia-copertura)
    `--sync-fase-orologio` + de-parametrizzazione (Ψ per deg, mediana locale). Vedi CLAUDECONNECT §30 (design), §31, §32, §33.
    **STATO (§33, WIP `2e39ea0`)**: implementato `--deparam-orologio` (orologio RELAZIONALE = coerenza d'arco intensiva;
    test-GRATIS: `omega_clk` era ~95% connettività, corr(deg)=0.948). Sigillo OFF byte-identico PASSATO; **sigillo
    gravità FALLITO** (la gravità è spin-modulata by design, riga ~2933 `grav*=_nb·_nb` → N 1990→1821). Decisione
    pendente: (1) valutare per osservabili, (2) rendere l'orologio pura-fase prima, (3) ripensare. Aggancio `--sync-fase-orologio` DOPO.
    **AGGIORNATO (§34, WIP `5c53717`)**: scelta (2) — orologio **PURA-FASE** (fase globale, non nell'asse). Sigilli
    PASSATI: OFF byte-identico; chirurgico `max|nb−nb'|=6.7e-16` (l'orologio non tocca nb→gravità); N 2014 vs legacy
    1990 (+1.2%, = rimozione del tilt-legacy). De-param RELAZIONALE+PURA-FASE completa e sigillata. PROSSIMO: campagna
    2000 passi/3 semi (coerenza del segno ↑? dispersione ↓?), poi ri-testare il sync sul DOF giusto (`--sync-fase-orologio`).
    **STOP (§38, 2026-09-07)**: campagna B **FERMATA** — misurava l'osservabile SBAGLIATO. Verificato nel codice: (1) il
    segno è CONDIZIONALMENTE dinamico — due canali reali segno→fisica (`SPIN_FEEDBACK` = `Im⟨lift_i|lift_j⟩`→coppia;
    `CHI_DA_SPINORE` = `sign(Re⟨canon|ψ⟩)`→perc_chi), ENTRAMBI OFF in B → in B il segno è solo diagnostico ("motore
    acceso, frizione staccata"). (2) `m0_spin_axis_R` = DIREZIONE nb (corregge §36: NON è il segno), cieco all'orologio
    pura-fase (nb invariante 6.7e-16). (3) anche `berry_*` è cieca (ricostruita da nb + Bargmann gauge-invariante). (4)
    NON esiste diagnostica del segno → va aggiunta (`|media sign(Re⟨canon(nb)|ψ⟩)|`). **PIANO B″**: `--chi-da-spinore`
    ON (filo coerente = stessa quantità dell'osservabile), de-param ON vs OFF (un flag = una variabile), misura
    coerenza-segno (ordina?) + N/spin_axis_R (cambia la fisica?). Prima: edit diagnostica pura (test byte-identico). Vedi CLAUDECONNECT §38.
- **Campagne lunghe**: `git worktree add ../st_wt/<commit> <commit>` (versione immutabile a un commit).
- **Versionamento DB (IMPLEMENTATO su `dev-infra`):** identità di accetta/rifiuta = **git blob hash** dei byte di
  `soliton_simulator.py` (`git hash-object`); `commit`/`branch`/`dirty` = metadati (branch diverso → solo warning,
  mai rifiuto; sporco → fallback `sha256` + warning). DB legacy (solo `code_hash` sha256) accettati per contenuto
  identico. **Ripresa di campagne vecchie**: se il DB è rifiutato per codice cambiato, esegui la versione giusta con
  `git worktree add ../st_wt/<commit-del-DB> <commit-del-DB>` (il commit è nei metadati del DB) — NON forzare `--db-cleanup`.
- **Layout output**: `db/<campagna>/*.pkl`, `csv/<campagna>/*.csv`, `log/<campagna>/*.log` (auto-mkdir motore per db/csv;
  gli script fanno `mkdir log\<campagna>` per il redirect). Video (`.mp4`, `out_video/`) fuori schema.

---

## PUNTO DI INTERRUZIONE — 2026-09-07 ~08:20 (ripresa rapida)

### IN CORSO adesso
- **Campagna STEP 2 chi-core** (`test_sync_spinore_step2.bat`, `out_sync_spinore_step2/`): i 3 run **ON completati**
  (on_s1/2/3 a 2000 passi, db+csv OK). Il batch si era BLOCCATO 4h dopo on_s3 (04:16→08:18, prob. sleep macchina)
  senza fare gli OFF. **Rilanciato** (riprendibile: hash db combacia, ON saltati come no-op) → sta facendo i **3 OFF**.
  ATTESA: off_s1/2/3, poi verdetto covariante ON vs OFF su `m0_spin_axis_R`/`m0_omega_axis_R`/`m0_spin_core_cv`.

### >>> INTERRUZIONE PER SPEGNIMENTO PC — 2026-09-07 (COME RIPRENDERE) <<<
- **UNICA campagna interrotta**: STEP 2 chi-core (`test_sync_spinore_step2.bat`). Stato al momento dello stop:
  - ON: on_s1/2/3 **COMPLETI** (2000 passi).
  - OFF: **off_s1 PARZIALE** (~273 passi, db salvato a step ~200); **off_s2/off_s3 NON iniziati**.
  - I DB/CSV sono ora in `db/sync_spinore_step2/` e `csv/sync_spinore_step2/` (migrati dal vecchio `out_sync_spinore_step2/`).
- **ATTENZIONE — il codice è CAMBIATO** (infra su `dev-infra`, commit `aa94b29`): quei DB sono legacy (sha256 del
  codice `5fbd53f`) → sul codice nuovo verrebbero **RIFIUTATI**. Per riprendere ESATTAMENTE la campagna interrotta:
  `git worktree add ../st_wt/5fbd53f 5fbd53f`, copiare/puntare i DB e rilanciare LÌ (blob combacia). In alternativa,
  ri-eseguire la campagna PULITA sul codice nuovo (consigliato se STEP 2 va comunque rifatto col nuovo layout).
- **NB**: `test_sync_spinore_step2.bat` è già aggiornato al nuovo layout (`db\sync_spinore_step2\`, `csv\...`, `log\...`).
- Le altre campagne (tauloc/scuotimento) erano gia' FERMATE (instabilita'), NON vanno riprese cosi'.

### DA FARE (coda, priorità dall'alto)
1. **Completare chi-core** (3 OFF) e dare il verdetto covariante: `--chi-core` da' il CANALE alla sync o no?
2. **FIX `--sync-fase-orologio`** (design pronto, CLAUDECONNECT §30): Kuramoto sulla FASE-orologio (segno di
   doppia-copertura) invece che sulla direzione di Bloch. È l'ipotesi che i dati indicano come causa del negativo.
   Implementare DOPO la campagna (non editare il .py mentre gira: contamina/rompe la ripresa). Poi A/B, 3 semi.
3. **STEP 2 candidate rimanenti** (una alla volta): `--guscio-morbido`. NB: `--cs-dinamico + --tauloc>1` è
   INSTABILE (CFL/nsub esplode) → evitare o usare tauloc gentile senza cs-dinamico.
4. **Programma DE-PARAMETRIZZAZIONE = limite continuo** (TODO dedicato sotto): GAMMA per primo (Classe 3,
   centrale), poi gF_med locale (Classe 4), normalizzare estensive (Classe 2). Attacca la radice della
   dispersione degli orologi.
5. **tauloc + scuotimento**: flag `--scuotimento` pronto e verificato, ma la variante con tauloc 2.0 era
   impraticabile (instabilità). Da rifare con tauloc gentile o senza cs-dinamico, se serve.
6. **Test RG / invarianza coarse-graining** (B vs 2B) — la prova del limite continuo.

### MIE VALUTAZIONI (guardiano, IN VERIFICA)
- **Il nuovo spinore NON è un fallimento**: la macchina è corretta (sigilli passati), ma ho messo il Kuramoto
  sul grado di liberta' SBAGLIATO — la frustrazione vive nel SEGNO/fase di doppia-copertura, non nella direzione
  di Bloch (firma: `omgR~0.2` > `spinR~0.1`). Il fix `--sync-fase-orologio` è il test diretto di questa ipotesi.
- **De-parametrizzare = limite continuo** (intuizione di Luca, verificata sullo SCALING): eliminare un parametro
  (scala assoluta) = rapporto di stato adimensionale = invariante di scala = converge a N→∞. Il criterio giusto
  NON è h→0 (2ℓ_P fondamentale) ma il coarse-graining/RG. Vedi REPORT_LIMITE_CONTINUO.md §14.
- **Le due cose si toccano**: la dispersione degli orologi che frustra la sync è in parte ARTEFATTO di Ψ-non-
  normalizzata (∝deg) + gF_med globale. Quindi il fix profondo potrebbe essere de-parametrizzare (GAMMA/gF_med),
  NON solo cambiare l'accoppiamento. Due strade: (A) sync-fase-orologio (rapido, test dell'ipotesi DOF);
  (B) de-parametrizzare (radice, ma piu' lungo). Consiglio: (A) prima come diagnosi, poi (B) come cura strutturale.
- **Riprendibilita' salva-lavoro**: senza il resume avremmo perso i 3 ON (ore). Da tenere per ogni campagna lunga.

---

## STATO RUN CORRENTE — 2026-09-07 (cosa gira / cosa attendiamo)

### IN RUN adesso (in attesa di completamento)
- **STEP 2 — candidata `--chi-core`** (`test_sync_spinore_step2.bat`, cartella `out_sync_spinore_step2/`).
  A/B `--sync-spinore` ON vs OFF a parita' di `--chi-core`, 3 semi, 2000 passi, minimo freddo, tutti con `--sync`.
  Stato: `on_s1` ~1137/2000 (primo dei 6 run: on_s1/2/3 poi off_s1/2/3). **ATTESA: verdetto covariante**
  (N appaiato) su `m0_spin_axis_R` / `m0_omega_axis_R` / `m0_spin_core_cv`, ON vs OFF — la candidata
  `--chi-core` da' il CANALE che fa propagare la sync o e' inerte/contrasta (come al minimo freddo, negativo)?

### FERMATI (NON in run) — instabilita' numerica, non forzare
- **Run `--chi-core --cs-dinamico --tauloc 2.0`** (`test_sync_spinore_step2cs.bat`) e la sua variante
  **`+ --scuotimento`** (`test_sync_spinore_step2cssc.bat`): IMPIANTATI al primo passo. MISURATO:
  `tauloc>1` con `cs-dinamico` fa ESPLODERE il sotto-ciclo metrico CFL (`nsub`) -> 10-100x piu' lento;
  `tauloc 2.0` = 1500 CPU-s con 0 righe (impraticabile), `tauloc 1.5` = 756 CPU-s per ~10 righe (rigidissimo).
  Cartelle svuotate. DA DECIDERE con Luca: tauloc gentile (1.1-1.2, comunque lento), oppure tauloc SENZA
  cs-dinamico, oppure abbandonare tauloc. Conferma la nota storica: "--tauloc grande impianta il 1o passo".

### DIAGNOSI del negativo sync-spinore + FIX proposto (design, 2026-09-07)
- **NON un fallimento della macchina** (corretta, sigilli passati) ma NEGATIVO diagnosticato. Causa principale
  (i dati la indicano): il Kuramoto `--sync-spinore` agisce sulla DIREZIONE di Bloch (`nb x nb_media`, torque
  trasverso), ma la frustrazione vive nella FASE lungo l'asse = SEGNO di doppia-copertura. DOF disaccoppiati:
  `omgR~0.2` (direzioni allineate) > `spinR~0.1` (segno frustrato). Vedi CLAUDECONNECT §30.
- **FIX proposto (design, NON implementato): `--sync-fase-orologio`** — Kuramoto sulla FASE dell'orologio:
  `theta_i=arg<canon(nb_i)|psi_i>`, `omega_sync_clk=forza*(wI @ sin(theta))/uno` sommato a `omega_clk` (lungo
  nb, non trasverso). Zero parametri nuovi (riusa `forza`). Aggancio col limite continuo: la dispersione degli
  orologi e' in parte artefatto di Ψ-non-normalizzata + gF_med globale -> de-parametrizzare aiuterebbe.
- **VINCOLO**: NON editare il .py mentre gira la campagna chi-core (contamina on_s2+ e rompe la ripresa).
  Implementare DOPO la campagna o fermarla. ATTESA conferma design + timing da Luca.

### Novita' di codice (2026-09-07)
- **`--scuotimento`** (nuovo flag, default off = byte-identico): forza `SCUOTIMENTO=True` anche in regime
  DETERMINISTICO (il vuoto ribolle ma la dinamica resta deterministica). Applicato dopo `--regime`.
  VERIFICATO: EXIT=0, stampa corretta, 21 righe, no crash.
- **Campagne RIPRENDIBILI**: rimosso il `del /q` distruttivo dagli script `test_sync_spinore*.bat`. Il sim
  riprende dal `--sync-db` (`salva_stato` salva TUTTO `__dict__` incl. cache spinoriali + stato RNG;
  `carica_stato` fa i passi rimanenti e appende il diaglog senza duplicati). ATTENZIONE: `carica_stato`
  VERIFICA l'HASH del codice -> **NON editare `soliton_simulator.py`** mentre i run girano, o i db vengono
  rifiutati (usare `--db-cleanup` per ripartire puliti). Hash ora CONGELATO per non rompere `chi-core`.

---

## TODO — LIMITE CONTINUO = DE-PARAMETRIZZAZIONE (pian piano, dal 2026-09-07)

**Scoperta (INTUIZIONE di Luca, criterio analitico):** il limite continuo di QUESTO sistema NON è `h→0`
(la granularità 2ℓ_P è FONDAMENTALE, Planck, non un artefatto) ma il **COARSE-GRAINING a grande scala**
(gruppo di rinormalizzazione: osservabili macroscopiche invarianti sotto raggruppamento B→2B). E
**"non parametri, ma leggi" ≡ criterio del limite continuo**: de-parametrizzare (sostituire una scala
assoluta con un rapporto di stato) = rendere adimensionale/invariante di scala = far convergere a N→∞.
Dettaglio e classificazione analitica in `REPORT_LIMITE_CONTINUO.md` §14. Etichetta: CRITERIO (mappa),
non risultato dimostrato — l'analitica dà lo SCALING, non il valore né l'indipendenza dal modo di crescere N.

Lista operativa (una alla volta, flag reversibile default-off, byte-identico off, A/B, 2000 passi + 3 semi):
- [ ] **GAMMA** (Classe 3, il più centrale — in Ψ, cs_floor, dens_crit): de-parametrizzare con un rapporto
      di stato adimensionale. Priorità 1: farebbe convergere tre osservabili insieme. Da decidere CON QUALE rapporto.
- [ ] **`gF_med`** (Classe 4, non-locale in `N_c`): localizzare con media di vicinato `wI` (come per il sync),
      in un ramo sperimentale; misurare l'impatto.
- [ ] **Estensive** (Classe 2): normalizzare nel DIAGLOG (non nella dinamica) — `Lz/I`, `N/V`, energia/N.
- [ ] **Test RG / invarianza coarse-graining**: stesso sistema a B vs 2B solitoni → osservabili macro coincidono?
- [ ] **Ψ / deg** (normalizzazione mancante, non parametro): ramo A/B esplorativo (rompe byte-identità).
- [ ] **Misura conservata dalla mitosi** (il punto duro, non chiudibile solo analiticamente): analitico + numerico.
- Altri parametri Classe 3 (DENS_CRIT_C, ELAST_C, K_C, KICK_TW, MU_PSI, TAU_*): dopo GAMMA.
- NON toccare le UNITÀ (LAM=2ℓ_P, DT, Φ_crit=2π): sono scale, non manopole.

---

## AGGIORNAMENTO — 2026-09-06

### Pacchetto SPINORE CORRETTO + Kuramoto SU(2) (tutto default-off, sigilli passati)

- **[FATTO, sigilli byte-identici]** Catena di gate rigorosi (analisi → stop → conferma → implementa).
      Vedi `CLAUDECONNECT.md` §28 per il dettaglio. Flag aggiunti (default off):
  - **`--spinore-corretto`** (master): orologio proprio de Broglie + spinore primario complesso
      `_psi_spinor` (n×2, SU(2)); Bloch `_nb` DERIVATO (nb=psi†σψ). Evaluate-then-commit, |psi|=1.
      Collisione di nome risolta: `self.psi`=materia U(1), `_psi_spinor`=spinore. Richiede `--spinore-vivo`.
  - **`--chi-da-spinore`** (flag 3): perc_chi da segno di doppia-copertura, post-commit; disattiva CHI_BASC.
  - **`--tempo-proprio-orientato`** (flag 4): r con segno (toglie |.| da f in ritmo()).
  - **`--sync-spinore`**: Kuramoto SU(2). omega_sync=forza·(nb×nb_media) da snapshot t-1, forza dal
      Kuramoto-φ. Torque ISTANTANEO in omega_tot (rotazione), MAI in omega_s (memoria). Zero parametri.
  - Cache coerenti dopo mitosi/Schwinger (`_eredita_spinore_figli`, regola D); eliminato reset spurio di
      `_psi_prec`. Diaglog sola-lettura esteso a `_psi_spinor,_nb,omega_s,phi_s`.
- **[SIGILLI]** OFF byte-identico (max|A−B|=0); ON |psi|²=1.000000 e `_psi_spinor/_nb/omega_s` len==n dopo mitosi.
- **[IN CORSO]** Campagna STEP 1 "minimo freddo" (`test_sync_spinore.bat`): solo prerequisiti, regime freddo,
      A/B ON vs OFF, 3 semi, 2000 passi. Misura COVARIANTE (N appaiato). DA LEGGERE a fine run.
- **[FATTO]** Diaglog reso COVARIANTE (intensivo/adimensionale, per-dominio; byte-identico): `spin_axis_R`
      (|media versori Bloch| globale [0,1], non diluisce), `m0_spin_axis_R` (allineamento spinori nucleo =
      parametro d'ordine Kuramoto SU(2)), `m0_omega_axis_R` (allineamento assi orologi), `m0_spin_core_cv`
      (spin_core_disp normalizzata per scala freq comovente). NB: tutti i run hanno SEMPRE `--sync`.
- **[NEGATIVO covariante, 3 semi]** STEP 1 minimo freddo completato. ON vs OFF a N APPAIATO (N=2000-3000;
      catena fredda cresce piano, N max ~3-4k). `m0_spin_axis_R` ~0.04 (FRUSTRATO) in ON e OFF, ON<OFF su
      tutti e 3 i semi -> `--sync-spinore` NON scioglie la frustrazione al minimo freddo. Solo accenno debole
      non robusto su `m0_omega_axis_R` (assi orologi, 2/3 semi). Coerente con la SOGLIA di Kuramoto
      (accoppiamento < dispersione orologi). Macchina corretta ma NON sufficiente. Analisi: out_freetest/_analisi_sync.py.
- **[PROSSIMO]** STEP 2: candidate una alla volta (--chi-core; poi --cs-dinamico; poi --guscio-morbido), A/B 3 semi.
- **[APERTO]** La macchina corretta è necessaria NON sufficiente per lo spin ½: l'ordinamento (frustrazione
      chiralità) è il problema separato che `--sync-spinore` prova a sciogliere.

---

## AGGIORNAMENTO — 2026-09-05

### Congelamento da guscio: RISULTATO 2 semi (diaglog pulito, byte-identico)

- **[IN VERIFICA, 2 semi]** Campagna `spin_core`/inerzia guscio (sep 8, 2000 passi). L'ipotesi
      "il guscio congela la precessione per INERZIA" **NON è confermata**: `corr(Jshell_frac,|Lz|)`
      e `corr(Rinerzia,|Lz|)` ~0 (cambiano segno tra semi). Il calo di `|Lz|`/`spin_core` in blocco
      è confuso con l'AGING (cresce tutto, ~18-21k nodi). **Segnale REALE e concorde:** il guscio
      **DISORDINA lo spin del nucleo** — `corr(Jshell_frac, spin_core_disp)` = +0.47/+0.40 su 2 semi;
      `corr(Nshell, spin_core)` negativo. Frustrazione/disordine, NON congelamento inerziale.
      Contro-prova in corso: A/B `--guscio-morbido` (se smussa il guscio → cala `spin_core_disp`).
      Dettaglio in `CLAUDECONNECT.md` §24.

### Diaglog reso SOLO-LETTURA (cura alla radice, byte-identico verificato)

- **[FATTO, DIMOSTRATO]** `chiralita_core_locale()` è IMPURA (muta `self._chi_core_nodi`,
      letto dalla fisica a ~1967). Il diaglog che la richiamava contaminava la dinamica.
      Cura: nel diaglog **lettura pura** del cache + **snapshot/restore** dei cache di
      continuità fisica che le funzioni diagnostiche mutano (`psi`, `_psi_prec` da `ritmo()`,
      `_spinor_lift`). Verificato: stato fisico finale **byte-identico** con/senza diaglog
      (`max|A−B|=0` su phi/d/tw/pos/…). Rimosso il flag `--diag-lente-ogni` (superfluo).
      Regola: **il diaglog è SOLO LETTURA, mai mutare stato fisico.**

### cs-dinamico: c locale nell'intero settore metrico (committato+pushato)

- **[IMPLEMENTATO]** Con `--cs-dinamico` la velocità metrica locale `cs_arco`
      è ora usata nell'INTERO settore metrico: sorgente in unità naturali
      (`cs_arco^2/d`), tempo plastico delle `d0` (`tau_p = d/cs_arco`) e target
      del termostato (`cs^2*P_eq`, con `cs` = mediana del campo locale). Prima
      questi tre usavano `CS_M` globale. Helper `_cs_nodo()` = unica fonte della
      legge `cs(rho)`. Ramo `CS_DINAMICO=False` invariato. Backup:
      `soliton_simulator.backup_2026-09-05_cs-locale.py`.
- **[DIMOSTRATO, formula]** La modifica APPROFONDISCE il congelamento del nucleo:
      `cs` bassa nel denso → `tau_p` più lungo del vecchio `CS_M` uniforme.

### spin_core (TODO PRIORITARIO 1) + diagnostica inerzia guscio

- **[IMPLEMENTATO]** Aggiunte colonne diaglog `m0_spin_core`/`m0_spin_core_disp`:
      spin di fase sulla maschera del nucleo (quartile interno di raggio), pesato
      `|Psi|^2`, SENZA selezione `perc_chi`.
- **[IMPLEMENTATO]** Diagnostica congelamento da guscio (massa 0, dominio
      nucleo+guscio): `m0_Mdyn`, `m0_Mcoh`, `m0_Rinerzia=Mdyn/|Mcoh|`,
      `m0_Jrot=Σ|Psi|^2 r^2`, `m0_Jshell_frac`, `m0_Ncore`, `m0_Nshell`.
- **[IN VERIFICA — 1 solo seme]** Run `test_spincore.bat` seed 1 (2000 passi):
      in blocco, mentre il guscio cresce (`Nshell 327→3964`, `Rinerzia 3.6→5.8`)
      la precessione `|Lz|` (0.19→0.08) e `spin_core` (0.40→0.18) CALANO ~½ e la
      dispersione sale. MA le correlazioni ISTANTANEE guscio↔precessione sono
      DEBOLI (`corr(Jshell_frac,|Lz|)≈0.08`, `corr(Rinerzia,|Lz|)≈0.03`). Unico
      segnale medio: `corr(Jshell_frac, spin_core_disp)=+0.47` (il guscio
      DISORDINA lo spin, non lo congela per inerzia). CONFONDENTE grave: cresce
      TUTTO (`Ncore` come `Nshell`) → "guscio" confuso con "aging". Il run è stato
      INTERROTTO (seed 2 a metà) per passare ai test-gratis; CSV in
      `out_spincore/PRE_diffusione/`.

### FASE 0 (in corso): test-gratis prima di ogni modifica

- **[IN CORSO]** Prima di scrivere la diffusione di superficie, test-gratis
      (nessuna modifica al codice) su caso attaccato (`nmasse 3 sep 4 400 passi
      2 semi`, con `--cs-dinamico --chi-core --spinore-vivo`):
      (a) `--tauloc 1/5/10`: la dilatazione forte irrigidisce il core?
      (b) `--elast-c 100 vs 0`: il `d/cs` basta senza il ×100 (ELAST_C ridondante)?
      Output in `out_freetest/`. Decidere la Fase 1 (diffusione) solo dai risultati.

### FASE 0 — risultati bounded (2026-09-05)

- **[DIMOSTRATO] (a) tempo-proprio SATURO a tauloc 1.** `tauloc 1` (sep 8, 60 passi)
      ha `tau_max=1.414=√2`: il fattore tempo-proprio è GIÀ SATURO. `tauloc 5` si
      **impianta al PRIMO passo** (unbuffered stampa solo la legenda, poi nulla).
- **[RETTIFICATO — NEGATIVO su me stesso] Il "runaway di mitosi" NON è verificato ed è
      quasi certamente errato.** `tauloc 1` non cresce (`accr≈1116` costante su 30 passi);
      `tauloc 5` si pianta allo step 0, quando N è ancora iniziale → NON può essere
      accumulo di nodi O(N²). Causa probabile (non isolata): instabilità del primo passo
      ad alta dilatazione (sospetto sotto-ciclo CFL `nsub`). Da misurare prima di affermare.
- **[IN VERIFICA] (b) ELAST_C ridondante: inconcludente a 60 passi.** `elast-c 100`
      vs `0` danno deformazione core quasi identica (`|d-d0|/d0` 0.8331 vs 0.8305),
      MA a 60 passi ELAST_C è DORMIENTE (densità uniforme → `1+100·max(ρ/ρ_med−1,0)≈1`).
      Non è prova di ridondanza: serve core maturo/denso. Da rifare più lungo.
- **[REVERTATO] `--diag-ogni`**: era stato aggiunto per throttlare il diaglog (che gira
      a OGNI passo, ~0.8 s/passo, O(N·logN)); su richiesta di Luca il codice è tornato
      alla forma originale (`git checkout soliton_simulator.py`). Il fatto che le diagnostiche
      non siano throttled resta valido ma non è stato modificato.

---

## AGGIORNAMENTO PRECEDENTE — 2026-09-04

### Chiusura sessione 2026-09-04

- **[IMPLEMENTATO]** Il pozzo fisico locale è centralizzato in `Rete.pozzo_grafo()`
      e la vista campo interpola la stessa quantità `phi_g` usata da `GRAV_BIFASE`.
      La vista topologica non usa più un layout XYZ come se fosse la fisica.
- **[IMPLEMENTATO]** `--sync` usa una snapshot unica del passo precedente per
      campo, intensità, metrica e settore spinoriale; il ricalcolo è ammesso solo
      quando la mitosi cambia la topologia.
- **[IMPLEMENTATO]** Ogni CSV batch e `diaglog` contiene una riga iniziale
      `# RUN_PARAMS` con parametri CLI, leggi attive e costanti effettive.
- **[AGGIORNATO]** Le campagne core, spin/chiralità e matrice CS sono state
      predisposte con `--cs-dinamico` in tutte le varianti; `test_cs_dinamico.bat`
      conserva il ramo OFF per l’A/B dedicato.
- **[VERIFICATO]** Compilazione, controllo del diff e batch minimo metadata/sync
      completati senza errori.
- **[FERMATO]** I batch lunghi precedenti sono stati interrotti prima di questa
      modifica e non sono stati considerati risultati della nuova configurazione.

Relazione completa: `REPORT_SESSIONE_2026-09-04.md`.

### TODO — prossima sessione

- **[TODO PRIORITARIO 1]** Aggiungere e misurare `spin_core` e `spin_core_disp`
      usando solo la maschera del nucleo, senza selezione `perc_chi=+1`. Il test
      deve usare la catena fisica completa: `--sync --cs-dinamico --verlet
      --spinore-vivo --spin-feedback --chi-core --viriale --zeta-vir
      --pav-com --chi-basc --polo-maturo --olon-part --ls-azim --verso-chi
      --tau-d0 --zeta-loc --plast-din --calore-vett`.
- **[TODO]** Rilanciare tutte le campagne aggiornate con `--cs-dinamico`, usando
      DB/output nuovi e 2–3 semi.
- **[TODO]** Attendere 2000 passi e confrontare `cs_eff_*`, `dmin_nodi`, torsione,
      coerenza, spin, `m*_Lz` e `Lz_orb_*`.
- **[TODO]** Verificare se la quasi-collocazione dei nodi altera il pozzo `phi_g`.
- **[TODO]** Valutare precessione e frame dragging solo da serie temporali e
      osservabili relazionali, non da singoli fotogrammi.

### Stato documentale e geometrico

- **[FATTO]** `README.md` è la guida operativa del progetto. Contiene il preambolo
      sull'intento e sull'ontologia: i solitoni sono puntatori di fase; materia,
      spazio e tempo sono interpretati come emergenti dalle relazioni.
- **[FATTO]** `FISICA.md` contiene la formalizzazione matematica delle leggi
      implementate, con formule, definizioni, osservabili e livelli di evidenza.
- **[FATTO]** `GEOMETRIA_CONTATTO.md` descrive pedissequamente la geometria di
      contatto attuale: grafo, criterio `cKDTree`, portata, `d`, `d0`, rilassamento,
      mitosi e memoria topologica.
- **[FATTO]** Le formule KaTeX dei documenti sono state rese compatibili con il
      renderer: eliminate le macro non consentite come `\operatorname` e corretti
      i pedici ambigui come `T_*`.

### Stato fisico verificato nel codice

- **[IMPLEMENTATO, SPERIMENTALE]** `--cs-dinamico` calcola una velocità metrica
       locale dal rapporto tra $|\Psi|^2$ e il solo vicinato topologico, con
       profilo `tanh`, floor emergente dalla saturazione $CS_M/(1+\gamma\sqrt I)$
       e media armonica sugli archi. Rigidità metrica, CFL e smorzamento usano
       `cs_eff` locale; la validazione richiede run lunghi e più semi.

- **[IMPLEMENTATO, SPERIMENTALE]** `--chi-core` calcola la chiralità emergente
      del core locale da $\rho_0$, $\rho_c$ e $\lambda_{eff}$, usando tutti i
      nodi nella maschera e senza selezionare il segno. La quantità core-aware
      guida campo spinoriale, torsione dipolare e frame-dragging; `perc_chi`
      resta microscopica per nascita, scuotimento e mitosi. Stabilità del segno
      e impatto fisico sono ancora da validare.

- **[IMPLEMENTATO]** Lo spinore SU(2) è attivo di default (`SPINORE=True`) e il
      metodo `_passo_spinoriale` viene eseguito a ogni passo; non è una voce “da
      implementare”. L'ordine macroscopico resta da misurare.
- **[IMPLEMENTATO]** La schermatura è attiva di default (`SCHERMATURA=True`),
      ancorata a `N_c` adattivo e alla densità locale `rho=|Psi|^2`.
- **[IMPLEMENTATO]** `P_LAM` è mantenuto solo per compatibilità con vecchi
      comandi; `lambda_nodi()` non lo usa come esponente. `LAM_MIN` non è più usato.
- **[IMPLEMENTATO]** La portata locale è limitata da `0.15*LAM`, valore
      geometrico attualmente codificato e da sottoporre ancora a validazione.
- **[IMPLEMENTATO]** La diagnostica registra `ncrit_adattivo`, `rho_critica`,
      `lambda_eff_min/med/max`, `lambda_eff_ratio_med` e `rho_su_rhoc_max`.
- **[IMPLEMENTATO]** La sincronizzazione sul taglio usa esclusivamente riferimenti
      di vicinato pesati da `wI`: media locale del pozzo e RMS locale dello shear;
      rimossi i riferimenti globali `pozzo.mean()` e `disp_shear.mean()`.
- **[IMPLEMENTATO, SPERIMENTALE]** Aggiunto `--verlet`: il ramo opzionale usa
      Velocity-Verlet nel sottociclo metrico `d/vd`; default off, con Eulero
      canonico invariato. Riduzione delle oscillazioni ancora da verificare.
- **[IMPLEMENTATO]** Create le varianti `_verlet` di tutti gli script di test,
      inclusi `RunTutti_verlet.bat/.bash` e `run_differenza_verlet.bat`; gli
      output delle varianti usano nomi distinti per mantenere l'A/B riproducibile.
- **[IMPLEMENTATO, SPERIMENTALE]** Esposto `ELAST_C=100` tramite `--elast-c`:
      il default è non regressivo, `0` spegne il nucleo elastico e `30/100/300`
      sono predisposti per i test di sensibilità.
- **[IMPLEMENTATO]** Aggiunti `test_ridondanza.bat`, `test_sensibilita.bat` e
      `test_scala.bat`; vanno eseguiti in quest'ordine e richiedono run lunghi
      su più semi per una conclusione.
- **[AGGIORNATO]** `test_ridondanza.bat` è temporaneamente impostato a 300 passi,
      con DB/output separati e suffisso `_300`, per un controllo preliminare
      rapido senza riutilizzare i DB incompatibili del tentativo precedente.
- **[IMPLEMENTATO]** Aggiunto `test_elastico_300.bat` come alternativa separata
      per il test rapido multiseme; non riutilizza né modifica `test_ridondanza.bat`.
- **[IMPLEMENTATO]** Aggiunto `test_elastico_700_sep10.bat`: stesso A/B
      multiseme a `sep=10` e 700 passi, con output/DB separati dal test da 300.
- **[AGGIORNATO]** I tre test ELAST_C ora usano la catena completa (`sync`,
      `viriale`, `zeta-vir`, `pav-com`, `chi-basc`, `polo-maturo`, `olon-part`,
      `calore-vett`, `verlet`) e DB distinti per seme/condizione; `sync-db` serve
      solo a spezzare e riprendere il run.
- **[IMPLEMENTATO]** Aggiunti due test di precessione a run singolo:
      `test_precessione_verso_chi.bat` e `test_precessione_ls_azim.bat`.
      Usano `sep=10`, seed 1, 700 passi e producono dati separati; ogni script
      avvia un solo processo.
- **[IMPLEMENTATO]** Il batch crea automaticamente le directory padre per i
      percorsi di `--csv`, `--diaglog` e `--sync-db`, evitando il `FileNotFoundError`
      quando si lancia il comando da una checkout pulita.
- **[IMPLEMENTATO]** Anche la modalità video crea automaticamente la directory
      padre di `--out`; verificato con 3 frame in una cartella nuova.
- **[IMPLEMENTATO]** Protetta la scala del pozzo in `memoria_hebbiana_moto()`
      contro array vuoti, evitando il crash NumPy su `np.median([])` durante
      run video con topologia in evoluzione.
- **[IMPLEMENTATO, DIAGNOSTICO]** Aggiunta la circolazione topologica passiva:
      i cicli sono costruiti da `net.i/net.j` e la corrente usa densità locale,
      twist e allineamento spinoriale, senza embedding.
- **[DIMOSTRATO, NEGATIVO]** La diagnostica è valida: gauge-invariante per
      rinumerazione degli archi (differenza `~5e-18`), indipendente
      dall'embedding (perturbando `pos` la circolazione non cambia), nulla con
      twist nullo o rete senza cicli, e non-nulla (`~0.12`) su un campo di
      twist artificiale non-gradiente. **Ma sul run reale la circolazione è
      zero numerico** (`|Γ|_max ~1e-15` medio, `~4e-14` picco) mentre `m0_Lz`
      dello stesso run è `~0.022` medio con picchi `~0.77`. Rapporto
      `Γ/m0_Lz ~5e-14`. Interpretazione: il twist reale all'equilibrio è
      essenzialmente un gradiente di fase (curl-free), quindi non porta
      corrente circolante; la "rotazione" vista in `m0_Lz` è artefatto
      dell'embedding (il dito, non la luna). Conferma dal lato gauge-invariante
      il risultato negativo sulla precessione. **Fase C (accoppiamento dinamico
      `--corrente-ciclica`) non giustificata**: non c'è circolazione da
      ridirigere e crearne una richiederebbe una sorgente non-gradiente
      imposta a mano (parametro spurio).
- **[IN CORSO]** Sono in esecuzione i test `sep=10`: confronto ELAST_C a 700
      passi (tre semi) e test a run singolo dei canali `--verso-chi`,
      `--ls-azim` e della circolazione topologica. I CSV/log non vanno letti
      come completi finché i processi non terminano.
- **[AGGIORNATO]** Tutti gli script di lancio attivi includono esplicitamente
      `--sync`, sia per Eulero sia per Velocity-Verlet; questa uniformità non
      aveva un effetto fisico finché `SYNC_UPDATE` era un flag non operativo.
- **[AGGIORNATO]** I CSV di `out_elast/` e i log `log/elast*.log` dei test ELAST_C
      vengono conservati nel repository; i DB `.pkl` restano esclusi perché sono
      cache di ripresa e i filmati restano esclusi da `.gitignore`.
- **[IMPLEMENTATO, SPERIMENTALE]** `--sync` ora seleziona l'ETC esteso: il campo
      materia usa `_phi_t` e la sorgente metrica usa `_peq_t` (con fallback di
      sola inizializzazione per i nuovi archi). Default ancora off; convergenza
      e superiorità rispetto al percorso storico sono da misurare.
- **[VERIFICATO]** Batch minimo con e senza `--sync` completati senza errori né
      valori non finiti; il ramo sincrono stampa il flag e produce `diaglog`.
- **[VERIFICATO]** Compilazione Python e batch breve con `diaglog` completati
      senza errori; il `diaglog` contiene le nuove colonne della schermatura.
- **[DA VERIFICARE]** Stabilità della taglia, contrasto nucleo/guscio e
      indipendenza da seed su tempi lunghi (almeno ~2000 passi, preferibilmente
      20000 e 2–3 semi).
- **[IN VERIFICA]** `--sync` è ora operativo e produce traiettorie diverse dal
      percorso storico: su grafo controllato da 100 nodi/739 archi, dopo 50 passi
      la differenza massima è `2.73e-1` su `phi` e `1.35e-3` su `d`. Il test di
      convergenza preliminare (`dt=.01` contro `.005`, stesso tempo fisico, 10/20
      passi) non mostra ancora un vantaggio di sync: errore `phi` `1.36e-2` senza
      sync contro `2.37e-2` con sync. Non promuovere quindi a default: servono
      run lunghi, più semi e una metrica di errore relazionale.

### Audit delle sezioni storiche

**Già fatto e ancora valido nel codice:**

- grafo multimassa e diagnostica per massa/coppia (`mI_*`, `coer_*`, `cosphi_*`,
      `Lz_orb_*`, `dist_*`);
- `TAU_LOCALI=True`, calcio vettoriale-chirale, doppia copertura e spinore
      SU(2) attivo;
- repulsione emergente (`REPULS_LEGGE=True`), frame-dragging e metrica dinamica;
- schermatura non parametrica attiva, basata su `rho=|Psi|^2` e `N_c` adattivo;
- documentazione separata in `FISICA.md` e `GEOMETRIA_CONTATTO.md`, con link
      dal `README.md`;
- correzioni KaTeX già applicate e verificate tramite controllo dei documenti.

**Desueto o da interpretare solo come storia:**

- il TODO che chiede di **reimplementare SU(2)** e la struttura spinoriale a
      doppia copertura: l’implementazione è già presente e attiva; resta aperta
      soltanto la misura dell’ordine macroscopico;
- il TODO che chiede di **ancorare la schermatura a `N_c`** eliminando
      `P_LAM`/`LAM_MIN`: è stato realizzato; la validazione della stabilità rimane
      aperta;
- il riferimento a `run_tutti.bash`/`.bat` come “10 test a 10000 passi”: gli
      script attuali hanno configurazioni diverse e alcuni run Windows usano
      20000 passi;
- i percorsi `soliton_simulator_BACKUP_pre_multimassa_20250827.py` e
      `soliton_simulator_MULTIMASSA.py`: non risultano presenti nel repository
      corrente;
- i risultati numerici del blocco **RISULTATI SESSIONE**, inclusi periodo,
      segni e correlazioni del 2025: sono risultati storici e non vanno attribuiti
      automaticamente alla fisica corrente senza ripetizione con il codice attuale;
- il TODO sul “freno non-locale guscio←nucleo” resta concettualmente aperto,
      anche se la schermatura e le metriche di portata sono state implementate:
      non è ancora dimostrato che stabilizzino il guscio su tempi lunghi.

**Ancora aperto e coerente con il codice corrente:**

- run lunghi su 2–3 semi per stabilità, plateau e indipendenza dal seed;
- verifica della sopravvivenza dei buchi neri sotto schermatura;
- separazione tra accrescimento, creazione di coppie e materia nuova;
- precessione orbitale reale e canale di moto posizionale;
- derivazione fondamentale dei coefficienti residui e del limite `0.15*LAM`;
- attrattore della densità del vuoto e rimozione del seme iniziale come input.

Le sezioni successive conservano il registro storico del progetto. Le voci che
contraddicono questo aggiornamento vanno interpretate come stato precedente e
non come descrizione dell'implementazione corrente.

---

## STATO ATTUALE DEL CANONICO

File ufficiale: **`soliton_simulator.py`** (canonico corrente).
Il backup pre-promozione citato nelle note storiche non è presente nel repository corrente.

**Default fisici ora ufficiali:**
- `REGIME = "deterministico"` (era stocastico)
- `TAU_LOCALI = True` — forma tau pura (tre tau locali, kappa=1, nessun parametro)
- `CALORE_VETTORIALE = True` — calcio termico vettoriale-chirale (innesco precessione)
- `TAU_USA_D0 = False` — usa d (distanza reale); d0 attivabile con `--tau-d0`

**Flag reversibili CLI:** `--tau-d0`, `--calore-scal`, `--calore-vett`, `--regime stocastico`, `--giri 0`.

Documento teorico canonico aggiornato: **`FISICA.md`** e **`GEOMETRIA_CONTATTO.md`**.
Documento storico: **`doc/leggi_del_sistema_solitoni .docx`**.

---

## FATTO (questa sessione)

- **Diaglog multimassa**: traccia tutte le masse (mI_*) e le interazioni per coppia (coer_ab,
  cosphi_ab, Lz_orb_ab, dist_ab). Header CSV dinamico.
- **Flag d/d0** (`--tau-d0`): tau_p su d0 invece di d. A run corti d~d0; divergono solo su run lunghi.
- **Calcio vettoriale-chirale** (`--calore-vett`): omega_s 3D + firma chirale di phivel. Verificato
  alla semina: chiralita' netta 0.39 (vs 0.03 scalare), omega_s 0.64 (vs 0).
- **Promozione a canonico** con backup datato. Default: determ + pura + calcio vett.
- **Documento**: sezioni 9.X (oscillatore di fase) e 9.Y (frustrazione + calcio chirale).
- **Script** di esperimento: disponibili `RunTutti.bat`, `RunTutti.bash` e gli
      script A/B `run_*.bat`; le durate e le condizioni sono definite dentro ciascun file.

## RISULTATI SESSIONE (livelli di certezza)

- **[DIMOSTRATO]** Binario = **oscillatore di fase**: interferenza oscilla costruttiva<->distruttiva,
  periodo ~1200-1800 passi. Confermato a sep 6, 8, 12.
- **[DIMOSTRATO]** **Nessuna precessione orbitale netta** nel binario: pendolo, non rotazione. Le
  rotazioni nei video erano camera auto (`--giri 0` per fermarla).
- **[DIMOSTRATO]** Insorgenza valle **ritardata dalla distanza** (leva): sep 12 il ciano parte dopo ~300 passi.
- **[DIMOSTRATO]** Tre masse: triangolo geometricamente rigido, dinamicamente asimmetrico. Pozzo
  centrale collettivo emergente.
- **[IN VERIFICA -> INDEBOLITO]** Calcio chirale come innesco precessione: 1o test (300 passi, 1 seed)
  coppie concordi (+0.37 gradi); 2o test (seed diverso) coppie DISCORDI (-0.12 gradi). NON replicato ->
  probabile rumore del seme. Serve run lungo + piu' semi. **Da aggiornare in docx 9.Y.**

---

## DA FARE — TODO STORICI DELLA SESSIONE (da riconvalidare)

- [ ] **Riconvalidare i run lunghi** degli script attuali, non necessariamente a 10000 passi.
- [ ] A/B **calcio vett vs scalare** con gli script attuali e 2-3 semi: Lz_orb concordi/crescenti
      (rotolamento) o pendolo? Escludere il caso del seed.
- [ ] **d vs d0 su run lungo**: respiro, oscillazione fase, valle ciano (d0 a 600 passi gia' meno ciano: 25 vs 44%).
- [ ] **Stabilita' oscillazione di fase** a 10000 passi (5-8 cicli): stabile, smorzata o amplificante?
- [ ] Dopo step ~2000: il pendolo diventa rotazione o resta oscillazione?
- [ ] Aggiornare la documentazione storica sul calcio chirale con il secondo seed e i risultati
      dei run lunghi; la documentazione corrente è in `FISICA.md`.
- [ ] Segno "azzurro tira": misura RITARDATA (non istantanea) della distanza ai picchi di ciano, su run lungo.

---

## DA FARE — TODO DAL DOCUMENTO (questioni aperte accumulate)

### Punto 0 — PRIORITA' MASSIMA: lo spin dei solitoni
- [x] **Struttura spinoriale implementata**: doppia copertura, Bloch e accoppiamento SU(2) sono
      presenti nel canonico e attivi di default. Restano da misurare ordine macroscopico e livelli.

### Programma di eliminazione dei 6 parametri residui
- [x] **P1**: costanti temporali locali espresse come rapporti adimensionali. _Implementazione presente;
      con TAU_LOCALI (forma pura), ma vedi sotto "kappa"._
- [ ] **P2** (buon candidato): `KICK_TW=0.35` -> conversione dell'energia torsionale elastica accumulata
      E_tw = 1/2 K_C (Theta/2pi)^2 alla mitosi, invece di un calcio fisso.
- [ ] **P3** (parziale): `G_PH=0.15` (attrito di fase, disperde energia fuori dal grafo) ->
      termostato di Nose-Hoover locale ancorato alla temperatura-legge.
- [ ] **P4** (da dimostrare): `ALPHA_M` -> forza hamiltoniana. _Nota: dimostrato che ALPHA_M e'
      irriducibile a c_s; resta l'altra via._
- [ ] **P5** (contiene errore aritmetico da correggere): `DENS_CRIT_C` -> coefficiente geometrico.
      L'integrale e' corretto ma la derivazione di C non chiude. Derivare C nel regime lineare s<<1.
- [ ] **P6** (ricerca aperta, alto rischio): `SEME_INIZIALE=900` -> far partire da grafo minimale
      (N=4, simplesso fondamentale) e lasciar emergere un punto fisso attrattore.
- [ ] **Aggiornamento P2 (kappa)**: la calibrazione a scala fissa NON regge; con tau_p = kappa*d/c_s
      usando i vecchi valori come kappa, il tempo plastico effettivo cambia. Da chiudere.

### Anello torsione-fase e questione Hamiltoniana
- [ ] Formalizzare: spazio degli stati (grafo dinamico), varieta' di contatto estesa, Hamiltoniana di
      contatto sul grafo. Chiarire se il frame-dragging va nel settore conservativo o dissipativo.

### Griglia scaling e calibrazione Planck
- [ ] **[P1 doc]** Completare la griglia dello scaling (~meta' punti fatti) per blindare gli esponenti
      di N_c ~ lambda^-3 * gamma^0.14.
- [ ] **[P2 doc]** Calibrazione alla scala di Planck: risolvere le masse iper-Planckiane (il ponte
      verso le masse fisiche non chiude, pur essendo coerente sul lato velocita').

### Stabilizzazione della taglia della materia (accrescimento infinito)
- [ ] **Riconvalidare** se schermatura e repulsione-legge stabilizzano la taglia: non è più
      corretto registrare come fatto attuale che il sistema “non stabilizza” in assoluto.
- [ ] Verificare che il freno effettivo agisca sul **GUSCIO** (dove avviene la mitosi), non solo
      sul centro già congelato.
- [ ] Modulare la separazione dell'anti-nodo come tanh(s): annichilazione dolce a bassa densita',
      netta ad alta. Resta da misurare l'efficacia del singolo evento di annichilazione.
- [x] Ancorare scala e profondita' della schermatura a `N_critico` invece che a parametri liberi
      (`P_LAM` e `LAM_MIN` non controllano più la dinamica).
- [ ] Verificare che i buchi neri (fenomeno reale nei video lunghi) restino tali sotto la nuova legge
      di freno — non sopprimerli per errore.

### Repulsione-legge e ramo repulsivo
- [ ] **[in verifica]** La repulsione-legge frena la divergenza ma il **plateau non e' ancora raggiunto**
      (run 2 masse >1400 passi). Elevare da "promettente" a "dimostrato".
- [ ] Sorvegliare il ramo repulsivo sui tempi lunghi (scrive sulla metrica di riposo, canale a rischio deriva).
- [ ] Il ramo repulsivo e' empiricamente sfuggente (si attiva solo in opposizione di fase): trovare test robusto.

### Piano di lavoro post-sessione kernel/mitosi (dal documento)
- [ ] Consolidare le 3 osservabili di controllo (olonomia, R90, sopravvivenza coerenza).
- [ ] **Rimisurare le leggi precedenti** col nuovo kernel razionale e nuova mitosi 4pi (hanno cambiato
      scala di massa e torsione).
- [ ] Attribuire con rigore il moto del baricentro (monotonia ~0.87) col controfattuale a soglia locale OFF.
- [ ] Vuoto a densita' emergente: manca un attrattore pulito, dipende dal seme.
- [ ] Coarse-graining: progettarlo conservativo (non alterare gli invarianti). **Solo DOPO la Fase 1**,
      mai prima (comprimere senza conoscere gli invarianti rompe la fisica).
- [ ] Pendenza della transizione di mitosi (oggi dolce): renderla piu' ripida senza introdurre parametri.
- [ ] Test smorzamento del gradiente di torsione: decade o raggiunge un asintoto?
- [ ] Costruzione del **canale di moto posizionale**: il ponte tra frame-dragging (che agisce sulle
      fasi) e le posizioni dinamiche (limite aperto registrato piu' volte).

---

## RITRATTAZIONI REGISTRATE (non ripetere questi errori)

- **Il pozzo misurato sul dito**: usare la lunghezza assoluta invece delle relazioni sugli archi era
  sbagliato. Misurare sempre le relazioni.
- **Rapporto 3.06 non fidato** (coincidenza tautologica) e **dilatazione tempo proprio inaffidabile**.
- **L_CONSERVA** (imporre rotazione rigida a mano) concettualmente sbagliato -> DEFAULT OFF.
- **Precessione scritta a mano**: tentativo di imporre la rotazione del vettore di Bloch -> rifiutato.
  La precessione non va scritta a mano, deve emergere.
- **Legge XIX** (gusci/confinamento) e un **corollario di chiralita'**: ritirate dopo test falliti.
- **[2026-09-03] Spinore SU(2) congelato = misure non-abeliane invalide.** Git-archeologia: la chiamata
  a `_passo_spinoriale` (evoluzione SU(2)) è stata persa come collaterale del refactor a snapshot/commit
  atomico ETC nel commit `d2c76f3` (2026-09-02) — bug, non scelta (messaggio "add script" non menziona
  lo spinore; `SPINORE=True` e init di `_nb` tenuti; funzione lasciata orfana, non cancellata). Da allora
  `_nb` resta all'init planare (coplanare → solid angle nullo). **Tutte le misure di fase di Berry /
  curvatura non-abeliana dal 2026-09-02 sono su spinore congelato: l'assenza non-abeliana NON è
  dimostrata, è artefatto di codice morto.** Anche la nota di CLAUDE.md "SU(2) attivo, chiamato a ogni
  step" era falsa e va considerata ritratta. La riattivazione (dietro flag, reinnesto nell'ordine ETC,
  A/B, rimisura) è l'unico modo per testare davvero il canale non-abeliano.

---

## PROBLEMI NOTI / TRAPPOLE

- **Batch vs Video separati**: `--batch` usa `--passi` (ignora --frames); `--test "..."` usa `--frames`
  (ignora --passi). Batch ignora --test (semina in cerchio via --nmasse).
- **Camera auto inganna**: video ruotano di default (`--giri 1.0`). `--giri 0` per camera ferma.
- **Video interrotti = illeggibili**: il moov atom si scrive a fine run. Non interrompere; usare --frames
  che finisca da solo.
- **Run corti (<2000 passi) ingannano**: la dinamica vera si sveglia dopo step ~2000. Non concludere sotto.
- **Un solo seed inganna**: il calcio chirale sembrava funzionare su 1 seed, smentito dal secondo. 2-3 semi sempre.
- **d/d0 nel diaglog**: la varianza di d/d0 (CV~0.28) e' la firma del **coarse-graining** dei regimi di
  scala (SCALA_B), NON un difetto. Gli invarianti relazionali (coerenza, cos dphi, grado) sono robusti (CV~0.001-0.006).
- **La media non va nelle leggi locali**: niente medie/mediane globali dentro le equazioni tau.

---

## FILE CHIAVE

| File | Ruolo |
|------|-------|
| `soliton_simulator.py` | **canonico** (determ + pura + calcio vett di default) |
| `FISICA.md` | formalizzazione delle leggi implementate |
| `GEOMETRIA_CONTATTO.md` | geometria di contatto e metrica degli archi |
| `doc/leggi_del_sistema_solitoni .docx` | documento storico delle leggi |
| `RunTutti.bash` / `RunTutti.bat` | lancia i test generali; durata definita nello script |
| `CLAUDE.md` | norme per l'agent (guardiano, principi, disciplina sperimentale) |