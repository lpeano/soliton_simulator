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


# ====================================================================== IL VUOTO DI RIFERIMENTO CHE GIRA (Luca 2026-11-04 09:00, la scelta (a); il task history TB3, sez. 4-5)
# ### B0 (633dcc10): F3 da solo sotto il tick vivo resta c(t) F3 entro 1.4e-14, e c gira (3 pi / 20 per tick dopo la rampa): phi0(t) = c(t) F3, con c MISURATO.
def tabella_fase(z, F3, K, dopo):
    """### **La tabella di `c(t)`:** il vuoto `F3` da solo *(`psi = 0`)* col tick vivo `AC.tick(z, t, K)` per `t = 1 .. K + dopo`; `c(t) = <F3, phi(t)> / |F3|^2`
    *(`c(0)` sullo stato di partenza)*; **`omega`** la media di `arg(c(t+1) / c(t))` sui `dopo` tick da `K` *(`t = K .. K + dopo - 1`)*. ### **Lo stato di `z` si rimette.**
    ### Dentro `SF.forma(VC.FORMA), BE.conv(DC.ZERO)`, come le corse."""
    from solitone import accensione as AC
    chiavi = [k for k, v in z["st"].items() if isinstance(v, np.ndarray)]
    salvato = {k: z["st"][k].copy() for k in chiavi}
    try:
        z["st"]["psi_h"][...] = 0.0
        z["st"]["phi_h"][...] = F3
        n3 = float(np.vdot(F3, F3).real)
        c = np.empty(K + dopo + 1, dtype=complex)
        c[0] = complex(np.vdot(F3, z["st"]["phi_h"]) / n3)
        for t in range(1, K + dopo + 1):
            AC.tick(z, t, K)
            c[t] = complex(np.vdot(F3, z["st"]["phi_h"]) / n3)
    finally:
        for k in chiavi:
            z["st"][k][...] = salvato[k]
    omega = float(np.mean(np.angle(c[K + 1:] / c[K:-1])))
    return c, omega


def c_di(t, tab, K, omega):
    """### **`c(t)`:** dalla tabella fino a `K` *(la rampa e il primo tick intero)*, poi `c(K) e^{i omega (t - K)}`."""
    return complex(tab[t]) if t <= K else complex(tab[K] * np.exp(1j * omega * (t - K)))


def fase_fascia(phi, rif, nodo, fascia):
    """### **Il controllo di Luca** *(09:00; il task history 5.3)*: sui nodi della fascia *(`fascia` maschera per nodo)*, PRIMA dell'assorbimento, `phi = a rif + r`:
    `d` per nodo `|phi - rif| / |rif|` *(medio e massimo)*, `a = <rif, phi> / |rif|^2`, `|a - 1|`, `arg a`, `|r| / |rif|`, tutti sulla fascia."""
    e = fascia[nodo]
    p, q = phi[e], rif[e]
    dn = np.zeros(len(fascia))
    nn = np.zeros(len(fascia))
    np.add.at(dn, nodo[e], np.abs(p - q) ** 2)
    np.add.at(nn, nodo[e], np.abs(q) ** 2)
    m = fascia & (nn > 0)
    dv = np.sqrt(dn[m] / nn[m])
    nq = float(np.vdot(q, q).real)
    a = complex(np.vdot(q, p) / nq)
    return {"d_medio": float(dv.mean()), "d_max": float(dv.max()), "a_meno_1": abs(a - 1.0), "arg_a": float(np.angle(a)),
            "r": float(np.linalg.norm(p - a * q) / np.sqrt(nq)), "d": float(np.linalg.norm(p - q) / np.sqrt(nq))}
