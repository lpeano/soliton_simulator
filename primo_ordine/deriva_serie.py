# -*- coding: utf-8 -*-
r"""**LE STATISTICHE DELLE SERIE** — *rapporti, escursioni, deriva SECOLARE.*

> ### ⛔⛔ **PERCHE' QUESTO MODULO ESISTE, e il motivo e' MISURATO:** con la cura del
> `2-quater` *(l'ordine INTERO dalla tabella)* `deriva.py` e' arrivato a
> ### **`763` righe**, oltre ### **il tetto di `700`** — e la regola dice ### **oltre, SI
> DIVIDE, NON SI ALLUNGA.**

### ⭐ **E IL TAGLIO SEGUE QUELLO CHE C'ERA GIA':** `deriva_referto.py` tiene
### **cio' che RACCONTA**, qui stanno ### **le statistiche PURE sulle serie** *(nessuna
scena, nessun motore, nessuno stato)*, e `deriva.py` tiene ### **la misura.**

### ✅ **E sono PURE davvero: prendono un array e tornano numeri.**
"""
import numpy as np
def rapporti(righe, col):
    """### I rapporti fra dimezzamenti consecutivi. ### **`4` = esponente `2`.**"""
    fuori = []
    for a, b in zip(righe[:-1], righe[1:]):
        fuori.append(a[col] / b[col] if b[col] > 0 else float("inf"))
    return fuori

def escursioni(serie):
    """### `(somma, primo, vuoto)`: ### **`max - min` lungo la corsa**, non `fine - inizio`.

    ### ⛔ **E la differenza conta:** `fine - inizio` di un'oscillazione puo' fare **zero**
    anche quando l'escursione e' grande. ### **L'escursione e' cio' che la verifica esterna
    ha misurato sul banco**, e si misura la stessa cosa per poter confrontare.
    """
    return tuple(float(serie[:, c].max() - serie[:, c].min()) for c in (1, 2, 3))

def secolare(serie):
    """### `(pendenza, ampiezza, rapporto)`: ### **deriva SECOLARE o OSCILLAZIONE?**

    ### ⭐ **Il criterio e' un rapporto e non un occhio:** si adatta una retta a `E(t)` e
    si confronta la **variazione che la retta spiega** con l'**ampiezza dei residui**.
    ### ✅ **`rapporto >> 1` vuol dire SECOLARE** *(la retta spiega quasi tutto)*;
    ### ⛔ **`rapporto << 1` vuol dire OSCILLANTE** *(la retta non spiega niente, e il
    segnale e' tutto nei residui)*.
    """
    t = serie[:, 0]
    e = serie[:, 1] - serie[0, 1]
    pend, quota = np.polyfit(t, e, 1)
    spiegata = abs(pend) * (t[-1] - t[0])
    residui = e - (pend * t + quota)
    amp = float(np.max(residui) - np.min(residui))
    return (float(pend), amp,
            spiegata / amp if amp > 0 else float("inf"))
