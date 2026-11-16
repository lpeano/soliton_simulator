# -*- coding: utf-8 -*-
r"""**L'ALONE DEL VUOTO DEL MATTONE** *(Luca `2026-11-16` `02:38`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24.31`; SOLO LETTURA)*.

    E:\python\py3132\python.exe csv/solitone/porto_alone.py > doc/referti_l2/mattone/porto_alone_vuoto.txt     (PYTHONNOUSERSITE=1, TMP su E:)

**(O) un'onda che si allontana o (P) il profilo che si assesta?** **Il profilo radiale di `|phi - phi0|`** *(il codice di `porto.dphi_nodi` e `porto.r_ogg`: attorno al baricentro di `rho`, la media per anello di `1` nodo)*
**e di `vuo`** *(l'energia del vuoto per nodo, `_libro_dei_conti.conti_per_nodo`)*: **su `L 324` a `k 0`** *(ricostruito come la cottura: il vuoto fresco, il mattone incollato; NESSUN tick)*, **`950`, `1000`;
su `L 162`** *(`L162_MGU_00500` ... `_03000`)*; **su `L 243`** *(`conv_GU_L243_02000`, il mattone di `L 162` incollato su `L 243`)*. **I raggi del `10%`, `5%`, `2%`, `1%`** *(la regola di `r_ogg`: il primo anello oltre il massimo
da cui il profilo resta sotto la soglia fino a meta' periodo)*. **Le velocita' dei tratti; il fronte** *(il massimo di `profilo(1000) - profilo(0)` oltre il raggio del `10%` di `k 0`)*. **Un'immagine dei profili.**
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import porto as PO  # noqa: E402

SOGLIE = (0.10, 0.05, 0.02, 0.01)
R_MAX = 140
DIR_E = MT.DIR_E


def profilo(Z, t, L):
    """### `(r, media |dphi| per anello, media vuo per anello, il baricentro)`."""
    import _libro_dei_conti as LC
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import toro as TO
    n = Z["n"]
    phi0 = BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
    d = np.sqrt(np.sum(np.abs(Z["st"]["phi_h"] - phi0).reshape(n * 6, -1) ** 2, axis=1))
    dn = np.sqrt(np.sum(d[Z["righe"]] ** 2, axis=1))
    rho = MT.rho_di(Z)
    b = TO.centro(rho, Z["m1"], Z["m2"], L)[:2]
    r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], b[0], b[1], L).T[:2])
    an = np.floor(r).astype(int)
    cnt = np.maximum(np.bincount(an), 1)
    media = np.bincount(an, weights=dn) / cnt
    vuo = np.asarray(LC.conti_per_nodo(Z["z"]["inc"], Z["mot"], Z["st"], Z["e_K"], V.LAM_ZERO, Z["par"])["vuo"], dtype=float)
    mv = np.bincount(an, weights=vuo, minlength=len(media)) / cnt
    return media, mv, b, int(TO.meta_periodo(L))


def raggi(media, meta):
    i_max = int(np.argmax(media[:meta]))
    out = {}
    for s in SOGLIE:
        sotto = media < s * media[i_max]
        out[s] = float("inf")
        for j in range(i_max + 1, meta):
            if sotto[j:meta].all():
                out[s] = float(j)
                break
    return out, i_max


def riga(nome, k, media, mv, b, meta):
    rr, i_max = raggi(media, meta)
    print("  %-8s k %5d: il baricentro (%.2f, %.2f); il massimo di |dphi| %.4e all'anello %d; i raggi: %s; la meta' periodo %d"
          % (nome, k, b[0], b[1], media[i_max], i_max, ", ".join("%g%% %s" % (100 * s, "%.0f" % rr[s]) for s in SOGLIE), meta))
    sys.stdout.flush()
    return rr


def main():
    import _presidio
    import convergenza as CV
    import convergenza_243 as C243
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    print("=" * 130)
    print("L'ALONE DEL VUOTO DEL MATTONE (Luca 02:38): il profilo radiale di |phi - phi0| e di vuo; sys.executable %s" % sys.executable)
    print("=" * 130)
    P = {}
    # ### L 324
    print("### L 324 (il porto): k 0 ricostruito come la cottura (nessun tick), k 950 e 1000 dagli stati")
    with PO.scena() as Z:
        L = PO.L
        MT.vuoto_fresco(Z, t0)
        fr = C243.francobollo_L162("MGU", 0)
        cd = PO.nodo_buono(fr, Z["bordo"]["c0"])
        MT.incolla(Z, fr, cd, True)
        R0, _b = PO.r_ogg(Z, t0)
        print("  il controllo della ricostruzione: R_ogg di porto.r_ogg a k 0 = %.1f (la cottura stampo' 44.0): %s" % (R0, "UGUALE" if R0 == 44.0 else "### DIVERSO: k 0 NON vale"))
        m, mv, b, meta = profilo(Z, t0, L)
        P[("L324", 0)] = (m, mv)
        rr = {0: riga("L 324", 0, m, mv, b, meta)}
        for k in (950, 1000):
            f = os.path.join(DIR_E, "porto_cottura_%05d.npz" % k)
            _C, mt, _cs = PO.carica(Z, f, rho_c, e)
            m, mv, b, meta = profilo(Z, int(mt["t"]), L)
            P[("L324", k)] = (m, mv)
            rr[k] = riga("L 324", k, m, mv, b, meta)
        Z["metti"]()
    print("-" * 130)
    r1755 = 61.0
    v1 = (rr[1000][0.02] - rr[0][0.02]) / 1000.0
    v2 = (r1755 - rr[1000][0.02]) / 755.0
    print("### IL RAGGIO DEL 2%%: k 0 %.0f, k 950 %.0f, k 1000 %.0f, k 1755 %.1f (il numero stampato dalla cottura, nessun profilo)" % (rr[0][0.02], rr[950][0.02], rr[1000][0.02], r1755))
    print("    la velocita' del tratto 0-1000 %.4f nodi/tick; del tratto 1000-1755 %.4f nodi/tick; il rapporto %.2f" % (v1, v2, v2 / v1 if v1 else float("nan")))
    for s in SOGLIE:
        print("    il raggio del %g%%: k 0 %.0f, 950 %.0f, 1000 %.0f; la velocita' 0-1000 %.4f nodi/tick" % (100 * s, rr[0][s], rr[950][s], rr[1000][s], (rr[1000][s] - rr[0][s]) / 1000.0))
    d = P[("L324", 1000)][0] - P[("L324", 0)][0]
    d950 = P[("L324", 950)][0] - P[("L324", 0)][0]
    r10 = int(rr[0][0.10])
    j = r10 + int(np.argmax(d[r10:R_MAX + 1]))
    j9 = r10 + int(np.argmax(d950[r10:R_MAX + 1]))
    print("### IL FRONTE (il massimo di profilo(k) - profilo(0) oltre il raggio del 10%% di k 0, %d): a k 950 all'anello %d (%.4e), a k 1000 all'anello %d (%.4e); lo spostamento in 50 tick %d"
          % (r10, j9, d950[j9], j, d[j], j - j9))
    ok_o = abs(v2 - v1) <= 0.30 * abs(v1) if v1 else False
    ok_p = abs(v2) < 0.5 * abs(v1) if v1 else False
    print("### LA PREVISIONE (sez. 24.31): (O) le due velocita' entro il 30%%: %s; (P) l'ultima sotto la meta' della prima: %s" % (ok_o, ok_p))
    print("=" * 130)
    # ### L 162
    print("### L 162 (il mattone sulla sua scena, la sua cottura)")
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        for k in (500, 1000, 1500, 2000, 2500, 3000):
            f = os.path.join(DIR_E, "L162_MGU_%05d.npz" % k)
            with np.load(f) as dd:
                Z["metti"]({x: dd[x].copy() for x in Z["chiavi"]})
                t = int(json.loads(str(dd["meta"]))["t"])
            m, mv, b, meta = profilo(Z, t, Z["L"])
            P[("L162", k)] = (m, mv)
            riga("L 162", k, m, mv, b, meta)
        Z["metti"]()
    print("### L 243 (conv_GU_L243_02000: il mattone di L 162 incollato su L 243, k 2000)")
    f = os.path.join(DIR_E, "conv_GU_L243_02000.npz")
    with np.load(f) as dd:
        mt = json.loads(str(dd["meta"]))
    print("    i metadati: mondo %s, L %s, k %s, t %s" % (mt.get("mondo"), mt.get("L"), mt.get("k"), mt.get("t")))
    with CV.scena_L(243, PO.R_A_PROVV) as Z:
        with np.load(f) as dd:
            Z["metti"]({x: dd[x].copy() for x in Z["chiavi"]})
        m, mv, b, meta = profilo(Z, int(mt["t"]), 243)
        P[("L243", 2000)] = (m, mv)
        riga("L 243", 2000, m, mv, b, meta)
        Z["metti"]()
    print("=" * 130)
    print("### I PROFILI (la media per anello, anelli 0..%d): |dphi| e vuo, per la forma della coda e per la mitosi (dove vuo per nodo e' piu' alto)" % R_MAX)
    chiavi = sorted(P)
    print("  anello  " + "  ".join("%-22s" % ("%s k%d" % c) for c in chiavi))
    for a in list(range(0, 20, 2)) + list(range(20, R_MAX + 1, 10)):
        print("  %6d  " % a + "  ".join("%10.3e %10.3e " % ((P[c][0][a], P[c][1][a]) if a < len(P[c][0]) else (float("nan"), float("nan"))) for c in chiavi))
    for c in chiavi:
        mv = P[c][1]
        i = int(np.argmax(mv[:R_MAX + 1]))
        print("    %s k%d: vuo per nodo e' massimo all'anello %d (%.4e); al centro %.4e; all'anello 60 %.4e" % (c[0], c[1], i, mv[i], mv[0], mv[60] if len(mv) > 60 else float("nan")))
    np.savez(os.path.join(MT.DIR_REF, "porto_alone_profili.npz"), **{"%s_%05d_dphi" % c: P[c][0] for c in chiavi}, **{"%s_%05d_vuo" % c: P[c][1] for c in chiavi})
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(13, 5))
        for c in chiavi:
            ax[0].semilogy(P[c][0][:R_MAX + 1], label="%s k%d" % c)
            ax[1].plot(P[c][1][:R_MAX + 1], label="%s k%d" % c)
        ax[0].set_xlabel("anello (nodi dal baricentro)")
        ax[0].set_ylabel("media |phi - phi0|")
        ax[1].set_xlabel("anello")
        ax[1].set_ylabel("media vuo per nodo")
        ax[0].legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(os.path.join(MT.DIR_REF, "porto_alone_profili.png"), dpi=110)
        print("### l'immagine: doc/referti_l2/mattone/porto_alone_profili.png")
    except ImportError as x:
        print("### l'immagine NON fatta: %r (i profili sono in porto_alone_profili.npz)" % x)
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
