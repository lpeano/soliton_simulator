# -*- coding: utf-8 -*-
r"""**LA CONVENZIONE DEI SEGNI SU UN CASO NOTO** *(Luca `2026-11-16` `10:39`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24.38`; SOLO LETTURA e stati costruiti a mano)*.

    E:\python\py3132\python.exe doc/referti_l2/mattone/segni_vortice.py > doc/referti_l2/mattone/segni_vortice.txt     (PYTHONNOUSERSITE=1, TMP su E:)

**Gli stati costruiti a mano** *(la scena S162, `L 162`, il centro nel nodo `(81, 81)`; `r`, `theta` da `toro.scarti`, `theta = atan2(y, x)`)*:
  - **il vortice:** `psi(v) = A0 f(r) e^{+i s theta(v)} u`, `f(r) = exp(-((r - 15)/5)^2)`, `s = +1` o `-1`; `u` = lo spinore *(12 componenti)* del nodo col `rho` massimo di
    `L162_MGU_03000.npz`, normalizzato; `A0` = la sua norma; `psi = 0` altrove; il vuoto `phi` quello della scena;
  - **l'`A` rotante:** `A_k = x_k dy_k - y_k dx_k` *(`(x_k, y_k)` il punto medio dell'arco `k` dal centro, `(dx_k, dy_k)` il vettore da `ii` a `jj`)*: la circolazione ANTIORARIA;
  - **la forma:** `rho(v) = f(r) (1 + 0.5 cos(3 (theta - phi0)))`, `phi0` in `{0, +10, -10}` gradi.
"""
import importlib.util
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(os.path.dirname(_QUI)))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_SOL, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
from solitone import toro as TO  # noqa: E402

CENTRO = (81.0, 81.0)
R_ANELLO, W_ANELLO = 15.0, 5.0
R_DISCO, R_FLUSSO, R_L = 8.0, 30.0, 40.0


def carica_rotazione():
    f = os.path.join(_QUI, "triangolo_rotazione_B.py")
    spec = importlib.util.spec_from_file_location("triangolo_rotazione_B", f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    import _presidio
    import energia as EN
    import triangolo_120 as T120
    _presidio.avvia(os.path.join(_SOL, "mattone.py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(os.path.join(_SOL, "triangolo_120.py"))
    _presidio.avvia(os.path.join(_QUI, "triangolo_rotazione_B.py"))
    _presidio.avvia(__file__)
    RB = carica_rotazione()
    print("=" * 130)
    print("LA CONVENZIONE DEI SEGNI SU UN CASO NOTO (Luca 2026-11-16 10:39; solo lettura); sys.executable %s" % sys.executable)
    print("=" * 130)
    A1, A2 = TO.vettori()
    croce = float(A1[0] * A2[1] - A1[1] * A2[0])
    print("### 1. GLI ASSI: A1 = %s, A2 = %s; A1 x A2 = %+.4f (%s)" % (A1.tolist(), A2.tolist(), croce, "la base e' DESTRA: (m1, m2) -> (x, y) conserva il verso" if croce > 0 else "### la base e' SINISTRA"))
    esiti = []
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        D = TO.scarti(m1, m2, CENTRO[0], CENTRO[1], L)
        dx, dy = D[:, 0], D[:, 1]
        r = np.hypot(dx, dy)
        th = np.arctan2(dy, dx)
        for nome, bersaglio in (("+x", (5.0, 0.0)), ("+y", (0.0, 5.0))):
            j = int(np.argmin((dx - bersaglio[0]) ** 2 + (dy - bersaglio[1]) ** 2))
            print("    il nodo piu' vicino a %s = %s dal centro: (m1, m2) = (%d, %d), (x, y) = (%+.3f, %+.3f), theta = %+.2f gradi" % (nome, bersaglio, m1[j], m2[j], dx[j], dy[j], math.degrees(th[j])))
        j0 = int(np.argmin((dx - 5) ** 2 + dy ** 2))
        j1 = int(np.argmin(dx ** 2 + (dy - 5) ** 2))
        esiti.append(("1. theta: +x circa 0 gradi, +y circa 90 gradi (entro 15)", abs(math.degrees(th[j0])) < 15 and abs(math.degrees(th[j1]) - 90) < 15))
        # ---------------------------------------------------------------- Campo.B su un A rotante
        C = MT.Campi(Z, "MU", rho_c, e)
        cam = C.campo
        p1 = np.concatenate([m1 + 2.0 / 3.0, m1 + 1.0 / 3.0])
        p2 = np.concatenate([m2 + 1.0 / 3.0, m2 + 2.0 / 3.0])
        rp = np.hypot(*TO.scarti(p1, p2, CENTRO[0], CENTRO[1], L).T[:2])
        ci, cj = cam.ii, cam.jj
        dd = TO.scarti(m1[cj], m2[cj], m1[ci], m2[ci], L)
        mx, my = dx[ci] + 0.5 * dd[:, 0], dy[ci] + 0.5 * dd[:, 1]
        cam.A[...] = mx * dd[:, 1] - my * dd[:, 0]
        B = cam.B()
        bm = float(B[rp <= R_DISCO].mean())
        print("    Campo.B sull'A ROTANTE antiorario (A_k = x dy - y dx): B medio nel disco %g %+.4e, il minimo %+.4e, il massimo %+.4e" % (R_DISCO, bm, float(B[rp <= R_DISCO].min()), float(B[rp <= R_DISCO].max())))
        esiti.append(("1. Campo.B di una circolazione ANTIORARIA e' POSITIVO", bm > 0))
        cam.A[...] = 0.0
        # ---------------------------------------------------------------- lo spinore u
        with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d0:
            Z["metti"]({x: d0[x].copy() for x in Z["chiavi"]})
        psin = Z["st"]["psi_h"][Z["righe"]].reshape(n, -1)
        jm = int(np.argmax(np.sum(np.abs(psin) ** 2, axis=1)))
        A0 = float(np.linalg.norm(psin[jm]))
        u = (psin[jm] / A0).reshape(Z["righe"].shape[1], -1)
        print("### 2. IL VORTICE: u = lo spinore del nodo %d di L162_MGU_03000 (la norma A0 = %.6e)" % (jm, A0))
        f = np.exp(-((r - R_ANELLO) / W_ANELLO) ** 2)
        mot = Z["mot"]
        ii, jj = np.asarray(mot.inc.ii), np.asarray(mot.inc.jj)
        de = TO.scarti(m1[jj], m2[jj], m1[ii], m2[ii], L)
        ex, ey = dx[ii] + 0.5 * de[:, 0], dy[ii] + 0.5 * de[:, 1]
        dentro = np.hypot(ex, ey) <= R_L
        segni = {}
        for s in (+1, -1):
            Z["metti"]()
            st = Z["st"]
            st["psi_h"][...] = 0.0
            amp = A0 * f * np.exp(1j * s * th)
            st["psi_h"][Z["righe"]] = amp[:, None, None] * u[None, :, :]
            ps = st["psi_h"][Z["righe"]].reshape(n, -1)
            g = T120.giro_di(np.concatenate([ps, ps.sum(axis=1, keepdims=True)], axis=1), m1, m2, L, CENTRO, R_ANELLO)
            J = np.asarray(EN.corrente(st, mot, Z["par"], None), dtype=float)
            Le = float(np.sum((J * (ex * de[:, 1] - ey * de[:, 0]))[dentro]))
            jf = np.imag(np.sum(np.conj(ps[ii]) * ps[jj], axis=1))
            Lf = float(np.sum((jf * (ex * de[:, 1] - ey * de[:, 0]))[dentro]))
            Bt = {}
            C = MT.Campi(Z, "MU", rho_c, e)
            for k in range(1, 4):
                C.tick(k, MT.T_162 + k, 1.0, e)
                if k in (1, 3):
                    Bk = C.campo.B()
                    Bt[k] = (float(Bk[rp <= R_DISCO].mean()), float(Bk[rp <= R_FLUSSO].sum()))
            segni[s] = (g, Le, Lf, Bt)
            print("  s = %+d: il giro (le 12 componenti) %s; la somma %+.3f" % (s, " ".join("%+.2f" % x for x in g[:-1]), g[-1]))
            print("          L dalla corrente di ENERGIA (energia.corrente) %+.6e; L dalla corrente di FASE Im(sum conj(psi_ii) psi_jj) %+.6e" % (Le, Lf))
            print("          B dalla dinamica (MU): dopo 1 tick nel disco %g %+.4e (il flusso entro %g %+.4e); dopo 3 tick %+.4e (%+.4e)" % (R_DISCO, Bt[1][0], R_FLUSSO, Bt[1][1], Bt[3][0], Bt[3][1]))
            sys.stdout.flush()
            esiti.append(("2a. s = %+d: il giro della somma = %+d (entro 0.1)" % (s, s), abs(g[-1] - s) < 0.1))
            esiti.append(("2b. s = %+d: L dalla corrente di FASE ha il segno %+d" % (s, s), Lf * s > 0))
        Z["metti"]()
    # ---------------------------------------------------------------- 3. la forma
    print("### 3. LA FORMA m=3 RUOTATA (la m=3 di triangolo_rotazione_B.forma, l'angolo = -(arg S - arg S0)/3)")
    rho0 = None
    a0 = None
    for phi0 in (0.0, 10.0, -10.0):
        rho = f * (1.0 + 0.5 * np.cos(3.0 * (th - math.radians(phi0))))
        a, amp, _I, cen = RB.forma(rho, m1, m2, L)
        if a0 is None:
            a0 = a
        ang = -math.degrees(math.atan2(math.sin(a - a0), math.cos(a - a0))) / 3.0
        print("    phi0 %+5.1f: l'angolo misurato %+.4f gradi; l'ampiezza %.4f; il centro (%.3f, %.3f)" % (phi0, ang, amp, cen[0], cen[1]))
        if phi0 != 0.0:
            esiti.append(("3. la forma ruotata di %+.0f gradi -> %+.0f (entro 0.1)" % (phi0, phi0), abs(ang - phi0) < 0.1))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-100s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    tutti = all(ok for _n, ok in esiti)
    gp, Lep, Lfp, Btp = segni[+1]
    print("=" * 130)
    print("### IL VERDETTO (la carta): %s" % ("S1: le convenzioni sono COERENTI (il giro, la corrente di fase, Campo.B, la forma)" if tutti else "### S2: una convenzione e' rovesciata: vedi i DEVE che falliscono"))
    print("    E, rispetto alla corrente di FASE del vortice s = +1 (L_fase %+.3e):" % Lfp)
    print("      L dalla corrente di ENERGIA %+.3e: %s" % (Lep, "lo STESSO verso" if Lep * Lfp > 0 else "### il verso OPPOSTO"))
    print("      B dalla dinamica (MU) dopo 3 tick %+.3e: %s" % (Btp[3][0], "lo STESSO verso" if Btp[3][0] * Lfp > 0 else ("### il verso OPPOSTO" if Btp[3][0] != 0 else "zero")))
    print("=" * 130)
    return 0 if tutti else 1


if __name__ == "__main__":
    sys.exit(main())
