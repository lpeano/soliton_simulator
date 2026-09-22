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
**⚠ Oggi NON è cablata, e va detto invece di darla per fatta** *(`A9`)*: l'hook rifiuterebbe ogni
commit al simulatore finché le schede non esistono.

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
| **4 — SIMMETRICO** | ❌ **VIOLATO.** Frena **solo** le discese. **È il cricchetto.** |
| **5 — si ripara all'origine** | ⚠ **DA DECIDERE:** il freno sta nel punto d'uso. **Dove nasce la discesa che va frenata?** |
| **6 — se satura è un allarme** | ⚠ i contatori **esistono** *(`_g_sm_discese`, `_g_sm_patol`, `_g_sm_viol_*`)*; **la frazione di saturazione non è mai stata letta in un referto.** Lavoro residuo. |
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

- **la frazione di SATURAZIONE del freno non è mai stata letta** *(`A11` cor.6)* — i contatori
  esistono, il referto no. **È il punto 5 del mandato dei sospesi:** distribuzione di `d0/LAM` e
  **test del cricchetto** su rumore simmetrico sintetico;
- **`A11` cor.5:** dove nasce la discesa che il freno trattiene? **Non è stato cercato.**
