# -*- coding: utf-8 -*-
r"""**CP E CPT, PEZZO PER PEZZO: CHI ROMPE** *(Luca `2026-11-17` `11:33`, B3: «se nessuno commuta: pezzo per pezzo chi rompe»; DOPO `simmetria_CP.txt`)*.

    E:\python\py3132\python.exe doc/referti_l2/simmetria_CP_pezzi.py > doc/referti_l2/simmetria_CP_pezzi.txt     (PYTHONNOUSERSITE=1, 1 filo, numba spento)

**I candidati** *(i migliori di `simmetria_CP.txt`, scelti DOPO lo schermo e scritti qui)*: **CPT** `inv, T sy, phi -> -conj(phi), sA -1, sE +1` *(il migliore)* e `sA -1, sE -1`; **CP** `spec, T s.l.sy, phi, sA +1, sE +1` *(il migliore di CP)*.
**Per ogni pezzo `Q`** *(come `simmetria_C_pezzi.py`: `campo.spinta(0.5)`, `fase_a`, `reazione(0.5)`, i sette pezzi della prima meta' di `composizione.ORDINE`, il tick)*: **CP:** `Theta(Q(x))` contro `Q(Theta(x))`; **CPT:** `Q(Theta(Q(x)))` contro `Theta(x)` *(un pezzo rovesciato dall'antiunitario)*. **Il controllo positivo:** l'identita' *(nessuna mappa, nessun coniugio)* nella forma CP da' `0`.
"""
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_QUI, os.path.join(_QUI, "mattone"), _SOL, _CSV, os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
from solitone import toro as TO  # noqa: E402

SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def main():
    import _presidio
    import _u1_prototipo as U1
    import composizione as CM
    import specchio_carta as SPC
    import tick as TK
    from solitone import _u1_oggi as UO
    from solitone import tick_lapse as TL
    _presidio.avvia(os.path.join(_SOL, "mattone.py"))
    _presidio.avvia(os.path.join(_QUI, "mattone", "specchio_carta.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("CP E CPT, PEZZO PER PEZZO (dopo simmetria_CP.txt); sys.executable %s" % sys.executable)
    print("=" * 130)
    ids = [x[0] for x in CM.ORDINE[:7]]
    assert len(set(ids)) == 7
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        mot, st, par = Z["mot"], Z["st"], Z["par"]
        nodo = np.asarray(mot.inc.nodo)
        ii, jj = nodo[0::2], nodo[1::2]
        with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
            X0 = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
            t0 = int(json.loads(str(d["meta"]))["t"])
        rho = np.sum(np.abs(X0["psi_h"][Z["righe"]].reshape(n, -1)) ** 2, axis=1)
        cb = TO.centro(rho, m1, m2, L)[:2]
        p0 = (int(round(cb[0])) % L, int(round(cb[1])) % L)
        C0 = MT.Campi(Z, "MGU", rho_c, e)
        ci, cj = np.asarray(C0.campo.ii), np.asarray(C0.campo.jj)
        A1v, A2v = TO.vettori()
        d30 = 2 * A1v + A2v
        ang = math.atan2(d30[1], d30[0])
        c2, s2 = math.cos(2 * ang), math.sin(2 * ang)
        lv = np.array([math.cos(ang), math.sin(ang)])
        geo = {"id": (v.copy(), np.arange(2 * len(ii)), np.arange(len(ci)), np.zeros(len(ci), bool))}
        for nome, M in (("inv", -np.eye(2)), ("spec", np.array([[c2, s2], [s2, -c2]]))):
            P = np.outer(m1 - p0[0], A1v) + np.outer(m2 - p0[1], A2v)
            qi = np.rint((P @ M.T) @ np.linalg.inv(np.column_stack([A1v, A2v])).T)
            sig = ((qi[:, 0].astype(int) + p0[0]) % L) * L + (qi[:, 1].astype(int) + p0[1]) % L
            ap, rov = SPC.mappa_archi(ii, jj, sig)
            hp = np.empty(2 * len(ap), dtype=int)
            hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
            hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
            assert np.array_equal(nodo[hp], sig[nodo])
            cap, crov = SPC.mappa_archi(ci, cj, sig)
            geo[nome] = (sig, hp, cap, crov)

        def theta(X, A, E, mp, T, f, sA, sE, cj_=True):
            sig, hp, cap, crov = geo[mp]
            Y = {}
            for k, a in X.items():
                b = np.conj(a) if (cj_ and np.iscomplexobj(a)) else a
                if k in ("psi_h", "psi"):
                    b = b @ T.T
                elif k == "phi_h":
                    b = f(a)
                y = np.empty_like(b)
                if a.shape[0] == n:
                    y[sig] = b
                else:
                    y[hp] = b
                Y[k] = y
            sg = np.where(crov, -1.0, 1.0)
            Ar, Er = np.empty_like(A), np.empty_like(E)
            Ar[cap] = sA * sg * A
            Er[cap] = sE * sg * E
            return Y, Ar, Er

        def prepara(X, A, E):
            Z["metti"]({k: v_.copy() for k, v_ in X.items()})
            Cx = MT.Campi(Z, "MGU", rho_c, e)
            Cx.campo.A[...] = A
            Cx.campo.E[...] = E
            Cx.campo.e = e
            Cx.e_prec = e
            U1.scrivi_U(mot, Cx.campo)
            return Cx

        Cx = prepara(X0, A0, E0)
        cs_x = np.array(TL.cs_al_centro(mot, st, par, Z["s"], Cx.legge, False, omega=1.0, giri_max=None, storia=None)[0], copy=True)

        def cs_di(mp):
            """### `cs` dello stato di partenza PERMUTATO dalla mappa del candidato (v2: nella v1 lo stesso `cs_x` sui due lati, errore mio)."""
            y = np.empty_like(cs_x)
            y[geo[mp][0]] = cs_x
            return y

        def applica(nome, X, A, E, cs):
            Cx = prepara(X, A, E)
            if nome == "spinta":
                Cx.campo.spinta(0.5)
            elif nome == "fase_a":
                TL.fase_a(mot, st, Cx.legge, Cx.e0, False)
            elif nome == "reazione":
                TL.reazione(mot, st, par, Z["s"], Cx.legge, 0.5)
            elif nome == "tick":
                Cx.tick(1, t0 + 1, 1.0, e)
            else:
                mot.cs = cs.copy()
                mot.lambda_c = None
                with UO.avvolto(mot, Cx.campo, True):
                    TK.percorri_tick(st, mot, par, tuple(i for i in ids if i != nome), None, 7)
            return {k: st[k].copy() for k in X}, Cx.campo.A.copy(), Cx.campo.E.copy()

        def diff(Pp, Q):
            out = {}
            for k in ("psi_h", "phi_h"):
                out[k] = float(np.max(np.abs(Pp[0][k] - Q[0][k]))) / max(float(np.max(np.abs(Q[0][k]))), 1e-300)
            out["A"] = float(np.max(np.abs(Pp[1] - Q[1]))) / max(float(np.max(np.abs(Q[1]))), 1e-300)
            out["E"] = float(np.max(np.abs(Pp[2] - Q[2]))) / max(float(np.max(np.abs(Q[2]))), 1e-300)
            out["max"] = max(out.values())
            return out

        mcj = lambda p: -np.conj(p)  # noqa: E731
        CAND = (("CPT", ("inv", SY, mcj, -1.0, +1.0), "inv sy -conj(phi) sA-1 sE+1"),
                ("CPT", ("inv", SY, mcj, -1.0, -1.0), "inv sy -conj(phi) sA-1 sE-1"),
                ("CP", ("spec", (lv[0] * SX + lv[1] * SY) @ SY, lambda p: p, +1.0, +1.0), "spec s.l.sy phi sA+1 sE+1"))
        pezzi = ["spinta", "fase_a", "reazione"] + ids + ["tick"]
        ok_ctrl = True
        for nome in pezzi:
            t1 = time.time()
            Px = applica(nome, X0, A0, E0, cs_x)
            ctrl = diff(applica(nome, *theta(X0, A0, E0, "id", I2, lambda p: p, 1.0, 1.0, cj_=False), cs_x), Px)["max"]
            ok_ctrl = ok_ctrl and ctrl == 0.0
            parti = []
            for fam, (mp, T, f, sA, sE), etich in CAND:
                if fam == "CP":
                    dd = diff(applica(nome, *theta(X0, A0, E0, mp, T, f, sA, sE), cs_di(mp)), theta(*Px, mp, T, f, sA, sE))
                else:
                    dd = diff(applica(nome, *theta(*Px, mp, T, f, sA, sE), cs_di(mp)), theta(X0, A0, E0, mp, T, f, sA, sE))
                parti.append("%s [%s] psi_h %.2e phi_h %.2e A %.2e E %.2e" % (fam, etich, dd["psi_h"], dd["phi_h"], dd["A"], dd["E"]))
            print("    %-24s il controllo %.1e (%.0f s)" % (nome, ctrl, time.time() - t1))
            for p_ in parti:
                print("        %s" % p_)
            sys.stdout.flush()
        Z["metti"]()
    print("-" * 130)
    print("  DEVE: il controllo positivo (l'identita') da' 0 per ogni pezzo: %s" % ("PASSA" if ok_ctrl else "### FALLISCE"))
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0 if ok_ctrl else 1


if __name__ == "__main__":
    sys.exit(main())
