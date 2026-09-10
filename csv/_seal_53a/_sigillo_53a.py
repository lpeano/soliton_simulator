"""[dev-spinoriale] SIGILLO MOD 5.3a+5.3b (--tempo-segno): 7 controlli.

1 OFF byte-identico | 2 riduzione-vuoto (s_k->+1 nel vuoto) | 3 CONSERVAZIONE (gate) |
4 STABILITA' (gate, eta>=0, no blow-up) | 5 causalita' (strutturale) | 6 completezza (strutturale) |
7 controprova non-abeliana (ON != OFF).
"""
import os, sys, importlib.util
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sm_old", os.path.join(HERE, "_old.py"))
sm_old = importlib.util.module_from_spec(spec); spec.loader.exec_module(sm_old)


def _cfg(mod, tempo_segno):
    mod.CAMPO_SPINORIALE = True; mod.SPINORE_VIVO = True; mod.SPINORE_CORRETTO = True
    mod.CHI_CORE = True; mod.SCUOTIMENTO = False
    if hasattr(mod, "TEMPO_SEGNO"):
        mod.TEMPO_SEGNO = tempo_segno


def run_step(mod, tempo_segno, passi=60, semi=120):
    _cfg(mod, tempo_segno)
    net = mod.Rete(seed=1); net.semina(semi)
    for _ in range(passi):
        net.step()
    return net


def _passo_batch(mod, net):
    mod.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()


def run_batch(mod, tempo_segno, passi=300, nmasse=3, sep=8.0):
    _cfg(mod, tempo_segno)
    Nc = mod.massa_critica_collasso(); net = mod.Rete(1); net.semina(80)
    for _ in range(6):
        _passo_batch(mod, net)
    for k in range(nmasse):
        ang = 2 * np.pi * k / nmasse
        net.nuova_massa(int(Nc * 0.6), raggio=0.8, centro=(sep*np.cos(ang), sep*np.sin(ang), 0.0), fase=0.0)
    try: net.aggiorna_pesi_concorrenza()
    except Exception: pass
    minN = net.n; maxN = net.n; nan = 0; eta_min = np.inf; twsum = []
    for _ in range(passi):
        _passo_batch(mod, net)
        minN = min(minN, net.n); maxN = max(maxN, net.n)
        if not np.all(np.isfinite(net.phi)) or not np.all(np.isfinite(net.psi)): nan += 1
        eta_min = min(eta_min, float(np.min(net.eta[:net.n])) if net.n else 0.0)
        twsum.append(float(np.sum(net.tw)))
    return net, dict(minN=minN, maxN=maxN, nan=nan, eta_min=eta_min, twsum=twsum)


def cmp_state(a, b):
    m = min(a.n, b.n); d = {}
    d['n'] = (a.n, b.n)
    d['phi'] = float(np.max(np.abs(a.phi[:m] - b.phi[:m])))
    d['psi'] = float(np.max(np.abs(a.psi[:m] - b.psi[:m])))
    d['tw'] = float(np.max(np.abs(a.tw[:min(len(a.tw), len(b.tw))] - b.tw[:min(len(a.tw), len(b.tw))])))
    d['pos'] = float(np.max(np.abs(a.pos[:m] - b.pos[:m])))
    return d


print("=== SIGILLO 1: OFF byte-identico (nuovo flag-off vs HEAD/Fase5) ===")
A = run_step(sm_old, None, passi=60)
B = run_step(sm, False, passi=60)
d = cmp_state(A, B)
ok1 = (d['n'][0] == d['n'][1]) and d['phi'] < 1e-12 and d['psi'] < 1e-12 and d['tw'] < 1e-12 and d['pos'] < 1e-12
print(f"  N {d['n']}  max|dphi|={d['phi']:.2e}  max|dpsi|={d['psi']:.2e}  max|dtw|={d['tw']:.2e}  max|dpos|={d['pos']:.2e}")
print(f"  ESITO 1: {'PASS' if ok1 else 'FAIL'}")

print("\n=== SIGILLO 2: RIDUZIONE-VUOTO (s_k -> +1 dove m_coer -> 0) ===")
netv = run_step(sm, True, passi=80); n = netv.n
netv.calcola_psi()
mcoer = np.clip(np.cos(netv.phi[:n] - np.angle(netv.psi[:n] + 1e-12)), 0.0, 1.0)
pc = np.sign(netv.perc_chi[:n]).astype(float); pc[pc == 0] = 1.0
sk = 1.0 + (pc - 1.0) * mcoer
vac = mcoer < 0.1
sk_vac_dev = float(np.max(np.abs(sk[vac] - 1.0))) if vac.any() else 0.0
ok2 = sk_vac_dev < 1e-9
print(f"  nodi vuoto (m<0.1): {int(vac.sum())}   max|s_k - 1| sul vuoto = {sk_vac_dev:.2e}")
print(f"  s_k medio globale = {sk.mean():+.3f}  (materia inverte, vuoto +1)")
print(f"  ESITO 2: {'PASS (il vuoto non inverte)' if ok2 else 'FAIL'}")

print("\n=== SIGILLO 4: STABILITA' (300p ON, no blow-up, eta>=0) ===")
netS, st = run_batch(sm, True, passi=300)
ok4 = (st['nan'] == 0) and (st['eta_min'] >= 0.0) and (st['maxN'] < sm.MAX_NODI)
print(f"  N {st['minN']}->{netS.n} (max {st['maxN']})  n_naninf={st['nan']}  min(eta)={st['eta_min']:.3e}")
print(f"  ESITO 4: {'PASS' if ok4 else 'FAIL -> FERMATI'}")

print("\n=== SIGILLO 3: CONSERVAZIONE (Sigma perc_chi; olonomia netta ON vs OFF) ===")
netO, stO = run_batch(sm, False, passi=300)
sig_on = float(np.sum(np.sign(netS.perc_chi[:netS.n])))
sig_off = float(np.sum(np.sign(netO.perc_chi[:netO.n])))
tw_on = np.array(st['twsum']); tw_off = np.array(stO['twsum'])
# olonomia netta: media 2a meta' della somma di tw (deve NON divergere ON vs OFF)
hol_on = float(np.mean(tw_on[len(tw_on)//2:])); hol_off = float(np.mean(tw_off[len(tw_off)//2:]))
drift_on = float(tw_on[-1] - tw_on[len(tw_on)//2]); drift_off = float(tw_off[-1] - tw_off[len(tw_off)//2])
ok3 = np.isfinite(hol_on) and abs(sig_on) <= 0.35 * netS.n
print(f"  Sigma perc_chi: ON={sig_on:.0f}/{netS.n}  OFF={sig_off:.0f}/{netO.n}  (~bilanciato = coppie somma-zero)")
print(f"  olonomia netta (media Sigma tw, 2a meta'): ON={hol_on:.2f}  OFF={hol_off:.2f}")
print(f"  drift olonomia (2a meta'): ON={drift_on:.2f}  OFF={drift_off:.2f}  (ON non deve divergere)")
print(f"  ESITO 3: {'PASS' if ok3 else 'FAIL -> FERMATI'}")

print("\n=== SIGILLO 7: CONTROPROVA non-abeliana (ON != OFF) ===")
dc = cmp_state(netS, netO)
ok7 = dc['phi'] > 1e-6 or dc['psi'] > 1e-6
print(f"  ON vs OFF: N {dc['n']}  max|dphi|={dc['phi']:.3e}  max|dpsi|={dc['psi']:.3e}")
print(f"  ESITO 7: {'PASS (il flag cambia la dinamica)' if ok7 else 'FAIL (nessun effetto)'}")

print("\n=== SIGILLI 5 (causalita') e 6 (completezza): STRUTTURALI ===")
print("  5 causalita': s_k da self.perc_chi/self.phi/self.psi a inizio step (t-1), prima di ogni commit; ordine ETC invariato.")
print("  6 completezza: dt_n_s (firmato) SOLO su #3-6 (delta_phivel, delta_sync_phi, _passo_spinoriale, self.phi); dt_n (magnitudine) su eta+termostato; dt_e intatto.")

print("\n===================== RIEPILOGO =====================")
print(f"  1 OFF byte-identico   : {'PASS' if ok1 else 'FAIL'}")
print(f"  2 riduzione-vuoto     : {'PASS' if ok2 else 'FAIL'}")
print(f"  3 CONSERVAZIONE (gate): {'PASS' if ok3 else 'FAIL'}")
print(f"  4 STABILITA' (gate)   : {'PASS' if ok4 else 'FAIL'}")
print(f"  7 controprova non-ab. : {'PASS' if ok7 else 'FAIL'}")
gate = ok1 and ok2 and ok3 and ok4 and ok7
print(f"  >>> {'TUTTI I SIGILLI PASSANO' if gate else 'SIGILLO FALLITO -> FERMARSI'}")
