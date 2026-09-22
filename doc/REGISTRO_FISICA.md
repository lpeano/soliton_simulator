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

<!-- SCHEDA nome=tempo-proprio funzioni=ritmo flag=TAU_LOC,TEMPO_SEGNO,TEMPO_PROPRIO_ORIENTATO,RITMO_WRAP_2PI -->
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
