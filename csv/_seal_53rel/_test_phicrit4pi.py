"""[dev-spinoriale] TEST-GRATIS 5.3c — PHI_CRIT=4pi soffoca la mitosi nel sistema spinoriale?

REPERTO da temere (commento riga 276-280 + logica mitosi righe 2582-2644): soglia0=PHI_CRIT e il
tetto TW_TETTO=4pi e' FISSO. Con PHI_CRIT=4pi la finestra di mitosi [soglia, tetto]=[4pi,4pi]
collassa -> la mitosi potrebbe non scattare MAI.

DOMANDA: nel sistema spinoriale Fase 5 (mitosi su rho_spin), con PHI_CRIT=4pi la mitosi scatta ancora?
MISURA: crescita di N con il VERO passo batch (scuoti_vuoto; step; mitosi; rilassa; hebb) e masse
seminate in cerchio (come --nmasse 3 --sep 8), PHI_CRIT=2pi (baseline) vs 4pi.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True
sm.SPINORE_CORRETTO = True
sm.CHI_CORE = True
sm.SCUOTIMENTO = False   # deterministico


def _passo(net):
    sm.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()


def run_N(phi_crit, passi=300, nmasse=3, sep=8.0):
    sm.PHI_CRIT = phi_crit
    Nc = sm.massa_critica_collasso()
    net = sm.Rete(1)
    net.semina(80)
    for _ in range(6):
        _passo(net)
    for k in range(nmasse):
        ang = 2 * np.pi * k / nmasse
        cx, cy = sep * np.cos(ang), sep * np.sin(ang)
        net.nuova_massa(int(Nc * 0.6), raggio=0.8, centro=(cx, cy, 0.0), fase=0.0)
    try:
        net.aggiorna_pesi_concorrenza()
    except Exception:
        pass
    n0 = net.n
    traccia = [net.n]
    for k in range(passi):
        _passo(net)
        if (k + 1) % 50 == 0:
            traccia.append(net.n)
    return n0, net.n, traccia


PI = np.pi
print("=== TEST-GRATIS 5.3c: mitosi con PHI_CRIT=2pi vs 4pi (sistema spinoriale Fase 5) ===\n")

n0a, nfa, tra = run_N(2 * PI)
print(f"PHI_CRIT=2pi  N: {n0a} -> {nfa}  (x{nfa/max(n0a,1):.2f})   traccia@50: {tra}")

n0b, nfb, trb = run_N(4 * PI)
print(f"PHI_CRIT=4pi  N: {n0b} -> {nfb}  (x{nfb/max(n0b,1):.2f})   traccia@50: {trb}")

print("\n=== ESITO ===")
cresc_2 = nfa - n0a
cresc_4 = nfb - n0b
print(f"  crescita 2pi = +{cresc_2}   crescita 4pi = +{cresc_4}")
if cresc_2 <= 0:
    print("  ATTENZIONE: baseline 2pi non innesca mitosi -> test inconcludente, rivedere config")
elif cresc_4 <= 0:
    print("  4pi SOFFOCA la mitosi (N non cresce) -> FERMARSI, applicare 4pi solo dove tocca la doppia copertura")
elif cresc_4 < 0.3 * cresc_2:
    print(f"  4pi DEPRIME la mitosi (crescita {cresc_4/max(cresc_2,1):.0%} del baseline) -> valutare con Luca")
else:
    print(f"  4pi mantiene la mitosi ({cresc_4/max(cresc_2,1):.0%} del baseline) -> si puo' procedere con 5.3c globale")
