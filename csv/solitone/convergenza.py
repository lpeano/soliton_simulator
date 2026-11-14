# -*- coding: utf-8 -*-
r"""**LA CONVERGENZA: QUANTO CONTA LA SCATOLA** *(Luca `2026-11-14` `15:20`, C1-C8; `15:22`, i posti; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `19`)*.

    python csv/solitone/convergenza.py deve81 > <scratchpad>/conv_deve81.txt                                         (il DEVE su L 81, (MU))
    python csv/solitone/convergenza.py corsa --mondo U|GU --L 162|243 [--bordo28] --registro conv-<mondo>-L<L>[b28] > <scratchpad>/conv_<mondo>_L<L>[b28].txt
    python csv/solitone/convergenza.py referto > doc/referti_l2/mattone/convergenza.txt

### **`corsa`:** **il mattone cotto su `L 81`** *((MU): `MU_05000`; (MGU): `MGU_10000`)* **incollato su `L 162`** *(la scena di S162)* **o su `L 243`** *(la scena COSTRUITA qui, `scena_L`: la sez. `19`)*,
**al vertice A del triangolo** *(lo stesso posto di (T-solo): `mattone_triangolo.posti`)*, **sul vuoto fresco al tick `60000`; il campo rifatto con Gauss** *(`A = 0`, `U` dal campo = `I`)*; **`2000` tick col
tick di `mattone_cottura.Corsa`** *((MU): il mondo SOLO U; (MGU): G+U)*. **Le misure** *(C4)*: **il picco a ogni tick; ogni `50` il picco, il raggio, la massa, il centro; S5'; la massa uscita dal bordo; il
picco subito dopo l'incollatura.** **La serie su `E:/soliton_simulator/mattone/lavoro`** *(fuori dal repo; copiata a corsa chiusa)*.
### **`--bordo28`** *(Luca `15:40`)*: **(MU) su `L 162` col bordo CENTRATO SUL MATTONE e `R_A = 28`** *(`bordo.g_estremita`, come la scena di S162; la rampa fino alla meta' del periodo del toro, `81`, contro `40.5` su `L 81`: dichiarato)*: **separa il bordo dalle copie.**
### **DEVE:** **(`deve81`) su `L 81`, (MU) dallo stato `MU_05000` caricato com'e': `50` tick col ciclo di questo file = `50` tick di `mattone_cottura.Corsa` AL BIT** *(esclusa `h_int`)*; **Gauss sotto `1e-10` a
ogni controllo; (`L 243`) il vuoto fresco: `|phi_j|^2 = 1` fuori dal bordo entro `1e-12`, e lo stesso disegno di fase ogni `3` nodi entro `1e-12`.**
"""
import argparse
import contextlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402
import mattone_cottura_U as CU  # noqa: E402
import mattone_rhoc as MR  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

MONDI = {"U": ("MU", 5000), "GU": ("MGU", 10000)}     # ### C1, C2
RIF = "S162"                                         # ### la corsa di riferimento per K, il vuoto F3, g_max
R_A_28 = 28.0                                        # ### Luca 15:40: (MU) su L 162 col bordo a 28 nodi dal centro del mattone (come TBS su L 81: bordo.R_A)
R_A_162 = 60.0                                       # ### Luca 15:49 (n.161): su L 162 il bordo da R_A 60, come (T-solo) (mio: la convergenza nella stessa scena di (T-solo))
R_A_243 = 121.5 - (81.0 - R_A_162)                   # ### MIO (sez. 19, 19.5): su L 243 la stessa fascia fra R_A e R_B che su L 162 (21): R_A = 100.5
N_TICK, OGNI, N_DEVE = 2000, 50, 50
TETTO_S = 28800.0                                    # ### Luca 15:22
TOLL_VUOTO = 1e-12
DIR_LAVORO = os.path.join(MT.DIR_E, "lavoro")
FIN_D = (250, 2000)                                  # ### C5: la deriva del picco sulla finestra 250-2000
ARRIVO = (1500, 2000)                                # ### C5: il picco medio di arrivo (mio: gli ultimi 500 tick)
CONVERGE, NON_CONVERGE = 0.3, 0.7                    # ### C5: le soglie del guardiano
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


# =====================================================================================
#   LA SCENA SU UN TORO DI LATO L (C3)
# =====================================================================================
@contextlib.contextmanager
def scena_L(L, R_A):
    """### **La scena di `mattone.scena` SENZA lo stato di una corsa** *(le stesse righe, nello stesso ordine)*: `V.scena` sotto `con_L(L)`, la forma, la partenza, `e_K`, gli autovettori, il vuoto F3 della
    corsa `RIF`; **lo stato della scena e' quello che `V.scena` costruisce** *(si sostituisce col vuoto fresco)*; **il bordo: centro `(L//2, L//2)`, `R_A` dato, `g_max` di `RIF`.**"""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    sol, vuoto, s = V.CORSE[CA.NOME]
    T_acc, _f = CA.CORSE[RIF]
    K = int(round(T_acc / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
        assert int(d["K"]) == K
    with CA.con_L(L), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, RIF)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot = z["st"], z["mot"]
        n = z["inc"].n
        assert z["L"] == L
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        cs0, lc0 = mot.cs, getattr(mot, "lambda_c", None)
        U0 = mot.geo.U.copy()
        stato = {k: st[k].copy() for k in chiavi}

        def metti(st_dato=None):
            for k in chiavi:
                st[k][...] = (st_dato or stato)[k]
            mot.cs, mot.lambda_c = cs0, lc0
            mot.geo.U[...] = U0
        metti()
        nodo = np.asarray(z["inc"].nodo)
        v_ = np.arange(n)
        bor = {"c0": [L // 2, L // 2], "R_A": R_A, "g_max": CA.BORDO[RIF]}
        g_e, gn, _r = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])
        Z = {"z": z, "st": st, "mot": mot, "par": z["par"], "n": n, "L": L, "nodo": nodo, "m1": v_ // L, "m2": v_ % L, "chiavi": chiavi, "stato": stato,
             "metti": metti, "phi_v": phi_v, "tab_c": tab_c, "omega": omega, "K": K, "s": s, "e_K": e_K, "g_e": g_e, "g_nodo": gn, "bordo": bor, "U0": U0,
             "righe": np.argsort(nodo, kind="stable").reshape(n, 6), "x_st": None}
        try:
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                yield Z
        finally:
            metti()


def controlla_vuoto(Z):
    """### **Il DEVE della scena di `L 243`** *(dopo `vuoto_fresco`)*: `max | |phi_j|^2 - 1 |` sui nodi fuori dal bordo *(`g = 0`)*; `max |phi(v + 3 a) - phi(v)|` lungo `A1` e `A2`."""
    L, n, righe = Z["L"], Z["n"], Z["righe"]
    st = Z["st"]
    p2 = np.zeros((n, 6))
    r6 = np.arange(6 * n)
    np.add.at(p2, (Z["nodo"], 2 * ((r6 // 2) % 3) + r6 % 2), np.abs(st["phi_h"]) ** 2)      # ### come p6_bracci.phi2_di
    dentro = Z["g_nodo"] == 0.0
    e1 = float(np.max(np.abs(p2[dentro] - 1.0)))
    m1, m2 = Z["m1"], Z["m2"]
    ph = st["phi_h"][righe]
    e3 = 0.0
    for d1, d2 in ((3, 0), (0, 3)):
        w = ((m1 + d1) % L) * L + (m2 + d2) % L
        e3 = max(e3, float(np.max(np.abs(ph[w] - ph))))
    return e1, e3, int(dentro.sum())


# =====================================================================================
#   IL CICLO (lo stesso per il DEVE su L 81 e per le corse)
# =====================================================================================
def gira(Z, C, k_da, n, t_di, e, S=None, nome_reg=None, gauss=None):
    """### **`n` tick col tick di `mattone_cottura.Corsa`**, il picco a ogni tick, le misure ogni `50` in `S`. `(Corsa, fermo)`."""
    R = CT.Corsa(Z, C)
    rho = MT.rho_di(Z)
    c = MT.centro_di(Z, rho)
    R.etichette([c])
    R.inizio(k_da)
    t1 = t_tappa = time.time()
    fermo = None

    def misura(k):
        rho = MT.rho_di(Z)
        c = MT.centro_di(Z, rho)
        if S is not None:
            S["pk_k"].append(k)
            S["picco"].append(float(rho.max()))
            S["resp"].append(MT.respiro(rho))
            if (k - k_da) % OGNI == 0:
                S["k"].append(k)
                S["rmax"].append(float(rho.max()))
                S["raggio"].append(MR.raggio(Z, rho, c))
                S["M"].append(float(rho.sum()))
                S["c1"].append(c[0])
                S["c2"].append(c[1])
        if (k - k_da) % CT.OGNI == 0:
            R.etichette([c])
    misura(k_da)
    for k in range(k_da + 1, k_da + n + 1):
        R.passo(k, t_di(k), 1.0, e)
        misura(k)
        if gauss is not None and (k - k_da) % MT.OGNI_GAUSS == 0:
            gauss.append(C.residuo())
        if S is not None and (k - k_da) % 250 == 0:
            print("    k %6d  il picco %.4e  il raggio %.4f  la massa %.10e  (%.0f s)" % (k, S["rmax"][-1], S["raggio"][-1], S["M"][-1], time.time() - t1))
            sys.stdout.flush()
        adesso = time.time()
        if nome_reg and adesso - t_tappa >= MT.TAPPA_S:
            MT.tappa(nome_reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / (k - k_da), MT.memoria_gb()))
            t_tappa = adesso
        if adesso - t1 > TETTO_S:
            fermo = "il tetto di %g s a k %d" % (TETTO_S, k)
            print("### FERMO: %s" % fermo)
            break
    return R, fermo


def deve81():
    import _presidio
    for m in ("mattone", "mattone_cottura", "mattone_cottura_U", "mattone_rhoc", "mattone_triangolo", "conti"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    caso, k0 = MONDI["U"]
    print("=" * 130)
    print("LA CONVERGENZA, IL DEVE SU L 81 (Luca 15:20): (MU) da %s_%05d caricato com'e' (U ricostruito), %d tick col ciclo di convergenza.py contro mattone_cottura.Corsa" % (caso, k0, N_DEVE))
    print("=" * 130)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        C, _f = CU.carica_U(Z, caso, rho_c, k0)
        R = CT.Corsa(Z, C)
        R.etichette([MT.centro_di(Z, MT.rho_di(Z))])
        R.inizio(k0)
        for k in range(k0 + 1, k0 + N_DEVE + 1):
            R.passo(k, MT.T_BASE + k, 1.0, e)
            if k % CT.OGNI == 0:
                R.etichette([MT.centro_di(Z, MT.rho_di(Z))])
        rif = {x: Z["st"][x].copy() for x in Z["chiavi"]}
        rif.update(campo_A=C.campo.A.copy(), campo_E=C.campo.E.copy())
        C, _f = CU.carica_U(Z, caso, rho_c, k0)
        S = {x: [] for x in ("pk_k", "picco", "resp", "k", "rmax", "raggio", "M", "c1", "c2")}
        gira(Z, C, k0, N_DEVE, lambda k: MT.T_BASE + k, e, S=S)
        mio = {x: Z["st"][x].copy() for x in Z["chiavi"]}
        mio.update(campo_A=C.campo.A.copy(), campo_E=C.campo.E.copy())
    div = [x for x in rif if x not in CU.CHIAVI_SERVIZIO and not np.array_equal(rif[x], mio[x])]
    esito("(MU) su L 81: %d tick col ciclo di convergenza.py = mattone_cottura.Corsa AL BIT (esclusa h_int)" % N_DEVE, not div, "diverse: %s" % div, True)
    print("ESITO: %d/%d; fallite %s" % (OK[0], OK[1], FALLITE))
    return 0 if not FALLITE else 1


def francobollo(caso, k):
    """### Il francobollo dello stato `<caso>_<k>` cotto su `L 81` *(come `mattone_triangolo.francobollo`)*."""
    f = os.path.join(MT.DIR_E, "%s_%05d.npz" % (caso, k))
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z81:
        with np.load(f) as d:
            Z81["metti"]({x: d[x] for x in Z81["chiavi"]})
        rho81 = MT.rho_di(Z81)
        c81 = MT.centro_di(Z81, rho81)
        st81 = {x: Z81["st"][x].copy() for x in Z81["chiavi"]}
        MT.vuoto_fresco(Z81, MT.T_BASE + k)
        phi_rif81 = Z81["st"]["phi_h"].copy()
        Z81["metti"](st81)
        fr = MT.ritaglia(Z81, c81, phi_rif81)
        fr["picco81"] = float(rho81.max())
        fr["file"] = f
    return fr


def corsa(mondo, L, nome_reg, bordo28=False):
    import _presidio
    import _u1_prototipo as U1
    import _vuoto_vivo_B as V
    for m in ("mattone", "mattone_cottura", "mattone_cottura_U", "mattone_rhoc", "mattone_triangolo", "conti"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    assert mondo in MONDI and L in (162, 243) and (not bordo28 or (L == 162 and mondo == "U"))
    tag = "L%d%s" % (L, "b28" if bordo28 else "")
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    caso, k0 = MONDI[mondo]
    fr = francobollo(caso, k0)
    t0 = MT.G2.T0
    print("=" * 130)
    print("LA CONVERGENZA (%s su L %d%s; Luca 15:20): il mattone %s (cotto su L 81, il picco %.4e) al vertice A, sul vuoto fresco al tick %d; %d tick; il tetto %g s" % (caso, L, ", IL BORDO A 28 (Luca 15:40)" if bordo28 else "", fr["file"], fr["picco81"], t0, N_TICK, TETTO_S))
    print("=" * 130)
    scena = MT.scena(MT.CORSA_162, MT.T_162) if L == 162 else scena_L(L, R_A_243)
    S = {x: [] for x in ("pk_k", "picco", "resp", "k", "rmax", "raggio", "M", "c1", "c2")}
    gauss = []
    with scena as Z:
        c0 = Z["bordo"]["c0"]
        cd = MTR.posti(c0, [fr], L)[0]
        print("### la scena: L %d, %d nodi; il bordo: il centro %s, R_A %.3f, g_max %g; il vertice A %s (a %.4f dal centro del bordo)"
              % (L, Z["n"], c0, Z["bordo"]["R_A"], Z["bordo"]["g_max"], cd, MT.distanza(L, cd, c0)))
        if L == 162 and not bordo28:
            from solitone import bordo as BO
            Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], R_A_162, Z["bordo"]["g_max"])[0]       # ### Luca 15:49: come (T-solo)
            print("### IL BORDO (Luca 15:49): R_A %g attorno al centro del bordo della scena (quello della scena %.3f)" % (R_A_162, Z["bordo"]["R_A"]))
        if bordo28:
            from solitone import bordo as BO
            from solitone import toro as TO
            Z["g_e"] = BO.g_estremita(Z["z"], cd[0], cd[1], R_A_28, Z["bordo"]["g_max"])[0]          # ### Luca 15:40: il bordo centrato sul mattone, R_A 28
            print("### IL BORDO A 28 (Luca 15:40): centrato sul mattone %s, R_A %g, R_B %g (la meta' del periodo), g_max %g" % (cd, R_A_28, TO.meta_periodo(L), Z["bordo"]["g_max"]))
        MT.vuoto_fresco(Z, t0)
        if L == 243:
            e1, e3, nd = controlla_vuoto(Z)
            esito("(L 243) il vuoto fresco: |phi_j|^2 = 1 fuori dal bordo (%d nodi) entro %g" % (nd, TOLL_VUOTO), e1 <= TOLL_VUOTO, "%.3e" % e1, True)
            esito("(L 243) il vuoto fresco: lo stesso disegno di fase ogni 3 nodi entro %g" % TOLL_VUOTO, e3 <= TOLL_VUOTO, "%.3e" % e3, True)
            if FALLITE:
                print("ESITO: ### FERMO (la scena di L 243): %d/%d; fallite %s" % (OK[0], OK[1], FALLITE))
                return 1
        D = MT.incolla(Z, fr, cd, True)
        C = MT.Campi(Z, caso, rho_c, e)
        rho = MT.rho_di(Z)
        C.campo.A[...] = 0.0
        C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
        C.campo.e = e
        C.e_prec = e
        U1.scrivi_U(Z["mot"], C.campo)
        assert np.array_equal(Z["mot"].geo.U, np.broadcast_to(np.eye(2, dtype=complex), Z["mot"].geo.U.shape)), "con A = 0 U NON e' I"
        gauss.append(C.residuo())
        print("### incollato a %s (Delta %.6f); il picco SUBITO DOPO l'incollatura %.4e (su L 81 %.4e); il residuo di Gauss iniziale %.3e" % (cd, D, float(rho.max()), fr["picco81"], gauss[0]))
        R, fermo = gira(Z, C, 0, N_TICK, lambda k: t0 + k, e, S=S, nome_reg=nome_reg, gauss=gauss)
        print("-" * 130)
        R.tabella(["sol"])
        T = {x: np.array(v) for x, v in R.T.items()}
        bordoM = np.array(T["Mp"] - T["Md"])
        f = os.path.join(MT.DIR_E, "conv_%s_%s_%05d.npz" % (mondo, tag, int(S["pk_k"][-1])))
        np.savez(f, meta=np.array(json.dumps({"mondo": mondo, "L": L, "k": int(S["pk_k"][-1]), "t": t0 + int(S["pk_k"][-1]), "sha": V.shas(Z["z"]), "codice": "csv/solitone/convergenza.py"})),
                 campo_A=C.campo.A, campo_E=C.campo.E, **{x: Z["st"][x] for x in Z["chiavi"]})
    kk = np.array(S["pk_k"])
    s5, ff = CT.s5p(kk, S["resp"], int(kk[-1]))
    print("### S5' (le ultime quattro finestre): %s -> %.4f" % (" ".join("%d-%d %.4f" % x for x in ff), s5))
    print("### la massa uscita dal bordo in tutto %.6e" % float(bordoM.sum()))
    esito("il residuo di Gauss sotto %g a ogni controllo" % MT.TOLL_GAUSS, max(gauss) < MT.TOLL_GAUSS, "il massimo %.3e" % max(gauss), True)
    os.makedirs(DIR_LAVORO, exist_ok=True)
    np.savez_compressed(os.path.join(DIR_LAVORO, "conv_%s_%s_serie.npz" % (mondo, tag)), bordoM=bordoM, s5=s5, **{x: np.array(v) for x, v in S.items()})
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, "FERMO " + fermo if fermo else "finita", time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   IL REFERTO (C5)
# =====================================================================================
def d_di(t, picco):
    """### `D1`: la deriva relativa del picco per `500` tick sulla finestra `FIN_D` *(la retta)*; `D2`: il picco medio di arrivo *(`ARRIVO`)*."""
    t, picco = np.asarray(t, dtype=float), np.asarray(picco, dtype=float)
    j = (t >= FIN_D[0]) & (t <= FIN_D[1])
    p = np.polyfit(t[j], picco[j], 1)
    a = (t >= ARRIVO[0]) & (t <= ARRIVO[1])
    return 500.0 * p[0] / float(np.mean(picco[j])), float(np.mean(picco[a])), int(t[-1])


def lettura(D):
    """### C5: `|D(243) - D(162)|` contro `|D(162) - D(81)|`."""
    a, b = abs(D[243] - D[162]), abs(D[162] - D[81])
    q = a / b if b else float("inf")
    return q, ("CONVERGE: L 162 E' ABBASTANZA GRANDE" if q < CONVERGE else ("NON CONVERGE: LA SCATOLA CONTA ANCORA" if q > NON_CONVERGE else "INDECISO"))


def referto():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA CONVERGENZA, IL REFERTO (Luca 15:20, C5): D1 la deriva relativa del picco per 500 tick (%d-%d), D2 il picco medio di arrivo (%d-%d); le soglie %g e %g" % (FIN_D + ARRIVO + (CONVERGE, NON_CONVERGE)))
    print("=" * 130)
    fonti = {("U", 81): ("lunga_MU_serie.npz", "lunga"), ("GU", 81): ("lunga_MGU_serie.npz", "lunga"), ("GU", 162): ("triangolo_solo_serie.npz", "solo"),
             ("U", 162): ("conv_U_L162_serie.npz", "conv"), ("U", 243): ("conv_U_L243_serie.npz", "conv"), ("GU", 243): ("conv_GU_L243_serie.npz", "conv")}
    for mondo in ("U", "GU"):
        D1, D2 = {}, {}
        print("-" * 130)
        for L in (81, 162, 243):
            nome, tipo = fonti[(mondo, L)]
            f = os.path.join(MT.DIR_REF if tipo == "solo" else DIR_LAVORO, nome)
            if not os.path.exists(f):
                print("    (%s) L %d: manca %s" % (mondo, L, f))
                continue
            s = np.load(f)
            if tipo == "lunga":
                t, p = np.array(s["k"], dtype=float) - s["k"][0], s["rmax"]
            elif tipo == "solo":
                t, p = np.arange(len(s["picco_A"]), dtype=float), s["picco_A"]
            else:
                t, p = np.array(s["pk_k"], dtype=float), s["picco"]
            jj = t <= N_TICK
            D1[L], D2[L], ult = d_di(t[jj], np.asarray(p)[jj])
            print("    (%s) L %3d (%s): D1 %+.5f per 500 tick; D2 %.4e; il picco al tick 0 %.4e; fino al tick %d" % (mondo, L, nome, D1[L], D2[L], float(np.asarray(p)[0]), ult))
        if mondo == "U":
            f = os.path.join(DIR_LAVORO, "conv_U_L162b28_serie.npz")
            if os.path.exists(f):
                s = np.load(f)
                t, p = np.array(s["pk_k"], dtype=float), s["picco"]
                b1, b2, ult = d_di(t, p)
                print("    (U) L 162 COL BORDO A 28 (Luca 15:40): D1 %+.5f; D2 %.4e; fino al tick %d" % (b1, b2, ult))
                if 81 in D1 and 162 in D1:
                    for nome, x, D in (("D1", b1, D1), ("D2", b2, D2)):
                        a, b = abs(x - D[81]), abs(x - D[162])
                        print("  (U) %s col bordo a 28: dista %.4g da L 81 e %.4g da L 162 normale -> %s" % (nome, a, b, "come L 81: IL COLPEVOLE E' IL BORDO" if a < b else "come L 162 normale: LE COPIE"))
            else:
                print("    (U) L 162 col bordo a 28: manca %s" % f)
        if len(D1) == 3:
            for nome, D in (("D1, la deriva", D1), ("D2, il picco di arrivo", D2)):
                q, lett = lettura(D)
                print("  (%s) %s: |D(243) - D(162)| / |D(162) - D(81)| = %.3f -> %s" % (mondo, nome, q, lett))
    print("=" * 130)
    return 0


def main(argv):
    if argv and argv[0] in ("deve81", "referto"):
        return deve81() if argv[0] == "deve81" else referto()
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("corsa",))
    ap.add_argument("--mondo", required=True, choices=sorted(MONDI))
    ap.add_argument("--L", type=int, required=True, choices=(162, 243))
    ap.add_argument("--bordo28", action="store_true")
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    return corsa(x.mondo, x.L, x.registro, x.bordo28)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
