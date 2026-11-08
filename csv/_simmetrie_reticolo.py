# -*- coding: utf-8 -*-
r"""**LE ROTAZIONI DEL RETICOLO A TRIANGOLI SUGLI SPINORI** *(Luca `2026-11-08` `14:19`, v1; il task history `doc/TASK_HISTORY/2026-11-08_zero_simmetrico_nel_nucleo.md`, sez. `2`)*.

### **Le mappe di `csv/solitone/carta_r60.py`** *(sigillata a `41fe6817`, `doc/referti_l2/simmetria_r60.txt` `13/13`)* **in un modulo di `csv/`**, perche' il collaudo del nucleo
*(`primo_ordine/_collauda_r60.py`)* **non puo' importare la libreria** *(`D6` della cassetta)*. ### ⚠ **DUE COPIE, dichiarate:** il collaudo controlla che queste mappe diano la `S`
derivata *(il nucleo della ricerca di dimensione `1`, coseno `1`)*, **cosi' la copia CONFRONTA.**
**`Rk`** = la rotazione di `60 k` gradi attorno al nodo `0`: i nodi `(m1, m2) -> (m1 - m2, m1)` *(`k` volte)*; l'estremita' di direzione uscente `j` nell'estremita' di
direzione `j + k` del nodo immagine; **`S` `6 c x 6 c`** per nodo nella base locale *(direzione x componente)*. **`S60 = exp(-i (pi/6) sigma_z)`.**
"""
import math

import numpy as np

S60 = np.diag([np.exp(-1j * math.pi / 6.0), np.exp(1j * math.pi / 6.0)])
SZ = np.diag([1.0 + 0j, -1.0])


def estremita_per_direzione(inc, nv):
    """### `ext[v, j]`: l'estremita' del nodo `v` con direzione uscente `j` *(l'angolo di `n` diviso `60` gradi)*; ALZA se un nodo non ha le sei direzioni."""
    ang = np.degrees(np.arctan2(nv[:, 1], nv[:, 0]))
    j = np.rint(ang / 60.0).astype(int) % 6
    assert float(np.max(np.abs(ang - 60.0 * np.rint(ang / 60.0)))) <= 1e-9, "una direzione non e' a multipli di 60 gradi"
    ext = -np.ones((inc.n, 6), dtype=np.int64)
    ext[inc.nodo, j] = np.arange(2 * inc.m)
    assert np.all(ext >= 0) and len(np.unique(ext)) == 2 * inc.m, "un nodo non ha le sei direzioni, una per estremita'"
    return ext


def mappa_nodi(L, k):
    """### il nodo immagine di ogni nodo per `R(60 k)` attorno al nodo `0`."""
    v = np.arange(L * L)
    m1, m2 = v // L, v % L
    for _ in range(k % 6):
        m1, m2 = (m1 - m2) % L, m1 % L
    return m1 * L + m2


def applica(x, ext, nm, S):
    """### `R_S` su `x` *(per estremita', `(2m, c)`)*: il vettore locale del nodo `v`, per `S`, nel nodo `nm[v]`."""
    c = x.shape[1]
    X = x[ext].reshape(ext.shape[0], 6 * c)
    out = np.empty_like(x)
    out[ext[nm]] = (X @ S.T).reshape(ext.shape[0], 6, c)
    return out


def S_derivata(k, spin):
    """### la permutazione `j -> j + k` delle direzioni `x` `spin`."""
    P = np.zeros((6, 6))
    for j in range(6):
        P[(j + k) % 6, j] = 1.0
    return np.kron(P, spin)
