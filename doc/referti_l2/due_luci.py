# -*- coding: utf-8 -*-
r"""**[M2053] LE DUE LUCI: LA DISPERSIONE DELLE ONDE DEL VUOTO phi** *(DECISIONE DI LUCA, 2026-11-26 20:53, dalla posta; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-undevicies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_luci.py noto > doc/referti_l2/due_luci_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/due_luci.py corsa --dir x --n 2 --eps 1e-3     (x: n 2, 4, 8, 16; y: n 2; e x n 2 a eps 5e-4; dalla coda, dopo B)
    E:\python\py3132\python.exe doc/referti_l2/due_luci.py lettura > doc/referti_l2/due_luci.txt

**La scena:** quella del fondo *(`triangolo_chi_v4.scena`)*, **`psi = 0`**, **`phi = phi_v (1 + eps e^{i q.x})`**, i campi `porto.campi` *(senza materia: zero)*, **il tick del fondo con `N = 1`** *(`fondo_1c.ciclo`, `cs_N` falso, `segno 0`: chi spento, lapse piatto, la forma `L-1`)*; `C.residuo` assoluto *(senza `rho`, come D2 di [M2034])*. **Le onde ammesse dal toro** *(`A1 = (1, 0)`, `A2 = (-1/2, sqrt3/2)`)*: lungo `x` la fase `2 pi n (m1 - m2/2)/L`, **`n` pari**, `|q| = 2 pi n/L`; lungo `y` la fase `2 pi n m2/L`, `|q| = 2 pi n/L_y`. **La misura, a ogni tick:** `A_0 = <phi_v|phi>/<phi_v|phi_v>`, `A_q = <phi_v w_q|phi>/<phi_v|phi_v>`; **`omega(q) - omega_phi`** = meno la pendenza del fit lineare della fase di `A_q/A_0` *(svolta)* sul tick.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import fondo_puntofisso as PF  # noqa: E402

BASE = os.path.join(PF.CTRL, "M2053")
K_CORSA = 1000
C_PSI = 0.084955            # ### ep_fondo.C_RET: v_max della banda della materia, per tick (ep_fondo.txt)
CORSE = (("x", 2, 1e-3), ("x", 4, 1e-3), ("x", 8, 1e-3), ("x", 16, 1e-3), ("y", 2, 1e-3), ("x", 2, 5e-4))


def onda(m1, m2, L, dire, n):
    """### la fase per nodo e `|q|`."""
    if dire == "x":
        assert n % 2 == 0, "lungo x il toro vuole n pari"
        return 2.0 * math.pi * n * (m1 - 0.5 * m2) / L, 2.0 * math.pi * n / L
    return 2.0 * math.pi * n * m2 / L, 2.0 * math.pi * n / (L * math.sqrt(3.0) / 2.0)


def residuo_assoluto_di(C, Z):
    import chi_tick as CT

    def r():
        if C.campo is None or C.campo.e == 0.0:
            return 0.0
        rho = CT.rho_di(Z["mot"], Z["st"])
        return float(np.max(np.abs(C.campo.div() - C.campo.e * (rho - rho.mean()))))
    return r


def prepara(Z, dire, n, eps):
    """### `(C, pv, w, q)`: il vuoto increspato nella scena."""
    from solitone import porto as PO
    MT = F1.TC.moduli()[0]
    F1.OGGETTO = PF.PARTENZA_1
    C, info, _dxy, _f, _X = F1.FS.carica(Z, "K", 3000)
    nodo = np.asarray(Z["mot"].inc.nodo)
    m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
    fase, q = onda(m1, m2, Z["L"], dire, n)
    pv = np.asarray(Z["phi_v"]).copy()
    w = np.exp(1j * fase[nodo])
    Z["st"]["psi_h"][...] = 0.0
    Z["st"]["phi_h"][...] = pv * (1.0 + eps * w)
    C = PO.campi(Z, MT.rho_c_assoluto(), MT.PB.E_DECISO)
    C.residuo = residuo_assoluto_di(C, Z)
    return C, pv, w, q


def gira(dire, n, eps, ticks):
    MV, P0 = F1.TT.nucleo()
    A0, Aq, A2q = [], [], []
    with F1.TC.scena() as Z:
        C, pv, w, q = prepara(Z, dire, n, eps)
        nrm = float(np.vdot(pv, pv).real)
        N = np.ones(Z["n"])

        def mis():
            ph = Z["st"]["phi_h"]
            A0.append(complex(np.vdot(pv, ph)) / nrm)
            Aq.append(complex(np.vdot(pv * w, ph)) / nrm)
            A2q.append(complex(np.vdot(pv * w * w, ph)) / nrm)
        mis()
        F1.ciclo(Z, C, ticks, lambda kk, prima: mis(), MV, P0, N, False, 0)
        Z["metti"]()
    return np.array(A0), np.array(Aq), np.array(A2q), q


def fit_omega(A0, Aq, k0=0, k1=None):
    """### `omega(q) - omega_phi` = meno la pendenza della fase svolta di `A_q/A_0` sul tick."""
    r = Aq / A0
    ph = np.unwrap(np.angle(r))
    k = np.arange(len(r))
    m = (k >= k0) & (k <= (k1 if k1 is not None else len(r) - 1))
    p = np.polyfit(k[m], ph[m], 1)
    res = ph[m] - np.polyval(p, k[m])
    return float(-p[0]), float(np.std(res))


def noto():
    import _presidio
    F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2053] I CASI NOTI DELLE DUE LUCI (la carta sez. 3-undevicies)")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    with F1.TC.scena() as Z:
        C, pv, w, q = prepara(Z, "x", 2, 1e-3)
        nrm = float(np.vdot(pv, pv).real)
        ph = Z["st"]["phi_h"]
        aq = complex(np.vdot(pv * w, ph)) / nrm
        a2 = complex(np.vdot(pv * w * w, ph)) / nrm
        Z["metti"]()
    esito("(K2) a k 0 la componente a q vale eps = 1e-3 entro 1e-12, quella a 2q sotto 1e-9", abs(aq - 1e-3) < 1e-12 and abs(a2) < 1e-9, "A_q %+.15e%+.3ei, |A_2q| %.2e" % (aq.real, aq.imag, abs(a2)))
    om = 0.0371
    k = np.arange(1000)
    sint = 1e-3 * np.exp(-1j * (om - 0.4712) * k) * np.exp(-1j * 0.4712 * k)
    f, s = fit_omega(np.exp(-1j * 0.4712 * k), sint)
    esito("(K3) la lettura su una serie sintetica e^{-i omega k} ridà omega(q) - omega_phi entro 1e-9", abs(f - (om - 0.4712)) < 1e-9, "%.12f contro %.12f" % (f, om - 0.4712))
    t1 = time.time()
    A0, Aq, A2q, q = gira("x", 2, 0.0, K_CORSA)
    o = -np.angle(A0[1:] / A0[:-1])
    esito("(K1) eps 0: il vuoto fermo per %d tick, omega_phi per tick costante entro 1e-12 (al bit non si chiede: l'arg arrotonda)" % K_CORSA, float(np.ptp(o)) < 1e-12 and float(np.max(np.abs(np.abs(A0) - 1.0))) < 1e-12, "omega_phi %+.12f, ptp %.2e, max ||A_0| - 1| %.2e (%.0f s)" % (float(o.mean()), float(np.ptp(o)), float(np.max(np.abs(np.abs(A0) - 1.0))), time.time() - t1))
    fall = [k_ for k_, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa(dire, n, eps):
    import _presidio
    F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(__file__)
    nome = "%s_n%d_eps%.0e" % (dire, n, eps)
    d = os.path.join(BASE, nome)
    assert not os.path.exists(os.path.join(d, "serie.json")), "%s c'e' gia': non si riscrive" % d
    os.makedirs(d, exist_ok=True)
    t1 = time.time()
    A0, Aq, A2q, q = gira(dire, n, eps, K_CORSA)
    f = os.path.join(d, "serie.json")
    open(f, "w", encoding="utf-8").write(json.dumps({"dir": dire, "n": n, "eps": eps, "q": q, "L": 162,
                                                     "A0": [[a.real, a.imag] for a in A0], "Aq": [[a.real, a.imag] for a in Aq], "A2q": [[a.real, a.imag] for a in A2q]}))
    PF.firma(f)
    print("### %s: q %.6f; %d tick in %.0f s" % (nome, q, K_CORSA, time.time() - t1))
    return 0


def leggi(dire, n, eps):
    f = os.path.join(BASE, "%s_n%d_eps%.0e" % (dire, n, eps), "serie.json")
    if not os.path.exists(f + ".sha1"):
        return None
    PF.controlla(f)
    x = json.load(open(f, encoding="utf-8"))
    c = lambda v: np.array([a + 1j * b for a, b in v])  # noqa: E731
    return x["q"], c(x["A0"]), c(x["Aq"]), c(x["A2q"])


def lettura():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2053] LE DUE LUCI (la carta sez. 3-undevicies): omega(q) - omega_phi del vuoto, c_phi, il gap, l'anisotropia; c_psi = %.6f (ep_fondo.C_RET)" % C_PSI)
    print("=" * 130)
    R = {}
    for dire, n, eps in CORSE:
        r = leggi(dire, n, eps)
        if r is None:
            print("  %s n %d eps %.0e: NON FINITA" % (dire, n, eps))
            continue
        q, A0, Aq, A2q = r
        dw, s = fit_omega(A0, Aq)
        dwa, _ = fit_omega(A0, Aq, 0, 500)
        dwb, _ = fit_omega(A0, Aq, 500, 1000)
        om0 = float(np.mean(-np.angle(A0[1:] / A0[:-1])))
        amp = np.abs(Aq / A0) / eps
        R[(dire, n, eps)] = (q, dw)
        print("  %s n %2d (L 162), eps %.0e: q %.6f; omega_phi %+.9f; omega(q) - omega_phi %+.6e (lo scarto del fit %.2e; [0, 500] %+.6e, [500, 1000] %+.6e); |A_q/A_0|/eps da %.4f a %.4f" % (
            dire, n, eps, q, om0, dw, s, dwa, dwb, float(amp.min()), float(amp.max())))
    lin = ("x", 2, 1e-3) in R and ("x", 2, 5e-4) in R
    if lin:
        r = R[("x", 2, 5e-4)][1] / R[("x", 2, 1e-3)][1] - 1.0
        print("### LA LINEARITA' (x, n 2): eps 5e-4 contro 1e-3: %+.3f%% %s" % (100 * r, "(entro l'1%)" if abs(r) <= 0.01 else "### OLTRE L'1%: NIENTE VERDETTO"))
        lin = abs(r) <= 0.01
    xs = sorted((R[k][0], R[k][1]) for k in R if k[0] == "x" and k[2] == 1e-3)
    if len(xs) >= 2:
        (q1, w1), (q2, w2) = xs[0], xs[1]
        cphi = (w2 - w1) / (q2 - q1)
        qq = np.array([a for a, _ in xs])
        ww = np.array([b for _, b in xs])
        pg = np.polyfit(qq ** 2, ww, 1)
        print("  c_phi (la pendenza fra i due q piu' piccoli lungo x, %.6f e %.6f): %+.6f; il gap (il fit omega = a + b q^2 lungo x): a %+.6e, b %+.6e" % (q1, q2, cphi, pg[1], pg[0]))
        if ("y", 2, 1e-3) in R:
            qy, wy = R[("y", 2, 1e-3)]
            wx = float(np.interp(qy, qq, ww))
            an = abs(wy / qy) / abs(wx / qy) - 1.0 if wx else float("nan")
            print("  l'anisotropia: lungo y q %.6f, omega(q) - omega_phi %+.6e; lungo x interpolato alla stessa q %+.6e: %+.2f%% %s" % (qy, wy, wx, 100 * an, "### ANISOTROPO (oltre il 5%)" if abs(an) > 0.05 else "(entro il 5%)"))
        if lin:
            rr = abs(abs(cphi) - C_PSI) / C_PSI
            print("### IL VERDETTO S4: |c_phi| %.6f contro c_psi %.6f: %.1f%% -> %s" % (abs(cphi), C_PSI, 100 * rr, "UNA LUCE SOLA" if rr < 0.10 else "DUE LUCI"))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "lettura"))
    ap.add_argument("--dir", choices=("x", "y"))
    ap.add_argument("--n", type=int)
    ap.add_argument("--eps", type=float)
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        return corsa(a.dir, a.n, a.eps)
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
