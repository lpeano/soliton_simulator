# -*- coding: utf-8 -*-
"""LE DUE NON LINEARITA' DI PROVA — **e la condizione su `φ` e' SECCA.**

> ## ⛔ **UNA FASE SCALARE `exp(-iφ)` COMMUTA CON `C` SOLO SE `φ` E' DISPARI SOTTO `C`.**
> Il conto, con `C ψ = σ_x ψ*`:
>
>     C (e^{-iφ(ψ)} ψ) = e^{+iφ(ψ)} Cψ        e        e^{-iφ(Cψ)} (Cψ)
>
> ### **Sono uguali se e solo se `φ(Cψ) = −φ(ψ)`.**

| | la fase | parita' sotto `C` | l'esito |
|---|---|---|---|
| **`(A)`** | `φ_k = g · ρ_k · dτ_k`, con `ρ = ρ₊ + ρ₋` | ### **PARI** *(`C` scambia le bande: la somma non cambia)* | ### ⛔ **ROMPE `C`**, ed e' **il braccio che DEVE fallire** la lettura `5` |
| **`(B)`** | `φ_k = g · s_k · dτ_k`, con `s = ρ₊ − ρ₋` | ### **DISPARI** *(`C` scambia le bande: la differenza cambia segno)* | ### ✅ **RISPETTA `C`** |

### ⭐ **E `(B)` NON E' UN TRUCCO ALGEBRICO:** su un cluster **tutto nella banda `+`** vale
`s = ρ`, quindi **`(B)` agisce ESATTAMENTE come `(A)`**; sul suo coniugato nella banda `−`
vale `s = −ρ`, quindi la fase **cambia segno** — che e' **esattamente cio' che serve perche'
il coniugato evolva coniugato.** ### ⛔ **`(A)` invece da' la STESSA fase alle due bande, e
cosi' TIENE una e DISFA l'altra.**

### ⚠ **E `g` NON SI TARA:** si **SCANSIONA** su potenze di due *(`{0, 1/4, 1/2, 1, 2}`)*,
perche' un fenomeno che vive in una finestra stretta di `g` e' **imposto** *(`A1`, e la terza
domanda della stella polare)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402

# ### ⛔ **LE `g` DELLA SCANSIONE, DICHIARATE, e tutte POTENZE DI DUE** *(cosi' `g·x` non
# ### aggiunge arrotondamento suo)*. ### **`0` c'e- di proposito: e- la camminata LINEARE**,
# ### cioe- il controllo dentro la stessa scansione.
G_SCANSIONE = (0.0, 0.25, 0.5, 1.0, 2.0)


def _fase_per_nodo(psi, sc, phi_nodo):
    """### Applica `exp(-i φ_k)` a **tutte le estremita'** del nodo `k`, **uguale sulle due
    bande** -- perche' una fase **scalare** e' scalare anche nello spinore."""
    f = np.exp(-1j * phi_nodo[sc["nodo"]]).reshape(-1, 1)
    return psi * f


def fase_pari(psi, sc, g, dtau):
    """### **`(A)`**: `φ_k = g · ρ_k · dτ_k`. ### ⛔ **PARI sotto `C` ⟹ rompe `C`.**"""
    return _fase_per_nodo(psi, sc, g * CM.rho_nodo(psi, sc) * dtau)


def fase_dispari(psi, sc, g, dtau):
    """### **`(B)`**: `φ_k = g · s_k · dτ_k`, con `s = ρ₊ − ρ₋`.

    ### ✅ **DISPARI sotto `C` ⟹ rispetta `C`**, e la scelta e' MIA, motivata nel task
    history: ### **e' l'unico scalare DISPARI che si costruisce da uno spinore a due
    componenti senza aggiungere niente.**
    """
    return _fase_per_nodo(psi, sc, g * CM.s_nodo(psi, sc) * dtau)


# ### ⚠ **E SI DICHIARANO IN UNA TABELLA**, perche- le letture ci girano sopra e
# ### ### **una lista scritta a mano in tre posti diverge.**
LE_DUE = (
    ("A", fase_pari, "PARI sotto C: rompe C -- il braccio che DEVE fallire"),
    ("B", fase_dispari, "DISPARI sotto C: rispetta C -- la candidata"),
)


if __name__ == "__main__":
    import scena as SC
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = SC.irregolare()
    r = SC.ritmi(sc, 11)
    psi = CM.stato_casuale(sc, 11)
    print("  la simmetria `C`, misurata su un tick, per g = 1:")
    for nome, f, nota in LE_DUE:
        a = CM.coniuga(CM.passo(psi, sc, r, 1.0, 1.0, f))
        b = CM.passo(CM.coniuga(psi), sc, r, 1.0, 1.0, f)
        print("     (%s)  max|C(U psi) - U(C psi)| = %.3g      %s"
              % (nome, float(np.max(np.abs(a - b))), nota))
