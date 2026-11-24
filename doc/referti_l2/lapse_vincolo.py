# -*- coding: utf-8 -*-
r"""**[M0528-N] IL LAPSE COME MOLTIPLICATORE: `N` DAL VINCOLO, NON DA CHI** *(il mandato di Luca [M0528] Parte 2; la carta `doc/CARTA_lapse_moltiplicatore.md`, sez. `1`, `3-bis`, `4`; il task history `doc/TASK_HISTORY/2026-11-23_lapse_vincolo_codice.md`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo.py casi_noti > doc/referti_l2/lapse_vincolo_casi_noti.txt
    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo.py vuoto --riga V2               (TC.scena, il vuoto fresco, 500 tick)
    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo.py mattone --riga V2V3           (il k 0 di C2, la scena di chi_mattone, 2000 tick; riparte dall'ultimo stato)
    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo.py caduta --riga V3 --scala 0.8 [--senza]   (la scena di [M0908] / eotvos_v2, N = N_imp x N_ris; --senza: N_ris = 1)
    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo.py coppia --riga V2V3 --gradi 180 [--senza]  (d 36 dallo stampo, N_imp = 1: la sorgente vera)

**Il vincolo** *(la carta, sez. `3-bis`)*: `c2 L chi = kappa (N_imp N_ris u - <N_imp N_ris u>)`, `N_ris = e^{-kappa chi}`, `somma chi = 0`; `u = s Q(cs = s N) - e0 rho` *(`chi_tick.Q_di`, `rho_di`)* con le tre righe del libro: **V2** solo `s Q` *(il tick `cs = s N`)*, **V3** solo `-e0 rho` *(la fase (a) `+`)*, **V2V3** tutti e due *(Z1; il V1 di [M0908])*; **F0** nessun collegamento *(solo per la coppia senza lapse)*. `c2 = chi_tick.C_CHI^2`, `kappa = chi_parametri_v2.KAPPA` *(nel mattone: `chi_tick.parametri`, lo stesso numero)*. **Il solutore:** `c2 L` col nodo `0` a terra, fattorizzata UNA volta; il punto fisso dal `chi` del tick prima *(al primo tick da `0`)*, `max|chi' - chi|/max|chi'| < 1e-10`; **oltre `200` iterazioni si FERMA** *(K2)*.
**Il tick:** il vincolo risolto dallo stato a INIZIO tick, poi `caduta_segno_v2.tick_var` con `N_imp N_ris` *(non palindromo in `N`: dichiarato)*.
**Il mattone** usa `chi_mattone.corsa` *(da `k 0`)* e `chi_mattone_v2.corsa` *(la ripresa)* **con `chi_tick.tick_chi` sostituito IN MEMORIA** dal tick del vincolo: `X["chi"]` = il `chi` risolto, `X["pi"] = 0`; cosi' le serie `uN_<R>` di `chi_mattone` sono `1 - N_ris`, confrontabili con quelle di chi. **Il Pound-Rebka interno:** `omega` = `-arg` della somma di `conj(psi prima) psi dopo` sul centro *(`r < 5` dal nodo di `rho` massimo al primo tick)* e sul bordo *(`5 <= r < 10`)*, per tick.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT  # noqa: E402
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import chi_parametri_v2 as CP2  # noqa: E402
import massa_calcio as MC  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0528")
RIGHE = {"V2": (True, 0, True, False), "V3": (False, +1, False, True), "V2V3": (True, +1, True, True), "F0": (False, 0, False, False)}   # ### (cs = s N, il segno della fase (a), s Q in u, -e0 rho in u)
TOL, MAXIT, K2 = 1e-10, 200, 20
C2 = CT.C_CHI ** 2
KAPPA = CP2.KAPPA
K_VUOTO, K_MATTONE, K_CADUTA, K_COPPIA, D_COPPIA = 500, 2000, 2000, 2000, 36
R_CENTRO, R_BORDO = 5.0, 10.0
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    for m in ("chi_tick.py", "caduta_libera.py", "caduta_segno_v2.py", "massa_calcio.py", "triangolo_chi_v4.py", "eotvos_v2.py", "chi_mattone.py", "chi_mattone_v2.py", "gravita_fase.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


class Solutore(object):
    """### `chi` da `c2 L chi = f` *(`m2 = 0`: il nodo `0` a terra, `f` a media nulla, poi `chi - <chi>`)* o da `(c2 L + m2) chi = f` *(`m2 > 0`: per CN1)*; la fattorizzazione UNA volta."""

    def __init__(self, mot, c2, m2=0.0):
        import scipy.sparse as sp
        import scipy.sparse.linalg as spl
        self.Lp = CT.Laplaciano(mot)
        self.n, self.c2, self.m2 = self.Lp.n, float(c2), float(m2)
        if self.m2 > 0.0:
            self._f = spl.factorized((self.c2 * self.Lp.L + self.m2 * sp.identity(self.n, format="csr")).tocsc())
        else:
            self._f = spl.factorized((self.c2 * self.Lp.L)[1:, 1:].tocsc())

    def risolvi(self, f):
        f = np.asarray(f, dtype=float)
        if self.m2 > 0.0:
            return self._f(f)
        x = np.zeros(self.n)
        x[1:] = self._f(f[1:])
        return x - x.mean()

    def residuo(self, chi, f):
        r = self.c2 * (self.Lp.L @ chi) + self.m2 * chi - f
        return float(np.max(np.abs(r)) / max(np.max(np.abs(f)), 1e-300))


def u_di(z, riga, s, e0, N):
    """### `u = s Q(cs = s N) - e0 rho` secondo la riga *(le righe di `chi_tick.u_di` e `forza`)*."""
    mot, st, par = z["mot"], z["st"], z["par"]
    _cs, _sg, conQ, conR = RIGHE[riga]
    u = np.zeros(mot.inc.n)
    if conQ:
        u = u + float(s) * CT.Q_di(mot, st, par, float(s) * N)
    if conR:
        u = u - float(e0) * CT.rho_di(mot, st)
    return u


def sorgente(z, riga, s, e0, N_imp, chi, kappa):
    """### `f = kappa N_imp N_ris u(N) - <...>`."""
    N = N_imp * np.exp(-kappa * chi)
    f = kappa * N * u_di(z, riga, s, e0, N)
    return f - f.mean()


def vincolo(z, riga, N_imp, chi0, sol, kappa, s, e0):
    """### il punto fisso: `(chi, iterazioni, d)`; ### oltre `MAXIT` solleva *(K2: FERMO)*."""
    chi = np.zeros(sol.n) if chi0 is None else np.array(chi0, dtype=float)
    d = math.inf
    for it in range(1, MAXIT + 1):
        nuovo = sol.risolvi(sorgente(z, riga, s, e0, N_imp, chi, kappa))
        m = float(np.max(np.abs(nuovo)))
        d = float(np.max(np.abs(nuovo - chi))) / m if m > 0.0 else float(np.max(np.abs(nuovo - chi)))
        chi = nuovo
        if d < TOL:
            return chi, it, d
    raise RuntimeError("### K2 FALLISCE: il punto fisso NON converge in %d iterazioni (d %.3e): FERMO" % (MAXIT, d))


def tick(z, campo, riga, acceso, N_imp, X, sol, kappa, s, e0, freddo):
    """### UN tick: il vincolo dallo stato a inizio tick *(se acceso)*, poi `tick_var` con `N_imp N_ris`. Restituisce le iterazioni *(0 se spento)*."""
    cs_N, segno = RIGHE[riga][:2]
    it = 0
    if acceso:
        chi, it, _d = vincolo(z, riga, N_imp, None if freddo else X["chi"], sol, kappa, s, e0)
        X["chi"] = chi
        N = N_imp * np.exp(-kappa * chi)
    else:
        N = N_imp
    CS.tick_var(z, campo, s, e0, N, cs_N, segno)
    return it


def _fatti(d):
    if not os.path.isdir(d):
        return []
    return sorted(int(f[6:12]) for f in os.listdir(d) if f.startswith("stato_") and f.endswith(".npz") and len(f) == 16 and os.path.exists(os.path.join(d, f + ".sha1")))


def _salva(d, k, Z, C, meta, extra, serie):
    fz = os.path.join(d, "stato_%06d.npz" % k)
    dati = {x: Z["st"][x] for x in Z["chiavi"]}
    dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **extra)
    np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
    open(fz + ".sha1", "w", encoding="utf-8").write(CL.sha1(fz) + "\n")
    fs = os.path.join(d, "serie_%06d.json" % k)
    open(fs, "w", encoding="utf-8").write(json.dumps(serie))
    open(fs + ".sha1", "w", encoding="utf-8").write(CL.sha1(fs) + "\n")


def _riprendi(d, k0, Z, C):
    import gravita_due_corpi_misure as GM
    import _u1_prototipo as U1
    X_, _m = GM.leggi(os.path.join(d, "stato_%06d.npz" % k0))
    Z["metti"]({x: X_[x] for x in Z["chiavi"]})
    C.campo.A[...] = X_["campo_A"]
    C.campo.E[...] = X_["campo_E"]
    U1.scrivi_U(Z["mot"], C.campo)
    serie = json.load(open(os.path.join(d, "serie_%06d.json" % k0), encoding="utf-8"))
    return X_, serie


def caduta(riga, scala, acceso, k_fino=K_CADUTA, d_out=None):
    """### la scena di `eotvos_v2.caduta` riga per riga *(il gradiente IMPOSTO di [M0908])*, con `N = N_imp x N_ris`."""
    avvia()
    G20, _ia, e0, MT = CL.parametri()
    d_out = d_out or os.path.join(BASE, "caduta_%s_x%.1f_%s" % (riga, scala, "vincolo" if acceso else "senza"))
    os.makedirs(d_out, exist_ok=True)
    fatti = _fatti(d_out)
    t1 = time.time()
    with TC.scena() as Z:
        L, n = Z["L"], Z["n"]
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        C, info, _dxy = MC.scena_calciata(Z, 0.0, 1, scala)
        s = float(Z["s"])
        chi_imp, N_imp = CL.campo_N(Z, info, A, 1.0)
        cs_N, segno = RIGHE[riga][:2]
        meta = dict(info, variante=riga, scala=scala, cs_N=cs_N, segno_fase=segno, segno_chi=1.0, acceso=True, A=A, G20=G20, L_y=Ly, kappa=CP2.KAPPA, s=s, e0=e0,
                    vincolo=bool(acceso), c2=C2, kappa_vincolo=KAPPA)
        sol = Solutore(Z["mot"], C2) if acceso else None
        X = {"chi": np.zeros(n)}
        serie = {"it": [], "s_tick": []}
        k0 = 0
        if fatti:
            k0 = fatti[-1]
            X_, serie = _riprendi(d_out, k0, Z, C)
            X["chi"] = X_["chi_ris"].copy()
            print("### LA RIPRESA P8: dallo stato a k %d" % k0)
        print("### la caduta %s x %g, il vincolo %s: A %.6e; kappa %r, c2 %r; l'impronta %s" % (riga, scala, "ACCESO" if acceso else "SPENTO", A, KAPPA, C2, CL.impronta(Z, C)[:12]))

        def salva(k):
            _salva(d_out, k, Z, C, meta, {"chi": chi_imp, "N": N_imp, "chi_ris": X["chi"]}, serie)
        if not fatti:
            salva(0)
        for k in range(k0 + 1, k_fino + 1):
            ta = time.time()
            serie["it"].append(tick(Z["z"], C.campo, riga, acceso, N_imp, X, sol, KAPPA, s, e0, k == 1))
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            serie["s_tick"].append(time.time() - ta)
            if k % 250 == 0:
                salva(k)
                Nr = np.exp(-KAPPA * X["chi"])
                print("    [stato] k %d: le iterazioni max %d; N_ris min %.6e max %.6e; %.2f s/tick (%.0f s)" % (k, max(serie["it"]), Nr.min(), Nr.max(), float(np.mean(serie["s_tick"][-250:])), time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    return 0


def vuoto(riga, k_fino=K_VUOTO):
    """### `TC.scena`, il vuoto fresco *(le righe di `caduta_libera.prepara` senza il francobollo)*, `N_imp = 1`, il vincolo acceso."""
    avvia()
    _G20, _ia, e0, MT = CL.parametri()
    d_out = os.path.join(BASE, "vuoto_%s" % riga)
    os.makedirs(d_out, exist_ok=True)
    fatti = _fatti(d_out)
    t1 = time.time()
    with TC.scena() as Z:
        MT_, _MTR, _T1, _TRU, _TV, PO = TC.moduli()
        rho_c, e, t0 = MT_.rho_c_assoluto(), MT_.PB.E_DECISO, MT_.G2.T0
        n = Z["n"]
        Z["g_e"] = np.zeros_like(Z["g_e"])
        MT_.vuoto_fresco(Z, t0)
        C = PO.campi(Z, rho_c, e)
        s = float(Z["s"])
        u0 = u_di(Z["z"], riga, s, e0, np.ones(n))
        meta = {"variante": riga, "kappa": KAPPA, "c2": C2, "s": s, "e0": e0, "max_psi": float(np.max(np.abs(Z["st"]["psi_h"]))), "u_min": float(u0.min()), "u_max": float(u0.max())}
        print("### il vuoto %s: max |psi_h| %.3e; u a k 0 da %.17e a %.17e (lo scarto %.3e); l'impronta %s" % (riga, meta["max_psi"], u0.min(), u0.max(), u0.max() - u0.min(), CL.impronta(Z, C)[:12]))
        sol = Solutore(Z["mot"], C2)
        X = {"chi": np.zeros(n)}
        serie = {"it": [], "max_N_1": [], "s_tick": []}
        k0 = 0
        if fatti:
            k0 = fatti[-1]
            X_, serie = _riprendi(d_out, k0, Z, C)
            X["chi"] = X_["chi_ris"].copy()
            print("### LA RIPRESA P8: dallo stato a k %d" % k0)
        uno = np.ones(n)

        def salva(k):
            _salva(d_out, k, Z, C, meta, {"chi_ris": X["chi"]}, serie)
        if not fatti:
            salva(0)
        for k in range(k0 + 1, k_fino + 1):
            ta = time.time()
            serie["it"].append(tick(Z["z"], C.campo, riga, True, uno, X, sol, KAPPA, s, e0, k == 1))
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            serie["max_N_1"].append(float(np.max(np.abs(np.exp(-KAPPA * X["chi"]) - 1.0))))
            serie["s_tick"].append(time.time() - ta)
            if k % 250 == 0:
                salva(k)
                print("    [stato] k %d: max|N - 1| %.3e (su tutta la corsa %.3e); le iterazioni max %d; %.2f s/tick (%.0f s)" % (k, serie["max_N_1"][-1], max(serie["max_N_1"]), max(serie["it"]), float(np.mean(serie["s_tick"][-250:])), time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    return 0


def mattone(riga):
    """### `chi_mattone.corsa` *(da `k 0`)* o `chi_mattone_v2.corsa` *(dall'ultimo stato)* con `chi_tick.tick_chi` sostituito IN MEMORIA dal tick del vincolo."""
    import chi_mattone as CM
    import chi_mattone_v2 as CMV2
    from solitone import toro as TO
    avvia()
    d_out = os.path.join(BASE, "mattone_%s" % riga)
    os.makedirs(d_out, exist_ok=True)
    fatti = sorted(int(f[6:11]) for f in os.listdir(d_out) if f.startswith("stato_") and f.endswith(".npz") and len(f) == 15 and os.path.exists(os.path.join(d_out, f + ".sha1")))
    k_da = fatti[-1] if fatti else 0
    S = {"k": k_da, "sol": None, "it": [], "om_c": [], "om_b": [], "s_tick": [], "centro": None}
    if k_da:
        with np.load(os.path.join(d_out, "extra_%05d.npz" % k_da)) as d:
            for q in ("it", "om_c", "om_b", "s_tick"):
                S[q] = list(d[q])
            S["centro"] = [int(x) for x in d["centro"]]
        assert len(S["it"]) == k_da
    cs_N, segno = RIGHE[riga][:2]

    def tick_vincolo(z, campo, P, Lp, X):
        mot, st = z["mot"], z["st"]
        n = mot.inc.n
        nodo = np.asarray(mot.inc.nodo)
        if S["sol"] is None:
            S["sol"] = Solutore(mot, P.c2)
            Lq = int(round(math.sqrt(n)))
            assert Lq * Lq == n
            v = np.arange(n)
            if S["centro"] is None:
                S["centro"] = [int(x) for x in divmod(int(np.argmax(CT.rho_di(mot, st))), Lq)]
            r = np.hypot(*TO.scarti(v // Lq, v % Lq, S["centro"][0], S["centro"][1], Lq).T[:2])
            S["dentro"], S["bordo"] = r < R_CENTRO, (r >= R_CENTRO) & (r < R_BORDO)
            print("### il tick del vincolo (%s): il centro (il nodo di rho massimo al primo tick) %s; i nodi del centro %d, del bordo %d" % (riga, S["centro"], int(S["dentro"].sum()), int(S["bordo"].sum())))
        ta = time.time()
        chi, it, _d = vincolo(z, riga, 1.0, None if S["k"] == 0 else X["chi"], S["sol"], P.kappa, P.s, P.e0)
        X["chi"][...] = chi
        X["pi"][...] = 0.0
        prima = st["psi_h"].copy()
        CS.tick_var(z, campo, P.s, P.e0, np.exp(-P.kappa * chi), cs_N, segno)
        q = np.sum(np.conj(prima) * st["psi_h"], axis=1)
        qr = np.bincount(nodo, weights=q.real, minlength=n)
        qi = np.bincount(nodo, weights=q.imag, minlength=n)
        S["om_c"].append(float(-np.angle(complex(qr[S["dentro"]].sum(), qi[S["dentro"]].sum()))))
        S["om_b"].append(float(-np.angle(complex(qr[S["bordo"]].sum(), qi[S["bordo"]].sum()))))
        S["it"].append(it)
        S["s_tick"].append(time.time() - ta)
        S["k"] += 1
        if S["k"] % 250 == 0:
            np.savez(os.path.join(d_out, "extra_%05d.npz" % S["k"]), **{q_: np.array(S[q_]) for q_ in ("it", "om_c", "om_b", "s_tick")}, centro=np.array(S["centro"]))
            print("    [vincolo] k %d: le iterazioni max %d; N_ris centro %.6e, min %.6e, max %.6e; omega centro %.6f bordo %.6f (gli ultimi 250); %.2f s/tick" % (
                S["k"], max(S["it"]), float(np.exp(-P.kappa * chi[np.argmax(CT.rho_di(mot, st))])), float(np.exp(-P.kappa * chi.max())), float(np.exp(-P.kappa * chi.min())),
                float(np.mean(S["om_c"][-250:])), float(np.mean(S["om_b"][-250:])), float(np.mean(S["s_tick"][-250:]))))
            sys.stdout.flush()
    CT.tick_chi = tick_vincolo
    CM.DIR = d_out
    print("### IL MATTONE COL LAPSE DAL VINCOLO, la riga %s: chi_tick.tick_chi SOSTITUITO IN MEMORIA; %s" % (riga, ("da k 0 (chi_mattone.corsa)" if not k_da else "LA RIPRESA P8 da k %d (chi_mattone_v2.corsa)" % k_da)))
    if not k_da:
        return CM.corsa(K_MATTONE, None)
    CMV2.corsa(k_da, K_MATTONE, None, d_out, d_in=d_out)
    return 0


def coppia(riga, gradi, acceso, k_fino=K_COPPIA, d_out=None):
    """### `fh_coppia36.corsa` riga per riga *(`gravita_fase.prepara` a `d 36`, il nucleo e la forma S1)*, `N_imp = 1`, col vincolo della riga."""
    import gravita_fase as GF
    import gravita_due_corpi_d as GDD
    import ripresa_F0_v2 as RF
    import torneo_tenuta as TT
    from solitone import toro as TO
    avvia()
    _G20, _ia, e0, MT = CL.parametri()
    MV, P0 = TT.nucleo()
    GF.D = D_COPPIA
    GDD.avvia()
    d_out = d_out or os.path.join(BASE, "coppia_%s_%d_%s" % (riga, gradi, "vincolo" if acceso else "senza"))
    os.makedirs(d_out, exist_ok=True)
    fatti = _fatti(d_out)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        C, info = GF.prepara(Z, gradi)
        V = np.asarray(info["centri"], float)
        M = 0.5 * (V[0] + V[1])
        A1 = np.asarray(TO.vettori()[0], float)[:2]
        dxy = TO.scarti(Z["m1"], Z["m2"], M[0], M[1], L)[:, :2]
        lato = dxy @ (A1 / np.hypot(*A1))
        s = float(Z["s"])
        sol = Solutore(mot, C2) if acceso else None
        X = {"chi": np.zeros(n)}
        serie = {"D": [], "it": [], "s_tick": [], "info": {k: info[k] for k in ("centri", "distanza", "fasi_gradi")}}
        meta = dict(serie["info"], variante=riga, vincolo=bool(acceso), kappa=KAPPA, c2=C2, s=s, e0=e0)
        k0 = 0
        if fatti:
            k0 = fatti[-1]
            X_, serie = _riprendi(d_out, k0, Z, C)
            X["chi"] = X_["chi_ris"].copy()
            print("### LA RIPRESA P8: dallo stato a k %d" % k0)
        print("### la coppia %s, %d gradi, il vincolo %s: d %d (la distanza dei vertici %.4f), le fasi %s; l'impronta %s" % (riga, gradi, "ACCESO" if acceso else "SPENTO", GF.D, info["distanza"], info["fasi_gradi"], CL.impronta(Z, C)[:12]))

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = [(dxy[s_] * rho[s_][:, None]).sum(axis=0) / rho[s_].sum() for s_ in (lato < 0.0, lato >= 0.0)]
            serie["D"].append((kk, float(np.hypot(*(b[1] - b[0]))), float(rho.sum())))

        def salva(k):
            _salva(d_out, k, Z, C, meta, {"chi_ris": X["chi"]}, serie)
        if not fatti:
            misura(0)
            salva(0)
        uno = np.ones(n)
        with RF.col_nucleo(MV, P0), MV.forma_esplicita("S1"):
            assert MV.ATTIVA == "S1" and MV.pezzi is P0
            for k in range(k0 + 1, k_fino + 1):
                ta = time.time()
                serie["it"].append(tick(Z["z"], C.campo, riga, acceso, uno, X, sol, KAPPA, s, e0, k == 1))
                if k % MT.OGNI_GAUSS == 0:
                    C.residuo()
                if k % MC.OGNI == 0:
                    misura(k)
                serie["s_tick"].append(time.time() - ta)
                if k % 250 == 0:
                    salva(k)
                    print("    k %d: D %.4f; le iterazioni max %d; %.2f s/tick (%.0f s)" % (k, serie["D"][-1][1], max(serie["it"]), float(np.mean(serie["s_tick"][-250:])), time.time() - t1))
                    sys.stdout.flush()
        Z["metti"]()
    return 0


def casi_noti():
    """### CN1, CN1b *(il solutore sul `k 0` di C2)*, CN2 e il suo DEVE FALLIRE *(Eotvos V2 x0.8, il vincolo spento)*, CN3 *(la coppia F0 in fase, il vincolo spento)*."""
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    import gravita_due_corpi_misure as GM
    avvia()
    t00 = time.time()
    print("=" * 140)
    print("[M0528-N] I CASI NOTI DEL LAPSE COME MOLTIPLICATORE (la carta sez. 4): kappa %r, c2 %r; TOL %.0e, MAXIT %d, K2 %d" % (KAPPA, C2, TOL, MAXIT, K2))
    print("=" * 140)
    MT, CV = PS.MT, PS.CV
    PS.presidi()
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot, n = Z["mot"], Z["mot"].inc.n
        s = float(Z["s"])
        Lp = CT.Laplaciano(mot)
        C0 = PS.PO.campi(Z, rho_c, e)
        e0 = float(C0.e0)
        P, m0, _a, _c = CT.parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, "C2")
        CSB.prepara(Z, 186, False, rho_c, e, t0)
        print("### CN1: il k 0 di C2 (L 186); i parametri di chi %r; m0 %+.12e" % (P, m0))
        esito("CN1: il kappa di chi_tick.parametri = chi_parametri_v2.KAPPA AL BIT", P.kappa == KAPPA, "%r" % P.kappa)
        uno = np.ones(n)
        esito("CN1: u della riga V2V3 a N = 1 = chi_tick.u_di AL BIT", np.array_equal(u_di(Z["z"], "V2V3", s, e0, uno), CT.u_di(mot, Z["st"], Z["par"], s, e0)))
        ref = CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0)
        mio = P.kappa * Solutore(mot, P.c2, P.m2).risolvi(u_di(Z["z"], "V2V3", s, e0, uno) - m0)
        rel = float(np.max(np.abs(mio - ref)) / np.max(np.abs(ref)))
        esito("CN1: il solutore con m2 e c0 di chi e N = 1 ridà chi_tick.chi_statico entro 1e-12 relativo", rel < 1e-12, "%.3e" % rel)
        sol = Solutore(mot, P.c2)
        c = int(np.argmax(CT.rho_di(mot, Z["st"])))
        for riga in ("V2V3", "V2", "V3"):
            ta = time.time()
            chi, it, d = vincolo(Z["z"], riga, 1.0, None, sol, P.kappa, s, e0)
            f = sorgente(Z["z"], riga, s, e0, 1.0, chi, P.kappa)
            res = sol.residuo(chi, f)
            N = np.exp(-P.kappa * chi)
            print("    CN1b %s da freddo: %d iterazioni (d %.2e) in %.1f s; il residuo relativo %.2e; somma chi %.2e; N al nodo di rho massimo %.8f, N min %.8f, N max %.8f; chi di chi (m2) al centro: N %.8f" % (
                riga, it, d, time.time() - ta, res, float(chi.sum()), float(N[c]), float(N.min()), float(N.max()), float(np.exp(-P.kappa * ref[c]))))
            esito("CN1b %s: il punto fisso da freddo converge in < %d iterazioni e il residuo < 1e-10" % (riga, K2), it < K2 and res < 1e-10, "%d, %.2e" % (it, res))
        Z["metti"]()
    print("-" * 140)
    ref_d = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1446", "eotvos", "x0.8", "caduta_V2")
    dcn = os.path.join(BASE, "casi_noti")

    def uguali(f1, f2):
        X1, _m1 = GM.leggi(f1)
        X2, _m2 = GM.leggi(f2)
        chiavi = [k for k in X2 if k in X1 and k not in ("meta",)]
        diverse = [k for k in chiavi if not np.array_equal(np.asarray(X1[k]), np.asarray(X2[k]))]
        return diverse, chiavi
    for sc, k_cmp, deve in ((0.8, (0, 250), True), (float(np.nextafter(0.8, 1.0)), (0,), False)):
        d = os.path.join(dcn, "CN2_V2_x%r" % sc)
        if os.path.isdir(d):
            for f in os.listdir(d):
                os.remove(os.path.join(d, f))
        caduta("V2", sc, False, max(k_cmp), d)
        for k in k_cmp:
            diverse, chiavi = uguali(os.path.join(d, "stato_%06d.npz" % k), os.path.join(ref_d, "stato_%06d.npz" % k))
            nome = "CN2: il vincolo SPENTO, V2 x %r, lo stato k %d contro [M1446] %s" % (sc, k, "AL BIT" if deve else "(DEVE FALLIRE: diverso)")
            esito(nome, (not diverse) if deve else bool(diverse), "le chiavi confrontate %s; diverse %s" % (chiavi, diverse))
    print("-" * 140)
    d = os.path.join(dcn, "CN3_coppia_F0_0")
    if os.path.isdir(d):
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))
    coppia("F0", 0, False, 250, d)
    mio = json.load(open(os.path.join(d, "serie_000250.json"), encoding="utf-8"))["D"]
    rif = json.load(open(os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0326", "coppia_F0_stampo_d36", "serie.json"), encoding="utf-8"))["D"]
    rif = [x for x in rif if x[0] <= 250]
    esito("CN3: la coppia F0 in fase, il vincolo spento: D(k) e la norma fino a k 250 contro [M0326-K] AL BIT", [tuple(x) for x in mio] == [tuple(x) for x in rif], "%d punti; l'ultimo %s contro %s" % (len(mio), mio[-1], rif[-1]))
    print("=" * 140)
    print("### %d DEVE, %d PASSANO; %.0f s" % (len(ESITI), sum(ESITI), time.time() - t00))
    return 0 if all(ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("casi_noti")
    for nome in ("vuoto", "mattone"):
        p = sub.add_parser(nome)
        p.add_argument("--riga", choices=("V2", "V3", "V2V3"), required=True)
    p = sub.add_parser("caduta")
    p.add_argument("--riga", choices=("V2", "V3", "V2V3"), required=True)
    p.add_argument("--scala", type=float, required=True)
    p.add_argument("--senza", action="store_true")
    p = sub.add_parser("coppia")
    p.add_argument("--riga", choices=("V2V3", "F0"), required=True)
    p.add_argument("--gradi", type=int, choices=(0, 180), required=True)
    p.add_argument("--senza", action="store_true")
    x = ap.parse_args(argv)
    if x.cmd == "casi_noti":
        return casi_noti()
    if x.cmd == "vuoto":
        return vuoto(x.riga)
    if x.cmd == "mattone":
        return mattone(x.riga)
    if x.cmd == "caduta":
        return caduta(x.riga, x.scala, not x.senza)
    assert not (x.riga == "F0" and not x.senza), "F0 non ha vincolo: --senza"
    return coppia(x.riga, x.gradi, not x.senza)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
