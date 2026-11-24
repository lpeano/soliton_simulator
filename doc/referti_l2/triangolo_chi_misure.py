# -*- coding: utf-8 -*-
r"""**T4: LE MISURE IN CORSA DEI TRONCHI DEL TRIANGOLO CON `chi`** *([M2357-T4]; la carta `doc/TASK_HISTORY/2026-11-21_triangolo_chi.md`, sez. `2` e `5`; SOLA LETTURA degli stati salvati)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi_misure.py giro --k 3000 > doc/referti_l2/triangolo_chi_misure.txt

**Il caso noto** *(DEVE, prima)*: sul mattone con `chi` *(la corsa della fisica vecchia, `CHI/mattone/stato_03000`)* i `20` archi con `|Theta|` piu' alto stanno nel guscio `17 <= r <= 20`; **DEVE FALLIRE** *(aggiunta mia, sez. `5`)*: `20` archi a caso *(il seme `11`)* no. **Per ogni tronco** *(t120, t120r28)* allo stato `k`: **(a)** i `20` archi con `|Theta|` piu' alto, classificati *(centrale, corridoio, guscio esterno, altrove)*, con l'angolo dal baricentro del triangolo e la distanza dall'asse del reticolo; il ritmo `|d Theta / dt|` fra `k - 250` e `k`; **(b)** la proiezione del primo scatto con `D = 250` e `D = 2500`, l'incertezza la differenza; **(c)** la circolazione: `B` medio sul disco di raggio `8` attorno alla media dei tre centri della materia e il flusso entro `30` *(`triangoli_magnetico`)*, l'orientamento a tre punte di `rho` entro `32` attorno al baricentro del triangolo, srotolato *(`girandola`)*, su tutti gli stati salvati fino a `k`.
"""
import argparse
import hashlib
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

CHI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI")
TRONCHI = ("t120", "t120r28")
QUANTO = 2.0 * math.pi
R_DISCO, R_FLUSSO, R_RHO = 8.0, 30.0, 32.0
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  %-112s %s   %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def leggi(f):
    h = hashlib.sha1(open(f, "rb").read()).hexdigest()
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == h, "lo sha1 di %s NON coincide" % f
    d = np.load(f)
    X = {x: d[x] for x in d.files}
    return X, json.loads(str(X.pop("meta"))), h


def punti_medi(Z):
    """### il punto medio di ogni arco nelle coordinate di reticolo `(m1, m2)` *(reali, l'immagine minima)*."""
    L = Z["L"]
    nodo = np.asarray(Z["mot"].inc.nodo)
    i, j = nodo[0::2], nodo[1::2]
    m1, m2 = (np.arange(Z["mot"].inc.n) // L).astype(float), (np.arange(Z["mot"].inc.n) % L).astype(float)
    d1 = ((m1[j] - m1[i] + 0.5 * L) % L) - 0.5 * L
    d2 = ((m2[j] - m2[i] + 0.5 * L) % L) - 0.5 * L
    return (m1[i] + 0.5 * d1) % L, (m2[i] + 0.5 * d2) % L, m1, m2


def dal_asse(gradi):
    return np.min(np.abs(((np.asarray(gradi)[:, None] - 60.0 * np.arange(6)[None, :]) + 180.0) % 360.0 - 180.0), axis=1)


def caso_noto():
    import prova_scatola5 as PS
    import chi_tick as CT
    from solitone import toro as TO
    CV = PS.CV
    print("=" * 130)
    print("IL CASO NOTO DI (a): il mattone con chi (la fisica vecchia) a k 3000: i 20 archi con |Theta| piu' alto nel guscio 17 <= r <= 20")
    print("=" * 130)
    f = os.path.join(CHI, "mattone", "stato_03000.npz")
    X, meta, h = leggi(f)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        p1, p2, _m1, _m2 = punti_medi(Z)
        c = meta["centro"]
        r = np.hypot(*TO.scarti(p1, p2, c[0], c[1], Z["L"]).T[:2])
        th = np.abs(X["theta_a"])
        assert th.shape == r.shape, "theta_a %s contro gli archi %s" % (th.shape, r.shape)
        top = np.argsort(th)[::-1][:20]
        rng = np.random.default_rng(11)
        caso = rng.choice(len(th), 20, replace=False)
        Z["metti"]()
    dentro = (r[top] >= 17.0) & (r[top] <= 20.0)
    print("### %s (sha1 %s): k %d, il centro %s; max |Theta| %.6f; i 20 piu' maturi a r %s" % (os.path.basename(f), h[:8], meta["k"], ["%.3f" % x for x in c], float(th.max()), ", ".join("%.2f" % x for x in r[top])))
    print("### 20 archi a caso (il seme 11): r %s" % ", ".join("%.1f" % x for x in r[caso]))
    esito("CASO NOTO: sul mattone a k 3000 i 20 archi piu' maturi nel guscio 17 <= r <= 20", bool(dentro.all()), "%d su 20" % int(dentro.sum()))
    esito("CASO NOTO DEVE FALLIRE (mio): 20 archi a caso NON tutti nel guscio", not bool(((r[caso] >= 17.0) & (r[caso] <= 20.0)).all()))


def srotola(gradi):
    out = [gradi[0]]
    for g in gradi[1:]:
        out.append(out[-1] + (g - out[-1] + 60.0) % 120.0 - 60.0)
    return out


def giro(k):
    import mattone as MT
    import chi_tick as CT
    from solitone import toro as TO
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        mot = Z["mot"]
        p1, p2, m1, m2 = punti_medi(Z)
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        q1 = np.concatenate([m1 + 2.0 / 3.0, m1 + 1.0 / 3.0])
        q2 = np.concatenate([m2 + 1.0 / 3.0, m2 + 2.0 / 3.0])
        for quale in TRONCHI:
            d = os.path.join(CHI, "triangolo", quale)
            print("=" * 130)
            print("IL TRONCO %s A k %d (sola lettura, %s)" % (quale, k, d))
            print("=" * 130)
            f = os.path.join(d, "stato_%06d.npz" % k)
            if not os.path.exists(f + ".sha1"):
                print("### lo stato %s NON c'e' ancora: il tronco %s non e' arrivato a k %d" % (os.path.basename(f), quale, k))
                continue
            X, meta, h = leggi(f)
            V = np.asarray(meta["centri"], dtype=float)
            lato = float(np.mean(meta["lati"]))
            G = (float(V[:, 0].mean()), float(V[:, 1].mean()))
            st = {x: X[x] for x in Z["chiavi"]}
            rho = np.zeros(n)
            np.add.at(rho, mot.inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            xyn = TO.scarti(m1, m2, G[0], G[1], L)[:, :2]
            angn = np.degrees(np.arctan2(xyn[:, 1], xyn[:, 0]))
            xyv = np.array([TO.scarti(np.array([v[0]]), np.array([v[1]]), G[0], G[1], L)[0, :2] for v in V])
            angv = np.degrees(np.arctan2(xyv[:, 1], xyv[:, 0]))
            centri = []
            for j in range(3):
                sett = np.abs(((angn - angv[j]) + 180.0) % 360.0 - 180.0) < 60.0
                w = rho[sett]
                centri.append((xyn[sett] * w[:, None]).sum(axis=0) / w.sum())
            centri = np.array(centri)
            xya = TO.scarti(p1, p2, G[0], G[1], L)[:, :2]
            th = np.abs(X["theta_a"])
            top = np.argsort(th)[::-1][:20]
            ins = lato / (2.0 * math.sqrt(3.0))

            def classe(p):
                if math.hypot(p[0], p[1]) <= ins:
                    return "centrale"
                for a, b in ((0, 1), (1, 2), (2, 0)):
                    u = centri[b] - centri[a]
                    t = float(np.dot(p - centri[a], u) / np.dot(u, u))
                    if 0.0 < t < 1.0 and float(np.hypot(*(p - centri[a] - t * u))) <= 6.0:
                        return "corridoio"
                if min(float(np.hypot(*(p - c))) for c in centri) <= 25.0:
                    return "guscio esterno"
                return "altrove"

            print("### %s (sha1 %s): il lato %.4f, l'inraggio %.4f; il baricentro del triangolo (m) %s; i centri della materia (dal baricentro, cartesiani) %s; max |Theta| %.6f" % (
                os.path.basename(f), h[:8], lato, ins, ["%.3f" % x for x in G], [["%.3f" % x for x in c] for c in centri], float(th.max())))
            cl = [classe(xya[a]) for a in top]
            an = np.degrees(np.arctan2(xya[top, 1], xya[top, 0]))
            da = dal_asse(an)
            print("    (a) i 20 archi con |Theta| piu' alto:")
            for q, a in enumerate(top):
                print("      %2d. l'arco %6d  |Theta| %.6f  r %.3f  l'angolo %+8.3f  dall'asse %.3f  %s" % (q + 1, a, th[a], float(np.hypot(*xya[a])), an[q], da[q], cl[q]))
            print("    (a) il conto: %s; la distanza dall'asse: la mediana %.3f, il massimo %.3f" % (", ".join("%s %d" % (c, cl.count(c)) for c in ("centrale", "corridoio", "guscio esterno", "altrove")), float(np.median(da)), float(da.max())))
            f1 = os.path.join(d, "stato_%06d.npz" % (k - 250))
            X1, _m, _h = leggi(f1)
            rit = np.abs(X["theta_a"] - X1["theta_a"]) / 250.0
            tr = np.argsort(rit)[::-1][:20]
            print("    (a) il ritmo |d Theta / dt| fra k %d e k %d: il massimo %.4e (l'arco %d, %s); i 20 piu' veloci: %s" % (
                k - 250, k, float(rit.max()), int(tr[0]), classe(xya[tr[0]]), ", ".join("%s %d" % (c, [classe(xya[a]) for a in tr].count(c)) for c in ("centrale", "corridoio", "guscio esterno", "altrove"))))
            pro = {}
            for D in (250, 2500):
                fD = os.path.join(d, "stato_%06d.npz" % (k - D))
                XD, _m, _h = leggi(fD)
                v = (th - np.abs(XD["theta_a"])) / float(D)
                ok = v > 0.0
                tk = np.full(len(th), np.inf)
                tk[ok] = k + (QUANTO - th[ok]) / v[ok]
                a = int(np.argmin(tk))
                pro[D] = (float(tk[a]), a)
                print("    (b) la proiezione con D = %d: il primo scatto a k %.0f (l'arco %d, %s, |Theta| %.6f, il ritmo %.4e)" % (D, tk[a], a, classe(xya[a]), th[a], v[a]))
            print("    (b) l'incertezza |k(250) - k(2500)| = %.0f tick" % abs(pro[250][0] - pro[2500][0]))
            print("    (c) la circolazione, su tutti gli stati salvati fino a k %d:" % k)
            ori, righe = [], []
            for kk in range(250, k + 1, 250):
                fk = os.path.join(d, "stato_%06d.npz" % kk)
                Xk, _m, _h = leggi(fk)
                cam.A[...] = Xk["campo_A"]
                B = cam.B()
                rk = np.zeros(n)
                np.add.at(rk, mot.inc.nodo, np.sum(np.abs(Xk["psi_h"]) ** 2, axis=1))
                ck = []
                for j in range(3):
                    sett = np.abs(((angn - angv[j]) + 180.0) % 360.0 - 180.0) < 60.0
                    w = rk[sett]
                    ck.append((xyn[sett] * w[:, None]).sum(axis=0) / w.sum())
                cm = np.mean(np.array(ck), axis=0)
                rB = np.hypot(*(TO.scarti(q1, q2, G[0], G[1], L)[:, :2] - cm).T)
                bm = float(B[rB <= R_DISCO].mean())
                fl = float(B[rB <= R_FLUSSO].sum())
                rr = np.hypot(xyn[:, 0], xyn[:, 1])
                sel = rr <= R_RHO
                ori.append(math.degrees(np.angle(np.sum(rk[sel] * np.exp(3j * np.radians(angn[sel]))))) / 3.0)
                righe.append((kk, bm, fl))
            ori = srotola(ori)
            for (kk, bm, fl), o in zip(righe, ori):
                print("      k %5d: B medio (8) %+.4e (%s), il flusso (30) %+.4e; l'orientamento a tre punte di rho (32) %+.2f gradi" % (kk, bm, "+" if bm > 0 else "-", fl, o))
            seg = [np.sign(b) for _k, b, _f in righe]
            print("    (c) il segno di B: %s; il 15/11 (T120, il bordo da R_A, senza chi): negativo a k 500-2000 (-6.2e-04 .. -1.26e-03); l'orientamento da %+.2f a %+.2f (il 15/11 T120: -30.00 -> -18.96 in 2000 tick)" % (
                "costante" if len(set(seg)) == 1 else "### CAMBIA", ori[0], ori[-1]))
        Z["metti"]()


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("giro")
    g.add_argument("--k", type=int, required=True)
    x = ap.parse_args(argv)
    caso_noto()
    giro(x.k)
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
