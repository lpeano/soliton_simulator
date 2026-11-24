# -*- coding: utf-8 -*-
r"""**[M0417-M] LE MISURE DEI DUE MATTONI E IL FILM LEGGERO** *(il mandato di Luca `2026-11-22` `04:17`; la carta `doc/TASK_HISTORY/2026-11-22_gravita_due_corpi.md`, sez. `2`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/gravita_due_corpi_misure.py > doc/referti_l2/gravita_due_corpi.txt

**Per ognuna delle quattro corse** *(`CHI/due_corpi/<F-on>`, gli stati `0, 250, ..., 3000`, lo sha1 controllato)*: (a) `D(k)` dai baricentri di `rho` delle due meta' e dai nodi di `rho` massimo lisciato sui `7` nodi; (b) il fit `D0 + v k + a k^2 / 2` con l'errore standard di `a`, poi `Da_F` e `Da_S`; (c) lungo la congiungente e nel vuoto lontano `chi`, `N`, la sorgente netta a `k 0, 1500, 3000`; (d) le pale. **Il film:** `rho`, `chi`, `Jx`, `Jy` per nodo di ogni stato in `doc/referti_l2/film/gravita_<corsa>.npz` *(il flusso con lo strumento del 15/11, come F1)*.
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
import triangolo_chi_v4 as TC  # noqa: E402
import chi_tick as CT  # noqa: E402
import gravita_due_corpi as GD  # noqa: E402

CORSE = ("F-on", "F-off", "S-on", "S-off")
KS = tuple(range(0, 3001, 250))
FILM = os.path.join(_QUI, "film")


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def leggi(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    z = np.load(f)
    X = {x: z[x] for x in z.files}
    return X, json.loads(str(X.pop("meta")))


def pala(d, rho):
    r = np.hypot(d[:, 0], d[:, 1])
    s = r <= 18.0
    w = rho[s]
    T = (d[s][:, :, None] * d[s][:, None, :] * w[:, None, None]).sum(axis=0)
    lam = np.linalg.eigvalsh(T)
    return math.sqrt(float(np.sum(w * r[s] ** 2) / np.sum(w))), float((lam[1] - lam[0]) / (lam[1] + lam[0]))


def fit(k, D):
    k = np.asarray(k, float)
    X = np.stack([np.ones_like(k), k, 0.5 * k * k], axis=1)
    b, res, _r, _s = np.linalg.lstsq(X, D, rcond=None)
    r = D - X @ b
    s2 = float(r @ r) / (len(k) - 3)
    cov = s2 * np.linalg.inv(X.T @ X)
    return float(b[0]), float(b[1]), float(b[2]), math.sqrt(float(cov[2, 2])), math.sqrt(s2)


def main():
    import _presidio
    import _u1_prototipo as U1
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "gravita_due_corpi.py"))
    _presidio.avvia(__file__)
    MT = TC.moduli()[0]
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    print("=" * 130)
    print("[M0417-M] I DUE MATTONI, CHI ACCESO CONTRO CHI SPENTO (la carta sez. 2): le quattro corse, gli stati 0 ... 3000 ogni 250")
    print("=" * 130)
    RIS = {}
    with TC.scena() as Z:
        mot = Z["mot"]
        n, L = mot.inc.n, Z["L"]
        nodo = np.asarray(mot.inc.nodo, dtype=np.int64)
        assert list(nodo[0::2][:6]) == [0, 0, 0, 1, 1, 1], "gli archi non sono 3 v + a"
        A1, A2 = TO.vettori()
        A1, A2 = np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]
        vett = np.stack([A1, A2, A1 + A2])
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        sp = mot.operatori["spostamento_trasporto"]
        cs0 = mot.cs
        for nome in CORSE:
            d = os.path.join(GD.BASE, nome)
            fs = [os.path.join(d, "stato_%06d.npz" % k) for k in KS]
            if not all(os.path.exists(f + ".sha1") for f in fs):
                print("### %s: gli stati non ci sono tutti (la corsa non e' finita): saltata" % nome)
                continue
            print("-" * 130)
            X0, meta0 = leggi(fs[0])
            V = np.asarray(meta0["centri"], float)
            M = 0.5 * (V[0] + V[1])
            pm = meta0["parametri"]
            dxy = TO.scarti(m1, m2, M[0], M[1], L)[:, :2]
            u = float(GD.DIST[0]) * A1 + float(GD.DIST[1]) * A2
            u = u / np.hypot(*u)
            lato = dxy @ u
            meta_s = [lato < 0.0, lato >= 0.0]
            print("### %s: i vertici %s, il punto medio %s; kappa %r, c0 %r (kappa di on %r)" % (nome, V.astype(int).tolist(), M.tolist(), pm["kappa"], pm["c0"], pm["kappa_on"]))
            Db, Dm, righe, F = [], [], [], {}
            for k, f in zip(KS, fs):
                X, meta = leggi(f)
                rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
                bari = [(dxy[s] * rho[s][:, None]).sum(axis=0) / rho[s].sum() for s in meta_s]
                g = rho.reshape(L, L)
                lis = (g + sum(np.roll(np.roll(g, a, 0), b, 1) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)))) / 7.0
                lis = lis.reshape(-1)
                mass = [dxy[np.nonzero(s)[0][int(np.argmax(lis[s]))]] for s in meta_s]
                Db.append(float(np.hypot(*(bari[1] - bari[0]))))
                Dm.append(float(np.hypot(*(mass[1] - mass[0]))))
                pale = [pala(dxy - b, rho) for b in bari]
                righe.append((k, Db[-1], Dm[-1], pale))
                # ### il flusso (lo strumento del 15/11, col cs e la fase di chi)
                Z["metti"]({x: X[x] for x in Z["chiavi"]})
                cam.A[...] = X["campo_A"]
                N = np.exp(-float(pm["kappa"]) * X["chi"])
                mot.cs = float(pm["s"]) * N
                mot.lambda_c = None
                CT.fase_a(mot, Z["st"], float(pm["e0"]), N)
                U1.scrivi_U(mot, cam)
                mm = cam.m
                prima = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
                sp(Z["st"], Z["par"], 0.5)
                J = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
                Z["metti"]()
                Jn = (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)
                if k in (0, 1500, 3000):
                    Z["metti"]({x: X[x] for x in Z["chiavi"]})
                    Q = CT.Q_di(mot, Z["st"], Z["par"], float(pm["s"]) * N)
                    rr = CT.rho_di(mot, Z["st"])
                    Z["metti"]()
                    sorg = float(pm["kappa"]) * N * (float(pm["s"]) * Q - float(pm["e0"]) * rr) - float(pm["c0"])
                    pts = [bari[0] + t * (bari[1] - bari[0]) for t in np.linspace(0.0, 1.0, 41)]
                    nn = [int(np.argmin(np.hypot(*(dxy - p).T))) for p in pts]
                    lont = (np.hypot(*(dxy - bari[0]).T) >= 50.0) & (np.hypot(*(dxy - bari[1]).T) >= 50.0)
                    ch = X["chi"]
                    print("    (c) k %d lungo la congiungente (41 punti): chi ai capi %.6f e %.6f, a meta' %.6f; N a meta' %.8f; la sorgente netta ai capi %+.4e e %+.4e, a meta' %+.4e, il min %+.4e, il max %+.4e; nel vuoto lontano (la mediana) chi %.6f, N %.8f, la sorgente %+.4e" % (
                        k, ch[nn[0]], ch[nn[-1]], ch[nn[20]], N[nn[20]], sorg[nn[0]], sorg[nn[-1]], sorg[nn[20]], float(sorg[nn].min()), float(sorg[nn].max()),
                        float(np.median(ch[lont])), float(np.median(N[lont])), float(np.median(sorg[lont]))))
                sfx = "_%06d" % k
                F["rho" + sfx], F["chi" + sfx] = rho.astype(np.float32), X["chi"].astype(np.float32)
                F["Jx" + sfx], F["Jy" + sfx] = Jn[:, 0].astype(np.float32), Jn[:, 1].astype(np.float32)
            mot.cs = cs0
            mot.lambda_c = None
            for k, db, dm, pale in righe:
                print("    k %4d  D (baricentri) %.4f  D (rho massimo lisciato) %.4f  (d) le pale: rqm %.4f, %.4f; a %.4f, %.4f" % (k, db, dm, pale[0][0], pale[1][0], pale[0][1], pale[1][1]))
            fb, fm = fit(KS, np.array(Db)), fit(KS, np.array(Dm))
            print("    (b) il fit sui baricentri: D0 %.4f, v %+.4e, a %+.4e +- %.2e (il residuo rms %.3e); sul rho massimo: a %+.4e +- %.2e (il residuo rms %.3e)" % (fb[0], fb[1], fb[2], fb[3], fb[4], fm[2], fm[3], fm[4]))
            RIS[nome] = (fb, fm)
            F.update(k=np.array(KS, dtype=np.int32), L=np.array(L), m1=m1.astype(np.float32), m2=m2.astype(np.float32), vertici=V.astype(np.int32), corsa=np.array(nome))
            ff = os.path.join(FILM, "gravita_%s.npz" % nome)
            np.savez_compressed(ff, **F)
            print("    il film %s: %.2f MB (sha1 %s)" % (os.path.relpath(ff, _QUI), os.path.getsize(ff) / 1e6, sha1(ff)[:8]))
            assert os.path.getsize(ff) <= 50e6, "sopra i 50 MB: FERMO"
        Z["metti"]()
    print("=" * 130)
    print("(b) IL CONFRONTO: Da = a(on) - a(off), l'incertezza in quadratura; Da < 0: chi ATTIRA (fuori dall'incertezza se |Da| > 2 sigma)")
    print("=" * 130)
    for sc in ("F", "S"):
        if "%s-on" % sc in RIS and "%s-off" % sc in RIS:
            for i, nome in ((0, "i baricentri"), (1, "il rho massimo")):
                on, off = RIS["%s-on" % sc][i], RIS["%s-off" % sc][i]
                da, sg = on[2] - off[2], math.hypot(on[3], off[3])
                print("  %s, %-15s a(on) %+.4e +- %.2e; a(off) %+.4e +- %.2e; Da %+.4e +- %.2e: %s" % (
                    sc, nome, on[2], on[3], off[2], off[3], da, sg, ("ATTIRA" if da < 0 else "SPINGE") + (" (fuori dall'incertezza)" if abs(da) > 2.0 * sg else " (DENTRO l'incertezza)")))
        else:
            print("  %s: manca una delle due corse" % sc)
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
