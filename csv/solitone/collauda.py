# -*- coding: utf-8 -*-
r"""**IL COLLAUDO DELLA CASSETTA DEGLI ATTREZZI DEL SOLITONE** *(il task history `doc/TASK_HISTORY/2026-11-01_cassetta_solitone.md`)*: ### **i test dei tre moduli, coi tempi.**

    python csv/solitone/collauda.py > doc/referti_l2/cassetta_solitone.txt
"""
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))

import solitone  # noqa: E402,F401  (i percorsi)

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-130s %s   %s" % (che[:130], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def main():
    import _presidio
    for m in ("__init__", "uscite", "protetto", "misure", "test_uscite", "test_protetto", "test_misure"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)          # ### per ultimo: SOLITON_DRIVER resta quello del collaudo
    from solitone import test_misure, test_protetto, test_uscite
    print("=" * 150)
    print("LA CASSETTA DEGLI ATTREZZI DEL SOLITONE (Luca 01:22): csv/solitone/ (uscite, protetto, misure); i test ridanno AL BIT i numeri gia' committati")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (t1) ogni modulo rida' al bit i numeri committati; (t2) un modulo non li rida': quale, perche'")
    print("=" * 150)
    tempi = {}
    s0 = time.time()
    test_uscite.gira(esito)
    tempi["uscite"] = time.time() - s0
    s0 = time.time()
    partenze = test_protetto.gira(esito)
    tempi["protetto"] = time.time() - s0
    s0 = time.time()
    test_misure.gira(esito, partenze)
    tempi["misure"] = time.time() - s0
    print("-" * 150)
    print("  i tempi: %s" % "; ".join("%s %.0f s" % kv for kv in tempi.items()))
    print("ESITO: %d/%d controlli passano; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main())
