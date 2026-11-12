# -*- coding: utf-8 -*-
r"""**IL BANCO DEL LAPSE** *(S5.1; Luca `2026-11-11` `11:33` e `13:22`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.13`)*. [[PUNTO-FISSO-CS-SOLITONE]]

**FUORI DAL NUCLEO:** usa `tick.percorri_tick`, `tick.meta_del_palindromo`, `tick.EPS_CS`, `tick.GIRI_MAX`, `energia_pesata.termini_di_h`, `energia_pesata.d_peso_arco`, `energia_pesata.pesi`
*(e attraverso `mot.cs` i pesi di `flussi_parziali`, la media ARMONICA sugli archi)* **senza modificarli.**

**Il tick col lapse** *(lo schema scelto da Luca: il palindromo con `N` a meta' passo)*:
1. **`cs = s N(rho)` dallo stato al CENTRO, a punto fisso** *(come `tick.cs_al_centro`; la copia fa la mezza reazione e mezzo palindromo)*;
2. **la reazione sulla materia, MEZZO passo prima e MEZZO dopo il palindromo:** `psi_h -> e^{-i Omega_k dtau/2} psi_h`,
   `Omega_k = s N'(rho_k) [ H_k(nodo) + somma_{a in k} (dw_a/dcs_k) H_a(arco) ]`, **col punto medio implicito** *(come `energia_pesata.applica`)*;
3. **il palindromo intero di oggi** con `mot.cs` = quel `cs` e `mot.lambda_c = None`.

**`legge`:** `("uno",)` **-- `N = 1` costante** *(`N' = 0`: la reazione non c'e', e il tick e' quello di oggi a `cs = s`)*; `("rho_c", rho_c)` **-- `N = 1/(1 + rho/rho_c)`.**
**`senza_reazione=True`:** **il DEVE FALLIRE di S5.2** *(l'orologio di nuovo a senso unico)*.
"""
import numpy as np

import composizione as CM
import energia_pesata as EP
import tick as TK

GIRI_MAX_REAZIONE = 200      # ### come energia_pesata.GIRI_MAX_OMEGA: il limite oltre il quale si DICHIARA che non converge
TOLL_REAZIONE = 1e-14        # ### Luca (S5.0 d): l'iterazione di punto fisso fino a 1e-14


def N_di(rho, legge):
    if legge[0] == "uno":
        return np.ones_like(rho)
    return 1.0 / (1.0 + rho / float(legge[1]))


def Np_di(rho, legge):
    if legge[0] == "uno":
        return np.zeros_like(rho)
    rc = float(legge[1])
    return -(1.0 / rc) / (1.0 + rho / rc) ** 2


def rho_di(mot, st):
    r = np.zeros(mot.inc.n)
    np.add.at(r, mot.inc.nodo, np.sum(np.abs(st["psi_h"].reshape(mot.inc.nodo.size, -1)) ** 2, axis=1))
    return r


def cs_di(mot, st, s, legge):
    return float(s) * N_di(rho_di(mot, st), legge)


def omega_psi(mot, st, par, s, legge):
    """### `Omega_k = s N'(rho_k) [ H_k(nodo) + somma (dw_a/dcs_k) H_a(arco) ]`, coi pesi di `mot.cs` *(il `cs` del tick)*."""
    per_nodo, per_arco = EP.termini_di_h(mot, st, par)
    dw = EP.d_peso_arco(mot)
    arco = np.zeros(mot.inc.n)
    np.add.at(arco, mot.inc.nodo, dw * np.repeat(per_arco, 2))
    return float(s) * Np_di(rho_di(mot, st), legge) * (per_nodo + arco)


def reazione(mot, st, par, s, legge, frazione):
    """### **La fase della reazione su `psi` per `dtau * frazione`, col punto medio implicito.** `(giri)`; `0` se non c'e' *(`legge` `uno`)*."""
    if legge[0] == "uno":
        return 0
    tau = float(mot.dtau[0]) * float(frazione)
    assert np.all(mot.dtau == mot.dtau[0]), "la reazione vuole un dtau uniforme"
    psi = st["psi_h"]
    salvo = psi.copy()
    nodo = mot.inc.nodo
    prec = omega_psi(mot, st, par, s, legge).copy()
    for giri in range(1, GIRI_MAX_REAZIONE + 1):
        psi[...] = salvo * np.exp(-1j * (prec * (tau * 0.5))[nodo])[:, None]
        nuovo = omega_psi(mot, st, par, s, legge)
        scarto = float(np.max(np.abs(nuovo - prec)))
        if scarto <= TOLL_REAZIONE * max(float(np.max(np.abs(nuovo))), 1e-300):
            prec = nuovo.copy()
            break
        prec = nuovo.copy()
    else:
        psi[...] = salvo
        raise AssertionError("la reazione NON converge in %d giri (ultimo scarto %.3e): si relaziona, non si sceglie un altro schema" % (GIRI_MAX_REAZIONE, scarto))
    psi[...] = salvo * np.exp(-1j * (prec * tau)[nodo])[:, None]
    return giri


def cs_al_centro(mot, st, par, s, legge, senza_reazione, omega=1.0, giri_max=None, storia=None):
    """### **`cs` dallo stato al CENTRO, a punto fisso:** la copia fa la mezza reazione e mezzo palindromo *(come `tick.cs_al_centro`)*. `(cs, giri)`.
    ### **S5.2-bis punto 3** *(lo strumento curato, non la legge)*: `omega < 1` **smorza** l'iterazione *(`cs <- cs + omega (cs_calcolato - cs)`)*; `giri_max` **il tetto** *(predefinito `tick.GIRI_MAX`)*;
    `storia` **una lista in cui si scrive lo scarto a ogni giro.** **A `omega = 1` e' lo stesso codice di prima** *(il ramo `prec = nuovo`)*."""
    meta = TK.meta_del_palindromo()
    prec = cs_di(mot, st, s, legge)
    for giri in range(1, (TK.GIRI_MAX if giri_max is None else giri_max) + 1):
        copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
        mot.cs = prec
        mot.lambda_c = None
        if not senza_reazione:
            reazione(mot, copia, par, s, legge, 0.5)
        TK.percorri_tick(copia, mot, par, (), None, meta)
        nuovo = cs_di(mot, copia, s, legge)
        scarto = float(np.max(np.abs(nuovo - prec)))
        if storia is not None:
            storia.append(scarto)
        if scarto <= TK.EPS_CS * float(np.max(np.abs(nuovo))):
            return nuovo, giri
        prec = nuovo if omega == 1.0 else prec + omega * (nuovo - prec)
    raise AssertionError("il punto fisso di cs del lapse NON converge in %d giri (ultimo scarto %.3e)" % (giri, scarto))


def fase_a(mot, st, legge, eps_a, senza_reazione):
    """### **La forma (a)** *(S5.3 A, sez. `32.1`)*: `E_N - eps_a somma_k (N_k - 1) rho_k`; **mezza fase per nodo** `e^{+i eps_a [(N_k - 1) + N'_k rho_k] / 2}` su `psi`
    *(la derivata del termine rispetto a `rho_k`; senza la reazione il termine in `N'` cade, come le altre reazioni)*. **A `N = 1` e' zero.**"""
    rho = rho_di(mot, st)
    g = N_di(rho, legge) - 1.0
    if not senza_reazione:
        g = g + Np_di(rho, legge) * rho
    st["psi_h"][...] = st["psi_h"] * np.exp(0.5j * float(eps_a) * g)[mot.inc.nodo][:, None]


def tick(mot, st, par, s, legge, senza_reazione=False, omega=1.0, giri_max=None, storia=None, eps_a=None):
    """### **UN tick col lapse.** `{"giri_cs", "giri_r1", "giri_r2"}`; `omega`, `giri_max`, `storia`: vedi `cs_al_centro` *(S5.2-bis punto 3)*.
    ### `eps_a` *(S5.3 A)*: **la forma (a)**, mezza fase PRIMA e mezza DOPO, fuori dal palindromo *(`fase_a`)*; `None` = lo stesso codice di prima."""
    if eps_a is not None:
        fase_a(mot, st, legge, eps_a, senza_reazione)
    cs, giri = cs_al_centro(mot, st, par, s, legge, senza_reazione, omega=omega, giri_max=giri_max, storia=storia)
    mot.cs = cs
    mot.lambda_c = None
    g1 = 0 if senza_reazione else reazione(mot, st, par, s, legge, 0.5)
    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    g2 = 0 if senza_reazione else reazione(mot, st, par, s, legge, 0.5)
    if eps_a is not None:
        fase_a(mot, st, legge, eps_a, senza_reazione)
    return {"giri_cs": giri, "giri_r1": g1, "giri_r2": g2}


def tick_di_oggi(mot, st, par, s):
    """### **Il tick di oggi:** `mot.cs = s` uniforme, `mot.lambda_c = None`."""
    mot.cs = np.full(mot.inc.n, float(s))
    mot.lambda_c = None
    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))


def energia(mot, st, par, s, legge):
    """### **`E_N` coi pesi DELLO STATO** *(`mot.cs = s N(rho di adesso)` per la lettura, poi si rimette)*: `somma w_k H_k + somma w_a H_a`."""
    salvo = mot.cs
    mot.cs = cs_di(mot, st, s, legge)
    try:
        per_nodo, per_arco = EP.termini_di_h(mot, st, par)
        w_nodo, w_arco = EP.pesi(mot)
        return float(np.sum(w_nodo * per_nodo)) + float(np.sum(w_arco * per_arco))
    finally:
        mot.cs = salvo
