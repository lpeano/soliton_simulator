# -*- coding: utf-8 -*-
r"""**E1, `v_max/s` IN FUNZIONE DI `theta = c s`** *(Luca `2026-11-09` `16:18`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `21`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_e1.py > doc/referti_l2/u1_e1.txt

**`theta = c s`** *(la variante di `_u1_terzo`: `espi(K s)`, `K = c / pi`)*, **`c` in {`2`, `pi`, `4`, `8.48`}, a `eps 0.5`; `v_max/s` a `s` `0.01`, `0.005`, `0.001` (il limite) e `0.15`.**
**I DEVE:** `E1-R` *(a `c = pi`, `s 0.15`: `0.588137` di P1 entro `1e-6`)*; `E1-F` *(DEVE FALLIRE: contro `0.601963`, il valore a `eps 0`)*. **Le letture:** `e-p` *(proporzionale entro `2%`)* / `e-n`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

C_E1 = (2.0, math.pi, 4.0, 8.48)   # ### Luca 16:18
EPS_E1 = 0.5                       # ### la moneta della tabella
S_LIM = (0.01, 0.005, 0.001)       # ### sez. 21: il limite col fit di grado 2
S_CORSA = 0.15
RIF_P1 = 0.588137                  # ### doc/referti_l2/u1_p1.txt (eps 0.5, s 0.15)
RIF_EPS0 = 0.601963                # ### doc/referti_l2/u1_p1.txt (eps 0, s 0.15)
TOLL = 1e-6
TOLL_PROP = 0.02                   # ### sez. 21: il 2%, mio, dichiarato
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def main():
    import _presidio
    import _triangoli_forza as TF
    import _u1_terzo as U3
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_terzo.py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_triangoli_forza.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("E1, v_max/s IN FUNZIONE DI theta = c s (sez. 21): c %s (K = c/pi), eps %g, s %s (il limite) e %g" % (["%.6f" % c for c in C_E1], EPS_E1, S_LIM, S_CORSA))
    print("=" * 130)
    ris = {}
    for c in C_E1:
        K = c / math.pi
        with U3.variante(K):
            for s in S_LIM + (S_CORSA,):
                ris[(c, s)] = TF.v_max(TF.matrice_L(EPS_E1, s))[0] / s
        ss = np.array(S_LIM)
        f0 = float(np.polyfit(ss, np.array([ris[(c, s)] for s in S_LIM]), 2)[2])
        ris[(c, "lim")] = f0
        print("  c %.6f (K %.6f): v_max/s %s | a s %g: %.8f | il limite %.8f | il limite / c %.8f" % (c, K, " ".join("%.8f" % ris[(c, s)] for s in S_LIM), S_CORSA, ris[(c, S_CORSA)], f0, f0 / c))
        sys.stdout.flush()
    print("-" * 130)
    esito("E1-R a c = pi, s %g: v_max/s = %.6f di P1 entro %g (la variante a K = 1 e' il tick di oggi)" % (S_CORSA, RIF_P1, TOLL), abs(ris[(math.pi, S_CORSA)] - RIF_P1) <= TOLL, "%.8f" % ris[(math.pi, S_CORSA)])
    esito("E1-F lo stesso contro il valore a eps 0 (%.6f)" % RIF_EPS0, abs(ris[(math.pi, S_CORSA)] - RIF_EPS0) <= TOLL, "%.8f" % ris[(math.pi, S_CORSA)], deve=False)
    rap = np.array([ris[(c, "lim")] / c for c in C_E1])
    disp = float((rap.max() - rap.min()) / rap.mean())
    lc = np.log(np.array(C_E1))
    a = float(np.polyfit(lc, np.log([ris[(c, "lim")] for c in C_E1]), 1)[0])
    print("  il rapporto (v_max/s) / c nel limite: %s; la dispersione (max - min) / media %.4f; la pendenza di ln v_max contro ln c %.4f" % (" ".join("%.6f" % x for x in rap), disp, a))
    print("  LA LETTURA: (%s)" % ("e-p: proporzionale a c entro %g: B ha ancora senso" % TOLL_PROP if disp <= TOLL_PROP else "e-n: NON proporzionale a c (la dispersione %.3f): B va ripensata" % disp))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
