# REFERTO — **`CURA 2`, IL TEMPO UNICO NELLA MITOSI: IL GIRO CORTO**

> **`TEMPO_UNICO_MITOSI`**, blob `49fc54d2`, seme `42`, `120` passi, `520.1 s`.
> **Riferimento `_cura1_corto`**, blob `dd82794a`, **stessa configurazione, un interruttore di
> differenza.**
> **E DUE PROCESSI FRESCHI A UN SOLO BRACCIO** — lo `STANDARD 1` che il sigillo aveva violato
> *(`Z145`)*. **Questo referto È `T5`**, per decisione di Luca.
> Tabelle generate da `csv/_test_fork/_referto_cura2.py` e `_z146_scelta_freno.py` *(`P1-ter`)*.

---

## 1. I CRITERI, FISSATI PRIMA *(scheda ⑨ par.9)*

| | criterio | esito |
|---|---|---|
| **`E1a`** | la mitosi **non muore** | ✅ **PASS** |
| **`E1b`** | **non esplode** | ✅ **PASS** |
| **`B`** | il bilancio di `d0` **chiude** | ✅ **PASS** — `5.304e-14` |
| **`K`** | quante volte il clip avrebbe morso | ✅ misurato, **e ribalta la lettura** |
| **`C` `H`** | le guardie `A8` | ✅ **zero salti su tre guardie** |
| **`G`** | dove nasce la materia | ✅ riportato |
| **`R`** | `d0` e `d/d0` per classe | ⚠ **misurato, e SMENTISCE la previsione** |
| **`V8` `V9`** | la distribuzione di `dx/d` | ✅ misurato |

---

## 2. `E1a` / `E1b` — **LA MITOSI VIVE**

```
                                cura1 (OFF)     cura2 (ON)     rapporto
  n al passo 120                       2660           2575       0.9680
  archi                              526302         526204       0.9998
  nati da mitosi                        209            137       0.6555
  eventi di mitosi                       67             76       1.1343
  nascite (semina/mit)                  171            196       1.1462
```

> **Il termine di paragone è `FASE_2PI`, che su questo criterio è CADUTA: `62` eventi → `1`.**
> **Qui gli eventi SALGONO** *(`67 → 76`, `+13 %`)* **e i nati SCENDONO** *(`209 → 137`,
> `−34 %`)*: **più eventi, meno figli per evento.**

**⚠ E LA PREVISIONE ERA DIVERSA.** La scheda ⑨ par.8 punto 4 diceva: *«`dt_e/DT` ha mediana
misurata `≈ 0.68`, il tasso può calare di ~`1/3`»*. **Il TASSO DI EVENTI non è calato: è
salito.** **Sono i NATI a calare, di `0.6555` — cioè quasi esattamente il `0.68` previsto**, ma
**sulla grandezza sbagliata.** *(Non l'avevo previsto, e lo scrivo invece di far combaciare il
numero a posteriori.)*

---

## 3. `K` — **IL CLIP: UN LATO NON MORDE MAI, L'ALTRO MORDE IL `99.97 %`**

```
  clip ALTO su `prob` (resp > 1)             0 / 63128409 =   0.00000 %
  clip a ZERO su `prob` (resp <= 0)   63110902 / 63128409 =  99.97227 %
  clip ALTO su `rep`                         0 / 63128409 =   0.00000 %
  Eulero con dt/tau > 1                      0 / 63128409 =   0.00000 %
```

> ### ❗ **LA FORMA DI POISSON È UN NO-OP IN QUESTO REGIME, E ORA SI SA DI QUANTO.**
> Poisson **conserva** il taglio in basso e toglie quello in alto. **Il taglio in alto non morde
> mai** *(zero su sessantatré milioni)*, e **quello in basso morde il `99.97 %`**, dove **le due
> forme coincidono esattamente** *(entrambe danno `0`)*.
> **Restano `17 507` casi su `63 128 409` — lo `0.028 %`** — in cui `resp > 0`, **e lì il clip
> non ha comunque mai morso.**
>
> **LA CURA DI `:5244` È CORRETTA E INERTE.** Toglie un limite che `A11` classifica come patch,
> **senza cambiare un numero.** *(Era il punto 1 di «cosa non so derivare»: ora è derivato.)*

**E `S12` idem: l'Eulero non ha mai avuto `dt/τ > 1`.** Su `_rep` con `tau_arco` il passo è
sempre corto. **Il difetto che `S12` cura è reale — è stato misurato su `peq`, `dt/τ = 1.2018` —
ma su QUESTO sito, in QUESTO regime, non si presenta.**

> **⚠ E NON È UN ARGOMENTO PER TOGLIERE LA CURA:** la forma esatta è **una combinazione
> convessa per qualunque passo**, quella di Eulero no. `A11`: non si tiene un integratore che
> può scavalcare perché *oggi* non scavalca.

---

## 4. `C` / `H` — **LE TRE GUARDIE NON SCATTANO MAI**

```
  `_r_corrente` (l'orologio)         invocazioni 120   salti 0 ( 0.00 %)
  `_cs_nodo_prev` (la velocita')     invocazioni 120   salti 0 ( 0.00 %)
  `_dt_e_ultimo` (il tempo d'arco)   invocazioni 120   salti 0 ( 0.00 %)
```

**È l'opposto esatto della storia di questo repo** — `_cs_nodo_prev` cadeva nel fallback il
**`71.88 %`** delle volte, `_psi_spin_prec` il **`95.33 %`**.

> ### ❗ **E IL PERCHÉ È L'ORDINE, NON LA GUARDIA — misurato, non supposto.**
> Allo **snapshot** `_r_corrente` è lungo **`2570` su `2575`**: è scritto in `step()`, e
> `mitosi()` gira **dopo** e aggiunge nodi. **Ma `_r_nodo_mitosi` è chiamata DENTRO `mitosi()`,
> PRIMA che i figli esistano**, e lì `len(r) == n`.
> **Nei due difetti storici la mitosi aveva già allungato `n` prima della lettura. Qui no.**
> **La legge è salva per l'ORDINE delle chiamate, e questo è più fragile di una guardia: basta
> spostare una riga.** → **in coda.**

---

## 5. ⚠ `R` — **LA PREVISIONE DI `×2.5`-`×3` SU `d0` NON È CONFERMATA**

**`d0`, mediana per classe d'arco** *(convenzione di `G1`-`G2`, `2391` **letto dal run**)*:

| classe | `p50` OFF | `p50` ON | variazione | `n` ON |
|---|--:|--:|--:|--:|
| vuoto-vuoto | `1.7385` | `1.7612` | **`+1.3 %`** | `59 676` |
| massa-massa | `1.2365` | `1.2028` | **`−2.7 %`** | `369 766` |
| CONFINE vuoto-massa | `1.4530` | `1.4802` | **`+1.9 %`** | `96 403` |
| CONFINE con nato | `1.5121` | `1.2558` | `−16.9 %` | `345` |
| nato-nato | `1.0316` | `1.1108` | `+7.7 %` | `14` |

**`d/d0`, mediana:** `1.0575 → 1.0514` · `0.7600 → 0.7708` · `1.2209 → 1.2040`. **Frazioni di
per cento.**

> ### ❗ **LA PREVISIONE ERA DI LUCA ED ERA DERIVATA, E NON REGGE.**
> *«Togliere il fattore di tempo dal bersaglio di `rep` ALZA l'equilibrio della repulsione, che
> allarga `d0`; nel regime repulsivo `tau_pp > centro = 2.5`, quindi circa ×2.5-×3.»*
> **MISURATO: `d0` si muove del `±3 %` sulle classi popolose.** **Non `×2.5`: `×1.01`.**
>
> **PERCHÉ, e il perché è nel criterio `K` della sezione 3:** il bersaglio di `rep` vive su
> `resp_int`, e **`resp <= 0` nel `99.97 %` dei casi** — cioè il ramo repulsivo è **quasi
> ovunque**, ma `rep = clip(−resp, 0, 1)` e **il clip alto non morde mai**, quindi `rep` resta
> **piccolo**. Moltiplicare per `2.5` una quantità piccola, dentro un rilassamento con
> `dt/τ ≪ 1`, **sposta poco l'equilibrio raggiunto in 120 passi.**
>
> **⚠ E QUESTO NON DICE CHE LA PREVISIONE SIA SBAGLIATA IN PRINCIPIO: dice che a 120 PASSI il
> sistema non ha percorso abbastanza del suo rilassamento.** Va letto come **limite superiore**,
> non come *«nessun effetto»* — è la distinzione che il repo impone già.

**⚠ E `A2` È RISPETTATO:** queste sono statistiche **del referto**. La legge tocca
`ampiezza_int`, `ampiezza`, `rep`, `prob`, `_rep`, `grad_tau`: **nessuna legge una statistica
globale.**

---

## 6. `G` — **LA MATERIA NASCE DOVE L'OROLOGIO CAMBIA, E IL CONTRASTO CRESCE CON LA CURA**

`grad|r|` lungo l'arco, `p10 / p50 / p90`:

| | TUTTI gli archi | archi con un **NATO** | rapporto delle mediane |
|---|---|---|--:|
| **cura1 (OFF)** | `7.630e-03` / `1.159e-01` / `6.842e-01` | `1.507e-02` / `2.860e-01` / `1.023e+00` *(n=526)* | **`2.47×`** |
| **cura2 (ON)** | `1.569e-02` / `9.946e-02` / `5.442e-01` | `2.898e-02` / `4.203e-01` / `9.519e-01` *(n=349)* | **`4.23×`** |

> **Si RIPORTA, non si giudica** *(criterio di Luca)*. **La materia nasce dove il gradiente
> dell'orologio è più alto in ENTRAMBI i bracci, e con la cura il contrasto è quasi il doppio.**
>
> **⚠ UN SEME, UN ISTANTE, NESSUNA BARRA** *(`P3`)*: su questo sistema caotico la barra giusta è
> la dispersione **fra semi**, e qui non c'è. **`2.47` contro `4.23` è un'INDICAZIONE, non un
> fatto.** **Servirebbero ≥ 4 semi.**
>
> **E c'è un motivo strutturale per cui potrebbe essere vero:** con la cura il gradiente **è**
> quello dell'orologio; senza, viene da `|tw|`, che è **torsione**. **Il braccio OFF mostra il
> contrasto su una grandezza che non guidava la mitosi.**
>
> **⚠ E IL CAMPIONE ON È RISTRETTO, dichiarato:** `526 194` archi su `526 204`, perché
> `_r_corrente` non copre i `5` figli dell'ultimo passo. **La restrizione tocca proprio i nati
> più recenti: è sbilanciata CONTRO l'effetto cercato.**

---

## 7. `V8` / `V9` — **`dx/d` È PICCOLO, E LA SATURAZIONE DI `tanh` NON SI MANIFESTA MAI**

```
  verso                n        p50      p90      p99    p99.9      max   >1   >2  >0.5
  discese       60538734     0.0019   0.0239   0.0310   0.0344   0.0385  0.0  0.0   0.0
  salite        65192342     0.0024   0.0124   0.0241   0.0307   0.0531  0.0  0.0   0.0
```

**Il massimo su `125 731 076` campioni è `0.0531`: `19` volte più piccolo della scala `x ~ 1` a
cui il tetto di `tanh` comincia a contare.** Al massimo misurato le due forme differiscono di
**`1.4e-03` relativo**.

> ### ✅ **IL DIFETTO DICHIARATO DI `tanh` — la saturazione a `2` — NON SI PRESENTA. COSTO MISURATO: NESSUNO.**

**⚠ E LA DERIVA DELLA PIANA NON SI PUÒ QUANTIFICARE, PER UN LIMITE MIO.** Vale
`exp(N·E[x²]/2)`, e **`E[x²]` NON È STATO REGISTRATO** — l'involucro ha salvato **quantili**,
`max` e quote. **I quantili non bastano a stimare una media di quadrati.** L'intervallo fra
ipotesi estreme:

| ipotesi su `sqrt(E[x²])` | 120 passi | 1200 passi | 6000 passi |
|---|--:|--:|--:|
| `= p50 (0.0024)` | `+0.03 %` | `+0.35 %` | `+1.74 %` |
| `= p90 (0.0124)` | `+0.93 %` | `+9.66 %` | `+58.61 %` |
| `= p99 (0.0241)` | `+3.55 %` | `+41.69 %` | `+471.12 %` |

> **A `120` passi è trascurabile in ogni ipotesi. A `6000` l'intervallo è TROPPO LARGO per
> decidere.**
> **COSA LO CHIUDEREBBE, a ZERO run in più:** registrare **`mean((dx/d)²)`** nello stesso
> involucro che già registra i quantili. **È una somma in più, sugli stessi campioni.**
>
> **⚠ LA SCELTA RESTA DI LUCA. Questa è la misura, non la decisione.**

---

## 8. COSA QUESTO REFERTO **NON** DICE

- **non dice che la cura sia giusta.** Dice che la mitosi vive, che il bilancio chiude, e
  **quanto** le forme nuove differiscono da quelle vecchie;
- **due delle tre sostituzioni formali sono INERTI in questo regime** *(Poisson, e l'integratore
  esatto)*. **L'effetto misurabile viene dalle due sostanziali**: il gradiente preso
  dall'orologio, e il fattore di tempo che entra una volta sola;
- **un seme, un istante, nessuna barra.** Tutti i confronti di questo referto sono **fra due
  run**, non **fra popolazioni di run**. `P3` vale per ognuno.
