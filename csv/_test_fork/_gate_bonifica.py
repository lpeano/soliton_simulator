# -*- coding: utf-8 -*-
"""GATE della BONIFICA -- A, B, C, D. Dai .pkl gia' committati. NESSUN RUN DI MISURA.

Questi NON sono osservabili di fisica: sono verifiche di LICEITA' delle correzioni proposte.
Si chiede a una grandezza se ha STRUTTURA, cioe' se e' libera di variare, prima di costruirci
sopra una legge. E' il presidio P4 applicato prima del cablaggio invece che dopo.

ASCII PURO (tre script gia' morti su cp1252).
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import glob
import os
import pickle

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = sorted(glob.glob(os.path.join(HERE, "_vuoto_s2ON_s?.pkl")))


def quadro(nome, x, soglia_uno=True):
    """La domanda e' sempre la stessa: e' concentrata su 1, o ha struttura?"""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if not len(x):
        print("  %-32s (vuoto)" % nome)
        return None
    q = np.percentile(x, [5, 25, 50, 75, 95])
    r = q[4] / q[0] if q[0] > 0 else float("inf")
    print("  %-32s med %10.4g | p05 %9.3g p95 %9.3g | p95/p05 %11.4g | IQR/med %8.3g | >1: %5.1f%%"
          % (nome, q[2], q[0], q[4], r, (q[3] - q[1]) / max(abs(q[2]), 1e-300),
             100.0 * (x > 1).mean()))
    return q


print("=" * 128)
print("GATE DELLA BONIFICA -- dati: %d run committati (blob a44adc31, 500 passi, 4 semi)" % len(FILES))
print("  ATTENZIONE: i .pkl sono del blob PRECEDENTE (a44adc31), non di 827d3bf8. La campagna")
print("  csrel e' stata fermata prima della scrittura del DB. Per una domanda STRUTTURALE")
print("  ('questo rapporto ha una distribuzione, o vale 1 per costruzione?') e' adeguato, ma")
print("  va DICHIARATO: il cs_floor relazionale cambia i valori, non la forma della domanda.")
print("=" * 128)

Aall, Dall, F_oggi, F_peq = [], [], [], []
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    psi = np.asarray(A["psi"])
    I = np.abs(psi) ** 2
    n = len(I)
    i = np.asarray(A["i"], int)
    j = np.asarray(A["j"], int)
    peq = np.asarray(A["peq"], float)
    m = (i < n) & (j < n) & np.isfinite(peq)
    i, j, peq = i[m], j[m], peq[m]

    # ---- GATE B: la proiezione ARCO -> NODO. peq e' per ARCO, l'inerzia per NODO.
    # Proiezione = MEDIA degli archi incidenti (non pesata): e' la stessa forma che il codice usa
    # gia' per den_w (:3140-3141), quindi non introduce una convenzione nuova.
    som = np.bincount(i, peq, minlength=n) + np.bincount(j, peq, minlength=n)
    cnt = np.bincount(i, minlength=n) + np.bincount(j, minlength=n)
    peq_nodo = som / np.maximum(cnt, 1)
    vivo = cnt > 0
    Aall.append((I[vivo] / np.maximum(peq_nodo[vivo], 1e-300)))

    # ---- GATE D: rho_arco / peq. ENTRAMBI per arco: nessuna proiezione.
    rho_arco = 0.5 * (I[i] + I[j])
    Dall.append(rho_arco / np.maximum(peq, 1e-300))

    # la frazione di archi col fattore di elasticita' ESATTAMENTE 1, oggi e con peq
    rho_med = max(float(np.median(I)), 1e-9)
    F_oggi.append(np.maximum(rho_arco / rho_med - 1.0, 0.0) == 0.0)
    F_peq.append(np.maximum(rho_arco / np.maximum(peq, 1e-30) - 1.0, 0.0) == 0.0)

print("\n### GATE A -- `rho_sorgente / peq_nodo` ha STRUTTURA?  (per la correzione (1), inerzia)")
print("-" * 128)
xa = np.concatenate(Aall)
quadro("I / peq_nodo   (aggregato)", xa)
print("\n  RIFERIMENTI, per sapere che faccia ha un SI' e che faccia ha un NO:")
print("  " + "-" * 60)
ref = []
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    I = np.abs(np.asarray(A["psi"])) ** 2
    ref.append(I / max(float(np.mean(I)), 1e-300))
quadro("[SI' noto] I / Lam (media)", np.concatenate(ref))
ref2 = []
for f in FILES:
    A = pickle.load(open(f, "rb"))["attrs"]
    I = np.abs(np.asarray(A["psi"])) ** 2
    ref2.append(I / max(float(np.median(I)), 1e-300))
quadro("[NO noto ] I / median(I)", np.concatenate(ref2))

print("\n### GATE D -- `rho_arco / peq` ha STRUTTURA?  (per la correzione (6), elasticita')")
print("-" * 128)
xd = np.concatenate(Dall)
quadro("rho_arco / peq   (aggregato)", xd)
fo = np.concatenate(F_oggi)
fp = np.concatenate(F_peq)
print()
print("  frazione di archi con fattore_elasticita = 1.0 ESATTO:")
print("      OGGI  (rho_arco / median(I_nodi)) : %6.2f %%" % (100.0 * fo.mean()))
print("      CON   peq                          : %6.2f %%" % (100.0 * fp.mean()))
print("      -> variazione: %.2f punti percentuali" % (100.0 * (fp.mean() - fo.mean())))

print("\n### GATE C -- quanto scatta `maximum(r, 0.01)`?  (per la correzione (5))")
print("-" * 128)
import csv
vals = []
for f in sorted(glob.glob(os.path.join(HERE, "_vuoto_s2ON_s?.vuoto.csv"))):
    r = list(csv.DictReader(open(f, newline="")))
    if r:
        k = r[-1]
        vals.append((os.path.basename(f)[:20], float(k.get("r_min", "nan")),
                     float(k.get("r_p05", "nan")), float(k.get("r_mediana", "nan"))))
for nm, rmin, rp05, rmed in vals:
    print("  %-22s r_min %10.4g   r_p05 %10.4g   r_mediana %8.4f   r_min < 0.01? %s"
          % (nm, rmin, rp05, rmed, "SI'" if rmin < 0.01 else "NO"))
print("=" * 128)
