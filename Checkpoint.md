# CHECKPOINT — Sistema dei Solitoni Relazionali (VQT / U2)

_Ultimo aggiornamento: 2026-09-03. Progetto di Luca Peano ("Il Muratore di Planck")._
_Traccia stato, fatto, da-fare. Da aggiornare a ogni sessione. Vedi CLAUDE.md per le norme di conduzione._

---

## AGGIORNAMENTO CORRENTE — 2026-09-03

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
- **[VERIFICATO]** Compilazione Python e batch breve con `diaglog` completati
      senza errori; il `diaglog` contiene le nuove colonne della schermatura.
- **[DA VERIFICARE]** Stabilità della taglia, contrasto nucleo/guscio e
      indipendenza da seed su tempi lunghi (almeno ~2000 passi, preferibilmente
      20000 e 2–3 semi).

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