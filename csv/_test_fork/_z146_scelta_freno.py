# -*- coding: utf-8 -*-
"""`Z146` -- LA LETTURA DI `V8`/`V9`: quanto costa la DERIVA della forma piana, a questi `|dx|/d`.

**Non ricopia numeri: PARSA `BILANCIO_d0.txt`** (`P1-ter`).

La domanda che decide fra le due forme della scheda 11:
  `piana`  `(d-LAM) <- (d-LAM)*exp(x)`      deriva `+E[x^2]/2` per applicazione, MOLTIPLICATIVA
  `tanh`   `(d-LAM) <- (d-LAM)*(1+tanh(x))` deriva ZERO ESATTO, ma SATURA a `2`

**E DICHIARA SUBITO IL PROPRIO LIMITE:** la deriva dipende da **`E[x^2]`**, e `E[x^2]` **NON E'
STATO REGISTRATO** -- l'involucro ha salvato **quantili**, `max` e quote. Quindi qui si da' un
**INTERVALLO** fra due ipotesi estreme, non un numero. **Un intervallo dichiarato vale; un
numero inventato no.**

ASCII puro.
"""
import io
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

SRC = os.path.join(_QUI, "_cura2_corto", "BILANCIO_d0.txt")
DEST = os.path.join(_QUI, "_cura2_corto", "Z146_scelta_freno.txt")
PASSI = (120, 1200, 6000)


def leggi_v8():
    """Estrae le righe `discese`/`salite` dalla tabella V8/V9. Nessun numero a mano."""
    t = io.open(SRC, encoding="utf-8").read()
    i = t.index("V8/V9")
    fuori = {}
    for r in t[i:].splitlines():
        c = r.split()
        if len(c) >= 8 and c[0] in ("discese", "salite"):
            fuori[c[0]] = dict(n=int(c[1]), p50=float(c[2]), p90=float(c[3]),
                               p99=float(c[4]), p999=float(c[5]), mx=float(c[6]))
    assert set(fuori) == {"discese", "salite"}, "tabella V8/V9 non trovata: %r" % (fuori,)
    return fuori


def main():
    W = sys.stdout.write
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        W(s)
        f.write(s)

    v = leggi_v8()
    P("# `Z146` -- LA SCELTA DELLA FORMA DEL FRENO-LEGGE, letta da `V8`/`V9`\n")
    P("# sorgente: %s (PARSATO, non ricopiato)\n#\n" % os.path.relpath(SRC, _QUI))

    P("I NUMERI, come stanno nel referto:\n")
    P("  %-10s %12s %9s %9s %9s %9s %9s\n"
      % ("verso", "n", "p50", "p90", "p99", "p99.9", "max"))
    for k in ("discese", "salite"):
        d = v[k]
        P("  %-10s %12d %9.4f %9.4f %9.4f %9.4f %9.4f\n"
          % (k, d["n"], d["p50"], d["p90"], d["p99"], d["p999"], d["mx"]))

    mx = max(v["discese"]["mx"], v["salite"]["mx"])
    P("\n" + "=" * 92 + "\n1. LA SATURAZIONE DI `tanh` -- il suo unico difetto dichiarato\n" + "=" * 92 + "\n")
    P("  `1+tanh(x) < 2` per costruzione, e la saturazione conta quando `x` e' di ordine `1`.\n")
    P("  il MASSIMO misurato su %d campioni e' x = %.4f\n"
      % (v["discese"]["n"] + v["salite"]["n"], mx))
    P("  fattore a quel massimo: 1+tanh(%.4f) = %.6f   contro exp(%.4f) = %.6f\n"
      % (mx, 1 + np.tanh(mx), mx, np.exp(mx)))
    P("  scarto fra le due forme AL MASSIMO MISURATO: %.3e (relativo %.3e)\n"
      % (abs((1 + np.tanh(mx)) - np.exp(mx)), abs((1 + np.tanh(mx)) - np.exp(mx)) / np.exp(mx)))
    P("\n  -> il tetto e' a `x` di ordine 1; il massimo misurato e' %.0f VOLTE piu' piccolo.\n"
      % (1.0 / mx))
    P("     LA SATURAZIONE DI `tanh` NON SI MANIFESTA MAI in questo regime, e la quota con\n")
    P("     |dx|/d > 0.5 e' ZERO su entrambi i versi.\n")

    P("\n" + "=" * 92 + "\n2. LA DERIVA DELLA FORMA PIANA -- e QUI IL DATO MANCA\n" + "=" * 92 + "\n")
    P("  La deriva per applicazione e' `E[x^2]/2`, e su N applicazioni il fattore accumulato\n")
    P("  e' `exp(N*E[x^2]/2)` (moltiplicativo).\n")
    P("  ⚠ `E[x^2]` NON E' STATO REGISTRATO: l'involucro ha salvato QUANTILI, `max` e quote.\n")
    P("    Quindi si da' un INTERVALLO fra due ipotesi estreme, non un numero.\n\n")
    P("  %-34s %12s %12s %12s\n" % ("ipotesi su sqrt(E[x^2])", "120 passi", "1200 passi", "6000 passi"))
    for nome, x in (("= p50  (%.4f) -- MINIMO" % v["salite"]["p50"], v["salite"]["p50"]),
                    ("= p90  (%.4f)" % v["salite"]["p90"], v["salite"]["p90"]),
                    ("= p99  (%.4f)" % v["salite"]["p99"], v["salite"]["p99"]),
                    ("= max  (%.4f) -- MASSIMO" % mx, mx)):
        col = []
        for N in PASSI:
            col.append("%+.2f %%" % (100.0 * (np.exp(N * x * x / 2.0) - 1.0)))
        P("  %-34s %12s %12s %12s\n" % (nome, col[0], col[1], col[2]))

    P("\n  -> A 120 PASSI LA DIFFERENZA E' TRASCURABILE IN OGNI IPOTESI.\n")
    P("     A 6000 PASSI L'INTERVALLO E' TROPPO LARGO PER DECIDERE: va da qualche per cento\n")
    P("     a un fattore. **E' UN LIMITE DELLA MIA MISURA, non del sistema.**\n")

    P("\n" + "=" * 92 + "\n3. COSA SI PUO' DIRE, E COSA NO\n" + "=" * 92 + "\n")
    P("  SI PUO' DIRE:\n")
    P("   - la SATURAZIONE di `tanh` non si manifesta: il suo unico difetto dichiarato NON\n")
    P("     si presenta a questi |dx|/d. Costo MISURATO: nessuno.\n")
    P("   - la DERIVA di `piana` e' positiva e si accumula; a 120 passi e' trascurabile.\n")
    P("   - le due forme coincidono entro %.1e al massimo misurato.\n" % (abs((1 + np.tanh(mx)) - np.exp(mx)) / np.exp(mx)))
    P("\n  NON SI PUO' DIRE:\n")
    P("   - QUANTO valga la deriva a tempi lunghi: serve `E[x^2]`, che non ho registrato.\n")
    P("   - che la scelta sia indifferente: lo e' a 120 passi, NON e' dimostrato a 6000.\n")
    P("\n  COSA LO CHIUDEREBBE, e costa ZERO run in piu':\n")
    P("   registrare `mean((dx/d)^2)` nello stesso involucro che gia' registra i quantili.\n")
    P("   E' UNA SOMMA IN PIU', sugli stessi campioni.\n")
    P("\n  ⚠ E LA SCELTA RESTA DI LUCA: questa e' la misura, non la decisione.\n")
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
