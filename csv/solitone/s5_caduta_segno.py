# -*- coding: utf-8 -*-
r"""**S5.2-bis, T-L4b: LA CADUTA COL SEGNO DELL'INERZIA** *(sul ramo laterale; Luca `2026-11-11` `22:26`-`22:28`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.22`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_caduta_segno.py > doc/referti_l2/s5_caduta_segno.txt

**La scena di T-L4** *(`s5_caduta.py`)*: **la forma (a)** -- `E_N = somma N h - eps_top somma (N - 1) rho`, cioe' una fase per nodo `e^{+i eps_top (N_k - 1)/2}` su `psi` prima e dopo il tick
*(a `N = 1` il tick di oggi al bit)* -- **accanto alla forma di oggi**; `400` tick; **la previsione del raggio** all'ordine zero e con la larghezza; **il principio di equivalenza** *(`sigma 8`, `sigma 8` ampiezza doppia,
`sigma 12`)*; **le letture (f1)-(f3).** **La forma (b) non si corre: da' (f2) per costruzione** *(sez. `31.22`)*.
"""
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_punto_fisso as CPF  # noqa: E402

GAMMI = (0.01, -0.01, 0.02, -0.02)   # ### sez. 31.19
SIGMA = 8.0                           # ### sez. 31.19
RHO_MAX = 1e-3                        # ### sez. 31.19
N_TICK = 400                          # ### sez. 31.22 (era 200 in T-L4)
TOLL_EQ = 0.05                        # ### Luca: il principio di equivalenza entro il 5%
TOLL_F1 = 0.15                        # ### Luca (f1): entro il 15%
N_ERR_F3 = 3.0                        # ### sez. 31.22 (f3): l'accelerazione sotto 3 volte il suo errore
DK = 0.02                             # ### sez. 31.19
H_CS = 1e-4                           # ### sez. 31.19
A_IMP = 1e-6                          # ### l'impulso del tick lineare
TOLL = 0.05                           # ### Luca: entro il 5%
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


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import composizione as CM
    import tick as TK
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "bordo", "carta_punto_fisso", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    t00 = time.time()
    print("=" * 130)
    print("S5.2-bis T-L4b (sez. 31.22): la caduta col segno dell'inerzia, la forma (a); s %g; gamma %s; sigma %g; rho max %g; %d tick; dk %g; h_cs %g" % (s, GAMMI, SIGMA, RHO_MAX, N_TICK, DK, H_CS))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
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
        d0 = TO.scarti(i1, i2, 0.0, 0.0, Lt)                      # ### lo spostamento di ogni nodo dal nodo 0 (l'immagine piu' vicina)

        def metti(psi, cs):
            for k in chiavi:
                st[k][...] = salvato[k]
            st["psi_h"][...] = psi.reshape(forma_psi)
            st["phi_h"][...] = c * phi_v
            mot.cs = cs
            mot.lambda_c = None

        def risposta(cs_val):
            """### `R[x, i, j]`: il tick lineare di `psi` *(complesso)* a `cs` uniforme, dalla cella del nodo `0`."""
            R = np.zeros((n, 12, 12), dtype=complex)
            for j in range(12):
                us = []
                for f in (1.0, -1.0):
                    p = np.zeros((n, 12), dtype=complex)
                    p[0, j] = f * A_IMP
                    metti(p, np.full(n, float(cs_val)))
                    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                    us.append(st["psi_h"].reshape(n, 12).copy())
                R[:, :, j] = (us[0] - us[1]) / (2 * A_IMP)
            return R

        def A_di(R, kv):
            return np.einsum("x,xij->ij", np.exp(-1j * (d0 @ kv)), R)

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            R0 = risposta(s)
            G = A_di(R0, np.zeros(2))
            lam, Vv = np.linalg.eig(G)
            E = -np.angle(lam)
            o = np.argsort(E)
            top = [int(o[-2]), int(o[-1])]
            Qm = np.linalg.qr(Vv[:, top])[0]
            q = Qm[:, 0] / np.linalg.norm(Qm[:, 0])
            print("### la coppia piu' alta a Gamma: eps %.12f, %.12f (la differenza %.2e); q = la prima colonna" % (E[top[0]], E[top[1]], E[top[1]] - E[top[0]]))

            def bande(A):
                w, vr = np.linalg.eig(A)
                vr = vr / np.linalg.norm(vr, axis=0)
                ov = np.abs(vr.conj().T @ q) ** 2
                o2 = np.argsort(-ov)[:2]
                return [(float(-np.angle(w[b])), float(ov[b]), vr[:, b]) for b in o2]
            b0 = bande(G)
            bp = bande(A_di(R0, DK * bh))
            bm = bande(A_di(R0, -DK * bh))
            Rp, Rm = risposta(s * (1 + H_CS)), risposta(s * (1 - H_CS))
            cp, cm = bande(A_di(Rp, np.zeros(2))), bande(A_di(Rm, np.zeros(2)))
            # ### le bande a k = +-dk: si appaiano per sovrapposizione con quelle a k = 0
            # ### a Gamma la coppia e' DEGENERE (gli autovettori non sono unici): le bande si definiscono a k = +dk, dove si separano, e si appaiano a -dk per sovrapposizione
            e0 = 0.5 * (b0[0][0] + b0[1][0])
            dcs = (max(cp, key=lambda x: x[1])[0] - max(cm, key=lambda x: x[1])[0]) / (2 * s * H_CS)
            pred = []
            for jb in range(2):
                v = bp[jb][2]
                ep = bp[jb][0]
                em = max(bm, key=lambda x: abs(np.vdot(x[2], v)))[0]
                e2 = (ep - 2 * e0 + em) / DK ** 2
                e1 = (ep - em) / (2 * DK)
                pred.append({"e0": e0, "e1": e1, "e2": e2, "dcs": dcs})
            wq = [abs(np.vdot(bp[j][2], q)) ** 2 for j in range(2)]
            wq = [x / sum(wq) for x in wq]
            for jb in range(2):
                p_ = pred[jb]
                print("    la banda %d: eps(0) %+.10f; d eps/dk %+.4e; d2 eps/dk2 %+.6e; d eps/d cs %+.6f; il peso di q a k = dk %.4f" % (jb, p_["e0"], p_["e1"], p_["e2"], p_["dcs"], wq[jb]))
            dNds1 = float(np.linalg.norm(B[0])) / Lt          # ### |grad N| per gamma = 1, dove il seno passa per zero
            xc = int(np.argmin(np.abs(i1 - 0) * 1000 + np.abs(i2 - Lt // 2)))
            dxc = TO.scarti(i1, i2, float(i1[xc]), float(i2[xc]), Lt)
            env = np.sqrt(RHO_MAX) * np.exp(-np.sum(dxc ** 2, axis=1) / (2 * SIGMA ** 2))
            psi0 = env[:, None] * q[None, :]
            print("### il pacchetto: centrato sul nodo %d (i1 %d, i2 %d), rho max %.3e, la norma %.6e; |grad N| / gamma = %.6f lungo B_0" % (xc, i1[xc], i2[xc], float(np.max(np.sum(np.abs(psi0) ** 2, axis=1))), float(np.sum(np.abs(psi0) ** 2)), dNds1))
            ris = {}

            def caduta(forma, g, sig, amp):
                """### `(a, errore, la velocita', xs, sha)`: `forma` "oggi" o "a"; `400` tick; il baricentro lungo `B_0`."""
                Nx = 1.0 + g * np.sin(2 * np.pi * i1 / Lt)
                cs = s * Nx
                env = amp * np.sqrt(RHO_MAX) * np.exp(-np.sum(dxc ** 2, axis=1) / (2 * sig ** 2))
                metti(env[:, None] * q[None, :], cs)
                mezza = np.exp(1j * e0 * (Nx - 1.0) * 0.5)[nodo][:, None]
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
                    rho = np.zeros(n)
                    np.add.at(rho, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
                    xs.append(float(np.sum(rho * (dxc @ bh)) / np.sum(rho)))
                tt = np.arange(N_TICK + 1, dtype=float)
                p, cov = np.polyfit(tt, np.array(xs), 2, cov=True)
                import hashlib
                hsh = hashlib.sha1(np.ascontiguousarray(st["psi_h"]).tobytes()).hexdigest()[:16]
                return 2.0 * p[0], 2.0 * float(np.sqrt(cov[0, 0])), p[1], xs, hsh

            def previsione(forma, g, sig):
                """### all'ordine zero (`k = 0`) e con la larghezza (`<eps> = eps_0 + eps''/(2 sigma^2)`), pesate sulle due bande."""
                out = []
                for corr in (False, True):
                    a = 0.0
                    for j in range(2):
                        p_ = pred[j]
                        fatt = (1.0 + p_["e2"] / (2.0 * sig ** 2 * p_["e0"])) if corr else 1.0
                        dOdN = s * p_["dcs"] * fatt - (p_["e0"] if forma == "a" else 0.0)
                        a += wq[j] * (-p_["e2"] * dOdN * g * dNds1)
                    out.append(a)
                return out
            print("### la forma (a): eps_top = %.10f per tick (la cima della coppia a Gamma); s d eps/d cs = %.6f; la differenza %+.4e" % (e0, s * pred[0]["dcs"], s * pred[0]["dcs"] - e0))
            # ---------------------------------------------------------------- N = 1: la forma (a) e' il tick di oggi al bit
            a_o0, ea_o0, _v, _x, h_o = caduta("oggi", 0.0, SIGMA, 1.0)
            a_a0, ea_a0, _v, _x, h_a = caduta("a", 0.0, SIGMA, 1.0)
            print("  gamma 0 (N = 1): oggi a %+.4e +- %.1e, sha %s; la forma (a) a %+.4e +- %.1e, sha %s" % (a_o0, ea_o0, h_o, a_a0, ea_a0, h_a))
            esito("T-L4b: a N = 1 la forma (a) e' il tick di oggi AL BIT (lo sha di psi dopo %d tick)" % N_TICK, h_o == h_a, "")
            esito("T-L4b: a N = 1 l'accelerazione della forma (a) = quella di oggi", a_o0 == a_a0, "%+.4e, %+.4e" % (a_o0, a_a0))
            # ---------------------------------------------------------------- i quattro gamma, la forma (a) e quella di oggi
            for forma in ("oggi", "a"):
                for g in GAMMI:
                    a_s, ea, v0, xs, _h = caduta(forma, g, SIGMA, 1.0)
                    p0, pw = previsione(forma, g, SIGMA)
                    ris[(forma, g)] = (a_s, ea, pw)
                    verso = "verso N piu' BASSO" if a_s * g < 0 else "verso N piu' ALTO"
                    print("  %-5s gamma %+.3f: lo spostamento a 100, 200, 400 tick %+.5f %+.5f %+.5f; a %+.6e +- %.1e (%.1f errori); prevista %+.6e (ordine zero) e %+.6e (con la larghezza); il rapporto %.4f; %s"
                          % (forma, g, xs[100], xs[200], xs[400], a_s, ea, abs(a_s) / ea, p0, pw, a_s / pw if pw else float("nan"), verso))
                for g in (0.01, 0.02):
                    esito("T-L4b %s: col gradiente rovesciato il verso si rovescia (gamma %+.2f)" % (forma, g), ris[(forma, g)][0] * ris[(forma, -g)][0] < 0, "%+.3e, %+.3e" % (ris[(forma, g)][0], ris[(forma, -g)][0]))
            # ---------------------------------------------------------------- il principio di equivalenza
            print("### IL PRINCIPIO DI EQUIVALENZA, la forma (a), gamma 0.02: tre pacchetti")
            eq = []
            for nome, sig, amp in (("sigma 8", SIGMA, 1.0), ("sigma 8, l'ampiezza doppia", SIGMA, 2.0), ("sigma 12", 12.0, 1.0)):
                a_s, ea, v0, xs, _h = caduta("a", 0.02, sig, amp)
                pw = previsione("a", 0.02, sig)[1]
                eq.append(a_s)
                print("    %-27s a %+.6e +- %.1e; prevista con la larghezza %+.6e" % (nome, a_s, ea, pw))
            sc = max(abs(x / eq[0] - 1.0) for x in eq)
            esito("T-L4b: il principio di equivalenza, i tre pacchetti con la stessa accelerazione entro il %g%%" % (100 * TOLL_EQ), sc <= TOLL_EQ, "lo scarto piu' grande %.4f" % sc)
            # ---------------------------------------------------------------- le letture
            print("-" * 130)
            ra = [ris[("a", g)] for g in GAMMI]
            if all(abs(a_s) < N_ERR_F3 * ea for a_s, ea, pw in ra):
                print("  LA LETTURA: (f3) nessuna forza misurabile con la forma (a) (sotto %g errori)" % N_ERR_F3)
            elif all(a_s * g < 0 for (a_s, ea, pw), g in zip(ra, GAMMI)):
                dentro = all(abs(a_s / pw - 1.0) <= TOLL_F1 for a_s, ea, pw in ra)
                print("  LA LETTURA: %s il pacchetto va verso N piu' BASSO; i rapporti con la previsione (con la larghezza) %s" % ("(f1)" if dentro else "verso giusto ma NON (f1): l'ampiezza fuori dal 15%;", ", ".join("%.3f" % (a_s / pw) for a_s, ea, pw in ra)))
            elif all(a_s * g > 0 for (a_s, ea, pw), g in zip(ra, GAMMI)):
                print("  LA LETTURA: (f2) va ancora verso N piu' alto: il segno dell'inerzia non basta")
            else:
                print("  LA LETTURA: caso intermedio (i versi non concordano)")
            print("  la forma (b) (il segno della materia rovesciato tutto insieme): (f2) per costruzione, non corsa (sez. 31.22)")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
