# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` — ### **NON si modifica a mano.**

### ⛔ **`P-E2` confronta l-IMPRONTA qui sotto con la riga di tabella e RIFIUTA il commit** se non corrispondono. ### **Per cambiare questo file si cambia LA TABELLA e si rigenera.**

### **La scheda:** `doc/leggi_era2/PROVA-HOPPING.md`.
"""
import numpy as np

# ### L-ID DELLA LEGGE: `P-E1` lo legge ### **via AST**, non per regex.
LEGGE = 'PROVA-HOPPING'
# ### L-IMPRONTA della riga di tabella *(`sha1` del `json` a chiavi ordinate)*.
IMPRONTA = '19547a22540dac81'
TIPO = 'termine_arco'
AMBITO = ('psi',)
PROVA = True
PARAMETRI = {'K': 1.0}


def energia(st, ii=None, jj=None):
    """### Il contributo di questa legge a `H`. ### **Reale.**"""
    psi_i_0 = st['psi'][ii][:, 0]
    psi_i_1 = st['psi'][ii][:, 1]
    psi_i_0c = np.conj(psi_i_0)
    psi_i_1c = np.conj(psi_i_1)
    psi_j_0 = st['psi'][jj][:, 0]
    psi_j_1 = st['psi'][jj][:, 1]
    psi_j_0c = np.conj(psi_j_0)
    psi_j_1c = np.conj(psi_j_1)
    K = PARAMETRI['K']
    _e = -K*(psi_i_0*psi_j_0c + psi_i_0c*psi_j_0 + psi_i_1*psi_j_1c + psi_i_1c*psi_j_1)
    return float(np.real(np.sum(_e)))


def gradiente(st, fuori, ii=None, jj=None):
    """### `dH/dpsi*`, ### **accumulato in `fuori`**.

    ### ⚠ **Si ACCUMULA** *(`+=`)*: `hamiltoniana.py` somma i termini
    ### **in un solo posto**, e un termine che SCRIVESSE invece di accumulare
    ### **cancellerebbe i termini prima di lui.**
    """
    psi_i_0 = st['psi'][ii][:, 0]
    psi_i_1 = st['psi'][ii][:, 1]
    psi_i_0c = np.conj(psi_i_0)
    psi_i_1c = np.conj(psi_i_1)
    psi_j_0 = st['psi'][jj][:, 0]
    psi_j_1 = st['psi'][jj][:, 1]
    psi_j_0c = np.conj(psi_j_0)
    psi_j_1c = np.conj(psi_j_1)
    K = PARAMETRI['K']
    _g = -K*psi_j_0
    np.add.at(fuori['psi'][:, 0], ii, _g * np.ones_like(psi_i_0c))
    _g = -K*psi_j_1
    np.add.at(fuori['psi'][:, 1], ii, _g * np.ones_like(psi_i_1c))
    _g = -K*psi_i_0
    np.add.at(fuori['psi'][:, 0], jj, _g * np.ones_like(psi_j_0c))
    _g = -K*psi_i_1
    np.add.at(fuori['psi'][:, 1], jj, _g * np.ones_like(psi_j_1c))
    return fuori

