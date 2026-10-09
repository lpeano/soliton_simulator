# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` — ### **NON si modifica a mano.**

### ⛔ **`P-E2` confronta l-IMPRONTA qui sotto con la riga di tabella e RIFIUTA il commit** se non corrispondono. ### **Per cambiare questo file si cambia LA TABELLA e si rigenera.**

### **La scheda:** `doc/leggi_era2/PROVA-LOCALE.md`.
"""
import numpy as np

# ### L-ID DELLA LEGGE: `P-E1` lo legge ### **via AST**, non per regex.
LEGGE = 'PROVA-LOCALE'
# ### L-IMPRONTA della riga di tabella *(`sha1` del `json` a chiavi ordinate)*.
IMPRONTA = '0e656d1cd4c84340'
TIPO = 'termine_nodo'
AMBITO = ('psi',)
PROVA = True
# ### LA TOLLERANZA su |Im(H)|: DICHIARATA, non scelta nel momento.
# ### 1e-10 relativo: l-espressione e- VERIFICATA REALE SIMBOLICAMENTE, quindi
# ### qui resta solo l-ERRORE DI VIRGOLA MOBILE -- e 1e-10 e- mille volte
# ### l-epsilon di float64 accumulato su una somma di qualche migliaio di
# ### termini.
TOLL_IM = 1e-10
PARAMETRI = {'g': 0.5}


def energia(st, ii=None, jj=None):
    """### Il contributo di questa legge a `H`. ### **Reale.**"""
    psi_0 = st['psi'][:, 0]
    psi_1 = st['psi'][:, 1]
    psi_0c = np.conj(psi_0)
    psi_1c = np.conj(psi_1)
    g = PARAMETRI['g']
    _e = (1/2)*g*(psi_0*psi_0c + psi_1*psi_1c)**2
    _s = np.sum(_e)
    # ### ⛔ NON `np.real`: un troncamento SILENZIOSO non e-
    # ### un ramo (`A8`). L-espressione e- VERIFICATA REALE SIMBOLICAMENTE dal
    # ### generatore; questo `assert` e- la rete SOTTO quella verifica, non AL
    # ### POSTO di essa -- e scatta se l-aritmetica in virgola mobile va oltre
    # ### la tolleranza dichiarata.
    _im = abs(float(np.imag(_s)))
    assert _im <= TOLL_IM * max(abs(float(np.real(_s))), 1.0), (
        '%s: |Im(H)| = ' % LEGGE + repr(_im)
        + ' oltre la tolleranza ' + repr(TOLL_IM)
        + ': l-espressione NON e- reale su questi dati')
    return float(np.real(_s))


def gradiente(st, fuori, ii=None, jj=None):
    """### `dH/dpsi*`, ### **accumulato in `fuori`**.

    ### ⚠ **Si ACCUMULA** *(`+=`)*: `hamiltoniana.py` somma i termini
    ### **in un solo posto**, e un termine che SCRIVESSE invece di accumulare
    ### **cancellerebbe i termini prima di lui.**
    """
    psi_0 = st['psi'][:, 0]
    psi_1 = st['psi'][:, 1]
    psi_0c = np.conj(psi_0)
    psi_1c = np.conj(psi_1)
    g = PARAMETRI['g']
    fuori['psi'][:, 0] += g*psi_0*(psi_0*psi_0c + psi_1*psi_1c)
    fuori['psi'][:, 1] += g*psi_1*(psi_0*psi_0c + psi_1*psi_1c)
    return fuori

