# -*- coding: utf-8 -*-
r"""**[M2330] IL MODELLO INTERO, LA V3: U RISCRITTO DOPO I PARAMETRI** *(la v2 fallì K1: con `kappa 0` il tick non rifa' la tenuta del giro 4; la causa candidata: `chi_parametri_v2.parametri_v2` chiama `Z["metti"](stato)`, che rimette il motore della scena e perde i link `U` scritti da `fondo_suite_v2.carica` con `U1.scrivi_U` quando `A != 0`; `due_corpi_fondo.py` e `_v2` sono usati e non si riscrivono; la carta sez. `3-quattuordecies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v3.py noto > doc/referti_l2/due_corpi_fondo_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v3.py corsa --quale d1      (d1, d2, d3: dalla coda)

**Una differenza in piu', in memoria:** `parametri` riscrive `U` dal campo *(`_u1_prototipo.scrivi_U(mot, C.campo)`, come `fondo_suite_v2.carica`)* dopo `gravita_due_corpi.parametri`. **Il resto:** la v2 cosi' com'e'.
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v2 as D2  # noqa: E402

D = D2.D
_parametri = D.parametri
_avvia = D.avvia


def avvia():
    import _presidio
    _avvia()
    _presidio.avvia(__file__)


def parametri(Z, C, chi_on):
    import _u1_prototipo as U1
    r = _parametri(Z, C, chi_on)
    U1.scrivi_U(Z["mot"], C.campo)
    return r


D.avvia = avvia
D.parametri = parametri

if __name__ == "__main__":
    sys.exit(D.main(sys.argv[1:]))
