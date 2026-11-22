# -*- coding: utf-8 -*-
r"""**[M1446-L] LE K DI V2 E V3 DA QUATTRO ZERI, FIANCO A FIANCO** *(l'aggiunta v3 di Luca a [M1446]; la carta `doc/CARTA_E_mc2.md`, sez. `3`; SOLA LETTURA; POST-HOC, dichiarato)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/legge_zeri.py > doc/referti_l2/legge_zeri.txt

**Gli zeri:** `0` *(lo zero simmetrico)*; `omega(1) + e0` *(= lo zero di V3 di [M1427])* e `omega(1) - omega_F3` *(fissi)*; **il vuoto LOCALE** *(`Delta(N) = omega_psi(N) - omega_phi_locale(N)`, misurato negli stati dell'orologio `N1`, `NmV2`, `NmV3`, `NpV3`, `k 250 ... 1000`, con `orologio_relativo.fasi`: `theta_v` col peso `rho` entro `r 15`, e il vuoto lontano `r > 40`)*. **`K = (a/(c^2 |grad N|)) / (d ln|omega - E0|/dN)`** col segno, `a` col verso da `caduta_libera.txt` *(positivo = VIA)*. **Il controllo di V2:** `(omega_psi - omega_vuoto_lontano)(N) = (omega(1) - omega_F3) N` entro `1e-3`.
"""
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import girandola_chi_v3 as GC  # noqa: E402
import orologio_mattone_v2 as OM  # noqa: E402
import orologio_relativo as ORL  # noqa: E402
import orologio_zero as OZ  # noqa: E402

C = {"c_m = 0.588 s": 0.588 * 0.15, "c = s": 0.15}
FORME = {"V2": ("N1", "NmV2"), "V3": ("NmV3", "N1", "NpV3")}


def main():
    import _presidio
    for m in ("orologio_relativo.py", "orologio_zero.py", "orologio_mattone_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    print("=" * 130)
    print("[M1446-L] LE K DI V2 E V3 DA QUATTRO ZERI (la carta sez. 3; POST-HOC, dichiarato)")
    print("=" * 130)
    MT = TC.moduli()[0]
    t0 = MT.G2.T0
    misure = {}
    with TC.scena() as Z:
        L = Z["L"]
        nodo = GC.toro_nodo(L)
        for var in ("N1", "NmV2", "NmV3", "NpV3"):
            ks = (250, 500, 750, 1000)
            tl, tf = [], []
            for k in ks:
                X, meta = ORL.PR_leggi(os.path.join(OM.BASE, var, "stato_%06d.npz" % k))
                o, far, _nf = ORL.fasi(Z, X["psi_h"], X["phi_h"], t0 + k, nodo, L, centri=(meta["centro"], meta["bari_k0"]))
                tl.append(o[0][2])
                tf.append(far)
            ac = ORL.arg_c(Z, t0 + ks[0], t0 + ks[-1])
            wF3 = -float(ac[-1] - ac[0]) / (ks[-1] - ks[0])
            dl = [ORL.PR.wrap(b - a) for a, b in zip(tl, tl[1:])]
            dfa = [ORL.PR.wrap(b - a) for a, b in zip(tf, tf[1:])]
            wphi = wF3 - float(np.mean(dl)) / 250.0
            wfar = wF3 - float(np.mean(dfa)) / 250.0
            wpsi = OZ.omega(var)
            misure[var] = (OM.VAR[var][0], wpsi, wphi, wfar, wF3, max(abs(x) for x in dl + dfa))
            print("  %-5s N %.4f: omega_psi %.10f; omega_phi locale %.8f (theta_v si sposta di %s rad in 250 tick); il vuoto lontano %.10f; omega_F3 %.10f" % (
                var, OM.VAR[var][0], wpsi, wphi, ", ".join("%+.4f" % x for x in dl), wfar, wF3))
        Z["metti"]()
    amb = max(m[5] for m in misure.values())
    print("  il controllo: lo spostamento massimo di theta_v fra due stati %.4f rad (sotto pi/2: %s)" % (amb, "SI'" if amb < math.pi / 2 else "### NO: ambiguo"))
    w1, wF3 = misure["N1"][1], misure["N1"][4]
    print("-" * 130)
    print("  IL CONTROLLO DI V2: (omega_psi - omega_vuoto_lontano)(N) contro (omega(1) - omega_F3) N = %.6f N" % (w1 - wF3))
    for var in FORME["V2"]:
        Nv, wp, _wl, wf, _f, _a = misure[var]
        x = wp - wf
        print("    %-5s N %.4f: %.6f contro %.6f: lo scarto %+.3e (%s)" % (var, Nv, x, (w1 - wF3) * Nv, x - (w1 - wF3) * Nv, "entro 1e-3" if abs(x - (w1 - wF3) * Nv) <= 1e-3 else "### FUORI"))
    cad = open(os.path.join(_QUI, "caduta_libera.txt"), encoding="utf-8").read()
    print("-" * 130)
    for forma, vs in FORME.items():
        m = re.search(r"^\s+%s\s+il baricentro\s+.*?: (VERSO|VIA) .*?\|a - a\(V0\)\| / \(c\^2 \|dN/dy\|\) = ([0-9.]+) \(c = 0\.588 s\), ([0-9.]+) \(c = s\)" % forma, cad, re.M)
        sg = 1.0 if m.group(1) == "VIA" else -1.0
        a = {"c_m = 0.588 s": sg * float(m.group(2)), "c = s": sg * float(m.group(3))}
        Ns = np.array([misure[v][0] for v in vs])
        wp = np.array([misure[v][1] for v in vs])
        wl = np.array([misure[v][2] for v in vs])
        zeri = [("0 (lo zero simmetrico)", np.zeros_like(Ns)), ("omega(1) + e0 = %.6f (fisso)" % (w1 + e0), np.full_like(Ns, w1 + e0)),
                ("omega(1) - omega_F3 = %.6f (fisso)" % (w1 - wF3), np.full_like(Ns, w1 - wF3)), ("il vuoto LOCALE (misurato a ogni N)", wl)]
        print("  %s (a/(c^2 |grad N|): %s; i punti N %s)" % (forma, ", ".join("%s %+.3f" % (k, v) for k, v in a.items()), Ns.tolist()))
        for nome, E0 in zeri:
            D = np.abs(wp - E0)
            dlnD = float(np.polyfit(Ns, np.log(D), 1)[0])
            print("    lo zero %-44s Delta(1) %.6f; d ln Delta/dN %+.5f; K: %s" % (nome, float(D[list(vs).index("N1")]), dlnD, "; ".join("%s %+.3f" % (k, v / dlnD) for k, v in a.items())))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
