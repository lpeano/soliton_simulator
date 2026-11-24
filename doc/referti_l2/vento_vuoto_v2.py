# -*- coding: utf-8 -*-
r"""**[M2245-A] IL VENTO DEL VUOTO, LA V2: `Z` COL PRODOTTO IN REALI** *(`vento_vuoto.py` fallì il caso noto «`J_phi` di `k 0` rispetto a se stesso = `0` al bit»: `-3.3e-21`, perche' `np.conj(a) * a` non da' la parte immaginaria esattamente nulla; quello script e' usato e non si riscrive; la carta sez. `3-undecies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/vento_vuoto_v2.py > doc/referti_l2/vento_vuoto.txt

**Una sola differenza, in memoria:** `per_nodo` calcola `conj(phi0) phi` come `(ar br + ai bi) + i (ar bi - ai br)`, che per `phi = phi0` da' `Im = 0` esatto. **Il resto:** `vento_vuoto.main` cosi' com'e'. Il file `M1330/b3v3/vento_vuoto.json` *(fuori dal repo)* viene riscritto con i numeri di questa versione.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import vento_vuoto as VV  # noqa: E402


def per_nodo(phi_h, phi0_h, nodo, n):
    """### `(rho_phi, Z)` per nodo, col prodotto `conj(phi0) phi` scritto in reali."""
    rho = np.bincount(nodo, weights=np.abs(phi_h) ** 2, minlength=n)
    ar, ai = phi0_h.real, phi0_h.imag
    br, bi = phi_h.real, phi_h.imag
    re = ar * br + ai * bi
    im = ar * bi - ai * br
    Zn = np.bincount(nodo, weights=re, minlength=n) + 1j * np.bincount(nodo, weights=im, minlength=n)
    return rho, Zn


VV.per_nodo = per_nodo

if __name__ == "__main__":
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "vento_vuoto.py"))
    _presidio.avvia(__file__)
    sys.exit(VV.main())
