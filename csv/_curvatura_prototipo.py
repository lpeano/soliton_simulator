# -*- coding: utf-8 -*-
r"""**IL PROTOTIPO DELLA CURVATURA DELLO SPAZIO SUI TRIANGOLI, IN MEMORIA (LA STRADA `A1`: `cs` nelle lunghezze)** *([[PROGETTO-CURVATURA]], [[U1-PROTOTIPO-TRIANGOLI]], [[PROGETTO-U1]],
[[LORENTZ-MATERIA-INTERFERENZA]], [[DECISIONE-SOLO-TRIANGOLI]])*.

> ### ⛔ **Il task history e' `2026-10-25_curvatura_prototipo.md`** *(`f4fb6582`: il metodo, le previsioni, i criteri)*; ### **il progetto `doc/PROGETTO_CURVATURA.md`** *(`dc56d417`)*.
> ### **LE SCELTE DI PROVA DI LUCA** *(`2026-10-25`, `16:26`; per il prototipo, NON leggi)*: ### **`A1`; `cs_rif` = il vuoto imperturbato; l'area con Erone; i versori fissi.**
> ### **`A1` IN MEMORIA:** ### **`flussi_parziali.s_arco` avvolta: `s_a (s_a/s_rif)`** *(l'angolo dello SPOSTAMENTO, della materia e del vuoto, e' `pi s_a r_a f`; il nodo resta `pi s_n`)*; ### **il campo `CampoA1`:
> l'area per placchetta `(sqrt3/4) Erone(l)/Erone(1,1,1)`, `l_a = s_rif/s_a`.** ### **Nessun file del nucleo cambia; `B-4` intatta.**
> ### **Importati, non copiati:** `_u1_terzo` *(`H_gen`, `variante` come modello)*, `_u1_secondo` *(`campo_gradiente`, `prepara`, `baricentro`, `c_lungo_a2`, la scena)*, `_u1_prototipo` *(`Campo`, `scena_materia`,
> `avvolto`, `tick`, `tick_campo`, `rho_nodi`, `rel`, `scrivi_U`, `rovescia`, `energia`, `pacchetto_campo`, `blocchi_campo`, `u_K`)*, `_triangoli_forza` *(`corsa_con`, `coppia_K`, `blocchi`, `pacchetto_banda`, `spazi_banda`)*,
> `_triangoli_fattore.ramo_lungo`, `_triangoli_bassa_energia` *(`matrice`, `J`)*.

Gira con:  python csv/_curvatura_prototipo.py parte0 > doc/referti_l2/curvatura_x_r.txt
           python csv/_curvatura_prototipo.py parte1 > doc/referti_l2/curvatura_prototipo.txt
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
import _u1_terzo as U3                                         # noqa: E402

RIF_FATTORE = "7daa8840"
R_LISTA = (0.5, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.25, 2.0)
R_SPETTRI = (0.8, 1.0, 1.25)
S_SPETTRI = 0.01
PASSI_R = 200
K_FINE = U3.K_FINE
NK = U2.NK3
H_R = 1e-4
TOLL_X1 = 1e-9
TOLL_XR = 1e-6
TOLL_SPETTRI = 1e-3
TOLL_B = 1e-6
TOLL_BIT = 1e-12
TOLL_REL = 1e-12
TOLL_ROTTA = 1e-9
R_CHIAVE = 1.1
N_A = 20
N_G = 200
N_REV = 100
N_EN = 500
L_M = 24
S_M = 0.1
ETA_M = 0.2
E_M = U.E_PROVA[1]
W_SCAN = (12.0, 16.0, 24.0)
TOLL_GAMMA = 0.05
TOLL_R1 = 0.10
S0_F = (0.05, 0.1, 0.3)
S0_EPS = 0.1
LX_F = 96
ETA_F = (0.0, 1e-3, -1e-3, 1e-2, -1e-2)
TOLL_CADUTA = 0.02
J0 = os.path.join(RADICE, "doc", "referti_l2", "curvatura_x_r.jsonl")
J1 = os.path.join(RADICE, "doc", "referti_l2", "curvatura_prototipo.jsonl")
JSONL = [J0]
OK = [0, 0]
FALLITE = []
EPS64 = float(np.finfo(float).eps)
VERO = [None]                    # ### `flussi_parziali.s_arco` VERO mentre `a1` e' accesa: il tempo del campo (`F1`) lo legge sempre


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-100s %s   %s" % (che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL[0], "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def git_jsonl(rif, rel):
    out = subprocess.run(["git", "show", "%s:%s" % (rif, rel)], capture_output=True, cwd=RADICE, check=True).stdout.decode("utf-8")
    return [json.loads(x) for x in out.splitlines() if x.strip()]


# =====================================================================================
#   LA VARIANTE A1, IN MEMORIA
# =====================================================================================
@contextlib.contextmanager
def a1(s_rif):
    """### **`s_arco` -> `s_a (s_a/s_rif)`:** ### **l'angolo dello spostamento e' `pi s_a r_a f`.** ### **A `s_a = s_rif` e' `s_a x 1.0`, esatto.** ### **La cache dei blocchi si svuota.**"""
    import _triangoli_forza as TF
    import flussi_parziali as FP
    vero = FP.s_arco

    def s_arco(mot):
        s = vero(mot)
        np.multiply(s, s / s_rif, out=s)
        return s
    TF._CACHE.clear()
    FP.s_arco = s_arco
    VERO[0] = vero
    try:
        yield
    finally:
        FP.s_arco = vero
        VERO[0] = None
        TF._CACHE.clear()


@contextlib.contextmanager
def a1_da_z_arco(r):
    """### **LA STESSA VARIANTE COSTRUITA ALTROVE** *(il controllo della chiave di `(a)`)*: ### **`z_arco` con `s_arco` moltiplicato per `r`** *(a `cs` uniforme)*."""
    import flussi_parziali as FP
    vero = FP.z_arco

    def z_arco(mot, frazione):
        f = FP._frazione_valida(frazione)
        s = FP.s_arco(mot) * r
        np.multiply(s, f, out=s)
        z = mot._b("fp_z_arco", (mot.inc.m, 1), complex)
        return FP.espi(s.reshape(-1, 1), z, mot._b("fp_w_arco", (mot.inc.m, 1), float))
    FP.z_arco = z_arco
    try:
        yield
    finally:
        FP.z_arco = vero


def erone(a, b, c):
    p = 0.5 * (a + b + c)
    return np.sqrt(p * (p - a) * (p - b) * (p - c))


class CampoA1(U.Campo):
    """### **Il campo con le lunghezze `l_a = s_rif/s_a`:** ### **l'area per placchetta `(sqrt3/4) Erone(l)/Erone(1,1,1)`** *(il tempo resta `F1`: la deriva `s_a^2 (l/l*)`, `l*/l` fisso perche' in 2D la stella dei
    `1`-forme e' invariante conforme)*."""

    def __init__(self, ii, jj, lati, e, forma, s_a, s_rif):
        U.Campo.__init__(self, ii, jj, lati, e, forma, s_a)
        l = s_rif / self.s_a
        P = self.P
        self.Ap = U.AREA * (erone(l[P[:, 0]], l[P[:, 1]], l[P[:, 2]]) / erone(1.0, 1.0, 1.0))

    def g(self, B):
        if self.forma == "compatto":
            return np.sin(self.e * B) / (self.e * self.Ap)
        return B / self.Ap

    def V(self):
        B = self.B()
        if self.forma == "compatto":
            return float(np.sum((1.0 - np.cos(self.e * B)) / (self.e * self.e * self.Ap)))
        return float(np.sum(B * B / (2.0 * self.Ap)))

    def densita_V(self):
        B = self.B()
        return (1.0 - np.cos(self.e * B)) / (self.e * self.e * self.Ap) if self.forma == "compatto" else B * B / (2.0 * self.Ap)


class _Ombra(object):
    """### **Per `_u1_prototipo.energia`:** ### **il peso dello spostamento e' `s_a r_a`** *(l'angolo di `A1`)*, ### **il campo e' quello vero.**"""

    def __init__(self, c, s_spost):
        self.c, self.s_a = c, s_spost

    def u(self):
        return self.c.u()

    def K(self):
        return self.c.K()

    def V(self):
        return self.c.V()


# =====================================================================================
#   PARTE 0 -- x(r) DAL GENERATORE
# =====================================================================================
def H_r(t1, t2, r):
    """### **`H_r = (I - P_u) + r P_-`** *(`P_- = _u1_terzo.H_gen - (I - P_u)`)*."""
    I_Pu = np.eye(6) - np.ones((6, 6)) / 6.0
    return I_Pu + r * (U3.H_gen(t1, t2) - I_Pu)


def mu_di(t1, t2, r):
    lam, V = np.linalg.eigh(H_r(t1, t2, r))
    return (1.0 + r) / 2.0 - lam, V


def coppia_r(r):
    """### **La coppia a `K` seguita in `r` per continuita'** *(dai livelli `mu0 = +-1/2` a `r = 1`, a `PASSI_R` passi, per sovrapposizione)*: `[(mu0, v)]`."""
    import _triangoli_forza as TF
    tK = TF.theta_di("A", 0.0)
    mu, V = mu_di(tK[0], tK[1], 1.0)
    idx = [int(np.argmin(np.abs(mu - 0.5))), int(np.argmin(np.abs(mu + 0.5)))]
    vv = [V[:, [i]] for i in idx]
    for rr in np.linspace(1.0, r, PASSI_R + 1)[1:]:
        mu, V = mu_di(tK[0], tK[1], rr)
        nuovi = []
        for v in vv:
            j = int(np.argmax(np.abs(V.conj().T @ v)[:, 0]))
            nuovi.append(V[:, [j]])
        vv = nuovi
    mu, V = mu_di(tK[0], tK[1], r)
    out = []
    for v in vv:
        j = int(np.argmax(np.abs(V.conj().T @ v)[:, 0]))
        out.append((float(mu[j]), V[:, [j]]))
    return out


def x_di(r):
    """### **`x(r) = sqrt(2 mu0 a)`** *(la curvatura fine di `_u1_terzo`: `mu - mu0 = a k^2 + b k^4 + c k^6` a `k <= K_FINE`, lungo la normale ad `a2`)*."""
    import _triangoli_forza as TF
    out = []
    for mu0, v in coppia_r(r):
        qq = np.linspace(0.0, K_FINE * math.sqrt(3.0) / 2.0, NK + 1)
        mm = []
        for q in qq:
            mu, V = mu_di(*TF.theta_di("A", q), r)
            j = int(np.argmax(np.abs(V.conj().T @ v)[:, 0]))
            mm.append(mu[j])
            v = V[:, [j]]
        k = qq * 2.0 / math.sqrt(3.0)
        X = np.stack([k ** 2, k ** 4, k ** 6], axis=1)
        cc, *_ = np.linalg.lstsq(X, np.array(mm) - mm[0], rcond=None)
        x2 = 2.0 * mm[0] * cc[0]
        out.append({"mu0": mu0, "a": float(cc[0]), "x": float(math.sqrt(x2)) if x2 > 0 else None})
    return out


def spettri_a1(r, s):
    """### **Gli spettri completi con `A1` a `cs` uniforme** *(`s_rif = s/r`)*: ### **la coppia a `K` piu' vicina a `pi s mu0(r)`, e `v_b` col fit di `_u1_terzo.vb_eps`.**"""
    import _triangoli_bassa_energia as BE
    import _triangoli_fattore as F
    import _triangoli_forza as TF
    out = []
    pred = coppia_r(r)
    with a1(s / r):
        A = BE.matrice(0.0, s, U3.LF, "simm")[U3.KF[0], U3.KF[1], :12, :12]
        lam, V = np.linalg.eig(A)
        w = -np.angle(lam)
        bl = TF.blocchi(0.0, s)
        for mu0, _v in pred:
            wp = np.pi * s * mu0
            idx = [int(i) for i in np.argsort(np.abs(w - wp))[:2]]
            Q = np.linalg.qr(V[:, idx])[0]
            w0 = float(np.mean(w[idx]))
            qq, ww = F.ramo_lungo(bl, Q, w0, U2.KMAX3 * math.sqrt(3.0) / 2.0, U2.NK3)
            k = qq * 2.0 / math.sqrt(3.0)
            y = ww ** 2 - w0 ** 2
            X = np.stack([k ** 2, k ** 4], axis=1)
            c, *_ = np.linalg.lstsq(X, y, rcond=None)
            out.append({"mu0": mu0, "w0": w0, "w_previsto": wp, "doppio": float(abs(w[idx[0]] - w[idx[1]])), "v_b_su_s": float(math.sqrt(c[0])) / s if c[0] > 0 else None})
    return out


def parte_0():
    print("### PARTE 0 -- LA PROVA DELL'OBIEZIONE DI LUCA DAGLI SPETTRI: x(r) dal generatore (I - P_u) + r P_-, lo zero simmetrico (mu = (1+r)/2 - lambda), eps 0")
    tab = []
    for r in R_LISTA:
        xs = x_di(r)
        tab.append({"r": r, "rami": xs, "rapporto": [np.pi * x["x"] / r for x in xs], "x_su_r4": [x["x"] / (r / 4.0) for x in xs]})
        print("  r %-5g | mu0 %s | x %s | x/(r/4) %s | il rapporto pi x/r %s (pi/4 = %.6f)"
              % (r, " ".join("%+.8f" % x["mu0"] for x in xs), " ".join("%.10f" % x["x"] for x in xs), " ".join("%.6f" % (x["x"] / (r / 4.0)) for x in xs),
                 " ".join("%.6f" % (np.pi * x["x"] / r) for x in xs), np.pi / 4))
        sys.stdout.flush()
    scrivi({"tipo": "x_r", "tabella": tab})
    x1 = [x["x"] for x in [t for t in tab if t["r"] == 1.0][0]["rami"]]
    esito("DEVE PASSARE: x(1) = 1/4 entro %g (i due rami)" % TOLL_X1, all(abs(x - 0.25) <= TOLL_X1 for x in x1), " ".join("%.12f" % x for x in x1))
    peg = max(abs(x["x"] - r["r"] / 4.0) for r in tab for x in r["rami"])
    esito("PUO' FALLIRE: x(r) = r/4 entro %g a ogni r (la previsione del guardiano)" % TOLL_XR, peg <= TOLL_XR, "lo scarto peggiore %.3e" % peg, deve=False)
    # ### da dove viene la massa
    dm = []
    for q in range(2):
        mp = x_di(1.0 + H_R)[q]["mu0"]
        mm = x_di(1.0 - H_R)[q]["mu0"]
        m0 = x_di(1.0)[q]["mu0"]
        dm.append((mp - mm) / (2 * H_R) / m0)
    print("  DA DOVE VIENE LA MASSA: d ln mu0/d ln r a r = 1 = %s (0 = solo il nodo)" % " ".join("%+.6f" % d for d in dm))
    # ### la forma della funzione x(r): la potenza locale
    rr = np.array([t["r"] for t in tab])
    xx = np.array([t["rami"][0]["x"] for t in tab])
    p = np.polyfit(np.log(rr), np.log(xx), 1)
    print("  LA FORMA: ln x contro ln r, la pendenza %.6f, l'intercetta exp %.6f (x = r/4 vorrebbe 1 e 0.25); il residuo massimo %.2e"
          % (p[0], math.exp(p[1]), float(np.max(np.abs(np.polyval(p, np.log(rr)) - np.log(xx))))))
    scrivi({"tipo": "massa_e_forma", "dlnmu0_dlnr": dm, "pendenza": float(p[0]), "intercetta": float(math.exp(p[1]))})
    # ### gli spettri completi
    peg = 0.0
    for r in R_SPETTRI:
        sp = spettri_a1(r, S_SPETTRI)
        xr = x_di(r)
        for q, b in enumerate(sp):
            d = abs(b["v_b_su_s"] / (np.pi * xr[q]["x"]) - 1.0)
            peg = max(peg, d)
        scrivi({"tipo": "spettri", "r": r, "s": S_SPETTRI, "rami": sp, "x": xr})
        print("  SPETTRI r %-5g s %g: w0 %s (previsto %s, il doppio %s) | v_b/s %s contro pi x(r) %s"
              % (r, S_SPETTRI, " ".join("%+.6e" % b["w0"] for b in sp), " ".join("%+.6e" % b["w_previsto"] for b in sp), " ".join("%.1e" % b["doppio"] for b in sp),
                 " ".join("%.8f" % b["v_b_su_s"] for b in sp), " ".join("%.8f" % (np.pi * x["x"]) for x in xr)))
    esito("DEVE PASSARE: gli spettri completi con A1 (s %g) danno v_b/s = pi x(r) entro %g relativo a r in %s" % (S_SPETTRI, TOLL_SPETTRI, R_SPETTRI), peg <= TOLL_SPETTRI, "%.2e" % peg)
    # ### la variante B: la materia non sente r
    vb_oggi = spettri_a1(1.0, S_SPETTRI)
    rap = [vb_oggi[0]["v_b_su_s"] / r for r in R_LISTA]
    cost = (max(rap) - min(rap)) / np.mean(rap)
    chiave = max(abs(rap[i] * R_LISTA[i] - vb_oggi[0]["v_b_su_s"]) for i in range(len(R_LISTA))) / vb_oggi[0]["v_b_su_s"]
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA: B (solo il campo), il rapporto delle due c costante in r; la chiave: rapporto x r = v_b/s di oggi entro %g" % TOLL_B,
          cost > 1e-3 and chiave <= TOLL_B, "variazione %.3f, la chiave %.1e" % (cost, chiave))
    scrivi({"tipo": "variante_B", "rapporti": rap, "r": list(R_LISTA)})
    return tab


# =====================================================================================
#   PARTE 1
# =====================================================================================
def scena_m(s_nodi_fn, forma, e, classe_campo, s_rif):
    """### La scena della materia di `_u1_prototipo.scena_materia`, ### **col `cs` per nodo dato e il campo `A1`** *(il tempo del campo `F1` dal `s_arco` VERO, prima della variante)*."""
    import flussi_parziali as FP
    inc, mot, st, par, c0 = U.scena_materia(S_M, L_M, e, forma)
    m1 = np.arange(mot.inc.n) // L_M
    mot.cs = s_nodi_fn(m1)
    s_a = (VERO[0] or FP.s_arco)(mot).copy()
    c = classe_campo(c0.ii, c0.jj, c0.lati, e, forma, s_a, s_rif) if classe_campo is CampoA1 else U.Campo(c0.ii, c0.jj, c0.lati, e, forma, s_a)
    return inc, mot, st, par, c


def parte_a():
    import _triangoli_forza as TF
    import tick as TK
    print("### (a) cs = cs_rif ovunque: il passo di oggi AL BIT con A1 accesa (materia e campo, %d tick, e %.4f, compatto)" % (N_A, E_M))
    unif = lambda m1: np.full(len(m1), S_M)
    with TF.conv("simm"):
        _, motR, stR, parR, cR = scena_m(unif, "compatto", E_M, None, S_M)
        with U.avvolto(motR, cR, True):
            for _ in range(N_A):
                U.tick(stR, motR, parR, cR)
        _, motF, stF, parF, cF = scena_m(unif, "compatto", E_M, CampoA1, S_M)
        with a1(S_M):
            with U.avvolto(motF, cF, True):
                for _ in range(N_A):
                    U.tick(stF, motF, parF, cF)
    ba, bb = TF.byte_attr(motR), TF.byte_attr(motF)
    dm = sorted(k for k in set(ba) | set(bb) if ba.get(k) != bb.get(k))
    ds = sorted(k for k in stR if stR[k].tobytes() != stF[k].tobytes())
    dc = [k for k in ("A", "E") if getattr(cR, k).tobytes() != getattr(cF, k).tobytes()]
    esito("DEVE PASSARE (a): A1 a cs = cs_rif = il passo di oggi AL BIT (st, %d attributi di mot, A ed E del campo)" % len(ba), not dm and not ds and not dc, "diversi: mot %s st %s campo %s" % (dm[:3], ds, dc))
    # ### la chiave: cs uniforme = 1.1 cs_rif
    with TF.conv("simm"):
        _, mo, so, po, _c = scena_m(unif, "compatto", 0.0, None, S_M)
        TK.percorri_tick(so, mo, po, ("CAMM-MATERIA-VUOTO",), None, 14)
        _, mv, sv, pv, _c = scena_m(unif, "compatto", 0.0, None, S_M)
        with a1(S_M / R_CHIAVE):
            TK.percorri_tick(sv, mv, pv, ("CAMM-MATERIA-VUOTO",), None, 14)
        _, mz, sz, pz, _c = scena_m(unif, "compatto", 0.0, None, S_M)
        with a1_da_z_arco(R_CHIAVE):
            TK.percorri_tick(sz, mz, pz, ("CAMM-MATERIA-VUOTO",), None, 14)
    d1 = U.rel(so["psi_h"], sv["psi_h"])
    d2 = U.rel(sz["psi_h"], sv["psi_h"])
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA: cs = %.1f cs_rif e' il passo di oggi (> 1e-6); E = lo spostamento con l'angolo pi s r costruito in z_arco entro %g" % (R_CHIAVE, TOLL_BIT),
          d1 > 1e-6 and d2 <= TOLL_BIT, "contro oggi %.2e; contro z_arco %.1e" % (d1, d2))
    scrivi({"tipo": "a", "mot_diversi": dm, "st_diversi": ds, "campo_diversi": dc, "chiave_oggi": d1, "chiave_z_arco": d2})


def parte_b():
    import _triangoli_forza as TF
    print("### (b) Gauss, la gauge, la reversibilita', l'energia: la materia in un gradiente cs = %.2f (1 + %.2f cos), A1 (s_rif %.2f), il campo F1 con Erone, e %.4f compatto" % (S_M, ETA_M, S_M, E_M))
    grad = lambda m1: S_M * (1.0 + ETA_M * np.cos(2.0 * np.pi * m1 / L_M))
    e = E_M
    out = {}
    with TF.conv("simm"):
        with a1(S_M):
            _, mot, st, par, c = scena_m(grad, "compatto", e, CampoA1, S_M)
            rho0 = U.rho_nodi(st, mot)
            c.E[...] = np.linalg.lstsq(c.matrice_div(), e * (rho0 - rho0.mean()), rcond=None)[0]
            G0 = c.div() - e * (rho0 - rho0.mean())
            sc = e * float(np.max(rho0))
            peg = 0.0
            import flussi_parziali as FP
            s_spost = FP.s_arco(mot).copy()
            s_n = mot.cs.copy()
            en = [U.energia(st, mot, _Ombra(c, s_spost), "simm", s_n)]
            with U.avvolto(mot, c, True):
                for t in range(N_EN):
                    U.tick(st, mot, par, c)
                    if t < N_G:
                        rho = U.rho_nodi(st, mot)
                        peg = max(peg, float(np.max(np.abs(c.div() - e * (rho - rho.mean()) - G0))) / sc)
                    en.append(U.energia(st, mot, _Ombra(c, s_spost), "simm", s_n))
            en = np.array(en)
            tt = np.arange(len(en), dtype=float)
            pp = np.polyfit(tt, en, 1)
            res = en - np.polyval(pp, tt)
            out["gauss"] = peg
            out["energia"] = {"deriva": float(abs(pp[0]) * N_EN), "ampiezza": float(res.max() - res.min()), "media": float(en.mean())}
            # ### la gauge, chi casuale
            rng = np.random.default_rng(U.SEME_CHI)
            sc2 = []
            for k in range(2):
                sc2.append(scena_m(grad, "compatto", e, CampoA1, S_M))
            _, m2, s2, p2, c2 = sc2[1]
            chi = rng.uniform(-math.pi, math.pi, m2.inc.n)
            s2["psi_h"] *= np.exp(1j * chi[m2.inc.nodo])[:, None]
            c2.A += (chi[c2.jj] - chi[c2.ii]) / e
            U.scrivi_U(m2, c2)
            amax = float(np.max(np.abs(c2.A)))
            for _, mm, ss, pq, cc in sc2:
                with U.avvolto(mm, cc, True):
                    for _ in range(U2.N_B):
                        U.tick(ss, mm, pq, cc)
            (_, m1_, s1_, _, c1_), (_, m2_, s2_, _, c2_) = sc2
            stima = U2.N_B * 6.0 * EPS64 * max(amax, float(np.max(np.abs(c2_.A)))) / U.AREA
            out["gauge"] = {"rho": U.rel(U.rho_nodi(s1_, m1_), U.rho_nodi(s2_, m2_)), "eB": float(np.max(np.abs(U2.avvolgi(e * c1_.B() - e * c2_.B())))) / (2 * np.pi),
                            "dE": float(np.max(np.abs(c1_.E - c2_.E))), "stima": stima}
            # ### la reversibilita'
            _, mot, st, par, c = scena_m(grad, "compatto", e, CampoA1, S_M)
            rho0 = U.rho_nodi(st, mot)
            c.E[...] = np.linalg.lstsq(c.matrice_div(), e * (rho0 - rho0.mean()), rcond=None)[0]
            psi0, A0, E0 = st["psi_h"].copy(), c.A.copy(), c.E.copy()
            am = 0.0
            with U.avvolto(mot, c, True):
                for _ in range(N_REV):
                    U.tick(st, mot, par, c)
                    am = max(am, float(np.max(np.abs(c.A))))
                U.rovescia(st, mot, c)
                for _ in range(N_REV):
                    U.tick(st, mot, par, c)
                U.rovescia(st, mot, c)
            out["rev"] = max(U.rel(psi0, st["psi_h"]), U.rel(A0, c.A, am), U.rel(E0, c.E))
    g = out["gauge"]
    print("  Gauss %.2e | gauge rho %.1e eB %.1e |dE| %.2e stima %.2e | rev %.2e | energia: deriva %.2e ampiezza %.2e (media %.5f)"
          % (out["gauss"], g["rho"], g["eB"], g["dE"], g["stima"], out["rev"], out["energia"]["deriva"], out["energia"]["ampiezza"], out["energia"]["media"]))
    esito("DEVE PASSARE (b): Gauss entro %g per %d tick" % (TOLL_REL, N_G), out["gauss"] <= TOLL_REL, "%.2e" % out["gauss"])
    esito("DEVE PASSARE (b): la gauge, rho ed eB entro %g e |dE| <= la stima" % TOLL_REL, g["rho"] <= TOLL_REL and g["eB"] <= TOLL_REL and g["dE"] <= g["stima"], "|dE|/stima %.3f" % (g["dE"] / g["stima"]))
    esito("DEVE PASSARE (b): la reversibilita' %d + %d entro %g" % (N_REV, N_REV, TOLL_REL), out["rev"] <= TOLL_REL, "%.2e" % out["rev"])
    esito("DEVE PASSARE (b): l'energia senza deriva (|pendenza| %d <= ampiezza/2)" % N_EN, out["energia"]["deriva"] <= out["energia"]["ampiezza"] / 2.0,
          "deriva/ampiezza %.3f" % (out["energia"]["deriva"] / out["energia"]["ampiezza"]))
    scrivi(dict(out, tipo="b", s=S_M, eta=ETA_M, e=e))


def campo_grad_a1(eta):
    """### Il campo nella scena di `64bb2328` *(`_u1_secondo.campo_gradiente`)* ### **coi pesi di `A1`** *(`s_rif = s0`)*."""
    c0, cs = U2.campo_gradiente(U2.LG2, U2.S0, eta, "F1", 1.0, "noncompatto")
    return CampoA1(c0.ii, c0.jj, c0.lati, 1.0, "noncompatto", c0.s_a, U2.S0), cs


def lungo_a1(eta, bl0, c0v):
    L1, L2 = U2.LG2
    c, cs = campo_grad_a1(eta)
    U2.prepara(c, bl0, (2 * np.pi * U2.N1_LUNGO / L1, 0.0), U2.W2, (L1 / 4.0, 0.0), "F1")
    pos, uu, ss = (L1 / 4.0, 0.0), [], []
    for t in range(U2.T_LUNGO + 1):
        if t:
            U.tick_campo(c)
        pos, w = U2.baricentro(c, pos)
        uu.append(pos[0] * math.sqrt(3.0) / 2.0)
        ss.append(float(np.sum(w * cs) / np.sum(w)))
    uu, ss = np.array(uu), np.array(ss)
    F = U2.FIN
    v = (uu[2 * F:] - uu[:-2 * F]) / (2 * F)
    sm = ss[F:-F]
    rr = v / (sm ** 2 / U2.S0)
    out = {"v_su_cs2": float(rr.mean()), "variazione": float((rr.max() - rr.min()) / rr.mean())}
    if eta > 0:
        p = np.polyfit(np.log(sm), np.log(v), 1)
        out["pendenza_lnv_lncs"] = float(p[0])
        out["gamma_shapiro"] = float(p[0] - 1.0)
        tp = float(np.sum(np.diff(uu) / (c0v * (0.5 * (ss[1:] + ss[:-1])) ** 2 / U2.S0)))
        out["T_rapporto"] = tp / U2.T_LUNGO
    return out


def fascio_a1(W, bl0, cp):
    """### Il fascio di `_u1_terzo.fascio_esteso` con `A1`: ### **l'accelerazione di Ehrenfest `-v dv/du` con `v = cs^2/cs_rif`** *(la luce di Einstein)* ### **e il fattore d'angolo.**"""
    import _triangoli_bassa_energia as BE
    L1, L2 = U2.LG2
    c, cs = campo_grad_a1(U2.ETA)
    spettro = U2.prepara(c, bl0, (2 * np.pi * U2.N_FASCIO[0] / L1, 2 * np.pi * U2.N_FASCIO[1] / L2), W, (L1 / 4.0, 0.0), "F1")
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
    acc = -(cs ** 2 / U2.S0) * (2.0 * cs * dsdu / U2.S0)
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
    vE, uE = 0.0, [uu[0]]
    for t in range(1, len(tt)):
        vE += 0.5 * (aE[t - 1] + aE[t])
        uE.append(uE[-1] + vE)
    aEf = 2.0 * float(np.polyfit(tt, np.array(uE), 2)[0])
    Lu = L1 * math.sqrt(3.0) / 2.0
    k1 = 2 * np.pi * U2.ETA / Lu
    kg = 2 * np.pi / Lu
    sg = np.array(sg)
    kappa = a / (cp * U2.S0) ** 2
    return {"W": W, "a": a, "kappa": kappa, "kappa_su_R1": kappa / k1, "kappa_su_R2": kappa / (2 * k1), "a_su_aE_cos2": a / (aEf * cos2), "cos2": cos2, "X": float(np.mean(kg * kg * sg * sg)),
            "sigma0": float(sg[0]), "sigma_fine": float(sg[-1])}


def parte_c():
    print("### (c) LA LUCE IN UN GRADIENTE CON A1 (la scena di 64bb2328: %dx%d, s0 %.2f, eta %.2f, cs_rif = s0; il campo F1 con Erone)" % (U2.LG2 + (U2.S0, U2.ETA)))
    bl0 = U.blocchi_campo(U2.S0)[0]
    ctrl = lungo_a1(0.0, bl0, None)
    lu = lungo_a1(U2.ETA, bl0, ctrl["v_su_cs2"])
    print("  il pacchetto lungo: v/(cs^2/cs_rif) %.5f variazione %.2e | d ln v/d ln cs %.4f: gamma (Shapiro) %.4f | il tempo d'arrivo previsto/vero %.5f | il controllo eta 0: %.5f"
          % (lu["v_su_cs2"], lu["variazione"], lu["pendenza_lnv_lncs"], lu["gamma_shapiro"], lu["T_rapporto"], ctrl["v_su_cs2"]))
    cp = U2.c_lungo_a2(bl0, U2.N_FASCIO, U2.LG2, U2.S0)
    fa = []
    for W in W_SCAN:
        f = fascio_a1(W, bl0, cp)
        fa.append(f)
        print("  il fascio W %4.1f: kappa/R1 %.4f kappa/R2 %.4f | a/(a_E <cos^2>) %.4f | X %.4f | sigma %.1f -> %.1f" % (W, f["kappa_su_R1"], f["kappa_su_R2"], f["a_su_aE_cos2"], f["X"], f["sigma0"], f["sigma_fine"]))
        sys.stdout.flush()
    X = np.array([f["X"] for f in fa])
    Y = np.array([f["kappa_su_R2"] for f in fa])
    p1 = np.polyfit(X, Y, 1)
    gamma_def = 2.0 * p1[-1] - 1.0
    print("  l'estrapolazione a X -> 0: kappa/R2 %.4f (grado 1): gamma (deflessione) = 2 kappa/R2 - 1 = %.4f" % (p1[-1], gamma_def))
    scrivi({"tipo": "c", "lungo": lu, "controllo": ctrl, "fasci": fa, "estrapolazione": [float(x) for x in p1], "gamma_deflessione": gamma_def, "gamma_shapiro": lu["gamma_shapiro"]})
    esito("PUO' FALLIRE (c): gamma (dalla deflessione estrapolata) entro %g da 1" % TOLL_GAMMA, abs(gamma_def - 1.0) <= TOLL_GAMMA, "gamma %.4f (Shapiro %.4f)" % (gamma_def, lu["gamma_shapiro"]), deve=False)
    peg = max(abs(f["kappa_su_R1"] - 1.0) for f in fa)
    esito("DEVE FALLIRE (c), PER LA CHIAVE GIUSTA: la deflessione entro %g da R1 (la chiave: kappa/R1 > 1.5 a ogni W)" % TOLL_R1,
          peg > TOLL_R1 and all(f["kappa_su_R1"] > 1.5 for f in fa), " ".join("%.3f" % f["kappa_su_R1"] for f in fa))
    return gamma_def, lu


def caduta(s0, eps, con_a1):
    """### Le corse di `_triangoli_fattore.parte_B` *(toro `A`, il pacchetto di banda, il baricentro lineare, `Lx 96`)*: ### **il differenziale per ramo, `eta 1e-3` e `1e-2`**, ### **con `A1` (`s_rif = s0`) o senza.**"""
    import _triangoli_forza as TF
    bande = TF.coppia_K(eps, s0)
    bl = TF.blocchi(eps, s0)
    Lx = LX_F
    n = Lx * TF.LY
    m1 = (np.arange(n) // TF.LY).astype(float)
    m2 = (np.arange(n) % TF.LY).astype(float)
    qs = TF.q_della_striscia(Lx)
    out = []
    for q_, b in enumerate(bande):
        Tm = max(Lx // 4, int(math.ceil(TF.PERIODI * 2.0 * np.pi / b["delta_min"])))
        cel = TF.pacchetto_banda("A", Lx, Lx / 4.0, Lx / 16.0, b["Q"], TF.spazi_banda(bl, b["Q"], "A", qs), m1, m2)
        if con_a1:
            with a1(s0):
                rs = {eta: TF.corsa_con("A", Lx, eps, s0, eta, cel, "simm", Tm, 0, True)[0] for eta in ETA_F}
        else:
            rs = {eta: TF.corsa_con("A", Lx, eps, s0, eta, cel, "simm", Tm, 0, True)[0] for eta in ETA_F}
        for eta in (1e-3, 1e-2):
            out.append({"banda": q_, "eta": eta, "tick": Tm, "dif": 0.5 * (rs[eta]["a"] - rs[-eta]["a"]), "a0": rs[0.0]["a"]})
    return out


def parte_d():
    print("### (d), (f) LA CADUTA DI UNA PARTICELLA LENTA (le corse di %s, Lx %d): il differenziale con A1 contro quello di oggi alla stessa scena" % (RIF_FATTORE, LX_F))
    righe = []
    for s0 in S0_F:
        t0 = time.time()
        a = caduta(s0, 0.0, True)
        o = caduta(s0, 0.0, False)
        for x, y in zip(a, o):
            r = {"s0": s0, "eps": 0.0, "banda": x["banda"], "eta": x["eta"], "dif_a1": x["dif"], "dif_oggi": y["dif"], "rapporto": x["dif"] / y["dif"], "tick": x["tick"]}
            righe.append(r)
            scrivi(dict(r, tipo="caduta"))
            print("  s0 %.2f banda %d eta %g (%d tick): dif A1 %+.5e oggi %+.5e: A1/oggi %.5f" % (s0, r["banda"], r["eta"], r["tick"], r["dif_a1"], r["dif_oggi"], r["rapporto"]))
        print("    (%.0fs)" % (time.time() - t0))
        sys.stdout.flush()
    a = caduta(S0_EPS, 0.5, True)
    o = caduta(S0_EPS, 0.5, False)
    for x, y in zip(a, o):
        r = {"s0": S0_EPS, "eps": 0.5, "banda": x["banda"], "eta": x["eta"], "dif_a1": x["dif"], "dif_oggi": y["dif"], "rapporto": x["dif"] / y["dif"], "tick": x["tick"]}
        righe.append(r)
        scrivi(dict(r, tipo="caduta"))
        print("  eps 0.5 s0 %.2f banda %d eta %g: dif A1 %+.5e oggi %+.5e: A1/oggi %.5f" % (S0_EPS, r["banda"], r["eta"], r["dif_a1"], r["dif_oggi"], r["rapporto"]))
    rap = [r["rapporto"] for r in righe if r["eps"] == 0.0]
    esito("PUO' FALLIRE (d): la caduta lenta con A1 invariata entro %g (eps 0, ogni s0, ramo, eta)" % TOLL_CADUTA, all(abs(x - 1) <= TOLL_CADUTA for x in rap),
          "A1/oggi da %.4f a %.4f" % (min(rap), max(rap)), deve=False)
    sel = [r for r in righe if r["s0"] == S0_EPS and r["eta"] == 1e-2]
    d0 = {(r["eps"], r["banda"]): r["dif_a1"] for r in sel}
    b01 = abs(d0[(0.0, 1)] / d0[(0.0, 0)] - 1)
    e05 = max(abs(d0[(0.5, q)] / d0[(0.0, q)] - 1) for q in (0, 1))
    esito("PUO' FALLIRE (f): l'universalita' con A1 a s0 %.2f: i due rami entro %g, eps 0.5 contro eps 0 entro %g" % (S0_EPS, TOLL_CADUTA, TOLL_CADUTA), b01 <= TOLL_CADUTA and e05 <= TOLL_CADUTA,
          "rami %.2e, eps %.2e" % (b01, e05), deve=False)
    return righe


def parte_e(tab0):
    print("### (e) IL RAPPORTO DELLE DUE c NEL GRADIENTE di (c): dal generatore al r locale (l'approssimazione localmente uniforme, dichiarata)")
    rr = np.array([t["r"] for t in tab0])
    rp = np.array([t["rapporto"][0] for t in tab0])
    rmin, rmax = 1.0 - U2.ETA, 1.0 + U2.ETA
    vals = {str(r): float(np.interp(r, rr, rp)) for r in (rmin, 1.0, rmax)}
    print("  r da %.2f a %.2f lungo il gradiente: pi x(r)/r %s (pi/4 = %.6f)" % (rmin, rmax, " ".join("r %s: %.6f" % (k, v) for k, v in vals.items()), np.pi / 4))
    scrivi({"tipo": "e", "rapporti": vals})


def testata(nome):
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 120)
    print("IL PROTOTIPO DELLA CURVATURA DELLO SPAZIO SUI TRIANGOLI, IN MEMORIA (la strada A1) -- %s" % nome)
    print("=" * 120)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_curvatura_prototipo.py", "csv/_u1_terzo.py", "csv/_u1_secondo.py", "csv/_u1_prototipo.py", "csv/_triangoli.py",
                                     "csv/_triangoli_bassa_energia.py", "csv/_triangoli_forza.py", "csv/_triangoli_fattore.py", "csv/_zero_simmetrico.py", "csv/_universalita_massa.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  le scelte di prova di Luca (2026-10-25 16:26): A1; cs_rif il vuoto imperturbato (il fondo della scena); Erone; i versori fissi; lo zero simmetrico")
    print("  la configurazione: R_LISTA %s R_SPETTRI %s S_SPETTRI %g PASSI_R %d K_FINE %g NK %d H_R %g; TOLL_X1 %g TOLL_XR %g TOLL_SPETTRI %g TOLL_B %g TOLL_BIT %g TOLL_REL %g"
          % (R_LISTA, R_SPETTRI, S_SPETTRI, PASSI_R, K_FINE, NK, H_R, TOLL_X1, TOLL_XR, TOLL_SPETTRI, TOLL_B, TOLL_BIT, TOLL_REL))
    print("    R_CHIAVE %.2f N_A %d N_G %d N_REV %d N_EN %d L_M %d S_M %.2f ETA_M %.2f E_M %.4f W_SCAN %s TOLL_GAMMA %g TOLL_R1 %g S0_F %s S0_EPS %.2f LX_F %d ETA_F %s TOLL_CADUTA %g; la scena di (c) LG2 %s S0 %.2f ETA %.2f"
          % (R_CHIAVE, N_A, N_G, N_REV, N_EN, L_M, S_M, ETA_M, E_M, W_SCAN, TOLL_GAMMA, TOLL_R1, S0_F, S0_EPS, LX_F, ETA_F, TOLL_CADUTA, U2.LG2, U2.S0, U2.ETA))
    print("-" * 120)
    sys.stdout.flush()
    io.open(JSONL[0], "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA, "parte": nome})


def main(argv):
    assert len(argv) == 1 and argv[0] in ("parte0", "parte1"), "uso: python csv/_curvatura_prototipo.py parte0|parte1"
    if argv[0] == "parte0":
        JSONL[0] = J0
        testata("PARTE 0: la prova dell'obiezione di Luca dagli spettri")
        parte_0()
    else:
        JSONL[0] = J1
        testata("PARTE 1: le misure del prototipo")
        for s in (S_M,):
            U.u_K(s)
        parte_a()
        print("-" * 120)
        parte_b()
        print("-" * 120)
        g, _ = parte_c()
        print("-" * 120)
        parte_d()
        print("-" * 120)
        JSONL_0 = JSONL[0]
        JSONL[0] = J0
        tab0 = [json.loads(l) for l in io.open(J0, encoding="utf-8") if '"x_r"' in l][0]["tabella"]
        JSONL[0] = JSONL_0
        parte_e(tab0)
    print("-" * 120)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
