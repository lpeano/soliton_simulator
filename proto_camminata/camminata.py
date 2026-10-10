# -*- coding: utf-8 -*-
"""LA CAMMINATA A MONETA — **moneta, spostamento, e la CONIUGAZIONE DI CARICA.**

**Un tick, e non c'e' niente altro:**

    psi' = SPOSTAMENTO( NONLINEARE( MONETA_DI_BANDA( GROVER( psi ) ) ) )

| | il pezzo | che cos'e' | dove vive |
|---|---|---|---|
| `GROVER` | `(2/d)·Σ_estremita − I`, **identica sulle due componenti** | **invariante per permutazione** delle estremita' del nodo | dentro UN nodo |
| `MONETA_DI_BANDA` | `exp(-i dτ_k σ_z)`, cioe' `diag(e^{-iθ}, e^{+iθ})` | **separa le due bande** di un angolo `∝ dτ_k`: ### **e' la massa** | dentro UN nodo |
| `NONLINEARE` | una fase `exp(-i φ_k)` | `nonlineare.py`, e la condizione su `φ` e' **secca** | dentro UN nodo |
| `SPOSTAMENTO` | scambio di `2a` e `2a+1` | ### **tutti gli archi INSIEME**: nessuno strato, nessun ordine | su UN arco |

### ⛔ **NESSUNO STRATO E NESSUN ORDINE FRA NODI:** la moneta e' **diagonale a blocchi per
nodo** e lo spostamento e' **una permutazione**, quindi **non esiste un <<ordine di
esecuzione>>** da dichiarare — ed e' esattamente cio' che `A17` chiede *(«l'ordine di
esecuzione non e' fisica»)*.

### ⭐ **LA CONIUGAZIONE DI CARICA: `C ψ = σ_x ψ*`** *(scambio delle bande + coniugazione)*, e
la derivazione sta nel task history. ### **Con lei la camminata LINEARE e' simmetrica AL BIT**,
e il braccio `0` lo misura.

### ⚠ **NESSUN `clip`, NESSUN pavimento, NESSUNA proiezione in questo file** — e un braccio del
collaudo lo verifica **sul sorgente**, perche' un clip **violerebbe `A14` per costruzione**.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import scena as SC                                             # noqa: E402

EPS = float(np.finfo(float).eps)


def stato_zero(sc):
    """### Lo stato: **un'ampiezza a due componenti per ogni ESTREMITA' d'arco.**"""
    return np.zeros((2 * sc["m"], 2), dtype=complex)


def stato_casuale(sc, seme):
    """Uno stato casuale **normalizzato**: serve ai bracci di simmetria."""
    rng = np.random.default_rng(seme)
    psi = (rng.standard_normal((2 * sc["m"], 2))
           + 1j * rng.standard_normal((2 * sc["m"], 2)))
    return psi / math.sqrt(float(np.sum(np.abs(psi) ** 2)))


def somma_per_nodo(psi, sc, esatta=False):
    """### La somma delle ampiezze **sulle estremita' di ogni nodo**.

    ### ⭐ **DUE MODI, e la differenza e' MISURATA, non supposta:** con `numpy` la somma
    dipende dall'ORDINE in virgola mobile *(quindi una rinumerazione cambia gli ultimi bit)*;
    con `math.fsum` la somma e' **ESATTA**, quindi l'isotropia diventa **esatta AL BIT.**

    ### ⚠ **E- una scelta di SOMMATORIA, non una manopola di fisica:** in aritmetica esatta
    i due modi danno **lo stesso numero**, e `hamiltoniana.py` dell'era `2` usa gia' `fsum`
    per la stessa ragione.
    """
    n = sc["n"]
    if not esatta:
        S = np.zeros((n, 2), dtype=complex)
        np.add.at(S, sc["nodo"], psi)
        return S
    S = np.zeros((n, 2), dtype=complex)
    per = [[] for _ in range(n)]
    for e, k in enumerate(sc["nodo"].tolist()):
        per[k].append(e)
    for k in range(n):
        ee = per[k]
        for c in (0, 1):
            re = math.fsum(float(psi[e, c].real) for e in ee)
            im = math.fsum(float(psi[e, c].imag) for e in ee)
            S[k, c] = complex(re, im)
    return S


def moneta_grover(psi, sc, esatta=False):
    """### `(2/d)·Σ − I` sulle estremita' del nodo, **identica sulle due bande.**

    ### ⛔ **E- UNITARIA PER QUALUNQUE GRADO**, perche' e' `2|u><u| − I` con `|u>` il
    vettore uniforme: una **riflessione**. ### ✅ **E- la ragione per cui la norma si
    conserva senza che io debba normalizzare niente** *(`A11`: nessuna cura dove non c'e'
    un errore)*.
    """
    S = somma_per_nodo(psi, sc, esatta)
    k = sc["nodo"]
    peso = (2.0 / sc["grado"][k]).reshape(-1, 1)
    return peso * S[k] - psi


def moneta_banda(psi, dtau_nodo, sc):
    """### `exp(-i dτ_k σ_z)`: le due bande prendono **fasi opposte.** E' la massa."""
    th = dtau_nodo[sc["nodo"]]
    out = np.empty_like(psi)
    out[:, 0] = psi[:, 0] * np.exp(-1j * th)
    out[:, 1] = psi[:, 1] * np.exp(+1j * th)
    return out


def moneta_banda_globale(psi, dt):
    """### La moneta di banda **a `dt` GLOBALE**: un angolo SOLO, uguale per tutti.

    ### ⛔ **ESISTE SOLO PER IL BRACCIO DELLA LETTURA `6`**, e per questo e- scritta
    ### **come un-altra strada**: prende ### **uno scalare**, non un array per nodo.
    ### ⭐ **E- cosi- che il braccio vale qualcosa:** se riusassi la stessa funzione
    con `r = 1` proverei ### **che `1` moltiplica come `1`**, non che il tempo proprio
    locale ### **non ha cambiato niente dove non doveva.**
    """
    out = np.empty_like(psi)
    out[:, 0] = psi[:, 0] * complex(np.exp(-1j * dt))
    out[:, 1] = psi[:, 1] * complex(np.exp(+1j * dt))
    return out


def passo_dt_globale(psi, sc, dt, esatta=False):
    """### Un tick con la moneta di banda a `dt` GLOBALE. ### **Il confronto della
    lettura `6`.**"""
    x = moneta_grover(psi, sc, esatta)
    x = moneta_banda_globale(x, dt)
    return spostamento(x)


def spostamento(psi):
    """### Scambia le due estremita' di **ogni** arco, **tutte insieme.**"""
    v = psi.reshape(-1, 2, 2)
    return v[:, ::-1, :].reshape(-1, 2).copy()


def coniuga(psi):
    """### **`C ψ = σ_x ψ*`**: scambia le bande e coniuga. ### `C² = I`."""
    return np.conj(psi)[:, ::-1].copy()


def passo(psi, sc, r, dt, g=0.0, nonlin=None, esatta=False):
    """### UN TICK. ### ⚠ **`dtau_k = r_k · dt`**, e il `dt` nudo sta **solo** nel cono."""
    dtau = r * dt
    x = moneta_grover(psi, sc, esatta)
    x = moneta_banda(x, dtau, sc)
    if nonlin is not None and g != 0.0:
        x = nonlin(x, sc, g, dtau)
    return spostamento(x)


def corri(psi, sc, r, dt, passi, g=0.0, nonlin=None, esatta=False, osserva=None):
    """`passi` tick. ### **`osserva(t, psi)` LEGGE e non scrive** *(`A17`)*."""
    fuori = []
    if osserva is not None:
        fuori.append(osserva(0, psi))
    for t in range(1, passi + 1):
        psi = passo(psi, sc, r, dt, g, nonlin, esatta)
        if osserva is not None:
            fuori.append(osserva(t, psi))
    return psi, fuori


# =====================================================================================
#   LE GRANDEZZE -- tutte LOCALI, e tutte LETTE
# =====================================================================================
def norma(psi):
    return float(np.sum(np.abs(psi) ** 2))


def rho_nodo(psi, sc):
    """### `ρ_k`: la densita' del nodo, somma sulle sue estremita' e sulle due bande."""
    out = np.zeros(sc["n"], dtype=float)
    np.add.at(out, sc["nodo"], np.sum(np.abs(psi) ** 2, axis=1))
    return out


def s_nodo(psi, sc):
    """### `s_k = ρ₊ − ρ₋`: lo **SBILANCIAMENTO DI BANDA**, ed e' **dispari sotto `C`.**"""
    out = np.zeros(sc["n"], dtype=float)
    np.add.at(out, sc["nodo"], np.abs(psi[:, 0]) ** 2 - np.abs(psi[:, 1]) ** 2)
    return out


def quasi_energia(psi, sc, r, dt, g=0.0, nonlin=None):
    """### `<psi|U|psi>`: per la camminata **lineare** `U` e' unitaria e questa e'
    **conservata**. ### ⚠ **Per le non lineari NON e' garantita**, ed e' la lettura `3`."""
    u = passo(psi, sc, r, dt, g, nonlin)
    return complex(np.sum(np.conj(psi) * u))


if __name__ == "__main__":
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = SC.irregolare()
    r = SC.ritmi(sc, 11)
    psi = stato_casuale(sc, 11)
    print("  scena: %s   estremita-: %d" % (sc["nome"], 2 * sc["m"]))
    print("  norma iniziale: %.17g" % norma(psi))
    fine, _ = corri(psi, sc, r, 1.0, 60)
    print("  norma dopo 60 tick: %.17g   (scarto %.3g)"
          % (norma(fine), abs(norma(fine) - 1.0)))
    a = coniuga(passo(psi, sc, r, 1.0))
    b = passo(coniuga(psi), sc, r, 1.0)
    print("  simmetria C della LINEARE: max|C(U psi) - U(C psi)| = %.3g"
          % float(np.max(np.abs(a - b))))
    # ### ⭐ **L-IMPRONTA: serve al braccio del DETERMINISMO FRA DUE PROCESSI.**
    # ### ⚠ **Si stampa su richiesta**, perche- un numero che compare sempre
    # ### ### **finisce copiato senza il suo comando.**
    if "--impronta" in sys.argv:
        import hashlib
        fine2, _ = corri(psi, sc, r, 1.0, 60)
        print("  IMPRONTA dopo 60 tick: %s"
              % hashlib.sha1(np.ascontiguousarray(fine2).tobytes()).hexdigest())
