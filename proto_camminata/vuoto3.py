# -*- coding: utf-8 -*-
r"""IL VUOTO LOCALE DETERMINISTICO — **un'ampiezza NEUTRA sulle estremita' d'arco.**

**Forma PROVVISORIA dichiarata** *(voce `VUOTO-LOCALE-DETERMINISTICO`; decisione di Luca,
`2026-10-11`)*. E' **l'erede deterministico e locale dello scuotimento dell'era `1`** — e di
quello il repo dice una cosa precisa *(`ffb891f`)*: **iniettava VARIANZA, non lavoro.**

| | che cosa | perche' |
|---|---|---|
| `a` | un'ampiezza **SCALARE complessa `φ_h`** per estremita' d'arco | ### **NEUTRA**: niente spin, niente `U(1)` |
| `b` | **Grover la mescola** sulle estremita' del nodo | e' **la stessa moneta** dello spinore: ### **non una legge in piu'** |
| `c` | lo spostamento la porta **SENZA la matrice `U`** | e' neutra ⟹ ### **invariante di gauge PER COSTRUZIONE** |
| `d` | `Λ_k = Σ \|φ_h\|²` sulle estremita' del nodo | la **densita' del vuoto** |
| `e` | la localita' caratteristica e' ### **IL CONO** | **nessun raggio scelto**: un arco per tick |
| `f` | fondo **uniforme** `\|φ\|² = λ₀`, **fasi dal seme** | `Λ_k > 0` ovunque, e il caso **solo** nelle condizioni iniziali |

> ## ⛔ **`φ` NON SI MESCOLA CON `ψ`, E NON E' UNA PRECAUZIONE: E' IL GAUGE.**
> `ψ` si trasforma con `e^{iφ_k} g_k`, `φ` **no** *(e' neutra)*: mescolarle vorrebbe dire
> **sommare due cose che si trasformano diversamente.** ### ✅ **Si scambiano ENERGIA**, e lo
> fa `saturazione3.py` — **non ampiezza.**

### ⚠ **E LA STATISTICA DEI VICINI RESTA SOLO COME BRACCIO DI CONFRONTO** *(`Λ_k` = media di
`ρ` sui vicini, l'`u_nodo` dell'era `1`)*: ### **richiede di leggere i VICINI dentro la
moneta**, che e' una cosa che la camminata **non fa** — e il confronto serve a **misurare la
differenza**, non a usarlo.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402
import scena as SC                                             # noqa: E402

# ### ⛔ **IL FONDO DEL VUOTO, DICHIARATO:** e- una ### **SONDA**, non una costante di
# ### una legge, e le letture lo scansionano ### **attraverso `x0 = h/Lambda`.**
LAMBDA0 = 1.0


def vuoto_zero(sc):
    """### Nessun vuoto: serve ai bracci che spengono tutto."""
    return np.zeros(2 * sc["m"], dtype=complex)


def vuoto_fondo(sc, lam0=LAMBDA0, seme=11):
    """### Il fondo **uniforme in modulo**, con le **fasi dal seme.**

    ### ⚠ **Il caso sta SOLO qui**, nelle condizioni iniziali: il passo e'
    ### **deterministico.**
    """
    rng = np.random.default_rng(seme + 777)
    fasi = rng.random(2 * sc["m"]) * 2.0 * math.pi
    return math.sqrt(lam0) * np.exp(1j * fasi)


def lambda_nodo(phi, sc):
    """### `Λ_k`: la densita' del vuoto del nodo."""
    out = np.zeros(sc["n"], dtype=float)
    np.add.at(out, sc["nodo"], np.abs(phi) ** 2)
    return out


def grover_scalare(phi, sc, esatta=False):
    """### La **stessa** moneta di Grover, sullo scalare: `(2/d)Σ − I`."""
    s = np.zeros(sc["n"], dtype=complex)
    if esatta:
        per = [[] for _ in range(sc["n"])]
        for e, k in enumerate(sc["nodo"].tolist()):
            per[k].append(e)
        for k in range(sc["n"]):
            ee = per[k]
            s[k] = complex(math.fsum(float(phi[e].real) for e in ee),
                           math.fsum(float(phi[e].imag) for e in ee))
    else:
        np.add.at(s, sc["nodo"], phi)
    k = sc["nodo"]
    return (2.0 / sc["grado"][k]) * s[k] - phi


def spostamento_scalare(phi):
    """### Scambia le due estremita' di ogni arco, ### **SENZA matrice.**"""
    v = phi.reshape(-1, 2)
    return v[:, ::-1].reshape(-1).copy()


def norma_vuoto(phi):
    return float(np.sum(np.abs(phi) ** 2))


def lambda_dai_vicini(psi, sc):
    """### **IL BRACCIO DI CONFRONTO:** `Λ_k` come **media di `ρ` sui VICINI**.

    ### ⛔ **NON si usa nella dinamica**, e il motivo e' dichiarato: ### **richiede di
    leggere i vicini dentro la moneta**, cioe' una cosa che la camminata **non fa** — la
    camminata legge **le estremita' del proprio nodo** e nient'altro. ### ✅ **Serve a
    MISURARE la differenza**, non a sostituire il vuoto.
    """
    rho = CM.rho_nodo(psi, sc)
    out = np.zeros(sc["n"], dtype=float)
    for k in range(sc["n"]):
        vic = sc["vicini"][k]
        out[k] = float(np.mean(rho[list(vic)])) if vic else 0.0
    return out


if __name__ == "__main__":
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = SC.irregolare()
    phi = vuoto_fondo(sc)
    lam = lambda_nodo(phi, sc)
    print("  vuoto: %d estremita-, norma %.17g" % (len(phi), norma_vuoto(phi)))
    print("  Lambda_k: min %.6f  max %.6f  (il grado va da %d a %d)"
          % (lam.min(), lam.max(), sc["grado"].min(), sc["grado"].max()))
    # ### la moneta e lo spostamento conservano la norma?
    a = grover_scalare(phi, sc)
    b = spostamento_scalare(a)
    print("  dopo Grover e spostamento: norma %.17g   (scarto %.3g)"
          % (norma_vuoto(b), abs(norma_vuoto(b) - norma_vuoto(phi))))
    # ### e Grover e- un-INVOLUZIONE?
    print("  Grover e- un-involuzione? max|G(G(phi)) - phi| = %.3g"
          % float(np.max(np.abs(grover_scalare(a, sc) - phi))))
