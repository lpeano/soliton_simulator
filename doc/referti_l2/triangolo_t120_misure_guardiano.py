# -*- coding: utf-8 -*-
r"""**LE MISURE DEL GUARDIANO DALLE MAPPE DEL TRIANGOLO A 120, RIFATTE NEL REPO** *(Luca `2026-11-17` `11:33`, A1-A5; la carta `doc/TASK_HISTORY/2026-11-17_misure_CP_mitosi.md`, sez. `2.1`; SOLA LETTURA delle mappe)*.

    E:\python\py3132\python.exe doc/referti_l2/triangolo_t120_misure_guardiano.py > doc/referti_l2/triangolo_t120_misure_guardiano.txt

**Le mappe** *(`doc/referti_l2/mattone/`)*: `triangolo_t120_mappe.npz` *(`0`-`2000` ogni `20`)*, `legati_t120_mappe_02000.npz` *(`2000`-`5960` ogni `60`)*, `legati_t120_mappe_06000.npz` *(`6000`-`12000` ogni `60`)*; **un fotogramma per tick** *(dove due file si toccano, quello che COMINCIA li')*.
**Il baricentro:** la media dei tre centri a `k 0` *(coordinate di indice)*, fisso; `theta = atan2(y, x)` dello scarto `toro.scarti`.
**I fotogrammi richiesti e assenti** *(`3000`, i multipli di `500`)*: **il piu' vicino, col suo tick stampato.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_SOL, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from solitone import toro as TO  # noqa: E402

MAPPE = ("triangolo_t120_mappe.npz", "legati_t120_mappe_02000.npz", "legati_t120_mappe_06000.npz")
ANELLI_A1 = ((12, 17), (17, 22), (22, 27), (27, 32))
R_FIN = 5.5           # la finestra delle culle: il disco di diametro 11 nodi (la carta, sez. 1, punto 2)
R_MEDIANA = 45.0


def carica():
    rif = os.path.join(_RADICE, "doc", "referti_l2", "mattone")
    F = {}
    geo = None
    for f in MAPPE:
        with np.load(os.path.join(rif, f)) as d:
            if geo is None:
                geo = {k: d[k].copy() for k in ("m1", "m2", "x", "y", "L")}
            else:
                assert all(np.array_equal(geo[k], d[k]) for k in ("m1", "m2", "L")), "le mappe hanno geometrie diverse: FERMO"
            for i, k in enumerate(d["tick"]):
                F[int(k)] = (d["rho"][i].astype(float), d["dphi"][i].astype(float), d["centri"][i].astype(float), f)
    return F, geo


def m_esima(w, th, sel, m):
    """### `(ampiezza, arg)` di `somma w e^{-i m theta}` sui nodi `sel`."""
    S = np.sum(w[sel] * np.exp(-1j * m * th[sel]))
    return abs(S) / float(np.sum(w[sel])), math.atan2(S.imag, S.real)


def vicino(ks, k):
    return min(ks, key=lambda q: (abs(q - k), q))


def main():
    sys.path.insert(0, _CSV)
    import _presidio
    _presidio.avvia(__file__)
    F, geo = carica()
    ks = sorted(F)
    L = int(geo["L"])
    m1, m2 = geo["m1"].astype(float), geo["m2"].astype(float)
    c0 = F[0][2]
    bar = (float(c0[:, 0].mean()), float(c0[:, 1].mean()))
    D = TO.scarti(m1, m2, bar[0], bar[1], L)
    r = np.hypot(D[:, 0], D[:, 1])
    th = np.arctan2(D[:, 1], D[:, 0])
    print("=" * 130)
    print("LE MISURE DEL GUARDIANO DALLE MAPPE DEL TRIANGOLO A 120, RIFATTE NEL REPO (Luca 2026-11-17 11:33, A1-A5)")
    print("=" * 130)
    print("### %d fotogrammi da %d a %d (le mappe: %s); L %d; il baricentro dei tre centri a k 0 (%.3f, %.3f) (indici)" % (len(ks), ks[0], ks[-1], ", ".join(MAPPE), L, bar[0], bar[1]))
    esiti = []
    # ---------------------------------------------------------------- il caso noto (Q-A4)
    f0 = np.exp(-((r - 22.0) / 5.0) ** 2)
    a0 = None
    for al in (0.0, 10.0, -7.0):
        w = f0 * (1.0 + 0.5 * np.cos(3.0 * (th - math.radians(al))))
        _A, g = m_esima(w, th, r <= 40, 3)
        if a0 is None:
            a0 = g
        rot = -math.degrees(math.atan2(math.sin(g - a0), math.cos(g - a0))) / 3.0
        print("    il caso noto: la tre punte ruotata di %+.1f gradi -> la rotazione misurata %+.4f" % (al, rot))
        if al != 0.0:
            esiti.append(("il caso noto: la rotazione %+.0f misurata entro 0.01 gradi" % al, abs(rot - al) < 0.01))
    # ---------------------------------------------------------------- A1
    print("-" * 130)
    k3 = vicino(ks, 3000)
    print("### A1. LA ROTAZIONE PER ANELLI SOTTILI (la m=3 di rho): -unwrap(arg)/3, rispetto al fotogramma %d (il piu' vicino a 3000); ogni fotogramma fra 2500 e 6000" % k3)
    kk = [k for k in ks if 2500 <= k <= 6000]
    tab = {}
    for a, b in ANELLI_A1:
        sel = (r >= a) & (r < b)
        amp, arg = zip(*[m_esima(F[k][0], th, sel, 3) for k in kk])
        u = np.unwrap(np.array(arg))
        rot = -np.degrees(u - u[kk.index(k3)]) / 3.0
        tab[(a, b)] = (np.array(amp), rot)
    print("    %6s  " % "k" + "  ".join("%7s-%-2s rot  amp  " % (a, b) for a, b in ANELLI_A1))
    for i, k in enumerate(kk):
        if i % 5 == 0 or k in (vicino(ks, 5000), k3, kk[-1]):
            print("    %6d  " % k + "  ".join("%+9.2f %6.3f   " % (tab[q][1][i], tab[q][0][i]) for q in ANELLI_A1))
    k5 = vicino(kk, 5000)
    i5 = kk.index(k5)
    print("    a k %d (il piu' vicino a 5000): %s" % (k5, ", ".join("%d-%d %+.2f gradi" % (q[0], q[1], tab[q][1][i5]) for q in ANELLI_A1)))
    for q in ANELLI_A1:
        rr = tab[q][1]
        print("    l'anello %d-%d: la rotazione fra %+.2f e %+.2f gradi; l'ampiezza fra %.3f e %.3f" % (q[0], q[1], float(rr.min()), float(rr.max()), float(tab[q][0].min()), float(tab[q][0].max())))
    est = tab[(27, 32)][1]
    print("    il 27-32 contro gli altri: %d fotogrammi su %d con il 27-32 AVANTI (rotazione maggiore) a tutti e tre gli altri anelli" % (
        int(np.sum(np.all([est >= tab[q][1] for q in ANELLI_A1[:3]], axis=0))), len(kk)))
    # ---------------------------------------------------------------- A2
    print("-" * 130)
    print("### A2. LE CULLE: per ogni centro, il baricentro di dphi sopra la mediana (la mediana entro %.0f nodi dal baricentro) nel disco di raggio %.1f nodi attorno al centro; ogni fotogramma 0-12000" % (R_MEDIANA, R_FIN))
    dist, sfas, rc, ru, tt = [], [], [], [], []
    for k in ks:
        rho, dph, cen, _f = F[k]
        med = float(np.median(dph[r <= R_MEDIANA]))
        dd, ss, rcc, ruu = [], [], [], []
        for j in range(3):
            Dj = TO.scarti(m1, m2, cen[j, 0], cen[j, 1], L)
            sel = np.hypot(Dj[:, 0], Dj[:, 1]) <= R_FIN
            w = np.clip(dph[sel] - med, 0.0, None)
            if w.sum() <= 0:
                dd.append(float("nan")); ss.append(float("nan")); rcc.append(float("nan")); ruu.append(float("nan"))
                continue
            cx = float(np.sum(w * Dj[sel, 0]) / w.sum())
            cy = float(np.sum(w * Dj[sel, 1]) / w.sum())
            dd.append(math.hypot(cx, cy))
            pc = TO.scarti(np.array([cen[j, 0]]), np.array([cen[j, 1]]), bar[0], bar[1], L)[0]
            pu = (pc[0] + cx, pc[1] + cy)
            a_c, a_u = math.atan2(pc[1], pc[0]), math.atan2(pu[1], pu[0])
            ss.append(math.degrees(math.atan2(math.sin(a_u - a_c), math.cos(a_u - a_c))))
            rcc.append(math.hypot(pc[0], pc[1]))
            ruu.append(math.hypot(*pu))
        dist.append(dd); sfas.append(ss); rc.append(rcc); ru.append(ruu); tt.append(k)
    dist, sfas, rc, ru, tt = map(np.array, (dist, sfas, rc, ru, tt))
    print("    la distanza culla-centro: la mediana %.3f nodi, il 5%% %.3f, il 95%% %.3f, il massimo %.3f; i fotogrammi senza culla (dphi mai sopra la mediana): %d" % (
        float(np.nanmedian(dist)), float(np.nanpercentile(dist, 5)), float(np.nanpercentile(dist, 95)), float(np.nanmax(dist)), int(np.sum(np.isnan(dist)))))
    print("    lo sfasamento in angolo (la culla meno il centro, attorno al baricentro): la mediana %+.2f gradi, il 5%% %+.2f, il 95%% %+.2f, il minimo %+.2f, il massimo %+.2f" % (
        float(np.nanmedian(sfas)), float(np.nanpercentile(sfas, 5)), float(np.nanpercentile(sfas, 95)), float(np.nanmin(sfas)), float(np.nanmax(sfas))))
    for j in range(3):
        ok = ~np.isnan(sfas[:, j])
        p = np.polyfit(tt[ok], sfas[ok, j], 1)
        print("    il centro %d: lo sfasamento, la pendenza %+.3f gradi per 1000 tick (da %+.2f a %+.2f in 12000 tick, la retta)" % (j, 1000 * p[0], np.polyval(p, 0), np.polyval(p, 12000)))
    print("    il raggio medio dei centri dal baricentro: da %.2f a %.2f; delle culle: da %.2f a %.2f" % (float(np.nanmin(rc.mean(1))), float(np.nanmax(rc.mean(1))), float(np.nanmin(ru.mean(1))), float(np.nanmax(ru.mean(1)))))
    # ---------------------------------------------------------------- A3, A4
    print("-" * 130)
    print("### A3 + A4: ai fotogrammi piu' vicini ai multipli di 500: la m=3 di dphi negli anelli 30-45 (il guscio) e 12-28 (ampiezza, orientamento -unwrap(arg)/3 rispetto al primo); la m=3 e la m=6 di rho nell'anello 12-32")
    k500 = [vicino(ks, 500 * i) for i in range(25)]
    sg, si = (r >= 30) & (r < 45), (r >= 12) & (r < 28)
    sr = (r >= 12) & (r < 32)
    g = [m_esima(F[k][1], th, sg, 3) for k in k500]
    gi = [m_esima(F[k][1], th, si, 3) for k in k500]
    ug = -np.degrees(np.unwrap([x[1] for x in g]) - np.unwrap([x[1] for x in g])[0]) / 3.0
    ui = -np.degrees(np.unwrap([x[1] for x in gi]) - np.unwrap([x[1] for x in gi])[0]) / 3.0
    r3 = [m_esima(F[k][0], th, sr, 3)[0] for k in k500]
    r6 = [m_esima(F[k][0], th, sr, 6)[0] for k in k500]
    print("    %6s  %22s  %22s  %16s" % ("k", "guscio 30-45 amp rot", "interno 12-28 amp rot", "rho m=3  m=6"))
    for i, k in enumerate(k500):
        print("    %6d  %10.3f %+10.2f  %10.3f %+10.2f  %8.3f %7.3f" % (k, g[i][0], ug[i], gi[i][0], ui[i], r3[i], r6[i]))
    # ---------------------------------------------------------------- A5
    print("-" * 130)
    print("### A5. IL TRIANGOLO DEI CENTRI: l'orientamento -unwrap(arg somma_j e^{-3 i theta_j})/3 attorno al loro baricentro, rispetto a k 0")
    ori = []
    for k in ks:
        cen = F[k][2]
        cb = TO.centro(np.ones(3), cen[:, 0], cen[:, 1], L)[:2]
        P = TO.scarti(cen[:, 0], cen[:, 1], cb[0], cb[1], L)
        S = np.sum(np.exp(-3j * np.arctan2(P[:, 1], P[:, 0])))
        ori.append(math.atan2(S.imag, S.real))
    ori = -np.degrees(np.unwrap(ori) - np.unwrap(ori)[0]) / 3.0
    for k in [vicino(ks, 1000 * i) for i in range(13)]:
        print("    k %6d  l'orientamento %+8.2f gradi" % (k, ori[ks.index(k)]))
    print("    fra 9000 e 9500, fotogramma per fotogramma (i tre centri in indici e l'orientamento):")
    for k in [q for q in ks if 9000 <= q <= 9500]:
        cen = F[k][2]
        print("    k %6d  %s  %+8.2f" % (k, "  ".join("(%7.2f, %7.2f)" % (cen[j, 0], cen[j, 1]) for j in range(3)), ori[ks.index(k)]))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-100s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
