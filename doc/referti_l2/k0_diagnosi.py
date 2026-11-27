# -*- coding: utf-8 -*-
r"""**[M1016] LA DIAGNOSI DI K0': QUANTO SONO GRANDI LE DIFFERENZE** *(la relazione, il pezzo 3d, `755a781c`, la dichiara PRIMA; nessuna correzione; la via e' quella di `due_corpi_fondo_v8.py`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/k0_diagnosi.py > doc/referti_l2/k0_diagnosi.txt

**La stessa ripresa di K0'** *(da `stato_005750`, `250` tick, la v8)*. **Per ogni riga della serie** *(ogni `10` tick)*: il massimo di `|differenza|` fra le colonne della riga e quelle di `serie.json`, e il massimo relativo. **Per `omega`:** il primo tick diverso, e il massimo di `|differenza|` per blocchi di `10` tick. **Alla fine, per ogni chiave dello stato:** il massimo di `|differenza|` contro `stato_006000.npz`, il massimo relativo `max|d| / max|riferimento|`, e il numero di elementi diversi. **La lettura** *(la relazione, pezzo 3d)*: se la prima differenza e' relativa sotto `1e-12` e cresce piano, e' l'ordine delle operazioni, la piattaforma o la libreria; se e' grande gia' al primo tick, c'e' uno stato che la ripresa non carica.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v8 as V8  # noqa: E402

V7 = V8.V7


def main():
    V7.avvia()
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1016] LA DIAGNOSI DI K0': da stato_005750, 250 tick (la v8), contro serie.json e stato_006000.npz")
    print("=" * 130)
    S = V7.serie_d1()
    rif = {int(r[0]): np.array(r, float) for r in S["serie"]}
    with np.load(os.path.join(V7.D1, "stato_006000.npz")) as z:
        fin = {x: z[x].copy() for x in z.files if x != "meta"}
    with V7.GD.TC.scena() as Z:
        R = V7.Ripresa(Z, 5750)
        R.gira(250)
        dd = {k: np.asarray(v).copy() for k, v in R.dati().items()}
        Z["metti"]()
    print("-" * 130)
    print("LA SERIE: per riga, max |d| fra le colonne e max relativo (|d| / |riferimento|)")
    print("-" * 130)
    for r in R.serie:
        a, b = np.array(r, float), rif[int(r[0])]
        d = np.abs(a - b)
        rel = d / np.maximum(np.abs(b), 1e-300)
        print("  k %d: max |d| %.3e; max rel %.3e; le colonne diverse %s" % (int(r[0]), float(d.max()), float(rel.max()), [i for i in range(len(a)) if a[i] != b[i]]))
    print("-" * 130)
    print("omega: il primo tick diverso, e max |d| per blocchi di 10 tick")
    print("-" * 130)
    for j in range(2):
        a, b = np.array(R.om[j]), np.array(S["omega"][j][5750:6000])
        d = np.abs(a - b)
        nz = np.nonzero(d)[0]
        print("  il corpo %d: il primo tick diverso %s; max |d| per blocco: %s" % (j + 1, (5751 + int(nz[0])) if len(nz) else "nessuno", " ".join("%.1e" % float(d[i:i + 10].max()) for i in range(0, 250, 10))))
    print("-" * 130)
    print("LO STATO A k 6000: per chiave, max |d|, max |d| / max |riferimento|, elementi diversi")
    print("-" * 130)
    for x in fin:
        a, b = dd[x], fin[x]
        d = np.abs(a - b)
        print("  %-8s: max |d| %.3e; relativo %.3e; diversi %d su %d" % (x, float(d.max()), float(d.max()) / max(float(np.abs(b).max()), 1e-300), int(np.count_nonzero(d)), d.size))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
