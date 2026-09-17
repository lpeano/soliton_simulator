# REFERTO — I GATE DELLA BONIFICA. **Due premesse del mandato non reggono, e una si ribalta.**

> **2026-09-17.** Branch `fork-su2`, blob **`827d3bf8`** (coincide con `HEAD`, byte grezzi, 0 CRLF).
> **NESSUN RUN DI MISURA.** I gate girano sui **`.pkl` gia' committati**; l'unica esecuzione e' il
> calcolo di distribuzioni su dati esistenti. **Nessun cablaggio eseguito.**
> Strumento: `csv/_test_fork/_gate_bonifica.py` -> `_gate_bonifica.txt`.
>
> **Ordine del mandato (§7.2): «GATE A, B, C, D -> STOP e riporta.»** E' quello che fa questo file.

---

## 0. IL VERDETTO IN QUATTRO RIGHE

> 1. **GATE A — PASSA.** `rho_sorgente/peq_nodo` ha struttura, e della stessa forma del caso
>    positivo noto `I/Lam`. **La correzione ① e' licita.**
> 2. **GATE B — risolto.** La proiezione arco->nodo esiste gia' nel codice, e **non degenera**.
> 3. **⚠ GATE C — la premessa di ⑤ e' VERA ma IRRILEVANTE: il clamp e' su CODICE MORTO.**
>    `spin_locale` **non e' mai chiamata**. E la conseguenza temuta — *«`dt_n` era clampato»* —
>    **e' FALSA**: `dt_n` non passa di li'.
> 4. **⚠⚠ GATE D — la premessa di ⑥ e' FALSA, e il difetto e' ESATTAMENTE L'OPPOSTO.**
>    Non *«`fattore = 1.0` su meta' degli archi»*: **0.13 %**. Il fattore mediano vale **8.8e+05**.
>    **La plasticita' non e' spenta a meta': e' congelata quasi ovunque.**

---

## 1. GATE A — `rho_sorgente / peq_nodo` HA STRUTTURA. ① e' licita.

*(4 semi, 500 passi, ~13 300 nodi. Il criterio: concentrata su 1 -> la correzione cade.)*

| grandezza | mediana | p05 | p95 | **p95/p05** | IQR/med | frazione >1 |
|---|---|---|---|---|---|---|
| **`I / peq_nodo`** | **7.5e-04** | 1.1e-05 | 5.37 | **4.86e+05** | 2.2e+03 | **34.9 %** |
| *[SI' noto] `I / Lam`* | 3.2e-04 | 7.1e-06 | 3.98 | 5.63e+05 | 7.4e+03 | 33.5 % |
| *[NO noto] `I / median(I)`* | **1.0000** | 0.023 | 1.3e+04 | 5.46e+05 | 7.5e+03 | **50.0 %** |

> **La riga da leggere e' la mediana, non la dispersione.** Tutte e tre hanno `p95/p05 ~ 5e5`:
> **la larghezza non distingue**. Cio' che distingue e' **dove sta il centro**:
> `I/median(I)` vale **1 esatto** e ha il **50.0 %** sopra 1 — *e' la definizione di mediana*,
> non un fatto sul sistema. `I/peq_nodo` ha mediana **7.5e-04** e il **34.9 %** sopra 1:
> **il nodo tipico e' lontano dal proprio sfondo, e in modo misurabile.**
>
> **`peq` si comporta come `Lam`, non come `median(I)`. GATE A PASSA.**

---

## 2. GATE B — la proiezione ARCO -> NODO, e perche' non degenera

`peq` e' per **ARCO** (`:1855`, nasce `np.full(len(dd), nan)`), `inerzia` e' per **NODO**.

**Proiezione usata:** media di `peq` sugli archi **incidenti** al nodo
(`bincount(i, peq) + bincount(j, peq)`, diviso il grado). **Non e' una convenzione nuova:** e'
**la stessa forma** che il codice usa gia' a `:3140-3141` per `den_w`.

**E la verifica che conta e' gia' fatta:** il GATE A e' stato misurato **sulla grandezza
proiettata**, non su `peq` grezzo. **La proiezione non introduce una media degenere.**

---

## 3. ⚠ GATE C — il clamp e' VERO, ma sta su CODICE MORTO

**La dimostrazione analitica del mandato regge**, e i dati la confermano:

| run | `r_min` | `r_p05` | `r_mediana` | `r_min < 0.01` ? |
|---|---|---|---|---|
| s2ON_s1 | 9.79e-04 | 0.1235 | 1.0000 | **si'** |
| s2ON_s2 | 7.61e-04 | 0.1156 | 1.0000 | **si'** |
| s2ON_s3 | **1.16e-04** | 0.0308 | 1.0000 | **si'** |
| s2ON_s4 | 4.35e-04 | 0.1371 | 1.0000 | **si'** |

`r` **scende davvero sotto 0.01** (fino a `1.16e-04`), e resta **sopra** il minimo analitico
`1.414e-06`: la protezione `+1e-6` dentro `ritmo()` fa il suo mestiere, come il mandato deduce.
*(E `r_mediana = 1.0000` su tutti e quattro: il punto fisso di C12, che infatti non misura nulla.)*

### 3.1 — MA `spin_locale` NON E' MAI CHIAMATA

```
grep -rn "spin_locale" --include=*.py .
  ./soliton_simulator.py:2324:    def spin_locale(self):        <- SOLO la definizione
  (piu' otto backup, tutti con la sola definizione)
```

**Il clamp `np.maximum(r, 0.01)` (`:2346`) vive dentro `spin_locale()`, che nessuno chiama.**

> **CONSEGUENZE, e la seconda e' la piu' importante:**
> 1. **Togliere il clamp e' corretto ma INERTE:** non cambia nessun risultato, perche' quel codice
>    non gira. Resta un'operazione di igiene — **e va dichiarata come tale**, non come una cura.
> 2. **La conseguenza temuta dal mandato e' FALSA.** Il mandato scrive: *«se scatta su una frazione
>    significativa, `dt_n` era clampato e tutto cio' che vive in tempo proprio girava in parte in
>    tempo di coordinata — tocca A4»*. **`dt_n` NON passa da li'**: e' costruito in `step`
>    (`dt_n = DT*r`, `:2851-2853`) **senza alcun clamp**. **Il tempo proprio non e' mai stato
>    tagliato.** *(Ed e' un sollievo, non un problema: sarebbe stato un difetto grosso.)*
>
> **Nota di categoria:** `spin_locale` e' **un terzo caso** della famiglia gia' catalogata —
> `_passo_spinoriale` docstring "ORFANO" ma **vivo**, `VERSO_CHI` cablato ma **muto**, e ora
> `spin_locale` **definito e mai chiamato**. **Il file contiene codice il cui stato di vita non e'
> leggibile dal codice stesso.**

---

## 4. ⚠⚠ GATE D — LA PREMESSA DI ⑥ E' FALSA, E IL DIFETTO E' L'OPPOSTO

**Il mandato afferma:** *«`rho_arco/rho_med ~ 1` per l'arco tipico, e il `max(...,0)` taglia a zero
da sotto -> `fattore_elasticita = 1.0` ESATTAMENTE, per costruzione, su META' degli archi.
Non "circa 1": esattamente.»*

**MISURATO (4 semi, ~840 000 archi):**

| | valore |
|---|---|
| archi con `fattore_elasticita = 1.0` esatto, **OGGI** | **0.13 %** |
| archi con `fattore = 1.0` esatto, **con `peq`** | **0.27 %** |

> ### **Non e' meta': e' lo 0.13 %. La premessa non regge.**

### 4.1 — Perche', ed e' un errore di POPOLAZIONE

`rho_med = median(I_NODI)` e' la mediana sui **NODI**; `rho_arco = 0.5*(I[i] + I[j])` vive sugli
**ARCHI**. Su una distribuzione a coda pesante la **media di due nodi** e' dominata dal maggiore dei
due, quindi l'arco tipico sta **molto sopra** la mediana nodale. Misurato:

| | p05 | **mediana** | p95 | max |
|---|---|---|---|---|
| `rho_arco / median(I_nodi)` | 5676 | **8830** | 1.50e+04 | 2.30e+04 |

**L'arco tipico non sta a 1: sta a quasi NOVEMILA.**
*(La mediana di un rapporto e' 1 solo se numeratore e denominatore vivono sulla STESSA popolazione.
Qui non ci vivono, ed e' il motivo per cui il punto fisso di C12 **non** si forma.)*

### 4.2 — E qui il difetto vero, che e' l'OPPOSTO di quello ipotizzato

Con `ELAST_C = 100`:

| `fattore_elasticita` | p05 | **mediana** | p95 | max |
|---|---|---|---|---|
| **OGGI** | 5.68e+05 | **8.83e+05** | 1.50e+06 | 2.30e+06 |
| **con `peq`** | 24.87 | **234.8** | 543.2 | 1711 |

`tau_p_loc = (d_arco/cs) * fattore_elasticita`, e `d0 += dt_e*(d - d0)/tau_p_loc`.

> ### **Il fattore mediano vale QUASI UN MILIONE. La plasticita' delle `d0` non e' "spenta a meta'":**
> ### **e' CONGELATA quasi ovunque**, perche' il tempo di rilassamento plastico e' ~`10^6` volte
> ### il tempo-luce dell'arco.
>
> **Con `peq` il fattore mediano scende a 235: circa 3760 volte piu' piccolo.** La correzione ⑥
> **non "accende un correttivo spento": SGONFIA un correttivo esploso.**

### 4.3 — Cosa resta in piedi di ⑥, e cosa no

- **CADE** la motivazione scritta nel mandato (*«spento per costruzione su meta' degli archi»*).
- **RESTA IN PIEDI**, e non e' poco: `median(I_nodi)` e' una **statistica GLOBALE** su un percorso
  fisico — la **Legge I** (`:265`, *«NESSUNA SCORCIATOIA GLOBALE»*) e §4. `peq` e' **per arco** e
  **locale**. **Su questo asse ⑥ e' giustificata esattamente come prima.**
- **⚠ MA L'EFFETTO E' GRANDE, NON COSMETICO:** un fattore mediano che passa da `8.8e+05` a `235`
  **cambia di tre ordini e mezzo il tempo di rilassamento plastico dello spazio**. **Non e' una
  ripulitura: e' una modifica di regime**, e va trattata come tale.

---

## 5. LE VERIFICHE PRELIMINARI (§7.1) — due ostacoli STRUTTURALI, da decidere

### 5.1 — ③ `_floor_d0`: **non ha accesso ne' a `cs` ne' a `dt_e`**, e restituisce uno SCALARE

```python
def _floor_d0(self):                       # :2476  -- NESSUN argomento
    if not PAV_COM or not len(self.d0):
        return 0.05                        # ramo A: costante assoluta
    f = 0.05 / LAM_BASE
    return f * float(np.median(self.d0))   # ramo B: SCALARE, mediana GLOBALE
```

| ostacolo | stato verificato |
|---|---|
| **`cs` non e' raggiungibile** | `cs_arco` e' **locale a `step`**, mai su `self` (esiste `_cs_nodo_prev`, che e' per NODO e di **un passo fa**) |
| **`dt_e` non e' raggiungibile** | costruito a **`:2853`** (`dt_e = DT*0.5*(r[i]+r[j])`, **per ARCO**) e **mai memorizzato** |
| **il ritorno e' uno SCALARE** | `cs_arco*dt_e` e' **per ARCO**: cambierebbe la **forma** del valore di ritorno |
| **sette punti di chiamata** | `:3261`, `:3365`, `:3763`, `:3830`, `:3841`, `:3883`, `:3922` |
| **quale ramo si sostituisce** | **non e' deciso dal mandato.** Sostituirli **entrambi** rende `PAV_COM` **inerte** — e `--pav-com` e' nella config della campagna |

> **NON e' una riga.** Richiede: rendere `cs` e `dt_e` disponibili (snapshot su `self`, **mai
> ricalcolo** — precedente `lambda_vuoto`/`calcola_psi`), accettare un ritorno per-arco su sette
> chiamanti, **e una decisione su `PAV_COM`.** **Non lo cablo senza quella decisione.**

### 5.2 — ④ `_rep`: `mitosi()` **non riceve `dt_e`**, e gli archi non hanno un "padre"

```python
def mitosi(self):        # :3263  -- NESSUN argomento: niente dt_e, niente dt_n
    ...
    tau_pp = 1.0 + avv / PHI_CRIT          # :3343  per ARCO, DISPONIBILE. OK.
    rep = np.clip(-resp, 0.0, 1.0)         # :3359  per ARCO
    if rep.any() and len(self.d0) == len(avv):     # <- guardia NON CONTATA (P5)
```

| punto | stato |
|---|---|
| **`tau_pp`** | **c'e'**, per arco, riga `:3343`. La proposta del mandato e' realizzabile |
| **`dt_e`** | **NON c'e'** in `mitosi()`. Va portato (snapshot su `self` in `step`) |
| **`_rep` alla nascita degli archi** | **NON e' «il figlio eredita da `src`»**: `_rep` e' per **ARCO**, e gli archi nascono in piu' punti. Il **pattern corretto e' gia' nel codice**: `peq` si estende con `np.full(len(dd), np.nan)` a `:1855`. **Quello e' il modello da copiare**, non l'eredita' nodale |
| **la guardia `len(self.d0) == len(avv)`** | **fallback non contato** (P5). Va strumentata **prima**, per sapere quante volte l'intero blocco repulsivo **non gira affatto** |

---

## 6. DOVE SIAMO, E COSA NON HO FATTO

| correzione | stato dopo i gate |
|---|---|
| **① `inerzia`** | **GATE A e B superati. Licita.** Non cablata (l'ordine dice STOP) |
| **② `spinta`** | nessun gate richiesto; nessun ostacolo trovato |
| **③ pavimento `d0`** | **BLOCCATA da una decisione**: quale ramo di `PAV_COM`, e come portare `cs`/`dt_e` |
| **④ memoria su `rep`** | realizzabile, **ma serve `dt_e` in `mitosi()`** e l'estensione di `_rep` alla nascita degli ARCHI |
| **⑤ clamp su `r`** | **igiene su codice morto.** La conseguenza temuta e' **falsa** |
| **⑥ `fattore_elasticita`** | **la premessa e' falsa; la giustificazione di LOCALITA' regge; l'effetto e' di TRE ORDINI E MEZZO** |

**NON ho cablato nulla. NON ho lanciato run di misura. NON ho scritto predizioni numeriche.**
**NON ho misurato ne' riportato:** `chi`, `|<n>|`, autocorrelazione, `theta`, `omega/sqrt(n)`,
`L_tot`, MISURA U, `cs_std/cs`.

**Una dichiarazione di provenienza, perche' conta:** i `.pkl` dei gate sono del blob **`a44adc31`**
(la campagna `csrel` e' stata fermata prima della scrittura del DB). Per una domanda **strutturale**
— *«questo rapporto ha una distribuzione, o vale 1 per costruzione?»* — e' adeguato, e il
`cs_floor` relazionale cambia i **valori**, non la **forma** della domanda. **Ma va detto, non
assunto.**
