# -*- coding: utf-8 -*-
r"""**L'AVVISO DI CONVERGENZA LENTA SUI GIRI: dove deve scattare, e dove deve restare zero.**

> ### ⛔ **Il task history e' `2026-10-21_regressione_d0.md`** *(annotazione `4-ter`, `dffb2fb7`)*.
> ### **Una misura: nessun file del nucleo si tocca.** `energia_pesata.applica` si avvolge, ###
> **SOLO IN MEMORIA**, con una funzione che chiama l'ORIGINALE e poi ### **legge** `mot.giri_omega`
> e `mot.avvisi_omega` *(nessuna copia del ciclo)*.

## I CONTROLLI
- ### **DEVE RIUSCIRE:** `D0` *(`braccio_accesa` di `primo_ordine/_collauda_cs.py`, `dtau 1`)* ###
  **produce almeno `1` avviso.**
- ### **DEVE RESTARE `0`:** `R1` di `594417f6` a lato `32` *(`braccio_proiettato`, `cs` acceso)* e
  ### **`C1` di strada `(d)`** *(`braccio_c1` di `primo_ordine/_misura_strada_d.py`)*.
- ### **IL CONTATORE:** la somma di `mot.avvisi_omega` sui motori ### **uguale** alle chiamate con
  `giri > GIRI_AVVISO_OMEGA` contate qui.
- ### **AL BIT:** `R1` coi `10` campi del `jsonl` di `594417f6` *(come `csv/_al_bit_cura_d0.py`)*, e ###
  **l'uscita di `braccio_c1` contenuta riga per riga in `doc/referti_l2/c1_tetto_omega.txt`.**

Gira con:  python csv/_avviso_giri.py
"""
import contextlib
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

C1_REFERTO = os.path.join(RADICE, "doc", "referti_l2", "c1_tetto_omega.txt")


def con_registro(EP, fai):
    """### Esegue `fai()` con `applica` avvolta: ### **i giri di ogni chiamata, e i motori visti.**"""
    vero = EP.applica
    giri, motori = [], {}

    def avvolta(mot, st, par, frazione):
        r = vero(mot, st, par, frazione)
        if mot.cs is not None and mot.lambda_c is not None:
            giri.append(mot.giri_omega)
            motori[id(mot)] = mot
        return r
    EP.applica = avvolta
    try:
        uscita = fai()
    finally:
        EP.applica = vero
    avvisi = sum(int(m.avvisi_omega) for m in motori.values())
    oltre = sum(int(g > EP.GIRI_AVVISO_OMEGA) for g in giri)
    return uscita, giri, avvisi, oltre


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _al_bit_cura_d0 as AB
    import _collauda_cs as CC
    import _misura_strada_d as SD
    import _stabilita_lineare as SL
    import energia_pesata as EP
    print("=" * 100)
    print("L'AVVISO DI CONVERGENZA LENTA SUI GIRI: oltre GIRI_AVVISO_OMEGA = %d (GIRI_MAX_OMEGA %d)"
          % (EP.GIRI_AVVISO_OMEGA, EP.GIRI_MAX_OMEGA))
    print("=" * 100)
    sys.stdout.flush()
    ok = [0, 0]

    def esito(che, passa, nota):
        ok[1] += 1
        ok[0] += int(bool(passa))
        print("  [%s] %s -- %s" % ("PASSA" if passa else "FALLISCE", che, nota))
        sys.stdout.flush()

    def riga(nome, giri, avvisi, oltre):
        print("  %-34s chiamate %5d  giri max %4d  oltre %d: %d  mot.avvisi_omega %d"
              % (nome, len(giri), max(giri) if giri else 0, EP.GIRI_AVVISO_OMEGA, oltre, avvisi))
        sys.stdout.flush()

    # ### D0
    tot_d0, coerente = 0, True
    for nn, seme in CC.SCENE:
        _u, g, a, o = con_registro(EP, lambda: CC.corri(nn, seme, CC.LC_DI_PROVA))
        riga("D0 dtau %g scena (%d, %d)" % (CC.DTAU, nn, seme), g, a, o)
        tot_d0 += a
        coerente &= a == o
    esito("### DEVE RIUSCIRE: D0 (braccio_accesa) produce almeno 1 avviso", tot_d0 >= 1,
          "%d avvisi sulle due scene" % tot_d0)
    # ### R1 di 594417f6
    vecchi = AB.committato()
    b, g, a, o = con_registro(EP, lambda: SL.braccio_proiettato(
        "R1 lato 32", 32, 0.125, SL.X, True, (), SL.EPS_REL, SL.TEMPO_LUNGO))
    riga("R1 lato 32 (594417f6)", g, a, o)
    coerente &= a == o
    esito("### DEVE RESTARE 0: R1 di 594417f6 a lato 32", a == 0 and len(g) > 0,
          "%d avvisi su %d chiamate" % (a, len(g)))
    v = vecchi["R1 lato 32"]
    diversi = [c for c in AB.CAMPI if not np.array_equal(np.asarray(b[c]), np.asarray(v[c]))]
    diversi += ["pend." + k for k in v["pend"]
                if not np.array_equal(np.asarray(b["pend"][k]), np.asarray(v["pend"][k]))]
    esito("### AL BIT: R1 lato 32 contro il jsonl di 594417f6", not diversi,
          "tutti identici" if not diversi else "### DIVERSI: %s" % ", ".join(diversi))
    # ### C1 di strada (d)
    buf = io.StringIO()

    def c1():
        with contextlib.redirect_stdout(buf):
            return SD.braccio_c1()
    _u, g, a, o = con_registro(EP, c1)
    riga("C1 di strada (d)", g, a, o)
    coerente &= a == o
    esito("### DEVE RESTARE 0: C1 di strada (d)", a == 0 and len(g) > 0,
          "%d avvisi su %d chiamate" % (a, len(g)))
    vecchio = set(io.open(C1_REFERTO, encoding="utf-8").read().splitlines())
    nuove = [r for r in buf.getvalue().splitlines() if r.strip()]
    mancano = [r for r in nuove if r not in vecchio]
    esito("### AL BIT: l'uscita di braccio_c1 sta riga per riga in c1_tetto_omega.txt",
          nuove and not mancano,
          "%d righe, %d mancanti%s" % (len(nuove), len(mancano),
                                       (": " + mancano[0][:80]) if mancano else ""))
    esito("### IL CONTATORE: mot.avvisi_omega = le chiamate oltre soglia contate qui", coerente,
          "su 4 corse")
    print("=" * 100)
    print("L'AVVISO SUI GIRI: %d su %d   %s" % (ok[0], ok[1], "### TUTTI PASSATI"
                                                if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
