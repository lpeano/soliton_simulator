"""[dev-spinoriale] TEST-GRATIS 2 — stabilita' di s_k materialita' con rho_c FISSO (no media globale).

Il flip 11.5% col rho_c=median(rho_spin) sospetto sia (a) media globale fluttuante (viola il principio),
(b) sign-flip benigno a s_k~0 (nodi congelati, dt_n_s~0, impatto dinamico nullo). Verifico entrambi:
usa rho_c FISSO (costante catturata una volta) e misura i flip pesati per |s_k| e la loro |s_k|.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False

net = sm.Rete(seed=1); net.semina(120)
for _ in range(80):
    net.step()
n = net.n

# rho_c FISSO catturato una volta (costante di sistema, NON media per-passo)
rho0 = np.asarray(net._rho_sorgente())[:n]
RHO_C = float(np.median(rho0))     # catturato una volta -> costante nel tempo


def s_k_fisso(net, n):
    rho = np.asarray(net._rho_sorgente())[:n]
    m = rho / (rho + RHO_C)
    pc = np.sign(net.perc_chi[:n]).astype(float); pc[pc == 0] = 1.0
    return 1.0 + (pc - 1.0) * m


prev = s_k_fisso(net, n)
flips = []; flips_forti = []; abs_at_flip = []
for _ in range(20):
    net.step()
    cur = s_k_fisso(net, n)
    m = min(len(prev), len(cur))
    fl = np.sign(cur[:m]) != np.sign(prev[:m])
    flips.append(np.mean(fl))
    # flip "forti" = quelli su nodi con |s_k| significativo (impatto dinamico reale)
    forte = fl & (np.abs(cur[:m]) > 0.3)
    flips_forti.append(np.mean(forte))
    if fl.any():
        abs_at_flip.append(np.median(np.abs(cur[:m][fl])))
    prev = cur

print("=== STABILITA' con rho_c FISSO (costante di sistema) ===")
print(f"  flip/passo sign(s_k)            = {np.mean(flips)*100:.1f}%  (vs 11.5% con median per-passo)")
print(f"  flip/passo FORTI (|s_k|>0.3)    = {np.mean(flips_forti)*100:.1f}%  (impatto dinamico reale)")
print(f"  |s_k| mediano ai nodi che flippano = {np.median(abs_at_flip) if abs_at_flip else float('nan'):.3f}  (~0 = congelati, benigni)")
print()
if np.mean(flips_forti) < 0.03:
    print("  ESITO: i flip sono BENIGNI (concentrati a s_k~0 = nodi congelati, dt_n_s~0).")
    print("         rho_c FISSO (non media per-passo) e' la scelta giusta: piu' stabile E rispetta 'media non va nelle leggi locali'.")
else:
    print("  ESITO: flip forti non trascurabili -> serve smorzamento o rho_c diverso.")
