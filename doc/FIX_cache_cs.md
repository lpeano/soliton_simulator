# FIX — la cache `_cs_nodo_prev` veniva scartata a ogni mitosi

**Data:** 2026-09-15 · **Branch:** `fork-su2` · **Blob PRIMA:** `7d484580` · **Blob DOPO:** vedi commit
**Regola par.5-ter:** relazione scritta nel momento del riscontro, prima di passare al pezzo dopo.

---

## 1. IL DIFETTO (confermato dal codice e misurato)

`_cs_nodo_prev` e' scritta a **fine passo** con l'`n` di quel passo (riga ~2918, dentro
`CS_DINAMICO and (FORK_SU2_MEM or STEP2_OROLOGIO)`). La **mitosi aggiunge nodi**, quindi al passo
successivo la guardia di `_tempo_luce_nodo`

```python
if csp is not None and len(csp) >= n:
```

fallisce e si cade nel ramo `else` -> `cs_nodo = CS_M` **costante**.

**Misurato sul file PRIMA della patch** (scena 3 masse, seme 1, 30 passi):
**cache inusabile in 24 passi su 30**, fallback in **23 chiamate su 32 = 71.88 %**.
(Il prompt riportava ~80 % su una scena leggermente diversa; l'ordine di grandezza coincide.)

**Chi ne risente:** `_tempo_luce_nodo` ha **due** chiamanti — `_bloch_ritardato` (riga 2462, **lo
STRATO 1, gia' sigillato 23/23**) e il rilassamento sotto `--tau-luce` (riga 1947). Quindi lo Strato 1
ha girato con `cs` congelato a `CS_M` per circa tre quarti dei passi da quando e' stato cablato.

**Perche' nessun sigillo l'ha visto:** il ramo `else` **non e' un errore** — e' il fallback legittimo
per `--cs-dinamico` OFF e per il primo passo. Il codice fa quello che dice; e' la **condizione** a
essere sbagliata in presenza di mitosi. Niente NaN, niente runaway, nessuna byte-identita' violata.

**Vie di crescita dei nodi (verificato dal sorgente, non per analogia):** sono **tre** —
mitosi (`:3192`), Schwinger (`:3309`) e **`semina()` (`:1600`)**. Le prime due passano da
`_eredita_spinore_figli`, la terza **no**. `semina()` in volo si attiva solo con `semina_cont`, che e'
**`False` di default** e si accende **unicamente dalla GUI** (`:4610`, `:4753`): nei run batch — da
cui vengono tutte le misure di questo programma — le vie vive sono due, ed entrambe sono curate.
**La terza resta scoperta sul percorso GUI** ed e' registrata in `RAMIFICAZIONI.md` (voce H).

---

## 2. LA CURA

Il figlio **eredita `cs` dal padre**, esattamente come `_nb_ret`, `_nb_prec`, `omega_s`,
`_psi_spinor`, `_psi_prec`: e' la **stessa convenzione**, in un **sesto** punto dello stesso blocco.
Zero parametri, zero floor, zero valori nuovi.

Una scelta di collocazione, dichiarata: l'estensione sta **PRIMA** della guardia
`if not (SPINORE_CORRETTO or CAMPO_SPINORIALE): return`, perche' questa cache vive sotto
`CS_DINAMICO and (FORK_SU2_MEM or STEP2_OROLOGIO)`, **non** sotto `--spinore-corretto`: metterla dopo
avrebbe lasciato il difetto vivo proprio nei run **STEP 2**. Se la cache non esiste (flag OFF) e' un
**no-op esatto**, ed e' quello che P1 dimostra.

Non e' stato toccato: la guardia, il ramo `else`, la scrittura a fine passo, nient'altro.

---

## 3. IL CONTATORE (par.9, presidio nuovo)

Il ramo `else` ora e' strumentato: `_cs_chiamate`, `_cs_fallback`, `_cs_fallback_ultimo`.
Diagnostici puri: non consumano RNG, non sono riletti da nessuna grandezza fisica.

> **Ogni ramo `else` / fallback / `getattr(..., default)` su un percorso FISICO va strumentato con un
> contatore.** Un fallback mai misurato e' un comportamento sconosciuto — e uno che scatta il 72 %
> delle volte **non e' un fallback, e' il comportamento principale.**

---

## 4. I SIGILLI — **5/5 PASS** (`csv/_seal_fork/_sigillo_fix_cache.txt`)

| | esito | numeri |
|---|---|---|
| **P1** byte-identita' a flag OFF | **PASS** | `n_A = n_B = 1692` (CONFRONTABILI), 21 campi, `max|A-B| = 0.000e+00`, stato RNG identico |
| **P1b** controllo: col flag ON devono DIFFERIRE | **PASS** | `n = 1821` contro `1771` — la patch **e' viva**, non e' codice morto |
| **P2** il contatore | **PASS** | **71.88 % -> 0.00 %** (23/32 -> 0/32) |
| **P3** `len(cache) == n` a ogni passo | **PASS** | passi inusabili: **24/30 -> 0/30** |
| **P4** stabilita' | **PASS** | `|nb|-1 = 2.2e-16`, NaN/inf **0**, `cs` finito e positivo, `tau` finito |

**P1b non era nel mandato: l'ho aggiunto.** Senza, una patch che non fa **nulla** passerebbe P1, P3 e
P4 e fallirebbe solo P2 — e P2 da solo non distingue "la cache e' lunga giusta" da "la cache lunga
giusta serve a qualcosa". Il controllo necessario e' che il **risultato fisico** cambi.

---

## 5. IL NUMERO CHE CAMBIA LA LETTURA DEL §4 — **scritto PRIMA della ri-misura**

P4 misura anche la **dispersione di `cs` riparato**:

```
cs cache: min 1.99954   max 2   (CS_M = 2)      max/min = 1.000230
```

**`cs` varia dello 0.023 %.**

Da qui segue una cosa che va detta **prima** di rifare T3, altrimenti diventa una scusa a posteriori:

> **La premessa quantitativa del mandato non regge.** Il mandato dice: *«l'effetto di `tau = d/cs`
> puo' esistere solo quando `cs` varia, cioe' in un quinto dei passi; con la cache attiva 1/5 del
> tempo, un effetto dimezzato e' quello che deve succedere»*.
> **Non segue.** Il fallback **non disattivava** `tau = d/cs`: lo calcolava come `tau = d/CS_M`.
> Il fattore **`d` era vivo nel 100 % dei passi.** Cio' che la FASE 2 sostituisce e'
> `TAU_A*max(dens/dens_rif, 0.05)` con `d/cs`, e quasi tutto quel cambiamento sta in **`d`**, non in
> `cs`. Il difetto congelava **solo** il fattore `cs`, che vale **1.000230** di escursione totale.

**PREDIZIONE, con la soglia scritta prima:** la pendenza T3 col flag ON **non si muovera' in modo
misurabile** — `|Delta pendenza|` sotto il proprio `SE`, cioe' sotto ~0.01. Se e' cosi', per la
lettura fissata dal mandato stesso vale l'esito **«il bug non era la causa: resta un residuo vero da
capire. Non inventare una spiegazione: riporta e fermati.»**

**La cura resta giusta comunque**, e per una ragione indipendente dal residuo: `cs` e' quasi-costante
**oggi**, alle densita' attuali (par.6: *«a densita' reali cs e' MORTO, I~0.05 contro soglia ~400»*).
Il giorno in cui `cs` sara' vivo, una cache scartata a ogni mitosi sarebbe un difetto **grande**, e lo
sarebbe in silenzio. Si ripara ora, mentre e' innocuo e dimostrabile.

---

## 6. ESITO DELLA RI-MISURA T3 — **LA MIA PREDIZIONE E' SMENTITA**

Quattro bracci, 300 passi, seme 1, scena 3 masse (`csv/_test_fork/_rimisura_t3.py`, committato
**prima** del run in `22a7c41`; output `csv/_test_fork/_rimisura_t3.txt`).

| braccio | pendenza | SE | r^2 | n | IC95 | theta mediana | fallback |
|---|---|---|---|---|---|---|---|
| **PRE  OFF** | **-0.1685** | 0.0090 | 0.126 | 2417 | [-0.1862, -0.1507] | 129.51 giri/passo | non strumentato |
| **PRE  ON**  | **-0.4265** | 0.0091 | 0.464 | 2534 | [-0.4444, -0.4086] | 43.55 giri/passo | non strumentato |
| **POST OFF** | **-0.1491** | 0.0085 | 0.109 | 2517 | [-0.1658, -0.1324] | 131.27 giri/passo | **0 / 302** |
| **POST ON**  | **-0.4710** | 0.0107 | 0.417 | 2690 | [-0.4921, -0.4500] | 42.81 giri/passo | **2 / 608** |

> **DIFFERENZA ON(post) - ON(pre) = -0.0445 +- 0.0141, z = 3.16.**
> **La predizione del §5 era: `|Delta|` SOTTO il proprio SE. E' FALSA.** Lo scrivo prima di
> qualunque commento: **ho predetto zero e ho misurato un effetto a 3 sigma.**

**Il braccio di controllo ha fatto il suo lavoro:** `PRE ON = -0.4265` riproduce il **-0.43** gia'
registrato in `doc/SIGILLO_tau_luce_FALLITO.md`, quindi la scena e' la stessa e i numeri sono
confrontabili con quelli storici. Non e' un confronto fra scene diverse.

### Cosa la patch ha e non ha recuperato

| | |
|---|---|
| attesa FASE 1 (stima **onesta**) | **-0.69** |
| ON prima della patch | **-0.4265** |
| ON dopo la patch | **-0.4710** |
| **frazione del divario recuperata** | **16.9 %** |
| divario **ancora** aperto | **-0.219** |

**Per la lettura fissata PRIMA dal mandato, questo e' il caso "valori intermedi": si riporta il
numero e la frazione, senza forzare.** Non e' ne' *«la meta' mancante ERA il bug»* (sarebbe servito
~50 %, e servirebbe una pendenza fra -0.7 e -1.0), ne' *«la pendenza resta ~ -0.43»*. **Il bug
contribuiva, e contribuiva poco: un sesto.** La FASE 2 **non si chiude**, e **resta un residuo vero
da capire** — che e' l'esito che il mandato prescrive di riportare **senza inventare spiegazioni**.

### Dove il mio ragionamento del §5 ha sbagliato

Avevo scritto: *«`cs` varia dello 0.023 %, quindi non puo' produrre uno spostamento di pendenza»*.
**L'errore sta nell'aver confrontato l'escursione di `cs` con l'ampiezza della pendenza.** Non sono
la stessa cosa: una pendenza trasversale non misura **quanto** `cs` varia, misura **come la sua
variazione e' CORRELATA con l'inerzia**. Un fattore che cambia dello 0.023 % ma **sistematicamente
nella stessa direzione** lungo l'asse dell'inerzia sposta la pendenza; uno che cambia del 50 % a caso
non la sposta. **Ho applicato un argomento di AMPIEZZA a una domanda di CORRELAZIONE.** Resta vero
che `d` era vivo nel 100 % dei passi e che quasi tutto l'effetto della FASE 2 sta in `d` — il **6/7**
del divario tuttora aperto lo conferma — ma la conclusione *«non puo' muoverla affatto»* **era
sbagliata**, e la misura la smentisce a 3 sigma.

### ⚠ E UN DUBBIO SUL METRO, che vale in ENTRAMBE le direzioni

`z = 3.16` e' costruito con le `SE` **interne a un singolo run** (l'errore di campionamento della
retta **dentro** quel run). Ma i due bracci ON sono **due traiettorie diverse di un sistema
caotico** — `N = 3999` contro `4100` — e la variabilita' **da run a run** non e' quella barra.
**Il valore sotto ipotesi nulla qui non e' zero:** e' la dispersione fra due run che differiscono
solo per una perturbazione numericamente irrilevante, e **quella non e' stata misurata.**

Lo scrivo **contro** la mia stessa posizione, non a suo favore: e' un'obiezione che indebolirebbe
allo stesso modo una conferma. E per `CLAUDE.md` par.2.7 (*mai su un solo seme*) va **misurata**, non
discussa.

---

## 7. IL CONTROLLO SUI SEMI — **il `z = 3.16` era DISPERSIONE DI RUN. Il "16.9 %" si RITIRA.**

`csv/_test_fork/_controllo_semi.py` (committato **prima** del run, `87f90d7`; output
`csv/_test_fork/_controllo_semi.txt`), 3 semi x 2 bracci, 300 passi, stessa scena.

| seme | ON **pre**-patch | ON **post**-patch | `Delta` |
|---|---|---|---|
| 1 | -0.4265 +- 0.0091 (N 3999, 43.55 giri) | -0.4710 +- 0.0107 (N 4100, 42.81 giri) | **-0.0445** |
| 2 | -0.4846 +- 0.0099 (N 3183, 32.50 giri) | -0.4479 +- 0.0082 (N 3121, 30.70 giri) | **+0.0367** |
| 3 | -0.4412 +- 0.0080 (N 3997, 44.85 giri) | -0.5047 +- 0.0116 (N 3768, 41.82 giri) | **-0.0635** |

> **Il segno NON e' concorde.** Il seme 2 va **nella direzione opposta**.
> `media(Delta) = -0.0238`, dev.std `0.0532`, **SE della media `0.0307`, `t = -0.77` (2 gdl)**.

### Il nullo, che nessuno aveva misurato

| | |
|---|---|
| `SE` **interna** a un singolo run (quella del `z = 3.16`) | **~0.010** |
| dispersione **FRA SEMI** a codice invariato, ramo pre | **0.0302** |
| dispersione **FRA SEMI** a codice invariato, ramo post | **0.0286** |

> **La barra giusta e' TRE VOLTE quella che avevo usato.** Su un sistema caotico la pendenza
> trasversale cambia da run a run di **0.03** *senza che il codice cambi*: e' il valore sotto
> ipotesi nulla, ed era **zero solo nella mia testa**.

### Cosa cade e cosa regge

**CADE** — `z = 3.16` e **"16.9 % del divario recuperato"**: **non sono numeri riportabili.** Si
ritirano dal par.6, da `RAMIFICAZIONI` C8, da `CLAUDE.md` par.9 e dalla relazione.

**NON E' UNA CONFERMA DELLA MIA PREDIZIONE.** `IC95` su `Delta` (t, 2 gdl) = **[-0.1560, +0.1084]**,
ampiezza **0.26**: contiene lo **zero** *e* contiene il **-0.1196** che l'ipotesi "~meta'" del
mandato richiederebbe. **Tre semi non decidono niente su questa domanda.** L'unica frase onesta e':
**l'esperimento non ha la potenza per distinguere un effetto della cura da zero.** Il mio errore di
ragionamento del par.6 (ampiezza contro correlazione) **resta un errore**; semplicemente, la misura
che sembrava dimostrarlo non lo dimostrava.

**REGGE, e robustamente:**

| affermazione | numero | contro la barra giusta (0.03) |
|---|---|---|
| **la FASE 2 non si chiude** | ON post medio **-0.4745**, divario verso -0.69 = **-0.2155**, SE della media **0.0165** | **z = 13.1** |
| **`--tau-luce` fa qualcosa di grande** | contrasto ON-OFF **-0.3219** | **11 volte** la dispersione fra semi |
| `theta` resta aliasato | **30.7 - 44.9 giri/passo** su tutti e sei i run | fuori scala |

### La cura resta, per la ragione che non dipende da questa misura

Il difetto era **reale e misurato** (fallback **71.88 % -> 0.00 %**, cache inusabile **24/30 -> 0/30**,
sigillo **5/5 PASS**): quelli restano. Cio' che si ritira e' l'**effetto fisico attribuito alla cura**,
non la cura. E resta valida la ragione indipendente: `cs` e' quasi-costante **oggi**; quando sara'
vivo, una cache scartata a ogni mitosi sarebbe un difetto **grande**, e lo sarebbe in silenzio.

---

## 9. T3 RIFATTO SUL SISTEMA PULITO (entrambe le cure) — **il numero, senza attribuirlo**

`csv/_test_fork/_rimisura_t3_pulito.txt`, 4 bracci, 300 passi, seme **1**, **con `--cs-dinamico`**
(riga 24 di `_rimisura_t3.py`), blob `08784685`.

| braccio | pendenza | SE | r² | n | IC95 | `theta` | fallback cache |
|---|---|---|---|---|---|---|---|
| PRE OFF | -0.1685 | 0.0090 | 0.126 | 2417 | [-0.1862, -0.1507] | 129.51 giri/passo | n/d |
| PRE ON | -0.4265 | 0.0091 | 0.464 | 2534 | [-0.4444, -0.4086] | 43.55 | n/d |
| **POST OFF** | **-0.1024** | 0.0071 | 0.088 | 2146 | [-0.1164, -0.0884] | 128.88 | **0/302** |
| **POST ON** | **-0.4555** | 0.0082 | 0.567 | 2364 | [-0.4715, -0.4394] | **38.99** | **2/608** |

### ⚠ IL «11.0 %» STAMPATO DALLO SCRIPT **NON E' UN RISULTATO**

Lo script calcola `Delta = -0.0290 +- 0.0122`, `z = 2.37`, e ne deriva «11.0 % recuperato».
**Non si riporta come numero**, per la ragione **gia' misurata oggi** (**C10**): quella `SE` e'
**interna a un singolo run**, mentre la dispersione **fra semi** su questa stessa osservabile vale
**~0.030**. Con `Delta = 0.029` e barra `0.030`, **non c'e' effetto misurabile: c'e' un seme.**

> **E' esattamente il 16.9 % di stamattina, con un'altra cifra.** Quel numero aveva `z = 3.16` su un
> seme ed e' stato **ritirato** quando tre semi hanno dato segno **non concorde**
> (-0.0445 / **+0.0367** / -0.0635, `t = -0.77`). **Non lo rifaccio.**
> Il mandato lo dice con parole sue: *«dopo tre errori consecutivi sullo stesso numero, la
> disciplina e' smettere di predirlo»*. **Aggiungo: e smettere di riportarlo su un seme.**

### COSA REGGE, contro la barra giusta

| affermazione | numero | contro 0.030 (fra semi) |
|---|---|---|
| **la FASE 2 NON si chiude** | divario POST ON verso `-0.69` = **-0.2345** | **z ≈ 7.8** |
| `--tau-luce` ha un effetto **grande** | contrasto ON-OFF **-0.3531** | **~12 volte** |
| `theta` resta **ALIASATO** | **38.99 giri/passo** nel braccio migliore | fuori scala |

### Un dettaglio che il contatore rende visibile

`fallback 2/608` nel braccio POST ON: la cache cade nel ramo `else` **2 volte su 608 chiamate
(0.33 %)** — il primo passo di ciascun braccio, dove un passato **non esiste ancora**. E' il
comportamento atteso **dopo** la cura, ed e' verificabile perche' il contatore c'e'.
