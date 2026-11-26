# -*- coding: utf-8 -*-
r"""**[M2034-B] LA LETTURA DI d1', d2', d3' COL CRITERIO C** *(DECISIONE DI LUCA `09:25` e [M2034] `20:34`; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-vicies`, scritta PRIMA di questo file)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_lettura_v3.py > doc/referti_l2/due_corpi_fondo_v6.txt

**I casi noti** N1-N3, poi **il controllo d3'** *(le `12` finestre da `500`: `w` con `fondo_puntofisso_chi.w_di` sui tre stati entro il `5%` di `4.5`, `omega` medio entro il `5%` di `0.0833`, il pozzo con `fondo_puntofisso_chi.profondita` sui tre stati entro il `10%` di `-102`)*, **le finestre valide stampate PRIMA di d1'**, poi **il controllo d2'** *(`max |d(k) - d(0)| < 0.5`)*, poi **le letture di d1' solo sulle finestre valide** *(come `due_corpi_lettura_v2`, che e' usato e non si riscrive)* e **il verdetto**.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_lettura_v2 as L2  # noqa: E402
import fondo_puntofisso_chi as FPC  # noqa: E402

VV2, VV, PF = L2.VV2, L2.VV, L2.PF
BASE = os.path.join(PF.CTRL, "M2034", "coppia")
GIRO3 = os.path.join(PF.CTRL, "M0414", "puntofisso_accoppiato", "giro_3")
FIN = [(k, k + 500) for k in range(0, 6000, 500)]
KS = list(range(0, 6001, 250))
RIF_W, RIF_OM, RIF_POZZO = 4.5, 0.0833, -102.0
TOL_W, TOL_OM, TOL_POZZO = 0.05, 0.05, 0.10
TOL_D2 = 0.5


def valide(righe, rw):
    """### le finestre in cui `w` *(tutti e tre gli stati)*, `omega` e il pozzo *(tutti e tre)* stanno nelle soglie."""
    out = []
    for (k0, k1), x in zip(FIN, righe):
        okw = all(abs(w / rw - 1.0) < TOL_W for w in x["w"])
        oko = abs(x["om"] / RIF_OM - 1.0) < TOL_OM
        okp = all(abs(p / RIF_POZZO - 1.0) < TOL_POZZO for p in x["pozzo"])
        out.append((k0, k1, okw, oko, okp, okw and oko and okp))
    return out


def main():
    import _presidio
    VV.V3.avvia()
    for m in ("vento_vuoto.py", "vento_vuoto_v2.py", "due_corpi_lettura_v2.py", "fondo_puntofisso_chi.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2034-B] LA LETTURA COL CRITERIO C (la carta sez. 3-vicies): d1' due chi on, d2' due chi off, d3' uno chi on; phi fresco c(t) phi_v; 6000 tick")
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
    # ### (N1) le formule del giro, rifatte sul giro 3 a k 500
    fg = os.path.join(GIRO3, "giro.json")
    PF.controlla(fg)
    G = json.load(open(fg, encoding="utf-8"))
    X5 = L2.leggi(os.path.join(GIRO3, "stato_000500.npz"))
    r5 = rho_psi(X5)
    w5, p5 = FPC.w_di(r5, L), FPC.profondita(ZG, r5, X5["chi"])
    esito("(N1) w_di sul giro 3 a k 500 = giro.json w[5] AL BIT", w5 == G["w"][5], "%.15g contro %.15g" % (w5, G["w"][5]))
    esito("(N1) profondita sul giro 3 a k 500 = giro.json profondita[5] AL BIT", p5 == G["profondita"][5], "%.15g contro %.15g" % (p5, G["profondita"][5]))
    S = {}
    for c in ("d1", "d2", "d3"):
        f = os.path.join(BASE, c, "serie.json")
        PF.controlla(f)
        S[c] = json.load(open(f, encoding="utf-8"))
    om3 = np.array(S["d3"]["omega"][0])
    esito("(N2) la serie di d3' ha 6000 omega", len(om3) == 6000, "%d" % len(om3))
    a0, a1 = G["finestra"]
    print("  ### il giro 3 sulla sua finestra [%d, %d] (solo stampa, non conta): w medio %.4f; omega medio %.6f; il pozzo medio %.3f" % (
        a0, a1, float(np.mean(G["w"][a0 // 100:a1 // 100 + 1])), float(np.mean(G["omega"][a0:a1])), float(np.mean(G["profondita"][a0 // 100:a1 // 100 + 1]))))
    print("-" * 130)
    print("IL CONTROLLO d3' (w e omega entro il 5%% di %.1f e %.4f; il pozzo entro il 10%% di %.0f), PER FINESTRA DI 500" % (RIF_W, RIF_OM, RIF_POZZO))
    print("-" * 130)
    W3, P3 = {}, {}
    for k in KS:
        X = L2.leggi(os.path.join(BASE, "d3", "stato_%06d.npz" % k))
        r = rho_psi(X)
        W3[k], P3[k] = FPC.w_di(r, L), FPC.profondita(ZG, r, X["chi"])
    righe = [dict(w=[W3[k0], W3[k0 + 250], W3[k1]], pozzo=[P3[k0], P3[k0 + 250], P3[k1]], om=float(om3[k0:k1].mean())) for k0, k1 in FIN]
    V = valide(righe, RIF_W)
    for (k0, k1, okw, oko, okp, ok), x in zip(V, righe):
        print("  [%4d, %4d]: w %.4f %.4f %.4f (%s); omega %.6f (%+.2f%%, %s); il pozzo %.3f %.3f %.3f (%s)  ->  %s" % (
            k0, k1, *x["w"], "si" if okw else "NO", x["om"], 100 * (x["om"] / RIF_OM - 1), "si" if oko else "NO", *x["pozzo"], "si" if okp else "NO", "VALIDA" if ok else "non valida"))
    VAL = [(k0, k1) for k0, k1, *_r, ok in V if ok]
    nv3 = [(k0, k1) for k0, k1, *_r, ok in valide(righe, RIF_W * 1.2) if ok]
    esito("(N3) DEVE FALLIRE: col riferimento di w a 4.5 x 1.2 nessuna finestra di d3' e' valida", len(nv3) == 0, "%d valide" % len(nv3))
    print("  ### LE FINESTRE VALIDE DI d3': %d su %d  %s" % (len(VAL), len(FIN), VAL))
    print("-" * 130)
    print("IL CONTROLLO d2' (chi off): max |d(k) - d(0)| < %.1f nodi" % TOL_D2)
    print("-" * 130)
    D = {}
    for c in ("d1", "d2"):
        sr = np.array(S[c]["serie"])
        D[c] = (sr[:, 0], np.hypot(sr[:, 4] - sr[:, 1], sr[:, 5] - sr[:, 2]))
    k2, d2 = D["d2"]
    dm = float(np.max(np.abs(d2 - d2[0])))
    ok2 = dm < TOL_D2
    print("  d2': d(0) %.6f; max |d(k) - d(0)| %.6f a k %d  ->  %s" % (float(d2[0]), dm, int(k2[np.argmax(np.abs(d2 - d2[0]))]), "FERMO" if ok2 else "### NON FERMO"))
    fall = [k for k, v in OK.items() if not v]
    if not VAL or not ok2:
        print("### IL VERDETTO SU d1' NON SI DA': %s" % ("nessuna finestra valida di d3'" if not VAL else "d2' non sta fermo"))
        print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
        print("=" * 130)
        return 0 if not fall else 1
    print("-" * 130)
    print("(i) d(k) E a PER FINESTRA VALIDA (a < 0: si avvicinano); a(d1') - a(d2')")
    print("-" * 130)
    k1_, d1_ = D["d1"]
    vs = []
    for k0, k1 in VAL:
        a1, s1, _ = L2.fit_d(k1_, d1_, k0, k1)
        a2, s2, _ = L2.fit_d(k2, d2, k0, k1)
        s = math.hypot(s1, s2)
        vs.append((a1 - a2) / s)
        print("  [%4d, %4d]: d(d1') %.6f -> %.6f;  a(d1') %+.4e +- %.1e;  a(d2') %+.4e +- %.1e;  a(d1') - a(d2') %+.4e +- %.1e (%+.1f sigma)" % (
            k0, k1, float(d1_[k1_ == k0][0]), float(d1_[k1_ == k1][0]), a1, s1, a2, s2, a1 - a2, s, (a1 - a2) / s))
    neg, pos = sum(1 for v in vs if v < -2.0), sum(1 for v in vs if v > 2.0)
    if 2 * neg >= len(vs) and pos == 0:
        ver = "SI AVVICINANO"
    elif 2 * pos >= len(vs) and neg == 0:
        ver = "SI ALLONTANANO"
    else:
        ver = "NESSUN SEGNALE"
    print("  ### IL VERDETTO SU d1' (la carta: oltre 2 sigma su almeno meta' delle valide, nessuna contraria): %s  (%d negative, %d positive oltre 2 sigma, su %d)" % (ver, neg, pos, len(vs)))
    print("-" * 130)
    print("(ii)-(v) SUGLI STATI DELLE FINESTRE VALIDE: J_r e rho_phi su [8,16) [16,32); chi su [0,4) [4,8) [8,16) [16,32); w (raggio quadratico medio nella meta'); omega medio")
    print("-" * 130)
    from solitone import toro as TO
    su = ((m1 + 1) % L) * L + (m2 + 2) % L
    giu = ((m1 - 1) % L) * L + (m2 - 2) % L
    dx_p = ((m1 + 1) % L) * L + m2
    sx_m = ((m1 - 1) % L) * L + m2
    kv = sorted({k for k0, k1 in VAL for k in (k0, k0 + 250, k1)})
    b = S["d1"]["meta"]["centro_coppia"]
    dxy = np.asarray(TO.scarti(m1, m2, b[0], b[1], L))[:, :2]
    masch = [dxy[:, 1] < 0.0, dxy[:, 1] >= 0.0]
    X0 = L2.leggi(os.path.join(BASE, "d1", "stato_000000.npz"))
    phi0 = X0["phi_h"]
    om1 = [np.array(o) for o in S["d1"]["omega"]]
    for k in kv:
        X = X0 if k == 0 else L2.leggi(os.path.join(BASE, "d1", "stato_%06d.npz" % k))
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
            o = float(om1[j][max(k - 250, 0):k].mean()) if k > 0 else float(om1[j][0])
            print("  d1' corpo %d k %4d: J_r %s;  rho_phi %s;  chi %s;  w %.4f;  omega (250 prima) %+.6f" % (
                j + 1, k, " ".join("%+.4e" % float(Jr[an(a_, b_)].mean()) for a_, b_ in L2.ANELLI_J),
                " ".join("%.6f" % float(rho[an(a_, b_)].mean()) for a_, b_ in L2.ANELLI_J),
                " ".join("%+.4e" % float(X["chi"][an(a_, b_)].mean()) for a_, b_ in L2.ANELLI_CHI),
                math.sqrt(float(np.sum(w * r * r) / w.sum())), o))
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
