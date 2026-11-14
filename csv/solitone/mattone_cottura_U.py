# -*- coding: utf-8 -*-
r"""**LA COTTURA COL CARICAMENTO CHE RICOSTRUISCE `U`** *(Luca `2026-11-14` `12:00`, il bivio (a'); `12:19`, le chiavi di servizio; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `16.5`-`16.7`)*.

    python csv/solitone/mattone_cottura_U.py cuoci --caso MGU --registro cottura-U-MGU > doc/referti_l2/mattone/cottura_U_MGU.txt

### **`mattone_cottura.cuoci` COSI' COM'E'** *(il DEVE della ripartenza `04000` -> `05000`, poi i pezzi da `1000` tick fino a COTTO)*, **con DUE funzioni sostituite IN MEMORIA prima della corsa** *(dichiarato; `mattone_cottura.py` NON si tocca)*:
1. **`carica`:** **dopo il caricamento `mot.geo.U` si ricostruisce dal campo salvato** *(`_u1_prototipo.scrivi_U`: l'`U` che `avvolto` lascia dopo l'ultimo tick, `exp(i e A)`; la prova: `geometria_nascosta.py ripartenza --caso MU --ricostruisci` UGUALE AL BIT, `45455a50`)*; **lo schema del tick e' quello di OGGI** *(le copie del punto fisso come in tutte le corse G+U fatte)*;
2. **`uguale_al_file`:** **il confronto ESCLUDE le CHIAVI DI SERVIZIO** *(Luca `12:19`)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone_cottura as CT  # noqa: E402

# ### LE CHIAVI DI SERVIZIO (Luca 12:19): NON sono stato della dinamica, e il confronto delle ripartenze le esclude.
CHIAVI_SERVIZIO = {
    "h_int": "una CACHE diagnostica: motore.elicita la riscrive per intero da psi_h (h.fill(0), poi la somma); la misura dell'energia la riscrive; dopo 1000 tick di ripartenza "
             "tutte le altre chiavi sono uguali AL BIT (geometria_ripartenza_MG.txt, geometria_ripartenza_MGU_U.txt): non entra nel tick",
}
_carica_vero = CT.carica


def carica_U(Z, caso, rho_c, k):
    """### `mattone_cottura.carica`, poi `mot.geo.U` ricostruito dal campo salvato *(se il caso ha il campo)*."""
    import _u1_prototipo as U1
    C, f = _carica_vero(Z, caso, rho_c, k)
    if C.campo is not None:
        U1.scrivi_U(Z["mot"], C.campo)
        print("### il caricamento di %s: U ricostruito dal campo salvato (max |U - I| %.3e)" % (f, float(np.max(np.abs(Z["mot"].geo.U - np.eye(2)[None, :, :])))))
    return C, f


def uguale_senza_servizio(Z, C, f):
    """### Le chiavi DIVERSE dal file, ESCLUSE le chiavi di servizio *(scritte a parte, come informazione)*."""
    with np.load(f) as d:
        tutte = [k for k in Z["chiavi"] if not np.array_equal(Z["st"][k], d[k])]
        if C.campo is not None:
            tutte += [k for k, a in (("campo_A", C.campo.A), ("campo_E", C.campo.E)) if not np.array_equal(a, d[k])]
    serv = [k for k in tutte if k in CHIAVI_SERVIZIO]
    print("### il confronto col file: le chiavi di servizio ESCLUSE %s; fra queste diverse: %s" % (sorted(CHIAVI_SERVIZIO), serv))
    return [k for k in tutte if k not in CHIAVI_SERVIZIO]


def main(argv):
    import _presidio
    for m in ("mattone_cottura", "mattone", "conti"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    print("### LA COTTURA COL CARICAMENTO CHE RICOSTRUISCE U (Luca 12:00, 12:19): mattone_cottura.carica e uguale_al_file SOSTITUITE IN MEMORIA; le chiavi di servizio:")
    for k, v in CHIAVI_SERVIZIO.items():
        print("    %s: %s" % (k, v))
    CT.carica = carica_U
    CT.uguale_al_file = uguale_senza_servizio
    return CT.main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
