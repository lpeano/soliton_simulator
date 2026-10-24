# -*- coding: utf-8 -*-
r"""**IL PROTOTIPO U(1), SECONDO PASSO: il sigillo di gauge rifatto (le decisioni di Luca), la luce in un gradiente con le due forme del tempo dell'arco, il limite di `v_b` a `s`
piccolo** *([[U1-PROTOTIPO-TRIANGOLI]], [[PROGETTO-U1]], [[LORENTZ-MATERIA-INTERFERENZA]], [[DECISIONE-SOLO-TRIANGOLI]])*.

> ### ⛔ **Il task history e' `2026-10-24_u1_secondo.md`** *(il metodo, le previsioni, i criteri, fissati prima)*; ### **le decisioni di Luca: `2026-10-24_u1_prototipo.md`, sezione `6`.**
> ### **Importati, non copiati:** `_u1_prototipo` *(`Campo`, `scena_materia`, `avvolto`, `tick`, `tick_campo`, `rho_nodi`, `rel`, `scrivi_U`, `pacchetto_campo`, `blocchi_campo`, `omega_fotone`, `t_di`,
> `parte_G`, `u_K`)*, `_triangoli` *(`scena_toro`, `TRIANGOLI`)*, `_triangoli_forza` *(`conv`, `blocchi`, `coppia_K`, `v_max`, `matrice_L`)*, `_triangoli_fattore.ramo_lungo`. ### **Il fit di `v_b`** *(8 righe)*
> ### **e' riscritto perche' in `_triangoli_fattore` sta dentro `parte_A`** *(dichiarato nel task history)*.

| | la forma del tempo dell'arco | l'energia |
|---|---|---|
| `F1` | la spinta `rot^T g(B)`, la deriva `s_a^2 (l/l*) E` *(`0b6bfde8`)* | `somma s_a^2 (l/l*) E^2/2 + V` |
| `F2` | la spinta `rot^T (s_p g(B))`, la deriva `s_a (l/l*) E`; `s_p` la media armonica dei tre nodi *(la regola di PROVA)* | `somma s_a (l/l*) E^2/2 + somma s_p V_p` |

Gira con:  python csv/_u1_secondo.py > doc/referti_l2/u1_secondo.txt
"""
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

RIF_U1 = "0b6bfde8"
RIF_FATTORE = "7daa8840"
CONV = ("simm", "oggi")
S_GRIGLIA = (0.05, 0.1, 0.3)
E_PROVA = U.E_PROVA
N_B = 100
SCALA_J = (0, 1, 2, 3, 4)            # ### chi_max = (e/2) 10^-j, la lettura della scala
TOLL_REL = 1e-12
TOLL_ROTTA = 1e-9
# ### la parte 2: la scena nuova
LG2 = (384, 48)
S0 = 0.2
ETA = 0.2
W2 = 12.0
N1_LUNGO = 14                        # ### t1 = 2 pi 14/384: |k| = 0.2646, il piu' vicino a 2 pi/24
N_FASCIO = (-8, 2)                   # ### t1 = 2 pi (-8)/384, t2 = 2 pi 2/48: la lunghezza d'onda 24 lungo a2
T_LUNGO = 600
T_FASCIO = 400
FIN = 10
TOLL_V = 0.02
TOLL_DEF = 0.10
L_G_MAT = 24
S_G_MAT = 0.1
ETA_G_MAT = 0.2
N_G_MAT = 200
# ### la parte 3
S3 = (0.02, 0.01, 0.005, 0.002, 0.001)
S3_VICINO = 1e-4
S_RIF3 = 0.05
KMAX3 = 0.1
NK3 = 200
TOLL_RIF3 = 1e-6
TOLL_PI4 = 1e-4
JSONL = os.path.join(RADICE, "doc", "referti_l2", "u1_secondo.jsonl")
OK = [0, 0]
FALLITE = []
EPS64 = float(np.finfo(float).eps)


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


def avvolgi(x):
    return (x + np.pi) % (2.0 * np.pi) - np.pi


# =====================================================================================
#   LE DUE VARIANTI DEL CAMPO
# =====================================================================================
class CampoModulo(U.Campo):
    """### **Il COMPATTO con `A` modulo `2 pi/e`** *(la decisione `(1)` di Luca)*: ### **la riduzione dopo ogni deriva** *(e dopo la trasformazione, a mano)*."""

    def riduci(self):
        P = 2.0 * np.pi / self.e
        self.A[...] = self.A - P * np.round(self.A / P)

    def deriva(self, f):
        U.Campo.deriva(self, f)
        self.riduci()


class CampoF2(U.Campo):
    """### **`F2`, adattata in impedenza:** ### **la deriva `s_a (l/l*) E`, la spinta `rot^T (s_p g)`, `s_p = 3/(1/s_i + 1/s_j + 1/s_k)`** *(la regola di prova)*."""

    def __init__(self, ii, jj, lati, e, forma, s_a, s_nodi):
        U.Campo.__init__(self, ii, jj, lati, e, forma, s_a)
        L1, L2 = self.lati
        v = np.arange(self.n)
        m1, m2 = v // L2, v % L2

        def nb(d1, d2):
            return ((m1 + d1) % L1) * L2 + (m2 + d2) % L2
        sn = np.asarray(s_nodi, dtype=float)
        su = 3.0 / (1.0 / sn[v] + 1.0 / sn[nb(1, 0)] + 1.0 / sn[nb(1, 1)])
        giu = 3.0 / (1.0 / sn[v] + 1.0 / sn[nb(1, 1)] + 1.0 / sn[nb(0, 1)])
        self.s_p = np.concatenate([su, giu])
        self.w = self.s_a * U.L_SU_LS

    def forza(self):
        g = self.g(self.B()) * self.s_p
        return self.asg[:, 0] * g[self.ap[:, 0]] + self.asg[:, 1] * g[self.ap[:, 1]]

    def V(self):
        B = self.B()
        if self.forma == "compatto":
            return float(np.sum(self.s_p * (1.0 - np.cos(self.e * B)) / (self.e * self.e * U.AREA)))
        return float(np.sum(self.s_p * B * B / (2.0 * U.AREA)))

    def densita_V(self):
        B = self.B()
        v = (1.0 - np.cos(self.e * B)) / (self.e * self.e * U.AREA) if self.forma == "compatto" else B * B / (2.0 * U.AREA)
        return self.s_p * v


def densita_V(c):
    if isinstance(c, CampoF2):
        return c.densita_V()
    B = c.B()
    return (1.0 - np.cos(c.e * B)) / (c.e * c.e * U.AREA) if c.forma == "compatto" else B * B / (2.0 * U.AREA)


def energia_nodi(c):
    eV = densita_V(c)
    return (c.w * c.E * c.E / 2.0).reshape(c.n, 3).sum(axis=1) + eV[:c.n] + eV[c.n:]


def baricentro(c, prec):
    """### Come `_u1_prototipo.baricentro`, ### **con l'energia della forma** *(`F2` pesa `V` con `s_p`)*."""
    L1, L2 = c.lati
    w = energia_nodi(c)
    v = np.arange(c.n)
    m1, m2 = (v // L2).astype(float), (v % L2).astype(float)
    d1 = (m1 - prec[0] + L1 / 2.0) % L1 - L1 / 2.0
    d2 = (m2 - prec[1] + L2 / 2.0) % L2 - L2 / 2.0
    return (prec[0] + float(np.sum(w * d1) / np.sum(w)), prec[1] + float(np.sum(w * d2) / np.sum(w))), w


# =====================================================================================
#   PARTE 1 -- il sigillo di gauge
# =====================================================================================
def gauge(conv, s, forma, e, chi_max, modo, modulo):
    """### `modo`: `"chi"`, `"solo_psi"`, `"globale"`; ### **`chi` in `[-chi_max, chi_max)`**; ### **`modulo`: il compatto con `A` modulo `2 pi/e`.**"""
    import _triangoli_forza as TF
    rng = np.random.default_rng(U.SEME_CHI)
    Cl = CampoModulo if modulo else U.Campo
    with TF.conv(conv):
        out = []
        for k in range(2):
            _, mot, st, par, c0 = U.scena_materia(s, U.L_MAT, e, forma)
            c = Cl(c0.ii, c0.jj, c0.lati, e, forma, c0.s_a)
            out.append((mot, st, par, c))
        mot2, st2, _, c2 = out[1]
        chi = rng.uniform(-chi_max, chi_max, mot2.inc.n)
        if modo == "globale":
            chi[...] = chi[0]
        st2["psi_h"] *= np.exp(1j * chi[mot2.inc.nodo])[:, None]
        if modo == "chi":
            c2.A += (chi[c2.jj] - chi[c2.ii]) / e
        if modulo:
            c2.riduci()
        U.scrivi_U(mot2, c2)
        amax = float(np.max(np.abs(c2.A)))
        for mot, st, par, c in out:
            with U.avvolto(mot, c, True):
                for _ in range(N_B):
                    U.tick(st, mot, par, c)
    (mot1, st1, _, c1), (mot2, st2, _, c2) = out
    r = U.rel(U.rho_nodi(st1, mot1), U.rho_nodi(st2, mot2))
    eE = U.rel(c1.E, c2.E)
    eB = float(np.max(np.abs(avvolgi(e * c1.B() - e * c2.B())))) / (2.0 * np.pi)
    stima = N_B * 6.0 * EPS64 * max(amax, float(np.max(np.abs(c2.A)))) / U.AREA
    dE = float(np.max(np.abs(c1.E - c2.E)))
    return {"rho": r, "E": eE, "eB": eB, "max": max(r, eE, eB), "A_max": amax, "dE": dE, "stima": stima, "dE_su_stima": dE / stima if stima > 0 else None,
            "E_max": float(np.max(np.abs(c1.E)))}


def parte_1():
    print("### PARTE 1 -- IL SIGILLO DI GAUGE RIFATTO (la decisione (1) di Luca): (b1) compatto con A modulo 2 pi/e, chi in [-pi, pi); (b2) non compatto, chi_max = e/2; %d tick" % N_B)
    righe = []
    for conv in CONV:
        for s in S_GRIGLIA:
            for e in E_PROVA:
                b1 = gauge(conv, s, "compatto", e, math.pi, "chi", True)
                b2 = gauge(conv, s, "noncompatto", e, e / 2.0, "chi", False)
                bn = gauge(conv, s, "noncompatto", e, e / 2.0, "solo_psi", False)
                gr = gauge(conv, s, "noncompatto", e, math.pi, "chi", False)
                r = {"tipo": "gauge", "conv": conv, "s": s, "e": e, "b1_compatto_modulo": b1, "b2_noncompatto_piccolo": b2, "b_meno": bn, "grande_noncompatto": gr,
                     "chi_max_b2": e / 2.0, "carica": "norma", "tempo_campo": "F1"}
                scrivi(r)
                righe.append(r)
                print("  %-4s s %.2f e %.4f | (b1) rho %.1e eB %.1e E %.1e (max|A'| %.2f, |dE|/stima %.3f) | (b2) rho %.1e eB %.1e E %.1e (max|A'| %.3f, |dE|/stima %.3f) | (b-) %.1e | grande: E %.1e, |dE|/stima %.3f"
                      % (conv, s, e, b1["rho"], b1["eB"], b1["E"], b1["A_max"], b1["dE_su_stima"], b2["rho"], b2["eB"], b2["E"], b2["A_max"], b2["dE_su_stima"], bn["max"], gr["E"], gr["dE_su_stima"]))
                sys.stdout.flush()
    scala = []
    for e in E_PROVA:
        for j in SCALA_J:
            g = gauge("simm", S_GRIGLIA[0], "noncompatto", e, (e / 2.0) * 10.0 ** (-j), "chi", False)
            scala.append({"e": e, "j": j, "chi_max": (e / 2.0) * 10.0 ** (-j), **g})
            print("  LA SCALA (lettura) simm s %.2f e %.4f chi_max %.2e: max|A'| %.2e | E %.2e | rho %.1e eB %.1e | |dE|/stima %.3f" % (S_GRIGLIA[0], e, (e / 2.0) * 10.0 ** (-j), g["A_max"], g["E"], g["rho"], g["eB"], g["dE_su_stima"]))
    scrivi({"tipo": "gauge_scala", "righe": scala})
    p1 = max(r["b1_compatto_modulo"]["max"] for r in righe)
    esito("DEVE PASSARE (b1): compatto, A modulo 2 pi/e: rho, eB, E entro %g relativo, ogni riga" % TOLL_REL, p1 <= TOLL_REL,
          "il peggiore %.2e (E %.1e)" % (p1, max(r["b1_compatto_modulo"]["E"] for r in righe)))
    p2 = max(r["b2_noncompatto_piccolo"]["max"] for r in righe)
    esito("DEVE PASSARE (b2): non compatto, chi_max = e/2: rho, eB, E entro %g relativo, ogni riga" % TOLL_REL, p2 <= TOLL_REL,
          "il peggiore %.2e (E %.1e)" % (p2, max(r["b2_noncompatto_piccolo"]["E"] for r in righe)))
    nb = min(r["b_meno"]["max"] for r in righe)
    chiave = all(r["b2_noncompatto_piccolo"]["dE_su_stima"] <= 1.0 and r["b2_noncompatto_piccolo"]["rho"] <= TOLL_REL and r["b2_noncompatto_piccolo"]["eB"] <= TOLL_REL for r in righe)
    esito("DEVE FALLIRE (b-), PER LA CHIAVE GIUSTA: solo psi > %g, e la corsa intera con lo stesso chi sotto la stima (rho, eB entro %g)" % (TOLL_ROTTA, TOLL_REL), nb > TOLL_ROTTA and chiave,
          "(b-) il minimo %.2e; la chiave %s (|dE|/stima al piu' %.3f)" % (nb, chiave, max(r["b2_noncompatto_piccolo"]["dE_su_stima"] for r in righe)))
    return righe, scala


# =====================================================================================
#   PARTE 2 -- la luce in un gradiente
# =====================================================================================
def campo_gradiente(lati, s0, eta, forma_t, e, forma):
    import _triangoli as T
    import flussi_parziali as FP
    inc, mot, st, par = T.scena_toro(T.TRIANGOLI, lati, 1.0, T.X)
    m1 = np.arange(inc.n) // lati[1]
    cs = s0 * (1.0 + eta * np.cos(2.0 * np.pi * m1 / lati[0]))
    assert float(cs.max()) * math.sqrt(24.0) < 2.0, "una scena oltre Courant"
    mot.cs = cs
    mot.lambda_c = None
    s_a = FP.s_arco(mot).copy()
    ii, jj = inc.nodo[0::2].astype(np.int64), inc.nodo[1::2].astype(np.int64)
    c = CampoF2(ii, jj, lati, e, forma, s_a, cs) if forma_t == "F2" else U.Campo(ii, jj, lati, e, forma, s_a)
    return c, cs


def prepara(c, bl0, t0, W, r0, forma_t):
    spettro = U.pacchetto_campo(c, bl0, t0, W, r0, 1)
    if forma_t == "F2":
        c.E *= c.s_a                   # ### F2 = F1 con E -> s E (a s uniforme): il modo di F1 portato in F2
    return spettro


def corsa_lungo(lati, s0, eta, forma_t, bl0, T, n1, W, c0):
    L1, L2 = lati
    c, cs = campo_gradiente(lati, s0, eta, forma_t, 1.0, "noncompatto")
    prepara(c, bl0, (2 * np.pi * n1 / L1, 0.0), W, (L1 / 4.0, 0.0), forma_t)
    H0 = c.K() + c.V()
    D0 = c.div()
    Emax0 = float(np.max(np.abs(c.E)))
    pos, uu, ss, gauss = (L1 / 4.0, 0.0), [], [], 0.0
    for t in range(T + 1):
        if t:
            U.tick_campo(c)
            gauss = max(gauss, float(np.max(np.abs(c.div() - D0))) / Emax0)
        pos, w = baricentro(c, pos)
        uu.append(pos[0] * math.sqrt(3.0) / 2.0)
        ss.append(float(np.sum(w * cs) / np.sum(w)))
    uu, ss = np.array(uu), np.array(ss)
    v = (uu[2 * FIN:] - uu[:-2 * FIN]) / (2 * FIN)
    rr = v / ss[FIN:-FIN]
    tratto = float(uu[-1] - uu[0])
    m1 = (np.arange(c.n) // L2).astype(float)
    d = ((m1 - L1 / 4.0 + L1 / 2.0) % L1 - L1 / 2.0) * math.sqrt(3.0) / 2.0
    dietro = float(np.sum(w[(d < -4.0 * W) & (d > -tratto)]) / np.sum(w))
    out = {"forma_t": forma_t, "eta": eta, "v_su_cs_media": float(rr.mean()), "v_su_cs_min": float(rr.min()), "v_su_cs_max": float(rr.max()),
           "variazione": float((rr.max() - rr.min()) / rr.mean()), "tratto": tratto, "dietro": dietro, "gauss": gauss, "energia": (c.K() + c.V() - H0) / H0,
           "cs_visto": [float(ss.min()), float(ss.max())]}
    if c0 is not None:
        tp = float(np.sum(np.diff(uu) / (c0 * 0.5 * (ss[1:] + ss[:-1]))))
        out.update(T_previsto=tp, T_vero=T, T_rapporto=tp / T)
    return out


def corsa_fascio(lati, s0, eta, forma_t, bl0, T, nf, W):
    L1, L2 = lati
    c, cs = campo_gradiente(lati, s0, eta, forma_t, 1.0, "noncompatto")
    prepara(c, bl0, (2 * np.pi * nf[0] / L1, 2 * np.pi * nf[1] / L2), W, (L1 / 4.0, 0.0), forma_t)
    pos, uu = (L1 / 4.0, 0.0), []
    for t in range(T + 1):
        if t:
            U.tick_campo(c)
        pos, _ = baricentro(c, pos)
        uu.append(pos[0] * math.sqrt(3.0) / 2.0)
    tt = np.arange(T + 1, dtype=float)
    p = np.polyfit(tt, np.array(uu), 2)
    return {"forma_t": forma_t, "a": 2.0 * float(p[0]), "v0_trasversa": float(p[1])}


def c_lungo_a2(bl0, nf, lati, s0):
    """### La velocita' di gruppo lungo `a2` del `k` centrale del fascio, per tempo proprio, dai blocchi a `s0` uniforme."""
    import _triangoli_bassa_energia as BE
    t = np.array([2 * np.pi * nf[0] / lati[0], 2 * np.pi * nf[1] / lati[1]])
    k = np.linalg.inv(BE.J) @ t
    a = np.array([-0.5, math.sqrt(3.0) / 2.0])
    h = 1e-5
    wp = U.omega_fotone(bl0, *U.t_di(*(k + h * a)))
    wm = U.omega_fotone(bl0, *U.t_di(*(k - h * a)))
    return (wp - wm) / (2 * h) / s0


def gauss_materia(forma_t):
    """### **`(G)`: Gauss con la materia in un gradiente di `cs`** *(il pacchetto a `K` sul toro `24 x 24`, compatto, `e 0.3029`)*."""
    import _triangoli_forza as TF
    import flussi_parziali as FP
    e = E_PROVA[1]
    with TF.conv("simm"):
        _, mot, st, par, c0 = U.scena_materia(S_G_MAT, L_G_MAT, e, "compatto")
        m1 = np.arange(mot.inc.n) // L_G_MAT
        mot.cs = S_G_MAT * (1.0 + ETA_G_MAT * np.cos(2.0 * np.pi * m1 / L_G_MAT))
        s_a = FP.s_arco(mot).copy()
        c = CampoF2(c0.ii, c0.jj, c0.lati, e, "compatto", s_a, mot.cs) if forma_t == "F2" else U.Campo(c0.ii, c0.jj, c0.lati, e, "compatto", s_a)
        rho0 = U.rho_nodi(st, mot)
        c.E[...] = np.linalg.lstsq(c.matrice_div(), e * (rho0 - rho0.mean()), rcond=None)[0]
        G0 = c.div() - e * (rho0 - rho0.mean())
        scala = e * float(np.max(rho0))
        peg = 0.0
        with U.avvolto(mot, c, True):
            for _ in range(N_G_MAT):
                U.tick(st, mot, par, c)
                rho = U.rho_nodi(st, mot)
                peg = max(peg, float(np.max(np.abs(c.div() - e * (rho - rho.mean()) - G0))) / scala)
    return peg


def confronta(nuova, vecchia):
    peg = 0.0
    for k, v in vecchia.items():
        if isinstance(v, float):
            peg = max(peg, abs(nuova[k] - v) / max(abs(v), 1e-300))
    return peg


def parte_2():
    print("### PARTE 2 -- LA LUCE IN UN GRADIENTE DI cs, LE DUE FORME (F1 di %s, F2 adattata in impedenza)" % RIF_U1)
    gm = {f: gauss_materia(f) for f in ("F1", "F2")}
    esito("DEVE PASSARE (G): Gauss con la materia in un gradiente di cs (%d tick), F1 e F2, entro %g" % (N_G_MAT, TOLL_REL), max(gm.values()) <= TOLL_REL,
          "F1 %.2e F2 %.2e" % (gm["F1"], gm["F2"]))
    scrivi({"tipo": "gauss_gradiente_materia", "F1": gm["F1"], "F2": gm["F2"], "L": L_G_MAT, "s": S_G_MAT, "eta": ETA_G_MAT, "tick": N_G_MAT, "e": E_PROVA[1]})
    # ### la riproduzione: parte_G di _u1_prototipo, cosi' com'e', scrive nel jsonl NUOVO
    vecchie = {r["tipo"]: r for r in git_jsonl(RIF_U1, "doc/referti_l2/u1_prototipo.jsonl") if r.get("tipo") in ("shapiro", "deflessione")}
    U.JSONL = JSONL
    n_prima = sum(1 for _ in io.open(JSONL, encoding="utf-8"))
    bl02 = U.blocchi_campo(U.S0_G)[0]
    U.parte_G(bl02)
    nuove = {}
    for i, l in enumerate(io.open(JSONL, encoding="utf-8")):
        if i >= n_prima:
            r = json.loads(l)
            if r.get("tipo") in ("shapiro", "deflessione"):
                nuove[r["tipo"]] = r
    pr = max(confronta(nuove[k], vecchie[k]) for k in ("shapiro", "deflessione"))
    esito("DEVE PASSARE: _u1_prototipo.parte_G rigirata riproduce (g) di %s entro 1e-9, ogni numero" % RIF_U1, pr <= 1e-9, "%.1e" % pr)
    srv = corsa_lungo(U.LG, U.S0_G, U.ETA_G, "F1", bl02, U.T_G, U.N1_G, U.W_G, None)
    ds = abs(srv["v_su_cs_media"] - vecchie["shapiro"]["v_su_cs_media"]) / vecchie["shapiro"]["v_su_cs_media"]
    esito("SERVIZIO: lo strumento nuovo in F1 sulla scena vecchia = (g) di %s (v/cs media) entro 1e-9" % RIF_U1, ds <= 1e-9, "%.1e" % ds)
    # ### la scena nuova
    L1, L2 = LG2
    Lu = L1 * math.sqrt(3.0) / 2.0
    lung = Lu / (2 * np.pi) * math.sqrt(1 - ETA ** 2) / ETA
    print("  LA SCENA NUOVA: toro %dx%d (Lu %.1f), cs = %.2f (1 + %.2f cos), cs fra %.3f e %.3f (Courant 0.408), W %.1f, la lunghezza del gradiente %.1f = %.1f W; il lungo t1 = 2 pi %d/%d, %d tick; il fascio %s, %d tick"
          % (L1, L2, Lu, S0, ETA, S0 * (1 - ETA), S0 * (1 + ETA), W2, lung, lung / W2, N1_LUNGO, L1, T_LUNGO, N_FASCIO, T_FASCIO))
    bl0 = U.blocchi_campo(S0)[0]
    ctrl = {f: corsa_lungo(LG2, S0, 0.0, f, bl0, T_LUNGO, N1_LUNGO, W2, None) for f in ("F1", "F2")}
    c0 = ctrl["F1"]["v_su_cs_media"]
    righe = {}
    for f in ("F1", "F2"):
        r = corsa_lungo(LG2, S0, ETA, f, bl0, T_LUNGO, N1_LUNGO, W2, c0)
        r["riflessione"] = r["dietro"] - ctrl[f]["dietro"]
        r["controllo"] = ctrl[f]
        righe[f] = r
        print("  %s lungo il gradiente: v/cs media %.5f (%.5f..%.5f) variazione %.2e | T previsto/T %.5f | dietro %.2e (controllo %.2e): riflessione %.2e | Gauss %.1e | energia %.1e | c0 (controllo) %.5f"
              % (f, r["v_su_cs_media"], r["v_su_cs_min"], r["v_su_cs_max"], r["variazione"], r["T_rapporto"], r["dietro"], ctrl[f]["dietro"], r["riflessione"], r["gauss"], r["energia"],
                 ctrl[f]["v_su_cs_media"]))
    esito("DEVE PASSARE (G): Gauss senza materia nel gradiente, F1 e F2, entro %g di max|E|" % TOLL_REL, max(righe[f]["gauss"] for f in righe) <= TOLL_REL,
          "F1 %.1e F2 %.1e" % (righe["F1"]["gauss"], righe["F2"]["gauss"]))
    cp = c_lungo_a2(bl0, N_FASCIO, LG2, S0)
    u0m = L1 / 4.0
    k1 = 2 * np.pi * ETA / Lu * math.sin(2 * np.pi * u0m / L1) / (1 + ETA * math.cos(2 * np.pi * u0m / L1))
    cs0 = S0 * (1 + ETA * math.cos(2 * np.pi * u0m / L1))
    fasci = {}
    for f in ("F1", "F2"):
        fa = corsa_fascio(LG2, S0, ETA, f, bl0, T_FASCIO, N_FASCIO, W2)
        fa["kappa"] = fa["a"] / (cp * cs0) ** 2
        fa["kappa_R1"] = k1
        fa["kappa_R2"] = 2 * k1
        fa["su_R1"] = fa["kappa"] / k1
        fasci[f] = fa
        print("  %s la deflessione: d2u/dt2 %.4e, v_par = %.5f cs(u0) %.3f: kappa %.4e contro R1 (Soldner) %.4e e R2 (Einstein) %.4e: kappa/R1 %.4f" % (f, fa["a"], cp, cs0, fa["kappa"], k1, 2 * k1, fa["su_R1"]))
    scrivi({"tipo": "gradiente", "lati": LG2, "s0": S0, "eta": ETA, "W": W2, "lunghezza_gradiente": lung, "lungo": righe, "fascio": fasci, "c_par": cp, "n1": N1_LUNGO, "n_fascio": N_FASCIO})
    esito("PUO' FALLIRE: F1, il pacchetto stretto, v/cs costante entro %g" % TOLL_V, righe["F1"]["variazione"] <= TOLL_V, "%.2e (F2 %.2e)" % (righe["F1"]["variazione"], righe["F2"]["variazione"]), deve=False)
    esito("PUO' FALLIRE: la deflessione entro %g da R1, con F1" % TOLL_DEF, abs(fasci["F1"]["su_R1"] - 1) <= TOLL_DEF, "kappa/R1 F1 %.4f (F2 %.4f)" % (fasci["F1"]["su_R1"], fasci["F2"]["su_R1"]), deve=False)
    return righe, fasci


# =====================================================================================
#   PARTE 3 -- il limite di v_b
# =====================================================================================
def vb_di(s):
    """### `v_b` dei due rami della coppia a `K` *(il fit di `_triangoli_fattore.parte_A`: `omega^2 - omega0^2 = v_b^2 k^2 + b k^4`, `k_max`, `NK` punti)* ### **e `v_max`.**"""
    import _triangoli_fattore as F
    import _triangoli_forza as TF
    bl = TF.blocchi(0.0, s)
    vb = []
    for b in TF.coppia_K(0.0, s):
        qq, ww = F.ramo_lungo(bl, b["Q"], b["w"], KMAX3 * math.sqrt(3.0) / 2.0, NK3)
        k = qq * 2.0 / math.sqrt(3.0)
        y = ww ** 2 - b["w"] ** 2
        X = np.stack([k ** 2, k ** 4], axis=1)
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        vb.append(float(math.sqrt(c[0])) if c[0] > 0 else None)
    vm = TF.v_max(TF.matrice_L(0.0, s))[0]
    return vb, float(vm)


def parte_3():
    print("### PARTE 3 -- IL LIMITE DI v_b A s PICCOLO (eps 0, lo zero simmetrico; la coppia a K; v_max)")
    rif = [r for r in git_jsonl(RIF_FATTORE, "doc/referti_l2/triangoli_fattore.jsonl") if r.get("tipo") == "fattori" and r["eps"] == 0.0 and r["s"] == S_RIF3]
    vb05, _ = vb_di(S_RIF3)
    d = max(abs(vb05[r["banda"]] - r["fit"][str(KMAX3)]["v_b"]) / S_RIF3 for r in rif)
    esito("DEVE PASSARE: a s %.2f v_b/s riproduce %s entro %g (i due rami)" % (S_RIF3, RIF_FATTORE, TOLL_RIF3), d <= TOLL_RIF3 and len(rif) == 2,
          "%s contro %s: %.1e" % (" ".join("%.6f" % (v / S_RIF3) for v in vb05), " ".join("%.6f" % (r["fit"][str(KMAX3)]["v_b"] / S_RIF3) for r in sorted(rif, key=lambda r: r["banda"])), d))
    tab = []
    for s in S3 + (S3_VICINO,):
        t0 = time.time()
        vb, vm = vb_di(s)
        tab.append({"s": s, "vb_su_s": [v / s for v in vb], "vmax_su_s": vm / s})
        print("  s %-7g v_b/s %s | v_max/s %.8f | %.0fs" % (s, " ".join("%.8f" % (v / s) for v in vb), vm / s, time.time() - t0))
        sys.stdout.flush()
    ss = np.array(S3)
    lim = {}
    for nome, ys in (("vb0", [r["vb_su_s"][0] for r in tab[:len(S3)]]), ("vb1", [r["vb_su_s"][1] for r in tab[:len(S3)]]), ("vmax", [r["vmax_su_s"] for r in tab[:len(S3)]])):
        ys = np.array(ys)
        p = np.polyfit(ss, ys, 2)
        q, *_ = np.linalg.lstsq(np.stack([np.ones_like(ss), ss ** 2], axis=1), ys, rcond=None)
        lim[nome] = {"libero": {"f0": float(p[2]), "f1": float(p[1]), "f2": float(p[0])}, "pari": {"f0": float(q[0]), "f2": float(q[1])}}
        print("  il limite di %-4s: libero f0 %.10f f1 %+.3e f2 %+.3e | pari f0 %.10f f2 %+.3e | contro pi/4: %+.3e (libero) %+.3e (pari)"
              % (nome, p[2], p[1], p[0], q[0], q[1], p[2] - math.pi / 4, q[0] - math.pi / 4))
    scrivi({"tipo": "limite_vb", "tabella": tab, "limiti": lim, "pi_su_4": math.pi / 4, "kmax": KMAX3, "nk": NK3})
    esito("PUO' FALLIRE: il limite di v_b/s (ramo 0, fit libero) entro %g da pi/4" % TOLL_PI4, abs(lim["vb0"]["libero"]["f0"] - math.pi / 4) <= TOLL_PI4,
          "%.8f contro %.8f" % (lim["vb0"]["libero"]["f0"], math.pi / 4), deve=False)
    return tab, lim


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 120)
    print("IL PROTOTIPO U(1), SECONDO PASSO: il sigillo di gauge rifatto, la luce in un gradiente con le due forme del tempo dell'arco, il limite di v_b a s piccolo")
    print("=" * 120)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_u1_prototipo.py", "csv/_u1_secondo.py", "csv/_triangoli.py", "csv/_triangoli_bassa_energia.py", "csv/_triangoli_forza.py",
                                     "csv/_triangoli_fattore.py", "csv/_zero_simmetrico.py", "csv/_universalita_massa.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: RIF_U1 %s RIF_FATTORE %s; CONV %s; S %s; E_PROVA %s; N_B %d; SCALA_J %s; TOLL_REL %g TOLL_ROTTA %g; la carica: la norma"
          % (RIF_U1, RIF_FATTORE, CONV, S_GRIGLIA, tuple(round(e, 6) for e in E_PROVA), N_B, SCALA_J, TOLL_REL, TOLL_ROTTA))
    print("    parte 2: LG2 %s S0 %.2f ETA %.2f W2 %.1f N1_LUNGO %d N_FASCIO %s T_LUNGO %d T_FASCIO %d FIN %d TOLL_V %g TOLL_DEF %g; (G) L %d s %.2f eta %.2f %d tick"
          % (LG2, S0, ETA, W2, N1_LUNGO, N_FASCIO, T_LUNGO, T_FASCIO, FIN, TOLL_V, TOLL_DEF, L_G_MAT, S_G_MAT, ETA_G_MAT, N_G_MAT))
    print("    parte 3: S3 %s S3_VICINO %g S_RIF3 %.2f KMAX3 %g NK3 %d TOLL_RIF3 %g TOLL_PI4 %g; eps 0, lo zero simmetrico" % (S3, S3_VICINO, S_RIF3, KMAX3, NK3, TOLL_RIF3, TOLL_PI4))
    print("-" * 120)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    for s in S_GRIGLIA + (S_G_MAT,):
        U.u_K(s)                      # ### fuori da ogni convenzione (annotazione 3 di 2026-10-24_u1_prototipo.md)
    parte_1()
    print("-" * 120)
    parte_2()
    print("-" * 120)
    parte_3()
    print("-" * 120)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
