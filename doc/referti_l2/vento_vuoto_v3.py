# -*- coding: utf-8 -*-
r"""**[M2245-A] IL VENTO DEL VUOTO, LA V3: d/dy COI NODI GIUSTI** *(errore mio, dichiarato in `3e138a1b`: `toro.vettori()` ha `A2 = (-1/2, sqrt3/2)`, quindi i nodi `(m1 -+ 1, m2 +- 2)` della v1 stavano a `(-+2, +-sqrt3)`, non lungo `y`; quelli giusti sono `(m1 + 1, m2 + 2)` e `(m1 - 1, m2 - 2)`; `vento_vuoto.py` e `_v2` sono usati e non si riscrivono)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/vento_vuoto_v3.py > doc/referti_l2/vento_vuoto_v3.txt

**Due differenze, in memoria:** `geometria` restituisce i nodi `su`/`giu` giusti; **prima di `main`, un caso noto in piu' che la v1 avrebbe fallito:** una fase `q x` deve dare `d theta/dy = 0` *(entro `1e-12`)*, e la vecchia scelta di nodi NON *(DEVE FALLIRE)*. **Il resto:** `vento_vuoto.main` della v2 *(il prodotto in reali)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import vento_vuoto_v2 as VV2  # noqa: E402

VV = VV2.VV
_geometria = VV.geometria


def geometria():
    nodo, n, L, m1, m2, dxy, _su, _giu, info = _geometria()
    su = ((m1 + 1) % L) * L + (m2 + 2) % L
    giu = ((m1 - 1) % L) * L + (m2 - 2) % L
    return nodo, n, L, m1, m2, dxy, su, giu, info


def caso_x():
    """### una fase `q x`: coi nodi giusti `d theta/dy = 0`; coi vecchi no. `True` se passa."""
    nodo, n, L, m1, m2, _dxy, su, giu, _info = geometria()
    vsu = ((m1 - 1) % L) * L + (m2 + 2) % L
    vgiu = ((m1 + 1) % L) * L + (m2 - 2) % L
    _p0, f0 = VV.leggi_stato(os.path.join(VV.V3.BASE, VV.TIPI["v0"], "stato_000000.npz"))
    x = (m1 - 0.5 * m2).astype(float)
    q = 2.0 * math.pi * 2.0 / L
    _r, Zq = VV2.per_nodo(f0 * np.exp(1j * q * x[nodo]), f0, nodo, n)
    inter = ((m2 >= 2) & (m2 < L - 2)) & ((m1 - 0.5 * m2 >= -L / 2 + 3) & (m1 - 0.5 * m2 < L - 3))
    giusta = float(np.max(np.abs(VV.dtheta_dy(Zq, su, giu)[inter])))
    vecchia = float(np.max(np.abs(VV.dtheta_dy(Zq, vsu, vgiu)[inter])))
    a = giusta < 1e-12
    b = vecchia > 1e-6
    print("  DEVE: (A1-x) una fase q x (2 giri su L): d theta/dy coi nodi giusti = 0 entro 1e-12           %s %.1e" % ("PASSA" if a else "### FALLISCE", giusta))
    print("  DEVE: (A1-x) DEVE FALLIRE lo zero coi nodi della v1 (m1 -+ 1, m2 +- 2)                           %s %.1e" % ("PASSA" if b else "### FALLISCE", vecchia))
    return a and b


VV.geometria = geometria

if __name__ == "__main__":
    import _presidio
    VV.V3.avvia()
    _presidio.avvia(os.path.join(_QUI, "vento_vuoto.py"))
    _presidio.avvia(os.path.join(_QUI, "vento_vuoto_v2.py"))
    _presidio.avvia(__file__)
    ok = caso_x()
    r = VV.main()
    sys.exit(0 if (ok and r == 0) else 1)
