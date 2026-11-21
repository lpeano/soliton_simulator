# -*- coding: utf-8 -*-
r"""**IL FLIP DI STELLA: F1, F2 PER CANDIDATO, F3** *(l'aggiunta di Luca `2026-11-20` `13:54`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md`, sez. `7`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/flip_di_stella.py > doc/referti_l2/flip_di_stella.txt

**Il flip di stella** *(7.1)*: dopo la nascita di stella sull'arco `a = (i, j)` col nodo `n`, i candidati `(x, y)` con `x` in `{i, j}`, `y` in `{k, l}`; `m` = l'altro vicino comune di `x` e `y`; l'arco `x - y` si toglie, nasce `n -> m` *(in coda)*; **in `n` la media delle estremita' di `n` verso `x` e verso `y`; in `m` la media di quelle di `m` verso `x` e verso `y`**; un fattore uniforme sui nodi `n, x, m, y` per `psi` e per `phi`.
**IL CASO CHE DEVE FALLIRE: il flip col VERSO** *(come `_conto_del_vuoto.flip`)*: le estremita' dell'arco tolto permutate sull'arco nato *(quella del capo `ii` in `n`, quella del capo `jj` in `m`)*, nessun fattore.
**LA SCELTA FRA I QUATTRO NON SI USA** *(7.2: la grandezza della `10.3` non e' univoca; FERMO prima di usarla)*: **qui ogni candidato si prova DA SOLO.**
**Lo stato:** C2 a `k 3000` *(dichiarato)*; i primi `200` archi nell'ordine di scatto.
"""
import math
import os
import sys
import time

import numpy as np
import scipy.sparse as sp

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "mattone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import covariante_e_famiglia as CF  # noqa: E402
import covariante_di_stella as CS  # noqa: E402
import nascita_energia_nulla as NN  # noqa: E402
import regole_fase_F3 as RF  # noqa: E402
import nascita_dentro_fuori as ND  # noqa: E402

N_SPECCHIO = 200
SOGLIA, SOGLIA_DEVE_FALLIRE = 1e-14, 1e-6


def nasci_stella(G, psi, phi, a):
    P = NN.preparo(G, psi, phi, a)
    s_old, s_new = CF.stelle(G, P["G2"], P["out"][3])
    return (P["G2"], CS.sc(G, psi, a, P, s_old, s_new), CS.sc(G, phi, a, P, s_old, s_new)), P["out"][3]


def arco_fra(ii, jj, x, y):
    e = np.where(((ii == x) & (jj == y)) | ((ii == y) & (jj == x)))[0]
    assert len(e) == 1, "fra %d e %d %d archi" % (x, y, len(e))
    return int(e[0])


def gira_grezzo(G2, arr, x, y, n, regola):
    """### `(G3, arr3, (e, m, h_n, h_m))`: il flip di `x - y` in `n -> m`, PRIMA del fattore."""
    ii, jj, nn, vec = G2
    e = arco_fra(ii, jj, x, y)
    com = ND.vicini(ii, jj, x) & ND.vicini(ii, jj, y)
    assert len(com) == 2 and n in com, "il quadrilatero di (%d, %d) non e' definito: vicini comuni %s" % (x, y, sorted(com))
    m = int(sorted(com - {n})[0])
    keep = np.ones(len(ii), dtype=bool)
    keep[e] = False
    G3 = (np.concatenate([ii[keep], [n]]), np.concatenate([jj[keep], [m]]), nn,
          np.concatenate([vec[keep], [ND.vettore(ii, jj, vec, n, x) + ND.vettore(ii, jj, vec, x, m)]]))
    m3 = len(G3[0])
    y3 = np.zeros((2 * m3,) + arr.shape[1:], dtype=arr.dtype)
    y3[:2 * (m3 - 1)] = arr[np.repeat(keep, 2)]
    h_n, h_m = 2 * (m3 - 1), 2 * (m3 - 1) + 1
    if regola == "stella":
        y3[h_n] = 0.5 * (RF.estremita_di(ii, jj, arr, n, x) + RF.estremita_di(ii, jj, arr, n, y))
        y3[h_m] = 0.5 * (RF.estremita_di(ii, jj, arr, m, x) + RF.estremita_di(ii, jj, arr, m, y))
    else:
        y3[h_n] = arr[2 * e]
        y3[h_m] = arr[2 * e + 1]
    return G3, y3, (e, m, h_n, h_m)


def gira(G2, psi2, phi2, x, y, n, regola):
    G3, p3, info = gira_grezzo(G2, psi2, x, y, n, regola)
    _G, f3, _i = gira_grezzo(G2, phi2, x, y, n, regola)
    if regola == "stella":
        m = info[1]
        quad = [n, x, m, y]
        h_old = np.where(np.isin(ND.nodo_h(G2[0], G2[1]), quad))[0]
        h_new = np.where(np.isin(ND.nodo_h(G3[0], G3[1]), quad))[0]
        for old, new in ((psi2, p3), (phi2, f3)):
            Nb, Na = CF.norma(old, h_old), CF.norma(new, h_new)
            if Nb > 0.0 and Na > 0.0:
                new[h_new] *= math.sqrt(Nb / Na)
    return (G3, p3, f3), info


def grafo_ok(G2, G3, n, x, y, m):
    """### F3: i gradi, Eulero, nessun arco doppio, ogni arco in due triangoli."""
    nn = G3[2]
    d2 = np.bincount(ND.nodo_h(G2[0], G2[1]), minlength=nn)
    d3 = np.bincount(ND.nodo_h(G3[0], G3[1]), minlength=nn)
    att = d2.copy()
    att[n] += 1
    att[m] += 1
    att[x] -= 1
    att[y] -= 1
    gradi = bool(np.array_equal(d3, att))
    eulero = int(np.sum(6 - d3)) == 0 and len(G3[0]) == 3 * nn
    u, v = np.minimum(G3[0], G3[1]), np.maximum(G3[0], G3[1])
    doppi = len(np.unique(u.astype(np.int64) * nn + v)) == len(u)
    A = sp.csr_matrix((np.ones(2 * len(u)), (np.concatenate([u, v]), np.concatenate([v, u]))), shape=(nn, nn))
    C = (A @ A).tocsr()
    tri = bool(np.all(np.asarray(C[u, v]).ravel() == 2.0))
    return gradi, eulero, doppi, tri


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "covariante_di_stella.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    print("=" * 130)
    print("IL FLIP DI STELLA: F1, F2 PER CANDIDATO, F3 (Luca 2026-11-20 13:54); lo stato di C2 a k 3000 (dichiarato); LA SCELTA FRA I QUATTRO NON SI USA")
    print("=" * 130)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    esiti = []
    # ------------------------------------------------------------------ F1
    cp, cz = np.array([0.3 + 0.1j, -0.2 + 0.4j]), 0.6 - 0.8j
    pu, fu = np.tile(cp, (len(psi), 1)), np.full(len(phi), cz)
    (G2u, p2u, f2u), nu = nasci_stella(G, pu, fu, int(archi[0]))
    p2u, f2u = np.tile(cp, (2 * len(G2u[0]), 1)), np.full(2 * len(G2u[0]), cz)      # ### il campo UNIFORME sul grafo nato (il fattore della nascita lo avrebbe cambiato sulla stella)
    ok1 = True
    for x in (nu["i"], nu["j"]):
        for y in (nu["k"], nu["l"]):
            _G, yp, info = gira_grezzo(G2u, p2u, x, y, nu["n"], "stella")
            _G, yf, _i = gira_grezzo(G2u, f2u, x, y, nu["n"], "stella")
            h = [info[2], info[3]]
            ok1 &= bool(np.all(yp[h] == p2u[0])) and bool(np.all(yf[h] == f2u[0]))
    print("### F1: sul campo uniforme le due estremita' nuove dei quattro flip (prima del fattore) = il valore AL BIT: %s" % ok1)
    esiti.append(("F1: sul campo uniforme le estremita' nuove del flip (prima del fattore) AL BIT", ok1))
    print("-" * 130)
    # ------------------------------------------------------------------ F2 e F3
    sig, ap, rov, hp, p0, scarto = CF.mappa_specchio(G, centro)
    psiR, phiR = np.empty_like(psi), np.empty_like(phi)
    psiR[hp], phiR[hp] = psi, phi
    nn = G[2]
    N = nn + 1
    sig2 = np.append(sig, nn)
    D = {"stella": np.full((N_SPECCHIO, 4, 2), np.nan), "verso": np.full((N_SPECCHIO, 4, 2), np.nan)}
    F3 = np.zeros((N_SPECCHIO, 4, 4), dtype=bool)
    DHf = np.full((N_SPECCHIO, 4), np.nan)
    nondef = 0
    t0 = time.time()
    for q in range(N_SPECCHIO):
        a = int(archi[q])
        A2, nA = nasci_stella(G, psi, phi, a)
        B2, nB = nasci_stella(G, psiR, phiR, int(ap[a]))
        F2m = NN.F_mano(*A2)["tot"]
        c = 0
        for x in (nA["i"], nA["j"]):
            for y in (nA["k"], nA["l"]):
                try:
                    for reg in ("stella", "verso"):
                        A3, info = gira(*A2, x, y, nA["n"], reg)
                        B3, _ib = gira(*B2, int(sig[x]), int(sig[y]), nB["n"], reg)
                        D[reg][q, c] = CF.confronta(A3, B3, sig2, N)
                        if reg == "stella":
                            F3[q, c] = grafo_ok(A2[0], A3[0], nA["n"], x, y, info[1])
                            DHf[q, c] = NN.F_mano(*A3)["tot"] - F2m
                except AssertionError as e:
                    nondef += 1
                    print("    l'arco %d, il candidato (%d, %d): NON definito (%s)" % (a, x, y, e))
                c += 1
        if q % 20 == 0:
            print("    %d su %d (%.0f s)" % (q, N_SPECCHIO, time.time() - t0))
            sys.stdout.flush()
    rv = rov[archi[:N_SPECCHIO]]
    print("### LO SPECCHIO DEL FLIP DA SOLO (a 30 gradi per il nodo %s; %d nascite x 4 candidati: %d conservate, %d ROVESCIATE); candidati NON definiti %d" % (tuple(int(v) for v in p0), N_SPECCHIO, int(np.sum(~rv)), int(np.sum(rv)), nondef))
    for reg in ("stella", "verso"):
        for cl, msk in (("conservati", ~rv), ("ROVESCIATI", rv)):
            X = D[reg][msk].reshape(-1, 2)
            print("    %-7s %-10s %3d flip: psi max %.3e (sopra %.0e: %3d), phi max %.3e (sopra: %3d)" % (reg, cl, len(X), np.nanmax(X[:, 0]), SOGLIA, int(np.sum(X[:, 0] > SOGLIA)), np.nanmax(X[:, 1]), int(np.sum(X[:, 1] > SOGLIA))))
    fallisce = bool(np.nanmax(D["verso"]) > SOGLIA_DEVE_FALLIRE)
    print("    il caso che DEVE FALLIRE (il flip col verso, come C3): lo scarto massimo %.3e (deve superare %.0e)" % (float(np.nanmax(D["verso"])), SOGLIA_DEVE_FALLIRE))
    esiti.append(("DEVE FALLIRE: il flip col verso sopra 1e-6 (o la prova non vale: FERMO)", fallisce))
    esiti.append(("P-F2: il flip di stella simmetrico su tutte le classi entro 1e-14 (ogni candidato)", bool(np.nanmax(D["stella"]) < SOGLIA) and nondef == 0))
    esiti.append(("P-F2: il flip col verso cade sui ROVESCIATI", bool(np.nanmax(D["verso"][rv]) > SOGLIA)))
    print("-" * 130)
    nomi = ("i gradi (n e m +1, x e y -1)", "Eulero (somma 6 - k = 0, E = 3 V)", "nessun arco doppio", "ogni arco in due triangoli")
    for t, nm in enumerate(nomi):
        print("### F3, %s: %d su %d flip" % (nm, int(np.sum(F3[:, :, t])), F3[:, :, 0].size))
    ok3 = bool(np.all(F3)) and nondef == 0
    esiti.append(("F3: i gradi, Eulero, nessun arco doppio, ogni arco in due triangoli, su ogni flip", ok3))
    print("### il DH del flip (il conto a mano; NON usato per scegliere): min %+.4e, mediana %+.4e, max %+.4e; negativi %d su %d" % (np.nanmin(DHf), np.nanmedian(DHf), np.nanmax(DHf), int(np.sum(DHf < 0)), int(np.sum(~np.isnan(DHf)))))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-118s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("### %.0f s" % (time.time() - t00))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
