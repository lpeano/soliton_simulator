# -*- coding: utf-8 -*-
r"""**IL «CALORE» COME FLUSSO USCENTE DI ENERGIA** *(Luca `2026-11-17` `14:27`, parte 3; la carta e le previsioni `doc/TASK_HISTORY/2026-11-17_flusso_uscente.md`, `831e8d52`; SOLO LETTURE e COPIE)*.

    E:\python\py3132\python.exe doc/referti_l2/flusso_uscente.py --confine <R> > doc/referti_l2/flusso_uscente.txt

**LA DEFINIZIONE** *(scritta prima)*: **`J[a]` = `energia.corrente(st, mot, par, None)`** *(l'energia che lo spostamento della MATERIA porta sull'arco `a`, positiva da `ii` a `jj`)*; **il flusso uscente attraverso l'anello `R`** *(attorno al baricentro della materia)*: **sugli archi con un capo dentro `R` e l'altro fuori, `J` col segno del verso USCENTE; SOLO LA PARTE POSITIVA** *(il mandato)*; accanto il netto.
**3.1 IL CASO NOTO** *(Q-A4, sulla dinamica vera)*: **due pacchetti a `15` nodi da un punto, con un gradiente di fase radiale `+k` e `-k`** *(lo spinore del mattone, una gaussiana di larghezza `6`)*, la scena S162, `5` tick: **lo spostamento radiale misurato della loro materia** e **il flusso uscente attraverso l'anello `15`** **devono avere lo STESSO segno, e i due pacchetti segni OPPOSTI.**
**3.2** il flusso attraverso gli anelli `15`, `20`, `30`, `45` negli stati della corsa su `L 186` *(la fase `0`: `k 950, 1000, 1950, 2000, 2950, 3000`)*; **la massa assorbita dal bordo per tick** *(dalle coppie `950`/`1000`, `1950`/`2000`, `2950`/`3000`)*; **il vuoto F3 puro** *(`psi = 0`: `J = 0` PER COSTRUZIONE -- un falso zero, dichiarato)*.
**3.3 L'ACCUMULO** *(fuori dal confine `--confine`, dalla parte 2)*: per arco, l'integrale del flusso uscente positivo fra i sei istanti *(il trapezio: un'APPROSSIMAZIONE, dichiarata)*; **il costo di una nascita** per anello *(la divisione generica di `nascita_dentro_fuori.py` sullo stato di `L 186` a `k 3000`, un arco ogni `5` anelli dal confine a `60`)*; **dove e quando l'accumulato copre il costo; le nascite per tick; i nodi in `10000` tick** *(al ritmo medio)*; **il costo di calcolo** *(una `energia.corrente` per tick, misurata)*.
**3.4** il flusso a `k 3000` contro `k 950`/`1000`. **3.5** Q1-Q3 accanto *(dove stanno: `soglia_nascita.txt`)*.
"""
import argparse
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
_PO = os.path.join(_RADICE, "primo_ordine")
for _p in (_QUI, _SOL, _CSV, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ANELLI = (15, 20, 30, 45)
KS = (950, 1000, 1950, 2000, 2950, 3000)


def flusso(J, ii, jj, r, R):
    """### `(positivo, netto, quanti)`: il flusso uscente attraverso l'anello `R` (`r` la distanza dei nodi dal centro)."""
    dentro_i, dentro_j = r[ii] < R, r[jj] < R
    x = np.where(dentro_i & ~dentro_j, J, 0.0) + np.where(~dentro_i & dentro_j, -J, 0.0)
    s = dentro_i != dentro_j
    return float(np.sum(np.clip(x[s], 0.0, None))), float(np.sum(x[s])), int(s.sum())


def main(argv):
    import _presidio
    import _u1_prototipo as U1
    import energia as EN
    import mattone as MT
    import convergenza as CV
    import prova_scatola5 as PS
    import _massa_nei_difetti as MD
    import nascita_dentro_fuori as ND
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_SOL, "prova_scatola5.py"))
    _presidio.avvia(os.path.join(_QUI, "nascita_dentro_fuori.py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--confine", type=float, required=True, help="il confine dalla parte 2 (nodi): la materia sotto l'1%%")
    x = ap.parse_args(argv)
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("IL CALORE COME FLUSSO USCENTE DI ENERGIA (Luca 2026-11-17 14:27, parte 3); il confine dalla parte 2: %.2f nodi" % x.confine)
    print("=" * 130)
    esiti = []
    # ---------------------------------------------------------------- 3.1 il caso noto
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        mot = Z["mot"]
        ii, jj = np.asarray(mot.inc.ii), np.asarray(mot.inc.jj)
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
            X0 = {k: d[k].copy() for k in Z["chiavi"]}
        psin = X0["psi_h"][Z["righe"]].reshape(n, -1)
        jm = int(np.argmax(np.sum(np.abs(psin) ** 2, axis=1)))
        u = (psin[jm] / np.linalg.norm(psin[jm])).reshape(Z["righe"].shape[1], -1)
        C = (81.0, 81.0)
        D = TO.scarti(m1, m2, C[0], C[1], L)
        r = np.hypot(D[:, 0], D[:, 1])
        print("### 3.1 IL CASO NOTO: due pacchetti a 15 nodi dal punto %s, il gradiente di fase radiale +k e -k (k 0.6), la scena S162, 5 tick" % (C,))
        segni = {}
        for s in (+1, -1):
            g = np.exp(-(np.hypot(D[:, 0] - 15.0, D[:, 1]) / 6.0) ** 2) * np.exp(1j * s * 0.6 * D[:, 0])
            st0 = {k: a.copy() for k, a in X0.items()}
            st0["psi_h"] = np.zeros_like(X0["psi_h"])
            st0["psi_h"][Z["righe"]] = 30.0 * g[:, None, None] * u[None, :, :]
            Z["metti"](st0)
            Cx = MT.Campi(Z, "MGU", rho_c, e)
            U1.scrivi_U(mot, Cx.campo)
            J = np.asarray(EN.corrente(Z["st"], mot, Z["par"], None), dtype=float)
            fp, fn, nq = flusso(J, ii, jj, r, 15.0)
            rho0 = np.sum(np.abs(Z["st"]["psi_h"][Z["righe"]].reshape(n, -1)) ** 2, axis=1)
            r0 = float(np.sum(rho0 * r) / np.sum(rho0))
            for k in range(1, 6):
                Cx.tick(k, MT.T_162 + k, 1.0, e)
            rho5 = np.sum(np.abs(Z["st"]["psi_h"][Z["righe"]].reshape(n, -1)) ** 2, axis=1)
            r5 = float(np.sum(rho5 * r) / np.sum(rho5))
            segni[s] = (fn, r5 - r0)
            print("    +k" if s > 0 else "    -k", end="")
            print(": il flusso uscente a t = 0 attraverso l'anello 15: il positivo %+.6e, il netto %+.6e (%d archi); lo spostamento radiale della materia in 5 tick %+.6e nodi" % (fp, fn, nq, r5 - r0))
        Z["metti"]()
    ok_s = all((segni[s][0] > 0) == (segni[s][1] > 0) for s in segni) and (segni[1][0] > 0) != (segni[-1][0] > 0)
    esiti.append(("3.1 il caso noto: il segno del flusso netto = il segno dello spostamento, e i due pacchetti opposti", ok_s))
    # ---------------------------------------------------------------- 3.2, 3.4
    print("-" * 130)
    print("### 3.2 IL FLUSSO NEGLI STATI DELLA CORSA SU L 186 (la fase 0): gli anelli %s; il positivo e il netto" % (ANELLI,))
    serie = {}
    mass = {}
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        L6, n6 = Z["L"], Z["n"]
        mot = Z["mot"]
        ii6, jj6 = np.asarray(mot.inc.ii), np.asarray(mot.inc.jj)
        v6 = np.arange(n6)
        q1, q2 = (v6 // L6).astype(float), (v6 % L6).astype(float)
        t_cor = []
        for k in KS:
            f = os.path.join(MT.DIR_E, "scatola5_L186_%05d.npz" % k)
            Cx, meta, _cs = PS.carica(Z, f, rho_c, e)
            U1.scrivi_U(mot, Cx.campo)
            rho6 = np.sum(np.abs(Z["st"]["psi_h"][Z["righe"]].reshape(n6, -1)) ** 2, axis=1)
            cb = TO.centro(rho6, q1, q2, L6)[:2]
            r6 = np.hypot(*TO.scarti(q1, q2, cb[0], cb[1], L6).T[:2])
            t1 = time.time()
            J = np.asarray(EN.corrente(Z["st"], mot, Z["par"], None), dtype=float).copy()
            t_cor.append(time.time() - t1)
            serie[k] = {R: flusso(J, ii6, jj6, r6, R) for R in ANELLI}
            serie[k]["J"] = J
            serie[k]["r"] = r6
            mass[k] = float(rho6.sum())
            print("    k %4d (il baricentro (%.2f, %.2f), la massa %.10e): %s" % (k, cb[0], cb[1], mass[k], "  ".join("R %d: + %.4e netto %+.4e" % (R, serie[k][R][0], serie[k][R][1]) for R in ANELLI)))
            sys.stdout.flush()
        print("    la massa assorbita dal bordo per tick: %s" % "; ".join("k %d-%d %.4e" % (a, b, (mass[a] - mass[b]) / (b - a)) for a, b in ((950, 1000), (1950, 2000), (2950, 3000))))
        print("    il vuoto F3 puro: J = 0 PER COSTRUZIONE (psi = 0: la corrente e' della materia) -- un falso zero, dichiarato nella carta")
        print("### 3.4 SI ESAURISCE? il flusso positivo a k 3000 contro k 950: %s" % "  ".join("R %d: %.3f" % (R, serie[3000][R][0] / serie[950][R][0]) if serie[950][R][0] > 0 else "R %d: -" % R for R in ANELLI))
        # ---------------------------------------------------------------- 3.3 l'accumulo e il costo
        print("-" * 130)
        Jp = {k: None for k in KS}
        for k in KS:
            r6 = serie[k]["r"]
            dentro_i = r6[ii6] < r6[jj6]
            Jout = np.where(dentro_i, serie[k]["J"], -serie[k]["J"])     # il verso uscente: da quello piu' vicino al centro a quello piu' lontano
            Jp[k] = np.clip(Jout, 0.0, None)
        acc = np.zeros(len(ii6))
        for a_, b_ in zip(KS[:-1], KS[1:]):
            acc += 0.5 * (Jp[a_] + Jp[b_]) * (b_ - a_)
        r_arco = 0.5 * (serie[3000]["r"][ii6] + serie[3000]["r"][jj6])
        fuori = r_arco >= x.confine
        rate = acc / (KS[-1] - KS[0])
        # il costo di una nascita per anello sullo stato a k 3000 (la divisione generica)
        G6 = (ii6, jj6, n6, np.asarray(MD.toro(L6)[3], dtype=float))
        st3 = {k: Z["st"][k].copy() for k in ("psi_h", "phi_h")}
        D6 = TO.scarti(q1, q2, cb[0], cb[1], L6)
        th6 = np.arctan2(D6[:, 1], D6[:, 0])
        costi = []
        for R in range(int(math.ceil(x.confine)), 61, 5):
            rm = np.hypot(D6[:, 0] + 0.5, D6[:, 1])
            i0 = int(np.argmin(np.abs(rm - R) + 10.0 * np.abs(th6)))
            Dl = ND.una_semplice(G6, st3["psi_h"], st3["phi_h"], 3 * i0) if hasattr(ND, "una_semplice") else None
            if Dl is None:
                F0 = ND.famiglie(G6, st3["psi_h"], st3["phi_h"])
                out = ND.nasci(G6, st3["psi_h"], st3["phi_h"], 3 * i0)
                ph = ND.v4f3(G6, st3["phi_h"], out[0], out[2], out[3]["n"])
                Dl = ND.delta(F0, ND.famiglie(out[0], out[1], ph))
            costi.append((R, float(rm[i0]), Dl["tot"]))
            print("    il costo di una nascita all'anello %2d (%.2f nodi): %s" % (R, rm[i0], ND.riga(Dl)))
            sys.stdout.flush()
        Z["metti"]()
    print("### 3.3 L'ACCUMULO fuori dal confine (%.2f nodi), il flusso uscente positivo per arco integrato da k %d a %d (il trapezio sui sei istanti):" % (x.confine, KS[0], KS[-1]))
    cR = np.array([c_[1] for c_ in costi])
    cV = np.array([c_[2] for c_ in costi])
    costo_a = np.interp(r_arco, cR, cV)
    pos = fuori & (costo_a > 0)
    print("    gli archi fuori dal confine: %d; col costo positivo: %d; il costo fra %.3e e %.3e" % (int(fuori.sum()), int(pos.sum()), float(cV.min()), float(cV.max())))
    if pos.any():
        tnasc = np.where(rate[pos] > 0, costo_a[pos] / np.where(rate[pos] > 0, rate[pos], 1.0), np.inf)
        j = int(np.argmin(tnasc))
        print("    il primo arco a nascere: a %.2f nodi, dopo %.4e tick (il ritmo %.4e per tick contro il costo %.4e)" % (float(r_arco[pos][j]), float(tnasc[j]), float(rate[pos][j]), float(costo_a[pos][j])))
        nasc = float(np.sum(np.where(np.isfinite(tnasc), 10000.0 / tnasc, 0.0)))
        print("    le nascite in 10000 tick al ritmo medio: %.4e (per tick %.4e: %s)" % (nasc, nasc / 10000.0, "oltre 1, D-M4 le limita a 1 per tick" if nasc > 10000 else "sotto 1 per tick"))
        print("    gli archi che coprono il costo entro 2050 tick (l'accumulato vero fra i sei istanti): %d" % int(np.sum(acc[pos] >= costo_a[pos])))
    print("    il costo di calcolo (Q-P1): una energia.corrente %.3f s (la mediana su sei), l'accumulo O(m) = %d archi per tick" % (float(np.median(t_cor)), len(ii6)))
    print("-" * 130)
    print("### 3.5 Q1-Q3 accanto (soglia_nascita.txt, il mattone su L 162): i massimi a 14.85 (Q1), 20.54 (Q2), 9.21 (Q3) nodi; il flusso uscente: vedi 3.2")
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("    (il tempo %.0f s)" % (time.time() - t00))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
