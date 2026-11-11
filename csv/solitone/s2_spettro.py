# -*- coding: utf-8 -*-
r"""**S2: LO SPETTRO DI STABILITA' LINEARE DEL VUOTO CON LA LEGGE DI `cs`** *(sul ramo laterale; Luca `2026-11-10` `19:37`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `28.2`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s2_spettro.py > doc/referti_l2/s2_spettro_vuoto_cs.txt

**La mappa di un tick nel riferimento che gira col vuoto** *(`phi -> e^{i omega} phi'`)*, **in rappresentazione reale** *(`Re phi`, `Im phi` delle `6` estremita' della cella, `cs` del nodo: `13` reali)*;
**la risposta a un impulso nel nodo `0` con differenze simmetriche** *(il controllo di linearita' `R(2a)` contro `R(a)`)*, **`A(k)` con `fft2`, gli autovalori per ogni `k`.**
**(L-F1)** F1 come nelle corse *(`r = 1 - e^{-omega_v}`, (q2))*; **(L-ist)** la stessa mappa con `r = 1`. **La mappa:** `Lambda_c`, `s`, `Lambda` *(12 punti)*. **I DEVE:** l'unitarieta' a `cs` spento;
il tasso di oggi contro `0.158`; l'onda piana nella simulazione; **DEVE FALLIRE:** il fattore `1 + 1e-3`. **Il meccanismo:** `lambda - A_cc = somma_b` dei contributi delle bande. **Le letture (w1)-(w4).**
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
from solitone import carta_f1 as F1  # noqa: E402
from solitone import carta_f1_lunga as F1L  # noqa: E402
from solitone import carta_punto_fisso as CPF  # noqa: E402

A_REL = 1e-4                   # ### mio (sez. 28.2 (d), ANNOTATA in 28.3): l'impulso relativo; R = (4 R(a) - R(2a)) / 3 (Richardson): con 1e-6 l'arrotondamento dava 2.8e-9 a cs spento
TOLL_LIN = 1e-6                # ### Luca: |R(2a) - R(a)| / max|R| sotto 1e-6
TOLL_TRASL = 1e-9              # ### mio (sez. 28.2 (d)): l'invarianza per traslazione
TOLL_PF = 1e-10                # ### mio (sez. 28.2 (b)): il residuo della base
TOLL_PSI = 1e-12               # ### mio (sez. 28.2 (a)): psi si stacca se le risposte incrociate stanno sotto
TOLL_UNIT = 1e-9               # ### Luca: max ||lambda| - 1| sotto 1e-9
RIF, TOLL_RIF = 0.158, 0.05    # ### Luca: 0.158 per tick entro il 5%
ONDA_AMP, ONDA_N, ONDA_DA, TOLL_ONDA = 1e-11, 100, 20, 0.05   # ### Luca: 100 tick, entro il 5%; mio: l'ampiezza 1e-11, la pendenza dal tick 20
FATT_F = 1e-3                  # ### Luca: il fattore 1 + 1e-3
STABILE = 1e-9                 # ### mio (sez. 28.2): stabile se |lambda|_max - 1 sotto 1e-9
LC_SCAN = (8.5, 17.0, 34.0, 68.0, 136.0, 340.0)   # ### Luca
S_SCAN = (0.05, 0.15, 0.3)                       # ### Luca
LAM_SCAN = (6.0, 3.0, 1.0, 0.5, 0.1)             # ### Luca
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
    import flussi_parziali as FP
    import tick as TK
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "toro", "bordo", "carta_punto_fisso", "carta_f1", "carta_f1_lunga"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    t00 = time.time()
    print("=" * 130)
    print("S2 (sez. 28.2): lo spettro lineare del vuoto c(%d) F3 con la legge di cs; a %g relativo; la linearita' %g; stabile se |lambda|_max - 1 < %g" % (CPF.TICK_D4, A_REL, TOLL_LIN, STABILE))
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
        assert inc.nodo.size == 6 * n and np.array_equal(inc.nodo[0::2], np.repeat(np.arange(n), 3)), "la cella NON e' di 3 archi per nodo"
        assert st["phi_h"].size == 6 * n, "phi NON ha 6 componenti per cella"
        npsi = st["psi_h"].size // n
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        lam0 = mot.densita_vuoto(st).copy()
        LAM = float(np.mean(lam0))
        lc_T2 = LAM * (1.0 - s) / s
        print("### Lambda del vuoto %.17g; Lambda_c di T2 %.12f; s %g; psi %d reali per cella (%s)" % (LAM, lc_T2, s, 2 * npsi, st["psi_h"].dtype))
        fp = np.zeros(n)
        # ------------------------------------------------------------------ |k| e la direzione, con l'immagine minima
        A1, A2 = TO.vettori()
        B = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
        m = np.fft.fftfreq(Lt) * Lt
        M1, M2 = np.meshgrid(m, m, indexing="ij")
        KK = np.full((Lt, Lt), np.inf)
        KX = np.zeros((Lt, Lt, 2))
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                kv = ((M1 + a * Lt)[..., None] * B[0] + (M2 + b * Lt)[..., None] * B[1]) / Lt
                q = np.hypot(kv[..., 0], kv[..., 1])
                meglio = q < KK
                KK = np.where(meglio, q, KK)
                KX = np.where(meglio[..., None], kv, KX)
        i1, i2 = np.arange(n) // Lt, np.arange(n) % Lt

        def vuoto_con(ph, psi=None):
            for k in chiavi:
                st[k][...] = salvato[k]
            st["psi_h"][...] = 0.0 if psi is None else psi
            st["phi_h"][...] = ph

        def mappa(ph, cs, lc, u, caso, psi=None, fattore=1.0):
            """### UN tick: `(e^{i omega} phi', cs' di F1, cs' istantaneo, psi')`; `caso` `"spento"` o `"cs"`."""
            vuoto_con(ph, psi)
            if caso == "spento":
                mot.cs = None
                mot.lambda_c = None
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                return st["phi_h"] * np.conj(u) * fattore, None, None, st["psi_h"].copy()
            with F1.cs_primo_zero(True):
                p0 = ph.copy()
                mot.cs = cs.copy()
                mot.lambda_c = float(lc)
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                lam = mot.densita_vuoto(st).copy()
                L = FP.cs(lam, lc, fp).copy()
                r = 1.0 - np.exp(-F1.omega_v(p0, st["phi_h"], mot.inc.nodo, mot.inc.n))
                return st["phi_h"] * np.conj(u), F1.rilassa(cs, L, r), F1.rilassa(cs, L, np.ones(n)), st["psi_h"].copy()

        def cella(ph, cs):
            v = [ph.reshape(n, 6).real, ph.reshape(n, 6).imag]
            if cs is not None:
                v.append(cs[:, None])
            return np.concatenate(v, axis=1)

        def base(lam_v, lc, caso):
            ph = c * phi_v * math.sqrt(lam_v / LAM)
            cs = None if caso == "spento" else FP.cs(mot.densita_vuoto((vuoto_con(ph), st)[1]), lc, fp).copy()
            p1, cf, ci, _ = mappa(ph, cs, lc, 1.0, caso)
            zz = complex(np.vdot(ph, p1))
            u = zz / abs(zz)
            res_phi = float(np.max(np.abs(p1 * np.conj(u) - ph))) / float(np.max(np.abs(ph)))
            res = {"phi": ph, "cs": cs, "u": u, "omega": abs(math.atan2(u.imag, u.real)), "res_phi": res_phi}
            if cs is not None:
                res["res_cf"] = float(np.max(np.abs(cf - cs))) / float(cs[0])
                res["res_ci"] = float(np.max(np.abs(ci - cs))) / float(cs[0])
            return res

        def risposta(b, lc, caso, x0=0, colonne=None, fattore=1.0, due=True):
            """### `R[x, i, j]`: la risposta della cella `x` alla direzione `j` della cella `x0`; `{"F1", "ist"}` per `cs`; e la linearita'."""
            ph_b, cs_b = b["phi"], b["cs"]
            nd = 12 if cs_b is None else 13
            sc = np.concatenate([np.abs(ph_b.reshape(n, 6)[x0])] * 2 + ([] if cs_b is None else [[cs_b[x0]]]))
            R = {"F1": np.zeros((n, nd, nd)), "ist": np.zeros((n, nd, nd))} if cs_b is not None else {"spento": np.zeros((n, nd, nd))}
            dev, psi_x = 0.0, 0.0
            for j in (range(nd) if colonne is None else colonne):
                a = A_REL * sc[j]
                uscite = {}
                for f in ((1, -1, 2, -2) if due else (1, -1)):
                    ph = ph_b.copy()
                    cs = None if cs_b is None else cs_b.copy()
                    if j < 6:
                        ph[6 * x0 + j] += f * a
                    elif j < 12:
                        ph[6 * x0 + j - 6] += 1j * f * a
                    else:
                        cs[x0] += f * a
                    p1, cf, ci, ps = mappa(ph, cs, lc, b["u"], caso, fattore=fattore)
                    uscite[f] = (cella(p1, cf), None if cf is None else cella(p1, ci), ps)
                psi_x = max(psi_x, float(np.max(np.abs(uscite[1][2] - uscite[-1][2]))) / (2 * a))
                for q, chi in enumerate(R):
                    r1 = (uscite[1][q] - uscite[-1][q]) / (2 * a)
                    if due:
                        r2 = (uscite[2][q] - uscite[-2][q]) / (4 * a)
                        dev = max(dev, float(np.max(np.abs(r2 - r1))) / max(float(np.max(np.abs(r1))), 1e-300))
                    R[chi][:, :, j] = (4.0 * r1 - r2) / 3.0 if due else r1
            return R, dev, psi_x

        def spettro(R):
            nd = R.shape[1]
            Ak = np.fft.fft2(R.reshape(Lt, Lt, nd, nd), axes=(0, 1))
            ev = np.linalg.eigvals(Ak.reshape(-1, nd, nd))
            mod = np.abs(ev)
            mk = mod.max(axis=1)
            im = int(np.argmax(mk))
            return {"Ak": Ak, "mod": mod, "max": float(mk[im]), "min": float(mod.min()), "dev_unit": float(np.max(np.abs(mod - 1.0))), "ik": im,
                    "neq": int(np.sum(mk >= mk[im] - 1e-9)), "k0": float(mk[0])}

        def descrivi(sp, nome):
            """### il `k` piu' instabile, l'autovettore, le bande, il meccanismo."""
            im = sp["ik"]
            a1, a2 = divmod(im, Lt)
            A = sp["Ak"][a1, a2]
            w, vr = np.linalg.eig(A)
            bb = int(np.argmax(np.abs(w)))
            lam_, v = w[bb], vr[:, bb]
            kx = KX[a1, a2]
            out = {"neq": sp["neq"], "m": (a1, a2), "k": float(KK[a1, a2]), "dir": float(np.degrees(np.arctan2(kx[1], kx[0]))) % 360.0, "lam": complex(lam_), "v": v}
            print("    %s: |lambda|_max %.12f, ln %.6f per tick, lambda %+.8f %+.8fi (arg %.6f); al k (m1, m2) = (%d, %d), |k| %.5f, la direzione %.2f gradi; %d k con lo stesso |lambda| (entro 1e-9); |lambda| max a k = 0: %.12f"
                  % (nome, abs(lam_), math.log(abs(lam_)), lam_.real, lam_.imag, np.angle(lam_), a1, a2, out["k"], out["dir"], sp["neq"], sp["k0"]))
            if A.shape[0] == 13:
                fcs = float(abs(v[12]) ** 2 / np.sum(np.abs(v) ** 2))
                Aff, Afc, Acf, Acc = A[:12, :12], A[:12, 12], A[12, :12], A[12, 12]
                wb, eb = np.linalg.eig(Aff)
                coef = np.linalg.solve(eb, v[:12])
                pes = np.abs(coef) ** 2 / np.sum(np.abs(coef) ** 2)
                ordine = np.argsort(-pes)
                print("      l'autovettore: la frazione in cs %.4e, in phi %.6f; le bande di phi (il blocco phi -> phi, cs congelato: max ||lambda_b| - 1| %.2e): i pesi piu' grandi %s"
                      % (fcs, 1.0 - fcs, float(np.max(np.abs(np.abs(wb) - 1.0))), "; ".join("%.4f (omega_b %+.6f)" % (pes[q], -np.angle(wb[q])) for q in ordine[:3])))
                inv = np.linalg.inv(eb)
                contr = np.array([(Acf @ eb[:, q]) * (inv[q, :] @ Afc) / (lam_ - wb[q]) for q in range(12)])
                g = complex(np.sum(contr))
                oc = np.argsort(-np.abs(contr))
                print("      il meccanismo: A_cc %+.8f %+.8fi; |A_c,phi| %.4e, |A_phi,c| %.4e; lambda - A_cc = %+.6e %+.6ei, g(lambda) = %+.6e %+.6ei (lo scarto %.2e)"
                      % (Acc.real, Acc.imag, float(np.linalg.norm(Acf)), float(np.linalg.norm(Afc)), (lam_ - Acc).real, (lam_ - Acc).imag, g.real, g.imag, abs(lam_ - Acc - g)))
                print("      i contributi di banda piu' grandi: %s" % "; ".join("omega_b %+.6f: %+.4e %+.4ei (lambda - lambda_b = %+.3e %+.3ei)" % (-np.angle(wb[q]), contr[q].real, contr[q].imag, (lam_ - wb[q]).real, (lam_ - wb[q]).imag) for q in oc[:3]))
                out.update({"fcs": fcs, "banda": float(-np.angle(wb[ordine[0]])), "peso": float(pes[ordine[0]])})
            sys.stdout.flush()
            return out

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            # ============================================================== il DEVE a cs spento, e il DEVE FALLIRE
            print("### A cs SPENTO (mot.cs = None, mot.lambda_c = None): 12 reali per cella")
            b0 = base(LAM, None, "spento")
            print("    la base: omega %.10f per tick; il residuo di phi %.3e" % (b0["omega"], b0["res_phi"]))
            R0, dev0, _ = risposta(b0, None, "spento")
            sp0 = spettro(R0["spento"])
            print("    la linearita' %.2e; |lambda| fra %.15f e %.15f; max ||lambda| - 1| %.3e" % (dev0, sp0["min"], sp0["max"], sp0["dev_unit"]))
            esito("cs spento: lo spettro e' unitario, max ||lambda| - 1| < %g" % TOLL_UNIT, sp0["dev_unit"] < TOLL_UNIT, "%.3e" % sp0["dev_unit"])
            esito("cs spento: la linearita' |R(2a) - R(a)| / max|R| < %g" % TOLL_LIN, dev0 < TOLL_LIN, "%.2e" % dev0)
            print("### IL DEVE FALLIRE: lo stesso, con phi per (1 + %g) dopo il tick (tutta phi: il modo giusto sono tutti)" % FATT_F)
            Rf, devf, _ = risposta(b0, None, "spento", fattore=1.0 + FATT_F)
            spf = spettro(Rf["spento"])
            print("    |lambda| fra %.15f e %.15f" % (spf["min"], spf["max"]))
            esito("il fattore: |lambda| = %.3f entro 1e-9 su ogni k" % (1 + FATT_F), abs(spf["max"] - 1 - FATT_F) < 1e-9 and abs(spf["min"] - 1 - FATT_F) < 1e-9, "%.3e, %.3e" % (spf["max"] - 1 - FATT_F, spf["min"] - 1 - FATT_F))
            esito("il fattore: lo spettro e' unitario, max ||lambda| - 1| < %g" % TOLL_UNIT, spf["dev_unit"] < TOLL_UNIT, "%.3e" % spf["dev_unit"], deve=False)
            del R0, Rf
            # ============================================================== il caso di oggi: psi, la traslazione
            bo = base(LAM, lc_T2, "cs")
            print("### IL CASO DI OGGI: Lambda %g, Lambda_c %.6f, cs del vuoto %.12f; omega %.10f; r %.10f; i residui della base: phi %.3e, cs (F1) %.3e, cs (ist) %.3e"
                  % (LAM, lc_T2, float(bo["cs"][0]), bo["omega"], 1.0 - math.exp(-bo["omega"]), bo["res_phi"], bo["res_cf"], bo["res_ci"]))
            print("### (a) psi a psi = 0: la risposta di phi, cs a un impulso di psi del nodo 0 (le %d direzioni reali), e di psi a phi, cs" % (2 * npsi))
            pmax, Rpp = 0.0, np.zeros((n, 2 * npsi, 2 * npsi))
            for j in range(2 * npsi):
                a = A_REL
                us = {}
                for f in (1, -1):
                    ps = np.zeros(st["psi_h"].shape, dtype=st["psi_h"].dtype).reshape(n, npsi)
                    ps[0, j % npsi] += (1.0 if j < npsi else 1j) * f * a
                    p1, cf, ci, q1 = mappa(bo["phi"], bo["cs"], lc_T2, bo["u"], "cs", psi=ps.reshape(st["psi_h"].shape))
                    us[f] = (cella(p1, cf), q1.reshape(n, npsi))
                pmax = max(pmax, float(np.max(np.abs(us[1][0] - us[-1][0]))) / (2 * a))
                dq = (us[1][1] - us[-1][1]) / (2 * a)
                Rpp[:, :, j] = np.concatenate([dq.real, dq.imag], axis=1)
            spp = spettro(Rpp)
            del Rpp
            Ro, devo, psi_x = risposta(bo, lc_T2, "cs")
            print("    max |d(phi, cs)/d psi| %.3e; max |d psi/d(phi, cs)| %.3e (la soglia %g); il blocco psi -> psi: |lambda| fra %.12f e %.12f" % (pmax, psi_x, TOLL_PSI, spp["min"], spp["max"]))
            stacca = pmax < TOLL_PSI and psi_x < TOLL_PSI
            print("    ### psi %s al primo ordine: %s" % ("SI STACCA" if stacca else "NON si stacca", "si toglie dal vettore (13 reali per cella)" if stacca else "### resta: lo spettro qui sotto NON lo contiene (FERMO dopo questa corsa)"))
            esito("(a) psi si stacca al primo ordine (le due risposte incrociate sotto %g)" % TOLL_PSI, stacca, "%.3e, %.3e" % (pmax, psi_x))
            x0 = (Lt // 2) * Lt + 7
            Rx, _, _ = risposta(bo, lc_T2, "cs", x0=x0, colonne=(0, 12))
            dtr = 0.0
            for j in (0, 12):
                sh = np.roll(Ro["F1"][:, :, j].reshape(Lt, Lt, -1), (x0 // Lt, x0 % Lt), axis=(0, 1)).reshape(n, -1)
                dtr = max(dtr, float(np.max(np.abs(Rx["F1"][:, :, j] - sh))) / float(np.max(np.abs(sh))))
            esito("(d) l'invarianza per traslazione: l'impulso nel nodo %d = quello del nodo 0 traslato (le direzioni 0 e 12), sotto %g" % (x0, TOLL_TRASL), dtr < TOLL_TRASL, "%.3e" % dtr)
            del Rx
            # ============================================================== la mappa
            punti = [("oggi", LAM, lc_T2)]
            for lc in LC_SCAN:
                if lc != 34.0:
                    punti.append(("Lambda_c %g" % lc, LAM, lc))
            for s_ in S_SCAN:
                if s_ != s:
                    punti.append(("s %g" % s_, LAM, (LAM - 0.0) * (1.0 - s_) / s_))
            for lv in LAM_SCAN:
                if lv != 6.0:
                    punti.append(("Lambda %g" % lv, lv, lc_T2))
            print("### LA MAPPA: %d punti (Lambda_c 34 e s 0.15 sono il caso di oggi, con Lambda_c di T2 %.12f; Lambda 6 e' il caso di oggi)" % (len(punti), lc_T2))
            tab_ = []
            for nome, lv, lc in punti:
                b = bo if nome == "oggi" else base(lv, lc, "cs")
                R, dev, _ = (Ro, devo, psi_x) if nome == "oggi" else risposta(b, lc, "cs")
                print("  IL PUNTO %s: Lambda %g, Lambda_c %.6f, cs del vuoto %.10f; omega %.10f, r %.10f; i residui: phi %.3e, cs (F1) %.3e, cs (ist) %.3e; la linearita' %.2e"
                      % (nome, lv, lc, float(b["cs"][0]), b["omega"], 1.0 - math.exp(-b["omega"]), b["res_phi"], b["res_cf"], b["res_ci"], dev))
                if max(b["res_phi"], b["res_cf"], b["res_ci"]) > TOLL_PF:
                    print("    ### LA BASE NON E' UN PUNTO FISSO (oltre %g): la linearizzazione qui NON vale (dichiarato, non corretto)" % TOLL_PF)
                esito("%s: la linearita' < %g" % (nome, TOLL_LIN), dev < TOLL_LIN, "%.2e" % dev)
                for caso in ("F1", "ist"):
                    sp = spettro(R[caso])
                    d_ = descrivi(sp, "(L-%s)" % caso)
                    tab_.append({"punto": nome, "Lambda": lv, "Lambda_c": lc, "cs": float(b["cs"][0]), "caso": caso, "max": sp["max"], "d": d_, "pf": max(b["res_phi"], b["res_cf"], b["res_ci"]) <= TOLL_PF})
                    if nome == "oggi":
                        if caso == "F1":
                            sp_oggi, d_oggi = sp, d_
                del sp
                if nome != "oggi":
                    del R
            # ============================================================== il DEVE di oggi, e l'onda piana
            t_oggi = math.log(sp_oggi["max"])
            esito("oggi (L-F1): il tasso piu' grande %.5f riproduce %g entro il %g%%" % (t_oggi, RIF, 100 * TOLL_RIF), abs(t_oggi / RIF - 1.0) <= TOLL_RIF, "il rapporto %.4f" % (t_oggi / RIF))
            a1, a2 = d_oggi["m"]
            fase = np.exp(2j * np.pi * (a1 * i1 + a2 * i2) / Lt)
            dl = np.real(d_oggi["v"][None, :] * fase[:, None])
            dl *= ONDA_AMP / float(np.max(np.abs(dl)))
            print("### L'ONDA PIANA: al k (%d, %d), la parte reale dell'autovettore, l'ampiezza massima %g; F1 vero, %d tick, contro un gemello senza onda" % (a1, a2, ONDA_AMP, ONDA_N))
            D = []
            with F1.cs_primo_zero(True):
                stati = {}
                for nome, ph, cs in (("base", bo["phi"].copy(), bo["cs"].copy()), ("onda", bo["phi"] + (dl[:, :6] + 1j * dl[:, 6:12]).reshape(-1), bo["cs"] + dl[:, 12])):
                    vuoto_con(ph)
                    traccia = []
                    for k in range(1, ONDA_N + 1):
                        p0 = st["phi_h"].copy()
                        mot.cs = cs.copy()
                        mot.lambda_c = float(lc_T2)
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                        L = FP.cs(mot.densita_vuoto(st), lc_T2, fp).copy()
                        r = 1.0 - np.exp(-F1.omega_v(p0, st["phi_h"], mot.inc.nodo, mot.inc.n))
                        cs = F1.rilassa(cs, L, r)
                        traccia.append((st["phi_h"].copy(), cs.copy()))
                    stati[nome] = traccia
                for k in range(ONDA_N):
                    D.append(math.sqrt(float(np.sum(np.abs(stati["onda"][k][0] - stati["base"][k][0]) ** 2) + np.sum((stati["onda"][k][1] - stati["base"][k][1]) ** 2))))
                del stati
            D = np.array(D)
            tt = np.arange(1, ONDA_N + 1)
            sel = tt >= ONDA_DA
            t_onda = F1L.pendenza(tt[sel], np.log(D[sel]))
            print("    la differenza ai tick 1, 10, 20, 50, 100: %s; la pendenza di ln dal tick %d al %d: %.5f per tick" % (" ".join("%.3e" % D[t - 1] for t in (1, 10, 20, 50, 100) if t <= ONDA_N), ONDA_DA, ONDA_N, t_onda))
            esito("l'onda piana cresce col tasso dello spettro %.5f entro il %g%%" % (t_oggi, 100 * TOLL_ONDA), abs(t_onda / t_oggi - 1.0) <= TOLL_ONDA, "%.5f, il rapporto %.4f" % (t_onda, t_onda / t_oggi))
    # ================================================================== la tabella e le letture
    print("-" * 130)
    print("  LA MAPPA:")
    print("  %-16s %8s %12s %12s %6s %16s %12s %9s %8s %4s %10s %12s %6s" % ("il punto", "Lambda", "Lambda_c", "cs vuoto", "caso", "|lambda|_max", "ln per tick", "|k|", "dir", "neq", "frazione cs", "la banda", "p.f."))
    for r_ in tab_:
        d_ = r_["d"]
        print("  %-16s %8g %12.6f %12.8f %6s %16.12f %12.6f %9.5f %8.2f %4d %10.3e %12.6f %6s" % (r_["punto"], r_["Lambda"], r_["Lambda_c"], r_["cs"], "L-" + r_["caso"], r_["max"], math.log(r_["max"]), d_["k"], d_["dir"], d_["neq"], d_.get("fcs", float("nan")), d_.get("banda", float("nan")), "si" if r_["pf"] else "NO"))
    inst = {(r_["punto"], r_["caso"]): r_["max"] - 1.0 > STABILE for r_ in tab_}
    stabili = [(r_["punto"], r_["caso"]) for r_ in tab_ if not inst[(r_["punto"], r_["caso"])]]
    print("  instabili (|lambda|_max - 1 > %g): %d su %d; stabili: %s" % (STABILE, sum(inst.values()), len(inst), stabili if stabili else "nessuno"))
    if inst[("oggi", "ist")]:
        print("  LA LETTURA: (w1) (L-ist) e' gia' instabile nel caso di oggi: la colpa e' della LEGGE, non della memoria")
    elif inst[("oggi", "F1")]:
        print("  LA LETTURA: (w2) (L-ist) stabile e (L-F1) instabile nel caso di oggi: la colpa e' della MEMORIA di F1")
    if stabili:
        print("  LA LETTURA: (w3) nella mappa esistono punti stabili (qui sopra): una MAPPA, nessuna scelta")
    else:
        print("  LA LETTURA: (w4) instabile in tutta la mappa: il vuoto con questa legge del tempo locale e' instabile per costruzione. FERMO: la decisione e' di Luca")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
