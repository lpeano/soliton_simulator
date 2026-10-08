# L'INDICE `v2` — **il referto della migrazione e della BONIFICA**

> ### ⛔ **I `6` CONTROLLI PASSANO** *(`6` su `6`)*, e il piu' importante e' il ### **primo**: ogni ID del vecchio indice compare in ### **UNO E UNO SOLO** di `voci.jsonl::id`, `voci.jsonl::alias`, `etichette_rimosse.jsonl`. ### **`0` persi, `0` doppi.**
>
> *Ogni numero esce da `doc/indice/` o da `doc/indice/_controlli.txt`.* *(`L-NUMERI`)*

---

# ⭐ `①` **I CONTEGGI**

| | |
|---|--:|
| ID al tag `era-1-secondo-ordine` | `953` |
| ### **voci** in `voci.jsonl` | ### **`867`** |
| ### **etichette rimosse** | ### **`85`** |
| righe di ### **traccia** | `974` |
| ### **conflitti** con le liste del guardiano | ### **`0`** |
| voci ### **bloccanti** | `12` |

### **per `classe`**

| `DIFETTO` | `FRONTE` | `CRITERIO` | `MISURA` | `TEORIA` | `CURA` | `PRESIDIO` | `STANDARD` |
|--:|--:|--:|--:|--:|--:|--:|--:|
| **441** | **166** | **91** | **54** | **51** | **46** | **16** | **2** |

### **per `dominio`**

| `DA_CLASSIFICARE` | `FISICA` | `METODO` | `INFRASTRUTTURA` |
|--:|--:|--:|--:|
| **664** | **94** | **79** | **30** |

### **per `era`**

| `DA_CLASSIFICARE` | `ENTRAMBE` | `1` | `2` |
|--:|--:|--:|--:|
| **713** | **65** | **46** | **43** |

### **per `stato`**

| `DA_CLASSIFICARE` | `CHIUSA` | `APERTA` | `SOSPESA` | `AGENDA` |
|--:|--:|--:|--:|--:|
| **480** | **187** | **111** | **46** | **43** |

### **LE REGOLE DELLA MIGRAZIONE, per quante volte hanno DECISO**

| regola | volte | che cosa fa |
|---|--:|---|
| `(a)` | ### **629** | i campi meccanici dall'indice del tag |
| `(b3)` | ### **228** | un segnaposto che ### **resta come voce `DA_CLASSIFICARE`** |
| `(b2)` | ### **84** | un segnaposto diventato ### **ETICHETTA DI DOCUMENTO** *(fuori da `voci.jsonl`)* |
| `(a2)` | ### **21** | un `alias` che era ### **l'ID di un'altra voce**: diventa un COLLEGAMENTO |
| `(a3)` | ### **10** | un ID con uno ### **SPAZIO**: normalizzato, e ### **il nome vecchio RESTA come alias** |
| `(b0)` | ### **1** | un segnaposto che era ### **un ID di VOCABOLARIO**, non una voce |
| `(a4)` | ### **1** | due ID vecchi che normalizzavano ### **nello stesso**: il secondo e' alias del primo |

# ✔ `②` **IL RAPPORTO DEI CONFLITTI con le liste del guardiano**

### ⭐ **NESSUN CONFLITTO.** Le tre liste si applicano al `100 %`:

| lista | che cosa impone | applicata |
|---|---|--:|
| ### **`L1`** | `METODO` o `INFRASTRUTTURA`, era `ENTRAMBE`, stato dall'era `1` | ### **`62` su `62`** |
| ### **`L2`** | `AGENDA`, `FISICA`, era `2` | ### **`43` su `43`** |
| ### **`L3`** | `SOSPESA`, `FISICA`, era `1` | ### **`46` su `46`** |

> ### ⚠ **E LA SCELTA FRA `METODO` E `INFRASTRUTTURA` E' MIA**, col motivo accanto a ciascuna nel sorgente. ### **La regola che ho usato:** `METODO` = come si ### **RAGIONA** e come si ### **MISURA**; `INFRASTRUTTURA` = gli ### **STRUMENTI** e i ### **FILE**. ### ⛔ **E' un giudizio, e Luca lo corregga.**

| | |
|---|--:|
| `METODO` nella `L1` | `32` |
| `INFRASTRUTTURA` nella `L1` | `30` |

### ⛔ **E LE DIECI NOTE «candidata SUPERATA da …» SONO NOTE, NON CHIUSURE:** nessuna voce e' stata chiusa ne' superata. ### **Si chiudono AL TRIAGE**, e il criterio e' in `doc/TRIAGE_ERA_1.md`.

# ⛔ `③` **LA TAVOLA CORTA DEI `DA_CLASSIFICARE`, per Luca** — *`480` voci*

### **Perche' non sono classificabili, in tre gruppi:**

| gruppo | quante | ### **perche'** | ### **la proposta** |
|---|--:|---|---|
| ### **SEGNAPOSTO** | ### **`233`** | erano voci *«(CITATO N volte, MAI definito in un registro)»*, e le loro citazioni ### **NON stanno solo** in task history o referti: stanno nel ### **codice** o in documenti di lavoro | ### **leggere `file_citanti`**: se la citazione e' un'etichetta locale, va in `etichette_rimosse`; se e' un difetto vero, va scritta come voce |
| ### **`tipo = altro`** | ### **`32`** | l'era `1` le marcava `altro`, che ### **non e' un'informazione** | ### **leggere la voce** e darle una classe. ### ⛔ **La migrazione NON ha indovinato**, ed e' il punto |
| ### **senza evidenza strutturale** | ### **`215`** | non sono `PRESIDIO` ne' `STANDARD`, non hanno un `padre`, e non erano chiuse | ### **il triage**: `indice cerca --stato DA_CLASSIFICARE` |

### **I PRIMI VENTI SEGNAPOSTO per numero di citazioni** *(il resto con `indice cerca --stato DA_CLASSIFICARE`)*:

| id | citazioni | ### **dove** | titolo dell'era `1` |
|---|--:|---|---|
| `IC95` | ### **216** | `STATO_CLAUDE_fork-su2.md` `csv/_indice_riordino.py` | (CITATO 80 volte, MAI definito in un registro) |
| `R1` | ### **200** | `ROADMAP_dev-spinoriale.md` `csv/_seal_53c/_old_sim.py` | (CITATO 30 volte, MAI definito in un registro) |
| `I2` | ### **192** | `RELAZIONE_PER_CLAUDE.md` `csv/_seal_53c/_old_sim.py` | (CITATO 28 volte, MAI definito in un registro) |
| `K1` | ### **182** | `RELAZIONE_PER_CLAUDE.md` `csv/_collaudo_istruzioni.py` | (CITATO 26 volte, MAI definito in un registro) |
| `TERRA-BUCONERO` | ### **158** | `csv/_indice_riordino.py` `csv/_seal_53c/_old_sim.py` | (CITATO 3 volte, MAI definito in un registro)  |
| `E1` | ### **152** | `RELAZIONE_PER_CLAUDE.md` `csv/_cure_verificate.py` | (CITATO 56 volte, MAI definito in un registro) |
| `P7` | ### **148** | `README.md` `STATO_CLAUDE_fork-su2.md` | (CITATO 18 volte, MAI definito in un registro) |
| `N3b` | ### **143** | `csv/_seal_fork/_ab_chibasc/_sim_prima.py` `csv/_seal_fork/_c1_semina/_sim_vecchio.py` | (CITATO 22 volte, MAI definito in un registro) |
| `T6` | ### **140** | `csv/_seal_fork/_c1_semina/_sim_vecchio.py` `csv/_seal_fork/_guasto_ripieghi/_sim_precura.py` | (CITATO 32 volte, MAI definito in un registro) |
| `W3` | ### **139** | `csv/_indice_riordino.py` `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | (CITATO 3 volte, MAI definito in un registro;  |
| `Y3` | ### **139** | `csv/_seal_fork/_ab_chibasc/_sim_prima.py` `csv/_seal_fork/_c1_semina/_sim_vecchio.py` | (CITATO 9 volte, MAI definito in un registro)  |
| `Y4` | ### **138** | `csv/_seal_fork/_ab_chibasc/_sim_prima.py` `csv/_seal_fork/_c1_semina/_sim_vecchio.py` | (CITATO 5 volte, MAI definito in un registro)  |
| `HDF5` | ### **133** | `csv/_seal_fork/_ab_chibasc/_sim_prima.py` `csv/_seal_fork/_c1_semina/_sim_vecchio.py` | (CITATO 8 volte, MAI definito in un registro) |
| `CONFIG-1/` | ### **125** | `csv/_seal_fork/_guasto_ripieghi/_sim_precura.py` `csv/_seal_fork/_sig_contrasto/SIGILLO_contrasto_intensivo.txt` | (CITATO 4 volte, MAI definito in un registro)  |
| `I3` | ### **124** | `csv/_seal_fork/_c1_semina/_sim_vecchio.py` `csv/_seal_fork/_guasto_ripieghi/_sim_precura.py` | (CITATO 8 volte, MAI definito in un registro)  |
| `M0` | ### **115** | `README.md` `csv/_indice_riordino.py` | (CITATO 3 volte, MAI definito in un registro;  |
| `K2` | ### **87** | `RELAZIONE_PER_CLAUDE.md` `csv/_collaudo_istruzioni.py` | (CITATO 19 volte, MAI definito in un registro) |
| `P0` | ### **80** | `csv/_seal_53c/_old_sim.py` `csv/_seal_fork/_ab_chibasc/_sim_prima.py` | (CITATO 12 volte, MAI definito in un registro; |
| `K5` | ### **72** | `csv/_collaudo_istruzioni.py` `csv/_configurazione.py` | (CITATO 12 volte, MAI definito in un registro) |
| `K3` | ### **71** | `csv/_collaudo_istruzioni.py` `csv/_configurazione.py` | (CITATO 17 volte, MAI definito in un registro) |

# 📌 `④` **LE ETICHETTE RIMOSSE** — *`85`, con `1633` citazioni in tutto*

### ⛔ **NON sono voci perdute: sono ID che NON ERANO VOCI.** Ciascuna porta ### **il numero di citazioni e i file**, e la regola che l'ha decisa.

| id | citazioni | regola | ### **dove** |
|---|--:|---|---|
| `T1` | ### **236** | (b2) DICHIARATA etichetta in una n | `RELAZIONE_PER_CLAUDE.md` `STATO_CLAUDE_fork-su2.md` |
| `S3` | ### **229** | (b2) DICHIARATA etichetta in una n | `CLAUDECONNECT.md` `RELAZIONE_CLAUDE_dev-spinoriale.md` |
| `S1` | ### **224** | (b2) DICHIARATA etichetta in una n | `CLAUDECONNECT.md` `RELAZIONE_CLAUDE_dev-spinoriale.md` |
| `MASSE-COERENTI` | ### **221** | (b2) DICHIARATA etichetta in una n | `README.md` `RELAZIONE_PER_CLAUDE.md` |
| `D3` | ### **172** | (b2) DICHIARATA etichetta in una n | `RELAZIONE_PER_CLAUDE.md` `csv/_seal_53c/_old_sim.py` |
| `TEMPO-LUCE` | ### **160** | (b2) DICHIARATA etichetta in una n | `csv/_chi_usa_il_tempo_luce.py` `csv/_indice_riordino.py` |
| `A3b` | ### **149** | (b0) e' un ID di VOCABOLARIO, non  | `csv/_registri_indice.py` `csv/_regole_proposta.py` |
| `STEP2` | ### **45** | (b2) DICHIARATA etichetta in una n | `RELAZIONE_PER_CLAUDE.md` `csv/_seal_fork/_sigillo_z43_cura1.py` |
| `H1` | ### **32** | (b2) DICHIARATA etichetta in una n | `RELAZIONE_PER_CLAUDE.md` `csv/_seal_fork/_P10_rigiro_a1ae5090.txt` |
| `H3` | ### **30** | (b2) DICHIARATA etichetta in una n | `RELAZIONE_PER_CLAUDE.md` `csv/_seal_fork/_P10_rigiro_a1ae5090.txt` |
| `H2` | ### **24** | (b2) DICHIARATA etichetta in una n | `RELAZIONE_PER_CLAUDE.md` `csv/_seal_fork/_P10_rigiro_a1ae5090.txt` |
| `D4` | ### **7** | (b2) DICHIARATA etichetta in una n | `csv/_seal_fork/_sigillo_chicoop_driver.py` `csv/_test_fork/_doc_traduzione.py` |
| `F4` | ### **3** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/STATO_RUN.md` |
| `F5` | ### **3** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/STATO_RUN.md` |
| `RI-LETTO` | ### **3** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/REFERTO_Z36_cucitura.md` |
| `CURA1-CORTO` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/STATO_RUN.md` |
| `CURA2-CORTO` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/STATO_RUN.md` |
| `D97` | ### **2** | (b2) DICHIARATA etichetta in una n | `doc/LISTA_CHIUSA.md` `doc/relazioni/2026-09-26.md` |
| `DIFETTI-NUOVI-FINE` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/STATO_RUN.md` |
| `INERZIA-1(` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/relazioni/2026-09-25.md` |
| `MANDATO-PATTERN` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/STATO_RUN.md` |
| `MODEL-FREE` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/relazioni/2026-09-25.md` |
| `N8` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/REFERTO_frequenza_riferimento.md` |
| `RAMPA-2/` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/STATO_RUN.md` |
| `RI-GIRABILI` | ### **2** | (b2) tutte le citazioni sono in do | `doc/LISTA_CHIUSA.md` `doc/STATO_RUN.md` |

*(Le altre `60` stanno in `doc/indice/etichette_rimosse.jsonl`.)*

# 📌 `⑤` **I LETTORI DELLA VISTA: censiti e dichiarati**

| file | che cos'e' | ### **che cosa gli e' successo** |
|---|---|---|
| `csv/_indice_id.py` | il validatore dell'era 1 | ADATTATO: legge la VISTA, e gli stati dello schema 2 sono nel suo vocabolario; il controllo delle VOCI PERSE ora sa degli alias e delle etichette rimosse |
| `csv/_hook_presidi.py` | il `pre-commit` | ADATTATO: gira ANCHE `indice.py valida`, e solo se `voci.jsonl` esiste -- cosi' si accende da se' |
| `csv/_presidio_indice.py` | `H-INDICE` nel `commit-msg` | legge la VISTA: gli ID che cerca ci sono tutti |
| `csv/_presidio_righe.py` | il presidio delle righe | legge la VISTA |
| `csv/_lista_chiusa.py` | la lista congelata | legge la VISTA |
| `csv/_punto_della_situazione.py` | il punto della situazione | legge la VISTA |
| `csv/_analisi_lettori_indice.py` | l'analisi dei lettori | legge la VISTA |
| `csv/_confronto_pds.py` | il confronto fra punti | legge la VISTA |
| `csv/_controlli_riordino.py` | i controlli del riordino | legge la VISTA |
| `csv/_indice_riordino.py` | il riordino | legge la VISTA |

### ⭐ **DUE SONO STATI ADATTATI, gli altri otto NO — e il motivo e' lo scopo della vista:** `doc/INDICE_ID.tsv` si rigenera con ### **le stesse `15` colonne**, quindi chi la legge ### **non si accorge del cambio di schema.** ### ⚠ **E' compatibilita', non equivalenza:** `leggi`, `variabili`, `assiomi`, `collegate` e `padre` ### **non hanno una colonna**, e chi li vuole legge la fonte.

---

# ⛔ **CHE COSA QUESTO REFERTO NON DICE**

| | |
|---|---|
| che l'indice sia ### **classificato** | ### ⛔ **no: `480` voci sono `DA_CLASSIFICARE`**, e sono ### **decisioni di Luca.** La migrazione ### **non ha indovinato niente** |
| che le voci sospese siano ### **giuste** | le `46` della lista `L3` sono ### **quelle del guardiano**, applicate come indicate. ### **Le altre non sono state sospese**, perche' senza dominio non si sa se la sospensione le riguarda |
| che le ### **etichette rimosse** siano spazzatura | ### **no:** alcune hanno ### **decine di citazioni**. Non erano ### **voci dell'indice**, e questo e' tutto |
| che la classificazione ### **`METODO`/`INFRASTRUTTURA`** sia verificata | ### ⚠ **e' un GIUDIZIO MIO**, col motivo accanto a ciascuna. ### **Luca lo corregga** |
| che il ### **triage** sia fatto | ### ⛔ **no**, e non si fa adesso: il piano e' in `doc/TRIAGE_ERA_1.md`, e parte da `indice cerca --stato SOSPESA` |
