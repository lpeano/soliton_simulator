# TASK HISTORY — **`Z9` per COORTE: il criterio è scaduto, e la legge di maturazione si DERIVA**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `8140f0c`
**Blob:** `b9e07c73` *(git blob)* · **byte grezzi sul disco:** `2a7207a4` · **albero PULITO**
**Si MISURA, non si cura.** *(Nessun cablaggio, nessuna promozione, nessun tocco a `TAU_A`/`ramp`.)*

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare i numeri*

### 1.1 ⚠ IL §4.1 — **i `.pkl` esistenti: la risposta è DOPPIA, e va detta così**

**Verificato dal disco, non asserito.**

**① IL PRESIDIO DEL BLOB FUNZIONA, ed è stato PROVATO:**

```
r.carica_stato("csv/_test_fork/_gvideo/frame_400.pkl")
-> RuntimeError: DB RIFIUTATO: codice diverso
   (blob DB=a1ae5090... vs ora=b9e07c73...). DB da commit=94e2ec07
```

**Il caricamento nel simulatore è IMPOSSIBILE, come deve essere.** *(Un fallback mai visto scattare è
un comportamento sconosciuto: qui l'ho visto scattare.)*

**② MA LA MISURA NON PASSA DA `carica_stato`.** Le sonde leggono `pickle.load(...)["attrs"]`
**direttamente**, e quel dizionario è **leggibile** — contiene **110 chiavi**, fra cui `eta`, `i`,
`j`, `d`, `tw`, `pos`, `psi`, `rho_spin`, **`_r_corrente`** e **tutti i contatori `_ritmo_*`**.

**③ ⚠ E QUELLO CHE MANCA È ESATTAMENTE IL TRACKING:**

```
csv/_test_fork/_gvideo/frame_400.pkl   tracking presente: []   <- conc_nodi, conc_archi, masse_info ASSENTI
csv/_test_fork/_g2m/frame_400.pkl      tracking presente: []
```

**È `Z53`: i dodici `.pkl` esistenti vengono dal blob `a1ae5090`, che scartava le tre chiavi in
silenzio.** **La coorte per APPARTENENZA A UNA MASSA non è ricavabile, e non la ricavo.**

> **QUINDI NON MI FERMO, MA CAMBIO DEFINIZIONE DI COORTE — ed è una delle due che il mandato
> nomina:** *«separati per generazione o per `eta` anagrafica»*.
> **La coorte ANAGRAFICA è ESATTA dai `.pkl`**, perché **i nodi si appendono in CODA**
> (`self.pos = np.vstack([self.pos, pos_figlio])`, `:3958`) **e nascono con `eta = 0`**
> (`self.eta = np.concatenate([self.eta, np.zeros(len(sel))])`, `:3961`; Schwinger `:4082`;
> `semina` `:1849`). **L'indice È l'ordine di nascita** — lo stesso fatto su cui poggia `Z46`.
> **Con sei snapshot ottengo SEI finestre di nascita esatte**, non una stima.

**COSA QUESTO COSTA, e lo dichiaro adesso perché non sembri una scoperta comoda dopo:**
**la domanda «i nodi di QUESTA massa maturano?» resta SENZA RISPOSTA.** Rispondo a
**«i nodi nati in QUESTA finestra maturano?»**, che **non è la stessa domanda.**
**Per la prima servirebbe rigirare una scena col blob nuovo, e NON lo faccio in questo giro.**

### 1.2 ⚠ LA LEGGE DI MATURAZIONE **SI DERIVA DAL CODICE**, non si misura per regressione

**Dal disco:**

```
:3236   w = self._pesi(); self.eta += dt_n
:3038   dt_n = DT * np.asarray(r_loc, float)[:n]        (TAU_LOC != 0)
:3036   dt_n = np.full(n, DT)                           (TAU_LOC == 0 -> r == 1)
:2649   ramp = np.minimum(1.0, self.eta / TAU_A)
```

> **Quindi `d(eta)/d(passo) = DT · r` ESATTAMENTE, per nodo.**
> **E il tempo di maturazione è `passi(ramp = 1) = TAU_A / (DT · r) = 5000 / r`**, con `TAU_A = 50`
> e `DT = 0.01`.

**Questa è UNA LEGGE, non un numero:** il `~0.009/passo` di `Z9` **corrisponde a `r ≈ 0.9`**, cioè è
**il tasso di UN nodo con un ritmo particolare**, non una proprietà del sistema.
**È esattamente il difetto che il rilievo di Luca denuncia.**

**E prevede la biforcazione senza guardare i dati:** con `r = r_floor = 1.414212e-06` *(i fermi di
`Z46`)* servono **`3.5 · 10⁹` passi**; con `r ≈ 1`, **`5000`**. **Un fattore `7 · 10⁵`.**
**NB:** `eta` usa `dt_n`, **non** `dt_n_s` — **`TEMPO_SEGNO` non tocca `eta`** (verificato a `:3236`).

### 1.3 ⚠ `base` — **l'assoluto NON lo ricostruisco, il RAPPORTO sì, ed è ESATTO**

```
:2650   base = np.exp(-self.d / self._lam_archi()) * ramp[self.i] * ramp[self.j]
:586    KERNEL_ALPHA = 1.0   -> base *= exp(alpha*tau/(1+beta*tau)),  tau = |tw|/PHI_CRIT
```

**`_lam_archi` chiama `lambda_nodi()`, che chiama `massa_critica_adattiva(self)`, che richiama i pesi
— una catena RICORSIVA con un ramo di guardia (`_calcolo_schermatura`).** **Ricostruirla fuori dal
simulatore è precisamente l'errore già fatto su `correzione`** *(due termini, uno dimenticato,
metà coppia — par.9)*. **NON la ricostruisco.**

> **Ma non serve:** il fattore `exp(-d/lam)` e il fattore di torsione **sono IDENTICI** nel kernel
> acerbo e in quello maturo, quindi **si cancellano**:
> **`base / base_maturo = ramp[i] · ramp[j]`, ESATTO.**
> **È un calcolo, non un run** — come il mandato chiede — **e non dipende da nulla che io debba
> indovinare.**

### 1.4 Cosa mi aspetto, e **cosa NON so**

**Mi aspetto** *(e se sbaglio lo annoto, non lo riscrivo)*: due popolazioni nettamente separate in
`r`, quindi due tempi di maturazione incommensurabili; e `ramp` **molto** sotto 1 ovunque, perché
anche `5000` passi sono **il doppio** dei `2400` della scena più lunga.

**NON so:**
- **se esista una coorte, anche piccola, già matura.** `eta_max = 15.92` a 1200 passi dà
  `ramp = 0.318`: **se anche il nodo più veloce è a un terzo, nessuno è maturo** — ma è un numero di
  un'altra scena e **va rimisurato qui, non trasportato** (A3c);
- **se `ramp[i]·ramp[j]` sugli ARCHI si distribuisca come il quadrato di `ramp` sui NODI.** Gli archi
  connettono nodi di coorti diverse, e **il prodotto pesa il MINORE dei due**: un arco fra un nodo
  maturo e un neonato è **acerbo**. **Questo lo devo guardare, non dedurre.**
- **se la fenomenologia con kernel maturo sia DIVERSA o solo PIÙ FORTE.** **E temo di non poterlo
  decidere senza un run** — vedi §2.4.

---

## 2. PROGETTAZIONE — *i passi, cosa decide ciascuno, cosa mi ferma*

### 2.1 ① la maturazione per coorte ANAGRAFICA
Sei coorti dalle sei finestre di nascita (indici `[0, n_f10)`, `[n_f10, n_f115)`, …).
Per ciascuna e a ogni snapshot: **`eta`** min/p05/mediana/p95/max, **`ramp`** gli stessi percentili,
**frazione con `ramp > 0.5` e `> 0.9`**, **numerosità**.
**DECIDE:** se i nodi originali maturano quando il tempo c'è, e se la mediana di popolazione è bassa
**solo** perché i neonati la tirano giù.

### 2.2 ② il tasso, **per coorte E per regime di moto**
`r` **si LEGGE da `_r_corrente`**, non si stima *(è nel `.pkl`; ⚠ ha lunghezza `8013` contro `n = 8018`
— scritto prima dell'ultima mitosi, e i cinque in eccesso vanno ESCLUSI, non riempiti)*.
Separazione **FERMI** (`r/r_floor < 2`) contro **MOBILI**, **mai una mediana comune** (A3c).
`d(eta)/d(passo)` misurato fra snapshot **per gruppo**, e **confrontato con `DT·r` letto**: se i due
non coincidono, **ho sbagliato la derivazione del §1.2 e lo scrivo.**
**Estrapolazione a `ramp = 1` per ciascun gruppo.**

### 2.3 ③ le conseguenze
Distribuzione di **`base/base_maturo = ramp[i]·ramp[j]`** (percentili), **e la frazione di archi
sopra `0.5`/`0.9`**. **Chi legge `_pesi()`**: enumerato **dal disco**, non a memoria.

### 2.4 ④ il criterio nuovo — **il deliverable**
**Derivato dal §1.2:** il criterio non può essere una mediana di popolazione, perché la popolazione
è **bimodale per costruzione**. **Proporrò la forma, con la soglia DERIVATA e non scelta**, e
**deve poter FALLIRE** — cioè deve esistere un numero misurabile che lo dichiari non soddisfatto,
**e oggi deve dire NON SODDISFATTO** se i numeri sono quelli che mi aspetto.

### 2.5 COSA MI FA FERMARE
- **se `d(eta)/d(passo)` misurato NON coincide con `DT·r` letto** → la derivazione del §1.2 è
  sbagliata, **e tutto il resto poggia su di essa: mi fermo e riporto;**
- **se `_r_corrente` non è nei `.pkl` di entrambe le scene** → `②` non si fa come progettato, **e lo
  dico invece di stimare `r` da `eta`** *(sarebbe circolare: `eta` cresce PER `r`)*;
- **se la domanda ③ «diverso o solo più forte» non è decidibile senza un run** → **lo scrivo come
  NON RISPOSTA.** **Non invento una misura sostitutiva** (§0④ del mandato).

---

## 3. TODO DEL NEXT STEP

- [x] blob/branch dal disco · `.pkl` verificati · **presidio del blob PROVATO**
- [x] previsioni qualitative → commit *(`f3895aa`, nove voci)*
- [x] ① → ② → ③ → ④
- [x] **`Z9` RISCRITTA** nel registro, col testo vecchio conservato VERBATIM in appendice al referto
- [x] referto + relazione **nello stesso commit**
- [x] **⚠ NON toccato:** `TAU_A`, `ramp`, `_pesi()`, il regime — **nessuna promozione, nessun cablaggio**

### ⚠ ESITO — **il falsificatore non scatta, e TRE previsioni mie cadono**

**Il falsificatore del §2.5** *(«se `d(eta)/d(passo)` misurato non coincide con `DT·r` letto, mi
fermo»)* **NON è scattato:** rapporto `0.9977` e `0.9966` negli ultimi due intervalli — **entro lo
`0.3 %`**. **La derivazione del §1.2 regge, e tutto il resto poggia su di essa.**

| previsione (`f3895aa`) | esito |
|---|---|
| **1** nessuna coorte a `ramp > 0.9` | **GIUSTA** (zero ovunque) |
| **1-bis** «credo nemmeno a `ramp > 0.5`» | **SBAGLIATA: il `37.7 %` della coorte originale ci arriva** |
| **2** la coorte più vecchia ha il `ramp` più alto *(controllo di sanità)* | **fallisce per un pelo** (`0.3214` contro `0.3212`) — **ma NON è un errore di assegnazione, verificato dal limite superiore della coorte giovane** |
| **3** la coorte originale è la più larga | **non confermata come formulata**: in relativo è la più STRETTA (`2.99` contro `3.67`) |
| **4** due popolazioni a ordini di distanza | **non verificabile qui: i FERMI sono ~0** |
| **5** «la frazione di fermi sarà molto più bassa del `93 %`» | **GIUSTA, ed era l'unica marcata come "può cadere"** |
| **6** il prodotto sarà più piccolo del quadrato | **SBAGLIATA NEL SEGNO** (`1.58×`, `1.13×`) |
| **7** `base/base_maturo < 0.01` per la maggioranza | **SBAGLIATA**: il `99.51 %` è SOPRA |
| **8** «non potrò decidere diverso-o-più-forte senza un run» | **avverata A METÀ**: la parte strutturale si decide, la fenomenologica no |
| **9** qualunque criterio derivato dirà NON SODDISFATTO | **GIUSTA** (fattore `13`/`18`, archi maturi `0.000000`) |

**E una cosa che NON avevo previsto affatto:** **i nati dopo sono il `70 %` dei NODI ma portano
l'`1.37 %` degli ESTREMI D'ARCO** *(grado mediano `496.0` contro `2.0`)*. **È la ragione per cui la
restrizione alla coorte originale, nel mio criterio, oggi è INERTE — e l'ho dichiarato (A9) invece di
venderla come presidio.**

### TODO — il passo successivo

- [ ] **la coorte PER MASSA**: richiede di **rigirare una scena col blob `b9e07c73`**, perché
      `conc_nodi` non è nei `.pkl` vecchi. **Non fatto, e dichiarato.**
- [ ] **il difetto P6**: `TAU_A`/`G_PH`/`CALORE_INIT` in `RUN_PARAMS`. **È una riga, ma è un
      CABLAGGIO e questo mandato lo vieta: va chiesto.**
- [ ] **`Z9-b` a `1`** — il criterio di chiusura, che oggi vale `0.075`
