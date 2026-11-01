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


PRIMA_ALLINEAMENTO = "9180fd38"     # ### l'ultimo commit prima dell'allineamento del mandato delle 01:28 (punto 6)
REFERTI_VECCHI = (("eps 0", "csv/_livelli_piatti.py", "doc/referti_l2/livelli_piatti.txt"), ("eps 0.5", "csv/_massimo_di_B.py", "doc/referti_l2/massimo_di_B.txt"),
                  ("A a K", "csv/_coppia_di_B.py", "doc/referti_l2/coppia_di_B.txt"))


def vecchi():
    """### **D6** *(01:28, punto 6)*: **gli script vecchi ridanno i loro referti perche' il loro codice e' AL BIT quello di prima:** nessun `.py` fuori da `csv/solitone/`
    e' cambiato da `PRIMA_ALLINEAMENTO`, e nessuno script fuori da `csv/solitone/` importa la libreria. ### **Rigirarli da byte identici sarebbe un FALSO-UNO.**"""
    import subprocess
    print("### D6: I TRE REFERTI VECCHI DOPO L'ALLINEAMENTO (%s)" % "; ".join("%s: %s -> %s" % r for r in REFERTI_VECCHI))
    rad = solitone.RADICE
    cambiati = subprocess.check_output(["git", "diff", "--name-only", PRIMA_ALLINEAMENTO, "HEAD", "--", "*.py"], cwd=rad).decode().split()
    sporchi = subprocess.check_output(["git", "status", "--porcelain", "--", "*.py"], cwd=rad).decode().splitlines()
    fuori = [f for f in cambiati if not f.startswith("csv/solitone/")]
    importano = []
    for cart in ("csv", "primo_ordine"):
        for d, _s, ff in os.walk(os.path.join(rad, cart)):
            if os.path.join("csv", "solitone") in d:
                continue
            for f in ff:
                if f.endswith(".py"):
                    with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
                        tt = fh.read()
                    if "import solitone" in tt or "from solitone" in tt:
                        importano.append(os.path.join(d, f))
    esito("DEVE PASSARE: D6 nessun .py fuori da csv/solitone/ cambiato da %s a HEAD, e niente di non committato" % PRIMA_ALLINEAMENTO, not fuori and not [x for x in sporchi if x.strip()],
          "cambiati %s" % (cambiati or "nessuno"))
    esito("DEVE PASSARE: D6 nessuno script fuori da csv/solitone/ importa la libreria", not importano, "%s" % importano)
    for _chi, scr, ref in REFERTI_VECCHI:
        print("    %s: il blob a %s e a HEAD %s" % (scr, PRIMA_ALLINEAMENTO, "uguali" if scr not in cambiati else "### DIVERSI"))


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
    vecchi()
    print("-" * 150)
    print("  i tempi: %s" % "; ".join("%s %.0f s" % kv for kv in tempi.items()))
    print("ESITO: %d/%d controlli passano; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main())
