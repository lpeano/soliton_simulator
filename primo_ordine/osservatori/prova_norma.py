# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` — ### **NON si modifica a mano.**

### ⛔ **UN OSSERVATORE LEGGE.** `P-E5` fa girare `misura()` e confronta lo stato ### **AL BYTE** prima e dopo: ### **una scrittura, anche involontaria, e- un ERRORE** *(`A17`)*.

### **La scheda:** `doc/leggi_era2/PROVA-NORMA.md`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from _rif import rif

# ### L-ID: un presidio lo legge ### **via AST**, non per regex.
LEGGE = 'PROVA-NORMA'
IMPRONTA = 'febcc615053eac7e'
TIPO = 'osservatore'
AMBITO = ('psi',)
PROVA = True
# ### LA VOCE che questo osservatore MISURA: un presidio la verifica.
VOCE = 'MISURA-NORMA-ERA2'
TOLL_IM = 1e-10


@rif('MISURA-NORMA-ERA2', ruolo="misura")
def misura(st):
    """### Il valore misurato. ### **Reale, e NON tocca `st`.**"""
    psi_0 = st['psi'][:, 0]
    psi_1 = st['psi'][:, 1]
    psi_0c = np.conj(psi_0)
    psi_1c = np.conj(psi_1)
    _e = psi_0*psi_0c + psi_1*psi_1c
    _s = np.sum(_e)
    # ### ⛔ NON `np.real`: lo stesso motivo dei
    # ### termini (`A8`). L-espressione e- VERIFICATA REALE
    # ### SIMBOLICAMENTE dal generatore, e questo assert e- la rete
    # ### SOTTO quella verifica.
    _im = abs(float(np.imag(_s)))
    assert _im <= TOLL_IM * max(abs(float(np.real(_s))), 1.0), (
        '%s: |Im| = ' % LEGGE + repr(_im)
        + ' oltre la tolleranza ' + repr(TOLL_IM))
    return float(np.real(_s))

