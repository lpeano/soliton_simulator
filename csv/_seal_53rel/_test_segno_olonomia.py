"""[dev-spinoriale] TEST-GRATIS MOD 5.3a — segno dalla STORIA (olonomia da twist) vs perc_chi.

s_k(tw)  = sign(cos(Theta_k/2)), Theta_k = twist accumulato per-nodo (media firmata archi incidenti).
           Fisica: tw=0->+1 (materia), tw=2pi->-1 (antimateria), tw=4pi->+1 (winding completo).
s_k(chi) = perc_chi (Z2 ereditato: antinodo nasce perc_chi=-perc_chi[genitore]).

3 proprieta': (i) +1 nel limite puro, (ii) stabile (basso flip/passo), (iii) distingue mat/antimat.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True; sm.SPINORE_CORRETTO = True; sm.CHI_CORE = True
sm.SCUOTIMENTO = False


def tw_nodo(net):
    """twist accumulato per-nodo = media FIRMATA di self.tw sugli archi incidenti."""
    n = net.n; i, j = net.i, net.j
    acc = np.zeros(n); deg = np.zeros(n)
    mi = i < n; mj = j < n
    np.add.at(acc, i[mi], net.tw[mi]); np.add.at(acc, j[mj], net.tw[mj])
    np.add.at(deg, i[mi], 1.0);        np.add.at(deg, j[mj], 1.0)
    return acc / np.maximum(deg, 1.0)


def sk_tw(net, n):
    return np.where(np.cos(tw_nodo(net)[:n] / 2.0) >= 0.0, 1.0, -1.0)


def sk_chi(net, n):
    pc = np.sign(net.perc_chi[:n]).astype(float); pc[pc == 0] = 1.0
    return pc


# ===== (1a) LIMITE PURO: tw=0 =====
net = sm.Rete(seed=1); net.semina(120)
sm.CAMPO_SPINORIALE = False
for _ in range(40):
    net.step()
sm.CAMPO_SPINORIALE = True
n = net.n
net.tw = np.zeros(len(net.tw))
s = sk_tw(net, n)
print("=== (1a) LIMITE PURO tw=0 ===")
print(f"  s_k(tw)=sign(cos(0)) : +1 su {int((s>0).sum())}/{n}   {'PASS' if np.all(s>0) else 'FAIL'}")

# ===== (1b) STATO SEAL in-fase (byte-identity gate reale): tw effettivo =====
net = sm.Rete(seed=1); net.semina(120)
sm.CAMPO_SPINORIALE = False
for _ in range(40):
    net.step()
sm.CAMPO_SPINORIALE = True
n = net.n
stw = sk_tw(net, n); schi = sk_chi(net, n)
print("\n=== (1b) STATO SEAL in-fase (gate byte-identity: quanti +1?) ===")
print(f"  s_k(tw)  : +1 su {int((stw>0).sum())}/{n}   (se non 120 -> rompe byte-identity nel seal)")
print(f"  perc_chi : +1 su {int((schi>0).sum())}/{n}")
print(f"  |tw_nodo| mediano nel seal = {np.median(np.abs(tw_nodo(net)[:n])):.3f}")

# ===== (2) STABILITA' + (3) corrispondenza perc_chi, fuori dal limite =====
net = sm.Rete(seed=1); net.semina(120)
for _ in range(60):
    net.step()
n = net.n
ptw = sk_tw(net, n); pchi = sk_chi(net, n)
ftw = []; fchi = []; agree = []
for _ in range(20):
    net.step()
    a = sk_tw(net, n); b = sk_chi(net, n)
    ftw.append(np.mean(a != ptw)); fchi.append(np.mean(b != pchi))
    agree.append(np.mean(a == b))
    ptw, pchi = a, b
print("\n=== (2) STABILITA' fuori dal limite (n={}) ===".format(n))
print(f"  s_k(tw)  flip/passo = {np.mean(ftw)*100:.1f}%   ({'STABILE' if np.mean(ftw)<0.05 else 'instabile'})")
print(f"  perc_chi flip/passo = {np.mean(fchi)*100:.1f}%   ({'STABILE' if np.mean(fchi)<0.05 else 'instabile'})")
print("\n=== (3) s_k(tw) coincide con perc_chi (materia/antimateria)? ===")
print(f"  accordo sign(cos(tw/2)) == perc_chi : {np.mean(agree)*100:.1f}%")
a = sk_tw(net, n); b = sk_chi(net, n)
print(f"  distribuzione s_k(tw):  +1 {int((a>0).sum())}/{n}  -1 {int((a<0).sum())}/{n}")
print(f"  distribuzione perc_chi: +1 {int((b>0).sum())}/{n}  -1 {int((b<0).sum())}/{n}")

# ===== (4) perc_chi vede l'antimateria (Z2 ereditato), indipendente dalla fase de Broglie =====
print("\n=== (4) perc_chi come s_k: le 3 proprieta' ===")
print(f"  (i)   limite: perc_chi +1 nel seal? {int((schi>0).sum())}/{n}  ({'tutto +1' if np.all(schi>0) else 'misto -> vedi (1b)'})")
print(f"  (ii)  stabile: flip/passo = {np.mean(fchi)*100:.1f}%")
print(f"  (iii) discreto Z2 ereditato dalle coppie (antinodo=-genitore) per costruzione = SI (non da fase de Broglie)")
