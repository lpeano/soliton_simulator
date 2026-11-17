# -*- coding: utf-8 -*-
r"""**LE REGOLE PER LA FASE DEL VUOTO SULLE ESTREMITA' NUOVE, SENZA D7** *(Luca `2026-11-17` `16:38`, A1-A2; la carta `doc/TASK_HISTORY/2026-11-17_mitosi_verso_il_test.md`, sez. `1`)*.

    E:\python\py3132\python.exe doc/referti_l2/regole_fase_F3.py > doc/referti_l2/regole_fase_F3.txt

**La mossa:** la divisione generica di `nascita_dentro_fuori.py` *(`nasci`: l'arco `a = i -> j`, il padre `i`, `n -> i, j, k, l`)*; **i MODULI come v4** *(uniformi sulle estremita' di `S` alla norma `N_S` di prima: `V` esatta)*; **le FASI:**
- **v4-F3** *(la regola di oggi: le fasi di v1, cioe' di D7: `chiv / |chiv|` sulle estremita' nuove in `n`)*;
- **FA «antipodale»:** ogni arco nuovo con le estremita' OPPOSTE come in F3; in `i` e `j` le fasi delle estremita' dell'arco tolto *(il trasporto)*, in `n` le opposte; **`n -> k`, `n -> l`: in `n` la fase dell'estremita' di `i` sugli archi `i -> k`, `i -> l`; in `k`, `l` le opposte**;
- **FT «trasporto del padre»:** in `n` la fase dell'estremita' di `i` nella STESSA direzione *(`n -> j`: l'arco tolto; `n -> i`: l'arco di `i` nella direzione opposta; `n -> k`, `n -> l`: `i -> k`, `i -> l`)*; in `i` e `j` il trasporto; in `k`, `l` le opposte di quelle in `n`.
**I casi:** il vuoto F3 puro della scena S162 *(`psi = 0`)*; il mattone `L162_MGU_03000` con l'arco agli anelli `23.81`, `30`, `60` *(il criterio di `nascita_dentro_fuori.py`)*. **`Delta H`** *(le famiglie)*, `V`; **la sensibilita':** il vuoto perturbato di `1e-12` relativo *(seme `11`)*, la differenza di `Delta H`.
**Il caso noto** *(Q-A4)*: la v4-F3 di questo script = `nascita_dentro_fuori.v4f3` AL BIT, e all'anello `60` il `Delta H` di `nascita_dentro_fuori.txt` *(`+2.611234e+01`)* alla precisione stampata.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
_PO = os.path.join(_RADICE, "primo_ordine")
for _p in (_QUI, _SOL, _CSV, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import nascita_dentro_fuori as ND  # noqa: E402

REGOLE = ("v4-F3", "FA", "FT")


def fase(z):
    return z / abs(z) if abs(z) > 0 else complex("nan")


def estremita_di(ii, jj, phi, x, y):
    """### l'estremita' in `x` dell'arco fra `x` e `y` (il suo valore)."""
    a = np.where((ii == x) & (jj == y))[0]
    if len(a):
        return phi[2 * a[0]]
    a = np.where((ii == y) & (jj == x))[0]
    return phi[2 * a[0] + 1]


def opposto(G, i, va):
    """### il vicino di `i` nella direzione `-va`."""
    ii, jj, _nn, vec = G
    for a in np.where(ii == i)[0]:
        if np.allclose(vec[a], -va, atol=1e-9):
            return int(jj[a])
    for a in np.where(jj == i)[0]:
        if np.allclose(-vec[a], -va, atol=1e-9):
            return int(ii[a])
    raise RuntimeError("nessun vicino di %d nella direzione opposta" % i)


def regola(nome, G, phi, a, out):
    """### `phi` dopo la nascita secondo la regola (i moduli v4; le fasi della regola)."""
    import _conto_del_vuoto as C3
    ii, jj, nn, vec = G
    G2, _psi2, phi1, nodi = out[0], out[1], out[2], out[3]
    n, i, j, k, l = nodi["n"], nodi["i"], nodi["j"], nodi["k"], nodi["l"]
    if nome == "v4-F3":
        return ND.v4f3(G, phi, G2, phi1, n)
    base = len(G2[0]) - 4
    f = phi1.copy()
    ei, ej = phi[2 * a], phi[2 * a + 1]                       # le estremita' dell'arco tolto, in i e in j
    eik, eil = estremita_di(ii, jj, phi, i, k), estremita_di(ii, jj, phi, i, l)
    if nome == "FA":
        fn = {0: -fase(ei), 1: -fase(ej), 2: fase(eik), 3: fase(eil)}
    else:
        jo = opposto(G, i, vec[a])
        fn = {0: fase(estremita_di(ii, jj, phi, i, jo)), 1: fase(ei), 2: fase(eik), 3: fase(eil)}
    for q in range(4):
        f[2 * (base + q)] = fn[q]
    f[2 * (base + 0) + 1] = fase(ei) if nome == "FA" else fase(phi1[2 * (base + 0) + 1])
    f[2 * (base + 1) + 1] = fase(ej) if nome == "FA" else fase(phi1[2 * (base + 1) + 1])
    f[2 * (base + 2) + 1] = -fn[2]
    f[2 * (base + 3) + 1] = -fn[3]
    hS, nodiS, _ = C3.sottospazio(G2[0], G2[1], G2[2], [n])
    vecchi = [v for v in nodiS if v < nn]
    N_S = float(np.sum(np.abs(phi[np.isin(ND.nodo_h(ii, jj), vecchi)]) ** 2))
    ph = phi1.copy()
    for q, h in enumerate(hS):
        z = f[h]
        ph[h] = math.sqrt(N_S / len(hS)) * (z / abs(z) if abs(z) > 0 else 1.0)
    return ph


def nascita(G, psi, phi, a, nome):
    with np.errstate(invalid="ignore", divide="ignore"):
        out = ND.nasci(G, psi, phi, a)
    psi2 = out[1]
    if not np.all(np.isfinite(psi2)):
        assert float(np.sum(np.abs(psi) ** 2)) == 0.0
        psi2[~np.isfinite(psi2)] = 0.0
    with np.errstate(invalid="ignore", divide="ignore"):
        ph = regola(nome, G, phi, a, out)
    if not np.all(np.isfinite(ph)):
        return None, out
    Dl = ND.delta(ND.famiglie(G, psi, phi), ND.famiglie(out[0], psi2, ph))
    Dl["V0"], Dl["V1"] = float(np.sum(np.abs(phi) ** 2)), float(np.sum(np.abs(ph) ** 2))
    return Dl, out


def main():
    import _presidio
    import _massa_nei_difetti as MD
    import mattone as MT
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "nascita_dentro_fuori.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LE REGOLE PER LA FASE DEL VUOTO SULLE ESTREMITA' NUOVE, SENZA D7 (Luca 2026-11-17 16:38, A1-A2)")
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L = Z["L"]
        ii, jj, nn, dirs = MD.toro(L)
        assert np.array_equal(np.asarray(Z["mot"].inc.ii), ii) and np.array_equal(np.asarray(Z["mot"].inc.jj), jj)
        phi_v = np.asarray(Z["phi_v"]).copy()
    with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
        psi_m, phi_m = d["psi_h"].copy(), d["phi_h"].copy()
    G = (ii, jj, nn, np.asarray(dirs, dtype=float))
    v = np.arange(nn)
    m1, m2 = (v // L).astype(float), (v % L).astype(float)
    rho = np.zeros(nn)
    np.add.at(rho, ND.nodo_h(ii, jj), np.abs(psi_m[:, 0]) ** 2 + np.abs(psi_m[:, 1]) ** 2)
    cb = TO.centro(rho, m1, m2, L)[:2]
    D = TO.scarti(m1, m2, cb[0], cb[1], L)
    th = np.arctan2(D[:, 1], D[:, 0])
    esiti = []

    def arco(R):
        rm = np.hypot(D[:, 0] + 0.5, D[:, 1])
        i0 = int(np.argmin(np.abs(rm - R) + 10.0 * np.abs(th)))
        return 3 * i0, float(rm[i0])
    casi = [("il vuoto F3 puro (psi = 0)", np.zeros_like(psi_m), phi_v, 3 * (81 * L + 81), None)]
    for R in (23.81, 30.0, 60.0):
        a, rr = arco(R)
        casi.append(("il mattone, l'arco a %.2f nodi" % rr, psi_m, phi_m, a, rr))
    rng = np.random.default_rng(11)
    for nome_c, psi, phi, a, rr in casi:
        print("-" * 130)
        print("### %s (l'arco %d: %d -> %d)" % (nome_c, a, ii[a], jj[a]))
        dphi = 1e-12 * float(np.max(np.abs(phi))) * (rng.standard_normal(phi.shape) + 1j * rng.standard_normal(phi.shape))
        for nome in REGOLE:
            Dl, out = nascita(G, psi, phi, a, nome)
            Dp, _o = nascita(G, psi, phi + dphi, a, nome)
            if Dl is None:
                print("    %-6s ### INDEFINITA (una fase 0/0)" % nome)
                continue
            sens = abs(Dp["tot"] - Dl["tot"]) / abs(Dl["tot"]) if Dp is not None else float("inf")
            print("    %-6s %s | V relativa %.1e | la sensibilita' (il vuoto perturbato di 1e-12): la differenza relativa di dH %.3e" % (nome, ND.riga(Dl), abs(Dl["V1"] - Dl["V0"]) / Dl["V0"], sens))
            if nome == "v4-F3" and rr is not None:
                ph_nd = ND.v4f3(G, phi, out[0], out[2], out[3]["n"])
                ph_me = regola("v4-F3", G, phi, a, out)
                esiti.append(("il caso noto (%s): la v4-F3 = nascita_dentro_fuori.v4f3 al bit" % nome_c, np.array_equal(ph_nd, ph_me)))
                if rr > 55:
                    esiti.append(("il caso noto: all'anello 60 dH = +2.611234e+01 (nascita_dentro_fuori.txt) alla precisione stampata", "%.6e" % Dl["tot"] == "2.611234e+01"))
            sys.stdout.flush()
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
