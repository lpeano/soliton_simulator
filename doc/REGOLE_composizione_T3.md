# `T3` — **LE REGOLE DI COMPOSIZIONE**, attributo per attributo *(2026-09-28)*

> **Il principio, come l'ha dato Luca:** ### **ogni legge contribuisce una VARIAZIONE, e le variazioni
> si SOMMANO.** Un rilassamento verso un bersaglio contribuisce `alpha·(bersaglio − x)`; le grandezze
> derivate *(`psi`, `w`, il pozzo)* si calcolano **una volta dalla fotografia**; i vincoli si applicano
> **una volta dopo la somma**; la struttura è **una fase a parte**.
>
> ### 🛑 **NESSUN CODICE.** Blob del simulatore **`1fc9235f`**, prima e dopo.
> **Strumento:** `csv/_test_fork/_etc_sovrapposizione.py` *(blob `9b683cbf`)*, referto
> `_etc_sovrapposizione.json`.

---

# 1. IL CONTO: **94 scritture di stato, e 80 rientrano già nelle cinque forme**

| forma | n. | come si compone |
|---|---|---|
| **1 · variazione** | **19** | `x += d` / `x = x + d` → **si somma** |
| **2 · rilassamento** | **3** | `x + a·(bersaglio − x)` → **è una variazione** |
| **3 · derivata** | **12** | si ricalcola **una volta dalla fotografia** |
| **4 · vincolo** | **6** | si applica **una volta dopo la somma** |
| **5 · struttura** | **40** | **fase a parte**, dopo la dinamica |
| ### **ECCEZIONE** | ### **14** | ### **da decidere** |

## 1.1 — ⚠ **La scoperta che conta, e cambia la dimensione del lavoro di `T3`**

Al primo giro le eccezioni erano **16**; poi ho insegnato al classificatore a riconoscere gli **alias
locali**, e sono scese. **Il motivo è il punto:**

```
self.phivel = _phivel_t + delta_phivel        # :5592
self.phi    = (_phi_t + dt_n_s*self.phivel + delta_sync_phi) % self._dphi()   # :5593
self.d      = _smp_d_ini + self._smorza(_smp_d_ini, _dxd, 'd_passo')          # :5945
```

### **Il codice scrive GIÀ in forma «fotografia + variazione».** Solo che **la fotografia vive in una
VARIABILE LOCALE** — `_phivel_t`, `_phi_t`, `_smp_d_ini` — **invece che in un oggetto dichiarato.**

> ### 📌 **Quindi `T3` non è una riscrittura della fisica: è rendere ESPLICITO ciò che il codice fa
> già in tre posti e non fa negli altri.** E `:5945` è **letteralmente la forma modello**:
> `foto + freno(δ)`, cioè **`C3`**.

---

# 2. PER ATTRIBUTO: chi incrementa, chi assegna, in quali forme

| attributo | incrementa *(1,2)* | assegna pieno *(3, ECC)* | forme |
|---|---|---|---|
| `d` | `step` | `step` | 1 · 2 · 5 · ### **ECC** |
| `d0` | `memoria_hebbiana_moto`, `mitosi`, `step` | — | 1 · 5 |
| `phi` | — | — | 4 · 5 |
| `phi_s` | — | `_passo_spinoriale` | 5 · ### **ECC** |
| `phivel` | `scuoti_vuoto`, `step` | — | 1 · 5 |
| `psi` · `psi_spin` | — | `calcola_psi`, `step` | **3** |
| `_psi_spinor` · `_psi_prec` · `_spinor_lift` · `_nb_prec` | — | vari | 3 · 5 |
| `omega_s` | — | `_passo_spinoriale` | 5 · ### **ECC** |
| `_nb` | `_passo_spinoriale` | `_passo_spinoriale` | 1 · 4 · 5 · ### **ECC** |
| `eta` · `tw` | `step` | — | 1 · 5 |
| `twp` | — | `step` | 5 · ### **ECC** |
| `vd` | `step` | `step` | 2 · 5 · ### **ECC** |
| `peq` | `step` | `step` | 1 · 5 · ### **ECC** |
| `mem_mot` | `memoria_hebbiana_moto` | — | 2 · 5 |
| `perc_chi` · `perc_geom` | — | `step` | 5 · ### **ECC** |

> ### **Nessun attributo è incrementato da due leggi E assegnato pieno da una terza**, che era il caso
> peggiore possibile. **`d0` — il più scritto, da tre leggi — è `1 · 5` puro: si somma e basta.**

---

# 3. LE ECCEZIONI: **14, e leggendole sono TRE famiglie**

## 3.1 — ### ⚠ **FAMIGLIA A: le DECISIONI CATEGORIALI. Queste non si sommano, e la decisione è di Luca**

| sito | scrittura |
|---|---|
| `:5639` | `perc_geom[:n] = np.where(twn > soglia, 1, -1)` |
| `:5642` · `:5666` | `perc_chi[:n] = np.where(twn > soglia, 1, -1)` · `np.where(real(_ov) >= 0, 1, -1)` |

### **Sono SEGNI: `+1` o `−1`.** Non c'è nessuna variazione da sommare — **una legge DECIDE un segno.**
> ### **E la superposizione non si applica per costruzione:** se due leggi decidessero il segno dello
> stesso nodo, *«sommare le variazioni»* darebbe `+2`, `0` o `−2`, che **non sono valori ammessi**.
>
> **Oggi il problema non si manifesta**, perché le scrive **solo `step`** — ma **`:5642` e `:5666` la
> scrivono DUE VOLTE nello stesso passo**, e la seconda **sovrascrive** la prima.
> ### **Serve una regola, e non la scelgo io.** Le tre che vedo:
> **(i) l'ULTIMA VINCE** *(è il comportamento di oggi, e va solo dichiarato)*;
> **(ii) una sola legge ha il diritto di scriverla** *(e le altre propongono)*;
> **(iii) si compone per VOTO** *(il segno della somma dei contributi)* — **che è una legge nuova**,
> e `9-ter` chiede di non aggiungerne.

## 3.2 — ### ⚠ **FAMIGLIA B: le ROTAZIONI. Non compongono per SOMMA**

| sito | scrittura |
|---|---|
| `:3970` | `self.omega_s = omega_new.copy()` |
| `:3971` | `self._nb = nb_new.copy()` *(il Bloch, ruotato)* |
| `:3979` | `self.phi_s = np.arccos(np.clip(nb_new[:, 2], -1, 1))` |

**`_nb` è un VERSORE sulla sfera, e `nb_new` è `nb` RUOTATO** *(`nb·cosA + (ohat × nb)·sinA + …`)*.
### **Due rotazioni compongono per MOLTIPLICAZIONE, non per addizione.**
**`phi_s` è la sua coordinata polare** → è una **derivata** *(forma 3)*, e basta dichiararla tale.

> ### **Questa non è un'eccezione da sanare: è la FISICA del settore `SU(2)`.** Il `REGISTRO_FISICA`
> lo impone già — *«`SU(2)` nell'algebra di Lie»* — e **sommare due rotazioni infinitesime è
> legittimo, sommare due rotazioni finite no.**
> ### **Propongo una forma 6: `gruppo`** — *il contributo è un generatore, e si compone
> nell'algebra, non nei valori*. **Se `T3` non l'ha, il settore spinoriale resta fuori dalla
> sovrapposizione — e sarebbe un buco grosso.**

## 3.3 — ### **FAMIGLIA C: l'INIZIALIZZAZIONE DEI NATI. Manca una forma**

| sito | scrittura |
|---|---|
| `:5698` | `self.peq[nuovi] = rho[nuovi]` |

**Non è dinamica e non è struttura:** la struttura ha già creato l'arco, e qui gli si dà **il valore
di partenza**. ### **È la «voce di STATO» della mitosi**, quella che la strada (a) rinvia a `T3`.
> ### **Propongo una forma 7: `nascita`** — *si applica SOLO ai nuovi indici, dopo la struttura, e
> non partecipa alla somma*. **È anche la forma che serve per `psi`/`psi_spin` estese ai nati.**

## 3.4 — Le restanti **8**: non sono eccezioni, sono **limiti del classificatore**

| sito | forma vera | perché non l'ha vista |
|---|---|---|
| `:5750` · `:5756` `peq = self._peq_esatto(...)` | ### **2 · rilassamento** | è in forma **chiusa dentro un helper**: `peq ← rho + (peq−rho)·exp(−dt/τ)`. Lo dice il suo docstring |
| `:5620` · `:5624` `twp = self._w8(dph + twist_dip)` · `= dph` | ### **3 · derivata** | `twp` è **la differenza di fase avvolta**, ricalcolata ogni passo da `phi`: va aggiunta all'elenco delle derivate |
| `:5921` `vd = vd_half + 0.5·dts·acc_next` | **1 · variazione** | è la **seconda mezza-spinta del Verlet**: variazione attraverso un locale definito **dentro il ciclo** |
| `:5922` `d = d_new` | **1 · variazione** | idem, `d_new = d + dts·vd_half` |
| `:5945` `d = _smp_d_ini + _smorza(...)` | ### **1 + 4** | ### **è `C3`: foto + freno(δ)**, la forma modello |

### **Quindi le eccezioni VERE sono 6, in tre famiglie**, e due chiedono **una forma nuova**.

---

# 4. LA MITOSI: come si separano struttura e stato nel nuovo ordine

**La strada (a) l'ha rinviata qui**, e ora si vede **perché `T3` è il posto giusto**: la separazione
non è un taglio nel testo, è **un cambio di forma delle scritture**.

## 4.1 — L'ordine di oggi, e perché non si taglia

Misurato in `doc/MITOSI_non_si_spezza_per_tipo.md`: **struttura e stato si alternano 26 volte**, e il
blocco Schwinger **li intreccia nella stessa istruzione**. **Nell'ordine di oggi lo stato dei nodi
nati è scritto PRIMA della struttura degli archi.**

## 4.2 — L'ordine nuovo, in **quattro** fasi

| | fase | che cosa fa |
|---|---|---|
| **1** | **decisione** | sulla **fotografia**: quali archi si dividono (`sel`), dove nasce il figlio, se scatta l'antifase. ### **Nessuna scrittura** |
| **2** | **struttura** | crea nodi e archi: `i`, `j`, `n`, e **estende** tutti gli array *(forma 5)*. ### **I nuovi indici sono noti da qui** |
| **3** | **nascita** *(forma 7)* | dà ai **soli nuovi indici** il valore di partenza: `phi = fm`, `phivel = media dei genitori`, `eta = 0`, lo spinore ereditato, `d`/`d0` dei tronconi, `peq`, `tw = 0`, `twp` ricalcolata. ### **Non partecipa alla somma** |
| **4** | **derivate** | `psi` e `psi_spin` **solo per i nati** *(è la radice di `PSI-FLASH`)* |

## 4.3 — ⚠ **CHE COSA CAMBIA RISPETTO A OGGI, e va dichiarato**

| | |
|---|---|
| ### **la decisione si prende sulla fotografia** | oggi `mitosi` legge `tw`, `d`, `peq` **già mossi da `step`**. Domani legge la fotografia: ### **gli archi che si dividono possono essere DIVERSI** |
| **l'ordine di scrittura cambia** | struttura **prima**, valori di nascita **dopo**. Oggi è il contrario per i nodi. ### **Questo è il riordino, ed è il lavoro di `T3`** |
| **`psi` non si ricalcola per tutti** | oggi `:6731` la ricalcola **intera** quando `len(psi) < n`. Domani si **estende**. ### **È `PSI-FLASH`, e qui si chiude** |
| ### **il numero di nascite cambierà** | conseguenza della prima riga. ### **Si RIPORTA, non è un criterio di successo** *(come da piano)* |
| **e non ci sono clip nuovi** | la nascita **a `LAM`** resta `_nasce`, che è già un vincolo dichiarato |

> ### 📌 **E una cosa che la separazione REGALA:** con la struttura come fase distinta, **`H-ETC-2`
> può permutare TUTTE le dinamiche** invece delle sole due prima di `mitosi`. **Il presidio diventa
> più forte proprio grazie al riordino** — che è l'argomento per farlo in `T3` e non prima.

---

# 5. CHE COSA CHIEDO A LUCA

### **Solo le eccezioni, come da mandato. Sono tre decisioni.**

| | decisione |
|---|---|
| **①** | **le DECISIONI CATEGORIALI** (`perc_chi`, `perc_geom`): quale regola? **(i)** l'ultima vince *(oggi)* · **(ii)** una sola legge ha il diritto · **(iii)** voto sul segno *(legge nuova)* |
| **②** | ### **la forma 6, `gruppo`**, per le rotazioni di `SU(2)`: la accetti? **Senza, il settore spinoriale resta fuori dalla sovrapposizione** |
| **③** | ### **la forma 7, `nascita`**: valori di partenza dei soli nuovi indici, dopo la struttura, fuori dalla somma. La accetti? **Serve anche a `psi`/`psi_spin` dei nati** |

**E due cose che NON chiedo, perché sono letture del codice e non decisioni:** `twp` va negli
attributi **derivati**; `_peq_esatto` **è** un rilassamento in forma chiusa. **Le dichiaro e le
correggo nel classificatore quando `T3` parte.**

---

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`SCHED-PASSO` · `MITOSI-NON-DIVISA` · `ETC-PASSO` · `PSI-FLASH` · `H-ETC-2` · `9-ter` · `A1` · `A9`
