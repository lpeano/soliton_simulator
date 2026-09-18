# -*- coding: utf-8 -*-
"""SIGILLO DEL DRIVER VIDEO -- **il rendering scrive sullo stato?** VERIFICATO, non dedotto.

IL RILIEVO: il driver `_scena_video.py` omette cio' che `update()` chiama per DISEGNARE
(`diagnostica`, `campo_spaziale`, `pozzo_grafo`, `intensita`). Avevo concluso *«il rendering non e'
fisica»*: **e' una DEDUZIONE**, e il precedente di `lambda_vuoto` (che sembrava di sola lettura e
chiamava `calcola_psi()`, che SCRIVE `self.psi`) dice che non basta.

LA LETTURA DEL SORGENTE dice questo, ed e' il PUNTO DI PARTENZA, non la prova:
  campo_spaziale (:4097-4153) scrive `self._r3`, `self._r3_G`, `self._ker_cache` -- letti SOLO da
                              se' stessa (:4115-4125) e azzerati a :2913: cache di RENDERING.
  pozzo_grafo    (:4214-4236) nessuna scrittura su `self`.
  intensita      (:2742-2744) nessuna scrittura su `self`.
  diagnostica    (:4451-4879) chiama `lambda_nodi`, `intensita`, `_pesi`, `_mat`. `_pesi` e' PURA
                              (legge eta/d/tw). `lambda_nodi` scrive solo `_calcolo_schermatura`,
                              messo True e rimesso False: guardia di rientranza, effetto netto nullo.
  ⚠ E il commento a :7168 -- *«le funzioni diagnostiche aggiornano cache che la DINAMICA legge»* --
    riguarda **`_diag_completa`** (:6255, che chiama `net.calcola_psi()` e `net.ritmo()`), **NON**
    `net.diagnostica()`. **Sono due funzioni diverse, e il batch protegge la PRIMA.**

LA PROVA: due run IDENTICI di N frame, uno SOLO-FISICA e uno che chiama ANCHE le quattro funzioni
di disegno a ogni frame, **nello stesso ordine di `update()`**. Poi si confronta lo stato.
  max|A-B| = 0.000e+00 CON SHAPE UGUALI -> il rendering NON tocca la fisica: il driver E' equivalente.
  differenza != 0, o shape diverse     -> NON e' equivalente: si dichiara quale e si corregge.
⚠ LA RIGA DELLE SHAPE SI STAMPA PER PRIMA: `max|A-B| = 0` puo' significare NESSUN CONFRONTO.
ASCII PURO.
"""
import os
import pickle
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
QUI = os.path.dirname(os.path.abspath(__file__))
NF = 12
DRV = os.path.join("csv", "_test_fork", "_scena_video.py")

print("=" * 112)
print("SIGILLO DRIVER VIDEO -- il rendering scrive sullo stato? %d frame per braccio" % NF)
print("=" * 112)

esiti = []
for modo, dest in (("fisica", "_sig_drv_A"), ("fedele", "_sig_drv_B")):
    d = os.path.join("csv", "_seal_fork", dest)
    print("\n  braccio %-8s -> %s" % (modo, d))
    r = subprocess.run([sys.executable, DRV, str(NF), d, str(NF), modo],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("    FALLITO (%d):\n%s" % (r.returncode, (r.stderr or r.stdout)[-1500:]))
        sys.exit(1)
    for ln in r.stdout.splitlines():
        if "frame" in ln and "n=" in ln:
            print("    " + ln.strip()[:100])
    esiti.append(os.path.join(d, "frame_%d.pkl" % NF))

A = pickle.load(open(esiti[0], "rb"))["attrs"]
B = pickle.load(open(esiti[1], "rb"))["attrs"]
nA = len(A["pos"]); nB = len(B["pos"])
print("\n--- IL CONFRONTO -- la riga delle SHAPE per PRIMA ---")
print("    n: %d contro %d" % (nA, nB))
campi = ["psi", "phi", "phivel", "eta", "d", "d0", "tw", "omega_s", "_nb", "psi_spin",
         "_psi_spinor", "_psi_prec", "perc_chi", "pos"]
mx = 0.0; diverse = 0; conf = 0
for c in campi:
    a = np.asarray(A.get(c, np.zeros(0))); b = np.asarray(B.get(c, np.zeros(0)))
    if a.shape != b.shape:
        diverse += 1
        print("      %-13s SHAPE DIVERSE %s contro %s  <- NESSUN CONFRONTO" % (c, a.shape, b.shape))
        continue
    conf += 1
    v = float(np.max(np.abs(a - b))) if a.size else 0.0
    mx = max(mx, v)
    print("      %-13s shape %-14s max|A-B| = %.3e" % (c, str(a.shape), v))

ok = (diverse == 0) and (conf >= 10) and (mx == 0.0)
print("\n  [%s] shape divergenti %d, array confrontati %d, max|A-B| = %.3e"
      % ("PASS" if ok else "FAIL", diverse, conf, mx))
print("""
  COME SI LEGGE -- fissato PRIMA:
    0.000e+00 CON SHAPE UGUALI su >= 10 array -> il rendering NON tocca la fisica: il driver E'
                                                 EQUIVALENTE, e lo si dichiara CON QUESTA VERIFICA
                                                 accanto, non con l'argomento 'non e' fisica'.
    differenza != 0 o shape diverse           -> NON equivalente: si dichiara QUALE funzione e si
                                                 corregge il driver chiamandola.""")
print("=" * 112)
sys.exit(0 if ok else 2)
