# -*- coding: utf-8 -*-
"""DIAGNOSI: da dove viene il `peq` DEGENERE? NaN di `_allaccia`, o decadimento dinamico?

Il mandato assume che la causa sia il `np.full(len(dd), np.nan)` di `_allaccia`. Ma `_allaccia` e'
chiamato SOLO da `semina()` <- `nuova_massa()`, cioe' alla COSTRUZIONE DELLA SCENA. In un run batch
gli archi nuovi nascono da `mitosi()` (che EREDITA peq) e dallo Schwinger (che usa `pmed`).
Quindi la premessa va VERIFICATA prima di cablare, non dopo.

Osserva soltanto: wrapper su `step` che ispeziona `self.peq`. Nessuna legge toccata.
ASCII PURO.
"""
import os
import sys

import numpy as np

ROOT = r"C:\Users\lpeano\soliton_simulator"
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

S.CS_DINAMICO = True
S.CAMPO_SPINORIALE = True
S.SPINORE_VIVO = True
S.CHI_CORE = True
S.FORK_SU2 = True
S.FORK_SU2_MEM = True

r = S.Rete(seed=11)
r.nuova_massa(120, raggio=2.0, centro=(-4.0, 0, 0), fase=0.0)
r.nuova_massa(120, raggio=2.0, centro=(4.0, 0, 0), fase=0.0)
r.nuova_massa(120, raggio=2.0, centro=(0.0, 4.0, 0), fase=0.0)

print("=" * 112)
print("DIAGNOSI DEL `peq` DEGENERE -- NaN o decadimento dinamico?")
print("=" * 112)
print("  SUBITO DOPO LA COSTRUZIONE DELLA SCENA (cioe' dopo _allaccia, prima di ogni step):")
peq = np.asarray(r.peq, float)
print("    archi %d | NaN %d (%.2f %%) | <=1e-30 finiti %d | psi lungo %d, n = %d"
      % (len(peq), int(np.isnan(peq).sum()), 100.0 * np.isnan(peq).mean(),
         int(((peq <= 1e-30) & np.isfinite(peq)).sum()), len(r.psi), r.n))
print("    -> se qui i NaN sono TUTTI gli archi, `_allaccia` e' davvero la sorgente iniziale.")

print("\n  EVOLUZIONE (dopo ogni step, PRIMA che la calibrazione del passo dopo intervenga):")
print("  %-6s %-9s %-14s %-16s %-14s %-10s" %
      ("passo", "archi", "NaN", "<=1e-30 finiti", "degeneri tot", "nuovi/passo"))
prec = 0
for k in range(1, 31):
    r.step()
    r.mitosi()
    peq = np.asarray(r.peq, float)
    nan = int(np.isnan(peq).sum())
    zero = int(((peq <= 1e-30) & np.isfinite(peq)).sum())
    deg = nan + zero
    if k <= 6 or k % 6 == 0:
        print("  %-6d %-9d %-14d %-16d %-14d %-10d"
              % (k, len(peq), nan, zero, deg, len(peq) - prec))
    prec = len(peq)

peq = np.asarray(r.peq, float)
nan = int(np.isnan(peq).sum())
zero = int(((peq <= 1e-30) & np.isfinite(peq)).sum())
print("\n" + "=" * 112)
print("VERDETTO")
print("  NaN residui            : %d  (%.4f %%)" % (nan, 100.0 * nan / max(len(peq), 1)))
print("  finiti ma <= 1e-30     : %d  (%.4f %%)" % (zero, 100.0 * zero / max(len(peq), 1)))
if zero > nan:
    print("""
  -> LA CAUSA DOMINANTE NON E' IL NaN: e' `peq` che DECADE a zero per DINAMICA.
     `peq` rilassa verso `rho` (:3154). Dove `rho` e' ~0 -- il vuoto -- `peq` lo segue fino a
     sottozero-macchina. La correzione (1) del mandato inizializzerebbe `peq` a `0.5*(I[a]+I[b])`,
     che in quelle regioni vale GIA' ~0: NON cambierebbe nulla.""")
elif nan > 0:
    print("""
  -> I NaN esistono e sopravvivono: la correzione (1) e' pertinente.""")
else:
    print("""
  -> NESSUN NaN e NESSUNO ZERO in questo scenario: la sorgente del degenere sta altrove.""")
print("\n  valori piu' piccoli di peq (finiti): %s"
      % np.sort(peq[np.isfinite(peq) & (peq > 0)])[:5])
print("  peq esattamente 0: %d" % int((peq == 0).sum()))
