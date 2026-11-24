# -*- coding: utf-8 -*-
r"""**LA COVARIANTE, LA FAMIGLIA FRA D7 E LA COVARIANTE, E LO SPECCHIO VERO** *(Luca `2026-11-20` `11:57`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_e_specchio.md`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/covariante_e_famiglia.py parte K 2      (K = 0, 1)
    E:\python\py3132\python.exe doc/referti_l2/covariante_e_famiglia.py det A          (A = a, b: due processi)
    E:\python\py3132\python.exe doc/referti_l2/covariante_e_famiglia.py specchio
    E:\python\py3132\python.exe doc/referti_l2/covariante_e_famiglia.py referto > doc/referti_l2/covariante_e_famiglia.txt

**La covariante** *(S1 = la `6.3` delle `10:31`; la carta 1.1)*: le estremita' di `n` = la media delle estremita' di `i` e `j` nella stessa direzione; in `k` *(e `l`)* sull'arco nuovo la media delle estremita' di `k` verso `i` e verso `j`; in `i`, `j` il trasporto; **un fattore uniforme sulla stella** *(`i, j, k, l, n`)* che rimette la norma di prima, per `psi` e per `phi`. **E2** = `psi` e `phi` covarianti.
**La famiglia `beta`** *(1.2)*: sulla stella `psi = (1 - beta) D7 + beta COV`, il fattore `sqrt(N_D7 / N_misto)`; `phi` = FA; la radice per bisezione a `53` passi *(`nascita_energia_nulla.radice`)*.
**Lo specchio vero** *(1.3)*: nascere e specchiare contro specchiare e nascere, ARRAY PER ARRAY; D7, COV, la radice, la D7 simmetrica, e **il padre = il nodo di indice minore** *(DEVE FALLIRE)*.
**Lo stato:** C2 a `k 3000` *(NON quello allo scatto: dichiarato)*; i `2929` candidati nell'ordine di scatto.
"""
import hashlib
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "mattone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import nascita_energia_nulla as NN  # noqa: E402
import regole_fase_F3 as RF  # noqa: E402
import nascita_dentro_fuori as ND  # noqa: E402

GRIGLIA = np.linspace(0.0, 1.0, 11)
N_CASO, N_DET, N_FILA, N_SPECCHIO = 20, 100, 20, 200
SOGLIA, SOGLIA_DEVE_FALLIRE = 1e-10, 1e-6
DIR_O = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "covariante")
CHIAVI = NN.CHIAVI


# ---------------------------------------------------------------------------------------------- le regole
def trasportato(x, keep, a, m2):
    """### `x` (psi o phi) sul grafo nato: gli archi tenuti, e il TRASPORTO dell'arco tolto su `n -> i`, `n -> j`; il resto a 0 (senza D7)."""
    y = np.zeros((2 * m2,) + x.shape[1:], dtype=x.dtype)
    base = m2 - 4
    y[:2 * base] = x[np.repeat(keep, 2)]
    y[2 * (base + 0) + 1] = x[2 * a]
    y[2 * (base + 1) + 1] = x[2 * a + 1]
    return y


def cov_grezza(G, x, a, nodi, keep, m2):
    """### La covariante PRIMA del fattore (la carta 1.1)."""
    ii, jj, _nn, vec = G
    i, j, k, l = nodi["i"], nodi["j"], nodi["k"], nodi["l"]
    va = vec[a]
    im, jp = RF.opposto(G, i, va), RF.opposto(G, j, -va)

    def E(u, v):
        return RF.estremita_di(ii, jj, x, u, v)
    y = trasportato(x, keep, a, m2)
    b = m2 - 4
    y[2 * (b + 0)] = 0.5 * (x[2 * a + 1] + E(i, im))
    y[2 * (b + 1)] = 0.5 * (x[2 * a] + E(j, jp))
    y[2 * (b + 2)] = 0.5 * (E(i, k) + E(j, k))
    y[2 * (b + 3)] = 0.5 * (E(i, l) + E(j, l))
    y[2 * (b + 2) + 1] = 0.5 * (E(k, i) + E(k, j))
    y[2 * (b + 3) + 1] = 0.5 * (E(l, i) + E(l, j))
    return y


def norma(x, h):
    return float(np.sum(np.abs(x[h]) ** 2))


def stelle(G, G2, nodi):
    s_old = np.where(np.isin(ND.nodo_h(G[0], G[1]), [nodi["i"], nodi["j"], nodi["k"], nodi["l"]]))[0]
    s_new = np.where(np.isin(ND.nodo_h(G2[0], G2[1]), [nodi["i"], nodi["j"], nodi["k"], nodi["l"], nodi["n"]]))[0]
    return s_old, s_new


def cov(G, x, a, P, s_old, s_new):
    nodi, keep = P["out"][3], P["out"][4]
    y = cov_grezza(G, x, a, nodi, keep, len(P["G2"][0]))
    Nb, Na = norma(x, s_old), norma(y, s_new)
    if Nb > 0.0 and Na > 0.0:
        y[s_new] *= math.sqrt(Nb / Na)
    return y


def misto(D7, COV, beta, s_new, N_D7):
    m = D7.copy()
    m[s_new] = (1.0 - beta) * D7[s_new] + beta * COV[s_new]
    Nm = norma(m, s_new)
    if Nm > 0.0:
        m[s_new] *= math.sqrt(N_D7 / Nm)
    return m


def d7_simmetrica(P, G2, nodi):
    """### Nessun padre: ognuno dei due capi da' un QUARTO della sua norma; `n` nella direzione di `chi_i + chi_j` (la carta 1.3)."""
    y = P["p0"].copy()
    nodo2 = ND.nodo_h(G2[0], G2[1])
    hi, hj = np.where(nodo2 == nodi["i"])[0], np.where(nodo2 == nodi["j"])[0]
    Ni, Nj = norma(y, hi), norma(y, hj)
    chi = y[hi].sum(axis=0) + y[hj].sum(axis=0)
    y[hi] /= math.sqrt(4.0 / 3.0)
    y[hj] /= math.sqrt(4.0 / 3.0)
    nc = np.linalg.norm(chi)
    b = P["base"]
    for q in range(4):
        y[2 * (b + q)] = math.sqrt((Ni + Nj) / 16.0) * chi / nc if nc > 0 else 0.0
    return y


def tutto(G, psi, phi, a, F0m):
    """### Le regole sull'arco `a`: il grafo, D7, COV (psi e phi), la stella, e `dh(beta)`."""
    P = NN.preparo(G, psi, phi, a)
    G2, ph = P["G2"], P["ph"]
    nodi = P["out"][3]
    s_old, s_new = stelle(G, G2, nodi)
    D7 = NN.psi_alpha(P, 1.0)
    Cp = cov(G, psi, a, P, s_old, s_new)
    Cf = cov(G, phi, a, P, s_old, s_new)
    N_D7 = norma(D7, s_new)

    def dh(beta):
        return NN.F_mano(G2, misto(D7, Cp, beta, s_new, N_D7), ph)["tot"] - F0m["tot"]
    return {"P": P, "G2": G2, "ph": ph, "D7": D7, "Cp": Cp, "Cf": Cf, "s_new": s_new, "N_D7": N_D7, "dh": dh, "nodi": nodi}


def nascita(G, psi, phi, a, F0m, F0p, pieno=True):
    T = tutto(G, psi, phi, a, F0m)
    G2, ph = T["G2"], T["ph"]
    R = {}
    g = np.array([T["dh"](float(x)) for x in GRIGLIA])
    R["DH_d7"], R["DH_b1"] = float(g[0]), float(g[-1])
    R["cambi"] = int(np.sum(np.sign(g[1:]) != np.sign(g[:-1])))
    R["DH_sym"] = NN.F_mano(G2, d7_simmetrica(T["P"], G2, T["nodi"]), ph)["tot"] - F0m["tot"]
    be, stato = NN.radice(T["dh"], float(g[0]), float(g[-1]))
    R["beta"], R["stato"] = be, stato
    rad = None
    if stato != 1:
        rad = (G2, misto(T["D7"], T["Cp"], be, T["s_new"], T["N_D7"]), ph)
    if pieno:
        De = ND.delta(F0p, ND.famiglie(G2, T["Cp"], T["Cf"]))
        for k in CHIAVI:
            R["E2_" + k] = De[k]
        R["DH_e2_mano"] = NN.F_mano(G2, T["Cp"], T["Cf"])["tot"] - F0m["tot"]
        if rad is not None:
            Dr = ND.delta(F0p, ND.famiglie(*rad))
            for k in CHIAVI:
                R["R_" + k] = Dr[k]
    return R, rad, T


CAMPI = ("DH_d7", "DH_b1", "DH_sym", "cambi", "beta", "stato", "DH_e2_mano") + tuple("E2_" + k for k in CHIAVI) + tuple("R_" + k for k in CHIAVI)


def tabella(Rs):
    return {c: np.array([R.get(c, np.nan) for R in Rs], dtype=float) for c in CAMPI}


def sha(T):
    h = hashlib.sha1()
    for c in CAMPI:
        h.update(np.ascontiguousarray(T[c]).tobytes())
    return h.hexdigest()[:12]


def fila(G, psi, phi, archi, F0p):
    righe, salt = [], {"diviso": 0, "senza_radice": 0, "non_triangolo": 0}
    H = [F0p["tot"]]
    Gc, pc, fc = G, psi, phi
    Fm, Fp = NN.F_mano(Gc, pc, fc), F0p
    for a0 in archi:
        if len(righe) >= N_FILA:
            break
        i, j = int(G[0][a0]), int(G[1][a0])
        q = np.where((Gc[0] == i) & (Gc[1] == j))[0]
        if len(q) == 0:
            salt["diviso"] += 1
            continue
        try:
            R, rad, _T = nascita(Gc, pc, fc, int(q[0]), Fm, Fp, pieno=False)
        except AssertionError:
            salt["non_triangolo"] += 1
            continue
        if rad is None:
            salt["senza_radice"] += 1
            continue
        Gc, pc, fc = rad
        Fp = ND.famiglie(Gc, pc, fc)
        Fm = NN.F_mano(Gc, pc, fc)
        H.append(Fp["tot"])
        righe.append((int(a0), i, j, R["beta"], H[-1] - H[-2], abs(H[-1] - H[-2]) / abs(H[-2])))
    return righe, salt, np.array(H)


def corri(sel, nome):
    import _presidio
    _presidio.avvia(__file__)
    os.makedirs(DIR_O, exist_ok=True)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    assert len(archi) == 2929 and max(sel) < len(archi)
    F0m, F0p = NN.F_mano(G, psi, phi), ND.famiglie(G, psi, phi)
    print("### %s: %d archi; H %.10e" % (nome, len(sel), F0p["tot"]))
    Rs, t0 = [], time.time()
    for c, q in enumerate(sel):
        R, _r, _T = nascita(G, psi, phi, int(archi[q]), F0m, F0p)
        Rs.append(R)
        if c % 100 == 0:
            print("    %d su %d (%.0f s)" % (c, len(sel), time.time() - t0))
            sys.stdout.flush()
    T = tabella(Rs)
    extra = {}
    if nome.startswith("det"):
        righe, salt, H = fila(G, psi, phi, archi, F0p)
        extra = {"fila": np.array(righe, dtype=float).reshape(-1, 6), "fila_H": H}
        print("### la fila: %d nascite, saltati %s" % (len(righe), salt))
    np.savez(os.path.join(DIR_O, nome + ".npz"), sel=np.asarray(sel), tempo=time.time() - t0, **T, **extra)
    print("### %s: lo sha1 dei risultati %s; %.0f s" % (nome, sha(T), time.time() - t0))
    return 0


# ---------------------------------------------------------------------------------------------- lo specchio
def mappa_specchio(G, centro):
    import specchio_carta as SC
    from solitone import toro as TO
    ii, jj, nn, _v = G
    L = int(round(math.sqrt(nn)))
    v = np.arange(nn)
    A1, A2 = TO.vettori()
    d30 = 2 * A1 + A2
    p0 = (int(round(float(centro[0]))), int(round(float(centro[1]))))
    sig, scarto, _M = SC.mappa_nodi(L, (v // L).astype(float), (v % L).astype(float), p0, math.atan2(d30[1], d30[0]))
    assert scarto < 1e-9 and np.array_equal(sig[sig], v)
    ap, rov = SC.mappa_archi(ii, jj, sig)
    hp = np.empty(2 * len(ap), dtype=int)
    hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
    hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
    assert np.array_equal(ND.nodo_h(ii, jj)[hp], sig[ND.nodo_h(ii, jj)])
    return sig, ap, rov, hp, p0, scarto


def chiavi_h(ii, jj, N):
    k = np.empty(2 * len(ii), dtype=np.int64)
    k[0::2] = ii.astype(np.int64) * N + jj
    k[1::2] = jj.astype(np.int64) * N + ii
    return k


def confronta(A, B, sig2, N):
    """### `A` nato e poi specchiato contro `B` nato sullo stato specchiato: (max |psi| relativo, max |phi| relativo)."""
    (GA, pA, fA), (GB, pB, fB) = A, B
    kB = chiavi_h(GB[0], GB[1], N)
    kA = chiavi_h(sig2[GA[0]], sig2[GA[1]], N)
    o = np.argsort(kB, kind="stable")
    pos = np.searchsorted(kB[o], kA)
    m = o[np.minimum(pos, len(o) - 1)]
    assert np.array_equal(kB[m], kA), "i due grafi nati non sono lo specchio l'uno dell'altro"
    dp = float(np.max(np.abs(pA - pB[m]))) / max(float(np.max(np.abs(pA))), 1e-300)
    df = float(np.max(np.abs(fA - fB[m]))) / max(float(np.max(np.abs(fA))), 1e-300)
    return dp, df


def regole_specchio(G, psi, phi, a, F0m):
    """### Le cinque regole sull'arco `a`: `{nome: (G2, psi2, phi2) o None}`."""
    T = tutto(G, psi, phi, a, F0m)
    G2, ph = T["G2"], T["ph"]
    out = {"D7": (G2, T["D7"], ph), "COV": (G2, T["Cp"], T["Cf"]), "D7SIM": (G2, d7_simmetrica(T["P"], G2, T["nodi"]), ph)}
    g0, g1 = T["dh"](0.0), T["dh"](1.0)
    be, st = NN.radice(T["dh"], g0, g1)
    out["RADICE"] = None if st == 1 else (G2, misto(T["D7"], T["Cp"], be, T["s_new"], T["N_D7"]), ph)
    ii, jj, nn, vec = G
    if ii[a] < jj[a]:
        out["MINIMO"] = out["D7"]
    else:
        ii2, jj2, vec2 = ii.copy(), jj.copy(), vec.copy()
        ii2[a], jj2[a], vec2[a] = jj[a], ii[a], -vec[a]
        p2, f2 = psi.copy(), phi.copy()
        p2[2 * a], p2[2 * a + 1] = psi[2 * a + 1], psi[2 * a]
        f2[2 * a], f2[2 * a + 1] = phi[2 * a + 1], phi[2 * a]
        Gr = (ii2, jj2, nn, vec2)
        Pr = NN.preparo(Gr, p2, f2, a)
        out["MINIMO"] = (Pr["G2"], NN.psi_alpha(Pr, 1.0), Pr["ph"])
    return out


NOMI_S = ("D7", "COV", "RADICE", "D7SIM", "MINIMO")


def specchio():
    import _presidio
    _presidio.avvia(__file__)
    os.makedirs(DIR_O, exist_ok=True)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    sig, ap, rov, hp, p0, scarto = mappa_specchio(G, centro)
    psiR, phiR = np.empty_like(psi), np.empty_like(phi)
    psiR[hp], phiR[hp] = psi, phi
    F0m, FRm = NN.F_mano(G, psi, phi), NN.F_mano(G, psiR, phiR)
    N = G[2] + 1
    sig2 = np.append(sig, G[2])
    D = {nm: np.full((N_SPECCHIO, 2), np.nan) for nm in NOMI_S}
    t0 = time.time()
    for q in range(N_SPECCHIO):
        a = int(archi[q])
        A = regole_specchio(G, psi, phi, a, F0m)
        B = regole_specchio(G, psiR, phiR, int(ap[a]), FRm)
        for nm in NOMI_S:
            if A[nm] is not None and B[nm] is not None:
                D[nm][q] = confronta(A[nm], B[nm], sig2, N)
        if q % 20 == 0:
            print("    %d su %d (%.0f s)" % (q, N_SPECCHIO, time.time() - t0))
            sys.stdout.flush()
    np.savez(os.path.join(DIR_O, "specchio.npz"), rov=rov[archi[:N_SPECCHIO]], p0=np.array(p0), scarto=scarto,
             H=np.array([F0m["tot"], FRm["tot"]]), **{nm: D[nm] for nm in NOMI_S})
    print("### lo specchio: %.0f s" % (time.time() - t0))
    return 0


# ---------------------------------------------------------------------------------------------- il referto
def casi_noti(G, psi, phi, archi, F0m, F0p, esiti):
    ok_psi, ok_dh = True, True
    for a in archi[:N_CASO]:
        Dl, out = RF.nascita(G, psi, phi, int(a), "FA")
        T = tutto(G, psi, phi, int(a), F0m)
        m0 = misto(T["D7"], T["Cp"], 0.0, T["s_new"], T["N_D7"])
        ok_psi &= bool(np.array_equal(m0, out[1]))
        Dm = ND.delta(F0p, ND.famiglie(T["G2"], m0, T["ph"]))
        ok_dh &= all(Dm[k] == Dl[k] for k in CHIAVI)
    print("### IL CASO NOTO (beta = 0 contro regole_fase_F3.nascita FA, %d archi): psi al bit %s; ogni termine di dH al bit %s" % (N_CASO, ok_psi, ok_dh))
    esiti.append(("il caso noto: beta = 0 = regole_fase_F3.nascita(FA) AL BIT, psi e ogni termine (%d archi)" % N_CASO, ok_psi and ok_dh))
    cp = np.array([0.3 + 0.1j, -0.2 + 0.4j])
    cz = 0.6 - 0.8j
    pu = np.tile(cp, (len(psi), 1))
    fu = np.full(len(phi), cz)
    a = int(archi[0])
    P = NN.preparo(G, pu, fu, a)
    yp = cov_grezza(G, pu, a, P["out"][3], P["out"][4], len(P["G2"][0]))
    yf = cov_grezza(G, fu, a, P["out"][3], P["out"][4], len(P["G2"][0]))
    b = len(P["G2"][0]) - 4
    nuove = [2 * (b + q) for q in range(4)] + [2 * (b + 2) + 1, 2 * (b + 3) + 1]
    ok_u = bool(np.all(yp[nuove] == cp)) and bool(np.all(yf[nuove] == cz))
    print("### IL CASO NOTO DEL CODICE: sul campo uniforme le 6 estremita' nuove della covariante (prima del fattore) = il valore AL BIT: %s" % ok_u)
    esiti.append(("il caso noto: sul campo uniforme la covariante (prima del fattore) da' il valore AL BIT", ok_u))
    return ok_psi and ok_dh and ok_u


def vuoto_F3(esiti):
    import _massa_nei_difetti as MD
    import mattone as MT
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L = Z["L"]
        ii, jj, nn, dirs = MD.toro(L)
        phi_v = np.asarray(Z["phi_v"]).copy()
    G = (ii, jj, nn, np.asarray(dirs, dtype=float))
    psi0 = np.zeros((len(phi_v), 2), dtype=complex)
    a = 3 * (81 * L + 81)
    F0 = ND.famiglie(G, psi0, phi_v)
    with np.errstate(invalid="ignore", divide="ignore"):
        P = NN.preparo(G, psi0, phi_v, a)
    s_old, s_new = stelle(G, P["G2"], P["out"][3])
    Cp = cov(G, psi0, a, P, s_old, s_new)
    Cf = cov(G, phi_v, a, P, s_old, s_new)
    D = ND.delta(F0, ND.famiglie(P["G2"], Cp, Cf))
    atteso = F0["tot"] / nn
    print("### LA PREVISIONE SUL VUOTO F3 PURO (S162, L %d, n %d, l'arco %d): H/n = %+.6e (il numero che la covariante DEVE dare); DH_cov = %+.6e; lo scarto relativo %.3e; per termine: %s" % (
        L, nn, a, atteso, D["tot"], abs(D["tot"] - atteso) / abs(atteso), ", ".join("%s %+.4e" % (k, D[k]) for k in CHIAVI[:-1])))
    esiti.append(("la previsione: sul vuoto F3 puro DH_cov = H/n entro 1e-6 relativo (la carta 1.4: credo di NO)", abs(D["tot"] - atteso) <= 1e-6 * abs(atteso)))


def referto():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "nascita_energia_nulla.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    print("=" * 130)
    print("LA COVARIANTE, LA FAMIGLIA FRA D7 E LA COVARIANTE, E LO SPECCHIO VERO (Luca 2026-11-20 11:57); lo stato di C2 a k 3000 (dichiarato)")
    print("=" * 130)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    F0m, F0p = NN.F_mano(G, psi, phi), ND.famiglie(G, psi, phi)
    esiti = []
    if not casi_noti(G, psi, phi, archi, F0m, F0p, esiti):
        print("### UN CASO NOTO DEL CODICE FALLISCE: FERMO")
    print("-" * 130)
    vuoto_F3(esiti)
    print("-" * 130)
    T = {c: np.full(len(archi), np.nan) for c in CAMPI}
    for p in sorted(x for x in os.listdir(DIR_O) if x.startswith("parte_")):
        with np.load(os.path.join(DIR_O, p)) as d:
            for c in CAMPI:
                T[c][d["sel"]] = d[c]
            print("### %s: %d archi, %.0f s" % (p, len(d["sel"]), float(d["tempo"])))
    e2 = T["E2_tot"]
    print("### E2 (la covariante, psi e phi): DH_cov min %+.4e, mediana %+.4e, max %+.4e; negativi %d su %d; |conto a mano - pieno| max %.3e" % (
        np.nanmin(e2), np.nanmedian(e2), np.nanmax(e2), int(np.sum(e2 < 0)), len(e2), float(np.nanmax(np.abs(T["DH_e2_mano"] - e2)))))
    print("    DH(D7) mediana %+.4e; |DH_cov| mediano / |DH(D7)| mediano = %.4f; per termine (la mediana): %s" % (
        np.median(T["DH_d7"]), float(np.median(np.abs(e2))) / float(np.median(np.abs(T["DH_d7"]))), ", ".join("%s %+.4e" % (k, float(np.median(T["E2_" + k]))) for k in CHIAVI[:-1])))
    print("    beta = 1 (la covariante con phi FA) contro E2: la differenza di DH mediana %+.4e (max |.| %.4e)" % (float(np.median(T["DH_b1"] - e2)), float(np.max(np.abs(T["DH_b1"] - e2)))))
    print("    la D7 simmetrica: DH mediana %+.4e (min %+.4e, max %+.4e)" % (np.median(T["DH_sym"]), np.min(T["DH_sym"]), np.max(T["DH_sym"])))
    st = T["stato"]
    rad = st != 1
    n_rad = int(np.sum(rad))
    be = T["beta"][rad]
    print("### ### LA FAMIGLIA BETA: LA RADICE su %d archi su %d (%.2f%%); DH(beta=1) positivi %d; i cambi di segno sugli 11 punti %s" % (
        n_rad, len(archi), 100.0 * n_rad / len(archi), int(np.sum(T["DH_b1"] > 0)), {int(k): int(v) for k, v in zip(*np.unique(T["cambi"], return_counts=True))}))
    if n_rad:
        print("    beta*: min %.6f, mediana %.6f, max %.6f; alla radice col conto pieno |DH| max %.3e (relativo a |H| %.3e); per termine (mediana): %s" % (
            be.min(), np.median(be), be.max(), np.nanmax(np.abs(T["R_tot"][rad])), np.nanmax(np.abs(T["R_tot"][rad])) / abs(F0p["tot"]), ", ".join("%s %+.4e" % (k, float(np.nanmedian(T["R_" + k][rad]))) for k in CHIAVI[:-1])))
    print("    PER ANELLO:")
    for lo in range(10, 24, 2):
        s = (r >= lo) & (r < lo + 2)
        if s.any():
            sr = s & rad
            print("      r %2d-%2d: %4d archi; DH(D7) %+.4e, DH_cov %+.4e, DH(beta=1) %+.4e, DH sim %+.4e (le mediane); la radice %4d, beta* mediana %s" % (
                lo, lo + 2, int(s.sum()), np.median(T["DH_d7"][s]), np.median(e2[s]), np.median(T["DH_b1"][s]), np.median(T["DH_sym"][s]), int(sr.sum()),
                "%.4f" % float(np.median(T["beta"][sr])) if sr.any() else "-"))
    esiti.append(("P-C1: |DH_cov| mediano sotto il 30%% di |DH(D7)| mediano", float(np.median(np.abs(e2))) < 0.3 * float(np.median(np.abs(T["DH_d7"])))))
    esiti.append(("P-E2: DH_cov negativo su piu' della meta' degli archi", int(np.sum(e2 < 0)) > len(e2) / 2.0))
    esiti.append(("P-C2: la radice della famiglia beta su almeno l'80%% degli archi (%.2f%%)" % (100.0 * n_rad / len(archi)), n_rad >= 0.8 * len(archi)))
    print("-" * 130)
    Dd = {}
    for x in ("det_a", "det_b"):
        with np.load(os.path.join(DIR_O, x + ".npz")) as d:
            Dd[x] = {k: d[k].copy() for k in d.files if k != "tempo"}
    uguali = all(np.array_equal(Dd["det_a"][k], Dd["det_b"][k], equal_nan=True) for k in Dd["det_a"])
    s = Dd["det_a"]["sel"]
    contro = all(np.array_equal(Dd["det_a"][c], T[c][s], equal_nan=True) for c in CAMPI)
    print("### IL DETERMINISMO: det_a e det_b AL BIT %s; contro le parti sugli stessi %d archi %s" % (uguali, len(s), contro))
    fl, H = Dd["det_a"]["fila"], Dd["det_a"]["fila_H"]
    print("### LE NASCITE IN FILA alla radice: %d; H prima %.10e" % (len(fl), H[0]))
    for q, x in enumerate(fl):
        print("    %2d: l'arco %6d (%d -> %d): beta* %.6f; H(dopo) - H(prima) %+.3e; relativo %.3e" % (q + 1, int(x[0]), int(x[1]), int(x[2]), x[3], x[4], x[5]))
    esiti.append(("P-C4: deterministica AL BIT (due processi) e uguale alle parti", uguali and contro))
    esiti.append(("P-C4: %d nascite in fila, |H(dopo) - H(prima)|/|H| sotto 1e-10 dopo ognuna" % N_FILA, len(fl) == N_FILA and bool(np.all(fl[:, 5] < 1e-10))))
    print("-" * 130)
    with np.load(os.path.join(DIR_O, "specchio.npz")) as d:
        rv = d["rov"]
        S = {nm: d[nm].copy() for nm in NOMI_S}
        print("### LO SPECCHIO VERO a 30 gradi per il nodo %s (lo scarto %.1e); H dello stato specchiato contro H relativo %.3e; i primi %d archi: %d a verso conservato, %d ROVESCIATI" % (
            tuple(d["p0"]), float(d["scarto"]), abs(d["H"][1] - d["H"][0]) / abs(d["H"][0]), N_SPECCHIO, int(np.sum(~rv)), int(np.sum(rv))))
    sim = {}
    for nm in NOMI_S:
        X = S[nm]
        ok_n = ~np.isnan(X[:, 0])
        for cl, m in (("conservati", ~rv), ("ROVESCIATI", rv)):
            mm = m & ok_n
            if mm.any():
                print("    %-7s %-10s %3d archi: psi max %.3e (sopra 1e-10: %3d), phi max %.3e (sopra 1e-10: %3d)" % (
                    nm, cl, int(mm.sum()), np.max(X[mm, 0]), int(np.sum(X[mm, 0] > SOGLIA)), np.max(X[mm, 1]), int(np.sum(X[mm, 1] > SOGLIA))))
            else:
                print("    %-7s %-10s   0 archi confrontabili" % (nm, cl))
        sim[nm] = bool(ok_n.any()) and bool(np.all(np.nanmax(X[ok_n], axis=1) < SOGLIA)) if ok_n.any() else None
    mn = S["MINIMO"]
    fallisce = bool(np.nanmax(mn) > SOGLIA_DEVE_FALLIRE)
    print("    il caso che DEVE FALLIRE (il padre = l'indice minore): lo scarto massimo %.3e (deve superare %.0e)" % (float(np.nanmax(mn)), SOGLIA_DEVE_FALLIRE))
    esiti.append(("DEVE FALLIRE: il padre = il nodo di indice minore da' uno scarto sopra 1e-6 (o la prova non vale: FERMO)", fallisce))
    if not fallisce:
        print("### ### IL CASO CHE DEVE FALLIRE NON FALLISCE: LA PROVA DELLO SPECCHIO NON VALE: FERMO")
    d7 = S["D7"]
    esiti.append(("P-C3: D7 NON simmetrica sulla classe rovesciata (sopra 1e-10 su almeno un arco rovesciato)", bool(np.nanmax(d7[rv]) > SOGLIA)))
    esiti.append(("P-C3: la covariante simmetrica su tutte le classi (sotto 1e-10)", sim["COV"] is True))
    esiti.append(("la radice della famiglia simmetrica allo specchio (sotto 1e-10 su tutti gli archi confrontabili)", sim["RADICE"] is True))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-118s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("### %.0f s" % (time.time() - t00))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "parte":
        K, NP = int(sys.argv[2]), int(sys.argv[3])
        sys.exit(corri([q for q in range(2929) if q % NP == K], "parte_%d" % K))
    if sys.argv[1] == "det":
        sys.exit(corri(list(range(N_DET)), "det_" + sys.argv[2]))
    if sys.argv[1] == "specchio":
        sys.exit(specchio())
    sys.exit(referto())
