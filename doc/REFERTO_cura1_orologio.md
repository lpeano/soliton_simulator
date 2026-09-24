# REFERTO — **`CURA 1`: L'OROLOGIO** *(giro corto, 120 passi)*

> **Sigillo `6/6`** *(`csv/_seal_fork/_sig_cura1/REFERTO.txt`)* · **giro corto `509.0 s`**
> *(`csv/_test_fork/_cura1_corto`)* · simulatore blob **`dd82794a`**, driver **`43ed085c`**,
> seme `42`.
> **Riferimento: `csv/_test_fork/_g4_riferimento` allo STESSO passo 120**, che ha girato
> **senza** la cura.

## 0. LA CURA GIRA DAVVERO — **letto dal referto di configurazione, non dedotto**

```
RITMO_WRAP_2PI                 False              True     <-- CAMBIATO
TW_SPINORE                     False              False
```

**`28` flag cambiati dall'argv su `123`.** È la prima volta che questo si legge da un file
invece di essere ricostruito: `csv/_test_fork/_cura1_corto/CONFIGURAZIONE.txt`.

**E il bilancio di `d0` CHIUDE: residuo relativo massimo `4.721e-14`.**

---

## 1. I NUMERI, al passo 120

| | senza la cura | **con la cura** | |
|---|--:|--:|---|
| `n` | `2647` | **`2660`** | `+0.49 %` |
| archi | `526282` | `526302` | `+0.004 %` |
| **mitosi** | `203` nati, `62` eventi | **`209` nati, `67` eventi** | `+3 %` / `+8 %` |
| **Schwinger** | `53` nati, `28` eventi | **`60` nati, `33` eventi** | `+13 %` / `+18 %` |
| `\|tw\|` mediana | `1.78474` | `1.78324` | `−0.08 %` |
| `\|tw\|` `p99` | `6.39139` | `6.34985` | `−0.65 %` |
| `\|tw\|` MAX | `34.34544` | `33.66720` | `−2.0 %` |
| **`r` mediana** | `1.018363` | **`0.680787`** | **`−33 %`** |
| `r` min | `0.000109` | `0.000578` | |
| `r` max | `1.414213` | `1.414213` | invariato *(il tetto)* |
| `r` al tetto | `0.76 %` | `1.02 %` | |
| `med d0` | `1.4150` | `1.3941` | `−1.5 %` |
| `med d/d0` | `0.8442` | **`0.8577`** | più vicino a `1` |

---

## 2. COSA SI LEGGE, e cosa NON si legge

### ✅ **LA MITOSI NON MUORE — ed è la differenza con `FASE_2PI`**

`FASE_2PI` da sola aveva portato la mitosi da **`62` a `1` evento** e Schwinger da **`28` a
`0`** *(`Z127`)*. **Qui la mitosi vive e cresce leggermente.** La ragione è nel grafo: la cura
tocca **`ritmo()`**, e `|tw|` — da cui dipende la mitosi — **resta praticamente invariato**
*(mediana `−0.08 %`)*. **È la conferma della correzione del grafo:** `tw` prende la sua scala da
`phi`, **non da `r`**.

### ✅ **L'UNICO EFFETTO SOPRA IL NULLO È SU `r`: mediana `−33 %`**

**E va letta insieme al nullo**, altrimenti non significa niente:

| grandezza | scarto misurato | nullo caotico noto |
|---|--:|---|
| `n` | `+0.49 %` | **`~1.4 %`** *(`Z21`)* → **sotto il nullo: NON attribuibile** |
| mitosi, eventi | `+8 %` | **non misurato** su questa grandezza → **non attribuibile** |
| Schwinger, eventi | `+18 %` | **non misurato** → **non attribuibile** |
| **`r` mediana** | **`−33 %`** | il gauge è deterministico, e `Z117` lo trovava **invariato** a 120 passi → **ATTRIBUIBILE** |

> **Quindi il referto dice UNA cosa sola con certezza: la cura abbassa `r`.** Tutto il resto è
> **dentro la dispersione di run**, a un seme, e va scritto come *«non misurato»*, non come
> *«nessun effetto»* né come *«migliora»*.

### 🟨 **E IL VERSO SMENTISCE IN PARTE `S09`**

`S09` ipotizzava: *la cura abbassa il gauge `median(|f|)`, quindi `x = f/med` **sale** per tutti
e **più nodi arrivano al tetto***.

**Misurato: `median(r)` SCENDE del `33 %`, e la quota al tetto SALE comunque** *(`0.76 %` →
`1.02 %`)*. **Le due cose insieme dicono che la distribuzione si ALLARGA**, non che si sposta:
la mediana cala e la coda al tetto cresce.

**`S09` resta aperto e va riformulato:** il meccanismo non è *«tutti salgono»*, è *«la
distribuzione si allarga»*. **Non lo inseguo adesso** *(`A12` regola 1)*.

### ⚠️ **COSA QUESTO REFERTO NON DICE**

- **non dice che la cura migliori il sistema.** `med d/d0` va da `0.8442` a `0.8577`, cioè
  verso `1`, ma **`+1.6 %` su un seme non è una misura**: è dentro la dispersione;
- **non dice niente su 600 passi.** Il giro è di **120**;
- **non dice niente su altri semi.** È **UNO**, e `P3` chiede `≥ 4` per una barra.

> ### **La cura resta giusta per la ragione con cui è nata, non per questi numeri**
> `D34` è **dimostrato sulla formula**: `max|w4(a) − a| = 0.000e+00` su `100 001` punti — un
> wrap su `4π` applicato a una differenza di `np.angle`, che ha periodo `2π`, **è l'identità e
> non avvolge niente**. **Lasciare un wrap che non avvolge non ha nessun argomento a favore**,
> e il giro corto serviva a misurare **quanto costa**, non a decidere **se farlo**.
> **Costa poco, e non rompe niente.**

---

## 3. `TW_SPINORE`: il blocco è provato, e non ritira nulla

| | |
|---|---|
| il rifiuto **scatta** con `--tw-spinore`, e **nomina la ragione** | `T4` **PASS** |
| e **non scatta** senza il flag | `T5` **PASS** — *è il controllo che rende `T4` leggibile* |
| **byte-inerte**: `206` campi identici, `0` diversi | `T6` **PASS** |
| nel run vero, `TW_SPINORE = False` | letto da `CONFIGURAZIONE.txt` |

**Non ritira nessuna misura:** `TW_SPINORE` era spento in **9 run su 11** ricostruibili e
`--tw-spinore` **non compare in nessun lanciatore committato**.
