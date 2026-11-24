# -*- coding: utf-8 -*-
r"""**L'ANISOTROPIA DELLA MATERIA SULLA GRIGLIA 96: GRIGLIA O RETICOLO?** *(la risposta di Luca al FERMO della carta della cura, `2026-11-21` notte; solo Bloch, nessuna corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lorentz_griglia96.py > doc/referti_l2/lorentz_griglia96.txt

**Come `lorentz_velocita.py materia`** *(`v_max` e `v_max` proiettata a `0`, `15`, `30` gradi, la stessa funzione `v_max_dir`)* **sulla matrice di Bloch del passo a `cs = s` col lato `96`** *(`_triangoli_bassa_energia.matrice(0.5, 0.15, 96, "simm")`)* **contro il lato `48`** *(il json di L1)*. **La lettura** *(fissata qui)*: se l'anisotropia `(max - min)/media` a `96` e' entro il `20%` di quella a `48`, **e' del reticolo**; se scende di piu', **era (anche) la griglia**.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import lorentz_velocita as LV  # noqa: E402


def main():
    import _presidio
    import _triangoli_forza as TF
    import _triangoli_bassa_energia as BE
    _presidio.avvia(os.path.join(_QUI, "lorentz_velocita.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("L'ANISOTROPIA DELLA MATERIA SULLA GRIGLIA 96 (la risposta di Luca al FERMO della carta della cura): solo Bloch")
    print("=" * 130)
    with open(os.path.join(_QUI, "lorentz_velocita_materia.json"), encoding="utf-8") as fh:
        M48 = json.load(fh)
    A = BE.matrice(LV.EPS_CORSA, LV.S_CORSA, 96, "simm")
    v0, dove, fase = TF.v_max(A)
    vd = LV.v_max_dir(A, LV.THETA)
    an96 = (max(vd) - min(vd)) / float(np.mean(vd))
    v48 = [M48["theta"][str(t)] for t in LV.THETA]
    an48 = (max(v48) - min(v48)) / float(np.mean(v48))
    print("### lato 48 (L1): v_max/s %.8f; proiettata %s; l'anisotropia %.4e" % (M48["v_max_su_s"], ", ".join("%g gradi %.8f" % (t, v / LV.S_CORSA) for t, v in zip(LV.THETA, v48)), an48))
    print("### lato 96: v_max/s %.8f (in %s); proiettata %s; l'anisotropia %.4e" % (v0 / LV.S_CORSA, dove, ", ".join("%g gradi %.8f" % (t, v / LV.S_CORSA) for t, v in zip(LV.THETA, vd)), an96))
    rap = an96 / an48
    print("### il rapporto delle anisotropie 96/48: %.4f -> %s" % (rap, "DEL RETICOLO (entro il 20%)" if abs(rap - 1.0) <= 0.2 else "ERA (ANCHE) LA GRIGLIA"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
