# -*- coding: utf-8 -*-
"""IL COSTO DEL MOTORE — **misurato, non stimato.**

> ### ⛔⛔ **PERCHE' QUESTO FILE ESISTE** *(`2026-10-17`, su rifiuto di `P-MOD`)*:
> questo `main` viveva ### **dentro `motore.py`**, che e' ### **nel NUCLEO della fisica** —
> e `motore.py` era a ### **`699` righe su un tetto di `700`.** ### **Aggiungere `3` righe
> per `D0` lo ha portato oltre**, e la regola e' chiara: ### **oltre SI DIVIDE, NON SI
> ALLUNGA.**
> ### ✅ **E uscire e' la cosa giusta comunque:** e' ### **un MISURATORE dentro un
> modulo del nucleo**, come `grafo.costo` — e nel nucleo i rami si dichiarano e i
> `default` sono vietati ### **perche' la' un `if` puo' cambiare la legge che gira.**
> ### **Un misuratore no, e allora sta fuori.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
import _presidio                                              # noqa: E402
import incidenza as IN                                        # noqa: E402
import motore as MO                                           # noqa: E402
import stato as ST                                            # noqa: E402

NL = chr(10)


def main(argv):
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    import stato as ST
    print("=" * 96)
    print("LE ALLOCAZIONI PER TICK -- misurate, non dichiarate")
    print("=" * 96)
    for nn in (64, 256, 1024):
        ii = np.arange(nn, dtype=IN.INDICE)
        jj = (ii + 1) % nn
        inc = IN.Incidenza(ii, jj, nn, capacita=nn)
        n_ver = np.zeros((2 * inc.m, 3), dtype=float)
        n_ver[:, 2] = 1.0
        U = np.zeros((inc.m, 2, 2), dtype=complex)
        U[:, 0, 0] = 1.0
        U[:, 1, 1] = 1.0
        st = ST.nuovo(nn, inc.m)
        st["psi_h"][0, 0] = 1.0
        mot = MO.Motore(inc, MO.Geometria(n_ver, U), st, np.full(nn, 0.1), "numpy")
        for _ in range(3):
            mot.operatori["grover"](st, {}, 1)
            mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
            mot.operatori["spostamento_trasporto"](st, {}, 1)
        primi = mot.ripieghi
        for _ in range(20):
            mot.operatori["grover"](st, {}, 1)
            mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
            mot.operatori["spostamento_trasporto"](st, {}, 1)
        print("  n=%-6d  buffer allocati: %d nei primi 3 tick, %d nei 20 dopo"
              "   byte: %d" % (nn, primi, mot.ripieghi - primi, mot.byte()))
    print("=" * 96)
    print("  ### ZERO allocazioni nei tick dopo i primi: e' la lettura che conta")
    print("=" * 96)
    print()
    print("=" * 96)
    print("UNA `cresci()` CONTRO UN PASSO, SULLO STESSO GRAFO -- il rapporto, MISURATO")
    print("=" * 96)
    print("  ### Il mandato della verifica esterna: se la ricostruzione supera il passo,")
    print("  ### SI DICHIARA come limite noto. ### NON si ottimizza adesso.")
    import time
    for nn in (1000, 10000, 100000):
        ii = np.arange(nn, dtype=IN.INDICE)
        jj = (ii + 1) % nn
        inc = IN.Incidenza(ii, jj, nn, capacita=2 * nn)
        n_ver = np.zeros((2 * inc.m, 3), dtype=float)
        n_ver[:, 2] = 1.0
        U = np.zeros((inc.m, 2, 2), dtype=complex)
        U[:, 0, 0] = 1.0
        U[:, 1, 1] = 1.0
        st = ST.nuovo(nn, inc.m)
        st["psi_h"][0, 0] = 1.0
        mot = MO.Motore(inc, MO.Geometria(n_ver, U), st, np.full(nn, 0.1), "numpy")
        # ### un passo = i tre pezzi su `psi`, cioe- cio- che un tick fa DAVVERO
        def _passo():
            mot.operatori["grover"](st, {}, 1)
            mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
            mot.operatori["spostamento_trasporto"](st, {}, 1)
        _passo()                                   # ### scalda i buffer: il primo ALLOCA
        giri = 20 if nn <= 10000 else 5
        t0 = time.perf_counter()
        for _ in range(giri):
            _passo()
        tp = (time.perf_counter() - t0) / giri
        # ### e una `cresci()` che NON cambia niente: ### **si misura la RICOSTRUZIONE**,
        # ### non la chirurgia -- cosi- il numero e- quello dell-`argsort`.
        tieni = np.ones(inc.m, dtype=bool)
        t0 = time.perf_counter()
        for _ in range(giri):
            mot.apri_tick()
            mot.cresci(tieni, [], [], 0, None)
            mot.chiudi_tick()
        tc = (time.perf_counter() - t0) / giri
        print("  n=%-7d m=%-7d  passo %8.3f ms   cresci() %8.3f ms   rapporto %6.2fx  %s"
              % (nn, inc.m, tp * 1e3, tc * 1e3, tc / tp,
                 "### LA RICOSTRUZIONE DOMINA" if tc > tp else "il passo domina"))
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
