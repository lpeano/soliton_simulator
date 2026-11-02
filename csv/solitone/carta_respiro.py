# -*- coding: utf-8 -*-
r"""**IL SOLITONE VESTITO: LA CARTA COMPLETATA COL RESPIRO** *(il mandato di Luca del `2026-11-02` dopo `25614c34`, punto `3`; l'errore del guardiano `n.90`;
il task history `doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`, sez. `6-bis`)*: ### **`Omega` dalla serie DENSA del cuore di BG-F-0.15 vivo** *((W1) dalla partenza,
(W2) dalla fine della corsa viva a `10000`)*; ### **le bande laterali `n (mu + k Omega)` contro le bande del vuoto; le uscite miste (L) e (C) con `A`, `B`, `P0`, `Ppi`;**
### **quale uscita e' aperta, e la sua quota contro l'alone.**

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
    from solitone import vuoto as VU
    sol, vuoto, s = V.CORSE[NOME]
    banda_sol = sol[0]
    testa, camp, _dd, _rr = V.serie(NOME)
    P = 2.0 * math.pi / s
    print("=" * 130)
    print("IL SOLITONE VESTITO: LA CARTA COMPLETATA COL RESPIRO (Luca, dopo 25614c34, punto 3; l'errore del guardiano n.90): Omega dal cuore denso, le bande laterali, le uscite miste (L) e (C)")
    print("  la configurazione: %s (%s, il vuoto %s, s %g, eps %g, N %.0e, L %d, la forma della tabella, cs spento); TICK_W1 %d TICK_W2 %d ARMONICHE %s LATERALI %s NETTO %g CAMBI_REL %g TRATTO_QUOTA %s ORDINE_QUOTA %g; PERIODI_MIN %d"
          % (NOME, sol, vuoto, s, V.EPS, V.N, V.L, TICK_W1, TICK_W2, ARMONICHE, LATERALI, NETTO, CAMBI_REL, TRATTO_QUOTA, ORDINE_QUOTA, RE.PERIODI_MIN))
    print("  il periodo delle frequenze 2 pi/s = %.6f; mu %+.12f; la banda del solitone %s" % (P, testa["info"]["mu"], banda_sol))
    print("  LE LETTURE, SCRITTE PRIMA: (r1) nessuna uscita aperta; (r2) un'uscita (C) aperta col respiro e quota compatibile; (r3) aperta, quota incompatibile; (r4) solo (L) aperta: decide Luca; (r5) altro")
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
        t1, fl1, ww1 = RE.serie_densa(z, 0, TICK_W1, w_in, h)
    finally:
        cm.__exit__(None, None, None)
    rif = {c["t"]: c["f_liscia"] for c in camp}
    conf = [(t, f) for t, f in zip(t1.tolist(), fl1.tolist()) if t % V.OGNI == 0]
    uguali = all(rif[t] == f for t, f in conf)
    print("### (W1) dalla partenza, %d tick (%.0f s)" % (TICK_W1, time.time() - s0))
    esito("DEVE PASSARE: (W1) la scena e' quella della corsa (mu, w_in) e il cuore denso a t %% %d == 0 = i campioni committati di _vuoto_vivo_B AL BIT" % V.OGNI,
          ok_sc and uguali and len(conf) == TICK_W1 // V.OGNI, "%d confronti; max|diff| %.1e" % (len(conf), max(abs(rif[t] - f) for t, f in conf)))
    r1 = RE.omega(fl1, s)
    stampa_omega("(W1)", r1, s)
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
        t2, fl2, ww2 = RE.serie_densa(z, t_end, t_end + TICK_W2, w_in2, h2)
    finally:
        cm.__exit__(None, None, None)
    print("### (W2) dalla fine della corsa viva (tick %d, tempo %.0f), %d tick (%.0f s)" % (t_end, t_end * s, TICK_W2, time.time() - s0))
    esito("DEVE PASSARE: (W2) lo stato di partenza = la fine dell'ultimo pezzo committato di _respiro_sul_fondo (t1 e gli sha, ogni chiave)", ok2, "t %d" % t_end)
    r2 = RE.omega(fl2, s)
    stampa_omega("(W2)", r2, s)
    # ------------------------------------------------------------------ Omega
    print("-" * 130)
    n1, n2 = netto(r1), netto(r2)
    Om = r1["picchi"][0]["Omega"]
    T1 = r1["picchi"][0]["periodo"]
    ok_netto = esito("DEVE PASSARE: (W1) il primo picco supera di %g volte il primo picco non armonico (Omega definito; altrimenti FERMO)" % NETTO, n1 >= NETTO, "rapporto %.2f; (W2) %.2f" % (n1, n2))
    c1 = r1["cambi"]["periodo"]
    esito("PUO' FALLIRE: (W1) il periodo dai cambi di segno entro %g del picco" % CAMBI_REL, c1 is not None and abs(c1 / T1 - 1.0) <= CAMBI_REL, "picco %.6f, cambi %s" % (T1, ("%.6f" % c1) if c1 else "--"))
    alias = sorted(1.0 / abs(1.0 / T1 + k / (V.OGNI * s)) for k in (-2, -1, 1, 2))
    print("  Omega della carta (W1) = %.6f (periodo %.6f); (W2) %.6f (periodo %.6f); ogni %d tick (%.1f) il periodo %.4f avrebbe gli alias %s"
          % (Om, T1, r2["picchi"][0]["Omega"], r2["picchi"][0]["periodo"], V.OGNI, V.OGNI * s, T1, " ".join("%.4f" % a for a in alias)))
    if not ok_netto:
        print("### FERMO: Omega non e' definito (nessun picco netto); la carta non prosegue")
        print("=" * 130)
        print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
        return 1
    # ------------------------------------------------------------------ le bande della materia, il vuoto
    print("### LE BANDE (in assoluto, mod 2 pi/s = %.6f)" % P)
    print("  la materia (uscite.spettro_scena, la scena di BG-F-0.15): %s" % "; ".join("%s [%.6f, %.6f]" % (g, a, b) for g, (a, b) in sp.items()))
    print("  il vuoto (test_vuoto): %s; nu di F0 %.9f" % ("; ".join("[%.6f, %.6f]" % iv for iv in vac), nu_F0))
    aperte = []
    # ------------------------------------------------------------------ le bande laterali sul vuoto
    print("### LE BANDE LATERALI CONTRO LE BANDE DEL VUOTO (il margine: la distanza dal bordo piu' vicino, NEGATIVO se dentro)")
    print("  (L) n (mu + k Omega):")
    for n_ in ARMONICHE:
        riga = []
        for k in LATERALI:
            d, m, jj = VU.margine(n_ * (mu + k * Om), taglio, inter, s)
            riga.append("k %+d %+.4f%s" % (k, m, "#" if d else ""))
            if d:
                aperte.append(("(L) vuoto, n %d k %+d" % (n_, k), m, None))
        print("    n %d: %s" % (n_, "  ".join(riga)))
    print("  (C) nu_F0 + k Omega (cio' che rho porta nel vuoto; k 0 e' F0 stesso, sul bordo per costruzione):")
    riga = []
    for k in LATERALI:
        if k == 0:
            continue
        d, m, jj = VU.margine(nu_F0 + k * Om, taglio, inter, s)
        riga.append("k %+d %+.4f%s" % (k, m, ("# bande %s" % jj) if d else ""))
        if d:
            aperte.append(("(C) vuoto, k %+d" % k, m, None))
    print("    %s" % "  ".join(riga))
    # ------------------------------------------------------------------ le uscite miste
    print("### LE USCITE MISTE: un'onda del vuoto (le 6 bande) piu' un'onda di materia (A, B, P0, Ppi); il margine piu' aperto sulle 6 bande del vuoto; '#' aperta, '*' per costruzione")
    print("  (L) nu_v + E_m contro n mu + k Omega;  (C+) E_m + (nu_v - nu_F0);  (C-) E_m - (nu_v - nu_F0)")
    for forma in ("L", "C+", "C-"):
        for g, Em in sp.items():
            riga = []
            for n_ in ARMONICHE:
                for k in LATERALI:
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
                    m, d, j, costr = best
                    riga.append("%d%+d %+.3f%s" % (n_, k, m, "*" if costr else "#" if d else ""))
                    if d and not costr:
                        aperte.append(("(%s) %s, n %d k %+d, la banda del vuoto %d" % (forma, g, n_, k, j), m, g))
            print("  (%-2s) %-3s %s" % (forma, g, " ".join(riga)))
    # ------------------------------------------------------------------ quale e' aperta, la quota
    print("-" * 130)
    print("### LE USCITE APERTE (escluse quelle per costruzione): %d" % len(aperte))
    for che, m, g in sorted(aperte, key=lambda a: a[1]):
        print("    %-70s dentro di %.4f" % (che, -m))
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
    for che, m, g in sorted(aperte, key=lambda a: a[1]):
        if g is None:
            v = "non misurabile da D (un'uscita del vuoto da solo: D e' materia)"
        elif pq[g] >= p_al:
            v = "COMPATIBILE (il gruppo cresce almeno quanto l'alone)"
        elif pq[g] < ORDINE_QUOTA * p_al:
            v = "INCOMPATIBILE (sotto un ordine di grandezza)"
        else:
            v = "fra le due (entro un ordine di grandezza, sotto l'alone)"
        print("    %-70s la quota: %s" % (che, v))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len([f for f in FALLITE if f.startswith("DEVE")]), FALLITE))
    return 0 if all(not f.startswith("DEVE") for f in FALLITE) else 1


if __name__ == "__main__":
    sys.exit(main())
