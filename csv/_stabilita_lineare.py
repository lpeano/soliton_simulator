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

Gira con:  python csv/_stabilita_lineare.py
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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
