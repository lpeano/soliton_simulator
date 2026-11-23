# -*- coding: utf-8 -*-
r"""**[M1658-S] 1a, L'ADDENDUM DELLA v2: IL FIT QUADRATICO E IL FIT LINEARE AL FONDO A K** *(la carta `doc/CARTA_fondo_giusto.md`, sez. `2-ter`; in memoria)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_K.py > doc/referti_l2/fondo_K.txt

**`A(k)`** da `fondo_materia.risposta` *(le righe di `torneo_fondo_v2`)*; K `(B0 + B1)/3`; lungo i versori di `B0`, `B1`, `20` punti `delta` in `(0, 0.15]`; per i due rami della coppia *(la finestra `[0.20, 0.30]`)*: (Q) `a delta^2`, (L) `v delta`, senza intercetta; «regge» se il residuo relativo massimo `< 5%`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_materia as FM  # noqa: E402

DELTE = np.linspace(0.0075, 0.15, 20)
FIN = (0.20, 0.30)


def fit(x, y):
    a = float(np.sum(x * y) / np.sum(x * x))
    r = y - a * x
    sa = float(np.sqrt(np.sum(r ** 2) / (len(x) - 1) / np.sum(x * x)))
    return a, sa, float(np.max(np.abs(r) / np.abs(y)))


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "fondo_materia.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1658-S] 1a, L'ADDENDUM v2: IL FIT QUADRATICO E LINEARE AL FONDO A K (|k - k_K| in (0, 0.15], 20 punti)")
    print("=" * 130)
    R, d0, _stampo, _L, _s = FM.risposta()
    sup = np.nonzero(np.abs(R).reshape(R.shape[0], -1).max(axis=1) > 0.0)[0]
    Rs, ds = R[sup], d0[sup]
    A1, A2 = TO.vettori()
    B = 2.0 * np.pi * np.linalg.inv(np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]])).T
    kK = (B[0] + B[1]) / 3.0

    def E_di(kv):
        return np.sort(-np.angle(np.linalg.eigvals(np.einsum("x,xij->ij", np.exp(-1j * (ds @ kv)), Rs))))
    E0 = E_di(kK)
    w0 = E0[(E0 > FIN[0]) & (E0 < FIN[1])]
    EK = float(w0.mean())
    m = int(np.sum(np.abs(E0 - EK) < 1e-9))
    print("### K: le quasi-energie nella finestra %s; E_K %+.10f; la molteplicita' %d" % (" ".join("%+.10f" % x for x in w0), EK, m))
    curvo, cono, piatto = True, True, True
    for nome, u in (("B0", B[0] / np.linalg.norm(B[0])), ("B1", B[1] / np.linalg.norm(B[1]))):
        Y = []
        for dl in DELTE:
            E = E_di(kK + dl * u)
            Y.append(np.sort(E[(E > FIN[0]) & (E < FIN[1])]) - EK)
        Y = np.array(Y)
        for b in range(Y.shape[1]):
            y = Y[:, b]
            a, sa, ra = fit(DELTE ** 2, y)
            v, sv, rv = fit(DELTE, y)
            print("  lungo %s, il ramo %d: (Q) a %+.6e +- %.1e, il residuo relativo massimo %.4f (%s); (L) v %+.6e +- %.1e, il residuo %.4f (%s); E - E_K da %+.3e a %+.3e" % (
                nome, b, a, sa, ra, "REGGE" if ra < 0.05 else "no", v, sv, rv, "REGGE" if rv < 0.05 else "no", float(y.min()), float(y.max())))
            curvo = curvo and ra < 0.05 and a > 0
            cono = cono and rv < 0.05 and v > 0 and not ra < 0.05
            piatto = piatto and float(np.max(np.abs(y))) < 1e-6
    v = "FONDO CURVO" if (curvo and m <= 2) else ("CONO" if cono else ("PIATTO" if piatto else "NESSUNO DEI TRE"))
    print("=" * 130)
    print("### IL VERDETTO (K2): %s" % v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
