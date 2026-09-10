"""[dev-spinoriale] VERIFICA DECISIVA: s_k(B') e' cieco all'antimateria?

L'antinodo (antimateria) nasce come _psi_spinor -> -_psi_spinor (segno globale, riga 985).
s_k(B') = sign(Re( e^{-i arg(psi_0)} <canon(nb)|psi> )) rimuove la fase globale via arg(psi_0).
Ma un segno globale (-1) E' una fase globale (pi). Test: s_k(B') cambia sotto psi -> -psi?
Se NON cambia -> B' e' CIECO all'antimateria (sempre +1 = triviale). s_k(A) invece deve cambiare.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False


def sk_A(net, n):
    canon = net._bloch_a_spinore(net._nb[:n])
    ov = np.sum(np.conj(canon) * net._psi_spinor[:n], axis=1)
    return np.where(np.real(ov) >= 0.0, 1.0, -1.0)


def sk_Bprime(net, n):
    canon = net._bloch_a_spinore(net._nb[:n])
    ov = np.sum(np.conj(canon) * net._psi_spinor[:n], axis=1)
    ov_ref = np.exp(-1j * np.angle(net._psi_spinor[:n, 0])) * ov
    return np.where(np.real(ov_ref) >= 0.0, 1.0, -1.0)


net = sm.Rete(seed=1); net.semina(120)
for _ in range(60):
    net.step()
n = net.n

A0 = sk_A(net, n); B0 = sk_Bprime(net, n)

# creo ANTIMATERIA a mano su meta' dei nodi: _psi_spinor -> -_psi_spinor (come l'antinodo, riga 985)
mask = np.zeros(n, bool); mask[::2] = True     # meta' nodi diventano antimateria
net._psi_spinor[mask] = -net._psi_spinor[mask]

A1 = sk_A(net, n); B1 = sk_Bprime(net, n)

print("=== VERIFICA: s_k sotto psi -> -psi (creazione di antimateria) su meta' dei nodi ===")
print(f"  s_k(A)  cambiati: {int(np.sum(A0[mask] != A1[mask]))}/{int(mask.sum())}  (dovrebbe cambiare TUTTI = vede l'antimateria)")
print(f"  s_k(B') cambiati: {int(np.sum(B0[mask] != B1[mask]))}/{int(mask.sum())}  (se 0 -> CIECO all'antimateria)")
print()
print(f"  s_k(A)  su antimateria: +1 su {int((A1[mask]>0).sum())}, -1 su {int((A1[mask]<0).sum())}")
print(f"  s_k(B') su antimateria: +1 su {int((B1[mask]>0).sum())}, -1 su {int((B1[mask]<0).sum())}")
print()
if np.sum(B0[mask] != B1[mask]) == 0:
    print("  ESITO: B' e' INVARIANTE sotto psi->-psi -> CIECO all'antimateria (sempre +1 = triviale).")
    print("         La depurazione ha rimosso ANCHE il segno di doppia-copertura (che E' una fase globale pi).")
    print("         A vede l'antimateria ma OSCILLA col de Broglie. Nessuno dei due va bene -> FERMARSI.")
else:
    print("  ESITO: B' distingue l'antimateria. OK.")
