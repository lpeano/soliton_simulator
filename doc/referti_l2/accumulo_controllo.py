# -*- coding: utf-8 -*-
r"""**IL CONTROLLO DELL'ACCUMULO: IL FLUSSO NETTO CHE ESCE PER TICK, CONTRO LE NASCITE CONTATE ARCO PER ARCO** *(Luca `2026-11-17` `16:02`, S1; la carta della mitosi sez. `12`)*.

    E:\python\py3132\python.exe doc/referti_l2/accumulo_controllo.py > doc/referti_l2/accumulo_controllo.txt

**Il difetto da misurare** *(il guardiano)*: l'accumulo di `flusso_uscente.py` *(3.3)* somma il flusso che ATTRAVERSA ogni arco: la stessa energia, uscendo, attraversa molti archi in fila e si conta molte volte.
**Il controllo:** **l'energia che esce per tick attraverso l'ANELLO** *(il confine `23.81`, e `30`, `45`; `flusso_uscente.flusso`: il NETTO e la parte positiva)* **negli stessi sei stati della fase `0` su `L 186`**; **diviso per il costo medio di una nascita fuori dal confine** *(letto da `flusso_uscente.txt`, le righe «il costo di una nascita»)* = **il massimo di nascite pagabili per tick**; contro **le `0.50` per tick** del referto *(letto)*. **La riserva sul netto in `2050` tick** *(il trapezio sui sei istanti: un'approssimazione, dichiarata)* **e quante nascite paga.**
"""
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_QUI, _SOL, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ANELLI = (23.81, 30.0, 45.0)
KS = (950, 1000, 1950, 2000, 2950, 3000)


def main():
    import _presidio
    import _u1_prototipo as U1
    import energia as EN
    import mattone as MT
    import convergenza as CV
    import prova_scatola5 as PS
    import flusso_uscente as FU
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "flusso_uscente.py"))
    _presidio.avvia(__file__)
    testo = open(os.path.join(_QUI, "flusso_uscente.txt"), encoding="utf-8").read()
    costi = [float(x) for x in re.findall(r"il costo di una nascita all'anello\s+\d+ \([\d.]+ nodi\): dH ([+-][\d.e+-]+)", testo)]
    ritmo = float(re.search(r"le nascite in 10000 tick al ritmo medio: ([\d.e+-]+) \(per tick ([\d.e+-]+)", testo).group(2))
    cm, cs = float(np.mean(costi)), float(np.std(costi))
    print("=" * 130)
    print("IL CONTROLLO DELL'ACCUMULO (Luca 2026-11-17 16:02, S1)")
    print("=" * 130)
    print("### da flusso_uscente.txt: i costi delle nascite fuori dal confine %s -> la media %.4f, la deviazione standard %.4f (%d valori); le nascite per tick dell'accumulo arco per arco %.4e" % (
        ", ".join("%.3f" % c for c in costi), cm, cs, len(costi), ritmo))
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    F = {R: [] for R in ANELLI}
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        L6, n6 = Z["L"], Z["n"]
        mot = Z["mot"]
        ii6, jj6 = np.asarray(mot.inc.ii), np.asarray(mot.inc.jj)
        v6 = np.arange(n6)
        q1, q2 = (v6 // L6).astype(float), (v6 % L6).astype(float)
        for k in KS:
            Cx, _meta, _cs = PS.carica(Z, os.path.join(MT.DIR_E, "scatola5_L186_%05d.npz" % k), rho_c, e)
            U1.scrivi_U(mot, Cx.campo)
            rho6 = np.sum(np.abs(Z["st"]["psi_h"][Z["righe"]].reshape(n6, -1)) ** 2, axis=1)
            cb = TO.centro(rho6, q1, q2, L6)[:2]
            r6 = np.hypot(*TO.scarti(q1, q2, cb[0], cb[1], L6).T[:2])
            J = np.asarray(EN.corrente(Z["st"], mot, Z["par"], None), dtype=float).copy()
            for R in ANELLI:
                p, nt, nq = FU.flusso(J, ii6, jj6, r6, R)
                F[R].append((p, nt))
            print("    k %4d: %s" % (k, "  ".join("R %.2f: + %.4e netto %+.4e" % (R, F[R][-1][0], F[R][-1][1]) for R in ANELLI)))
        Z["metti"]()
    print("-" * 130)
    for R in ANELLI:
        net = np.array([x[1] for x in F[R]])
        pos = np.array([x[0] for x in F[R]])
        integ = float(np.sum([0.5 * (net[q] + net[q + 1]) * (KS[q + 1] - KS[q]) for q in range(len(KS) - 1)]))
        mx = float(net.mean()) / cm
        print("### l'anello %.2f: il netto per tick la media %+.4e (la deviazione standard %.4e su %d istanti; da %+.4e a %+.4e); il positivo la media %.4e" % (
            R, float(net.mean()), float(net.std()), len(net), float(net.min()), float(net.max()), float(pos.mean())))
        print("    il massimo di nascite pagabili dal NETTO: %.4e per tick (+- %.1e dalla dispersione del netto); contro %.4e dell'accumulo arco per arco: il fattore %.1f" % (
            mx, float(net.std()) / cm, ritmo, ritmo / mx if mx > 0 else float("inf")))
        print("    la riserva sul netto da k %d a k %d (il trapezio sui sei istanti): %+.4e; le nascite che paga al costo medio: %.2f" % (KS[0], KS[-1], integ, integ / cm))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
