# -*- coding: utf-8 -*-
r"""**LA PROVA CHE NUMBA FUNZIONA** *(Luca `2026-11-15` `12:32`, C4; nell'ambiente `E:\python\venv_numba`, NON in quello delle corse)*.

    E:\python\venv_numba\Scripts\python.exe csv/solitone/prova_numba.py > <scratchpad>/prova_numba.txt     (poi doc/referti_l2/numba_installazione.txt)

**Una funzione piccola con `@njit` su un array di complessi a doppia precisione** *(la somma dei moduli quadri, `n = 10^7`)*: **il tempo della prima chiamata** *(la compilazione)* **e della seconda; la stessa con
`parallel=True` e `prange`: i fili che usa** *(`numba.get_num_threads`, lo strato `numba.threading_layer`)*; **il risultato contro `numpy`** *(la differenza relativa: l'ordine delle somme cambia, NON al bit; dichiarato)*.
### **Nessun codice del simulatore** *(C6)*. **La macchina e' CARICA** *(le corse in giro)*: **i tempi sono indicativi.**
"""
import os
import sys
import time

import numpy as np


def main():
    import numba
    from numba import njit, prange

    @njit(cache=False)
    def somma(z):
        s = 0.0
        for i in range(z.shape[0]):
            s += z[i].real * z[i].real + z[i].imag * z[i].imag
        return s

    @njit(parallel=True, cache=False)
    def somma_par(z):
        s = 0.0
        for i in prange(z.shape[0]):
            s += z[i].real * z[i].real + z[i].imag * z[i].imag
        return s
    print("=" * 110)
    print("LA PROVA CHE NUMBA FUNZIONA (Luca 12:32, C4): Python %s; numpy %s (%s); numba %s; la macchina CARICA" % (sys.version.split()[0], np.__version__, os.path.dirname(np.__file__), numba.__version__))
    print("=" * 110)
    rng = np.random.default_rng(7)
    z = rng.standard_normal(10 ** 7) + 1j * rng.standard_normal(10 ** 7)
    t = time.perf_counter()
    rif = float(np.sum(np.abs(z) ** 2))
    t_np = time.perf_counter() - t
    for nome, f in (("@njit", somma), ("@njit(parallel=True) + prange", somma_par)):
        t = time.perf_counter()
        a = f(z)
        t1 = time.perf_counter() - t
        t = time.perf_counter()
        b = f(z)
        t2 = time.perf_counter() - t
        print("    %-32s la prima chiamata %.3f s (con la compilazione), la seconda %.4f s; il risultato %.15e, contro numpy %.3e relativo; due chiamate uguali al bit: %s"
              % (nome, t1, t2, b, abs(b - rif) / rif, a == b))
    print("    numpy np.sum(np.abs(z) ** 2): %.4f s" % t_np)
    print("### i fili: numba.get_num_threads() %d; NUMBA_NUM_THREADS %d; lo strato %s; os.cpu_count() %d" % (numba.get_num_threads(), numba.config.NUMBA_NUM_THREADS, numba.threading_layer(), os.cpu_count()))
    print("=" * 110)
    return 0


if __name__ == "__main__":
    sys.exit(main())
