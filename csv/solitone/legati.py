# -*- coding: utf-8 -*-
r"""**GLI OGGETTI LEGATI: LE CORSE LUNGHE** *(Luca `2026-11-15` `10:29`, parte B; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `23`)*.

    python csv/solitone/legati.py coppia --mondo GU --da 6000 --fino 18000 --registro legati-GU > <scratchpad>/legati_GU_06000.txt          (B1)
    python csv/solitone/legati.py coppia --mondo GUpi --da 2000 --fino 18000 --registro legati-GUpi > <scratchpad>/legati_GUpi_02000.txt    (B2)
    python csv/solitone/legati.py triangolo --da 2000 --fino 6000 --registro legati-t120 > <scratchpad>/legati_t120_02000.txt              (B3, dopo triangolo_120.py)
    python csv/solitone/legati.py lettura > doc/referti_l2/mattone/legati_lettura.txt                                                      (B5)
    (i referti: doc/referti_l2/mattone/legati_<mondo>_<da>.txt; se il tetto ferma una corsa, si riparte con --da l'ultimo stato salvato)

### **`coppia`** *(B1, B2)*: **la scena di C35-pi, il bordo da `R_A 60`, G+U, il tick di `mattone_cottura.Corsa`, le misure di `coppia_lunga.py`** *(ogni `50` tick `d` dai semipiani, il baricentro, il raggio entro `60`,
`A2`, la massa, la massa oltre `R_A`, i centri delle culle, Gauss ogni `250`; il picco a ogni tick; le mappe ogni `100`)*. ### **La partenza:** **B1 da `coppia_lunga_06000`** *(il DEVE della ripartenza da `05000`:
`1000` tick, gli stati di `coppia_lunga` sono ogni `1000`: MIA LETTURA di «gli ultimi `50` tick», dichiarata)*; **B2 da `coppiaGUpi_L162_02000`** *(il DEVE da `01500`: `500` tick, gli stati ogni `500`; dichiarato)*;
**da uno stato di QUESTO file: `50` tick** *(gli stati a `k % 1000 == 0` E a `k % 1000 == 950`)*.
### **`triangolo`** *(B3, la fase 2)*: **la scena di S162, il bordo da `R_A 60`, G+U; le misure di (T-fase)** *(lati, masse, raggi, centri ogni `50`; il picco di ogni solitone a ogni tick)* **e quelle di `triangolo_120.py`**
*(il giro e la densita' al centro ogni `100`; la massa totale e oltre `R_A` ogni `50`)*; **le mappe ogni `60`** *(Luca `10:29`: dopo `2000`)*; **la partenza da `triangolo_t120_02000`, il DEVE da `01950`: `50` tick.**
### **B4** *(Luca `10:29`)*: **la massa oltre `R_A` sopra `1e-4` relativo: scritta accanto alla distanza, la corsa continua; sopra `1e-2`: L'ARRESTO** *(il porto e' troppo piccolo: si scrive; NON e' un FERMO)*.
### **Il tetto `28800 s`** *(`MT.TETTO_S`, Luca `10:10`)*; **lo stato ogni `1000` tick** *(e `50` prima)*.
### **DEVE:** **ogni ripartenza rifa' gli ultimi tick AL BIT** *(esclusa `h_int`)*; **Gauss sotto `1e-10` a ogni controllo** *(`L 162`)*; **per la coppia: la massa persa = la massa uscita dal bordo entro `1e-6`** *(come `coppia_lunga`)*.
"""
import argparse
import glob
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
import mattone_triangolo as MTR  # noqa: E402
import triangolo_120 as T120  # noqa: E402
import triangolo_video as TV  # noqa: E402

CORSA_C, T_C = "C35-pi", 60000                 # ### la scena di B2 (coppia_lunga)
R_A = 60.0                                     # ### Luca 15:49
OGNI, OGNI_STATO, PRIMA = 50, 1000, 50         # ### lo stato a k % 1000 == 0 e a k % 1000 == 950
OGNI_MAPPA_C, OGNI_MAPPA_T = 100, 60           # ### le mappe: la coppia come coppia_lunga; il triangolo dopo 2000 ogni 60 (Luca 10:29)
R_FORMA = 60.0
AVVISO, ARRESTO = 1e-4, 1e-2                   # ### B4
PARTENZE = {("GU", 6000): ("coppia_lunga_06000", "coppia_lunga_05000", 1000),
            ("GUpi", 2000): ("coppiaGUpi_L162_02000", "coppiaGUpi_L162_01500", 500),
            ("t120", 2000): ("triangolo_t120_02000", "triangolo_t120_01950", 50)}
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  DEVE PASSARE: %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def sorgente(nome, k):
    """### `(lo stato a k, lo stato prima, i tick del DEVE)`: uno stato di questo file *(50 tick)*, o le partenze dichiarate."""
    f = os.path.join(MT.DIR_E, "legati_%s_%05d.npz" % (nome, k))
    g = os.path.join(MT.DIR_E, "legati_%s_%05d.npz" % (nome, k - PRIMA))
    if os.path.exists(f) and os.path.exists(g):
        return f, g, PRIMA
    a, b, n = PARTENZE[(nome, k)]
    return os.path.join(MT.DIR_E, a + ".npz"), os.path.join(MT.DIR_E, b + ".npz"), n


def carica(Z, f, rho_c, e):
    import _u1_prototipo as U1
    with np.load(f) as d:
        Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
        A, E = d["campo_A"].copy(), d["campo_E"].copy()
        meta = json.loads(str(d["meta"])) if "meta" in d.files else {}
    C = MT.Campi(Z, "MGU", rho_c, e)
    C.campo.A[...] = A
    C.campo.E[...] = E
    C.campo.e = e
    C.e_prec = e
    U1.scrivi_U(Z["mot"], C.campo)                         # ### d9318470: l'U che avvolto lascia dopo l'ultimo tick
    return C, meta


def uguale(Z, C, f):
    with np.load(f) as d:
        div = [x for x in Z["chiavi"] if x not in CU.CHIAVI_SERVIZIO and not np.array_equal(Z["st"][x], d[x])]
        div += [x for x, a in (("campo_A", C.campo.A), ("campo_E", C.campo.E)) if not np.array_equal(a, d[x])]
    return div


def avvia_presidi():
    import _presidio
    for m in ("mattone", "mattone_cottura", "mattone_cottura_U", "mattone_triangolo", "triangolo_120", "triangolo_video"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)


# =====================================================================================
#   B1, B2: LA COPPIA
# =====================================================================================
def coppia(mondo, k_da, k_fino, reg):
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    avvia_presidi()
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    f_da, f_prima, n_deve = sorgente(mondo, k_da)
    print("=" * 130)
    print("GLI OGGETTI LEGATI (Luca 10:29, %s): la coppia %s da k %d a k %d (%s); la scena di %s, il bordo da R_A %g, G+U; il tetto %g s; B4: oltre R_A %g scritto, %g l'ARRESTO"
          % ("B1" if mondo == "GU" else "B2", mondo, k_da, k_fino, f_da, CORSA_C, R_A, MT.TETTO_S, AVVISO, ARRESTO))
    print("=" * 130)
    with MT.scena(CORSA_C, T_C) as Z:
        L, n, righe, m1, m2 = Z["L"], Z["n"], Z["righe"], Z["m1"], Z["m2"]
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], R_A, Z["bordo"]["g_max"])[0]
        xs = TO.scarti(m1, m2, c0[0], c0[1], L)[:, 0]
        r_c0 = np.hypot(*TO.scarti(m1, m2, c0[0], c0[1], L).T[:2])

        def nuova_corsa(C):
            R = CT.Corsa(Z, C)
            a, b = CC.centri_semipiani(MT.rho_di(Z), m1, m2, L, xs, 0.0)
            R.etichette([a, b])
            return R
        # ---------------------------------------------------------------- il DEVE della ripartenza
        C, _m = carica(Z, f_prima, rho_c, e)
        k_prima = k_da - n_deve
        R = nuova_corsa(C)
        R.inizio(k_prima)
        for k in range(k_prima + 1, k_da + 1):
            R.passo(k, T_C + k, 1.0, e)
            if (k - k_prima) % CT.OGNI == 0:
                a, b = CC.centri_semipiani(MT.rho_di(Z), m1, m2, L, xs, 0.0)
                R.etichette([a, b])
        div = uguale(Z, C, f_da)
        esito("la ripartenza da %s per %d tick = %s AL BIT (esclusa h_int)" % (os.path.basename(f_prima), n_deve, os.path.basename(f_da)), not div, "diverse: %s" % div)
        if div:
            print("ESITO: ### FERMO: la ripartenza NON e' esatta")
            return 1
        # ---------------------------------------------------------------- la corsa
        C, _m = carica(Z, f_da, rho_c, e)
        R = nuova_corsa(C)
        S = {x: [] for x in ("k", "d", "b1", "b2", "raggio", "A2", "M", "fuori", "gauss", "u1_A", "u2_A", "u1_B", "u2_B")}
        PK, MP = [], {"k": [], "rho": [], "dphi": [], "E": []}
        fine = {"perche": "finita"}

        def misura(k):
            rho = MT.rho_di(Z)
            PK.append(float(rho.max()))
            fare, mappa = (k - k_da) % OGNI == 0, (k - k_da) % OGNI_MAPPA_C == 0
            if fare or mappa:
                phi0 = BO.c_di(T_C + k, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
                dphi = np.sqrt(np.sum(np.abs(Z["st"]["phi_h"] - phi0).reshape(n * 6, -1) ** 2, axis=1))
                dphi_n = np.sqrt(np.sum(dphi[righe] ** 2, axis=1))
            if fare:
                a, b = CC.centri_semipiani(rho, m1, m2, L, xs, 0.0)
                bc = TO.centro(rho, m1, m2, L)[:2]
                pos = TO.scarti(m1, m2, bc[0], bc[1], L)[:, :2]
                r = np.hypot(pos[:, 0], pos[:, 1])
                th = np.arctan2(pos[:, 1], pos[:, 0])
                dentro = r <= R_FORMA
                S["k"].append(k)
                S["d"].append(float(np.hypot(*CC.vettore(a, b, L))))
                S["b1"].append(bc[0])
                S["b2"].append(bc[1])
                S["raggio"].append(float(math.sqrt(np.sum(rho[dentro] * r[dentro] ** 2) / np.sum(rho[dentro]))))
                S["A2"].append(float(abs(np.sum(rho[dentro] * np.exp(2j * th[dentro]))) / np.sum(rho[dentro])))
                S["M"].append(float(rho.sum()))
                S["fuori"].append(float(rho[r_c0 > R_A].sum() / rho.sum()))
                S["gauss"].append(C.residuo() if (k - k_da) % MT.OGNI_GAUSS == 0 else float("nan"))
                msk = xs < 0.0
                for q, sel in (("A", msk), ("B", ~msk)):
                    u = TO.centro(np.where(sel, dphi_n, 0.0), m1, m2, L)[:2]
                    S["u1_" + q].append(u[0])
                    S["u2_" + q].append(u[1])
                if (k - k_da) % 500 == 0:
                    print("    k %5d  d %.4f  il raggio %.4f  A2 %.4f  il picco %.4e  la massa %.6e  oltre R_A %.3e%s  Gauss %s  (%.0f s)" % (k, S["d"][-1], S["raggio"][-1], S["A2"][-1], PK[-1], S["M"][-1], S["fuori"][-1],
                          "  ### OLTRE %g (B4)" % AVVISO if S["fuori"][-1] > AVVISO else "", "%.2e" % S["gauss"][-1] if S["gauss"][-1] == S["gauss"][-1] else "--", time.time() - t00))
                    sys.stdout.flush()
                if S["fuori"][-1] > ARRESTO:
                    fine["perche"] = "L'ARRESTO (B4): la massa oltre R_A %.3e > %g a k %d, d %.4f: il porto e' troppo piccolo" % (S["fuori"][-1], ARRESTO, k, S["d"][-1])
            if mappa:
                MP["k"].append(k)
                MP["rho"].append(rho.astype(np.float32))
                MP["dphi"].append(dphi_n.astype(np.float32))
                MP["E"].append(np.sqrt(np.sum(C.campo.E.reshape(n, 3) ** 2, axis=1)).astype(np.float32))
            if k > k_da and (k % OGNI_STATO == 0 or k % OGNI_STATO == OGNI_STATO - PRIMA):
                a, b = CC.centri_semipiani(rho, m1, m2, L, xs, 0.0)
                T120.salva_stato(Z, C, k, T_C + k, "legati_%s" % mondo, "csv/solitone/legati.py", [list(map(float, a)), list(map(float, b))])
        R.inizio(k_da)
        misura(k_da)
        t1 = t_tappa = time.time()
        for k in range(k_da + 1, k_fino + 1):
            R.passo(k, T_C + k, 1.0, e)
            if (k - k_da) % CT.OGNI == 0:
                a, b = CC.centri_semipiani(MT.rho_di(Z), m1, m2, L, xs, 0.0)
                R.etichette([a, b])
            misura(k)
            adesso = time.time()
            if reg and adesso - t_tappa >= MT.TAPPA_S:
                MT.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / (k - k_da), MT.memoria_gb()))
                t_tappa = adesso
            if fine["perche"] != "finita":
                break
            if adesso - t1 > MT.TETTO_S:
                fine["perche"] = "il tetto di %g s a k %d (si riparte da %d)" % (MT.TETTO_S, k, (k // OGNI_STATO) * OGNI_STATO)
                break
        print("-" * 130)
        print("### %d tick in %.0f s; %s" % (k - k_da, time.time() - t1, fine["perche"]))
        R.tabella(["A", "B"])
        T = {x: np.array(v) for x, v in R.T.items()}
        bordoM = float(np.sum(T["Mp"] - T["Md"]))
        geo = T120.geometria(Z)
    np.savez_compressed(os.path.join(MT.DIR_REF, "legati_%s_serie_%05d.npz" % (mondo, k_da)), picco=np.array(PK), **{x: np.array(v) for x, v in S.items()})
    f = os.path.join(MT.DIR_REF, "legati_%s_mappe_%05d.npz" % (mondo, k_da))
    np.savez_compressed(f, tick=np.array(MP["k"], dtype=np.int32), rho=np.stack(MP["rho"]), dphi=np.stack(MP["dphi"]), E=np.stack(MP["E"]), **geo)
    print("### LE MAPPE: %d fotogrammi in %s, %.1f MB" % (len(MP["k"]), f, os.path.getsize(f) / 1e6))
    d = np.array(S["d"])
    fu = np.array(S["fuori"])
    print("### d da %.4f a %.4f (il minimo %.4f a k %d, il massimo %.4f a k %d); la massa oltre R_A il massimo %.3e (oltre %g dal tick %s)" % (d[0], d[-1], d.min(), S["k"][int(d.argmin())], d.max(), S["k"][int(d.argmax())],
          fu.max(), AVVISO, S["k"][int(np.argmax(fu > AVVISO))] if (fu > AVVISO).any() else "mai"))
    persa = S["M"][0] - S["M"][-1]
    print("### LA MASSA: persa %.6e, uscita dal bordo %.6e, la differenza relativa %.3e" % (persa, bordoM, abs(persa - bordoM) / S["M"][0]))
    g = np.array(S["gauss"])
    g = g[g == g]
    esito("Gauss sotto %g a ogni controllo (L 162)" % MT.TOLL_GAUSS, len(g) > 0 and float(g.max()) < MT.TOLL_GAUSS, "il massimo %.3e" % float(g.max()))
    esito("la massa persa = la massa uscita dal bordo entro 1e-6 relativo", abs(persa - bordoM) / S["M"][0] <= 1e-6, "%.3e" % (abs(persa - bordoM) / S["M"][0]))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, fine["perche"], time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   B3: IL TRIANGOLO A 120 GRADI, LA FASE 2
# =====================================================================================
def triangolo(k_da, k_fino, reg):
    from solitone import bordo as BO
    from solitone import toro as TO
    avvia_presidi()
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    f_da, f_prima, n_deve = sorgente("t120", k_da)
    print("=" * 130)
    print("GLI OGGETTI LEGATI (Luca 10:29, B3): il triangolo a 120 gradi da k %d a k %d (%s); la scena di S162, il bordo da R_A %g, G+U; le mappe ogni %d; il tetto %g s; B4: oltre R_A %g scritto, %g l'ARRESTO"
          % (k_da, k_fino, f_da, MTR.R_A_SCENA, OGNI_MAPPA_T, MT.TETTO_S, AVVISO, ARRESTO))
    print("=" * 130)

    def centri_di(f, k):
        with np.load(f) as d:
            meta = json.loads(str(d["meta"]))
        if meta.get("centri"):
            return [list(map(float, c)) for c in meta["centri"]]
        s = np.load(os.path.join(MT.DIR_REF, "triangolo_t120_serie.npz"))
        j = int(np.nonzero(s["k"] == k)[0][0])
        return [[float(s["c1_" + q][j]), float(s["c2_" + q][j])] for q in "ABC"]
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L = Z["L"]
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
        # ---------------------------------------------------------------- il DEVE della ripartenza
        C, _m = carica(Z, f_prima, rho_c, e)
        k_prima = k_da - n_deve
        R = CT.Corsa(Z, C)
        cen = centri_di(f_prima, k_prima)
        R.etichette(cen)
        R.inizio(k_prima)
        for k in range(k_prima + 1, k_da + 1):
            R.passo(k, t0 + k, 1.0, e)
            cen, _lab = MTR.centri_pezzi(Z, MT.rho_di(Z), cen)
            if (k - k_prima) % CT.OGNI == 0:
                R.etichette(cen)
        div = uguale(Z, C, f_da)
        esito("la ripartenza da %s per %d tick = %s AL BIT (esclusa h_int)" % (os.path.basename(f_prima), n_deve, os.path.basename(f_da)), not div, "diverse: %s" % div)
        if div:
            print("ESITO: ### FERMO: la ripartenza NON e' esatta")
            return 1
        # ---------------------------------------------------------------- la corsa
        C, _m = carica(Z, f_da, rho_c, e)
        R = CT.Corsa(Z, C)
        cen = centri_di(f_da, k_da)
        R.etichette(cen)
        nomi = ("A", "B", "C")
        S = {x: [] for x in ("k", "l_AB", "l_BC", "l_CA", "gauss") + tuple("%s_%s" % (q, nn) for q in ("M", "raggio", "c1", "c2") for nn in nomi)}
        PK = {nn: [] for nn in nomi}
        fine = {"perche": "finita"}
        st = {"cen": cen}

        def misura(k):
            rho = MT.rho_di(Z)
            st["cen"], lab = MTR.centri_pezzi(Z, rho, st["cen"])
            for j, nn in enumerate(nomi):
                PK[nn].append(float(rho[lab == j].max()))
            if (k - k_da) % OGNI == 0:
                c_ = st["cen"]
                S["k"].append(k)
                for j, nn in enumerate(nomi):
                    S["M_" + nn].append(float(rho[lab == j].sum()))
                    S["raggio_" + nn].append(MTR.MR.raggio(Z, rho, c_[j]))
                    S["c1_" + nn].append(c_[j][0])
                    S["c2_" + nn].append(c_[j][1])
                S["l_AB"].append(MT.distanza(L, c_[0], c_[1]))
                S["l_BC"].append(MT.distanza(L, c_[1], c_[2]))
                S["l_CA"].append(MT.distanza(L, c_[2], c_[0]))
                S["gauss"].append(C.residuo() if (k - k_da) % MT.OGNI_GAUSS == 0 else float("nan"))
            T120.misura_extra(Z, C, k, t0 + k, R.lab, R.n_sol, (lambda kk, tt: TV.CorsaVideo.foto(R, kk, tt)) if (k - k_da) % OGNI_MAPPA_T == 0 else None, (k - k_da) % T120.OGNI_GIRO == 0)
            if (k - k_da) % OGNI == 0:
                fu = T120.GIRO["fuori"][-1]
                if (k - k_da) % 500 == 0:
                    print("    k %5d  lati %.4f %.4f %.4f  masse %s  raggi %s  oltre R_A %.3e%s  Gauss %s  (%.0f s)" % (k, S["l_AB"][-1], S["l_BC"][-1], S["l_CA"][-1], " ".join("%.6e" % S["M_" + nn][-1] for nn in nomi),
                          " ".join("%.4f" % S["raggio_" + nn][-1] for nn in nomi), fu, "  ### OLTRE %g (B4)" % AVVISO if fu > AVVISO else "", "%.2e" % S["gauss"][-1] if S["gauss"][-1] == S["gauss"][-1] else "--", time.time() - t00))
                    sys.stdout.flush()
                if fu > ARRESTO:
                    fine["perche"] = "L'ARRESTO (B4): la massa oltre R_A %.3e > %g a k %d, i lati %.4f %.4f %.4f: il porto e' troppo piccolo" % (fu, ARRESTO, k, S["l_AB"][-1], S["l_BC"][-1], S["l_CA"][-1])
            if k > k_da and (k % OGNI_STATO == 0 or k % OGNI_STATO == OGNI_STATO - PRIMA):
                T120.salva_stato(Z, C, k, t0 + k, "legati_t120", "csv/solitone/legati.py", [list(map(float, c)) for c in st["cen"]])
        R.inizio(k_da)
        misura(k_da)
        t1 = t_tappa = time.time()
        for k in range(k_da + 1, k_fino + 1):
            R.passo(k, t0 + k, 1.0, e)
            if (k - k_da) % CT.OGNI == 0:
                R.etichette(st["cen"])
            misura(k)
            adesso = time.time()
            if reg and adesso - t_tappa >= MT.TAPPA_S:
                MT.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / (k - k_da), MT.memoria_gb()))
                t_tappa = adesso
            if fine["perche"] != "finita":
                break
            if adesso - t1 > MT.TETTO_S:
                fine["perche"] = "il tetto di %g s a k %d (si riparte da %d)" % (MT.TETTO_S, k, (k // OGNI_STATO) * OGNI_STATO)
                break
        print("-" * 130)
        print("### %d tick in %.0f s; %s" % (k - k_da, time.time() - t1, fine["perche"]))
        R.tabella(list(nomi))
        geo = T120.geometria(Z)
    np.savez_compressed(os.path.join(MT.DIR_REF, "legati_t120_serie_%05d.npz" % k_da), **{("picco_" + nn): np.array(v) for nn, v in PK.items()}, **{x: np.array(v) for x, v in S.items()})
    np.savez_compressed(os.path.join(MT.DIR_REF, "legati_t120_giro_%05d.npz" % k_da), **{x: np.array(v) for x, v in T120.GIRO.items()})
    FO = TV.FOTO
    f = os.path.join(MT.DIR_REF, "legati_t120_mappe_%05d.npz" % k_da)
    np.savez_compressed(f, tick=np.array(FO["k"], dtype=np.int32), rho=np.stack(FO["rho"]), dphi=np.stack(FO["dphi"]), E=np.stack(FO["E"]), centri=np.stack(FO["centri"]), **geo)
    print("### LE MAPPE: %d fotogrammi in %s, %.1f MB" % (len(FO["k"]), f, os.path.getsize(f) / 1e6))
    lm = (np.array(S["l_AB"]) + np.array(S["l_BC"]) + np.array(S["l_CA"])) / 3.0
    print("### il lato medio da %.4f a %.4f (il minimo %.4f a k %d, il massimo %.4f a k %d); la massa oltre R_A il massimo %.3e" % (lm[0], lm[-1], lm.min(), S["k"][int(lm.argmin())], lm.max(), S["k"][int(lm.argmax())],
          max(T120.GIRO["fuori"])))
    g = np.array(S["gauss"])
    g = g[g == g]
    esito("Gauss sotto %g a ogni controllo (L 162)" % MT.TOLL_GAUSS, len(g) > 0 and float(g.max()) < MT.TOLL_GAUSS, "il massimo %.3e" % float(g.max()))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, fine["perche"], time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   B5: LA LETTURA
# =====================================================================================
LISCIA, FINESTRA = 11, 20             # ### le inversioni (mie): la media mobile su 11 punti (550 tick), l'estremo il minimo/massimo entro +- 20 punti (1000 tick)
P2_DA, P2_A, P1_EQ = 44.0, 49.0, 29.0  # ### le previsioni del guardiano (10:29)


def inversioni(k, y):
    """### Gli estremi della serie lisciata *(mia definizione, dichiarata)*: `[(tick, valore lisciato, 'min'|'max')]`."""
    k, y = np.asarray(k, dtype=float), np.asarray(y, dtype=float)
    if len(y) < 2 * FINESTRA + LISCIA:
        return []
    ys = np.convolve(y, np.ones(LISCIA) / LISCIA, mode="same")
    h = LISCIA // 2
    out = []
    for i in range(FINESTRA + h, len(y) - FINESTRA - h):
        w = ys[i - FINESTRA:i + FINESTRA + 1]
        if ys[i] == w.min() and ys[i] < ys[i - FINESTRA] and ys[i] < ys[i + FINESTRA]:
            out.append((k[i], ys[i], "min"))
        elif ys[i] == w.max() and ys[i] > ys[i - FINESTRA] and ys[i] > ys[i + FINESTRA]:
            out.append((k[i], ys[i], "max"))
    return out


def serie_unita(pezzi):
    """### I pezzi `(k, y)` uniti in ordine di tick, senza ripetere un tick."""
    kk, yy = [], []
    for k, y in pezzi:
        for a, b in zip(k, y):
            if kk and a <= kk[-1]:
                continue
            kk.append(float(a))
            yy.append(float(b))
    return np.array(kk), np.array(yy)


def leggi_inversioni(nome, k, y):
    inv = inversioni(k, y)
    print("    %s: da %.4f (k %d) a %.4f (k %d); le inversioni (la serie lisciata): %s" % (nome, y[0], k[0], y[-1], k[-1], ["%s %.4f a k %d" % (t, v, kk) for kk, v, t in inv] or "nessuna"))
    if len(inv) >= 2:
        dt = np.diff([x[0] for x in inv])
        print("      il periodo (2 x la media fra due inversioni successive): %.0f tick (le meta' %s)" % (2.0 * dt.mean(), [int(x) for x in dt]))
    return inv


def lettura():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(__file__)
    ref = MT.DIR_REF

    def pezzi(nome):
        return sorted(glob.glob(os.path.join(ref, "legati_%s_serie_*.npz" % nome)))
    print("=" * 130)
    print("GLI OGGETTI LEGATI, LA LETTURA (Luca 10:29, B5): la distanza (i lati) nel tempo, le inversioni, il periodo, le previsioni P1-P3; le inversioni sulla serie lisciata (11 punti) entro +- 1000 tick (mie)")
    print("=" * 130)
    letture = {}
    for mondo, prima, P in (("GU", ("coppia_GU_L162_serie.npz", "coppia_lunga_serie.npz"), "P1"), ("GUpi", ("coppia_GUpi_L162_serie.npz",), "P2")):
        pz = []
        for f in prima:
            s = np.load(os.path.join(ref, f))
            pz.append((s["t"] if "t" in s.files else s["k"], s["d"]))
        fu = []
        for f in pezzi(mondo):
            s = np.load(f)
            pz.append((s["k"], s["d"]))
            fu.append(float(np.max(s["fuori"])))
        k, d = serie_unita(pz)
        print("### %s (%s; i pezzi %s)" % ("B1, B2 in fase" if mondo == "GU" else "B2, B2-pi in opposizione", P, [os.path.basename(x) for x in pezzi(mondo)]))
        letture[mondo] = leggi_inversioni("d", k, d)
        print("      la massa oltre R_A nei pezzi lunghi: il massimo %s" % ("%.3e" % max(fu) if fu else "--"))
    # ---------------------------------------------------------------- B3
    pz, gz = [], []
    s0 = np.load(os.path.join(ref, "triangolo_t120_serie.npz"))
    lm0 = (np.array(s0["l_AB"]) + np.array(s0["l_BC"]) + np.array(s0["l_CA"])) / 3.0
    pz.append((s0["k"], lm0))
    for f in pezzi("t120"):
        s = np.load(f)
        pz.append((s["k"], (np.array(s["l_AB"]) + np.array(s["l_BC"]) + np.array(s["l_CA"])) / 3.0))
    k3, lm = serie_unita(pz)
    print("### B3, IL TRIANGOLO A 120 GRADI (P3)")
    letture["t120"] = leggi_inversioni("il lato medio", k3, lm)
    gfiles = [os.path.join(ref, "triangolo_t120_giro.npz")] + sorted(glob.glob(os.path.join(ref, "legati_t120_giro_*.npz")))
    G = {"k": [], "grande": [], "somma": [], "dens": [], "comp": [], "fuori": []}
    for f in gfiles:
        g = np.load(f)
        for i, kk in enumerate(g["k"]):
            if G["k"] and kk <= G["k"][-1]:
                continue
            G["k"].append(int(kk))
            G["grande"].append(float(g["grande"][i]))
            G["somma"].append(float(g["somma"][i]))
            G["dens"].append(float(g["dens"][i]))
            G["comp"].append(np.rint(g["comp"][i]).astype(int))
        G["fuori"].append(float(np.max(g["fuori"])))
    print("    IL GIRO DELLA FASE (ogni %d tick; mostrati ogni 500): la piu' grande, la somma delle 12, quante delle 12 a +1" % T120.OGNI_GIRO)
    for i, kk in enumerate(G["k"]):
        if kk % 500 == 0:
            print("      k %5d: la piu' grande %+.2f; la somma %+.2f; a +1 %2d delle 12; la densita' al centro %.4e" % (kk, G["grande"][i], G["somma"][i], int((G["comp"][i] == 1).sum()), G["dens"][i]))
    resta = bool(len(G["grande"]) and np.all(np.rint(G["grande"]) == 1))
    print("      -> il giro della piu' grande %s" % ("RESTA +1 a ogni controllo" if resta else "### NON resta +1 (dal tick %d)" % next(kk for kk, g in zip(G["k"], G["grande"]) if int(np.rint(g)) != 1)))
    # la densita' al centro contro (T-fase): il video (0-2000, ogni 20) e il trifoglio (2000-6000, ogni 100)
    rap = []
    for fm in ("triangolo_video_mappe.npz", "triangolo_trifoglio_mappe.npz"):
        mp = np.load(os.path.join(ref, fm))
        tk = np.array(mp["tick"])
        m1, m2, L = np.array(mp["m1"], dtype=float), np.array(mp["m2"], dtype=float), int(mp["L"])
        for i, kk in enumerate(G["k"]):
            jv = np.nonzero(tk == kk)[0]
            if not len(jv) or (rap and kk <= rap[-1][0]):
                continue
            c3 = np.asarray(mp["centri"][jv[0]], dtype=float)
            dd = np.hypot(*TO.scarti(m1, m2, c3[:, 0].mean(), c3[:, 1].mean(), L).T[:2])
            dv = float(np.asarray(mp["rho"][jv[0]], dtype=float)[dd <= T120.R_DISCO].mean())
            rap.append((kk, G["dens"][i], dv, G["dens"][i] / dv))
    print("    LA DENSITA' AL CENTRO contro (T-fase) agli stessi tick (il video fino a 2000, il trifoglio dopo; mostrati ogni 500): T120, (T-fase), il rapporto")
    for kk, a, b, q in rap:
        if kk % 500 == 0:
            print("      k %5d: %.4e  %.4e  %.4f" % (kk, a, b, q))
    bassa = bool(rap and all(q < 0.5 for _k, _a, _b, q in rap))
    print("      -> %s (la soglia mia, sez. 23: sotto la meta' a ogni controllo); il rapporto da %.4f a %.4f, il massimo %.4f" % ("MOLTO PIU' BASSA" if bassa else "### NON sempre sotto la meta'", rap[0][3], rap[-1][3], max(q for *_x, q in rap)) if rap else "      -> nessun tick comune")
    print("    la massa oltre R_A: il massimo %.3e" % max(G["fuori"]))
    # ---------------------------------------------------------------- le previsioni
    print("-" * 130)
    print("### LE PREVISIONI (del guardiano, 10:29, scritte PRIMA); un risultato diverso: una SORPRESA")
    inv = letture["GU"]
    dopo = [x for x in inv if x[0] >= 4000]
    eq = np.mean([x[1] for x in dopo]) if dopo else float("nan")
    print("    (P1) B2 OSCILLA (almeno due inversioni dal k 4000), l'equilibrio intorno a %g: le inversioni %d; l'equilibrio (la media degli estremi) %.3f -> %s" % (P1_EQ, len(dopo), eq,
          "CONFERMATA (che OSCILLA)" if len(dopo) >= 2 else "### NON CONFERMATA: una SORPRESA"))
    inv = letture["GUpi"]
    mx = [x for x in inv if x[2] == "max"]
    print("    (P2) B2-pi si ferma fra %g e %g e torna indietro: %s -> %s" % (P2_DA, P2_A, ("il primo massimo %.3f a k %d" % (mx[0][1], mx[0][0])) if mx else "nessun massimo",
          "CONFERMATA" if (mx and P2_DA <= mx[0][1] <= P2_A) else ("### NON CONFERMATA: si ferma fuori dall'intervallo (una SORPRESA)" if mx else "### NON CONFERMATA (nessuna inversione)")))
    inv = letture["t120"]
    mx = [x for x in inv if x[2] == "max"]
    allarga = lm[-1] > lm[0]
    print("    (P3) il triangolo SI ALLARGA: %s (il lato medio da %.4f a %.4f); NESSUNA fusione: il lato medio minimo %.4f; il VORTICE: il giro %s, la densita' %s; si ferma fra %g e %g: %s"
          % ("si'" if allarga else "### NO", lm[0], lm[-1], lm.min(), "resta" if resta else "### NON resta", "molto piu' bassa" if bassa else "### non sempre", P2_DA, P2_A,
             ("il primo massimo %.3f a k %d" % (mx[0][1], mx[0][0])) if mx else "nessun massimo"))
    print("=" * 130)
    return 0


def main(argv):
    if argv and argv[0] == "lettura":
        return lettura()
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("coppia", "triangolo"))
    ap.add_argument("--mondo", choices=("GU", "GUpi"))
    ap.add_argument("--da", type=int, required=True)
    ap.add_argument("--fino", type=int, required=True)
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.azione == "coppia":
        assert x.mondo, "--mondo GU|GUpi"
        return coppia(x.mondo, x.da, x.fino, x.registro)
    return triangolo(x.da, x.fino, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
