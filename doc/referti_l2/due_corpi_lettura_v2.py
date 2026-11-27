# -*- coding: utf-8 -*-
r"""**[M2330] LE LETTURE DEL MODELLO INTERO, LA V2: d/dy COI NODI GIUSTI** *(errore mio, dichiarato in `3e138a1b`: `A2 = (-1/2, sqrt3/2)`; i nodi `(m1 -+ 1, m2 +- 2)` della v1 stavano a `(-+2, +-sqrt3)`; i giusti sono `(m1 + 1, m2 + 2)` e `(m1 - 1, m2 - 2)`; in piu' il caso noto `q x -> J_y = 0`; `due_corpi_lettura.py` e' usato e non si riscrive)*. **IL RESTO, la v1:** *(DECISIONE DI LUCA, 2026-11-24 23:30; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-quindecies`; solo letture sugli stati e sulle serie di `M2330/d1, d2, d3`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_lettura_v2.py > doc/referti_l2/due_corpi_fondo_v2.txt

**(i)** dalla serie ogni `10` tick: `d(k)` = la distanza fra i baricentri dei due corpi *(nel riferimento della corsa: gli scarti dal centro della coppia a `k 0`)*; per finestra di `1000` il fit `d = c0 + c1 k + a k^2/2` *(`caduta_finestre.fit` sulla colonna della distanza)*; `a < 0` = si avvicinano. **(ii)** `J_phi` come in `vento_vuoto_v2` *(la fase acquistata da `k 0` della stessa corsa, il prodotto in reali)*, `J_x` coi nodi `(m1 +- 1, m2)`, `J_y` coi nodi a `+- sqrt3` lungo `y`; **la componente radiale** `J . r_hat` dal baricentro del corpo, mediata sugli anelli `[8, 16)` e `[16, 32)` dentro la meta' del corpo; **negativa = verso l'oggetto**. **(iii)** `rho_phi` sugli stessi anelli. **(iv)** `chi` sugli anelli `[0, 4)`, `[4, 8)`, `[8, 16)`, `[16, 32)`; la profondita' = la media su `[0, 4)`. **(v)** `w` di ogni corpo = il raggio quadratico medio di `rho_psi` nella sua meta' *(`sqrt(somma rho d^2 / somma rho)`)*; `omega` per tick dalla serie, la media per finestra di `250`; il respiro = `(w_max - w_min)/w_medio` sui `25` stati.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import vento_vuoto_v2 as VV2  # noqa: E402

VV = VV2.VV
PF = VV.PF
BASE = os.path.join(PF.CTRL, "M2330")
CORSE = (("d1", 2), ("d2", 2), ("d3", 1))
KS = list(range(0, 6001, 250))
FIN = [(k, k + 1000) for k in range(0, 6000, 1000)]
ANELLI_J = ((8.0, 16.0), (16.0, 32.0))
ANELLI_CHI = ((0.0, 4.0), (4.0, 8.0), (8.0, 16.0), (16.0, 32.0))
S3 = math.sqrt(3.0)


def leggi(f):
    PF.controlla(f)
    with np.load(f) as z:
        return {k: z[k].copy() for k in z.files}


def fit_d(k, d, k0, k1):
    """### `(a, sigma_a, n)`: il fit quadratico di `d(k)` su `[k0, k1]` *(le righe di `caduta_finestre.fit`)*."""
    m = (k >= k0) & (k <= k1)
    kk, y = k[m], d[m]
    A = np.stack([np.ones_like(kk), kk, 0.5 * kk * kk], axis=1)
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - A @ c
    cov = float(np.sum(r ** 2) / (len(kk) - 3)) * np.linalg.inv(A.T @ A)
    return float(c[2]), math.sqrt(cov[2, 2]), int(m.sum())


def main():
    import _presidio
    from solitone import toro as TO
    VV.V3.avvia()
    for m in ("vento_vuoto.py", "vento_vuoto_v2.py", "due_corpi_fondo.py", "due_corpi_lettura.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2330] LE LETTURE DEL MODELLO INTERO (la carta sez. 3-quindecies): d1 due oggetti chi on, d2 due chi off, d3 uno chi on; 6000 tick")
    print("=" * 130)
    with VV.F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        Z["metti"]()
    su = ((m1 + 1) % L) * L + (m2 + 2) % L
    giu = ((m1 - 1) % L) * L + (m2 - 2) % L
    dx_p = ((m1 + 1) % L) * L + m2
    sx_m = ((m1 - 1) % L) * L + m2
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    S = {}
    for c, q in CORSE:
        f = os.path.join(BASE, c, "serie.json")
        PF.controlla(f)
        S[c] = json.load(open(f, encoding="utf-8"))
    X0 = {c: leggi(os.path.join(BASE, c, "stato_000000.npz")) for c, _q in CORSE}
    esito("(Luca) d2 a k 0 = d1 a k 0 AL BIT (psi_h, phi_h, chi, pi)", all(np.array_equal(X0["d1"][x], X0["d2"][x]) for x in ("psi_h", "phi_h", "chi", "pi")))
    R = {}
    for c, q in CORSE:
        meta = S[c]["meta"]
        b = meta["centro_coppia"]
        dxy = np.asarray(TO.scarti(m1, m2, b[0], b[1], L))[:, :2]
        masch = [np.ones(n, bool)] if q == 1 else [dxy[:, 1] < 0.0, dxy[:, 1] >= 0.0]
        phi0 = X0[c]["phi_h"]
        R[c] = {}
        for k in KS:
            X = X0[c] if k == 0 else leggi(os.path.join(BASE, c, "stato_%06d.npz" % k))
            rpsi = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
            rho, Zn = VV2.per_nodo(X["phi_h"], phi0, nodo, n)
            Jy = rho * VV.dtheta_dy(Zn, su, giu)
            Jx = rho * np.angle(np.conj(Zn[sx_m]) * Zn[dx_p]) / 2.0
            corpi = []
            for mm in masch:
                w = rpsi * mm
                cb = (dxy * w[:, None]).sum(axis=0) / w.sum()
                r = np.hypot(dxy[:, 0] - cb[0], dxy[:, 1] - cb[1])
                rx, ry = (dxy[:, 0] - cb[0]) / np.maximum(r, 1e-300), (dxy[:, 1] - cb[1]) / np.maximum(r, 1e-300)
                Jr = Jx * rx + Jy * ry
                an = lambda a_, b_: mm & (r >= a_) & (r < b_)  # noqa: E731
                corpi.append(dict(
                    b=cb, w=float(math.sqrt(np.sum(w * r * r) / w.sum())),
                    Jr=[float(Jr[an(a_, b_)].mean()) for a_, b_ in ANELLI_J],
                    rphi=[float(rho[an(a_, b_)].mean()) for a_, b_ in ANELLI_J],
                    chi=[float(X["chi"][an(a_, b_)].mean()) for a_, b_ in ANELLI_CHI]))
            R[c][k] = corpi
        sr = np.array(S[c]["serie"])
        esito("(%s) il baricentro di k 0 riletto dallo stato = la serie a k 0 AL BIT" % c, all(R[c][0][j]["b"][0] == sr[0, 1 + 3 * j] and R[c][0][j]["b"][1] == sr[0, 2 + 3 * j] for j in range(q)))
        esito("(%s) J radiale di k 0 (la fase rispetto a se stessa) = 0 AL BIT" % c, all(x == 0.0 for j in range(q) for x in R[c][0][j]["Jr"]))
    # ### il segno del radiale: una fase q r attorno al corpo 1 di d1 da' J_r = + rho q (uscente positivo)
    b1 = R["d1"][0][0]["b"]
    b = S["d1"]["meta"]["centro_coppia"]
    dxy = np.asarray(TO.scarti(m1, m2, b[0], b[1], L))[:, :2]
    rr = np.hypot(dxy[:, 0] - b1[0], dxy[:, 1] - b1[1])
    qq = 0.05
    f0 = X0["d1"]["phi_h"]
    rho, Zq = VV2.per_nodo(f0 * np.exp(1j * qq * rr[nodo]), f0, nodo, n)
    Jy = rho * VV.dtheta_dy(Zq, su, giu)
    Jx = rho * np.angle(np.conj(Zq[sx_m]) * Zq[dx_p]) / 2.0
    an = (rr >= 8.0) & (rr < 16.0)
    Jr = (Jx * (dxy[:, 0] - b1[0]) + Jy * (dxy[:, 1] - b1[1])) / np.maximum(rr, 1e-300)
    rap = float(Jr[an].mean() / (rho[an].mean() * qq))
    esito("(segno) una fase uscente q r: J radiale su [8, 16) = + rho q entro il 5% (uscente POSITIVO)", abs(rap - 1.0) < 0.05, "il rapporto %.4f" % rap)
    esito("(segno) DEVE FALLIRE: la stessa fase da' J radiale NEGATIVO", not (rap < 0.0), "")
    xx = (m1 - 0.5 * m2).astype(float)
    qx = 2.0 * math.pi * 2.0 / L
    _r, Zx = VV2.per_nodo(f0 * np.exp(1j * qx * xx[nodo]), f0, nodo, n)
    jy = float(np.max(np.abs(VV.dtheta_dy(Zx, su, giu))))
    jyv = float(np.max(np.abs(VV.dtheta_dy(Zx, ((m1 - 1) % L) * L + (m2 + 2) % L, ((m1 + 1) % L) * L + (m2 - 2) % L))))
    esito("(x) una fase q x (2 giri su L): d theta/dy = 0 entro 1e-12 coi nodi giusti", jy < 1e-12, "%.1e" % jy)
    esito("(x) DEVE FALLIRE lo zero coi nodi della v1", jyv > 1e-6, "%.1e" % jyv)
    print("-" * 130)
    print("(i) LA DISTANZA FRA I BARICENTRI d(k) E LA SUA ACCELERAZIONE (a < 0: si avvicinano)")
    print("-" * 130)
    D = {}
    for c in ("d1", "d2"):
        sr = np.array(S[c]["serie"])
        k = sr[:, 0]
        d = np.hypot(sr[:, 4] - sr[:, 1], sr[:, 5] - sr[:, 2])
        D[c] = (k, d)
        print("  %s: d(0) %.6f; d(1000) %.6f; d(2000) %.6f; d(3000) %.6f; d(4000) %.6f; d(5000) %.6f; d(6000) %.6f; d(6000) - d(0) %+.6f" % (
            c, *[float(d[k == x][0]) for x in range(0, 6001, 1000)], float(d[-1] - d[0])))
    for k0, k1 in FIN + [(0, 6000)]:
        a1, s1, _ = fit_d(*D["d1"], k0, k1)
        a2, s2, _ = fit_d(*D["d2"], k0, k1)
        print("  [%4d, %4d]: a(d1) %+.4e +- %.1e;  a(d2) %+.4e +- %.1e;  a(d1) - a(d2) %+.4e +- %.1e (%.1f sigma)" % (k0, k1, a1, s1, a2, s2, a1 - a2, math.hypot(s1, s2), abs(a1 - a2) / math.hypot(s1, s2)))
    print("-" * 130)
    print("(ii) J_phi RADIALE (negativo = verso l'oggetto) e (iii) rho_phi, sugli anelli [8,16) e [16,32), per corpo e per stato")
    print("-" * 130)
    for c, q in CORSE:
        for j in range(q):
            r0 = R[c][0][j]["rphi"]
            for k in KS:
                x = R[c][k][j]
                print("  %s corpo %d k %4d: J_r %+.4e %+.4e;  rho_phi %.6f (%+.3f%%) %.6f (%+.3f%%)" % (c, j + 1, k, x["Jr"][0], x["Jr"][1], x["rphi"][0], 100 * (x["rphi"][0] / r0[0] - 1), x["rphi"][1], 100 * (x["rphi"][1] / r0[1] - 1)))
    print("-" * 130)
    print("(iv) chi SUGLI ANELLI [0,4), [4,8), [8,16), [16,32) per corpo e per stato; la profondita' = [0,4)")
    print("-" * 130)
    for c, q in CORSE:
        for j in range(q):
            p0 = R[c][0][j]["chi"][0]
            for k in KS:
                x = R[c][k][j]["chi"]
                print("  %s corpo %d k %4d: chi %+.6e %+.6e %+.6e %+.6e;  la profondita' rispetto a k 0 %+.3f%%" % (c, j + 1, k, x[0], x[1], x[2], x[3], 100 * (x[0] / p0 - 1) if p0 != 0 else float("nan")))
    print("-" * 130)
    print("(v) w DI OGNI CORPO (il raggio quadratico medio nella sua meta') E omega PER FINESTRA DI 250; il respiro (w_max - w_min)/w_medio")
    print("-" * 130)
    for c, q in CORSE:
        om = S[c]["omega"]
        for j in range(q):
            ws = [R[c][k][j]["w"] for k in KS]
            o = np.array(om[j])
            print("  %s corpo %d: w %s" % (c, j + 1, " ".join("%.3f" % w for w in ws)))
            print("           omega (media per 250) %s" % " ".join("%+.6f" % float(o[i:i + 250].mean()) for i in range(0, len(o), 250)))
            print("  ### %s corpo %d: il respiro %.4f (%s del 10%%)" % (c, j + 1, (max(ws) - min(ws)) / float(np.mean(ws)), "sotto" if (max(ws) - min(ws)) / float(np.mean(ws)) < 0.10 else "SOPRA"))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
