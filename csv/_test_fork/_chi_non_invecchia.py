# -*- coding: utf-8 -*-
"""CHI NON INVECCHIA -- le quattro misure del mandato, DAI .pkl GIA' ESISTENTI. **NESSUN RUN NUOVO.**

Progettazione in doc/TASK_HISTORY/2026-09-18_chi-non-invecchia.md (49c0c28). **NESSUNA CURA.**

⚠ GLI ISTANTI SI CITANO COL LORO `_db_step`, MAI COL NOME DEL FILE: il primo watcher li aveva
mislabellati (uno conteneva 840). Il nome non e' un dato, il `_db_step` dentro lo e'.

1 distribuzione di `eta` (p05/p25/MEDIANA/p75/p95/max) e LA FRAZIONE entro una tolleranza DICHIARATA
  dal valore di semina, a ogni istante.
2 SONO SEMPRE GLI STESSI? Jaccard degli indici fermi fra istanti consecutivi -- lo STESSO metodo di
  `Z44`. E CHI SONO: grado, raggio, indice.
3 IL FALSIFICATORE DELLA MITOSI: i nodi si APPENDONO in coda, quindi L'INDICE E' L'ORDINE DI NASCITA.
  indice < n(primo istante) => c'era gia'. Se i fermi fossero i neonati sarebbero OTTO, non meta'.
4 `r` DEI FERMI, ricavato da `eta(t2) - eta(t1)` diviso `DT*(t2-t1)`: e' la DEFINIZIONE (`eta += DT*r`),
  e non richiede che `r` sia salvato. Confronto col PAVIMENTO `1e-6/(1/sqrt(2)+1e-6) = 1.414212e-06`
  e con i nodi che hanno `f = 0` ESATTO (il confronto diretto con `Z44`).
ASCII PURO.
"""
import glob
import os
import pickle
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
D = os.path.join("csv", "_test_fork", "_g1200")
DT = 0.01
R_FLOOR = 1e-6 / (1.0 / np.sqrt(2.0) + 1e-6)

print("=" * 118)
print("CHI NON INVECCHIA -- dai .pkl del run continuo. NESSUN RUN NUOVO, NESSUNA CURA.")
print("=" * 118)
print("  r al PAVIMENTO di ritmo() : %.6e   ->  dt_n = DT*r_floor = %.6e" % (R_FLOOR, DT * R_FLOOR))

S = {}
for p in sorted(glob.glob(os.path.join(D, "stato_*.pkl"))):
    try:
        st = pickle.load(open(p, "rb"))
    except Exception as e:
        print("  ILLEGGIBILE %s (%s)" % (os.path.basename(p), e)); continue
    a = st["attrs"]; s = int(a.get("_db_step", -1))
    if s < 0:
        continue
    S[s] = a
    S[s]["__file"] = os.path.basename(p)
T = sorted(S)
print("\n  istanti disponibili (dal `_db_step`, non dal nome): %s" % T)
for s in T:
    print("    step %-6d n = %-6d  file %s" % (s, len(S[s]["pos"]), S[s]["__file"]))
if len(T) < 2:
    print("  SERVONO almeno due istanti."); sys.exit(1)
N0 = len(S[T[0]]["pos"])

# tolleranza DICHIARATA: il valore di semina piu' cio' che il PAVIMENTO accumula fino a quell'istante
SEM = float(np.median(np.asarray(S[T[0]]["eta"], float)[:N0]))
print("\n  valore di semina di `eta` (mediana al primo istante): %.8g" % SEM)
print("  TOLLERANZA DICHIARATA: `eta <= semina + 3 * DT*r_floor*step` -- cioe' TRE VOLTE cio' che il")
print("  pavimento accumulerebbe. Chi sta sotto NON ha accumulato piu' del pavimento: e' FERMO.")


def eta(s):
    n = len(S[s]["pos"])
    return np.asarray(S[s]["eta"], float)[:n], n


def fermi(s):
    e, n = eta(s)
    soglia = SEM + 3.0 * DT * R_FLOOR * s
    return np.where(e <= soglia)[0], e, n, soglia


# ------------------------------------------------------------------ 1
print("\n--- (1) LA DISTRIBUZIONE DI `eta`, e quanti sono ancora al valore di semina ---")
print("  %-7s %-7s %-11s %-11s %-12s %-11s %-11s %-11s | %-9s %-9s"
      % ("step", "n", "p05", "p25", "MEDIANA", "p75", "p95", "max", "n FERMI", "FRAZIONE"))
for s in T:
    idx, e, n, soglia = fermi(s)
    print("  %-7d %-7d %-11.8g %-11.8g %-12.8g %-11.8g %-11.8g %-11.8g | %-9d %-9.4f"
          % (s, n, np.percentile(e, 5), np.percentile(e, 25), np.median(e),
             np.percentile(e, 75), np.percentile(e, 95), e.max(), len(idx), len(idx) / n))
print("  (frazione ~0.5 che NON cala -> meta' del sistema e' ferma. Se cala -> e' una coda.)")

# ------------------------------------------------------------------ 3 (il falsificatore, PRIMA)
print("\n--- (3) ⚠ IL FALSIFICATORE DELLA MITOSI, applicato PRIMA di descrivere ---")
print("  %-7s %-9s %-13s %-15s %-15s"
      % ("step", "n", "nati dopo t0", "fermi NATI dopo", "fermi PRESENTI a t0"))
for s in T:
    idx, e, n, _ = fermi(s)
    nuovi = n - N0
    f_nuovi = int(np.sum(idx >= N0))
    print("  %-7d %-9d %-13d %-15d %-15d" % (s, n, nuovi, f_nuovi, len(idx) - f_nuovi))
print("  (se i fermi fossero i NEONATI, il loro numero sarebbe <= 'nati dopo t0'.)")

# ------------------------------------------------------------------ 2
print("\n--- (2) SONO SEMPRE GLI STESSI? (Jaccard, lo stesso metodo di `Z44`) ---")
for a_, b_ in zip(T[:-1], T[1:]):
    A = set(fermi(a_)[0].tolist()); B = set(fermi(b_)[0].tolist())
    u = len(A | B)
    print("  step %-6d -> %-6d : |A| %-6d |B| %-6d  intersezione %-6d  JACCARD %.4f  |B\\A| %d"
          % (a_, b_, len(A), len(B), len(A & B), (len(A & B) / u) if u else 0.0, len(B - A)))
A0 = set(fermi(T[0])[0].tolist()); AN = set(fermi(T[-1])[0].tolist())
print("  PRIMO (%d) contro ULTIMO (%d): intersezione %d su |primo| %d = %.4f"
      % (T[0], T[-1], len(A0 & AN), len(A0), len(A0 & AN) / max(len(A0), 1)))

print("\n  CHI SONO (all'ultimo istante): grado e raggio, fermi contro tutti")
s = T[-1]; idx, e, n, _ = fermi(s)
a = S[s]
ii = np.asarray(a.get("i", np.zeros(0, int))); jj = np.asarray(a.get("j", np.zeros(0, int)))
grado = np.zeros(n)
if ii.size:
    m = (ii < n) & (jj < n)
    grado = (np.bincount(ii[m], minlength=n) + np.bincount(jj[m], minlength=n)).astype(float)
R = np.linalg.norm(np.asarray(a["pos"])[:n, :2], axis=1)
mob = np.setdiff1d(np.arange(n), idx)
for eti, sel in (("FERMI", idx), ("mobili", mob)):
    if len(sel) == 0:
        continue
    print("    %-8s n %-6d | grado p25 %-7.4g mediana %-7.4g p75 %-7.4g | raggio p25 %-7.4g mediana %-7.4g p75 %-7.4g"
          % (eti, len(sel), np.percentile(grado[sel], 25), np.median(grado[sel]), np.percentile(grado[sel], 75),
             np.percentile(R[sel], 25), np.median(R[sel]), np.percentile(R[sel], 75)))

# ------------------------------------------------------------------ 4
print("\n--- (4) ⚠ `r` DEI FERMI, ricavato da `eta += DT*r`, contro il PAVIMENTO ---")
print("  %-18s %-13s %-13s %-13s | %-13s %-13s"
      % ("intervallo", "r FERMI med", "r FERMI p95", "r/r_floor", "r tutti med", "r tutti p95"))
for a_, b_ in zip(T[:-1], T[1:]):
    na = len(S[a_]["pos"]); nb = len(S[b_]["pos"]); m = min(na, nb)
    ea = np.asarray(S[a_]["eta"], float)[:m]; eb = np.asarray(S[b_]["eta"], float)[:m]
    rr = (eb - ea) / (DT * (b_ - a_))
    idx = fermi(b_)[0]; idx = idx[idx < m]
    if len(idx) < 5:
        continue
    print("  %-18s %-13.6e %-13.6e %-13.4f | %-13.6e %-13.6e"
          % ("%d -> %d" % (a_, b_), np.median(rr[idx]), np.percentile(rr[idx], 95),
             np.median(rr[idx]) / R_FLOOR, np.median(rr), np.percentile(rr, 95)))
print("  (r/r_floor ~ 1 -> i fermi sono AL PAVIMENTO ASSOLUTO di `ritmo()`, non 'lenti'.)")

print("\n  E QUANTI DI LORO HANNO `f = 0` ESATTO? (il confronto diretto con `Z44`)")
for s in T:
    a = S[s]; n = len(a["pos"])
    ps = a.get("psi_spin"); idx = fermi(s)[0]
    if ps is None:
        print("    step %-6d psi_spin ASSENTE nel .pkl" % s); continue
    ps = np.asarray(ps)[:n]
    z = np.where(np.sqrt(np.sum(np.abs(ps) ** 2, axis=1)) == 0.0)[0]
    print("    step %-6d  fermi %-6d   |psi_spin| = 0 ESATTO: %-6d   fermi CON psi_spin=0: %d"
          % (s, len(idx), len(z), len(set(idx.tolist()) & set(z.tolist()))))
print("""
  COME SI LEGGE -- le cinque letture erano fissate PRIMA (task history 49c0c28):
    frazione ~50 %, sempre gli stessi, n quasi costante -> META' DEL SISTEMA CONGELATA: Z9 va
                                                           RISCRITTA. Riporta e FERMATI.
    flusso che riparte            -> transitorio di nascita (ma con 8 nodi nuovi NON torna).
    mediana bassa ma frazione piccola -> CODA, non congelamento.
    nessuna regge                 -> si dice, senza inventare la quinta.
    ⚠ LA MIA: r dei fermi = PAVIMENTO -> la causa non e' `eta` ne' `ramp`, e' IL BOTTLENECK di
      `ritmo()`, e la voce giusta e' Z43, non Z9. L'ordine dei due mandati si inverte.""")
print("\n" + "=" * 118)
