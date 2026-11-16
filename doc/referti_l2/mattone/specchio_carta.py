# -*- coding: utf-8 -*-
r"""**LA CARTA DELLO SPECCHIO, C1 E C2** *(Luca `2026-11-16` `10:43`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24.40`; SOLO calcoli su stati salvati e riflessi)*.

    E:\python\py3132\python.exe doc/referti_l2/mattone/specchio_carta.py > doc/referti_l2/mattone/specchio_carta.txt     (PYTHONNOUSERSITE=1, TMP su E:)

**Lo specchio:** la retta a `30` gradi *(la direzione `2 A1 + A2`)* per il nodo piu' vicino al vertice A del triangolo a `k 0` *(la serie)*; `x, y` da `toro.vettori`.
**C1:** `phi_v` riflesso *(per estremita')* contro `phi_v`, `-phi_v`, `conj(phi_v)`, `e^{i alpha} phi_v`.
**C2:** dallo stato `triangolo_t120_00500` *(col campo)*: `R(tick^N(x))` contro `tick^N(R(x))`, il tick di `mattone.Campi` (MGU) nella scena del triangolo *(il bordo `R_A_SCENA` attorno a `c0`)*;
`R`: i nodi e le estremita' permutati, lo spinore per `T` *(e il coniugio, se chiesto)*, `phi` per `+1` o `-1` *(e il coniugio)*, `A` ed `E` per arco col segno del verso per `+1` o `-1`.
"""
import itertools
import json
import math
import os
import sys
import time

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

N_LUNGO = 10
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def mappa_nodi(L, m1, m2, p0, ang):
    """### `sigma[v]`: il nodo immagine; lo scarto massimo della posizione riflessa dal nodo trovato."""
    A1, A2 = TO.vettori()
    Bm = np.column_stack([A1, A2])
    Bi = np.linalg.inv(Bm)
    P = np.outer(m1 - p0[0], A1) + np.outer(m2 - p0[1], A2)
    c, s = math.cos(2 * ang), math.sin(2 * ang)
    M = np.array([[c, s], [s, -c]])
    Q = P @ M.T
    q = Q @ Bi.T
    qi = np.rint(q)
    scarto = float(np.max(np.abs(q - qi)))
    n1 = (qi[:, 0].astype(int) + int(p0[0])) % L
    n2 = (qi[:, 1].astype(int) + int(p0[1])) % L
    return n1 * L + n2, scarto, M


def mappa_archi(ii, jj, sig):
    """### `(a', rovescio)` per ogni arco `(ii, jj)`: l'arco immagine e se il verso si rovescia."""
    chiave = {}
    for a, (i, j) in enumerate(zip(ii, jj)):
        chiave[(int(i), int(j))] = a
    ap = np.empty(len(ii), dtype=int)
    rov = np.empty(len(ii), dtype=bool)
    for a, (i, j) in enumerate(zip(ii, jj)):
        x, y = int(sig[i]), int(sig[j])
        if (x, y) in chiave:
            ap[a], rov[a] = chiave[(x, y)], False
        else:
            ap[a], rov[a] = chiave[(y, x)], True
    return ap, rov


def main():
    import _presidio
    import _u1_prototipo as U1
    import mattone_triangolo as MTR
    from solitone import bordo as BO
    _presidio.avvia(os.path.join(_SOL, "mattone.py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("LA CARTA DELLO SPECCHIO, C1 E C2 (Luca 2026-11-16 10:43; solo calcoli); sys.executable %s" % sys.executable)
    print("=" * 130)
    s = np.load(os.path.join(MT.DIR_REF, "triangolo_t120_serie.npz"))
    V = {q: (float(s["c1_" + q][0]), float(s["c2_" + q][0])) for q in "ABC"}
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        v = np.arange(n)
        m1, m2 = v // L, v % L
        mot = Z["mot"]
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
        A1, A2 = TO.vettori()
        d30 = 2 * A1 + A2
        ang = math.atan2(d30[1], d30[0])
        p0 = (int(round(V["A"][0])), int(round(V["A"][1])))
        sig, scarto, M = mappa_nodi(L, m1.astype(float), m2.astype(float), p0, ang)
        print("### LO SPECCHIO: la retta a %.4f gradi per il nodo %s (il vertice A a k 0 = (%.2f, %.2f)); lo scarto massimo della mappa dei nodi %.2e" % (math.degrees(ang), p0, V["A"][0], V["A"][1], scarto))
        assert scarto < 1e-9, "la retta NON e' una retta di specchio del reticolo: FERMO"
        assert np.array_equal(np.sort(sig), v) and np.array_equal(sig[sig], v), "la mappa dei nodi non e' una involuzione biunivoca"
        Bi = np.linalg.inv(np.column_stack([A1, A2]))

        def immagine_indici(c):
            P = (c[0] - p0[0]) * A1 + (c[1] - p0[1]) * A2
            q = Bi @ (M @ P)
            return (q[0] + p0[0], q[1] + p0[1])
        for q in "ABC":
            im = immagine_indici(V[q])
            print("    il vertice %s (%.2f, %.2f) -> (%.2f, %.2f)" % (q, V[q][0], V[q][1], im[0], im[1]))
        imc0 = immagine_indici(c0)
        print("    il centro del bordo c0 (%.3f, %.3f) -> (%.3f, %.3f): la distanza %.3f nodi" % (c0[0], c0[1], imc0[0], imc0[1], MT.distanza(L, tuple(c0), imc0)))
        ge = np.asarray(Z["g_e"])
        # ---------------------------------------------------------------- gli archi della passeggiata
        nodo = np.asarray(mot.inc.nodo)
        ii, jj = nodo[0::2], nodo[1::2]
        ap, rov = mappa_archi(ii, jj, sig)
        hp = np.empty(2 * len(ap), dtype=int)
        hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
        hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
        assert np.array_equal(nodo[hp], sig[nodo]), "la mappa delle estremita' non porta il nodo giusto"
        print("### gli archi della passeggiata: %d, rovesciati %d" % (len(ap), int(rov.sum())))
        nv = mot.geo.n
        Mn = np.column_stack([nv[:, :2] @ M.T, nv[:, 2]])
        print("    i versori: max |n[h'] - M n[h]| (nel piano, z uguale) %.3e; max |n[h'] - M n[h]| con z -> -z %.3e" % (
            float(np.max(np.abs(nv[hp] - Mn))), float(np.max(np.abs(nv[hp] - np.column_stack([Mn[:, :2], -Mn[:, 2]]))))))
        g_rifl = ge[hp] if ge.shape[0] == 2 * len(ap) else ge[sig]
        print("    il bordo g_e riflesso contro g_e: max |differenza| %.3e (max g_e %.3e)" % (float(np.max(np.abs(g_rifl - ge))), float(np.max(np.abs(ge)))))
        # ---------------------------------------------------------------- C1
        phv = np.asarray(Z["phi_v"])
        pr = np.empty_like(phv)
        pr[hp] = phv
        sc = float(np.max(np.abs(phv)))
        al = float(np.angle(np.sum(np.conj(phv) * pr)))
        print("### C1: phi_v riflesso (per estremita') contro:")
        for nome, x in (("phi_v", phv), ("-phi_v", -phv), ("conj(phi_v)", np.conj(phv)), ("-conj(phi_v)", -np.conj(phv)), ("e^{i alpha} phi_v, alpha = %.6f" % al, np.exp(1j * al) * phv)):
            print("    %-36s la differenza relativa %.3e" % (nome, float(np.max(np.abs(pr - x))) / sc))
        # ---------------------------------------------------------------- C2: gli archi del campo
        f5 = os.path.join(MT.DIR_E, "triangolo_t120_00500.npz")
        with np.load(f5) as d:
            X0 = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
            t5 = int(json.loads(str(d["meta"]))["t"])
        C = MT.Campi(Z, "MGU", rho_c, e)
        cap, crov = mappa_archi(C.campo.ii, C.campo.jj, sig)
        segno_a = np.where(crov, -1.0, 1.0)
        print("### C2: gli archi del campo %d, rovesciati %d; lo stato triangolo_t120_00500 (t %d); %s" % (len(cap), int(crov.sum()), t5, {k: X0[k].shape for k in X0}))
        righe = Z["righe"]

        def rifletti(X, A, E, T, cj, ps, sa):
            Y = {}
            for k, a in X.items():
                if k == "psi_h":
                    b = np.conj(a) if cj else a
                    y = np.empty_like(a)
                    y[hp] = b @ T.T
                    Y[k] = y
                elif k == "psi":
                    b = np.conj(a) if cj else a
                    y = np.empty_like(a)
                    y[sig] = b @ T.T
                    Y[k] = y
                elif k == "phi_h":
                    b = np.conj(a) if cj else a
                    y = np.empty_like(a)
                    y[hp] = ps * b
                    Y[k] = y
                elif a.shape[0] == n:
                    y = np.empty_like(a)
                    y[sig] = a
                    Y[k] = y
                elif a.shape[0] == 2 * len(ap):
                    y = np.empty_like(a)
                    y[hp] = a
                    Y[k] = y
                else:
                    raise RuntimeError("la chiave %s di forma %s: non so rifletterla" % (k, a.shape))
            Ar = np.empty_like(A)
            Er = np.empty_like(E)
            Ar[cap] = sa * segno_a * A
            Er[cap] = sa * segno_a * E
            return Y, Ar, Er

        def corri(X, A, E, N):
            Z["metti"]({k: v_.copy() for k, v_ in X.items()})
            Cx = MT.Campi(Z, "MGU", rho_c, e)
            Cx.campo.A[...] = A
            Cx.campo.E[...] = E
            Cx.campo.e = e
            Cx.e_prec = e
            U1.scrivi_U(Z["mot"], Cx.campo)
            for k in range(1, N + 1):
                Cx.tick(500 + k, t5 + k, 1.0, e)
            return {k: Z["st"][k].copy() for k in X}, Cx.campo.A.copy(), Cx.campo.E.copy()

        bar = (sum(V[q][0] for q in "ABC") / 3.0, sum(V[q][1] for q in "ABC") / 3.0)
        vicino_n = np.hypot(*TO.scarti(m1, m2, bar[0], bar[1], L).T[:2]) <= 40.0
        vicino_h = vicino_n[nodo]
        print("    il confronto si stampa su TUTTO il toro e, a parte, entro 40 nodi dal baricentro (%.2f, %.2f) (lontano dal bordo, che non e' simmetrico)" % bar)

        def diff(P, Q):
            out = {}
            for k in ("psi_h", "phi_h"):
                out[k] = float(np.max(np.abs(P[0][k] - Q[0][k]))) / float(np.max(np.abs(Q[0][k])))
                out[k + " (40)"] = float(np.max(np.abs(P[0][k][vicino_h] - Q[0][k][vicino_h]))) / float(np.max(np.abs(Q[0][k])))
            out["A"] = float(np.max(np.abs(P[1] - Q[1]))) / max(float(np.max(np.abs(Q[1]))), 1e-300)
            return out
        l = np.array([math.cos(ang), math.sin(ang)])
        lp = np.array([-math.sin(ang), math.cos(ang)])
        Ts = [("I", np.eye(2, dtype=complex)), ("sigma_x", SX), ("sigma_y", SY), ("sigma_z", SZ),
              ("sigma.l", l[0] * SX + l[1] * SY), ("sigma.l_perp", lp[0] * SX + lp[1] * SY)]
        t1 = time.time()
        Y1 = corri(X0, A0, E0, 1)
        print("    un tick dallo stato vero: %.1f s" % (time.time() - t1))
        risultati = []
        for (tn, T), cj, ps, sa in itertools.product(Ts, (False, True), (1.0, -1.0), (1.0, -1.0)):
            R1 = rifletti(Y1[0], Y1[1], Y1[2], T, cj, ps, sa)
            X0r = rifletti(X0, A0, E0, T, cj, ps, sa)
            Y2 = corri(X0r[0], X0r[1], X0r[2], 1)
            dd = diff(Y2, R1)
            risultati.append((max(dd["psi_h (40)"], dd["phi_h (40)"]), tn, cj, ps, sa, dd))   # ### l'ordine: entro 40 nodi (il bordo non e' simmetrico)
            print("    T %-13s coniugio %-5s phi %+.0f A %+.0f: dopo 1 tick psi_h %.3e (entro 40: %.3e), phi_h %.3e (%.3e), A %.3e" % (tn, cj, ps, sa, dd["psi_h"], dd["psi_h (40)"], dd["phi_h"], dd["phi_h (40)"], dd["A"]))
            sys.stdout.flush()
        risultati.sort(key=lambda x: x[0])
        print("### I MIGLIORI su %d tick:" % N_LUNGO)
        YL = corri(X0, A0, E0, N_LUNGO)
        lungo = []
        for _m, tn, cj, ps, sa, _d in risultati[:2]:
            T = dict(Ts)[tn]
            RL = rifletti(YL[0], YL[1], YL[2], T, cj, ps, sa)
            X0r = rifletti(X0, A0, E0, T, cj, ps, sa)
            Y2 = corri(X0r[0], X0r[1], X0r[2], N_LUNGO)
            dd = diff(Y2, RL)
            lungo.append((max(dd.values()), tn, cj, ps, sa, max(dd["psi_h (40)"], dd["phi_h (40)"])))
            print("    T %-13s coniugio %-5s phi %+.0f A %+.0f: dopo %d tick psi_h %.3e (entro 40: %.3e), phi_h %.3e (%.3e), A %.3e" % (tn, cj, ps, sa, N_LUNGO, dd["psi_h"], dd["psi_h (40)"], dd["phi_h"], dd["phi_h (40)"], dd["A"]))
        Z["metti"]()
    best = min(lungo)
    best40 = min(lungo, key=lambda x: x[5])
    print("### entro 40 nodi dal baricentro, il migliore: T %s, coniugio %s, phi %+.0f, A %+.0f: %.3e" % (best40[1], best40[2], best40[3], best40[4], best40[5]))
    print("-" * 130)
    print("### C2, LA LETTURA (fissata prima: esiste se dopo %d tick la differenza relativa < 1e-10): %s" % (
        N_LUNGO, ("ESISTE: T %s, coniugio %s, phi %+.0f, A %+.0f (%.3e)" % (best[1], best[2], best[3], best[4], best[0])) if best[0] < 1e-10 else
        ("NON ESISTE FRA QUESTI CANDIDATI: il migliore T %s, coniugio %s, phi %+.0f, A %+.0f da' %.3e" % (best[1], best[2], best[3], best[4], best[0]))))
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
