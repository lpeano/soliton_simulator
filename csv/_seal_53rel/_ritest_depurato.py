"""[dev-spinoriale] RI-TEST depurati MOD 5.3 — s_k=B' (fase de Broglie rimossa) + magnitudine torsionale.
Nessuna implementazione di dinamica: solo misura sui dati Fase 5.

RI-TEST 1 (s_k B'): (a) limite -> +1 su 120/120? (b) flip/passo fuori dal limite (B' stabile vs A instabile)?
                    (c) B' distingue materia/antimateria (correla con perc_chi)?
RI-TEST 2 (S3b depurato): la magnitudine = 1+|tw|/PHI_CRIT (torsione), coerente/stabile nel tempo vs de Broglie?
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False
PHI = sm.PHI_CRIT; DT = sm.DT


def sk_A(net, n):
    canon = net._bloch_a_spinore(net._nb[:n])
    ov = np.sum(np.conj(canon) * net._psi_spinor[:n], axis=1)
    return np.where(np.real(ov) >= 0.0, 1.0, -1.0)


def sk_Bprime(net, n):
    canon = net._bloch_a_spinore(net._nb[:n])
    ov = np.sum(np.conj(canon) * net._psi_spinor[:n], axis=1)
    ov_ref = np.exp(-1j * np.angle(net._psi_spinor[:n, 0])) * ov
    return np.where(np.real(ov_ref) >= 0.0, 1.0, -1.0)


def tau_nodo_torsione(net):
    n = net.n; aw = np.abs(net.tw); acc = np.zeros(n); i, j = net.i, net.j
    mi = i < n; mj = j < n
    np.add.at(acc, i[mi], aw[mi]); np.add.at(acc, j[mj], aw[mj])
    deg = getattr(net, "_deg", None)
    deg = np.asarray(deg)[:n] if deg is not None and len(deg) >= n else (
        np.bincount(i[mi], minlength=n)[:n] + np.bincount(j[mj], minlength=n)[:n])
    return 1.0 + acc / np.maximum(deg, 1) / PHI


# ===================== RI-TEST 1a: LIMITE (spinori in fase, tutta materia) =====================
net = sm.Rete(seed=1); net.semina(120)
sm.CAMPO_SPINORIALE = False
for _ in range(40):
    net.step()
n = net.n
ps = np.zeros((n, 2), complex); ps[:, 0] = np.exp(1j * net.phi[:n])
net._psi_spinor = ps.copy(); net._nb = np.tile([0.0, 0.0, 1.0], (n, 1))
a_lim = sk_A(net, n); b_lim = sk_Bprime(net, n)
print("=== RI-TEST 1a: s_k nel LIMITE (spinori in fase) ===")
print(f"  (A) letterale : +1 su {int((a_lim>0).sum())}/{n}   {'PASS' if np.all(a_lim>0) else 'FAIL (oscilla con phi)'}")
print(f"  (B') depurato : +1 su {int((b_lim>0).sum())}/{n}   {'PASS (gate S3a)' if np.all(b_lim>0) else 'FAIL'}")

# ===================== RI-TEST 1b/1c: FUORI dal limite (dinamica reale) =====================
sm.CAMPO_SPINORIALE = True
net = sm.Rete(seed=1); net.semina(120)
for _ in range(60):
    net.step()               # solo step() -> N resta costante (no mitosi) -> flip pulito
n = net.n
prevA = sk_A(net, n); prevB = sk_Bprime(net, n)
flipA = []; flipB = []; agree_chi = []
for _ in range(20):
    net.step()
    A = sk_A(net, n); B = sk_Bprime(net, n)
    flipA.append(np.mean(A != prevA)); flipB.append(np.mean(B != prevB))
    if len(net.perc_chi) >= n:
        pc = np.sign(net.perc_chi[:n]).astype(float); pc[pc == 0] = 1.0
        agree_chi.append(np.mean(B == pc))
    prevA, prevB = A, B
print("\n=== RI-TEST 1b: FLIP/passo fuori dal limite (n={}) ===".format(n))
print(f"  (A) letterale flip/passo  = {np.mean(flipA)*100:.1f}%   (instabile = oscilla col de Broglie)")
print(f"  (B') depurato flip/passo  = {np.mean(flipB)*100:.1f}%   ({'STABILE' if np.mean(flipB)<0.05 else 'ancora instabile'})")
print("\n=== RI-TEST 1c: B' distingue materia/antimateria ===")
Bfin = sk_Bprime(net, n)
print(f"  distribuzione s_k(B'): +1 su {int((Bfin>0).sum())}/{n}  -1 su {int((Bfin<0).sum())}/{n}")
if agree_chi:
    print(f"  accordo sign(s_k B') == sign(perc_chi): {np.mean(agree_chi)*100:.1f}%  (alto = coerente col lobo/chiralita')")

# ===================== RI-TEST 2: magnitudine = torsione (depurata dal de Broglie) =====================
print("\n=== RI-TEST 2: magnitudine del tempo proprio ===")
r_deb = net.ritmo()
tau = tau_nodo_torsione(net)
m = min(len(r_deb), len(tau))
c = np.corrcoef(np.asarray(r_deb)[:m], tau[:m])[0, 1]
print(f"  corr( ritmo() de Broglie , 1+|tw|/PHI_CRIT ) = {c:+.4f}  (~0 = grandezze DIVERSE, confermato)")
# stabilita' nel tempo: variazione relativa per passo di de Broglie vs torsione
r_prev = np.asarray(net.ritmo())[:n]; tau_prev = tau_nodo_torsione(net)[:n]
dvr = []; dvt = []
for _ in range(10):
    net.step()
    r_now = np.asarray(net.ritmo())[:n]; tau_now = tau_nodo_torsione(net)[:n]
    dvr.append(np.median(np.abs(r_now - r_prev) / np.maximum(np.abs(r_prev), 1e-9)))
    dvt.append(np.median(np.abs(tau_now - tau_prev) / np.maximum(np.abs(tau_prev), 1e-9)))
    r_prev, tau_prev = r_now, tau_now
print(f"  variazione relativa/passo:  de Broglie r = {np.median(dvr)*100:.1f}%   torsione tau = {np.median(dvt)*100:.1f}%")
_esito2 = "PIU' STABILE (lenta, giusta per la dilatazione)" if np.median(dvt) < np.median(dvr) else "NON piu' stabile"
print(f"  -> la torsione e' {_esito2} del de Broglie")
