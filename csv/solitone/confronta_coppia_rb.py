# -*- coding: utf-8 -*-
r"""**(r-b) K-rb: IL TAGLIO NON CAMBIA IL PASSATO** *(il task history `doc/TASK_HISTORY/2026-11-07_referto_coppia_C35.md`, sez. `16`)*. [[PIANO-2D-3D]]

    python csv/solitone/confronta_coppia_rb.py > doc/referti_l2/confronta_coppia_rb.txt

**Le righe delle TABELLE A BLOCCHI** *(`  <a> .. <b> ...`)* **con la fine del blocco `b <= 10000`** *(il `t` del referto ufficiale)*, **nel referto (r-b) e nel referto ufficiale a `10000`, AL CARATTERE, nello stesso ordine.**
**K-rb** *(DEVE PASSARE)*: `coppia_C35-0_rb.txt` contro `coppia_C35-0.txt`, e `coppia_C35-pi_rb.txt` contro `coppia_C35-pi.txt`. **K-rb-F** *(DEVE FALLIRE)*: `coppia_C35-0_rb.txt` contro `coppia_C35-pi.txt`.
"""
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
RADICE = os.path.dirname(os.path.dirname(_QUI))
REF = os.path.join(RADICE, "doc", "referti_l2")
T_UFF = 10000.0                # ### la fine del referto ufficiale, in unita' di tempo
BLOCCO = re.compile(r"^\s+(\d+) \.\. +(\d+) ")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))


def blocchi(nome):
    """### Le righe a blocchi con la fine `<= T_UFF`, nell'ordine."""
    out = []
    for r in io.open(os.path.join(REF, nome), encoding="utf-8").read().splitlines():
        m = BLOCCO.match(r)
        if m and float(m.group(2)) <= T_UFF:
            out.append(r)
    return out


def confronta(a, b):
    for k, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return False, k, (x[:90], y[:90])
    if len(a) != len(b):
        return False, min(len(a), len(b)), ("lunghezze %d e %d" % (len(a), len(b)), "")
    return True, len(a), ("", "")


def main():
    import _presidio
    _presidio.avvia(__file__)
    for che, nuovo, uff, deve in (("K-rb C35-0: le righe a blocchi fino a 10000 del referto (r-b) = quelle del referto ufficiale, al carattere", "coppia_C35-0_rb.txt", "coppia_C35-0.txt", True),
                                  ("K-rb C35-pi: lo stesso per C35-pi", "coppia_C35-pi_rb.txt", "coppia_C35-pi.txt", True),
                                  ("K-rb-F il referto (r-b) di C35-0 contro l'ufficiale di C35-pi (un'altra corsa)", "coppia_C35-0_rb.txt", "coppia_C35-pi.txt", False)):
        a, b = blocchi(nuovo), blocchi(uff)
        ug, k, (x, y) = confronta(a, b)
        ug = ug and k > 0
        esito(che, ug, "%d righe confrontate (%d e %d)%s" % (k, len(a), len(b), "" if ug else "; la prima diversa, riga %d: %r contro %r" % (k, x, y)), deve=deve)
    print("### %d su %d come devono%s" % (OK[0], OK[1], ("   FALLITE: " + "; ".join(FALLITE)) if FALLITE else ""))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
