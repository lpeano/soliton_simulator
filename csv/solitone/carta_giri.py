# -*- coding: utf-8 -*-
r"""**LA CARTA DEI DUE GIRI** *(Luca `17:30`, la condizione delle `18:05`, le aggiunte delle `18:12` e `18:18`; il task history
`doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`, sez. `13`, `13-bis`, `13-ter`)*: ### **`TP1000` (da `0` a `16000`, i pezzi interi del repo) piu' `DG1000` (la versione rada
del repo), il centro periodico srotolato.**

    python csv/solitone/carta_giri.py > doc/referti_l2/due_giri.txt      # (scrive anche doc/referti_l2/due_giri/traiettoria.png)

### **I DEVE:** `A3`, `A4`, il disco, **la rada dall'intera** *(lo `sha1` dell'intera su `E:`, i campioni comuni uguali al bit)*, **le riprese al bit** *(`corsa_accensione.ripartenza`; solo gli stati INTERMEDI, Luca dopo `fabce56d`)*; `A3` da `accensione.a3`. ### **`Lambda` vicino senza il solitone** *(n.98)*.
### **Le misure:** la fermata; a blocchi di `1000` la posizione, la velocita', la direzione, la curvatura, il raggio, il verso, `w`, il cuore, l'alone; il raggio contro la
velocita'; i passaggi dal punto di partenza; la velocita' lungo il giro e il primo giro contro il secondo; il libro attorno al centro ai passaggi e a meta' giro *(`18:12`)*;
`Lambda` e `rho` al punto di partenza dalle mappe; l'alone verso un tetto *(`18:18`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))

import solitone  # noqa: E402,F401  (i percorsi)

GIRO = 81.0                    # ### un giro lungo A1: il periodo del toro (L A1, lungo L)
FINESTRA_P = 1000.0            # ### Luca 18:12: da 1000 prima a 1000 dopo ogni passaggio
PRIMA_MAPPA = 500.0            # ### "poco prima di ogni passaggio": l'istantanea piu' vicina a t_p - 500 (dichiarato, sez. 13-bis)
BINS_GIRO = 9                  # ### la velocita' lungo il giro: 9 tratti di 9 nodi (dichiarato)
TOLL_TP = 1e-10                # ### A3
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def pendenza(x, y):
    return float(np.polyfit(x, y, 1)[0]) if len(x) >= 3 else float("nan")


def rade():
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    d = CA.RADA["DG1000"]
    nn = sorted(n for n in os.listdir(d) if n.startswith("DG1000_") and n.endswith(".jsonl")) if os.path.isdir(d) else []
    rr = [V.LP.leggi(os.path.join(d, n)) for n in nn]
    for a, b in zip(rr, rr[1:]):
        assert a["t1"] == b["t0"], "un buco fra i pezzi radi"
    return rr


def main(argv):
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import corsa_accensione as CA
    from solitone import mappe as MP
    from solitone import toro as TO
    for m in ("__init__", "toro", "mappe", "accensione", "corsa_accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    s = V.CORSE[CA.NOME][2]
    B = CA.BLOCCO
    A1, A2 = TO.vettori()
    print("=" * 130)
    print("LA CARTA DEI DUE GIRI (Luca 17:30, 18:05, 18:12, 18:18): TP1000 (0 .. 16000, i pezzi interi) + DG1000 (la versione rada, un campione ogni %d tick), il centro periodico" % CA.OGNI_RADA)
    print("  le letture di Luca, scritte prima: (r1) ripassa senza cambiare; (r2) la propria scia lo frena o lo devia; (r3) la velocita' dipende dalla posizione lungo il giro e si ripete;")
    print("  (r4) si scioglie prima; (r5) altro. GIRO %g FINESTRA_P %g PRIMA_MAPPA %g BINS_GIRO %d" % (GIRO, FINESTRA_P, PRIMA_MAPPA, BINS_GIRO))
    print("=" * 130)
    # ------------------------------------------------------------------ i DEVE
    rp, cp, _d, _a = CA.serie("TP1000")
    rd = rade()
    if not rd:
        print("### DG1000: NESSUN PEZZO RADO")
        return
    cd = [c for r in rd for c in r["campioni"]]
    ult = rd[-1]
    fermata = ult.get("fermata")
    fatta = ult["t1"] >= ult["t_fine"] or bool(fermata)
    print("### DG1000: %d pezzi, %d campioni radi, fino a %.2f; %s" % (len(rd), len(cd), ult["t1"] * s, ("LA FERMATA: " + fermata) if fermata else
                                                                       ("(c) IL TETTO t %g" % (ult["t_fine"] * s) if ult["t1"] >= ult["t_fine"] else "### NON FINITA")))
    esito("DEVE PASSARE: DG1000 finita (una delle tre)", fatta, "")
    M_ = np.array([c["E"]["totale"]["M"] for c in cp + cd])
    V_ = np.array([c["E"]["totale"]["V"] for c in cp + cd])
    t3 = np.array([c["t"] for c in cp + cd]) * s
    oM, nM = AC.a3(t3, M_, cd[-1]["t"], TOLL_TP)
    oV, nV = AC.a3(t3, V_, cd[-1]["t"], TOLL_TP)
    esito("DEVE PASSARE: A3 TP1000 + DG1000 M e V (accensione.a3, Luca dopo fabce56d)", oM and oV, "M %s; V %s" % (nM, nV))
    esito("DEVE PASSARE: A4 il libro col par della corsa", all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rd), "")
    disco = rd[0].get("disco")
    esito("DEVE PASSARE: il disco prima di cominciare (%d volte la stima)" % MP.VOLTE_SPAZIO, bool(disco) and disco["ok"], disco["nota"] if disco else "nessuna registrazione")
    cattive, n_com = [], 0
    for r in rd:
        f = r["intera"]["file"]
        if not os.path.exists(f) or MP.sha1(f) != r["intera"]["sha1"]:
            cattive.append(r["t0"])
            continue
        ri = V.LP.leggi(f)
        ci = [c for c in ri["campioni"] if c["t"] % CA.OGNI_RADA == 0]
        di = [d for d in ri["D"] if d["t"] % CA.OGNI_RADA == 0]
        if ci != r["campioni"] or di != r["D"] or ri["sha_fine"] != r["sha_fine"]:
            cattive.append(r["t0"])
        n_com += len(ci)
    esito("DEVE PASSARE: la versione rada si ricava dall'intera (lo sha1 dell'intera su E:, i campioni e le righe di D comuni uguali AL BIT, lo sha_fine)", not cattive,
          "%d campioni comuni; pezzi diversi %s" % (n_com, cattive or "nessuno"))
    rip_tutti = CA.ripartenza("DG1000")
    rip = [x for x in rip_tutti if x[0] < ult["t1"]]       # ### Luca dopo fabce56d: solo gli stati intermedi (l'ultimo tick non ha i 100 dopo, n.97)
    print("  gli stati salvati %s; il controllo delle riprese solo sugli intermedi (Luca dopo fabce56d): %s; l'ultimo tick %d, letto %s"
          % ([x[0] for x in rip_tutti], [x[0] for x in rip], ult["t1"], "; ".join("al bit" if a else "### NO" for t_, a, _b in rip_tutti if t_ >= ult["t1"]) or "nessuno stato"))
    esito("DEVE PASSARE: ogni stato INTERMEDIO salvato si rilegge AL BIT e ripartendo per %d tick ridà AL BIT lo stato della corsa" % CA.DOPO_STATO, all(a and b for _t, a, b in rip),
          "; ".join("tick %d: letto %s, dopo %s" % (t, "al bit" if a else "### NO", "al bit" if b else "### NO") for t, a, b in rip) or "nessuno stato (la corsa finita prima)")
    # ------------------------------------------------------------------ la traiettoria
    camp = cp + cd
    L = rp[0]["L"]
    tt = np.array([c["t"] for c in camp]) * s
    per = [c["per"] for c in camp]
    c1 = np.array([p["c1"] for p in per])
    c2 = np.array([p["c2"] for p in per])
    u1 = np.concatenate([[0.0], np.cumsum(((np.diff(c1) + 0.5 * L) % L) - 0.5 * L)])
    u2 = np.concatenate([[0.0], np.cumsum(((np.diff(c2) + 0.5 * L) % L) - 0.5 * L)])
    X = u1[:, None] * A1 + u2[:, None] * A2
    cam = np.hypot(X[:, 0], X[:, 1])
    ww = np.array([p["w"] for p in per])
    fl = np.array([p["f_liscia"] for p in per])
    al = np.array([p["alone"] for p in per])
    print("### A BLOCCHI DI %g (TP1000 fino a 16000, poi DG1000 rado; v per 1000 unita' di tempo; l'angolo dall'asse x; la curvatura fra blocchi consecutivi, kappa = d theta [rad] / ds)" % B)
    print("    %-17s %-18s %-8s %-11s %-8s %-8s %-11s %-9s %-9s %-9s %-10s" % ("il tempo", "la posizione", "cammino", "|v|", "angolo", "d theta", "kappa", "raggio", "w", "cuore", "alone"))
    bl = []
    a = 0.0
    while a <= tt[-1]:
        m = (tt >= a) & (tt < a + B)
        if m.sum() >= 3:
            vx, vy = 1000 * pendenza(tt[m], X[m, 0]), 1000 * pendenza(tt[m], X[m, 1])
            bl.append({"a": a, "m": m, "P": X[m].mean(axis=0), "v": math.hypot(vx, vy), "ang": math.degrees(math.atan2(vy, vx)), "w": float(ww[m].mean()), "fl": float(fl[m].mean()),
                       "al": float(al[m].mean()), "cam": float(cam[m].mean()), "pal": 1000 * pendenza(tt[m], al[m])})
        a += B
    for b0, b1 in zip([None] + bl[:-1], bl):
        if b0 is None:
            dth, k = float("nan"), float("nan")
        else:
            dth = ((b1["ang"] - b0["ang"] + 180.0) % 360.0) - 180.0
            ds = float(np.hypot(*(b1["P"] - b0["P"])))
            k = math.radians(dth) / ds if ds > 0 else float("nan")
        b1["k"] = k
        print("    %7.0f .. %7.0f (%8.2f, %7.2f) %-8.2f %-11.4e %+-8.1f %+-8.2f %+-11.4e %-9.2f %-9.4f %-9.5f %-10.5f %s"
              % (b1["a"], b1["a"] + B, b1["P"][0], b1["P"][1], b1["cam"], b1["v"], b1["ang"], dth, k, 1.0 / abs(k) if k == k and k != 0 else float("inf"), b1["w"], b1["fl"], b1["al"],
                 "" if dth != dth else ("antiorario" if dth > 0 else "orario")))
    vv = np.array([b["v"] for b in bl[1:]])
    rr_ = np.array([1.0 / abs(b["k"]) if b["k"] == b["k"] and b["k"] != 0 else np.nan for b in bl[1:]])
    ok = np.isfinite(rr_) & (vv > 2.0)
    if ok.sum() >= 3:
        print("  IL RAGGIO CONTRO LA VELOCITA' (i blocchi con |v| > 2 per 1000, dichiarato: sotto, la direzione e' il tremolio): la retta di ln raggio contro ln |v|: la pendenza %+.3f (%d blocchi)"
              % (pendenza(np.log(vv[ok]), np.log(rr_[ok])), int(ok.sum())))
    # ------------------------------------------------------------------ i passaggi
    x0 = (per[0]["x"], per[0]["y"])
    dist0 = np.array([TO.distanza((p["x"], p["y"]), x0, L) for p in per])
    print("### I PASSAGGI DAL PUNTO DI PARTENZA (il centro periodico a meno di 3 w dalla posizione iniziale; per ogni giro k, nel tratto di cammino [81 k - 40.5, 81 k + 40.5], il minimo della distanza)")
    passaggi = []
    for k in (1, 2):
        m = (cam >= GIRO * k - 0.5 * GIRO) & (cam < GIRO * k + 0.5 * GIRO)
        if not m.any():
            print("  il giro %d: non ci arriva (il cammino massimo %.2f)" % (k, cam.max()))
            continue
        i = np.nonzero(m)[0][int(np.argmin(dist0[m]))]
        dentro = dist0[i] < 3.0 * ww[i]
        passaggi.append((k, i))
        prima = (tt >= tt[i] - 500.0) & (tt < tt[i])
        dopo = (tt > tt[i]) & (tt <= tt[i] + 500.0)
        def vel(mm):
            return (1000 * pendenza(tt[mm], X[mm, 0]), 1000 * pendenza(tt[mm], X[mm, 1]))
        vp, vd = vel(prima), vel(dopo)
        print("  il giro %d: a tempo %.1f la distanza minima %.3f (3 w %.2f: %s); il cammino %.2f; |v| prima %.4e (angolo %+.1f), dopo %.4e (angolo %+.1f); w %.4f, il cuore %.5f, l'alone %.5f"
              % (k, tt[i], dist0[i], 3 * ww[i], "DENTRO" if dentro else "### FUORI", cam[i], math.hypot(*vp), math.degrees(math.atan2(vp[1], vp[0])), math.hypot(*vd),
                 math.degrees(math.atan2(vd[1], vd[0])), ww[i], fl[i], al[i]))
    # ------------------------------------------------------------------ la velocita' lungo il giro
    print("### LA VELOCITA' LUNGO IL GIRO (il cammino modulo %g in %d tratti; |v| medio per tratto, dalla retta del cammino contro il tempo; il primo giro contro il secondo)" % (GIRO, BINS_GIRO))
    for k in (0, 1):
        riga = []
        for j in range(BINS_GIRO):
            lo, hi = GIRO * k + GIRO * j / BINS_GIRO, GIRO * k + GIRO * (j + 1) / BINS_GIRO
            m = (cam >= lo) & (cam < hi)
            riga.append("%5.1f..%5.1f %s" % (lo, hi, ("%.3e" % (1000 * pendenza(tt[m], cam[m]))) if m.sum() >= 3 else "--"))
        print("  il giro %d: %s" % (k + 1, "; ".join(riga)))
    # ------------------------------------------------------------------ 18:12 il libro attorno al centro
    print("### RIPRENDE ENERGIA AL PUNTO DI PARTENZA? (Luca 18:12) il libro col par attorno al centro periodico (E_cen: il vicino a R_VICINO w_in, solo nei campioni di DG1000)")
    tE = np.array([c["t"] for c in cd]) * s
    cE = [c["per"].get("E_cen") for c in cd]
    def finestra(tc, che):
        m = np.array([(abs(t - tc) <= FINESTRA_P) and (e is not None) for t, e in zip(tE, cE)])
        if m.sum() < 3:
            print("  %s a %.1f: la finestra non c'e' nei campioni con E_cen" % (che, tc))
            return
        sel = [e for e, k in zip(cE, m) if k]
        tsel = tE[m]
        parti = []
        for conto in ("M", "leg", "vuo", "tot"):
            y = np.array([e["vicino"][conto] for e in sel])
            parti.append("%s %+.4e (dalla %+.4e alla %+.4e; la retta %+.4e per 1000)" % (conto, y[-1] - y[0], y[0], y[-1], 1000 * pendenza(tsel, y)))
        print("  %s a %.1f (%d campioni): il vicino, la variazione: %s" % (che, tc, int(m.sum()), "; ".join(parti)))
    for k, i in passaggi:
        finestra(tt[i], "il passaggio del giro %d" % k)
    for k in (1, 2):
        m = cam >= GIRO * (k - 1) + 0.5 * GIRO
        if not m.any():
            continue
        tm = tt[int(np.argmax(m))]
        if len(tE) and tm >= tE[0]:
            finestra(tm, "il confronto: meta' del giro %d (il cammino %.1f)" % (k, GIRO * (k - 1) + 0.5 * GIRO))
        else:
            print("  il confronto: meta' del giro %d a %.1f: prima di DG1000, senza E_cen" % (k, tm))
    # ------------------------------------------------------------------ 18:12 le mappe al punto di partenza
    print("### LAMBDA E RHO AL PUNTO DI PARTENZA DALLE MAPPE (l'istantanea piu' vicina a t_p - %g; il disco di raggio 3 w0 attorno alla posizione iniziale SENZA i nodi entro 3 w" % PRIMA_MAPPA)
    print("    dal centro del solitone (Luca dopo fabce56d, n.98), contro il lontano: fuori da quel disco e fuori da 3 w attorno al centro del solitone)")
    mm_, _ss, _cc = CA.file_e("DG1000")
    for k, i in passaggi:
        tv = tt[i] - PRIMA_MAPPA
        trovata = None
        for f in mm_:
            d = MP.leggi(f)
            j = int(np.argmin(np.abs(d["t"] * s - tv)))
            if trovata is None or abs(d["t"][j] * s - tv) < abs(trovata[1]["t"][trovata[2]] * s - tv):
                trovata = (f, d, j)
        if trovata is None:
            print("  il giro %d: nessuna mappa" % k)
            continue
        _f, d, j = trovata
        m1 = d["d1"].astype(float) + L // 2
        m2 = d["d2"].astype(float) + L // 2
        w0 = rp[0]["campioni"][0]["w"]
        pos = TO.posizioni(m1.astype(int), m2.astype(int), L)
        d0 = np.array([TO.distanza(q, x0, L) for q in pos])
        dc = np.array([TO.distanza(q, d["centro"][j], L) for q in pos])
        wj = ww[int(np.argmin(np.abs(tt - d["t"][j] * s)))]
        disco = d0 <= 3.0 * w0
        vic = disco & (dc > 3.0 * wj)
        lon = (~disco) & (dc > 3.0 * wj)
        lam, rho = d["Lambda"][j].astype(np.float64), d["rho"][j].astype(np.float64)
        print("  il giro %d: il disco vicino %d nodi (3 w0 %.2f), di cui entro 3 w dal centro (3 w %.2f) %d, liberi %d; il nodo del disco piu' lontano dal centro a %.2f"
              % (k, int(disco.sum()), 3.0 * w0, 3.0 * wj, int((disco & ~vic).sum()), int(vic.sum()), float(dc[disco].max())))
        if not vic.any():
            print("  il giro %d: ### NESSUN NODO DEL DISCO VICINO E' LIBERO DAL SOLITONE: da questa istantanea la domanda non ha risposta" % k)
            continue
        print("  il giro %d: l'istantanea a %.1f (il centro a %.2f dal punto di partenza): Lambda vicino %.6f, lontano %.6f (il rapporto %.6f); rho vicino %.4e, lontano %.4e; %d e %d nodi"
              % (k, d["t"][j] * s, TO.distanza(d["centro"][j], x0, L), lam[vic].mean(), lam[lon].mean(), lam[vic].mean() / lam[lon].mean(), rho[vic].mean(), rho[lon].mean(), int(vic.sum()), int(lon.sum())))
    # ------------------------------------------------------------------ 18:18 l'alone verso un tetto
    print("### L'ALONE VERSO UN TETTO? (Luca 18:18) la pendenza a blocchi; la retta contro a(t) = a_tetto (1 - e^{-(t - t0)/tau}), dopo T_acc; i residui")
    T_acc = CA.CORSE["TP1000"][0]
    m = tt >= T_acc
    print("  le pendenze per blocco (per 1000): %s" % "; ".join("%g %.3e" % (b["a"], b["pal"]) for b in bl))
    cl = np.polyfit(tt[m], al[m], 1)
    rl = float(np.sqrt(np.mean((np.polyval(cl, tt[m]) - al[m]) ** 2)))
    print("  LA RETTA: %.4e + %.4e t (per 1000: %.4e); il residuo quadratico medio %.4e" % (cl[1], cl[0], 1000 * cl[0], rl))
    try:
        from scipy.optimize import curve_fit

        def f(t, at, t0, tau):
            return at * (1.0 - np.exp(-(t - t0) / tau))
        p0 = (2.0 * al[m][-1], tt[m][0], tt[m][-1])
        pe, _cov = curve_fit(f, tt[m], al[m], p0=p0, maxfev=20000)
        re = float(np.sqrt(np.mean((f(tt[m], *pe) - al[m]) ** 2)))
        print("  L'ESPONENZIALE CON TETTO (scipy curve_fit, i valori iniziali: a_tetto = 2 x l'ultimo alone, t0 = T_acc, tau = la fine): a_tetto %.4e, t0 %.1f, tau %.1f; il residuo %.4e"
              % (pe[0], pe[1], pe[2], re))
        print("  il rapporto dei residui (l'esponenziale / la retta): %.4f" % (re / rl))
    except Exception as e:  # noqa: BLE001
        print("  L'ESPONENZIALE CON TETTO: il fit non converge (%s)" % e)
    a3 = [(c["t"] * s, c["per"]["alone_3w"]) for c in cd if "alone_3w" in c["per"]]
    if a3:
        t3, y3 = np.array(a3).T
        print("  (i) l'alone a 3 w(t) (solo DG1000; prima di 16000 dalle mappe di TM1000, che non e' ancora girata): da %.5f a %.5f, la pendenza %+.4e per 1000; a 3 w0 nello stesso tratto %+.4e"
              % (y3[0], y3[-1], 1000 * pendenza(t3, y3), 1000 * pendenza(t3, np.array([c["per"]["alone"] for c in cd if "alone_3w" in c["per"]]))))
    print("  (ii) la pendenza dell'alone contro la velocita', per blocco: %s" % "; ".join("|v| %.2f -> %.3e" % (b["v"], b["pal"]) for b in bl))
    print("  (iii) il libro attorno al centro (DG1000), M vicino per blocco: %s" % "; ".join(
        "%g %.1f" % (b["a"], np.mean([e["vicino"]["M"] for e, t in zip(cE, tE) if e is not None and b["a"] <= t < b["a"] + B])) for b in bl if any(b["a"] <= t < b["a"] + B for t in tE)))
    # ------------------------------------------------------------------ il grafico
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 5))
        cc = np.array([[p["x"], p["y"]] for p in per])
        rombo = np.array([-0.5 * L * A1 - 0.5 * L * A2, 0.5 * L * A1 - 0.5 * L * A2, 0.5 * L * A1 + 0.5 * L * A2, -0.5 * L * A1 + 0.5 * L * A2, -0.5 * L * A1 - 0.5 * L * A2])
        ax.plot(rombo[:, 0], rombo[:, 1], color="0.6", lw=1)
        sc = ax.scatter(cc[:, 0], cc[:, 1], c=tt, s=2, cmap="viridis")
        ax.plot([x0[0]], [x0[1]], "r+", ms=12)
        ax.set_aspect("equal")
        ax.set_title("il centro periodico sul rombo del toro (TP1000 + DG1000)")
        fig.colorbar(sc, label="tempo")
        out = os.path.join(CA.RADA["DG1000"], "traiettoria.png")
        fig.savefig(out, dpi=110)
        print("### IL GRAFICO: %s" % out)
    except Exception as e:  # noqa: BLE001
        print("### IL GRAFICO: non fatto (%s)" % e)
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


if __name__ == "__main__":
    main(sys.argv[1:])
