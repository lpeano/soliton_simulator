# REFERTO — **le somme: né redistribuzione né riduzione. IL FONDO SI SOLLEVA, e il momento netto CONVERGE**

**Blob `775ceab7`** · seme 42 · passo **240** · tre rami: **A** (nessuna cura), **B**
(`COPPIA_RECIPROCA`), **B'** (`GRAV_AMPIEZZA`) · strumento `csv/_test_fork/_somme.py` (`5ec2372f`),
esito `_somme.txt` · letture e soglia (**5 %**) fissate **PRIMA** in `doc/TASK_HISTORY/2026-09-20_la-somma.md` (`abc67a8`).

> **⚠ Gli snapshot sono RICOSTRUITI** *(il mio script li aveva cancellati: `Z31` rifatto)*, **e la
> ricostruzione è VERIFICATA: il ramo A dà `113 campi, 0 diversi` contro l'archivio in ENTRAMBI
> gli esperimenti.**
> **UN SEME, UNA SCENA, mezzo run, override del blob.** `--tau-luce` sigillo 6/7.

---

## 0. DUE PRESIDI CHE HANNO MORSO

**① `n` NON è identico** — e le somme sono **estensive**:

```
A = 2417        B = 2426        B' = 2420
```

**Quindi le somme grezze non sono confrontabili**, e tutti i numeri qui sotto sono **normalizzati
per `n`**. *(La differenza di `n` è dello `0.4 %`, gli scarti sono del `14-75 %`: non è `n` a
spiegarli — ma andava dichiarato, non assunto.)*

**② I nodi con `rho ≤ 1e-6`** *(dove l'inerzia è al pavimento, cioè su **un numero scelto**)*:

```
A = 26 (1.08 %)     B = 35 (1.44 %)     B' = 29 (1.20 %)
```

**③ E una somma che NON ho calcolato:** `sum(inerzia·|omega|²)`, l'energia rotazionale **vera**,
richiede `_T2` — **che non è negli snapshot**. **Non l'ho calcolata con un'inerzia inventata.**

## 1. ⚠ UN DIFETTO DEL MIO STRUMENTO, dichiarato

La funzione `rel()` usava `abs()`: **ha perso il SEGNO degli scarti.** Il verdetto automatico ha
detto *«non coincide»* — **giusto** — ma stampando `+13.67 %` per un ramo che in realtà **SCENDE**
del `13.8 %`. **Ricalcolato col segno**, ed è quel segno a contenere il reperto.

## 2. LE SOMME, normalizzate e col segno

| ramo | `sum|ω|/n` | scarto | `sum|ω|²/n` | scarto | **`|sum ω|/n`** | **scarto** |
|---|---|---|---|---|---|---|
| **A** | 104.27 | — | 5.483e+06 | — | **75.286** | — |
| **B** coppia | 128.87 | **+23.6 %** | 2.304e+06 | −58.0 % | **20.401** | **−72.9 %** |
| **B'** grav | 89.90 | **−13.8 %** | 1.387e+06 | −74.7 % | **20.098** | **−73.3 %** |

### ⚠ `sum|ω|` va in DIREZIONI OPPOSTE nelle due cure

**`+23.6 %` e `−13.8 %`.** **Le due cure non concordano nemmeno nel segno** — quindi **nessuna
delle quattro letture scatta**, e non ne invento una quinta.

## 3. IL REPERTO — **il MOMENTO NETTO converge allo STESSO valore**

```
|sum(omega)|/n :   A = 75.286   ->   B = 20.401   e   B' = 20.098
                   scendono del 72.9 % e del 73.3 %
                   e differiscono FRA LORO dell' 1.73 %
```

> **Due cure in punti DIVERSI della catena portano il momento netto per nodo da `75.3` a `~20.2`,
> e arrivano entro l'`1.7 %` l'una dall'altra.**
> **Non è conservazione** *(scende del 73 %)*: **è CONVERGENZA A UN VALORE COMUNE.**

## 4. E IL FONDO SI SOLLEVA DI OTTO-NOVE ORDINI

**L'istogramma di `log10|ω|`, agli stessi bin**, è il dato più netto dell'intera misura:

```
bin        -14    -12    -10     -8     -6     -4     -2      2      4
A          619    836     24      9      3     10    904      7      5
B            0      0      0      0      0   1477    900     18     12
B'           0      0      0      0      0   1472    900     15     10
```

**Nel ramo A ci sono `1455` nodi fra `10⁻¹⁴` e `10⁻¹²`. Nei rami curati NON CE N'È NEMMENO UNO:
sono tutti risaliti a `~10⁻⁴`.**

```
mediana:   4.93e-11  ->  1.88e-03  /  1.81e-03      OTTO ordini
p25:       9.58e-13  ->  8.70e-04  /  8.47e-04      NOVE ordini
```

**E i due rami curati sono quasi indistinguibili fra loro** (`1477/900` contro `1472/900`).

**La concentrazione cala:** i primi 10 nodi detenevano il **`99.73 %`** di `sum|ω|` in A, e il
`68 %` / `77 %` nei curati.

**E i nodi eccitati sono quasi gli stessi FRA le due cure, non con A:**

```
Jaccard:   A vs B = 0.4000     A vs B' = 0.4800     B vs B' = 0.8333
```

## 5. IL VERDETTO

> **NESSUNA DELLE QUATTRO LETTURE.** Le somme **non coincidono** (`14-75 %` contro una soglia del
> `5 %`), **non scendono tutte** (`sum|ω|` sale in una cura e scende nell'altra), **non salgono
> tutte**.
>
> **Ma l'ipotesi di partenza — «le cure REDISTRIBUISCONO» — è più vicina al vero di quanto le
> somme dicano, e per una ragione che le somme non catturavano:** ciò che cambia non è come
> l'`omega` totale si distribuisce fra i nodi, **è che una popolazione di ~1455 nodi che stava a
> `10⁻¹³` — cioè NUMERICAMENTE SPENTA — si accende a `10⁻⁴`.**
>
> **E questo accade in modo quasi identico nelle due cure**, che pure toccano punti diversi.

**Cosa NON scrivo:** *perché* quei nodi fossero a `10⁻¹³` nel ramo A, e *perché* qualunque
perturbazione del termine di coppia li accenda. **Non l'ho misurato.** *(Un'ipotesi che non uso: in
A il loro contributo si cancellava, e le cure rompono la cancellazione. È un'ipotesi.)*

**Nessuna identificazione:** non dico che «si conserva il momento angolare». **Dico che il momento
netto per nodo converge a `~20.2` in entrambe le cure, entro l'1.7 %, partendo da `75.3`.**
