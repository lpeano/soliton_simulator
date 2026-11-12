# -*- coding: utf-8 -*-
r"""**S5.2, T-L4: LA CADUTA DI UN PACCHETTO IN UN `N` ESTERNO** *(sul ramo laterale; Luca `2026-11-11` `11:33`, `13:22`, `17:22`, `18:17`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.15`, `31.19`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_caduta.py > doc/referti_l2/s5_lapse_caduta.txt

**Il vuoto `c(10000) F3` senza il solitone; un pacchetto gaussiano della banda dei solitoni** *(`q` della coppia piu' alta a `Gamma`, la larghezza `8`, `rho` massima `1e-3`)*; **`cs = s N(x)`,
`N = 1 + gamma sin(2 pi i1 / L)` ESTERNO e statico** *(niente reazione)*, **lo zero O1 dei pezzi.** **La previsione del raggio:** `a = -(d^2 eps/dk^2)(d eps/d cs) s dN/dx` *(le due bande della coppia
pesate con la sovrapposizione)*; **la misura:** il baricentro lungo `B_0`, una parabola su `200` tick. **DEVE:** entro il `5%`; il verso si rovescia con `gamma`. **O4: solo previsto.**
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
N_TICK = 200                          # ### sez. 31.19
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
    print("S5.2 T-L4 (sez. 31.19): la caduta; s %g; gamma %s; sigma %g; rho max %g; %d tick; dk %g; h_cs %g" % (s, GAMMI, SIGMA, RHO_MAX, N_TICK, DK, H_CS))
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
            for g in GAMMI:
                Nx = 1.0 + g * np.sin(2 * np.pi * i1 / Lt)
                cs = s * Nx
                a_pred = sum(wq[j] * (-pred[j]["e2"] * pred[j]["dcs"] * s * g * dNds1) for j in range(2))
                metti(psi0, cs)
                xs = []
                for k in range(N_TICK + 1):
                    if k > 0:
                        mot.cs = cs
                        mot.lambda_c = None
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                    rho = np.zeros(n)
                    np.add.at(rho, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
                    xs.append(float(np.sum(rho * (dxc @ bh)) / np.sum(rho)))
                tt = np.arange(N_TICK + 1, dtype=float)
                p = np.polyfit(tt, np.array(xs), 2)
                a_sim = 2.0 * p[0]
                verso = "verso N piu' BASSO" if a_sim * g < 0 else "verso N piu' ALTO"
                ris[g] = a_sim
                print("  gamma %+.3f: lo spostamento lungo B_0 a 50, 100, 200 tick: %+.5f %+.5f %+.5f; a misurata %+.6e, prevista %+.6e (il rapporto %.4f); la velocita' iniziale %+.3e; %s"
                      % (g, xs[50], xs[100], xs[200], a_sim, a_pred, a_sim / a_pred if a_pred else float("nan"), p[1], verso))
                esito("T-L4 gamma %+.3f: l'accelerazione = la previsione del raggio entro il %g%%" % (g, 100 * TOLL), a_pred != 0 and abs(a_sim / a_pred - 1.0) <= TOLL, "il rapporto %.4f" % (a_sim / a_pred if a_pred else float("nan")))
            for g in (0.01, 0.02):
                esito("T-L4: col gradiente rovesciato il verso si rovescia (gamma %+.2f contro %+.2f)" % (g, -g), ris[g] * ris[-g] < 0, "%+.3e, %+.3e" % (ris[g], ris[-g]))
            print("  O4 (solo previsto, sez. 31.19): con lo zero locale una pendenza costante di N non da' potenziale; la forza lineare sparisce, resta un termine ~ (a^2/4) lapl(cs)")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
