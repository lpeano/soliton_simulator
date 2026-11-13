# -*- coding: utf-8 -*-
r"""**P6, I BRACCI: (0) DUE VOLTE, (G), (U), (G+U), (U) COL CAMPO DA ZERO** *(Luca `2026-11-13` `09:45`; il task history `doc/TASK_HISTORY/2026-11-12_inerzia_G_U_domini.md`, sez. `11`, `11.14`)*. [[PIANO-2D-3D]]

    python csv/solitone/p6_bracci.py --braccio 0 --registro p6-0 > <scratchpad>/p6_0.txt        (poi copiato in doc/referti_l2/p6_bracci/0.txt)
    ... --braccio 0bis | G | U | GU | Uzero
    python csv/solitone/p6_bracci.py --referto > doc/referti_l2/p6_bracci.txt

**La scena di G2 e della prova breve** *(C35-pi a `60000`, `L 162`, il bordo dopo ogni tick)*. **I tick:** (0) `accensione.tick`; (G) `tick_lapse.tick` *(`rho_c = rho_0 / 1e-2`, la forma (a); le
costanti e `eps_top_tl4b` IMPORTATE da `s5_coppia_lapse.py`)*; (U) `_u1_oggi.tick` col campo di Gauss *(`p6_u_breve.gauss_sparso`)*; (Uzero) lo stesso col campo `A = E = 0`;
### **(GU) l'ADATTATORE** *(sez. `11.14`)*: **il corpo di `tick_lapse.tick` con `avvolto` SOLO attorno al `percorri_tick` vero** *(le copie del punto fisso di `cs` non fanno sorgere il campo)*,
la spinta a meta' ai due estremi; **il suo DEVE: a `e = 0`, `20` tick = (G) al bit.** **Le uscite** in `doc/referti_l2/p6_bracci/<braccio>.npz` *(alla fine)*; **le misure, i DEVE e le letture: `--referto`.**
### **L'ENERGIA DEL TORO INTERO ogni `50` tick** *(Luca `2026-11-13` `13:43`)*: **i termini del libro dei conti** *(`_libro_dei_conti.conti_per_nodo`, sommati su TUTTO il toro: `cost`, `cin`, `leg`, `vuo`, `tot`, `M`, `V`)*,
**SOLO il toro intero** *(le regioni dipendono dallo zero)*; **`e_K` della scena** *(`protetto.e_K`)*; **col lapse, il `cs` del tick** *(quello che `tick_lapse.tick` lascia in `mot.cs`)*, dichiarato.
"""
import argparse
import json
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
import s5_coppia_lapse as G2  # noqa: E402  (CORSA, T0, R_LAPSE, TETTO_S, TOLL_D, N_ERR, eps_top_tl4b: RIPRESI)
import p6_u_breve as PB  # noqa: E402  (E_DECISO, FORMA, gauss_sparso, rho_nodi, dati_di_e, le soglie del FERMO: RIPRESI)

BRACCI = ("0", "0bis", "G", "U", "GU", "Uzero")
N_TICK = 1500                       # ### Luca 09:45
OGNI, OGNI_PHI = 50, 250            # ### Luca 22:52 e 09:45: rho e i centri ogni 50; |phi_j|^2 e dLambda ogni 250
N_ADATT = 20                        # ### il DEVE dell'adattatore (mio, dichiarato): 20 tick a e = 0
TETTO_MB = 60.0                     # ### Luca 22:52
TAPPA_S = 600.0                     # ### la skill registro-corse: una tappa ogni circa 10 minuti
N_FINTA = 10.0                      # ### Luca 20:45: l'accelerazione finta = 10 errori del fit di (0)
RADICE = os.path.dirname(_CSV)
DIR_OUT = os.path.join(RADICE, "doc", "referti_l2", "p6_bracci")
REF = os.path.join(RADICE, "doc", "referti_l2")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


# =====================================================================================
#   I TICK
# =====================================================================================
def tick_GU(z, s, legge, e0, campo):
    """### **L'ADATTATORE (G+U)** *(sez. `11.14`)*: **il corpo di `tick_lapse.tick`** *(`senza_reazione` False, `omega` 1, `giri_max` e `storia` None, `eps_a = e0`)* **con
    `_u1_oggi.avvolto` SOLO attorno al `percorri_tick` vero;** **la spinta del campo a meta' ai due estremi, come `_u1_oggi.tick`.**"""
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    from solitone import tick_lapse as TL
    mot, st, par = z["mot"], z["st"], z["par"]
    campo.spinta(0.5)
    TL.fase_a(mot, st, legge, e0, False)
    cs, _giri = TL.cs_al_centro(mot, st, par, s, legge, False, omega=1.0, giri_max=None, storia=None)
    mot.cs = cs
    mot.lambda_c = None
    TL.reazione(mot, st, par, s, legge, 0.5)
    with UO.avvolto(mot, campo, True):
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    TL.reazione(mot, st, par, s, legge, 0.5)
    TL.fase_a(mot, st, legge, e0, False)
    campo.spinta(0.5)


# =====================================================================================
#   UN BRACCIO
# =====================================================================================
def braccio(nome, registro):
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import _registro_corse as RC
    from solitone import _u1_oggi as UO
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    from solitone import tick_lapse as TL
    from solitone import toro as TO
    import _libro_dei_conti as LC
    for m in ("__init__", "corsa_accensione", "accensione", "bordo", "carta_coppia", "toro", "tick_lapse", "_u1_oggi", "s5_coppia_lapse", "p6_u_breve", "_registro_corse", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("_u1_prototipo", "_libro_dei_conti"):
        _presidio.avvia(os.path.join(_CSV, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(RADICE, "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    assert nome in BRACCI
    t00 = time.time()
    e = PB.E_DECISO
    e0 = G2.eps_top_tl4b()
    sol, vuoto, s = V.CORSE[CA.NOME]
    T_acc, _fine = CA.CORSE[G2.CORSA]
    K = int(round(T_acc / s))
    rr = CA.serie(G2.CORSA)[0]
    x_st = [x for r in rr for x in (r.get("stati") or []) if x["t"] == G2.T0]
    assert len(x_st) == 1
    bor = rr[-1]["bordo"]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
        assert int(d["K"]) == K
    rif0 = None
    f0 = os.path.join(DIR_OUT, "0.npz")
    if nome in ("U", "GU", "Uzero") and os.path.exists(f0):
        with np.load(f0) as d:
            rif0 = dict(zip([int(x) for x in d["t"]], [float(x) for x in d["M"]]))
    print("=" * 130)
    print("P6, IL BRACCIO (%s) (sez. 11.14): lo stato di %s a %d; fino a %d tick (il tetto %g s); rho e i centri ogni %d, |phi_j|^2 e dLambda ogni %d; e %.7e; eps_a %.10f; R_LAPSE %g; il registro %s"
          % (nome, G2.CORSA, G2.T0, N_TICK, G2.TETTO_S, OGNI, OGNI_PHI, e, e0, G2.R_LAPSE, registro))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(G2.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, rec["larghezza"])[0]
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, G2.CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        n, L = inc.n, z["L"]
        assert L == CA.LCORSA[G2.CORSA]
        cs_scena, lc_scena = mot.cs, getattr(mot, "lambda_c", None)
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        nodo = np.asarray(inc.nodo)
        righe_idx = np.arange(6 * n)
        idx6 = 2 * ((righe_idx // 2) % 3) + righe_idx % 2
        v_ = np.arange(n)
        m1, m2 = v_ // L, v_ % L
        x = TO.scarti(m1, m2, bor["c0"][0], bor["c0"][1], L)[:, 0]
        g_e = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])[0]
        sul_bordo = np.zeros(n, dtype=bool)
        np.logical_or.at(sul_bordo, nodo, g_e > 0)
        U0 = mot.geo.U.copy()
        assert float(np.max(np.abs(U0 - np.eye(2)[None, :, :]))) == 0.0, "la scena NON ha U = I"
        with np.load(x_st[0]["file"]) as d:
            assert int(d["t"]) == G2.T0
            stato = {k: d[k].copy() for k in chiavi}

        def metti_stato():
            for k in chiavi:
                st[k][...] = stato[k]
            mot.cs, mot.lambda_c = cs_scena, lc_scena
            mot.geo.U[...] = U0

        def centri(rho):
            cA, cB = CC.centri_semipiani(rho, m1, m2, L, x, 0.0)
            return float(np.hypot(*CC.vettore(cA, cB, L))), cA, cB

        def phi2_di():
            tmp = np.zeros((n, 6))
            np.add.at(tmp, (nodo, idx6), np.abs(st["phi_h"]) ** 2)   # ### come s5_g1_lunga.phi2_di
            return tmp.T.copy()

        metti_stato()
        assert V.shas(z) == x_st[0]["sha"], "lo stato di %s a %d NON e' quello registrato nel jsonl" % (G2.CORSA, G2.T0)
        r0 = PB.rho_nodi(st, nodo, n)
        d0, cA0, cB0 = centri(r0)
        nuc = []
        for c_ in (cA0, cB0):
            pos = TO.scarti(m1, m2, c_[0], c_[1], L)
            nuc.append(np.hypot(pos[:, 0], pos[:, 1]) < w_in)
        rho_0 = float(r0[nuc[0] | nuc[1]].mean())
        legge = ("rho_c", rho_0 / G2.R_LAPSE)
        print("### a t %d: d0 %.6f; rho_0 (i due centri, r < w_in %.6f) %.6f; rho_c %.6f; M %.10e; max rho %.6e; %d nodi sul bordo" % (G2.T0, d0, w_in, rho_0, legge[1], float(r0.sum()), float(r0.max()), int(sul_bordo.sum())))

        def campo_gauss(e_):
            campo = UO.campo_della_scena(z, e_, PB.FORMA)
            b = e_ * (r0 - r0.mean())
            res = 0.0
            if e_ != 0.0:
                campo.E[...], D = PB.gauss_sparso(campo, b)
                res = float(np.linalg.norm(D @ campo.E - b)) / float(np.linalg.norm(b))
            return campo, b, res

        out = {"braccio": nome, "e": e, "eps_a": e0, "R_LAPSE": G2.R_LAPSE, "rho_c": legge[1], "rho_0": rho_0, "d0": d0, "w_in": w_in, "L": int(L), "e_K": e_K}
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ---------------------------------------------------------------- il DEVE dell'adattatore (solo GU)
            if nome == "GU":
                metti_stato()
                t1 = time.time()
                for k in range(1, N_ADATT + 1):
                    TL.tick(mot, st, par, s, legge, eps_a=e0)
                    BO.assorbi(st, g_e, BO.c_di(G2.T0 + k, tab_c, K, omega) * phi_v)
                sha_G = V.shas(z)
                metti_stato()
                c_nullo, _b, _r = campo_gauss(0.0)
                for k in range(1, N_ADATT + 1):
                    tick_GU(z, s, legge, e0, c_nullo)
                    BO.assorbi(st, g_e, BO.c_di(G2.T0 + k, tab_c, K, omega) * phi_v)
                sha_A = V.shas(z)
                diverse = [k for k in sha_G if sha_G[k] != sha_A[k]]
                print("### l'adattatore a e = 0 contro (G), %d tick (%.0f s): le chiavi diverse %s" % (N_ADATT, time.time() - t1, diverse))
                out["adattatore_diverse"] = diverse
                if diverse:
                    print("### IL DEVE DELL'ADATTATORE FALLISCE: FERMO, il braccio NON gira")
                    out["fermo"] = "l'adattatore a e = 0 non riproduce (G): %s" % diverse
                    salva(nome, out, None)
                    return 1
            # ---------------------------------------------------------------- il braccio
            metti_stato()
            campo, b0, scala, G0 = None, None, None, None
            if nome in ("U", "GU"):
                campo, b0, out["gauss_iniziale"] = campo_gauss(e)
                print("### il campo di Gauss: il residuo iniziale |D E - b| / |b| %.3e" % out["gauss_iniziale"])
            elif nome == "Uzero":
                campo = UO.campo_della_scena(z, e, PB.FORMA)
                b0 = e * (r0 - r0.mean())
            if campo is not None:
                G0 = campo.div() - b0
                scala = e * float(r0.max())
            S = {k: [] for k in ("t", "d", "cA", "cB", "M", "V", "rmax", "KV", "eB", "G_in", "G_bordo") + tuple("E_" + c for c in LC.CONTI)}
            SP = {"t": [], "phi2": [], "dLambda": []}
            RH = []
            lam0 = phi2_di().sum(axis=0)

            def misura(t):
                rho = PB.rho_nodi(st, nodo, n)
                dd, cA, cB = centri(rho)
                S["t"].append(t)
                S["d"].append(dd)
                S["cA"].append(cA)
                S["cB"].append(cB)
                S["M"].append(float(np.sum(np.abs(st["psi_h"]) ** 2)))
                S["V"].append(float(np.sum(np.abs(st["phi_h"]) ** 2)))
                S["rmax"].append(float(rho.max()))
                RH.append(rho.reshape(L, L).astype(np.float32))
                conti = LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)     # ### Luca 13:43: il toro INTERO, per termini
                for c in LC.CONTI:
                    S["E_" + c].append(float(np.sum(conti[c])))
                if campo is not None:
                    S["KV"].append(campo.K() + campo.V())
                    S["eB"].append(float(np.max(np.abs(e * campo.B()))))
                    G = campo.div() - e * (rho - rho.mean())
                    dG = np.abs(G - G0) / scala
                    S["G_in"].append(float(dG[~sul_bordo].max()))
                    S["G_bordo"].append(float(dG[sul_bordo].max()))
                if (t - G2.T0) % OGNI_PHI == 0:
                    f2 = phi2_di()
                    SP["t"].append(t)
                    SP["phi2"].append(f2.reshape(6, L, L).astype(np.float32))
                    SP["dLambda"].append((f2.sum(axis=0) - lam0).reshape(L, L).astype(np.float32))

            misura(G2.T0)
            t1 = time.time()
            t_tappa = time.time()
            t_blocco = time.time()
            fermo, fatti = None, 0
            for k in range(1, N_TICK + 1):
                t = G2.T0 + k
                if nome in ("0", "0bis"):
                    AC.tick(z, t, K)
                elif nome == "G":
                    TL.tick(mot, st, par, s, legge, eps_a=e0)
                elif nome in ("U", "Uzero"):
                    UO.tick(z, t, K, campo, True)
                else:
                    tick_GU(z, s, legge, e0, campo)
                BO.assorbi(st, g_e, BO.c_di(t, tab_c, K, omega) * phi_v)
                fatti = k
                if k % OGNI == 0:
                    misura(t)
                    f = []
                    if campo is not None:
                        if S["d"][-1] < PB.FERMO_D * d0:
                            f.append("si fonde (d %.4f)" % S["d"][-1])
                        if S["rmax"][-1] > PB.FERMO_RHO * float(r0.max()):
                            f.append("esplode (max rho %.4e)" % S["rmax"][-1])
                        if rif0 is not None and t in rif0 and abs(S["M"][-1] / rif0[t] - 1.0) > PB.FERMO_M:
                            f.append("esplode (M / M_0 - 1 = %.3e)" % (S["M"][-1] / rif0[t] - 1.0))
                        if nome != "Uzero" and S["KV"][-1] > PB.FERMO_CAMPO * S["KV"][0]:
                            f.append("il campo cresce (K + V %.4e)" % S["KV"][-1])
                        if S["eB"][-1] > PB.FERMO_EB:
                            f.append("max |e B| %.3f" % S["eB"][-1])
                    adesso = time.time()
                    print("    t %6d  d %.6f  M %.10e  rmax %.4e%s  (%.0f s)" % (t, S["d"][-1], S["M"][-1], S["rmax"][-1],
                          ("  K+V %.6e  eB %.2e  G %.2e / %.2e" % (S["KV"][-1], S["eB"][-1], S["G_in"][-1], S["G_bordo"][-1])) if campo is not None else "", adesso - t1))
                    sys.stdout.flush()
                    if f:
                        fermo = (t, f)
                        print("### FERMO a t %d (le soglie della sez. 11.12): %s" % fermo)
                        break
                    if registro and adesso - t_tappa >= TAPPA_S:
                        RC.tappa(registro, "tick %d (%d fatti)" % (t, k))
                        t_tappa = adesso
                    blocco = adesso - t_blocco
                    t_blocco = adesso
                    if k < N_TICK and (adesso - t1) + blocco > G2.TETTO_S:
                        print("### il tetto: %.0f s fatti, il prossimo blocco di %d tick (%.0f s) lo supererebbe: ci si ferma a %d tick (dichiarato)" % (adesso - t1, OGNI, blocco, k))
                        break
            secondi = time.time() - t1
            out.update(tick_fatti=fatti, secondi=secondi, fermo=fermo, sha=V.shas(z))
            print("### (%s): %d tick in %.0f s (%.3f s per tick); d da %.6f a %.6f" % (nome, fatti, secondi, secondi / max(1, fatti), S["d"][0], S["d"][-1]))
        mot.geo.U[...] = U0
    salva(nome, out, (S, SP, RH))
    print("### %.0f s in tutto" % (time.time() - t00))
    return 0


def salva(nome, out, serie):
    os.makedirs(DIR_OUT, exist_ok=True)
    f = os.path.join(DIR_OUT, nome + ".npz")
    dati = {"meta": np.array(json.dumps(out, default=str))}
    if serie is not None:
        S, SP, RH = serie
        dati.update(t=np.array(S["t"]), d=np.array(S["d"]), cA=np.array(S["cA"], dtype=np.float64), cB=np.array(S["cB"], dtype=np.float64),
                    M=np.array(S["M"]), V=np.array(S["V"]), rmax=np.array(S["rmax"]), rho=np.stack(RH),
                    t_phi=np.array(SP["t"]), phi2=np.stack(SP["phi2"]), dLambda=np.stack(SP["dLambda"]))
        for k in ("KV", "eB", "G_in", "G_bordo") + tuple(x for x in S if x.startswith("E_")):
            if S[k]:
                dati[k] = np.array(S[k])
    np.savez_compressed(f, **dati)
    mb = os.path.getsize(f) / 1e6
    print("### %s: %.2f MB%s" % (os.path.relpath(f, RADICE), mb, "" if mb <= TETTO_MB else "   ### OLTRE %g MB: FERMO prima del commit" % TETTO_MB))


# =====================================================================================
#   IL REFERTO
# =====================================================================================
def leggi(nome):
    f = os.path.join(DIR_OUT, nome + ".npz")
    if not os.path.exists(f):
        return None
    with np.load(f) as d:
        out = {k: d[k].copy() for k in d.files if k not in ("rho", "phi2", "dLambda")}
        out["meta"] = json.loads(str(d["meta"]))
    return out


def referto():
    import _presidio
    from solitone import carta_coppia as CC
    from solitone import mappe as MP
    from solitone import toro as TO
    _presidio.avvia(__file__)
    B = {b: leggi(b) for b in BRACCI}
    mancano = [b for b in BRACCI if B[b] is None]
    print("=" * 130)
    print("P6, I BRACCI: IL REFERTO (sez. 11.14): %s; mancano %s" % (", ".join("(%s) %d tick" % (b, B[b]["meta"].get("tick_fatti", 0)) for b in BRACCI if B[b] is not None), mancano))
    print("=" * 130)
    assert not mancano, "mancano dei bracci: %s" % mancano
    d0 = B["0"]["meta"]["d0"]
    n_com = min(len(B[b]["t"]) for b in BRACCI)
    tt = B["0"]["t"][:n_com]
    for b in BRACCI:
        assert np.array_equal(B[b]["t"][:n_com], tt), "i tick dei bracci non coincidono"
    tf = (tt - G2.T0).astype(float)
    print("### la durata COMUNE: %d tick (%d punti ogni %d); per braccio: %s" % (int(tf[-1]), n_com, OGNI, ", ".join("(%s) %d" % (b, B[b]["meta"]["tick_fatti"]) for b in BRACCI)))
    for b in BRACCI:
        m = B[b]["meta"]
        print("    (%s): %d tick in %.0f s; d da %.6f a %.6f; il FERMO %s" % (b, m["tick_fatti"], m["secondi"], B[b]["d"][0], B[b]["d"][-1], m.get("fermo")))
    print("-" * 130)
    # ---------------------------------------------------------------- i DEVE
    L = int(B["0"]["meta"]["L"])
    v_ = np.arange(L * L)
    m1, m2 = v_ // L, v_ % L
    from solitone import corsa_accensione as CA
    bor = CA.serie(G2.CORSA)[0][-1]["bordo"]
    x = TO.scarti(m1, m2, bor["c0"][0], bor["c0"][1], L)[:, 0]
    dm = {}
    cartella = os.path.join(MP.RADICE, G2.CORSA)
    for f in sorted(os.listdir(cartella)):
        if f.endswith(".npz"):
            with np.load(os.path.join(cartella, f)) as d:
                T, RH = d["t"], d["rho"]
                for i in range(len(T)):
                    if G2.T0 < int(T[i]) <= G2.T0 + N_TICK:
                        cA, cB = CC.centri_semipiani(RH[i].astype(np.float64), m1, m2, L, x, 0.0)
                        dm[int(T[i])] = float(np.hypot(*CC.vettore(cA, cB, L)))
    t0l = list(B["0"]["t"])
    com = [t for t in t0l if t in dm]
    ed = max(abs(B["0"]["d"][t0l.index(t)] - dm[t]) for t in com) if com else float("inf")
    esito("(0) contro le mappe di C35-pi: d alla stessa ora entro %g" % G2.TOLL_D, len(com) > 0 and ed <= G2.TOLL_D, "%.3e su %d tick" % (ed, len(com)), True)
    diverse = [k for k in B["0"]["meta"]["sha"] if B["0"]["meta"]["sha"][k] != B["0bis"]["meta"]["sha"][k]]
    esito("(0) rifatto = (0) AL BIT (gli sha di ogni chiave alla fine)", not diverse and B["0"]["meta"]["tick_fatti"] == B["0bis"]["meta"]["tick_fatti"], "diverse: %s" % diverse, True)
    with open(os.path.join(REF, "s5_coppia_lapse.txt"), encoding="utf-8") as f:
        testo = f.read()
    g_on = float(re.search(r"### \(on\): 1500 tick in [0-9]+ s; d da [0-9.]+ a ([0-9.]+)", testo).group(1))
    g_off = float(re.search(r"### \(off\): 1500 tick in [0-9]+ s; d da [0-9.]+ a ([0-9.]+)", testo).group(1))
    if B["0"]["meta"]["tick_fatti"] == 1500:
        esito("(0) riproduce (off) di G2: d a 1500 tick = %.6f entro 1e-6" % g_off, abs(B["0"]["d"][-1] - g_off) <= 1e-6, "%.6f" % B["0"]["d"][-1], True)
    if B["G"]["meta"]["tick_fatti"] == 1500:
        esito("(G) riproduce (on) di G2: d a 1500 tick = %.6f entro 1e-6" % g_on, abs(B["G"]["d"][-1] - g_on) <= 1e-6, "%.6f" % B["G"]["d"][-1], True)
    else:
        print("  (G) NON arriva a 1500 tick (%d): il confronto con G2 non si fa" % B["G"]["meta"]["tick_fatti"])
    with open(os.path.join(REF, "p6_u_breve.txt"), encoding="utf-8") as f:
        pb = float(re.search(r"t  60200  d ([0-9.]+) ", f.read()).group(1))
    iu = list(B["U"]["t"]).index(G2.T0 + 200)
    esito("(U) riproduce la prova breve: d a %d = %.6f entro 1e-6" % (G2.T0 + 200, pb), abs(B["U"]["d"][iu] - pb) <= 1e-6, "%.6f" % B["U"]["d"][iu], True)
    esito("l'adattatore di (G+U) a e = 0 = (G) al bit (%d tick)" % N_ADATT, B["GU"]["meta"].get("adattatore_diverse") == [], "diverse: %s" % B["GU"]["meta"].get("adattatore_diverse"), True)
    # ---------------------------------------------------------------- le parabole
    dd0 = B["0"]["d"][:n_com]
    a0, ea0 = CC.curvatura(tf, dd0)
    print("-" * 130)
    print("### la parabola di d_0 da sola: d'' %+.6e +- %.1e (l'errore del fit di (0): la scala della finta)" % (a0, ea0))
    a_f = N_FINTA * ea0
    yy = B["0bis"]["d"][:n_com] + 0.5 * a_f * tf * tf - dd0
    af_m, eaf_m = CC.curvatura(tf, yy)
    esito("(0) rifatto + una finta di %g errori (%.3e), meno (0): compatibile con zero entro 3 max(errore, errore di (0))" % (N_FINTA, a_f), abs(af_m) <= G2.N_ERR * max(eaf_m, ea0),
          "misurata %+.3e +- %.1e" % (af_m, eaf_m), False)
    ris = {}
    print("### d_X - d_0, la parabola (d'' in piu', per tick^2):")
    for b in ("G", "U", "GU", "Uzero"):
        y = B[b]["d"][:n_com] - dd0
        a, ea = CC.curvatura(tf, y)
        ris[b] = (a, ea, y)
        print("    (%-5s) %+.6e +- %.1e (%6.1f errori); d_X - d_0 alla fine %+.4e; ogni %d tick: %s" % (b, a, ea, abs(a) / ea if ea else float("inf"), y[-1], 5 * OGNI, " ".join("%+.2e" % v for v in y[::5])))
    m = B["U"]["meta"]
    d_dec, N, mu, _e2 = PB.dati_di_e()
    a_att = m["e"] ** 2 * N / (2.0 * math.pi * mu * d0)
    print("    (U) contro l'atteso d'' = -2 a = %.6e: il rapporto %.4f (la prova breve: 0.0178)" % (-2 * a_att, ris["U"][0] / (-2 * a_att)))
    ctrl = float(np.max(np.abs(ris["GU"][2])))
    print("  controllo: (G+U) diverso da (0): max |d_GU - d_0| %.3e" % ctrl)
    # ---------------------------------------------------------------- l'energia del toro intero (Luca 13:43)
    print("-" * 130)
    termini = [k[2:] for k in B["0"] if k.startswith("E_")]
    print("### L'ENERGIA DEL TORO INTERO per termini (il libro dei conti), la variazione dal tick %d al tick %d (la durata comune); e_K %.10f" % (G2.T0, int(tt[-1]), B["0"]["meta"]["e_K"]))
    print("    %-6s %s" % ("", "  ".join("%16s" % c for c in termini)))
    for b in BRACCI:
        print("    (%-5s)  all'inizio %s" % (b, "  ".join("%16.9e" % B[b]["E_" + c][0] for c in termini)))
        print("    (%-5s)  la variazione %s" % (b, "  ".join("%+16.9e" % (B[b]["E_" + c][n_com - 1] - B[b]["E_" + c][0]) for c in termini)))
    for b in ("G", "U", "GU", "Uzero"):
        print("    (%-5s) meno (0), la variazione %s" % (b, "  ".join("%+16.9e" % ((B[b]["E_" + c][n_com - 1] - B[b]["E_" + c][0]) - (B["0"]["E_" + c][n_com - 1] - B["0"]["E_" + c][0])) for c in termini)))
    for b in ("U", "GU", "Uzero"):
        if "KV" in B[b]:
            print("    (%-5s) il campo K + V: da %.6e a %.6e" % (b, B[b]["KV"][0], B[b]["KV"][n_com - 1]))
    # ---------------------------------------------------------------- l'additivita' e il rapporto delle forze
    D = ris["GU"][2] - ris["G"][2] - ris["U"][2]
    aD, eaD = CC.curvatura(tf, D)
    print("-" * 130)
    print("### L'ADDITIVITA': [(G+U) - (0)] - [(G) - (0)] - [(U) - (0)]: d'' %+.6e +- %.1e (%.1f errori); alla fine %+.4e; la somma attesa (G) + (U) %+.6e, misurata (G+U) %+.6e"
          % (aD, eaD, abs(aD) / eaD if eaD else float("inf"), D[-1], ris["G"][0] + ris["U"][0], ris["GU"][0]))
    print("### IL RAPPORTO DELLE FORZE (sez. 12.1 f): a_G / a_U = %+.4f (a_G %+.4e, a_U %+.4e), con rho_c %.6f (rho_0 / %g) ed e %.7e"
          % (ris["G"][0] / ris["U"][0], ris["G"][0], ris["U"][0], B["G"]["meta"]["rho_c"], G2.R_LAPSE, m["e"]))
    # ---------------------------------------------------------------- le letture
    print("-" * 130)

    def segno(b):
        a, ea, _y = ris[b]
        return "+" if a > G2.N_ERR * ea else ("-" if a < -G2.N_ERR * ea else "0")
    print("  LE LETTURE (sez. 11.4, a %g errori): (G) %s; (U) %s; (G+U) %s; (U) da zero %s   [+ si allontanano, - si avvicinano, 0 niente oltre %g errori]"
          % (G2.N_ERR, segno("G"), segno("U"), segno("GU"), segno("Uzero"), G2.N_ERR))
    print("  L'ADDITIVITA': %s" % ("entro %g errori: i due campi NON si parlano" % G2.N_ERR if abs(aD) <= G2.N_ERR * eaD else "OLTRE %g errori: i due campi si parlano" % G2.N_ERR))
    print("  (G+U) da una sola distanza: il segno netto %s ((gu1) o (gu2) si decidono con la serie di distanze)" % segno("GU"))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--braccio", choices=BRACCI)
    ap.add_argument("--registro")
    ap.add_argument("--referto", action="store_true")
    x = ap.parse_args(argv)
    if x.referto:
        return referto()
    assert x.braccio, "--braccio o --referto"
    return braccio(x.braccio, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
