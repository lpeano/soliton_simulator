"""[dev-spinoriale] TEST-GRATIS 3 — materialita' da densita' LENTA (peq) vs rho_spin istantaneo.

Il flip ~10% viene da rho_spin istantaneo (batte col de Broglie). peq (sfondo, evolve con tau_bg)
e' LENTO. Confronto la stabilita' di m_k (e quindi s_k) da rho_spin vs da peq (aggregato a nodo).
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False


def peq_nodo(net, n):
    """peq (per-arco) aggregato a nodo = media sugli archi incidenti."""
    acc = np.zeros(n); deg = np.zeros(n); i, j = net.i, net.j
    pq = net.peq
    mi = i < n; mj = j < n
    fin = np.isfinite(pq)
    np.add.at(acc, i[mi & fin], pq[mi & fin]); np.add.at(deg, i[mi & fin], 1.0)
    np.add.at(acc, j[mj & fin], pq[mj & fin]); np.add.at(deg, j[mj & fin], 1.0)
    return acc / np.maximum(deg, 1.0)


net = sm.Rete(seed=1); net.semina(120)
for _ in range(80):
    net.step()
n = net.n

RHO_C = float(np.median(np.asarray(net._rho_sorgente())[:n]))
PEQ_C = float(np.median(peq_nodo(net, n)))


def sk_rho(net, n):
    rho = np.asarray(net._rho_sorgente())[:n]; m = rho / (rho + RHO_C)
    pc = np.sign(net.perc_chi[:n]).astype(float); pc[pc == 0] = 1.0
    return 1.0 + (pc - 1.0) * m


def sk_peq(net, n):
    pq = peq_nodo(net, n); m = pq / (pq + PEQ_C)
    pc = np.sign(net.perc_chi[:n]).astype(float); pc[pc == 0] = 1.0
    return 1.0 + (pc - 1.0) * m


pr = sk_rho(net, n); pp = sk_peq(net, n)
fr = []; fp = []
for _ in range(20):
    net.step()
    cr = sk_rho(net, n); cp = sk_peq(net, n)
    m = min(len(pr), len(cr), len(pp), len(cp))
    fr.append(np.mean(np.sign(cr[:m]) != np.sign(pr[:m])))
    fp.append(np.mean(np.sign(cp[:m]) != np.sign(pp[:m])))
    pr, pp = cr, cp

print("=== stabilita' materialita': rho_spin istantaneo vs peq (sfondo lento) ===")
print(f"  flip/passo s_k da rho_spin = {np.mean(fr)*100:.1f}%")
print(f"  flip/passo s_k da peq      = {np.mean(fp)*100:.1f}%")
# variazione relativa/passo delle due densita' (chi e' piu' lenta)
rho_p = np.asarray(net._rho_sorgente())[:n]; peq_p = peq_nodo(net, n)
dvr = []; dvp = []
for _ in range(10):
    net.step()
    rho_n = np.asarray(net._rho_sorgente())[:n]; peq_n = peq_nodo(net, n)
    m = min(len(rho_p), len(rho_n), len(peq_p), len(peq_n))
    dvr.append(np.median(np.abs(rho_n[:m]-rho_p[:m])/np.maximum(np.abs(rho_p[:m]),1e-9)))
    dvp.append(np.median(np.abs(peq_n[:m]-peq_p[:m])/np.maximum(np.abs(peq_p[:m]),1e-9)))
    rho_p, peq_p = rho_n, peq_n
print(f"  variazione/passo:  rho_spin = {np.median(dvr)*100:.1f}%   peq = {np.median(dvp)*100:.1f}%")
_win = "peq (lenta) e' PIU' STABILE" if np.mean(fp) < np.mean(fr) else "rho_spin"
print(f"  -> materialita' da {_win}")
