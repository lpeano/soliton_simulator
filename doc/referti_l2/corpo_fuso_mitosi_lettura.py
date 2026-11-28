# -*- coding: utf-8 -*-
r"""**[M1013] C-3, LA LETTURA DI C SU 0-16250** *(DECISIONE DI LUCA, 2026-11-28 10:13; la carta `doc/CARTA_mitosi.md`, sezione «C, LA CURA DEL FLIP
ILLEGALE E LA LETTURA SU 0-16250», C-3; lettura, nessun tick)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_mitosi_lettura.py > doc/referti_l2/corpo_fuso_mitosi_lettura.txt

**Le fonti:** `M0026/C/nascite.json` *(le nascite fino a 16250)*, gli stati `stato_*.npz` ogni 250, le righe «k ...: ... H ..., E_persa ...» del log
`controllo/M1446/log/M0026_C.txt`. **Il respiro C4 su [15500, 18000] NON si legge qui.**
- **Il ritmo:** le nascite per bin di 250 tick *(la griglia allineata a 250, dal bin che contiene la prima)*, la retta `a + b t` e l'esponenziale
  `exp(c + t / tau)` adattate con la DEVIANZA DI POISSON *(due parametri ciascuna)*; vince la devianza piu' bassa, «NON DECIDIBILE» se la differenza e' < 2.
  (L1) dati sintetici esponenziali: vince l'esponenziale, `tau` entro il 5%; (L2) dati sintetici lineari: vince la retta.
- **L'energia:** `H`, `E_persa`, `H + E_persa` contro le nascite; «come nella fiammata» se `H + E_persa` resta costante entro l'1% della variazione di `H`.
- **Il corpo ogni 1000 dal 11000:** `R` *(rms dal centro periodico di `rho_psi`)*, `max rho_psi`, `max |chi|`. (L3) `R` di `stato_011000` con le posizioni
  della scena = con le posizioni di `stato_011750` *(i primi `n0` nodi)* AL BIT.
- **Il raggio della nascita:** la distanza del nato *(`pos` del registro)* dal centro di `rho_psi` dello stato salvato subito prima, contro `2 R`.
- (L4) le nascite di `nascite.json` = `meta["nascite"]` di `stato_016250` = le righe «[nascita ...]» del log con `k <= 16250`.
"""
import json
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import corpo_fuso_mitosi as CFM  # noqa: E402  (### anche il percorso di csv/, per _presidio)

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
D_C = os.path.join(CTRL, "M0026", "C")
LOG = os.path.join(CTRL, "M1446", "log", "M0026_C.txt")
K_FINE, BIN = 16250, 250
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def devianza(y, lam):
    lam = np.maximum(lam, 1e-300)
    t = np.where(y > 0, y * np.log(np.where(y > 0, y, 1.0) / lam), 0.0)
    return float(2.0 * np.sum(t - (y - lam)))


def adatta(t, y):
    """### la retta e l'esponenziale con la devianza di Poisson."""
    from scipy.optimize import minimize
    t0 = float(t.mean())
    s = t - t0
    b0, a0 = np.polyfit(s, y, 1)

    def f_lin(p):
        lam = p[0] + p[1] * s
        return 1e30 if np.any(lam <= 0) else devianza(y, lam)
    r_lin = minimize(f_lin, [max(a0, 1e-3), b0], method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-10, "maxiter": 20000})
    q1, q0 = np.polyfit(s, np.log(np.maximum(y, 0.5)), 1)

    def f_exp(p):
        return devianza(y, np.exp(p[0] + p[1] * s))
    r_exp = minimize(f_exp, [q0, q1], method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-10, "maxiter": 20000})
    return {"retta": (r_lin.x, float(r_lin.fun)), "esponenziale": (r_exp.x, float(r_exp.fun)), "t0": t0}


def verdetto(F):
    dl, de = F["retta"][1], F["esponenziale"][1]
    if abs(dl - de) < 2.0:
        return "NON DECIDIBILE"
    return "esponenziale" if de < dl else "retta"


def leggi_log():
    righe, nasc = [], []
    pat = re.compile(r"^    k (\d+): .*?max\|chi\| ([\d.e+\-]+); nascite (\d+), n (\d+); H ([+\-\d.e]+), E_persa ([+\-\d.e]+)")
    pn = re.compile(r"^    \[nascita (\d+)\] k (\d+),")
    for r in open(LOG, encoding="utf-8", errors="replace"):
        m = pat.match(r)
        if m:
            righe.append((int(m.group(1)), float(m.group(2)), int(m.group(3)), int(m.group(4)), float(m.group(5)), float(m.group(6))))
        m = pn.match(r)
        if m:
            nasc.append((int(m.group(1)), int(m.group(2))))
    return righe, nasc


def main():
    import _presidio
    _presidio.avvia(__file__)
    from solitone import toro as TO
    print("=" * 134)
    print("[M1013] C-3: LA LETTURA DI C (M0026/C) SU 0-16250 -- IL RITMO DELLE NASCITE, L'ENERGIA, IL CORPO, IL RAGGIO DELLA NASCITA")
    print("=" * 134)
    # ### L1, L2: i dati sintetici
    rng = np.random.default_rng(20261128)
    t = np.arange(11500, 16250, BIN, dtype=float) + 0.5 * BIN
    tau_v = 1800.0
    ys = rng.poisson(np.exp(math.log(8.0) + (t - t[0]) / tau_v)).astype(float)
    F = adatta(t, ys)
    tau_f = 1.0 / F["esponenziale"][0][1]
    esito("(L1) sintetici esponenziali (tau %.0f): vince l'esponenziale, tau entro il 5%%" % tau_v, verdetto(F) == "esponenziale" and abs(tau_f / tau_v - 1) < 0.05,
          "%s; tau %.1f; devianze retta %.2f, esp %.2f" % (verdetto(F), tau_f, F["retta"][1], F["esponenziale"][1]))
    yl = rng.poisson(5.0 + 0.012 * (t - t[0])).astype(float)
    F = adatta(t, yl)
    esito("(L2) sintetici lineari: vince la retta", verdetto(F) == "retta", "%s; devianze retta %.2f, esp %.2f" % (verdetto(F), F["retta"][1], F["esponenziale"][1]))
    # ### L4
    B = json.load(open(os.path.join(D_C, "nascite.json"), encoding="utf-8"))
    with np.load(os.path.join(D_C, "stato_%06d.npz" % K_FINE)) as z:
        meta = json.loads(str(z["meta"]))
    righe, nasc = leggi_log()
    nl = sum(1 for _q, k in nasc if k <= K_FINE)
    esito("(L4) le nascite: nascite.json = meta di stato_016250 = il log con k <= 16250", len(B) == meta["nascite"] == nl, "%d, %d, %d" % (len(B), meta["nascite"], nl))
    print("-" * 134)
    # ### il ritmo
    kb = np.array([b["k"] for b in B])
    t_ini = (int(kb.min()) // BIN) * BIN
    bordi = np.arange(t_ini, K_FINE + 1, BIN)
    y, _ = np.histogram(kb, bins=bordi)
    tc = 0.5 * (bordi[:-1] + bordi[1:])
    print("### IL RITMO: le nascite per bin di %d tick da k %d a %d (%d bin; la prima a k %d, %d nascite):" % (BIN, t_ini, K_FINE, len(y), int(kb.min()), int(y.sum())))
    print("    " + " ".join("%d" % v for v in y))
    for a in range(11000, K_FINE, 1000):
        print("    [%5d, %5d): %4d nascite" % (a, a + 1000, int(((kb >= a) & (kb < a + 1000)).sum())))
    F = adatta(tc, y.astype(float))
    (ra, rb), dl = F["retta"]
    (ec, eq), de = F["esponenziale"]
    print("  la retta: rate = %.3f + %.5f (t - %.0f) a bin; devianza %.3f (gradi di liberta' %d)" % (ra, rb, F["t0"], dl, len(y) - 2))
    print("  l'esponenziale: rate = exp(%.4f + (t - %.0f) / %.1f) a bin; il raddoppio ogni %.0f tick; devianza %.3f" % (ec, F["t0"], 1.0 / eq, math.log(2.0) / eq, de))
    print("### IL RITMO, IL VERDETTO (la carta: devianza piu' bassa, < 2 NON DECIDIBILE): %s (differenza %.3f)" % (verdetto(F), dl - de))
    print("-" * 134)
    # ### l'energia
    R_ = np.array(righe)
    H, Ep, nn = R_[:, 4], R_[:, 5], R_[:, 2]
    S = H + Ep
    print("### L'ENERGIA dal log (ogni 1000):")
    for r in righe:
        if (r[0] % 1000 == 0 and r[0] <= K_FINE) or r[0] == K_FINE:
            print("    k %5d: nascite %3d, n %5d; H %+.6e, E_persa %+.6e, H + E_persa %+.6e" % (r[0], r[2], r[3], r[4], r[5], r[4] + r[5]))
    pre, post = R_[:, 0] < 11500, (R_[:, 0] >= 11500) & (R_[:, 0] <= K_FINE)
    dH = float(H[post].max() - H[post].min())
    dS = float(S[post].max() - S[post].min())
    print("  senza nascite (k < 11500): H da %+.6e a %+.6e, l'escursione di H %.4e" % (H[pre][0], H[pre][-1], float(H[pre].max() - H[pre].min())))
    print("  con le nascite (11500..16250): l'escursione di H %.4e, di H + E_persa %.4e (il rapporto %.4f); H + E_persa da %+.6e a %+.6e" % (
        dH, dS, dS / dH, float(S[post][0]), float(S[post][-1])))
    pf = np.polyfit(nn[post], S[post], 1)
    print("  H + E_persa contro il numero di nascite: la pendenza %+.4e a nascita" % pf[0])
    print("### L'ENERGIA, LA LETTURA (la carta: costante entro l'1%% della variazione di H): %s" % ("COME NELLA FIAMMATA" if dS < 0.01 * dH else "NON COSTANTE: il tick non conserva H + E_persa"))
    print("-" * 134)
    # ### il corpo
    with CFM.V6.GD.TC.scena() as Z:
        nodo0 = np.asarray(Z["mot"].inc.nodo)
        n0, L = int(Z["mot"].inc.n), int(Z["L"])
        m1s, m2s = np.asarray(Z["m1"], dtype=float), np.asarray(Z["m2"], dtype=float)
        Z["metti"]()

    def corpo(k, pos=None):
        with np.load(os.path.join(D_C, "stato_%06d.npz" % k)) as z:
            psi, chi = z["psi_h"], z["chi"]
            if "ii" in z.files:
                ii, jj = z["ii"], z["jj"]
                nodo = np.empty(2 * len(ii), dtype=np.int64)
                nodo[0::2], nodo[1::2] = ii, jj
                m1, m2 = z["m1"], z["m2"]
            else:
                nodo, m1, m2 = nodo0, m1s, m2s
        if pos is not None:
            m1, m2 = pos
        n = len(m1)
        rho = np.bincount(nodo, weights=np.sum(np.abs(psi) ** 2, axis=1), minlength=n)
        c1, c2, _x, _y = TO.centro(rho, m1, m2, L)
        d = np.asarray(TO.scarti(m1, m2, c1, c2, L))[:, :2]
        r = np.hypot(d[:, 0], d[:, 1])
        R = float(np.sqrt(np.sum(rho * r ** 2) / np.sum(rho)))
        return {"R": R, "rho_max": float(rho.max()), "chi_max": float(np.max(np.abs(chi))), "c": (c1, c2), "n": n}
    with np.load(os.path.join(D_C, "stato_011750.npz")) as z:
        p1, p2 = z["m1"][:n0], z["m2"][:n0]
    a3, b3 = corpo(11000), corpo(11000, (p1, p2))
    esito("(L3) R di stato_011000 con le posizioni della scena = con quelle di stato_011750 AL BIT", a3["R"] == b3["R"], "%.12f contro %.12f" % (a3["R"], b3["R"]))
    print("### IL CORPO ogni 1000 dal 11000:")
    CS = {}
    for k in range(11000, K_FINE + 1, BIN):
        CS[k] = corpo(k)
    for k in list(range(11000, K_FINE, 1000)) + [K_FINE]:
        c = CS[k]
        print("    k %5d: n %5d; R %.4f; max rho_psi %.6e; max |chi| %.4e" % (k, c["n"], c["R"], c["rho_max"], c["chi_max"]))
    print("-" * 134)
    # ### il raggio della nascita
    print("### IL RAGGIO DELLA NASCITA: la distanza del nato dal centro di rho_psi dello stato salvato subito prima, contro 2 R di quello stato")
    dist, dentro = [], []
    for b in B:
        ks = (b["k"] // BIN) * BIN
        c = CS[max(ks, 11000)]
        d = np.asarray(TO.scarti(np.array([b["pos"][0]]), np.array([b["pos"][1]]), c["c"][0], c["c"][1], L))[0, :2]
        dist.append(float(np.hypot(d[0], d[1])))
        dentro.append(dist[-1] <= 2.0 * c["R"])
    dist, dentro = np.array(dist), np.array(dentro)
    for a in range(11000, K_FINE, 1000):
        s = (kb >= a) & (kb < a + 1000)
        if s.sum():
            print("    [%5d, %5d): %4d nascite; la distanza mediana %.2f, massima %.2f; entro 2 R %.1f%% (2 R a k %d: %.2f)" % (
                a, a + 1000, int(s.sum()), float(np.median(dist[s])), float(dist[s].max()), 100.0 * float(dentro[s].mean()), a, 2.0 * CS[a]["R"]))
    print("### IL RAGGIO, TUTTE: %d nascite su %d entro 2 R (%.1f%%); la distanza massima %.2f" % (int(dentro.sum()), len(dentro), 100.0 * float(dentro.mean()), float(dist.max())))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
