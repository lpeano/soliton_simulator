# -*- coding: utf-8 -*-
r"""**IL VUOTO SULLA CARTA** *(il mandato di Luca delle `01:04` del `2026-11-02`, passo `2`; il task history `doc/TASK_HISTORY/2026-11-02_solitone_vestito.md`)*:
### **le bande del vuoto linearizzato attorno a `F0`** *(il tick INTERO del nucleo con `psi = 0`)*, ### **e dove cade una frequenza rispetto a quelle bande, col margine.**

### **Con `psi = 0` e `cs` spento il tick sul vuoto e' LINEARE** *(`CAMM-FASE-VUOTO` ha generatore `cs_primo(Lambda) * (...)`, nullo; `CAMM-MATERIA-VUOTO` con `S1` ha
### `alpha = beta = 0` dove `rho = 0`)*: restano `GROVER-VUOTO` e `SPOSTAMENTO-VUOTO`. ### **Lo verifica `test_vuoto` (`V1`), non si suppone.**
### ⚠ **`phi_h` e' ordinato per ARCO** *(`2a`, `2a+1`)*, non per nodo: `celle` ricostruisce `(nodo, tipo)` dalla direzione dell'arco, come `_vuoto_sul_fondo.fondo_uniforme`.
"""
import math

import numpy as np


def celle(inc, L):
    """### **`(idx, dirs)`:** `idx[v, 2 d + r]` e' l'estremita' del nodo `v` sull'arco di direzione `dirs[d]`, `r = 0` la CODA, `1` la TESTA."""
    n = inc.n
    v = np.arange(n)
    m1, m2 = v // L, v % L
    pos_a, segno_a = [], []
    for a in range(inc.m):
        i, j = int(inc.nodo[2 * a]), int(inc.nodo[2 * a + 1])
        d = ((int(m1[j] - m1[i]) + L // 2) % L - L // 2, (int(m2[j] - m2[i]) + L // 2) % L - L // 2)
        pos = d if (d[0] > 0 or (d[0] == 0 and d[1] > 0)) else (-d[0], -d[1])
        pos_a.append(pos)
        segno_a.append(pos == d)
    dirs = sorted(set(pos_a))
    assert len(dirs) == 3, dirs
    idx = np.full((n, 6), -1, dtype=int)
    for a in range(inc.m):
        k = dirs.index(pos_a[a])
        coda, testa = (2 * a, 2 * a + 1) if segno_a[a] else (2 * a + 1, 2 * a)
        for e, r in ((coda, 0), (testa, 1)):
            assert idx[int(inc.nodo[e]), 2 * k + r] == -1, "due estremita' nello stesso posto"
            idx[int(inc.nodo[e]), 2 * k + r] = e
    assert np.all(idx >= 0) and len(set(idx.ravel().tolist())) == 2 * inc.m
    return idx, dirs


def a_celle(phi, idx, L):
    return phi[idx].reshape(L, L, 6)


def da_celle(c, idx, L):
    out = np.empty(idx.size, dtype=complex)
    out[idx.ravel()] = c.reshape(-1)
    return out


def tick_vuoto(z, phi):
    """### **Il tick INTERO del nucleo con `psi = 0`** *(come `_vuoto_vivo_B.corsa`: `SF.forma(VC.FORMA)`, `BE.conv(DC.ZERO)`, `tick.percorri_tick`)*: `phi` dopo un tick.
    ### **La scena si rimette com'era** *(ogni array di `z["st"]`)*."""
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    try:
        z["st"]["psi_h"][...] = 0.0
        z["st"]["phi_h"][...] = phi
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))
        assert not np.any(z["st"]["psi_h"]), "con psi = 0 il tick ha creato materia"
        return z["st"]["phi_h"].copy()
    finally:
        for k, v in salvato.items():
            z["st"][k][...] = v


def matrice(z, idx):
    """### **`A_v(k)` `(L, L, 6, 6)`:** le risposte a un impulso unitario nel nodo `0`, tipo per tipo, `fft2` *(come `_dove_va_la_materia.matrice` per la materia)*."""
    L = z["L"]
    A = np.empty((L, L, 6, 6), dtype=complex)
    for c in range(6):
        p = np.zeros(idx.size, dtype=complex)
        p[idx[0, c]] = 1.0
        A[:, :, :, c] = np.fft.fft2(a_celle(tick_vuoto(z, p), idx, L), axes=(0, 1))
    return A


def applica(A, phi, idx, L):
    """### **`ifft(A_v fft(phi))`:** il tick ricostruito dalla matrice di Bloch."""
    fh = np.fft.fft2(a_celle(phi, idx, L), axes=(0, 1))
    return da_celle(np.fft.ifft2(np.einsum("abij,abj->abi", A, fh), axes=(0, 1)), idx, L)


def bande(A, s):
    """### **Le `6` bande come intervalli sul cerchio delle frequenze** `-arg/s` *(mod `2 pi/s`)*: il taglio nel mezzo del gap piu' largo di TUTTO lo spettro, poi la
    `j`-esima frequenza a ogni `k` *(continua in `k`)*. ### **`(taglio, intervalli [lo, hi] misurati dal taglio, il gap piu' largo)`.**
    ### ⚠ **I bordi sono quelli della griglia `L x L`** *(con `L` multiplo di `3`, `Gamma`, `K` e `K'` ci sono)*."""
    P = 2.0 * math.pi / s
    lam = np.linalg.eigvals(A.reshape(-1, 6, 6))
    f = np.mod(-np.angle(lam) / s, P)
    tutte = np.sort(f.ravel())
    gaps = np.diff(np.concatenate([tutte, [tutte[0] + P]]))
    g = int(np.argmax(gaps))
    taglio = float(np.mod(tutte[g] + 0.5 * gaps[g], P))
    rel = np.sort(np.mod(f - taglio, P), axis=1)
    return taglio, [(float(rel[:, j].min()), float(rel[:, j].max())) for j in range(6)], float(gaps[g])


def unione(inter):
    """### **Gli intervalli fusi** *(misurati dal taglio)*."""
    tutte = sorted(inter)
    fusi = [list(tutte[0])]
    for lo, hi in tutte[1:]:
        if lo <= fusi[-1][1]:
            fusi[-1][1] = max(fusi[-1][1], hi)
        else:
            fusi.append([lo, hi])
    return fusi


def margine(freq, taglio, inter, s):
    """### **`(dentro, margine, bande)`:** il margine e' la distanza dal bordo di banda piu' vicino, ### **negativo se dentro** *(la profondita')*."""
    P = 2.0 * math.pi / s
    x = float(np.mod(freq - taglio, P))
    dentro = [j for j, (lo, hi) in enumerate(inter) if lo <= x <= hi]
    if dentro:
        return True, -max(min(x - inter[j][0], inter[j][1] - x) for j in dentro), dentro
    return False, min(min(abs(x - lo), abs(x - hi)) for lo, hi in inter), []


def frequenza(z, phi, s):
    """### **`(nu, residuo, |lambda| - 1)`** di `phi` sotto il tick del vuoto: `lambda = <phi, T phi>/<phi, phi>`, `nu = -arg(lambda)/s` mod `2 pi/s`."""
    T = tick_vuoto(z, phi)
    lf = complex(np.vdot(phi, T) / np.vdot(phi, phi))
    return (float(np.mod(-math.atan2(lf.imag, lf.real) / s, 2.0 * math.pi / s)), float(np.linalg.norm(T - lf * phi) / np.linalg.norm(phi)), abs(lf) - 1.0)
