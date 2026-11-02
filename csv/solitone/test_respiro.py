# -*- coding: utf-8 -*-
r"""**I TEST DEL RESPIRO SULLA CARTA** *(il task history `2026-11-02_accensione_lenta`, sez. `6-bis`, `R1`-`R3`)*: ### **su serie e intervalli costruiti, nessuna scena.**"""
import math

import numpy as np

from . import respiro as RE

PASSO = 0.15                   # ### il passo di BG-F-0.15 (s 0.15: un tick)
N_TICK = 4000                  # ### la finestra (W1): 600 unita' di tempo
PERIODO_PROVA = 4.07           # ### il periodo del seno di prova (il periodo del modo di modo_lento.txt)
OGNI_RADO = 10                 # ### il campionamento dei campioni committati (_vuoto_vivo_B.OGNI)
TOLL_FREQ = 1e-6               # ### R1: l'errore relativo sulla frequenza
TOLL_SOMMA = 1e-15             # ### R3


def gira(esito):
    print("### IL RESPIRO SULLA CARTA (csv/solitone/respiro.py): PASSO %g N_TICK %d PERIODO_PROVA %g OGNI_RADO %d TOLL_FREQ %g TOLL_SOMMA %g; PERIODI_MIN %d"
          % (PASSO, N_TICK, PERIODO_PROVA, OGNI_RADO, TOLL_FREQ, TOLL_SOMMA, RE.PERIODI_MIN))
    t = np.arange(N_TICK) * PASSO
    f0 = 1.0 / PERIODO_PROVA
    y = 0.59 + 1e-5 * t - 3e-9 * t * t + 2e-3 * np.cos(2.0 * math.pi * f0 * t + 0.7)
    r = RE.omega(y, PASSO)
    p = r["picchi"][0]
    err = abs(p["frequenza"] / f0 - 1.0)
    esito("DEVE PASSARE: R1 omega ritrova un seno noto (periodo %g, a ogni tick, con una tendenza quadratica) entro %g sulla frequenza" % (PERIODO_PROVA, TOLL_FREQ),
          err <= TOLL_FREQ and abs(p["ampiezza"] / 2e-3 - 1.0) <= 1e-6, "periodo %.9f, errore %.1e, ampiezza %.6e; cambi %.4f" % (p["periodo"], err, p["ampiezza"], r["cambi"]["periodo"]))
    fa = 1.0 / (OGNI_RADO * PASSO) - f0              # ### il seno SOTTO Nyquist che, campionato ogni OGNI_RADO tick, da' gli stessi campioni di f0
    ya = 0.59 + 2e-3 * np.cos(2.0 * math.pi * fa * t + 0.7)
    ra = RE.omega(ya, PASSO)
    rr = RE.omega(ya[::OGNI_RADO], PASSO * OGNI_RADO)
    pa, pr = ra["picchi"][0], rr["picchi"][0]
    esito("DEVE FALLIRE: R1-F un seno di periodo %.4f (sotto il Nyquist dei campioni radi) campionato ogni %d tick ridà la frequenza vera entro %g" % (1.0 / fa, OGNI_RADO, TOLL_FREQ),
          not abs(pr["frequenza"] / fa - 1.0) <= TOLL_FREQ,
          "a ogni tick %.6f; ogni %d tick letto %.6f (l'alias); gli alias dai cambi %s" % (pa["periodo"], OGNI_RADO, pr["periodo"], " ".join("%.4f" % x for x in rr["cambi"]["alias"])))
    P = 2.0 * math.pi / PASSO
    casi = [(0.5, (P - 1.0, P + 2.0), True, -1.5), (P - 0.5, (P - 1.0, P + 2.0), True, -0.5), (3.0, (P - 1.0, P + 2.0), False, 1.0), (P - 2.0, (P - 1.0, P + 2.0), False, 1.0),
            (7.0, (1.0, 1.0 + P), True, -0.5 * P)]
    ok = all(RE.margine_mod(x, iv, P)[0] == d and abs(RE.margine_mod(x, iv, P)[1] - m) <= 1e-12 for x, iv, d, m in casi)
    esito("DEVE PASSARE: R2 margine_mod su un intervallo che passa per lo zero del cerchio: dentro e fuori, il margine col segno, il cerchio intero", ok,
          " ".join("%+.3f" % RE.margine_mod(x, iv, P)[1] for x, iv, _d, _m in casi))
    a, b = (-1.25, 0.5), (3.0, 3.75)
    s_ = RE.somma(a, b)
    o_ = RE.opposto(a)
    esito("DEVE PASSARE: R3 somma e opposto contro il conto a mano", abs(s_[0] - 1.75) <= TOLL_SOMMA and abs(s_[1] - 4.25) <= TOLL_SOMMA and o_ == (-0.5, 1.25), "%s %s" % (s_, o_))
