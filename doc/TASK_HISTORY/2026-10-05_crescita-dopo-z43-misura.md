# `CRESCITA-DOPO-Z43` — **LA MISURA**: perché la rete quasi non cresce più

*(Mandato di Luca del 2026-10-05, dopo il sigillo della `PARTE B` di `Z43` (`9731201`).
Viene **PRIMA** della misura con `DT` dimezzato, che resta in coda subito dopo.
Il simulatore **`f7237563` NON si tocca**: patch su **copie**.)*

> ### ⛔ **SOLO NUMERI, NESSUNA CURA.** La crescita e la soglia di mitosi sono **decisioni di
> ### Luca**, e questo mandato non ne prende nessuna.

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo prima di guardare, e che cosa NON so*

### IL FATTO, e non è mio: è misurato

Dal referto `9731201` *(criterio `7`)* e dalla misura indipendente del guardiano su Linux:
al passo `150`, `n = 12827` nella `PARTE B` contro `14328` nella `PARTE A`, da una partenza
di `12802`. Cioè **~25 nascite contro ~1500**, e nella `PARTE B` concentrate in **13 passi
su 150**.

### ⚠ **E IL RALLENTAMENTO UNIFORME NON LO SPIEGA, e il conto è di una riga**

`r` mediano è `0.815126`. Il fattore di tempo entra nella probabilità **UNA volta sola**
*(`CURA 2`: `ampiezza = ampiezza_int * _ft` con `_ft = dt_e/DT`)*, quindi gli eventi attesi
per passo scalano di **`~0.815`**. ### **Un fattore `0.815` non fa un fattore `~60`.**
C'è dunque **almeno un'altra causa**, e il mandato dice quale sospettare.

### L'IPOTESI DEL GUARDIANO — **da VERIFICARE, non da assumere**

La soglia di mitosi **si abbassa col GRADIENTE del tempo proprio**
*(voce `MITOSI-SOGLIA-GRAD`, `_r_nodo_mitosi` e `decidi_divisione`)*:

```
grad_modula = |r[i] - r[j]|
soglia      = soglia0 * (1.0 - 0.3 * tanh(grad_modula))
```

Con l'altalena, `r` spaziava su `[1.4142e-06, 1.4142]` e il gradiente fra vicini era
**enorme** → `tanh → ~0.888` → la soglia **crollava** fino a `~0.73 * soglia0`. Con `r`
liscio il gradiente è piccolo → `tanh → ~0` → la soglia **resta `soglia0`**.
### ⚠ **Se è così, gran parte della crescita misurata finora era alimentata
### DALL'ARTEFATTO DELL'OROLOGIO**, non dalla fisica.

### CHE COSA MI ASPETTO, scritto ORA perché dopo non valga come previsione

**Mi aspetto che i due bracci si separino sul PRIMO cancello, `avv > soglia`**, e che la
causa dominante sia **il gradiente** e non il rallentamento uniforme. ### **Il perché è il
`0.3`:** la modulazione può spostare la soglia **del 27 %** al massimo, e `avv` è una
torsione accumulata la cui distribuzione, vicino alla soglia, è **ripida** — spostare la
soglia del 27 % può spazzare via quasi tutti i candidati.

### ⛔ **E QUESTO È ESATTAMENTE CIÒ CHE NON SO, e lo scrivo come incertezza e non come
### cautela di maniera**

**Non so quanto sia ripida la distribuzione di `avv` attorno alla soglia.** Se fosse
**piatta**, un `27 %` darebbe un effetto di ordine `27 %`, non `60×`, e l'ipotesi del
gradiente **cadrebbe** — e allora la causa sarebbe altrove *(il cancello della densità, il
segno, o `avv` stesso che è cambiato perché la torsione evolve in un tempo diverso)*.
### **Il punto (b) del mandato esiste per questo: senza le DISTRIBUZIONI, il conteggio dei
### cancelli dice DOVE si separano e non PERCHÉ.**

### E UNA TERZA CAUSA POSSIBILE CHE IL MANDATO NON NOMINA, e la metto per iscritto

`avv = |tw|` **non è un dato esterno**: la torsione evolve integrando in `dt_e`, cioè
**nel tempo proprio**. Con `r` diverso, **`|tw|` al passo `k` è una grandezza diversa**.
Quindi i bracci potrebbero separarsi **non perché la soglia è più alta, ma perché `avv` è
più bassa** — e il censimento dei cancelli, da solo, **non distingue i due casi**: li
distingue il confronto fra la **distribuzione di `avv`** e quella di **`soglia`**.
### ✅ **Per questo riporto le due distribuzioni, non il solo rapporto.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi farebbe FERMARE*

### LA CATENA DEI CANCELLI, **censita dall'AST e dal sorgente**, in ordine

`decidi_divisione` *(`:8255` sul blob `f7237563`)*. Le letture si fissano **qui**, prima dei
numeri:

| # | il cancello | la riga | che cosa lo chiude |
|--:|---|---|---|
| `0` | la rete ha archi | `if not len(self.tw): return None, {}` | rete senza archi |
| — | `soglia0 = PHI_CRIT + pi` *(`TORS_4PI and not FASE_2PI`)* | — | `= 3pi` |
| — | **la MODULAZIONE:** `soglia = soglia0*(1 - 0.3*tanh(|r_i - r_j|))` | — | ### **è l'ipotesi** |
| `1` | **sopra soglia:** `ecc = avv/soglia - 1`, poi `max(ecc, 0)` | — | `avv <= soglia` → `salita = 0` |
| `2` | **sotto il tetto `4pi`:** `discesa = clip(1 - avv/4pi, 0, 1)` | — | `avv >= 4pi` → `discesa = 0` |
| `3` | **segno di creazione:** `segno = -tanh(3*(pos_torsione - centro))` | — | `segno <= 0` → regime **repulsivo** |
| — | `ampiezza = salita*discesa*_ft` con `_ft = dt_e/DT` | — | ### **è il rallentamento uniforme** |
| `4` | **l'estrazione:** `prob = 1 - exp(-max(resp, 0))`, `nasce = rng < prob` | — | il dado |
| `5` | **il tetto `MITMAX`** | `c[argsort(avv)][:MITMAX]` | ### **inerte: `MITMAX = 0`** |
| `6` | **la densità:** `0.5*(I[a]+I[b]) >= QMIN_M * median(peq)` | — | ### **`QMIN_M = 0.000`** |
| `7` | **`A13`/`2LAM`:** `FRAZ*d >= LAM` **e** `(1-FRAZ)*d >= LAM` | — | archi corti |
| → | **le nascite** | `sel = c[ok]`, `nati += len(sel)` | — |

> ### 📌 **DUE CANCELLI SONO GIÀ NOTI COME QUASI-INERTI, e lo dichiaro PRIMA di misurarli**,
> così non posso spacciarlo per una scoperta: **`MITMAX = 0`** *(`:3065`, nessun tetto)* e
> **`QMIN_M = 0.000`** *(`:3058`)*, che rende il cancello `6` la condizione
> `0.5*(I[a]+I[b]) >= 0`, cioè ### **sempre vera per densità non negative.** Li misuro
> comunque, perché **un cancello che credo inerte e non misuro è un cancello che non so.**

### COME SI MISURA — **tre ganci su una COPIA, e la legge non si riscrive**

Le grandezze del punto (b) sono **locali** di `decidi_divisione`, e `_dt_e_ultimo` viene
**riscritto nello stesso passo**: da fuori **non si possono leggere**. Quindi **tre ganci**,
ciascuno con la sua **ancora contata** *(`P1-quater`)*:

1. dopo `soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))` → `_rn`, `grad_modula`,
   `soglia0`, `soglia`;
2. prima di `c = np.where(nasce)[0]` → `avv`, `soglia`, `ecc`, `salita`, `discesa`, `_ft`,
   `segno`, `resp`, `prob`, `nasce`;
3. dopo `ok = ok & _conforme` → `c`, `ok`, `_no_dens`, `_no_lam`, `I`, `_dc`.

### ✅ **I ganci LEGGONO i valori che la legge ha calcolato: non ne ricalcolano nessuno.**
Ricostruire `soglia` o `_ft` fuori sarebbe **una seconda scrittura della stessa legge**
*(`9-ter`)*, ed è l'errore che la `PARTE B` ha già pagato una volta
*(il criterio `5` chiamato **fuori dal passo**, `aafb3eb`)*.

### ⚠ **E IL GANCIO `3` STA DENTRO `if len(c):`**, quindi nei passi senza candidati non
scatta: quei passi hanno **zero nascite da divisione** per costruzione, e si **contano**
separatamente invece di apparire come dati mancanti.

### I QUATTRO BRACCI

| | | |
|---|---|---|
| **`A`** | la `PARTE A` | blob **`062172d3`**, dal tag `pre-z43-cura2-r-da-cs` |
| **`B`** | la `PARTE B` | blob **`f7237563`**, il simulatore di oggi |
| **`Ap`**, **`Bp`** | le **copie patchate** coi tre ganci | una per braccio |

### ⚠ **E I CONTEGGI SI PRENDONO DALLE COPIE PATCHATE, non dai bracci nudi**, perché i ganci
non toccano la fisica: **leggono e accumulano**. ### **Ma lo DICHIARO invece di assumerlo**,
e il controllo di ricostruzione qui sotto è ciò che lo **verifica**: se un gancio cambiasse
la fisica, le nascite ricostruite **non** coinciderebbero con `n` finale.

### IL CONTROFATTUALE del punto (d) — e **una cosa che non è letteralmente vera**

Su una copia della `PARTE B` **dichiarata come tale**: `r` moltiplicato per
`1/mediana(r)` del passo, cioè **il rallentamento uniforme tolto**.

> ### ⚠ **E IL MANDATO DICE <<gradienti intatti>>: NON LO SONO, e il conto è immediato.**
> Riscalare `r` per `1/mediana(r) ≈ 1.227` moltiplica **anche** `|r_i - r_j|` per `1.227`.
> ### **Quindi il gradiente non resta intatto: CRESCE del 23 %** — e un gradiente più
> grande **abbassa** la soglia, cioè spinge le nascite **verso l'alto**.
> ### ✅ **Questo NON rompe il controfattuale, lo rende CONSERVATIVO nella direzione giusta:**
> se le nascite **restano basse** nonostante un gradiente *maggiorato* e il rallentamento
> *rimosso*, la conclusione <<non è il rallentamento>> è **più forte**, non più debole.
> Se invece **risalgono**, il `23 %` di gradiente in più è una **causa confondente** che va
> dichiarata — e allora il controfattuale **non separa** le due cause e lo dirò.
> ### **Applico la prescrizione di Luca ALLA LETTERA e ne dichiaro il limite: non la
> ### cambio di mia iniziativa.**

**Dove si applica:** subito dopo che `ritmo()` ha restituito `r`, in `step()`, così
**tutto** ciò che sta a valle *(`dt_n`, `dt_e`, il gradiente della mitosi)* vede `r`
riscalato. ### **È un braccio DICHIARATO FINTO: non è una cura e non entra nel simulatore.**

### I CONTROLLI CHE POSSONO FALLIRE — **fissati ORA**

| | il controllo | se fallisce |
|--:|---|---|
| **`C1`** | **RICOSTRUZIONE AL CONTEGGIO:** `somma(ammessi)` + `_g_nati_schwinger` **==** `n_150 - n_0`, **in CIASCUN braccio** | ### ⛔ **il censimento dei cancelli è INCOMPLETO: FERMO** |
| **`C2`** | **zero candidati non è un confronto:** se un braccio ha `0` candidati su tutti i `150` passi, il confronto per cancello **non esiste** | ### **si dichiara, non si interpreta** |
| **`C3`** | i ganci **non cambiano la fisica**: `n` e gli archi finali della copia patchata **==** quelli del braccio nudo | ### ⛔ **i numeri sono dello strumento, non del sistema: FERMO** |
| **`C4`** | la **separazione** dei bracci cade su **UN** cancello nominato, non su <<più o meno tutti>> | ### **si riporta quale, e se sono due si dice che sono due** |

### ⚠ **`C1` È IL CONTROLLO VERO, e va detto perché:** `nati += len(sel)` *(`:8855`)* e
`nati += nc` *(`:8971`)* sono **le uniche due strade** per cui `n` cresce in un run
*(la semina sta prima del passo `1`, e `_allaccia` aggiunge **archi**, non nodi)*.
### **Se la somma non torna, c'è una terza strada che non ho censito** — ed è esattamente
il tipo di cosa che ho già sbagliato tre volte in due giorni.

## LA STELLA POLARE

> ### 📌 **QUESTO MANDATO NON CAMBIA LA FISICA: è una MISURA.** Ma le cinque domande si
> rispondono comunque, e **due hanno una risposta che NON è <<non si applica>>** — perché
> riguardano **il risultato che sto per affermare**, non una legge che sto per scrivere.

**1 — `A14`, conservazione locale.** **Non si applica alla misura**, e il perché è che non
scrive nessuna legge: i ganci **leggono**. ### ⚠ **Ma si applica a ciò che la misura
POTREBBE far concludere:** se la crescita era alimentata dal gradiente dell'orologio, allora
**i nodi nati finora erano creati da un artefatto numerico**, e la domanda *<<quella massa da
dove veniva?>>* è una domanda di `A14`. ### **Non la risolvo qui: la nomino.**

**2 — i tre gradini.** Il risultato che affermerò arriva al gradino **(a) robusto al rumore
numerico** *(due bracci, stessa scena, stesso seme, lockstep)* e, **grazie al controfattorale
(d)**, al gradino **(b) regge togliendo la legge pratica** — dove la *legge pratica* è il
`0.3` della modulazione **vista attraverso il rallentamento uniforme**.
### ⛔ **NON arriva al gradino (c):** non esiste un limite noto con cui confrontare un
conteggio di nascite su questa scena. ### **E i conteggi ASSOLUTI dipendono dalla
piattaforma** *(`STELLA_POLARE`, ②: Linux `16/14/6/6` dove Windows dà `14/12/4/4`)*, quindi
### **il risultato è il RAPPORTO fra i bracci, non il numero di nascite.**

**3 — numeri e leggi.** ### **ZERO**: nessun numero nuovo, nessuna legge nuova, nessun clip.
Lo strumento ha **una** costante sua — il passo a cui misura le distribuzioni — e si fissa
**qui**, non dai dati. ### ⚠ **E la misura NOMINA un numero che già c'è e che `A1`
condanna: il `0.3`** della modulazione, *«ampiezza < 0.3 della soglia»*, che è **scelto**.
### **Questa misura dice quanto costa, non lo cambia.**

**4 — `rho`, `c_s`, il SEGNO.** **La misura non li tocca.** ### ✅ **Ma li LEGGE tutti e tre,
ed è il punto:** `c_s` entra in `r` *(è la cura `(2)`)*, `rho` è il cancello `6`, e **il
SEGNO è il cancello `3`** — `segno = -tanh(3*(pos_torsione - centro))`, che decide
**creazione contro repulsione**. ### **Se i bracci si separassero sul cancello `3`, la
risposta sarebbe <<il verso>>, non <<la soglia>>**, e sarebbe un risultato diverso da quello
che mi aspetto.

**5 — emergente o imposto.** ### **È LA DOMANDA DI QUESTO MANDATO, non una formalità.**
La crescita misurata finora **sopravvive** se si toglie la legge pratica che la potrebbe
produrre — il gradiente di `r` gonfiato dall'altalena? ### **Il punto (d) è il test, e la
risposta può essere NO.** ### ⚠ **E se è NO, la conclusione non è <<la cura ha rotto la
crescita>>: è <<la crescita di prima era in parte IMPOSTA>>** — e distinguere le due frasi
è l'unica ragione per cui questa misura vale la pena.

## ⚠ ANNOTAZIONE DEL 2026-10-05 — **LE QUATTRO VERIFICHE DEL GUARDIANO, e la mia
## previsione REFUTATA**

> ### **PAR.8: IL RAGIONAMENTO PRELIMINARE NON SI RISCRIVE QUANDO SI RIVELA SBAGLIATO, SI
> ### ANNOTA.** Cio' che ho scritto prima dei dati **resta dov'e'**; qui c'e' che cosa non
> vedeva. ### **Ogni verifica l'ho RIFATTA sui dati, non ricopiata dal messaggio del
> guardiano.**

### ✖ **(1) LA MIA PREVISIONE ERA SBAGLIATA, E DUE VOLTE**

Avevo scritto: *<<mi aspetto che i due bracci si separino sul PRIMO cancello>>*.
**Primo errore:** si separano su **piu' di uno**. ### **Secondo errore, e l'ha trovato il
guardiano: avevo contato fra i canali il cancello `2`, CHE NON E' UN CANALE.**

Gli archi che passano il cancello `1` e **non** il `2` sono ### **esattamente quelli con
`|tw| >= 4pi`** *(identita', non stima: il cancello `2` e' `avv < 4pi`)*. Sono una
popolazione ### **FISSA**: `0` al passo `1`, **`109` al passo `2`**, poi quasi costante, e
### **pesa quasi uguale nei TRE bracci** *(`~14981` / `~14338` / `~14153` passi-arco)* --
quindi ### **non dipende dalla legge del tempo proprio.**
### ✔ **Togliendola, il salto NETTO del cancello `2` vale `1.0000` in ENTRAMBI i bracci.**
Il *<<`x0.425`>>* era ### **la diluizione di una popolazione fissa**, e le frazioni
diversissime *(`10 %` in `Ap`, `62 %` in `Bp`)* vengono dal **denominatore**, non dalla
popolazione. ### **Registrata come voce nuova `ARCHI-OLTRE-4PI`, da NON indagare ora.**

### ✔ **(2) LA SCOMPOSIZIONE GIUSTA E' IN TRE FATTORI, e il prodotto E' il fattore**

Non *<<tre cancelli con tre salti>>*, ma **tre rapporti moltiplicativi**:
**(a)** la popolazione nella finestra `Sum g1^g2^g3`; **(b)** il tasso di estrazione **per
arco** `Sum g4 / Sum g1^g2^g3` *(dove vive `_ft`, cioe' il rallentamento)*; **(c)** il
cancello `2LAM`.
### **E il loro prodotto e' il fattore sulle divisioni PER COSTRUZIONE ALGEBRICA** -- i
denominatori si cancellano a due a due. ### **Quindi il suo valore non e' <<tornare>>: e'
DOVE sta il fattore**, e il referto lo riporta anche **per finestre di passi**.
### ⚠ **Con una riserva che aggiungo io:** nella finestra `60`-`100` la `PARTE B` ha **un
numero di divisioni dell'ordine dell'unita'**, quindi ### **quel rapporto non ha peso
statistico** e va letto come tale.

### ✖ **(3) LA SOGLIA VA GUARDATA SUGLI ARCHI CHE PASSANO, non sul mediano della rete**

`soglia_su_g1`. E lo stato dell'ipotesi del guardiano si scrive ### **cosi', e non in un
altro modo:**

> ### **<<FALSA al mediano della rete** *(l'errore e' del guardiano e lui lo dichiara)*,
> ### **SOSTENUTA sugli archi che entrano nella finestra.>>**

### ⛔ **ED E' UNA CORRELAZIONE, NON UNA CAUSA -- e il meccanismo per cui lo e' si puo'
### nominare:** l'insieme `g1` e' **definito** da `avv > soglia`, cioe' ### **si seleziona
condizionando su una soglia BASSA.** Un insieme scelto perche' la sua soglia e' stata
superata ### **ha per costruzione soglie piu' basse della rete, in QUALUNQUE braccio e con
QUALUNQUE meccanismo.** ### **Quindi <<la soglia e' bassa dove nascono>> non dimostra
<<nascono perche' la soglia e' bassa>>:** e' un effetto di **SELEZIONE**, e separarlo vuole
un **intervento** sulla soglia, non un'osservazione.

### ✖ **(4) LE DISTRIBUZIONI TARDIVE C'ERANO GIA', e la frase larga era MIA**

Avevo chiamato *<<lacuna della misura>>* l'assenza delle distribuzioni tardive.
### **I QUANTILI C'ERANO A OGNI PASSO** -- `avv`, `soglia`, **`soglia_su_g1`**, `ft`,
`segno`, `rapporto_avv_soglia`, `prob_su_g123` -- e la tabella della soglia ai passi `50`,
`70`, `100`, `140` ne e' la prova. ### **La lacuna riguardava le DISTRIBUZIONI PIENE** *(il
blocco `mod` col gradiente, il morso e `r` per nodo)*, **non i quantili**.
### ✔ **E l'aggiunta dei quattro passi resta utile** -- serve al blocco `mod`, che davvero
c'era a un passo solo -- ### **ma non era una lacuna sui quantili, e dirlo era un errore mio
di ampiezza.**

### CHE COSA RESTA A LUCA, e **non lo decido io**

**il peso `0.3`** della modulazione *(un numero **scelto**, che `A1` condanna)*, e
### **se le nascite della `PARTE A` fossero un ARTEFATTO.** ### ⛔ **E la misura con `DT`
dimezzato NON si avvia finche' Luca non lo dice.**

## ⛔ ANNOTAZIONE DEL 2026-10-05 — **UN'INFERENZA MIA E' RITIRATA: `dt_e` non entra
## una volta sola**

> ### **PAR.8: SI ANNOTA, NON SI RISCRIVE.** *(Obiezione del guardiano. ### **L'inferenza va
> RITIRATA, non riformulata** — e la lettura del codice l'ho **rifatta io**, non ricopiata.)*

### CHE COSA AVEVO SCRITTO, e perche' era sbagliato

Nel referto *(`12e2ca7`)*: *<<togliere il rallentamento uniforme da' **al massimo `x1.23`**
sugli eventi attesi **perche' entra una volta sola, nel fattore `(b)`**>>*, e ne deducevo che
il `x3.89` osservato in `Bc` venisse ### **dal gradiente.**
### ⛔ **LA PREMESSA E' FALSA.**

### IL CENSIMENTO DI `dt_e`, **rifatto sul codice, per riga**

| riga | dove entra |
|---|---|
| `:7795` / `:7799` | ### **LA SCARICA DELLA TORSIONE:** `self.tw += _w8(dph + twist_dip - twp) - dt_e * self.tw / _ttw` |
| `:7926`-`:7934` | il rilassamento di **`peq`** |
| `:8044` | **`dts = dt_e / nsub`**, il sotto-passo della metrica |
| `:8234` | il rilassamento viscoso di **`d0`** |
| `:8231` | il **tetto `CFL`** |
| `:7259`-`:7266` | **`_ft = dt_e/DT`**, cioe' il fattore `(b)` — ### **l'unico che avevo contato** |

### ⛔ **E ANCHE QUESTO CENSIMENTO ERA INCOMPLETO** — *annotazione del 2026-10-05, sulla
### stessa riga, come il guardiano chiede*

**Il guardiano ne ha trovato uno che mi mancava**, e ### **rifacendo la `grep` su `dt_e`,
`_dt_e_ultimo` e `_dte` ne ho trovato UN ALTRO che lui non nomina.** ### **Quindi non ne
mancava uno: ne mancavano DUE.**

**IL CENSIMENTO GIUSTO — `dt_e` entra in SETTE LEGGI:**

| # | riga | la legge |
|--:|---|---|
| `1` | `:7795` / `:7799` | la **SCARICA della torsione** |
| `2` | `:7924`-`:7934` | **`peq`** *(quattro rami: esatto/Eulero x tau locale/globale)* |
| `3` | `:8044` | **`dts = dt_e / nsub`**, i sotto-passi della metrica |
| `4` | `:8234` / `:8249` | il **rilassamento viscoso di `d0`** *(due rami: tau locale/`TAU_P`)* |
| `5` | `:8243`-`:8245` | ### **il LAPLACIANO di `d0` col suo clip `CFL`** — `_cfl = cs_taup*dt_e`, e `dt_e` e' **anche** nel termine: `clip(dt_e*cs_taup*d_arco*_lap_d0, -_cfl, +_cfl)`. ### **MANCAVA A ME E AL GUARDIANO** |
| `6` | `:8432` | **`_ft = dt_e/DT`** → la probabilita' di mitosi, cioe' il fattore `(b)` |
| `7` | `:8489`-`:8519` | ### **LA MEMORIA DI REPULSIONE, dentro `decidi_divisione`** — `_dte = _dt_e_ultimo`, `_rap = _dte/_tau_a`, `self._rep = rep + (self._rep - rep)*exp(-_rap)`, e poi `_rep` **spinge `d0`**: `spinta = 0.02*self.d0*_rep_mem` *(`:8551`)*. ### **IL SETTIMO DEL GUARDIANO** |

**Piu' il contorno, che NON sono leggi:** `:7439` la **definizione**
*(`dt_e = DT*0.5*(r_i+r_j)`)*, `:7474` il **riporto** in `_dt_e_ultimo`, `:8231` il **tetto
`CFL`** *(un registro diagnostico)*.

### ⚠ **E IL MIO <<SEI>> ERA SBAGLIATO IN DUE MODI, non in uno:** contava il tetto `CFL`
*(un diagnostico)* **come se fosse una legge**, e ### **ometteva sia il laplaciano di `d0`
che la memoria di repulsione.**

> ### ✔ **IL RITIRO DELL'INFERENZA RESTA COM'E': QUESTO LO RAFFORZA.** Con **sette** leggi
> invece di una, *<<`dt_e` entra una volta sola>>* non e' solo falso: ### **e' falso di
> un fattore sette.**
>
> ### ⛔ **E IL SETTIMO E' IL PIU' SCOMODO DI TUTTI, e va detto perche':** vive
> ### **DENTRO `decidi_divisione`**, cioe' **dentro la funzione che la misura stava
> analizzando**, e da li' **spinge `d0`** — che e' la lunghezza che il cancello `A13`/`2LAM`
> legge *(il fattore `(c)`)*. ### **Quindi `dt_e` tocca TUTTI E TRE i fattori della mia
> scomposizione**, non due: `(a)` per la scarica e il laplaciano, `(b)` per `_ft`, `(c)` per
> `_rep` → `d0`.

### LA LEZIONE, aggiornata

La prima volta avevo contato **uno**. La seconda, **sei** — ### **e due dei sei erano
sbagliati** *(uno di troppo, due di meno)*. ### **Un censimento si fa con lo strumento
(`grep`) e si RIFA quando qualcuno ne trova un pezzo**, perche' se ne manca uno
### **probabilmente ne manca un altro.**

### ⛔ **E LA SCARICA HA IL SEGNO OPPOSTO**

Un `dt_e` **piu' grande** rende `- dt_e*tw/_ttw` **piu' negativo**, cioe' ### **scarica la
torsione PIU' IN FRETTA** — **contro** le nascite. Quindi riscalare `r` cambia ### **anche
la popolazione che arriva nella finestra, cioe' il fattore `(a)`** — che e' il canale
**dominante**.

### ➜ **NEL BRACCIO `Bc` SI MUOVONO TRE COSE INSIEME**

il **gradiente** *(`+23 per cento`)*; la **probabilita' per arco** *(`ft` piu' grande,
**pro** nascite)*; la **velocita' di scarica della torsione** *(piu' veloce, **contro** le
nascite)*.
### **Da quel braccio NON SI SEPARANO**, e il `x3.89` ### **non si puo' attribuire a nessuno
dei tre.**

### ✔ **CHE COSA IL CONTROFATTUALE DICE ANCORA, e non e' poco**

### **Togliere il rallentamento uniforme NON riporta le nascite verso `Ap`** *(restano al
`5.7 %`)*. ### **PERCHE' no, questo braccio non lo dice.**

### E LA LEZIONE, che e' la stessa di tre volte in due giorni

Avevo contato **un** consumatore di `dt_e` e concluso **<<una volta sola>>**.
### ⛔ **Un'inferenza che poggia su un censimento NON FATTO e' un'asserzione travestita** —
e `P1` dice esattamente questo: *non usare l'associazione senza verificare*.
### **Il censimento costa una `grep`.**

## 3. TODO DEL NEXT STEP — **operativo**

1. **commit di questo task history**, prima dello strumento;
2. lo **strumento** `csv/_test_fork/_crescita_dopo_z43.py`: quattro bracci, tre ganci
   contati, il controfattuale dichiarato, il **collaudo**;
3. **commit dello strumento**, prima della corsa;
4. la **corsa**: `150` passi, seme `11`, scena del driver;
5. i **quattro controlli** `C1`-`C4`, e `FERMO` se `C1` o `C3` falliscono;
6. il **referto** `doc/REFERTO_crescita_dopo_z43_2026-10-05.md`, **generato**, coi blob;
7. la **relazione** e le voci nell'indice, **nello stesso giro**;
8. la **voce nuova `GRAVITA-POTENZIALE`** *(decisione di Luca, da curare dopo)*,
   registrata **nello stesso giro** di questo mandato.
