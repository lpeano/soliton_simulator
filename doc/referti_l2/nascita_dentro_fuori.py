# -*- coding: utf-8 -*-
r"""**L'ENERGIA DELLA NASCITA DENTRO E FUORI DALLA MATERIA** *(Luca `2026-11-17` `14:27`, parte 2; la carta e le previsioni `doc/TASK_HISTORY/2026-11-17_flusso_uscente.md`, `831e8d52`; SOLO COPIE dello stato)*.

    E:\python\py3132\python.exe doc/referti_l2/nascita_dentro_fuori.py > doc/referti_l2/nascita_dentro_fuori.txt

**LA DIVISIONE D'ARCO GENERICA** *(su un grafo qualunque; la STESSA regola di `_conto_del_vuoto.nascita`)*: l'arco `a = (i -> j)` tolto; `k`, `l` = i due vicini comuni di `i` e `j` *(`k` a SINISTRA di `i -> j`, `l` a destra: il segno del prodotto vettoriale)*; il nodo nuovo `n`; gli archi nuovi `n -> i, j, k, l` in coda; le estremita' dell'arco tolto trasportate su `n -> i` *(in `i`)* e `n -> j` *(in `j`)*; **D7 sul padre `i`**; le estremita' nuove in `k` e `l` a `0`; **`phi` con v4-F3** *(`divisione_vuoto_F3.py`)*; i vettori d'arco tenuti per il motore *(`n -> i = -a/2`, `n -> j = +a/2`, `n -> k = (i -> k) - a/2`)*.
**Il conto:** il motore della carta *(`_conto_del_vuoto.motore`: `U = I`, `cs` spento, `PAR = {eps: 0}`)*; **i termini per famiglia** *(il Grover di `psi` e di `phi` per nodo, `N`, l'arco di `psi` e di `phi`: `energia_pesata.termini_di_h`)*; **materia = Grover psi + arco psi; vuoto = Grover phi + arco phi; legame = N.**
**Il caso noto** *(Q-A4)*: la divisione generica sullo stato `stato_K(24)`, l'arco di `nascita`, = `nascita` AL BIT *(gli array e `Delta H`)*.
**2.1** il profilo sul mattone `L162_MGU_03000`: un arco per anello `8`-`60` *(il nodo `i` con l'arco `i -> i + (1,0)` il cui punto medio e' piu' vicino all'anello, nella direzione `theta ~ 0`)*; **il confine** *(il termine della materia sotto l'`1%` e il `10%` di `|Delta H|`)*. **2.2** il perche' *(le famiglie)*. **2.3** **20 nascite in fila** all'anello del confine e all'anello `13.8` *(ognuna sull'arco del nodo nato per ultimo col termine d'arco del vuoto piu' alto; a pari merito l'indice piu' basso)*. **2.4** con U *(A, E della scena; `A` sugli archi nuovi a meta' flusso; `E` da Gauss vero; `U = e^{i e A}` nel conto; l'energia `E^2/2` NON pesata, accanto)*. **2.5** il triangolo e la coppia *(5 anelli)*.
"""
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
_PO = os.path.join(_RADICE, "primo_ordine")
for _p in (_QUI, _SOL, _CSV, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ANELLI = list(range(8, 61))
N_FILA = 20


def nodo_h(ii, jj):
    h = np.empty(2 * len(ii), dtype=int)
    h[0::2] = ii
    h[1::2] = jj
    return h


def vicini(ii, jj, v):
    return set(jj[ii == v].tolist()) | set(ii[jj == v].tolist())


def vettore(ii, jj, vec, x, y):
    """### il vettore da `x` a `y` dall'arco che li unisce."""
    a = np.where((ii == x) & (jj == y))[0]
    if len(a):
        return vec[a[0]]
    a = np.where((ii == y) & (jj == x))[0]
    return -vec[a[0]]


def nasci(G, psi, phi, a, campo=None):
    """### La divisione generica dell'arco `a`. `G = (ii, jj, nn, vec)`. `(G2, psi2, phi1, nodi, keep)`; `campo = (A, E)` -> anche `(A2, E2_senza_gauss)`."""
    ii, jj, nn, vec = G
    i, j = int(ii[a]), int(jj[a])
    com = sorted(vicini(ii, jj, i) & vicini(ii, jj, j))
    assert len(com) == 2, "l'arco %d non ha due vicini comuni (%s): non e' un lato di due triangoli" % (a, com)
    va = vec[a]
    cr = [va[0] * vettore(ii, jj, vec, i, c)[1] - va[1] * vettore(ii, jj, vec, i, c)[0] for c in com]
    k, l = (com[0], com[1]) if cr[0] > 0 else (com[1], com[0])
    n = nn
    keep = np.ones(len(ii), dtype=bool)
    keep[a] = False
    nuovi = np.where(keep)[0]
    ii2 = np.concatenate([ii[keep], [n] * 4])
    jj2 = np.concatenate([jj[keep], [i, j, k, l]])
    vec2 = np.concatenate([vec[keep], np.array([-0.5 * va, 0.5 * va, vettore(ii, jj, vec, i, k) - 0.5 * va, vettore(ii, jj, vec, i, l) - 0.5 * va])])
    m2 = len(ii2)
    psi2 = np.zeros((2 * m2, 2), dtype=complex)
    phi2 = np.zeros(2 * m2, dtype=complex)
    e = np.repeat(keep, 2)
    psi2[:2 * len(nuovi)] = psi[e]
    phi2[:2 * len(nuovi)] = phi[e]
    base = len(nuovi)
    psi2[2 * (base + 0) + 1] = psi[2 * a]
    phi2[2 * (base + 0) + 1] = phi[2 * a]
    psi2[2 * (base + 1) + 1] = psi[2 * a + 1]
    phi2[2 * (base + 1) + 1] = phi[2 * a + 1]
    hp = np.where(nodo_h(ii2, jj2) == i)[0]
    Np_psi = float(np.sum(np.abs(psi2[hp]) ** 2))
    Np_phi = float(np.sum(np.abs(phi2[hp]) ** 2))
    chi = psi2[hp].sum(axis=0)
    chiv = phi2[hp].sum()
    psi2[hp] /= math.sqrt(2.0)
    phi2[hp] /= math.sqrt(2.0)
    for q in range(4):
        h = 2 * (base + q)
        psi2[h] = (1.0 / math.sqrt(2.0)) * math.sqrt(Np_psi / 4.0) * chi / np.linalg.norm(chi) if np.linalg.norm(chi) > 0 else 0.0
        phi2[h] = (1.0 / math.sqrt(2.0)) * math.sqrt(Np_phi / 4.0) * chiv / abs(chiv)
    out = [(ii2, jj2, nn + 1, vec2), psi2, phi2, {"n": n, "i": i, "j": j, "k": k, "l": l}, keep, abs(chiv) / math.sqrt(Np_phi * len(hp))]
    if campo is not None:
        A, E = campo
        Aa = A[a]
        A2 = np.concatenate([A[keep], [-0.5 * Aa, 0.5 * Aa, 0.0, 0.0]])
        E2 = np.concatenate([E[keep], [0.0, 0.0, 0.0, 0.0]])

        def Ad(x, y):
            q = np.where((ii == x) & (jj == y))[0]
            if len(q):
                return A[q[0]]
            return -A[np.where((ii == y) & (jj == x))[0][0]]
        # il triangolo vecchio (i, j, k): Phi = A(i->j) + A(j->k) + A(k->i); la meta' a (i, n, k): A(i->n) + A(n->k) + A(k->i) = Phi/2
        for c, q in ((k, 2), (l, 3)):
            Phi = Aa + Ad(j, c) + Ad(c, i)
            A2[base + q] = 0.5 * Phi - 0.5 * Aa - Ad(c, i)    # A(n -> c) con A(i -> n) = +A_a/2
        out.append((A2, E2))
    return out


def v4f3(G, phi, G2, phi1, n):
    import _conto_del_vuoto as C3
    ii, jj, nn, _v = G
    ii2, jj2, nn2, _v2 = G2
    hS, nodiS, _ = C3.sottospazio(ii2, jj2, nn2, [n])
    vecchi = [v for v in nodiS if v < nn]
    N_S = float(np.sum(np.abs(phi[np.isin(nodo_h(ii, jj), vecchi)]) ** 2))
    ph = phi1.copy()
    fase = np.empty(len(hS), dtype=complex)
    for q, h in enumerate(hS):
        z = phi1[h] if abs(phi1[h]) > 0 else phi1[h ^ 1]
        fase[q] = z / abs(z) if abs(z) > 0 else 1.0
    ph[hS] = math.sqrt(N_S / len(hS)) * fase
    return ph


def famiglie(G, psi, phi, U=None):
    """### le famiglie di `termini_di_h` col motore della carta (e `U = e^{i e A}` se dato)."""
    import _conto_del_vuoto as C3
    import energia_pesata as EP
    import materia_vuoto as MV
    ii, jj, nn, vec = G
    mot, st = C3.motore(ii, jj, nn, vec, psi, phi)
    if U is not None:
        mot.geo.U[:, 0, 0] = U
        mot.geo.U[:, 1, 1] = U
    Om = EP.OMEGA_H
    nodo = nodo_h(ii, jj)
    nrm_psi = np.zeros(nn); np.add.at(nrm_psi, nodo, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2)
    nrm_phi = np.zeros(nn); np.add.at(nrm_phi, nodo, np.abs(phi) ** 2)
    S_psi = np.zeros((nn, 2), dtype=complex); np.add.at(S_psi, nodo, psi)
    S_phi = np.zeros(nn, dtype=complex); np.add.at(S_phi, nodo, phi)
    d = np.bincount(nodo, minlength=nn).astype(float)
    w = psi.reshape(len(ii), 2, 2)
    f = phi.reshape(len(ii), 2)
    Uq = mot.geo.U
    F = {"G_psi": float(np.sum(-Om * (0.5 * nrm_psi - (np.abs(S_psi[:, 0]) ** 2 + np.abs(S_psi[:, 1]) ** 2) / d))),
         "a_psi": float(np.sum(Om * np.real(np.einsum("ai,aji,aj->a", np.conj(w[:, 0, :]), np.conj(Uq), w[:, 1, :])))),
         "N": float(np.sum(MV.N(nrm_psi, nrm_phi))),
         "G_phi": float(np.sum(-Om * (0.5 * nrm_phi - np.abs(S_phi) ** 2 / d))),
         "a_phi": float(np.sum(Om * np.real(np.conj(f[:, 0]) * f[:, 1])))}
    pn, pa = EP.termini_di_h(mot, st, {"eps": 0.0})
    tot = float(np.sum(pn)) + float(np.sum(pa))
    F["tot"] = tot
    F["ctrl"] = abs(tot - sum(F[x] for x in ("G_psi", "a_psi", "N", "G_phi", "a_phi"))) / max(abs(tot), 1.0)
    return F


def delta(F0, F1):
    D = {k: F1[k] - F0[k] for k in ("G_psi", "a_psi", "N", "G_phi", "a_phi", "tot")}
    D["mat"] = D["G_psi"] + D["a_psi"]
    D["vuo"] = D["G_phi"] + D["a_phi"]
    return D


def riga(D):
    return "dH %+.6e = materia %+.6e (G_psi %+.4e a_psi %+.4e) + vuoto %+.6e (G_phi %+.4e a_phi %+.4e) + N %+.4e; materia/|dH| %.3e" % (
        D["tot"], D["mat"], D["G_psi"], D["a_psi"], D["vuo"], D["G_phi"], D["a_phi"], D["N"], abs(D["mat"]) / abs(D["tot"]) if D["tot"] != 0 else float("inf"))


def gauss(G, rho, E, e):
    """### `E` corretto perche' `div E = e (rho - media)` sul grafo `G` (il laplaciano col nodo 0 tolto, come p6_u_breve.gauss_sparso)."""
    import scipy.sparse as sp
    import scipy.sparse.linalg as spl
    ii, jj, nn, _v = G
    m = len(ii)
    D = sp.csr_matrix((np.concatenate([np.ones(m), -np.ones(m)]), (np.concatenate([jj, ii]), np.concatenate([np.arange(m), np.arange(m)]))), shape=(nn, m))
    b = e * (rho - rho.mean()) - D @ E
    Lap = (D @ D.T).tocsc()
    x = np.zeros(nn)
    x[1:] = spl.spsolve(Lap[1:, 1:], b[1:])
    x -= x.mean()
    return E + D.T @ x, float(np.max(np.abs(D @ (E + D.T @ x) - e * (rho - rho.mean()))))


def main():
    import _presidio
    import _conto_del_vuoto as C3
    import _massa_nei_difetti as MD
    import mattone as MT
    import divisione_vuoto_F3 as DF
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_CSV, "_conto_del_vuoto.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    print("=" * 130)
    print("L'ENERGIA DELLA NASCITA DENTRO E FUORI DALLA MATERIA (Luca 2026-11-17 14:27, parte 2); la divisione d'arco generica; phi con v4-F3; il conto della carta (U = I salvo 2.4)")
    print("=" * 130)
    esiti = []
    # ---------------------------------------------------------------- il caso noto
    sc = C3.stato_K(24)
    iiK, jjK, nnK, dK, psiK, phiK = sc
    GK = (iiK, jjK, nnK, np.asarray(dK, dtype=float))
    c = 12
    aK = 3 * (c * 24 + c)
    rif = C3.nascita(24, *sc)
    mio = nasci(GK, psiK, phiK, aK)
    uguali = all(np.array_equal(x, y) for x, y in ((mio[0][0], rif[0]), (mio[0][1], rif[1]), (mio[1], rif[4]), (mio[2], rif[5])))
    vn = np.asarray(rif[3], dtype=float)
    vn = vn / np.linalg.norm(vn, axis=1)[:, None]
    vm = mio[0][3] / np.linalg.norm(mio[0][3], axis=1)[:, None]
    print("### IL CASO NOTO: la divisione generica contro _conto_del_vuoto.nascita su stato_K(24): ii, jj, psi, phi uguali al bit: %s; i versori, la differenza massima %.1e; i nodi %s contro %s" % (
        uguali, float(np.max(np.abs(vn - vm))), mio[3], rif[6]))
    esiti.append(("il caso noto: la divisione generica = nascita al bit (ii, jj, psi, phi)", uguali and mio[3] == rif[6]))
    # ---------------------------------------------------------------- il mattone
    import _massa_nei_difetti as MD  # noqa: F811
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n0 = Z["L"], Z["n"]
        ii, jj, nn, dirs = MD.toro(L)
        assert np.array_equal(np.asarray(Z["mot"].inc.ii), ii) and np.array_equal(np.asarray(Z["mot"].inc.jj), jj)
        C0 = MT.Campi(Z, "MGU", MT.rho_c_assoluto(), MT.PB.E_DECISO)
        assert np.array_equal(np.asarray(C0.campo.ii), ii) and np.array_equal(np.asarray(C0.campo.jj), jj), "l'ordine degli archi del campo non e' quello del toro: FERMO"
    G = (ii, jj, nn, np.asarray(dirs, dtype=float))
    e = MT.PB.E_DECISO
    v = np.arange(nn)
    m1, m2 = (v // L).astype(float), (v % L).astype(float)
    stati = {}
    for nome, f in (("il mattone", "L162_MGU_03000.npz"), ("il triangolo", "legati_t120_03000.npz"), ("la coppia", "legati_GU_07000.npz")):
        with np.load(os.path.join(MT.DIR_E, f)) as d:
            stati[nome] = (d["psi_h"].copy(), d["phi_h"].copy(), d["campo_A"].copy(), d["campo_E"].copy())

    def geometria(psi):
        rho = np.zeros(nn)
        np.add.at(rho, nodo_h(ii, jj), np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2)
        cb = TO.centro(rho, m1, m2, L)[:2]
        D = TO.scarti(m1, m2, cb[0], cb[1], L)
        r = np.hypot(D[:, 0], D[:, 1])
        th = np.arctan2(D[:, 1], D[:, 0])
        Rm = math.sqrt(float(np.sum(rho * r ** 2) / np.sum(rho)))
        return rho, cb, D, r, th, Rm

    def arco_all_anello(D, th, R):
        rm = np.hypot(D[:, 0] + 0.5, D[:, 1])
        i0 = int(np.argmin(np.abs(rm - R) + 10.0 * np.abs(th)))
        return 3 * i0, float(rm[i0])

    def una(G_, psi, phi, a, U=None, campo=None):
        F0 = famiglie(G_, psi, phi, U)
        out = nasci(G_, psi, phi, a, campo)
        G2, psi2, phi1, nodi, keep, chiv = out[:6]
        ph = v4f3(G_, phi, G2, phi1, nodi["n"])
        U2 = None
        extra = {}
        if campo is not None:
            A2, E2 = out[6]
            rho2 = np.zeros(G2[2]); np.add.at(rho2, nodo_h(G2[0], G2[1]), np.abs(psi2[:, 0]) ** 2 + np.abs(psi2[:, 1]) ** 2)
            E2g, res = gauss(G2, rho2, E2, e)
            U2 = np.exp(1j * e * A2)
            extra = {"dE2": 0.5 * float(np.sum(E2g ** 2)) - 0.5 * float(np.sum(campo[1] ** 2)), "gauss": res, "A2": A2, "E2": E2g}
        F1 = famiglie(G2, psi2, ph, U2)
        return delta(F0, F1), G2, psi2, ph, nodi, chiv, max(F0["ctrl"], F1["ctrl"]), extra

    # ---------------------------------------------------------------- 2.1 e 2.2
    psi, phi, A0, E0 = stati["il mattone"]
    rho, cb, D, r, th, Rm = geometria(psi)
    print("-" * 130)
    print("### 2.1 IL PROFILO SUL MATTONE: il baricentro (%.3f, %.3f); il raggio della materia (rms) %.3f nodi" % (cb[0], cb[1], Rm))
    prof = []
    for R in ANELLI:
        a, rr = arco_all_anello(D, th, R)
        Dl, _G2, _p, _ph, nodi, chiv, ctrl, _x = una(G, psi, phi, a)
        rho_a = 0.5 * (rho[ii[a]] + rho[jj[a]])
        prof.append((R, rr, Dl, rho_a))
        print("    anello %2d (il punto medio a %6.2f nodi = %.2f R_m; rho all'arco %.4e; |chiv| relativa %.2e; il controllo %.1e): %s" % (R, rr, rr / Rm, rho_a, chiv, ctrl, riga(Dl)))
        sys.stdout.flush()
    conf = {}
    for soglia in (0.10, 0.01):
        sotto = [x for x in prof if abs(x[2]["mat"]) < soglia * abs(x[2]["tot"])]
        primo = sotto[0][1] if sotto else None
        resta = None
        for q in range(len(prof)):
            if all(abs(x[2]["mat"]) < soglia * abs(x[2]["tot"]) for x in prof[q:]):
                resta = prof[q][1]
                break
        conf[soglia] = (primo, resta)
        print("### IL CONFINE al %.0f%%: la prima volta a %s nodi; da li' in poi sempre sotto: da %s nodi (%s R_m)" % (100 * soglia, "%.2f" % primo if primo else "mai", "%.2f" % resta if resta else "mai",
              "%.2f" % (resta / Rm) if resta else "-"))
    # 2.2
    i13 = min(prof, key=lambda x: abs(x[1] - 13.8))
    print("### 2.2 IL PERCHE' all'anello %.2f: %s" % (i13[1], riga(i13[2])))
    # ---------------------------------------------------------------- 2.3 le nascite in fila (e 2.4 con U)
    R1 = conf[0.01][1] if conf[0.01][1] else 30.0
    for conU in (False, True):
        for Rf in (13.8, R1):
            a, rr = arco_all_anello(D, th, Rf)
            Gc, pc, fc = G, psi.copy(), phi.copy()
            campo = (A0.copy(), E0.copy()) if conU else None
            U = np.exp(1j * e * A0) if conU else None
            print("-" * 130)
            print("### 2.%s LE NASCITE IN FILA all'anello %.2f (%s): %d nascite" % ("4" if conU else "3", rr, "CON U: A a meta' flusso, E da Gauss vero, U = e^{i e A}" if conU else "U = I", N_FILA))
            segni = []
            for q in range(N_FILA):
                Dl, G2, p2, f2, nodi, chiv, ctrl, ex = una(Gc, pc, fc, a, U, campo)
                segni.append(Dl["tot"])
                print("    %2d: l'arco %d (%d -> %d), |chiv| %.2e: %s%s" % (q + 1, a, Gc[0][a], Gc[1][a], chiv, riga(Dl),
                      ("; E^2/2 %+.4e, Gauss dopo %.1e" % (ex["dE2"], ex["gauss"])) if ex else ""))
                sys.stdout.flush()
                Gc, pc, fc = G2, p2, f2
                if conU:
                    campo = (ex["A2"], ex["E2"])
                    U = np.exp(1j * e * ex["A2"])
                nn_ = nodi["n"]
                cand = np.where((Gc[0] == nn_) | (Gc[1] == nn_))[0]
                T = np.real(np.conj(fc[2 * cand]) * fc[2 * cand + 1])
                a = int(cand[np.lexsort((cand, -T))][0])
            cambi = [q + 1 for q in range(1, len(segni)) if (segni[q] > 0) != (segni[q - 1] > 0)]
            print("    i segni: %s; i cambi di segno alle nascite %s" % ("".join("+" if x > 0 else "-" for x in segni), cambi if cambi else "nessuno"))
    # ---------------------------------------------------------------- 2.5
    for nome in ("il triangolo", "la coppia"):
        psi_, phi_, _A, _E = stati[nome]
        rho_, cb_, D_, r_, th_, Rm_ = geometria(psi_)
        print("-" * 130)
        print("### 2.5 %s: il baricentro (%.2f, %.2f), il raggio della materia %.2f" % (nome.upper(), cb_[0], cb_[1], Rm_))
        for R in (10, 20, 30, 45, 60):
            a, rr = arco_all_anello(D_, th_, R)
            Dl, _G2, _p, _ph, _n, chiv, ctrl, _x = una(G, psi_, phi_, a)
            print("    anello %2d (%.2f nodi): %s" % (R, rr, riga(Dl)))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
