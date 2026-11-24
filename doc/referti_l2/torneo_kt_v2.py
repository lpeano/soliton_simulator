# -*- coding: utf-8 -*-
r"""**[M2351] K-T v2: LE SEI TENUTE E (a) RILETTE** *(la carta `doc/CARTA_torneo_nonlinearita.md`, sez. 13; sola lettura degli stati di `torneo_tenuta.py` e `torneo_tenuta_v2.py`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/torneo_kt_v2.py > doc/referti_l2/torneo_kt_v2.txt

**K-T v2** *(sostituisce K-T: l'errore del guardiano `n.231`)*: **REGGE se `w(3000)/w(1500)` in `[0.7, 1.3]` e un pezzo solo a `k 3000`** *(`w` e i pezzi con `torneo_tenuta.misura`)*. **I DEVE:** F0 *(S1)*, FH, FT, L+0.5, L+0.25 REGGE; **L0 NON REGGE** *(il controllo negativo)*. Stampa anche le corse di (c) e di (a), senza DEVE *(il loro verdetto e' la misura)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import torneo_tenuta as TT  # noqa: E402
import torneo_tenuta_v2 as TT2  # noqa: E402

ATTESE = {"S1_cima": True, "FH_cima": True, "FT_cima": True, "L+0.5_cima": True, "L+0.25_cima": True, "L0_cima": False}
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def main():
    import _presidio
    for m in ("torneo_tenuta.py", "torneo_tenuta_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2351] K-T v2 (la carta sez. 13): w(3000)/w(1500) in [0.7, 1.3] e un pezzo a k 3000; L0 il controllo negativo")
    print("=" * 130)
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()
    for base in (TT.DIR, TT2.DIR):
        for nome in sorted(os.listdir(base)):
            d = os.path.join(base, nome)
            f15, f30 = os.path.join(d, "stato_001500.npz"), os.path.join(d, "stato_003000.npz")
            if not (os.path.exists(f15) and os.path.exists(f30)):
                print("  %-26s (non ha k 1500 e k 3000: saltata)" % nome)
                continue
            w15, p15, m15, _a = TT.misura(f15, nodo, n, L)
            w30, p30, m30, _b = TT.misura(f30, nodo, n, L)
            r = w30 / w15
            regge = 0.7 <= r <= 1.3 and p30 == 1
            print("  %-26s w %.3f -> %.3f (il rapporto %.3f); i pezzi %d -> %d; il picco %.4e -> %.4e: %s" % (
                os.path.basename(base) + "/" + nome, w15, w30, r, p15, p30, m15, m30, "REGGE" if regge else "NON REGGE"))
            if base == TT.DIR and nome in ATTESE:
                esito("%s: %s" % (nome, "REGGE" if ATTESE[nome] else "NON REGGE (il controllo negativo)"), regge == ATTESE[nome], "(%.3f, %d pezzi)" % (r, p30))
    print("=" * 130)
    print("  %d DEVE su %d   %s" % (sum(ESITI), len(ESITI), "TUTTI PASSATI" if all(ESITI) else "### CI SONO BUCHI"))
    print("=" * 130)
    return 0 if all(ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
