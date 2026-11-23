# -*- coding: utf-8 -*-
r"""**[M1739-E] IL PREZZO DELLO SPAZIO: L'ENERGIA PERSA ALLE 538 NASCITE** *(Luca, 2026-11-23; la carta `doc/CARTA_prezzo_spazio.md`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/nascite/prezzo_spazio.py > doc/referti_l2/nascite/prezzo_spazio.txt

**Le funzioni di lettura di `nascite_lettura.py`** *(le nascite, gli stati con lo sha1, `theta_nodo`)*. Per nascita: `DH`, `DH_nascita`, `DH_flip`; **sui genitori** `i, j` nello stato salvato PRIMA: `Theta_v`, `Lambda`, `rho`, `|phi - phi0|^2` *(`phi0` dai mezzi archi coi due capi a `r > 60`)*. **Il caso noto:** `somma DH` contro la deriva di `E` della serie, e con la deriva dei tick del tronco *(`k 30000-35750`)* tolta.
"""
import glob
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import nascite_lettura as NL  # noqa: E402

R_LONTANO = 60.0
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def retta(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    A = np.vstack([np.ones_like(x), x]).T
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - A @ c
    s2 = float(np.sum(r ** 2) / (len(x) - 2))
    cov = s2 * np.linalg.inv(A.T @ A)
    rr = float(np.corrcoef(x, y)[0, 1])
    return float(c[0]), float(c[1]), math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1]), rr


def genitori(B, stati):
    from solitone import toro as TO
    ks_st = np.array([k for k, _ in stati])
    TH, LA, RHO, DPHI, DK = [], [], [], [], []
    cache = {}
    for b in B:
        jp = int(np.nonzero(ks_st < b["k"])[0][-1])
        if jp not in cache:
            X = NL.leggi(stati[jp][1])
            n = X["n"]
            T = NL.theta_nodo(X)
            nodo = np.empty(2 * len(X["ii"]), dtype=np.int64)
            nodo[0::2], nodo[1::2] = X["ii"], X["jj"]
            rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
            with np.load(stati[jp][1]) as d:
                lam = np.asarray(d["Lambda"], float)
            c = TO.centro(rho, X["m1"], X["m2"], NL.L)[:2]
            r = np.hypot(*TO.scarti(X["m1"], X["m2"], c[0], c[1], NL.L).T[:2])
            lont = np.repeat((r[X["ii"]] > R_LONTANO) & (r[X["jj"]] > R_LONTANO), 2)
            phi = X["phi_h"]
            dph = np.abs(phi - phi[lont].mean(axis=0)) ** 2
            if dph.ndim > 1:
                dph = dph.sum(axis=1)
            dn = np.bincount(nodo, weights=dph, minlength=n) / np.maximum(np.bincount(nodo, minlength=n), 1)
            cache.clear()
            cache[jp] = (T, lam, rho, dn, n, stati[jp][0])
        T, lam, rho, dn, n, kp = cache[jp]
        i, j = b["nodi"]["i"], b["nodi"]["j"]
        DK.append(b["k"] - kp)
        if max(i, j) >= n:
            TH.append(np.nan)
            LA.append(np.nan)
            RHO.append(np.nan)
            DPHI.append(np.nan)
            continue
        TH.append(float(np.mean(T[[i, j]])))
        LA.append(float(np.mean(lam[[i, j]])))
        RHO.append(float(np.mean(rho[[i, j]])))
        DPHI.append(float(np.mean(dn[[i, j]])))
    return tuple(np.array(x) for x in (TH, LA, RHO, DPHI, DK))


def serie_E():
    K, E, Dn = [], [], []
    for d in (NL.D_T, NL.D_1, NL.D_2):
        for f in sorted(glob.glob(os.path.join(d, "serie_*.npz"))):
            with np.load(f) as z:
                if "D_n" not in z.files:
                    continue
                K += list(z["k"])
                E += list(z["E"])
                Dn += list(z["D_n"])
    K, E, Dn = np.array(K), np.array(E), np.array(Dn)
    o = np.argsort(K, kind="stable")
    K, E, Dn = K[o], E[o], Dn[o]
    u = np.concatenate([[True], np.diff(K) > 0])
    return K[u], E[u], Dn[u]


def main():
    import _presidio
    _presidio.avvia(os.path.join(NL._SU, "coppie_57.py"))
    _presidio.avvia(os.path.join(_QUI, "nascite_lettura.py"))
    _presidio.avvia(__file__)
    print("=" * 140)
    print("[M1739-E] IL PREZZO DELLO SPAZIO (la carta doc/CARTA_prezzo_spazio.md; sola lettura). ### L'energia PER PEZZI al tick della nascita NON E' NEI DATI (una ripresa): NON MISURATO")
    print("=" * 140)
    B = NL.nascite()
    stati = NL.elenco_stati()
    DH = np.array([b["DH"] for b in B])
    DHn = np.array([b["DH_nascita"] for b in B])
    DHf = np.array([b["DH_flip"] for b in B])
    print("(1) %d nascite; DH: la media %+.4f, la deviazione %.4f, la mediana %+.4f, da %+.4f a %+.4f; la somma %+.6f; E_persa all'ultima %+.6f" % (
        len(B), DH.mean(), DH.std(ddof=1), float(np.median(DH)), DH.min(), DH.max(), DH.sum(), B[-1]["E_persa"]))
    print("    la scomposizione della regola: DH_nascita la media %+.4f (da %+.4f a %+.4f), DH_flip la media %+.4f (da %+.4f a %+.4f); |DH - DH_nascita - DH_flip| massimo %.3e" % (
        DHn.mean(), DHn.min(), DHn.max(), DHf.mean(), DHf.min(), DHf.max(), float(np.max(np.abs(DH - DHn - DHf)))))
    m = float(DH.mean())
    print("    |DH/media - 1| <= 0.3 (entro +-30%% di una costante) in %.4f delle nascite; la deviazione relativa %.4f" % (float(np.mean(np.abs(DH / m - 1.0) <= 0.3)), DH.std(ddof=1) / abs(m)))
    print("    per terzi della corsa: %s" % "; ".join("%d-%d: la media %+.3f" % (a + 1, b, float(DH[a:b].mean())) for a, b in ((0, 179), (179, 358), (358, len(DH)))))
    print("(3) IL SEGNO: DH > 0 in %d su %d (%.4f)" % (int((DH > 0).sum()), len(DH), float(np.mean(DH > 0))))
    TH, LA, RHO, DPHI, DK = genitori(B, stati)
    ok = np.isfinite(TH)
    print("### i genitori (i, j) nello stato salvato prima (%d nascite; saltate %d: un genitore nato nella stessa finestra); i tick dallo stato: la mediana %d, il massimo %d" % (
        int(ok.sum()), int((~ok).sum()), int(np.median(DK)), int(DK.max())))
    print("    Theta_v la media %.4f (da %.4f a %.4f); Lambda la media %.6f (da %.6f a %.6f); rho la media %.4f (da %.4f a %.4f); |phi - phi0|^2 la media %.4f" % (
        np.nanmean(TH), np.nanmin(TH), np.nanmax(TH), np.nanmean(LA), np.nanmin(LA), np.nanmax(LA), np.nanmean(RHO), np.nanmin(RHO), np.nanmax(RHO), np.nanmean(DPHI)))
    for nome, x in (("Lambda", LA), ("rho", RHO), ("|phi - phi0|^2", DPHI), ("Theta_v", TH)):
        a, b_, sa, sb, rr = retta(x[ok], DH[ok])
        print("    (%s) DH = a + b %s: a %+.4f +- %.4f, b %+.6e +- %.1e (%.1f sigma); la correlazione %+.4f" % ("2" if nome == "Theta_v" else "1", nome, a, sa, b_, sb, b_ / sb if sb > 0 else float("nan"), rr))
    q = DH[ok] / LA[ok]
    print("    DH/Lambda: la media %+.4f, la deviazione relativa %.4f; entro +-30%% della media in %.4f" % (float(q.mean()), float(q.std(ddof=1) / abs(q.mean())), float(np.mean(np.abs(q / q.mean() - 1) <= 0.3))))
    K, E, Dn = serie_E()
    i0 = int(np.nonzero(K < B[0]["k"])[0][-1])
    i1 = len(K) - 1
    dE = float(E[i1] - E[i0])
    print("### IL CASO NOTO: E (la serie) da k %d (%.6f, nascite %d) a k %d (%.6f, nascite %d): la deriva %+.6f; la somma dei DH %+.6f; lo scarto %+.6e (relativo a E %.2e)" % (
        K[i0], E[i0], Dn[i0], K[i1], E[i1], Dn[i1], dE, DH.sum(), dE - DH.sum(), abs(dE - DH.sum()) / abs(E[i0])))
    esito("il caso noto: la somma dei 538 DH = la deriva di E della corsa entro 1e-9", abs(dE - DH.sum()) <= 1e-9, "%+.3e" % (dE - DH.sum()))
    t = (K >= 30000) & (K <= 35750)
    p = np.polyfit(K[t], E[t], 1)
    corr = dE - p[0] * (K[i1] - K[i0])
    print("    la deriva dei tick dal tronco (k 30000-35750, senza nascite): %+.6e per tick; tolta su %d tick: %+.6f; contro la somma dei DH: lo scarto %+.4f (%.2f%%)" % (
        p[0], K[i1] - K[i0], corr, corr - DH.sum(), 100 * (corr - DH.sum()) / DH.sum()))
    sen = np.nonzero(np.diff(Dn) == 0)[0]
    sen = sen[K[sen] >= K[i0]]
    if sen.size:
        r_sen = (E[sen + 1] - E[sen]) / (K[sen + 1] - K[sen])
        print("    la deriva per tick negli intervalli di 50 tick SENZA nascite dopo la prima (%d): la media %+.4e, la mediana %+.4e" % (sen.size, float(r_sen.mean()), float(np.median(r_sen))))
    print("=" * 140)
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0


if __name__ == "__main__":
    sys.exit(main())
