"""[dev-spinoriale] CANDIDATO B'' — depurazione col riferimento dal CAMPO EMESSO psi_spin.

B' (rif = arg(_psi_spinor_0)) e' CIECO all'antimateria (il rif si ribalta col segno globale).
B'' usa il rif dal CAMPO EMESSO psi_spin[:,0], che NON dipende dal segno globale di _psi_spinor:
  s_k(B'') = sign( Re( e^{-i arg(psi_spin_0)} <canon(nb)|_psi_spinor> ) )
Test-GRATIS: (a) limite -> +1 su 120/120? (b) flip/passo (stabile?) (c) vede l'antimateria (psi->-psi)?
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False


def _rif_emesso(net, n):
    ps = getattr(net, "psi_spin", None)
    if ps is None or len(ps) < n:
        net.calcola_psi(); ps = net.psi_spin
    return np.angle(ps[:n, 0])


def sk_Bpp(net, n):
    canon = net._bloch_a_spinore(net._nb[:n])
    ov = np.sum(np.conj(canon) * net._psi_spinor[:n], axis=1)
    ov_ref = np.exp(-1j * _rif_emesso(net, n)) * ov
    return np.where(np.real(ov_ref) >= 0.0, 1.0, -1.0)


# (a) LIMITE
net = sm.Rete(seed=1); net.semina(120)
sm.CAMPO_SPINORIALE = False
for _ in range(40):
    net.step()
sm.CAMPO_SPINORIALE = True
n = net.n
net.calcola_psi()
ps = np.zeros((n, 2), complex); ps[:, 0] = np.exp(1j * net.phi[:n])
net._psi_spinor = ps.copy(); net._nb = np.tile([0.0, 0.0, 1.0], (n, 1))
# nel limite il campo emesso psi_spin[:,0] deve valere e^{i phi}: lo forzo coerente col limite
net.psi_spin = ps.copy()
b_lim = sk_Bpp(net, n)
print("=== B'' (rif dal campo emesso) ===")
print(f"  (a) LIMITE: +1 su {int((b_lim>0).sum())}/{n}   {'PASS' if np.all(b_lim>0) else 'FAIL'}")

# (b) FLIP + (c) ANTIMATERIA fuori dal limite
net = sm.Rete(seed=1); net.semina(120)
for _ in range(60):
    net.step()
n = net.n
prev = sk_Bpp(net, n); flips = []
for _ in range(20):
    net.step(); cur = sk_Bpp(net, n); flips.append(np.mean(cur != prev)); prev = cur
print(f"  (b) FLIP/passo = {np.mean(flips)*100:.1f}%   ({'STABILE' if np.mean(flips)<0.05 else 'instabile'})")

B0 = sk_Bpp(net, n)
mask = np.zeros(n, bool); mask[::2] = True
net._psi_spinor[mask] = -net._psi_spinor[mask]     # antimateria su meta' nodi
B1 = sk_Bpp(net, n)
print(f"  (c) sotto psi->-psi (antimateria): s_k(B'') cambiati {int(np.sum(B0[mask]!=B1[mask]))}/{int(mask.sum())}  (60/60 = vede l'antimateria)")
vede = np.sum(B0[mask] != B1[mask]) == mask.sum()
stab = np.mean(flips) < 0.05
lim = np.all(b_lim > 0)
print()
print(f"  ESITO B'': limite {'OK' if lim else 'NO'} | stabile {'OK' if stab else 'NO'} | vede antimateria {'OK' if vede else 'NO'}")
_verdetto = "B'' RISOLVE (stabile E vede antimateria): candidato valido" if (lim and stab and vede) else "B'' non risolve del tutto"
print(f"  -> {_verdetto}")
