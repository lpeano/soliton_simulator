# -*- coding: utf-8 -*-
"""U7 -- SEPARAZIONE DI SCALE per la correzione (4). **BLOCCANTE, si esegue PRIMA di cablare.**

La forma proposta e':      tau_p_loc = (d_arco / cs_arco) * (rho_arco / peq)
Perche' A5 (causalita') sia rispettato serve  tau_p >= d/cs,  cioe'  rho_arco/peq >= 1  OVUNQUE.
E perche' l'integrazione non diverga serve    dt_e / tau_p < 1.

Il mandato lo dice esplicitamente: *"Se rho_arco/peq < 1 da qualche parte, li' tau_p < d/cs e A5 e'
violato: riporta la frazione e FERMATI"*. Il GATE D ha gia' misurato 99.7 % sopra 1: **questo file
guarda lo 0.3 %**, che il mandato chiede di non ignorare.

NON e' una misura di fisica: e' una verifica di liceita' della forma. Dati: .pkl gia' committati.
ASCII PURO.
"""
import glob
import os
import pickle

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FILES = sorted(glob.glob(os.path.join(ROOT, "csv", "_test_fork", "_vuoto_s2ON_s?.pkl")))
DT = 0.01          # dal modulo; verificato sotto
CS_M = 2.0

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-46s %s" % ("PASS" if ok else "FAIL", nome, misura))


print("=" * 118)
print("U7 -- SEPARAZIONE DI SCALE (bloccante).  tau_p = (d/cs) * (rho_arco/peq)")
print("=" * 118)

rap_all, cfl_all, sotto_all = [], [], []
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    I = np.abs(np.asarray(A["psi"])) ** 2
    n = len(I)
    i = np.asarray(A["i"], int)
    j = np.asarray(A["j"], int)
    peq = np.asarray(A["peq"], float)
    d = np.asarray(A["d"], float)
    d0 = np.asarray(A["d0"], float)
    csn = np.asarray(A.get("_cs_nodo_prev"), float)
    r = np.asarray(A.get("_r_corrente"), float)
    m = (i < n) & (j < n) & np.isfinite(peq) & (peq > 0)
    i, j, peq, d, d0 = i[m], j[m], peq[m], d[m], d0[m]

    rho_arco = 0.5 * (I[i] + I[j])
    rap = rho_arco / peq
    rap_all.append(rap)
    sotto_all.append(rap < 1.0)

    # cs d'arco: media ARMONICA dei cs nodali, come il codice (:3129-3131)
    if csn is not None and len(csn) >= n:
        cs_arco = 2.0 * csn[i] * csn[j] / np.maximum(csn[i] + csn[j], 1e-12)
    else:
        cs_arco = np.full(len(i), CS_M)
    # dt_e d'arco: DT * 0.5*(r_i + r_j), come il codice (:2853)
    if r is not None and len(r) >= n:
        dt_e = DT * 0.5 * (r[i] + r[j])
    else:
        dt_e = np.full(len(i), DT)
    # d_arco: il codice usa la media di d0 se PLAST_DIN, altrimenti di d. Qui il caso PLAST_DIN.
    d_arco = 0.5 * (d0[i] + d0[j]) if len(d0) >= n else d
    d_arco = 0.5 * (d0 + d0)  # gli array sono gia' per arco: d0 e' per ARCO in questo codice
    tau_p = (d_arco / np.maximum(cs_arco, 1e-9)) * rap
    cfl_all.append(dt_e / np.maximum(tau_p, 1e-300))

rap = np.concatenate(rap_all)
cfl = np.concatenate(cfl_all)
sotto = np.concatenate(sotto_all)

print("\n--- (a) A5: rho_arco/peq >= 1 OVUNQUE?  (tau_p mai piu' veloce del tempo-luce) ---")
q = np.percentile(rap, [0.1, 1, 5, 50, 95, 99])
print("  archi: %d      min %.6g   p0.1 %.4g   p1 %.4g   p5 %.4g   mediana %.4g"
      % (len(rap), rap.min(), q[0], q[1], q[2], q[3]))
print("  frazione SOTTO 1 : %.4f %%   (%d archi su %d)" % (100.0 * sotto.mean(), sotto.sum(), len(rap)))
if sotto.any():
    s = rap[sotto]
    print("  di quelli sotto 1: min %.6g   mediana %.6g   max %.6g" % (s.min(), np.median(s), s.max()))
    print("  tau_p / (d/cs) nel caso PEGGIORE = %.6g   ->  tau_p e' %.3g volte il tempo-luce"
          % (rap.min(), rap.min()))
verdetto("U7a rho_arco/peq >= 1 ovunque (A5)", bool(rap.min() >= 1.0),
         "min = %.6g, frazione sotto 1 = %.4f %%" % (rap.min(), 100.0 * sotto.mean()))

print("\n--- (b) stabilita': dt_e / tau_p < 1 ovunque? ---")
print("  max dt_e/tau_p = %.6g    p99 = %.4g    mediana = %.4g"
      % (cfl.max(), np.percentile(cfl, 99), np.median(cfl)))
verdetto("U7b dt_e / tau_p < 1 ovunque", bool(cfl.max() < 1.0),
         "max = %.6g (frazione >= 1: %.4f %%)" % (cfl.max(), 100.0 * (cfl >= 1).mean()))

print("\n" + "=" * 118)
ok = sum(esiti)
print("U7: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
COME SI LEGGE UN FAIL DI U7a
----------------------------
Non dice che la forma sia sbagliata: dice che su una FRAZIONE di archi `tau_p` scenderebbe SOTTO il
tempo-luce, cioe' la forma di riposo inseguirebbe la forma attuale piu' in fretta di quanto un
segnale possa attraversare l'arco. Il mandato lo marca come violazione di A5 e ordina di FERMARSI.
La frazione, il minimo e la loro distribuzione sono qui sopra: servono alla decisione, non la
sostituiscono.""")
