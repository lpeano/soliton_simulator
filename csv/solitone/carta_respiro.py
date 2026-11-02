# -*- coding: utf-8 -*-
r"""**IL SOLITONE VESTITO: LA CARTA COMPLETATA COL RESPIRO** *(il mandato di Luca del `2026-11-02` dopo `25614c34`, punto `3`; l'errore del guardiano `n.90`;
il task history `doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`, sez. `6-bis`)*: ### **`Omega` dalla serie DENSA del cuore di BG-F-0.15 vivo** *((W1) dalla partenza,
(W2) dalla fine della corsa viva a `10000`)*; ### **le bande laterali `n (mu + k Omega)` contro le bande del vuoto; le uscite miste (L) e (C) con `A`, `B`, `P0`, `Ppi`;**
### **quale uscita e' aperta, e la sua quota contro l'alone.**

### **La decisione di Luca (a) dopo `04b02794`** *(sez. `8`)*: ### **niente `Omega` unico** -- il DEVE del picco netto resta scritto com'e' e fallisce; ### **le tabelle per OGNI picco**
*(i primi `PRIMI`, piu' quelli fino a `FRAZIONE` del primo)*, le miste a `k = 0` una volta, la lettura del guardiano. ### **L'aggiunta delle `09:20`** *(sez. `8-bis`)*:
### **di che modo e' ogni picco** *(il cuore, `w`, il baricentro, `Q2`, `Q3`, `Lambda` medio; la significativita')*.

    python csv/solitone/carta_respiro.py > doc/referti_l2/solitone_vestito_carta_respiro.txt
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

NOME = "BG-F-0.15"
TICK_W1 = 4000                 # ### (W1): 600 unita' di tempo dalla partenza (task history, sez. 6-bis)
TICK_W2 = 2000                 # ### (W2): 300 unita' di tempo dalla fine della corsa viva
ARMONICHE = (1, 2)             # ### n (il mandato)
LATERALI = (-3, -2, -1, 0, 1, 2, 3)   # ### k (il mandato)
NETTO = 3.0                    # ### il primo picco supera di 3 volte il secondo (fuori dalle sue armoniche), o Omega non e' definito: FERMO (task history)
CAMBI_REL = 0.05               # ### il periodo dai cambi entro il 5% del picco: un controllo, non un FERMO (task history)
TRATTO_QUOTA = (5000.0, 10000.0)   # ### la quota: le pendenze sul tratto della crescita (task history, sez. 6-bis, passo 6)
ORDINE_QUOTA = 0.1             # ### incompatibile se la pendenza del gruppo e' sotto un ordine di grandezza quella dell'alone (task history)
PRIMI = 5                      # ### i 5 picchi gia' trovati di ogni finestra (Luca, dopo 04b02794)
FRAZIONE = 0.1                 # ### piu' quelli fino a 1/10 dell'ampiezza del primo (Luca, dopo 04b02794)
SIGNIF = 3.0                   # ### un picco c'e' in un osservabile se la significativita' arriva a 3; la classe: la QUOTA piu' alta fra quelli dove c'e'; nessuno: "nessuna" (sez. 8-bis e l'annotazione)
OSSERVABILI = (("cuore", "il respiro"), ("w", "il respiro"), ("x", "lo spostamento"), ("y", "lo spostamento"),
               ("Q2 re", "la deformazione"), ("Q2 im", "la deformazione"), ("Q3 re", "la deformazione"), ("Q3 im", "la deformazione"),
               ("Lambda", "lo scambio col vuoto"))   # ### (il nome, la classe) (sez. 8-bis)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scena_pronta(V, MI, US, sol, vuoto, s):
    """### **La scena di `_vuoto_vivo_B.corsa`:** `w_in`, `h`, lo spettro della materia *(dalla scena, prima della partenza)*, la partenza; ### **la scena rimessa.**"""
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    cm = V.scena(s, vuoto, V.EPS)
    rec, z, phi0, pK = cm.__enter__()
    with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
        w_in = DC.forma(z, rec["larghezza"])[0]
    h = MI.lunghezza_arco(z)
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    sp = US.spettro_scena(z, phi0, s)
    p0, info = V.partenza(sol, z, phi0, pK, s)
    for k, v in salvato.items():
        z["st"][k][...] = v
    return cm, z, phi0, w_in, h, sp, p0, info


def stampa_omega(che, r, s):
    from solitone import respiro as RE
    print("  %s: la finestra %.1f unita' di tempo, il canale %.3e; i picchi (almeno %d periodi nella finestra), per ampiezza:" % (che, r["finestra"], r["canale"], RE.PERIODI_MIN))
    f1 = r["picchi"][0]["frequenza"]
    for p in r["picchi"]:
        k = RE.armonica_di(p["frequenza"], f1, r["canale"]) if p is not r["picchi"][0] else None
        print("    periodo %.6f  Omega %.6f  ampiezza %.4e%s" % (p["periodo"], p["Omega"], p["ampiezza"], ("  (armonica %d del primo)" % k) if k else ""))
    c = r["cambi"]
    print("    i cambi di segno (col passo %g): %d cambi, il periodo %s; Nyquist %.3f" % (s, c["cambi"], ("%.6f" % c["periodo"]) if c["periodo"] else "--", c["nyquist"]))


def netto(r):
    from solitone import respiro as RE
    pp = r["picchi"]
    f1 = pp[0]["frequenza"]
    altri = [p for p in pp[1:] if RE.armonica_di(p["frequenza"], f1, r["canale"]) is None]
    return (pp[0]["ampiezza"] / altri[0]["ampiezza"]) if altri else float("inf")


def pendenza(x, y):
    return float(np.polyfit(x, y, 1)[0])


def margine_vuoto(x, vac, P):
    """### **`(dentro, margine, banda)`** di `x` dalle bande del vuoto *(`respiro.margine_mod`, il minimo sulle bande)*."""
    from solitone import respiro as RE
    return min((RE.margine_mod(x, iv, P) + (j,) for j, iv in enumerate(vac)), key=lambda a: a[1])


def riga_mista(forma, Em, n_, k, Om, mu, vac, nu_F0, P, g, banda_sol):
    """### **Un'uscita mista** *(un'onda del vuoto piu' un'onda di materia `Em`)*: ### **`(margine, dentro, banda del vuoto, per costruzione)`**, il piu' aperto sulle bande del vuoto."""
    from solitone import respiro as RE
    from solitone import test_vuoto
    x = n_ * mu + k * Om
    best = None
    for j, iv in enumerate(vac):
        if forma == "L":
            S = RE.somma(iv, Em)
            zero = 0.0
        else:
            rel = (iv[0] - nu_F0, iv[1] - nu_F0)
            S = RE.somma(Em, rel if forma == "C+" else RE.opposto(rel))
            zero = nu_F0
        d, m = RE.margine_mod(x, S, P)
        cz = RE.margine_mod(zero, iv, P)
        costr = n_ == 1 and k == 0 and g == banda_sol and (cz[0] or cz[1] <= test_vuoto.TOLL_BORDO)
        if best is None or m < best[0]:
            best = (m, d, j, costr)
    return best


def main():
    import _presidio
    for m in ("__init__", "misure", "uscite", "protetto", "vuoto", "test_vuoto", "respiro", "test_respiro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    import _respiro_congelato as RC
    import _respiro_sul_fondo as RS
    import _vuoto_vivo_B as V
    from solitone import misure as MI
    from solitone import respiro as RE
    from solitone import test_respiro
    from solitone import test_vuoto
    from solitone import uscite as US
    sol, vuoto, s = V.CORSE[NOME]
    banda_sol = sol[0]
    testa, camp, _dd, _rr = V.serie(NOME)
    P = 2.0 * math.pi / s
    print("=" * 130)
    print("IL SOLITONE VESTITO: LA CARTA COMPLETATA COL RESPIRO (Luca, dopo 25614c34, punto 3; l'errore del guardiano n.90), CON LA DECISIONE DI LUCA (a) DOPO 04b02794 E L'AGGIUNTA DELLE 09:20")
    print("  la configurazione: %s (%s, il vuoto %s, s %g, eps %g, N %.0e, L %d, la forma della tabella, cs spento); TICK_W1 %d TICK_W2 %d ARMONICHE %s LATERALI %s NETTO %g CAMBI_REL %g TRATTO_QUOTA %s ORDINE_QUOTA %g; PERIODI_MIN %d"
          % (NOME, sol, vuoto, s, V.EPS, V.N, V.L, TICK_W1, TICK_W2, ARMONICHE, LATERALI, NETTO, CAMBI_REL, TRATTO_QUOTA, ORDINE_QUOTA, RE.PERIODI_MIN))
    print("  la decisione (a) e l'aggiunta: PRIMI %d FRAZIONE %g SIGNIF %g; gli osservabili %s" % (PRIMI, FRAZIONE, SIGNIF, " ".join("%s (%s)" % (o, c) for o, c in OSSERVABILI)))
    print("  il periodo delle frequenze 2 pi/s = %.6f; mu %+.12f; la banda del solitone %s" % (P, testa["info"]["mu"], banda_sol))
    print("  LE LETTURE, SCRITTE PRIMA: (r1) nessuna uscita aperta; (r2) un'uscita (C) aperta col respiro e quota compatibile; (r3) aperta, quota incompatibile; (r4) solo (L) aperta: decide Luca; (r5) altro")
    print("  E DOPO 04b02794 (sez. 8, 8-bis): (p1) mu - Omega dei picchi veloci di (W1) nella banda del vuoto; (p2) no; (p3) una mista aperta a k 0; (p4) in (W2) un k +-3 dentro una banda;")
    print("    (m1) i picchi lenti nel respiro, la coppia veloce in un altro osservabile; (m2) tutti nello stesso; (m3) la coppia veloce nello scambio col vuoto; (m4) un picco 'nessuna'")
    print("  L'IPOTESI DI LUCA, scritta prima: ogni frequenza e' un modo diverso in cui il solitone tiene la sua energia; l'energia totale e' una sola (H si conserva; qui non si misura)")
    print("=" * 130)
    test_respiro.gira(esito)
    rv = test_vuoto.gira(esito)
    taglio, inter, nu_F0 = rv["taglio"], rv["inter"], rv["nu"]
    vac = [(lo + taglio, hi + taglio) for lo, hi in inter]
    print("-" * 130)
    # ------------------------------------------------------------------ (W1)
    s0 = time.time()
    cm, z, phi0, w_in, h, sp, p0, info = scena_pronta(V, MI, US, sol, vuoto, s)
    try:
        mu = info["mu"]
        ok_sc = mu == testa["info"]["mu"] and w_in == testa["w_in"]
        z["st"]["psi_h"][...] = p0
        S1 = RE.serie_modi(z, 0, TICK_W1, w_in, h)
    finally:
        cm.__exit__(None, None, None)
    rif = {c["t"]: c["f_liscia"] for c in camp}
    conf = [(t, f) for t, f in zip(S1["t"].tolist(), S1["f_liscia"].tolist()) if t % V.OGNI == 0]
    uguali = all(rif[t] == f for t, f in conf)
    print("### (W1) dalla partenza, %d tick (%.0f s)" % (TICK_W1, time.time() - s0))
    esito("DEVE PASSARE: (W1) la scena e' quella della corsa (mu, w_in) e il cuore denso a t %% %d == 0 = i campioni committati di _vuoto_vivo_B AL BIT" % V.OGNI,
          ok_sc and uguali and len(conf) == TICK_W1 // V.OGNI, "%d confronti; max|diff| %.1e" % (len(conf), max(abs(rif[t] - f) for t, f in conf)))
    r1 = RE.omega(S1["f_liscia"], s, None)
    r1_5 = dict(r1, picchi=r1["picchi"][:PRIMI])
    stampa_omega("(W1)", r1_5, s)
    # ------------------------------------------------------------------ (W2)
    s0 = time.time()
    ult = V.LP.leggi(os.path.join(RS.DIR_JSON, RS.nomi()[-1]))
    cm, z, phi0, w_in2, h2, _sp, _p0, _info = scena_pronta(V, MI, US, sol, vuoto, s)
    try:
        with np.load(os.path.join(RS.DIR_NPZ, NOME + ".npz")) as dati:
            t_end = int(dati["t"])
            for k in z["st"]:
                if isinstance(z["st"][k], np.ndarray):
                    z["st"][k][...] = dati[k]
        ok2 = t_end == ult["t1"] and V.shas(z) == ult["sha_fine"]
        S2 = RE.serie_modi(z, t_end, t_end + TICK_W2, w_in2, h2)
    finally:
        cm.__exit__(None, None, None)
    print("### (W2) dalla fine della corsa viva (tick %d, tempo %.0f), %d tick (%.0f s)" % (t_end, t_end * s, TICK_W2, time.time() - s0))
    esito("DEVE PASSARE: (W2) lo stato di partenza = la fine dell'ultimo pezzo committato di _respiro_sul_fondo (t1 e gli sha, ogni chiave)", ok2, "t %d" % t_end)
    r2 = RE.omega(S2["f_liscia"], s, None)
    r2_5 = dict(r2, picchi=r2["picchi"][:PRIMI])
    stampa_omega("(W2)", r2_5, s)
    # ------------------------------------------------------------------ Omega
    print("-" * 130)
    n1, n2 = netto(r1_5), netto(r2_5)
    Om = r1["picchi"][0]["Omega"]
    T1 = r1["picchi"][0]["periodo"]
    ok_netto = esito("DEVE PASSARE: (W1) il primo picco supera di %g volte il primo picco non armonico (Omega definito; altrimenti FERMO)" % NETTO, n1 >= NETTO, "rapporto %.2f; (W2) %.2f" % (n1, n2))
    c1 = r1["cambi"]["periodo"]
    esito("PUO' FALLIRE: (W1) il periodo dai cambi di segno entro %g del picco" % CAMBI_REL, c1 is not None and abs(c1 / T1 - 1.0) <= CAMBI_REL, "picco %.6f, cambi %s" % (T1, ("%.6f" % c1) if c1 else "--"))
    alias = sorted(1.0 / abs(1.0 / T1 + k / (V.OGNI * s)) for k in (-2, -1, 1, 2))
    print("  Omega della carta (W1) = %.6f (periodo %.6f); (W2) %.6f (periodo %.6f); ogni %d tick (%.1f) il periodo %.4f avrebbe gli alias %s"
          % (Om, T1, r2["picchi"][0]["Omega"], r2["picchi"][0]["periodo"], V.OGNI, V.OGNI * s, T1, " ".join("%.4f" % a for a in alias)))
    if not ok_netto:
        print("### FERMO (come in 04b02794): Omega unico non e' definito (nessun picco netto)")
        print("### LA DECISIONE DI LUCA (a), DOPO 04b02794: niente Omega unico; le tabelle per OGNI picco, nelle due finestre")
    # ------------------------------------------------------------------ i picchi delle tabelle
    el = {"(W1)": RE.elenco(r1, FRAZIONE, PRIMI), "(W2)": RE.elenco(r2, FRAZIONE, PRIMI)}
    rr = {"(W1)": r1, "(W2)": r2}
    picchi = []
    for fin in ("(W1)", "(W2)"):
        r = rr[fin]
        print("### I PICCHI DELLE TABELLE %s: i primi %d piu' quelli con ampiezza >= %g del primo (%.4e), senza doppioni entro 1 canale (%.3e); %d massimi rifiniti"
              % (fin, PRIMI, FRAZIONE, r["picchi"][0]["ampiezza"], r["canale"], len(r["picchi"])))
        for j, p in enumerate(el[fin]):
            nome = "%s.%d" % (fin[1:3], j + 1)
            picchi.append((nome, fin, p))
            print("    %-4s periodo %10.6f  Omega %9.6f  ampiezza %.4e  (il %d-esimo per altezza dello spettro)" % (nome, p["periodo"], p["Omega"], p["ampiezza"], r["picchi"].index(p) + 1))
    # ------------------------------------------------------------------ le bande
    print("-" * 130)
    print("### LE BANDE (in assoluto, mod 2 pi/s = %.6f)" % P)
    print("  la materia (uscite.spettro_scena, la scena di BG-F-0.15): %s" % "; ".join("%s [%.6f, %.6f]" % (g, a, b) for g, (a, b) in sp.items()))
    print("  il vuoto (test_vuoto): %s; nu di F0 %.9f" % ("; ".join("[%.6f, %.6f]" % iv for iv in vac), nu_F0))
    aperte = []
    # ------------------------------------------------------------------ le miste a k = 0
    print("### LE USCITE MISTE A k 0 (non dipendono da Omega): un'onda del vuoto (le bande) piu' un'onda di materia; il margine piu' aperto, NEGATIVO se dentro; '#' aperta, '*' per costruzione")
    print("  (L) nu_v + E_m contro n mu;  (C+) E_m + (nu_v - nu_F0);  (C-) E_m - (nu_v - nu_F0)")
    for forma in ("L", "C+", "C-"):
        riga = []
        for g, Em in sp.items():
            for n_ in ARMONICHE:
                m, d, j, costr = riga_mista(forma, Em, n_, 0, 0.0, mu, vac, nu_F0, P, g, banda_sol)
                riga.append("%s n%d %+.4f%s" % (g, n_, m, "*" if costr else "#" if d else ""))
                if d and not costr:
                    aperte.append(("(%s) %s, n %d k 0, la banda del vuoto %d" % (forma, g, n_, j), m, g, None))
        print("  (%-2s) %s" % (forma, "  ".join(riga)))
    dmu = margine_vuoto(mu, vac, P)
    for n_ in ARMONICHE:
        d, m, j = margine_vuoto(n_ * mu, vac, P)
        print("  n mu da solo contro le bande del vuoto (k 0, n %d): %s, margine %+.4f (la banda %d)" % (n_, "DENTRO" if d else "fuori", m, j))
        if d:
            aperte.append(("(L) vuoto, n %d k 0, la banda %d" % (n_, j), m, None, None))
    # ------------------------------------------------------------------ per ogni picco
    for nome, fin, p in picchi:
        O = p["Omega"]
        print("### IL PICCO %s %s: periodo %.6f, Omega %.6f, ampiezza %.4e" % (nome, fin, p["periodo"], O, p["ampiezza"]))
        for n_ in ARMONICHE:
            riga = []
            for k in LATERALI:
                d, m, j = margine_vuoto(n_ * (mu + k * O), vac, P)
                riga.append("k%+d %+.4f%s" % (k, m, "#" if d else ""))
                if d and k != 0:
                    aperte.append(("(L) vuoto, n %d k %+d, la banda %d" % (n_, k, j), m, None, (nome, fin, p)))
            print("    (L) n %d (mu + k Omega): %s" % (n_, "  ".join(riga)))
        riga = []
        for k in LATERALI:
            if k == 0:
                continue
            d, m, j = margine_vuoto(nu_F0 + k * O, vac, P)
            riga.append("k%+d %+.4f%s" % (k, m, "#" if d else ""))
            if d:
                aperte.append(("(C) vuoto, nu_F0 %+d Omega, la banda %d" % (k, j), m, None, (nome, fin, p)))
        print("    (C) nu_F0 + k Omega:     %s" % "  ".join(riga))
        for forma in ("L", "C+", "C-"):
            for g, Em in sp.items():
                riga = []
                for n_ in ARMONICHE:
                    for k in LATERALI:
                        if k == 0:
                            continue
                        m, d, j, costr = riga_mista(forma, Em, n_, k, O, mu, vac, nu_F0, P, g, banda_sol)
                        riga.append("%d%+d %+.3f%s" % (n_, k, m, "#" if d else ""))
                        if d:
                            aperte.append(("(%s) %s, n %d k %+d, la banda del vuoto %d" % (forma, g, n_, k, j), m, g, (nome, fin, p)))
                print("    (%-2s) %-3s %s" % (forma, g, " ".join(riga)))
    # ------------------------------------------------------------------ la lettura del guardiano
    print("-" * 130)
    print("### LA LETTURA DEL GUARDIANO (Luca dopo 04b02794, punto 2), DA VERIFICARE:")
    for nome, fin, p in picchi:
        if fin != "(W1)":
            continue
        x = float(np.mod(mu - p["Omega"], P))
        d, m, j = margine_vuoto(x, vac, P)
        print("    %-4s periodo %10.6f: mu - Omega = %.6f (mod %.6f): %s, margine %+.4f (la banda %d [%.6f, %.6f])" % (nome, p["periodo"], x, P, "DENTRO" if d else "fuori", m, j, vac[j][0], vac[j][1]))
    print("    (W2): mu da solo, margine %+.4f; per ogni picco lo spostamento 3 Omega e i margini di mu +- 3 Omega:" % dmu[1])
    for nome, fin, p in picchi:
        if fin != "(W2)":
            continue
        mp, mm = margine_vuoto(mu + 3 * p["Omega"], vac, P), margine_vuoto(mu - 3 * p["Omega"], vac, P)
        print("    %-4s periodo %10.6f: 3 Omega = %.4f; mu + 3 Omega %s %+.4f; mu - 3 Omega %s %+.4f" % (nome, p["periodo"], 3 * p["Omega"], "DENTRO" if mp[0] else "fuori", mp[1], "DENTRO" if mm[0] else "fuori", mm[1]))
    # ------------------------------------------------------------------ di che modo e' ogni picco
    print("-" * 130)
    print("### DI CHE MODO E' OGNI PICCO (l'aggiunta di Luca delle 09:20): lo spettro separato di ogni osservabile, i primi %d picchi" % PRIMI)
    SS = {"(W1)": S1, "(W2)": S2}
    serie = {}
    for fin in ("(W1)", "(W2)"):
        S = SS[fin]
        wm = float(np.mean(S["w"]))
        serie[fin] = {"cuore": (S["f_liscia"], float(np.mean(S["f_liscia"]))), "w": (S["w"], wm), "x": (S["x"], wm), "y": (S["y"], wm),
                      "Q2 re": (S["q2"].real, 1.0), "Q2 im": (S["q2"].imag, 1.0), "Q3 re": (S["q3"].real, 1.0), "Q3 im": (S["q3"].imag, 1.0),
                      "Lambda": (S["lam"], float(np.mean(S["lam"])))}
        print("  %s: le medie: cuore %.6f, w %.6f, (x, y) (%.4f, %.4f), |Q2| %.4e, |Q3| %.4e, Lambda %.6f; le escursioni (max - min): x %.3e, y %.3e"
              % (fin, serie[fin]["cuore"][1], wm, np.mean(S["x"]), np.mean(S["y"]), np.mean(np.abs(S["q2"])), np.mean(np.abs(S["q3"])), serie[fin]["Lambda"][1], np.ptp(S["x"]), np.ptp(S["y"])))
        for o, _c in OSSERVABILI:
            ro = RE.omega(serie[fin][o][0], s, PRIMI)
            print("    %-7s %s" % (o, "  ".join("%.4f (%.2e)" % (q["periodo"], q["ampiezza"] / serie[fin][o][1]) for q in ro["picchi"])))
    print("  PER OGNI PICCO DELLE TABELLE: la QUOTA (a^2/2 sulla varianza dell'osservabile tolta la tendenza, in %%) e la significativita' (l'ampiezza / la mediana dello spettro; c'e' se >= %g)" % SIGNIF)
    print("    %-4s %-10s %s %-28s" % ("", "periodo", " ".join("%-15s" % o for o, _c in OSSERVABILI), "la classe"))
    classi = {}
    for nome, fin, p in picchi:
        cel, best = [], None
        for o, c in OSSERVABILI:
            sg, a, qu = RE.presenza(serie[fin][o][0], s, p["frequenza"])
            cel.append("%5.1f%% %8.0f" % (100.0 * qu, sg))
            if sg >= SIGNIF and (best is None or qu > best[0]):
                best = (qu, o, c)
        cl = best[2] if best else "nessuna (un battimento interno)"
        classi[nome] = (cl,)
        print("    %-5s %10.6f %s %s%s" % (nome, p["periodo"], " ".join("%-15s" % x for x in cel), cl, (" (%s, %.1f%%)" % (best[1], 100.0 * best[0])) if best else ""))
    # ------------------------------------------------------------------ quale e' aperta, la quota
    print("-" * 130)
    print("### LE USCITE APERTE (escluse quelle per costruzione): %d" % len(aperte))
    cv, dv = RC.serie_viva()
    ta = np.array([c["t"] for c in cv]) * s
    al = np.array([c["alone"] for c in cv])
    ma = (ta >= TRATTO_QUOTA[0]) & (ta <= TRATTO_QUOTA[1])
    p_al = 1000.0 * pendenza(ta[ma], al[ma])
    td = np.array([d["t"] for d in dv]) * s
    md = (td >= TRATTO_QUOTA[0]) & (td <= TRATTO_QUOTA[1])
    nD2 = np.array([d["nD"] ** 2 for d in dv])
    print("### LA QUOTA (un ordine di grandezza, non una derivazione; la corsa viva committata, il tratto %g .. %g): la pendenza dell'alone %+.4e per 1000" % (TRATTO_QUOTA[0], TRATTO_QUOTA[1], p_al))
    pq = {}
    for g in sp:
        q = np.array([d["bande"][g] for d in dv]) * nD2
        pq[g] = 1000.0 * pendenza(td[md], q[md])
        print("    il gruppo %-3s: f_g |D|^2/|psi0|^2 da %.4e a %.4e, la pendenza %+.4e per 1000 (rapporto con l'alone %+.3f)" % (g, q[md][0], q[md][-1], pq[g], pq[g] / p_al))
    for che, m, g, pk in sorted(aperte, key=lambda a: a[1]):
        if g is None:
            v = "non misurabile da D (un'uscita del vuoto da solo: l'alone e D sono materia)"
        elif pq[g] >= p_al:
            v = "COMPATIBILE (il gruppo cresce almeno quanto l'alone)"
        elif pq[g] < ORDINE_QUOTA * p_al:
            v = "INCOMPATIBILE (sotto un ordine di grandezza)"
        else:
            v = "fra le due (entro un ordine di grandezza, sotto l'alone)"
        chi = "k 0: lo stato stesso, nessun picco" if pk is None else "%s %s periodo %.6f ampiezza %.4e (%s)" % (pk[0], pk[1], pk[2]["periodo"], pk[2]["ampiezza"], classi[pk[0]][0])
        print("    %-58s dentro di %.4f | %s | la quota: %s" % (che, -m, chi, v))
    print("=" * 130)
    dev = [f for f in FALLITE if f.startswith("DEVE")]
    puo = [f for f in FALLITE if not f.startswith("DEVE")]
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s; PUO' FALLIRE fallite: %d %s" % (OK[0], OK[1], len(dev), dev, len(puo), puo))
    return 0 if not dev else 1


if __name__ == "__main__":
    sys.exit(main())
