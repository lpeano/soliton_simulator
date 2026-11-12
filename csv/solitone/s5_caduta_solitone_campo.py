# -*- coding: utf-8 -*-
r"""**G1 RIFATTA SALVANDO IL CAMPO, PER L'ANIMAZIONE** *(Luca `2026-11-12`; fuori dal nucleo, nessun cambio di legge, nessuna taratura)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_caduta_solitone_campo.py > doc/referti_l2/campo_g1/referto.txt

**La scena e la caduta di G1** *(`s5_caduta_solitone.py`, NON modificato: le costanti si importano da li'; la scena e il ciclo della forma (a) sono gli stessi, e il DEVE
sugli spostamenti controlla che lo siano)*: **lo stato di TBS a `10000`, `L 81`, `s 0.15`, la forma (a)** *(mezza fase `e^{+i eps_top (N_k - 1)/2}` prima e dopo il tick)*,
**`2000` tick; solo `gamma 0` e `gamma +0.02`.** **Ogni `20` tick:** `rho` per nodo *(`float32`, `81 x 81`)* **e il centro periodico; una volta la mappa di `N`.**
**Le uscite:** `doc/referti_l2/campo_g1/g1_campo_gamma000.npz`, `g1_campo_gamma020.npz` *(le chiavi `t`, `rho`, `centro`, `N`)*.
### **I DEVE** *(Luca)*: **gli spostamenti lungo `B_0` a `500`, `1000`, `2000` tick = quelli del referto di G1 entro `1e-6`;** **la norma di `rho` per fotogramma costante
entro `1e-10` relativo;** **DEVE FALLIRE: gli spostamenti di `gamma +0.02` contro i valori di `gamma 0`.** ### ⚠ **Il referto di G1 ha `5` decimali** *(l'errore di
arrotondamento fino a `5e-6`)*: **accanto al criterio come scritto, il confronto alla QUINTA cifra** *(`%+.5f` uguale)*, **dichiarato prima della corsa.**
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
from solitone import s5_caduta_solitone as G1  # noqa: E402  (le costanti di G1, il file NON modificato)

CASI = (0.0, 0.02)                            # ### Luca: solo gamma 0 e +0.02
RIF = {0.0: (+0.00175, +0.00026, -0.01251),   # ### Luca: dal referto di G1 (doc/referti_l2/s5_caduta_solitone.txt), la forma (a)
       0.02: (+1.73152, +6.59588, +21.95921)}
T_RIF = (500, 1000, 2000)
TOLL_X = 1e-6                                 # ### Luca
TOLL_NORMA = 1e-10                            # ### Luca
DIR_OUT = os.path.join(os.path.dirname(os.path.dirname(_QUI)), "doc", "referti_l2", "campo_g1")
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
    print("G1 COL CAMPO (Luca 2026-11-12): lo stato di %s a %d; s %g; gamma %s; %d tick, rho e il centro ogni %d; la forma (a)" % (G1.CORSA, G1.T_STATO, s, CASI, G1.N_TICK, G1.OGNI))
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
        with np.load(x_st[0]["file"]) as d:
            assert int(d["t"]) == G1.T_STATO
            stato = {k: d[k].copy() for k in chiavi}

        def metti_stato():
            for k in chiavi:
                st[k][...] = stato[k]

        def rho_di():
            r = np.zeros(n)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            return r

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ---------------------------------------------------------------- eps_top: come G1 (la coppia piu' alta a Gamma, il pacchetto su c F3)
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
            print("### eps_top = %.10f per tick (la coppia %.12f, %.12f)" % (e0, E[-2], E[-1]))
            metti_stato()
            assert V.shas(z) == x_st[0]["sha"], "lo stato NON e' quello registrato"
            r0 = rho_di()
            c1_0, c2_0 = TO.centro(r0, i1, i2, Lt)[:2]
            print("### il centro di partenza (c1, c2) %.4f %.4f" % (c1_0, c2_0))
            os.makedirs(DIR_OUT, exist_ok=True)
            ris = {}
            for g in CASI:
                Nx = 1.0 + g * np.sin(2 * np.pi * (i1 - c1_0) / Lt)
                cs = s * Nx
                mezza = np.exp(1j * e0 * (Nx - 1.0) * 0.5)[nodo][:, None]
                metti_stato()
                tt, xs, rhos, cen, norme = [], [], [], [], []
                t1 = time.time()
                for k in range(G1.N_TICK + 1):
                    if k > 0:
                        st["psi_h"][...] = st["psi_h"] * mezza
                        mot.cs = cs
                        mot.lambda_c = None
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                        st["psi_h"][...] = st["psi_h"] * mezza
                    if k % G1.OGNI == 0:
                        r = rho_di()
                        c1, c2 = TO.centro(r, i1, i2, Lt)[:2]
                        dc1 = ((c1 - c1_0 + 0.5 * Lt) % Lt) - 0.5 * Lt
                        dc2 = ((c2 - c2_0 + 0.5 * Lt) % Lt) - 0.5 * Lt
                        tt.append(k)
                        xs.append(float((dc1 * np.asarray(A1) + dc2 * np.asarray(A2)) @ bh))
                        rhos.append(r.reshape(Lt, Lt).astype(np.float32))
                        cen.append((c1, c2))
                        norme.append(float(r.sum()))
                f = os.path.join(DIR_OUT, "g1_campo_gamma%03d.npz" % int(round(g * 1000)))
                np.savez_compressed(f, t=np.array(tt), rho=np.stack(rhos), centro=np.array(cen, dtype=np.float64), N=Nx.reshape(Lt, Lt).astype(np.float32))
                ris[g] = (np.array(xs), np.array(norme))
                print("  gamma %+.3f: lo spostamento lungo B_0 a 500, 1000, 2000 tick %+.5f %+.5f %+.5f; %d fotogrammi; %s, %d byte; %.0f s"
                      % (g, xs[500 // G1.OGNI], xs[1000 // G1.OGNI], xs[-1], len(tt), os.path.relpath(f, os.path.dirname(os.path.dirname(_QUI))), os.path.getsize(f), time.time() - t1))
    print("-" * 130)
    for g in CASI:
        xs, norme = ris[g]
        v = [xs[t // G1.OGNI] for t in T_RIF]
        sc = max(abs(a - b) for a, b in zip(v, RIF[g]))
        esito("gamma %+.2f: gli spostamenti a 500, 1000, 2000 = il referto di G1 entro %g (come scritto da Luca)" % (g, TOLL_X), sc <= TOLL_X, "lo scarto piu' grande %.2e" % sc)
        esito("gamma %+.2f: gli spostamenti a 500, 1000, 2000 = il referto di G1 alla QUINTA cifra (%%+.5f, il formato del referto)" % g,
              all(("%+.5f" % a) == ("%+.5f" % b) for a, b in zip(v, RIF[g])), " ".join("%+.7f" % a for a in v))
        nr = float(np.max(np.abs(norme / norme[0] - 1.0)))
        esito("gamma %+.2f: la norma di rho per fotogramma costante entro %g relativo" % (g, TOLL_NORMA), nr <= TOLL_NORMA, "%.2e" % nr)
    v = [ris[0.02][0][t // G1.OGNI] for t in T_RIF]
    sc = max(abs(a - b) for a, b in zip(v, RIF[0.0]))
    esito("gli spostamenti di gamma +0.02 contro i valori di gamma 0, entro %g" % TOLL_X, sc <= TOLL_X, "%.2e" % sc, deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
