# -*- coding: utf-8 -*-
r"""**S5.3 G2: DUE SOLITONI VICINI, LA PRIMA GRAVITA' FRA CORPI A CORTO RAGGIO** *(sul ramo laterale; Luca `2026-11-11` `23:42`-`23:45`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `32.3`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_coppia_lapse.py > doc/referti_l2/s5_coppia_lapse.txt

**La scena:** lo stato di C35-pi a `T0` *(`L 162`; ### `T0` e `R_LAPSE` sono le PROPOSTE (D1) e (D2) della sez. `32.3`, in attesa di Luca)*, **il bordo della corsa dopo ogni tick**
*(`bordo.assorbi` col riferimento `c(t) F3`)*. **Due corse dalla stessa partenza:** **(off)** il tick della corsa *(`accensione.tick`)*; **(on)** il lapse `N(rho)`, `rho_c = rho_0 / R_LAPSE`,
**con la forma (a)** *(`tick_lapse.tick`, `eps_a = eps_top` di T-L4b, letto dal suo referto)*. **`d` dai semipiani** *(`carta_coppia.centri_semipiani`, lo scarto lungo `A1` dal centro del
bordo)* **ogni `50` tick.** **DEVE:** (off) = le mappe di C35-pi *(`d` ogni `100` tick, entro `1e-5`)*. **Il fit:** `d_on - d_off` con la parabola; **le letture (p1)-(p3)** a `3` errori.
"""
import math
import os
import re
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "C35-pi"                    # ### Luca (G2)
T0 = 60000                          # ### (D1), PROPOSTA mia in attesa di Luca: lo stato a 66000 NON esiste (gli stati sono ogni 10000 tick)
R_LAPSE = 1e-2                      # ### (D2), PROPOSTA mia in attesa di Luca: rho_c = rho_0 / 1e-2, come T-L2
N_MAX, OGNI = 5000, 50              # ### Luca (G2): fino a 5000 tick, ogni 50
TETTO_S = 3600.0                    # ### Luca (G2): 60 minuti per corsa
TOLL_D = 1e-5                       # ### mio (dichiarato, sez. 32.3): (off) contro le mappe float32
N_ERR = 3.0                         # ### Luca (p1)-(p3): 3 errori
REF_TL4B = os.path.join(os.path.dirname(os.path.dirname(_QUI)), "doc", "referti_l2", "s5_caduta_segno.txt")
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


def eps_top_tl4b():
    with open(REF_TL4B, encoding="utf-8") as f:
        for riga in f:
            m = re.search(r"la forma \(a\): eps_top = ([0-9.]+) per tick", riga)
            if m:
                return float(m.group(1))
    raise AssertionError("eps_top NON trovato nel referto di T-L4b")


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import corsa_accensione as CA
    from solitone import mappe as MP
    from solitone import tick_lapse as TL
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "accensione", "bordo", "carta_coppia", "mappe", "tick_lapse", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    T_acc, _fine = CA.CORSE[CORSA]
    K = int(round(T_acc / s))
    e0 = eps_top_tl4b()
    rr = CA.serie(CORSA)[0]
    x_st = [x for r in rr for x in (r.get("stati") or []) if x["t"] == T0]
    assert len(x_st) == 1, "lo stato di %s a %d NON e' uno solo nel jsonl" % (CORSA, T0)
    bor = rr[-1]["bordo"]
    t00 = time.time()
    print("=" * 130)
    print("S5.3 G2 (sez. 32.3): due solitoni vicini; lo stato di %s a %d (%s; ### T0 e R_LAPSE proposte (D1), (D2)); s %g; rho_c = rho_0 / %g; eps_a %.10f (T-L4b); fino a %d tick, d ogni %d; il tetto %g s per corsa"
          % (CORSA, T0, x_st[0]["file"], s, R_LAPSE, e0, N_MAX, OGNI, TETTO_S))
    print("  il bordo della corsa: c0 %s, R_A %g, g_max %g" % (bor["c0"], bor["R_A"], bor["g_max"]))
    print("=" * 130)
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
        assert int(d["K"]) == K
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, rec["larghezza"])[0]
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
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
        g_e, _gn, _r = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])
        with np.load(x_st[0]["file"]) as d:
            assert int(d["t"]) == T0
            stato = {k: d[k].copy() for k in chiavi}

        def metti_stato():
            for k in chiavi:
                st[k][...] = stato[k]
            mot.cs, mot.lambda_c = cs_scena, lc_scena

        def rho_di():
            r = np.zeros(n)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            return r

        def d_di(rho):
            cA, cB = CC.centri_semipiani(rho, m1, m2, L, x, 0.0)
            return float(np.hypot(*CC.vettore(cA, cB, L))), cA, cB

        metti_stato()
        assert V.shas(z) == x_st[0]["sha"], "lo stato di %s a %d NON e' quello registrato nel jsonl" % (CORSA, T0)
        r0 = rho_di()
        d0, cA, cB = d_di(r0)
        nuc = []
        for c_ in (cA, cB):
            pos = TO.scarti(m1, m2, c_[0], c_[1], L)
            nuc.append(np.hypot(pos[:, 0], pos[:, 1]) < w_in)
        rho_0 = float(r0[nuc[0] | nuc[1]].mean())
        legge = ("rho_c", rho_0 / R_LAPSE)
        print("### a t %d: d %.6f; i centri (indici) %s, %s; w_in %.6f; rho_0 = la rho media dei due centri (r < w_in) %.6f; rho_c %.6f" % (T0, d0, np.round(cA, 4), np.round(cB, 4), w_in, rho_0, legge[1]))

        def corsa(modo, n_tick):
            metti_stato()
            ds, tt = [d0], [T0]
            for k in range(1, n_tick + 1):
                t = T0 + k
                if modo == "off":
                    AC.tick(z, t, K)
                else:
                    TL.tick(mot, st, par, s, legge, eps_a=e0)
                BO.assorbi(st, g_e, BO.c_di(t, tab_c, K, omega) * phi_v)
                if k % OGNI == 0:
                    ds.append(d_di(rho_di())[0])
                    tt.append(t)
            return np.array(tt), np.array(ds)

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ---------------------------------------------------------------- il tempo di (on): la durata
            t1 = time.time()
            corsa("on", OGNI)
            per_tick = (time.time() - t1) / OGNI
            n_tick = min(N_MAX, int(TETTO_S / per_tick) // OGNI * OGNI)
            print("### (on): %.3f s per tick nei primi %d; la durata %d tick%s" % (per_tick, OGNI, n_tick, "" if n_tick == N_MAX else " (### ridotta dal tetto di %g s, dichiarato)" % TETTO_S))
            t1 = time.time()
            tt, d_off = corsa("off", n_tick)
            print("### (off): %d tick in %.0f s; d da %.6f a %.6f" % (n_tick, time.time() - t1, d_off[0], d_off[-1]))
            t1 = time.time()
            tt2, d_on = corsa("on", n_tick)
            assert np.array_equal(tt, tt2)
            print("### (on): %d tick in %.0f s; d da %.6f a %.6f" % (n_tick, time.time() - t1, d_on[0], d_on[-1]))
        # ---------------------------------------------------------------- DEVE: (off) = C35-pi, dalle mappe
        dm = {}
        cartella = os.path.join(MP.RADICE, CORSA)
        for f in sorted(os.listdir(cartella)):
            if not f.endswith(".npz"):
                continue
            with np.load(os.path.join(cartella, f)) as d:
                T, RH = d["t"], d["rho"]
                for i in range(len(T)):
                    if T0 <= int(T[i]) <= T0 + n_tick:
                        dm[int(T[i])] = d_di(RH[i].astype(np.float64))[0]
        com = [t for t in tt if t in dm]
        ed = max(abs(d_off[list(tt).index(t)] - dm[t]) for t in com)
        print("  (off) contro le mappe di %s: %d tick comuni (ogni 100), lo scarto piu' grande di d %.3e" % (CORSA, len(com), ed))
        esito("(off) ridà C35-pi: d dalle mappe alla stessa ora entro %g" % TOLL_D, len(com) > 0 and ed <= TOLL_D, "%.3e su %d tick" % (ed, len(com)))
        ef = max(abs(d_off[list(tt).index(t)] - dm[t] - 0.01) for t in com)
        esito("lo stesso confronto con d spostato di 0.01", len(com) > 0 and ef <= TOLL_D, "%.3e" % ef, deve=False)
        # ---------------------------------------------------------------- d_on - d_off
        dd = d_on - d_off
        tf = (tt - T0).astype(float)
        a, ea = CC.curvatura(tf, dd)
        print("-" * 130)
        print("### d_on - d_off ogni %d tick (ogni %d stampati): %s" % (OGNI, 10 * OGNI, " ".join("%+.3e" % v for v in dd[::10])))
        print("    la velocita' relativa in piu' (differenza centrata, a meta' e alla fine): %+.3e, %+.3e per tick" % (
            (dd[len(dd) // 2 + 1] - dd[len(dd) // 2 - 1]) / (2 * OGNI), (dd[-1] - dd[-3]) / (2 * OGNI)))
        print("    la parabola: l'accelerazione relativa in piu' %+.6e +- %.1e per tick^2 (%.1f errori)" % (a, ea, abs(a) / ea if ea else float("inf")))
        if a < -N_ERR * ea:
            print("  LA LETTURA: (p1) d_on - d_off scende oltre %g errori: un'attrazione in piu' dall'orologio, fra corpi" % N_ERR)
        elif a > N_ERR * ea:
            print("  LA LETTURA: (p3) d_on - d_off sale oltre %g errori: una repulsione" % N_ERR)
        else:
            print("  LA LETTURA: (p2) nessuna differenza oltre %g errori: con N locale, a questa distanza, non si sentono" % N_ERR)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
