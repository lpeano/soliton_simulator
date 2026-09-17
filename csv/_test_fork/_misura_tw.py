# -*- coding: utf-8 -*-
"""MISURA TW — che cosa fa DAVVERO `--tw-spinore`, prima di scriverne il sigillo.

PERCHE' ESISTE: par.9, «un criterio di sigillo si scrive da una MISURA, non dal proprio modello
mentale» (tre criteri stale in un giorno, tutti FALSE FAIL). E par.0-ter P1: se un fatto misurato
contraddice la descrizione della legge, si SEGNALA, non si esegue.

LA DOMANDA, in tre parti, tutte decidibili dai NUMERI:
  A. CONTROLLO POSITIVO: ON e OFF differiscono? su quanti nodi? di quanto?
  B. RIDUZIONE AL LIMITE: con `tw = 0` il contributo e' ESATTAMENTE zero?
  C. LA LEGGE CODIFICATA E' QUELLA DICHIARATA? Il commento dice «la torsione pilota il Bloch di
     tw/2», cioe' un ANGOLO. Il codice (:2149-2154) somma `tw/(4 pi)` a `omega_new`, che e' una
     VELOCITA' angolare (`theta = |omega|*dt`, :2210), e il risultato finisce in `self.omega_s`
     (:2313), la MEMORIA persistente. Se e' cosi', la rotazione per passo non e' `tw/2` ma
     `(tw/4pi)*dt_n`, e all'equilibrio del rilassamento `-omega_s/tau` vale `(tw/4pi)*tau/dt_n`.
     QUI SI MISURA IL RAPPORTO, non si argomenta.
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
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SIM = os.path.join(ROOT, "soliton_simulator.py")
PY = sys.executable
PASSI = int(sys.argv[1]) if len(sys.argv) > 1 else 150
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", str(PASSI),
        "--ogni", str(PASSI), "--db-ogni", str(PASSI),
        "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
        "--calore-scal", "--deparam-orologio", "--verlet",
        "--fork-su2", "--fork-su2-mem", "--cs-dinamico"]   # par.4: --cs-dinamico CI VA SEMPRE


def run(tag, extra=()):
    db = os.path.join(HERE, "_tw_%s.pkl" % tag)
    cmd = [PY, SIM] + BASE + list(extra) + ["--csv", db + ".cond.csv",
                                            "--sync-db", db, "--db-cleanup"]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:]); print("STDERR:", r.stderr[-2000:])
        raise SystemExit("run FALLITO: " + tag)
    with open(db, "rb") as f:
        return pickle.load(f)["attrs"]


print("=" * 96)
print("MISURA TW — %d passi, seme 1, --cs-dinamico ACCESO" % PASSI)
print("=" * 96)
A = run("off")
B = run("on", ["--tw-spinore"])

nA = len(np.asarray(A.get("pos"))); nB = len(np.asarray(B.get("pos")))
print("\nnodi:  OFF %d   ON %d" % (nA, nB))
if nA != nB:
    print("  ⚠ SHAPE DIVERSE: il confronto punto-a-punto NON esiste (par.9). Si legge solo")
    print("    il fatto che ON e OFF DIVERGONO, non di quanto per nodo.")

# ---- A. CONTROLLO POSITIVO -------------------------------------------------------------------
oA = np.asarray(A.get("omega_s"), float); oB = np.asarray(B.get("omega_s"), float)
k = min(len(oA), len(oB))
d = np.linalg.norm(oB[:k] - oA[:k], axis=1)
mA = np.linalg.norm(oA[:k], axis=1)
print("\n--- A. CONTROLLO POSITIVO (ON vs OFF, primi %d nodi) ---" % k)
print("  nodi con |d omega| > 1e-13 : %d / %d  (%.1f%%)" % ((d > 1e-13).sum(), k,
                                                            100.0 * (d > 1e-13).sum() / max(k, 1)))
print("  |d omega| mediana          : %.6e" % float(np.median(d)))
print("  |omega| mediana OFF        : %.6e" % float(np.median(mA)))

# ---- C. LA LEGGE CODIFICATA CONTRO QUELLA DICHIARATA ------------------------------------------
tw = np.asarray(B.get("tw"), float)
print("\n--- C. LA LEGGE CODIFICATA CONTRO QUELLA DICHIARATA ---")
if tw.size:
    twh = np.abs(tw) / (2.0 * 2.0 * np.pi)            # il `_twh` del codice, in modulo
    print("  |tw| mediana                        : %.6e   (PHI_CRIT = 2pi = %.6f)" % (
        float(np.median(np.abs(tw))), 2 * np.pi))
    print("  |tw|/(4pi) mediana  [= il termine]  : %.6e" % float(np.median(twh)))
    print("  DICHIARATO  angolo per passo = tw/2 : %.6e rad" % float(np.median(np.abs(tw)) / 2.0))
else:
    print("  (nessun arco: tw vuoto)")
oBn = np.linalg.norm(oB, axis=1)
print("  |omega_s| mediana ON                : %.6e" % float(np.median(oBn)))
print("  |omega_s| mediana OFF               : %.6e" % float(np.median(mA)))
print("""
  COME SI LEGGE (e cosa NON dice): se `|d omega|` e' dell'ordine di `|tw|/(4pi)` allora il termine
  entra come somma DIRETTA a una velocita' angolare, e l'angolo effettivo per passo e'
  `|tw|/(4pi) * dt_n`, NON `tw/2`. Se invece e' molto PIU' GRANDE, il termine si e' ACCUMULATO
  nella memoria `omega_s` attraverso il rilassamento (fattore ~ tau/dt_n). Le due letture si
  distinguono dal NUMERO, e il numero e' qui sopra.""")

# ---- stabilita' ------------------------------------------------------------------------------
psp = B.get("_psi_spinor")
if psp is not None and len(psp):
    nor = np.linalg.norm(np.asarray(psp), axis=1)
    print("\n--- stabilita' col flag ON ---")
    print("  max| |psi| - 1 | = %.3e su %d nodi" % (float(np.max(np.abs(nor - 1.0))), len(nor)))
fin = all(np.all(np.isfinite(v)) for v in B.values()
          if isinstance(v, np.ndarray) and v.dtype != object and np.issubdtype(v.dtype, np.number))
print("  nessun NaN/inf in tutto lo stato: %s" % fin)
pos = np.asarray(B.get("pos"), float)
print("  max|x| = %.4g" % float(np.max(np.abs(pos))))
print("=" * 96)
