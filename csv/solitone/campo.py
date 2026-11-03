# -*- coding: utf-8 -*-
r"""**FIN DOVE ARRIVA IL CAMPO: I PROFILI AD ANELLI E LA PORTATA** *(Luca, `2026-11-03` `18:26`; il task history `doc/TASK_HISTORY/2026-11-03_campo_TM1000.md`)*.
### **Gli anelli:** l'anello `k` sono i nodi con `k <= r < k + 1` attorno al centro periodico *(l'immagine piu' vicina, `toro.scarti`)*, `k = 0 .. ceil(R) - 1`, `r < R` *(`R` la meta'
del periodo)*; ### **la media per anello** e' la media sui nodi dell'anello. ### **La portata** di un profilo per una soglia: `R_contiguo`, il bordo interno del primo anello dal centro in
fuori la cui media NON supera la soglia *(«entro cui supera»)*, e `R_ultimo`, il bordo esterno dell'ultimo anello che la supera; `nan` per `R_contiguo` se non scende mai *(oltre `R`)*.
"""
import math

import numpy as np

from . import toro as TO


def quanti(R):
    """### **Il numero degli anelli** fino a `R`: `ceil(R)` *(l'ultimo, `[floor(R), R)`, e' tagliato)*."""
    return int(math.ceil(R))


def anelli(m1, m2, c1, c2, L, R):
    """### **`(k, r)`:** l'anello di ogni nodo *(`-1` oltre `R`)* e la distanza dal centro `(c1, c2)` *(gli indici)*, con l'immagine piu' vicina."""
    D = TO.scarti(m1, m2, c1, c2, L)
    r = np.hypot(D[:, 0], D[:, 1])
    k = np.floor(r).astype(np.int64)
    k[r >= R] = -1
    return k, r


def profilo(x, k, n):
    """### **La media di `x` per anello** *(`n` anelli; `nan` dove un anello e' vuoto)*."""
    m = k >= 0
    s = np.bincount(k[m], weights=np.asarray(x, dtype=float)[m], minlength=n)[:n]
    c = np.bincount(k[m], minlength=n)[:n]
    with np.errstate(invalid="ignore", divide="ignore"):
        return s / c


def portata(prof, soglia):
    """### **`(R_contiguo, R_ultimo)`** del profilo per la soglia *(la definizione nel docstring del modulo)*."""
    sopra = np.asarray(prof) > soglia
    giu = np.nonzero(~sopra)[0]
    su = np.nonzero(sopra)[0]
    return (float(giu[0]) if len(giu) else float("nan")), (float(su[-1] + 1) if len(su) else 0.0)
