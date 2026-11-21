# -*- coding: utf-8 -*-
r"""**LA PROIEZIONE DEL PRIMO SCATTO DAGLI STATI DEL TRONCO** *(Luca `2026-11-21` `12:56`: lo stato delle corse; il tronco ha passato `k 27888`, il primo scatto della stima, SENZA scattare)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_proiezione_scatto.py > doc/referti_l2/mitosi_proiezione_scatto.txt

**Legge, non tocca:** gli stati del tronco *(`E:/soliton_simulator/controllo/mitosi_rami/TRONCO/stato_<k>.npz`, la chiave `theta_a`, lo sha1 controllato)* e i candidati della stima *(`E:/soliton_simulator/controllo/torsione/candidati.npz`)*.
**Dice:** il `Theta` di oggi dei primi candidati della stima; il massimo `|Theta|` per `k`; **il primo arco a `2 pi`** col ritmo lineare da due punti diversi, e col fit quadratico di `|Theta|` sui `300` archi piu' vicini alla soglia; **quanti archi scattano entro `k 40000`** *(il `--fino` del tronco: oltre, il tronco esce SENZA scatto e i rami non partono)*.
### **E' UNA PROIEZIONE, non una misura:** il lapse si muove *(il ritmo dell'arco col `|Theta|` massimo scende tratto per tratto)*.
"""
import hashlib
import math
import os
import sys

import numpy as np

B = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_rami", "TRONCO")
F_CAND = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "torsione", "candidati.npz")
Q = 2.0 * math.pi
FINO = 40000


def theta(k):
    f = os.path.join(B, "stato_%05d.npz" % k)
    with open(f, "rb") as fh:
        h = hashlib.sha1(fh.read()).hexdigest()
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == h, "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        return d["theta_a"].copy()


def main():
    sys.path[:0] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "csv")]
    import _presidio
    _presidio.avvia(__file__)
    ks = sorted(int(n[6:11]) for n in os.listdir(B) if n.startswith("stato_") and n.endswith(".npz"))
    kU = ks[-1]
    print("=" * 120)
    print("LA PROIEZIONE DEL PRIMO SCATTO DAGLI STATI DEL TRONCO (Luca 2026-11-21 12:56); l'ultimo stato k %d" % kU)
    print("=" * 120)
    U = theta(kU)
    with np.load(F_CAND) as c:
        A, T = c["archi"].copy(), c["T"].copy()
    o = np.argsort(T)[:3]
    print("### I PRIMI TRE CANDIDATI DELLA STIMA (lineare da C2 a k 3000) e il loro Theta a k %d (la soglia %.4f):" % (kU, Q))
    for i in o:
        print("    l'arco %d: T %.2f; Theta a k %d %+.6f" % (A[i], T[i], kU, U[A[i]]))
    kk = [k for k in (13750, 20000, 25000, 27000) if k in ks] + [kU]
    S = {k: theta(k) for k in kk}
    print("### il massimo |Theta| per k: %s" % ", ".join("k %d %.4f (l'arco %d)" % (k, np.abs(S[k]).max(), int(np.argmax(np.abs(S[k])))) for k in kk))
    im = int(np.argmax(np.abs(U)))
    print("### l'arco col |Theta| massimo (%d), il ritmo per tratto (1e-4 per tick): %s" % (im, ", ".join(
        "%d-%d %.4f" % (kk[j], kk[j + 1], (S[kk[j + 1]][im] - S[kk[j]][im]) / (kk[j + 1] - kk[j]) * 1e4) for j in range(len(kk) - 1))))
    print("### IL RITMO LINEARE (da k0 a k %d):" % kU)
    for k0 in [k for k in (25000, 27000) if k in S]:
        v = (U - S[k0]) / (kU - k0)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where((np.sign(v) == np.sign(U)) & (v != 0), (Q - np.abs(U)) / np.abs(v), np.inf)
        i = int(np.argmin(t))
        print("    da k %d: il primo a 2 pi l'arco %d a k %.0f; gli archi entro k %d: %d" % (k0, i, kU + t[i], FINO, int(np.sum(kU + t <= FINO))))
    kq = [k for k in ks if k >= kU - 5750 and (k - (kU - 5750)) % 250 == 0]
    M = np.array([theta(k) for k in kq])
    K = np.array(kq, dtype=float) - kU
    top = np.argsort(-np.abs(U))[:300]
    best = []
    for i in top:
        c = np.polyfit(K, np.abs(M[:, i]), 2)
        r = [x.real for x in np.roots([c[0], c[1], c[2] - Q]) if abs(x.imag) < 1e-9 and x.real > 0]
        best.append((min(r) if r else np.inf, int(i), c))
    best.sort(key=lambda x: x[0])
    fin = [x for x in best if np.isfinite(x[0])]
    print("### IL FIT QUADRATICO di |Theta| su %d stati (k %d-%d), i 300 archi col |Theta| maggiore: %d arrivano a 2 pi; entro k %d: %d" % (
        len(kq), kq[0], kq[-1], len(fin), FINO, sum(1 for x in fin if kU + x[0] <= FINO)))
    for t, i, c in best[:3]:
        print("    l'arco %d: a k %.0f (la curvatura %.2e, il ritmo oggi %.3e)" % (i, kU + t, c[0], c[1]))
    print("=" * 120)
    return 0


if __name__ == "__main__":
    sys.exit(main())
