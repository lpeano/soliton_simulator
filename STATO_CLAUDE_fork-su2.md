# STATO PER CLAUDE — branch `fork-su2`

> File di continuità locale al branch, aggiornato a OGNI commit/push (regola Luca 2026-09-11).
> Serve a Claude per riprendere lo stato senza rileggere tutta la storia. Lingua: italiano.
> La doc canonica di tracing vive su `main`; questo è lo stato operativo del branch di sviluppo.

## BRANCH — il fork vive QUI (regola Luca 2026-09-13)
- **`fork-su2`**, creato da `dev-spinoriale` al commit **`c9fcc1e`** (blob `soliton_simulator.py`
  = **4fc7a794**, invariato al momento della biforcazione). Tracciato su `origin/fork-su2`.
- **Tutte le modifiche al `.py` per il fork SU(2) si fanno QUI, non su `dev-spinoriale`**, che
  resta la BASELINE intatta: se il non-abeliano demolisce, ci si torna in un secondo
  (`doc/ROADMAP_fork_SU2.md`, sezione PREPARAZIONE).
- Questo file e' il rename di `STATO_CLAUDE_dev-spinoriale.md` (un solo file di stato per branch,
  il nome dice quale). **ATTENZIONE AL MERGE:** se un giorno `fork-su2` rientra in
  `dev-spinoriale`, il rename cancellerebbe lo stato di quel branch — va risolto a mano,
  consapevolmente, non lasciato fare a git.
- **Il blob 4fc7a794 CESSA di essere il riferimento su questo branch** appena il PEZZO 1 tocca il
  `.py`. La precondizione "blob == 4fc7a794" scritta in `ROADMAP_dev-spinoriale.md` e nel
  gate-cache vale ancora per `dev-spinoriale`, NON per `fork-su2`: qui il gate va **ri-timbrato
  sul nuovo blob** (altrimenti il guard di `csv/_test_53c/_run_batch.ps1` blocca ogni campagna).

## Ultimo aggiornamento
- Data: 2026-09-13
- Ultimo commit: STATO allineato a CLAUDE.md v2 + documenti di riferimento in `doc/`.
- Branch allineato con `origin/dev-spinoriale`.
- Blob `soliton_simulator.py` = **4fc7a794** (verificato dal disco, invariato: nessuna modifica al codice).

## REGOLE E DOCUMENTI (aggiornamento 2026-09-13)
- **CLAUDE.md v2** e' l'istruzione autorevole (sostituisce `.github/copilot-instructions.md`, che resta
  solo come contesto storico). Novita' rispetto alla v1: par.0-bis (leggi le istruzioni a ogni avvio +
  rilettura dopo compattazione), par.5 politiche di commit (un commit = un cambiamento logico, forma del
  messaggio, commit anche del sigillo FALLITO poi STOP, niente `Start-Sleep`/polling), par.5-bis
  auto-manutenzione (CLAUDE.md per i fatti stabili, STATO a ogni commit, commit dedicato per le regole).
  Promosse in par.2/4 tre regole prima solo in copilot-instructions: snapshot/restore COMPLETO incluso RNG
  per la purezza pure-read; `--cs-dinamico` implica `--chi-core` e `--spinore-vivo`; mai confronti a passo
  fisso su sistema che si espande (aliasing).
- **Documenti di riferimento ora NEL REPO**, cartella `doc/` (prima esistevano solo nel Progetto/chat,
  assenti da tutti i branch e dalla storia git -> il par.0-bis non era eseguibile):
  `BUSSOLA_dev-spinoriale.md`, `BUSSOLA_TECNICA_dev-spinoriale.md` (v2), `ROADMAP_fork_SU2.md`,
  `PROTOCOLLO_test_olonomia.md`, `SYSTASIS_nota_concettuale.md`.
- **CONFLITTO D'ORDINE: RISOLTO (Luca, 2026-09-13) -> FORK-FIRST.** Vale CLAUDE.md par.6: si parte dal
  fork non-abeliano; GAMMA / Step 1A / Step 2 (cs<->orologio) / Step 3 (alpha_G) sono **A VALLE**
  (a densita' reali cs e' MORTO, I~0.05 vs soglia ~400 -> ogni test cs-dipendente oggi e' NULLO).
  Allineati di conseguenza: `ROADMAP_dev-spinoriale.md` (radice) marcata **SUPERATA** (rimandata, NON
  ritrattata: la matematica resta valida e si riprende dopo il fork) e la sua "PROSSIMA AZIONE"
  marcata SOSPESA; `doc/BUSSOLA_dev-spinoriale.md` riga 86, puntatore corretto a
  `doc/ROADMAP_fork_SU2.md` + nota che la sua lista 0-4 e' l'ordine STORICO, non di esecuzione.
- **ROADMAP VIVA = `doc/ROADMAP_fork_SU2.md`** (Preparazione -> PEZZO 1 -> PEZZO 2 -> PEZZO 3, un pezzo
  un sigillo). Il test di verifica e' `doc/PROTOCOLLO_test_olonomia.md`, da eseguire DOPO il sigillo di
  riduzione al limite (se non passa, misurerebbe un bug, non la fisica).
- **§9 RIVERIFICATO DA LUCA sul repo (blob 4fc7a794): sano tranne la riga gia' corretta.** Confermati
  dal disco: forza 2207-2208 ✓, cs 2187 ✓, omega_clk/`_phc`/dt_n NON usano cs ✓, chiamata
  `_passo_spinoriale` 2419 dietro SPINORE_VIVO ✓, ancora elastica 3234-3237 con filtro
  `1-tanh(d/LAM)` a 3224 ✓. L'unico sbaglio era 2196 (docstring citato come codice), gia' fixato.
- **COORDINAMENTO (regola Luca 2026-09-13): la CLAUDE.md AUTOREVOLE e' quella NEL REPO.** Le copie
  fuori dal repo sono indietro sul fix 2207-2208 e **NON vanno ripushate** (rimetterebbero l'errore).
  Le modifiche a CLAUDE.md le applica Claude Code nel repo; Luca fornisce il testo esatto.

## PROSSIMA AZIONE — FORK, STRATO 0 (PEZZO 1)
Ordine operativo in `doc/ROADMAP_fork_SU2.md`, un pezzo un sigillo, flag OFF di default:
1. **PEZZO 1** — funzione `U_ij(n_i,n_j)` isolata: `chi=arccos(n_i.n_j)`, `m_hat=(n_j x n_i)/|...|`,
   `U_ij=exp(-i (chi/2) m_hat.sigma)`. Sigilli: allineati -> U->I ; `U U^dag = I` ; caso antipodale
   gestito dal PESO (Pezzo 2), MAI da una convenzione d'asse.
2. **PEZZO 2** — peso `w_ij=|n_j x n_i|=sin(chi)`. Niente soglia netta, niente coefficiente tarato.
3. **PEZZO 3** — cablaggio nella forza, **righe 2207-2208** (`_coppia_interferenza`):
   `Im<psi_i|psi_j> -> w_ij * Im<psi_i|U_ij|psi_j>`. Attenzione all'ORIENTAMENTO (`U_ij=U_ji^dag`):
   con gli scalari era irrilevante, ora conta. Sigillo: flag OFF / allineati -> BYTE-IDENTICO.
4. Poi (lettura, gratis): controllare che `SYNC_UPDATE` e `SCUOTIMENTO` siano ATTIVI nella config del
   fork, altrimenti la degenerazione dei Bloch non si rompe.
5. Poi le verifiche dinamiche (Luca gira, Claude legge): distribuzione degli angoli chi, olonomia
   W(r) secondo `doc/PROTOCOLLO_test_olonomia.md`, isotropia `<n>`.

## ROADMAP A VALLE (GAMMA / cs<->orologio) — ⚠ RIMANDATA dopo il fork (2026-09-13)
> Vedi `ROADMAP_dev-spinoriale.md` (marcata SUPERATA) + `/memories/repo/roadmap_todo.md`.
> **Non e' il lavoro corrente**: la prossima azione e' il fork Strato 0 (sezione sopra). Questa
> sezione resta come RECORD del piano e della sua matematica: valida, solo rimandata.

Obiettivo: EM e gravita' come 2 proiezioni dello STESSO campo spinoriale, con la giusta gerarchia.
- Canali gauge-invarianti = MODULO |psi|^2 (gravita') vs FASE/segno (EM). MAI Re/Im per-arco
  (2 proiezioni di 1 solo grado, gauge-dipendenti; Im = motore forza, non carica). Bargmann e' CIECO
  al segno (telescoping) -> misura EM = phase-locking TEMPORALE (SYNC/Kuramoto).
- STEP 0 SALTATO (Luca): seed-1 (B) = BASELINE INTERNA, non risultato robusto. seed-2/3 = TODO
  rimandato (solo se il (B) andra' presentato come stabilito).
- STEP 1A [SOSPESO, non piu' la prossima azione] (pure-read, NON tocca .py): scrivere `_run_3gamma.ps1` +
  `_analizza_3gamma.py`, coarse-graining a blocchi di b, fittare d in gamma_eff(b)~b^d nei due canali
  (modulo; fase via SYNC). Verdetto: FASE d~0 + DENSITA' d<0 = gerarchia emersa. Sigillo b=1=identita' byte-id.
- STEP 1B (flag `--gamma-nudo`/`--gamma-relazionale`), STEP 2 (accoppiamento cs<->orologio:
  omega_clk*(cs/CS_M)^2, solo magnitudine; segno invariato; sigillo cs=CS_M byte-id + stabilita'),
  STEP 3 (esplorativo alpha_G, magnitudine NON torna ~35 ordini). Tutto SCRITTO, NON eseguito.
- Regola: CHECKPOINT a Luca tra ogni step. Precondizione ripresa: blob == 4fc7a794.

## VERDETTO SEED 1 (completo, 3 bracci a 800 passi) — (B) abeliano su tutti
| Braccio | N | solo-materia (2a met) | spin_ovl | segno_ov | verdetto |
|---|---|---|---|---|---|
| b1_base | 4713 | -0.00024 | 0.5000 | 0.638 | (B) abeliano |
| b2_orolseg (5.3c) | 4933 | +0.00011 | 0.5000 | 0.631 | (B) abeliano |
| b3_orolseg_cs (5.3c+cs) | 4697 | +0.00028 | 0.5000 | 0.637 | (B) abeliano |
- Solo-materia decade sempre 0.65->~0. cs-dinamico NON aggiunge ordine (b3 ~ b1/b2).
- Misure gauge-robuste concordi: spin_ovl=0.5000, segno_ov~2/pi ovunque.
- PUNTO 3 (asimmetria settori): la firma AGISCE ma non ordina. frac_chi_neg: b1=0.4997,
  b2 (5.3c)=0.5122 (verso antimateria), b3 (5.3c+cs)=0.4917 (verso opposto). N diverge (b2 4933).
- CAUTELA: 1 solo seed. Non consolidato -> servono seed 2 e 3 (gate-cache -> cache-hit istantaneo).
- berry_segno IGNORATO (cieco: olonomia Bargmann chiusa telescopa la fase per-nodo del segno).

## Cosa è stato fatto (in ordine)
1. **MOD 5.3c `--orologio-segno`** (commit `77c83e5`): firma il VERSO dell'orologio de Broglie INTERNO
   `_phc = exp(-0.5j * s_k * omega_clk * dt)` con `s_k = sign(perc_chi)` STABILE (materia exp−, antimateria exp+).
   Vive nel ramo `--deparam-orologio`. Richiede `--campo-spinoriale --spinore-corretto`.
   SIGILLI GATE PASS: OFF byte-identico (max|A−B|=0 su 32 array), riduzione-al-limite esatto, |ψ|=1, stabilità.
2. **Reperto**: sotto `--campo-spinoriale` la firma NON è inerte — il segno per-nodo cambia l'interferenza del
   campo emesso `mat(w)@_psi_spinor` → rho_spin → N diverge (3228→3273) = canale non-abeliano VOLUTO (Fase 3).
3. **Presidio carica per-coppia** (commit `c45a81b`): la firma è APPEND-ONLY su perc_chi (0/120 riscritture),
   Schwinger antinodo = −perc_chi[genitore], quantizzazione ±1. Σperc_chi drifta solo per lignaggio (mitosi).
4. **FIX presidio critico** (commit `109744a`): `segno_arco_coer_materia` NON più tautologico — settore materia
   selezionato con `perc_chi>0` (etichetta stabile), misura coerenza di `_sgn` (doppia-copertura). + `n_arco_materia`.
   Baseline: 0.65 → ~0 (metrica discrimina). Statistica: 54206 archi materia-materia.
5. **FIX PUREZZA DIAGLOG** (commit `109744a`): bug pre-esistente — sotto `--campo-spinoriale` il diaglog
   contaminava (N 3228 vs 3299). Cause: cache `psi_spin,rho_spin,_psi_spin_prec` + stato RNG non nello
   snapshot/restore. Estesi `_snap_fisica` (diaglog) e `_snap_cond` (condensazione). VERIFICATO byte-identico
   con/senza `--diaglog` (max|A−B|=0) nel config NON-verlet.
6. **Regole comportamentali** (commit `2f8fa61` + copilot-instructions): (a) diaglog/trace SOLO-LETTURA, mai
   toccare la fisica, verifica byte-identico obbligatoria; (b) ogni commit → push, messaggi approfonditi,
   commit/push prima di ogni run; (c) `--verlet` default nei test.

## Campagna 5.3c — CHIUSA come baseline (non e' il lavoro corrente)
> La prossima azione e' il **fork Strato 0** (sezione "PROSSIMA AZIONE" sopra). Quanto segue e' il
> record della campagna e i suoi TODO, che restano aperti ma RIMANDATI.

- **SEED 1 COMPLETO** (vedi verdetto sopra): (B) abeliano su b1/b2/b3.
- **TODO RIMANDATO: seed 2 e 3.** Servono solo se il (B) andra' presentato come risultato STABILITO
  (oggi e' BASELINE INTERNA, 1 seed). Comando: `powershell -File csv/_test_53c/_run_batch.ps1 -seed 2`
  poi `-seed 3` (gate-cache -> cache-hit istantaneo se il blob e' invariato). Commit/push PRIMA di ogni
  run. Attenzione OOM se video attivo. NB: il fork cambiera' il blob -> gate da ri-timbrare.
- Poi: verdetto consolidato a 3 seed + punto 3 (asimmetria) + effetto cs.
- **Verdetto** (arbitro = `segno_arco_coer_materia` SOLO-MATERIA): (A) sale/resta = ordine vero;
  (B) ~0 = separazione/abeliano. Guardare SOLO-MATERIA, non il totale. Analisi: `csv/_test_53c/_analizza_bracci.py`.

## Config base dei bracci (identico al pilota 5.3a + firme + verlet + deparam)
`--batch --nmasse 3 --sep 8 --passi 800 --ogni 100 --campo-spinoriale --spinore-vivo --spinore-corretto
--chi-core --calore-scal --deparam-orologio --verlet` + `--seed S` + firma del braccio.

## Presidi di Luca ancora aperti
- Ri-confermare 5.3a pulito dopo il fix (nel launcher, run `r53a_tsegno_s1`).
- Monitorare braccio 3 (`--cs-dinamico`) per instabilità; STOP se cs non governa il cono causale.

## ARBITRO GAUGE-INVARIANTE — OLONOMIA DI BARGMANN (Luca 2026-09-11)
- Domanda di Luca "la correlazione e' calcolata bene?" -> scoperto che `segno_arco_coer` e' GAUGE-DIPENDENTE
  (segni relativi a canon(nb_k), frame locali diversi per nodo; correlazione su arco APERTO e' gauge-dipendente).
- Verdetto (B) regge per TRIANGOLAZIONE con misure gauge-INVARIANTI: spin_overlap=0.5 (direzione random),
  segno_ov_absmedia~2/pi=0.637 (fase doppia-copertura uniformemente random).
- CURA DEFINITIVA aggiunta (pure-read, in circolazione_topologica + diaglog): OLONOMIA DI BARGMANN di
  _psi_spinor su cicli chiusi = arg(prod <psi_k|psi_{k+1}>). Gauge-invariante per costruzione. La berry su nb
  e' cieca-al-segno (§38-bis); questa usa il PRIMARIO -> sonda DIRETTAMENTE il segno-orologio. Colonne:
  berry_spinor_media (FIRMATA = l'arbitro: ~0=frustrato blindato, !=0=ordine), _media_assoluta, _rms, _max.
- RE-RUN NECESSARIO per popolare berry_spinor. IN ATTESA: Luca genera un VIDEO (python 27104, config 5.3c+cs)
  -> no contention. Al via, rilanciare i batch (gate-cache auto-verifica il nuovo blob + purezza col nuovo pure-read).

## GATE-CACHE (Luca 2026-09-11) — rigore + velocità
- I gate NON sono più solo script a mano: `csv/_test_53c/_run_batch.ps1` ha un GUARD che legge `gate_cache.json`
  ancorato al **git BLOB** di `soliton_simulator.py` (byte attuali, cattura anche modifiche non committate).
- Cache-hit (blob invariato + PASS) → parti istantaneo. Cache-miss/stale → `_gate.ps1` rigira il presidio UNA
  volta e timbra la cache; se FAIL → STOP (non lancia i bracci). Qualsiasi modifica al .py invalida la cache.
- Gate vivo = `_check_presidio.py` (purezza byte-id + baseline discrimina + non-tautologico, exit 0/1).
  Sigilli firma (OFF byte-id, riduzione-al-limite, norma) = analitici + verificati al sigillo 77c83e5.
- Uso: `powershell -File csv/_test_53c/_run_batch.ps1 -seed N` (auto-gate su cache-miss).

## Futuro concordato (non ora)
- Refactor diaglog→messaging: produttore emette snapshot immutabile; consumer applica REGOLE PURE
  disaccoppiate da `net`, fa i conti pesanti a parte. Purezza per costruzione.
