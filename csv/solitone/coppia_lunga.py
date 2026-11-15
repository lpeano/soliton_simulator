# -*- coding: utf-8 -*-
r"""**LA FABBRICA, IL 2x: LA COPPIA B2 PROSEGUE** *(Luca `2026-11-15` `01:54`, F2; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `22`, `22.3`)*.

    python csv/solitone/coppia_lunga.py --registro coppia-lunga > <scratchpad>/coppia_lunga.txt     (poi doc/referti_l2/mattone/coppia_lunga.txt; le mappe in coppia_lunga_mappe.npz)

### **B2** *(`mattone_coppia_L162.py --mondo GU`: due mattoni di `L 162` in fase, la scena di C35-pi, il bordo da `60`, G+U)* **PROSEGUE dal suo ultimo stato** *(`coppiaGU_L162_02000`; `U` dal campo)* **per `4000` tick in
piu'** *(in tutto `6000`)*. ### **DEVE** *(gli stati sono ogni `500`)*: **da `coppiaGU_L162_01500`, `500` tick = `coppiaGU_L162_02000` AL BIT** *(esclusa `h_int`)*.
### **Ogni `50` tick** *(come il trifoglio, F1)*: **`d`** *(dai semipiani, come B2)*, **il baricentro, il raggio di tutta la materia entro `60`, la componente a DUE punte `A2 = |somma rho e^{2 i theta}| / somma rho`, la
massa, i centri delle due culle** *(`|phi - phi0|` sul pezzo di ciascuno)*, **Gauss ogni `250`; il picco a ogni tick; le mappe ogni `100`; lo stato ogni `1000`; la massa oltre `R_A` dal centro del bordo all'inizio e alla
fine; la massa uscita dal bordo** *(il DEVE: la massa persa = la massa uscita dal bordo entro `1e-6` relativo)*.
### **LA LETTURA** *(le soglie del guardiano, F1)*: **il COLLASSO: il picco oltre `2` volte quello del mattone** *(`1250 -> 2500`)* **e in crescita per `500` tick; l'ESPLOSIONE: il raggio oltre `40` o la massa oltre `R_A`
oltre l'`1%`; «UNA PALLA» se `A2` scende sotto il `5%` e la forma cambia meno del `2%` fra due finestre di `1000` tick** *(e allora: le due culle restano o si fondono)*. **Collasso ed esplosione: un risultato, si scrive.**
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

CORSA_C, T_C = "C35-pi", 60000
R_A_COPPIA = 60.0
K_DA, N_PIU, N_DEVE = 2000, 4000, 500
OGNI, OGNI_MAPPA, OGNI_STATO, FIN = 50, 100, 1000, 1000
R_FORMA = 60.0
PICCO_MATTONE, COLLASSO, RAGGIO_MAX, FUORI_MAX = 1250.0, 2.0, 40.0, 0.01
PALLA, CAMBIA = 0.05, 0.02


def carica(Z, k, rho_c, e):
    import _u1_prototipo as U1
    f = os.path.join(MT.DIR_E, "coppiaGU_L162_%05d.npz" % k)
    with np.load(f) as d:
        Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
        A, E = d["campo_A"].copy(), d["campo_E"].copy()
    C = MT.Campi(Z, "MGU", rho_c, e)
    C.campo.A[...] = A
    C.campo.E[...] = E
    C.campo.e = e
    C.e_prec = e
    U1.scrivi_U(Z["mot"], C.campo)
    return C, f


def main(argv):
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    for m in ("mattone", "mattone_cottura", "mattone_cottura_U"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    reg = argv[argv.index("--registro") + 1] if "--registro" in argv else None
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("LA FABBRICA, IL 2x (Luca 01:54, F2): B2 da k %d per %d tick in piu'; la scena di %s, il bordo da R_A %g, G+U" % (K_DA, N_PIU, CORSA_C, R_A_COPPIA))
    print("=" * 130)
    with MT.scena(CORSA_C, T_C) as Z:
        L, n, righe, m1, m2 = Z["L"], Z["n"], Z["righe"], Z["m1"], Z["m2"]
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], R_A_COPPIA, Z["bordo"]["g_max"])[0]
        xs = TO.scarti(m1, m2, c0[0], c0[1], L)[:, 0]
        r_c0 = np.hypot(*TO.scarti(m1, m2, c0[0], c0[1], L).T[:2])

        def gira(C, k_da, n_tick, misura=None):
            R = CT.Corsa(Z, C)
            a, b = CC.centri_semipiani(MT.rho_di(Z), m1, m2, L, xs, 0.0)
            R.etichette([a, b])
            R.inizio(k_da)
            if misura:
                misura(k_da, C)
            t1 = t_tappa = time.time()
            for k in range(k_da + 1, k_da + n_tick + 1):
                R.passo(k, T_C + k, 1.0, e)
                if (k - k_da) % CT.OGNI == 0:
                    a, b = CC.centri_semipiani(MT.rho_di(Z), m1, m2, L, xs, 0.0)
                    R.etichette([a, b])
                if misura:
                    misura(k, C)
                if reg and time.time() - t_tappa >= MT.TAPPA_S:
                    MT.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (time.time() - t1) / (k - k_da), MT.memoria_gb()))
                    t_tappa = time.time()
            return R
        # ---------------------------------------------------------------- il DEVE della ripartenza
        C, f15 = carica(Z, K_DA - N_DEVE, rho_c, e)
        gira(C, K_DA - N_DEVE, N_DEVE)
        f20 = os.path.join(MT.DIR_E, "coppiaGU_L162_%05d.npz" % K_DA)
        with np.load(f20) as d:
            div = [x for x in Z["chiavi"] if x not in CU.CHIAVI_SERVIZIO and not np.array_equal(Z["st"][x], d[x])]
            div += [x for x, a in (("campo_A", C.campo.A), ("campo_E", C.campo.E)) if not np.array_equal(a, d[x])]
        print("  DEVE PASSARE: la ripartenza da %s per %d tick = %s AL BIT (esclusa h_int)   %s   diverse: %s" % (f15, N_DEVE, f20, "PASSA" if not div else "### FALLISCE", div))
        if div:
            print("ESITO: ### FERMO: la ripartenza NON e' esatta")
            return 1
        # ---------------------------------------------------------------- il 2x
        C, _f = carica(Z, K_DA, rho_c, e)
        S = {x: [] for x in ("k", "d", "b1", "b2", "raggio", "A2", "M", "fuori", "gauss", "u1_A", "u2_A", "u1_B", "u2_B")}
        PK, MP = [], {"k": [], "rho": [], "dphi": [], "E": []}
        stato = {"fermo": None}

        def misura(k, C):
            rho = MT.rho_di(Z)
            PK.append(float(rho.max()))
            fare = (k - K_DA) % OGNI == 0
            mappa = (k - K_DA) % OGNI_MAPPA == 0
            if not (fare or mappa):
                return
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
                S["fuori"].append(float(rho[r_c0 > R_A_COPPIA].sum() / rho.sum()))
                S["gauss"].append(C.residuo() if (k - K_DA) % MT.OGNI_GAUSS == 0 else float("nan"))
                m = xs < 0.0
                for q, sel in (("A", m), ("B", ~m)):
                    u = TO.centro(np.where(sel, dphi_n, 0.0), m1, m2, L)[:2]
                    S["u1_" + q].append(u[0])
                    S["u2_" + q].append(u[1])
                if (k - K_DA) % 500 == 0:
                    print("    k %5d  d %.4f  il raggio %.4f  A2 %.4f  il picco %.4e  la massa %.6e  oltre R_A %.3e  Gauss %s  (%.0f s)" % (k, S["d"][-1], S["raggio"][-1], S["A2"][-1], PK[-1], S["M"][-1], S["fuori"][-1],
                          "%.2e" % S["gauss"][-1] if S["gauss"][-1] == S["gauss"][-1] else "--", time.time() - t00))
                    sys.stdout.flush()
            if mappa:
                MP["k"].append(k)
                MP["rho"].append(rho.astype(np.float32))
                MP["dphi"].append(dphi_n.astype(np.float32))
                MP["E"].append(np.sqrt(np.sum(C.campo.E.reshape(n, 3) ** 2, axis=1)).astype(np.float32))
            if k > K_DA and (k - K_DA) % OGNI_STATO == 0:
                np.savez(os.path.join(MT.DIR_E, "coppia_lunga_%05d.npz" % k), meta=np.array(json.dumps({"k": k, "t": T_C + k, "sha": V.shas(Z["z"]), "codice": "csv/solitone/coppia_lunga.py"})),
                         campo_A=C.campo.A, campo_E=C.campo.E, **{x: Z["st"][x] for x in Z["chiavi"]})
        R = gira(C, K_DA, N_PIU, misura)
        print("-" * 130)
        R.tabella(["A", "B"])
        T = {x: np.array(v) for x, v in R.T.items()}
        bordoM = float(np.sum(T["Mp"] - T["Md"]))
        A1, A2 = TO.vettori()
        xy = m1[:, None] * A1[None, :] + m2[:, None] * A2[None, :]
        geo = dict(m1=m1.astype(np.int16), m2=m2.astype(np.int16), x=xy[:, 0].astype(np.float32), y=xy[:, 1].astype(np.float32), L=np.int16(L))
    np.savez_compressed(os.path.join(MT.DIR_REF, "coppia_lunga_serie.npz"), picco=np.array(PK), **{x: np.array(v) for x, v in S.items()})
    np.savez_compressed(os.path.join(MT.DIR_REF, "coppia_lunga_mappe.npz"), tick=np.array(MP["k"], dtype=np.int16), rho=np.stack(MP["rho"]), dphi=np.stack(MP["dphi"]), E=np.stack(MP["E"]), **geo)
    # ---------------------------------------------------------------- le letture
    kk, A2s, rg, pk = np.array(S["k"]), np.array(S["A2"]), np.array(S["raggio"]), np.array(PK)
    persa = S["M"][0] - S["M"][-1]
    print("### LA MASSA: persa %.6e, uscita dal bordo %.6e, la differenza relativa %.3e (il DEVE: entro 1e-6)" % (persa, bordoM, abs(persa - bordoM) / S["M"][0]))
    sopra = pk > COLLASSO * PICCO_MATTONE
    collasso = bool(sopra[-500:].all() and pk[-1] > pk[-500]) if len(pk) >= 500 else False
    esplosione = bool(rg.max() > RAGGIO_MAX or max(S["fuori"]) > FUORI_MAX)
    w = [(kk > a) & (kk <= a + FIN) for a in range(K_DA, int(kk[-1]), FIN)]
    a2w = [float(A2s[x].mean()) for x in w]
    rgw = [float(rg[x].mean()) for x in w]
    dA, dR = abs(a2w[-1] - a2w[-2]) / max(a2w[-2], 1e-30), abs(rgw[-1] - rgw[-2]) / rgw[-2]
    palla = a2w[-1] < PALLA and dA < CAMBIA and dR < CAMBIA
    lett = "IL COLLASSO" if collasso else ("L'ESPLOSIONE" if esplosione else ("UNA PALLA" if palla else ("SI ARROTONDA" if a2w[-1] < PALLA else "NON SI FERMA / ANCORA DUE")))
    du = [math.hypot(S["u1_A"][i] - S["u1_B"][i], S["u2_A"][i] - S["u2_B"][i]) for i in (0, -1)]
    print("### LA LETTURA: A2 per finestra %s; il raggio %s; il picco max %.4e; la massa oltre R_A max %.3e; d da %.4f a %.4f; la distanza fra le culle da %.3f a %.3f (in indici) -> %s"
          % (["%.4f" % x for x in a2w], ["%.3f" % x for x in rgw], float(pk.max()), max(S["fuori"]), S["d"][0], S["d"][-1], du[0], du[-1], lett))
    g = np.array(S["gauss"])
    g = g[g == g]
    ok = g.max() < MT.TOLL_GAUSS and abs(persa - bordoM) / S["M"][0] <= 1e-6
    print("  DEVE PASSARE: Gauss sotto %g (il massimo %.3e) e la massa persa = la massa uscita dal bordo entro 1e-6: %s" % (MT.TOLL_GAUSS, g.max(), "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    print("ESITO: %s; %.0f s in tutto" % (lett, time.time() - t00))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
