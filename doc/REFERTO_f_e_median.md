# REFERTO — **l'algebra è falsificata. E `f` CROLLA, non cresce. Ma la ricostruzione non riproduce `r`**

**Blob `775ceab7`** · seme 42 · le due finestre a 6 passi (`0→60`, `180→240`) · strumento
`csv/_test_fork/_f_e_median.py` (`cd1ad7e4`), esito `_f_e_median.txt` · letture fissate **PRIMA**
in `doc/TASK_HISTORY/2026-09-20_f-e-median.md` (`929d61e`).

> **NESSUN RUN: i dati bastavano.** `psi_spin`, `_psi_spin_prec` e `_med_f_prec` sono **tutti**
> negli snapshot. Il §3 del mandato non si è applicato.

---

## 1. ⚠ L'ALGEBRA DEL MANDATO È FALSIFICATA, e con un margine enorme

```
passo   x DEDOTTO (invertendo r)   x RICALCOLATO (dai dati)   rapporto
12          1.6                        0.72065                0.45
18          4.35                       0.0807754              0.019
24        224                          0.0051151              2.3e-05
```

**Al passo 24 `x` vale `0.005`, non `224`: un fattore `44 000`.** **Era la prima cosa da
falsificare, e il mandato stesso lo diceva.**

## 2. E `f` NON CRESCE: **CROLLA**

**Finestra `0 → 60`:**

```
        |f| p05     |f| p25     |f| p50     |f| p95    |f| max   | med USATO   x = p50/med
6       0.00136     0.008481    0.1794      0.2386     0.2419    | 0.268318    0.6687
12      0.001347    0.009215    0.2101      0.3464     0.3519    | 0.2915      0.7206
18      0.001272    0.00871     0.02802     0.1342     0.1375    | 0.346905    0.08078
24      0.0003323   0.001264    0.002114    0.02153    0.08481   | 0.413286    0.005115
60      0.0002779   0.001232    0.00304     0.09051    0.2736    | 0.29967     0.01014
```

```
|f| MEDIANA:  0.179428 -> 0.00304   (x0.017, cioe' -98 %)
med USATO  :  0.268318 -> 0.29967   (x1.117, SALE)
```

> **Nessuna delle quattro letture scatta come scritta.** **`α`** diceva *«`median(|f|)` crolla»*:
> **non crolla, sale del 12 %.** **`β`** diceva *«`f` cresce»*: **crolla di 60 volte.**
> **`γ`** diceva *«nessuno dei due si muove»*: **`f` si muove eccome — nella direzione opposta a
> quella prevista.**
> **`δ`**: il pavimento **non scatta mai** — `+0` in tutte e venti le transizioni delle due
> finestre, coerente col `2 su 2700`.

## 3. ⚠ MA LA MIA RICOSTRUZIONE NON RIPRODUCE `r` — e questo limita tutto il resto

**Ricalcolando `r` dalla formula di `ritmo()`, nodo per nodo, con l'`f` e il `med` ricostruiti:**

```
passo | x p50      r RICALCOLATO | r SALVATO p50   scarto mediano
6     | 0.66871    0.78613       | 0.8569          0.032        <- ACCORDO BUONO
12    | 0.72065    0.82682       | 1.2004          0.200
18    | 0.080775   0.11386       | 1.3783          0.884
24    | 0.0051151  0.0072351     | 1.4141          1.406        <- ROTTO
60    | 0.010145   0.014348      | 1.4141          1.399
```

> **Al passo 6 la ricostruzione funziona** *(scarto `0.032`)*. **Poi diverge progressivamente e al
> passo 24 è completamente rotta.**

**Quindi: `f` e `med` che leggo dagli snapshot NON sono quelli con cui il codice ha calcolato il
`r` salvato.** Due spiegazioni possibili — **e non ne scelgo nessuna, perché non le ho misurate**:

- il `med` salvato (`_med_f_prec`) **non è** quello usato in quel passo;
- **oppure `_r_corrente` è scritto in un momento del passo diverso** da quello in cui `psi_spin` e
  `_psi_spin_prec` assumono i valori salvati. **È la famiglia di `Z19`** — *«una grandezza letta in
  un momento del passo diverso da quello che il codice dichiara»*, **quarta occorrenza**.

**⚠ CONSEGUENZA SULLA LETTURA:** **non posso concludere se sia `f` a muoversi o il metro ad
accorciarsi**, perché la catena che ricostruisco **non riproduce l'osservabile**. **Quello che
misuro è vero di `f` come lo ricostruisco io, non necessariamente di `f` come lo usa `ritmo()`.**

## 4. UN FATTO CHE RESTA, e non dipende dalla ricostruzione

**`med` OSCILLA dell'`802 %` fra passi consecutivi** nella finestra `180→240`:

```
passo    180      186      192      198      204      210      216
med    0.0653   0.1201   0.1158   0.0103   0.0260   0.2343   0.0532
```

**`Z43` dava il `62 %`. Qui è tredici volte tanto.** E `_med_f_prec` è letto **direttamente** dallo
snapshot, **non ricostruito**: questo numero non dipende dalla mia catena.

> **Nella finestra `0→60` l'oscillazione massima è `19.1 %`. Nella finestra dell'evento è
> `802 %`.** Il metro è **molto** più instabile durante l'evento che all'inizio.

## 5. IL VERDETTO

**Tre cose sono state falsificate, tutte e tre erano ipotesi:**

1. **`x ≈ 224`** → misurato `0.005`, **fattore 44 000**;
2. **«`f` cresce di centinaia di volte per passo»** → **crolla del 98 %** nei primi 24 passi;
3. **«`median(|f|)` crolla verso il pavimento»** → **sale del 12 %**, e il pavimento **non scatta
   mai** nelle due finestre.

**E una cosa nuova è emersa, che nessuna delle quattro letture prevedeva:** **la catena
`f → x → r` ricostruita dagli snapshot riproduce `r` al passo 6 e non lo riproduce più dal 24.**

**Non so perché, e non lo invento.** È il reperto, ed è quello che va guardato prima di qualunque
altra cosa su `r`: **finché quella catena non torna, ogni lettura su `r` poggia su una
ricostruzione che non riproduce l'osservabile.**
