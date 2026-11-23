# -*- coding: utf-8 -*-
r"""**[M0037] L'EOTVOS AL FONDO A K CON LE MASSE 1 E 4** *(Luca, 2026-11-24 00:37; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-septies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/eotvos_fondo.py caduta --coll V2          (coll V0, V2)
    E:\python\py3132\python.exe doc/referti_l2/eotvos_fondo.py calcio --k 0.010         (k 0.0, 0.010)
    E:\python\py3132\python.exe doc/referti_l2/eotvos_fondo.py lettura > doc/referti_l2/eotvos_fondo.txt

**`fondo_1c.caduta` e `fondo_1c.calcio` cosi' come sono**, con `fondo_1c.OGGETTO` = l'oggetto a2 *(`M1658/tenuta_v2/L-1_a2.0_l1.0/stato_003000.npz`)* e `fondo_1c.BASE` = `M1658/c1_a2`, cambiate IN MEMORIA prima di tutto. **La lettura:** `m*(a2)`, `K(a2)` col `grad omega` di S3, `eta` fra 1c e a2.
"""
import argparse
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658")
OGG_A2 = os.path.join(CTRL, "tenuta_v2", "L-1_a2.0_l1.0", "stato_003000.npz")
BASE_A2 = os.path.join(CTRL, "c1_a2")
BASE_1C = F1.BASE


def su_a2():
    F1.OGGETTO = OGG_A2
    F1.BASE = BASE_A2


def mstar_K(base):
    F1.BASE = base
    MC = F1.MC
    r0, r1 = F1.leggi("calcio_%s" % MC.nome(0.0, 1)), F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    if r0 is None or r1 is None:
        return None
    v0, s0, _ = MC.velocita(r0["serie"])
    v1, s1, _ = MC.velocita(r1["serie"])
    m = 0.010 / (v1 - v0)
    return m, abs(m) * math.hypot(s0, s1) / abs(v1 - v0)


def caduta_netta(base):
    F1.BASE = base
    c, c0 = F1.leggi("caduta_V2"), F1.leggi("caduta_V0")
    if c is None or c0 is None:
        return None
    a, sa, dn = F1.fit_a(c["serie"])
    a0, sa0, _ = F1.fit_a(c0["serie"])
    return a - a0, math.hypot(sa, sa0), float(c["A"]), dn


def lettura():
    import _presidio
    import chi_parametri_v2 as CP2
    F1.avvia()
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0037] L'EOTVOS AL FONDO A K: LA MASSA 1 (1c) E LA MASSA 4 (a2) (la carta sez. 2-septies)")
    print("=" * 130)
    F1.BASE = BASE_1C
    D = {}
    for Nv in (0.9965, 1.0035):
        x = F1.leggi("orologio_V2_N%.4f" % Nv)
        D[Nv] = float((np.array(x["omega"]) - np.array(x["omega_phi"])).mean())
    dw_dN = (D[1.0035] - D[0.9965]) / 0.007
    R = {}
    for nome, base in (("1c (massa 1)", BASE_1C), ("a2 (massa 4)", BASE_A2)):
        ms = mstar_K(base)
        cd = caduta_netta(base)
        if ms is None or cd is None:
            print("  %s: NON FINITA" % nome)
            continue
        da, sda, A, dn = cd
        Ly = 162 * math.sqrt(3.0) / 2.0
        gw = dw_dN * (-CP2.KAPPA * A * 2.0 * math.pi / Ly)
        pred = -gw / ms[0]
        K = da / pred
        sK = abs(K) * math.hypot(sda / da, ms[1] / ms[0])
        R[nome] = (da, sda, K, sK)
        print("  %s: m* %+.4f +- %.4f; a - a(V0) %+.4e +- %.1e; -grad omega/m* %+.4e; K %+.4f +- %.4f; la norma %.1e" % (nome, ms[0], ms[1], da, sda, pred, K, sK, dn))
    if len(R) == 2:
        (a1, s1, K1, sK1), (a2, s2, K2, sK2) = R["1c (massa 1)"], R["a2 (massa 4)"]
        eta = 2.0 * abs(a1 - a2) / (a1 + a2)
        se = 4.0 * math.hypot(a2 * s1, a1 * s2) / (a1 + a2) ** 2
        print("### K(a2)/K(1c) %.4f; K(a2) - K(1c) %+.4f +- %.4f" % (K2 / K1, K2 - K1, math.hypot(sK1, sK2)))
        print("### eta = 2 |a1 - a2|/(a1 + a2) = %.4f +- %.4f (a_i = a - a(V0))" % (eta, se))
    print("=" * 130)
    return 0


def main(argv):
    import _presidio
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("caduta", "calcio", "lettura"))
    ap.add_argument("--coll", choices=("V0", "V2"))
    ap.add_argument("--k", type=float)
    a = ap.parse_args(argv)
    if a.cosa == "lettura":
        return lettura()
    su_a2()
    _presidio.avvia(__file__)
    if a.cosa == "caduta":
        return F1.caduta(a.coll)
    return F1.calcio(a.k)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
