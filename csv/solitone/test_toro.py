# -*- coding: utf-8 -*-
r"""**I TEST DELLE MISURE SUL TORO** *(il task history `2026-11-02_accensione_lenta`, sez. `11`)*: ### **il reticolo della scena, e una `rho` gaussiana scritta a mano.**"""
import math

import numpy as np

from . import toro as TO

SIGMA = 6.6                    # ### la gaussiana dei test: la larghezza della partenza di BG-F-0.15 (6.61), arrotondata
FONDO = 1e-4                   # ### il fondo uniforme della gaussiana (un alone)
MEZZO = 40                     # ### il mezzo lato in indici (L 81 e' dispari)
TOLL_ARR = 1e-12               # ### T1, T2: l'arrotondamento delle somme (relativo)
TOLL_C = 1e-9                  # ### T1, T2: i centri


def _gauss(m1, m2, L):
    p = TO.posizioni(m1, m2, L)
    return np.exp(-0.5 * np.sum(p ** 2, axis=1) / SIGMA ** 2) + FONDO


def _sposta(rho, m1, m2, L, k1, k2):
    """### **La `rho` spostata di `(k1, k2)` indici:** una permutazione esatta dei nodi."""
    out = np.empty_like(rho)
    out[((m1 + k1) % L) * L + (m2 + k2) % L] = rho
    return out


def _euclidee(rho, pos, w_in, w0, h):
    M = float(rho.sum())
    c = (rho @ pos) / M
    d = np.hypot(pos[:, 0] - c[0], pos[:, 1] - c[1])
    w = math.sqrt(float(rho @ np.sum((pos - c) ** 2, axis=1)) / M)
    g = np.clip((w_in + 0.5 * h - d) / h, 0.0, 1.0)
    return {"x": float(c[0]), "y": float(c[1]), "w": w, "f_win": float(rho[d <= w_in].sum()) / M, "f_liscia": float(rho @ g) / M, "alone": 1.0 - float(rho[d <= 3.0 * w0].sum()) / M}


def gira(esito):
    import _vuoto_vivo_B as V
    print("### LE MISURE SUL TORO (csv/solitone/toro.py): SIGMA %g FONDO %g MEZZO %d TOLL_ARR %g TOLL_C %g SETTORI %d" % (SIGMA, FONDO, MEZZO, TOLL_ARR, TOLL_C, TO.SETTORI))
    sol, vuoto, s = V.CORSE["BG-F-0.15"]
    with V.scena(s, vuoto, V.EPS) as (rec, z, _phi0, _pK):
        L, m1, m2, pos = z["L"], np.asarray(z["m1"]), np.asarray(z["m2"]), z["pos"].copy()
        w0 = rec["larghezza"]
    esito("DEVE PASSARE: T0 le posizioni della scena sono (m1 - L//2) A1 + (m2 - L//2) A2, AL BIT (L %d)" % L, np.array_equal(pos, TO.posizioni(m1, m2, L)), "")
    r = TO.meta_periodo(L)
    esito("DEVE PASSARE: T3 la meta' del periodo piu' corto del toro e' L/2 (i periodi L A1, L A2, L (A1 + A2) sono lunghi L)", abs(r - 0.5 * L) <= TOLL_C, "%.12f" % r)
    w_in, h = SIGMA, 1.0
    rho = _gauss(m1, m2, L)
    a, Da, Ma = TO.misure(rho, m1, m2, L, w_in, w0, h)
    e = _euclidee(rho, pos, w_in, w0, h)
    chiavi = ("w", "f_win", "f_liscia", "alone")
    peggio = 0.0
    for k1, k2 in ((MEZZO, 0), (0, MEZZO), (MEZZO, MEZZO)):
        b, _D, _M = TO.misure(_sposta(rho, m1, m2, L, k1, k2), m1, m2, L, w_in, w0, h)
        dc = max(abs(((b["c1"] - a["c1"] - k1 + 0.5 * L) % L) - 0.5 * L), abs(((b["c2"] - a["c2"] - k2 + 0.5 * L) % L) - 0.5 * L))
        dm = max(abs(b[k] / a[k] - 1.0) for k in chiavi)
        peggio = max(peggio, dm)
        esito("DEVE PASSARE: T1 la gaussiana spostata di (%d, %d) indici: le misure periodiche uguali entro %g, il centro spostato di (%d, %d) entro %g" % (k1, k2, TOLL_ARR, k1, k2, TOLL_C),
              dm <= TOLL_ARR and dc <= TOLL_C, "il peggiore relativo %.2e, il centro %.2e" % (dm, dc))
    es = _euclidee(_sposta(rho, m1, m2, L, MEZZO, 0), pos, w_in, w0, h)
    de = max(abs(es[k] / e[k] - 1.0) for k in chiavi)
    esito("DEVE FALLIRE: T1-F le misure EUCLIDEE della gaussiana spostata di (%d, 0) uguali entro %g" % (MEZZO, TOLL_ARR), not de <= TOLL_ARR,
          "il peggiore relativo %.2e (w %.4f contro %.4f, il cuore %.5f contro %.5f)" % (de, es["w"], e["w"], es["f_liscia"], e["f_liscia"]))
    dc = math.hypot(a["x"] - e["x"], a["y"] - e["y"])
    dm = max(abs(a[k] / e[k] - 1.0) for k in ("f_win", "f_liscia", "alone"))
    esito("DEVE PASSARE: T2 la gaussiana al centro: il centro periodico e l'euclideo entro %g, cuore, f_win, alone entro %g (w no: le distanze lontane cambiano)" % (TOLL_C, TOLL_ARR),
          dc <= TOLL_C and dm <= TOLL_ARR, "il centro %.2e, il peggiore relativo %.2e; w periodico %.6f, euclideo %.6f" % (dc, dm, a["w"], e["w"]))
    q = TO.alone_settori(rho, Da, Ma, w0)
    esito("DEVE PASSARE: T4 l'alone per settore somma all'alone (entro %g)" % TOLL_ARR, abs(math.fsum(q) - a["alone"]) <= TOLL_ARR * max(a["alone"], 1e-300) + 1e-15,
          "la somma %.15e, l'alone %.15e" % (math.fsum(q), a["alone"]))
