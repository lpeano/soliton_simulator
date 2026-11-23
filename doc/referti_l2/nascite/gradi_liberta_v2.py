# -*- coding: utf-8 -*-
r"""**[M1751-L] LA SCHEDA SPETTRALE -- LA V2** *(`gradi_liberta.py` e' usato e non si riscrive: le schede caddero all'apertura dello stato, `KeyError 'R_A'`: gli stati `prima_`/`dopo_` delle riprese hanno un `meta` RIDOTTO; il log `gradi_liberta_fallito.txt`, `42ac7465`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe C:/Users/lpeano/wt_mitosi/doc/referti_l2/nascite/gradi_liberta_v2.py scheda --nascite 1,2,3,10,269
    E:\python\py3132\python.exe doc/referti_l2/nascite/gradi_liberta_v2.py lettura > doc/referti_l2/nascite/gradi_liberta.txt

**Una sola differenza:** `aperto` sostituita IN MEMORIA: lo stato si apre da una **COPIA** *(`completo_<nome>`, nella stessa cartella, con il suo sha1)* il cui `meta` e' completato con le chiavi che mancano, **prese dallo stato di PARTENZA della stessa ripresa** *(`ripresa_nascita.partenza`: i parametri della corsa -- `R_A`, `incollato`, `Delta`, ... -- costanti per tutta la corsa)*; le chiavi gia' presenti *(`k`, `nascita`, `centro`, ...)* restano quelle dello stato. **Gli stati originali non si toccano.** Il resto: `gradi_liberta.py` cosi' com'e'.
"""
import contextlib
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import gradi_liberta as GL  # noqa: E402

NL, RN = GL.NL, GL.RN
_VERO = GL.aperto


def completo(f):
    d = os.path.dirname(f)
    q = int(os.path.basename(d).split("_")[1])
    b = NL.nascite()[q - 1]
    part = RN.partenza(q, int(b["k"]))
    with np.load(part) as z:
        mp = json.loads(str(z["meta"]))
    with np.load(f) as z:
        X = {x: z[x] for x in z.files}
    m = json.loads(str(X["meta"]))
    aggiunte = sorted(x for x in mp if x not in m)
    m2 = dict(mp)
    m2.update(m)
    X["meta"] = np.array(json.dumps(m2))
    fc = os.path.join(d, "completo_" + os.path.basename(f))
    np.savez(fc, **X)
    with open(fc + ".sha1", "w", encoding="utf-8") as fh:
        fh.write(NL.CP.sha1(fc) + "\n")
    print("    il meta di %s completato da %s: %s" % (os.path.basename(f), os.path.basename(part), aggiunte))
    return fc


@contextlib.contextmanager
def aperto(f):
    with _VERO(completo(f)) as x:
        yield x


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "gradi_liberta.py"))
    _presidio.avvia(__file__)
    GL.aperto = aperto
    return GL.main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
