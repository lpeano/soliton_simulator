# -*- coding: utf-8 -*-
r"""**[M0118-01] LA CADUTA PER PARTI E LA FORMA DURANTE LA CADUTA -- LA LETTURA V3** *(DECISIONE DI LUCA, 2026-11-24 01:17; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-decies`; `caduta_parti_v2.py` e' IN CORSA e non si tocca: qui la sua lettura, poi la forma)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_parti_v3.py > doc/referti_l2/caduta_parti.txt

**Dagli stati ogni `250` di `M1658/c1_parti/caduta_V2`:** `w(k)` e i pezzi *(`torneo_tenuta.misura`)*; `m = 3` sugli anelli *(`forma_fondo.momenti`, `forma_fondo.geometria`)*; **`omega` su `[k, k + 250]`** = `(-arg <psi_k|psi_{k+250}> + 2 pi m)/250`, `m` per l'`omega` piu' vicino a `+0.0940`, con la fedelta'. **Il caso noto** sulla tenuta 1b *(`omega.npy`)*: `[2500, 2750]`, `[2750, 3000]` entro `1e-4`; **DEVE FALLIRE** `[2500, 3000]` diviso per `250`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import caduta_parti_v2 as CPV2  # noqa: E402
import forma_fondo as FF  # noqa: E402
import torneo_tenuta as TT  # noqa: E402

D_ST = CPV2.D_ST
TEN = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658", "tenuta", "L-1_proiezione_K")
OMEGA_RIF = 0.0940
PASSO = 250


def omega_tra(p1, p2, nt):
    z = complex(np.vdot(p1, p2))
    phi = -math.atan2(z.imag, z.real)
    m = round((nt * OMEGA_RIF - phi) / (2.0 * math.pi))
    fid = abs(z) / math.sqrt(float(np.vdot(p1, p1).real) * float(np.vdot(p2, p2).real))
    return (phi + 2.0 * math.pi * m) / nt, fid


def forma():
    import gravita_due_corpi_misure as GM
    print("-" * 130)
    print("[M0118-01] LA FORMA DURANTE LA CADUTA (gli stati ogni %d): w e i pezzi, m = 3 sugli anelli %s, omega su [k, k + %d]" % (PASSO, FF.ANELLI, PASSO))
    print("-" * 130)
    with FF.TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        Z["metti"]()
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    om = np.load(os.path.join(TEN, "omega.npy"))
    P = {k: GM.leggi(os.path.join(TEN, "stato_%06d.npz" % k))[0]["psi_h"] for k in (2500, 2750, 3000)}
    for k0 in (2500, 2750):
        w, fid = omega_tra(P[k0], P[k0 + PASSO], PASSO)
        media = float(om[k0:k0 + PASSO].mean())
        esito("il caso noto omega [%d, %d] della tenuta 1b = la media di omega.npy entro 1e-4" % (k0, k0 + PASSO), abs(w - media) <= 1e-4, "%+.7f contro %+.7f (|d| %.1e; la fedelta' %.6f)" % (w, media, abs(w - media), fid))
    w, fid = omega_tra(P[2500], P[3000], PASSO)
    media = float(om[2500:3000].mean())
    esito("DEVE FALLIRE: [2500, 3000] diviso per 250 (la finestra sbagliata) oltre 1e-4", abs(w - media) > 1e-4, "%+.7f contro %+.7f" % (w, media))
    uno = np.ones(n)
    prec = None
    righe = []
    for k in range(0, 2001, PASSO):
        f = os.path.join(D_ST, "stato_%06d.npz" % k)
        X, meta = GM.leggi(f)
        wv, pz, mx, M = TT.misura(f, nodo, n, L)
        rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
        _d, r, th = FF.geometria(rho, m1, m2, L)
        m3 = []
        for lo, hi in FF.ANELLI:
            sel = (r >= lo) & (r < hi)
            a3, o3 = FF.momenti(rho, th, sel, 3)
            f3, _o = FF.momenti(uno, th, sel, 3)
            m3.append("[%2g, %2g) %.5f (%+7.2f gradi; il favo %.5f)" % (lo, hi, a3, o3, f3))
        om_s = ""
        if prec is not None:
            wo, fid = omega_tra(prec, X["psi_h"], PASSO)
            om_s = "; omega [%d, %d] %+.7f, la fedelta' %.6f" % (k - PASSO, k, wo, fid)
            righe.append(wo)
        prec = X["psi_h"]
        print("  k %4d: w %.3f, i pezzi %d, il picco lisciato %.4e, la massa %.6f%s" % (k, wv, pz, mx, M, om_s))
        print("          m = 3: " + "; ".join(m3))
    if righe:
        print("### omega: la prima finestra %+.7f, l'ultima %+.7f, la differenza %+.2e; il minimo %+.7f, il massimo %+.7f; il gap (0.011870, 0.245338)" % (righe[0], righe[-1], righe[-1] - righe[0], min(righe), max(righe)))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE della forma: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    return 0 if not fall else 1


def main():
    import _presidio
    for m in ("caduta_parti.py", "caduta_parti_v2.py", "forma_fondo.py", "torneo_tenuta.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    r1 = CPV2.lettura()
    r2 = forma()
    print("=" * 130)
    return r1 or r2


if __name__ == "__main__":
    sys.exit(main())
