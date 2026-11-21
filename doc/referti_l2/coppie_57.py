# -*- coding: utf-8 -*-
r"""**M1: LE COPPIE 5-7** *(il mandato di Luca `2026-11-21` `23:13`; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md`, sez. `3.2`; sola lettura)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/coppie_57.py > doc/referti_l2/coppie_57.txt

**Gli stati:** il toro iniziale *(il caso noto)* e il ramo MITOSI `k 36000`, `k 36250`. **La sorgente:** il nodo piu' vicino al centro della materia *(`toro.centro(rho)`, come `mitosi_rami`)*. **Per stato:** i nodi di grado `!= 6` *(grado, passi dalla sorgente, `r`)*; per ogni 5 il 7 piu' vicino in passi e viceversa *(legate `1`, vicine `2-3`, separate `> 3`)*; la curvatura netta `somma (6 - grado) 60` gradi nelle palle di passi `5, 10, 15, 18, 20, 25`.
**Le funzioni di lettura** *(`stato`, `passi_da`, `angolo_e_r`)* **le usa anche `raggruppamento_nascite.py`.**
"""
import hashlib
import json
import os
import sys

import numpy as np

_RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for _p in (os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "csv", "solitone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
L = 186
D = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_rami", "MITOSI")
STATI = (36000, 36250)
PALLE = (5, 10, 15, 18, 20, 25)


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def toro():
    v = np.arange(L * L)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L
    return np.repeat(v, 3), np.stack([nb(1, 0), nb(0, 1), nb(1, 1)], axis=1).reshape(-1), m1.astype(float), m2.astype(float)


def stato(f):
    """### `{ii, jj, n, m1, m2, rho, theta, k, sorgente, centro}` da uno stato salvato *(`None`: il toro iniziale, `rho` uniforme)*."""
    from solitone import toro as TO
    if f is None:
        ii, jj, m1, m2 = toro()
        n = L * L
        rho = np.ones(n)
        th = None
        k = 0
        c = (L / 2.0, L / 2.0)
    else:
        assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
        with np.load(f) as d:
            X = {x: d[x] for x in d.files if x in ("psi_h", "ii", "jj", "m1", "m2", "theta_a", "meta")}
        meta = json.loads(str(X["meta"]))
        if "ii" in X:
            ii, jj, m1, m2 = X["ii"].astype(np.int64), X["jj"].astype(np.int64), np.asarray(X["m1"], float), np.asarray(X["m2"], float)
        else:
            ii, jj, m1, m2 = toro()
        n = len(m1)
        nodo = np.empty(2 * len(ii), dtype=np.int64)
        nodo[0::2], nodo[1::2] = ii, jj
        rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
        th = X["theta_a"]
        k = int(meta["k"])
        c = TO.centro(rho, m1, m2, L)[:2]
    r = np.hypot(*TO.scarti(m1, m2, c[0], c[1], L).T[:2])
    return {"ii": ii, "jj": jj, "n": n, "m1": m1, "m2": m2, "rho": rho, "theta": th, "k": k, "centro": c, "r": r, "sorgente": int(np.argmin(r))}


def grafo(S):
    import scipy.sparse as sp
    ii, jj, n = S["ii"], S["jj"], S["n"]
    return sp.csr_matrix((np.ones(2 * len(ii)), (np.concatenate([ii, jj]), np.concatenate([jj, ii]))), shape=(n, n))


def passi_da(A, sorgenti):
    from scipy.sparse import csgraph
    return csgraph.shortest_path(A, unweighted=True, indices=np.atleast_1d(sorgenti))


def angolo_e_r(S, nodi, da):
    """### l'angolo (gradi, `[0, 360)`) e la distanza nel disegno dei `nodi` attorno al nodo `da` *(l'immagine minima)*."""
    from solitone import toro as TO
    x = TO.scarti(S["m1"][nodi], S["m2"][nodi], S["m1"][da], S["m2"][da], L)
    return np.degrees(np.arctan2(x[:, 1], x[:, 0])) % 360.0, np.hypot(x[:, 0], x[:, 1])


def misura(S, nome):
    ii, jj, n = S["ii"], S["jj"], S["n"]
    grado = np.bincount(np.concatenate([ii, jj]), minlength=n)
    A = grafo(S)
    src = S["sorgente"]
    ds = passi_da(A, src)[0]
    dif = np.nonzero(grado != 6)[0]
    print("### %s (k %d, n %d): la sorgente %d (r %.3f); i gradi %s; i difetti %d" % (nome, S["k"], n, src, S["r"][src], dict(zip(*np.unique(grado, return_counts=True))), dif.size))
    for v in dif:
        print("    il nodo %6d: grado %d, %d passi dalla sorgente, r %.3f" % (v, grado[v], int(ds[v]), S["r"][v]))
    cinque, sette = dif[grado[dif] == 5], dif[grado[dif] == 7]
    out = {"k": S["k"], "n": int(n), "difetti": int(dif.size), "cinque": int(cinque.size), "sette": int(sette.size), "coppie": [], "palle": {}}
    if cinque.size and sette.size:
        Dc = passi_da(A, cinque)[:, sette]
        for q, v in enumerate(cinque):
            j = int(np.argmin(Dc[q]))
            dd = int(Dc[q, j])
            cl = "legata" if dd == 1 else ("vicina" if dd <= 3 else "separata")
            out["coppie"].append({"cinque": int(v), "sette": int(sette[j]), "passi": dd, "classe": cl})
            print("    il 5 %d -> il 7 piu' vicino %d a %d passi (%s)" % (v, sette[j], dd, cl))
        for q, v in enumerate(sette):
            j = int(np.argmin(Dc[:, q]))
            print("    il 7 %d -> il 5 piu' vicino %d a %d passi" % (v, cinque[j], int(Dc[j, q])))
    for R in PALLE:
        dentro = ds <= R
        cur = float(np.sum((6 - grado[dentro]) * 60.0))
        out["palle"][str(R)] = cur
    print("    la curvatura netta (gradi) nelle palle di passi %s: %s" % (PALLE, ", ".join("%g" % out["palle"][str(R)] for R in PALLE)))
    return out


def main():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("M1, LE COPPIE 5-7 (Luca 2026-11-21 23:13; la carta sez. 3.2): sola lettura")
    print("=" * 130)
    esiti = []
    t0 = misura(stato(None), "IL TORO INIZIALE (il caso noto)")
    ok0 = t0["difetti"] == 0 and all(v == 0.0 for v in t0["palle"].values())
    esiti.append(("DEVE: il toro iniziale: tutti i gradi 6, la curvatura 0 in ogni palla", ok0))
    R = {}
    for k in STATI:
        f = os.path.join(D, "stato_%05d.npz" % k)
        R[k] = misura(stato(f), "IL RAMO MITOSI %s (sha1 %s)" % (os.path.basename(f), sha1(f)[:8]))
    r1 = R[36000]
    pm1 = r1["cinque"] == 1 and r1["sette"] == 1 and r1["difetti"] == 2 and r1["coppie"] and r1["coppie"][0]["passi"] == 1
    r9 = R[36250]
    pm2 = bool(r9["coppie"]) and all(c["passi"] <= 2 for c in r9["coppie"])
    pm3 = r9["palle"]["18"] == 0.0
    print("-" * 130)
    print("### P-M1 (k 36000, una nascita: un 5 e un 7 a distanza 1, nessun altro difetto): %s (5: %d, 7: %d, le coppie %s)" % ("VERA" if pm1 else "FALSA", r1["cinque"], r1["sette"], [c["passi"] for c in r1["coppie"]]))
    print("### P-M2 (k 36250: ogni 5 col suo 7 a distanza <= 2): %s (5: %d, 7: %d, le distanze %s)" % ("VERA" if pm2 else "FALSA", r9["cinque"], r9["sette"], [c["passi"] for c in r9["coppie"]]))
    print("### P-M3 (k 36250: la curvatura nella palla di raggio 18 e' 0): %s (%g gradi)" % ("VERA" if pm3 else "FALSA", r9["palle"]["18"]))
    for nm, ok in esiti:
        print("  %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
