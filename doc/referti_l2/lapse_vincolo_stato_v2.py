# -*- coding: utf-8 -*-
r"""**[M0528] LO STATO DELLE CORSE DAL DISCO -- LA V2** *(la v1 `lapse_vincolo_stato.py` cadde all'import: `_presidio` sta in `csv/` e il percorso lo mette l'import di `lapse_vincolo`, che la v1 non faceva; il log `lapse_vincolo_stato_fallito.txt`, `7d802780`)*. **Una sola differenza:** `import lapse_vincolo` prima, poi la v1 intera. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo_stato_v2.py > doc/referti_l2/lapse_vincolo_stato.txt
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import lapse_vincolo  # noqa: E402,F401  (il percorso di csv/, per _presidio)
import lapse_vincolo_stato as ST  # noqa: E402


def main():
    import _presidio
    _presidio.avvia(__file__)
    return ST.main()


if __name__ == "__main__":
    sys.exit(main())
