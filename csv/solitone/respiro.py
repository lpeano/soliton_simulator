# -*- coding: utf-8 -*-
r"""**IL RESPIRO SULLA CARTA** *(il mandato di Luca del `2026-11-02` dopo `25614c34`, punto `3`; il task history `doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`, sez. `6-bis`)*:
### **la serie DENSA del cuore** *(il tick intero, il cuore liscio a ogni tick)*, ### **`Omega` dai picchi, coi cambi di segno e col passo;**
### **le frequenze sul cerchio** *(mod `2 pi/s`)*: **il margine da un intervallo e la somma di due bande.**

### ⚠ **I campioni committati del cuore sono ogni `10` tick** *(`1.5` unita' di tempo)*: ### **un respiro non si legge da li'** *(gli alias, `misure.periodo_dai_cambi`)*.
### **Un picco conta se nella finestra ci stanno almeno `PERIODI_MIN` periodi:** sotto, e' la deriva lenta, non un respiro *(un limite della finestra, non un parametro)*.
"""
import math

import numpy as np

from . import misure as MI

PERIODI_MIN = 10               # ### un picco con meno di 10 periodi nella finestra e' deriva, non respiro (task history, sez. 6-bis)


def serie_densa(z, t0, t1, w_in, h):
    """### **Il tick INTERO del nucleo** *(come `_vuoto_vivo_B.corsa`: `SF.forma(VC.FORMA)`, `BE.conv(DC.ZERO)`, `tick.percorri_tick` col `par` della scena)*
    **da `t0` a `t1` sullo stato che sta in `z`**, ### **il cuore liscio a ogni tick** *(`misure.campione`)*: ### **`(t, f_liscia, w)` come array.**"""
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    tt, fl, ww = [], [], []
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        for t in range(t0 + 1, t1 + 1):
            TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))
            c = MI.campione(z, t, w_in, h)
            tt.append(t)
            fl.append(c["f_liscia"])
            ww.append(c["w"])
    return np.array(tt), np.array(fl), np.array(ww)


def _potenza(t, r, f):
    """### **La varianza spiegata da `a cos + b sin` alla frequenza `f`** *(minimi quadrati, la tendenza quadratica nel disegno)*."""
    X = np.column_stack([np.ones_like(t), t, t * t, np.cos(2.0 * math.pi * f * t), np.sin(2.0 * math.pi * f * t)])
    c = np.linalg.lstsq(X, r, rcond=None)[0]
    return float(np.sum((X @ c - r) ** 2)), c


def omega(y, passo, quanti=5):
    """### **I picchi dello spettro di `y`** *(campionata ogni `passo`)*: tolta la tendenza quadratica, la finestra di Hann, i massimi locali;
    ### **ogni picco rifinito coi minimi quadrati** *(`a cos + b sin` piu' la tendenza, la frequenza nel suo intervallo di `+- 1` canale)*.
    ### **Solo i picchi con almeno `PERIODI_MIN` periodi nella finestra.** ### **Accanto, il periodo dai cambi di segno** *(`misure.periodo_dai_cambi`, con gli alias)*.
    ### **`{"picchi": [{frequenza, periodo, Omega, ampiezza}], "cambi": ..., "canale": df, "finestra": T}`**, i picchi per ampiezza decrescente."""
    from scipy.optimize import minimize_scalar
    y = np.asarray(y, dtype=float)
    n = len(y)
    t = np.arange(n) * passo
    r = y - np.polyval(np.polyfit(t, y, 2), t)
    F = np.abs(np.fft.rfft(r * np.hanning(n)))
    df = 1.0 / (n * passo)
    fmin = PERIODI_MIN / (n * passo)
    loc = [i for i in range(1, len(F) - 1) if F[i] > F[i - 1] and F[i] >= F[i + 1] and i * df >= fmin]
    loc.sort(key=lambda i: -F[i])
    picchi = []
    for i in loc[:quanti]:
        m = minimize_scalar(lambda f: _potenza(t, y, f)[0], bounds=((i - 1) * df, (i + 1) * df), method="bounded", options={"xatol": 1e-12 * df})
        f = float(m.x)
        c = _potenza(t, y, f)[1]
        picchi.append({"frequenza": f, "periodo": 1.0 / f, "Omega": 2.0 * math.pi * f, "ampiezza": float(math.hypot(c[3], c[4])), "canale": i})
    return {"picchi": picchi, "cambi": MI.periodo_dai_cambi(r, passo), "canale": df, "finestra": n * passo}


def elenco(r, frazione, primi):
    """### **I picchi da tenere** *(la decisione di Luca dopo `04b02794`)*: ### **i primi `primi` di `r["picchi"]`, piu' quelli con ampiezza `>= frazione` volte il primo;**
    ### **due picchi rifiniti entro `1` canale sono lo stesso picco** *(un lobo della finestra)*: si tiene il piu' ampio. **L'ordine di `r["picchi"]` resta.**"""
    pp = r["picchi"]
    a1 = pp[0]["ampiezza"]
    presi = [p for j, p in enumerate(pp) if j < primi or p["ampiezza"] >= frazione * a1]
    out = []
    for p in presi:
        gemelli = [q for q in presi if abs(q["frequenza"] - p["frequenza"]) <= r["canale"]]
        if max(gemelli, key=lambda q: q["ampiezza"]) is p:
            out.append(p)
    return out


def presenza(y, passo, f):
    """### **La significativita' di `f` in `y`** *(l'aggiunta di Luca delle `09:20`)*: ### **l'ampiezza rifinita a `f`** *(`a cos + b sin` piu' la tendenza quadratica)*
    **divisa per la MEDIANA dello spettro d'ampiezza** *(Hann, tolta la tendenza, i canali con almeno `PERIODI_MIN` periodi)*. ### **Adimensionale: si confronta fra osservabili.**
    ### **`(significativita', ampiezza, quota)`:** la quota e' `a^2/2` sulla varianza di `y` tolta la tendenza, ### **la parte della fluttuazione di `y` che sta a `f`**.
    ### ⚠ **Su una serie liscia la mediana e' il fondo delle code della finestra, non un rumore** *(la prova a secco: significativita' fino a `~3e5`)*: ### **la classe di un
    picco si legge dalla QUOTA; la significativita' dice solo se il picco c'e'** *(il task history, sez. `8-bis`, l'annotazione)*."""
    y = np.asarray(y, dtype=float)
    n = len(y)
    t = np.arange(n) * passo
    r = y - np.polyval(np.polyfit(t, y, 2), t)
    w = np.hanning(n)
    A = 2.0 * np.abs(np.fft.rfft(r * w)) / float(w.sum())
    k0 = int(math.ceil(PERIODI_MIN))
    c = _potenza(t, y, f)[1]
    a = float(math.hypot(c[3], c[4]))
    return a / float(np.median(A[k0:])), a, 0.5 * a * a / float(np.mean(r * r))


def serie_modi(z, t0, t1, w_in, h):
    """### **Come `serie_densa`, con gli osservabili dei modi** *(l'aggiunta di Luca delle `09:20`; il task history, sez. `8-bis`)*: a ogni tick
    ### **`misure.campione`** *(`f_liscia`, `w`, `x`, `y`)*, ### **`Lambda` medio sotto il solitone** `sum(rho lam)/sum(rho)` *(`_energia_del_legame.densita`)*,
    ### **la deformazione** `Q2 = sum(rho g (dx + i dy)^2)/sum(rho g r^2)`, `Q3 = sum(rho g (dx + i dy)^3)/sum(rho g r^3)` *(`g` la rampa del cuore liscio)*.
    ### **Un dict di array:** `t`, `f_liscia`, `w`, `x`, `y`, `lam`, `q2`, `q3` *(complessi)*."""
    import _deriva_congelato as DC
    import _energia_del_legame as EL
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    out = {k: [] for k in ("t", "f_liscia", "w", "x", "y", "lam", "q2", "q3")}
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        for t in range(t0 + 1, t1 + 1):
            TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))
            c = MI.campione(z, t, w_in, h)
            rho, lam = EL.densita(z["inc"], z["st"])
            u = (z["pos"][:, 0] - c["x"]) + 1j * (z["pos"][:, 1] - c["y"])
            r = np.abs(u)
            g = rho * np.clip((w_in + 0.5 * h - r) / h, 0.0, 1.0)
            for k in ("t", "f_liscia", "w", "x", "y"):
                out[k].append(c[k])
            out["lam"].append(float(rho @ lam) / float(rho.sum()))
            out["q2"].append(complex(np.sum(g * u ** 2) / np.sum(g * r ** 2)))
            out["q3"].append(complex(np.sum(g * u ** 3) / np.sum(g * r ** 3)))
    return {k: np.array(v) for k, v in out.items()}


def armonica_di(f, f1, df, nmax=5):
    """### **`n` se `f` e' entro `2` canali da `n f1`** *(`n = 2 .. nmax`)*, altrimenti `None`."""
    for k in range(2, nmax + 1):
        if abs(f - k * f1) <= 2.0 * df:
            return k
    return None


# ====================================================================== LE FREQUENZE SUL CERCHIO
def margine_mod(x, iv, P):
    """### **`(dentro, margine)`:** la distanza di `x` dall'intervallo `iv = (lo, hi)` sul cerchio di periodo `P`; ### **negativo se dentro** *(la profondita')*.
    ### **Un intervallo largo almeno `P` copre tutto il cerchio.**"""
    lo, hi = iv
    w = hi - lo
    if w >= P:
        return True, -0.5 * P
    u = float(np.mod(x - lo, P))
    if u <= w:
        return True, -min(u, w - u)
    return False, min(u - w, P - u)


def somma(a, b):
    """### **La somma di Minkowski di due intervalli:** `(a0 + b0, a1 + b1)`."""
    return (a[0] + b[0], a[1] + b[1])


def opposto(a):
    return (-a[1], -a[0])
