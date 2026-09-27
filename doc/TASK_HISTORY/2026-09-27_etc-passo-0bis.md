# `ETC-PASSO` — **SCHEMA A: FASE 0-bis, il progetto dettagliato** *(2026-09-27)*

> **Decisione di Luca:** *«SCHEMA A, TUTTO SIMULTANEO (Jacobi) su tutto il passo pieno.
> Strutturale, come `TEMPO_UNICO_MITOSI`. Base: la FASE 0 (`ae8d056`).»*
> **E la regola che governa tutto:** *«NESSUN CLIP. La cura non introduce clip, tetti, pavimenti
> o guardie numeriche di nessun tipo, nemmeno "temporanei".»*
>
> ### 🛑 **NESSUN CODICE DEL SIMULATORE È CAMBIATO.** Blob `e203f9a8` *(sha1 dei byte)*, prima e
> ### dopo. Questo commit porta **un solo strumento di misura nuovo** e **documenti**.

**Lo strumento:** `csv/_test_fork/_etc_progetto.py` *(blob sha1-BYTE `92fb2285`)*, referto
`_etc_progetto.json` *(`0c362f32`)*. **Il `.json` vecchio è stato CANCELLATO e rigenerato**, come
chiesto: non si riusa un referto che non viene dal sorgente accanto.

---

# 1. SCRITTURE CONCORRENTI

## 1.1 — **Tutte e 21 sono concorrenti. Nessuna esclusa.**

| attributo | leggi | siti per legge |
|---|---|---|
| `_nb` | 3 | `step`(6) · `mitosi`(1) · `memoria_hebbiana_moto`(1) |
| `d0` | 3 | `step`(4) · `mitosi`(4) · `memoria_hebbiana_moto`(12) |
| `phi` | 3 | `step`(1) · `mitosi`(5) · `memoria_hebbiana_moto`(1) |
| `phivel` | 3 | `scuoti_vuoto`(1) · `step`(1) · `mitosi`(2) |
| `psi` | 3 | `step`(11) · `rilassa_disegno`(2) · `memoria_hebbiana_moto`(2) |
| `psi_spin` | 3 | `step`(4) · `rilassa_disegno`(1) · `memoria_hebbiana_moto`(1) |
| `_nb_prec` `_psi_prec` `_psi_spinor` `_spinor_lift` `d` `eta` `mem_mot` `omega_s` `peq` `perc_chi` `perc_geom` `phi_s` `tw` `twp` `vd` | 2 | *(quasi sempre `step` + `mitosi`)* |

### **21 su 21 concorrenti, 0 scritte da una sola legge.**

## 1.2 — **Le 120 scritture, in cinque forme** *(il criterio è nel docstring dello strumento)*

| classe | siti | come si compone |
|---|---|---|
| **`A`** incremento *(`+=`, e `self.X = self.X + δ`)* | **20** | ### **SOMMA delle variazioni** — la regola di Luca, senza altro |
| **`A-bis`** mescola `(1-p)·X + p·E` | **1** | **è una variazione**: `δ = p·(E − X)`. Si somma come le altre |
| **`S`** estensione / troncamento strutturale | **40** | **non è una variazione**: è STRUTTURA, e va **dopo** *(par.2)* |
| **`C`** assegnazione indipendente dal corrente | **46** | variazione implicita `δ = nuovo − fotografia` |
| **`B`** vincolo sul valore corrente | ### **13** | ### **NON è una variazione — par.1.3, e qui mi FERMO** |

> ⚠ **Tre giri di correzione del criterio, e li dichiaro perché il numero è cambiato ogni volta:**
> **59 → 18 → 13**. Contavo come «non componibile» ① `np.concatenate([self.X, …])`, che è
> **estensione**; ② `self.X = self.X + δ`, che è **un incremento scritto come assegnazione**;
> ③ `…astype(self.perc_chi.dtype)`, che dipende dal **tipo** e non dal **valore**.
> **Il numero buono è 13**, e viene dal quarto criterio.

## 1.3 — 🛑 **LE 13 SCRITTURE CHE NON SONO VARIAZIONI. QUI MI FERMO: DECIDE LUCA.**

### **Gruppo ① — PAVIMENTI E CLIP: 8 siti. Sono quelli veri.**

| attributo | siti | il codice |
|---|---|---|
| **`d0`** | **7** | `self.d0 = self._pav_d0(self.d0)` → `np.maximum(v, self._floor_d0())` — `:5899` *(step)*, `:6157` *(mitosi)*, `:6664` `:6817` `:6840` `:6994` `:7042` *(memoria\_hebbiana\_moto)* |
| **`d`** | **1** | `:5782` `self.d = np.maximum(self.d + dts * self.vd, 0.05)` |

> ### **PERCHÉ NON SO DECIDERLO IO, ed è il punto:** sommare le variazioni e applicare il
> pavimento **una volta sola** *(a fine passo)* **non dà lo stesso risultato** che applicarlo
> **sette volte** durante il passo. **La differenza è fisica, non numerica:** oggi ogni legge
> vede `d0` già rialzato al pavimento dalla legge prima, e costruisce la propria variazione su
> **quel** valore. **Scegliere «una volta sola» è scegliere una legge diversa**, e la regola
> d'oro dice che una legge non la scelgo io.
>
> ### ⚠ **E LA REGOLA «NESSUN CLIP» NON RISOLVE QUESTO, lo rende più stretto.** Luca ha detto che
> la cura **non ne introduce**. Questi **c'erano già**. Ma la cura **non può non toccarli**: deve
> decidere **quante volte** girano. **Le uniche tre risposte che vedo sono tutte decisioni di
> teoria**, e le espongo senza sceglierne una:
> **(i)** il pavimento gira **una volta**, a fine passo, sul totale;
> **(ii)** gira **dopo ciascuna legge**, e allora il passo **non è Jacobi** su `d0` e `d`;
> **(iii)** il pavimento **non è un clip ma una legge** *(`A11`: «un limite è una legge»)*, va
> **derivato** e allora la domanda cambia forma.
> **Non ne scelgo nessuna.**

### **Gruppo ② — VINCOLI GEOMETRICI: 5 siti. Qui ho una lettura, e la espongo.**

| attributo | siti | il codice | **la mia lettura** |
|---|---|---|---|
| **`phi`** | **4** | `(self.phi[k] + δ) % self._dphi()` — `:6265` `:6266` `:6269` *(mitosi)*, `:7040` *(memoria)* | **la fase vive su un cerchio**: il `%` non limita, **rappresenta**. Sommare le δ e avvolgere **una volta** a fine passo è **esattamente equivalente** finché si somma prima e si avvolge dopo |
| **`_nb`** | **1** | `:3228` `self._nb = self._nb / max(‖_nb‖, 1e-9)` | **il Bloch è un versore**: la divisione è la **proiezione sulla sfera**. Sommare le δ e proiettare **una volta** è **più corretto** geometricamente di proiettare a ogni sotto-passo |

> **⚠ MA NON LE TOLGO DALLA LISTA, e dico perché.** Luca ha scritto *«normalizzazione»*
> **esplicitamente** fra ciò su cui mi devo fermare. E ha ragione anche sul `%`: *«una volta
> invece di quattro»* **cambia i numeri** — l'equivalenza che ho scritto vale sull'algebra, **non
> sul galleggiante**, e fra `mitosi` e `memoria_hebbiana_moto` ci sono leggi che **leggono `phi`
> nel mezzo**. **Quindi: le porto con una raccomandazione, non con una decisione.**

---

# 1-bis. `CLIP-INVENTARIO` — **i clip che ci sono già**

**Solo inventario. La cura (a) non ne tocca nessuno e non ne aggiunge.**
**117 guardie** nelle **59 funzioni** del percorso vivo del passo pieno, in **sei nature**, e la
natura si decide **dal POSTO, non dalla grandezza della costante** *(criterio confermato da Luca:
`np.maximum(self._deg, 1)` è una guardia, non un tetto)*:

| natura | n. | che cos'è |
|---|---|---|
| ### **`TETTO-FISICO`** | ### **27** | ### **limita il VALORE che una legge produce — SOLO questi sono tetti** |
| `anti-zero` | 48 | sta al **denominatore** di una divisione |
| `epsilon` | 19 | pavimento `≤ 1e-6`: guardia numerica *(il denominatore è spesso altrove)* |
| `parte-positiva` | 9 | `maximum(x, 0.0)` **esatto**: è la **forma di una legge**, non una guardia |
| `dominio` | 8 | argomento di `arccos`/`arcsin`/`sqrt`/`log`: **condizione di esistenza** |
| `selezione` | 6 | `maximum(A, B)` **senza costanti**: *sceglie* fra due grandezze, non limita |

**I 27 tetti fisici, per famiglia** *(l'elenco riga per riga è nel referto e nell'uscita dello
strumento)*:

| famiglia | dove |
|---|---|
| **pavimenti su `d` e `d0`** | `:5737` `:5782` *(`0.05`)*, `:4456` `_pav_d0`, `:4515` `_nasce` → `maximum(v, LAM)`, `:6368` |
| **clip sui PASSI di una legge** | `:6650` `proj`, `:6806` `spinta`, `:6812` `grav`, `:6835` `flusso`, `:6991` `coesione`, `:7037` `shift_fase` *(±π/4)*, `:5891` `_lap_d0` *(±CFL)* |
| **clip su grandezze in `[0,1]`** | `:5183` `_mcoer`, `:5234` `coerenza`, `:6006` `discesa`, `:6073` `rep`, `:3878` `ramp`, `:3613` |
| **il termostato** | `:5370` `clip(xi_termo, −2, 2)`, col commento che si autodichiara *«guardia»* |
| **il disegno** | `:6511` `clip(acc, ±0.5)`, `:6513` `nan_to_num(pos)` — **fuori dalla fisica** |
| **altri** | `:531` `:1762` `:3631` `:4872` `:5237` `:5601` `:6851` `:7018` |

> ### ⚠ **E IL RESIDUO DI IMPRECISIONE, che dichiaro invece di nasconderlo:** fra i 27 restano
> **tre pavimenti di GRADO** — `:1762`, `:5237`, `:6851`, tutti `maximum(deg, 1)` — che **sono
> guardie**, ma la divisione che proteggono sta **altrove** e lo strumento, che guarda il sito,
> **non può vederlo**. **Quindi «27» è un limite SUPERIORE dei tetti veri.**

---

# 2. MITOSI E ARCHI

## 2.1 — Quali grandezze sono **per arco**, e come lo so

**Lo snapshot `.npz` del pilota non basta** *(contiene `d`, `phi`, `i`, `j`, `n`, `pos`: **2** delle
21)*. Quindi la natura si legge **dal codice**, con un criterio del codice stesso: **la mitosi
estende con la maschera `keep` ciò che è per arco**.

| | attributi |
|---|---|
| **per NODO (13)** | `phi` `phi_s` `phivel` `eta` `perc_chi` `perc_geom` `mem_mot` `_nb` `_nb_prec` `omega_s` `_psi_spinor` `_psi_prec` `_spinor_lift` |
| **per ARCO (6)** | ### `d` `d0` `vd` `peq` `tw` `twp` |
| **non estesi dalla mitosi (2)** | ### `psi` `psi_spin` — **ed è la radice di `PSI-FLASH`** *(par.3.2)* |

## 2.2 — ✅ **Gli archi divisi NON hanno bisogno di una regola nuova**

**La domanda era:** *«cosa succede alle variazioni per arco degli archi che la mitosi divide?»*
**La risposta cade dall'ordine che Luca ha già fissato** — *prima le variazioni dinamiche, poi i
cambiamenti strutturali*:

1. la variazione `δ` dell'arco `e` si applica **mentre `e` esiste ancora**;
2. **poi** la mitosi lo divide, e le **regole di nascita di oggi girano sul valore GIÀ aggiornato**.

**E le regole di nascita di oggi sono quattro, diverse fra loro**, lette da `:6305-6318`:

| array | che cosa fanno i due figli |
|---|---|
| `d` | **si dimezza**: `[d[keep], dh, dh]` con `dh = d/2` |
| `d0` | idem, via `d0new` |
| `vd` `peq` | **si COPIANO** dall'arco padre: `[…, X[sel], X[sel]]` |
| `tw` | ### **si azzera** |
| `twp` | ### **si RICALCOLA dalla fase**: `_wphi(phi[a]−fm)`, `_wphi(fm−phi[b])` |

> ### **Nessuna delle quattro va cambiata, e nessuna nuova va inventata.** È il risultato che
> volevo dal punto 2: **l'ordine imposto da Luca rende la domanda vuota.**

## 2.3 — ⚠ **La conseguenza che invece NON è vuota, e va dichiarata**

**Le decisioni della mitosi — *dove* nascere — si prendono sulla FOTOGRAFIA**, come Luca ha
prescritto. **Quindi l'arco scelto può non essere quello che lo stato aggiornato sceglierebbe.**
**Non è un difetto: è esattamente ciò che «simultaneo» significa** — la mitosi decide su `t`, non
su `t+½`. **Ma cambia quali archi si dividono**, e va messo in conto quando si guarderà il numero
di nascite del sigillo.

---

# 3. I NATI

## 3.1 — Le regole di nascita, **lette dal codice** *(`:6225-6245`, `_eredita_spinore_figli`)*

| grandezza | regola di oggi |
|---|---|
| `phi` | `fm`, il **punto medio** *(con `+dphi/2` per la frazione in antifase)* |
| `phivel` | ### **media dei due genitori**: `0.5·(phivel[a] + phivel[b])` |
| `phi_s` | eredita dal genitore `a` |
| `eta` | ### **zero** |
| `perc_chi` `perc_geom` `mem_mot` | ereditano da `a` |
| lo **spinore** *(`_nb`, `_nb_prec`, `omega_s`, `_psi_spinor`, `_spinor_lift`, `_psi_prec`)* | `_eredita_spinore_figli(a, segno=1)` — **regola D**, dal genitore |

### **La cura NON tocca nessuna di queste.** Restano quelle di oggi, come da mandato.

## 3.2 — ✅ **`psi` e `psi_spin`: le sole due che la mitosi NON estende, ed è la cura**

**Misurato al par.2.1.** Poiché nessuno le estende, dopo la mitosi `len(psi) < n`, e allora
`memoria_hebbiana_moto:6608` fa `self.calcola_psi()` — **che le ricalcola TUTTE**, con i pesi
nuovi. **Quella `psi` entra in `pozzo_grafo` e quindi nella spinta `S09` dello stesso passo**:
è `PSI-FLASH`, e questa è la sua radice, non un difetto del diagnostico.

> ### **La cura, e non aggiunge una legge:** `psi` e `psi_spin` si **estendono come tutte le
> altre** — **calcolate solo per i nati, sul loro vicinato** — e i nodi preesistenti **conservano
> il valore della fotografia**. **Il numero delle leggi non aumenta** *(`9-ter`)*: si toglie
> un'**eccezione**, cioè le due grandezze che erano le uniche a non avere una regola di nascita.

---

# 4. CACHE

| cache | chi la costruisce | nella cura |
|---|---|---|
| `w` *(`_pesi()`)* | oggi, **dentro `calcola_psi` quando `w is None`** | ### **UNA volta dalla fotografia**, e si **passa**. `calcola_psi` senza `w` dentro `passo_pieno` = **errore** *(`H-ETC-1`)* |
| `psi` | `calcola_psi(w)` | una volta dalla fotografia, **più i nati** *(par.3.2)* |
| pozzo *(`pozzo_grafo`)* | da `I = |psi|²` | una volta, dalla `psi` della fotografia |
| `_deg` | `_grado()` | **si RICOSTRUISCE dopo il cambiamento strutturale** — la mitosi lo fa già a `:6319`. **Non si fotografa** |
| `_S` `_perm` | invalidate a `None` | si ricostruiscono a inizio del passo successivo |

---

# 5. NUMERI CASUALI

| legge | usi di `rng` |
|---|---|
| `scuoti_vuoto` | **1** |
| `step` | **7** |
| `mitosi` | **4** |
| `rilassa_disegno` · `memoria_hebbiana_moto` | 0 · 0 |

### **3 leggi su 5 consumano `rng`, per un totale di 12 siti.**
**Un flusso per legge, derivato da `(seme, passo, legge)`**, così che permutare l'ordine **non
cambi le estrazioni**. **Senza questo, `H-ETC-2` fallirebbe per il motivo sbagliato** — e il
fallimento sembrerebbe una prova di asincronia quando sarebbe solo un `rng` scorrevole.

> ⚠ **E va detto che questo CAMBIA I NUMERI anche a cura spenta**, perché sostituisce un unico
> flusso con tre. **Non c'è modo di renderlo byte-inerte**: o si permuta, o si conserva il flusso
> unico. **Lo dichiaro qui perché il sigillo non se lo trovi davanti come sorpresa.**

---

# 6. LE 56 LETTURE SPORCHE: dove vanno a finire

**Tabella generata dallo strumento**, incrociando il referto della FASE 0 con le quattro classi:

| destinazione dopo la cura | letture |
|---|---|
| ### **FOTOGRAFIA** | ### **36** |
| `CONTATORE VIVO` *(l'accumulo è il suo scopo — `A8`)* | 8 |
| `CACHE RICOSTRUITA` *(derivata, non si fotografa)* | 6 |
| `STRUTTURA VIVA` *(una nascita non si nasconde — `9-ter`)* | 4 |
| **FOTOGRAFIA, ma resta `A3-DISEGNO`** *(`pos`)* | 2 |

### **56 su 56 classificate. Zero non classificate.**

---

# 7. COSA SI ARCHIVIA *(decisione 3: si conserva tutto)*

| | |
|---|---|
| **un TAG** sul percorso sequenziale di oggi | prima di toccare una riga, così il *«come girava prima»* è recuperabile **per costruzione** *(par.7 di `CLAUDE.md`)* |
| **`SYNC_UPDATE` e i suoi rami parziali** | **restano nel codice**, e si **dichiarano** sorpassati: il suo raggio era `step` + `_passo_spinoriale`, **una legge su cinque** |
| **`--sync`** | diventa un **no-op ACCETTATO**: il flag continua a esistere, non fallisce, e **stampa che è assorbito** dalla cura. **Non si toglie** |
| il vecchio percorso | `csv/_archivio/`, con la riga d'inventario |

---

# 8. COSTO

**`n` e `m` REALI dallo stato del pilota** *(`stato_seme14_passo000120.npz`: `n = 13372` nodi,
`m = 469702` archi)*; **componenti e dtype letti dal costruttore** *(`:1673-1745`)*; l'aritmetica
è dello strumento.

### **La fotografia costa `26 182 880` byte = `24.97 MB`, UNA COPIA PER PASSO.**

| | |
|---|---|
| **`m/n = 35.1`** | il grafo è **molto più fitto di archi che di nodi** |
| ### **i 6 array PER ARCO sono `22 545 696` byte, cioè l'86 %** | `d` `d0` `vd` `peq` `tw` `twp`, `3.76 MB` ciascuno |
| i 15 per nodo | il 14 % restante |

> **IL TEMPO NON LO STIMO.** Dipende dalla banda di memoria della macchina, e **una stima
> inventata sarebbe peggio di nessuna stima**. Si misura quando la cura gira, non prima.

---

# TODO DEL NEXT STEP

> ### 🛑 **STOP. Il punto 1.3 è un bivio che non attraverso da solo.**

1. ### **Servono le decisioni di Luca sulle 13 del par.1.3** — le **8 di pavimento** in primo
   luogo, che sono quelle vere; le **5 geometriche** con la mia raccomandazione già scritta.
2. **Poi la FASE 1, un passo alla volta:** presidi → archiviazione → cura → sigillo.
   `H-ETC-2` **per primo e da solo**: se **passa** sul codice di oggi, mi fermo.
3. **`CLIP-INVENTARIO`** è una voce d'indice a sé: **la decide Luca dopo**, e **(a) non la tocca**.

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`ETC-PASSO` · `CLIP-INVENTARIO` · `H-ETC-1` · `H-ETC-2` · `PSI-FLASH` · `A3-DISEGNO` · `A11` · `A13`
