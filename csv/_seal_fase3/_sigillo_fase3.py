"""[branch dev-spinoriale] SIGILLO FASE 3 (coppia = overlap spinoriale).

GATE = riduzione-al-limite S3: con spinore in fase psi=(e^{i phi},0), la coppia SPINORIALE
(ramo CAMPO_SPINORIALE) deve coincidere ESATTAMENTE con la coppia SCALARE (canonico).
Se NON coincide -> FERMATI (la generalizzazione non e' esatta).

Test in-process sul VERO codice (_coppia_interferenza), nessuna replica della matematica a mano.
Include anche la controprova: fuori dal limite (comp b != 0) la coppia DEVE differire.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

rng = np.random.default_rng(1)

# --- Costruisco una rete piccola e coerente (2000 passi non servono: testo la FORMULA) ---
net = sm.Rete(seed=1)
net.semina(200)
for _ in range(30):
    net.step()

n = net.n
i, j = net.i, net.j
w = net._pesi()
A = w * np.cos(net.phi0[i] - net.phi0[j])
z = np.exp(1j * net.phi)

# --- LIMITE: spinore ESATTAMENTE in fase con phi -> psi=(e^{i phi}, 0) ---
psi_lim = np.zeros((n, 2), dtype=complex)
psi_lim[:, 0] = np.exp(1j * net.phi[:n])
psi_lim[:, 1] = 0.0
net._psi_spinor = psi_lim

sm.CAMPO_SPINORIALE = False
c_scal = net._coppia_interferenza(A, z)
sm.CAMPO_SPINORIALE = True
c_spin = net._coppia_interferenza(A, z)

d = np.max(np.abs(c_spin - c_scal))
print(f"[S3 GATE] max|coppia_spin - coppia_scal| (limite b=0) = {d:.3e}")
gate_ok = d < 1e-12
print(f"[S3 GATE] {'PASS' if gate_ok else 'FAIL -> FERMATI'}")

# --- CONTROPROVA: spinore NON riducibile a fase U(1) (theta/fase VARIANO per nodo) -> DEVE differire ---
theta = rng.uniform(0.1, 1.4, n)      # asse Bloch diverso per nodo (non gauge globale)
chi = rng.uniform(0.0, 2 * np.pi, n)  # fase relativa componenti diversa per nodo
psi_gen = np.zeros((n, 2), dtype=complex)
psi_gen[:, 0] = np.exp(1j * net.phi[:n]) * np.cos(theta / 2)
psi_gen[:, 1] = np.exp(1j * (net.phi[:n] + chi)) * np.sin(theta / 2)
net._psi_spinor = psi_gen
c_spin2 = net._coppia_interferenza(A, z)
dg = np.max(np.abs(c_spin2 - c_scal))
print(f"[CONTROPROVA] max|coppia_spin(b!=0) - coppia_scal| = {dg:.3e} (deve essere > 0)")
print(f"[CONTROPROVA] {'PASS (non-abeliano attivo)' if dg > 1e-9 else 'FAIL (ramo inerte)'}")

# --- Fallback: spinore assente -> coppia == scalare ---
net._psi_spinor = None
c_fb = net._coppia_interferenza(A, z)
df = np.max(np.abs(c_fb - c_scal))
print(f"[FALLBACK] spinore None -> max|coppia - scal| = {df:.3e} (deve essere 0)")

print("\nESITO:", "SIGILLO FASE 3 OK" if (gate_ok and dg > 1e-9 and df < 1e-12)
      else "SIGILLO FASE 3 FALLITO")
