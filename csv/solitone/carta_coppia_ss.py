# -*- coding: utf-8 -*-
r"""**IL REFERTO DI `C50-0` SENZA IL SINGOLO DI RIFERIMENTO** *(Luca `2026-11-11` `09:22`; il task history `doc/TASK_HISTORY/2026-11-07_referto_coppia_C35.md`, sez. `18`)*. [[PIANO-2D-3D]] [[VUOTO-SUL-FONDO]]

    python csv/solitone/carta_coppia_ss.py --corsa C50-0 > doc/referti_l2/coppia_C50-0_ss.txt

**Importa le funzioni di `carta_coppia.py` senza toccarlo.** **Della carta resta cio' che chiede solo la coppia:** `d` dai semipiani, l'angolo, il baricentro, `(M1 - M2)/M` a blocchi;
i centri del vuoto della coppia *(A-V, A-V-F)*; l'asimmetria di scambio *(A-S-I, A-S-I-F, A-S)*. **Si tolgono** *(chiedono il singolo, sez. `18.2`)*: R0, A0, A0-F, le due gobbe, la forza,
`2 |dx|` del singolo, le colonne del singolo nei centri del vuoto, C0, C0-F, `D`, la lente, i profili, C-T, C-T-F, E-0, `E_int`, FA0, la fase relativa, `oltre`.
**Si aggiunge:** U2 per terzo di corsa con `C35-0` e `C35-pi` ricalcolati accanto *(DEVE = i referti (r-b) al carattere; DEVE FALLIRE incrociato)*; **il bilancio del bordo** *(`C50-0`,
`C35-0`, `C35-pi`, `S162`)*; **le letture (c1)-(c3)** *(a `3` errori)*.
"""
import io
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_coppia as CC  # noqa: E402

ACCANTO = ("C35-0", "C35-pi")                    # ### Luca: accanto, nella stessa tabella
REF_RB = {"C35-0": "coppia_C35-0_rb.txt", "C35-pi": "coppia_C35-pi_rb.txt"}
BILANCIO = ("C50-0", "C35-0", "C35-pi", "S162")  # ### Luca: come per S162 e C35-pi
BIL_TICK = (50000, 100000, 150000, 200000)       # ### mio (sez. 18.3)
N_ERR = 3.0                                      # ### Luca: oltre 3 errori
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-110s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def distanza(corsa, s):
    """### `d` dai semipiani a ogni mappa *(come `carta_coppia.main`)*: `(tm in unita', dS, ang, bar, dM, il resto)`."""
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    rr, camp = CA.serie(corsa)[:2]
    bor = rr[0]["bordo"]
    L = CA.LCORSA[corsa]
    c0 = np.array(bor["c0"], dtype=float)
    tm, rho, lam, _cen = CC.carica_mappe(corsa)
    tm = tm * s
    n = L * L
    v = np.arange(n)
    m1, m2 = v // L, v % L
    X = TO.scarti(m1, m2, c0[0], c0[1], L)
    x = X[:, 0]
    M = camp[0]["E"]["totale"]["M"] / 2.0
    dS, ang, bar, dM, matA, matB = [], [], [], [], [], []
    for i in range(len(tm)):
        g = rho[i]
        cA, cB = CC.centri_semipiani(g, m1, m2, L, x, 0.0)
        D = CC.vettore(cA, cB, L)
        dS.append(float(np.hypot(*D)))
        ang.append(math.degrees(math.atan2(D[1], D[0])))
        pA = TO.scarti(np.array([cA[0]]), np.array([cA[1]]), c0[0], c0[1], L)[0]
        bar.append(pA + 0.5 * D)
        matA.append(pA)
        matB.append(pA + D)
        dM.append(float(g[x < 0].sum() - g[x >= 0].sum()) / M)
    return {"tm": tm, "rho": rho, "lam": lam, "dS": np.asarray(dS), "ang": np.asarray(ang), "bar": np.asarray(bar), "dM": np.asarray(dM), "matA": np.asarray(matA),
            "matB": np.asarray(matB), "X": X, "x": x, "y": X[:, 1], "c0": c0, "L": L, "bor": bor, "rr": rr, "camp": camp, "M": M}


def terzi(tm, dS, s):
    """### **Il calcolo di `carta_coppia.u2`, che RITORNA le righe** *(le stesse stringhe)*: `(righe, tab, pendenza, errore)`."""
    from solitone import stazionarieta as SZ
    tm, dS = np.asarray(tm, float), np.asarray(dS, float)
    conf = [0.0] + [k * s for k in CC.TERZI] + [tm[-1] + 1e-9]
    righe, tab = [], []
    for a, b in zip(conf[:-1], conf[1:]):
        k = (tm >= a) & (tm < b)
        x = dS[k]
        tau = float(SZ.tau_int(x)[0])
        ne = len(x) / (2.0 * max(tau, 0.5))
        sd = float(np.std(x))
        P = SZ.periodo(tm[k], x, a, b)[0]
        tab.append((float(x.mean()), sd / math.sqrt(ne), sd, sd / math.sqrt(2.0 * ne)))
        righe.append("  %8.1f .. %8.1f %5d %9.4f %9.4f %9.4f %9.4f %9.4f %9.4f %8.2f %10s" % (a, min(b, tm[-1]), len(x), x.min(), x.max(), tab[-1][0], tab[-1][1], sd, tab[-1][3], tau, "%.1f" % P if P else "-"))
    p, cov = np.polyfit(tm, dS, 1, cov=True)
    res = dS - np.polyval(p, tm)
    tr = float(SZ.tau_int(res)[0])
    ep = math.sqrt(cov[0, 0]) * math.sqrt(2.0 * max(tr, 0.5))
    righe.append("  la pendenza su tutta la corsa: %+.4e +- %.1e per unita' di tempo (%+.4f +- %.4f per 100000 tick; tau_int dei residui %.2f)" % (p[0], ep, p[0] * s * 1e5, ep * s * 1e5, tr))
    return righe, tab, float(p[0]), ep


def righe_rb(nome):
    """### **Le righe di U2 nel referto (r-b)** *(le tre dei terzi e la pendenza)*."""
    out = []
    with io.open(os.path.join(CC.DIR_REF, REF_RB[nome]), encoding="utf-8") as f:
        dentro = False
        for riga in f:
            r = riga.rstrip("\n")
            if r.startswith("### U2"):
                dentro = True
                continue
            if dentro and (re.match(r"^\s+[0-9.]+ \.\.\s+[0-9.]+\s+\d+\s", r) or r.startswith("  la pendenza su tutta la corsa")):
                out.append(r)
    return out


def main(argv):
    corsa = argv[argv.index("--corsa") + 1]
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import campo as CP
    from solitone import corsa_accensione as CA
    for m in ("__init__", "toro", "mappe", "corsa_accensione", "carta_coppia", "stazionarieta", "campo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    _sol, _vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("IL REFERTO DI %s SENZA IL SINGOLO (Luca 2026-11-11 09:22; il task history 2026-11-07_referto_coppia_C35 sez. 18): BLOCCO %g, TERZI %s tick, le letture a %g errori" % (corsa, CC.BLOCCO, CC.TERZI, N_ERR))
    print("### TOLTI (chiedono il singolo, sez. 18.2): R0; A0, A0-F; d dalle due gobbe; la forza; 2|dx| del singolo; le colonne del singolo nei centri del vuoto; C0, C0-F, D, la lente, i profili;"
          " C-T, C-T-F; E-0, E_int; FA0 e la fase relativa; oltre")
    print("=" * 130)
    Z = distanza(corsa, s)
    tm, dS, L, c0, bor = Z["tm"], Z["dS"], Z["L"], Z["c0"], Z["bor"]
    cop = Z["rr"][0]["coppia"]
    d = int(cop["d"])
    print("  la coppia: d %d, segno %+d, centro_1 %s; il bordo: c0 %s, R_A %g, g_max %g; L %d; le mappe: %d, t %.2f .. %.2f (unita')" % (d, int(cop["segno"]), cop["centro_1"], list(c0), bor["R_A"], bor["g_max"], L, len(tm), tm[0], tm[-1]))
    print("-" * 130)
    # ------------------------------------------------------------------ d(t) a blocchi (dai semipiani)
    print("### d(t) a blocchi di %g: dai semipiani (la media e la deviazione); l'angolo dell'asse; il baricentro dal punto medio; (M1 - M2)/M" % CC.BLOCCO)
    print("  %-17s %4s %-21s %-10s %-18s %-11s" % ("il tempo", "ist", "d semipiani", "angolo", "baricentro", "(M1-M2)/M"))
    for b0 in np.arange(0.0, tm[-1] + 1e-9, CC.BLOCCO):
        k = (tm >= b0) & (tm < b0 + CC.BLOCCO)
        if not k.any():
            continue
        print("  %7.0f .. %7.0f %4d %9.5f +- %8.5f %+10.4f %+8.4f %+8.4f %+11.3e" % (b0, b0 + CC.BLOCCO, k.sum(), dS[k].mean(), dS[k].std(), Z["ang"][k].mean(), Z["bar"][k, 0].mean(),
              Z["bar"][k, 1].mean(), Z["dM"][k].mean()))
    print("-" * 130)
    # ------------------------------------------------------------------ i centri del vuoto della coppia (senza le colonne del singolo)
    X, x, y = Z["X"], Z["x"], Z["y"]
    n = L * L
    m1, m2 = np.arange(n) // L, np.arange(n) % L
    _kk, rB = CP.anelli(m1, m2, c0[0], c0[1], L, float("inf"))
    ovale = rB < float(bor["R_A"])
    sA, sB = x < 0, x >= 0

    def centri_vuoto(q, msk):
        out = np.full((2, 2), np.nan)
        for j, semi in enumerate((sA, sB)):
            w = q * (msk & semi)
            sw = float(w.sum())
            if sw > 0.0:
                out[j] = (X * w[:, None]).sum(axis=0) / sw
        return out
    iA, iB, iF = (int(np.argmin(np.hypot(x - px, y))) for px in (-15.0, 15.0, -60.0))
    assert ovale[iA] and ovale[iB] and not ovale[iF], "le punte di A-V: due dentro l'ovale, una fuori"
    q = np.zeros(n)
    q[iA] = q[iB] = 1.0
    cv = centri_vuoto(q, ovale)
    eV = float(max(np.max(np.abs(cv[0] - X[iA])), np.max(np.abs(cv[1] - X[iB]))))
    esito("A-V due punte ai nodi piu' vicini a (-15, 0) e (+15, 0): i centri del vuoto = le loro X entro 1e-12", eV <= 1e-12, "%.3e" % eV)
    q[iF] = 1.0
    cvF = centri_vuoto(q, np.ones(n, dtype=bool))
    eVF = float(np.max(np.abs(cvF[0] - X[iA])))
    esito("A-V-F con una terza punta fuori dall'ovale e SENZA la maschera: il centro = la punta dentro entro 1e-12", eVF <= 1e-12, "%.3e" % eVF, deve=False)
    lam = Z["lam"]
    dL = lam - lam[0]
    vp, vn = (np.full((len(tm), 2, 2), np.nan) for _ in range(2))
    for i in range(1, len(tm)):
        vp[i] = centri_vuoto(np.maximum(dL[i], 0.0), ovale)
        vn[i] = centri_vuoto(np.maximum(-dL[i], 0.0), ovale)
    dvp = np.hypot(*(vp[:, 1] - vp[:, 0]).T)
    matA, matB = Z["matA"], Z["matB"]
    print("### i centri del vuoto disturbato della coppia: dentro l'ovale r < R_A = %g (%d nodi), per semipiano; x lungo l'asse dal punto medio, a blocchi di %g: la media e [il minimo, il massimo]" % (bor["R_A"], int(ovale.sum()), CC.BLOCCO))
    print("  %-17s %-27s %-27s %-27s %-27s %-8s" % ("il tempo", "mat x A", "mat x B", "v+ x A", "v+ x B", "d v+"))
    for b0 in np.arange(0.0, tm[-1] + 1e-9, CC.BLOCCO):
        k = (tm >= b0) & (tm < b0 + CC.BLOCCO) & (tm > 0)
        if not k.any():
            continue

        def col(a):
            return "%+8.3f [%+8.3f %+8.3f]" % (np.mean(a), np.min(a), np.max(a))
        print("  %7.0f .. %7.0f %s %s %s %s %8.3f   v- x A %+8.3f  v- x B %+8.3f" % (b0, b0 + CC.BLOCCO, col(matA[k, 0]), col(matB[k, 0]), col(vp[k, 0, 0]), col(vp[k, 1, 0]), dvp[k].mean(),
              vn[k, 0, 0].mean(), vn[k, 1, 0].mean()))
    print("-" * 130)
    # ------------------------------------------------------------------ A-S
    rho = Z["rho"]
    g0 = rho[0].reshape(L, L)
    g0n = CC.senza_nyquist(g0)
    eI = float(np.max(np.abs(CC.r180(CC.r180(g0n, L, c0[0], c0[1]), L, c0[0], c0[1]) - g0n)) / np.max(np.abs(g0n)))
    eIF = float(np.max(np.abs(CC.r180(CC.r180(g0, L, c0[0], c0[1]), L, c0[0], c0[1]) - g0)) / np.max(np.abs(g0)))
    esito("A-S-I R180 due volte attorno al punto medio = l'identita' sul campo SENZA Nyquist, entro 1e-10 del massimo", eI <= 1e-10, "%.3e" % eI)
    esito("A-S-I-F lo stesso sul campo intero (con Nyquist): entro 1e-10", eIF <= 1e-10, "%.3e" % eIF, deve=False)
    asy = np.array([float(np.linalg.norm(CC.senza_nyquist(rho[i].reshape(L, L)) - CC.r180(CC.senza_nyquist(rho[i].reshape(L, L)), L, c0[0], c0[1])) / np.linalg.norm(CC.senza_nyquist(rho[i].reshape(L, L)))) for i in range(len(tm))])
    lg = np.log(asy)
    pend = [CC.pendenza(tm[(tm >= t0) & (tm <= t0 + CC.FIN_AS)], lg[(tm >= t0) & (tm <= t0 + CC.FIN_AS)]) for t0 in tm if t0 + CC.FIN_AS <= tm[-1]]
    jm = int(np.argmax(pend))
    print("  l'asimmetria di scambio |rho - R180 rho| / |rho| attorno al punto medio: a t 0 %.4e, alla fine %.4e; il massimo %.4e a t %.1f" % (asy[0], asy[-1], asy.max(), tm[int(np.argmax(asy))]))
    esito("A-S la pendenza di log(asimmetria) su finestre di %g non supera 1/TAU_CAOS = %.4e" % (CC.FIN_AS, 1.0 / CC.TAU_CAOS), max(pend) <= 1.0 / CC.TAU_CAOS, "il massimo %.4e alla finestra da t %.1f" % (max(pend), tm[jm]))
    for b0 in np.arange(0.0, tm[-1] + 1e-9, 2 * CC.BLOCCO * 10):
        k = (tm >= b0) & (tm < b0 + 2 * CC.BLOCCO * 10)
        print("  %7.0f .. %7.0f  l'asimmetria media %.4e" % (b0, b0 + 2 * CC.BLOCCO * 10, asy[k].mean()))
    print("-" * 130)
    # ------------------------------------------------------------------ U2: C50-0, e accanto C35-0, C35-pi ricalcolati
    print("### U2: la distanza d dai SEMIPIANI per terzo di corsa (i confini %s tick); l'ampiezza = la deviazione standard; gli errori con N_eff = N / (2 tau_int) di Sokal" % (CC.TERZI,))
    print("  %-19s %5s %9s %9s %9s %9s %9s %9s %8s %10s" % ("il terzo (unita')", "N", "min", "max", "media", "+-", "ampiezza", "+-", "tau_int", "periodo"))
    righe, tab, p, ep = terzi(tm, dS, s)
    tutte = {corsa: (righe, tab, p, ep)}
    print("  %s (d iniziale %d):" % (corsa, d))
    for r in righe:
        print(r)
    for nome in ACCANTO:
        Zc = distanza(nome, s)
        rc, tc, pc, epc = terzi(Zc["tm"], Zc["dS"], s)
        tutte[nome] = (rc, tc, pc, epc)
        print("  %s (ricalcolato dalle sue mappe; d iniziale %d):" % (nome, int(Zc["rr"][0]["coppia"]["d"])))
        for r in rc:
            print(r)
        del Zc
    for nome in ACCANTO:
        ref = righe_rb(nome)
        esito("%s: le righe di U2 ricalcolate = quelle del referto (r-b) %s, al carattere (%d righe)" % (nome, REF_RB[nome], len(ref)), ref == tutte[nome][0], "")
    esito("il controllo sa dire di no: le righe di %s contro il referto (r-b) di %s" % ACCANTO, righe_rb(ACCANTO[1]) == tutte[ACCANTO[0]][0], "", deve=False)
    print("-" * 130)
    # ------------------------------------------------------------------ il bilancio del bordo
    print("### IL BILANCIO DEL BORDO: assorbiti (cumulativi, dal campo bordo dei jsonl alla fine del pezzo), relativi a M0, V0, E0")
    print("  %-8s %8s %12s %12s %12s %10s %10s %10s" % ("la corsa", "il tick", "M_ass", "V_ass", "E_ass", "M_ass/M0", "V_ass/V0", "E_ass/E0"))
    for nome in BILANCIO:
        rr = CA.serie(nome)[0]
        per_t1 = {int(r["t1"]): r["bordo"] for r in rr}
        for tk in BIL_TICK:
            b = per_t1.get(tk)
            if b is None:
                print("  %-8s %8d %12s" % (nome, tk, "-"))
                continue
            print("  %-8s %8d %12.6e %12.6e %12.6e %10.3e %10.3e %10.3e" % (nome, tk, b["M_ass"], b["V_ass"], b["E_ass"], b["M_ass"] / b["M0"], b["V_ass"] / b["V0"], b["E_ass"] / b["E0"]))
    print("-" * 130)
    # ------------------------------------------------------------------ le letture
    (m1_, e1, a1, ea1), (m2_, e2, a2, ea2), (m3_, e3, a3, ea3) = tab
    lim_m = N_ERR * math.hypot(e1, e3)
    lim_a = N_ERR * math.hypot(ea1, ea3)
    print("  %s: le medie %.4f +- %.4f, %.4f +- %.4f, %.4f +- %.4f; le ampiezze %.4f +- %.4f, %.4f +- %.4f, %.4f +- %.4f; la pendenza %+.4e +- %.1e per unita'" % (
        corsa, m1_, e1, m2_, e2, m3_, e3, a1, ea1, a2, ea2, a3, ea3, p, ep))
    print("  m3 - m1 = %+.4f (3 errori %.4f); a3 - a1 = %+.4f (3 errori %.4f); |p| / ep = %.2f" % (m3_ - m1_, lim_m, a3 - a1, lim_a, abs(p) / ep))
    if m3_ - m1_ > lim_m:
        print("  LA LETTURA: (c2) la coppia si ALLONTANA: la media cresce oltre 3 errori")
    elif m1_ - m3_ > lim_m:
        print("  LA LETTURA: (c3) la coppia si AVVICINA: la media scende oltre 3 errori")
    elif abs(p) <= N_ERR * ep and a3 - a1 <= lim_a:
        print("  LA LETTURA: (c1) la coppia resta LEGATA: nessuna tendenza oltre 3 errori, l'ampiezza limitata")
    else:
        print("  LA LETTURA: caso intermedio (ne' c2 ne' c3; la pendenza a %.2f errori, a3 - a1 %+.4f contro %.4f)" % (abs(p) / ep, a3 - a1, lim_a))
    print("  ACCANTO (qualitativo, senza estrapolare): %s" % "; ".join("%s le medie %.2f, %.2f, %.2f, le ampiezze %.2f, %.2f, %.2f, la pendenza %+.2f per 100000 tick" % (
        nome, t_[1][0][0], t_[1][1][0], t_[1][2][0], t_[1][0][2], t_[1][1][2], t_[1][2][2], t_[2] * s * 1e5) for nome, t_ in tutte.items()))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
