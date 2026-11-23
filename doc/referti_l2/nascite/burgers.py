# -*- coding: utf-8 -*-
r"""**[M1751-L] S5-S6: IL DIZIONARIO DEI BURGERS E LA «FORZA» FRA LE DISLOCAZIONI** *(Luca, 2026-11-23; la carta `doc/CARTA_gradi_di_liberta.md`, sez. `0.4`, `0.5`, `1`; SOLA LETTURA degli stati salvati, nessun motore)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/nascite/burgers.py > doc/referti_l2/nascite/burgers.txt

**A ogni stato salvato** *(MITOSI `36000`, `36250`; MITOSI-v2 da `36500` a `45976`)*: i gradi; **le coppie 5-7 LEGATE** *(un 5 e un 7 adiacenti: l'assegnamento ottimo `linear_sum_assignment` sugli archi 5-7)*; **`b = R_{+90}(x_7 - x_5)/|x_7 - x_5|`** arrotondato alla piu' vicina delle sei direzioni del favo *(la teoria dei difetti, non le righe: la carta sez. 0.5)*; la somma dei `b`; il catalogo; **le annullanti** *(due coppie con `b` opposti entro `3` passi)*. **S6:** le coppie seguite fra stati consecutivi *(la piu' vicina con lo stesso `b`, entro `2` unita')*; per ogni coppia di coppie seguite in tre stati consecutivi la variazione seconda di `r` *(l'«accelerazione» per `250^2` tick)*; i fit `a r^(-p)`, `a r^(-1)`, `a r^(-2)` sulle medie per classi di `r`; il segno contro `b_1 . b_2`. ### **Il grafo cambia solo alle nascite** *(la carta sez. 0.4)*: il moto e' della regola.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import nascite_lettura as NL  # noqa: E402

DIREZIONI = np.array([[math.cos(math.radians(60 * q)), math.sin(math.radians(60 * q))] for q in range(6)])
VICINE = 3
SEGUI = 2.0
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def scarto(X, a, b):
    """### `x_b - x_a` nel disegno *(l'immagine minima, `toro.scarti`)*."""
    from solitone import toro as TO
    d = TO.scarti(np.asarray([X["m1"][b]]), np.asarray([X["m2"][b]]), X["m1"][a], X["m2"][a], NL.L)
    return np.asarray(d[0][:2], float)


def coppie(X):
    from scipy.optimize import linear_sum_assignment
    A = NL.adiacenza(X)
    g = np.bincount(np.concatenate([X["ii"], X["jj"]]), minlength=X["n"])
    c5, c7 = np.nonzero(g == 5)[0], np.nonzero(g == 7)[0]
    out = []
    if c5.size and c7.size:
        M = A[c5][:, c7].toarray()
        costo = np.where(M > 0, 1.0, 1e6)
        r, c = linear_sum_assignment(costo)
        for a, b in zip(r, c):
            if M[a, b] > 0:
                v5, v7 = int(c5[a]), int(c7[b])
                d = scarto(X, v5, v7)
                bb = np.array([-d[1], d[0]]) / np.linalg.norm(d)
                q = int(np.argmax(DIREZIONI @ bb))
                mid = np.array([X["m1"][v5], X["m2"][v5]], float)
                out.append({"cinque": v5, "sette": v7, "q": q, "b": DIREZIONI[q], "scarto": float(np.degrees(np.arccos(min(1.0, float(DIREZIONI[q] @ bb))))), "nodo": v5, "pos": mid})
    altri = {int(x): int(g[x]) for x in np.nonzero((g != 6) & (g != 5) & (g != 7))[0]}
    return out, int(c5.size), int(c7.size), altri, A


def main():
    import _presidio
    from scipy.sparse import csgraph
    _presidio.avvia(os.path.join(NL._SU, "coppie_57.py"))
    _presidio.avvia(os.path.join(_QUI, "nascite_lettura.py"))
    _presidio.avvia(__file__)
    print("=" * 140)
    print("[M1751-L] S5-S6: I BURGERS E LA «FORZA» (la carta sez. 0.4, 0.5, 1). ### b e' della teoria dei difetti (perpendicolare al legame 5-7), non delle righe; il grafo cambia solo alle nascite")
    print("=" * 140)
    stati = [(k, f) for k, f in NL.elenco_stati() if k >= 36000]
    serie = []
    for k, f in stati:
        X = NL.leggi(f)
        P, n5, n7, altri, A = coppie(X)
        sb = np.sum([p["b"] for p in P], axis=0) if P else np.zeros(2)
        cat = np.bincount([p["q"] for p in P], minlength=6)
        ann = 0
        if P:
            nodi = np.array([p["cinque"] for p in P])
            D = csgraph.dijkstra(A, unweighted=True, indices=nodi, limit=VICINE + 0.5)[:, nodi]
            for a in range(len(P)):
                if any(D[a, c] <= VICINE and P[a]["q"] == (P[c]["q"] + 3) % 6 for c in range(len(P)) if c != a):
                    ann += 1
        print("  k %5d (nascite %3d): 5 %3d, 7 %3d, legate %3d; altri gradi %s; |somma b| %.3e; i tipi (0, 60, ..., 300 gradi) %s; annullanti %d (%.3f); lo scarto angolare massimo da una direzione %.2f gradi" % (
            k, X["meta"]["nascite"], n5, n7, len(P), dict(sorted(__import__("collections").Counter(altri.values()).items())), float(np.linalg.norm(sb)), list(cat), ann, ann / max(len(P), 1), max((p["scarto"] for p in P), default=0.0)))
        serie.append({"k": k, "P": P, "X": {x: X[x] for x in ("m1", "m2")}, "n5": n5, "n7": n7, "sb": sb, "cat": cat, "ann": ann, "nascite": X["meta"]["nascite"]})
    s0 = serie[0]
    esito("K1 a k 36000 (una nascita): due coppie legate e la somma dei b zero (un dipolo)", len(s0["P"]) == 2 and float(np.linalg.norm(s0["sb"])) < 1e-9, "legate %d, |somma b| %.3e" % (len(s0["P"]), float(np.linalg.norm(s0["sb"]))))
    esito("K1 a k 36250 (M1, P-M2): 8 cinque e 8 sette, tutti in coppie legate", s0 is not None and serie[1]["n5"] == 8 and serie[1]["n7"] == 8 and len(serie[1]["P"]) == 8, "5 %d, 7 %d, legate %d" % (serie[1]["n5"], serie[1]["n7"], len(serie[1]["P"])))
    zero = [float(np.linalg.norm(s["sb"])) for s in serie]
    print("### la somma dei b su tutto il toro: il massimo |somma b| sugli stati %.3e" % max(zero))
    fin = serie[-1]
    tot = int(np.sum(fin["cat"]))
    o = np.sort(fin["cat"])[::-1]
    print("### S5 IL CATALOGO a k %d: %d coppie legate (5 %d, 7 %d); i tipi %s; i 4 piu' frequenti coprono %.4f; le annullanti %.4f" % (
        fin["k"], tot, fin["n5"], fin["n7"], list(fin["cat"]), float(o[:4].sum() / max(tot, 1)), fin["ann"] / max(tot, 1)))
    # ### S6: seguire le coppie
    print("-" * 140)
    print("S6 LE COPPIE SEGUITE (la piu' vicina con lo stesso b, entro %.1f) e la variazione seconda di r fra coppie seguite in tre stati consecutivi" % SEGUI)
    from solitone import toro as TO
    import coppie_57 as CP
    Sf = CP.stato(os.path.join(NL.D_2, "stato_45976.npz"))
    XY = np.asarray(TO.scarti(Sf["m1"], Sf["m2"], Sf["centro"][0], Sf["centro"][1], NL.L))[:, :2]
    print("    le posizioni: una volta, dal centro della materia a k 45976 (le coppie stanno nell'anello r %.1f-%.1f, lontano dal bordo del toro L %d)" % (
        float(np.min(Sf["r"][[p["cinque"] for p in serie[-1]["P"]]])), float(np.max(Sf["r"][[p["cinque"] for p in serie[-1]["P"]]])), NL.L))

    def distanza(_X, a, b):
        return float(np.linalg.norm(XY[b] - XY[a]))
    traccia = []
    for t in range(len(serie) - 1):
        a, b = serie[t], serie[t + 1]
        m = {}
        for i, p in enumerate(a["P"]):
            best, bd = None, None
            for j, q in enumerate(b["P"]):
                if q["q"] != p["q"]:
                    continue
                d = distanza(None, p["cinque"], q["cinque"])
                if d <= SEGUI and (bd is None or d < bd):
                    best, bd = j, d
            if best is not None:
                m[i] = (best, bd)
        mosse = [v[1] for v in m.values()]
        traccia.append(m)
        if t % 8 == 0 or t == len(serie) - 2:
            print("    da k %d a k %d: seguite %d su %d; ferme (spostamento 0) %d; lo spostamento medio %.3f" % (a["k"], b["k"], len(m), len(a["P"]), sum(1 for x in mosse if x == 0.0), float(np.mean(mosse)) if mosse else float("nan")))
    R, ACC, SG = [], [], []
    for t in range(1, len(serie) - 1):
        m0, m1 = traccia[t - 1], traccia[t]
        inv0 = {v[0]: i for i, v in m0.items()}
        vive = [(inv0[j], j, m1[j][0]) for j in m1 if j in inv0]
        if len(vive) < 2:
            continue
        idx = [np.array([serie[t - 1 + u]["P"][v[u]]["cinque"] for v in vive]) for u in range(3)]
        bq = np.array([serie[t]["P"][v[1]]["b"] for v in vive])
        rr = [np.linalg.norm(XY[idx[u]][:, None, :] - XY[idx[u]][None, :, :], axis=2) for u in range(3)]
        iu = np.triu_indices(len(vive), 1)
        r1 = rr[1][iu]
        s = r1 > 0
        R += list(r1[s])
        ACC += list((rr[2][iu] - 2 * rr[1][iu] + rr[0][iu])[s])
        SG += list((bq @ bq.T)[iu][s])
    R, ACC, SG = np.array(R), np.array(ACC), np.array(SG)
    print("    le coppie di coppie seguite in tre stati: %d; l'accelerazione NON zero in %d (%.4f)" % (len(R), int(np.sum(ACC != 0)), float(np.mean(ACC != 0)) if len(R) else 0.0))
    if len(R) and np.sum(ACC != 0) >= 5:
        bordi = np.arange(1, 42, 2.0)
        cx, cy = [], []
        for a, b in zip(bordi[:-1], bordi[1:]):
            s = (R >= a) & (R < b) & (ACC != 0)
            if s.sum() >= 3:
                cx.append(float(R[s].mean()))
                cy.append(float(np.mean(np.abs(ACC[s]))))
        cx, cy = np.array(cx), np.array(cy)
        if len(cx) >= 3:
            lx, ly = np.log(cx), np.log(cy)
            p, c = np.polyfit(lx, ly, 1, cov=True)
            res = ly - np.polyval(p, lx)
            r2 = 1 - float(np.sum(res ** 2) / np.sum((ly - ly.mean()) ** 2))
            print("    il fit |acc| = a r^(-p) sulle medie per classi di r (%d classi): p = %.3f +- %.3f, R^2 %.3f" % (len(cx), -p[0], math.sqrt(c[0, 0]), r2))
            for pp in (1.0, 2.0):
                a = float(np.exp(np.mean(ly + pp * lx)))
                rr = ly - (np.log(a) - pp * lx)
                print("    il fit a r^(-%g): a %.4e, R^2 %.3f" % (pp, a, 1 - float(np.sum(rr ** 2) / np.sum((ly - ly.mean()) ** 2))))
            nz = ACC != 0
            el = np.mean(np.sign(ACC[nz]) == np.sign(SG[nz])) if nz.any() else float("nan")
            print("    il segno elastico (acc > 0 se b1.b2 > 0, repulsione fra uguali): %.4f delle coppie con acc != 0 (%d)" % (el, int(nz.sum())))
            v = "LEGGE 2D" if (abs(-p[0] - 1) <= 0.3 and el > 0.7) else ("NESSUNA LEGGE" if r2 < 0.5 else "UNA LEGGE CON p %.2f" % (-p[0]))
            print("### K5: %s" % v)
        else:
            print("### K5: NON MISURATO (meno di 3 classi di r con accelerazioni non zero)")
    else:
        print("### K5: NON MISURATO (le accelerazioni non zero sono meno di 5)")
    print("=" * 140)
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0


if __name__ == "__main__":
    sys.exit(main())
