# -*- coding: utf-8 -*-
r"""**L'ANALISI DI STABILITA' LINEARE ESATTA DELLO STATO DI MATERIA UNIFORME** — *un conto, che non
cambia il modello.*

> ### ⛔ **Il task history e' `2026-10-20_stabilita_lineare.md`** *(`51986247`)*, coi criteri
> fissati prima. Decisione di Luca del `2026-10-20` alle `12:32`. ### **Nessuna cura.**

## ⭐ IL METODO

### **La funzione di Green di UN tick, lungo l'orbita:** la cella e' il nodo `v` coi suoi `2`
archi *(`4` estremita', `12` complessi, `24` reali)*. Per ogni coordinata reale `j` della cella
`0` si perturba la base di `eps_j`, si fa un tick, e la differenza divisa per `eps_j` e' ### **la
colonna `j`**; ### **la trasformata di Fourier sulle celle da' `R_t(k)` per TUTTI i `k`**. La
monodromia `M(k) = R_N(k) ... R_1(k)` su `N dtau = 25`, e ### **`gamma(k) = ln |lambda_max| /
(N dtau cs_m)`**.

## ⛔ LE PROVE

`P1` nessuna memoria nelle cache · `P2` la linearita' a due ampiezze · ### **il caso che deve
fallire: la camminata sola, ESATTA** · ### **il caso che deve riuscire: gamma e `k` come le
misure.**

Gira con:  python csv/_stabilita_lineare.py            (il conto di `c38367db`)
           python csv/_stabilita_lineare.py --lungo    (l'intervallo lungo, a lati pari)
           python csv/_stabilita_lineare.py --proiettata  (la base proiettata, gamma come pendenza)
           python csv/_stabilita_lineare.py --risonanza   (D0: la dispersione della camminata contro la banda di S3)
"""
import io
import json
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _jeans_del_modello as JM                                 # noqa: E402

EPS = float(np.finfo(float).eps)
X = 0.1
RAPPORTO = 1.0
TEMPO_N = 25.0                 # N dtau: dichiarato nel task history
EPS_REL = 1e-7
EPS_REL_2 = 1e-6
BANDA_LIN = 1e-3               # P2: tolleranza del conto, dichiarata
ULP_C2 = 64.0                  # il caso che deve fallire: N * 64 ulp
BUDGET_S = 4 * 3600.0
S3 = "CAMM-MATERIA-VUOTO"
FASE = "CAMM-FASE-VUOTO"
CACHE = ("psi", "rho", "Lambda", "h_int")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "stabilita_lineare.jsonl")
J_RAFF = os.path.join(RADICE, "doc", "referti_l2", "raffinamento.jsonl")
NC = 12                        # complessi per cella
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-70s %s   %s" % (che[:70], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


# =====================================================================================
#   LA SCENA E IL PASSO
# =====================================================================================
def scena(lato, dtau, x):
    import scena_l2 as SC
    import statica_protocollo as PR
    lati = (lato, lato)
    inc, mot, st, par, _c, _p = SC.scena(dtau, PR.VUOTO, 0.0, PR.RAGGIO, False, True, False,
                                         PR.SEME, 1, lati=lati)
    st["psi_h"][...] = float(np.sqrt(x)) * PR.chi_allineato(lati, inc.m)
    return inc, mot, st, par


def copia(st):
    return {k: v.copy() for k, v in st.items()}


def passo(st, mot, par, acceso, salta, lc):
    import composizione as CM
    import tick as TK
    if acceso:
        TK.tick_con_cs(st, mot, par, lc, salta)
    else:
        TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))


def celle(st, n):
    """### `(n, 24)` reali: per cella le `4` estremita' -- `psi` (`8`) e `phi` (`4`) -- re e im."""
    z = np.concatenate([st["psi_h"].reshape(n, 8), st["phi_h"].reshape(n, 4)], axis=1)
    return np.concatenate([z.real, z.imag], axis=1)


def perturba(st, j, e):
    """### La coordinata reale `j` della cella `0` di `e`."""
    c, im = j % NC, j >= NC
    d = 1j * e if im else e
    if c < 8:
        st["psi_h"][c // 2, c % 2] += d
    else:
        st["phi_h"][c - 8] += d


# =====================================================================================
#   LA FUNZIONE DI GREEN E LA MONODROMIA
# =====================================================================================
def green(base, mot, par, acceso, salta, lc, lato, scale, eps_rel, dopo=None):
    """### `R(k)` `(L, L, 24, 24)` di un tick dalla base; `dopo` e' il tick della base."""
    n = lato * lato
    if dopo is None:
        dopo = copia(base)
        passo(dopo, mot, par, acceso, salta, lc)
    c0 = celle(dopo, n)
    R = np.empty((lato, lato, 2 * NC, 2 * NC), dtype=complex)
    for j in range(2 * NC):
        e = eps_rel * scale[0 if (j % NC) < 8 else 1]
        p = copia(base)
        perturba(p, j, e)
        passo(p, mot, par, acceso, salta, lc)
        d = (celle(p, n) - c0) / e
        R[:, :, :, j] = np.fft.fft2(d.reshape(lato, lato, 2 * NC), axes=(0, 1))
    return R, dopo


def uniformita(st, n):
    c = celle(st, n)
    s = float(np.max(np.abs(c))) or 1.0
    return float(np.max(np.abs(c - c[0]))) / (EPS * s)


def gamma_da(M, tempo):
    lam = np.linalg.eigvals(M)
    return np.log(np.max(np.abs(lam), axis=-1)) / tempo


def braccio(nome, lato, dtau, x, acceso, salta, eps_rel):
    import flussi_parziali as FP
    inc, mot, st, par = scena(lato, dtau, x)
    n = inc.n
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    lc = RAPPORTO * lm
    cs_m = lm / (lm + lc) if acceso else 1.0
    if acceso:
        FP.accendi_cs(mot, lc, st)
    N = int(round(TEMPO_N / dtau))
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    fuori = {"nome": nome, "lato": lato, "dtau": dtau, "x": x, "acceso": acceso,
             "salta": list(salta), "eps_rel": eps_rel, "N": N, "cs_m": cs_m,
             "rho_m": rm, "lambda_m": lm, "fine": "N"}
    M = np.broadcast_to(np.eye(2 * NC, dtype=complex), (lato, lato, 2 * NC, 2 * NC)).copy()
    unif = uniformita(st, n)
    t0 = time.time()
    base = st
    for t in range(1, N + 1):
        R, dopo = green(base, mot, par, acceso, salta, lc, lato, scale, eps_rel)
        M = np.matmul(R, M)
        base = dopo
        unif = max(unif, uniformita(base, n))
        if t == N // 2:
            fuori["gamma_meta"] = gamma_da(M, (N // 2) * dtau * cs_m)
        if time.time() - t0 > BUDGET_S:
            fuori["fine"] = "BUDGET superato al passo %d di %d" % (t, N)
            N = t
            break
    fuori["secondi"] = time.time() - t0
    fuori["uniformita_ulp"] = unif
    fuori["gamma"] = gamma_da(M, N * dtau * cs_m)
    fuori["nu_s3"] = lm ** 2 / (rm + lm) ** 2
    return fuori


def braccio_c2_esatto(lato, dtau):
    """### La camminata sola e' LINEARE: impulso `1` su base NULLA, nessuna differenza."""
    inc, mot, st, par = scena(lato, dtau, X)
    n = inc.n
    for k in st:
        st[k][...] = 0
    zero = copia(st)
    passo(zero, mot, par, False, (S3,), 0.0)
    R, _ = green(st, mot, par, False, (S3,), 0.0, lato, (1.0, 1.0), 1.0, dopo=zero)
    N = int(round(TEMPO_N / dtau))
    M = np.linalg.matrix_power(R, N)
    lam = np.linalg.eigvals(M)
    return {"N": N, "dev": float(np.max(np.abs(np.log(np.abs(lam))))),
            "zero_dopo": float(np.max(np.abs(celle(zero, n))))}


# =====================================================================================
#   LE STAMPE
# =====================================================================================
def kpi(m, lato):
    m = m if m <= lato // 2 else m - lato
    return m, 2.0 * m / lato


def sommario(b):
    g = np.asarray(b["gamma"])
    lato = b["lato"]
    i, j = np.unravel_index(int(np.argmax(g)), g.shape)
    (mx, px), (my, py) = kpi(i, lato), kpi(j, lato)
    print("  %-30s lato %-4d dtau %-8g x %-5g N %-4d [%s, %.0f s]  uniformita' %.1f ulp"
          % (b["nome"], lato, b["dtau"], b["x"], b["N"], b["fine"], b["secondi"],
             b["uniformita_ulp"]))
    print("      gamma max %+.4e a k = (%d,%d) = (%.3f, %.3f) pi;  gamma(k=0) %+.3e;"
          "  N/2: %+.4e;  nu_S3/OMEGA_H %.4f"
          % (float(g[i, j]), mx, my, px, py, float(g[0, 0]),
             float(np.max(b["gamma_meta"])), b["nu_s3"] / np.pi))
    ax = [float(g[m, 0]) for m in range(0, lato // 2 + 1, max(1, lato // 16))]
    dg = [float(g[m, m]) for m in range(0, lato // 2 + 1, max(1, lato // 16))]
    # ### 📌 INFORMAZIONE, NON CRITERIO (aggiunta dopo una prova non tenuta, che ha visto
    # ### gamma diverso fra N/2 e N e gamma(k = 0) > 0): ### **il gamma della SECONDA META'
    # ### dell'intervallo**, `(ln|l_N| - ln|l_N/2|) / (tempo della seconda meta')`, che ### **toglie
    # ### il transitorio** -- e se differisce dal gamma dichiarato, l'intervallo non basta.
    tn = b["N"] * b["dtau"] * b["cs_m"]
    tm = (b["N"] // 2) * b["dtau"] * b["cs_m"]
    g2 = (g * tn - np.asarray(b["gamma_meta"]) * tm) / (tn - tm)
    i2, j2 = np.unravel_index(int(np.argmax(g2)), g2.shape)
    print("      ### INFORMAZIONE: gamma della seconda meta' -- max %+.4e a k = (%d,%d);"
          " a k = 0 %+.3e" % (float(g2[i2, j2]), kpi(i2, lato)[0], kpi(j2, lato)[0],
                              float(g2[0, 0])))
    passo_ = max(1, lato // 16)
    print("      lungo (m,0), m = 0,%d,..: %s" % (passo_, " ".join("%+.3f" % v for v in ax)))
    print("      lungo (m,m), m = 0,%d,..: %s" % (passo_, " ".join("%+.3f" % v for v in dg)))
    sys.stdout.flush()
    return float(g[i, j]), (mx, my)


def misurati():
    fuori = {}
    with io.open(J_RAFF, encoding="utf-8") as f:
        for riga in f:
            b = json.loads(riga)
            s = b["dtau"] * b["cs_m"]
            fuori[(b["nome"], b["lato"])] = {
                "gamma": b["rho"]["gamma"] / s, "barra": b["rho"]["barra"] / s,
                "k": [(b[c]["onda"]["kx"], b[c]["onda"]["ky"]) for c in ("rho", "lam")]}
    return fuori


def salva(b):
    d = dict(b)
    d["gamma"] = np.asarray(b["gamma"]).tolist()
    d["gamma_meta"] = np.asarray(b["gamma_meta"]).tolist()
    with io.open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(d) + "\n")


# =====================================================================================
#   MAIN
# =====================================================================================
def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    import statica_protocollo as PR
    import tick as TK
    ts = JM.t_soglia()
    print("=" * 100)
    print("L'ANALISI DI STABILITA' LINEARE ESATTA DELLO STATO DI MATERIA UNIFORME -- un conto")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la materia uniforme: VUOTO %.1f, rapporto %g, chi_allineato; la cella: 4 estremita',"
          " 24 reali" % (PR.VUOTO, RAPPORTO))
    print("  il passo: %d pezzi, impronta %s; la monodromia su N dtau = %g; eps_rel %g (e %g);"
          " banda di linearita' %g; budget %.0f s" % (len(CM.ORDINE), CM.IMPRONTA, TEMPO_N,
                                                     EPS_REL, EPS_REL_2, BANDA_LIN, BUDGET_S))
    print("  la soglia di Student (4 gradi) %.3f; OMEGA_H = pi" % ts)
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    mis = misurati()

    # ---------------------------------------------------------------- P1
    print("### P1: NESSUNA MEMORIA NELLE CACHE")
    for acceso in (True, False):
        import flussi_parziali as FP
        inc, mot, st, par = scena(31, 0.125, X)
        lc = float(np.mean(mot.densita_vuoto(st)))
        if acceso:
            FP.accendi_cs(mot, lc, st)
        passo(st, mot, par, acceso, (), lc)         # una base dopo un tick: le cache piene
        a, b = copia(st), copia(st)
        for k in CACHE:
            b[k][...] = 0
        passo(a, mot, par, acceso, (), lc)
        passo(b, mot, par, acceso, (), lc)
        uguali = (np.array_equal(a["psi_h"], b["psi_h"]) and
                  np.array_equal(a["phi_h"], b["phi_h"]))
        if not esito("P1 cs %s: un tick con le cache azzerate = con le cache, AL BIT"
                     % ("acceso" if acceso else "spento"), uguali):
            print("### STOP: le cache sono memoria, e il conto lineare dovrebbe includerle")
            return 1
    print("-" * 100)

    # ---------------------------------------------------------------- il caso che deve fallire
    print("### IL CASO CHE DEVE FALLIRE: LA CAMMINATA SOLA (senza %s, cs spento), ESATTA" % S3)
    c2 = braccio_c2_esatto(31, 0.125)
    tetto = c2["N"] * ULP_C2 * EPS
    if not esito("C2 esatta: max |ln|lambda|| <= N * 64 ulp, per ogni k",
                 c2["dev"] <= tetto, "%.3e contro %.3e (N %d; la base nulla resta %.1e)"
                 % (c2["dev"], tetto, c2["N"], c2["zero_dopo"])):
        print("### STOP: la camminata sola non conserva la norma di ogni modo")
        return 1
    bb = {}
    b = braccio("C2 differenze (pavimento)", 31, 0.125, X, False, (S3,), EPS_REL)
    salva(b)
    bb["C2"] = b
    pav = float(np.max(np.abs(b["gamma"])))
    print("  ### INFORMAZIONE: il pavimento del metodo (C2 con le differenze sulla base"
          " uniforme): max |gamma| %.3e" % pav)
    sommario(b)
    print("-" * 100)

    # ---------------------------------------------------------------- P2 e il caso che riesce
    print("### P2 E IL CASO CHE DEVE RIUSCIRE (lato 31, dtau 0.125, x 0.1)")
    for nome, acceso in (("R1", True), ("R2", False)):
        b1 = braccio("%s (b)" % nome if acceso else "%s (a) S3 sola" % nome, 31, 0.125, X,
                     acceso, (), EPS_REL)
        salva(b1)
        b2 = braccio("%s eps 1e-6" % nome, 31, 0.125, X, acceso, (), EPS_REL_2)
        salva(b2)
        bb[nome] = b1
        gmax, kmax = sommario(b1)
        g1, g2 = np.asarray(b1["gamma"]), np.asarray(b2["gamma"])
        d = float(np.max(np.abs(g1 - g2)))
        if not esito("P2 %s: max_k |gamma_1e-7 - gamma_1e-6| <= %g max gamma"
                     % (nome, BANDA_LIN), d <= BANDA_LIN * gmax,
                     "%.3e contro %.3e" % (d, BANDA_LIN * gmax)):
            print("### STOP: il conto non e' lineare in eps")
            return 1
        m = mis[(nome, 31)]
        ok = esito("%s: gamma max %.4f = misurato %.4f +- %.4f entro t*barra"
                   % (nome, gmax, m["gamma"], m["barra"]),
                   abs(gmax - m["gamma"]) <= ts * m["barra"],
                   "%.2f barre semplici" % (abs(gmax - m["gamma"]) / m["barra"]))
        for kx, ky in m["k"]:
            gk = float(g1[kx % 31, ky % 31])
            ok &= esito("%s: il k misurato (%d,%d) fra i massimi: gamma %.4f >= %.4f"
                        % (nome, kx, ky, gk, gmax - ts * m["barra"]),
                        gk >= gmax - ts * m["barra"])
        if not ok:
            print("### STOP: il conto non riproduce le misure")
            return 1
    print("-" * 100)

    # ---------------------------------------------------------------- la scomposizione
    print("### LA SCOMPOSIZIONE (lato 31)")
    b = braccio("(c) senza FASE, cs acceso", 31, 0.125, X, True, (FASE,), EPS_REL)
    salva(b)
    sommario(b)
    print("### x in {0.01, 0.1, 1}: gamma max, il k, e nu_S3/OMEGA_H")
    for nome, acceso in (("R1", True), ("R2", False)):
        for x in (0.01, 1.0):
            b = braccio("%s x %g" % (nome, x), 31, 0.125, x, acceso, (), EPS_REL)
            salva(b)
            sommario(b)
    print("### IL NUMERO DI COURANT: dtau a griglia fissa (lato 31, x 0.1)")
    for nome, acceso in (("R1", True), ("R2", False)):
        for dt in (0.25, 0.0625):
            b = braccio("%s dtau %g" % (nome, dt), 31, dt, X, acceso, (), EPS_REL)
            salva(b)
            sommario(b)
    print("-" * 100)

    # ---------------------------------------------------------------- l'invarianza di raffinamento
    print("### L'INVARIANZA DI RAFFINAMENTO (regola di scala di Luca)")
    for nome, acceso in (("R1", True), ("R2", False)):
        g31 = np.asarray(bb[nome]["gamma"])
        for lato, dt in ((62, 0.0625), (124, 0.03125)):
            b = braccio("%s lato %d" % (nome, lato), lato, dt, X, acceso, (), EPS_REL)
            salva(b)
            gmax, _k = sommario(b)
            if b["fine"] != "N":
                print("### STOP: il budget e' superato -- si riporta e ci si ferma")
                return 1
            m = mis[(nome, lato)]
            esito("%s lato %d: gamma max %.4f = misurato %.4f +- %.4f entro t*barra"
                  % (nome, lato, gmax, m["gamma"], m["barra"]),
                  abs(gmax - m["gamma"]) <= ts * m["barra"],
                  "%.2f barre semplici" % (abs(gmax - m["gamma"]) / m["barra"]))
            q = lato // 31
            gc = np.asarray(b["gamma"])[::q, ::q]
            print("      la curva sui k comuni con lato 31: max |gamma_%d - gamma_31| %.3e"
                  " (relativo al massimo %.3e)"
                  % (lato, float(np.max(np.abs(gc - g31))),
                     float(np.max(np.abs(gc - g31))) / float(np.max(g31))))
    print("=" * 100)
    print("### %d/%d prove passate. NESSUNA CURA: ogni cura tocca una legge. LINEARE e Lambda_c"
          " FERMI." % tuple(OK))
    print("=" * 100)
    _ = TK
    return 0


# =====================================================================================
#   L'INTERVALLO LUNGO, A LATI PARI  (mandato di Luca del 2026-10-20, 15:57)
#   ### task history `2026-10-20_stabilita_intervallo_lungo.md` (`61b420a5`).
#   ### ⛔ **SI AGGIUNGE, non si riscrive:** tutto cio' che sta sopra resta il conto di
#   ### `c38367db`, e la prima prova di `--lungo` lo rifa' AL BIT.
# =====================================================================================
TEMPO_LUNGO = 100.0            # N dtau, dal mandato
BUDGET_LUNGO = 3 * 3600.0      # dal mandato
SOGLIA_5 = 0.05                # asintotico e chi vince, dal mandato
INTORNO = 0.1                  # l'intorno di (pi, pi), in unita' di pi, dal mandato
GUARDIANO = {"intero": (0.3754, (10, 0)), "meta": (0.585, (16, 16)), "banda": 1e-3}
JSONL_LUNGO = os.path.join(RADICE, "doc", "referti_l2", "stabilita_intervallo_lungo.jsonl")


def braccio_lungo(nome, lato, dtau, x, acceso, salta, eps_rel):
    """### Come `braccio`, con ### **la monodromia RINORMALIZZATA per `k`** e i quattro quarti."""
    import flussi_parziali as FP
    inc, mot, st, par = scena(lato, dtau, x)
    n = inc.n
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    lc = RAPPORTO * lm
    cs_m = lm / (lm + lc) if acceso else 1.0
    if acceso:
        FP.accendi_cs(mot, lc, st)
    N = int(round(TEMPO_LUNGO / dtau))
    assert N % 4 == 0, "N = %d non si divide in quattro quarti" % N
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    fuori = {"nome": nome, "lato": lato, "dtau": dtau, "x": x, "acceso": acceso,
             "salta": list(salta), "eps_rel": eps_rel, "N": N, "cs_m": cs_m,
             "rho_m": rm, "lambda_m": lm, "fine": "N"}
    M = np.broadcast_to(np.eye(2 * NC, dtype=complex), (lato, lato, 2 * NC, 2 * NC)).copy()
    acc = np.zeros((lato, lato))
    L = []
    unif = uniformita(st, n)
    t0 = time.time()
    base = st
    for t in range(1, N + 1):
        R, dopo = green(base, mot, par, acceso, salta, lc, lato, scale, eps_rel)
        M = np.matmul(R, M)
        s = np.sqrt(np.sum(np.abs(M) ** 2, axis=(-2, -1)))
        M /= s[..., None, None]
        acc += np.log(s)
        base = dopo
        unif = max(unif, uniformita(base, n))
        if t % (N // 4) == 0:
            L.append(acc + np.log(np.max(np.abs(np.linalg.eigvals(M)), axis=-1)))
        if time.time() - t0 > BUDGET_LUNGO:
            fuori["fine"] = "BUDGET superato al passo %d di %d" % (t, N)
            break
    fuori["secondi"] = time.time() - t0
    fuori["uniformita_ulp"] = unif
    fuori["L"] = L
    if fuori["fine"] == "N":
        tq = (N // 4) * dtau * cs_m
        fuori["gamma"] = L[3] / (4 * tq)
        fuori["gamma_meta"] = L[1] / (2 * tq)
        fuori["quarti"] = [(L[q] - (L[q - 1] if q else 0.0)) / tq for q in range(4)]
        fuori["seconda_meta"] = (L[3] - L[1]) / (2 * tq)
    fuori["nu_s3"] = lm ** 2 / (rm + lm) ** 2
    return fuori


def c2_esatto_lungo(lato, dtau):
    """### La camminata sola, ESATTA, su `N dtau = 100`."""
    inc, mot, st, par = scena(lato, dtau, X)
    for k in st:
        st[k][...] = 0
    zero = copia(st)
    passo(zero, mot, par, False, (S3,), 0.0)
    R, _ = green(st, mot, par, False, (S3,), 0.0, lato, (1.0, 1.0), 1.0, dopo=zero)
    N = int(round(TEMPO_LUNGO / dtau))
    lam = np.linalg.eigvals(np.linalg.matrix_power(R, N))
    return {"N": N, "dev": float(np.max(np.abs(np.log(np.abs(lam)))))}


def fase_pi(m, lato):
    """### `k` in unita' di `pi`, in `(-1, 1]`."""
    m = m % lato
    return 2.0 * (m if m <= lato // 2 else m - lato) / lato


def punto_banda(g4, lato):
    """### Il massimo di `g4` su assi e diagonale, esclusi `k = 0` e l'intorno di `(pi, pi)`."""
    meglio, dove = -np.inf, None
    for m in range(1, lato):
        for kx, ky in ((m, 0), (0, m), (m, m)):
            px, py = fase_pi(kx, lato), fase_pi(ky, lato)
            if (1.0 - abs(px)) <= INTORNO and (1.0 - abs(py)) <= INTORNO:
                continue
            if g4[kx, ky] > meglio:
                meglio, dove = float(g4[kx, ky]), (kx, ky)
    return dove


def semi_larghezza(g4, lato):
    h = lato // 2
    for d in range(1, 5):
        if g4[h - d, h - d] < 0.5 * g4[h, h]:
            return d
    return None


def leggi_lungo(b):
    """### Le etichette del task history, sezione `3`."""
    lato = b["lato"]
    q = [np.asarray(v) for v in b["quarti"]]
    g4 = q[3]
    mx = float(np.max(g4))
    h = lato // 2
    kb = punto_banda(g4, lato)
    punti = (("(pi,pi)", (h, h)), ("banda", kb), ("k=0", (0, 0)))
    print("      i quattro quarti (gamma nel tempo proprio); il massimo assoluto dell'ultimo"
          " quarto %+.4e" % mx)
    et = {}
    for nome, (kx, ky) in punti:
        v = [float(qq[kx, ky]) for qq in q]
        asin = abs(v[3] - v[2]) <= SOGLIA_5 * mx
        et[nome] = {"k": [int(kx), int(ky)], "quarti": v, "asintotico": bool(asin)}
        print("      %-8s k = (%d,%d) = (%.3f, %.3f) pi:  %s   -> %s"
              % (nome, kx, ky, fase_pi(kx, lato), fase_pi(ky, lato),
                 " ".join("%+.4e" % w for w in v),
                 "ASINTOTICO" if asin else "NON ASINTOTICO"))
    a, c = et["(pi,pi)"]["quarti"][3], et["banda"]["quarti"][3]
    if abs(a - c) < SOGLIA_5 * mx:
        vince = "NON DECIDIBILE"
    else:
        vince = "IL PICCO a (pi,pi)" if a > c else "LA BANDA"
    print("      CHI VINCE nell'ultimo quarto: %s  (picco %+.4e, banda %+.4e, differenza %.3e"
          " contro %.3e)" % (vince, a, c, abs(a - c), SOGLIA_5 * mx))
    sm = float(np.asarray(b["seconda_meta"])[0, 0])
    z = et["k=0"]["quarti"][3]
    vera = z >= 0.5 * sm and z > 0.02
    print("      k = 0: ultimo quarto %+.4e, seconda meta' %+.4e -> %s"
          % (z, sm, "CRESCITA VERA" if vera else
             "TRANSITORIO: la frase <<nessuna lunghezza minima>> si RITIRA"))
    diag = [float(g4[h - d, h - d]) for d in (4, 3, 2, 1, 0)]
    sl = semi_larghezza(g4, lato)
    print("      la diagonale negli ultimi 4 m prima di pi (m = %d..%d): %s;  semi-larghezza %s"
          % (h - 4, h, " ".join("%+.4e" % w for w in diag), sl if sl else "> 4"))
    sys.stdout.flush()
    return {"punti": et, "vince": vince, "k0_vera": bool(vera), "diagonale": diag,
            "semi_larghezza": sl}


def salva_lungo(b, et):
    d = {k: v for k, v in b.items() if k not in ("L", "gamma", "gamma_meta", "quarti",
                                                  "seconda_meta")}
    for k in ("L", "quarti"):
        if k in b:
            d[k] = [np.asarray(v).tolist() for v in b[k]]
    for k in ("gamma", "gamma_meta", "seconda_meta"):
        if k in b:
            d[k] = np.asarray(b[k]).tolist()
    d["etichette"] = et
    with io.open(JSONL_LUNGO, "a", encoding="utf-8") as f:
        f.write(json.dumps(d) + "\n")


def vecchio_jsonl(nome):
    with io.open(JSONL, encoding="utf-8") as f:
        for riga in f:
            b = json.loads(riga)
            if b["nome"] == nome:
                return b
    raise AssertionError("il braccio `%s` non e' nel jsonl di c38367db" % nome)


def simmetrici(k, lato):
    """### Le immagini di `k` per le simmetrie del quadrato."""
    a, b = k
    fuori = set()
    for x, y in ((a, b), (b, a)):
        for sx in (1, -1):
            for sy in (1, -1):
                fuori.add(((sx * x) % lato, (sy * y) % lato))
    return fuori


def main_lungo(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    import statica_protocollo as PR
    print("=" * 100)
    print("L'ANALISI DI STABILITA' LINEARE SU UN INTERVALLO LUNGO, A LATI PARI -- un conto")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la materia uniforme: x %g, VUOTO %.1f, rapporto %g, chi_allineato; la cella: 24 reali"
          % (X, PR.VUOTO, RAPPORTO))
    print("  il passo: %d pezzi, impronta %s; lati 32 (dtau 0.125) e 64 (dtau 0.0625);"
          " N dtau = %g; la monodromia RINORMALIZZATA per k; i quattro quarti"
          % (len(CM.ORDINE), CM.IMPRONTA, TEMPO_LUNGO))
    print("  eps_rel %g (e %g a lato 32); banda di linearita' %g; soglie %g; intorno di (pi,pi)"
          " %g pi; budget %.0f s" % (EPS_REL, EPS_REL_2, BANDA_LIN, SOGLIA_5, INTORNO,
                                     BUDGET_LUNGO))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL_LUNGO, "w", encoding="utf-8").close()

    print("### I CASI DI CONTROLLO")
    vecchio = vecchio_jsonl("R2 (a) S3 sola")
    b = braccio("R2 (a) S3 sola", 31, 0.125, X, False, (), EPS_REL)
    g = np.asarray(b["gamma"])
    i, j = np.unravel_index(int(np.argmax(g)), g.shape)
    if not esito("il conto di c38367db AL BIT: R2 a lato 31, gamma %.4f a (%d,%d)"
                 % (float(g[i, j]), kpi(i, 31)[0], kpi(j, 31)[0]),
                 np.array_equal(g, np.asarray(vecchio["gamma"]))):
        print("### STOP: lo strumento esteso non riproduce c38367db")
        return 1
    c2 = c2_esatto_lungo(32, 0.125)
    tetto = c2["N"] * ULP_C2 * EPS
    if not esito("DEVE FALLIRE: la camminata sola esatta, lato 32, N dtau 100: <= N*64 ulp",
                 c2["dev"] <= tetto, "%.3e contro %.3e (N %d)" % (c2["dev"], tetto, c2["N"])):
        print("### STOP: il metodo e' rotto")
        return 1
    b = braccio("R2 lato 32, N dtau 25", 32, 0.125, X, False, (), EPS_REL)
    g = np.asarray(b["gamma"])
    tn = b["N"] * b["dtau"] * b["cs_m"]
    tm = (b["N"] // 2) * b["dtau"] * b["cs_m"]
    g2 = (g * tn - np.asarray(b["gamma_meta"]) * tm) / (tn - tm)
    ok = True
    for che, arr, (val, kk) in (("intero", g, GUARDIANO["intero"]),
                                ("seconda meta'", g2, GUARDIANO["meta"])):
        i, j = np.unravel_index(int(np.argmax(arr)), arr.shape)
        ok &= esito("DEVE RIUSCIRE: R2 lato 32, N dtau 25, %s: %.4f a (%d,%d) contro %.3f a %s"
                    % (che, float(arr[i, j]), kpi(i, 32)[0], kpi(j, 32)[0], val, kk),
                    abs(float(arr[i, j]) - val) <= GUARDIANO["banda"]
                    and (i, j) in simmetrici(kk, 32))
    if not ok:
        print("### STOP: il conto non riproduce i numeri del guardiano")
        return 1
    print("-" * 100)

    risultati = {}
    for lato, dtau in ((32, 0.125), (64, 0.0625)):
        for nome, acceso in (("R1", True), ("R2", False)):
            b = braccio_lungo("%s lato %d" % (nome, lato), lato, dtau, X, acceso, (), EPS_REL)
            if b["fine"] != "N":
                salva_lungo(b, None)
                print("  %s lato %d: %s -- ### STOP: si dichiara e ci si ferma"
                      % (nome, lato, b["fine"]))
                return 1
            sommario(b)
            et = leggi_lungo(b)
            salva_lungo(b, et)
            risultati[(nome, lato)] = et
            if lato == 32:
                b2 = braccio_lungo("%s lato 32 eps 1e-6" % nome, lato, dtau, X, acceso, (),
                                   EPS_REL_2)
                if b2["fine"] != "N":
                    print("  linearita' %s: %s -- ### STOP" % (nome, b2["fine"]))
                    return 1
                d = float(np.max(np.abs(np.asarray(b["gamma"]) - np.asarray(b2["gamma"]))))
                gm = float(np.max(b["gamma"]))
                salva_lungo(b2, None)
                if not esito("linearita' %s lato 32: max_k |gamma_1e-7 - gamma_1e-6| <= %g max"
                             % (nome, BANDA_LIN), d <= BANDA_LIN * gm,
                             "%.3e contro %.3e" % (d, BANDA_LIN * gm)):
                    print("### STOP: il conto non e' lineare in eps")
                    return 1
    print("-" * 100)
    print("### LA LARGHEZZA DEL PICCO a (pi,pi): semi-larghezza in m (NUMERO DI ARCHI)")
    for nome in ("R1", "R2"):
        a, c = risultati[(nome, 32)]["semi_larghezza"], risultati[(nome, 64)]["semi_larghezza"]
        if a is None or c is None:
            v = "non misurabile entro 4 m"
        else:
            griglia, segue_k = abs(c - a) <= 1, abs(c - 2 * a) <= 1
            v = ("NON SEPARABILE (entrambe)" if griglia and segue_k else
                 "SEGUE LA GRIGLIA" if griglia else "SEGUE k" if segue_k else
                 "ne' l'una ne' l'altra")
        print("  %s: lato 32 %s, lato 64 %s -> %s" % (nome, a, c, v))
    print("=" * 100)
    print("### %d/%d prove passate. NESSUNA CURA. LINEARE e Lambda_c FERMI; D4 da rileggere."
          % tuple(OK))
    print("=" * 100)
    return 0


# =====================================================================================
#   LA BASE PROIETTATA E GAMMA COME PENDENZA  (mandato di Luca del 2026-10-20, 18:02)
#   ### task history `2026-10-20_base_proiettata.md` (`29faf0ef`).
#   ### ⛔ **SI AGGIUNGE, non si riscrive:** il conto di `c38367db` (senza argomenti) e
#   ### quello di `16b5d10f` (`--lungo`) restano intatti, e le prove li rifanno AL BIT.
# =====================================================================================
OGNI = 4                       # ogni quanti tick si registra ln|lambda| e ln||M||, dal mandato
SOGLIA_UNIF = 1e3              # ulp: la base valida, dal mandato
PREV_GUARDIANO = 1e-2          # la previsione del guardiano, dal mandato
ULP_P3 = 64.0                  # P3, dal mandato
JSONL_PROIETTATA = os.path.join(RADICE, "doc", "referti_l2", "stabilita_base_proiettata.jsonl")


def proietta(st, n):
    """### Ogni campo sulla MEDIA DELLE CELLE, componente per componente della cella."""
    for v in st.values():
        if v.shape[0] == n:
            v[...] = np.mean(v, axis=0)
        elif v.shape[0] == 4 * n:
            w = v.reshape((n, 4) + v.shape[1:])
            w[...] = np.mean(w, axis=0)
        else:
            raise AssertionError("un campo di forma %r non e' ne' per nodo ne' per estremita'"
                                 % (v.shape,))


def pendenze(tt, LL, da, a):
    """### La pendenza dei minimi quadrati di `L(k)` contro `t` sui campioni in `[da, a]`."""
    sel = [i for i, t in enumerate(tt) if da - 1e-12 <= t <= a + 1e-12]
    t = np.asarray([tt[i] for i in sel])
    y = np.stack([LL[i] for i in sel])
    tm = t - t.mean()
    return np.tensordot(tm, y - y.mean(axis=0), axes=(0, 0)) / float(np.sum(tm ** 2))


def braccio_proiettato(nome, lato, dtau, x, acceso, salta, eps_rel, tempo):
    import flussi_parziali as FP
    inc, mot, st, par = scena(lato, dtau, x)
    n = inc.n
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    lc = RAPPORTO * lm
    cs_m = lm / (lm + lc) if acceso else 1.0
    if acceso:
        FP.accendi_cs(mot, lc, st)
    N = int(round(tempo / dtau))
    assert N % 4 == 0, "N = %d non si divide in quattro quarti" % N
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    fuori = {"nome": nome, "lato": lato, "dtau": dtau, "x": x, "acceso": acceso,
             "salta": list(salta), "eps_rel": eps_rel, "N": N, "cs_m": cs_m,
             "rho_m": rm, "lambda_m": lm, "fine": "N", "proiettata": True}
    M = np.broadcast_to(np.eye(2 * NC, dtype=complex), (lato, lato, 2 * NC, 2 * NC)).copy()
    acc = np.zeros((lato, lato))
    zero = np.zeros((lato, lato))
    tt, Le, Ln, Lq = [0.0], [zero], [zero], {}
    unif = uniformita(st, n)
    t0 = time.time()
    base = st
    for t in range(1, N + 1):
        R, dopo = green(base, mot, par, acceso, salta, lc, lato, scale, eps_rel)
        unif = max(unif, uniformita(dopo, n))
        proietta(dopo, n)
        M = np.matmul(R, M)
        s = np.sqrt(np.sum(np.abs(M) ** 2, axis=(-2, -1)))
        M /= s[..., None, None]
        acc += np.log(s)
        base = dopo
        if t % OGNI == 0 or t % (N // 4) == 0:
            le = acc + np.log(np.max(np.abs(np.linalg.eigvals(M)), axis=-1))
            tt.append(t * dtau * cs_m)
            Le.append(le)
            Ln.append(acc.copy())
            if t % (N // 4) == 0:
                Lq[t // (N // 4)] = le
        if time.time() - t0 > BUDGET_LUNGO:
            fuori["fine"] = "BUDGET superato al passo %d di %d" % (t, N)
            break
    fuori["secondi"] = time.time() - t0
    fuori["uniformita_ulp"] = unif
    fuori["nu_s3"] = lm ** 2 / (rm + lm) ** 2
    if fuori["fine"] != "N":
        return fuori
    T = N * dtau * cs_m
    tq = T / 4.0
    fuori["gamma"] = Lq[4] / T
    fuori["gamma_meta"] = Lq[2] / (T / 2.0)
    fuori["quarti"] = [(Lq[q] - (Lq[q - 1] if q > 1 else 0.0)) / tq for q in (1, 2, 3, 4)]
    fuori["pend"] = {"meta_eig": pendenze(tt, Le, T / 2.0, T),
                     "meta_norm": pendenze(tt, Ln, T / 2.0, T),
                     "q4_eig": pendenze(tt, Le, 3.0 * T / 4.0, T),
                     "q4_norm": pendenze(tt, Ln, 3.0 * T / 4.0, T)}
    h = lato // 2
    fuori["serie"] = {"t": tt,
                      "(pi,pi)": [[float(a[h, h]) for a in Le], [float(a[h, h]) for a in Ln]],
                      "k=0": [[float(a[0, 0]) for a in Le], [float(a[0, 0]) for a in Ln]]}
    return fuori


def leggi_proiettata(b):
    lato = b["lato"]
    p = {k: np.asarray(v) for k, v in b["pend"].items()}
    sm = p["meta_eig"]
    mx = float(np.max(sm))
    h = lato // 2
    kb = punto_banda(sm, lato)
    punti = (("(pi,pi)", (h, h)), ("banda", kb), ("k=0", (0, 0)))
    print("      LE PENDENZE (tempo proprio): il massimo della seconda meta' %+.4e" % mx)
    print("      %-8s %-22s %-11s %-11s %-11s %-11s  %s"
          % ("punto", "k", "meta' eig", "meta' norma", "q4 eig", "q4 norma", "etichetta"))
    et = {}
    for nome, (kx, ky) in punti:
        v = {k: float(a[kx, ky]) for k, a in p.items()}
        asin = (abs(v["meta_eig"] - v["q4_eig"]) <= SOGLIA_5 * mx
                and abs(v["meta_eig"] - v["meta_norm"]) <= SOGLIA_5 * mx)
        et[nome] = {"k": [int(kx), int(ky)], "pendenze": v, "asintotico": bool(asin)}
        print("      %-8s (%d,%d)=(%.3f,%.3f)pi %+.4e %+.4e %+.4e %+.4e  %s"
              % (nome, kx, ky, fase_pi(kx, lato), fase_pi(ky, lato), v["meta_eig"],
                 v["meta_norm"], v["q4_eig"], v["q4_norm"],
                 "ASINTOTICO" if asin else "NON ASINTOTICO"))
    a, c = et["(pi,pi)"]["pendenze"]["meta_eig"], et["banda"]["pendenze"]["meta_eig"]
    if abs(a - c) < SOGLIA_5 * mx:
        vince = "NON DECIDIBILE"
    else:
        vince = "IL PICCO a (pi,pi)" if a > c else "LA BANDA"
    print("      CHI VINCE (pendenza della seconda meta'): %s  (picco %+.4e, banda %+.4e,"
          " differenza %.3e contro %.3e)" % (vince, a, c, abs(a - c), SOGLIA_5 * mx))
    z, zq = et["k=0"]["pendenze"]["meta_eig"], et["k=0"]["pendenze"]["q4_eig"]
    vera = z > 0.02 and zq >= 0.5 * z
    print("      k = 0: seconda meta' %+.4e, ultimo quarto %+.4e -> %s"
          % (z, zq, "CRESCITA VERA" if vera else
             "TRANSITORIO: la frase <<nessuna lunghezza minima>> si RITIRA"))
    diag = [float(sm[h - d, h - d]) for d in (4, 3, 2, 1, 0)]
    sl = semi_larghezza(sm, lato)
    print("      la diagonale negli ultimi 4 m prima di pi (m = %d..%d): %s;  semi-larghezza %s"
          % (h - 4, h, " ".join("%+.4e" % w for w in diag), sl if sl else "> 4"))
    passo_ = max(1, lato // 16)
    print("      la pendenza della seconda meta' lungo (m,0), m = 0,%d,..: %s" % (passo_, " ".join(
        "%+.3f" % float(sm[m, 0]) for m in range(0, h + 1, passo_))))
    print("      la pendenza della seconda meta' lungo (m,m), m = 0,%d,..: %s" % (passo_, " ".join(
        "%+.3f" % float(sm[m, m]) for m in range(0, h + 1, passo_))))
    q = [float(np.asarray(qq)[h, h]) for qq in b["quarti"]]
    print("      INFORMAZIONE, i quattro quarti alla vecchia a (pi,pi): %s"
          % " ".join("%+.4e" % w for w in q))
    sys.stdout.flush()
    return {"punti": et, "vince": vince, "k0_vera": bool(vera), "diagonale": diag,
            "semi_larghezza": sl, "quarti_pipi": q}


def salva_proiettata(b, et):
    d = {}
    for k, v in b.items():
        if k in ("gamma", "gamma_meta"):
            d[k] = np.asarray(v).tolist()
        elif k == "quarti":
            d[k] = [np.asarray(w).tolist() for w in v]
        elif k == "pend":
            d[k] = {kk: np.asarray(w).tolist() for kk, w in v.items()}
        else:
            d[k] = v
    d["etichette"] = et
    with io.open(JSONL_PROIETTATA, "a", encoding="utf-8") as f:
        f.write(json.dumps(d) + "\n")


def lungo_jsonl(nome):
    with io.open(JSONL_LUNGO, encoding="utf-8") as f:
        for riga in f:
            b = json.loads(riga)
            if b["nome"] == nome:
                return b
    raise AssertionError("il braccio `%s` non e' nel jsonl di 16b5d10f" % nome)


def prova_p3(acceso):
    """### `(ulp, al_bit)`: la base dopo un tick con `mot` sporcato da un tick PERTURBATO."""
    import flussi_parziali as FP
    inc, mot, st, par = scena(31, 0.125, X)
    lc = float(np.mean(mot.densita_vuoto(st)))
    if acceso:
        FP.accendi_cs(mot, lc, st)
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    peggio, al_bit = 0.0, True
    for j in (0, 5, 13, 20):
        p = copia(st)
        perturba(p, j, EPS_REL * scale[0 if (j % NC) < 8 else 1])
        passo(p, mot, par, acceso, (), lc)
        a = copia(st)
        passo(a, mot, par, acceso, (), lc)
        q = copia(st)
        passo(q, mot, par, acceso, (), lc)
        c = copia(st)
        passo(c, mot, par, acceso, (), lc)
        for k in ("psi_h", "phi_h"):
            d = float(np.max(np.abs(a[k] - c[k])))
            al_bit &= bool(np.array_equal(a[k], c[k]))
            peggio = max(peggio, d / (EPS * float(np.max(np.abs(c[k])))))
    return peggio, al_bit


def main_proiettata(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    import statica_protocollo as PR
    print("=" * 100)
    print("L'INTERVALLO LUNGO CON LA BASE PROIETTATA E GAMMA COME PENDENZA -- un conto")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la materia uniforme: x %g, VUOTO %.1f, rapporto %g, chi_allineato; la cella: 24 reali"
          % (X, PR.VUOTO, RAPPORTO))
    print("  il passo: %d pezzi, impronta %s; lati 32 (dtau 0.125) e 64 (dtau 0.0625);"
          " N dtau = %g; la BASE PROIETTATA sulla media delle celle dopo ogni tick;"
          " la monodromia rinormalizzata per k" % (len(CM.ORDINE), CM.IMPRONTA, TEMPO_LUNGO))
    print("  gamma = la PENDENZA (minimi quadrati, tempo proprio) di ln|lambda| e ln||M||, campioni"
          " ogni %d tick, sulla seconda meta' e sull'ultimo quarto" % OGNI)
    print("  soglie: base valida <= %g ulp (prima della proiezione); 5%% del massimo; previsione"
          " %g; P3 %g ulp; linearita' %g; budget %.0f s" % (SOGLIA_UNIF, PREV_GUARDIANO, ULP_P3,
                                                            BANDA_LIN, BUDGET_LUNGO))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL_PROIETTATA, "w", encoding="utf-8").close()

    print("### I CASI DI CONTROLLO")
    vecchio = vecchio_jsonl("R2 (a) S3 sola")
    b = braccio("R2 (a) S3 sola", 31, 0.125, X, False, (), EPS_REL)
    if not esito("il conto di c38367db (senza argomenti) AL BIT: R2 a lato 31",
                 np.array_equal(np.asarray(b["gamma"]), np.asarray(vecchio["gamma"]))):
        print("### STOP: lo strumento non riproduce c38367db")
        return 1
    lu = lungo_jsonl("R2 lato 32")
    b = braccio_lungo("R2 lato 32", 32, 0.125, X, False, (), EPS_REL)
    bit = all(np.array_equal(np.asarray(x_), np.asarray(y_)) for x_, y_ in zip(b["L"], lu["L"]))
    if not esito("--lungo (16b5d10f) AL BIT: R2 lato 32, i quattro L", bit):
        print("### STOP: lo strumento non riproduce 16b5d10f")
        return 1
    if not esito("DEVE FALLIRE: la proiezione SPENTA, R2 lato 32, N dtau 100: uniformita' > %g ulp"
                 % SOGLIA_UNIF, b["uniformita_ulp"] > SOGLIA_UNIF,
                 "%.3e ulp" % b["uniformita_ulp"]):
        print("### STOP: la proiezione non e' cio' che tiene la base")
        return 1
    c2 = c2_esatto_lungo(32, 0.125)
    tetto = c2["N"] * ULP_C2 * EPS
    if not esito("DEVE FALLIRE: la camminata sola esatta, lato 32, N dtau 100: <= N*64 ulp",
                 c2["dev"] <= tetto, "%.3e contro %.3e" % (c2["dev"], tetto)):
        print("### STOP: il metodo e' rotto")
        return 1
    for acceso in (True, False):
        u, bit = prova_p3(acceso)
        if not esito("P3 cs %s: la base dopo un tick perturbato = dopo un tick della base"
                     % ("acceso" if acceso else "spento"), bit or u <= ULP_P3,
                     "%s, %.1f ulp" % ("AL BIT" if bit else "non al bit", u)):
            print("### STOP: la funzione di Green ha una memoria in `mot`")
            return 1
    ok = True
    for nome, vnome, acceso in (("R1", "R1 (b)", True), ("R2", "R2 (a) S3 sola", False)):
        b = braccio_proiettato("%s lato 31 N dtau 25" % nome, 31, 0.125, X, acceso, (),
                               EPS_REL, TEMPO_N)
        g, gv = np.asarray(b["gamma"]), np.asarray(vecchio_jsonl(vnome)["gamma"])
        d = float(np.max(np.abs(g - gv)))
        ok &= esito("DEVE RIUSCIRE: %s proiettato, lato 31, N dtau 25 = c38367db entro 1e-3 max"
                    % nome, d <= 1e-3 * float(np.max(gv)),
                    "%.3e contro %.3e; uniformita' %.1f ulp" % (d, 1e-3 * float(np.max(gv)),
                                                               b["uniformita_ulp"]))
    b = braccio_proiettato("R2 lato 32 N dtau 25", 32, 0.125, X, False, (), EPS_REL, TEMPO_N)
    g = np.asarray(b["gamma"])
    T = b["N"] * b["dtau"]
    g2 = (g * T - np.asarray(b["gamma_meta"]) * T / 2.0) / (T / 2.0)
    for che, arr, (val, kk) in (("intero", g, GUARDIANO["intero"]),
                                ("seconda meta'", g2, GUARDIANO["meta"])):
        i, j = np.unravel_index(int(np.argmax(arr)), arr.shape)
        ok &= esito("DEVE RIUSCIRE: R2 proiettato lato 32, N dtau 25, %s: %.4f a (%d,%d)"
                    " contro %.4f a %s" % (che, float(arr[i, j]), kpi(i, 32)[0], kpi(j, 32)[0],
                                          val, kk),
                    abs(float(arr[i, j]) - val) <= GUARDIANO["banda"]
                    and (i, j) in simmetrici(kk, 32))
    if not ok:
        print("### STOP: la base proiettata non riproduce i conti di controllo")
        return 1
    print("-" * 100)

    risultati = {}
    for lato, dtau in ((32, 0.125), (64, 0.0625)):
        for nome, acceso in (("R1", True), ("R2", False)):
            b = braccio_proiettato("%s lato %d" % (nome, lato), lato, dtau, X, acceso, (),
                                   EPS_REL, TEMPO_LUNGO)
            if b["fine"] != "N":
                salva_proiettata(b, None)
                print("  %s lato %d: %s -- ### STOP: si dichiara e ci si ferma"
                      % (nome, lato, b["fine"]))
                return 1
            sommario(b)
            if not esito("BASE VALIDA %s lato %d: uniformita' <= %g ulp per tutto l'intervallo"
                         % (nome, lato, SOGLIA_UNIF), b["uniformita_ulp"] <= SOGLIA_UNIF,
                         "%.1f ulp" % b["uniformita_ulp"]):
                salva_proiettata(b, None)
                print("### STOP: il braccio NON VALE")
                return 1
            et = leggi_proiettata(b)
            salva_proiettata(b, et)
            risultati[(nome, lato)] = et
            if nome == "R1":
                v = lungo_jsonl("R1 lato %d" % lato)["etichette"]["punti"]["(pi,pi)"]["quarti"]
                d = max(abs(a_ - c_) for a_, c_ in zip(et["quarti_pipi"], v))
                esito("LA PREVISIONE DEL GUARDIANO, R1 lato %d: i quarti a (pi,pi) = 16b5d10f"
                      " entro %g" % (lato, PREV_GUARDIANO), d <= PREV_GUARDIANO,
                      "16b5d10f %s; differenza massima %.3e"
                      % (" ".join("%.4f" % w for w in v), d))
            if lato == 32:
                b2 = braccio_proiettato("%s lato 32 eps 1e-6" % nome, lato, dtau, X, acceso, (),
                                        EPS_REL_2, TEMPO_LUNGO)
                if b2["fine"] != "N":
                    print("  linearita' %s: %s -- ### STOP" % (nome, b2["fine"]))
                    return 1
                p1 = np.asarray(b["pend"]["meta_eig"])
                p2 = np.asarray(b2["pend"]["meta_eig"])
                d = float(np.max(np.abs(p1 - p2)))
                salva_proiettata(b2, None)
                if not esito("linearita' %s lato 32: la pendenza della seconda meta', 1e-7"
                             " contro 1e-6, <= %g max" % (nome, BANDA_LIN),
                             d <= BANDA_LIN * float(np.max(p1)),
                             "%.3e contro %.3e" % (d, BANDA_LIN * float(np.max(p1)))):
                    print("### STOP: il conto non e' lineare in eps")
                    return 1
    print("-" * 100)
    print("### LA LARGHEZZA DEL PICCO a (pi,pi): semi-larghezza in m (NUMERO DI ARCHI)")
    for nome in ("R1", "R2"):
        a, c = risultati[(nome, 32)]["semi_larghezza"], risultati[(nome, 64)]["semi_larghezza"]
        if a is None or c is None:
            v = "non misurabile entro 4 m"
        else:
            griglia, segue_k = abs(c - a) <= 1, abs(c - 2 * a) <= 1
            v = ("NON SEPARABILE (entrambe)" if griglia and segue_k else
                 "SEGUE LA GRIGLIA" if griglia else "SEGUE k" if segue_k else
                 "ne' l'una ne' l'altra")
        print("  %s: lato 32 %s, lato 64 %s -> %s" % (nome, a, c, v))
    print("=" * 100)
    print("### %d/%d prove passate. NESSUNA CURA. LINEARE e Lambda_c FERMI; D4 da rileggere."
          % tuple(OK))
    print("=" * 100)
    return 0


# =====================================================================================
#   D0: LA RISONANZA  (mandato di Luca del 2026-10-21, 09:22)
#   ### task history `2026-10-21_d0_risonanza.md` (`605f006b`), con la LISTA CHIUSA delle
#   ### condizioni scritta prima dei numeri. ### ⛔ **SI AGGIUNGE, non si riscrive:** i modi
#   ### di prima restano, e le prove li rifanno AL BIT.
# =====================================================================================
LATO_D0 = 32
DTAU_D0 = 0.125
XX_D0 = (0.01, 0.1, 1.0)
PESO_POMPA = 1e-6              # il peso minimo di una fase della pompa, dal task history
TOLL_PASSI = 1.0               # la distanza massima in passi di k, dal mandato
JSONL_D0 = os.path.join(RADICE, "doc", "referti_l2", "d0_risonanza.jsonl")
CONDIZIONI = (("K1", "interbanda", 1), ("K2", "interbanda", 2), ("K3", "laterali", 1),
              ("K4", "laterali", 2), ("K5", "laterali", 0), ("K6", "precessione", None))


def camminata_complessa(lato, dtau):
    """### `A(k)` `(L, L, 12, 12)` della camminata sola, ESATTA, e la prova di linearita' complessa."""
    inc, mot, st, par = scena(lato, dtau, X)
    n = inc.n
    for k in st:
        st[k][...] = 0
    zero = copia(st)
    passo(zero, mot, par, False, (S3,), 0.0)
    A = np.empty((lato, lato, NC, NC), dtype=complex)
    peggio = 0.0
    for c in range(NC):
        p = copia(st)
        perturba(p, c, 1.0)
        passo(p, mot, par, False, (S3,), 0.0)
        r = celle(p, n)
        z = r[:, :NC] + 1j * r[:, NC:]
        A[:, :, :, c] = np.fft.fft2(z.reshape(lato, lato, NC), axes=(0, 1))
        q = copia(st)
        perturba(q, c + NC, 1.0)
        passo(q, mot, par, False, (S3,), 0.0)
        r2 = celle(q, n)
        z2 = r2[:, :NC] + 1j * r2[:, NC:]
        peggio = max(peggio, float(np.max(np.abs(z2 - 1j * z))))
    return A, peggio


def fasi(B, dtau):
    """### `omega` in `(-pi/dtau, pi/dtau]`, ordinate, e lo scarto massimo di `|lambda|` da `1`."""
    lam = np.linalg.eigvals(B)
    om = -np.angle(lam) / dtau
    return np.sort(om, axis=-1), float(np.max(np.abs(np.abs(lam) - 1.0)))


def pompa(dtau):
    """### Le fasi `k = 0` della MATERIA occupate dallo stato uniforme, coi pesi."""
    inc, mot, st, par = scena(LATO_D0, dtau, X)
    A, _ = camminata_complessa(LATO_D0, dtau)
    Am = A[0, 0][:8, :8]
    lam, V = np.linalg.eig(Am)
    c = celle(st, inc.n)[0]
    z0 = (c[:NC] + 1j * c[NC:])[:8]
    coef = np.linalg.solve(V, z0)
    w = np.abs(coef) ** 2 / float(np.sum(np.abs(coef) ** 2))
    om = -np.angle(lam) / dtau
    tenute = [(float(o), float(p)) for o, p in zip(om, w) if p > PESO_POMPA]
    return tenute


def avvolgi(r, dtau):
    m = np.pi / dtau
    return (r + m) % (2 * m) - m


def residui(nome, om_k, om_mk, Om, nu, dtau):
    """### `(m, combinazioni)`: i residui di una condizione lungo una retta (`om_*` `(M, 12)`)."""
    _n, tipo, molt = [c for c in CONDIZIONI if c[0] == nome][0]
    M = om_k.shape[0]
    out = []
    if tipo == "interbanda":
        d = om_k[:, :, None] - om_k[:, None, :]
        iu = ~np.eye(NC, dtype=bool)
        d = d[:, iu]
        for s in (1, -1):
            out.append(d - s * molt * nu)
    elif tipo == "laterali":
        sm = om_k[:, :, None] + om_mk[:, None, :]
        sm = sm.reshape(M, -1)
        pp = np.array([a + b for a in Om for b in Om])
        base = sm[:, :, None] - pp[None, None, :]
        base = base.reshape(M, -1)
        for s in ((1, -1) if molt else (0,)):
            out.append(base - s * molt * nu)
    else:
        d = om_k[:, :, None] - om_k[:, None, :]
        iu = ~np.eye(NC, dtype=bool)
        d = d[:, iu]
        pr = np.array([a - b for a in Om for b in Om if a != b] or [0.0])
        base = (d[:, :, None] - pr[None, None, :]).reshape(M, -1)
        out.append(base)
    return avvolgi(np.concatenate(out, axis=1), dtau)


def incroci(R, dtau):
    """### Gli `m` (interpolati) dove un residuo cambia segno, senza il salto di `2 pi / dtau`."""
    a, b = R[:-1], R[1:]
    ok = (a * b <= 0) & (np.abs(a) + np.abs(b) < np.pi / dtau)
    mi, ci = np.nonzero(ok)
    fr = np.where(np.abs(a[mi, ci] - b[mi, ci]) > 0,
                  np.abs(a[mi, ci]) / np.abs(a[mi, ci] - b[mi, ci] + 1e-300), 0.0)
    return np.unique(np.round(mi + fr, 6))


def distanza(nome, rette, gm, nu, Om, dtau):
    """### Per ogni retta: `(m del massimo, incrocio piu' vicino, distanza in passi)`."""
    fuori = {}
    for rn, (om_k, om_mk) in rette.items():
        g = gm[rn]
        mmax = 1 + int(np.argmax(g[1:]))
        cr = incroci(residui(nome, om_k, om_mk, Om, nu, dtau), dtau)
        if len(cr) == 0:
            fuori[rn] = (mmax, None, float("inf"))
        else:
            j = int(np.argmin(np.abs(cr - mmax)))
            fuori[rn] = (mmax, float(cr[j]), float(abs(cr[j] - mmax)))
    return fuori


def main_risonanza(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    L, dt = LATO_D0, DTAU_D0
    h = L // 2
    print("=" * 100)
    print("D0: LA BANDA DI S3 E' UNA RISONANZA FRA LA CAMMINATA E IL RITMO DI S3? -- una diagnosi")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  il passo: %d pezzi, impronta %s; lato %d, dtau %g; R2 (S3 sola, cs spento) con la base"
          " proiettata, N dtau %g, x in %s" % (len(CM.ORDINE), CM.IMPRONTA, L, dt, TEMPO_LUNGO,
                                               XX_D0))
    print("  la dispersione: la camminata sola ESATTA, A(k) 12x12 complessa, omega in (-pi/dtau,"
          " pi/dtau], rami ordinati, materia (8) e vuoto (4) separati")
    print("  gamma(k): la pendenza della seconda meta', stimatore della NORMA; le rette (m,0) e (m,m),"
          " m = 1..%d; la tolleranza %g passo di k (pi/%d)" % (h, TOLL_PASSI, h))
    print("  la lista CHIUSA: %s" % ", ".join("%s %s%s" % (c[0], c[1], "" if c[2] is None else
                                                         " x%d nu" % c[2]) for c in CONDIZIONI))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL_D0, "w", encoding="utf-8").close()

    print("### I CASI DI CONTROLLO E LE PROVE")
    vecchio = vecchio_jsonl("R2 (a) S3 sola")
    b = braccio("R2 (a) S3 sola", 31, 0.125, X, False, (), EPS_REL)
    if not esito("il conto di c38367db (senza argomenti) AL BIT: R2 a lato 31",
                 np.array_equal(np.asarray(b["gamma"]), np.asarray(vecchio["gamma"]))):
        return 1
    lu = lungo_jsonl("R2 lato 32")
    b = braccio_lungo("R2 lato 32", 32, 0.125, X, False, (), EPS_REL)
    if not esito("--lungo (16b5d10f) AL BIT: R2 lato 32, i quattro L",
                 all(np.array_equal(np.asarray(x_), np.asarray(y_))
                     for x_, y_ in zip(b["L"], lu["L"]))):
        return 1
    A, lin = camminata_complessa(L, dt)
    om_m, dev_m = fasi(A[..., :8, :8], dt)
    om_v, dev_v = fasi(A[..., 8:, 8:], dt)
    fuori_blocco = float(max(np.max(np.abs(A[..., :8, 8:])), np.max(np.abs(A[..., 8:, :8]))))
    if not esito("la camminata sola e' LINEARE IN SENSO COMPLESSO: risposta(i e) = i risposta(e)",
                 lin <= 64 * EPS, "%.3e" % lin):
        return 1
    if not esito("i suoi autovalori hanno modulo 1 (materia e vuoto)",
                 max(dev_m, dev_v) <= 64 * EPS, "%.3e, %.3e" % (dev_m, dev_v)):
        return 1
    esito("psi e phi NON si mescolano nella camminata sola (i blocchi fuori diagonale)",
          fuori_blocco <= 64 * EPS, "%.3e" % fuori_blocco)
    om = np.concatenate([om_m, om_v], axis=-1)
    om = np.sort(om, axis=-1)
    Om_t = pompa(dt)
    Om = [o for o, _w in Om_t]
    print("  LA POMPA (le fasi k = 0 della materia occupate dallo stato uniforme, peso > %g): %s"
          % (PESO_POMPA, "; ".join("omega %+.6f peso %.6f" % (o, w) for o, w in Om_t)))
    if len(Om) > 1:
        print("  la precessione (differenze): %s" % " ".join(
            "%+.6f" % (a - c) for a in Om for c in Om if a > c))
    proj = lungo_jsonl  # (solo per non confondere i nomi qui sotto)
    _ = proj
    pr_vecchio = None
    with io.open(JSONL_PROIETTATA, encoding="utf-8") as f:
        for riga in f:
            q = json.loads(riga)
            if q["nome"] == "R2 lato 32":
                pr_vecchio = q
    gm, nus = {}, {}
    for x in XX_D0:
        b = braccio_proiettato("R2 lato 32 x %g" % x, L, dt, x, False, (), EPS_REL, TEMPO_LUNGO)
        if b["fine"] != "N":
            print("  ### STOP: %s" % b["fine"])
            return 1
        nus[x] = b["nu_s3"]
        pn = np.asarray(b["pend"]["meta_norm"])
        gm[x] = {"(m,0)": [float(pn[m, 0]) for m in range(h + 1)],
                 "(m,m)": [float(pn[m, m]) for m in range(h + 1)]}
        if x == 0.1:
            d = max(float(np.max(np.abs(np.asarray(b["pend"][k_]) -
                                        np.asarray(pr_vecchio["pend"][k_]))))
                    for k_ in ("meta_eig", "meta_norm"))
            if not esito("DEVE RIUSCIRE: R2 x 0.1 = 594417f6 entro 1e-3 su ogni k, due stimatori",
                         d <= 1e-3, "%.3e" % d):
                return 1
        print("  R2 x %-5g  nu_S3 %.6f  uniformita' %.1f ulp  [%.0f s]"
              % (x, nus[x], b["uniformita_ulp"], b["secondi"]))
        sys.stdout.flush()
    print("-" * 100)

    print("### LA DISPERSIONE DELLA CAMMINATA, omega_a(k) (in 1/tempo), lungo le rette")
    rette = {}
    for rn, idx in (("(m,0)", lambda m: (m % L, 0)), ("(m,m)", lambda m: (m % L, m % L))):
        ok = np.array([om[idx(m)] for m in range(h + 1)])
        omk = np.array([om[idx(-m)] for m in range(h + 1)])
        rette[rn] = (ok, omk)
        print("  %s:" % rn)
        for m in range(0, h + 1, 2):
            print("     m %2d  %s" % (m, " ".join("%+.3f" % v for v in ok[m])))
    print("### gamma(k) di R2 (pendenza della seconda meta', norma), lungo le rette")
    for x in XX_D0:
        for rn in ("(m,0)", "(m,m)"):
            g = gm[x][rn]
            mm = 1 + int(np.argmax(g[1:]))
            print("  x %-5g %s  massimo a m = %2d (%.3f pi) %+.4f;  %s"
                  % (x, rn, mm, 2.0 * mm / L, g[mm], " ".join("%+.3f" % v for v in g)))
    print("-" * 100)

    print("### LE CONDIZIONI: il m del massimo, l'incrocio piu' vicino, la distanza (passi di k)")
    tengono = []
    risultati = {}
    for nome, _t, _mo in CONDIZIONI:
        tutte = True
        righe = []
        for x in XX_D0:
            dd = distanza(nome, rette, {rn: gm[x][rn] for rn in rette}, nus[x], Om, dt)
            for rn, (mm, cr, di) in dd.items():
                righe.append("x %-5g %s max %2d incrocio %s dist %s"
                             % (x, rn, mm, "%.2f" % cr if cr is not None else "-",
                                "%.2f" % di if di != float("inf") else "inf"))
                tutte &= di <= TOLL_PASSI
            risultati[(nome, x)] = dd
        print("  %s  %s" % (nome, "TIENE" if tutte else "non tiene"))
        for r_ in righe:
            print("       %s" % r_)
        if tutte:
            tengono.append(nome)
    print("-" * 100)
    print("### IL CASO PERMUTATO (deve fallire), per ogni condizione che tiene")
    troppo_larga = []
    for nome in tengono:
        for perm in ((XX_D0[2], XX_D0[0], XX_D0[1]), (XX_D0[1], XX_D0[2], XX_D0[0])):
            tutte = True
            for x, xp in zip(XX_D0, perm):
                dd = distanza(nome, rette, {rn: gm[x][rn] for rn in rette}, nus[xp], Om, dt)
                tutte &= all(di <= TOLL_PASSI for (_m, _c, di) in dd.values())
            esito("DEVE FALLIRE: %s col nu permutato %s" % (nome, perm), not tutte)
            if tutte:
                troppo_larga.append(nome)
    print("=" * 100)
    if troppo_larga:
        v = "STOP: il criterio e' TROPPO LARGO (%s tiene anche col nu permutato)" % troppo_larga
    elif len(tengono) == 1:
        v = "D0 TIENE: la condizione %s" % tengono[0]
    elif not tengono:
        v = "D0 CADE: nessuna condizione della lista tiene"
    else:
        v = "NON DECIDIBILE: tengono %s" % tengono
    print("### IL VERDETTO: %s" % v)
    with io.open(JSONL_D0, "a", encoding="utf-8") as f:
        f.write(json.dumps({"pompa": Om_t, "nu": {str(k_): v_ for k_, v_ in nus.items()},
                            "omega": {rn: [r.tolist() for r in rette[rn]] for rn in rette},
                            "gamma": {str(k_): v_ for k_, v_ in gm.items()},
                            "distanze": {"%s %s" % k_: {rn: list(v_) for rn, v_ in d_.items()}
                                         for k_, d_ in risultati.items()},
                            "tengono": tengono, "troppo_larga": troppo_larga,
                            "verdetto": v}) + "\n")
    print("### %d/%d prove passate. NESSUNA CURA SCELTA." % tuple(OK))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--lungo"]:
        sys.exit(main_lungo(sys.argv[2:]))
    if sys.argv[1:2] == ["--proiettata"]:
        sys.exit(main_proiettata(sys.argv[2:]))
    if sys.argv[1:2] == ["--risonanza"]:
        sys.exit(main_risonanza(sys.argv[2:]))
    sys.exit(main(sys.argv[1:]))
