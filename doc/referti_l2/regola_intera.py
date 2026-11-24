# -*- coding: utf-8 -*-
r"""**LA REGOLA INTERA: LA NASCITA DI STELLA, I QUATTRO FLIP, LA SCELTA (A)** *(l'aggiunta di Luca `2026-11-20` `14:53`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md`, sez. `8`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/regola_intera.py parte K 2      (K = 0, 1)
    E:\python\py3132\python.exe doc/referti_l2/regola_intera.py specchio
    E:\python\py3132\python.exe doc/referti_l2/regola_intera.py referto > doc/referti_l2/regola_intera.txt

**La scelta (A)** *(D-FLIP-SCELTA)*: fra i quattro lati `(i, k)`, `(j, k)`, `(j, l)`, `(i, l)` si gira quello che lascia `H` piu' BASSA dopo, **col conto PIENO** *(`nascita_dentro_fuori.famiglie`)*; **se il migliore e il secondo distano meno di `GUARDIA |H|` = `1e-12 |H|`: NESSUN flip** *(una guardia contro l'arrotondamento, non una manopola: `A1`)*. **`E_persa = - (DH nascita + DH flip)`.**
**P5 sulla regola intera** *(i primi `200` archi)*: nascere e girare il flip scelto, poi specchiare, contro specchiare e fare la regola intera sull'arco specchiato; **il caso che DEVE FALLIRE:** la regola col flip col VERSO *(`flip_di_stella.gira(..., "verso")`, scelto allo stesso modo)*.
**Lo stato:** C2 a `k 3000` *(dichiarato)*.
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "mattone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import covariante_e_famiglia as CF  # noqa: E402
import flip_di_stella as FS  # noqa: E402
import nascita_energia_nulla as NN  # noqa: E402
import nascita_dentro_fuori as ND  # noqa: E402

GUARDIA = 1e-12
N_SPECCHIO = 200
SOGLIA, SOGLIA_DEVE_FALLIRE = 1e-14, 1e-6
DIR_O = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "regola")


def regola(G, psi, phi, a, H0, giro="stella"):
    """### La regola intera sull'arco `a`: `(R, stato_finale)`; `R` con i quattro `H`, la scelta, lo scarto, i `DH`."""
    A2, nd = FS.nasci_stella(G, psi, phi, a)
    Hb = ND.famiglie(*A2)["tot"]
    lati = ((nd["i"], nd["k"]), (nd["j"], nd["k"]), (nd["j"], nd["l"]), (nd["i"], nd["l"]))
    Hs, St = [], []
    for x, y in lati:
        A3, _info = FS.gira(*A2, x, y, nd["n"], giro)
        Hs.append(ND.famiglie(*A3)["tot"])
        St.append(A3)
    o = np.argsort(np.array(Hs), kind="stable")
    gap = Hs[o[1]] - Hs[o[0]]
    pari = gap < GUARDIA * abs(Hs[o[0]])
    R = {"H": Hs, "scelto": -1 if pari else int(o[0]), "gap": gap / abs(Hs[o[0]]), "DH_nascita": Hb - H0,
         "DH_flip": 0.0 if pari else Hs[o[0]] - Hb, "lati": lati, "nodi": nd}
    return R, (A2 if pari else St[int(o[0])])


def corri(sel, nome):
    import _presidio
    _presidio.avvia(__file__)
    os.makedirs(DIR_O, exist_ok=True)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    assert len(archi) == 2929 and max(sel) < len(archi)
    H0 = ND.famiglie(G, psi, phi)["tot"]
    print("### %s: %d archi; H %.10e" % (nome, len(sel), H0))
    out = {k: [] for k in ("scelto", "gap", "DH_nascita", "DH_flip", "H4")}
    t0 = time.time()
    for c, q in enumerate(sel):
        R, _s = regola(G, psi, phi, int(archi[q]), H0)
        for k in ("scelto", "gap", "DH_nascita", "DH_flip"):
            out[k].append(R[k])
        out["H4"].append(R["H"])
        if c % 100 == 0:
            print("    %d su %d (%.0f s)" % (c, len(sel), time.time() - t0))
            sys.stdout.flush()
    np.savez(os.path.join(DIR_O, nome + ".npz"), sel=np.asarray(sel), tempo=time.time() - t0, **{k: np.array(v) for k, v in out.items()})
    print("### %s: %.0f s" % (nome, time.time() - t0))
    return 0


def specchio():
    import _presidio
    _presidio.avvia(__file__)
    os.makedirs(DIR_O, exist_ok=True)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    sig, ap, rov, hp, p0, scarto = CF.mappa_specchio(G, centro)
    psiR, phiR = np.empty_like(psi), np.empty_like(phi)
    psiR[hp], phiR[hp] = psi, phi
    H0, H0R = ND.famiglie(G, psi, phi)["tot"], ND.famiglie(G, psiR, phiR)["tot"]
    N = G[2] + 1
    sig2 = np.append(sig, G[2])
    ii, jj = G[0], G[1]
    D = {g: np.full((N_SPECCHIO, 2), np.nan) for g in ("stella", "verso")}
    stato = {g: np.zeros(N_SPECCHIO, dtype=int) for g in ("stella", "verso")}     # ### 0 gira lo stesso lato, 1 nessun flip su entrambi, 2 diverso
    rov_g = np.zeros(N_SPECCHIO, dtype=int)                                       # ### il verso dell'arco GIRATO (stella): 1 rovesciato, 0 conservato, -1 nessun flip
    t0 = time.time()
    for q in range(N_SPECCHIO):
        a = int(archi[q])
        for g in ("stella", "verso"):
            RA, SA = regola(G, psi, phi, a, H0, g)
            RB, SB = regola(G, psiR, phiR, int(ap[a]), H0R, g)
            if RA["scelto"] < 0 and RB["scelto"] < 0:
                stato[g][q] = 1
            elif RA["scelto"] >= 0 and RB["scelto"] >= 0:
                xa, ya = RA["lati"][RA["scelto"]]
                xb, yb = RB["lati"][RB["scelto"]]
                stato[g][q] = 0 if {int(sig[xa]), int(sig[ya])} == {int(xb), int(yb)} else 2
            else:
                stato[g][q] = 2
            if stato[g][q] != 2:
                D[g][q] = CF.confronta(SA, SB, sig2, N)
            if g == "stella":
                if RA["scelto"] < 0:
                    rov_g[q] = -1
                else:
                    xa, ya = RA["lati"][RA["scelto"]]
                    rov_g[q] = int(rov[FS.arco_fra(ii, jj, xa, ya)])
        if q % 20 == 0:
            print("    %d su %d (%.0f s)" % (q, N_SPECCHIO, time.time() - t0))
            sys.stdout.flush()
    np.savez(os.path.join(DIR_O, "specchio.npz"), rov_a=rov[archi[:N_SPECCHIO]], rov_g=rov_g, p0=np.array(p0), **{"D_" + g: D[g] for g in D}, **{"stato_" + g: stato[g] for g in stato})
    print("### lo specchio: %.0f s" % (time.time() - t0))
    return 0


def referto():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "flip_di_stella.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    print("=" * 130)
    print("LA REGOLA INTERA: LA NASCITA DI STELLA, I QUATTRO FLIP, LA SCELTA (A) (Luca 2026-11-20 14:53); lo stato di C2 a k 3000 (dichiarato); la guardia %.0e |H|" % GUARDIA)
    print("=" * 130)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    esiti = []
    T = {}
    for p in sorted(x for x in os.listdir(DIR_O) if x.startswith("parte_")):
        with np.load(os.path.join(DIR_O, p)) as d:
            for k in ("scelto", "gap", "DH_nascita", "DH_flip"):
                T.setdefault(k, np.full(len(archi), np.nan))[d["sel"]] = d[k]
            print("### %s: %d archi, %.0f s" % (p, len(d["sel"]), float(d["tempo"])))
    sc = T["scelto"]
    pari = int(np.sum(sc < 0))
    print("### ### P-F3: il flip c'e' su %d nascite su %d (%.2f%%); il pari merito (nessun flip) %d; i lati scelti (i,k) (j,k) (j,l) (i,l): %s" % (
        int(np.sum(sc >= 0)), len(sc), 100.0 * np.sum(sc >= 0) / len(sc), pari, [int(np.sum(sc == c)) for c in range(4)]))
    g = T["gap"]
    print("    lo scarto fra il migliore e il secondo, in unita' di |H|: min %.3e, mediana %.3e, max %.3e; sotto 1e-12 %d, sotto 1e-10 %d, sotto 1e-8 %d" % (
        np.min(g), np.median(g), np.max(g), int(np.sum(g < 1e-12)), int(np.sum(g < 1e-10)), int(np.sum(g < 1e-8))))
    print("    DH della nascita: mediana %+.4e; DH del flip scelto: mediana %+.4e (min %+.4e, max %+.4e); E_persa per nascita (- la somma): mediana %+.4e" % (
        np.median(T["DH_nascita"]), np.median(T["DH_flip"]), np.min(T["DH_flip"]), np.max(T["DH_flip"]), -np.median(T["DH_nascita"] + T["DH_flip"])))
    print("    PER ANELLO (le mediane): ")
    for lo in range(10, 24, 2):
        s = (r >= lo) & (r < lo + 2)
        if s.any():
            print("      r %2d-%2d: %4d archi; il pari merito %3d; lo scarto %.3e; DH nascita %+.4e, flip %+.4e" % (lo, lo + 2, int(s.sum()), int(np.sum(sc[s] < 0)), np.median(g[s]), np.median(T["DH_nascita"][s]), np.median(T["DH_flip"][s])))
    esiti.append(("P-F3: il minimo unico (il flip c'e') su almeno il 90%% delle nascite (%.2f%%)" % (100.0 * np.sum(sc >= 0) / len(sc)), np.sum(sc >= 0) >= 0.9 * len(sc)))
    esiti.append(("P-F4: lo scarto mediano sopra 1e-8 |H| (%.3e)" % float(np.median(g)), float(np.median(g)) > 1e-8))
    print("-" * 130)
    with np.load(os.path.join(DIR_O, "specchio.npz")) as d:
        ra, rg = d["rov_a"].astype(bool), d["rov_g"]
        Ds, Dv, ss, sv = d["D_stella"], d["D_verso"], d["stato_stella"], d["stato_verso"]
        print("### P5 SULLA REGOLA INTERA (a 30 gradi per il nodo %s; %d archi)" % (tuple(int(v) for v in d["p0"]), len(ra)))
    for nome, Dx, sx in (("stella", Ds, ss), ("verso", Dv, sv)):
        print("    %-6s: lo stesso lato %d, nessun flip su entrambi %d, DIVERSO %d" % (nome, int(np.sum(sx == 0)), int(np.sum(sx == 1)), int(np.sum(sx == 2))))
        for cl, m in (("l'arco girato conservato", rg == 0), ("l'arco girato ROVESCIATO", rg == 1), ("nessun flip", rg == -1), ("l'arco diviso conservato", ~ra), ("l'arco diviso ROVESCIATO", ra)):
            X = Dx[m & (sx != 2)]
            if len(X):
                print("        %-26s %3d: psi max %.3e, phi max %.3e (sopra %.0e: %d)" % (cl, len(X), np.max(X[:, 0]), np.max(X[:, 1]), SOGLIA, int(np.sum(np.max(X, axis=1) > SOGLIA))))
    fallisce = bool(np.sum(sv == 2) > 0 or np.nanmax(Dv) > SOGLIA_DEVE_FALLIRE)
    print("    il caso che DEVE FALLIRE (la regola col flip col verso): DIVERSO %d, lo scarto massimo %.3e" % (int(np.sum(sv == 2)), float(np.nanmax(Dv))))
    esiti.append(("DEVE FALLIRE: la regola col flip col verso cade (o la prova non vale: FERMO)", fallisce))
    esiti.append(("P-F5: la regola intera simmetrica allo specchio su tutte le classi entro 1e-14 (lo stesso lato o nessun flip su entrambi)", bool(np.all(ss != 2)) and bool(np.nanmax(Ds) < SOGLIA)))
    esiti.append(("i pari merito: lo specchio da' nessun flip su ENTRAMBI i lati", bool(np.all(ss[rg == -1] == 1))))
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
    if sys.argv[1] == "specchio":
        sys.exit(specchio())
    sys.exit(referto())
