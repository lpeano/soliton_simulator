# STATO PER CLAUDE — branch `dev-spinoriale`

> File di continuità locale al branch, aggiornato a OGNI commit/push (regola Luca 2026-09-11).
> Serve a Claude per riprendere lo stato senza rileggere tutta la storia. Lingua: italiano.
> La doc canonica di tracing vive su `main`; questo è lo stato operativo del branch di sviluppo.

## Ultimo aggiornamento
- Data: 2026-09-11
- Ultimo commit: `2f8fa61` (regola commit/push)
- Branch allineato con `origin/dev-spinoriale`.

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

## In corso / prossimo
- **Purezza diaglog VERIFICATA byte-identica** (max|A−B|=0) sia NON-verlet sia CON `--verlet` (config test).
  Baseline `segno_arco_coer_materia` 0.65→~0 (metrica discrimina), 54039 archi materia-materia (statistica solida).
- **Campagna PRONTA ma IN ATTESA** (Luca sta generando un video → no contention/OOM): lanciare
  `csv/_test_53c/_run_bracci.ps1` quando la macchina è libera:
  - RI-CONFERMA 5.3a pulito (`--tempo-segno` seed 1) vs baseline b1 → il NO-GO regge senza contaminazione?
  - 9 BRACCI (3 × seed 1,2,3): b1_base, b2_orolseg (`--orologio-segno`), b3_orolseg_cs (`+ --cs-dinamico`).
- **Verdetto** (arbitro = `segno_arco_coer_materia` SOLO-MATERIA): (A) sale/resta = ordine vero;
  (B) ~0 = separazione/abeliano. Guardare SOLO-MATERIA, non il totale. Analisi: `csv/_test_53c/_analizza_bracci.py`.

## Config base dei bracci (identico al pilota 5.3a + firme + verlet + deparam)
`--batch --nmasse 3 --sep 8 --passi 800 --ogni 100 --campo-spinoriale --spinore-vivo --spinore-corretto
--chi-core --calore-scal --deparam-orologio --verlet` + `--seed S` + firma del braccio.

## Presidi di Luca ancora aperti
- Ri-confermare 5.3a pulito dopo il fix (nel launcher, run `r53a_tsegno_s1`).
- Monitorare braccio 3 (`--cs-dinamico`) per instabilità; STOP se cs non governa il cono causale.

## Futuro concordato (non ora)
- Refactor diaglog→messaging: produttore emette snapshot immutabile; consumer applica REGOLE PURE
  disaccoppiate da `net`, fa i conti pesanti a parte. Purezza per costruzione.
