# -*- coding: utf-8 -*-
r"""**G1 CON LE COMPONENTI E IL VUOTO** *(Luca `2026-11-12` `14:55`, `15:08`; fuori dal nucleo, nessun cambio di legge, nessuna taratura; SOLO NUMERI, nessuna lettura fisica)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_caduta_solitone_componenti.py > doc/referti_l2/campo_g1_componenti/referto.txt

**La scena e la caduta di G1 col campo** *(`s5_caduta_solitone.py` e `s5_caduta_solitone_campo.py`, NON modificati: le costanti si importano da li'; la scena, `eps_top` e il ciclo
della forma (a) sono gli stessi, e i DEVE contro gli npz di `fc96390e` lo controllano)*: **TBS a `10000`, `L 81`, `s 0.15`, `gamma 0` e `+0.02`, `2000` tick.** **Ogni `40` tick**
*(`51` fotogrammi)*, `float32`, `81 x 81`:
- **`psi2[c]`, `c = 0..11`, l'ordine del nucleo:** **`psi_h` ha una riga per ESTREMITA' d'arco** *(la riga `6 x + 2 k + e`: l'arco `k = 0, 1, 2` della cella `x`, l'estremita' `e = 0` nel
  nodo `x`, `e = 1` nel nodo vicino)* **e la colonna `sigma = 0, 1`** *(lo spin del nucleo)*. **La componente `c = 2 (2 k + e) + sigma` nel NODO dove sta l'estremita'** *(ogni nodo ne
  riceve esattamente una per `(k, e)`: controllato)*; **la direzione di ogni `k` stampata nel referto.** **La somma delle `12` e' la `rho` del nodo.**
- **`phi2[j]`, `j = 2 k + e = 0..5`:** **lo stesso per `phi_h`** *(una componente per estremita', senza spin)*.
- **`dLambda`:** `Lambda - Lambda(il primo fotogramma)` per nodo *(`Lambda = somma |phi|^2` delle estremita' del nodo, come le mappe)*; **il centro periodico.**
- **una volta:** `N` e `phi2_rif`, **le `6` componenti del vuoto F3 di riferimento** *(`c(t) F3` al tick dello stato, il riferimento del bordo: il vuoto «lontano dal solitone»)*.
**Le uscite:** `doc/referti_l2/campo_g1_componenti/g1_comp_gamma000.npz`, `g1_comp_gamma020.npz`; **il referto:** per ogni caso, a `0`, `1000`, `1800`, `2000` tick, la frazione della norma in ciascuna componente.
### **I DEVE** *(Luca)*: **la somma delle `12` = la `rho` di `fc96390e` negli stessi tick entro `1e-6` relativo** *(i nodi con `rho > 1e-6 rho max`)*; **il centro = quello di `fc96390e` entro
`1e-9`;** **la norma costante entro `1e-10`;** **DEVE FALLIRE:** **la somma delle sole prime `11` = `rho` entro `1e-6`.** **Oltre `60 MB` per npz: fermo prima del commit.**
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
from solitone import s5_caduta_solitone_campo as GC  # noqa: E402  (NON modificato)

OGNI_C = 40                     # ### Luca: ogni 40 tick, 51 fotogrammi
T_FRAZ = (0, 1000, 1800, 2000)  # ### Luca (15:08)
TOLL_RHO = 1e-6                 # ### Luca
SOGLIA_RHO = 1e-6               # ### Luca: i nodi con rho > 1e-6 rho max
TOLL_C = 1e-9                   # ### Luca
TOLL_NORMA = 1e-10              # ### Luca
TETTO_MB = 60.0                 # ### Luca
DIR_OUT = os.path.join(os.path.dirname(os.path.dirname(_QUI)), "doc", "referti_l2", "campo_g1_componenti")
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
    for m in ("__init__", "corsa_accensione", "bordo", "carta_punto_fisso", "toro", "s5_caduta_solitone", "s5_caduta_solitone_campo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
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
    print("G1 CON LE COMPONENTI E IL VUOTO (Luca 2026-11-12 14:55, 15:08): lo stato di %s a %d; s %g; gamma %s; %d tick, ogni %d; la forma (a); SOLO NUMERI" % (G1.CORSA, G1.T_STATO, s, GC.CASI, G1.N_TICK, OGNI_C))
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
        assert nodo.size == 6 * n and st["psi_h"].shape == (6 * n, 2) and st["phi_h"].shape == (6 * n,), "psi_h NON ha una riga per estremita' (6 n, 2)"
        vv = np.arange(n)
        i1, i2 = vv // Lt, vv % Lt
        A1, A2 = TO.vettori()
        B = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
        bh = B[0] / np.linalg.norm(B[0])
        d0 = TO.scarti(i1, i2, 0.0, 0.0, Lt)
        # ---------------------------------------------------------------- le componenti: (k, e) di ogni riga, e ogni nodo ne riceve una per (k, e)
        righe = np.arange(6 * n)
        kk, ee = (righe // 2) % 3, righe % 2
        conta = np.zeros((n, 6), dtype=int)
        np.add.at(conta, (nodo, 2 * kk + ee), 1)
        esito("ogni nodo riceve esattamente UNA estremita' per (k, e): le 12 componenti di psi e le 6 di phi sono per nodo", bool(np.all(conta == 1)), "min %d max %d" % (conta.min(), conta.max()))
        for k in range(3):
            a = 3 * 0 + k
            dv = TO.scarti(i1[[nodo[2 * a + 1]]], i2[[nodo[2 * a + 1]]], float(i1[nodo[2 * a]]), float(i2[nodo[2 * a]]), Lt)[0]
            print("  l'arco k = %d: dall'estremita' e = 0 (il nodo della cella) all'estremita' e = 1, lo spostamento (%+.4f, %+.4f), l'angolo %.1f gradi" % (k, dv[0], dv[1], float(np.degrees(np.arctan2(dv[1], dv[0])))))
        print("  le componenti di psi: c = 2 (2 k + e) + sigma, sigma la colonna di psi_h (lo spin del nucleo); di phi: j = 2 k + e")
        idx = 2 * kk + ee

        def componenti():
            p2 = np.abs(st["psi_h"]) ** 2
            out_p = np.zeros((12, n))
            for sg in range(2):
                tmp = np.zeros((n, 6))
                np.add.at(tmp, (nodo, idx), p2[:, sg])
                for j in range(6):
                    out_p[2 * j + sg] = tmp[:, j]
            tmp = np.zeros((n, 6))
            np.add.at(tmp, (nodo, idx), np.abs(st["phi_h"]) ** 2)
            return out_p, tmp.T.copy()

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
            # ---------------------------------------------------------------- il vuoto F3 di riferimento: c(t) F3 al tick dello stato (il riferimento del bordo)
            for k in chiavi:
                st[k][...] = salvato[k]
            st["phi_h"][...] = BO.c_di(G1.T_STATO, tab, Kf, omega) * phi_v
            _pp, phi2_rif = componenti()
            metti_stato()
            assert V.shas(z) == x_st[0]["sha"], "lo stato NON e' quello registrato"
            r0 = np.zeros(n)
            np.add.at(r0, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            c1_0, c2_0 = TO.centro(r0, i1, i2, Lt)[:2]
            os.makedirs(DIR_OUT, exist_ok=True)
            ris = {}
            for g in GC.CASI:
                Nx = 1.0 + g * np.sin(2 * np.pi * (i1 - c1_0) / Lt)
                cs = s * Nx
                mezza = np.exp(1j * e0 * (Nx - 1.0) * 0.5)[nodo][:, None]
                metti_stato()
                tt, P2, F2, DL, cen, norme = [], [], [], [], [], []
                lam0 = None
                t1 = time.time()
                for k in range(G1.N_TICK + 1):
                    if k > 0:
                        st["psi_h"][...] = st["psi_h"] * mezza
                        mot.cs = cs
                        mot.lambda_c = None
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                        st["psi_h"][...] = st["psi_h"] * mezza
                    if k % OGNI_C == 0:
                        p2, f2 = componenti()
                        rho = p2.sum(axis=0)
                        lam = f2.sum(axis=0)
                        if lam0 is None:
                            lam0 = lam.copy()
                        c1, c2 = TO.centro(rho, i1, i2, Lt)[:2]
                        tt.append(k)
                        P2.append(p2.reshape(12, Lt, Lt).astype(np.float32))
                        F2.append(f2.reshape(6, Lt, Lt).astype(np.float32))
                        DL.append((lam - lam0).reshape(Lt, Lt).astype(np.float32))
                        cen.append((c1, c2))
                        norme.append(float(rho.sum()))
                f = os.path.join(DIR_OUT, "g1_comp_gamma%03d.npz" % int(round(g * 1000)))
                np.savez_compressed(f, t=np.array(tt), psi2=np.stack(P2), phi2=np.stack(F2), dLambda=np.stack(DL), centro=np.array(cen, dtype=np.float64),
                                    N=Nx.reshape(Lt, Lt).astype(np.float32), phi2_rif=phi2_rif.reshape(6, Lt, Lt).astype(np.float32))
                mb = os.path.getsize(f) / 1e6
                ris[g] = (np.array(tt), np.stack(P2), np.array(cen), np.array(norme), f, mb)
                print("  gamma %+.3f: %d fotogrammi; %s, %.2f MB; %.0f s" % (g, len(tt), os.path.relpath(f, os.path.dirname(os.path.dirname(_QUI))), mb, time.time() - t1))
    print("-" * 130)
    print("### LE FRAZIONI DELLA NORMA PER COMPONENTE (c = 2 (2 k + e) + sigma; solo numeri)")
    for g in GC.CASI:
        tt, P2, cen, norme, f, mb = ris[g]
        for tf in T_FRAZ:
            i = int(np.where(tt == tf)[0][0])
            fr = P2[i].reshape(12, -1).astype(np.float64).sum(axis=1)
            fr /= fr.sum()
            print("  gamma %+.2f, tick %4d: %s" % (g, tf, " ".join("c%d %.5f" % (cc, fr[cc]) for cc in range(12))))
    print("-" * 130)
    for g in GC.CASI:
        tt, P2, cen, norme, f, mb = ris[g]
        with np.load(os.path.join(GC.DIR_OUT, "g1_campo_gamma%03d.npz" % int(round(g * 1000)))) as d:
            tc, rc, cc = d["t"], d["rho"], d["centro"]
        j = [int(np.where(tc == t)[0][0]) for t in tt]
        som = P2.astype(np.float64).sum(axis=1)
        som11 = P2[:, :11].astype(np.float64).sum(axis=1)
        ref = rc[j].astype(np.float64)
        m = ref > SOGLIA_RHO * ref.max()
        e12 = float(np.max(np.abs(som[m] - ref[m]) / ref[m]))
        e11 = float(np.max(np.abs(som11[m] - ref[m]) / ref[m]))
        ec = float(np.max(np.abs(cen - cc[j])))
        en = float(np.max(np.abs(norme / norme[0] - 1.0)))
        esito("gamma %+.2f: la somma delle 12 |psi_c|^2 = rho di fc96390e negli stessi tick, entro %g relativo (rho > %g rho max)" % (g, TOLL_RHO, SOGLIA_RHO), e12 <= TOLL_RHO, "%.2e" % e12)
        esito("gamma %+.2f: il centro = quello di fc96390e entro %g" % (g, TOLL_C), ec <= TOLL_C, "%.2e" % ec)
        esito("gamma %+.2f: la norma costante entro %g relativo" % (g, TOLL_NORMA), en <= TOLL_NORMA, "%.2e" % en)
        esito("gamma %+.2f: la somma delle SOLE prime 11 = rho entro %g" % (g, TOLL_RHO), e11 <= TOLL_RHO, "%.2e" % e11, deve=False)
        esito("gamma %+.2f: l'npz sotto %g MB" % (g, TETTO_MB), mb <= TETTO_MB, "%.2f MB" % mb)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
