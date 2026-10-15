# -*- coding: utf-8 -*-
r"""**LA DERIVAZIONE DELLE QUATTRO FORME, VERIFICATA DA `sympy`** — *un conto, non una
misura.*

> **Punto 1 del mandato di Luca del 2026-10-15** *(terzo pezzo di `L2`)*.

## ⭐ I VINCOLI, E DA DOVE VIENE TUTTO

Un termine **locale** `N = Lambda · F(x)` con `x = rho/Lambda`, **omogeneo di grado `1`**:
### **la scala viene dal vuoto locale, e non c'e' nessuna costante.** Allora

```
alpha = dN/drho    = F'(x)              <- quello che agisce su psi
beta  = dN/dLambda = F(x) - x F'(x)     <- quello che agisce su phi
```

### ⭐⭐ **E L'IDENTITA' CHE LEGA I DUE:**

```
beta'(x) = F' - F' - x F'' = - x F''(x) = - x alpha'(x)
```

## ⛔⛔ E LA CONSEGUENZA NON E' <<OBBLIGA>>: E' **<<EQUIVALE>>**

### Se `beta` e' **esattamente lineare**, `beta = -c x`, l'equazione `F - x F' = -c x` si
risolve **in forma chiusa**:

```
(F/x)' = (x F' - F)/x^2 = c/x    ==>    F/x = c ln x + k
                                 ==>    F = c x ln x + k x
                                 ==>    alpha = c ln x + (c + k)        LOGARITMICA
```

> ### **`beta` esattamente lineare  <==>  `alpha` logaritmica.**

### ✅ **E il verso inverso, con la sua IPOTESI DICHIARATA:** se `alpha` e' **limitata e
Lipschitz** *(`alpha'` limitata)*, allora `beta' = -x alpha' -> 0` per `x -> 0`, quindi
### **`beta` non puo' essere lineare fino a zero.**
### ⚠ **L'ipotesi serve:** con `alpha` limitata ma `alpha'` che oscilla come `1/x` il conto
**non si chiude**, e ### **non enuncio un teorema piu' largo di quello che dimostro.**

## ⭐ E CON `rho` AL POSTO DI `h` IL FLUSSO SU `psi` CAMBIA NATURA

```
rho = somma_h |psi_h|^2      ==>   dN/dpsi_h^* = alpha · psi_h     ==>  UNA FASE
h   = somma_h psi^dag (sigma.n) psi   ==>   dh/dpsi_h^* = (sigma.n) psi_h  ==>  UNA ROTAZIONE
```

### ✅ **E una fase NON cambia `rho`:** ### **il termine conserva la sua sorgente.**

Gira con:  python primo_ordine/_deriva_forme_l2.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def braccio_identita():
    """### ⭐ **L'identita' `beta' = -x alpha'`, per una `F` GENERICA.**"""
    import sympy as sp
    print("-" * 96)
    print("### (A) L'IDENTITA' beta' = -x alpha', per una F GENERICA")
    x, rho, lam = sp.symbols("x rho Lambda", positive=True)
    F = sp.Function("F")
    N = lam * F(rho / lam)
    al = sp.simplify(sp.diff(N, rho).subs(rho, x * lam))
    be = sp.simplify(sp.diff(N, lam).subs(rho, x * lam))
    esito("(A1) `alpha = F'(x)`", sp.simplify(al - sp.Derivative(F(x), x).doit()) == 0,
          "sympy: alpha = %s" % al)
    esito("(A2) `beta = F(x) - x F'(x)`",
          sp.simplify(be - (F(x) - x * sp.diff(F(x), x))) == 0,
          "sympy: beta = %s" % sp.simplify(be))
    d = sp.simplify(sp.diff(be, x) + x * sp.diff(al, x))
    esito("(A3) `beta'(x) + x alpha'(x) = 0`", d == 0, "sympy: la differenza fa %s" % d)
    return True


def braccio_se_e_solo_se():
    """### ⛔⛔ **Il SE E SOLO SE: `beta` lineare <==> `alpha` logaritmica.**"""
    import sympy as sp
    print("-" * 96)
    print("### (B) IL SE E SOLO SE: beta esattamente lineare  <==>  alpha logaritmica")
    x = sp.symbols("x", positive=True)
    c, k = sp.symbols("c k", real=True)
    F = sp.Function("F")
    # ### il verso ANDATA: si RISOLVE l-equazione, non si indovina la soluzione
    sol = sp.dsolve(sp.Eq(F(x) - x * sp.diff(F(x), x), -c * x), F(x))
    print("      sympy risolve  F - x F' = -c x  e da':  %s" % sol)
    Fs = sol.rhs
    al = sp.simplify(sp.diff(Fs, x))
    print("      e allora alpha = F' = %s" % al)
    # ### la forma attesa: `c ln x + costante`
    C1 = [s for s in Fs.free_symbols if str(s).startswith("C")]
    cost = sp.symbols("K")
    atteso = c * sp.log(x) + cost
    diff = sp.simplify(sp.expand(al - atteso))
    senza_log = sp.simplify(diff - diff.subs(sp.log(x), 0))
    esito("(B1) `alpha` ha la forma `c ln x + costante`", senza_log == 0,
          "la parte che dipende da ln x e' esattamente `c ln x`")
    # ### il verso RITORNO: `alpha` limitata e Lipschitz ==> `beta' -> 0`
    A = sp.Function("alpha")
    be1 = -x * sp.diff(A(x), x)
    lim = sp.limit(be1.subs(sp.Derivative(A(x), x), sp.Symbol("L")), x, 0)
    esito("(B2) con `alpha'` LIMITATA, `beta' = -x alpha' -> 0` per `x -> 0`",
          sp.simplify(lim) == 0,
          "sympy: il limite fa %s  (l'ipotesi `alpha'` limitata e' DICHIARATA)" % lim)
    print("      ### QUINDI: non esiste una F con beta lineare fino a 0 E alpha limitata")
    print("      ### e Lipschitz. La costrizione e' DIMOSTRATA, non supposta.")
    return True


# ====================================================================== le quattro forme
def _forme_sympy():
    import sympy as sp
    x = sp.symbols("x", positive=True)
    p = sp.Rational(2, 1) / sp.pi
    forme = {}
    # ### `S1`: la saturazione di oggi, con `rho` al posto di `h`
    forme["S1"] = ("N = Lambda G(x), G = x - arctan x", x - sp.atan(x))
    # ### `S2`: `N = rho ln(rho/Lambda)`  ==>  `F = x ln x`
    forme["S2"] = ("N = rho ln(rho/Lambda)", x * sp.log(x))
    # ### `S3`: `N = rho ln(rho/(rho+Lambda))`  ==>  `F = x ln(x/(1+x))`
    forme["S3"] = ("N = rho ln(rho/(rho+Lambda))", x * sp.log(x / (1 + x)))
    # ### ⛔ **`S4` NON passa da `sympy.integrate`, e il motivo e' misurato:** l-integrale
    # ### di `alpha` esce in ### **`lerchphi`**, che ### **non si lambdifica** -- quindi
    # ### la verifica numerica degli attesi NON si potrebbe fare. ### ✅ **Si usa la forma
    # ### CHIUSA IPERGEOMETRICA**, verificata contro una ### **quadratura numerica**:
    # ### `F = pi x - 2 pi x 2F1(1, 1/p; 1+1/p; -x^p)`, perche-
    # ### `alpha = pi - 2 pi/(1+x^p)` e `integrale_0^x dt/(1+t^p) = x 2F1(...)`.
    return x, p, forme


P4 = 2.0 / np.pi


def alpha4(x):
    """### `alpha = pi tanh(ln x / pi) = pi (x^p - 1)/(x^p + 1)`, ### **con `p = 2/pi`.**"""
    x = np.asarray(x, dtype=float)
    return np.pi * (x ** P4 - 1.0) / (x ** P4 + 1.0)


def F4(x):
    """### `F = integrale_0^x alpha`, ### **in forma CHIUSA ipergeometrica.**

    `alpha = pi - 2 pi/(1+x^p)`, e `integrale_0^x dt/(1+t^p) = x · 2F1(1, 1/p; 1+1/p;
    -x^p)`. ### ✅ **E si VERIFICA contro una quadratura**, invece di fidarsi.
    """
    from scipy.special import hyp2f1
    x = np.asarray(x, dtype=float)
    return np.pi * x - 2.0 * np.pi * x * hyp2f1(1.0, 1.0 / P4, 1.0 + 1.0 / P4,
                                                -(x ** P4))


def beta4(x):
    """### `beta = F - x alpha`."""
    x = np.asarray(x, dtype=float)
    return F4(x) - x * alpha4(x)


def braccio_s4():
    """### ⭐ **`S4`: la forma chiusa, la quadratura, e i QUATTRO attesi del mandato.**"""
    from scipy.integrate import quad
    print("-" * 96)
    print("### (D4) `S4`: la forma chiusa ipergeometrica contro una QUADRATURA, e i"
          " quattro attesi")
    # ### (i) la forma chiusa contro la quadratura
    peggio = 0.0
    for xv in (0.01, 0.1, 0.5, 1.0, 2.0, 10.0):
        q = quad(lambda t: float(alpha4(t)), 0.0, xv, limit=200)[0]
        peggio = max(peggio, abs(float(F4(xv)) - q) / max(abs(q), 1e-30))
    esito("(D4-0) `F` in forma chiusa == la QUADRATURA di `alpha`", peggio <= 1e-8,
          "scarto relativo massimo %.3e su 6 valori di x" % peggio)
    # ### (ii) l-identita- `beta' = -x alpha'`, per differenze finite
    h = 1e-6
    peg = 0.0
    for xv in (0.05, 0.3, 1.0, 3.0):
        bp = (float(beta4(xv + h)) - float(beta4(xv - h))) / (2 * h)
        ap = (float(alpha4(xv + h)) - float(alpha4(xv - h))) / (2 * h)
        peg = max(peg, abs(bp + xv * ap))
    esito("(D4-1) `S4` rispetta `beta' = -x alpha'` (differenze finite)", peg <= 1e-5,
          "scarto massimo %.3e su 4 valori di x" % peg)
    # ### (iii) `|alpha| < pi` ovunque
    xs = np.array([1e-12, 1e-6, 0.01, 1.0, 100.0, 1e6, 1e12])
    m = float(np.max(np.abs(alpha4(xs))))
    esito("(D4a) `|alpha| < pi` ovunque", m < np.pi,
          "max |alpha| = %.6f su x da 1e-12 a 1e12, e pi = %.6f" % (m, np.pi))
    # ### (iv) l-esponente per `x` piccolo: `1 + 2/pi`
    xa, xb = 1e-6, 1e-5
    pend = float(np.log(abs(beta4(xb)) / abs(beta4(xa))) / np.log(xb / xa))
    esito("(D4b) `beta ~ x^(1+2/pi)` per `x` piccolo", abs(pend - (1.0 + P4)) <= 0.02,
          "pendenza %.4f contro 1+2/pi = %.4f" % (pend, 1.0 + P4))
    # ### (v) `beta ~ -x` vicino a `x = 1`
    b1 = float(beta4(1.0))
    esito("(D4c) `beta ~ -x` vicino a `x = 1`", abs(b1 + 1.0) <= 0.35,
          "beta(1) = %.5f, e il lineare darebbe -1" % b1)
    # ### (vi) `beta` SATURA per `x` grande
    g = [abs(float(beta4(t))) for t in (10.0, 100.0, 1000.0)]
    esito("(D4d) `beta` SATURA per `x` grande (cresce meno che lineare)",
          g[2] / g[1] < 10.0,
          "|beta| a 10, 100, 1000: %.4f %.4f %.4f -> rapporto 1000/100 = %.3f"
          " (lineare darebbe 10)" % (g[0], g[1], g[2], g[2] / g[1]))
    # ### e i numeri che servono alla misura, stampati
    print("      ### I NUMERI DI `S4` CHE SERVONO ALLA MISURA:")
    for xv in (0.01, 0.03, 0.1, 0.2, 0.5, 1.0, 2.0):
        print("        x = %-5.3g  alpha = %+.6f   beta = %+.6e"
              % (xv, float(alpha4(xv)), float(beta4(xv))))
    sys.stdout.flush()
    return True


def braccio_forme():
    """### Le quattro forme: `alpha`, `beta`, e gli **attesi del mandato.**"""
    import sympy as sp
    print("-" * 96)
    print("### (C) LE QUATTRO FORME: alpha, beta, e gli attesi del mandato")
    x, p, forme = _forme_sympy()
    fuori = {}
    for nome in ("S1", "S2", "S3"):
        testo, F = forme[nome]
        al = sp.simplify(sp.diff(F, x))
        be = sp.simplify(F - x * sp.diff(F, x))
        fuori[nome] = (al, be)
        print("  %s  %s" % (nome, testo))
        print("      alpha = %s" % sp.simplify(al))
        print("      beta  = %s" % be)
        # ### l-identita- su OGNI forma, non solo in generale
        d = sp.simplify(sp.diff(be, x) + x * sp.diff(al, x))
        esito("(C) %s rispetta `beta' = -x alpha'`" % nome, sp.simplify(d) == 0,
              "la differenza fa %s" % d)
        sys.stdout.flush()
    # ============================================== gli attesi, uno per uno
    print("-" * 96)
    print("### (D) GLI ATTESI DEL MANDATO, verificati uno per uno")
    al1, be1 = fuori["S1"]
    s = sp.series(be1, x, 0, 5).removeO()
    esito("(D1) `S1`: `beta ~ -(2/3) x^3` per `x` piccolo",
          sp.simplify(s - (-sp.Rational(2, 3) * x ** 3)) == 0,
          "sympy: la serie fa %s" % s)
    al2, be2 = fuori["S2"]
    esito("(D2) `S2`: `beta = -x` a OGNI x, e `alpha = 1 + ln x` (diverge)",
          sp.simplify(be2 + x) == 0 and sp.simplify(al2 - (1 + sp.log(x))) == 0,
          "beta = %s, alpha = %s, e alpha(0+) = %s"
          % (be2, sp.simplify(al2), sp.limit(al2, x, 0)))
    al3, be3 = fuori["S3"]
    esito("(D3) `S3`: `beta = -x/(1+x)`, e `alpha` diverge per `x -> 0`",
          sp.simplify(be3 + x / (1 + x)) == 0 and sp.limit(al3, x, 0) == -sp.oo,
          "beta = %s, e alpha(0+) = %s" % (sp.simplify(be3), sp.limit(al3, x, 0)))
    return fuori


def braccio_psi():
    """### ⭐ **Il flusso su `psi`: UNA FASE con `rho`, UNA ROTAZIONE con `h`.**"""
    import sympy as sp
    print("-" * 96)
    print("### (E) IL FLUSSO SU psi: una FASE con rho, una ROTAZIONE con h")
    a, b = sp.symbols("a b")
    ac, bc = sp.symbols("ac bc")
    # ### `rho = |a|^2 + |b|^2` scritto con le coniugate come variabili indipendenti
    rho = a * ac + b * bc
    esito("(E1) `drho/dpsi^*` e' `psi` (quindi il flusso e' una FASE)",
          sp.simplify(sp.diff(rho, ac) - a) == 0
          and sp.simplify(sp.diff(rho, bc) - b) == 0,
          "drho/d(a*) = %s, drho/d(b*) = %s" % (sp.diff(rho, ac), sp.diff(rho, bc)))
    # ### `h = psi^dag (sigma.n) psi` con `n = z` per concretezza: `|a|^2 - |b|^2`
    h = a * ac - b * bc
    esito("(E2) `dh/dpsi^*` NON e' `psi` (il flusso e' una ROTAZIONE)",
          sp.simplify(sp.diff(h, bc) + b) == 0 and sp.simplify(sp.diff(h, bc) - b) != 0,
          "dh/d(a*) = %s, dh/d(b*) = %s: ### i segni sono OPPOSTI, e' sigma_z"
          % (sp.diff(h, ac), sp.diff(h, bc)))
    # ### e una FASE non cambia `rho`
    t, alv = sp.symbols("t alpha", real=True)
    a2 = a * sp.exp(-sp.I * alv * t)
    esito("(E3) e una FASE NON cambia `rho`: la sorgente e' CONSERVATA dal termine",
          sp.simplify(sp.Abs(a2) ** 2 - sp.Abs(a) ** 2) == 0,
          "|a e^{-i alpha t}|^2 - |a|^2 = 0 per sympy")
    return True


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 96)
    print("LA DERIVAZIONE DELLE QUATTRO FORME, VERIFICATA DA sympy -- un conto, non una"
          " misura")
    print("=" * 96)
    import sympy as sp
    print("  sympy %s" % sp.__version__)
    braccio_identita()
    braccio_se_e_solo_se()
    forme = braccio_forme()
    braccio_s4()
    braccio_psi()
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E LA FORMA NON SI DECIDE QUI: `S1`-`S4` vivono dentro gli script, la")
    print("###   tabella delle leggi NON e' toccata, e la scelta e' di Luca.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
