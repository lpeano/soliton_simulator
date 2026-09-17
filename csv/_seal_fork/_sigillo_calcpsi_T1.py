# -*- coding: utf-8 -*-
"""Q1-Q2 -- TEMPO 1 di `calcola_psi(w=None)`: **solo strumentazione.**

Q1 [BLOCCANTE] aggiungere i contatori deve essere BYTE-IDENTICO (e con lo STESSO N: la riga dei
                conteggi si stampa PER PRIMA, perche' shape diverse = MANCANZA DI CONFRONTO).
Q2            il contatore DEVE leggere > 0. Se legge 0, la diagnosi e' sbagliata: reperto, STOP.
              (E' il controllo positivo dello STRUMENTO, non della correzione.)

E la TABELLA: quante chiamate, quante con `w is None`, **per CHIAMANTE**, separando
**DENTRO** il passo (finestra t/t+1 -> violano l'intento di :2959) da **FUORI** (non violano nulla).
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
PRE = os.path.join(SC, "_pre_calcpsi.py")
esiti = []

# I chiamanti che stanno DENTRO la finestra del passo. Ricavati dal sorgente, non indovinati:
# sono i metodi che `step()` invoca (direttamente o no) fra il calcolo di `w` e la fine del passo.
DENTRO = {"step", "_passo_spinoriale", "mitosi", "ritmo", "lambda_vuoto",
          "_coppia_interferenza", "_forze", "_gravita", "_cs_nodo"}


def verdetto(nome, ok, misura):
    esiti.append(bool(ok))
    print("[%s] %-50s %s" % ("PASS" if ok else "FAIL", nome, misura))


def gira(sim, tag, passi=40, seme=9):
    db = os.path.join(SC, "_q_%s.pkl" % tag)
    cmd = [sys.executable, sim, "--batch", "--nmasse", "3", "--sep", "8",
           "--seed", str(seme), "--passi", str(passi), "--ogni", str(passi),
           "--db-ogni", str(passi), "--campo-spinoriale", "--spinore-vivo",
           "--spinore-corretto", "--chi-core", "--calore-scal", "--deparam-orologio",
           "--verlet", "--fork-su2", "--fork-su2-mem", "--cs-dinamico",
           "--csv", os.path.join(SC, "_q_%s.csv" % tag), "--sync-db", db, "--db-cleanup"]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        print("  [run %s FALLITO rc=%s]\n%s" % (tag, p.returncode, (p.stderr or "")[-1200:]))
        return None
    return pickle.load(open(db, "rb"))["attrs"]


print("=" * 118)
print("Q1-Q2 -- TEMPO 1: contare il fallback `w is None` di calcola_psi(). NESSUNA LEGGE TOCCATA.")
print("=" * 118)

A = gira(PRE, "pre")
B = gira(os.path.join(ROOT, "soliton_simulator.py"), "post")

if A is None or B is None:
    esiti.append(False)
else:
    # ---------------------------------------------------------------- Q1
    print("\n--- (Q1) i contatori sono INERTI?  [BLOCCANTE] ---")
    ka, kb = set(A), set(B)
    nuove = sorted(kb - ka)
    print("  chiavi nuove nel DB (i contatori): %s" % nuove)
    comuni = sorted(ka & kb)
    shape_ok, confrontati, peggio, peggio_k, diversi = True, 0, 0.0, "-", []
    for k in comuni:
        try:
            x = np.asarray(A[k]); y = np.asarray(B[k])
        except Exception:
            continue
        if x.dtype == object or y.dtype == object or x.ndim == 0:
            continue
        if x.shape != y.shape:
            shape_ok = False; diversi.append("%s %s!=%s" % (k, x.shape, y.shape)); continue
        confrontati += 1
        if np.issubdtype(x.dtype, np.number) or np.issubdtype(x.dtype, np.complexfloating):
            d = np.abs(x - y); m = float(np.max(d)) if d.size else 0.0
            if m > peggio:
                peggio, peggio_k = m, k
    print("  PRESIDIO, riga dei conteggi PER PRIMA: nodi PRE %d, nodi POST %d"
          % (len(np.asarray(A["psi"])), len(np.asarray(B["psi"]))))
    print("  array con SHAPE UGUALI effettivamente confrontati: %d   (shape diverse: %d)"
          % (confrontati, len(diversi)))
    verdetto("Q1a c'e' CONFRONTO (stesso N, shape uguali)",
             shape_ok and confrontati > 10 and len(np.asarray(A["psi"])) == len(np.asarray(B["psi"])),
             "%d array confrontati" % confrontati)
    verdetto("Q1b BYTE-IDENTICO: max|A-B| = 0.000e+00  [BLOCCANTE]", peggio == 0.0,
             "max = %.3e (peggiore: %s) su %d array" % (peggio, peggio_k, confrontati))

    # ---------------------------------------------------------------- Q2
    print("\n--- (Q2) il contatore LEGGE? (controllo positivo dello STRUMENTO) ---")
    tot = B.get("_calcpsi_chiamate")
    none = B.get("_calcpsi_w_none")
    orig = B.get("_calcpsi_origini") or {}
    print("  chiamate TOTALI a calcola_psi : %s" % tot)
    print("  di cui con `w is None`        : %s   (%.2f %%)"
          % (none, 100.0 * (none or 0) / max(tot or 1, 1)))
    verdetto("Q2 il contatore legge > 0", bool(none), "_calcpsi_w_none = %s" % none)

    # ---------------------------------------------------------------- la TABELLA
    print("\n--- LA TABELLA PER CHIAMANTE ---")
    print("  %-34s %-10s %-12s" % ("chiamante:riga", "volte", "posizione"))
    print("  " + "-" * 60)
    d_in = d_out = 0
    for k, v in sorted(orig.items(), key=lambda x: -x[1]):
        nome = k.split(":")[0]
        pos = "DENTRO il passo" if nome in DENTRO else "fuori"
        if nome in DENTRO:
            d_in += v
        else:
            d_out += v
        print("  %-34s %-10d %-12s" % (k, v, pos))
    print("  " + "-" * 60)
    print("  %-34s %-10d" % ("DENTRO il passo (violano :2959)", d_in))
    print("  %-34s %-10d" % ("fuori (non violano nulla)", d_out))
    print("""
  LA DISTINZIONE CHE DECIDE: solo i chiamanti DENTRO il passo violano l'intento scritto a :2959
  (*"Non ricalcolare psi in punti diversi del passo: quello introdurrebbe letture miste t/t+1"*).
  Quelli FUORI - diagnostica, setup, analisi - possono restare, e vanno DICHIARATI tali, non
  corretti per simmetria.""")
    passi = 40
    print("  media per passo: %.2f chiamate, di cui %.2f con w is None"
          % ((tot or 0) / passi, (none or 0) / passi))

print("\n" + "=" * 118)
ok = sum(esiti)
print("Q1-Q2: %d/%d PASS -> %s" % (ok, len(esiti), "PASS" if ok == len(esiti) else "FAIL"))
print("""
COSA QUESTO SIGILLO NON DICE
----------------------------
NON dice che i pesi ricalcolati siano DIVERSI da quelli di `step()`. Dice quante volte vengono
ricalcolati e da chi. **Se coincidessero, il difetto sarebbe teorico** - ed e' esattamente cio' che
Q4 misurera' nel TEMPO 2, che NON e' in questo commit.""")
