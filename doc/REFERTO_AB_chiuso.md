# REFERTO DI CHIUSURA — **A si DILATA tutto insieme, B sta fermo e pochi archi impazziscono**

> L'A/B a `sep = 4.0` e' **finito**. **Ramo A: 3000 passi, intatto.** **Ramo B: fermato al passo
> 390.** Simulatore `edb8f844` / git-blob `b44f50ce`, **mai toccato**; driver `9aee4fc2`; seme `42`.
> Strumento `csv/_test_fork/_fuga_vd.py`; output `_fuga_vd_finale.txt`.
> **⚠ UN SEME PER RAMO: nessuna differenza e' attribuita a `chi_basc`. Vedi §5.**

---

## 1. COME SONO FINITI

| | **ramo A** *(`chi_basc` ACCESO)* | **ramo B** *(SPENTO)* |
|---|---|---|
| arrivato a | **3000 passi (500/500 frame)** | **390 passi (65/500)** — fermato da Luca |
| `n` finale | **18 000** *(da 2391: `x7.5`)* | 3 241 |
| costo/frame | **`27.457 -> 28.015 s` = `+2 %` su 3000 passi** | `25 -> oltre 600 s` |
| `nsub` | **`4`** *(il pavimento)*, fino alla fine | **`15 594`** all'ultimo campione |
| snapshot | **25/25, 0 saltati, 0 FALLITI** *(0.97 GB)* | 3/3 intatti |

**La domanda che Luca aveva posto — *«vedere se si rompe o se arriva intatto: entrambi gli esiti
sono informativi»* — ha risposta: A ARRIVA INTATTO.**

---

## 2. ⚠ MA «INTATTO» NON VUOL DIRE «FERMO» — **e avevo scritto io che A era piatto**

**Il COSTO di A e' piatto. `|vd|` NO.**

```
ramo A       n        |vd| p50   |vd| p99   |vd| MAX    n3
passo  120   2672      0.5394     1.334      3.354       1
passo 1200   4598      0.1213     0.651      2.620       1      <- il MINIMO
passo 3000  18000      0.2944     2.201     18.95        1      <- x7.2 sul max
```
**`|vd|.max` fa `x7.2` fra il passo 1200 e il 3000.** Avevo riportato A come *«piatto»*: **era vero
del costo, non della velocita'.** **Lo correggo.**

### 2.1 Perche' allora `nsub` e' rimasto `4`? **Perche' `n3` e' un RAPPORTO**

`n3 = ceil(|vd|.max * DT / (0.1 * median(d)))`

```
ramo   passo    median(d)    |vd|.max    n3
A       120        1.186       3.354      1
A      3000        2.786      18.95       1      <- 0.68 arrotondato a 1: il NUMERATORE e' cresciuto
                                                    x5.65, ma il DENOMINATORE x2.35
B       120       0.9528       2.923      1
B       360        1.024     531.6       52      <- il denominatore NON si e' mosso (+7 %)
```

> **In A crescono INSIEME: il sistema si dilata, e le velocita' crescono con lui. Il rapporto resta
> limitato.**
> **In B cresce SOLO il numeratore: il sistema sta fermo e pochi archi impazziscono.**

---

## 3. ⚠ IL DISCRIMINANTE — **ed era la lettura di Luca, ora con i numeri di ENTRAMBI i bracci**

Il mandato del `0 -> 120` poneva il criterio cosi':
> *«In un collasso fisico la coda INTERA si alza: l'energia si concentra, ma la regione partecipa.
> Qui il resto RALLENTA — cioe' l'energia non viene da nessuna parte: APPARE.»*

**RAMO A — tutta la distribuzione sale insieme:**
```
              p50        p99        max      #{|vd|>1}   #{>10}   #{>30}   #{>100}
passo 1200   0.1213     0.651      2.62         724         0        0        0
passo 3000   0.2944     2.201     18.95       48280        82        0        0
              x2.4       x3.4       x7.2        x67
```
**`#{|vd| > 30}` e `#{> 100}` restano ZERO a TUTTI E 25 gli istanti.**

**RAMO B — il corpo scende, la coda esplode:**
```
              p50        p99        max      #{|vd|>1}   #{>10}   #{>30}   #{>100}
passo 120    0.1921     1.176      2.923      17279         0        0        0
passo 360    0.1011     0.4926   531.6          586       231      135       61
              x0.53      x0.42     x182         x0.03
```

> **In A il `p99` fa `x3.4` SALENDO. In B fa `x0.42` SCENDENDO, mentre il massimo fa `x182`.**
> **La lettura di Luca separa i due rami in modo netto, e non serviva una soglia inventata: il
> SEGNO della derivata del `p99` basta.**

### 3.1 E la conferma piu' diretta: **la tensione della POPOLAZIONE**

```
d/d0 mediano di TUTTI gli archi        ramo A passo 3000:  2.288      <- tutto il sistema e' TESO
                                       ramo B passo  360:  1.076      <- il sistema e' A RIPOSO
```
**In A la dilatazione e' `+126.96 %` e il sistema intero e' steso di `2.3` volte.**
**In B la dilatazione e' `+20.77 %` e il grosso sta a riposo, mentre pochi archi arrivano a
`d/d0 = 178`.**

> **Sono due fenomeni diversi, non due gradi dello stesso fenomeno.**

---

## 4. ⚠ E UNA COSA CHE NON ARCHIVIO COME «A STA BENE»

```
#{|vd| > 10} nel ramo A:   0 fino al passo 2400, poi  1, 7, 21, 43, 57, 82
n3 del ramo A al passo 3000: 0.68 -> arrotondato a 1
```
**La coda di A si sta POPOLANDO negli ultimi 600 passi**, e `n3` e' al **68 %** della soglia che lo
porterebbe a `2`. **A 3000 passi A e' sano; NON e' detto che lo sia a 6000**, e il run a `sep = 8`
si pianto' al 2700. **Lo scrivo perche' «e' arrivato» non significa «era al sicuro».**

---

## 5. ⚠ COSA QUESTO NON DICE — **e questo paragrafo vale quanto gli altri**

- **UN SEME PER RAMO.** Su questo sistema il nullo di un confronto fra bracci **non e' zero**: e' la
  dispersione **FRA SEMI**, che questo esperimento **NON misura** (`CLAUDE.md` par.9, e `P3`).
  > **Quindi: la differenza fra «A arriva a 3000» e «B esplode a 390» NON e' attribuita a
  > `chi_basc`.** E' **GRANDE e MONOTONA**, e si riporta come tale. **Per attribuirla servono `>= 4`
  > semi per braccio.**
- **NON decide se `chi_basc` vada tolto.** La decisione resta di Luca, e `Z73` resta **APERTA**;
- **NON spiega perche' cinque nodi di VUOTO siano i piu' connessi del sistema** (`Z77`);
- **NON spiega la SECONDA FASE di B** — `n1` che sostituisce `n3` come vincolo dominante, misurata
  alle 19:15 sul processo vivo (`Z74`). **La rigiocata `0 -> 120` non poteva vederla.**

---

## 6. LO STATO DEI FRONTI, dopo questo arco

| voce | stato |
|---|---|
| **`Z73`** `chi_basc` | **APERTA.** Ritirata **due volte**; il run lungo conferma che **non blocca la mitosi** |
| **`Z74`** la fuga di B | **APERTA** — resta da spiegare la seconda fase (`n1`) |
| **`Z75`** `nsub` invisibile | **APERTA** — il contatore **si puo' cablare ora: i run sono finiti** |
| **`Z76`** i nati di grado 2 | **APERTA** — `4932` su `7323` al passo 1680; a 3000 `n = 18000` |
| **`Z77`** `d0` che crolla | **APERTA** — il candidato *(compressione degenere)* **non e' dimostrato** |
