# -*- coding: utf-8 -*-
r"""**[M1310-P] IL POUND-REBKA DI G+U: L'OROLOGIO DI UN MATTONE CON L'ALTRO VICINO** *(il mandato di Luca [M1310] delle `13:10`, fase B; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `6`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/pound_rebka_GU.py > doc/referti_l2/pound_rebka_GU.txt

**Gli stati** delle coppie del `14-16/11` *(`E:\soliton_simulator\mattone\coppia<mondo>_L162_<k>.npz`, ogni `500` tick)*; **per mattone** *(le due meta' lungo `A1` dal baricentro di tutta la materia)*: la fase `Phi = arg somma_{r < 15} rho psi_c`; **la frequenza fra stati successivi sciolta con `omega_ref`** = la frequenza dell'orologio-mattone `N1` *([M1253-O], il mattone da solo, la fase a ogni tick)*: `omega = omega_ref + wrap(-dPhi - omega_ref dk)/dk`; **il controllo:** ogni `omega` entro `+-0.006` da `omega_ref` *(se no l'ambiguita' non e' sciolta)*.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402,F401  (i percorsi)
import girandola_chi_v3 as GC  # noqa: E402
import orologio_mattone as OM  # noqa: E402

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "mattone")
COPPIE = (("GU", "B2 in fase, d 35", (500, 1000, 1500, 2000)), ("GUd50", "in fase, d 50", (500, 1000, 1500, 2000)),
          ("GUd65", "in fase, d 65 (L 243)", (500, 1000, 1500)), ("GUpi", "B2-pi in antifase, d 35", (500, 1000, 1500, 2000)))
R_OROLOGIO = 15.0
SCIOLTA = 0.006                 # ### la carta 6.2: meta' di 2 pi/500
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def wrap(x):
    return (x + math.pi) % (2.0 * math.pi) - math.pi


def omega_ref():
    f = os.path.join(OM.BASE, "N1", "fase.npy")
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    F = np.load(f)
    ph = np.unwrap(np.angle(F))
    k = np.arange(len(F), dtype=float)
    m = k >= OM.K_DA_FIT
    A = np.stack([np.ones(m.sum()), k[m]], axis=1)
    b, *_ = np.linalg.lstsq(A, ph[m], rcond=None)
    res = ph[m] - A @ b
    return -float(b[1]), float(np.sqrt(res @ res / (m.sum() - 2))), float(np.std(-np.diff(ph)[OM.K_DA_FIT:]))


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "orologio_mattone.py"))
    _presidio.avvia(os.path.join(_QUI, "girandola_chi_v3.py"))
    _presidio.avvia(__file__)
    w0, rms, sd = omega_ref()
    print("=" * 130)
    print("[M1310-P] IL POUND-REBKA DI G+U (la carta sez. 6): omega_ref (l'orologio N1, il mattone da solo) %.10f per tick (il residuo del fit %.3e rad; la deviazione standard dell'incremento per tick %.3e)" % (w0, rms, sd))
    print("=" * 130)
    esito("P CASO NOTO: il mattone da solo (N1) ha la frequenza costante: il residuo del fit lineare della fase sotto 1 rad su 900 tick", rms < 1.0, "(%.3e rad)" % rms)
    A1 = np.asarray(TO.vettori()[0], float)[:2]
    RIS = {}
    for mondo, nome, ks in COPPIE:
        print("-" * 130)
        righe = []
        for k in ks:
            f = os.path.join(DIR, "coppia%s_L162_%05d.npz" % (mondo, k))
            with np.load(f) as z:
                psi_h, rho_k = z["psi_h"], z["rho"]
                meta = json.loads(str(z["meta"]))
            n = len(rho_k)
            L = int(round(math.sqrt(n)))
            assert L * L == n and psi_h.shape[0] == 6 * n
            nodo = GC.toro_nodo(L)
            rho = np.bincount(nodo, weights=np.sum(np.abs(psi_h) ** 2, axis=1), minlength=n)
            scarto = float(np.max(np.abs(rho - rho_k)) / np.max(rho_k))
            v = np.arange(n)
            m1, m2 = v // L, v % L
            cg = TO.centro(rho, m1, m2, L)[:2]
            dxy = TO.scarti(m1, m2, cg[0], cg[1], L)[:, :2]
            xs = dxy @ (A1 / np.hypot(*A1))
            pn = GC.fase_dei_nodi(psi_h, nodo)
            out = []
            for meta_s in (xs < 0.0, xs >= 0.0):
                b = (dxy[meta_s] * rho[meta_s][:, None]).sum(axis=0) / rho[meta_s].sum()
                dentro = np.hypot(*(dxy - b).T) < R_OROLOGIO
                comp = int(np.argmax([np.sum(np.abs(pn[dentro, j]) ** 2) for j in (0, 1)]))
                out.append((b, complex(np.sum(rho[dentro] * pn[dentro, comp])), comp, float(rho[dentro].sum())))
            d = float(np.hypot(*(out[1][0] - out[0][0])))
            righe.append((k, d, out))
            print("  %-26s k %4d (t %d; sha1 %s): L %d, rho del file contro psi_h %.1e; d %.4f; le fasi %+.5f (comp %d, la massa entro 15 %.4e) e %+.5f (comp %d, %.4e)" % (
                nome, k, meta["t"], sha1(f)[:8], L, scarto, d, np.angle(out[0][1]), out[0][2], out[0][3], np.angle(out[1][1]), out[1][2], out[1][3]))
        om = []
        for (ka, da, oa), (kb, db, ob) in zip(righe, righe[1:]):
            dk = kb - ka
            w = [w0 + wrap(-(np.angle(ob[j][1]) - np.angle(oa[j][1])) - w0 * dk) / dk for j in (0, 1)]
            om.append((ka, kb, 0.5 * (da + db), w))
            print("    k %4d -> %4d, d medio %.4f: omega A %.8f, B %.8f; la media %.8f; omega - omega_ref %+.4e (A %+.4e, B %+.4e)" % (
                ka, kb, 0.5 * (da + db), w[0], w[1], 0.5 * (w[0] + w[1]), 0.5 * (w[0] + w[1]) - w0, w[0] - w0, w[1] - w0))
        RIS[mondo] = (nome, om)
    print("=" * 130)
    tutti = [x for _n, om in RIS.values() for _a, _b, _d, w in om for x in w]
    esito("P CONTROLLO: ogni omega sciolta entro +-%.3f da omega_ref (l'ambiguita' di 2 pi/500 sciolta)" % SCIOLTA, all(abs(x - w0) <= SCIOLTA for x in tutti), "(il massimo %.4e)" % max(abs(x - w0) for x in tutti))
    print("  LA SINTESI: per coppia, omega - omega_ref (la media degli intervalli) e lo scarto fra le due meta'")
    for mondo, (nome, om) in RIS.items():
        dm = [0.5 * (w[0] + w[1]) - w0 for _a, _b, _d, w in om]
        sc = [abs(w[0] - w[1]) for _a, _b, _d, w in om]
        print("    %-26s d medio %.3f: omega - omega_ref %+.4e (da %+.4e a %+.4e); lo scarto A - B medio %.3e" % (nome, float(np.mean([x[2] for x in om])), float(np.mean(dm)), min(dm), max(dm), float(np.mean(sc))))
    print("-" * 130)
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
