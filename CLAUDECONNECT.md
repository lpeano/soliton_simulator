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

### §32 — IMPLEMENTAZIONE infra (check DB + layout output) + branch `dev-<nome>` (2026-09-07)
Sessione di realizzazione. Richieste di Luca: (a) implementare il nuovo check DB e "spostare i log/db/csv nei
posti giusti in TUTTI i sorgenti"; (b) prima layout flat, poi correzione "il layout non può essere flat" →
sottocartella per campagna; (c) "un unico `dev` è limitante sui paralleli: serve `dev-<nome-sviluppo>`";
(d) rendicontare e tracciare PER CLAUDE la nuova filosofia.

**FATTO e verificato (nel codice, non nei commenti):**
- **Motore** `soliton_simulator.py`: nuovo `_versione_codice()` + `salva_stato`/`carica_stato`. Identità
  accetta/rifiuta = **git blob hash** dei byte del file (`git hash-object`), stabile e file-scoped; metadati
  `commit`/`branch`/`dirty`; fallback `sha256` (no-git o DB legacy). **Test passati**: ripresa ACCETTA (stesso
  blob) con avviso dirty; blob taroccato RIFIUTATO; DB legacy (solo `code_hash`) accettato per contenuto identico;
  auto-mkdir crea `db/`/`csv/`. Il branch NON entra nella chiave (stesso commit su branch diversi = stessa fisica).
- **Layout output**: migrati i file esistenti in `db/<campagna>/`, `csv/<campagna>/`, `log/<campagna>/` (nomi
  originali). Riscritti ~52 `.bat` + 2 `.bash` al nuovo layout (bulk + verifica campione + 2 mancati sistemati a
  mano: step2cs/step2cssc). `.gitignore` riscritto (traccia `csv/**` e `log/**`, MAI i `.pkl` in `db/`).
  `analisi_covariante.py`: esempio d'uso aggiornato; gli altri `.py` prendono i percorsi come argomenti. Video
  (`.mp4`, `out_video/`) fuori scope. Compila.
- **Branch**: adottata la convenzione **`dev-<nome-sviluppo>`** (paralleli), niente più `dev` unico. Creato
  `dev-infra` (commit `aa94b29`, l'infra sopra); `dev-dof` diramato da `dev-infra` (eredita l'infra); eliminati
  `dev` e `test/dof-fase-orologio`. Doc/tracing (questa voce, `CLAUDE.md`, `Checkpoint.md`, memoria) su `main`.

**Per Claude — la nuova filosofia in due righe:** (1) l'identità del DB è il **git blob** del codice (non lo
sha256 grezzo, non il branch): un merge o un cambio-branch a codice identico NON invalida i DB; per riprendere
una campagna vecchia usa `git worktree` sul commit del DB. (2) Output SEMPRE in `db/<campagna>/`,
`csv/<campagna>/`, `log/<campagna>/`; il motore crea db/csv, lo script crea `log\<campagna>`. (3) Sviluppo su
`dev-<nome>` paralleli; la doc vive solo su `main`.

**Prossimo passo (su `dev-dof`)**: implementare `--sync-fase-orologio` e la de-parametrizzazione (ordine §30:
prima de-parametrizzare = radice della dispersione, poi il Kuramoto sul segno).

### §33 — DE-PARAM OROLOGIO su dev-dof: analisi, test-GRATIS, impl, SIGILLI (2026-09-07)
Sessione su `dev-dof`. Sequenza decisa da Luca: **prima la convergenza (de-parametrizzazione), poi l'aggancio**
("i test dell'aggancio dopo aver fixato la CONVERGENZA"). Correzione chiave di Luca: **"la normalizzazione non per
volume ma RELAZIONALE sulla rete"** (i due principi ferrei: coerenza d'arco, non ampiezza÷volume).

**Analisi coupling (in banca, DIMOSTRATA — codice+dati).** `--sync-spinore` fa torque TRASVERSO `forza*(nb×nb_media)`
→ allinea la DIREZIONE di Bloch, non il SEGNO/fase (l'orologio `omega_clk` lungo nb). DOF disaccoppiati.
Dati (ultimo terzo): `m0_spin_axis_R`(segno)≈0.068-0.072 IDENTICO ON/OFF (sync NON tocca il segno);
`m0_omega_axis_R`(direzioni)≈0.19-0.24. `--sync-fase-orologio` (design §30) resta in banca per DOPO.

**Test-GRATIS convergenza (il cancello, PASSATO).** Su stato reale (n=1990, deg 2→379): `omega_clk=(|Ψ|²/rho_c_glob)·r`
correla con la connettività a **corr(deg)=+0.948, corr(Σw)=+0.975** → **~95% artefatto di connettività, non fisica**.
La coerenza d'arco RELAZIONALE `Σⱼwᵢⱼcos(φᵢ−φⱼ)/Σⱼwᵢⱼ` ha **corr(deg)=−0.10 ≈ 0** → intensiva, indipendente dal grado.
La volume-normalizzata `|F/Σw|²` (mia prima proposta) RIGETTATA da Luca ("è il dito"). Cancello: artefatto dominante → de-param giustificata.

**Implementazione (flag `--deparam-orologio`, default off, richiede --spinore-corretto).** `omega_clk` diventa la
coerenza d'arco intensiva (tetto naturale 1, nessun rho_c globale, nessun volume). Solo l'input dell'orologio;
`calcola_psi` (Ψ-sorgente) INTATTA. Commit WIP `2e39ea0`.

**SIGILLI — reperto CRITICO (NEGATIVO parziale, onesto).**
- **OFF byte-identico: PASSATO** (`max|A−B|=0` su tutti gli attrs vs pre-edit). ✓
- **Gravità invariata: FALLITO.** ON vs OFF: N **1990→1821**. Causa trovata nel codice (riga ~2933):
  **la gravità è SPIN-MODULATA by design** — `grav *= prod_interno` con `prod_interno=Σ_nb[ii]·_nb[jj]`, e
  `grav→spinta→d0`. Quindi orologio→spinore→`_nb`→`prod_interno`→gravità→mitosi→N. **L'orologio NON è
  disaccoppiato dalla gravità.** Secondo reperto: `omega_clk` NON è "pura fase" come dice il commento —
  `omega_tot=omega_new+omega_clk·nb` con `omega_new≠0` inclina l'asse di rotazione → cambia `_nb` (vale già in OFF).
- **Conseguenza:** il sigillo "gravità byte-identica" atteso da Luca è **impossibile per costruzione** (gravità
  spin-modulata). La de-param è un cambiamento fisico GLOBALE, non isolato. Ψ-sorgente intatta ma dinamica accoppiata.

**DECISIONE PENDENTE (Luca: "poi vediamo").** Tre strade: (1) accettare che è cambiamento fisico reale e valutare
per OSSERVABILI su campagna 2000 passi/3 semi (dispersione orologio/segno ↓? convergenza ↑? il calo N −8.5% a 600
passi è formazione o destabilizzazione?); (2) rendere l'orologio DAVVERO pura-fase (separare `omega_clk·nb` da
`omega_new` così che NON inclini `_nb`), poi la de-param diventa isolabile e il sigillo gravità torna possibile;
(3) ripensare (attaccare la connettività estensiva a monte, non l'orologio a valle). Consiglio guardiano: la (2)
prima — l'orologio che inclina `_nb` è un difetto a sé, indipendente dalla de-param.

### §34 — OROLOGIO PURA-FASE: la cura convergente (2026-09-07)
Luca sceglie l'opzione (2): **orologio PURA-FASE**. Motivo (converge tutto): la fase globale ruota il SEGNO
(doppia-copertura) attorno a nb ma lascia nb INVARIANTE; la gravità è modulata dalla DIREZIONE (`grav*=nb·nb`),
non dalla fase → pura-fase (a) decoupla dalla gravità (chirurgico) e (b) attacca il DOF giusto (il segno, §30).

**Implementazione (WIP `5c53717`).** Sotto `--deparam-orologio`: `omega_clk` (coerenza d'arco relazionale) NON
entra più nell'asse di rotazione (`omega_tot = omega_new [+omega_sync]`), ma è applicato DOPO come fase globale
`a1,b1 *= e^{-i·omega_clk·dt/2}`. OFF invariato.

**SIGILLI — PASSATI (verificati, 600 passi seed 1).**
- **OFF byte-identico**: `max|A−B|=0.000e+00` vs pre-edit. ✓
- **Chirurgico (prova decisiva)**: fase globale ARBITRARIA su `_psi_spinor` → `max|nb−nb'| = 6.7e-16` (≈0 macchina):
  una fase globale lascia `nb=ψ†σψ` INVARIANTE → l'orologio pura-fase **non può** toccare la gravità. `nb_new`
  dipende ORA solo da `omega_new` (memoria hebbiana), non dall'orologio.
- **N**: pura-fase **2014** vs legacy **1990** (**+1.2%**), contro il **−8.5%** (1821) della versione non-pura-fase.
  Il residuo +1.2% NON è l'orologio che tocca la gravità (provato 6.7e-16) ma la RIMOZIONE del tilt-legacy (il bug:
  l'orologio che inclinava nb): 2014 = gravità "pulita", 1990 = buggata.
- **Effetto sul segno**: `_psi_spinor` cambia (l'orologio pilota il segno). ✓

**Stato**: de-param orologio RELAZIONALE + PURA-FASE completa e sigillata su `dev-dof`. Radice della dispersione
(95% connettività) rimossa in modo chirurgico. **PROSSIMO**: campagna 2000 passi/3 semi per misurare se la
coerenza del SEGNO migliora (dispersione orologio ↓), poi — con la dispersione ridotta — ri-testare il sync
(`--sync-fase-orologio`, in banca §30) sul DOF giusto. Metodo consolidato in `copilot-instructions.md`
("Metodo di lavoro standard": cancello test-GRATIS + relazionale-non-volume + sigilli mirati + riporta i negativi).

### §35 — CERTIFICAZIONE NUMERICA + due bug pre-esistenti stanati (2026-09-07) — HANDOFF PER ANALISI
Test di convergenza-dt (Luca: "dimostra che l'epsilon non si amplifica, non eliminarlo") sulla de-param pura-fase.
Il test ha stanato **tre reperti prima del "va"**, tutti tracciati qui.

**REPERTO A — falso sigillo.** Il primo confronto `max|A−B|=0` era FUORVIANTE: era 0 solo perché saltava gli array
a forma diversa (N diverso). Corretto: si confronta N *e* i valori.

**REPERTO B — contaminazione PRE-ESISTENTE della condensazione (bug, ora sanato, commit `946b464`).** Il blocco
condensazione (a `--ogni`) chiamava `net.calcola_psi()` che muta `self.psi` SENZA snapshot/restore. Catena:
`--ogni` → `calcola_psi` muta `self.psi` → `ritmo()` del passo dopo legge quella (`a=angle(psi)−angle(_psi_prec)`)
→ tempo proprio diverso → fisica diversa. **Stesso pattern ritmo/_psi_prec già sanato nel diaglog, ricomparso in
un path dimenticato.** FIX: snapshot/restore delle 8 cache attorno a `calcola_psi` (come il diaglog). SIGILLO:
`--ogni 50` == `--ogni 600` con `max|A−B|=0` → `--ogni` ora byte-identico neutro. **La contaminazione era
SIGNIFICATIVA: N pulito 2433 vs contaminato 2014 (+21%, amplificata dal caos).** Conseguenza retroattiva: **le
campagne passate con `--ogni < passi` hanno il tempo proprio contaminato** — da rivalutare.

**REPERTO C — il mio test era confuso.** I due run di convergenza avevano `--ogni` diverso (50 vs 100) → A vs B era
confuso da `--ogni`, non solo da dt. Demolito e rifatto pulito.

**Sigilli verificati (fondamenta pulite):**
- **Diaglog PULITO**: con vs senza diaglog (stesso `--ogni 600`) → `max|A−B|=0` (X==Y=2014). Le osservabili
  covarianti sono letture pure (`getattr(net,'omega_s')`, ecc.) — scagionate.
- **Pura-fase chirurgica** (§34): fase globale lascia `nb` invariante a 6.7e-16 → non tocca la gravità.
- **OFF byte-identico** (§33/§34): `--deparam-orologio` off = codice pre-esistente.

**CONVERGENZA-dt PULITA (dt=0.01 vs dt/2=0.005, media 2ª metà t∈[3,6], condensazione sanata):**
- `m0_spin_axis_R` (il SEGNO/DOF, ciò che conta per la de-param): **0.0485 vs 0.0485 = 0% CONVERGE** → fisica, dt-stabile.
- `spin_axis_R`: 0.038/0.037 (4%, near-zero) ✓.
- `m0_omega_axis_R`: 0.034/0.025 (28% ma **near-zero**). NB: la pulizia ha SMASCHERATO che il "40% sistematico"
  di prima (0.184/0.305) era **contaminazione da `--ogni`**, non fisica.
- `m0_spin_core_cv` (la DISPERSIONE, bersaglio de-param): **1.380 vs 1.648 = 16%, NON converge pulito.** APERTO:
  siamo in FORMAZIONE (600 passi < 2000); da certificare con run lungo. È l'unico residuo per il "va" pieno.

**DOVE STANNO I FILE (per l'analisi):**
- **Codice** (branch `dev-dof`): de-param relazionale + pura-fase = commit `5c53717`; flag `--dt` + FIX condensazione
  sola-lettura = commit `946b464`. Motore `soliton_simulator.py`: clock in `_passo_spinoriale` (~riga 1705-1785,
  ramo `DEPARAM_OROLOGIO`); fix condensazione nel loop batch (~riga 5484, `_snap_cond`); gravità spin-modulata
  ~riga 2933 (`grav *= _nb·_nb`).
- **Dati** (branch `dev-dof`, commit `6763f81`): `csv/deparam_probe/` (diaglog) e `log/deparam_probe/`. Chiave:
  `clean_dt1.csv` (dt=0.01) e `clean_dt2.csv` (dt=0.005) = convergenza PULITA; `diagseal_*` = sigillo diaglog;
  `fix_o50/o600` = sigillo condensazione. I `.pkl` (DB di stato, 146MB) sono esclusi (gitignore) ma **rigenerabili
  deterministicamente** (seed 1) coi comandi nei log.
- **Comando per rigenerare** un probe: `python soliton_simulator.py --batch --nmasse 2 --sep 6 --seed 1
  --spinore-vivo --spinore-corretto --sync --deparam-orologio --dt <DT> --passi <P> --ogni <P> --diaglog <out.csv>`.

**ANALISI CHIESTA A CLAUDE:** (1) confermare/criticare la lettura della convergenza pulita (segno converge 0% =
fisica; `m0_spin_core_cv` 16% = formazione o dt-sensibilità reale?); (2) valutare se serve il run lungo (2000
passi) per certificare `m0_spin_core_cv` prima del "va"; (3) verdetto su come la contaminazione retroattiva (`--ogni`)
possa aver sporcato le campagne passate; (4) prossimo: con fondamenta pulite, ri-test del sync sul segno (la
de-param riduce la dispersione → il sync ordina la chiralità?).

### §36 — ANALISI di Claude (guardiano) + CORREZIONE onesta di §35 (2026-09-07)
Claude ha verificato la convergenza pulita e **corretto §35 su un punto** (l'etichetta "formazione" era ottimista).
Copilot ha RI-VERIFICATO i numeri e conferma la correzione. Test dell'etichetta formazione: se è formazione,
l'ultimo quarto deve convergere MEGLIO della 2ª metà.

| osservabile | diff 2ª metà | diff ultimo ¼ | verdetto |
|---|---|---|---|
| `m0_spin_axis_R` (il SEGNO) | 0% | 4% | **CONVERGE (~0-4%) → CERTIFICATO fisica** ✓ |
| `spin_axis_R` | 4% | 16% | near-zero (rumore, % gonfiato dal valore piccolo) |
| `m0_spin_core_cv` (dispersione) | 16% | 15% | **NON migliora → "formazione" NON dimostrata → NON certificato** |
| `m0_omega_axis_R` | 28% | 19% | migliora poco ma resta 19% (valori near-zero 0.034/0.025) |

**VERDETTO (onesto, corregge §35):**
- **"va" PARZIALE.** Certificato SOLO sul **segno** (`m0_spin_axis_R` converge → dt-indipendente → fisica). È
  l'osservabile che conta per la chiralità/frustrazione → **il ri-test del sync su di esso è affidabile.**
- **`m0_spin_core_cv` (16%) e `m0_omega_axis_R` (28%) NON convergono, e l'ultimo quarto NON migliora** → l'etichetta
  "formazione" di §35 è NON verificata. NON spacciarli per convergenti. Serve un **run lungo (t≥20, ~2000+ passi)**
  per distinguere formazione (transiente) da dt-dipendenza genuina. APERTO.
- La pulizia aveva già smascherato che il "40%" su `m0_omega_axis_R` era contaminazione `--ogni` (ora near-zero).

**PROSSIMO (confermato da Claude):** procedere al **ri-test del sync sul segno certificato** (`m0_spin_axis_R`), SENZA
attendere di chiudere `spin_core_cv` (riguarda altre osservabili). Domanda che conta: la de-param riduce la
dispersione dell'orologio (−95% l'artefatto) → il sync ora ordina la chiralità (m0_spin_axis_R sale)? Quando c'è
tempo, il run lungo (t≥20) per chiudere l'etichetta formazione su `spin_core_cv`.

### §37 — CAMPAGNA B pronta (test-GRATIS del guardiano): la de-param SOLA ordina il segno? (2026-09-07)
Il guardiano raccomanda **B prima di A**: non un precursore ma IL test. Ragionamento: la frustrazione nasce dagli
orologi che si SFASANO (frequenze ρ·r disperse); la de-param riduce la dispersione del ~95% → orologi a frequenze
simili → **potrebbero non sfasarsi più → il segno resta coerente DA SOLO, senza sync esplicito**. Se è così, la
de-param sola risolve e `--sync-fase-orologio` (A) NON serve. B è gratis (zero codice) e decisivo.
- **Script**: `test_deparam_segno.bat` (dev-dof, commit `9c0d05a`, smoke OK). A/B `--deparam-orologio` ON vs OFF,
  minimo freddo (`--spinore-vivo --spinore-corretto --sync`), 2000 passi, 3 semi, sep 6, diaglog.
- **Misura**: `m0_spin_axis_R` (il segno, l'unica osservabile CERTIFICATA §36) COVARIANTE a N appaiato, su 3 semi,
  significatività oltre il rumore fra semi (NON il "+0.011" su 1 seme). `analisi_covariante.py m0_spin_axis_R on_sX.csv off_sX.csv`.
- **Verdetto atteso**: ON>OFF concorde 3 semi oltre rumore → la de-param sola ordina il segno (vicinissimi allo spin ½);
  nessun cambiamento → serve A (`--sync-fase-orologio`, §30). Ordine: B → A se serve → C (run lungo t≥20 per `spin_core_cv`) in parallelo.
- **Esecuzione**: sul hardware di Luca (~5h, 6 run 2000 passi con diaglog; impraticabile in-ambiente).

### §38 — STOP CAMPAGNA B: la campagna misurava l'OSSERVABILE SBAGLIATO (2026-09-07)
**Luca ferma tutto** (campagna B + video) e chiede: "come è possibile ~0.05 frustrato, cosa non va?". Il guardiano
verifica NEL CODICE (non a memoria) e trova NON un bug, ma una catena di **mismatch osservabile/meccanismo**. DIMOSTRATO.

**1. Il segno è CONDIZIONALMENTE dinamico (non cosmetico, non sempre fisico).** Esistono DUE canali reali che portano
il segno di doppia-copertura dello spinore nella FISICA, ENTRAMBI default-OFF e ASSENTI dai flag di B:
- `SPIN_FEEDBACK` (`--spin-feedback`, riga 2102): `coppia += _feedback_spinoriale_archi` = `Im⟨lift_i|lift_j⟩` =
  fase RELATIVA fra nodi → `coppia` → `delta_phivel` (riga 2169) → fisica. Canale vero. Nessun parametro (divide per grado pesato).
- `CHI_DA_SPINORE` (`--chi-da-spinore`, riga 2262): segno = `sign(Re⟨canon(nb)|_psi_spinor⟩)` → `perc_chi` →
  frame-drag/`VERSO_CHI` (riga 2121), kick vettoriale firmato (riga 271), `CHI_CORE` (riga 1618). Molto dinamico.
- Campagna B: `--spinore-vivo --spinore-corretto --sync --deparam-orologio` → **né spin-feedback né chi-da-spinore**
  → in B il segno è PURAMENTE DIAGNOSTICO (lo leggono solo le diagnostiche). Ordinarlo non muove nessuna forza.
- SOTTIGLIEZZA che risolve il dubbio "fase globale = cosmetica": l'orologio applica una fase **PER-NODO**
  (`omega_clk` è array) → cambia la fase RELATIVA fra nodi → è fisica *se* un canale la legge (SPIN_FEEDBACK la legge).
  Il segno NON è cosmetico in assoluto: è cosmetico SOLO coi fili staccati (come in B). Metafora: **motore acceso
  (spinore SU(2)), frizione staccata (no feedback), tachimetro sbagliato (direzione invece di segno).**

**2. `m0_spin_axis_R` è la DIREZIONE, non il segno (corregge §36).** `m0_spin_axis_R` = `|media versori nb|`
(righe 4756/4873) = allineamento delle DIREZIONI di Bloch. La de-param pura-fase lascia `nb` INVARIANTE (6.7e-16) →
`m0_spin_axis_R` è CIECO all'orologio per costruzione. §36 aveva certificato `m0_spin_axis_R` come "il segno": ERRORE,
è la direzione (l'aspetto che il vecchio Bloch aveva già; il NUOVO spinore aggiunge il SEGNO, non la direzione).

**3. Anche la BERRY è cieca al segno (corregge la prima cura del guardiano).** `berry_spin_media` /
`berry_spin_media_assoluta` (righe 1256-1275) NON leggono `_psi_spinor`: ricostruiscono gli spinori DA `nb`
(`th=arccos(nb_z), ph=arctan2(nb_y,nb_x)`) e fanno l'invariante di BARGMANN (prodotto ciclico), gauge-invariante per
costruzione ("le fasi arbitrarie dei singoli spinori si cancellano"). Cieca al segno per DUE motivi (legge nb + Bargmann
cancella le fasi per-nodo). RITRATTATA la raccomandazione "misura la Berry".

**4. NON esiste una diagnostica del segno.** L'unica lettura di `Re⟨canon(nb)|_psi_spinor⟩` è dentro il ramo
`CHI_DA_SPINORE` (riga 2265, mutazione di perc_chi, non lettura). Va AGGIUNTA una diagnostica PURA:
`sign_k = sign(Re⟨canon(nb_k)|ψ_k⟩)`, coerenza `|media(sign_k)|` ∈ [0,1] (→1 coerente, →0 frustrato). È l'osservabile giusto.

**Scelta del filo per il test decisivo (più netta della "profondità"): `--chi-da-spinore`.** Le tre quantità sono
DIVERSE: `Im⟨lift_i|lift_j⟩` (SPIN_FEEDBACK, fase relativa inter-nodo) ≠ `Re⟨canon|ψ⟩` (CHI_DA_SPINORE, segno per-nodo)
≠ Berry (fase geometrica di nb, cieca). L'osservabile-segno da aggiungere legge ESATTAMENTE ciò che CHI_DA_SPINORE
collega alla fisica → **osservabile = filo = stessa quantità** (coerenza di doppia-copertura). SPIN_FEEDBACK collegherebbe
una quantità diversa = ennesimo mismatch. Il loop segno→perc_chi→frame-drag→nb(asse)→ψ è l'accoppiamento dinamico
VOLUTO che il test deve sondare (il guard riga 4213 richiede `--spinore-corretto` per evitare solo il loop spurio diretto).

**PIANO B″ (deciso col guardiano Luca): il test che chiede la cosa giusta.** A parità di tutto
(`--spinore-vivo --spinore-corretto --sync --chi-da-spinore`, minimo freddo, 2000 passi, 3 semi), UNICA variabile
`--deparam-orologio` ON vs OFF (un flag = una variabile). Osservabili: (a) coerenza-segno nuova → la de-param ordina
il segno? (b) N + spin_axis_R → il segno ordinato CAMBIA la fisica? B″ è il primo test che risponde alla domanda VERA
(non a metà): può dare positivo o negativo, ma con osservabile giusto e frizione attaccata. Prima di lanciare: 2 edit
— (1) aggiungere la diagnostica pura di coerenza-segno (lettura pura, default invariato, test byte-identico);
(2) nessun nuovo flag (`--chi-da-spinore` esiste). NON ancora lanciato: si attende il go dopo il diff della diagnostica.


### §39 — Diagnostica SEGNO+VERSO aggiunta, B'' con spin-feedback (2026-09-07, WIP - PC spento)
GO del guardiano a B''. Distinzione chiave: DRIVER (cosa il filo legge) != ORDER PARAMETER (cosa misuriamo). Aggiunta diagnostica pure-read su dev-dof (commit 9542f2f, py_compile OK): segno_arco_coer=<sign(Re<canon|psi>)_i*_j> archi (foglio doppia-copertura, RISPONDE all'orologio a differenza di spin_axis_R/berry_* ciechi), verso_arco_coer=<nb_i.nb_j> archi, segno_ov_absmedia. Misura SEGNO e VERSO con lo stesso metodo -> si ordinano INSIEME (un motore) o separati (due)? Covariante per-arco, zero parametri.
FILO scelto con Luca = --spin-feedback (sua idea: 'segno dentro la memoria hebbiana'; gia' implementato come _feedback_spinoriale_archi = Im<psi_i|psi_j>->coppia, legge nuda zero param). IMPEGNO REGISTRATO: il filo spin-feedback tocca il verso INDIRETTAMENTE (->coppia->phi U(1)->hebbiano->nb) = debole. Se B'' ordina il SEGNO ma NON il VERSO -> NON dire 'abeliano': fare B''-bis con --chi-da-spinore (filo diretto via frame-drag/kick) PRIMA del verdetto. Due fili falliti = abeliano; un filo debole no.
RIPRESA (da fare): (1) sigillo diaglog-puro byte-identico; (2) run-lampo colonne !=0; (3) script B'' (--spinore-vivo --spinore-corretto --sync --spin-feedback, de-param ON/OFF unica variabile, 2000p/3semi). Dettagli in /memories/repo/deparam_orologio.md par.39.

### §40 — Nota in RISERVA: unificazione del motore (Dirac). NON implementare ora (2026-09-08, idea di Luca)
DIAGNOSI: lo spinore ha OGGI motori DIVERSI per i due DOF: VERSO (nb) <- omega_new (memoria hebbiana);
SEGNO <- omega_clk (orologio, coerenza di fase con de-param). Due sorgenti distinte -> verso e segno possono
ordinarsi separatamente = possibile radice della frustrazione. IDEA (Dirac): in un vero spinore SU(2) il motore
e' UNO SOLO (massa/energia): ruota l'INTERO spinore, verso e segno emergono INSIEME. LINEA ROSSA: deve emergere
da un PRINCIPIO, MAI da un termine che forza verso=segno. QUANDO: solo SE i pilota mostrano verso+segno scollegati.

### §41 — Pilota go/no-go spin-feedback: NO-GO (2026-09-08) [NEGATIVO]
Sigillo diaglog-puro §39 PASSATO (2 run 300p seed1 con/senza --diaglog: tutti gli array fisici max|A-B|=0, N=2011;
colonne §39 pure-read certificate). Pilota (800p, 1 seme, de-param ON vs OFF, filo --spin-feedback, media dal 25%):
segno_arco_coer ON+0.00006/OFF+0.00016, verso_arco_coer ON-0.00001/OFF+0.00104 -> ENTRAMBI DENTRO IL RUMORE
(sd~0.003). segno_ov_absmedia~0.67 (commitment locale al foglio) ma segno_arco_coer~0 (fogli non coerenti fra
archi) = frustrazione, identica ON/OFF. NON e' 'segno si', verso no'. NO-GO sulla campagna 5h. Cautele: 800p=formazione, 1 seme.

### §42 — Pilota chi-da-spinore: SECONDO FILO FALLITO (2026-09-08) [NEGATIVO]
Filo DIRETTO --chi-da-spinore (perc_chi=segno doppia-copertura -> frame-drag/chi-core). Stesso disegno §41.
segno_arco_coer ON+0.00008/OFF-0.00009 (dentro rumore sd~0.0035); verso_arco_coer ~0 entrambi; segno_ov~0.65.
Anche il filo diretto/forte NON ordina il segno. BILANCIO DUE FILI (spin-feedback indiretto + chi-da-spinore
diretto) falliti -> ipotesi 'due motori scollegati/abeliano' SALE. Motore-unico (§40) da RISERVA a candidata giustificata.

### §43 — Motore-unico = ARTEFATTO DI RETICOLO (2026-09-08) [DIMOSTRATO, negativo formale]
La 'carta finale' motore-unico NON e' genuina. ALGEBRA: nb=psi†sigma psi -> psi e' autostato +1 di nb·sigma ->
exp(-i/2 omega_clk dt nb·sigma)psi = FASE PURA (identica a _phc). Unire a omega_new differisce dallo split solo
per il commutatore BCH O(dt^2) -> NEL CONTINUO unito==split (il sigillo conv-dt lo rivelerebbe artefatto).
CORROBORAZIONE: il ramo OFF dei pilota E' gia' la struttura motore-unito; OFF≈ON su segno_arco_coer (§41/§42).
VIA GENUINA proposta: accoppiamento sui SEGNI dei vicini, O(dt^1), gravita'-safe = --sync-fase-orologio.

### §44 — Implementato --sync-fase-orologio + SIGILLI (2026-09-08) [macchina corretta]
Kuramoto sul SEGNO di doppia-copertura (via genuina §43). alpha_k=arg<canon(nb_k)|psi_k>; eta=dt*forza*sin(media-alpha);
psi->e^{i eta}psi (FASE GLOBALE -> nb invariante, agisce solo sul segno). Zero param (riusa forza/wI/uno). Flag default
OFF byte-identico. SIGILLI: (1) OFF byte-identico PASSATO; (3) unitarieta' PASSATO; (2) gravita'-safe (torque O(dt^2)
su nb); (5) sign O(dt^1) analitico. Sigillo (4) conv-dt sulle intensive nella campagna.

### §45 — Pilota sync-fase-orologio: NO-GO, TERZA via fallita (2026-09-08) [NEGATIVO]
Pilota 800p 1 seme ON vs OFF: segno_arco_coer ON+0.00005/OFF-0.00005 (dentro rumore); verso~0; segno_ov~0.66.
Il sync FA qualcosa (_psi_spinor cambia, sigilli) ma NON ordina relazionalmente (segno_arco_coer piatto ~0). BILANCIO
TRE VIE tutte ~0 ON=OFF: §41 spin-feedback, §42 chi-da-spinore, §44 sync-fase-orologio (la carta finale abeliana).
-> IPOTESI ABELIANA SALE FORTE. §45-bis: variante antiferromagnetica anche smentita.

### §46 — Implementato --kuramoto-su2 (via NON-ABELIANA) — l'ULTIMA carta (2026-09-08)
Kuramoto SU(2) NON-ABELIANO: ruota lo SPINORE INTERO verso la media SU(2) dei vicini, rotazione geodetica attorno
all'asse VARIABILE nb x nb_bar (non commuta -> non-abeliano genuino). Il torque allinea il VERSO (nb->nb_bar); il
SEGNO segue per OLONOMIA (fase geometrica), NON targettizzato (targettizzare=abeliano gia' fallito). nb SI muove
(gravita' fisica, voluto). O(dt^1), zero param. Flag --kuramoto-su2 default OFF. Colonna diaglog spin_overlap_arco
= <|<psi_i|psi_j>|^2> (coerenza SU(2) PIENA, pure-read). Se olonomia ordina -> spin 1/2; se no -> teorema di assenza.

### §46-bis — SIGILLI --kuramoto-su2 FATTI: 1+2 PASSATI, pilota in corso (2026-09-09)
Ripresa mattutina. OLD (pre-kuramoto) = ff2982e. 3 run 300p seed1 (pre=--spinore-vivo --spinore-corretto --sync
--deparam-orologio): OLD, NEW-off, NEW-on --kuramoto-su2. SIGILLO 1 (OFF byte-identico OLD vs NEW-off): max|A-B|=0
su 28 array (complessi confrontati col MODULO). PASSATO. SIGILLO 2 (unitarieta' NEW-on): |psi|=1 (3.3e-16), len==n=1856.
PASSATO. SIGILLO 3 (primo ordine) analitico O(dt^1); SIGILLO 4 (conv-dt) nella campagna covariante. PRELIM a 300p
(formazione, 1 seme, NON verdetto): spin_overlap_arco ON=0.5000 OFF=0.5000 (spinori scorrelati sugli archi),
segno_arco_coer ON-0.0006 (dentro rumore sd~0.003), verso~0, spin_axis_R 0.041 entrambi -> nessun accenno precoce.
Evidenza committata+pushata su dev-dof (6a3864a, csv/_seal_k2/_verifica.py). IN CORSO: pilota go/no-go 800p seed1
ON vs OFF (csv/deparam_pilota_k2/). Se accenna -> 3 semi/2000 + conv-dt covariante; se ~0 -> ABELIANO definitivo.

### §46-ter — Pilota --kuramoto-su2: NO-GO, la via non-abeliana fallisce (2026-09-09) [IN VERIFICA -> NEGATIVO]
Confronto covariante ON vs OFF a N APPAIATO (N 824->2231 x2.71, tau_cum~704; a passo fisso misureresti
l'espansione), terzo tardivo, finestra N comune [824,2231]: spin_overlap_arco (SU(2) PIENO, primario)
ON=0.50001 OFF=0.50002 = SCORRELATO in entrambi (0.5=scorrelato); segno_arco_coer ON-OFF=-0.00016 (~uguale);
verso_arco_coer ~0 ON=OFF; spin_axis_R ~uguale. UNICO stacco: segno_ov_absmedia ON=0.666 OFF=0.708 (ON<OFF
di 0.041 = direzione SBAGLIATA: il torque geodetico DISORDINA il foglio locale, non lo ordina). Accoppiamento
(corr temporale 2a meta' ON): corr(segno,verso)=+0.016~0 (NON un motore unico), corr(verso,overlap)=+1.000
(l'overlap SU(2) e' guidato SOLO dal verso; il segno non ci mette coerenza). OLONOMIA NON trasferisce coerenza
al segno = 'olonomia persa'. BILANCIO 4 VIE tutte piatte (segno_arco_coer~0, ON=OFF): §41 spin-feedback, §42
chi-da-spinore, §44 sync-fase-orologio (abeliano), §46 kuramoto-su2 (NON-ABELIANO genuino, l'ultima carta);
§43 motore-unico=artefatto O(dt^2). -> IPOTESI ABELIANA molto forte. CAUTELE: 800p=FORMAZIONE, 1 seme -> NON
verdetto. GATE a Luca: (A) conferma 3 semi/2000+conv-dt covariante -> se ~0 concorde = ABELIANO DEFINITIVO
(negativo che vale un positivo, chiusura formale); (B) diagnosi perche' nemmeno il non-abeliano ordina (torque
si dissolve in mitosi/espansione? o segno=gauge non-osservabile §38). MAI forzare verso=segno. Relazione:
RELAZIONE_CLAUDE_2026-09-09.md; dati csv/deparam_pilota_k2/ (dev-dof b729fe8), .pkl esclusi.

### §47 — [branch dev-dof] TRE FRENI A MANO + fix CHI_BASC + bracci A/V/B/C (2026-09-09) [DIMOSTRATO, negativo]
L'intuizione di Luca ("il test ha tutti gli agganci?") ha stanato un freno TRIPLO nel pilota kuramoto-su2:
(1) flag CHI_BASC/OLON_PART spenti; (2) CHI_BASC ROTTO (test-GRATIS: soglia=np.median(twn) GLOBALE invece di
PHI_CRIT/2pi come dice il commento -> IMPONEVA il 50/50 che doveva ROMPERE; median->50% +1 vs 2pi->0.9%; viola
"la media non va qui"); (3) OLON_PART inerte senza --viriale (annidato in if VIRIALE). FIX di legge (1 riga,
median->PHI_CRIT, backup datato): allineamento-alla-legge, NON trucco. Sigillo OFF byte-identico PASSATO
(max|A-B|=0). Run-lampo: --chi-basc ora perc_chi +1 all'1.3% (rompe il 50/50). BRACCI (800p seed1, N appaiato):
A=--chi-basc, V=--viriale(controllo), B=--viriale --olon-part (vs V), C=tutto. TUTTI NO-GO su ENTRAMBI gli assi:
spin_overlap_arco ~0.500 (scorrelato) ovunque; berry_spin_media FIRMATA ~0 ovunque (olonomia locale forte ~1.1
ASSOLUTA ma i SEGNI SI CANCELLANO). CHI_BASC per giunta SOFFOCA la crescita (N 1174/1017 vs 2231; masse ferme).
Il 372 costante nel CSV C = firma del congelamento (occhio di Luca); MA test decisivo: il sistema congelato C ha
spin_overlap 0.49976 IDENTICO ai non-congelati V/B -> il congelamento NON maschera (gli osservabili del segno
sono relazionali sugli archi, a N fisso). Ne' chiralita', ne' viriale, ne' olonomia locale ordinano il segno.
Soglia intermedia = parametro tarato = linea rossa (ritirata). Dati csv/deparam_bracci/ (dev-dof). Muro = quanto 2pi.

### §48 — [branch dev-dof] TRACING PER-PASSO: il segno DECADE, l'ordine e' un REPULSORE (2026-09-09) [reperto chiave]
Prima del bivio, tracing deterministico per CAPIRE il meccanismo. Flag --trace-segno (pure-read, SIGILLO OFF
byte-identico PASSATO max|A-B|=0). Snapshot (db_on.pkl) sembrava (d) "segno geometricamente random". MA il
tracing per-passo RIBALTA: il segno NASCE ORDINATO (segno_arco 0.996, semina fase=0) e DECADE a 0.000 in ~10
passi. Crollo PRE-nascite (nati=0 fino step7 -> coppie ESCLUSE, ipotesi (a) cade). torque COLLASSA (0.93->0.15).
CONFERMATO su 2 SEMI (seed1 e seed2 identici, seed2 decade piu' rapido). MECCANISMO: lo stato a segno ordinato e'
un REPULSORE, l'attrattore e' lo scorrelato. Feedback auto-distruttivo: segno si disordina -> media SU(2) vicini
si cancella -> torque cala -> non riallinea -> amplifica. Il sistema RELASSA ATTIVAMENTE VIA dall'ordine.
=> TEOREMA DI ASSENZA CON MECCANISMO: il core non e' abeliano per caso/limite di misura, ma perche' l'ordine del
segno e' un repulsore dinamico. Molto piu' forte di "misurato ~0". Dati trace_segno.csv/trace_segno_s2.csv (dev-dof).
BIVIO nominato con onesta': SCOPRIRE (l'attuale e' abeliano, ordine repulsore - certificato) vs COSTRUIRE.

### §49 — [branch dev-spinoriale] REFACTORING RIFONDATIVO: lo spinore emette il campo (2026-09-09)
Nuovo branch PARALLELO `dev-spinoriale` (da dev-dof). Visione di Luca (dai 12 anni): il solitone e' uno SPINORE
SU(2) che EMETTE il campo (la sfera-otto), non una fase scalare con lo spinore aggiunto. Inversione ontologica:
campo->spinore diventa SPINORE->campo. Il fondamentale diventa SU(2) (non-abeliano INCORPORATO, non innestato).
COLLEGAMENTO col §48: nell'attuale l'ordine del segno e' un REPULSORE (segno = grado aggiunto, niente lo
stabilizza); nel spinoriale la MATERIA stessa richiede accordo di segno (interferenza NON distruttiva, Legge II)
-> l'ordine diventerebbe un ATTRATTORE (la materia coerente esiste solo dove i segni concordano). NON e' un trucco:
la materia stabilizza l'ordine PER FISICA, non per termine imposto. Il fallimento dell'attuale (§48) e' la mappa
per il nuovo. Doc sotto doc/: FONDAZIONE_SPINORIALE.md (leggi I-X + geometria di contatto), REFACTORING_SPINORIALE.md
(piano tecnico, flag --campo-spinoriale, fasi+sigilli riduzione-al-limite), ONTOLOGIA_SPINORIALE.md. Solo fondazione,
NIENTE codice ancora. Progetto di settimane. REGOLA: d'ora in poi ogni relazione/commit dichiara il BRANCH.
