# -*- coding: utf-8 -*-
r"""**LA CORSA DI SEPARAZIONE COL BORDO UGUALE A QUELLO DI `L 81`** *(Luca `2026-11-14` `17:02`, (1); la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `19.6`)*.

    python csv/solitone/convergenza_b28.py --registro conv-U-L162b28 > <scratchpad>/conv_U_L162b28.txt

### **(MU) su `L 162` col bordo UGUALE a quello di `L 81` IN TUTTO:** **`R_A = 28`, `R_B = 40.5`** *(la rampa `sin^2` ripida da `28` a `40.5`)*, **`g_max` oltre `40.5` fino agli angoli;** **calcolato con
`bordo.profilo(r, 28, 40.5, g_max)` sugli anelli di `campo.anelli`** *(le righe di `bordo.g_estremita` con `R_B` dato invece della meta' del periodo)*. **`bordo.py` e `convergenza.py` NON si toccano**
*(`convergenza.py` e' in uso da `conv-U-L162`)*: **`bordo.g_estremita` si sostituisce IN MEMORIA per questa corsa, poi `convergenza.main` con `--bordo28`** *(dichiarato)*. **Cosi' l'unica differenza con `L 81`
restano le copie periodiche.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import convergenza as CV  # noqa: E402

R_A_81, R_B_81 = 28.0, 40.5            # ### Luca 17:02: il bordo di L 81 (bordo.R_A; R_B la meta' del periodo di L 81)


def main(argv):
    import _presidio
    from solitone import bordo as BO
    from solitone import campo as CP
    from solitone import toro as TO
    for m in ("convergenza",):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    assert R_B_81 == TO.meta_periodo(81), "R_B di L 81 NON e' 40.5"

    def g_estremita_81(z, c1, c2, R_A_, g_max):
        """### Le righe di `bordo.g_estremita` con `R_B = 40.5` *(il bordo di `L 81`)*."""
        L = z["L"]
        v = np.arange(z["inc"].n)
        _k, r = CP.anelli(v // L, v % L, c1, c2, L, float("inf"))
        gn = BO.profilo(r, R_A_, R_B_81, g_max)
        return gn[z["inc"].nodo], gn, r
    vero = BO.g_estremita
    BO.g_estremita = g_estremita_81
    print("### LA CORSA DI SEPARAZIONE (Luca 17:02): bordo.g_estremita SOSTITUITA in memoria: il profilo sin^2 da R_A %g a R_B %g (come L 81), g_max oltre; poi convergenza.py --mondo U --L 162 --bordo28" % (R_A_81, R_B_81))
    print("### (la riga di convergenza.py che stampa «R_B ... la meta' del periodo» dice il valore di TO.meta_periodo: il bordo VERO di questa corsa e' quello sopra)")
    try:
        return CV.main(["corsa", "--mondo", "U", "--L", "162", "--bordo28"] + list(argv))
    finally:
        BO.g_estremita = vero


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
