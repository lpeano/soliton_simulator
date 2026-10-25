# -*- coding: utf-8 -*-
r"""**IL TERZO PASSO DEL U(1): la larghezza del fascio (il `16%` della deflessione), e la regola `theta = s/x` sui triangoli, in memoria (la materia alla stessa `c` della luce?)**
*([[U1-PROTOTIPO-TRIANGOLI]], [[PROGETTO-U1]], [[LORENTZ-MATERIA-INTERFERENZA]], [[DECISIONE-SOLO-TRIANGOLI]])*.

> ### ⛔ **Il task history e' `2026-10-25_u1_terzo.md`** *(`47f9fff8`: il metodo, le previsioni, i criteri)*; ### **le decisioni di Luca: `2026-10-24_u1_secondo.md`, sezione `5`.** ### **`B-4` NON cambia: la variante vive in un `with`.**
> ### **Importati, non copiati:** `_u1_secondo` *(`campo_gradiente`, `prepara`, `baricentro`, `corsa_lungo`, `corsa_fascio`, `c_lungo_a2`, le costanti della scena)*, `_u1_prototipo` *(`tick_campo`, `blocchi_campo`)*,
> `_triangoli_forza` *(`coppia_K`, `blocchi`, `matrice_L`, `v_max`, `corsa_con`, `pacchetto_banda`, `spazi_banda`, `q_della_striscia`, `tori`)*, `_triangoli_bassa_energia` *(`matrice`, `curvatura`)*,
> `_triangoli_fattore.ramo_lungo`, `_triangoli_dove_la_luce.vmax_tutti`, `_scala_e_zero` *(`H_eff`, `esponente`)*.
> ### ⚠ **Due trappole, dal codice:** `_triangoli_forza.modo` scrive `dw_simm = dw + pi` a mano e `_triangoli_bassa_energia.main` mette `pi s` nello zero simmetrico: ### **qui lo scarto fra i due zeri `sigma` si MISURA.**

Gira con:  python csv/_u1_terzo.py > doc/referti_l2/u1_terzo.txt
"""
import contextlib
import io
import json
import math
import os
import subprocess
import sys
import time
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402
import _u1_prototipo as U                                      # noqa: E402
import _u1_secondo as U2                                       # noqa: E402

RIF_SEC = "64bb2328"
RIF_BASSA = "8781162c"
RIF_FATTORE = "7daa8840"
# ### parte 1
W_SCAN = (6.0, 8.0, 12.0, 16.0, 24.0)
TOLL_RIP = 1e-9
TOLL_EST = 0.02
# ### parte 2
S_VAR = (0.001, 0.01, 0.05, 0.1, 0.3)
EPS_VAR = (0.0, 0.5)
S_RIP = (0.05, 0.1, 0.3)
EPS_RIP = (0.0, 0.5)
H_DER = 1e-3                    # ### la derivata in s: +-H s (come _triangoli_bassa_energia.H)
S_DELTA = (0.02, 0.05, 0.1, 0.2, 0.3)
S0_F = (0.05, 0.1, 0.3)
LX_F = 96
ETA_F = (0.0, 1e-3, -1e-3, 1e-2, -1e-2)
S_CHIAVE = 0.1
LF = 6
KF = (2, 2)
TOLL_BIT = 1e-12
TOLL_X = 1e-9
TOLL_VB1 = 1e-6
TOLL_F1 = 0.02
TOLL_RG = 0.05
TOLL_LS = 1e-6
K_FINE = 0.01
JSONL = os.path.join(RADICE, "doc", "referti_l2", "u1_terzo.jsonl")
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


def git_jsonl(rif, rel):
    out = subprocess.run(["git", "show", "%s:%s" % (rif, rel)], capture_output=True, cwd=RADICE, check=True).stdout.decode("utf-8")
    return [json.loads(x) for x in out.splitlines() if x.strip()]


def av(x):
    return float((x + np.pi) % (2.0 * np.pi) - np.pi)


# =====================================================================================
#   LA VARIANTE theta = s/x, IN MEMORIA
# =====================================================================================
@contextlib.contextmanager
def variante(K):
    """### **`espi(s K)` invece di `espi(s)`:** ### **`theta = pi K s f`**, con `K = 1/(pi x)` ### **(`theta = s f/x`)**. ### **Le cache dei blocchi si svuotano entrando e uscendo.**"""
    import _triangoli_forza as TF
    import flussi_parziali as FP
    vero = FP.espi

    def espi(s, z, lavoro):
        return vero(s * K, z, lavoro)
    TF._CACHE.clear()
    FP.espi = espi
    try:
        yield
    finally:
        FP.espi = vero
        TF._CACHE.clear()


# =====================================================================================
#   PARTE 1 -- la larghezza del fascio
# =====================================================================================
def fascio_esteso(W, bl0, cp):
    """### Il fascio di `_u1_secondo.corsa_fascio` *(F1)* ### **con la larghezza `sigma_u(t)` e la previsione di Ehrenfest** *(la media di `-s ds/du` sull'energia, integrata due volte)*."""
    L1, L2 = U2.LG2
    c, cs = U2.campo_gradiente(U2.LG2, U2.S0, U2.ETA, "F1", 1.0, "noncompatto")
    spettro = U2.prepara(c, bl0, (2 * np.pi * U2.N_FASCIO[0] / L1, 2 * np.pi * U2.N_FASCIO[1] / L2), W, (L1 / 4.0, 0.0), "F1")
    # ### ⭐ **il fattore d'angolo** *(annotazione `3` del task history, una LETTURA)*: ### **`<cos^2 theta>` sullo spettro pesato con l'energia** *(`theta` l'angolo fra `k` e `a2`)*
    import _triangoli_bassa_energia as BE
    Jinv = np.linalg.inv(BE.J)
    a2 = np.array([-0.5, math.sqrt(3.0) / 2.0])
    num = den = 0.0
    for t1, t2, g, uk in spettro:
        C = np.array([[1.0, np.exp(1j * t1), -1.0], [-np.exp(1j * t2), -1.0, 1.0]])
        Hk = g * g * (U2.S0 ** 2 * U.L_SU_LS * float(np.sum(np.abs(uk[3:]) ** 2)) / 2.0 + float(np.sum(np.abs(C @ uk[:3]) ** 2)) / (2.0 * U.AREA))
        kk = Jinv @ np.array([t1, t2])
        num += Hk * float(kk @ a2) ** 2 / float(kk @ kk)
        den += Hk
    cos2 = num / den
    m1 = (np.arange(c.n) // L2).astype(float)
    dsdu = -U2.S0 * U2.ETA * 2 * np.pi / L1 * np.sin(2 * np.pi * m1 / L1) / (math.sqrt(3.0) / 2.0)
    acc = -cs * dsdu
    pos, uu, sg, aE = (L1 / 4.0, 0.0), [], [], []
    for t in range(U2.T_FASCIO + 1):
        if t:
            U.tick_campo(c)
        pos, w = U2.baricentro(c, pos)
        uu.append(pos[0] * math.sqrt(3.0) / 2.0)
        d = ((m1 - pos[0] + L1 / 2.0) % L1 - L1 / 2.0) * math.sqrt(3.0) / 2.0
        sw = float(np.sum(w))
        sg.append(math.sqrt(max(float(np.sum(w * d * d)) / sw - (float(np.sum(w * d)) / sw) ** 2, 0.0)))
        aE.append(float(np.sum(w * acc)) / sw)
    tt = np.arange(U2.T_FASCIO + 1, dtype=float)
    a = 2.0 * float(np.polyfit(tt, np.array(uu), 2)[0])
    # ### Ehrenfest: u_E'' = <-s ds/du>_w(t), u_E'(0) = 0 (il fascio parte parallelo)
    vE, uE = 0.0, [uu[0]]
    for t in range(1, len(tt)):
        vE += 0.5 * (aE[t - 1] + aE[t])
        uE.append(uE[-1] + vE)
    aEf = 2.0 * float(np.polyfit(tt, np.array(uE), 2)[0])
    u0m = L1 / 4.0
    Lu = L1 * math.sqrt(3.0) / 2.0
    k1 = 2 * np.pi * U2.ETA / Lu * math.sin(2 * np.pi * u0m / L1) / (1 + U2.ETA * math.cos(2 * np.pi * u0m / L1))
    cs0 = U2.S0 * (1 + U2.ETA * math.cos(2 * np.pi * u0m / L1))
    kg = 2 * np.pi / Lu
    sg = np.array(sg)
    return {"W": W, "cos2": cos2, "a_su_aE_cos2": a / (aEf * cos2), "a": a, "kappa": a / (cp * cs0) ** 2, "kappa_su_R1": a / (cp * cs0) ** 2 / k1, "a_ehrenfest": aEf, "a_su_aE": a / aEf, "sigma0": float(sg[0]),
            "sigma_fine": float(sg[-1]), "allargamento": float(sg[-1] / sg[0]), "X": float(np.mean(kg * kg * sg * sg))}


def parte_1():
    print("### PARTE 1 -- IL 16%% DELLA DEFLESSIONE: F1, la scena di %s (%dx%d, s0 %.2f, eta %.2f), il fascio largo W in %s" % ((RIF_SEC,) + U2.LG2 + (U2.S0, U2.ETA, W_SCAN)))
    vecchio = [r for r in git_jsonl(RIF_SEC, "doc/referti_l2/u1_secondo.jsonl") if r.get("tipo") == "gradiente"][0]
    bl0 = U.blocchi_campo(U2.S0)[0]
    cp = U2.c_lungo_a2(bl0, U2.N_FASCIO, U2.LG2, U2.S0)
    fa12 = U2.corsa_fascio(U2.LG2, U2.S0, U2.ETA, "F1", bl0, U2.T_FASCIO, U2.N_FASCIO, 12.0)
    ctrl12 = U2.corsa_lungo(U2.LG2, U2.S0, 0.0, "F1", bl0, U2.T_LUNGO, U2.N1_LUNGO, 12.0, None)
    lu12 = U2.corsa_lungo(U2.LG2, U2.S0, U2.ETA, "F1", bl0, U2.T_LUNGO, U2.N1_LUNGO, 12.0, ctrl12["v_su_cs_media"])
    d1 = abs(fa12["a"] - vecchio["fascio"]["F1"]["a"]) / abs(vecchio["fascio"]["F1"]["a"])
    d2 = max(abs(lu12[k] - vecchio["lungo"]["F1"][k]) / max(abs(vecchio["lungo"]["F1"][k]), 1e-300) for k in ("v_su_cs_media", "variazione", "T_rapporto", "dietro", "energia"))
    esito("DEVE PASSARE: il fascio e il pacchetto lungo W 12 (F1) riproducono %s entro %g" % (RIF_SEC, TOLL_RIP), max(d1, d2) <= TOLL_RIP, "fascio %.1e, lungo %.1e" % (d1, d2))
    righe = []
    for W in W_SCAN:
        t0 = time.time()
        fe = fascio_esteso(W, bl0, cp)
        if W == 12.0:
            esito("SERVIZIO: il fascio esteso a W 12 = corsa_fascio (la stessa a)", abs(fe["a"] - fa12["a"]) <= 1e-12 * abs(fa12["a"]), "%.1e" % abs(fe["a"] - fa12["a"]))
        ct = U2.corsa_lungo(U2.LG2, U2.S0, 0.0, "F1", bl0, U2.T_LUNGO, U2.N1_LUNGO, W, None)
        lu = U2.corsa_lungo(U2.LG2, U2.S0, U2.ETA, "F1", bl0, U2.T_LUNGO, U2.N1_LUNGO, W, ct["v_su_cs_media"])
        fe.update(riflessione=lu["dietro"] - ct["dietro"], v_su_cs_variazione=lu["variazione"], T_rapporto=lu["T_rapporto"])
        righe.append(fe)
        scrivi(dict(fe, tipo="fascio"))
        print("  W %4.1f | kappa/R1 %.4f | a/a_Ehrenfest %.4f | <cos^2> %.4f, a/(a_E <cos^2>) %.4f | sigma_u %.1f -> %.1f (x%.2f) | X = <k_g^2 sigma^2> %.4f | riflessione %.2e | v/cs variazione %.2e | %.0fs"
              % (W, fe["kappa_su_R1"], fe["a_su_aE"], fe["cos2"], fe["a_su_aE_cos2"], fe["sigma0"], fe["sigma_fine"], fe["allargamento"], fe["X"], fe["riflessione"], fe["v_su_cs_variazione"], time.time() - t0))
        sys.stdout.flush()
    X = np.array([r["X"] for r in righe])
    Y = np.array([r["kappa_su_R1"] for r in righe])
    p1 = np.polyfit(X, Y, 1)
    p2 = np.polyfit(X, Y, 2)
    print("  L'ESTRAPOLAZIONE a X -> 0 (il fascio largo e il gradiente lento): grado 1 %.4f (pendenza %+.3f), grado 2 %.4f" % (p1[-1], p1[0], p2[-1]))
    scrivi({"tipo": "estrapolazione", "grado1": [float(x) for x in p1], "grado2": [float(x) for x in p2]})
    esito("PUO' FALLIRE: la deflessione estrapolata (grado 1, X -> 0) entro %g da R1" % TOLL_EST, abs(p1[-1] - 1.0) <= TOLL_EST, "%.4f" % p1[-1], deve=False)
    return righe


# =====================================================================================
#   PARTE 2 -- la variante
# =====================================================================================
def H_gen(t1, t2):
    """### **Il generatore a `s -> 0`, dalle PROIEZIONI** *(non dal passo)*: ### **`H = (I - P_u) + P_-`** sulle `6` estremita' del nodo *(`0..2` i lati `+` dei tre archi propri, `3..5` i lati `-` dei tre entranti)*."""
    H = np.eye(6) - np.ones((6, 6)) / 6.0
    H = H.astype(complex)
    for a, th in enumerate((t1, t2, t1 + t2)):
        H[a, a] += 0.5
        H[3 + a, 3 + a] += 0.5
        H[a, 3 + a] += -0.5 * np.exp(1j * th)
        H[3 + a, a] += -0.5 * np.exp(-1j * th)
    return H


def dH_gen(t1, t2):
    d1 = np.zeros((6, 6), dtype=complex)
    d2 = np.zeros((6, 6), dtype=complex)
    for a, (th, c1, c2) in enumerate(((t1, 1, 0), (t2, 0, 1), (t1 + t2, 1, 1))):
        g = -0.5 * 1j * np.exp(1j * th)
        d1[a, 3 + a] += c1 * g
        d1[3 + a, a] += c1 * np.conj(g)
        d2[a, 3 + a] += c2 * g
        d2[3 + a, a] += c2 * np.conj(g)
    return d1, d2


def x_dal_generatore(w_ref):
    """### **`x = sqrt(mu0 mu'')`, `mu = 1 - lambda_H`** *(lo zero simmetrico)*, ### **la coppia a `K` scelta dai livelli misurati** `w_ref/(pi s)` *(a `s 0.001`)*, ### **il fit di `_u1_secondo.vb_di`** *(`k_max 0.1`, `200` punti, lungo la normale ad `a2`)*; ### **e `y = max |grad lambda_H|`.**"""
    import _triangoli_bassa_energia as BE
    import _triangoli_forza as TF
    lam, V = np.linalg.eigh(H_gen(2 * np.pi / 3, 2 * np.pi / 3))
    mu = 1.0 - lam
    xs = []
    for wr in w_ref:
        i = int(np.argmin(np.abs(mu - wr)))
        v = V[:, [i]]
        qq = np.linspace(0.0, K_FINE * math.sqrt(3.0) / 2.0, U2.NK3 + 1)
        mm = []
        for q in qq:
            l2, V2 = np.linalg.eigh(H_gen(*TF.theta_di("A", q)))
            j = int(np.argmax(np.abs(V2.conj().T @ v)[:, 0]))
            mm.append(1.0 - l2[j])
            v = V2[:, [j]]
        k = qq * 2.0 / math.sqrt(3.0)
        # ### ⚠ **la curvatura FINE** *(annotazione `1` del task history)*: ### **`mu - mu0 = a k^2 + b k^4 + c k^6` a `k <= K_FINE`, e `x^2 = 2 mu0 a`** *(`v_b^2 = omega0 omega''`)*
        X = np.stack([k ** 2, k ** 4, k ** 6], axis=1)
        cc, *_ = np.linalg.lstsq(X, np.array(mm) - mm[0], rcond=None)
        x2 = 2.0 * mm[0] * cc[0]
        xs.append({"mu0": float(mu[i]), "mu_ref": float(wr), "x": float(math.sqrt(x2)) if x2 > 0 else None})
    J = BE.J
    ymax = 0.0
    n = 96
    for n1 in range(n):
        for n2 in range(n):
            t1, t2 = 2 * np.pi * n1 / n, 2 * np.pi * n2 / n
            l2, V2 = np.linalg.eigh(H_gen(t1, t2))
            d1, d2 = dH_gen(t1, t2)
            g1 = np.real(np.einsum("ij,ik,kj->j", V2.conj(), d1, V2))
            g2 = np.real(np.einsum("ij,ik,kj->j", V2.conj(), d2, V2))
            gx = J[0, 0] * g1 + J[1, 0] * g2
            gy = J[0, 1] * g1 + J[1, 1] * g2
            ymax = max(ymax, float(np.max(np.hypot(gx, gy))))
    return xs, ymax


def sigma_zeri(eps, s):
    """### **Lo scarto fra i due zeri, MISURATO:** `A_simm = e^{-i sigma s} A_oggi` *(il blocco della materia al lato `6`)*: ### `sigma` e lo scarto da un fattore unico."""
    import _triangoli_bassa_energia as BE
    As = BE.matrice(eps, s, LF, "simm")[KF[0], KF[1], :12, :12]
    Ao = BE.matrice(eps, s, LF, "oggi")[KF[0], KF[1], :12, :12]
    i = np.unravel_index(np.argmax(np.abs(Ao)), Ao.shape)
    r = As[i] / Ao[i]
    sig = -float(np.angle(r)) / s
    return sig, float(np.max(np.abs(As - r * Ao)))


def vb_eps(eps, s):
    """### `v_b` dei due rami della coppia a `K` *(lo stesso fit di `_u1_secondo.vb_di`, a `eps` dato)*, i livelli `w`, i `Q`."""
    import _triangoli_fattore as F
    import _triangoli_forza as TF
    bl = TF.blocchi(eps, s)
    out = []
    for b in TF.coppia_K(eps, s):
        qq, ww = F.ramo_lungo(bl, b["Q"], b["w"], U2.KMAX3 * math.sqrt(3.0) / 2.0, U2.NK3)
        k = qq * 2.0 / math.sqrt(3.0)
        y = ww ** 2 - b["w"] ** 2
        X = np.stack([k ** 2, k ** 4], axis=1)
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        out.append({"w": float(b["w"]), "Q": b["Q"], "v_b": float(math.sqrt(c[0])) if c[0] > 0 else None, "delta_min": b["delta_min"]})
    return out


def riga_variante(eps, s, sig, K):
    """### `(a)`-`(d)` a `(eps, s)`. ### ⛔ **LA MAPPA ESATTA** *(annotazione `2` del task history)*: ### **la variante a `(eps, s)` E' il passo di oggi a `(eps/K, K s)`** *(la moneta va con `eps dtau`)*: ### **il blocco si
    CONFRONTA a ogni riga entro `TOLL_BIT`, e le grandezze per tick si leggono dal passo di oggi** *(`_triangoli_forza.coppia_K` scrive `pi s` a mano: sotto la variante non si puo' chiamare)*; ### **`d/ds = K d/ds'`.**
    ### **`v_max` si misura a variante ACCESA** *(nessuna trappola)*."""
    import _triangoli_bassa_energia as BE
    import _triangoli_dove_la_luce as DL
    import _triangoli_forza as TF
    e2, s2 = eps / K, s * K
    with variante(K):
        Av = BE.matrice(eps, s, LF, "simm")
        vm = DL.vmax_tutti(eps, s)
    mappa = float(np.max(np.abs(Av - BE.matrice(e2, s2, LF, "simm"))))
    bande = vb_eps(e2, s2)
    piu = [b["w"] for b in TF.coppia_K(e2, s2 * (1 + H_DER))]
    meno = [b["w"] for b in TF.coppia_K(e2, s2 * (1 - H_DER))]
    A = TF.matrice_L(e2, s2)
    rami = []
    for q, b in enumerate(bande):
        cu = BE.curvatura(A, TF.KL[0], TF.KL[1], b["w"], b["Q"])
        om = float(np.mean(cu["cart_autovalori"]))
        dws = K * (piu[q] - meno[q]) / (2 * H_DER * s2)
        vb = b["v_b"]
        fat = {}
        for nome, c in (("luce", s), ("v_max", vm["tutti"])):
            fat[nome] = {"c": c, "R_t": s * dws / b["w"], "Q_b": b["w"] * om / vb ** 2, "L": (vb / c) ** 2, "F": s * om * dws / c ** 2}
        kk = cu["h11"] / cu["v"] ** 2 if cu["v"] else None
        rami.append({"w": b["w"], "v_b": vb, "omega2": om, "dw_simm": dws, "h11": cu["h11"], "v": cu["v"], "k": kk, "fattori": fat, "delta_min": b["delta_min"]})
    a0 = s * rami[0]["k"] * (rami[0]["dw_simm"] - sig)
    b0 = s * rami[1]["k"] * (rami[1]["dw_simm"] - sig)
    ma, mb = 2 * s * rami[0]["k"] * sig, 2 * s * rami[1]["k"] * sig
    ls = (b0 - a0) / (ma - mb) if ma != mb else None
    salto = abs(bande[1]["w"] - bande[0]["w"])
    return {"eps": eps, "s": s, "eps_mappa": e2, "s_mappa": s2, "mappa": mappa, "sigma": sig, "rami": rami, "v_max": vm, "salto": salto, "salto_su_s": salto / s, "lambda_stella": ls,
            "vb_su_s": [r["v_b"] / s for r in rami], "vmax_su_s": vm["tutti"] / s}


def delta_esponente(eps):
    import _scala_e_zero as Z
    import _triangoli_bassa_energia as BE
    Hs = {}
    for x in S_DELTA:
        B = BE.matrice(eps, x, 16, "oggi")[1, 0, :12, :12]
        lam, V = np.linalg.eig(B)
        Hs[x] = Z.H_eff(V, -np.angle(lam), x)
    n0 = np.linalg.norm(Hs[S_DELTA[0]])
    d = {x: float(np.linalg.norm(Hs[x] - Hs[S_DELTA[0]]) / n0) for x in S_DELTA}
    return d, Z.esponente(d, True)


def forza(s0, sig, K):
    """### Le corse di `_triangoli_fattore.parte_B` *(toro `A`, `eps 0`, il pacchetto di banda, il baricentro lineare)* a `Lx 96`; ### **`a_H` con `dw_simm` NUMERICO** *(lo scarto `sigma` dentro)*; ### **`a_RG` con `c = s0`.**"""
    import _triangoli_bassa_energia as BE
    import _triangoli_forza as TF
    f = TF.tori()["A"]["f"]
    s2 = K * s0
    bande = vb_eps(0.0, s2)
    piu = [b["w"] for b in TF.coppia_K(0.0, s2 * (1 + H_DER))]
    meno = [b["w"] for b in TF.coppia_K(0.0, s2 * (1 - H_DER))]
    bl = TF.blocchi(0.0, s2)
    A = TF.matrice_L(0.0, s2)
    Lx = LX_F
    n = Lx * TF.LY
    m1 = (np.arange(n) // TF.LY).astype(float)
    m2 = (np.arange(n) % TF.LY).astype(float)
    qs = TF.q_della_striscia(Lx)
    out = []
    for q_, b in enumerate(bande):
        om = float(np.mean(BE.curvatura(A, TF.KL[0], TF.KL[1], b["w"], b["Q"])["cart_autovalori"]))
        dws = K * (piu[q_] - meno[q_]) / (2 * H_DER * s2)
        Tm = max(Lx // 4, int(math.ceil(TF.PERIODI * 2.0 * np.pi / b["delta_min"])))
        cel = TF.pacchetto_banda("A", Lx, Lx / 4.0, Lx / 16.0, b["Q"], TF.spazi_banda(bl, b["Q"], "A", qs), m1, m2)
        with variante(K):
            rs = {eta: TF.corsa_con("A", Lx, 0.0, s0, eta, cel, "simm", Tm, 0, True)[0] for eta in ETA_F}
        for eta in (1e-3, 1e-2):
            dif = 0.5 * (rs[eta]["a"] - rs[-eta]["a"])
            dsdm = -s0 * eta * 2.0 * np.pi / Lx
            aH = -om * dws * dsdm / f ** 2
            aRG = -s0 ** 2 * (dsdm / s0) / f ** 2
            out.append({"s0": s0, "banda": q_, "eta": eta, "tick": Tm, "differenziale": dif, "semisomma": 0.5 * (rs[eta]["a"] + rs[-eta]["a"]), "a0": rs[0.0]["a"],
                        "dif_su_aH": dif / aH, "dif_su_aRG_luce": dif / aRG, "gamma_medio": rs[eta]["gamma_medio"], "dw_simm": dws, "omega2": om})
    return out


def parte_2():
    import _triangoli_bassa_energia as BE
    import _triangoli_forza as TF
    print("### PARTE 2 -- LA REGOLA theta = s/x SUI TRIANGOLI, IN MEMORIA (espi avvolta; B-4 non cambia)")
    # ### la variante SPENTA: la riproduzione
    liv = {(r["eps"], r["s"]): r["livelli"]["K"] for r in git_jsonl(RIF_BASSA, "doc/referti_l2/triangoli_bassa_energia.jsonl") if r.get("tipo") == "livelli"}
    fat = {(r["s"], r["banda"]): r for r in git_jsonl(RIF_FATTORE, "doc/referti_l2/triangoli_fattore.jsonl") if r.get("tipo") == "fattori" and r["eps"] == 0.0}
    peg = 0.0
    for eps in EPS_RIP:
        for s in S_RIP:
            W = -np.angle(np.linalg.eigvals(TF.matrice_L(eps, s)[TF.KL[0], TF.KL[1], :12, :12]))
            w = np.sort(np.array([av(x) for x in W]))
            lv = []
            for x in w:
                if lv and abs(x - lv[-1][0]) < 1e-9:
                    lv[-1][1] += 1
                else:
                    lv.append([float(x), 1])
            r = liv[(eps, s)]
            assert [m for _, m in lv] == [m for _, m in r], "le molteplicita' a K"
            peg = max(peg, max(abs(a[0] - b[0]) for a, b in zip(lv, r)))
            if eps == 0.0:
                for q, b in enumerate(vb_eps(0.0, s)):
                    ff = fat[(s, q)]
                    om = float(np.mean(BE.curvatura(TF.matrice_L(0.0, s), TF.KL[0], TF.KL[1], b["w"], b["Q"])["cart_autovalori"]))
                    peg = max(peg, abs(b["w"] - ff["omega0"]), abs(om - ff["omega2"]), abs(b["v_b"] - ff["fit"]["0.1"]["v_b"]))
    esito("DEVE PASSARE: la variante SPENTA riproduce %s (i livelli a K) e %s (omega0, omega'', v_b) entro %g" % (RIF_BASSA, RIF_FATTORE, TOLL_BIT), peg <= TOLL_BIT, "%.1e" % peg)
    sig0, res0 = sigma_zeri(0.0, S_CHIAVE)
    # ### x dal generatore
    w_ref = [b["w"] / (np.pi * 0.001) for b in TF.coppia_K(0.0, 0.001)]
    xs, ymax = x_dal_generatore(w_ref)
    x = xs[0]["x"]
    print("  x DAL GENERATORE H = (I - P_u) + P_- (le proiezioni, non il passo): %s | il limite misurato in %s: (pi/4)/pi = 0.25 | y = max|grad lambda_H| %.10f (pi y %.10f contro v_max/s -> 0.5984674498)"
          % (" ".join("mu0 %.6f (misurato %.6f) x %.12f" % (r["mu0"], r["mu_ref"], r["x"]) for r in xs), RIF_SEC, ymax, np.pi * ymax))
    scrivi({"tipo": "x_generatore", "rami": xs, "y": ymax, "pi_y": np.pi * ymax})
    if abs(x - 0.25) > TOLL_X:
        print("  ### x RICAVATO NON E' 1/4 entro %g: si usa il ricavato (task history 2.3)" % TOLL_X)
    K = 1.0 / (np.pi * x)
    print("  la variante: K = 1/(pi x) = %.12f (theta = %.6f s f); il limite di sicurezza theta <= pi: s <= pi x = %.6f; con la luce Courant s <= 0.408" % (K, np.pi * K, np.pi * x))
    with variante(K):
        sig1, res1 = sigma_zeri(0.0, S_CHIAVE)
    esito("SERVIZIO: lo scarto fra i due zeri misurato: pi spenta, 1/x accesa, entro %g (e un fattore unico)" % TOLL_BIT,
          abs(sig0 - np.pi) <= TOLL_BIT and abs(sig1 - 1.0 / x) <= TOLL_BIT * 10 and max(res0, res1) <= TOLL_BIT, "spenta %.12f accesa %.12f, residui %.1e %.1e" % (sig0, sig1, res0, res1))
    # ### la chiave: la variante a s 0.1 contro oggi a s 0.1 e a s 0.1 pi K / pi
    with variante(K):
        Av = BE.matrice(0.0, S_CHIAVE, LF, "simm")[:, :, :12, :12]
    Ao = BE.matrice(0.0, S_CHIAVE, LF, "simm")[:, :, :12, :12]
    Ar = BE.matrice(0.0, S_CHIAVE * K, LF, "simm")[:, :, :12, :12]
    d_oggi = float(np.max(np.abs(Av - Ao)))
    d_scala = float(np.max(np.abs(Av - Ar)))
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA: <<theta = s/x a s %.1f e' il passo di oggi>> (> 1e-3); E = oggi a s %.6f entro %g (eps 0)" % (S_CHIAVE, S_CHIAVE * K, TOLL_BIT),
          d_oggi > 1e-3 and d_scala <= TOLL_BIT, "contro oggi %.2e, contro oggi a s K %.1e" % (d_oggi, d_scala))
    scrivi({"tipo": "chiave", "contro_oggi": d_oggi, "contro_scala": d_scala, "K": K, "sigma_spenta": sig0, "sigma_accesa": sig1})
    righe = []
    sig = sig1
    if True:
        for eps in EPS_VAR:
            for s in S_VAR:
                t0 = time.time()
                r = riga_variante(eps, s, sig, K)
                righe.append(r)
                scrivi(dict(r, tipo="variante", rami=[{k: v for k, v in rr.items()} for rr in r["rami"]]))
                f_l = [rr["fattori"]["luce"] for rr in r["rami"]]
                f_v = [rr["fattori"]["v_max"] for rr in r["rami"]]
                print("  eps %.1f s %-5g [la mappa %.1e] | v_b/s %s | v_max/s %.6f | salto/s %.6f | F(c=1) %s (R_t %s Q_b %s L %s) | F(v_max) %s | lambda* %s | %.0fs"
                      % (eps, s, r["mappa"], " ".join("%.8f" % v for v in r["vb_su_s"]), r["vmax_su_s"], r["salto_su_s"], " ".join("%.5f" % f["F"] for f in f_l), " ".join("%.5f" % f["R_t"] for f in f_l),
                         " ".join("%.5f" % f["Q_b"] for f in f_l), " ".join("%.5f" % f["L"] for f in f_l), " ".join("%.5f" % f["F"] for f in f_v), U.f_(r["lambda_stella"], "%.8f"), time.time() - t0))
                sys.stdout.flush()
        lim = {}
        for eps in EPS_VAR:
            rr = [r for r in righe if r["eps"] == eps]
            ss = np.array([r["s"] for r in rr])
            for nome, ys in (("vb0", [r["vb_su_s"][0] for r in rr]), ("vb1", [r["vb_su_s"][1] for r in rr]), ("vmax", [r["vmax_su_s"] for r in rr]), ("salto", [r["salto_su_s"] for r in rr])):
                p = np.polyfit(ss, np.array(ys), 2)
                lim["%s_eps%g" % (nome, eps)] = {"f0": float(p[2]), "f1": float(p[1]), "f2": float(p[0])}
                print("  il limite a s -> 0, eps %.1f, %-5s: f0 %.10f f1 %+.3e f2 %+.3e" % (eps, nome, p[2], p[1], p[0]))
        scrivi({"tipo": "limiti_variante", "limiti": lim})
        pm = max(r["mappa"] for r in righe)
        esito("DEVE PASSARE: la mappa, la variante a (eps, s) = oggi a (eps/K, K s), entro %g a ogni riga" % TOLL_BIT, pm <= TOLL_BIT, "%.1e" % pm)
        esp = {}
        for eps in EPS_VAR:
            with variante(K):
                d, p = delta_esponente(eps)
            esp[eps] = p
            print("  delta(s) eps %.1f (k(1,0), lato 16): %s | l'esponente contro s %s" % (eps, " ".join("%g:%.2e" % (k, v) for k, v in d.items()), U.f_(p, "%.3f")))
            scrivi({"tipo": "delta_variante", "eps": eps, "delta": {str(k): v for k, v in d.items()}, "esponente": p})
        fz = []
        for s0 in S0_F:
            t0 = time.time()
            for r in forza(s0, sig, K):
                fz.append(r)
                scrivi(dict(r, tipo="forza_variante"))
                print("  la forza s0 %.2f banda %d eta %g (%d tick): dif %+.4e semis %+.2e | dif/a_H %.4f | dif/a_RG(c = 1) %.4f | <g> %.4f" % (r["s0"], r["banda"], r["eta"], r["tick"], r["differenziale"],
                                                                                                                                   r["semisomma"], r["dif_su_aH"], r["dif_su_aRG_luce"], r["gamma_medio"]))
            print("    (%.0fs)" % (time.time() - t0))
            sys.stdout.flush()
    l0 = lim["vb0_eps0"]["f0"]
    esito("PUO' FALLIRE: il limite di v_b/s (eps 0, ramo 0) entro %g da 1" % TOLL_VB1, abs(l0 - 1.0) <= TOLL_VB1, "%.10f" % l0, deve=False)
    sel = [rr["fattori"]["luce"]["F"] for r in righe if r["eps"] == 0.0 and r["s"] <= 0.1 for rr in r["rami"]]
    esito("PUO' FALLIRE: F con c = 1 entro %g da 1 a s <= 0.1 (eps 0)" % TOLL_F1, all(abs(f - 1) <= TOLL_F1 for f in sel), " ".join("%.4f" % f for f in sel), deve=False)
    sel = [r["dif_su_aRG_luce"] for r in fz if r["s0"] == S0_F[0]]
    esito("PUO' FALLIRE: la forza a_mis/a_RG(c = 1) entro %g da 1 a s0 %.2f" % (TOLL_RG, S0_F[0]), all(abs(v - 1) <= TOLL_RG for v in sel), " ".join("%.4f" % v for v in sel), deve=False)
    sel = [r["lambda_stella"] for r in righe if r["eps"] == 0.0]
    esito("PUO' FALLIRE: lambda* = 1/2 entro %g (eps 0)" % TOLL_LS, all(v is not None and abs(v - 0.5) <= TOLL_LS for v in sel), " ".join(U.f_(v, "%.8f") for v in sel), deve=False)
    return righe, lim, fz


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 120)
    print("IL TERZO PASSO DEL U(1): la larghezza del fascio, e la regola theta = s/x sui triangoli, in memoria")
    print("=" * 120)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_u1_prototipo.py", "csv/_u1_secondo.py", "csv/_u1_terzo.py", "csv/_triangoli.py", "csv/_triangoli_bassa_energia.py",
                                     "csv/_triangoli_forza.py", "csv/_triangoli_fattore.py", "csv/_triangoli_dove_la_luce.py", "csv/_scala_e_zero.py", "csv/_zero_simmetrico.py",
                                     "csv/_universalita_massa.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: parte 1: W_SCAN %s TOLL_RIP %g TOLL_EST %g; la scena di %s (LG2 %s S0 %.2f ETA %.2f N_FASCIO %s T_FASCIO %d N1_LUNGO %d T_LUNGO %d), F1"
          % (W_SCAN, TOLL_RIP, TOLL_EST, RIF_SEC, U2.LG2, U2.S0, U2.ETA, U2.N_FASCIO, U2.T_FASCIO, U2.N1_LUNGO, U2.T_LUNGO))
    print("    parte 2: S_VAR %s EPS_VAR %s S_RIP %s EPS_RIP %s H_DER %g S_DELTA %s S0_F %s LX_F %d ETA_F %s S_CHIAVE %.2f; lo zero simmetrico; TOLL_BIT %g TOLL_X %g TOLL_VB1 %g TOLL_F1 %g TOLL_RG %g TOLL_LS %g"
          % (S_VAR, EPS_VAR, S_RIP, EPS_RIP, H_DER, S_DELTA, S0_F, LX_F, ETA_F, S_CHIAVE, TOLL_BIT, TOLL_X, TOLL_VB1, TOLL_F1, TOLL_RG, TOLL_LS))
    print("-" * 120)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    parte_1()
    print("-" * 120)
    parte_2()
    print("-" * 120)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
