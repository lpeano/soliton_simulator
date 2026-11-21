# -*- coding: utf-8 -*-
r"""**IL FILM LEGGERO** *(la richiesta di Luca `2026-11-21` sera: sola lettura, nessun tick, nessuna corsa toccata)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/film/esporta_film.py --quale mitosi --out doc/referti_l2/film/mitosi.npz
    E:\python\py3132\python.exe doc/referti_l2/film/esporta_film.py --quale chi --out doc/referti_l2/film/mattone_chi.npz

**`mitosi`:** lo stato del tronco PRIMA della prima nascita *(`TRONCO/prima_nascita_35976.npz`)* e gli stati salvati del ramo MITOSI fino a `k 36250`; per stato `rho` *(dalle estremita')*, **gli archi `ii`, `jj` e le posizioni del disegno `m1`, `m2` DI QUELLO STATO** *(il grafo cresce)*; **le nascite** *(`nascite_36250.json`: `k`, l'arco, il nodo nuovo, `r`, `DH`, `DH_nascita`, `DH_flip`)*.
**`chi`:** gli stati salvati della corsa del mattone con `chi` *(`E:/soliton_simulator/controllo/CHI/mattone/stato_*.npz`, dal piu' vecchio all'ultimo con la sua `.sha1`)*; per stato `rho` e `chi`; **gli archi e le posizioni UNA volta** *(il grafo e' il toro, non cambia: dichiarato)*.
**Le posizioni del disegno** sono le coordinate di reticolo `m1`, `m2` *(il punto e' `m1 a1 + m2 a2`, coi vettori del triangolare)*; **tutto in `float32`** *(gli indici `int32`)*, compresso. **Sopra `50 MB`:** un nodo su due fuori da `r 60` *(dal centro del `meta`)*, e il file lo dichiara *(`dimezzato`)*.
"""
import argparse
import glob
import hashlib
import json
import os
import sys

import numpy as np

L, N0 = 186, 186 * 186
BASE_M = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_rami")
BASE_C = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "mattone")
TETTO = 50e6


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def toro():
    """### gli archi del toro di `L 186`: l'arco `3 v + a` da `v` verso `a1`, `a2`, `a1 + a2` *(come `mitosi_film.toro`)*."""
    v = np.arange(N0)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L
    return np.repeat(v, 3), np.stack([nb(1, 0), nb(0, 1), nb(1, 1)], axis=1).reshape(-1), m1.astype(float), m2.astype(float)


def leggi(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        X = {x: d[x] for x in d.files if x in ("psi_h", "ii", "jj", "m1", "m2", "chi", "meta")}
    meta = json.loads(str(X.pop("meta")))
    if "ii" in X:
        ii, jj, m1, m2 = X["ii"].astype(np.int64), X["jj"].astype(np.int64), np.asarray(X["m1"], float), np.asarray(X["m2"], float)
    else:
        ii, jj, m1, m2 = toro()
    n = len(m1)
    nodo = np.empty(2 * len(ii), dtype=np.int64)
    nodo[0::2], nodo[1::2] = ii, jj
    rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
    return int(meta["k"]), meta, rho, X.get("chi"), ii, jj, m1, m2


def scrivi(out, D):
    np.savez_compressed(out, **D)
    return os.path.getsize(out)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quale", choices=("mitosi", "chi"), required=True)
    ap.add_argument("--out", required=True)
    x = ap.parse_args(argv)
    os.makedirs(os.path.dirname(x.out), exist_ok=True)
    if x.quale == "mitosi":
        fs = [os.path.join(BASE_M, "TRONCO", "prima_nascita_35976.npz")]
        fs += [f for f in sorted(glob.glob(os.path.join(BASE_M, "MITOSI", "stato_*.npz"))) if int(os.path.basename(f)[6:-4]) <= 36250]
    else:
        fs = sorted((f for f in glob.glob(os.path.join(BASE_C, "stato_*.npz")) if os.path.exists(f + ".sha1")), key=lambda f: int(os.path.basename(f)[6:-4]))
    print("### %s: %d stati, da %s a %s" % (x.quale, len(fs), os.path.basename(fs[0]), os.path.basename(fs[-1])))
    S = [leggi(f) for f in fs]
    centro = S[0][1]["centro"]

    def costruisci(dimezza):
        D = {"k": np.array([s[0] for s in S], dtype=np.int32), "centro": np.array(centro, dtype=np.float32), "L": np.array(L), "dimezzato": np.array(dimezza)}
        tieni_di = {}
        for k, meta, rho, chi, ii, jj, m1, m2 in S:
            n = len(m1)
            if dimezza:
                dx = ((m1 - centro[0] + L / 2) % L) - L / 2
                dy = ((m2 - centro[1] + L / 2) % L) - L / 2
                xx, yy = dx + 0.5 * dy, (np.sqrt(3.0) / 2.0) * dy
                r = np.hypot(xx, yy)
                tieni = (r <= 60.0) | (np.arange(n) % 2 == 0)
            else:
                tieni = np.ones(n, dtype=bool)
            tieni_di[k] = tieni
            D["rho_%06d" % k] = rho[tieni].astype(np.float32)
            if chi is not None:
                D["chi_%06d" % k] = np.asarray(chi)[tieni].astype(np.float32)
            if x.quale == "mitosi" or k == S[0][0]:
                sfx = ("_%06d" % k) if x.quale == "mitosi" else ""
                D["ii" + sfx], D["jj" + sfx] = ii.astype(np.int32), jj.astype(np.int32)
                D["m1" + sfx], D["m2" + sfx] = m1.astype(np.float32), m2.astype(np.float32)
                if dimezza:
                    D["nodi_tenuti" + sfx] = np.nonzero(tieni)[0].astype(np.int32)
        if x.quale == "mitosi":
            with open(os.path.join(BASE_M, "MITOSI", "nascite_36250.json"), encoding="utf-8") as fh:
                B = json.load(fh)
            D["nascite_k"] = np.array([b["k"] for b in B], dtype=np.int32)
            D["nascite_arco"] = np.array([b["a"] for b in B], dtype=np.int32)
            D["nascite_n"] = np.array([b["nodi"]["n"] for b in B], dtype=np.int32)
            D["nascite_r"] = np.array([b["r"] for b in B], dtype=np.float32)
            D["nascite_DH"] = np.array([b["DH"] for b in B], dtype=np.float32)
            D["nascite_DH_nascita"] = np.array([b["DH_nascita"] for b in B], dtype=np.float32)
            D["nascite_DH_flip"] = np.array([b["DH_flip"] for b in B], dtype=np.float32)
        return D
    D = costruisci(False)
    sz = scrivi(x.out, D)
    dimezzato = False
    if sz > TETTO:
        print("### %.1f MB: sopra il tetto, UN NODO SU DUE FUORI DA r 60" % (sz / 1e6))
        D = costruisci(True)
        sz = scrivi(x.out, D)
        dimezzato = True
    print("### %s: %.2f MB%s; %d chiavi; i k: %s" % (x.out, sz / 1e6, " (DIMEZZATO fuori da r 60)" if dimezzato else "", len(D), [s[0] for s in S]))
    if x.quale == "mitosi":
        print("### le nascite: %d (k %s)" % (len(D["nascite_k"]), [int(v) for v in D["nascite_k"]]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
