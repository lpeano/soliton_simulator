# -*- coding: utf-8 -*-
r"""**LA CAUSA DEL NaN IN `E_leg`** *(la nota di Luca delle `11:17` del `2026-10-28`; [[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]])*: ### **dove compare, su quali nodi, e se viene da `Lambda` a zero.**

### **Il percorso misurato e' quello di `_solitone_con_la_buca.prepara`:** ### **`SC.stato_uniforme` e poi `SC.parti`, alle due taglie.**
### **Nessuna corsa: lo stato di costruzione e basta.**

    python csv/_nan_e_leg.py > doc/referti_l2/nan_e_leg.txt
"""
import os
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402


def misura(taglia):
    """### **Lo stato di `prepara`, e i nodi dove `lam * F1(rho / lam)` non e' finito.**"""
    import _energia_del_legame as EL
    import _scomposizione_solitone as SC
    import _solitone_con_la_buca as B
    N, _L = B.TAGLIE[taglia]
    # ### le righe di B.prepara: prepara non restituisce lo stato uniforme, che e' quello da guardare
    import _modi_pi_e_solitoni as MPS
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    VC.S = B.S_CORSA
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        cc, _cy, _w0 = STR.c_triangoli(B.S_CORSA)
        ls = MPS.largo(VC.FORMA, cc, B.S_CORSA, N)
    finally:
        MPS.LAM0 = vero
    rec = {"larghezza": ls["larghezza"], "c": cc, "mu": ls["mu"], "fattore": (B.TAGLIE[taglia][1] - 0.1) / ls["larghezza"]}
    L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, rec["fattore"], rec)
    incu, motu, stu = SC.stato_uniforme(L, Q, m1, m2)
    rho = np.zeros(incu.n)
    np.add.at(rho, incu.nodo, np.sum(np.abs(stu["psi_h"]) ** 2, axis=1))
    lam = np.zeros(incu.n)
    np.add.at(lam, incu.nodo, np.abs(stu["phi_h"]) ** 2)
    with warnings.catch_warnings(record=True) as avvisi:
        warnings.simplefilter("always")
        with np.errstate(all="warn"):
            el = lam * SC.F1(rho / lam)
            E_mat, _E_v, E_leg, M, _V = SC.parti(incu, motu, stu)
    nonfin = ~np.isfinite(el)
    # ### lo stato delle corse a t = 0, per confronto: il vuoto del fondo e l'uniforme
    lam_corse = {}
    for scena in B.SCENE:
        st["phi_h"][...] = B.vuoto_iniziale(scena, inc, L)
        _r, lm = EL.densita(inc, st)
        lam_corse[scena] = (float(lm.min()), int(np.sum(lm == 0.0)))
    return {"taglia": taglia, "n": incu.n, "lam_zero": int(np.sum(lam == 0.0)), "lam_max": float(lam.max()), "rho_min": float(rho.min()),
            "nonfin": int(nonfin.sum()), "E_leg": E_leg, "E_mat": E_mat, "e_K": E_mat / M, "avvisi": sorted({str(a.message) for a in avvisi}),
            "lam_corse": lam_corse}


def main():
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_vuoto_congelato as VC
    s_vero = VC.S
    try:
        print("=" * 110)
        print("LA CAUSA DEL NaN IN E_leg: lo stato di _solitone_con_la_buca.prepara (SC.stato_uniforme, poi SC.parti), alle due taglie")
        print("=" * 110)
        for t in ("grande", "piccola"):
            r = misura(t)
            print("### %s: %d nodi; nello stato di costruzione Lambda = 0 su %d nodi (max %.3e), rho minimo %.6e;" % (t, r["n"], r["lam_zero"], r["lam_max"], r["rho_min"]))
            print("    lam * F1(rho / lam) non finito su %d nodi; E_leg = %r; E_mat = %.12e; e_K = E_mat / M = %.12e" % (r["nonfin"], r["E_leg"], r["E_mat"], r["e_K"]))
            print("    gli avvisi: %s" % r["avvisi"])
            for sc, (lmin, lz) in r["lam_corse"].items():
                print("    lo stato delle corse a t = 0, vuoto %-8s: Lambda minimo %.6e, nodi a zero %d" % (sc, lmin, lz))
    finally:
        VC.S = s_vero
    return 0


if __name__ == "__main__":
    sys.exit(main())
