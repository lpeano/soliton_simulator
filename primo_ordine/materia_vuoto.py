# -*- coding: utf-8 -*-
"""IL GENERATORE DELL'ACCOPPIAMENTO MATERIA-VUOTO — **le tre funzioni, e il LIMITE.**

> `N_k = rho_k ln(rho_k / (rho_k + Lambda_k))`, con `rho_k = somma_h |psi_h|^2` e
> `Lambda_k = somma_h |phi_h|^2`. ### **Decisione di Luca del `2026-10-15`** *(`23:30`)*:
> sostituisce `CAMM-SATURAZIONE`, e le leggi restano `7`.

## ⭐⭐ LE DUE DERIVATE, CHE SONO IL FLUSSO

```
alpha = dN/drho    = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)      -> una FASE su psi
beta  = dN/dLambda = -rho/(rho+Lambda) = -x/(1+x)                    -> una FASE su phi
```

### ⭐ **E `alpha` DA' UNA FASE E NON UNA ROTAZIONE, al contrario della saturazione:**
la sorgente e' `rho`, e `drho/dpsi^* = psi` ### **con lo STESSO segno nelle due
componenti**; la saturazione aveva `h = s . n`, e `dh/dpsi^*` ha ### **segni OPPOSTI** —
cioe' `sigma_z` nella base di `n`, che e' ### **una rotazione.**
### ⚠ **E la differenza conta:** una rotazione attorno a `n` ### **CAMBIA `h`** *(era il
«l'elicita' nasce»)*, mentre ### **una fase NON cambia `rho`: questo termine CONSERVA LA
SUA SORGENTE.**

## ⭐⭐ PERCHE' IL FLUSSO E' ESATTO — *si DIMOSTRA, non si promette*

### **`N` dipende SOLO da `rho` e `Lambda`**, e il flusso mette ### **solo fasi**: quindi
### **non cambia ne' `rho` ne' `Lambda`**, cioe' ### **`alpha` e `beta` sono COSTANTI
durante il pezzo.** ### ✅ **Allora `exp(-i a dtau/2) exp(-i a dtau/2) = exp(-i a dtau)`
IN ARITMETICA ESATTA**, e ### **due mezzi fanno l'intero** — un collaudo ne misura
### **gli ulp**, che e' l'unica cosa che resta da misurare.

## ⛔ `rho = 0`: UNA SINGOLARITA' ELIMINABILE, NON UN PAVIMENTO

### **`alpha` non e' definita dove `rho = 0`** *(`ln 0`)*. ### ⭐ **Ma la' `psi = 0`, e la
fase di un vettore nullo non vuol dire niente:** `exp(-i a dtau) * 0 = 0` ### **per
QUALUNQUE `a`.** ### ✅ **Quindi `alpha = 0` la' e' IL VALORE CHE L'ESPRESSIONE PRENDE**
dove e' definita, non una protezione.
### ⛔ **E NESSUN PAVIMENTO SU `rho > 0`:** dove `rho` e' piccolo ma non nullo `alpha` e'
grande *(diverge come `ln rho`)*, e ### **si usa com'e'** — e' esattamente il caso che la
misura della risposta statica va a guardare.
### ⚠ **E la differenza fra un limite e un pavimento NON e' lessicale:** un pavimento
violerebbe `A11` *(nessuna cura dove non c'e' un errore)*; ### **un limite e' la
funzione.**

### ✅ **E SONO PURE: nessun `self`, nessuno stato, nessun buffer.** Il collaudo le prova
### **sui numeri**, senza costruire un motore.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import flussi_parziali as FP                                   # noqa: E402


def N(rho, lam):
    """### `N = rho ln(rho/(rho+Lambda))`, ### **col limite `rho -> 0` che fa `0`.**

    ### ⭐ **`x ln x -> 0` per `x -> 0`**, quindi la' il termine ### **non c'e'**: e' il
    valore che la funzione PRENDE, e ### **l'energia lo usa.**
    """
    rho = np.asarray(rho, dtype=float)
    lam = np.asarray(lam, dtype=float)
    fuori = np.zeros(np.broadcast(rho, lam).shape, dtype=float)
    vivi = rho > 0.0
    if np.any(vivi):
        r = np.broadcast_to(rho, fuori.shape)[vivi]
        s = r + np.broadcast_to(lam, fuori.shape)[vivi]
        fuori[vivi] = r * np.log(r / s)
    return fuori


def alpha(rho, lam):
    """### `alpha = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)`, ### **`0` dove `rho = 0`.**"""
    rho = np.asarray(rho, dtype=float)
    lam = np.asarray(lam, dtype=float)
    fuori = np.zeros(np.broadcast(rho, lam).shape, dtype=float)
    vivi = rho > 0.0
    if np.any(vivi):
        r = np.broadcast_to(rho, fuori.shape)[vivi]
        l = np.broadcast_to(lam, fuori.shape)[vivi]
        s = r + l
        fuori[vivi] = np.log(r / s) + l / s
    return fuori


def beta(rho, lam):
    """### `beta = -rho/(rho+Lambda)`, ### **definita OVUNQUE** *(e `0` dove `rho = 0`)*.

    ### 📌 **Qui non c'e' nessun limite da prendere:** il numeratore e' `rho`, quindi
    dove `rho = 0` la frazione fa `0` ### **senza bisogno di dirlo** — e dove `Lambda = 0`
    con `rho > 0` fa ### **`-1`**, che e' la saturazione completa.
    """
    rho = np.asarray(rho, dtype=float)
    lam = np.asarray(lam, dtype=float)
    fuori = np.zeros(np.broadcast(rho, lam).shape, dtype=float)
    vivi = rho > 0.0
    if np.any(vivi):
        r = np.broadcast_to(rho, fuori.shape)[vivi]
        fuori[vivi] = -r / (r + np.broadcast_to(lam, fuori.shape)[vivi])
    return fuori


def pezzi(rho, lam):
    """### `(alpha, beta)` in un giro solo: ### **quello che il motore chiede.**"""
    return alpha(rho, lam), beta(rho, lam)


def applica(mot, st, frazione):
    """### **IL FLUSSO, APPLICATO ALLO STATO** per `frazione * dtau`.

    ### ⛔⛔ **PERCHE- STA QUI E NON NEL MOTORE, e il motivo e- MISURATO:** con questo
    corpo dentro `motore.py` il file arrivava a ### **`714` righe**, oltre ### **il tetto
    di `700`** -- e la regola dice ### **oltre, SI DIVIDE, NON SI ALLUNGA.**
    ### ⭐ **E- lo stesso motivo per cui questo modulo e `saturazione.py` esistono:**
    ### **le funzioni della legge stanno con la legge**, e il motore resta
    ### **il REGISTRO che dice quale operatore risponde a quale `id`.**

    ### ✅ **DUE FASI E NIENT-ALTRO**, e ### **due buffer, non quattro:** la fase di
    `psi` si applica ### **prima**, poi ### **gli stessi due buffer** portano quella di
    `phi` -- le due estremita- hanno la stessa taglia, e il flusso ### **non ha bisogno
    di tenerle insieme.**
    """
    rho = mot.densita_materia(st)
    lam = mot.densita_vuoto(st)
    al, be = pezzi(rho, lam)
    nodo = mot.inc.nodo
    f = float(frazione)
    dtau = FP.dtau_nodo(mot)
    fas = mot._b("mv_fas", (st["psi_h"].shape[0],), float)
    esp = mot._b("mv_esp", fas.shape, st["phi_h"].dtype)
    np.take(al * dtau * f, nodo, out=fas)
    np.multiply(fas, -1j, out=esp)
    np.exp(esp, out=esp)
    np.multiply(st["psi_h"], esp.reshape(-1, 1), out=st["psi_h"])
    np.take(be * dtau * f, nodo, out=fas)
    np.multiply(fas, -1j, out=esp)
    np.exp(esp, out=esp)
    np.multiply(st["phi_h"], esp, out=st["phi_h"])
    mot.applicazioni["CAMM-MATERIA-VUOTO"] += 1
    return st
