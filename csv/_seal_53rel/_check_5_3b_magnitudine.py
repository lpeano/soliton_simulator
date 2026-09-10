"""[dev-spinoriale] CHECK 5.3b — la magnitudine di ritmo() (Fase5) e' gia' torsionale o e' de Broglie?

ritmo() sotto CAMPO_SPINORIALE: f = |Delta angle(psi_spin[:,0])|/DT (rate de Broglie del CAMPO
EMESSO), poi normalizzato mediana + bottleneck -> r. Confronto r con la dilatazione torsionale
esplicita tau_nodo = 1 + media_archi|tw|/PHI_CRIT (la stessa del kernel mitosi).
Se corr(r, tau_nodo) ~ forte -> 5.3b e' quasi no-op. Se ~0 -> 5.3b e' sostituzione REALE.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False
PHI = sm.PHI_CRIT


def tau_nodo_torsione(net):
    n = net.n
    aw = np.abs(net.tw)
    acc = np.zeros(n); i, j = net.i, net.j
    mi = i < n; mj = j < n
    np.add.at(acc, i[mi], aw[mi]); np.add.at(acc, j[mj], aw[mj])
    deg = getattr(net, "_deg", None)
    deg = np.asarray(deg)[:n] if deg is not None and len(deg) >= n else (
        np.bincount(i[mi], minlength=n)[:n] + np.bincount(j[mj], minlength=n)[:n])
    return 1.0 + acc / np.maximum(deg, 1) / PHI


net = sm.Rete(seed=1)
net.semina(120)
for _ in range(60):
    net.step()

corrs = []
for s in range(10):
    net.step()
    r = net.ritmo()               # magnitudine attuale (de Broglie del campo emesso, normalizzata)
    if r is None:
        continue
    tau = tau_nodo_torsione(net)
    m = min(len(r), len(tau))
    rr, tt = np.asarray(r)[:m], tau[:m]
    ok = np.isfinite(rr) & np.isfinite(tt)
    if ok.sum() > 10 and np.std(rr[ok]) > 0 and np.std(tt[ok]) > 0:
        corrs.append(np.corrcoef(rr[ok], tt[ok])[0, 1])

print("=== CHECK 5.3b: corr( ritmo() , 1+|tw|/PHI_CRIT ) ===")
print(f"  corr media = {np.mean(corrs):+.4f}  (min {np.min(corrs):+.4f}  max {np.max(corrs):+.4f})  su {len(corrs)} passi")
c = np.mean(corrs)
if abs(c) > 0.7:
    print("  -> magnitudine GIA' torsionale: 5.3b quasi no-op")
elif abs(c) > 0.3:
    print("  -> parzialmente correlata: 5.3b cambierebbe il pattern in parte")
else:
    print("  -> magnitudine NON torsionale (de Broglie): 5.3b = SOSTITUZIONE REALE (rompe riduzione a Fase5)")
