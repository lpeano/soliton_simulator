# -*- coding: utf-8 -*-
r"""**DOVE SI ROMPE LA `C` CON I FLUSSI PARZIALI — e che cosa la riparerebbe.**

> **Il quarto criterio di uscita di `L1` dice:** *«il collaudo della `C`-simmetria resta
> verde»*. ### ⛔ **NON RESTA VERDE**, e questo file misura **il MECCANISMO**, non
> l'effetto: ### **perche' si rompe, e che cosa la ripara.**

## ⭐ IL MECCANISMO, DERIVATO PRIMA DI MISURARLO

### **La `C` contiene una CONIUGAZIONE COMPLESSA.** Quindi, per un operatore `A`:
`C A C^-1 = (i sigma_y) A^* (i sigma_y)^-1` — e ### **conta `A^*`.**

```
G(theta) = P_u + e^{i theta}(I - P_u)      con P_u REALE
G(theta)^* = P_u + e^{-i theta}(I - P_u) = G(-theta)
```

### ⛔ **E `G(-theta) = G(theta)` SOLO SE `e^{i theta}` E' REALE, cioe' SOLO a
`theta = 0` o `theta = pi`.** ### ⭐⭐ **QUINDI LA `C` DEL CAMMINO NON ERA UNA PROPRIETA'
SUA: ERA UNA CONSEGUENZA DEL FATTO CHE I PEZZI ERANO INVOLUZIONI** — stavano **tutti
all'angolo `pi`**, dove la fase e' reale. ### **Rendendoli flussi, `(B)` la toglie.**

### ✅ **E CIO' CHE LA RIPAREREBBE SI LEGGE DALLA STESSA RIGA: `theta -> -theta`**, cioe'
una `C` che ### **rovescia anche il verso del tempo proprio** *(una `CT`, non una `C`)*.
### ⛔ **E QUELLA E' UNA DECISIONE DI FISICA DI LUCA, non mia.**

## ⚠ COME SI MISURA SENZA UN `dtau` NEGATIVO

### **Il cono vieta `dtau <= 0`**, quindi `G(-theta)` **non si puo' chiedere al motore.**
### ⭐ **Ma non serve:** `G` e' unitaria e normale, quindi
`G(theta)^* = G(-theta) = G(theta)^-1`. ### ✅ **Allora la prova e':**

```
(a)  Op( conj( Op( conj(psi) ) ) ) == psi        <- Op^* = Op^-1, cioe' Op^* = Op(-theta)
(b)  conj( Op( conj(psi) ) ) == Op(psi)          <- vale SOLO se Op^* = Op, cioe' a theta = pi
```

### 📌 **E isola esattamente il pezzo che `(B)` cambia: LA FASE.** Le altre due parti
della `C` *(`i sigma_y` e `U -> C U`)* ### **non dipendono da `theta`**, quindi non
possono essere la causa.

Gira con:  python primo_ordine/_misura_c_flussi.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA**
NN = 12
SEME = 7
DTAU = (1.0, 0.25)
PEZZI = ("grover", "spostamento_trasporto", "grover_scalare", "spostamento_scalare")
NORMA = "locale"
VUOTO_MODULO = 2.0


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


def _coniuga(st):
    """### La coniugazione complessa di `psi` e `phi`, ### **in posto.**"""
    np.conj(st["psi_h"], out=st["psi_h"])
    np.conj(st["phi_h"], out=st["phi_h"])


def c_completa(mot, st):
    """### La `C` **COMPLETA**: `psi -> i sigma_y psi^*`, `phi -> phi^*`,
    ### **`U -> sigma_y U^* sigma_y^-1`.**

    ### ⛔ **E IL TERZO PEZZO NON E' UN DETTAGLIO: E' LA CORREZIONE DI LUCA DEL
    `2026-10-13`.** ### ⚠ **Avevo concluso <<il trasporto deve stare in `SU(2)`>>
    PROPRIO perche' avevo dimenticato che ### la coniugazione di carica INVERTE ANCHE IL
    CAMPO DI GAUGE** -- e con la `C` completa il residuo era `0.000e+00` anche con una `U`
    generica. ### **Qui la metto intera, per non rifare lo stesso errore.**

    ### 📌 **E I DUE QUADRATI SONO DIVERSI, derivati:** `C^2 = -1` su `psi`
    *(`sigma_y^* = -sigma_y`)*, `C^2 = +1` su `phi` e su `U`. ### **Il segno si porta nel
    confronto, non si nasconde in un valore assoluto.**
    """
    psi = st["psi_h"]
    np.conj(psi, out=psi)
    np.einsum("ij,aj->ai", 1.0j * SY, psi.copy(), out=psi)
    np.conj(st["phi_h"], out=st["phi_h"])
    U = mot.geo.U
    np.einsum("ij,ajk,kl->ail", SY, np.conj(U.copy()), SY, out=U)


def _applica(mot, st, nome):
    mot.apri_tick()
    mot.operatori[nome](st, {}, 1)
    mot.chiudi_tick()


def _scarto(a, b):
    return max(float(np.max(np.abs(a[0] - b[0]))), float(np.max(np.abs(a[1] - b[1]))))


def _scala(a):
    return max(float(np.max(np.abs(a[0]))), float(np.max(np.abs(a[1]))))


def prove(dtau):
    """### Le due prove, ### **per ogni pezzo, a un `dtau` dato.**"""
    import deriva as DV
    eps_m = float(np.finfo(float).eps)
    print("-" * 96)
    print("  dtau = %.4f  ->  theta = %.4f pi" % (dtau, dtau))
    for nome in PEZZI:
        # ### ⭐ **(a) `C Op(theta) C^-1 = Op(-theta)`, con la `C` COMPLETA.** La prova:
        # ### `C`, `Op`, `C`, `Op` ### **torna allo stato di partenza** -- col segno di
        # ### `C^2`, che e- ### **`-1` su `psi` e `+1` su `phi`.**
        _i, mot, st, _p = DV.scena(NN, SEME, dtau, norma=NORMA,
                                   vuoto_modulo=VUOTO_MODULO, su2=True)
        inizio = (-st["psi_h"].copy(), st["phi_h"].copy())
        c_completa(mot, st)
        _applica(mot, st, nome)
        c_completa(mot, st)
        _applica(mot, st, nome)
        d = _scarto((st["psi_h"], st["phi_h"]), inizio)
        sc = _scala(inizio)
        esito("(a) `%s`: `C Op(theta) C^-1 = Op(-theta)`" % nome,
              d <= 64 * eps_m * sc,
              "scarto %.3e su scala %.3e, cioe' %.1f ulp" % (d, sc, d / (eps_m * sc)))
        # ### ⭐ **(b) `C Op C^-1 = Op`, cioe- LA `C`-COVARIANZA VERA**: vale ### **SOLO
        # ### a `theta = pi`**, ed e- ### **cio- che la strada `(B)` TOGLIE.**
        _i, mot, st, _p = DV.scena(NN, SEME, dtau, norma=NORMA,
                                   vuoto_modulo=VUOTO_MODULO, su2=True)
        c_completa(mot, st)
        _applica(mot, st, nome)
        c_completa(mot, st)
        coniugato = (-st["psi_h"].copy(), st["phi_h"].copy())
        _i, mot, st, _p = DV.scena(NN, SEME, dtau, norma=NORMA,
                                   vuoto_modulo=VUOTO_MODULO, su2=True)
        _applica(mot, st, nome)
        d = _scarto(coniugato, (st["psi_h"], st["phi_h"]))
        sc = _scala(coniugato)
        atteso = dtau == 1.0
        esito("(b) `%s`: `C Op C^-1 = Op`%s" % (nome, " [ATTESO SI]" if atteso
                                                else " [ATTESO NO]"),
              (d <= 64 * eps_m * sc) == atteso,
              "scarto %.3e su scala %.3e" % (d, sc))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 96)
    print("LA `C` E I FLUSSI PARZIALI: dove si rompe, e che cosa la riparerebbe")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: nn = %d   seme = %d   dtau = %s   norma = %s"
          "   vuoto_modulo = %.1f   su2 = True"
          % (NN, SEME, DTAU, NORMA, VUOTO_MODULO))
    for dtau in DTAU:
        prove(dtau)
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ⭐ E LA LETTURA, se i bracci passano: `Op^* = Op(-theta)` SEMPRE, e")
    print("###   `Op^* = Op` SOLO a theta = pi. Cioe' la `C` del cammino era UNA")
    print("###   CONSEGUENZA DELLE INVOLUZIONI, e la `C` che sopravvive a (B) deve")
    print("###   ROVESCIARE IL TEMPO PROPRIO -- una `CT`. ### E' UNA DECISIONE DI LUCA.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
