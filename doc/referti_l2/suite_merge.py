# -*- coding: utf-8 -*-
r"""**[M1330-A2] IL CASO NOTO DELLE NASCITE DOPO IL MERGE lapse-u -> mitosi** *(DECISIONE DI LUCA, 2026-11-24 13:30 e 13:33)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/suite_merge.py > doc/referti_l2/suite_merge.txt

**Dal tronco a `k 35976`** *(`TRONCO/prima_nascita_35976.npz`, lo stato prima della prima nascita)* **col codice del ramo fuso** *(`mitosi_rami_v2.ciclo`, modo `mitosi`, come O2 di `orientamento_prove.py`)* **fino a `k 36000`**: lo stato **AL BIT** con `MITOSI/stato_36000.npz` *(`orientamento_prove.confronta`: ogni array, il grafo, i versori, Theta, le posizioni, `gauss_acc`, `cs_prec`, `E_persa`)*. **DEVE FALLIRE:** lo stesso stato finale contro `MITOSI/stato_36250.npz`.
"""
import os
import shutil
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import orientamento_prove as OP  # noqa: E402

R2, ML, PS = OP.R2, OP.ML, OP.PS
F36000 = os.path.join(OP.D_M, "stato_36000.npz")
D_OUT = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1330", "suite_merge")


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_rami_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "orientamento_prove.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    if os.path.isdir(D_OUT):
        shutil.rmtree(D_OUT)
    print("=" * 130)
    print("[M1330-A2] IL CASO NOTO DELLE NASCITE DOPO IL MERGE: dal tronco k 35976 col codice fuso fino a k 36000, contro MITOSI/stato_36000 AL BIT")
    print("=" * 130)
    _c, k, fin = R2.ciclo("SUITE_MERGE", "mitosi", OP.F_TR, 36000, None, d_out=D_OUT)
    dd = OP.confronta(fin, F36000)
    print("### dal tronco k 35976 fino a k %d contro %s (sha1 %s): %s" % (k, os.path.basename(F36000), ML.sha1(F36000)[:8], "AL BIT" if not dd else "### DIVERSE: %s" % dd))
    OP.esito("lo stato a k 36000 col codice fuso = MITOSI/stato_36000 AL BIT", not dd)
    d2 = OP.confronta(fin, OP.F36250)
    OP.esito("DEVE FALLIRE: lo stesso stato contro MITOSI/stato_36250 (diverso)", bool(d2), "diversi %s" % d2)
    return OP.fine()


if __name__ == "__main__":
    sys.exit(main())
