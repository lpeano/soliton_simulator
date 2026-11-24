# -*- coding: utf-8 -*-
r"""**[M1932] B3 DALL'OGGETTO DEL QUARTO GIRO** *(DECISIONE DI LUCA, 2026-11-24 19:32; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-octies`; `legge_fondo_v2.py` e' usato, il suo caso noto ha girato, e non si riscrive)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v2b.py caduta --coll V0               (M1932B3_V0, dalla coda, solo se il giro 4 non e' FERMO)
    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v2b.py caduta --coll V2 --scala 0.5   (0.5, 1.0, 2.0)
    E:\python\py3132\python.exe doc/referti_l2/legge_fondo_v2b.py lettura > doc/referti_l2/legge_fondo_v2.txt

**Una sola differenza, in memoria:** l'oggetto e' `puntofisso_v3b/giro_3/stato_006000.npz`, la partenza del giro 4, cioe' lo stato la cui evoluzione e' misurata da `fondo_puntofisso_v3b4.py`. Le uscite vanno in `M1330/b3` *(vuota: B3 non e' mai partita)*. **La lettura** stampa prima il respiro del giro 4 e la sua fascia, poi `legge_fondo_v2.lettura` cosi' com'e'.
"""
import argparse
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import legge_fondo_v2 as LF  # noqa: E402
import fondo_puntofisso_v3b4 as G4  # noqa: E402

LF.OGGETTO_B3 = G4.PARTENZA_G4


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3b4.py"))
    _presidio.avvia(__file__)
    G4.lettura()
    return LF.lettura()


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("caduta", "lettura"))
    ap.add_argument("--coll", choices=("V0", "V2"))
    ap.add_argument("--scala", type=float, choices=LF.SCALE)
    a = ap.parse_args(argv)
    if a.cosa == "caduta":
        import _presidio
        _presidio.avvia(os.path.join(_QUI, "legge_fondo_v2.py"))
        _presidio.avvia(__file__)
        return LF.caduta(a.coll, a.scala)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
