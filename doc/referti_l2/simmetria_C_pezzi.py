# -*- coding: utf-8 -*-
r"""**LA SIMMETRIA C, PEZZO PER PEZZO: QUALE TERMINE ROMPE C, E DI QUANTO** *(il passo diagnostico della carta `doc/TASK_HISTORY/2026-11-17_mitosi_primo_passo.md`, sez. `2.3`, «se cade: quale termine rompe C»; DOPO `simmetria_C.txt`)*.

    E:\python\py3132\python.exe doc/referti_l2/simmetria_C_pezzi.py > doc/referti_l2/simmetria_C_pezzi.txt     (PYTHONNOUSERSITE=1, 1 filo, numba spento)

**I pezzi del tick di G+U** *(`csv/solitone/p6_bracci.py`, `tick_GU`)*: `campo.spinta(0.5)`; `tick_lapse.fase_a`; `tick_lapse.reazione(0.5)`; **i sette pezzi della prima meta' del palindromo** *(`composizione.ORDINE[:7]`, uno alla volta con `tick.percorri_tick(..., salta = gli altri, None, 7)`, dentro `_u1_oggi.avvolto`; `mot.cs` fissato a quello dello stato di partenza, **lo stesso per i due lati**; la differenza di `cs` fra `x` e `C(x)` si stampa a parte)*.
**Per ogni pezzo `P`:** `C(P(x))` contro `P(C(x))` per i `32` candidati di `simmetria_C.py`; **il migliore e il suo valore**, sul toro intero *(un pezzo solo non tocca il bordo)*.
**IL CONTROLLO POSITIVO** *(che mancava in `simmetria_C.py`)*: **l'identita' SENZA coniugio** *(`T = I`, `f = phi`, `s = +1`)* **deve dare `0` per ogni pezzo e per il tick intero** *(il determinismo della catena di confronto)*: **se non da' `0`, i numeri non si leggono.**
"""
import itertools
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_QUI, _SOL, _CSV, os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import simmetria_C as SC  # noqa: E402


def main():
    import _presidio
    import _u1_prototipo as U1
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    from solitone import tick_lapse as TL
    _presidio.avvia(os.path.join(_SOL, "mattone.py"))
    _presidio.avvia(os.path.join(_QUI, "simmetria_C.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("LA SIMMETRIA C, PEZZO PER PEZZO (dopo simmetria_C.txt); sys.executable %s; e %r" % (sys.executable, e))
    print("=" * 130)
    PRIMA = CM.ORDINE[:7]
    ids = [x[0] for x in PRIMA]
    assert len(set(ids)) == 7, "la prima meta' del palindromo non ha sette id distinti: FERMO"
    print("### i pezzi della prima meta' del palindromo: %s" % ids)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        mot, st, par = Z["mot"], Z["st"], Z["par"]
        with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
            X0 = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()
            t0 = int(json.loads(str(d["meta"]))["t"])

        def prepara(X, A, E):
            Z["metti"]({k: v_.copy() for k, v_ in X.items()})
            Cx = MT.Campi(Z, "MGU", rho_c, e)
            Cx.campo.A[...] = A
            Cx.campo.E[...] = E
            Cx.campo.e = e
            Cx.e_prec = e
            U1.scrivi_U(mot, Cx.campo)
            return Cx

        def esito(Cx, X):
            return {k: st[k].copy() for k in X}, Cx.campo.A.copy(), Cx.campo.E.copy()

        Cx = prepara(X0, A0, E0)
        cs_x, _g = TL.cs_al_centro(mot, st, par, Z["s"], Cx.legge, False, omega=1.0, giri_max=None, storia=None)
        cs_x = np.array(cs_x, copy=True)
        print("### cs dallo stato di partenza: forma %s, da %.6e a %.6e" % (cs_x.shape, float(np.min(cs_x)), float(np.max(cs_x))))

        def applica(nome, X, A, E):
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
                mot.cs = cs_x.copy()
                mot.lambda_c = None
                with UO.avvolto(mot, Cx.campo, True):
                    TK.percorri_tick(st, mot, par, tuple(i for i in ids if i != nome), None, 7)
            return esito(Cx, X)

        def diff(P, Q):
            out = {}
            for k in ("psi_h", "phi_h"):
                out[k] = float(np.max(np.abs(P[0][k] - Q[0][k]))) / max(float(np.max(np.abs(Q[0][k]))), 1e-300)
            out["A"] = float(np.max(np.abs(P[1] - Q[1]))) / max(float(np.max(np.abs(Q[1]))), 1e-300)
            out["E"] = float(np.max(np.abs(P[2] - Q[2]))) / max(float(np.max(np.abs(Q[2]))), 1e-300)
            out["max"] = max(out.values())
            return out

        # la differenza di cs fra x e C(x) per il candidato sigma_y, phi, s -1 (stampata a parte)
        Xc, Ac, Ec = SC.coniuga(X0, A0, E0, SC.SY, SC.FS[0][1], -1.0)
        Cc = prepara(Xc, Ac, Ec)
        cs_c, _g = TL.cs_al_centro(mot, st, par, Z["s"], Cc.legge, False, omega=1.0, giri_max=None, storia=None)
        print("### cs di C(x) (T sigma_y, f phi, s -1) contro cs di x: max |differenza| relativa %.3e" % (float(np.max(np.abs(np.asarray(cs_c) - cs_x))) / float(np.max(np.abs(cs_x)))))
        print("-" * 130)
        pezzi = ["spinta", "fase_a", "reazione"] + ids + ["tick"]
        controlli = []
        tabella = []
        for nome in pezzi:
            t1 = time.time()
            Px = applica(nome, X0, A0, E0)
            # il controllo positivo: l'identita' SENZA coniugio
            Pi = applica(nome, *SC.coniuga(X0, A0, E0, SC.TS[0][1], SC.FS[0][1], 1.0, coniugio=False))
            ctrl = diff(Pi, SC.coniuga(Px[0], Px[1], Px[2], SC.TS[0][1], SC.FS[0][1], 1.0, coniugio=False))["max"]
            controlli.append((nome, ctrl))
            ris = []
            for (tn, T), (fn, f), s in itertools.product(SC.TS, SC.FS, SC.SS):
                R = SC.coniuga(Px[0], Px[1], Px[2], T, f, s)
                Q = applica(nome, *SC.coniuga(X0, A0, E0, T, f, s))
                dd = diff(Q, R)
                ris.append((dd["max"], tn, fn, s, dd))
            ris.sort(key=lambda x: x[0])
            m, tn, fn, s, dd = ris[0]
            tabella.append((nome, m, tn, fn, s, dd, ctrl))
            print("    %-24s il controllo (identita') %.1e | il migliore T %-8s f %-11s s %+.0f: psi_h %.3e  phi_h %.3e  A %.3e  E %.3e   (%.1f s)" % (
                nome, ctrl, tn, fn, s, dd["psi_h"], dd["phi_h"], dd["A"], dd["E"], time.time() - t1))
            sys.stdout.flush()
        Z["metti"]()
    print("-" * 130)
    ok = all(c == 0.0 for _n, c in controlli)
    print("  DEVE: il controllo positivo (l'identita' senza coniugio) da' 0 per ogni pezzo e per il tick: %s %s" % ("PASSA" if ok else "### FALLISCE", "" if ok else [x for x in controlli if x[1] != 0.0]))
    print("### I PEZZI CHE COMMUTANO CON C (il migliore sotto 1e-12):  %s" % [x[0] for x in tabella if x[1] < 1e-12])
    print("### I PEZZI CHE ROMPONO C (il migliore sopra 1e-12):        %s" % [(x[0], "%.2e" % x[1]) for x in tabella if x[1] >= 1e-12])
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
