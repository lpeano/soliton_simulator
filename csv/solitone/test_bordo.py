# -*- coding: utf-8 -*-
r"""**I TEST DEL BORDO ASSORBENTE** *(`bordo.py`; il task history `2026-11-03_TB3_bordo_assorbente`)*: ### **il reticolo della scena, stati di prova scritti a mano.**
### `G0` il profilo: `0` dentro `R_A`, `g_max` da `R_B`, crescente, continuo con la derivata nulla a `R_A`; `G1` il bilancio: `M` dopo + `dM` = `M` prima *(e `V`)*; `G1-F` *(deve fallire)* senza
`dM`; `G2` se `phi = phi0` e `psi = 0` nella fascia lo stato resta AL BIT *(si assorbono le onde, non il vuoto)*; `G3` dentro `R_A` lo stato resta AL BIT; `G4` `fase_fascia` *(Luca 09:00)* su `rif` e su `e^{i DELTA} rif`; `G5` `c_di` *(la tabella, poi la fase costante)*.
"""
import numpy as np

from . import bordo as BO
from . import toro as TO

G_PROVA = 0.1                  # ### un g_max di prova (non quello della corsa: quello lo sceglie carta_bordo)
TOLL = 1e-12
DELTA = 0.01                   # ### G4: uno sfasamento di prova


def gira(esito):
    import _vuoto_vivo_B as V
    print("### IL BORDO ASSORBENTE (csv/solitone/bordo.py): R_A %g G_PROVA %g TOLL %g" % (BO.R_A, G_PROVA, TOLL))
    sol, vuoto, s = V.CORSE["BG-F-0.15"]
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, _pK):
        L, inc = z["L"], z["inc"]
        st0 = {k: z["st"][k].copy() for k in ("psi_h", "phi_h")}
    R_B = TO.meta_periodo(L)
    r = np.linspace(0.0, 47.0, 4701)
    g = BO.profilo(r, BO.R_A, R_B, G_PROVA)
    ok = (bool(np.all(g[r < BO.R_A] == 0.0)) and bool(np.all(g[r >= R_B] == G_PROVA)) and bool(np.all(np.diff(g) >= 0.0))
          and float(BO.profilo(BO.R_A + 1e-6, BO.R_A, R_B, G_PROVA)) < 1e-12)
    esito("DEVE PASSARE: G0 il profilo: 0 dentro R_A %g, g_max da R_B %.2f, crescente, la derivata nulla a R_A" % (BO.R_A, R_B), ok,
          "g(R_A + 1e-6) %.2e" % float(BO.profilo(BO.R_A + 1e-6, BO.R_A, R_B, G_PROVA)))
    g_e, gn, rn = BO.g_estremita(z, L // 2, L // 2, BO.R_A, G_PROVA)
    rng = np.random.default_rng(20261103)
    st = {"psi_h": rng.standard_normal(st0["psi_h"].shape) + 1j * rng.standard_normal(st0["psi_h"].shape),
          "phi_h": st0["phi_h"] + 0.1 * (rng.standard_normal(st0["phi_h"].shape) + 1j * rng.standard_normal(st0["phi_h"].shape))}
    M0, V0 = float(np.sum(np.abs(st["psi_h"]) ** 2)), float(np.sum(np.abs(st["phi_h"]) ** 2))
    dentro = {k: v[gn[inc.nodo] == 0.0].copy() for k, v in st.items()}
    dM, dV = BO.assorbi(st, g_e, st0["phi_h"])
    M1, V1 = float(np.sum(np.abs(st["psi_h"]) ** 2)), float(np.sum(np.abs(st["phi_h"]) ** 2))
    eM, eV = abs((M1 + dM) / M0 - 1.0), abs((V1 + dV) / V0 - 1.0)
    esito("DEVE PASSARE: G1 il bilancio: M dopo + dM = M prima, V dopo + dV = V prima, entro %g relativo" % TOLL, eM <= TOLL and eV <= TOLL,
          "M %.2e, V %.2e; dM / M0 %.3e" % (eM, eV, dM / M0))
    esito("DEVE FALLIRE: G1-F senza dM, M dopo = M prima entro %g" % TOLL, not abs(M1 / M0 - 1.0) <= TOLL, "%.3e" % abs(M1 / M0 - 1.0))
    esito("DEVE PASSARE: G3 dentro R_A (g = 0) lo stato resta AL BIT", all(np.array_equal(st[k][gn[inc.nodo] == 0.0], dentro[k]) for k in st),
          "%d estremita' dentro, %d nella fascia" % (int(np.sum(gn[inc.nodo] == 0.0)), int(np.sum(gn[inc.nodo] > 0.0))))
    st2 = {"psi_h": np.zeros_like(st0["psi_h"]), "phi_h": st0["phi_h"].copy()}
    dM2, dV2 = BO.assorbi(st2, g_e, st0["phi_h"])
    esito("DEVE PASSARE: G2 con psi = 0 e phi = phi0 lo stato resta AL BIT (si assorbono le onde, non il vuoto)",
          np.array_equal(st2["phi_h"], st0["phi_h"]) and not np.any(st2["psi_h"]) and dM2 == 0.0 and dV2 == 0.0, "dM %g dV %g" % (dM2, dV2))
    fascia = gn > 0.0
    rif = st0["phi_h"]
    f0 = BO.fase_fascia(rif.copy(), rif, inc.nodo, fascia)
    f1 = BO.fase_fascia(np.exp(1j * DELTA) * rif, rif, inc.nodo, fascia)
    esito("DEVE PASSARE: G4 fase_fascia: phi = rif da' d 0 e a 1; phi = e^{i %g} rif da' arg a = %g, |a - 1| = |e^{i %g} - 1|, r 0 (entro %g)" % (DELTA, DELTA, DELTA, TOLL),
          f0["d_max"] == 0.0 and f0["a_meno_1"] <= TOLL and abs(f1["arg_a"] - DELTA) <= TOLL and abs(f1["a_meno_1"] - abs(np.exp(1j * DELTA) - 1.0)) <= TOLL and f1["r"] <= TOLL
          and abs(f1["d_medio"] - abs(np.exp(1j * DELTA) - 1.0)) <= TOLL, "arg a %.15f, d medio %.3e, r %.1e" % (f1["arg_a"], f1["d_medio"], f1["r"]))
    tab = np.exp(1j * 0.3 * np.arange(11))
    esito("DEVE PASSARE: G5 c_di: la tabella fino a K, poi c(K) e^{i omega (t - K)} (continua a K)", BO.c_di(10, tab, 10, 0.3) == tab[10] and abs(BO.c_di(13, tab, 10, 0.3) - np.exp(1j * 3.9)) <= TOLL,
          "c_di(13) %.15f %+.15fi" % (BO.c_di(13, tab, 10, 0.3).real, BO.c_di(13, tab, 10, 0.3).imag))
