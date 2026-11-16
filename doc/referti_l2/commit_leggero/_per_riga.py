# -*- coding: utf-8 -*-
"""Aiutante della prova S2 (Luca 2026-11-16 08:57): carica `indice.py` DA UN PERCORSO e stampa l'impronta di `_storico_da_git()`.

    python _per_riga.py <albero>/csv/indice.py

Stampa una riga: `PER_RIGA <sha1 di repr((per_riga, n_head, n_stage))> <len(per_riga)> <n_head> <n_stage> <secondi>`.
"""
import hashlib
import importlib.util
import os
import sys
import time


def main(argv):
    f = os.path.abspath(argv[0])
    sys.path.insert(0, os.path.dirname(f))
    spec = importlib.util.spec_from_file_location("indice_in_prova", f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    t = time.time()
    pr, nh, ns = m._storico_da_git()
    print("PER_RIGA %s %d %d %d %.1f s" % (hashlib.sha1(repr((pr, nh, ns)).encode("utf-8")).hexdigest(), len(pr), nh, ns, time.time() - t))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
