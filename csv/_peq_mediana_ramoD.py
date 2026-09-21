# -*- coding: utf-8 -*-
"""SOLA LETTURA: la MEDIANA di `peq` negli snapshot del ramo D, e quanto `anom` produrrebbe.

Il candidato viene dal CODICE, non da un'intuizione: `:4846` (Schwinger) scrive
`peq = median(self.peq)` sui `2*nc` archi nuovi, e quegli archi **non** passano dalla
calibrazione `:4189` (che tocca solo i NaN di `_allaccia`). Se la mediana e' crollata
sotto il pavimento `1e-9`, un arco nuovo con `rho` ordinario da' `anom` enorme.
"""
import gzip
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

os.chdir(os.path.abspath(os.path.join(_QUI, "..")))
ARCH = os.path.join("csv", "_test_fork", "_ab_D")
ALPHA_M, DT, CS_M, PAV = 0.05, 0.01, 2.0, 1e-9

print("%6s %12s %12s %12s | %14s %14s %10s" % (
    "passo", "median(peq)", "min(peq)", "median(rho)", "anom se Schwinger", "|src|", "n1"))
print("-" * 96)
for k in (120, 600, 960, 1080, 1200):
    p = os.path.join(ARCH, "scena_%06d.pkl.gz" % k)
    if not os.path.exists(p):
        continue
    with gzip.open(p, "rb") as f:
        a = pickle.load(f)["attrs"]
    peq = np.asarray(a["peq"], float)
    I = np.abs(np.asarray(a["psi"])) ** 2
    i, j = np.asarray(a["i"]), np.asarray(a["j"])
    n = len(I)
    m = (i < n) & (j < n)
    rho = 0.5 * (I[i[m]] + I[j[m]])
    pm = float(np.nanmedian(peq))
    # un arco appena nato da Schwinger: peq = mediana globale, rho = quello della coppia
    anom_s = (np.median(rho) - pm) / max(pm, PAV)
    src = ALPHA_M * abs(anom_s)
    n1 = np.ceil(src * DT / (0.02 * CS_M))
    print("%6d %12.4e %12.4e %12.4e | %14.4e %14.4e %10.0f"
          % (k, pm, float(np.nanmin(peq)), float(np.median(rho)), anom_s, src, n1))

print()
print("LETTURA: `anom` cresce SOLO quando la mediana scende SOTTO il pavimento 1e-9.")
print("Finche' median(peq) >> 1e-9, un arco di Schwinger da' anom ~ rho/peq, grande ma non enorme.")
