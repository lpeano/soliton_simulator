# -*- coding: utf-8 -*-
r"""**[M1631-E] L'EQUIVALENZA DI S1-bis: lambda = -1 E' IL CAMMINO CONIUGATO?** *(il mandato di Luca [M1631], 1d; la carta `doc/CARTA_torneo_nonlinearita.md`, sez. `2` e `6`; IN MEMORIA, nessun file del nucleo toccato)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/equivalenza_lambda.py > doc/referti_l2/equivalenza_lambda.txt

**UN tick intero** *(`tick.percorri_tick`, l'ordine intero, senza `U` e senza `chi`)* **su uno stato con materia** *(`CHI/caduta/V0/stato_001000`, S162: la scena di tutte le misure, non `L 16`, dichiarato)*. **Tre ticks:** **A** = `lambda = -1` *(`alpha -> -alpha_S1`, `beta -> -beta_S1` in memoria)*, `cs = s`, `eps = +0.5`; **B** = F0, `cs = -s` *(`theta -> -theta`: `theta = pi dtau_nodo/dtau_rif`)*, `eps = -0.5` *(`a -> -a`)*, applicato al CONIUGATO dello stato; **C** = F0, `cs = s`, `eps = 0.5`. **Le due affermazioni:** **(S1-bis, del mandato)** `T_A(X) = conj(T_B(conj X))` entro `1e-12`; **(dalle righe)** `T_C(X) = conj(T_B(conj X))` *(perche' `materia_vuoto.applica` usa `dtau_nodo = dtau cs`: con `cs -> -s` si rovescia ANCHE il tempo della non linearita')*. Lo scarto relativo su `psi_h` e `phi_h`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402

TOLL = 1e-12                    # ### il mandato


def main():
    import _presidio
    import composizione as CM
    import tick as TK
    import materia_vuoto as MV
    from termini import camm_moneta_spin as TMS
    _presidio.avvia(__file__)
    X, _meta = GM.leggi(os.path.join(CL.BASE, "V0", "stato_001000.npz"))
    print("=" * 130)
    print("[M1631-E] L'EQUIVALENZA DI S1-bis (la carta sez. 2, 6): UN tick intero sullo stato CHI/caduta/V0/stato_001000 (S162); la forma del nucleo %s, eps %r" % (MV.ATTIVA, TMS.PARAMETRI["eps"]))
    print("=" * 130)
    a0, b0, eps0 = MV.alpha, MV.beta, TMS.PARAMETRI["eps"]
    out = {}
    with TC.scena() as Z:
        mot, st, par = Z["mot"], Z["st"], Z["par"]
        n, s = mot.inc.n, float(Z["s"])
        cs0, lc0 = mot.cs, getattr(mot, "lambda_c", None)

        def tick(nome, coniuga, segno_cs, eps, lam):
            Z["metti"]({x: X[x] for x in Z["chiavi"]})
            if coniuga:
                st["psi_h"][...] = np.conj(st["psi_h"])
                st["phi_h"][...] = np.conj(st["phi_h"])
            mot.cs = np.full(n, segno_cs * s)
            mot.lambda_c = None
            TMS.PARAMETRI["eps"] = eps
            if lam != 1.0:
                MV.alpha = lambda r, l_: lam * a0(r, l_)
                MV.beta = lambda r, l_: lam * b0(r, l_)
            try:
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                y = (st["psi_h"].copy(), st["phi_h"].copy())
            finally:
                MV.alpha, MV.beta, TMS.PARAMETRI["eps"] = a0, b0, eps0
                mot.cs, mot.lambda_c = cs0, lc0
            if coniuga:
                y = (np.conj(y[0]), np.conj(y[1]))
            out[nome] = y
            print("  %s: cs %+g s, eps %+g, lambda %+g, lo stato %s; |psi_h| %.6e, |phi_h| %.6e" % (nome, segno_cs, eps, lam, "CONIUGATO prima e dopo" if coniuga else "com'e'", float(np.linalg.norm(y[0])), float(np.linalg.norm(y[1]))))
        try:
            tick("A (lambda -1)", False, 1.0, eps0, -1.0)
            tick("B (F0, theta e a rovesciati, coniugato)", True, -1.0, -eps0, 1.0)
            tick("C (F0, oggi)", False, 1.0, eps0, 1.0)
        except Exception as ex:
            print("### il tick con cs < 0 o eps < 0 ALZA: %r -- 1d non si puo' fare in memoria cosi'" % (ex,))
            Z["metti"]()
            print("=" * 130)
            return 1
        Z["metti"]()

    def scarto(p, q):
        return max(float(np.linalg.norm(p[i] - q[i]) / np.linalg.norm(q[i])) for i in (0, 1))
    sA = scarto(out["A (lambda -1)"], out["B (F0, theta e a rovesciati, coniugato)"])
    sC = scarto(out["C (F0, oggi)"], out["B (F0, theta e a rovesciati, coniugato)"])
    sAC = scarto(out["A (lambda -1)"], out["C (F0, oggi)"])
    print("-" * 130)
    print("  S1-bis (del mandato): T_A(X) contro conj(T_B(conj X)): lo scarto relativo massimo %.3e" % sA)
    print("  dalle righe:          T_C(X) contro conj(T_B(conj X)): %.3e" % sC)
    print("  il controllo:         T_A(X) contro T_C(X) (lambda -1 contro F0, devono differire): %.3e" % sAC)
    print("  DEVE: 1d (S1-bis, entro 1e-12)                                                       %s" % ("PASSA" if sA <= TOLL else "### FALLISCE"))
    print("  l'affermazione dalle righe (il tempo della non linearita' segue cs)                  %s" % ("VERA entro 1e-12" if sC <= TOLL else "falsa"))
    print("=" * 130)
    return 0 if sA <= TOLL else 1


if __name__ == "__main__":
    sys.exit(main())
