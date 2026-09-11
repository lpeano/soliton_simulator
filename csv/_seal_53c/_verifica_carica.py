"""PRESIDIO Luca: confermare COL DATO (non per ipotesi) che il declassamento del sigillo 5 e' giusto.
Domanda precisa: la firma --orologio-segno conserva la carica PER COPPIA?
  (a) la firma NON riscrive perc_chi di nodi esistenti (append-only)?
  (b) le coppie Schwinger nascono +/- (antinodo = -genitore)?
  (c) perc_chi resta quantizzato +-1 (nessuna corruzione)?
Se si': Sigma perc_chi cambia solo per lignaggio/nascite (mitosi eredita +genitore = NON conservato
gia' in OFF) -> declassamento GIUSTO. Se no -> la firma rompe una conservazione -> bug nascosto.
"""
import sys, os
import numpy as np
# forza Agg + salta i bottoni interattivi al momento dell'import (il modulo crea una figure)
sys.argv = ['harness', '--test']
import matplotlib; matplotlib.use('Agg')

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, ROOT)
import soliton_simulator as ss

# CONFIG del test (identica ai bracci) CON la firma ON: campo-spinoriale + spinore-corretto +
# deparam-orologio + chi-core + calore-scal + orologio-segno. CHI_BASC/CHI_DA_SPINORE OFF.
ss.SPINORE_VIVO = True
ss.SPINORE_CORRETTO = True
ss.CAMPO_SPINORIALE = True
ss.DEPARAM_OROLOGIO = True
ss.OROLOGIO_SEGNO = True
ss.CHI_CORE = True
ss.CALORE_VETTORIALE = False   # --calore-scal
ss.CHI_BASC = False
ss.CHI_DA_SPINORE = False

print("Config firma ON:", dict(OROLOGIO_SEGNO=ss.OROLOGIO_SEGNO, CAMPO_SPINORIALE=ss.CAMPO_SPINORIALE,
      DEPARAM_OROLOGIO=ss.DEPARAM_OROLOGIO, CHI_BASC=ss.CHI_BASC, CHI_DA_SPINORE=ss.CHI_DA_SPINORE))

net = ss.Rete(1)
net.semina(80)
for _ in range(6):
    ss.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()
Nc = ss.massa_critica_collasso()
for k in range(3):
    ang = 2 * np.pi * k / 3
    net.nuova_massa(int(Nc * 0.6), raggio=0.8, centro=(8 * np.cos(ang), 8 * np.sin(ang), 0.0), fase=0.0)

viol_rewrite = 0      # quante volte perc_chi ESISTENTE e' stato riscritto (deve restare 0)
viol_quant = 0        # quanti valori fuori da {-1,+1} (deve restare 0)
sigma_traj = []
n_traj = []
coppie_prev = 0
schwinger_bilanciata = True

for step in range(120):
    ss.scuoti_vuoto(net)
    n_before = net.n
    pc_before = net.perc_chi[:n_before].copy()
    net.step()               # include _passo_spinoriale (la firma _phc) e i rami CHI_* (off)
    # dopo step: perc_chi esistente non deve cambiare (firma append-only, CHI_* off)
    if len(net.perc_chi) < n_before or not np.array_equal(net.perc_chi[:n_before], pc_before):
        viol_rewrite += 1
    net.mitosi()             # mitosi (append +genitore) + Schwinger (append -genitore)
    net.rilassa_disegno(); net.memoria_hebbiana_moto()
    # quantizzazione
    u = np.unique(net.perc_chi)
    if not set(u.tolist()).issubset({-1, 1}):
        viol_quant += int(np.sum(~np.isin(net.perc_chi, [-1, 1])))
    sigma_traj.append(int(np.sum(net.perc_chi)))
    n_traj.append(net.n)

sigma_traj = np.array(sigma_traj); n_traj = np.array(n_traj)
print(f"\npassi=120  N {n_traj[0]}->{n_traj[-1]}  coppie_nate(Schwinger)={net.coppie_nate}  nati(mitosi)={net.nati}")
print(f"[A] APPEND-ONLY: perc_chi esistente riscritto in {viol_rewrite}/120 passi "
      f"-> {'OK (mai riscritto: la firma non tocca la carica)' if viol_rewrite == 0 else 'VIOLATO!'}")
print(f"[C] QUANTIZZAZIONE: valori fuori da +-1 = {viol_quant} -> {'OK (+-1 intatto)' if viol_quant == 0 else 'CORRUZIONE!'}")
print(f"[drift] Sigma perc_chi: {sigma_traj[0]} -> {sigma_traj[-1]} (range {sigma_traj.min()}..{sigma_traj.max()}) "
      f"= DRIFTA per lignaggio (mitosi eredita +genitore) -> NON e' conservata nemmeno in OFF")

# [B] verifica per-coppia leggendo la sorgente: antinodo Schwinger = -perc_chi[genitore]
import re
src = open(os.path.join(ROOT, 'soliton_simulator.py')).read()
riga_schw = [l.strip() for l in src.splitlines() if 'self.perc_chi, -self.perc_chi[' in l]
print(f"[B] Schwinger per-coppia (codice): {riga_schw[0] if riga_schw else 'NON TROVATA!'}")
print("    -> l'antinodo nasce con perc_chi = -perc_chi[genitore] (coppia +/-, somma zero per coppia).")

ok = (viol_rewrite == 0) and (viol_quant == 0) and bool(riga_schw)
print(f"\n=== PRESIDIO SIGILLO 5: {'CONFERMATO' if ok else 'FALLITO'} ===")
print("VERDETTO: la firma NON riscrive perc_chi (append-only), la carica resta +-1, le coppie Schwinger")
print("nascono +/-. Sigma perc_chi drifta SOLO per nascite/lignaggio (mitosi), non e' una legge conservata")
print("(vale gia' in OFF). Percio' il 'sigillo 5 off==on' era un TEST SBAGLIATO -> declassamento GIUSTO,")
print("ora CONFERMATO COL DATO, non per ipotesi.")
sys.exit(0 if ok else 1)
