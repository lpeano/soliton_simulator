# REFERTO — **la «scala minima» è dichiarata, non fissata. E il sistema nasce sotto.**

> `§7.1` e `§7.2` del mandato, eseguiti **prima di scrivere una riga di cura**, come ordinato.
> **Nessuna modifica alla fisica.** Simulatore `d163510d -> 01146a16` *(solo la ricomposizione di un
> commento che la mia strumentazione aveva spezzato)*.
> Dati: `csv/_test_fork/_d0_sotto_LAM.txt`. **25 snapshot del ramo A, 3 del ramo B.**

---

## 1. IL VINCOLO ESISTE NEL CODICE, E NESSUNO LO FA RISPETTARE

```python
:4359   self.d0 = np.maximum(self.d0, self._floor_d0())   # PAVIMENTO: la spinta non deve
:4360   #   portare d0 sotto la scala minima, o lo stress |d-d0|/d0 diverge (bug rientrante)
```
**La ragione scritta lì è ESATTA: è il meccanismo misurato in `Z79`.** Qualcuno lo sapeva.

**Ma il presidio non fa ciò che dichiara:**
```python
def _floor_d0(self):
    f = 0.05 / LAM_BASE          # = 0.0625
    return f * float(np.median(self.d0))        # <-- COMOVENTE
```
> **Se `median(d0)` scende, il pavimento scende con lei.** Un arco può restare «sopra il pavimento»
> mentre **entrambi affondano**. **`A9`** *(un presidio che non impedisce non è un presidio)* **e
> `A3b`** *(normalizzato sulla mediana di ciò che limita)*.

**⚠ E «scala minima» il commento la NOMINA, il codice non la FISSA.**

---

## 2. LA MISURA — **dal 26 al 55 % degli archi è già sotto `LAM`**

```
ramo passo   archi      min(d0)   p05(d0)   p50(d0)   max(d0)  pavim.   archi < LAM=0.8
A    120     527441     0.0525    0.4544    0.8401     1.532   0.05250  201233  (38.2 %)
A    360     527539     0.04935   0.1862    0.7897     2.834   0.04935  292708  (55.5 %)
A    1200    529905     0.05635   0.4857    0.9016     3.521   0.05635  140404  (26.5 %)
A    1800    534236     0.06293   0.06293   1.007      7.47    0.06293  152167  (28.5 %)
A    3000    546792     0.07635   0.07635   1.222    101.6     0.07635  185299  (33.9 %)
B    120     527857     0.05013   0.4638    0.8021     1.514   0.05013  260102  (49.3 %)
B    360     528158     0.05619   0.5842    0.8990     1.639   0.05619  137768  (26.1 %)
```

> **Non è una coda: è da un quarto a più della metà del sistema, a TUTTI gli istanti, in ENTRAMBI
> i rami.**

### 2.1 E la ragione si vede: **la mediana di `d0` STA su `LAM`**

`median(d0)` vale **`0.8401`** (A/120), **`0.8021`** (B/120), **`1.2216`** (A/3000), contro
**`LAM = 0.80`**.
> **La distribuzione è CENTRATA sulla scala minima, non sopra. Il sistema NASCE così.**

### 2.2 ⚠ E il pavimento di oggi morde — **sul 5 % degli archi, ed è `A3b` misurato**

**`min(d0)` coincide ESATTAMENTE col pavimento a TUTTI gli snapshot.** E **dal passo 1800 in poi
nel ramo A anche `p05(d0)` coincide col minimo e col pavimento**:
> **almeno il `5 %` degli archi è INCHIODATO** a un pavimento **comovente**, che nel frattempo
> **sale** da `0.0525` a `0.0764` seguendo la mediana.
> **Una grandezza che sembra evolvere e invece sta appoggiata a un pavimento — la quinta volta.**

---

## 3. LA VERIFICA ANALITICA — **il guadagno è REALE**

`stress = |d - d0|/d0`; con `d0 >= X` il limite superiore è `d_max/X - 1`.

| ramo | passo | `d_max` | pavim. oggi | limite OGGI | limite con `LAM` | guadagno |
|---|---|---|---|---|---|---|
| A | 120 | 3.185 | 0.05250 | **59.7** | **3.0** | `20.0x` |
| A | 1200 | 4.583 | 0.05635 | 80.3 | 4.7 | `17.0x` |
| A | 3000 | 20.13 | 0.07635 | 262.6 | 24.2 | `10.9x` |
| B | 120 | 3.15 | 0.05013 | 61.8 | 2.9 | `21.1x` |
| B | 360 | 149.1 | 0.05619 | 2652.7 | 185.4 | `14.3x` |

> **Da `11x` a `21x`, e in un sistema sano il limite vale `3`.** Resta grande **solo dove `d` stesso
> è esploso** *(B al 360, `d_max = 149`)* — **e quello è a valle della divergenza, non a monte.**

**⚠ CORREZIONE A UNA MIA FRASE:** avevo scritto che *«`d` arriva a 101.6 nel ramo A al 3000»*.
**Falso: `101.6` è il massimo di `d0`. Il massimo di `d` è `20.13`.**

---

## 4. ⚠ IL PROBLEMA CHE LA MISURA SOLLEVA — **nessuna forma è marginale**

La forma chiesta — *«`d0` si avvicina a `LAM` asintoticamente, senza mai raggiungerlo»* — deve
valere **`LAM` a `d0 -> 0`** e **`d0` a `d0 -> infinito`**. **Qualunque mappa liscia con quelle due
condizioni distorce massimamente PROPRIO a `LAM`:**

```
d0_eff = sqrt(d0^2 + LAM^2)          a d0 = LAM  ->  1.414 * LAM    (+41 %)
d0_eff = LAM + d0^2/(LAM + d0)       a d0 = LAM  ->  1.5   * LAM    (+50 %)
```
**E la mediana di `d0` È `LAM`.**
> **La saturazione non correggerebbe una coda: sposterebbe il CENTRO della distribuzione del
> `40-50 %`.**

**E l'alternativa — un pavimento NETTO a `LAM` — è quella che il mandato stesso scarta**
*(«un pavimento netto non risolve: sposta»)*, **e la misura dice perché aveva ragione:**
> **inchioderebbe il `26-55 %` degli archi esattamente a `LAM`** — lo stesso ammucchiamento `A3b`
> che oggi c'è al `5 %`, **moltiplicato per dieci.**

---

## 5. LE TRE STRADE — **e non ne scelgo una**

| | strada | cosa costa |
|---|---|---|
| **①** | **saturare verso una scala PIÙ BASSA di `LAM`** | curerebbe la divergenza **senza toccare il bulk** — **ma QUALE scala? Non ne ho una DERIVATA, e sceglierla sarebbe `A1`** |
| **②** | **accettare lo spostamento del bulk** come conseguenza voluta | se `d0 < LAM` è davvero *«un punto, non un'onda»*, allora **metà del sistema oggi non è fisica**, e spostarla **è** il senso della cura |
| **③** | **chiedersi se `LAM` sia la scala giusta PER `d0`** | **`LAM` è la lunghezza d'onda del SOLITONE; `d0` è la lunghezza di riposo di un ARCO.** Che debbano coincidere **è un'assunzione, non una misura** |

> **⚠ E se la risposta fosse «la mediana DEVE spostarsi», allora non è una cura: è una RIFONDAZIONE
> della geometria, e va chiamata così.**

---

## 6. COSA QUESTO REFERTO **NON** DICE

- **NON dice che `d0 < LAM` sia patologico.** Dice che è **la condizione di un quarto-metà del
  sistema, dalla semina**, e che nessuno l'aveva misurata;
- **NON propone una forma**, perché ognuna delle tre strade ne implica una diversa e **`A1` chiede
  che la scala sia DERIVATA**;
- **NON tocca** `scala_statale`/`I_med²`, le dimensioni dei tre addendi, `n3`, il fratello `S09`,
  il clip causale: **tutti registrati** *(`Z80`-`Z82`)*, **nessuno curato**;
- **UN seme, DUE rami.** Le frazioni sono su `~528 000` archi per snapshot *(statistica per-arco
  solida)*, **ma la scena è una.**
