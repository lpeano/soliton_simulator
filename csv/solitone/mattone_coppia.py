# -*- coding: utf-8 -*-
r"""**LE DUE COPPIE DI MATTONI COTTI** *(Luca `2026-11-13` `22:54`; `2026-11-14` `09:34`, B1-B4; il task history `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `8` e `15`)*.

    python csv/solitone/mattone_coppia.py --mondo GU --registro mattone-coppia-<mondo> > <scratchpad>/mattone_coppia_<mondo>.txt   (poi in doc/referti_l2/mattone/coppia_<mondo>.txt)

**Il codice di `c1740faa`** *(mai girato)* **con un argomento per il mondo** *(Luca `09:34`)*: ### **SOLO GU** *(Luca `09:38`: la coppia G e' tolta)*:
**due (MGU) COTTI, il mondo G+U** *(il caso `MGU`, `r = 1`, lo stesso `rho_c` ASSOLUTO, `e*`)*. **Il mattone cotto da `doc/referti_l2/mattone/cottura_<caso>.json`.** **Due francobolli UGUALI** *(fase `0`, spin su)* **sul vuoto fresco
di `L 162` al tick `60000`, nella scena di C35-pi** *(il suo bordo)*, **ai centri di C35-pi a `60000`** *(il nodo piu' vicino con lo spostamento multiplo di `3`; `d0` vera stampata)*. ### **La materia per
SOMMA; il vuoto per PRODOTTO** *(`phi = phi_1 x prodotto_{i>1} (phi_i / phi_F3)`)*. **Campi pieni dal tick `0`, nessuna rampa; U con Gauss** *(`A = 0`)*. **`2000` tick; `d`, i centri, il picco e la
massa per semipiano ogni `10` tick; Gauss ogni `250`; lo stato ogni `500` su E:; il tick di `mattone_cottura.Corsa`** *(i conti R-CONTI)*.
### **LA TABELLA DELLE FORZE in finestre di `250` tick** *(la prima l'assestamento)*; **B3 SU B2, LA LETTURA** *(Luca `09:38`)*: `d''` **sui tick `250`-`2000`: «G E' UNA FORZA» se positiva oltre `3` errori E almeno il `30%`
di `GUrampa`; «ERA IL COLPETTO DELL'ALLARGAMENTO» se entro `3` errori da `U_2000`; «INDECISO» altrimenti** *(i riferimenti letti dal referto dei bracci del principale)*.
### **DEVE:** **un solo francobollo: la somma e il prodotto = `mattone.incolla` AL BIT; in GU Gauss sotto `1e-10` a ogni controllo.**
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402

MONDI = {"GU": "MGU"}                   # ### Luca 09:34: un argomento per il mondo; 09:38: SOLO il mondo G+U (la coppia G tolta)
CORSA_C, T_C = "C35-pi", 60000         # ### Luca 22:54: i centri come C35-pi a 60000
N_TICK, OGNI, OGNI_STATO = 2000, CT.OGNI, 500
FIN = 250                              # ### B1: la tabella delle forze in finestre di 250 tick
ASSESTAMENTO = 250
R_MASSA = 18.8                         # ### Luca 22:54: la massa di ogni francobollo oltre 18.8 nodi (meta' di d0)
N_ERR, FORZA = 3.0, 0.30                # ### B3 su B2 (Luca 09:38): forza se oltre 3 errori e almeno il 30% di GUrampa; colpetto se entro 3 errori da U_2000
REF_BRACCI = ("8ca61a34", "doc/referti_l2/p6_bracci.txt")   # ### il referto dei bracci di P6 sul principale (15/15)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def vicino_mod3(x, src):
    """### Il nodo piu' vicino a `x` con `(nodo - src) % 3 == 0`."""
    r = int(round(x))
    return min((r - 1, r, r + 1), key=lambda c: (abs(c - x) if (c - src) % 3 == 0 else 1e9))


def riferimenti():
    """### `d''` di `(G = Grampa)`, `(U = U_2000)`, `(GU = GUrampa)` dal referto dei bracci del principale *(`git show`, non ricopiati)*."""
    testo = subprocess.check_output(["git", "show", "%s:%s" % REF_BRACCI], cwd=MT.RADICE).decode("utf-8")
    out = {}
    for b, chi in (("G", "Grampa"), ("U", "U_2000"), ("GU", "GUrampa")):
        m = re.search(r"\(%s\s*= %s\s*\) ([+-][0-9.e+-]+) \+- ([0-9.e+-]+)" % (b, chi), testo)
        out[b] = (float(m.group(1)), float(m.group(2)))
    return out


def main(argv):
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    for m in ("mattone", "mattone_cottura", "conti", "p6_bracci", "p6_u_breve", "carta_coppia"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--mondo", required=True, choices=sorted(MONDI))
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    mondo, caso = x.mondo, MONDI[x.mondo]
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO if caso == "MGU" else 0.0
    ref = riferimenti()
    with open(os.path.join(MT.DIR_REF, "cottura_%s.json" % caso), encoding="utf-8") as fh:
        ct = json.load(fh)
    assert ct["cotto"], "il mattone %s NON e' cotto" % caso
    f81 = ct["file"]
    t_m = MT.T_BASE + int(ct["k"])
    print("=" * 130)
    print("LA COPPIA %s (Luca 09:34, B%d): due (%s) COTTI da %s (k %d) sul vuoto di L 162 al tick %d (la scena di %s); campi pieni dal tick 0; rho_c %.6f, e %.7e; %d tick"
          % (mondo, 2, caso, f81, ct["k"], T_C, CORSA_C, rho_c, e, N_TICK))
    print("    i riferimenti (%s:%s): (GU = GUrampa) d'' %+.6e +- %.1e; (U = U_2000) %+.6e +- %.1e; (G = Grampa) %+.6e +- %.1e  -- d_X - d_0, NON omogenei col d'' crudo della coppia: il SEGNO e l'ORDINE"
          % (REF_BRACCI[0], REF_BRACCI[1], ref["GU"][0], ref["GU"][1], ref["U"][0], ref["U"][1], ref["G"][0], ref["G"][1]))
    print("=" * 130)
    # ---------------------------------------------------------------- il francobollo
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z81:
        with np.load(f81) as d:
            Z81["metti"]({k: d[k] for k in Z81["chiavi"]})
        rho81 = MT.rho_di(Z81)
        c81 = MT.centro_di(Z81, rho81)
        picco_mattone = float(rho81.max())
        st81 = {k: Z81["st"][k].copy() for k in Z81["chiavi"]}
        MT.vuoto_fresco(Z81, t_m)
        phi_rif81 = Z81["st"]["phi_h"].copy()
        Z81["metti"](st81)
        fr = MT.ritaglia(Z81, c81, phi_rif81)
    serie_m = np.load(os.path.join(MT.DIR_REF, "cottura_%s_serie.npz" % caso))
    ult = serie_m["k"] > serie_m["k"][-1] - CT.PEZZO
    picchi_m = serie_m["rmax"][ult]
    m_fuori = float(np.sum(np.abs(fr["psi"][fr["r"] > R_MASSA]) ** 2 * fr["w"][fr["r"] > R_MASSA].reshape(-1, 1, 1) ** 2))
    m_tot = float(np.sum(np.abs(fr["psi"]) ** 2 * fr["w"].reshape(-1, 1, 1) ** 2))
    print("### il francobollo: R_t %.1f; %d nodi; il picco del mattone a k %d %.4e (nell'ultimo pezzo da %.4e a %.4e); la massa del francobollo %.6e, oltre %.1f nodi %.6e (%.3e relativo)"
          % (fr["R_t"], len(fr["w"]), ct["k"], picco_mattone, picchi_m.min(), picchi_m.max(), m_tot, R_MASSA, m_fuori, m_fuori / m_tot))
    with MT.scena(CORSA_C, T_C) as Z:
        st, L = Z["st"], Z["L"]
        bor = Z["bordo"]
        xs = TO.scarti(Z["m1"], Z["m2"], bor["c0"][0], bor["c0"][1], L)[:, 0]
        cA, cB = CC.centri_semipiani(MT.rho_di(Z), Z["m1"], Z["m2"], L, xs, 0.0)
        d_c = float(np.hypot(*CC.vettore(cA, cB, L)))
        centri = [[vicino_mod3(c[i], fr["centro"][i]) for i in (0, 1)] for c in (cA, cB)]
        d0_nodi = float(np.hypot(*CC.vettore(np.array(centri[0], dtype=float), np.array(centri[1], dtype=float), L)))
        print("### i centri di %s a %d: A (%.4f, %.4f), B (%.4f, %.4f), d %.6f; i nodi (multipli di 3 dal centro del francobollo): %s, la loro distanza %.6f"
              % (CORSA_C, T_C, cA[0], cA[1], cB[0], cB[1], d_c, centri, d0_nodi))
        MT.vuoto_fresco(Z, T_C)
        phi_F3 = st["phi_h"].copy()
        vuoto = {k: st[k].copy() for k in Z["chiavi"]}
        E_v = MT.energia(Z)

        def da_vuoto():
            for k in Z["chiavi"]:
                st[k][...] = vuoto[k]
        # ---------------------------------------------------------------- ogni francobollo da solo (S6)
        soli, Delte = [], []
        for c in centri:
            da_vuoto()
            Delte.append(MT.incolla(Z, fr, c, True))
            soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
        # ---------------------------------------------------------------- il DEVE: un solo francobollo

        def somma(psis):
            out = psis[0].copy()
            for q in psis[1:]:
                out = out + q
            return out

        def prodotto(phis):
            out = phis[0].copy()
            for q in phis[1:]:
                out = out * (q / phi_F3)
            return out
        psi1, phi1 = somma([soli[0][0]]), prodotto([soli[0][1]])
        div = [k for k, a, b in (("psi", psi1, soli[0][0]), ("phi", phi1, soli[0][1])) if not np.array_equal(a, b)]
        esito("(%s) un solo francobollo: la somma e il prodotto = l'incollatura di S6 AL BIT" % mondo, not div, "diverse: %s" % div, True)
        # ---------------------------------------------------------------- la coppia
        st["psi_h"][...] = somma([s_[0] for s_ in soli])                # ### la materia per SOMMA (il vuoto ha psi = 0)
        st["phi_h"][...] = prodotto([s_[1] for s_ in soli])             # ### il vuoto per PRODOTTO, dalla prima incollatura
        E_c = MT.energia(Z)
        nodo = Z["nodo"]
        dA = np.hypot(*TO.scarti(Z["m1"], Z["m2"], centri[0][0], centri[0][1], L).T[:2])
        dB = np.hypot(*TO.scarti(Z["m1"], Z["m2"], centri[1][0], centri[1][1], L).T[:2])
        lontano = (dA > fr["R_t"] + MT.RACCORDO) & (dB > fr["R_t"] + MT.RACCORDO)
        p2 = np.zeros((Z["n"], 6))
        righe6 = np.arange(6 * Z["n"])
        np.add.at(p2, (nodo, 2 * ((righe6 // 2) % 3) + righe6 % 2), np.abs(st["phi_h"]) ** 2)     # ### come p6_bracci.phi2_di
        print("### la coppia incollata: Delta %s; E(coppia) - E(vuoto) %.6e; |phi_j|^2 lontano (fuori da R_t + %g dai due centri, %d nodi): la mediana %.12f, il minimo %.12f, il massimo %.12f"
              % (["%.6f" % dd for dd in Delte], E_c - E_v, MT.RACCORDO, int(lontano.sum()), float(np.median(p2[lontano])) if lontano.any() else float("nan"),
                 float(p2[lontano].min()) if lontano.any() else float("nan"), float(p2[lontano].max()) if lontano.any() else float("nan")))
        # ---------------------------------------------------------------- i campi pieni
        C = MT.Campi(Z, caso, rho_c, MT.PB.E_DECISO)
        g0 = 0.0
        if C.campo is not None:
            rho = MT.rho_di(Z)
            C.campo.A[...] = 0.0
            C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
            C.campo.e = e
            C.e_prec = e
            g0 = C.residuo()
            print("### il campo di Gauss (A = 0): il residuo iniziale %.3e" % g0)
        R = CT.Corsa(Z, C)
        S = {k: [] for k in ("t", "d", "cA1", "cA2", "cB1", "cB2", "pA", "pB", "mA", "mB", "gauss")}

        def misura(k):
            rho = MT.rho_di(Z)
            a, b = CC.centri_semipiani(rho, Z["m1"], Z["m2"], L, xs, 0.0)
            m = xs < 0.0
            S["t"].append(k)
            S["d"].append(float(np.hypot(*CC.vettore(a, b, L))))
            S["cA1"].append(a[0])
            S["cA2"].append(a[1])
            S["cB1"].append(b[0])
            S["cB2"].append(b[1])
            S["pA"].append(float(rho[m].max()))
            S["pB"].append(float(rho[~m].max()))
            S["mA"].append(float(rho[m].sum()))
            S["mB"].append(float(rho[~m].sum()))
            S["gauss"].append(C.residuo() if (k % MT.OGNI_GAUSS == 0 and C.campo is not None) else float("nan"))
            R.etichette([a, b])
        misura(0)
        print("### d0 VERA (dai semipiani, sullo stato incollato): %.6f" % S["d"][0])
        R.inizio(0)
        t1 = t_tappa = time.time()
        fermo = None
        for k in range(1, N_TICK + 1):
            R.passo(k, T_C + k, 1.0, e)
            if k % OGNI == 0:
                misura(k)
                if k % 250 == 0:
                    print("    k %5d  d %.6f  A (%.3f, %.3f) picco %.4e massa %.6e  B (%.3f, %.3f) picco %.4e massa %.6e  Gauss %s  (%.0f s)" % (
                        k, S["d"][-1], S["cA1"][-1], S["cA2"][-1], S["pA"][-1], S["mA"][-1], S["cB1"][-1], S["cB2"][-1], S["pB"][-1], S["mB"][-1],
                        "%.2e" % S["gauss"][-1] if S["gauss"][-1] == S["gauss"][-1] else "--", time.time() - t1))
                    sys.stdout.flush()
            if k % OGNI_STATO == 0:
                f = os.path.join(MT.DIR_E, "coppia%s_%05d.npz" % (mondo, k))
                dati = {kk: st[kk] for kk in Z["chiavi"]}
                if C.campo is not None:
                    dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
                np.savez(f, meta=np.array(json.dumps({"mondo": mondo, "k": k, "t": T_C + k, "sha": V.shas(Z["z"]), "codice": "csv/solitone/mattone_coppia.py"})), **dati)
            adesso = time.time()
            if adesso - t_tappa >= MT.TAPPA_S:
                mem = MT.memoria_gb()
                MT.tappa(x.registro, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / k, mem))
                t_tappa = adesso
                if mem < MT.MEM_MIN_GB:
                    fermo = "la memoria libera %.2f GB sotto %g GB a k %d" % (mem, MT.MEM_MIN_GB, k)
            if adesso - t1 > MT.TETTO_S:
                fermo = "il tetto di %g s a k %d" % (MT.TETTO_S, k)
            if fermo:
                print("### FERMO: %s" % fermo)
                break
        print("-" * 130)
        print("### %d tick in %.0f s" % (int(S["t"][-1]), time.time() - t1))
        R.tabella(["A", "B"])
    os.makedirs(MT.DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(MT.DIR_REF, "coppia_%s_serie.npz" % mondo), **{k: np.array(v) for k, v in S.items()})
    tt, dd = np.array(S["t"], dtype=float), np.array(S["d"])
    g = np.array(S["gauss"])
    g = g[g == g]
    # ---------------------------------------------------------------- la tabella delle forze (R-CONTI-2, finestre di 250: il mandato)
    print("### LA TABELLA DELLE FORZE (finestre di %d tick; la prima l'ASSESTAMENTO): d, la velocita' relativa d' e l'accelerazione relativa d'' (la parabola)" % FIN)
    for a in range(0, N_TICK, FIN):
        ii = (tt >= a) & (tt <= a + FIN)
        if ii.sum() >= 4:
            acc, ea = CC.curvatura(tt[ii], dd[ii])
            vel = CC.pendenza(tt[ii], dd[ii])
            print("    tick %4d-%4d: d da %.6f a %.6f; d' %+.4e; d'' %+.6e +- %.1e (%.1f errori)%s" % (a, a + FIN, dd[ii][0], dd[ii][-1], vel, acc, ea, abs(acc) / ea if ea else float("inf"),
                                                                                       "   (l'ASSESTAMENTO)" if a < ASSESTAMENTO else ""))
    ii = (tt >= ASSESTAMENTO) & (tt <= N_TICK)
    a_c, ea_c = CC.curvatura(tt[ii], dd[ii])
    aGU, (aU, eU) = ref["GU"][0], ref["U"]
    eU_c = (ea_c ** 2 + eU ** 2) ** 0.5            # ### l'errore della differenza da U_2000: in quadratura (mio, dichiarato)
    if a_c > N_ERR * ea_c and a_c >= FORZA * aGU:
        lett = "G E' UNA FORZA"
    elif abs(a_c - aU) <= N_ERR * eU_c:
        lett = "ERA IL COLPETTO DELL'ALLARGAMENTO"
    else:
        lett = "INDECISO"
    print("-" * 130)
    print("### B3 SU B2, LA LETTURA (Luca 09:38): d'' sui tick %d-%d %+.6e +- %.1e (%.1f errori); contro GUrampa %+.6e: %.3f (la soglia %g); da U_2000 %+.6e: %+.3e, %.1f errori (in quadratura; la soglia %g)"
          % (ASSESTAMENTO, N_TICK, a_c, ea_c, abs(a_c) / ea_c if ea_c else float("inf"), aGU, a_c / aGU, FORZA, aU, a_c - aU, abs(a_c - aU) / eU_c if eU_c else float("inf"), N_ERR))
    print("  LA LETTURA: %s" % lett)
    pA, pB = np.array(S["pA"]), np.array(S["pB"])
    print("### IL PICCO: A da %.4e a %.4e (min %.4e, max %.4e); B da %.4e a %.4e (min %.4e, max %.4e); il mattone nell'ultimo pezzo della cottura: da %.4e a %.4e"
          % (pA[0], pA[-1], pA.min(), pA.max(), pB[0], pB[-1], pB.min(), pB.max(), picchi_m.min(), picchi_m.max()))
    print("### LA MASSA: A da %.6e a %.6e, B da %.6e a %.6e" % (S["mA"][0], S["mA"][-1], S["mB"][0], S["mB"][-1]))
    if C.campo is not None:
        esito("il residuo di Gauss sotto %g a ogni controllo (ogni %d tick)" % (MT.TOLL_GAUSS, MT.OGNI_GAUSS), len(g) > 0 and float(g.max()) < MT.TOLL_GAUSS and g0 < MT.TOLL_GAUSS,
              "il massimo %.3e (l'iniziale %.3e)" % (float(g.max()) if len(g) else float("nan"), g0), True)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; la lettura %s; %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, lett, "FERMO " + fermo if fermo else "finita", time.time() - t00))
    return 0 if (not FALLITE and not fermo) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
