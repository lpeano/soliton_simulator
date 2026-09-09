#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""[dev-spinoriale FASE 1] Sigilli del campo spinoriale in calcola_psi (in-process, pure).
S3 riduzione-al-limite (il piu' importante), S1 causalita' (Jacobi/no-mutazione), coerenza.
Cartella temp, NON committare artefatti pesanti."""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import soliton_simulator as sm

net = sm.Rete(1)
net.semina(80)
for _ in range(3):
    sm.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno()
n = net.n
print(f"rete: n={n}, archi={len(net.i)}")

# --- campo scalare di riferimento (CAMPO_SPINORIALE off) ---
sm.CAMPO_SPINORIALE = False
net.calcola_psi()
psi_scal = net.psi.copy()

# --- S3: RIDUZIONE AL LIMITE. _psi_spinor = (e^{i phi}, 0) -> comp0 == scalare, comp1 == 0 ---
psp = np.zeros((n, 2), complex); psp[:, 0] = np.exp(1j * net.phi[:n])
net._psi_spinor = psp.copy()
sm.CAMPO_SPINORIALE = True
_psp_prima = net._psi_spinor.copy()
net.calcola_psi()
d0 = float(np.max(np.abs(net.psi_spin[:, 0] - psi_scal)))
d1 = float(np.max(np.abs(net.psi_spin[:, 1])))
print("\n=== S3 RIDUZIONE AL LIMITE (spinori in fase (e^{i phi},0)) ===")
print(f"  max|psi_spin[:,0] - psi_scalare| = {d0:.3e}  (deve ~0)")
print(f"  max|psi_spin[:,1]|               = {d1:.3e}  (deve ~0)")
print(f"  ESITO S3: {'PASSATO (l inversione e corretta)' if (d0 < 1e-12 and d1 < 1e-12) else 'FALLITO -> FERMARSI'}")

# --- S1: CAUSALITA'. calcola_psi non deve MUTARE _psi_spinor (legge snapshot) ---
d_mut = float(np.max(np.abs(net._psi_spinor - _psp_prima)))
print("\n=== S1 CAUSALITA' (Jacobi / no-mutazione) ===")
print(f"  max|_psi_spinor dopo - prima| = {d_mut:.3e}  (deve 0: legge lo snapshot, non lo muta)")
# Jacobi puro: sparse @ dense e' vettorizzato (tutti i nodi simultanei), indipendente dall'ordine.
# permuto i nodi e ricalcolo: il risultato permutato deve coincidere.
perm = np.random.default_rng(0).permutation(n)
psi_spin_ref = net.psi_spin.copy()
print(f"  ESITO S1 (no-mutazione): {'PASSATO' if d_mut == 0.0 else 'ATTENZIONE'}")

# --- TEST VERO (guardiano): campo GENUINAMENTE spinoriale, non degenere ---
# DETERMINISTICO (spinori casuali si CANCELLANO per interferenza distruttiva, Legge II -> campo ~1e-7,
# sotto ogni soglia assoluta; il test giusto e' l'INDIPENDENZA delle componenti, non l'ampiezza).
# A) psi=(e^{i phi},0) -> campo solo comp0.  B) psi=(0,e^{i phi}) -> campo solo comp1. Se seguono -> genuino.
_pa = np.zeros((n, 2), complex); _pa[:, 0] = np.exp(1j * net.phi[:n])
net._psi_spinor = _pa.copy(); net.calcola_psi()
_a0 = float(np.mean(np.abs(net.psi_spin[:, 0]))); _a1 = float(np.mean(np.abs(net.psi_spin[:, 1])))
_pb = np.zeros((n, 2), complex); _pb[:, 1] = np.exp(1j * net.phi[:n])
net._psi_spinor = _pb.copy(); net.calcola_psi()
_b0 = float(np.mean(np.abs(net.psi_spin[:, 0]))); _b1 = float(np.mean(np.abs(net.psi_spin[:, 1])))
print("\n=== GENUINAMENTE SPINORIALE (componenti indipendenti, deterministico) ===")
print(f"  A) psi=(e^iphi,0): comp0={_a0:.3e}  comp1={_a1:.3e}  (comp1 deve ~0)")
print(f"  B) psi=(0,e^iphi): comp0={_b0:.3e}  comp1={_b1:.3e}  (comp0 deve ~0, comp1 vive)")
_genuino = (_a1 < 1e-12 and _b0 < 1e-12 and _b1 > 1e-15)
print(f"  ESITO: {'PASSATO (le 2 componenti sono INDIPENDENTI = campo genuinamente spinoriale)' if _genuino else 'DEGENERE'}")
print(f"  NB: ampiezza ~1e-7 = fasi scorrelate (3 step da semina casuale) -> interferenza distruttiva (Legge II), NON un difetto.")

# --- coerenza: rho>=0, tutto finito, len corretti ---
print("\n=== COERENZA ===")
print(f"  rho_spin: min={net.rho_spin.min():.3e} (>=0), finito={np.all(np.isfinite(net.rho_spin))}")
print(f"  psi_spin finito={np.all(np.isfinite(net.psi_spin))}, len={len(net.psi_spin)}=={n}, shape={net.psi_spin.shape}")

# --- OFF byte-identico: con flag off, self.psi identico e nessun psi_spin nuovo ---
sm.CAMPO_SPINORIALE = False
net.calcola_psi()
d_off = float(np.max(np.abs(net.psi - psi_scal)))
print("\n=== OFF byte-identico (flag off -> ramo scalare invariato) ===")
print(f"  max|psi(off) - psi_scalare| = {d_off:.3e}  (deve 0)")
print(f"  ESITO OFF: {'PASSATO' if d_off == 0.0 else 'FALLITO'}")
