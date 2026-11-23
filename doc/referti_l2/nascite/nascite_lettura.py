# -*- coding: utf-8 -*-
r"""**[M1623-L] LA LETTURA DELLE 538 NASCITE DI MITOSI-v2** *(Luca, 2026-11-23; la carta `doc/CARTA_nascite_lettura.md`, le definizioni fissate PRIMA dei numeri; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/nascite/nascite_lettura.py > doc/referti_l2/nascite/nascite_538.txt

**Scrive anche** `doc/referti_l2/nascite/nascite_538.tsv` *(N1, una riga per nascita)*. **Le fonti:** `E:/soliton_simulator/controllo/mitosi_rami/` *(`TRONCO`, `MITOSI`, `MITOSI_V2`: le nascite, gli stati ogni `250` con lo sha1, le serie ogni `50`)*.
**L'ordine:** K1 *(i casi noti: le prime 9 contro M1-M3; la norma fuori dalle nascite)*, N1, N2 *(K2)*, N3 *(K5)*, N4 *(K3)*, N5 *(K4, e le distanze dalle nascite precedenti)*, N6.
"""
import contextlib
import glob
import io
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_SU = os.path.dirname(_QUI)
if _SU not in sys.path:
    sys.path.insert(0, _SU)
import coppie_57 as CP  # noqa: E402   (mette csv/ e csv/solitone/ sul percorso)

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_rami")
D_T, D_1, D_2 = (os.path.join(BASE, x) for x in ("TRONCO", "MITOSI", "MITOSI_V2"))
L = CP.L
ASSE = 10.0                     # ### «sull'asse»: entro 10 gradi (il criterio di P-M5)
FIN_ANELLO = 1000               # ### N3: finestre da 1000 tick
CUORE, GUSCIO = 10.0, 25.0      # ### N6: i confini del mandato (P6)
R_LONTANO = 60.0                # ### N6: phi0 dai mezzi archi coi due capi a r > 60 (la carta sez. 3)
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


# ------------------------------------------------------------------------------------------ le fonti
def nascite():
    B = json.load(open(os.path.join(D_1, "nascite_36250.json"), encoding="utf-8"))
    B2 = json.load(open(os.path.join(D_2, "nascite_45976.json"), encoding="utf-8"))
    assert len(B) == 9 and len(B2) == 529, (len(B), len(B2))
    return B + B2


def elenco_stati():
    out = [(35750, os.path.join(D_T, "stato_35750.npz"))]
    for d in (D_1, D_2):
        for f in sorted(glob.glob(os.path.join(d, "stato_*.npz"))):
            out.append((int(os.path.basename(f)[6:11]), f))
    out.sort()
    assert len(set(k for k, _ in out)) == len(out)
    return out


_CACHE = {}


def leggi(f):
    """### lo stato *(lo sha1 verificato)*: il grafo, le posizioni, `theta_a`, `psi_h`, `phi_h`, `meta`."""
    if f in _CACHE:
        return _CACHE[f]
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CP.sha1(f), "lo sha1 di %s NON coincide: FERMO" % f
    with np.load(f) as d:
        X = {x: d[x] for x in d.files if x in ("psi_h", "phi_h", "ii", "jj", "m1", "m2", "theta_a", "meta")}
    if "ii" not in X:
        X["ii"], X["jj"], X["m1"], X["m2"] = CP.toro()
    X["ii"], X["jj"] = X["ii"].astype(np.int64), X["jj"].astype(np.int64)
    X["n"] = len(X["m1"])
    X["meta"] = json.loads(str(X["meta"]))
    _CACHE.clear()
    _CACHE[f] = X
    return X


def theta_nodo(X):
    t = np.abs(X["theta_a"])
    return np.bincount(X["ii"], weights=t, minlength=X["n"]) + np.bincount(X["jj"], weights=t, minlength=X["n"])


def adiacenza(X):
    import scipy.sparse as sp
    ii, jj, n = X["ii"], X["jj"], X["n"]
    return sp.csr_matrix((np.ones(2 * len(ii)), (np.concatenate([ii, jj]), np.concatenate([jj, ii]))), shape=(n, n))


def vicini(A, insieme):
    s = np.asarray(sorted(insieme), dtype=np.int64)
    v = np.unique(A[s].indices)
    return np.setdiff1d(v, s)


# ------------------------------------------------------------------------------------------ l'angolo: una funzione MIA (K1 la confronta con coppie_57)
def angolo_mio(m1, m2, nodi, da):
    """### l'angolo attorno al nodo `da`: lo scarto per indice riportato in `[-L/2, L/2)`, in coordinate coi vettori del favo, l'immagine piu' corta fra le nove scritta a mano."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    d1 = ((np.asarray(m1)[nodi] - m1[da] + 0.5 * L) % L) - 0.5 * L
    d2 = ((np.asarray(m2)[nodi] - m2[da] + 0.5 * L) % L) - 0.5 * L
    ang = np.empty(len(nodi))
    rr = np.empty(len(nodi))
    for q in range(len(nodi)):
        x0 = d1[q] * A1 + d2[q] * A2
        best, bd = None, None
        for k1 in (-1, 0, 1):
            for k2 in (-1, 0, 1):
                y = x0 + L * (k1 * A1 + k2 * A2)
                dd = float(np.sum(y ** 2))
                if bd is None or dd < bd:
                    best, bd = y, dd
        ang[q] = np.degrees(np.arctan2(best[1], best[0])) % 360.0
        rr[q] = np.hypot(best[0], best[1])
    return ang, rr


def dall_asse(a):
    x = np.mod(a, 60.0)
    return np.minimum(x, 60.0 - x)


# ------------------------------------------------------------------------------------------ K1
def k1():
    print("K1 I CASI NOTI: le prime 9 nascite contro M1-M3 (MITOSI/stato_36250, raggruppamento_nascite.py e coppie_57.py)")
    S = CP.stato(os.path.join(D_1, "stato_36250.npz"))
    B9 = json.load(open(os.path.join(D_1, "nascite_36250.json"), encoding="utf-8"))
    nati = np.array([b["nodi"]["n"] for b in B9], dtype=np.int64)
    a_loro, r_loro = CP.angolo_e_r(S, nati, S["sorgente"])
    a_mio, r_mio = angolo_mio(S["m1"], S["m2"], nati, S["sorgente"])
    print("    gli angoli (M3): %s" % ", ".join("%.2f" % v for v in a_loro))
    print("    i miei:          %s; lo scarto massimo %.3e gradi, in r %.3e" % (", ".join("%.2f" % v for v in a_mio), float(np.max(np.abs(a_mio - a_loro))), float(np.max(np.abs(r_mio - r_loro)))))
    esito("K1 gli angoli delle prime 9: la mia funzione = coppie_57.angolo_e_r AL BIT", np.array_equal(a_mio, a_loro) and np.array_equal(r_mio, r_loro))
    esito("K1 le prime 9 tutte entro %.0f gradi da un asse (M3: il massimo 7.79)" % ASSE, float(np.max(dall_asse(a_mio))) <= ASSE, "il massimo %.2f" % float(np.max(dall_asse(a_mio))))
    with contextlib.redirect_stdout(io.StringIO()):
        out = CP.misura(S, "k 36250")
    X = leggi(os.path.join(D_1, "stato_36250.npz"))
    g = np.bincount(np.concatenate([X["ii"], X["jj"]]), minlength=X["n"])
    c5, c7 = np.nonzero(g == 5)[0], np.nonzero(g == 7)[0]
    A = adiacenza(X)
    legati = sum(1 for v in c5 if np.intersect1d(A[v].indices, c7).size > 0)
    print("    i gradi a k 36250: miei %d cinque, %d sette, %d cinque legati a un 7; coppie_57: %d, %d, passi %s" % (c5.size, c7.size, legati, out["cinque"], out["sette"], [c["passi"] for c in out["coppie"]]))
    esito("K1 le coppie a k 36250: 8 cinque e 8 sette, ognuno legato (M1, P-M2), e = coppie_57", c5.size == out["cinque"] == 8 and c7.size == out["sette"] == 8 and legati == 8 and all(c["passi"] == 1 for c in out["coppie"]))


# ------------------------------------------------------------------------------------------ N1, N2
def n1_n2(B):
    print("N1 LA LISTA E N2 GLI ASSI (lo stato finale MITOSI_V2/stato_45976: la sorgente, le posizioni):")
    S = CP.stato(os.path.join(D_2, "stato_45976.npz"))
    nati = np.array([b["nodi"]["n"] for b in B], dtype=np.int64)
    ang, rr = angolo_mio(S["m1"], S["m2"], nati, S["sorgente"])
    da = dall_asse(ang)
    sull = da <= ASSE
    N, k_on = len(B), int(sull.sum())
    from scipy.stats import binom
    p_unif = float(binom.sf(k_on - 1, N, 1.0 / 3.0))
    orig = np.arange(L * L)
    rmin, rmax = float(S["r"][nati].min()), float(S["r"][nati].max())
    an = orig[(S["r"][orig] >= rmin) & (S["r"][orig] <= rmax)]
    a_an, _ = angolo_mio(S["m1"], S["m2"], an, S["sorgente"])
    f_an = float(np.mean(dall_asse(a_an) <= ASSE))
    p_an = float(binom.sf(k_on - 1, N, f_an))
    f9 = float(np.mean(sull[:9]))
    print("    la sorgente %d; r dei nati (dal centro della materia a k 45976) da %.3f a %.3f" % (S["sorgente"], rmin, rmax))
    print("    sull'asse (entro %.0f gradi): %d su %d = %.4f; le prime 9 (nello stato finale) %.4f; la distanza media dall'asse %.3f gradi, la mediana %.3f, il massimo %.3f" % (
        ASSE, k_on, N, k_on / N, f9, float(np.mean(da)), float(np.median(da)), float(np.max(da))))
    print("    il nullo uniforme 1/3: p = %.3e; il nullo dell'anello (%d nodi originari con r in [%.3f, %.3f], la loro frazione sull'asse %.4f): p = %.3e" % (p_unif, an.size, rmin, rmax, f_an, p_an))
    for nome, sel in (("1-100", slice(0, 100)), ("101-300", slice(100, 300)), ("301-538", slice(300, N))):
        print("    le nascite %s: sull'asse %.4f" % (nome, float(np.mean(sull[sel]))))
    fr = k_on / N
    zona = "IMPRONTA DEL FAVO" if (fr > 0.9 and p_unif < 1e-4) else ("SI SFUMA" if fr < 0.7 else "FRA 0.7 E 0.9")
    print("    K2: %s" % zona)
    return {"ang": ang, "da": da, "sull": sull, "r_fin": S["r"][nati], "S": S, "nati": nati, "fr": fr, "zona": zona, "f_an": f_an}


# ------------------------------------------------------------------------------------------ N3
def n3(B):
    from scipy.optimize import minimize
    print("N3 IL RITMO: le nascite per %d tick da k %d" % (FIN_ANELLO, B[0]["k"]))
    ks = np.array([b["k"] for b in B])
    k0 = int(ks[0])
    bordi = k0 + FIN_ANELLO * np.arange(11)
    cnt = np.histogram(ks, bins=bordi)[0].astype(float)
    t = np.arange(10) + 0.5
    print("    i conteggi: %s (in tutto %d; fuori dalle finestre %d)" % (", ".join("%d" % c for c in cnt), int(cnt.sum()), len(ks) - int(cnt.sum())))
    print("    i nodi: %s" % ", ".join("%d" % (L * L + int(np.sum(ks < b))) for b in bordi))

    def nll(lam):
        return float(np.sum(lam - cnt * np.log(lam)))
    lc = float(cnt.mean())
    r_lin = minimize(lambda p: nll(np.maximum(p[0] + p[1] * t, 1e-12)), [lc, 0.0], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
    r_exp = minimize(lambda p: nll(np.exp(p[0] + p[1] * t)), [math.log(lc), 0.0], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
    M = {"costante": (np.full(10, lc), 1, None), "lineare": (r_lin.x[0] + r_lin.x[1] * t, 2, r_lin.x), "esponenziale": (np.exp(r_exp.x[0] + r_exp.x[1] * t), 2, r_exp.x)}
    best = None
    for nome, (lam, p, x) in M.items():
        aic = 2 * p + 2 * nll(lam)
        chi2 = float(np.sum((cnt - lam) ** 2 / lam))
        extra = ""
        if nome == "lineare":
            I = np.array([[np.sum(1 / lam), np.sum(t / lam)], [np.sum(t / lam), np.sum(t * t / lam)]])
            s = math.sqrt(np.linalg.inv(I)[1, 1])
            extra = "a %.3f, b %+.3f +- %.3f per finestra (%.1f sigma)" % (x[0], x[1], s, x[1] / s)
            M[nome] = (lam, p, x, x[1], s)
        elif nome == "esponenziale":
            I = np.array([[np.sum(lam), np.sum(t * lam)], [np.sum(t * lam), np.sum(t * t * lam)]])
            s = math.sqrt(np.linalg.inv(I)[1, 1])
            extra = "A %.3f, c %+.4f +- %.4f per finestra (%.1f sigma)" % (math.exp(x[0]), x[1], s, x[1] / s)
            M[nome] = (lam, p, x, x[1], s)
        else:
            M[nome] = (lam, p, x, 0.0, 0.0)
        print("    %-12s AIC %.3f; chi2 di Pearson %.3f su %d gradi; %s" % (nome, aic, chi2, 10 - p, extra))
        if best is None or aic < best[1]:
            best = (nome, aic)
    _lam, _p, _x, pend, s = M[best[0]]
    verdetto = "COSTANTE" if best[0] == "costante" or abs(pend) <= 2 * s else ("ACCELERA" if pend > 0 else "RALLENTA")
    print("    K5: il migliore (AIC) %s: %s" % (best[0], verdetto))
    return verdetto


# ------------------------------------------------------------------------------------------ N4
def serie_tutte():
    K, Mv, Dn = [], [], []
    for d in (D_T, D_1, D_2):
        for f in sorted(glob.glob(os.path.join(d, "serie_*.npz"))):
            with np.load(f) as z:
                if "D_n" not in z.files:
                    continue
                K += list(z["k"])
                Mv += list(z["M"])
                Dn += list(z["D_n"])
    K, Mv, Dn = np.array(K), np.array(Mv), np.array(Dn)
    o = np.argsort(K, kind="stable")
    K, Mv, Dn = K[o], Mv[o], Dn[o]
    u = np.concatenate([[True], np.diff(K) > 0])
    return K[u], Mv[u], Dn[u]


def n4(B, stati):
    print("N4 Z3: LA NORMA (la serie ogni 50 tick: M = somma |psi_h|^2, D_n le nascite fatte; phi dagli stati ogni 250)")
    K, Mv, Dn = serie_tutte()
    sel = (K >= 35500)
    K, Mv, Dn = K[sel], Mv[sel], Dn[sel]
    dM = np.abs(Mv[1:] / Mv[:-1] - 1.0)
    nb = np.diff(Dn)
    con, senza = nb > 0, nb == 0
    print("    %d intervalli da k %d a %d; con nascite %d (le nascite dentro %d), senza %d" % (len(dM), K[0], K[-1], int(con.sum()), int(nb[con].sum()), int(senza.sum())))
    print("    |dM/M| per intervallo: CON nascite il massimo %.3e (la mediana %.3e); SENZA il massimo %.3e (la mediana %.3e)" % (
        float(dM[con].max()), float(np.median(dM[con])), float(dM[senza].max()) if senza.any() else float("nan"), float(np.median(dM[senza])) if senza.any() else float("nan")))
    sg = np.sign(Mv[1:] - Mv[:-1])[con]
    print("    il segno di dM negli intervalli con nascite: + %d, - %d, 0 %d; M da %.15e a %.15e (relativo %.3e)" % (int((sg > 0).sum()), int((sg < 0).sum()), int((sg == 0).sum()), Mv[0], Mv[-1], abs(Mv[-1] / Mv[0] - 1)))
    esito("K1 la norma fuori dalle nascite: |dM/M| < 1e-12 in ogni intervallo di 50 tick senza nascite", senza.any() and float(dM[senza].max()) < 1e-12, "%.3e" % float(dM[senza].max()))
    k3 = float(dM[con].max()) < 1e-10
    print("    K3: %s" % ("CONSERVATA" if k3 else "NON CONSERVATA, il massimo %.3e" % float(dM[con].max())))
    P = []
    for k, f in stati:
        if k < 36000:
            continue
        X = leggi(f)
        P.append((k, float(np.sum(np.abs(X["phi_h"]) ** 2)), int(X["meta"]["nascite"]), float(np.sum(np.abs(X["psi_h"]) ** 2))))
    dp = [abs(P[q + 1][1] / P[q][1] - 1.0) for q in range(len(P) - 1)]
    print("    phi (gli stati da k 36000, %d intervalli da 250): |d somma phi^2 / somma phi^2| il massimo %.3e, la mediana %.3e" % (len(dp), max(dp), float(np.median(dp))))
    DH = np.array([b["DH"] for b in B])
    print("    L'ENERGIA (dai bilanci, non dalla norma): DH per nascita la media %+.4e, da %+.4e a %+.4e; la somma %+.6e; E_persa all'ultima %+.6e" % (
        float(DH.mean()), float(DH.min()), float(DH.max()), float(DH.sum()), B[-1]["E_persa"]))
    print("    P9 il massimo %.3e; il residuo di Gauss il massimo %.3e; F3 vero in %d su %d" % (max(b["P9"] for b in B), max(b["res"] for b in B), sum(1 for b in B if b.get("F3", True)), len(B)))
    return "CONSERVATA" if k3 else "NON CONSERVATA"


# ------------------------------------------------------------------------------------------ N5 e N1
def n5(B, stati, N2):
    print("N5 B1/Z4: THETA ATTORNO AL NATO (Theta_v = somma |theta_a| sugli archi del nodo; prima = lo stato con k < k nascita, dopo = il primo con k >= k nascita)")
    ks_st = np.array([k for k, _ in stati])
    righe = []
    finestre = {}
    for q, b in enumerate(B):
        jp = int(np.nonzero(ks_st < b["k"])[0][-1])
        jd = int(np.nonzero(ks_st >= b["k"])[0][0])
        finestre.setdefault((jp, jd), []).append(q)
    G_prima, G_dopo, V1p, V1d, V2p, V2d, C_rap, coppie, gradi6, saltate = [], [], [], [], [], [], [], {}, {}, []
    for (jp, jd), qs in sorted(finestre.items()):
        Xp = leggi(stati[jp][1])
        Tp, np_ = theta_nodo(Xp), Xp["n"]
        Xd = leggi(stati[jd][1])
        Td = theta_nodo(Xd)
        A = adiacenza(Xd)
        g = np.bincount(np.concatenate([Xd["ii"], Xd["jj"]]), minlength=Xd["n"])
        from scipy.sparse import csgraph
        nati_f = np.array([B[q]["nodi"]["n"] for q in qs], dtype=np.int64)
        dist = csgraph.dijkstra(A, unweighted=True, indices=nati_f, limit=3.5, min_only=True)
        rf = N2["S"]["r"]
        rmin, rmax = float(rf[N2["nati"]].min()), float(rf[N2["nati"]].max())
        ctrl = np.nonzero(np.isinf(dist[:np_]) & (np.arange(np_) < L * L) & (rf[:np_] >= rmin) & (rf[:np_] <= rmax))[0]
        cr = float(np.mean(Td[ctrl]) / np.mean(Tp[ctrl])) if ctrl.size else float("nan")
        for q in qs:
            b = B[q]
            nd = b["nodi"]
            i, j, n = nd["i"], nd["j"], nd["n"]
            sei = [nd[x] for x in ("i", "j", "k", "l", "n", "m")]
            c5 = [v for v in sei if g[v] == 5]
            c7 = [v for v in sei if g[v] == 7]
            leg = any(np.intersect1d(A[v].indices, c7).size > 0 for v in c5)
            coppie[q] = "5-7" if leg else "altro"
            gradi6[q] = [int(g[v]) for v in sei]
            if max(i, j) >= np_:
                saltate.append(q)
                continue
            G_prima.append(float(np.mean(Tp[[i, j]])))
            G_dopo.append(float(np.mean(Td[[i, j, n]])))
            v1 = vicini(A, {i, j, n})
            v2 = np.setdiff1d(vicini(A, set(v1.tolist()) | {i, j, n}), v1)
            v1o, v2o = v1[v1 < np_], v2[v2 < np_]
            V1p.append(float(np.mean(Tp[v1o])))
            V1d.append(float(np.mean(Td[v1o])))
            V2p.append(float(np.mean(Tp[v2o])))
            V2d.append(float(np.mean(Td[v2o])))
            C_rap.append(cr)
            righe.append(q)
    G_prima, G_dopo, V1p, V1d, V2p, V2d, C_rap = (np.array(x) for x in (G_prima, G_dopo, V1p, V1d, V2p, V2d, C_rap))
    rg = float(G_dopo.mean() / G_prima.mean())
    r1, r2, rc = float(V1d.mean() / V1p.mean()), float(V2d.mean() / V2p.mean()), float(np.nanmean(C_rap))
    print("    %d nascite in %d finestre (saltate %d: il genitore nato nella stessa finestra, non esiste nello stato prima); Theta medio (rad, somma sugli archi del nodo):" % (len(righe), len(finestre), len(saltate)))
    print("      genitore+nato: prima %.4f, dopo %.4f: il rapporto %.4f" % (G_prima.mean(), G_dopo.mean(), rg))
    print("      i vicini a 1 passo: prima %.4f, dopo %.4f: il rapporto %.4f" % (V1p.mean(), V1d.mean(), r1))
    print("      i vicini a 2 passi: prima %.4f, dopo %.4f: il rapporto %.4f" % (V2p.mean(), V2d.mean(), r2))
    print("      il controllo (l'anello delle nascite, a piu' di 3 passi da ogni nascita della finestra): il rapporto medio %.4f" % rc)
    print("      i rapporti diviso il controllo: genitore+nato %.4f, vicini 1 %.4f, vicini 2 %.4f" % (rg / rc, r1 / rc, r2 / rc))
    q50 = np.percentile(V1d / V1p, [10, 50, 90])
    print("      la distribuzione per nascita, vicini 1 dopo/prima: il 10%% %.3f, la mediana %.3f, il 90%%  %.3f; genitore+nato: %s" % (q50[0], q50[1], q50[2], ", ".join("%.3f" % v for v in np.percentile(G_dopo / G_prima, [10, 50, 90]))))
    k4 = "CHIUDE" if (rg < 0.5 and r1 <= 1.2) else ("SI SPOSTA" if r1 > 1.2 else "RESTA")
    print("    K4 (il criterio del mandato, sui rapporti grezzi): %s" % k4)
    print("    LE NASCITE CHE SI TOCCANO (il grafo finale): la distanza in passi dalla nascita precedente piu' vicina, e il tempo dalla precedente")
    from scipy.sparse import csgraph
    Xf = leggi(os.path.join(D_2, "stato_45976.npz"))
    Af = adiacenza(Xf)
    nati = np.array([b["nodi"]["n"] for b in B], dtype=np.int64)
    Dm = csgraph.dijkstra(Af, unweighted=True, indices=nati)[:, nati]
    dmin = np.array([int(np.min(Dm[j, :j])) for j in range(1, len(nati))])
    kk = np.array([b["k"] for b in B])
    print("      %d nascite: a 1 passo %.4f, a <= 2 %.4f, a <= 3 %.4f; la media %.3f, la mediana %d, il massimo %d; le prime 9 (M2): %s" % (
        dmin.size, float(np.mean(dmin == 1)), float(np.mean(dmin <= 2)), float(np.mean(dmin <= 3)), float(dmin.mean()), int(np.median(dmin)), int(dmin.max()), list(dmin[:8])))
    print("      il tempo dalla nascita precedente: la mediana %d tick, il 10%% %d, il 90%% %d" % (int(np.median(np.diff(kk))), int(np.percentile(np.diff(kk), 10)), int(np.percentile(np.diff(kk), 90))))
    nc = sum(1 for v in coppie.values() if v == "5-7")
    print("    N1 la coppia (i gradi dei sei nodi nello stato dopo): 5-7 %d, altro %d" % (nc, len(coppie) - nc))
    return {"coppie": coppie, "gradi": gradi6, "k4": k4, "dmin": dmin}


# ------------------------------------------------------------------------------------------ N6
def n6(B, N2):
    print("N6 DOVE: r registrato (dal centro fisso della corsa) e il profilo dello stato finale")
    r = np.array([b["r"] for b in B])
    print("    il cuore r < %.0f: %d; il guscio [%.0f, %.0f): %d (%.4f); oltre: %d; r da %.3f a %.3f, la mediana %.3f" % (
        CUORE, int((r < CUORE).sum()), CUORE, GUSCIO, int(((r >= CUORE) & (r < GUSCIO)).sum()), float(np.mean((r >= CUORE) & (r < GUSCIO))), int((r >= GUSCIO).sum()), r.min(), r.max(), float(np.median(r))))
    pas = np.array([b["passi"] for b in B])
    print("    i passi dalla sorgente: da %d a %d, la mediana %d" % (pas.min(), pas.max(), int(np.median(pas))))
    S = N2["S"]
    X = leggi(os.path.join(D_2, "stato_45976.npz"))
    nodo = np.empty(2 * len(X["ii"]), dtype=np.int64)
    nodo[0::2], nodo[1::2] = X["ii"], X["jj"]
    rh = S["r"][nodo]
    lont = (S["r"][X["ii"]] > R_LONTANO) & (S["r"][X["jj"]] > R_LONTANO)
    lh = np.repeat(lont, 2)
    phi = X["phi_h"]
    phi0 = phi[lh].mean(axis=0)
    dphi = np.abs(phi - phi0) ** 2
    if dphi.ndim > 1:
        dphi = dphi.sum(axis=1)
    dn = np.bincount(nodo, weights=dphi, minlength=X["n"]) / np.maximum(np.bincount(nodo, minlength=X["n"]), 1)
    rho = S["rho"]
    anelli = np.arange(0, 41)
    print("    il profilo per anello (r intero, lo stato finale; le nascite dal r ricalcolato col centro della materia finale):")
    rn = N2["r_fin"]
    for a in anelli:
        m = (S["r"] >= a) & (S["r"] < a + 1)
        nb = int(np.sum((rn >= a) & (rn < a + 1)))
        if m.any():
            print("      r %2d: rho %.4e, |phi - phi0|^2 %.4e, le nascite %d" % (a, float(rho[m].mean()), float(dn[m].mean()), nb))
    return float(np.mean((r >= CUORE) & (r < GUSCIO)))


def main():
    import _presidio
    _presidio.avvia(os.path.join(_SU, "coppie_57.py"))
    _presidio.avvia(__file__)
    print("=" * 140)
    print("[M1623-L] LE 538 NASCITE DI MITOSI-v2: LA LETTURA (la carta doc/CARTA_nascite_lettura.md; sola lettura)")
    print("### «prima» e «dopo» hanno la risoluzione dei dati: 50 tick la norma, 250 Theta e il grafo. K3 e la parte «scende» di K4 sono GARANTITE dal codice (la carta sez. 2).")
    print("=" * 140)
    B = nascite()
    stati = elenco_stati()
    print("### %d nascite (9 + 529), da k %d a k %d; %d stati da k %d a k %d" % (len(B), B[0]["k"], B[-1]["k"], len(stati), stati[0][0], stati[-1][0]))
    k1()
    if any(v is False for v in OK.values()):
        print("### K1 CADE: FERMO")
        return 1
    print("-" * 140)
    N2 = n1_n2(B)
    print("-" * 140)
    v3 = n3(B)
    print("-" * 140)
    v4 = n4(B, stati)
    print("-" * 140)
    N5 = n5(B, stati, N2)
    print("-" * 140)
    g6 = n6(B, N2)
    f = os.path.join(_QUI, "nascite_538.tsv")
    righe = ["q\tk\tarco\ti\tj\tn\tr\tpassi\tangolo\tdall_asse\tsull_asse\tcoppia\tgradi_i_j_k_l_n_m"]
    for q, b in enumerate(B):
        nd = b["nodi"]
        righe.append("%d\t%d\t%d\t%d\t%d\t%d\t%.6f\t%d\t%.4f\t%.4f\t%d\t%s\t%s" % (q + 1, b["k"], b["a"], nd["i"], nd["j"], nd["n"], b["r"], b["passi"], N2["ang"][q], N2["da"][q], int(N2["sull"][q]), N5["coppie"][q], ",".join(str(x) for x in N5["gradi"][q])))
    s = "\n".join(righe) + "\n"
    open(f, "w", encoding="utf-8", newline="").write(s)
    print("=" * 140)
    print("### IL RIASSUNTO: K2 %s (sull'asse %.4f); K3 %s; K4 %s; K5 %s; il guscio %.4f; N1 in %s" % (N2["zona"], N2["fr"], v4, N5["k4"], v3, g6, os.path.basename(f)))
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0


if __name__ == "__main__":
    sys.exit(main())
