# -*- coding: utf-8 -*-
"""IL GENERATORE DELL'ACCOPPIAMENTO MATERIA-VUOTO -- ### **DAL `2026-11-01` (Luca `16:52`) LE FORME SONO DUE, `S1` (predefinita, DALLA TABELLA) E `S3` (opzione esplicita): sotto, `FORME`.** ### **E DAL `2026-11-22` (il mandato [M1631] di Luca, il torneo; sul ramo `lapse-u`) LE OPZIONI ESPLICITE SONO ANCHE `L+0.5`, `L+0.25`, `L0`, `L-0.25`, `L-0.5`, `L-1`, `FH`, `FT`** *(`doc/CARTA_torneo_nonlinearita.md`, sez. 1)*: **`S1` resta la PREDEFINITA.** Il testo che segue e' quello di `S3`.

### — **le tre funzioni, e il LIMITE.**

> `N_k = rho_k ln(rho_k / (rho_k + Lambda_k))`, con `rho_k = somma_h |psi_h|^2` e
> `Lambda_k = somma_h |phi_h|^2`. ### **Decisione di Luca del `2026-10-15`** *(`23:30`)*:
> sostituisce `CAMM-SATURAZIONE`. ### ⚠ **E IL CONTO GIUSTO E' QUESTO** *(errore `n.1`
> del guardiano, corretto il `2026-10-16`)*: ### **le leggi che GIRANO erano `6` e restano
> `6`** -- nell'ordine di composizione entra questa ed esce la saturazione, che
> ### **RESTA in tabella come SCHEDA SUPERATA.** ### **Le righe non di prova della tabella
> sono `8`, e non c'e' niente da decidere.**

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
import contextlib
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import flussi_parziali as FP                                   # noqa: E402


def N_s3(rho, lam):
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


def alpha_s3(rho, lam):
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


def beta_s3(rho, lam):
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


# =====================================================================================
#   S1 -- LA FORMA DEL LEGAME DECISA DA LUCA (decisione (1) delle `01:27`, nel nucleo dalle `16:52` del `2026-11-01`)
# =====================================================================================
# ### `N = Lambda F1(x)`, `F1(x) = x - arctan x`, `x = rho/Lambda`: ### **le espressioni di `csv/`** *(`_screening_forme_s3._ab("S1")`,
# ### `_scomposizione_solitone.F1`)*, **operazione per operazione**, perche' il confronto con le misure di `csv/` e' AL BIT.
# ### `alpha = F1'(x) = dN/drho`, `beta = F1(x) - x F1'(x) = dN/dLambda`: ### **il vuoto riceve la rotazione gemella** *(acbdfb88)*.
# ### **NESSUNA COSTANTE** *(la scala e' il vuoto locale, come per `S3`)*.
# ### ⛔ **`Lambda = 0` con `rho > 0`: il LIMITE, non un pavimento** *(l'assioma sui limiti, nel docstring di `N_s1`)*: `x -> infinito`, `alpha -> 1`, `beta -> -pi/2`, `N -> rho`.
# ### **E `rho = 0`:** `alpha = 0`, `beta = 0`, `N = 0` -- il valore che le espressioni PRENDONO *(a `Lambda > 0`, `x = 0`)*.
def N_s1(rho, lam):
    """### `N = Lambda (x - arctan x)`, `x = rho/Lambda`; ### **`rho` dove `Lambda = 0`** *(il limite, non un pavimento: `A11`)*, `0` dove `rho = 0`."""
    rho = np.asarray(rho, dtype=float)
    lam = np.asarray(lam, dtype=float)
    fuori = np.zeros(np.broadcast(rho, lam).shape, dtype=float)
    r = np.broadcast_to(rho, fuori.shape)
    l = np.broadcast_to(lam, fuori.shape)
    pieni = (r > 0.0) & (l > 0.0)
    if np.any(pieni):
        x = r[pieni] / l[pieni]
        fuori[pieni] = l[pieni] * (x - np.arctan(x))
    senza_vuoto = (r > 0.0) & (l == 0.0)
    fuori[senza_vuoto] = r[senza_vuoto]
    return fuori


def alpha_s1(rho, lam):
    """### `alpha = x^2/(1+x^2)`; ### **`1` dove `Lambda = 0`** *(il limite)*, `0` dove `rho = 0`."""
    rho = np.asarray(rho, dtype=float)
    lam = np.asarray(lam, dtype=float)
    fuori = np.zeros(np.broadcast(rho, lam).shape, dtype=float)
    r = np.broadcast_to(rho, fuori.shape)
    l = np.broadcast_to(lam, fuori.shape)
    pieni = (r > 0.0) & (l > 0.0)
    if np.any(pieni):
        x = r[pieni] / l[pieni]
        fuori[pieni] = x ** 2 / (1.0 + x ** 2)
    fuori[(r > 0.0) & (l == 0.0)] = 1.0
    return fuori


def beta_s1(rho, lam):
    """### `beta = x - arctan x - x^3/(1+x^2)`; ### **`-pi/2` dove `Lambda = 0`** *(il limite)*, `0` dove `rho = 0`."""
    rho = np.asarray(rho, dtype=float)
    lam = np.asarray(lam, dtype=float)
    fuori = np.zeros(np.broadcast(rho, lam).shape, dtype=float)
    r = np.broadcast_to(rho, fuori.shape)
    l = np.broadcast_to(lam, fuori.shape)
    pieni = (r > 0.0) & (l > 0.0)
    if np.any(pieni):
        x = r[pieni] / l[pieni]
        fuori[pieni] = x - np.arctan(x) - x ** 3 / (1.0 + x ** 2)
    fuori[(r > 0.0) & (l == 0.0)] = -0.5 * np.pi
    return fuori


# =====================================================================================
#   LA FORMA SI LEGGE DALLA TABELLA (`CAMM-MATERIA-VUOTO`, `parametri.forma`; il modulo generato)
# =====================================================================================
# ### ⛔ **NESSUNA SCELTA SCRITTA QUI:** `FORMA` e' il valore della tabella. ### **`S3` resta come OPZIONE ESPLICITA**, solo per riprodurre il
# ### vecchio *(Luca `16:52`)*: `scegli(nome)` per un processo intero, `forma_esplicita(nome)` per un contesto.
# ### ⚠ **`pezzi` e `applica` chiamano `alpha` e `beta` PER NOME DI MODULO:** cosi' la sostituzione di `MV.pezzi` di `csv/_screening_forme_s3.forma`
# ### continua a funzionare per gli strumenti di `csv/`.
# =====================================================================================
#   LE FORME DEL TORNEO -- il mandato [M1631] di Luca (2026-11-22, sul ramo `lapse-u`; la carta `doc/CARTA_torneo_nonlinearita.md`, sez. 1)
# =====================================================================================
# ### **OPZIONI ESPLICITE, come `S3`: la PREDEFINITA resta `S1`** *(il valore della tabella)*. **Nessuna costante tarata:** `lambda` e' il NOME della forma
# ### *(i sei valori del mandato)*, `FH` e `FT` non hanno parametri. **Le convenzioni di `S1`:** a `Lambda = 0` con `rho > 0` il LIMITE *(non un pavimento)*;
# ### a `rho = 0` *(con `Lambda > 0`)* il valore che le espressioni PRENDONO a `x = 0`; a `rho = 0` e `Lambda = 0` lo zero.
def _forma_lambda(lam):
    """### **Flambda:** `lambda` volte `N`, `alpha`, `beta` di `S1` *(i limiti di `S1` per `lambda`)*."""
    lam = float(lam)

    def N_l(rho, l_):
        return lam * N_s1(rho, l_)

    def alpha_l(rho, l_):
        return lam * alpha_s1(rho, l_)

    def beta_l(rho, l_):
        return lam * beta_s1(rho, l_)
    return N_l, alpha_l, beta_l


def _tre(rho, lam):
    rho = np.asarray(rho, dtype=float)
    lam = np.asarray(lam, dtype=float)
    fuori = np.zeros(np.broadcast(rho, lam).shape, dtype=float)
    r = np.broadcast_to(rho, fuori.shape)
    l = np.broadcast_to(lam, fuori.shape)
    return fuori, r, l, (r > 0.0) & (l > 0.0), (r == 0.0) & (l > 0.0), (r > 0.0) & (l == 0.0)


def N_fh(rho, lam):
    """### **FH** *(Luca `16:28`)*: `N = Lambda (x - 2 arctan x)`; ### **`rho` dove `Lambda = 0`** *(il limite)*, `0` dove `rho = 0`."""
    fuori, r, l, pieni, _vu, sv = _tre(rho, lam)
    x = r[pieni] / l[pieni]
    fuori[pieni] = l[pieni] * (x - 2.0 * np.arctan(x))
    fuori[sv] = r[sv]
    return fuori


def alpha_fh(rho, lam):
    """### **FH**: `alpha = (x^2 - 1)/(x^2 + 1)`; ### **`1` dove `Lambda = 0`** *(il limite)*, **`-1` dove `rho = 0`** *(il valore a `x = 0`)*."""
    fuori, r, l, pieni, vu, sv = _tre(rho, lam)
    x = r[pieni] / l[pieni]
    fuori[pieni] = (x ** 2 - 1.0) / (x ** 2 + 1.0)
    fuori[vu] = -1.0
    fuori[sv] = 1.0
    return fuori


def beta_fh(rho, lam):
    """### **FH**: `beta = x - 2 arctan x - x (x^2 - 1)/(x^2 + 1)`; ### **`-pi` dove `Lambda = 0`** *(il limite)*, `0` dove `rho = 0`."""
    fuori, r, l, pieni, _vu, sv = _tre(rho, lam)
    x = r[pieni] / l[pieni]
    fuori[pieni] = x - 2.0 * np.arctan(x) - x * (x ** 2 - 1.0) / (x ** 2 + 1.0)
    fuori[sv] = -np.pi
    return fuori


def _lncosh(y):
    """### `ln cosh y = |y| + log1p(e^{-2|y|}) - ln 2`: ### **la stessa funzione, in una forma che NON trabocca** *(`cosh` trabocca oltre `|y| ~ 710`; dichiarato nel task history)*."""
    a = np.abs(y)
    return a + np.log1p(np.exp(-2.0 * a)) - np.log(2.0)


_LNCOSH1 = float(_lncosh(np.float64(1.0)))
_BETA_FT_LIMITE = -1.0 - float(np.log(2.0)) - _LNCOSH1          # ### il limite di `ln cosh(x - 1) - ln cosh 1 - x tanh(x - 1)` per `x -> infinito`


def N_ft(rho, lam):
    """### **FT**: `N = Lambda (ln cosh(x - 1) - ln cosh 1)`; ### **`rho` dove `Lambda = 0`** *(il limite)*, `0` dove `rho = 0`."""
    fuori, r, l, pieni, _vu, sv = _tre(rho, lam)
    x = r[pieni] / l[pieni]
    fuori[pieni] = l[pieni] * (_lncosh(x - 1.0) - _LNCOSH1)
    fuori[sv] = r[sv]
    return fuori


def alpha_ft(rho, lam):
    """### **FT**: `alpha = tanh(x - 1)`; ### **`1` dove `Lambda = 0`** *(il limite)*, **`tanh(-1)` dove `rho = 0`** *(il valore a `x = 0`)*."""
    fuori, r, l, pieni, vu, sv = _tre(rho, lam)
    x = r[pieni] / l[pieni]
    fuori[pieni] = np.tanh(x - 1.0)
    fuori[vu] = np.tanh(-1.0)
    fuori[sv] = 1.0
    return fuori


def beta_ft(rho, lam):
    """### **FT**: `beta = ln cosh(x - 1) - ln cosh 1 - x tanh(x - 1)`; ### **`-1 - ln 2 - ln cosh 1` dove `Lambda = 0`** *(il limite)*, `0` dove `rho = 0`."""
    fuori, r, l, pieni, _vu, sv = _tre(rho, lam)
    x = r[pieni] / l[pieni]
    fuori[pieni] = _lncosh(x - 1.0) - _LNCOSH1 - x * np.tanh(x - 1.0)
    fuori[sv] = _BETA_FT_LIMITE
    return fuori


FORME = {"S1": (N_s1, alpha_s1, beta_s1), "S3": (N_s3, alpha_s3, beta_s3),
         "L+0.5": _forma_lambda(0.5), "L+0.25": _forma_lambda(0.25), "L0": _forma_lambda(0.0),
         "L-0.25": _forma_lambda(-0.25), "L-0.5": _forma_lambda(-0.5), "L-1": _forma_lambda(-1.0),
         "FH": (N_fh, alpha_fh, beta_fh), "FT": (N_ft, alpha_ft, beta_ft)}

import termini.camm_materia_vuoto as _TMV                     # noqa: E402

FORMA = _TMV.PARAMETRI["forma"]
assert FORMA in FORME, "la forma della tabella %r non e' fra quelle del nucleo %s" % (FORMA, sorted(FORME))
N, alpha, beta = FORME[FORMA]
ATTIVA = FORMA


def scegli(nome):
    """### **L'opzione esplicita, per un processo intero:** `N`, `alpha`, `beta` della forma `nome`."""
    global N, alpha, beta, ATTIVA
    assert nome in FORME, "la forma %r non e' fra quelle del nucleo %s" % (nome, sorted(FORME))
    N, alpha, beta = FORME[nome]
    ATTIVA = nome


@contextlib.contextmanager
def forma_esplicita(nome):
    """### **L'opzione esplicita, per un contesto:** rimette la forma di prima all'uscita."""
    prima = ATTIVA
    scegli(nome)
    try:
        yield
    finally:
        scegli(prima)


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
