# -*- coding: utf-8 -*-
r"""IL REFERTO DELLA DERIVA — **scritto da chi ha misurato, e non ricopiato.**

### ⛔ **PERCHE' STA IN UN FILE SUO:** `primo_ordine/deriva.py` ha passato il tetto di
`700` righe, e la regola e' ### **oltre SI DIVIDE, NON SI ALLUNGA.** ### ⚠ **E la riga di
taglio non e' casuale:** la- dentro c'e' ### **la MISURA**, qui c'e' ### **COME SI
RACCONTA** -- due responsabilita' diverse, e il presidio lo ha fatto notare prima di me.

### ⚠ **E `CONFIG` sta QUI**, perche' e' cio' che il referto ### **deve dichiarare per
intero** *(la regola di `H-P5`)*: il difetto che quel presidio cura e' ### **dichiarare i
parametri che ho toccato io e tacere i trenta che stavano a default.**
"""
import os

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))


DOVE = os.path.join(os.path.dirname(_QUI), "doc", "REFERTO_deriva_energia.md")
CONFIG = (("seme", 7),
          ("eps della moneta di spin", 0.5),
          ("sommatoria", "numpy"),
          ("psi iniziale", "gaussiano complesso dal seme, NORMALIZZATO a 1"),
          ("phi iniziale", "modulo 1, fasi uniformi dal seme"),
          ("versori n per estremita'", "gaussiani dal seme, normalizzati a 1"),
          ("U per arco", "U(2) casuale via QR, COMPAGNA = coniugata trasposta"),
          ("il tick", "l'ORDINE INTERO di composizione.py, 7 applicazioni"),
          ("il flusso N", "ACCESO, in due mezzi (Strang)"))


def scrivi_referto(dati):
    """### Il referto, ### **scritto dallo script che ha misurato** *(`L-NUMERI`).**

    ### ⚠ **E dichiara `CONFIG` per intero**, che e' la regola di **`H-P5`**.
    """
    import io
    import platform
    nl = chr(10)
    r = []
    r.append("# LA DERIVA DI `E` SUL TICK INTERO — **il `4.20` non si riproduce, e il"
             " perche' e' STRUTTURALE**")
    r.append("")
    r.append("> ### ⛔ **IL NUMERO VECCHIO ERA ORFANO** *(`L-NUMERI-DERIVA-ORFANA`)*:"
             " nessuno script lo")
    r.append("> produceva. ### **Questo referto lo sostituisce con numeri che escono da un"
             " comando.**")
    r.append("")
    r.append("Lo rigira:  `python primo_ordine/deriva.py --scrivi`")
    r.append("")
    r.append("## 1. LA CONFIGURAZIONE INTERA")
    r.append("")
    r.append("| la voce | il valore |")
    r.append("|---|---|")
    for k, v in CONFIG:
        r.append("| %s | `%s` |" % (k, v))
    r.append("| piattaforma | `%s`, python `%s`, numpy `%s` |" %
             (platform.system(), platform.python_version(), np.__version__))
    r.append("")
    for blocco in dati:
        r.extend(blocco)
        r.append("")
    dati_b = (nl.join(r) + nl).encode("utf-8")
    io.open(DOVE, "wb").write(dati_b)
    return DOVE
