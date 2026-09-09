#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confronto covariante di un braccio vs baseline a N APPAIATO (kuramoto-su2 + sblocchi olonomia).
Uso: python _confronta_braccio.py <braccio.csv> <baseline.csv> [etichetta]
DUE ASSI (indicazione guardiano):
  SBILANCIAMENTO/olonomia netta: berry_spin_media (firmata), berry_spin_media_assoluta, olonomia_fase_media_assoluta
  ORDINE LOCALE:                 spin_overlap_arco (SU(2) pieno, 0.5=scorrelato), segno_arco_coer, verso_arco_coer
Sbilanciare != ordinare: leggere entrambi."""
import csv, sys, os
import numpy as np

def load(path):
    lines = [l for l in open(path) if not l.lstrip().startswith('#')]
    rows = list(csv.DictReader(lines))
    def col(name):
        return np.array([float(x[name]) for x in rows if x.get(name) not in ('', None)]) if rows and name in rows[0] else None
    return col

ASSI = {
 'SBILANCIAMENTO (olonomia netta)': ['berry_spin_media', 'berry_spin_media_assoluta', 'olonomia_fase_media_assoluta'],
 'ORDINE LOCALE (coerenza vicini)': ['spin_overlap_arco', 'segno_arco_coer', 'verso_arco_coer'],
 'contesto': ['segno_ov_absmedia', 'spin_axis_R'],
}

def interp_N(y, N, grid):
    o = np.argsort(N); return np.interp(grid, N[o], y[o])

def main(brpath, bapath, lab):
    br = load(brpath); ba = load(bapath)
    Nb, Na = br('n'), ba('n')
    lo = max(Nb.min(), Na.min()); hi = min(Nb.max(), Na.max())
    grid = np.linspace(lo, hi, 200); late = grid >= (lo + 2*(hi-lo)/3)
    print(f"=== BRACCIO {lab}: {os.path.basename(brpath)} vs baseline {os.path.basename(bapath)} ===")
    print(f"N braccio {Nb[0]:.0f}->{Nb[-1]:.0f} | baseline {Na[0]:.0f}->{Na[-1]:.0f} | N comune [{lo:.0f},{hi:.0f}]  (late = ultimo terzo)")
    for asse, cols in ASSI.items():
        print(f"\n-- {asse} --")
        print(f"  {'colonna':30s}{'BRACCIO':>12s}{'BASELINE':>12s}{'delta':>12s}{'sd':>10s}  esito")
        for c in cols:
            yb, ya = br(c), ba(c)
            if yb is None or ya is None:
                print(f"  {c:30s}{'ASSENTE':>12s}"); continue
            yb_i = interp_N(yb, Nb, grid); ya_i = interp_N(ya, Na, grid)
            d = yb_i - ya_i; m = float(np.mean(d[late])); sd = float(np.std(d[late]))
            tag = 'STACCA' if abs(m) > 2*sd else '~uguale'
            print(f"  {c:30s}{np.mean(yb_i[late]):>12.5f}{np.mean(ya_i[late]):>12.5f}{m:>+12.5f}{sd:>10.5f}  {tag}")
    print("\nNB: 800p=formazione,1 seme -> pilota. spin_overlap 0.5=scorrelato. Sbilanciare(berry) != ordinare(overlap/segno).")

if __name__ == '__main__':
    br = sys.argv[1] if len(sys.argv) > 1 else 'csv/deparam_bracci/A.csv'
    ba = sys.argv[2] if len(sys.argv) > 2 else 'csv/deparam_pilota_k2/on.csv'
    lab = sys.argv[3] if len(sys.argv) > 3 else 'A'
    main(br, ba, lab)
