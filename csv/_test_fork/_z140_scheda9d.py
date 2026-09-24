# -*- coding: utf-8 -*-
"""Scheda 9: il clamp VIVO (correzione mia) e il criterio R esteso (richiesta di Luca)."""
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

# ---------------------------------------------------------------- (1) il clamp: correzione
A = u"""| clamp | perché sparisce |
|---|---|
| `max(tau_pp, 1e-12)` | `tau_pp` **esce dalla formula**: non c'è più nulla da proteggere |
| *(nuovo)* una divisione per `tau_arco` | `d ≥ LAM` per costruzione *(la scala minima)* e `cs_arco > 0`, quindi **`tau_arco > 0` derivato**. **Serve solo il contatore** del caso `cs_arco = 0`, che non deve capitare |"""
B = u"""### ❌ **CORREZIONE MIA: i clamp NON sono «due che spariscono». È UNO che sparisce e UNO che NASCE.**

**Avevo scritto** che *«due clamp spariscono per costruzione»*. **Il secondo era falso**, e l'ho
visto controllando invece di assumere.

| clamp | prima | dopo | verdetto |
|---|---|---|---|
| `max(tau_pp, 1e-12)` | **È CODICE MORTO**: `tau_pp = 1 + |tw|/PHI_CRIT` con `|tw| ≥ 0`, quindi **`tau_pp ≥ 1` SEMPRE** e il clamp è **irraggiungibile** | esce dalla formula | **sparisce, e non proteggeva nulla** |
| `max(tau_arco, 1e-12)` | — | **NASCE, ed è VIVO** | ⚠ **UN CLAMP IN PIÙ, non in meno** |

**Perché è vivo:** `tau_arco = d/cs_arco` si annulla se `d = 0`, e **`d ≥ LAM` vale solo con
`SCALA_MIN` oppure `SCALA_MIN_PASSO` accesi** *(il pavimento di `_nasce`)*. **È una dipendenza,
e va dichiarata.**

**MISURATO nel giro di `CURA 1`** *(`SCALA_MIN = False`, **`SCALA_MIN_PASSO = True`**)*:

| | |
|---|--:|
| `LAM` | **`0.8`** |
| `min(d)` | **`0.800000`** — **esattamente `LAM`** |
| `min(d)/LAM` | **`1.0000`** |
| archi con `d < LAM` | **`0` su `526302`** |

> **Quindi nella configurazione dei run il clamp non morde — ma NON per costruzione: per via di
> un FLAG.** Si scrive il clamp, **si CONTA**, e si dichiara che la garanzia viene da
> `SCALA_MIN_PASSO`. **`A11`: un limite ammesso solo se esprime un vincolo dichiarato** — qui il
> vincolo è *«nessuna lunghezza sotto `LAM`»*, che è una legge del sistema, **non una
> protezione da un errore.** È legittimo **a condizione di dirlo.**
>
> **⚠ E IL CONTO DI PRIMA ERA SBAGLIATO PURE NEL NUMERO:** avevo scritto `min(d)/LAM = 2.0000`
> perché il mio script aveva `LAM = 0.4` cablato a mano invece di leggerlo. **`LAM` è `0.8`**, e
> il rapporto è **`1.0000`**. *(`P1-ter`: un numero ricopiato a mano non ha provenienza.)*"""
t = s1(t, A, B)
t = s1(t, u"### ✅ **E DUE CLAMP SPARISCONO PER COSTRUZIONE** *(`A11`)*",
       u"### ⚠ **I CLAMP: uno SPARISCE, uno NASCE** *(`A11`)*")

# ---------------------------------------------------------------- (2) criterio R esteso
A2 = (u"| **`R`** | **`med d0`, `med d/d0`, e il TERMINE DELLA REPULSIONE nel bilancio**, "
      u"contro `_cura1_corto` |")
B2 = (u"| **`R`** | **`d0` e `d/d0` con i QUANTILI (`p10`, mediana, `p90`) e la divisione "
      u"VUOTO / CONFINE / MASSA**, più il **TERMINE DELLA REPULSIONE nel bilancio**, contro "
      u"`_cura1_corto` |")
t = s1(t, A2, B2)

A3 = (u"**circa ×2.5-×3**. **Si RIPORTA il verso e l'ampiezza**, e se `d0` si allarga **non è una "
      u"sorpresa: è la previsione** |")
B3 = (u"**circa ×2.5-×3**. **Si RIPORTA il verso e l'ampiezza**, e se `d0` si allarga **non è una "
      u"sorpresa: è la previsione**. "
      u"**⚠ E LA MEDIANA DA SOLA NON BASTA — rilievo di Luca, 2026-09-24:** *«la mediana è un "
      u"riassunto GLOBALE di un rapporto LOCALE: può nascondere compressione e stiramento che si "
      u"COMPENSANO»*. Quindi **`p10`, mediana, `p90`** e la **divisione per classe d'arco**, con "
      u"la **stessa convenzione di `G1`-`G2`** *(`csv/_test_fork/_dove_spinge_la_gravita.py:72-78`: "
      u"nodo `< 900` = **VUOTO**, `< 2391` = **MASSA seminata**, oltre = **NATO**; l'arco prende "
      u"la coppia delle due classi)* — **non una convenzione nuova**. "
      u"**E `A2` vale: statistiche globali SOLO nel referto, MAI nella legge.** La legge tocca "
      u"`ampiezza_int`, `ampiezza_ev`, `rep`, `prob`, `_rep`, `grad_r`: **nessuna di queste legge "
      u"una statistica globale.** |")
t = s1(t, A3, B3)

io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("%d sostituzioni: il clamp corretto, il criterio R esteso." % N)
