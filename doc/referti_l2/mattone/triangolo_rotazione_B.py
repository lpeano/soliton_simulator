# -*- coding: utf-8 -*-
r"""**IL CAMPO B E LA ROTAZIONE DEL TRIANGOLO A 120 GRADI SU TUTTA LA CORSA** *(Luca `2026-11-16` `09:25`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24.36`; SOLO LETTURA)*.

    E:\python\py3132\python.exe doc/referti_l2/mattone/triangolo_rotazione_B.py > doc/referti_l2/mattone/triangolo_t120_rotazione_B.txt     (PYTHONNOUSERSITE=1, TMP su E:)

**(a) la rotazione dalle MAPPE** *(`rho` per nodo)*: **`S = somma rho e^{-3 i theta}` sull'anello `12`-`32` attorno al baricentro periodico di `rho`; l'angolo = `-arg(S)/3`, srotolato.**
**(b) `I = somma rho r^2`** *(entro la meta' periodo)*; **`L = somma_k J_k (r_k x d_k)_z`** *(`J` = `energia.corrente`, l'ENERGIA portata dallo spostamento da `ii` a `jj`)* **dagli stati completi.**
**(c) `B`** *(`_u1_prototipo.Campo.B`, per placchetta)* **medio nel disco `8` e il flusso entro `30`, dagli stati completi.**
"""
import json
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

ANELLO = (12.0, 32.0)
R_DISCO, R_FLUSSO = 8.0, 30.0
MAPPE = ("triangolo_t120_mappe.npz", "legati_t120_mappe_02000.npz", "legati_t120_mappe_06000.npz")
SERIE = ("triangolo_t120_serie.npz", "legati_t120_serie_02000.npz", "legati_t120_serie_06000.npz")
STATI_120 = [("triangolo_t120", k) for k in (500, 1000, 1500, 2000)] + [("legati_t120", k) for k in range(3000, 12001, 1000)]
STATI_FASE = [("triangolo_video", k) for k in (500, 1000, 1500, 2000)]
GUARDIANO = {2000: 10.0, 4000: 15.0, 8000: 32.0, 9000: 66.0, 12000: 98.0}


def geometria(rho, m1, m2, L):
    c1, c2, _x, _y = TO.centro(rho, m1, m2, L)
    D = TO.scarti(m1, m2, c1, c2, L)
    return c1, c2, D[:, 0], D[:, 1]


def forma(rho, m1, m2, L):
    """### `(arg S, ampiezza |S|/somma rho sull'anello, I, il centro)`."""
    c1, c2, dx, dy = geometria(rho, m1, m2, L)
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    a = (r >= ANELLO[0]) & (r <= ANELLO[1])
    S = complex(np.sum(rho[a] * np.exp(-3j * th[a])))
    meta = TO.meta_periodo(L)
    I = float(np.sum((rho * r * r)[r <= meta]))
    return math.atan2(S.imag, S.real), abs(S) / float(np.sum(rho[a])), I, (c1, c2)


def lati():
    k, l = [], []
    for f in SERIE:
        s = np.load(os.path.join(MT.DIR_REF, f))
        for i, kk in enumerate(s["k"]):
            if int(kk) not in k:
                k.append(int(kk))
                l.append(float((s["l_AB"][i] + s["l_BC"][i] + s["l_CA"][i]) / 3.0))
    o = np.argsort(k)
    return np.array(k)[o], np.array(l)[o]


def rotazione():
    tk, arg, amp, II = [], [], [], []
    for f in MAPPE:
        d = np.load(os.path.join(MT.DIR_REF, f))
        L = int(d["L"])
        m1, m2 = d["m1"].astype(float), d["m2"].astype(float)
        for i, k in enumerate(d["tick"]):
            if int(k) in tk:
                continue
            a, am, I, _c = forma(d["rho"][i].astype(float), m1, m2, L)
            tk.append(int(k))
            arg.append(a)
            amp.append(am)
            II.append(I)
    o = np.argsort(tk)
    tk, arg, amp, II = np.array(tk)[o], np.unwrap(np.array(arg)[o]), np.array(amp)[o], np.array(II)[o]
    ang = -np.degrees(arg - arg[0]) / 3.0
    return tk, ang, amp, II


def main():
    import _presidio
    import energia as EN
    _presidio.avvia(os.path.join(_SOL, "mattone.py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL CAMPO B E LA ROTAZIONE DEL TRIANGOLO A 120 GRADI (Luca 2026-11-16 09:25; solo lettura); sys.executable %s" % sys.executable)
    print("  il centro: il baricentro periodico di rho; l'anello %g-%g; l'angolo della forma = -arg(somma rho e^{-3i theta})/3, srotolato" % ANELLO)
    print("=" * 130)
    tk, ang, amp, II = rotazione()
    kl, ll = lati()
    print("### (a) LA ROTAZIONE DALLE MAPPE: %d istanti da k %d a %d" % (len(tk), tk[0], tk[-1]))
    print("### IL CONTROLLO DI SCALA contro i numeri del guardiano (gradi; entro 3):")
    scala = True
    for k, g in sorted(GUARDIANO.items()):
        m = float(np.interp(k, tk, ang))
        ok = abs(m - g) <= 3.0
        scala = scala and ok
        print("    k %5d: il guardiano %+6.1f, qui %+7.2f  %s" % (k, g, m, "ok" if ok else "### FUORI"))
    print("  DEVE: la rotazione entro 3 gradi dal guardiano nei 5 punti  %s" % ("PASSA" if scala else "### FALLISCE"))
    print("    %6s %10s %12s %10s %14s %12s" % ("k", "angolo", "omega/1000", "ampiezza", "I", "lato medio"))
    rig = {}
    for k in range(0, 12001, 500):
        a = float(np.interp(k, tk, ang))
        a2 = float(np.interp(min(k + 250, tk[-1]), tk, ang))
        a1 = float(np.interp(max(k - 250, tk[0]), tk, ang))
        om = (a2 - a1) / (min(k + 250, tk[-1]) - max(k - 250, tk[0])) * 1000.0
        rig[k] = (a, om, float(np.interp(k, tk, amp)), float(np.interp(k, tk, II)), float(np.interp(k, kl, ll)))
        print("    %6d %+10.2f %+12.2f %10.4f %14.6e %12.3f" % ((k,) + rig[k]))
    j = int(np.argmin(ll))
    print("### il minimo del lato: %.3f a k %d" % (ll[j], kl[j]))
    print("-" * 130)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    righe = {}
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        C = MT.Campi(Z, "MGU", rho_c, e)
        cam = C.campo
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        p1 = np.concatenate([m1 + 2.0 / 3.0, m1 + 1.0 / 3.0])
        p2 = np.concatenate([m2 + 1.0 / 3.0, m2 + 2.0 / 3.0])
        mot = Z["mot"]
        ii, jj = np.asarray(mot.inc.ii), np.asarray(mot.inc.jj)
        meta = TO.meta_periodo(L)
        print("### (b) e (c) DAGLI STATI COMPLETI: B medio nel disco %g e il flusso entro %g; L dalla corrente di ENERGIA; I entro %d" % (R_DISCO, R_FLUSSO, meta))
        print("    %-16s %6s %-20s %12s %12s %14s %14s %12s" % ("la corsa", "k", "il centro (rho)", "B medio (8)", "flusso (30)", "L", "I", "L/I"))
        for nome, stati in (("120", STATI_120), ("T-fase", STATI_FASE)):
            for pref, k in stati:
                with np.load(os.path.join(MT.DIR_E, "%s_%05d.npz" % (pref, k))) as dd:
                    Z["metti"]({x: dd[x].copy() for x in Z["chiavi"]})
                    cam.A[...] = dd["campo_A"]
                rho = MT.rho_di(Z)
                c1, c2, dx, dy = geometria(rho, m1, m2, L)
                B = cam.B()
                rp = np.hypot(*TO.scarti(p1, p2, c1, c2, L).T[:2])
                bm = float(B[rp <= R_DISCO].mean())
                fl = float(B[rp <= R_FLUSSO].sum())
                J = np.asarray(EN.corrente(Z["st"], mot, Z["par"], None), dtype=float)
                dd_ = TO.scarti(m1[jj], m2[jj], m1[ii], m2[ii], L)
                rx, ry = dx[ii] + 0.5 * dd_[:, 0], dy[ii] + 0.5 * dd_[:, 1]
                dentro = np.hypot(rx, ry) <= meta
                Lz = float(np.sum((J * (rx * dd_[:, 1] - ry * dd_[:, 0]))[dentro]))
                r = np.hypot(dx, dy)
                I = float(np.sum((rho * r * r)[r <= meta]))
                righe[(nome, k)] = (bm, fl, Lz, I)
                print("    %-16s %6d (%7.2f, %7.2f)   %+12.4e %+12.4e %+14.6e %14.6e %+12.4e" % (nome, k, c1, c2, bm, fl, Lz, I, Lz / I))
                sys.stdout.flush()
        Z["metti"]()
    print("-" * 130)
    s120 = [(k, righe[("120", k)]) for _p, k in STATI_120]
    Ls = np.array([x[1][2] for x in s120])
    print("### (b) L: la media %+.4e, la variazione massima %.1f%% della media; il segno di L %s; il verso della rotazione %s"
          % (Ls.mean(), 100.0 * np.max(np.abs(Ls - Ls.mean())) / abs(Ls.mean()), sorted(set("+" if x > 0 else "-" for x in Ls)), "+" if ang[-1] > 0 else "-"))
    print("    LA LETTURA (fissata prima): L costante se entro il 10%%: %s" % ("SI'" if np.max(np.abs(Ls - Ls.mean())) <= 0.1 * abs(Ls.mean()) else "NO"))
    print("    T-fase: |L| a 2000 %.4e contro 120 a 2000 %.4e (il rapporto %.3f)" % (abs(righe[("T-fase", 2000)][2]), abs(righe[("120", 2000)][2]), abs(righe[("T-fase", 2000)][2]) / abs(righe[("120", 2000)][2])))
    print("### LA PATTINATRICE: omega misurato (dalla rotazione, gradi per 1000 tick) contro omega previsto = omega(k0) (L/I)(k) / (L/I)(k0), k0 = 3000")
    k0 = 3000
    LI0 = righe[("120", k0)][2] / righe[("120", k0)][3]
    om0 = rig[k0][1]
    for k, x in s120:
        prev = om0 * (x[2] / x[3]) / LI0
        mis = rig[k][1]
        print("    k %5d: omega misurato %+8.2f, previsto %+8.2f, il rapporto %s; il lato %.3f; B al centro %+.4e" % (k, mis, prev, "%.2f" % (mis / prev) if prev else "--", rig[k][4], x[0]))
    kmin = int(round(kl[j] / 1000.0) * 1000)
    if ("120", kmin) in righe:
        x = righe[("120", kmin)]
        prev = om0 * (x[2] / x[3]) / LI0
        q = rig[kmin][1] / prev if prev else float("nan")
        print("    LA LETTURA (fissata prima), al minimo del lato (lo stato piu' vicino, k %d): misurato / previsto %.2f -> la pattinatrice %s" % (kmin, q, "SPIEGA" if 0.7 <= q <= 1.4 else "NON spiega"))
    print("### (c) B DOPO L'ARROTOLAMENTO (circa k 2800): il segno e |B| contro k 2000 (%+.4e):" % righe[("120", 2000)][0])
    b2 = righe[("120", 2000)][0]
    resta = True
    for k in range(3000, 12001, 1000):
        b = righe[("120", k)][0]
        ok = (b * b2 > 0) and abs(b) >= 0.1 * abs(b2)
        resta = resta and ok
        print("    k %5d: B %+.4e (%.2f di quello a 2000) %s" % (k, b, b / b2, "" if ok else "###"))
    print("    LA LETTURA (fissata prima): B %s" % ("RESTA (stesso segno, sopra il 10%)" if resta else "NON resta a ogni tick (vedi le righe ###)"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
