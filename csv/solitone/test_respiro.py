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
FRAZIONE = 0.1                 # ### R4: «fino a 1/10 dell'ampiezza del primo» (Luca, dopo 04b02794)
FRAZIONE_F = 1.0 / 30.0        # ### R4-F: un elenco a 1/30 deve contenere il terzo seno (ampiezza 0.05): DEVE FALLIRE il "non lo contiene"
SEME = 20261102                # ### R5: il rumore
SIGNIF = 3.0                   # ### R5: la soglia di lettura della significativita' (il task history, sez. 8-bis)
TOLL_QUOTA = 1e-2              # ### R5-Q: un seno puro (con la tendenza) ha la quota 1 entro 1e-2 (la tendenza quadratica tolta ne assorbe una parte piccola)


def gira(esito):
    print("### IL RESPIRO SULLA CARTA (csv/solitone/respiro.py): PASSO %g N_TICK %d PERIODO_PROVA %g OGNI_RADO %d TOLL_FREQ %g TOLL_SOMMA %g FRAZIONE %g FRAZIONE_F %g SEME %d SIGNIF %g TOLL_QUOTA %g; PERIODI_MIN %d"
          % (PASSO, N_TICK, PERIODO_PROVA, OGNI_RADO, TOLL_FREQ, TOLL_SOMMA, FRAZIONE, FRAZIONE_F, SEME, SIGNIF, TOLL_QUOTA, RE.PERIODI_MIN))
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
    ff = (1.0 / PERIODO_PROVA, 1.0 / 0.99, 1.0 / 19.5)
    y3 = 0.59 + 1e-5 * t + 2e-3 * np.cos(2.0 * math.pi * ff[0] * t) + 0.3e-3 * np.cos(2.0 * math.pi * ff[1] * t + 1.1) + 0.1e-3 * np.cos(2.0 * math.pi * ff[2] * t + 2.3)
    r3 = RE.omega(y3, PASSO, None)
    e3 = RE.elenco(r3, FRAZIONE, 1)
    trovati = [any(abs(p["frequenza"] - f) <= r3["canale"] for p in e3) for f in ff]     # ### entro 1 canale: con tre seni il fit di uno alla volta sente gli altri
    doppi = any(abs(p["frequenza"] - q["frequenza"]) <= r3["canale"] for i, p in enumerate(e3) for q in e3[i + 1:])
    esito("DEVE PASSARE: R4 elenco a %g (primi 1) su tre seni di ampiezza 1, 0.15, 0.05: i primi due entro 1 canale, non il terzo, nessun doppione" % FRAZIONE,
          trovati == [True, True, False] and not doppi, "%d picchi nell'elenco (%d massimi rifiniti): %s" % (len(e3), len(r3["picchi"]), " ".join("%.4f" % p["periodo"] for p in e3)))
    eF = RE.elenco(r3, FRAZIONE_F, 1)
    esito("DEVE FALLIRE: R4-F elenco a %.4f NON contiene il terzo seno (periodo 19.5)" % FRAZIONE_F, any(abs(p["frequenza"] - ff[2]) <= r3["canale"] for p in eF),
          "%d picchi: %s" % (len(eF), " ".join("%.4f" % p["periodo"] for p in eF)))
    rng = np.random.default_rng(SEME)
    rum = 1e-3 * rng.standard_normal(N_TICK)
    s1, a1, q1 = RE.presenza(0.59 + rum + 0.3e-3 * np.cos(2.0 * math.pi * ff[1] * t), PASSO, ff[1])
    s0, a0, _q0 = RE.presenza(0.59 + rum, PASSO, ff[1])
    esito("DEVE PASSARE: R5 presenza: un seno di ampiezza 3e-4 nel rumore gaussiano di sigma 1e-3 ha significativita' >= %g" % SIGNIF, s1 >= SIGNIF, "significativita' %.2f, ampiezza %.3e, quota %.4f" % (s1, a1, q1))
    esito("DEVE FALLIRE: R5-F presenza: sul solo rumore la significativita' alla stessa frequenza e' >= %g" % SIGNIF, not s0 >= SIGNIF, "significativita' %.2f, ampiezza %.3e" % (s0, a0))
    _sp, ap, qp = RE.presenza(y, PASSO, f0)
    _sq, _aq, qq = RE.presenza(0.59 + rum + 0.3e-3 * np.cos(2.0 * math.pi * ff[1] * t), PASSO, ff[1])
    qa = 0.5 * 0.3e-3 ** 2 / (1e-6 + 0.5 * 0.3e-3 ** 2)
    esito("DEVE PASSARE: R5-Q la quota: il seno puro di R1 ha quota 1 entro %g; il seno di R5 nel rumore ha quota a^2/2/(sigma^2 + a^2/2) = %.4f entro un fattore 2" % (TOLL_QUOTA, qa),
          abs(qp - 1.0) <= TOLL_QUOTA and 0.5 * qa <= qq <= 2.0 * qa, "seno puro %.6f (ampiezza %.6e); nel rumore %.4f" % (qp, ap, qq))
