# -*- coding: utf-8 -*-
r"""`M-B2` — **L'ERRORE DI CONSERVAZIONE DI `H_tot` CALA COME `dtau^2`?**

> **Criterio di uscita di `L1`, nelle parole di Luca:** *«con `dtau` uniforme
> `= dtau_rif/2^k` (`k = 1..4`), l'errore di conservazione dell'energia totale (strada
> `B`) cala di un **fattore 4** a ogni dimezzamento. Riporta la tabella dei rapporti.»*

## ⭐ CHE COS'E' `H_tot` DI STRADA `(B)`, E PERCHE' NON E' LA `E` DI PRIMA

### **Ogni strato del passo e' il flusso di un generatore LOCALE**, e `H_tot` e' la somma
dei valori medi di quei generatori — ### **uno per arco, uno per nodo, uno per
estremita'**:

```
H_tot = - pi  SOMMA_nodi ( <psi|psi>_k - |SOMMA_k psi|^2/d_k )      il Grover di psi
        - pi  SOMMA_archi ( <psi|psi>_a - 2 Re[psi_0^dagger U^dagger psi_1] )/2   il hop
        - pi  SOMMA_nodi ( ... )   - pi SOMMA_archi ( ... )         gli stessi su phi
        + eps SOMMA_estremita <psi_h| sigma.n_h |psi_h>             la moneta di spin
        + SOMMA_nodi Lambda_k G(h_k/Lambda_k)                       la saturazione
```

### ⛔ **E NON E' LA `E` DELLA DERIVA:** quella ha **raggio 1** *(usa `W`, cioe' guarda il
vicino)*, questa ha ### **raggio ZERO** — un arco, un nodo, un'estremita'.
### ⭐ **`omega = pi` NON E' UNA COSTANTE NUOVA:** e' il raccordo `B-4` con `dtau_rif = 1`.

## ⚠ IL PROTOCOLLO: **TEMPO TOTALE FISSO**, e il perche' decide la previsione

### ⛔ **A numero di tick FISSO l'errore globale andrebbe come `N dtau^3`**, cioe'
**fattore 8**; ### ✅ **a TEMPO TOTALE fisso** *(`N = T/dtau`, quindi `N` RADDOPPIA a ogni
dimezzamento)* **va come `T dtau^2`**, cioe' ### **fattore 4** — ed e' il fattore che il
criterio nomina. ### **Quindi il protocollo e' a tempo totale fisso**, e lo dico prima di
misurare.

### 📌 **E L'ERRORE E' L'ESCURSIONE, non `fine - inizio`:** `max_t |H(t) - H(0)|`.
### ⛔ **E' una lezione gia' pagata:** con una quantita' che oscilla, `fine - inizio` e'
**un campione casuale** e aveva fatto sembrare falsa una previsione vera.

## ⛔ IL PERIMETRO

### Usa `deriva.py` **IN SOLA LETTURA** *(`DV.scena`, `DV.tick`)*, che la scelta di
perimetro di Luca del `2026-10-15` ammette per i criteri di uscita di questo livello.

## 📌 E IL LIMITE A `Lambda == 0` NON E' UN PAVIMENTO

### `Lambda G(h/Lambda)` ### **tende a `h`** quando `Lambda -> 0`, perche' `Lambda arctan` va
a zero. ### ✅ **E' il VALORE CHE LA FUNZIONE PRENDE la'**, quindi `A11` e' rispettato:
### **un pavimento curerebbe dove non c'e' un errore, un limite E' la funzione.**

Gira con:  python primo_ordine/_misura_mb2.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import saturazione as SAT                                     # noqa: E402

# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA**
TEMPO = 8.0
KAPPA = (1, 2, 3, 4)
NN = 16
SEME = 7
NORMA = "locale"
VUOTO_MODULO = 2.0
SU2 = True
OMEGA = float(np.pi)


def _per_nodo(inc, v):
    """### Somma per nodo di un reale per estremita', ### **senza cicli Python.**"""
    fuori = np.zeros(inc.n, dtype=float)
    np.add.at(fuori, inc.nodo, v)
    return fuori


def h_tot(inc, mot, st, par):
    """### `H_tot`, ### **la somma dei generatori locali.**"""
    psi, phi = st["psi_h"], st["phi_h"]
    m = inc.m
    U = mot.geo.U
    # ------------------------------------------------- i due pezzi di NODO
    nrm_psi = _per_nodo(inc, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2)
    nrm_phi = _per_nodo(inc, np.abs(phi) ** 2)
    S_psi = np.zeros((inc.n, 2), dtype=complex)
    np.add.at(S_psi, inc.nodo, psi)
    S_phi = np.zeros(inc.n, dtype=complex)
    np.add.at(S_phi, inc.nodo, phi)
    d = inc.grado.astype(float)
    pu_psi = (np.abs(S_psi[:, 0]) ** 2 + np.abs(S_psi[:, 1]) ** 2) / d
    pu_phi = np.abs(S_phi) ** 2 / d
    nodo = -OMEGA * float(np.sum((nrm_psi - pu_psi) + (nrm_phi - pu_phi)))
    # ------------------------------------------------- i due pezzi di ARCO
    v = psi.reshape(m, 2, 2)
    p0, p1 = v[:, 0, :], v[:, 1, :]
    incro = np.einsum("ai,aji,aj->a", np.conj(p0), np.conj(U), p1)
    nrm_a = (np.abs(p0) ** 2).sum(axis=1) + (np.abs(p1) ** 2).sum(axis=1)
    arco_psi = float(np.sum(nrm_a - 2.0 * np.real(incro))) / 2.0
    w = phi.reshape(m, 2)
    f0, f1 = w[:, 0], w[:, 1]
    arco_phi = float(np.sum(np.abs(f0) ** 2 + np.abs(f1) ** 2
                            - 2.0 * np.real(np.conj(f0) * f1))) / 2.0
    arco = -OMEGA * (arco_psi + arco_phi)
    # ------------------------------------------------- la moneta di spin
    h = mot.elicita(st).copy()
    moneta = float(par["eps"]) * float(np.sum(h))
    # ------------------------------------------------- la saturazione
    lam = mot.densita_vuoto(st).copy()
    buoni = lam > 0.0
    N = np.where(buoni, h, 0.0).astype(float)
    if np.any(buoni):
        x = h[buoni] / lam[buoni]
        N[buoni] = lam[buoni] * SAT.G(x)
    # ### ⚠ **E DOVE `Lambda == 0` il LIMITE e' `h`**, non uno zero: `Lambda G(h/Lambda)`
    # ### ### **tende a `h`** *(`Lambda arctan -> 0`)*. ### **E- la funzione, non un
    # ### pavimento** -- e il perche- sta nel docstring del modulo.
    N[~buoni] = h[~buoni]
    satura = float(np.sum(N))
    return nodo + arco + moneta + satura


def _tick_palindromo(st, mot, par, ordine):
    """### ⛔ **UN TICK CON L'ORDINE PALINDROMO — SOLO PER DIAGNOSI.**

    ### ⚠ **NON cambia la tabella e NON cambia il passo del simulatore:** vive qui
    dentro, e serve a rispondere a UNA domanda -- ### **il rapporto `2` viene dalla
    composizione NON SIMMETRICA, o da altro?**
    ### ⭐ **E questo esperimento PRIMA DI `(B)` ERA IMPOSSIBILE:** i cinque pezzi
    ### **ALZAVANO** a una frazione diversa da `1`.
    """
    import deriva as DV
    mot.apri_tick()
    for idl, frazione in ordine:
        nome, vuole_par = DV.OPERATORE[idl]
        mot.operatori[nome](st, par if vuole_par else {}, frazione)
    mot.chiudi_tick()


def _palindromo():
    """### L'ordine della tabella, ### **spezzato a meta' e rispecchiato.**"""
    import composizione as CM
    mezzi = [(idl, fr * 0.5) for idl, fr, _t in CM.ORDINE]
    return mezzi + mezzi[::-1]


def diagnosi():
    """### Gli stessi `dtau`, ### **con l'ordine palindromo**: che rapporti da'?"""
    import deriva as DV
    ordine = _palindromo()
    print("-" * 96)
    print("### 📌 DIAGNOSI (NON un criterio, e NON una modifica alla tabella):")
    print("###   lo STESSO H_tot e gli STESSI dtau, con l'ordine SPEZZATO A META' E")
    print("###   RISPECCHIATO (%d pezzi invece di %d). Risponde a UNA domanda: il"
          % (len(ordine), len(ordine) // 2))
    print("###   rapporto 2 viene dalla composizione NON SIMMETRICA o da altro?")
    righe = []
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        tick = int(round(TEMPO / dtau))
        inc, mot, st, par = DV.scena(NN, SEME, dtau, norma=NORMA,
                                     vuoto_modulo=VUOTO_MODULO, su2=SU2)
        h0 = h_tot(inc, mot, st, par)
        peggio = 0.0
        for _t in range(tick):
            _tick_palindromo(st, mot, par, ordine)
            d = abs(h_tot(inc, mot, st, par) - h0)
            if d > peggio:
                peggio = d
        rap = (righe[-1] / peggio) if righe and peggio > 0 else float("nan")
        righe.append(peggio)
        print("###   k=%d  dtau=%.6f  tick=%-5d escursione=%.6e  rapporto %s"
              % (k, dtau, tick, peggio,
                 "--" if np.isnan(rap) else "%.3f" % rap))
        sys.stdout.flush()
    rap = [righe[i - 1] / righe[i] for i in range(1, len(righe)) if righe[i] > 0]
    print("###   I RAPPORTI PALINDROMI: %s   (pendenza log2: %s)"
          % ("  ".join("%.3f" % r for r in rap),
             "  ".join("%.3f" % np.log2(r) for r in rap)))
    return rap


def una_corsa(dtau, tick):
    """### `(escursione, H0)` su `tick` tick, ### **guardando H A OGNI TICK.**"""
    import deriva as DV
    inc, mot, st, par = DV.scena(NN, SEME, dtau, norma=NORMA,
                                 vuoto_modulo=VUOTO_MODULO, su2=SU2)
    h0 = h_tot(inc, mot, st, par)
    peggio = 0.0
    for _t in range(tick):
        DV.tick(st, mot, par)
        d = abs(h_tot(inc, mot, st, par) - h0)
        if d > peggio:
            peggio = d
    return peggio, h0


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 96)
    print("M-B2: L'ERRORE DI CONSERVAZIONE DI H_tot CONTRO dtau -- tempo totale FISSO")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: T = %.1f   nn = %d   seme = %d   norma = %s"
          "   vuoto_modulo = %.1f   su2 = %s   omega = pi"
          % (TEMPO, NN, SEME, NORMA, VUOTO_MODULO, SU2))
    print("-" * 96)
    print("  %-4s %-10s %-7s %-14s %-14s %s"
          % ("k", "dtau", "tick", "H(0)", "escursione", "rapporto col k-1"))
    righe = []
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        tick = int(round(TEMPO / dtau))
        err, h0 = una_corsa(dtau, tick)
        rap = (righe[-1][2] / err) if righe and err > 0 else float("nan")
        righe.append((dtau, tick, err))
        print("  %-4d %-10.6f %-7d %-14.6f %-14.6e %s"
              % (k, dtau, tick, h0, err,
                 "--" if np.isnan(rap) else "%.3f" % rap))
        sys.stdout.flush()
    print("-" * 96)
    rap = [righe[i - 1][2] / righe[i][2] for i in range(1, len(righe))
           if righe[i][2] > 0]
    if not rap:
        print("### ⛔ escursione NULLA: niente da misurare, e un rapporto non esiste")
        return 1
    print("  I RAPPORTI: %s" % ("  ".join("%.3f" % r for r in rap),))
    print("  LA PENDENZA in log2: %s"
          % ("  ".join("%.3f" % np.log2(r) for r in rap),))
    vicino = [abs(r - 4.0) <= 0.8 for r in rap]
    if all(vicino):
        print("### ✅ `M-B2` PASSA: ogni rapporto e' 4 entro 0.8, cioe' l'errore e'"
              " `O(dtau^2)`")
        return 0
    print("### ⛔ `M-B2` NON DA' 4: i rapporti sono %s"
          % ("  ".join("%.3f" % r for r in rap),))
    print("###   E LO RIPORTO COSI' COM'E': una pendenza 1 vorrebbe dire che la"
          " composizione")
    print("###   NON E' SIMMETRICA -- l'ordine della tabella spezza a meta' SOLO la")
    print("###   saturazione, e i cinque pezzi in mezzo stanno a frazione 1.")
    print("###   NESSUN PARAMETRO SI TOCCA per far tornare il 4.")
    diagnosi()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
