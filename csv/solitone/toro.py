# -*- coding: utf-8 -*-
r"""**LE MISURE SUL TORO** *(Luca, `2026-11-02`, dopo `455b9a95`; il task history `doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`, sez. `11`)*: ### **il centro periodico e le
misure centrate li'.**

### **Il toro** *(`_energia_del_legame.stato`)*: il nodo `v` ha gli indici `m1 = v // L`, `m2 = v % L`, e la posizione `(m1 - L//2) A1 + (m2 - L//2) A2`
*(`A1`, `A2` di `_solitoni_triangoli`)*: ### **un ROMBO a `60` gradi, coi periodi `L A1`, `L A2`, `L (A1 + A2)`.**
### **Il centro:** la media circolare sugli indici, `c = L/(2 pi) arg sum rho e^{i 2 pi m/L}`, per `m1` e per `m2`.
### **Le distanze:** lo scarto per indice riportato in `[-L/2, L/2)`, poi ### **la piu' corta fra le `9` immagini** `(k1, k2)` in `{-1, 0, 1}^2` *(col rombo, riportare ogni
indice da solo non basta)*. ### **Le misure: le stesse espressioni** di `_salti_nel_cuore.campione` e `_congelato_lungo.punto`; cambia solo la distanza.
"""
import math

import numpy as np

SETTORI = 8                    # ### i settori angolari attorno al centro (il task history, sez. 11: avanti e dietro col passo di 45 gradi)


def vettori():
    import _solitoni_triangoli as STR
    return np.asarray(STR.A1, dtype=float), np.asarray(STR.A2, dtype=float)


def immagini(L):
    """### **I vettori del toro** `L (k1 A1 + k2 A2)`, `(k1, k2)` in `{-1, 0, 1}^2`: `(9, 2)`."""
    A1, A2 = vettori()
    return np.array([L * (k1 * A1 + k2 * A2) for k1 in (-1, 0, 1) for k2 in (-1, 0, 1)])


def meta_periodo(L):
    """### **La meta' del periodo piu' corto del toro** *(il raggio del cerchio inscritto nella cella di Wigner-Seitz)*, ### **dai vettori del toro.**"""
    im = immagini(L)
    n = np.hypot(im[:, 0], im[:, 1])
    return 0.5 * float(n[n > 0].min())


def posizioni(m1, m2, L):
    A1, A2 = vettori()
    return (np.asarray(m1) - L // 2)[:, None] * A1 + (np.asarray(m2) - L // 2)[:, None] * A2


def centro(rho, m1, m2, L):
    """### **Il centro periodico:** `(c1, c2)` in `[0, L)` *(gli indici)* e la posizione `(x, y)`, con `c - L//2` riportato in `[-L/2, L/2)`."""
    k = 2.0 * math.pi / L
    cc = []
    for m in (m1, m2):
        z = complex(np.sum(rho * np.exp(1j * k * m)))
        cc.append((math.atan2(z.imag, z.real) / k) % L)
    A1, A2 = vettori()
    q = [((c - L // 2 + 0.5 * L) % L) - 0.5 * L for c in cc]
    p = q[0] * A1 + q[1] * A2
    return cc[0], cc[1], float(p[0]), float(p[1])


def piu_vicina(D, L):
    """### **Gli scarti `D` `(n, 2)` gia' riportati per indice, ridotti all'immagine piu' vicina.**"""
    im = immagini(L)
    tutti = D[:, None, :] + im[None, :, :]
    j = np.argmin(np.sum(tutti ** 2, axis=2), axis=1)
    return tutti[np.arange(len(D)), j]


def scarti(m1, m2, c1, c2, L):
    """### **Lo scarto di ogni nodo dal centro, con l'immagine piu' vicina:** `(n, 2)`."""
    A1, A2 = vettori()
    d1 = ((np.asarray(m1) - c1 + 0.5 * L) % L) - 0.5 * L
    d2 = ((np.asarray(m2) - c2 + 0.5 * L) % L) - 0.5 * L
    return piu_vicina(d1[:, None] * A1 + d2[:, None] * A2, L)


def distanza(p, q, L):
    """### **La distanza fra due posizioni sul toro, con l'immagine piu' vicina.**"""
    A1, A2 = vettori()
    B = np.column_stack([A1, A2])
    a = np.linalg.solve(B, np.asarray(p, dtype=float) - np.asarray(q, dtype=float))
    a = ((a + 0.5 * L) % L) - 0.5 * L
    D = piu_vicina((a[0] * A1 + a[1] * A2)[None, :], L)
    return float(np.hypot(D[0, 0], D[0, 1]))


def misure(rho, m1, m2, L, w_in, w0, h):
    """### **Le misure centrate sul centro periodico** *(le espressioni di `_salti_nel_cuore.campione` e `_congelato_lungo.punto`)*:
    `({"c1", "c2", "x", "y", "w", "f_win", "f_liscia", "alone"}, D, M)`."""
    M = float(rho.sum())
    c1, c2, x, y = centro(rho, m1, m2, L)
    D = scarti(m1, m2, c1, c2, L)
    d = np.hypot(D[:, 0], D[:, 1])
    w = math.sqrt(float(rho @ np.sum(D ** 2, axis=1)) / M)
    g = np.clip((w_in + 0.5 * h - d) / h, 0.0, 1.0)
    return {"c1": c1, "c2": c2, "x": x, "y": y, "w": w, "f_win": float(rho[d <= w_in].sum()) / M, "f_liscia": float(rho @ g) / M,
            "alone": 1.0 - float(rho[d <= 3.0 * w0].sum()) / M}, D, M


def settore(D):
    """### **Il settore di ogni nodo** *(`0 .. SETTORI-1`, l'angolo da `x` in senso antiorario, `45` gradi ciascuno)*."""
    a = np.arctan2(D[:, 1], D[:, 0]) % (2.0 * math.pi)
    return np.minimum((a / (2.0 * math.pi / SETTORI)).astype(int), SETTORI - 1)


def alone_settori(rho, D, M, w0):
    """### **L'alone per settore:** la massa fuori da `3 w0` in ciascun settore, sulla massa totale."""
    s = settore(D)
    fuori = np.hypot(D[:, 0], D[:, 1]) > 3.0 * w0
    return [float(rho[(s == j) & fuori].sum()) / M for j in range(SETTORI)]


def maschere_settori(D):
    s = settore(D)
    return {"s%d" % j: s == j for j in range(SETTORI)}
