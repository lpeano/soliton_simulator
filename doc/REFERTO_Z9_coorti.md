# REFERTO — **`Z9` per coorte: il kernel è al `7.5 %` del suo valore maturo, e la mediana di popolazione sottostima di `2.5×` la coorte che conta**

**Data:** 2026-09-18 · **Blob `b9e07c73` INVARIATO** — **nessun run nuovo**, i dodici `.pkl` esistevano
**Task history con la derivazione, committato PRIMA:** `efd7a34` · **Previsioni:** `f3895aa`
**Sonda:** `_z9_coorti.py` · **Output:** `csv/_test_fork/_z9_coorti.txt`

> **⚠ IN TESTA:** **`--tau-luce` HA IL SIGILLO FALLITO** (par.0): **ramo NON CERTIFICATO, e ogni
> numero lo eredita.** **`--chi-basc` attivo.** **UN SEME per scena, sei istanti.**
> **⚠ LA COORTE È ANAGRAFICA, NON PER MASSA.** **NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.**
> **Si è MISURATO, non curato: `TAU_A`, `ramp` e `_pesi()` NON sono stati toccati.**

---

## 0. ⚠ IL §4.1 — **i `.pkl` esistenti: la risposta è DOPPIA**

**① IL PRESIDIO DEL BLOB FUNZIONA, ed è stato PROVATO, non asserito:**

```
r.carica_stato("csv/_test_fork/_gvideo/frame_400.pkl")
-> RuntimeError: DB RIFIUTATO: codice diverso (blob DB=a1ae5090... vs ora=b9e07c73...)
```

**② MA LA MISURA NON PASSA DA `carica_stato`:** le sonde leggono `["attrs"]` direttamente, e quel
dizionario ha **110 chiavi** leggibili.

**③ ⚠ E QUELLO CHE MANCA È ESATTAMENTE IL TRACKING:** `conc_nodi`/`conc_archi`/`masse_info` **assenti
in entrambe le scene** — è `Z53`, e i dodici `.pkl` vengono dal blob `a1ae5090`.

> **QUINDI: la domanda «i nodi di QUESTA MASSA maturano?» RESTA SENZA RISPOSTA, e non la sostituisco
> fingendo che sia la stessa.** Ho risposto a **«i nodi nati in QUESTA FINESTRA maturano?»**, che è
> l'altra delle due definizioni che il mandato nomina. **Per la prima servirebbe rigirare una scena
> col blob nuovo, e non l'ho fatto.**

**La coorte anagrafica è ESATTA, non stimata:** i nodi si appendono in coda (`:3958`) e nascono con
`eta = 0` (`:3961`, `:4082`, `:1849`). **Sei snapshot → sei finestre di nascita esatte.**

---

## 1. ⚠ LA LEGGE — **si DERIVA dal codice, e la misura la conferma allo `0.3 %`**

```
:3236  self.eta += dt_n      :3038  dt_n = DT * r      :2649  ramp = min(1, eta/TAU_A)
```

> **`d(eta)/d(passo) = DT · r` ESATTAMENTE, per nodo.**
> **`passi(ramp = 1) = TAU_A / (DT · r) = 5000 / r`.**

**Il `~0.009/passo` di `Z9` corrisponde a `r ≈ 0.9`: è il tasso di UN NODO con un ritmo particolare,
non una proprietà del sistema.** **È il difetto che il rilievo di Luca denuncia, e adesso ha un nome:
`Z9` aveva scambiato un valore di `r` per una costante.**

**IL FALSIFICATORE FISSATO PRIMA** *(«se `d(eta)/d(passo)` misurato non coincide con `DT·r` letto, mi
fermo»)* **NON SCATTA:**

```
TRE   intervallo   deta/dpasso    DT*r letto     rapporto MED
      10->115       7.639e-03      1.369e-02        0.6250
      115->190      9.372e-03      1.103e-02        0.8123
      190->270      8.153e-03      8.929e-03        0.9679
      270->375      6.472e-03      7.068e-03        0.9977
      375->400      7.553e-03      7.683e-03        0.9966
```

**Negli ultimi due intervalli il rapporto vale `0.9977` e `0.9966`: la derivazione è confermata entro
lo `0.3 %`.** **Nel primo vale `0.625`, e la ragione è MISURATA, non ipotizzata:** al frame 10
`r` mediano vale **`1.414119`**, cioè **`√2` — il TETTO di `ritmo()`** — e scende a `~1.0`.
**`r` campionato ai due ESTREMI non cattura un `r` che si muove dentro l'intervallo.**
**Serviva uno scarto di ORDINI per rompere la derivazione: non c'è.**
*(Scena DUE: `0.807 / 1.038 / 0.780 / 0.737 / 0.940` — oscilla intorno a 1 entro il `±26 %`.)*

### 1.1 ⚠ E IL FATTO PIÙ PULITO DEL GIRO — **`eta` è un TEMPO PROPRIO, e si vede**

**Al frame 10 tutti i `2391` nodi hanno la STESSA età anagrafica — `60` passi — ma `eta` va da
`0.2722` a `0.5049`: un fattore `1.85`.**

> **Stessa età, tempi propri diversi dell'85 %.** **Non è un artefatto: è `dt_n = DT·r` che fa il suo
> mestiere.** **E rende impossibile per costruzione UN tempo di maturazione: ce n'è uno per nodo.**

---

## 2. ① LA MATURAZIONE PER COORTE — **e la mediana di popolazione SOTTOSTIMA di `2.5×`**

**All'ultimo istante (frame 400 = passo 2400):**

```
TRE MASSE              nodi    ramp MED   ramp p95   fr>0.5    fr>0.9
presenti al f10        2391     0.3212     0.6110    0.3768    0.0000
nati f10 -> f115       1204     0.3214     0.5573    0.1902    0.0000
nati f115 -> f190       712     0.2212     0.4484    0.0000    0.0000
nati f190 -> f270      1136     0.1702     0.3295    0.0000    0.0000
nati f270 -> f375      2037     0.0761     0.1952    0.0000    0.0000
nati f375 -> f400       538     0.0093     0.0362    0.0000    0.0000
TUTTA LA POPOLAZIONE   8018     0.2171     0.5959    0.1409    0.0000

DUE MASSE              nodi    ramp MED   ramp p95   fr>0.5    fr>0.9
presenti al f10        1895     0.3264     0.5693    0.3821    0.0000
TUTTA LA POPOLAZIONE   5878     0.2207     0.5480    0.1538    0.0000
```

> **`ramp > 0.9`: ZERO. In ogni coorte, a ogni istante, in entrambe le scene.**
> **`ramp > 0.5`: il `37.68 %` (TRE) e il `38.21 %` (DUE) della coorte ORIGINALE.**
> **Contro il `14.09 %` e il `15.38 %` della POPOLAZIONE.**
> **RAPPORTO `2.67` e `2.48`: la statistica di popolazione sottostima di due volte e mezzo la
> maturità della coorte che porta la struttura.** **Il rilievo di Luca è confermato con un numero.**

### 2.1 ⚠ DUE MIE PREVISIONI CADONO, E LE SCRIVO

- **PREVISIONE 1, metà sbagliata:** avevo scritto *«credo nemmeno a `ramp > 0.5`»*. **Falso: oltre un
  terzo della coorte originale ci arriva.** **I nodi originali MATURANO, quando il tempo c'è.**
- **PREVISIONE 2 — il mio CONTROLLO DI SANITÀ — fallisce per un pelo:** al frame 400 la coorte
  `f10→115` ha `ramp` mediano **`0.3214`** contro **`0.3212`** dell'originale *(e `0.3319` contro
  `0.3264` a due masse)*. **Avevo scritto che se l'ordinamento non regge è colpa MIA.**
  **⚠ Ma NON è un errore di assegnazione, e lo verifico DAI DATI:** la coorte più giovane ha
  `eta max = 2.05` (TRE) e `2.08` (DUE) al frame 400, contro i `150 passi × DT × r ≈ 2.06` attesi.
  **L'assegnazione è confermata dal suo stesso limite superiore.** **L'inversione è REALE, è nella
  quarta cifra, e non la spiego** — non ho una misura che la spieghi, e non invento.
- **PREVISIONE 3 non è confermata come formulata:** prevedevo la coorte originale **la più larga**.
  In termini RELATIVI è la più STRETTA: `p95/p05` vale **`2.99`** per l'originale contro **`3.67`**
  per la seconda. **In termini assoluti ha la `p95` più alta (`30.55` contro `27.86`)** — **le due
  letture dicono cose diverse, e riporto entrambe invece di scegliere quella che mi dà ragione.**

---

## 3. ② IL TASSO — **e il `93 %` di `Z46` NON si ripresenta**

```
        FERMI (r/r_floor < 2) su len(r)
TRE     0/2391  8/3595  0/4307  0/5439  0/7477  0/8013
DUE     0/1895  3/2906  0/3347  0/4083  46/5461 3/5874
```

> **Nella scena VIDEO la popolazione al pavimento è ZERO o dell'ordine di POCHE UNITÀ.**
> **Nel batch di `Z46` era il `92.7 %`.**

**⚠ E va detta con A3c, non trasportata:** `Z46` misura il **batch a 1200 passi** (`_g1200`), questa è
la **scena N-MASSE video**. **Sono scene diverse.** **Quello che si può dire è che la frazione al
pavimento NON è una proprietà del sistema: è una proprietà della SCENA** — e questo **qualifica**
`Z46`, non lo smentisce. **PREVISIONE 5 CONFERMATA**, ed era la sola che avevo marcato come «può
cadere».

**L'ESTRAPOLAZIONE, per gruppo:**

```
TRE   r MED mobili = 1.071354   -> passi(ramp=1) = 4667    (la scena ne ha 2400: 51.4 % del cammino)
DUE   r MED mobili = 0.935469   -> passi(ramp=1) = 5345    (la scena ne ha 2400: 44.9 % del cammino)
```

---

## 4. ③ LE CONSEGUENZE — **il kernel gira al `7.5 %`, e NON è un'ampiezza pura**

**`base = exp(-d/lam) · ramp[i] · ramp[j] · exp(α·tau/(1+β·tau))`** *(`:2650`, `:586`)*.
**L'assoluto NON è stato ricostruito**, e la ragione è nel codice: `_lam_archi → lambda_nodi →
massa_critica_adattiva → i pesi` è **una catena RICORSIVA con un ramo di guardia**, e ricostruirla
fuori dal simulatore è **l'errore già fatto su `correzione`** (due termini, uno dimenticato, metà
coppia). **Ma non serve:** i due fattori non-`ramp` **sono identici** nel kernel acerbo e in quello
maturo, **e si CANCELLANO**:

> **`base / base_maturo = ramp[i] · ramp[j]`, ESATTO. È un calcolo, non un run.**

```
TRE   frame   archi     | p05        MEDIANA    p95        | fr>0.01  fr>0.5  fr>0.9
      10      429498    | 4.345e-05  9.907e-05  1.002e-04  | 0.0000   0.0000  0.0000
      115     431022    | 6.493e-03  9.352e-03  2.233e-02  | 0.4189   0.0000  0.0000
      190     431930    | 1.518e-02  2.237e-02  6.313e-02  | 0.9969   0.0000  0.0000
      270     433380    | 2.541e-02  4.037e-02  1.403e-01  | 0.9965   0.0000  0.0000
      375     435959    | 3.877e-02  6.907e-02  3.048e-01  | 0.9954   0.0000  0.0000
      400     436636    | 4.122e-02  7.454e-02  3.527e-01  | 0.9951   0.0000  0.0000

DUE   400     311292    | 3.367e-02  5.527e-02  2.893e-01  | 0.9943   0.0000  0.0000
```

> **Il kernel tipico gira al `7.45 %` (TRE) e al `5.53 %` (DUE) del suo valore maturo.**
> **E NESSUN arco supera `0.5`. Mai. In nessuna delle due scene, a nessun istante.**

### 4.1 ⚠ PREVISIONE 7 SBAGLIATA, e di parecchio

Avevo previsto **`base/base_maturo < 0.01` per la stragrande maggioranza**. **Misurato: il
`99.51 %` degli archi è SOPRA `0.01`.** **Avevo sbagliato per un fattore `7.5` sulla mediana e nel
verso opposto sulla frazione.**

### 4.2 ⚠ PREVISIONE 6 SBAGLIATA NEL SEGNO — **e la spiegazione l'ho MISURATA, non scritta**

```
TRE  ramp MED nodi = 0.21711  ->  il suo QUADRATO = 0.047135
     base/base_maturo MEDIANO misurato = 0.074540      (rapporto 1.5814)
DUE                                       0.055270      (rapporto 1.1347)
```

Avevo previsto il prodotto **più piccolo** del quadrato *(«pesa il minore dei due»)*. **È più
grande.** Mi era venuta subito una spiegazione — *gli archi connettono nodi coetanei* — **e una
spiegazione in testa non è una misura.** **Misurata, col nullo accanto:**

```
corr(ramp[i], ramp[j]) sugli archi =  +0.8015 (TRE)   +0.8569 (DUE)
NULLO (estremo j rimescolato, 5 volte) = +0.0027 +0.0012 -0.0014 +0.0009 +0.0002
```

> **`+0.80` contro un nullo di `±0.004`: DUECENTO volte il nullo.**
> **Gli archi sono ASSORTATIVI PER ETÀ.** **La spiegazione regge — ma adesso è un numero.**

### 4.3 ⚠ «DIVERSO O SOLO PIÙ FORTE» — **risposta PARZIALE, e il resto è NON RISPOSTO**

**Avevo previsto (previsione 8) di non poterlo decidere senza un run. Lo confermo per la parte
fenomenologica — ma una parte si decide, ed è più di quanto avessi previsto:**

**Se `ramp[i]·ramp[j]` fosse COSTANTE su tutti gli archi, sarebbe un'AMPIEZZA PURA:** riscalerebbe
tutti i pesi dello stesso fattore, e ogni legge che normalizza su somme locali sarebbe invariata.
**Non lo è:**

```
p95/p05 di base/base_maturo:   frame 10 -> 2.31        frame 400 -> 8.56 (TRE),  8.59 (DUE)
```

> **Il fattore di immaturità VARIA di `8.6` volte da arco ad arco, e la variazione è CORRELATA
> con l'età (`+0.80`).** **Quindi il kernel acerbo NON riscala i pesi: li RIPESA**, e li ripesa
> **sistematicamente a favore dei legami vecchio-vecchio.**
> **⚠ MA QUESTO NON DICE CHE LA FENOMENOLOGIA SIA DIVERSA:** dirlo richiederebbe far girare il
> sistema col kernel maturo, cioè **≥ 4667 passi** oppure **forzare `ramp = 1`, che è CABLARE** ed è
> vietato dal mandato. **QUELLA PARTE RESTA NON RISPOSTA, e non invento una misura sostitutiva.**

---

## 5. ④ IL CRITERIO NUOVO — **il deliverable**

**`Z9` non si chiude: si RISCRIVE in modo che si possa chiudere.** Due pezzi.

### Z9-a — **LA CONDIZIONE DI REGIME, da dichiarare in OGNI referto che usi una scena**

```
passi_mancanti = TAU_A / (DT * r_MED_MOBILI)  -  passi_fatti
```

con **`r` LETTO da `_r_corrente`** *(mai stimato da `eta`: sarebbe circolare, `eta` cresce PER `r`)*
e la mediana presa **sui soli MOBILI** *(mai su tutta la popolazione: A3c)*.

**Oggi: `4667 − 2400 = 2267` passi (TRE), `5345 − 2400 = 2945` (DUE).**
**Zero numeri scelti: `TAU_A` e `DT` sono nel codice, `r` è nei dati.**

### Z9-b — **IL CRITERIO DI CHIUSURA, e PUÒ FALLIRE**

> **`Z9` si chiude quando `median(ramp[i]·ramp[j])` sugli archi INTERNI alla coorte originale
> vale `1`** — cioè quando **l'arco tipico più vecchio è SATURO.**

**Non contiene nessuna soglia scelta (A1):** `ramp = min(1, eta/TAU_A)` **satura in un punto ESATTO**,
`eta = TAU_A`. **«Maturo» è un evento netto, non un taglio.**

```
                                       TRE       DUE
median(base/base_maturo) archi interni  0.074950  0.055417     <- deve valere 1
frazione di archi MATURI (entrambi gli estremi eta >= TAU_A)  0.000000  0.000000
```

> **NON SODDISFATTO, di un fattore `13` e `18`.** **E la frazione di archi maturi è ZERO ESATTO.**
> **PREVISIONE 9 CONFERMATA** — ed era scritta proprio perché il criterio potesse smentirla.

**E PUÒ FALLIRE DAVVERO:** se il sistema smettesse di maturare — `r` che scende al pavimento — il
numero **smetterebbe di crescere** e il criterio resterebbe **aperto per sempre**. **È esattamente
ciò che è successo nel batch di `Z46`**, dove il `92.7 %` dei nodi ha `r/r_floor = 1.0000`.

### 5.1 ⚠ E LA PARTE DEL MIO CRITERIO CHE **OGGI NON FA LAVORO** — A9

**La restrizione «archi INTERNI alla coorte originale» serviva a togliere la diluizione dei neonati.
MISURATA, oggi non toglie niente:**

```
median su archi INTERNI all'originale : 0.074950      (TRE)    0.055417  (DUE)
median su TUTTI gli archi             : 0.074540               0.055270
```

**Differiscono nella QUARTA cifra.** **Perché:**

```
             nodi            grado MEDIANO   estremi d'arco
ORIGINALI    2391 (29.8 %)       496.0          861330
NATI DOPO    5627 (70.2 %)         2.0           11942
-> i nati dopo sono il 70.2 % dei NODI ma portano l'1.37 % degli ESTREMI D'ARCO
```

**E il `2.0` non è un caso: è ESATTAMENTE ciò che il codice prescrive** — *il figlio nasce con due
archi, verso i due genitori* (par.9) — **verificato dai dati.**

> **⚠ A9: «un presidio che non impedisce non è un presidio».** **Oggi quella restrizione è INERTE**,
> e lo dichiaro invece di venderla come protezione. **Resta scritta perché protegge da uno scenario
> DIVERSO** — neonati che acquisiscano grado — **ma non è lei a far funzionare il criterio.**
> **Quello che lo fa funzionare è che la mediana è sugli ARCHI e non sui NODI**, ed è **quella** la
> differenza col criterio scaduto.

---

## 6. IL DIFETTO **P6** CHE IL MANDATO CHIEDEVA DI REGISTRARE

**`RUN_PARAMS` (`:6274-6296`) scrive `leggi_attive` con `REGIME` e `costanti_effettive` con
`LAM`, `GAMMA`, `SCALA_B`, `CS_M`, `K_C`, `PHI_CRIT` — ma NON `TAU_A`, NON `G_PH`, NON
`CALORE_INIT`.** **I tre numeri che DEFINISCONO il regime sono gli unici che mancano.**

**Sono DEDUCIBILI da `REGIME`, non SCRITTI** — ed è la stessa forma del caso `CS_DINAMICO` già in
par.9: **una deduzione dichiarata vale, una ricostruzione a memoria no.**

**E qui la deduzione è stata fatta con la catena più corta disponibile, non a memoria:** il `.pkl`
**registra il blob**, si estrae il blob con `git cat-file -p`, e da lì si leggono `REGIME` e
`_TAU_A_REGIME`:

```
blob nel .pkl = a1ae5090  ->  REGIME = "deterministico"  ->  _TAU_A_REGIME = 50.0
```

**Entrambe le scene, ramo DETERMINISTICO, `TAU_A = 50`.** *(Il ramo `"stocastico"` darebbe `2.0` ed è
marcato «canonico»: se avesse girato quello, `passi(ramp=1)` sarebbe `200/r` invece di `5000/r`.)*

---

## 7. A8 — I CONTATORI GIÀ CABLATI, letti

```
                              TRE        DUE
_ritmo_chiamate               2400       2400     <- = passi: nessuna chiamata persa
_ritmo_med_assente               3          3
_ritmo_med_non_promosso          2          2
_ritmo_med_sul_pavimento         2          2     <- il presidio di Z42, quasi mai attivo QUI
_ritmo_f_tutto_nullo             1          1
_cs_chiamate                  7198       7198
_cs_fallback                     2          2     <- 0.03 %: la cura della cache tiene
_inerzia_al_pavimento       608018     468367     di _inerzia_tot 11253029 / 8556050  (5.4 % / 5.5 %)
nati                          5627       3984
```

**⚠ `_ritmo_med_sul_pavimento = 2` su 2400 passi**, contro i **1202** del batch a 1200 passi di `Z46`.
**Stessa asimmetria fra le due scene che il §3 mostra su `r`, e con lo stesso segno.**

---

## 8. I LIMITI, tutti insieme

**Un seme per scena · `--tau-luce` col SIGILLO FALLITO su entrambe · `--chi-basc` attivo · sei
istanti · COORTE ANAGRAFICA e non per massa (`Z53`) · `base` ASSOLUTO non ricostruito (dichiarato, e
non serve per il rapporto) · «diverso o solo più forte» risposto SOLO nella parte strutturale ·
il confronto col `93 %` di `Z46` è FRA SCENE DIVERSE (A3c) · NESSUNA IDENTIFICAZIONE DI FISICA.**


---

## 9. APPENDICE — **il testo di `Z9` PRIMA di questa riscrittura, VERBATIM**

**par.5-quater: il registro e' uno STATO, non una cronaca — quindi la voce si RISCRIVE. Ma il testo
vecchio non si butta: diceva com'era e a quale blob, ed e' un'informazione.** *(E' la stessa
convenzione dei marchi storici dello Strato 1 in CLAUDE.md par.9.)*

```
| **Z9** | **IL KERNEL NON HA MAI FINITO DI ACCENDERSI: `ramp` matura in ~5526 passi, i run sono 300-500** (2026-09-17) | `_pesi()` costruisce `base = exp(-d/lam) * ramp[i] * ramp[j]` con `ramp = min(1, eta/TAU_A)`. `eta` e' il **tempo proprio** e cresce di **~0.009 per passo**, `TAU_A = 50` -> **per `ramp = 1` servono ~5526 passi**. Misurato: `ramp` mediano **0.0002** al passo 1, **0.0106** al 60, **0.0217** al 120; a 500 passi vale **~0.09**. E poiche' `base ∝ ramp[i]·ramp[j]`, **il peso d'arco tipico e' ~1 % di quello maturo**. **NON E' UN DIFETTO — `ramp` e' una LEGGE** (la maturazione dell'arco col tempo proprio), non una regolarizzazione. **Ma e' una condizione di REGIME mai dichiarata.** *(E' anche la vera ragione per cui `psi = 0` alla costruzione della scena: non manca l'inizializzazione, `calcola_psi()` E' gia' chiamato via `_registra_concorrenza`. Controprova: forzando `eta = TAU_A`, `max\|psi\| = 8.02`.)* | **LE CONSEGUENZE NON SONO STATE MISURATE**, e dire *«quindi le misure sono sbagliate»* sarebbe l'errore di ampiezza-contro-correlazione gia' catalogato in §9. **Cio' che e' stabilito e' il regime, non il suo effetto.** Le vie (accorciare `TAU_A` per il ramp, disaccoppiare `ramp` dall'eta', o accettare il transitorio continuando a contarlo) sono **decisioni di regime**, e due su tre toccano una legge. -> `doc/REFERTO_psi_zero_ramp.md` | **✅ RIMISURATA sul blob `a8f1b2f4` il 2026-09-17** (`doc/REFERTO_rimisura_Z9.md`): **SOSTANZIALMENTE INTATTA.** Scena ORIGINALE (l'unica confrontabile): `ramp` mediano **0.0002 / 0.0102 / 0.0204** ai passi 1/60/120 contro **0.0002 / 0.0106 / 0.0217**; `eta` **0.00849/passo** contro ~0.009; **`ramp = 1` a ~5887** contro ~5526. Scena del BATCH (il numero valido oggi): **~5960**. **⚠ Lo scarto e' +6.5 % / +7.9 %, nella direzione «piu' lenta» — ma e' UN SOLO SEME, e P3 vieta di chiamarlo un effetto: la dispersione di `ramp` fra semi NON e' mai stata misurata.** **Il fatto non cambia: il kernel matura in ~5900 passi, i run sono 300-500, a 500 passi `ramp` sta sotto il 10 %.** **⚠ LA TESTIMONIANZA DI LUCA, registrata CON LA SUA QUALIFICA (2026-09-17):** *«quel parametro era stato settato cosi' in sessioni precedenti, **prima di creare il repository**, per non far esplodere tutto»*. **E' una TESTIMONIANZA RIFERITA, non un riscontro: precedente al branch, NON verificabile da git.** **Cosa git dice, verificato dal disco:** il primo commit che **aggiunge** `soliton_simulator.py` e' **`670310f`** (2026-08-28 — **non `ca02af0`**, che e' del 13 settembre ed e' «PEZZO 2 peso sin chi»); **`670310f^` NON ha il file**; **`TAU_A = 50` e' gia' li'** (riga 130), accanto al `2.0` marcato «canonico»; e **`git log -S "_TAU_A_REGIME = 50.0"` trova UN SOLO commit, quello.** **Nessun commit ha mai cambiato quel valore: la decisione e' PRECEDENTE AL REPOSITORY.** **E' un'ASSENZA DI PROVA, non una prova di assenza** — la testimonianza resta tale finche' un esperimento non la conferma o la smentisce. **ESPERIMENTO ESEGUITO il 2026-09-17** (`--tau-a 2.0`, flag OFF di default, S3 byte-identico committato PRIMA del run): **NON DIVERGE** — S1 5/5 PASS, zero NaN, `\|nb\|=1`, `_taup_cfl_max` 0.563 contro 0.564. **La testimonianza non e' confermata nella forma letterale. MA i segni di stress sono grossi:** `psi` max **x91** (0.064 -> 5.83), `d0` **x17.4**, `phivel` **x22.7**, **nodi finali -32 %** (2577 -> 1754). **«Regge» significa solo «l'aritmetica non produce NaN».** **E `Z9` sarebbe risolta:** `ramp` mediano da **0.0148 a 0.470**, maturita' a **~255 passi** invece di ~6000-8000 — **dentro la durata dei run**. **TERZA lettura: regge con stress. NON promosso, default invariato**, e `TAU_A=2.0` con `G_PH=3e-3` **non e' ne' il canonico ne' il deterministico: e' una TERZA combinazione mai validata**. **E l'esperimento ha mosso ENTRAMBE le leggi di `Z10`:** parte dello stress puo' venire dalla **memoria spinoriale**, non dalla maturazione — **distinguerle richiede la separazione che `Z10` chiede.** -> `doc/REFERTO_esperimento_tau_a.md`
```

**Cosa di quel testo RESTA VERO:** la formula (`base = exp(-d/lam)*ramp[i]*ramp[j]`), il fatto che
`eta` sia il tempo proprio, `TAU_A = 50`, e la conclusione qualitativa che il kernel non ha finito di
accendersi. **I tre `ramp` mediani citati (`0.0002`, `0.0106`, `0.0217`) sono misure reali di quella
scena, e non sono stati toccati.**

**Cosa NON regge:** **il `~0.009 per passo` come COSTANTE** — e' il tasso di un nodo con `r ~ 0.9` —
**e i `~5526 passi` che ne discendono**, che sono **un** numero dove la legge ne da' **uno per nodo**.
**E il criterio implicito «il `ramp` mediano cresce», per la ragione che Luca ha nominato.**
