# -*- coding: utf-8 -*-
"""SIGILLO DELL'OSSERVATORE — la misura del vuoto e' PURE-READ? (par.2.3)

Un diagnostico che contamina la fisica non misura il sistema: misura se stesso. Qui si verifica
con DUE RUN VERI che l'osservatore di `_osserva_vuoto.py` non cambi un bit dello stato finale.

SIGILLI
  O1  osservatore ON vs OFF, stesso seed -> max|A-B| = 0.000e+00 su tutti gli array di stato
  O2  l'A/B dello scuotimento e' a VARIABILE SINGOLA: `--regime deterministico` cambia SOLO
      SCUOTIMENTO (confronto di TUTTI i globali del modulo, non solo di quelli attesi)
  O3  il braccio ON ha SCUOTIMENTO=True e il braccio OFF SCUOTIMENTO=False, ed entrambi hanno
      FORK_SU2 e FORK_SU2_MEM attivi (il run deve testare lo STRATO 1, non lo Strato 0 inerte)

Finestra: 150 passi. Basta per una byte-identita' (una divergenza si manifesta al primo passo) e
NON pretende di concludere nulla di fisico (par.2.7).
"""
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DRV = os.path.join(HERE, "_osserva_vuoto.py")
PY = sys.executable
PASSI = 150

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-46s %s" % ("PASS" if ok else "FAIL", nome, misura))


def run(tag, extra=()):
    cmd = [PY, DRV, "--seed", "1", "--passi", str(PASSI), "--ogni", "50",
           "--tag", tag, "--outdir", HERE] + list(extra)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-1200:])
        print("STDERR:", r.stderr[-1200:])
        raise SystemExit("run FALLITO: " + tag)
    pk = os.path.join(HERE, "_vuoto_%s_s1.pkl" % tag)
    with open(pk, "rb") as f:
        return pickle.load(f)["attrs"], r.stdout


def diff(A, B):
    worst, bad = 0.0, {}
    for k in A:
        if k in B and isinstance(A[k], np.ndarray) and isinstance(B[k], np.ndarray) \
                and A[k].dtype != object:
            if A[k].shape != B[k].shape:
                bad[k] = ("SHAPE", A[k].shape, B[k].shape)
                continue
            if A[k].size:
                d = float(np.max(np.abs(A[k].astype(np.complex128) - B[k].astype(np.complex128))))
                if d > 0:
                    bad[k] = d
                worst = max(worst, d)
    return worst, bad


print("=" * 92)
print("SIGILLO OSSERVATORE — la misura del vuoto e' PURE-READ? (2 run veri, %d passi)" % PASSI)
print("=" * 92)

A, out_on = run("sigON")                                  # con osservatore
B, out_off = run("sigOFF", extra=["--no-osserva"])        # senza osservatore
n_a, n_b = len(A.get("phi", ())), len(B.get("phi", ()))
worst, bad = diff(A, B)
# PRESIDIO (lezione 2026-09-14): uno zero puo' voler dire "nessun confronto". Prima le shape.
verdetto("O1.0 stesso numero di nodi (il confronto ESISTE)", n_a == n_b and n_a > 0,
         "nodi: osservatore ON = %d, OFF = %d" % (n_a, n_b))
verdetto("O1 osservatore ON vs OFF: byte-identico", worst == 0.0 and not bad,
         "max|A-B| = %.3e%s" % (worst, "" if not bad else "  DIVERGENTI: " + str(list(bad)[:5])))

print()
print("=" * 92)
print("O2 — l'A/B dello scuotimento e' a VARIABILE SINGOLA?")
print("=" * 92)
BASE = ["--batch", "--nmasse", "3", "--sep", "8", "--seed", "1", "--passi", "1",
        "--ogni", "1", "--db-ogni", "1", "--campo-spinoriale", "--spinore-vivo",
        "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet",
        "--fork-su2", "--fork-su2-mem"]
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"] + BASE
import soliton_simulator as S  # noqa: E402


def globali():
    return {k: v for k, v in vars(S).items()
            if not k.startswith("__") and isinstance(v, (int, float, bool, str, type(None), tuple))}


prima = globali()
sys.argv = ["soliton_simulator.py"] + BASE + ["--regime", "deterministico"]
S._applica_regime(S._cli())
dopo = globali()
cambiati = sorted(k for k in set(prima) | set(dopo)
                  if prima.get(k, "<assente>") != dopo.get(k, "<assente>"))
for k in cambiati:
    print("   %-20s %-14r -> %r" % (k, prima.get(k), dopo.get(k)))
extra = [k for k in cambiati if k not in ("SCUOTIMENTO", "REGIME")]
verdetto("O2 --regime deterministico cambia SOLO SCUOTIMENTO", not extra and "SCUOTIMENTO" in cambiati,
         "cambiati: %s%s" % (cambiati, "" if not extra else "  <-- OLTRE al previsto: " + str(extra)))

print()
print("=" * 92)
print("O3 — i due bracci hanno i flag giusti?")
print("=" * 92)
_, out_det = run("sigDET", extra=["--regime-det", "--no-osserva"])


def riga_flag(txt):
    for l in txt.splitlines():
        if l.startswith("[osserva]") and "SCUOTIMENTO" in l:
            return l.strip()
    return "(riga [osserva] non trovata)"


r_on, r_det = riga_flag(out_on), riga_flag(out_det)
print("   braccio ON : %s" % r_on)
print("   braccio OFF: %s" % r_det)
verdetto("O3a braccio ON: SCUOTIMENTO=True", "SCUOTIMENTO=True" in r_on, r_on[-60:])
verdetto("O3b braccio OFF: SCUOTIMENTO=False", "SCUOTIMENTO=False" in r_det, r_det[-60:])
verdetto("O3c entrambi testano lo STRATO 1 (fork + memoria)",
         "FORK_SU2=True FORK_SU2_MEM=True" in r_on and "FORK_SU2=True FORK_SU2_MEM=True" in r_det,
         "fork+mem attivi su entrambi i bracci")

print("=" * 92)
tot_, ok_ = len(esiti), sum(esiti)
print("SIGILLO OSSERVATORE: %d/%d PASS -> %s" % (ok_, tot_, "PASS" if ok_ == tot_ else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
Che le misure siano CORRETTE, solo che non CONTAMINANO. Che chi e <n> misurino quel che si crede
lo dice la loro definizione (arccos del prodotto scalare fra Bloch vicini; media vettoriale dei
Bloch), non questo sigillo. E 150 passi non concludono nulla di fisico (par.2.7).
""")
sys.exit(0 if ok_ == tot_ else 1)
