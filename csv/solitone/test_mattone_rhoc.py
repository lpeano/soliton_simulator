# -*- coding: utf-8 -*-
r"""**IL COLLAUDO DI `mattone_rhoc.py`** *(Luca `2026-11-13` `23:22`)*.

    python csv/solitone/test_mattone_rhoc.py > doc/referti_l2/mattone/collaudo_rhoc.txt

**DEVE PASSARE:** **col `rho_c` di (MG)** *(`227058.574864`)* **i primi `20` tick del ciclo di `mattone_rhoc` = i primi `20` di (MG)** *(`mattone.Campi`, il caso `MG`, la rampa `r(k)`, il bordo)* **AL BIT;**
**`N` al centro a piena rampa coerente con la legge** *(`r = 1`: `N = 1/(1 + rho/rho_c)` sul nodo del centro, lo stato di TBS a `10000`)*: **(MG/2) circa `0.974`, (MGx2) circa `0.993`** *(i numeri veri stampati)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_rhoc as MR  # noqa: E402

N_PROVA = 20
TOLL_N = 1e-3          # ### mio, dichiarato: N al centro (dal cs del tick vero) contro la legge sullo stato di partenza, a r = 1 per 1 tick
ATTESI = {"MGmezzo": 0.974, "MGdoppio": 0.993}   # ### Luca 23:22 (circa)


def main():
    import _presidio
    import _vuoto_vivo_B as V
    for m in ("mattone", "mattone_rhoc"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    print("=" * 120)
    print("IL COLLAUDO DI mattone_rhoc: %d tick; N al centro a piena rampa" % N_PROVA)
    print("=" * 120)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        Z["metti"]()
        C = MT.Campi(Z, "MG", MR.RHO_C_MG, MT.PB.E_DECISO)
        for k in range(1, N_PROVA + 1):
            C.tick(k, MT.T_BASE + k, MT.r_di(k), 0.0)
        sha_mg = V.shas(Z["z"])
        Z["metti"]()
        S, _f = MR.corsa(Z, MR.RHO_C_MG, N_PROVA, None, 0, "prova", 10 ** 9)
        sha_r = V.shas(Z["z"])
        div = [k for k in sha_mg if sha_mg[k] != sha_r[k]]
        MR.esito("col rho_c di (MG): i primi %d tick del ciclo di mattone_rhoc = (MG) AL BIT" % N_PROVA, not div, "diverse: %s" % div, True)
        for caso, rc in MR.CASI.items():
            Z["metti"]()
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            v = MR.nodo_centro(Z, c)
            Cx = MT.Campi(Z, "MG", rc, MT.PB.E_DECISO)
            Cx.tick(1, MT.T_BASE + 1, 1.0, 0.0)
            N_mis = float(np.asarray(Z["mot"].cs, dtype=float)[v] / Z["s"])
            N_legge = 1.0 / (1.0 + float(rho[v]) / rc)
            print("    %s: rho al centro %.4f; N dalla legge %.6f; N del tick vero (r = 1, 1 tick) %.6f; circa (Luca) %.3f" % (caso, rho[v], N_legge, N_mis, ATTESI[caso]))
            MR.esito("(%s) N al centro a piena rampa coerente con la legge entro %g (e circa %.3f entro 0.005)" % (caso, TOLL_N, ATTESI[caso]),
                     abs(N_mis - N_legge) <= TOLL_N and abs(N_mis - ATTESI[caso]) <= 0.005, "%.6f contro %.6f" % (N_mis, N_legge), True)
        Z["metti"]()
    print("=" * 120)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (MR.OK[0], MR.OK[1], len(MR.FALLITE), MR.FALLITE))
    return 0 if not MR.FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
