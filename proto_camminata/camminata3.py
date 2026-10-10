r"""LA CAMMINATA `v3` — **il passo di STRANG, la `C` ESTESA, e il passo INVERSO.**

**Un tick** *(decisione di Luca, `2026-10-11`)*:

    N(dtau/2)  ->  passo LINEARE del v2 + vuoto (Grover e spostamento)  ->  N(dtau/2)

> ## ⭐ **LA COMPOSIZIONE E' SIMMETRICA, e non e' un gusto:** una composizione simmetrica
> ## **annulla l'errore di ordine PARI**, quindi l'errore di composizione e' `O(dtau^3)` —
> ## ed e' la stessa ragione per cui l'integratore a strati dell'era `2` e' simmetrico.

### ⛔ **E CON `N` SPENTO IL `v3` E' IL `v2`, AL BIT:** il passo lineare e' **lo stesso
codice** *(`camminata2.passo2`)*, e il vuoto **non tocca lo spinore**. ### **E' la lettura
`(R)`, la prima che si misura — e se non e' al bit, il `v3` ha invalidato il `v2`.**

### ⭐ **LA `C` ESTESA:** `psi -> i sigma_y psi*`, **`phi -> phi*`**. Commuta col flusso di `N`
perche' `G'` e' **pari** *(l'angolo non cambia)* e `b` e' **dispari** *(la fase del vuoto
commuta)*.

### ⚠ **IL PASSO INVERSO ESISTE ED E' ESATTO:** il flusso si inverte con `dtau -> -dtau`,
Grover e' **un'involuzione** *(`G^2 = I`, misurato)*, la moneta di spin con `-eps`, e lo
spostamento scambiando all'indietro con `U^dagger`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import saturazione3 as S3                                      # noqa: E402
import scena as SC                                             # noqa: E402
import vuoto3 as V3                                            # noqa: E402


def stato3(sc, seme=11, lam0=V3.LAMBDA0, con_vuoto=True):
    """Lo stato del `v3`: **lo spinore** e **il vuoto**, in un dizionario."""
    return {"psi": CM.stato_casuale(sc, seme),
            "phi": V3.vuoto_fondo(sc, lam0, seme) if con_vuoto else V3.vuoto_zero(sc)}


def coniuga3(st):
    """### **`C` ESTESA:** `psi -> i sigma_y psi*`, `phi -> phi*`."""
    return {"psi": C2.coniuga2(st["psi"]), "phi": np.conj(st["phi"])}


def _lineare(psi, phi, sc, geo, r, dt, eps, esatta=False):
    """Il passo lineare: **il `v2` sullo spinore**, Grover e spostamento sul vuoto."""
    p = C2.passo2(psi, sc, geo, r, dt, eps, 0.0, None, esatta)
    f = V3.spostamento_scalare(V3.grover_scalare(phi, sc, esatta))
    return p, f


def _lineare_inverso(psi, phi, sc, geo, r, dt, eps, esatta=False):
    """L'inverso esatto del passo lineare."""
    # ### lo spostamento all-indietro: `out[2a] = U^dagger in[2a+1]` si rovescia
    U = geo["U"]
    v = psi.reshape(-1, 2, 2)
    x = np.empty_like(v)
    x[:, 0, :] = np.einsum("aji,aj->ai", np.conj(U), v[:, 1, :])
    x[:, 1, :] = np.einsum("aij,aj->ai", U, v[:, 0, :])
    x = x.reshape(-1, 2)
    # ### Grover e- un-INVOLUZIONE, quindi si riapplica
    x = CM.moneta_grover(x, sc, esatta)
    # ### e la moneta di spin si gira
    x = C2.moneta_spin(x, geo, -eps, r * dt, sc)
    f = V3.grover_scalare(V3.spostamento_scalare(phi), sc, esatta)
    return x, f


def passo3(st, sc, geo, r, dt, eps, flusso=None, esatta=False):
    """### UN TICK del `v3`, ### **composizione SIMMETRICA.**

    ### ⚠ **`flusso = None` vuol dire `N` SPENTO**, e allora questo passo e'
    ### **esattamente il `v2`** sullo spinore.
    """
    psi, phi = st["psi"], st["phi"]
    mezzo = 0.5 * r * dt
    if flusso is not None:
        psi, phi = flusso(psi, phi, sc, geo, mezzo)
    psi, phi = _lineare(psi, phi, sc, geo, r, dt, eps, esatta)
    if flusso is not None:
        psi, phi = flusso(psi, phi, sc, geo, mezzo)
    return {"psi": psi, "phi": phi}


def passo3_inverso(st, sc, geo, r, dt, eps, flusso=None, esatta=False):
    """### L'INVERSO ESATTO del tick: ### **i tre pezzi al contrario, e `dtau` negativo.**"""
    psi, phi = st["psi"], st["phi"]
    mezzo = -0.5 * r * dt
    if flusso is not None:
        psi, phi = flusso(psi, phi, sc, geo, mezzo)
    psi, phi = _lineare_inverso(psi, phi, sc, geo, r, dt, eps, esatta)
    if flusso is not None:
        psi, phi = flusso(psi, phi, sc, geo, mezzo)
    return {"psi": psi, "phi": phi}


def corri3(st, sc, geo, r, dt, eps, passi, flusso=None, osserva=None):
    fuori = []
    if osserva is not None:
        fuori.append(osserva(0, st))
    for t in range(1, passi + 1):
        st = passo3(st, sc, geo, r, dt, eps, flusso)
        if osserva is not None:
            fuori.append(osserva(t, st))
    return st, fuori


def energia_totale(st, sc, geo):
    """### `Σ_k N_k`: l'energia della saturazione, **letta.**"""
    import nonlineare2 as N2
    h = N2.elicita_nodo(st["psi"], sc, geo)
    lam = V3.lambda_nodo(st["phi"], sc)
    return float(np.sum(S3.energia(h, lam)))


if __name__ == "__main__":
    import geometria as GE
    SC._niente_simulatore()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sc = SC.irregolare()
    uno = np.ones(sc["n"], dtype=float)
    geo = GE.scena_identita(sc)
    st = stato3(sc, 11)
    # ### (R) la REGRESSIONE: con `N` spento, lo spinore e- quello del `v2`, AL BIT
    a = st["psi"].copy()
    for _ in range(40):
        a = C2.passo2(a, sc, geo, uno, 1.0, 0.5)
    b = dict(st)
    for _ in range(40):
        b = passo3(b, sc, geo, uno, 1.0, 0.5, None)
    print("  (R) regressione al v2, N spento: max|psi3 - psi2| = %.3g"
          % float(np.max(np.abs(b["psi"] - a))))
    # ### (V) la REVERSIBILITA-
    k = 20
    c = dict(st)
    for _ in range(k):
        c = passo3(c, sc, geo, uno, 1.0, 0.5, S3.flusso)
    for _ in range(k):
        c = passo3_inverso(c, sc, geo, uno, 1.0, 0.5, S3.flusso)
    print("  (V) reversibilita- su %d+%d passi: max|psi - psi0| = %.3g   "
          "max|phi - phi0| = %.3g"
          % (k, k, float(np.max(np.abs(c["psi"] - st["psi"]))),
             float(np.max(np.abs(c["phi"] - st["phi"])))))
    # ### le norme e la C
    d = dict(st)
    for _ in range(40):
        d = passo3(d, sc, geo, uno, 1.0, 0.5, S3.flusso)
    print("  norme dopo 40 tick con N: psi %.3g   phi %.3g"
          % (abs(CM.norma(d["psi"]) - CM.norma(st["psi"])),
             abs(V3.norma_vuoto(d["phi"]) - V3.norma_vuoto(st["phi"]))))
    e1 = coniuga3(passo3(st, sc, geo, uno, 1.0, 0.5, S3.flusso))
    e2 = passo3(coniuga3(st), sc, geo, uno, 1.0, 0.5, S3.flusso)
    print("  la C estesa sul passo intero: max|C U - U C| = %.3g (psi)  %.3g (phi)"
          % (float(np.max(np.abs(e1["psi"] - e2["psi"]))),
             float(np.max(np.abs(e1["phi"] - e2["phi"])))))
