# -*- coding: utf-8 -*-
r"""**LA MITOSI CON CHI: L'UNIONE** *(il ramo `mitosi-chi`; il mandato unico di Luca `2026-11-21` `19:40`, R1-R4; la carta `doc/TASK_HISTORY/2026-11-21_mitosi_chi.md`, sez. `2.2`-`2.3`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_chi.py p60 > doc/referti_l2/mitosi_chi_p60.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_chi.py nascite > doc/referti_l2/mitosi_chi_nascite.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_chi.py p8 > doc/referti_l2/mitosi_chi_p8.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_chi.py rami_prova > doc/referti_l2/mitosi_chi_rami_prova.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_chi.py ramo --nome MITOSICHI --da primo --dopo 20000 --registro <voce>
    E:\python\py3132\python.exe doc/referti_l2/mitosi_chi.py ramo --nome CHIEXT --da primo --dopo 20000 --registro <voce>

**Importa senza toccarli** *(sono IN USO nei rami della mitosi, o nella corsa del ramo `lapse-u`)*: `mitosi_rami`, `mitosi_lunga`, `mitosi_regola`, `mitosi_corsa`, `chi_tick`, `chi_mattone`, `chi_tronco`.
**Il campo `chi`** *(`Chi`)*: `X = {chi, pi, theta_a}`, i parametri *(`chi_tick.parametri`, asseriti al bit su quelli del `meta`)*, **il Laplaciano RICOSTRUITO dopo ogni crescita**, il contatore della mitosi **con `theta` = `X["theta_a"]`** *(lo stesso array: `tick_chi` accumula, `Contatore.accumula` NON si chiama)*.
**La regola** *(`regola_chi`)*: i candidati di `mitosi_regola.candidato` *(il grafo, `psi`, `phi`, i versori, il campo, il motore del candidato)*, **`H` = `chi_tick.energia_chi` sul motore del candidato** *(`chi`, `pi`: i vecchi, sul nodo `n` la media di `i` e `j`; il Laplaciano del candidato)*; la scelta (A) di `mitosi_regola.regola` riga per riga. **`applica_chi`:** `mitosi_regola.applica` con `mot.cs = None` per la durata *(NON calcola `cs` dalla legge `N(rho)`)*, poi `mot.cs` di prima con in coda `s exp(- kappa chi_n)`; `chi`, `pi` col nodo nuovo; il Laplaciano nuovo.
**La nascita** *(`NascitaChi.nasci`, le righe di `mitosi_rami.Rami.nasci` con `energia_chi`)*: `DH`, `E_persa -= H1 - H0`, P9 a ogni nascita *(oltre `1e-12`: FERMO)*, `gauss_acc`, il luogo, **`DH_chi`, `somma c0` prima e dopo.**
**Il ciclo** *(`ciclo`, le righe di `mitosi_rami.ciclo`)*: il passo di `chi_mattone_v2` col campo generico; i modi `mitosi` *(MITOSI-CHI)* e `ext` *(CHI-EXT)*; le misure del ramo `mitosi` piu' quelle di `chi`; finche' non ci sono nascite anche `R5` e `dphi_nodi` *(come la corsa con `chi`)*.
**Le prove** *(la carta sez. `2.3`)*: `p60`, `nascite` *(P1, P3, P9, i casi noti nel guscio e a `r 30`, K4 dopo la nascita, Q-P1)*, `p8`, `rami_prova` *(R4)*. **P5** sta in `mitosi_chi_specchio.py`.
"""
import datetime
import glob
import json
import math
import os
import shutil
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_rami as MRA  # noqa: E402
import chi_tick as CT  # noqa: E402
import chi_mattone as CM  # noqa: E402

ML = MRA.ML
MR, MC, PS = ML.MR, ML.MC, ML.PS
CSB = MC.CSB
BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_chi")
DIR_M = CM.DIR
CHIAVI_P = ("kappa", "c0", "c2", "m2", "e0", "s")
QUANTO = 2.0 * math.pi
OGNI, OGNI_STATO = 50, 250
GUARDIA = MR.GUARDIA


# ------------------------------------------------------------------------------------------ il campo chi
class Chi(object):
    def __init__(self, P, X, mot, cont):
        self.P, self.X, self.cont = P, X, cont
        self.X["theta_a"] = cont.theta
        self.Lp = CT.Laplaciano(mot)

    def controlla(self):
        assert self.X["theta_a"] is self.cont.theta, "Theta della corsa e il contatore NON sono lo stesso array"


def parametri_di(Z):
    MT = PS.MT
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    Lp0 = CT.Laplaciano(Z["mot"])
    s = float(Z["s"])
    C0 = PS.PO.campi(Z, rho_c, e)
    e0 = float(C0.e0)
    P, m0, _a, _c = CT.parametri(Z, PS, CSB, Lp0, rho_c, e, t0, s, e0, "C2")
    return P, m0


def controlla_parametri(P, m0, meta):
    pm = meta["parametri"]
    for q in CHIAVI_P:
        assert getattr(P, q) == pm[q], "il parametro %s ricalcolato %r contro %r nel meta: FERMO" % (q, getattr(P, q), pm[q])
    assert m0 == pm["m0"], "m0 ricalcolato %r contro %r nel meta: FERMO" % (m0, pm["m0"])


def energia(Z, C, K):
    """### `(H, H_chi)`: `chi_tick.energia_chi` sul motore vero."""
    return CT.energia_chi(Z["mot"], Z["st"], Z["par"], K.P, K.Lp, K.X, C.campo)


# ------------------------------------------------------------------------------------------ la regola con chi
def candidato_chi(Z, C, a, lato, regola, K, fattore=True):
    S = MR.candidato(Z, C, a, lato, regola, fattore)
    nd = S["nodi"]
    i, j = nd["i"], nd["j"]
    chi3 = np.append(K.X["chi"], 0.5 * (K.X["chi"][i] + K.X["chi"][j]))
    pi3 = np.append(K.X["pi"], 0.5 * (K.X["pi"][i] + K.X["pi"][j]))
    Lp3 = CT.Laplaciano(S["mot"])
    H3, Hc3 = CT.energia_chi(S["mot"], S["st"], Z["par"], K.P, Lp3, {"chi": chi3, "pi": pi3}, S["campo"])
    S["H_corsa_oggi"] = S["H"]
    S["H"], S["H_chi"], S["chi"], S["pi"] = H3, Hc3, chi3, pi3
    return S


def regola_chi(Z, C, a, K, giro="stella"):
    """### `mitosi_regola.regola` riga per riga, con `candidato_chi`."""
    nas = candidato_chi(Z, C, a, None, giro, K)
    nd = nas["nodi"]
    lati = ((nd["i"], nd["k"]), (nd["j"], nd["k"]), (nd["j"], nd["l"]), (nd["i"], nd["l"]))
    cand = [candidato_chi(Z, C, a, lt, giro, K) for lt in lati]
    Hs = np.array([c["H"] for c in cand])
    o = np.argsort(Hs, kind="stable")
    gap = float(Hs[o[1]] - Hs[o[0]])
    pari = gap < GUARDIA * abs(float(Hs[o[0]]))
    scelto = nas if pari else cand[int(o[0])]
    R = {"H": Hs.tolist(), "H_nascita": nas["H"], "H_chi_nascita": nas["H_chi"], "scelto": -1 if pari else int(o[0]), "gap": gap / abs(float(Hs[o[0]])), "lati": lati,
         "nodi": scelto["nodi"], "t": [nas["t"]] + [c["t"] for c in cand], "cand": [nas] + cand}
    return R, scelto


def applica_chi(Z, C, K, S):
    mot = Z["mot"]
    cs0 = mot.cs
    mot.cs = None
    inf = MR.applica(Z, C, K.cont, S)
    K.X["chi"] = np.array(S["chi"], dtype=float)
    K.X["pi"] = np.array(S["pi"], dtype=float)
    K.X["theta_a"] = K.cont.theta
    if cs0 is not None:
        mot.cs = np.append(np.asarray(cs0, dtype=float), K.P.s * math.exp(-K.P.kappa * float(S["chi"][-1])))
    K.Lp = CT.Laplaciano(mot)
    assert K.X["chi"].size == mot.inc.n and K.X["theta_a"].size == mot.inc.m, "chi o Theta NON seguono il grafo"
    return inf


class NascitaChi(ML.Nascite):
    def __init__(self, cont, e_persa, nascite, accese, gacc, centro, K):
        ML.Nascite.__init__(self, cont, e_persa, nascite, accese)
        self.gacc = np.array(gacc, dtype=float)
        self.centro = centro
        self.K = K

    def nasci(self, Z, C, a, k, perche):
        """### `mitosi_rami.Rami.nasci` riga per riga, con `energia_chi` e la regola con `chi`; in piu' `DH_chi`, `somma c0`."""
        K = self.K
        t1 = time.time()
        n0 = int(Z["mot"].inc.n)
        H0, Hc0 = energia(Z, C, K)
        R, S = regola_chi(Z, C, int(a), K)
        keep, mb = S["keep"], S["mb"]
        nuovi = len(S["ii"]) - mb
        Ec = S["campo"].E - np.concatenate([C.campo.E[keep], np.zeros(nuovi)])
        assert self.gacc.shape == (keep.size,), "gauss_acc non segue il grafo"
        inf = applica_chi(Z, C, K, S)
        self.gacc = np.concatenate([self.gacc[keep], np.zeros(nuovi)]) + Ec
        H1, Hc1 = energia(Z, C, K)
        d9 = abs(H1 - S["H"]) / abs(S["H"])
        self.e_persa -= (H1 - H0)
        self.nascite += 1
        nd = R["nodi"]
        n = nd["n"]
        ii, jj = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
        src = int(np.argmin(ML.raggi(Z, MRA.Rami.centro_materia(Z))))
        dn = int(ML.passi(ii, jj, Z["mot"].inc.n, src)[n])
        r_n = float(ML.raggi(Z, self.centro)[n])
        b = {"k": int(k), "a": int(a), "perche": perche, "nodi": {x: int(v) for x, v in nd.items()}, "scelto": int(R["scelto"]), "gap": float(R["gap"]),
             "DH_nascita": float(R["H_nascita"] - H0), "DH_flip": float(S["H"] - R["H_nascita"]) if R["scelto"] >= 0 else 0.0, "DH": float(H1 - H0), "P9": float(d9),
             "DH_chi": float(Hc1 - Hc0), "somma_c0": [K.P.c0 * float(n0), K.P.c0 * float(Z["mot"].inc.n)], "chi_n": float(K.X["chi"][n]),
             "res": float(S["res"]), "E_persa": self.e_persa, "t": time.time() - t1, "ok": bool(inf["ok_fuori"] and inf["ok_geo"] and inf["ok_U"]),
             "pos": [float(Z["m1"][-1]), float(Z["m2"][-1])], "r": r_n, "passi": dn, "Ec_norma": float(np.linalg.norm(Ec)), "Ec_max": float(np.max(np.abs(Ec)))}
        self.bilanci.append(b)
        print("    [nascita %d] k %d, l'arco %d (%s): n %d a r %.2f, %d passi dalla sorgente; DH nascita %+.4e flip %+.4e chi %+.4e; P9 %.1e; |Ec| %.3e; E_persa %+.6e (%.1f s)" % (
            self.nascite, k, a, perche, n, r_n, dn, b["DH_nascita"], b["DH_flip"], b["DH_chi"], d9, b["Ec_norma"], self.e_persa, b["t"]))
        sys.stdout.flush()
        assert b["ok"] and d9 <= 1e-12, "la nascita NON e' entrata nel motore come il candidato (P9 %.1e): FERMO" % d9
        return b


# ------------------------------------------------------------------------------------------ salva e riprendi
def salva(Z, C, NS, k, t, meta, f):
    """### `mitosi_rami.salva` riga per riga, piu' `chi`, `pi`."""
    mot = Z["mot"]
    NS.K.controlla()
    dati = {x: Z["st"][x] for x in Z["chiavi"]}
    dati.update(campo_A=C.campo.A, campo_E=C.campo.E, theta_a=NS.cont.theta, gauss_acc=NS.gacc, chi=NS.K.X["chi"], pi=NS.K.X["pi"])
    if NS.nascite:
        dati.update(ii=np.asarray(mot.inc.nodo[0::2]), jj=np.asarray(mot.inc.nodo[1::2]), geo_n=mot.geo.n, campo_vec=C.campo.vec,
                    m1=np.asarray(Z["m1"], dtype=float), m2=np.asarray(Z["m2"], dtype=float))
    meta = dict(meta, k=int(k), t=float(t), E_persa=NS.e_persa, nascite=NS.nascite, n=int(mot.inc.n))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    np.savez(f, meta=np.array(json.dumps(meta)), **dati)
    s = ML.sha1(f)
    with open(f + ".sha1", "w", encoding="utf-8") as fh:
        fh.write(s + "\n")
    return s


def apri(Z, f, accese, P, m0):
    """### `(C, NS, meta)`: dallo stato del tronco `chi` *(nessun grafo, nessun `E_persa`: `controllo_senza_bordo.riprendi` + il campo generico)* o da uno stato del ramo *(`mitosi_lunga.riprendi`)*; piu' `chi`, `pi`, `gauss_acc`."""
    import contatore as CO
    MT = PS.MT
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    with np.load(f) as d:
        meta0 = json.loads(str(d["meta"]))
        X = {q: d[q].copy() for q in ("chi", "pi")}
        g = d["gauss_acc"].copy() if "gauss_acc" in d.files else None
    if "E_persa" not in meta0:
        C, meta, cs, _s = CSB.riprendi(Z, f, False, rho_c, e)
        assert cs is None, "lo stato ha un cs_prec: non e' della corsa con chi"
        MC.campo_generico(Z, C)
        with np.load(f) as d:
            cont = CO.Contatore(d["theta_a"])
        e_persa, nascite = 0.0, 0
    else:
        C, NS0, meta, cs = ML.riprendi(Z, f, rho_c, e, accese)
        assert cs is None, "lo stato ha un cs_prec: non e' della corsa con chi"
        cont, e_persa, nascite = NS0.cont, NS0.e_persa, NS0.nascite
    controlla_parametri(P, m0, meta)
    K = Chi(P, X, Z["mot"], cont)
    NS = NascitaChi(cont, e_persa, nascite, accese, g if g is not None else np.zeros(Z["mot"].inc.m), meta["centro"], K)
    assert K.X["chi"].size == Z["mot"].inc.n and K.X["theta_a"].size == Z["mot"].inc.m and NS.gacc.size == Z["mot"].inc.m
    return C, NS, meta


def stato_di(Z, C, NS):
    out = ML.stato_di(Z, C, NS)
    out.update(gauss_acc=NS.gacc.copy(), chi=NS.K.X["chi"].copy(), pi=NS.K.X["pi"].copy())
    return out


def stati(d):
    out = []
    for f in sorted(glob.glob(os.path.join(d, "stato_*.npz"))):
        k = int(os.path.basename(f)[6:-4])
        ok = os.path.exists(f + ".sha1") and open(f + ".sha1", encoding="utf-8").read().split()[0] == ML.sha1(f)
        out.append((k, f, ok))
    return sorted(out)


def ultimo(d):
    """### lo stato integro piu' recente *(i nomi a `5` o `6` cifre)*."""
    for k, f, ok in reversed(stati(d)):
        if ok:
            return k, f
        print("### lo stato %s NON e' integro: si prende quello prima" % os.path.basename(f))
    return None


# ------------------------------------------------------------------------------------------ il ciclo
def ciclo(nome, modo, f, k_fino, reg, forza=None, nascita_iniziale=True, d_out=None, d_serie=None, tocca=None):
    """### `modo`: `mitosi` *(MITOSI-CHI)* o `ext` *(CHI-EXT)*. `(codice, k, stato_di)`. `d_serie`: dove sono le serie di `k_da` *(di default `d_out`)*; `tocca`: l'arco il cui `E` si sposta di un ulp alla ripresa *(SOLO nelle prove)*."""
    from solitone import _registro_corse as RC
    from solitone import toro as TO
    MT, CV, MRo, CTO = PS.MT, PS.CV, PS.MR, PS.CT
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    t00 = time.time()
    d_out = d_out or os.path.join(BASE, nome)
    d_serie = d_serie or d_out
    codice = 0
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        P, m0 = parametri_di(Z)
        C, NS, meta = apri(Z, f, modo == "mitosi", P, m0)
        K = NS.K
        if tocca is not None:
            C.campo.E[tocca] = np.nextafter(C.campo.E[tocca], np.inf)
        k_da = int(meta["k"])
        centro = meta["centro"]
        print("### %s (%s): da %s (k %d, sha1 %s), fino a k %d; le nascite %s; i parametri AL BIT col meta: %r" % (
            nome, modo, f, k_da, ML.sha1(f)[:8], k_fino, "ACCESE" if modo == "mitosi" else "SPENTE", P))
        sys.stdout.flush()
        L = Z["L"]
        v = np.arange(L * L)
        r0 = np.hypot(*TO.scarti((v // L).astype(float), (v % L).astype(float), centro[0], centro[1], L).T[:2])
        anelli = {R_: np.nonzero((r0 >= R_ - 0.5) & (r0 < R_ + 0.5))[0] for R_ in ML.ANELLI}
        sfx = os.path.basename(f)[6:-4] if os.path.basename(f).startswith("stato_") else None
        Xs, EX = {}, None
        if sfx is not None:
            fs, fx = os.path.join(d_serie, "serie_%s.npz" % sfx), os.path.join(d_serie, "serie_chi_%s.npz" % sfx)
            if os.path.exists(fs):
                with np.load(fs) as d:
                    Xs = {x: list(d[x]) for x in d.files}
            if os.path.exists(fx):
                with np.load(fx) as d:
                    EX = {x: list(d[x]) for x in d.files}
        if EX is None:
            EX = {x: [] for x in ("k", "picco", "H", "H_chi", "chi_medio", "max_theta") + tuple("uN_%d" % R for R in CM.ANELLI) + tuple("rit_%d" % R for R in CM.ANELLI)}
        Mi = ML.misure_su(Z, centro, {x: Xs[x] for x in Xs if not x.startswith("D_") and not x.startswith("G_")} or None)
        nomi_D = ("D_k", "D_med40", "D_med60", "D_r50", "D_r90", "D_w", "D_n", "D_epersa", "G_norma", "G_max_lontano", "G_max_40", "G_d_max")
        DS = {x: Xs.get(x, []) for x in nomi_D}
        fn = os.path.join(d_out, "nascite_%s.json" % sfx) if sfx else None
        if fn and os.path.exists(fn):
            with open(fn, encoding="utf-8") as fh:
                NS.bilanci = json.load(fh)
        geo = {}

        def rigeometria():
            r = ML.raggi(Z, centro)
            nodo = np.asarray(Z["mot"].inc.nodo)
            geo.update(r=r, nodo=nodo, ra=0.5 * (r[nodo[0::2]] + r[nodo[1::2]]), c0n=int(np.argmin(r)) if "c0n" not in geo else geo["c0n"])
        rigeometria()

        class CorsaChi(CTO.Corsa):
            def passo(self, k, t, r_, e_):
                C_, Z_ = self.C, self.Z
                if e_ > 0.0 and C_.e_prec == 0.0:
                    rh = MT.rho_di(Z_)
                    C_.campo.A[...] = 0.0
                    C_.campo.E[...] = C_.gauss(e_ * (rh - rh.mean()))
                elif C_.e_prec > 0.0:
                    C_.campo.E *= e_ / C_.e_prec
                C_.campo.e = e_
                C_.e_prec = e_
                CT.tick_chi(Z_["z"], C_.campo, K.P, K.Lp, K.X)
                totp = float(np.sum(CTO.CO.conti_nodo(Z_)["tot"]))
                self.registra(k, totp, self.kv(), float(np.sum(np.abs(Z_["st"]["psi_h"]) ** 2)))

        def misura_chi(k):
            rh = MT.rho_di(Z)
            H, Hc = energia(Z, C, K)
            uN = 1.0 - np.exp(-K.P.kappa * K.X["chi"])
            cs_ = K.P.s * np.exp(-K.P.kappa * K.X["chi"])
            nodo, r, ra, c0n = geo["nodo"], geo["r"], geo["ra"], geo["c0n"]
            rit = math.pi * np.abs(cs_[nodo[0::2]] - cs_[nodo[1::2]])
            EX["k"].append(k)
            EX["picco"].append(float(rh.max()))
            EX["H"].append(H)
            EX["H_chi"].append(Hc)
            EX["chi_medio"].append(float(K.X["chi"].mean()))
            EX["max_theta"].append(float(np.max(np.abs(K.X["theta_a"]))))
            for R in CM.ANELLI:
                EX["uN_%d" % R].append(float(uN[c0n]) if R == 0 else CM.anello(r, uN, R))
                EX["rit_%d" % R].append(CM.anello(ra, rit, R) if R > 0 else float(np.mean(rit[(nodo[0::2] == c0n) | (nodo[1::2] == c0n)])))

        def dopo_nascita():
            nonlocal Mi
            Mi = ML.misure_su(Z, centro, Mi.S)
            RC_.etichette([meta["lab"]])
            rigeometria()

        RC_ = CorsaChi(Z, C)
        RC_.etichette([meta["lab"]])
        RC_.inizio(k_da)
        if modo == "mitosi" and nascita_iniziale and meta.get("tronco_scatto"):
            sc = NS.cont.scattati()
            assert sc.size, "lo stato del tronco NON ha un arco scattato"
            NS.nasci(Z, C, int(sc[0]), k_da, "lo scatto del tronco; %d in attesa" % (sc.size - 1))
            dopo_nascita()
        t1 = t_tappa = time.time()
        R5 = rg = float("nan")
        k = k_da
        for k in range(k_da, k_fino + 1):
            if k > k_da:
                RC_.passo(k, t0 + k, 1.0, e)
                K.controlla()
                if forza is not None and k == forza[0]:
                    a_ = forza[1]
                    th = float(K.X["theta_a"][a_])
                    K.X["theta_a"][a_] = th + QUANTO * (1.0 if th >= 0.0 else -1.0)      # ### SOLO nelle prove: lo scatto forzato
                if modo == "mitosi":
                    sc = NS.cont.scattati()
                    if sc.size:
                        NS.nasci(Z, C, int(sc[0]), k, "scattato; %d in attesa" % (sc.size - 1))
                        dopo_nascita()
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            if k > k_da and k % CTO.OGNI == 0:
                RC_.etichette([c])
                meta["lab"] = [float(x) for x in c]
            if k % PS.OGNI == 0:
                R5 = PS.r5(Z, t0 + k)[0] if not NS.nascite else float("nan")
                rg = MRo.raggio(Z, rho, c)
            if k % PS.OGNI_MAPPA == 0 and not NS.nascite:
                PS.PO.dphi_nodi(Z, t0 + k)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % OGNI == 0 and k > k_da:
                Mi.misura(k, RC_, R5, rg)
                misura_chi(k)
                ii, jj = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
                src = int(np.argmin(ML.raggi(Z, c)))
                dd = ML.passi(ii, jj, Z["mot"].inc.n, src)
                e1 = ML.scala(dd, rho)
                da_ = np.minimum(dd[ii], dd[jj])
                lont = da_ >= int(dd.max()) - 1
                a40 = np.isin(ii, anelli[40.0]) | np.isin(jj, anelli[40.0])
                g = np.abs(NS.gacc)
                for x_, v_ in (("D_k", k), ("D_med40", float(np.median(dd[anelli[40.0]]))), ("D_med60", float(np.median(dd[anelli[60.0]]))),
                               ("D_r50", e1[0]), ("D_r90", e1[1]), ("D_w", e1[2]), ("D_n", NS.nascite), ("D_epersa", NS.e_persa),
                               ("G_norma", float(np.linalg.norm(NS.gacc))), ("G_max_lontano", float(g[lont].max())), ("G_max_40", float(g[a40].max())), ("G_d_max", int(dd.max()))):
                    DS[x_].append(v_)
                if k % 250 == 0:
                    S = Mi.S
                    print("    k %6d  M %.12e  E %+.10e  H %+.10e  E_persa %+.6e  H+E_persa %+.10e  nascite %d  n %d  D1 %.1f/%.1f  E1 %s  1-N centro %.4e  max|Theta| %.4f  (%.0f s)" % (
                        k, S["M"][-1], S["E"][-1], EX["H"][-1], NS.e_persa, EX["H"][-1] + NS.e_persa, NS.nascite, Z["mot"].inc.n, DS["D_med40"][-1], DS["D_med60"][-1], e1,
                        EX["uN_0"][-1], EX["max_theta"][-1], time.time() - t00))
                    sys.stdout.flush()
            if k > k_da and (k % OGNI_STATO == 0 or k == k_fino):
                fz = os.path.join(d_out, "stato_%06d.npz" % k)
                s = salva(Z, C, NS, k, t0 + k, dict(meta, tronco_scatto=False), fz)
                sx = "%06d" % k
                np.savez(os.path.join(d_out, "serie_%s.npz" % sx), **{x: np.array(v_) for x, v_ in list(Mi.S.items()) + list(DS.items())})
                np.savez(os.path.join(d_out, "serie_chi_%s.npz" % sx), **{x: np.array(v_) for x, v_ in EX.items()})
                with open(os.path.join(d_out, "nascite_%s.json" % sx), "w", encoding="utf-8") as fh:
                    json.dump(NS.bilanci, fh)
                print("    [stato] k %d sha1 %s" % (k, s[:8]))
                sys.stdout.flush()
            adesso = time.time()
            if reg and adesso - t_tappa >= MT.TAPPA_S:
                RC.tappa(reg, "k %d; %.3f s per tick; nascite %d; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), NS.nascite, MT.memoria_gb()))
                t_tappa = adesso
        fine = stato_di(Z, C, NS)
        fine["serie"] = {"M": Mi.S, "D": DS, "chi": EX}
        Z["metti"]()
    print("### %s: %d tick in %.0f s; %d nascite; E_persa %+.6e; il codice %d" % (nome, k - k_da, time.time() - t00, NS.nascite, NS.e_persa, codice))
    sys.stdout.flush()
    return codice, k, fine


def diverse(a, b):
    return ML.diverse({x: a[x] for x in a if x != "serie"}, {x: b[x] for x in b if x != "serie"})


# ------------------------------------------------------------------------------------------ P6.0
def p60():
    """### P6.0 *(la carta sez. `2.3`)*: CHI-EXT da `stato_02750` della corsa `lapse-u` a `k 3000` contro `stato_03000`."""
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    K0, K1 = 2750, 3000
    f0, f1 = os.path.join(DIR_M, "stato_%05d.npz" % K0), os.path.join(DIR_M, "stato_%05d.npz" % K1)
    esiti = []
    print("=" * 140)
    print("P6.0 DEL RAMO mitosi-chi (Luca 2026-11-21 19:40, R2; la carta sez. 2.3): il passo del ramo (CHI-EXT, il campo generico) da %s a k %d contro %s della corsa del ramo lapse-u" % (
        os.path.basename(f0), K1, os.path.basename(f1)))
    print("=" * 140)
    d = os.path.join(BASE, "P60")
    if os.path.isdir(d):
        shutil.rmtree(d)
    t1 = time.time()
    _c, k, fine = ciclo("P60", "ext", f0, K1, None, d_out=os.path.join(d, "ext"), d_serie=DIR_M)
    tt = (time.time() - t1) / (K1 - K0)
    assert ML.sha1(f1) == open(f1 + ".sha1", encoding="utf-8").read().split()[0]
    dd = []
    with np.load(f1) as z:
        for x in ("Lambda", "h_int", "phi_h", "psi", "psi_h", "rho"):
            if not np.array_equal(fine[x], z[x]):
                dd.append(x)
        for x, y in (("A", "campo_A"), ("E", "campo_E"), ("chi", "chi"), ("pi", "pi"), ("theta", "theta_a")):
            if not np.array_equal(fine[x], z[y]):
                dd.append(x)
    print("### lo stato a k %d contro %s (ogni array, A, E, chi, pi, theta_a): %s" % (K1, os.path.basename(f1), "AL BIT" if not dd else "### DIVERSE: %s" % dd))
    esiti.append(("P6.0: lo stato del ramo a k %d = quello della corsa del ramo lapse-u AL BIT" % K1, not dd))
    with np.load(os.path.join(DIR_M, "serie_%05d.npz" % K1)) as z:
        S0 = {x: np.asarray(z[x]) for x in z.files}
    with np.load(os.path.join(DIR_M, "serie_chi_%05d.npz" % K1)) as z:
        X0 = {x: np.asarray(z[x]) for x in z.files}
    S1, X1 = fine["serie"]["M"], fine["serie"]["chi"]
    bit, ulp = [], {}
    for nm, A_, B_ in (("M", S1, S0), ("chi", X1, X0)):
        for x in B_:
            p, q = np.asarray(A_[x], dtype=float), B_[x].astype(float)
            if p.shape != q.shape:
                bit.append("%s:%s forma" % (nm, x))
                continue
            if np.array_equal(p, q, equal_nan=True):
                continue
            if x in ("E", "H"):
                ulp["%s:%s" % (nm, x)] = float(np.nanmax(np.abs(p - q) / np.spacing(np.abs(q))))
            else:
                bit.append("%s:%s" % (nm, x))
    okS = not bit and all(v <= 8.0 for v in ulp.values())
    print("### le misure (%d da k 0 a k %d) contro quelle della corsa: AL BIT salvo %s; E e H in ulp relativi: %s -> %s" % (
        len(S0["k"]), K1, bit or "nessuna", {x: round(v, 1) for x, v in ulp.items()} or "AL BIT", "PASSA" if okS else "### NON PASSA"))
    esiti.append(("P6.0: le misure AL BIT, E e H entro 8 ulp (il campo generico somma V in un altro ordine)", okS))
    a_t = 0
    _c, _k, rotto = ciclo("P60_rotto", "ext", f0, K0 + 10, None, d_out=os.path.join(d, "rotto"), d_serie=DIR_M, tocca=a_t)
    _c, _k, sano = ciclo("P60_sano", "ext", f0, K0 + 10, None, d_out=os.path.join(d, "sano"), d_serie=DIR_M)
    dr = diverse(rotto, sano)
    print("### DEVE FALLIRE: E dell'arco %d spostato di 1 ulp alla ripresa, %d tick: %s" % (a_t, 10, "diverse: %s" % dr[:8] if dr else "### UGUALE"))
    esiti.append(("DEVE FALLIRE: un ulp di E su un arco cambia lo stato", bool(dr)))
    print("### Q-P1: il tick del ramo (con le misure) %.3f s" % tt)
    print("-" * 140)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 140)
    return 0 if all(ok for _n, ok in esiti) else 1


def esiti_stampa(esiti):
    print("-" * 140)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 140)
    return 0 if all(ok for _n, ok in esiti) else 1


# ------------------------------------------------------------------------------------------ le nascite forzate: P1, P3, P9, i casi noti, K4, Q-P1
def k4(Lp, n_nodi, nodo_h, sorgente, c2, m2):
    """### la riga di K4 di `chi_prove.py`: `chi = 1` sul nodo `sorgente`, `t = 1..30`; `(passa, il primo t che cade)`."""
    import scipy.sparse as sp
    from scipy.sparse import csgraph
    ii, jj = nodo_h[0::2], nodo_h[1::2]
    Adj = sp.csr_matrix((np.ones(2 * len(ii)), (np.concatenate([ii, jj]), np.concatenate([jj, ii]))), shape=(n_nodi, n_nodi))
    dist = csgraph.shortest_path(Adj, unweighted=True, indices=sorgente)
    chi = np.zeros(n_nodi)
    chi[sorgente] = 1.0
    pi = np.zeros(n_nodi)
    for t in range(1, 31):
        pi += 0.5 * (c2 * Lp.delta(chi) - m2 * chi)
        chi += pi
        pi += 0.5 * (c2 * Lp.delta(chi) - m2 * chi)
        if not (bool(np.all(chi[dist > t] == 0.0)) and bool(np.any(chi[dist == t] != 0.0))):
            return False, t
    return True, None


def nascite():
    import types
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    MT, CV = PS.MT, PS.CV
    f3 = os.path.join(DIR_M, "stato_03000.npz")
    esiti = []
    print("=" * 140)
    print("LE NASCITE FORZATE DEL RAMO mitosi-chi (Luca 2026-11-21 19:40, R2-R3; la carta sez. 2.3): P1, P3, P9, i casi noti nel guscio e a r 30, K4 dopo la nascita, Q-P1; dallo stato %s della corsa del ramo lapse-u, piu' 5 tick" % os.path.basename(f3))
    print("=" * 140)
    for caso, (r_min, r_max, r_bers) in (("NEL GUSCIO", (17.0, 20.0, 18.9)), ("A r 30", (0.0, 1e9, 30.0))):
        with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
            P, m0 = parametri_di(Z)
            C, NS, meta = apri(Z, f3, True, P, m0)
            K = NS.K
            mot, st = Z["mot"], Z["st"]
            tt = []
            for _q in range(5):
                t1 = time.time()
                CT.tick_chi(Z["z"], C.campo, K.P, K.Lp, K.X)
                tt.append(time.time() - t1)
            K.controlla()
            r = ML.raggi(Z, meta["centro"])
            nodo0 = np.asarray(mot.inc.nodo).copy()
            ra = 0.5 * (r[nodo0[0::2]] + r[nodo0[1::2]])
            dentro = np.nonzero((ra >= r_min) & (ra <= r_max))[0]
            a = int(dentro[np.argmin(np.abs(ra[dentro] - r_bers))])
            n0 = int(mot.inc.n)
            M0, V0 = float(np.sum(np.abs(st["psi_h"]) ** 2)), float(np.sum(np.abs(st["phi_h"]) ** 2))
            res0 = MR.residuo(C.campo, MT.rho_di(Z))
            H0, Hc0 = energia(Z, C, K)
            print("### %s: l'arco %d a r %.3f (il punto medio); H prima %.12e (H_chi %+.6e); somma c0 %.10e" % (caso, a, float(ra[a]), H0, Hc0, K.P.c0 * n0))
            R, S = regola_chi(Z, C, a, K)
            nd = R["nodi"]
            for q, (lt, h) in enumerate(zip(R["lati"], R["H"])):
                print("    il flip %d (%d, %d): H %.10e (DH dalla nascita %+.6e)%s" % (q, lt[0], lt[1], h, h - R["H_nascita"], "   <- SCELTO" if q == R["scelto"] else ""))
            print("    la sola nascita H %.10e (DH %+.6e, H_chi %+.6e); lo scarto fra il migliore e il secondo %.3e |H|; chi del nodo nuovo %+.6e (la media di %+.6e e %+.6e); il tempo %s s" % (
                R["H_nascita"], R["H_nascita"] - H0, R["H_chi_nascita"], R["gap"], float(S["chi"][-1]), float(K.X["chi"][nd["i"]]), float(K.X["chi"][nd["j"]]), ["%.1f" % x for x in R["t"]]))
            M1, V1 = float(np.sum(np.abs(S["psi"]) ** 2)), float(np.sum(np.abs(S["phi"]) ** 2))
            dM, dV = abs(M1 - M0) / M0, abs(V1 - V0) / V0
            lato = R["lati"][R["scelto"]] if R["scelto"] >= 0 else None
            Sf = candidato_chi(Z, C, a, lato, "stella", K, fattore=False)
            dMf = abs(float(np.sum(np.abs(Sf["psi"]) ** 2)) - M0) / M0
            dVf = abs(float(np.sum(np.abs(Sf["phi"]) ** 2)) - V0) / V0
            print("### P1: M %.1e, V %.1e; DEVE FALLIRE senza il fattore di stella: M %.1e, V %.1e" % (dM, dV, dMf, dVf))
            esiti.append(("%s P1: le norme M e V entro 1e-12 relativo" % caso, dM <= 1e-12 and dV <= 1e-12))
            esiti.append(("%s DEVE FALLIRE: senza il fattore di stella le norme escono da 1e-12" % caso, dMf > 1e-12 or dVf > 1e-12))
            print("### P3: il residuo di Gauss prima %.3e; dopo %.3e; DEVE FALLIRE senza Gauss %.3e" % (res0, S["res"], S["res_senza_gauss"]))
            esiti.append(("%s P3: il residuo dopo la nascita sotto 10 volte quello di prima" % caso, S["res"] <= 10 * res0))
            esiti.append(("%s DEVE FALLIRE: senza Gauss sopra 10 volte" % caso, S["res_senza_gauss"] > 10 * res0))
            b = NS.nasci(Z, C, a, int(meta["k"]) + 5, "FORZATA (%s)" % caso)
            H1, Hc1 = energia(Z, C, K)
            d9f = abs(H1 - (S["H"] - S["H_chi"])) / abs(S["H"])
            print("### P9: H riletta %.17e contro il candidato %.17e: %.1e |H|; E_persa %+.6e, -(H dopo - H prima) %+.6e; DEVE FALLIRE il candidato senza H_chi: %.1e |H|" % (
                H1, S["H"], b["P9"], NS.e_persa, -(H1 - H0), d9f))
            esiti.append(("%s P9: H riletta = H del candidato entro 1e-12 |H|, E_persa = -DH" % caso, b["P9"] <= 1e-12 and NS.e_persa == -(H1 - H0)))
            esiti.append(("%s DEVE FALLIRE: il candidato senza H_chi fuori da 1e-12" % caso, d9f > 1e-12))
            print("### IL CASO NOTO: DH nascita %+.6e, DH flip %+.6e, DH %+.6e, DH_chi %+.6e; somma c0 %.10e -> %.10e (la differenza %.6e, c0 %.6e); il lato %s; n %d a r %.3f, %d passi dalla sorgente" % (
                b["DH_nascita"], b["DH_flip"], b["DH"], b["DH_chi"], b["somma_c0"][0], b["somma_c0"][1], b["somma_c0"][1] - b["somma_c0"][0], K.P.c0, lato, nd["n"], b["r"], b["passi"]))
            ok_g = K.X["chi"].size == mot.inc.n and K.X["pi"].size == mot.inc.n and K.cont.theta.size == mot.inc.m and len(Z["m1"]) == mot.inc.n and K.Lp.n == mot.inc.n
            esiti.append(("%s chi, pi, Theta, le posizioni, il Laplaciano seguono il grafo" % caso, ok_g))
            nn = int(mot.inc.n)
            nodo1 = np.asarray(mot.inc.nodo)
            ok4, t4 = k4(K.Lp, nn, nodo1, nn - 1, K.P.c2, K.P.m2)
            vecchio = CT.Laplaciano(types.SimpleNamespace(inc=types.SimpleNamespace(nodo=nodo0, n=nn)))
            ok4f, t4f = k4(vecchio, nn, nodo1, nn - 1, K.P.c2, K.P.m2)
            print("### K4 DOPO LA NASCITA (chi = 1 sul nodo nato %d): %s; DEVE FALLIRE col Laplaciano del grafo vecchio (il nodo nuovo isolato): %s" % (
                nn - 1, "PASSA per t = 1..30" if ok4 else "### CADE a t %s" % t4, ("cade a t %s" % t4f) if not ok4f else "### PASSA"))
            esiti.append(("%s K4: il fronte di chi a un arco per tick sul grafo nuovo" % caso, ok4))
            esiti.append(("%s DEVE FALLIRE: K4 col Laplaciano del grafo vecchio" % caso, not ok4f))
            ta = []
            for _q in range(5):
                t1 = time.time()
                CT.tick_chi(Z["z"], C.campo, K.P, K.Lp, K.X)
                ta.append(time.time() - t1)
            K.controlla()
            print("### Q-P1: il tick prima della nascita %.3f s, dopo %.3f s (la media di 5); la nascita %.1f s" % (float(np.mean(tt)), float(np.mean(ta)), b["t"]))
            sys.stdout.flush()
            Z["metti"]()
    return esiti_stampa(esiti)


# ------------------------------------------------------------------------------------------ P8
def p8():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    f3 = os.path.join(DIR_M, "stato_03000.npz")
    with np.load(f3) as z:
        a = int(np.argmax(np.abs(z["theta_a"])))
    KF, KM, KE = 3001, 3005, 3010
    d = os.path.join(BASE, "P8")
    if os.path.isdir(d):
        shutil.rmtree(d)
    esiti = []
    print("=" * 140)
    print("P8 DEL RAMO mitosi-chi (Luca 2026-11-21 19:40, R2; la carta sez. 2.3): lo scatto FORZATO dell'arco %d a k %d (la nascita), %d tick di fila contro %d + salva + riprendi + %d" % (a, KF, KE - 3000, KM - 3000, KE - KM))
    print("=" * 140)
    _c, _k, cont = ciclo("P8_fila", "mitosi", f3, KE, None, forza=(KF, a), d_out=os.path.join(d, "fila"), d_serie=DIR_M)
    _c, _k, _p = ciclo("P8_prima", "mitosi", f3, KM, None, forza=(KF, a), d_out=os.path.join(d, "spezza"), d_serie=DIR_M)
    fm = os.path.join(d, "spezza", "stato_%06d.npz" % KM)
    _c, _k, rip = ciclo("P8_dopo", "mitosi", fm, KE, None, d_out=os.path.join(d, "spezza"))
    dd = diverse(cont, rip)
    print("### P8: %d tick di fila contro la ripresa da %s (sha1 %s): %s; chi %d nodi, Theta %d archi, E_persa %+.6e" % (
        KE - 3000, os.path.basename(fm), ML.sha1(fm)[:8],
        "AL BIT su ogni chiave, A, E, il grafo, i versori, Theta, le posizioni, E_persa, gauss_acc, chi, pi" if not dd else "### DIVERSE: %s" % dd,
        cont["chi"].size, cont["theta"].size, float(cont["E_persa"][0])))
    esiti.append(("P8: la ripresa dopo una nascita AL BIT (chi, pi, Theta, il grafo compresi)", not dd))
    esiti.append(("P8 non a vuoto: la nascita c'e' stata (un nodo in piu')", cont["chi"].size == 186 * 186 + 1))
    fr = os.path.join(d, "rotto", "stato_%06d.npz" % KM)
    os.makedirs(os.path.dirname(fr), exist_ok=True)
    shutil.copyfile(fm, fr)
    shutil.copyfile(fm + ".sha1", fr + ".sha1")
    meta_ = os.path.getsize(fr) // 2
    with open(fr, "r+b") as fh:
        fh.seek(meta_)
        x = fh.read(1)
        fh.seek(meta_)
        fh.write(bytes([x[0] ^ 0x01]))
    rifiuta = False
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        try:
            P, m0 = parametri_di(Z)
            apri(Z, fr, True, P, m0)
            print("### DEVE FALLIRE: un byte dello stato cambiato: ### la ripresa ACCETTA")
        except AssertionError as ex:
            rifiuta = "sha1" in str(ex)
            print("### DEVE FALLIRE: un byte dello stato cambiato: la ripresa RIFIUTA (%s)" % ex)
        Z["metti"]()
    esiti.append(("DEVE FALLIRE: un byte dello stato salvato cambiato -> la ripresa RIFIUTA (lo sha1)", rifiuta))
    return esiti_stampa(esiti)


# ------------------------------------------------------------------------------------------ R4: la prova della ramificazione
def rami_prova():
    import _presidio
    import chi_tronco as TR
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(os.path.join(_QUI, "chi_tronco.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    f3 = os.path.join(DIR_M, "stato_03000.npz")
    with np.load(f3) as z:
        a = int(np.argmax(np.abs(z["theta_a"])))
    KF, KS, KE = 3003, 3006, 3009
    d = os.path.join(BASE, "PROVA_RAMI")
    if os.path.isdir(d):
        shutil.rmtree(d)
    esiti = []
    print("=" * 140)
    print("R4, LA PROVA DELLA RAMIFICAZIONE DEL RAMO mitosi-chi (Luca 2026-11-21 19:40; la carta sez. 2.3; come 6e51d762): lo scatto FORZATO dell'arco %d a k %d (solo qui)" % (a, KF))
    print("=" * 140)
    _c, _k, cont_m = ciclo("PROVA_cont_m", "mitosi", f3, KS, None, forza=(KF, a), d_out=os.path.join(d, "cont_m"), d_serie=DIR_M)
    _c, _k, cont_c = ciclo("PROVA_cont_c", "ext", f3, KS, None, forza=(KF, a), d_out=os.path.join(d, "cont_c"), d_serie=DIR_M)
    cod, kt, _f = TR.corsa(f3, KS, None, os.path.join(d, "tronco"), forza=(KF, a))
    with open(os.path.join(d, "tronco", "scatto.json"), encoding="utf-8") as fh:
        sj = json.load(fh)
    print("### il tronco chi (chi_tronco.py, il campo prototipo): il codice %d a k %d; scatto.json %s" % (cod, kt, json.dumps({x: sj[x] for x in ("k", "archi", "quanti")})))
    esiti.append(("il tronco esce col codice dello scatto al tick forzato", cod == TR.SCATTO and kt == KF and sj["k"] == KF))
    _c, _k, ramo_m = ciclo("PROVA_m", "mitosi", sj["file"], KS, None, d_out=os.path.join(d, "ramo_m"))
    _c, _k, ramo_c = ciclo("PROVA_c", "ext", sj["file"], KS, None, d_out=os.path.join(d, "ramo_c"))
    _c, _k, senza = ciclo("PROVA_senza", "mitosi", sj["file"], KS, None, nascita_iniziale=False, d_out=os.path.join(d, "ramo_senza"))
    d1, d2, d3 = diverse(cont_m, ramo_m), diverse(cont_c, ramo_c), diverse(cont_m, senza)
    print("### R1: il ramo MITOSI-CHI contro la corsa continua (k %d): %s" % (KS, "AL BIT su ogni chiave, A, E, il grafo, i versori, Theta, le posizioni, E_persa, gauss_acc, chi, pi" if not d1 else "### DIVERSE: %s" % d1))
    esiti.append(("R1: il ramo MITOSI-CHI = la corsa continua con le nascite AL BIT", not d1))
    print("### R2: il ramo CHI-EXT contro la corsa continua spenta: %s" % ("AL BIT" if not d2 else "### DIVERSE: %s" % d2))
    esiti.append(("R2: il ramo CHI-EXT = la corsa continua spenta AL BIT", not d2))
    print("### DEVE FALLIRE: il ramo MITOSI-CHI SENZA la nascita iniziale: %s" % ("### UGUALE" if not d3 else "diverse: %s" % d3[:6]))
    esiti.append(("DEVE FALLIRE: il ramo MITOSI-CHI senza la nascita iniziale e' diverso", bool(d3)))
    _c, _k, cont_e = ciclo("PROVA_cont_e", "mitosi", f3, KE, None, forza=(KF, a), d_out=os.path.join(d, "cont_e"), d_serie=DIR_M)
    u = ultimo(os.path.join(d, "ramo_m"))
    _c, _k, rip = ciclo("PROVA_rip", "mitosi", u[1], KE, None, d_out=os.path.join(d, "ramo_m"))
    d4 = diverse(cont_e, rip)
    print("### R3: la ripresa del ramo MITOSI-CHI da %s fino a k %d contro la continua: %s" % (os.path.basename(u[1]), KE, "AL BIT" if not d4 else "### DIVERSE: %s" % d4))
    esiti.append(("R3: la ripresa dopo una nascita AL BIT", not d4))
    return esiti_stampa(esiti)


def main(argv):
    import argparse
    import _presidio
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("p60")
    sub.add_parser("nascite")
    sub.add_parser("p8")
    sub.add_parser("rami_prova")
    r = sub.add_parser("ramo")
    r.add_argument("--nome", choices=("MITOSICHI", "CHIEXT"), required=True)
    r.add_argument("--da", choices=("primo", "ultimo"), required=True)
    r.add_argument("--dopo", type=int, required=True)
    r.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cmd in ("p60", "nascite", "p8", "rami_prova"):
        return {"p60": p60, "nascite": nascite, "p8": p8, "rami_prova": rami_prova}[x.cmd]()
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(os.path.join(_QUI, "mitosi_lunga.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    from solitone import _registro_corse as RC
    import chi_tronco as TR
    d = os.path.join(BASE, x.nome)
    with open(os.path.join(TR.DIR_T, "scatto.json"), encoding="utf-8") as fh:
        sj = json.load(fh)
    k_fine = int(sj["k"]) + int(x.dopo)
    if x.da == "primo":
        f = sj["file"]
        assert ML.sha1(f) == sj["sha1"], "lo stato del tronco NON e' integro"
    else:
        u = ultimo(d)
        assert u is not None, "nessuno stato integro di %s" % x.nome
        f = u[1]
        if x.registro:
            RC.tappa(x.registro, "RIPRESA di %s da k %d, %s sha1 %s" % (x.nome, u[0], os.path.basename(f), ML.sha1(f)[:8]))
    cod, _k, _f = ciclo(x.nome, "mitosi" if x.nome == "MITOSICHI" else "ext", f, k_fine, x.registro, d_out=d)
    return cod


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
