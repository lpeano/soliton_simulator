# -*- coding: utf-8 -*-
r"""**L'ACCENSIONE LENTA DEL VUOTO** *(il mandato di Luca delle `01:13` del `2026-11-02`, con le decisioni dopo `25614c34`; il task history
`doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`)*: ### **si parte a vuoto congelato e si accende l'aggiornamento del vuoto con `lam(t)` da `0` a `1`.**

### **`tick_acceso(z, lam)`:** il ciclo di `tick.percorri_tick` *(`mot.apri_tick`, `composizione.ORDINE`, `tick.OPERATORE`, `mot.chiudi_tick`)* con:
### **i pezzi del vuoto** *(`_solitone_vuoto_congelato.VUOTO`)* **a frazione `frazione * lam`** *(saltati a `lam = 0`: il nucleo rifiuta la frazione `0`)*;
### **la rotazione gemella `beta` scalata a `lam * beta`**, sostituendo `materia_vuoto.pezzi` con `(al, lam * be)` di quello attivo *(sotto `SF.forma`, `pezzi` e' gia'
### sostituito: scalare `MV.beta` non arriverebbe)*. ### **Il palindromo resta palindromo:** ogni pezzo del vuoto ha la stessa scala nelle due meta'.
### **Nessuna legge nuova:** `dtau` e' gia' un argomento dei pezzi.

### **La vita dal cuore a blocchi e l'alone** *(Luca, dopo `bfee5330`)*: `medie_a_blocchi`, `vita_a_blocchi`, `tempo_alone`.

### **`A3`, la conservazione di `M` e `V`** *(Luca, dopo `fabce56d`)*: `a3`, ### **oltre `A3_TICK_LUNGA` tick la deriva lineare sotto `A3_PENDENZA` per `1000`.**

### **La rampa** *(dichiarata nel task history, prima)*: `lam_k = sin^2(pi k / (2 K))`, `k = 1 .. K`, `K = T_acc/s`; `lam_K = 1` esatto; ### **dopo, `tick.percorri_tick`.**
"""
import math

import numpy as np

A3_TICK_LUNGA = 100000         # ### Luca dopo fabce56d: oltre questi tick la corsa e' lunga, e A3 guarda la deriva
A3_PENDENZA = 1e-11            # ### ... lineare nel tempo e sotto 1e-11 per 1000 unita' di tempo


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


def medie_a_blocchi(tau, f, tau0, blocco=1000.0):
    """### **Le medie di `f` su blocchi `[a, a + blocco)`, `a = tau0 + k blocco`** *(Luca, dopo `bfee5330`, punto `1`)*: ### **solo i blocchi COMPLETI**, cioe' con un
    campione entro un passo di campionamento *(misurato dai campioni)* dalla fine del blocco. ### **`[(a, b, media)]`.**"""
    tau, f = np.asarray(tau), np.asarray(f)
    passo = float(np.median(np.diff(tau)))
    out = []
    a = tau0
    while a + blocco <= tau[-1] + passo:
        m = (tau >= a) & (tau < a + blocco)
        if m.any() and tau[m][-1] >= a + blocco - passo:
            out.append((a, a + blocco, float(f[m].mean())))
        a += blocco
    return out


def vita_a_blocchi(tau, f, tau0, meta=0.5, blocco=1000.0):
    """### **La vita dal cuore a blocchi** *(Luca, dopo `bfee5330`, punto `1`)*: ### **la meta' rispetto alla media del PRIMO blocco dopo `tau0`.**
    ### **Misurata:** il CENTRO del primo blocco con la media sotto meta' *(la risoluzione e' il blocco)*. ### **Altrimenti ESTRAPOLATA, dichiarata:** la retta delle
    medie contro i centri, su tutti i blocchi completi, fino a meta'; solo con la pendenza negativa e almeno `3` blocchi.
    ### **`{"rif", "blocchi", "misurata", "estrapolata", "pendenza"}`** *(la pendenza per `1000`)*."""
    bb = medie_a_blocchi(tau, f, tau0, blocco)
    rif = bb[0][2]
    out = {"rif": rif, "blocchi": bb, "misurata": None, "estrapolata": None, "pendenza": float("nan")}
    sotto = [b for b in bb if b[2] < meta * rif]
    if sotto:
        out["misurata"] = 0.5 * (sotto[0][0] + sotto[0][1])
    if len(bb) >= 3:
        cc = np.array([0.5 * (a + b) for a, b, _m in bb])
        p, c = np.polyfit(cc, np.array([m for _a, _b, m in bb]), 1)
        out["pendenza"] = 1000.0 * float(p)
        if not sotto and p < 0:
            out["estrapolata"] = float((meta * rif - c) / p)
    return out


def tempo_alone(tau, al, tau0, tau1, quota):
    """### **La vita dell'emissione** *(Luca, dopo `bfee5330`, punto `3`)*: ### **il tempo a cui la retta dell'alone su `[tau0, tau1]` arriva a `quota`**
    *(l'alone e' gia' una frazione della materia)*. ### **`(tempo o None, la pendenza per 1000, misurato)`**: `misurato` se un campione arriva gia' a `quota`;
    nessun tempo se la pendenza non e' positiva."""
    tau, al = np.asarray(tau), np.asarray(al)
    m = (tau >= tau0) & (tau <= tau1)
    p, c = np.polyfit(tau[m], al[m], 1)
    su = np.nonzero(al[m] >= quota)[0]
    if len(su):
        return float(tau[m][su[0]]), 1000.0 * float(p), True
    return (float((quota - c) / p) if p > 0 else None), 1000.0 * float(p), False


def a3(tau, x, tick, toll):
    """### **`A3`** *(Luca, dopo `fabce56d`)*: ### **fino a `A3_TICK_LUNGA` tick, `max|x/x0 - 1| <= toll`; oltre, la retta di `x/x0 - 1` contro il tempo ha la
    pendenza sotto `A3_PENDENZA` per `1000` e il residuo massimo entro `toll`** *(«lineare»: la lettura dichiarata nel task history, sez. `13-quinquies`; tolta la retta,
    il criterio di prima)*. `tick` e' il tick dell'ultimo campione. ### **`(passa, la nota)`.**"""
    tau, d = np.asarray(tau, dtype=float), np.asarray(x, dtype=float) / float(x[0]) - 1.0
    if tick <= A3_TICK_LUNGA:
        mx = float(np.max(np.abs(d)))
        return mx <= toll, "corta (%d tick): max %.2e (la tolleranza %g)" % (tick, mx, toll)
    p, c = np.polyfit(tau, d, 1)
    res = float(np.max(np.abs(d - (p * tau + c))))
    return abs(1000.0 * p) <= A3_PENDENZA and res <= toll, "lunga (%d tick): la pendenza %+.3e per 1000 (il tetto %g), il residuo %.2e (la tolleranza %g)" % (
        tick, 1000.0 * p, A3_PENDENZA, res, toll)
