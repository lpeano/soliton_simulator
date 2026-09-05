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

---

## Stato corrente (per la ripresa)
- **[FASE 2A FATTA, da committare]**: flag `--diag-lente-ogni N` (default 1 = identico) throttla solo
  `chi_core` (lenta/costante, 94 ms a scala); VELOCI a ogni passo. Verificato densità colonne + compile.
  NIENTE riuso byte-identico (mitosi cambia N — §20), NIENTE throttle delle veloci, NIENTE async.
- **Codice committato**: cs-locale integrale, spin_core, diagnostica inerzia guscio (`48310e0`/`a5bf7de`);
  profiling Fase 1 (`c98a9ca`).
- **Codice al baseline corretto**: nessun throttle (l'edit `--diag-ogni`/`_diag_leggera` aliasava le veloci ed
  è stato annullato). Tutto a ogni passo = niente aliasing. py_compile OK.
- **NON ancora scritto**: diffusione `--guscio-morbido` (Fase 1) — in attesa dei test-gratis.
- **Decisioni aperte (Luca decide):**
  1. Profilare quale sub-blocco domina gli ~0.8 s/passo, poi throttlare SOLO quel blocco lento-pesante
     (gating `if diag_full:` in `_diag_completa`) tenendo le veloci ogni passo — oppure lasciare tutto
     ogni passo (corretto ma lento).
  2. Isolare la causa dell'instabilità del PRIMO passo a `--tauloc` alto (sospetto CFL `nsub`) per far
     girare i test tauloc come nella prima proposta (sep 4, tauloc 1/5/10).
  3. (b) ELAST_C 100 vs 0 su core MATURO/denso (a 60 passi ELAST_C è dormiente → inconcluso).
- **Governance**: ogni modifica dietro flag default-off; 2000 passi + 2-3 semi per concludere;
  verificare nel codice non nei commenti; misura prima, modifica dopo; il campionamento è fisica (no aliasing).
