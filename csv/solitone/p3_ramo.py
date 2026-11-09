# -*- coding: utf-8 -*-
r"""**P3, LA PROVA DEL DIVIETO DI `cs` SUL PRINCIPALE** *(il task history del prototipo, sez. `20`)*. [[H-NUCLEO-CONGELATO]]

    python csv/solitone/p3_ramo.py > doc/referti_l2/p3_ramo.txt

**I DEVE:** `P3-D` *(sul principale, `cs` acceso: `energia_pesata.applica` ALZA)*; `P3-0` *(a `cs` spento chiama la vera, che ritorna lo stato: il braccio `0`)*;
`P3-F` *(DEVE FALLIRE: la decisione pura col ramo `zero-nel-nucleo` vieta)*; `P3-S` *(la decisione pura col principale SBLOCCATO non vieta)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi, e vieta_cs all'import)

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


class Finto(object):
    def __init__(self, cs, lc):
        self.cs, self.lambda_c = cs, lc


def main():
    import _presidio
    import energia_pesata as EP
    from solitone import ramo as R
    _presidio.avvia(os.path.join(_QUI, "ramo.py"))
    _presidio.avvia(os.path.join(_QUI, "__init__.py"))
    _presidio.avvia(__file__)
    ramo, testo = R.stato_del_repo()
    print("=" * 130)
    print("P3, IL DIVIETO DI cs SUL PRINCIPALE: il ramo %r; NUCLEO_CONGELATO %s; il divieto attivo: %s" % (ramo, "presente" if testo is not None else "assente", R.ATTIVO[0]))
    print("=" * 130)
    st = {"x": np.zeros(3)}
    try:
        EP.applica(Finto(np.ones(3), 34.0), st, None, 0.5)
        alza, msg = False, "non alza"
    except R.CsVietatoSulPrincipale as e:
        alza, msg = True, str(e)[:90]
    esito("P3-D sul principale, cs acceso (mot.cs e mot.lambda_c non None): energia_pesata.applica ALZA", alza and ramo == "primo-ordine", msg)
    out = EP.applica(Finto(None, None), st, None, 0.5)
    esito("P3-0 a cs spento la vera energia_pesata.applica ritorna lo stato, senza alzare (il braccio 0)", out is st, "")
    esito("P3-F la decisione pura col ramo zero-nel-nucleo e lo stato CONGELATO: vieta", R.decidi("zero-nel-nucleo", "stato: CONGELATO\n"), "", deve=False)
    esito("P3-S la decisione pura col principale SBLOCCATO (con la decisione di Luca): non vieta", not R.decidi("primo-ordine", "stato: SBLOCCATO\ndecisione_di_luca: x\n"), "")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
