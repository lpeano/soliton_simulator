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
