# -*- coding: utf-8 -*-
r"""**I DATI PER L'ANIMAZIONE** *(Luca `2026-11-20` `18:56`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `15`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_film.py --base E:\soliton_simulator\controllo\mitosi_rami --out doc/referti_l2/mitosi_film

**Legge, non tocca:** gli stati salvati dalle corse *(`<base>/TRONCO`, `<base>/MITOSI`, `<base>/C2EXT`: `stato_<k>.npz`, controllati con lo sha1)* e i bilanci delle nascite *(l'ultimo `nascite_<k>.json` di MITOSI)*.
**Scrive in `<out>`:** `posizioni_originali.npz` *(`m1`, `m2` dei `L^2` nodi del toro, `float32`, una volta)*; **`TRONCO.npz` e `C2EXT.npz`** *(`rho_<k>` ogni `1000` tick, `float32`)*; **`MITOSI.npz`** *(`rho_<k>`, `grado_<k>` e le posizioni dei nodi NATI `m1_nuovi_<k>`, `m2_nuovi_<k>` ogni `1000` tick)*; **`nascite.json`** *(per nascita: `tick`, `i`, `j`, `k`, `l`, `n`, il lato del flip `x`, `y` e `m` -- `null` col pari merito --, `DH_nascita`, `DH_flip`, `E_persa`)*.
**`rho` si RICALCOLA dalle estremita'** *(`somma |psi_h|^2` sul nodo; il grafo dello stato, o il toro di `L 186` -- l'arco `3 v + a` da `v` verso `a1`, `a2`, `a1 + a2` -- se lo stato non lo porta)*. **Il lato del flip:** l'indice scelto fra `(i, k)`, `(j, k)`, `(j, l)`, `(i, l)` *(l'ordine di `mitosi_regola.regola`)*.
"""
import argparse
import glob
import hashlib
import json
import os
import sys

import numpy as np

L, N0 = 186, 186 * 186
OGNI = 1000


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def toro():
    v = np.arange(N0)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L
    ii = np.repeat(v, 3)
    jj = np.stack([nb(1, 0), nb(0, 1), nb(1, 1)], axis=1).reshape(-1)
    return ii, jj


def leggi(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        X = {x: d[x] for x in d.files if x in ("psi_h", "ii", "jj", "m1", "m2", "meta")}
    meta = json.loads(str(X.pop("meta")))
    if "ii" in X:
        ii, jj, n = X["ii"].astype(np.int64), X["jj"].astype(np.int64), int(meta["n"])
    else:
        ii, jj = toro()
        n = N0
    nodo = np.empty(2 * len(ii), dtype=np.int64)
    nodo[0::2], nodo[1::2] = ii, jj
    rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
    grado = np.bincount(nodo, minlength=n)
    return int(meta["k"]), rho, grado, X.get("m1"), X.get("m2")


def corsa(d, con_grado, ogni):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "stato_*.npz"))):
        k = int(os.path.basename(f)[6:11])
        if k % ogni:
            continue
        k_, rho, grado, m1, m2 = leggi(f)
        assert k_ == k
        out["rho_%05d" % k] = rho.astype(np.float32)
        if con_grado:
            out["grado_%05d" % k] = grado.astype(np.int16 if grado.max() < 32767 else np.int32)
            if m1 is not None:
                out["m1_nuovi_%05d" % k] = np.asarray(m1[N0:], dtype=np.float32)
                out["m2_nuovi_%05d" % k] = np.asarray(m2[N0:], dtype=np.float32)
    return out


def nascite(d):
    fs = sorted(glob.glob(os.path.join(d, "nascite_*.json")))
    if not fs:
        return []
    with open(fs[-1], encoding="utf-8") as fh:
        B = json.load(fh)
    out = []
    for b in B:
        nd = b["nodi"]
        lati = ((nd["i"], nd["k"]), (nd["j"], nd["k"]), (nd["j"], nd["l"]), (nd["i"], nd["l"]))
        x, y = lati[b["scelto"]] if b["scelto"] >= 0 else (None, None)
        out.append({"tick": b["k"], "i": nd["i"], "j": nd["j"], "k": nd["k"], "l": nd["l"], "n": nd["n"], "x": x, "y": y, "m": nd.get("m"),
                    "DH_nascita": b["DH_nascita"], "DH_flip": b["DH_flip"], "E_persa": b["E_persa"]})
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ogni", type=int, default=OGNI)                     # ### 1000 (il mandato); un altro valore solo per provare lo script
    x = ap.parse_args(argv)
    os.makedirs(x.out, exist_ok=True)
    v = np.arange(N0)
    np.savez_compressed(os.path.join(x.out, "posizioni_originali.npz"), m1=(v // L).astype(np.float32), m2=(v % L).astype(np.float32), L=np.array(L))
    for nome, con_grado in (("TRONCO", False), ("MITOSI", True), ("C2EXT", False)):
        d = os.path.join(x.base, nome)
        if not os.path.isdir(d):
            print("### %s: nessuna cartella" % nome)
            continue
        D = corsa(d, con_grado, x.ogni)
        np.savez_compressed(os.path.join(x.out, "%s.npz" % nome), **D)
        print("### %s: %d istantanee (%s)" % (nome, sum(1 for k in D if k.startswith("rho_")), ", ".join(sorted(k for k in D if k.startswith("rho_")))[:200]))
    N = nascite(os.path.join(x.base, "MITOSI"))
    with open(os.path.join(x.out, "nascite.json"), "w", encoding="utf-8") as fh:
        json.dump(N, fh, indent=0)
    print("### nascite.json: %d nascite" % len(N))
    tot = sum(os.path.getsize(f) for f in glob.glob(os.path.join(x.out, "*")))
    print("### la cartella %s: %.2f MB" % (x.out, tot / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
