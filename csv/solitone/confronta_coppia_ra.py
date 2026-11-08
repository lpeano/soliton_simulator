# -*- coding: utf-8 -*-
r"""**(r-a) K1 E K2: LA PARTE COMUNE DEL REFERTO NUOVO = IL REFERTO UFFICIALE** *(il task history `doc/TASK_HISTORY/2026-11-07_referto_coppia_C35.md`, sez. `12`)*. [[PIANO-2D-3D]]

    python csv/solitone/confronta_coppia_ra.py > doc/referti_l2/confronta_coppia_ra.txt

**K1** *(DEVE PASSARE)*: **le righe di `doc/referti_l2/coppia_C35-0_30000.txt` PRIMA della sezione «OLTRE»** *(tolte le righe `[TIMBRO]`, che portano il blob)*
**= le righe di `doc/referti_l2/coppia_C35-0.txt`** *(il referto ufficiale a `10000`, `838e4b45`)* **prima del blocco finale dell'ESITO, AL CARATTERE.**
**K2** *(DEVE FALLIRE)*: **lo stesso confronto contro `doc/referti_l2/coppia_C35-pi.txt`** *(un'altra corsa: il confronto deve saper dire «diverso»)*.
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
RADICE = os.path.dirname(os.path.dirname(_QUI))
REF = os.path.join(RADICE, "doc", "referti_l2")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))


def righe(nome):
    t = io.open(os.path.join(REF, nome), encoding="utf-8").read().splitlines()
    return [r for r in t if not r.startswith("[TIMBRO]")]


def parte_comune_nuova(r):
    i = next(k for k, x in enumerate(r) if x.startswith("### OLTRE t "))
    assert r[i - 1].startswith("-" * 50), "la sezione OLTRE comincia con la sua riga di trattini"
    return r[:i - 1]


def parte_ufficiale(r):
    i = max(k for k, x in enumerate(r) if x.startswith("ESITO:"))
    assert r[i - 1].startswith("=" * 50)
    return r[:i - 1]


def confronta(a, b):
    """### `(uguali, il primo indice diverso, le due righe)`."""
    for k, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return False, k, (x[:90], y[:90])
    if len(a) != len(b):
        return False, min(len(a), len(b)), ("lunghezze %d e %d" % (len(a), len(b)), "")
    return True, len(a), ("", "")


def main():
    import _presidio
    _presidio.avvia(__file__)
    nuovo = parte_comune_nuova(righe("coppia_C35-0_30000.txt"))
    for che, nome, deve in (("K1 la parte comune del referto a 30000 = il referto ufficiale di C35-0 a 10000, al carattere", "coppia_C35-0.txt", True),
                            ("K2 la stessa parte comune = il referto di C35-pi (un'altra corsa)", "coppia_C35-pi.txt", False)):
        uff = parte_ufficiale(righe(nome))
        ug, k, (x, y) = confronta(nuovo, uff)
        esito(che, ug, "%d righe confrontate%s" % (k, "" if ug else "; la prima diversa, riga %d: %r contro %r" % (k, x, y)), deve=deve)
    print("### %d su %d come devono%s" % (OK[0], OK[1], ("   FALLITE: " + "; ".join(FALLITE)) if FALLITE else ""))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
