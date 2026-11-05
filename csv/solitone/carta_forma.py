# -*- coding: utf-8 -*-
r"""**LA FORMA DEL SOLITONE: ESAGONO O DISCO, E LA CORONA** *(Luca `2026-11-04` `20:18`-`22:26`, i criteri `FX` di Luca del `2026-11-05`; il task history `doc/TASK_HISTORY/2026-11-05_forma_isotropia_corona.md`, 1.1 e 4.1)*
    python csv/solitone/carta_forma.py > doc/referti_l2/forma_solitone.txt
### **Solo lettura delle mappe leggere nel repo** *(`doc/referti_l2/campo_TB3/mappe_leggere.npz`, `F3` col bordo; `doc/referti_l2/campo_TM1000/mappe_leggere.npz`, **`F0`**, il toro chiuso; `float16`)*.
### **La misura:** per ogni mappa `R(theta)` in `N_SET` settori, il raggio massimo dei nodi con `rho >= soglia` attorno al centro periodico *(l'immagine minima fra le `9`)*, entro la meta' del periodo;
`c_n` = la media sui settori di `R e^{-i n theta}`; l'esagonalita' `|c6| / c0`, l'ovalita' `|c2| / c0`, `|c1| / c0` *(il centro della forma contro il centro periodico)*, i vertici `arg(c6) / 6`. Le `SOGLIE`
contro il mare *(la mediana di `rho` oltre `R_MARE`)*: una soglia sotto il mare non conta. Lo spessore del bordo: la media sui settori di `R(rho >= 1) - R(rho >= 300)`. **La corona:** gli anelli di `2` nodi
da `16` a `34` *(oltre `35` toccano i lati del rombo: esclusi)*, le armoniche `1 .. 12` della densita' pesata con `rho` e di `log10 rho`, la parte coerente nel tempo dei sei lobi, le chiazze in decadi.
### **I DEVE** *(Luca `2026-11-05`)*: `FX0` l'esagono sintetico *(`rho 1000` dentro un esagono regolare di circumraggio `18`, i vertici a `0`, `15`, `30` gradi)*: l'esagonalita' entro il `20%` del continuo
*(`2.3%`-`3.5%`)* e i vertici entro `5` gradi; `FX1` il disco di raggio `18`: l'esagonalita' sotto `1%`; `FX1-F` *(deve fallire)* lo stesso disco col centro sbagliato di `3` nodi: `|c1| / c0` sotto `1%`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

N_SET = 36                     # ### Luca: 36 settori
SOGLIE = (1.0, 10.0, 100.0, 300.0)   # ### Luca
R_MARE = 25.0                  # ### Luca: il mare, la mediana di rho oltre 25 nodi
ANELLI = tuple((a, a + 2.0) for a in range(16, 34, 2))   # ### Luca: anelli di 2 nodi da 16 a 34
N_ARM = 12                     # ### Luca: le armoniche da 1 a 12
T_DA = 7000.0                  # ### Luca: «dopo t 7000» (la misura preliminare)
CONTINUO = 0.0291              # ### diag_fx_attese.txt: l'esagonalita' dell'esagono regolare nel continuo
FX0_BANDA = (0.023, 0.035)     # ### Luca 2026-11-05: entro il 20% del continuo
FX0_VERT = 5.0                 # ### Luca 2026-11-05: i vertici entro 5 gradi
FX1_TETTO = 0.01               # ### Luca 2026-11-05
FX1F_TETTO = 0.01              # ### Luca 2026-11-05: |c1| / c0
R_SINT = 18.0                  # ### Luca: il raggio dei sintetici
SPOST_F = 3.0                  # ### Luca: il centro sbagliato di 3 nodi
DIR_REF = os.path.join(solitone.RADICE, "doc", "referti_l2")
CORSE = (("TB3", "campo_TB3", "F3, col bordo (g_max 0.03, R_A 28)"), ("TM1000", "campo_TM1000", "F0, il toro chiuso"))

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def posizioni(m1, m2, A1, A2):
    return m1[:, None] * A1 + m2[:, None] * A2


def spost(P, c, L, A1, A2):
    """### **Lo spostamento di ogni nodo dal punto `c` (cartesiano), l'immagine minima fra le `9`:** `(r, theta)`."""
    best = None
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            d = P + a * L * A1 + b * L * A2 - c
            if best is None:
                best = d.copy()
            else:
                piu = np.hypot(d[:, 0], d[:, 1]) < np.hypot(best[:, 0], best[:, 1])
                best[piu] = d[piu]
    return np.hypot(best[:, 0], best[:, 1]), np.mod(np.arctan2(best[:, 1], best[:, 0]), 2 * np.pi)


def forma(rho, r, th, soglia, Rmax):
    """### **`R(theta)` e le sue armoniche** *(i vertici a `-arg(c6) / 6`: `c6 = media R e^{-i 6 theta}` va come `e^{-i 6 theta_v}` se `R` ha il massimo a `theta_v`; il segno corretto il `2026-11-05`, trovato da `FX0` a `15` gradi)*: `{"esag", "oval", "c1", "vert", "R0", "R"}`; `None` se nessun nodo supera la soglia."""
    j = np.minimum((th / (2 * np.pi / N_SET)).astype(int), N_SET - 1)
    R = np.zeros(N_SET)
    sel = (rho >= soglia) & (r <= Rmax)
    if not sel.any():
        return None
    np.maximum.at(R, j[sel], r[sel])
    tj = (np.arange(N_SET) + 0.5) * 2 * np.pi / N_SET
    c = {n: np.mean(R * np.exp(-1j * n * tj)) for n in (0, 1, 2, 6)}
    c0 = abs(c[0])
    return {"esag": abs(c[6]) / c0, "oval": abs(c[2]) / c0, "c1": abs(c[1]) / c0, "vert": -math.degrees(np.angle(c[6])) / 6.0, "R0": float(np.real(c[0])), "R": R}


def ang(a, b, per=60.0):
    """la distanza fra due angoli modulo `per`"""
    d = (a - b) % per
    return min(d, per - d)


def corona(rho, r, th):
    """### **Per ogni anello:** le armoniche della densita' pesata `|somma rho e^{-i n th}| / somma rho` *(complesse, per la parte coerente)*, l'ampiezza dei lobi di `log10 rho` in decadi
    *(`2 |media (log10 rho) e^{-i n th}|`)*, le chiazze *(la deviazione standard di `log10 rho` meno la media dell'anello)*, i nodi a `rho = 0` *(esclusi dal logaritmo)*."""
    out = []
    nn = np.arange(1, N_ARM + 1)
    for a, b in ANELLI:
        sel = (r >= a) & (r < b)
        x, t = rho[sel], th[sel]
        w = np.exp(-1j * np.outer(nn, t))
        cw = (w @ x) / x.sum()
        pos = x > 0
        lg = np.log10(x[pos])
        cl = 2.0 * np.abs((w[:, pos] @ (lg - lg.mean())) / pos.sum())
        out.append({"cw": cw, "cl": cl, "chiazze": float(lg.std()), "zeri": int((~pos).sum()), "nodi": int(sel.sum())})
    return out


def main(argv):
    del argv
    import _presidio
    from solitone import toro as TO
    for m in ("__init__", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    A1, A2 = TO.vettori()
    print("=" * 130)
    print("LA FORMA DEL SOLITONE (Luca 2026-11-04 20:18-22:26; i criteri FX di Luca 2026-11-05): N_SET %d SOGLIE %s R_MARE %g ANELLI %g .. %g (di 2) N_ARM %d T_DA %g"
          % (N_SET, SOGLIE, R_MARE, ANELLI[0][0], ANELLI[-1][1], N_ARM, T_DA))
    print("  ### TB3 e' F3 col bordo; TM1000 e' F0, il toro chiuso: il confronto mescola il vuoto e il bordo, e un run per tipo")
    print("  il rumore della misura: la deviazione standard di mappa in mappa accanto a ogni media; ### nessuna differenza si legge sotto due deviazioni standard (Luca)")
    print("=" * 130)
    # ------------------------------------------------------------------ i sintetici, con le stesse funzioni
    L = 81
    m1, m2 = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    P = posizioni(m1.ravel(), m2.ravel(), A1, A2)
    C0 = 40 * A1 + 40 * A2
    r, th = spost(P, C0, L, A1, A2)
    Rmax = TO.meta_periodo(L)
    for vert in (0.0, 15.0, 30.0):
        phf = np.mod(th - math.radians(vert), math.pi / 3) - math.pi / 6
        rho = np.where(r * np.cos(phf) <= R_SINT * math.cos(math.pi / 6), 1000.0, 0.0)
        f = forma(rho, r, th, 300.0, Rmax)
        esito("DEVE PASSARE: FX0 l'esagono sintetico (circumraggio %g, i vertici a %g gradi): l'esagonalita' in %s e i vertici entro %g gradi" % (R_SINT, vert, FX0_BANDA, FX0_VERT),
              FX0_BANDA[0] <= f["esag"] <= FX0_BANDA[1] and ang(f["vert"], vert) <= FX0_VERT, "esagonalita' %.4f (il continuo %.4f), i vertici a %+.2f gradi" % (f["esag"], CONTINUO, f["vert"]))
    rho = np.where(r <= R_SINT, 1000.0, 0.0)
    f = forma(rho, r, th, 300.0, Rmax)
    esito("DEVE PASSARE: FX1 il disco sintetico di raggio %g: l'esagonalita' sotto %g" % (R_SINT, FX1_TETTO), f["esag"] < FX1_TETTO, "%.4f (|c1|/c0 %.4f, ovalita' %.4f)" % (f["esag"], f["c1"], f["oval"]))
    r2, th2 = spost(P, C0 + SPOST_F * A1, L, A1, A2)
    f2 = forma(rho, r2, th2, 300.0, Rmax)
    esito("DEVE FALLIRE: FX1-F lo stesso disco col centro sbagliato di %g nodi lungo A1: |c1|/c0 sotto %g" % (SPOST_F, FX1F_TETTO), not f2["c1"] < FX1F_TETTO,
          "|c1|/c0 %.4f (atteso ~8.6%%, diag_fx_attese.txt); l'ovalita' %.4f" % (f2["c1"], f2["oval"]))
    # ------------------------------------------------------------------ le mappe vere
    serie = {}
    for nome, cart, desc in CORSE:
        with np.load(os.path.join(DIR_REF, cart, "mappe_leggere.npz")) as d:
            T, RH, CE, d1, d2, Lm = d["tempo"].astype(float), d["rho"], d["centro"].astype(float), d["d1"], d["d2"], int(d["L"])
        assert Lm == L
        Pm = posizioni(d1.astype(int) + L // 2, d2.astype(int) + L // 2, A1, A2)
        righe = []
        for i in range(len(T)):
            rho = RH[i].astype(np.float64)
            c = CE[i, 0] * A1 + CE[i, 1] * A2
            r, th = spost(Pm, c, L, A1, A2)
            mare = float(np.median(rho[(r > R_MARE) & (r <= Rmax)]))
            ff = {sg: forma(rho, r, th, sg, Rmax) for sg in SOGLIE}
            sp = None
            if ff[1.0] is not None and ff[300.0] is not None and 1.0 > mare:
                sp = float(np.mean(ff[1.0]["R"] - ff[300.0]["R"]))
            righe.append({"t": float(T[i]), "mare": mare, "f": ff, "spess": sp, "cor": corona(rho, r, th)})
        serie[nome] = righe
        print("-" * 130)
        print("### %s (%s): %d mappe, t %.0f .. %.0f; per ogni mappa: il mare; per soglia l'esagonalita', l'ovalita', |c1|/c0, i vertici (gradi, mod 60); * = la soglia sotto il mare (non conta)"
              % (nome, desc, len(righe), righe[0]["t"], righe[-1]["t"]))
        print("  %8s %9s  %s  %8s" % ("t", "mare", "  ".join("%-31s" % ("soglia %g: es/ov/c1/vert" % sg) for sg in SOGLIE), "spessore"))
        for x in righe:
            cel = []
            for sg in SOGLIE:
                f = x["f"][sg]
                if f is None:
                    cel.append("%-31s" % "-")
                else:
                    cel.append("%s%.4f %.4f %.4f %+6.1f    " % ("*" if sg <= x["mare"] else " ", f["esag"], f["oval"], f["c1"], f["vert"]))
            print("  %8.0f %9.3e  %s  %8s" % (x["t"], x["mare"], "  ".join(cel), "-" if x["spess"] is None else "%.2f" % x["spess"]))
    # ------------------------------------------------------------------ le medie e il confronto
    print("-" * 130)
    fine_c = min(serie["TB3"][-1]["t"], serie["TM1000"][-1]["t"])
    finestre = (("TB3", T_DA, serie["TB3"][-1]["t"]), ("TB3", T_DA, fine_c), ("TM1000", T_DA, fine_c))
    print("### LE MEDIE (mappa per mappa, +- la deviazione standard), solo le mappe con la soglia sopra il mare; t da %g" % T_DA)
    med = {}
    for nome, a, b in finestre:
        xs = [x for x in serie[nome] if a <= x["t"] <= b]
        for sg in SOGLIE:
            v = [x["f"][sg] for x in xs if x["f"][sg] is not None and sg > x["mare"]]
            if not v:
                print("  %-7s t %5.0f .. %5.0f soglia %5g: nessuna mappa valida (sotto il mare in %d su %d)" % (nome, a, b, sg, len(xs), len(xs)))
                continue
            e = np.array([f["esag"] for f in v])
            o = np.array([f["oval"] for f in v])
            c1 = np.array([f["c1"] for f in v])
            vt = np.array([f["vert"] for f in v])
            med[(nome, a, b, sg)] = (e.mean(), e.std(), len(v))
            print("  %-7s t %5.0f .. %5.0f soglia %5g: %3d mappe; esagonalita' %.4f +- %.4f; ovalita' %.4f +- %.4f (max %.4f); |c1|/c0 %.4f +- %.4f (max %.4f); i vertici %+.1f +- %.1f gradi"
                  % (nome, a, b, sg, len(v), e.mean(), e.std(), o.mean(), o.std(), o.max(), c1.mean(), c1.std(), c1.max(), vt.mean(), vt.std()))
        sps = [x["spess"] for x in xs if x["spess"] is not None]
        print("  %-7s t %5.0f .. %5.0f lo spessore del bordo (R(rho>=1) - R(rho>=300)): %s" % (nome, a, b, ("%.2f +- %.2f nodi (%d mappe)" % (np.mean(sps), np.std(sps), len(sps))) if sps else "nessuna mappa valida (rho 1 sotto il mare)"))
    print("  ### IL CONFRONTO TB3 - TM1000 a tempi uguali (t %g .. %g), per soglia: la differenza delle medie contro due deviazioni standard (la piu' grande delle due)" % (T_DA, fine_c))
    for sg in SOGLIE:
        a, b = med.get(("TB3", T_DA, fine_c, sg)), med.get(("TM1000", T_DA, fine_c, sg))
        if a is None or b is None:
            print("    soglia %5g: non confrontabile (una delle due senza mappe valide)" % sg)
            continue
        dd, ss = a[0] - b[0], 2.0 * max(a[1], b[1])
        print("    soglia %5g: %+.4f contro 2 sigma %.4f: %s" % (sg, dd, ss, "SI LEGGE" if abs(dd) > ss else "non si legge (sotto due deviazioni standard)"))
    # ------------------------------------------------------------------ la corona
    print("-" * 130)
    print("### LA CORONA, t da %g (TB3 fino a %g, TM1000 fino a %g): per anello, media sulle mappe; i sei lobi della densita' pesata |c6| (media dei moduli), la parte coerente |media c6| / media |c6| e la"
          % (T_DA, serie["TB3"][-1]["t"], serie["TM1000"][-1]["t"]))
    print("  fase dei vertici -arg(media c6) / 6; i lobi di log10 rho in decadi (n = 6) e le chiazze (la deviazione standard di log10 rho); il massimo delle armoniche 1..12 pesate (quale n)")
    print("  ### per TB3 gli anelli oltre R_A 28 stanno dentro la fascia del bordo")
    for nome, _c, _d in CORSE:
        xs = [x for x in serie[nome] if x["t"] >= T_DA]
        print("  %s (%d mappe)" % (nome, len(xs)))
        print("    %-9s %7s %10s %9s %9s %11s %9s %13s %6s" % ("anello", "nodi", "|c6| pes.", "coerente", "fase6", "lobi6 dec", "chiazze", "max |c_n|", "zeri"))
        for ia, (a, b) in enumerate(ANELLI):
            cw = np.array([x["cor"][ia]["cw"] for x in xs])
            mod = np.abs(cw).mean(axis=0)
            c6 = cw[:, 5]
            coe = abs(c6.mean()) / np.abs(c6).mean()
            cl6 = np.mean([x["cor"][ia]["cl"][5] for x in xs])
            ch = np.mean([x["cor"][ia]["chiazze"] for x in xs])
            nmax = int(np.argmax(mod)) + 1
            zeri = sum(x["cor"][ia]["zeri"] for x in xs)
            print("    %4g-%-4g %7d %10.4f %9.3f %+9.1f %11.3f %9.3f %8.4f (n %2d) %6d" % (a, b, xs[0]["cor"][ia]["nodi"], np.abs(c6).mean(), coe, -math.degrees(np.angle(c6.mean())) / 6.0, cl6, ch,
                                                                                 mod[nmax - 1], nmax, zeri))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
