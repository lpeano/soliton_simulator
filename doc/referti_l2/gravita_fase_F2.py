# -*- coding: utf-8 -*-
r"""**[M1446-F2] CHI FA B? U SPENTO, phi CONGELATO, TUTTI E DUE, A d 39 IN FASE E IN ANTIFASE** *(l'aggiunta di Luca a [M1446]; la carta `doc/CARTA_E_mc2.md`, sez. `F2`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/gravita_fase_F2.py corsa --var U0 --gradi 0 --fino 3000      (var: U0, PHI, U0PHI; gradi: 0, 180)
    E:\python\py3132\python.exe doc/referti_l2/gravita_fase_F2.py lettura > doc/referti_l2/fase_relativa_F2.txt

**La scena:** `gravita_fase.prepara` *(d 39, le fasi `0, delta`)*, `kappa = 0` *(`gravita_due_corpi.parametri(Z, C, False)`)*. **Il tick:** `chi_tick_v2.tick_chi_v2` riga per riga con due interruttori: **U0** = niente `campo.spinta` e niente `UO.avvolto` *(`mot.geo.U = U0 = I` a ogni tick)*; **PHI** = dopo ogni tick `phi_h = c(t0 + k) phi_v` *(il vuoto fresco della corsa allo stesso tick, `mattone.vuoto_fresco`: la sola parte di phi)*. **Gli stati** ogni `250` in `CHI/due_corpi/F2_<var>_D<gradi>`. **La lettura:** `a` da `D(k)` dei baricentri con le righe di `gravita_fase.lettura`; `A = (a0 - a180)/2`, `B = (a0 + a180)/2` *(gli errori in quadratura)*, per ogni interruttore e per il riferimento *(`F-off`, `D180-off`)*; le letture della carta F2.
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
import chi_tick as CT  # noqa: E402
import gravita_due_corpi as GD  # noqa: E402
import gravita_due_corpi_d as GDD  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402
import gravita_fase as GF  # noqa: E402

VAR = {"U0": (False, True), "PHI": (True, False), "U0PHI": (False, False)}      # ### (U acceso, phi libero)
GRADI = (0, 180)


def tick_F2(z, campo, P, Lp, X, u_acceso, phi_libero, phi_vuoto, U0):
    """### `chi_tick_v2.tick_chi_v2` riga per riga, coi due interruttori."""
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    mot, st, par = z["mot"], z["st"], z["par"]
    dt = float(mot.dtau[0])
    assert np.all(mot.dtau == mot.dtau[0]), "dtau non uniforme: il salto di rana di chi vuole un dtau solo"
    if u_acceso:
        campo.spinta(0.5)
    else:
        mot.geo.U[...] = U0
    X["pi"] += (0.5 * dt * P.f) * CT.forza(mot, st, par, P, Lp, X["chi"])
    X["chi"] += (0.5 * dt) * X["pi"]
    N = np.exp(-P.kappa * X["chi"])
    mot.cs = P.s * N
    mot.lambda_c = None
    CT.fase_a(mot, st, P.e0, N)
    if u_acceso:
        with UO.avvolto(mot, campo, True):
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    else:
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    CT.fase_a(mot, st, P.e0, N)
    d = np.asarray(mot.dtau, dtype=float) * np.asarray(mot.cs, dtype=float)
    nodo = np.asarray(mot.inc.nodo)
    X["theta_a"] += math.pi * (d[nodo[0::2]] - d[nodo[1::2]])
    X["chi"] += (0.5 * dt) * X["pi"]
    X["pi"] += (0.5 * dt * P.f) * CT.forza(mot, st, par, P, Lp, X["chi"])
    if u_acceso:
        campo.spinta(0.5)
    if not phi_libero:
        st["phi_h"][...] = phi_vuoto


def corsa(var, gradi, k_fino):
    import _presidio
    from solitone import bordo as BO
    for m in ("gravita_fase.py", "chi_tick_v2.py", "chi_tick.py", "gravita_due_corpi.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    GDD.avvia()
    MT = TC.moduli()[0]
    t0 = MT.G2.T0
    u_acceso, phi_libero = VAR[var]
    nome = "F2_%s_D%d" % (var, gradi)
    d_out = os.path.join(GD.BASE, nome)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        Lp = CT.Laplaciano(mot)
        C, info = GF.prepara(Z, gradi)
        P, Pon, m0 = GD.parametri(Z, C, False)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        U0 = Z["U0"].copy()
        meta = dict(info, corsa=nome, var=var, u_acceso=u_acceso, phi_libero=phi_libero, parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "e0": P.e0, "s": P.s, "f": P.f})
        print("### %s: U %s, phi %s; i vertici %s, la distanza %.4f, le fasi %s; kappa %r; |U0 - I| %.1e; l'impronta %s" % (
            nome, "acceso" if u_acceso else "SPENTO", "libero" if phi_libero else "CONGELATO al vuoto puro", info["centri"], info["distanza"], info["fasi_gradi"], P.kappa,
            float(np.max(np.abs(U0 - np.eye(2)[None]))), GD.impronta(Z, C, X)))

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")
        salva(0)
        t1 = time.time()
        for k in range(1, k_fino + 1):
            pv = BO.c_di(t0 + k, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
            tick_F2(Z["z"], C.campo, P, Lp, X, u_acceso, phi_libero, pv, U0)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % GD.OGNI_STATO == 0 or k == k_fino:
                salva(k)
                print("    [stato] k %d (%.0f s)" % (k, time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    return 0


def lettura():
    import _presidio
    from solitone import toro as TO
    for m in ("gravita_fase.py", "gravita_due_corpi_d.py", "gravita_due_corpi_misure.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    KS = tuple(range(0, 3001, 250))
    print("=" * 130)
    print("[M1446-F2] CHI FA B? (la carta sez. F2): a da D(k); A = (a0 - a180)/2, B = (a0 + a180)/2")
    print("=" * 130)
    gruppi = [("riferimento (F, nessun interruttore)", "F-off", "D180-off")] + [("%s (%s)" % (v, {"U0": "U spento", "PHI": "phi congelato", "U0PHI": "tutti e due"}[v]), "F2_%s_D0" % v, "F2_%s_D180" % v) for v in VAR]
    out = {}
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        A1 = np.asarray(TO.vettori()[0], float)[:2]

        def a_di(nome):
            fs = [os.path.join(GD.BASE, nome, "stato_%06d.npz" % k) for k in KS]
            if not all(os.path.exists(f + ".sha1") for f in fs):
                return None
            X0, meta0 = GM.leggi(fs[0])
            V = np.asarray(meta0["centri"], float)
            M = 0.5 * (V[0] + V[1])
            dxy = TO.scarti(Z["m1"], Z["m2"], M[0], M[1], L)[:, :2]
            lato = dxy @ (A1 / np.hypot(*A1))
            Db = []
            for f in fs:
                X, _m = GM.leggi(f)
                rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
                b = [(dxy[s] * rho[s][:, None]).sum(axis=0) / rho[s].sum() for s in (lato < 0.0, lato >= 0.0)]
                Db.append(float(np.hypot(*(b[1] - b[0]))))
            fb = GM.fit(KS, np.array(Db))
            print("    %-14s le fasi %s: D da %.4f a %.4f; a %+.4e +- %.1e (il residuo %.2e)" % (nome, meta0.get("fasi_gradi"), Db[0], Db[-1], fb[2], fb[3], fb[4]))
            return fb[2], fb[3]
        for titolo, n0, n180 in gruppi:
            print("  %s" % titolo)
            r0, r180 = a_di(n0), a_di(n180)
            if r0 is None or r180 is None:
                print("    ### gli stati non ci sono tutti: saltato")
                continue
            A = 0.5 * (r0[0] - r180[0])
            B = 0.5 * (r0[0] + r180[0])
            sg = 0.5 * math.hypot(r0[1], r180[1])
            out[titolo.split()[0]] = (A, B, sg)
            print("    A %+.4e, B %+.4e, sigma %.1e (B/sigma %+.1f)" % (A, B, sg, B / sg))
        Z["metti"]()
    print("-" * 130)
    if all(k in out for k in ("riferimento", "U0", "PHI")):
        _A, Br, sr = out["riferimento"]
        _A, Bu, su = out["U0"]
        _A, Bp, sp = out["PHI"]
        da_G = abs(Bp) < 2 * sp and abs(Bu - Br) < 2 * math.hypot(su, sr)
        da_U = abs(Bu) < 2 * su and abs(Bp - Br) < 2 * math.hypot(sp, sr)
        print("  le letture della carta F2: B da G col vuoto %s; B da U %s; %s" % (
            "SI'" if da_G else "no", "SI'" if da_U else "no", "" if (da_G or da_U) else "### ne' l'una ne' l'altra: tutti e due o nessuno (i numeri sopra)"))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("corsa")
    c.add_argument("--var", choices=sorted(VAR), required=True)
    c.add_argument("--gradi", type=int, choices=GRADI, required=True)
    c.add_argument("--fino", type=int, required=True)
    sub.add_parser("lettura")
    x = ap.parse_args(argv)
    return corsa(x.var, x.gradi, x.fino) if x.cmd == "corsa" else lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
