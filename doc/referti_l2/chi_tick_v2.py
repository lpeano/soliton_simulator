# -*- coding: utf-8 -*-
r"""**IL TICK CON `chi` ALLA VELOCITA' DELLA LUCE -- LA V2** *(il mandato di Luca `2026-11-21` `23:30`; la carta `doc/TASK_HISTORY/2026-11-21_lorentz_locale.md`, sez. `4`)*. [[PROGETTO-MITOSI]]

**`chi_tick.py` e' IN USO e non si tocca.** Qui `tick_chi` ed `energia_chi` riga per riga con **UNA differenza: l'INERZIA `f`** *(`pi_dot = f F`, `F` la forza di oggi; l'energia cinetica `pi^2 / (2 f)`)*, **`f = (s / (c_chi sqrt(3/2)))^2`** *(i numeri del codice: `s`, `C_CHI`)*; **`kappa` il NUMERO di oggi** *(`chi_parametri_v2.KAPPA`, D3)*. **Il punto fisso statico non cambia** *(la forza `F = 0` non contiene `f`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import chi_tick as CT  # noqa: E402
import chi_parametri_v2 as CP2  # noqa: E402

CHIAVI_CHI = CT.CHIAVI_CHI


def inerzia(s, c2):
    """### `f = (s / (c sqrt(3/2)))^2`: `v_chi = sqrt(f) c sqrt(3/2) = s` *(la luce: `v = s_a = s`, L1)*."""
    return (float(s) / math.sqrt(float(c2) * 1.5)) ** 2


class Parametri2(CT.Parametri):
    def __init__(self, kappa, c0, s, e0, f, c2=CT.C_CHI ** 2, m2=(1.0 / CT.PORTATA) ** 2):
        CT.Parametri.__init__(self, kappa, c0, s, e0, c2, m2)
        self.f = float(f)

    def __repr__(self):
        return CT.Parametri.__repr__(self) + ", f %r" % self.f


def parametri_v2(Z, PS, CSB, rho_c, e, t0, s, e0, partenza="C2", stato=None):
    """### i parametri v2: `kappa` il NUMERO *(D3)*, `c0 = kappa m0`, `f` dall'inerzia. `(P2, m0)`."""
    P, m0 = CP2.parametri_v2(Z, PS, CSB, rho_c, e, t0, s, e0, partenza, stato)
    return Parametri2(P.kappa, P.c0, P.s, P.e0, inerzia(P.s, P.c2), P.c2, P.m2), m0


def tick_chi_v2(z, campo, P, Lp, X):
    """### `chi_tick.tick_chi` riga per riga, con `pi += (dt/2) f F`."""
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    mot, st, par = z["mot"], z["st"], z["par"]
    dt = float(mot.dtau[0])
    assert np.all(mot.dtau == mot.dtau[0]), "dtau non uniforme: il salto di rana di chi vuole un dtau solo"
    campo.spinta(0.5)
    X["pi"] += (0.5 * dt * P.f) * CT.forza(mot, st, par, P, Lp, X["chi"])
    X["chi"] += (0.5 * dt) * X["pi"]
    N = np.exp(-P.kappa * X["chi"])
    mot.cs = P.s * N
    mot.lambda_c = None
    CT.fase_a(mot, st, P.e0, N)
    with UO.avvolto(mot, campo, True):
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    CT.fase_a(mot, st, P.e0, N)
    d = np.asarray(mot.dtau, dtype=float) * np.asarray(mot.cs, dtype=float)
    nodo = np.asarray(mot.inc.nodo)
    X["theta_a"] += math.pi * (d[nodo[0::2]] - d[nodo[1::2]])
    X["chi"] += (0.5 * dt) * X["pi"]
    X["pi"] += (0.5 * dt * P.f) * CT.forza(mot, st, par, P, Lp, X["chi"])
    campo.spinta(0.5)


def energia_chi_v2(mot, st, par, P, Lp, X, campo):
    """### `chi_tick.energia_chi` riga per riga, con la cinetica `pi^2 / (2 f)`. `(H, H_chi)`."""
    import energia_pesata as EP
    chi, pi = X["chi"], X["pi"]
    N = np.exp(-P.kappa * chi)
    copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
    salvo, lc = mot.cs, getattr(mot, "lambda_c", None)
    mot.cs = P.s * N
    mot.lambda_c = None
    try:
        pn, pa = EP.termini_di_h(mot, copia, par)
        wn, wa = EP.pesi(mot)
        G = float(np.sum(wn * pn)) + float(np.sum(wa * pa))
    finally:
        mot.cs, mot.lambda_c = salvo, lc
    rho = CT.rho_di(mot, st)
    Fa = -P.e0 * float(np.sum((N - 1.0) * rho))
    dch = chi[Lp.ii] - chi[Lp.jj]
    Hc = 0.5 * float(np.sum(pi * pi)) / P.f + 0.5 * P.c2 * float(np.sum(dch * dch)) + 0.5 * P.m2 * float(np.sum(chi * chi)) + P.c0 * float(np.sum(chi))
    return G + Fa + campo.K() + campo.V() + Hc, Hc
