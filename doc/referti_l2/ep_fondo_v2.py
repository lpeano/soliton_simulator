# -*- coding: utf-8 -*-
r"""**[M1330-F] E(p) -- LA V2 DEL CALCIO** *(`ep_fondo.py` cadde: le corse fecero i `1000` tick e poi caddero salvando lo stato finale, perche' la cartella `M1330/ep/k<k>` nasce DOPO, in `fondo_1c.scrivi`; errore mio; la carta sez. `4-ter`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/ep_fondo_v2.py calcio --k 0.1        (k 0, 0.01, ..., 0.5: 1000 tick)
    E:\python\py3132\python.exe doc/referti_l2/ep_fondo.py lettura > doc/referti_l2/ep_fondo.txt     (la lettura della v1, invariata)

**Una sola differenza:** la cartella `fondo_1c.BASE` si crea PRIMA della corsa *(`os.makedirs`; se c'e' gia' una serie, ALZA: non si riscrive)*. Il resto: `ep_fondo.calcio` cosi' com'e'.
"""
import argparse
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import ep_fondo as EP  # noqa: E402


def main(argv):
    import _presidio
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("calcio",))
    ap.add_argument("--k", type=float, choices=EP.KK)
    a = ap.parse_args(argv)
    _presidio.avvia(os.path.join(_QUI, "ep_fondo.py"))
    _presidio.avvia(__file__)
    d = EP.base_k(a.k)
    assert not os.path.exists(os.path.join(d, "calcio_%s" % EP.F1.MC.nome(a.k, 1), "serie.json")), "%s ha gia' una serie: non si riscrive" % d
    os.makedirs(d, exist_ok=True)
    return EP.calcio(a.k)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
