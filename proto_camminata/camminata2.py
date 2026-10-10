# -*- coding: utf-8 -*-
"""LA CAMMINATA `v2` — **lo spin si lega al moto, e il trasporto e' `U(2)`.**

**Un tick, e non c'e' niente altro** *(decisione di Luca, voce `SPIN-LEGATO-AL-MOTO`)*:

    psi' = SPOSTAMENTO_CON_TRASPORTO( NONLINEARE( GROVER( MONETA_DI_SPIN( psi ) ) ) )

| | il pezzo | la forma | dove vive |
|---|---|---|---|
| `1` | **moneta di SPIN** | `exp(-i α σ·n_{k,a}) = cos α I − i sin α (σ·n)`, `α = eps·dτ_k` | **UNA estremita'** |
| `2` | **GROVER** | `(2/d)Σ − I`, **uguale sulle due componenti** | dentro UN nodo |
| `3` | **non linearita'** | una fase per nodo *(`nonlineare2.py`)* | dentro UN nodo |
| `4` | **SPOSTAMENTO con TRASPORTO** | `ψ'[partner(h)] = U[h] ψ[h]`, **tutti gli archi insieme** | su UN arco |

### ⭐ **LA DIFFERENZA COL `v1` E' TUTTA NEL PEZZO `1` E NEL PEZZO `4`:** nel `v1` la moneta di
banda era **diagonale** e lo spostamento **non toccava lo spinore**, quindi le due componenti
**non si mescolavano mai** *(misurato: un braccio del collaudo del `v1` lo dice)*. ### **Qui
`σ·n` NON e' diagonale** *(a meno che `n = ±ẑ`)* e **`U` mescola durante il trasporto.**

### ⛔ **LA CONIUGAZIONE DI CARICA E' `C ψ = i σ_y ψ*`**, e la derivazione sta nel task history:
**commuta con tutto `SU(2)`** *(quindi con la moneta di spin e col trasporto geometrico)*, e
### **INVERTE la fase `U(1)`** — cioe' manda la camminata **nell'anti-camminata.**

### ⚠ **NESSUN `clip`, NESSUN pavimento in questo file**, e un braccio lo verifica sul sorgente.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402
import geometria as GE                                         # noqa: E402
import scena as SC                                             # noqa: E402

EPS = float(np.finfo(float).eps)


def moneta_spin(psi, geo, eps, dtau, sc):
    """### `exp(-i eps dτ_k σ·n)` **per ESTREMITA'**: e' qui che spin e direzione si legano.

    ### ⭐ **E- ESATTA, non un'esponenziale numerica:** `exp(-i α σ·n) = cos α I − i sin α
    (σ·n)` perche' `(σ·n)² = I` quando `|n| = 1`. ### **Quindi nessun errore di troncamento,
    e la forma e' UNITARIA al bit.**
    """
    if eps == 0.0:
        return psi
    al = eps * dtau[sc["nodo"]]
    c = np.cos(al)
    s = np.sin(al)
    n = geo["n"]
    # ### (sigma.n) applicato a (psi0, psi1), scritto a mano per non costruire 416 matrici
    a0 = n[:, 2] * psi[:, 0] + (n[:, 0] - 1j * n[:, 1]) * psi[:, 1]
    a1 = (n[:, 0] + 1j * n[:, 1]) * psi[:, 0] - n[:, 2] * psi[:, 1]
    out = np.empty_like(psi)
    out[:, 0] = c * psi[:, 0] - 1j * s * a0
    out[:, 1] = c * psi[:, 1] - 1j * s * a1
    return out


def spostamento_trasporto(psi, geo, sc):
    """### Scambia le due estremita' di ogni arco **trasportando**, tutte insieme.

    ### ⛔ **`U_jk = U_kj^†` NON e' una convenzione: e' cio' che rende lo spostamento
    UNITARIO.** Senza quella, la norma non si conserverebbe — e si vedrebbe subito.
    """
    U = geo["U"]
    v = psi.reshape(-1, 2, 2)                 # (arco, lato, componente)
    out = np.empty_like(v)
    # ### il lato `0` (su `u`) va sul lato `1` (su `v`) trasportato da `U`
    out[:, 1, :] = np.einsum("aij,aj->ai", U, v[:, 0, :])
    # ### e il lato `1` torna sul lato `0` con `U^dagger`
    out[:, 0, :] = np.einsum("aji,aj->ai", np.conj(U), v[:, 1, :])
    return out.reshape(-1, 2)


def coniuga2(psi):
    """### **`C ψ = i σ_y ψ*`**: `(ψ₀, ψ₁) → (conj(ψ₁), −conj(ψ₀))`. ### `C² = −I`.

    ### ⚠ **`C² = −I` e NON `+I`**, e non e' un difetto: e' la **doppia copertura**
    *(`DOPPIA-COP`)*. ### **Su un'osservabile bilineare non si vede**, e il braccio lo
    verifica invece di assumerlo.
    """
    out = np.empty_like(psi)
    out[:, 0] = np.conj(psi[:, 1])
    out[:, 1] = -np.conj(psi[:, 0])
    return out


def passo2(psi, sc, geo, r, dt, eps, g=0.0, nonlin=None, esatta=False):
    """### UN TICK del `v2`. ### **L'ordine e' quello del mandato**, e non ce n'e' un altro."""
    dtau = r * dt
    x = moneta_spin(psi, geo, eps, dtau, sc)
    x = CM.moneta_grover(x, sc, esatta)
    if nonlin is not None and g != 0.0:
        x = nonlin(x, sc, geo, g, dtau)
    return spostamento_trasporto(x, geo, sc)


def corri2(psi, sc, geo, r, dt, eps, passi, g=0.0, nonlin=None, osserva=None):
    fuori = []
    if osserva is not None:
        fuori.append(osserva(0, psi))
    for t in range(1, passi + 1):
        psi = passo2(psi, sc, geo, r, dt, eps, g, nonlin)
        if osserva is not None:
            fuori.append(osserva(t, psi))
    return psi, fuori


def passo_coniugato(psi, sc, geo, r, dt, eps, g=0.0, nonlin=None):
    """### Il passo della **ANTI-camminata**: la stessa scena con `θ → −θ`.

    ### ⭐ **Serve al braccio `0`:** con un campo `U(1)` acceso, `C` **non** e' una
    simmetria della singola camminata — manda la camminata **in questa.** ### **E la
    coniugata si costruisce prendendo `U*`**, perche' `(e^{iθ}V)* = e^{-iθ}V*` e `V*` sta
    ancora in `SU(2)`.
    """
    geo2 = dict(geo)
    # ### ⚠ **E LA COSTRUZIONE NON E- `U*`, come avevo scritto al primo giro:** il
    # ### conto dice `C M = M' C` con **`M' = sigma_y M* sigma_y^{-1}`**, e per
    # ### `M = exp(i t) V` quello fa **`exp(-i t) V`** -- cioe- **la stessa `V`** e
    # ### **la fase OPPOSTA**, non `V*`.
    # ### ✅ **E si ottiene con `U / det(U)`**, perche- `det(exp(i t) V) = exp(2i t)`.
    # ### ⭐ **MISURATO: con `U*` il braccio dava `0.16`; con `U/det(U)` da- ZERO.**
    det = np.linalg.det(geo["U"]).reshape(-1, 1, 1)
    geo2["U"] = geo["U"] / det
    return passo2(psi, sc, geo2, r, dt, eps, g, nonlin)


# =====================================================================================
#   LO SPETTRO -- la matrice del passo, costruita applicandolo alla base
# =====================================================================================
def matrice_passo(sc, geo, r, dt, eps):
    """### La matrice `(4m x 4m)` del passo **LINEARE**, colonna per colonna.

    ### ⚠ **Si costruisce APPLICANDO IL PASSO**, non riscrivendolo: cosi' la matrice e'
    ### **la stessa cosa** che gira nelle corse, e non una seconda implementazione che
    potrebbe divergere.
    """
    dim = 4 * sc["m"]
    M = np.zeros((dim, dim), dtype=complex)
    base = np.zeros((2 * sc["m"], 2), dtype=complex)
    for j in range(dim):
        base[:] = 0.0
        base[j // 2, j % 2] = 1.0
        M[:, j] = passo2(base, sc, geo, r, dt, eps).reshape(-1)
    return M


def quasi_energie(sc, geo, r, dt, eps):
    """### Gli autovalori del passo, come **quasi-energie** `ω = arg(λ)`, ordinate."""
    M = matrice_passo(sc, geo, r, dt, eps)
    lam = np.linalg.eigvals(M)
    return np.sort(np.angle(lam)), lam


def gap_massimo(om):
    """### `(gap massimo, spaziatura media)` sul **cerchio** delle quasi-energie."""
    o = np.sort(np.asarray(om, dtype=float))
    d = np.diff(o)
    # ### il cerchio si chiude: l-ultimo salto e- quello che passa per `pi`
    d = np.append(d, (o[0] + 2.0 * math.pi) - o[-1])
    return float(np.max(d)), float(np.mean(d))


if __name__ == "__main__":
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = SC.irregolare()
    r = SC.ritmi(sc, 11)
    psi = CM.stato_casuale(sc, 11)
    for nome, geo in (("identita", GE.scena_identita(sc)),
                      ("gauge_puro", GE.scena_gauge_puro(sc, 11)),
                      ("curva", GE.scena_curva(sc, 11))):
        fine, _ = corri2(psi, sc, geo, r, 1.0, 0.5, 60)
        a = coniuga2(passo2(psi, sc, geo, r, 1.0, 0.5))
        b = passo2(coniuga2(psi), sc, geo, r, 1.0, 0.5)
        c = passo_coniugato(coniuga2(psi), sc, geo, r, 1.0, 0.5)
        print("  %-11s norma %.17g   |C U - U C| = %.3g   |C U - U* C| = %.3g"
              % (nome, CM.norma(fine), float(np.max(np.abs(a - b))),
                 float(np.max(np.abs(a - c)))))
    # ### e il mescolamento delle componenti, che e- il punto del v2
    solo0 = psi.copy()
    solo0[:, 1] = 0.0
    solo0 /= math.sqrt(CM.norma(solo0))
    for eps in (0.0, 0.5):
        f, _ = corri2(solo0, sc, GE.scena_identita(sc), r, 1.0, eps, 60)
        print("  identita, eps=%.1f: |componente 1| MAX = %.3g"
              % (eps, float(np.max(np.abs(f[:, 1])))))
