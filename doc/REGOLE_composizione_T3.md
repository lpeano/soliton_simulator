# `T3` — **LE REGOLE DI COMPOSIZIONE**, attributo per attributo *(2026-09-28)*

> **Il principio, come l'ha dato Luca:** ### **ogni legge contribuisce una VARIAZIONE, e le variazioni
> si SOMMANO.** Un rilassamento verso un bersaglio contribuisce `alpha·(bersaglio − x)`; le grandezze
> derivate *(`psi`, `w`, il pozzo)* si calcolano **una volta dalla fotografia**; i vincoli si applicano
> **una volta dopo la somma**; la struttura è **una fase a parte**.
>
> ### 🛑 **NESSUN CODICE.** Blob del simulatore **`1fc9235f`**, prima e dopo.
> **Strumento:** `csv/_test_fork/_etc_sovrapposizione.py` *(blob `d0c8e951`, era `9b683cbf`)*,
> referto `_etc_sovrapposizione.json`.

> # ✅ **AGGIORNATO il 2026-09-28 con le DECISIONI DI LUCA**
> **Le tre decisioni sono arrivate**, e questo documento le **recepisce**. ### **Le eccezioni sono
> ZERO:** tutte e 94 le scritture rientrano ora in **una forma dichiarata**.
>
> | | decisione |
> |---|---|
> | **①** | ### **le decisioni categoriali NON sono un'eccezione:** la regola *«UNA SOLA legge scrive ogni grandezza-segno»* è ### **già vera per costruzione** *(è la cura di `A6-PERCCHI`)*. **Si DICHIARA, non si cura, e non si archivia niente** |
> | **②** | ### **forma 6 `gruppo`: ACCETTATA** |
> | **③** | ### **forma 7 `nascita`: ACCETTATA** |
>
> ### 📌 **E le sezioni sbagliate NON sono state riscritte: sono ANNOTATE.** Quello che credevo
> prima di guardare resta leggibile col ✗ accanto, e la correzione sta sotto. *(Un documento
> riscritto a posteriori è una ricostruzione, non un impegno.)*

---

# 1. IL CONTO: **94 scritture di stato, e ora le ECCEZIONI sono ZERO**

> ### 📌 **Le due tabelle stanno in `doc/REGOLE_composizione_T3_tabelle.md`, e sono GENERATE.**
> Non le ricopio qui: **un numero ricopiato a mano non ha provenienza, uno generato ce l'ha**
> *(`L-NUMERI`)*. Le scrive lo strumento stesso a ogni giro.

**Com'è cambiato il conto** *(prima → dopo le decisioni e le correzioni)*:

| | prima | dopo |
|---|---|---|
| **ECCEZIONE** | **14** | ### **0** |
| **1 · variazione** | 19 | **22** |
| **2 · rilassamento** | 3 | **6** |
| **3 · derivata** | 12 | **14** |
| **6 · gruppo** | — | **2** |
| **7 · nascita** | — | **1** |
| **0 · segno** | — | **3** |

**`4 · vincolo` resta 6 e `5 · struttura` resta 40**, e ### **il totale resta 94**: nessuna
scrittura è apparsa o sparita, **si sono solo spostate di casella**.

## 1.0 — ⚠ **Due correzioni al classificatore che NON sono fra quelle chieste da Luca**

**Le dichiaro perché cambiano dei numeri**, e se il criterio non regge **si tolgono**:

| | correzione | effetto misurato |
|---|---|---|
| **①** | **l'ALIAS TRANSITIVO:** una locale definita come `y = self.x + δ` **è** una variazione di `x`, e assegnarla è ancora `1 · variazione` | `:5921` `vd`, `:5922` `d` e `:3970` `omega_s` **escono dalle eccezioni**. E `_smp_d_ini` ora si vede, perché nasce dentro un `IfExp` |
| **②** | ### **`.copy()` non cambia la forma:** si svolge prima di classificare | è ciò che fa uscire `:3970` `omega_s = omega_new.copy()` |

> ### ⚠ **E una cosa che ho trovato correggendo, e che contraddice in parte la MIA stessa proposta:**
> **`omega_s` NON ha bisogno della forma 6.** `omega_new = omega_src + dtn_c·(…)` è **un'addizione
> nell'algebra**, e l'algebra **è** uno spazio vettoriale: ### **`omega_s` è `1 · variazione`, e si
> somma.** Delle tre scritture che avevo messo in famiglia B, **la forma 6 serve davvero solo a
> `_nb`** *(il versore, che è l'elemento di gruppo)* **e a `phi_s`** *(la sua coordinata polare)*.
> **La forma 6 resta necessaria** — senza, `_nb` non ha una regola — **ma copre 2 scritture, non 3.**

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

### ➜ **La tabella è in `doc/REGOLE_composizione_T3_tabelle.md`, generata.**

**Quello che la tabella dice, e che non cambia con le correzioni:**

> ### **Nessun attributo è incrementato da due leggi E assegnato pieno da una terza**, che era il caso
> peggiore possibile. **`d0` — il più scritto, da tre leggi — è `1 · 5` puro: si somma e basta.**

**E due letture in più, che prima non si vedevano:**

| | |
|---|---|
| ### **`peq` è l'unico attributo in QUATTRO forme** | `1` *(variazione)*, `2` *(il rilassamento in forma chiusa)*, `5` *(struttura)* e `7` *(nascita)*. **È l'attributo che la separazione della mitosi tocca più a fondo** |
| **`_nb` è in `1 · 4 · 5 · 6`** | e la `4` **non è un clip**: è la **rinormalizzazione del versore**, che è la legge di `SU(2)`, non una protezione |

---

# 3. LE ECCEZIONI: **erano 14 in tre famiglie. Ora sono ZERO**

## 3.1 — ### ⚠ **FAMIGLIA A: le DECISIONI CATEGORIALI. Queste non si sommano, e la decisione è di Luca**

> # ✗ **CORREZIONE DEL GUARDIANO** *(Luca, 2026-09-28)* — **e l'errore è MIO**
> **Quello che avevo scritto:** *«`:5642` e `:5666` la scrivono DUE VOLTE nello stesso passo, e la
> seconda sovrascrive la prima»*. ### **È FALSO.**
> `:5639` e `:5642` sono l'### **`if` e l'`else` della STESSA condizione** — `if CHI_COOP: … else: …`
> — quindi **non girano mai insieme**. **Col driver `CHI_COOP` è ACCESO**, quindi `perc_geom` la
> scrive **solo `:5639`** e `perc_chi` **solo `:5666`**.
>
> **Verificato a RUNTIME** *(`csv/_seal_fork/_sig_segni_una_legge.py`, 3 passi pieni sulla scena
> `(ii)(a)`, seme `11`)*:
>
> | riga | grandezza | esecuzioni |
> |---|---|---|
> | `:5639` | `perc_geom` | **3** |
> | `:5642` | `perc_chi` | ### **ZERO** |
> | `:5666` | `perc_chi` | **3** |
>
> ### 📌 **Quindi la regola (ii) — «una sola legge ha il diritto di scriverla» — È GIÀ VERA PER
> COSTRUZIONE.** È **la cura di `A6-PERCCHI`**, già fatta. ### **Si DICHIARA, non si cura, e non si
> archivia niente** *(decisione di Luca)*.
>
> **E la lezione sul metodo, che in questa sessione è la QUARTA:** ### **l'analisi statica vede le
> SCRITTURE e non le CONDIZIONI CHE LE ESCLUDONO.** Per questo il verdetto qui viene dalla
> **copertura di riga a runtime**, non da un conteggio sull'AST.
> **⚠ E una trappola dentro la trappola:** `:5666` gira **con `CHI_DA_SPINORE` SPENTO**, perché
> `_chi_da_psi = CHI_DA_SPINORE or CHI_COOP` *(`:5653`)*. **Chi legge solo il flag conclude il
> contrario.**
>
> ### **Nel classificatore diventa `0 · segno`: un'ESENZIONE, non una sesta forma** — e l'esenzione
> **regge su una condizione che il classificatore NON può verificare**, quindi la verifica **vive
> nel sigillo**.

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

> # ✅ **FORMA 6 `gruppo`: ACCETTATA** *(Luca, 2026-09-28)*
> ### **Con una precisazione che ho trovato io correggendo, e che corregge me:** delle tre scritture
> di questa famiglia **solo DUE hanno bisogno della forma 6**.
>
> | sito | forma vera | perché |
> |---|---|---|
> | `:3971` `_nb` | ### **6 · gruppo** | è **l'elemento di gruppo**: `nb_new` è `nb` **ruotato** |
> | `:3979` `phi_s` | ### **6 · gruppo** | è la **coordinata polare** del versore, riletta da lui |
> | `:3970` `omega_s` | ### **1 · variazione** | `omega_new = omega_src + dtn_c·(…)` è ### **un'ADDIZIONE nell'algebra**, e l'algebra **è** uno spazio vettoriale: **si somma** |
>
> **Quindi la forma 6 copre 2 scritture, non 3** — e questo è il verso giusto: ### **una regola in
> meno da applicare, non una in più** *(`9-ter`)*.

## 3.3 — ### **FAMIGLIA C: l'INIZIALIZZAZIONE DEI NATI. Manca una forma**

| sito | scrittura |
|---|---|
| `:5698` | `self.peq[nuovi] = rho[nuovi]` |

**Non è dinamica e non è struttura:** la struttura ha già creato l'arco, e qui gli si dà **il valore
di partenza**. ### **È la «voce di STATO» della mitosi**, quella che la strada (a) rinvia a `T3`.
> ### **Propongo una forma 7: `nascita`** — *si applica SOLO ai nuovi indici, dopo la struttura, e
> non partecipa alla somma*. **È anche la forma che serve per `psi`/`psi_spin` estese ai nati.**

> # ✅ **FORMA 7 `nascita`: ACCETTATA** *(Luca, 2026-09-28)*
> **E il criterio con cui il classificatore la riconosce NON è un nome:** la maschera degli indici è
> `nuovi = np.isnan(self.peq)`, e ### **`isnan` su una grandezza di stato SIGNIFICA «gli indici che
> non hanno ancora un valore»**, cioè **i nati**. *(Il criterio sta in `nati_di()`.)*

## 3.4 — Le restanti **8**: non sono eccezioni, sono **limiti del classificatore**

| sito | forma vera | perché non l'ha vista |
|---|---|---|
| `:5750` · `:5756` `peq = self._peq_esatto(...)` | ### **2 · rilassamento** | è in forma **chiusa dentro un helper**: `peq ← rho + (peq−rho)·exp(−dt/τ)`. Lo dice il suo docstring |
| `:5620` · `:5624` `twp = self._w8(dph + twist_dip)` · `= dph` | ### **3 · derivata** | `twp` è **la differenza di fase avvolta**, ricalcolata ogni passo da `phi`: va aggiunta all'elenco delle derivate |
| `:5921` `vd = vd_half + 0.5·dts·acc_next` | **1 · variazione** | è la **seconda mezza-spinta del Verlet**: variazione attraverso un locale definito **dentro il ciclo** |
| `:5922` `d = d_new` | **1 · variazione** | idem, `d_new = d + dts·vd_half` |
| `:5945` `d = _smp_d_ini + _smorza(...)` | ### **1 + 4** | ### **è `C3`: foto + freno(δ)**, la forma modello |

### **Quindi le eccezioni VERE sono 6, in tre famiglie**, e due chiedono **una forma nuova**.

> # ✅ **TUTTE E OTTO CORRETTE nel classificatore** *(2026-09-28)*
> **Le due che Luca aveva già dichiarato non-decisioni** — `twp` fra le **derivate**, `_peq_esatto`
> **rilassamento in forma chiusa** — **sono cablate**: `twp` entra in `DERIVATE`, e un `Call` a
> `_peq_esatto` esce `2 · rilassamento`.
> **Le altre tre** *(`:5921`, `:5922`, `:3970`)* **le ha risolte l'alias transitivo** del par.1.0.
>
> ### ⚠ **E UNA IMPRECISIONE CHE RESTA, dichiarata:** `:5945` esce **`2 · rilassamento`** perché il
> freno **rilegge la fotografia**, ma **la sua forma vera è `1 + 4`: `foto + freno(δ)`**, cioè
> **`C3`**. ### **Il classificatore non sa esprimere una COMPOSIZIONE di due forme**, e sceglie la
> più vicina. **Non è un'eccezione: è un'etichetta imprecisa, e il codice lo dice nel suo
> docstring.**

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

## 4.4 — ### 🆕 **LA NASCITA È UN EVENTO ATOMICO** *(decisione di Luca, 2026-09-28)*

> ### **Una nascita non è «un figlio che appare»: è una TRANSAZIONE che comprende il RINCULO DEI
> GENITORI.** Materia e quantità di moto si ridistribuiscono **nello stesso istante**, o non si
> conservano affatto.

**Che cosa comprende l'evento atomico, e va scritto tutto dentro la fase 3:**

| | il pezzo | perché è dentro l'evento e non fuori |
|---|---|---|
| **①** | **il figlio esiste** *(la struttura l'ha creato nella fase 2)* | è il presupposto, non il contenuto |
| **②** | **i valori di partenza del figlio** | la forma **7** |
| **③** | ### **il RINCULO DEI GENITORI** | l'arco genitore si **accorcia** per far posto ai due tronconi, e i nodi ai suoi estremi **ne risentono**. ### **Se questo pezzo sta FUORI dall'evento, una legge successiva vede uno stato in cui la materia è comparsa dal nulla** |
| **④** | **le derivate dei soli nati** *(fase 4)* | `psi`, `psi_spin` |

> ### 📌 **E il criterio operativo, che è la ragione per cui Luca lo chiede ORA:** ### **l'evento
> atomico o si applica INTERO o non si applica.** Non esiste uno stato intermedio visibile a
> un'altra legge — ed è **esattamente la garanzia che lo schedulatore esiste per dare** *(`apri` /
> `chiudi` sono già una transazione: `T1`)*.

**⚠ Che cosa NON dice questa decisione:** **non dice COME si distribuisce il rinculo.** Quella è
fisica, e va **derivata** *(`A1`)*, non scelta. **Va misurata in `T3` e riportata.**

---

# 5. ~~CHE COSA CHIEDO A LUCA~~ → **LE TRE DECISIONI, ARRIVATE E RECEPITE**

| | che cosa chiedevo | ### **la risposta di Luca** *(2026-09-28)* |
|---|---|---|
| **①** | le **decisioni categoriali**: (i) l'ultima vince · (ii) una sola legge ha il diritto · (iii) voto sul segno | ### **NESSUNA DELLE TRE, perché la (ii) È GIÀ VERA.** *«La regola è già vera per costruzione (è la cura di `A6-PERCCHI`): va DICHIARATA, non si archivia niente.»* **E la mia premessa era falsa** — par.3.1 |
| **②** | la **forma 6 `gruppo`** | ### **ACCETTATA** *(e serve a 2 scritture, non 3 — par.3.2)* |
| **③** | la **forma 7 `nascita`** | ### **ACCETTATA** |

**E le due che non chiedevo sono cablate:** `twp` fra le **derivate**, `_peq_esatto`
**rilassamento**. *(Erano dichiarate come letture del codice: ora sono nel codice del
classificatore.)*

---

# 6. 🆕 **LE TRE COSE DA REGISTRARE, e NESSUNA si cura ora**

**Mandato di Luca:** *«da registrare per la fisica, NON ora»*. **Le tre voci sono nell'indice**, e
qui sta il **perché ciascuna è un problema** — coi numeri letti dal codice sul blob `1fc9235f`.

## 6.1 — `TORS-SPINTA`: **una LEGGE DINAMICA nascosta dentro `mitosi()`**

`:6307` `spinta = 0.02 · self.d0 · _rep_mem` → `:6309` `self.d0 = self.d0 + self._sd0(spinta)`.
### **È una scrittura di `d0`, cioè DINAMICA, dentro la funzione che il registro dichiara `AMBIGUA`.**
**È la separazione di `T3` che la fa uscire allo scoperto.**

**I TRE NUMERI NON DERIVATI:**

| | numero | dove | stato |
|---|---|---|---|
| **①** | **`0.02`** *(velocità: 2 % per passo)* | `:6307` | ### **lo dichiara IL CODICE STESSO:** *«`A1` RESTA VIOLATO, E VA DETTO: il `0.02` è un numero SCELTO»* |
| **②** | **`3.0`** *(pendenza dell'inversione)* | `:6179` `segno = −tanh(3.0·(pos − centro))` | **scelto** |
| **③** | **il punto d'inversione a `3.5 π`** | `:6177` `centro = 0.5·(pos_soglia + pos_tetto)` | ### **il VALORE è derivato** *(punto medio fra soglia `3π` e tetto `4π`)*, **ma la SCELTA del punto medio no** |

**Due cose che NON sono il difetto:** la spinta è **moltiplicativa in `d0`** *(scala **locale**
dell'arco)*, e questo è **già curato** — la versione vecchia usava `median(d0)`, una statistica
**globale** dentro un termine dichiarato *«Locale pura»* *(`A2`, `A3`)*; **il gemello sull'altra
spinta è `S09-MEDIANA`, ancora aperto**. E la spinta va **in una sola direzione**: allarga `d0` e
**non lo restringe mai** *(la famiglia di `D31`)*.

> **Dopo `T3`, le tre opzioni da portare:** i numeri si **derivano** · diventano **parametri
> dichiarati** · oppure la spinta si esprime **in unità di `LAM`** *(la scala di Planck del sistema,
> `A13`)*.

## 6.2 — `MAX-NODI-FERMA`: **una guardia di MEMORIA che cambia la FISICA in silenzio**

| sito | che cosa fa **oggi** |
|---|---|
| `:6058` | `if self.n >= MAX_NODI …: return 0` → ### **la mitosi restituisce ZERO NASCITE e il run continua** come se la fisica avesse deciso di non far nascere niente |
| `:2924` | `n = max(0, min(n, MAX_NODI − self.n))` → la **semina si tronca** |
| `:6481` | `if COPPIA_MIT > 0.0 and self.n < MAX_NODI` → il **canale di Schwinger si spegne** |

> ### 📌 **E IL CODICE SA GIÀ CHE È SBAGLIATO.** Il commento di `:1851` dice: *«se lo fosse, la
> misura è da rifare con più memoria, **non da troncare**»*. ### **L'intenzione è scritta e il codice
> fa l'opposto: è esattamente la forma che `A8` esiste per impedire.**

### ➜ **La cura, CONFERMATA da Luca:** **UN** controllo dello schedulatore che ### **FERMA il run con
un errore esplicito, MAI troncare**, **col suo caso che deve fallire**. **E in futuro `MAX_NODI` va
ELIMINATO.**

**Perché non blocca il run base:** il default è **4 000 000** nodi e il pilota sta attorno a
**12 800**. ### **Il difetto è la SILENZIOSITÀ, non il limite.**

## 6.3 — `MITOSI-SOGLIA-GRAD`: **la soglia si abbassa, e l'ampiezza è a mano**

`:6132` `soglia = soglia0 · (1.0 − 0.3 · tanh(grad_modula))`, con
`:6130 grad_modula = |_rn[i] − _rn[j]|` e `:6128 _rn = self._r_nodo_mitosi()`.

| | |
|---|---|
| ### **derivato** | `soglia0 = PHI_CRIT + π = 3π` — **quanto di olonomia** più **twist dipolare massimo**, e *«se cambiano gli ingredienti la soglia si aggiorna da sé»* |
| ### **NON derivato** | l'**ampiezza `0.3`** e la **forma `tanh`**: il commento le dichiara come *«modulazione limitata: la soglia scende di al più ~30 %»*, che è **una scelta** |
| **già curato, non ricontarlo** | il gradiente si prende da **`r`** *(il tempo proprio VERO)* e non da `1/r` né da `abs(tw)` — è **`CURA 2`**, e il conto sta nel commento: `1/r` farebbe **saturare** il `tanh` a `1` esatto, cioè un **riscalamento costante** della soglia, ossia **un parametro nascosto** *(`A1`, e `A11` cor.6: un limite che satura è un allarme)* |
| ⚠ **attenzione al nome** | `1 + abs(tw)/PHI_CRIT` **non è un tempo proprio**: è una **posizione sull'asse della torsione**. Si chiamava `tau_pp`, e lo ha rinominato **`D32`** |

**La legge è interessante e il bersaglio è grosso:** *«la materia va dove il tempo rallenta»* è
### **il principio di equivalenza**, cioè la ③ delle tre prove del bersaglio. **Ma va derivata.**

---

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`SCHED-PASSO` · `SCHED-T3-REGOLE` · `MITOSI-NON-DIVISA` · `ETC-PASSO` · `PSI-FLASH` · `H-ETC-2` ·
`A6-PERCCHI` · `TORS-SPINTA` · `MAX-NODI-FERMA` · `MITOSI-SOGLIA-GRAD` · `S09-MEDIANA` · `D31` ·
`D32` · `A13` · `9-ter` · `A1` · `A8` · `A9` · `A11`
