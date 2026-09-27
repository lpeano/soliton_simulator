# `VIDEO-SCENA` — **far VEDERE la scena del pilota**, senza toccare la fisica

> **Richiesta di Luca, 2026-09-27**, da fare **INSIEME al giro che salva gli stati — un solo run**.
> **Criteri scritti e committati PRIMA del codice** (`CLAUDE.md` par.8).

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Che cosa si vede, e che cosa NON si vede — **va detto prima di girare**

**Il video mostra `pos`, che e' IL DISEGNO.** La fisica di questo repo vive **sugli ARCHI**: le
distanze sono `net.d` lungo il grafo, e `pos` **non entra nella dinamica** (`A3-DISEGNO`, ed e' il
senso della cura `POZZO_D`).

> ### ⚠ **QUINDI IL VIDEO PUO' MENTIRE SU UNA COSA PRECISA: la VICINANZA.**
> Due nodi possono apparire **vicini sullo schermo** ed essere **lontani sul grafo**, e viceversa.
> **La didascalia FISSA lo dice in ogni fotogramma** — *«posizioni = disegno (`A3-DISEGNO`), non
> distanze fisiche»* — **e non e' una formalita': e' l'unico presidio possibile su un'immagine.**

**Cosa il video mostra ONESTAMENTE, invece:** **la FASE**, che e' una grandezza di nodo e **non ha
niente a che fare con `pos`**. Il colore `cos(phi_k - dphi/2)` e' **la coerenza con la fase delle
masse**, ed e' **esattamente la grandezza che il pilota ha misurato crollare** *(`coer_campo`
`0.99877 -> 0.19555`)*. **Il video serve a VEDERE quel crollo**, non a giudicare le distanze.

### 1.2 ✅ Verificato dal sorgente

* il simulatore usa **`FFMpegWriter`** (`:8748`, `:8809`) con `w.saving(fig, out, dpi)` e
  `w.grab_frame()`: **stesso writer, stesso schema**;
* **`FFMpegWriter.isAvailable()` → `True`**, binario in `C:\ProgramData\chocolatey\bin\ffmpeg.EXE`.
  *(Se non ci fosse, il rendering **si ferma e lo dice**, invece di produrre un file monco.)*
* `dphi = net._dphi() = 4 pi` col driver *(`FASE_2PI` spenta)*, quindi **la fase delle masse e'
  `dphi/2 = 2 pi`**, che e' cio' che la scena scrive.

### 1.3 ⚠ Che cosa NON so

* **quanto pesano i fotogrammi.** `60` istanti × `n ~ 13 000` × (`pos` 3 float64 + `phi` 1) ≈
  **25 MB** in locale. **Si misura**, non si assume.
* **quanto costa il rendering** di `60` fotogrammi con `~13 000` punti. **Si misura.**
* **se `n` cresce durante il run** *(e cresce: `12 802 -> 13 444`)*, quindi **ogni fotogramma ha un
  numero di nodi DIVERSO**. Il rendering deve reggerlo, e **il bordo delle masse del passo 0 vale
  solo sui primi `n0` indici**.

---

## 2. PROGETTAZIONE — i criteri, **prima dei numeri**

### 2.1 Che cosa si salva, e dove

| | |
|---|---|
| **fotogrammi** *(solo seme `11`)* | **`pos` e `phi`**, **ogni 2 passi fino a 120** → `61` istanti *(`0, 2, …, 120`)* |
| **dove** | `csv/_test_fork/_pilota_prova1/stati/` — **gia' in `.gitignore`** (`STATI-LOCALI`) |
| **stati completi ai checkpoint** | `i`, `j`, `d`, `phi`, `n` a `0/40/80/120`, **tutti i semi**, **locali** |
| **in git** | **solo** `sha1` dei byte grezzi, **percorso** e **comando**, nell'inventario |

### 2.2 I criteri

| # | criterio | che cosa decide | che cosa mi fa FERMARE |
|--:|---|---|---|
| **`V1`** | **la fisica non cambia**: firme `sha1` campo per campo contro il braccio **senza** salvataggio, **2 semi**, `passo_pieno` | il salvataggio e' **diagnostico** | **un solo campo diverso**: allora il salvataggio **non e' inerte** e il run misurerebbe un altro sistema |
| **`V1b`** | **`n` fotogrammi attesi = `61`**, e `61` scritti | non si perdono istanti in silenzio | un conteggio diverso: si dice quale manca |
| **`V2`** | **la scala del colore e' FISSA `[-1, +1]` su TUTTI i fotogrammi** | un colore che si rinormalizza per fotogramma **mostrerebbe sempre lo stesso contrasto** e nasconderebbe il crollo | se la scala non e' fissa, il video **e' una bugia visiva** — ed e' `A3`, la stessa famiglia del *«normalizzato sulla propria mediana»* |
| **`V3`** | il **bordo** marca i nodi delle tre masse **del passo 0**, e **solo quelli** | si vede **chi era massa**, non chi lo sembra ora | se marcasse la regione **corrente**, il video mostrerebbe la definizione che il pilota ha gia' messo in dubbio (`MASSA-ID`) |
| **`V4`** | in sovrimpressione: **passo**, **`coer_campo` di ogni massa**, **`n_fase`** | i numeri **accanto** all'immagine, cosi' l'occhio non decide da solo | se un numero mancasse, il fotogramma non e' leggibile |
| **`V5`** | la **didascalia fissa** *«posizioni = disegno (`A3-DISEGNO`), non distanze fisiche»* **in ogni fotogramma** | l'unico presidio possibile su un'immagine | **se manca, il video non si consegna** |
| **`V6`** | **il costo**: MB dei fotogrammi, MB del video, secondi del rendering | non si assume che sia gratis | — |
| **`V7`** | **`sha1` e percorso** del video **nell'inventario**, col **comando** che lo rigenera | `STATI-LOCALI`: il dato **e'** il comando | se il video finisse in git, la regola e' violata |

### 2.3 ⚠ Le letture si fissano QUI

* **il colore e' `cos(phi_k - dphi/2)` con `dphi` preso da `net._dphi()`**, **mai** un `2 pi`
  scritto a mano — e' la stessa regola del periodo della fase;
* **`+1` = in fase con le masse, `-1` = in antifase.** La **colormap e' DIVERGENTE e centrata sullo
  zero**, cosi' il segno si legge a colpo d'occhio;
* **il video NON e' una misura e non entra in nessun referto.** E' un **diagnostico**: se mostrasse
  qualcosa che i numeri non dicono, **vincono i numeri** — e quella discrepanza diventa **una voce**,
  non una conclusione;
* **`H-P9` vale per il RUN**, che avanza con `passo_pieno`. **Il rendering e' offline, dai
  fotogrammi salvati**, e non avanza niente.

### 2.4 Che cosa questo task **NON** fa

**Non tocca il simulatore** *(il salvataggio sta nel braccio, il rendering e' uno script a parte)*,
**non cambia la fisica** *(`V1` lo prova)*, **non produce numeri nuovi**.

---

## 3. TODO DEL NEXT STEP

- [ ] il salvataggio nel braccio: stati completi ai checkpoint **+** `pos`/`phi` ogni 2 passi
      per il seme `11`, **tutti in locale**;
- [ ] `csv/_test_fork/_video_scena.py`: il rendering con `FFMpegWriter`, `V2`-`V5`;
- [ ] il sigillo `V1`/`V1b` **prima del run lungo** *(giro corto, `STANDARD 5`)*;
- [ ] **un run** *(4 semi, 120 passi)*, poi il rendering;
- [ ] inventario con `sha1` + percorso + comando di **video e stati**; relazione; **STOP**.
