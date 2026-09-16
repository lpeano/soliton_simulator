# REFERTO FASE A — L'INVENTARIO DEI SIGILLI, e due flag che sarebbero stati MUTI

> **2026-09-16.** Blob **`c57800c1`** (byte grezzi, 0 CRLF). Branch `fork-su2`.
> **Sola lettura del codice + un sigillo eseguito.** Nessuna accensione in questo referto.
> Criterio applicato: **§10 ②** — *una componente si accende solo se e' **sigillata con controllo
> positivo***. E il precedente che lo rende obbligatorio: il sigillo dello **Strato 1 si schiantava
> da due giorni** senza che nessuno lo sapesse. **Un sigillo che non gira non e' un sigillo.**

---

## 0. IL VERDETTO IN TRE RIGHE

> 1. **I 28 nomi di flag proposti ESISTONO tutti** nell'argv. Nessuno inventato, nessuno mancante.
> 2. **14 flag su 16 NON HANNO ALCUN SIGILLO.** Tier 2 e Tier 3 sono a **zero su dieci**.
> 3. **Passa solo `STEP2_OROLOGIO`** (9/10, col FAIL atteso). Tutto il resto **resta spento**.

---

## 1. I NOMI — verificati uno per uno dagli `add_argument`

Tutti e 28 esistono, con `dest` e `action=store_true`: `--campo-spinoriale`, `--spinore-vivo`,
`--spinore-corretto`, `--chi-core`, `--calore-scal`, `--deparam-orologio`, `--verlet`, `--fork-su2`,
`--fork-su2-mem`, `--cs-dinamico`, `--tau-luce`, `--rumore-colorato`, `--step2-orologio`,
`--tw-spinore`, `--ls-azim`, `--zeta-loc`, `--zeta-vir`, `--guscio-morbido`, `--plast-din`,
`--pav-com`, `--viriale`, `--chi-basc`, `--verso-chi`, `--olon-part`, `--polo-maturo`,
`--tempo-proprio-orientato`, `--spin-feedback`, `--chi-da-spinore`.

---

## 2. LA TABELLA DEI SIGILLI

| flag | sigillo che lo **TESTA** | gira sul blob? | controllo positivo | esito |
|---|---|---|---|---|
| **`STEP2_OROLOGIO`** | `_sigillo_step2.py` | **si', 9/10** | **si' — `S3.0`** | **ACCENDIBILE** |
| `RUMORE_COLORATO` | `_sigillo_rumore_colorato.py` | si' | si' (`N1b`, `N7b`) | **`N2` FAIL** -> spento |
| `TAU_LUCE` | `_sigillo_tau_luce.py` | si' | si' | **FAIL** (`T2`/`T3`/`T4`) |
| `TW_SPINORE` | **nessuno** | — | — | spento |
| `LS_AZIM` | **nessuno** | — | — | spento |
| `SPIN_FEEDBACK` | **nessuno** | — | — | spento |
| `ZETA_LOC` `ZETA_VIR` `GUSCIO_MORBIDO` `PLAST_DIN` `PAV_COM` `VIRIALE` | **nessuno (6/6)** | — | — | spenti |
| `CHI_BASC` `VERSO_CHI` `OLON_PART` `POLO_MATURO` | **nessuno (4/4)** | — | — | spenti |
| `TEMPO_PROPRIO_ORIENTATO` `CHI_DA_SPINORE` | **nessuno** | — | — | spenti |

**Criterio usato, e conta:** un flag e' **testato** solo se un sigillo lo **commuta** e confronta
(in un `extra=[...]`, o assegnandolo come globale). **Essere nella `BASE` argv di un sigillo NON e'
un sigillo di quel flag.** Con quel criterio `CAMPO_SPINORIALE`, `SPINORE_VIVO`, `VERLET`,
`CHI_CORE`, `DEPARAM_OROLOGIO` compaiono in **nove** sigilli **senza mai esserne il soggetto**.

*(Correzione alla mia stessa ricerca: `TAU_LUCE` risultava «nessuno» perche' il suo sigillo lo
accende con `carica(..., ["--tau-luce"])`, una forma che il pattern non prendeva. Verificato invece
di fidarmi del risultato.)*

### 2-bis. Lo Step 2 in dettaglio: **9/10, e il FAIL e' quello atteso**

```
[PASS] S3.0  l'orologio ha un contributo NON NULLO (il test VEDE)  39/40 nodi, |f(1)-f(0)| > 1e-13
[PASS] S3    omega_eff/omega_base = (cs/CS_M)^2                    max|mis - atteso| = 3.469e-18
[PASS] S3b   l'orologio RALLENTA dove cs e' basso                  0.0100 volte a cs = 0.1*CS_M
[PASS] S3c   a cs = CS_M il fattore e' 1 ESATTO                    1.000000000000000
[PASS] S2    ON (cs=CS_M) vs OFF: BYTE-IDENTICO                    0.000e+00, nodi 2924 = 2924
[PASS] S4a/b/c  |psi| = 1 (4.441e-16), nessun NaN, max|x| = 9.254
[FAIL] S1    flag OFF vs codice pre-cablaggio                      nodi 3164 contro 2924, 32 shape
```

> **`S1` FALLISCE contro il blob `2277e9a0`, che e' di QUATTRO cambiamenti fa** (cablaggio
> `tau-luce`, **C7**, **C11**, le due correzioni di difetto). **`max|A-B| = 0.000e+00` con nodi
> 3164 contro 2924 e' MANCANZA DI CONFRONTO**, non identita': e' la stessa classe di FAIL legittimo
> gia' documentata per `S1a`/`S1b` dello Strato 1.
> **E `S2` e' il confronto che CONTA e PASSA:** ON contro OFF sul codice **attuale**, `0.000e+00`
> con **2924 = 2924**, cioe' **il confronto ESISTE**. E' la riduzione al limite, sul blob di oggi.
> **Il sigillo si cita cosi': «9/10 + 1 FAIL ATTESO», MAI «10/10».**

---

## 3. ⚠ DUE FLAG CHE SAREBBERO STATI **MUTI**, e nessuno dei due lo dichiara

### 3.1 — **`VERSO_CHI` e' MORTO se `CHI_CORE` e' acceso**

```python
if FRAME_DRAG and len(_tw_t):                       # :2880   FRAME_DRAG = True
    if CHI_CORE and len(self.perc_chi) >= self.n:   # :2881   <- ARRIVA PRIMA
        twn = (pi*0.5*(chi_core[i] - chi_core[j])) / PHI_CRIT
    elif VERSO_CHI and len(self.perc_chi) >= self.n:  # :2884 <- MAI RAGGIUNTO
```

**`--chi-core` e' nella config base di OGNI run.** Quindi **accendere `--verso-chi` sarebbe un
NO-OP SILENZIOSO**: si crederebbe di aver aggiunto una legge e non si sarebbe aggiunto nulla.
**ESCE DALLA LISTA**, e resta scritto qui — *altrimenti fra un mese qualcuno lo riaccende credendo
di aver aggiunto una legge.*

### 3.2 — **Tre flag vivono DENTRO `if VIRIALE:`**, e non lo dicono

`LS_AZIM` (`:3744`), `ZETA_VIR` (`:3739`, nel ramo gravitazionale) e `OLON_PART` (`:3732`) stanno
**dentro `if VIRIALE:`** (`:3724`), a sua volta dentro `if GRAV_BIFASE and len(proj):`.
**Senza `--viriale` sono no-op muti.** *(`GRAV_BIFASE = True`, quindi quello non blocca.)*
**NB:** `ZETA_VIR` ha un **secondo** punto d'uso (`:3115`, `:3152`) dentro `if VERLET:`, che e'
acceso: **li' e' vivo anche senza `VIRIALE`.** Il flag e' quindi **parzialmente** condizionato —
il che e' peggio di esserlo del tutto, perche' meta' dell'effetto sparirebbe in silenzio.

### 3.3 — Conflitto **`CHI_BASC` / `CHI_DA_SPINORE`**, confermato

`:3017`: `if CHI_BASC and not CHI_DA_SPINORE`. **Si escludono a vicenda.** Nessuno dei due e'
sigillato, quindi oggi il punto non si pone — **ma la scelta e' di Luca quando si porra'.**

### 3.4 — ⚠ E UNA CORREZIONE A ME: **`ZETA_LOC` e `ZETA_VIR` NON si escludono**

Avevo sospettato che il secondo uccidesse il primo. **Verificato dal codice: falso.**
```python
if ZETA_M == 0.0:  beta = BETA_M
elif ZETA_LOC:     beta = 2*zeta_loc*cs/d      # sceglie COME si calcola beta
else:              beta = 2*ZETA_M*cs/d
...
if ZETA_VIR and _sin2_vir is not None:  beta = beta * (1 - sin2_vir)   # MODULA dopo
```
**Sono componibili.** *(E `ZETA_M = 0.75`, non 0, quindi il ramo di `ZETA_LOC` e' raggiungibile.)*

---

## 4. `TEMPO_PROPRIO_ORIENTATO` — il piu' pesante dei tre «separati»

Confermato a **`:1897`**: `f = signed if TEMPO_PROPRIO_ORIENTATO else np.abs(signed)`.

> **Spento, `ritmo()` prende il MODULO: `r` perde il SEGNO, e `dt_n = DT*r` e' POSITIVO per
> costruzione.** L'antimateria **non puo'** avere un orologio speculare, perche' il segno e'
> buttato via **a monte**.

**Non ha sigillo**, e **cambia la NATURA di `dt_n`**, non il suo valore: accenderlo renderebbe
**incomparabile** tutto lo storico. **Resta spento**, e quando si aprira' servira' — oltre al
sigillo — l'osservabile **frazione di nodi con `r < 0`**, che oggi sarebbe identicamente zero.

---

## 5. LA DECISIONE (Luca, 2026-09-16) — **UNO ALLA VOLTA**

> **Step 2 acceso (passa la FASE A) · `TW_SPINORE` sigillato e POI acceso · test a variabile singola.**

**Perche' non tutti e quattordici, con le parole del mandato stesso:** *«con ~15 leggi accese, un
cambiamento non e' attribuibile a una sola»*. **L'assenza di sigilli sta forzando la metodologia
migliore**, non impedendo il lavoro.

**Perche' `TW_SPINORE` per primo:** e' **l'unico meccanismo del sistema il cui asse NON svanisce
all'allineamento** — Kuramoto, Larmor e `cross(B,nb)` si annullano **proprio quando l'ordine
comincia** (il codice lo dice di Larmor: *«il difetto che spense SPIN_LARMOR»*). E' gia' a **zero
parametri** (`tw/2`, spin-1/2 geometrico, `PHI_CRIT` gia' nel sistema), il suo prerequisito
(`--spinore-vivo`) e' **gia' acceso**, e vive nello **stesso settore 4pi** dell'orologio che da ieri
gira davvero (**C11**).

**E `SPIN_LARMOR` resta spento per una ragione che va scritta:** **`TW_SPINORE` e' la sua CURA**
(asse `sigma` **fisso** dalla chiralita' del legame, **persistente** anche ad allineamento).
Accenderli insieme sarebbe **accendere il bug e la sua cura**. Il ramo di Larmor **non si cancella**:
e' l'evidenza che spiega perche' `TW_SPINORE` esiste.

---

## 6. LE ALTRE TREDICI — restano nel registro, sigillabili UNA ALLA VOLTA

`RUMORE_COLORATO` (serve solo correggere `N2` e aggiornare il riferimento) · `TAU_LUCE` (sigillo
FALLITO, voce **A** del registro) · `LS_AZIM` · `SPIN_FEEDBACK` · `ZETA_LOC` · `ZETA_VIR` ·
`GUSCIO_MORBIDO` · `PLAST_DIN` · `PAV_COM` · `VIRIALE` · `CHI_BASC` · `OLON_PART` · `POLO_MATURO` ·
`TEMPO_PROPRIO_ORIENTATO` · `CHI_DA_SPINORE`.
**`VERSO_CHI` NO: e' uscito dalla lista perche' e' MUTO sotto `CHI_CORE`** (§3.1).
