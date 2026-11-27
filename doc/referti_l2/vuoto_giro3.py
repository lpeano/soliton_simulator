# -*- coding: utf-8 -*-
r"""**[M2034-A] LA DIAGNOSI DEL VUOTO DEL GIRO 3 DI [M0414]** *(DECISIONE DI LUCA, 2026-11-26 20:34, dalla posta; il piano di [M0925]; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-septendecies`; solo letture)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/vuoto_giro3.py > doc/referti_l2/vuoto_giro3.txt

Su `M0414/puntofisso_accoppiato/giro_3/partenza_giro_4.npz`: per anello dal baricentro di `rho_psi` *(`[45, 60)`, `[60, 75)`, `[75, 90)`)* il rapporto di `rho_phi` contro quella di `phi_v`; **`J_phi`** = `rho_phi grad theta`, `theta` la fase di `somma conj(phi_v) phi` per nodo, i nodi giusti *(`(m1 +- 1, m2)`, `(m1 +- 1, m2 +- 2)`)*, radiale e tangenziale *(negativo = verso l'oggetto)*; **`chi(d)`** per anello. **(V1)** sul vuoto fresco il rapporto `1` e la corrente `0` entro `1e-9`; DEVE FALLIRE con una fase `q y`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import fondo_puntofisso as PF  # noqa: E402

STATO = os.path.join(PF.CTRL, "M0414", "puntofisso_accoppiato", "giro_3", "partenza_giro_4.npz")
ANELLI = ((45.0, 60.0), (60.0, 75.0), (75.0, 90.0))
ANELLI_CHI = ((0.0, 15.0), (15.0, 30.0), (30.0, 45.0)) + ANELLI
S3 = math.sqrt(3.0)


def per_nodo(phi, ref, nodo, n):
    """### `(rho_phi, Z)`: `Z = somma conj(ref) phi` col prodotto in reali *(Im = 0 esatto per phi = ref)*."""
    rho = np.bincount(nodo, weights=np.abs(phi) ** 2, minlength=n)
    ar, ai, br, bi = ref.real, ref.imag, phi.real, phi.imag
    Zn = np.bincount(nodo, weights=ar * br + ai * bi, minlength=n) + 1j * np.bincount(nodo, weights=ar * bi - ai * br, minlength=n)
    return rho, Zn


def correnti(rho, Zn, vic):
    sx, dx, giu, su = vic
    gx = np.angle(np.conj(Zn[sx]) * Zn[dx]) / 2.0
    gy = np.angle(np.conj(Zn[giu]) * Zn[su]) / (2.0 * S3)
    return rho * gx, rho * gy


def anelli_di(v, d, an):
    return [float(v[(d >= a) & (d < b)].mean()) for a, b in an]


def main():
    import _presidio
    from solitone import toro as TO
    F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(__file__)
    PF.controlla(STATO)
    print("=" * 130)
    print("[M2034-A] LA DIAGNOSI DEL VUOTO DEL GIRO 3 (la carta sez. 3-septendecies): %s" % STATO)
    print("=" * 130)
    with F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        pv = np.asarray(Z["phi_v"]).copy()
        tab, K = Z["tab_c"], Z["K"]
        Z["metti"]()
    vic = (((m1 - 1) % L) * L + m2, ((m1 + 1) % L) * L + m2, ((m1 - 1) % L) * L + (m2 - 2) % L, ((m1 + 1) % L) * L + (m2 + 2) % L)
    with np.load(STATO) as z:
        phi, psi, chi = z["phi_h"].copy(), z["psi_h"].copy(), z["chi"].copy()
    rpsi = np.bincount(nodo, weights=np.sum(np.abs(psi) ** 2, axis=1), minlength=n)
    b = TO.centro(rpsi, m1, m2, L)[:2]
    dxy = np.asarray(TO.scarti(m1, m2, b[0], b[1], L))[:, :2]
    d = np.hypot(dxy[:, 0], dxy[:, 1])
    rx, ry = dxy[:, 0] / np.maximum(d, 1e-300), dxy[:, 1] / np.maximum(d, 1e-300)
    print("  il centro (baricentro di rho_psi) %s; |c| = |tab_c[K]| %.9f" % (["%.3f" % x for x in b], abs(complex(tab[K]))))
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    # ### (V1)
    rv, Zv = per_nodo(pv, pv, nodo, n)
    jx, jy = correnti(rv, Zv, vic)
    rat = [x / x for x in anelli_di(rv, d, ANELLI)]
    jm = float(max(np.max(np.abs(jx)), np.max(np.abs(jy))))
    esito("(V1) il vuoto fresco: il rapporto 1 e la corrente 0 entro 1e-9", all(abs(r - 1.0) < 1e-9 for r in rat) and jm < 1e-9, "max |J| %.1e" % jm)
    y = (m2 * S3 / 2.0)[nodo]
    q = 2.0 * math.pi * 2.0 / (L * S3 / 2.0)
    rq, Zq = per_nodo(pv * np.exp(1j * q * y), pv, nodo, n)
    jx, jy = correnti(rq, Zq, vic)
    esito("(V1) DEVE FALLIRE lo zero: una fase q y da' una corrente lungo y", float(np.max(np.abs(jy))) > 1e-6, "max |J_y| %.3e" % float(np.max(np.abs(jy))))
    # ### i numeri
    rho, Zn = per_nodo(phi, pv, nodo, n)
    rv0 = np.bincount(nodo, weights=np.abs(pv) ** 2, minlength=n)
    jx, jy = correnti(rho, Zn, vic)
    jr, jt = jx * rx + jy * ry, -jx * ry + jy * rx
    print("-" * 130)
    print("  per anello (d dal centro): rho_phi / rho_phi(phi_v); J_phi radiale e tangenziale (la media; negativo = verso l'oggetto); |J| medio")
    print("-" * 130)
    a1, a0 = anelli_di(rho, d, ANELLI), anelli_di(rv0, d, ANELLI)
    ar_, at_ = anelli_di(jr, d, ANELLI), anelli_di(jt, d, ANELLI)
    aj = anelli_di(np.hypot(jx, jy), d, ANELLI)
    for (lo, hi), x1, x0, r_, t_, m_ in zip(ANELLI, a1, a0, ar_, at_, aj):
        print("    [%2.0f, %2.0f): rho_phi %.6f / %.6f = %.6f;  J radiale %+.4e, tangenziale %+.4e, |J| medio %.4e" % (lo, hi, x1, x0, x1 / x0, r_, t_, m_))
    print("  chi per anello: %s" % "  ".join("[%2.0f, %2.0f) %+.4f" % (lo, hi, v) for (lo, hi), v in zip(ANELLI_CHI, anelli_di(chi, d, ANELLI_CHI))))
    print("  chi a d > 45: media %+.4f, min %+.4f, max %+.4f" % (float(chi[d > 45].mean()), float(chi[d > 45].min()), float(chi[d > 45].max())))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
