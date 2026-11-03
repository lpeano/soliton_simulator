# -*- coding: utf-8 -*-
r"""**I TEST DEL VUOTO SULLA CARTA** *(il task history `2026-11-02_solitone_vestito`, `V1`-`V4`)*: ### **sulla scena di BG-F-0.15** *(il fondo `F0`, `s 0.15`)*."""
import math

import numpy as np

from . import protetto as P
from . import vuoto as VU

SEME = 20261102                # ### i vettori casuali di V1 e V2
TOLL_LIN = 1e-10               # ### V1
TOLL_RIC = 1e-12               # ### V2
TOLL_UNI = 1e-12               # ### V3
TOLL_BORDO = 1e-9              # ### V4: F0 dentro o sul bordo di una banda
TOLL_FRECCIA = 1e-12           # ### V5: la freccia per nodo (somme di sei termini di modulo 1)


def gira(esito):
    import _coppia_di_B as CB
    import _livelli_piatti as LP
    import _vuoto_sul_fondo as VSF
    import _vuoto_vivo_B as V
    import scena_l2 as SL
    print("### IL VUOTO SULLA CARTA (csv/solitone/vuoto.py): la scena di BG-F-0.15, il tick intero con psi = 0; SEME %d TOLL_LIN %g TOLL_RIC %g TOLL_UNI %g TOLL_BORDO %g"
          % (SEME, TOLL_LIN, TOLL_RIC, TOLL_UNI, TOLL_BORDO))
    _sol, vuoto, s = V.CORSE["BG-F-0.15"]
    rng = np.random.default_rng(SEME)
    with P.scena_vuoto(CB.N, CB.L, V.EPS, s, LP.FORMA, vuoto) as (_rec, z, phi0, _pK):
        L, inc = z["L"], z["inc"]
        F0 = VSF.fondo_uniforme(inc, L, SL.VUOTO_PER_ESTREMITA)[0]
        esito("DEVE PASSARE: V0 il vuoto della scena e' F0 (_vuoto_sul_fondo.fondo_uniforme) AL BIT", F0.tobytes() == phi0.tobytes(), "")
        idx, dirs = VU.celle(inc, L)
        e = rng.standard_normal(F0.shape) + 1j * rng.standard_normal(F0.shape)
        e *= np.linalg.norm(F0) / np.linalg.norm(e)
        Te = VU.tick_vuoto(z, e)
        lin = float(np.linalg.norm(VU.tick_vuoto(z, F0 + e) - VU.tick_vuoto(z, F0) - Te) / np.linalg.norm(Te))
        esito("DEVE PASSARE: V1 con psi = 0 il tick sul vuoto e' lineare: |T(F0 + e) - T(F0) - T(e)|/|T(e)| <= %g" % TOLL_LIN, lin <= TOLL_LIN, "%.2e" % lin)
        A = VU.matrice(z, idx)
        g = rng.standard_normal(F0.shape) + 1j * rng.standard_normal(F0.shape)
        Tg = VU.tick_vuoto(z, g)
        er = float(np.linalg.norm(VU.applica(A, g, idx, L) - Tg) / np.linalg.norm(Tg))
        esito("DEVE PASSARE: V2 A_v ricostruisce il tick: |T(g) - ifft(A_v fft(g))|/|T(g)| <= %g" % TOLL_RIC, er <= TOLL_RIC, "%.2e" % er)
        nu, resF0, dl = VU.frequenza(z, F0, s)
        import _solitone_dal_fondo as SD
        aF0 = VU.freccia(F0, idx, dirs)
        att = np.array([2.0, 2.0 * math.sqrt(3.0)])
        e5 = float(np.max(np.abs(aF0 - att)))
        esito("DEVE PASSARE: V5 la freccia di F0 e' (2, 2 sqrt3) su ogni nodo (modulo 4, a 60 gradi) entro %g" % TOLL_FRECCIA, e5 <= TOLL_FRECCIA, "max scarto %.2e" % e5)
        aF3 = VU.freccia(SD.fondo_con_fasi(inc, L, dict(SD.FASI)["F3"]), idx, dirs)
        esito("DEVE PASSARE: V5-N la freccia di F3 (fasi 0, 0, pi) e' nulla su ogni nodo entro %g" % TOLL_FRECCIA, float(np.max(np.abs(aF3))) <= TOLL_FRECCIA,
              "max %.2e" % float(np.max(np.abs(aF3))))
        fi = VU.freccia_media(VU.freccia(SD.fondo_con_fasi(inc, L, (0.0, 0.0, 0.5 * math.pi)), idx, dirs))
        esito("DEVE PASSARE: V5-I la freccia dell'ibrido (0, 0, pi/2) ha il modulo 4 cos(pi/4) = 2 sqrt2 su ogni nodo entro %g" % TOLL_FRECCIA,
              abs(fi["modulo"] - 2.0 * math.sqrt(2.0)) <= TOLL_FRECCIA and fi["scarto"] <= TOLL_FRECCIA, "modulo %.15f, scarto %.2e" % (fi["modulo"], fi["scarto"]))
        aI = VU.freccia(SD.fondo_con_fasi(inc, L, (0.0, 0.0, 0.5 * math.pi)), idx, dirs)
        esito("DEVE FALLIRE: V5-F la freccia dell'ibrido e' quella di F0 entro %g" % TOLL_FRECCIA, not float(np.max(np.abs(aI - aF0))) <= TOLL_FRECCIA,
              "max %.3f" % float(np.max(np.abs(aI - aF0))))
    Ar = A.reshape(-1, 6, 6)
    uni = float(np.max(np.abs(np.einsum("kji,kjl->kil", Ar.conj(), Ar) - np.eye(6))))
    esito("DEVE PASSARE: V3 A_v(k) unitaria a ogni k entro %g; F0 autostato del tick, residuo e |lambda| - 1 <= %g" % (TOLL_UNI, TOLL_UNI),
          uni <= TOLL_UNI and resF0 <= TOLL_UNI and abs(dl) <= TOLL_UNI, "max|A^H A - I| %.2e; F0: residuo %.2e, |lambda| - 1 %.1e, nu %.12f" % (uni, resF0, dl, nu))
    taglio, inter, gap = VU.bande(A, s)
    d_nu, m_nu, j_nu = VU.margine(nu, taglio, inter, s)
    esito("DEVE PASSARE: V4 il rivelatore trova nu di F0 dentro o sul bordo di una banda (margine <= %g)" % TOLL_BORDO, d_nu or m_nu <= TOLL_BORDO,
          "%s, margine %+.3e, bande %s" % ("dentro" if d_nu else "fuori", m_nu, j_nu))
    d_g, m_g, _j = VU.margine(taglio, taglio, inter, s)
    esito("DEVE FALLIRE: V4-F il mezzo del gap piu' largo e' dentro una banda", not d_g, "margine %+.6f (il gap e' largo %.6f)" % (m_g, gap))
    return {"A": A, "s": s, "L": L, "dirs": dirs, "nu": nu, "taglio": taglio, "inter": inter, "gap": gap, "margine_nu": (d_nu, m_nu, j_nu)}
