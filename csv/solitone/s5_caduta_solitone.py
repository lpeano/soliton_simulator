# -*- coding: utf-8 -*-
r"""**S5.3 G1: LA CADUTA DI UN SOLITONE VERO, CON LA FORMA (a)** *(sul ramo laterale; Luca `2026-11-11` `23:42`-`23:45`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `32.2`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_caduta_solitone.py > doc/referti_l2/s5_caduta_solitone.txt

**La scena:** lo stato di TBS a `10000` tick *(`L 81`; il bordo spento)* nello stesso `N` esterno di T-L4 *(`N = 1 + gamma sin(2 pi (i1 - c1)/L)`, lo zero del seno sul centro
del solitone, dichiarato)*, `cs = s N`, **la forma (a)** *(mezza fase per nodo `e^{+i eps_top (N_k - 1)/2}` su `psi` prima e dopo il tick, come T-L4b)* **e accanto la forma di oggi.**
**Prima della corsa:** `eps_top` *(la cima della coppia a `Gamma`, come T-L4b)*; `E_g = somma_k (h_k - eps_top rho_k)` con `h_k = dE/dN_k` a `N = 1` *(`s (H_k + somma dw/dcs H_a)`,
come `tick_lapse.omega_psi`)*, **col controllo di scala** sul pacchetto di T-L4b *(`somma h / somma rho` = `s d eps / d cs` entro l'`1%`)*; la frequenza del cuore contro `eps_top`.
**Il centro periodico** *(`toro.centro`)* ogni `20` tick, `2000` tick; la parabola. **I DEVE:** il tick del banco a `N = 1` = il tick della corsa *(`accensione.tick`)*; a `N = 1` il centro
non accelera *(`|a| <= 3` errori, la deriva propria e' la parte lineare)*; il verso si rovescia col gradiente. **Le letture (e1)-(e3)** contro le accelerazioni di T-L4b *(lette dal suo referto)*.
"""
import os
import re
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_punto_fisso as CPF  # noqa: E402

CORSA, T_STATO = "TBS", 10000       # ### Luca (G1): lo stato di TBS a 10000
GAMMI = (0.01, -0.01, 0.02, -0.02)  # ### Luca (G1): gli stessi gamma di T-L4
N_TICK, OGNI = 2000, 20             # ### Luca (G1): 2000 tick, il centro ogni 20
TETTO_S = 3600.0                    # ### Luca (G1): il tetto di 60 minuti
TOLL_E1 = 0.10                      # ### Luca (e1): entro il 10%
N_ERR = 3.0                         # ### Luca (G2, e qui per la caduta nulla a N = 1): 3 errori
TOLL_SCALA = 0.01                   # ### mio (dichiarato, sez. 32.2): il controllo di scala di E_g entro l'1%
TOLL_TICK = 1e-12                   # ### mio (dichiarato): il tick del banco = il tick della corsa, relativo
N_TICK_DEVE = 20                    # ### mio: i tick del confronto
SOGLIA_CUORE = 0.5                  # ### mio (dichiarato): il cuore = i nodi con rho > 0.5 rho max
SIGMA, RHO_MAX = 8.0, 1e-3          # ### il pacchetto di T-L4b (sez. 31.19)
DK, H_CS, A_IMP = 0.02, 1e-4, 1e-6  # ### come T-L4b
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


def tl4b():
    """### le accelerazioni della forma (a) di T-L4b, dal suo referto: `{gamma: (a, errore)}`."""
    out = {}
    with open(REF_TL4B, encoding="utf-8") as f:
        for riga in f:
            m = re.match(r"\s+a\s+gamma ([+-][0-9.]+): .*; a ([+-][0-9.e+-]+) \+- ([0-9.e+-]+) ", riga)
            if m:
                out[float(m.group(1))] = (float(m.group(2)), float(m.group(3)))
    assert sorted(out) == sorted(GAMMI), "il referto di T-L4b NON ha i quattro gamma della forma (a): %s" % sorted(out)
    return out


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import composizione as CM
    import energia_pesata as EP
    import tick as TK
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "accensione", "bordo", "carta_punto_fisso", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    T_acc, _fine = CA.CORSE[CORSA]
    K = int(round(T_acc / s))
    assert T_STATO > K, "lo stato e' nella rampa di accensione"
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, Kf = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, Kf, omega)
    rif = tl4b()
    rr = CA.serie(CORSA)[0]
    x_st = [x for r in rr for x in (r.get("stati") or []) if x["t"] == T_STATO]
    assert len(x_st) == 1, "lo stato di %s a %d NON e' uno solo" % (CORSA, T_STATO)
    t00 = time.time()
    print("=" * 130)
    print("S5.3 G1 (sez. 32.2): la caduta di un solitone vero, la forma (a); lo stato di %s a %d (%s); s %g; gamma %s; %d tick, il centro ogni %d; il tetto %g s" % (CORSA, T_STATO, x_st[0]["file"], s, GAMMI, N_TICK, OGNI, TETTO_S))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CPF.CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        n, Lt = inc.n, z["L"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        nodo = np.asarray(inc.nodo)
        forma_psi = st["psi_h"].shape
        vv = np.arange(n)
        i1, i2 = vv // Lt, vv % Lt
        A1, A2 = TO.vettori()
        B = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
        bh = B[0] / np.linalg.norm(B[0])
        d0 = TO.scarti(i1, i2, 0.0, 0.0, Lt)
        cs_scena, lc_scena = mot.cs, getattr(mot, "lambda_c", None)   # ### il motore della scena, rimesso prima del tick della corsa
        with np.load(x_st[0]["file"]) as d:
            assert int(d["t"]) == T_STATO
            stato = {k: d[k].copy() for k in chiavi}
        print("### la scena: L %d; il cs del motore della scena %s; lambda_c %s" % (Lt, "None" if mot.cs is None else "un array", "None" if getattr(mot, "lambda_c", None) is None else "un array"))

        def metti_stato():
            for k in chiavi:
                st[k][...] = stato[k]

        def rho_di():
            r = np.zeros(n)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            return r

        def h_di(cs):
            """### `h_k = dE/dN_k` a `cs` dato: `s (H_k + somma_a dw_a/dcs_k H_a)` *(la struttura di `tick_lapse.omega_psi`)*."""
            mot.cs = cs
            mot.lambda_c = None
            per_nodo, per_arco = EP.termini_di_h(mot, st, par)
            dw = EP.d_peso_arco(mot)
            arco = np.zeros(n)
            np.add.at(arco, nodo, dw * np.repeat(per_arco, 2))
            return s * (per_nodo + arco)

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ---------------------------------------------------------------- eps_top e s d eps/d cs, come T-L4b
            def metti_pacchetto(psi, cs):
                for k in chiavi:
                    st[k][...] = salvato[k]
                st["psi_h"][...] = psi.reshape(forma_psi)
                st["phi_h"][...] = c * phi_v
                mot.cs = cs
                mot.lambda_c = None

            def risposta(cs_val):
                R = np.zeros((n, 12, 12), dtype=complex)
                for j in range(12):
                    us = []
                    for f in (1.0, -1.0):
                        p = np.zeros((n, 12), dtype=complex)
                        p[0, j] = f * A_IMP
                        metti_pacchetto(p, np.full(n, float(cs_val)))
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                        us.append(st["psi_h"].reshape(n, 12).copy())
                    R[:, :, j] = (us[0] - us[1]) / (2 * A_IMP)
                return R

            def A_di(R, kv):
                return np.einsum("x,xij->ij", np.exp(-1j * (d0 @ kv)), R)
            R0 = risposta(s)
            lam, Vv = np.linalg.eig(A_di(R0, np.zeros(2)))
            E = -np.angle(lam)
            o = np.argsort(E)
            top = [int(o[-2]), int(o[-1])]
            e0 = 0.5 * (E[top[0]] + E[top[1]])
            q = np.linalg.qr(Vv[:, top])[0][:, 0]
            q = q / np.linalg.norm(q)

            def cima(R):
                w = -np.angle(np.linalg.eigvals(A_di(R, np.zeros(2))))
                return float(np.sort(w)[-1])
            dcs = (cima(risposta(s * (1 + H_CS))) - cima(risposta(s * (1 - H_CS)))) / (2 * s * H_CS)
            print("### eps_top = %.10f per tick (la coppia %.12f, %.12f); s d eps/d cs = %.6f" % (e0, E[top[0]], E[top[1]], s * dcs))
            # ---------------------------------------------------------------- il controllo di scala di E_g: il pacchetto di T-L4b
            xc = int(np.argmin(np.abs(i1 - 0) * 1000 + np.abs(i2 - Lt // 2)))
            dxc = TO.scarti(i1, i2, float(i1[xc]), float(i2[xc]), Lt)
            env = np.sqrt(RHO_MAX) * np.exp(-np.sum(dxc ** 2, axis=1) / (2 * SIGMA ** 2))
            metti_pacchetto(env[:, None] * q[None, :], np.full(n, s))
            rp = rho_di()
            hp = h_di(np.full(n, s))
            print("### IL PACCHETTO DI T-L4b: la norma %.6e; somma h / somma rho = %.6f (s d eps/d cs %.6f); E_g / norma = %+.6e (atteso s d eps/d cs - eps_top = %+.6e)"
                  % (rp.sum(), hp.sum() / rp.sum(), s * dcs, (hp.sum() - e0 * rp.sum()) / rp.sum(), s * dcs - e0))
            esito("il controllo di scala: per il pacchetto lineare somma h / somma rho = s d eps/d cs entro l'%g%%" % (100 * TOLL_SCALA), abs(hp.sum() / rp.sum() / (s * dcs) - 1.0) <= TOLL_SCALA, "il rapporto %.6f" % (hp.sum() / rp.sum() / (s * dcs)))
            esito("il controllo di scala: lo stesso con s d eps/d cs raddoppiato", abs(hp.sum() / rp.sum() / (2 * s * dcs) - 1.0) <= TOLL_SCALA, "", deve=False)
            # ---------------------------------------------------------------- il solitone: E_g e il cuore
            metti_stato()
            assert V.shas(z) == x_st[0]["sha"], "lo stato di %s a %d NON e' quello registrato nel jsonl" % (CORSA, T_STATO)
            r0 = rho_di()
            h0 = h_di(np.full(n, s))
            metti_stato()
            c1_0, c2_0 = TO.centro(r0, i1, i2, Lt)[:2]
            cuore = r0 > SOGLIA_CUORE * r0.max()
            print("### IL SOLITONE (%s a %d): la norma %.6e; rho max %.4e; il centro (c1, c2) %.4f %.4f; il cuore %d nodi (rho > %g rho max)" % (CORSA, T_STATO, r0.sum(), r0.max(), c1_0, c2_0, int(cuore.sum()), SOGLIA_CUORE))
            print("    somma h = %+.6e; E_g = somma (h - eps_top rho) = %+.6e; per unita' di norma %+.6e (il pacchetto di T-L4b: %+.6e; il rapporto %.4f)"
                  % (h0.sum(), h0.sum() - e0 * r0.sum(), (h0.sum() - e0 * r0.sum()) / r0.sum(), (hp.sum() - e0 * rp.sum()) / rp.sum(),
                     ((h0.sum() - e0 * r0.sum()) / r0.sum()) / ((hp.sum() - e0 * rp.sum()) / rp.sum())))
            # ---------------------------------------------------------------- DEVE: il tick del banco a N = 1 = il tick della corsa
            metti_stato()
            mot.cs, mot.lambda_c = cs_scena, lc_scena
            for t in range(T_STATO + 1, T_STATO + N_TICK_DEVE + 1):
                AC.tick(z, t, K)
            corsa_psi, corsa_phi = st["psi_h"].copy(), st["phi_h"].copy()
            metti_stato()
            psi_t = [st["psi_h"].reshape(n, 12).copy()]
            for t in range(N_TICK_DEVE):
                mot.cs = np.full(n, s)
                mot.lambda_c = None
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                psi_t.append(st["psi_h"].reshape(n, 12).copy())
            dd = max(float(np.max(np.abs(st["psi_h"] - corsa_psi)) / np.max(np.abs(corsa_psi))), float(np.max(np.abs(st["phi_h"] - corsa_phi)) / np.max(np.abs(corsa_phi))))
            esito("il tick del banco a N = 1 (cs = s, lambda_c None) = il tick della corsa (accensione.tick), %d tick, entro %g" % (N_TICK_DEVE, TOLL_TICK), dd <= TOLL_TICK,
                  "%.3e (al bit: %s)" % (dd, np.array_equal(st["psi_h"], corsa_psi) and np.array_equal(st["phi_h"], corsa_phi)))
            om = [float(-np.angle(np.vdot(psi_t[k][cuore], psi_t[k + 1][cuore]))) for k in range(N_TICK_DEVE)]
            print("### IL CUORE: la frequenza per tick %.10f (min %.10f, max %.10f su %d tick); eps_top %.10f; lo spostamento di legame omega - eps_top = %+.6e"
                  % (float(np.mean(om)), min(om), max(om), N_TICK_DEVE, e0, float(np.mean(om)) - e0))
            # ---------------------------------------------------------------- le cadute
            ris = {}
            t_corsa = time.time()

            def caduta(forma, g):
                Nx = 1.0 + g * np.sin(2 * np.pi * (i1 - c1_0) / Lt)
                cs = s * Nx
                mezza = np.exp(1j * e0 * (Nx - 1.0) * 0.5)[nodo][:, None]
                metti_stato()
                xs = []
                for k in range(N_TICK + 1):
                    if k > 0:
                        if forma == "a":
                            st["psi_h"][...] = st["psi_h"] * mezza
                        mot.cs = cs
                        mot.lambda_c = None
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                        if forma == "a":
                            st["psi_h"][...] = st["psi_h"] * mezza
                    if k % OGNI == 0:
                        c1, c2 = TO.centro(rho_di(), i1, i2, Lt)[:2]
                        dc1 = ((c1 - c1_0 + 0.5 * Lt) % Lt) - 0.5 * Lt
                        dc2 = ((c2 - c2_0 + 0.5 * Lt) % Lt) - 0.5 * Lt
                        xs.append(float((dc1 * np.asarray(A1) + dc2 * np.asarray(A2)) @ bh))
                tt = np.arange(0, N_TICK + 1, OGNI, dtype=float)
                p, cov = np.polyfit(tt, np.array(xs), 2, cov=True)
                return 2.0 * p[0], 2.0 * float(np.sqrt(cov[0, 0])), p[1], xs
            stima = None
            for forma, g in [("a", 0.0)] + [(f_, g_) for f_ in ("a", "oggi") for g_ in GAMMI]:
                if stima is not None and time.time() - t_corsa + stima > TETTO_S:
                    print("  ### il tetto di %g s: %s gamma %+.3f NON corsa (dichiarato)" % (TETTO_S, forma, g))
                    continue
                t1 = time.time()
                ris[(forma, g)] = caduta(forma, g)
                stima = time.time() - t1
                a, ea, v0, xs = ris[(forma, g)]
                print("  %-5s gamma %+.3f: lo spostamento lungo B_0 a 500, 1000, 2000 tick %+.5f %+.5f %+.5f; la velocita' iniziale %+.4e; a %+.6e +- %.1e (%.1f errori); %.0f s"
                      % (forma, g, xs[500 // OGNI], xs[1000 // OGNI], xs[-1], v0, a, ea, abs(a) / ea if ea else float("inf"), stima))
            a00, e00 = ris[("a", 0.0)][:2]
            esito("a N = 1 il centro non accelera: |a| <= %g errori (la deriva propria e' la parte lineare)" % N_ERR, abs(a00) <= N_ERR * e00, "a %+.3e +- %.1e" % (a00, e00))
            netto = {}
            for forma in ("a", "oggi"):
                for g in GAMMI:
                    if (forma, g) in ris:
                        a, ea = ris[(forma, g)][:2]
                        netto[(forma, g)] = (a - a00, float(np.hypot(ea, e00)))
            for forma in ("a", "oggi"):
                for g in (0.01, 0.02):
                    if (forma, g) in netto and (forma, -g) in netto:
                        esito("%s: col gradiente rovesciato il verso si rovescia (gamma %+.2f), al netto di N = 1" % (forma, g), netto[(forma, g)][0] * netto[(forma, -g)][0] < 0,
                              "%+.3e, %+.3e" % (netto[(forma, g)][0], netto[(forma, -g)][0]))
            # ---------------------------------------------------------------- le letture
            print("-" * 130)
            print("### LE ACCELERAZIONI NETTE (meno N = 1) CONTRO T-L4b (la forma (a), il pacchetto)")
            ra = []
            for g in GAMMI:
                if ("a", g) not in netto:
                    continue
                a, ea = netto[("a", g)]
                ar, er = rif[g]
                ra.append((g, a, ea, a / ar, abs(a / ar) * float(np.hypot(ea / a, er / ar))))
                print("    gamma %+.3f: il solitone %+.6e +- %.1e (%s); T-L4b %+.6e +- %.1e; il rapporto %.4f +- %.4f; la forma di oggi %s"
                      % (g, a, ea, "verso N piu' BASSO" if a * g < 0 else "verso N piu' ALTO", ar, er, ra[-1][3], ra[-1][4],
                         ("%+.6e" % netto[("oggi", g)][0]) if ("oggi", g) in netto else "-"))
            if not ra or all(abs(x[1]) < N_ERR * x[2] for x in ra):
                print("  LA LETTURA: (e3) nessuna caduta misurabile (sotto %g errori)" % N_ERR)
            elif all(x[1] * x[0] < 0 for x in ra):
                if all(abs(x[3] - 1.0) <= TOLL_E1 for x in ra):
                    print("  LA LETTURA: (e1) il solitone cade verso N piu' basso con la STESSA accelerazione dei pacchetti di T-L4b entro il %g%%: l'equivalenza regge per un corpo legato" % (100 * TOLL_E1))
                else:
                    print("  LA LETTURA: (e2) verso N piu' basso, un'accelerazione DIVERSA: i rapporti %s" % ", ".join("%.4f +- %.4f" % (x[3], x[4]) for x in ra))
            elif all(x[1] * x[0] > 0 for x in ra):
                print("  LA LETTURA: (e3) verso N piu' ALTO")
            else:
                print("  LA LETTURA: caso intermedio (i versi non concordano)")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
