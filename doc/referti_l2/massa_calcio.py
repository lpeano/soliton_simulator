# -*- coding: utf-8 -*-
r"""**[M1446-M] LA MASSA DEL SOLITONE COL CALCIO** *(il mandato di Luca [M1446], corsia M; la carta `doc/CARTA_E_mc2.md`, sez. `M`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/massa_calcio.py corsa --k 0.010 --asse 1      (k 0, 0.005, 0.010; asse 1 = A1, 2 = A2; 1000 tick)
    E:\python\py3132\python.exe doc/referti_l2/massa_calcio.py lettura > doc/referti_l2/massa_calcio.txt

**La scena** `caduta_libera.prepara` *(il mattone al centro di S162)*, `N = 1`, il tick V0 *(`caduta_segno_v2.tick_var` con `N = 1`, `cs = s`, la fase spenta)*. **Il calcio:** `psi_h <- psi_h e^{i k . x}` per nodo *(`x` dal centro del mattone, l'immagine piu' vicina; `k` lungo l'asse)*, **prima di `porto.campi`** *(il campo dalla materia calciata: `rho` non cambia)*. **Il baricentro di `rho` ogni `10` tick**; **la lettura:** il fit lineare lungo l'asse su `k 200 ... 1000`, `m* = k/v` col segno.
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
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1446", "calcio")
K_FINO, OGNI, K_DA_FIT = 1000, 10, 200          # ### la carta: 1000 tick, il baricentro ogni 10, il transitorio 200 (mio)
CORSE = ((0.0, 1), (0.010, 1), (0.010, 2), (0.005, 1), (0.005, 2))
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def nome(k, asse):
    return "k%05.3f_a%d" % (k, asse)


def asse_u(asse):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    a = np.asarray(A1 if asse == 1 else A2, float)[:2]
    return a / np.hypot(*a)


def calcia(Z, info, k, asse):
    """### la fase `e^{i k u . x}` per nodo sui semiarchi di `psi_h`."""
    from solitone import toro as TO
    c = info["centro"]
    dxy = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"])[:, :2] - np.asarray(info["bari_k0"])
    f = np.exp(1j * float(k) * (dxy @ asse_u(asse)))
    nodo = np.asarray(Z["mot"].inc.nodo)
    Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * f[nodo][:, None]
    return dxy


def scena_calciata(Z, k, asse, scala=1.0):
    """### `caduta_libera.prepara`, poi la norma (eotvos) e il calcio, poi `porto.campi` di nuovo. `(C, info, dxy)`."""
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    _C, info = CL.prepara(Z)
    if scala != 1.0:
        Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * math.sqrt(float(scala))
    dxy = calcia(Z, info, k, asse) if k else None
    if dxy is None:
        from solitone import toro as TO
        c = info["centro"]
        dxy = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"])[:, :2] - np.asarray(info["bari_k0"])
    C = PO.campi(Z, MT.rho_c_assoluto(), MT.PB.E_DECISO)
    return C, info, dxy


def corsa(k, asse, scala=1.0, base=BASE, etichetta=None):
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "triangolo_chi_v4.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    _G20, _ia, e0, MT = CL.parametri()
    nm = etichetta or nome(k, asse)
    d_out = os.path.join(base, nm)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy = scena_calciata(Z, k, asse, scala)
        s = float(Z["s"])
        N = np.ones(n)
        u = asse_u(asse)
        print("### il calcio %s: k %g lungo l'asse %d %s; la norma x %g; il centro %s; l'impronta di partenza %s" % (nm, k, asse, u.tolist(), scala, info["centro"], CL.impronta(Z, C)[:12]))
        serie = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b @ u), float(b[0]), float(b[1]), float(rho.sum()), float(rho.max())))
        misura(0)
        t1 = time.time()
        for kk in range(1, K_FINO + 1):
            CS.tick_var(Z["z"], C.campo, s, e0, N, False, 0)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            if kk % OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: lungo l'asse %+.5f (%.0f s)" % (kk, serie[-1][1], time.time() - t1))
                sys.stdout.flush()
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"k": k, "asse": asse, "scala": scala, "serie": serie, "info": {x: info[x] for x in ("centro", "bari_k0", "y_c", "massa")}}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_FINO, time.time() - t1))
    return 0


def velocita(serie):
    s = np.array(serie)
    m = s[:, 0] >= K_DA_FIT
    A = np.stack([np.ones(m.sum()), s[m, 0]], axis=1)
    b, *_ = np.linalg.lstsq(A, s[m, 1], rcond=None)
    r = s[m, 1] - A @ b
    cov = float(r @ r) / (m.sum() - 2) * np.linalg.inv(A.T @ A)
    return float(b[1]), math.sqrt(cov[1, 1]), math.sqrt(float(r @ r) / (m.sum() - 2))


def lettura():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1446-M] LA MASSA DEL SOLITONE COL CALCIO (la carta sez. M): v dal fit su k %d ... %d, m* = k/v" % (K_DA_FIT, K_FINO))
    print("=" * 130)
    R = {}
    for k, asse in CORSE:
        f = os.path.join(BASE, nome(k, asse), "serie.json")
        if not os.path.exists(f + ".sha1"):
            print("  %s: non c'e' ancora" % nome(k, asse))
            continue
        assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f)
        S = json.load(open(f, encoding="utf-8"))["serie"]
        v, sv, rms = velocita(S)
        R[(k, asse)] = (v, sv)
        ms = (k / v) if k else float("nan")
        print("  %s: v lungo l'asse %+.6e +- %.1e (il residuo %.2e); lo spostamento a k 1000 %+.4f; la norma da %.6e a %.6e; m* = k/v = %s" % (
            nome(k, asse), v, sv, rms, S[-1][1] - S[0][1], S[0][4], S[-1][4], ("%+.3f +- %.3f" % (ms, abs(ms) * sv / abs(v))) if k else "-"))
    print("-" * 130)
    if (0.0, 1) in R:
        v, sv = R[(0.0, 1)]
        esito("K1-M: a k = 0 il mattone fermo (v entro 3 sigma da 0)", abs(v) <= 3.0 * sv, "(%+.2e +- %.1e)" % (v, sv))
    ms = [k / R[(k, a)][0] for k, a in CORSE if k and (k, a) in R]
    if ms:
        print("  m*_sol: %s; la media %+.3f" % (", ".join("%+.3f" % x for x in ms), float(np.mean(ms))))
        esito("K2: m*_sol NEGATIVA (se positiva la lettura del guardiano cade)", all(x < 0 for x in ms), "(%s)" % ", ".join("%+.2f" % x for x in ms))
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("corsa")
    c.add_argument("--k", type=float, required=True)
    c.add_argument("--asse", type=int, choices=(1, 2), required=True)
    sub.add_parser("lettura")
    x = ap.parse_args(argv)
    return corsa(x.k, x.asse) if x.cmd == "corsa" else lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
