# REFERTO — **la tensione nasce dal DENOMINATORE: `d0` crolla, `d` quasi non si muove**

> Criteri fissati prima in `doc/TASK_HISTORY/2026-09-20_rigiocata-0-120.md` (`23834ff`).
> Strumento `csv/_test_fork/_rigiocata_0_120.py`; output `_rigiocata_0_120.txt`,
> `_rigiocata_geometria.txt`. **Ramo B FERMATO** (frame 65/500); **ramo A non toccato.**
> **120 passi, campionati a OGNI passo. Simulatore `edb8f844`, invariato.**

---

## 1. IL SIGILLO INTERNO: **`138 / 138`, PASS** — e ci sono volute tre passate

```
campi confrontati: 138   DIVERSI: 0
solo nel RIFERIMENTO: 3 ['conc_archi','conc_nodi','masse_info']   |   solo nella RIGIOCATA: 0
PASS -- 138 campi IDENTICI. (e lo zero non e' mancanza di confronto: n=2998 in entrambi)
```

**La rigiocata E' il ramo B.** La serie che segue vale.

### 1.1 La strada, perche' l'errore era istruttivo e non banale

| passata | esito | causa |
|---|---|---|
| 1a | `136/137`, diverso `_g_kernel_alpha_tot` | la rigiocata **saltava** le `diagnostica()` del driver |
| 2a | `137/138`, **delta `+5`** *(mia **piu' alta**)* | ne contavo **una di troppo** |
| 3a | **`138/138`** | **l'ORDINE**: il driver salva **PRIMA** della `diagnostica()` del frame 20 |

**⚠ E IL CRITERIO NON E' STATO ALLARGATO.** Alla prima passata **tutti i campi FISICI erano gia'
identici** e l'unico diverso era un contatore diagnostico: sarebbe bastato dire *«il criterio si
intende sui soli campi fisici»* e i numeri sarebbero stati pubblicabili.
**Non l'ho fatto: ho corretto il CICLO.** Allargare un criterio **dopo** averne visto l'esito, e a
proprio favore, e' la famiglia del *criterio scaduto* — con l'aggravante di esserne l'autore.

### 1.2 Il numero che ha chiuso il ciclo — **misurato, non dedotto**

Invece di rigiocare al buio una terza volta, **una sonda da un minuto**:
```
dopo 1 frame (6 passi):   _g_kernel_alpha_tot = 79
dopo UNA diagnostica():                         84      -> diagnostica costa 5 chiamate a `_pesi()`
dopo UNA salva_stato():                         84      -> salva_stato ne costa 0
```
**Da cui i conti tornano ESATTAMENTE:**
```
riferimento   1554 = fisica 1534 + 4 diagnostiche x 5     (frame 1, 5, 10, 15)
2a passata    1559 = fisica 1534 + 5 diagnostiche x 5     (contavo anche il frame 20)
```
> **La FISICA coincideva gia': `1534 = 1534`. L'errore era di ORDINE.**

---

## 2. ⚠ LA RISPOSTA ALLA DOMANDA CHIAVE — **e' `d0` CHE CALA**

Il mandato chiedeva: *«`d/d0` puo' salire perche' `d` cresce, oppure perche' `d0` CALA. Sono due
fenomeni diversi e vanno distinti esplicitamente.»*

**L'arco `16-481`, a ogni passo:**
```
passo      d        d0       d/d0     |vd|        popolazione: d0 p50
  0     0.7344   0.7344     1.000    0            0.8801
 20     0.7728   0.7728     1.000    0.4988       0.7652
 40     0.9455   0.8119     1.165    1.053        0.7744
 60     1.232    1.001      1.231    1.352        0.7804
 65     1.296    0.4679     2.769    1.386        0.7827     <- d0 DIMEZZA
 80     1.490    0.4949     3.012    1.390        0.7865
 95     1.720    0.5035     3.416    1.250        0.7929
110     1.875    0.3610     5.195    0.9718       0.7989
120     1.968    0.2425     8.113    0.7297       0.8021
```

| | passo 0 | passo 120 | fattore |
|---|---|---|---|
| **`d`** *(il numeratore)* | 0.7344 | 1.968 | **x2.68** — **liscio e monotono** |
| **`d0`** *(il denominatore)* | 0.7344 | **0.2425** | **x0.33** — **a SCATTI, e oscilla** |

> **`d0` NON decresce: SALTA.** `1.001 -> 0.468 -> 1.173 -> 0.495 -> 1.031 -> 0.361 -> 0.426 -> 0.243`.
> **E' la firma di eventi DISCRETI, non di un rilassamento.**

**⚠ E NON E' UN FENOMENO GLOBALE: la mediana di `d0` sulla POPOLAZIONE non si muove**
(`0.880 -> 0.802`, **`-9 %`** in 120 passi) **mentre quella dell'arco `16-481` fa `-67 %`.**
**E `d/d0` mediano della popolazione resta a `1.000`-`1.025`: il sistema e' a RIPOSO.**

> **LA TENSIONE NON NASCE PERCHE' QUALCOSA SI ALLONTANA.**
> **Nasce perche' LA MOLLA SI ACCORCIA sotto un legame che quasi non si muove.**
> E' esattamente la seconda alternativa che il mandato chiedeva di distinguere.

### 2.1 E la lettura che scatta, fra le quattro fissate prima

Delle quattro *(istante preciso / monotona dalla semina / oscilla-e-si-fissa / nessun innesco)**:
**scatta la TERZA, e in una forma precisa: `d0` OSCILLA e a ogni oscillazione perde terreno.**
**Non c'e' UN istante:** ci sono **salti ripetuti** — il primo grosso fra il passo 60 e il 65
(`1.001 -> 0.468`, **dimezza**).

**⚠ E il dimezzamento e' un numero che il codice conosce:** la *compressione degenere* della mitosi
pone **`d0 = d/2`** (par.9). **Fra 0 e 120 nascono `607` nodi** (`n: 2391 -> 2998`), e i cinque hanno
**~620 archi ciascuno**: sono i nodi che la mitosi tocca piu' spesso.
**NON lo dichiaro dimostrato** — servirebbe tracciare quale evento tocca quell'arco — **ma il
valore `x0.5` e il profilo a scatti puntano li', e il candidato ha un nome.**

---

## 3. ⚠ LA GEOMETRIA — **un ERRORE DI POPOLAZIONE, ed era MIO**

Avevo riportato: *«CORRELAZIONE fra distanza dal baricentro e `_deg`: **+0.5086**, contro un nullo
di `0.0205`»*. **Quel numero e' un artefatto, e lo RITIRO.**

```
popolazione                  n        corr     |r| p50   deg p50
TUTTI                      2998     +0.2828      3.743       536      <- la mescolanza
  solo VUOTO (0-899)        900     +0.0705      2.989       180      <- NULLO 0.033, 3σ 0.100 -> NON significativa
  solo MASSE (900-2390)    1491     -0.9797      3.962       561      <- fortissima, SEGNO OPPOSTO
  solo NATI (2391+)         607     -0.0273      3.844         2      <- nullo
originali (vuoto+masse)    2391     +0.5928      3.707       549      <- il mio +0.5086
```

> **Il segno GLOBALE e' POSITIVO; quello della MATERIA e' `-0.98`.**
> **La correlazione globale e' INTERAMENTE l'artefatto di due popolazioni con gradi diversi**
> *(vuoto `180`, masse `561`)* **e raggi diversi.** E' **`A3`**, l'errore di popolazione, **e l'ho
> fatto io poche ore dopo averne censito quattro nel registro.**

**Dentro la MATERIA la relazione e' quasi perfetta e ha senso fisico:** `-0.9797`, cioe' **piu'
lontano dal centro della massa = MENO connesso** — i nodi di bordo hanno meno vicini.
**Dentro il VUOTO non c'e' relazione:** `+0.0705` **sotto** i `3σ` di `0.100`.

### 3.1 E la domanda del §2 del mandato ha una risposta: **NO**

> *«VERIFICA se i cinque siano i piu' connessi PERCHE' stanno al centro geometrico della scena.»*

**I cinque sono nodi del VUOTO** *(indici `16, 481, 621, 627, 837`, tutti `< 900`; `net.semina(900)`
gira a livello di modulo **prima** di `_semina_n_masse()`)*, e:

```
nodo      |r|    rango |r| NEL VUOTO    _deg    rango deg NEL VUOTO
16      2.751          41.0 %            605          94.9 %
481     2.816          44.0 %            643          99.1 %
621     3.268          64.1 %            610          95.8 %
627     2.754          41.2 %            649          99.3 %
837     3.123          55.9 %            610          95.8 %
```
**Raggio ORDINARIO (p41-p64), grado al VERTICE (p95-p99).**
**E nel vuoto il raggio non spiega il grado. Quindi: NO, non sono connessi perche' stanno al centro.**

### 3.2 ⚠ E resta un fatto che NON ho spiegato, ed e' piu' grosso della domanda di partenza

**Il grado mediano del VUOTO e' `180`, quello delle MASSE `561`, e il massimo delle masse e' `603`.**
**I cinque sono nodi di VUOTO con grado `605`-`649`: sopra il MASSIMO della materia.**

> **Cinque nodi di vuoto sono i piu' connessi dell'intero sistema, piu' di qualunque nodo di
> materia, e stanno a raggio ordinario.** **Perche', non lo so.** E' la voce che si apre.

---

## 4. §2 DELL'ISTRUZIONE — **`diagnostica()` NON scrive fisica, e si dichiara**

Enumerate **tutte** le funzioni che `diagnostica()` chiama, e cercate le assegnazioni `self.X = ...`
nel corpo di ciascuna:

| funzione | scritture |
|---|---|
| `diagnostica` | **0** |
| `intensita` · `_mat` · `_lam_archi` · `massa_critica_adattiva` · `stato_crossover` | **0** |
| `_pesi` | **4, tutti contatori `_g_kernel_alpha_*`** |
| `lambda_nodi` | **1: `_calcolo_schermatura`** |

**`_calcolo_schermatura` NON e' stato fisico, ed e' dimostrato e non asserito:** ha **tre**
occorrenze in tutto il file, **tutte dentro `lambda_nodi`** — `:2100` lo legge, `:2102` lo mette a
`True`, `:2106` lo rimette a `False`. **E' una GUARDIA DI RIENTRANZA**, e al ritorno vale di nuovo
`False`. **Nessuna legge lo legge.**

> **ESITO: oggi nessuna funzione chiamata da `diagnostica()` scrive stato fisico.**
> **Lo si dice invece di lasciarlo implicito**, perche' un esito buono non verificato e' indistin-
> guibile da uno cattivo non verificato.

**⚠ MA IL RISCHIO RESTA, e il precedente e' reale:** `calcola_psi()` **scrive `self.psi`,
`self.psi_spin`, `self.rho_spin`** — **fisica** — e **`lambda_vuoto` sembrava di sola lettura e la
chiamava.** **Oggi `diagnostica()` NON la chiama.** Se un giorno la chiamasse, **la differenza di
PERCORSO fra run e rigiocata diventerebbe differenza di FISICA**, e una rigiocata misurerebbe un
altro sistema **senza che nessuno se ne accorga** — perche' il sigillo confronta lo stato finale, e
lo stato finale sarebbe coerente con se stesso.

---

## 5. COSA QUESTO REFERTO **NON** DICE

- **NON dimostra che sia la mitosi ad accorciare `d0`.** Il valore `x0.5` e il profilo a scatti
  **puntano** alla compressione degenere, ma **servirebbe tracciare gli eventi su quell'arco**;
- **NON spiega perche' cinque nodi di VUOTO abbiano il grado piu' alto del sistema** — e' il fatto
  nuovo, ed e' aperto;
- **NON vede la SECONDA FASE** della divergenza *(`n1` che prende il posto di `n3`, misurata alle
  19:15 col processo vivo)*: al passo 120 non era cominciata **nemmeno la prima**. **Dichiarato
  prima di misurare**, nel task history;
- **NON decide l'A/B di `chi_basc`** — un seme per ramo;
- **NON si estende al blocco del passo 2700**, che resta un fenomeno separato.
