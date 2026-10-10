# -*- coding: utf-8 -*-
"""LE NON LINEARITA' DEL `v2` — **e la candidata e' L'ELICITA'.**

> ## ⛔ **IL PROBLEMA, posto dal mandato:** la fase dispari del `v1` usava `ρ₀ − ρ₁`, e
> ## **le rotazioni `SU(2)` ora MESCOLANO le due componenti** — quindi quella grandezza
> ## **non e' piu' invariante.** Serve una grandezza **locale**, **invariante di gauge**
> ## *(`SU(2)` e `U(1)`)* e **DISPARI sotto `C`**.

### ⭐ **LA RISPOSTA, derivata nel task history PRIMA di scrivere questo file:**

| la grandezza | `U(1)` | `SU(2)` locale | sotto `C` | serve? |
|---|---|---|---|---|
| `ρ = ψ†ψ` | **invariante** | **invariante** | ### **PARI** | ### ⛔ e' la `(A)` |
| `s = ψ†σψ` | **invariante** | ### **RUOTA** | ### **DISPARI** | ### ⛔ non da sola |
| ### **`s·n`** | **invariante** | ### ✅ **INVARIANTE** | ### ✅ **DISPARI** | ### ⭐ **SI'** |

### ⭐ **E QUELLA GRANDEZZA HA UN NOME: E' L'ELICITA'** — **lo spin proiettato sulla direzione
dell'arco**, vista dal nodo. ### **`s` e `n` ruotano INSIEME** sotto una trasformazione di
gauge *(il versore e' il riferimento locale)*, quindi il prodotto **non cambia**; e `s` e'
dispari sotto `C`, quindi il prodotto lo e'.

### ⛔ **E QUESTO E' IL SECONDO MOTIVO PER CUI I VERSORI SERVONO, e non era nel mandato:**
senza una direzione **non esiste** uno scalare locale invariante di gauge e dispari sotto `C`
— ### **la non linearita' simmetrica non si potrebbe nemmeno SCRIVERE.**

### ⚠ **`g` NON SI TARA:** si **scansiona** su potenze di due *(`PROVV-U-FISSE-TRE-SCENE` e il
punto `2c` del mandato)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402

# ### ⛔ **LE `g` E GLI `eps` DELLA SCANSIONE, DICHIARATI, e tutti POTENZE DI DUE.**
# ### **Lo `0` c-e- di proposito in entrambe: e- il CONTROLLO dentro la scansione.**
G_SCANSIONE = (0.0, 0.25, 0.5, 1.0, 2.0)
EPS_SCANSIONE = (0.0, 0.25, 0.5, 1.0)


def spin_estremita(psi):
    """### `s_h = ψ†σψ` per ogni estremita': **tre numeri REALI.**"""
    a = psi[:, 0]
    b = psi[:, 1]
    sx = 2.0 * np.real(np.conj(a) * b)
    sy = 2.0 * np.imag(np.conj(a) * b)
    sz = np.abs(a) ** 2 - np.abs(b) ** 2
    return np.stack((sx, sy, sz), axis=1)


def elicita_estremita(psi, geo):
    """### `s_h · n_h`: ### **lo spin proiettato sulla direzione**, per estremita'."""
    return np.sum(spin_estremita(psi) * geo["n"], axis=1)


def elicita_nodo(psi, sc, geo):
    """### `h_k`: l'elicita' **sommata sulle estremita' del nodo.**"""
    out = np.zeros(sc["n"], dtype=float)
    np.add.at(out, sc["nodo"], elicita_estremita(psi, geo))
    return out


def _fase_per_nodo(psi, sc, phi_nodo):
    f = np.exp(-1j * phi_nodo[sc["nodo"]]).reshape(-1, 1)
    return psi * f


def fase_pari2(psi, sc, geo, g, dtau):
    """### **`(A)`**: `φ_k = g·ρ_k·dτ_k`. ### ⛔ **PARI sotto `C` ⟹ ROMPE `C`.**"""
    return _fase_per_nodo(psi, sc, g * CM.rho_nodo(psi, sc) * dtau)


def fase_elicita(psi, sc, geo, g, dtau):
    """### **`(B)`**: `φ_k = g·h_k·dτ_k` con `h` l'ELICITA'.

    ### ✅ **Invariante di gauge e DISPARI sotto `C`**, quindi la fase commuta con `C`
    *(una fase scalare commuta con `C` se e solo se e' dispari)*.
    """
    return _fase_per_nodo(psi, sc, g * elicita_nodo(psi, sc, geo) * dtau)


LE_DUE_V2 = (
    ("A", fase_pari2, "PARI sotto C (la densita-): ROMPE C -- il braccio che DEVE fallire"),
    ("B", fase_elicita, "DISPARI sotto C (l-ELICITA-): invariante di gauge -- la candidata"),
)


if __name__ == "__main__":
    import camminata2 as C2
    import geometria as GE
    import scena as SC
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = SC.irregolare()
    r = SC.ritmi(sc, 11)
    psi = CM.stato_casuale(sc, 11)
    print("  la simmetria `C` delle due non linearita-, su un tick, g=1, eps=0.5:")
    for nome, geo in (("identita", GE.scena_identita(sc)),
                      ("curva", GE.scena_curva(sc, 11))):
        for et, f, nota in LE_DUE_V2:
            a = C2.coniuga2(C2.passo2(psi, sc, geo, r, 1.0, 0.5, 1.0, f))
            b = C2.passo_coniugato(C2.coniuga2(psi), sc, geo, r, 1.0, 0.5, 1.0, f)
            print("     %-9s (%s)  |C U - U* C| = %.3g      %s"
                  % (geo["nome"], et, float(np.max(np.abs(a - b))), nota[:46]))
    # ### e l-INVARIANZA DI GAUGE dell-elicita-, misurata
    g0 = GE.scena_identita(sc)
    g1 = GE.scena_gauge_puro(sc, 11)
    h0 = elicita_nodo(psi, sc, g0)
    # ### lo stato ruotato col gauge: `psi -> g_k psi`
    ruot = np.empty_like(psi)
    for e in range(2 * sc["m"]):
        k = int(sc["nodo"][e])
        ruot[e] = g1["g"][k] @ psi[e]
    h1 = elicita_nodo(ruot, sc, g1)
    print("  l-ELICITA- e- invariante di gauge? max|h - h'| = %.3g"
          % float(np.max(np.abs(h0 - h1))))
    h2 = elicita_nodo(ruot, sc, {"n": g1["n_non_ruotati"]})
    print("  e SENZA ruotare i versori?        max|h - h''| = %.3g   ### deve essere GRANDE"
          % float(np.max(np.abs(h0 - h2))))
