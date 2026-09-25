# REGISTRO DELLA FISICA — **un documento unico, su tutto il modello, passato e futuro**

> **Mandato di Luca, 2026-09-22.** Il registro dei difetti dice *«questo era rotto»*; **questo
> documento dice «questa è la legge»**, e le due cose non si sostituiscono.
>
> **⚠ IL VINCOLO CHE GOVERNA IL `CHK3`:** **le cure non partono finché la scheda della componente
> da curare non esiste.** Una cura deve **nascere dalla scheda** — dalla formula, dalle dimensioni,
> da cosa legge e cosa scrive, dai limiti classificati con `A11`. **Se la scheda non c'è, si cura
> di nuovo alla cieca**, ed è il modo in cui sono nati `D01`–`D33`.

## COSA CONTIENE UNA SCHEDA, e perché ciascuna voce

| voce | perché c'è |
|---|---|
| **LA FORMA** | la formula **copiata dal codice che gira**, non dal commento *(par.0)* |
| **DA DOVE VIENE** | derivazione o origine. **Se non si ricostruisce, si scrive `NON RICOSTRUITO`** |
| **LE DIMENSIONI** | `A3c`: due grandezze si confrontano solo se sono **confrontabili** |
| **COSA LEGGE / COSA SCRIVE** | i siti dell'inventario *(`REG-A`)*, col nome di traccia |
| **I LIMITI, classificati con `A11`** | ogni `clip`, pavimento o tetto, **col corollario che rispetta o viola** |
| **LO STATO** | `SANA` · `DA VERIFICARE` · **`DIFETTOSA`** *(col numero del difetto)* |
| **LE DOMANDE APERTE** | **domande, non scelte.** Una scheda non decide: prepara la decisione |
| **L'EPOCA DI OGNI NUMERO** | `par.9-bis`: un numero dell'epoca 1 non è una premessa per l'epoca 3 |

**REG-R, la regola mantenuta** *(da cablare quando le schede coprono le leggi attive)*: **nessuna
legge fisica entra, cambia o esce dal simulatore senza passare da questo documento**, con un hook
che rifiuta un commit a `soliton_simulator.py` che non tocchi il registro, salvo
`[SENZA-FISICA: <motivo>]`.
**✅ CABLATA il 2026-09-22 — e nella forma che la rende un presidio invece di una formalità.**
`csv/_hook_fisica.py`, dentro il `commit-msg` già esistente *(un hook solo: due che se lo contendono è il modo in cui un presidio sparisce in silenzio)*. **Non chiede di «toccare il registro»** — lo soddisferebbe una riga qualsiasi in fondo al file. **Chiede che la modifica cada DENTRO la sezione della legge toccata**, e se quella legge **non ha una scheda**, dice *«prima si crea la scheda»*.

> ### ⚠ **UN INDEBOLIMENTO DI `REG-R`, dichiarato il 2026-09-24**
>
> **`_applica_flag` e `_cli` NON sono leggi**: sono il cablaggio dei flag. Ma è **lì** che un
> flag viene collegato alla sua legge, quindi `REG-R` li vede cambiare e chiede una scheda.
> **Li ho aggiunti alle `funzioni=` delle due schede che governano i flag cablati in quel
> commit** — `tempo-proprio` per `RITMO_WRAP_2PI`, `torsione-spinore` per `TW_SPINORE` —
> perché è vero che la cura *sta* lì.
>
> **L'INDEBOLIMENTO: da ora un commit che tocca `_applica_flag` per un flag QUALUNQUE
> soddisfa `REG-R` toccando una di queste due schede.** È meno stretto di prima, e va detto
> invece di scoprirlo dopo. **Non l'ho risolto**: la via pulita sarebbe che `REG-R` mappasse
> il flag, non la funzione, e quella è una modifica al presidio che **non decido da solo**.

**COME SA QUALE SCHEDA:** ogni scheda porta un marcatore leggibile da codice — `<!-- SCHEDA nome=… funzioni=… flag=… -->` — e la sezione va da un marcatore al successivo.
**COME SA COSA È CAMBIATO:** dalla diff in cache di `soliton_simulator.py`, le righe toccate risalgono alla **funzione** che le contiene *(per NOME, via AST della versione in cache — par.0)* o al **flag** di modulo assegnato su quella riga.

**⚠ IL LIMITE, dichiarato invece che nascosto:** **non distingue una modifica di LEGGE da una di COMMENTO.** Distinguerle richiederebbe un confronto di AST fra le due versioni, e **un commento che descrive una legge è parte della legge** *(i commenti stale sono un difetto documentato di questo repo)*. **Quindi è più severo del necessario**, e le modifiche davvero non fisiche passano per `[SENZA-FISICA: <motivo>]`.

## COSA C'È DA COPRIRE — **dalla `FASE A`, misurato, non stimato**

**`164` scritture di stato su `27` grandezze, di cui `65` CONCATENAZIONI**, più `313` scritture su
attributi **non dichiarati fisici** *(`csv/_seal_fork/_inventario_scrittori.py`, blob `2c70e4ad`,
voce `Z…` della `FASE A`, commit `9a82bfb`)*.
**Ogni scrittore dei 164 deve finire in una scheda.**

**L'ORDINE, fissato da Luca il 2026-09-22 e rivisto dopo `Z109`:**
① **il freno di `SCALA_MIN`** · ② **la memoria del moto** · ③ **la gravità bifase** ·
④ **la coesione** · poi mitosi, Schwinger, rilassamento di `peq`; poi le altre attive, poi le
**dormienti**.

---

<!-- SCHEDA nome=freno-scala-min funzioni=_smorza,_smp_apri,_smp_chiudi,_smp_snap,_sd0,_pav_d0,_floor_d0,_nasce flag=SCALA_MIN,SCALA_MIN_PASSO -->
# ① IL FRENO DI `SCALA_MIN` — **`SCALA_MIN_PASSO` / `_smorza` / `_smp_chiudi`**

> **STATO: `DIFETTOSA`.** Difetto **`D31`**. **Viola `A11` corollario 4 e corollario 7(b).**
> **È IL MOTORE DELLA CRESCITA DI `d0`**, misurato due volte con un bilancio che chiude.
>
> ### ➜ **`_nasce` ORA MISURA LA LUNGHEZZA CHE FABBRICA** *(2026-09-25, `U2`)*
>
> Tre contatori `A8`, **byte-inerti**: `_sm_visti`, `_sm_troncati`, **`_sm_lunghezza`**.
> **`_g_sm_nascite` contava le INVOCAZIONI, non i troncamenti** — quindi *«quanto `_nasce`
> ha fabbricato»* **non era leggibile**. Ora `_sm_lunghezza = sum(LAM - d)` sui troncati è
> **il contributo DIRETTO di questa funzione al gonfiamento di `d0`, nelle stesse unita'
> del bilancio** — cioè nelle stesse unita' in cui `D31` accusa il freno.
> **Serve a `U2`**, e la legge sta in scheda ⑫.
>
> ### ➜ **`_nasce` HA PERSO IL SUO GATE** *(2026-09-24, `D38`)*
>
> `_nasce` — *il troncone sotto `LAM` si porta A `LAM`* — era `if not (SCALA_MIN or
> SCALA_MIN_PASSO): return v`. **Il gate è TOLTO: il presidio agisce SEMPRE.**
> **Coi default del SORGENTE la legge `d >= LAM` era VIOLATA AL PASSO ZERO su `223 380`
> archi**, ed è **lo stesso schema che `E4-LAM` ha tolto al CONTROLLO e che era rimasto
> all'ESECUZIONE**: *il controllo era legge, chi la faceva rispettare era un'opzione.*
>
> **⚠ E NON È UNA CURA, È UN PRESIDIO** *(decisione di Luca)*: con `SEMINA_LAM` acceso **non
> deve scattare mai**, e **`_g_sm_nascite` è la sua misura**. **La legge sta in scheda ⑫.**
>
> ### ✅ **LA FORMA DELLA CURA DI `D31` È DECISA** *(Luca, 2026-09-24)*
>
> ```
> (d − LAM)  ←  (d − LAM) · (1 + tanh(dx / d))
> ```
>
> **LA MISURA CHE L'HA DECISA:** `V8`/`V9` dal giro corto di `CURA 2` — **`max |dx|/d = 0.0531`
> su `125 731 076` campioni, ZERO oltre `0.5`** su entrambi i versi. **Il solo difetto
> dichiarato di `tanh`, la saturazione a `2`, non si presenta mai:** conta a `x ~ 1`, e il
> massimo misurato è **`19` volte** più piccolo.
>
> **⚠ E IL CONFRONTO NON È SIMMETRICO:** la deriva di `piana` vale `exp(N·E[x²]/2)`, e **`E[x²]`
> NON è stato registrato** — a `6000` passi l'intervallo va da **`+1.7 %` a `+471 %`**.
> **Si sceglie la forma il cui prezzo si CONOSCE.**
>
> **CRITERIO CHE LA RIAPRE, scritto ORA** *(par.10: la condizione si scrive al momento della
> decisione, non dopo)*: **una quota NON NULLA di `|dx|/d > 0.5`.**
>
> **⚠ NESSUN CODICE: la forma è decisa, la scrittura no.** Sta in **scheda ⑩ par.4-quinquies**,
> e **l'ordine — se il freno-legge venga prima o dopo `CURA 3` — è un CHECKPOINT di Luca.**

## LA FORMA — copiata dal codice, non dal commento

**Il nucleo, `_smorza` (`:3526`):**
```
eff(prima, dx) =  dx                                se  dx >= 0     <- IDENTITÀ ESATTA
                  dx * max(0, 1 - LAM/prima)        se  dx <  0     <- solo la DISCESA è frenata
```
**L'applicazione, `_smp_chiudi` (`:3698`), UNA VOLTA per passo:**
```
v  = d0 a INIZIO passo                   (fotografia di `_smp_apri`, :3666)
dx = d0 a FINE passo - v                 (la variazione TOTALE del passo)
d0 <- v + eff(v, dx)
```

**L'INVARIANTE, dichiarato nel docstring e verificato algebricamente qui:**
```
nuovo - LAM = (prima - LAM) * (1 + dx/prima)
```
*(sviluppo: `nuovo = prima + dx - dx·LAM/prima`, e `(prima-LAM)(1+dx/prima) = prima + dx - LAM -
LAM·dx/prima`. Coincidono.)*

> **COSA DICE DAVVERO QUESTO INVARIANTE, ed è il contenuto fisico della legge:** per `prima > LAM`
> e `dx > -prima`, il fattore `(1 + dx/prima)` è **positivo**, quindi **`nuovo > LAM` sempre**.
> **`LAM` è una BARRIERA ASSORBENTE DALL'ALTO: non si tocca e non si attraversa, la si avvicina
> asintoticamente.**

## DA DOVE VIENE

**`LAM` è la scala del sistema** — la stessa che fissa `R_CONN = 3·LAM`, il filtro di portata
`1 − tanh(d/LAM)` e l'ancora elastica. **Non è un numero scelto per questa legge:** esisteva prima.
**Il vincolo dichiarato è: nessuna lunghezza sotto `LAM`** *(`:979`)*.
**La FORMA `1 − LAM/x` invece NON è derivata: è stata scelta fra tre**, e le altre due sono cadute
*(`A11` cor.7, `doc/TASK_HISTORY/2026-09-21_ramo_D_tre_modifiche.md`)*. **`NON RICOSTRUITO`: perché
proprio questa forma e non un'altra che rispetti l'obbligo (b).**

## LE DIMENSIONI

| simbolo | dimensione |
|---|---|
| `prima`, `dx`, `eff`, `LAM` | **lunghezza** `[L]` |
| `LAM/prima` | **adimensionale** |
| `eff = dx · (1 − LAM/prima)` | `[L]` ✔ |

**Coerente.** *(Il difetto non è dimensionale: è di simmetria.)*

## COSA LEGGE / COSA SCRIVE

- **legge:** `d0` a inizio passo *(`_smp_apri`)*, `d0` corrente, `LAM`.
- **scrive:** **tutto `d0`**, a fine passo, dentro `_smp_chiudi` *(`:3719`)*.
- **⚠ E NON HA NESSUN SITO DI TRACCIA** — è il difetto **`D04`**: la scrittura è **invisibile** a
  `_traccia_d0`, ed è il termine che in `Z107` lasciava il bilancio aperto. Nel bilancio di `G4` è
  aggirato **avvolgendo `_smorza` dall'esterno**; **nel simulatore il sito manca ancora.**
- **il chiamante `d0_passo`** è quello del bilancio; esiste anche `d_passo`, **dentro un sito già
  tracciato**, che non va sommato o si conta due volte.

## I LIMITI, CLASSIFICATI CON `A11`

| corollario | esito |
|---|---|
| **1 — origine fisica** | ✅ `LAM` è la scala del sistema, non una difesa dalla divisione |
| **2 — non dipende da ciò che limita** | ✅ `LAM` è costante; **non** insegue `d0` *(a differenza del pavimento comovente `f·median(d0)` di `Z91`)* |
| **3 — non ribalta segni** | ✅ `fatt ∈ [0,1]`, quindi `eff` ha il segno di `dx`; e `_g_sm_max_giu ≤ 0` lo misura a ogni scrittura |
| **4 — SIMMETRICO** | ❌ **VIOLATO, e DIMOSTRATO sulla formula** *(`Z113`, `4/4`)*: su rumore a media **zero esatta**, lontano dal confine, la deriva è **`+1.582064e-03`** contro l'attesa derivata **`+1.582007e-03`** — **scarto `0.0 %`**. **E con `LAM = 0` la deriva è `0.000000e+00` ESATTO**, con un freno **simmetrico** `5.9e-09`: **viene dall'ASIMMETRIA** |
| **5 — si ripara all'origine** | ⚠ **DA DECIDERE:** il freno sta nel punto d'uso. **Dove nasce la discesa che va frenata?** |
| **6 — se satura è un allarme** | ❌ **VIOLATO, e ora è MISURATO** *(`Z113`)*: al passo 600 il **`13.74 %`** degli archi sta in `[1.0, 1.1)·LAM`, dove il freno annulla il **`99.96 %`** di ogni discesa, e porta il **`35.80 %`** del freno. **La popolazione si è POLARIZZATA:** `13.74 %` incollato al muro, **`60.32 %` oltre `3·LAM`**, le bande intermedie svuotate |
| **7(a) — lontano è identità** | ✅ per `x ≫ LAM`, `1 − LAM/x → 1` |
| **7(b) — nessuna deriva su spinte simmetriche** | ❌ **VIOLATO, ed è il punto.** |
| **7(c) — larghezza dalla fisica** | ✅ la larghezza **è** `LAM` |

## LO STATO: `DIFETTOSA` — **e quanto pesa, misurato**

| | `Z108` *(braccio acceso, 600 passi)* | `Z109` *(senza memoria del moto)* |
|---|--:|--:|
| **FRENO** | **`+117.41 %`** del `Δ(Σd0)` | **`+218.33 %`** |
| scritture fisiche | `−17.43 %` | `−118.38 %` |
| nascite − morti | `0.01 %` | `0.05 %` |
| residuo del bilancio | `1.138e-13` | `1.170e-13` |

> **Gli scrittori fisici tirano `d0` GIÙ. È il VINCOLO a gonfiarlo.**
> **E la sua quota CRESCE quando si spegne un'altra legge**, perché il `Δ` si rimpicciolisce e il
> freno no. **Epoca: archivi delle cure**, blob `ab685eac`, UN seme, UNA scena, 600 passi.

## LE DOMANDE APERTE — **tre candidati per il limite fisico. DOMANDE, non scelte.**

> **Poste da Luca, 2026-09-22.** **Nessuna è stata scelta, e questa scheda non sceglie.**

### (A) **La barriera da POTENZIALE, con un integratore che non la scavalca**

**L'idea:** invece di frenare la variazione *a posteriori*, mettere `LAM` in un **potenziale** che
diverge al confine, e integrarlo con uno schema che **non può** scavalcarlo — come `PEQ_ESATTO` ha
fatto per `peq` *(`A11` cor.5: la positività **dimostrata** da una combinazione convessa invece che
**imposta** da un pavimento)*.

**LE DOMANDE:**
1. **Qual è il potenziale, e da dove viene?** Se va scelto, è una manopola *(par.3)*.
2. **Rispetta l'obbligo (b)?** Un potenziale repulsivo è **simmetrico per costruzione** — ma
   aggiunge **energia**: da dove la prende?
3. **`A6`:** il potenziale dipenderebbe da `d0` e agirebbe su `d0` nello **stesso istante**. Serve
   uno sfasamento, come la cura dell'anello di `ritmo()`?

### (B) **La repulsione a `4π` che ESISTE GIÀ** *(→ `D33`, misurato oggi)*

**L'idea:** il sistema **ha già** una repulsione per la materia super-compressa — il ramo negativo
di `mitosi()` *(`:5153`)*. **Non serve inventarla: serve farla arrivare dove serve.**

**MA `D33` DICE CHE OGGI NON CI ARRIVA**, e i numeri sono di **oggi**, archivi delle cure:
- il **segno** si inverte oltre `~3.5π`, **ma `discesa = clip(1 − |tw|/4π, 0, 1)` è ZERO ESATTO da
  `4π`**: la finestra utile è larga **mezzo `π`**;
- **dal `75.3 %` al `95.8 %`** degli archi oltre l'inversione riceve **repulsione esattamente zero**;
- il saldo di `S05_spinta_locale` su 600 passi vale **`+3.57`** contro **`−2.6e+05`** di `S09`:
  **un fattore `~1e-5`**.

**⚠ E IL NUMERO CHE CIRCOLAVA ERA DI UN'ALTRA EPOCA:** il commento `:64-66` dice che la torsione
**satura a `~2.5π`** — **`PRE-FORK`**. **Oggi `max|tw|` sta fra `9.5π` e `13.0π`.**

**LE DOMANDE:**
1. **`discesa` deve annullarsi a `4π`?** Nasce come *«spegnimento della MITOSI al tetto»* — ma
   moltiplica **anche** il ramo repulsivo. **Sono due leggi in un prodotto solo.**
2. **Se si separassero, la repulsione oltre `4π` sarebbe la barriera cercata?** E con quale
   ampiezza, visto che il `0.02` di `:5230` è **un numero scelto** *(`A1` violato, già dichiarato)*?
3. **La repulsione agisce su `d0`, il freno agisce su `d0`. Sono lo stesso vincolo scritto due
   volte?** Se sì, **una delle due va tolta**, non affiancata.

### (C) **Un'esclusione alla Pauli sugli spinori, DA DERIVARE**

**L'idea:** la scala minima non sarebbe un vincolo **sulla lunghezza**, ma la **conseguenza** di
un'antisimmetria degli spinori: due nodi nello stesso stato non possono coincidere. **Sarebbe
l'unico dei tre candidati a rendere `LAM` un RISULTATO invece che un'ipotesi.**

**LE DOMANDE:**
1. **`A6` (teorema):** il trasporto oggi è **scalare** *(`:2207-2208`, abeliano per struttura)*.
   **Un'esclusione richiede l'antisimmetria dello stato a due corpi: il sistema ce l'ha?**
2. **Da dove verrebbe la scala?** Un'esclusione dà una **densità** massima, non una lunghezza:
   il passaggio `densità → LAM` **va derivato, non postulato** *(par.3)*.
3. **È verificabile oggi?** `spin_ovl = 0.5` = **direzioni di Bloch CASUALI** *(par.9)*: su un
   substrato senza struttura di spin, **un'esclusione non ha su cosa agire.** **La domanda
   precedente a tutte è se il substrato esista.**

## LAVORO RESIDUO DI QUESTA SCHEDA

- ✅ **FATTO** *(`Z113`)*: le bande di `d0/LAM` e il test del cricchetto. **Restano i CONTATORI del simulatore** *(`_g_sm_discese`, `_g_sm_patol`, `_g_sm_viol_*`)*, **mai letti in un referto**: la misura di `Z113` è fatta sugli snapshot e su una formula, **non su quei contatori**;
- ⚠ **`_smorza` HA DUE CRICCHETTI, non uno** *(trovato sbagliando, reperto `7203ae3`)*: oltre a `LAM`, la guardia **`pos = prima > 0`** azzera le discese e lascia passare le salite. **Non è raggiungibile oggi** — `d0 >= LAM` per costruzione — **ma è una proprietà della formula, e una cura che tocchi il pavimento la incontrerà**;
- **`A11` cor.5:** dove nasce la discesa che il freno trattiene? **Non è stato cercato.**

---


### ❌❌ `_nasce` — **I CONTATORI MESCOLAVANO `d` CON `d0`. CORRETTO** *(rilievo di Luca, 2026-09-25)*

**`_nasce` è una legge di questa scheda**, e i suoi contatori appartengono qui.

`_nasce(v, dove="?", md=1, md0=1)`. **`md`/`md0` dicono quanti ARCHI VERI di `d` e di `d0`
diventa ogni voce di `v` nel sito che chiama** — e **sono diversi in ognuno dei quattro siti**:

| sito | `md` | `md0` | dal codice |
|---|--:|--:|---|
| `semina` — `_allaccia`, `dd` | `1` | `1` | `d = concat([d, dd])` **e** `d0 = concat([d0, dd])`: **UNA chiamata, DUE grandezze** |
| `mitosi` — `dh` | **`2`** | `0` | `d = concat([d[keep], dh, dh])`: **due archi per voce** |
| `mitosi` — `d0new` | `0` | `1` | `d0new` è **già** `concat([d0h, d0h])` |
| `schwinger` — `dd` | **`2`** | **`2`** | `[d, dd, dd]` **e** `[d0, dd, dd]` |

**Contatori: `_sm_{lun,tr,vis}{d,d0}_{sito}`.** Byte-inerti *(si somma, non si cambia)*.

> ### **Solo `_sm_lund0_*` è nelle unità del bilancio di `d0`, quindi solo quello entra in `P-GONFIA`.**

**COSA C'ERA PRIMA, e perché era sbagliato:** un contatore solo, `_sm_lunghezza`, che
① **sommava `d` e `d0` nello stesso numero** — quindi **non era nelle unità di nessuna delle
due**, che era l'unica ragione per cui l'avevo scritto; ② **sottocontava di `2`** il sito `dh`;
③ contava le **voci**, non gli **archi**, anche nel denominatore.

**SIGILLO: `csv/_seal_fork/_sigillo_u2_contatori.py`** — **una MITOSI VERA** con un solo arco a
`1.2 LAM` *(`dh = 0.6 LAM`, entrambi i figli troncati)*; atteso per costruzione
`trd = trd0 = 2`, `lund = lund0 = 0.8 LAM`. **`U2-6` è il caso che DEVE fallire** *(`P1-sexies`)*:
la formula vecchia, sullo stesso evento, dava `0.4 LAM` su `d` e una somma mescolata di `1.2 LAM`.

**⚠ `_g_sm_nascite` RESTA, e misura un'altra cosa:** le **INVOCAZIONI**. Una chiamata che non
tronca nulla lo fa salire ugualmente — è il presidio di `D38`, non una misura del troncamento.

<!-- SCHEDA nome=memoria-del-moto funzioni=memoria_hebbiana_moto flag=MEM_HEBB,MEM_MOTO,MEM_MOTO_TUTTO,SCALA_P_MEDIANA,ZETA_VIR -->
# ② LA MEMORIA DEL MOTO — **`memoria_hebbiana_moto` / `S08_proj` / `mem_mot`**

> **STATO: `DIFETTOSA`.** Difetti **`D03`** *(direzioni dal disegno, `Imed` globale, tetto
> `0.01·median(d0)`)* e **`D02`** *(il pozzo usa `pos`)*.
> **Cura derivata e NON scritta: `MEM_ARCO`.** **Spegnerla toglie il `62 %` della crescita di `d0`
> e FA SPARIRE LA COMPRESSIONE** *(`Z109`)*.

## LA FORMA — copiata dal codice (`:5644-5676`), non dal commento

```
twn[nodo]   = SUM |tw| sugli archi incidenti / deg            [rad]
dtw[arco]   = twn[jj] - twn[ii]                               [rad]
dirarc      = (pos[jj] - pos[ii]) / |pos[jj] - pos[ii]|       <- DAL DISEGNO (D02/D03)
grad_tw[n]  = SUM_archi dtw * dirarc / deg                    [rad]   <- NON diviso per una lunghezza
plast       = tanh(|grad_tw|)                                 in [0,1)
mem_mot     = (1 - plast)*mem_mot + plast*grad_tw             <- LA MEMORIA: rilassamento
memedge     = 0.5*(mem_mot[ii]*I[ii]/Imed + mem_mot[jj]*I[jj]/Imed)    <- Imed GLOBALE
proj        = SUM(memedge * dirarc)
proj        = clip(proj, -0.01*median(d0), +0.01*median(d0))  <- TETTO GLOBALE
d0[mask]   += _sd0(proj, mask)                                <- il sito `S08_proj`
```
**E IL QUARTO PUNTO, che non scrive su `d0` e che `MEM_MOTO` non copriva** (`:6033`):
```
proiezione_trasversale = SUM(mem_mot[ii] * dir_laterale)
shift_fase_dinamico    = accoppiamento_dinamico * proiezione_trasversale * (d_archi/d0_archi)
phi[ii] = (phi[ii] + clip(shift_fase_dinamico, -pi/4, +pi/4)) % 4pi
```

## DA DOVE VIENE

**Legge del momento:** `mem(t+1) = mem(t) + correzione_dal_campo`. La **plasticità** non è scelta:
è `|grad_tw|` stesso, saturato da `tanh`. **Questo è derivato.**
**`NON RICOSTRUITO`:** perché la correzione sia `grad_tw` *(differenza di torsione per nodo)* e
non un'altra forma; e perché il tetto sia `0.01`.

## LE DIMENSIONI — **e qui c'è un problema**

| simbolo | dimensione |
|---|---|
| `tw`, `twn`, `dtw`, `grad_tw`, `mem_mot` | **angolo** — adimensionale |
| `dirarc`, `I/Imed`, `plast` | adimensionale |
| **`proj`** | **adimensionale** |
| **`d0`** | **lunghezza `[L]`** |

> **⚠ `proj` È UN NUMERO PURO, E VIENE SOMMATO A UNA LUNGHEZZA.**
> **L'unica cosa che gli dà unità di lunghezza è IL CLIP `0.01·median(d0)`.**
> **Quindi il clip non è un limite: è la SCALA della legge** — ed è esattamente ciò che il
> `78 %`–`89 %` di saturazione misurato dice *(`Z112`)*.
>
> **E `grad_tw` è chiamato GRADIENTE ma non è diviso per una lunghezza:** un gradiente vero
> sarebbe `dtw/L`. **`A3c`.**

## COSA LEGGE / COSA SCRIVE

- **legge:** `tw`, `pos` *(il DISEGNO — `D02`)*, `psi` → `I` e `Imed` *(media **globale** —
  `A2`, `D03`)*, `_deg`, `d0`.
- **scrive:** `mem_mot` *(stato per nodo)* · `d0` al sito **`S08_proj`** · **`phi`** al
  punto `:6033`.
- **flag:** **`MEM_MOTO`** recinta la **sola** scrittura su `d0`; **`MEM_MOTO_TUTTO`** recinta
  **tutti e quattro** i punti *(sigillo `10/10`, blob `21e3a3dc`)*.

## I LIMITI, CLASSIFICATI CON `A11`

| limite | corollario | esito |
|---|---|---|
| `clip(proj, ±0.01·median(d0))` | **1** | ❌ il `0.01` è **scelto** *(`A1`)* |
| | **2** | ❌ **cresce con `d0`**: più `d0` scappa, più il tetto glielo consente |
| | **6** | ❌ **saturo nel `78 %`–`89 %`**: *«non è un limite, è la legge»* |
| `max(median(I), 1e-9)` | **1** | ⚠ difesa dalla divisione, non vincolo fisico |
| `max(|v|, 1e-9)` su `L` | **1** | ⚠ idem |
| `clip(shift_fase, ±π/4)` | **1** | ⚠ dichiarato *«limite geometrico causale»*: **da verificare se satura** — **non misurato** |

## LO STATO: `DIFETTOSA` — **e quanto pesa, misurato**

| | acceso | spento *(`MEM_MOTO=False`)* |
|---|--:|--:|
| `Δ(Σd0)` su 600 passi | `+1.731e+06` | **`+6.504e+05`** — **−62 %** |
| `S08_proj`, saldo | `+7.151e+05` | assente |
| `med d/d0` finale | `0.7489` **`NON REGGE`** | **`0.8546` `REGGE`** |
| criteri | `6/8` | **`7/8`** |

## L'IPOTESI DELLA COMPRESSIONE — **misurata, e si divide in due**

> *«`S08_proj` scrive `d0` verso l'ALTO senza che `d` segua, e questo abbassa `d/d0`»*
> *(Luca, 2026-09-22 · `csv/_test_fork/_compressione_memmoto.py` blob `f5e55310`, `Z112`)*

**✅ LA PARTE «`d` NON SEGUE» REGGE, e nettamente.** Fra i due bracci allo **stesso** passo,
spegnendo `S08_proj`:

| passo | `Δd0/d0` | `Δd/d` | **rapporto** |
|--:|--:|--:|--:|
| 120 | `−11.42 %` | `−1.37 %` | **`8.35`** |
| 360 | `−27.94 %` | `−3.11 %` | **`8.97`** |
| 600 | `−32.01 %` | `−12.97 %` | **`2.47`** |

**`d0` è da `2.5` a `9` volte più sensibile di `d`.** Il criterio chiedeva `>= 2` ovunque: **c'è.**

**⚠ LA PARTE «VERSO L'ALTO» NON REGGE COME SCRITTA, e va detto.** La frazione di archi con
`proj > 0` è **`57.7 %` · `64.3 %` · `58.6 %` · `51.4 %` · `47.4 %`**: **decresce**, e **al
passo 600 è SOTTO metà** con **somma NEGATIVA** *(`−8.4e+02`)*.
**Ma la correlazione trasversale è forte e sempre dello stesso segno: `−0.19` … `−0.44`**,
contro un nullo di `1.4e-03` — **da `140` a `310` volte il suo valore sotto ipotesi nulla**.
**Gli archi che ricevono più `proj` HANNO `d/d0` più basso, nello stesso istante.**

> **COME SI LEGGONO INSIEME, ed è il limite che avevo dichiarato PRIMA:** `proj` è l'incremento
> **istantaneo**, `d/d0` è una **storia**. **Al passo 600 l'istantaneo è già girato in negativo
> mentre `d0` resta alto: è l'ACCUMULO che comprime, non il segno del momento.**
> **L'ipotesi regge nella sostanza — `S08_proj` è la causa della compressione — ma il
> meccanismo NON è «spinge sempre in su»: è «ha spinto in su, e `d0` non torna».**
> **E questo è esattamente il cricchetto del freno** *(scheda ①, `A11` cor.4)*: `d0` sale e non
> può scendere. **Le due schede si toccano qui.**

## ⚠ `FASE_2PI` TOCCA UN SITO ANCHE QUI

**`:6105`**, l'avvolgimento di `phi` dopo lo spostamento di fase, passa da `% (4π)` a **`% self._dphi()`**. **È l'unico punto di questa scheda che la cura del dominio attraversa**, e la legge della memoria del moto **non cambia**: cambia **il periodo su cui `phi` si richiude** dopo che questa legge l'ha spostata.

## LE DOMANDE APERTE

1. **`proj` è adimensionale e viene sommato a una lunghezza.** **Quale lunghezza fisica lo
   converte?** Oggi lo fa il clip, che è un numero scelto. **`MEM_ARCO` deve rispondere a questa
   prima di essere scritta.**
2. **`grad_tw` è un gradiente senza divisione per la lunghezza dell'arco.** Dividerlo cambia la
   legge o la ripara?
3. **Il `62 %` di `Z109` non è il peso della sola scrittura su `d0`:** `shift_fase_dinamico` legge
   `d_archi/d0_archi`, quindi il punto (4) è **accoppiato** al punto (3) attraverso `d0`
   *(sigillo di `G4-bis`, `T6`)*. **`G4-bis` è il braccio che separa le due cose.**
4. **Se `d0` è `2.5`–`9` volte più sensibile di `d`, che cosa lega `d` a `d0`?** La compressione
   è un difetto **di `d0`** o un'**assenza di accoppiamento** verso `d`?

---

<!-- SCHEDA nome=gravita-bifase funzioni=pozzo_grafo,_nb_grav flag=GRAV_BIFASE,VIRIALE,LS_AZIM,PHI_CRIT,K_FRANGE -->
# ③ LA GRAVITA' BIFASE — **`GRAV_BIFASE` / `S09_spinta_med` / `S10_grav_med`**

> **STATO: `DIFETTOSA`.** Difetto **`D01`**. **Viola `A2`, `A5` e `A11` corollario 6.**
> **NON è il motore della fuga di `d0`** *(`Z107`: spegnendola il rapporto passa da `1.2321` a
> `1.2211`, lo `0.9 %`)*, **ma è il maggior scrittore in ampiezza**: `±2.5e+06`–`3.7e+06`
> per 600 passi.

## LA FORMA — copiata dal codice (`:5766-5850`)

```
grav      = -tanh(s) * ampiezza                       s = |tw|/PHI_CRIT - 1, FIRMATA
                                                      -s = il VERSO (attrae / respinge)
se SPINORE:  grav = grav * (nb_g[ii]·nb_g[jj]) * sign(dpozzo)     <- proiezione spinoriale

c_sistema      = LAM * sqrt(K_C)                      velocità del cono, da LAM e K_C
passo_causale  = c_sistema * DT                       IL TETTO

se VIRIALE:  radiale  = grav * cos2
             tangenz  = |grav| * sin2 * sign(circ_arc)      (o `_azim` se LS_AZIM)
             spinta   = radiale + tangenz
             spinta   = clip(spinta, ±passo_causale)
             d0[mask] += _sd0(spinta * median(d0[mask]), mask)        <- `S09_spinta_med`
altrimenti:  grav     = clip(grav, ±passo_causale)
             d0[mask] += _sd0(grav * median(d0[mask]), mask)          <- `S10_grav_med`
```

## DA DOVE VIENE

**Il verso è DERIVATO:** `s = |tw|/PHI_CRIT - 1` è lo scarto dal **quanto di olonomia**, e il
segno di `-tanh(s)` dice se l'arco è sotto o sopra il giro completo. **Bifase: attrae da una
parte, respinge dall'altra, e la soglia è `PHI_CRIT`, che esisteva già.**
**`NON RICOSTRUITO`:** perché `tanh` e non un'altra saturazione; perché la scomposizione
radiale/tangenziale usi `cos2`/`sin2` di quell'angolo.

## LE DIMENSIONI — **e qui c'è il difetto**

| simbolo | dimensione |
|---|---|
| `s`, `tanh(s)`, `ampiezza`, `cos2`, `sin2`, `proiez` | adimensionale |
| **`grav`, `spinta`** | **adimensionale** |
| `c_sistema = LAM·√K_C` | `[L/T]` |
| **`passo_causale = c_sistema·DT`** | **`[L]`** |
| `spinta * median(d0)` | `[L]` |

> **⚠ `spinta` VIENE CLIPPATA A UNA LUNGHEZZA E POI MOLTIPLICATA PER UN'ALTRA LUNGHEZZA.**
> Dopo il clip `spinta` ha unità `[L]`; moltiplicarla per `median(d0)` dà **`[L²]`**, che viene
> sommato a `d0` — **`[L]`**. **È `D01`, e la scheda lo rende esplicito:** *«clippa al passo
> causale — quindi è già una LUNGHEZZA — e poi moltiplica per `median(d0)`: statistica GLOBALE
> e lunghezza AL QUADRATO»*.

## COSA LEGGE / COSA SCRIVE

- **legge:** `tw`, `pozzo_grafo` → `dpozzo` *(che usa `pos`, il **DISEGNO** — `D02`)*,
  `_nb_grav()`, `median(d0[mask])` *(**globale** — `A2`)*, `LAM`, `K_C`, `DT`.
- **scrive:** `d0` a **`S09_spinta_med`** *(ramo `VIRIALE`)* oppure **`S10_grav_med`**.
  **I due rami sono esclusivi:** in tutti i run del fork gira `S09`, e **`S10` è inerte**
  *(`Z102`)*.
- **flag:** `GRAV_BIFASE` *(sigillo `7/7`, `G3`)*.

## I LIMITI, CLASSIFICATI CON `A11`

| limite | corollario | esito |
|---|---|---|
| `clip(spinta, ±passo_causale)` | **1** | ✅ **causalità**: `c_sistema` viene da `LAM` e `K_C`, non è scelto |
| | **2** | ✅ costante, non insegue `d0` |
| | **6** | ❌ **VIOLATO: `85.05 %` degli archi-passo INCOLLATO AL TETTO**, e il **`99.69 %`** del saldo viene da incrementi **saturi** *(`Z106`)*. **Non è un limite: è la legge**, e nessuno l'ha scelta |
| | **5 (A5)** | ⚠ `c_sistema` è costruito su **costanti di modulo** e **non conosce il cono del LUOGO** — lo stesso difetto che `COES_CAUSALE` ha curato per la coesione |

## LO STATO: `DIFETTOSA` — **e dove spinge, misurato**

- **il saldo netto vive SUL CONFINE vuoto-massa e TIRA GIÙ:** `-1.4150` per arco, il **`107 %`**
  del totale *(`Z105`)*;
- i **20 archi** col `|saldo|` maggiore sono **`20/20` nel VUOTO**, e il confine è **DIFFUSO** su
  **`96 429`** archi all'**`85 %`** del plateau;
- saldo su 600 passi: **`-1.901e+05`** *(braccio acceso)*, **`-2.598e+05`** *(senza memoria del
  moto)* — **il maggior scrittore in ampiezza, e tira GIÙ.**

## LE DOMANDE APERTE

1. **Se il `99.69 %` del saldo viene da incrementi saturi, che legge sta girando davvero?**
   Quella scritta, o **`spinta = passo_causale · sign(...)`**? *(`A11` cor.6.)*
2. **Il tetto è GLOBALE mentre `COES_CAUSALE` ha reso locale quello della coesione.**
   Perché non qui? È la stessa `A5`.
3. **`median(d0[mask])` è una statistica globale dentro una legge che si dichiara locale.**
   `SPINTA_LOCALE` è la cura derivata — **e deve risolvere anche il `[L²]`.**

---

<!-- SCHEDA nome=coesione funzioni= flag=COES_ADIM,COES_CAUSALE,K_C -->
# ④ LA COESIONE — **`COES_ADIM` / `COES_CAUSALE` / `S12_coesione`**

> **STATO: `DA VERIFICARE`.** Il difetto **`D18`** *(istanti misti e tetto globale)* è
> **`CURATO`** da `COES_CAUSALE` *(`C4`, sigillo `5/5`)*, e la forma adimensionale da `COES_ADIM`.
> **È l'unica delle quattro che arriva alla scheda già curata.**

## LA FORMA — copiata dal codice (`:5939-6032`)

```
coesione_relazionale = scala_statale * (forza_campo + richiamo_elastico)
                       * filtro_portata * d0[mask]**2 * (I_arco/I_med)
tasso_dinamico       = tanh(stress_metrico) * d0[mask]

se COES_ADIM:   _delta_coes = _passo_causale * _F_adim          |_F_adim| <= 1 PER COSTRUZIONE
                d0[mask] += _sd0(_delta_coes, mask)
altrimenti:     d0[mask] += _sd0(clip(coesione_relazionale, ±tasso_dinamico), mask)
                                                                 <- il ramo STORICO
se COES_CAUSALE: _passo_causale = cs_arco * DT      <- il cono LOCALE, col `cs` del nodo PIÙ LENTO
altrimenti:      _passo_causale = LAM*sqrt(K_C)*DT  <- costanti di MODULO
```
**⚠ I due rami di `COES_ADIM` sono MUTUAMENTE ESCLUSIVI e condividono UN solo sito di traccia**
— ed è la coppia che ha prodotto il falso positivo di `Z114`.

## LE DIMENSIONI — **coerenti, ed è la cura che le ha rese tali**

| simbolo | dimensione |
|---|---|
| `_F_adim` | **adimensionale**, e `|_F_adim| <= 1` **per costruzione** |
| `_passo_causale = cs_arco·DT` | **`[L]`** |
| `_delta_coes` | **`[L]`** ✅ |

> **È l'unica delle quattro leggi in cui l'incremento ha le unità giuste SENZA che un clip
> gliele dia.** *(Confronta: `proj` della memoria del moto — adimensionale; `spinta` della
> gravità — `[L²]`.)*

## I LIMITI, CLASSIFICATI CON `A11`

| limite | corollario | esito |
|---|---|---|
| `_passo_causale = cs_arco·DT` | **1** | ✅ **causalità LOCALE**: `cs` del nodo più lento, zero parametri |
| | **2** | ✅ non insegue `d0` |
| | **6** | ⚠ **i contatori ESISTONO** *(`_g_cct_stringe`, `_g_cct_allarga`, `_g_cct_archi`, `_g_cct_min`)* **ma la frazione non è in nessun referto**. **Lavoro residuo.** Il massimo misurato è `0.2384`, **e un MASSIMO non dice QUANTO SPESSO** |
| | **7(a)** | ✅ `|_F_adim| <= 1` per costruzione: non è un clip, è un **dominio** |

> **E il tetto locale NON è sempre più stretto:** dove il cono è veloce **ALLARGA**. **È
> causalità, non prudenza** — e va detto, perché la lettura sbagliata *(«una cura che
> restringe»)* circola facile.

## LO STATO: `DA VERIFICARE` — **e quanto pesa**

saldo su 600 passi: **`-1.025e+05`** *(braccio acceso)*, **`-1.064e+05`** *(senza memoria del
moto)*. **Tira GIÙ, come tutti gli scrittori fisici.**

## LE DOMANDE APERTE

1. **Quante volte il tetto causale morde?** I contatori ci sono, **nessuno li ha letti**. Finché
   non lo si fa, non si può dire se `A11` cor.6 sia rispettato. **È lo stesso lavoro residuo del
   freno.**
2. **`scala_statale`, `forza_campo`, `richiamo_elastico`: da dove vengono?** **`NON RICOSTRUITO`**
   in questa scheda — vanno lette dal codice che le costruisce, e non l'ho fatto.
3. **Il ramo storico** *(`COES_ADIM = False`)* **è ancora raggiungibile.** Se non serve più,
   è codice morto che complica l'appaiamento delle tracce *(`Z114`)*; se serve, **cosa lo
   giustifica?**

---

<!-- SCHEDA nome=tempo-proprio funzioni=ritmo,_cli,_applica_flag flag=TAU_LOC,TEMPO_SEGNO,TEMPO_PROPRIO_ORIENTATO,RITMO_WRAP_2PI -->

> ### ➜ **`CURA 2` PASSA DI QUI, e questa scheda deve dirlo** *(2026-09-24, blob `b881db89`)*
>
> `_cli` e `_applica_flag` acquisiscono **`--tempo-unico-mitosi`** *(con `TEMPO_UNICO_MITOSI`
> nel `global`, come `RITMO_WRAP_2PI`: senza, l'assegnamento creerebbe una locale e il flag
> sarebbe **silenziosamente inerte** — il difetto documentato di `--tau-a`)*. **La legge sta in
> scheda ⑨**; qui resta il rimando, perché `REG-R` mappa **per funzione**.
>
> **➤ E `SEMINA_LAM` passa di qui allo stesso modo** *(2026-09-24)*: `--semina-lam` in `_cli`,
> la riga in `_applica_flag`, e **`SEMINA_LAM` nel `global`** — senza il quale l'assegnamento
> creerebbe una locale e il flag sarebbe **silenziosamente inerte**. **La legge sta in scheda
> ⑫.**
>
> **⚠ E C'È UN LEGAME DI SOSTANZA, non solo di funzione: `CURA 2` prende il suo orologio da
> QUI.** `_r_nodo_mitosi` legge `_r_corrente`, cioè l'`r` che **`ritmo()` di questa scheda
> produce**; e il `tau_nodo` che la cura **sostituisce** è **identico al ramo `TEMPO_SEGNO`**
> — un ramo di **questa** scheda **che non gira** *(`Z130`)*. **La mitosi usava come «tempo
> proprio» la definizione di tempo che il resto del sistema ha SCARTATO.**

> ## ✅ **`RITMO_WRAP_2PI` È APPROVATA — decisione di Luca, 2026-09-24**
>
> **Da oggi il driver la accende in OGNI run** *(`--ritmo-wrap-2pi`, cablato in
> `csv/_test_fork/_scena_video.py`)*. `D34` passa da **difetto aperto** a **CURA IN CODICE**.
>
> **Che cosa è stato aggiunto**, perché fino a oggi la cura era accendibile **solo
> in-process**: l'opzione **`--ritmo-wrap-2pi`** nel simulatore e la riga corrispondente in
> `_applica_flag` *(con `RITMO_WRAP_2PI` nel `global`: senza, l'assegnamento creerebbe una
> **locale** e il flag resterebbe **inerte in silenzio** — è il difetto già catalogato di
> `--tau-a`)*.
>
> **⚠ E NON È BYTE-INERTE, ed è il punto:** è una **cura**, non un'opzione. **I numeri presi
> prima di oggi non si confrontano con quelli di dopo senza dirlo** *(par.9-bis)*, e lo stato
> effettivo di ogni run sta in `CONFIGURAZIONE.txt`.
>
> **Il default nel sorgente resta `False`**, come per tutte le cure non ancora in epoca 3: chi
> vuole il braccio di confronto **omette il flag**, e il referto lo mostra.
# ⑤ IL TEMPO PROPRIO — **`ritmo()` / `r` / `dt_n = DT·r`**, e il surrogato **`tau_pp`**

> **STATO: `DIFETTOSA`.** Difetti **`D34`** *(il wrap «a `4π`» non avvolge)* e **`D32`**
> *(due grandezze diverse col nome di tempo proprio)*.
> **È la grandezza da cui dipende il tic di OGNI processo locale** *(par.9: `dt_n = DT·r`, e
> `DT` nudo dentro un rilassamento locale impone un frame preferito, cioè un etere)*.

## LA FORMA — copiata dal codice (`:2536-2646`)

```
se TEMPO_SEGNO:                                 <- OGGI `False`: questo ramo NON gira
    r = 1 + mean(|tw| sugli archi incidenti)/PHI_CRIT
altrimenti, il ramo DE BROGLIE, che e' quello che gira:
    a      = angle(psi) - angle(psi_prec)
    signed = ((a + pi) % (2 pi) - pi) / DT                    <- ramo SCALARE: periodo 2pi
    se CAMPO_SPINORIALE e psi_spin e' allineato:
        a      = angle(psi_spin[:,0]) - angle(psi_spin_prec[:,0])
        signed = ((a + 2 pi) % (4 pi) - 2 pi) / DT            <- ramo SPINORIALE: `D34`
    f    = signed  (o |signed| se non TEMPO_PROPRIO_ORIENTATO)
    med  = median(|f|) del passo PRECEDENTE                   <- gauge SFASATO (cura dell'anello)
    x    = f / med
    r    = x/sqrt(1 + x^2) + 1e-6                             <- SATURA a ~1
    r_n  = r / (1/sqrt(2) + 1e-6)                             <- x=1 -> 1
    ritorna 1 + TAU_LOC*(r_n - 1)
```
**E IL SURROGATO, che e' un'ALTRA legge (`:5160`):** `tau_pp = 1 + |tw|/PHI_CRIT`, **per ARCO**,
usato da **mitosi**, **repulsione** e dalla memoria `_rep`.

## ⚠ IL CODICE CONTIENE IL PROPRIO CONTROESEMPIO

**Il ramo SCALARE avvolge su `2π`. Il ramo SPINORIALE, OTTO RIGHE DOPO, su `4π`.**
**Stessa grandezza, stesso significato, due periodi diversi, nella stessa funzione.**
E il commento di `:2566-2568` dichiara l'equivalenza **con la sua condizione**:
*«nel limite `psi_spin[:,0] = psi` e **`|dphi| < pi`** → ritmo IDENTICO»*.
**`|dphi| < pi` e' ESATTAMENTE la condizione in cui il taglio non si attraversa.**
**Il commento sapeva già dove sta il difetto, e nessuno ha letto la condizione come un
avvertimento.**

## LE DIMENSIONI

| simbolo | dimensione |
|---|---|
| `a`, `signed·DT` | **angolo** — adimensionale |
| `signed`, `f`, `med` | `[1/T]` |
| `x = f/med`, `r`, `r_n` | **adimensionale** ✅ |
| `dt_n = DT·r` | `[T]` ✅ |
| **`tau_pp`** | **adimensionale** — *si chiama «tempo proprio» ma NON ha dimensione di tempo* |

> **`A3c`: `r` e `tau_pp` sono ENTRAMBI adimensionali, quindi CONFRONTABILI** — ed è
> precisamente per questo che `D32` è un difetto e non un equivoco di notazione: **due numeri
> puri con lo stesso nome fisico e correlazione `~0`.**

## COSA LEGGE / COSA SCRIVE

- **legge:** `psi`, `_psi_prec`, `psi_spin`, `_psi_spin_prec`, `_med_f_prec`, `tw` *(solo nel ramo
  `TEMPO_SEGNO`, che non gira)*.
- **scrive:** `_med_f_ultimo` *(registro, promosso da `step()`)*, e **`_r_corrente`** — che
  **`step()`** salva. **`ritmo()` non scrive nessuno snapshot**, di proposito: ha **tre**
  chiamanti e **due sono DIAGNOSTICI**; se avanzasse lo stato qui, ogni chiamata diagnostica
  muoverebbe la fisica *(par.2.3)*.
- **a valle:** `dt_n = DT·r` — **il tic di ogni processo locale**.

## I LIMITI, CLASSIFICATI CON `A11`

| limite | corollario | esito |
|---|---|---|
| `+1e-6` in `r = x/√(1+x²) + 1e-6` | **1** | ❌ **numero SCELTO**, non un vincolo fisico |
| | **2** | ✅ costante |
| | **6** | ⚠ **e' un PAVIMENTO che MORDE:** `min(r) = 1.414212e-06` **misurato**, cioè **esattamente il pavimento** *(`Z117`)*. **Quando `f ≈ 0` il tempo proprio del nodo NON si ferma: si ferma AL PAVIMENTO** |
| `max(median(|f|), 1e-9)` | **1** | ⚠ difesa dalla divisione |
| la saturazione `x/√(1+x²)` | **7(a)** | ✅ identità per `x ≪ 1`; **e non è un `clip`: è liscia ovunque**, derivata continua |

> **⚠ E IL «RAPPORTO `max/min` = `1.000e+06`» NON È UNA MISURA:** è `1.4142 / 1.4142e-6`,
> cioè **`1/1e-6`, l'inverso della regolarizzazione**. **Correzione a una mia frase di `Z110`**,
> che lo chiamava *«il clip»*.

## LO STATO: `DIFETTOSA`

- **`D34`** — il wrap del ramo spinoriale. **Dimostrato:** `max|w4(a) − a| = 0.000e+00` su
  `100 001` punti. **Misurato raro:** `4.45e-05` dei nodi, `12` chiamate su `119`; **ma
  arricchimento `728.94 x` al tetto** e **gauge invariato** *(`1.000000`)*.
  **✅ CURA `RITMO_WRAP_2PI`, IN CODICE dal 2026-09-22** *(blob `21e3a3dc` → `3d91338e`)*,
  **spenta di default**. **Tocca UNA SOLA riga e SOLO il ramo spinoriale:**
  `signed = ((a + π) % 2π − π)/DT`, **la stessa forma del ramo scalare otto righe sopra**.
  **Il default NON si cambia qui:** è una decisione di Luca dopo la prova a 600 passi *(`E3`)*.
- **`D32`** — `r` e `tau_pp`: correlazione **`-0.13`…`+0.29`**, segno non concorde.
  **Cura: DA DECIDERE** — §D del mandato propone **un solo tempo proprio** *(`r`, letto come
  osservabile)*, con **`tau_pp` tolto** e la mitosi che legge `r`. **È una lettura DA PROVARE,
  non una decisione presa.**

## LE DOMANDE APERTE

1. **Se si unifica il tempo proprio, quali leggi cambiano significato?** `tau_pp` compare in
   **12 righe di codice**: mitosi *(soglia, segno, ampiezza)*, repulsione, e il rilassamento di
   `_rep`. **Vanno elencate una per una prima di toccarle** — è il lavoro di `PROBLEMI-CHK3`.
2. **Il pavimento `1e-6` è un vincolo o una difesa?** Oggi **morde**: `min(r)` è esattamente
   lui. **Un nodo con `f = 0` che tempo proprio ha?** *(Zero è una risposta fisica; `1.414e-6`
   è un numero scelto.)*
3. **⚠ L'ANELLO CHE `A6` TIENE D'OCCHIO, posto da Luca il 2026-09-22:** **l'orologio dello spinore si calcola dalla VARIAZIONE della fase dello spinore, e poi FA AVANZARE quella stessa fase.** `r` viene da `angle(psi_spin) − angle(psi_spin_prec)`; `dt_n = DT·r` entra nell'integrazione che **muove `psi_spin`**; al passo dopo `r` si rimisura da lì. **È un anello CHIUSO.**
   **NON è retroazione ISTANTANEA** — lo snapshot è **ritardato** *(`_psi_spin_prec` è del passo precedente, promosso da `step()`)*, **e questo lo mette fuori dalla lettera di `A6`**. **Ma è esattamente la forma che `A6` sorveglia**, e va scritto invece di essere dedotto ogni volta da capo.
   **NON DA CHIUDERE ORA.** La domanda è: *un orologio che misura sé stesso può derivare senza che nulla lo riporti indietro?* — e il candidato per deciderlo è la **dispersione di `r` a codice invariato fra semi**, che oggi **non è misurata**.
4. **Il gauge è `median(|f|)` del passo PRECEDENTE** — cura dell'anello istantaneo *(`A6`)*.
   **Ma resta una statistica GLOBALE dentro una legge per nodo** *(`A2`)*. **È accettabile
   perché è un GAUGE, o è lo stesso difetto di `D01`?** **NON DECISO.**

---

<!-- SCHEDA nome=fase-phi funzioni=_w4,_w8,_wphi,_dphi,circolazione_topologica,semina,step flag=FASE_2PI,TORS_4PI -->
# ⑥ LA FASE `φ` E IL SUO DOMINIO — **`semina` / `_w4` / `_w8` / `step`**

> **STATO: `DIFETTOSA`.** Difetti **`D34`** *(il wrap del ritmo)*, **`D35`** *(l'antifase di
> Schwinger)*, e i sospetti **`S07`**, **`S08`**.
> **⚠ QUESTA SCHEDA RIVENDICA `step` IN VIA PROVVISORIA:** `step` fa **tutto**, e attribuirlo
> alla fase è improprio. Lo tiene perché `REG-R` mappa **per funzione** e i due siti di `φ`
> vivono lì. **Quando `step` avrà la sua scheda, il marcatore si divide.**
>
> ### ➜ **E `semina()` HA UN RAMO NUOVO: `SEMINA_LAM`** *(2026-09-24)*
>
> Questa scheda rivendica `semina` **per la FASE** *(`φ` nasce su `[0, 4π)`)*. Il ramo nuovo
> **non tocca la fase**: tocca **le POSIZIONI** — ogni nodo a distanza `>= LAM` da qualunque
> altro, con `RSA` — e **la sua legge sta in scheda ⑫**.
> **⚠ Ma è nella STESSA funzione**, quindi una modifica futura alla fase della semina e una alla
> geometria **si incontrano qui**. *(Stessa ragione per cui questa scheda rivendica `step` «in
> via provvisoria»: quando `semina` avrà la sua scheda, il marcatore si divide.)*
>
> ### ➜ **E `CURA 2` HA TOCCATO `step`, con una modifica SENZA FLAG** *(2026-09-24)*
>
> La media **armonica** d'arco di `:4791` — `cs_arco = 2·cs_i·cs_j/(cs_i+cs_j)`, il *«collo di
> bottiglia causale»* — è stata **ESTRATTA nel metodo `_cs_arco_da_nodo`** e `step()` ora lo
> **chiama**, **senza che l'espressione cambi di una virgola**. Motivo: `mitosi()` ne ha
> bisogno per `tau_arco = d/cs_arco`, e **duplicarla avrebbe dato due leggi che possono
> divergere**.
>
> **⚠ NON È GATED DA NESSUN FLAG**, quindi nessun sigillo di byte-inerzia del *flag* la copre:
> **la copre solo `T4`**, che confronta il run a flag SPENTO col riferimento `_cura1_corto`.
> **Se `T4` fallisce, il primo sospetto è questa estrazione, non la cura.**
>
> *(E conferma ciò che questa scheda dice già: `step` fa troppe cose perché una sola scheda lo
> rivendichi. La divisione del marcatore resta in coda.)*

## LA REGOLA DI FONDO *(decisione di Luca, 2026-09-22)*

> **Lo spinore ha periodo `4π`; tutto ciò che si OSSERVA da lui ha periodo `2π`; un ACCUMULO
> non ha periodo.**
> `np.angle`, `|ψ|²`, `exp(iφ)`, `cos`, `sin` hanno **periodo `2π`**: **non vedono il segno
> dello spinore.** **Un avvolgimento su `4π` applicato a una grandezza a periodo `2π` non
> avvolge niente. Un «`+2π` = antifase» letto attraverso `exp(iφ)` è un'identità.**
> **Per ogni `π` del codice la domanda è: questa grandezza è lo SPINORE, un'OSSERVABILE o un
> ACCUMULO?**

## LA FORMA OGGI — copiata dal codice

```
semina  (:2349-2350)   phi, phi0 <- ph % (4 pi)                    <- il dominio DICHIARATO
step    (:4625)        phi <- (phi_t + dt_n_s*phivel + dsync) % (4 pi)
mitosi  (:5289-5357)   fm, phi[a], phi[b], phi[g]  % (4 pi)
mem_mot (:6105)        phi[ii] <- (phi[ii] + shift) % (4 pi)
_w4     (:3423)        (a + 2 pi) % (4 pi) - 2 pi                  <- differenze di fase
_w8     (:3426)        (a + 4 pi) % (8 pi) - 4 pi                  <- la TORSIONE accumulata
```

## ⚠ IL FATTO MISURATO, ed è il cuore della scheda

**In `31` righe su `31` il campo legge `φ` attraverso `exp`, `cos`, `sin` o `angle`** *(`Z118`,
censimento da AST)*. **In tutte e 31 la doppia copertura di `φ` è INVISIBILE alla fisica**,
perché `exp(i(φ + 2π)) = exp(iφ)`. **Non è un'interpretazione: è un conto.**

**E la verifica che Luca ha chiesto è stata fatta** *(`Z120`)*: **nessuna riga della FISICA
distingue `φ` da `φ + 2π`**, fuori dalla torsione *(`_w4`/`_w8`)* e dall'antifase.
`31` candidati letti uno per uno: `13` assegnamenti, `7` torsione, `2` antifase, `6` diagnostici.

> **⚠ E UNA PREMESSA CHE È CADUTA, scritta qui perché non si riusi:** il docstring di
> `_passo_spinoriale` dice che `φ` è **l'azimut del vettore di Bloch**. **MISURATO: FALSO**
> *(`Z121`, `R ≤ 0.18` contro un criterio di `0.90` e un nullo di `0.016`)*.
> **Se `φ` non è l'azimut, che cos'è? → `S08`, aperto.** **Refutare non è spiegare.**

## LE DIMENSIONI

`φ`, `_w4(Δφ)`, `_w8(…)`, `twist_dip` sono **angoli**, cioè adimensionali. **Coerente.**
*(Il difetto non è dimensionale: è di PERIODO.)*

## I LIMITI, CLASSIFICATI CON `A11` e con le classi `T/L/E`

| punto | classe | esito |
|---|:--:|---|
| `% (2π)`, `% (4π)`, `_w4`, `_w8` | **`T`** | **NON si levigano.** Il salto da `2π` a `0` è un artefatto della **coordinata**: levigarlo **inventerebbe valori che non esistono**. **La cura è il PERIODO GIUSTO** |
| la soglia della mitosi, `discesa`, il punto di inversione | **`L`** | **si levigano**, coi tre obblighi del cor.7 e la **larghezza DERIVATA** — **ma appartengono a `SCALE-TW`, non a qui** |
| la nascita di un nodo | **`E`** | **evento discreto**: resta discreto, **ma il suo TASSO dev'essere liscio** |

## LA CURA DECISA — **`FASE_2PI`**, spenta di default — ✅ **IN CODICE** *(blob `3d91338e` → `445e2896`)*

**I DUE AIUTANTI, e sono il punto della forma:** **`_dphi()`** *(il periodo)* e **`_wphi()`** *(l'avvolgimento di una differenza)*. **UN SOLO POSTO da cui tutti prendono il periodo**, così non si possono sfasare fra loro — **che è esattamente il difetto che `D34` ha mostrato costare caro**: due rami della stessa funzione con due periodi diversi, a otto righe di distanza.

> **Decisione di Luca, presa dopo la verifica di `Z120`.** **Regge su TRE argomenti invece dei
> quattro iniziali**, perché il quarto *(l'azimut)* è caduto con `Z121` — **e l'argomento
> caduto non argomenta per `4π`: dice solo che `φ` non è ciò che il commento dichiarava.**

**`φ` è una FASE ORDINARIA su `[0, 2π)`. L'antifase è `+π`.**
**La doppia copertura resta dove è già vera: nel SEGNO esplicito** *(`_spinor_lift`,
`s_k = sign(perc_chi)`)* **e nei MEZZI ANGOLI** *(`exp(-0.5i…)`)* — **un solo ponte** *(`A10`)*.

**COSA TOCCA, e nient'altro:**

| | sito | oggi | con `FASE_2PI` |
|---|---|---|---|
| (a) | `:2349`, `:2350`, `:4625`, `:5289`, `:5291`, `:5353`, `:5354`, `:5357`, `:6105` | `% (4π)` | **`% (2π)`** |
| (b) | `:2218`, `:4628`, `:5273`, `:5403`, `:5404`, `:5508`, `:5509` | `_w4(Δφ)` | **`_w2(Δφ)`** *(via `_wphi`)* |
| (c) | `:5311` *(dormiente)*, **`:5443`** *(`D35`, attivo)* | `+2π` | **`+π`** |
| (d) | `:5104` | `soglia0 = 2π + π = 3π` | **`soglia0 = 2π`** |

**⚠ COSA NON TOCCA, ed è una scelta di confine:** **`:4651-4655`**, dove `_w8`/`_w4` avvolgono
la **TORSIONE ACCUMULATA** *(`tw`, `twp`)*. **`tw` è un ACCUMULO: non ha periodo**, e il suo
dominio appartiene a **`SCALE-TW`**. **Toccarlo qui mescolerebbe due decisioni.**
*(La conseguenza — `dph` passa da `(-2π, 2π]` a `(-π, π]`, quindi `twp` cambia intervallo
— **non è una modifica: è un effetto, ed è il test `E1`.**)*

**⚠ E IL PUNTO (e) DEL §D È GIÀ IN CODICE:** *«la coppia nasce con lo spinore di segno
opposto»* — `:5477` fa già `_eredita_spinore_figli(aa, segno=-1)`. **Verificato dal sorgente:
non c'è niente da cambiare lì.**

## LE DOMANDE APERTE

1. **`S08`: se `φ` non è l'azimut del Bloch, che cos'è?** **Non si risolve con un'altra
   misura adesso** *(decisione di Luca)*.
2. **`S07`:** `:5894` collassa a `2π` una differenza a `4π` — **dormiente** *(`K_FRANGE = 0`)*.
   **Con `φ` su `2π` quella riga diventa corretta per costruzione:** la cura la sana senza
   toccarla.
3. **Il dominio di `tw` resta a `4π`/`8π`.** **Con `φ` su `2π` è ancora il dominio giusto,
   o `_w8` diventa l'identità come lo era il wrap del ritmo?** → **`SCALE-TW`**.

---

<!-- SCHEDA nome=mitosi-schwinger funzioni=mitosi flag=MITOSI_DIR,ANTIFASE_ADD,COPPIA_MIT,PLAST_MIT,KICK_TW,REGIME -->
# ⑦ LA MITOSI E SCHWINGER — **`mitosi()`**

> **STATO: `DIFETTOSA`.** Difetti **`D35`** *(l'antifase della coppia)* e **`D33`** *(la
> repulsione che si spegne al tetto)*. Piu' **`D03`** per la parte di `_rep`.
>
> ### ➜ **`CURA 2` MODIFICA `mitosi()`, e la legge sta in scheda ⑨** *(2026-09-24)*
>
> Quattro rami gated su **`TEMPO_UNICO_MITOSI`** *(spento di default)*: `grad_tau`, il fattore
> di tempo di `ampiezza`, la forma di `prob`, il bersaglio e il rilassamento di `_rep`.
> **I quattro usi di `tau_pp` come POSIZIONE sull'asse della torsione** — `tau_soglia`,
> `tau_tetto`, `centro`, `segno`, cioè **la forma riportata qui sotto** — **NON sono toccati**,
> e il sigillo lo verifica **dall'AST** *(`T3`)*, non a parola.
>
> **➜ E `mitosi()` HA UN CONTATORE IN PIÙ, incondizionato** *(2026-09-24, `_tum_clip0_prob`)*:
> `np.clip(resp, 0, 1)` taglia **in alto E IN BASSO**, e finora contavo **solo il lato alto**.
> **Il lato basso morde su tutto il regime repulsivo** — cioè sulla metà di questa scheda che
> riguarda `_rep`. **Byte-inerte per costruzione, non misurata.**
>
> **⚠ E IL CLIP SU `rep` HA LO STESSO DOPPIO LATO E IL CONTATORE DEL LATO BASSO NON C'È ANCORA.**
>
> **⚠ E `D33` È DENTRO IL PERIMETRO DELLA CURA:** *«la repulsione che si spegne al tetto»* vive
> su `_rep`, che `CURA 2` cambia in **due** punti — il bersaglio *(ora senza il fattore di
> tempo)* e l'integratore *(ora esatto invece che Eulero)*. **La cura NON dichiara di curare
> `D33`**, e il criterio `R` misura proprio **quanto `d0` si allarga**: la previsione di Luca è
> **×2.5-×3** sul bersaglio. **Se `D33` si muovesse, sarebbe un effetto collaterale da
> RIPORTARE, non un merito da rivendicare.**

## LA FORMA — copiata dal codice

```
soglia0 = PHI_CRIT + twist_max = 2pi + pi = 3pi          (TORS_4PI acceso)
soglia  = soglia0 * (1 - 0.3*tanh(grad_tau))             modulazione LOCALE
ecc     = max(|tw|/soglia - 1, 0)
salita  = satura(ecc)                                     zero sotto soglia
discesa = clip(1 - |tw|/TW_TETTO, 0, 1)                   ZERO da 4pi
tau_pp  = 1 + |tw|/PHI_CRIT                               <- il "tempo proprio surrogato"
centro  = 0.5*(tau_soglia + tau_tetto)
segno   = -tanh(3.0*(tau_pp - centro))                    + crea, - respinge
resp    = salita * discesa * (1/tau_pp) * segno
prob    = clip(resp, 0, 1)        ->  nasce = rng < prob             (CREAZIONE)
rep     = clip(-resp, 0, 1)       ->  _rep rilassa con tau_pp        (REPULSIONE)
```
**LA COPPIA (Schwinger):** `prob_coppia = 1 - exp(-COPPIA_MIT * eccesso)`, e il partner nasce
con **`anti = (fm + 2π) % 4π`** *(`:5443`)* **e lo spinore di segno opposto** *(`:5477`)*.

## ⚠ I DUE DIFETTI, MISURATI

**`D35` — l'antifase non è un'antifase.** Il campo è `F = Σ K·exp(iφ)`, e
`exp(i(φ + 2π)) = exp(iφ)`: **nel campo l'antiparticella è IDENTICA alla particella.**
**Il commento dice `+π`, il codice fa `+2π`: fa fede il codice.**
**E il ramo È ATTIVO:** `COPPIA_MIT = 1.0`, e `S07_schwinger` scatta **`102` · `90` · `172`**
volte su 600 passi nei tre bracci *(`Z119`)*.

**`D33` — la repulsione si spegne dove servirebbe.** Il `segno` si inverte oltre `~3.5π`, **ma
`discesa` è ZERO ESATTO da `4π`**: la finestra utile è larga **mezzo `π`**, e **dal `75 %`
al `96 %` degli archi oltre l'inversione riceve repulsione esattamente zero** *(`Z111`)*.

## I LIMITI, CLASSIFICATI

| limite | classe | `A11` |
|---|:--:|---|
| `soglia0 = 3π` | **`L`** | ⚠ **derivazione A POSTERIORI**: `2π + π` è stato giustificato dopo, e **cade con `FASE_2PI`** *(`§D` punto 2)*. **È il punto più incerto, e lo decide `E1`** |
| `0.3 * tanh(grad_tau)` | **`L`** | ❌ il `0.3` è **scelto** *(`A1`)* → `SCALE-TW` |
| `clip(1 - \|tw\|/4π, 0, 1)` | **`L`** | ❌ **`D33`**: azzera il ramo repulsivo oltre `4π`. **Due leggi in un prodotto solo** |
| `tanh(3.0 * …)` | **`L`** | ❌ il `3.0` è **scelto** → `SCALE-TW` |
| `0.02 * d0 * _rep` | **`L`** | ❌ il `0.02` è **scelto**, già dichiarato in `D03` |
| la nascita di un nodo | **`E`** | ✅ **evento discreto con TASSO liscio** — la campana **è** già liscia; **ma `salita` ha un `max(…, 0)` e `discesa` un `clip`: due spigoli DENTRO il tasso**, da verificare |

## COSA CAMBIA CON `FASE_2PI` — ✅ **IN CODICE** *(blob `445e2896`)*, spenta di default

- **`anti = (fm + π) % 2π`** — cura `D35`;
- **`soglia0 = 2π`** — *«un arco porta una differenza fino a `π`; quando porta un quanto
  intero (`2π`) si divide, e ciascuna metà ne porta `π`»* *(Luca)*;
- **e il punto di inversione SI SPOSTA come conseguenza:** `tau_soglia` passa da `2.5` a `2`,
  quindi `centro` da `2.75` a **`2.5`**, cioè **l'inversione da `3.5π` a `3π`**. **La finestra
  di `D33` si allarga da mezzo `π` a un `π` intero** — **non è una cura di `D33`, è un
  effetto, e va misurato.**

## LE DOMANDE APERTE

1. **`E1`: la mitosi a `2π` funziona senza tarature?** Né zero mitosi né esplosione. **Se
   fallisce, cade il punto 2 del `§D`**, e con esso la soglia a `2π`.
2. **`E2`: le coppie annichilano?** Oggi la frazione è `~0`. **Se resta `~0` con `+π`, cade il
   punto 5**, e `S06` *(il «muro dell'1 %»)* **non** ha la spiegazione che sembra avere.
3. **L'argomento della soglia vale per una differenza ISTANTANEA, ma `tw` è un ACCUMULO che
   decade.** **È la crepa dichiarata da Luca stesso**, e `E1` è il suo giudice.

## I CRITERI DEI TEST, **fissati PRIMA di girare** *(par.5-septies)*

> **⚠ CHI HA SCRITTO QUALE TEST, e va detto perché due sono MIEI — è `Z125`.**
> Nel repo esistevano **solo `E1` ed `E2`**, e ho citato *«i quattro test `E1`-`E4`»* **undici
> volte** senza che `E3` ed `E4` fossero scritti da nessuna parte. **`E1` ed `E2` sono di Luca
> e non si toccano; `E3` ed `E4` li DERIVO, e Luca può sostituirli.**
> Lo strumento è **`csv/_test_fork/_f2p_test_E.py`**, e i criteri stanno **nel suo codice**,
> non solo qui *(`P1-ter`)*.

| test | di chi | criterio | **origine della soglia** |
|---|:--:|---|---|
| **`E1a`** la mitosi non muore | **Luca** | `_g_nati_mitosi > 0` e `n` cresce | il nullo: se la cura rompesse `fm`, le nascite sarebbero `0` |
| **`E1b`** la mitosi non esplode | **Luca** | `n` finale **< 10×** il riferimento, e il run **arriva** a 600 passi | **MISURATA: `178` archi per nodo** *(`526672 / 2959`)*. `10× n` = `~5.3M` archi = `10×` memoria e tempo: **oltre, il sistema non è simulabile, e QUELLA è l'esplosione**. **`MAX_NODI = 4000000` non serve: è una guardia di memoria, non di fisica** |
| **`E1c`** il **fattore** | *mio* | le nascite salgono di un fattore **fra `5×` e `100×`** | **DERIVATA dagli archi GIÀ SUL DISCO**: la campana ha il picco a `|tw| = soglia`, e la finestra **nuova** *(`tau` `2.0`-`2.5`)* contiene **`17113`** archi contro i **`346`** della vecchia *(`tau` `2.5`-`3.0`)* al passo 600 — **`49.46×`**. La banda è **un ordine per lato** perché la **larghezza** della campana non entra nel conto e **la mitosi CONSUMA la torsione** *(retroazione che smorza)*. **Questo test giudica ME, non la cura** |
| **`E2`** le coppie annichilano | **Luca** | **NON MISURABILE**, e si dichiara | vedi il blocco qui sotto |
| **`E3`** la finestra di `D33` | *mio* | si riporta la **popolazione** delle due finestre nei due bracci | il §E **stesso** dice *«non è una cura di `D33`, è un effetto, e va misurato»*. **Si RIPORTA, non si giudica** |
| **`E4`** i diagnostici di fase | *mio* | `max(φ) < 2π` nel braccio della cura | la **riserva ② di `Z120`**. **Il nullo è il sigillo:** a flag spento `max(φ) = 12.565546` |

### ❌ **`E2` NON È MISURABILE IN QUESTO RUN, e lo dichiaro invece di riportare uno zero**

**L'ANNICHILAZIONE VIVE SOLO DENTRO `ANTIFASE_ADD` (`:5351`), CHE È `False`.**
Il ramo che la cura tocca — **`:5499`** — è la **creazione di coppia alla Schwinger**, e lì
l'antifase decide se l'antiparticella è **DISTINGUIBILE** dalla particella nel campo: che è la
**precondizione** dell'annichilazione, **non l'annichilazione**.

**Riportare uno zero sarebbe leggere un'ASSENZA DI MECCANISMO come un'assenza di effetto** —
lo stesso errore del `max|A-B| = 0.000e+00` per **mancanza di confronto**.

**COSA SI MISURA AL SUO POSTO**, e il valore atteso **non è scelto**, è `|exp(i s) − 1|`:

| | `max|exp(i·anti) − exp(i·part)|` |
|---|--:|
| **spenta** — `+2π` su dominio `4π` | **`2.156e-15`** → **identica**: è `D35` |
| **accesa** — `+π` su dominio `2π` | **`2.000000`** → **opposta** |

> ### ⚠ **E LA CONSEGUENZA PER `S06` È PIÙ FORTE DELLA DOMANDA DI PARTENZA**
> Il «muro dell'1 %» **non si spiega con `D35` da solo**: il meccanismo che annichilerebbe
> **non gira**. **`S06` non si chiude con questa cura**, e per misurarlo servirebbe accendere
> `ANTIFASE_ADD` — che è un **ESPERIMENTO** *(par.10)*, **non fisica**, e va **chiesto a Luca**
> invece che deciso qui.

### ✅ **IL CONTROLLO DELL'INVOLUCRO È STATO FATTO PRIMA** *(`STANDARD ⑤`)*

Lo strumento puntato sul **riferimento CONTRO SE STESSO** dà **`2/4`**: `E1a` e `E1b`
**passano**, **`E1c` e `E4` NON passano** — perché il braccio della «cura» *è* il riferimento.
**I criteri non sono vuoti.** → `csv/_test_fork/_f2p_CONTROLLO_involucro.txt`

**E il controllo ha trovato un difetto prima del run:** `n` **non è una chiave** dello snapshot
*(si legge da `len(phi)`)*, e lo strumento si schiantava con `KeyError: 'n'`. **Su un run vero
lo schianto sarebbe arrivato dopo quaranta minuti.**

---


### ❗ LA MITOSI CHIAMA `_nasce` DUE VOLTE, E LE DUE CHIAMATE NON HANNO LA STESSA MOLTEPLICITÀ *(2026-09-25)*

**Fatto di questa scheda, e ci si sbaglia facile** *(mi ci sono sbagliato io)*:

```python
dh    = self._nasce(dh,    'mitosi', 2, 0)   # `len(sel)` voci -> concat([d[keep], dh, dh])
d0new = self._nasce(d0new, 'mitosi', 0, 1)   # d0new e' GIA' concat([d0h, d0h])
```

> **`dh` ha una voce per arco che si divide, ma diventa DUE archi di `d`.**
> **`d0new` ha già le due voci dei figli.**
> **Chi conta le voci invece degli archi sbaglia di `2` sul primo e di niente sul secondo** —
> cioè in modo **asimmetrico fra le due grandezze**, che è il difetto peggiore da leggere.

**E IL RAMO SCHWINGER È UN TERZO CASO:** `dd` finisce in `concat([d, dd, dd])` **e** in
`concat([d0, dd, dd])`, quindi è `×2` su **entrambe** le grandezze — e **la sua lunghezza viene
da `pos`, non da `d`** *(voce `A3` della coda)*.

**La legge dei contatori sta nella scheda `freno-scala-min`, con `_nasce`.**

<!-- SCHEDA nome=torsione-spinore funzioni=_passo_spinoriale,_applica_flag flag=TW_SPINORE,SYNC_SPINORE,SPIN_LARMOR,SPIN_FEEDBACK -->

# ⑧ TORSIONE → SPINORE — **il ponte INVERSO**

> **Scheda aperta il 2026-09-24 per `CURA 1b`.** È l'unica legge del registro che esiste
> **per essere bloccata**, non per essere applicata.

## LA FORMA, dal codice

```
:3095   _twh = self.tw[mask] / (2.0 * max(PHI_CRIT, 1e-9))
:3097   _otw = np.zeros((n, 3));  _degt = np.zeros(n)
:3098   np.add.at(_otw, ii, _axis * _twh[:, None])          # mutazione IN PLACE
:3099   np.add.at(_otw, jj, _axis * _twh[:, None])
:3100   omega_new = omega_new + _otw / np.maximum(_degt[:, None], 1.0)
```

**Il verso è: `tw` → `omega_s` → `_psi_spinor`.** La **torsione**, che prende la sua scala da
`phi`, **scrive lo SPINORE**.

## PERCHÉ È IL VERSO SBAGLIATO

**È la classe `INVERSA` della mappa del `4pi`** *(`csv/_test_fork/_diag_D/MAPPA_4PI.md`:
`:3100` e la sua conseguenza `:3264`, le **uniche due** su 139 punti)*.

| | |
|---|---|
| il `4pi` di `_psi_spinor` | **`VERA`**: un oggetto di spin 1/2 torna in sé dopo `4pi`. È fisica |
| il `4pi` di `phi` | **`DICHIARATA`**: una **convenzione del codice** |
| `tw` | **`EREDITATA`**: prende la scala da `phi` |

**Quindi `TW_SPINORE` fa scrivere il `4pi` VERO dal `4pi` FINTO.** E la freccia causale del
par.4 di `CLAUDE.md` dice l'opposto: *«i nodi guidano, gli archi ricordano»* — **se in un test
gli spinori diventano passivi (il link li comanda) → BUG, da rilevare, non l'obiettivo.**

## E IL COMMENTO È FALSO, che è una ragione in più

Il commento (`:705-709`, `:2146-2148`) dice che la torsione *«pilota il Bloch di `tw/2`»*, cioè
un **ANGOLO**. **Il codice somma `tw/(2·PHI_CRIT)` a `omega_new`, che è una VELOCITÀ
ANGOLARE**: l'angolo effettivo è **`1.564e-03` rad/passo** contro i **`9.827e-01`** dichiarati,
**fattore `628.3 = 2π/DT`** — *un'unità di misura mancante, non un'approssimazione*.
E il termine finisce in **`self.omega_s`**, la **memoria persistente**, mentre il commento di
`SYNC_SPINORE` dice, **dello stesso blocco**, che metterci un torque *«darebbe
accumulo/divergenza»*. **Unico fra i termini del blocco, `_otw` NON è diviso per l'inerzia.**
→ `doc/REFERTO_tw_spinore.md`, fronte `W`.

## ✅ NON HA MAI GIRATO — **misurato, non supposto**

**`TW_SPINORE = False` in 9 run su 11 ricostruibili**, e **`--tw-spinore` non compare in
nessun lanciatore committato** a nessuno di quei commit
*(`csv/_test_fork/_RICOSTRUZIONE_config.txt`, `Z128`)*. I due non ricostruiti sono i due
`controllo`, che non lasciano snapshot.

> **Nessuna misura di questo programma è contaminata da questa legge.** È il motivo per cui
> bloccarla **non ritira nulla**.

## LA CURA — `CURA 1b`: **il simulatore RIFIUTA DI PARTIRE**

**Decisione di Luca, 2026-09-24.** `TW_SPINORE` resta **nel codice, spento, e BLOCCATO**: se
qualcuno lo accende, il simulatore **si ferma con la ragione**.

**Perché un blocco e non la cancellazione:** par.10 — *«il codice di una legge esclusa non si
cancella mai: resta spento, ed è l'evidenza che spiega perché esiste il suo sostituto»*.
`TW_SPINORE` esiste **perché** `SPIN_LARMOR` fallisce: cancellarlo farebbe perdere il
**perché**.

**Perché un blocco e non un semplice default spento:** il default è già spento, e **non ha
impedito nulla** — `A9`: *un presidio che non impedisce non è un presidio*. Un flag che
introduce il **verso sbagliato del ponte** non deve poter essere acceso **per sbaglio**, e
oggi basterebbe `--tw-spinore`.

**Che cosa NON è:** non è una cura di un difetto misurato, perché **la legge non ha mai
girato e quindi non ha prodotto nulla da curare**. È un **presidio strutturale**, e va detto
così invece di contarlo fra le cure.

## COSA NON SI SA DERIVARE — **dichiarato** *(`A12` regola 4)*

**Se un ponte torsione → spinore possa esistere AFFATTO, in qualche forma.**
L'architettura a un solo ponte dice che la torsione va **ricavata dal trasporto degli
spinori** *(olonomia SU(2))*, non dalle differenze di `phi`. **In quell'architettura la
domanda cambia**: la torsione sarebbe già una proprietà degli spinori trasportati, e una
retroazione su `omega_s` **non sarebbe più un ponte inverso** — sarebbe dinamica interna.
**Non lo so derivare oggi, e non lo decido: è la domanda che il `CHECKPOINT` mette a Luca.**

## ✅ LA CURA È IN CODICE — 2026-09-24

**`_applica_flag`, subito dopo `TW_SPINORE = bool(getattr(a, "tw_spinore", False))`:**

```python
if TW_SPINORE:
    raise SystemExit("[tw-spinore] RIFIUTO DI PARTIRE: e' il ponte inverso. ...")
```

**Il messaggio nomina la ragione** *(il ponte inverso, le righe `:3090-3100`, la scheda, il
referto col commento falso)* **e dice come riaprirlo**: *«una decisione di Luca, non la
rimozione di questa riga»*.

**Perché in `_applica_flag` e non nel punto d'uso:** lì il rifiuto arriva **prima che la scena
nasca**, quindi non c'è nessun run a metà da interpretare. Un rifiuto dentro `step()` lascerebbe
uno stato parziale sul disco.

---

<!-- SCHEDA nome=tempo-nella-mitosi funzioni=mitosi,_cs_arco_da_nodo,_r_nodo_mitosi,_fattore_tempo_arco,_tau_arco_causale flag=TEMPO_UNICO_MITOSI,MITOSI_DIR -->

# ⑨ IL TEMPO NELLA MITOSI — **`CURA 2`**

> **Mandato di Luca, 2026-09-24.** Flag: **`TEMPO_UNICO_MITOSI`**, spento di default.
> **Riscritta** dopo il mandato: la prima stesura aveva **due errori**, segnati con ❌.

## 0. IL PRINCIPIO, ed è di Luca

> ### **«Si applicano le cose CORRETTE e COERENTI. Dove intenzione e implementazione
> ### divergono, si realizza l'INTENZIONE. Ogni grandezza con le sue UNITÀ giuste.»**

**Operativamente: si cura dove intenzione e implementazione DIVERGONO; dove sono coerenti non
si tocca.** L'intenzione si legge **dal commento e dal nome**, che sono ciò che la legge
*dichiara di essere*.

| riga | l'INTENZIONE, dal commento | l'IMPLEMENTAZIONE | coerenti? |
|---|---|---|:--:|
| `:5240` | *«ritmo»* | `1/(1 + |tw|/PHI_CRIT)`: reciproco di una **torsione** | **NO** |
| `:5244` | una **probabilità** | `clip(resp, 0, 1)`: un **clip** `A11` | **NO** |
| `:5280` | *«rilassa con tempo `tau_pp` — **un tempo locale dello stesso arco**»* e *«`A5` livello 1, **rilassamento esponenziale**»* | una **torsione** come costante di tempo, **e un EULERO esplicito** | **NO, due volte** |
| `:5189-5196` | *«gradiente di **tempo proprio** lungo l'arco»* | gradiente di `mean(|tw|)` | **NO** |
| `:5234-5239` | soglia, tetto, centro, **inversione**: posizioni sull'asse di `tw` | esattamente quello | **SÌ → NON SI TOCCA** |

---

## 1. UN SOLO TEMPO D'ARCO: **`dt_e`, che il sistema definisce già**

**`:4352`: `dt_e = DT * 0.5 * (r[i] + r[j])`.** È **il** tempo proprio d'arco del sistema, e la
mitosi usa **quello**, cioe' il fattore adimensionale **`dt_e/DT = 0.5(r_i + r_j)`**.

### ❌ **IL MIO PRIMO ERRORE: avevo proposto `min(r_i, r_j)`**

**Era sbagliato per la ragione più semplice: creava un SECONDO orologio d'arco**, accanto a
quello che il sistema ha già. *«Un solo tempo»* è il nome di questa cura, e la mia proposta ne
aggiungeva uno.

**E l'argomento con cui l'avevo scartata la media era anch'esso sbagliato:** avevo scritto che
una media *«viola `A2`, è una statistica in una legge locale»*. **`A2` riguarda le statistiche
GLOBALI** — una mediana su tutta la rete, una media su tutti i nodi. **La media dei DUE nodi di
un arco è locale per costruzione**, ed è la definizione che il sistema usa già.

> **L'argomento causale per `min(r)` non è privo di senso, ma se vale, vale per TUTTO il
> sistema, non per la mitosi da sola.** → va **in coda** come proposta generale, `S13`.

### ⚠ **E la media ARMONICA esisteva già, per il `cs`**

`:4774`: `cs_arco = 2·cs_i·cs_j / (cs_i + cs_j)`, col commento *«**collo di bottiglia causale:
media armonica, non media aritmetica**»*. **La mia tabella delle alternative la liquidava con
«vale per rate in serie, e l'arco non lo è»: era sbagliato**, perché il sistema la usa
esattamente per questo e la chiama col suo nome.
**Il sistema ha quindi DUE medie d'arco, ciascuna col suo dominio:** **aritmetica** per il
**tempo** (`dt_e`), **armonica** per la **velocità** (`cs_arco`). **Non se ne inventa una terza.**

---

## 2. IL GRADIENTE DI TEMPO PROPRIO — **su `r`, e la ragione è derivata**

**Oggi** (`:5189-5196`): `tau_nodo = 1 + mean(|tw|)/PHI_CRIT` per nodo, poi
`grad_tau = |tau_i − tau_j|`, poi `soglia = soglia0·(1 − 0.3·tanh(grad_tau))`.

**`tau_nodo` è IDENTICO al ramo `TEMPO_SEGNO` di `ritmo()` — quello che NON GIRA** *(`Z130`)*.
**La mitosi usa come «tempo proprio» la definizione di tempo che il resto del sistema ha
SCARTATO.** Sono **due orologi nello stesso passo**.

**Con la cura: `grad_r = |r_i − r_j|`.**

### **`r` o `1/r`? Si prende `r`, e NON è una preferenza**

`tau_nodo` oggi è una **lentezza** *(«tau_nodo alto = tempo lento», lo dice il commento)*, e
l'analogo diretto della lentezza è **`1/r`**. **Ma `1/r` È ILLIMITATO**, e il conto lo mostra:

| | intervallo | `tanh` del gradiente | la modulazione `1 − 0.3·tanh` |
|---|---|---|---|
| **`r`** | `[1.4142e-6, 1.4142]` | `tanh(grad) ≤ tanh(1.4142) = 0.8884` | **`[0.7335, 1]·soglia0` — MODULA** |
| `1/r` | `[0.707, 707107]` | `grad` fino a `~7e5` → **`tanh = 1` ESATTO** | **`0.7·soglia0` COSTANTE** |

> **Con `1/r` la modulazione diventa un RISCALAMENTO COSTANTE della soglia**, cioè **un
> parametro nascosto** *(`A1`)*, non una legge. **Con `r` resta una modulazione.**
> **`A11` cor.6: un limite che satura è un allarme** — e `1/r` lo farebbe saturare **sempre**.

---

## 3. IL RILASSAMENTO DI `_rep` — **`S12` APPROVATO DA LUCA**

**Oggi** (`:5280`): `self._rep += _dte * (rep − self._rep) / max(tau_pp, 1e-12)`.

**Tre difetti nella stessa riga, e il commento ne dichiara due:**

| | |
|---|---|
| **① la DILATAZIONE È CONTATA DUE VOLTE** | `_dte` **è già** `DT·0.5(r_i+r_j)`, cioè contiene già il tempo proprio; dividere **anche** per `tau_pp` la conta una seconda volta |
| **② `tau_pp` non è una durata** | è un numero puro *(un fattore di dilatazione)*. Una costante di tempo **deve avere le unità di un tempo** |
| **③ l'integratore è un EULERO ESPLICITO** | il commento dichiara *«`A5` livello 1, **rilassamento esponenziale**»*, e `par.4` impone la **forma esatta** |

### **LA DURATA, DERIVATA: `tau_arco = d / cs_arco`**

**È il ritardo causale dell'arco**, e **le due grandezze esistono già**:

| | | unità |
|---|---|---|
| `d` | la **lunghezza dell'arco**, `self.d` | `[LAM]` |
| `cs_arco` | la velocità d'onda d'arco, **media armonica** *(`:4774`)* | `[LAM/DT]` |
| **`tau_arco = d / cs_arco`** | **una DURATA** | **`[DT]`** ✅ |

**È la stessa legge che `FORK_SU2_MEM` usa per il ritardo dei Bloch** *(`tau = d/cs`,
`_tempo_luce_nodo`)*, **al livello dell'ARCO invece che del nodo** — e al livello dell'arco `d` e
`cs_arco` sono **direttamente disponibili**, senza la media sul grado che la versione nodale deve
fare. **Zero parametri nuovi, zero coefficienti.**

### **LA FORMA ESATTA**

```
_rep  <-  rep + (_rep - rep) * exp(-dt_e / tau_arco)
```

**L'esponente è `[DT]/[DT]` = numero puro.** È la stessa forma che `PEQ_ESATTO` (`C1`) ha imposto
a `peq` e che `par.4` impone a ogni rilassamento di primo ordine. **È una combinazione convessa**,
quindi `_rep` resta **fra `rep` e il suo valore precedente per QUALUNQUE passo**: non può
scavalcare, e il difetto che l'Eulero aveva su `peq` *(`dt/tau > 1` misurato `1.2018`)* **non può
ripresentarsi**.

### ⚠ **PRECISAZIONE 1 del guardiano: `cs_arco` NON È DISPONIBILE in `mitosi()`**

**È una LOCALE di `step()`** (`:4774`), **non un attributo.** Quindi `tau_arco = d/cs_arco` va
**ricostruito** dentro `mitosi()` da **`self._cs_nodo_prev`** — che è **classe `A8b`**, la stessa
di `_cs_nodo_prev` quando era **stale al `71.88 %`**.

**TRE conseguenze, tutte obbligatorie:**

#### ① **UNA SOLA FORMULA, non due copie**

Si **estrae una funzione** per la media armonica d'arco, e la chiamano **entrambi**: `step()`
(`:4774`) **e** `mitosi()`.

```
_cs_arco_da_nodo(cs_nodo, i, j)  =  2·cs_i·cs_j / max(cs_i + cs_j, 1e-12)
```

**È lo stesso argomento del docstring di `_tempo_luce_nodo`:** *«UNICO punto del file in cui
questa relazione è scritta … duplicarla avrebbe significato avere **due leggi che possono
divergere**»*. **Due copie della media armonica sarebbero due leggi.**

#### ② **LA GUARDIA SU `_cs_nodo_prev` SI CONTA** *(`A8`, quattro numeri)*

invocazioni · salti · **la forma** al fallimento *(le due lunghezze; `-1` = assente)* ·
**quando** *(l'indice dell'ultima saltata)*.

**Il fallback è `CS_M`**, e **non è una convenzione nuova**: è esattamente ciò che `step()` fa
già a `:4778` quando `CS_DINAMICO` è spento — `cs_arco = np.full(len(i), CS_M)`.

#### ③ **IL SIGILLO DEVE PROVARE CHE L'ESTRAZIONE NON CAMBIA `step()`**

**A flag SPENTO, `step()` deve restare byte-identico dopo l'estrazione della funzione.**
È la stessa prova che l'estrazione di `_tempo_luce_nodo` ha dovuto dare *(«senza cambiarne una
virgola»)*, e **non è ovvia**: un'estrazione può cambiare l'ordine delle operazioni in
virgola mobile.

### ⚠ **I CLAMP: uno SPARISCE, uno NASCE** *(`A11`)*

### ✅ **DECISIONE DI LUCA, 2026-09-24: NON SI SCRIVE NESSUN CLAMP. È UNA LEGGE.**

> ### **«La lunghezza degli archi non può scendere sotto la lunghezza tipica del sistema» è una
> ### LEGGE, non una garanzia che dipende da un flag.**

**Quindi in `CURA 2` `tau_arco = d / cs_arco` si scrive COSÌ, senza `np.maximum`.** Se uno dei
due fosse zero, **il livello NUMERICO di `C5` alza un'eccezione con la riga esatta**:
`np.seterr(over='raise', divide='raise', invalid='raise')` a **`:7382`**. **È `A11` fatto bene:
un limite che protegge da un errore si sostituisce con il RILEVAMENTO dell'errore.**

#### ① **`d ≥ LAM`: L'INVARIANTE ESISTE — MA È GATED SU UN FLAG, ed è il difetto**

`DOMINI['d'] = ('lam', …)` e `DOMINI['d0'] = ('lam', …)` **ci sono** (`:215-216`). Ma il
controllo, a **`:3702`**, è:

```python
_lam_attivo = SCALA_MIN or SCALA_MIN_PASSO        # :3657
…
if _lam_attivo:
    cattivo = ~fin | (vf < LAM * (1.0 - 1e-12));  regola = '>= LAM, con la scala minima accesa'
else:
    cattivo = ~fin | (vf <= 0.0);                 regola = '> 0 (scala minima SPENTA)'
```

> **Una LEGGE verificata solo quando un flag è acceso non è una legge: è un'opzione.**
> **→ va reso INCONDIZIONATO**, ed è la voce `E4-LAM` della coda: **non lo faccio in `CURA 2`**,
> perché cambierebbe il comportamento di una configurazione diversa da quella dei run *(a flag
> spenti, un `d < LAM` oggi passa e domani fermerebbe il run)*, **e quella è una decisione di
> Luca su `C5`, non un pezzo di questa cura.**
>
> **Per `CURA 2` non serve:** nei run `SCALA_MIN_PASSO` è **acceso**, quindi l'invariante
> controlla `d ≥ LAM` **davvero**, e **misurato**: `min(d) = 0.800000 = LAM` esatto, `0` archi
> sotto su `526302`.

#### ② **`cs` NON PUÒ ESSERE ZERO — derivato dal codice, non misurato**

```python
_scala      = max(_Lam, 1e-30) / GAMMA_TURBO**2
cs_floor    = CS_M / (1.0 + sqrt(_I) * sqrt(1.0/_scala))      # > 0: il denominatore e' >= 1
cs_floor    = min(cs_floor, CS_M)                             # quindi 0 < cs_floor <= CS_M
transizione = 0.5 * (1.0 + tanh(1.0 - u_nodo))                # in (0, 1) STRETTO
return        cs_floor + (CS_M - cs_floor) * transizione      # >= cs_floor > 0
```

**`cs ∈ (0, CS_M]` PER COSTRUZIONE**, e `cs_arco` è la **media armonica di due numeri
positivi**, dunque **positiva**. *(La misura concorda e non serve alla dimostrazione:
`min(cs) = 4.3465e-01`, **`0` zeri esatti** su `2660` nodi.)*

> **Quindi è un INVARIANTE, non un caso da contare** — e si aggiunge a `DOMINI`:
> `'_cs_nodo_prev': ('pos', …)`. **Legge soltanto: su un run sano non cambia un bit.**
> **Nel ramo `CS_DINAMICO` spento `cs_arco = CS_M` costante**, quindi positivo anche lì.

### ❌ **E RESTA LA MIA CORREZIONE SUL CONTO DEI CLAMP, perché il primo pezzo era giusto**

**Avevo scritto** che *«due clamp spariscono per costruzione»*. **Il secondo era falso**, e l'ho
visto controllando invece di assumere.

| clamp | prima | dopo | verdetto |
|---|---|---|---|
| `max(tau_pp, 1e-12)` | **È CODICE MORTO**: `tau_pp = 1 + |tw|/PHI_CRIT` con `|tw| ≥ 0`, quindi **`tau_pp ≥ 1` SEMPRE** e il clamp è **irraggiungibile** | esce dalla formula | **sparisce, e non proteggeva nulla** |
| `max(tau_arco, 1e-12)` | — | **NON SI SCRIVE** *(decisione di Luca)* | **`d ≥ LAM` è una legge e `cs > 0` è derivato: al posto del clamp c'è l'INVARIANTE** |

**Il primo pezzo resta vero e utile:** `max(tau_pp, 1e-12)` era **codice morto**, e accorgersene è il tipo di cosa che `A11` chiede. **Il secondo pezzo è caduto**: non nasce nessun clamp, perché `d ≥ LAM` è una **legge** e `cs > 0` è **derivato**.

**MISURATO nel giro di `CURA 1`** *(`SCALA_MIN = False`, **`SCALA_MIN_PASSO = True`**)*:

| | |
|---|--:|
| `LAM` | **`0.8`** |
| `min(d)` | **`0.800000`** — **esattamente `LAM`** |
| `min(d)/LAM` | **`1.0000`** |
| archi con `d < LAM` | **`0` su `526302`** |

> **Quindi nella configurazione dei run il clamp non morde — ma NON per costruzione: per via di
> un FLAG.** Si scrive il clamp, **si CONTA**, e si dichiara che la garanzia viene da
> `SCALA_MIN_PASSO`. **`A11`: un limite ammesso solo se esprime un vincolo dichiarato** — qui il
> vincolo è *«nessuna lunghezza sotto `LAM`»*, che è una legge del sistema, **non una
> protezione da un errore.** È legittimo **a condizione di dirlo.**
>
> **⚠ E IL CONTO DI PRIMA ERA SBAGLIATO PURE NEL NUMERO:** avevo scritto `min(d)/LAM = 2.0000`
> perché il mio script aveva `LAM = 0.4` cablato a mano invece di leggerlo. **`LAM` è `0.8`**, e
> il rapporto è **`1.0000`**. *(`P1-ter`: un numero ricopiato a mano non ha provenienza.)*

---

## 4. LA PROBABILITÀ DI MITOSI — **la forma di Poisson, e il clip sparisce**

**Oggi** (`:5244`): `prob = np.clip(resp, 0.0, 1.0)`. **Un clip `A11` su una probabilità.**

**Con la cura:**

```
prob = 1 - exp(-max(resp, 0))
```

**Perché è DERIVATA e non scelta:** `resp` è il **numero atteso di eventi** nel passo proprio
locale *(un tasso per unità di tempo di coordinata, moltiplicato per `dt_e/DT`)*, e la
probabilità di **almeno un evento** di un processo di Poisson con quel numero atteso è
`1 − e^{−λ}`. **Sta in `[0, 1)` per costruzione: il clip non ha più niente da tagliare.**

**E per ampiezze piccole coincide con la vecchia forma:** `1 − e^{−λ} = λ − λ²/2 + …`, quindi
**l'errore relativo è `λ/2`**: sotto `λ = 0.02` le due forme differiscono di meno dell'`1 %`.

### ⚠ **IL FATTORE DI TEMPO VA CONTATO UNA VOLTA SOLA**

`tau_locale` **non si sostituisce con `dt_e/DT` lasciando poi un secondo `dt_e/DT`
nell'esponente**: sarebbe **la dilatazione contata due volte**, lo stesso difetto del par.3 ①.
**Il fattore compare UNA volta**, dentro `ampiezza`:

```
ampiezza = salita * discesa * (dt_e / DT)        # numero atteso di eventi
resp     = ampiezza * segno
prob     = 1 - exp(-max(resp, 0))
```

### ✅ **E LA SOSTITUZIONE TOGLIE UN DOPPIO CONTO DELLA TORSIONE**

`tau_locale = 1/(1 + |tw|/PHI_CRIT)` **decresce con la torsione**. Ma `discesa =
clip(1 − |tw|/TW_TETTO, 0, 1)` **fa già esattamente questo**, e va a zero al tetto.
**Quindi oggi la soppressione ad alta torsione è contata DUE VOLTE**, una in `discesa` e una in
`tau_locale`. **Con `dt_e/DT` resta contata una volta**, in `discesa`, dove la legge la
dichiara — e il fattore di tempo fa il mestiere del tempo.

---

## 5. ✅ **PRECISAZIONE 2 del guardiano: SÌ, È UN DOPPIO CONTEGGIO. LO CORREGGO.**

**La domanda:** con la cura, il ritmo `dt_e/DT` entrerebbe **due volte** nel ramo repulsivo —
nel **bersaglio** `rep` *(via `ampiezza`)* e nella **velocità del rilassamento** *(via `dt_e`
nell'esponente)*.

### **LA RAGIONE, in una riga, e dice CORREGGI**

> **Un'INTENSITÀ D'EQUILIBRIO non può dipendere dalla DURATA del passo: se dipendesse, la
> stessa condizione fisica darebbe un equilibrio diverso a seconda di quanto batte l'orologio
> locale. Una PROBABILITÀ PER PASSO, invece, DEVE dipenderne.**

**`rep` è il BERSAGLIO di un rilassamento**, cioè il valore verso cui `_rep` tende: è un
**equilibrio**. **`prob` è una probabilità nel passo**: è un **conteggio**. Sono due tipi
diversi, e il tempo entra **solo nel secondo**.

### **LA CAMPANA SI LEGGE DUE VOLTE, e ciascuna lettura ha le SUE unità**

```
ampiezza_int = salita * discesa                    # INTENSITA'   [numero puro]
ampiezza_ev  = ampiezza_int * (dt_e / DT)          # EVENTI ATTESI [numero puro]

resp_int = ampiezza_int * segno                    # -> il BERSAGLIO
resp_ev  = ampiezza_ev  * segno                    # -> la PROBABILITA'

rep   = clip(-resp_int, 0, 1)                      # equilibrio: SENZA tempo
prob  = 1 - exp(-max(resp_ev, 0))                  # per passo:  CON il tempo
_rep <- rep + (_rep - rep) * exp(-dt_e / tau_arco) # il tempo entra QUI, nella VELOCITA'
```

**Il tempo compare UNA volta per ciascuna grandezza, e mai due nella stessa.**

> ### ✅ **E COSÌ LA CURA CHIUDE UN DIFETTO CHE NÉ IO NÉ IL MANDATO AVEVAMO NOMINATO**
> **Oggi** `ampiezza = salita·discesa·(1/tau_pp)` **e `rep = clip(−ampiezza·segno, 0, 1)`**:
> quindi **l'equilibrio della repulsione dipende GIÀ da un fattore che il commento chiama
> «ritmo»**. Ed è la **terza** dipendenza da `|tw|` nello stesso bersaglio, dopo `salita` e
> `discesa`. **Togliendo il fattore di tempo restano le due che sono la legge** — attivazione
> sopra soglia, spegnimento al tetto — **e l'equilibrio smette di dipendere dall'orologio.**

### ⚠ **E IL CLIP SU `rep` RESTA, perché È RAGGIUNGIBILE — VERIFICATO, non assunto**

Avevo pensato di sostituirlo con `tanh` *(la normalizzazione che `COES_ADIM` usa per una
magnitudine)*, o di dichiararlo inerte perché il suo lato superiore è inarrivabile.
**Ho controllato, e NON è inarrivabile:**

| | |
|---|---|
| `satura(f) = f/(1 + GAMMA·|f|)` | → **`1/GAMMA`** per `f → ∞` |
| **`GAMMA = 0.05`** *(letto dal sorgente e dal referto di configurazione)* | → **`salita < 20`** |
| quindi `|resp_int| < 20` | **il clip a `1` MORDE**, e non di poco |

> **Quindi il clip resta in questa cura, e la sua sostituzione si DECIDE SU UNA MISURA, non su
> un'opinione:** `tanh` e il clip **coincidono dove il clip non morde** e differiscono solo dove
> mordeva. **Si conta quante volte morde** — è il criterio `K`, esteso da `prob` anche a `rep`.
> **Se non morde mai, la sostituzione è sicura; se morde, cambia la fisica e la decisione è di
> Luca.** *(`A12` regola 4: dichiarato, non deciso.)*

## 6. LA TABELLA DELLE UNITÀ

| grandezza | **prima** | **dopo** | nota |
|---|---|---|---|
| `DT` | tempo di coordinata | — | l'unità di tempo |
| `r` | numero puro | — | `dt_n = DT·r` |
| `dt_e` | `[DT]` | — | `DT·0.5(r_i+r_j)`, `:4352` |
| `dt_e/DT` | — | **numero puro** | il fattore di tempo proprio d'arco |
| `avv = |tw|` | `[rad]` | — | torsione |
| `soglia` | `[rad]` | `[rad]` | modulata da `grad_r`, non da `grad_tau` |
| `ecc = avv/soglia − 1` | numero puro | — | rapporto di due angoli |
| `salita`, `discesa` | numero puro | — | |
| `tau_locale` | numero puro *(ma **era** un reciproco di torsione)* | **`dt_e/DT`** | **ora è un tempo, come il nome dice** |
| `ampiezza` | numero puro **(con un fattore di tempo travestito)** | **si SDOPPIA** | vedi le due righe sotto |
| **`ampiezza_int`** | — | **numero puro** | `salita·discesa`: **INTENSITÀ**, senza tempo. Va al **bersaglio** `rep` |
| **`ampiezza_ev`** | — | **numero puro** | `ampiezza_int·(dt_e/DT)`: **eventi attesi**, col tempo. Va a `prob` |
| `segno` | numero puro `(−1, 1)` | — | resta |
| `resp` | numero puro | **si SDOPPIA in `resp_int` e `resp_ev`** | uno per il bersaglio, uno per la probabilita' |
| `rep` | numero puro **con clip**, e **col fattore di tempo** | numero puro **con clip**, **SENZA** il fattore di tempo | e' un **equilibrio**: non deve dipendere dalla durata del passo |
| `prob` | numero puro **con clip** | numero puro **in `[0,1)` per costruzione** | il clip sparisce |
| `tau_pp` | numero puro, **usato come TEMPO** | **esce dagli usi TEMPO** | resta solo come coordinata di torsione |
| **`tau_arco`** | — | **`[DT]`** | `d/cs_arco`: **una durata vera** |
| `_rep` | numero puro | — | rilassa in forma **esatta** |
| `grad_tau` → `grad_r` | `[rad]`/PHI_CRIT | **numero puro** | gradiente di un **ritmo** |

**Nessuna grandezza con unità diverse viene sommata o confrontata**: gli unici confronti sono
`avv` con `soglia` *(entrambi `[rad]`)* e `tau_pp` con `centro` *(entrambi numeri puri sull'asse
di torsione)*.

---

## 7. LA PROVENIENZA DI `r` DENTRO `mitosi()`, e la guardia

`r` per nodo è in `self._r_corrente`, scritto in `step()` a `:4397` **ma solo
`if FORK_SU2_MEM`**.

| questione | risposta, **dal codice** |
|---|---|
| è disponibile? | **sì**: il ciclo è `step(); mitosi(); …`, quindi `mitosi()` segue **immediatamente** |
| la lunghezza è giusta? | **sì in quel punto** — `n` non è ancora cresciuto. Ma è un array **per-nodo attraversato da un punto di crescita**: la classe `A8b` di `_cs_nodo_prev` *(`71.88 %`)* e `_psi_spin_prec` *(`95.33 %`)* |
| se `FORK_SU2_MEM` è spento? | `_r_corrente` è `None`. **Dipendenza DICHIARATA**: nei run del fork è acceso |
| indici d'arco `≥ n`? | il codice si guarda già *(`self.i[self.i < self.n]`, `:5190-5192`)*: si fa lo stesso, **e si conta** |

**LA GUARDIA SI CONTA, NON SI TACE** *(`A8`)*: **quattro** numeri — invocazioni, salti, **la
forma** al fallimento *(le due lunghezze)*, e **quando** *(l'indice dell'ultima saltata)*.
Il fallback è **`dt_e/DT = 1`**, cioè *«nessuna dilatazione»*: la stessa convenzione che
`ritmo()` usa quando non c'è un passato *(`np.ones`)*, **non una convenzione nuova**.

---

## 8. COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **se il clip su `rep` si possa sostituire con `tanh`** *(par.5)*: **non è una questione di principio ma di MISURA** — le due forme coincidono dove il clip non morde, e `GAMMA = 0.05` dice che **può mordere** *(`salita < 20`)*. **Il criterio `K` lo conta**, e poi decide Luca;
2. **il `0.3`** della modulazione della soglia: era un numero scelto **prima** della cura, e la
   cura non lo migliora né lo peggiora — **ne cambia la scala dell'argomento**, e il conto del
   par.2 dice di quanto *(`tanh ≤ 0.8884` invece di `→ 1`)*;
3. **il `3.0`** dentro `tanh(3.0·(tau_pp − centro))`: resta `TORSIONE`, resta com'è, **è un
   numero scelto** e la scheda lo deve dire;
4. **che il tasso di mitosi resti dello stesso ordine.** `1/tau_pp ∈ (0,1]` con mediana vicina a
   `1`; `dt_e/DT` ha **mediana misurata `≈ 0.68`** *(`Z135`)*. **Il tasso può calare di ~`1/3`**,
   e **`E1a` è il suo giudice**. *(Non metto un fattore di normalizzazione: sarebbe un numero
   scelto.)*

---

## 9. I CRITERI DELLA PROVA, fissati qui

| | criterio | origine |
|---|---|---|
| **`E1a`** | la mitosi **non muore**: nascite `> 0` e eventi **dello stesso ordine** del riferimento | di Luca. `FASE_2PI` è caduta qui *(`62` → `1` evento)* |
| **`E1b`** | **non esplode**: `n` finale `< 10×` il riferimento | **misurata**: `178` archi per nodo |
| **`B`** | il **bilancio di `d0` CHIUDE** | il criterio di `G4` |
| **`K`** | **quante volte il clip avrebbe morso**, su `prob` **E su `rep`** | richiesta di Luca, **estesa a `rep`**: dice **quanto la forma nuova differisce dalla vecchia**. Se su `prob` è `0`, la cura di `:5244` è **formale**. **Su `rep` decide se il clip si può sostituire con `tanh`**, e quella decisione è di Luca |
| **`H`** | **la guardia di `_cs_nodo_prev`**: invocazioni, salti, forma, quando | `A8`. Era **stale al `71.88 %`** in passato: se salta, `tau_arco` cade su `CS_M` e **il rilassamento non è quello dichiarato** |
| **`G`** | **dove nasce la materia rispetto al gradiente di `r`** | richiesta di Luca. **Si RIPORTA**, non si giudica |
| **`R`** | **`d0` e `d/d0` con i QUANTILI (`p10`, mediana, `p90`) e la divisione VUOTO / CONFINE / MASSA**, più il **TERMINE DELLA REPULSIONE nel bilancio**, contro `_cura1_corto` | **richiesta di Luca, 2026-09-24**, e la previsione è **sua e derivata**: togliere il fattore di tempo dal bersaglio di `rep` **ALZA l'equilibrio della repulsione**, che **allarga `d0`**. **Quanto:** il bersaglio viene moltiplicato per `tau_pp = 1 + |tw|/PHI_CRIT`, e nel regime repulsivo `tau_pp > centro = 2.5`, quindi **circa ×2.5-×3**. **Si RIPORTA il verso e l'ampiezza**, e se `d0` si allarga **non è una sorpresa: è la previsione**. **⚠ E LA MEDIANA DA SOLA NON BASTA — rilievo di Luca, 2026-09-24:** *«la mediana è un riassunto GLOBALE di un rapporto LOCALE: può nascondere compressione e stiramento che si COMPENSANO»*. Quindi **`p10`, mediana, `p90`** e la **divisione per classe d'arco**, con la **stessa convenzione di `G1`-`G2`** *(`csv/_test_fork/_dove_spinge_la_gravita.py:72-78`: nodo `< 900` = **VUOTO**, `< 2391` = **MASSA seminata**, oltre = **NATO**; l'arco prende la coppia delle due classi)* — **non una convenzione nuova**. **E `A2` vale: statistiche globali SOLO nel referto, MAI nella legge.** La legge tocca `ampiezza_int`, `ampiezza_ev`, `rep`, `prob`, `_rep`, `grad_r`: **nessuna di queste legge una statistica globale.** |
| **`C`** | la **guardia** di `_r_corrente`: quante volte salta, e **quando** | `A8`. Se salta **fuori dal transitorio**, il referto **non si legge** |
| **`V8`/`V9`** | **la distribuzione di `\|dx\|/d`** — `p50`/`p90`/`p99`/`p99.9`, `max`, e la quota `> 0.5`, `> 1`, `> 2` — **separata per SALITE e DISCESE** | **decisione di Luca, 2026-09-24: SENZA UN RUN IN PIÙ.** L'involucro del bilancio avvolge già `_smorza` e vede ogni `(dx, prima)`: il numero che sceglie fra `piana` e `tanh` *(scheda ⑪)* **si raccoglie qui dentro**. Criterio committato **prima** in `2c4da47` |

**Riferimento: `csv/_test_fork/_cura1_corto`** — stessa configurazione, `CURA 1` accesa, questo
flag **spento**. **Differisce per UN interruttore.**

---

## 10. IL CODICE, COM'È STATO SCRITTO — *2026-09-24, blob `b881db89`*

### 10.1 QUATTRO METODI NUOVI, e ciascuno esiste per non avere DUE leggi

| metodo | cosa fa | perché è un metodo e non una riga |
|---|---|---|
| **`_cs_arco_da_nodo`** | media **armonica** del `cs` sui due estremi | **ESTRATTA da `step()` `:4791` senza cambiarne una virgola.** `mitosi()` ne ha bisogno per `tau_arco = d/cs_arco`; **duplicarla avrebbe significato due leggi che possono divergere** — lo stesso argomento del docstring di `_tempo_luce_nodo`. **`T4` prova che l'estrazione non ha cambiato un bit** |
| **`_r_nodo_mitosi`** | l'orologio **per nodo**, per il gradiente | guardia **contata `A8`**: invocazioni, salti, **forma** al fallimento, **quando** |
| **`_fattore_tempo_arco`** | `dt_e/DT` per arco | **LETTO da `_dt_e_ultimo`, NON ricalcolato.** Ricalcolarlo sarebbe **una seconda formula per lo stesso tempo** |
| **`_tau_arco_causale`** | `d / cs_arco`, e **ha le unità di un TEMPO** | `[LAM]/[LAM/DT] = [DT]`. **NESSUN CLAMP**, ed è una decisione di Luca: `d ≥ LAM` è una **LEGGE** *(`E4-LAM`)* e `cs > 0` è **derivato** |

### 10.2 LE QUATTRO MODIFICHE GATED, tutte dentro `mitosi()`

```
:5297   grad_tau   da |tw| per nodo  ->  da r per nodo  (_r_nodo_mitosi)
:5370   ampiezza   * 1/tau_pp        ->  * dt_e/DT      (_fattore_tempo_arco)
        prob       clip(resp,0,1)    ->  1 - exp(-max(resp,0))     [Poisson]
:5387   rep        bersaglio da resp ->  da resp_int (SENZA il tempo)
:5438   _rep       Eulero con tau_pp ->  forma ESATTA con tau_arco  [S12]
```

> **⚠ E IL FATTORE DI TEMPO ENTRA UNA VOLTA SOLA, non due — è il rilievo di Luca del `e11602d`.**
> `rep` è il **BERSAGLIO di un rilassamento**, cioè un **EQUILIBRIO**: non può dipendere dalla
> **durata** del passo, senno' la stessa condizione fisica darebbe un equilibrio diverso a
> seconda di quanto batte l'orologio locale. `prob` è una **probabilità NEL passo**, cioè un
> **conteggio**: **deve** dipenderne. Per questo esistono `ampiezza_int` *(senza tempo)* e
> `ampiezza` *(con)*, e il bersaglio legge la prima.

### 10.2-bis ⚠ **I QUATTRO METODI SONO LEGGI, E `REG-R` LO HA PRETESO**

Il primo tentativo di commit è stato **RIFIUTATO**: *«queste leggi non hanno una scheda»*, e
le elencava tutte e quattro. **Aveva ragione, e non era una formalità** — sono quattro
relazioni fisiche *(una media d'arco, un orologio per nodo, un fattore di tempo, un ritardo
causale)*, e senza scheda si curerebbe alla cieca. **Sono entrate nel marcatore di questa
scheda**, che è dove la loro legge è scritta.

> **⚠ E UNA TENSIONE VA DICHIARATA, non nascosta: `_cs_arco_da_nodo` NON È SOLO DI QUESTA
> SCHEDA.** La chiama anche `step()`, che appartiene alla ⑥, e la relazione vive in `step()`
> **da prima della cura**. Sta qui perché **qui è stata scritta la sua derivazione**
> *(armonica perché è un collo di bottiglia; aritmetica per il tempo, armonica per la
> velocità)*. **È lo stesso caso della ⑥ che rivendica `step` «in via provvisoria», con lo
> stesso rimedio: quando `step` avrà la sua scheda, il marcatore si divide.** Finché non
> succede, **una modifica a questa media obbliga a toccare la ⑨ e non la ⑥**, e chi la cerca
> partendo da `step()` deve passare dal rimando che la ⑥ ora porta.

### 10.2-ter ⚠ **IL CLIP HA DUE LATI, E NE CONTAVO UNO SOLO** — *rilievo di Luca, 2026-09-24*

`np.clip(resp, 0, 1)` taglia **in alto** *(contato: `_tum_clip_prob` = **`0` su `63 148 047`**)*
**e in basso**. **Il lato basso morde ogni volta che `resp <= 0`, cioè su TUTTO il regime
repulsivo** — e dire *«il clip non morde»* con in mano solo il lato alto **sarebbe falso**.

Aggiunto **`_tum_clip0_prob`**, incondizionato come gli altri.

> **E dice una cosa precisa sulla cura: la forma di Poisson `1 − exp(−max(resp, 0))` CONSERVA il
> taglio in basso.** È il taglio **in alto** che sparisce. Quindi `_tum_clip0_prob` misura
> **quanto è grande il pezzo di dominio su cui le due forme COINCIDONO ESATTAMENTE** *(entrambe
> danno `0`)*. **Più è grande, più la cura di `:5244` è formale.**

### 10.3 I CONTATORI `A8`, e girano **ANCHE A FLAG SPENTO**

`_tum_clip_prob*`, `_tum_clip_rep*`, `_tum_eulero_gt1`/`_tot` sono **fuori dal gate**, di
proposito: così **il «prima» del criterio `K` arriva dal giro di byte-inerzia del sigillo,
senza un run in più**. Sono l'unica ragione per cui `T4` riporta dei campi *«non confrontati»*
invece di zero.

---

<!-- SCHEDA nome=nascita-archi funzioni=_allaccia,_nasce,semina,_semina_lam,_celle_vive flag=SEMINA_LAM,NASCITA_LAM,SCALA_MIN,SCALA_MIN_PASSO,LAM -->

# ⑫ LA NASCITA DEGLI ARCHI — **la cura della semina** *(`D38`, decisione `D-b` di Luca)*

> **Decisione di Luca, 2026-09-24:** *«Non deve nascere un arco sotto `LAM`. Il troncone
> `_nasce` resta come PRESIDIO.»*
> **NESSUN CODICE in questa scheda.** Difetto e criteri **prima**, cura **dopo**.
>
> ## ❌ **`NASCITA_LAM` È RITIRATA — decisione di Luca, 2026-09-24**
>
> **La prima cura che avevo proposto era `keep &= (dd >= LAM)`: FILTRARE GLI ARCHI.**
> **È ritirata**, e il motivo è **il criterio che avevo scritto io stesso** nel par.2 di questa
> scheda: *«se la mediana della distanza al primo vicino è sotto `LAM`, il difetto è nelle
> POSIZIONI, e nessun aggiustamento sugli ARCHI può curarlo»*.
>
> ### **Filtrare gli archi lascia i NODI a `0.135·LAM` l'uno dall'altro.** Toglie il sintomo
> ### *(`d < LAM`)* e lascia la violazione *(`|pos_i − pos_j| < LAM`)*. **Con `A13` non è
> ### nemmeno una mezza cura: è la cura di un'altra cosa.**
>
> **NON si cancella** *(par.10: il codice di una legge esclusa non si cancella mai)*: resta qui,
> **come il perché esiste `SEMINA_LAM`.**

## 1. IL DIFETTO — **`D38`**

`_allaccia` prende la lunghezza dell'arco dal `cKDTree`:

```python
M = Tn.sparse_distance_matrix(T, rc, output_type="coo_matrix")
a, b, dd = M.row + base, M.col, M.data          # dd = la distanza EUCLIDEA VERA fra `pos`
...
dd = self._nasce(dd)                            # [SCALA_MIN] il troncone parte da LAM
```

e `_nasce` *(`:3845-3853`)* è:

```python
if not (SCALA_MIN or SCALA_MIN_PASSO):
    return v
return np.maximum(v, LAM)
```

> ### ❗ **LA LEGGE `d >= LAM` È VERIFICATA SEMPRE (`E4-LAM`) MA FATTA RISPETTARE ALLA NASCITA
> ### DA UN'OPZIONE.** È **lo schema che `E4-LAM` ha tolto al CONTROLLO e che è rimasto
> ### all'ESECUZIONE.** Coi **default del sorgente** la legge è **violata al passo zero**.

## 2. LA CAUSA — **non è negli ARCHI: è nelle POSIZIONI**

*(`csv/_test_fork/_geometria_semina.py`, blob `49fc54d2`, passo ZERO, `--scala-min-passo=off`
per avere la `d` GREZZA — col ramo acceso la domanda risponderebbe sempre zero.)*

**Distanza al PRIMO VICINO di ogni nodo** *(la più corta che quel nodo può avere)*:

```
n=2391  LAM=0.800000  R_CONN=2.400000
p01=0.022187  p10=0.049003  p50=0.107721  p90=0.473825  p99=0.676303
min=0.009679  max=0.814763
sotto_LAM = 2390 su 2391 (99.96 %)   mediana/LAM = 0.134651   min/LAM = 0.012098
```

> ### ❗ **IL `99.96 %` DEI NODI HA IL PRIMO VICINO SOTTO `LAM`, e la mediana è `0.135·LAM`:
> ### LA SEMINA METTE I NODI ~`7.4` VOLTE PIÙ FITTI DELLA LUNGHEZZA TIPICA DEL SISTEMA.**
>
> **Quindi `_nasce` non «corregge» `d`: LA SCOLLEGA DA `pos`.** Per il `42.47 %` degli archi,
> dopo il troncone **`d ≠ |pos_i − pos_j|`**. **È `D02` FATTO A MANO** — la distanza e il
> disegno divergono **per costruzione**, e divergono **al passo zero**.

**Sugli archi:** `223 380` su `525 973` — il **`42.47 %`** — nascono sotto `LAM`.

## 3. ❗ IL NUMERO CHE RENDE LA CURA POSSIBILE

```
SE_TAGLIASSI  archi_rimasti = 302593 su 525973 (57.53 %)
SE_TAGLIASSI  nodi_isolati  = 0 su 2391 (0.00 %)
```

> ### **NON CREARE gli archi sotto `LAM` costa il `42.47 %` degli archi e ZERO NODI ISOLATI.**
> **Era la domanda che poteva uccidere la cura, ed è misurata prima di proporla:** un nodo
> isolato **non è un nodo più semplice, è un nodo che esce dalla fisica**. **Non ce n'è
> nessuno**, perché `R_CONN = 3·LAM` lascia un anello `[LAM, 3·LAM]` pieno di vicini.

## 4. LA CURA — **`SEMINA_LAM`, spenta di default. UN INTERRUTTORE SOLO.**

**`A13` dice che sotto `LAM` non esiste niente, nemmeno una distanza fra nodi.** Quindi la cura
non sta sugli archi: **sta dove i nodi vengono messi.**

```
in `semina()`:  ogni nodo nuovo a distanza >= LAM da QUALUNQUE nodo GIA' PRESENTE
                -- della stessa massa, delle altre masse, del VUOTO DI FONDO --
                con semina casuale e SCARTO (RSA, random sequential adsorption)
```

**E il vuoto di fondo segue la stessa regola:** *non ci sono nodi di seconda classe.*

> ### PERCHÉ È DERIVATA E NON SCELTA *(par.3, zero manopole)*
> **`LAM` c'è già** ed è l'assioma; **`R_CONN = 3·LAM` c'è già**. **La cura non introduce
> nessun numero.** L'`RSA` non ha parametri: propone un punto, lo accetta se rispetta `LAM`,
> altrimenti lo scarta.

### ❗ E SE `n` NON ENTRA NEL RAGGIO, **LA SEMINA RIFIUTA** *(`A9`)*

> **NIENTE RIDUZIONI SILENZIOSE.** Se in quel raggio non stanno `n` nodi a distanza `LAM`, la
> semina **si ferma** con un messaggio che **nomina `n`, il raggio e il massimo possibile**.
> **È la ragione per cui questo è un presidio e non una nota:** una semina che «fa del suo
> meglio» consegnerebbe **una massa più piccola di quella chiesta, in silenzio**, e ogni
> misura successiva sarebbe su una taglia diversa da quella scritta nel comando.
>
> **La SCENA calcola il raggio da `n`** *(decisione di Luca)*: è la scena a sapere quanto spazio
> serve, non la semina a stringersi.

### E `_nasce` RESTA — **come PRESIDIO, e ora agisce SEMPRE**

`D38` *(il troncone sotto flag)* **si cura qui**: il presidio **non è più gated**.
Dopo la cura **non deve scattare mai**, e **`_g_sm_nascite` è la sua misura**: se sale, un arco
è nato sotto `LAM` **da un'altra strada**.

> **⚠ E LE ALTRE STRADE ESISTONO:** la **mitosi** crea nodi vicino al genitore, e questa scheda
> **non la copre**. **`S4` lo RILEVEREBBE al passo zero, non nei passi dopo.** → in coda.

## 5. I CRITERI DELLA PROVA, **fissati QUI, PRIMA DEL CODICE** *(mandato di Luca)*

| | criterio | origine |
|---|---|---|
| **`S1`** | **flag SPENTO = byte-identico**: **firma dei byte** su tutti i campi, **un processo per braccio** | par.2.1 · `STANDARD 1` · `STANDARD 2` |
| **`S2`** | **passo ZERO: `min` distanza fra POSIZIONI `>= LAM`** *(`cKDTree`, `k=2`)* | ❗ **è `A13` misurato direttamente**, e **è il criterio che `NASCITA_LAM` non poteva soddisfare** |
| **`S3`** | **passo ZERO: `sum(d < LAM) == 0` E `sum(d == LAM) == 0`** | **i due INSIEME**: il primo da solo lo darebbe anche `_nasce`. **Lo zero sul secondo distingue «non c'è bisogno di troncare» da «troncato»** |
| **`S4`** | **`_g_sm_nascite == 0`** al passo zero | il presidio **non deve scattare**. **Rileva solo il passo zero**, non i passi dopo |
| **`S5`** | **nodi isolati `== 0`** | un nodo isolato **non è un nodo più semplice: è un nodo che esce dalla fisica** |
| **`S6`** | **`d == |pos_i − pos_j|` per OGNI arco al passo zero** | ❗ dice se la cura ha curato **`D02` a questo sito**: oggi diverge sul `42.47 %` |
| **`S7`** | **giro corto di 120 passi**: la mitosi **viva**, il **bilancio di `d0` CHIUDE** | `E1a` e `B`, gli stessi di `CURA 1` e `CURA 2`. ❗ **è il solo che può BOCCIARE la cura** |

### ✅ **LA STRADA è `(ii)`: MASSA = REGIONE A FASE COERENTE NEL VUOTO** *(Luca, 2026-09-25)*

```
un vuoto UNICO seminato con SEMINA_LAM (saturazione esatta) su una palla che
contiene le tre regioni.
LE MASSE NON AGGIUNGONO NODI: sono i nodi del vuoto DENTRO TRE SFERE, a cui si
assegna la STESSA FASE (fase della scena + il rumore che `semina()` usa gia').
Fuori: fasi casuali, come oggi. Coorti registrate come oggi (`massa_k`).
```

> ### **ZERO NUMERI NUOVI, e per una ragione che vale più dell'economia:** la materia **era
> ### già** uno **STATO del nodo** nel codice — `I > Λ`, *«sotto `Λ` sei vuoto, sopra sei
> ### materia»* *(voce `M1` della coda)*. **La strada `(ii)` non aggiunge un'ontologia: rende
> ### la SCENA coerente con quella che il simulatore ha già.**
>
> **E risolve il vincolo che uccideva `(i)`:** con `A13` una massa **non può essere più densa
> del vuoto** — stessa distanza minima per tutti — quindi *«aggiungere nodi»* dentro un vuoto
> saturo **è impossibile per costruzione**. Se la massa non aggiunge nodi, il problema non
> esiste.

### LA GEOMETRIA, e cosa è SCELTO

```
tre regioni su un cerchio di raggio `sep` -> distanza fra i CENTRI = sep*sqrt(3) (corda 120')
intervallo fra i BORDI = sep*sqrt(3) - 2*r      ** = R_CONN e' una SCELTA di Luca **
raggio del VUOTO = sep + r + R_CONN            <- il minimo che contiene le tre regioni
                                                  PIU' un guscio di R_CONN
```

**I numeri si calcolano con la semina VERA** *(`csv/_test_fork/_scene_coerenti.py`)*, **non si
stimano**, e si committano **prima** della misura.

### I DUE CRITERI IN PIÙ — **`S9` e `S10`**, fissati PRIMA *(Luca, 2026-09-25)*

| | criterio | perché |
|---|---|---|
| **`S9`** | **al passo ZERO: intensità media DENTRO le regioni / quella del vuoto, `> 1`** — e **si riporta il valore** | ❗ **È IL CRITERIO CHE DECIDE SE LA STRADA `(ii)` ESISTE.** Se le regioni non sono **materia per il codice**, allora «massa = fase coerente» è una parola, non una scena. **E non basta «esiste un effetto»: il valore va detto**, perché `1.01` e `10` sono due fisiche diverse |
| **`S10`** | **le regioni restano coerenti**: frazione di nodi della coorte con `I > Λ`, ai passi `0`, `30`, `60`, `120` | ❗ **SE CROLLA È UN RISULTATO, NON UN DIFETTO** *(Luca)*: direbbe che **la coerenza da sola non tiene la materia**. **Reperto e stop.** È il solo criterio di questa scheda che può dire qualcosa sulla FISICA invece che sul codice |

> **⚠ E `S10` HA UN NULLO CHE VA DETTO ORA** *(presidio del valore sotto ipotesi nulla)*:
> **fuori dalle regioni le fasi sono casuali**, quindi la frazione con `I > Λ` nel VUOTO non è
> zero — `Λ` è la **media** di `I`, quindi per costruzione **circa metà dei nodi** ci sta
> sopra. **Il numero che conta è il CONTRASTO fra coorte e vuoto, non il valore assoluto**, e
> il referto deve riportare **entrambi**.

### ✅ **LA SCENA `(a)` SI CHIAMA «STESSO RAGGIO», NON «STESSA MATERIA»** *(Luca, 2026-09-25)*

**Si tiene il RAGGIO `4.0964`**, cioe' **`~411` nodi per regione**, non `497`.

> ### **E LA RAGIONE È PIÙ FORTE DELLA SCELTA: i `497` per massa di `CURA 2` ERANO SOTTO LA
> ### SCALA DI PLANCK.** Stavano in un raggio `0.7 = 0.875·LAM`, dove ci stanno **`5`** nodi
> *(rapporto `104`)*. **Non c'è una «stessa materia» da conservare: quella materia non
> esisteva.** Conservare `497` sarebbe **portare avanti un numero nato in un regime che `A13`
> ha dichiarato inesistente.**
>
> **Il nome cambia perche' il nome era una PROMESSA sbagliata**, ed è lo stesso difetto dei
> commenti scaduti: *«stessa materia»* avrebbe fatto leggere il confronto come se una
> grandezza fosse tenuta fissa, mentre quella grandezza **non ha un valore precedente valido**.

**La scena `(b)` resta com'è:** `sep = 4.0`, `r_regione = 2.2641`, `~70` nodi per regione.

### ❗ `P-GONFIA` — **IL RIFERIMENTO CAMBIA, E VA DICHIARATO** *(Luca, 2026-09-25)*

**Il confronto con `CURA 2` è fra SCENE DIVERSE e non attribuisce niente alla semina.**
*(Scena diversa, `n` diverso, raggio diverso, `QUOTA` diversa: qualunque differenza di `d0`
potrebbe venire da lì.)*

```
BRACCIO DI CONTROLLO DI `P-GONFIA`:
  la STESSA scena (ii) -- stesso raggio del vuoto, stesso `n`, stesse regioni,
  stesso seme -- con `SEMINA_LAM` **SPENTA**.
  UNICA DIFFERENZA: la distanza minima.
```

> **La soglia resta «MENO DELLA METÀ»**, ma **applicata a QUESTO confronto**.
> **Il confronto con `CURA 2` resta nel referto come riferimento DI UN'ALTRA SCENA**, e va
> letto così: dice **dove siamo**, non **cosa ha fatto la semina**.

### ❗ `S10` — **TRE PRECISAZIONI PRIMA DELLA MISURA** *(Luca, 2026-09-25)*

1. **BRACCIO DI CONTROLLO:** la stessa scena, **stesso seme**, con **fasi CASUALI anche dentro
   le tre regioni**. **`S10` si legge come CONTRASTO fra la coorte coerente e questo controllo,
   non in assoluto.** *(Senza, il `~50 %` che `Λ` dà per costruzione si leggerebbe come mezzo
   successo.)*
2. **PROFILO PER GUSCI**, contati **in ARCHI dal nucleo della regione** *(non da `pos`)*:
   frazione con `I > Λ` ai passi `0`, `30`, `60`, `120`.
   **Distingue l'EROSIONE DAL BORDO dallo SFASAMENTO GLOBALE** — due esiti che un numero unico
   confonderebbe.
3. **PREVISIONE, scritta prima:** la scena **`(b)` perde coerenza PRIMA della `(a)`**.
   `r = 2.26 < R_CONN = 2.4`, quindi **nessun nodo della regione `(b)` ha tutti i vicini
   dentro**; in `(a)` *(`r = 4.10`)* il nucleo interno di raggio `~1.70` **ce li ha tutti**.
   **Se accade il contrario, va spiegato.**

> ### ⛔ **E SE LA COERENZA CROLLA: REPERTO E STOP. NESSUNA LEGGE NUOVA PER TENERLA** *(Luca)*.
> **La diagnosi si fa DOPO, spegnendo UNA legge alla volta** — dispersione delle frequenze,
> calci di fase della mitosi, torsione.
> **È `A12` applicato al contrario:** una misura che fallisce **non autorizza una legge**, e
> aggiungere un meccanismo per salvare un risultato è il modo in cui una teoria smette di
> poter essere smentita.

### ❗ LE PREVISIONI ANALITICHE, **committate PRIMA del giro** *(punto 4 del mandato)*

| | grandezza | `CURA 2` | scena `(ii)` | `×` |
|---|---|--:|--:|--:|
| **`P1`** | somma dei pesi per nodo | `~50` | `~9` | `0.18` |
| **`P2`** | contrasto `I_massa / I_vuoto` | `~13` | `~27` | `2.1` |
| **`P3`** | `Λ` | `~140` | `~5` | `0.036` |
| **`P3b`** | ampiezza dello scuotimento | — | **`~5×` più bassa** | `0.2` |
| **`P4`** | `cs_floor` dentro le masse | `~0.9` | `~0.55` | `0.61` |
| **`P5`** | `lambda_nodi` | — | **quasi COSTANTE, `0.74`-`0.76 LAM` ovunque** | — |

**LE ASSUNZIONI, dichiarate:** `SCALA_AMP = 1` · pesi `exp(-d/LAM)` · **nessuna correlazione
`RSA`**.

> **⚠ E UNA DICHIARAZIONE DI PROVENIENZA, perche' conta per come si legge un errore:
> QUESTE PREVISIONI VENGONO DAL MANDATO, NON LE HO DERIVATE IO.** Le committo come sono, con le
> loro assunzioni, **e le verifico al passo zero**. Se sbagliassi a rivendicarle come mie, un
> loro fallimento non direbbe piu' se è sbagliata l'assunzione o il conto.
>
> **CRITERIO: se una previsione sbaglia di più di un FATTORE 2, va spiegato perche'** — *o
> l'assunzione è falsa, o la legge fa altro da ciò che dice* *(Luca)*. **E `P5` è la piu'
> interessante**: se `lambda_nodi` è quasi costante, **la legge di schermatura è di fatto
> SPENTA dalla soglia irraggiungibile** — cioè lo stesso difetto di `massa_critica_collasso`,
> visto da un'altra legge.

### ⚠ `U2` È ATTIVA IN ENTRAMBI I BRACCI DI `P-GONFIA` E FABBRICA LUNGHEZZA *(Luca, 2026-09-25)*

**Non cambia il criterio**, e va dichiarata come tale: serve a **leggere quanto del gonfiamento
viene dalla MITOSI** invece che dalla semina.

> **Il problema è che `U2` agisce in ENTRAMBI i bracci, e probabilmente PIÙ nel controllo**,
> dove `SEMINA_LAM` è spenta e **quasi tutti gli archi sono corti**. **Il confronto di
> `P-GONFIA` mescola quindi due effetti**, e senza contarli il suo esito — passi o fallisca —
> non si attribuisce.

**NEL REFERTO, PER OGNI BRACCIO:**

| | cosa | quando |
|---|---|---|
| **`U2a`** | **la LUNGHEZZA FABBRICATA da `_nasce`**, `sum(LAM - v)` sugli archi troncati, **SEPARATA per grandezza (`d`, `d0`) e per sito (`semina`, `mitosi`, `schwinger`)** e contata sugli **ARCHI VERI**. **Nel confronto con la crescita di `d0` entra SOLO `_sm_lund0_*`** | cumulativa, e **al netto del passo zero** |
| **`U2b`** | quanti archi sono stati **troncati**, e su quanti visti — **stessa separazione** | idem |
| **`U2c`** | **frazione di archi sotto `2 LAM`** | ai passi `0` e `120` |

### ❗ E IL CONTATORE CHE LUCA CITAVA NON MISURAVA QUESTO — rilievo mio, verificato dal codice

**`_g_sm_nascite` CONTA LE INVOCAZIONI di `_nasce`, non i troncamenti:**

```python
self._g_sm_nascite = getattr(self, '_g_sm_nascite', 0) + 1
return np.maximum(v, LAM)
```

**Una chiamata che non tronca nulla lo fa salire ugualmente.** Quindi *«quante volte `_nasce` ha
troncato un figlio della mitosi»* **non era leggibile**: il numero non c'era.

> **Tre contatori nuovi, tutti BYTE-INERTI** *(si somma, non si cambia)*: `_sm_visti`,
> `_sm_troncati`, **`_sm_lunghezza`**.
> ### **E `_sm_lunghezza` è quello che conta: `sum(LAM - d)` è il contributo DIRETTO di `_nasce`
> ### al gonfiamento di `d0`, NELLE STESSE UNITÀ DEL BILANCIO.**
> Così `P-GONFIA` non dice solo *«quanto è cresciuto»*: dice **quanta di quella crescita è
> lunghezza FABBRICATA alla nascita**, e quanto resta da spiegare.

### ❌❌ `U2` ERA SBAGLIATA: **UN CONTATORE SOLO, E MESCOLAVA `d` CON `d0`** *(rilievo di Luca, 2026-09-25)*

**Cio' che avevo scritto ieri:** *«`_sm_lunghezza` è il contributo DIRETTO di `_nasce` al
gonfiamento di `d0`, NELLE STESSE UNITÀ DEL BILANCIO»*. **Non lo era**, e la ragione è nel
codice che avevo letto io stesso per scrivere la riga.

> ### **`_nasce` è chiamata in QUATTRO siti, e la MOLTEPLICITÀ degli archi veri è DIVERSA in ognuno.**

| sito | chiamata | archi veri di `d` | archi veri di `d0` | dal codice |
|---|---|--:|--:|---|
| **`semina`** | `_allaccia`: `dd` | `1` | `1` | `d = concat([d, dd])` **e** `d0 = concat([d0, dd])` — **UNA chiamata vale per DUE grandezze** |
| **`mitosi`** | `dh` | **`2`** | `0` | `d = concat([d[keep], dh, dh])` — **`dh` ha `len(sel)` voci ma diventa DUE archi per voce** |
| **`mitosi`** | `d0new` | `0` | `1` | `d0new` è **già** `concat([d0h, d0h])`: i due figli ci sono già |
| **`schwinger`** | `dd` | **`2`** | **`2`** | `concat([d, dd, dd])` **e** `concat([d0, dd, dd])` |

**TRE DIFETTI IN UNO, e il primo distrugge proprio la ragione per cui il contatore esisteva:**

1. **la somma MESCOLAVA `d` e `d0`** — quindi **non era «nelle unità del bilancio di `d0`»**,
   che era l'unica cosa che le dava senso in `P-GONFIA`;
2. **il sito `dh` era SOTTOCONTATO DI `2`**: contava le voci di `dh`, non gli archi che ne nascono;
3. **`_sm_visti` contava le VOCI**, non gli archi, con lo stesso errore nel denominatore.

**LA CORREZIONE:** `_nasce(v, dove, md, md0)`. Contatori `_sm_{lun,tr,vis}{d,d0}_{sito}`,
**separati per grandezza e per sito, sugli ARCHI VERI**.

> ### **Solo `_sm_lund0_*` entra nel confronto con la crescita di `d0` in `P-GONFIA`.**

**⚠ E LO SCHWINGER È UN QUARTO SITO, NON NEI TRE DEL RILIEVO:** è `×2` su **entrambe** le
grandezze. Lo segnalo perché cambia il conto, e perché la sua lunghezza viene da **`pos`, non da
`d`** — cioè è anche la voce **`A3`** della coda.

### ✅ IL SIGILLO: `csv/_seal_fork/_sigillo_u2_contatori.py`

**Il caso a risposta nota, come chiesto da Luca:** **una MITOSI VERA** con **un solo arco a
`1.2 LAM`** — `dh = 0.6 LAM < LAM`, **entrambi i figli troncati**.

```
ATTESO PER COSTRUZIONE:
  _sm_trd_mitosi   = 2                       (DUE archi di `d`, non uno)
  _sm_trd0_mitosi  = 2
  _sm_lund_mitosi  = 2 * (LAM - 0.6 LAM)     = 0.8 LAM
  _sm_lund0_mitosi = 2 * (LAM - 0.6 LAM)     = 0.8 LAM
```

**`U2-6` È IL CASO CHE DEVE FALLIRE** *(`P1-sexies`, ed è il criterio più importante)*: la
formula VECCHIA, **sullo stesso evento**, dava `0.4 LAM` sul lato `d` e una somma mescolata di
`1.2 LAM`, **che non è in nessuna delle due unità**. Il criterio applicato a quella **deve dare
FAIL**: se passasse, non discriminerebbe la cura dal difetto.

**`U2-5` è MODEL-FREE:** non confronta col mio conto, **legge `d` e `d0` e conta gli archi che
nell'ARRAY stanno a `LAM`**. **`U2-8` è la BYTE-IDENTITÀ** al codice di `HEAD`, col suo controllo
positivo *(un caso diverso DEVE risultare diverso, sennò «identico» è un confronto cieco)*.

**COSA IL SIGILLO NON DICE, dichiarato nel referto:** **il sito `schwinger` NON è collaudato**
— quel ramo non è stato fatto scattare, e la sua molteplicità è **letta dal codice, non
misurata**.

### ❗ IL COSTO SI MISURA DAGLI **ARCHI**, non dai nodi *(punto 5)*

**Al passo ZERO si conta il numero di ARCHI di entrambe le scene, PRIMA di stimare i tempi.**
**Stima da verificare:** `(a)` `~500k` archi *(simile a `CURA 2`)*, `(b)` `~150k`.

> **E il mio avviso di costo di ieri era sbagliato nella grandezza guardata:** avevo detto
> *«il vuoto di `A` ha `5.4×` i nodi, quindi costera' molto di piu'»*. **Il costo dipende dagli
> ARCHI**, e con `A13` i nodi sono **piu' distanti**, quindi **meno connessi**: `5.4×` i nodi
> **non significa `5.4×` gli archi**. **Si misura, non si stima.**

### ❗ `P-GONFIA` — **LA PREVISIONE, CON LA SUA SOGLIA NUMERICA FISSATA ORA**

**La previsione di Luca:** *la crescita della mediana di `d0` nei 120 passi **CALA NETTAMENTE**
rispetto al giro di `CURA 2`.*

**Il riferimento, LETTO dal bilancio di `CURA 2`** *(`csv/_test_fork/_cura2_corto/BILANCIO_d0.txt`,
colonna `med vivi`)*:

```
med vivi:  passo 8 -> 0.938570      passo 120 -> 1.382321
CRESCITA CURA 2 = +47.2795 %
```

> ### **SOGLIA: la crescita deve essere `< +23.64 %`, cioè MENO DELLA METÀ.**
>
> **⚠ E «metà» È UNA SCELTA, non una derivazione — lo dico invece di farla passare per un
> conto.** Non so derivare quanto debba calare: so che il freno agisce **sugli archi al muro**,
> e quegli archi **non esisteranno più**. **Un fattore 2 è la soglia più grossolana che possa
> ancora distinguere «cala nettamente» da «cala un po'»**, ed è grossolana **di proposito**:
> il riferimento è **UN SEME SOLO**, la dispersione fra semi **non è misurata** *(`P3`)*, e una
> soglia fine su un riferimento senza barra sarebbe finta precisione.
>
> ### **SE NON CALA → IL MOTORE È IL FRENO, e il freno-legge va in coda** *(decisione di Luca)*.
> **È una previsione che può FALLIRE e indirizzare il lavoro**, non una che conferma comunque.

> ### ⚠ LE ALTRE PREVISIONI, scritte PRIMA
> **NON sarà byte-inerte e cambierà TUTTO**: `n`, la densità, il bilancio, la mitosi.
> **Mi aspetto numeri diversi, non numeri uguali.**
>
> **⚠ E DUE INCOGNITE, dichiarate invece che nascoste:**
> 1. **quanti nodi entreranno davvero.** Con distanza minima `LAM` la densità massima è fissata
>    dalla geometria: la semina **potrebbe RIFIUTARE** le taglie di oggi. **Se rifiuta, non è un
>    difetto della cura: è `A13` che dice che quella taglia non esiste.**
> 2. **la coesione.** Il grafo sarà molto più rado e `R_CONN = 3·LAM` resta invariato.
>    **Non l'ho misurato, e `S7` è dove si vedrà.**

## 5-bis. ❗ **IL RIFIUTO HA GIÀ PARLATO, AL PRIMO GIRO DEL FLAG** *(2026-09-24, blob `ba9054ce`)*

**Non era una prova: stavo solo verificando che il flag arrivasse.** `--semina-lam` da solo, e
la *cura del mondo* ricostruisce il vuoto di fondo dopo i flag:

```
[semina-lam] RIFIUTO DI SEMINARE: non ci stanno 900 nodi a distanza >= LAM
  chiesti      n = 900
  raggio       r = 4.000000   (= 5.000 LAM)
  LAM            = 0.800000
  collocati      = 352   <- il MASSIMO RAGGIUNTO, misurato adesso
  stima RSA      = 384   <- frazione di impacchettamento ~0.384 (STIMA di letteratura)
  nodi gia' presenti = 0
```

> ### **IL VUOTO DI FONDO DI DEFAULT — `900` NODI IN RAGGIO `4.0` — NON ENTRA: NE STANNO `352`.**
>
> **E' la prima incognita che avevo dichiarato, e si è materializzata subito.** **Non è un
> difetto della cura: è `A13` che dice che quella taglia non esiste.** Prima di oggi il sistema
> la otteneva **sovrapponendo i nodi sotto la scala di Planck.**
>
> **E il RIFIUTO ha fatto il suo mestiere al primo colpo:** senza di lui la semina avrebbe
> consegnato **`352` nodi invece di `900`, in silenzio**, e ogni misura successiva sarebbe stata
> su una taglia diversa da quella scritta nel comando *(`A9`)*.

### ⚠⚠ **IL LIMITE DEL RIFIUTO, e va letto PRIMA di credergli** *(rilievo di Luca, 2026-09-24)*

`_semina_lam` si arrende quando **un lotto di `n` proposte non accetta nessun punto**, e **il
lotto ha la taglia CHIESTA**. Da qui tre conseguenze, e nessuna è innocua:

1. **`collocati` DIPENDE DA `n`.** Più se ne chiedono, più tentativi si fanno, più se ne
   piazzano. **MISURATO a `r = 4.0`, stesso seme:**
   ```
   n=900 -> 372 | n=2000 -> 371 | n=4000 -> 399 | n=8000 -> 411 | n=16000 -> 398 | n=32000 -> 418
   ```
   **`+12 %` su un intervallo di richieste di `35x`.** **Non è «il massimo che ci sta»: è un
   LIMITE INFERIORE che cresce con la richiesta.**
2. **CON `n` PICCOLO IL RIFIUTO PUÒ ESSERE FALSO:** bastano `n` mancati di fila mentre c'è
   ancora posto. **È il silenzio al contrario che `A9` vuole evitare** — non nasconde una
   riduzione, ma **può negare una taglia che in realtà entrerebbe.**
3. **la bisezione del raggio poggia su un sì/no RUMOROSO**, quindi il raggio per `n` **si dà
   con la sua dispersione fra semi, mai come un numero secco.**

> **IL CRITERIO DI ARRESTO NON È STATO CAMBIATO** *(decisione di Luca: prima si misura quanto
> pesa)*. Cambiarlo introdurrebbe **un NUMERO** — la taglia del lotto — che è ciò che si voleva
> evitare *(par.3)*. **Il limite è scritto DENTRO il messaggio di rifiuto**, così chi lo legge
> lo legge lì e non qui.

**⚠ E IL `352` DEL PRIMO GIRO VA RILETTO COSÌ:** veniva da `ask = 900`. **Non era sbagliato,
ma non era «la capienza»: era la capienza A QUELLA DOMANDA.**

**LA STIMA `RSA` REGGE:** `384` previsti contro `352` misurati, **scarto `8.3 %`** — e la stima
è un **limite superiore** *(ignora il bordo)*, quindi il verso è quello giusto.

### ➤ COSA NE DISCENDE PER LA TAGLIA, e è una DECISIONE DI LUCA

`n` scala come `r³`, quindi il raggio che serve è `r = 4 · (n/352)^(1/3)`:

| `n` chiesti | raggio necessario | in `LAM` |
|--:|--:|--:|
| `352` | `4.00` | `5.0` |
| `500` | `4.50` | `5.6` |
| `900` | `5.48` | `6.8` |
| `2391` *(la scena di oggi)* | `7.60` | `9.5` |

> **Il punto di partenza che Luca ipotizzava — `~500` nodi, raggio `~4` — è a un soffio: con
> raggio `4` ne stanno `352`, e per `500` serve `4.5`.** **La taglia la sceglie Luca** *(mandato)*.

---

## 5-ter. ✅ **L'ARRESTO SI DERIVA DA `LAM`** — decisione di Luca, 2026-09-24

> **Nessuna taglia di lotto. Saturazione ESATTA.**

**IL METODO — Zhang & Torquato (2013), suddivisione di celle:**

```
celle di lato LAM/sqrt(3)  ->  diagonale = LAM  ->  AL PIU' UN NODO PER CELLA
  cella COPERTA da un nodo (distanza dal nodo allo spigolo PIU' LONTANO <= LAM)  -> MORTA
  cella fuori dalla regione                                                      -> MORTA
  cella LIBERA (nessun nodo entro LAM dal suo punto PIU' VICINO)  -> ci si puo' seminare
  cella PARZIALMENTE coperta                                      -> SI SUDDIVIDE in 8
si propone SOLO nelle celle vive; si finisce quando non ne resta NESSUNA
```

> ### **IL RIFIUTO SCATTA SOLO SE `n` SUPERA LA SATURAZIONE VERA.**
> Non più «un lotto senza accettazioni»: **non c'è più posto, e lo si sa per costruzione.**
> **Cade con lui il difetto che Luca aveva trovato:** il rifiuto **non può più essere falso.**

### ⚠⚠ E QUI DEVO DIRE UNA COSA SU «ZERO NUMERI NUOVI»

**Il metodo è parameter-free nella FISICA: l'unica lunghezza è `LAM`, e `LAM/sqrt(3)` ne
discende** *(la diagonale del cubo di lato `a` è `a·sqrt(3)`, quindi `a = LAM/sqrt(3)` dà
diagonale `LAM`)*.

**MA LA SUDDIVISIONE NON TERMINA IN MODO ESATTO AL BORDO DELLA REGIONE**, e va detto:

- una cella tutta dentro la palla si risolve *(coperta o libera)* in un numero finito di
  suddivisioni, perché i nodi sono finiti;
- **una cella che ATTRAVERSA la superficie della sfera non è né dentro né fuori**, quindi si
  suddividerebbe **all'infinito**: il guscio ha volume che tende a zero ma **non diventa mai
  vuoto**.

> ### ✅ **LA RISOLUZIONE NON SI SCEGLIE — precisazione di Luca, 2026-09-24**
>
> ```
> si ferma la suddivisione quando il lato della cella e' piu' piccolo di cio' che
> `float64` distingue RISPETTO A LAM:        lato < LAM * eps_macchina
> ```
>
> **`eps` è una proprietà DEL CALCOLATORE, non un numero scelto** — `np.finfo(float).eps`,
> `2.22e-16`. **Sotto quella soglia due posizioni non sono più posizioni diverse: sono lo
> stesso `float`.** Suddividere ancora non aggiungerebbe informazione, **ne toglierebbe**.
>
> **Avevo scritto «non è zero numeri, è zero numeri fisici più una risoluzione»: con `eps` la
> frase cade**, perché `eps` non è un numero del modello né una mia scelta. **Resta UN
> NUMERO SOLO: `LAM`.**
>
> **IL CONTATORE `A8` RESTA** *(Luca)*, e va detto perché: `eps` rende la risoluzione non
> arbitraria, **non la rende innocua**. Se celle vengono abbandonate lì, la saturazione
> dichiarata **non è esatta**, ed è esattamente ciò che il contatore deve rendere visibile.
> **Un presidio che non conta non è un presidio.**

## 5-ter-bis. ✅ **IL CODICE DELL'ARRESTO DERIVATO** — *2026-09-24*

**Due metodi:** `_celle_vive` *(la classificazione)* e `_semina_lam` *(il ciclo)*.

```
celle di lato LAM/sqrt(3), OGNI cella col SUO lato (le libere restano grandi)
  MORTA        tutta fuori dalla palla, OPPURE coperta da un nodo
  LIBERA       tutta dentro, e il nodo PIU' VICINO AL CENTRO dista >= LAM
               ⚠ NON "ogni suo punto va bene": il test guarda UN SOLO nodo, e un
                 ALTRO nodo puo' stare entro LAM da un angolo (rilievo di Luca)
  DA DIVIDERE  in parte coperta, o a cavallo del bordo -> si spezza in 8
la cella si sorteggia con peso `lato^3`; si finisce quando non resta nessuna cella
```

### ⚠ DUE LIMITI DEL CODICE, dichiarati invece che taciuti

1. **il test guarda UN SOLO nodo — il più vicino al CENTRO della cella — e questo ha DUE
   conseguenze, non una:** una cella coperta dall'**unione** di più nodi non è riconosciuta e
   **si suddivide** *(costa lavoro, non correttezza)*; **e una cella detta «LIBERA» può avere un
   altro nodo entro `LAM` da un angolo**, quindi **«LIBERA» non garantisce che ogni suo punto
   vada bene** *(rilievo di Luca)*.
   **LA CORRETTEZZA NON DIPENDE DA QUESTO TEST:** dipende dal fatto che **ogni proposta è
   verificata contro TUTTI i nodi** prima di essere accettata. Il test delle celle serve a
   sapere **dove proporre** e **quando fermarsi**, non a garantire i punti;
2. **la risoluzione `LAM · eps`** ferma la suddivisione, e le celle abbandonate lì si **contano**
   *(`_sl_abbandonate`)*. **Se il contatore sale, la saturazione dichiarata non è esatta.**

### ❌ E UNA DIAGNOSI MIA, SBAGLIATA, che resta scritta

Avevo scritto che **`C3` aveva preso un difetto del codice** *(frazione `0.536` contro `0.384`)*.
**Era la frazione GLOBALE, che il mandato di Luca aveva già dichiarato inadatta.**
**La prova che la diagnosi era sbagliata: dopo la «correzione» la globale è SALITA** *(`0.536`
→ `0.568`)*. **Ho letto un numero dichiarato inadatto e ne ho tratto una conclusione.**

**Il cambiamento resta comunque giusto, per un'altra ragione:** proponevo **un punto per cella**,
quindi gli interstizi pesavano come le regioni grandi e **le proposte non erano uniformi nel
volume libero** — e l'`RSA` è *esattamente* «uniforme nella regione, condizionato
all'accettazione». **La cura era giusta; il motivo che avevo scritto no.**

## 5-quater. I CRITERI DELL'ARRESTO DERIVATO — **fissati PRIMA del codice** *(Luca)*

| | criterio | perché |
|---|---|---|
| **`C1`** | **flag spento: byte-identico** | par.2.1. L'arresto vive dentro `SEMINA_LAM`: a flag spento non esiste |
| **`C2`** | **la capienza è INDIPENDENTE da `n` chiesto** *(prova del raddoppio)* | ❗ **È IL CRITERIO CHE OGGI FALLISCE:** misurato `+0.61 %`, `+4.11 %`, `+2.77 %` a tre raggi. **Con l'arresto derivato deve dare `0` esatto**, perché la saturazione non dipende dalla domanda |
| **`C3`** | **frazione di impacchettamento `0.384` NELLA SFERA INTERNA** — i nodi a distanza `>= R_CONN` dal bordo, **entro la dispersione fra QUATTRO semi** | ❗ **È IL CONTROLLO CONTRO UN VALORE ESTERNO AL PROGETTO**: se si discosta, **il codice è sbagliato**, non il sistema. **RIDEFINITO da Luca, 2026-09-24:** si misura **dentro**, dove il bordo non arriva, **e li' vale `0.384` senza sconti** |
| **`C4`** | **nessun rifiuto falso**: con `n` sotto la capienza misurata la semina riesce **sempre**, su **quattro semi** | è il difetto che Luca ha trovato, e questo criterio **lo mette alla prova invece di fidarsi** |

> ### ⚠ `C3` È IL CRITERIO PIÙ FORTE DEI QUATTRO, e va detto perché
> `C1`, `C2` e `C4` verificano che il codice sia **coerente con se stesso**. **`C3` lo confronta
> con un numero che nessuno in questo progetto ha scelto** — la frazione di saturazione
> dell'`RSA` in 3D, `~0.384`, misurata in letteratura su un problema che è lo **stesso**.
> **È il solo dei quattro che possa dire «il codice è sbagliato» invece di «il codice non fa
> quello che credevo».**
>
> ### ✅ **E IL SUO LIMITE È TOLTO, NON GIRATO — precisazione di Luca**
>
> **Avevo scritto «`C3` si legge sui raggi GRANDI, e sui piccoli si aspetta di meno».**
> **È un criterio che si adatta al risultato**, cioè il difetto che `P1-sexies` insegue: una
> soglia che si allarga dove il dato non torna **non può più fallire**.
>
> **LA FORMA GIUSTA È RESTRINGERE IL DOMINIO, NON LA SOGLIA:** si misura la frazione **solo
> sui nodi a distanza `>= R_CONN` dal bordo**. **Lì il bordo non arriva, e `0.384` vale senza
> sconti**, entro la dispersione fra **quattro semi**.
> **La soglia resta dura; è il dominio a essere onesto.**

**⚠ I NUMERI DI PRIMA RESTANO NEL REGISTRO COME STORIA** *(decisione di Luca)*: sono
misurati col criterio a lotti, e **vanno rifatti**. Il par.5-bis e questa sezione dicono con
quale criterio ciascuno è stato preso.

## 6. `massa_critica_collasso` — **MARCATA, NON TOCCATA** *(decisione di Luca)*

> ### **«Tarata sotto la scala di Planck, da non usare.»**

**Il conto, derivato** *(`csv/_test_fork/_usi_massa_critica.py`)*:

```
massa_critica_collasso() = 621.4858 nodi, in una sfera di raggio LAM = 0.8
quanti PUNTI stanno in una palla di raggio LAM con distanze mutue >= LAM?
  uno al centro + al piu' 12 sulla sfera (separazione >= 60 gradi = NUMERO DI BACIO, K(3)=12)
  -> al piu' 13
RAPPORTO CHIESTO / POSSIBILE = 47.81
```

**La costante chiede ~`48` volte più nodi di quanti ne stiano.**

**`36` usi nel simulatore, elencati dall'AST: `21` nel codice della FISICA** *(dove essere tarata
sotto la scala di Planck **entra nelle leggi**)* **e `15` nelle SCENE** *(dove decide **quanti**
nodi seminare)*. **Non si tocca niente:** l'elenco è **il perimetro della marcatura**, perché
una costante marcata senza l'elenco di chi la usa è un'avvertenza generica, **e un'avvertenza
generica non impedisce nulla** *(`A9`)*.

> **⚠ E IL MIO PRIMO CONTO ERA SBAGLIATO:** avevo usato l'impacchettamento di **Kepler** —
> palline di raggio `LAM/2` **interamente dentro** una sfera di raggio `LAM`, `8·0.7405 = 5.92`.
> **Kepler impone una condizione più stretta di quella vera**: qui il vincolo è **solo sui
> centri**. **Il numero di Luca — «circa una dozzina» — era esatto, e il mio troppo piccolo di
> ~2.2 volte.** Il conto sbagliato **resta stampato nel referto**, col perché.

## 7. COSA QUESTA SCHEDA **NON** COPRE

- **la MITOSI**, che crea nodi vicino al genitore: **rispetta `LAM`?** `S4` lo rileverebbe **al
  passo zero**, non ai passi dopo. **→ in coda, misurarlo;**
- **`Λ = media GLOBALE di `I` dentro la legge locale di `cs`** — più materia nel sistema, meno
  rallentamento: **sospetto famiglia `D01`/`D03`. → in coda;**
- **la scelta alternativa: FILTRARE GLI ARCHI** *(`NASCITA_LAM`)*, **ritirata** — vedi il
  cappello di questa scheda. **Esclusa per DIMOSTRAZIONE**, non per misura: lascia i nodi sotto
  `LAM`, quindi **viola `A13` per costruzione**.

---

<!-- SCHEDA nome=invarianti funzioni=verifica_invarianti flag=INVARIANTI,DOMINI -->

# ⑩ GLI INVARIANTI DI DOMINIO — **`C5`**

> **Scheda aperta il 2026-09-24, e mancava.** `C5` è in `CURE VERIFICATE` con sigillo `3/3`,
> **è la sola cura ACCESA DI DEFAULT**, e **non aveva una scheda**: `REG-R` l'ha preteso quando
> `E4-LAM` ha toccato la legge. *(Un difetto di inventario, non di fisica — ma l'ordine giusto
> è questo: prima la scheda.)*

## LA FORMA

**`verifica_invarianti(dove, passo)`** scorre **`DOMINI`** — un dizionario
`nome → (forma, perché)` — e per ogni grandezza di stato presente controlla che stia **nel suo
dominio**. Alla prima violazione **solleva `DominioViolato`** con: **la grandezza**, **la regola
violata**, **il passo**, **gli INDICI**, **i valori**, **dove**, e **quale arco** *(`i`-`j`)*.

**DUE LIVELLI, e la distinzione è il punto:**

| livello | che cosa prende | come |
|---|---|---|
| **NUMERICO** | overflow, **divisione per zero**, valori non validi | `np.seterr(over='raise', divide='raise', invalid='raise', under='ignore')` a **`:7382`**. **L'UNDERFLOW non ferma niente**, perché densità come `1e-81` di un nodo neonato sono **legittime** |
| **FISICO** | ogni grandezza **dentro il suo dominio**, a fine passo | `DOMINI` + `verifica_invarianti` |

> **L'esplosione del 21/9 NON era un overflow** *(`1.8e6` è un numero normale)*: **l'avrebbe
> presa solo la regola FISICA `peq >= 0`.** È la ragione per cui i due livelli non si
> sostituiscono.

## LE FORME DI DOMINIO

| forma | regola | esempi |
|---|---|---|
| `'lam'` | **`>= LAM`** | `d`, `d0` |
| `'pos'` | `> 0` | `_dt_e_ultimo`, `_r_corrente`, `_cs_nodo_prev` |
| `'finito'` | finito, nessun vincolo di segno | `vd`, `_spinor_lift` |
| `'fase'` | in `[0, 4π)` | `phi`, `phi0` |
| `'unita'` | `|x| = 1` *(tolleranza `1e-6`)* | gli spinori |
| `'idx'` | `0 <= x < n` | `i`, `j` |

## ✅ `E4-LAM` — **LA LEGGE `d >= LAM` SI VERIFICA SEMPRE** *(decisione di Luca, 2026-09-24)*

> ### **«La lunghezza degli archi non può scendere sotto la lunghezza tipica del sistema» è una
> ### LEGGE, non una garanzia che dipende da un flag.»**

**PRIMA** il controllo della forma `'lam'` era dentro `if _lam_attivo:`, con
`_lam_attivo = SCALA_MIN or SCALA_MIN_PASSO`, e **a flag spenti DEGRADAVA a `> 0`**:

```python
if _lam_attivo:  cattivo = ~fin | (vf < LAM * (1.0 - 1e-12))   # '>= LAM, con la scala minima accesa'
else:            cattivo = ~fin | (vf <= 0.0)                   # '> 0 (scala minima SPENTA)'
```

**DOPO**, incondizionato:

```python
cattivo = ~fin | (vf < LAM * (1.0 - 1e-12))
regola  = '>= LAM (= %.6f) -- LEGGE, non opzione' % LAM
```

**E `_lam_attivo` è stato TOLTO**: era il suo unico uso, e lasciarlo sarebbe stato codice morto
*(verificato dall'AST: `0` riferimenti di codice)*.

**Perché è giusto, in una riga:** **una legge verificata solo quando un flag è acceso non è una
legge, è un'opzione** — ed è `A9`: *un presidio che non impedisce non è un presidio.*

**La tolleranza `1e-12` non è un numero scelto:** è l'**arrotondamento** di `LAM`, cioè la
precisione con cui `LAM` stesso è rappresentabile.

### **IL SIGILLO** — `csv/_seal_fork/_sigillo_e4lam.py`

| | | |
|---|---|---|
| `T3` | **un arco sotto `LAM` a flag SPENTI FERMA il run** | quello che prima **non** faceva |
| `T4` | e con `d >= LAM` **non** si ferma | **il controllo che rende `T3` leggibile**: senza, `T3` passerebbe anche se il controllo si fermasse sempre |
| `T5` | **byte-inerte**: `206` campi identici, `0` diversi contro `_cura1_corto` | l'invariante **legge soltanto** |

**Il messaggio, verbatim:**

```
[INVARIANTE] `d` VIOLA `>= LAM (= 0.800000) -- LEGGE, non opzione` al passo 1
  indici (primi 8): 1     valori: 4.000000e-01     arco=1-2
```

## ❌ `D37` — **UNA CHIAVE DUPLICATA NEI `DOMINI`, ed è mia**

`'_cs_nodo_prev'` compariva **due volte**: `:226` *(la mia)* e `:257` *(preesistente)*.
**In un letterale di dict vince l'ULTIMA**, quindi la mia era **codice morto** — e **il sigillo
lo ha mostrato**, stampando una descrizione **che non era la mia**.

**La causa è `P1`:** avevo cercato la voce in una finestra di **28 righe** (`213-240`) e la voce
sta a **`:257`**. **Ho concluso un'ASSENZA da una ricerca PARZIALE.**
**Cura: si toglie la mia, si tiene la preesistente.** **E la derivazione resta valida:
`cs > 0` era GIÀ un invariante**, fatto da qualcun altro prima di me.

### ✅ **`D37` È CURATO** — 2026-09-24, lo stesso giorno in cui è nato

La voce duplicata è **via**, e **la derivazione di `cs > 0` è stata SPOSTATA sulla voce
preesistente** invece di essere buttata — col motivo per cui era nata **e col perché era
un duplicato**, così chi la legge fra un mese sa entrambe le cose.

**E c'è un TEST PERMANENTE:** **`T1b`** del sigillo `E4-LAM` verifica **dall'AST** che il
letterale `DOMINI` **non abbia chiavi duplicate** — oggi **`42` chiavi, `0` duplicate** —
col suo collaudo `K7` *(un `DOMINI` con `'a'` due volte → `['a']`)* e `K8` *(uno pulito non
dà falsi allarmi)*.

> **⚠ IL LIMITE DI `T1b`, dichiarato:** guarda il **letterale**. Voci aggiunte con
> `DOMINI[...] = ...` **non le vedrebbe**. Oggi non ce ne sono, e se ce ne fossero il test
> **non lo direbbe**.

## ⚠ COSA QUESTA LEGGE **NON** FA, dichiarato

- **non corregge**: **legge soltanto**, e su un run sano **non cambia un bit**. Se scatta, il
  run **si ferma** — non si aggiusta;
- **non dice se la REALIZZAZIONE di una legge sia giusta.** Verifica che `d >= LAM`; **come** il
  sistema lo ottiene è il **freno a senso unico**, cioè **`D31`**. **La legge è giusta, la
  realizzazione no**, e sono due cose separate;
- **non copre le grandezze assenti**: `getattr(self, quale, None) -> continue`. Una grandezza
  che **non esiste** non viene controllata, e **questo non è contato**. *(Candidato per un
  contatore `A8`: quante voci di `DOMINI` vengono SALTATE per assenza. Non fatto.)*

## COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **se `'fase'` debba essere `[0, 4π)` o `[0, 2π)`.** È la domanda di `FASE_2PI`, e
   l'invariante **segue** la decisione invece di guidarla — oggi codifica il `4π`
   **dichiarato**, che la mappa del `4π` classifica come **convenzione**, non come misura;
2. **quante voci di `DOMINI` vengano saltate per assenza** in un run vero: non misurato.

---

<!-- SCHEDA nome=freno-legge funzioni=_smorza flag=SCALA_MIN,SCALA_MIN_PASSO,LAM -->

# ⑪ IL FRENO DIVENTA LA LEGGE — **la cura proposta di `D31`**

> **Decisione di Luca, 2026-09-24: SCHEDA ORA, CODICE SOLO DOPO LA PROVA DI `CURA 2`.**
> **Qui non si tocca una riga di codice.**

## 0. LA LEGGE, nelle parole di Luca

> ### **«Nessun arco sotto `LAM`, e l'avvicinamento al minimo è ASINTOTICO: rallenta sempre
> ### di più, senza mai toccarlo.»**

**Che cosa vuol dire, in una riga:** più l'arco è vicino al minimo, più **ogni suo movimento**
viene rallentato. **Al confine la mobilità va a zero**: l'arco si avvicina a `LAM` per sempre
senza toccarlo, come una curva che si avvicina al suo asintoto. **Lontano dal confine la
mobilità torna quasi piena.**

**✅ LA LEGGE È GIUSTA. ❌ LA REALIZZAZIONE NO.**

## 1. IL FRENO DI OGGI — `_smorza`, `:3607-3618`

```python
scende = dx < 0.0
fatt   = max(0.0, 1.0 - LAM / prima)          # = (d - LAM)/d  =  LA MOBILITA'
eff    = np.where(scende, dx * fatt, dx)      # <-- SOLO la discesa
```

Con **`u = d − LAM`** *(la distanza dal minimo)* e **`m = u/d`** *(la mobilità)*:

| verso | oggi | è asintotico? |
|---|---|:--:|
| **discesa** `dx < 0` | `u ← u·(1 + dx/d)`, cioè incremento `dx·m` | **SÌ** — `m → 0` al confine |
| **salita** `dx > 0` | `u ← u + dx` — **identità esatta, nessun rallentamento** | **NO** |

> **È tutta qui l'asimmetria, ed è il cricchetto di `D31`.**

## 2. LA DERIVA DI OGGI — **primo ordine, e MASSIMA AL CONFINE**

Rumore simmetrico: `dx = +a` e `dx = −a` con probabilità `1/2`.

```
E[Δu]  =  ½·(+a)  +  ½·(−a·m)  =  (a/2)·(1 − m)  =  (a/2)·(LAM/d)
```

| | |
|---|---|
| **ordine nel rumore** | **PRIMO** — lineare in `a` |
| **al confine** *(`d → LAM`)* | `LAM/d → 1` ⇒ **`E[Δu] → a/2`: la deriva è MASSIMA proprio dove il vincolo morde** |
| **lontano** *(`d ≫ LAM`)* | `LAM/d → 0` ⇒ la deriva svanisce |

> **Il cricchetto spinge gli archi LONTANO dal muro, e spinge di più quanto più sono vicini.**
> È la forma esatta di ciò che `Z113` ha dimostrato *(deriva `+1.582064e-03` contro l'attesa
> derivata `+1.582007e-03`, scarto `0.0 %`)* e che i bilanci misurano: il termine **FRENO** vale
> **`+117 %`** di `Δ(Σd0)` nel riferimento di `G4`. **Un freno che AGGIUNGE lunghezza è un
> motore.**

## 3. LA FORMA PROPOSTA — **la stessa mobilità nei DUE versi, in forma esatta**

```
(d − LAM)  ←  (d − LAM) · exp(dx / d)
```

cioè, tenendo l'interfaccia di `_smorza` *(che ritorna un INCREMENTO)*:

```
eff  =  u · (exp(dx / d) − 1)              # e il chiamante fa d += eff, come oggi
```

### **LE TRE PROPRIETÀ, verificate sulla formula**

| | | |
|---|---|:--:|
| **(a) SIMMETRICA** | lo stesso fattore per `dx > 0` e `dx < 0`. **Un arco vicino al minimo è «viscoso»: si muove poco in entrambi i versi** | ✅ |
| **(b) MAI SOTTO `LAM`, per QUALUNQUE passo** | `exp(·) > 0` sempre ⇒ `u_new > 0` **strettamente**, anche per `dx → −∞`. **L'arco si avvicina a `LAM` per sempre senza toccarlo** | ✅ |
| **(c) LOCALE** | lontano da `LAM`: `u ≈ d` ⇒ `u_new ≈ d·exp(dx/d) ≈ d + dx` — **tende all'identità** | ✅ |

### **E AL PRIMO ORDINE È ESATTAMENTE LA MOBILITÀ DI OGGI**

```
u·(exp(dx/d) − 1)  =  u·(dx/d)  +  O(dx²)  =  dx·m  +  O(dx²)
```

**Cioè: il fattore non cambia, cambia il VERSO IN CUI SI APPLICA.** Non è una legge nuova: è
**la stessa legge, resa simmetrica**.

### ⚠ **E UN GUADAGNO CHE OGGI NON C'È: il vincolo vale anche A METÀ PASSO**

Oggi `u ← u(1 + dx/d)` diventa **negativo** se `dx < −d`, e il conto è immediato. Il
`max(0, …)` protegge il **fattore**, non il **risultato**. Oggi quel caso è solo **contato**
*(`_g_sm_patol`)*. **Con l'esponenziale non può succedere**, e il vincolo vale **a ogni
scrittura**, non solo al controllo di fine passo.

## 4. LA DERIVA RESIDUA — **secondo ordine, nulla al confine, decade lontano**

Stesso rumore simmetrico `dx = ±a`:

```
E[u_new]  =  u · ½·(e^{a/d} + e^{−a/d})  =  u · cosh(a/d)

E[Δu]     =  u · (cosh(a/d) − 1)  =  u · a²/(2d²)  +  O(a⁴)
```

| | oggi | proposta |
|---|---|---|
| **ordine nel rumore** | **primo**: `(a/2)·(LAM/d)` | **SECONDO**: `u·a²/(2d²)` |
| **al confine** `d → LAM` | **`→ a/2`, MASSIMA** | **`→ 0`** *(perché `u → 0`)* |
| **lontano** `d ≫ LAM` | `→ 0` | `→ a²/(2d)`, decade come `1/d`; **in termini RELATIVI `a²/(2d²)`** |

### **IL RAPPORTO FRA LE DUE, e da' una CONDIZIONE**

```
  nuova / oggi  =  [u·a²/(2d²)] / [(a/2)·(LAM/d)]  =  a·u / (d·LAM)  =  a·(d−LAM) / (d·LAM)
```

* **al confine** `d → LAM`: il rapporto **→ 0**. La proposta è **incomparabilmente migliore
  proprio dove oggi la deriva è massima**;
* **lontano** `d ≫ LAM`: il rapporto **→ `a / LAM`**.

> ### ❗ **QUINDI LA PROPOSTA È MIGLIORE OVUNQUE SE E SOLO SE `a < LAM`**
> cioè **se il passo tipico di rumore è più piccolo della scala minima**.
> **`LAM = 0.8`. Il valore di `a` NON È MISURATO**, e va misurato prima di cablare: è la
> prima cosa che la verifica deve dire. *(`A12` regola 4: dichiarato, non assunto.)*

## 4-bis. ❓ **LA CORREZIONE DI ITÔ** — *proposta del guardiano, e la scelta è di Luca*

> **La deriva residua viene dalla CONVESSITÀ di `exp`.** La correzione derivata la toglie:
>
> ```
> (d − LAM)  ←  (d − LAM) · exp(dx/d − (dx/d)²/2)
> ```

**Verificato numericamente, non solo algebricamente** *(`csv/_test_fork/_z147_ito.py`)*. Con
`s = a/d`:

| `s` | **piana** `E[f]−1` | attesa `s²/2` | **Itô** `E[f]−1` | attesa `−s⁴/12` | `\|Itô\|/\|piana\|` |
|--:|--:|--:|--:|--:|--:|
| `0.250` | `+3.141310e-02` | `3.125e-02` | **`−3.201451e-04`** | `−3.255e-04` | `1.019e-02` |
| `0.125` | `+7.822678e-03` | `7.813e-03` | **`−2.026048e-05`** | `−2.035e-05` | `2.590e-03` |
| `0.0625` | `+1.953761e-03` | `1.953e-03` | **`−1.270242e-06`** | `−1.272e-06` | `6.502e-04` |

**E l'ORDINE si legge raddoppiando `s`:**

| | piana | Itô |
|---|--:|--:|
| `s: 0.0625 → 0.125` | **`×4.004`** *(atteso `2² = 4`)* | **`×15.950`** *(atteso `2⁴ = 16`)* |
| `s: 0.125 → 0.25` | **`×4.016`** | **`×15.801`** |

> **La deriva scende dal SECONDO al QUARTO ordine**, e **cambia SEGNO: diventa NEGATIVA**,
> cioè **verso il confine** invece che lontano da esso.

### ✅ **E c'è un secondo guadagno che la sola deriva non mostra: la FEDELTÀ**

Entrambe le forme tendono alla legge **`u ← u(1 + x)`**, con `x = dx/d`. **Quanto le si
avvicinano:**

| `x` | `u(1+x)` | **piana** | eccesso | **Itô** | eccesso |
|--:|--:|--:|--:|--:|--:|
| `0.1` | `1.10000` | `1.10517` | **`+5.17e-03`** | `1.09966` | **`−3.41e-04`** |
| `0.3` | `1.30000` | `1.34986` | **`+4.99e-02`** | `1.29046` | **`−9.54e-03`** |

**`exp(x − x²/2) = 1 + x + O(x³)`: i termini in `x²` si cancellano ESATTAMENTE.**
Quindi, **su una spinta DETERMINISTICA**, la correzione **non è un bias: toglie l'eccesso di
convessità della piana**, ed è **più fedele** alla legge voluta, non meno.

> **⚠ Il «bias verso il basso di ordine `dx²`» è vero RELATIVAMENTE ALLA PIANA, non
> relativamente alla LEGGE.** Va detto così, perché le due letture portano a decisioni opposte.

### ❌ **MA C'È UN COSTO, e non è nella deriva: la forma NON È MONOTONA**

`f(x) = exp(x − x²/2)` ha **massimo in `x = 1`**, dove vale `√e = 1.64872`. **E poi scende:**

| `x` | piana `exp(x)` | **Itô** | |
|--:|--:|--:|---|
| `0.5` | `1.64872` | `1.45499` | |
| **`1.0`** | `2.71828` | **`1.64872`** | **← il MASSIMO** |
| `1.5` | `4.48169` | `1.45499` | |
| `2.0` | `7.38906` | `1.00000` | **← una salita non muove nulla** |
| `2.5` | `12.18249` | **`0.53526`** | **← UNA SALITA FA SCENDERE** |
| `3.0` | `20.08554` | **`0.22313`** | |

> ### ❗ **Per `dx > 2d` la forma di Itô TRASFORMA UNA SALITA IN UNA DISCESA.**
> **La piana è monotona sempre.** E qualunque salita, con Itô, **non può far crescere `u` di
> più di `√e ≈ 1.6487`** in una scrittura.
>
> **È esattamente la firma che `A11` cerca:** *una spinta più grande che produce un effetto
> più piccolo.* **Non è un difetto se `\|dx\|/d` resta piccolo — ma «resta piccolo» è una
> MISURA, non un'assunzione.**

### **IL CONFRONTO, in una tabella sola**

| | **piana** `exp(x)` | **Itô** `exp(x − x²/2)` |
|---|---|---|
| deriva, rumore simmetrico | `+u·s²/2` — **2° ordine, POSITIVA** *(lontano dal muro)* | **`−u·s⁴/12` — 4° ordine, NEGATIVA** *(verso il muro)* |
| fedeltà a `u(1+x)` | eccesso `+x²/2` | **esatta a `O(x³)`** |
| mai sotto `LAM` | ✅ | ✅ |
| **monotona in `dx`** | **✅ sempre** | **❌ massimo a `x=1`; per `x>2` una salita fa SCENDERE** |
| tetto per scrittura | nessuno | `u·√e ≈ 1.6487·u` |

### ⚠ **E UNA CONSEGUENZA CHE TOCCA UN ALTRO FRONTE**

**La deriva di Itô è NEGATIVA: spinge gli archi PIANO VERSO il muro**, mentre quella di oggi
li spinge **lontano**. **È debolissima** *(`4°` ordine)*, ma il verso è opposto — e la domanda
**«chi spinge gli archi contro il muro»** è già aperta come **`D33` / `S05`**. **Aggiungere una
spinta verso il muro, per quanto piccola, va detto a chi indaga quel fronte.**

> ### **LA SCELTA È DI LUCA, e non la prendo io.** Il criterio che la decide è **misurabile**:
> **la distribuzione di `\|dx\|/d`.** Se resta ben sotto `1`, **Itô è migliore su tutto** e la
> non-monotonia non si manifesta mai. Se arriva vicino a `1`, il tetto `√e` comincia a mordere,
> e **a `2` inverte**. → punti `V8` e `V9` della verifica.

## 4-ter. ✅ **LA TERZA FORMA: `1 + tanh(x)`** — *proposta di Luca, e domina la seconda*

```
(d − LAM)  ←  (d − LAM) · (1 + tanh(dx/d))
```

**Le quattro proprietà, verificate con lo STESSO strumento** *(`csv/_test_fork/_z147_ito.py`)*:

### ✅ **(1) DERIVA ESATTAMENTE NULLA, a TUTTI gli ordini**

`(1 + tanh(x)) + (1 + tanh(−x)) = 2` **per disparità di `tanh`**. Non è un'approssimazione: è
un'identità.

| `s` | `E[f] − 1` |
|--:|--:|
| `0.500` | **`0.000000000000000e+00`** |
| `0.125` | **`0.000000000000000e+00`** |
| `0.001` | **`0.000000000000000e+00`** |

> **Zero ESATTO in macchina, a ogni `s` provato.** La piana dà `+s²/2`, Itô `−s⁴/12`;
> **questa dà zero e basta.**

### ✅ **(2) MONOTONA** — la derivata è `sech²(x) > 0` sempre

Su `[−3, 3]`: **`0` incrementi negativi su `6000`**. *(Itô ne ha `2000` su `3000`.)*

### ✅ **(3) MAI SOTTO `LAM`** — `1 + tanh(x) ∈ (0, 2)`

`x = −50 →` fattore `0.000000e+00` *(numericamente, ma matematicamente `> 0`: `~2e^{2x}`)* ·
`x = +50 →` fattore `2.000000`.

### ✅ **(4) FEDELTÀ `O(x³)`, come Itô** — `1 + tanh(x) = 1 + x − x³/3 + …`, **nessun termine in `x²`**

| `x` | `u(1+x)` | piana | eccesso | Itô | eccesso | **tanh** | **eccesso** |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `0.30` | `1.30000` | `1.34986` | `+4.986e-02` | `1.29046` | `−9.538e-03` | `1.29131` | **`−8.687e-03`** |
| `1.00` | `2.00000` | `2.71828` | `+7.183e-01` | `1.64872` | `−3.513e-01` | `1.76159` | **`−2.384e-01`** |

**È anche un po' PIÙ fedele di Itô** a `x` moderati.

### ⚠ **(5) IL LIMITE, dichiarato: UNA SALITA AL PIÙ RADDOPPIA `(d − LAM)`**

`1 + tanh(x) < 2` **per costruzione**. È una **saturazione**, e `A11` cor.6 dice che *un limite
che satura è un allarme*. **Va giudicato con la distribuzione di `|dx|/d`, esattamente come il
tetto `√e` di Itô** — punti `V8`/`V9`.

> **Ed è MENO restrittivo del tetto di Itô** *(`2` contro `1.6487`)*, **e senza la
> non-monotonia.**

## 4-quater. ❗ **LE TRE FORME A CONFRONTO**

| | **deriva simmetrica** | **monotona** | **fedeltà a `u(1+x)`** | **tetto per una SALITA** |
|---|---|:--:|---|---|
| **piana** `exp(x)` | `+s²/2` — **2° ord., POSITIVA** *(lontano dal muro)* | **✅** | eccesso `+x²/2` | **nessuno** |
| **Itô** `exp(x−x²/2)` | `−s⁴/12` — 4° ord., NEGATIVA | **❌** *(max a `x=1`)* | `O(x³)` | `√e = 1.6487` |
| **tanh** `1+tanh(x)` | **`0` ESATTO** | **✅** | `O(x³)` | `2` *(raddoppia)* |

> ### ❗ **`tanh` DOMINA `Itô` SU OGNI ASSE**
> deriva **più piccola** *(zero contro quarto ordine)* · **monotona**, e Itô no · **stessa**
> fedeltà, anzi un po' migliore · tetto **meno restrittivo** *(`2` contro `1.6487`)*.
> **Quindi Itô esce dal confronto**: non c'è nessun asse su cui sia preferibile.

> ### **LA SCELTA VERA È FRA `piana` E `tanh`, e si riduce a UNA domanda:**
> **`piana` non ha tetto ma HA deriva. `tanh` non ha deriva ma SATURA a `2`.**
> **La decide la DISTRIBUZIONE di `|dx|/d`** — punti `V8`/`V9` — **e la decide Luca DOPO quella
> misura.** *(Non prima: senza quel numero non c'è una base derivata.)*

## 4-quinquies. ✅ **LA FORMA È DECISA — `1 + tanh(x)`** *(decisione di Luca, 2026-09-24)*

```
(d − LAM)  ←  (d − LAM) · (1 + tanh(dx / d))
```

### LA MISURA CHE L'HA DECISA — `V8`/`V9`, dal giro corto di `CURA 2`

*(`csv/_test_fork/_cura2_corto/BILANCIO_d0.txt`, blob `49fc54d2`, `120` passi, seme `42`)*

```
  verso                n        p50      p90      p99    p99.9      max   >0.5   >1   >2
  discese       60538734     0.0019   0.0239   0.0310   0.0344   0.0385    0.0  0.0  0.0
  salite        65192342     0.0024   0.0124   0.0241   0.0307   0.0531    0.0  0.0  0.0
```

> ### ❗ **IL SOLO DIFETTO DICHIARATO DI `tanh` — LA SATURAZIONE A `2` — NON SI PRESENTA MAI.**
> Il **massimo** su **`125 731 076`** campioni è **`0.0531`**: la saturazione conta a `x` di
> ordine `1`, e il massimo misurato è **`19` volte più piccolo**. **Zero campioni oltre `0.5`,
> su entrambi i versi.** Al massimo misurato le due forme differiscono di **`1.4e-03`
> relativo**.
>
> **Quindi `tanh` paga il suo unico prezzo ZERO VOLTE, e in cambio dà deriva ESATTAMENTE nulla.**

### ⚠ E IL CONFRONTO NON È SIMMETRICO, PERCHÉ SULL'ALTRO PIATTO IL NUMERO MANCA

La deriva di `piana` vale `exp(N·E[x²]/2)`, e **`E[x²]` NON È STATO REGISTRATO** — l'involucro
ha salvato **quantili**, `max` e quote, **e i quantili non bastano a stimare una media di
quadrati** *(`csv/_test_fork/_z146_scelta_freno.py`)*:

| ipotesi su `sqrt(E[x²])` | 120 passi | 1200 passi | 6000 passi |
|---|--:|--:|--:|
| `= p50 (0.0024)` | `+0.03 %` | `+0.35 %` | `+1.74 %` |
| `= p90 (0.0124)` | `+0.93 %` | `+9.66 %` | `+58.61 %` |
| `= p99 (0.0241)` | `+3.55 %` | `+41.69 %` | `+471.12 %` |

> **A `120` passi la scelta è indifferente in ogni ipotesi. A `6000` l'intervallo va da
> `+1.7 %` a `+471 %`: TROPPO LARGO per decidere.**
>
> ### **E LA DECISIONE NON NE È INDEBOLITA — È ANZI IL SUO ARGOMENTO PIÙ FORTE:**
> **il costo di `tanh` è MISURATO e vale zero; il costo di `piana` è NON MISURATO e il suo
> intervallo arriva a un fattore.** **Si sceglie la forma il cui prezzo si conosce.**

### ⚠ COSA RESTEREBBE DA MISURARE, e costa **ZERO run in più**

Registrare **`mean((dx/d)²)`** nello stesso involucro che già registra i quantili: **è una somma
in più, sugli stessi campioni.** **Non cambia la decisione** — servirebbe a sapere **di quanto**
`piana` sarebbe stata peggiore, non **se**. **→ in coda.**

### ⚠ E LA DECISIONE PORTA IL SUO REGIME, come ogni numero di questo repo *(`9-bis`)*

`|dx|/d ≤ 0.053` è misurato a **`120` passi**, su **un seme**, con `--sep 4.0`. **Se un giorno
`|dx|/d` si avvicinasse a `1`, la saturazione di `tanh` comincerebbe a mordere e questa
decisione andrebbe RIFATTA, non difesa.**
**IL CRITERIO CHE LA RIAPRE, scritto ORA e non dopo** *(`par.10`: la condizione di retrocessione
si scrive al momento della promozione)*:
### **una quota NON NULLA di `|dx|/d > 0.5`.**

## 5. ❌ **PERCHÉ NON `exp(dx/u)`** — la variabile `log(d − LAM)`

La scelta «naturale» sarebbe far evolvere **liberamente** `log u`, cioè `u ← u·exp(dx/u)`.
**È SBAGLIATA, e il motivo è un conto:** vicino al confine `u → 0`, quindi **una spinta in su
piccola diventa un salto enorme** — `exp(a/u) → ∞`. **Una spinta LIMITATA produrrebbe uno
spostamento ILLIMITATO**, che è la firma di `A11`.

**Con `exp(dx/d)` non succede**, perché `d ≥ LAM > 0` **per legge**, quindi l'esponente è
**limitato da `|dx|/LAM`**.

> **Era una mia proposta, e Luca l'ha corretta prima che diventasse codice.** Sta qui perché
> **il codice di una via scartata non si cancella: e' l'evidenza che spiega perché esiste
> quella scelta** *(par.10)*.

## 6. I LIMITI, CLASSIFICATI CON `A11`

| limite | oggi | con la proposta |
|---|---|---|
| `max(0.0, 1.0 - LAM/base)` | **protegge il FATTORE** dal diventare negativo quando `d < LAM` — cioè **da uno stato che `E4-LAM` ora VIETA** | **SPARISCE**: `d ≥ LAM` è un invariante verificato **sempre**, quindi `1 − LAM/d ≥ 0` è **derivato** |
| `pos = prima > 0` | protegge da `d = 0` | **SPARISCE per la stessa ragione**: `d ≥ LAM > 0` |
| *(nuovo)* overflow di `exp` | — | **NESSUN CLAMP.** `|dx|/d ≤ |dx|/LAM`, e se mai superasse `709` è **`np.seterr(over='raise')`** a fermarsi **con la riga** — la stessa scelta di `E4-LAM` |

> **Due limiti spariscono e nessuno nasce**, e questa volta **l'ho verificato** invece di
> dirlo *(è l'errore di `Z142`)*: entrambi proteggevano da `d < LAM`, che **ora è un
> invariante**.

## 7. LA VERIFICA, **sulla FORMULA, col test di `Z113`**

**Non un run: un conto**, come `Z113`. Lo strumento deve mostrare:

| | che cosa | criterio |
|---|---|---|
| **`V1`** | **quanto vale `a`**, il passo tipico di rumore, **misurato** | è il numero che decide la condizione `a < LAM` del par.4 |
| **`V2`** | la deriva di **oggi** sotto rumore simmetrico | deve **riprodurre `Z113`**: `≈ +1.582e-03` con i suoi parametri |
| **`V3`** | la deriva della **proposta**, stessa `a`, stessi `d` | deve essere **del secondo ordine**: raddoppiando `a` deve **quadruplicare**, non raddoppiare |
| **`V4`** | la deriva della proposta **al confine** *(`d → LAM`)* | **→ 0**, mentre quella di oggi **→ `a/2`** |
| **`V5`** | la deriva della proposta **lontano** | decade come `1/d` in assoluto, `1/d²` in relativo |
| **`V6`** | **il caso che DEVE fallire**: la forma `exp(dx/u)` | deve **esplodere** vicino al confine, e il test lo deve **mostrare** |
| **`V7`** | **mai sotto `LAM`**: una discesa enorme, `dx = −100·d` | oggi **attraversa**; la proposta **no**, per qualunque passo |
| **`V8`** | **la DISTRIBUZIONE di `\|dx\|/d`**, non solo il suo tipico | è **il numero che decide fra piana e Itô**: `p50`, `p99`, `max`. Se `max ≪ 1` la non-monotonia di Itô **non si manifesta mai** |
| **`V9`** | **quante scritture hanno `\|dx\|/d > 1`, e quante `> 2`** | `> 1`: Itô **comprime**; `> 2`: Itô **inverte il verso**. **Se sono zero, la scelta è libera; se non lo sono, la piana è l'unica monotona** |

## 8. COSA NON SO DERIVARE — **dichiarato** *(`A12` regola 4)*

1. **che la deriva residua di secondo ordine sia TRASCURABILE.** So che è di second'ordine,
   nulla al confine e decrescente lontano. **Non so derivare che su `600` passi e `526` mila
   archi non si accumuli**: è una misura, non un teorema;
2. **il valore di `a`**, il passo tipico di rumore. **Senza, la condizione `a < LAM` non si può
   dichiarare vera** — ed è il punto `V1`;
3. **se la stessa forma vada applicata a `d0` come a `d`.** `_smorza` è chiamata per **entrambi**
   *(`quale` ∈ `{d, d0, d0_passo, …}`)*, e `d0` è una lunghezza di **riposo**: che debba obbedire
   alla stessa legge è **plausibile, non derivato**;
4. **chi spinge gli archi contro il muro.** La proposta toglie **il cricchetto del freno**, non
   la **causa** per cui gli archi ci arrivano. **Resta aperta e SEPARATA:** `D33` e `S05`.
5. ~~**se la SATURAZIONE di `tanh` a `2` si manifesti davvero**~~ — **RISOLTO il 2026-09-24**: **non si manifesta**, `max |dx|/d = 0.0531` su `125 731 076` campioni, **zero oltre `0.5`** *(par.4-quinquies)*. **Resta aperto `E[x²]`**, che non ho registrato e che direbbe **di quanto** `piana` sarebbe stata peggiore. Dipende da `\|dx\|/d`, che **non è
   misurato** — punti `V8`/`V9`. **Senza quel numero la scelta fra le due forme non ha una
   base derivata**, e resta di Luca;
6. **se una deriva NEGATIVA di quarto ordine sia preferibile a una POSITIVA di secondo.** È
   più piccola di ordini di grandezza, **ma va verso il muro** — e la domanda «chi spinge gli
   archi contro il muro» è un fronte aperto. **Più piccolo non è automaticamente meglio quando
   il SEGNO cambia.**

> **E la cosa più importante, che non va persa:** **questa cura NON elimina la deriva. La
> abbassa di un ordine e la annulla dove oggi è massima.** Dire *«il cricchetto sparisce»*
> sarebbe falso: `cosh(x) ≥ 1` sempre, quindi `E[Δu] ≥ 0` **sempre**. **Cambia l'ORDINE, non il
> segno.**

