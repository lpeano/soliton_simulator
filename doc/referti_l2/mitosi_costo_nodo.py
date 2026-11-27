# -*- coding: utf-8 -*-
r"""**[M2245-27] A1, IL COSTO DI UN NODO** *(DECISIONE DI LUCA, 2026-11-27 22:45; la carta `doc/CARTA_mitosi.md`, sez. «A. LE CINQUE LETTURE», A1; solo letture)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_costo_nodo.py > doc/referti_l2/mitosi_costo_nodo.txt

**Per ogni nascita della fiammata** *(MITOSI + MITOSI_V2, `538`, i registri `nascite_*.json`)*: `DH` *(dal registro)*, `n(k) = n0 + i`
*(`n0` = `n` del meta di `MITOSI/stato_36000` meno le sue nascite; `i` il numero d'ordine: la regola di `mitosi_energia_fiammata.py`)*,
**la densita' locale** = la media di `rho` sui nodi a distanza `< 4` dalla `pos` della nascita *(`toro.scarti`, `L 186`)*, dallo stato salvato
piu' vicino con `k <=` quello della nascita *(risoluzione `250`, dichiarata)*. **Il fit, dichiarato prima:** `DH = a + b x` ai minimi quadrati,
`sigma` dai residui; **COSTANTE** se `|b| < 2 sigma_b`; se no con `c x^2`: **LINEARE** se `|c| < 2 sigma_c`, **ALTRO** se no. Lo Spearman stampato.
**Casi noti:** (K1) `-somma DH` = `E_persa` finale entro `1e-9`; (K2) il fit su dati sintetici costanti + rumore da' COSTANTE, su dati con una
pendenza nota la ritrova entro `2 sigma`; (K3) la densita' locale di una `rho` costante `0.5` e' `0.5` al bit.
"""
import glob
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "csv", "solitone")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import mitosi_dati as MD  # noqa: E402

L = 186
R_LOC = 4.0
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def nascite():
    N = {}
    for c in ("MITOSI", "MITOSI_V2"):
        for x in json.load(open(MD.ultimo(c, "nascite"), encoding="utf-8")):
            N.setdefault((int(x["k"]), int(x["a"])), x)
    return [N[q] for q in sorted(N)]


def stati():
    """### `[(k, file)]` ordinati: il tronco prima della prima nascita, MITOSI, MITOSI_V2."""
    out = [(35976, os.path.join(MD.R, "TRONCO", "prima_nascita_35976.npz"))]
    for c in ("MITOSI", "MITOSI_V2"):
        for f in glob.glob(os.path.join(MD.R, c, "stato_*.npz")):
            out.append((int(os.path.basename(f)[6:-4]), f))
    return sorted(out)


def densita_locale(rho, m1, m2, pos):
    from solitone import toro as TO
    d = np.asarray(TO.scarti(m1, m2, float(pos[0]), float(pos[1]), L))[:, :2]
    sel = np.hypot(d[:, 0], d[:, 1]) < R_LOC
    return float(rho[sel].mean()), int(sel.sum())


def fit(x, y, grado):
    X = np.column_stack([x ** p for p in range(grado + 1)])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ c
    s2 = float(r @ r) / max(len(y) - grado - 1, 1)
    cov = s2 * np.linalg.inv(X.T @ X)
    return c, np.sqrt(np.diag(cov))


def verdetto(x, y):
    xs = (x - x.mean()) / x.std()          # ### standardizzato: solo per il condizionamento; il verdetto non cambia
    c1, s1 = fit(xs, y, 1)
    if abs(c1[1]) < 2.0 * s1[1]:
        return "COSTANTE", c1, s1, None, None
    c2, s2 = fit(xs, y, 2)
    return ("LINEARE" if abs(c2[2]) < 2.0 * s2[2] else "ALTRO"), c1, s1, c2, s2


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_dati.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2245-27] A1, IL COSTO DI UN NODO (la carta doc/CARTA_mitosi.md, A1): DH per nascita contro n(k) e contro la densita' locale")
    print("=" * 130)
    nas = nascite()
    DH = np.array([float(x["DH"]) for x in nas])
    ks = np.array([int(x["k"]) for x in nas])
    # ### (K1)
    ep = float(nas[-1]["E_persa"])
    r = abs(-float(DH.sum()) - ep) / abs(ep)
    esito("(K1) -somma DH delle %d nascite = E_persa finale entro 1e-9 relativo" % len(DH), r < 1e-9, "|d|/|E_persa| %.3e" % r)
    # ### n(k)
    with np.load(os.path.join(MD.R, "MITOSI", "stato_36000.npz"), allow_pickle=True) as z:
        meta = json.loads(str(z["meta"]))
    n0 = int(meta["n"]) - int(meta["nascite"])
    n = n0 + np.arange(len(nas), dtype=float)
    print("  n0 %d (n %d meno %d nascite di stato_36000); n da %d a %d" % (n0, int(meta["n"]), int(meta["nascite"]), int(n[0]), int(n[-1])))
    # ### (K3)
    S = stati()
    with np.load(S[0][1], allow_pickle=True) as z:
        m1, m2 = z["m1"].copy(), z["m2"].copy()
    v, cnt = densita_locale(np.full(len(m1), 0.5), m1, m2, nas[0]["pos"])
    esito("(K3) la densita' locale di una rho costante 0.5 = 0.5 AL BIT", v == 0.5, "%.17g su %d nodi" % (v, cnt))
    # ### (K2)
    rng = np.random.default_rng(20261127)
    y0 = float(DH.mean()) + float(DH.std()) * rng.standard_normal(len(n))
    v0 = verdetto(n, y0)
    esito("(K2) dati sintetici costanti + rumore (sigma = std dei DH, seme 20261127): COSTANTE", v0[0] == "COSTANTE", "b %+.4e +- %.4e" % (v0[1][1], v0[2][1]))
    b_vera = 0.01
    y1 = 3.0 + b_vera * n + 0.5 * rng.standard_normal(len(n))
    c1, s1 = fit(n - n.mean(), y1, 1)
    esito("(K2) pendenza nota %.3g: ritrovata entro 2 sigma" % b_vera, abs(c1[1] - b_vera) < 2.0 * s1[1], "b %+.6e +- %.2e" % (c1[1], s1[1]))
    # ### la densita' locale
    print("-" * 130)
    ks_s = np.array([k for k, _ in S])
    rho_loc = np.zeros(len(nas))
    cache = {}
    for i, x in enumerate(nas):
        j = int(np.searchsorted(ks_s, int(x["k"]), side="right") - 1)
        assert j >= 0
        if j not in cache:
            cache.clear()
            with np.load(S[j][1], allow_pickle=True) as z:
                cache[j] = (z["rho"].copy(), z["m1"].copy(), z["m2"].copy(), S[j][0])
        rho, a1, a2, kst = cache[j]
        rho_loc[i], _ = densita_locale(rho, a1, a2, x["pos"])
    print("  la densita' locale (r < %.0f, dallo stato salvato prima): media %.4e, da %.4e a %.4e" % (R_LOC, rho_loc.mean(), rho_loc.min(), rho_loc.max()))
    print("  DH: media %+.4f, da %+.4f a %+.4f" % (DH.mean(), DH.min(), DH.max()))
    print("-" * 130)
    for nome, x in (("n(k)", n), ("la densita' locale", rho_loc), ("r dal centro (registro)", np.array([float(q["r"]) for q in nas]))):
        v = verdetto(x, DH)
        riga = "  DH contro %-24s: %-9s b %+.4e +- %.4e (per una deviazione standard di x)" % (nome, v[0], v[1][1], v[2][1])
        if v[3] is not None:
            riga += "; c %+.4e +- %.4e" % (v[3][2], v[4][2])
        print(riga + "; Spearman %+.4f" % spearman(x, DH))
    print("-" * 130)
    print("  DH per decile della densita' locale:")
    q = np.quantile(rho_loc, np.linspace(0, 1, 11))
    for a, b in zip(q[:-1], q[1:]):
        s = (rho_loc >= a) & (rho_loc <= b)
        print("    [%.3e, %.3e]: %3d nascite, DH medio %+.3f, std %.3f" % (a, b, int(s.sum()), DH[s].mean(), DH[s].std()))
    print("  DH per finestra di 1000 tick:")
    for a in range(35000, 46000, 1000):
        s = (ks >= a) & (ks < a + 1000)
        if s.any():
            print("    [%5d, %5d): %3d nascite, DH medio %+.3f, densita' locale media %.3e" % (a, a + 1000, int(s.sum()), DH[s].mean(), rho_loc[s].mean()))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
