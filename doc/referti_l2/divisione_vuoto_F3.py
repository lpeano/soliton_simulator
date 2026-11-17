# -*- coding: utf-8 -*-
r"""**LA REGOLA DEL VUOTO ALLA NASCITA, RIMISURATA SUL VUOTO F3** *(Luca `2026-11-17` `13:16`, parte 3; la carta `doc/TASK_HISTORY/2026-11-17_CPT_F3_soglia.md`, sez. `1` e `2.3`)*.

    E:\python\py3132\python.exe doc/referti_l2/divisione_vuoto_F3.py > doc/referti_l2/divisione_vuoto_F3.txt

**La mossa:** la nascita `(b1)` di `csv/_conto_del_vuoto.py` *(`nascita`: l'arco `i -> i + (1,0)` a `i = (L/2, L/2)` diviso, `n` legato a `i, j, k, l`, D7 sul padre `i`)*; **il conto:** `_conto_del_vuoto.motore` e `parti` *(`termini_di_h`: il motore della carta, `U = I`, `cs` spento, `PAR = {eps: 0}`: **il campo U(1) NON entra**)*.
**Le regole su F3** *(le sole definite: la carta, sez. `1`)*: **v1** *(D7 anche su `phi`, com'e')*; **v4-F3** *(SCELTA MIA, dichiarata: i moduli delle estremita' di `S` uniformi alla norma `N_S` di prima, le fasi quelle di v1; dove v1 e' `0`, la fase dell'estremita' compagna dello stesso arco)*.
**I casi:** **(K) il caso noto:** il vuoto UNIFORME `stato_K(24)`: v1 e v4-F3 devono ridare v1 e v4 di `divisione_vuoto_rigirato.txt`; **(a)** il vuoto F3 puro della scena S162 *(`phi_v`, `psi = 0`)*; **(b)** il mattone `L162_MGU_03000` con l'arco all'anello `13`-`14` dal baricentro della materia, **(c)** lo stesso con l'arco all'anello `60`; **lo stato TRASLATO** perche' l'arco scelto cada in `(L/2, L/2)` *(una rinumerazione; F3 e' invariante per traslazione)*.
**Per ogni regola:** `Delta H_tot` con le parti *(materia, vuoto, legame)*, `V` prima e dopo, **le estremita' cambiate FUORI da `S`** *(la localita': devono essere `0`)*.
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
for _p in (_SOL, _CSV, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

RIF = {"v1": -8.548213678, "v4": -0.300804079}     # divisione_vuoto_rigirato.txt, NASCITA, L 24 (il caso noto)


def nodo_h(ii, jj):
    h = np.empty(2 * len(ii), dtype=int)
    h[0::2] = ii
    h[1::2] = jj
    return h


def regole(L, sc):
    """### `{nome: (phi2, hS, dopo)}` per v1 e v4-F3."""
    import _conto_del_vuoto as C3
    ii, jj, nn, dirs, psi, phi = sc
    with np.errstate(invalid="ignore", divide="ignore"):
        dopo = C3.nascita(L, ii, jj, nn, dirs, psi, phi)
    ii2, jj2, nn2, _d2, psi2, phi1, nodi, chi = dopo
    if not np.all(np.isfinite(psi2)):
        # ### psi = 0 (il vuoto puro): D7 divide per |chi| = 0; il valore voluto e' 0 (la norma del padre e' 0): scritto nel referto
        assert float(np.sum(np.abs(psi) ** 2)) == 0.0, "psi non finito con una materia non nulla: FERMO"
        psi2[~np.isfinite(psi2)] = 0.0
        print("    (psi = 0: le estremita' nuove di psi messe a 0, il valore che D7 da' con la norma del padre 0)")
    hS, nodiS, _ = C3.sottospazio(ii2, jj2, nn2, [nodi[x] for x in chi])
    nh0 = nodo_h(ii, jj)
    vecchi = [v for v in nodiS if v < nn]
    N_S = float(np.sum(np.abs(phi[np.isin(nh0, vecchi)]) ** 2))
    ph = phi1.copy()
    fase = np.empty(len(hS), dtype=complex)
    for q, h in enumerate(hS):
        z = phi1[h] if abs(phi1[h]) > 0 else phi1[h ^ 1]
        fase[q] = z / abs(z) if abs(z) > 0 else 1.0
    ph[hS] = math.sqrt(N_S / len(hS)) * fase
    return {"v1": (phi1.copy(), hS, dopo), "v4-F3": (ph, hS, dopo)}, N_S


def conta(L, sc, nome, ph, hS, dopo):
    import _conto_del_vuoto as C3
    ii, jj, nn, dirs, psi, phi = sc
    ii2, jj2, nn2, dirs2, psi2, phi1, _nodi, _chi = dopo
    mot0, st0 = C3.motore(ii, jj, nn, dirs, psi, phi)
    mot1, st1 = C3.motore(ii2, jj2, nn2, dirs2, psi2, ph)
    p0, p1 = C3.parti(mot0, st0), C3.parti(mot1, st1)
    fuori = np.setdiff1d(np.arange(len(ph)), hS)
    cambiate = int(np.sum(ph[fuori] != phi1[fuori]))
    return {"dH": p1[0] - p0[0], "mat": p1[1] - p0[1], "vuo": p1[2] - p0[2], "leg": p1[3] - p0[3],
            "V0": float(np.sum(np.abs(phi) ** 2)), "V1": float(np.sum(np.abs(ph) ** 2)), "fuori": cambiate, "S": len(hS)}


def stampa(nome, r):
    print("    %-6s Delta H_tot %+.9e = materia %+.6e + vuoto %+.6e + legame %+.6e | V %.9e -> %.9e (relativa %.1e) | |S| %d, cambiate FUORI da S %d" % (
        nome, r["dH"], r["mat"], r["vuo"], r["leg"], r["V0"], r["V1"], abs(r["V1"] - r["V0"]) / r["V0"], r["S"], r["fuori"]))


def trasla(ii, L, psi_h, phi_h, d1, d2):
    """### La rinumerazione `v -> v + (d1, d2)`: l'arco `k = 3 v + a` -> `3 v' + a`, le estremita' `2 k + s` -> `2 k' + s`."""
    n = L * L
    v = np.arange(n)
    vp = ((v // L + d1) % L) * L + (v % L + d2) % L
    k = np.arange(3 * n)
    kp = 3 * vp[k // 3] + k % 3
    h = np.arange(6 * n)
    hpp = 2 * kp[h // 2] + h % 2
    ps, ph = np.empty_like(psi_h), np.empty_like(phi_h)
    ps[hpp] = psi_h
    ph[hpp] = phi_h
    return ps, ph


def main():
    import _presidio
    import _conto_del_vuoto as C3
    import _massa_nei_difetti as MD
    import mattone as MT
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_CSV, "_conto_del_vuoto.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA REGOLA DEL VUOTO ALLA NASCITA, RIMISURATA SUL VUOTO F3 (Luca 2026-11-17 13:16, parte 3); le regole: v1 e v4-F3 (la fase: una scelta mia, dichiarata)")
    print("=" * 130)
    esiti = []
    # ---------------------------------------------------------------- K
    print("### (K) IL CASO NOTO: il vuoto UNIFORME stato_K(24) (divisione_vuoto_rigirato.txt: v1 %.9f, v4 %.9f)" % (RIF["v1"], RIF["v4"]))
    sc = C3.stato_K(24)
    R, _N = regole(24, sc)
    for nome, (ph, hS, dopo) in R.items():
        r = conta(24, sc, nome, ph, hS, dopo)
        stampa(nome, r)
        rif = RIF["v1" if nome == "v1" else "v4"]
        esiti.append(("K. %s ridà %s del referto rigirato entro 1e-8" % (nome, "v1" if nome == "v1" else "v4"), abs(r["dH"] - rif) < 1e-8))
    # ---------------------------------------------------------------- la scena S162
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        ii, jj, nn, dirs = MD.toro(L)
        mi, mj = np.asarray(Z["mot"].inc.ii), np.asarray(Z["mot"].inc.jj)
        assert np.array_equal(mi, ii) and np.array_equal(mj, jj), "l'ordine degli archi della scena NON e' quello di _massa_nei_difetti.toro: FERMO"
        print("### la scena S162: L %d, %d nodi, %d archi; l'ordine degli archi = _massa_nei_difetti.toro (asserito)" % (L, n, len(ii)))
        phi_v = np.asarray(Z["phi_v"]).copy()
        with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
            psi_m, phi_m = d["psi_h"].copy(), d["phi_h"].copy()
    c = L // 2
    v = np.arange(n)
    m1, m2 = (v // L).astype(float), (v % L).astype(float)
    rho = np.sum(np.abs(psi_m) ** 2, axis=1)
    rho_n = np.zeros(n)
    np.add.at(rho_n, nodo_h(ii, jj), rho)
    cb = TO.centro(rho_n, m1, m2, L)[:2]
    D = TO.scarti(m1, m2, cb[0], cb[1], L)
    r_n = np.hypot(D[:, 0], D[:, 1])
    th = np.arctan2(D[:, 1], D[:, 0])
    casi = [("(a) il vuoto F3 puro (psi = 0)", np.zeros_like(psi_m), phi_v, (0, 0), None)]
    for anello in (13.5, 60.0):
        # il nodo i con l'arco i -> i + (1,0) il cui punto medio sta a distanza ~anello, nella direzione theta ~ 0
        rm = np.hypot(D[:, 0] + 0.5, D[:, 1])
        j0 = int(np.argmin(np.abs(rm - anello) + 10.0 * np.abs(th)))
        casi.append(("(%s) il mattone, l'arco all'anello %.1f (il nodo (%d, %d), il punto medio a %.2f nodi dal baricentro)" % ("b" if anello < 30 else "c", anello, m1[j0], m2[j0], rm[j0]),
                     psi_m, phi_m, (c - int(m1[j0]), c - int(m2[j0])), rm[j0]))
    print("### il baricentro della materia del mattone (%.3f, %.3f)" % (cb[0], cb[1]))
    tab = []
    for nome_c, ps, ph0, (d1, d2), _r in casi:
        ps_t, ph_t = trasla(ii, L, ps, ph0, d1, d2)
        sc = (ii, jj, nn, dirs, ps_t, ph_t)
        print("-" * 130)
        print("### %s; la traslazione (%d, %d)" % (nome_c, d1, d2))
        R, N_S = regole(L, sc)
        print("    N_S %.9e (la norma del vuoto di S prima)" % N_S)
        for nome, (ph, hS, dopo) in R.items():
            r = conta(L, sc, nome, ph, hS, dopo)
            stampa(nome, r)
            tab.append((nome_c[:3], nome, r))
            esiti.append(("%s %s: locale (nessuna estremita' cambiata fuori da S) e V conservata entro 1e-12" % (nome_c[:3], nome), r["fuori"] == 0 and abs(r["V1"] - r["V0"]) / r["V0"] < 1e-12))
            sys.stdout.flush()
    print("-" * 130)
    print("### LA TABELLA (Delta H_tot)")
    for caso, nome, r in tab:
        print("    %-4s %-6s %+.6e" % (caso, nome, r["dH"]))
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
