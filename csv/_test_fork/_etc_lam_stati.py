# -*- coding: utf-8 -*-
"""**SOLA LETTURA: `min(d)` e quanti archi stanno sotto `LAM`, nei 16 stati del pilota.**

**Perche' (mandato di Luca del 2026-09-27):** la formulazione *«gli 8 pavimenti sono MORTI»* e'
imprecisa e va corretta. **Morto e' il pavimento VECCHIO** -- `_floor_d0` = `0.05` assoluto,
oppure il **5 %** della mediana di `d0` con `PAV_COM`. **Al suo posto c'e' la SCALA MINIMA `LAM`**
(`SCALA_MIN_PASSO`, `_nasce`, `SEMINA_LAM`, `MITOSI_2LAM`), **che e' VIVA**. Questo strumento
misura **che la legge viva sia rispettata negli stati gia' salvati**.

**NESSUN RUN.** Si leggono i 16 `.npz` del pilota (`d`, `i`, `j`, `n`) e basta.
**`LAM` si legge DAL SORGENTE**, non si ricopia: si importa il modulo senza configurarlo.
⚠ **E `LAM` puo' essere riscalato dal coarse-graining** (`--scala`): qui si riporta il valore
**del sorgente** e si dichiara, invece di assumere che il run girasse a scala 1.

COMANDO:  python csv/_test_fork/_etc_lam_stati.py
"""
import io
import json
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)

SIM = os.path.join(RADICE, "soliton_simulator.py")
STATI = os.path.join(_QUI, "_pilota_prova1", "stati")

# LAM dal SORGENTE, per lettura del testo: importare il modulo lo farebbe girare.
_t = io.open(SIM, encoding="utf-8").read()
LAM = float(re.search(r"^LAM\s*=\s*([0-9.eE+-]+)", _t, re.M).group(1))
LAM_BASE = float(re.search(r"^LAM_BASE\s*=\s*([0-9.eE+-]+)", _t, re.M).group(1))
PAV_VECCHIO = 0.05
print("LAM = %g   LAM_BASE = %g   (letti dal sorgente %s)"
      % (LAM, LAM_BASE, os.path.basename(SIM)))
print("il PAVIMENTO VECCHIO era %g assoluto, oppure %g * median(d0) con PAV_COM"
      % (PAV_VECCHIO, PAV_VECCHIO / LAM_BASE))
print("")

nomi = sorted(x for x in os.listdir(STATI) if x.startswith("stato_") and x.endswith(".npz"))
print("stati trovati: %d" % len(nomi))
print("")
print("  %-6s %-7s %-9s %-9s %-14s %-12s %s"
      % ("seme", "passo", "n", "m", "min(d)", "min/LAM", "archi d < LAM"))
R = []
for nm in nomi:
    z = np.load(os.path.join(STATI, nm), allow_pickle=True)
    d = np.asarray(z["d"], dtype=float)
    seme = int(z["seme"]) if "seme" in z.files else -1
    passo = int(z["passo"]) if "passo" in z.files else -1
    n = int(z["n"]) if "n" in z.files else -1
    sotto = int(np.sum(d < LAM))
    mn = float(d.min()) if len(d) else float("nan")
    R.append({"file": nm, "seme": seme, "passo": passo, "n": n, "m": int(len(d)),
              "min_d": mn, "sotto_LAM": sotto,
              "frazione_sotto": (sotto / float(len(d))) if len(d) else 0.0,
              "min_su_LAM": mn / LAM if len(d) else float("nan"),
              "sotto_pav_vecchio": int(np.sum(d < PAV_VECCHIO))})
    print("  %-6d %-7d %-9d %-9d %-14.6f %-12.4f %d"
          % (seme, passo, n, len(d), mn, mn / LAM, sotto))

print("")
print("=" * 78)
tot_sotto = sum(r["sotto_LAM"] for r in R)
peggio = min(R, key=lambda r: r["min_d"])
print("  archi sotto LAM, SOMMATI su tutti i 16 stati : %d" % tot_sotto)
print("  il minimo assoluto                           : %.6f  (seme %d, passo %d) = %.4f * LAM"
      % (peggio["min_d"], peggio["seme"], peggio["passo"], peggio["min_d"] / LAM))
print("  archi sotto il PAVIMENTO VECCHIO (%g), sommati: %d"
      % (PAV_VECCHIO, sum(r["sotto_pav_vecchio"] for r in R)))
print("")
if tot_sotto == 0:
    print("  ### LA LEGGE VIVA E' RISPETTATA: nessun arco sotto LAM in nessuno dei 16 stati.")
    print("      E il minimo sta ESATTAMENTE a LAM: la legge viva MORDE, e tiene.")
    print("      Il pavimento VECCHIO (%g) sta %.0f volte PIU' IN BASSO del minimo (%.6f):"
          % (PAV_VECCHIO, peggio["min_d"] / PAV_VECCHIO, peggio["min_d"]))
    print("      non avrebbe potuto mordere nemmeno se fosse stato vivo.")
else:
    print("  ### ATTENZIONE: %d archi sotto LAM. La legge viva NON e' rispettata." % tot_sotto)
print("=" * 78)

OUT = os.path.join(_QUI, "_etc_lam_stati.json")
io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
    {"LAM": LAM, "LAM_BASE": LAM_BASE, "pavimento_vecchio": PAV_VECCHIO,
     "stati": R, "archi_sotto_LAM_totali": tot_sotto}, indent=1, ensure_ascii=False,
    sort_keys=True))
print("")
print("scritto: " + OUT)
