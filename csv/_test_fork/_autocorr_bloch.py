# -*- coding: utf-8 -*-
"""AUTOCORRELAZIONE SPAZIALE DEI BLOCH — la firma che distingue DOMINI da COLLASSO GLOBALE.

PERCHE' SERVE (doc/PREDIZIONE_kuramoto.md §2)
---------------------------------------------
`chi` fra vicini e `|<n>|` globale non bastano: un `chi` basso e' compatibile **sia** coi domini
**sia** col collasso globale. Cio' che li separa e' come la correlazione `<n_i . n_j>` si comporta
al crescere della DISTANZA:

    RUMORE            ~0 a ogni distanza
    COLLASSO globale  ~1 a ogni distanza          <- una direzione unica per tutto il sistema
    DOMINI            parte alta e DECADE a una scala finita

PURE-READ PER COSTRUZIONE
-------------------------
Non tocca il simulatore e non lo importa nemmeno: legge i `.pkl` di stato gia' scritti dai run
(`pos`, `_nb`). Non c'e' nulla da sigillare, perche' non c'e' nulla che possa mutare.
Si confrontano gli stati allo STESSO passo finale, quindi il confronto e' a parita' di orizzonte.

CAMPIONAMENTO
-------------
Le coppie sono O(N^2) (N ~ 3500 -> 6 milioni): si campiona un sottoinsieme casuale di coppie con un
seed FISSO (riproducibile) e si bina per distanza. Il campionamento e' della DIAGNOSTICA, non della
fisica: non introduce parametri nel modello.

USO
---
python csv/_test_fork/_autocorr_bloch.py  [file.pkl ...]
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
N_COPPIE = 400000          # coppie campionate per stato
SEED = 20260914            # fisso: la diagnostica dev'essere riproducibile
N_BIN = 14


def carica(p):
    st = pickle.load(open(p, "rb"))["attrs"]
    pos = np.asarray(st["pos"], float)
    nb = st.get("_nb")
    if nb is None:
        return None
    nb = np.asarray(nb, float)
    n = min(len(pos), len(nb))
    nb = nb[:n]
    nb = nb / np.maximum(np.linalg.norm(nb, axis=1, keepdims=True), 1e-30)
    return pos[:n], nb


def profilo(pos, nb, g):
    n = len(pos)
    ii = g.integers(0, n, N_COPPIE)
    jj = g.integers(0, n, N_COPPIE)
    m = ii != jj
    ii, jj = ii[m], jj[m]
    d = np.linalg.norm(pos[ii] - pos[jj], axis=1)
    c = np.sum(nb[ii] * nb[jj], axis=1)
    # BIN LOGARITMICI, non a quantili. Con 3 masse a sep=8 la geometria e' bimodale (coppie dentro
    # una massa, d < ~2; coppie fra masse, d ~ 13-16) e i quantili sprecherebbero 8 bin su 12 nel
    # campo lontano, dove non c'e' nulla da vedere, lasciandone 4 proprio dove una scala di dominio
    # vivrebbe. I bin log danno risoluzione uniforme in scala, che e' cio' che serve per un decadimento.
    dmin = max(float(np.percentile(d, 0.5)), 1e-3)
    bordi = np.geomspace(dmin, float(d.max()) * 1.001, N_BIN + 1)
    out = []
    for k in range(N_BIN):
        s = (d >= bordi[k]) & (d < bordi[k + 1])
        if s.sum() > 50:
            out.append((float(np.median(d[s])), float(np.mean(c[s])), int(s.sum())))
    return out


def main():
    file = sys.argv[1:] or [
        os.path.join(HERE, "_vuoto_ab_on_s1.pkl"),
        os.path.join(HERE, "_vuoto_ab_off_s1.pkl"),
        os.path.join(HERE, "_vuoto_k_noise_s1.pkl"),
        os.path.join(HERE, "_vuoto_k_frozen_s1.pkl"),
    ]
    g = np.random.default_rng(SEED)
    print("=" * 100)
    print("AUTOCORRELAZIONE SPAZIALE  <n_i . n_j>  in funzione della distanza")
    print("=" * 100)
    print("RIFERIMENTI:  rumore -> ~0 a ogni distanza  |  collasso -> ~1 a ogni distanza  |"
          "  domini -> alta poi DECADE")
    for p in file:
        if not os.path.exists(p):
            print("\n--- %-28s  ASSENTE" % os.path.basename(p))
            continue
        r = carica(p)
        if r is None:
            print("\n--- %-28s  _nb assente nello stato" % os.path.basename(p))
            continue
        pos, nb = r
        mv = nb.mean(axis=0)
        prof = profilo(pos, nb, np.random.default_rng(SEED))
        print("\n--- %s   N=%d   |<n>|=%.6f   (atteso casuale 1/sqrt(N)=%.4f)"
              % (os.path.basename(p), len(nb), float(np.linalg.norm(mv)), 1.0 / np.sqrt(len(nb))))
        print("      distanza :", "".join("%8.2f" % d for d, _, _ in prof))
        print("     <n_i.n_j> :", "".join("%8.4f" % c for _, c, _ in prof))
        print("      n coppie :", "".join("%8d" % k for _, _, k in prof))
        if prof:
            c0, cN = prof[0][1], prof[-1][1]
            print("     vicino=%.4f  lontano=%.4f  calo=%.4f" % (c0, cN, c0 - cN))
    print("=" * 100)


if __name__ == "__main__":
    main()
