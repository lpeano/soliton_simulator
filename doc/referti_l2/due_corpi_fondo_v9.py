# -*- coding: utf-8 -*-
r"""**[M1107] LA CORSA LUNGA d1'', v9: U RIFATTA DOPO LA CARICA (IL TENTATIVO 1 SU 2)** *(DECISIONE DI LUCA, 2026-11-27 `11:07` e `11:44`; la relazione, B5b, `b1a22f1c`; `due_corpi_fondo_v8.py` e' usato e non si riscrive: K0' fallisce, `755a781c`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v9.py noto > doc/referti_l2/due_corpi_fondo_v9_noto.txt      (K0', K0'-neg)
    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v9.py corsa       (d1'': da stato_006000 a k 18000; dalla coda)

**L'unica differenza dalla v8, in memoria:** dopo la carica dello stato *(`Ripresa.__init__` della v7)*, **`scrivi_U(mot, C.campo)`**, cioe' `U[:,0,0] = U[:,1,1] = exp(i e A)` con la `A` appena caricata. E' la `U` che la corsa continua ha alla fine di ogni tick *(B5: `mot.geo.U` era l'unica voce di stato diversa dopo la ricarica)*. **`scrivi_U` e' quella del modulo che usa il passo** *(`solitone._u1_oggi.U1`, cioe' `_u1_prototipo`)*. Il nucleo non si tocca. **Il resto** *(K0', K0'-neg, la corsa, `M2034/coppia/d1L`)* e' quello della v7 e della v8.
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v8 as V8  # noqa: E402

V7 = V8.V7
_init7 = V7.Ripresa.__init__
_avvia8 = V7.avvia


def avvia():
    import _presidio
    _avvia8()
    _presidio.avvia(__file__)


def init(self, Z, k_da, campo_E=True):
    from solitone import _u1_oggi as UO
    _init7(self, Z, k_da, campo_E)
    UO.U1.scrivi_U(Z["mot"], self.C.campo)


V7.avvia = avvia
V7.Ripresa.__init__ = init

if __name__ == "__main__":
    sys.exit(V7.main(sys.argv[1:]))
