# REFERTO — **`Z9` è ancora quella. E `R6` REGGE.**

**Blob:** `a8f1b2f4` (byte grezzi `cf6722ff`), HEAD `82aa2d1`. **Nessuna cura, nessun cablaggio,
nessun pavimento.** `Z10` non toccata.

---

## 1. `Z9` — **sostanzialmente intatta**

**Due scene, e la distinzione è metodologica:** la misura originale (`cdc0e41`) usava una scena a
**3 masse da 120, raggio 2.0**, con `step(); mitosi()`. **Quella è l'unica confrontabile coi suoi
numeri.** La scena del **batch** è invece il sistema che gira davvero. **Riporto entrambe**, perché
un confronto fra numeri presi in modo diverso non è un confronto.

### (A) Scena ORIGINALE — confrontabile con `cdc0e41`

| passo | `ramp` mediano **oggi** | `ramp` mediano **`cdc0e41`** |
|---|---|---|
| 1 | **0.0002** | 0.0002 |
| 60 | **0.010179** | 0.0106 |
| 120 | **0.020414** | 0.0217 |

```
crescita di eta per passo      : 0.00849341    (riferimento: ~0.009)
passo estrapolato per ramp = 1 : 5887          (riferimento: ~5526)
```

### (B) Scena del BATCH — il numero valido oggi

```
passo   1 : ramp mediano 0.0002      p05 0.0002     p95 0.0012     ramp=0: 0.00 %
passo  60 : ramp mediano 0.010082    p05 0.0061     p95 0.0163     ramp=0: 0.00 %
passo 120 : ramp mediano 0.020167    p05 0.0128     p95 0.0319     ramp=0: 0.00 %
crescita di eta per passo      : 0.00838942
passo estrapolato per ramp = 1 : 5960
```

### ⚠ IL VERDETTO, e va dato con la barra che non ho

**I numeri sono nella stessa direzione che il mandato indicava come possibile — maturazione un po'
più LENTA** (`5887` e `5960` contro `5526`, cioè **+6.5 %** e **+7.9 %**) — **e la catena causale è
plausibile**: i neonati ora pesano **zero** invece di `2e-4`, contribuiscono meno a `psi`, quindi `r`
è più basso, quindi `eta` cresce più piano.

> **MA È UN SOLO SEME, e P3 vieta di chiamarlo un effetto.**
> **Su questo sistema la dispersione fra semi di una grandezza trasversale è già stata misurata
> intorno al 3 % sulle pendenze, e nessuno ha mai misurato la dispersione di `ramp`.**
> **Uno scarto del 6-8 % su un seme solo NON è distinguibile dalla dispersione.**

**Quindi la lettura onesta è la PRIMA delle tre: `Z9` è sostanzialmente INTATTA.**
*(Se la si volesse chiamare «peggiorata», servirebbero ≥ 4 semi — e non è questo il mandato.)*

**E il fatto che conta non è cambiato di una virgola:**
> **Il kernel matura in ~5900 passi. I run sono 300-500. A 500 passi `ramp` sta sotto il 10 %,
> e il peso d'arco tipico è ~1 % di quello maturo.**
> **`Z9` resta il difetto da cui questo filone è partito, e resta da curare.**

---

## 2. `R6` — **REGGE. L'ostacolo non è caduto.**

```
                            OGGI (a8f1b2f4)      riferimento (8bfcf46)
_pesi() per passo                12                      16
   di cui PRIMA della cache       7                       9
   di cui DOPO                    5                       7
```

**Il TEMPO 2 ha ridotto le chiamate da 16 a 12 — ma `_pesi()` gira ANCORA A CAVALLO della scrittura
di `_cs_nodo_prev`.**

**La lettura era fissata prima:** *«se `_pesi()` gira una volta, o comunque tutta da un lato della
scrittura → `R6` è caduto; se gira ancora a cavallo → `R6` regge»*. **Gira 7 prima e 5 dopo.**

> **`R6` REGGE, e la cura `ramp = eta/(d_nodo/cs_nodo)` resta bloccata:** valutarla lì violerebbe
> **A6** su **5 chiamate su 12** — il **42 %**, a ogni passo, in modo permanente. *(Era il 44 %.)*

### E il quadro per chiamante spiega perché il TEMPO 2 non bastava

```
stato_crossover = 1354      step = 123      calcola_psi = 37
```

**Il TEMPO 2 agiva su `calcola_psi`, che è il 2.4 % delle chiamate.** **L'89 % viene da
`stato_crossover`**, attraverso `massa_critica_adattiva` — **la ricorsione indiretta già registrata
(voce M, e il referto del 2026-09-14)**. **Correggere `calcola_psi` non poteva sbloccare `R6`, e
infatti non l'ha sbloccato.**

**Nota collaterale:** `_pesi()` come lettore di `_cs_nodo_prev` ha ora un fallback dell'**1.19 %**
(era **7.82 %**) — coerente col minor numero di chiamate, e resta il **terzo lettore** con una
frazione propria (A8b).

---

## 3. COSA NE SEGUE, e non lo decido io

- **`Z9` va curata, e le due cure provate sono bocciate a ragione:** `TAU_A = LAM/cs` **sposta** il
  numero su `LAM`; `ramp = eta/(d/cs)` **viola A6** dove verrebbe valutato.
- **La via che `R6` indica**, e che questo referto non percorre: **valutare il `ramp` UNA VOLTA per
  passo**, da uno stato coerente — cioè **uno snapshot**, con il prezzo A8b (estensione ai cinque
  punti di crescita, contatore). **È la voce Z12, e resta una decisione.**
- **Oppure affrontare la ricorsione `stato_crossover → _pesi()`** — **l'89 % delle chiamate** — che
  è il vero motivo per cui `_pesi()` gira dodici volte. **Ma è la voce M, un fronte diverso**, ed è
  già stato stabilito che lì *«resta il costo, non la cura»*.

**`Z10` resta aperta, e la sua soluzione — separare le due leggi che `TAU_A` governa — vale a
prescindere da questa misura.**
