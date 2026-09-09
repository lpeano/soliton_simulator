#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confronto covariante ON vs OFF del pilota --kuramoto-su2, a N APPAIATO (non a passo).
Il sistema si espande (N cresce): confrontare allo stesso step misura l'espansione, non la fisica.
Interpolo gli order parameter di ON e OFF sulla griglia di N COMUNE e leggo ON-OFF.
  spin_overlap_arco = SU(2) PIENA (primario). segno_arco_coer / verso_arco_coer = foglio / verso.
GO se ON si stacca da OFF oltre il rumore su spin_overlap/segno; NO-GO se ON~OFF (kuramoto inerte)."""
import csv, os
import numpy as np

def load(path):
    lines = [l for l in open(path) if not l.lstrip().startswith('#')]
    rows = list(csv.DictReader(lines))
    def col(name):
        return np.array([float(x[name]) for x in rows if x.get(name) not in ('', None)])
    return col

ORD = ['spin_overlap_arco', 'segno_arco_coer', 'verso_arco_coer', 'segno_ov_absmedia', 'spin_axis_R']
on = load('csv/deparam_pilota_k2/on.csv')
off = load('csv/deparam_pilota_k2/off.csv')
Non, Noff = on('n'), off('n')
lo = max(Non.min(), Noff.min()); hi = min(Non.max(), Noff.max())
print(f"=== CONFRONTO COVARIANTE ON vs OFF (N appaiato) ===")
print(f"N ON:  {Non[0]:.0f}->{Non[-1]:.0f}   N OFF: {Noff[0]:.0f}->{Noff[-1]:.0f}")
print(f"finestra N COMUNE: [{lo:.0f}, {hi:.0f}]")

def interp_on_N(colvals, Nvals, grid):
    # N e' monotono crescente (a meno di rumore mitosi): ordino per N e interpolo
    o = np.argsort(Nvals)
    return np.interp(grid, Nvals[o], colvals[o])

grid = np.linspace(lo, hi, 200)
# separo la finestra "tardiva" (ultimo terzo di N comune) = dopo la formazione grezza
late = grid >= (lo + 2*(hi-lo)/3)
print(f"\n{'order parameter':22s}{'ON(late)':>11s}{'OFF(late)':>11s}{'ON-OFF':>11s}{'sd(diff)':>11s}  esito")
for c in ORD:
    yon = interp_on_N(on(c), Non, grid)
    yoff = interp_on_N(off(c), Noff, grid)
    diff = yon - yoff
    dlate = diff[late]
    m = float(np.mean(dlate)); sd = float(np.std(dlate))
    # significativo se |media| > 2*sd/sqrt(neff) usando sd della differenza sulla finestra
    sig = abs(m) > 2*sd
    tag = ("STACCA" if sig else "~uguale")
    print(f"{c:22s}{np.mean(yon[late]):>11.5f}{np.mean(yoff[late]):>11.5f}{m:>+11.5f}{sd:>11.5f}  {tag}")
print("\nNB: 800 passi=formazione, 1 seme -> PILOTA (accenno), non verdetto. spin_overlap 0.5=scorrelato.")
