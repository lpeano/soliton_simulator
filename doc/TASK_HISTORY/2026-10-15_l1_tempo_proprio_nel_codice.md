# `L1` — IL TEMPO PROPRIO IN OGNI LEGGE: **il codice**

> **Mandato di Luca del 2026-10-15, versione RIFINITA** *(vale l'ultima,
> `[[PRECEDENZA-IN-CODA]]`)*. Le decisioni `B-3` e `B-4` sono registrate in `af3e40c`:
> **questo e' il punto 1**, il codice.
>
> ### ⛔ **E SI SCRIVE PRIMA DI GUARDARE**, come il paragrafo 8 delle regole pretende: il
> commit di questo file e' **antenato** dei commit del lavoro, e l'ordine si verifica da
> `git`, non dalla mia parola.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare, e cosa NON so*

### ⭐ **CIO' CHE CREDO DI SAPERE, e viene da misure gia' fatte**

1. **La forma e' derivata, non scelta** *(da `1dcf315` e dalla derivazione di strada `(B)`)*:
   il Grover e lo spostamento di oggi sono **involuzioni hermitiane**, cioe' **flussi di un
   generatore locale presi all'angolo `pi`**.
   `S_U = [[0, U^dagger],[U, 0]]` e' hermitiana e unitaria; `P- = (I - S_U)/2` e' un
   proiettore; `exp(i pi P-) = I - 2 P- = S_U`. E `G = 2 P_u - I = exp(i pi (I - P_u))`.
2. **Ogni strato fattorizza ESATTAMENTE** *(supporti disgiunti: ogni estremita' appartiene a
   esattamente UN arco e UN nodo)*, quindi l'errore di Strang sta **FRA gli strati**, non
   dentro: raffinare `dtau` lo riduce, raffinare la **scena** no. ### **E' questo che rende
   `M-B2` una misura sensata.**
3. **Le tre letture dirette di `self.dtau`** stanno in `_moneta_spin` *(una)* e in
   `_saturazione` *(due)*: le ho censite col grep, non ricordate.
4. **`espi` e' necessaria perche' `numpy` non ha `cospi`/`sinpi`**:
   `np.exp(1j*np.pi) = -1 + 1.2246e-16j`, e quel `1.2246e-16` **ucciderebbe `M-B1`.**

### 📌 **ANNOTAZIONE, misurata MENTRE scrivevo questo file** *(e la annoto invece di
riscrivere il punto `4`, perche' la regola dice **si ANNOTA**)*

```
np.exp(1j*np.pi)  = -1 + 1.2246467991473532e-16j      <- il 1.2e-16 che ucciderebbe M-B1
np.cos(np.pi)     = -1.0        ESATTO
np.sin(np.pi)     =  1.2246467991473532e-16   NON esatto   <- il male sta nel SENO, non nel coseno
```

### ⭐ **QUINDI `espi` NON HA BISOGNO DI UN COSENO SPECIALE: solo del seno.** E la cura e'
**un'identita', non un caso particolare:** per `s` in `[0, 1]`,
`sin(pi s) = sin(pi (1-s))`, e `1-s` e' **esatto** per `s >= 0.5` *(lemma di Sterbenz)*;
riducendo con `r = min(s, 1-s)` si ha `r = 0` **esatto** a `s = 1`, quindi
`sin(pi r) = 0` **esatto**.

### ⚠⚠ **E UNA TRAPPOLA CHE HO VISTO SOLO PERCHE' HO PROVATO PIU' VALORI:** la forma ovvia
della media armonica, `2 d d/(d+d)`, e' **esatta per `0.25`, `0.31`, `0.37` e `1/3`**, e
### **SBAGLIATA per `0.1`, `0.2` e `0.4`.** ### ⛔ **Cioe' con la scena a `dtau = 0.25`
*(quella di `bande` e `segno`)* la forma sbagliata AVREBBE PASSATO `M-B1`**, e il difetto
sarebbe uscito dopo, su un'altra scena. ### **La forma `S/2 - D^2/(2S)` e' esatta su tutti
e otto**, coincide con `2ab/(a+b)` entro **`7.2` ulp** su `100000` coppie casuali, ed e'
**simmetrica in `i<->j` al bit** *(verificato: `True`)*.

### ⛔ **CIO' CHE NON SO, e che decide tutto: CHE COS'E' `dtau_rif`**

### ⚠ **Ci sono DUE letture di `B-4`, e danno codici DIVERSI:**

| | la lettura | che cosa implica |
|---|---|---|
| **(i)** | `dtau_rif = max(dtau)` **ricalcolato**, il massimo dei nodi di ADESSO | un riscalamento **uniforme** di `dtau` e' **inerte**: `s = dtau/max(dtau) = 1` sempre |
| **(ii)** | `dtau_rif` = **il tetto del cono**, l'orologio piu' veloce **POSSIBILE** *(`cs` al massimo)*, cioe' **UNA SCELTA DI UNITA'** | `theta = pi · dtau/dtau_rif` **scala con `dtau`** |

### ⭐⭐ **E NON LA SCELGO IO: LA SCELGONO I CRITERI DI USCITA DI LUCA.** Sotto la lettura
**(i)** *(il massimo corrente)*:
- **`_collauda_tempo_proprio.py` NON POTREBBE MAI PASSARE:** misura
  `|psi(dtau) - psi(dtau/2)|` con `dtau` **uniforme**, e sotto `(i)` dimezzare un `dtau`
  uniforme **non cambia nulla** — `s` resta `1`. ### **I quattro violatori resterebbero
  violatori per sempre**, e il criterio sarebbe **impossibile**, non difficile.
- **`M-B2` SAREBBE VUOTA:** `dtau` uniforme `= dtau_rif/2^k` sotto `(i)` da' ancora
  `s = 1`, quindi **zero cambiamento e nessun fattore 4.**

### ✅ **QUINDI LA LETTURA E' LA `(ii)`, e non per preferenza: perche' la `(i)` rende DUE
criteri su quattro VUOTI.** E la `(ii)` e' anche **cio' che il testo di Luca dice**:
*«e' una SCELTA DI UNITA', non una costante nuova»*, e `B-5`
*(«il tick e' l'orologio piu' veloce possibile»)* **e' il tetto del cono**.

### ⭐ **E LA CONSEGUENZA OPERATIVA E' CHE `omega` SPARISCE DAL CODICE.** Con `dtau_rif = 1`
*(l'unita')* il raccordo `omega·dtau_rif = pi` da' `omega = pi`, e nel codice compare
**solo `theta = pi·dtau`**: ### ✅ **nessuna costante nuova,
`CARTA-FISICA-SIMULATORE/F10` rispettato per COSTRUZIONE e non per disciplina.**

### 📌 **E UN FATTO CHE HO MISURATO PRIMA DI SCRIVERLO**, perche' la lettura `(ii)` pretende
`dtau <= 1`: **tutti i `dtau` in uso nel repo oggi sono `0.1`, `0.2`, `0.25`, `0.31`,
`0.37`, `0.4`** *(censimento col grep su `primo_ordine/*.py`)*. ### ✅ **Nessuno viola il
cono**, quindi la lettura `(ii)` **non rompe nessuna scena esistente** — e il `<= 1` si
asserisce *(ALZA)*, **non si taglia** *(`A11`)*.

### ⚠⚠ **E CIO' CHE MI ASPETTO DI ROMPERE, e lo scrivo PRIMA per non poterlo minimizzare
dopo:** sotto `(ii)`, con le scene di oggi *(`dtau ~ 0.2-0.37`)* il Grover e lo spostamento
agiscono a **`theta = 0.2 pi` - `0.37 pi`**, **non a `pi`**. ### **Quindi NON sono piu'
involuzioni**, e ogni collaudo che asserisce `G^2 = I` o *«due spostamenti = identita'»*
### **DEVE fallire.** ### ⭐ **Non e' un difetto del mio codice: e' il CONTENUTO di `L1`** —
e il mio dovere e' **riportare quali, con i numeri**, non aggiustarli perche' tornino verdi.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | il passo | **che cosa decide** | **cosa mi FERMA** |
|---|---|---|---|
| `1` | **`espi(s) = e^{i pi s}`** in un modulo nuovo, `primo_ordine/flussi_parziali.py` *(il tetto di `700` righe di `P-MOD` vieta di allungare `motore.py`, che sta a `677`)* | se `M-B1` e' possibile: **serve `espi(1) = -1 + 0j` ESATTO** | `espi(1) != -1+0j` al bit → **non si procede**, perche' nessuna forma dell'operatore puo' rimediare |
| `2` | **`dtau_arco`, la media armonica di `B-3`**, nella forma `S/2 - D^2/(2S)` con `S = d_i + d_j`, `D = d_i - d_j` | se `M-B1` e' possibile **con `dtau` uniforme**: questa forma e' **ESATTA quando i due sono uguali** *(`D = 0` ⟹ `S/2 = 2d/2 = d` al bit)*, mentre `2 d_i d_j/(d_i+d_j)` **NON lo e'** | se la forma esatta non esistesse, `M-B1` sarebbe fuori portata |
| `3` | **IL PUNTO UNICO DI LETTURA**: `dtau_nodo`, `dtau_rif`, `s_nodo`, `s_arco`, e **le tre letture dirette di `self.dtau` passano da li'** | che `L2` possa far variare `cs` **in un posto solo**: e' cio' che il mandato chiede | una lettura diretta che resta → il punto unico **non e' unico** |
| `4` | **I QUATTRO OPERATORI PARZIALI**, `psi` **e** `phi`: `hop(theta)` sull'arco, `G(theta)` sul nodo | la fisica di `L1` | — |
| `5` | **`M-B1`**: `dtau = 1` ovunque → **identita' AL BIT** con `717bb60`, `>= 200` tick, `psi` **e** `phi` | se il raccordo `B-4` e' vero nel codice | **se fallisce, FERMO**: committo la misura e spiego |
| `6` | **`_collauda_tempo_proprio.py`**: `VIOLATORI_ATTESI` **svuotato**, e un violatore **FA FALLIRE** il `pre-commit`. ### **E lo DIMOSTRO**: rimetto per prova un pezzo a tick fisso, guardo fallire, poi togli la prova | che il presidio **impedisca** invece di raccontare *(`A9`)* | se non fallisce davvero, il presidio e' **una tenda** |
| `7` | **`M-B2`**: `dtau = dtau_rif/2^k`, `k = 1..4` → l'errore di conservazione **cala di `4`** a ogni dimezzamento | che l'errore sia **di Strang** *(`O(dtau^2)`)* e non qualcos'altro | un rapporto lontano da `4` → **FERMO e lo riporto**: non tocco parametri |
| `8` | **IL CENSIMENTO DEI COLLAUDI CHE CAMBIANO VERDETTO**, con il perche' di ognuno | quanto costa `L1` al resto del banco | un collaudo che fallisce **per un motivo che non so spiegare** → FERMO |

### ⛔ **LE DUE COSE CHE NON FACCIO, e le scrivo per non scivolarci:**
1. **non tocco `deriva.py`** se non **in lettura** *(il perimetro di Luca)*, e se una sua
   parte dovesse servire **la dichiaro una per una**;
2. **non cambio `tipo: pezzo_unitario` in `flusso`** nella tabella. ### **Perche' sarebbe una
   decisione di fisica mia:** `flusso` in quel formato vuol dire **generatore scritto come
   ESPRESSIONE in tabella**, e questi generatori *(`P-`, `P_u`)* sono **operatori sul grafo
   che il formato non puo' esprimere** — e' il posto `P4`, gia' dichiarato. ### **E cambiare
   il tipo cambierebbe l'ORDINE generato** *(Strang spezzerebbe in `0.5 + 0.5`)*, cioe'
   **cambierebbe il passo**, che `M-B1` misura.

---

## 3. LA STELLA POLARE — **le cinque risposte, scritte PRIMA del codice**

| | la risposta |
|---|---|
| **1. `A14`, conserva localmente?** | **La CARICA si': ogni pezzo e' UNITARIO** *(`hop(theta)` e `G(theta)` sono esponenziali di operatori hermitiani a supporto di raggio ZERO — un arco, un nodo)*. ### ⚠ **L'ENERGIA no, e NON per colpa di `L1`:** l'errore di Strang **fra gli strati** resta, ed e' **esattamente cio' che `M-B2` misura.** ### ⭐ **E `L1` lo MIGLIORA** invece di peggiorarlo: oggi quell'errore **non cala affatto** raffinando `dtau`, perche' due strati su quattro **ignorano `dtau`**; dopo, cala come `dtau^2`. ### **La violazione resta dichiarata in `CONSERVAZIONE-LOCALE`.** |
| **2. a quale GRADINO arriva?** | **`(a)`, robusto al rumore numerico**, e per `M-B1` **piu' di `(a)`: identita' AL BIT**. ### ⛔ **NON arriva a `(c)`** *(un limite noto)*: nessuno ha mostrato che questo passo tenda all'equazione di Dirac, e **non lo affermo.** |
| **3. aggiunge un numero o una legge?** | ### ✅ **NESSUN NUMERO NUOVO, e si vede nel codice: `omega` non compare.** Il raccordo `omega·dtau_rif = pi` con `dtau_rif` **unita'** lascia **solo `theta = pi·dtau`**, e `pi` **non e' una manopola.** ### **E NESSUNA LEGGE NUOVA:** le leggi restano `7` prima e `7` dopo *(`9-ter`: una cura non aumenta il numero delle leggi)* — cambia la **FORMA** di quattro, non il loro numero. ### ⛔ **E nessun clip, nessun pavimento, nessun tetto** *(`A11`)*: `theta <= pi` **viene dalla definizione**, e `dtau <= dtau_rif` e' **un assert che ALZA**, non un taglio. |
| **4. tocca `rho`, `c_s` o il SEGNO?** | **Tocca `c_s` nel VERSO <<struttura → dinamica>>**, e **solo per predisporre**: a `L1` `cs` resta **UNIFORME**, e cio' che si costruisce e' **il PUNTO UNICO** da cui `L2` lo fara' variare. ### ⛔ **Nessun accoppiamento EM↔curvatura e' toccato**, in nessuno dei due versi. |
| **5. emergente o imposto?** | ### **IMPOSTO, e lo dico senza attenuarlo:** il tempo proprio locale **e' un'ASSUNZIONE del modello** *(`TEMPO-PROPRIO-LOCALE`)*, non un fenomeno che emerge. ### ⭐ **Cio' che e' EMERGENTE e' la CONSEGUENZA:** che l'errore di energia cali come `dtau^2` **non e' imposto da nessuna riga** — e' cio' che `M-B2` **misura e potrebbe smentire.** |

---

## 4. TODO DEL NEXT STEP — *operativa, non un riassunto*

1. `primo_ordine/flussi_parziali.py`: `espi`, `dtau_nodo`, `dtau_rif`, `s_nodo`, `s_arco`
   *(media armonica nella forma `S/2 - D^2/(2S)`)*, e i quattro operatori parziali.
   ### **Dichiarato in `csv/_file_fisica.py` e in `_mappa.yaml`** *(altrimenti
   `H-FISICA-FUORI-LISTA` e `P-MOD` rifiutano)*.
2. `motore.py`: i quattro operatori chiamano il modulo nuovo; **le tre letture dirette di
   `self.dtau` passano dall'accessore**; gli `assert frazione == 1` **non sono piu' veri** e
   diventano `0 < frazione <= 1`.
3. `leggi.yaml`: la `scheda` delle quattro leggi dice **la forma nuova** *(`H-REG-R` pretende
   la scheda in `REGISTRO_FISICA` nello stesso commit)*; **l'`ordine` NON si tocca.**
4. `_collauda_tempo_proprio.py`: `VIOLATORI_ATTESI = ()`, e `return 1` quando ce n'e' uno.
   ### **Con la prova del fallimento, mostrata e poi togliere.**
5. `M-B1` e `M-B2`: due script in `primo_ordine/`, **ognuno col suo referto**, e i numeri
   salvati **DURANTE** la corsa.
6. Il censimento dei collaudi che cambiano verdetto, **con il motivo di ognuno.**
7. `doc/RIPRESA_2026-10-15.md` e `doc/MAPPA_DIPENDENZE.md`: `L1` chiuso **o perche' no.**
   Poi **STOP**: `L2` vuole una decisione di fisica di Luca.
