# -*- coding: utf-8 -*-
r"""**IL RIUSO DELLA FATTORIZZAZIONE DI GAUSS** *(Luca `2026-11-15` `14:05`, ripetuto alle `15:07`; la profilazione `c3bb6534`: la risoluzione sparsa `0.64 s` per tick)*.

### **Un ADATTATORE, fuori dal nucleo:** **`accendi()` sostituisce IN MEMORIA `p6_u_breve.gauss_sparso` con `gauss_sparso_riuso`: lo STESSO conto** *(`D` la divergenza sparsa, il Laplaciano `D D^T`, `phi` del nodo `0`
fissato, poi la media tolta, `E = D^T phi`)*, **ma `D`, il Laplaciano e la sua FATTORIZZAZIONE si fanno UNA volta per campo** *(`scipy.sparse.linalg.factorized`)* **e si riusano** *(`D` dipende solo da `ii`, `jj`: la
topologia, che non cambia)*. **`spegni()` rimette l'originale.** **Chi lo chiama:** **`mattone.Campi.gauss`** *(`PB.gauss_sparso`, dal modulo)*. ### **Se sia AL BIT con `spsolve`: lo dice `prova_gauss.py`.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import p6_u_breve as PB  # noqa: E402

_ORIGINALE = PB.gauss_sparso
CACHE = {"campo": None, "D": None, "risolvi": None, "costruite": 0}


def gauss_sparso_riuso(campo, b):
    """### **`p6_u_breve.gauss_sparso` riga per riga**, con `D` e la fattorizzazione conservate per il campo."""
    import scipy.sparse.linalg as spl
    b = np.asarray(b, dtype=float)
    assert abs(float(b.sum())) <= 1e-12 * float(np.sum(np.abs(b))) + 1e-300, "b NON e' a media nulla: Gauss sul toro non ha soluzione"
    if CACHE["campo"] is not campo:
        D = PB.matrice_div_sparsa(campo)
        Lap = (D @ D.T).tocsc()
        CACHE.update(campo=campo, D=D, risolvi=spl.factorized(Lap[1:, 1:]), costruite=CACHE["costruite"] + 1)
    D = CACHE["D"]
    phi = np.zeros(campo.n)
    phi[1:] = CACHE["risolvi"](b[1:])
    phi -= phi.mean()
    E = D.T @ phi
    return E, D


def accendi():
    PB.gauss_sparso = gauss_sparso_riuso


def spegni():
    PB.gauss_sparso = _ORIGINALE
    CACHE.update(campo=None, D=None, risolvi=None)
