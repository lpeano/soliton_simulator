# -*- coding: utf-8 -*-
r"""**IL TRIFOGLIO LUNGO: SI FERMA COME UN OGGETTO NUOVO?** *(Luca `2026-11-14` `23:32`, L2-L4; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `21`)*.

    python csv/solitone/trifoglio.py corsa --registro trifoglio > <scratchpad>/trifoglio.txt        (poi doc/referti_l2/mattone/trifoglio.txt; le mappe in triangolo_trifoglio_mappe.npz)

### **La corsa del video** *(`triangolo_video.py`: (T-fase) col mattone di `L 162`, la scena di S162, il bordo da `60`, G+U)* **PROSEGUE dal suo ultimo stato** *(`triangolo_video_02000`; il caricamento che ricostruisce
`U` dal campo, `d9318470`)* **per `4000` tick in piu'** *(in tutto `6000`)*, **col tick di `mattone_cottura.Corsa`.**
### **DEVE** *(la ripartenza; MIA LETTURA del mandato: gli stati sono ogni `500` tick)*: **da `triangolo_video_01500`, `500` tick = `triangolo_video_02000` AL BIT** *(esclusa `h_int`)*.
### **L3, ogni `50` tick:** **il baricentro; il raggio di tutta la materia** *(`sqrt(somma rho r^2 / somma rho)` entro `60` nodi dal baricentro)*; **la componente a TRE punte `A3 = |somma rho e^{3 i theta}| / somma rho`**
*(entro `60`)*; **i centri dei tre solitoni** *(il centro periodico di `rho` sul pezzo di ciascuno)* **e delle tre CULLE** *(il centro di `|phi - phi0|` sullo stesso pezzo)*; **il campo U lontano: su un anello a `40`-`50` nodi
dal baricentro, la media di `|E|` e `|somma |E| e^{3 i theta}| / somma |E|`.** **Il picco a ogni tick; le tre mappe ogni `100` tick; lo stato ogni `1000` su E:.**
### **L4, la lettura** *(le soglie MIE dove il mandato non le dice)*: **«UN OGGETTO NUOVO CON LA SUA FORMA» se `A3` nell'ultima finestra di `1000` tick resta almeno il `25%` di quella della prima, e la forma**
*(`A3` e il raggio)* **cambia meno del `2%` fra le ultime due finestre; «SI ARROTONDA» se `A3` scende sotto il `25%`; «NON SI FERMA» se la forma cambia di piu'.**
"""
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

K_DA, N_PIU, N_DEVE = 2000, 4000, 500
OGNI, OGNI_MAPPA, OGNI_STATO = 50, 100, 1000
R_FORMA, ANELLO = 60.0, (40.0, 50.0)
RESTA, CAMBIA = 0.25, 0.02
FIN = 1000


def carica(Z, k, rho_c, e):
    import _u1_prototipo as U1
    f = os.path.join(MT.DIR_E, "triangolo_video_%05d.npz" % k)
    with np.load(f) as d:
        Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
        A, E = d["campo_A"].copy(), d["campo_E"].copy()
    C = MT.Campi(Z, "MGU", rho_c, e)
    C.campo.A[...] = A
    C.campo.E[...] = E
    C.campo.e = e
    C.e_prec = e
    U1.scrivi_U(Z["mot"], C.campo)                         # ### d9318470: l'U che avvolto lascia dopo l'ultimo tick
    return C, f


def main(argv):
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import toro as TO
    for m in ("mattone", "mattone_cottura", "mattone_cottura_U", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    reg = argv[argv.index("--registro") + 1] if "--registro" in argv else None
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    sv = np.load(os.path.join(MT.DIR_REF, "triangolo_video_serie.npz"))
    print("=" * 130)
    print("IL TRIFOGLIO LUNGO (Luca 23:32, L2-L4): il video da k %d per %d tick in piu'; la scena di S162, il bordo da R_A %g, G+U; le mappe ogni %d, lo stato ogni %d" % (K_DA, N_PIU, MTR.R_A_SCENA, OGNI_MAPPA, OGNI_STATO))
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n, righe, m1, m2 = Z["L"], Z["n"], Z["righe"], Z["m1"], Z["m2"]
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]

        def centri_da_serie(k):
            j = int(np.nonzero(sv["k"] == k)[0][0])
            return [[float(sv["c1_" + q][j]), float(sv["c2_" + q][j])] for q in "ABC"]

        def gira(k_da, n_tick, misura=None):
            C = Z["_C"]
            R = CT.Corsa(Z, C)
            cen = centri_da_serie(k_da)
            R.etichette(cen)
            R.inizio(k_da)
            stato = {"cen": cen}
            if misura:
                misura(k_da, stato, R)
            t1 = t_tappa = time.time()
            for k in range(k_da + 1, k_da + n_tick + 1):
                R.passo(k, t0 + k, 1.0, e)
                rho = MT.rho_di(Z)
                stato["cen"], _lab = MTR.centri_pezzi(Z, rho, stato["cen"])
                if (k - k_da) % CT.OGNI == 0:
                    R.etichette(stato["cen"])
                if misura:
                    misura(k, stato, R)
                if reg and time.time() - t_tappa >= MT.TAPPA_S:
                    MT.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (time.time() - t1) / (k - k_da), MT.memoria_gb()))
                    t_tappa = time.time()
            return R
        # ---------------------------------------------------------------- il DEVE della ripartenza
        Z["_C"], f15 = carica(Z, K_DA - N_DEVE, rho_c, e)
        gira(K_DA - N_DEVE, N_DEVE)
        f20 = os.path.join(MT.DIR_E, "triangolo_video_%05d.npz" % K_DA)
        with np.load(f20) as d:
            div = [x for x in Z["chiavi"] if x not in CU.CHIAVI_SERVIZIO and not np.array_equal(Z["st"][x], d[x])]
            div += [x for x, a in (("campo_A", Z["_C"].campo.A), ("campo_E", Z["_C"].campo.E)) if not np.array_equal(a, d[x])]
        print("  DEVE PASSARE: la ripartenza da %s per %d tick = %s AL BIT (esclusa h_int)   %s   diverse: %s" % (f15, N_DEVE, f20, "PASSA" if not div else "### FALLISCE", div))
        if div:
            print("ESITO: ### FERMO: la ripartenza NON e' esatta")
            return 1
        # ---------------------------------------------------------------- il trifoglio lungo
        Z["_C"], _f = carica(Z, K_DA, rho_c, e)
        S = {x: [] for x in ("k", "b1", "b2", "raggio", "A3", "M", "E_tondo", "E_A3", "gauss") + tuple("%s_%s" % (q, s) for q in ("c1", "c2", "u1", "u2") for s in "ABC")}
        PK, MP = [], {"k": [], "rho": [], "dphi": [], "E": [], "centri": []}

        def misura(k, stato, R):
            rho = MT.rho_di(Z)
            PK.append(float(rho.max()))
            if (k - K_DA) % OGNI and (k - K_DA) % OGNI_MAPPA:
                return
            C = Z["_C"]
            b = TO.centro(rho, m1, m2, L)[:2]
            pos = TO.scarti(m1, m2, b[0], b[1], L)[:, :2]
            r = np.hypot(pos[:, 0], pos[:, 1])
            th = np.arctan2(pos[:, 1], pos[:, 0])
            dentro = r <= R_FORMA
            phi0 = BO.c_di(t0 + k, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
            dphi = np.sqrt(np.sum(np.abs(Z["st"]["phi_h"] - phi0).reshape(n * 6, -1) ** 2, axis=1))
            dphi_n = np.sqrt(np.sum(dphi[righe] ** 2, axis=1))
            En = np.sqrt(np.sum(C.campo.E.reshape(n, 3) ** 2, axis=1))
            if (k - K_DA) % OGNI == 0:
                cen, lab = MTR.centri_pezzi(Z, rho, stato["cen"])
                S["k"].append(k)
                S["b1"].append(b[0])
                S["b2"].append(b[1])
                S["raggio"].append(float(math.sqrt(np.sum(rho[dentro] * r[dentro] ** 2) / np.sum(rho[dentro]))))
                S["A3"].append(float(abs(np.sum(rho[dentro] * np.exp(3j * th[dentro]))) / np.sum(rho[dentro])))
                S["M"].append(float(rho.sum()))
                an = (r >= ANELLO[0]) & (r <= ANELLO[1])
                S["E_tondo"].append(float(En[an].mean()))
                S["E_A3"].append(float(abs(np.sum(En[an] * np.exp(3j * th[an]))) / np.sum(En[an])))
                S["gauss"].append(C.residuo() if (k - K_DA) % MT.OGNI_GAUSS == 0 else float("nan"))
                for i, q in enumerate("ABC"):
                    S["c1_" + q].append(cen[i][0])
                    S["c2_" + q].append(cen[i][1])
                    u = TO.centro(np.where(lab == i, dphi_n, 0.0), m1, m2, L)[:2]
                    S["u1_" + q].append(u[0])
                    S["u2_" + q].append(u[1])
                if (k - K_DA) % 500 == 0:
                    print("    k %5d  il raggio %.4f  A3 %.4f  la massa %.6e  |E| sull'anello %.4e (A3 %.4f)  Gauss %s  (%.0f s)" % (k, S["raggio"][-1], S["A3"][-1], S["M"][-1], S["E_tondo"][-1], S["E_A3"][-1],
                          "%.2e" % S["gauss"][-1] if S["gauss"][-1] == S["gauss"][-1] else "--", time.time() - t00))
                    sys.stdout.flush()
            if (k - K_DA) % OGNI_MAPPA == 0:
                MP["k"].append(k)
                MP["rho"].append(rho.astype(np.float32))
                MP["dphi"].append(dphi_n.astype(np.float32))
                MP["E"].append(En.astype(np.float32))
                MP["centri"].append(np.array(stato["cen"], dtype=np.float32))
            if k > K_DA and (k - K_DA) % OGNI_STATO == 0:
                np.savez(os.path.join(MT.DIR_E, "triangolo_trifoglio_%05d.npz" % k), meta=np.array(json.dumps({"k": k, "t": t0 + k, "sha": V.shas(Z["z"]), "codice": "csv/solitone/trifoglio.py"})),
                         campo_A=C.campo.A, campo_E=C.campo.E, **{x: Z["st"][x] for x in Z["chiavi"]})
        R = gira(K_DA, N_PIU, misura)
        print("-" * 130)
        R.tabella(["A", "B", "C"])
        A1, A2 = TO.vettori()
        xy = m1[:, None] * A1[None, :] + m2[:, None] * A2[None, :]
        geo = dict(m1=m1.astype(np.int16), m2=m2.astype(np.int16), x=xy[:, 0].astype(np.float32), y=xy[:, 1].astype(np.float32), L=np.int16(L))
    np.savez_compressed(os.path.join(MT.DIR_REF, "triangolo_trifoglio_serie.npz"), picco=np.array(PK), **{x: np.array(v) for x, v in S.items()})
    np.savez_compressed(os.path.join(MT.DIR_REF, "triangolo_trifoglio_mappe.npz"), tick=np.array(MP["k"], dtype=np.int16), rho=np.stack(MP["rho"]), dphi=np.stack(MP["dphi"]), E=np.stack(MP["E"]),
                        centri=np.stack(MP["centri"]), **geo)
    # ---------------------------------------------------------------- L4
    kk = np.array(S["k"])
    A3, rg = np.array(S["A3"]), np.array(S["raggio"])
    kf = int(kk[-1])
    w = [(kk > a) & (kk <= a + FIN) for a in range(K_DA, kf, FIN)]
    a3w = [float(A3[x].mean()) for x in w]
    rgw = [float(rg[x].mean()) for x in w]
    dA, dR = abs(a3w[-1] - a3w[-2]) / a3w[-2], abs(rgw[-1] - rgw[-2]) / rgw[-2]
    if a3w[-1] < RESTA * a3w[0]:
        lett = "SI ARROTONDA IN UN SOLITONE GRANDE"
    elif dA < CAMBIA and dR < CAMBIA:
        lett = "UN OGGETTO NUOVO CON LA SUA FORMA"
    else:
        lett = "NON SI FERMA"
    g = np.array(S["gauss"])
    g = g[g == g]
    print("### L4: A3 per finestra di %d tick %s; il raggio %s; fra le ultime due: A3 %.4f, il raggio %.4f -> %s" % (FIN, ["%.4f" % x for x in a3w], ["%.3f" % x for x in rgw], dA, dR, lett))
    print("  DEVE PASSARE: il residuo di Gauss sotto %g a ogni controllo   %s   il massimo %.3e" % (MT.TOLL_GAUSS, "PASSA" if g.max() < MT.TOLL_GAUSS else "### FALLISCE", g.max()))
    print("=" * 130)
    print("ESITO: %s; %.0f s in tutto" % (lett, time.time() - t00))
    return 0 if g.max() < MT.TOLL_GAUSS else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
