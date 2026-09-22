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

---

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
