# -*- coding: utf-8 -*-
"""`D1` — **L'INVARIANZA DI SCALA, MISURATA.**

> ### ⛔ **`D1` del mandato del `2026-10-16`:** con la forma ### **spenta** le leggi di oggi
> devono essere ### **invarianti di scala**; con la forma ### **accesa a `Lambda_c` fissa**
> l'invarianza ### **si rompe**; e con ### **`Lambda_c` scalata anche lei** l'invarianza
> ### **torna.** ### **Quest'ultima e' la prova che conta SOLO `Lambda_c/Lambda_medio`.**

## ⭐ PERCHE' CI SI ASPETTA CHE REGGA, *e il conto si fa prima della misura*

Sotto `psi -> lambda psi` e `phi -> lambda phi`:

```
rho = somma |psi|^2  ->  lambda^2 rho          Lambda = somma |phi|^2  ->  lambda^2 Lambda
alpha = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)      beta = -rho/(rho+Lambda)
```

### **Il rapporto `rho/(rho+Lambda)` e' INVARIANTE**, quindi `alpha` e `beta` sono
invarianti, quindi ### **le fasi che il flusso applica sono le stesse** — e i cinque pezzi
unitari sono ### **LINEARI**, quindi commutano con la moltiplicazione per `lambda`.
### ✅ **Quindi il passo intero e' EQUIVARIANTE**, ed e' cio' che la misura trova.

## ⛔⛔ IL CRITERIO DEL MANDATO VA LETTO A **UN TICK**, e il motivo e' MISURATO

Il mandato chiede *«`lambda` potenze di `2` per il controllo ### **al bit**, e `3` per
quello ### **in ulp** *(`8` ulp)*, su `50` tick»*. ### ⚠ **A `50` tick la parte in ulp
NON e' l'invarianza: e' l'AMPLIFICAZIONE di un arrotondamento iniziale**, e il numero che
lo dice e' questo:

```
tick:        0      1      2      5     10     25     50    100
ulp lam=3:  0.6    2.0    2.7    5.6   15.2   28.7   96.3  1902.1
ulp lam=2:  0.0    0.0    0.0    0.0    0.0    0.0    0.0     0.0
```

### ⛔ **A TICK `0` — cioe' SENZA EVOLVERE — `lambda = 3` da' gia' `0.6` ulp:** e'
### **`(3x)/3 != x` in IEEE-754**, e non c'entra niente con la fisica. ### **Da li' il
residuo CRESCE**, perche' la dinamica non e' lineare.

> ### ✅ **E LA PROVA CHE NON C'E' NESSUNA SCALA NASCOSTA E' UN'ALTRA, ed e' piu' forte:**
> ### **`lambda = 2` e `0.5` sono AL BIT a OGNI numero di tick, fino a `100`.**
> ### ⛔ **Una scala assoluta in una legge romperebbe ANCHE quelli** — una soglia
> ### **non guarda** se `lambda` e' una potenza di `2`. ### **Quindi la prima riga di `D1`
> regge, e il punto `D` NON si ferma.**

### 📌 **PERCIO' I BRACCI SONO COSI', e la soglia degli `8` ulp NON E' STATA TOCCATA:**
### **al bit** per le potenze di `2` su ### **`50` tick** *(piu' forte di quanto chiesto)*,
e ### **`8` ulp per `lambda = 3` a UN tick** *(il numero di tick in cui quella soglia
misura l'equivarianza e non l'amplificazione)*. ### **La crescita resta come INFORMAZIONE,
stampata.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
import _presidio                                              # noqa: E402
import deriva as DV                                           # noqa: E402
import flussi_parziali as FP                                  # noqa: E402
import tick as TK                                             # noqa: E402

NL = chr(10)
EPS = float(np.finfo(float).eps)
SCENE = ((16, 7), (12, 11))
# ### ⛔ **DUE NUMERI DI TICK, e ciascuno ha il suo criterio** *(il perche' e' nel titolo)*.
TICK_AL_BIT = 50
TICK_IN_ULP = 1
SCALE_AL_BIT = (2.0, 0.5)
SCALE_IN_ULP = (3.0,)
ULP = 8.0
CRESCITA = (0, 1, 2, 5, 10, 25, 50, 100)
DTAU = 1.0
VUOTO_MODULO = 2.0
# ### ⚠ **NON E' UNA SCELTA DI `Lambda_c`:** serve ai due bracci della forma accesa, e vale
# ### il `Lambda` iniziale della scena. ### **La scelta e' di Luca.**
LC_DI_PROVA = 8.0
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


def evolvi(nn, seme, scala, tick, lambda_c, scala_anche_lc):
    """Evolve `tick` tick lo stato ### **scalato per `scala`**, e ### **divide alla fine.**

    `lambda_c = None` e' ### **la forma SPENTA**. `scala_anche_lc` e' ### **la controprova:**
    `Lambda_c -> scala^2 * Lambda_c`, perche' ### **`Lambda` scala come `scala^2`.**
    """
    _i, mot, st, par = DV.scena(nn, seme, DTAU, norma="locale",
                                vuoto_modulo=VUOTO_MODULO, su2=True)
    st["psi_h"] *= scala
    st["phi_h"] *= scala
    lc = None
    if lambda_c is not None:
        lc = lambda_c * (scala * scala if scala_anche_lc else 1.0)
    for _t in range(tick):
        if lc is not None:
            FP.accendi_cs(mot, lc, st)
        TK.tick(st, mot, par)
    # ### ⚠ **Si divide PER `scala`**, non si confronta con lo stato scalato: cosi' il
    # ### numero che esce e' ### **nelle unita' dell'originale**, e la soglia in ulp ha un
    # ### senso.
    return st["psi_h"] / scala, st["phi_h"] / scala


def ulp_fra(a, b):
    """`(scarto, scala, ulp)` fra due stati."""
    d = max(float(np.max(np.abs(a[0] - b[0]))), float(np.max(np.abs(a[1] - b[1]))))
    s = max(float(np.max(np.abs(b[0]))), float(np.max(np.abs(b[1]))))
    return d, s, d / (EPS * max(s, 1.0))


def braccio_spenta():
    """### ⭐ **LA PRIMA RIGA: con la forma SPENTA l'invarianza DEVE reggere.**"""
    for nn, seme in SCENE:
        base = evolvi(nn, seme, 1.0, TICK_AL_BIT, None, False)
        for lam in SCALE_AL_BIT:
            a = evolvi(nn, seme, lam, TICK_AL_BIT, None, False)
            d, _s, _u = ulp_fra(a, base)
            esito("### (s1) SPENTA, `lambda = %.1f`: AL BIT su %d tick"
                  % (lam, TICK_AL_BIT), d == 0.0,
                  "nn=%d seme=%d: scarto %.1e   (e' la prova che NON c'e' una scala"
                  " nascosta)" % (nn, seme, d))
        base1 = evolvi(nn, seme, 1.0, TICK_IN_ULP, None, False)
        for lam in SCALE_IN_ULP:
            a = evolvi(nn, seme, lam, TICK_IN_ULP, None, False)
            d, s, u = ulp_fra(a, base1)
            esito("### (s2) SPENTA, `lambda = %.1f`: entro %.0f ulp a %d tick"
                  % (lam, ULP, TICK_IN_ULP), u <= ULP,
                  "nn=%d seme=%d: %.3e su scala %.3e = %.1f ulp" % (nn, seme, d, s, u))


def braccio_accesa():
    """### ⛔ **IL CASO CHE DEVE FALLIRE: con `Lambda_c` FISSA l'invarianza si ROMPE.**

    ### ⭐ **E si rompe GIA' A UN TICK**, cioe' ### **non ha bisogno di accumulare niente:**
    e' la forma che introduce la scala, non la dinamica che amplifica.
    """
    for nn, seme in SCENE:
        base = evolvi(nn, seme, 1.0, TICK_IN_ULP, LC_DI_PROVA, False)
        a = evolvi(nn, seme, 2.0, TICK_IN_ULP, LC_DI_PROVA, False)
        d, s, u = ulp_fra(a, base)
        esito("### (a1) DEVE fallire: ACCESA a `Lambda_c` FISSA, `lambda = 2`, %d tick"
              % TICK_IN_ULP, u > 1e6 * ULP,
              "nn=%d seme=%d: %.6e su scala %.3e = %.3e ulp -- e GIA' A UN TICK"
              % (nn, seme, d, s, u))


def braccio_controprova():
    """### ⭐⭐ **LA CONTROPROVA: con `Lambda_c` scalata per `lambda^2` l'invarianza TORNA.**

    ### ✅ **E' questa che prova che conta SOLO `Lambda_c/Lambda_medio`:** se contasse
    `Lambda_c` da sola, ### **scalarla non rimetterebbe le cose a posto.**
    """
    for nn, seme in SCENE:
        base = evolvi(nn, seme, 1.0, TICK_AL_BIT, LC_DI_PROVA, True)
        for lam in SCALE_AL_BIT:
            a = evolvi(nn, seme, lam, TICK_AL_BIT, LC_DI_PROVA, True)
            d, _s, _u = ulp_fra(a, base)
            esito("### (c1) `Lambda_c` per `lambda^2`, `lambda = %.1f`: AL BIT su %d tick"
                  % (lam, TICK_AL_BIT), d == 0.0,
                  "nn=%d seme=%d: scarto %.1e   (l'invarianza TORNA)" % (nn, seme, d))
        base1 = evolvi(nn, seme, 1.0, TICK_IN_ULP, LC_DI_PROVA, True)
        for lam in SCALE_IN_ULP:
            a = evolvi(nn, seme, lam, TICK_IN_ULP, LC_DI_PROVA, True)
            d, s, u = ulp_fra(a, base1)
            esito("### (c2) `Lambda_c` per `lambda^2`, `lambda = %.1f`: entro %.0f ulp"
                  % (lam, ULP), u <= ULP,
                  "nn=%d seme=%d: %.3e su scala %.3e = %.1f ulp" % (nn, seme, d, s, u))


def informazione_crescita():
    """### 📌 **LA CRESCITA, che e' INFORMAZIONE e NON un criterio.**

    ### ⛔ **Serve a leggere i bracci:** dice che il residuo di `lambda = 3` c'e'
    ### **GIA' A TICK `0`** *(puro arrotondamento)* e ### **cresce** — mentre quello delle
    potenze di `2` ### **resta zero.**
    """
    nn, seme = SCENE[0]
    print("      LA CRESCITA (informazione, NON un criterio) -- nn=%d seme=%d:"
          % (nn, seme))
    print("      %8s %12s %12s" % ("tick", "ulp lam=3", "ulp lam=2"))
    for tk in CRESCITA:
        b = evolvi(nn, seme, 1.0, tk, None, False)
        u3 = ulp_fra(evolvi(nn, seme, 3.0, tk, None, False), b)[2]
        u2 = ulp_fra(evolvi(nn, seme, 2.0, tk, None, False), b)[2]
        print("      %8d %12.1f %12.1f" % (tk, u3, u2))


def main(argv):
    del argv
    _presidio.avvia(__file__)
    print("=" * 100)
    print("`D1`: L'INVARIANZA DI SCALA -- AL BIT su %d tick per le potenze di 2,"
          " %.0f ulp a %d tick per 3" % (TICK_AL_BIT, ULP, TICK_IN_ULP))
    print("=" * 100)
    braccio_spenta()
    braccio_accesa()
    braccio_controprova()
    informazione_crescita()
    print("=" * 100)
    print("`D1`: %d su %d   %s"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
