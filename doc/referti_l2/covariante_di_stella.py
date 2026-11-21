# -*- coding: utf-8 -*-
r"""**LA COVARIANTE DI STELLA** *(Luca `2026-11-20` `13:33`, TODO 2; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/covariante_di_stella.py parte K 2      (K = 0, 1)
    E:\python\py3132\python.exe doc/referti_l2/covariante_di_stella.py det A          (A = a, b: due processi)
    E:\python\py3132\python.exe doc/referti_l2/covariante_di_stella.py specchio
    E:\python\py3132\python.exe doc/referti_l2/covariante_di_stella.py referto > doc/referti_l2/covariante_di_stella.txt

**La covariante di stella** *(la carta 1.1)*: `n -> k` = la media di `i -> k` e `j -> k` *(lo stesso per `l`)*; `n -> i` = l'estremita' di `j` verso `i`; `n -> j` = quella di `i` verso `j`; l'estremita' nuova di `k` = la media di `k -> i` e `k -> j` *(lo stesso per `l`)*; in `i` e `j` il trasporto *(la mia lettura, dichiarata)*; un fattore uniforme sulla stella per `psi` e uno per `phi`. **Solo `i, j, k, l`.**
**`E_persa` = `- somma dei DH`** *(la carta 1.2)*; nella fila `DH` a mano alla nascita, `H` col conto pieno dopo.
**Lo stato:** C2 a `k 3000` *(NON quello allo scatto: dichiarato)*. **E2 e D7 accanto:** dalle parti della sez. `17` *(`E:/soliton_simulator/controllo/covariante/`)*.
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
import covariante_e_famiglia as CF  # noqa: E402
import nascita_energia_nulla as NN  # noqa: E402
import regole_fase_F3 as RF  # noqa: E402
import nascita_dentro_fuori as ND  # noqa: E402

N_DET, N_FILA, N_SPECCHIO = 100, 20, 200
SOGLIA_SPECCHIO, SOGLIA_DEVE_FALLIRE, SOGLIA_EPERSA = 1e-14, 1e-6, 1e-12
DIR_O = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "stella")
CHIAVI = NN.CHIAVI


def sc_grezza(G, x, a, nodi, keep, m2):
    """### La covariante di stella PRIMA del fattore (la carta 1.1)."""
    ii, jj = G[0], G[1]
    i, j, k, l = nodi["i"], nodi["j"], nodi["k"], nodi["l"]

    def E(u, v):
        return RF.estremita_di(ii, jj, x, u, v)
    y = CF.trasportato(x, keep, a, m2)
    b = m2 - 4
    y[2 * (b + 0)] = x[2 * a + 1]
    y[2 * (b + 1)] = x[2 * a]
    y[2 * (b + 2)] = 0.5 * (E(i, k) + E(j, k))
    y[2 * (b + 3)] = 0.5 * (E(i, l) + E(j, l))
    y[2 * (b + 2) + 1] = 0.5 * (E(k, i) + E(k, j))
    y[2 * (b + 3) + 1] = 0.5 * (E(l, i) + E(l, j))
    return y


def sc(G, x, a, P, s_old, s_new):
    y = sc_grezza(G, x, a, P["out"][3], P["out"][4], len(P["G2"][0]))
    Nb, Na = CF.norma(x, s_old), CF.norma(y, s_new)
    if Nb > 0.0 and Na > 0.0:
        y[s_new] *= math.sqrt(Nb / Na)
    return y


def nascita(G, psi, phi, a, F0m, F0p, pieno=True):
    P = NN.preparo(G, psi, phi, a)
    G2 = P["G2"]
    s_old, s_new = CF.stelle(G, G2, P["out"][3])
    Sp, Sf = sc(G, psi, a, P, s_old, s_new), sc(G, phi, a, P, s_old, s_new)
    R = {"DH_mano": NN.F_mano(G2, Sp, Sf)["tot"] - F0m["tot"],
         "Mp": CF.norma(Sp, s_new) - CF.norma(psi, s_old), "Mf": CF.norma(Sf, s_new) - CF.norma(phi, s_old)}
    if pieno:
        Dl = ND.delta(F0p, ND.famiglie(G2, Sp, Sf))
        for k in CHIAVI:
            R["SC_" + k] = Dl[k]
    return R, (G2, Sp, Sf)


CAMPI = ("DH_mano", "Mp", "Mf") + tuple("SC_" + k for k in CHIAVI)


def tabella(Rs):
    return {c: np.array([R.get(c, np.nan) for R in Rs], dtype=float) for c in CAMPI}


def sha(T):
    h = hashlib.sha1()
    for c in CAMPI:
        h.update(np.ascontiguousarray(T[c]).tobytes())
    return h.hexdigest()[:12]


def fila(G, psi, phi, archi, F0p):
    righe, salt = [], {"diviso": 0, "non_triangolo": 0, "non_definita": 0}
    H0 = F0p["tot"]
    Gc, pc, fc = G, psi, phi
    Fm, Fp = NN.F_mano(Gc, pc, fc), F0p
    Ep = 0.0
    for c, a0 in enumerate(archi):
        if len(righe) >= N_FILA:
            break
        i, j = int(G[0][a0]), int(G[1][a0])
        q = np.where((Gc[0] == i) & (Gc[1] == j))[0]
        if len(q) == 0:
            salt["diviso"] += 1
            continue
        try:
            R, nuovo = nascita(Gc, pc, fc, int(q[0]), Fm, Fp, pieno=False)
        except AssertionError:
            salt["non_triangolo"] += 1
            print("    il candidato %d (l'arco %d: %d -> %d): i due estremi NON hanno due vicini comuni (la divisione non e' definita)" % (c, int(a0), i, j))
            continue
        except RuntimeError as e:
            salt["non_definita"] += 1
            print("    il candidato %d (l'arco %d: %d -> %d): NON definita (%s)" % (c, int(a0), i, j, e))
            continue
        Ep -= R["DH_mano"]
        Gc, pc, fc = nuovo
        Fp = ND.famiglie(Gc, pc, fc)
        Fm = NN.F_mano(Gc, pc, fc)
        sc_ = abs(Fp["tot"] + Ep - H0) / abs(H0)
        righe.append((int(a0), i, j, R["DH_mano"], Fp["tot"], Ep, sc_))
        print("    la nascita %2d (il candidato %d, l'arco %d: %d -> %d): DH %+.6e; H %.10e; E_persa %+.6e; |H + E_persa - H0|/|H0| %.3e" % (len(righe), c, int(a0), i, j, R["DH_mano"], Fp["tot"], Ep, sc_))
        sys.stdout.flush()
    return righe, salt


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
        R, _n = nascita(G, psi, phi, int(archi[q]), F0m, F0p)
        Rs.append(R)
        if c % 100 == 0:
            print("    %d su %d (%.0f s)" % (c, len(sel), time.time() - t0))
            sys.stdout.flush()
    T = tabella(Rs)
    f = os.path.join(DIR_O, nome + ".npz")
    np.savez(f, sel=np.asarray(sel), tempo=time.time() - t0, **T)
    print("### %s: salvato; lo sha1 dei risultati %s; %.0f s" % (nome, sha(T), time.time() - t0))
    sys.stdout.flush()
    if nome.startswith("det"):
        righe, salt = fila(G, psi, phi, archi, F0p)
        np.savez(f, sel=np.asarray(sel), tempo=time.time() - t0, fila=np.array(righe, dtype=float).reshape(-1, 7), salt=np.array([salt[k] for k in ("diviso", "non_triangolo", "non_definita")]), **T)
        print("### la fila: %d nascite, saltati %s; %.0f s" % (len(righe), salt, time.time() - t0))
    return 0


def specchio():
    import _presidio
    _presidio.avvia(__file__)
    os.makedirs(DIR_O, exist_ok=True)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    sig, ap, rov, hp, p0, scarto = CF.mappa_specchio(G, centro)
    psiR, phiR = np.empty_like(psi), np.empty_like(phi)
    psiR[hp], phiR[hp] = psi, phi
    F0m, FRm = NN.F_mano(G, psi, phi), NN.F_mano(G, psiR, phiR)
    F0p = ND.famiglie(G, psi, phi)
    N = G[2] + 1
    sig2 = np.append(sig, G[2])
    nomi = ("SC", "MINIMO")
    D = {nm: np.full((N_SPECCHIO, 2), np.nan) for nm in nomi}
    t0 = time.time()
    for q in range(N_SPECCHIO):
        a = int(archi[q])
        _r, A = nascita(G, psi, phi, a, F0m, F0p, pieno=False)
        _r, B = nascita(G, psiR, phiR, int(ap[a]), FRm, F0p, pieno=False)
        D["SC"][q] = CF.confronta(A, B, sig2, N)
        mA = CF.regole_specchio(G, psi, phi, a, F0m)["MINIMO"]
        mB = CF.regole_specchio(G, psiR, phiR, int(ap[a]), FRm)["MINIMO"]
        D["MINIMO"][q] = CF.confronta(mA, mB, sig2, N)
        if q % 20 == 0:
            print("    %d su %d (%.0f s)" % (q, N_SPECCHIO, time.time() - t0))
            sys.stdout.flush()
    np.savez(os.path.join(DIR_O, "specchio.npz"), rov=rov[archi[:N_SPECCHIO]], p0=np.array(p0), scarto=scarto, H=np.array([F0m["tot"], FRm["tot"]]), **D)
    print("### lo specchio: %.0f s" % (time.time() - t0))
    return 0


def vuoto_F3():
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
    s_old, s_new = CF.stelle(G, P["G2"], P["out"][3])
    D = ND.delta(F0, ND.famiglie(P["G2"], sc(G, psi0, a, P, s_old, s_new), sc(G, phi_v, a, P, s_old, s_new)))
    print("### IL VUOTO F3 PURO (S162, L %d, l'arco %d; NESSUNA attesa, dichiarato): DH_SC %+.6e; per termine: %s; accanto E2 +3.384608e-02 (covariante_vuoto_F3.txt) e FA +3.476457e+00 (regole_fase_F3.txt)" % (
        L, a, D["tot"], ", ".join("%s %+.4e" % (k, D[k]) for k in CHIAVI[:-1])))


def referto():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "covariante_e_famiglia.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    print("=" * 130)
    print("LA COVARIANTE DI STELLA (Luca 2026-11-20 13:33); lo stato di C2 a k 3000 (dichiarato)")
    print("=" * 130)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    esiti = []
    cp, cz = np.array([0.3 + 0.1j, -0.2 + 0.4j]), 0.6 - 0.8j
    pu, fu = np.tile(cp, (len(psi), 1)), np.full(len(phi), cz)
    a = int(archi[0])
    P = NN.preparo(G, pu, fu, a)
    m2 = len(P["G2"][0])
    yp, yf = sc_grezza(G, pu, a, P["out"][3], P["out"][4], m2), sc_grezza(G, fu, a, P["out"][3], P["out"][4], m2)
    b = m2 - 4
    nuove = [2 * (b + q) for q in range(4)] + [2 * (b + 2) + 1, 2 * (b + 3) + 1]
    ok_u = bool(np.all(yp[nuove] == cp)) and bool(np.all(yf[nuove] == cz))
    print("### IL CASO NOTO DEL CODICE: sul campo uniforme le 6 estremita' nuove (prima del fattore) = il valore AL BIT: %s" % ok_u)
    esiti.append(("il caso noto: sul campo uniforme la covariante di stella (prima del fattore) da' il valore AL BIT", ok_u))
    if not ok_u:
        print("### IL CASO NOTO FALLISCE: FERMO")
    print("-" * 130)
    vuoto_F3()
    print("-" * 130)
    T = {c: np.full(len(archi), np.nan) for c in CAMPI}
    for p in sorted(x for x in os.listdir(DIR_O) if x.startswith("parte_")):
        with np.load(os.path.join(DIR_O, p)) as d:
            for c in CAMPI:
                T[c][d["sel"]] = d[c]
            print("### %s: %d archi, %.0f s" % (p, len(d["sel"]), float(d["tempo"])))
    V = {c: np.full(len(archi), np.nan) for c in ("E2_tot", "DH_d7")}
    for p in sorted(x for x in os.listdir(CF.DIR_O) if x.startswith("parte_")):
        with np.load(os.path.join(CF.DIR_O, p)) as d:
            for c in V:
                V[c][d["sel"]] = d[c]
    definiti = int(np.sum(~np.isnan(T["SC_tot"])))
    dh = T["SC_tot"]
    print("### DH_SC: definita su %d archi su %d; min %+.4e, mediana %+.4e, max %+.4e; negativi %d; |a mano - pieno| max %.3e; la norma (materia, vuoto) dopo - prima: max |.| %.3e, %.3e" % (
        definiti, len(archi), np.nanmin(dh), np.nanmedian(dh), np.nanmax(dh), int(np.sum(dh < 0)), float(np.nanmax(np.abs(T["DH_mano"] - dh))), float(np.nanmax(np.abs(T["Mp"]))), float(np.nanmax(np.abs(T["Mf"])))))
    print("    accanto (le mediane): E2 %+.4e, D7 %+.4e; DH_SC per termine (mediane): %s" % (np.median(V["E2_tot"]), np.median(V["DH_d7"]), ", ".join("%s %+.4e" % (k, float(np.nanmedian(T["SC_" + k]))) for k in CHIAVI[:-1])))
    print("    DH_SC - E2: mediana %+.4e, max |.| %.4e" % (float(np.nanmedian(dh - V["E2_tot"])), float(np.nanmax(np.abs(dh - V["E2_tot"])))))
    print("    PER ANELLO (le mediane):")
    for lo in range(10, 24, 2):
        s = (r >= lo) & (r < lo + 2)
        if s.any():
            print("      r %2d-%2d: %4d archi; DH_SC %+.4e (materia %+.4e, vuoto %+.4e, N %+.4e); E2 %+.4e; D7 %+.4e" % (
                lo, lo + 2, int(s.sum()), np.nanmedian(dh[s]), np.nanmedian(T["SC_G_psi"][s] + T["SC_a_psi"][s]), np.nanmedian(T["SC_G_phi"][s] + T["SC_a_phi"][s]),
                np.nanmedian(T["SC_N"][s]), np.median(V["E2_tot"][s]), np.median(V["DH_d7"][s])))
    esiti.append(("P-SC1 (gli archi): definita sul 100%% dei 2929 (%d)" % definiti, definiti == len(archi)))
    esiti.append(("P-SC3: DH_SC mediano negativo e fra -40 e 0 (%+.3f)" % float(np.nanmedian(dh)), -40.0 <= float(np.nanmedian(dh)) < 0.0))
    print("-" * 130)
    Dd = {}
    for x in ("det_a", "det_b"):
        with np.load(os.path.join(DIR_O, x + ".npz")) as d:
            Dd[x] = {k: d[k].copy() for k in d.files if k != "tempo"}
    uguali = all(np.array_equal(Dd["det_a"][k], Dd["det_b"][k], equal_nan=True) for k in Dd["det_a"])
    s = Dd["det_a"]["sel"]
    contro = all(np.array_equal(Dd["det_a"][c], T[c][s], equal_nan=True) for c in CAMPI)
    print("### IL DETERMINISMO: det_a e det_b AL BIT %s; contro le parti sugli stessi %d archi %s" % (uguali, len(s), contro))
    esiti.append(("il determinismo: due processi AL BIT (i %d archi e la fila) e uguali alle parti" % N_DET, uguali and contro))
    fl, salt = Dd["det_a"]["fila"], Dd["det_a"]["salt"]
    print("### LA FILA: %d nascite; saltati: divisi %d, senza due vicini comuni %d, NON definite %d" % (len(fl), int(salt[0]), int(salt[1]), int(salt[2])))
    for q, x in enumerate(fl):
        print("    %2d: l'arco %6d (%d -> %d): DH %+.6e; H %.10e; E_persa %+.6e; |H + E_persa - H0|/|H0| %.3e" % (q + 1, int(x[0]), int(x[1]), int(x[2]), x[3], x[4], x[5], x[6]))
    esiti.append(("P-SC1 (la fila): %d nascite, NESSUNA non definita" % N_FILA, len(fl) == N_FILA and int(salt[1]) == 0 and int(salt[2]) == 0))
    esiti.append(("P-SC4: nella fila |H + E_persa - H0|/|H0| sotto 1e-12 dopo ognuna", len(fl) == N_FILA and bool(np.all(fl[:, 6] < SOGLIA_EPERSA))))
    print("-" * 130)
    with np.load(os.path.join(DIR_O, "specchio.npz")) as d:
        rv = d["rov"]
        S = {nm: d[nm].copy() for nm in ("SC", "MINIMO")}
        print("### LO SPECCHIO VERO a 30 gradi per il nodo %s (lo scarto %.1e); H dello stato specchiato contro H relativo %.3e; %d archi: %d conservati, %d ROVESCIATI" % (
            tuple(int(x) for x in d["p0"]), float(d["scarto"]), abs(d["H"][1] - d["H"][0]) / abs(d["H"][0]), len(rv), int(np.sum(~rv)), int(np.sum(rv))))
    for nm in ("SC", "MINIMO"):
        for cl, m in (("conservati", ~rv), ("ROVESCIATI", rv)):
            X = S[nm][m]
            print("    %-7s %-10s %3d archi: psi max %.3e (sopra %.0e: %3d), phi max %.3e (sopra: %3d)" % (nm, cl, len(X), np.max(X[:, 0]), SOGLIA_SPECCHIO, int(np.sum(X[:, 0] > SOGLIA_SPECCHIO)), np.max(X[:, 1]), int(np.sum(X[:, 1] > SOGLIA_SPECCHIO))))
    fallisce = bool(np.max(S["MINIMO"]) > SOGLIA_DEVE_FALLIRE)
    print("    il caso che DEVE FALLIRE (il padre a indice minore): lo scarto massimo %.3e (deve superare %.0e)" % (float(np.max(S["MINIMO"])), SOGLIA_DEVE_FALLIRE))
    esiti.append(("DEVE FALLIRE: il padre a indice minore sopra 1e-6 (o la prova non vale: FERMO)", fallisce))
    esiti.append(("P-SC2: la covariante di stella simmetrica su tutte le classi entro 1e-14", bool(np.all(S["SC"] < SOGLIA_SPECCHIO))))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-118s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    cond = all(ok for nm, ok in esiti if not nm.startswith("P-SC3"))      # ### le condizioni di Luca (e i casi noti); P-SC3 e' una previsione, non una condizione
    print("### LA CONDIZIONE DI LUCA PER PROSEGUIRE (definita al 100%%, simmetrica entro 1e-14, deterministica, H + E_persa entro 1e-12): %s" % ("PASSA" if cond else "### CADE: FERMO"))
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
