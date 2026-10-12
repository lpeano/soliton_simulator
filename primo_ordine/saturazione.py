# -*- coding: utf-8 -*-
"""IL GENERATORE DELLA SATURAZIONE — **le quattro funzioni, e il LIMITE.**

> `N_k = Lambda_k G(x_k)`, con `x_k = h_k / Lambda_k` e **`G(x) = x - arctan x`**.

### ⛔ **PERCHE' UN MODULO A SE', e NON e' una scelta estetica:** `motore.py` ha
superato **il tetto di `700` righe** quando il flusso e' entrato, e la regola dice
**oltre, SI DIVIDE, NON SI ALLUNGA**. ### ⭐ **E il taglio e' quello giusto:**
qui stanno **le funzioni del GENERATORE** *(la forma della legge, che vive in tabella)*,
la' sta **il motore** *(che le applica)*.

### ✅ **E SONO PURE: nessun `self`, nessuno stato, nessun buffer.** Il collaudo
le prova **sui numeri**, senza costruire un motore.

### ⭐ **IL LIMITE `Lambda -> 0` NON E' UN PAVIMENTO.** Dove `Lambda == 0`
**esatto** si usa la forma limite *(`G' = 1`, `b = -(pi/2) sign(h)`)*: ### **e' il valore
che la funzione PRENDE la'**, non una protezione. ### ⚠ **E la differenza conta:**
un pavimento violerebbe l'assioma che vieta una cura dove non c'e' un errore;
**un limite e' la funzione.**
"""
import math

import numpy as np

# ### ⭐ **MEZZO PI, e NON e' una costante nuova:** e' il valore che `b(x)`
# ### **PRENDE** nel limite `Lambda -> 0`, cioe' `-pi/2 sign(h)`. ### **Non e' tarato
# ### su niente** -- e' un limite, e l'assioma riguarda i numeri **SCELTI**.
PIMEZZI = 0.5 * math.pi


def G(x):
    """### `G(x) = x - arctan x`: ### **dispari**, e cresce come `x^3/3` all'origine."""
    return x - np.arctan(x)


def Gp(x):
    """### `G'(x) = x^2 / (1 + x^2)`: ### **PARI e LIMITATA -- e' LA SATURAZIONE.**"""
    return (x * x) / (1.0 + x * x)


def b(x):
    """### `b(x) = dN/dLambda = x/(1+x^2) - arctan x`: ### **DISPARI.**"""
    return x / (1.0 + x * x) - np.arctan(x)


def pezzi(h, lam):
    """### `(angolo per unita' di tempo, fase per unita' di tempo)`, ### **col LIMITE.**

    ### ⛔ **DOVE `Lambda == 0` ESATTO si usa la forma limite** *(`G' = 1`,
    `b = -(pi/2) sign(h)`)*: ### **non e' un pavimento, e' il valore che la funzione
    PRENDE la'.** ### ⚠ **E la differenza conta:** un pavimento violerebbe
    `A11` *(nessuna cura dove non c'e' un errore)*; ### **un limite e' la funzione.**
    """
    buoni = lam > 0.0
    al = np.ones_like(lam)
    be = -PIMEZZI * np.sign(h)
    if np.any(buoni):
        x = h[buoni] / lam[buoni]
        al[buoni] = Gp(x)
        be[buoni] = b(x)
    return al, be
