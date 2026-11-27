# -*- coding: utf-8 -*-
r"""**[M1519] IL CORPO FUSO: S1 LA CORSA LIBERA d1''' E S2 IL PUNTO FISSO ACCOPPIATO 2M** *(DECISIONE DI LUCA, 2026-11-27 `15:19`, dalla posta, `df8635b5`; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-unetvicies`, scritta PRIMA, `57392380`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso.py noto > doc/referti_l2/corpo_fuso_noto.txt      (K0'', K0''-neg, K1'', K5, K6, KQ)
    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso.py corsa          (S1: d1L/stato_018000 -> k 54000, in M1519/d1T; dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso.py puntofisso     (S2: 3 giri da 6000, in M1519/puntofisso_2M; dalla coda)

**La ripresa** e' quella della v9 *(`due_corpi_fondo_v9`: il ciclo `D.ciclo` della v2, `geo.U` riscritta dopo la carica)*, con **un'unica generalizzazione**: lo stato si carica da un FILE qualunque *(non solo da `M2034/coppia/d1`)*. I parametri e `centro_coppia` si asseriscono uguali al meta di `d1L/serie.json`. **S2** e' lo schema di [M0414] *(`fondo_puntofisso_chi_v2.giro`)* sulla scena di d1': `omega` sull'INTERA `psi`, `w` e la profondita' sulla `rho` totale, `P` da `V2.periodo`, la nuova partenza = `psi` medio riproiettato su `Q_K` *(`PF.trasforma`)* alla massa di `d1L/stato_018000`, `chi` medio, `pi = 0`.
"""
import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v9 as V9  # noqa: E402
import fondo_puntofisso_chi_v2 as V2  # noqa: E402

V7 = V9.V7
V6, D, PF, CT, GD = V7.V6, V7.D, V7.PF, V7.CT, V7.GD
FPC = V2.FPC
D1L = os.path.join(PF.CTRL, "M2034", "coppia", "d1L")
DIR = os.path.join(PF.CTRL, "M1519")
D_S1 = os.path.join(DIR, "d1T")
D_S2 = os.path.join(DIR, "puntofisso_2M")
K_DA, K_A, OGNI_STATO, OGNI_SERIE, OGNI_PARZIALE = 18000, 54000, 250, 10, 2500
K_GIRO, OGNI_W, FIN, GIRI = 6000, 100, 250, 3
TOL_OMEGA = 1e-12          # ### Luca, 13:12
TOL_MASSA = 1e-12          # ### la carta, KQ


def avvia():
    import _presidio
    V7.avvia()
    for m in ("fondo_puntofisso_chi.py", "fondo_puntofisso_chi_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def serie_d1L():
    f = os.path.join(D1L, "serie.json")
    PF.controlla(f)
    return json.load(open(f, encoding="utf-8"))


class Ripresa10(V7.Ripresa):
    """### la `Ripresa` della v7/v8/v9, ma lo stato da `f_stato`; `k_da` il tick assoluto del primo tick dopo la carica meno uno."""

    def __init__(self, Z, f_stato, k_da, corsa, scrivi_U=True, azzera_pi=False):
        from solitone import _u1_oggi as UO
        mt = serie_d1L()["meta"]
        self.Z, self.k_da = Z, k_da
        mot = Z["mot"]
        self.n = mot.inc.n
        self.nodo = np.asarray(mot.inc.nodo)
        self.Lp = CT.Laplaciano(mot)
        self.C, info, self.X = V6.costruisci(Z, 2, V6.STATO_G3)
        self.P, Pon, m0 = D.parametri(Z, self.C, True)
        par = {"kappa": self.P.kappa, "c0": self.P.c0, "m0": m0, "c2": self.P.c2, "m2": self.P.m2, "e0": self.P.e0, "s": self.P.s, "f": self.P.f, "kappa_on": Pon.kappa}
        assert par == mt["parametri"], "i parametri NON sono quelli di d1L: %r contro %r" % (par, mt["parametri"])
        assert info["centro_coppia"] == mt["centro_coppia"], "centro_coppia NON e' quello di d1L"
        self.meta = dict(info, corsa=corsa, da=f_stato, k_da=k_da, parametri=par, pi_azzerato=azzera_pi)
        self.dxy0, M0 = D.corpi(Z, info["centro_coppia"], 2)
        self.maschere = [mm[self.nodo] for mm in M0]
        self.M0 = M0
        PF.controlla(f_stato)
        with np.load(f_stato) as z:
            for x in Z["chiavi"]:
                assert Z["st"][x].shape == z[x].shape
                Z["st"][x][...] = z[x]
            self.C.campo.A[...] = z["campo_A"]
            self.C.campo.E[...] = z["campo_E"]
            for q in CT.CHIAVI_CHI:
                self.X[q][...] = z[q]
        if azzera_pi:
            self.X["pi"][...] = 0.0
        if scrivi_U:
            UO.U1.scrivi_U(mot, self.C.campo)
        self.serie, self.om = [], [[] for _ in M0]


def giro_pf(R, ticks, salva=None, stampa=None):
    """### il ciclo del punto fisso (lo schema di `V2.giro`) per `ticks` tick, tick relativo; ritorna gli accumulatori."""
    Z, X = R.Z, R.X
    nodo, n, L = R.nodo, R.n, Z["L"]
    rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
    A = {"w": [FPC.w_di(rho, L)], "pr": [FPC.profondita(Z, rho, X["chi"])], "om": [], "mcf": []}
    mc_cur = [float(np.max(np.abs(X["chi"])))]
    somma, schi = np.zeros_like(Z["st"]["psi_h"]), np.zeros_like(X["chi"])
    A["S"], A["SC"] = {0: somma.copy()}, {0: schi.copy()}
    th = [0.0]
    t1 = time.time()

    def dopo(kk, prima):
        o = float(-np.angle(np.vdot(prima, Z["st"]["psi_h"])))
        A["om"].append(o)
        th[0] += o
        somma[...] += Z["st"]["psi_h"] * np.exp(1j * th[0])
        schi[...] += X["chi"]
        mc_cur.append(float(np.max(np.abs(X["chi"]))))
        if kk % OGNI_W == 0:
            r = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            A["w"].append(FPC.w_di(r, L))
            A["pr"].append(FPC.profondita(Z, r, X["chi"]))
        if kk % FIN == 0:
            A["S"][kk], A["SC"][kk] = somma.copy(), schi.copy()
            A["mcf"].append(max(mc_cur[1:]) if len(mc_cur) > 1 else mc_cur[0])
            mc_cur[:] = [mc_cur[-1]]
            if salva is not None:
                salva(kk)
        if stampa is not None and kk % 500 == 0:
            print("    k %d: w %.3f, max|chi| (la finestra) %.3f, la profondita' %+.3f, omega %+.6f (%.0f s)" % (kk, A["w"][-1], A["mcf"][-1], A["pr"][-1], o, time.time() - t1))
            sys.stdout.flush()
    D.ciclo(Z, R.C, R.P, R.Lp, X, ticks, dopo)
    return A


def noto():
    avvia()
    print("=" * 130)
    print("[M1519] I CASI NOTI DEL CORPO FUSO (la carta sez. 3-unetvicies): K0'', K0''-neg, K1'', K5, K6, KQ")
    print("=" * 130)
    S = serie_d1L()
    rif = {int(r[0]): r for r in S["serie"]}
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    f0, f1 = os.path.join(D1L, "stato_017750.npz"), os.path.join(D1L, "stato_018000.npz")
    PF.controlla(f1)
    with np.load(f1) as z:
        fin = {x: z[x].copy() for x in z.files if x != "meta"}
    print("  il riferimento: %s (%d chiavi); la partenza %s" % (f1, len(fin), f0))
    for caso in ("K0''", "K0''-neg", "K1''"):
        t1 = time.time()
        with GD.TC.scena() as Z:
            R = Ripresa10(Z, f0, 17750, "noto", scrivi_U=(caso != "K0''-neg"))
            if caso == "K1''":
                A = giro_pf(R, 250)
                dd = R.dati()
                diversi = [x for x in fin if not np.array_equal(np.asarray(dd[x]), fin[x])]
                esito("(K1'') il ciclo del punto fisso da stato_017750, 250 tick = d1L/stato_018000 AL BIT, ogni chiave (%d)" % len(fin), not diversi, "diverse: %s; %d omega, %d finestre" % (diversi, len(A["om"]), len(A["mcf"])))
                psi = np.asarray(fin["psi_h"])
                massa = float(np.sum(np.abs(psi) ** 2))
                Q = PF.leggi_Q()
                m2 = float(np.sum(np.abs(PF.trasforma(psi, Q, R.n, massa)) ** 2))
                esito("(KQ) la riproiezione Q_K della psi di stato_018000 alla sua massa ridà la massa entro 1e-12", abs(m2 / massa - 1.0) < TOL_MASSA, "massa %.10e, dopo %.10e, rel %.3e" % (massa, m2, m2 / massa - 1.0))
                m1 = float(np.sum(np.abs(PF.trasforma(psi, Q, R.n, 995010.8931463911)) ** 2))
                esito("(KQ-neg) DEVE FALLIRE: chiesta la massa di UN oggetto, la massa NON e' quella di riferimento", abs(m1 / massa - 1.0) > 0.1, "dopo %.6e, rapporto %.6f" % (m1, m1 / massa))
            else:
                r0 = R.misura(17750)
                if caso == "K0''":
                    esito("(carica) la riga della serie a k 17750 = quella di d1L/serie.json AL BIT", r0 == rif[17750], "%r" % r0[:3])
                R.gira(250)
                dd = R.dati()
                diversi = [x for x in fin if not np.array_equal(np.asarray(dd[x]), fin[x])]
                if caso == "K0''":
                    esito("(K0'') lo stato a k 18000 = d1L/stato_018000 AL BIT, ogni chiave (%d)" % len(fin), not diversi, "diverse: %s" % diversi)
                    ks = [int(r[0]) for r in R.serie]
                    esito("(K0'') la serie %d..%d (%d righe) = d1L/serie.json AL BIT" % (ks[0], ks[-1], len(ks)), all(r == rif[int(r[0])] for r in R.serie))
                    rel = max(abs(a - b) / abs(b) for j in range(2) for a, b in zip(R.om[j], S["omega"][j][11750:12000]))
                    nn = min(len(R.om[j]) for j in range(2))
                    esito("(K0'') omega dei tick 17751..18000 (%d), i due corpi: |d omega|/omega < 1e-12 (Luca 13:12)" % nn, nn == 250 and rel < TOL_OMEGA, "max rel %.3e" % rel)
                else:
                    esito("(K0''-neg) senza riscrivere geo.U lo stato a k 18000 e' DIVERSO da d1L/stato_018000", bool(diversi), "diverse: %s" % diversi)
            Z["metti"]()
        print("    (%s: %.0f s)" % (caso, time.time() - t1))
        sys.stdout.flush()
    base = [10.0 + 0.1 * i for i in range(24)]
    v = list(base)
    for c in (4, 14):
        for j, a_ in ((-3, 1.0), (-2, 2.0), (-1, 3.0), (0, 4.0), (1, 3.0), (2, 2.0), (3, 1.0)):
            v[c + j] = base[c + j] + 10.0 * a_
    Pp, kp, fonte = V2.periodo(v)
    esito("(K5) due picchi a 10 finestre (2500 tick): P 2500", Pp == 2500 and len(kp) == 2, "P %d, i picchi a k %s" % (Pp, kp))
    v1 = list(base)
    for j, a_ in ((-3, 1.0), (-2, 2.0), (-1, 3.0), (0, 4.0), (1, 3.0), (2, 2.0), (3, 1.0)):
        v1[9 + j] = base[9 + j] + 10.0 * a_
    _p1, kp1, fonte1 = V2.periodo(v1)
    esito("(K5) DEVE FALLIRE i due picchi: con un picco solo P e' il ripiego dichiarato", len(kp1) == 1 and fonte1.startswith("il ripiego"), fonte1)
    c = np.array([-100.0, -37.0, 5.0, 0.0])
    sc = np.zeros_like(c)
    for _ in range(2500):
        sc += c
    esito("(K6) la media di un chi costante (interi) su 2500 tick = lo stesso chi AL BIT", np.array_equal(sc / 2500.0, c), "%s" % (sc / 2500.0))
    fall = [k for k, v_ in OK.items() if not v_]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def corsa():
    avvia()
    assert not os.path.exists(os.path.join(D_S1, "stato_%06d.npz" % (K_DA + OGNI_STATO))), "%s c'e' gia': non si riscrive" % D_S1
    os.makedirs(D_S1, exist_ok=True)
    S = serie_d1L()
    f_da = os.path.join(D1L, "stato_%06d.npz" % K_DA)
    t1 = time.time()
    with GD.TC.scena() as Z:
        R = Ripresa10(Z, f_da, K_DA, "d1T")
        r0 = R.misura(K_DA)
        assert r0 == [r for r in S["serie"] if int(r[0]) == K_DA][0], "la riga a k %d NON e' quella di d1L/serie.json" % K_DA
        R.serie.append(r0)
        print("### [M1519] S1, d1''': da %s, %d tick (fino a k %d); la riga a k %d = d1L/serie.json AL BIT" % (f_da, K_A - K_DA, K_A, K_DA))
        sys.stdout.flush()

        def scrivi_serie(nome):
            f = os.path.join(D_S1, nome)
            open(f, "w", encoding="utf-8").write(json.dumps({"meta": R.meta, "serie": R.serie, "omega": R.om}))
            PF.firma(f)

        def salva(kk):
            if kk % OGNI_STATO:
                return
            fz = os.path.join(D_S1, "stato_%06d.npz" % kk)
            np.savez(fz, meta=np.array(json.dumps(dict(R.meta, k=kk))), **R.dati())
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")
            u = R.serie[-1]
            print("    k %d: y1 %+.4f y2 %+.4f; max|chi| %.4e (%.0f s)" % (kk, u[2], u[5], u[-1], time.time() - t1))
            sys.stdout.flush()
            if kk % OGNI_PARZIALE == 0:
                scrivi_serie("serie_parziale.json")
        R.gira(K_A - K_DA, salva)
        scrivi_serie("serie.json")
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_A - K_DA, time.time() - t1))
    ok = os.path.exists(os.path.join(D_S1, "stato_%06d.npz.sha1" % K_A))
    print("### stato_%06d.npz %s" % (K_A, "ESISTE" if ok else "### NON ESISTE"))
    return 0 if ok else 1


def puntofisso():
    avvia()
    assert not os.path.exists(D_S2), "%s c'e' gia': non si riscrive" % D_S2
    f_rif = os.path.join(D1L, "stato_%06d.npz" % K_DA)
    massa = PF.massa_di(f_rif)
    Q = PF.leggi_Q()
    print("### [M1519] S2, il punto fisso accoppiato 2M: %d giri da %d tick; la massa di riferimento %.10e (da %s)" % (GIRI, K_GIRO, massa, f_rif))
    sys.stdout.flush()
    f_part = f_rif
    for g in range(1, GIRI + 1):
        d = os.path.join(D_S2, "giro_%d" % g)
        os.makedirs(d)
        t1 = time.time()
        with GD.TC.scena() as Z:
            R = Ripresa10(Z, f_part, 0, "S2_giro_%d" % g, azzera_pi=True)
            res0 = float(R.C.residuo())
            print("### giro %d: la partenza %s (pi = 0); il residuo di Gauss %.3e" % (g, f_part, res0))
            sys.stdout.flush()

            def salva(k, d=d, R=R, g=g):
                PF.salva_stato(os.path.join(d, "stato_%06d.npz" % k), R.dati(), dict(R.meta, k=k, giro=g))
            salva(0)
            A = giro_pf(R, K_GIRO, salva, True)
            Z["metti"]()
        Pp, kp, fonte = V2.periodo(A["mcf"])
        ka, kb = K_GIRO - Pp, K_GIRO
        psi_medio = (A["S"][kb] - A["S"][ka]) / float(kb - ka)
        chi_medio = (A["SC"][kb] - A["SC"][ka]) / float(kb - ka)
        import gravita_due_corpi_misure as GM
        X6, m6 = GM.leggi(os.path.join(d, "stato_%06d.npz" % K_GIRO))
        dati = {x: X6[x] for x in X6}
        dati["psi_h"] = PF.trasforma(psi_medio, Q, R.n, massa)
        dati["chi"] = chi_medio
        dati["pi"] = np.zeros_like(X6["pi"])
        f_nuova = os.path.join(d, "partenza_giro_%d.npz" % (g + 1))
        PF.salva_stato(f_nuova, dati, dict(m6, giro=g + 1, finestra=[ka, kb], P=Pp))
        esce = {"giro": g, "partenza": f_part, "residuo_partenza": res0, "massa": massa, "w": A["w"], "maxchi_fin": A["mcf"], "profondita": A["pr"], "omega": A["om"],
                "P": Pp, "picchi_k": kp, "fonte": fonte, "finestra": [ka, kb], "partenza_nuova": f_nuova, "parametri": R.meta["parametri"]}
        f = os.path.join(d, "giro.json")
        open(f, "w", encoding="utf-8").write(json.dumps(esce))
        PF.firma(f)
        print("### giro %d: P %d (%s); i picchi a k %s; la finestra [%d, %d]; %d tick in %.0f s" % (g, Pp, fonte, kp, ka, kb, K_GIRO, time.time() - t1))
        sys.stdout.flush()
        f_part = f_nuova
    ok = all(os.path.exists(os.path.join(D_S2, "giro_%d" % g, "giro.json.sha1")) for g in range(1, GIRI + 1))
    print("### %d giri: %s" % (GIRI, "CHIUSI" if ok else "### NON TUTTI"))
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "puntofisso"))
    a = ap.parse_args(argv)
    return {"noto": noto, "corsa": corsa, "puntofisso": puntofisso}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
