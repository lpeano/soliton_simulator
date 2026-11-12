# -*- coding: utf-8 -*-
r"""**IL PENDOLO INTERO: LA G1 LUNGHISSIMA, DUE PERIODI** *(Luca `2026-11-12` `21:20`; fuori dal nucleo, nessun cambio di legge, nessuna taratura)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_g1_lunghissima.py > doc/referti_l2/campo_g1_lunghissima/referto.txt

**La scena e il ciclo della G1 lunga** *(`s5_g1_lunga.py`, NON modificato: le costanti si importano da li'; la scena e il ciclo della forma (a) COPIATI, dichiarato; il DEVE sui primi `5000`
tick contro `0a275348` controlla che siano gli stessi)*: **TBS a `10000`, `L 81`, la forma (a), `gamma +0.02`, `14000` tick; `rho` ogni `40`, `|phi_j|^2` e `dLambda` ogni `200`, il centro ogni `20`.**
**Il referto:** **ogni `200` tick la distanza dalla cresta** *(la cresta e' la linea `i1 = c1_0 + L/4`; la distanza CON SEGNO = `Delta i1` periodico per la spaziatura delle linee `2 pi / |B_0|`)*,
**`rho` massima, i nodi di partecipazione, le due larghezze;** **i punti d'INVERSIONE** *(gli estremi locali della distanza col segno, dal centro ogni `20` tick)* **e l'ampiezza a ciascuno**
*(`|distanza|` all'inversione)*; **il periodo misurato** *(fra inversioni dalla stessa parte)*; **il profilo dell'anello vecchio ogni `1000` tick come in `0a275348`.**
### **Le letture, scritte PRIMA** *(Luca)*: **(p1) l'ampiezza CALA a ogni mezzo periodo** *(lo smorzamento: la frazione per mezzo periodo; resa operativa, mia: ogni rapporto fra ampiezze consecutive sotto `0.95`)*;
**(p2) l'ampiezza resta COSTANTE entro il `5%`** *(il calo di `0a275348` era della partenza)*; **(p3) il moto smette di essere periodico** *(mia, dichiarata: meno di `3` inversioni, o i mezzi
periodi che differiscono oltre il `20%`)*.
### **I DEVE:** **i primi `5000` tick = `0a275348`** *(`rho` entro `1e-6` relativo nei tick comuni)*; **la norma costante entro `1e-10`;** **DEVE FALLIRE: lo stesso confronto coi fotogrammi spostati
di uno;** **oltre `60 MB`: FERMO prima del commit.**
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
from solitone import s5_g1_lunga as GL  # noqa: E402  (NON modificato)

N_TICK = 14000                  # ### Luca 21:20
OGNI_RHO, OGNI_PHI, OGNI_CEN = 40, 200, 20   # ### Luca 21:20
OGNI_REF, OGNI_PROF = 200, 1000              # ### Luca 21:20
N_CONFRONTO = 5000              # ### Luca 21:20: i primi 5000 tick = 0a275348
TOLL_P2 = 0.05                  # ### Luca: entro il 5%
SOGLIA_P1 = 0.95                # ### mia, dichiarata
TOLL_PERIODO = 0.20             # ### mia, dichiarata (p3)
RADICE = os.path.dirname(os.path.dirname(_QUI))
DIR_OUT = os.path.join(RADICE, "doc", "referti_l2", "campo_g1_lunghissima")
NPZ_RIF = os.path.join(RADICE, "doc", "referti_l2", "campo_g1_lunga", "g1_lunga.npz")   # ### 0a275348
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
    for m in ("__init__", "corsa_accensione", "bordo", "carta_punto_fisso", "toro", "s5_caduta_solitone", "s5_g1_lunga"):
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
    print("IL PENDOLO INTERO, LA G1 LUNGHISSIMA (Luca 2026-11-12 21:20): lo stato di %s a %d; s %g; gamma %+g; %d tick; rho ogni %d, |phi_j|^2 e dLambda ogni %d, il centro ogni %d" % (
        G1.CORSA, G1.T_STATO, s, GL.GAMMA, N_TICK, OGNI_RHO, OGNI_PHI, OGNI_CEN))
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
        perp = np.array([-bh[1], bh[0]])
        passo_linee = 2.0 * np.pi / np.linalg.norm(B[0])
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
            Nx = 1.0 + GL.GAMMA * np.sin(2 * np.pi * (i1 - c1_0) / Lt)
            cs = s * Nx
            mezza = np.exp(1j * e0 * (Nx - 1.0) * 0.5)[nodo][:, None]
            cresta = c1_0 + Lt / 4.0
            metti_stato()
            tr, RH, norme, tp, F2, DL, tc, cen, ref = [], [], [], [], [], [], [], [], []
            lam0 = None
            t1 = time.time()
            for k in range(N_TICK + 1):
                if k > 0:
                    st["psi_h"][...] = st["psi_h"] * mezza
                    mot.cs = cs
                    mot.lambda_c = None
                    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                    st["psi_h"][...] = st["psi_h"] * mezza
                if k % OGNI_CEN == 0:
                    rho = rho_di()
                    c1, c2 = TO.centro(rho, i1, i2, Lt)[:2]
                    tc.append(k)
                    cen.append((c1, c2))
                    norme.append(float(rho.sum()))
                    if k % OGNI_RHO == 0:
                        tr.append(k)
                        RH.append(rho.reshape(Lt, Lt).astype(np.float32))
                    if k % OGNI_REF == 0:
                        X = TO.scarti(i1, i2, c1, c2, Lt)
                        w = rho / rho.sum()
                        npart = float(rho.sum() ** 2 / np.sum(rho ** 2))
                        di = ((c1 - cresta + 0.5 * Lt) % Lt) - 0.5 * Lt
                        ref.append((k, c1, c2, di * passo_linee, float(rho.max()), npart, float(np.sqrt(np.sum(w * (X @ bh) ** 2))), float(np.sqrt(np.sum(w * (X @ perp) ** 2)))))
                if k % OGNI_PHI == 0:
                    f2 = phi2_di()
                    lam = f2.sum(axis=0)
                    if lam0 is None:
                        lam0 = lam.copy()
                    tp.append(k)
                    F2.append(f2.reshape(6, Lt, Lt).astype(np.float32))
                    DL.append((lam - lam0).reshape(Lt, Lt).astype(np.float32))
            print("### %d tick in %.0f s" % (N_TICK, time.time() - t1))
    os.makedirs(DIR_OUT, exist_ok=True)
    f = os.path.join(DIR_OUT, "g1_lunghissima.npz")
    tr, tp, tc, RH, F2, cen, norme = np.array(tr), np.array(tp), np.array(tc), np.stack(RH), np.stack(F2), np.array(cen, dtype=np.float64), np.array(norme)
    np.savez_compressed(f, t_rho=tr, rho=RH, t_centro=tc, centro=cen, t_phi=tp, phi2=F2, dLambda=np.stack(DL), N=Nx.reshape(Lt, Lt).astype(np.float32))
    mb = os.path.getsize(f) / 1e6
    print("  %s: %.2f MB; %d fotogrammi di rho, %d di phi, %d centri" % (os.path.relpath(f, RADICE), mb, len(tr), len(tp), len(tc)))
    print("-" * 130)
    print("### ogni %d tick: il tick, il centro (c1, c2), la distanza dalla cresta (col segno), rho max, i nodi di partecipazione, le larghezze (gradiente, cresta)" % OGNI_REF)
    for (k, c1, c2, dc, rm, npart, lg, lc) in ref:
        print("  %5d  %7.3f %7.3f  %+8.3f  %8.1f  %6.1f  %5.2f %5.2f" % (k, c1, c2, dc, rm, npart, lg, lc))
    print("-" * 130)
    # ---------------------------------------------------------------- le inversioni, l'ampiezza, il periodo
    dist = np.array([(((c[0] - cresta + 0.5 * Lt) % Lt) - 0.5 * Lt) * passo_linee for c in cen])
    inv = [i for i in range(1, len(dist) - 1) if (dist[i] - dist[i - 1]) * (dist[i + 1] - dist[i]) < 0]
    print("### LE INVERSIONI (gli estremi locali della distanza dalla cresta, dal centro ogni %d tick): %d" % (OGNI_CEN, len(inv)))
    amp = []
    for i in inv:
        amp.append(abs(dist[i]))
        print("  il tick %5d: la distanza dalla cresta %+8.3f, l'ampiezza %.3f" % (tc[i], dist[i], abs(dist[i])))
    mezzi = [int(tc[inv[j + 1]] - tc[inv[j]]) for j in range(len(inv) - 1)]
    if len(inv) >= 3:
        periodi = [int(tc[inv[j + 2]] - tc[inv[j]]) for j in range(len(inv) - 2)]
        print("  i mezzi periodi %s; i periodi (fra inversioni dalla stessa parte) %s" % (mezzi, periodi))
    rap = [amp[j + 1] / amp[j] for j in range(len(amp) - 1)]
    print("  i rapporti fra ampiezze consecutive: %s" % ", ".join("%.4f" % x for x in rap))
    print("-" * 130)
    irregolare = len(inv) < 3 or (len(mezzi) >= 2 and (max(mezzi) - min(mezzi)) > TOLL_PERIODO * float(np.mean(mezzi)))
    if irregolare:
        print("  LA LETTURA: (p3) il moto smette di essere periodico (meno di 3 inversioni, o i mezzi periodi oltre il %g%%)" % (100 * TOLL_PERIODO))
    elif all(abs(x - 1.0) <= TOLL_P2 for x in rap):
        print("  LA LETTURA: (p2) l'ampiezza resta costante entro il %g%%: il calo di 0a275348 era della partenza" % (100 * TOLL_P2))
    elif all(x < SOGLIA_P1 for x in rap):
        print("  LA LETTURA: (p1) l'ampiezza cala a ogni mezzo periodo: lo smorzamento per mezzo periodo %.4f (1 - il rapporto medio)" % (1.0 - float(np.mean(rap))))
    else:
        print("  LA LETTURA: caso intermedio (ne' p1, ne' p2, ne' p3 come scritte); i rapporti qui sopra")
    print("-" * 130)
    # ---------------------------------------------------------------- l'anello vecchio ogni 1000 tick, come in 0a275348
    X0 = TO.scarti(i1, i2, c1_0, c2_0, Lt)
    R0 = np.hypot(X0[:, 0], X0[:, 1])
    print("### IL PROFILO DELL'ANELLO VECCHIO ogni %d tick (come in 0a275348: il semipiano opposto al moto, R %d-%d dalla posizione iniziale)" % ((OGNI_PROF,) + GL.R_PROF))
    for t in range(0, N_TICK + 1, OGNI_PROF):
        jp = int(np.where(tp == t)[0][0])
        jc = int(np.where(tc == t)[0][0])
        sp = TO.scarti(np.array([cen[jc][0]]), np.array([cen[jc][1]]), c1_0, c2_0, Lt)[0]
        u = sp / np.linalg.norm(sp) if np.linalg.norm(sp) > 0.5 else bh
        semi = (X0 @ u) < 0
        dphi = F2[jp].reshape(6, -1).astype(np.float64).sum(axis=0) - 6.0
        medie = [float(dphi[semi & (R0 >= r) & (R0 < r + 1)].mean()) for r in range(GL.R_PROF[0], GL.R_PROF[1])]
        i_min = int(np.argmin(medie))
        m_an = semi & (R0 >= GL.R_PROF[0]) & (R0 < GL.R_PROF[1])
        print("  tick %5d: il raggio del minimo %.1f, la profondita' %+.4f, il deficit %.1f; il centro della materia %.3f %.3f" % (
            t, GL.R_PROF[0] + i_min + 0.5, medie[i_min], float(np.maximum(-dphi[m_an], 0.0).sum()), cen[jc][0], cen[jc][1]))
    print("-" * 130)
    # ---------------------------------------------------------------- i DEVE
    with np.load(NPZ_RIF) as d:
        trf, rf = d["t_rho"], d["rho"].astype(np.float64)
    com = [int(t) for t in tr if t <= N_CONFRONTO and t in set(trf.tolist())]
    ja = [int(np.where(tr == t)[0][0]) for t in com]
    jf = [int(np.where(trf == t)[0][0]) for t in com]
    a_, b_ = RH[ja].astype(np.float64), rf[jf]
    m = b_ > GL.SOGLIA_RHO * b_.max()
    er = float(np.max(np.abs(a_[m] - b_[m]) / b_[m]))
    esito("i primi %d tick = 0a275348: rho entro %g relativo (%d tick comuni)" % (N_CONFRONTO, GL.TOLL_RHO, len(com)), er <= GL.TOLL_RHO, "%.2e" % er)
    a2, b2 = RH[ja[1:]].astype(np.float64), rf[jf[:-1]]
    m2 = b2 > GL.SOGLIA_RHO * b2.max()
    ef = float(np.max(np.abs(a2[m2] - b2[m2]) / b2[m2]))
    esito("lo stesso confronto coi fotogrammi spostati di uno, entro %g" % GL.TOLL_RHO, ef <= GL.TOLL_RHO, "%.2e" % ef, deve=False)
    en = float(np.max(np.abs(norme / norme[0] - 1.0)))
    esito("la norma costante entro %g relativo" % GL.TOLL_NORMA, en <= GL.TOLL_NORMA, "%.2e" % en)
    esito("l'npz sotto %g MB" % GL.TETTO_MB, mb <= GL.TETTO_MB, "%.2f MB" % mb)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
