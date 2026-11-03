# -*- coding: utf-8 -*-
r"""**I TEST DEI PROFILI AD ANELLI** *(`campo.py`; il task history `2026-11-03_campo_TM1000`)*: ### **il reticolo della scena, e funzioni scritte a mano.**"""
import math

import numpy as np

from . import campo as CP
from . import test_toro as TT
from . import toro as TO

ELLE = 3.0                     # ### C3: la lunghezza dell'esponenziale exp(-r / ELLE)
SOGLIE = (1e-3, 1e-4, 1e-5)    # ### C3: le soglie del mandato
TOLL_ARR = 1e-12               # ### C2: l'arrotondamento (relativo)


def gira(esito):
    import _vuoto_vivo_B as V
    print("### I PROFILI AD ANELLI (csv/solitone/campo.py): ELLE %g SOGLIE %s TOLL_ARR %g; la gaussiana di test_toro (SIGMA %g)" % (ELLE, SOGLIE, TOLL_ARR, TT.SIGMA))
    sol, vuoto, s = V.CORSE["BG-F-0.15"]
    with V.scena(s, vuoto, V.EPS) as (_rec, z, _phi0, _pK):
        L, m1, m2 = z["L"], np.asarray(z["m1"]), np.asarray(z["m2"])
    R = TO.meta_periodo(L)
    n = CP.quanti(R)
    rho = TT._gauss(m1, m2, L)
    c1, c2, _x, _y = TO.centro(rho, m1, m2, L)
    k, r = CP.anelli(m1, m2, c1, c2, L, R)
    m = k >= 0
    ok = bool(np.all((k[m] <= r[m]) & (r[m] < k[m] + 1) & (r[m] < R))) and bool(np.all(r[~m] >= R)) and int(k.max()) == n - 1
    esito("DEVE PASSARE: C1 ogni nodo dell'anello k ha k <= r < k + 1 e r < R (R %.2f, %d anelli); oltre R l'anello -1" % (R, n), ok,
          "%d nodi negli anelli, %d oltre" % (int(m.sum()), int((~m).sum())))
    p0 = CP.profilo(rho, k, n)
    peggio = 0.0
    for k1, k2 in ((TT.MEZZO, 0), (0, TT.MEZZO), (TT.MEZZO, TT.MEZZO)):
        rs = TT._sposta(rho, m1, m2, L, k1, k2)
        a1, a2, _x, _y = TO.centro(rs, m1, m2, L)
        ks, _r = CP.anelli(m1, m2, a1, a2, L, R)
        peggio = max(peggio, float(np.nanmax(np.abs(CP.profilo(rs, ks, n) / p0 - 1.0))))
    esito("DEVE PASSARE: C2 la gaussiana spostata di mezzo lato (tre versi), col centro ricalcolato: lo stesso profilo entro %g" % TOLL_ARR, peggio <= TOLL_ARR, "il peggiore relativo %.2e" % peggio)
    rs = TT._sposta(rho, m1, m2, L, TT.MEZZO, 0)
    a1, a2, _x, _y = TO.centro(rs, m1, m2, L)
    pos = TO.posizioni(m1, m2, L)
    A1, A2 = TO.vettori()
    pc = ((a1 - L // 2) * A1 + (a2 - L // 2) * A2)
    re = np.hypot(*(pos - pc).T)
    ke = np.floor(re).astype(np.int64)
    ke[re >= R] = -1
    de = float(np.nanmax(np.abs(CP.profilo(rs, ke, n) / p0 - 1.0)))
    esito("DEVE FALLIRE: C2-F la distanza EUCLIDEA (senza l'immagine piu' vicina) sulla gaussiana spostata di (%d, 0): lo stesso profilo entro %g" % (TT.MEZZO, TOLL_ARR),
          not de <= TOLL_ARR, "il peggiore relativo %.2e" % de)
    f = np.exp(-r / ELLE)
    pf = CP.profilo(f, k, n)
    righe, ok = [], True
    for sg in SOGLIE:
        rc, ru = CP.portata(pf, sg * pf[0])
        att = ELLE * math.log(1.0 / sg)
        ok = ok and abs(rc - att) <= 1.0 and abs(ru - att) <= 1.0
        righe.append("%g: contiguo %g ultimo %g, ELLE ln(1/f) %.3f" % (sg, rc, ru, att))
    esito("DEVE PASSARE: C3 la portata di exp(-r / %g) entro 1 anello da ELLE ln(1/f), per le tre soglie" % ELLE, ok, "; ".join(righe))
