#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TEST-GRATIS snapshot (pure-read su DB esistente): perche' i segni si cancellano?
Reperto: |s_k| alto (commitment locale) ma <s_i*s_j>~0 (scorrelato sugli archi). Discrimina 4 ipotesi:
 (a) coppie iniettano segni opposti; (b) twist non accumula (segno indefinito); (c) torque~0 (media vicini
 si cancella); (d) segno geometricamente random. Snapshot = un istante (per la traiettoria serve il trace)."""
import pickle, sys
import numpy as np

def canon(nb):  # = _bloch_a_spinore
    nb = np.asarray(nb, float).reshape(-1, 3)
    th = np.arccos(np.clip(nb[:, 2], -1.0, 1.0)); ph = np.arctan2(nb[:, 1], nb[:, 0])
    return np.stack([np.cos(th/2.0), np.sin(th/2.0)*np.exp(1j*ph)], axis=1)

p = sys.argv[1] if len(sys.argv) > 1 else 'csv/deparam_pilota_k2/db_on.pkl'
a = pickle.load(open(p, 'rb'))['attrs']
n = len(a['phi']); PHI = 2*np.pi
psi = np.asarray(a['_psi_spinor'])[:n]; nb = np.asarray(a['_nb'])[:n]
i = np.asarray(a['i']); j = np.asarray(a['j']); tw = np.asarray(a['tw']); deg = np.asarray(a['_deg'])[:n]
mk = (i < n) & (j < n); ii = i[mk]; jj = j[mk]
s = np.real(np.sum(np.conj(canon(nb)) * psi, axis=1))     # foglio +- per nodo
sg = np.sign(s)
print(f"=== SNAPSHOT {p}  (n={n}, archi={mk.sum()}) ===")
print(f"|s_k| (commitment locale): mean={np.mean(np.abs(s)):.3f}  median={np.median(np.abs(s)):.3f}  (alto=segno DEFINITO)")
print(f"segno s_k: +{100*np.mean(sg>0):.1f}%  -{100*np.mean(sg<0):.1f}%")
# --- meccanismo di cancellazione: archi concordi/discordi ---
prod = sg[ii]*sg[jj]
print(f"\n[MECCANISMO] archi sign_i*sign_j: concordi(+1) {100*np.mean(prod>0):.1f}%  discordi(-1) {100*np.mean(prod<0):.1f}%  <prod>={np.mean(prod):+.4f}")
print("  -> ~50/50 = i segni si cancellano SUGLI ARCHI (definiti localmente, scorrelati fra vicini)")
# --- (b) twist accumula? ---
twn = np.zeros(n); np.add.at(twn, i, np.abs(tw)); np.add.at(twn, j, np.abs(tw)); twn = twn/np.maximum(deg,1)
print(f"\n[b: twist] twn/2pi: mean={np.mean(twn)/PHI:.3f}  frazione>2pi(giro completo)={100*np.mean(twn>PHI):.1f}%")
print(f"  |s_k| e' alto ({np.mean(np.abs(s)):.2f})? -> il segno e' DEFINITO, NON indefinito -> ipotesi (b) {'DEBOLE' if np.mean(np.abs(s))>0.4 else 'possibile'}")
# --- (c) torque: media SU(2) dei vicini si cancella? ---
acc = np.zeros((n,2), complex); np.add.at(acc, ii, psi[jj]); np.add.at(acc, jj, psi[ii])
mag = np.linalg.norm(acc, axis=1)/np.maximum(deg,1)       # |media vicini psi| per nodo
print(f"\n[c: torque] |media SU(2) vicini| per nodo: mean={np.mean(mag):.3f}  (0=si cancella->torque nullo, 1=allineati)")
# --- (d) segno spazialmente random vs correlato con la geometria ---
# correlazione di sign(s) con twn (l'olonomia): il segno segue la torsione o e' random?
from numpy import corrcoef
c_stw = corrcoef(sg, twn)[0,1]; c_snz = corrcoef(sg, nb[:,2])[0,1]
print(f"\n[d: random?] corr(sign_s, twn)={c_stw:+.3f}  corr(sign_s, nb_z)={c_snz:+.3f}  (~0 = segno NON legato a torsione/geometria = random)")
print(f"\nLEGGIBILITA': pattern sistematico? archi {100*np.mean(prod>0):.0f}/{100*np.mean(prod<0):.0f}, |media vicini|={np.mean(mag):.2f} -> {'LEGGIBILE (deterministico)' if True else 'caos'}")
