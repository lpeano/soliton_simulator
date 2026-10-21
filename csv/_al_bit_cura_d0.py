# -*- coding: utf-8 -*-
r"""**LA CURA DI `D0` AL BIT, sul referto della base proiettata** *(`594417f6`)*.

> ### ⛔ **Il task history e' `2026-10-21_regressione_d0.md`** *(annotazione `4-bis`, `8a5855ab`)*:
> ### **a campione, `594417f6` `R2` a lato `32`**, identico al bit. ### **Una misura: nessun file
> del nucleo si tocca.** Si rigira `braccio_proiettato` di `csv/_stabilita_lineare.py` ### **con gli
> stessi argomenti di `main_proiettata`**, e si confronta ### **col `jsonl` committato a `594417f6`**
> *(letto con `git show`, non dal disco: il disco puo' essere stato riscritto)*.

## ⚠ PERCHE' ANCHE `R1`
### **`R2` gira con `cs` SPENTO** *(`acceso False`)*: `energia_pesata.applica` ### **esce alla prima
guardia**, e la cura non puo' toccarlo per costruzione. ### **`R1` lato `32` ha `cs` ACCESO**: ### **e'
il caso in cui il punto fisso di `Omega` gira davvero**, quindi il confronto che conta.

## IL CRITERIO
### **AL BIT** `gamma`, `gamma_meta`, `quarti`, le quattro `pend`, `uniformita_ulp`, `cs_m`, `N`.
### **Un solo valore diverso: STOP**, e la domanda a Luca.

Gira con:  python csv/_al_bit_cura_d0.py
"""
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

COMMIT = "594417f6"
PERCORSO = "doc/referti_l2/stabilita_base_proiettata.jsonl"
CAMPI = ("gamma", "gamma_meta", "quarti", "uniformita_ulp", "cs_m", "N")
BRACCI = (("R2 lato 32", False), ("R1 lato 32", True))


def committato():
    testo = subprocess.check_output(["git", "show", "%s:%s" % (COMMIT, PERCORSO)], cwd=RADICE)
    righe = [json.loads(r) for r in testo.decode("utf-8").splitlines() if r.strip()]
    return {r["nome"]: r for r in righe}


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _stabilita_lineare as SL
    print("=" * 100)
    print("LA CURA DI D0 AL BIT, sul referto della base proiettata (%s)" % COMMIT)
    print("=" * 100)
    print("  braccio_proiettato(nome, 32, 0.125, X %g, acceso, (), EPS_REL %g, TEMPO_LUNGO %g),"
          " gli argomenti di main_proiettata" % (SL.X, SL.EPS_REL, SL.TEMPO_LUNGO))
    print("-" * 100)
    sys.stdout.flush()
    vecchi = committato()
    ok = [0, 0]
    for nome, acceso in BRACCI:
        b = SL.braccio_proiettato(nome, 32, 0.125, SL.X, acceso, (), SL.EPS_REL, SL.TEMPO_LUNGO)
        v = vecchi[nome]
        assert v["acceso"] == acceso and v["fine"] == "N" and b["fine"] == "N", nome
        diversi = [c for c in CAMPI if not np.array_equal(np.asarray(b[c]), np.asarray(v[c]))]
        diversi += ["pend." + k for k in v["pend"]
                    if not np.array_equal(np.asarray(b["pend"][k]), np.asarray(v["pend"][k]))]
        ok[1] += 1
        ok[0] += int(not diversi)
        print("  [%s] %s (cs %s): %d campi confrontati AL BIT -- %s"
              % ("PASSA" if not diversi else "FALLISCE", nome, "acceso" if acceso else "spento",
                 len(CAMPI) + len(v["pend"]),
                 "tutti identici" if not diversi else "### DIVERSI: %s" % ", ".join(diversi)))
        print("      gamma max %.17g   uniformita' %.3f ulp   %.0f s"
              % (float(np.max(b["gamma"])), b["uniformita_ulp"], b["secondi"]))
        sys.stdout.flush()
    print("=" * 100)
    print("LA CURA AL BIT: %d su %d   %s" % (ok[0], ok[1], "### TUTTI IDENTICI" if ok[0] == ok[1]
                                             else "### STOP: UN VALORE FISICO E' CAMBIATO"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
