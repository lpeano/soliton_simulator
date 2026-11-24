# -*- coding: utf-8 -*-
r"""**[M1640-R] IL RESPIRO A N UNIFORME -- LA V2 DI `respiro_N.py`** *(la v1, sha1 dei byte `3c9dc596`, e' usata e non si riscrive: le sei corse caddero alla stampa di partenza di `corsa`, `TypeError`: la stringa ha `%g` per `R_C` e gli argomenti no; il log `respiro_N_fallito.txt`, `2b3c2b0d`)*. **Una sola differenza:** `corsa` riga per riga con `R_C` negli argomenti della stampa. Le cartelle, i casi noti e la lettura sono quelli della v1. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/respiro_N_v2.py --riga V2 --N 0.99 --fino 20000
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import respiro_N as RN  # noqa: E402
from respiro_N import TC, TT, avvia, cartella, scena, R_C, R10, rho_di, w_picco, OGNI_W, OGNI_STATO, omega_di, ciclo, K_FINO  # noqa: E402,F401


def corsa(riga, N, k_fino):
    avvia()
    MV, P0 = TT.nucleo()
    d_out = cartella(riga, N)
    os.makedirs(d_out, exist_ok=True)
    fatti = sorted(int(f[6:12]) for f in os.listdir(d_out) if f.startswith("stato_") and f.endswith(".npz") and os.path.exists(os.path.join(d_out, f + ".sha1")))
    t1 = time.time()
    with TC.scena() as Z:
        C, info, G, Nv, cs_N, segno, e0, s = scena(Z, riga, N, MV, P0)
        S = {"om": [], "omc": [], "om10": [], "kw": [], "w": [], "mx": [], "M": [], "s_tick": []}
        k0 = 0
        if fatti:
            import gravita_due_corpi_misure as GM
            import _u1_prototipo as U1
            k0 = fatti[-1]
            X, _m = GM.leggi(os.path.join(d_out, "stato_%06d.npz" % k0))
            Z["metti"]({x: X[x] for x in Z["chiavi"]})
            C.campo.A[...] = X["campo_A"]
            C.campo.E[...] = X["campo_E"]
            U1.scrivi_U(Z["mot"], C.campo)
            S = json.load(open(os.path.join(d_out, "serie_%06d.json" % k0), encoding="utf-8"))
            assert len(S["om"]) == k0
            print("### LA RIPRESA P8: dallo stato a k %d" % k0)
        elif riga == "CTRL":
            Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * np.exp(1j * float(e0) * (0.99 - 1.0))
        print("### %s N %.2f (cs_N %s, segno %d): %s (k %d); il centro %d; %d nodi a r < %g, %d a r in %s; e0 %.10f; fino a %d" % (
            riga, N, cs_N, segno, info["file"], info["k_file"], G["centro"], int(np.sum(G["r"] < R_C)), R_C, int(np.sum((G["r"] >= R10[0]) & (G["r"] < R10[1]))), R10, e0, k_fino))

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            fj = os.path.join(d_out, "serie_%06d.json" % k)
            open(fj, "w", encoding="utf-8").write(json.dumps(S))
            np.savez(fz, meta=np.array(json.dumps({"riga": riga, "N": N, "cs_N": cs_N, "segno": segno, "k": k, "partenza": info["file"], "centro": G["centro"], "e0": e0})), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")

        def misura(k):
            rho = rho_di(Z, G)
            w, mx = w_picco(rho, G)
            S["kw"].append(k)
            S["w"].append(w)
            S["mx"].append(mx)
            S["M"].append(float(rho.sum()))
        if not fatti:
            misura(0)
            salva(0)
        ta = [time.time()]

        def dopo(kk, prima):
            k = k0 + kk
            ps = Z["st"]["psi_h"]
            S["om"].append(omega_di(prima, ps))
            S["omc"].append(omega_di(prima, ps, G["mc"]))
            S["om10"].append(omega_di(prima, ps, G["m10"]))
            S["s_tick"].append(time.time() - ta[0])
            ta[0] = time.time()
            if k % OGNI_W == 0:
                misura(k)
            if k % OGNI_STATO == 0:
                salva(k)
                print("    [stato] k %d: w %.3f, il picco %.4e, omega %+.7f, omega_c - omega_10 %+.3e, la norma %.12e; %.3f s/tick (%.0f s)" % (
                    k, S["w"][-1], S["mx"][-1], S["om"][-1], S["omc"][-1] - S["om10"][-1], S["M"][-1], float(np.mean(S["s_tick"][-250:])), time.time() - t1))
                sys.stdout.flush()
        ciclo(Z, C, k_fino - k0, dopo, MV, P0, Nv, cs_N, segno, e0, s)
        Z["metti"]()
    print("### %d tick in %.0f s" % (k_fino - k0, time.time() - t1))
    return 0


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--riga", choices=tuple(RN.RIGHE), required=True)
    ap.add_argument("--N", type=float, required=True)
    ap.add_argument("--fino", type=int, required=True)
    a = ap.parse_args(argv)
    return corsa(a.riga, a.N, a.fino)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
