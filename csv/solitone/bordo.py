# -*- coding: utf-8 -*-
r"""**IL BORDO ASSORBENTE** *(Luca, `2026-11-03` `21:52`; il task history `doc/TASK_HISTORY/2026-11-03_TB3_bordo_assorbente.md`)*: ### **un'operazione FUORI dal nucleo, dopo ogni tick.**
### **La fascia:** i nodi a distanza periodica `R >= R_A` dal centro iniziale del solitone *(`campo.anelli`: esatta in indici)*. ### **Il profilo** `g(R) = g_max sin^2(pi/2 (R - R_A) / (R_B - R_A))`
per `R_A <= R < R_B`, `g_max` oltre *(`R_B` la meta' del periodo, `40.5`; i nodi negli angoli del rombo, fino a `L / sqrt 3`, hanno `g_max`: dichiarato)*. ### **L'assorbimento:** `psi -> psi (1 - g)`,
`phi -> phi0 + (phi - phi0)(1 - g)` *(`g` del nodo dell'estremita')*: si assorbono le onde del vuoto attorno a `phi0`, non il vuoto. ### **I conti:** `M` e `V` tolti dalla fascia a ogni chiamata
*(prima meno dopo)*, per il bilancio `M dentro + M assorbita = M0`.
"""
import math

import numpy as np

from . import campo as CP

R_A = 28.0                     # ### Luca 21:52: la fascia da 28 nodi dal centro iniziale


def profilo(r, R_A_, R_B, g_max):
    """### **`g` per nodo** dalla distanza `r`: `0` dentro `R_A_`, la rampa `sin^2` fino a `R_B`, `g_max` oltre."""
    r = np.asarray(r, dtype=float)
    x = np.clip((r - R_A_) / (R_B - R_A_), 0.0, 1.0)
    return g_max * np.sin(0.5 * math.pi * x) ** 2


def g_estremita(z, c1, c2, R_A_, g_max):
    """### **`(g` per estremita', `g` per nodo, `r` per nodo`)`** attorno al centro `(c1, c2)` *(gli indici)*; `R_B` la meta' del periodo."""
    from . import toro as TO
    L = z["L"]
    v = np.arange(z["inc"].n)
    _k, r = CP.anelli(v // L, v % L, c1, c2, L, float("inf"))
    gn = profilo(r, R_A_, TO.meta_periodo(L), g_max)
    return gn[z["inc"].nodo], gn, r


def assorbi(st, g_e, phi0):
    """### **L'assorbimento sullo stato `st`** *(in posto)*: `(dM, dV)`, la materia e il vuoto TOLTI *(prima meno dopo; `dV` puo' essere negativo se `|phi0| > |phi|`)*."""
    psi, phi = st["psi_h"], st["phi_h"]
    M0 = float(np.sum(np.abs(psi) ** 2))
    V0 = float(np.sum(np.abs(phi) ** 2))
    f = 1.0 - g_e
    psi *= f[:, None]
    phi[...] = phi0 + (phi - phi0) * f
    return M0 - float(np.sum(np.abs(psi) ** 2)), V0 - float(np.sum(np.abs(phi) ** 2))
