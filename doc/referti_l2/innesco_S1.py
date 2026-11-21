# -*- coding: utf-8 -*-
r"""**S1 SUI CANDIDATI: QUANTI ARCHI CHE ARRIVANO A `2 pi` PASSANO IL FILTRO DELLA MATERIA** *(Luca `2026-11-17` `21:00`, TODO 2; la carta `doc/TASK_HISTORY/2026-11-17_innesco_contatore.md`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/innesco_S1.py > doc/referti_l2/innesco_S1.txt

**S1** *(la scelta del guardiano; l'`1%` e' un NUMERO, `A1`)*: **la nascita e' permessa solo se il termine della MATERIA della nascita FA** *(`G_psi + a_psi` di `nascita_dentro_fuori.delta`)* **e' sotto l'`1%` di `|Delta H|`.** **I candidati:** i `2929` archi che arrivano a `2 pi` entro `1e5` tick *(`torsione_segmenti.py`, `candidati.npz`)*. ### **LO STATO E' QUELLO DI C2 A `k 3000`, NON quello al momento dello scatto** *(che sta a `2.8e4`-`1e5` tick: non esiste)*: **dichiarato.** **La nascita:** `regole_fase_F3.nascita(..., "FA")` *(la divisione generica, i moduli v4, le fasi FA)*.
**Il caso noto** *(Q-A4)*: sul mattone `L162_MGU_03000`, l'arco a `23.81` nodi: **FA da' `dH +4.459258e+00`, `materia/|dH| 6.002e-02`** *(`regole_fase_F3.txt`)*, alla precisione stampata.
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import regole_fase_F3 as RF  # noqa: E402  (aggiunge al percorso csv/, csv/solitone/, primo_ordine/)

SOGLIA = 0.01
DIR_T = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "torsione")


def caso_noto():
    import _massa_nei_difetti as MD
    import mattone as MT
    from solitone import toro as TO
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L = Z["L"]
        ii, jj, nn, dirs = MD.toro(L)
    with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
        psi, phi = d["psi_h"].copy(), d["phi_h"].copy()
    G = (ii, jj, nn, np.asarray(dirs, dtype=float))
    a = 66417
    Dl, _o = RF.nascita(G, psi, phi, a, "FA")
    rap = abs(Dl["mat"]) / abs(Dl["tot"])
    print("### il caso noto (L162_MGU_03000, l'arco %d: %d -> %d): FA dH %+.6e, materia/|dH| %.3e" % (a, ii[a], jj[a], Dl["tot"], rap))
    return "%+.6e" % Dl["tot"] == "+4.459258e+00" and "%.3e" % rap == "6.002e-02"


def main():
    import _presidio
    import _massa_nei_difetti as MD
    import convergenza as CV
    import prova_scatola5 as PS
    _presidio.avvia(os.path.join(_QUI, "regole_fase_F3.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("S1 SUI CANDIDATI: LA MATERIA DELLA NASCITA FA SOTTO L'1%% DI |DH|? (Luca 2026-11-17 21:00)")
    print("=" * 130)
    esiti = [("il caso noto: FA a 23.81 nodi su L162 = regole_fase_F3.txt alla precisione stampata", caso_noto())]
    with np.load(os.path.join(DIR_T, "candidati.npz")) as d:
        archi, r, Tk = d["archi"].copy(), d["r"].copy(), d["T"].copy()
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        ii, jj, nn, dirs = MD.toro(186)
        assert np.array_equal(np.asarray(Z["mot"].inc.ii), ii) and np.array_equal(np.asarray(Z["mot"].inc.jj), jj), "l'ordine degli archi della scena non e' quello del toro"
        Z["metti"]()
    with np.load(os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "C2", "stato_03000.npz")) as d:
        psi, phi = d["psi_h"].copy(), d["phi_h"].copy()
    G = (ii, jj, nn, np.asarray(dirs, dtype=float))
    print("### %d candidati (r da %.2f a %.2f); lo stato di C2 a k 3000" % (archi.size, float(r.min()), float(r.max())))
    t0 = time.time()
    rap = np.zeros(archi.size)
    dH = np.zeros(archi.size)
    for q, a in enumerate(archi):
        Dl, _o = RF.nascita(G, psi, phi, int(a), "FA")
        if Dl is None:
            rap[q], dH[q] = np.nan, np.nan
            continue
        dH[q] = Dl["tot"]
        rap[q] = abs(Dl["mat"]) / abs(Dl["tot"])
        if q % 250 == 0:
            print("    %d su %d (%.0f s)" % (q, archi.size, time.time() - t0))
            sys.stdout.flush()
    passa = rap < SOGLIA
    print("-" * 130)
    print("### il rapporto materia/|dH| della nascita FA: min %.3e, mediana %.3e, max %.3e; indefinite %d" % (float(np.nanmin(rap)), float(np.nanmedian(rap)), float(np.nanmax(rap)), int(np.sum(np.isnan(rap)))))
    print("### ### PASSANO S1 (materia sotto l'1%%): %d su %d" % (int(np.sum(passa)), archi.size))
    for lo in range(10, 23, 2):
        s = (r >= lo) & (r < lo + 2)
        if s.any():
            print("    r %2d-%2d: %4d archi; materia/|dH| mediana %.3e (min %.3e); dH mediana %+.4e; passano %d" % (lo, lo + 2, int(s.sum()), float(np.nanmedian(rap[s])), float(np.nanmin(rap[s])), float(np.nanmedian(dH[s])), int(np.sum(passa[s]))))
    print("### %.0f s" % (time.time() - t0))
    esiti.append(("P-L4: fra gli archi a 2 pi entro 1e5 tick meno della meta' passa S1 (%d su %d)" % (int(np.sum(passa)), archi.size), int(np.sum(passa)) < archi.size / 2.0))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
