# -*- coding: utf-8 -*-
"""I CONTI DELLA CORREZIONE DI ITO, verificati numericamente (scheda 11, par.4-bis).

Proposta del guardiano, 2026-09-24. SOLA LETTURA, nessun run, nessun simulatore:
e' un conto SULLA FORMULA, come Z113.

    piana:  u <- u * exp(x)              con x = dx/d
    Ito:    u <- u * exp(x - x^2/2)
    tanh:   u <- u * (1 + tanh(x))       <-- TERZA forma, proposta da Luca il 2026-09-24

Cio' che si verifica, e ogni riga e' un criterio a risposta NOTA:
  * la deriva sotto rumore simmetrico dx = +-a, e il suo ORDINE;
  * la FEDELTA' alla legge u(1+x) a cui entrambe tendono;
  * la MONOTONIA in dx -- dove la forma di Ito smette di esserlo.
ASCII PURO.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)


def piana(x):
    return np.exp(x)


def ito(x):
    return np.exp(x - x * x / 2.0)


def tanhf(x):
    """(1 + tanh(x)). Deriva ESATTAMENTE nulla per rumore simmetrico, a TUTTI gli ordini:
    (1 + tanh(x)) + (1 + tanh(-x)) = 2 per disparita' di tanh."""
    return 1.0 + np.tanh(x)


def main():
    W = sys.stdout.write
    W("# I CONTI DELLA CORREZIONE DI ITO -- scheda 11, par.4-bis\n#\n")
    W("# piana: u <- u*exp(x)          Ito: u <- u*exp(x - x^2/2)      x = dx/d\n\n")

    W("DERIVA SOTTO RUMORE SIMMETRICO  dx = +-a,  s = a/d\n")
    W("%8s | %14s %14s | %14s %14s | %10s\n"
      % ("s", "piana E[f]-1", "attesa s^2/2", "Ito E[f]-1", "attesa -s^4/12", "rapporto"))
    W("-" * 96 + "\n")
    for s in (0.5, 0.25, 0.125, 0.0625, 0.03125):
        p = 0.5 * (piana(s) + piana(-s)) - 1.0
        i = 0.5 * (ito(s) + ito(-s)) - 1.0
        W("%8.5f | %14.6e %14.6e | %14.6e %14.6e | %10.3e\n"
          % (s, p, s * s / 2, i, -s ** 4 / 12, abs(i) / abs(p)))

    W("\nL'ORDINE, raddoppiando s: la piana deve fare x4 (2^2), Ito x16 (2^4)\n")
    for a, b in ((0.25, 0.125), (0.125, 0.0625), (0.0625, 0.03125)):
        pa = 0.5 * (piana(a) + piana(-a)) - 1
        pb = 0.5 * (piana(b) + piana(-b)) - 1
        ia = 0.5 * (ito(a) + ito(-a)) - 1
        ib = 0.5 * (ito(b) + ito(-b)) - 1
        W("  s %.5f -> %.5f :  piana x%.3f   Ito x%.3f\n" % (b, a, pa / pb, ia / ib))

    W("\nFEDELTA' alla legge u(1+x), a cui ENTRAMBE tendono\n")
    W("%6s | %10s | %12s %12s | %12s %12s\n"
      % ("x", "u(1+x)", "piana", "eccesso", "Ito", "eccesso"))
    W("-" * 82 + "\n")
    for x in (0.05, 0.1, 0.3, 0.5):
        W("%6.2f | %10.5f | %12.5f %+12.3e | %12.5f %+12.3e\n"
          % (x, 1 + x, piana(x), piana(x) - (1 + x), ito(x), ito(x) - (1 + x)))
    W("  -> exp(x - x^2/2) = 1 + x + O(x^3): i termini in x^2 si CANCELLANO.\n")

    W("\nMONOTONIA IN dx -- il massimo di exp(x - x^2/2) e' in x = 1, dove vale sqrt(e)\n")
    W("%6s | %14s | %12s | %s\n" % ("x", "piana exp(x)", "Ito", "nota"))
    W("-" * 82 + "\n")
    for x in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        nota = ""
        if abs(x - 1.0) < 1e-12:
            nota = "<-- IL MASSIMO, sqrt(e) = %.5f" % np.sqrt(np.e)
        elif x > 2.0:
            nota = "<-- UNA SALITA FA SCENDERE"
        elif abs(x - 2.0) < 1e-12:
            nota = "<-- una salita non muove nulla"
        W("%6.1f | %14.5f | %12.5f | %s\n" % (x, piana(x), ito(x), nota))

    W("\nIL CASO CHE DEVE FALLIRE: una forma monotona NON deve avere un massimo interno.\n")
    xs = np.linspace(0.0, 3.0, 3001)
    d_p = np.diff(piana(xs))
    d_i = np.diff(ito(xs))
    W("  piana: incrementi negativi su [0,3] = %d su %d  -> %s\n"
      % (int((d_p < 0).sum()), len(d_p),
         "MONOTONA" if (d_p >= 0).all() else "*** NON monotona ***"))
    W("  Ito:   incrementi negativi su [0,3] = %d su %d  -> %s\n"
      % (int((d_i < 0).sum()), len(d_i),
         "MONOTONA" if (d_i >= 0).all() else "NON MONOTONA (atteso: il massimo e' in x=1)"))
    W("\n" + "=" * 96 + "\n")
    W("LA TERZA FORMA: u <- u*(1 + tanh(x))   -- proposta di Luca, 2026-09-24\n")
    W("=" * 96 + "\n")
    W("  DERIVA per rumore simmetrico: e' ZERO ESATTO, a TUTTI gli ordini.\n")
    W("  %8s | %24s | %s\n" % ("s", "E[f] - 1", "quanto dista da 0"))
    for s in (0.5, 0.25, 0.125, 0.0625, 1e-3):
        v = 0.5 * (tanhf(s) + tanhf(-s)) - 1.0
        W("  %8.5f | %24.15e | %s\n"
          % (s, v, "ZERO ESATTO" if v == 0.0 else "*** non zero ***"))
    W("  -> (1+tanh(x)) + (1+tanh(-x)) = 2 per DISPARITA' di tanh: non e' un'approssimazione.\n")

    W("\n  MONOTONIA: la derivata e' sech^2(x) > 0 sempre.\n")
    xs2 = np.linspace(-3.0, 3.0, 6001)
    dt = np.diff(tanhf(xs2))
    W("  incrementi negativi su [-3,3]: %d su %d -> %s\n"
      % (int((dt < 0).sum()), len(dt),
         "MONOTONA" if (dt >= 0).all() else "*** NON monotona ***"))

    W("\n  MAI SOTTO LAM: 1 + tanh(x) sta in (0, 2), quindi u_new > 0 per qualunque dx.\n")
    W("  x = -50 -> fattore %.6e ;  x = +50 -> fattore %.6f   (il TETTO e' 2)\n"
      % (tanhf(-50.0), tanhf(50.0)))

    W("\n  FEDELTA': 1 + tanh(x) = 1 + x - x^3/3 + ... -> NESSUN termine in x^2, come Ito.\n")
    W("  %6s | %9s | %11s %11s | %11s %11s | %11s %11s\n"
      % ("x", "u(1+x)", "piana", "eccesso", "Ito", "eccesso", "tanh", "eccesso"))
    W("  " + "-" * 96 + "\n")
    for x in (0.1, 0.3, 0.5, 1.0):
        W("  %6.2f | %9.5f | %11.5f %+11.3e | %11.5f %+11.3e | %11.5f %+11.3e\n"
          % (x, 1 + x, piana(x), piana(x) - (1 + x), ito(x), ito(x) - (1 + x),
             tanhf(x), tanhf(x) - (1 + x)))

    W("\n" + "=" * 96 + "\n")
    W("LE TRE FORME A CONFRONTO\n")
    W("=" * 96 + "\n")
    W("  %-22s %-23s %-12s %-16s %s\n"
      % ("", "deriva simmetrica", "monotona", "fedelta'", "tetto per SALITA"))
    W("  " + "-" * 94 + "\n")
    W("  %-22s %-23s %-12s %-16s %s\n"
      % ("piana  exp(x)", "+s^2/2  (2 ord., POS)", "SI'", "eccesso +x^2/2", "NESSUNO"))
    W("  %-22s %-23s %-12s %-16s %s\n"
      % ("Ito    exp(x-x^2/2)", "-s^4/12 (4 ord., NEG)", "*** NO ***", "O(x^3)",
         "sqrt(e) = 1.6487"))
    W("  %-22s %-23s %-12s %-16s %s\n"
      % ("tanh   1+tanh(x)", "ZERO ESATTO", "SI'", "O(x^3)", "2 (RADDOPPIA)"))
    W("\n  -> `tanh` DOMINA `Ito` su OGNI asse: deriva piu' piccola (zero contro 4 ordine),\n")
    W("     MONOTONA (Ito no), stessa fedelta', e tetto MENO restrittivo (2 contro 1.6487).\n")
    W("     La scelta vera e' fra `piana` e `tanh`, e la decide la DISTRIBUZIONE di |dx|/d:\n")
    W("     `piana` non ha tetto ma HA deriva; `tanh` non ha deriva ma SATURA a 2.\n")

    W("\n!! NESSUNO DI QUESTI NUMERI DICE QUALE FORMA SIA GIUSTA: lo decide la\n")
    W("   DISTRIBUZIONE di |dx|/d nei run, che NON e' misurata (punti V8/V9).\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
