# -*- coding: utf-8 -*-
r"""**[M0528-N] IL VUOTO COL LAPSE DAL VINCOLO -- LA V2** *(`lapse_vincolo.vuoto` cadde alle `08:56`: `C.residuo()` divide per `e max rho`, e nel vuoto di `TC.scena` `psi_h = 0`; il log `doc/referti_l2/lapse_vincolo_vuoto_fallito.txt`. `lapse_vincolo.py` e' in uso e non si tocca: qui `vuoto` riga per riga con UNA differenza: **il controllo di Gauss si salta se `max rho = 0`** -- e' una diagnosi, non scrive niente; il numero di volte che si salta e' scritto nella serie)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo_vuoto.py --riga V2      (le cartelle vuoto_v2_<riga>; 500 tick; riparte dall'ultimo stato)
"""
import argparse
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import lapse_vincolo as LV  # noqa: E402


def vuoto(riga, k_fino=LV.K_VUOTO):
    import _presidio
    LV.avvia()
    _presidio.avvia(__file__)
    _G20, _ia, e0, MT = LV.CL.parametri()
    d_out = os.path.join(LV.BASE, "vuoto_v2_%s" % riga)
    os.makedirs(d_out, exist_ok=True)
    fatti = LV._fatti(d_out)
    t1 = time.time()
    with LV.TC.scena() as Z:
        MT_, _MTR, _T1, _TRU, _TV, PO = LV.TC.moduli()
        rho_c, e, t0 = MT_.rho_c_assoluto(), MT_.PB.E_DECISO, MT_.G2.T0
        n = Z["n"]
        Z["g_e"] = np.zeros_like(Z["g_e"])
        MT_.vuoto_fresco(Z, t0)
        C = PO.campi(Z, rho_c, e)
        s = float(Z["s"])
        u0 = LV.u_di(Z["z"], riga, s, e0, np.ones(n))
        meta = {"variante": riga, "kappa": LV.KAPPA, "c2": LV.C2, "s": s, "e0": e0, "max_psi": float(np.max(np.abs(Z["st"]["psi_h"]))), "u_min": float(u0.min()), "u_max": float(u0.max())}
        print("### il vuoto %s (la v2): max |psi_h| %.3e; u a k 0 da %.17e a %.17e (lo scarto %.3e); l'impronta %s" % (riga, meta["max_psi"], u0.min(), u0.max(), u0.max() - u0.min(), LV.CL.impronta(Z, C)[:12]))
        sol = LV.Solutore(Z["mot"], LV.C2)
        X = {"chi": np.zeros(n)}
        serie = {"it": [], "max_N_1": [], "s_tick": [], "gauss_saltati": 0}
        k0 = 0
        if fatti:
            k0 = fatti[-1]
            X_, serie = LV._riprendi(d_out, k0, Z, C)
            X["chi"] = X_["chi_ris"].copy()
            print("### LA RIPRESA P8: dallo stato a k %d" % k0)
        uno = np.ones(n)

        def salva(k):
            LV._salva(d_out, k, Z, C, meta, {"chi_ris": X["chi"]}, serie)
        if not fatti:
            salva(0)
        for k in range(k0 + 1, k_fino + 1):
            ta = time.time()
            serie["it"].append(LV.tick(Z["z"], C.campo, riga, True, uno, X, sol, LV.KAPPA, s, e0, k == 1))
            if k % MT.OGNI_GAUSS == 0:
                if float(LV.CT.rho_di(Z["mot"], Z["st"]).max()) > 0.0:
                    C.residuo()
                else:
                    serie["gauss_saltati"] += 1
            serie["max_N_1"].append(float(np.max(np.abs(np.exp(-LV.KAPPA * X["chi"]) - 1.0))))
            serie["s_tick"].append(time.time() - ta)
            if k % 250 == 0:
                salva(k)
                print("    [stato] k %d: max|N - 1| %.3e (su tutta la corsa %.3e); le iterazioni max %d; il controllo di Gauss saltato %d volte (max rho = 0); %.2f s/tick (%.0f s)" % (
                    k, serie["max_N_1"][-1], max(serie["max_N_1"]), max(serie["it"]), serie["gauss_saltati"], float(np.mean(serie["s_tick"][-250:])), time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--riga", choices=("V2", "V3", "V2V3"), required=True)
    sys.exit(vuoto(ap.parse_args(sys.argv[1:]).riga))
