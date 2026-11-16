# -*- coding: utf-8 -*-
r"""**IL PERCHE' DELL'ULP DEL SECONDO PASSO** *(la carta `doc/TASK_HISTORY/2026-11-15_motore_numba.md`, sez. `13`; N1; SOLO MISURA)*.

    E:\python\py3132\python.exe csv/solitone/prova_numba_ulp.py > doc/referti_l2/motore_numba_ulp.txt     (NUMBA_CACHE_DIR su E:, PYTHONNOUSERSITE=1, TMP su E:)

**H1:** **i cicli SIMD di numpy per il prodotto COMPLESSO usano una FMA**; numba con `fastmath=False` no.
**H2:** **l'`einsum` somma in un altro ordine.** **H3:** **la promozione reale -> complesso di numpy diversa da `complex(x, 0)`.**
**Come si legge** *(fissato nella carta, prima)*: **H1 VERA se numpy coincide con una variante FMA in TUTTI gli elementi e numba con la formula semplice in tutti;
FALSA se numpy coincide con la formula semplice; altrimenti nessuna conclusione.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)

N = 200000          # ### la lunghezza dei vettori lunghi
NC = 20000          # ### il campione per math.fma e per gli scalari di Python (un ciclo in Python)


def quota(a, b):
    """### la frazione degli elementi UGUALI al bit, e quanti diversi."""
    u = int(np.count_nonzero(a == b))
    return "%d su %d uguali (%d diversi)" % (u, a.size, a.size - u)


def main():
    import _presidio
    _presidio.avvia(__file__)
    from numba import njit
    import numba
    print("=" * 130)
    print("IL PERCHE' DELL'ULP (sez. 13): numpy %s, numba %s; sys.executable %s" % (np.__version__, numba.__version__, sys.executable))
    print("### la CPU e numpy: np.show_runtime() (le estensioni SIMD trovate e quelle usate)")
    sys.stdout.flush()
    np.show_runtime()
    sys.stdout.flush()
    print("=" * 130)
    rng = np.random.default_rng(13)
    a = rng.standard_normal(N) + 1j * rng.standard_normal(N)
    b = rng.standard_normal(N) + 1j * rng.standard_normal(N)
    ar, ai, br, bi = a.real.copy(), a.imag.copy(), b.real.copy(), b.imag.copy()

    # ### H1
    p_np = np.multiply(a, b)
    re_s = ar * br - ai * bi                                   # ### la formula semplice: ogni operazione un ufunc, ogni risultato arrotondato
    im_s = ar * bi + ai * br
    print("### H1, IL PRODOTTO COMPLESSO, vettori lunghi (%d):" % N)
    print("  numpy contro la formula semplice:   la parte reale %s; l'immaginaria %s" % (quota(p_np.real, re_s), quota(p_np.imag, im_s)))
    s = slice(0, NC)
    f1 = np.array([math.fma(x, y, -(u * v)) for x, y, u, v in zip(ar[s], br[s], ai[s], bi[s])])
    f2 = np.array([math.fma(-u, v, x * y) for x, y, u, v in zip(ar[s], br[s], ai[s], bi[s])])
    g1 = np.array([math.fma(x, v, u * y) for x, y, u, v in zip(ar[s], br[s], ai[s], bi[s])])
    g2 = np.array([math.fma(u, y, x * v) for x, y, u, v in zip(ar[s], br[s], ai[s], bi[s])])
    print("  numpy contro le FMA (i primi %d):   reale fma(ar,br,-ai*bi) %s; fma(-ai,bi,ar*br) %s" % (NC, quota(p_np.real[s], f1), quota(p_np.real[s], f2)))
    print("                                      immag fma(ar,bi,ai*br) %s; fma(ai,br,ar*bi) %s" % (quota(p_np.imag[s], g1), quota(p_np.imag[s], g2)))

    @njit(fastmath=False, error_model="numpy")
    def k_mul(x, y, out):
        for i in range(x.shape[0]):
            out[i] = x[i] * y[i]
    p_nb = np.empty_like(a)
    k_mul(a, b, p_nb)
    print("  numba contro la formula semplice:   reale %s; immag %s" % (quota(p_nb.real, re_s), quota(p_nb.imag, im_s)))
    print("  numba contro numpy:                 %s" % quota(p_nb, p_np))
    p_py = np.array([complex(x) * complex(y) for x, y in zip(a[s], b[s])])
    print("  Python scalare contro semplice:     reale %s; immag %s" % (quota(p_py.real, re_s[s]), quota(p_py.imag, im_s[s])))
    corti = np.empty(2000, complex)
    for i in range(2000):
        corti[i] = np.multiply(a[i:i + 1], b[i:i + 1])[0]
    print("  numpy CORTO (1 elemento) contro numpy lungo: %s; contro la formula semplice: reale %s" % (quota(corti, p_np[:2000]), quota(corti.real, re_s[:2000])))

    fma_tutti = bool(np.array_equal(p_np.real[s], f1) or np.array_equal(p_np.real[s], f2)) and bool(np.array_equal(p_np.imag[s], g1) or np.array_equal(p_np.imag[s], g2))
    semplice_np = bool(np.array_equal(p_np.real, re_s) and np.array_equal(p_np.imag, im_s))
    semplice_nb = bool(np.array_equal(p_nb.real, re_s) and np.array_equal(p_nb.imag, im_s))
    if fma_tutti and semplice_nb and not semplice_np:
        v1 = "H1 VERA: numpy = una variante FMA in tutti gli elementi del campione; numba = la formula semplice in tutti"
    elif semplice_np:
        v1 = "H1 FALSA: numpy = la formula semplice"
    else:
        v1 = "NESSUNA CONCLUSIONE su H1 (numpy FMA in tutti: %s; numba semplice in tutti: %s; numpy semplice: %s)" % (fma_tutti, semplice_nb, semplice_np)
    print("  ### %s" % v1)

    # ### H3: il reale per il complesso
    x = rng.standard_normal(N)
    p3 = np.multiply(x, b)
    print("### H3, REALE x COMPLESSO: numpy contro (x*br, x*bi): reale %s; immag %s" % (quota(p3.real, x * br), quota(p3.imag, x * bi)))
    p3n = np.empty_like(b)

    @njit(fastmath=False, error_model="numpy")
    def k_mul_r(x, y, out):
        for i in range(x.shape[0]):
            out[i] = complex(x[i], 0.0) * y[i]
    k_mul_r(x, b, p3n)
    print("  numba complex(x,0)*b contro numpy: %s" % quota(p3n, p3))

    # ### H2: l'einsum a due fattori
    m = N // 4
    U = (rng.standard_normal((m, 2, 2)) + 1j * rng.standard_normal((m, 2, 2)))
    v = (rng.standard_normal((m, 2)) + 1j * rng.standard_normal((m, 2)))
    e1 = np.einsum("aij,aj->ai", U, v)
    e_m = (0 + U[:, :, 0] * v[:, 0:1]) + U[:, :, 1] * v[:, 1:2]
    print("### H2, L'EINSUM aij,aj->ai (%d): contro (0 + U0 v0) + U1 v1 in numpy: %s" % (m, quota(e1, e_m)))

    @njit(fastmath=False, error_model="numpy")
    def k_ein(U, v, out):
        for a_ in range(U.shape[0]):
            for i in range(2):
                t = 0j
                t = t + U[a_, i, 0] * v[a_, 0]
                t = t + U[a_, i, 1] * v[a_, 1]
                out[a_, i] = t
    e_n = np.empty_like(v)
    k_ein(U, v, e_n)
    print("  il ciclo numba contro l'einsum: %s; contro (0 + U0 v0) + U1 v1 in numpy: %s" % (quota(e_n, e1), quota(e_n, e_m)))
    print("=" * 130)
    print("ESITO: %s" % v1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
