# -*- coding: utf-8 -*-
r"""**S5.0 (f): LA SORGENTE MISTA DELL'OROLOGIO** *(sul ramo laterale; Luca `2026-11-11` `16:44`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.16`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_sorgente.py > doc/referti_l2/s5_sorgente_mista.txt

**`S` = la MATERIA con lo zero O1 + il VUOTO con lo zero locale O4** *(i `6` vicini)*. **Per nodo** *(il nodo piu' meta' dei suoi archi, da `energia_pesata.termini_di_h`)*: **il vuoto** = l'energia con
`psi = 0`; **l'accoppiamento** = `materia_vuoto.N(rho, Lambda)`; **la materia** = il totale meno il vuoto meno l'accoppiamento. **Tre attribuzioni dell'accoppiamento:** (A-m), (A-v), (A-mv).
**Le scene:** `TBS` a `10000` *(per zona)*; il vuoto uniforme `c(10000) F3`; il vuoto con le onde di H4 (v1). **I DEVE:** il vuoto uniforme `0`; lo zero globale per nodo; lo scarto previsto per
unita' di norma; `A_h` di H4; **DEVE FALLIRE:** il vuoto con lo zero O1. **Le letture (g1)-(g3).**
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

TOLL = 1e-12                    # ### Luca
C_NODO = -6.0 * math.pi         # ### mio: lo spostamento per nodo (un valore qualunque; quello del vuoto con O1)
C_NORMA = -0.5 * math.pi        # ### sez. 31.16 (c): il passaggio dallo zero di prima a O1, per unita' di norma
GUSCIO = (16.0, 18.0)           # ### Luca
LONTANO = 30.0                  # ### Luca
R_ZONA = 20.0                   # ### come H4 (A_h)
A_H_REF = "3.308833e-02"        # ### il referto di H4
ATTR = ("A-m", "A-v", "A-mv")
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
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import energia_pesata as EP
    import materia_vuoto as MV
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import h4_vuoto as H4
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "bordo", "carta_punto_fisso", "toro", "h4_vuoto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("energia_pesata", "materia_vuoto"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0 = CA.serie(CPF.CORSA)[0]
    w_in = float(rr0[0]["w_in"])
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    t00 = time.time()
    print("=" * 130)
    print("S5.0 (f) (sez. 31.16): la sorgente mista S = materia (O1) + vuoto (O4); le attribuzioni dell'accoppiamento %s; cs = s = %g uniforme" % (ATTR, s))
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
        n, Lt, m = inc.n, z["L"], inc.m
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        nodo = np.asarray(inc.nodo)
        coppie = nodo.reshape(m, 2)
        vicini = np.zeros((n, 6), dtype=int)
        conta = np.zeros(n, dtype=int)
        for a_, b_ in coppie:
            vicini[a_, conta[a_]] = b_
            conta[a_] += 1
            vicini[b_, conta[b_]] = a_
            conta[b_] += 1
        assert np.all(conta == 6), "i nodi NON hanno 6 vicini"

        def o4(e):
            return e - e[vicini].mean(axis=1)

        def per_nodo(psi, phi):
            for k in chiavi:
                st[k][...] = salvato[k]
            st["psi_h"][...] = psi
            st["phi_h"][...] = phi
            mot.cs = np.full(n, float(s))
            mot.lambda_c = None
            pn, pa = EP.termini_di_h(mot, st, par)
            e = pn.copy()
            np.add.at(e, coppie[:, 0], 0.5 * pa)
            np.add.at(e, coppie[:, 1], 0.5 * pa)
            rho = np.zeros(n)
            np.add.at(rho, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            lam = mot.densita_vuoto(st).copy()
            return e, rho, lam

        def parti(psi, phi):
            """### `(materia, vuoto, accoppiamento, rho, Lambda)` per nodo."""
            T, rho, lam = per_nodo(psi, phi)
            Vv, _r0, lam0 = per_nodo(np.zeros_like(psi), phi)
            assert np.array_equal(lam0, lam), "Lambda cambia con psi: la scomposizione non vale"
            cp = np.asarray(MV.N(rho, lam), dtype=float)
            return T - Vv - cp, Vv, cp, rho, lam

        def S_di(mat, vac, cp, attr, zero_vuoto="O4"):
            f = (lambda e: e) if zero_vuoto == "O1" else o4
            if attr == "A-m":
                return mat + cp + f(vac)
            if attr == "A-v":
                return mat + f(vac + cp)
            return mat + 0.5 * cp + f(vac + 0.5 * cp)

        zero_psi = np.zeros(st["psi_h"].shape, dtype=st["psi_h"].dtype)
        # ------------------------------------------------------------------ il vuoto uniforme
        mat0, vac0, cp0, _r, _l = parti(zero_psi, c * phi_v)
        print("### IL VUOTO UNIFORME c(10000) F3 (psi = 0): la materia max |.| %.3e; l'accoppiamento max %.3e; il vuoto (O1) da %.10e a %.10e" % (float(np.max(np.abs(mat0))), float(np.max(np.abs(cp0))), float(vac0.min()), float(vac0.max())))
        for a in ATTR:
            S0 = S_di(mat0, vac0, cp0, a)
            esito("il vuoto uniforme, %s: S = 0 entro %g per nodo" % (a, TOLL), float(np.max(np.abs(S0))) < TOLL, "max |S| %.3e" % float(np.max(np.abs(S0))))
        S0f = S_di(mat0, vac0, cp0, "A-m", zero_vuoto="O1")
        esito("il vuoto uniforme col vuoto contato con O1 (non O4): S = 0 entro %g" % TOLL, float(np.max(np.abs(S0f))) < TOLL, "S medio %.6f (-6 pi = %.6f)" % (float(S0f.mean()), -6 * math.pi), deve=False)
        # ------------------------------------------------------------------ TBS a 10000
        xs = stati[CPF.TICK_D4]
        with np.load(xs["file"]) as d:
            ps, ph = d["psi_h"].copy(), d["phi_h"].copy()
        for k in chiavi:
            st[k][...] = salvato[k]
        with np.load(xs["file"]) as d:
            for k in chiavi:
                st[k][...] = d[k]
        assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"
        mat, vac, cp, rho, lam = parti(ps, ph)
        M = float(rho.sum())
        vv = np.arange(n)
        c1, c2 = TO.centro(rho, vv // Lt, vv % Lt, Lt)[:2]
        pos = TO.scarti(vv // Lt, vv % Lt, c1, c2, Lt)
        rr = np.hypot(pos[:, 0], pos[:, 1])
        zone = (("il centro", rr < w_in), ("l'interno", (rr >= w_in) & (rr < GUSCIO[0])), ("il guscio", (rr >= GUSCIO[0]) & (rr < GUSCIO[1])),
                ("l'alone", (rr >= GUSCIO[1]) & (rr <= LONTANO)), ("il vuoto lontano", rr > LONTANO))
        print("### %s: M = la norma di materia %.6f; il centro di rho (%.5f, %.5f); w_in %.6f; per nodo: la materia (O1) somma %.6e, il vuoto (O1) somma %.6e, l'accoppiamento somma %.6e"
              % (os.path.basename(xs["file"]), M, c1, c2, w_in, float(mat.sum()), float(vac.sum()), float(cp.sum())))
        print("  %-17s %6s %6s %14s %14s %14s %12s %14s" % ("la zona", "nodi", "attr", "S medio", "S min", "S max", "f(S<0) rho", "rho medio"))
        letture = {}
        for a in ATTR:
            S = S_di(mat, vac, cp, a)
            for nome, msk in zone:
                x = S[msk]
                w = rho[msk]
                fn = float(w[x < 0].sum() / w.sum()) if w.sum() > 0 else float("nan")
                print("  %-17s %6d %6s %+14.6e %+14.6e %+14.6e %12.4e %14.4e" % (nome, int(msk.sum()), a, float(x.mean()), float(x.min()), float(x.max()), fn, float(rho[msk].mean())))
            tot = float(S.sum())
            neg = float(S[S < 0].sum())
            fz = {nome: (float(rho[msk][S[msk] < 0].sum() / rho[msk].sum()) if rho[msk].sum() > 0 else 0.0) for nome, msk in zone}
            print("    %s: il totale di S %+.6e; S / M %+.6f; la somma delle parti negative %+.6e (%.4f del totale positivo)" % (a, tot, tot / M, neg, -neg / float(S[S > 0].sum())))
            letture[a] = (tot, fz, neg / float(S[S > 0].sum()))
            # ------------------------------------------------------------- lo zero globale
            Tn = mat + vac + cp
            mat_c = (Tn + C_NODO) - (vac + C_NODO) - cp
            S_c = S_di(mat_c, vac + C_NODO, cp, a)
            dn = float(np.max(np.abs(S_c - S)))
            esito("%s: S identica dopo lo spostamento dello zero globale di %.4f PER NODO (entro %g)" % (a, C_NODO, TOLL * max(1.0, float(np.max(np.abs(S))))), dn <= TOLL * max(1.0, float(np.max(np.abs(S)))), "%.3e" % dn)
            mat_u = (Tn + C_NORMA * (rho + lam)) - (vac + C_NORMA * lam) - cp - C_NORMA * rho
            S_u = S_di(mat_u, vac + C_NORMA * lam, cp, a)
            prev = C_NORMA * (lam - lam[vicini].mean(axis=1))
            du = float(np.max(np.abs((S_u - S) - prev)))
            print("    %s, lo zero per unita' di norma (c = %.4f): lo scarto di S max %.3e (previsto c (Lambda_k - media Lambda_j), max %.3e)" % (a, C_NORMA, float(np.max(np.abs(S_u - S))), float(np.max(np.abs(prev)))))
            esito("%s: lo scarto per unita' di norma = c (Lambda_k - media_j Lambda_j) entro %g" % (a, TOLL * max(1.0, float(np.max(np.abs(S))))), du <= TOLL * max(1.0, float(np.max(np.abs(S)))), "%.3e" % du)
        # ------------------------------------------------------------------ il vuoto con le onde di H4 (v1)
        zona = rr[nodo] > R_ZONA
        res = ph - c * phi_v
        A_h = float(np.sqrt(np.mean(np.abs(res[zona]) ** 2)))
        esito("A_h = quello di H4 (%s, alla settima cifra)" % A_H_REF, "%.6e" % A_h == A_H_REF, "%.6e" % A_h)
        Pr, bins, dk = H4.spettro(np.where(zona, res, 0.0), Lt, n)
        rg = np.random.default_rng(CPF.SEME)
        W = (rg.normal(size=(Lt, Lt, 6)) + 1j * rg.normal(size=(Lt, Lt, 6))) * np.sqrt(Pr[bins])[..., None]
        dlt = np.fft.ifft2(W, axes=(0, 1)).reshape(-1)
        dlt -= (np.vdot(phi_v, dlt) / np.vdot(phi_v, phi_v)) * phi_v
        n3 = float(np.vdot(phi_v, phi_v).real)
        dd = dlt * (A_h / float(np.sqrt(np.mean(np.abs(dlt) ** 2))))
        al = math.sqrt(1.0 - float(np.vdot(dd, dd).real) / n3)
        phd = c * (al * phi_v + dd)
        matw, vacw, cpw, _r, lamw = parti(zero_psi, phd)
        Sw = S_di(matw, vacw, cpw, "A-m")
        print("### IL VUOTO CON LE ONDE di H4 (v1) (A_h %.6e, 1 - alpha %.3e): S per nodo (le tre attribuzioni coincidono: psi = 0): la media %+.6e, la rms %.6e, il min %+.6e, il max %+.6e, la frazione negativa %.4f; la somma %+.6e"
              % (A_h, 1.0 - al, float(Sw.mean()), float(np.std(Sw)), float(Sw.min()), float(Sw.max()), float(np.mean(Sw < 0)), float(Sw.sum())))
        print("  accanto, il vuoto con O1 sulla stessa scena: la media %+.6e, la rms %.6e" % (float(vacw.mean()), float(np.std(vacw))))
    # ================================================================== le letture
    print("-" * 130)
    for a in ATTR:
        tot, fz, rneg = letture[a]
        dentro = max(fz["il centro"], fz["il guscio"], fz["l'alone"])
        if tot > 0 and dentro < 0.01:
            print("  LA LETTURA, %s: (g1) S >= 0 nel centro, nel guscio e nell'alone (la frazione negativa pesata al piu' %.4f) e il totale positivo (%+.6e): la sorgente e' sana" % (a, dentro, tot))
        elif tot > 0:
            print("  LA LETTURA, %s: (g2) zone negative (la frazione pesata: il centro %.4f, il guscio %.4f, l'alone %.4f), il totale positivo (%+.6e): l'energia di LEGAME; le parti negative valgono %.4f del totale positivo" % (a, fz["il centro"], fz["il guscio"], fz["l'alone"], tot, -rneg))
        else:
            print("  LA LETTURA, %s: (g3) il totale e' negativo (%+.6e): FERMO" % (a, tot))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
