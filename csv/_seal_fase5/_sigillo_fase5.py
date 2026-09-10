"""[branch dev-spinoriale] SIGILLO FASE 5 (canali del SEGNO non-abeliani).

MOD 5.1 coppie (densita' -> _rho_sorgente, eredita' antinodo segno opposto agganciata a CAMPO_SPINORIALE).
MOD 5.2 mitosi (soglia densita' -> _rho_sorgente, figlio eredita spinore pieno).
MOD 5.3 tempo proprio: ritmo() dal campo spinoriale (psi_spin[:,0]) battendo su 4pi.

GATE = S3 riduzione-al-limite DETERMINISTICA (senza rumore): con spinori in fase psi=(e^{i phi},0),
UN passo completo (N, phi, pos, _psi_spinor, _nb) deve essere IDENTICO ON vs OFF. rho_spin=|psi|^2,
ritmo spinoriale=ritmo scalare (|dphi|<pi), eredita' invariata nel limite. Se NON coincide -> FERMATI.

Deterministico: stessi 40 passi di formazione a CAMPO OFF (stesso seed) -> stato identico; poi 1 passo dal
limite con campo ON/OFF. Controprova: spinori per-nodo -> ON != OFF (canali del segno non-abeliani).
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.SPINORE_VIVO = True
sm.SPINORE_CORRETTO = True
sm.CHI_CORE = True
# S3 = riduzione DETERMINISTICA: spengo il rumore del vuoto (reagisce, come in Fase 4).
sm.SCUOTIMENTO = False


def stato_base():
    sm.CAMPO_SPINORIALE = False
    net = sm.Rete(seed=1)
    net.semina(120)
    for _ in range(40):
        net.step()
    return net


def un_passo(campo, in_fase=True, seed_pernodo=7):
    net = stato_base()
    n = net.n
    if in_fase:
        ps = np.zeros((n, 2), complex)
        ps[:, 0] = np.exp(1j * net.phi[:n])
        net._psi_spinor = ps.copy()
        net._nb = np.tile([0.0, 0.0, 1.0], (n, 1))
    else:
        rng = np.random.default_rng(seed_pernodo)
        theta = rng.uniform(0.1, 1.4, n); chi = rng.uniform(0.0, 2 * np.pi, n)
        ps = np.zeros((n, 2), complex)
        ps[:, 0] = np.exp(1j * net.phi[:n]) * np.cos(theta / 2)
        ps[:, 1] = np.exp(1j * (net.phi[:n] + chi)) * np.sin(theta / 2)
        net._psi_spinor = ps.copy()
    sm.CAMPO_SPINORIALE = campo
    net.step()
    return net


def confronta(a, b):
    m = min(a.n, b.n)
    d = {}
    d['n'] = (a.n, b.n)
    d['phi'] = np.max(np.abs(a.phi[:m] - b.phi[:m]))
    d['pos'] = np.max(np.abs(a.pos[:m] - b.pos[:m]))
    if hasattr(a, '_psi_spinor') and hasattr(b, '_psi_spinor'):
        mm = min(len(a._psi_spinor), len(b._psi_spinor), m)
        d['psi_spinor'] = np.max(np.abs(a._psi_spinor[:mm] - b._psi_spinor[:mm]))
    return d


print("=== S3 GATE: riduzione-al-limite (spinori in fase, 1 passo ON vs OFF) ===")
A = un_passo(False, in_fase=True)
B = un_passo(True, in_fase=True)
d = confronta(A, B)
print(f"  n: OFF={d['n'][0]} ON={d['n'][1]}")
print(f"  max|dphi|        = {d['phi']:.3e}  (deve ~0)")
print(f"  max|dpos|        = {d['pos']:.3e}  (deve ~0)")
print(f"  max|d_psi_spinor|= {d.get('psi_spinor', float('nan')):.3e}  (deve ~0)")
gate = (d['n'][0] == d['n'][1]) and d['phi'] < 1e-10 and d['pos'] < 1e-10 and d.get('psi_spinor', 1) < 1e-10
print(f"  ESITO S3 GATE: {'PASS' if gate else 'FAIL -> FERMATI'}")

print("\n=== CONTROPROVA non-abeliana (spinori per-nodo -> ON != OFF) ===")
C = un_passo(False, in_fase=False)
D = un_passo(True, in_fase=False)
dd = confronta(C, D)
diff = max(dd['phi'], dd['pos'], dd.get('psi_spinor', 0))
print(f"  n: OFF={dd['n'][0]} ON={dd['n'][1]}  max|dphi|={dd['phi']:.3e} max|d_psi_spinor|={dd.get('psi_spinor', float('nan')):.3e}")
print(f"  ESITO: {'PASS (canali del segno non-abeliani attivi)' if diff > 1e-9 else 'FAIL (ramo inerte)'}")

print("\nESITO FASE 5:", "SIGILLO OK" if (gate and diff > 1e-9) else "SIGILLO FALLITO")
