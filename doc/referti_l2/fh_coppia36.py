# -*- coding: utf-8 -*-
r"""**[M0326-K] IL CASO NOTO DELLA COPPIA A d 36** *(`fh_suite.coppia_stampo` a `d 35` FALLI': `gravita_due_corpi_d.vertici` vuole `d` multiplo di `3` -- «il vettore della coppia non porta su un nodo buono», `doc/referti_l2/coppia_caso_noto_d35_fallita.txt`; qui `d 36`, il multiplo di 3 piu' vicino, scelta mia dichiarata; il resto `fh_suite.coppia_stampo` riga per riga)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fh_coppia36.py corsa
    E:\python\py3132\python.exe doc/referti_l2/fh_coppia36.py lettura > doc/referti_l2/coppia_caso_noto.txt

**La lettura:** `a` dal fit di `gravita_due_corpi_misure.fit`; **i confronti, tutti riscalati per `1/d`** *(la legge del 2D: mia, dichiarata)*: il mandato `-1.0e-06` a `d 35` -> `x 35/36`; F-off `-1.2603e-06` a `d 39` -> `x 39/36`; lo stato compatto `-1.3867e-06` a `d 35` *(M0149)* -> `x 35/36`. **K1:** entro il `15%` del mandato riscalato.
"""
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import massa_calcio as MC  # noqa: E402
import torneo_tenuta as TT  # noqa: E402
import fondo_suite_v2 as FS  # noqa: E402
import fh_suite as FHS  # noqa: E402

D = 36
NOME = "coppia_F0_stampo_d36"


def corsa():
    import gravita_fase as GF
    import gravita_due_corpi_d as GDD
    from solitone import toro as TO
    FHS.avvia()
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fh_suite.py"))
    MV, P0 = TT.nucleo()
    GF.D = D
    GDD.avvia()
    d_out = os.path.join(FHS.BASE, NOME)
    os.makedirs(d_out, exist_ok=True)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info = GF.prepara(Z, 0)
        V = np.asarray(info["centri"], float)
        M = 0.5 * (V[0] + V[1])
        A1 = np.asarray(TO.vettori()[0], float)[:2]
        dxy = TO.scarti(Z["m1"], Z["m2"], M[0], M[1], L)[:, :2]
        lato = dxy @ (A1 / np.hypot(*A1))
        print("### la coppia F0 dallo stampo: d %d (la distanza dei vertici %.4f), le fasi %s; l'impronta %s" % (GF.D, info["distanza"], info["fasi_gradi"], TT.impronta(Z, C)[:12]))
        Ds = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = [(dxy[s_] * rho[s_][:, None]).sum(axis=0) / rho[s_].sum() for s_ in (lato < 0.0, lato >= 0.0)]
            Ds.append((kk, float(np.hypot(*(b[1] - b[0]))), float(rho.sum())))

        def dopo(kk, prima):
            if kk % MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: D %.4f (%.0f s)" % (kk, Ds[-1][1], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        FS._tick_loop(Z, C, "S1", FHS.K_COPPIA, dopo, MV, P0, np.ones(n), False)
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"D": Ds, "info": {k: info[k] for k in ("centri", "distanza", "fasi_gradi")}}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (FHS.K_COPPIA, time.time() - t1))
    return 0


def lettura():
    import gravita_due_corpi_misure as GM
    import _presidio
    _presidio.avvia(__file__)
    r = FHS._leggi(NOME)
    ks = np.array([x[0] for x in r["D"]], float)
    Dv = np.array([x[1] for x in r["D"]], float)
    fb = GM.fit(ks, Dv)
    a, sa = fb[2], fb[3]
    print("=" * 130)
    print("[M0326-K] IL CASO NOTO DELLA COPPIA, d %d (la carta sez. 4; d 35 non e' un nodo buono)" % D)
    print("=" * 130)
    print("  F0 in fase dallo stampo, la distanza %.4f: D da %.4f a %.4f; a %+.4e +- %.1e (il residuo %.2e); la norma %.9e -> %.9e" % (r["info"]["distanza"], Dv[0], Dv[-1], a, sa, fb[4], r["D"][0][2], r["D"][-1][2]))
    ok = None
    for nome, rif in (("il mandato -1.0e-06 a d 35, x 35/36", -1.0e-06 * 35.0 / D), ("F-off -1.2603e-06 a d 39, x 39/36", -1.2603e-06 * 39.0 / D), ("lo stato compatto -1.3867e-06 a d 35, x 35/36", -1.3867e-06 * 35.0 / D)):
        print("    contro %s = %+.4e: il rapporto %.3f" % (nome, rif, a / rif))
        if ok is None:
            ok = abs(a / rif - 1.0) <= 0.15
    print("  DEVE: K1 S5: entro il 15%% del mandato riscalato   %s" % ("PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(corsa() if sys.argv[1:] == ["corsa"] else lettura())
