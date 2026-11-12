# -*- coding: utf-8 -*-
r"""**IL VIDEO TRIPLO: LA PARTENZA SUL PENDIO, SULLA CRESTA, E COL CAMPO ACCESO PIANO** *(Luca `2026-11-12` `20:10`; fuori dal nucleo, nessun cambio di legge, nessuna taratura)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_g1_tre_partenze.py > doc/referti_l2/campo_g1_tre/referto.txt

**La scena e il ciclo della G1 lunga** *(`s5_g1_lunga.py`, NON modificato: le costanti si importano da li'; la scena e il ciclo della forma (a) sono COPIATI, dichiarato; il DEVE di (A) contro
`0a275348` controlla che siano gli stessi)*: **TBS a `10000`, `L 81`, `s 0.15`, la forma (a), `4000` tick; `rho` ogni `20`, `|phi_j|^2` e `dLambda` ogni `100`, il centro.**
- **(A)** come la G1 lunga: `N = 1 + gamma sin(2 pi (i1 - c1)/L)`, `gamma 0.02` dal tick `0` *(il riferimento)*;
- **(B)** **la CRESTA sul centro iniziale:** `N = 1 + gamma cos(2 pi (i1 - c1)/L)` *(dichiarato)*;
- **(C)** come (A), ma **`gamma` sale LINEARE da `0` a `0.02` in `500` tick, poi costante** *(dichiarato; `cs` e la fase della forma (a) ricalcolati a ogni tick della rampa)*.
**Il referto, ogni `100` tick, per ciascuna:** **il centro e la distanza dalla cresta** *(la cresta e' la linea `i1 = c1_cresta`: `c1 + L/4` per (A) e (C), `c1` per (B); la distanza = `Delta i1`
periodico per la spaziatura delle linee, `2 pi / |B_0|`)*; **`rho` massima; i nodi di partecipazione** *(`(somma rho)^2 / somma rho^2`)*; **le due larghezze** *(i secondi momenti di `rho` attorno al
centro, lungo il gradiente `B_0` e lungo la cresta)*; **il rapporto `rho max / la densita' media del corpo`** *(`rho max` per i nodi di partecipazione, sulla norma: la misura del respiro del guardiano)*.
**Il respiro** *(dichiarato)*: **l'ampiezza picco-picco di quel rapporto sui `4000` tick.**
### **Le letture, scritte PRIMA** *(Luca)*: **(B) se la cresta e' l'equilibrio, il centro resta entro `1` nodo dalla cresta per `4000` tick; se (B) respira con un'ampiezza simile ad (A)** *(il rapporto
dei respiri `>= 0.5`, mio, dichiarato)*, **il respiro viene dall'accensione brusca o dal campo stesso, non dal pendolo. (C) se il respiro di (C) e' meno della meta' di quello di (A), una parte viene
dall'accensione brusca.**
### **I DEVE:** **(A) = `0a275348` nei primi `4000` tick** *(`rho` entro `1e-6` relativo sui nodi con `rho > 1e-6 rho max`)*; **la norma costante entro `1e-10` in tutte e tre;** **DEVE FALLIRE:
(B) contro (A) entro `1e-6`;** **oltre `60 MB` per npz: FERMO prima del commit.**
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

N_TICK = 4000                   # ### Luca 20:10
RAMPA = 500                     # ### Luca 20:10: la rampa lineare di (C)
OGNI_REF = 100                  # ### Luca 20:10
RAPP_SIMILE = 0.5               # ### mio, dichiarato: «simile» = il rapporto dei respiri >= 0.5
TOLL_CRESTA = 1.0               # ### Luca: entro 1 nodo
RADICE = os.path.dirname(os.path.dirname(_QUI))
DIR_OUT = os.path.join(RADICE, "doc", "referti_l2", "campo_g1_tre")
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
    g0 = GL.GAMMA
    print("=" * 130)
    print("IL VIDEO TRIPLO (Luca 2026-11-12 20:10): lo stato di %s a %d; s %g; gamma %+g; %d tick; (A) il pendio, (B) la cresta sul centro, (C) la rampa di %d tick" % (G1.CORSA, G1.T_STATO, s, g0, N_TICK, RAMPA))
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
            onda = {"A": np.sin(2 * np.pi * (i1 - c1_0) / Lt), "B": np.cos(2 * np.pi * (i1 - c1_0) / Lt), "C": np.sin(2 * np.pi * (i1 - c1_0) / Lt)}
            cresta = {"A": c1_0 + Lt / 4.0, "B": c1_0, "C": c1_0 + Lt / 4.0}
            ris = {}
            os.makedirs(DIR_OUT, exist_ok=True)
            for caso in ("A", "B", "C"):
                metti_stato()
                tr, RH, cen, norme, tp, F2, DL, righe_ref = [], [], [], [], [], [], [], []
                lam0 = None
                g_prec = None
                t1 = time.time()
                for k in range(N_TICK + 1):
                    if k > 0:
                        g = g0 * min(k / RAMPA, 1.0) if caso == "C" else g0
                        if g != g_prec:
                            Nx = 1.0 + g * onda[caso]
                            cs = s * Nx
                            mezza = np.exp(1j * e0 * (Nx - 1.0) * 0.5)[nodo][:, None]
                            g_prec = g
                        st["psi_h"][...] = st["psi_h"] * mezza
                        mot.cs = cs
                        mot.lambda_c = None
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                        st["psi_h"][...] = st["psi_h"] * mezza
                    if k % GL.OGNI_RHO == 0:
                        rho = rho_di()
                        c1, c2 = TO.centro(rho, i1, i2, Lt)[:2]
                        tr.append(k)
                        RH.append(rho.reshape(Lt, Lt).astype(np.float32))
                        cen.append((c1, c2))
                        norme.append(float(rho.sum()))
                        if k % OGNI_REF == 0:
                            X = TO.scarti(i1, i2, c1, c2, Lt)
                            w = rho / rho.sum()
                            npart = float(rho.sum() ** 2 / np.sum(rho ** 2))
                            lg = float(np.sqrt(np.sum(w * (X @ bh) ** 2)))
                            lc = float(np.sqrt(np.sum(w * (X @ perp) ** 2)))
                            di = ((c1 - cresta[caso] + 0.5 * Lt) % Lt) - 0.5 * Lt
                            righe_ref.append((k, c1, c2, di * passo_linee, float(rho.max()), npart, lg, lc, float(rho.max()) * npart / float(rho.sum())))
                    if k % GL.OGNI_PHI == 0:
                        f2 = phi2_di()
                        lam = f2.sum(axis=0)
                        if lam0 is None:
                            lam0 = lam.copy()
                        tp.append(k)
                        F2.append(f2.reshape(6, Lt, Lt).astype(np.float32))
                        DL.append((lam - lam0).reshape(Lt, Lt).astype(np.float32))
                f = os.path.join(DIR_OUT, "g1_tre_%s.npz" % caso)
                np.savez_compressed(f, t_rho=np.array(tr), rho=np.stack(RH), centro=np.array(cen, dtype=np.float64), t_phi=np.array(tp), phi2=np.stack(F2), dLambda=np.stack(DL),
                                    onda=onda[caso].reshape(Lt, Lt).astype(np.float32), gamma=g0, rampa=(RAMPA if caso == "C" else 0))
                ris[caso] = (np.array(tr), np.stack(RH), np.array(norme), righe_ref, f, os.path.getsize(f) / 1e6)
                print("### (%s): %d tick in %.0f s; %s %.2f MB" % (caso, N_TICK, time.time() - t1, os.path.relpath(f, RADICE), ris[caso][5]))
    print("-" * 130)
    resp = {}
    for caso in ("A", "B", "C"):
        print("### (%s) ogni %d tick: il tick, il centro (c1, c2), la distanza dalla cresta, rho max, i nodi di partecipazione, le larghezze (gradiente, cresta), rho max / la densita' media del corpo" % (caso, OGNI_REF))
        for (k, c1, c2, dc, rm, npart, lg, lc, rap) in ris[caso][3]:
            print("  %4d  %7.3f %7.3f  %+7.3f  %8.1f  %6.1f  %5.2f %5.2f  %.3f" % (k, c1, c2, dc, rm, npart, lg, lc, rap))
        raps = np.array([x[8] for x in ris[caso][3]])
        resp[caso] = float(raps.max() - raps.min())
        print("  il respiro (picco-picco di rho max / la densita' media del corpo): %.4f" % resp[caso])
    print("-" * 130)
    dB = max(abs(x[3]) for x in ris["B"][3])
    print("  LA LETTURA (B), l'equilibrio: la distanza massima dalla cresta %.3f: %s" % (dB, "il centro resta entro %g nodo: la cresta e' l'EQUILIBRIO" % TOLL_CRESTA if dB <= TOLL_CRESTA else "il centro esce oltre %g nodo" % TOLL_CRESTA))
    print("  LA LETTURA (B), il respiro: %.4f contro (A) %.4f (il rapporto %.3f): %s" % (resp["B"], resp["A"], resp["B"] / resp["A"],
          "SIMILE: il respiro viene dall'accensione brusca o dal campo stesso, non dal pendolo" if resp["B"] / resp["A"] >= RAPP_SIMILE else "NON simile (sotto %g)" % RAPP_SIMILE))
    print("  LA LETTURA (C): il respiro %.4f contro (A) %.4f (il rapporto %.3f): %s" % (resp["C"], resp["A"], resp["C"] / resp["A"],
          "meno della meta': una parte viene dall'accensione brusca" if resp["C"] < 0.5 * resp["A"] else "non meno della meta'"))
    print("-" * 130)
    with np.load(NPZ_RIF) as d:
        trf, rf = d["t_rho"], d["rho"].astype(np.float64)
    tA, RA = ris["A"][0], ris["A"][1].astype(np.float64)
    com = [t for t in tA if t in set(trf.tolist()) and t <= N_TICK]
    ja = [int(np.where(tA == t)[0][0]) for t in com]
    jf = [int(np.where(trf == t)[0][0]) for t in com]
    m = rf[jf] > GL.SOGLIA_RHO * rf[jf].max()
    eA = float(np.max(np.abs(RA[ja][m] - rf[jf][m]) / rf[jf][m]))
    esito("(A) = 0a275348 nei primi %d tick: rho entro %g relativo (%d tick)" % (N_TICK, GL.TOLL_RHO, len(com)), eA <= GL.TOLL_RHO, "%.2e" % eA)
    for caso in ("A", "B", "C"):
        nn = ris[caso][2]
        en = float(np.max(np.abs(nn / nn[0] - 1.0)))
        esito("(%s): la norma costante entro %g relativo" % (caso, GL.TOLL_NORMA), en <= GL.TOLL_NORMA, "%.2e" % en)
        esito("(%s): l'npz sotto %g MB" % (caso, GL.TETTO_MB), ris[caso][5] <= GL.TETTO_MB, "%.2f MB" % ris[caso][5])
    RB = ris["B"][1].astype(np.float64)
    mB = RA > GL.SOGLIA_RHO * RA.max()
    eB = float(np.max(np.abs(RB[mB] - RA[mB]) / RA[mB]))
    esito("(B) contro (A) entro %g" % GL.TOLL_RHO, eB <= GL.TOLL_RHO, "%.2e" % eB, deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
