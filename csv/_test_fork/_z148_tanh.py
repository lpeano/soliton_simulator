# -*- coding: utf-8 -*-
"""Scheda 11, par.4-ter: la TERZA forma (tanh) e la tabella delle tre. Nessun codice."""
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

N = 0


def s1(t, v, nu):
    global N
    assert t.count(v) == 1, "occ=%d per %r" % (t.count(v), v[:70])
    N += 1
    return t.replace(v, nu)


P = "doc/REGISTRO_FISICA.md"
t = io.open(P, encoding="utf-8", newline="").read()

A = u"## 5. ❌ **PERCHÉ NON `exp(dx/u)`** — la variabile `log(d − LAM)`"
B = u"""## 4-ter. ✅ **LA TERZA FORMA: `1 + tanh(x)`** — *proposta di Luca, e domina la seconda*

```
(d − LAM)  ←  (d − LAM) · (1 + tanh(dx/d))
```

**Le quattro proprietà, verificate con lo STESSO strumento** *(`csv/_test_fork/_z147_ito.py`)*:

### ✅ **(1) DERIVA ESATTAMENTE NULLA, a TUTTI gli ordini**

`(1 + tanh(x)) + (1 + tanh(−x)) = 2` **per disparità di `tanh`**. Non è un'approssimazione: è
un'identità.

| `s` | `E[f] − 1` |
|--:|--:|
| `0.500` | **`0.000000000000000e+00`** |
| `0.125` | **`0.000000000000000e+00`** |
| `0.001` | **`0.000000000000000e+00`** |

> **Zero ESATTO in macchina, a ogni `s` provato.** La piana dà `+s²/2`, Itô `−s⁴/12`;
> **questa dà zero e basta.**

### ✅ **(2) MONOTONA** — la derivata è `sech²(x) > 0` sempre

Su `[−3, 3]`: **`0` incrementi negativi su `6000`**. *(Itô ne ha `2000` su `3000`.)*

### ✅ **(3) MAI SOTTO `LAM`** — `1 + tanh(x) ∈ (0, 2)`

`x = −50 →` fattore `0.000000e+00` *(numericamente, ma matematicamente `> 0`: `~2e^{2x}`)* ·
`x = +50 →` fattore `2.000000`.

### ✅ **(4) FEDELTÀ `O(x³)`, come Itô** — `1 + tanh(x) = 1 + x − x³/3 + …`, **nessun termine in `x²`**

| `x` | `u(1+x)` | piana | eccesso | Itô | eccesso | **tanh** | **eccesso** |
|--:|--:|--:|--:|--:|--:|--:|--:|
| `0.30` | `1.30000` | `1.34986` | `+4.986e-02` | `1.29046` | `−9.538e-03` | `1.29131` | **`−8.687e-03`** |
| `1.00` | `2.00000` | `2.71828` | `+7.183e-01` | `1.64872` | `−3.513e-01` | `1.76159` | **`−2.384e-01`** |

**È anche un po' PIÙ fedele di Itô** a `x` moderati.

### ⚠ **(5) IL LIMITE, dichiarato: UNA SALITA AL PIÙ RADDOPPIA `(d − LAM)`**

`1 + tanh(x) < 2` **per costruzione**. È una **saturazione**, e `A11` cor.6 dice che *un limite
che satura è un allarme*. **Va giudicato con la distribuzione di `|dx|/d`, esattamente come il
tetto `√e` di Itô** — punti `V8`/`V9`.

> **Ed è MENO restrittivo del tetto di Itô** *(`2` contro `1.6487`)*, **e senza la
> non-monotonia.**

## 4-quater. ❗ **LE TRE FORME A CONFRONTO**

| | **deriva simmetrica** | **monotona** | **fedeltà a `u(1+x)`** | **tetto per una SALITA** |
|---|---|:--:|---|---|
| **piana** `exp(x)` | `+s²/2` — **2° ord., POSITIVA** *(lontano dal muro)* | **✅** | eccesso `+x²/2` | **nessuno** |
| **Itô** `exp(x−x²/2)` | `−s⁴/12` — 4° ord., NEGATIVA | **❌** *(max a `x=1`)* | `O(x³)` | `√e = 1.6487` |
| **tanh** `1+tanh(x)` | **`0` ESATTO** | **✅** | `O(x³)` | `2` *(raddoppia)* |

> ### ❗ **`tanh` DOMINA `Itô` SU OGNI ASSE**
> deriva **più piccola** *(zero contro quarto ordine)* · **monotona**, e Itô no · **stessa**
> fedeltà, anzi un po' migliore · tetto **meno restrittivo** *(`2` contro `1.6487`)*.
> **Quindi Itô esce dal confronto**: non c'è nessun asse su cui sia preferibile.

> ### **LA SCELTA VERA È FRA `piana` E `tanh`, e si riduce a UNA domanda:**
> **`piana` non ha tetto ma HA deriva. `tanh` non ha deriva ma SATURA a `2`.**
> **La decide la DISTRIBUZIONE di `|dx|/d`** — punti `V8`/`V9` — **e la decide Luca DOPO quella
> misura.** *(Non prima: senza quel numero non c'è una base derivata.)*

## 5. ❌ **PERCHÉ NON `exp(dx/u)`** — la variabile `log(d − LAM)`"""
t = s1(t, A, B)

# cosa non so derivare: si aggiorna
A2 = (u"5. **se la non-monotonia di Itô si manifesti davvero.**")
B2 = (u"5. **se la SATURAZIONE di `tanh` a `2` si manifesti davvero**, e la stessa domanda per la "
      u"non-monotonia di Itô.")
t = s1(t, A2, B2)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("%d sostituzioni. par.4-ter e 4-quater nella scheda 11." % N)
