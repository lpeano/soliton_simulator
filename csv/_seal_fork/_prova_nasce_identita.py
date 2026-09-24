# -*- coding: utf-8 -*-
"""`C1` -- **«SONO GLI STESSI ARCHI» SI PROVA PER IDENTITA', NON PER CONTEGGIO.**

> **La frase del referto `7408463` era DEDOTTA da due conteggi diversi** -- `223 396` al passo 1
> del braccio senza cure contro `223 380` al passo 0 del braccio con. **Due numeri vicini non
> sono un'identita': e' lo `STANDARD 9`** *(una presenza, come un'assenza, non si dichiara da
> un indizio)*. *(Rilievo di Luca, 2026-09-24.)*

**LA PROVA VERA, al PASSO ZERO, un processo per braccio** *(`STANDARD 1`)*:

```
d_off   il driver con `--scala-min-passo=off`   ->  `_nasce` NON tronca
d_on    il driver nudo                          ->  `_nasce` tronca
CRITERIO:   d_on.tobytes() == np.maximum(d_off, LAM).tobytes()
```

**E' un'identita' di BYTE** *(`STANDARD 2`)*, non un `max|delta|`: se `_nasce` fosse
`np.maximum` **e nient'altro**, i byte coincidono. **Se non coincidono, fa anche altro.**

**L'argv si LEGGE dal driver** *(`csv/_testa_driver.py`)*, non si ricopia *(`P1-ter`, `C4`)*.
ASCII puro.
"""
import hashlib
import io
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_sig_cura2", "PROVA_nasce_identita.txt")
TMP = os.path.join(_QUI, "_sig_cura2", "_nasce_tmp")

FIGLIO = r'''
import os, sys, numpy as np
sys.path.insert(0, os.path.join(RAD, "csv"))
import _testa_driver as T
S, argv, g = T.esegui(os.path.join(TMPD, "_scarto"), EXTRA)
S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = float(SEPV)
S._NMASSE_VIDEO["size"] = None
S.avvia_test("N-MASSE")()
net = S.net
d = np.ascontiguousarray(np.asarray(net.d, dtype=float))
np.save(os.path.join(TMPD, NOME + ".npy"), d)
print("OK %s n=%d archi=%d LAM=%.9f SCALA_MIN=%s SCALA_MIN_PASSO=%s nascite=%s"
      % (NOME, net.n, d.size, S.LAM, S.SCALA_MIN, S.SCALA_MIN_PASSO,
         getattr(net, "_g_sm_nascite", 0)))
print("ARGVSIM " + " ".join(argv))
'''


def braccio(nome, extra, sep, P):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nEXTRA = %r\nSEPV = %r\n"
           % (RADICE, TMP, nome, extra, sep)) + FIGLIO
    r = subprocess.run([sys.executable, "-c", src], cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    righe = (r.stdout or "").splitlines()
    ok = [x for x in righe if x.startswith("OK ")]
    av = [x for x in righe if x.startswith("ARGVSIM ")]
    if r.returncode != 0 or not ok:
        P("  *** braccio %s MORTO (rc=%d) ***\n%s\n"
          % (nome, r.returncode, ((r.stdout or "") + (r.stderr or ""))[-2500:]))
        return None, None
    P("  %s\n" % ok[0][3:])
    return np.load(os.path.join(TMP, nome + ".npy")), (av[0][8:] if av else "")


def main():
    try:
        os.makedirs(TMP)
    except OSError:
        pass
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    P("# `C1` -- LA PROVA PER IDENTITA': `_nasce` e' `np.maximum(d, LAM)` E NIENT'ALTRO?\n#\n")
    P("# Passo ZERO, un processo per braccio (`STANDARD 1`). Argv LETTA dal driver.\n#\n")
    # il `--sep` del driver: si LEGGE, non si assume
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _testa_driver as T
    _t = io.open(T.DRIVER, encoding="utf-8").read()
    import re
    m = re.search(r'^SEP = "([^"]+)"', _t, re.M)
    sep = m.group(1) if m else "?"
    P("  `--sep` DEL DRIVER, letto dal sorgente: %s\n\n" % sep)

    d_on, av_on = braccio("on", [], sep, P)
    d_off, av_off = braccio("off", ["--scala-min-passo=off"], sep, P)
    if d_on is None or d_off is None:
        f.close()
        return 1

    # LAM dal simulatore, non ricopiato
    sys.path.insert(0, RADICE)
    import soliton_simulator as _S
    LAM = _S.LAM
    P("\n  LAM = %.9f (letto dal simulatore)\n" % LAM)
    P("  forma: d_on %s  d_off %s\n" % (d_on.shape, d_off.shape))

    P("\n" + "=" * 100 + "\nIL CRITERIO\n" + "=" * 100 + "\n")
    if d_on.shape != d_off.shape:
        P("  *** FORME DIVERSE: il confronto non ha nulla da confrontare ***\n")
        P("  (e' la trappola del `max|A-B| = 0` per MANCANZA DI CONFRONTO)\n")
        f.close()
        return 1
    att = np.ascontiguousarray(np.maximum(d_off, LAM))
    ok = (d_on.tobytes() == att.tobytes())
    P("  sha1(d_on)               = %s\n" % hashlib.sha1(d_on.tobytes()).hexdigest()[:16])
    P("  sha1(max(d_off, LAM))    = %s\n" % hashlib.sha1(att.tobytes()).hexdigest()[:16])
    P("  IDENTICI BIT A BIT       = %s\n" % ok)
    P("\n  -> %s\n" % ("**PASS. `_nasce` e' `np.maximum(d, LAM)` E NIENT'ALTRO**, e «sono gli\n"
                       "     stessi archi» NON e' piu' una deduzione da due conteggi: e'\n"
                       "     un'IDENTITA' DI BYTE."
                       if ok else
                       "*** FAIL: `_nasce` fa ANCHE ALTRO. La frase del referto va RITIRATA. ***"))
    div = int(np.sum(d_on != att))
    P("     elementi diversi: %d su %d\n" % (div, d_on.size))

    P("\n" + "=" * 100 + "\nI NUMERI CHIESTI\n" + "=" * 100 + "\n")
    sotto = int(np.sum(d_off < LAM))
    P("  min(d_off)/LAM           = %.6f\n" % (float(d_off.min()) / LAM))
    P("  archi con d_off < LAM    = %d su %d (%.2f %%)\n"
      % (sotto, d_off.size, 100.0 * sotto / d_off.size))
    P("  archi con d_on == LAM    = %d\n" % int(np.sum(d_on == LAM)))
    P("  min(d_on)/LAM            = %.6f\n" % (float(d_on.min()) / LAM))
    P("\n  -> i TRE numeri devono coincidere: `d_off < LAM`, `d_on == LAM`, e il conteggio\n")
    P("     del referto. **Se coincidono, sono davvero GLI STESSI ARCHI.**\n")

    P("\n  argv del simulatore, braccio ON:\n    %s\n" % (av_on or "?"))
    P("  (differenza col braccio OFF: solo `SCALA_MIN_PASSO`)\n")
    f.close()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
