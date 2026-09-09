#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valutazione ON del pilota --kuramoto-su2 (letto covariante: N cresce, leggo a scala/pop appaiata).
Non un verdetto (800 passi=formazione, 1 seme): cerca un ACCENNO che gli order parameter si muovano.
  spin_overlap_arco  = <|<psi_i|psi_j>|^2> (SU(2) PIENA): 0.5=scorrelato, ->1 coerente. PRIMARIO.
  segno_arco_coer    = <sign_i*sign_j> (foglio doppia-copertura): 0=frustrato, ->+/-1 ordinato.
  verso_arco_coer    = <nb_i.nb_j> (verso di Bloch).
Se verso E segno salgono INSIEME -> candidato spin 1/2 (olonomia). Se verso sale ma segno no -> olonomia persa."""
import csv, sys, os
import numpy as np

def load(path):
    lines = [l for l in open(path) if not l.lstrip().startswith('#')]
    r = csv.DictReader(lines)
    rows = list(r)
    def col(name):
        return np.array([float(x[name]) for x in rows if x.get(name) not in ('', None)])
    return rows, col

def stats_window(col, step, lo, hi):
    m = (step >= lo) & (step < hi)
    return float(np.mean(col[m])) if m.any() else float('nan')

def main(path):
    rows, col = load(path)
    step = col('step'); N = col('n')
    ORD = ['spin_overlap_arco', 'segno_arco_coer', 'verso_arco_coer', 'segno_ov_absmedia', 'spin_axis_R']
    print(f"=== VALUTAZIONE ON  ({os.path.basename(path)}, {len(rows)} righe) ===")
    print(f"N (nodi): inizio={N[0]:.0f}  fine={N[-1]:.0f}  (espansione x{N[-1]/max(N[0],1):.2f})")
    # tempo proprio cumulativo (covariante): tau_cum = sum tau_mean*DT ; DT ~ diff(step) (qui costante)
    try:
        tau = col('tau_mean'); dstep = np.diff(step, prepend=step[0])
        tau_cum = np.cumsum(tau * np.maximum(dstep, 0))
        print(f"tau_cum (tempo proprio): fine={tau_cum[-1]:.3f}  (vs step {step[-1]:.0f})")
    except Exception:
        tau_cum = None
    smax = step[-1]
    wins = [('early [0,1/3)', 0, smax/3), ('mid   [1/3,2/3)', smax/3, 2*smax/3), ('late  [2/3,end]', 2*smax/3, smax+1)]
    print("\n-- evoluzione per finestra temporale (media) --")
    hdr = "  finestra           N     " + "  ".join(f"{c[:16]:>16}" for c in ORD)
    print(hdr)
    for name, lo, hi in wins:
        nwin = stats_window(N, step, lo, hi)
        vals = "  ".join(f"{stats_window(col(c), step, lo, hi):>16.5f}" for c in ORD)
        print(f"  {name:16s} {nwin:6.0f}  {vals}")
    # trend 1a vs 2a meta' (letto a popolazione crescente: e' l'accenno grezzo)
    print("\n-- trend 1a vs 2a meta' (2a - 1a) --")
    half = smax/2
    for c in ORD:
        v = col(c)
        a = stats_window(v, step, 0, half); b = stats_window(v, step, half, smax+1)
        sd = float(np.std(v[step >= half])) if (step >= half).any() else float('nan')
        freccia = "UP" if (b-a) > 2*sd/np.sqrt(max((step>=half).sum(),1)) else ("dn" if (a-b) > 2*sd/np.sqrt(max((step>=half).sum(),1)) else "==")
        print(f"  {c:20s}: 1a={a:+.5f}  2a={b:+.5f}  delta={b-a:+.5f}  sd(2a)={sd:.5f}  [{freccia}]")
    # accoppiamento segno<->verso: si muovono insieme? (correlazione temporale nella 2a meta')
    try:
        sg = col('segno_arco_coer'); vs = col('verso_arco_coer'); sp = col('spin_overlap_arco')
        m = step >= half
        if m.sum() > 3:
            def corr(a, b):
                a=a[m]-a[m].mean(); b=b[m]-b[m].mean()
                d=np.sqrt((a*a).sum()*(b*b).sum())
                return float((a*b).sum()/d) if d>0 else float('nan')
            print("\n-- accoppiamento (corr temporale 2a meta') --")
            print(f"  corr(segno, verso)   = {corr(sg, vs):+.3f}  (>0 = si muovono insieme -> un motore)")
            print(f"  corr(segno, overlap) = {corr(sg, sp):+.3f}")
            print(f"  corr(verso, overlap) = {corr(vs, sp):+.3f}")
    except Exception as e:
        print("  [accoppiamento non calcolabile]", e)

if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else 'csv/deparam_pilota_k2/on.csv'
    main(p)
