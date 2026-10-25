# -*- coding: utf-8 -*-
r"""**LA MATERIA LEGGERA, SULLA CARTA** *([[MATERIA-LEGGERA]], [[LORENTZ-MATERIA-INTERFERENZA]], [[V-MAX-DIREZIONI]])*: ### **il limite `v_max/c` dipende dalla massa della coppia rispetto alla
larghezza della sua banda?** ### **`L1` la scomposizione, `L2` le manopole, `L3` il riferimento a nido d'ape con la massa di Semenoff.**

> ### ⛔ **Il task history e' `2026-10-25_materia_leggera.md`.** ### **Sulla carta: il generatore e gli spettri, nessuna dinamica, nessun file del nucleo.**
> ### **Importati, non copiati:** `_curvatura_parte2` *(`H_ab`, `H_moneta`)*, `_u1_terzo.H_gen`, `_triangoli_forza` *(`blocchi`, `A_di`)*, `_triangoli_bassa_energia.J`.

Gira con:  python csv/_materia_leggera.py > doc/referti_l2/materia_leggera.txt
"""
import io
import json
import math
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

BETA_SU_ALPHA = (0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0)
EPSS = (0.0, 0.1, 0.25, 0.5, 1.0, 1.5)
SS = (0.01, 0.05, 0.3, 0.5, 0.7, 0.9, 0.99)
DELTE = (-0.4, -0.2, 0.0, 0.2, 0.4)
DD = (1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005)
N_GRIGLIA = 48
N_CONV = 96
N_PARTENZE = 5
H_CURV = 1e-3
H_GRAD = 1e-6
TOLL_PIATTA = 1e-9
TOLL_L1 = 1e-5
TOLL_UNO = 1e-2
MW_PICCOLO = 0.01
MW_SOGLIA = 0.1
TOLL_CTRL = 1e-4
TOLL_SCALA = 1e-10
TOLL_UNIV = 1e-6
TOLL_ISO = 1e-6
TOLL_CONV = 1e-6
SALTO_MIN = 1e-3
CHIAVE = 0.1
JSONL = os.path.join(RADICE, "doc", "referti_l2", "materia_leggera.jsonl")
RIF_L1 = os.path.join(RADICE, "doc", "referti_l2", "curvatura_0bis_v2.jsonl")
OK = [0, 0]
FALLITE = []
TK = (2 * np.pi / 3, 2 * np.pi / 3)


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def t_di(kx, ky):
    import _triangoli_bassa_energia as BE
    J = BE.J
    return J[0, 0] * kx + J[0, 1] * ky, J[1, 0] * kx + J[1, 1] * ky


def k_di(t1, t2):
    import _triangoli_bassa_energia as BE
    return np.linalg.solve(BE.J, np.array([t1, t2]))


# =====================================================================================
#   LE FAMIGLIE: mu(t) ordinato, dallo zero di ciascuna
# =====================================================================================
def fam_ab(alpha, beta):
    import _curvatura_parte2 as P2
    z = 0.5 * (alpha + beta)
    return lambda t1, t2: np.sort(z - np.linalg.eigvalsh(P2.H_ab(t1, t2, alpha, beta)))


def fam_eps(eps):
    import _curvatura_parte2 as P2
    return lambda t1, t2: np.sort(1.0 - np.linalg.eigvalsh(P2.H_moneta(t1, t2, 1.0, 1.0, 1.0, eps)))


def fam_s(s):
    import _triangoli_forza as TF
    bl = TF.blocchi(0.0, s)

    def f(t1, t2):
        A = TF.A_di(bl, t1, t2)[0::2, 0::2]
        return np.sort(-np.angle(np.linalg.eigvals(A)) / (np.pi * s))
    return f


def fam_zero(delta):
    import _u1_terzo as U3
    return lambda t1, t2: np.sort(1.0 - delta - np.linalg.eigvalsh(U3.H_gen(t1, t2)))


def fam_semenoff(D):
    def f(t1, t2):
        # ### i tre vicini `0`, `a1`, `-a2` (a `60` gradi fra loro): il punto di Dirac cade in `K = (2pi/3, 2pi/3)`
        ff = 1.0 + np.exp(1j * t1) + np.exp(-1j * t2)
        e = math.sqrt(D * D + abs(ff) ** 2)
        return np.array([-e, e])
    return f


# =====================================================================================
#   LA BANDA DELLA COPPIA E LE SUE GRANDEZZE
# =====================================================================================
def griglia(f, n):
    out = np.array([[f(2 * np.pi * a / n, 2 * np.pi * b / n) for b in range(n)] for a in range(n)])
    return out


def bande_coppia(f, G):
    """### Le bande NON piatte; quella col `mu` positivo piu' piccolo a `K` (la ALTA) e quella col negativo piu' vicino a zero (la BASSA)."""
    nb = G.shape[-1]
    piatte = [b for b in range(nb) if np.ptp(G[..., b]) < TOLL_PIATTA]
    mk = f(*TK)
    su = [b for b in range(nb) if b not in piatte and mk[b] > 0]
    giu = [b for b in range(nb) if b not in piatte and mk[b] < 0]
    bu = min(su, key=lambda b: (mk[b], b))
    bd = max(giu, key=lambda b: (mk[b], -b))
    return bu, bd, piatte, mk


def curvatura(f, b, direzione):
    h = H_CURV
    kK = k_di(*TK)
    u = np.array(direzione, dtype=float)

    def m(x):
        k = kK + x * u
        return f(*t_di(k[0], k[1]))[b]
    return (-m(2 * h) + 16 * m(h) - 30 * m(0) + 16 * m(-h) - m(-2 * h)) / (12 * h * h)


def grad(f, b, k):
    h = H_GRAD
    gx = (f(*t_di(k[0] + h, k[1]))[b] - f(*t_di(k[0] - h, k[1]))[b]) / (2 * h)
    gy = (f(*t_di(k[0], k[1] + h))[b] - f(*t_di(k[0], k[1] - h))[b]) / (2 * h)
    return math.hypot(gx, gy)


def v_max(f, b, n):
    from scipy.optimize import minimize
    cand = []
    for a in range(n):
        for c in range(n):
            k = k_di(2 * np.pi * a / n, 2 * np.pi * c / n)
            cand.append((grad(f, b, k), k))
    cand.sort(key=lambda z: -z[0])
    best, dove = cand[0][0], cand[0][1]
    for g0, k0 in cand[:N_PARTENZE]:
        res = minimize(lambda x: -grad(f, b, x), k0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 4000})
        if -res.fun > best:
            best, dove = float(-res.fun), res.x
    return best, cand[0][0], [float(x) for x in dove]


def misura(nome, par, f):
    t0 = time.time()
    G = griglia(f, N_GRIGLIA)
    bu, bd, piatte, mk = bande_coppia(f, G)
    m_su, m_giu = float(mk[bu]), float(-mk[bd])
    W = float(np.ptp(G[..., bu]))
    nb = G.shape[-1]
    vicine = [x for x in (bu - 1, bu + 1) if 0 <= x < nb and x != bu and np.ptp(G[..., x]) >= 0]
    salto = min([float(np.min(np.abs(G[..., bu] - G[..., x]))) for x in vicine if not np.allclose(G[..., x], G[..., bu])] or [float("inf")])
    cx, cy = curvatura(f, bu, (1, 0)), curvatura(f, bu, (0, 1))
    vb_x, vb_y = math.sqrt(max(m_su * cx, 0.0)), math.sqrt(max(m_su * cy, 0.0))
    cdx = curvatura(f, bd, (1, 0))
    vb_giu = math.sqrt(max(-mk[bd] * -cdx, 0.0))
    vm, vm_g, dove = v_max(f, bu, N_GRIGLIA)
    vm2, _g2, _d2 = v_max(f, bu, N_CONV)
    vmd, _gd, _dd = v_max(f, bd, N_GRIGLIA)
    r = {"famiglia": nome, "par": par, "banda": bu, "banda_giu": bd, "piatte": piatte, "m": m_su, "m_giu": m_giu, "W": W, "m_su_W": m_su / W, "salto": salto,
         "v_b": vb_x, "v_b_y": vb_y, "v_b_giu": vb_giu, "isotropia": abs(vb_x - vb_y), "v_max": vm, "v_max_griglia": vm_g, "v_max_96": vm2, "v_max_giu": vmd,
         "dove": dove, "v_max_su_v_b": vm / vb_x if vb_x > 0 else None, "conv": abs(vm2 - vm), "univ_m": abs(m_su - m_giu), "univ_v": abs(vb_x - vb_giu), "secondi": time.time() - t0}
    scrivi(dict(r, tipo="misura"))
    print("  %-8s %-8s banda %2d: m %.6f (giu' %.6f) W %.6f m/W %.5f | v_b %.6f (y %.6f, giu' %.6f) v_max %.6f (griglia %.6f, 96 %.6f) v_max/v_b %.6f | salto %.2e | %.0f s"
          % (nome, par, bu, m_su, m_giu, W, m_su / W, vb_x, vb_y, vb_giu, vm, vm_g, vm2, r["v_max_su_v_b"] or float("nan"), salto, r["secondi"]))
    sys.stdout.flush()
    return r


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA MATERIA LEGGERA, SULLA CARTA: v_max/v_b contro m/W per le manopole del modello e per un Dirac a nido d'ape con la massa di Semenoff")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_materia_leggera.py", "csv/_curvatura_parte2.py", "csv/_u1_terzo.py", "csv/_triangoli_forza.py", "doc/referti_l2/curvatura_0bis_v2.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: BETA_SU_ALPHA %s EPSS %s SS %s DELTE %s DD %s N_GRIGLIA %d N_CONV %d N_PARTENZE %d H_CURV %g H_GRAD %g TOLL_PIATTA %g"
          % (BETA_SU_ALPHA, EPSS, SS, DELTE, DD, N_GRIGLIA, N_CONV, N_PARTENZE, H_CURV, H_GRAD, TOLL_PIATTA))
    print("  le soglie: TOLL_L1 %g TOLL_UNO %g MW_PICCOLO %g MW_SOGLIA %g TOLL_CTRL %g TOLL_SCALA %g TOLL_UNIV %g TOLL_ISO %g TOLL_CONV %g SALTO_MIN %g CHIAVE %g"
          % (TOLL_L1, TOLL_UNO, MW_PICCOLO, MW_SOGLIA, TOLL_CTRL, TOLL_SCALA, TOLL_UNIV, TOLL_ISO, TOLL_CONV, SALTO_MIN, CHIAVE))
    print("  le unita': quelle del generatore (v/s = pi v; c = 1/pi a r 1)")
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    # ### L1
    rap = None
    for l in io.open(RIF_L1, encoding="utf-8"):
        d = json.loads(l)
        if d.get("tipo") == "rapporto":
            rap = d["rapporti"]["1.0"]
    vbc, vmc = rap["v_b_su_c"], rap["v_max_su_c"]
    q = vmc / vbc
    print("### L1 -- LA SCOMPOSIZIONE a r 1 (dal jsonl di afba052b): v_b/c %.7f, v_max/c %.7f, v_max/v_b %.7f; il prodotto %.7f" % (vbc, vmc, q, vbc * q))
    scrivi({"tipo": "L1", "v_b_su_c": vbc, "v_max_su_c": vmc, "v_max_su_v_b": q})
    esito("DEVE PASSARE (1): (v_b/c)(v_max/v_b) = v_max/c entro %g, v_b/c = 0.785398 e v_max/v_b = 0.76304 entro %g" % (TOLL_L1, TOLL_L1),
          abs(vbc * q - vmc) <= TOLL_L1 and abs(vbc - 0.785398) <= TOLL_L1 and abs(q - 0.76304) <= TOLL_L1, "%.7f %.7f" % (vbc, q))
    ris = {}
    print("### L2 (a) -- alpha/beta (alpha 1)")
    for r_ in BETA_SU_ALPHA:
        ris[("ab", r_)] = misura("ab", r_, fam_ab(1.0, r_))
    ris[("ab", "2,2")] = misura("ab", "2,2", fam_ab(2.0, 2.0))
    print("### L2 (b) -- eps della moneta")
    for e in EPSS:
        ris[("eps", e)] = misura("eps", e, fam_eps(e))
    print("### L2 (c) -- s del tick (eps 0)")
    for s in SS:
        ris[("s", s)] = misura("s", s, fam_s(s))
    print("### L2 (d) -- lo zero spostato di delta")
    for dl in DELTE:
        ris[("zero", dl)] = misura("zero", dl, fam_zero(dl))
    print("### L2 (e) -- i termini S: su un vuoto uniforme una fase uniforme per nodo, cioe' uno spostamento dello zero: e' la (d) (non misurato a parte)")
    print("### L3 -- il riferimento: il Dirac a nido d'ape con la massa di Semenoff D")
    for D in DD:
        ris[("semenoff", D)] = misura("semenoff", D, fam_semenoff(D))
    print("-" * 130)
    print("### I CRITERI")
    pic = [ris[("semenoff", D)] for D in DD if ris[("semenoff", D)]["m_su_W"] <= MW_PICCOLO]
    esito("DEVE PASSARE (2): il riferimento a m/W <= %g ha v_max/v_b entro %g da 1" % (MW_PICCOLO, TOLL_UNO), bool(pic) and all(abs(r["v_max_su_v_b"] - 1) <= TOLL_UNO for r in pic),
          " ".join("m/W %.4f: %.5f" % (r["m_su_W"], r["v_max_su_v_b"]) for r in pic))
    base = [ris[("ab", 1.0)], ris[("eps", 0.0)], ris[("s", 0.01)]]
    ok3 = all(abs(r["m"] - 0.5) <= TOLL_CTRL and abs(r["W"] - 0.5) <= TOLL_CTRL and abs(r["v_max_su_v_b"] - 0.76304) <= TOLL_CTRL for r in base)
    ok3 &= abs(ris[("ab", "2,2")]["m_su_W"] - ris[("ab", 1.0)]["m_su_W"]) <= TOLL_SCALA and abs(ris[("ab", "2,2")]["v_max_su_v_b"] - ris[("ab", 1.0)]["v_max_su_v_b"]) <= TOLL_SCALA
    esito("DEVE PASSARE (3): (a) a alpha = beta = 1, (b) a eps 0, (c) a s 0.01: m = W = 1/2 e v_max/v_b = 0.76304 entro %g; alpha = beta = 2 lo stesso entro %g" % (TOLL_CTRL, TOLL_SCALA), ok3,
          " | ".join("m %.6f W %.6f q %.6f" % (r["m"], r["W"], r["v_max_su_v_b"]) for r in base))
    modello = [r for (fa, _p), r in ris.items() if fa in ("ab", "eps", "s", "zero")]
    piccoli = [r for r in modello if r["m_su_W"] <= MW_PICCOLO]
    esito("PUO' FALLIRE (4): ogni manopola che rende m/W <= %g da' v_max/v_b entro %g da 1" % (MW_PICCOLO, TOLL_UNO), bool(piccoli) and all(abs(r["v_max_su_v_b"] - 1) <= TOLL_UNO for r in piccoli),
          ("nessuna manopola arriva a m/W <= %g; il minimo %.4f (%s %s)" % (MW_PICCOLO, min(r["m_su_W"] for r in modello), min(modello, key=lambda r: r["m_su_W"])["famiglia"], min(modello, key=lambda r: r["m_su_W"])["par"]))
          if not piccoli else " ".join("%s %s: %.4f" % (r["famiglia"], r["par"], r["v_max_su_v_b"]) for r in piccoli), deve=False)
    buoni = [r for r in modello if r["m_su_W"] < MW_SOGLIA and r["univ_m"] <= TOLL_UNIV and r["univ_v"] <= TOLL_UNIV and r["isotropia"] <= TOLL_ISO]
    esito("PUO' FALLIRE (5): una manopola rende m/W < %g senza rompere l'universalita' fra le bande o l'isotropia" % MW_SOGLIA, bool(buoni),
          " ".join("%s %s m/W %.4f" % (r["famiglia"], r["par"], r["m_su_W"]) for r in buoni) or "nessuna", deve=False)
    q1, q2 = ris[("semenoff", DD[0])]["v_max_su_v_b"], ris[("semenoff", DD[-1])]["v_max_su_v_b"]
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA (6): v_max/v_b non dipende da m/W sul riferimento; la chiave: fra D %g e D %g cambia di piu' di %g" % (DD[0], DD[-1], CHIAVE), abs(q1 - q2) > CHIAVE, "%.5f %.5f" % (q1, q2))
    print("### LA CONVERGENZA DI v_max (griglia %d contro %d, dopo l'ottimizzatore): il massimo scarto %.2e" % (N_GRIGLIA, N_CONV, max(r["conv"] for r in ris.values())))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
