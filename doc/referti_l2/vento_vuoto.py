# -*- coding: utf-8 -*-
r"""**[M2245-A] IL VENTO DEL VUOTO: LE LETTURE** *(DECISIONE DI LUCA, 2026-11-24 22:49; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-undecies`; solo letture sugli stati di [M2210], nessuna corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/vento_vuoto.py > doc/referti_l2/vento_vuoto.txt

**Le definizioni** *(dichiarate nella carta)*: per nodo, `rho_phi = somma |phi_h|^2` sulle sei mezze-spighe; **la fase acquistata** `theta(k) = arg somma conj(phi_h(0)) phi_h(k)` *(rispetto allo stato `k 0` della stessa corsa: non serve il tick assoluto di `bordo.c_di`)*; **`d theta/dy`** = `arg(conj(Z_giu) Z_su) / (2 sqrt3)` coi nodi `(m1 - 1, m2 + 2)` e `(m1 + 1, m2 - 2)`, che stanno esattamente a `+- sqrt3` lungo `y`; **`J_phi = rho_phi d theta/dy`** *(la corrente di Noether di un campo complesso)*, mediata sui nodi a distanza `> 25` dal baricentro di `rho_psi`; **`v_phi = <J_phi>/<rho_phi>`** sugli stessi nodi *(ha le dimensioni di un numero d'onda: la riserva e' nella carta)*.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import legge_fondo_v3 as V3  # noqa: E402
import gradiente_pesato as GP  # noqa: E402

F1, PF = V3.F1, V3.PF
TIPI = V3.TIPI
KS = list(range(0, 2001, 250))
S3 = math.sqrt(3.0)


def geometria():
    """### `(nodo, n, L, m1, m2, dxy, su, giu)` dalla scena con l'oggetto del giro 4 caricato *(i `dxy` di `FS.carica`)*."""
    V3.su_v3()
    with F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        _C, info, dxy, _f, _X = F1.FS.carica(Z, "K", 3000)
        Z["metti"]()
    v = np.arange(n)
    assert np.array_equal(m1, v // L) and np.array_equal(m2, v % L), "i nodi non sono v = m1 L + m2"
    su = ((m1 - 1) % L) * L + (m2 + 2) % L
    giu = ((m1 + 1) % L) * L + (m2 - 2) % L
    return nodo, n, L, m1, m2, dxy, su, giu, info


def per_nodo(phi_h, phi0_h, nodo, n):
    """### `(rho_phi, Z)` per nodo: `Z = somma conj(phi0) phi` sulle mezze-spighe del nodo."""
    rho = np.bincount(nodo, weights=np.abs(phi_h) ** 2, minlength=n)
    zz = np.conj(phi0_h) * phi_h
    Zn = np.bincount(nodo, weights=zz.real, minlength=n) + 1j * np.bincount(nodo, weights=zz.imag, minlength=n)
    return rho, Zn


def dtheta_dy(Zn, su, giu):
    return np.angle(np.conj(Zn[giu]) * Zn[su]) / (2.0 * S3)


def leggi_stato(f):
    import gravita_due_corpi_misure as GM
    PF.controlla(f)
    X, _m = GM.leggi(f)
    return X["psi_h"], X["phi_h"]


def bari(psi_h, nodo, n, dxy):
    r = np.bincount(nodo, weights=np.sum(np.abs(psi_h) ** 2, axis=1), minlength=n)
    return (dxy * r[:, None]).sum(axis=0) / r.sum(), r


def main():
    import _presidio
    V3.avvia()
    _presidio.avvia(os.path.join(_QUI, "legge_fondo_v3.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2245-A] IL VENTO DEL VUOTO (la carta sez. 3-undecies): gli stati ogni 250 di [M2210] (r1 gradino, r2 rampa, r3 V0); il raggio %.0f dal baricentro" % V3.RAGGIO)
    print("=" * 130)
    nodo, n, L, m1, m2, dxy, su, giu, info = geometria()
    y = m2 * S3 / 2.0
    Ly = L * S3 / 2.0
    V3.su_v3()
    S = {t: F1.leggi(TIPI[t]) for t in TIPI}
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    # ### i casi noti
    _p0, f0 = leggi_stato(os.path.join(V3.BASE, TIPI["gradino"], "stato_000000.npz"))
    rho0, Z0 = per_nodo(f0, f0, nodo, n)
    esito("(A1) J_phi di k 0 rispetto a se stesso (fase uniforme 0) = 0 AL BIT", np.all(rho0 * dtheta_dy(Z0, su, giu) == 0.0))
    _r, Za = per_nodo(f0 * np.exp(1j * 0.3), f0, nodo, n)
    ja = float(np.max(np.abs(dtheta_dy(Za, su, giu))))
    esito("(A1) la fase uniforme 0.3: |d theta/dy| massimo < 1e-12 (l'arrotondamento: 0.3 non e' al bit)", ja < 1e-12, "%.1e" % ja)
    q = 2.0 * math.pi * 3.0 / Ly
    yh = y[nodo]
    _r, Zq = per_nodo(f0 * np.exp(1j * q * yh), f0, nodo, n)
    dq = dtheta_dy(Zq, su, giu)
    lontano_da_bordo = (m2 >= 2) & (m2 < L - 2)
    eq = float(np.max(np.abs(dq[lontano_da_bordo] / q - 1.0)))
    esito("(A1) DEVE FALLIRE lo zero: la rampa di fase q y (3 giri su L_y) da' d theta/dy = q entro 1e-9 (fuori dalla cucitura del toro)", eq < 1e-9, "max |d/q - 1| %.1e" % eq)
    phis0 = {}
    for t in TIPI:
        _p, f = leggi_stato(os.path.join(V3.BASE, TIPI[t], "stato_000000.npz"))
        phis0[t] = f
    esito("(A4) phi di k 0 uguale AL BIT nelle tre corse", all(np.array_equal(phis0[t], phis0["gradino"]) for t in TIPI))
    # ### le letture
    _G20, _ia, _e0, _MT = F1.CL.parametri()
    import chi_parametri_v2 as CP2
    A = float(S["gradino"]["A"])
    gN = GP.dNdy(y, info["y_c"], A, Ly, CP2.KAPPA)
    om = 0.47123889803846897
    R = {t: {} for t in TIPI}
    for t in TIPI:
        sr = np.array(S[t]["serie"])
        for k in KS:
            ps, ph = leggi_stato(os.path.join(V3.BASE, TIPI[t], "stato_%06d.npz" % k))
            b, rpsi = bari(ps, nodo, n, dxy)
            d = np.hypot(dxy[:, 0] - b[0], dxy[:, 1] - b[1])
            far = d > V3.RAGGIO
            rho, Zn = per_nodo(ph, phis0[t], nodo, n)
            dth = dtheta_dy(Zn, su, giu)
            J = rho * dth
            i = int(np.argmax(np.where(far, rpsi, -1.0)))
            yv = sr[:, 2]
            j = int(np.where(sr[:, 0] == k)[0][0])
            j0, j1 = max(j - 1, 0), min(j + 1, len(sr) - 1)
            vk = float((yv[j1] - yv[j0]) / (sr[j1, 0] - sr[j0, 0]))
            if t == "gradino":
                keff = k
            elif t == "rampa":
                keff = sum(min(x / 500.0, 1.0) for x in range(1, k + 1))
            else:
                keff = 0.0
            R[t][k] = dict(J=float(J[far].mean()), rho=float(rho[far].mean()), v=vk, rif=float(om * keff * np.sum(rho[far] * gN[far]) / np.sum(rho[far])),
                           imax=i, dmax=float(d[i]), ang=float(math.degrees(math.atan2(dxy[i, 1] - b[1], dxy[i, 0] - b[0]))), dyc=float(y[i] - info["y_c"]), amax=float(np.sqrt(rpsi[i])),
                           th_abs=None)
            if k in (0, 1000, 2000) and t in ("gradino", "v0"):
                Za_ = np.bincount(nodo, weights=ph.real, minlength=n) + 1j * np.bincount(nodo, weights=ph.imag, minlength=n)
                rr = [m2 == r_ for r_ in range(L)]
                R[t][k]["th_abs"] = [float(np.angle(Za_[w].sum())) for w in rr]
                R[t][k]["th_rel"] = [float(np.angle(Zn[w].sum())) for w in rr]
    print("-" * 130)
    print("(A1) J_phi LONTANO (la media sui nodi a d > 25) E (A2) v_phi = <J>/<rho_phi>; accanto, il riferimento omega k_eff <dN/dy> (il ritmo locale SE omega del vuoto scalasse come N; omega %.6f della scena)" % om)
    print("-" * 130)
    print("  %5s  %-46s %-46s %-46s" % ("k", "r1 gradino: J, v_phi, riferimento", "r2 rampa: J, v_phi, riferimento", "r3 V0: J, v_phi"))
    for k in KS:
        c = []
        for t in TIPI:
            x = R[t][k]
            c.append("%+.4e %+.4e %+.4e" % (x["J"], x["J"] / x["rho"], x["rif"]))
        print("  %5d  %-46s %-46s %-46s" % (k, c[0], c[1], c[2]))
    print("  (A2) v_phi / v dell'oggetto (v - v(V0) dalla serie, la differenza centrata a 10 tick):")
    for k in KS[1:]:
        vv = {t: R[t][k]["v"] - R["v0"][k]["v"] for t in ("gradino", "rampa")}
        print("    k %4d: gradino v %+.4e, v_phi/v %+.4e;  rampa v %+.4e, v_phi/v %+.4e" % (k, vv["gradino"], (R["gradino"][k]["J"] / R["gradino"][k]["rho"]) / vv["gradino"], vv["rampa"], (R["rampa"][k]["J"] / R["rampa"][k]["rho"]) / vv["rampa"]))
    for t in ("gradino", "rampa", "v0"):
        kk = np.array(KS[1:], float)
        jj = np.array([R[t][k]["J"] - R["v0"][k]["J"] for k in KS[1:]]) if t != "v0" else np.array([R[t][k]["J"] - R[t][0]["J"] for k in KS[1:]])
        Am = np.stack([np.ones_like(kk), kk], axis=1)
        cfit, *_ = np.linalg.lstsq(Am, jj, rcond=None)
        res = jj - Am @ cfit
        cov = float(np.sum(res ** 2) / (len(kk) - 2)) * np.linalg.inv(Am.T @ Am)
        r2 = 1.0 - float(np.sum(res ** 2) / np.sum((jj - jj.mean()) ** 2)) if np.sum((jj - jj.mean()) ** 2) > 0 else float("nan")
        print("  ### %s: %s contro k (k 250..2000): la pendenza %+.4e +- %.1e (%.1f sigma), R2 %.4f" % (t, "J - J(V0)" if t != "v0" else "J - J(k 0)", cfit[1], math.sqrt(cov[1, 1]), abs(cfit[1]) / math.sqrt(cov[1, 1]) if cov[1, 1] > 0 else float("inf"), r2))
    print("-" * 130)
    print("(A3) DOVE STA IL MASSIMO DI |psi| LONTANO (d > 25): il nodo (m1, m2), d dal baricentro, la direzione (gradi, 0 = +x, 90 = +y), y - y_c (L_y/4 = %.3f)" % (Ly / 4.0))
    print("-" * 130)
    for t in ("gradino", "rampa", "v0"):
        for k in KS:
            x = R[t][k]
            print("  %-8s k %4d: |psi| %.4e al nodo (%3d, %3d); d %6.2f; direzione %+7.1f; y - y_c %+8.3f" % (t, k, x["amax"], m1[x["imax"]], m2[x["imax"]], x["dmax"], x["ang"], x["dyc"]))
    print("-" * 130)
    print("(A4) LA FASE DI phi LUNGO y (arg della somma su x, per riga m2): assoluta (arg somma phi_h) e acquistata da k 0; ogni 9 righe")
    print("-" * 130)
    for t in ("gradino", "v0"):
        for k in (0, 1000, 2000):
            x = R[t][k]
            print("  %-8s k %4d assoluta:   %s" % (t, k, " ".join("%+.3f" % x["th_abs"][r_] for r_ in range(0, L, 9))))
            print("  %-8s k %4d acquistata: %s" % (t, k, " ".join("%+.3f" % x["th_rel"][r_] for r_ in range(0, L, 9))))
    out = os.path.join(V3.BASE, "vento_vuoto.json")
    open(out, "w", encoding="utf-8").write(json.dumps({t: {str(k): {a: b for a, b in R[t][k].items() if a not in ("th_abs", "th_rel")} for k in KS} for t in TIPI}))
    PF.firma(out)
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
