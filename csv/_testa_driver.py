# -*- coding: utf-8 -*-
"""LA TESTA DEL DRIVER, eseguita fino a `_applica_flag` -- **UN POSTO SOLO**.

`P1-ter`: l'argv del driver **non si ricopia a mano**. E ricostruirla sarebbe **una SECONDA
formula per la stessa cosa**, che e' l'errore che questo repo insegue: si **ESEGUE** la testa
del driver vero e si prende `sys.argv` come l'ha lasciata lui.

**COSA FA:** esegue `csv/_test_fork/_scena_video.py` **fino all'ancora `S._applica_flag(a)`
inclusa** -- quindi legge le opzioni, costruisce l'argv del simulatore, importa il simulatore e
gli applica i flag -- e **si ferma li'**: nessuna scena, nessun passo.

**L'ancora si cerca nel TESTO INTERO** *(`STANDARD 9`)* e **deve essere unica**.

⚠ **NON E' UN PRESIDIO:** chi vuole puo' sempre costruirsi un'argv sua. E' **l'unico posto in
cui questa idea e' scritta**, cosi' se cambia, cambia una volta.
⚠ `csv/_seal_fork/_sigillo_driver_accende.py` ha ancora la **sua copia** di questa idea: va
   migrata qui. **In coda.**

ASCII puro.
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
ANCORA = "S._applica_flag(a)"


def esegui(dest, extra=None):
    """Esegue la testa del driver. Torna `(modulo_simulatore, argv_del_simulatore, globali)`.

    `dest`  la destinazione posizionale che il driver si aspetta (non ci scrive nulla: la
            testa si ferma prima).
    `extra` opzioni NOMINALI da passare AL DRIVER (es. `--scala-min-passo=off`, `--sep=8`).
    """
    os.chdir(RADICE)
    t = io.open(DRIVER, encoding="utf-8").read()
    assert t.count(ANCORA) == 1, "ancora non unica nel driver: %d" % t.count(ANCORA)
    testa = t[:t.index(ANCORA) + len(ANCORA)] + "\n_ARGV_SIM = list(sys.argv)\n"
    g = {"__name__": "__main__", "__file__": DRIVER}
    vecchio = list(sys.argv)
    sys.argv = ["_scena_video.py", "1", dest] + list(extra or [])
    try:
        exec(compile(testa, DRIVER, "exec"), g)
    finally:
        sys.argv = vecchio
    S = g.get("S") or sys.modules["soliton_simulator"]
    return S, g.get("_ARGV_SIM") or [], g
