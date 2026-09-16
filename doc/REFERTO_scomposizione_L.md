# REFERTO — DA DOVE VIENE LA CRESCITA DI `L_tot`

> **2026-09-16.** Blob **`c57800c1`** (byte grezzi, 0 CRLF). Branch `fork-su2`.
> **Nessun run nuovo, nessuna modifica alla fisica.** Dati: i 4 CSV della baseline.
> Predizione scritta e committata **prima**: `doc/PREDIZIONE_scomposizione_L.md` (`5fe79cd`).
> Calcolo: `csv/_test_fork/_scomposizione_L.py` -> `_scomposizione_L.txt`.

---

## 0. IL VERDETTO IN UNA RIGA

> ### **DOMINA `A`: e' l'INERZIA che cresce, non `omega`.**
> ### Peso di `A`: **89.6 % · 93.0 % · 97.7 % · 99.7 %** sui quattro run.
> ### **`L_tot` non e' una violazione di conservazione: e' un sistema che non ha finito di accendersi.**

**La predizione scritta prima e' CONFERMATA**, e con un margine che non lascia spazio al terzo caso.

---

## 1. LA SCOMPOSIZIONE

`L_tot ~ n * <I*|omega|>`, quindi `d log(L/n) = d log(I) + d log(|omega|) + misto`.
Dal primo campione utile (passo 50) all'ultimo (passo 500):

| run | `d log(L/n)` | **`A` = `d log(Lam)`** | **`B` = `d log RMS(omega)`** | misto | **peso di `A`** |
|---|---|---|---|---|---|
| OFF s1 | +4.703 | **+6.032** | **+0.702** | −2.032 | **89.6 %** |
| OFF s2 | +4.833 | **+7.253** | **+0.549** | −2.968 | **93.0 %** |
| ON s1 | +1.859 | **+5.931** | **+0.142** | −4.214 | **97.7 %** |
| ON s2 | +2.308 | **+7.301** | **−0.019** | −4.974 | **99.7 %** |

**In fattori moltiplicativi su 450 passi:**

| run | `Lam` (~ inerzia media) | `RMS(omega)` |
|---|---|---|
| OFF s1 | **x416** | x2.02 |
| OFF s2 | **x1412** | x1.73 |
| ON s1 | **x376** | x1.15 |
| ON s2 | **x1481** | **x0.98** |

> **Nel braccio ON `omega` e' PIATTO o in leggero CALO** (`x1.15`, `x0.98`) **mentre l'inerzia
> cresce di tre ordini di grandezza.** Non c'e' nessuna sorgente che pompa momento angolare:
> **c'e' un campo che si accende.**

**Dispersione FRA SEMI** (P3, mai la `SE` interna): peso di `A` **89.6 / 93.0 %** (OFF) e
**97.7 / 99.7 %** (ON). *Con 2 semi `t(0.025,1) = 12.706` e nessun IC95 decide — ma qui non serve
un IC: la separazione fra `A` e `B` e' di **un ordine di grandezza**, non di una deviazione
standard.*

---

## 2. LA PROVA INDIPENDENTE: `I` MEDIANA ERA INCOLLATA AL PAVIMENTO

| run | l'inerzia mediana lascia il floor `1e-6` al passo | valore a 500 |
|---|---|---|
| OFF s1 | **350** | 2.29e-6 |
| OFF s2 | **250** | 4.12e-6 |
| ON s1 | **350** | 2.58e-6 |
| ON s2 | **250** | 4.14e-6 |

**Per meta' run il nodo TIPICO e' stato al pavimento**, cioe' con un'inerzia che **non e' una massa
ma una regolarizzazione** (§9). **Ne e' uscito solo negli ultimi 150-250 passi.**
**Un sistema il cui nodo tipico ha appena acquisito una massa non e' un sistema a regime.**

---

## 3. ⚠ IL CONTROLLO §3.2: **INTENSIFICAZIONE, non aggregazione** — e di molto

| run | `n` | `L_tot` | **`L_tot/n`** |
|---|---|---|---|
| OFF s1 | x2.01 | x222 | **x110** |
| OFF s2 | x1.51 | x190 | **x126** |
| ON s1 | x1.97 | x12.7 | **x6.4** |
| ON s2 | x1.59 | x16.0 | **x10.1** |

`n` cresce di **1.5-2 volte**, `L_tot/n` di **6-126**: **la crescita e' quasi tutta
INTENSIFICAZIONE**. Il totale, da solo, non lo avrebbe distinto.

**⚠ E QUI UN FATTO CHE NON AVEVO PREVISTO:** `L_tot/n` cresce **x110-126** mentre `Lam` cresce
`x416-1412` e `RMS(omega)` `x2`. **Il prodotto delle mediane non si avvicina neanche**
(`I` mediana **x2.3-4.1**, `omega` mediano **x0.5-1.9**). **Quindi la crescita di `L_tot` sta nella
CODA, non nel nodo tipico**: poche unita' con `I*|omega|` grandissimo dominano la somma.
*(E' anche la ragione per cui la scomposizione con le MEDIANE non chiude — vedi §5.)*

---

## 4. CONTROLLO §3.1 — la popolazione non perde nodi

**Zero intervalli con `n` in calo**, su tutti e quattro i run: nessuna rimozione o fusione fra
campioni. `Delta L` mescola **crescita** e **aggiunta**, mai **crescita** e **rimozione**.
**E' il caso piu' semplice da leggere — ma NON isola i passi birth-free**, che restano non
scomponibili dai dati committati (§0 della predizione).

---

## 5. ⚠ DUE ERRORI MIEI IN QUESTO STESSO LAVORO, entrambi dichiarati

### 5.1 — La prima scomposizione NON CHIUDEVA, e il difetto era del metodo

Avevo scomposto con le **MEDIANE** di `I` e `omega` contro `L/n`, che e' una **MEDIA**.
**Le mediane non si moltiplicano per dare la media:** il termine misto assorbiva **tutto** lo
scarto (dell'ordine del totale), e la scomposizione era **illeggibile**.
**Corretto** usando statistiche **commensurabili**: `Lam` (media di `|psi|^2`) e `RMS(omega)`
(da `fdt_om2_media`). **Il tentativo fallito resta nello script**, dichiarato.

**E il misto resta grande e NEGATIVO anche cosi', con due cause note nello stesso verso:**
1. `Lam` e' media di `rho`, ma l'inerzia ha un **floor** `1e-6`: finche' molti nodi sono al floor,
   `media(inerzia) > Lam` e converge verso `Lam` **dall'alto** -> **`Lam` SOVRASTIMA** la crescita
   dell'inerzia media;
2. `I` e `omega` sono **anticorrelati** (pendenza **−1.056**, C1), quindi `media(I*omega)` cresce
   **meno** di `media(I)*RMS(omega)`.

> **Quindi `A` e' semmai SOVRASTIMATO. Ma `B` e' misurato DIRETTAMENTE ed e' ~0**, e la conclusione
> *«non e' `omega` che cresce»* **non dipende** dalla sovrastima di `A`.

### 5.2 — Ho quasi distrutto i riferimenti dei sigilli

Ripulendo i caratteri non-cp1252 dagli script ho passato un `glob` su **tutti** i `.py` di
`csv/_seal_fork/` e `csv/_test_fork/`, toccando anche i **`_old_sim_pre_*.py`** e i
**`._sim.py`** — che sono **copie BYTE-ESATTE** e il cui unico valore e' il blob.
**Ripristinati subito** da `git cat-file -p` in binario, e **verificati uno per uno**:
`a467fd9a`, `08784685`, `968fba34`, `2277e9a0`, `7d484580`, `b298677a`, `f5887254` — tutti tornati
al valore atteso, **zero differenze di contenuto residue**.
**La lezione, e non e' nuova:** uno script di pulizia che gira su un `glob` **non sa quali file
sono dati e quali sono codice**. I file-riferimento andrebbero marcati come tali.

### 5.3 — E un fatto emerso ripristinando: **l'evidenza CRLF non e' mai entrata in git**

I tre `._sim.py` erano stati committati come **prova** del file CRLF (442240 byte, sha1 grezzo
`37c31630`). **Ma il blob storato e' `08784685`, 435730 byte, ZERO CR.**
**Il filtro `clean` di git ha normalizzato la prova al momento del commit.**

> **Non si puo' committare un file per il suo essere CRLF: git lo normalizza entrando.**
> I tre `._sim.py` nel repo sono **identici al riferimento** e **non portano informazione**.
> **L'unico record superstite del `37c31630` e' il `.motivo.txt` scritto a mano** — che si e'
> rivelato non un di piu', ma **l'unica prova possibile**.

---

## 6. COSA QUESTO REFERTO NON DICE

1. **Non dice nulla sui passi birth-free in particolare.** La separazione `con/senza nascite`
   del referto della baseline resta un fatto misurato, ma la sua **scomposizione** richiede la
   serie **per passo**, che **non e' nei dati**. **Serve un run**, e lo si dice invece di fingere.
2. **Non dice che la conservazione sia rispettata.** Dice che **la domanda e' mal posta adesso**:
   la conservazione si giudica **a regime**, e a 500 passi il sistema ha vissuto **un decimo**
   della propria maturazione (`ramp = min(1, eta/TAU_A)` arriva al pieno a ~5000 passi, `:2321`).
3. **Non dice perche' la crescita stia nella CODA** e non nel nodo tipico. **E' un fatto nuovo,
   emerso qui, e non e' spiegato.**

---

## 7. LA MINIMA COSA CHE CHIUDEREBBE LA DOMANDA (non fatta, dichiarata)

Persistere `serie_L` **per passo** (`passo`, `n`, `L_tot`, `sum(I)`, `sum(|omega|)`) in un CSV a
parte: **una riga di scrittura** nell'osservatore, **zero fisica**. Renderebbe la scomposizione
`A`/`B` **esatta e ristretta ai birth-free** al **prossimo** run — senza lanciarne uno apposta.
