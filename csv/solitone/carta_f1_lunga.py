# -*- coding: utf-8 -*-
r"""**T2, LA CARTA F1 ALLUNGATA** *(sul ramo laterale; Luca `2026-11-09` `20:13`, ripartito `2026-11-10` `01:22`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `25`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/carta_f1_lunga.py > doc/referti_l2/carta_f1_lunga.txt

**F1 di `carta_f1.py`** *(le sue funzioni, importate: il rilassamento esatto, `r = 1 - e^{-omega_v}`, (q2))* **a `5000` tick** *(il tetto dei `60` minuti: `3000`, sez. `25.1`)*: **il vuoto F3 da solo** *(F1-V come LETTURA,
il criterio di Luca)*; **la base da `TBS` a `10000` tick e due perturbazioni sul centro, `1e-8` e `1e-10`.** **Ogni `100` tick:** la differenza, `cs` min col raggio, `r` max, la norma, il calore. **Le letture s1-s4.**
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
from solitone import carta_punto_fisso as CPF  # noqa: E402

N_TICK = 5000                  # ### sez. 25.1 (1)
N_RIPIEGO = 3000               # ### sez. 25.1 (1): il mandato
TETTO_S = 3600.0               # ### sez. 25.1 (1): 60 minuti
N_STIMA = 100                  # ### sez. 25.1 (1): i tick su cui si stima il costo
AMPIEZZE = (1e-8, 1e-10)       # ### sez. 25.1 (2)
OGNI = 100                     # ### sez. 25.1 (3)
SOGLIA_LYAP = 1e-4             # ### sez. 25.1 (4) = carta_f1.SOGLIA_OLTRE
TICK_V = (50, 1000)            # ### sez. 25.1 (5), piu' la fine
FATT_V = 2.0                   # ### Luca: F1-V «entro un fattore 2»
P_S1, F_S1, P_S4, F_S4 = 0.1, 2.0, 0.05, 0.05   # ### sez. 25.2
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


class Muro(Exception):
    pass


def corsa(st, mot, par, lc, cs0, n_tick, rr, base=None, tieni=False, tempo=None):
    """### Come `carta_f1.corsa` in (q2), con i campioni ogni `OGNI` tick. `base`: la lista dei `cs` della base (la differenza a ogni tick); `tieni`: tiene `cs` di ogni tick.
    ### (s3): `cs` min `<= 0` alza `Muro` col tick, il raggio e `Lambda` locale; un'eccezione del tick si riporta uguale."""
    import composizione as CM
    import energia_pesata as EP
    import flussi_parziali as FP
    import tick as TK
    fp = np.zeros(mot.inc.n)
    cs = cs0.copy()
    calore = 0.0
    tutti, camp, diff, lam_m = [], [], [], []
    t0 = time.time()
    with F1.cs_primo_zero(True):
        for k in range(1, n_tick + 1):
            phi0 = st["phi_h"].copy()
            mot.cs = cs.copy()
            mot.lambda_c = float(lc)
            try:
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            except Exception as e:
                raise Muro("tick %d: il tick alza %s: %s" % (k, type(e).__name__, str(e)[:120]))
            r = 1.0 - np.exp(-F1.omega_v(phi0, st["phi_h"], mot.inc.nodo, mot.inc.n))
            lam = mot.densita_vuoto(st)
            L = FP.cs(lam, lc, fp).copy()
            g0 = EP.g_pesata(mot, st, par)
            cs1 = F1.rilassa(cs, L, r)
            mot.cs = cs1.copy()
            g1 = EP.g_pesata(mot, st, par)
            calore += float(g1 - g0)
            cs = cs1
            i = int(np.argmin(cs))
            if cs[i] <= 0.0:
                raise Muro("tick %d: cs min %.3e <= 0 al nodo %d, il raggio %.2f, Lambda locale %.6f" % (k, float(cs[i]), i, float(rr[i]), float(lam[i])))
            lam_m.append(float(lam.mean()))
            if tieni:
                tutti.append(cs.copy())
            if base is not None:
                diff.append(float(np.max(np.abs(cs - base[k - 1]))))
            if k % OGNI == 0 or k in TICK_V or k == n_tick:
                camp.append({"t": k, "cs_min": float(cs[i]), "raggio": float(rr[i]), "r_max": float(r.max()), "norma": float(np.sum(np.abs(st["psi_h"]) ** 2)),
                             "calore": calore, "cs_media": float(cs.mean()), "diff": diff[-1] if diff else None})
            if tempo is not None and k == N_STIMA:
                tempo.append((time.time() - t0) / N_STIMA)
    return {"cs": tutti, "camp": camp, "diff": np.array(diff), "lam_media": np.array(lam_m), "cs_fine": cs}


def ultimo_terzo(camp, n):
    return [c for c in camp if c["t"] % OGNI == 0 and c["t"] > 2 * n / 3.0]


def pendenza(x, y):
    return float(np.polyfit(np.asarray(x, float), np.asarray(y, float), 1)[0])


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
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "toro", "carta_punto_fisso", "carta_f1"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0, _camp = CA.serie(CPF.CORSA)[:2]
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    t00 = time.time()
    print("=" * 130)
    print("T2, LA CARTA F1 ALLUNGATA (sez. 25): %s a %d tick; %d tick (il tetto %g s: %d); le ampiezze %s sul centro; ogni %d tick" % (CPF.CORSA, CPF.TICK_D4, N_TICK, TETTO_S, N_RIPIEGO, AMPIEZZE, OGNI))
    print("=" * 130)
    rg = np.random.default_rng(CPF.SEME)
    cs_ = rg.uniform(0.01, 0.3, 1000)
    L_ = rg.uniform(0.01, 0.3, 1000)
    r_ = 1.0 - np.exp(-rg.uniform(0.0, 1.5, 1000))
    d1 = float(np.max(np.abs(F1.inversa(F1.rilassa(cs_, L_, r_), L_, r_) - cs_) / cs_))
    esito("F1-I l'inversa del rilassamento al confine ridà cs entro 1e-14 relativo (1000 terne a caso)", d1 <= 1e-14, "%.2e" % d1)
    d2 = float(np.max(np.abs(F1.inversa_trapezio(F1.rilassa(cs_, L_, r_), L_, r_) - cs_) / cs_))
    esito("F1-F il rilassamento invertito col TRAPEZIO ridà cs entro 1e-14", d2 <= 1e-14, "%.2e" % d2, deve=False)
    n = N_TICK
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
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        # ------------------------------------------------------------------ F1-V, il vuoto F3 da solo
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        lam0 = mot.densita_vuoto(st).copy()
        lc = float(np.mean(lam0)) * (1.0 - s) / s
        print("### Lambda_c = %.12f; Lambda del vuoto all'inizio %.17g" % (lc, float(lam0.mean())))
        tempo = []
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            cs0 = FP.cs(lam0, lc, np.zeros(inc.n)).copy()
            # ### il tetto dei 60 minuti: si stima sui primi N_STIMA tick del vuoto, poi si decide n
            prova = corsa(st, mot, par, lc, cs0, N_STIMA, np.zeros(inc.n), tempo=tempo)
            proiez = tempo[0] * N_TICK * 4
            if proiez > TETTO_S:
                n = N_RIPIEGO
            print("### il costo: %.4f s per tick sui primi %d del vuoto; la proiezione per 4 corse da %d: %.0f s: %s" % (tempo[0], N_STIMA, N_TICK, proiez, "SOTTO il tetto, %d tick" % n if n == N_TICK else "### SOPRA il tetto: TUTTE le corse a %d tick (dichiarato)" % n))
            del prova
            st["psi_h"][...] = 0.0
            st["phi_h"][...] = phi_v
            vv = corsa(st, mot, par, lc, cs0, n, np.zeros(inc.n), tieni=False)
        dcs_dl = lc / (float(lam0.mean()) + lc) ** 2
        print("  F1-V, LA LETTURA (Luca): dcs/dLambda = Lambda_c/(Lambda + Lambda_c)^2 = %.6e; la deriva attesa = dcs/dLambda x (la deriva media misurata di Lambda)" % dcs_dl)
        tv = {c["t"]: c for c in vv["camp"]}
        for t in TICK_V + (n,):
            dl = float(vv["lam_media"][t - 1] - lam0.mean())
            att = dcs_dl * dl
            mis = tv[t]["cs_media"] - float(cs0.mean())
            dentro = att != 0.0 and mis * att > 0 and (1.0 / FATT_V) <= mis / att <= FATT_V
            print("    tick %5d: la deriva di Lambda %+.4e; di cs misurata %+.4e, attesa %+.4e; il rapporto %s: %s" % (t, dl, mis, att, "%.4f" % (mis / att) if att else "-", "ENTRO un fattore 2" if dentro else "### FUORI"))
        # ------------------------------------------------------------------ la base e le perturbazioni
        xs = stati[CPF.TICK_D4]

        def carica():
            with np.load(xs["file"]) as d:
                for k in chiavi:
                    st[k][...] = d[k]
            assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"
        carica()
        rho = np.zeros(inc.n)
        np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        nodi = np.arange(inc.n)
        Lt = z["L"]
        c1, c2 = TO.centro(rho, nodi // Lt, nodi % Lt, Lt)[:2]
        pos = TO.scarti(nodi // Lt, nodi % Lt, c1, c2, Lt)
        rr = np.hypot(pos[:, 0], pos[:, 1])
        ris = {}
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for pert in (0.0,) + AMPIEZZE:
                carica()
                cs0 = FP.cs(mot.densita_vuoto(st), lc, np.zeros(inc.n)).copy()
                cs0[rr < 1.0] += pert
                t1 = time.time()
                print("### la corsa %s (%d nodi perturbati), %d tick" % ("BASE" if pert == 0.0 else "perturbata %g" % pert, int(np.sum(rr < 1.0)) if pert else 0, n))
                sys.stdout.flush()
                try:
                    ris[pert] = corsa(st, mot, par, lc, cs0, n, rr, base=None if pert == 0.0 else ris[0.0]["cs"], tieni=pert == 0.0)
                except Muro as e:
                    print("  ### (s3) IL MURO: %s -- FERMO" % e)
                    print("=" * 130)
                    print("ESITO: %d/%d controlli come devono; fallite: %d %s; (s3); %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
                    return 1
                print("    %.0f s" % (time.time() - t1))
                print("    %7s %12s %10s %8s %10s %24s %16s" % ("tick", "differenza", "cs min", "raggio", "r max", "la norma", "il calore"))
                for c in ris[pert]["camp"]:
                    print("    %7d %12s %10.6f %8.2f %10.4f %24.12f %+16.6e" % (c["t"], "%.3e" % c["diff"] if c["diff"] is not None else "-", c["cs_min"], c["raggio"], c["r_max"], c["norma"], c["calore"]))
                sys.stdout.flush()
    print("-" * 130)
    livelli = {}
    for pert in AMPIEZZE:
        d = ris[pert]["diff"]
        oltre = np.flatnonzero(d > SOGLIA_LYAP)
        fine = int(oltre[0]) if len(oltre) else len(d)
        tt = np.arange(1, fine + 1)
        ok = d[:fine] > 0
        lyap = pendenza(tt[ok], np.log(d[:fine][ok])) if np.sum(ok) >= 2 else float("nan")
        u3 = ultimo_terzo(ris[pert]["camp"], n)
        p3 = 1000.0 * pendenza([c["t"] for c in u3], [math.log10(c["diff"]) for c in u3])
        livelli[pert] = (10 ** float(np.mean([math.log10(c["diff"]) for c in u3])), p3)
        print("  l'ampiezza %g: il tasso di crescita (stima di Lyapunov) dal tick 1 al %d (la differenza sotto %g): %.5f per tick (il fattore %.5f); l'ultimo terzo: il livello %.3e, la pendenza %+.4f decadi per 1000 tick"
              % (pert, fine, SOGLIA_LYAP, lyap, math.exp(lyap) if lyap == lyap else float("nan"), livelli[pert][0], p3))
    ra = livelli[AMPIEZZE[0]][0] / livelli[AMPIEZZE[1]][0]
    pmax = max(abs(v[1]) for v in livelli.values())
    if pmax < P_S1 and 1.0 / F_S1 <= ra <= F_S1:
        lett = "s1: si stabilizza (|pendenza| max %.4f), lo stesso livello per le due ampiezze (il rapporto %.3f)" % (pmax, ra)
    elif max(v[1] for v in livelli.values()) >= P_S1:
        lett = "s2: continua a crescere (la pendenza max %.4f decadi per 1000 tick)" % max(v[1] for v in livelli.values())
    else:
        lett = "fra s1 e s2: la pendenza sotto %g (%.4f) ma i livelli differiscono oltre un fattore %g (il rapporto %.3f)" % (P_S1, pmax, F_S1, ra)
    cm = ris[0.0]["camp"]
    u3 = ultimo_terzo(cm, n)
    p4 = 1000.0 * pendenza([c["t"] for c in u3], [math.log(c["cs_min"]) for c in u3])
    mn = min(c["cs_min"] for c in cm)
    if abs(p4) < P_S4:
        t4 = next(c["t"] for c in cm if c["cs_min"] <= (1.0 + F_S4) * mn)
        l4 = "s4: la discesa di cs min SI ARRESTA (la pendenza di ln nell'ultimo terzo %+.4f per 1000 tick); entro il 5%% del minimo %.6f dal tick %d" % (p4, mn, t4)
    else:
        l4 = "s4: la discesa di cs min CONTINUA: la pendenza di ln(cs min) nell'ultimo terzo %+.4f per 1000 tick (il minimo %.6f)" % (p4, mn)
    print("  LA LETTURA: (%s)" % lett)
    print("  LA LETTURA: (%s)" % l4)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %d tick; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, n, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
