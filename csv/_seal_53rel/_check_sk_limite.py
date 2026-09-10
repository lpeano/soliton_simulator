"""[dev-spinoriale] CHECK riduzione-al-limite di s_k (design MOD 5.3a) — nessuna modifica al codice.

Verifica il PUNTO CRITICO: nel limite scalare (spinori in fase, tutta materia), la formula
LETTERALE s_k = sign(Re<canon(nb)|_psi_spinor>) da' +1 (come assunto) o oscilla con la fase?
Confronta con la variante a FASE RIMOSSA s_k = sign(Re( e^{-i phi} <canon|psi> )).
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = False
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False

net = sm.Rete(seed=1)
net.semina(120)
for _ in range(40):
    net.step()
n = net.n

# STATO LIMITE (come il sigillo S3 in_fase): _psi_spinor=(e^{i phi},0), nb=polo nord
ps = np.zeros((n, 2), complex); ps[:, 0] = np.exp(1j * net.phi[:n])
net._psi_spinor = ps.copy()
net._nb = np.tile([0.0, 0.0, 1.0], (n, 1))

canon = net._bloch_a_spinore(net._nb[:n])
ov = np.sum(np.conj(canon) * net._psi_spinor[:n], axis=1)

# (A) formula LETTERALE
sk_lett = np.where(np.real(ov) >= 0.0, 1.0, -1.0)
# (B) fase RIMOSSA (riferita a self.phi)
ov_ref = np.exp(-1j * net.phi[:n]) * ov
sk_ref = np.where(np.real(ov_ref) >= 0.0, 1.0, -1.0)

print("=== s_k nel limite scalare (spinori in fase, tutta materia) ===")
print(f"  n = {n}")
print(f"  (A) LETTERALE  s_k=sign(Re<canon|psi>):        +1 su {int((sk_lett>0).sum())}/{n}  -1 su {int((sk_lett<0).sum())}/{n}")
print(f"      Re(ov) min={np.real(ov).min():+.3f} max={np.real(ov).max():+.3f}  (= cos(phi), oscilla!)")
print(f"  (B) FASE RIMOSSA sign(Re(e^-i.phi <canon|psi>)): +1 su {int((sk_ref>0).sum())}/{n}  -1 su {int((sk_ref<0).sum())}/{n}")
print(f"      Re(ov_ref) min={np.real(ov_ref).min():+.3f} max={np.real(ov_ref).max():+.3f}")
print()
print(f"  ESITO: (A) riduce a +1 ovunque? {'SI' if np.all(sk_lett>0) else 'NO -> S3a FALLIREBBE con la formula letterale'}")
print(f"         (B) riduce a +1 ovunque? {'SI -> riduzione esatta' if np.all(sk_ref>0) else 'NO'}")
