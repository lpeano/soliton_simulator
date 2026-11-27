# -*- coding: utf-8 -*-
r"""**[M2330] IL MODELLO INTERO, LA V2: IL NUCLEO PRESO PRIMA DELLA SCENA** *(`due_corpi_fondo.py noto` cadde: `torneo_tenuta.nucleo()` chiamato dentro `TC.scena()`, dove `pezzi` e' gia' avvolto; errore mio; quello script e' usato e non si riscrive; la carta sez. `3-quattuordecies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v2.py noto > doc/referti_l2/due_corpi_fondo_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v2.py corsa --quale d1      (d1, d2, d3: dalla coda)

**Due differenze, in memoria:** `avvia` prende anche `MV, P0 = torneo_tenuta.nucleo()`, prima della scena *(come `fondo_1c.caduta`)*; `ciclo` usa quelli. **Il resto:** `due_corpi_fondo` cosi' com'e'.
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo as D  # noqa: E402

F1, CV2 = D.F1, D.CV2
NUC = []
_avvia = D.avvia


def avvia():
    import _presidio
    _avvia()
    _presidio.avvia(__file__)
    NUC[:] = list(F1.TT.nucleo())


def ciclo(Z, C, P, Lp, X, quanti, dopo):
    """### `due_corpi_fondo.ciclo` riga per riga, con `MV, P0` presi prima della scena."""
    import ripresa_F0_v2 as RF
    MV, P0 = NUC
    _G20, _ia, _e0, MT = F1.CL.parametri()
    with RF.col_nucleo(MV, P0), MV.forma_esplicita(F1.FORMA_OGG):
        assert MV.ATTIVA == F1.FORMA_OGG and MV.pezzi is P0
        for kk in range(1, quanti + 1):
            prima = Z["st"]["psi_h"].copy()
            CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)
            if kk % MT.OGNI_GAUSS == 0:
                C.residuo()
            dopo(kk, prima)


D.avvia = avvia
D.ciclo = ciclo

if __name__ == "__main__":
    sys.exit(D.main(sys.argv[1:]))
