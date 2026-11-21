# -*- coding: utf-8 -*-
r"""**O3 RILETTO DAI FILE: LA DECIMA NASCITA** *(il mandato di Luca `2026-11-21` `23:13`; la prova `orientamento_prove.py corse` ha contato le nascite nei bilanci della SOLA corsa -- che parte da `k 36250` senza i bilanci di prima -- e ha dato FALLISCE per un errore dello script: qui il criterio si rilegge dai file salvati, NESSUNA corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/orientamento_o3_rilettura.py > doc/referti_l2/orientamento_o3_rilettura.txt

**Il criterio** *(la carta sez. `4.4`, lo stesso)*: la decima nascita c'e' *(il numero delle nascite nel `meta` dello stato finale `>= 10`, e `9` nello stato di partenza)*; la PRIMA nascita della corsa e' la decima; **P9 a `0` e F3 a ogni nascita della corsa.**
"""
import hashlib
import json
import os
import sys

import numpy as np

D = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_rami")


def meta_di(f):
    h = hashlib.sha1(open(f, "rb").read()).hexdigest()
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == h, "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        return json.loads(str(d["meta"])), h


def main():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    m0, h0 = meta_di(os.path.join(D, "MITOSI", "stato_36250.npz"))
    m1, h1 = meta_di(os.path.join(D, "PROVA_V2", "o3", "stato_36350.npz"))
    with open(os.path.join(D, "PROVA_V2", "o3", "nascite_36350.json"), encoding="utf-8") as fh:
        B = json.load(fh)
    print("=" * 130)
    print("O3 RILETTO DAI FILE (Luca 2026-11-21 23:13; la carta sez. 4.4): nessuna corsa")
    print("=" * 130)
    print("### lo stato di partenza k %d (sha1 %s): %d nascite; lo stato finale k %d (sha1 %s): %d nascite; i bilanci della corsa: %d" % (m0["k"], h0[:8], m0["nascite"], m1["k"], h1[:8], m1["nascite"], len(B)))
    for q, b in enumerate(B):
        print("    la nascita %d (k %d, l'arco %d): r %.3f, %d passi; P9 %.1e; F3 %s" % (m0["nascite"] + q + 1, b["k"], b["a"], b["r"], b["passi"], b["P9"], b["F3"]))
    ok = m0["nascite"] == 9 and m1["nascite"] >= 10 and len(B) == m1["nascite"] - m0["nascite"] and all(b["P9"] == 0.0 and b["F3"] for b in B)
    decima = B[0] if B else None
    print("### la decima nascita: %s" % ("k %d, l'arco %d, r %.3f (il guscio 18-20: %s)" % (decima["k"], decima["a"], decima["r"], 18.0 <= decima["r"] <= 20.0) if decima else "### NON c'e'"))
    print("  DEVE: O3: la decima nascita passa; P9 a 0 e F3 a ogni nascita (riletto dai file)        %s" % ("PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
