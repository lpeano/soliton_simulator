# -*- coding: utf-8 -*-
r"""**LA MONETA E' LA MASSA? La curvatura `c` della camminata a onde lunghe in funzione di `eps`.**

> ### ⛔ **Il task history e' `2026-10-22_moneta_massa.md`.** ### **`eps` SOLO nella scena** *(`_stabilita_lineare.EPS_MONETA` e
> `_triangoli.EPS_MONETA`, in memoria)*; ### **`leggi.yaml` e l'impronta intatti.**

## `--misura 1`: la camminata sola, esatta
Lato `32` e `64`, `eps` `0`, `0.125`, `0.25`, `0.5`, `1`, `2` *(gli stessi alle due taglie: la regola di oggi)*. ### **`c` con la procedura di
`82b40ca1`** *(i `12` rami ordinati lungo `(m, 0)`, i rami `3, 4, 5, 9, 10, 11`, la mediana di `|v_g(1)|/k(1)`)*; ### **e nel settore della
materia** *(`8` rami)*: per ogni ramo dispersivo il fit `omega_b(k) - omega_b(0) = sqrt(Delta^2 + v^2 k^2) - Delta` *(`k <= 0.25 pi`)*.

## `--misura 2`: la lunghezza dell'instabilita' di `S1`
`R2`, `x 0.1`, lato `32`, base proiettata, `N dtau 400`, la norma, a `eps dtau` `0.03125`, `0.0625`, `0.125`; ### **il `k` del massimo contro
`sqrt(2 gamma / c)`** con la `c` della misura `1`.

Gira con:  python csv/_moneta_massa.py --misura 1      (e --misura 2)
"""
import io
import json
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

EPS = float(np.finfo(float).eps)
EPS_LISTA = (0.0, 0.125, 0.25, 0.5, 1.0, 2.0)
TAGLIE = ((32, 0.125), (64, 0.0625))
RAMI = (3, 4, 5, 9, 10, 11)
C_82 = {32: 0.3894, 64: 0.3882}       # 82b40ca1, a eps 0.5
TOLL_C = 1e-4
FIT, MASSA, TAGLIA = 0.05, 0.05, 0.01  # dal mandato
EPS_M2 = (0.25, 0.5, 1.0)             # eps dtau 0.03125, 0.0625, 0.125 a dtau 0.125
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def jl(m):
    return os.path.join(RADICE, "doc", "referti_l2", "moneta_massa_%d.jsonl" % m)


# =====================================================================================
#   MISURA 1
# =====================================================================================
def dispersione(L, dt, eps):
    import _stabilita_lineare as SL
    vero = SL.EPS_MONETA
    SL.EPS_MONETA = eps
    try:
        A, _lin = SL.camminata_complessa(L, dt)
    finally:
        SL.EPS_MONETA = vero
    om_m, _ = SL.fasi(A[..., :8, :8], dt)
    om_v, _ = SL.fasi(A[..., 8:, 8:], dt)
    om = np.sort(np.concatenate([om_m, om_v], axis=-1), axis=-1)
    h = L // 2
    kk = 2.0 * np.pi * np.arange(h + 1) / L
    riga = np.array([om[m % L, 0] for m in range(h + 1)])
    rm = np.array([om_m[m % L, 0] for m in range(h + 1)])
    return kk, np.gradient(riga, kk, axis=0), rm, np.gradient(rm, kk, axis=0)


def fit_massa(kk, y):
    """### `y ~ s (sqrt(Delta^2 + v^2 k^2) - Delta)`: `(Delta, v, scarto relativo massimo)`."""
    from scipy.optimize import curve_fit
    s = 1.0 if y[-1] >= 0 else -1.0
    z = s * y

    def f(k, D, v):
        return np.sqrt(D * D + v * v * k * k) - abs(D)
    try:
        (D, v), _ = curve_fit(f, kk, z, p0=(1.0, 1.0), maxfev=20000)
    except Exception:                                         # noqa: BLE001
        return float("nan"), float("nan"), float("inf")
    D, v = abs(D), abs(v)
    sc = float(np.max(np.abs(f(kk, D, v) - z)) / max(float(np.max(np.abs(z))), 1e-300))
    return D, v, sc


def misura_1():
    out = {}
    for L, dt in TAGLIE:
        k1 = 2.0 * np.pi / L
        for eps in EPS_LISTA:
            kk, vg, rm, vgm = dispersione(L, dt, eps)
            cc = [abs(vg[1, a]) / k1 for a in RAMI if abs(vg[1, a]) > 0.0]
            c_ref = float(np.median(cc)) if cc else float("nan")
            disp = [b for b in range(rm.shape[1]) if float(np.max(np.abs(vgm[:, b]))) > 0.1]
            sel = kk <= 0.25 * np.pi + 1e-12
            fits = []
            for b in disp:
                D, v, sc = fit_massa(kk[sel], rm[sel, b] - rm[0, b])
                gap = float(np.min([abs(rm[0, b] - rm[0, o]) for o in range(rm.shape[1]) if o != b]))
                r21 = float(abs(vgm[2, b] / vgm[1, b])) if vgm[1, b] else float("nan")
                fits.append({"ramo": b, "Delta": D, "v": v, "c_fit": v * v / D if D > 0 else float("inf"),
                             "scarto": sc, "salto_k0": gap, "r21": r21, "c_v1": abs(vgm[1, b]) / k1})
            med = lambda q: float(np.median([f_[q] for f_ in fits])) if fits else float("nan")   # noqa: E731
            r = {"lato": L, "dtau": dt, "eps": eps, "eps_dtau": eps * dt, "c_ref": c_ref,
                 "dispersivi": len(disp), "Delta": med("Delta"), "v": med("v"), "c_fit": med("c_fit"),
                 "scarto_fit": max([f_["scarto"] for f_ in fits], default=float("nan")),
                 "r21": med("r21"), "c_v1": med("c_v1"), "rami": fits}
            r["cDelta"] = r["c_v1"] * r["Delta"]
            out[(L, eps)] = r
            print("  lato %d eps %-5g (eps dtau %.5f): c(82b40ca1) %.4f; materia: %d rami dispersivi, Delta %.5f, v %.5f,"
                  " c=v^2/Delta %.4f, c=v_g(1)/k(1) %.4f, c*Delta %.5f, fit %.3f, v_g(2)/v_g(1) %.3f"
                  % (L, eps, eps * dt, c_ref, len(disp), r["Delta"], r["v"], r["c_fit"], r["c_v1"], r["cDelta"],
                     r["scarto_fit"], r["r21"]))
            sys.stdout.flush()
            with io.open(jl(1), "a", encoding="utf-8") as f_:
                f_.write(json.dumps(r) + "\n")
    print("-" * 100)
    for L, _dt in TAGLIE:
        esito("DEVE RIUSCIRE: lato %d eps 0.5, la c di 82b40ca1 entro %g" % (L, TOLL_C),
              abs(out[(L, 0.5)]["c_ref"] - C_82[L]) <= TOLL_C,
              "%.5f contro %.4f" % (out[(L, 0.5)]["c_ref"], C_82[L]))
    # ### LE LETTURE
    print("### LE LETTURE")
    let = {}
    for L, _dt in TAGLIE:
        pos = [out[(L, e)] for e in EPS_LISTA if e > 0]
        cd = [r["cDelta"] for r in pos]
        dq = [r["Delta"] / r["eps"] for r in pos]
        cost = (max(cd) - min(cd)) / np.mean(cd) <= MASSA
        prop = (max(dq) - min(dq)) / np.mean(dq) <= MASSA
        zero = abs(out[(L, 0.0)]["r21"] - 1.0) <= MASSA
        fitok = all(r["scarto_fit"] <= FIT for r in pos)
        v = "EPS E' LA MASSA" if (cost and prop and zero) else ("NON E' LA MASSA" if not (cost or prop or zero)
                                                               else "PARZIALE")
        print("  lato %d: c*Delta %s (costante entro 5%%? %s); Delta/eps %s (proporzionale? %s); a eps 0 v_g(2)/v_g(1)"
              " %.3f (lineare? %s); il fit entro 5%% a ogni eps > 0? %s -> ### %s"
              % (L, ["%.4f" % x for x in cd], cost, ["%.4f" % x for x in dq], prop, out[(L, 0.0)]["r21"], zero,
                 fitok, v))
        let[L] = {"cDelta": cd, "Delta_su_eps": dq, "costante": bool(cost), "proporzionale": bool(prop),
                  "lineare_a_zero": bool(zero), "fit": bool(fitok), "verdetto": v}
    tag = []
    for e in EPS_LISTA:
        if e > 0:
            a, b = out[(32, e)]["cDelta"], out[(64, e)]["cDelta"]
            tag.append(abs(b - a) / abs(a))
    print("  c*Delta lato 64 contro lato 32, stesso eps: scarti %s -> entro 1%%? %s"
          % (["%.4f" % x for x in tag], all(x <= TAGLIA for x in tag)))
    with io.open(jl(1), "a", encoding="utf-8") as f_:
        f_.write(json.dumps({"letture": {str(k): v for k, v in let.items()}, "taglie": tag}) + "\n")
    return 0


# =====================================================================================
#   MISURA 2
# =====================================================================================
def misura_2():
    import _screening_forme_s3 as SF
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import _triangoli as T
    c1 = {}
    for r in io.open(jl(1), encoding="utf-8"):
        w = json.loads(r)
        if w.get("lato") == 32:
            c1[w["eps"]] = w["c_ref"]
    vecchio = None
    for r in io.open(os.path.join(RADICE, "doc", "referti_l2", "lineare_s1_s4_scala.jsonl"), encoding="utf-8"):
        w = json.loads(r)
        if w.get("forma") == "S1" and w.get("lato") == 32:
            vecchio = np.asarray(w["meta_norm"])
    tab = []
    for eps in EPS_M2:
        t0 = time.time()
        vero = T.EPS_MONETA
        T.EPS_MONETA = eps
        try:
            with SF.forma("S1"):
                b = ST.braccio_proiettato("R2 S1 eps %g" % eps, T.QUADRATO, "Q", SL.EPS_REL, 400.0, 32, 0.125)
        finally:
            T.EPS_MONETA = vero
        g = np.asarray(b["pend"]["meta_norm"])
        i = tuple(int(a) for a in np.unravel_index(int(np.argmax(g)), g.shape))
        km = float(np.sqrt(sum((abs(m if m <= 16 else m - 32) * 2.0 / 32) ** 2 for m in i)))
        kp = float(np.sqrt(2.0 * float(g.max()) / c1[eps]) / np.pi)
        passi = (km - kp) / (2.0 / 32)
        print("  eps %-5g (eps dtau %.5f): gamma %.5f a %s, k misurato %.4f pi, previsto sqrt(2 gamma/c) %.4f pi (c %.4f),"
              " scarto %+.2f passi; uniformita' %.1f ulp; %.0f s" % (eps, eps * 0.125, float(g.max()), i, km, kp, c1[eps],
                                                                     passi, b["uniformita_ulp"], time.time() - t0))
        sys.stdout.flush()
        esito("eps %g: la base <= %g ulp" % (eps, SL.SOGLIA_UNIF), b["uniformita_ulp"] <= SL.SOGLIA_UNIF,
              "%.1f ulp" % b["uniformita_ulp"])
        if eps == 0.5:
            esito("DEVE RIUSCIRE: eps 0.5 ridà S1 lato 32 di cb846b2a AL BIT", bool(np.array_equal(g, vecchio)),
                  "la mappa intera")
        tab.append({"eps": eps, "gamma": float(g.max()), "dove": list(i), "k_misurato": km, "k_previsto": kp,
                    "c": c1[eps], "passi": passi})
        with io.open(jl(2), "a", encoding="utf-8") as f_:
            f_.write(json.dumps(tab[-1]) + "\n")
    segue = all(abs(t_["passi"]) <= 1.0 for t_ in tab)
    print("  ### LA LUNGHEZZA SEGUE c? %s (entro 1 passo per tutti e tre gli eps)" % ("SI'" if segue else "NO"))
    with io.open(jl(2), "a", encoding="utf-8") as f_:
        f_.write(json.dumps({"segue": bool(segue)}) + "\n")
    return 0


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    m = int(argv[argv.index("--misura") + 1])
    print("=" * 100)
    print("LA MONETA E' LA MASSA? -- misura %d" % m)
    print("=" * 100)
    print("  il passo: %d pezzi, impronta %s (intatto); eps SOLO nella scena" % (len(CM.ORDINE), CM.IMPRONTA))
    print("-" * 100)
    sys.stdout.flush()
    io.open(jl(m), "w", encoding="utf-8").close()
    rc = misura_1() if m == 1 else misura_2()
    print("=" * 100)
    print("LA MISURA %d: %d su %d controlli   %s" % (m, OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1]
                                                   else "### CI SONO BUCHI"))
    print("=" * 100)
    return rc or (0 if OK[0] == OK[1] else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
