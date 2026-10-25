# -*- coding: utf-8 -*-
r"""**LA CURVATURA, PARTE 0-BIS: la velocita' della luce in `A1` MISURATA, e la velocita' massima VERA della materia a `r != 1`** *([[PROGETTO-CURVATURA]], [[LORENTZ-MATERIA-INTERFERENZA]],
[[DECISIONE-SOLO-TRIANGOLI]])*.

> ### ⛔ **Il task history e' `2026-10-25_curvatura_0bis.md`** *(`8288068d`)*. ### **Nessun file del nucleo; `B-4` intatta.**
> ### **Importati, non copiati:** `_curvatura_prototipo` *(`CampoA1`, `a1`, `coppia_r`, `x_di`, `H_r`, `mu_di`)*, `_u1_terzo` *(`dH_gen`)*, `_u1_prototipo` *(`blocchi_campo`, `omega_fotone`, `t_di`, `max_instabile`,
> `corsa_pacchetto`)*, `_triangoli_forza` *(`v_max`, `matrice_L`, `theta_di`)*, `_triangoli_bassa_energia.J`.
> ### **`CampoA1` entra negli strumenti del campo avvolgendo `_u1_prototipo.campo_toro`** *(in un `with`; il tempo del campo resta `F1`, la `s` vera)*.

Gira con:  python csv/_curvatura_0bis.py > doc/referti_l2/curvatura_0bis.txt
"""
import contextlib
import io
import json
import math
import os
import sys
import time
import warnings
from collections import deque

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402
import _curvatura_prototipo as CP                              # noqa: E402
import _u1_prototipo as U                                      # noqa: E402
import _u1_terzo as U3                                         # noqa: E402

R_LISTA = (0.5, 0.8, 1.0, 1.25, 2.0)
R_SPETTRI = (0.5, 1.0, 2.0)
S_LUCE = 0.05
S_SPETTRI = 0.01
GRIGLIE = (48, 96, 192)
K_PICCOLO = U.K_PICCOLO
H_K = U.H_K
DIREZIONI_V = U.DIREZIONI_V
VMAX_1 = 0.599286                 # ### il valore del guardiano (l'ottimizzatore), scritto PRIMA di questa corsa; il vecchio 0.598467 e' la sottostima di _triangoli_forza.v_max
VMAX_1_VECCHIO = 0.598467
STIME = {0.5: 0.382103, 2.0: 0.764206}
TOLL_STIME = 1e-5
N_GRIGLIA_OTT = 120
R_DIREZIONI = (0.8, 1.0, 1.25)
DIREZIONI_ARCHI = (0.0, 120.0, 60.0, 30.0)   # ### le tre direzioni degli archi e la normale ad a2
TOLL_DIR = 1e-3
QUOTE = (0.0, 0.25, 0.5)                    # ### m1/L1: cs = 0.24, 0.20, 0.16 nella scena di 31ee70cc
W_A2 = 8.0
T_A2 = 80
ESP_LUNGO = 2.0245                           # ### d ln v/d ln cs lungo il gradiente, 31ee70cc
TOLL_ESP = 0.05
TOLL_C1 = 1e-3
TOLL_VMAX1 = 1e-5
TOLL_X1 = 1e-9
TOLL_CR = 1e-3
JSONL = os.path.join(RADICE, "doc", "referti_l2", "curvatura_0bis_v2.jsonl")   # ### la seconda corsa (la correzione del guardiano dopo 52eba072): la prima resta in curvatura_0bis.*
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-100s %s   %s" % (che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


@contextlib.contextmanager
def campo_a1(r):
    """### **`_u1_prototipo.campo_toro` avvolta:** ### **il campo `CampoA1` con `s_rif = s/r`** *(quindi `l = 1/r` per arco)*."""
    vero = U.campo_toro

    def campo_toro(lati, s, e, forma):
        import _triangoli as T
        ii, jj, nn = T.toro_spostamenti(lati, T.TRIANGOLI[0])
        return CP.CampoA1(ii, jj, lati, e, forma, np.full(len(ii), float(s)), float(s) / r)
    U.campo_toro = campo_toro
    try:
        yield
    finally:
        U.campo_toro = vero


def luce(r):
    """### **`M1`:** ### **la dispersione** *(`v_g/s` a `|k| = K_PICCOLO`, `12` direzioni)*, ### **il pacchetto** *(`corsa_pacchetto`, contro la previsione dallo spettro)*, ### **Courant** *(`max|lambda|` fuori dalla gauge, `48 x 48`)*."""
    s = S_LUCE
    with campo_a1(r):
        bl, fuori, ricostr = U.blocchi_campo(s)
        vg = []
        for k in range(DIREZIONI_V):
            a = np.pi * k / DIREZIONI_V
            wp = U.omega_fotone(bl, *U.t_di((K_PICCOLO + H_K) * math.cos(a), (K_PICCOLO + H_K) * math.sin(a)))
            wm = U.omega_fotone(bl, *U.t_di((K_PICCOLO - H_K) * math.cos(a), (K_PICCOLO - H_K) * math.sin(a)))
            vg.append((wp - wm) / (2 * H_K) / s)
        inst, dove = U.max_instabile(bl, 48)
        pk = U.corsa_pacchetto(s, "noncompatto", 1.0, bl)
    return {"r": r, "s": s, "c_archi": float(np.mean(vg)), "isotropia": float((max(vg) - min(vg)) / np.mean(vg)), "c_propria": float(np.mean(vg)) / r,
            "max_lambda": inst, "k_max": dove, "pacchetto_v": pk["v"], "pacchetto_v_prevista": pk["v_prevista"], "blocchi_fuori": fuori, "ricostruzione": ricostr,
            "courant_carta": 2.0 / (math.sqrt(24.0) * r)}


def grad_mu(t1, t2, r, v):
    d1, d2 = U3.dH_gen(t1, t2)
    g1 = -r * float(np.real(np.vdot(v, d1 @ v)))
    g2 = -r * float(np.real(np.vdot(v, d2 @ v)))
    import _triangoli_bassa_energia as BE
    J = BE.J
    return math.hypot(J[0, 0] * g1 + J[1, 0] * g2, J[0, 1] * g1 + J[1, 1] * g2)


def vmax_banda_K(r, n):
    """### **`M2`: la banda della coppia a `K` SEGUITA PER CONTINUITA' su tutta la griglia `n x n`** *(dal `K`, in ampiezza, per sovrapposizione col vicino gia' assegnato)*; ### **`pi max |grad mu|`.**"""
    out = []
    kK = (n // 3, n // 3)
    for mu0, v0 in CP.coppia_r(r):
        vec = {kK: v0[:, 0]}
        best = grad_mu(2 * np.pi * kK[0] / n, 2 * np.pi * kK[1] / n, r, v0[:, 0])
        q = deque([kK])
        while q:
            i, j = q.popleft()
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = (i + di) % n, (j + dj) % n
                if (a, b) in vec:
                    continue
                t1, t2 = 2 * np.pi * a / n, 2 * np.pi * b / n
                lam, V = np.linalg.eigh(CP.H_r(t1, t2, r))
                jj = int(np.argmax(np.abs(V.conj().T @ vec[(i, j)])))
                vec[(a, b)] = V[:, jj]
                best = max(best, grad_mu(t1, t2, r, V[:, jj]))
                q.append((a, b))
        out.append(np.pi * best)
    return out


def vmax_direzioni(r, n, ndir):
    """### ⭐ **LA DIAGNOSI DEL VALORE DI RIFERIMENTO** *(annotazione `1` del task history, una LETTURA)*: ### **il massimo con la scansione su `ndir` direzioni in `[0, pi]`, come fa `_triangoli_forza.v_max` sui
    gruppi degeneri** *(a `eps 0` ogni banda del tick e' doppia per lo spin)*: ### **`max |g . d|` invece di `|g|`.**"""
    import _triangoli_bassa_energia as BE
    J = BE.J
    dirs = [np.array([math.cos(a), math.sin(a)]) for a in np.linspace(0.0, np.pi, ndir)]
    best = 0.0
    for a in range(n):
        for b in range(n):
            t1, t2 = 2 * np.pi * a / n, 2 * np.pi * b / n
            lam, V = np.linalg.eigh(CP.H_r(t1, t2, r))
            d1, d2 = U3.dH_gen(t1, t2)
            for c in range(6):
                v = V[:, c]
                g1 = -r * float(np.real(np.vdot(v, d1 @ v)))
                g2 = -r * float(np.real(np.vdot(v, d2 @ v)))
                g = np.array([J[0, 0] * g1 + J[1, 0] * g2, J[0, 1] * g1 + J[1, 1] * g2])
                best = max(best, max(abs(float(g @ d)) for d in dirs))
    return np.pi * best


def mu_banda_alta(t1, t2, r):
    """### **La banda ALTA** *(`mu` piu' grande: `+mu0` a `K`, `(1 + r)/2` a `Gamma`)*: ### **isolata** *(il salto con la seconda si misura sulla griglia)*: l'ordinamento non la mescola."""
    mu, V = CP.mu_di(t1, t2, r)
    return mu, V


def vmax_ottimizzato(r):
    """### **Il massimo della banda alta: la griglia `N_GRIGLIA_OTT` e poi Nelder-Mead sul modulo del gradiente** *(la correzione del guardiano)*: ### `pi max |grad mu|`, il punto, il salto minimo."""
    from scipy.optimize import minimize

    def g_di(x):
        mu, V = mu_banda_alta(x[0], x[1], r)
        return grad_mu(x[0], x[1], r, V[:, 0])
    n = N_GRIGLIA_OTT
    best, dove, salto = -1.0, None, 1e9
    for a in range(n):
        for b in range(n):
            x = (2 * np.pi * a / n, 2 * np.pi * b / n)
            mu, V = mu_banda_alta(x[0], x[1], r)
            salto = min(salto, float(mu[0] - mu[1]))
            g = grad_mu(x[0], x[1], r, V[:, 0])
            if g > best:
                best, dove = g, x
    res = minimize(lambda x: -g_di(x), np.array(dove), method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-15, "maxiter": 20000})
    import _triangoli_bassa_energia as BE
    k = np.linalg.inv(BE.J) @ np.array(res.x)
    return {"griglia": np.pi * best, "ottimo": np.pi * float(-res.fun), "t": [float(x) for x in res.x], "k_cart": [float(x) for x in k], "salto_minimo": salto}


def luce_direzioni(r):
    """### **`M1-BIS (i)`:** ### **`v_g/s` a `|k| = K_PICCOLO` nelle tre direzioni degli archi e lungo la normale ad `a2`**, a `cs` uniforme."""
    s = S_LUCE
    out = {}
    with campo_a1(r):
        bl, _, _ = U.blocchi_campo(s)
        for gradi in DIREZIONI_ARCHI:
            a = math.radians(gradi)
            wp = U.omega_fotone(bl, *U.t_di((K_PICCOLO + H_K) * math.cos(a), (K_PICCOLO + H_K) * math.sin(a)))
            wm = U.omega_fotone(bl, *U.t_di((K_PICCOLO - H_K) * math.cos(a), (K_PICCOLO - H_K) * math.sin(a)))
            out[str(gradi)] = (wp - wm) / (2 * H_K) / s
    return out


def luce_lungo_a2():
    """### **`M1-BIS (ii)`:** ### **nella scena del gradiente di `31ee70cc`, un pacchetto LOCALIZZATO** *(largo `W_A2`, `cs` quasi costante su di lui)* ### **che si propaga lungo `a2`, a tre quote:**
    ### **la velocita' lungo `a2`** *(la proiezione dello spostamento su `a2`, archi per tick)* ### **contro `cs` mediato sull'energia; l'esponente `d ln v/d ln cs`.**"""
    import _u1_secondo as U2
    L1, L2 = U2.LG2
    bl0 = U.blocchi_campo(U2.S0)[0]
    t0 = (2 * np.pi * U2.N_FASCIO[0] / L1, 2 * np.pi * U2.N_FASCIO[1] / L2)
    out = []
    for q in QUOTE:
        c, cs = CP.campo_grad_a1(U2.ETA)
        m1q = q * L1
        U.pacchetto_campo(c, bl0, t0, W_A2, (m1q, L2 / 2.0), 2)
        pos, xx, ss = (m1q, L2 / 2.0), [], []
        for tt in range(T_A2 + 1):
            if tt:
                U.tick_campo(c)
            pos, w = U2.baricentro(c, pos)
            xx.append(-0.5 * (pos[0] - m1q) + (pos[1] - L2 / 2.0))
            ss.append(float(np.sum(w * cs) / np.sum(w)))
        v = float(np.polyfit(np.arange(T_A2 + 1, dtype=float), np.array(xx), 1)[0])
        out.append({"quota": q, "m1": m1q, "v_a2": v, "cs": float(np.mean(ss))})
    p = np.polyfit(np.log([o["cs"] for o in out]), np.log([o["v_a2"] for o in out]), 1)
    return out, float(p[0])


def vmax_tutte(r, n):
    best = 0.0
    for a in range(n):
        for b in range(n):
            t1, t2 = 2 * np.pi * a / n, 2 * np.pi * b / n
            lam, V = np.linalg.eigh(CP.H_r(t1, t2, r))
            for c in range(6):
                best = max(best, grad_mu(t1, t2, r, V[:, c]))
    return np.pi * best


def main(argv):
    del argv
    import _presidio
    import _triangoli_forza as TF
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 120)
    print("LA CURVATURA, PARTE 0-BIS: la luce in A1 misurata, la velocita' massima vera della materia, il rapporto delle due c nella stessa unita'")
    print("=" * 120)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_curvatura_0bis.py", "csv/_curvatura_prototipo.py", "csv/_u1_terzo.py", "csv/_u1_secondo.py", "csv/_u1_prototipo.py",
                                     "csv/_triangoli.py", "csv/_triangoli_forza.py", "csv/_triangoli_bassa_energia.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: R_LISTA %s R_SPETTRI %s S_LUCE %g (Courant in A1: s <= 0.40825/r, al r massimo 2: 0.2041) S_SPETTRI %g GRIGLIE %s K_PICCOLO %g H_K %g DIREZIONI_V %d"
          % (R_LISTA, R_SPETTRI, S_LUCE, S_SPETTRI, GRIGLIE, K_PICCOLO, H_K, DIREZIONI_V))
    print("    VMAX_1 %g STIME %s TOLL_C1 %g TOLL_VMAX1 %g TOLL_X1 %g TOLL_CR %g TOLL_STIME %g; le unita': archi per tempo proprio (la velocita' per tick / s), e lunghezza propria per tempo proprio (x l = 1/r)"
          % (VMAX_1, STIME, TOLL_C1, TOLL_VMAX1, TOLL_X1, TOLL_CR, TOLL_STIME))
    print("-" * 120)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    print("### M1 -- LA LUCE IN A1 (una regione uniforme, s %g, s_rif = s/r, l = 1/r, A_p = (sqrt3/4)/r^2, il tempo del campo F1)" % S_LUCE)
    L = {}
    for r in R_LISTA:
        t0 = time.time()
        L[r] = luce(r)
        scrivi(dict(L[r], tipo="luce"))
        x = L[r]
        print("  r %-5g | c (dispersione) %.6f archi/tempo proprio = %.6f lunghezza propria/tempo proprio | isotropia %.1e | il pacchetto %.5f (previsto %.5f) | max|lambda| %.12f (Courant carta s <= %.4f) | %.0fs"
              % (r, x["c_archi"], x["c_propria"], x["isotropia"], x["pacchetto_v"], x["pacchetto_v_prevista"], x["max_lambda"], x["courant_carta"], time.time() - t0))
        sys.stdout.flush()
    esito("SERVIZIO: stabile a s %g per ogni r (max|lambda| fuori dalla gauge <= 1 + 1e-6)" % S_LUCE, all(L[r]["max_lambda"] <= 1 + 1e-6 for r in R_LISTA),
          " ".join("%.9f" % L[r]["max_lambda"] for r in R_LISTA))
    print("-" * 120)
    print("### M2 -- LA VELOCITA' MASSIMA VERA DELLA MATERIA (il generatore H_r, la banda della coppia a K seguita per continuita'; e su tutte le bande)")
    V = {}
    for r in R_LISTA:
        t0 = time.time()
        vb = [np.pi * x["x"] for x in CP.x_di(r)]
        vk = {n: CP_max for n, CP_max in ((n, vmax_banda_K(r, n)) for n in GRIGLIE)}
        vt = vmax_tutte(r, GRIGLIE[0])
        vo = vmax_ottimizzato(r)
        V[r] = {"v_b": vb, "v_max_K": {str(n): v for n, v in vk.items()}, "v_max_tutte_48": vt, "ottimizzato": vo}
        scrivi(dict(V[r], tipo="materia", r=r))
        print("  r %-5g | v_b/s %s | v_max/s banda K seguita: %s | tutte le bande (48) %.6f | L'OTTIMIZZATORE (griglia %d %.7f): %.7f a t %s, k %s, il salto minimo con la seconda banda %.4f | %.0fs"
              % (r, " ".join("%.6f" % x for x in vb), " | ".join("%d: %s" % (n, " ".join("%.6f" % x for x in v)) for n, v in vk.items()), vt, N_GRIGLIA_OTT, vo["griglia"], vo["ottimo"],
                 " ".join("%.5f" % x for x in vo["t"]), " ".join("%.5f" % x for x in vo["k_cart"]), vo["salto_minimo"], time.time() - t0))
        sys.stdout.flush()
    vd = vmax_direzioni(1.0, GRIGLIE[0], 61)
    scrivi({"tipo": "diagnosi_direzioni", "r": 1.0, "n": GRIGLIE[0], "ndir": 61, "v_max_su_s": vd})
    print("  LA CAUSA DELLA SOTTOSTIMA (lettura): r 1, griglia %d: la scansione su 61 direzioni (come _triangoli_forza.v_max) %.7f; |grad| %.7f; l'ottimizzatore %.7f; il vecchio valore %.6f"
          % (GRIGLIE[0], vd, V[1.0]["v_max_tutte_48"], V[1.0]["ottimizzato"]["ottimo"], VMAX_1_VECCHIO))
    sp = {}
    for r in R_SPETTRI:
        with CP.a1(S_SPETTRI / r):
            sp[r] = float(TF.v_max(TF.matrice_L(0.0, S_SPETTRI))[0]) / S_SPETTRI
        scrivi({"tipo": "spettri", "r": r, "s": S_SPETTRI, "v_max_su_s": sp[r]})
        print("  gli spettri completi con A1 (s %g, tutte le bande, griglia 48) a r %g: v_max/s %.6f contro il generatore (tutte, 48) %.6f" % (S_SPETTRI, r, sp[r], V[r]["v_max_tutte_48"]))
    print("-" * 120)
    print("### M3 -- IL RAPPORTO, nella stessa unita' (archi per tempo proprio)")
    rap = {}
    for r in R_LISTA:
        c = L[r]["c_archi"]
        vm = V[r]["ottimizzato"]["ottimo"]
        rap[r] = {"v_max_su_c": vm / c, "v_b_su_c": V[r]["v_b"][0] / c, "v_max_tutte_su_c": V[r]["v_max_tutte_48"] / c}
        print("  r %-5g | c %.6f | v_max (l'ottimizzatore) %.6f: v_max/c %.6f | v_b %.6f: v_b/c %.6f | v_max (tutte) / c %.6f"
              % (r, c, vm, rap[r]["v_max_su_c"], V[r]["v_b"][0], rap[r]["v_b_su_c"], rap[r]["v_max_tutte_su_c"]))
    scrivi({"tipo": "rapporto", "rapporti": {str(k): v for k, v in rap.items()}})
    print("-" * 120)
    print("### M1-BIS (i) -- LA LUCE NELLE DIREZIONI, a cs uniforme (le tre direzioni degli archi e la normale ad a2)")
    DIR = {}
    for r in R_DIREZIONI:
        DIR[r] = luce_direzioni(r)
        sp_ = max(DIR[r].values()) - min(DIR[r].values())
        scrivi({"tipo": "direzioni", "r": r, "v_g_su_s": DIR[r]})
        print("  r %-5g | %s | la variazione relativa %.2e" % (r, " ".join("%s gradi %.7f" % (k, v) for k, v in DIR[r].items()), sp_ / np.mean(list(DIR[r].values()))))
    print("### M1-BIS (ii) -- LA LUCE LUNGO a2 NEL GRADIENTE di 31ee70cc (un pacchetto largo %.0f, %d tick, a tre quote)" % (W_A2, T_A2))
    A2, esp_a2 = luce_lungo_a2()
    for o in A2:
        print("  la quota m1/L1 %.2f (m1 %.0f): v lungo a2 %.6f archi/tick a cs %.5f: v/(cs^2/cs_rif) %.5f" % (o["quota"], o["m1"], o["v_a2"], o["cs"], o["v_a2"] / (o["cs"] ** 2 / 0.2)))
    print("  l'esponente d ln v/d ln cs lungo a2: %.4f (lungo il gradiente, 31ee70cc: %.4f)" % (esp_a2, ESP_LUNGO))
    scrivi({"tipo": "lungo_a2", "quote": A2, "esponente": esp_a2, "esponente_lungo_gradiente": ESP_LUNGO})
    print("-" * 120)
    print("### I CONTROLLI")
    x1 = [x["x"] for x in CP.x_di(1.0)]
    vk1 = V[1.0]["ottimizzato"]["ottimo"]
    esito("DEVE PASSARE: a r 1, c = 1 entro %g; v_max/s (l'ottimizzatore) = %g entro %g; x(1) = 1/4 entro %g" % (TOLL_C1, VMAX_1, TOLL_VMAX1, TOLL_X1),
          abs(L[1.0]["c_archi"] - 1) <= TOLL_C1 and abs(vk1 - VMAX_1) <= TOLL_VMAX1 and all(abs(x - 0.25) <= TOLL_X1 for x in x1),
          "c %.6f, v_max %.6f (tutte %.6f), x %s" % (L[1.0]["c_archi"], vk1, V[1.0]["v_max_tutte_48"], " ".join("%.10f" % x for x in x1)))
    peg = max(abs(L[r]["c_archi"] / r - 1) for r in R_LISTA)
    esito("PUO' FALLIRE: c_luce(r) = r archi per tempo proprio entro %g a ogni r (la carta)" % TOLL_CR, peg <= TOLL_CR, "lo scarto peggiore %.2e" % peg, deve=False)
    peg = max(abs(V[r]["ottimizzato"]["ottimo"] - STIME[r]) for r in STIME)
    esito("PUO' FALLIRE: v_max/s (l'ottimizzatore) contro le stime del guardiano entro %g" % TOLL_STIME, peg <= TOLL_STIME,
          " ".join("r %g %.7f/%.6f" % (r, V[r]["ottimizzato"]["ottimo"], STIME[r]) for r in STIME), deve=False)
    d1 = (max(DIR[1.0].values()) - min(DIR[1.0].values())) / np.mean(list(DIR[1.0].values()))
    esito("DEVE PASSARE (M1-BIS): a r 1 le quattro direzioni uguali entro %g" % TOLL_DIR, d1 <= TOLL_DIR, "%.2e" % d1)
    dd = max((max(DIR[r].values()) - min(DIR[r].values())) / np.mean(list(DIR[r].values())) for r in R_DIREZIONI)
    esito("PUO' FALLIRE (M1-BIS i): isotropa entro %g a ogni r" % TOLL_DIR, dd <= TOLL_DIR, "la peggiore %.2e" % dd, deve=False)
    esito("PUO' FALLIRE (M1-BIS ii): l'esponente lungo a2 = %.2f entro %g" % (ESP_LUNGO, TOLL_ESP), abs(esp_a2 - ESP_LUNGO) <= TOLL_ESP, "%.4f" % esp_a2, deve=False)
    esito("PUO' FALLIRE: v_max/c_luce < 1 a ogni r (nessun superamento della luce in A1)", all(rap[r]["v_max_su_c"] < 1 for r in R_LISTA),
          " ".join("%.4f" % rap[r]["v_max_su_c"] for r in R_LISTA), deve=False)
    var = rap[0.5]["v_max_su_c"] / rap[2.0]["v_max_su_c"]
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA: v_max/c_luce costante in r (la chiave: il rapporto fra r 0.5 e r 2 > 1.5)", var > 1.5, "%.3f" % var)
    print("-" * 120)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
