# -*- coding: utf-8 -*-
r"""**I TRIANGOLI ESATTAMENTE EQUILATERI** *(Luca `2026-11-15` `02:08`, la costruzione del guardiano; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `22.4`)*.

    python csv/solitone/triangolo_equilatero.py prova > doc/referti_l2/mattone/triangolo_equilatero.txt

### **La costruzione:** **il primo vertice `P`** *(il nodo scelto, lo spostamento multiplo di `3` dal centro d'origine del mattone)*; **il secondo `P + 3 (a, b)`; il terzo `P + 3 R(a, b)`, `R` la rotazione di `60` gradi
sul reticolo triangolare NELLE COORDINATE DEI NODI.** ### **LA CONVENZIONE DEL CODICE** *(dichiarata)*: **`toro.vettori`: `A1 = (1, 0)`, `A2 = (-1/2, sqrt 3 / 2)`, cioe' `120` gradi fra `A1` e `A2`; la rotazione di `60`
gradi porta `A1` in `A1 + A2` e `A2` in `-A1`: `R(a, b) = (a - b, a)`; il lato `3 sqrt(a^2 - a b + b^2)`.** *(La formula di Luca `(-b, a + b)` e `3 sqrt(a^2 + a b + b^2)` e' la stessa rotazione nella convenzione a
`60` gradi; per `(13, 0)` il lato e' `39` in tutte e due.)*
### **DEVE:** **i tre lati veri uguali entro `1e-9`; il terzo vertice sui nodi buoni** *(lo spostamento da `P` multiplo di `3` nelle due coordinate)*; **DEVE FALLIRE: con la rotazione dell'altra convenzione `(-b, a + b)` i lati NON sono uguali** *(a `b != 0`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import solitone  # noqa: E402,F401

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))


def R(a, b):
    """### La rotazione di `60` gradi nelle coordinate dei nodi di QUESTO codice *(`A1`, `A2` a `120` gradi)*."""
    return a - b, a


def vertici(P, a, b, L):
    """### I tre vertici `P`, `P + 3 (a, b)`, `P + 3 R(a, b)`, nel toro di lato `L`."""
    ra, rb = R(a, b)
    return [[P[0] % L, P[1] % L], [(P[0] + 3 * a) % L, (P[1] + 3 * b) % L], [(P[0] + 3 * ra) % L, (P[1] + 3 * rb) % L]]


def lato(a, b):
    return 3.0 * math.sqrt(a * a - a * b + b * b)


def lati(V, L):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    out = []
    for i, j in ((0, 1), (1, 2), (2, 0)):
        d = TO.scarti(np.array([V[j][0]]), np.array([V[j][1]]), V[i][0], V[i][1], L)[0]
        out.append(float(np.hypot(d[0], d[1])))
    return out


def prova():
    import _presidio
    _presidio.avvia(__file__)
    L = 162
    P = (112, 107)                                   # ### il vertice A di (T-fase) (il nodo buono dal centro d'origine del mattone)
    print("=" * 130)
    print("I TRIANGOLI ESATTAMENTE EQUILATERI (Luca 02:08): P %s; la rotazione di 60 gradi nella convenzione del codice R(a, b) = (a - b, a)" % (P,))
    print("=" * 130)
    for a, b in ((13, 0), (0, 13), (13, 13), (8, 5), (-13, 0)):
        V = vertici(P, a, b, L)
        ll = lati(V, L)
        uguali = max(ll) - min(ll) <= 1e-9
        buoni = all((V[k][0] - P[0]) % 3 == 0 and (V[k][1] - P[1]) % 3 == 0 for k in range(3))
        print("    (a, b) = (%d, %d): i vertici %s; i lati veri %s; il lato atteso %.9f" % (a, b, V, ["%.12f" % x for x in ll], lato(a, b)))
        esito("(a, b) = (%d, %d): i tre lati uguali entro 1e-9 e i vertici sui nodi buoni" % (a, b), uguali and buoni and abs(ll[0] - lato(a, b)) <= 1e-9, "max - min %.3e; buoni %s" % (max(ll) - min(ll), buoni), True)
    a, b = 8, 5
    V = [[P[0], P[1]], [P[0] + 3 * a, P[1] + 3 * b], [P[0] - 3 * b, P[1] + 3 * (a + b)]]
    ll = lati(V, L)
    esito("l'altra convenzione (-b, a + b) a (8, 5): i lati uguali", max(ll) - min(ll) <= 1e-9, "i lati %s" % ["%.4f" % x for x in ll], False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s" % (OK[0], OK[1], FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(prova() if sys.argv[1:] == ["prova"] else 2)
