# -*- coding: utf-8 -*-
r"""`M1` — **IL SEGNO DELLA SATURAZIONE**: `-N` e `-D`, candidate **ACCENDIBILI**.

> ## ⭐ **E IL SEGNO OPPOSTO E' GRATIS, ed e' un conto e non una fortuna:**
> ## `saturazione3.flusso` applica `exp(-i G' dtau (sigma.n))` sullo spinore e
> ## `phi exp(-i b dtau)` sul vuoto. ### **Mandare `dtau` in `-dtau` flippa ENTRAMBI**, che
> ## e' esattamente *«rotazione `-G' dtau`, fase del vuoto `-b dtau`»* del mandato.

| | la conseguenza | perche' |
|---|---|---|
| `a` | `-N` e' **hamiltoniano** | e' il flusso di `-N`, e `N` e' una funzione di stato |
| `b` | e' **esatto** | e' la **stessa** forma chiusa, con il tempo rovesciato |
| `c` | e' **reversibile** | l'inverso e' `+dtau` |
| `d` | **rispetta `C`** | `N` resta **dispari**, e il conto del `v3` non cambia di segno nelle ipotesi |
| `e` | **nessuna costante nuova** | e' ### **un segno, non un parametro** *(`W2`, `A1`)* |

### ⛔ **MAI DI DEFAULT:** `flusso_di("lineare")` da' `None`, e ### **a candidata spenta il
passo e' il `v3` AL BIT** — un braccio del banco lo verifica.

### ⚠ **E LA GRANDEZZA CONSERVATA DI `-N` E' `-N`, e la chiamo con quel nome:** non si
promuove a *«energia»* *(`V8` della voce `15`, e `[[PROMOZIONE-CONSERVAZIONE-MODIFICATA]]` e'
una decisione di Luca aperta)*.

### ⚠ **NESSUN `clip`, NESSUNA costante tarata in questo file.**
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import interferenza3 as I3                                     # noqa: E402
import saturazione3 as S3                                      # noqa: E402

# ### ⛔ **I NOMI ENTRANO NELLE USCITE**, e `lineare` e' ### **il controllo che PUO-
# ### fallire**: se il lineare desse la stessa concentrazione, la non linearita-
# ### ### **non starebbe facendo niente.**
VARIANTI = ("lineare", "+N", "-N", "+D", "-D")
# ### ⛔ **LA GRIGLIA DI `x0`, DICHIARATA:** quella della lettura `T` del `v3`,
# ### ### **da `1/8` a `8`**, come il mandato chiede.
X0_GRIGLIA = (0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0)


def _meno(flusso):
    """### Il flusso col **segno opposto**: ### **`dtau -> -dtau`, e nient'altro.**"""
    def f(psi, phi, sc, geo, dtau):
        return flusso(psi, phi, sc, geo, -dtau)
    f.__name__ = "meno_" + getattr(flusso, "__name__", "flusso")
    return f


flusso_meno_N = _meno(S3.flusso)
flusso_meno_D = _meno(I3.flusso_D)


def flusso_di(variante):
    """### Il flusso della variante, oppure ### **`None` = SPENTO = il `v3` lineare.**"""
    assert variante in VARIANTI, "### variante `%r` sconosciuta" % (variante,)
    if variante == "lineare":
        return None
    if variante == "+N":
        return S3.flusso
    if variante == "-N":
        return flusso_meno_N
    if variante == "+D":
        return I3.flusso_D
    return flusso_meno_D


if __name__ == "__main__":
    import math

    import numpy as np
    import camminata as CM
    import camminata3 as C3
    import geometria as GE
    import scena as SC
    import vuoto3 as V3
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    SC._niente_simulatore()
    sc = SC.irregolare(120)
    geo = GE.scena_curva(sc, 11)
    geo_i = GE.scena_identita(sc)
    uno = np.ones(sc["n"], dtype=float)
    st = C3.stato3(sc, 11)
    K = 20
    n0 = CM.norma(st["psi"])
    f0 = V3.norma_vuoto(st["phi"])
    print("  %-10s %-14s %-14s %-14s %s"
          % ("variante", "norma psi", "norma phi", "inverso",
             "la C (identita-)"))
    for et in VARIANTI:
        fl = flusso_di(et)
        a = dict(st)
        for _ in range(K):
            a = C3.passo3(a, sc, geo, uno, 1.0, 0.5, fl)
        b = dict(a)
        for _ in range(K):
            b = C3.passo3_inverso(b, sc, geo, uno, 1.0, 0.5, fl)
        inv = max(float(np.max(np.abs(b["psi"] - st["psi"]))),
                  float(np.max(np.abs(b["phi"] - st["phi"])))) \
            / max(math.sqrt(f0), 1.0)
        # ### ⛔ **LA `C` SI MISURA SULL-IDENTITA-, E NON SULLA CURVA, e al primo
        # ### giro sbagliavo:** sulla curva ### **ogni** variante dava `0.149`,
        # ### ### **`lineare` COMPRESA** -- perche- quello e- l-effetto noto della fase
        # ### `U(1)`, che manda la camminata ### **nell-ANTI-camminata** *(misurato nel
        # ### `v2`)*. ### ⚠ **Un numero uguale su tutte le varianti non dice niente
        # ### sul SEGNO**, ed e- un falso-positivo.
        e1 = C3.coniuga3(C3.passo3(st, sc, geo_i, uno, 1.0, 0.5, fl))
        e2 = C3.passo3(C3.coniuga3(st), sc, geo_i, uno, 1.0, 0.5, fl)
        cc = max(float(np.max(np.abs(e1["psi"] - e2["psi"]))),
                 float(np.max(np.abs(e1["phi"] - e2["phi"]))))
        print("  %-10s %-14.3g %-14.3g %-14.3g %.3g"
              % (et, abs(CM.norma(a["psi"]) - n0) / n0,
                 abs(V3.norma_vuoto(a["phi"]) - f0) / f0, inv, cc))
    # ### ⛔ **E LA REGRESSIONE: a candidata SPENTA il passo e- il `v3` lineare AL BIT**
    import camminata2 as C2
    a = st["psi"].copy()
    b = dict(st)
    for _ in range(K):
        a = C2.passo2(a, sc, geo, uno, 1.0, 0.5)
        b = C3.passo3(b, sc, geo, uno, 1.0, 0.5, flusso_di("lineare"))
    print()
    print("  la REGRESSIONE, candidata spenta: max|psi - psi_v2| = %.3g  ### **AL BIT**"
          % float(np.max(np.abs(b["psi"] - a))))
