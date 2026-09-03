# Come interpretare i dati — Campagna `spinore-vivo`

Guida di lettura per la campagna A/B prodotta da `test_spinore_vivo.bat`.
Scopo: capire se, riattivando l'evoluzione SU(2) (`--spinore-vivo`), il settore
non-abeliano produce una **precessione di spin coerente** (segnale vero) oppure
solo **disordine frustrato** (rumore non-abeliano), e se tocca la circolazione
orbitale. Tutte le misure sono passive e gauge-invarianti (nessuna coordinata).

> **Disciplina (obbligatoria prima di concludere).** Non concludere sotto ~2000
> passi: sotto è formazione, non dinamica. Non concludere da un solo seme: un
> effetto è sistematico solo se concorde sui semi 1 e 2. Distinguere sempre i
> livelli: **dimostrato** (robusto, ripetibile), **in verifica** (segnale ma non
> solido), **aperto** (non ancora testato).

---

## 1. I run della campagna

Un flag = una variabile: le braccia differiscono **solo** per `--spinore-vivo`.

| File diaglog | Config | Spinore | Seme |
|---|---|---|---|
| `m2_on_s1.csv`   | binario, base minima (`--verlet --sync`) | **VIVO** | 1 |
| `m2_on_s2.csv`   | binario, base minima | **VIVO** | 2 |
| `prec_on_s1.csv` | binario, catena precessione piena (`--viriale --ls-azim …`) | **VIVO** | 1 |
| `prec_on_s2.csv` | binario, catena precessione piena | **VIVO** | 2 |
| `m2_off_s1.csv`   | binario, base minima | congelato (baseline) | 1 |
| `prec_off_s1.csv` | binario, catena precessione piena | congelato (baseline) | 1 |

- **ON** = spinore reinnestato (evoluzione SU(2) viva). **OFF** = spinore
  congelato all'init planare (comportamento canonico attuale).
- L'OFF è **confermativo** (baseline appaiata, un solo seme): serve solo come
  riferimento a una variabile. L'informazione sta negli ON.

---

## 2. Le grandezze e come leggerle

### 2.1 Fase di Berry sui cicli — il canale non-abeliano
Invariante di Bargmann–Pancharatnam sui cicli del grafo (curvatura SU(2)).

| Colonna | Cosa misura | Lettura |
|---|---|---|
| `berry_spin_media` | media **firmata** di $\gamma_C$ | **il discriminante**: ≠0 = coerente; ~0 = incoerente |
| `berry_spin_media_assoluta` | media di $|\gamma_C|$ | intensità grezza (alta anche nel disordine) |
| `berry_spin_rms` | radice quadratica media | ampiezza delle fluttuazioni |
| `berry_spin_max` | picco sul ciclo peggiore | valore estremo (poco robusto) |

- **OFF**: tutte ≡ 0 (Bloch coplanari) — è la verifica che la baseline è pulita.
- **ON**: se `berry_spin_media` firmata è ≠0 e stabile → curvatura **coerente**.
  Se solo `_media_assoluta`/`_rms` sono alte ma la **firmata ~0** → i segni si
  cancellano = **disordine frustrato**, non circolazione.
- **Rapporto chiave**: `berry_spin_media` (firmata) / `berry_spin_media_assoluta`.
  Vicino a 1 = coerente; vicino a 0 = incoerente.

### 2.2 Ordine dello spinore — `spin_cluster_modulo` ($S_M$)
$S_M=\left|\frac1N\sum_i\mathbf n_i\right|$, modulo della media dei vettori di Bloch.

- $S_M\to1$: spin **ordinati** (allineati o in precessione collettiva).
- $S_M\to0$: spin **sparsi** sulla sfera = frustrati.
- OFF: $S_M=1$ (tutti identici, congelati). ON: il valore vero.
- È indipendente dall'embedding e complementare a Berry: $S_M$ vede l'ordine
  globale, Berry vede la curvatura sui cammini.

### 2.3 Tasso di precessione — `spin_cluster_omega` ($\omega_S$)
Angolo spazzato per passo dalla direzione media $\hat{\mathbf S}=\sum\mathbf n_i/|\sum\mathbf n_i|$.

- Significativo **solo se $S_M$ è alto** (direzione media ben definita).
- $S_M$ alto **e** $\omega_S$ stabile ≠0 → **precessione di spin coerente**: è il
  segnale che cerchiamo.
- Se $S_M$ è basso, $\omega_S$ è la rotazione di una direzione mal definita →
  **non significativo**, ignorarlo.

### 2.4 Olonomia di fase — `olonomia_fase_*`
$\oint_C\mathrm d\phi$ sui cicli: componente armonica del settore U(1) (vortici).

- Vive nel campo di fase, **indipendente dallo spinore**. Atteso simile ON e OFF.
- Se cambia molto ON vs OFF, è un accoppiamento inatteso spin→fase da indagare.

### 2.5 Circolazione orbitale — `circolazione_topologica_*`
Corrente d'arco sui cicli. Atteso ~0 (twist curl-free).

- Se resta ~0 anche ON → lo spinore vivo **non** genera corrente orbitale
  (l'eventuale segnale è nello spin, non nell'orbita).
- Se diventa ≠0 coerente ON → l'orbitale si accende: risultato forte, da
  verificare con cura.

### 2.6 Proxy dell'espansione — `d0_mean`, `dens_g0`
Il sistema si dilata (`d0_mean` cresce). Servono a controllare che i trend di
Berry/$S_M$ non siano **artefatti dell'espansione**.

- Correlare `berry_spin_media`/`S_M` con `d0_mean` (metrica) e `dens_g0` (densità).
- Correlazione **debole** ($|r|<0.3$) → il segnale è intrinseco, non diluizione.
- Attenzione: la correlazione **istantanea** non cattura accoppiamenti **ritardati**
  (l'espansione è monotòna, Berry oscilla). Per chiudere: berry(t) vs
  espansione(t−τ) sui run completi.

### 2.7 Solo Part 2 (precessione): `Lz_orb_01`, `m0_Lz`
- `Lz_orb_01`: variazione dell'angolo della congiungente = **precessione orbitale
  candidata**. Dipende dalle posizioni.
- `m0_Lz`: rotazione dell'asse PCA della massa — **dipende dall'embedding**
  (rotazione spuria possibile).
- **Confronto decisivo**: `m0_Lz` grande ma $\omega_S$/`berry_media` ~0 → la
  "rotazione" è il **dito** (embedding). $\omega_S$/`berry_media` ≠0 coerente →
  è la **luna** (spin che precede davvero).

---

## 3. La tabella che decide (coerente vs frustrato)

Da leggere sull'**ultimo terzo** dei run ON completi (2000 passi), concorde sui 2 semi.

| $S_M$ | `berry_media`/`berry_absmed` | $\omega_S$ | Conclusione |
|---|---|---|---|
| alto (→1) | ~1 (firmata ≈ abs) | ≠0 stabile | **Precessione di spin coerente** — la luna ruota. Segnale non-abeliano vero. |
| basso (→0) | ~0 (firmata ≪ abs) | irrilevante | **Frustrato** — `|berry|` alto è disordine, non circolazione. Teorema vero: canale presente ma frustrato. |
| alto | ~1 | ~0 | **Ordine congelato** — spin allineati ma non ruotano. Curvatura statica. |
| →1 congelato | 0 | 0 | Riga OFF (baseline): conferma solo che la baseline è pulita. |

---

## 4. Il confronto ON vs OFF (il debito di ritrattazione)

Oltre al discriminante, confrontare le leggi "dimostrate" (densità, coerenza,
metrica, `Lz_orb`) tra ON e OFF appaiati:

- **Identiche** ON vs OFF → le leggi **non dipendono** da SU(2): lo spinore vivo
  non le cambia (buona notizia per la robustezza).
- **Diverse** → quelle leggi dipendevano dallo spinore congelato: vanno rimisurate
  e le conclusioni precedenti riviste.

---

## 5. Riassunto operativo

1. Aspetta i 4 run ON completi (2000 passi).
2. Guarda `S_M`, `berry_spin_media`/`_media_assoluta`, `omega_S` sull'ultimo terzo,
   su **entrambi** i semi.
3. Applica la tabella §3 → coerente, frustrato o congelato.
4. Controlla la covarianza con l'espansione (§2.6) prima di attribuire un trend.
5. Part 2: confronta $\omega_S$/`berry_media` (gauge-inv) con `m0_Lz`/`Lz_orb`
   (embedding) → luna o dito.
6. Etichetta ogni conclusione: dimostrato / in verifica / aperto.

---

## 6. Risultati misurati (esecuzione del 2026-09-03)

Campagna interrotta prima del completamento: disponibili `m2_on_s1` e `m2_on_s2`
**completi** (2000 passi), `prec_on_s1` **parziale** (~467 passi), baseline OFF non
ancora eseguite. Lettura sull'ultimo terzo e andamento per quarti.

### Dati

| Run | $S_M$ (per quarti) | $\omega_S$ (per quarti) | berry firm/abs |
|---|---|---|---|
| `m2_on_s1` (2000) | 0.29 → 0.51 → 0.53 → **0.61** | 0.81 → 0.42 → 0.26 → **0.17** | +0.005 |
| `m2_on_s2` (2000) | 0.38 → 0.51 → 0.56 → **0.63** | 0.68 → 0.30 → 0.29 → **0.21** | −0.005 |
| `prec_on_s1` (467, parziale) | 0.23 → 0.32 → 0.63 → **0.66** | 0.25 → 0.21 → 0.08 → **0.06** | +0.03 |

Soglia di rumore casuale $S_M \sim 1/\sqrt N \approx 0.02$ (N ~ 2500 spin) →
$S_M \approx 0.6$ è **~30× sopra il rumore**.

### Conclusioni con livello di certezza

- **[DIMOSTRATO] Ordine di spin parziale emergente.** $S_M$ cresce in modo
  **monotòno e riproducibile** su entrambi i semi (→ 0.60–0.63), ~30× sopra il
  rumore. Lo spinore vivo **non si frustra a zero**: costruisce una polarizzazione
  netta. Non è sincronizzazione piena ($S_M \ne 1$), ma ordine genuino.

- **[IN VERIFICA] La precessione RALLENTA, non è stazionaria.** $\omega_S$
  **decresce monotòno** in tutti i run (s1: 0.81→0.17; s2: 0.68→0.21; prec:
  0.25→0.06). I decrementi si riducono (possibile asintoto), ma a 2000 passi
  $\omega_S$ **sta ancora calando** — non un plateau. Quindi: mentre l'ordine
  $S_M$ si costruisce, la direzione media **si stabilizza e rallenta**. Aperto se
  $\omega_S$ tenda a un valore piccolo ≠0 (precessione lenta stazionaria) o a 0
  (ordine che si congela). Nel run di precessione piena tende più verso 0.
  *Nota: una precedente lettura a run parziale suggeriva un "plateau ~0.18"; il
  trend per quarti la corregge — è un declino, non un plateau.*

- **[DIMOSTRATO negativo] La curvatura sui cicli è incoerente.** `berry_firm/abs`
  ~0 in tutti i run e **il segno flippa tra i semi** (+ vs −): la fase di Berry
  sui cicli locali è rumore, non segnale. La coerenza (se c'è) è **globale**
  (in $S_M$), non nella tessitura locale.

- **[DIMOSTRATO negativo] Handedness del transiente.** Il segno di $\omega_S$ è
  **positivo in tutti e tre i run** (verso concorde). Ma poiché $\omega_S$
  decade, è la chiralità di un transiente di ordinamento, non di una precessione
  sostenuta.

### Sintesi

Riacceso il settore SU(2), emerge un **ferromagnete di spin parziale** ($S_M\sim0.6$,
robusto) la cui direzione media **precede rallentando** ($\omega_S$ in declino, verso
concorde). **Non** frustrazione (S_M non crolla), **non** precessione stazionaria
confermata (omega non fa plateau a 2000 passi), **non** coerenza sui cicli locali.
Restano aperti: il destino asintotico di $\omega_S$, le baseline OFF appaiate, e il
confronto Part 2 con `m0_Lz` (spin che precede vs asse orbitale che ruota).
