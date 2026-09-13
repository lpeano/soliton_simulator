# CLAUDECONNECT — Transcript di sessione (agent ↔ Luca)

> File di continuità della chat con l'agent (GitHub Copilot / Claude) sul progetto
> **Sistema dei Solitoni Relazionali (VQT / U2)**. Trascrive cronologicamente le richieste
> di Luca e le azioni/risposte dell'agent, con i livelli di certezza (DIMOSTRATO / IN VERIFICA
> / APERTO / NEGATIVO). Da mantenere aggiornato a ogni scambio. Lingua: italiano.
>
> Convenzioni: "L:" = Luca, "A:" = agent. Vedi anche `Checkpoint.md`, `CLAUDE.md`,
> `/memories/repo/` per lo stato macchina.

---

## Sessione 2026-09-05

### 1. L: inerzia del guscio → massa irrimovibile? (analisi matematica)
**Domanda.** Se troppa materia nel guscio, l'inerzia rende la massa irrimovibile? Come si
calcola? Come seminare masse stabili non congelate.

**A — analisi (verificata nel codice, non nei commenti).** Tre "inerzie" distinte:
- **(A) fase**: `Δv = dt/M_PH·(T−ξv)`, `M_PH=1.0` COSTANTE ([soliton_simulator.py] L206/L1892). Uniforme, il guscio non la irrigidisce.
- **(B) spin**: `ω += dt·(B×n/|Ψ|² − ω/τ)` (L1556/L1577). `|Ψ|²` a DENOMINATORE (resistiva) ma LOCALE: guscio antifase ha `|Ψ|²` basso → reagisce in fretta, non congela; il lento è il nucleo.
- **(C) moto della massa (memoria hebbiana)**: sposta `d0` ∝ `|Ψ|²·mem_mot` (numeratore = momento), con TETTO per-arco `±0.01·median(d0)`.

Risultato: la tua intuizione vale netta per la **rotazione**: momento d'inerzia `J = Σ|Ψ|² r²`
([soliton_simulator.py] L2534) → un guscio lontano domina `J ∝ r²`. Tensione tra **massa dinamica**
`M_dyn = Σ|Ψ|²` (guscio incluso) e **massa coerente** `M_coh = Σ cos(φ−φ_m)` (guscio antifase
sottrae). Rapporto `R = M_dyn/M_coh` = "inerzia per massa coerente" = l'irrimovibilità quantificata.
Livelli: J-rotazionale **DIMOSTRATO** (formula); dominanza reale del guscio **IN VERIFICA**; semina **APERTO**.

### 2. L: usano la velocità della luce non omogenea?
**A — verifica.** Sì ma solo a metà. Con `--cs-dinamico` (default OFF, [soliton_simulator.py] L262)
la `cs` locale entrava SOLO nel settore ondulatorio (rigidità `cs²·lap`, smorzamento `β`, CFL).
NON entrava (usavano `CS_M` globale): **sorgente** (`CS_M²/d`), **τ_p plastico delle d0**, **termostato**.
Cioè i canali che muovono/assestano la massa (l'inerzia plastica) giravano su c OMOGENEA. **DIMOSTRATO**
(disomogeneità interna reale: rigidità locale, sorgente+τ_p globali).

### 3. L: no, con --cs-dinamico tutto deve usare c dinamica e locale
**A — modifica (coerenza, non esperimento).** Backup datato `soliton_simulator.backup_2026-09-05_cs-locale.py`.
Con `CS_DINAMICO=True` ora TUTTO il settore metrico usa `cs_arco`:
- Helper `_cs_nodo()` = unica fonte della legge `cs(ρ)`.
- Sorgente: `cs_arco²/d`.
- τ_p plastico: `d/cs_arco`.
- Termostato: `cs_rappr²·P_eq`, `cs_rappr` = mediana del campo locale (gauge globale → mediana lecita).
Ramo `CS_DINAMICO=False` byte-identico. Compile OK; smoke ON+sync/ON-nosync(fallback)/OFF exit 0;
`cs_eff` presente in ON, assente in OFF.
**Nota guardiano [DIMOSTRATO]**: la modifica APPROFONDISCE il congelamento del nucleo (cs bassa nel denso → τ_p più lungo).

### 4. L: con --cs-dinamico servono sempre --chi-core e --spinore-vivo, anche nei test
**A.** Regola registrata in `/memories/repo/convenzioni_flag.md`. Applicata:
- A/B puliti: `test_cs_dinamico.bat`, `test_spin_chiralita_nativo.bat` → aggiunto `--chi-core`.
- Matrici che variano chi-core (`test_matrice_cs_ordine_richiesto.bat`, `test_metriche_chiralita_spin_precessione.bat`):
  conflitto segnalato; su scelta di Luca → aggiunto `--chi-core` a TUTTE le celle (BASE/FEEDBACK collassano in duplicati).

### 5. L: sospetto — troppo guscio congela masse e precessione (intrinseca+estrinseca). Verifica analitica + come seminare
**A — analitica onesta (conferma in parte, corregge in parte).**
- **Estrinseca (orbitale): CONFERMATO [DIMOSTRATO analitico]** — `J ≈ N_s I_s R_s²`, `Ω_orb ∝ 1/J`, raggio al quadrato.
- **Traslazione: [IN VERIFICA]** — l'àncora rigida è il NUCLEO (τ_p lungo, cs bassa), il guscio è fluido; ma un guscio pesante gonfia `M_dyn` e resiste via rete elastica. Netto = competizione.
- **Intrinseca (spin): NON supportata [NEGATIVO già dimostrato]** — killer = auto-spegnimento da allineamento (`corr(S_M,ω_S)=−0.43`), non il guscio.
- **Semina**: già compatta+coerente (`fase=0.0`, [soliton_simulator.py] L4293); il freezing è EMERGENTE (mitosi). Rimedio vero = "freno non-locale guscio←nucleo" (TASK APERTO già registrato, [soliton_simulator.py] L54).

### 6. L: quindi? → costruisci la diagnostica
**A.** Bottom line: va MISURATO. Agganciata la macchina `centro_/guscio_` esistente.

### 7. L: guarda nei TODO il primo test per oggi, aggiungi le metriche e il test, lancialo
**A — errore e correzione.** Preso all'inizio il "primo test" dalla MEMORIA di repo (chiralità di
gruppo `⟨χ_i χ_j⟩`): creato `test_chi_corr.py`, lanciato (3 semi, 400 passi). Verdetto PRELIMINARE:
z_perm medio 0.76 → pista morta / nessuna struttura (400 passi = solo formazione).

### 8. L: ma hai verificato nel Checkpoint cosa dovevi fare?
**A — correzione.** Il vero primo test è il **Checkpoint TODO PRIORITARIO 1**: `spin_core` /
`spin_core_disp` sulla maschera del nucleo, senza selezione `perc_chi`, catena completa. Implementato
nel diaglog (`m0_spin_core`, `m0_spin_core_disp`): vphi sul nucleo (quartile interno raggio), pesato `|Ψ|²`, no chiralità.

### 9. L: aggiungi quanto visto sul congelamento da guscio
**A.** Aggiunte colonne diaglog (massa 0, dominio nucleo+guscio): `m0_Mdyn`, `m0_Mcoh`,
`m0_Rinerzia=Mdyn/|Mcoh|`, `m0_Jrot=Σ|Ψ|²r²`, `m0_Jshell_frac`, `m0_Ncore`, `m0_Nshell`. Compile+smoke
catena completa OK; colonne presenti (a 40 passi tutto nucleo: Ncore 369, Nshell 3, R 1.03).

### 10. L: i 3 switch attivi con cs-dinamico? attivali, committa, pusha, lancia lungo
**A.** `test_spincore.bat` ha già i 3 switch (`--cs-dinamico --chi-core --spinore-vivo`) + catena
Checkpoint completa. Creato `test_spincore.bat` (2 masse, sep 8, 2000 passi, 3 semi). **Commit+push**
`48310e0`. Lanciato lungo in background.

### 11. L: verifica i numeri (seed 1 completo)
**A — lettura onesta (1 solo seme).**
- In blocco: guscio cresce (`Nshell 327→3964`, `Rinerzia 3.6→5.8`) mentre `|Lz|` (0.19→0.08) e
  `spin_core` (0.40→0.18) CALANO ~½, dispersione sale. Direzione a favore.
- MA correlazioni ISTANTANEE deboli: `corr(Jshell_frac,|Lz|)≈0.08`, `corr(Rinerzia,|Lz|)≈0.03`.
  Unico segnale medio: `corr(Jshell_frac, spin_core_disp)=+0.47` → il guscio DISORDINA lo spin, non lo congela.
- CONFONDENTE grave: cresce TUTTO (Ncore come Nshell) → "guscio" confuso con "aging".
- Verdetto: ipotesi direzionalmente supportata in blocco, NON confermata come meccanismo causale pulito.

### 12. L: (da guardiano) prompt strutturato — FASE 0 test-gratis prima, poi diffusione solo se serve
Ordine: (0) stop run in corso + salva CSV in `PRE_diffusione/`; test-gratis `--tauloc 1/5/10` (dilatazione→rigidità?)
e `--elast-c 100 vs 0` (ELAST_C ridondante con d/cs?). (1) diffusione di superficie `--guscio-morbido`
(default off): `d0 += dt_e·D·lap_d0`, `D = cs_arco·d_arco` (nessun parametro libero), CFL, floor. (2) A/B lungo.
Vincoli: flag default off; laplaciano = quello delle onde; nessun parametro nuovo; mostra il diff prima di applicare.
"PROCEDI IN AUTONOMIA, committa e mantieni il Checkpoint a ogni step."

**A — FASE 0 in corso.**
- Stoppata campagna spincore (seed 2 a metà); CSV/pkl/log preservati in `out_spincore/PRE_diffusione/` e `log/PRE_diffusione/`.
- Checkpoint aggiornato (blocco 2026-09-05).
- Batteria (a) `tauloc 1/5/10` × 2 semi lanciata.

### 13. L: stime tempi Fase 0
**A — ALLARME dai dati reali.** `tauloc 1` (30 passi, no diaglog) = **80,3 s** → ~2,7 s/passo: è il
costo della FISICA (caso attaccato sep 4 + catena completa + cs-dinamico), non del diaglog. `tauloc 5`
run 2: PID vivo, **~2,6 h CPU, ZERO output** → all'epoca etichettato **"runaway di mitosi"**. **[RETTIFICATO
in §17: NON verificato, quasi certamente ERRATO — è un impianto del PRIMO passo, non crescita nodi.]**
La stima "1-2 min/run" valeva solo per `tauloc 1`. Run impiantati fermati. (Errore mio: usato
`Start-Sleep` — da evitare.)

### 14. L: trascrivi la chat in CLAUDECONNECT sulla root, mantienilo aggiornato, committa+pusha, riprendi
**A.** Creato questo file. Commit+push di tutto (`0fd36b7`). → ripresa Fase 0 **ri-scalata** a taglia
che finisce (ridurre passi/masse o disattivare il runaway), poi tabelle (a)/(b), poi decisione diffusione.

### 15. L: autogenera il file canonico di regole di Copilot + obbligo di manutenere CLAUDE.md
**A.** Creato `.github/copilot-instructions.md` con le regole di questa chat (lingua italiana; guardiano;
due principi ferrei; "la media non va qui"; verifica nel codice non nei commenti; livelli di certezza;
disciplina sperimentale 2000 passi + 2-3 semi; test-gratis prima delle modifiche; flag default-off +
backup datato + py_compile + smoke + A/B una variabile + mostra diff; `--cs-dinamico ⟹ --chi-core +
--spinore-vivo`; batch≠video; MAI Start-Sleep/polling; runaway mitosi; manutenzione `Checkpoint.md` +
`CLAUDECONNECT.md` + **`CLAUDE.md`** + `/memories/repo/`; commit a ogni step, push solo su richiesta).

### 16. Fase 0 ri-scalata (bounded) + throttling diagnostiche
**Contesto (guardiano di Luca):** rallentamento attribuito (all'epoca) al "runaway" da `--tauloc` alto.
**A — risultati bounded (sep 8, seed 1):**
- **(a) tauloc [NON CONCLUSA — vedi §17]**: `tauloc 1` 60 passi = 139s, `tau_max=1.414=√2` (fattore
  tempo-proprio GIÀ SATURO, DIMOSTRATO); `tauloc 5` si impianta al primo passo. La causa NON è un runaway
  di nodi (vedi §17): resta solo la saturazione del fattore a tauloc 1.
- **(b) ELAST_C — INCONCLUSIVO [IN VERIFICA]**: a 60 passi `elast-c 100` vs `0` danno deformazione
  core quasi identica (`|d-d0|/d0` 0.8331 vs 0.8305). MA ELAST_C è DORMIENTE quando la densità è
  uniforme (`1+100·max(ρ/ρ_med−1,0)≈1`) → non è prova di ridondanza. Serve core maturo/denso.
- **Throttling [VERIFICATO nel codice]**: `_diag_completa` (Delaunay vortici + centro/guscio + J/inerzia)
  gira a OGNI passo (riga ~5061), NON throttled. Costo ~0.8 s/passo (~34% runtime su ~800 nodi), O(N·logN)
  non O(N²). Era stato aggiunto `--diag-ogni N`, poi **REVERTATO** (§17, richiesta di Luca: forma originale).

### 17. L: aspetta — spiega il runaway, c'era o no? se non c'era torna alla forma originale
**A — RETTIFICA onesta (guardiano).** Il "runaway di mitosi" NON era verificato ed è quasi certamente ERRATO.
Prove misurate: (1) `tlq5.log` (tauloc 5, `python -u` unbuffered) stampa SOLO la legenda dei flag, poi NULLA:
nessuna riga di step → si impianta DENTRO il primo `net.step()`, quando N è ancora quello iniziale (nessuna
mitosi possibile). (2) `nd_tl1.log` (tauloc 1, senza diag): `accr≈1116→1117` su 30 passi → ZERO crescita
nodi. Quindi NON è accumulo progressivo di nodi (O(N²)). Causa reale, probabile ma non ancora isolata:
instabilità numerica del PRIMO passo ad alta dilatazione (sospetto: sotto-ciclo metrico CFL `nsub` che
esplode). **Codice riportato alla forma originale**: `git checkout` di `soliton_simulator.py` → rimosso
`--diag-ogni` (era l'unica modifica non committata). py_compile OK. Lezione: non etichettare un meccanismo
senza misurarlo ("misura prima di concludere").

### 18. L: throttling SOLO per le metriche pesanti; poi — il campionamento è FISICA (aliasing/Nyquist)
**Contesto (guardiano di Luca):** (a) throttlare solo le metriche pesanti, le altre a ogni passo; (b) poi
un argomento fisico profondo: certe metriche oscillano al passo (Lz, Berry, fasi) → throttlarle è **aliasing**
(sotto Nyquist si ricostruisce fisica FALSA, come sotto-risolvere Planck). Per le veloci serve campionamento
fine; se fossero anche pesanti servirebbe messaggistica **async** (cattura leggera ogni passo + calcolo fuori).

**A — misura prima (guardiano).** Avevo ri-aggiunto `--diag-ogni` con `_diag_leggera` (solo min/max/mean) +
`_diag_completa` throttlata. **ERRORE:** le metriche VELOCI (`m0_Lz`, `berry`, `spin_neel`, `guscio_circ`,
`m0_spin_core`) stavano nel blocco throttlato → le avrei **aliasate**. **Edit annullato** (`git checkout`),
codice al baseline corretto (tutto ogni passo, niente aliasing), py_compile OK.

**Classificazione MISURATA** (da `tl1_diag.csv`, 60 passi ogni-passo, lag-1 autocorr):
- VELOCE (aliasing se throttlata): `m0_Lz` (ac −0.23), `berry_spin_media` (−0.04), `spin_neel_modulo`
  (−0.09), `guscio_circ` (0.30), `centro_cosphi`, `m0_spin_core`.
- LENTA (throttle-safe): `m0_Mdyn`/`m0_Jrot` (ac 1.0), `m0_Rinerzia`, dispersioni, `d_mean`,
  `m0_carica`/vortici (Delaunay, costante), `dens_g*`.

**Conclusione architetturale [MISURATA]:** le metriche veloci sono tutte ECONOMICHE (Lz=PCA 2×2, spin=media
mascherata, Berry/Neel=piccole somme); le pesanti (Delaunay, profilo radiale) sono LENTE. **Nessuna metrica
è fast∩heavy → l'ASYNC NON serve.** Basta: veloci-economiche a ogni passo, throttle solo lente-pesanti.
(In Python l'async su numpy CPU-bound pagherebbe GIL + copia snapshot: costo reale, beneficio nullo qui.)
Eccezione non ancora classificata: `m*_picco_*` (spin picco per-massa) — possibile fast∩heavy, da misurare.

### 19. L: prompt FASE 1 (verifica) — la pesante è lenta o alimenta veloci? profila e riporta prima di agire
**A — profiling MISURATO** (stato reale caricato da `tl1_db.pkl`, n=824, archi=138k, grafo denso):
| sub-blocco | ms | alimenta | natura |
|---|---|---|---|
| `chiralita_core_locale` | 94 | `chi_core_*` | RIDONDANTE — già cachata in `self._chi_core_nodi` (step, riga 1858) |
| cicli + `circolazione_topologica` | ~60+47 | **berry_spin_media (VELOCE)** + olonomia/circ (lente) | alimenta VELOCE → non throttlabile |
| `calcola_psi` | 22 | ricalcolo | RIDONDANTE — `self.psi` già calcolata nello step |
| Delaunay vortici/inerzia/`dens_g*` | ~4 | m0_carica/Jrot (lente) | throttle-safe ma MINORE |

**VERDETTO §19 [poi RETTIFICATO in §20]:** avevo concluso "riusare `self.psi` e `self._chi_core_nodi`
già calcolati (byte-identico, ~116 ms)". **SBAGLIATO** — vedi §20.

### 20. RETTIFICA: il riuso NON è byte-identico (la mitosi cambia N) → pivot a 2A throttle di chi_core
**A — errore e correzione (guardiano; Luca aveva segnalato l'esatto dubbio).** Fra il cache nello step e il
ricalcolo nel diaglog c'è la **mitosi** (cambia N e topologia) + rilassa + memoria. Quindi `self.psi` e
`self._chi_core_nodi` cachati sono a N VECCHIO/metà-step, mentre `_diag_completa` li ricalcola a N NUOVO
(fine-step). Riusarli darebbe numeri DIVERSI → **il "byte-identico" NON regge**. Il riuso (2B) è abbandonato.

**Soluzione corretta = 2A throttle SELETTIVO.** Misurato che `chi_core_*` è **COSTANTE/lenta** (lag-1) → la
funzione più cara (`chiralita_core`, 94 ms su grafo denso) è **throttle-safe**: diradarla NON aliasa.
Implementato flag **`--diag-lente-ogni N`** (default 1 = IDENTICO): con N>1 solo `chi_core` è calcolata ogni
N passi (+ prima riga per l'header), mentre Berry/Neel/Lz/spin_core/guscio_circ restano a OGNI passo.

**VERIFICATO:** py_compile OK. A/B 20 passi (`dl1` vs `dl10`): a N=1 tutte le colonne 21/21 dense (=baseline);
a N=10 `chi_core`/`rho_c_core` = 3/21 (diradate), mentre `berry`/`spin_neel`/`m0_Lz`/`m0_spin_core`/`guscio_circ`
= **21/21 dense → zero aliasing**. Speedup nullo a 20 passi (grafo piccolo, chi_core ~1 ms) ma ~85 ms/passo
risparmiati **a scala** (chi_core = 94 ms a n=824, misurato). Byte-identico a N=1 per costruzione
(`if CHI_CORE and diag_lente` = `if CHI_CORE` quando N=1).

### 21. RETTIFICA FINALE: due difetti di chiralita_core_locale nel diaglog → CURA ALLA RADICE (lettura pura + snapshot/restore)
**Contesto (2 reperti indipendenti):** (A, §20) il ricalcolo nel diaglog è a N nuovo (mitosi) → non
byte-identico; (B, reperto Claude) `chiralita_core_locale()` è IMPURA: muta `self._chi_core_nodi` (riga ~954)
che la FISICA legge a ~1967 (frame-drag/torsione). Il diaglog che la richiama (riga ~4362) SOVRASCRIVE lo
stato fisico → diagnostica accoppiata alla fisica. Il throttle (§20) NON era la cura giusta (mascherava, non
risolveva). **Verificato nel codice: entrambi i reperti reali.**

**CURA ALLA RADICE (il diaglog è SOLO LETTURA):**
1. `chi_core` nel diaglog: **lettura pura** del cache `getattr(net,'_chi_core_nodi',None)`, mai richiamare
   la funzione mutante né ricalcolare.
2. **Snapshot/restore** dei cache di CONTINUITÀ FISICA che le funzioni diagnostiche mutano transitoriamente
   e che la dinamica legge: `psi` (da `_pesi`→`lambda_nodi`), **`_psi_prec`** (da `ritmo()`, tempo proprio —
   il colpevole principale: il diaglog chiamava `ritmo()` pre-aggiornando `_psi_prec` → dt diverso il passo
   dopo), `_spinor_lift` (feedback spinoriale).
3. Rimosso il flag `--diag-lente-ogni` (dead code: chi_core in lettura pura non costa più i 94 ms).

**VERIFICA OBBLIGATORIA — PASSA.** Stesso caso (sep 4, `--chi-core --spinore-vivo --cs-dinamico --sync`, seed 1,
40 passi) con diaglog ogni passo vs senza: stato fisico finale **BYTE-IDENTICO** (phi/phivel/d/d0/tw/pos/perc_chi/eta,
`max|A−B| = 0.000e+00`, N_A=N_B=1288). Prima della cura divergeva (N_A=1373 poi 1935 vs N_B=1568). Post-pulizia
ri-verificato (1207=1207). `chi_core_media`/`m0_Lz`/`berry` restano densi a ogni passo. **Reperto B chiuso: il
diaglog non muta più la fisica.** Lezione: una diagnostica che chiama funzioni IMPURE (cache letti dalla
dinamica) accoppia misura e fisica — il diaglog dev'essere read-only, con snapshot/restore dei cache condivisi.

---

## Stato corrente (per la ripresa)

### §24. RISULTATO — congelamento da guscio: 2 semi puliti (diaglog non contamina)
Campagna `test_spincore.bat` con diaglog SOLO-LETTURA (fisica byte-identica). Seed 1 e 2 completi (2000 passi),
seed 3 in corso. Analisi (correlazioni + trend 1ª/2ª metà):
- **In blocco, concorde su 2 semi:** mentre il guscio cresce (Nshell 483→5490 / 308→4210; Rinerzia 3.6→6.8 /
  2.0→4.7), `spin_core` cala (0.28→0.04 / 0.14→−0.24), `|Lz|` cala (0.080→0.038 / 0.075→0.020),
  `spin_core_disp` sale (1.37→2.64 / 1.55→1.81).
- **Correlazioni istantanee:** `corr(Jshell_frac,|Lz|)` = +0.05/−0.06 ≈ **0**; `corr(Rinerzia,|Lz|)` = +0.04/−0.02 ≈ **0**;
  `corr(Nshell,|Lz|)` = −0.09/−0.25 (debole); `corr(Nshell,spin_core)` = −0.10/−0.62; **`corr(Jshell_frac,spin_core_disp)`
  = +0.47/+0.40 (CONCORDE).**
- **VERDETTO [IN VERIFICA, 2 semi]:** l'ipotesi "il guscio congela la precessione per INERZIA" **NON è confermata**
  (corr con |Lz| ~0, cambia segno). Il calo di |Lz| in blocco è confuso con l'AGING (cresce tutto: ~21000/18000 nodi).
  Il segnale **REALE e concorde**: il guscio **DISORDINA lo spin del nucleo** (Jshell_frac↔spin_core_disp ≈ +0.4;
  Nshell↔spin_core negativo). NON congelamento inerziale → **frustrazione/disordine**. Stesso segnale (+0.47) del
  run contaminato di seed-1 → è fisica reale, non artefatto del diaglog (la cura era necessaria ma non l'ha inventato).
- **CONTRO-PROVA in corso:** A/B `--guscio-morbido` (OFF s1 fatto, ON s1 in corso): se smussare il guscio riduce
  `spin_core_disp`, il disordine viene davvero dal guscio ruvido.

### §25. SPINORE & DOPPIA COPERTURA — indagine + risultato (NEGATIVO)
**Domanda di Luca:** "pensavo lo spinore funzionasse, cosa mancava?" → verifica nel codice.
- **Stato verificato:** `SPINORE_VIVO` on (evoluzione viva, non l'orfano). MA lo spinore è agganciato **solo alla
  CHIRALITÀ** (χ_i·χ_j → riflessione σz/σx = generatori SU(2)), **NON alla TORSIONE a 4π** (`tw`, doppia copertura):
  il canale tw→spinore vive solo in `SPIN_LARMOR` (off, storicamente fallito per auto-spegnimento).
- **Le "due z"** (spinore a 2 componenti col segno, `_spinor_lift = [cos(θ/2), sin(θ/2)e^{iφ}]`) **ci sono ma
  come LIFT DERIVATO** dal Bloch a una z: il segno a doppia copertura è **misurato, non guidato**. L'evoluzione è
  SO(3) sul Bloch; il segno è ricostruito per continuità, non un DOF primario.
- **Cosa mancava:** che il **twist a 4π pilotasse il Bloch** — precessione di **`tw/2`** (la metà = firma spin-½)
  attorno a un asse persistente.
- **IMPLEMENTATO `--tw-spinore`** (default off, byte-identico OFF, commit `bf0f75e`): Bloch precede di `tw/2`
  attorno all'asse σ chirale (persistente, non `n_i×n_j` che si auto-spegneva in SPIN_LARMOR). Smoke 30 passi:
  non destabilizza (nodi stabili), `spin_cluster_omega` +94%, `guscio_circ` 1.0→0.5. **Promettente in formazione.**
- **RISULTATO A/B 2000 passi (3 semi ON vs 2 OFF, sep 6) — DIMOSTRATO NEGATIVO:** a equilibrio **ON ≈ OFF su tutto**.
  `spin_cluster_omega`: ON 0.010/0.010/0.011 vs OFF 0.011/0.010 (identico). Auto-spegnimento `corr(M,ω) ~ −0.35`
  presente in ENTRAMBI. `spin_core`/`guscio_circ`/`|Lz|`: rumore seme-a-seme, nessuna differenza sistematica.
  → il boost dello smoke era **solo formazione**; a equilibrio il twist a 4π satura, `tw/2` diventa offset inerte,
  l'ordinamento spin si auto-spegne come sempre. **L'aggancio così com'è NON dà lo spin coerente sperato.**

### §26. Prerequisito risolto: il diaglog contaminava la fisica (§21)
Prima di ogni misura di spin: `chiralita_core_locale` (muta `_chi_core_nodi`) e `ritmo` (muta `_psi_prec`),
letti dalla dinamica, venivano chiamati dal diaglog → la diagnostica alterava la fisica. Reso SOLO-LETTURA
(lettura pura + snapshot/restore di psi/_psi_prec/_spinor_lift). Fisica BYTE-IDENTICA con/senza diaglog (verificato,
commit `2465d2d`). Senza questo, nessuna misura di spin era affidabile.

### §27. COVARIANZA — critica di Luca ("hai fatto misure covarianti? il sistema si estende!")
**Punto (giusto):** le misure erano in TEMPO-COORDINATA e mediate su una POPOLAZIONE che cresce (N: 372→~20000).
Non covarianti → "il dito, non la luna". Il "calo" di spin poteva essere l'espansione, non la fisica.
**Re-analisi covariante (dati tw_spinore, confronto a N APPAIATO invece che a passo fisso):**
- `tau_mean = 1.000` sempre → il tempo proprio MEDIO è gaugeato a 1 (mediana del ritmo); la covarianza che conta
  qui è la POPOLAZIONE crescente, non il clock.
- **Il "calo" era in gran parte DILUIZIONE da espansione:** a N appaiato la coerenza `spin_cluster_modulo` è
  ROBUSTA (~0.7); cala solo mite 0.73→0.70 da N=8k a N=16k (non il collasso che vedevo a passo fisso).
- **A N=16k, ON > OFF** (S_M: ON 0.711 vs OFF 0.686, concorde su 3 semi) → `--tw-spinore` dà un PICCOLO vantaggio
  di coerenza che il confronto a passo fisso NASCONDEVA. `omega`/tempo-proprio: ON ≈ OFF.
- **VERDETTO RIVISTO:** §25 ("ON=OFF, nullo") va AMMORBIDITO — covariantemente c'è un accenno di effetto ON
  (piccolo, ~+0.025, da confermare per significatività). E il §24 ("guscio disordina lo spin") va RI-VERIFICATO
  covariante: parte del disordine/calo potrebbe essere diluizione da espansione.
- **LEZIONE (metodologica, per Claude):** in questo sistema che si ESTENDE, misurare a passo fisso e su media
  globale è NON covariante. Servono osservabili INTENSIVI/adimensionali, coerenza PER DOMINIO, confronto a
  N/tempo-proprio-cumulativo APPAIATI. Da implementare nel diaglog prima di dichiarare verdetti.

### Stato campagne (2026-09-06)
- **spin_core (3 semi):** §24 confermato — guscio DISORDINA lo spin (corr Jshell↔spin_core_disp +0.47/+0.40/+0.51),
  NON congela per inerzia. Dati cancellati dal working dir su richiesta (recuperabili da git, commit `fc88537`).
- **tw-spinore A/B (`out_tw_spinore/`):** §25, negativo. In fase di commit anche se non tutto finito (off_s3 parziale).
- **guscio-morbido (FASE 2) e regimi (sep 5/6/8/12):** dati cancellati (working dir pulito), da rifare se serve.
- **APERTO:** l'aggancio doppia-copertura→spin va ripensato (l'asse σ chirale non basta a evitare l'auto-spegnimento
  a equilibrio); oppure il segnale è genuinamente frustrato (plasma vortice-antivortice bilanciato, `m0_carica`~0).

### Riferimenti codice/commit
- **[FATTO, `2465d2d`] CURA ALLA RADICE (§21):** diaglog SOLO-LETTURA (chi_core lettura pura + snapshot/restore
  di psi/_psi_prec/_spinor_lift). Fisica byte-identica. Flag `--diag-lente-ogni` rimosso.
- **[FATTO, `41f75b5`] FASE 1 (§23):** diffusione `--guscio-morbido` (default off): `d0 += clip(dt_e*D*lap(d0),
  ±cs*dt_e)`, `D = cs_arco*d_arco` (nessun coeff. nuovo). Smussa solo il guscio.
- **Codice base**: cs-locale integrale, spin_core, diagnostica inerzia guscio (`48310e0`/`a5bf7de`).
- **Aperto:** instabilità del warmup a `--tauloc` alto (sospetto CFL `nsub`, IN VERIFICA); ELAST_C 100 vs 0 su core maturo.
- **Governance**: flag default-off; 2000 passi + 2-3 semi; verificare nel codice; misura prima, modifica dopo;
  il campionamento è fisica (no aliasing); **il diaglog è SOLO LETTURA (mai mutare stato fisico)**.

---

## §28 — PACCHETTO SPINORE CORRETTO + KURAMOTO SU(2) (2026-09-06)

Catena di gate rigorosi (Copilot analizza → si ferma → Luca+guardiano confermano → implementa), costruita
pezzo per pezzo dalle domande di Luca. Ogni passo sotto flag default-off, evaluate-then-commit, sigilli passati.

### Richieste di Luca (cronologia)
1. "gestisci tutte le misure metriche in modo covariante SEMPRE" → regola covarianza in copilot-instructions +
   `analisi_covariante.py` (confronto a N appaiato). [committato+pushato]
2. "Implementa la gestione corretta dello spinore sotto `--spinore-corretto`… PRIORITÀ ASSOLUTA: cache e
   contemporaneità (evaluate-then-commit). Prima MOSTRA (i) variabili snapshottate (ii) niente commit di
   metà passo (iii) estensione cache dopo mitosi. Non procedere finché non confermo."
3. (dopo conferma) → implementato `--spinore-corretto` + flag separati `--chi-da-spinore`, `--tempo-proprio-orientato`.
4. "Aggiungi Kuramoto sul settore SPINORE sotto `--sync-spinore`… MOSTRA (i) formula omega_sync (ii) ordine ETC
   (iii) zero parametri. Non procedere finché non confermo." → confermato: omega_sync in omega_tot (rotazione),
   NON in omega_s (memoria) — torque istantaneo, non momento conservato (altrimenti accumulo/divergenza).
5. "Testa --sync-spinore a SCALA (minimo freddo), non tutto acceso: classi A prerequisiti / B candidate una
   alla volta / C rumore. Attento alla soglia di Kuramoto."
6. "procedi con campagna lunga ma prima aggiorna Claude."

### Cosa è stato implementato (tutto default-off, sigilli passati)
- **`--spinore-corretto`** (master): OROLOGIO PROPRIO de Broglie [omega_clk=(rho/rho_c)·r lungo l'asse di Bloch
  PROPRIO nb = pura fase] + SPINORE PRIMARIO complesso `_psi_spinor` (n×2) in SU(2); Bloch `_nb` DERIVATO
  (nb=psi†σψ). U=exp(-i/2 ω·σ dt), |psi|=1 atomico. Richiede `--spinore-vivo`. **Risolve la collisione di nome**:
  `self.psi` è il campo materia U(1), lo spinore è `_psi_spinor` (nuovo).
- **`--chi-da-spinore`** (flag 3): perc_chi = segno di doppia-copertura di `_psi_spinor` DOPO il commit; disattiva
  CHI_BASC; richiede `--spinore-corretto`.
- **`--tempo-proprio-orientato`** (flag 4): r con SEGNO (toglie |.| da f in `ritmo()`).
- **`--sync-spinore`**: Kuramoto SU(2). `omega_sync = forza·(nb × nb_media)`, `nb_media=(wI@nb_t)/uno` da
  snapshot t-1, `forza` = la STESSA del Kuramoto-φ (K_SYNC, 2/π, prof_rel, rinforzo_shear). Torque ISTANTANEO
  → in `omega_tot` (rotazione), MAI in `omega_s` (memoria). Zero parametri nuovi.
- **Cache coerenti dopo mitosi/Schwinger** (`_eredita_spinore_figli`, regola D): il figlio eredita lo spinore
  COMPLESSO del genitore col segno (antinodo = −psi); estende anche `_psi_prec` → elimina il RESET SPURIO
  globale in `ritmo()` su len!=n. Audit di TUTTI i punti di crescita di n (semina/mitosi/Schwinger).
- **Diaglog sola-lettura** esteso: snapshot/restore di `_psi_spinor,_nb,_nb_prec,omega_s,phi_s`.

### Sigilli (verificati)
- `--spinore-corretto`: OFF byte-identico (max|A−B|=0, n=831); ON |psi|²=1.000000, `_psi_spinor/_nb/omega_s`
  tutti len==n dopo mitosi (n=842). Commit del pacchetto.
- `--sync-spinore`: OFF byte-identico (max|A−B|=0, n=831); ON |psi|²=1, len==n (n=844). Commit.

### Test a SCALA (metodo guardiano) — `test_sync_spinore.bat`
- **STEP 1 MINIMO FREDDO**: solo prerequisiti (`--spinore-vivo --spinore-corretto --sync`), regime deterministico
  = FREDDO (SCUOTIMENTO off), niente classe B/C. A/B ON vs OFF, 3 semi, 2000 passi, sep 6.
- Misura COVARIANTE (N appaiato): `spin_cluster_modulo` (→1?), Berry firmata/assoluta, dispersione omega/assi.
- **Soglia di Kuramoto**: può sincronizzare il nucleo (denso) ma non il guscio (rado, frequenze disperse) →
  risultato fisico, va LETTO non forzato.
- **APERTO**: la macchina corretta è necessaria NON sufficiente per lo spin ½; l'ordinamento (frustrazione) è
  il problema separato che `--sync-spinore` prova a sciogliere.
- **STEP 2/3** (dopo): candidate una alla volta (--cs-dinamico, --chi-core, --guscio-morbido); annealing.

### In corso
- Campagna STEP 1 FERMATA e RILANCIATA con misure COVARIANTI (richiesta Luca: "voglio tutte le misure
  covarianti, poi fermi e rilanci"). `spin_cluster_modulo` e `spin_core*` non erano covarianti: media globale
  che diluisce ~1/sqrt(N) / unita' di phivel che driftano col vuoto / settore materia non spinore.
- **Aggiunti al diaglog osservabili COVARIANTI (intensivi, adimensionali, per-dominio), diaglog byte-identico**:
  - `spin_axis_R` = |media VERSORI di Bloch| globale [0,1] (non diluisce, sostituisce spin_cluster_modulo).
  - `m0_spin_axis_R` = allineamento spinori nel NUCLEO [0,1] = parametro d'ordine del Kuramoto SU(2).
  - `m0_omega_axis_R` = allineamento ASSI degli orologi (omega_s) nel nucleo [0,1].
  - `m0_spin_core_cv` = spin_core_disp / scala freq comovente (mediana |phivel|, gauge) -> adimensionale.
- **Tutti i run hanno SEMPRE --sync** (ETC/contemporaneita'): gia' in PREREQ, entrambi i rami A/B.

### §29 — STEP 1 RISULTATO: NEGATIVO covariante (2026-09-07)
Campagna completata (6 run, 2000 passi, 3 semi). Confronto ON vs OFF a **N appaiato** (N=2000/2500/3000;
la catena fredda cresce piano, N max ~3000-4300, NON ~18-20k delle campagne calde).
- **`m0_spin_axis_R` (allineamento spinori nucleo): NEGATIVO.** ON-OFF ~ -0.001/+0.004/-0.028; per-seme @N=3000
  ON<OFF su TUTTI e 3 (0.034/0.048, 0.046/0.111, 0.056/0.062). Valore assoluto ~0.04 = FRUSTRATO in ON e OFF.
  La sincronizzazione NON ordina i Bloch.
- **`m0_omega_axis_R` (assi orologi): accenno debole NON robusto.** ON>OFF (+0.03/+0.05) ma solo 2 semi su 3
  (seed 3 inverte).
- **`m0_spin_core_cv` (dispersione): rumoroso**, nessuna riduzione chiara.
- **VERDETTO (guardiano): al MINIMO FREDDO --sync-spinore NON scioglie la frustrazione.** Coerente con la
  SOGLIA di Kuramoto (accoppiamento < dispersione degli orologi rho*r). La macchina e' corretta (sigilli
  passati) ma NECESSARIA NON SUFFICIENTE. CAVEAT: regime meno maturo (N~3-4k); non escluso che a N maggiore
  o con un canale (STEP 2) cambi. Strumento: out_freetest/_analisi_sync.py.
- **PROSSIMO: STEP 2** = candidate una alla volta (--chi-core; poi --cs-dinamico [che porta --chi-core];
  poi --guscio-morbido), A/B, 3 semi, per vedere se una da' il CANALE che fa propagare la sync.

### §30 — DIAGNOSI del negativo + FIX proposto (design, 2026-09-07)
Domanda di Luca: "il nuovo spinore pare un fallimento? come mai?". Da guardiano: NON un fallimento della
MACCHINA (corretta, sigilli passati) ma un NEGATIVO informativo e DIAGNOSTICATO. Ipotesi (IN VERIFICA):
1. **Kuramoto sul grado di liberta' SBAGLIATO (causa principale, i dati la indicano).** La frustrazione vive
   nel SEGNO di doppia-copertura = FASE lungo l'asse dello spinore. L'orologio de Broglie ruota psi attorno
   al proprio asse (pura fase) a `omega_clk=(rho/rho_c)*r`: densita' diverse -> orologi a freq diverse ->
   i SEGNI si sfasano -> frustrazione. Ma `--sync-spinore` fa `omega_sync=forza*(nb x nb_media)` = torque
   TRASVERSO che allinea la DIREZIONE di Bloch, NON la fase-segno. DOF disaccoppiati. Firma nei dati:
   `omgR~0.2` (direzioni) > `spinR~0.1` (segno) -> ho sincronizzato le direzioni, non il segno.
2. **L'orologio CREA la dispersione** (omega_clk ∝ rho, rho varia enorme nucleo/guscio) -> auto-sabotaggio.
3. **Aggancio col limite continuo**: la dispersione e' in parte ARTEFATTO: rho = Ψ non normalizzata per deg
   (estensiva) e rho_c usa gF_med (mediana globale non-locale). De-parametrizzare/normalizzare -> dispersione
   cala -> sync potrebbe agganciare. Fallimento sync e limite continuo = stesso problema.
4. Forse stato genuinamente bilanciato (vortice-antivortice, m0_carica~0): allora spinR~0 e' fisica corretta.

**FIX PROPOSTO (design, non ancora implementato): `--sync-fase-orologio`** (flag separato, default off).
Kuramoto sulla FASE dell'orologio (segno di doppia-copertura), non sulla direzione:
- `theta_i = arg<canon(nb_i)|psi_i>` (fase lungo l'asse = doppia-copertura, come --chi-da-spinore);
- `omega_sync_clk_i = forza_i * (wI @ sin(theta) campo-medio) / uno` -> si SOMMA a `omega_clk` (lungo nb),
  NON al torque trasverso. `forza` = la stessa del Kuramoto-phi. ZERO parametri nuovi.
- ETC: theta da snapshot t-1, wI da step, in omega_clk prima della U, commit atomico.
**VINCOLO OPERATIVO**: NON editare soliton_simulator.py mentre gira la campagna chi-core (il .bat lancia un
python nuovo per ogni run -> on_s2+ girerebbero con codice diverso da on_s1 = contaminazione; e l'hash del db
cambia = ripresa rotta). Implementare DOPO la fine della campagna (o fermarla prima). ATTESA conferma design + timing.

### §31 — MODELLO BRANCH/COMMIT + versionamento DB + tracing su main (2026-09-07)
Richieste di Luca (cronologia): (a) "sospendi la campagna, occupati di spostare il check di scrittura DB
sull'hash della COMMIT"; (b) "usa un checkout chrooted alla versione giusta dell'hash per eseguire i test";
(c) "dubbio: meglio un branch per i test, chiave = coppia branch/commit; `main` stabile, `dev` sviluppo";
(d) "quello che c'è ora su `main` va tenuto STABILE; tutta la documentazione e il tracing restano su `main`,
unico punto di tracing per tutti i branch; crea il branch per i test in corso e fai referenziare quel branch
dalla doc".

**Verifica nel codice (non nei commenti).** Check attuale in `salva_stato`/`carica_stato` (soliton_simulator.py
~L1868/L1892): identità = `code_hash = sha256(bytes dell'INTERO file)[:16]`, rifiutato al ricarico se diverso.
Limite: qualunque edit (anche un commento) cambia l'hash → DB rifiutato; non mappa la storia git.

**Valutazione (guardiano).** La coppia branch/commit è metà giusta: il **commit** è l'identità sana, il **branch
NON** deve entrare nella chiave di rifiuto (stesso commit su `dev` o `main` = codice byte-identico = stessa fisica;
un merge `dev→main` non deve invalidare DB identici → sarebbe guardare il dito, non la luna). Buco scoperto:
working tree SPORCO (file modificato non committato) → il commit hash mente → serve guardiano del dirty. Il
"chroot" per i test = `git worktree` (versione immutabile a un commit, senza toccare main/dev).

**Design deciso (da implementare su `dev`):** identità di accettazione/rifiuto = git **blob hash** di
`soliton_simulator.py` (file-scoped, immutabile); metadati registrati = `commit`, `branch`, `blob`, `dirty`;
branch diverso → solo warning; working tree sporco → fallback su `sha256` + warning; DB legacy (solo `code_hash`)
gestiti in retro-compatibilità.

**Modello branch/tracing (canonico, vedi Checkpoint "MODELLO BRANCH E TRACING"):** `main` = codice stabile +
UNICO hub di documentazione/tracing per tutti i branch; `dev` = sviluppo/test in corso (solo codice); doc
aggiornata SOLO su `main`. Creato `dev` da `main` stabile (`5fbd53f`). Prossimo passo: implementare il
versionamento DB su `dev`, con backup datato del canonico prima di modificarlo.



---

## Sessione 2026-09-13 — FORK SU(2): dai documenti al cablaggio, e il teorema che lo ferma

> Agent: Claude Code (Opus 5). Branch di lavoro: **`fork-su2`** (creato oggi da `dev-spinoriale`).
> Blob `soliton_simulator.py`: `4fc7a794` (inizio) -> `b4c6c3f8` -> `cf24cd28` -> **`968fba34`** (fine).
> Tutti i commit pushati. Tutti i sigilli sono script committati in `csv/_seal_fork/`, exit 0/1.

### §32 — Allineamento delle istruzioni e dei documenti (commit 57010f5, e3c4447, 29b0ac5)
**L:** "rileggi le direttive da CLAUDE.md", poi "ho aggiornato le istruzioni rivedile".

**A — verifiche dal disco.** Blob confermato `4fc7a794`. Trovato che i **cinque documenti di
riferimento citati dal par.0-bis NON esistevano in nessun branch ne' nella storia git**: il par.0-bis
non era eseguibile. **L** li ha forniti; entrati nel repo in `doc/`: BUSSOLA, BUSSOLA_TECNICA v2,
ROADMAP_fork_SU2, PROTOCOLLO_test_olonomia, SYSTASIS.
Promosse in CLAUDE.md tre regole che vivevano solo in `.github/copilot-instructions.md` (retrocesso a
contesto storico): snapshot/restore completo incluso RNG per la purezza; `--cs-dinamico` implica
`--chi-core` e `--spinore-vivo`; mai confronti a passo fisso su sistema che si espande (aliasing).

### §33 — ERRORE DEL GUARDIANO, corretto dai due occhi (commit ddefcfd) — DIMOSTRATO
**A:** segnalato che CLAUDE.md par.9 indicava la forza di interferenza alla **riga 2196**, ma li' c'e'
il **DOCSTRING**: il codice eseguibile e' alle **righe 2207-2208**.
**L:** *"Claude Code ha ragione, e io avevo torto. E' l'errore ESATTO contro cui il §0 mette in guardia
('verifica dal codice, non dai commenti'), e l'ho commesso io scrivendo la bussola stessa. Non e' un
fallimento del sistema: e' il sistema che FUNZIONA."* Poi ha **riverificato tutto il §9 dal repo**:
sano tranne quella riga (cs 2187, `_phc`/`omega_clk`/`dt_n` non usano cs, `_passo_spinoriale` 2419
dietro SPINORE_VIVO, ancora elastica 3234-3237 + filtro 3224).
**Regola di coordinamento nata qui:** la CLAUDE.md **autorevole e' quella nel REPO**; le copie fuori
non vanno ripushate. Le modifiche le applica Claude Code, Luca fornisce il testo esatto.

### §34 — Ordine di lavoro: FORK-FIRST (commit a936d3c, abe9925, c9fcc1e)
**L** conferma **fork-first** e segnala di aver introdotto lui stesso un puntatore stale (la BUSSOLA
rimandava alla vecchia `ROADMAP_dev-spinoriale`, gamma-first). Allineati: STATO, ROADMAP radice
marcata **SUPERATA** (rimandata, NON ritrattata), BUSSOLA riga 86.
Promosse due regole in CLAUDE.md, testo dato da **L**: **par.2 sigillo 7** (niente conclusioni sotto
~2000 passi, mai un solo seme) e **par.4 LOCALE PURA** (mai sottrarre la media globale: introduce
non-localita' in un sistema relazionale). Sostituite le citazioni del vecchio `ISTRUZIONI_CLAUDE_CODE`
con `CLAUDE.md`: **un solo file autorevole per le regole dell'esecutore**, per non ricreare la
trappola dei due documenti che divergono in silenzio.

### §35 — Branch `fork-su2` (commit cebaee3)
**A** stava scrivendo il PEZZO 1 direttamente su `dev-spinoriale`. **L:** *"fermo, devi forkare un
altro branch"*. Stop in tempo: il `.py` non era stato toccato (blob verificato dopo lo stop: intatto).
Creato `fork-su2` da `dev-spinoriale`, che resta **BASELINE intatta**. File di stato rinominato
`STATO_CLAUDE_fork-su2.md`.

### §36 — PEZZO 1: connessione di Berry `_link_su2` (commit 8039e1f) — DIMOSTRATO, 17/17 PASS
`U_ij = exp(-i (chi/2) m_hat.sigma)`, ritorna `(U, w)`. Sigillo `csv/_seal_fork/_sigillo_pezzo1.py`.
Numeri: allineati -> U=I **esatto** (0.000e+00); unitarieta' 5.6e-16; **det U = 1** 4.5e-16 (e' SU(2),
non U(2): la fase U(1)/EM resta separata); `U_ji = U_ij^dag` **esatto**; trasporto
`|<psi_i|U_ij|psi_j>| = 1` entro 5.6e-16 su 20000 archi; **`|[U1,U2]| = 1.000e+00`** (non commutano).
**Fatto geometrico contro-intuitivo, verificato:** con `m_hat = (n_j x n_i)` la matrice trasporta
**n_j -> n_i**, che e' il verso giusto per `Im<psi_i|U_ij|psi_j>`. **L** ha rigirato il sigillo di
persona (17/17, exit 0) e verificato dal disco branch, blob e assenza di call-site.
**Presidio aggiunto da A:** S9 dice che lo **STRUMENTO** e' non-abeliano, **non il SISTEMA**.

### §37 — PEZZO 2 e il REPERTO sul peso (commit ca02af0) — NEGATIVO, poi risolto
Il peso era gia' dentro `_link_su2`; mancava il sigillo della **grandezza composta**
`w * Im<psi_i|U_ij|psi_j>`. 11/11 PASS, incluso **antisimmetria i<->j = azione-reazione** (5.6e-16).
**REPERTO:** il sigillo previsto *"allineati -> byte-identico allo scalare"* **non puo' passare** con
`w = sin(chi)`: a chi=0 il peso vale 0, ma lo scalare **non** e' zero se le fasi differiscono
(**max 9.954e-01**). Coincidono solo con spinori canonici dei Bloch, e nel codice non e' il caso:
`_nb_grav` prende i Bloch dal campo EMESSO `psi_spin`, `_coppia_interferenza` trasporta `_psi_spinor`.
**`sin(chi)` spegne il canale di fase (EM).**

### §38 — Diagnosi di L: `sin(chi)` SOVRA-CORREGGE (commit aa42518, 83d9203)
**L:** *"non e' un bivio 'perdere l'EM o tenerlo': e' un BUG del peso."* L'indeterminatezza dell'asse si
annulla a entrambi gli estremi ma e' **dannosa solo a chi=pi**: a chi=0 `sin(chi/2)=0` uccide gia' il
termine dell'asse (U=I qualunque sia m_hat) -> **innocua**; a chi=pi `sin(chi/2)=1` lo lascia vivo ->
**dannosa**. Quindi **il sigillo non era sbagliato: stava diagnosticando il peso.**
**L** ha riconosciuto falsa la propria riga in BUSSOLA TECNICA par.4.1 (*"allineati -> w=0, innocuo"*):
corretta nel doc, con la riga originale lasciata e la correzione sotto.
**L** ha respinto la strada *"accettare e riformulare il sigillo"*: corretta in se' (par.2.2) **ma non
va usata per coprire una perdita di fisica**.
**Errore di A, trovato e dichiarato da A prima di usarne i numeri:** la prima versione del test
sull'antipodale perturbava **l'angolo** e dava PASS a tutti, "nessun peso" incluso — non discriminava.
L'indeterminatezza e' sulla **direzione** dell'asse: test corretto = 360 direzioni azimutali, e solo
cosi' "nessun peso" fallisce (dispersione **1.62 costante** fino a eps=1e-6).

### §39 — DELIBERA: il peso e' `cos(chi/2)` (commit 3916e29, 4d7ca25) — DIMOSTRATO, 19/19 PASS
**A** scopre che il peso **non va scelto**: il trasporto parallelo **NON normalizzato**
`N = (1 + n_i.n_j) I + i (n_i x n_j).sigma` e' polinomiale nei Bloch e vale **esattamente
`2 cos(chi/2) U`** (2.7e-14 su 200000 archi). Il peso e' `|N|/2`: cio' che resta non normalizzando.
**L** verifica (4.6e-14) e aggiunge **la ragione che eleva la scelta da elegante a giusta**:
- **`cos(chi/2) = |<n_i|n_j>|` = OVERLAP QUANTISTICO dei due spin** (misurato 1.122e-14). Non e' un
  regolarizzatore ma un **ACCOPPIAMENTO FISICO**, e un accoppiamento e' **globale per natura**: cade
  cosi' la domanda sull'"ammorbidimento stretto", che era mal posta.
- **Contro `cos^2(chi/2)`: e' la PROBABILITA' di Born** (9.548e-15). La forza e' `Im<psi_i|N|psi_j>`,
  una **AMPIEZZA**: si pesa con un'ampiezza, non con una probabilita'. Conterebbe due volte.
**Tre presidi di L, sigillati:** (1) nella forza si usa **N/2**, che ad allineati vale I -> riduzione
allo scalare **4.441e-16** (con `sin(chi)`: 9.992e-01) — **reperto del §37 CHIUSO**; (2) **N nella
forza, `U = N/sqrt(det N)` nell'olonomia** — la fase dell'olonomia e' identica con N o U (9.149e-13),
il peso fattorizza come scalare positivo sul ciclo; (3) **l'algebra NON dimostra la correttezza
dinamica**: quella la dice un run.
**Rifattorizzazione:** `_link_su2_N` (primitiva della forza, polinomiale) + `_link_su2` riscritta su N.
**Spariscono arccos, asse normalizzato e il floor 1e-30** dalla forza; resta un solo caso degenere, nel
ramo dell'olonomia, dove e' genuino. **A dichiara** che 5 asserzioni dei sigilli PEZZO 1/2 sono state
riscritte perche' **codificavano la specifica vecchia, cioe' il bug** — non per farle passare.

### §40 — PEZZO 3: cablato, sigillato, **INERTE** (commit 6d66887) — NEGATIVO, DIMOSTRATO
Flag `--fork-su2` (OFF di default), `_mat2` per le due direzioni dell'arco (`_mat` metterebbe lo stesso
valore in M[i,j] e M[j,i]: rompe l'hermitianita'), e la sostituzione in `_coppia_interferenza`.
**Sigilli: 6 PASS, 2 FAIL.** PASS: flag OFF **byte-identico** (0.000e+00 su 32 array, due run veri
contro il commit fisso `4d7ca25`); riduzione al limite ad allineati (0.000e+00); azione-reazione su
entrambi i rami; norma |psi|=1 (2.220e-16 su 3209 nodi); nessun NaN/inf.
**FAIL (S2b, S6): con Bloch generici il ramo ON non differisce dallo scalare.**

**NON E' UN BUG: E' UN TEOREMA** (`csv/_seal_fork/_reperto_inerzia.py`, 1.570e-15 su 200000 coppie).
Se i Bloch sono quelli **degli stessi spinori trasportati**:
`(n_i.sigma)(n_j.sigma) = (n_i.n_j) I + i (n_i x n_j).sigma` => `N = I + (n_i.sigma)(n_j.sigma)`; ma
`|psi_i>` e' autovettore di `(n_i.sigma)` con autovalore +1, idem j => `<psi_i|N|psi_j> = 2<psi_i|psi_j>`.
**La connessione porta psi_j esattamente su psi_i: un overlap con se stesso non puo' cambiare.**
E' la forma **forte** del caveat gia' in `doc/ROADMAP_fork_SU2.md` (*"i link derivati dai soli Bloch
sono schiavi della materia"*): **non sono solo schiavi, sono INERTI.**
**Distinzione ferma:** riguarda la **FORZA**. L'**OLONOMIA** resta non banale (§36, S9). Ma un
diagnostico non e' dinamica: se la forza non cambia, il sistema non cambia.

### §41 — Il falso positivo evitato (commit 2d8cd5d) — PRESIDIO
Dai run a 150 passi si leggeva **N = 3164 (OFF) contro 3209 (ON), +1.4%**: sembra che il fork agisca.
**Non agisce.** Misure rifatte pulite: a **2 passi** il ramo ON viene **eseguito 305 volte** (spia su
stderr, su copia strumentata); a **3 passi** i due `.pkl` sono **byte-identici**; a **40 passi**
**max|OFF-ON| = 2.220e-16** con N identico (1889 = 1889). Il ramo gira, ma per il teorema da' lo stesso
risultato: cambia solo il **percorso di calcolo** (4 matvec invece di 2) e quindi l'ultimo bit. Il
sistema e' caotico e quel rumore a 1e-16 si amplifica fino a cambiare le mitosi. **La differenza di N
e' rumore amplificato, non fisica.**
**PRESIDIO:** misurare la divergenza a **orizzonte CORTO**. Se a 40 passi vale 1e-16, dentro non c'e'
fisica, qualunque cosa si veda dopo.
**Secondo bug di A, trovato e corretto:** `_sigillo_pezzo3.py` estraeva il codice di confronto da
**`HEAD`**. Appena il cablaggio e' stato committato, HEAD ha smesso di essere il pre-cablaggio: il
sigillo avrebbe confrontato il nuovo codice **con se stesso** e sarebbe passato sempre. Ora punta al
commit fisso `4d7ca25`. **Un sigillo ancorato a HEAD si auto-assolve.**

### §42 — DECISIONE APERTA (a L, non all'agent) — da CHE COSA si costruisce la connessione?
**Controprova misurata:** con Bloch presi da un campo **diverso** dagli spinori trasportati il trasporto
agisce eccome (**9.940e-01**). E i due oggetti **esistono gia' distinti** nel codice (`psi_spin` emesso
vs `_psi_spinor` primario). **Ma sceglierlo perche' fa muovere il risultato sarebbe tarare un
meccanismo per ottenere un effetto: l'opposto del par.3.**
Tre strade, nessuna deliberata:
1. **Dal campo emesso `psi_spin`** — da giustificare fisicamente; se la risposta e' *"perche' cosi'
   funziona"*, e' la strada sbagliata.
2. **Dallo STRATO 1** (ipotesi che l'agent considera la piu' seria, e non e' un rattoppo): con la
   memoria del link (`dU/dt = (U^Berry - U)/tau`) U **non e' piu' istantaneamente** la connessione
   degli stati correnti -> **il teorema di inerzia si rompe da solo, per costruzione**. Sarebbe
   coerente con il piano gia' scritto: forse **lo Strato 0 e' inerte BY DESIGN** e il fork inizia a
   vivere solo allo Strato 1.
3. Accettare che lo Strato 0 sia solo infrastruttura diagnostica (olonomia), non dinamica.
**L:** *"ci penso e ti dico domani."* Fino ad allora: **flag OFF, ramo inerte, gate NON ri-timbrato**
(con il fork inerte nessun run cambia davvero), **`dev-spinoriale` intatto** (blob `4fc7a794`).

### §43 — Presidio ancora aperto sul peso — IN VERIFICA
`cos(chi/2)` chiude i problemi **numerico**, **EM** e **antipodale**. **NON** e' dimostrata la sua
correttezza **DINAMICA**: sotto-pesa gli archi a chi grande (0.707 a 90 gradi, 0.500 a 120). C'e' un
argomento buono che sia giusto (`N|psi_j>` e' la proiezione naturale, spin disallineati interferiscono
meno) **ma e' un argomento, non una misura**. Olonomia W(r), stabilita' e comportamento EM: li dice un
run. **Elegante non significa dinamicamente corretto.** Oggi il punto e' accademico, perche' il ramo e'
inerte.
