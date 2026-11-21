# -*- coding: utf-8 -*-
r"""**IL FLUSSO DI B NELLA PLACCHETTA, SOLO MISURA** *(Luca `2026-11-17` `19:40`; la carta `doc/TASK_HISTORY/2026-11-17_flusso_placchetta.md`)*. [[PROGETTO-U1]]

    E:\python\py3132\python.exe doc/referti_l2/flusso_placchetta.py > doc/referti_l2/flusso_placchetta.txt

**La definizione:** per ogni placchetta `p` *(triangolo antiorario)* **`Phi_p = e * somma sul bordo di +-A_a`** *(`e = p6_u_breve.E_DECISO`)*; il valore GREZZO e quello ridotto in `(-pi, pi]`; il quanto `|Phi_p| = 2 pi`. **Il campo delle corse e' NON COMPATTO** *(la carta, sez. `1`)*.
**Le placchette costruite QUI dal reticolo** *(`su`: `v -> v+a1 -> v+a1+a2`; `giu`: `v -> v+a1+a2 -> v+a2`; l'arco `x -> y` col segno `+` se e' `3x + a` verso `y`, `-` se e' l'arco di `y` verso `x`)*, **e K4 le confronta con `e * _u1_prototipo.Campo.B()`.**
**Gli stati:** `E:/soliton_simulator/controllo/<C1|C2>/stato_<k>.npz` *(`campo_A`, `meta["centro"]`)*, `k = 250 ... 3000`; **`k 0`: `A = 0` per costruzione** *(`porto.campi`)*. **Nessuna corsa, nessuna scena:** il toro `L 186` dai suoi indici.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_QUI, _SOL, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)

L = 186
DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
STATI = tuple(range(250, 3001, 250))
R_MATERIA, CONFINE = 12.4, 23.81


def placchette(L):
    """### `(P, S, off)`: le placchette `su` (prime `n`) e `giu` (ultime `n`), gli archi e i segni costruiti dai vicini; `off` lo scarto del baricentro dal nodo `v` (in `m1, m2`)."""
    n = L * L
    v = np.arange(n)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L

    def arco(x, a):          # ### l'arco a (0: a1, 1: a2, 2: a1 + a2) che parte da x
        return 3 * x + a
    v1, v2, v12 = nb(1, 0), nb(0, 1), nb(1, 1)
    # su: v -> v+a1 (a1 da v, +), v+a1 -> v+a1+a2 (a2 da v+a1, +), v+a1+a2 -> v (a1+a2 da v, -)
    su_P = np.stack([arco(v, 0), arco(v1, 1), arco(v, 2)], axis=1)
    su_S = np.tile([1.0, 1.0, -1.0], (n, 1))
    # giu: v -> v+a1+a2 (a1+a2 da v, +), v+a1+a2 -> v+a2 (a1 da v+a2, -), v+a2 -> v (a2 da v, -)
    giu_P = np.stack([arco(v, 2), arco(v2, 0), arco(v, 1)], axis=1)
    giu_S = np.tile([1.0, -1.0, -1.0], (n, 1))
    assert np.array_equal(nb(1, 0)[v2], v12)
    P = np.concatenate([su_P, giu_P])
    S = np.concatenate([su_S, giu_S])
    off = np.concatenate([np.tile([2.0 / 3.0, 1.0 / 3.0], (n, 1)), np.tile([1.0 / 3.0, 2.0 / 3.0], (n, 1))])
    return P, S, off


def phi(A, P, S, e):
    return e * (A[P[:, 0]] * S[:, 0] + A[P[:, 1]] * S[:, 1] + A[P[:, 2]] * S[:, 2])


def ridotto(x):
    return np.angle(np.exp(1j * x))


def carica(nome, k):
    f = os.path.join(DIR, nome, "stato_%05d.npz" % k)
    with np.load(f) as d:
        return d["campo_A"].copy(), json.loads(str(d["meta"]))["centro"]


def retta(x, y):
    X = np.vstack([x, np.ones_like(x)]).T
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ c
    sig = float(np.sqrt(np.sum(res ** 2) / max(len(x) - 2, 1)))
    return float(c[0]), sig / float(np.sqrt(np.sum((x - x.mean()) ** 2))), float(c[1])


def main():
    import _presidio
    import _u1_prototipo as U1
    import p6_u_breve as PB
    from solitone import toro as TO
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL FLUSSO DI B NELLA PLACCHETTA (Luca 2026-11-17 19:40): Phi_p = e * somma +-A sul bordo, sugli stati di C1 e C2")
    print("=" * 130)
    e = PB.E_DECISO
    print("### e = %r; la forma del campo delle corse: %s (g = B / AREA: la spinta usa B, non sin B)" % (e, PB.FORMA))
    P, S, off = placchette(L)
    n = L * L
    v = np.arange(n)
    m1, m2 = (v // L).astype(float), (v % L).astype(float)
    pm1 = np.concatenate([m1, m1]) + off[:, 0]
    pm2 = np.concatenate([m2, m2]) + off[:, 1]
    esiti = []
    # ------------------------------------------------------------------ K1
    A0 = np.zeros(3 * n)           # ### l'array di porto.campi a k 0 (A = 0 per costruzione)
    f0 = phi(A0, P, S, e)
    print("K1: A = 0 (k 0, porto.campi): Phi diverso da 0 su %d placchette su %d" % (int(np.sum(f0 != 0)), f0.size))
    esiti.append(("K1: A = 0 -> Phi = 0 al bit su tutte le placchette", bool(np.all(f0 == 0.0))))
    # ------------------------------------------------------------------ K2, K3, K4 sugli stati
    rng = np.random.default_rng(0)
    c = U1.Campo(np.repeat(v, 3), np.stack([((v // L + 1) % L) * L + v % L, (v // L) * L + (v % L + 1) % L, ((v // L + 1) % L) * L + (v % L + 1) % L], axis=1).reshape(-1), (L, L), e, PB.FORMA, np.ones(3 * n))
    out = {}
    k2, k4 = [], []
    for nome in ("C2", "C1"):
        out[nome] = {}
        for k in STATI:
            A, centro = carica(nome, k)
            f = phi(A, P, S, e)
            out[nome][k] = (f, centro)
            k2.append(abs(float(np.sum(f))) / max(float(np.sum(np.abs(f))), 1e-300))
            c.A[...] = A
            k4.append(float(np.max(np.abs(f - e * np.concatenate([c.B()[:n], c.B()[n:]])))) / max(float(np.max(np.abs(f))), 1e-300))
    print("K2: |somma Phi| / somma |Phi| su ogni stato: massimo %.3e" % max(k2))
    esiti.append(("K2: la somma di Phi su tutte le placchette = 0 entro l'arrotondamento (|somma| / somma|.| sotto 1e-12)", max(k2) <= 1e-12))
    print("K4: max |Phi (le placchette di qui) - e * Campo.B()| / max |Phi|, su ogni stato: massimo %.3e" % max(k4))
    esiti.append(("K4: Phi = e * Campo.B() (il rotore del codice) entro 1e-12 relativo", max(k4) <= 1e-12))
    A, _c = carica("C2", 3000)
    f = phi(A, P, S, e)
    chi = float(np.std(A)) * rng.standard_normal(n)
    ii = np.repeat(v, 3)
    jj = c.jj
    Ag = A + chi[jj] - chi[ii]
    dg = float(np.max(np.abs(phi(Ag, P, S, e) - f))) / float(np.max(np.abs(f)))
    A1_ = A.copy()
    A1_[0] += float(np.std(A))
    d1 = float(np.max(np.abs(phi(A1_, P, S, e) - f))) / float(np.max(np.abs(f)))
    print("K3: la trasformazione di gauge a caso (seme 0, chi della scala di A): max |Delta Phi| / max |Phi| = %.3e; DEVE FALLIRE, un arco solo cambiato: %.3e" % (dg, d1))
    esiti.append(("K3 (P-B4): Phi invariato per gauge entro 1e-12 relativo (C2 k 3000)", dg <= 1e-12))
    esiti.append(("K3, DEVE FALLIRE: un arco solo cambiato muove Phi oltre 1e-12", d1 > 1e-12))
    # ------------------------------------------------------------------ M1-M4
    print("-" * 130)
    serie = {}
    for nome in ("C2", "C1"):
        print("%s:" % nome)
        mx, med_an, dove = [], [], []
        for k in STATI:
            f, centro = out[nome][k]
            D = TO.scarti(pm1, pm2, centro[0], centro[1], L)
            r = np.hypot(D[:, 0], D[:, 1])
            a = np.abs(f)
            i = int(np.argmax(a))
            an = np.floor(r).astype(int)
            mean_an = np.bincount(an, weights=a) / np.maximum(np.bincount(an), 1)
            mx.append(float(a.max()))
            dove.append(float(r[i]))
            med_an.append(mean_an)
            fr = ridotto(f)
            su, giu = slice(0, n), slice(n, 2 * n)
            if k in (250, 1500, 3000):
                print("  k %4d: max |Phi| grezzo %.6e (ridotto %.6e) a r %.2f (%s); il segno medio %+.3e; |Phi| medio %.3e" % (
                    k, float(a.max()), float(np.max(np.abs(fr))), float(r[i]), "su" if i < n else "giu", float(np.mean(np.sign(f))), float(a.mean())))
                for nm_, sl in (("su", su), ("giu", giu)):
                    ms = np.bincount(an[sl], weights=a[sl], minlength=an.max() + 1) / np.maximum(np.bincount(an[sl], minlength=an.max() + 1), 1)
                    mxs = np.zeros(an.max() + 1)
                    np.maximum.at(mxs, an[sl], a[sl])
                    print("     %-3s anelli 0..45 (media, massimo): %s" % (nm_, "  ".join("%d: %.2e %.2e" % (j, ms[j], mxs[j]) for j in range(0, 46, 3))))
            else:
                print("  k %4d: max |Phi| %.6e a r %.2f; |Phi| medio %.3e" % (k, float(a.max()), float(r[i]), float(a.mean())))
        serie[nome] = (np.array(mx), np.array(dove), med_an)
        ks = np.array(STATI, dtype=float)
        p, ep, _q = retta(ks, np.array(mx))
        ian = int(np.argmax(med_an[-1]))
        ya = np.array([x[ian] if ian < len(x) else 0.0 for x in med_an])
        pa, epa, _qa = retta(ks, ya)

        def verdetto(p_, e_):
            return "CRESCE" if p_ > 3 * e_ else ("CALA" if p_ < -3 * e_ else "RESTA")
        print("  M2: max |Phi| contro k: la pendenza %+.4e +- %.1e per tick (%s); |Phi| medio all'anello %d (il massimo a k 3000): %+.4e +- %.1e (%s)" % (p, ep, verdetto(p, ep), ian, pa, epa, verdetto(pa, epa)))
        m3 = float(np.max(mx)) / (2 * math.pi)
        txt = "M3: max |Phi| / 2 pi = %.4e" % m3
        if p > 3 * ep:
            t = (2 * math.pi - mx[-1]) / p
            txt += "; al ritmo di M2 il primo quanto a k 3000 + %.4e tick (fra %.4e e %.4e con +- un errore)" % (t, (2 * math.pi - mx[-1]) / (p + ep), (2 * math.pi - mx[-1]) / max(p - ep, 1e-300))
        print("  " + txt)
        if nome == "C2":
            esiti.append(("P-B1: in C2 max |Phi| sotto 1e-2 rad su tutti gli stati (%.3e)" % max(mx), max(mx) < 1e-2))
            esiti.append(("P-B2: il massimo entro 25 nodi dal baricentro su tutti gli stati (C2: le distanze da %.2f a %.2f)" % (min(dove), max(dove)), max(dove) <= 25.0))
    m2_, m1_ = serie["C2"][0], serie["C1"][0]
    rel = np.abs(m1_ - m2_) / m2_
    print("M4: C1 contro C2, |max|Phi|_C1 - max|Phi|_C2| / max|Phi|_C2 per stato: %s" % "  ".join("k %d: %.3e" % (k, x) for k, x in zip(STATI, rel)))
    esiti.append(("P-B3: C1 e C2 entro il 10%% su max |Phi| a ogni stato (il massimo %.3e)" % float(rel.max()), bool(np.all(rel < 0.10))))
    # ------------------------------------------------------------------ M5
    figura(out["C2"][3000], pm1, pm2)
    print("M5: la mappa di Phi a k 3000 (C2): flusso_placchetta.png")
    print("### l'ALIASING (dichiarato): gli stati ogni 250 tick; un'oscillazione di A piu' veloce di 500 tick NON si vede")
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0


def figura(fc, pm1, pm2):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from solitone import toro as TO
    f, centro = fc
    D = TO.scarti(pm1, pm2, centro[0], centro[1], L)
    r = np.hypot(D[:, 0], D[:, 1])
    sel = r <= 60.0
    m = float(np.max(np.abs(f[sel])))
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    sc = ax.scatter(D[sel, 0], D[sel, 1], c=f[sel], s=1.5, cmap="RdBu_r", vmin=-m, vmax=m)
    t = np.linspace(0, 2 * math.pi, 400)
    for R, st, nm in ((R_MATERIA, "--", "il raggio della materia 12.4"), (CONFINE, "-", "il confine dell'energia 23.81")):
        ax.plot(R * np.cos(t), R * np.sin(t), st, color="black", lw=0.9, label=nm)
    ax.set_aspect("equal")
    ax.set_title("Phi_p = e * somma A a k 3000 (C2); 2 pi = %.3f" % (2 * math.pi))
    ax.legend(loc="upper right", fontsize=8)
    fig.colorbar(sc, ax=ax, label="Phi (rad)")
    fig.savefig(os.path.join(_QUI, "flusso_placchetta.png"), dpi=110)


if __name__ == "__main__":
    sys.exit(main())
