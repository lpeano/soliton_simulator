# CHECKPOINT — Sistema dei Solitoni Relazionali (VQT / U2)

_Ultimo aggiornamento: 2025-08-27 (sera). Progetto di Luca Peano ("Il Muratore di Planck")._
_Traccia stato, fatto, da-fare. Da aggiornare a ogni sessione. Vedi CLAUDE.md per le norme di conduzione._

---

## STATO ATTUALE DEL CANONICO

File ufficiale: **`soliton_simulator.py`** (superset di tutto; ex-MULTIMASSA promosso a canonico).
Backup pre-promozione: `soliton_simulator_BACKUP_pre_multimassa_20250827.py`.

**Default fisici ora ufficiali:**
- `REGIME = "deterministico"` (era stocastico)
- `TAU_LOCALI = True` — forma tau pura (tre tau locali, kappa=1, nessun parametro)
- `CALORE_VETTORIALE = True` — calcio termico vettoriale-chirale (innesco precessione)
- `TAU_USA_D0 = False` — usa d (distanza reale); d0 attivabile con `--tau-d0`

**Flag reversibili CLI:** `--tau-d0`, `--calore-scal`, `--calore-vett`, `--regime stocastico`, `--giri 0`.

Documento canonico: **`leggi_del_sistema_solitoni.docx`**.

---

## FATTO (questa sessione)

- **Diaglog multimassa**: traccia tutte le masse (mI_*) e le interazioni per coppia (coer_ab,
  cosphi_ab, Lz_orb_ab, dist_ab). Header CSV dinamico.
- **Flag d/d0** (`--tau-d0`): tau_p su d0 invece di d. A run corti d~d0; divergono solo su run lunghi.
- **Calcio vettoriale-chirale** (`--calore-vett`): omega_s 3D + firma chirale di phivel. Verificato
  alla semina: chiralita' netta 0.39 (vs 0.03 scalare), omega_s 0.64 (vs 0).
- **Promozione a canonico** con backup datato. Default: determ + pura + calcio vett.
- **Documento**: sezioni 9.X (oscillatore di fase) e 9.Y (frustrazione + calcio chirale).
- **Script** `run_tutti.bash`/`.bat`: 10 test paralleli a 10000 passi.

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

## DA FARE — TODO DELLA SESSIONE (priorita' immediata)

- [ ] **Lanciare `run_tutti.bash`/.bat a 10000 passi** (hardware Luca; l'ambiente Claude sfora i timeout).
- [ ] A/B **calcio vett vs scalare** a 10000 passi, 3 masse, **con 2-3 semi**: Lz_orb concordi/crescenti
      (rotolamento) o pendolo? Escludere il caso del seed.
- [ ] **d vs d0 su run lungo**: respiro, oscillazione fase, valle ciano (d0 a 600 passi gia' meno ciano: 25 vs 44%).
- [ ] **Stabilita' oscillazione di fase** a 10000 passi (5-8 cicli): stabile, smorzata o amplificante?
- [ ] Dopo step ~2000: il pendolo diventa rotazione o resta oscillazione?
- [ ] Aggiornare docx 9.Y col 2o seed (segnale non replicato) + risultati run lunghi.
- [ ] Segno "azzurro tira": misura RITARDATA (non istantanea) della distanza ai picchi di ciano, su run lungo.

---

## DA FARE — TODO DAL DOCUMENTO (questioni aperte accumulate)

### Punto 0 — PRIORITA' MASSIMA: lo spin dei solitoni
- [ ] **Reimplementare la struttura del solitone** secondo le specifiche originali (sinusoide chirale
      che si chiude su se' stessa, doppia copertura 4pi, due antichiralita' di percorrenza). La fisica di
      base cambia -> ogni legge gia' stabilita andra' **rimisurata** sotto la nuova struttura.
- [ ] Settore spinoriale SU(2) a doppia copertura: quantizzazione dello spin in livelli subordinata a
      questa implementazione dinamica.

### Programma di eliminazione dei 6 parametri residui
- [ ] **P1** (pronto): costanti temporali dissipative -> rapporti adimensionali. _Sostanzialmente fatto
      con TAU_LOCALI (forma pura), ma vedi sotto "kappa"._
- [ ] **P2** (buon candidato): `KICK_TW=0.35` -> conversione dell'energia torsionale elastica accumulata
      E_tw = 1/2 K_C (Theta/2pi)^2 alla mitosi, invece di un calcio fisso.
- [ ] **P3** (in parte fatto): `G_PH=0.15` (attrito di fase, disperde energia fuori dal grafo) ->
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
- [ ] Il sistema NON stabilizza la taglia (manca opposizione all'accrescimento). Rimedio: **soglia
      DINAMICA di equilibrio** via creazione di coppia di antifase (non un valore fisso).
- [ ] Il freno deve agire sul **GUSCIO** (dove avviene la mitosi), non sul centro (gia' congelato).
- [ ] Modulare la separazione dell'anti-nodo come tanh(s): annichilazione dolce a bassa densita',
      netta ad alta. Resta da misurare l'efficacia del singolo evento di annichilazione.
- [ ] Ancorare scala e profondita' della schermatura a N_critico invece che a parametri liberi
      (P_LAM, LAM_MIN sono due parametri liberi da eliminare).
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
| `soliton_simulator_BACKUP_pre_multimassa_20250827.py` | backup pre-promozione |
| `soliton_simulator_MULTIMASSA.py` | copia allineata al canonico |
| `leggi_del_sistema_solitoni.docx` | documento canonico delle leggi |
| `run_tutti.bash` / `run_tutti.bat` | lancia tutti i test a 10000 passi in parallelo |
| `CLAUDE.md` | norme per l'agent (guardiano, principi, disciplina sperimentale) |