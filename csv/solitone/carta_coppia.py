# -*- coding: utf-8 -*-
r"""**IL REFERTO DELLA COPPIA** *(il piano delle corse della coppia, `2026-11-06_coppia_corse` sez. `2`; le misure di `2026-11-05_coppia_forza_e_campi` sez. `3`;
il task history `doc/TASK_HISTORY/2026-11-07_referto_coppia_C35.md`)*
    python csv/solitone/carta_coppia.py --corsa C35-0 > doc/referti_l2/coppia_C35-0.txt
    python csv/solitone/carta_coppia.py --corsa C35-pi > doc/referti_l2/coppia_C35-pi.txt
### **Solo lettura** delle mappe e degli stati su `E:` e dei jsonl nel repo, di `<corsa>` e del suo singolo di riferimento *(`RIF`: `S162` per `C35`)*; ### **il calcolo:**
`E[0]` del vuoto `c(t) F3` su `L 162` a ogni campione, e **due tick** *(`C-T`)* da uno stato di `S162`.
### **I DEVE:** `R0` *(il singolo della coppia = il riferimento)*; `A0`, `A0-F` *(i due metodi sulla coppia sintetica, entro `TOLL_A0` nodi; l'asse spostato di `SPOST_A0F`)*;
`A-V`, `A-V-F` *(i centri del vuoto disturbato: due punte esatte; senza la maschera dell'ovale una punta fuori sposta il centro)*; `A-S-I`, `A-S-I-F` *(`R180` due volte = l'identita' sul campo senza i modi di Nyquist; sul campo intero deve fallire)*, `A-S` *(la pendenza di `log` dell'asimmetria di scambio, su finestre di `FIN_AS`, sotto `1 / TAU`)*; `C0`, `C0-F` *(il difetto di
sovrapposizione sulla coppia sintetica, e con lo spostamento sbagliato di `1` nodo)*; `C-T`, `C-T-F` *(il tick commuta con la traslazione di `d`, entro `n eps`)*; `E-0` *(il libro ricalcolato a `t 0` = il campione, il controllo positivo di `E[0]`)*; `FA0`
*(la fase relativa a `t 0` = il segno della coppia, entro il limite delle code incrociate)*.
"""
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

RIF = {"C35-0": "S162", "C35-pi": "S162"}   # ### il singolo di riferimento (Luca 2026-11-06 12:42: S162 il riferimento di C35; per C50 NON c'e')
TOLL_A0 = 0.05        # ### A0 (Luca 2026-11-05 15:28, come proposta): nodi
SPOST_A0F = 5.0       # ### A0-F (come proposta): l'asse di separazione spostato di 5 nodi
TAU = 35.0            # ### A-S (Luca 2026-11-05 15:28): un e-fold ogni tau
FIN_AS = 3.0 * TAU    # ### A-S: la finestra della pendenza (MIA, dichiarata: tre tau)
TOLL_C0F = 1e-3       # ### C0-F (come proposta)
BLOCCO = 500.0        # ### le tabelle a blocchi di 500 unita' (come carta_campo)
TEMPI_PROFILI = (0.0, 3330.0, 6660.0, 9990.0)   # ### come carta_campo
CONTI = ("cin", "vuo", "leg", "cost", "tot")
DIR_REF = os.path.join(solitone.RADICE, "doc", "referti_l2")

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


def indice_mappe(corsa):
    """### **Le righe delle mappe nell'indice** `doc/referti_l2/mappe_indice_<corsa>.txt`: `[(percorso, byte, sha1)]` nell'ordine."""
    out = []
    with open(os.path.join(DIR_REF, "mappe_indice_%s.txt" % corsa), encoding="utf-8") as f:
        for riga in f:
            m = re.search(r"(E:\\soliton_simulator\\mappe\\%s\\%s_\d+\.npz)\s+(\d+) byte\s+sha1 ([0-9a-f]{40})" % (re.escape(corsa), re.escape(corsa)), riga)
            if m:
                out.append((m.group(1), int(m.group(2)), m.group(3)))
    return out


def carica_mappe(corsa):
    """### **Le mappe della corsa, concatenate** *(lo sha1 di ogni file contro l'indice: se diverso, `assert`)*."""
    from solitone import mappe as MP
    t, rho, lam, cen = [], [], [], []
    for f, _b, sha in indice_mappe(corsa):
        assert MP.sha1(f) == sha, "il file %s NON e' quello dell'indice" % f
        with np.load(f) as d:
            t.append(d["t"].copy())
            rho.append(d["rho"].astype(float))
            lam.append(d["Lambda"].astype(float))
            cen.append(d["centro"].copy())
    return np.concatenate(t), np.concatenate(rho), np.concatenate(lam), np.concatenate(cen)


def rolla(a, d, L):
    """### **La traslazione di `d` nodi lungo l'indice `1`** *(come la partenza della coppia in `corsa_accensione`: `roll` dell'asse `0` di `(L, L, -1, ...)`)*."""
    return np.roll(a.reshape((L, L, -1) + a.shape[1:]), d, axis=0).reshape(a.shape)


def fasi(L, d1, d2):
    k = np.fft.fftfreq(L)
    return np.exp(-2j * math.pi * (k[:, None] * d1 + k[None, :] * d2))


def sposta(G, L, d1, d2):
    """### **`g(m - delta)` dalla trasformata `G` di `g` su `(L, L)`** *(lo spostamento frazionario sul toro per indice; esatto per una funzione a banda limitata)*."""
    return np.fft.ifft2(G * fasi(L, d1, d2)).real


def senza_nyquist(g):
    """### **Il campo senza i modi di Nyquist** *(la riga e la colonna `L/2` della trasformata a zero; Luca `2026-11-07` `16:25`, la via (a))*: **su `L` pari lo spostamento
    frazionario rende complessi quei modi e `.real` ne butta la parte immaginaria; senza, la rotazione e' esatta all'arrotondamento.**"""
    L = g.shape[0]
    assert g.shape == (L, L) and L % 2 == 0, "senza_nyquist vuole un toro L x L con L pari"
    G = np.fft.fft2(g)
    G[L // 2, :] = 0.0
    G[:, L // 2] = 0.0
    return np.fft.ifft2(G).real


def r180(g, L, c1, c2):
    """### **`g(2 c - m)`:** la rotazione di `180` gradi attorno al punto `c` *(indici, frazionari)*: `m -> -m` e' l'inversione del reticolo triangolare."""
    gf = np.roll(g[::-1, ::-1], 1, axis=(0, 1))
    return sposta(np.fft.fft2(gf), L, 2.0 * c1, 2.0 * c2)


def centri_semipiani(rho, m1, m2, L, x, soglia):
    """### **I centri periodici dei due semipiani** *(il nodo e' del solitone `1` se il suo scarto lungo `A1` dal punto medio e' sotto `soglia`)*: `(cA, cB)` indici."""
    from solitone import toro as TO
    m = x < soglia
    cA = TO.centro(rho * m, m1, m2, L)[:2]
    cB = TO.centro(rho * ~m, m1, m2, L)[:2]
    return np.array(cA), np.array(cB)


def vettore(cA, cB, L):
    """### **Il vettore da `cA` a `cB`** *(indici)* **in coordinate cartesiane, con l'immagine piu' vicina.**"""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    q = ((np.asarray(cB) - np.asarray(cA) + 0.5 * L) % L) - 0.5 * L
    return TO.piu_vicina((q[0] * A1 + q[1] * A2)[None, :], L)[0]


def due_gobbe(rho, GS, L, x0):
    """### **L'adattamento a due gobbe:** `rho ~ S(m - a) + S(m - b)`, `S` il singolo allo stesso `t`; `a`, `b` liberi ai minimi quadrati. `(a, b, successo)`."""
    from scipy.optimize import least_squares
    g = rho.reshape(L, L)

    def res(p):
        return (g - np.fft.ifft2(GS * (fasi(L, p[0], p[1]) + fasi(L, p[2], p[3]))).real).ravel()
    r = least_squares(res, x0, method="lm", xtol=1e-12, ftol=1e-12)
    return r.x[:2], r.x[2:], bool(r.success)


def pendenza(t, y):
    A = np.vstack([t - t.mean(), np.ones_like(t)]).T
    return float(np.linalg.lstsq(A, y, rcond=None)[0][0])


def curvatura(t, y):
    """### **`d''` da una parabola ai minimi quadrati, e il suo errore standard.**"""
    tc = t - t.mean()
    A = np.vstack([tc ** 2, tc, np.ones_like(tc)]).T
    p, res, _rk, _sv = np.linalg.lstsq(A, y, rcond=None)
    dof = max(1, len(t) - 3)
    s2 = float(res[0]) / dof if len(res) else 0.0
    cov = s2 * np.linalg.inv(A.T @ A)
    return 2.0 * float(p[0]), 2.0 * math.sqrt(max(0.0, float(cov[0, 0])))


def main(argv):
    corsa = argv[argv.index("--corsa") + 1]
    if corsa not in RIF:
        raise SystemExit("### la corsa %s NON ha un singolo di riferimento col suo bordo (RIF): il referto non si fa" % corsa)
    rif = RIF[corsa]
    import _deriva_congelato as DC
    import _libro_dei_conti as LCO
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import carta_statiche as CS
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "toro", "mappe", "bordo", "accensione", "corsa_accensione", "carta_statiche"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    L = CA.LCORSA[corsa]
    assert CA.LCORSA[rif] == L
    T_acc = CA.CORSE[corsa][0]
    K = int(round(T_acc / s))
    print("=" * 130)
    print("IL REFERTO DELLA COPPIA %s contro il singolo %s (L %d; il task history 2026-11-07_referto_coppia_C35): TOLL_A0 %g SPOST_A0F %g TAU %g FIN_AS %g (mia) TOLL_C0F %g BLOCCO %g"
          % (corsa, rif, L, TOLL_A0, SPOST_A0F, TAU, FIN_AS, TOLL_C0F, BLOCCO))
    print("=" * 130)
    rrC, campC = CA.serie(corsa)[:2]
    rrS, campS = CA.serie(rif)[:2]
    cop, copS, bor = rrC[0]["coppia"], rrS[0]["coppia"], rrC[0]["bordo"]
    d, segno = int(cop["d"]), int(cop["segno"])
    c0 = np.array(bor["c0"], dtype=float)
    print("  la coppia: d %d, segno %+d, centro_1 %s, il centro del bordo %s, R_A %g, g_max %g" % (d, segno, cop["centro_1"], list(c0), bor["R_A"], bor["g_max"]))
    esito("DEVE PASSARE: R0 il singolo della coppia (sha_singolo, centro_1) = quello di %s, e il bordo lo stesso" % rif,
          cop["sha_singolo"] == copS["sha_singolo"] and cop["centro_1"] == copS["centro_1"] and bor["c0"] == rrS[0]["bordo"]["c0"] and bor["R_A"] == rrS[0]["bordo"]["R_A"],
          "sha %s, %s" % (cop["sha_singolo"][:8], copS["sha_singolo"][:8]))
    tC = np.array([c["t"] for c in campC])
    assert np.array_equal(tC, np.array([c["t"] for c in campS])), "i campioni NON sono agli stessi t"

    # ------------------------------------------------------------------ le mappe
    tm, rhoC, lamC, _cenC = carica_mappe(corsa)
    tmS, rhoS, lamS, cenS = carica_mappe(rif)
    assert np.array_equal(tm, tmS), "le mappe NON sono agli stessi t"
    # ### la cura del 2026-11-07 (il task history sez. 6, l'errore (1)): il t delle mappe e' in TICK; tutta la carta lavora in unita' di tempo (t * s)
    tm, tmS = tm * s, tmS * s
    n = L * L
    v = np.arange(n)
    m1, m2 = v // L, v % L
    X = TO.scarti(m1, m2, c0[0], c0[1], L)        # ### lo scarto cartesiano di ogni nodo dal punto medio (A1 = (1, 0): x lungo l'asse)
    x, y = X[:, 0], X[:, 1]
    A1, A2 = TO.vettori()
    print("  le mappe: %d istantanee per corsa, t %.2f .. %.2f; il semipiano del solitone 1: x < 0 dal punto medio (sul toro la seconda linea a L/2, l'immagine piu' vicina)" % (len(tm), tm[0], tm[-1]))
    print("-" * 130)

    # ------------------------------------------------------------------ A0, A0-F sulla coppia sintetica
    eS, eF, eG, nG = [], [], [], 0
    for i in range(len(tm)):
        R = rhoS[i]
        syn = R + rolla(R, d, L)
        cA, cB = centri_semipiani(syn, m1, m2, L, x, 0.0)
        eS.append(abs(np.hypot(*vettore(cA, cB, L)) - d))
        cA, cB = centri_semipiani(syn, m1, m2, L, x, SPOST_A0F)
        eF.append(abs(np.hypot(*vettore(cA, cB, L)) - d))
        if i % 33 == 0:                            # ### l'adattamento sulla sintetica, una ogni 33 istantanee (il costo)
            a, b, ok = due_gobbe(syn, np.fft.fft2(R.reshape(L, L)), L, [0.3, -0.2, d - 0.4, 0.2])
            eG.append(abs(np.hypot(*((b - a)[0] * A1 + (b - a)[1] * A2)) - d))
            nG += 0 if ok else 1
    esito("DEVE PASSARE: A0 sulla coppia sintetica (%s + la stessa traslata di %d) d dai semipiani e dalle due gobbe entro %g nodi" % (rif, d, TOLL_A0),
          max(eS) <= TOLL_A0 and max(eG) <= TOLL_A0 and nG == 0, "semipiani il peggiore %.3e su %d; due gobbe %.3e su %d (non convergenti %d)" % (max(eS), len(eS), max(eG), len(eG), nG))
    esito("DEVE FALLIRE: A0-F l'asse di separazione spostato di %g nodi: d dai semipiani entro %g" % (SPOST_A0F, TOLL_A0), not (max(eF) <= TOLL_A0), "il peggiore %.3e" % max(eF))

    # ------------------------------------------------------------------ d(t), la forza, il baricentro, l'angolo; il singolo da solo
    dS, dG, ang, bar, nonc, M1, M2 = [], [], [], [], 0, [], []
    matA, matB = [], []                         # ### i centri della materia in X dal punto medio (sez. 5)
    xa = [0.0, 0.0, float(d), 0.0]
    for i in range(len(tm)):
        g = rhoC[i]
        cA, cB = centri_semipiani(g, m1, m2, L, x, 0.0)
        D = vettore(cA, cB, L)
        dS.append(float(np.hypot(*D)))
        ang.append(math.degrees(math.atan2(D[1], D[0])))
        pA = TO.scarti(np.array([cA[0]]), np.array([cA[1]]), c0[0], c0[1], L)[0]
        bar.append(pA + 0.5 * D)
        matA.append(pA)
        matB.append(pA + D)
        a, b, ok = due_gobbe(g, np.fft.fft2(rhoS[i].reshape(L, L)), L, xa)
        nonc += 0 if ok else 1
        xa = [a[0], a[1], b[0], b[1]]
        dG.append(float(np.hypot(*((b - a)[0] * A1 + (b - a)[1] * A2))))
        M1.append(float(g[x < 0].sum()))
        M2.append(float(g[x >= 0].sum()))
    dS, dG, ang, bar, M1, M2 = map(np.asarray, (dS, dG, ang, bar, M1, M2))
    dxS = (cenS[:, 0] - cenS[0, 0])               # ### lo spostamento del singolo lungo A1 dal suo t 0 (il centro della mappa, (x, y))
    print("  l'adattamento a due gobbe: non convergenti %d su %d (FERMO sopra il 10%%: %s)" % (nonc, len(tm), "SI'" if nonc > 0.1 * len(tm) else "no"))
    M = campC[0]["E"]["totale"]["M"] / 2.0
    mu = M / 2.0
    print("### d(t) a blocchi di %g: i semipiani e le due gobbe (la media e la deviazione), d - %d contro 2 |dx| del singolo %s (cio' che il singolo fa da solo); l'angolo dell'asse;"
          " il baricentro dal punto medio; M1 - M2 relativa" % (BLOCCO, d, rif))
    print("  %-17s %4s %-21s %-21s %-12s %-10s %-18s %-11s" % ("il tempo", "ist", "d semipiani", "d due gobbe", "2|dx| sing.", "angolo", "baricentro", "(M1-M2)/M"))
    for b0 in np.arange(0.0, tm[-1] + 1e-9, BLOCCO):
        k = (tm >= b0) & (tm < b0 + BLOCCO)
        if not k.any():
            continue
        print("  %7.0f .. %7.0f %4d %9.5f +- %8.5f %9.5f +- %8.5f %12.5f %+10.4f %+8.4f %+8.4f %+11.3e"
              % (b0, b0 + BLOCCO, k.sum(), dS[k].mean(), dS[k].std(), dG[k].mean(), dG[k].std(), 2 * np.abs(dxS[k]).mean(), ang[k].mean(), bar[k, 0].mean(), bar[k, 1].mean(),
                 ((M1[k] - M2[k]) / M).mean()))
    print("### la forza lungo l'asse dopo la rampa (t >= %g): d'' da una parabola per blocco (dalle due gobbe), F = mu d'' con mu = M/2 = %.6e (M la norma di ciascuno, dichiarato)" % (T_acc, mu))
    for b0 in np.arange(T_acc, tm[-1] + 1e-9, 2 * BLOCCO):
        k = (tm >= b0) & (tm < b0 + 2 * BLOCCO)
        if k.sum() < 5:
            continue
        dd, ed = curvatura(tm[k], dG[k])
        print("  %7.0f .. %7.0f  d'' %+.4e +- %.4e  F %+.4e +- %.4e" % (b0, b0 + 2 * BLOCCO, dd, ed, mu * dd, mu * ed))
    terzo = tm >= tm[-1] * 2.0 / 3.0
    print("  (q1, la proposta, nessun verdetto) l'ultimo terzo: d - %d dalle due gobbe %+.5f, dai semipiani %+.5f; 3 volte la deviazione di 2 dx del singolo %.5f"
          % (d, dG[terzo].mean() - d, dS[terzo].mean() - d, 3 * (2 * dxS[terzo]).std()))
    print("-" * 130)

    # ------------------------------------------------------------------ i centri del vuoto disturbato (Luca 2026-11-07 10:20; il task history sez. 5)
    from solitone import campo as CP
    _kk, rB = CP.anelli(m1, m2, c0[0], c0[1], L, float("inf"))
    ovale = rB < float(bor["R_A"])                  # ### "l'ovale": la zona senza assorbimento, con la distanza del bordo (mio, dichiarato)
    sA, sB = x < 0, x >= 0

    def centri_vuoto(q, msk):
        """### `(2, 2)`: i centri in `X` di `q >= 0` pesato, sui nodi di `msk`, per semipiano (`x < 0`, `x >= 0`)."""
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
    esito("DEVE PASSARE: A-V due punte ai nodi piu' vicini a (-15, 0) e (+15, 0): i centri del vuoto = le loro X entro 1e-12", eV <= 1e-12, "%.3e" % eV)
    q[iF] = 1.0
    cvF = centri_vuoto(q, np.ones(n, dtype=bool))
    eVF = float(np.max(np.abs(cvF[0] - X[iA])))
    esito("DEVE FALLIRE: A-V-F con una terza punta fuori dall'ovale (il nodo piu' vicino a (-60, 0)) e SENZA la maschera: il centro = la punta dentro entro 1e-12", not (eVF <= 1e-12), "%.3e" % eVF)
    matA, matB = np.asarray(matA), np.asarray(matB)
    dLC_, dLS_ = lamC - lamC[0], lamS - lamS[0]
    vp, vn, vSp, vSn = (np.full((len(tm), 2, 2), np.nan) for _ in range(4))
    for i in range(1, len(tm)):
        vp[i] = centri_vuoto(np.maximum(dLC_[i], 0.0), ovale)
        vn[i] = centri_vuoto(np.maximum(-dLC_[i], 0.0), ovale)
        vSp[i] = centri_vuoto(np.maximum(dLS_[i], 0.0), ovale)
        vSn[i] = centri_vuoto(np.maximum(-dLS_[i], 0.0), ovale)
    dvp = np.hypot(*(vp[:, 1] - vp[:, 0]).T)
    print("### i centri del vuoto disturbato (sez. 5): dentro l'ovale r < R_A = %g (%d nodi), per semipiano; x lungo l'asse dal punto medio, a blocchi di %g: la media e [il minimo, il massimo]" % (bor["R_A"], int(ovale.sum()), BLOCCO))
    print("  mat = la materia (i centri dei semipiani di d(t)); v+ = dLambda > 0 (il mandato); v- = dLambda < 0 (mio); d v+ = la distanza dei due v+; %s = il singolo, semipiano x < 0 (mio)" % rif)
    print("  %-17s %-27s %-27s %-27s %-27s %-8s %-9s %-9s" % ("il tempo", "mat x A", "mat x B", "v+ x A", "v+ x B", "d v+", "%s v+" % rif, "%s v-" % rif))
    for b0 in np.arange(0.0, tm[-1] + 1e-9, BLOCCO):
        k = (tm >= b0) & (tm < b0 + BLOCCO) & (tm > 0)
        if not k.any():
            continue

        def col(a):
            return "%+8.3f [%+8.3f %+8.3f]" % (np.mean(a), np.min(a), np.max(a))
        print("  %7.0f .. %7.0f %s %s %s %s %8.3f %+9.3f %+9.3f   v- x A %+8.3f  v- x B %+8.3f"
              % (b0, b0 + BLOCCO, col(matA[k, 0]), col(matB[k, 0]), col(vp[k, 0, 0]), col(vp[k, 1, 0]), dvp[k].mean(), vSp[k, 0, 0].mean(), vSn[k, 0, 0].mean(),
                 vn[k, 0, 0].mean(), vn[k, 1, 0].mean()))
    dopo = tm >= T_acc
    print("  dopo la rampa (t >= %g), l'escursione di x (il massimo meno il minimo): mat A %.3f B %.3f; v+ A %.3f B %.3f; v- A %.3f B %.3f; %s v+ %.3f v- %.3f; nessuna soglia (le letture v1-v3)"
          % (T_acc, np.ptp(matA[dopo, 0]), np.ptp(matB[dopo, 0]), np.ptp(vp[dopo, 0, 0]), np.ptp(vp[dopo, 1, 0]), np.ptp(vn[dopo, 0, 0]), np.ptp(vn[dopo, 1, 0]),
             rif, np.ptp(vSp[dopo, 0, 0]), np.ptp(vSn[dopo, 0, 0])))
    print("-" * 130)

    # ------------------------------------------------------------------ A-S: l'asimmetria di scambio
    g0 = rhoC[0].reshape(L, L)
    g0n = senza_nyquist(g0)
    eI = float(np.max(np.abs(r180(r180(g0n, L, c0[0], c0[1]), L, c0[0], c0[1]) - g0n)) / np.max(np.abs(g0n)))
    eIF = float(np.max(np.abs(r180(r180(g0, L, c0[0], c0[1]), L, c0[0], c0[1]) - g0)) / np.max(np.abs(g0)))
    esito("DEVE PASSARE: A-S-I R180 due volte attorno al punto medio = l'identita' sul campo SENZA Nyquist, entro 1e-10 del massimo (Luca 16:25, la via (a))", eI <= 1e-10, "%.3e" % eI)
    esito("DEVE FALLIRE: A-S-I-F lo stesso sul campo intero (con Nyquist): entro 1e-10", not (eIF <= 1e-10), "%.3e" % eIF)
    peso_N = np.array([float(np.linalg.norm(rhoC[i] - senza_nyquist(rhoC[i].reshape(L, L)).reshape(-1)) / np.linalg.norm(rhoC[i])) for i in range(len(tm))])
    print("  il peso del modo di Nyquist nel campo |rho - rho_N| / |rho|: a t 0 %.4e, il massimo %.4e (la rotazione si fa sul campo senza Nyquist: dichiarato)" % (peso_N[0], peso_N.max()))
    asy = np.array([float(np.linalg.norm(senza_nyquist(rhoC[i].reshape(L, L)) - r180(senza_nyquist(rhoC[i].reshape(L, L)), L, c0[0], c0[1])) / np.linalg.norm(senza_nyquist(rhoC[i].reshape(L, L)))) for i in range(len(tm))])
    lg = np.log(asy)
    pend = [pendenza(tm[(tm >= t0) & (tm <= t0 + FIN_AS)], lg[(tm >= t0) & (tm <= t0 + FIN_AS)]) for t0 in tm if t0 + FIN_AS <= tm[-1]]
    jm = int(np.argmax(pend))
    print("  l'asimmetria di scambio |rho - R180 rho| / |rho| attorno al punto medio: a t 0 %.4e (premessa 3: NON zero), alla fine %.4e; il massimo %.4e a t %.1f"
          % (asy[0], asy[-1], asy.max(), tm[int(np.argmax(asy))]))
    esito("DEVE PASSARE: A-S la pendenza di log(asimmetria) su finestre di %g non supera 1/TAU = %.4e" % (FIN_AS, 1.0 / TAU), max(pend) <= 1.0 / TAU,
          "il massimo %.4e alla finestra da t %.1f" % (max(pend), tm[jm]))
    for b0 in np.arange(0.0, tm[-1] + 1e-9, 2 * BLOCCO):
        k = (tm >= b0) & (tm < b0 + 2 * BLOCCO)
        print("  %7.0f .. %7.0f  l'asimmetria media %.4e" % (b0, b0 + 2 * BLOCCO, asy[k].mean()))
    print("-" * 130)

    # ------------------------------------------------------------------ C0, C0-F, il difetto di sovrapposizione del vuoto, i profili, la lente
    dLC, dLS = lamC - lamC[0], lamS - lamS[0]
    i1 = len(tm) // 2
    syn = dLS[i1] + rolla(dLS[i1], d, L)
    D0 = float(np.linalg.norm(syn - (dLS[i1] + rolla(dLS[i1], d, L))) / np.linalg.norm(syn))
    D0F = float(np.linalg.norm(syn - (dLS[i1] + rolla(dLS[i1], d + 1, L))) / np.linalg.norm(syn))
    esito("DEVE PASSARE: C0 sulla coppia sintetica (dLambda di %s + la stessa traslata di %d, a t %.1f) D = 0 alla macchina" % (rif, d, tm[i1]), D0 == 0.0, "%.3e" % D0)
    esito("DEVE FALLIRE: C0-F lo spostamento sbagliato di 1 nodo: D sotto %g" % TOLL_C0F, not (D0F < TOLL_C0F), "%.3e" % D0F)
    r = np.hypot(x, y)
    disco, lente = r < d, r < d / 4.0
    print("### il difetto di sovrapposizione del vuoto D = |dL_C - dL_S - roll(dL_S)| / |dL_C| (tutto il toro; nel disco r < %d dal punto medio); la lente r < %.2f: (rho_C - rho_S - roll rho_S) / rho_C"
          % (d, d / 4.0))
    for b0 in np.arange(0.0, tm[-1] + 1e-9, BLOCCO):
        k = np.where((tm >= b0) & (tm < b0 + BLOCCO) & (tm > 0))[0]
        if len(k) == 0:
            continue
        Dt, Dd, Ln = [], [], []
        for i in k:
            dif = dLC[i] - dLS[i] - rolla(dLS[i], d, L)
            Dt.append(np.linalg.norm(dif) / np.linalg.norm(dLC[i]))
            Dd.append(np.linalg.norm(dif[disco]) / np.linalg.norm(dLC[i][disco]))
            rl = rhoC[i] - rhoS[i] - rolla(rhoS[i], d, L)
            Ln.append(rl[lente].sum() / rhoC[i][lente].sum())
        print("  %7.0f .. %7.0f  D %.4e  D nel disco %.4e  la lente %+.4e" % (b0, b0 + BLOCCO, np.mean(Dt), np.mean(Dd), np.mean(Ln)))
    asse, trav = np.abs(y) < 0.5, np.abs(x) < 0.5
    print("### i profili di dLambda lungo l'asse (|y| < 0.5) e di traverso al punto medio (|x| < 0.5), ogni 5 nodi da -40 a 40: la coppia, e sotto la somma dei due singoli")
    for tp in TEMPI_PROFILI:
        i = int(np.argmin(np.abs(tm - tp)))
        som = dLS[i] + rolla(dLS[i], d, L)
        for nome_p, msk, cc in (("asse", asse, x), ("trav.", trav, y)):
            righe = []
            for q in (dLC[i], som):
                righe.append(" ".join("%+.2e" % (q[msk & (np.abs(cc - p) < 0.5)].mean() if (msk & (np.abs(cc - p) < 0.5)).any() else float("nan")) for p in range(-40, 41, 5)))
            print("  t %7.1f %-5s coppia %s" % (tm[i], nome_p, righe[0]))
            print("  %15s singoli %s" % ("", righe[1]))
    print("-" * 130)

    # ------------------------------------------------------------------ C-T: il tick commuta con la traslazione; E[0]; E_int; la fase relativa
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as dd_:
        tab_c, omega = dd_["c"].copy(), float(dd_["omega"])
    e_K = rrC[0]["e_K"]
    xS = [xx for rr in rrS for xx in (rr.get("stati") or []) if xx["t"] == 10000]
    assert len(xS) == 1
    with np.load(xS[0]["file"]) as dd_:
        stS = {k: dd_[k].copy() for k in dd_.files if k != "t"}
    assert all(SFM.sha(stS[k]) == vv for k, vv in xS[0]["sha"].items()), "lo stato di %s a 10000 NON e' quello del jsonl" % rif
    with CS.scena_con(V.N, L), V.scena(s, vuoto, V.EPS) as (_rec, z, _phi0, _pK):
        assert z["L"] == L
        salvato = {k: vv.copy() for k, vv in z["st"].items() if isinstance(vv, np.ndarray)}
        assert set(salvato) == set(stS), "le chiavi dello stato NON sono quelle della scena"
        assert all(vv.shape[0] % n == 0 for vv in salvato.values())
        phi_v = CA.vuoto_della_corsa(z, corsa)
        nodo_h = np.asarray(z["inc"].nodo).copy()     # ### il nodo di ogni estremita' (la fase relativa da psi_h, la cura (2))

        def metti(st):
            for k, vv in st.items():
                z["st"][k][...] = vv

        def un_tick(st):
            metti(st)
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                AC.tick(z, 10001, K)
            return {k: z["st"][k].copy() for k in st}
        A = {k: rolla(vv, d, L) for k, vv in un_tick(stS).items()}
        B = un_tick({k: rolla(vv, d, L) for k, vv in stS.items()})
        AF = {k: rolla(vv, d + 1, L) for k, vv in un_tick(stS).items()}
        eCT = max(float(np.max(np.abs(A[k] - B[k]))) / max(1e-300, float(np.max(np.abs(A[k])))) for k in A)
        eCF = max(float(np.max(np.abs(AF[k] - B[k]))) / max(1e-300, float(np.max(np.abs(AF[k])))) for k in AF)
        lim = n * np.finfo(float).eps
        esito("DEVE PASSARE: C-T un tick dello stato di %s a 10000 traslato di %d = il traslato del tick (senza bordo), entro n eps = %.2e relativo per chiave" % (rif, d, lim),
              eCT <= lim, "%.3e" % eCT)
        esito("DEVE FALLIRE: C-T-F lo stesso col traslato di %d: entro n eps" % (d + 1), not (eCF <= lim), "%.3e" % eCF)
        x0C = [xx for rr in rrC for xx in (rr.get("stati") or []) if xx["t"] == 0][0]
        with np.load(x0C["file"]) as dd_:
            st0C = {k: dd_[k].copy() for k in dd_.files if k != "t"}
        E0 = {k: [] for k in CONTI}
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):     # ### come il libro della corsa
            metti(st0C)
            eC0 = math.fsum(LCO.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, z["par"])["tot"].tolist())
            rE = abs(eC0 / campC[0]["E"]["totale"]["tot"] - 1.0)
            esito("DEVE PASSARE: E-0 il libro ricalcolato sullo stato di %s a t 0 = E del campione a t 0, entro n eps = %.2e relativo (mio: il controllo positivo di E[0])" % (corsa, lim),
                  rE <= lim, "%.3e" % rE)
            for c in campC:
                z["st"]["psi_h"][...] = 0.0
                z["st"]["phi_h"][...] = BO.c_di(c["t"], tab_c, K, omega) * phi_v
                co = LCO.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, z["par"])
                for k in CONTI:
                    E0[k].append(math.fsum(co[k].tolist()))
        metti(salvato)
    E0 = {k: np.array(vv) for k, vv in E0.items()}
    tt = tC * s
    Ei = {k: np.array([cC["E"]["totale"][k] - 2.0 * cS["E"]["totale"][k] for cC, cS in zip(campC, campS)]) + E0[k] for k in CONTI}
    Ea = Ei["tot"] + np.array([cC["bordo"]["E_ass"] - 2.0 * cS["bordo"]["E_ass"] for cC, cS in zip(campC, campS)])
    print("### E_int = E[C] - 2 E[S] + E[0] (Luca 16:28; E[0] il vuoto c(t) F3 su L %d, %d campioni; E[0] tot da %.10e a %.10e), per termini; e con E_ass (la forma conservata col bordo)"
          % (L, len(tt), E0["tot"][0], E0["tot"][-1]))
    print("  %-17s %-12s %-12s %-12s %-12s %-12s %-12s" % ("il tempo", "cin", "vuo", "leg", "cost", "tot", "tot + E_ass"))
    for b0 in np.arange(0.0, tt[-1] + 1e-9, BLOCCO):
        k = (tt >= b0) & (tt < b0 + BLOCCO)
        print("  %7.0f .. %7.0f %s %+.5e" % (b0, b0 + BLOCCO, " ".join("%+.5e" % Ei[c][k].mean() for c in CONTI), Ea[k].mean()))
    print("  a t 0: E_int %+.6e (E[S] %.10e: relativa %.3e)" % (Ei["tot"][0], campS[0]["E"]["totale"]["tot"], Ei["tot"][0] / campS[0]["E"]["totale"]["tot"]))
    print("-" * 130)
    stC = [xx for rr in rrC for xx in (rr.get("stati") or [])]
    x0S = [xx for rr in rrS for xx in (rr.get("stati") or []) if xx["t"] == 0][0]
    with np.load(x0S["file"]) as dd_:
        ref = dd_["psi_h"].copy()                    # ### la cura (2): la chiave psi degli stati e' NULLA, lo stato vero e' psi_h per estremita'
    refB = rolla(ref, d, L)                          # ### la stessa traslazione della partenza della coppia (roll di (L, L, -1, ...))
    mA, mB = (x < 0)[nodo_h], (x >= 0)[nodo_h]       # ### il semipiano dell'estremita' e' quello del suo nodo
    print("### la fase relativa dei due: arg <roll(psi_S(0)) | psi_C>_B - arg <psi_S(0) | psi_C>_A sui semipiani, agli stati completi")
    fa = []
    for xx in stC:
        with np.load(xx["file"]) as dd_:
            ps = dd_["psi_h"].copy()
        pA = complex(np.sum(np.conj(ref[mA]) * ps[mA]))
        pB = complex(np.sum(np.conj(refB[mB]) * ps[mB]))
        f = math.atan2((pB / pA).imag, (pB / pA).real)
        fa.append(f)
        print("  t %8.1f  |pA| %.6e |pB| %.6e  la fase relativa %+.6f rad" % (xx["t"] * s, abs(pA), abs(pB), f))
    atteso = 0.0 if segno > 0 else math.pi
    cA_ = abs(complex(np.sum(np.conj(ref[mA]) * refB[mA]))) / float(np.sum(np.abs(ref[mA]) ** 2))
    cB_ = abs(complex(np.sum(np.conj(refB[mB]) * ref[mB]))) / float(np.sum(np.abs(refB[mB]) ** 2))
    dfa = abs(((fa[0] - atteso + math.pi) % (2 * math.pi)) - math.pi)
    esito("DEVE PASSARE: FA0 la fase relativa a t 0 = %s (il segno %+d), entro le code incrociate sui semipiani %.3e" % ("0" if segno > 0 else "pi", segno, cA_ + cB_), dfa <= cA_ + cB_,
          "%.3e" % dfa)
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
