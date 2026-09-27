# `SCIOGLIMENTO` — perché `coer_campo` va da `0.999` a `0.20` in 120 passi

> **Mandato di Luca, 2026-09-27. SOLO MISURA: nessuna legge si tocca, nessuna cura si propone
> come fatta.** Ordine: **criteri PRIMA (un commit)**, poi le misure **a `pilota-prova1-stati`
> chiuso**. **Nessun file del run in corso si modifica finché gira** (`par.5`).
>
> **Ogni ipotesi ha un caso che DEVE fallire** (`P1-sexies`), e si riferisce per ipotesi:
> **confermata / smentita / non determinata**, coi **numeri** e le **barre fra semi**.

---

## 1. ✅ **CIÒ CHE È GIÀ VERIFICATO DAL SORGENTE** *(sola lettura, nessun run)*

### 1.1 `H1` **CONFERMATA (struttura)** — la scena NON tocca `phivel`

`_semina_masse_coerenti` scrive **due** cose sui nodi della regione, e basta:

```python
net.phi[idx]  = ph % net._dphi()
net.phi0[idx] = net.phi[idx]
```

**`phivel` non compare.** I nodi tengono il `phivel` della **semina** (`:2767`):
`normal(0, _CALORE_INIT)`, o `chi * normal(_CALORE_INIT, _CALORE_INIT*0.5)` col calore vettoriale.
**La scena mette i nodi IN FASE e li lascia con VELOCITÀ DI FASE CASUALI.**
*(Quanto pesi è `S1`: il fatto è accertato, la sua grandezza no.)*

### 1.2 `H2` **CONFERMATA (struttura)** — la coppia non legge la fase corrente

Al sito di chiamata (`:5194-5196`): `A = w * cos(phi0[i] - phi0[j])`, `z = exp(1j*_phi_t)`.
Nel ramo **`CAMPO_SPINORIALE + FORK_SU2`** *(quello del driver)* il ritorno è
`K_C * imag(conj(_a)*(_c00+_c01) + conj(_b)*(_c10+_c11))`: **`z` NON compare.**
`A` contiene **`phi0`**, la fase **iniziale**; `_psi_spinor` nasce da `_bloch_a_spinore(nb)`
(`:1957`), cioè dall'**azimut del Bloch**.

> ### 🎯 **`d(coppia)/d(phi) = 0` ESATTAMENTE, per struttura. Non è un effetto piccolo: è ASSENZA DI DIPENDENZA.**
> **⚠ Ma la guardia `len(_psi_spinor) >= n` decide quale ramo gira**, e il ramo di ripiego
> `K_C*imag(conj(z)*(mat(A)@z))` **dipende da `phi`**. **Quante volte tiene, nel run, è `S2b`.**

### 1.3 ❗ **LA RIDUZIONE AL LIMITE `(e^{i phi}, 0)` NON VALE NELL'INIZIALIZZAZIONE REALE**

| | |
|---|---|
| il limite **dichiarato** *(docstring, e di nuovo a `:4012`)* | `(e^{i phi}, 0)` — prima componente **di modulo 1, fase `phi`** |
| `_estendi_psi_spinor` **reale** (`:1952-1962`) | `(cos(th/2), sin(th/2) e^{i ph_Bloch})` — prima componente **REALE**, `phi` **non entra** |

**Coincidono solo se `th = 0`, e nemmeno allora** *(lì vale `1`, non `e^{i phi}`)*.
**È un REGIME DICHIARATO, non lo stato iniziale.** *(Quanto disti: `S2c`.)*

### 1.4 ❗ `H5` — **ANCHE `ritmo()` NON LEGGE `phi`**, e i due residui si separano

**Da dove prende la frequenza, nel run:** con `CAMPO_SPINORIALE` acceso, da **`psi_spin[:,0]`**,
**non** da `self.psi`. E `psi_spin = mat(w) @ (amp * _psi_spinor)` (`:4018-4020`) — cioè **dallo
spinore, che non contiene `phi`**. *(Il ramo `phi` esiste solo come **fallback** se `_psi_spinor`
manca: `:4016`.)*

**E i residui su `r_k` sono DUE, e vanno distinti:**

| | |
|---|---|
| **`A3` — CURATO** | la normalizzazione usa `median(\|f\|)` **del passo PRECEDENTE** (`_med_f_prec`), non dello stesso istante: il punto fisso `median(x) = 1` **per identità** è stato tolto |
| **`A2` — RESIDUO** | ma quella mediana è **GLOBALE**, su tutti i nodi: **`r_k` di una massa è misurato contro l'intero universo**, non contro il proprio vicinato |

### 1.5 ❗ `H4` — **il Kuramoto usa `pos` E il centro di massa GLOBALE**, e una parte si cancella

```python
cmv   = (self.pos[:n] * I2[:, None]).sum(0) / max(I2.sum(), 1e-9)   # centro di massa GLOBALE
r_cm  = norm(self.pos[:n] - cmv) + LAM * 0.5                        # <- `pos`
pozzo = I2.sum() / r_cm                                             # <- somma GLOBALE
prof_rel = pozzo / media_p                                          # media pesata sui VICINI
forza = (2/pi) * prof_rel * rinforzo_shear
```

**E qui va fatta una distinzione che il conto impone:**

* **`I2.sum()` SI CANCELLA in `prof_rel`** *(sta a numeratore e denominatore)*: quel residuo `A2`
  è **INERTE**. **Dirlo è ciò che distingue una lettura attenta da una frettolosa.**
* **`cmv` e `pos` NON si cancellano:** `r_cm` è la distanza dal **centro di massa globale**,
  calcolata sul **DISEGNO**. ### **Residuo `A3-DISEGNO` + `A2`, attivo.**

> **⚠ E il commento lì accanto dice *«Nessuna media globale entra nella legge locale»*** — riferito
> a `scala_shear_locale`. **È vero di quello e falso di `pozzo`**, che sta quattro righe sopra.
> **Non è una bugia: è un commento che parla di meno di quanto il lettore gli attribuisce.**

### 1.6 🎯 **IL QUADRO CHE NE ESCE — e va letto come struttura, non ancora come causa**

`phi` evolve **solo** per `phivel` e Kuramoto (`:5442`):
`self.phi = (_phi_t + dt_n_s*self.phivel + delta_sync_phi) % dphi`.
**La coppia non la legge** *(1.2)*; **`ritmo()` non la legge** *(1.4)*.
### **L'UNICA cosa che agisce su `phi` per riallinearlo è il Kuramoto — la cui forza passa da `pos` e dal centro di massa globale.**
**Questo è un fatto di struttura. QUANTO pesi, e se basti a spiegare `0.999 → 0.20`, lo dicono le
misure — e finché non le ho, non lo dico.**

---

## 2. PROGETTAZIONE — i criteri, **prima dei numeri**

**Tutto a run chiuso, su file NUOVI**, sugli stati `.npz` o su bracci corti separati.

| # | misura | conferma se | **il caso che DEVE fallire** |
|--:|---|---|---|
| **`S1`** | dispersione di `phivel` **dentro le masse al passo 0**, contro il suo **nullo** *(la dispersione nel VUOTO, non zero)* e contro `_CALORE_INIT = 0.4` | la dispersione è **dell'ordine** del tasso di sfasamento osservato | se fosse **nulla o trascurabile**, `H1` **cade** |
| **`S1b`** | **braccio corto, 40 passi, 4 semi:** i nodi di massa partono con **`phivel` = media della massa**, contro il braccio attuale. **La coerenza tiene?** | `coer_campo(40)` **risale** oltre la barra fra semi | **se NON risalisse**, `H1` da sola **non spiega** lo scioglimento |
| **`S2`** | su uno stato salvato: **perturba `phi` dentro una massa**, ricalcola la coppia. `max\|Δcoppia\|/eps` | **`0` ESATTO** *(non «piccolo»)* | **la CONTROPROVA che DEVE rispondere: lo stesso test sul ramo SCALARE** *(`CAMPO_SPINORIALE` spento)*, dove `d(coppia)/d(phi)` **deve** essere `≠ 0`. E il gemello: perturbare **`_psi_spinor`** → la coppia **deve** cambiare. Senza questi, uno zero vorrebbe dire *«non ho misurato niente»* |
| **`S2b`** | **quante volte la guardia `len(_psi_spinor) >= n` TIENE**, per passo | dice **quale ramo gira davvero** | se cadesse spesso sul ramo scalare, `H2` vale **solo per una frazione**, e **la frazione si scrive** |
| **`S2c`** | `\|<(e^{i phi},0) \| psi_spinor>\|` per nodo | **misura** quanto lo stato vero dista dal limite di 1.3 | — |
| **`S3`** | **`xi_termo` per passo**; **se `< 0` il termostato POMPA energia** | `xi_termo < 0` su una frazione non trascurabile | **il nullo:** `xi_termo` su un vuoto **senza masse**, stesso seme. Se fosse negativo **anche lì**, non è **delle masse** |
| **`S5`** | **`H5`** — dentro ogni massa, nei primi 40 passi, **scomporre lo sfasamento** nella parte da **dispersione di `phivel`** e in quella da **dispersione di `r_k`** | quale dei due domina | **`r_k` è uniforme dentro una massa?** Se lo fosse, la seconda parte è **zero** e la scomposizione è vuota — **si misura prima di scomporre** (`P4`) |

**`H4` non si progetta oltre la registrazione di 1.5:** il mandato dice *«da valutare solo dopo
`H1`»*.

### 2.1 ⚠ Le letture si fissano QUI

* **`S1b` NON richiede di modificare il simulatore** — e correggo ciò che avevo scritto prima:
  `phivel` si impone **nello script di test**, subito dopo `avvia_test(...)()`, con
  `net.phivel[idx] = media`. **Nessun file del simulatore viene toccato.**
* **ogni numero con la BARRA FRA SEMI** (`P3`, `t(3) = 3.182`), e **i nulli come LIMITI**;
* **`S2` è una derivata numerica**: si dichiara l'`eps` e si riporta `max|Δ|/eps`;
* **nessuna di queste misure tocca una legge.**

---

## 3. 📌 **L'ORIENTAMENTO DI LUCA — registrato, NON deciso, NON implementato**

> **Luca lo dichiara esplicitamente: NON è una decisione e NON si implementa prima delle misure.**
> **Sta qui perché chi legge il repo lo trovi**, non perché sia stato scelto.

1. **la fase come OROLOGIO:** `dphi/dt = omega0 * r_k + delta_k`, con `delta_k` *(l'attuale
   `phivel`)* come **eccitazione** — **nulla o quasi per una massa a riposo**;
2. **conta la differenza di `r_k` fra massa e vuoto** *(dilatazione del tempo)*, **non `omega0`**;
   **possibile origine della spinta come gradiente di fase**;
3. **una sola fase:** lo spinore porta `phi` come **fase globale** (`e^{i phi/2}`), così **coppia,
   ritmo e campo vedono la stessa `phi`**.

**Alternativa da tenere aperta:** `phi` come **onda con inerzia** *(tipo sine-Gordon)*; in quel caso
**basterebbe una condizione iniziale coerente**.

### **Le misure `H1`-`H5` devono dire QUALE di queste letture regge. Non lo decide questo documento.**

---

## 4. TODO

- [x] `H1` verificata dal sorgente; `H2` verificata **per struttura**; la riduzione al limite
      **non vale**; `H5` — `ritmo()` legge lo **spinore**, e i residui `A3`/`A2` su `r_k` separati;
      `H4` — `pos` + centro di massa globale, **con la parte che si cancella dichiarata**;
- [ ] `S1`, `S1b`, `S2`, `S2b`, `S2c`, `S3`, `S5` — **a run chiuso**, su file nuovi;
- [ ] il referto **per ipotesi**: confermata / smentita / non determinata, **coi numeri e le barre**;
- [ ] **nessuna cura**: la scelta è di Luca.

---

# 5. `H6` — **IL FLASH DI `|psi|` NEI PASSI CON NASCITE** *(rilievo del guardiano, 2026-09-27)*

> **Solo misura. Nessuna legge si tocca, nessuna cura si propone.**
> **Criteri PRIMA; l'arm strumentato è SOLA LETTURA.**

## 5.1 ✅ **IL FLASH È GIÀ MISURATO, dai fotogrammi salvati — e segue le NASCITE**

*(`max(phi_g)` e `mean(phi_g)` per fotogramma, seme 11. `phi_g ∝ |psi|²`.)*

| passo | `max(phi_g)` | `mean(phi_g)` | `n` | |
|--:|--:|--:|--:|---|
| 40 | `736.39` | `138.68` | `12802` | |
| **42** | ### **`1816.91`** | ### **`366.18`** | `12803` | **`n +1`** ← **prima nascita** |
| 44 | `710.50` | `139.72` | `12803` | rientra |
| 56 | `620.54` | `131.94` | `12803` | |
| **58** | **`1572.14`** | **`352.94`** | `12805` | **`n +2`** |
| 60 | `532.55` | `118.26` | `12806` | `n +1` **ma NON alto** |
| **62** | **`1499.33`** | **`346.58`** | `12811` | **`n +5`** |
| 64 | `1454.70` | `342.52` | `12814` | `n +3`, resta alto |
| 66 | `481.51` | `113.28` | `12816` | `n +2` **ma NON alto** |
| **68** | **`1359.20`** | **`333.97`** | `12822` | **`n +6`** |

> ### 🎯 **NON È UN PICCO LOCALE: È TUTTO IL CAMPO.** `mean(phi_g)` fa `138.7 → 366.2 → 139.7`,
> ### un fattore **`2.64`** su `|psi|²`, cioè **`1.62` su `|psi|`**, e torna indietro.
> **E il primo flash è ESATTAMENTE alla prima nascita** *(passo 42, `n: 12802 → 12803`)*.
> ⚠ **MA LA REGOLA «nascite → flash» NON BASTA:** ai passi `60` e `66` ci sono nascite e **il
> flash NON c'è**. **Quella è la cosa che la misura deve spiegare**, e finché non è spiegata
> l'ipotesi non è confermata.

## 5.2 ❗ **IL MECCANISMO CANDIDATO È NEL SORGENTE, ed è DOPPIO**

**Due punti ricalcolano `psi` con la STESSA guardia**, e girano **dopo** `mitosi()` *(che fa
crescere `n`)*, nello stesso passo:

```python
:6529  _togli_rotazione_rigida()      if not hasattr(self,"psi") or len(self.psi) < n: calcola_psi()
:6608  memoria_hebbiana_moto()        if not hasattr(self,"psi") or len(self.psi) < n: calcola_psi()
```

**L'ordine del passo è `… mitosi → rilassa_disegno → memoria_hebbiana_moto`.** Quindi:

* **passo SENZA nascite** → `len(psi) == n` → **nessuno dei due ricalcola**: `psi` resta quella di
  `step()`, calcolata col `w` di **inizio passo**;
* **passo CON nascite** → `len(psi) < n` → **RICALCOLA IL PRIMO CHE ARRIVA**, e `calcola_psi()`
  **senza `w`** rifà i pesi **sulla `d` CORRENTE** — cioè **dopo** mitosi e rilassamento.

### **Due `psi` diverse, a seconda di CHI arriva per primo. È esattamente la «lettura mista t/t+1» della nota `A8` del 17/9.**

**E i passi `60` e `66` sono il banco di prova**: hanno nascite e **non** flashano. **Se il
meccanismo è questo, deve esistere una differenza di PERCORSO** *(per esempio: `rilassa_disegno`
ha già ricalcolato, quindi `memoria_hebbiana_moto` trova `len(psi) == n` e non rifà nulla)*.
**Se quella differenza non c'è, l'ipotesi cade.**

## 5.3 I criteri

| # | misura | conferma se | **il caso che DEVE fallire** |
|--:|---|---|---|
| **`S6`** | per passo: `max(phi_g)`, `mean(\|psi\|²)` **dentro le masse** e **nel vuoto**, **nascite nel passo** | il flash è **globale**, non delle masse | se fosse **solo dentro le masse**, non è `psi`: è la scena |
| **`S6b`** | **`_calcpsi_origini`** — chi ha chiamato `calcola_psi` e **quante volte** — e **CHI PER ULTIMO**, per passo | identifica il meccanismo | **i passi SENZA flash DEVONO avere lo stesso ultimo chiamante**. **Se l'ultimo chiamante fosse lo stesso anche nei passi CON flash, `H6` è SMENTITA** |
| **`S6c`** | correlazione **flash ↔ nascite ↔ ultimo chiamante**, coi passi `60` e `66` **guardati uno per uno** | spiega le eccezioni | se `60` e `66` **non** si distinguessero per percorso, `H6` **non spiega i dati** |
| **`S6d`** | **`r_k` ai passi del flash** *(legame con `H5`)* | se il tempo proprio sobbalza | ⚠ **PREDIZIONE DA SORGENTE: col driver `ritmo()` legge `psi_spin`, NON `psi`** *(par.1.4)*. **Quindi un salto di `psi` NON dovrebbe muovere `r_k`.** **Se `r_k` sobbalzasse lo stesso**, la mia lettura di `ritmo()` è sbagliata e **va ritirata** |

### 5.4 Le letture si fissano QUI

* **l'ultimo chiamante si rileva avvolgendo `calcola_psi` SULL'ISTANZA** *(la stessa tecnica della
  `Spia`)*: **nessun file del simulatore viene toccato**;
* **`_calcpsi_origini` conta per SITO, non in ORDINE** — quindi **da solo non dice chi è stato
  l'ultimo**, e va detto invece di usarlo come se lo dicesse;
* **il flash si misura sul campo, non sui pixel:** il conteggio dei pixel saturi del guardiano è
  **il segnale**; `max(phi_g)` e `mean(phi_g)` sono **la grandezza**.

