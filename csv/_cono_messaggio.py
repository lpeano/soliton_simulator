# -*- coding: utf-8 -*-
r"""**`[[CONO-MESSAGGIO-ROTTO]]`: il rifiuto del cono esce come `AssertionError`, col messaggio giusto.**

> ### ⛔ **Il task history e' `2026-10-21_regressione_d0.md`** *(annotazione `4-ter`, `dffb2fb7`)*.
> Si ripete ### **la scena di `a688c219` fuori dal cono**: `braccio_accesa` di
> `primo_ordine/_collauda_cs.py` *(`accendi_cs(LC_DI_PROVA)` prima di ogni tick)* a ### **`dtau 1.25`**,
> scena `(16, 7)`, ### **senza nessuna guardia dello strumento**: il rifiuto deve venire dal nucleo.

## I CONTROLLI
- ### **DEVE RIUSCIRE:** alza ### **`AssertionError`** *(non `TypeError`)*, ### **col messaggio che
  porta `dove` e il valore di `s`**, e ### **al tick dove `a688c219` diceva FUORI DAL CONO** *(`18`)*.
- ### **E IL VALORE STAMPATO E' QUELLO VERO:** `s` nel messaggio uguale a `max(dtau_nodo) / dtau_rif`
  calcolato qui prima del tick *(`1.023501` in `a688c219`)*.
- ### **DEVE NON ALZARE:** a `dtau 1`, la scena di `D0`, `TICK` tick: dentro il cono nessun rifiuto.

Gira con:  python csv/_cono_messaggio.py
"""
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

DTAU_FUORI = 1.25
TICK_ATTESO = 18
_S = re.compile(r"un `s` del (\w+) vale ([0-9.eE+-]+) > 1")


def corsa(CC, DV, FP, TK, dtau):
    """`CC.TICK` tick col `cs` acceso; ### l'eccezione che esce, il tick, e `s` prima del tick."""
    _i, mot, st, par = DV.scena(16, 7, dtau, norma="locale", vuoto_modulo=CC.VUOTO_MODULO,
                                su2=True)
    s_prima = None
    for t in range(CC.TICK):
        FP.accendi_cs(mot, CC.LC_DI_PROVA, st)
        s_prima = float(np.max(FP.dtau_nodo(mot))) / float(FP.dtau_rif(mot))
        try:
            TK.tick(st, mot, par)
        except Exception as e:                                # noqa: BLE001
            return e, t, s_prima
    return None, None, s_prima


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _collauda_cs as CC
    import deriva as DV
    import flussi_parziali as FP
    import tick as TK
    print("=" * 100)
    print("CONO-MESSAGGIO-ROTTO: il rifiuto del cono, dal nucleo, a dtau %g (scena (16, 7) di D0)"
          % DTAU_FUORI)
    print("=" * 100)
    ok = [0, 0]

    def esito(che, passa, nota):
        ok[1] += 1
        ok[0] += int(bool(passa))
        print("  [%s] %s -- %s" % ("PASSA" if passa else "FALLISCE", che, nota))
        sys.stdout.flush()

    e, t, s_prima = corsa(CC, DV, FP, TK, DTAU_FUORI)
    print("  eccezione: %s al tick %s" % (type(e).__name__ if e else "NESSUNA", t))
    print("  messaggio: %s" % (str(e) if e else "-"))
    m = _S.search(str(e)) if e else None
    esito("### DEVE RIUSCIRE: AssertionError (non TypeError), al tick %d" % TICK_ATTESO,
          isinstance(e, AssertionError) and t == TICK_ATTESO,
          "%s al tick %s" % (type(e).__name__ if e else "nessuna", t))
    esito("### il messaggio porta dove e s", m is not None,
          ("dove = %s, s = %s" % (m.group(1), m.group(2))) if m else "### non li porta")
    esito("### e s nel messaggio e' quello vero (max dtau_nodo / dtau_rif prima del tick)",
          m is not None and float(m.group(2)) == s_prima,
          "%s contro %.17g" % (m.group(2) if m else "-", s_prima))
    e1, t1, _s1 = corsa(CC, DV, FP, TK, CC.DTAU)
    esito("### DEVE NON ALZARE: a dtau %g, dentro il cono, %d tick" % (CC.DTAU, CC.TICK),
          e1 is None, "nessuna eccezione" if e1 is None else "%s al tick %d" % (type(e1).__name__, t1))
    print("=" * 100)
    print("IL MESSAGGIO DEL CONO: %d su %d   %s" % (ok[0], ok[1], "### TUTTI PASSATI"
                                                   if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
