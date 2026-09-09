#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""[dev-spinoriale FASE 2] Sigillo S3 riduzione-al-limite IN-PROCESS su stato COERENTE.
Nel limite: _psi_spinor=(e^{i phi},0) E _nb=[0,0,1] (coerenti) -> gli helper _rho_sorgente e _nb_grav
(che pilotano densita' e gravita') devono ridursi ESATTAMENTE al vecchio (|psi|^2 e _nb).
Fuori limite (spinori evoluti) diverge = nuova fisica (voluto, Fase 2)."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import soliton_simulator as sm

net = sm.Rete(1); net.semina(80)
for _ in range(3): sm.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno()
n = net.n
net.calcola_psi()
rho_scal = np.abs(net.psi[:n]) ** 2                      # densita' vecchia

# --- STATO COERENTE nel limite: spinore in fase asse 0, nb = Bloch = [0,0,1] ---
psp = np.zeros((n, 2), complex); psp[:, 0] = np.exp(1j * net.phi[:n])
net._psi_spinor = psp.copy()
net._nb = np.tile(np.array([0.0, 0.0, 1.0]), (n, 1))     # Bloch di (e^{i phi},0), coerente
nb_vecchio = net._nb.copy()

sm.CAMPO_SPINORIALE = True
net.calcola_psi()                                        # calcola psi_spin/rho_spin
rho_on = net._rho_sorgente()                             # densita' sorgente (ON)
nb_on = net._nb_grav()                                   # direzione gravita' (ON, nativa dal campo)

d_rho = float(np.max(np.abs(rho_on - rho_scal)))
d_nb = float(np.max(np.abs(nb_on - nb_vecchio)))
print("=== S3 RIDUZIONE-AL-LIMITE (stato coerente: psi=(e^iphi,0), nb=[0,0,1]) ===")
print(f"  densita': max|rho_spin - |psi|^2|      = {d_rho:.3e}  (deve ~0)")
print(f"  direzione: max|nb_nativo - nb_vecchio| = {d_nb:.3e}  (deve ~0)")
_ok = (d_rho < 1e-12 and d_nb < 1e-12)
print(f"  ESITO S3: {'PASSATO (densita e gravita si riducono al vecchio)' if _ok else 'FALLITO -> FERMARSI'}")

# --- coerenza: nb normalizzato, rho>=0 ---
_nn = np.linalg.norm(nb_on, axis=1)
print("\n=== COERENZA ===")
print(f"  |nb_nativo| in [1-e,1+e]: max|1-|nb|| = {np.max(np.abs(_nn - 1.0)):.3e}")
print(f"  rho_spin: min={rho_on.min():.3e} (>=0), finito={np.all(np.isfinite(rho_on))}")

# --- controprova (fuori limite): spinori con comp1 != 0 -> nb_nativo != [0,0,1] (nuova fisica) ---
_pb = np.zeros((n, 2), complex)
_th = 0.7; _pb[:, 0] = np.cos(_th) * np.exp(1j * net.phi[:n]); _pb[:, 1] = np.sin(_th)
net._psi_spinor = _pb.copy(); net.calcola_psi()
nb_out = net._nb_grav()
_devia = float(np.mean(np.abs(nb_out[:, 2] - 1.0)))      # nb_z si stacca da 1 = direzione diversa
print("\n=== CONTROPROVA fuori limite (spinori inclinati theta=0.7) ===")
print(f"  media|nb_z - 1| = {_devia:.3f}  (>0 = la gravita' vede una direzione DIVERSA = campo pilota, nuova fisica)")
