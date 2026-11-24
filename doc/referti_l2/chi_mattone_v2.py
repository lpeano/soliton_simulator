# -*- coding: utf-8 -*-
r"""**LA PARTE C ALLUNGATA: IL MATTONE DI C2 COL CAMPO CHI DA `k 3000` A `k 20000`** *(la decisione di Luca `2026-11-21` `19:28`; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `13`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_mattone_v2.py prova > doc/referti_l2/chi_mattone_ripresa.txt
    E:\python\py3132\python.exe doc/referti_l2/chi_mattone_v2.py corsa --da 3000 --fino 20000 --registro chi-mattone-lungo
    E:\python\py3132\python.exe doc/referti_l2/chi_mattone_v2.py referto > doc/referti_l2/chi_mattone_v2.txt

**`chi_mattone.py` e' usato e non si riscrive:** questo file ne riprende il cammino *(`corsa`)* con **la ripresa da uno stato** *(`controllo_senza_bordo.riprendi` piu' `chi`, `pi`, `theta_a`; i parametri RICALCOLATI e asseriti al bit su quelli del `meta`)*, e ne usa le costanti e le funzioni *(`DIR`, `OGNI`, `ANELLI`, `sha1`, `anello`)*.
**`prova`** *(sez. `13.2`)*: da `stato_02750` a `k 3000` in `E:/soliton_simulator/controllo/CHI/prova_ripresa/`: DEVE lo stato a `k 3000` al bit con `stato_03000` e le serie `2800`-`3000` al bit; DEVE FALLIRE con `pi = 0` alla ripresa *(le serie a `k 2800` diverse)*.
**`referto`** *(sez. `13.3`)*: gli estremi locali di `w` *(stretti su `+-5` misure)*, P-X11, P-X12, P-X13, la lettura; la figura `chi_mattone_v2.png` *(`w`, la massa entro `12.4`, il picco contro `k`, con `chi` e C2 fino a `k 3000`)*.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT
import chi_mattone as CM

DIR = CM.DIR
DIR_PROVA = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "prova_ripresa")
CHIAVI_P = ("kappa", "c0", "c2", "m2", "e0", "s")
FINESTRA = 5


def corsa(k_da, k_fino, reg, d_out, pi_zero=False, d_in=DIR):
    """### dalla `stato_<k_da>` di `d_in` fino a `k_fino`; gli stati e le serie in `d_out`. Restituisce `(M.S, EX, Z-stato a k_fino, A, E, X)`."""
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(os.path.join(_QUI, "chi_mattone.py"))
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    from solitone import _registro_corse as RC
    from solitone import toro as TO
    MT, CTO, CV, MR = PS.MT, PS.CT, PS.CV, PS.MR
    PS.presidi()
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    t00 = time.time()
    os.makedirs(d_out, exist_ok=True)
    print("=" * 140)
    print("LA PARTE C ALLUNGATA (Luca 2026-11-21 19:28; il task history del ramo lapse-u, sez. 13): da k %d a k %d%s; gli stati in %s" % (
        k_da, k_fino, " ### CON pi = 0 ALLA RIPRESA (il caso che DEVE FALLIRE)" if pi_zero else "", d_out))
    print("=" * 140)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        Lp = CT.Laplaciano(mot)
        s = float(Z["s"])
        C0 = PS.PO.campi(Z, rho_c, e)
        e0 = float(C0.e0)
        P, m0, a, _c = CT.parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, "C2")
        f = os.path.join(d_in, "stato_%05d.npz" % k_da)
        C, meta, cs, sh = CSB.riprendi(Z, f, False, rho_c, e)
        assert cs is None, "lo stato ha un cs_prec: non e' della corsa con chi"
        assert int(meta["k"]) == k_da
        pm = meta["parametri"]
        for q in CHIAVI_P:
            assert getattr(P, q) == pm[q], "il parametro %s ricalcolato %r contro %r nel meta: FERMO" % (q, getattr(P, q), pm[q])
        assert m0 == pm["m0"], "m0 ricalcolato %r contro %r nel meta: FERMO" % (m0, pm["m0"])
        with np.load(f) as d:
            X = {q: d[q].copy() for q in CT.CHIAVI_CHI}
        if pi_zero:
            X["pi"][...] = 0.0
        print("### la ripresa da %s (sha1 %s, ricontrollato); i parametri ricalcolati AL BIT con quelli del meta: %r; m0 %+.12e" % (f, sh[:8], P, m0))
        M = CSB.Misure(Z, meta["centro"])
        with np.load(os.path.join(d_in, "serie_%05d.npz" % k_da)) as d:
            M.S = {x: list(d[x]) for x in d.files}
        with np.load(os.path.join(d_in, "serie_chi_%05d.npz" % k_da)) as d:
            EX = {x: list(d[x]) for x in d.files}
        assert M.S["k"][-1] == k_da and EX["k"][-1] == k_da
        r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], meta["centro"][0], meta["centro"][1], Z["L"]).T[:2])
        c0n = int(np.argmin(r))
        nodo = np.asarray(mot.inc.nodo)
        ra = 0.5 * (r[nodo[0::2]] + r[nodo[1::2]])

        class CorsaChi(CTO.Corsa):
            def passo(self, k, t, r_, e_):
                C_, Z_ = self.C, self.Z
                if e_ > 0.0 and C_.e_prec == 0.0:
                    rh = MT.rho_di(Z_)
                    C_.campo.A[...] = 0.0
                    C_.campo.E[...] = C_.gauss(e_ * (rh - rh.mean()))
                elif C_.e_prec > 0.0:
                    C_.campo.E *= e_ / C_.e_prec
                C_.campo.e = e_
                C_.e_prec = e_
                CT.tick_chi(Z_["z"], C_.campo, P, Lp, X)
                totp = float(np.sum(CTO.CO.conti_nodo(Z_)["tot"]))
                self.registra(k, totp, self.kv(), float(np.sum(np.abs(Z_["st"]["psi_h"]) ** 2)))

        def misura_chi(k):
            rh = MT.rho_di(Z)
            H, Hc = CT.energia_chi(mot, Z["st"], Z["par"], P, Lp, X, C.campo)
            uN = 1.0 - np.exp(-P.kappa * X["chi"])
            cs_ = P.s * np.exp(-P.kappa * X["chi"])
            rit = math.pi * np.abs(cs_[nodo[0::2]] - cs_[nodo[1::2]])
            EX["k"].append(k)
            EX["picco"].append(float(rh.max()))
            EX["H"].append(H)
            EX["H_chi"].append(Hc)
            EX["chi_medio"].append(float(X["chi"].mean()))
            EX["max_theta"].append(float(np.max(np.abs(X["theta_a"]))))
            for R in CM.ANELLI:
                EX["uN_%d" % R].append(float(uN[c0n]) if R == 0 else CM.anello(r, uN, R))
                EX["rit_%d" % R].append(CM.anello(ra, rit, R) if R > 0 else float(np.mean(rit[(nodo[0::2] == c0n) | (nodo[1::2] == c0n)])))

        def salva(k):
            fz = os.path.join(d_out, "stato_%05d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            h = CM.sha1(fz)
            with open(fz + ".sha1", "w", encoding="utf-8") as fh:
                fh.write(h + "\n")
            M.salva(os.path.join(d_out, "serie_%05d.npz" % k))
            np.savez(os.path.join(d_out, "serie_chi_%05d.npz" % k), **{q: np.array(v_) for q, v_ in EX.items()})
            return h

        RC_ = CorsaChi(Z, C)
        RC_.etichette([meta["lab"]])
        RC_.inizio(k_da)
        t1 = t_tappa = time.time()
        R5 = rg = float("nan")
        for k in range(k_da, k_fino + 1):
            if k > k_da:
                RC_.passo(k, t0 + k, 1.0, e)
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            if k > k_da and k % CTO.OGNI == 0:
                RC_.etichette([c])
                meta["lab"] = [float(x) for x in c]
            if k % PS.OGNI == 0:
                R5, _rr, _b = PS.r5(Z, t0 + k)
                rg = MR.raggio(Z, rho, c)
            if k % PS.OGNI_MAPPA == 0:
                PS.PO.dphi_nodi(Z, t0 + k)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k > k_da and k % CM.OGNI == 0:
                M.misura(k, RC_, R5, rg)
                misura_chi(k)
            if k > k_da and k % 250 == 0:
                S = M.S
                print("    k %5d  la massa %.12e  l'energia %+.10e  il raggio %.4f  Min12.4 %.6e  il picco %.4e  H %+.10e  H_chi %+.4e  chi medio %+.4e  1-N centro %.4e  max|Theta| %.4f  (%.0f s)" % (
                    k, S["M"][-1], S["E"][-1], S["raggio"][-1], S["Min_12.4"][-1], EX["picco"][-1], EX["H"][-1], EX["H_chi"][-1], EX["chi_medio"][-1], EX["uN_0"][-1], EX["max_theta"][-1], time.time() - t00))
                sys.stdout.flush()
            if k > k_da and k % CM.OGNI_STATO == 0:
                h = salva(k)
                print("    [stato] k %d sha1 %s" % (k, h[:8]))
            adesso = time.time()
            if reg and adesso - t_tappa >= MT.TAPPA_S:
                RC.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), MT.memoria_gb()))
                t_tappa = adesso
        fine = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy(), CT.copia_X(X))
        Z["metti"]()
    print("-" * 140)
    print("### %d tick in %.0f s (%.3f s per tick)" % (k_fino - k_da, time.time() - t1, (time.time() - t1) / max(1, k_fino - k_da)))
    print("=" * 140)
    return M.S, EX, fine


def prova():
    """### la prova della ripresa *(sez. `13.2`)*: DEVE al bit da `2750` a `3000`; DEVE FALLIRE con `pi = 0`."""
    K0, K1, K_ROTTO = 2750, 3000, 2800
    S, EX, (st, A, E, X) = corsa(K0, K1, None, DIR_PROVA)
    f3 = os.path.join(DIR, "stato_%05d.npz" % K1)
    assert open(f3 + ".sha1", encoding="utf-8").read().split()[0] == CM.sha1(f3)
    diverse = []
    with np.load(f3) as d:
        for x in st:
            if not np.array_equal(st[x], d[x]):
                diverse.append(x)
        for x, v in (("campo_A", A), ("campo_E", E)):
            if not np.array_equal(v, d[x]):
                diverse.append(x)
        for q in CT.CHIAVI_CHI:
            if not np.array_equal(X[q], d[q]):
                diverse.append(q)
    with np.load(os.path.join(DIR, "serie_%05d.npz" % K1)) as d:
        S0 = {x: np.asarray(d[x]) for x in d.files}
    with np.load(os.path.join(DIR, "serie_chi_%05d.npz" % K1)) as d:
        X0 = {x: np.asarray(d[x]) for x in d.files}
    ds = [x for x in S0 if not np.array_equal(np.asarray(S[x]), S0[x])] + ["chi:" + x for x in X0 if not np.array_equal(np.asarray(EX[x]), X0[x])]
    i0 = list(S0["k"]).index(K0 + CM.OGNI)
    print("### LA RIPRESA (da k %d a k %d contro la corsa di fila): lo stato a k %d %s; le serie da k %d a k %d %s" % (
        K0, K1, K1, "AL BIT (ogni array, chi, pi, theta_a compresi)" if not diverse else "### DIVERSO: %s" % diverse,
        K0 + CM.OGNI, K1, "AL BIT (%d misure)" % (len(S0["k"]) - i0) if not ds else "### DIVERSE: %s" % ds))
    ok = not diverse and not ds
    S2, EX2, _f = corsa(K0, K_ROTTO, None, os.path.join(DIR_PROVA, "rotto"), pi_zero=True)
    j = list(S0["k"]).index(K_ROTTO)
    rotto = [x for x in ("raggio", "Min_12.4", "E") if S2[x][-1] != S0[x][j]] + ["chi:" + x for x in ("H", "H_chi", "chi_medio") if EX2[x][-1] != X0[x][j]]
    print("### IL CASO CHE DEVE FALLIRE (pi = 0 alla ripresa, fino a k %d): le misure diverse %s (H %+.10e contro %+.10e) -> %s" % (
        K_ROTTO, rotto, EX2["H"][-1], X0["H"][j], "FALLISCE, come deve" if rotto else "### NON FALLISCE: la prova non vede pi"))
    ok = ok and bool(rotto)
    print("=" * 140)
    print("### LA PROVA DELLA RIPRESA: %s" % ("PASSA" if ok else "NON PASSA: FERMO"))
    print("=" * 140)
    return 0 if ok else 1


def estremi(k, w):
    """### i minimi e i massimi locali STRETTI sulla finestra `+-FINESTRA` misure *(sez. `13.3`)*."""
    out = []
    for i in range(FINESTRA, len(w) - FINESTRA):
        fin = np.concatenate([w[i - FINESTRA:i], w[i + 1:i + FINESTRA + 1]])
        if w[i] < fin.min():
            out.append(("min", int(k[i]), float(w[i])))
        elif w[i] > fin.max():
            out.append(("max", int(k[i]), float(w[i])))
    return out


def referto(k_fine):
    import _presidio
    _presidio.avvia(__file__)
    f = os.path.join(DIR, "serie_%05d.npz" % k_fine)
    fx = os.path.join(DIR, "serie_chi_%05d.npz" % k_fine)
    with np.load(f) as d:
        S = {k: np.asarray(d[k]) for k in d.files}
    with np.load(fx) as d:
        X = {k: np.asarray(d[k]) for k in d.files}
    with np.load(CM.F_C2_SERIE) as d:
        S2 = {k: np.asarray(d[k]) for k in d.files}
    print("=" * 140)
    print("LA PARTE C ALLUNGATA: IL MATTONE DI C2 COL CAMPO CHI FINO A k %d, IL REFERTO (Luca 2026-11-21 19:28; il task history del ramo lapse-u, sez. 13)" % k_fine)
    print("=" * 140)
    print("### la serie con chi: %s (sha1 %s); la serie di chi: %s (sha1 %s); C2: %s (sha1 %s)" % (f, CM.sha1(f)[:8], fx, CM.sha1(fx)[:8], CM.F_C2_SERIE, CM.sha1(CM.F_C2_SERIE)[:8]))
    k = S["k"]
    assert np.array_equal(k, X["k"]) and np.all(np.diff(k) == CM.OGNI) and k[0] == 0 and k[-1] == k_fine, "le serie non sono continue"
    w = S["raggio"]
    print("       k    w chi     M<12.4 chi     M<25 chi       il picco      la norma          E (di oggi)       H (con chi)        H_chi      1-N centro   max|Theta|")
    for i in range(len(k)):
        if k[i] % 500 == 0:
            print("    %5d  %8.4f  %13.6e  %13.6e  %11.4e  %.10e  %+.8e  %+.10e  %+.4e  %.4e  %.4f" % (
                k[i], w[i], S["Min_12.4"][i], S["Min_25"][i], X["picco"][i], S["M"][i], S["E"][i], X["H"][i], X["H_chi"][i], X["uN_0"][i], X["max_theta"][i]))
    print("### 1 - N per anello e il ritmo del contatore per anello (1e-4 per tick), ogni 2000 tick:")
    print("       k   " + "  ".join("%9s" % ("r %d" % R) for R in CM.ANELLI))
    for i in range(len(k)):
        if k[i] % 2000 == 0:
            print("    %5d   " % k[i] + "  ".join("%9.2e" % X["uN_%d" % R][i] for R in CM.ANELLI))
            print("           " + "  ".join("%9.4f" % (X["rit_%d" % R][i] * 1e4) for R in CM.ANELLI))
    E = estremi(k, w)
    print("### GLI ESTREMI LOCALI DI w (stretti su +-%d misure, +-%d tick), da k 0:" % (FINESTRA, FINESTRA * CM.OGNI))
    for t, kk, v in E:
        i = list(k).index(kk)
        print("    %s  k %5d  w %.4f  M<12.4 %.6e  il picco %.4e" % (t, kk, v, S["Min_12.4"][i], X["picco"][i]))
    esc = [abs(E[j + 1][2] - E[j][2]) for j in range(len(E) - 1)]
    print("### le escursioni di w fra un estremo e il successivo: %s" % ", ".join("%.4f" % x for x in esc))
    dopo = [x for x in E if x[1] > 2750]
    nmin, nmax = sum(1 for x in dopo if x[0] == "min"), sum(1 for x in dopo if x[0] == "max")
    wmin = float(w.min())
    x11 = nmin >= 1 and nmax >= 1 and wmin >= 8.0
    print("### P-X11 (dopo k 2750 almeno un minimo e un massimo locali, e w mai sotto 8.0): %d minimi, %d massimi dopo k 2750; w minimo %.4f a k %d -> %s" % (
        nmin, nmax, wmin, int(k[int(np.argmin(w))]), "VERA" if x11 else "FALSA"))
    mins, maxs = [x[1] for x in E if x[0] == "min"], [x[1] for x in E if x[0] == "max"]
    if len(mins) >= 2:
        per, come = [mins[j + 1] - mins[j] for j in range(len(mins) - 1)], "fra minimi successivi"
    elif len(maxs) >= 2:
        per, come = [maxs[j + 1] - maxs[j] for j in range(len(maxs) - 1)], "fra massimi successivi"
    elif mins and maxs:
        per, come = [2 * abs(maxs[0] - mins[0])], "STIMA: il doppio della distanza fra il minimo e il massimo"
    else:
        per, come = [], "non misurabile"
    x12 = bool(per) and all(2000 <= p <= 8000 for p in per)
    print("### P-X12 (il periodo fra 2000 e 8000 tick): %s: %s -> %s" % (come, per, "VERA" if x12 else "FALSA"))
    H = X["H"]
    i3 = list(k).index(3000)
    a1 = (H[:i3 + 1].max() - H[:i3 + 1].min()) / abs(H[0])
    a2 = (H[i3:].max() - H[i3:].min()) / abs(H[0])
    p1 = np.polyfit(k[:i3 + 1], H[:i3 + 1], 1)[0]
    p2 = np.polyfit(k[i3:], H[i3:], 1)[0]
    x13 = a2 <= 2.0 * a1
    print("### P-X13 (l'escursione relativa di H su k 3000-%d non oltre il doppio di quella su k 0-3000): %.4e contro %.4e (il rapporto %.4f); la pendenza lineare di H %+.4e per tick contro %+.4e -> %s" % (
        k_fine, a2, a1, a2 / a1, p2, p1, "VERA" if x13 else "FALSA"))
    ultimo = float(w[-1])
    w2750 = float(w[list(k).index(2750)])
    collassa = nmax == 0 and ultimo < w2750 and X["picco"][-1] > X["picco"][list(k).index(2750)]
    assesta = len(esc) >= 2 and all(esc[j + 1] < esc[j] for j in range(len(esc) - 1))
    print("### LA LETTURA (sez. 13.3; la parola la sceglie Luca): OSCILLA %s; COLLASSA %s (w a k %d %.4f contro %.4f a k 2750); SI ASSESTA %s (le escursioni tutte decrescenti)" % (
        "SI'" if x11 else "NO", "SI'" if collassa else "NO", k_fine, ultimo, w2750, "SI'" if assesta else "NO"))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(3, 1, figsize=(12, 11), sharex=True)
        ax[0].plot(k, w, label="con chi")
        ax[0].plot(S2["k"], S2["raggio"], "--", label="C2 (fino a k 3000)")
        for t, kk, v in E:
            ax[0].plot([kk], [v], "v" if t == "min" else "^", color="k")
        ax[0].axhline(8.0, color="r", lw=0.5)
        ax[0].set_title("w (il raggio)")
        ax[0].legend()
        ax[1].plot(k, S["Min_12.4"], label="con chi")
        ax[1].plot(S2["k"], S2["Min_12.4"], "--", label="C2 (fino a k 3000)")
        ax[1].set_title("la massa entro 12.4")
        ax[1].legend()
        ax[2].plot(k, X["picco"], label="con chi")
        L = 186
        v = np.arange(L * L)
        a1_, a2_ = v // L, v % L
        jj = np.stack([((a1_ + 1) % L) * L + a2_, a1_ * L + (a2_ + 1) % L, ((a1_ + 1) % L) * L + (a2_ + 1) % L], axis=1).reshape(-1)
        nodo = np.empty(2 * len(jj), dtype=np.int64)
        nodo[0::2], nodo[1::2] = np.repeat(v, 3), jj
        kc, pc = [], []
        for kk in range(250, 3001, 250):
            fs = os.path.join(CM.D_C2, "stato_%05d.npz" % kk)
            with np.load(fs) as d:
                pc.append(float(np.max(np.bincount(nodo, weights=np.sum(np.abs(d["psi_h"]) ** 2, axis=1), minlength=L * L))))
            kc.append(kk)
        ax[2].plot(kc, pc, "--o", ms=3, label="C2 (fino a k 3000, gli stati ogni 250)")
        ax[2].set_title("il picco di rho")
        ax[2].set_xlabel("k")
        ax[2].legend()
        fig.tight_layout()
        fp = os.path.join(_QUI, "chi_mattone_v2.png")
        fig.savefig(fp, dpi=90)
        print("### la figura: %s" % fp)
    except ImportError as x:
        print("### la figura NON fatta: %s" % x)
    print("=" * 140)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("corsa")
    c.add_argument("--da", type=int, required=True)
    c.add_argument("--fino", type=int, required=True)
    c.add_argument("--registro")
    sub.add_parser("prova")
    r = sub.add_parser("referto")
    r.add_argument("--fino", type=int, default=20000)
    x = ap.parse_args(argv)
    if x.cmd == "corsa":
        corsa(x.da, x.fino, x.registro, DIR)
        return 0
    if x.cmd == "prova":
        return prova()
    return referto(x.fino)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
