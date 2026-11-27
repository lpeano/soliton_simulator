# -*- coding: utf-8 -*-
r"""**[M0137-0] A COSTO ZERO: IL TRANSITORIO DI chi E' DEL GRADINO O DELL'INCONTRO?** *(DECISIONE DI LUCA, 2026-11-25 01:37, dalla posta; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-sedecies`; solo letture)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_d3.py > doc/referti_l2/chi_d3.txt

Dalle serie di `M2330/d3` *(un oggetto, chi on)* e `d1` *(due, chi on)*: **`max|chi|`** *(l'ultima colonna della serie, ogni `10` tick)*, il massimo per finestra di `250`; e **`w(k)`** di `torneo_tenuta.misura` sugli stati ogni `250` *(per d1 e' il `w` del campo intero: due oggetti; si stampa per completezza)*.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import fondo_puntofisso as PF  # noqa: E402

BASE = os.path.join(PF.CTRL, "M2330")


def main():
    import _presidio
    F1.avvia()
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0137-0] max|chi|(k) e w(k) di d3 (un oggetto, chi on) e d1 (due, chi on), [M2330]")
    print("=" * 130)
    with F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        Z["metti"]()
    for c in ("d3", "d1"):
        f = os.path.join(BASE, c, "serie.json")
        PF.controlla(f)
        s = np.array(json.load(open(f, encoding="utf-8"))["serie"])
        k, mc = s[:, 0], s[:, -1]
        print("  %s: max|chi| per finestra di 250 (k fino a): %s" % (c, " ".join("%d:%.1f" % (k1, float(mc[(k > k1 - 250) & (k <= k1)].max())) for k1 in range(250, 6001, 250))))
        ws = []
        for kk in range(0, 6001, 250):
            fz = os.path.join(BASE, c, "stato_%06d.npz" % kk)
            PF.controlla(fz)
            ws.append(F1.TT.misura(fz, nodo, n, L)[0])
        print("  %s: w (torneo_tenuta.misura) ogni 250: %s" % (c, " ".join("%.2f" % w for w in ws)))
        print("  %s: max|chi| a k 0 %.3f, il massimo su tutta la corsa %.3f a k %d; w da %.3f a %.3f, (max - min)/medio %.4f" % (
            c, float(mc[0]), float(mc.max()), int(k[int(np.argmax(mc))]), min(ws), max(ws), (max(ws) - min(ws)) / float(np.mean(ws))))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
