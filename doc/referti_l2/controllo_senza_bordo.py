# -*- coding: utf-8 -*-
r"""**LA CORSA DI CONTROLLO SENZA BORDO E SENZA MITOSI** *(Luca `2026-11-17` `15:22`; la carta e le previsioni `doc/TASK_HISTORY/2026-11-17_controllo_senza_bordo.md`, `181df738`)*.

    E:\python\py3132\python.exe doc/referti_l2/controllo_senza_bordo.py caso
    E:\python\py3132\python.exe doc/referti_l2/controllo_senza_bordo.py costo --L 186 --tick 100
    E:\python\py3132\python.exe doc/referti_l2/controllo_senza_bordo.py corsa --nome C1 --L 186 --bordo si --da 0 --fino 3000 --registro controllo-C1
    E:\python\py3132\python.exe doc/referti_l2/controllo_senza_bordo.py referto > doc/referti_l2/controllo_senza_bordo.txt

**Il cammino:** quello della fase `0` *(`prova_scatola5.corsa` da `k 0`: il francobollo, `vuoto_fresco`, `incolla`, `r5`, `metti_bordo(2 R_ogg)`, `porto.campi`; `mattone_cottura.Corsa.passo`; le misure di `prova_scatola5` alla stessa cadenza)*; **SENZA BORDO = `Z["g_e"] = 0`** *(la carta, sez. `1`; il caso K2 lo prova uguale al bit a `p6_bracci.tick_GU`)*.
**Le misure ogni `OGNI` tick** *(il centro = il baricentro della materia a `k 0`)*: la massa entro `12.4`, `15`, `20`, `25`, `30`, `45`; il flusso di energia `J` *(`flusso_uscente.flusso`, su una COPIA dello stato)* agli anelli `15`, `20`, `30`, `45`, il positivo e il netto; R_ogg al `5%` e il raggio *(`prova_scatola5.r5`, `mattone_rhoc.raggio`)*; la norma e l'energia totale *(`Corsa.T`: `totd + KVd`, il conto dopo il bordo)*.
**Gli stati** ogni `250` tick in `E:/soliton_simulator/controllo/<nome>/stato_%05d.npz` col `.sha1`; **la ripresa** con `--da k` *(K3 la prova al bit)*. **C1 contro la fase `0`** ai tick `950, 1000, 1950, 2000, 2950, 3000` *(`legati.uguale`, esclusa `h_int`)*.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_QUI, _SOL, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import prova_scatola5 as PS  # noqa: E402
import flusso_uscente as FU  # noqa: E402

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
OGNI = 50
OGNI_STATO = 250
R_MASSA = (12.4, 15.0, 20.0, 25.0, 30.0, 45.0)
R_J = (15.0, 20.0, 30.0, 45.0)
FASE0 = (950, 1000, 1950, 2000, 2950, 3000)


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def copia_stato(st):
    return {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in st.items()}


def prepara(Z, L, bordo, rho_c, e, t0):
    """### Lo stato di `k 0` della fase `0` (le righe di `prova_scatola5.corsa`); `bordo` False -> `g_e = 0`."""
    MT, C243, PO = PS.MT, PS.C243, PS.PO
    fr = C243.francobollo_L162("MGU", 0)
    MT.vuoto_fresco(Z, t0)
    cd = PS.nodo_buono(fr, Z["bordo"]["c0"], L)
    D = MT.incolla(Z, fr, cd, True)
    R, rr, b = PS.r5(Z, t0)
    PS.metti_bordo(Z, PS.FATTORE_R_A * R)
    if not bordo:
        Z["g_e"] = np.zeros_like(Z["g_e"])
    C = PO.campi(Z, rho_c, e)
    return C, {"incollato": [int(x) for x in cd], "Delta": float(D), "R_ogg5_k0": float(R), "R_A": float(PS.FATTORE_R_A * R)}


def salva(Z, C, k, t, meta, nome):
    d = os.path.join(DIR, nome)
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "stato_%05d.npz" % k)
    dati = {x: Z["st"][x] for x in Z["chiavi"]}
    dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
    cs = PS.LC.cs_prec()
    if cs is not None:
        dati["cs_prec"] = cs
    np.savez(f, meta=np.array(json.dumps(dict(meta, k=k, t=t))), **dati)
    s = sha1(f)
    with open(f + ".sha1", "w", encoding="utf-8") as fh:
        fh.write(s + "\n")
    return f, s


def riprendi(Z, f, bordo, rho_c, e):
    s = sha1(f)
    with open(f + ".sha1", encoding="utf-8") as fh:
        assert fh.read().split()[0] == s, "lo sha1 di %s non coincide: FERMO" % f
    with np.load(f) as d:
        Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
        A, E = d["campo_A"].copy(), d["campo_E"].copy()
        meta = json.loads(str(d["meta"]))
        cs = d["cs_prec"].copy() if "cs_prec" in d.files else None
    PS.metti_bordo(Z, meta["R_A"])
    if not bordo:
        Z["g_e"] = np.zeros_like(Z["g_e"])
    return PS.PO.campi(Z, rho_c, e, A, E), meta, cs, s


class Misure(object):
    def __init__(self, Z, centro):
        from solitone import toro as TO
        self.Z = Z
        L = Z["L"]
        self.r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], centro[0], centro[1], L).T[:2])
        self.ii, self.jj = np.asarray(Z["mot"].inc.ii), np.asarray(Z["mot"].inc.jj)
        self.S = {x: [] for x in ("k", "M", "E", "R5", "raggio") + tuple("Min_%g" % R for R in R_MASSA) + tuple("Jp_%g" % R for R in R_J) + tuple("Jn_%g" % R for R in R_J)}

    def misura(self, k, RC_, R5, raggio):
        import energia as EN
        MT = PS.MT
        Z = self.Z
        rho = MT.rho_di(Z)
        stc = copia_stato(Z["st"])
        J = np.asarray(EN.corrente(stc, Z["mot"], Z["par"], None), dtype=float)
        S = self.S
        S["k"].append(k)
        S["M"].append(float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2)))
        T = RC_.T
        S["E"].append(float(T["totd"][-1] + T["KVd"][-1]) if T["totd"] else float("nan"))
        S["R5"].append(float(R5))
        S["raggio"].append(float(raggio))
        for R in R_MASSA:
            S["Min_%g" % R].append(float(rho[self.r < R].sum()))
        for R in R_J:
            p, n_, _q = FU.flusso(J, self.ii, self.jj, self.r, R)
            S["Jp_%g" % R].append(p)
            S["Jn_%g" % R].append(n_)

    def salva(self, f):
        np.savez(f, **{x: np.array(v) for x, v in self.S.items()})


def corsa(nome, L5, bordo, k_da, k_fino, reg, ogni):
    from solitone import _registro_corse as RC
    MT, CT, PO, LC, LG, MR, CV = PS.MT, PS.CT, PS.PO, PS.LC, PS.LG, PS.MR, PS.CV
    PS.presidi()
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    print("=" * 130)
    print("IL CONTROLLO SENZA BORDO (Luca 2026-11-17 15:22): %s, L %d, il bordo %s, da k %d a k %d, le misure ogni %d" % (nome, L5, "SI" if bordo else "NO (g_e = 0)", k_da, k_fino, ogni))
    print("=" * 130)
    with CV.scena_L(L5, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        assert Z["L"] == L5
        if k_da == 0:
            C, meta = prepara(Z, L5, bordo, rho_c, e, t0)
            rho = MT.rho_di(Z)
            meta["centro"] = [float(x) for x in MT.centro_di(Z, rho)]
            meta["lab"] = meta["centro"]
            cs = None
            M = Misure(Z, meta["centro"])
            print("### lo stato di k 0: %s; il centro delle misure %s" % (json.dumps(meta), meta["centro"]))
        else:
            f = os.path.join(DIR, nome, "stato_%05d.npz" % k_da)
            C, meta, cs, s = riprendi(Z, f, bordo, rho_c, e)
            M = Misure(Z, meta["centro"])
            with np.load(os.path.join(DIR, nome, "serie_%05d.npz" % k_da)) as d:
                M.S = {x: list(d[x]) for x in d.files}
            print("### la ripresa da %s (sha1 %s, ricontrollato)" % (f, s[:8]))
        PO.accendi(cs)
        try:
            RC_ = CT.Corsa(Z, C)
            RC_.etichette([meta["lab"]])
            RC_.inizio(k_da)
            t1 = t_tappa = time.time()
            k = k_da
            for k in range(k_da, k_fino + 1):
                if k > k_da:
                    RC_.passo(k, t0 + k, 1.0, e)
                rho = MT.rho_di(Z)
                c = MT.centro_di(Z, rho)
                if k > k_da and (k - 0) % CT.OGNI == 0:
                    RC_.etichette([c])
                    meta["lab"] = [float(x) for x in c]
                if k % PS.OGNI == 0:
                    R5, _rr, _b = PS.r5(Z, t0 + k)
                    rg = MR.raggio(Z, rho, c)
                if k % PS.OGNI_MAPPA == 0:
                    PO.dphi_nodi(Z, t0 + k)
                if k % MT.OGNI_GAUSS == 0:
                    C.residuo()
                if k % ogni == 0 and not (k == k_da and k_da > 0):
                    M.misura(k, RC_, R5, rg)
                if k % 250 == 0:
                    S = M.S
                    print("    k %5d  la massa %.12e  l'energia %+.10e  R5 %.1f  Min12.4 %.6e  J45 + %.4e netto %+.4e  (%.0f s)" % (
                        k, S["M"][-1], S["E"][-1], S["R5"][-1], S["Min_12.4"][-1], S["Jp_45"][-1], S["Jn_45"][-1], time.time() - t00))
                    sys.stdout.flush()
                if bordo and L5 == 186 and k in FASE0 and k > k_da:
                    fz = os.path.join(MT.DIR_E, "scatola5_L186_%05d.npz" % k)
                    div = LG.uguale(Z, C, fz)
                    print("### C1 CONTRO LA FASE 0 a k %d (%s): %s" % (k, os.path.basename(fz), "AL BIT (esclusa h_int)" if not div else "### DIVERSE: %s" % div))
                if k > k_da and k % OGNI_STATO == 0:
                    f, s = salva(Z, C, k, t0 + k, meta, nome)
                    M.salva(os.path.join(DIR, nome, "serie_%05d.npz" % k))
                    print("    [stato] k %d: %s sha1 %s" % (k, os.path.basename(f), s[:8]))
                adesso = time.time()
                if reg and adesso - t_tappa >= MT.TAPPA_S:
                    RC.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), MT.memoria_gb()))
                    t_tappa = adesso
        finally:
            LC.spegni()
        Z["metti"]()
    f = os.path.join(_QUI, "controllo_%s_serie.npz" % nome)
    M.salva(f)
    print("-" * 130)
    print("### %d tick in %.0f s (%.3f s per tick); la serie in %s" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), f))
    print("=" * 130)
    return 0


def caso():
    MT, CT, PO, LC, LG, CV = PS.MT, PS.CT, PS.PO, PS.LC, PS.LG, PS.CV
    PS.presidi()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    esiti = []
    print("=" * 130)
    print("I CASI NOTI DEL CONTROLLO SENZA BORDO (Luca 2026-11-17 15:22)")
    print("=" * 130)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        # ---------------------------------------------------------------- K1
        MT.vuoto_fresco(Z, t0)
        PS.metti_bordo(Z, 50.0)
        Z["g_e"] = np.zeros_like(Z["g_e"])
        C = PO.campi(Z, rho_c, e)
        PO.accendi(None)
        try:
            RC_ = CT.Corsa(Z, C)
            RC_.etichette([[93.0, 93.0]])
            RC_.inizio(0)
            V0 = float(np.sum(np.abs(Z["st"]["phi_h"]) ** 2))
            M0 = float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2))
            for k in range(1, 101):
                RC_.passo(k, t0 + k, 1.0, e)
            T = RC_.T
            E = np.array(T["totd"]) + np.array(T["KVd"])
            V1 = float(np.sum(np.abs(Z["st"]["phi_h"]) ** 2))
            M1 = float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2))
        finally:
            LC.spegni()
        dE = float(np.max(np.abs(E - E[0])) / abs(E[0]))
        print("### K1 il vuoto F3 puro senza bordo, 100 tick: la norma del vuoto %.15e -> %.15e (relativa %.1e); la materia %.1e -> %.1e; l'energia: la deriva massima relativa %.3e" % (
            V0, V1, abs(V1 - V0) / V0, M0, M1, dE))
        esiti.append(("K1 la norma del vuoto costante entro 1e-12 e la materia 0 (il flusso di massa 0)", abs(V1 - V0) / V0 < 1e-12 and M1 == 0.0))
        print("    (l'energia: QC la conserva al secondo ordine; la deriva si dichiara: %.3e)" % dE)
        Z["metti"]()
        # ---------------------------------------------------------------- K2
        C, meta = prepara(Z, 186, False, rho_c, e, t0)
        X0 = {x: Z["st"][x].copy() for x in Z["chiavi"]}
        A0, E0 = C.campo.A.copy(), C.campo.E.copy()
        PO.accendi(None)
        try:
            C.tick(1, t0 + 1, 1.0, e)
            Ya = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            Aa, Ea = C.campo.A.copy(), C.campo.E.copy()
            Z["metti"]({x: v.copy() for x, v in X0.items()})
            C.campo.A[...] = A0
            C.campo.E[...] = E0
            import _u1_prototipo as U1
            U1.scrivi_U(Z["mot"], C.campo)                               # ### U dal campo rimesso (il primo tick l'ha cambiata)
            PS.MT.PBR.tick_GU(Z["z"], Z["s"], C.legge, C.e0, C.campo)
            Yb = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            Ab, Eb = C.campo.A.copy(), C.campo.E.copy()
        finally:
            LC.spegni()
        div = [x for x in Ya if x != "h_int" and not np.array_equal(Ya[x], Yb[x])] + [x for x, a, b in (("A", Aa, Ab), ("E", Ea, Eb)) if not np.array_equal(a, b)]
        print("### K2 un tick di Campi.tick con g_e = 0 contro un tick di p6_bracci.tick_GU, dallo stesso stato di k 0: %s" % ("AL BIT (esclusa h_int)" if not div else "### DIVERSE: %s" % div))
        esiti.append(("K2 senza bordo (g_e = 0) = tick_GU al bit", not div))
        Z["metti"]()
        # ---------------------------------------------------------------- K3
        def venti(spezza):
            C, meta = prepara(Z, 186, False, rho_c, e, t0)
            rho = MT.rho_di(Z)
            meta["centro"] = meta["lab"] = [float(x) for x in MT.centro_di(Z, rho)]
            PO.accendi(None)
            try:
                RC_ = CT.Corsa(Z, C)
                RC_.etichette([meta["lab"]])
                RC_.inizio(0)
                for k in range(1, 21):
                    RC_.passo(k, t0 + k, 1.0, e)
                    if spezza and k == 10:
                        f, s = salva(Z, C, 10, t0 + 10, meta, "K3")
                        LC.spegni()
                        C, meta2, cs, _s = riprendi(Z, f, False, rho_c, e)
                        PO.accendi(cs)
                        RC_ = CT.Corsa(Z, C)
                        RC_.etichette([meta2["lab"]])
                        RC_.inizio(10)
                out = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy())
            finally:
                LC.spegni()
            Z["metti"]()
            return out
        a, b = venti(False), venti(True)
        div = [x for x in a[0] if x != "h_int" and not np.array_equal(a[0][x], b[0][x])] + [x for x, p, q in (("A", a[1], b[1]), ("E", a[2], b[2])) if not np.array_equal(p, q)]
        print("### K3 la ripresa: 20 tick di fila contro 10 + salva + riprendi + 10 (senza bordo): %s" % ("AL BIT (esclusa h_int)" if not div else "### DIVERSE: %s" % div))
        esiti.append(("K3 la ripresa al bit", not div))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-100s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


def costo(L5, n_tick):
    MT, CT, PO, LC, MR, CV = PS.MT, PS.CT, PS.PO, PS.LC, PS.MR, PS.CV
    PS.presidi()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    with CV.scena_L(L5, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, meta = prepara(Z, L5, True, rho_c, e, t0)
        rho = MT.rho_di(Z)
        c = MT.centro_di(Z, rho)
        M = Misure(Z, c)
        PO.accendi(None)
        try:
            RC_ = CT.Corsa(Z, C)
            RC_.etichette([c])
            RC_.inizio(0)
            tt = []
            for k in range(1, n_tick + 1):
                t1 = time.time()
                RC_.passo(k, t0 + k, 1.0, e)
                tt.append(time.time() - t1)
            t1 = time.time()
            R5, _rr, _b = PS.r5(Z, t0 + n_tick)
            rg = MR.raggio(Z, MT.rho_di(Z), c)
            t_r5 = time.time() - t1
            t1 = time.time()
            M.misura(n_tick, RC_, R5, rg)
            t_m = time.time() - t1
        finally:
            LC.spegni()
        Z["metti"]()
    tm = float(np.median(tt))
    print("### IL COSTO su L %d (%d tick, col bordo; il carico della macchina com'e'): il tick la mediana %.3f s (da %.3f a %.3f); r5 + raggio %.3f s; la misura nuova (J, le masse) %.3f s" % (L5, n_tick, tm, min(tt), max(tt), t_r5, t_m))
    print("    la misura nuova ogni %d tick costa %.2f%% dei %d tick; la stima di 3000 tick: %.2f ore" % (OGNI, 100.0 * t_m / (OGNI * tm), OGNI, 3000 * tm * (1 + t_m / (OGNI * tm)) / 3600.0))
    return 0


def referto():
    print("(il referto si scrive dopo le corse: il comando e' nel commit del referto)")
    return 0


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("caso")
    c = sub.add_parser("costo")
    c.add_argument("--L", type=int, required=True)
    c.add_argument("--tick", type=int, required=True)
    r = sub.add_parser("corsa")
    r.add_argument("--nome", required=True)
    r.add_argument("--L", type=int, required=True)
    r.add_argument("--bordo", choices=("si", "no"), required=True)
    r.add_argument("--da", type=int, required=True)
    r.add_argument("--fino", type=int, required=True)
    r.add_argument("--registro")
    r.add_argument("--ogni", type=int, default=OGNI)
    sub.add_parser("referto")
    x = ap.parse_args(argv)
    if x.cmd == "caso":
        return caso()
    if x.cmd == "costo":
        return costo(x.L, x.tick)
    if x.cmd == "corsa":
        return corsa(x.nome, x.L, x.bordo == "si", x.da, x.fino, x.registro, x.ogni)
    return referto()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
