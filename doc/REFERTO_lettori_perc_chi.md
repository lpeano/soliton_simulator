# REFERTO — **i LETTORI di `perc_chi`, verificati dal disco**

> Mandato: *«la tabella dei lettori verificata dal disco → riporta PRIMA di scrivere codice»*
> (correzione del ramo C, §5.2). **Nessun codice scritto, nessun run lanciato.**
> Simulatore **`b46835bd`** (sha1 byte grezzi). Flag letti **a runtime** con l'argv del ramo A,
> non dedotti dai default.

---

## 1. IL FATTO CHE DECIDE IL DISEGNO — **la catena della torsione tocca `perc_chi` in UN SOLO PUNTO**

Con **`CHI_CORE = True`** (il ramo A), **tutti e tre i siti della catena passano da
`chiralita_core_locale()`**, e le letture dirette di `perc_chi` sono **rami `else` non
raggiungibili**:

| sito | forma | con `CHI_CORE=True` |
|---|---|---|
| `:2388-2395` `_passo_spinoriale` | `if CHI_CORE and len(perc_chi)>=n: chi_nodi = chiralita_core_locale()` **else** `chi_nodi = perc_chi[:n]` | **l'`else` NON gira** — ed e' contato `A8`: **0 salti su 12** |
| `:3763-3764` `step`, `FRAME_DRAG` | `if CHI_CORE and ...: chi_core = chiralita_core_locale()` | **passa di li'** |
| `:3766`/`:3772` `VERSO_CHI` / fallback | `elif` dopo il ramo `CHI_CORE` | **irraggiungibili** (`VERSO_CHI=False`) |
| `:3894-3898` `step`, `TORS_4PI` | `_chi_core_nodi` se `CHI_CORE`, **else** `perc_chi[:n]` | usa la **cache scritta a `:1600`** dalla stessa funzione |

> **E dentro `chiralita_core_locale()` la lettura e' UNA:** **`:1574`** — `chi =
> self.perc_chi[:self.n].astype(float)`, poi `chi_core = chi.copy()` e la media pesata
> `sum(wloc*chi[gruppo])/sum(wloc)` sul core locale.

**CONSEGUENZA OPERATIVA: dirottare `:1574` su `perc_geom` dirotta TUTTA la catena della torsione.**
**Un punto, non quattro** — ed e' esattamente cio' che `Z2` misura *(«la torsione riceve lo stesso
ingresso del ramo A»)*.
**I tre rami `else` (`:2395`, `:3772`, `:3898`) vanno dirottati LO STESSO**, benche' non
raggiungibili nel ramo A: hanno **lo stesso ruolo semantico**, e lasciarli su `perc_chi`
significherebbe che il giorno in cui `CHI_CORE` si spegne la geometria tornerebbe a leggere la
carica **in silenzio**. *(E' il difetto del default ribaltato, par.9.)*

---

## 2. ⚠ I LETTORI CHE NON SONO NELLA TABELLA DEL MANDATO — **CINQUE, e UNO E' VIVO**

**Non li assegno: li riporto, come il mandato impone.**

| sito | funzione | gate | **stato nel ramo A** | cosa fa con `perc_chi` |
|---|---|---|---|---|
| `:622` | `scuoti_vuoto` | `CALORE_VETTORIALE` | **OFF** *(il driver passa `--calore-scal`)* | `calcio = calcio * perc_chi` — **firma antichirale** del calcio termico su `phivel` |
| `:2099` | `_allaccia` | `COMPAT_CHI` | **OFF** | `opposti = perc_chi[a] != perc_chi[b]` — **allaccia SOLO archi fra chiralita' opposte** |
| `:2731` | `_passo_spinoriale` | `OROLOGIO_SEGNO` | **OFF** | `_sk = sign(perc_chi)` — **verso dell'orologio de Broglie** (materia `exp(-)` / antimateria `exp(+)`) |
| **`:4493`** | **`mitosi`** | **`REGIME == "deterministico"`** | **⚠ ACCESO** | `chi_a, chi_b = perc_chi[a], perc_chi[b]` — **calcio di fase ANTISIMMETRICO** ai due figli: `±0.5*KICK_TW*sciolta*chi*mod` |
| `:1878` | `circolazione_topologica` | `ha_spin` | diagnostico | `chi_n = perc_chi * _nb` — **gia' refutato** come fisica (`Z70`) |

### ⚠ E `:4493` E' VIVO MENTRE IL SUO PROPRIO COMMENTO DICE IL CONTRARIO

Il commento a **`:4489`** chiama l'altro ramo *«REGIME STOCASTICO (canonico, validato): rinculo di
fase casuale. **DEFAULT**»*. **E' FALSO.** `:115` dice
`REGIME = "deterministico"  # ... "deterministico" (default: forma pura + calcio vett)`, e
**letto a runtime con l'argv del ramo A vale `'deterministico'`** *(`KICK_TW = 0.35`)*.

> **Il ramo che gira e' quello che usa `perc_chi`.** **Verificato dall'esecuzione, non dal
> commento** (par.0). **Sesto commento stale catalogato in questo repo.**

**PERCHE' CONTA PER IL RAMO C:** tre dei cinque sono **spenti**, quindi la loro assegnazione e'
**byte-inerte in questo run** — qualunque cosa si decida. **`:4493` invece cambia i numeri**, ed e'
**l'unico dei cinque su cui la decisione ha conseguenze misurabili adesso.**

**COSA E' (per chi deve decidere, senza che decida io):** sta **dentro `mitosi()`**, ma **non e'
eredita'**: e' il **calcio di fase** che i due figli ricevono alla divisione, con una componente
**comune** e una **chirale antisimmetrica**. La tabella del mandato assegna *«eredita' alla mitosi /
coppie di Schwinger → `perc_chi`»*; **questo sito e' nella stessa funzione ma non e' quella riga**,
e va deciso esplicitamente.

---

## 3. GLI SCRITTORI — **cinque, e due sono i protagonisti**

| sito | funzione | cosa scrive |
|---|---|---|
| `:1966` | `semina` | **estensione**: `chi_nuovi = rng.choice([-1,1], n)` — carica **casuale** alla semina |
| `:4467` | `mitosi` | **estensione**: eredita `perc_chi[a]` — **stesso segno del genitore** *(rompe `N(+1)-N(-1)`)* |
| `:4597` | `mitosi`, Schwinger | **estensione**: `-perc_chi[aa]` — **segno opposto** *(conserva)* |
| **`:3924`** | **`step`, `CHI_BASC`** | **`perc_chi[:n] = where(twn > soglia, +1, -1)`** — **e' QUESTO che va su `perc_geom`** |
| **`:3941-3945`** | **`step`, `CHI_DA_SPINORE`** | **`perc_chi[:n] = where(Re(ov) >= 0, +1, -1)`** — **resta su `perc_chi`** |

---

## 4. I DIAGNOSTICI — **non toccano la fisica, e vanno lasciati su `perc_chi`**

`:1658` `misura_spin_picco_massa` · `:1715` `misura_spin_picco_per_chiralita` · `:1737`
`misura_spin_picco_positivi` · `:1878` `circolazione_topologica` · `:5583` render ·
`:7235` `segno_arco_coer_materia` · `:7625` `batch_condensazione`.

> **Misurano la CARICA** *(materia/antimateria, `perc_chi>0`)*: leggono `perc_chi` **per
> definizione**, e nel disegno cooperativo continuano a farlo. **Nessuno di questi scrive.**

---

## 5. COSA QUESTO REFERTO **NON** DICE

- **NON assegna** i cinque lettori fuori tabella: li **riporta**, come il mandato ordina;
- **NON dice che `:1574` sia l'unico punto in assoluto**: dice che **con `CHI_CORE=True`** e'
  l'unico **raggiungibile** della catena. Con `CHI_CORE` spento i tre `else` tornano vivi — ed e'
  la ragione per cui vanno dirottati anche loro;
- **NON misura nulla del ramo C**: e' una lettura del codice, **zero run**.
