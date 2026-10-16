# -*- coding: utf-8 -*-
r"""**LA VARIABILE DEL FLUSSO CHE GIRA**, letta ### **dalla TABELLA.**

> ### ⛔⛔ **`STRUMENTO-LEGGE-DALLA-TABELLA`** *(decisione di Luca, `2026-10-16`
> `13:25`)*: uno strumento ### **non contiene** l'id di una legge, ne' la sua formula.
> ### **E se trova un flusso che non sa misurare, ALZA.**

### ⚠ **PERCHE' UN MODULO A SE':** con la cura del `2-quater` `deriva.py` e' arrivato a
### **`763` righe**, oltre ### **il tetto di `700`** — e ### **`m0` non poteva uscire**,
perche' chiama `corri` e avrebbe fatto ### **un ciclo di import** *(`P-MOD` lo ha
rifiutato: «due moduli che si importano a vicenda NON SONO DUE MODULI»)*.
### ✅ **Questo invece non importa `deriva`:** legge ### **la tabella e il motore**, e
basta.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import composizione as CM                                     # noqa: E402

def flusso_che_gira():
    """### L-`id` e la FRAZIONE del flusso ### **nell-ORDINE**, dalla tabella.

    ### ⛔ **`STRUMENTO-LEGGE-DALLA-TABELLA`:** uno strumento ### **non contiene** l-id
    di una legge, e ### **ALZA** se trova un flusso che non sa misurare.
    """
    import motore as MO
    quale = CM.ORDINE[0]
    assert quale[0] in MO.FLUSSI, (
        "il PRIMO pezzo dell-ordine e- `%s` e NON e- un flusso: lo strumento prende il"
        " <<mezzo tick>> dopo il primo pezzo, e sa farlo solo se quello e- un FLUSSO"
        % (quale[0],))
    assert quale[0] in CONOSCIUTI, (
        "il flusso nell-ordine e- `%s` e lo strumento NON SA la sua variabile: conosce"
        " %s" % (quale[0], sorted(CONOSCIUTI)))
    return quale[0], float(quale[1])


# ### ⛔ **I FLUSSI CHE LO STRUMENTO SA MISURARE, con la loro VARIABILE:** non e- un id
# ### usato a mano, e- ### **il dizionario di cio- che conosce** -- e cio- che non c-e-
# ### ### **fa ALZARE.**
CONOSCIUTI = {"CAMM-MATERIA-VUOTO": "rho/Lambda"}


def satura(st, mot):
    """### `max_k x_k` con `x` ### **LA VARIABILE DEL FLUSSO CHE GIRA.**

    ### ⛔ **RISCRITTA IL `2026-10-16`** *(il perche- sta nel task history
    `2026-10-16_2quater_deriva_satura.md`)*: misurava ### **`|h|/Lambda`**, la variabile
    della ### **SATURAZIONE**, che non e- piu- nell-ordine. ### **Il flusso si LEGGE dalla
    tabella**, e ### **senza questo numero una misura su `N` e- un FALSO-ZERO sospetto.**
    """
    flusso_che_gira()
    rho = mot.densita_materia(st)
    lam = mot.densita_vuoto(st)
    buoni = lam > 0.0
    return float(np.max(rho[buoni] / lam[buoni])) if np.any(buoni) else 0.0


def satura_elicita(st, mot):
    """### `max_k |h_k/Lambda_k|`: ### **la variabile VECCHIA**, per il caso che DEVE fallire.

    ### ⛔ **NON decide niente:** serve al braccio `(1)` per ### **mostrare** che su uno
    stato a ### **`h = 0` ma `rho > 0`** il controllo vecchio direbbe ### **<<nessuna
    materia>>**.
    """
    h = mot.elicita(st)
    lam = mot.densita_vuoto(st)
    buoni = lam > 0.0
    return float(np.max(np.abs(h[buoni] / lam[buoni]))) if np.any(buoni) else 0.0
