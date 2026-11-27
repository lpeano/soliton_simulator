# -*- coding: utf-8 -*-
r"""**[M1016] LA CORSA LUNGA d1'', v8: IL CICLO VERO (QUELLO DELLA v2)** *(DECISIONE DI LUCA, 2026-11-27 `10:16`; la carta `doc/CARTA_fondo_giusto.md`, il seguito [M1016]; `due_corpi_fondo_v7.py` e' usato e non si riscrive: cadde su `torneo_tenuta.nucleo()` dentro la scena, `0cc00fab`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v8.py noto > doc/referti_l2/due_corpi_fondo_v8_noto.txt      (K0', K0'-neg)
    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v8.py corsa       (d1'': da stato_006000 a k 18000; dalla coda)

**L'unica differenza dalla v7, in memoria:** `Ripresa.gira` chiama **`D.ciclo`**, cioe' il ciclo della v2 *(il nucleo preso in `D.avvia`, PRIMA della scena: la via con cui e' girata d1')*, con un `dopo` che porta il tick relativo `kk` a quello assoluto `k_da + kk`. **`C.residuo`** cade a `kk % 250 == 0`, che e' lo stesso tick assoluto perche' `k_da % 250 == 0` *(asserito)*. **Il resto** *(la carica, la misura, K0', K0'-neg, la corsa, `M2034/coppia/d1L`)* e' quello della v7.
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v7 as V7  # noqa: E402

D = V7.D
assert D.ciclo.__module__ == "due_corpi_fondo_v2", "D.ciclo NON e' quello della v2: %s" % D.ciclo.__module__
_avvia7 = V7.avvia


def avvia():
    import _presidio
    _avvia7()
    _presidio.avvia(os.path.join(_QUI, "due_corpi_fondo_v2.py"))
    _presidio.avvia(__file__)


def gira(self, ticks, dopo_extra=None):
    """### `D.ciclo` (la v2) per `ticks` tick; il `dopo` col tick ASSOLUTO `k_da + kk`."""
    assert self.k_da % 250 == 0
    k_da = self.k_da

    def dopo(kk, prima):
        ka = k_da + kk
        for j, ms in enumerate(self.maschere):
            self.om[j].append(float(-V7.np.angle(V7.np.vdot(prima[ms], self.Z["st"]["psi_h"][ms]))))
        if ka % V7.OGNI_SERIE == 0:
            self.serie.append(self.misura(ka))
        if dopo_extra is not None:
            dopo_extra(ka)
    D.ciclo(self.Z, self.C, self.P, self.Lp, self.X, ticks, dopo)


V7.avvia = avvia
V7.Ripresa.gira = gira

if __name__ == "__main__":
    sys.exit(V7.main(sys.argv[1:]))
