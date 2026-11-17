# -*- coding: utf-8 -*-
r"""**LE NASCITE SU ARCHI SPARSI: DILUIZIONE LOCALE O UN EFFETTO CHE SI ALLARGA?** *(Luca `2026-11-17` `16:02`, S3; la carta della mitosi sez. `12`; SOLO COPIE dello stato)*.

    E:\python\py3132\python.exe doc/referti_l2/nascite_sparse.py > doc/referti_l2/nascite_sparse.txt

**Lo stato:** la fase `0` su `L 186` a `k 3000` *(`E:/soliton_simulator/mattone/scatola5_L186_03000.npz`)*. **La nascita:** la divisione generica di `nascita_dentro_fuori.py` *(`nasci`, `v4f3`, `famiglie`, `delta`: la stessa)*.
**S3a:** all'anello del confine *(`23.81` nodi)*, **20 archi a `18` gradi l'uno dall'altro attorno al baricentro** *(l'arco del reticolo col punto medio piu' vicino a ciascun punto)*, **in ordine, uno dopo l'altro sullo stato che cresce**; **S3b:** lo stesso all'anello `30`. **Per ogni nascita:** `Delta H` scomposto per termine **in sequenza** e, **accanto, sullo stato VERGINE** *(lo stesso arco senza le nascite prima: separa l'ANGOLO dall'accumulo)*; il rapporto ultima/prima.
**Accanto** *(letta, non rifatta)*: la sequenza «sul nato per ultimo» della sez. `2.3` *(`nascita_dentro_fuori.txt`, l'anello `23.81`, `L 162`)*.
**Il caso noto:** la prima nascita di S3a = `nascita_dentro_fuori.nasci` sullo stesso arco AL BIT *(gli array e `Delta H`)*.
**La riserva** *(`accumulo_controllo.txt`, il netto al confine integrato in `2050` tick)*: **quante nascite in fila paga, nei tre casi.**
"""
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
_PO = os.path.join(_RADICE, "primo_ordine")
for _p in (_QUI, _SOL, _CSV, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

CONFINE = 23.81
N = 20


def main():
    import _presidio
    import _massa_nei_difetti as MD
    import mattone as MT
    import convergenza as CV
    import prova_scatola5 as PS
    import nascita_dentro_fuori as ND
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "nascita_dentro_fuori.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LE NASCITE SU ARCHI SPARSI (Luca 2026-11-17 16:02, S3)")
    print("=" * 130)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        L, n = Z["L"], Z["n"]
        ii, jj, nn, dirs = MD.toro(L)
        assert np.array_equal(np.asarray(Z["mot"].inc.ii), ii) and np.array_equal(np.asarray(Z["mot"].inc.jj), jj), "l'ordine degli archi non e' quello del toro: FERMO"
        PS.carica(Z, os.path.join(MT.DIR_E, "scatola5_L186_03000.npz"), rho_c, e)
        psi0, phi0 = Z["st"]["psi_h"].copy(), Z["st"]["phi_h"].copy()
        Z["metti"]()
    G0 = (ii, jj, nn, np.asarray(dirs, dtype=float))
    v = np.arange(nn)
    m1, m2 = (v // L).astype(float), (v % L).astype(float)
    rho = np.zeros(nn)
    np.add.at(rho, ND.nodo_h(ii, jj), np.abs(psi0[:, 0]) ** 2 + np.abs(psi0[:, 1]) ** 2)
    cb = TO.centro(rho, m1, m2, L)[:2]
    D = TO.scarti(m1, m2, cb[0], cb[1], L)
    de = TO.scarti(m1[jj], m2[jj], m1[ii], m2[ii], L)
    mid = D[ii, :2] + 0.5 * de[:, :2]
    print("### lo stato: L 186, k 3000; il baricentro della materia (%.3f, %.3f)" % (cb[0], cb[1]))
    tabelle = {}
    for nome, R in (("S3a (il confine)", CONFINE), ("S3b (30 nodi)", 30.0)):
        archi = []
        for q in range(N):
            th = math.radians(18.0 * q)
            p = np.array([R * math.cos(th), R * math.sin(th)])
            a = int(np.argmin(np.hypot(mid[:, 0] - p[0], mid[:, 1] - p[1])))
            archi.append((int(ii[a]), int(jj[a]), float(np.hypot(*mid[a]))))
        print("-" * 130)
        print("### %s: 20 archi a 18 gradi, all'anello %.2f" % (nome, R))
        Gc, pc, fc = G0, psi0.copy(), phi0.copy()
        righe = []
        for q, (i0, j0, rr) in enumerate(archi):
            a = int(np.where((Gc[0] == i0) & (Gc[1] == j0))[0][0])
            F0 = ND.famiglie(Gc, pc, fc)
            out = ND.nasci(Gc, pc, fc, a)
            ph = ND.v4f3(Gc, fc, out[0], out[2], out[3]["n"])
            Dl = ND.delta(F0, ND.famiglie(out[0], out[1], ph))
            # lo stato VERGINE: lo stesso arco senza le nascite prima
            a0 = int(np.where((ii == i0) & (jj == j0))[0][0])
            o0 = ND.nasci(G0, psi0, phi0, a0)
            Dv = ND.delta(ND.famiglie(G0, psi0, phi0), ND.famiglie(o0[0], o0[1], ND.v4f3(G0, phi0, o0[0], o0[2], o0[3]["n"])))
            if q == 0 and nome.startswith("S3a"):
                ug = all(np.array_equal(x, y) for x, y in ((out[1], o0[1]), (out[2], o0[2]), (out[0][0], o0[0][0]), (out[0][1], o0[0][1])))
                print("### IL CASO NOTO: la prima nascita di S3a = nasci sullo stesso arco dello stato vergine AL BIT (gli array): %s; Delta H %+.9e contro %+.9e" % (ug, Dl["tot"], Dv["tot"]))
                assert ug and Dl["tot"] == Dv["tot"], "il caso noto non passa: FERMO"
            righe.append((Dl["tot"], Dv["tot"]))
            print("    %2d: l'arco (%d -> %d) a %.2f nodi, %3d gradi: IN SEQUENZA %s | VERGINE dH %+.6e" % (q + 1, i0, j0, rr, 18 * q, ND.riga(Dl), Dv["tot"]))
            sys.stdout.flush()
            Gc, pc, fc = out[0], out[1], ph
        s = np.array([x[0] for x in righe])
        vg = np.array([x[1] for x in righe])
        print("### %s: l'ultima / la prima in sequenza %.4f; la sequenza contro il vergine, arco per arco: la differenza relativa massima %.3e; la dispersione del vergine per angolo: da %+.4f a %+.4f" % (
            nome, s[-1] / s[0], float(np.max(np.abs(s - vg) / np.abs(vg))), float(vg.min()), float(vg.max())))
        tabelle[nome] = s
    # ---------------------------------------------------------------- accanto: 2.3 e la riserva
    t23 = open(os.path.join(_QUI, "nascita_dentro_fuori.txt"), encoding="utf-8").read()
    blocco = t23.split("### 2.3 LE NASCITE IN FILA all'anello 23.81 (U = I)")[1].split("i segni:")[0]
    fila = np.array([float(x) for x in re.findall(r"dH ([+-][\d.e+-]+) =", blocco)])
    tabelle["2.3 (sul nato per ultimo, L 162)"] = fila
    print("-" * 130)
    print("### ACCANTO, la sezione 2.3 (nascita_dentro_fuori.txt, l'anello 23.81, L 162): %d nascite, da %+.4f a %+.4f, l'ultima / la prima %.4f" % (len(fila), fila[0], fila[-1], fila[-1] / fila[0]))
    ta = open(os.path.join(_QUI, "accumulo_controllo.txt"), encoding="utf-8").read()
    ris = float(re.search(r"l'anello 23\.81:.*?la riserva sul netto da k 950 a k 3000 \(il trapezio sui sei istanti\): ([+-][\d.e+-]+)", ta, re.S).group(1))
    print("### LA RISERVA sul netto al confine in 2050 tick (accumulo_controllo.txt): %+.4e" % ris)
    for nome, s in tabelle.items():
        cum = np.cumsum(s)
        quante = int(np.sum(cum <= ris)) if ris > 0 else 0
        print("    %-36s la riserva paga %d nascite in fila (il costo cumulato: le prime 5 %s)" % (nome, quante, ", ".join("%.2f" % x for x in cum[:5])))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
