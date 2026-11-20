# -*- coding: utf-8 -*-
r"""**LA PROVA DELLA MEMORIA PER ARCO `Theta`** *(il ramo `mitosi`; mandato di Luca `2026-11-20` `10:31`, TODO 3)*.

    E:\python\py3132\python.exe csv/solitone/prova_contatore.py > doc/referti_l2/mitosi_contatore.txt

**Il caso noto** *(Q-A4)*: **`Theta` a `k 3000` di C2 dai `12` segmenti** *(`E:/soliton_simulator/controllo/torsione/C2_<k0>.npz`, `torsione_segmenti.py` del ramo `primo-ordine`)* **= la riga di `innesco_stima.py`** *(`np.sum([acc], axis=0)`)* **AL BIT**; **contro `theta3000` di `candidati.npz`** *(la somma cumulata tick per tick: un altro ordine)* **entro `1e-12` rad**; **nessun arco a `2 pi` a `k 3000`** *(il primo a `2.79e4`: `torsione_segmenti.txt`)*.
**Il toro** `L 24` *(`prova_u1_generico.toro`)*: **`ritmo` contro il conto arco per arco** *(un ciclo, `cs` a caso, seme `0`)* **AL BIT**; **la crescita** *(`Incidenza.cresci` con `prova_u1_generico.dividi`)*: **ogni arco tenuto conserva il suo `Theta` AL BIT** *(cercato per `(ii, jj)`)*, **i `4` nuovi a `0`, l'arco diviso CONSUMATO**; **`scattati` ordinati per indice, `2 pi` esatto compreso**; **P8: salva e riprendi da un `.npz` AL BIT.**
**I CASI CHE DEVONO FALLIRE:** `mot.dtau != 1`; `accumula` su un grafo cresciuto senza `cresci` del contatore; `cresci` con una maschera non booleana.
"""
import math
import os
import sys
import tempfile

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
_RADICE = os.path.dirname(_CSV)
for _p in (_QUI, _CSV, os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

L, SEME = 24, 0
DIR_T = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "torsione")
K0S = tuple(range(0, 3000, 250))


class _Mot(object):
    def __init__(self, inc, dtau):
        self.inc, self.dtau = inc, dtau


def alza(f):
    try:
        f()
    except (AssertionError, RuntimeError):
        return True
    return False


def main():
    import _presidio
    import contatore as CO
    import incidenza as IN
    import prova_u1_generico as PU
    _presidio.avvia(os.path.join(_QUI, "contatore.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA PROVA DELLA MEMORIA PER ARCO THETA (il ramo mitosi; Luca 2026-11-20 10:31)")
    print("=" * 130)
    esiti = []
    # ------------------------------------------------------------------ il caso noto: C2 a k 3000
    acc = []
    for k0 in K0S:
        with np.load(os.path.join(DIR_T, "C2_%05d.npz" % k0)) as d:
            acc.append(d["acc"].copy())
    C = CO.Contatore.da_segmenti(acc)
    Th = np.sum(acc, axis=0)
    with np.load(os.path.join(DIR_T, "candidati.npz")) as d:
        archi, th3 = d["archi"].copy(), d["theta3000"].copy()
    dmax = float(np.max(np.abs(C.theta[archi] - th3)))
    print("### IL CASO NOTO: Theta a k 3000 dai %d segmenti di C2: %d archi, max |Theta| %.6e rad; contro la riga di innesco_stima.py AL BIT %s; contro theta3000 di candidati.npz (%d archi) max %.3e rad; scattati %d" % (
        len(acc), C.theta.size, float(np.max(np.abs(C.theta))), np.array_equal(C.theta, Th), archi.size, dmax, C.scattati().size))
    esiti.append(("il caso noto: Theta(3000) = np.sum(acc, axis=0) di innesco_stima.py AL BIT", np.array_equal(C.theta, Th)))
    esiti.append(("il caso noto: contro theta3000 di candidati.npz (la somma tick per tick) entro 1e-12 rad", dmax < 1e-12))
    esiti.append(("il caso noto: nessun arco a 2 pi a k 3000 (il primo a 2.79e4, torsione_segmenti.txt)", C.scattati().size == 0))
    # ------------------------------------------------------------------ il toro L 24: ritmo
    ii, jj, n, vec = PU.toro(L)
    inc = IN.Incidenza(ii, jj, n, len(ii))
    rng = np.random.default_rng(SEME)
    cs = 0.5 + rng.random(n)
    mot = _Mot(inc, np.ones(n))
    r = CO.ritmo(mot, cs)
    r0 = np.array([math.pi * (1.0 * cs[int(ii[a])] - 1.0 * cs[int(jj[a])]) for a in range(len(ii))])
    esiti.append(("ritmo = pi (dtau cs_i - dtau cs_j) arco per arco AL BIT (L 24, cs a caso)", np.array_equal(r, r0)))
    esiti.append(("DEVE FALLIRE: mot.dtau != 1", alza(lambda: CO.ritmo(_Mot(inc, np.full(n, 0.5)), cs))))
    # ------------------------------------------------------------------ la crescita
    C = CO.Contatore(rng.standard_normal(len(ii)) * 3.0)
    C.theta[5] = 2.0 * math.pi
    C.theta[2] = -2.0 * math.pi
    sc = C.scattati()
    atteso = np.nonzero(np.abs(C.theta) >= 2.0 * math.pi)[0]
    esiti.append(("scattati: ordinati per indice, 2 pi esatto compreso (gli archi 2 e 5 dentro)", np.array_equal(sc, atteso) and np.all(np.diff(sc) > 0) and 2 in sc and 5 in sc))
    prima = {(int(x), int(y)): float(t) for x, y, t in zip(ii, jj, C.theta)}
    a = 3 * (7 * L + 9)
    tieni, nii, njj, _vn, nodi, _d = PU.dividi(ii, jj, n, vec, a)
    inc.cresci(tieni, np.array(nii), np.array(njj), 1)
    esiti.append(("DEVE FALLIRE: accumula su un grafo cresciuto senza cresci del contatore", alza(lambda: C.accumula(_Mot(inc, np.ones(n + 1)), np.ones(n + 1)))))
    esiti.append(("DEVE FALLIRE: cresci con una maschera non booleana", alza(lambda: CO.Contatore(C.theta.copy()).cresci(np.nonzero(tieni)[0], 4))))
    C.cresci(tieni, 4)
    ii2, jj2 = np.asarray(inc.ii), np.asarray(inc.jj)
    tenuti = all(C.theta[q] == prima[(int(ii2[q]), int(jj2[q]))] for q in range(len(ii2) - 4))
    nuovi0 = bool(np.all(C.theta[-4:] == 0.0))
    consumato = (int(ii[a]), int(jj[a])) not in {(int(x), int(y)) for x, y in zip(ii2, jj2)}
    print("### la crescita sull'arco %d (%d -> %d): gli archi %d -> %d; Theta dei tenuti al bit %s; i 4 nuovi a 0 %s; l'arco diviso consumato %s" % (a, ii[a], jj[a], len(ii), len(ii2), tenuti, nuovi0, consumato))
    esiti.append(("la crescita: ogni arco tenuto conserva Theta AL BIT, i 4 nuovi a 0, l'arco diviso consumato", tenuti and nuovi0 and consumato and C.theta.size == len(ii2)))
    t_prima = C.theta.copy()
    C.accumula(_Mot(inc, np.ones(n + 1)), np.ones(n + 1))
    esiti.append(("dopo la crescita accumula sul grafo nuovo (cs uniforme: il ritmo 0, Theta invariato AL BIT)", np.array_equal(C.theta, t_prima)))
    # ------------------------------------------------------------------ P8
    with tempfile.TemporaryDirectory() as dd:
        f = os.path.join(dd, "s.npz")
        np.savez(f, **C.salva({}))
        with np.load(f) as d:
            C2 = CO.Contatore.riprendi(d)
    esiti.append(("P8: salva e riprendi da un .npz AL BIT", np.array_equal(C2.theta, C.theta) and C2.theta.dtype == C.theta.dtype))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-118s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
