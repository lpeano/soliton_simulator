# -*- coding: utf-8 -*-
r"""**LA CIRCONFERENZA DELL'ANELLO `40` E LA DISTANZA ESTERNA FRA NODI OPPOSTI, A OGNI STATO SALVATO** *(l'aggiunta al referto di Luca `2026-11-21` `14:06`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `17`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_anelli.py prova --base E:\soliton_simulator\controllo\mitosi_rami > doc/referti_l2/mitosi_anelli_prova.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_anelli.py rami  --base E:\soliton_simulator\controllo\mitosi_rami > doc/referti_l2/mitosi_anelli.txt

**Legge, non tocca:** gli stati salvati *(lo sha1 controllato)*, i bilanci delle nascite *(`nascite_<k>.json`)*, la serie *(`D_med40`, la D1 della corsa)*.
**Le definizioni** *(la carta sez. `17.2`)*: **il centro** = `meta["centro"]`; **il raggio** con `toro.scarti` *(gli originari dal toro, i nati dalla loro posizione)*; **l'anello `40`** = gli originari con `39.5 <= r0 < 40.5`; **la fascia** = l'anello `40` piu' i nati su un arco con le DUE estremita' nella fascia *(per genealogia, nell'ordine delle nascite)*; **la circonferenza** = il ciclo piu' corto della fascia che attraversa UNA volta il taglio all'angolo `pi`; **la distanza esterna** = `6` coppie fisse di nodi opposti dell'anello `40` *(gli angoli `0, 30, ..., 150` gradi e gli opposti)* nel grafo SENZA i nodi con `r < 20.5`.
**`prova`** *(la carta sez. `17.4`)*: sul toro, col centro dell'ultimo stato integro del tronco: **la scala** *(contro `2 pi 40` e `pi 40`)*; **ogni arco della fascia diviso -> la circonferenza RADDOPPIA**; **ogni arco fuori dall'anello `20` diviso -> la distanza esterna RADDOPPIA**; **ogni arco dentro l'anello `20` diviso -> NIENTE cambia** *(il controllo fermo)*.
"""
import argparse
import glob
import hashlib
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.join(_QUI, "..", "..", "csv")
for p in (_CSV,):
    if p not in sys.path:
        sys.path.insert(0, p)
L, N0 = 186, 186 * 186
R_ANELLO, R_DENTRO = 40.0, 20.5
ANGOLI = tuple(range(0, 180, 30))


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
    return ii, jj, m1.astype(float), m2.astype(float)


def leggi(f):
    """### `(k, ii, jj, n, m1, m2, centro)` da uno stato: il grafo se lo porta, se no il toro."""
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        X = {x: d[x] for x in d.files if x in ("ii", "jj", "m1", "m2", "meta")}
    meta = json.loads(str(X.pop("meta")))
    if "ii" in X:
        ii, jj, m1, m2 = X["ii"].astype(np.int64), X["jj"].astype(np.int64), np.asarray(X["m1"], float), np.asarray(X["m2"], float)
    else:
        ii, jj, m1, m2 = toro()
    return int(meta["k"]), ii, jj, len(m1), m1, m2, [float(c) for c in meta["centro"]]


def polari(m1, m2, c):
    from solitone import toro as TO
    S = TO.scarti(m1, m2, c[0], c[1], L)
    return np.hypot(S[:, 0], S[:, 1]), np.arctan2(S[:, 1], S[:, 0])


def mezzo(m1, m2, i, j):
    """### il punto medio sul toro *(lo scarto piu' corto, non la media dei numeri: un arco che attraversa il bordo)*."""
    d1 = ((m1[j] - m1[i] + 0.5 * L) % L) - 0.5 * L
    d2 = ((m2[j] - m2[i] + 0.5 * L) % L) - 0.5 * L
    return (m1[i] + 0.5 * d1) % L, (m2[i] + 0.5 * d2) % L


def bfs(ii, jj, n, sorgenti):
    import scipy.sparse as sp
    from scipy.sparse import csgraph
    A = sp.csr_matrix((np.ones(2 * len(ii)), (np.concatenate([ii, jj]), np.concatenate([jj, ii]))), shape=(n, n))
    return csgraph.shortest_path(A, unweighted=True, indices=np.asarray(sorgenti, dtype=np.int64))


def fascia(r, n, nati):
    """### l'anello `40` degli originari, piu' i nati su un arco della fascia *(nell'ordine: `nati` = `[(i, j, n), ...]`)*."""
    b = np.zeros(n, dtype=bool)
    b[:N0] = (r[:N0] >= R_ANELLO - 0.5) & (r[:N0] < R_ANELLO + 0.5)
    for i, j, x in nati:
        if b[i] and b[j]:
            b[x] = True
    return b


def circonferenza(ii, jj, n, b, ang):
    """### il ciclo piu' corto della fascia che attraversa UNA volta il taglio all'angolo `pi`: `(lunghezza, archi del taglio)`."""
    e = b[ii] & b[jj]
    a, c = ii[e], jj[e]
    taglio = np.abs(ang[a] - ang[c]) > math.pi
    if not np.any(taglio):
        return math.nan, 0
    D = bfs(a[~taglio], c[~taglio], n, c[taglio])
    best = np.array([D[t, a[taglio][t]] for t in range(int(taglio.sum()))])
    return (float(1 + best.min()) if np.isfinite(best).any() else math.nan), int(taglio.sum())


def coppie(r0, ang0):
    """### `6` coppie fisse di nodi opposti dell'anello `40` *(dalle posizioni ORIGINARIE)*."""
    an = np.nonzero((r0 >= R_ANELLO - 0.5) & (r0 < R_ANELLO + 0.5))[0]
    out = []
    for g in ANGOLI:
        t = math.radians(g)
        da = lambda x: np.abs(np.angle(np.exp(1j * (ang0[an] - x))))
        out.append((int(an[np.argmin(da(t))]), int(an[np.argmin(da(t + math.pi))])))
    return out


def esterna(ii, jj, n, dentro, cp):
    e = ~(dentro[ii] | dentro[jj])
    D = bfs(ii[e], jj[e], n, [a for a, _ in cp])
    return [float(D[t, b]) for t, (_, b) in enumerate(cp)]


def misura(ii, jj, n, m1, m2, c, nati, cp):
    r, ang = polari(m1, m2, c)
    b = fascia(r, n, nati)
    ci, nt = circonferenza(ii, jj, n, b, ang)
    ex = esterna(ii, jj, n, r < R_DENTRO, cp)
    return ci, ex, int(b.sum()), nt, r


def dividi(ii, jj, m1, m2, quali):
    """### ogni arco in `quali` diviso in due da un nodo nuovo al suo punto medio: `(ii, jj, n, m1, m2, nati)`."""
    q = np.nonzero(quali)[0]
    n0 = len(m1)
    nuovi = n0 + np.arange(q.size)
    x1, x2 = mezzo(m1, m2, ii[q], jj[q])
    tieni = ~quali
    ii2 = np.concatenate([ii[tieni], ii[q], nuovi])
    jj2 = np.concatenate([jj[tieni], nuovi, jj[q]])
    return ii2, jj2, n0 + q.size, np.concatenate([m1, x1]), np.concatenate([m2, x2]), [(int(ii[t]), int(jj[t]), int(x)) for t, x in zip(q, nuovi)]


def ultimo(d, pat="stato_*.npz"):
    for f in sorted(glob.glob(os.path.join(d, pat)), reverse=True):
        if os.path.exists(f + ".sha1") and open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f):
            return f
    return None


def prova(base):
    f = ultimo(os.path.join(base, "TRONCO"))
    k, ii, jj, n, m1, m2, c = leggi(f)
    assert n == N0, "la prova vuole il toro (lo stato %s ha %d nodi)" % (f, n)
    r0, ang0 = polari(m1, m2, c)
    cp = coppie(r0, ang0)
    print("### IL TORO di %s (k %d, il centro %.3f %.3f); le coppie opposte: %s" % (os.path.basename(f), k, c[0], c[1], cp))
    ci, ex, nb_, nt, r = misura(ii, jj, n, m1, m2, c, [], cp)
    print("### LA SCALA: la circonferenza %.0f passi (la fascia %d nodi, %d archi del taglio) contro 2 pi 40 = %.1f: il rapporto %.4f" % (ci, nb_, nt, 2 * math.pi * 40, ci / (2 * math.pi * 40)))
    print("    la distanza esterna %s, la media %.2f, contro pi 40 = %.1f: il rapporto %.4f" % ([int(x) for x in ex], np.mean(ex), math.pi * 40, np.mean(ex) / (math.pi * 40)))
    ok = 2 * math.pi * 40 <= ci <= 1.3 * 2 * math.pi * 40
    print("    ### la scala (la circonferenza fra 2 pi 40 e 1.3 volte): %s" % ("OK" if ok else "NON TORNA"))
    b = (r >= R_ANELLO - 0.5) & (r < R_ANELLO + 0.5)
    casi = (("ogni arco della FASCIA diviso", b[ii] & b[jj], "circ", 2.0),
            ("ogni arco FUORI dall'anello 20 diviso", ~((r < R_DENTRO)[ii] | (r < R_DENTRO)[jj]), "est", 2.0),
            ("ogni arco DENTRO l'anello 20 diviso (deve restare fermo)", (r < R_DENTRO)[ii] & (r < R_DENTRO)[jj], "tutte", 1.0))
    for nome, q, cosa, att in casi:
        i2, j2, n2, a1, a2, nati = dividi(ii, jj, m1, m2, q)
        c2, e2, _, _, _ = misura(i2, j2, n2, a1, a2, c, nati, cp)
        rc, re = c2 / ci, np.array(e2) / np.array(ex)
        if cosa == "circ":
            v = rc == att
        elif cosa == "est":
            v = bool(np.all(re == att))
        else:
            v = rc == 1.0 and bool(np.all(re == 1.0))
        print("### %s (%d archi): la circonferenza %.0f (x %.4f), la distanza esterna %s (x %s): atteso x %.0f su %s -> %s" % (
            nome, int(q.sum()), c2, rc, [int(x) for x in e2], [round(float(x), 4) for x in re], att, cosa, "OK" if v else "NON TORNA"))
        ok &= v
    print("### LA PROVA: %s" % ("PASSA" if ok else "NON PASSA: FERMO"))
    return 0 if ok else 1


def d1(d, k):
    f = os.path.join(d, "serie_%05d.npz" % k)
    if not os.path.exists(f):
        return math.nan
    with np.load(f) as s:
        if "D_k" not in s.files:
            return math.nan
        w = np.nonzero(np.asarray(s["D_k"]) == k)[0]
        return float(np.asarray(s["D_med40"])[w[-1]]) if w.size else math.nan


def nati_di(d, k):
    f = os.path.join(d, "nascite_%05d.json" % k)
    if not os.path.exists(f):
        return []
    with open(f, encoding="utf-8") as fh:
        B = json.load(fh)
    return [(int(b["nodi"]["i"]), int(b["nodi"]["j"]), int(b["nodi"]["n"])) for b in B]


def rami(base):
    with open(os.path.join(base, "TRONCO", "scatto.json"), encoding="utf-8") as fh:
        sj = json.load(fh)
    k0, ii, jj, n, m1, m2, c = leggi(sj["file"])
    r0, ang0 = polari(m1[:N0], m2[:N0], c)
    cp = coppie(r0, ang0)
    ci0, ex0, _, _, _ = misura(ii, jj, n, m1, m2, c, [], cp)
    print("### IL PUNTO DI RAMIFICAZIONE k %d: la circonferenza %.0f, la distanza esterna %s (la media %.2f); le coppie %s" % (k0, ci0, [int(x) for x in ex0], np.mean(ex0), cp))
    for nome in ("MITOSI", "C2EXT"):
        d = os.path.join(base, nome)
        fs = sorted(f for f in glob.glob(os.path.join(d, "stato_*.npz")) if os.path.exists(f + ".sha1"))
        print("### %s: %d stati" % (nome, len(fs)))
        print("       k    D1(passi)   circ   circ-circ0   est media   est-est0   nascite   r>=20.5   nella fascia   le 6 distanze")
        fermo = True
        for f in fs:
            k, ii, jj, n, m1, m2, c_ = leggi(f)
            assert c_ == c, "il centro dello stato non e' quello del punto di ramificazione"
            nati = nati_di(d, k)
            ci, ex, _, _, r = misura(ii, jj, n, m1, m2, c, nati, cp)
            fuori = sum(1 for _, _, x in nati if r[x] >= R_DENTRO)
            fa = int(np.sum(fascia(r, n, nati)[N0:]))
            print("    %5d    %8.1f   %5.0f   %+9.0f    %9.2f   %+8.2f   %7d   %7d   %12d   %s" % (
                k, d1(d, k), ci, ci - ci0, np.mean(ex), np.mean(ex) - np.mean(ex0), len(nati), fuori, fa, [int(x) for x in ex]))
            fermo &= ci == ci0 and ex == ex0
        if nome == "C2EXT":
            print("### IL CONTROLLO FERMO (C2-EXT, il grafo non cambia): %s" % ("IDENTICO a ogni stato" if fermo else "SI MUOVE: FERMO"))
    return 0


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("prova", "rami"))
    ap.add_argument("--base", required=True)
    x = ap.parse_args(argv)
    print("=" * 130)
    print("LA CIRCONFERENZA DELL'ANELLO 40 E LA DISTANZA ESTERNA (Luca 2026-11-21 14:06; la carta sez. 17): %s" % x.cosa)
    print("=" * 130)
    rc = prova(x.base) if x.cosa == "prova" else rami(x.base)
    print("=" * 130)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
