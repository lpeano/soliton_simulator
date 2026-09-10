"""[branch dev-spinoriale] SIGILLO FASE 4 (evoluzione dello spinore non-abeliana - ARRICCHIMENTO).

MOD 4.1 inerzia = rho_spin (era |psi|^2). MOD 4.2 correzione = cross(B,nb) + cross(nb_campo,nb)
(ARRICCHIMENTO: mantiene i generatori chirali di B, aggiunge il torque verso il Bloch del campo emesso).

GATE = S3 riduzione-al-limite: con spinori in fase psi=(e^{i phi},0), l'EVOLUZIONE COMPLETA (un passo,
_psi_spinor e _nb) deve essere IDENTICA ON vs OFF. cross(nb_campo,nb)=cross(nb_campo-nb,nb) -> 0 nel limite
(nb_campo=nb=polo); rho_spin=|psi|^2 nel limite. Se NON coincide -> FERMATI.

Deterministico (stesso seed, stessi 20 passi di formazione a CAMPO OFF -> stato identico), poi UN passo dal
limite con campo ON/OFF. Controprova: spinori per-nodo -> ON != OFF (evoluzione non-abeliana attiva).
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

# flag necessari perche' l'evoluzione spinoriale sia viva (_psi_spinor primario)
sm.SPINORE_VIVO = True
sm.SPINORE_CORRETTO = True
sm.CHI_CORE = True
# S3 e' una riduzione DETERMINISTICA: spengo il rumore del vuoto (SCUOTIMENTO), che altrimenti
# perturba il Bloch di stato self._nb e attiva (correttamente) il torque di riallineamento
# cross(nb_campo, nb) -> non-byte-identico per reazione al rumore, non per deviazione dal limite.
sm.SCUOTIMENTO = False


def stato_base():
    """20 passi di formazione a CAMPO OFF (deterministico, stesso seed) -> stato identico riproducibile."""
    sm.CAMPO_SPINORIALE = False
    net = sm.Rete(seed=1)
    net.semina(120)
    for _ in range(20):
        net.step()
    return net


def un_passo_dal_limite(campo_finale):
    net = stato_base()
    n = net.n
    # forzo spinori IN FASE: psi=(e^{i phi}, 0) -> tutti i Bloch al polo nord
    ps = np.zeros((n, 2), complex)
    ps[:, 0] = np.exp(1j * net.phi[:n])
    net._psi_spinor = ps.copy()
    net._nb = np.tile([0.0, 0.0, 1.0], (n, 1))
    sm.CAMPO_SPINORIALE = campo_finale
    net.step()
    return net._psi_spinor.copy(), net._nb.copy(), net.n


def un_passo_pernodo(campo_finale):
    net = stato_base()
    n = net.n
    rng = np.random.default_rng(7)
    theta = rng.uniform(0.1, 1.4, n)
    chi = rng.uniform(0.0, 2 * np.pi, n)
    ps = np.zeros((n, 2), complex)
    ps[:, 0] = np.exp(1j * net.phi[:n]) * np.cos(theta / 2)
    ps[:, 1] = np.exp(1j * (net.phi[:n] + chi)) * np.sin(theta / 2)
    net._psi_spinor = ps.copy()
    sm.CAMPO_SPINORIALE = campo_finale
    net.step()
    return net._psi_spinor.copy(), net.n


print("=== S3 GATE: riduzione-al-limite (spinori in fase, evoluzione completa ON vs OFF) ===")
psiA, nbA, nA = un_passo_dal_limite(False)
psiB, nbB, nB = un_passo_dal_limite(True)
m = min(nA, nB)
d_psi = np.max(np.abs(psiA[:m] - psiB[:m]))
d_nb = np.max(np.abs(nbA[:m] - nbB[:m]))
print(f"  n: OFF={nA} ON={nB}")
print(f"  max|_psi_spinor(t+dt) ON-OFF| = {d_psi:.3e}  (deve ~0)")
print(f"  max|_nb(t+dt) ON-OFF|         = {d_nb:.3e}  (deve ~0)")
gate = (nA == nB) and d_psi < 1e-12 and d_nb < 1e-12
print(f"  ESITO S3 GATE: {'PASS' if gate else 'FAIL -> FERMATI'}")

print("\n=== CONTROPROVA non-abeliana (spinori per-nodo -> evoluzione ON != OFF) ===")
pgA, ngA = un_passo_pernodo(False)
pgB, ngB = un_passo_pernodo(True)
mg = min(ngA, ngB)
dg = np.max(np.abs(pgA[:mg] - pgB[:mg]))
print(f"  max|_psi_spinor ON-OFF| (per-nodo) = {dg:.3e}  (deve > 0)")
print(f"  ESITO: {'PASS (evoluzione non-abeliana attiva)' if dg > 1e-9 else 'FAIL (ramo inerte)'}")

print("\nESITO FASE 4:", "SIGILLO OK" if (gate and dg > 1e-9) else "SIGILLO FALLITO")
