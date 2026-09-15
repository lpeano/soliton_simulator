# IL TERMINE MANCANTE? — smorzamento di Gilbert dal FDT. **FASE 1: analitico**

> **Scritto per Claude web.** Branch `fork-su2`, 2026-09-15. Blob sul disco **`f5887254`**
> (gate `CLAUDE.md` §0 su `c0803713`: disallineamento voluto, ramo turbo diagnostico).
> **Nessun codice toccato.** Nessun cablaggio: questa è la sola FASE 1.

---

## 0. IL VERDETTO IN UNA RIGA

> **L'ipotesi NON regge, ma non per il motivo per cui potrebbe non reggere: la diagnosi da cui
> parte è basata su due commenti STALE.** La dissipazione su `omega_s` **esiste già** (riga 1918) e
> il calcio termico **non alimenta** `omega_s` a ogni passo (è un colpo unico alla nascita).
> Derivando comunque il coefficiente di Gilbert dal FDT — e viene fuori **senza parametri** —
> risulta **3.8·10⁴ volte troppo lento**. **Terzo ramo della regola: reperto, non fallimento.**

---

## 1. PRIMA DI DERIVARE: le due premesse non reggono al codice

`CLAUDE.md` §0 impone di verificare dal **sorgente eseguibile**, non dalle annotazioni. Applicato:

### 1.1 «`omega_s` è conservativo: si conserva, non rilassa» — **FALSO**

I commenti lo dicono in **due punti**:
- riga **868**: *«MEMORIA HEBBIANA del momento angolare spinoriale (motore conservativo: si
  conserva, non rilassa)»*
- riga **1803**: *«omega si CONSERVA (non insegue lo zero)»*

Ma **l'unico** aggiornamento per passo di `omega_s` è la riga **1918**:

```python
omega_new = omega_src + dtn_c * (correzione / inerzia[:, None] - omega_src / _tau)
                                                                #  ^^^^^^^^^^^^^^^
```

> **Il termine dissipativo c'è, ed è un rilassamento del primo ordine con `tau = TAU_A · max(rho/rho_rif, 0.05)`.**

Verificato scorrendo **tutte** le occorrenze di `omega_s`: le uniche scritture sono
l'inizializzazione (867), l'eredità alla mitosi (1158), il calcio alla semina (1594), gli
adattamenti di lunghezza (1814-1816), lo snapshot sincrono (1834) e **il commit della 1918**
(riga 2088). Nessun'altra sorgente.

**Sono due commenti stale** — esattamente l'errore del docstring «ORFANO» che `CLAUDE.md` §0
impone di non ripetere. Vanno corretti nel file (proposta in §7).

### 1.2 «il calcio termico alimenta `omega_s`» — **FALSO: è alla nascita, non per passo**

Righe 1592-1594:
```python
if CALORE_VETTORIALE and _CALORE_INIT > 0:
    calcio_omega = self.rng.normal(0, _CALORE_INIT, (n, 3))
    self.omega_s = np.vstack([self.omega_s, calcio_omega]) ...
```
Sono **dentro `semina()`** (che inizia a riga 1555): è il **punto zero alla nascita del nodo**, una
volta sola. **Non** è una sorgente di rumore per passo.

> Quindi lo schema «accumulatore conservativo + sorgente di rumore che lo alimenta = crescita senza
> limite» **non descrive questo codice**: mancano entrambi i pezzi.

### 1.3 Dove il rumore entra DAVVERO

Il rumore per passo colpisce `self._nb` (riga **1847**, gated `SCUOTIMENTO and not SYNC_UPDATE`,
attivo nei run del fork), con ampiezza `amp = sqrt(Lam)/(1 + I2/Lam)`. Sotto `--spinore-corretto`
il `_nb` **committato** è ri-derivato da `_psi_spinor`, quindi quella perturbazione **non si
accumula sul Bloch**: entra in `omega_s` **solo** attraverso `correzione = cross(B, nb)`.

> **Il rumore è una PERTURBAZIONE DELLA COPPIA, non una forza stocastica su `omega_s`.**
> È il fatto già registrato in `CLAUDE.md` §9 il 2026-09-15.

---

## 2. LA LEGGE DI CRESCITA — misurata, non assunta

Il punto 2 del mandato chiede se il tempo di crescita torna. Con **un solo** campione di `|omega_s|`
non si distingue diffusivo da balistico: i due differiscono di due ordini. Serviva la **traiettoria**
(`csv/_test_fork/_crescita_omega.py`, pure-read, 150 passi, seme 1).

| n | `\|omega_s\|` | `omega/√n` | `omega/n` |
|---|---|---|---|
| 10 | 1.71e4 | 5404 | 1709 |
| 30 | 3.44e4 | 6273 | 1145 |
| 60 | 4.90e4 | 6327 | 817 |
| 100 | 6.39e4 | 6391 | 639 |
| 150 | 7.27e4 | 5937 | 485 |

> **`omega/√n` è costante entro il 4.6 %** su 15 punti; **`omega/n` varia di 3.5×.**
> **La crescita è DIFFUSIVA**, cioè un **random walk smorzato**, non una deriva coerente.

**Correzione a me stesso, dichiarata:** da un solo punto avevo dedotto crescita *balistica* (in
`doc/BILANCIO_ordine_spin.md` §6 non compare, ma era la mia prima lettura in sede di derivazione).
La traiettoria dice il contrario. **È il motivo per cui questa sonda è stata fatta prima di scrivere
il verdetto**, invece di ragionare su un punto solo.

---

## 3. E C'È UN PLATEAU — la dissipazione esistente **funziona**

Per un random walk smorzato l'equilibrio è `omega_eq = sigma·sqrt(tau/(2·dt))`:

```
sigma (incremento per passo, dal fit)   6314
tau/DT misurato (seconda meta' del run)  250 passi
omega_eq PREVISTO                       7.06e+04
omega MISURATO al passo 150             7.27e+04     -> scarto x1.03
```

E la **decelerazione si vede**: da n=100 a n=150 `omega` cresce ×1.138, mentre il puro `√n` darebbe
×1.225. Sta appiattendosi.

> **La dissipazione non manca: c'è, è efficace, e produce già un equilibrio finito.**
> Il problema è **dove** sta quell'equilibrio.

```
theta al plateau = omega_eq * dt_n = 705.9 rad = 4.05e4 gradi/passo = 112 GIRI per passo
```

**Nota collaterale** (stesso schema già visto altrove): nella seconda metà del run `tau/DT` vale
esattamente **250**, cioè `TAU_A · 0.05 / DT` — **è il PAVIMENTO** di
`max(rho/rho_rif, 0.05)` a fissare il tempo di dissipazione, non la densità. Un'altra
regolarizzazione che, alle scale simulabili, diventa il parametro fisico.

---

## 4. IL COEFFICIENTE DI GILBERT DAL FDT — **derivato, zero parametri**

Il mandato chiede di ricavarlo, non di sceglierlo. Si ricava, e **i parametri si cancellano**.

**La sorgente** (riga 1847): `nb <- normalizza(nb + xi·amp)`, con `xi ~ N(0,1)^3`. Le due componenti
**trasverse** danno uno spostamento angolare per passo con `<dtheta^2> = 2·amp^2`, quindi una
**diffusione angolare**

```
D = 2 · amp^2 / dt
```

**Il rilassamento di Gilbert** allinea `n` a `B`: `dtheta/dt = -lambda·theta + rumore`.
Due condizioni di equilibrio che devono coincidere:

```
Langevin:  <theta^2> = D / (2·lambda)
Boltzmann: <theta^2> = 2·kT / |B|          (potenziale U = -|B|·cos theta, due gradi di liberta')
=>         lambda = D·|B| / (4·kT) = amp^2 · |B| / (2 · dt · kT)
```

**La temperatura.** L'unica scala parameter-free è `Lam`, l'energia del vuoto — **la stessa da cui
il rumore è costruito**. Ponendo `kT = Lam` e usando i valori **misurati** al passo 150
(`Lam = 1.32e-4`, `amp = 0.0115`, quindi `amp^2 ≈ Lam`):

> **lambda = |B| / (2·dt) = 3.47 / tempo  ->  tempo di allineamento 1/lambda = 28.8 PASSI**

`Lam` **si cancella**: il coefficiente non dipende dall'energia del vuoto. Con la stima di vuoto
puro (`amp = sqrt(Lam)/2`, cioè `amp^2 = Lam/4`) verrebbe `lambda = |B|/(8·dt)` → **115 passi**.
**I due differiscono di 4×, e non cambiano il verdetto.**

---

## 5. IL CONFRONTO CHE DECIDE — la regola era scritta PRIMA

| tempo | valore |
|---|---|
| `dt_n` | 0.01 (un passo) |
| `tau_crescita` — a raggiungere il plateau | ~150-250 passi (misurato: sta appiattendosi a 150) |
| `tau_smorzamento` — allineamento FDT **derivato** | **28.8 passi** (115 con la stima di vuoto) |
| `tau_disordine` — rimescolamento **misurato** | **0.0030 passi** |
| `theta` al plateau | **4.05e4 gradi/passo = 112 giri** |

**Prima lettura — il termine come smorzamento su `omega` (è ciò che il mandato chiede):**
poiché `omega_eq` va come `sqrt(tau)`, per scendere sotto i 30 gradi/passo servirebbe un `tau`
**più piccolo di 1.8·10^6 volte** (da 250 passi a 1.4e-4 passi). Il FDT **non lo licenzia**: per
giustificare quello smorzamento il rumore dovrebbe essere più forte dello stesso fattore, e non lo è.

**Seconda lettura — il termine come allineamento su `n` (la forma corretta di LLG):**
`1/lambda = 28.8 passi` contro un rimescolamento di `0.0030 passi`:

> **lo smorzamento FDT è ~10^4 volte più lento del disordine che dovrebbe combattere.**

Entrambe le letture cadono nello **stesso ramo della regola del punto 4**:

> ### `tau_smorzamento >> tau_crescita` → lo smorzamento FDT è **troppo debole**. **REPERTO, non fallimento.**

---

## 6. CONTROLLO DI CONSISTENZA — il punto 5 del mandato

Se il settore di spin fosse in **equilibrio termico** con momento d'inerzia `I = 1e-6`,
l'equipartizione `(1/2)·I·<omega^2> = (3/2)·kT` darebbe, per il `|omega|` misurato:

```
kT = I·omega^2/3 = 1e-6 · (4.9e4)^2 / 3 = 800
Lam (energia del vuoto) al passo 60      = 4.4e-5
kT / Lam                                  ~ 2e7
```

> **Non è un equilibrio termico:** la "temperatura" implicita è ~10^7 volte l'energia del vuoto che
> genera il rumore. È un **equilibrio DINAMICO pilotato** — un random walk smorzato alimentato da una
> coppia grande — non un bagno termico. Ed è la ragione strutturale per cui il FDT non può fissare il
> coefficiente giusto: **il FDT accoppia una dissipazione a una FLUTTUAZIONE, e qui il termine
> dominante non è una fluttuazione.**

---

## 7. COSA DICE DAVVERO IL REPERTO, e cosa NON dice

**La diagnosi corretta resta quella già registrata** in `CLAUDE.md` §9 e
`doc/BILANCIO_ordine_spin.md` §6.1: `omega = coppia/inerzia` è enorme perché **l'inerzia è la
densità, e vale ~1e-7**. La dissipazione c'è e funziona; il plateau che produce è alto perché
**l'ingresso** è alto, non perché **l'uscita** manchi.

**Non è un fallimento dell'idea di Gilbert.** Il termine LLG è l'**unico** termine che allinea, ed è
strutturalmente il candidato giusto per un "Kuramoto emergente". Quello che la FASE 1 dice è che
**alla scala attuale il suo coefficiente FDT è irrilevante**, e che metterne uno più grande
significherebbe **sceglierlo** — cioè violare §3 (zero manopole) e, peggio, mettere dissipazione
senza fluttuazione: lo stesso errore, ribaltato.

**Due cose che questo NON tocca:**
- i sei lati restano come sono: tre sono **dimostrazioni algebriche** (teorema di inerzia,
  invarianza del Bloch sotto Step 2, FDT dello scuotimento) e non dipendono da nulla di questo;
- il cablaggio **non è stato fatto** e non va fatto: la FASE 1 non conferma.

**Proposta minima e separata** (un commit suo, se la vuoi): correggere i **due commenti stale** alle
righe **868** e **1803**, che dicono che `omega_s` non rilassa mentre la riga **1918** lo rilassa.
È il difetto che ha fatto partire questo mandato da una diagnosi sbagliata.

---

## 8. SE SI VOLESSE COMUNQUE USCIRE DALL'ALIASING — le leve vere, in ordine di onestà

1. **Alzare l'inerzia**, cioè lavorare dove la densità è O(1). Toglie la causa, non il sintomo, e
   riallinea con l'altra faccia dello stesso problema (`cs` morto a queste densità).
2. **Risolvere il tempo dello spin** con un sotto-passo tipo `nsub`. Il mandato lo chiama sintomo e
   ha ragione, ma con la crescita **diffusiva e con plateau** qui misurata il numero di sotto-passi
   **non diverge**: servirebbero ~`theta/2pi` ≈ 112 sotto-passi a plateau costante, non "sempre di
   più". È un presidio numerico onesto, non una cura.
3. **Gilbert con coefficiente scelto**: efficace ma **fuori regola** (§3). Se mai, va dichiarato per
   quello che è — una manopola — non spacciato per derivato dal FDT.

---

## 9. COSA NON È STATO TOCCATO

`soliton_simulator.py` **non è stato modificato**: blob `f5887254`, `git status` pulito, nessun flag
nuovo. `csv/_test_fork/_crescita_omega.py` legge solo array di stato e ricalcola `Lam` in locale con
la formula di `lambda_vuoto`, invece di chiamarla, perché quella invocherebbe `calcola_psi()` e
muterebbe la cache.

**Difetto della sonda, dichiarato:** nella prima esecuzione la colonna era etichettata `|F| med` ma
stampava l'**inerzia**. Etichetta corretta nel file committato; il numero era giusto, il nome no.
