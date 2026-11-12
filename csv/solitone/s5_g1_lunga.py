# -*- coding: utf-8 -*-
r"""**LA G1 LUNGA COL VUOTO** *(Luca `2026-11-12` `15:12`, `17:05`, `19:05`; fuori dal nucleo, nessun cambio di legge, nessuna taratura)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_g1_lunga.py > doc/referti_l2/campo_g1_lunga/referto.txt

**La scena e la caduta di G1 con le componenti** *(`s5_caduta_solitone_componenti.py`, non modificato: la scena, `eps_top` e il ciclo della forma (a) sono COPIATI di la', dichiarato; il DEVE sui
primi `2000` tick controlla che siano gli stessi)*: **TBS a `10000`, `L 81`, `s 0.15`, la forma (a), `gamma +0.02`, `5000` tick.**
**Le uscite** *(`doc/referti_l2/campo_g1_lunga/g1_lunga.npz`)*: **`rho` ogni `20` tick** *(`float32`, `81 x 81`)* **e il centro; le `6` `|phi_j|^2` e `dLambda` ogni `100` tick; `N`.**
**Il referto, ogni `500` tick: il profilo dell'anello vecchio nel SOLO semipiano opposto al moto** *(i nodi con `(x - x0) . u < 0`, `x0` la posizione iniziale della materia, `u` il versore
dello spostamento del centro fino a quel tick; a `t = 0` il versore di `B_0`, dichiarato)*, **`R 10`-`22` dalla posizione iniziale, anelli di larghezza `1`: il raggio del minimo di `dphi` medio, la
profondita'** *(quel minimo)*, **il deficit** *(la somma di `max(-dphi, 0)` sull'anello `10`-`22` del semipiano)*; `dphi = somma_j |phi_j|^2 - 6`.
### **Le letture, scritte PRIMA** *(Luca `17:05`)*: **(v1) RESTA: la profondita' entro il `5%` di quella a `2000` fino a `5000`; (v2) EVAPORA: cala in modo regolare, con un tempo di vita stimato**
*(la retta della profondita' contro il tempo da `2000` a `5000`: dove arriva a zero)*; **(v3) RESIDUO: cala oltre il `5%` e poi si ferma** *(`4500` e `5000` entro il `5%`)*.
### **I DEVE:** **i primi `2000` tick uguali a `e5c4b62b`** *(`rho` e `|phi_j|^2` entro `1e-6` relativo negli stessi tick; `rho` sui nodi con `rho > 1e-6 rho max`)*; **la norma costante entro
`1e-10`; oltre `60 MB` per npz: FERMO prima del commit.** **DEVE FALLIRE:** **lo stesso confronto con i fotogrammi di `e5c4b62b` spostati di uno.**
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_punto_fisso as CPF  # noqa: E402
from solitone import s5_caduta_solitone as G1  # noqa: E402  (NON modificato)

GAMMA = 0.02                    # ### Luca 15:12
N_LUNGA = 5000                  # ### Luca 15:12
OGNI_RHO, OGNI_PHI, OGNI_PROF = 20, 100, 500   # ### Luca 15:12, 17:05
R_PROF = (10, 22)               # ### Luca 17:05
TOLL_V1 = 0.05                  # ### Luca 17:05: entro il 5%
TOLL_RHO = 1e-6                 # ### Luca 17:05
SOGLIA_RHO = 1e-6               # ### come in G1 con le componenti
TOLL_NORMA = 1e-10
TETTO_MB = 60.0                 # ### Luca 17:05
RADICE = os.path.dirname(os.path.dirname(_QUI))
DIR_OUT = os.path.join(RADICE, "doc", "referti_l2", "campo_g1_lunga")
NPZ_RIF = os.path.join(RADICE, "doc", "referti_l2", "campo_g1_componenti", "g1_comp_gamma020.npz")   # ### e5c4b62b
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
    for m in ("__init__", "corsa_accensione", "bordo", "carta_punto_fisso", "toro", "s5_caduta_solitone"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali"):
        _presidio.avvia(os.path.join(RADICE, "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, Kf = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, Kf, omega)
    rr = CA.serie(G1.CORSA)[0]
    x_st = [x for r in rr for x in (r.get("stati") or []) if x["t"] == G1.T_STATO]
    assert len(x_st) == 1
    t00 = time.time()
    print("=" * 130)
    print("LA G1 LUNGA COL VUOTO (Luca 2026-11-12 15:12, 17:05, 19:05): lo stato di %s a %d; s %g; gamma %+g; %d tick; rho ogni %d, |phi_j|^2 e dLambda ogni %d; il profilo ogni %d" % (
        G1.CORSA, G1.T_STATO, s, GAMMA, N_LUNGA, OGNI_RHO, OGNI_PHI, OGNI_PROF))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(G1.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
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
        righe = np.arange(6 * n)
        idx = 2 * ((righe // 2) % 3) + righe % 2

        def phi2_di():
            tmp = np.zeros((n, 6))
            np.add.at(tmp, (nodo, idx), np.abs(st["phi_h"]) ** 2)
            return tmp.T.copy()

        def rho_di():
            r = np.zeros(n)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            return r

        with np.load(x_st[0]["file"]) as d:
            assert int(d["t"]) == G1.T_STATO
            stato = {k: d[k].copy() for k in chiavi}

        def metti_stato():
            for k in chiavi:
                st[k][...] = stato[k]

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            def metti_pacchetto(psi, cs):
                for k in chiavi:
                    st[k][...] = salvato[k]
                st["psi_h"][...] = psi.reshape(forma_psi)
                st["phi_h"][...] = c * phi_v
                mot.cs = cs
                mot.lambda_c = None
            R = np.zeros((n, 12, 12), dtype=complex)
            for j in range(12):
                us = []
                for f in (1.0, -1.0):
                    p = np.zeros((n, 12), dtype=complex)
                    p[0, j] = f * G1.A_IMP
                    metti_pacchetto(p, np.full(n, s))
                    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                    us.append(st["psi_h"].reshape(n, 12).copy())
                R[:, :, j] = (us[0] - us[1]) / (2 * G1.A_IMP)
            A0 = np.einsum("x,xij->ij", np.exp(-1j * (d0 @ np.zeros(2))), R)
            E = np.sort(-np.angle(np.linalg.eigvals(A0)))
            e0 = 0.5 * (E[-1] + E[-2])
            print("### eps_top = %.10f per tick" % e0)
            metti_stato()
            assert V.shas(z) == x_st[0]["sha"], "lo stato NON e' quello registrato"
            r0 = rho_di()
            c1_0, c2_0 = TO.centro(r0, i1, i2, Lt)[:2]
            Nx = 1.0 + GAMMA * np.sin(2 * np.pi * (i1 - c1_0) / Lt)
            cs = s * Nx
            mezza = np.exp(1j * e0 * (Nx - 1.0) * 0.5)[nodo][:, None]
            metti_stato()
            tr, RH, cen, norme, tp, F2, DL = [], [], [], [], [], [], []
            lam0 = None
            t1 = time.time()
            for k in range(N_LUNGA + 1):
                if k > 0:
                    st["psi_h"][...] = st["psi_h"] * mezza
                    mot.cs = cs
                    mot.lambda_c = None
                    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                    st["psi_h"][...] = st["psi_h"] * mezza
                if k % OGNI_RHO == 0:
                    rho = rho_di()
                    tr.append(k)
                    RH.append(rho.reshape(Lt, Lt).astype(np.float32))
                    cen.append(TO.centro(rho, i1, i2, Lt)[:2])
                    norme.append(float(rho.sum()))
                if k % OGNI_PHI == 0:
                    f2 = phi2_di()
                    lam = f2.sum(axis=0)
                    if lam0 is None:
                        lam0 = lam.copy()
                    tp.append(k)
                    F2.append(f2.reshape(6, Lt, Lt).astype(np.float32))
                    DL.append((lam - lam0).reshape(Lt, Lt).astype(np.float32))
            print("### %d tick in %.0f s" % (N_LUNGA, time.time() - t1))
    os.makedirs(DIR_OUT, exist_ok=True)
    f = os.path.join(DIR_OUT, "g1_lunga.npz")
    tr, tp, RH, F2, cen, norme = np.array(tr), np.array(tp), np.stack(RH), np.stack(F2), np.array(cen, dtype=np.float64), np.array(norme)
    np.savez_compressed(f, t_rho=tr, rho=RH, centro=cen, t_phi=tp, phi2=F2, dLambda=np.stack(DL), N=Nx.reshape(Lt, Lt).astype(np.float32))
    mb = os.path.getsize(f) / 1e6
    print("  %s: %.2f MB; %d fotogrammi di rho, %d di phi" % (os.path.relpath(f, RADICE), mb, len(tr), len(tp)))
    print("-" * 130)
    # ---------------------------------------------------------------- il profilo dell'anello vecchio, nel semipiano opposto al moto
    from solitone import toro as TO
    X0 = TO.scarti(i1, i2, c1_0, c2_0, Lt)
    R0 = np.hypot(X0[:, 0], X0[:, 1])
    print("### IL PROFILO DELL'ANELLO VECCHIO (il semipiano opposto al moto, R %d-%d dalla posizione iniziale; anelli di larghezza 1; dphi = somma |phi_j|^2 - 6)" % R_PROF)
    prof = {}
    for t in range(0, N_LUNGA + 1, OGNI_PROF):
        jp = int(np.where(tp == t)[0][0])
        jr = int(np.where(tr == t)[0][0])
        sp = TO.scarti(np.array([cen[jr][0]]), np.array([cen[jr][1]]), c1_0, c2_0, Lt)[0]
        u = sp / np.linalg.norm(sp) if np.linalg.norm(sp) > 0.5 else bh
        semi = (X0 @ u) < 0
        dphi = F2[jp].reshape(6, -1).astype(np.float64).sum(axis=0) - 6.0
        medie = []
        for r in range(R_PROF[0], R_PROF[1]):
            m = semi & (R0 >= r) & (R0 < r + 1)
            medie.append(float(dphi[m].mean()))
        i_min = int(np.argmin(medie))
        m_an = semi & (R0 >= R_PROF[0]) & (R0 < R_PROF[1])
        deficit = float(np.maximum(-dphi[m_an], 0.0).sum())
        prof[t] = (R_PROF[0] + i_min + 0.5, medie[i_min], deficit)
        print("  tick %4d: il raggio del minimo %.1f, la profondita' %+.4f, il deficit %.1f; il centro della materia %.3f %.3f (u %+.3f %+.3f)" % (
            t, prof[t][0], prof[t][1], prof[t][2], cen[jr][0], cen[jr][1], u[0], u[1]))
    print("-" * 130)
    # ---------------------------------------------------------------- le letture v1-v3
    ts = [t for t in prof if t >= 2000]
    d2 = prof[2000][1]
    rap = {t: prof[t][1] / d2 for t in ts}
    print("  la profondita' rispetto a quella a 2000: %s" % ", ".join("%d %.4f" % (t, rap[t]) for t in ts))
    if all(abs(rap[t] - 1.0) <= TOLL_V1 for t in ts):
        print("  LA LETTURA: (v1) RESTA: la profondita' entro il %g%% di quella a 2000 fino a %d" % (100 * TOLL_V1, N_LUNGA))
    else:
        tt = np.array(ts, dtype=float)
        dd = np.array([prof[t][1] for t in ts])
        a, b = np.polyfit(tt, dd, 1)
        vita = (-b / a - 2000.0) if a != 0 and -b / a > 2000.0 else float("nan")
        mono = all(abs(prof[ts[i + 1]][1]) <= abs(prof[ts[i]][1]) for i in range(len(ts) - 1))
        if abs(rap[N_LUNGA] - rap[N_LUNGA - OGNI_PROF]) <= TOLL_V1 * abs(rap[N_LUNGA - OGNI_PROF]) and abs(rap[N_LUNGA] - 1.0) > TOLL_V1 and not mono:
            print("  LA LETTURA: (v3) RESIDUO: cala oltre il %g%% e poi si ferma (%d e %d entro il %g%%)" % (100 * TOLL_V1, N_LUNGA - OGNI_PROF, N_LUNGA, 100 * TOLL_V1))
        elif mono:
            print("  LA LETTURA: (v2) EVAPORA: cala in modo regolare; la retta dal 2000: %+.3e per tick; il tempo di vita stimato dopo 2000: %.0f tick" % (a, vita))
        else:
            print("  LA LETTURA: caso intermedio (ne' v1, ne' v2, ne' v3 come scritte); la retta dal 2000 %+.3e per tick" % a)
    print("-" * 130)
    # ---------------------------------------------------------------- i DEVE
    with np.load(NPZ_RIF) as d:
        tq, P2q, F2q = d["t"], d["psi2"].astype(np.float64), d["phi2"].astype(np.float64)
    rho_q = P2q.sum(axis=1)
    com_r = [int(t) for t in tq if t <= 2000 and t % OGNI_RHO == 0]
    jr = [int(np.where(tr == t)[0][0]) for t in com_r]
    jq = [int(np.where(tq == t)[0][0]) for t in com_r]
    a_, b_ = RH[jr].astype(np.float64), rho_q[jq]
    m = b_ > SOGLIA_RHO * b_.max()
    er = float(np.max(np.abs(a_[m] - b_[m]) / b_[m]))
    com_p = [int(t) for t in tq if t <= 2000 and t % OGNI_PHI == 0]
    jp = [int(np.where(tp == t)[0][0]) for t in com_p]
    jq2 = [int(np.where(tq == t)[0][0]) for t in com_p]
    ep = float(np.max(np.abs(F2[jp].astype(np.float64) - F2q[jq2]) / np.abs(F2q[jq2])))
    esito("i primi 2000 tick = e5c4b62b: rho entro %g relativo (%d tick comuni)" % (TOLL_RHO, len(com_r)), er <= TOLL_RHO, "%.2e" % er)
    esito("i primi 2000 tick = e5c4b62b: |phi_j|^2 entro %g relativo (%d tick comuni)" % (TOLL_RHO, len(com_p)), ep <= TOLL_RHO, "%.2e" % ep)
    jr2 = [int(np.where(tr == t)[0][0]) for t in com_r[1:]]
    a2, b2 = RH[jr2].astype(np.float64), rho_q[jq[:-1]]
    m2 = b2 > SOGLIA_RHO * b2.max()
    ef = float(np.max(np.abs(a2[m2] - b2[m2]) / b2[m2]))
    esito("lo stesso confronto con i fotogrammi di e5c4b62b spostati di uno, entro %g" % TOLL_RHO, ef <= TOLL_RHO, "%.2e" % ef, deve=False)
    en = float(np.max(np.abs(norme / norme[0] - 1.0)))
    esito("la norma costante entro %g relativo" % TOLL_NORMA, en <= TOLL_NORMA, "%.2e" % en)
    esito("l'npz sotto %g MB" % TETTO_MB, mb <= TETTO_MB, "%.2f MB" % mb)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
