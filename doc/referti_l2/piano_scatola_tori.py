# -*- coding: utf-8 -*-
r"""**I TORI MINIMI DEL PIANO DI VERIFICA** *(Luca `2026-11-16` `17:47`; R-SCATOLA al 5% con le TRE clausole, la correzione di Luca `16:58`)*.

    python doc/referti_l2/piano_scatola_tori.py > doc/referti_l2/piano_scatola_tori.txt

**La regola:** `R_ogg = r_scena + 25` *(il raggio del 5% del vuoto del mattone, `prova_scatola5`: `25.0` a `k 0`)*; **la distanza dal centro al LATO del rombo `L sqrt(3)/4`
almeno `max(3 R_ogg, 2 R_ogg + 30)`**; `L` intero per eccesso, e il primo multiplo di `3` da li' *(come `L 186`: il nodo buono del francobollo e' a passi di `3`)*.
**`r_scena`:** la coppia a distanza `d`: `d / 2`; il triangolo di lato `a`: `a / sqrt(3)`. **Per una corsa lunga conta la `d` PIU' GRANDE che la corsa tocca** *(dalle corse di `L 162`)*.
"""
import math
import sys

R5 = 25.0


def L_min(r):
    R = r + R5
    lato = max(3.0 * R, 2.0 * R + 30.0)
    L = int(math.ceil(lato * 4.0 / math.sqrt(3.0)))
    L3 = L + (-L) % 3
    return R, lato, L, L3


def main():
    print("=" * 110)
    print("I TORI MINIMI DEL PIANO DI VERIFICA (R-SCATOLA al 5%%, tre clausole; R_ogg = r_scena + %g)" % R5)
    print("=" * 110)
    print("    %-52s %8s %8s %10s %8s %10s" % ("la scena", "r_scena", "R_ogg", "lato min", "L min", "L mult. 3"))
    righe = [("il mattone da solo", 0.0),
             ("FASE 1: la coppia a 35", 35.0 / 2), ("FASE 1: la coppia a 45", 45.0 / 2),
             ("FASE 1: la coppia a 51", 51.0 / 2), ("FASE 1: la coppia a 66", 66.0 / 2),
             ("FASE 3 V-B2: in fase da 35 (su L 162 d fra 28.7 e 35.1)", 35.06 / 2),
             ("FASE 3 V-B2pi: antifase da 35 (su L 162 d fino a 42.42)", 42.42 / 2),
             ("FASE 3 V-T120: il triangolo (il lato fino a 40.84)", 40.84 / math.sqrt(3.0))]
    for nome, r in righe:
        R, lato, L, L3 = L_min(r)
        print("    %-52s %8.2f %8.2f %10.2f %8d %10d" % (nome, r, R, lato, L, L3))
    print("=" * 110)
    return 0


if __name__ == "__main__":
    sys.exit(main())
