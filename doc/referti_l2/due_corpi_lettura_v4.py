# -*- coding: utf-8 -*-
r"""**[M0024] LA LETTURA DI d1', d2', d3' COL CRITERIO C', I NUMERI SEMPRE, D2'** *(DECISIONE DI LUCA, 2026-11-27 `00:24`; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-vicies` e il suo seguito, scritta PRIMA; `due_corpi_lettura_v3.py` e' usato e non si tocca: la v4 lo importa per i riferimenti e per le finestre)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_lettura_v4.py > doc/referti_l2/due_corpi_fondo_v6_C.txt

**L'ordine:** N1, (R) sul giro 3, le finestre valide di d3' *(C': `omega` medio e pozzo medio per finestra di `500`; `w` medio sui periodi `[0, 2500]`, `[2500, 5000]`, `[3500, 6000]` entro il `10%` di `4.60`)*, i numeri N per tutte e tre, `d(k)` per finestra per d1' e d2' col verso, poi **il verdetto D2'** per finestra valida: `|Delta d(d1')| > 3 |Delta d(d2')|` **e lo stesso segno di d2'** *(la lettura letterale di «nello stesso verso»; il caso col verso opposto si stampa a parte, fuori dalla regola)*.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_lettura_v3 as L3  # noqa: E402

L2, FPC, VV2, VV, PF = L3.L2, L3.FPC, L3.VV2, L3.VV, L3.PF
BASE, GIRO3, FIN, KS = L3.BASE, L3.GIRO3, L3.FIN, L3.KS
PERIODI = [(0, 2500), (2500, 5000), (3500, 6000)]
RIF_WP, TOL_WP = 4.60, 0.10
CORSE = (("d1", 2), ("d2", 2), ("d3", 1))


def ok_om(x):
    return abs(x / L3.RIF_OM - 1.0) < L3.TOL_OM


def ok_pz(x):
    return abs(x / L3.RIF_POZZO - 1.0) < L3.TOL_POZZO


def ok_wp(x):
    return abs(x / RIF_WP - 1.0) < TOL_WP


def main():
    import _presidio
    VV.V3.avvia()
    for m in ("vento_vuoto.py", "vento_vuoto_v2.py", "due_corpi_lettura_v2.py", "fondo_puntofisso_chi.py", "due_corpi_lettura_v3.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0024] LA LETTURA COL CRITERIO C' (la carta sez. 3-vicies, il seguito): d1' due chi on, d2' due chi off, d3' uno chi on; 6000 tick")
    print("=" * 130)
    with VV.F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        Z["metti"]()
    ZG = {"m1": m1, "m2": m2, "L": L}
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))

    def rho_psi(X):
        return np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
    fg = os.path.join(GIRO3, "giro.json")
    PF.controlla(fg)
    G = json.load(open(fg, encoding="utf-8"))
    X5 = L2.leggi(os.path.join(GIRO3, "stato_000500.npz"))
    r5 = rho_psi(X5)
    w5, p5 = FPC.w_di(r5, L), FPC.profondita(ZG, r5, X5["chi"])
    esito("(N1) w_di e profondita sul giro 3 a k 500 = giro.json [5] AL BIT", w5 == G["w"][5] and p5 == G["profondita"][5], "%.15g %.15g" % (w5, p5))
    print("-" * 130)
    print("(R) IL GIRO 3 DI RIFERIMENTO CONTRO C'")
    print("-" * 130)
    gw = {p: float(np.mean(G["w"][p[0] // 100:p[1] // 100 + 1])) for p in PERIODI}
    for p in PERIODI:
        print("  il periodo [%4d, %4d]: w medio %.4f (%+.2f%% di %.2f, %s)" % (*p, gw[p], 100 * (gw[p] / RIF_WP - 1), RIF_WP, "si" if ok_wp(gw[p]) else "NO"))
    gn = 0
    for k0, k1 in FIN:
        om, pz = float(np.mean(G["omega"][k0:k1])), float(np.mean(G["profondita"][k0 // 100:k1 // 100 + 1]))
        gn += ok_om(om) and ok_pz(pz)
        print("  [%4d, %4d]: omega %.6f (%s); il pozzo medio %.3f (%s)" % (k0, k1, om, "si" if ok_om(om) else "NO", pz, "si" if ok_pz(pz) else "NO"))
    esito("(R) il giro 3: w su [3500, 6000] entro il 10%% di 4.60, e omega e pozzo su 12 finestre su 12", ok_wp(gw[(3500, 6000)]) and gn == 12, "w %.4f; %d su 12" % (gw[(3500, 6000)], gn))
    print("-" * 130)
    print("IL CONTROLLO d3' CON C'")
    print("-" * 130)
    S = {}
    for c, _q in CORSE:
        f = os.path.join(BASE, c, "serie.json")
        PF.controlla(f)
        S[c] = json.load(open(f, encoding="utf-8"))
    om3 = np.array(S["d3"]["omega"][0])
    W3, P3 = {}, {}
    for k in KS:
        X = L2.leggi(os.path.join(BASE, "d3", "stato_%06d.npz" % k))
        r = rho_psi(X)
        W3[k], P3[k] = FPC.w_di(r, L), FPC.profondita(ZG, r, X["chi"])
    pv = []
    for p in PERIODI:
        wm = float(np.mean([W3[k] for k in KS if p[0] <= k <= p[1]]))
        if ok_wp(wm):
            pv.append(p)
        print("  il periodo [%4d, %4d]: w medio %.4f (%+.2f%% di %.2f)  ->  %s" % (*p, wm, 100 * (wm / RIF_WP - 1), RIF_WP, "VALIDO" if ok_wp(wm) else "non valido"))
    VAL = []
    for k0, k1 in FIN:
        om, pz = float(om3[k0:k1].mean()), float(np.mean([P3[k0], P3[k0 + 250], P3[k1]]))
        dentro = [p for p in pv if p[0] <= k0 and k1 <= p[1]]
        ok = ok_om(om) and ok_pz(pz) and bool(dentro)
        if ok:
            VAL.append((k0, k1))
        print("  [%4d, %4d]: omega %.6f (%s); il pozzo medio %.3f (%s); dentro un periodo valido: %s  ->  %s" % (
            k0, k1, om, "si" if ok_om(om) else "NO", pz, "si" if ok_pz(pz) else "NO", dentro if dentro else "NO", "VALIDA" if ok else "non valida"))
    print("  ### LE FINESTRE VALIDE DI d3' (C'): %d su %d  %s" % (len(VAL), len(FIN), VAL))
    print("-" * 130)
    print("N. I NUMERI PER TUTTE E TRE, sui 25 stati: J_r e rho_phi su [8,16) [16,32); chi su [0,4) [4,8) [8,16) [16,32); w (raggio quadratico medio nella meta'); omega medio dei 250 prima")
    print("-" * 130)
    from solitone import toro as TO
    su = ((m1 + 1) % L) * L + (m2 + 2) % L
    giu = ((m1 - 1) % L) * L + (m2 - 2) % L
    dx_p = ((m1 + 1) % L) * L + m2
    sx_m = ((m1 - 1) % L) * L + m2
    for c, q in CORSE:
        b = S[c]["meta"]["centro_coppia"]
        dxy = np.asarray(TO.scarti(m1, m2, b[0], b[1], L))[:, :2]
        masch = [np.ones(n, bool)] if q == 1 else [dxy[:, 1] < 0.0, dxy[:, 1] >= 0.0]
        X0 = L2.leggi(os.path.join(BASE, c, "stato_000000.npz"))
        phi0 = X0["phi_h"]
        oms = [np.array(o) for o in S[c]["omega"]]
        for k in KS:
            X = X0 if k == 0 else L2.leggi(os.path.join(BASE, c, "stato_%06d.npz" % k))
            rpsi = rho_psi(X)
            rho, Zn = VV2.per_nodo(X["phi_h"], phi0, nodo, n)
            Jy = rho * VV.dtheta_dy(Zn, su, giu)
            Jx = rho * np.angle(np.conj(Zn[sx_m]) * Zn[dx_p]) / 2.0
            for j, mm in enumerate(masch):
                w = rpsi * mm
                cb = (dxy * w[:, None]).sum(axis=0) / w.sum()
                r = np.hypot(dxy[:, 0] - cb[0], dxy[:, 1] - cb[1])
                rx, ry = (dxy[:, 0] - cb[0]) / np.maximum(r, 1e-300), (dxy[:, 1] - cb[1]) / np.maximum(r, 1e-300)
                Jr = Jx * rx + Jy * ry
                an = lambda a_, b_: mm & (r >= a_) & (r < b_)  # noqa: E731
                o = float(oms[j][k - 250:k].mean()) if k > 0 else float(oms[j][0])
                print("  %s corpo %d k %4d: J_r %s;  rho_phi %s;  chi %s;  w %.4f;  omega %+.6f" % (
                    c, j + 1, k, " ".join("%+.4e" % float(Jr[an(a_, b_)].mean()) for a_, b_ in L2.ANELLI_J),
                    " ".join("%.6f" % float(rho[an(a_, b_)].mean()) for a_, b_ in L2.ANELLI_J),
                    " ".join("%+.4e" % float(X["chi"][an(a_, b_)].mean()) for a_, b_ in L2.ANELLI_CHI),
                    math.sqrt(float(np.sum(w * r * r) / w.sum())), o))
    print("-" * 130)
    print("N. d(k) PER FINESTRA DI 500, d1' E d2' (Delta d < 0 = VERSO); a dal fit di due_corpi_lettura_v2")
    print("-" * 130)
    D = {}
    for c in ("d1", "d2"):
        sr = np.array(S[c]["serie"])
        D[c] = (sr[:, 0], np.hypot(sr[:, 4] - sr[:, 1], sr[:, 5] - sr[:, 2]))

    def dd(c, k0, k1):
        k, d = D[c]
        return float(d[k == k0][0]), float(d[k == k1][0])
    for k0, k1 in FIN + [(0, 6000)]:
        riga = []
        for c in ("d1", "d2"):
            a0, a1 = dd(c, k0, k1)
            a, s, _ = L2.fit_d(*D[c], k0, k1)
            riga.append("%s' d %.6f -> %.6f, Delta %+.6f (%s), a %+.3e +- %.1e" % (c, a0, a1, a1 - a0, "VERSO" if a1 < a0 else "VIA", a, s))
        print("  [%4d, %4d]: %s;  %s" % (k0, k1, riga[0], riga[1]))
    z0, z1 = dd("d2", 0, 6000)
    print("  ### LA DERIVA DI d2' (chi off) su [0, 6000]: %+.6f nodi, %s" % (z1 - z0, "VERSO" if z1 < z0 else "VIA"))
    print("-" * 130)
    print("IL VERDETTO D2' SULLE FINESTRE VALIDE: |Delta d(d1')| > 3 |Delta d(d2')| e lo stesso segno di d2'")
    print("-" * 130)
    conta = {"VERSO": 0, "VIA": 0, "non distinguibile": 0}
    for k0, k1 in VAL:
        a0, a1 = dd("d1", k0, k1)
        b0, b1 = dd("d2", k0, k1)
        x, y = a1 - a0, b1 - b0
        if abs(x) > 3.0 * abs(y) and x * y > 0:
            v = "VERSO" if x < 0 else "VIA"
        else:
            v = "non distinguibile"
        conta[v] += 1
        nota = "  (fuori regola: |Delta d1'| > 3 |Delta d2'| ma col verso OPPOSTO a d2')" if abs(x) > 3.0 * abs(y) and x * y <= 0 else ""
        print("  [%4d, %4d]: Delta d1' %+.6f, Delta d2' %+.6f, il rapporto %.2f  ->  %s%s" % (k0, k1, x, y, abs(x) / abs(y) if y != 0 else float("inf"), v, nota))
    print("  ### IL VERDETTO D2' su %d finestre valide: VERSO %d, VIA %d, non distinguibile dalla deriva senza chi %d" % (len(VAL), conta["VERSO"], conta["VIA"], conta["non distinguibile"]))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
