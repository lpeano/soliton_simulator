# -*- coding: utf-8 -*-
"""L'HAMILTONIANA — **somma i termini: `H` e `dH/dpsi*`, in UN SOLO POSTO.**

> ### ⭐ **PERCHE' UN SOLO POSTO:** se la somma dei termini stesse in due punti *(uno per
> `H`, uno per il gradiente)*, ### **le due somme potrebbero divergere** — e un gradiente
> che non è il gradiente di quella `H` ### **non si vede guardando il codice: si vede solo
> misurando.**

### ⛔ **E LA SOMMA HA UN ORDINE CANONICO, PER ID.** `float` non è associativo: sommare
`a+b+c` e `c+b+a` dà ### **bit diversi**. ### **L'ordine per ID rende la somma
riproducibile**, e il collaudo prova che ### **permutare i termini lascia lo stato
BYTE-IDENTICO.**

### ⚠ **E I TERMINI SI CARICANO DA `termini/`, letti via `LEGGE`:** l'elenco
### **non si scrive a mano qui** — sarebbe ### **un terzo posto** dove una legge può
esistere o mancare, e `P-E1` ne conosce ### **tre.**
"""
import importlib.util
import math
import os

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
TERMINI = os.path.join(_QUI, "termini")


def carica_termini():
    """### I moduli di `termini/` che dichiarano `LEGGE`, ### **in ordine di ID.**"""
    fuori = []
    for f in sorted(os.listdir(TERMINI)):
        if not f.endswith(".py") or f == "__init__.py":
            continue
        p = os.path.join(TERMINI, f)
        spec = importlib.util.spec_from_file_location("_t_" + f[:-3], p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        if hasattr(m, "LEGGE"):
            fuori.append(m)
    # ### ⛔ **L-ORDINE CANONICO E- PER ID**, non per nome di file: il nome del file e-
    # ### ### **una conseguenza** dell-ID, e se un giorno cambiasse la regola di nomina
    # ### ### **l-ordine della somma cambierebbe senza che nessuno lo decida.**
    return sorted(fuori, key=lambda m: m.LEGGE)


def energia(st, ii, jj, termini):
    """### `H(psi)`, ### **sommata in ordine canonico per ID.**

    ### ⭐ **Con `math.fsum`**: la somma ### **ad arrotondamento esatto** non dipende
    dall-ordine degli addendi, quindi ### **due permutazioni danno lo STESSO bit** -- e
    l-ordine canonico resta ### **come seconda difesa**, non come unica.
    """
    # ### \u26d4 **NESSUN DEFAULT** *(punto `15(b)`)*: `termini` ### **si passa**,
    # ### e chi non lo passa ### **ha un errore**, non un comportamento a sorpresa.
    t = sorted(termini, key=lambda m: m.LEGGE)
    pezzi = []
    for m in t:
        pezzi.append(m.energia(st, ii, jj))
    return math.fsum(pezzi)


def gradiente_grezzo(st, ii, jj, termini):
    """### Il gradiente ### **NELL-ORDINE DATO**, senza riordinare.

    ### ⛔ **Esiste SOLO per il collaudo**, e serve a provare che l-ordine canonico
    ### **fa un lavoro vero**: con questa funzione una permutazione
    ### **cambia i bit**, e con `gradiente()` ### **no.**
    ### ⚠ **La fisica NON la chiama**: `passo.py` usa `gradiente()`.
    """
    fuori = {k: np.zeros_like(v) for k, v in st.items()}
    for m in termini:
        m.gradiente(st, fuori, ii, jj)
    return fuori


def gradiente(st, ii, jj, termini):
    """### `dH/dpsi*`, ### **accumulato in ordine canonico per ID.**

    ### ⚠ **Qui `fsum` NON si puo- usare:** gli addendi sono ### **array complessi**, e
    `fsum` lavora su scalari reali. ### ➜ **Resta l-ordine canonico**, e il collaudo
    ### **misura** che una permutazione dia lo stesso bit *(e se un giorno non lo dara-,
    il collaudo lo dira- invece di lasciarlo scoprire)*.
    """
    # ### ⛔ **L-ORDINE CANONICO SI IMPONE ANCHE SU UNA LISTA DATA, e PORTA CARICO:**
    # ### misurato, ### **permutare gli addendi del gradiente NON da- lo stesso bit**
    # ### *(a differenza di `H`, che usa `fsum`)*. ### **Quindi il `sorted` non e- un
    # ### ornamento: e- cio- che rende la somma RIPRODUCIBILE.**
    # ### ⚠ **E il collaudo misura ENTRAMBE le cose:** che una lista permutata dia
    # ### ### **lo stesso bit** *(perche- si riordina)*, e che la somma ### **grezza**
    # ### ### **non lo dia** -- ### **altrimenti il primo braccio sarebbe un FALSO-UNO**,
    # ### vero per costruzione e non per misura.
    # ### \u26d4 **NESSUN DEFAULT** *(punto `15(b)`)*.
    t = sorted(termini, key=lambda m: m.LEGGE)
    fuori = {k: np.zeros_like(v) for k, v in st.items()}
    for m in t:
        m.gradiente(st, fuori, ii, jj)
    return fuori
