# -*- coding: utf-8 -*-
"""Scheda 11, par.4-bis: la correzione di Ito, valutata. Nessun codice."""
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
B = u"""## 4-bis. ❓ **LA CORREZIONE DI ITÔ** — *proposta del guardiano, e la scelta è di Luca*

> **La deriva residua viene dalla CONVESSITÀ di `exp`.** La correzione derivata la toglie:
>
> ```
> (d − LAM)  ←  (d − LAM) · exp(dx/d − (dx/d)²/2)
> ```

**Verificato numericamente, non solo algebricamente** *(`csv/_test_fork/_z147_ito.py`)*. Con
`s = a/d`:

| `s` | **piana** `E[f]−1` | attesa `s²/2` | **Itô** `E[f]−1` | attesa `−s⁴/12` | `\|Itô\|/\|piana\|` |
|--:|--:|--:|--:|--:|--:|
| `0.250` | `+3.141310e-02` | `3.125e-02` | **`−3.201451e-04`** | `−3.255e-04` | `1.019e-02` |
| `0.125` | `+7.822678e-03` | `7.813e-03` | **`−2.026048e-05`** | `−2.035e-05` | `2.590e-03` |
| `0.0625` | `+1.953761e-03` | `1.953e-03` | **`−1.270242e-06`** | `−1.272e-06` | `6.502e-04` |

**E l'ORDINE si legge raddoppiando `s`:**

| | piana | Itô |
|---|--:|--:|
| `s: 0.0625 → 0.125` | **`×4.004`** *(atteso `2² = 4`)* | **`×15.950`** *(atteso `2⁴ = 16`)* |
| `s: 0.125 → 0.25` | **`×4.016`** | **`×15.801`** |

> **La deriva scende dal SECONDO al QUARTO ordine**, e **cambia SEGNO: diventa NEGATIVA**,
> cioè **verso il confine** invece che lontano da esso.

### ✅ **E c'è un secondo guadagno che la sola deriva non mostra: la FEDELTÀ**

Entrambe le forme tendono alla legge **`u ← u(1 + x)`**, con `x = dx/d`. **Quanto le si
avvicinano:**

| `x` | `u(1+x)` | **piana** | eccesso | **Itô** | eccesso |
|--:|--:|--:|--:|--:|--:|
| `0.1` | `1.10000` | `1.10517` | **`+5.17e-03`** | `1.09966` | **`−3.41e-04`** |
| `0.3` | `1.30000` | `1.34986` | **`+4.99e-02`** | `1.29046` | **`−9.54e-03`** |

**`exp(x − x²/2) = 1 + x + O(x³)`: i termini in `x²` si cancellano ESATTAMENTE.**
Quindi, **su una spinta DETERMINISTICA**, la correzione **non è un bias: toglie l'eccesso di
convessità della piana**, ed è **più fedele** alla legge voluta, non meno.

> **⚠ Il «bias verso il basso di ordine `dx²`» è vero RELATIVAMENTE ALLA PIANA, non
> relativamente alla LEGGE.** Va detto così, perché le due letture portano a decisioni opposte.

### ❌ **MA C'È UN COSTO, e non è nella deriva: la forma NON È MONOTONA**

`f(x) = exp(x − x²/2)` ha **massimo in `x = 1`**, dove vale `√e = 1.64872`. **E poi scende:**

| `x` | piana `exp(x)` | **Itô** | |
|--:|--:|--:|---|
| `0.5` | `1.64872` | `1.45499` | |
| **`1.0`** | `2.71828` | **`1.64872`** | **← il MASSIMO** |
| `1.5` | `4.48169` | `1.45499` | |
| `2.0` | `7.38906` | `1.00000` | **← una salita non muove nulla** |
| `2.5` | `12.18249` | **`0.53526`** | **← UNA SALITA FA SCENDERE** |
| `3.0` | `20.08554` | **`0.22313`** | |

> ### ❗ **Per `dx > 2d` la forma di Itô TRASFORMA UNA SALITA IN UNA DISCESA.**
> **La piana è monotona sempre.** E qualunque salita, con Itô, **non può far crescere `u` di
> più di `√e ≈ 1.6487`** in una scrittura.
>
> **È esattamente la firma che `A11` cerca:** *una spinta più grande che produce un effetto
> più piccolo.* **Non è un difetto se `\|dx\|/d` resta piccolo — ma «resta piccolo» è una
> MISURA, non un'assunzione.**

### **IL CONFRONTO, in una tabella sola**

| | **piana** `exp(x)` | **Itô** `exp(x − x²/2)` |
|---|---|---|
| deriva, rumore simmetrico | `+u·s²/2` — **2° ordine, POSITIVA** *(lontano dal muro)* | **`−u·s⁴/12` — 4° ordine, NEGATIVA** *(verso il muro)* |
| fedeltà a `u(1+x)` | eccesso `+x²/2` | **esatta a `O(x³)`** |
| mai sotto `LAM` | ✅ | ✅ |
| **monotona in `dx`** | **✅ sempre** | **❌ massimo a `x=1`; per `x>2` una salita fa SCENDERE** |
| tetto per scrittura | nessuno | `u·√e ≈ 1.6487·u` |

### ⚠ **E UNA CONSEGUENZA CHE TOCCA UN ALTRO FRONTE**

**La deriva di Itô è NEGATIVA: spinge gli archi PIANO VERSO il muro**, mentre quella di oggi
li spinge **lontano**. **È debolissima** *(`4°` ordine)*, ma il verso è opposto — e la domanda
**«chi spinge gli archi contro il muro»** è già aperta come **`D33` / `S05`**. **Aggiungere una
spinta verso il muro, per quanto piccola, va detto a chi indaga quel fronte.**

> ### **LA SCELTA È DI LUCA, e non la prendo io.** Il criterio che la decide è **misurabile**:
> **la distribuzione di `\|dx\|/d`.** Se resta ben sotto `1`, **Itô è migliore su tutto** e la
> non-monotonia non si manifesta mai. Se arriva vicino a `1`, il tetto `√e` comincia a mordere,
> e **a `2` inverte**. → punti `V8` e `V9` della verifica.

## 5. ❌ **PERCHÉ NON `exp(dx/u)`** — la variabile `log(d − LAM)`"""
t = s1(t, A, B)

# i due punti nuovi della verifica
A2 = (u"| **`V7`** | **mai sotto `LAM`**: una discesa enorme, `dx = −100·d` | oggi "
      u"**attraversa**; la proposta **no**, per qualunque passo |")
B2 = (A2 + u"\n| **`V8`** | **la DISTRIBUZIONE di `\|dx\|/d`**, non solo il suo tipico | è **il "
      u"numero che decide fra piana e Itô**: `p50`, `p99`, `max`. Se `max ≪ 1` la non-monotonia "
      u"di Itô **non si manifesta mai** |\n"
      u"| **`V9`** | **quante scritture hanno `\|dx\|/d > 1`, e quante `> 2`** | `> 1`: Itô "
      u"**comprime**; `> 2`: Itô **inverte il verso**. **Se sono zero, la scelta è libera; se "
      u"non lo sono, la piana è l'unica monotona** |")
t = s1(t, A2, B2)

# cosa non so derivare
A3 = (u"4. **chi spinge gli archi contro il muro.** La proposta toglie **il cricchetto del "
      u"freno**, non\n   la **causa** per cui gli archi ci arrivano. **Resta aperta e "
      u"SEPARATA:** `D33` e `S05`.")
B3 = (A3 + u"\n5. **se la non-monotonia di Itô si manifesti davvero.** Dipende da `\|dx\|/d`, che "
      u"**non è\n   misurato** — punti `V8`/`V9`. **Senza quel numero la scelta fra le due forme "
      u"non ha una\n   base derivata**, e resta di Luca;\n"
      u"6. **se una deriva NEGATIVA di quarto ordine sia preferibile a una POSITIVA di secondo.** "
      u"È\n   più piccola di ordini di grandezza, **ma va verso il muro** — e la domanda "
      u"«chi spinge gli\n   archi contro il muro» è un fronte aperto. **Più piccolo non è "
      u"automaticamente meglio quando\n   il SEGNO cambia.**")
t = s1(t, A3, B3)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("%d sostituzioni. Il par.4-bis (Ito) e i punti V8/V9 sono nella scheda 11." % N)
