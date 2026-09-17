# -*- coding: utf-8 -*-
"""ANALISI TW — legge i .pkl gia' prodotti da _misura_tw.py. NESSUN RUN NUOVO.

SOLO ASCII: l'UnicodeEncodeError su cp1252 ha gia' ucciso tre script (par.9, terza volta).

LA DOMANDA E' TRASVERSALE, non temporale (presidio par.9): si confrontano, ALLO STESSO ISTANTE e
DENTRO LO STESSO RUN, tre grandezze:
  (a) l'angolo DICHIARATO dal commento          tw/2                      [rad per passo]
  (b) il termine CODIFICATO (:2149)             tw/(4 pi)                 [entra in omega_s]
  (c) l'angolo che (b) produce davvero          tw/(4 pi) * dt_n          [rad per passo]
Non si confrontano due run: OFF e ON hanno 2849 e 3047 nodi, cioe' il confronto punto-a-punto
NON ESISTE (par.9, trappola del "max|A-B| = 0.000e+00").
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import os
import pickle
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
import soliton_simulator as S   # solo per DT, PHI_CRIT, TAU_A: nessun run

A = pickle.load(open(os.path.join(HERE, "_tw_off.pkl"), "rb"))["attrs"]
B = pickle.load(open(os.path.join(HERE, "_tw_on.pkl"), "rb"))["attrs"]
nA = len(np.asarray(A["pos"])); nB = len(np.asarray(B["pos"]))

print("=" * 92)
print("ANALISI TW  --  150 passi, seme 1, --cs-dinamico ACCESO.  DT = %g, PHI_CRIT = %.6f"
      % (S.DT, S.PHI_CRIT))
print("=" * 92)

print("\n--- A. CONTROLLO POSITIVO: il flag FA QUALCOSA? ---")
print("  nodi OFF %d   ON %d   -> DIVERGONO (differenza %d nodi, %.1f%%)"
      % (nA, nB, nB - nA, 100.0 * (nB - nA) / nA))
print("  Il flag NON e' codice morto. Ma ATTENZIONE: shape diverse = il confronto punto-a-punto")
print("  NON ESISTE, quindi da qui NON si legge 'di quanto' cambia omega. Si legge solo CHE cambia.")

tw = np.asarray(B["tw"], float)
om = np.linalg.norm(np.asarray(B["omega_s"], float), axis=1)
omA = np.linalg.norm(np.asarray(A["omega_s"], float), axis=1)
atw = np.abs(tw)
twh = atw / (2.0 * S.PHI_CRIT)          # il `_twh` del codice, in modulo

print("\n--- C. LA LEGGE CODIFICATA CONTRO QUELLA DICHIARATA (dentro il SOLO run ON) ---")
print("  archi                                  : %d" % atw.size)
print("  |tw| mediana                           : %.6e  rad" % np.median(atw))
print("  (a) DICHIARATO  angolo/passo = tw/2    : %.6e  rad   <- 'pilota il Bloch di tw/2'" % np.median(atw / 2.0))
print("  (b) CODIFICATO  termine = tw/(4 pi)    : %.6e        <- sommato a omega_new (:2149-2154)" % np.median(twh))
print("  (c) angolo che (b) produce = (b)*dt_n  : %.6e  rad   (dt_n mediano = DT, perche' median(r)=1" % (np.median(twh) * S.DT))
print("                                                         ESATTO per costruzione, presidio P4)")
print("  RAPPORTO (a)/(c) = 2 pi / DT           : %.4g" % (2.0 * np.pi / S.DT))
print("""
  LETTURA: (a) e (c) differiscono di un fattore 2 pi/DT. Il commento descrive un ANGOLO, il codice
  somma il numero a una VELOCITA' ANGOLARE (theta = |omega|*dt, :2210 e :2296). Non e' una
  riformulazione: sono due leggi diverse, e quella che gira e' (c).""")

print("\n--- D. E DOVE FINISCE: MEMORIA, non rotazione istantanea ---")
print("  Il risultato va in self.omega_s (:2313), cioe' nella MEMORIA persistente, dove ogni passo")
print("  riceve +tw/(4 pi) e perde -omega_s/tau. All'equilibrio quel termine da solo vale")
print("  omega_tw = tw/(4 pi) * tau/dt_n, cioe' AMPLIFICATO di tau/dt_n.")
tau_su_dt = S.TAU_A * 0.05 / S.DT
print("  tau/dt_n al PAVIMENTO (TAU_A*0.05/DT, par.9)   : %.4g passi" % tau_su_dt)
print("  omega_tw d'equilibrio al pavimento             : %.6e" % (np.median(twh) * tau_su_dt))
print("  |omega_s| mediana MISURATA nel run ON          : %.6e" % np.median(om))
print("  |omega_s| mediana MISURATA nel run OFF         : %.6e" % np.median(omA))
print("  peso del termine TW sul totale (equilibrio/misurato) : %.4g" % (
    np.median(twh) * tau_su_dt / max(np.median(om), 1e-300)))

print("""
  CONFRONTO CHE RENDE IL PUNTO NON-TEORICO: il commento di SYNC_SPINORE (:724, :2157-2160) dice che
  il torque di allineamento entra in omega_tot e NON in omega_s perche' la memoria 'darebbe
  accumulo/divergenza'. TW_SPINORE fa ESATTAMENTE cio' che quel commento dichiara divergente.
  E, unico fra i termini del blocco, _otw NON e' diviso per l'inerzia.""")

psp = np.asarray(B["_psi_spinor"])
nor = np.linalg.norm(psp, axis=1)
fin = all(np.all(np.isfinite(v)) for v in B.values()
          if isinstance(v, np.ndarray) and v.dtype != object and np.issubdtype(v.dtype, np.number))
print("\n--- stabilita' col flag ON (NON e' un sigillo: e' un controllo minimo) ---")
print("  max| |psi| - 1 | = %.3e su %d nodi" % (np.max(np.abs(nor - 1.0)), nor.size))
print("  nessun NaN/inf in tutto lo stato : %s" % fin)
print("  max|x| = %.4g" % np.max(np.abs(np.asarray(B["pos"], float))))
print("=" * 92)
