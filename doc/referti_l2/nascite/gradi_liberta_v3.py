# -*- coding: utf-8 -*-
r"""**[M1751-L] LA SCHEDA SPETTRALE -- LA V3** *(la v2 cadde due volte, `5c51f40a` e questo commit: (1) la ripresa della nascita 1 non ha `cs_prec` -- la nascita avviene prima di ogni tick; (2) `gradi_liberta.scheda` chiama `Z["metti"]()` su una scena CRESCIUTA, che non si rimette: errori miei)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe C:/Users/lpeano/wt_mitosi/doc/referti_l2/nascite/gradi_liberta_v3.py scheda --nascite 1,2,3,10,269
    E:\python\py3132\python.exe doc/referti_l2/nascite/gradi_liberta_v3.py lettura > doc/referti_l2/nascite/gradi_liberta.txt

**Due differenze, IN MEMORIA** *(`gradi_liberta.py` e la v2 sono usati e non si riscrivono)*: **(1)** `aperto` apre una COPIA dello stato col `meta` completato dalla partenza della ripresa *(come la v2)* **e con `cs_prec` dalla partenza SOLO se manca e la partenza ha lo STESSO `k`** *(se no: ALZA)*; **(2)** `gradi_liberta.scheda` dal suo sorgente riga per riga **senza la riga `Z["metti"]()`** *(l'assert: una sola)*.
"""
import contextlib
import inspect
import json
import os
import sys
import textwrap

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
        cs_p = z["cs_prec"].copy() if "cs_prec" in z.files else None
    with np.load(f) as z:
        X = {x: z[x] for x in z.files}
    m = json.loads(str(X["meta"]))
    aggiunte = sorted(x for x in mp if x not in m)
    m2 = dict(mp)
    m2.update(m)
    X["meta"] = np.array(json.dumps(m2))
    nota = ""
    if "cs_prec" not in X:
        assert cs_p is not None and int(mp["k"]) == int(m["k"]), "cs_prec manca in %s e la partenza %s NON e' allo stesso k (%s contro %s): FERMO" % (f, part, mp.get("k"), m.get("k"))
        X["cs_prec"] = cs_p
        nota = "; cs_prec dalla partenza (lo stesso k %d)" % int(m["k"])
    fc = os.path.join(d, "completo3_" + os.path.basename(f))
    np.savez(fc, **X)
    with open(fc + ".sha1", "w", encoding="utf-8") as fh:
        fh.write(NL.CP.sha1(fc) + "\n")
    print("    il meta di %s completato da %s: %s%s" % (os.path.basename(f), os.path.basename(part), aggiunte, nota))
    return fc


@contextlib.contextmanager
def aperto(f):
    with _VERO(completo(f)) as x:
        yield x


def scheda_senza_metti():
    src = textwrap.dedent(inspect.getsource(GL.scheda))
    riga = '            Z["metti"]()\n'
    assert src.count(riga) == 1, "la riga Z[metti] NON e' una sola nella scheda della v1"
    src = src.replace(riga, "")
    exec(compile(src, GL.__file__ + " (la v3: senza Z[metti])", "exec"), GL.__dict__)


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "gradi_liberta.py"))
    _presidio.avvia(__file__)
    GL.aperto = aperto
    scheda_senza_metti()
    return GL.main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
