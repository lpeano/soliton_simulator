# -*- coding: utf-8 -*-
r"""**LA NASCITA A ENERGIA NULLA SENZA RADICE: I NUMERI PER ANELLO E IL PERCHE'** *(Luca `2026-11-20` `10:31`, TODO 2; la carta `doc/TASK_HISTORY/2026-11-20_nascita_energia_nulla.md`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/nascita_energia_nulla_anelli.py > doc/referti_l2/nascita_energia_nulla_anelli.txt

**Perche' esiste** *(DICHIARATO, dopo il primo sguardo alle parti)*: `nascita_energia_nulla.py referto` stampa la distribuzione per anello SOLO sugli archi con la radice; **sulle parti la radice manca su tutti**, e la distribuzione di `DH(0)`, `DH(1)` e dei cambi di segno non si stamperebbe. **Questo script la legge dalle parti** *(`E:/soliton_simulator/controllo/nascita_nulla/parte_*.npz`, nessun conto nuovo)*; **e sui primi `50` archi nell'ordine di scatto, il perche': `DH(0)` e `DH(1)` scomposti per termine col conto PIENO** *(`nascita_dentro_fuori.famiglie`)*.
**Il caso noto** *(Q-A4)*: `DH(0)` e `DH(1)` a mano delle parti contro il conto pieno sugli stessi `50` archi, entro `1e-9` relativo.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import nascita_energia_nulla as NN  # noqa: E402
import nascita_dentro_fuori as ND  # noqa: E402

N_PERCHE = 50


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "nascita_energia_nulla.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA NASCITA A ENERGIA NULLA SENZA RADICE: I NUMERI PER ANELLO E IL PERCHE' (Luca 2026-11-20 10:31)")
    print("=" * 130)
    G, psi, phi, archi, r, Tk, _c = NN.carica()
    T = {c: np.full(len(archi), np.nan) for c in NN.CAMPI}
    for p in sorted(x for x in os.listdir(NN.DIR_O) if x.startswith("parte_")):
        with np.load(os.path.join(NN.DIR_O, p)) as d:
            for c in NN.CAMPI:
                T[c][d["sel"]] = d[c]
    st = T["stato"]
    print("### gli stati: la radice %d, senza radice %d, un estremo esatto %d, indefiniti %d (su %d)" % (int(np.sum(st == 0)), int(np.sum(st == 1)), int(np.sum(st == 2)), int(np.sum(st == 3)), len(archi)))
    print("### i segni: DH(0) negativo %d, positivo %d; DH(1) negativo %d, positivo %d" % (int(np.sum(T["DH0"] < 0)), int(np.sum(T["DH0"] > 0)), int(np.sum(T["DH1"] < 0)), int(np.sum(T["DH1"] > 0))))
    print("### i cambi di segno di DH sugli 11 punti di alpha: %s" % {int(k): int(v) for k, v in zip(*np.unique(T["cambi"], return_counts=True))})
    print("### DH(1) - DH(0) (quanto la quota di D7 cambia l'energia): min %+.4e, mediana %+.4e, max %+.4e" % (float(np.min(T["DH1"] - T["DH0"])), float(np.median(T["DH1"] - T["DH0"])), float(np.max(T["DH1"] - T["DH0"]))))
    print("-" * 130)
    print("### PER ANELLO:")
    for lo in range(10, 24, 2):
        s = (r >= lo) & (r < lo + 2)
        if s.any():
            print("    r %2d-%2d: %4d archi; DH(0) mediana %+.4e (min %+.4e, max %+.4e); DH(1) mediana %+.4e (min %+.4e, max %+.4e); DH(1)/DH(0) mediana %.4f" % (
                lo, lo + 2, int(s.sum()), float(np.median(T["DH0"][s])), float(np.min(T["DH0"][s])), float(np.max(T["DH0"][s])),
                float(np.median(T["DH1"][s])), float(np.min(T["DH1"][s])), float(np.max(T["DH1"][s])), float(np.median(T["DH1"][s] / T["DH0"][s]))))
    print("-" * 130)
    F0 = ND.famiglie(G, psi, phi)
    rig = {0.0: [], 1.0: []}
    scarto = 0.0
    for q in range(N_PERCHE):
        P = NN.preparo(G, psi, phi, int(archi[q]))
        for al in (0.0, 1.0):
            Dl = ND.delta(F0, ND.famiglie(P["G2"], NN.psi_alpha(P, al), P["ph"]))
            rig[al].append([Dl[k] for k in NN.CHIAVI])
            dm = T["DH0" if al == 0.0 else "DH1"][q]
            scarto = max(scarto, abs(Dl["tot"] - dm) / abs(F0["tot"]))
    print("### IL PERCHE' (i primi %d archi nell'ordine di scatto, il conto pieno; la mediana di ogni termine):" % N_PERCHE)
    for al in (0.0, 1.0):
        M = np.array(rig[al])
        print("    alpha %.0f: %s" % (al, ", ".join("%s %+.4e" % (k, float(np.median(M[:, c]))) for c, k in enumerate(NN.CHIAVI))))
    print("### il caso noto: DH a mano delle parti contro il conto pieno, lo scarto massimo relativo a |H| %.3e" % scarto)
    print("-" * 130)
    print("  DEVE: %-118s %s" % ("il caso noto: DH(0) e DH(1) delle parti = il conto pieno entro 1e-9 relativo a |H| (%d archi)" % N_PERCHE, "PASSA" if scarto < 1e-9 else "### FALLISCE"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
