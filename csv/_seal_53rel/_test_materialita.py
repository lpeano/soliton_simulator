"""[dev-spinoriale] TEST-GRATIS MOD 5.3a corretta — s_k modulato dalla MATERIALITA'.

s_k = 1 + (perc_chi - 1) * m_k ,  m_k = rho_spin / (rho_spin + rho_c)  in [0,1].
- vuoto (rho << rho_c): m->0 -> s_k -> +1 (AVANTI, il vuoto NON inverte);
- materia (rho >> rho_c): m->1 -> s_k -> perc_chi (materia +1, antimateria -1).

VERIFICHE: (1) il vuoto NON inverte (s_k~+1 a rho bassa); (2) la materia segue perc_chi (a rho alta);
(3) stabilita' (basso flip/passo). rho_c = scala di densita' gia' nel sistema (qui: mediana rho_spin, gauge).
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False


def materialita(net, n):
    rho = np.asarray(net._rho_sorgente())[:n]
    rho_c = max(float(np.median(rho)), 1e-9)           # scala di densita' di sistema (gauge)
    return rho / (rho + rho_c), rho, rho_c


def s_k_mat(net, n):
    m, rho, rho_c = materialita(net, n)
    pc = np.sign(net.perc_chi[:n]).astype(float); pc[pc == 0] = 1.0
    return 1.0 + (pc - 1.0) * m, m, pc


net = sm.Rete(seed=1); net.semina(120)
for _ in range(80):
    net.step()
n = net.n
sk, m, pc = s_k_mat(net, n)

vac = m < 0.3          # vuoto/spaziotempo (bassa materialita')
mat = m > 0.7          # materia/antimateria (alta materialita')
print("=== distribuzione materialita' m_k ===")
print(f"  n={n}  m in [{m.min():.2f},{m.max():.2f}]  vuoto(m<0.3): {int(vac.sum())}  materia(m>0.7): {int(mat.sum())}")

print("\n=== (1) il VUOTO non inverte ===")
if vac.any():
    print(f"  s_k medio sul vuoto = {sk[vac].mean():+.3f}  (deve ~+1)   min={sk[vac].min():+.3f}")
    print(f"  frazione s_k>0.9 sul vuoto = {np.mean(sk[vac] > 0.9)*100:.0f}%")
else:
    print("  nessun nodo di vuoto puro (m<0.3) in questa formazione")

print("\n=== (2) la MATERIA segue perc_chi ===")
if mat.any():
    agree = np.mean(np.sign(sk[mat]) == pc[mat]) if np.any(pc[mat] != 0) else float('nan')
    print(f"  nodi materia: {int(mat.sum())}   accordo sign(s_k)==perc_chi = {agree*100:.0f}%")
    print(f"  su antimateria-materia (perc_chi=-1, m>0.7): s_k medio = {sk[mat & (pc<0)].mean() if np.any(mat&(pc<0)) else float('nan'):+.3f}  (deve ~-1)")
    print(f"  su materia (perc_chi=+1, m>0.7): s_k medio = {sk[mat & (pc>0)].mean() if np.any(mat&(pc>0)) else float('nan'):+.3f}  (deve ~+1)")
else:
    print("  nessun nodo materia (m>0.7): formazione poco densa; abbasso soglia a m>0.6")
    mat2 = m > 0.6
    if mat2.any():
        agree = np.mean(np.sign(sk[mat2]) == pc[mat2])
        print(f"  (m>0.6) nodi={int(mat2.sum())} accordo sign(s_k)==perc_chi = {agree*100:.0f}%")

print("\n=== (3) STABILITA' ===")
prev = np.sign(s_k_mat(net, n)[0]); flips = []
for _ in range(20):
    net.step()
    cur = np.sign(s_k_mat(net, n)[0])
    flips.append(np.mean(cur != prev)); prev = cur
print(f"  flip/passo sign(s_k) = {np.mean(flips)*100:.1f}%  ({'STABILE' if np.mean(flips)<0.05 else 'instabile'})")

print("\n=== ESITO ===")
vac_ok = (not vac.any()) or (sk[vac].mean() > 0.9)
mat_ok = True
print(f"  vuoto neutro (s_k~+1): {'OK' if vac_ok else 'NO'}")
print(f"  materia segue perc_chi: vedi (2)")
