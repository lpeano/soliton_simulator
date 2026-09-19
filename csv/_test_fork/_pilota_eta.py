# -*- coding: utf-8 -*-
"""PILOTA del run a 6000: il batch MATURA, o `r` e' al pavimento come dice `Z46`?

Task history con le tre letture, committato PRIMA: doc/TASK_HISTORY/2026-09-19_run-6000.md (91cd9dc)

LA MISURA CHE DECIDE, ed e' esatta con UN SOLO snapshot:
  per i nodi presenti da t = 0 (indice < n0), `eta(T)/T` E' la media di `DT*r` su tutto il run.
  Non servono due istanti. Si separa per `r` letto da `_r_corrente` -- MAI una mediana sulle due
  popolazioni insieme (A3c).

  :3236  self.eta += dt_n     :3038  dt_n = DT * r     :2649  ramp = min(1, eta/TAU_A)
  ->  passi(ramp = 1) = TAU_A / (DT * r) = 5000 / r

IN TESTA: `--tau-luce` ha il SIGILLO COMPLESSIVO ancora FAIL (resta `T3`), ramo NON CERTIFICATO.
UN SEME (900, lo stesso di `Z46`). NESSUN VERDETTO DI FISICA.
ASCII PURO.
"""
import os
import pickle
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
DT = 0.01          # dal simulatore :189
TAU_A = 50.0       # ramo REGIME = "deterministico" (:117-121)
R_FLOOR = 1e-6 / (1.0 / np.sqrt(2.0) + 1e-6)
FERMO = 2.0        # r/r_floor < 2 -> FERMO. Z46 misura 1.0000 esatto sui fermi.
PKL = os.path.join("csv", "_test_fork", "_pilota6000", "pilota.pkl")
N0 = 1196          # nodi al passo 0, LETTO dal CSV del pilota (colonna n_tot, riga passo=0)

print("=" * 116)
print("PILOTA DEL RUN A 6000 -- il batch matura, o `r` e' al pavimento? (seme 900, come Z46)")
print("=" * 116)
print("  IN TESTA: --tau-luce ha il SIGILLO COMPLESSIVO ancora FAIL (resta T3): ramo NON CERTIFICATO.")
print("            UN SEME. NESSUN VERDETTO DI FISICA.")

s = pickle.load(open(PKL, "rb"))
a = s["attrs"]
T = int(a.get("_db_step", -1))
n = len(a["pos"])
eta = np.asarray(a["eta"], float)[:n]
rc = a.get("_r_corrente", None)
print("")
print("  .pkl       : %s   %.2f MB" % (PKL, os.path.getsize(PKL) / 1048576.0))
print("  blob nel DB: %s   passo = %d   n = %d   n0 = %d (dal CSV)" % (str(s.get("blob"))[:8], T, n, N0))
if rc is None:
    print("  `_r_corrente` ASSENTE -> NON stimo r da eta (sarebbe CIRCOLARE: eta cresce PER r). STOP.")
    raise SystemExit(1)
r = np.asarray(rc, float)
m = min(n, r.size)
print("  len(_r_corrente) = %d (scritta prima dell'ultima mitosi: i %d in eccesso sono ESCLUSI)"
      % (r.size, n - m))

# ------------------------------------------------------------------ la popolazione di r
print("")
print("--- (1) `r` NEL BATCH: e' al pavimento? (r_floor = %.6e) ---" % R_FLOOR)
fer = (r[:m] / R_FLOOR) < FERMO
mob = ~fer
print("    FERMI  %6d nodi (%5.1f %%)   r mediana %.6e   r/r_floor %.4f"
      % (fer.sum(), 100.0 * fer.mean(), float(np.median(r[:m][fer])) if fer.any() else np.nan,
         float(np.median(r[:m][fer])) / R_FLOOR if fer.any() else np.nan))
print("    MOBILI %6d nodi (%5.1f %%)   r mediana %.6e   r/r_floor %.4g"
      % (mob.sum(), 100.0 * mob.mean(), float(np.median(r[:m][mob])) if mob.any() else np.nan,
         float(np.median(r[:m][mob])) / R_FLOOR if mob.any() else np.nan))
print("    (Z46, STESSO seme e STESSA scena, a 120-1200 passi: 92.7 %% FERMI con r/r_floor = 1.0000)")

# ------------------------------------------------------------------ il tasso, per gruppo
print("")
print("--- (2) IL TASSO d(eta)/d(passo), FERMI e MOBILI SEPARATI (A3c: mai una mediana comune) ---")
ori = np.zeros(m, bool)
ori[:min(N0, m)] = True          # i nodi presenti da t = 0: per loro eta/T E' la media di DT*r
print("    %-22s %-8s %-15s %-15s %-15s" % ("gruppo", "nodi", "eta MEDIANA", "d(eta)/d(passo)", "passi a ramp=1"))
for nome, sel in (("ORIGINALI FERMI", ori & fer), ("ORIGINALI MOBILI", ori & mob),
                  ("NATI DOPO", ~ori)):
    if sel.sum() < 1:
        print("    %-22s %-8d  (nessuno)" % (nome, sel.sum()))
        continue
    e = eta[:m][sel]
    tasso = float(np.median(e)) / float(T)
    att = (TAU_A / tasso) if tasso > 0 else float("inf")
    print("    %-22s %-8d %-15.6e %-15.6e %-15.4g"
          % (nome, sel.sum(), float(np.median(e)), tasso, att))
print("    (per gli ORIGINALI eta/T e' ESATTAMENTE la media di DT*r sul run: nessuna stima.)")
print("    CONTROLLO: DT * r mediano dei MOBILI = %.6e   contro il tasso misurato qui sopra."
      % (DT * float(np.median(r[:m][mob])) if mob.any() else np.nan))

# ------------------------------------------------------------------ ramp
print("")
print("--- (3) `ramp = min(1, eta/%.0f)` ADESSO, e dove arriva a 6000 ---" % TAU_A)
ramp = np.minimum(1.0, eta[:m] / TAU_A)
print("    %-22s %-8s %-12s %-12s %-10s %-10s %-14s"
      % ("gruppo", "nodi", "ramp MED", "ramp p95", "fr>0.5", "fr>0.9", "ramp a 6000"))
for nome, sel in (("ORIGINALI FERMI", ori & fer), ("ORIGINALI MOBILI", ori & mob),
                  ("NATI DOPO", ~ori), ("TUTTI", np.ones(m, bool))):
    if sel.sum() < 1:
        continue
    rp = ramp[sel]
    e = eta[:m][sel]
    proj = min(1.0, float(np.median(e)) / float(T) * 6000.0 / TAU_A)
    print("    %-22s %-8d %-12.6g %-12.6g %-10.4f %-10.4f %-14.4g"
          % (nome, sel.sum(), float(np.median(rp)), float(np.percentile(rp, 95)),
             float(np.mean(rp > 0.5)), float(np.mean(rp > 0.9)), proj))
print("    (`ramp a 6000` e' una PROIEZIONE LINEARE del tasso misurato: vale se il tasso resta")
print("     costante, e il tasso dipende da `r`, che NON e' garantito costante. E' una stima.)")

# ------------------------------------------------------------------ Z9-b
print("")
print("--- (4) IL CRITERIO `Z9-b`: median(ramp[i]*ramp[j]) sugli archi INTERNI alla coorte ORIGINALE ---")
ii = np.asarray(a["i"], int)
jj = np.asarray(a["j"], int)
msk = (ii < m) & (jj < m)
I2, J2 = ii[msk], jj[msk]
b_tot = ramp[I2] * ramp[J2]
oo = (I2 < N0) & (J2 < N0)
print("    archi totali %d   interni alla coorte originale %d (%.2f %%)"
      % (b_tot.size, int(oo.sum()), 100.0 * oo.sum() / max(b_tot.size, 1)))
if oo.sum() >= 5:
    b_ori = b_tot[oo]
    print("    median(base/base_maturo) SU QUELLI : %.8f     <- DEVE valere 1 per chiudere Z9"
          % float(np.median(b_ori)))
    print("    p05 %.8f   p95 %.8f   p95/p05 %.4f" %
          (float(np.percentile(b_ori, 5)), float(np.percentile(b_ori, 95)),
           float(np.percentile(b_ori, 95)) / max(float(np.percentile(b_ori, 5)), 1e-300)))
print("    median su TUTTI gli archi          : %.8f" % float(np.median(b_tot)))
print("    frazione di archi MATURI (entrambi gli estremi eta >= TAU_A): %.6f"
      % float(np.mean((eta[I2] >= TAU_A) & (eta[J2] >= TAU_A))))

# ------------------------------------------------------------------ il costo
print("")
print("--- (5) IL COSTO DEL RUN VERO ---")
mb = os.path.getsize(PKL) / 1048576.0
print("    un .pkl pesa %.2f MB  ->  30 snapshot = %.2f GB   (liberi sul disco: 20 GB, 96 %% pieno)"
      % (mb, 30 * mb / 1024.0))
print("    durata MISURATA sul pilota: 371 s per 300 passi = 123.7 s/100 passi")
print("    -> 6000 passi = %.0f s = %.2f h   SE il costo per passo resta costante." % (60.0 * 123.7, 60.0 * 123.7 / 3600.0))
print("    (`Z46` dice che nel batch `n` e' PIATTO: se regge, l'estrapolazione tiene. Se `n` cresce,")
print("     il costo cresce con lui ed e' un LIMITE INFERIORE.)")
print("=" * 116)
