# -*- coding: utf-8 -*-
r"""**P6, LA PROVA BREVE DEL SOLO BRACCIO (U)** *(Luca `2026-11-12` `20:52`, `22:52`; il task history `doc/TASK_HISTORY/2026-11-12_inerzia_G_U_domini.md`, sez. `11.9`, `11.12`)*. [[PIANO-2D-3D]]

    python csv/solitone/p6_u_breve.py > doc/referti_l2/p6_u_breve.txt

**P0:** `e` ricalcolato dai referti *(`e = sqrt(a 2 pi mu d / N)`, `a = 1e-6`)* contro la decisione `6.315414e-05` *(si usa la decisione)*. **P1:** Gauss col Laplaciano SPARSO
*(`D D^T phi = b`, `E = D^T phi`, la soluzione di norma minima)* **= `lstsq` denso** sul toro `L 24` entro `1e-10` *(DEVE FALLIRE: la stessa piu' un rotore)*. **P2:** la scena di G2
*(C35-pi a `60000`, `L 162`, il bordo dopo ogni tick)*, **il campo NON compatto con `E` da Gauss** *(`div E = e (rho - media rho)`: lo sfondo neutralizzante, DICHIARATO)*.
**P3:** (0) `200` tick *(DEVE: le mappe di C35-pi entro `1e-5`)*. **P4:** (U) a `e = 0` *(DEVE: lo stato a `200` = (0) AL BIT)*. **P5:** (U) `200` tick, ogni `10`: `d`, `K + V`,
l'energia della materia, `M`, `V`, `max |e B|`, il residuo di Gauss. **P6:** la parabola di `d_U - d_0`, il rapporto con l'atteso `d'' = -2 a`. **Il FERMO e le letture: sez. `11.12`.**
"""
import math
import os
import re
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "C35-pi"                    # ### Luca (P6, sez. 11.1): la coppia di G2
T0 = 60000                          # ### come G2
E_DECISO = 6.315414e-05             # ### Luca 20:52 (sez. 11.9)
A_SCELTA = 1e-6                     # ### Luca 20:52: l'accelerazione attesa di un corpo, nodi per tick^2
FORMA = "noncompatto"               # ### Luca (sez. 11.3, 11.7): non compatta, come T3
N_TICK, OGNI = 200, 10              # ### Luca 20:52: 200 tick, ogni 10
L_PICCOLO, SEME = 24, 0             # ### P1: il toro piccolo e il seme di b (miei, dichiarati)
TOLL_GAUSS = 1e-10                  # ### Luca 22:52
AMP_ROT = 1e-6                      # ### P1 DEVE FALLIRE: il rotore aggiunto, relativo alla norma (mio, dichiarato)
TOLL_D = 1e-5                       # ### come G2: (0) contro le mappe float32
N_ERR = 3.0                         # ### le letture (b1)-(b3) a 3 errori, come G2
FERMO_D, FERMO_M, FERMO_RHO, FERMO_CAMPO, FERMO_EB = 0.5, 1e-3, 2.0, 10.0, 1.0   # ### le soglie del FERMO (sez. 11.12): mie, dichiarate; EB 1 rad di Luca 13:26 (T6a)
REF = os.path.join(os.path.dirname(_CSV), "doc", "referti_l2")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def cerca(nome, regex):
    with open(os.path.join(REF, nome), encoding="utf-8") as f:
        for riga in f:
            m = re.search(regex, riga)
            if m:
                return float(m.group(1))
    raise AssertionError("%r NON trovato in %s" % (regex, nome))


def dati_di_e():
    """### **P0:** `d`, `N = M/2` dal referto di U4; `eps''` dal referto di T-L4b *(la banda 0)*."""
    d = cerca("unificazione_riproduzione.txt", r"la distanza della coppia: vecchio ([0-9.]+) ")
    M = cerca("unificazione_riproduzione.txt", r"la norma vecchio ([0-9.]+) ")
    e2 = cerca("s5_caduta_segno.txt", r"la banda 0: .* d2 eps/dk2 ([-+0-9.e]+);")
    return d, M / 2.0, 1.0 / abs(e2), e2


def matrice_div_sparsa(campo):
    """### **`D` sparsa** *(come `Campo.matrice_div`: `+1` sull'arrivo `jj`, `-1` sulla partenza `ii`)*."""
    import scipy.sparse as sp
    m = campo.m
    righe = np.concatenate([campo.jj, campo.ii])
    col = np.concatenate([np.arange(m), np.arange(m)])
    val = np.concatenate([np.ones(m), -np.ones(m)])
    return sp.csr_matrix((val, (righe, col)), shape=(campo.n, m))


def gauss_sparso(campo, b):
    """### **La soluzione di NORMA MINIMA di `D E = b`** *(`b` a media nulla)*: **`D D^T phi = b`** *(il Laplaciano del grafo, singolare per le costanti: `phi` del nodo `0` fissato a
    `0`, poi la media tolta)*, **`E = D^T phi`** *(nell'immagine di `D^T`, ortogonale al nucleo di `D`: e' la norma minima, la soluzione di `lstsq`)*."""
    import scipy.sparse.linalg as spl
    b = np.asarray(b, dtype=float)
    assert abs(float(b.sum())) <= 1e-12 * float(np.sum(np.abs(b))) + 1e-300, "b NON e' a media nulla: Gauss sul toro non ha soluzione"
    D = matrice_div_sparsa(campo)
    Lap = (D @ D.T).tocsc()
    phi = np.zeros(campo.n)
    phi[1:] = spl.spsolve(Lap[1:, 1:], b[1:])
    phi -= phi.mean()
    E = D.T @ phi
    return E, D


def rho_nodi(st, nodo, n):
    r = np.zeros(n)
    np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    return r


def p1_toro_piccolo(e):
    """### **P1:** sparsa contro `lstsq` denso sul toro `L_PICCOLO`, `b` casuale a media nulla; **DEVE FALLIRE: la stessa piu' un rotore.**"""
    from solitone import _u1_oggi as UO
    L = L_PICCOLO
    v = np.arange(L * L)
    m1, m2 = v // L, v % L

    def nb(d1, d2):
        return ((m1 + d1) % L) * L + (m2 + d2) % L
    ii = np.repeat(v, 3)
    jj = np.stack([nb(1, 0), nb(0, 1), nb(1, 1)], axis=1).reshape(-1)
    c = UO.Campo(ii, jj, (L, L), e, FORMA, np.ones(3 * L * L))
    rng = np.random.default_rng(SEME)
    b = rng.standard_normal(L * L)
    b -= b.mean()
    E_sp, D = gauss_sparso(c, b)
    E_ls = np.linalg.lstsq(c.matrice_div(), b, rcond=None)[0]
    r = float(np.max(np.abs(E_sp - E_ls))) / float(np.max(np.abs(E_ls)))
    res = float(np.max(np.abs(D @ E_sp - b))) / float(np.max(np.abs(b)))
    print("### P1, il toro L %d (seme %d): max|E_sparsa - E_lstsq| / max|E_lstsq| %.3e; il residuo di Gauss della sparsa max|D E - b| / max|b| %.3e" % (L, SEME, r, res))
    esito("P1: la soluzione di Gauss sparsa = lstsq denso entro %g relativo (toro L %d)" % (TOLL_GAUSS, L), r <= TOLL_GAUSS, "%.3e" % r)
    g = rng.standard_normal(2 * L * L)
    rot = c.matrice_rot().T @ g
    rot *= AMP_ROT * float(np.linalg.norm(E_sp)) / float(np.linalg.norm(rot))
    E_alt = E_sp + rot
    r_alt = float(np.max(np.abs(E_alt - E_ls))) / float(np.max(np.abs(E_ls)))
    res_alt = float(np.max(np.abs(D @ E_alt - b))) / float(np.max(np.abs(b)))
    print("    la stessa piu' un rotore (%g della norma): il residuo di Gauss %.3e (Gauss resta vera), lo scarto da lstsq %.3e" % (AMP_ROT, res_alt, r_alt))
    esito("P1: la chiave del DEVE FALLIRE: la stessa piu' un rotore soddisfa Gauss entro %g" % TOLL_GAUSS, res_alt <= TOLL_GAUSS, "%.3e" % res_alt)
    esito("P1: la stessa piu' un rotore (Gauss vera, NON di norma minima) = lstsq entro %g" % TOLL_GAUSS, r_alt <= TOLL_GAUSS, "%.3e" % r_alt, deve=False)
    return res_alt


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import _u1_oggi as UO
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import corsa_accensione as CA
    from solitone import mappe as MP
    from solitone import protetto as P
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "accensione", "bordo", "carta_coppia", "mappe", "toro", "protetto", "_u1_oggi"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("_u1_prototipo", "_libro_dei_conti"):
        _presidio.avvia(os.path.join(_CSV, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(_CSV), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    # ---------------------------------------------------------------- P0: e
    d_dec, N, mu, e2 = dati_di_e()
    e_ric = math.sqrt(A_SCELTA * 2.0 * math.pi * mu * d_dec / N)
    print("=" * 130)
    print("P6, LA PROVA BREVE DI (U) (sez. 11.9, 11.12): lo stato di %s a %d; %d tick, d ogni %d; il campo %s, E da Gauss (lo sfondo neutralizzante -e media rho, DICHIARATO)" % (CORSA, T0, N_TICK, OGNI, FORMA))
    print("=" * 130)
    print("### P0: d %.6f, N = M/2 %.6e (unificazione_riproduzione.txt); eps'' %.6e, mu = 1/|eps''| %.6f (s5_caduta_segno.txt); e = sqrt(a 2 pi mu d / N) con a %g: %.7e; la decisione %.7e"
          % (d_dec, N, e2, mu, A_SCELTA, e_ric, E_DECISO))
    esito("P0: e ricalcolato dai referti = la decisione 6.315414e-05 alle 7 cifre", abs(e_ric - E_DECISO) <= 5e-7 * E_DECISO, "%.7e" % e_ric)
    e = E_DECISO
    # ---------------------------------------------------------------- P1: Gauss sul toro piccolo
    p1_toro_piccolo(e)
    # ---------------------------------------------------------------- P2: la scena di G2
    sol, vuoto, s = V.CORSE[CA.NOME]
    T_acc, _fine = CA.CORSE[CORSA]
    K = int(round(T_acc / s))
    rr = CA.serie(CORSA)[0]
    x_st = [x for r in rr for x in (r.get("stati") or []) if x["t"] == T0]
    assert len(x_st) == 1, "lo stato di %s a %d NON e' uno solo nel jsonl" % (CORSA, T0)
    bor = rr[-1]["bordo"]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
        assert int(d["K"]) == K
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        n, L = inc.n, z["L"]
        assert L == CA.LCORSA[CORSA]
        cs_scena, lc_scena = mot.cs, getattr(mot, "lambda_c", None)
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        nodo = np.asarray(inc.nodo)
        v_ = np.arange(n)
        m1, m2 = v_ // L, v_ % L
        x = TO.scarti(m1, m2, bor["c0"][0], bor["c0"][1], L)[:, 0]
        g_e = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])[0]
        sul_bordo = np.zeros(n, dtype=bool)
        np.logical_or.at(sul_bordo, nodo, g_e > 0)
        U0 = mot.geo.U.copy()
        assert float(np.max(np.abs(U0 - np.eye(2)[None, :, :]))) == 0.0, "la scena NON ha U = I"
        with np.load(x_st[0]["file"]) as d:
            assert int(d["t"]) == T0
            stato = {k: d[k].copy() for k in chiavi}

        def metti_stato():
            for k in chiavi:
                st[k][...] = stato[k]
            mot.cs, mot.lambda_c = cs_scena, lc_scena
            mot.geo.U[...] = U0

        def d_di(rho):
            cA, cB = CC.centri_semipiani(rho, m1, m2, L, x, 0.0)
            return float(np.hypot(*CC.vettore(cA, cB, L)))

        def campo_di_gauss(e_):
            campo = UO.campo_della_scena(z, e_, FORMA)
            r0 = rho_nodi(st, nodo, n)
            b = e_ * (r0 - r0.mean())
            if e_ != 0.0:
                campo.E[...], D = gauss_sparso(campo, b)
                res = float(np.linalg.norm(D @ campo.E - b)) / float(np.linalg.norm(b))
                res_max = float(np.max(np.abs(D @ campo.E - b))) / float(np.max(np.abs(b)))
            else:
                res = res_max = 0.0
            G0 = campo.div() - b
            return campo, r0, G0, res, res_max

        metti_stato()
        assert V.shas(z) == x_st[0]["sha"], "lo stato di %s a %d NON e' quello registrato nel jsonl" % (CORSA, T0)
        r0 = rho_nodi(st, nodo, n)
        d0 = d_di(r0)
        a_att = e * e * N / (2.0 * math.pi * mu * d0)
        dd_att = -2.0 * a_att
        print("### P2: a t %d d0 %.6f (i semipiani); L %d, %d nodi (%d sul bordo); e_K %.10f; M %.6e, max rho %.6e" % (T0, d0, L, n, int(sul_bordo.sum()), e_K, float(r0.sum()), float(r0.max())))
        print("    L'ATTESO (sez. 3, sez. 11.12): a di un corpo = e^2 N / (2 pi mu d0) = %.6e; d'' = -2 a = %.6e per tick^2 (alla d della decisione, %.6f: a %.6e)"
              % (a_att, dd_att, d_dec, e * e * N / (2.0 * math.pi * mu * d_dec)))

        def corsa(modo, e_):
            """### `modo`: `"0"` il tick della corsa; `"U"` il tick avvolto col campo di Gauss a `e_`. ### Le serie ogni `OGNI` tick; il FERMO solo per `"U"` con `e_ != 0`."""
            metti_stato()
            campo = G0 = None
            out = {"t": [T0], "d": [d0], "fermo": None}
            if modo == "U":
                campo, r_i, G0, res, res_max = campo_di_gauss(e_)
                out.update(res=res, res_max=res_max)
            scala = e_ * float(r0.max())

            def misura(t):
                rho = rho_nodi(st, nodo, n)
                riga = {"t": t, "d": d_di(rho), "M": float(np.sum(np.abs(st["psi_h"]) ** 2)), "V": float(np.sum(np.abs(st["phi_h"]) ** 2)), "rmax": float(rho.max())}
                riga["E_mat"] = float(np.sum(LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"]))
                if campo is not None:
                    riga["K"], riga["Vc"] = campo.K(), campo.V()
                    riga["eB"] = float(np.max(np.abs(e_ * campo.B())))
                    if e_ != 0.0:
                        G = campo.div() - e_ * (rho - rho.mean())
                        dG = np.abs(G - G0) / scala
                        riga["G_in"], riga["G_bordo"] = float(dG[~sul_bordo].max()), float(dG[sul_bordo].max())
                return riga
            righe = [misura(T0)]
            for k in range(1, N_TICK + 1):
                t = T0 + k
                if modo == "0":
                    AC.tick(z, t, K)
                else:
                    UO.tick(z, t, K, campo, True)
                BO.assorbi(st, g_e, BO.c_di(t, tab_c, K, omega) * phi_v)
                if k % OGNI == 0:
                    rg = misura(t)
                    righe.append(rg)
                    out["t"].append(t)
                    out["d"].append(rg["d"])
                    if modo == "U" and e_ != 0.0:
                        f = []
                        if rg["d"] < FERMO_D * d0:
                            f.append("si fonde (d %.4f < %g d0)" % (rg["d"], FERMO_D))
                        m0 = rif_M.get(t)
                        if m0 is not None and abs(rg["M"] / m0 - 1.0) > FERMO_M:
                            f.append("esplode (M_U / M_0 - 1 = %.3e)" % (rg["M"] / m0 - 1.0))
                        if rg["rmax"] > FERMO_RHO * float(r0.max()):
                            f.append("esplode (max rho %.4e)" % rg["rmax"])
                        if rg["K"] + rg["Vc"] > FERMO_CAMPO * (righe[0]["K"] + righe[0]["Vc"]):
                            f.append("il campo cresce (K + V %.4e)" % (rg["K"] + rg["Vc"]))
                        if rg["eB"] > FERMO_EB:
                            f.append("max |e B| %.3f > %g rad" % (rg["eB"], FERMO_EB))
                        if f:
                            out["fermo"] = (t, f)
                            break
            out["righe"] = righe
            out["sha"] = V.shas(z)
            out["t"], out["d"] = np.array(out["t"]), np.array(out["d"])
            mot.geo.U[...] = U0
            return out

        rif_M = {}
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            t1 = time.time()
            c0 = corsa("0", 0.0)
            print("### P3 (0): %d tick in %.0f s; d da %.6f a %.6f" % (N_TICK, time.time() - t1, c0["d"][0], c0["d"][-1]))
            rif_M.update({r["t"]: r["M"] for r in c0["righe"]})
            t1 = time.time()
            cz = corsa("U", 0.0)
            print("### P4 (U) a e = 0: %d tick in %.0f s; d da %.6f a %.6f" % (N_TICK, time.time() - t1, cz["d"][0], cz["d"][-1]))
            t1 = time.time()
            cu = corsa("U", e)
            print("### P5 (U) a e %.7e: %d tick in %.0f s (%.3f s per tick); d da %.6f a %.6f" % (e, len(cu["righe"]) * OGNI - OGNI, time.time() - t1, (time.time() - t1) / max(1, (len(cu["righe"]) - 1) * OGNI), cu["d"][0], cu["d"][-1]))
        mot.geo.U[...] = U0
    # ---------------------------------------------------------------- P3: (0) contro le mappe
    dm = {}
    cartella = os.path.join(MP.RADICE, CORSA)
    for f in sorted(os.listdir(cartella)):
        if not f.endswith(".npz"):
            continue
        with np.load(os.path.join(cartella, f)) as d:
            T, RH = d["t"], d["rho"]
            for i in range(len(T)):
                if T0 < int(T[i]) <= T0 + N_TICK:
                    dm[int(T[i])] = d_di(RH[i].astype(np.float64))
    tt = list(c0["t"])
    com = [t for t in tt if t in dm]
    ed = max(abs(c0["d"][tt.index(t)] - dm[t]) for t in com) if com else float("inf")
    print("-" * 130)
    print("  (0) contro le mappe di %s: %d tick comuni %s, lo scarto piu' grande di d %.3e" % (CORSA, len(com), com, ed))
    esito("P3: (0) ridà C35-pi: d dalle mappe alla stessa ora entro %g" % TOLL_D, len(com) > 0 and ed <= TOLL_D, "%.3e su %d tick" % (ed, len(com)))
    # ---------------------------------------------------------------- P4: il campo spento
    diverse = [k for k in c0["sha"] if c0["sha"][k] != cz["sha"][k]]
    esito("P4: (U) a e = 0 riproduce (0) AL BIT: gli sha di ogni chiave dello stato a %d" % (T0 + N_TICK), not diverse, "diverse: %s" % diverse)
    if cu["fermo"] is None:
        diverse_u = [k for k in c0["sha"] if c0["sha"][k] != cu["sha"][k]]
        print("  controllo: (U) col suo e cambia lo stato (gli sha diversi da (0)): %s" % (diverse_u,))
    # ---------------------------------------------------------------- P5: le serie
    print("-" * 130)
    print("### P5, IL RESIDUO DI GAUSS INIZIALE a L %d: |D E - b| / |b| %.3e; max|D E - b| / max|b| %.3e" % (L, cu["res"], cu["res_max"]))
    print("### P5, ogni %d tick: d_U, d_U - d_0, K + V del campo, l'energia della materia (tot; e la differenza da (0)), M_U / M_0 - 1, V, max rho, max|e B|, Gauss |G - G0| / (e max rho0) fuori e sul bordo" % OGNI)
    r0s = {r["t"]: r for r in c0["righe"]}
    for r in cu["righe"]:
        q = r0s[r["t"]]
        print("    t %6d  d %.6f  dd %+.4e  K+V %.6e  E_mat %.10e (%+.4e)  M %+.3e  V %.6e  rmax %.4e  eB %.3e  G %.2e / %.2e"
              % (r["t"], r["d"], r["d"] - q["d"], r["K"] + r["Vc"], r["E_mat"], r["E_mat"] - q["E_mat"], r["M"] / q["M"] - 1.0, r["V"], r["rmax"], r["eB"], r["G_in"], r["G_bordo"]))
    print("    e (0): E_mat da %.10e a %.10e; M da %.10e a %.10e" % (c0["righe"][0]["E_mat"], c0["righe"][-1]["E_mat"], c0["righe"][0]["M"], c0["righe"][-1]["M"]))
    if cu["fermo"] is not None:
        print("=" * 130)
        print("### FERMO a t %d (le soglie della sez. 11.12): %s" % cu["fermo"])
    # ---------------------------------------------------------------- P6: la parabola
    nu = len(cu["d"])
    dd = cu["d"] - c0["d"][:nu]
    tf = (cu["t"] - T0).astype(float)
    a, ea = CC.curvatura(tf, dd) if nu >= 4 else (float("nan"), float("nan"))
    print("-" * 130)
    print("### P6: d_U - d_0 ogni %d tick: %s" % (OGNI, " ".join("%+.3e" % v for v in dd)))
    print("    la parabola: d'' in piu' %+.6e +- %.1e per tick^2 (%.1f errori); l'atteso %.6e; il rapporto misurato / atteso %.4f"
          % (a, ea, abs(a) / ea if ea else float("inf"), dd_att, a / dd_att))
    if a < -N_ERR * ea:
        print("  LA LETTURA: (b1) d'' negativo oltre %g errori: si avvicinano, il verso dell'atteso" % N_ERR)
    elif a > N_ERR * ea:
        print("  LA LETTURA: (b3) d'' positivo oltre %g errori: si allontanano, contro l'atteso" % N_ERR)
    else:
        print("  LA LETTURA: (b2) entro %g errori: in %d tick non si misura niente" % (N_ERR, N_TICK))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; FERMO del campo: %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, "SI" if cu["fermo"] else "no", time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
