# -*- coding: utf-8 -*-
r"""**[M2351] LA SUITE SUL MATTONE DEL FONDO: 5b IL CALCIO** *(la carta `doc/CARTA_torneo_nonlinearita.md`, sez. 13; il task history `doc/TASK_HISTORY/2026-11-22_fondo_suite.md`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_suite.py calcio --sorgente fondo --k 0.010 --asse 1      (sorgente: fondo, F0; k 0 asse 1, k 0.010 assi 1 e 2)
    E:\python\py3132\python.exe doc/referti_l2/fondo_suite.py lettura_calcio > doc/referti_l2/fondo_calcio.txt

**Le sorgenti** *(lo stato a `k 1500`)*: **fondo** = `tenuta_v2/L-1_proiezione_Gamma`, la forma `L-1`; **F0** = `tenuta/S1_cima`, la forma `S1` *(il caso noto)*. **La partenza:** psi, phi, il campo `A`, `E` DAL FILE *(`U` riscritto dal campo)*; la forma coi `pezzi` del NUCLEO dentro la scena *(`ripresa_F0_v2.col_nucleo`, `materia_vuoto.forma_esplicita`)*. **Il centro:** il nodo del massimo della densita' lisciata; **gli scarti `x`** dal baricentro di `rho` *(l'immagine piu' vicina a quel nodo)*. **Il calcio:** `psi_h <- psi_h e^{i k u . x}` *(le righe di `massa_calcio.calcia`)*; il campo NON si ricalcola. **Il tick V0** *(`tick_var`, `N = 1`)*, `1000` tick, il baricentro lungo l'asse ogni `10`. **La lettura:** il fit lineare su `k 200 ... 1000` *(`massa_calcio.velocita`)*; **`m* = k/v` col segno**; **sotto il rumore** se `|v - v(k=0)| < 3 sigma`: allora **`|m*| > k/(3 sigma)`**. **Il caso noto:** F0, la media di m* sui due assi entro il `2%` di `-19.26` *(`massa_calcio.txt`)*.
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
import massa_calcio as MC  # noqa: E402
import ripresa_F0_v2 as RF  # noqa: E402
import torneo_tenuta as TT  # noqa: E402
import torneo_tenuta_v2 as TT2  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M2351")
SORGENTI = {"fondo": (os.path.join(TT2.DIR, "L-1_proiezione_Gamma", "stato_001500.npz"), "L-1"),
            "F0": (os.path.join(TT.DIR, "S1_cima", "stato_001500.npz"), "S1")}
CALCI = ((0.0, 1), (0.010, 1), (0.010, 2))
M_F0, TOLL_F0 = -19.26, 0.02
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "triangolo_chi_v4.py", "massa_calcio.py", "ripresa_F0_v2.py", "torneo_tenuta.py", "torneo_tenuta_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def carica(Z, sorgente):
    """### lo stato a `k 1500` della sorgente nella scena: `(C, info, dxy, forma)`; il campo dal file, `U` dal campo."""
    import gravita_due_corpi_misure as GM
    import _u1_prototipo as U1
    from solitone import toro as TO
    f, forma = SORGENTI[sorgente]
    X, meta = GM.leggi(f)
    C, _info = CL.prepara(Z)
    Z["metti"]({x: X[x] for x in Z["chiavi"]})
    C.campo.A[...] = X["campo_A"]
    C.campo.E[...] = X["campo_E"]
    U1.scrivi_U(Z["mot"], C.campo)
    nodo = np.asarray(Z["mot"].inc.nodo)
    n, L = Z["n"], Z["L"]
    rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
    i = int(np.argmax(TT.lisciata(rho, L)))
    c = (int(Z["m1"][i]), int(Z["m2"][i]))
    d = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2]
    bari = (d * rho[:, None]).sum(axis=0) / rho.sum()
    info = {"centro": list(c), "bari_k0": bari.tolist(), "y_c": float(meta.get("y_c", 0.0)), "massa": float(rho.sum()), "file": f, "k_file": int(meta["k"]), "forma": forma}
    return C, info, d - bari, forma


def nome_calcio(sorgente, k, asse):
    return "calcio_%s_%s" % (sorgente, MC.nome(k, asse))


def calcio(sorgente, k, asse):
    avvia()
    MV, P0 = TT.nucleo()
    _G20, _ia, e0, MT = CL.parametri()
    d_out = os.path.join(BASE, nome_calcio(sorgente, k, asse))
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma = carica(Z, sorgente)
        u = MC.asse_u(asse)
        if k:
            Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * np.exp(1j * float(k) * (dxy @ u))[nodo][:, None]
        s = float(Z["s"])
        N = np.ones(n)
        print("### %s: la sorgente %s (%s, k %d), la forma %s; k %g lungo l'asse %d %s; il centro %s, il baricentro %s; l'impronta %s" % (
            os.path.basename(d_out), sorgente, info["file"], info["k_file"], forma, k, asse, u.tolist(), info["centro"], info["bari_k0"], TT.impronta(Z, C)[:12]))
        serie = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b @ u), float(b[0]), float(b[1]), float(rho.sum()), float(rho.max())))
        misura(0)
        t1 = time.time()
        with RF.col_nucleo(MV, P0), MV.forma_esplicita(forma):
            assert MV.ATTIVA == forma and MV.pezzi is P0
            for kk in range(1, MC.K_FINO + 1):
                CS.tick_var(Z["z"], C.campo, s, e0, N, False, 0)
                if kk % MT.OGNI_GAUSS == 0:
                    C.residuo()
                if kk % MC.OGNI == 0:
                    misura(kk)
                if kk % 250 == 0:
                    print("    k %d: lungo l'asse %+.5f (%.0f s)" % (kk, serie[-1][1], time.time() - t1))
                    sys.stdout.flush()
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"sorgente": sorgente, "k": k, "asse": asse, "serie": serie, "info": info}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s (%.3f s per tick)" % (MC.K_FINO, time.time() - t1, (time.time() - t1) / MC.K_FINO))
    return 0


def lettura_calcio():
    avvia()
    print("=" * 130)
    print("[M2351-M] 5b IL CALCIO DAL k 1500 (la carta sez. 13): v dal fit su k %d ... %d, m* = k/v col segno; sotto il rumore |v - v0| < 3 sigma" % (MC.K_DA_FIT, MC.K_FINO))
    print("=" * 130)
    for sorgente in ("F0", "fondo"):
        R = {}
        for k, asse in CALCI:
            f = os.path.join(BASE, nome_calcio(sorgente, k, asse), "serie.json")
            if not os.path.exists(f + ".sha1"):
                print("  %s: non c'e' ancora" % nome_calcio(sorgente, k, asse))
                continue
            assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f)
            S = json.load(open(f, encoding="utf-8"))["serie"]
            v, sv, rms = MC.velocita(S)
            R[(k, asse)] = (v, sv)
            print("  %-26s v lungo l'asse %+.6e +- %.1e (il residuo %.2e); lo spostamento a k 1000 %+.4f; la norma %.6e -> %.6e" % (
                nome_calcio(sorgente, k, asse), v, sv, rms, S[-1][1] - S[0][1], S[0][4], S[-1][4]))
        if (0.0, 1) not in R:
            continue
        v0, s0 = R[(0.0, 1)]
        ms = []
        for k, asse in CALCI[1:]:
            if (k, asse) not in R:
                continue
            v, sv = R[(k, asse)]
            sg = math.hypot(sv, s0)
            if abs(v - v0) < 3.0 * sg:
                print("    %s asse %d: ### SOTTO IL RUMORE (|v - v0| %.2e < 3 sigma %.2e): |m*| > k/(3 sigma) = %.1f" % (sorgente, asse, abs(v - v0), 3 * sg, k / (3 * sg)))
            else:
                ms.append(k / v)
                print("    %s asse %d: m* = k/v = %+.3f +- %.3f (con v - v0: %+.3f)" % (sorgente, asse, k / v, abs(k / v) * sv / abs(v), k / (v - v0)))
        if ms:
            print("  %s: m*_sol %s, la media %+.3f" % (sorgente, ", ".join("%+.3f" % x for x in ms), float(np.mean(ms))))
        if sorgente == "F0":
            esito("il caso noto: F0 da k 1500, m* media entro il %g%% di %+.2f" % (100 * TOLL_F0, M_F0), len(ms) == 2 and abs(float(np.mean(ms)) / M_F0 - 1.0) <= TOLL_F0,
                  "(%s)" % ("%+.3f" % float(np.mean(ms)) if ms else "nessuna"))
    print("=" * 130)
    return 0 if all(ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("calcio", "lettura_calcio"))
    ap.add_argument("--sorgente", choices=sorted(SORGENTI))
    ap.add_argument("--k", type=float)
    ap.add_argument("--asse", type=int, choices=(1, 2))
    a = ap.parse_args(argv)
    if a.cosa == "calcio":
        return calcio(a.sorgente, a.k, a.asse)
    return lettura_calcio()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
