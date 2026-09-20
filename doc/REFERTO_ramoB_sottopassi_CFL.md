# REFERTO — **il ramo B rallenta perche' `nsub` esplode, e lo tira `|vd|.max()` su POCHI archi**

> **Catturato a run VIVO il 2026-09-20, con `py-spy`.** Nessun processo e' stato ucciso, nessun file
> del percorso in uso e' stato toccato. Dati grezzi: `csv/_test_fork/_diag_B/stack_B_1809.txt`.
> **Simulatore `edb8f844` (blob git `b44f50ce`), invariato dal lancio.**

---

## 1. IL FATTO — **A e' piatto, B raddoppia e poi quadruplica**

Costo **per intervallo** *(la derivata di `elapsed`, non la media cumulata)*:

```
ramo A   26.9  26.8  28.0  26.4  26.8  26.9  26.9  27.2  ...  28.0      PIATTO su 215 frame
ramo B   25.1  40.5  84.2  41.0  129.8  121.0  274.3                    x11 in 25 frame
```

**⚠ E UNA PARTE DEL PRIMO PICCO E' MIA, va detto subito:** i valori `40.5` e `84.2` (frame 35-40)
cadono nella finestra in cui stavo girando il controllo delle componenti *(scipy su 527k archi)* e
un `git log -S` su tutto il repo. **Ho consumato CPU ai run.**
**Ma cio' che viene DOPO non e' mio:** a quel punto avevo smesso, **e il ramo A e' rimasto piatto a
`28.0` per tutto il tempo.** Un contendente di CPU avrebbe rallentato **entrambi**.

---

## 2. LO STACK — **sei campioni, tutti nello stesso punto**

```
py-spy dump --pid 30996   (ramo B, VIVO)
  campioni: :3967  :3937  :3935  :3943  :3936  :3933      -- tutti in `step`, nessun frame piu' profondo
```

**Sono tutte e sei dentro il corpo del ciclo `for _ in range(nsub)` di `:3931`** — il **ciclo dei
SOTTOPASSI CFL** del ramo `VERLET`.

> **Il processo non e' bloccato: sta ITERANDO.** E' la differenza fra *«fermo»* e *«lento»*, e
> l'unico modo di saperlo era guardare lo stack.

---

## 3. PERCHE' — **`nsub` e' un `max()`, e basta UN arco a tirarlo**

```python
:3920   nsub = int(max(4, n1, n2, n3))
:3922   n1 = ceil(|src|.max()  * DT / (0.05 * cs_max))
:3923   n2 = ceil(max(beta)    * DT / 0.5)
:3924   n3 = ceil(|vd|.max()   * DT / (0.1 * median(d) * cs_max/CS_M))
```

**Il costo di un passo e' PROPORZIONALE a `nsub`**, e `nsub` e' un **massimo su tutti gli archi**.

**MISURATO dagli snapshot gia' su disco** *(nessun run toccato; `src` e `beta` non sono salvati,
quindi si ricostruisce solo `n3` — ed e' gia' sufficiente)*:

| ramo | passo | `n` | `\|vd\|.max` | `median(d)` | **`n3`** | `\|vd\|` **p99** |
|---|---|---|---|---|---|---|
| **A** | 120 | 2672 | 3.354 | 1.186 | **1** | 1.334 |
| **A** | 600 | 2856 | 3.767 | 2.600 | **1** | 0.786 |
| **A** | 1200 | 4598 | 2.620 | 2.585 | **1** | 0.651 |
| **B** | 120 | 2998 | 2.923 | 0.953 | **1** | 1.176 |
| **B** | 240 | 3130 | **79.15** | 0.983 | **9** | 0.823 |
| **B** | 360 | 3229 | **531.6** | 1.024 | **52** | **0.493** |

### 3.1 ⚠ IL DETTAGLIO CHE DECIDE LA DIAGNOSI: **il p99 SCENDE mentre il max ESPLODE**

**In B, `|vd|` al 99° percentile CALA** — `1.176 -> 0.823 -> 0.493` — **mentre il massimo va da
`2.9` a `531.6`.**

> **Non e' la popolazione degli archi ad accelerare: e' UNA CODA DI POCHISSIMI ARCHI.**
> **E poiche' `nsub` e' un `max()`, quei pochi archi impongono il passo di integrazione A TUTTI.**

**`n3` da `1` a `52` e' un fattore `52` sul costo del passo**, e il rallentamento osservato
(`~25 -> ~274 s/frame`, fattore `11`) e' **dello stesso ordine**, misurato fra due istanti in cui
`n3` e' passato da `9` a `52`.

---

## 4. COSA QUESTO DICE SUL BLOCCO DEL RUN A 6000 — **l'ipotesi ② torna in gioco**

`doc/REFERTO_blocco_run6000.md` §5 elencava fra le ipotesi:

> *«**② La degenerazione di `d0`.** Se qualche passo adattivo si accorcia in risposta, il numero di
> sottopassi cresce. **Ma questo e' esattamente cio' che il CFL dovrebbe registrare, e non lo
> registra** — quindi o il meccanismo e' un altro, o esiste un ciclo che il CFL non conta.»*

**La seconda alternativa e' quella giusta, e ora c'e' una prova diretta invece di una congettura:**
il contatore guardato allora era **`_taup_cfl_max`**, che **non e' `nsub`**. **`nsub` non ha un
contatore**: e' una variabile locale di `step`, ricalcolata a ogni passo e mai registrata.

> **Un ciclo il cui conteggio non e' registrato da nessuna parte e' esattamente «un ciclo che il CFL
> non conta».** *(Ed e' il presidio del par.9 — «ogni ramo va contato» — applicato a un CICLO invece
> che a un `else`.)*

**⚠ MA NON E' LA STESSA DIAGNOSI, e non va scritta come tale:** qui il ramo B **avanza** (lo stack
si muove, il progresso viene scritto); il run a 6000 era fermo **due ore senza scrivere nulla**.
**Questa e' una spiegazione del RALLENTAMENTO, e una PISTA — non una spiegazione — per il blocco.**

---

## 5. ⚠ COSA QUESTO **NON** DICE — e la cautela e' scritta prima dei numeri

**NON dice che sia `chi_basc` a causarlo.** `chi_basc=off` e' l'**unica** variabile che distingue i
due bracci, **ma c'e' UN SEME PER RAMO**: su questo sistema due traiettorie che divergono a `1e-16`
danno numeri diversi **a codice invariato** (`CLAUDE.md` par.9), e il nullo di un confronto fra
bracci **non e' zero** — e' la dispersione **FRA SEMI**, che questo esperimento **non misura**.

> **Quindi: la differenza e' GRANDE e MONOTONA, e si riporta come tale.**
> **NON si dichiara significativa, e NON si attribuisce a `chi_basc`.**
> **Quello che servirebbe per attribuirla: >= 4 semi per braccio.**

**E non e' nemmeno detto che sia una patologia.** Un arco con `|vd| = 531` e' un arco che si muove
molto; il referto del 2700 aveva la stessa ambiguita' e la stessa domanda aperta — *«il sistema
stava degenerando o stava facendo qualcosa?»* **Non la risolvo qui.**

---

## 6. LA CONSEGUENZA OPERATIVA — **e la decisione e' di Luca**

**Proiezione, dichiarata come proiezione:** al ritmo dell'ultimo intervallo (`274 s/frame`) i
**440 frame** che restano a B costerebbero **~33 ore**. **E `n3` sta CRESCENDO**, quindi e' un
**limite inferiore**, non una stima.

| | stato |
|---|---|
| **ramo A** | **sano**: frame 215/500, `28.0 s/frame` stabile, `n3 = 1` a 1200 passi. Finisce in **~2.2 h** |
| **ramo B** | **avanza, ma degenera**: frame 60/500, `n3 = 52` e in crescita |

**L'archivio parziale di B vale comunque** *(3 snapshot: 120, 240, 360)*, ed e' **gia' abbastanza
per il reperto di questo documento**.

**Le opzioni, e non ne scelgo una:**
1. **lasciarlo correre** — costa giorni, e non e' detto che arrivi;
2. **fermarlo e tenere i 3 snapshot** — l'A/B resta a 360 passi invece di 3000, ma **il reperto su
   `|vd|.max` e' gia' acquisito**;
3. **fermarlo e rilanciarlo con piu' semi a meno passi** — l'unica strada che renderebbe
   **attribuibile** la differenza fra i bracci (par.5).

> **NON ho ucciso niente, e non lo faro' senza che Luca decida.**
