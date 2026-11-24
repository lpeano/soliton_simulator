# -*- coding: utf-8 -*-
r"""**LA PARTE C: IL MATTONE DI C2 COL CAMPO CHI, 3000 TICK** *(il mandato di Luca `2026-11-21` `15:57`, con la forma (a) e la massa; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `9.4`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_mattone.py corsa --fino 3000 --registro chi-mattone
    E:\python\py3132\python.exe doc/referti_l2/chi_mattone.py referto > doc/referti_l2/chi_mattone.txt

**La corsa** *(il cammino di `controllo_senza_bordo.corsa`, `CorsaSB` con il tick di `chi_tick` al posto di `tick_GU`; NESSUN lapse `N(rho)`: `PO.accendi` non si chiama)*: i parametri CALCOLATI *(`chi_tick.parametri`)*; **`k 0` di C2** *(`prepara`, senza bordo)*; **`chi` al profilo statico della sorgente di `k 0`, `pi = 0`**; ogni `50` tick le misure di C2 *(`Misure`)* piu' **il picco di `rho`, `H` e `H_chi`, la media di `chi`, `1 - N` per anello, il ritmo `pi |cs_i - cs_j|` per anello, `max |Theta|`**; gli stati ogni `250` tick in `E:/soliton_simulator/controllo/CHI/mattone/` *(con `chi`, `pi`, `theta_a`)*.
**Il referto:** il confronto con C2 agli stessi tick *(`E:/soliton_simulator/controllo/C2/serie_03000.npz`; il picco dagli stati di C2 ogni `250`)*; **P-X4** *(a `3000` tick `w` = `raggio` e la massa entro `12.4` entro il `10%` di C2: «il mattone regge»)*; **P-X5** *(`1 - N` all'anello `60` sopra il `5%` del centro per tutta la corsa; ### la coda contro il vuoto lontano, la carta sez. `11.4`: `(u60 - u80) / (u0 - u80)`, e accanto il rapporto grezzo)*; **le figure** *(`chi_mattone.png`)*.
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

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "mattone")
F_C2_SERIE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "C2", "serie_03000.npz")
D_C2 = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "C2")
OGNI, OGNI_STATO = 50, 250
ANELLI = (0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80)


def sha1(f):
    import hashlib
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def anello(r, y, R):
    w = (r >= R - 0.5) & (r < R + 0.5)
    return float(y[w].mean()) if w.any() else math.nan


def corsa(k_fino, reg):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    from solitone import _registro_corse as RC
    from solitone import toro as TO
    MT, CTO, CV, MR = PS.MT, PS.CT, PS.CV, PS.MR
    PS.presidi()
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    t00 = time.time()
    os.makedirs(DIR, exist_ok=True)
    print("=" * 140)
    print("LA PARTE C: IL MATTONE DI C2 COL CAMPO CHI (Luca 2026-11-21 15:57; il task history del ramo lapse-u, sez. 9.4), da k 0 a k %d" % k_fino)
    print("=" * 140)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        s = float(Z["s"])
        Lp = CT.Laplaciano(mot)
        C0 = PS.PO.campi(Z, rho_c, e)
        e0 = float(C0.e0)
        P, m0, a, _c = CT.parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, "C2")
        print("### i parametri (CALCOLATI): %r; m0 %+.12e; a %.10e" % (P, m0, a))
        C, meta = CSB.prepara(Z, 186, False, rho_c, e, t0)
        rho = MT.rho_di(Z)
        meta["centro"] = [float(x) for x in MT.centro_di(Z, rho)]
        meta["lab"] = meta["centro"]
        meta["parametri"] = {"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s}
        M = CSB.Misure(Z, meta["centro"])
        r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], meta["centro"][0], meta["centro"][1], Z["L"]).T[:2])
        c0n = int(np.argmin(r))
        nodo = np.asarray(mot.inc.nodo)
        ra =0.5 * (r[nodo[0::2]] + r[nodo[1::2]])
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0))
        print("### k 0 di C2: %s; il centro %s, il nodo %d; chi statico al centro %+.6e, 1 - N al centro %.6e" % (
            json.dumps({k: meta[k] for k in ("Delta", "R_ogg5_k0")}), meta["centro"], c0n, X["chi"][c0n], 1.0 - math.exp(-P.kappa * X["chi"][c0n])))

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

        EX = {x: [] for x in ("k", "picco", "H", "H_chi", "chi_medio", "max_theta") + tuple("uN_%d" % R for R in ANELLI) + tuple("rit_%d" % R for R in ANELLI)}

        def misura_chi(k):
            rh = MT.rho_di(Z)
            H, Hc = CT.energia_chi(mot, Z["st"], Z["par"], P, Lp, X, C.campo)
            uN = 1.0 - np.exp(-P.kappa * X["chi"])
            cs = P.s * np.exp(-P.kappa * X["chi"])
            rit = math.pi * np.abs(cs[nodo[0::2]] - cs[nodo[1::2]])
            EX["k"].append(k)
            EX["picco"].append(float(rh.max()))
            EX["H"].append(H)
            EX["H_chi"].append(Hc)
            EX["chi_medio"].append(float(X["chi"].mean()))
            EX["max_theta"].append(float(np.max(np.abs(X["theta_a"]))))
            for R in ANELLI:
                EX["uN_%d" % R].append(float(uN[c0n]) if R == 0 else anello(r, uN, R))
                EX["rit_%d" % R].append(anello(ra, rit, R) if R > 0 else float(np.mean(rit[(nodo[0::2] == c0n) | (nodo[1::2] == c0n)])))

        def salva(k):
            f = os.path.join(DIR, "stato_%05d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(f, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            h = sha1(f)
            with open(f + ".sha1", "w", encoding="utf-8") as fh:
                fh.write(h + "\n")
            M.salva(os.path.join(DIR, "serie_%05d.npz" % k))
            np.savez(os.path.join(DIR, "serie_chi_%05d.npz" % k), **{q: np.array(v_) for q, v_ in EX.items()})
            return h

        RC_ = CorsaChi(Z, C)
        RC_.etichette([meta["lab"]])
        RC_.inizio(0)
        t1 = t_tappa = time.time()
        R5 = rg = float("nan")
        for k in range(0, k_fino + 1):
            if k > 0:
                RC_.passo(k, t0 + k, 1.0, e)
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            if k > 0 and k % CTO.OGNI == 0:
                RC_.etichette([c])
                meta["lab"] = [float(x) for x in c]
            if k % PS.OGNI == 0:
                R5, _rr, _b = PS.r5(Z, t0 + k)
                rg = MR.raggio(Z, rho, c)
            if k % PS.OGNI_MAPPA == 0:
                PS.PO.dphi_nodi(Z, t0 + k)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % OGNI == 0:
                M.misura(k, RC_, R5, rg)
                misura_chi(k)
            if k % 250 == 0:
                S = M.S
                print("    k %5d  la massa %.12e  l'energia %+.10e  il raggio %.4f  Min12.4 %.6e  il picco %.4e  H %+.10e  H_chi %+.4e  chi medio %+.4e  1-N centro %.4e  max|Theta| %.4f  (%.0f s)" % (
                    k, S["M"][-1], S["E"][-1], S["raggio"][-1], S["Min_12.4"][-1], EX["picco"][-1], EX["H"][-1], EX["H_chi"][-1], EX["chi_medio"][-1], EX["uN_0"][-1], EX["max_theta"][-1], time.time() - t00))
                sys.stdout.flush()
            if k > 0 and k % OGNI_STATO == 0:
                h = salva(k)
                print("    [stato] k %d sha1 %s" % (k, h[:8]))
            adesso = time.time()
            if reg and adesso - t_tappa >= MT.TAPPA_S:
                RC.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k), MT.memoria_gb()))
                t_tappa = adesso
        Z["metti"]()
    print("-" * 140)
    print("### %d tick in %.0f s (%.3f s per tick)" % (k_fino, time.time() - t1, (time.time() - t1) / max(1, k_fino)))
    print("=" * 140)
    return 0


def referto():
    import _presidio
    _presidio.avvia(__file__)
    f = os.path.join(DIR, "serie_03000.npz")
    fx = os.path.join(DIR, "serie_chi_03000.npz")
    with np.load(f) as d:
        S = {k: np.asarray(d[k]) for k in d.files}
    with np.load(fx) as d:
        X = {k: np.asarray(d[k]) for k in d.files}
    with np.load(F_C2_SERIE) as d:
        S2 = {k: np.asarray(d[k]) for k in d.files}
    print("=" * 140)
    print("LA PARTE C: IL MATTONE DI C2 COL CAMPO CHI, IL REFERTO (Luca 2026-11-21 15:57; il task history del ramo lapse-u, sez. 9.4)")
    print("=" * 140)
    print("### la serie con chi: %s (sha1 %s); C2: %s (sha1 %s)" % (f, sha1(f)[:8], F_C2_SERIE, sha1(F_C2_SERIE)[:8]))
    assert np.array_equal(S["k"], S2["k"]), "i tick delle due serie NON coincidono"
    print("       k    w chi     w C2     M<12.4 chi     M<12.4 C2      M<25 chi       M<25 C2      la norma chi    la norma C2     E chi            E C2")
    for i, k in enumerate(S["k"]):
        if k % 250 == 0:
            print("    %5d  %8.4f %8.4f  %13.6e  %13.6e  %13.6e  %13.6e  %.10e  %.10e  %+.8e  %+.8e" % (
                k, S["raggio"][i], S2["raggio"][i], S["Min_12.4"][i], S2["Min_12.4"][i], S["Min_25"][i], S2["Min_25"][i], S["M"][i], S2["M"][i], S["E"][i], S2["E"][i]))
    L = 186
    v = np.arange(L * L)
    a1, a2 = v // L, v % L
    jj = np.stack([((a1 + 1) % L) * L + a2, a1 * L + (a2 + 1) % L, ((a1 + 1) % L) * L + (a2 + 1) % L], axis=1).reshape(-1)
    nodo = np.empty(2 * len(jj), dtype=np.int64)
    nodo[0::2], nodo[1::2] = np.repeat(v, 3), jj
    print("### il picco di rho (ricalcolato dalle estremita'), con chi e C2:")
    for k in range(500, 3001, 500):
        fs = os.path.join(D_C2, "stato_%05d.npz" % k)
        assert open(fs + ".sha1", encoding="utf-8").read().split()[0] == sha1(fs)
        with np.load(fs) as d:
            p2 = float(np.max(np.bincount(nodo, weights=np.sum(np.abs(d["psi_h"]) ** 2, axis=1), minlength=L * L)))
        i = list(X["k"]).index(k)
        print("    k %5d   con chi %.6e   C2 %.6e   il rapporto %.4f" % (k, X["picco"][i], p2, X["picco"][i] / p2))
    print("### 1 - N per anello (con chi):")
    print("       k   " + "  ".join("%9s" % ("r %d" % R) for R in ANELLI) + "   chi medio     H_chi        H")
    for i, k in enumerate(X["k"]):
        if k % 250 == 0:
            print("    %5d   " % k + "  ".join("%9.2e" % X["uN_%d" % R][i] for R in ANELLI) + "   %+.3e   %+.3e   %+.8e" % (X["chi_medio"][i], X["H_chi"][i], X["H"][i]))
    print("### il ritmo del contatore pi |cs_i - cs_j| per anello (1e-4 per tick; l'anello 0: gli archi del nodo del centro), e max |Theta|:")
    for i, k in enumerate(X["k"]):
        if k % 500 == 0:
            print("    %5d   " % k + "  ".join("%9.4f" % (X["rit_%d" % R][i] * 1e4) for R in ANELLI) + "   max|Theta| %.4f" % X["max_theta"][i])
    i3 = list(S["k"]).index(3000)
    dw = abs(S["raggio"][i3] / S2["raggio"][i3] - 1.0)
    dm = abs(S["Min_12.4"][i3] / S2["Min_12.4"][i3] - 1.0)
    regge = dw <= 0.10 and dm <= 0.10
    print("### P-X4 (a 3000 tick w e la massa entro 12.4 entro il 10%% di C2): w %.4f contro %.4f (%.4f), M<12.4 %.6e contro %.6e (%.4f) -> %s" % (
        S["raggio"][i3], S2["raggio"][i3], dw, S["Min_12.4"][i3], S2["Min_12.4"][i3], dm, "VERA: il mattone REGGE" if regge else "FALSA: il mattone NON regge (FERMO)"))
    u0, u60, u80 = np.array(X["uN_0"]), np.array(X["uN_60"]), np.array(X["uN_80"])
    q = (u60 - u80) / (u0 - u80)
    qg = u60 / u0
    print("### P-X5 (la carta sez. 11.4: (u60 - u80) / (u0 - u80) sopra 0.05 a ogni misura): il minimo %.4f, il massimo %.4f -> %s; il rapporto grezzo u60 / u0: il minimo %.4f, il massimo %.4f" % (
        q.min(), q.max(), "VERA" if q.min() > 0.05 else "FALSA", qg.min(), qg.max()))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 2, figsize=(13, 9))
        ax[0, 0].plot(S["k"], S["raggio"], label="con chi")
        ax[0, 0].plot(S2["k"], S2["raggio"], "--", label="C2")
        ax[0, 0].set_title("w (il raggio)")
        ax[0, 0].legend()
        ax[0, 1].plot(S["k"], S["Min_12.4"], label="con chi")
        ax[0, 1].plot(S2["k"], S2["Min_12.4"], "--", label="C2")
        ax[0, 1].set_title("la massa entro 12.4")
        ax[0, 1].legend()
        for i, k in enumerate(X["k"]):
            if k in (0, 1000, 2000, 3000):
                ax[1, 0].plot(ANELLI, [X["uN_%d" % R][i] for R in ANELLI], marker="o", label="k %d" % k)
        ax[1, 0].axhline(0.0, color="k", lw=0.5)
        ax[1, 0].set_title("1 - N per anello")
        ax[1, 0].legend()
        for i, k in enumerate(X["k"]):
            if k in (0, 1000, 2000, 3000):
                ax[1, 1].plot(ANELLI, [X["rit_%d" % R][i] * 1e4 for R in ANELLI], marker="o", label="k %d" % k)
        ax[1, 1].set_title("il ritmo del contatore per anello (1e-4 per tick)")
        ax[1, 1].legend()
        fig.tight_layout()
        fp = os.path.join(_QUI, "chi_mattone.png")
        fig.savefig(fp, dpi=90)
        print("### le figure: %s" % fp)
    except ImportError as x:
        print("### le figure NON fatte: %s" % x)
    print("=" * 140)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("corsa")
    c.add_argument("--fino", type=int, required=True)
    c.add_argument("--registro")
    sub.add_parser("referto")
    x = ap.parse_args(argv)
    if x.cmd == "corsa":
        return corsa(x.fino, x.registro)
    return referto()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
