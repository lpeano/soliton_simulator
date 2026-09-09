# RELAZIONE per Claude — Sessione 2026-09-09 (branch `dev-dof`)

> Report di continuità per la prossima sessione. Argomento: **sigilli e pilota della via NON-ABELIANA
> `--kuramoto-su2`** — l'ULTIMA carta per l'ordinamento del segno di doppia-copertura (spin-½). Lingua:
> italiano. Etichette: DIMOSTRATO / IN VERIFICA / APERTO / NEGATIVO. Tracing di dettaglio anche in
> `/memories/repo/deparam_orologio.md` §46–§46-bis e nel transcript `CLAUDECONNECT.md` (su `main`) §40–§46-bis.

---

## 0. TL;DR (leggi prima questo)

- **Sigilli `--kuramoto-su2` PASSATI** (macchina corretta): SIGILLO 1 (OFF byte-identico, OLD `ff2982e` vs
  NEW-off) `max|A-B|=0` su 28 array; SIGILLO 2 (unitarietà) `|ψ|=1` (3.3e-16), `len==n`; SIGILLO 3 (primo
  ordine) analitico O(dt¹); SIGILLO 4 (conv-dt) rinviato alla campagna. [DIMOSTRATO]
- **Pilota go/no-go = NO-GO.** A N appaiato (covariante), il primario `spin_overlap_arco` (coerenza SU(2)
  PIENA) è **0.500 in ON come in OFF** = spinori **scorrelati** sugli archi. `segno_arco_coer` e
  `verso_arco_coer` ≈ 0, ON ≈ OFF. L'olonomia **non trasferisce coerenza al segno**. [IN VERIFICA → NEGATIVO]
- **L'unico stacco è nella direzione sbagliata:** `segno_ov_absmedia` ON < OFF di 0.041 → il torque
  geodetico **abbassa** il commitment locale al foglio (disordina), non lo ordina relazionalmente.
- **Bilancio programma spin-½:** 4 vie tutte piatte (`segno_arco_coer≈0`, ON=OFF): §41 spin-feedback
  (indiretto), §42 chi-da-spinore (diretto), §44 sync-fase-orologio (Kuramoto abeliano O(dt¹) genuino),
  §46 kuramoto-su2 (**non-abeliano genuino, l'ultima carta**). §43 motore-unico = artefatto O(dt²).
  → **IPOTESI ABELIANA molto forte.** Nessun accoppiamento ordina il segno di doppia-copertura.
- **Cautele ferree:** pilota a **800 passi = FORMAZIONE** (sotto 2000), **1 seme**. NON è verdetto.
  Il verdetto "ABELIANO DEFINITIVO" (negativo che vale quanto un positivo) va **certificato** a 3 semi/2000.

---

## 1. Cosa è stato fatto in sessione

### 1.1 Sigilli `--kuramoto-su2` (ripresa §46 → §46-bis)
- OLD (pre-kuramoto) = commit `ff2982e` (HEAD `1fcf16c` contiene già il codice kuramoto → per il sigillo 1
  OLD deve essere il commit PRIMA di kuramoto). Cartella temp `csv/_seal_k2/` (`_old_sim.py` estratto da
  `git show ff2982e:...`, `_verifica.py`, `db_*.pkl`, `*.csv`).
- 3 run 300 passi seed 1, prereq `--spinore-vivo --spinore-corretto --sync --deparam-orologio`: OLD,
  NEW-off, NEW-on `--kuramoto-su2`.
- **SIGILLO 1** (OFF byte-identico, OLD vs NEW-off): `max|A-B| = 0` su 28 array. **PASSATO** — il flag OFF
  non tocca la fisica. NB tecnica: gli array complessi (`_psi_spinor`, `psi`, `_psi_prec`) vanno confrontati
  col **modulo** `np.abs(a-b)`, non castandoli a `float` (scarterebbe la parte immaginaria).
- **SIGILLO 2** (unitarietà NEW-on): `|ψ_spinor| = 1` (`max|1-|.|| = 3.3e-16`), `len(ψ) == n = 1856`.
  **PASSATO.** NB: `n` è una `@property`, NON in `__dict__`/attrs del pkl → dedurlo da `len(phi)`.
- **SIGILLO 3** (primo ordine): analitico. L'angolo di rotazione = `|Ω|·dt` con `dt` fattore lineare
  esplicito → O(dt¹) per costruzione (empirico contaminato da soglie/caos come in §44). [DIMOSTRATO analitico]
- **SIGILLO 4** (conv-dt): rinviato alla campagna covariante (sulle intensive, N appaiato).

### 1.2 Pilota go/no-go (800 passi, seed 1, ON vs OFF)
- `csv/deparam_pilota_k2/{on,off}.csv` + `cond_*`. Prereq fissi `--spinore-vivo --spinore-corretto --sync
  --deparam-orologio`; unica variabile `--kuramoto-su2`.
- Il sistema si espande forte: **N 824 → 2231 (×2.71)**, `tau_cum ≈ 704`. → confronto **covariante a N
  appaiato** obbligato (a passo fisso misureresti l'espansione = il dito).

---

## 2. Numeri del pilota (a N appaiato, terzo tardivo, finestra N comune [824, 2231])

| Order parameter | ON | OFF | ON−OFF | sd | esito |
|---|---|---|---|---|---|
| `spin_overlap_arco` (SU(2) pieno, **primario**) | 0.50001 | 0.50002 | −0.00001 | 0.0010 | ~uguale |
| `segno_arco_coer` | −0.00003 | 0.00013 | −0.00016 | 0.0038 | ~uguale |
| `verso_arco_coer` | 0.00002 | 0.00003 | −0.00002 | 0.0020 | ~uguale |
| `segno_ov_absmedia` (commitment locale) | 0.666 | 0.708 | **−0.041** | 0.0088 | STACCA (↓, direzione sbagliata) |
| `spin_axis_R` | 0.039 | 0.039 | +0.0007 | 0.019 | ~uguale |

Accoppiamento segno↔verso (corr temporale, 2ª metà del solo ON): `corr(segno,verso) = +0.016 ≈ 0`
(**non** un motore unico), `corr(verso,overlap) = +1.000` (l'overlap SU(2) è guidato **solo** dal verso;
il segno non ci mette coerenza), `corr(segno,overlap) = +0.016`.

**Interpretazione (guardiano):** il torque non-abeliano muove gli spinori, ma il segno resta **scollegato**
dal verso e la coerenza SU(2) piena sugli archi resta a livello di scorrelato (0.500). L'olonomia — la fase
geometrica dell'asse variabile `nb×nb_bar` — **non genera** coerenza di segno relazionale. Esattamente lo
scenario "verso allinea, segno no" che avevamo indicato come *olonomia persa*; qui, per giunta, a 800 passi
con espansione ×2.71 **nemmeno il verso** si ordina sugli archi (il disordine di popolazione da mitosi domina).

---

## 3. Cosa resta da fare (gate a Luca)

- **(A) [consigliata]** Conferma disciplinare **3 semi / 2000 passi + conv-dt covariante** su `--kuramoto-su2`
  ON/OFF (N appaiato). Se `spin_overlap_arco`/`segno_arco_coer` restano ~0 concordi → **ABELIANO DEFINITIVO**
  (il negativo formale che chiude il programma spin-½ con questo motore). È la chiusura dovuta di un filone
  lungo, e i pilota sono a formazione.
- **(B)** Diagnosi (zero-param, non rinforzabile) del *perché* nemmeno il non-abeliano ordina: ipotesi guida =
  il torque geodetico si dissolve nella mitosi/espansione ×2.71 più veloce di quanto allinei; oppure il segno
  è genuinamente un gauge non-osservabile in questo motore (à la §38: condizionalmente dinamico).
- **NON** introdurre un termine che forza `verso = segno` per "farli ordinare": sarebbe un trucco, non una
  legge. La linea rossa §40 resta.

---

## 4. Stato repo / riproducibilità

- `soliton_simulator.py` **NON modificato** in sessione (solo sigilli + run + lettura). HEAD codice = `1fcf16c`.
- Evidenza sigilli: `csv/_seal_k2/_verifica.py` (committato `6a3864a`). `_old_sim.py`/`.pkl`/csv esclusi
  (rigenerabili: OLD = `git show ff2982e:soliton_simulator.py`; DB deterministici seed 1).
- Dati pilota: `csv/deparam_pilota_k2/{on,off,cond_on,cond_off}.csv` + `_valuta_on.py` + `_confronta.py`.
  I `.pkl` esclusi (gitignore).
- Doc canonica su `main` (`CLAUDECONNECT.md` §40–§46-bis, `Checkpoint.md`) allineata (commit `40c7dc8`).

---

## 5. AGGIORNAMENTO (stessa giornata) — I TRE FRENI A MANO + fix `CHI_BASC` [DIMOSTRATO]

Dopo il NO-GO del pilota `--kuramoto-su2`, l'intuizione di Luca ("il test ha tutti gli agganci?") ha
innescato una catena di verifiche. Il pilota girava **col freno a mano — anzi, triplo**:

1. **Flag spenti**: il pilota kuramoto-su2 girava con `CHI_BASC=OFF` e `OLON_PART=OFF` — i due meccanismi
   che organizzano/sbloccano l'olonomia (rompono il bilanciamento 50/50 dei ±π).
2. **`CHI_BASC` ROTTO** (test-GRATIS sui dati reali `db_ond.pkl`): il codice (riga ~2308) usava
   `soglia = np.median(twn)` — **MEDIANA GLOBALE** — mentre il commento dichiara "soglia = 2π (PHI_CRIT)".
   **Il commento mente.** Conseguenze verificate sui dati: la mediana dà `perc_chi=+1` al **50.0%** dei nodi
   (per costruzione ~metà sopra/metà sotto) → **IMPONE** il 50/50 che `CHI_BASC` dovrebbe *rompere*. Tre
   violazioni: (a) commento mente; (b) la mediana è il freno a mano DENTRO lo sblocco; (c) viola "la media
   non va qui" (mediana globale in decisione locale). Distribuzione `twn`: min 0.02, median 2.88, max 7.85,
   2π=6.28 → con soglia 2π solo **0.9%** maturi (17 nodi su 1856).
3. **`OLON_PART` inerte senza `--viriale`**: annidato in `if VIRIALE:` (righe 3004–3011). Senza viriale non
   fa nulla → il braccio B come da prompt sarebbe stato un altro test viziato (misura zero).

### FIX di legge (non trucco): `CHI_BASC` soglia `median(twn)` → `PHI_CRIT`
- Backup datato `soliton_simulator.backup_2026-09-09_chibasc-2pi.py`. Diff = **1 riga** (riga ~2308),
  isolata dentro `if CHI_BASC:`. Allinea il codice alla legge già scritta nel commento (soglia = quanto 2π,
  locale per-nodo, zero parametri). NON è un target ("finché il segno si ordina") ma un allineamento-alla-legge.
- **SIGILLO OFF byte-identico PASSATO**: backup vs fix (senza `--chi-basc`), `max|A-B|=0` su 28 array →
  non-regressione intatta (il fix vive solo nel ramo ON).
- **Run-lampo (100 passi, `--chi-basc`)**: `perc_chi=+1` all'**1.3%** (98.7% a −1, mean −0.974) → il flag ORA
  rompe il 50/50 (legge vera). [confermato che il flag fa ciò che deve, prima di leggere i risultati]

### Disegno del test (concordato con Luca) — attribuzione pulita
`VIRIALE` = conversione viriale: converte spinta **radiale → tangenziale/orbitale** (in base alla circolazione
del twist), imparentata col frame-dragging; zero param, normalizza per 2π. `OLON_PART` vive dentro: fa entrare
l'**olonomia locale** (`twn_a`) nella conversione tangenziale → inerte senza VIRIALE.

| Braccio | Flag oltre base+kuramoto-su2 | Confronto |
|---|---|---|
| baseline | (nessuno) = `csv/deparam_pilota_k2/on.csv` | — |
| **A** | `--chi-basc` (fixato 2π) | vs baseline |
| **V** | `--viriale` (controllo) | vs baseline |
| **B** | `--viriale --olon-part` | vs **V** (isola OLON_PART) |
| **C** | `--chi-basc --viriale --olon-part` | vs V e vs A |

### STATO (a fine sessione)
- **Braccio A COMPLETATO (800 passi, seed 1) — NO-GO su ENTRAMBI gli assi [IN VERIFICA].**
  Confronto covariante a N appaiato (script `csv/deparam_bracci/_confronta_braccio.py`, braccio vs
  baseline `csv/deparam_pilota_k2/on.csv`). **Fatto strutturale**: `--chi-basc` (98.7% a −1) **soffoca la
  crescita** — N arriva a **1174** vs **2231** del baseline (mitosi quasi ferma con quasi-tutto vuoto);
  finestra N comune ristretta [826, 1174].
  - **Asse SBILANCIAMENTO/olonomia netta**: `berry_spin_media` (firmata) A=0.009 vs base=0.096 (~uguale,
    A più basso → NON sale); `berry_spin_media_assoluta` ~1.13 uguale; `olonomia_fase_media_assoluta`
    A=6.94 vs base=10.10 (**STACCA ↓**). → l'olonomia locale ASSOLUTA è forte e uguale, ma la FIRMATA ~0
    in entrambi = i segni si CANCELLANO (frustrata, senza verso netto). Rompere il 50/50 non le dà un verso.
  - **Asse ORDINE LOCALE**: `spin_overlap_arco` A=0.49986 vs base=0.49926 (~uguale, **0.5 = scorrelato**);
    `segno_arco_coer`/`verso_arco_coer` ~0, ~uguali. Nessuna coerenza locale.
  - Contesto: `segno_ov_absmedia` A=0.633 vs base=0.819 (**STACCA ↓** = meno commitment locale).
  - **VERDETTO A**: il 50/50 NON era il blocco. Sbilanciare verso 98.7% −1 (legge vera 2π) non sblocca
    l'olonomia netta né crea ordine locale — la DEPRIME (olonomia_fase ↓, commitment ↓) e soffoca la
    dinamica. **Conferma la questione profonda: il muro sembra il quanto 2π stesso, non la configurazione
    delle chiralità.** "Sbilanciare ≠ ordinare": qui non fa né l'uno né l'altro nel verso giusto.
  - Cautele: 800p=formazione, 1 seme; N comune ristretto (soppressione crescita). Firma però chiara e negativa.
- **PROSSIMO**: bracci V (viriale-solo, controllo) e B (viriale+olon-part vs V) testano un asse INDIPENDENTE
  (conversione radiale→orbitale + olonomia locale), non tocco da chi-basc. Poi C (tutto). In attesa scelta Luca:
  procedere V/B/C o fermarsi a ragionare sul quanto 2π (il muro candidato).

### Riproducibilità / doppio-check per Claude
- Fix: 1 riga, `git diff soliton_simulator.py`. Backup = `soliton_simulator.backup_2026-09-09_chibasc-2pi.py`.
- Test-GRATIS soglia: rigira lo snippet su `csv/_seal_k2/db_ond.pkl` (median vs 2π sulla torsione `twn`).
- Sigillo OFF: `csv/_seal_chibasc/{bkoff,newoff,cond_*}.csv` (+ i DB `.pkl` esclusi ma rigenerabili seed 1);
  confronto attrs backup vs fix. Run-lampo: `csv/_seal_chibasc/lampo.csv` + `db_lampo.pkl`.
- **DA VERIFICARE (Claude)**: che il fix sia SOLO allineamento-alla-legge (soglia 2π = PHI_CRIT, locale,
  zero param), non un target; che il sigillo OFF sia davvero byte-identico; che la lettura dei bracci usi
  entrambi gli assi (berry = sbilanciamento, overlap/segno = ordine locale) a N appaiato.

---

## 5. DOPPIO CHECK richiesto a Claude (rivedi il CODICE del test, non fidarti dei numeri)

Un sigillo/confronto vale quanto lo script che lo calcola. Ti chiedo esplicitamente di **rileggere e
criticare** i tre script del test (committati e pushati su `origin/dev-dof`), prima di dare per buono il
verdetto NO-GO. Cerca bug, bias e assunzioni nascoste — sono io stesso ad averli scritti in questa sessione.

**Script da revisionare (percorsi esatti):**
1. `csv/_seal_k2/_verifica.py` (commit `6a3864a`) — SIGILLI 1 (OFF byte-identico OLD vs NEW-off) e 2
   (unitarietà). **Punti da controllare:** (a) gli array complessi sono confrontati col **modulo**
   `np.abs(a-b)` — corretto per il byte-identico (se `a==b` → 0), ma verifica che non nasconda differenze
   di fase; (b) le chiavi presenti "solo in OLD" o "solo in NEW-off" sono **stampate ma NON fanno fallire**
   il sigillo — è giusto? (sono cache diagnostiche, ma controlla); (c) `n` è dedotto da `len(phi)` perché è
   una `@property` non serializzata — verifica che `phi` sia effettivamente per-nodo.
2. `csv/deparam_pilota_k2/_valuta_on.py` (commit `b729fe8`) — evoluzione temporale + correlazioni del solo ON.
   **Punti da controllare:** (a) possibile **bias own-canon**: `segno = sign(Re⟨canon(nb)|ψ⟩)` usa `_bloch_a_spinore(nb)`
   come canone, che dipende da `nb` stesso → il segno potrebbe essere parzialmente auto-referenziale; (b)
   `corr(verso, overlap) = +1.000` è **sospettosamente perfetto** — è una tautologia (`spin_overlap_arco` è
   dominato dal verso by construction) o un vero segnale? va capito.
3. `csv/deparam_pilota_k2/_confronta.py` (commit `b729fe8`) — confronto covariante ON vs OFF **a N appaiato**
   via interpolazione su griglia di N. **Punti da controllare:** (a) `N` non è perfettamente monotono (la
   mitosi lo fa oscillare) → `argsort(N)+np.interp` può introdurre artefatti; valuta se serve un binning
   robusto invece dell'interpolazione; (b) il test di significatività `|media| > 2·sd` sulla finestra tardiva
   è **grezzo** (nessun n_eff, nessuna correzione per autocorrelazione temporale) — va bene per un pilota ma
   NON per il verdetto a 2000/3 semi; (c) la finestra "tardiva" = ultimo terzo del **range di N comune**, non
   dello step: conferma che sia la scelta covariante giusta.

**Se trovi un errore che cambia il segno del risultato → il NO-GO va rifatto.** Se gli script reggono, il
NO-GO del pilota è solido come pilota (ma resta 800p/1 seme → conferma 3 semi/2000 comunque necessaria).
