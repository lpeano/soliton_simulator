# -*- coding: utf-8 -*-
r"""**IL COLLAUDO DEL TIMBRO COI FINE RIGA NORMALIZZATI** *(Luca `2026-11-13`, dopo il falso allarme n.149 del guardiano)*.

    python csv/test_timbro_eol.py > doc/referti_l2/timbro_eol.txt

**Su un repo git TEMPORANEO** *(nessun file vero toccato)*: **un file Python committato LF** *(con un `.gitattributes` `* text eol=lf`, come il repo)*; poi:
**DEVE PASSARE:** **lo stesso file riscritto in CRLF: «pulito»** *(e `solo_fine_riga`)*; **il file com'e': «pulito»;**
**DEVE FALLIRE:** **un byte cambiato davvero** *(una lettera)*, **anche in CRLF: «pulito».**
"""
import os
import shutil
import subprocess
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import _presidio  # noqa: E402

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-90s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:90], "PASSA" if passa else "### FALLISCE", nota))


def main():
    _presidio.avvia(os.path.join(_QUI, "_presidio.py"))
    _presidio.avvia(__file__)
    print("=" * 110)
    print("IL TIMBRO COI FINE RIGA NORMALIZZATI, su un repo git temporaneo")
    print("=" * 110)
    d = tempfile.mkdtemp(prefix="timbro_eol_")
    try:
        def git(*a):
            subprocess.run(["git", "-c", "user.email=collaudo@locale", "-c", "user.name=collaudo", "-c", "core.autocrlf=true"] + list(a),
                           cwd=d, check=True, capture_output=True)
        git("init", "-q")
        open(os.path.join(d, ".gitattributes"), "wb").write(b"* text eol=lf\n")
        f = os.path.join(d, "prova.py")
        lf = b"# prova\nx = 1\nprint(x)\n"
        open(f, "wb").write(lf)
        git("add", ".")
        git("commit", "-q", "-m", "prova")
        t = _presidio.timbro(f)
        esito("il file com'e' (LF): pulito", t["dirty"] is False and not t["solo_fine_riga"], "dirty %s, solo_fine_riga %s" % (t["dirty"], t["solo_fine_riga"]), True)
        open(f, "wb").write(lf.replace(b"\n", b"\r\n"))
        t = _presidio.timbro(f)
        esito("lo stesso file in CRLF: pulito (solo i fine riga)", t["dirty"] is False and t["solo_fine_riga"] is True, "dirty %s, solo_fine_riga %s" % (t["dirty"], t["solo_fine_riga"]), True)
        open(f, "wb").write(lf.replace(b"x = 1", b"x = 2").replace(b"\n", b"\r\n"))
        t = _presidio.timbro(f)
        esito("un byte cambiato davvero (x = 2), in CRLF: pulito", t["dirty"] is False, "dirty %s" % t["dirty"], False)
        open(f, "wb").write(lf.replace(b"x = 1", b"x = 2"))
        t = _presidio.timbro(f)
        esito("un byte cambiato davvero (x = 2), in LF: pulito", t["dirty"] is False, "dirty %s" % t["dirty"], False)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("=" * 110)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
