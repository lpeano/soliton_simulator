# -*- coding: utf-8 -*-
"""Prova di fumo della scena (ii): geometria, saturazione, coerenza, distanza minima."""
import importlib.util as iu
import sys
import time

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sp = iu.spec_from_file_location("s", "soliton_simulator.py")
S = iu.module_from_spec(sp)
sp.loader.exec_module(S)
S.SEMINA_LAM = True


def prova(sep, casuali, seme=11):
    S.net = S.Rete(seme)
    S.test["dati"] = {}
    S._NMASSE_VIDEO["sep"] = sep
    S._MC_VIDEO["nodi"] = 0
    S._MC_VIDEO["fasi_casuali"] = casuali
    t0 = time.time()
    S._semina_masse_coerenti()
    dt = time.time() - t0
    co = S.test["dati"]["coorti"]
    D = S._dphi = S.net._dphi()
    print("  tempo %.1f s" % dt)
    for k in range(3):
        ph = S.net.phi[co["massa_%d" % k]]
        z = abs(np.mean(np.exp(1j * ph * 2 * np.pi / D)))
        print("    massa_%d  n=%-5d std(phi) %8.4f   COERENZA CIRCOLARE |<e^iphi>| = %.6f"
              % (k, len(ph), ph.std(), z))
    ph = S.net.phi[co["vuoto"]]
    z = abs(np.mean(np.exp(1j * ph * 2 * np.pi / D)))
    print("    vuoto    n=%-5d std(phi) %8.4f   COERENZA CIRCOLARE           = %.6f"
          "   nullo ~ 1/sqrt(n) = %.4f" % (len(ph), ph.std(), z, 1.0 / np.sqrt(len(ph))))
    from scipy.spatial import cKDTree
    dd = cKDTree(S.net.pos).query(S.net.pos, k=2)[0][:, 1]
    print("    min distanza fra nodi = %.9f   LAM = %.9f   archi = %d"
          % (dd.min(), S.LAM, len(S.net.d)))
    return S.test["dati"]["scena_ii"]


print("=" * 96)
print("SCENA (b)  --sep 4.0   fasi COERENTI")
d = prova(4.0, False)
print("   ", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in sorted(d.items())})
print()
print("SCENA (b)  --sep 4.0   fasi CASUALI  (braccio di controllo di S10)")
prova(4.0, True)
print()
print("SCENA (a)  --sep 6.1158   fasi COERENTI")
d = prova(6.1158, False)
print("   ", {k: (round(v, 6) if isinstance(v, float) else v) for k, v in sorted(d.items())})
