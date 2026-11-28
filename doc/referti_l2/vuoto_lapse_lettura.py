# -*- coding: utf-8 -*-
r"""**[M0026] F, LA LETTURA: IL VUOTO CON IL LAPSE DIPINTO CONTRO IL VUOTO PIATTO DI [M0106]** *(DECISIONE DI LUCA, 2026-11-28 00:26;
la carta `doc/CARTA_mitosi.md`, «F, LA VIA (a)»; lettura, nessun tick)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/vuoto_lapse_lettura.py > doc/referti_l2/vuoto_lapse_mitosi.txt

Per gli stati `36000, 37000, ..., 41000, 41976` di `M0026/F` *(dipinto)* e di `M0237/vuoto_v2` *([M0106], piatto)*: `max |Theta|` e gli archi oltre `pi`;
la norma `somma |phi_h|^2`; **per fascia del seno** *(`u = 2 pi (y - y_c)/L_y`, `y_c = 0`; il FONDO `sin u < -0.5`, i FIANCHI `|sin u| <= 0.5`, la
CIMA `sin u > 0.5`)*: `rho_phi` medio e **`J_y`** medio *(`vuoto_giro3`: `rho_phi grad theta`, `theta` la fase di `somma conj(phi_v) phi`)* con il
segno del gradiente di `N` *(positivo = verso dove `N` cresce, cioe' verso il fondo del pozzo dipinto)*. `H` dall'ultima `serie_*.npz`.
**Casi noti** *(V1 di `vuoto_giro3`, su `L 186`)*: il vuoto fresco ha corrente `0` entro `1e-9`; DEVE FALLIRE con una fase `q y`.
"""
import glob
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import vuoto_giro3 as VG  # noqa: E402
import vuoto_lapse_mitosi as VL  # noqa: E402

KS = (36000, 37000, 38000, 39000, 40000, 41000, 41976)
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "vuoto_giro3.py"))
    _presidio.avvia(os.path.join(_QUI, "vuoto_lapse_mitosi.py"))
    _presidio.avvia(__file__)
    PS = VL.PS
    print("=" * 130)
    print("[M0026] F, LA LETTURA: il vuoto con il lapse dipinto (M0026/F) contro il vuoto piatto di [M0106] (M0237/vuoto_v2)")
    print("=" * 130)
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        pv = np.asarray(Z["phi_v"]).copy()
        Z["metti"]()
    A, G20, Ly, kappa = VL.ampiezza(L)
    vic = (((m1 - 1) % L) * L + m2, ((m1 + 1) % L) * L + m2, ((m1 - 1) % L) * L + (m2 - 2) % L, ((m1 + 1) % L) * L + (m2 + 2) % L)
    rv, Zv = VG.per_nodo(pv, pv, nodo, n)
    jx, jy = VG.correnti(rv, Zv, vic)
    jm = float(max(np.max(np.abs(jx)), np.max(np.abs(jy))))
    esito("(V1) il vuoto fresco su L 186: la corrente 0 entro 1e-9", jm < 1e-9, "max |J| %.1e" % jm)
    y = m2 * VG.S3 / 2.0
    q = 2.0 * math.pi * 2.0 / (L * VG.S3 / 2.0)
    rq, Zq = VG.per_nodo(pv * np.exp(1j * q * y[nodo]), pv, nodo, n)
    _jx, jyq = VG.correnti(rq, Zq, vic)
    esito("(V1) DEVE FALLIRE lo zero: una fase q y da' una corrente lungo y", float(np.max(np.abs(jyq))) > 1e-6, "max |J_y| %.3e" % float(np.max(np.abs(jyq))))
    u = 2.0 * math.pi * (y - VL.Y_C) / Ly
    su = np.sin(u)
    dN = -kappa * A * (2.0 * math.pi / Ly) * np.cos(u)            # ### il segno di dN/dy (N = exp(-kappa A sin u))
    fasce = (("il FONDO (sin u < -0.5)", su < -0.5), ("i FIANCHI (|sin u| <= 0.5)", np.abs(su) <= 0.5), ("la CIMA (sin u > 0.5)", su > 0.5))
    print("  L %d, L_y %.6f, A %.6e, kappa %r; N da %.6f a %.6f" % (L, Ly, A, kappa, float(np.exp(-kappa * A)), float(np.exp(kappa * A))))
    print("-" * 130)
    for nome, d in (("DIPINTO (M0026/F)", VL.D_OUT), ("PIATTO ([M0106], M0237/vuoto_v2)", VL.D_M0106)):
        print("### %s: %s" % (nome, d))
        for k in KS:
            f = os.path.join(d, "stato_%05d.npz" % k)
            if not os.path.exists(f):
                print("    k %d: lo stato non c'e'" % k)
                continue
            with np.load(f) as z:
                phi, th = z["phi_h"], np.abs(z["theta_a"])
                nn = len(z["Lambda"])
            assert nn == n, "lo stato ha %d nodi, la scena %d: nel vuoto non doveva nascere niente" % (nn, n)
            rho, Zn = VG.per_nodo(phi, pv, nodo, n)
            jx, jy = VG.correnti(rho, Zn, vic)
            jv = jy * np.sign(dN)                                  # ### positivo = verso dove N cresce (il fondo)
            riga = "    k %5d: max |Theta| %.4f (oltre pi %d); la norma %.12e;" % (k, float(th.max()), int((th > math.pi).sum()), float(np.sum(np.abs(phi) ** 2)))
            for nf, msk in fasce:
                riga += "  %s rho_phi %.6f J_y verso N+ %+.3e;" % (nf.split(" (")[0], float(rho[msk].mean()), float(jv[msk & (np.abs(dN) > 0)].mean()))
            print(riga)
    for nome, d in (("DIPINTO", VL.D_OUT), ("PIATTO", VL.D_M0106)):
        fs = sorted(glob.glob(os.path.join(d, "serie_*.npz")))
        if fs:
            with np.load(fs[-1]) as z:
                k_, E = z["k"], z["E"]
            print("### H, %s (%s): da %+.12e (k %d) a %+.12e (k %d): |dH|/|H| %.3e" % (nome, os.path.basename(fs[-1]), float(E[0]), int(k_[0]), float(E[-1]), int(k_[-1]), abs(float(E[-1] - E[0])) / abs(float(E[0]))))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
