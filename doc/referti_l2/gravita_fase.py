# -*- coding: utf-8 -*-
r"""**[M1446-F] G+U CONTRO LA FASE RELATIVA delta: LA FORMA cos(delta) REGGE?** *(l'aggiunta v2 di Luca a [M1446], corsia F; la carta `doc/CARTA_E_mc2.md`, sez. `2.2`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/gravita_fase.py corsa --gradi 90 --fino 3000      (delta in gradi: 90, 60, 180, 270; d 39; kappa 0)
    E:\python\py3132\python.exe doc/referti_l2/gravita_fase.py lettura > doc/referti_l2/fase_relativa.txt

**La corsa:** le righe di `gravita_due_corpi_d.prepara_coppia` *(la scena di [M0417], d 39)* con le fasi `0` e `delta` al posto di `gravita_due_corpi.FASI`; `chi` coi parametri di oggi e **`kappa = 0`** *(«off»: G+U senza `chi`, lo stesso `c0`)*; il tick `chi_tick_v2.tick_chi_v2`; gli stati ogni `250` in `CHI/due_corpi/D<gradi>-off`. **La lettura:** `D(k)` dai baricentri *(le righe di `gravita_due_corpi_misure`)*, il fit, `a`; **con F-off (`delta = 0`) e S-off (`delta = 120`)**; il fit `a = A cos(delta) + B` su tutti i punti; lo scarto massimo diviso `|A|`.
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
import chi_tick_v2 as CV2  # noqa: E402
import gravita_due_corpi as GD  # noqa: E402
import gravita_due_corpi_d as GDD  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402

D = 39
GRADI = (90, 60, 180, 270)              # ### la carta: pi/2, pi/3, pi, 3 pi/2


def prepara(Z, gradi):
    """### `gravita_due_corpi_d.prepara_coppia` riga per riga con le fasi `0, delta`."""
    MT, MTR, T1, TRU, TV, PO = TC.moduli()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    st, L = Z["st"], Z["L"]
    fr = TV.francobollo_L162(0)
    centri, tgt = GDD.vertici(fr, L, D)
    Z["g_e"] = np.zeros_like(Z["g_e"])
    MT.vuoto_fresco(Z, t0)
    phi_F3 = st["phi_h"].copy()
    vuoto = {x: st[x].copy() for x in Z["chiavi"]}
    fasi = (0.0, math.radians(gradi))
    soli = []
    for j, c in enumerate(centri):
        for x in Z["chiavi"]:
            st[x][...] = vuoto[x]
        MT.incolla(Z, fr, c, True)
        if fasi[j] != 0.0:
            st["psi_h"][...] = st["psi_h"] * np.exp(1j * fasi[j])
        soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
    st["psi_h"][...] = soli[0][0] + soli[1][0]
    st["phi_h"][...] = soli[0][1] * (soli[1][1] / phi_F3)
    C = PO.campi(Z, rho_c, e)
    return C, {"scena": "D%d" % gradi, "d": D, "centri": centri, "bersaglio": list(tgt), "distanza": MT.distanza(L, centri[0], centri[1]), "fasi_gradi": [0.0, float(gradi)]}


def corsa(gradi, k_fino):
    GDD.avvia()
    MT = TC.moduli()[0]
    nome = "D%d-off" % gradi
    d_out = os.path.join(GD.BASE, nome)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        Lp = CT.Laplaciano(mot)
        C, info = prepara(Z, gradi)
        P, Pon, m0 = GD.parametri(Z, C, False)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        meta = dict(info, corsa=nome, parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": P.f, "kappa_on": Pon.kappa})
        print("### %s: i vertici %s, la distanza %.4f, le fasi %s; kappa %r, c0 %r; m0 %+.12e; l'impronta %s" % (nome, info["centri"], info["distanza"], info["fasi_gradi"], P.kappa, P.c0, m0, GD.impronta(Z, C, X)))

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")
        salva(0)
        t1 = time.time()
        for k in range(1, k_fino + 1):
            CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)
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
    for m in ("gravita_due_corpi_d.py", "gravita_due_corpi_misure.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    KS = tuple(range(0, 3001, 250))
    print("=" * 130)
    print("[M1446-F] G+U (kappa = 0) CONTRO LA FASE RELATIVA delta, d 39 (la carta sez. 2.2): a da D(k) dei baricentri; il fit A cos(delta) + B")
    print("=" * 130)
    corse = [("F-off", 0.0), ("S-off", 120.0)] + [("D%d-off" % g, float(g)) for g in GRADI]
    punti = []
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        A1 = np.asarray(TO.vettori()[0], float)[:2]
        for nome, g in corse:
            fs = [os.path.join(GD.BASE, nome, "stato_%06d.npz" % k) for k in KS]
            if not all(os.path.exists(f + ".sha1") for f in fs):
                print("  %s: gli stati non ci sono tutti: saltata" % nome)
                continue
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
            punti.append((g, fb[2], fb[3]))
            print("  %-8s delta %5.1f gradi (le fasi del meta %s): D da %.4f a %.4f; a %+.4e +- %.1e (il residuo %.2e)" % (nome, g, meta0.get("fasi_gradi"), Db[0], Db[-1], fb[2], fb[3], fb[4]))
        Z["metti"]()
    if len(punti) >= 3:
        d = np.radians([p[0] for p in punti])
        y = np.array([p[1] for p in punti])
        w = 1.0 / np.array([p[2] for p in punti]) ** 2
        Am = np.stack([np.cos(d), np.ones_like(d)], axis=1)
        W = np.diag(w)
        cov = np.linalg.inv(Am.T @ W @ Am)
        b = cov @ Am.T @ W @ y
        res = y - Am @ b
        print("-" * 130)
        print("  il fit pesato a = A cos(delta) + B: A %+.4e +- %.1e, B %+.4e +- %.1e; lo scarto massimo %.3e = %.3f |A|: %s" % (
            b[0], math.sqrt(cov[0, 0]), b[1], math.sqrt(cov[1, 1]), float(np.abs(res).max()), float(np.abs(res).max() / abs(b[0])), "cos(delta) REGGE entro il 20%" if np.abs(res).max() <= 0.2 * abs(b[0]) else "cos(delta) NON regge entro il 20%"))
        for (g, a, sa), r in zip(punti, res):
            print("    delta %5.1f: a %+.4e, il fit %+.4e, lo scarto %+.3e (%.1f sigma)" % (g, a, a - r, r, abs(r) / sa))
    else:
        print("  meno di 3 punti: il fit non si fa")
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("corsa")
    c.add_argument("--gradi", type=int, choices=GRADI, required=True)
    c.add_argument("--fino", type=int, required=True)
    sub.add_parser("lettura")
    x = ap.parse_args(argv)
    return corsa(x.gradi, x.fino) if x.cmd == "corsa" else lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
