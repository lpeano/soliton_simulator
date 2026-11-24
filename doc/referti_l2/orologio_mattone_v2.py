# -*- coding: utf-8 -*-
r"""**[M1253-O] [M1310-A] L'OROLOGIO-MATTONE -- LA V2** *(il mandato di Luca [M1310] delle `13:10`, fase A: la variante V3 anche a `N = 1.0035`, `NpV3`; V1 ai due `N` c'e' gia' *(`Nm`, `Np`)*; la lettura legge tutte e sei; il resto la v1 riga per riga)*. **IL TITOLO DELLA V1: L'OROLOGIO-MATTONE: NEL TEMPO PIU' LENTO IL MATTONE BATTE PIU' PIANO O PIU' VELOCE?** *(la richiesta di Luca delle `12:53`; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `5.2`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/orologio_mattone_v2.py corsa --var NpV3      (N1, Nm, Np, NmV2, NmV3 della v1; qui NpV3; 1000 tick)
    E:\python\py3132\python.exe doc/referti_l2/orologio_mattone_v2.py lettura > doc/referti_l2/orologio_mattone.txt

**La scena** *(`caduta_libera.prepara`: il mattone al centro di S162, senza bordo)*; **`N` UNIFORME** *(nessun gradiente)*: `N1` `1`, `Nm` `0.9965`, `Np` `1.0035` *(cs `= s N` e la forma (a), come V1)*; `NmV2` *(`0.9965`, solo `cs`)*, `NmV3` *(`0.9965`, solo la fase)*. **Il tick** `caduta_segno_v2.tick_var`. **A ogni tick** la fase `Phi = arg somma_{r < 15} rho psi_c` *(la componente del primo semiarco con la norma piu' grande a `k 0`; il centro fisso a `k 0`)*; gli stati a `k 250, 500, 750, 1000`. **La lettura:** `omega = -dPhi/dk` dal fit lineare su `k 100 ... 1000`; `q = omega(N)/omega(1)`; i casi noti *(N1 al bit con V0; `omega(N1)` contro `e0 + 0.1493` entro l'`1%`)*.
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
import girandola_chi_v3 as GC  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402

VAR = {"N1": (1.0, True, +1), "Nm": (0.9965, True, +1), "Np": (1.0035, True, +1), "NmV2": (0.9965, True, 0), "NmV3": (0.9965, False, +1), "NpV3": (1.0035, False, +1)}   # ### Luca 12:53: (N, cs = s N, il segno della fase)
K_FINO = 1000                   # ### Luca
K_DA_FIT = 100                  # ### la carta 5.2: i primi 100 tick fuori (mio, dichiarato)
R_OROLOGIO = 15.0               # ### Luca: entro r 15
G1_CUORE = 0.1493               # ### Luca: G1 del 12/11, il cuore sopra la cima
BASE = os.path.join(CL.BASE, "orologio")
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "girandola_chi_v3.py", "triangolo_chi_v4.py", "orologio_mattone.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def corsa(var):
    avvia()
    from solitone import toro as TO
    _G20, _ia, e0, MT = CL.parametri()
    Nv, cs_N, segno = VAR[var]
    d_out = os.path.join(BASE, var)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info = CL.prepara(Z)
        s = float(Z["s"])
        N = np.full(n, Nv)
        rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
        c = info["centro"]
        dxy = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2] - np.asarray(info["bari_k0"])
        dentro = np.hypot(dxy[:, 0], dxy[:, 1]) < R_OROLOGIO
        pn = GC.fase_dei_nodi(Z["st"]["psi_h"], nodo)
        comp = int(np.argmax([np.sum(np.abs(pn[dentro, j]) ** 2) for j in (0, 1)]))
        print("### l'orologio %s: N %.4f, cs %s, la fase (a) %+d; s %r, e0 %r; i nodi entro r %g: %d; la componente %d; l'impronta di partenza %s" % (
            var, Nv, "s N" if cs_N else "s", segno, s, e0, R_OROLOGIO, int(dentro.sum()), comp, CL.impronta(Z, C)[:12]))

        def fase():
            p = GC.fase_dei_nodi(Z["st"]["psi_h"], nodo)[:, comp]
            r_ = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            return complex(np.sum(r_[dentro] * p[dentro]))
        F = [fase()]
        t1 = time.time()
        for k in range(1, K_FINO + 1):
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            F.append(fase())
            if k % 250 == 0:
                fz = os.path.join(d_out, "stato_%06d.npz" % k)
                dati = {x: Z["st"][x] for x in Z["chiavi"]}
                dati.update(campo_A=C.campo.A, campo_E=C.campo.E, N=N)
                np.savez(fz, meta=np.array(json.dumps(dict(info, variante=var, N=Nv, cs_N=cs_N, segno_fase=segno, s=s, e0=e0, k=k))), **dati)
                open(fz + ".sha1", "w", encoding="utf-8").write(CL.sha1(fz) + "\n")
                print("    [stato] k %d (%.0f s)" % (k, time.time() - t1))
                sys.stdout.flush()
        np.save(os.path.join(d_out, "fase.npy"), np.array(F))
        open(os.path.join(d_out, "fase.npy.sha1"), "w", encoding="utf-8").write(CL.sha1(os.path.join(d_out, "fase.npy")) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_FINO, time.time() - t1))
    return 0


def lettura():
    avvia()
    print("=" * 130)
    print("[M1253-O] L'OROLOGIO-MATTONE (la carta sez. 5.2): omega = -dPhi/dk dal fit lineare su k %d ... %d; q = omega(N)/omega(1)" % (K_DA_FIT, K_FINO))
    print("=" * 130)
    om = {}
    for var in VAR:
        f = os.path.join(BASE, var, "fase.npy")
        if not os.path.exists(f + ".sha1"):
            print("### %s: la corsa non c'e': saltata" % var)
            continue
        assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f), "lo sha1 di %s NON coincide" % f
        F = np.load(f)
        ph = np.unwrap(np.angle(F))
        k = np.arange(len(F), dtype=float)
        m = k >= K_DA_FIT
        A = np.stack([np.ones(m.sum()), k[m]], axis=1)
        b, *_ = np.linalg.lstsq(A, ph[m], rcond=None)
        res = ph[m] - A @ b
        s2 = float(res @ res) / (m.sum() - 2)
        err = math.sqrt(s2 * np.linalg.inv(A.T @ A)[1, 1])
        dph = np.diff(ph)
        om[var] = (-float(b[1]), err)
        print("  %-5s omega %.10f +- %.2e (il residuo rms %.3e rad); l'incremento per tick da %.6f a %.6f; |somma| da %.4e a %.4e" % (
            var, -b[1], err, math.sqrt(s2), float(-dph.max()), float(-dph.min()), float(np.abs(F).min()), float(np.abs(F).max())))
    print("-" * 130)
    if "N1" in om:
        import s5_coppia_lapse as SL
        e0 = float(SL.eps_top_tl4b())
        bit = []
        for kk in (250, 500, 750, 1000):
            Xa, _ = GM.leggi(os.path.join(BASE, "N1", "stato_%06d.npz" % kk))
            Xb, _ = GM.leggi(os.path.join(CL.BASE, "V0", "stato_%06d.npz" % kk))
            bit.append(all(np.array_equal(Xa[x], Xb[x]) for x in ("psi_h", "phi_h", "campo_A", "campo_E")))
        esito("O CASO NOTO: N1 al bit con V0 a k 250, 500, 750, 1000 (psi_h, phi_h, A, E)", all(bit), "(%s)" % bit)
        rif = e0 + G1_CUORE
        esito("O CASO NOTO: omega(N1) = e0 + 0.1493 (G1) entro l'1%%", abs(om["N1"][0] / rif - 1.0) <= 0.01, "(omega %.6f contro %.6f: lo scarto %+.3e)" % (om["N1"][0], rif, om["N1"][0] / rif - 1.0))
        for var, (Nv, _c, _s) in VAR.items():
            if var == "N1" or var not in om:
                continue
            q = om[var][0] / om["N1"][0]
            sq = q * math.hypot(om[var][1] / om[var][0], om["N1"][1] / om["N1"][0])
            nat = (q - 1.0) * (Nv - 1.0) > 0 and abs(abs(q - 1.0) - abs(Nv - 1.0)) <= 0.3 * abs(Nv - 1.0)
            lett = "COME IN NATURA (~N)" if nat else ("AL CONTRARIO (cresce dove N cala)" if (q - 1.0) * (Nv - 1.0) < 0 else "lo stesso verso di N, ma non ~N")
            print("  %-5s N %.4f: q = omega/omega(1) = %.8f +- %.1e; q - 1 = %+.4e contro N - 1 = %+.4e (il rapporto %+.3f): %s" % (var, Nv, q, sq, q - 1.0, Nv - 1.0, (q - 1.0) / (Nv - 1.0), lett))
    print("-" * 130)
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("corsa")
    c.add_argument("--var", choices=tuple(VAR), required=True)
    sub.add_parser("lettura")
    x = ap.parse_args(argv)
    return corsa(x.var) if x.cmd == "corsa" else lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
