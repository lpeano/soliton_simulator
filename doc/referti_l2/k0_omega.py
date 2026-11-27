# -*- coding: utf-8 -*-
r"""**[M1107] LO SCARTO DI omega NELLA RIPRESA v9** *(la relazione, B5d, `e91d7462`, lo dichiara PRIMA; non e' un tentativo di correzione: misura)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/k0_omega.py > doc/referti_l2/k0_omega.txt

**La ripresa della v9** *(da `stato_005750`, `250` tick)*; **per `omega` di ciascun corpo**, contro `serie.json` *(i tick `5751..6000`)*: il numero di tick diversi, il massimo di `|d|`, il massimo relativo, e il massimo di `|d|` in unita' dell'ultimo bit *(`np.spacing`)*. **In piu'**, per il tick `5751`: `omega` ricalcolato dagli stessi due vettori con `np.vdot` e con la somma esplicita `np.sum(np.conj(a) * b)`, per vedere se il calcolo da' bit diversi sugli STESSI dati.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v9 as V9  # noqa: E402

V7 = V9.V7


def main():
    V7.avvia()
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 120)
    print("[M1107] LO SCARTO DI omega NELLA RIPRESA v9: da stato_005750, 250 tick, contro serie.json")
    print("=" * 120)
    S = V7.serie_d1()
    coppie = []
    with V7.GD.TC.scena() as Z:
        R = V7.Ripresa(Z, 5750)
        primo = {"prima": Z["st"]["psi_h"].copy()}

        def extra(ka):
            if ka == 5751:
                primo["dopo"] = Z["st"]["psi_h"].copy()
        R.gira(250, extra)
        Z["metti"]()
    del coppie
    for j in range(2):
        a, b = np.array(R.om[j]), np.array(S["omega"][j][5750:6000])
        d = np.abs(a - b)
        ulp = d / np.spacing(np.abs(b))
        print("  il corpo %d: %d tick diversi su %d; max |d| %.3e; max relativo %.3e; max in ulp %.1f" % (j + 1, int(np.count_nonzero(d)), d.size, float(d.max()), float((d / np.abs(b)).max()), float(ulp.max())))
    print("-" * 120)
    print("IL TICK 5751: omega dagli STESSI due vettori, np.vdot contro la somma esplicita, e il valore di serie.json")
    print("-" * 120)
    for j, ms in enumerate(R.maschere):
        x, y = primo["prima"][ms], primo["dopo"][ms]
        o1 = float(-np.angle(np.vdot(x, y)))
        o2 = float(-np.angle(np.sum(np.conj(x) * y)))
        o3 = float(-np.angle(np.vdot(x.copy(), y.copy())))
        print("  il corpo %d: vdot %r; vdot su copie %r; somma esplicita %r; serie.json %r" % (j + 1, o1, o3, o2, S["omega"][j][5750]))
    print("=" * 120)
    return 0


if __name__ == "__main__":
    sys.exit(main())
