"""Diagnostica S3 Fase 4: confronta il gate su ATTUALE (Fase 4) vs BACKUP (Fase 3).
Se il backup da' ~0 e l'attuale 2e-3 -> il colpevole e' Fase 4. Altrimenti e' lo step completo."""
import os, sys, importlib.util
import numpy as np

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def gate(sm):
    sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True

    def base():
        sm.CAMPO_SPINORIALE = False
        net = sm.Rete(seed=1); net.semina(120)
        for _ in range(20):
            net.step()
        return net

    def passo(campo):
        net = base()
        n = net.n
        ps = np.zeros((n, 2), complex); ps[:, 0] = np.exp(1j * net.phi[:n])
        net._psi_spinor = ps.copy()
        net._nb = np.tile([0.0, 0.0, 1.0], (n, 1))
        sm.CAMPO_SPINORIALE = campo
        net.step()
        return net._psi_spinor.copy(), net._nb.copy(), net.n

    pA, nbA, nA = passo(False)
    pB, nbB, nB = passo(True)
    m = min(nA, nB)
    return np.max(np.abs(pA[:m] - pB[:m])), np.max(np.abs(nbA[:m] - nbB[:m]))


att = load(os.path.join(BASE, 'soliton_simulator.py'), 'm_att')
bk = load(os.path.join(BASE, 'soliton_simulator.backup_2026-09-10_fase4.py'), 'm_bk')

dpsi_att, dnb_att = gate(att)
dpsi_bk, dnb_bk = gate(bk)
print(f"ATTUALE (Fase 4): max|dpsi|={dpsi_att:.3e}  max|dnb|={dnb_att:.3e}")
print(f"BACKUP  (Fase 3): max|dpsi|={dpsi_bk:.3e}  max|dnb|={dnb_bk:.3e}")
print()
if dpsi_bk < 1e-12 and dpsi_att > 1e-9:
    print("=> COLPEVOLE: Fase 4 (il backup si riduce, l'attuale no).")
elif dpsi_bk > 1e-9:
    print("=> Il 2e-3 preesiste (Fasi 1-3 in step completo): il confronto su step() e' troppo severo,")
    print("   il gate va fatto SULLA SOLA EVOLUZIONE (_passo_spinoriale), non sullo step intero.")
else:
    print("=> Entrambi ~0: rivedere il setup del sigillo.")
