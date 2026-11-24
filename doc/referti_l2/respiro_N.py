# -*- coding: utf-8 -*-
r"""**[M1640-R] IL RESPIRO COME OROLOGIO SENZA ZERO: `N` UNIFORME IN V2 E IN V3** *(Luca, 2026-11-23; la carta `doc/CARTA_respiro_orologio.md`, scritta prima)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/respiro_N.py casi_noti > doc/referti_l2/respiro_N_casi_noti.txt
    E:\python\py3132\python.exe doc/referti_l2/respiro_N.py corsa --riga V2 --N 0.99        (N1, V2, V3, CTRL; 20000 tick; riparte dall'ultimo stato)
    E:\python\py3132\python.exe doc/referti_l2/respiro_N.py lettura > doc/referti_l2/respiro_N.txt

**La scena:** `fondo_suite_v2.carica(Z, "F0", 1500)` *(il compatto, la forma S1 del nucleo: come `fh_suite.tenuta_lunga`)*. **Il ciclo:** `fondo_suite_v2._tick_loop` riga per riga, con `(cs_N, segno)` per riga *(quello chiama `tick_var` col segno `0`)*: **N1** `N = 1`; **V2** `(True, 0)`; **V3** `(False, +1)`; **CTRL** `N = 1` con `psi_h *= e^{i e0 (0.99 - 1)}` UNA volta a `k 0`.
**Ogni `50` tick** `w` e il picco *(`torneo_tenuta.lisciata`, `torneo_tenuta.misura`)*; **a ogni tick** `omega`, `omega_c` *(i mezzi archi dei nodi a `r < 5`)*, `omega_10` *(`9 <= r < 11`)*; **il centro:** il picco della `rho` lisciata a `k 0`. **Gli stati ogni `250`** con le serie *(P8)*.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import torneo_tenuta as TT  # noqa: E402
import fondo_suite_v2 as FS  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1640")
TENUTA_S1 = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0326", "tenuta_lunga_S1")
K_FINO, OGNI_W, OGNI_STATO = 20000, 50, 250
R_C, R10 = 5.0, (9.0, 11.0)
RIGHE = {"N1": (False, 0), "V2": (True, 0), "V3": (False, 1), "CTRL": (False, 0)}
K_FIT = 2000
K_RHO = (5000, 10000, 20000)
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-112s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "torneo_tenuta.py", "fondo_suite_v2.py", "chi_tick.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def cartella(riga, N):
    return os.path.join(BASE, "%s_%.2f" % (riga, N))


def geometria(Z):
    """### il centro *(il picco della `rho` lisciata a `k 0`)*, `r` per nodo, le maschere dei mezzi archi."""
    from solitone import toro as TO
    nodo = np.asarray(Z["mot"].inc.nodo)
    n, L = Z["n"], Z["L"]
    rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
    i = int(np.argmax(TT.lisciata(rho, L)))
    d = TO.scarti(Z["m1"], Z["m2"], Z["m1"][i], Z["m2"][i], L)[:, :2]
    r = np.hypot(d[:, 0], d[:, 1])
    return {"nodo": nodo, "n": n, "L": L, "centro": i, "r": r, "mc": r[nodo] < R_C, "m10": (r[nodo] >= R10[0]) & (r[nodo] < R10[1])}


def rho_di(Z, G):
    return np.bincount(G["nodo"], weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=G["n"])


def w_picco(rho, G):
    lis = TT.lisciata(rho, G["L"])
    mx = float(lis.max())
    return math.sqrt(float(np.sum(lis > 0.5 * mx)) * math.sqrt(3.0) / 2.0 / math.pi), mx


def scena(Z, riga, N, MV, P0):
    """### la partenza: `(C, info, G, Nv, cs_N, segno, e0, s)`."""
    _G20, _ia, e0, _MT = CL.parametri()
    C, info, _dxy, forma, _X = FS.carica(Z, "F0", 1500)
    assert forma == "S1", forma
    G = geometria(Z)
    cs_N, segno = RIGHE[riga]
    Nv = np.full(Z["n"], float(N))
    return C, info, G, Nv, cs_N, segno, e0, float(Z["s"])


def ciclo(Z, C, quanti, dopo, MV, P0, Nv, cs_N, segno, e0, s):
    """### `fondo_suite_v2._tick_loop` riga per riga, col `segno` passato."""
    import ripresa_F0_v2 as RF
    MT = CL.parametri()[3]
    with RF.col_nucleo(MV, P0), MV.forma_esplicita("S1"):
        assert MV.ATTIVA == "S1" and MV.pezzi is P0
        for kk in range(1, quanti + 1):
            prima = Z["st"]["psi_h"].copy()
            CS.tick_var(Z["z"], C.campo, s, e0, Nv, cs_N, segno)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            dopo(kk, prima)


def omega_di(prima, dopo, m=None):
    if m is None:
        return float(-np.angle(np.vdot(prima, dopo)))
    return float(-np.angle(np.vdot(prima[m], dopo[m])))


# ------------------------------------------------------------------------------------------ la corsa
def corsa(riga, N, k_fino=K_FINO):
    avvia()
    MV, P0 = TT.nucleo()
    d_out = cartella(riga, N)
    os.makedirs(d_out, exist_ok=True)
    fatti = sorted(int(f[6:12]) for f in os.listdir(d_out) if f.startswith("stato_") and f.endswith(".npz") and os.path.exists(os.path.join(d_out, f + ".sha1")))
    t1 = time.time()
    with TC.scena() as Z:
        C, info, G, Nv, cs_N, segno, e0, s = scena(Z, riga, N, MV, P0)
        S = {"om": [], "omc": [], "om10": [], "kw": [], "w": [], "mx": [], "M": [], "s_tick": []}
        k0 = 0
        if fatti:
            import gravita_due_corpi_misure as GM
            import _u1_prototipo as U1
            k0 = fatti[-1]
            X, _m = GM.leggi(os.path.join(d_out, "stato_%06d.npz" % k0))
            Z["metti"]({x: X[x] for x in Z["chiavi"]})
            C.campo.A[...] = X["campo_A"]
            C.campo.E[...] = X["campo_E"]
            U1.scrivi_U(Z["mot"], C.campo)
            S = json.load(open(os.path.join(d_out, "serie_%06d.json" % k0), encoding="utf-8"))
            assert len(S["om"]) == k0
            print("### LA RIPRESA P8: dallo stato a k %d" % k0)
        elif riga == "CTRL":
            Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * np.exp(1j * float(e0) * (0.99 - 1.0))
        print("### %s N %.2f (cs_N %s, segno %d): %s (k %d); il centro %d; %d nodi a r < %g, %d a r in %s; e0 %.10f; fino a %d" % (
            riga, N, cs_N, segno, info["file"], info["k_file"], G["centro"], int(np.sum(G["r"] < R_C)), int(np.sum((G["r"] >= R10[0]) & (G["r"] < R10[1]))), R10, e0, k_fino))

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            fj = os.path.join(d_out, "serie_%06d.json" % k)
            open(fj, "w", encoding="utf-8").write(json.dumps(S))
            np.savez(fz, meta=np.array(json.dumps({"riga": riga, "N": N, "cs_N": cs_N, "segno": segno, "k": k, "partenza": info["file"], "centro": G["centro"], "e0": e0})), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")

        def misura(k):
            rho = rho_di(Z, G)
            w, mx = w_picco(rho, G)
            S["kw"].append(k)
            S["w"].append(w)
            S["mx"].append(mx)
            S["M"].append(float(rho.sum()))
        if not fatti:
            misura(0)
            salva(0)
        ta = [time.time()]

        def dopo(kk, prima):
            k = k0 + kk
            ps = Z["st"]["psi_h"]
            S["om"].append(omega_di(prima, ps))
            S["omc"].append(omega_di(prima, ps, G["mc"]))
            S["om10"].append(omega_di(prima, ps, G["m10"]))
            S["s_tick"].append(time.time() - ta[0])
            ta[0] = time.time()
            if k % OGNI_W == 0:
                misura(k)
            if k % OGNI_STATO == 0:
                salva(k)
                print("    [stato] k %d: w %.3f, il picco %.4e, omega %+.7f, omega_c - omega_10 %+.3e, la norma %.12e; %.3f s/tick (%.0f s)" % (
                    k, S["w"][-1], S["mx"][-1], S["om"][-1], S["omc"][-1] - S["om10"][-1], S["M"][-1], float(np.mean(S["s_tick"][-250:])), time.time() - t1))
                sys.stdout.flush()
        ciclo(Z, C, k_fino - k0, dopo, MV, P0, Nv, cs_N, segno, e0, s)
        Z["metti"]()
    print("### %d tick in %.0f s" % (k_fino - k0, time.time() - t1))
    return 0


# ------------------------------------------------------------------------------------------ i casi noti (in memoria, prima delle corse)
def casi_noti():
    import gravita_due_corpi_misure as GM
    avvia()
    MV, P0 = TT.nucleo()
    print("=" * 130)
    print("[M1640-R] I CASI NOTI (in memoria; prima delle corse)")
    print("=" * 130)
    fin = {}
    for riga, N, quanti in (("N1", 1.0, 500), ("V2", 1.0, 250), ("V3", 1.0, 250), ("V3", 0.99, 250), ("V2", 0.99, 250)):
        t1 = time.time()
        with TC.scena() as Z:
            C, _info, G, Nv, cs_N, segno, e0, s = scena(Z, riga, N, MV, P0)
            snap = {}

            def dopo(kk, prima):
                if kk % 250 == 0:
                    snap[kk] = {x: Z["st"][x].copy() for x in Z["chiavi"]}
                    snap[kk]["campo_A"] = C.campo.A.copy()
                    snap[kk]["campo_E"] = C.campo.E.copy()
            ciclo(Z, C, quanti, dopo, MV, P0, Nv, cs_N, segno, e0, s)
            Z["metti"]()
        fin[(riga, N)] = snap
        print("    %s N %.2f: %d tick in %.0f s" % (riga, N, quanti, time.time() - t1))
    for k in (250, 500):
        X, _m = GM.leggi(os.path.join(TENUTA_S1, "stato_%06d.npz" % k))
        Y = fin[("N1", 1.0)][k]
        diversi = [x for x in Y if not np.array_equal(X[x], Y[x])]
        esito("CN1 N1 a k %d = la tenuta S1 di [M0326-T] AL BIT (%d array)" % (k, len(Y)), not diversi, "diversi: %s" % diversi)
    Y = fin[("N1", 1.0)][250]
    for riga in ("V2", "V3"):
        X = fin[(riga, 1.0)][250]
        diversi = [x for x in Y if not np.array_equal(X[x], Y[x])]
        esito("CN2 %s con N = 1 = N1 a k 250 AL BIT (tick_var: s * 1.0 = s, exp(0) = 1)" % riga, not diversi, "diversi: %s" % diversi)
    for riga in ("V3", "V2"):
        X = fin[(riga, 0.99)][250]
        esito("DEVE FALLIRE: %s con N = 0.99 diverso da N1 a k 250 (psi_h)" % riga, not np.array_equal(X["psi_h"], Y["psi_h"]), "max|d psi_h| %.3e" % float(np.max(np.abs(X["psi_h"] - Y["psi_h"]))))
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0 if not fall else 1


# ------------------------------------------------------------------------------------------ la lettura
def fit_respiro(k, y):
    from scipy.optimize import curve_fit
    k, y = np.asarray(k, float), np.asarray(y, float)
    m = k >= K_FIT
    k, y = k[m], y[m]
    x = y - np.polyval(np.polyfit(k, y, 1), k)
    F = np.abs(np.fft.rfft(x))
    fr = np.fft.rfftfreq(len(x), d=float(k[1] - k[0]))
    j = int(np.argmax(F[1:])) + 1
    T0 = 1.0 / fr[j]

    def f(kk, a, b, A, T, ph):
        return a + b * (kk - K_FIT) + A * np.sin(2 * np.pi * kk / T + ph)
    p0 = [float(y.mean()), 0.0, float(np.std(x) * math.sqrt(2)), T0, 0.0]
    best = None
    for ph0 in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        p0[4] = ph0
        try:
            p, c = curve_fit(f, k, y, p0=p0, maxfev=20000)
        except RuntimeError:
            continue
        res = y - f(k, *p)
        chi = float(np.sum(res ** 2))
        if best is None or chi < best[2]:
            best = (p, c, chi)
    p, c, chi = best
    dof = len(k) - 5
    s = math.sqrt(c[3, 3])
    return {"T": float(p[3]), "sT": float(s), "A": float(p[2]), "T_fft": float(T0), "rms": math.sqrt(chi / dof), "n": len(k)}


def battimento(S):
    d = np.asarray(S["omc"], float) - np.asarray(S["om10"], float)
    d = d[K_FIT:]
    b = d.reshape(20, -1).mean(axis=1)
    return float(d.mean()), float(b.std(ddof=1) / math.sqrt(len(b)))


def lettura():
    import gravita_due_corpi_misure as GM
    avvia()
    print("=" * 140)
    print("[M1640-L] IL RESPIRO COME OROLOGIO SENZA ZERO: LE LETTURE (la carta sez. 4-6)")
    print("=" * 140)
    corse = [("N1", 1.0), ("V2", 0.99), ("V2", 1.01), ("V3", 0.99), ("V3", 1.01), ("CTRL", 1.0)]
    R, RHO = {}, {}
    for riga, N in corse:
        d = cartella(riga, N)
        fj = os.path.join(d, "serie_%06d.json" % K_FINO)
        if not os.path.exists(os.path.join(d, "stato_%06d.npz.sha1" % K_FINO)):
            print("    %s %.2f: NON FINITA" % (riga, N))
            continue
        S = json.load(open(fj, encoding="utf-8"))
        fw, fm = fit_respiro(S["kw"], S["w"]), fit_respiro(S["kw"], S["mx"])
        b = battimento(S)
        M = np.asarray(S["M"])
        R[(riga, N)] = {"w": fw, "mx": fm, "b": b, "norma": float(np.max(np.abs(M / M[0] - 1.0))), "om": float(np.mean(S["om"][K_FIT:]))}
        print("    %-4s N %.2f: T(w) %.2f +- %.2f (lo spettro %.0f; A %.3f; rms %.3f, %d punti); T(picco) %.2f +- %.2f; il battimento omega_c - omega_10 %+.5e +- %.1e; omega %+.7f; la norma %.2e" % (
            riga, N, fw["T"], fw["sT"], fw["T_fft"], fw["A"], fw["rms"], fw["n"], fm["T"], fm["sT"], b[0], b[1], R[(riga, N)]["om"], R[(riga, N)]["norma"]))
        RHO[(riga, N)] = {}
        for k in K_RHO:
            X, _m = GM.leggi(os.path.join(d, "stato_%06d.npz" % k))
            nodo_h = None
            RHO[(riga, N)][k] = X
        esito("K1 %s %.2f: arriva a %d, la norma entro 1e-12" % (riga, N, K_FINO), R[(riga, N)]["norma"] < 1e-12, "%.2e" % R[(riga, N)]["norma"])
    print("-" * 140)
    if ("N1", 1.0) in R:
        T1 = R[("N1", 1.0)]["w"]
        esito("K1 a N = 1 il periodo ridà 5125 entro l'1%% (### 5125 E' IL CENTRO DI UN BIN: la carta sez. 5)", abs(T1["T"] / 5125.0 - 1.0) <= 0.01, "T %.2f +- %.2f (%.2f%%)" % (T1["T"], T1["sT"], 100 * (T1["T"] / 5125.0 - 1)))
    # ### K2: rho al bit contro N1, e lo scarto, con CTRL
    if ("N1", 1.0) in RHO:
        with TC.scena() as Z:
            nodo = np.asarray(Z["mot"].inc.nodo)
            n = Z["n"]
            Z["metti"]()

        def rho(X):
            return np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
        print("  K2 / S3: rho contro N1 (max|d rho|/max rho; lo sha1 dei byte di rho)")
        for riga, N in (("V3", 0.99), ("V3", 1.01), ("CTRL", 1.0), ("V2", 0.99), ("V2", 1.01)):
            if (riga, N) not in RHO:
                continue
            riga_s = []
            tutti = True
            for k in K_RHO:
                a, b = rho(RHO[("N1", 1.0)][k]), rho(RHO[(riga, N)][k])
                eq = np.array_equal(a, b)
                tutti = tutti and eq
                riga_s.append("k %d: %s %.3e (%s / %s)" % (k, "AL BIT" if eq else "diverso", float(np.max(np.abs(a - b)) / a.max()), hashlib.sha1(a.tobytes()).hexdigest()[:8], hashlib.sha1(b.tobytes()).hexdigest()[:8]))
            print("    %-4s %.2f: %s" % (riga, N, "; ".join(riga_s)))
            if riga == "V3":
                esito("K2 V3 %.2f: rho AL BIT con N = 1 a k %s" % (N, K_RHO), tutti)
    print("-" * 140)
    out = {}
    for forma in ("V2", "V3"):
        if (forma, 0.99) in R and (forma, 1.01) in R:
            for q in ("w", "mx"):
                a, b = R[(forma, 0.99)][q], R[(forma, 1.01)][q]
                rr = a["T"] / b["T"]
                srr = rr * math.hypot(a["sT"] / a["T"], b["sT"] / b["T"])
                out[(forma, q)] = (rr, srr)
                print("  %s T(0.99)/T(1.01) da %s: %.5f +- %.5f; contro 1.0202 (%+.1f sigma) e 1.0000 (%+.1f sigma)" % (forma, q, rr, srr, (rr - 1.0202) / srr, (rr - 1.0) / srr))
            ba, bb = R[(forma, 0.99)]["b"], R[(forma, 1.01)]["b"]
            if bb[0] != 0.0:
                rb = bb[0] / ba[0]
                srb = abs(rb) * math.hypot(ba[1] / ba[0], bb[1] / bb[0])
                print("  %s il battimento: b(1.01)/b(0.99) %.5f +- %.5f (un orologio che riscala: 1.0202)" % (forma, rb, srb))
                out[(forma, "b")] = (rb, srb)
    if ("V2", "w") in out:
        rr, srr = out[("V2", "w")]
        esito("K3 V2: T(0.99)/T(1.01) = 1.0202 entro 0.003 (dal respiro w)", abs(rr - 1.0202) <= 0.003, "%.5f +- %.5f" % (rr, srr))
    print("=" * 140)
    fall = [k for k, v in OK.items() if v is False]
    nm = [k for k, v in OK.items() if v is None]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s, %d NON MISURATI %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall, len(nm), nm))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("casi_noti", "corsa", "lettura"))
    ap.add_argument("--riga", choices=tuple(RIGHE))
    ap.add_argument("--N", type=float, default=1.0)
    a = ap.parse_args(argv)
    if a.cosa == "casi_noti":
        return casi_noti()
    if a.cosa == "corsa":
        return corsa(a.riga, a.N)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
