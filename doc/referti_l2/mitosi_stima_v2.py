# -*- coding: utf-8 -*-
r"""**LA STIMA DELLE DUE CORSE, C2-EXT E MITOSI, COL TRONCO COMUNE** *(il TODO `4`; Luca `2026-11-20` `17:08`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `12`-`13`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_stima_v2.py > doc/referti_l2/mitosi_stima_v2.txt

**LA V2:** la v1 *(`mitosi_stima.py`, `4391013c`)* si e' fermata all'import di `_presidio` *(`csv/` non nel percorso)*, prima di ogni conto; qui solo il percorso.

**I numeri entrano da file, non a mano:** **i costi** *(il tick prima e dopo una nascita, la nascita)* **dal referto `doc/referti_l2/mitosi_nasce.txt`** *(la riga `### IL COSTO`)*; **i tempi di scatto** dai `2929` candidati *(`E:/soliton_simulator/controllo/torsione/candidati.npz`, `T`: l'estrapolazione LINEARE di `Theta` da C2 fino a `k 3000`, `torsione_segmenti.py` del ramo `primo-ordine`)*; **la taglia di uno stato** da uno stato di C2.
**Il tronco comune:** **da `k 3000` al primo scatto** *(il minimo di `T`)* **una corsa sola** *(il passo di MITOSI = quello di C2 al bit, P6.0)*; **poi due rami in parallelo:** C2-EXT *(le nascite spente)* e MITOSI.
**Le nascite di MITOSI in una finestra** `Delta` dopo il primo scatto: **i candidati con `T` dentro la finestra, al piu' uno per tick** *(D-M4)*. ### **E' un MINIMO e un'APPROSSIMAZIONE, dichiarati:** gli archi NUOVI *(da `Theta = 0`)* non sono contati; `T` e' lineare *(il lapse si muove)*; le nascite cambiano il lapse vicino.
**Le lunghezze dei rami NON sono decise:** **la tabella per piu' finestre** *(Luca sceglie)*.
"""
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.join(os.path.dirname(os.path.dirname(_QUI)), "csv")
if _CSV not in sys.path:
    sys.path.insert(0, _CSV)                                               # ### V2: la v1 (4391013c) non trovava _presidio
F_COSTO = os.path.join(_QUI, "mitosi_nasce.txt")
F_P6 = os.path.join(_QUI, "mitosi_p6_0.txt")
F_CAND = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "torsione", "candidati.npz")
F_STATO = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "C2", "stato_03000.npz")
K0 = 3000
FINESTRE = (2500, 5000, 10000, 20000, 40000, 72000)
OGNI_STATO = 250


def costi():
    with open(F_COSTO, encoding="utf-8") as f:
        for riga in f:
            if riga.startswith("### IL COSTO"):
                x = [float(v) for v in re.findall(r"(\d+\.\d+) s", riga)]
                return x[0], x[1], x[2], riga.strip()
    raise RuntimeError("la riga del costo non e' nel referto %s" % F_COSTO)


def costo_p6():
    """### il tick di MITOSI senza nascite in P6.0 (meno processi sulla macchina): `il tempo per tick ... MITOSI <x> s`."""
    with open(F_P6, encoding="utf-8") as f:
        for riga in f:
            if riga.startswith("### il tempo per tick"):
                return float(re.search(r"MITOSI (\d+\.\d+) s", riga).group(1)), riga.strip()
    raise RuntimeError("la riga del tempo non e' nel referto %s" % F_P6)


def main():
    import _presidio
    _presidio.avvia(__file__)
    t_carico, t_dopo_carico, t_nascita, riga = costi()
    t_scarico, riga6 = costo_p6()
    with np.load(F_CAND) as d:
        T = np.sort(d["T"].copy())
    taglia = os.path.getsize(F_STATO)
    print("=" * 130)
    print("LA STIMA DELLE DUE CORSE C2-EXT E MITOSI COL TRONCO COMUNE (Luca 2026-11-20 17:08; il TODO 4)")
    print("=" * 130)
    print("### i costi (dal referto %s): %s" % (os.path.basename(F_COSTO), riga))
    print("### e dal referto %s: %s" % (os.path.basename(F_P6), riga6))
    print("    ### LA FORBICE: il tick %.3f s (P6.0, la macchina meno carica) -- %.3f s (nasce, la macchina carica); una nascita %.1f s (carica)" % (t_scarico, max(t_carico, t_dopo_carico), t_nascita))
    print("### i candidati: %d; il primo scatto a T %.1f; T al 10%% %.0f, al 50%% %.0f, al 90%% %.0f, l'ultimo %.0f" % (
        len(T), T[0], *np.percentile(T, [10, 50, 90]), T[-1]))
    for nome_t, t_senza in (("SCARICA", t_scarico), ("CARICA", max(t_carico, t_dopo_carico))):
        t_dopo = t_senza
        print("### ---- la macchina %s: il tick %.3f s" % (nome_t, t_senza))
        k1 = int(math.floor(T[0]))
        tronco = k1 - K0
        h_tronco = tronco * t_senza / 3600.0
        print("### IL TRONCO COMUNE: da k %d a k %d (il tick prima del primo scatto): %d tick, %.1f ore, UNA corsa; %d stati da %.1f MB (%.2f GB)" % (
            K0, k1, tronco, h_tronco, tronco // OGNI_STATO, taglia / 1e6, (tronco // OGNI_STATO) * taglia / 1e9))
        print("### I DUE RAMI dopo il primo scatto, in PARALLELO (due processi): la finestra Delta in tick")
        print("      Delta    nascite (minimo)   MITOSI ore   C2-EXT ore   il totale dal k %d (ore, coi rami in parallelo)   gli stati (GB, i due rami)" % K0)
        for D in FINESTRE:
            nas = int(np.sum(T < k1 + D))
            nas = min(nas, D)
            h_m = (D * t_dopo + nas * t_nascita) / 3600.0
            h_c = D * t_senza / 3600.0
            print("    %7d    %6d             %8.1f     %8.1f     %8.1f                                       %6.2f" % (
                D, nas, h_m, h_c, h_tronco + max(h_m, h_c), 2 * (D // OGNI_STATO) * taglia / 1e9))
    print("### LE AVVERTENZE (dichiarate): le nascite sono un MINIMO (gli archi nuovi da Theta = 0 non sono contati) e T e' l'estrapolazione LINEARE da C2 a k 3000;")
    print("    il costo del tick dopo la nascita e' misurato dopo UNA nascita (un grafo che cresce di piu' costa di piu': O(m)); le misure ogni 50 tick e D1, E1 non sono nel costo.")
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
