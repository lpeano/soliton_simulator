r"""**IL CRITERIO «COMPATIBILE CON ZERO» SU UN VALORE ASSOLUTO NON PUO' PASSARE** *(collaudo)*.

> **Rilievo di Luca, 2026-09-26:** `C1` chiedeva *«la media di **`|pend(contrasto)-pend(coppia)|`**
> e' compatibile con zero entro 2 SE»*. **Con il VALORE ASSOLUTO quella media NON PUO' essere
> compatibile con zero nemmeno con una cura perfetta**, perche' e' una media di quantita' tutte
> positive: il suo valore atteso e' `> 0` per costruzione, e la sua `SE` non basta a coprirlo.

**COSA MISURA QUESTO COLLAUDO** *(`P1-sexies`, e **committato PRIMA** di rileggere i numeri veri)*:
su **rumore PURO** — quattro valori `N(0, s)`, cioe' il caso in cui **la cura e' perfetta e resta
solo il rumore** — quante volte passa il criterio nelle due forme:

```
con |x|      media(|x|)  <= 2 * SE(|x|)          <- LA FORMA VECCHIA, che Luca dice mal posta
col SEGNO    |media(x)|  <= 2 * SE(x)            <- LA FORMA NUOVA
```

**LA SEPARAZIONE E' IL PUNTO:** se la forma vecchia **fallisce sulla maggioranza** del rumore puro,
allora il suo `FAIL` sui dati veri **non dice niente sulla cura** — dice che il criterio non e'
soddisfacibile. E se la forma nuova **passa** sul rumore puro, allora un suo `FAIL` **sarebbe**
informativo.

**⚠ E IL NUMERO ATTESO SI DICHIARA PRIMA, per quello che e':** per 4 valori `iid N(0,1)` la forma
col segno e' **esattamente** un `t` di Student con **3 gradi di liberta'** contro la soglia `2`,
quindi `P(|t_3| <= 2) ~ 0.86`. **Luca scrive «~90 % o piu'»: se esce `86 %` lo dico**, perche' il
criterio del collaudo e' **la SEPARAZIONE fra le due forme**, non il raggiungimento di `0.90`.

Sola lettura, nessun simulatore: e' matematica su numeri casuali.

ASCII puro.
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. E' un collaudo di un CRITERIO
#   STATISTICO su numeri casuali: non esiste una «configurazione del driver» in cui questo conto
#   sia stato fatto, e dichiararla sarebbe una riga vuota.
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "COLLAUDO_criterio_zero.txt")
NL = chr(10)

PROVE = 100000
N = 4
SEME = 20260926          # seme FISSO: il collaudo dev'essere rigirabile allo stesso numero

R = []


def P(s=""):
    R.append(s)


def passa(x, con_valore_assoluto):
    """Il criterio, nelle due forme. `x` e' `(prove, N)`."""
    if con_valore_assoluto:
        y = np.abs(x)
        m = y.mean(axis=1)
    else:
        y = x
        m = np.abs(y.mean(axis=1))
    se = y.std(axis=1, ddof=1) / np.sqrt(y.shape[1])
    return m <= 2.0 * se, m / np.maximum(se, 1e-300)


rng = np.random.default_rng(SEME)
P("=" * 100)
P("COLLAUDO DEL CRITERIO «COMPATIBILE CON ZERO» -- su RUMORE PURO   (2026-09-26)")
P("=" * 100)
P()
P("  %d prove, %d valori per prova, seme FISSO %d" % (PROVE, N, SEME))
P("  Il rumore puro e' il caso in cui **la cura e' perfetta e resta solo la dispersione fra semi**.")
P()
P("%-16s %-12s %-14s %-14s %-14s %s"
  % ("scala s", "forma", "PASSA", "media/SE p50", "media/SE p90", "lettura"))
esiti = {}
for s in (0.01, 0.05, 1.0):
    x = rng.normal(0.0, s, size=(PROVE, N))
    for con_abs, nome in ((True, "con |x|"), (False, "col SEGNO")):
        ok, rap = passa(x, con_abs)
        q = float(ok.mean())
        esiti[(s, nome)] = q
        P("%-16.3g %-12s %-14.4f %-14.4f %-14.4f %s"
          % (s, nome, q, float(np.median(rap)), float(np.percentile(rap, 90)),
             "quasi sempre FALLISCE" if q < 0.2 else
             ("quasi sempre PASSA" if q > 0.8 else "misto")))
P()
P("  ⚠ **LA SCALA `s` NON CONTA, ed e' il punto:** il criterio e' un rapporto `media/SE`, quindi")
P("    e' **invariante di scala**. Le tre righe per forma danno lo stesso numero a meno del")
P("    rumore di campionamento: **se cosi' non fosse, il collaudo sarebbe sbagliato.**")
P()
_abs = float(np.mean([esiti[(s, "con |x|")] for s in (0.01, 0.05, 1.0)]))
_sgn = float(np.mean([esiti[(s, "col SEGNO")] for s in (0.01, 0.05, 1.0)]))
P("=" * 100)
P("IL VERDETTO")
P("=" * 100)
P("  con |x|     passa il %.2f %%   ->  FALLISCE il %.2f %% delle volte SU RUMORE PURO"
  % (100.0 * _abs, 100.0 * (1.0 - _abs)))
P("  col SEGNO   passa il %.2f %%" % (100.0 * _sgn))
P()
_sep = (_abs < 0.2) and (_sgn > 0.8)
if _sep:
    P("  -> **LE DUE FORME SI SEPARANO**, e la conseguenza e' netta:")
    P("     **il `FAIL` della forma con `|x|` NON dice niente sulla cura**: quel criterio")
    P("     fallisce anche quando NON c'e' nessun effetto residuo. **Non era soddisfacibile.**")
    P("     La forma col SEGNO passa sul rumore puro, quindi un suo `FAIL` **sarebbe** informativo.")
else:
    P("  -> ⛔ **LE DUE FORME NON SI SEPARANO: STOP.** Il collaudo non dimostra quello che deve,")
    P("     e il cambio di criterio **non e' giustificato da questo conto**.")
P()
P("  ⚠ **E IL NUMERO ATTESO, dichiarato PRIMA:** per 4 valori `iid` la forma col segno e'")
P("    **esattamente** un `t` di Student con **3 gradi di liberta'** contro la soglia `2`, quindi")
P("    `P(|t_3| <= 2) ~ 0.86`. **Luca scriveva «~90 %% o piu'»: il valore vero e' `%.0f %%`, e lo"
  % (100.0 * _sgn))
P("    dico invece di arrotondarlo verso l'aspettativa.** Il criterio del collaudo e' **la")
P("    SEPARAZIONE** (`< 20 %%` contro `> 80 %%`), e quella c'e'.")
P()
P("COSA QUESTO COLLAUDO *NON* DICE:")
P("  - **non dice che la cura funzioni**: dice che **il criterio vecchio non poteva dirlo**.")
P("  - non dice che la forma col segno sia l'unica sana: dice che **e' soddisfacibile**.")
P("  - il rumore e' `N(0, s)` **indipendente**: sui dati veri i quattro semi potrebbero essere")
P("    correlati *(stessa scena, stessa geometria)*, e allora la `SE` vera sarebbe piu' grande.")
P("    **Non lo misuro qui**, e va detto.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
sys.exit(0 if _sep else 1)
