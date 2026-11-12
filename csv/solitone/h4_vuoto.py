# -*- coding: utf-8 -*-
r"""**H4: IL VUOTO COL TEMPO LOCALE REGGE I DISTURBI?** *(sul ramo laterale; Luca `2026-11-10` `16:06`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `27.10`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/h4_vuoto.py --corsa vuoto > doc/referti_l2/h4_vuoto_disturbato.txt
    python csv/solitone/h4_vuoto.py --corsa iq    > doc/referti_l2/h4_distribuzione.txt

**`vuoto`:** il controllo dello strumento *(`10` nodi a `Lambda = 0.002`)*; **`A_h`** *(la rms del residuo `phi - c F3` di `TBS` a `10000` oltre `r 20`)* **e lo spettro radiale**; **(v0)** il vuoto `c(10000) F3`, F1; **(v1)** col disturbo `A_h`, F1;
**(v2)** lo stesso, `cs` SPENTO; **(v3)** `A_h / 10`, F1; **il gemello di (v1) e (v2)** *(`phi` della cella del nodo `0` per `1 + 1e-10`)*. **`iq`:** la scena di (i) *(`TBS` a `10000`, F1)* con la distribuzione.
**F1 come T2** *(il rilassamento esatto, (q2), il bordo spento)*. **Ogni `50` tick:** `cs` min, i quantili, le frazioni sotto `1e-3` e `1e-2`, `Lambda` min e la rms, le norme. **Le letture (u1)-(u3), (e1)-(e2).**
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

N_TICK = 5000                  # ### Luca: 5000 tick ciascuna
N_RIPIEGO = 3000               # ### il tetto di 60 minuti per corsa (come T2)
TETTO_S = 3600.0
OGNI = 50                      # ### Luca: ogni 50 tick
QUANT = (0.001, 0.01, 0.1, 0.5)   # ### Luca: i quantili 0.1%, 1%, 10%, 50%
SOGLIE = (1e-3, 1e-2)          # ### Luca: le frazioni sotto 1e-3 e 1e-2
R_ZONA = 20.0                  # ### Luca: la zona r > 20 per A_h
GEMELLO = 1e-10                # ### Luca: il gemello disturbato di 1e-10
SOGLIA_LYAP = F1L.SOGLIA_LYAP  # ### come T2
LAM_PROVA, N_PROVA = 0.002, 10   # ### Luca: 10 nodi a Lambda = 0.002
CALMO = 0.7                    # ### Luca (u2): cs min sopra 0.7 s
RMS_V2 = 0.10                  # ### Luca (u1): la rms di Lambda in (v2) entro il 10%
E1, E2 = 1e-3, 1e-2            # ### Luca (e1), (e2)
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


def statistiche(cs, lam):
    q = np.quantile(cs, QUANT)
    return {"cs_min": float(cs.min()), "q": [float(x) for x in q], "f3": float(np.mean(cs < SOGLIE[0])), "f2": float(np.mean(cs < SOGLIE[1])),
            "lam_min": float(lam.min()), "lam_rms": float(np.std(lam))}


def corsa(st, mot, par, lc, cs0, n_tick, f1, tieni_lam=False, base_lam=None):
    """### **F1 come `carta_f1_lunga.corsa`** *(q2)* **o `cs` SPENTO** *(`mot.cs = None`, `mot.lambda_c = None`)*; **ogni `OGNI` tick le statistiche** *(a `cs` spento quelle di `L = FP.cs(Lambda)`)*.
    `tieni_lam`: tiene `Lambda` di ogni tick; `base_lam`: la differenza `max|Lambda - base|` a ogni tick."""
    import composizione as CM
    import flussi_parziali as FP
    import tick as TK
    fp = np.zeros(mot.inc.n)
    cs = cs0.copy() if cs0 is not None else None
    camp, lam_m, lams, diff = [], [], [], []
    t0 = time.time()
    n = n_tick
    with F1.cs_primo_zero(f1):
        for k in range(1, n_tick + 1):
            if k > n:
                break
            if f1:
                phi0 = st["phi_h"].copy()
                mot.cs = cs.copy()
                mot.lambda_c = float(lc)
            else:
                mot.cs = None
                mot.lambda_c = None
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            lam = mot.densita_vuoto(st).copy()
            L = FP.cs(lam, lc, fp).copy()
            if f1:
                r = 1.0 - np.exp(-F1.omega_v(phi0, st["phi_h"], mot.inc.nodo, mot.inc.n))
                cs = F1.rilassa(cs, L, r)
                if float(cs.min()) <= 0.0:
                    raise F1L.Muro("tick %d: cs min %.3e <= 0" % (k, float(cs.min())))
            lam_m.append(float(lam.mean()))
            if tieni_lam:
                lams.append(lam)
            if base_lam is not None:
                diff.append(float(np.max(np.abs(lam - base_lam[k - 1]))))
            if k == OGNI and n_tick == N_TICK and (time.time() - t0) / OGNI * N_TICK * (2 if (tieni_lam or base_lam is not None) else 1) > TETTO_S:
                n = N_RIPIEGO
                print("    ### il tetto di 60 minuti: la proiezione supera %g s, la corsa va a %d tick (dichiarato)" % (TETTO_S, n))
            if k % OGNI == 0:
                c = statistiche(cs if f1 else L, lam)
                c.update({"t": k, "norma_phi": float(np.sum(np.abs(st["phi_h"]) ** 2)), "norma_psi": float(np.sum(np.abs(st["psi_h"]) ** 2)), "cs_media": float((cs if f1 else L).mean()),
                          "diff": diff[-1] if diff else None})
                camp.append(c)
    return {"camp": camp, "lam_media": np.array(lam_m), "lams": lams, "diff": np.array(diff), "n": min(n, n_tick), "s": time.time() - t0}


def stampa(nome, ris):
    print("  %s: %d tick, %.0f s" % (nome, ris["n"], ris["s"]))
    print("    %6s %10s %10s %10s %10s %10s %9s %9s %10s %10s %20s %10s %10s" % ("tick", "cs min", "q 0.1%", "q 1%", "q 10%", "q 50%", "f<1e-3", "f<1e-2", "Lambda min", "rms Lambda", "la norma di phi", "di psi", "gemello"))
    for c in ris["camp"]:
        print("    %6d %10.3e %10.3e %10.3e %10.3e %10.3e %9.2e %9.2e %10.3e %10.3e %20.10f %10.3e %10s" % (c["t"], c["cs_min"], c["q"][0], c["q"][1], c["q"][2], c["q"][3], c["f3"], c["f2"], c["lam_min"], c["lam_rms"],
              c["norma_phi"], c["norma_psi"], "%.3e" % c["diff"] if c["diff"] is not None else "-"))
    sys.stdout.flush()


def lyapunov(nome, d):
    oltre = np.flatnonzero(d > SOGLIA_LYAP)
    fine = int(oltre[0]) if len(oltre) else len(d)
    tt = np.arange(1, fine + 1)
    ok = d[:fine] > 0
    ly = F1L.pendenza(tt[ok], np.log(d[:fine][ok])) if np.sum(ok) >= 2 else float("nan")
    print("  %s, il gemello: la stima di Lyapunov dal tick 1 al %d (la differenza di Lambda sotto %g): %.5f per tick; la differenza alla fine %.3e" % (nome, fine, SOGLIA_LYAP, ly, d[-1] if len(d) else float("nan")))


def terzi(camp, chiave):
    n = len(camp)
    a, b = camp[: n // 3], camp[2 * n // 3:]
    return float(np.mean([c[chiave] for c in a])), float(np.mean([c[chiave] for c in b]))


def spettro(res, Lt, n):
    """### **Lo spettro radiale** del residuo nella cella `(L, L, 6)`: `(i bin, la potenza per bin, il bin di ogni k, dk)`."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    B = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
    F = np.fft.fft2(res.reshape(Lt, Lt, -1), axes=(0, 1))
    P = np.sum(np.abs(F) ** 2, axis=2)
    m = np.fft.fftfreq(Lt) * Lt
    M1, M2 = np.meshgrid(m, m, indexing="ij")
    kk = None
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            kv = ((M1 + a * Lt)[..., None] * B[0] + (M2 + b * Lt)[..., None] * B[1]) / Lt
            q = np.hypot(kv[..., 0], kv[..., 1])
            kk = q if kk is None else np.minimum(kk, q)
    dk = float(np.hypot(*B[0])) / Lt
    bins = np.floor(kk / dk + 0.5).astype(int)
    nb = int(bins.max()) + 1
    Pr = np.bincount(bins.ravel(), weights=P.ravel(), minlength=nb) / np.maximum(np.bincount(bins.ravel(), minlength=nb), 1)
    return Pr, bins, dk


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import flussi_parziali as FP
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    quale = sys.argv[sys.argv.index("--corsa") + 1]
    assert quale in ("vuoto", "iq"), "--corsa vuoto | iq"
    for m in ("__init__", "corsa_accensione", "toro", "bordo", "carta_punto_fisso", "carta_f1", "carta_f1_lunga"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0 = CA.serie(CPF.CORSA)[0]
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    t00 = time.time()
    print("=" * 130)
    print("H4 (sez. 27.10), %s: F1 (q2), il bordo spento; %d tick; ogni %d; i quantili %s; le soglie %s; c(%d) = %+.12f %+.12fi" % (quale, N_TICK, OGNI, QUANT, SOGLIE, CPF.TICK_D4, c.real, c.imag))
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
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        lam0 = mot.densita_vuoto(st).copy()
        lc = float(np.mean(lam0)) * (1.0 - s) / s
        print("### Lambda_c = %.12f; Lambda del vuoto %.17g (min %.17g, max %.17g); s %g" % (lc, float(lam0.mean()), float(lam0.min()), float(lam0.max()), s))
        xs = stati[CPF.TICK_D4]

        def carica():
            for k in chiavi:
                st[k][...] = salvato[k]
            with np.load(xs["file"]) as d:
                for k in chiavi:
                    st[k][...] = d[k]
            assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"

        def vuoto_con(phi):
            for k in chiavi:
                st[k][...] = salvato[k]
            st["psi_h"][...] = 0.0
            st["phi_h"][...] = phi

        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            if quale == "iq":
                carica()
                L0 = FP.cs(mot.densita_vuoto(st), lc, np.zeros(n)).copy()
                print("### (i-q): la partenza %s; F1 tutto insieme, come (i)" % os.path.basename(xs["file"]))
                ris = corsa(st, mot, par, lc, L0, N_TICK, True)
                stampa("(i-q)", ris)
                print("-" * 130)
                f3 = [c_["f3"] for c_ in ris["camp"]]
                a, b = terzi(ris["camp"], "f3")
                print("  (i-q) la frazione sotto 1e-3: il massimo %.3e (al tick %d); la media del primo terzo %.3e, dell'ultimo %.3e; alla fine %.3e" % (max(f3), ris["camp"][int(np.argmax(f3))]["t"], a, b, f3[-1]))
                if max(f3) < E1:
                    print("  LA LETTURA: (e1) la frazione sotto 1e-3 resta sotto %g per tutta la corsa: pochi nodi, il minimo e' un valore estremo" % E1)
                elif f3[-1] > E2 and b > a:
                    print("  LA LETTURA: (e2) la frazione sotto 1e-3 cresce oltre %g: e' il vuoto intero che si svuota" % E2)
                else:
                    print("  LA LETTURA: caso intermedio (il massimo %.3e, alla fine %.3e)" % (max(f3), f3[-1]))
            else:
                # ------------------------------------------------------------ lo strumento: 10 nodi a Lambda = 0.002
                vuoto_con(c * phi_v)
                nodi_p = np.random.default_rng(CPF.SEME).choice(n, N_PROVA, replace=False)
                for x in nodi_p:
                    e = np.flatnonzero(inc.nodo == x)
                    st["phi_h"][e] *= math.sqrt(LAM_PROVA / float(np.sum(np.abs(st["phi_h"][e]) ** 2)))
                lp = mot.densita_vuoto(st).copy()
                sp = statistiche(FP.cs(lp, lc, np.zeros(n)).copy(), lp)
                print("### lo strumento su uno stato di prova: %d nodi a Lambda %g (Lambda di quei nodi %s); cs di quei nodi %.3e" % (N_PROVA, LAM_PROVA, ", ".join("%.6g" % lp[x] for x in nodi_p[:3]), float(FP.cs(lp, lc, np.zeros(n))[nodi_p[0]])))
                esito("lo strumento: la frazione sotto 1e-3 = %d/%d esatta" % (N_PROVA, n), sp["f3"] == N_PROVA / n, "%.6e contro %.6e" % (sp["f3"], N_PROVA / n))
                esito("lo strumento: «la frazione sotto 1e-3 e' zero (il vuoto calmo)» sullo stato di prova", sp["f3"] == 0.0, "%.3e" % sp["f3"], deve=False)
                # ------------------------------------------------------------ A_h e lo spettro
                with np.load(xs["file"]) as d:
                    phs, pss = d["phi_h"].copy(), d["psi_h"].copy()
                rho = np.zeros(n)
                np.add.at(rho, inc.nodo, np.sum(np.abs(pss) ** 2, axis=1))
                vv = np.arange(n)
                c1, c2 = TO.centro(rho, vv // Lt, vv % Lt, Lt)[:2]
                pos = TO.scarti(vv // Lt, vv % Lt, c1, c2, Lt)
                rr = np.hypot(pos[:, 0], pos[:, 1])
                zona = rr[inc.nodo] > R_ZONA
                res = phs - c * phi_v
                A_h = float(np.sqrt(np.mean(np.abs(res[zona]) ** 2)))
                ap = complex(np.vdot(phi_v[zona], phs[zona]) / np.vdot(phi_v[zona], phi_v[zona]))
                print("### A_h: la rms di |phi - c F3| sulle %d estremita' a r > %g dal centro di rho (%.5f, %.5f) di %s: %.6e; |F3| per estremita' %.6f; la proiezione sulla zona a = %+.8f %+.8fi (c = %+.8f %+.8fi, |a - c| %.3e)"
                      % (int(zona.sum()), R_ZONA, c1, c2, os.path.basename(xs["file"]), A_h, float(np.sqrt(np.mean(np.abs(phi_v) ** 2))), ap.real, ap.imag, c.real, c.imag, abs(ap - c)))
                Pr, bins, dk = spettro(np.where(zona, res, 0.0), Lt, n)
                kp = int(np.argmax(Pr[1:])) + 1
                print("### lo spettro radiale del residuo (la zona r <= %g a zero; dk %.5f): il picco al bin %d (|k| %.4f); la potenza per bin 0..%d: %s" % (R_ZONA, dk, kp, kp * dk, min(len(Pr), 40) - 1, " ".join("%.2e" % x for x in Pr[:40])))
                rg = np.random.default_rng(CPF.SEME)
                W = (rg.normal(size=(Lt, Lt, 6)) + 1j * rg.normal(size=(Lt, Lt, 6))) * np.sqrt(Pr[bins])[..., None]
                dlt = np.fft.ifft2(W, axes=(0, 1)).reshape(-1)
                dlt -= (np.vdot(phi_v, dlt) / np.vdot(phi_v, phi_v)) * phi_v
                n3 = float(np.vdot(phi_v, phi_v).real)

                def disturbato(A):
                    dd = dlt * (A / float(np.sqrt(np.mean(np.abs(dlt) ** 2))))
                    al = math.sqrt(1.0 - float(np.vdot(dd, dd).real) / n3)
                    ph = c * (al * phi_v + dd)
                    print("    il disturbo A %.4e: 1 - alpha %.3e; la norma di phi %.10f contro il vuoto %.10f (relativa %.2e); |<F3, delta>| / |F3|^2 %.2e"
                          % (A, 1.0 - al, float(np.vdot(ph, ph).real), n3, float(np.vdot(ph, ph).real) / n3 - 1.0, abs(complex(np.vdot(phi_v, dd))) / n3))
                    return ph
                ris = {}
                for nome, A, f1, gem in (("(v0)", 0.0, True, False), ("(v1)", A_h, True, True), ("(v2)", A_h, False, True), ("(v3)", A_h / 10.0, True, False)):
                    print("### LA CORSA %s: A %.4e, %s%s" % (nome, A, "F1" if f1 else "cs SPENTO", ", col gemello" if gem else ""))
                    ph = disturbato(A) if A > 0 else c * phi_v
                    vuoto_con(ph)
                    cs0 = FP.cs(mot.densita_vuoto(st), lc, np.zeros(n)).copy() if f1 else None
                    try:
                        ris[nome] = corsa(st, mot, par, lc, cs0, N_TICK, f1, tieni_lam=gem)
                    except F1L.Muro as e:
                        print("  ### %s IL MURO: %s" % (nome, e))
                        ris[nome] = None
                        continue
                    stampa(nome, ris[nome])
                    if gem:
                        ph2 = ph.copy()
                        ph2[0:6] *= (1.0 + GEMELLO)
                        vuoto_con(ph2)
                        cs0 = FP.cs(mot.densita_vuoto(st), lc, np.zeros(n)).copy() if f1 else None
                        try:
                            g = corsa(st, mot, par, lc, cs0, ris[nome]["n"], f1, base_lam=ris[nome]["lams"])
                            lyapunov(nome, g["diff"])
                            print("    il gemello, la differenza ai tick 50, 500, 1000, 2000, fine: %s" % " ".join("%.3e" % g["diff"][t - 1] for t in (50, 500, 1000, 2000, len(g["diff"])) if t <= len(g["diff"])))
                        except F1L.Muro as e:
                            print("  ### %s, il gemello: IL MURO: %s" % (nome, e))
                        ris[nome]["lams"] = []
                    if nome == "(v0)":
                        dcs_dl = lc / (float(lam0.mean()) + lc) ** 2
                        tv = {c_["t"]: c_ for c_ in ris[nome]["camp"]}
                        cs00 = float(FP.cs(lam0, lc, np.zeros(n)).mean())
                        okv = True
                        for t in sorted({OGNI, 1000, ris[nome]["n"]} & set(range(1, ris[nome]["n"] + 1))):
                            dl = float(ris[nome]["lam_media"][t - 1] - lam0.mean())
                            att = dcs_dl * dl
                            mis = tv[t]["cs_media"] - cs00
                            dentro = (att != 0.0 and mis * att > 0 and 0.5 <= mis / att <= 2.0) or (att == 0.0 and mis == 0.0)
                            okv = okv and dentro
                            print("    F1-V tick %5d: la deriva di Lambda %+.4e; di cs misurata %+.4e, attesa %+.4e: %s" % (t, dl, mis, att, "ENTRO un fattore 2" if dentro else "### FUORI"))
                        esito("(v0) F1-V: la deriva di cs entro un fattore 2 da dcs/dLambda x la deriva di Lambda, ai tick %d, 1000, %d" % (OGNI, ris[nome]["n"]), okv)
    if quale == "vuoto":
        print("-" * 130)
        v1, v2, v3 = ris.get("(v1)"), ris.get("(v2)"), ris.get("(v3)")

        def turb(r):
            if r is None:
                return True
            a, b = terzi(r["camp"], "f3")
            return min(c_["cs_min"] for c_ in r["camp"]) < 1e-3 and b > a

        def calmo(r):
            return r is not None and min(c_["cs_min"] for c_ in r["camp"]) > CALMO * s
        for nome, r in (("(v1)", v1), ("(v3)", v3)):
            if r is not None:
                a, b = terzi(r["camp"], "f3")
                print("  %s: cs min %.3e (il minimo della corsa); la frazione sotto 1e-3, il primo terzo %.3e, l'ultimo %.3e; turbolento %s; calmo (cs min > %g s) %s" % (nome, min(c_["cs_min"] for c_ in r["camp"]), a, b, turb(r), CALMO, calmo(r)))
        if v2 is not None:
            r0 = v2["camp"][0]["lam_rms"]
            dev = max(abs(c_["lam_rms"] / r0 - 1.0) for c_ in v2["camp"])
            print("  (v2): la rms di Lambda al primo campione %.4e; lo scarto relativo massimo %.4f (entro %g: %s)" % (r0, dev, RMS_V2, dev <= RMS_V2))
            v2ok = dev <= RMS_V2
        else:
            v2ok = False
        if turb(v1) and v2ok:
            print("  LA LETTURA: (u1) H4 REGGE: (v1) turbolento, (v2) calmo nella rms di Lambda: il vuoto col tempo locale non regge i disturbi, il solitone non serve")
        if calmo(v1):
            print("  LA LETTURA: (u2) H4 CADE: (v1) resta calmo (cs min sopra %g s): la discesa ha bisogno del solitone" % CALMO)
        if turb(v1) and calmo(v3):
            print("  LA LETTURA: (u3) una soglia: (v1) turbolento con A_h, (v3) calmo con A_h / 10")
        if not (turb(v1) and v2ok) and not calmo(v1) and not (turb(v1) and calmo(v3)):
            print("  LA LETTURA: caso intermedio (nessuna di u1, u2, u3)")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
