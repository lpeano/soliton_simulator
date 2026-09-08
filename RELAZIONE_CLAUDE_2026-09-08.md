# RELAZIONE per Claude — Sessione 2026-09-08 (branch `dev-dof`)

> Report di continuità per la prossima sessione. Argomento: la **carta finale sullo spin-½**
> (ordinamento del segno di doppia-copertura) e la scoperta che il **"motore-unico" così come
> proposto è un artefatto di reticolo**. Lingua: italiano. Etichette: DIMOSTRATO / IN VERIFICA /
> APERTO / NEGATIVO. Tracing di dettaglio anche in `/memories/repo/deparam_orologio.md` §39–§43.

---

## 0. TL;DR (leggi prima questo)

- **Due fili di accoppiamento segno→fisica FALLISCONO** entrambi (segno non si ordina): `--spin-feedback`
  (indiretto, §41) e `--chi-da-spinore` (diretto, §42). `segno_arco_coer ≈ 0`, ON ≈ OFF, dentro il rumore.
- La "carta finale" proposta era il **motore-unico** (unificare `ω_new` verso + `ω_clk` segno in una sola
  rotazione SU(2), à la Dirac). **Analisi algebrica: NON è genuino.** Con `nb = ψ†σψ`, la massa lungo `nb`
  è **fase pura**; unirla a `ω_new` dà solo un accoppiamento **O(dt²) = artefatto di reticolo** che svanisce
  nel continuo. **Motore-unito ≡ split nel continuo.** [DIMOSTRATO, algebra SU(2)]
- **Corroborazione nei dati:** il ramo OFF (legacy = `ω_new + ω_clk·nb`) È già la struttura "motore-unito"
  e dà `segno_arco_coer` identico allo split (ON). I pilota **hanno già misurato** unito vs split → nessuna
  differenza. [DIMOSTRATO nei dati]
- **Conseguenza:** il motore-unico non è la carta finale genuina. La via genuina all'ordinamento del segno
  (quantità RELAZIONALE d'arco) è un **accoppiamento relazionale sui SEGNI dei vicini**, gravità-safe e primo
  ordine in dt = **`--sync-fase-orologio`** (§30/§31). **Decisione a Luca (gate aperto).**

---

## 1. Da dove si partiva (stato all'inizio sessione)

- Branch `dev-dof`, HEAD era `9542f2f`: aggiunte le **3 colonne diagnostiche §39** in
  `soliton_simulator.py` (~riga 4771), pure-read: `segno_arco_coer = ⟨sign_i·sign_j⟩` (ORDER PARAMETER del
  SEGNO), `verso_arco_coer = ⟨nb_i·nb_j⟩` (il VERSO), `segno_ov_absmedia = |Re⟨canon|ψ⟩|` medio.
- Campagna B″ preparata ma **non lanciata**; mancavano 2 sigilli + il pilota go/no-go.

## 2. Sigilli PASSATI (prima di ogni campagna) [DIMOSTRATO]

1. **Diaglog-puro byte-identico:** 2 run (300 passi, seed 1, `--spinore-vivo --spinore-corretto --sync
   --deparam-orologio --spin-feedback`), uno con `--diaglog` e uno senza. TUTTI gli array fisici
   `max|A−B| = 0` (phi, _nb, psi, d, _psi_spinor, perc_chi, pos, omega_s, phi_s, _psi_prec, _nb_prec,
   _spinor_lift), N = 2011 identico. Le colonne §39 sono PURE-READ certificate. Le chiavi presenti solo
   nel run-diaglog (`_ang_prec_*`, `_nhat_prec`, `_shat_prec`, `_ang_orb`) sono cache diagnostiche di
   precessione: il sigillo prova che NON toccano la fisica.
2. **Run-lampo:** colonne §39 finite/non-nulle/in range; `|ψ_spinor| = 1` (max|1−|.|| = 3.3e-16), len == n.

## 3. La catena spinoriale, verificata nel codice (per contesto)

**INGRESSI (3 motori che ruotano lo spinore):**
- `ω_new` (~L1668) → VERSO: memoria hebbiana `ω_src + dt·(cross(B,nb)/inerzia − ω_src/τ)`. Può inclinare nb.
- `ω_clk` (L1723 de-param / L1728 legacy) → SEGNO: de-param = coerenza d'arco intensiva·ritmo; legacy =
  (ρ/ρ_c)·ritmo. Applicato (de-param) come fase globale `_phc` (L1751), oppure (legacy) lungo nb (L1729).
- `ω_sync` (L1688) → DIREZIONE: Kuramoto SU(2) `forza·(nb×nb_media)`, solo con `--sync-spinore`.
- (+ asse tw-spinore: blocco `TW_SPINORE` L1665, asse `cl=χ_i·χ_j` σ_x/σ_z, angolo tw/2 — NON `twist_dip`).

**USCITE (cosa lo spinore pilota):**
- → GRAVITÀ (L2940): `grav *= (Σ nb_i·nb_j)·sign(dpozzo)`. L'allineamento di spin modula la gravità.
  Il sigillo "6.7e-16" prova che l'orologio pura-fase lascia nb invariante → NON tocca la gravità (disaccoppiamento).
- → MATERIA/FASE (L987→L2103): `--spin-feedback`, `Im⟨lift_i|lift_j⟩ → coppia → delta_phivel → φ`.
- → CHIRALITÀ (L2265): `--chi-da-spinore`, `perc_chi = sign(Re⟨canon|ψ⟩) → frame-drag/kick/chi-core`.

## 4. I due pilota go/no-go (800 passi, 1 seme, de-param ON vs OFF, media dal 25%+)

### §41 — filo `--spin-feedback` (indiretto)
| osservabile | ON | OFF | ON−OFF | sd |
|---|---|---|---|---|
| segno_arco_coer | +0.00006 | +0.00016 | −0.00010 | ~0.003 |
| verso_arco_coer | −0.00001 | +0.00104 | −0.00106 | ~0.002 |
| segno_ov_absmedia | 0.670 | 0.675 | −0.005 | ~0.025 |
| spin_axis_R | 0.039 | 0.044 | −0.006 | ~0.017 |

**NO-GO.** Nessun accenno; de-param non alza il segno sopra OFF. → 5h risparmiate. Dati: `csv/deparam_pilota/`.

### §42 — filo `--chi-da-spinore` (diretto, frame-drag)
| osservabile | ON | OFF | ON−OFF | sd |
|---|---|---|---|---|
| segno_arco_coer | +0.00008 | −0.00009 | +0.00017 | ~0.0035 |
| verso_arco_coer | +0.00031 | +0.00034 | −0.00003 | ~0.0021 |
| segno_ov_absmedia | 0.651 | 0.650 | +0.0005 | ~0.006 |
| spin_axis_R | 0.035 | 0.036 | −0.001 | ~0.015 |

**Anche il filo diretto FALLISCE.** Segno piatto a ~0 (non "piccolo positivo"), ON≈OFF. Dati: `csv/deparam_pilota_chi/`.
Nota (da Luca): i due fili falliscono **anche a N=32000 maturo** → non è solo formazione, l'accoppiamento-via-filo è esaurito.

**Firma comune:** `segno_ov_absmedia ≈ 0.65–0.67` (ogni nodo SCEGLIE un foglio) ma `segno_arco_coer ≈ 0`
(i fogli NON sono coerenti fra archi) = frustrazione relazionale, identica ON/OFF.

## 5. La carta finale "motore-unico" — DESIGN e perché NON è genuino

**Proposta:** con `--motore-unico`, una sola rotazione `U = exp(−i/2 ω_tot·σ dt)`,
`ω_tot = ω_inerzia (hebbiano) + ω_massa (ω_clk·nb, lungo nb per salvare la gravità)`, togliendo la fase
globale `_phc`. Principio: l'orologio/massa è la sorgente unica; verso e segno componenti dello stesso ω_tot.

**DISSENSO DA GUARDIANO [DIMOSTRATO]:**
- Poiché `nb = ψ†σψ`, lo spinore ψ è l'**autostato +1** di `nb·σ`. Quindi
  `exp(−i/2 ω_clk dt nb·σ) ψ = exp(−i/2 ω_clk dt) ψ` = **fase pura** (identica a `_phc`).
- Unire `ω_clk·nb` a `ω_new` in un solo U differisce dallo split solo per il commutatore BCH
  `[ω_new·σ, ω_clk nb·σ] dt² = 2i ω_clk (ω_new×nb)·σ dt² = O(dt²)`. Su una traiettoria: `O(dt²)·(T/dt) = O(dt) → 0`.
  **Nel continuo, motore-unito ≡ split.** Il sigillo D (convergenza-dt) lo rivelerebbe come artefatto.
- **Tensione strutturale:** MOD 2 (massa lungo nb, per la gravità) ⟹ fase pura ⟹ nessun accoppiamento nel
  continuo. Per accoppiare davvero segno↔verso la massa dovrebbe essere FUORI nb ⟹ inclina nb ⟹ rompe la
  gravità. Massa-lungo-nb e accoppiamento-genuino **si escludono**.
- **Corroborazione empirica:** il ramo OFF (legacy `ω_new + ω_clk·nb`) È la struttura "motore-unito"; nei
  pilota OFF ≈ ON su `segno_arco_coer`. Unito e split **non si distinguono nei dati**, come predice il continuo.

**Conclusione:** il motore-unico "fondi ω_clk·nb in ω_tot" è continuo-equivalente a ciò che è già misurato
NEGATIVO. Implementarlo darebbe (a) nessun effetto o (b) un artefatto-dt che il sigillo D scarta.

## 6. La via genuina (proposta, GATE aperto)

Il segno è RELAZIONALE d'arco (`⟨sign_i·sign_j⟩`). Per ordinarlo serve un termine che **agganci i segni dei
VICINI** nel continuo (primo ordine in dt), non una rifusione per-nodo lungo nb. L'unico gravità-safe (resta
lungo nb = fase pura per-nodo) e senza forzare verso=segno è **`--sync-fase-orologio`** (§30/§31): Kuramoto
sulla **fase di doppia-copertura** fra vicini, guidato dalla stessa sorgente-massa (coerenza d'arco), zero
parametri. Ordina `segno_arco_coer` direttamente e relazionalmente.

**Tre strade (in attesa di Luca):**
1. Implementare il motore-unico **come conferma negativa formale** (atteso ~0 + sigillo D che flagga l'artefatto).
2. **Pivot a `--sync-fase-orologio`** — l'accoppiamento relazionale genuino sul segno.
3. Rivedere il conto se c'è un buco (l'autostato +1, l'O(dt²), la corroborazione OFF≈ON).

Se anche `--sync-fase-orologio` desse ~0 su 3 semi a 2000 passi → **teorema di assenza pulito: sistema ABELIANO**
sul settore del segno, da registrare con onore.

## 7. Roadmap di fondo (DOPO il verdetto sul segno, NON ora)

**DE-PARAMETRIZZAZIONE = limite continuo = compressione**, UN parametro alla volta QUANDO il modello lo chiede:
sostituire scale assolute (GAMMA, K_C, DENS_CRIT_C, ELAST_C, TAU, medie globali) con rapporti di stato
adimensionali, verificando a ogni passo che convergenze/similitudini sopravvivano. Obiettivo: osservabili
intensive che convergono a N→∞ = costanti candidate. Programma lungo, separato, una leva alla volta.

## 8. Stato del repo / riproducibilità

- Nessuna modifica a `soliton_simulator.py` in questa sessione (solo run + lettura + questa relazione).
- Dati committati: `csv/deparam_pilota/` (§41), `csv/deparam_pilota_chi/` (§42). `.pkl` esclusi (gitignore),
  rigenerabili deterministicamente (seed 1). Script: `csv/_analisi_pilota.py <cartella>`.
- Comandi pilota (riproducibili): `--batch --nmasse 2 --sep 6 --seed 1 --passi 800 --ogni 100 --db-ogni 400
  --spinore-vivo --spinore-corretto --sync {--spin-feedback | --chi-da-spinore} [--deparam-orologio]`.
- Commit chiave: `86989a4` (§41), `d77c09b` (§42), + questo.

---

## 9. §44 — IMPLEMENTATO `--sync-fase-orologio` (la via genuina) + SIGILLI

Design approvato al gate (guardiano VIA LIBERA su (i)-(iv)). **Implementato** dietro flag `--sync-fase-orologio`
(default OFF = byte-identico). È la carta finale genuina: Kuramoto sul SEGNO di doppia-copertura.

**Cosa fa (codice):** in `_passo_spinoriale`, ramo `SPINORE_CORRETTO`, dopo il `_phc` de-param:
```
alpha_k = arg<canon(nb_k)|psi_k>            # segno di doppia-copertura (snapshot t-1)
z_k = e^{i alpha_k};  Z_k = (wI @ z)/uno    # media di vicinato pesata (snapshot t-1)
eta_k = forza_sync * sin(angle(Z)-angle(z)) * dt   # Kuramoto O(dt^1), forza dal Kuramoto-phi
psi_k -> e^{i eta_k} psi_k                  # FASE GLOBALE -> nb invariante, agisce solo sul SEGNO
```
Zero parametri (riusa `forza`/`wI`/`uno`/`K_SYNC`). Plumbing: `_forza_sync/_wI_sync/_uno_sync` ora salvati
anche `if SYNC_FASE_OROLOGIO`. Guard: richiede `--spinore-corretto` (senno' avviso/no-op).

**SIGILLI (dati in csv/_seal_sfo, probe rigenerabili):**
| sigillo | esito | come |
|---|---|---|
| 1 — OFF byte-identico | ✅ PASSATO | OLD (HEAD) vs NEW-off: tutti gli array `max\|A−B\|=0`, N=2111 |
| 3 — unitarietà | ✅ PASSATO | `\|ψ\|=1` (3.3e-16), len==n |
| 2 — gravità (nb O(dt²)) | ✅ PASSATO | a 1 passo `Δnb ≈ 0.57·Δψ²` (2° ordine); Δψ=2.7e-4 → Δnb=4.15e-8. Il torque NON tilta nb al 1° ordine → gravità-safe nel continuo |
| 5 — sign O(dt¹) | ✅ PASSATO (analitico) | `_eta = forza·sin(Δα)·dt`: dt fattore lineare esplicito, forza/α da snapshot t−1 → O(dt¹) per costruzione (stesso metodo che diagnosticò motore-unico=O(dt²)) |
| 4 — convergenza-dt | ⏳ da fare | sulle intensive, nella campagna covariante |

**Reperto importante (perché l'empirico non basta):** a 300 passi N diverge (ON=2051 vs OFF=2111). NON è
gravità: è il **caos** che amplifica QUALSIASI perturbazione (anche il residuo O(dt²)) a O(1) in ~3 passi
(nb 4e-8→0.375). Stesso meccanismo della de-param (§34, N 2014 vs 1990). Lo scaling-dt empirico a 1 passo è
**contaminato** da soglie discrete (mitosi/nascita-morte nodi → index-shift): Δψ empirico ~dt⁵, NON l'ordine
del torque. Per questo il sigillo 5 poggia sull'**analitico** (decisivo, non hand-waving) e il sigillo 4 va
letto sulle **intensive** (covarianza = la lezione del coarse-graining), non su N/traiettorie.

**DECISIONE (guardiano):** strada (1) **covariante** — NON il refactor (separare α scalare = estetica non
necessaria, cambierebbe il design da ri-verificare). Il caos decorrela N; le intensive (`segno_arco_coer`,
`verso_arco_coer`) a N-appaiato salgono comunque se il sync ordina.

**PROSSIMO:** pilota corto go/no-go (`--sync-fase-orologio` ON/OFF, prereqs `--spinore-vivo --spinore-corretto
--sync --deparam-orologio` fissi, 1 seme, 800 passi) su `segno_arco_coer`+`verso_arco_coer` a N-appaiato; se
accenna → pieno 3 semi/2000 passi + convergenza-dt (sigillo 4). Lettura (caveat own-canon del guardiano):
segno E verso insieme = ordinamento vero; solo segno = verificare artefatto own-canon.

**VERDETTO finale atteso:** segno_arco_coer ON≫OFF concorde 3 semi → **spin-½** (il sync relazionale ordina il
segno). Ancora ~0 → **teorema di assenza ABELIANO pulito** (tre vie fallite: filo §41/42, unico-artefatto §43,
sync-relazionale §44). Codice: `soliton_simulator.py` (flag `--sync-fase-orologio`, default OFF).
