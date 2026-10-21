# -*- coding: utf-8 -*-
r"""**IL FATTORE DI CONTRAZIONE DEL PUNTO FISSO DI `Omega`, sulla scena di `D0`, a piu' `dtau`.**

> ### ⛔ **Il task history e' `2026-10-21_regressione_d0.md`** *(annotazione `4-bis`, `8a5855ab`)*.
> ### **Una misura: nessun file del nucleo si tocca.** Si ripete il braccio `braccio_accesa` di
> `primo_ordine/_collauda_cs.py` *(`TICK` tick, `accendi_cs(LC_DI_PROVA)` prima di ogni tick)*, ###
> **cambiando SOLO il `dtau` della scena**; `energia_pesata.applica` si avvolge, ### **SOLO IN
> MEMORIA**, con una funzione che chiama l'ORIGINALE e poi ### **legge** `mot.giri_omega` e
> `mot.fattore_omega` *(nessuna copia del ciclo)*.

## I CONTROLLI
- ### **DEVE RIUSCIRE:** a `dtau = DTAU` del collaudo, ### **entrambe le scene di `D0` convergono**
  coi giri stampati.
- ### **DEVE FALLIRE:** con `GIRI_MAX_OMEGA = 120` *(in memoria)*, ### **la scena `(16, 7)` ALZA.**
- ### **IL CONTATORE E' QUELLO CHE DICE:** `mot.avvisi_omega` ### **uguale** alle chiamate col
  fattore oltre `SOGLIA_AVVISO_OMEGA`, contate qui.

## LA MISURA
Il fattore a `dtau` `0.5`, `1`, `1.25`, `1.5`: medio e massimo, ### **e se a qualche `dtau` non converge
entro `GIRI_MAX_OMEGA` giri** *(non e' un errore della misura: si dice)*.

Gira con:  python csv/_fattore_omega.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

JSONL = os.path.join(RADICE, "doc", "referti_l2", "fattore_omega.jsonl")
DTAU_MISURA = (0.5, 1.0, 1.25, 1.5)


def corsa(CC, DV, EP, FP, TK, nn, seme, dtau):
    """`CC.TICK` tick col `cs` acceso; ### le chiamate di `applica` registrate dal motore."""
    vero = EP.applica
    chiamate = []

    def avvolta(mot, st, par, frazione):
        r = vero(mot, st, par, frazione)
        if mot.cs is not None and mot.lambda_c is not None:
            chiamate.append((mot.giri_omega, mot.fattore_omega))
        return r
    EP.applica = avvolta
    alzato, tick_alza, mot = None, None, None
    try:
        _i, mot, st, par = DV.scena(nn, seme, dtau, norma="locale",
                                    vuoto_modulo=CC.VUOTO_MODULO, su2=True)
        for t in range(CC.TICK):
            FP.accendi_cs(mot, CC.LC_DI_PROVA, st)
            TK.tick(st, mot, par)
    except AssertionError as e:
        alzato, tick_alza = str(e), t
    finally:
        EP.applica = vero
    return chiamate, alzato, tick_alza, mot


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _collauda_cs as CC
    import deriva as DV
    import energia_pesata as EP
    import flussi_parziali as FP
    import tick as TK
    print("=" * 100)
    print("IL FATTORE DI CONTRAZIONE DEL PUNTO FISSO DI Omega, sulla scena di D0")
    print("=" * 100)
    print("  braccio_accesa di _collauda_cs.py: LC_DI_PROVA %g, TICK %d, VUOTO_MODULO %g, DTAU del"
          " collaudo %g; GIRI_MAX_OMEGA %d, SOGLIA_AVVISO_OMEGA %g"
          % (CC.LC_DI_PROVA, CC.TICK, CC.VUOTO_MODULO, CC.DTAU, EP.GIRI_MAX_OMEGA,
             EP.SOGLIA_AVVISO_OMEGA))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    ok = [0, 0]

    def esito(che, passa, nota):
        ok[1] += 1
        ok[0] += int(bool(passa))
        print("  [%s] %s -- %s" % ("PASSA" if passa else "FALLISCE", che, nota))
        sys.stdout.flush()

    righe = []
    for dtau in DTAU_MISURA:
        for nn, seme in CC.SCENE:
            ch, alzato, tick_alza, mot = corsa(CC, DV, EP, FP, TK, nn, seme, dtau)
            g = np.array([c[0] for c in ch], dtype=float)
            f = np.array([c[1] for c in ch], dtype=float)
            oltre = int(np.sum(f > EP.SOGLIA_AVVISO_OMEGA))
            r = {"dtau": dtau, "nn": nn, "seme": seme, "chiamate": len(ch),
                 "giri_max": int(g.max()) if g.size else None,
                 "giri_medio": float(g.mean()) if g.size else None,
                 "fattore_medio": float(f.mean()) if f.size else None,
                 "fattore_max": float(f.max()) if f.size else None,
                 "oltre_soglia": oltre, "avvisi_omega": int(mot.avvisi_omega) if mot else None,
                 "fattore_omega_max": float(mot.fattore_omega_max) if mot else None,
                 "alza": alzato, "tick_alza": tick_alza}
            righe.append(r)
            print("  dtau %-5g nn=%-3d seme=%-3d  chiamate %4d  giri medio %7.2f max %4s  fattore"
                  " medio %.4f max %.4f  oltre %g: %d (contatore %s)  %s"
                  % (dtau, nn, seme, len(ch), r["giri_medio"] or 0, r["giri_max"],
                     r["fattore_medio"] or 0, r["fattore_max"] or 0, EP.SOGLIA_AVVISO_OMEGA,
                     oltre, r["avvisi_omega"],
                     ("### NON CONVERGE entro %d giri, al tick %d" % (EP.GIRI_MAX_OMEGA, tick_alza))
                     if alzato else "converge in tutti i %d tick" % CC.TICK))
            with io.open(JSONL, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r) + "\n")
            sys.stdout.flush()
    print("-" * 100)
    d0 = [r for r in righe if r["dtau"] == CC.DTAU]
    esito("### DEVE RIUSCIRE: a dtau %g le scene di D0 convergono" % CC.DTAU,
          all(r["alza"] is None for r in d0),
          "giri max %s" % ", ".join("(%d,%d) %s" % (r["nn"], r["seme"], r["giri_max"]) for r in d0))
    esito("### IL CONTATORE: mot.avvisi_omega = le chiamate oltre soglia contate qui",
          all(r["avvisi_omega"] == r["oltre_soglia"] for r in righe),
          "su %d corse" % len(righe))
    ufficiale = EP.GIRI_MAX_OMEGA
    EP.GIRI_MAX_OMEGA = 120
    try:
        _ch, alzato, tick_alza, _m = corsa(CC, DV, EP, FP, TK, 16, 7, CC.DTAU)
    finally:
        EP.GIRI_MAX_OMEGA = ufficiale
    esito("### DEVE FALLIRE: con GIRI_MAX_OMEGA 120 la scena (16, 7) ALZA",
          alzato is not None,
          ("al tick %d: %s" % (tick_alza, alzato[:90])) if alzato else "### NON ALZA")
    print("=" * 100)
    print("IL FATTORE DI Omega: %d su %d   %s" % (ok[0], ok[1], "### TUTTI PASSATI"
                                                   if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
