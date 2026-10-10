r"""LA NON LINEARITA' SATURANTE — **HAMILTONIANA, SENZA `g`, e col FLUSSO ESATTO.**

**Decisione di Luca, `2026-10-11`.** L'energia locale e'

    N_k = Lambda_k * G(x_k),    x_k = h_k / Lambda_k,    G(x) = x - arctan(x)

con `h_k` l'**elicita'** del nodo *(il `v2`)* e `Lambda_k` la **densita' del vuoto** *(il
`v3`)*.

> ## ⭐ **IL FLUSSO SI INTEGRA ESATTAMENTE, E IL MOTIVO STA IN DUE INVARIANTI.**
> `dN/dh = G'(x)` manda lo spinore in una **rotazione attorno al SUO versore**, e una rotazione
> attorno a `n` lascia `s.n` **invariante** ⟹ **`h` non cambia.**
> `dN/dLambda = b(x)` manda il vuoto in una **fase**, e una fase lascia `|phi|^2`
> ⟹ **`Lambda` non cambia.**
> ### ✅ **Quindi `x`, `G'` e `b` sono COSTANTI durante il flusso**, e l'integrale e'
> **in forma chiusa**: una rotazione di `G'(x) dtau` e una fase di `b(x) dtau`.

| | la funzione | la forma | la parita' sotto `C` |
|---|---|---|---|
| `G` | `x - arctan x` | **dispari** | `N` e' **DISPARI** |
| `G'` | `x^2/(1+x^2)` | ### **PARI, e LIMITATA in `[0,1)`** | l'angolo **non cambia** |
| `b` | `x/(1+x^2) - arctan x` | ### **DISPARI** | la fase del vuoto **commuta** |

### ⭐ **E LA SATURAZIONE E' `G'` LIMITATA, non una legge a parte:** sotto il vuoto *(`|x|`
piccolo)* `G' ~ x^2` e **quasi niente accade**; attorno a `|x| ~ 1` **si lega**; molto sopra
`G' -> 1` e **smette di crescere**. ### ⛔ **E' la barriera di degenerazione della decisione
`1`, SENZA una legge in piu'.**

### ⚠ **IL LIMITE `Lambda -> 0` SI GESTISCE COL LIMITE, NON CON UN PAVIMENTO** *(`A11`)*:
`G' -> 1`, `b -> -(pi/2) sign(h)`, `N -> h - (pi/2) Lambda sign(h)` — **tutto finito.**
### ✅ **Nel codice: `Lambda == 0.0` ESATTO usa la forma limite**, e per `Lambda > 0` la
formula e' esatta. **Nessun epsilon, nessun clip.**

### ⛔ **E NON C'E' NESSUN `g`:** conta **solo il rapporto `h/Lambda`**. Resta `eps`
*(spin-direzione)*, **scansionato**.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402
import nonlineare2 as N2                                       # noqa: E402
import vuoto3 as V3                                            # noqa: E402

PIMEZZI = 0.5 * math.pi


def G(x):
    """`G(x) = x - arctan x`: **dispari**, e cresce come `x^3/3` all'origine."""
    return x - np.arctan(x)


def Gp(x):
    """`G'(x) = x^2/(1+x^2)`: ### **PARI e LIMITATA** — e' **la saturazione.**"""
    return (x * x) / (1.0 + x * x)


def b(x):
    """`b(x) = dN/dLambda = x/(1+x^2) - arctan x`: ### **DISPARI.**"""
    return x / (1.0 + x * x) - np.arctan(x)


def pezzi(h, lam):
    """### `(angolo per unita' di tempo, fase per unita' di tempo)`, **col limite.**

    ### ⛔ **DOVE `Lambda == 0.0` ESATTO si usa la forma limite** *(`G' = 1`,
    `b = -(pi/2) sign(h)`)*: ### **non e' un pavimento, e' il valore che la funzione
    PRENDE la'.**
    """
    buoni = lam > 0.0
    al = np.ones_like(lam)
    be = -PIMEZZI * np.sign(h)
    if np.any(buoni):
        x = h[buoni] / lam[buoni]
        al[buoni] = Gp(x)
        be[buoni] = b(x)
    return al, be


def energia(h, lam):
    """### `N_k`, **col limite** `Lambda -> 0`: `N -> h - (pi/2) Lambda sign(h)`."""
    buoni = lam > 0.0
    out = h - PIMEZZI * lam * np.sign(h)
    if np.any(buoni):
        out[buoni] = lam[buoni] * G(h[buoni] / lam[buoni])
    return out


def _ruota_attorno_a_n(psi, geo, ang):
    """`exp(-i ang (sigma.n))` per **estremita'**: `cos I - i sin (sigma.n)`."""
    c = np.cos(ang)
    s = np.sin(ang)
    n = geo["n"]
    a0 = n[:, 2] * psi[:, 0] + (n[:, 0] - 1j * n[:, 1]) * psi[:, 1]
    a1 = (n[:, 0] + 1j * n[:, 1]) * psi[:, 0] - n[:, 2] * psi[:, 1]
    out = np.empty_like(psi)
    out[:, 0] = c * psi[:, 0] - 1j * s * a0
    out[:, 1] = c * psi[:, 1] - 1j * s * a1
    return out


def flusso(psi, phi, sc, geo, dtau):
    """### **IL FLUSSO ESATTO di `N` per un tempo `dtau`** *(un array per nodo)*.

    ### ✅ **Una rotazione e una fase, e nient'altro:** niente integratore, niente passo,
    niente troncamento. ### **E il suo inverso e' `dtau -> -dtau`.**
    """
    h = N2.elicita_nodo(psi, sc, geo)
    lam = V3.lambda_nodo(phi, sc)
    al, be = pezzi(h, lam)
    ang = (al * dtau)[sc["nodo"]]
    fas = (be * dtau)[sc["nodo"]]
    return _ruota_attorno_a_n(psi, geo, ang), phi * np.exp(-1j * fas)


# =====================================================================================
#   I DUE CONTROLLI, dichiarati -- e ognuno DEVE fare una cosa precisa
# =====================================================================================
def flusso_su_rho(psi, phi, sc, geo, dtau):
    """### **CONTROLLO che DEVE ROMPERE `C`:** la stessa saturazione **su `rho`**.

    ### ⛔ **`rho` e' PARI sotto `C`**, e `dN/drho` moltiplica `psi` *(non `(sigma.n)psi`)*
    ⟹ e' una **fase scalare PARI** ⟹ ### **rompe `C`**, per lo stesso conto del `v2`.
    """
    rho = CM.rho_nodo(psi, sc)
    lam = V3.lambda_nodo(phi, sc)
    al, be = pezzi(rho, lam)
    fas = (al * dtau)[sc["nodo"]]
    fav = (be * dtau)[sc["nodo"]]
    return psi * np.exp(-1j * fas).reshape(-1, 1), phi * np.exp(-1j * fav)


def flusso_v2(psi, phi, sc, geo, dtau, g=1.0):
    """### **CONTROLLO del `v2`:** la fase `exp(-i g h dtau)`, ### **NON hamiltoniana.**

    ### ⚠ **Non viene da nessun `N`:** e' una fase messa a mano, e la lettura `(3)` dice
    che ### **DEVE far DERIVARE** l'energia.
    """
    h = N2.elicita_nodo(psi, sc, geo)
    fas = (g * h * dtau)[sc["nodo"]]
    return psi * np.exp(-1j * fas).reshape(-1, 1), phi


LE_TRE = (
    ("N", flusso, "la saturazione HAMILTONIANA su h/Lambda: la candidata"),
    ("rho", flusso_su_rho, "la stessa saturazione su rho: PARI, DEVE rompere C"),
    ("v2", flusso_v2, "la fase non hamiltoniana del v2: DEVE far derivare l-energia"),
)


if __name__ == "__main__":
    import geometria as GE
    import scena as SC
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    # ### LE DERIVATE, VERIFICATE NUMERICAMENTE invece che credute
    print("  LE DERIVATE DI N, verificate con una differenza centrata:")
    hh, ll, d = 0.7, 1.3, 1e-6
    dh = (energia(np.array([hh + d]), np.array([ll]))[0]
          - energia(np.array([hh - d]), np.array([ll]))[0]) / (2 * d)
    dl = (energia(np.array([hh]), np.array([ll + d]))[0]
          - energia(np.array([hh]), np.array([ll - d]))[0]) / (2 * d)
    x = hh / ll
    print("     dN/dh  numerica %.10f   formula G'(x)  %.10f   scarto %.3g"
          % (dh, Gp(x), abs(dh - Gp(x))))
    print("     dN/dL  numerica %.10f   formula b(x)   %.10f   scarto %.3g"
          % (dl, b(x), abs(dl - b(x))))
    print("  LA SATURAZIONE: G'(x) per x = 1/8, 1, 8, 64:  %s"
          % "  ".join("%.6f" % Gp(np.array([v]))[0] for v in (0.125, 1.0, 8.0, 64.0)))
    print("  IL LIMITE Lambda -> 0:  G'(inf) = %.6f   b(inf) = %.6f   (-pi/2 = %.6f)"
          % (Gp(np.array([1e12]))[0], b(np.array([1e12]))[0], -PIMEZZI))
    # ### GLI INVARIANTI DEL FLUSSO, misurati
    sc = SC.irregolare()
    geo = GE.scena_identita(sc)
    psi = CM.stato_casuale(sc, 11)
    phi = V3.vuoto_fondo(sc)
    h0 = N2.elicita_nodo(psi, sc, geo)
    l0 = V3.lambda_nodo(phi, sc)
    p1, f1 = flusso(psi, phi, sc, geo, np.full(sc["n"], 0.37))
    h1 = N2.elicita_nodo(p1, sc, geo)
    l1 = V3.lambda_nodo(f1, sc)
    print("  GLI INVARIANTI del flusso:  max|h - h'| = %.3g   max|Lambda - Lambda'| = %.3g"
          % (float(np.max(np.abs(h0 - h1))), float(np.max(np.abs(l0 - l1)))))
    print("  e le norme:  psi %.3g   phi %.3g"
          % (abs(CM.norma(p1) - CM.norma(psi)),
             abs(V3.norma_vuoto(f1) - V3.norma_vuoto(phi))))
