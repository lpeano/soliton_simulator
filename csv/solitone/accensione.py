# -*- coding: utf-8 -*-
r"""**L'ACCENSIONE LENTA DEL VUOTO** *(il mandato di Luca delle `01:13` del `2026-11-02`, con le decisioni dopo `25614c34`; il task history
`doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`)*: ### **si parte a vuoto congelato e si accende l'aggiornamento del vuoto con `lam(t)` da `0` a `1`.**

### **`tick_acceso(z, lam)`:** il ciclo di `tick.percorri_tick` *(`mot.apri_tick`, `composizione.ORDINE`, `tick.OPERATORE`, `mot.chiudi_tick`)* con:
### **i pezzi del vuoto** *(`_solitone_vuoto_congelato.VUOTO`)* **a frazione `frazione * lam`** *(saltati a `lam = 0`: il nucleo rifiuta la frazione `0`)*;
### **la rotazione gemella `beta` scalata a `lam * beta`**, sostituendo `materia_vuoto.pezzi` con `(al, lam * be)` di quello attivo *(sotto `SF.forma`, `pezzi` e' gia'
### sostituito: scalare `MV.beta` non arriverebbe)*. ### **Il palindromo resta palindromo:** ogni pezzo del vuoto ha la stessa scala nelle due meta'.
### **Nessuna legge nuova:** `dtau` e' gia' un argomento dei pezzi.

### **La rampa** *(dichiarata nel task history, prima)*: `lam_k = sin^2(pi k / (2 K))`, `k = 1 .. K`, `K = T_acc/s`; `lam_K = 1` esatto; ### **dopo, `tick.percorri_tick`.**
"""
import math

import numpy as np


def tick_acceso(z, lam):
    """### **Un tick con l'aggiornamento del vuoto scalato di `lam`** *(dentro `SF.forma(VC.FORMA)`, `BE.conv(DC.ZERO)`, come le corse)*."""
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    import materia_vuoto as MV
    import tick as TK
    st, mot, par = z["st"], z["mot"], z["par"]
    b0 = MV.pezzi

    def pz(r, l):
        al, be = b0(r, l)
        return al, lam * be

    MV.pezzi = pz
    try:
        mot.apri_tick()
        for idl, fr, _t in CM.ORDINE:
            nome, vp = TK.OPERATORE[idl]
            if idl in VC.VUOTO:
                if lam == 0.0:
                    continue
                f = fr * lam
            else:
                f = fr
            mot.operatori[nome](st, par if vp else {}, f)
        mot.chiudi_tick()
    finally:
        MV.pezzi = b0


def lam_di(t, K):
    """### **`lam` al tick `t`** *(`1 .. K` la rampa; dopo, `1`)*."""
    if t >= K:
        return 1.0
    return math.sin(0.5 * math.pi * t / K) ** 2


def tick(z, t, K):
    """### **Il tick `t` della corsa:** nella rampa `tick_acceso(z, lam_di(t, K))`, dopo il tick intero del nucleo."""
    import composizione as CM
    import tick as TK
    if t < K:
        tick_acceso(z, lam_di(t, K))
    else:
        TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))


def mu_rayleigh(z, s):
    """### **`mu` di Rayleigh del tick INTERO** *(`psi` e `phi` evolvono insieme)* **sullo stato in `z`:** `(mu, residuo)`; ### **la scena si rimette.**"""
    import composizione as CM
    import tick as TK
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    p = salvato["psi_h"]
    try:
        TK.percorri_tick(z["st"], z["mot"], z["par"], (), None, len(CM.ORDINE))
        T = z["st"]["psi_h"].copy()
    finally:
        for k, v in salvato.items():
            z["st"][k][...] = v
    lr = complex(np.vdot(p, T) / np.vdot(p, p))
    return -math.atan2(lr.imag, lr.real) / s, float(np.linalg.norm(T - lr * p) / np.linalg.norm(p))


def vita_a_meta(tau, f, tau0, meta=0.5, coda=3000.0):
    """### **La vita principale** *(Luca, la precisazione della decisione `9`)*: ### **il primo `tau > tau0` con il cuore liscio sotto `meta` del suo valore a `tau0`.**
    ### **Se non ci arriva: l'ESTRAPOLAZIONE dichiarata** con la pendenza degli ultimi `coda` *(come `_respiro_congelato`)*.
    ### **`{"f0", "misurata", "estrapolata", "pendenza"}`** *(la pendenza per `1000`)*."""
    tau, f = np.asarray(tau), np.asarray(f)
    i0 = int(np.argmin(np.abs(tau - tau0)))
    f0 = float(f[i0])
    dopo = np.nonzero((tau > tau0) & (f < meta * f0))[0]
    m = tau >= tau[-1] - coda
    p = float(np.polyfit(tau[m], f[m], 1)[0])
    out = {"f0": f0, "tau0": float(tau[i0]), "misurata": float(tau[dopo[0]]) if len(dopo) else None, "pendenza": 1000.0 * p, "estrapolata": None}
    if not len(dopo) and p < 0:
        out["estrapolata"] = float(tau[-1] + (meta * f0 - f[-1]) / p)
    return out
