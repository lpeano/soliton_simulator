r"""**`C1` NELLA FORMA COL SEGNO** — dai json GIA' SCRITTI, nessun rigiro del simulatore.

> **Il criterio vecchio non era soddisfacibile**, e non lo dice il dato: lo dice il **collaudo**
> (`csv/_collaudo_criterio_zero.py`, `doc/COLLAUDO_criterio_zero.txt`). Su **rumore puro** — cioe'
> con la cura **perfetta** e solo la dispersione fra semi — la forma con `|x|` **fallisce
> l'85.89 %** delle volte, con `media/SE` tipica **`2.897`**. **Un criterio che fallisce quasi
> sempre quando non c'e' nulla da trovare non misura nulla.**

```
VECCHIO   media( |pend(contrasto) - pend(coppia)| )  <=  2 * SE(|...|)
NUOVO     | media( pend(contrasto) - pend(coppia) ) |  <=  2 * SE(...)     <- FIRMATE
```

**La differenza e' il VALORE ASSOLUTO:** la media di quantita' tutte positive **non puo'** essere
compatibile con zero; la media di quantita' **firmate** puo', **se i segni si compensano** — che e'
esattamente cio' che deve accadere quando resta solo rumore.

**`(b)` resta invariato:** la media ON sta **sotto** quella del braccio `/W`. *(Qui si usano i
**moduli**, perche' `(b)` confronta **quanto** le due forme si discostano, non in che verso: e' una
scelta, e la dichiaro.)*

**SOLA LETTURA: si leggono i json dei bracci `on_*` e `suW_*` del sigillo della cura A.** Nessun
simulatore gira, e le pendenze si ricalcolano con **la stessa funzione** `pend` del sigillo —
copiata, non riscritta.

ASCII puro.
"""
# ESENTE-P5: legge JSON gia' scritti e non fa girare il simulatore. La configurazione di quei dati
#   e' dichiarata NEL REFERTO DEL SIGILLO che li ha prodotti (`P5` la stampa li'), e ripeterla qui
#   sarebbe una copia non verificata invece di una dichiarazione.
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
TMP = os.path.join(_QUI, "_sig_cura_A", "_tmp")
DEST = os.path.join(_QUI, "_sig_cura_A", "C1_COL_SEGNO.txt")
NL = chr(10)


def pend(x, y):
    """LA STESSA funzione del sigillo, copiata: riscriverla sarebbe una seconda formula."""
    x = np.log(np.asarray(x, float))
    y = np.asarray(y, float)
    m = np.isfinite(y) & (y > 0) & np.isfinite(x)
    if m.sum() < 3:
        return float("nan")
    return float(np.polyfit(x[m], np.log(y[m]), 1)[0])


R = []


def P(s=""):
    R.append(s)


def leggi(nome):
    p = os.path.join(TMP, nome + ".json")
    if not os.path.exists(p):
        return None
    try:
        return json.loads(io.open(p, encoding="utf-8").read())
    except Exception:
        return None


def differenze(prefisso):
    """`{verso: {seme: pend(contrasto) - pend(coppia)}}`, FIRMATE."""
    fuori = {}
    for f in sorted(os.listdir(TMP)):
        if not f.endswith(".json") or not f.startswith(prefisso + "_s"):
            continue
        nome = f[:-5]
        o = leggi(nome)
        if not o or not o.get("casi"):
            continue
        cc = [c for c in o["casi"] if "errore" not in c]
        if len(cc) < 3:
            continue
        ks = [c["K"] for c in cc]
        pc = pend(ks, [c["coppia_p50"] for c in cc])
        px = pend(ks, [c["contrasto_p50"] for c in cc])
        _sm = nome.split("_")[1]
        _vs = nome.rsplit("_", 1)[-1]
        fuori.setdefault(_vs, {})[_sm] = (px - pc, pc, px, o.get("blob_sim"), o.get("quando"))
    return fuori


ON = differenze("on")
SUW = differenze("suW")
OFF = differenze("off")

P("=" * 104)
P("`C1` NELLA FORMA COL SEGNO -- dai json GIA' SCRITTI   (2026-09-26)")
P("=" * 104)
P()
P("  Nessun rigiro del simulatore: si leggono i json dei bracci del sigillo della cura A,")
P("  e le pendenze si ricalcolano con **la stessa funzione `pend`** del sigillo, copiata.")
P("  La configurazione e' quella dichiarata nel referto del sigillo (`P5` la stampa li').")
P()
P("  ⚠ **IL MOTIVO DEL CAMBIO E' IL COLLAUDO, NON IL DATO:** su rumore puro la forma con `|x|`")
P("    fallisce l'**85.89 %** delle volte (`media/SE` tipica `2.897`), la forma col segno passa")
P("    l'**86.13 %**. *(`doc/COLLAUDO_criterio_zero.txt`, committato PRIMA di questi numeri.)*")
P()
P("%-9s %-7s %-13s %-13s %-15s %s"
  % ("verso", "seme", "pend.coppia", "pend.contrasto", "DIFFERENZA", "blob / quando"))
for _v in sorted(ON):
    for _s in sorted(ON[_v]):
        d, pc, px, bl, qd = ON[_v][_s]
        P("%-9s %-7s %-13.4f %-13.4f %+15.4f %s / %s"
          % (_v, _s, pc, px, d, bl, (qd or "")[:19]))
P()

P("=" * 104)
P("`(a')` -- LA MEDIA DELLE DIFFERENZE **FIRMATE** E' COMPATIBILE CON ZERO?")
P("=" * 104)
P("%-9s %-6s %-40s %-11s %-11s %-11s %s"
  % ("verso", "semi", "differenze firmate", "media", "SE", "|media|/SE", "esito"))
esiti_a, esiti_b = {}, {}
for _v in sorted(ON):
    x = np.array([ON[_v][s][0] for s in sorted(ON[_v])], float)
    if x.size < 2:
        continue
    m = float(np.mean(x))
    se = float(np.std(x, ddof=1)) / np.sqrt(x.size)
    rap = abs(m) / se if se else float("nan")
    ok = abs(m) <= 2.0 * se
    esiti_a[_v] = (x.size, m, se, rap, ok)
    P("%-9s %-6d %-40s %+11.4f %-11.4f %-11.4f %s"
      % (_v, x.size, "  ".join("%+.4f" % q for q in x), m, se, rap,
         "COMPATIBILE" if ok else "NON compatibile"))
P()
P("=" * 104)
P("`(b)` -- LA MEDIA ON STA SOTTO QUELLA DI `/W`?  *(sui MODULI: `(b)` confronta QUANTO, non il verso)*")
P("=" * 104)
P("%-9s %-14s %-14s %-14s %s" % ("verso", "media|ON|", "media|/W|", "rapporto", "esito"))
for _v in sorted(ON):
    a_ = float(np.mean([abs(ON[_v][s][0]) for s in sorted(ON[_v])]))
    b_ = (float(np.mean([abs(SUW[_v][s][0]) for s in sorted(SUW.get(_v, {}))]))
          if SUW.get(_v) else float("nan"))
    c_ = float(np.mean([abs(OFF[_v][s][0]) for s in sorted(OFF.get(_v, {}))])) \
        if OFF.get(_v) else float("nan")
    ok = a_ < b_
    esiti_b[_v] = (a_, b_, c_, ok)
    P("%-9s %-14.4f %-14.4f %-14.4f %s"
      % (_v, a_, b_, (b_ / a_) if a_ else float("nan"), "ON STA SOTTO" if ok else "ON NON sta sotto"))
    P("%-9s %-14s OFF %.4f  (rapporto OFF/ON %.4g)" % ("", "", c_, (c_ / a_) if a_ else float("nan")))
P()

_A = bool(esiti_a) and all(v[4] for v in esiti_a.values())
_B = bool(esiti_b) and all(v[3] for v in esiti_b.values())
P("=" * 104)
P("ESITO DI `C1` COL SEGNO:  (a') %s      (b) %s      ->  %s"
  % ("PASS" if _A else "FAIL", "PASS" if _B else "FAIL",
     "PASS" if (_A and _B) else "FAIL"))
P("=" * 104)
P()
P("  CONFRONTO COL NUMERO DEL GUARDIANO (Luca), che va detto anche se coincide:")
P("    atteso   lunghi |media|/SE 0.97      corti |media|/SE 1.26")
for _v in sorted(esiti_a):
    P("    misurato %-8s |media|/SE %.4f" % (_v, esiti_a[_v][3]))
P()
P("COSA QUESTO NON DICE:")
P("  - **non rimisura niente**: e' una LETTURA dei json del sigillo, con la sua configurazione.")
P("  - **`(b)` usa i MODULI**, ed e' una scelta dichiarata: confronta **quanto** le due forme si")
P("    discostano, non in che verso.")
P("  - ⚠ **con semi CORRELATI la `SE` calcolata SOTTOSTIMA quella vera**, quindi `|media|/SE` e'")
P("    **gonfiato** e il criterio fallisce **piu'** spesso: **un `FAIL` potrebbe essere un artefatto")
P("    della correlazione, un `PASS` resta informativo** *(correzione di Luca al verso che avevo")
P("    scritto)*. **La correlazione fra i semi NON e' misurata.**")
P("  - QUATTRO semi: `t(0.025,3) = 3.18`, quindi la soglia `2 SE` e' **piu' severa** di un IC95.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
sys.exit(0 if (_A and _B) else 1)
