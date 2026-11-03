# -*- coding: utf-8 -*-
r"""**FIN DOVE ARRIVA IL CAMPO: I PROFILI AD ANELLI E LA PORTATA** *(Luca, `2026-11-03` `18:26`; il task history `doc/TASK_HISTORY/2026-11-03_campo_TM1000.md`)*.
### **Gli anelli:** l'anello `k` sono i nodi con `k <= r < k + 1` attorno al centro periodico *(l'immagine piu' vicina fra le `9`, in indici: `anelli`)*, `k = 0 .. ceil(R) - 1`, `r < R` *(`R` la meta'
del periodo)*; ### **la media per anello** e' la media sui nodi dell'anello. ### **La portata** di un profilo per una soglia: `R_contiguo`, il bordo interno del primo anello dal centro in
fuori la cui media NON supera la soglia *(«entro cui supera»)*, e `R_ultimo`, il bordo esterno dell'ultimo anello che la supera; `nan` per `R_contiguo` se non scende mai *(oltre `R`)*.
"""
import math

import numpy as np



def quanti(R):
    """### **Il numero degli anelli** fino a `R`: `ceil(R)` *(l'ultimo, `[floor(R), R)`, e' tagliato)*."""
    return int(math.ceil(R))


def anelli(m1, m2, c1, c2, L, R):
    """### **`(k, r)`:** l'anello di ogni nodo *(`-1` oltre `R`)* e la distanza dal centro `(c1, c2)` *(gli indici)*, con l'immagine piu' vicina fra le `9`.
    ### **`r^2` dagli scarti in INDICI:** `|a A1 + b A2|^2 = a^2 + b^2 - a b` *(`A1 . A2 = -1/2`)*, ESATTO per scarti interi. ### **Perche' non in coordinate cartesiane** *(la
    cassetta `920c0ff7`, `C3`)*: con `sqrt 3 / 2` i primi vicini di un centro su un nodo uscivano a `1 - eps` e cadevano nell'anello `0` *(`5` nodi invece di `1`)*."""
    e1 = ((np.asarray(m1, dtype=float) - c1 + 0.5 * L) % L) - 0.5 * L
    e2 = ((np.asarray(m2, dtype=float) - c2 + 0.5 * L) % L) - 0.5 * L
    r2 = None
    for k1 in (-1, 0, 1):
        for k2 in (-1, 0, 1):
            a, b_ = e1 + k1 * L, e2 + k2 * L
            q = a * a + b_ * b_ - a * b_
            r2 = q if r2 is None else np.minimum(r2, q)
    r = np.sqrt(r2)
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


def multipoli(f, D, R):
    """### **I due poli di `f` entro `R` dal centro** *(`D` gli scarti, l'immagine piu' vicina; il task history `2026-11-03_TM3_campo_F3`)*: ### **il dipolo** `p = sum f D`, l'asse
    `atan2(p_y, p_x)` *(gradi)*, il modulo e il relativo `|p| / sum |f| |D|`; ### **il quadrupolo** `q = sum f (Dx + i Dy)^2`, l'asse `arg(q) / 2` *(gradi, modulo `180`)*, il modulo e il
    relativo `|q| / sum |f| |D|^2` *(`0` isotropo, `1` una retta)*."""
    f = np.asarray(f, dtype=float)
    r2 = D[:, 0] ** 2 + D[:, 1] ** 2
    m = r2 <= R * R
    f, D, r2 = f[m], D[m], r2[m]
    p = np.sum(f[:, None] * D, axis=0)
    zz = (D[:, 0] + 1j * D[:, 1]) ** 2
    q = complex(np.sum(f * zz))
    bp = float(np.sum(np.abs(f) * np.sqrt(r2)))
    bq = float(np.sum(np.abs(f) * r2))
    return {"p_asse": math.degrees(math.atan2(p[1], p[0])), "p": float(np.hypot(*p)), "p_rel": float(np.hypot(*p)) / bp if bp > 0 else float("nan"),
            "q_asse": 0.5 * math.degrees(math.atan2(q.imag, q.real)), "q": abs(q), "q_rel": abs(q) / bq if bq > 0 else float("nan"), "nodi": int(m.sum())}
