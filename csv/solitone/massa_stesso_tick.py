# -*- coding: utf-8 -*-
r"""**IL CONTROLLO DELLA MASSA ALLO STESSO TICK** *(Luca `2026-11-15` `20:40`, R1; SOLO LETTURA; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24.26`)*.

    python csv/solitone/massa_stesso_tick.py <referto.txt> <serie.npz> [...]     > <scratchpad>/massa_stesso_tick.txt
    (oggi: legati_GU_06000.txt legati_GU_serie_06000.npz  legati_GUpi_02000.txt legati_GUpi_serie_02000.npz)

### **Il DEVE di `legati.py`** *(«la massa persa = la massa uscita dal bordo entro `1e-6` relativo»)* **confrontava la massa all'ULTIMA MISURA** *(ogni `50` tick)* **col bordo all'ULTIMO TICK** *(dove il tetto ferma)*: **due istanti diversi.**
**Qui: per OGNI tick in cui ci sono tutti e due** *(la massa nella serie, ogni `50`; il bordo cumulato «bordo M» nella TABELLA DEI CONTI del referto, ogni `500` e all'ultimo tick)*, **la massa persa `M(k0) - M(k)` contro il bordo
cumulato a `k`; la differenza relativa a `M(k0)`; LA STESSA SOGLIA `1e-6`** *(non rivista)*. **E' una correzione DICHIARATA del controllo, non della soglia.**
### **Il limite, dichiarato:** **il bordo nella tabella ha `5` cifre significative** *(l'arrotondamento al piu' circa `0.05` in assoluto, contro la soglia `1e-6 x M(k0)`, circa `2`)*.
"""
import io
import os
import re
import sys

import numpy as np

SOGLIA = 1e-6


def bordo_della_tabella(f):
    """### `{k: bordo M cumulato}` dalla TABELLA DEI CONTI del referto *(l'ultima colonna)*."""
    out, dentro = {}, False
    for r in io.open(f, encoding="utf-8"):
        if "LA TABELLA DEI CONTI" in r:
            dentro = True
            continue
        if dentro:
            m = re.match(r"\s+(\d+)\s+(.*)$", r)
            if not m:
                if r.strip().startswith("k"):
                    continue
                if out:
                    break
                continue
            out[int(m.group(1))] = float(m.group(2).split()[-1])
    return out


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL CONTROLLO DELLA MASSA ALLO STESSO TICK (Luca 20:40, R1): la massa persa M(k0) - M(k) contro il bordo cumulato a k, a OGNI tick comune; la soglia %g (la stessa del DEVE)" % SOGLIA)
    print("=" * 130)
    fallite = []
    for i in range(0, len(argv), 2):
        fr, fs = argv[i], argv[i + 1]
        bo = bordo_della_tabella(fr)
        s = np.load(fs)
        k, M = [int(x) for x in s["k"]], [float(x) for x in s["M"]]
        Mk = dict(zip(k, M))
        k0 = k[0]
        comuni = sorted(x for x in bo if x in Mk and x > k0)
        print("### %s + %s: k0 %d, M(k0) %.6e; i tick comuni %d (%s ... %s); l'ultimo tick della tabella %d, l'ultima misura della serie %d"
              % (os.path.basename(fr), os.path.basename(fs), k0, Mk[k0], len(comuni), comuni[0], comuni[-1], max(bo), k[-1]))
        peggio = 0.0
        for x in comuni:
            persa = Mk[k0] - Mk[x]
            rel = abs(persa - bo[x]) / Mk[k0]
            peggio = max(peggio, rel)
            print("    k %6d: persa %.4f, bordo %.4f, la differenza %+.4f, relativa %.3e" % (x, persa, bo[x], persa - bo[x], rel))
        passa = peggio <= SOGLIA
        if not passa:
            fallite.append(os.path.basename(fr))
        print("  DEVE PASSARE: la massa persa = il bordo ALLO STESSO TICK entro %g relativo, a ogni tick comune   %s   il massimo %.3e" % (SOGLIA, "PASSA" if passa else "### FALLISCE", peggio))
        print("-" * 130)
    print("ESITO: %s" % ("TUTTI PASSANO" if not fallite else "### FALLISCONO: %s" % fallite))
    return 0 if not fallite else 1


if __name__ == "__main__":
    _QUI = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(_QUI))
    sys.exit(main(sys.argv[1:]))
