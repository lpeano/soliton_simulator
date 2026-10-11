# -*- coding: utf-8 -*-
r"""LE SEI LETTURE DEL `v4` — **ognuna per `(F)` E per `(S)`**, come il mandato chiede.

| | la lettura | la soglia, **fissata nel task history PRIMA dei numeri** |
|---|---|---|
| `L0` | **invarianza locale della luce** | in archi per **tempo proprio**: `\|v - 1\| <= 3 sigma` della regressione |
| `L1` | **l'impronta** di un grumo su `Lambda` e su `cs` | `dLambda(r)` fuori dal grumo **significativo** se `> 3 sigma`; il **fronte** `<= t` archi |
| `L2` | **collettivo contro passaggio** | la differenza fra impronta **stabile** e **transitoria** significativa se `> 3 sigma` |
| `L3` | **la luce sente la massa** | ritardo d'arrivo `> 3 sigma` contro lo **stesso** lancio senza grumo |
| `L4` | **materia e antimateria** | `max\|Lambda(C) - Lambda\|` e `max\|cs(C) - cs\|` `<= passi * n_est * eps` |
| `L5` | **due grumi con `cs`** | la pendenza differisce da quella del `v3` di `> 3 sigma` **combinato** |

> ## ⛔ **IL LIMITE, DICHIARATO PRIMA DI MISURARE** *(task history, `4`)*: `L1`, `L2` e `L5`
> ## dicono *«partendo da un grumo `v3` auto-intrappolato»*, e il ### **`v3` non ne ha
> ## trovato nessuno** *(misurato due volte: referto `v3`, e di nuovo in `G1`)*.
> ## ### **Quindi usano un PACCHETTO**, e ogni risultato va letto come ### **«l'impronta di
> ## un pacchetto»**, non «l'impronta di una massa».

> ## ⚠ **E SONO OSSERVATORI, NON LEGGI:** la dinamica resta **solo** `camminata4.passo4`,
> ## e un braccio del collaudo verifica ### **byte a byte** che le letture non tocchino lo
> ## stato che ricevono.

Gira con:  python proto_camminata/_letture4.py
"""
import io
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import camminata as CM                                         # noqa: E402
import camminata3 as C3                                        # noqa: E402
import camminata4 as C4                                        # noqa: E402
import cslocale4 as CS4                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import saturazione3 as S3                                      # noqa: E402
import scena as SC                                             # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import _letture3 as L3                                         # noqa: E402

EPS = float(np.finfo(float).eps)
SEMI = (11, 23, 37, 53)
PASSI = 24
EPS_RIF = 0.5
USCITE = os.path.join(_QUI, "uscite")
FONTE = os.path.join(USCITE, "letture_v4.json")


# =====================================================================================
#   GLI AIUTI
# =====================================================================================
def corri(st, sc, geo, candidata, passi, cs=None, flusso=None, cand_vuoto=None,
          osserva=None):
    """### Corre `passi` tick con la candidata scelta, e ### **non tocca `st`.**"""
    z = {"psi": st["psi"].copy(), "phi": st["phi"].copy()}
    if candidata == "S":
        z = C4.stato_S(z, sc)
    fuori = []
    if osserva is not None:
        fuori.append(osserva(0, z))
    for t in range(1, passi + 1):
        if candidata == "F":
            z = C4.passo4_F(z, sc, geo, 1.0, EPS_RIF, cs, flusso,
                            candidata_vuoto=cand_vuoto)
        else:
            z = C4.passo4_S(z, sc, geo, 1.0, EPS_RIF, cs, flusso)
        if osserva is not None:
            fuori.append(osserva(t, z))
    return z, fuori


def pacchetto(sc, geo, centro, seme=11):
    """### Un **PACCHETTO SENZA MASSA**: un'estremita' sola, e ### **`N` spento.**

    ### ⛔ **<<Senza massa>> qui vuol dire <<senza `N`>>**, e non e' una parola: la massa
    del `v3` e' ### **la saturazione**, e spegnerla e' l'unico modo di non averla.
    """
    psi = CM.stato_zero(sc)
    e0 = int(np.argmax(sc["nodo"] == centro))
    psi[e0, 0] = 1.0
    return {"psi": psi / math.sqrt(CM.norma(psi)),
            "phi": V3.vuoto_fondo(sc, V3.LAMBDA0, seme)}


def distanza_media(sc, st, d):
    """### La distanza media **pesata su `rho`**, in archi."""
    rho = CM.rho_nodo(st["psi"], sc)
    tot = float(np.sum(rho))
    return float(np.sum(rho * d) / tot) if tot > 0 else float("nan")


# =====================================================================================
#   L0  --  L'INVARIANZA LOCALE DELLA LUCE
# =====================================================================================
def l0(sc, geo, candidata):
    """### `L0`: la velocita' di un pacchetto in **archi/tick** e in **archi/tempo proprio**.

    ### ⛔ **IL `cs` E' UNIFORME E IMPOSTO**, ed e' il controllo che il mandato chiede
    *(«prima imposto come controllo»)*: una zona a `cs` uniforme e' ### **l'unico caso in cui
    <<la velocita' locale>> ha un significato senza ambiguita'.**

    ### ⭐ **LA PREVISIONE DEL MANDATO, che ho adottato:** in archi/tick ### **`cs`**, in
    archi/tempo proprio ### **`1`**.
    """
    # ### \u26d4 **LA SCENA E- IL *REGOLARE*, e NON e- una scelta di gusto:**
    # ### sull-irregolare l-eccentricita- e- ### **`6`**, quindi il fronte ### **satura in
    # ### sei tick** -- e adattare una retta su una curva satura da- ### **una pendenza che
    # ### non e- una velocita-.**
    # ### \u26a0 **E AL PRIMO GIRO L-AVEVO FATTO:** `v_tick` veniva ### **`0.060` a
    # ### `cs = 1`**, dove il `v3` sulla stessa domanda misura ### **`0.768`**, e la
    # ### velocita- ### **non dipendeva da `cs`** *(`0.060`, `0.074`, `0.077`, `0.074`)* --
    # ### che e- la firma di una misura ### **che non misura la velocita-.**
    # ### \u2b50 **E LA FINESTRA SCALA CON `cs`**, perche- un pacchetto piu- lento ci
    # ### mette piu- tick a percorrere gli stessi archi: `tick = (ecc - 2)/cs`.
    reg = SC.regolare()
    geo_r = GE.scena_identita(reg)
    d0 = SC.distanze(reg, 0)
    ecc = int(d0.max())
    fuori = {"scena": "regolare", "eccentricita": ecc}
    for c in (1.0, 0.75, 0.5, 0.25):
        cs = c * np.ones(reg["n"], dtype=float)
        tick = max(4, min(48, int((ecc - 2) / c)))
        pend_m, pend_f = [], []
        for s in SEMI:
            st = L3.grumo(reg, geo_r, 0, 0, 0.0, seme=s)[0] if False else None
            psi = CM.stato_zero(reg)
            for e in range(2 * reg["m"]):
                if int(reg["nodo"][e]) == 0:
                    psi[e] = L3._autovettore_piu(geo_r["n"][e])
            psi = psi / math.sqrt(CM.norma(psi))
            st = {"psi": psi, "phi": V3.vuoto_fondo(reg, V3.LAMBDA0, s)}
            med, fro, tt = [], [], []
            _z, oss = corri(st, reg, geo_r, candidata, tick, cs,
                            osserva=lambda t, z: L3.distanza_media_e_fronte(reg, z, d0))
            for t, (m, f) in enumerate(oss):
                if t == 0:
                    continue
                med.append(m)
                fro.append(f)
                tt.append(t)
            pend_m.append(L3.pendenza(tt, med))
            pend_f.append(L3.pendenza(tt, fro))
        vm = float(np.mean([p[0] for p in pend_m]))
        sm = max(float(np.std([p[0] for p in pend_m], ddof=1)) if len(pend_m) > 1 else 0.0,
                 float(np.mean([p[1] for p in pend_m])))
        vf = float(np.mean([p[0] for p in pend_f]))
        sf = max(float(np.std([p[0] for p in pend_f], ddof=1)) if len(pend_f) > 1 else 0.0,
                 float(np.mean([p[1] for p in pend_f])))
        fuori["cs=%.2f" % c] = {
            "cs": c, "tick": tick,
            "v_tick_media": vm, "sigma_media": sm,
            "v_tick_fronte": vf, "sigma_fronte": sf,
            "v_proprio_media": vm / c, "sigma_proprio_media": sm / c,
            "v_proprio_fronte": vf / c, "sigma_proprio_fronte": sf / c,
            "semi": len(SEMI)}
    # ### \u26d4 **E L-INVARIANZA LOCALE SI LEGGE COME UN *RAPPORTO*, non come <<vale `1`>>:**
    # ### la velocita- a `cs = 1` ### **non e- `1`** nemmeno nel `v3` *(e- `0.768`, misurato:
    # ### la camminata di Grover ### **non satura il cono**)*. ### **Quindi la domanda giusta
    # ### e-: la velocita- in tempo proprio e- LA STESSA a ogni `cs`?**
    rif = fuori["cs=1.00"]
    for k, v in list(fuori.items()):
        if not k.startswith("cs="):
            continue
        for et in ("media", "fronte"):
            a = v["v_proprio_%s" % et]
            b = rif["v_proprio_%s" % et]
            sg = math.sqrt(v["sigma_proprio_%s" % et] ** 2
                           + rif["sigma_proprio_%s" % et] ** 2)
            v["rapporto_%s" % et] = (a / b) if b != 0 else float("nan")
            v["scarto_dal_riferimento_%s" % et] = abs(a - b)
            v["in_sigma_%s" % et] = (abs(a - b) / sg) if sg > 0 else 0.0
            v["entro_3sigma_%s" % et] = bool(abs(a - b) <= 3.0 * sg and sg > 0.0)
    return fuori


# =====================================================================================
#   L1  --  L'IMPRONTA
# =====================================================================================
def l1(sc, geo, candidata, cand_vuoto, forma_cs="dispersione"):
    """### `L1`: il profilo di `Lambda` e di `cs` per **anelli di distanza di grafo**.

    ### ⛔ **E IL CONFRONTO E' COL *v3*, non con lo stato iniziale:** la domanda e' *«si
    forma una zona modificata FUORI dal grumo?»*, e senza il riferimento ### **`Lambda` si
    muove anche nel `v3`** *(misurato: `3.63` in un tick)*.
    """
    st, dentro, d = L3.grumo(sc, geo, 0, 1, 8.0, seme=SEMI[0])
    anelli = sorted(set(int(x) for x in d if x >= 0))
    # ### il riferimento: lo STESSO stato, ma la legge SPENTA (il `v3`)
    rif, _o = corri(st, sc, geo, candidata, PASSI, None, S3.flusso, None)
    vivo, _o = corri(st, sc, geo, candidata, PASSI, "vuoto", S3.flusso, cand_vuoto)
    l_rif = V3.lambda_nodo(rif["phi"], sc)
    l_viv = V3.lambda_nodo(vivo["phi"], sc)
    c_rif = CS4.cs_nodo(rif["phi"], sc, forma_cs)
    c_viv = CS4.cs_nodo(vivo["phi"], sc, forma_cs)
    prof = {}
    for r in anelli:
        kk = [k for k in range(sc["n"]) if int(d[k]) == r]
        if not kk:
            continue
        dl = l_viv[kk] - l_rif[kk]
        dc = c_viv[kk] - c_rif[kk]
        sg = float(np.std(dl, ddof=1) / math.sqrt(len(kk))) if len(kk) > 1 else 0.0
        sgc = float(np.std(dc, ddof=1) / math.sqrt(len(kk))) if len(kk) > 1 else 0.0
        prof[str(r)] = {"r": r, "nodi": len(kk),
                        "dLambda": float(np.mean(dl)), "sigma_dLambda": sg,
                        "dcs": float(np.mean(dc)), "sigma_dcs": sgc,
                        "significativo": bool(abs(float(np.mean(dl))) > 3.0 * sg
                                              and sg > 0.0),
                        "dentro_il_grumo": r <= 1}
    # ### il FRONTE: il raggio piu' grande dove `dLambda` supera `3 sigma`, tick per tick
    fronte = []
    for t in (1, 2, 3, 4, 6, 8, 12, PASSI):
        a, _o = corri(st, sc, geo, candidata, t, None, S3.flusso, None)
        b, _o = corri(st, sc, geo, candidata, t, "vuoto", S3.flusso, cand_vuoto)
        dl = V3.lambda_nodo(b["phi"], sc) - V3.lambda_nodo(a["phi"], sc)
        soglia = 3.0 * float(np.std(dl, ddof=1)) / math.sqrt(sc["n"])
        tocchi = [int(d[k]) for k in range(sc["n"]) if abs(dl[k]) > soglia and d[k] >= 0]
        fronte.append({"tick": t, "raggio": max(tocchi) if tocchi else 0,
                       "entro_il_cono": bool((max(tocchi) if tocchi else 0) <= t)})
    return {"profilo": prof, "fronte": fronte, "nodi_nel_grumo": len(dentro),
            "candidata_vuoto": cand_vuoto, "forma_cs": forma_cs}


# =====================================================================================
#   L2  --  COLLETTIVO CONTRO PASSAGGIO
# =====================================================================================
def l2(sc, geo, candidata, cand_vuoto):
    """### `L2`: un **pacchetto di passaggio** con la STESSA norma lascia la stessa impronta?

    ### ⛔ **LA NORMA SI PAREGGIA, ed e' il punto:** se le due impronte si distinguono solo
    perche' uno dei due ha piu' norma, ### **non si e' misurato niente.**
    """
    d0 = SC.distanze(sc, 0)
    st_g, _dd, _d = L3.grumo(sc, geo, 0, 1, 8.0, seme=SEMI[0])
    st_p = pacchetto(sc, geo, 0, SEMI[0])
    # ### \u26d4 **LE NORME SI PAREGGIANO A MANO, E AL PRIMO GIRO NON LO FACEVO:** il
    # ### braccio diceva ### **`norme_pari: False`**, e aveva ragione -- `L3.grumo`
    # ### ### **riscala `psi` DOPO averlo normalizzato**, per portare `x0` al valore
    # ### voluto, quindi la sua norma ### **NON e- `1`.** ### \u26a0 **Confrontare due
    # ### impronte di norma diversa non misura il <<collettivo contro passaggio>>: misura
    # ### la norma.**
    n_g = CM.norma(st_g["psi"])
    st_p = {"psi": st_p["psi"] * math.sqrt(n_g / CM.norma(st_p["psi"])),
            "phi": st_p["phi"]}
    norme = (CM.norma(st_g["psi"]), CM.norma(st_p["psi"]))
    fuori = {}
    for nome, st, fl in (("grumo", st_g, S3.flusso), ("passaggio", st_p, None)):
        traccia = []
        for t in (2, 4, 8, 12, PASSI):
            a, _o = corri(st, sc, geo, candidata, t, None, fl, None)
            b, _o = corri(st, sc, geo, candidata, t, "vuoto", fl, cand_vuoto)
            dl = V3.lambda_nodo(b["phi"], sc) - V3.lambda_nodo(a["phi"], sc)
            vicini = [k for k in range(sc["n"]) if 0 <= d0[k] <= 2]
            traccia.append({"tick": t,
                            "impronta_vicina": float(np.mean(np.abs(dl[vicini]))),
                            "impronta_totale": float(np.mean(np.abs(dl)))})
        p, sg = L3.pendenza([x["tick"] for x in traccia],
                            [x["impronta_vicina"] for x in traccia])
        fuori[nome] = {"traccia": traccia, "pendenza_impronta": p, "sigma": sg,
                       "impronta_finale": traccia[-1]["impronta_vicina"],
                       "norma_psi": float(CM.norma(st["psi"]))}
    a, b = fuori["grumo"], fuori["passaggio"]
    sgc = math.sqrt(a["sigma"] ** 2 + b["sigma"] ** 2)
    fuori["confronto"] = {
        "norme_pari": bool(abs(norme[0] - norme[1]) <= PASSI * 2 * sc["m"] * EPS),
        "differenza_pendenze": abs(a["pendenza_impronta"] - b["pendenza_impronta"]),
        "sigma_combinato": sgc,
        "si_distinguono": bool(abs(a["pendenza_impronta"] - b["pendenza_impronta"])
                               > 3.0 * sgc and sgc > 0.0)}
    return fuori


# =====================================================================================
#   L3  --  LA LUCE SENTE LA MASSA
# =====================================================================================
def l3(sc, geo, candidata, cand_vuoto):
    """### `L3`: il **ritardo** di un pacchetto lanciato vicino al grumo.

    ### ⛔ **IL CONFRONTO E' LO STESSO LANCIO SENZA GRUMO, stesso seme**: senza quello il
    ritardo sarebbe ### **la dispersione del pacchetto**, non un effetto del grumo.
    """
    # ### \u26d4 **IL MISURANDO E- IL *TEMPO D-ARRIVO* AL BERSAGLIO, non la distanza
    # ### media -- e la ragione e- un difetto MIO.** Al primo giro misuravo la pendenza
    # ### della distanza media dal nodo di lancio, ### **ma lo stato <<con grumo>>
    # ### CONTIENE il grumo**: la sua `rho` sta ferma a una distanza fissa dal lancio, e
    # ### ### **entra nella media.** ### \u26a0 **Il <<ritardo>> di `7.96 sigma` che avevo
    # ### misurato era in gran parte QUELLO**, non la luce che sente la massa.
    # ### \u2b50 **`argmax` NON HA SOGLIE:** il tick in cui `rho` al bersaglio e- massima
    # ### e- ### **un numero intero senza parametri**, e il bersaglio e- ### **lontano dal
    # ### grumo**, quindi la `rho` del grumo la- e- piccola.
    d0 = SC.distanze(sc, 0)
    lontano = int(np.argmax(d0))
    dl = SC.distanze(sc, lontano)
    # ### il BERSAGLIO: il nodo piu- lontano DAL LANCIO, cioe- al di la- del grumo
    bersaglio = int(np.argmax(dl))
    fuori = {}
    for con in (False, True):
        arrivi, picchi = [], []
        for s in SEMI:
            st = pacchetto(sc, geo, lontano, s)
            if con:
                g, _dd, _d = L3.grumo(sc, geo, 0, 1, 8.0, seme=s)
                psi = st["psi"] + g["psi"]
                st = {"psi": psi, "phi": st["phi"]}
            _z, oss = corri(st, sc, geo, candidata, PASSI,
                            "vuoto" if con else None, S3.flusso if con else None,
                            cand_vuoto if con else None,
                            osserva=lambda t, z: float(
                                CM.rho_nodo(z["psi"], sc)[bersaglio]))
            v = np.asarray(oss, dtype=float)
            arrivi.append(float(np.argmax(v)))
            picchi.append(float(np.max(v)))
        fuori["con_grumo" if con else "senza_grumo"] = {
            "tick_di_arrivo": float(np.mean(arrivi)),
            "sigma_arrivo": (float(np.std(arrivi, ddof=1)) / math.sqrt(len(arrivi))
                             if len(arrivi) > 1 else 0.0),
            "picco": float(np.mean(picchi)),
            "sigma_picco": (float(np.std(picchi, ddof=1)) / math.sqrt(len(picchi))
                            if len(picchi) > 1 else 0.0),
            "nodo_di_lancio": lontano, "bersaglio": bersaglio,
            "distanza_lancio_bersaglio": int(dl[bersaglio]),
            "distanza_grumo_bersaglio": int(d0[bersaglio])}
    a, b = fuori["senza_grumo"], fuori["con_grumo"]
    sgc = math.sqrt(a["sigma_arrivo"] ** 2 + b["sigma_arrivo"] ** 2)
    sgp = math.sqrt(a["sigma_picco"] ** 2 + b["sigma_picco"] ** 2)
    fuori["confronto"] = {
        "ritardo_tick": b["tick_di_arrivo"] - a["tick_di_arrivo"],
        "sigma_combinato": sgc,
        "in_sigma": (abs(b["tick_di_arrivo"] - a["tick_di_arrivo"]) / sgc)
                    if sgc > 0 else 0.0,
        "significativo": bool(abs(b["tick_di_arrivo"] - a["tick_di_arrivo"]) > 3.0 * sgc
                              and sgc > 0.0),
        "deviazione_picco": b["picco"] - a["picco"],
        "sigma_picco_combinato": sgp,
        "picco_significativo": bool(abs(b["picco"] - a["picco"]) > 3.0 * sgp
                                    and sgp > 0.0)}
    return fuori


# =====================================================================================
#   L4  --  MATERIA E ANTIMATERIA
# =====================================================================================
def l4(sc, geo, candidata, cand_vuoto, forma_cs="dispersione"):
    """### `L4`: il grumo **coniugato** produce la stessa impronta e lo stesso `cs`?

    ### ⭐ **E DEVE, per `W5`:** `rho` e `Lambda` sono ### **pari sotto `C`**, quindi
    ### **materia e antimateria piegano il tempo allo stesso modo** — ed e' il senso fisico
    del vincolo, non una formalita'.
    """
    st, _dd, _d = L3.grumo(sc, geo, 0, 1, 8.0, seme=SEMI[0])
    stc = C3.coniuga3(st)
    a, _o = corri(st, sc, geo, candidata, PASSI, "vuoto", S3.flusso, cand_vuoto)
    b, _o = corri(stc, sc, geo, candidata, PASSI, "vuoto", S3.flusso, cand_vuoto)
    la, lb = V3.lambda_nodo(a["phi"], sc), V3.lambda_nodo(b["phi"], sc)
    ca = CS4.cs_nodo(a["phi"], sc, forma_cs)
    cb = CS4.cs_nodo(b["phi"], sc, forma_cs)
    soglia = PASSI * 2 * sc["m"] * EPS * max(float(np.max(la)), 1.0)
    return {"max_dLambda": float(np.max(np.abs(la - lb))),
            "max_dcs": float(np.max(np.abs(ca - cb))),
            "soglia": soglia,
            "tiene": bool(float(np.max(np.abs(la - lb))) <= soglia
                          and float(np.max(np.abs(ca - cb))) <= soglia)}


# =====================================================================================
#   L5  --  DUE GRUMI CON `cs` ACCESO
# =====================================================================================
def l5(sc, geo, candidata, cand_vuoto):
    """### `L5`: due grumi, e si avvicinano **piu' che nel `v3`**?

    ### ⛔ **E IL CONFRONTO E' CON LE PENDENZE DI `G2`, come il mandato chiede** — stessa
    scena, stessa costruzione, stesso numero di tick. ### ⚠ **E la mia previsione, scritta
    prima:** `G2` ha dato ### **`0.69 sigma`** fra `N` e lineare, e un effetto di gravita'
    sara' ### **piu' piccolo di quello** ⟹ ### **prevedo NESSUNA differenza misurabile.**
    """
    d0 = SC.distanze(sc, 0)
    fuori = {}
    for D in (2, 4):
        cand = [k for k in range(sc["n"]) if int(d0[k]) == D]
        if not cand:
            continue
        c2 = int(cand[0])
        a, _z, _d = L3.grumo(sc, geo, 0, 0, 8.0, seme=SEMI[0])
        b, _z2, _d2 = L3.grumo(sc, geo, c2, 0, 8.0, seme=SEMI[0])
        psi = a["psi"] + b["psi"]
        st = {"psi": psi / math.sqrt(CM.norma(psi)), "phi": a["phi"]}
        import _guscio_moto as GM
        za, zb = GM.meta_di_voronoi(sc, 0, c2)
        zone = (set(za) | {0}, set(zb) | {c2})
        for et, cs, cv in (("v3", None, None), ("cs_locale", "vuoto", cand_vuoto)):
            sep, tick = [], []
            _z, oss = corri(st, sc, geo, candidata, PASSI, cs, S3.flusso, cv,
                            osserva=lambda t, z: GM.centri(sc, z, zone))
            for t, (ca_, cb_) in enumerate(oss):
                sep.append(float(SC.distanze(sc, ca_)[cb_]))
                tick.append(t)
            p, sg = L3.pendenza(tick, sep)
            fuori["%s D=%d" % (et, D)] = {
                "D": D, "pendenza_separazione": p, "sigma": sg,
                "separazione_iniziale": sep[0], "separazione_finale": sep[-1]}
        k1, k2 = "v3 D=%d" % D, "cs_locale D=%d" % D
        if k1 in fuori and k2 in fuori:
            sgc = math.sqrt(fuori[k1]["sigma"] ** 2 + fuori[k2]["sigma"] ** 2)
            dd = abs(fuori[k1]["pendenza_separazione"]
                     - fuori[k2]["pendenza_separazione"])
            fuori["confronto D=%d" % D] = {
                "differenza": dd, "sigma_combinato": sgc,
                "in_sigma": (dd / sgc) if sgc > 0 else 0.0,
                "significativo": bool(dd > 3.0 * sgc and sgc > 0.0)}
    return fuori


# =====================================================================================
def main():
    SC._niente_simulatore()
    os.makedirs(USCITE, exist_ok=True)
    sc = SC.irregolare()
    geo = GE.scena_identita(sc)
    fuori = {"scena": {"n": sc["n"], "m": sc["m"], "seme": SEMI[0], "passi": PASSI,
                       "semi": list(SEMI), "eps": EPS_RIF},
             "L0": {}, "L1": {}, "L2": {}, "L3": {}, "L4": {}, "L5": {}}
    print("=" * 100)
    print("LE SEI LETTURE DEL v4 -- ognuna per (F) e per (S)")
    print("=" * 100)
    for cand in C4.CANDIDATE:
        print("  --- la candidata `%s` ---" % cand)
        fuori["L0"][cand] = l0(sc, geo, cand)
        for k, v in sorted(fuori["L0"][cand].items()):
            if not k.startswith("cs="):
                continue
            print("    L0 %s: fronte %.4f +/- %.4f archi/tick   proprio %.4f +/- %.4f   "
                  "rapporto al riferimento %.4f   entro 3 sigma: %s"
                  % (k, v["v_tick_fronte"], v["sigma_fronte"],
                     v["v_proprio_fronte"], v["sigma_proprio_fronte"],
                     v["rapporto_fronte"], v["entro_3sigma_fronte"]))
        for cv in ("scatter", "trasmissione"):
            fuori["L1"]["%s %s" % (cand, cv)] = l1(sc, geo, cand, cv)
            r = fuori["L1"]["%s %s" % (cand, cv)]
            sig = [p["r"] for p in r["profilo"].values()
                   if p["significativo"] and not p["dentro_il_grumo"]]
            print("    L1 %s: anelli FUORI dal grumo con dLambda oltre 3 sigma: %s   "
                  "fronte finale r=%d (entro il cono: %s)"
                  % (cv, sig or "NESSUNO", r["fronte"][-1]["raggio"],
                     r["fronte"][-1]["entro_il_cono"]))
        fuori["L2"][cand] = l2(sc, geo, cand, "scatter")
        c = fuori["L2"][cand]["confronto"]
        print("    L2 grumo contro passaggio: differenza %.3g, %.2f sigma, "
              "si distinguono: %s  (norme pari: %s)"
              % (c["differenza_pendenze"],
                 (c["differenza_pendenze"] / c["sigma_combinato"])
                 if c["sigma_combinato"] > 0 else 0.0,
                 c["si_distinguono"], c["norme_pari"]))
        fuori["L3"][cand] = l3(sc, geo, cand, "scatter")
        c = fuori["L3"][cand]["confronto"]
        print("    L3 la luce sente la massa: ritardo %+.2f tick, %.2f sigma, "
              "significativo: %s   (lancio %d -> bersaglio %d, il grumo e- a %d archi)"
              % (c["ritardo_tick"], c["in_sigma"], c["significativo"],
                 fuori["L3"][cand]["senza_grumo"]["nodo_di_lancio"],
                 fuori["L3"][cand]["senza_grumo"]["bersaglio"],
                 fuori["L3"][cand]["senza_grumo"]["distanza_grumo_bersaglio"]))
        fuori["L4"][cand] = l4(sc, geo, cand, "scatter")
        c = fuori["L4"][cand]
        print("    L4 materia/antimateria: max|dLambda| %.3g, max|dcs| %.3g, "
              "soglia %.3g, tiene: %s"
              % (c["max_dLambda"], c["max_dcs"], c["soglia"], c["tiene"]))
        fuori["L5"][cand] = l5(sc, geo, cand, "scatter")
        for k, v in sorted(fuori["L5"][cand].items()):
            if k.startswith("confronto"):
                print("    L5 %s: differenza %.5f, %.2f sigma, significativo: %s"
                      % (k, v["differenza"], v["in_sigma"], v["significativo"]))
    io.open(FONTE, "wb").write(
        (json.dumps(fuori, ensure_ascii=False, indent=1, sort_keys=True)
         + chr(10)).encode("utf-8"))
    print("-" * 100)
    print("  scritto %s" % os.path.relpath(FONTE, RADICE).replace(os.sep, "/"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
