# -*- coding: utf-8 -*-
r"""**LA PROVA DI B4: LE POSIZIONI E LA SCENA CHE CRESCE, v2** *(il ramo `mitosi`; mandato di Luca `2026-11-20` `10:31`)*.

    E:\python\py3132\python.exe csv/solitone/prova_posizioni_v2.py > doc/referti_l2/mitosi_B4_posizioni.txt

**La v2** *(DICHIARATO)*: la v1 (`prova_posizioni.py`, `68089e6d`) si e' FERMATA con un `KeyError`: la sua scena finta NON aveva la chiave `righe`, e `cresci` sostituisce solo le chiavi che ci sono. **Un errore della PROVA, non del modulo.** La v2 mette `righe` nella scena finta; il resto e' la v1 riga per riga.

**Il toro** `L 24` *(gli archi `a1`, `a2`, `a1 + a2`, come `prova_u1_generico.toro`)*; **la crescita:** `Incidenza.cresci` con la divisione di `prova_u1_generico.dividi`.
- **`righe(inc)` = `argsort(nodo, kind="stable").reshape(n, 6)` AL BIT** *(la riga che c'era nelle due scene)*; dopo la crescita **RIFIUTA**;
- **`toro.centro` e `toro.scarti` con le posizioni FLOAT = con gli indici INTERI, AL BIT** *(una `rho` a caso, seme `0`)*;
- **il nodo nato al PUNTO MEDIO:** la distanza da `i` e da `j` = meta' della lunghezza dell'arco, **anche su un arco che attraversa la cucitura del toro**;
- **`cresci(Z, ...)`:** `n`, `nodo`, le posizioni crescono; `g_e` a zero; **`righe`, `phi_v`, `stato`, `metti`, `g_nodo` RIFIUTANO**;
- **`mappe.scrivi`:** con le posizioni intere **gli stessi array** della versione del padre *(`d1`, `d2` `int16`)*; con un nodo nato `float64`; **un'istantanea di un'altra taglia RIFIUTATA**;
- **I CASI CHE DEVONO FALLIRE:** `cresci` prima che il grafo cresca; `cresci` con un bordo NON nullo; `righe` su un grafo con un nodo di grado `7`.
"""
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


class _Mot(object):
    def __init__(self, inc):
        self.inc = inc


def alza(f):
    try:
        f()
    except (AssertionError, RuntimeError):
        return True
    return False


def scena(IN, ii, jj, n):
    inc = IN.Incidenza(ii, jj, n, len(ii))
    v = np.arange(n)
    import posizioni as PZ
    return {"mot": _Mot(inc), "n": n, "L": L, "nodo": np.asarray(inc.nodo), "m1": v // L, "m2": v % L,
            "righe": PZ.righe(inc), "g_e": np.zeros(2 * len(ii)), "phi_v": np.ones(2 * len(ii), dtype=complex), "stato": {}, "metti": lambda: None, "g_nodo": np.zeros(n)}


def main():
    import _presidio
    import incidenza as IN
    import mappe as MP
    import posizioni as PZ
    import prova_u1_generico as PU
    import toro as TO
    _presidio.avvia(os.path.join(_QUI, "posizioni.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA PROVA DI B4: LE POSIZIONI E LA SCENA CHE CRESCE, v2 (il ramo mitosi; Luca 2026-11-20 10:31)")
    print("=" * 130)
    esiti = []
    ii, jj, n, vec = PU.toro(L)
    Z = scena(IN, ii, jj, n)
    inc = Z["mot"].inc
    R = PZ.righe(inc)
    R0 = np.argsort(np.asarray(inc.nodo), kind="stable").reshape(n, 6)
    esiti.append(("righe(inc) = argsort(nodo, stable).reshape(n, 6) AL BIT (valori e tipo)", np.array_equal(R, R0) and R.dtype == R0.dtype))
    rng = np.random.default_rng(SEME)
    rho = rng.random(n)
    m1i, m2i = Z["m1"], Z["m2"]
    m1f, m2f = m1i.astype(float), m2i.astype(float)
    ci, cf = TO.centro(rho, m1i, m2i, L), TO.centro(rho, m1f, m2f, L)
    si, sf = TO.scarti(m1i, m2i, ci[0], ci[1], L), TO.scarti(m1f, m2f, cf[0], cf[1], L)
    esiti.append(("toro.centro e toro.scarti con le posizioni float = con gli indici interi AL BIT", ci == cf and np.array_equal(si, sf)))
    # ------------------------------------------------------------------ i casi che devono fallire, prima della crescita
    esiti.append(("DEVE FALLIRE: cresci PRIMA che il grafo cresca", alza(lambda: PZ.cresci(Z, 0, 1, 1))))
    # ------------------------------------------------------------------ la crescita: un arco dentro, uno sulla cucitura
    lun = float(np.hypot(*vec[0]))
    for nome, a in (("dentro il toro", 3 * (5 * L + 7)), ("sulla cucitura (m1 = L - 1 -> 0)", 3 * ((L - 1) * L + 7))):
        Z = scena(IN, ii, jj, n)
        inc = Z["mot"].inc
        tieni, nii, njj, _vn, nodi, _d = PU.dividi(ii, jj, n, vec, a)
        inc.cresci(tieni, np.array(nii), np.array(njj), 1)
        p1, p2 = PZ.cresci(Z, nodi["i"], nodi["j"], 1)
        di = float(np.hypot(*TO.scarti(np.array([p1]), np.array([p2]), Z["m1"][nodi["i"]], Z["m2"][nodi["i"]], L)[0][:2]))
        dj = float(np.hypot(*TO.scarti(np.array([p1]), np.array([p2]), Z["m1"][nodi["j"]], Z["m2"][nodi["j"]], L)[0][:2]))
        print("### %s: l'arco %d (%d -> %d); il nodo nato a (%.3f, %.3f); la distanza da i %.15f, da j %.15f (meta' arco %.15f)" % (nome, a, nodi["i"], nodi["j"], p1, p2, di, dj, 0.5 * lun))
        esiti.append(("il nodo nato al punto medio, %s: distanza da i e da j = meta' arco entro 1e-14" % nome, abs(di - 0.5 * lun) < 1e-14 and abs(dj - 0.5 * lun) < 1e-14))
        cresciuta = (Z["n"] == n + 1 and len(Z["m1"]) == n + 1 and Z["m1"].dtype == float and np.array_equal(Z["nodo"], np.asarray(inc.nodo))
                     and len(Z["g_e"]) == 2 * inc.m and float(np.max(np.abs(Z["g_e"]))) == 0.0 and np.array_equal(Z["m1"][:n], m1f))
        esiti.append(("cresci, %s: n, nodo, le posizioni (le vecchie al bit), g_e a zero della taglia nuova" % nome, cresciuta))
        rif = all(alza(f) for f in (lambda: Z["righe"][0], lambda: Z["phi_v"][0], lambda: Z["stato"]["psi_h"], lambda: Z["metti"](), lambda: Z["g_nodo"][0], lambda: PZ.righe(inc)))
        esiti.append(("cresci, %s: righe, phi_v, stato, metti, g_nodo e righe(inc) RIFIUTANO" % nome, rif))
    # ------------------------------------------------------------------ il bordo non nullo
    Z = scena(IN, ii, jj, n)
    Z["g_e"][0] = 0.5
    tieni, nii, njj, _vn, nodi, _d = PU.dividi(ii, jj, n, vec, 0)
    Z["mot"].inc.cresci(tieni, np.array(nii), np.array(njj), 1)
    esiti.append(("DEVE FALLIRE: cresci con un bordo NON nullo (g_e != 0)", alza(lambda: PZ.cresci(Z, nodi["i"], nodi["j"], 1))))
    # ------------------------------------------------------------------ mappe
    ist = [{"t": 1, "rho": rho.astype(np.float32), "Lambda": rho.astype(np.float32), "centro": np.array([1.0, 2.0]), "lam": 0.5}]
    with tempfile.TemporaryDirectory() as dd:
        f1 = os.path.join(dd, "a.npz")
        MP.scrivi(f1, ist, m1i, m2i, L)
        X = MP.leggi(f1)
        prima = {"d1": (np.asarray(m1i) - L // 2).astype(np.int16), "d2": (np.asarray(m2i) - L // 2).astype(np.int16)}
        esiti.append(("mappe, le posizioni intere: d1 e d2 = la riga del padre (int16) AL BIT", all(np.array_equal(X[k], prima[k]) and X[k].dtype == np.int16 for k in prima)))
        m1g, m2g = np.concatenate([m1f, [3.5]]), np.concatenate([m2f, [7.0]])
        ist2 = [dict(ist[0], rho=np.concatenate([rho, [0.1]]).astype(np.float32))]
        f2 = os.path.join(dd, "b.npz")
        MP.scrivi(f2, ist2, m1g, m2g, L)
        X2 = MP.leggi(f2)
        esiti.append(("mappe, un nodo nato: d1, d2 float64 con la meta' (3.5 - L/2)", X2["d1"].dtype == np.float64 and X2["d1"][-1] == 3.5 - L // 2))
        esiti.append(("DEVE FALLIRE: mappe con un'istantanea di un'altra taglia", alza(lambda: MP.scrivi(os.path.join(dd, "c.npz"), ist, m1g, m2g, L))))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-118s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
