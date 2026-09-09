#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sigilli --kuramoto-su2 (§46). Cartella temp, NON committare i .pkl.
  1) OFF byte-identico: db_old (pre-kuramoto) vs db_offd (NEW, flag OFF) -> max|A-B|=0 su ogni array fisico.
  2) unitarieta': |psi_spinor|=1 e len==n su db_ond (NEW, flag ON).
  prelim) ON vs OFF su spin_overlap_arco / segno_arco_coer / verso_arco_coer (media dal 25%+).
Sigillo 3 (primo ordine) = analitico; sigillo 4 (conv-dt) = nella campagna covariante."""
import pickle, sys, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

def _attrs(path):
    return pickle.load(open(path, 'rb'))['attrs']

def sigillo1(pold, poff):
    a = _attrs(pold); b = _attrs(poff)
    ka = set(a); kb = set(b)
    solo_a = sorted(ka - kb); solo_b = sorted(kb - ka)
    peggio = 0.0; peggio_k = None; nko = 0; ncheck = 0
    for k in sorted(ka & kb):
        va, vb = a[k], b[k]
        if isinstance(va, np.ndarray) and isinstance(vb, np.ndarray):
            if va.shape != vb.shape:
                print(f"   [SHAPE DIVERSA] {k}: {va.shape} vs {vb.shape}"); nko += 1; continue
            if va.size == 0:
                continue
            d = float(np.nanmax(np.abs(va - vb)))   # np.abs gestisce reali E complessi (modulo)
            ncheck += 1
            if d > peggio:
                peggio = d; peggio_k = k
            if d > 0:
                nko += 1
        else:
            if va != vb:
                print(f"   [SCALARE DIVERSO] {k}: {va} vs {vb}"); nko += 1
    print(f"--- SIGILLO 1 (OFF byte-identico: OLD vs NEW-off) ---")
    print(f"   array confrontati: {ncheck}; con differenza: {nko}")
    print(f"   MAX|A-B| = {peggio:.3e}  (peggior chiave: {peggio_k})")
    if solo_a: print(f"   chiavi solo in OLD: {solo_a}")
    if solo_b: print(f"   chiavi solo in NEW-off: {solo_b}")
    ok = (peggio == 0.0 and nko == 0)
    print(f"   ESITO: {'PASSATO (byte-identico)' if ok else 'FALLITO'}")
    return ok

def sigillo2(pon):
    a = _attrs(pon)
    psi = a.get('_psi_spinor')
    # n e' una property (non in __dict__): lo deduco da un array di stato per-nodo.
    _ref = a.get('phi', a.get('pos'))
    n = int(len(_ref)) if _ref is not None else -1
    print(f"--- SIGILLO 2 (unitarieta' NEW-on) ---")
    if psi is None:
        print("   _psi_spinor ASSENTE -> FALLITO"); return False
    norms = np.linalg.norm(np.asarray(psi), axis=1)
    dev = float(np.max(np.abs(norms - 1.0)))
    lenok = (len(psi) == n)
    print(f"   |psi_spinor|: max|1-|.|| = {dev:.3e}; len(psi)={len(psi)} n={n} (len==n: {lenok})")
    ok = (dev < 1e-9 and lenok)
    print(f"   ESITO: {'PASSATO' if ok else 'FALLITO'}")
    return ok

def _tail_mean(path, col, frac=0.25):
    import csv
    rows = []
    with open(path, newline='') as f:
        lines = [ln for ln in f if not ln.lstrip().startswith('#')]   # salta # RUN_PARAMS
        r = csv.DictReader(lines)
        for row in r:
            if col in row and row[col] not in ('', None):
                try: rows.append(float(row[col]))
                except ValueError: pass
    if not rows: return None
    k = int(len(rows) * frac)
    seg = rows[k:] if len(rows) > k else rows
    return float(np.mean(seg))

def prelim(pon_csv, poff_csv):
    print(f"--- PRELIM (media dal 25%+, ON vs OFF) ---")
    cols = ['spin_overlap_arco', 'segno_arco_coer', 'verso_arco_coer', 'segno_ov_absmedia', 'spin_axis_R']
    for c in cols:
        on = _tail_mean(pon_csv, c); off = _tail_mean(poff_csv, c)
        if on is None or off is None:
            print(f"   {c:20s}: colonna assente (ON={on} OFF={off})"); continue
        print(f"   {c:20s}: ON={on:+.6f}  OFF={off:+.6f}  (ON-OFF={on-off:+.6f})")

if __name__ == '__main__':
    d = HERE
    s1 = sigillo1(f"{d}/db_old.pkl", f"{d}/db_offd.pkl")
    print()
    s2 = sigillo2(f"{d}/db_ond.pkl")
    print()
    prelim(f"{d}/on.csv", f"{d}/off.csv")
    print()
    print(f"=== SIGILLI 1+2: {'ENTRAMBI PASSATI' if (s1 and s2) else 'ATTENZIONE (vedi sopra)'} ===")
    sys.exit(0 if (s1 and s2) else 1)
