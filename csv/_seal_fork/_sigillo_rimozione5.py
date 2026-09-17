# -*- coding: utf-8 -*-
"""V9 -- SIGILLO **ASSOLUTO** DELLA RIMOZIONE DI `spin_locale()` (correzione (5)).

La rimozione di codice morto deve essere ESATTAMENTE inerte: `max|A-B| = 0.000e+00` su OGNI array,
**con le shape UGUALI**. La condizione sulle shape non e' pignoleria: su questo repo uno zero e'
gia' stato letto come identita' mentre era MANCANZA DI CONFRONTO (CLAUDE.md par.9, due casi).

SE LA RIMOZIONE NON FOSSE INERTE, la conclusione NON e' "ho rotto qualcosa": e' che **GATE C aveva
torto**, cioe' esiste una via di chiamata che la scansione non ha trovato. E' scritto cosi' anche
in doc/PREVISIONI_qualitative.md par.6, PRIMA di eseguire.

Confronta due processi: il file PRIMA della rimozione (copia in scratchpad) e quello DOPO.
ASCII PURO.
"""
import os
import pickle
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SC = os.environ.get("SCRATCH", HERE)
PRE = os.path.join(SC, "_pre_rimozione5.py")
PASSI = 40
SEME = 3

esiti = []


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-46s %s" % ("PASS" if ok else "FAIL", nome, misura))


def gira(sim, tag):
    db = os.path.join(SC, "_v9_%s.pkl" % tag)
    cmd = [sys.executable, sim, "--batch", "--nmasse", "3", "--sep", "8",
           "--seed", str(SEME), "--passi", str(PASSI), "--ogni", str(PASSI),
           "--db-ogni", str(PASSI), "--campo-spinoriale", "--spinore-vivo",
           "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio",
           "--verlet", "--fork-su2", "--fork-su2-mem", "--cs-dinamico",
           "--csv", os.path.join(SC, "_v9_%s.csv" % tag), "--sync-db", db, "--db-cleanup"]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        print("  [run %s FALLITO rc=%s]\n%s" % (tag, p.returncode, (p.stderr or "")[-1200:]))
        return None
    return pickle.load(open(db, "rb"))["attrs"]


print("=" * 118)
print("V9 -- RIMOZIONE DI `spin_locale()`: deve essere ESATTAMENTE INERTE")
print("=" * 118)
print("  PRIMA : %s" % PRE)
print("  DOPO  : %s" % os.path.join(ROOT, "soliton_simulator.py"))
print("  %d passi, seme %d, stessi flag.\n" % (PASSI, SEME))

# il metodo esiste prima e non esiste dopo
pre_src = open(PRE, encoding="utf-8", errors="replace").read()
post_src = open(os.path.join(ROOT, "soliton_simulator.py"), encoding="utf-8", errors="replace").read()
verdetto("V9a il metodo c'era ed e' sparito dal CODICE",
         ("def spin_locale" in pre_src) and
         (sum(1 for l in post_src.splitlines() if "def spin_locale" in l.split("#")[0]) == 0),
         "prima: definito; dopo: 0 definizioni (resta solo il commento che spiega)")

A = gira(PRE, "pre")
B = gira(os.path.join(ROOT, "soliton_simulator.py"), "post")
if A is None or B is None:
    esiti.append(False)
else:
    ka, kb = set(A), set(B)
    print("  array nel DB: PRIMA %d, DOPO %d, comuni %d" % (len(ka), len(kb), len(ka & kb)))
    verdetto("V9b le CHIAVI del DB coincidono", ka == kb,
             "solo prima: %s | solo dopo: %s" % (sorted(ka - kb)[:4], sorted(kb - ka)[:4]))

    shape_ok, confrontati, peggio, peggio_k, diversi = True, 0, 0.0, "-", []
    for k in sorted(ka & kb):
        x, y = A[k], B[k]
        try:
            x = np.asarray(x); y = np.asarray(y)
        except Exception:
            continue
        if x.dtype == object or y.dtype == object or x.ndim == 0:
            continue
        if x.shape != y.shape:
            shape_ok = False
            diversi.append("%s %s!=%s" % (k, x.shape, y.shape))
            continue
        confrontati += 1
        if np.issubdtype(x.dtype, np.number) or np.issubdtype(x.dtype, np.complexfloating):
            d = np.abs(x - y)
            m = float(np.max(d)) if d.size else 0.0
            if m > peggio:
                peggio, peggio_k = m, k

    print("  array confrontati con SHAPE UGUALI: %d" % confrontati)
    if diversi:
        print("  SHAPE DIVERSE: %s" % ", ".join(diversi[:8]))
    verdetto("V9c NESSUN array ha shape diversa (c'e' confronto)", shape_ok and confrontati > 10,
             "%d array confrontati, %d con shape diversa" % (confrontati, len(diversi)))
    verdetto("V9d BYTE-IDENTICO: max|A-B| = 0.000e+00  [ASSOLUTO]", peggio == 0.0,
             "max = %.3e (peggiore: %s) su %d array" % (peggio, peggio_k, confrontati))

print("\n" + "=" * 118)
ok = sum(esiti)
print("V9: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
NB: V9d e' l'UNICO sigillo di questa bonifica in cui uno ZERO e' il risultato voluto, e proprio per
questo V9c lo precede: senza la garanzia che le shape coincidano, `max|A-B| = 0.000e+00` puo'
significare "nessun confronto" invece di "identico". Qui il numero di array effettivamente
confrontati e' stampato accanto allo zero, perche' lo zero da solo non e' leggibile.""")
