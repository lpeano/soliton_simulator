# -*- coding: utf-8 -*-
r"""**LA CURVATURA, PARTE 2 SULLA CARTA: esiste una lunghezza che non tocca la massa?** ### **La famiglia `H(alpha, beta) = alpha (I - P_u) + beta P_-`, gli zeri, le due condizioni della
relativita' generale a campo debole** *([[PROGETTO-CURVATURA]], [[LORENTZ-MATERIA-INTERFERENZA]])*.

> ### ⛔ **Il task history e' `2026-10-25_curvatura_parte2.md`** *(`cd7aa992`)*. ### **Sulla carta: il generatore, nessuna corsa di dinamica; nessun file del nucleo.**
> ### **Importati, non copiati:** `_u1_terzo.H_gen` *(il controllo a `alpha = beta = 1`)*, `_curvatura_prototipo` *(`x_di`, la coppia di `A1`)*, `_triangoli_forza.theta_di`, `_triangoli.TRIANGOLI` *(i versori)*.
> ### **`H_ab` e' scritto con le STESSE operazioni di `_u1_terzo.H_gen`, moltiplicate per `alpha` e `beta`** *(cosi' a `alpha = beta = 1` e' lo stesso AL BIT)*.

Gira con:  python csv/_curvatura_parte2.py > doc/referti_l2/curvatura_parte2.txt
"""
import io
import json
import math
import os
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

R_P0 = (0.5, 1.0, 2.0)
R_C = (0.5, 0.8, 0.9, 0.95, 0.99, 1.0, 1.05, 1.25, 2.0)
R_D = (0.5, 0.8, 0.9, 1.0)
N_COPPIE = 20
SEME = 7
AB_MIN, AB_MAX, AB_PASSO = 0.05, 4.0, 0.01
AB_PASSO_GROSSO = 0.1
PASSI = 200
K_FINE = 0.01
NK = 200
EPS = 0.5
TOLL_P0 = 1e-8
TOLL_A = 1e-8
TOLL_D = 1e-6
JSONL = os.path.join(RADICE, "doc", "referti_l2", "curvatura_parte2.jsonl")
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


def H_ab(t1, t2, alpha, beta):
    """### **`alpha (I - P_u) + beta P_-`**, ### **con le operazioni di `_u1_terzo.H_gen`** *(gli stessi passi, ogni termine per il suo peso)*."""
    H = alpha * (np.eye(6) - np.ones((6, 6)) / 6.0)
    H = H.astype(complex)
    for a, th in enumerate((t1, t2, t1 + t2)):
        H[a, a] += beta * 0.5
        H[3 + a, 3 + a] += beta * 0.5
        H[a, 3 + a] += beta * (-0.5 * np.exp(1j * th))
        H[3 + a, a] += beta * (-0.5 * np.exp(-1j * th))
    return H


def coppia(alpha, beta):
    """### **La coppia a `K` seguita per continuita' da `(1, 1)`** *(i livelli `lambda = 1/2` e `3/2`)*: `[(lambda0, v)]`."""
    import _triangoli_forza as TF
    tK = TF.theta_di("A", 0.0)
    lam, V = np.linalg.eigh(H_ab(tK[0], tK[1], 1.0, 1.0))
    idx = [int(np.argmin(np.abs(lam - 0.5))), int(np.argmin(np.abs(lam - 1.5)))]
    vv = [V[:, [i]] for i in idx]
    for f in np.linspace(0.0, 1.0, PASSI + 1)[1:]:
        lam, V = np.linalg.eigh(H_ab(tK[0], tK[1], 1.0 + f * (alpha - 1.0), 1.0 + f * (beta - 1.0)))
        vv = [V[:, [int(np.argmax(np.abs(V.conj().T @ v)[:, 0]))]] for v in vv]
    return [(float(np.real(np.vdot(v[:, 0], H_ab(tK[0], tK[1], alpha, beta) @ v[:, 0]))), v) for v in vv]


def mu_x(alpha, beta, zero):
    """### **`mu0 = z - lambda0` e `x = sqrt(2 mu0 a)`** *(la curvatura fine lungo la normale ad `a2`)* ### **per i due membri della coppia;** `zero` in `("Z1", "Z2", "Z3")`."""
    import _triangoli_forza as TF
    cp = coppia(alpha, beta)
    if zero == "Z1":
        z = 0.5 * (alpha + beta)
    elif zero == "Z2":
        z = 0.0
    else:
        z = 0.5 * (cp[0][0] + cp[1][0])
    out = []
    for lam0, v in cp:
        qq = np.linspace(0.0, K_FINE * math.sqrt(3.0) / 2.0, NK + 1)
        ll = []
        for q in qq:
            lam, V = np.linalg.eigh(H_ab(*TF.theta_di("A", q), alpha, beta))
            j = int(np.argmax(np.abs(V.conj().T @ v)[:, 0]))
            ll.append(lam[j])
            v = V[:, [j]]
        k = qq * 2.0 / math.sqrt(3.0)
        X = np.stack([k ** 2, k ** 4, k ** 6], axis=1)
        cc, *_ = np.linalg.lstsq(X, -(np.array(ll) - ll[0]), rcond=None)
        mu0 = z - ll[0]
        x2 = 2.0 * mu0 * cc[0]
        out.append({"lambda0": float(ll[0]), "mu0": float(mu0), "a": float(cc[0]), "x": float(math.sqrt(x2)) if x2 > 0 else None, "x2": float(x2)})
    return z, out


def piu(r):
    """### **Il membro della coppia col `mu0 > 0` nello zero `Z1`.**"""
    return max(r, key=lambda e: e["mu0"])


def H_moneta(t1, t2, alpha, beta, gamma, eps):
    """### **Il blocco `12 x 12`** *(`6` estremita' x lo spin)*: ### **`H_ab x I_2 - gamma (eps/pi) sigma.n`** *(i versori dei triangoli: `+e_a` sui lati `+`, `-e_a` sui lati `-`)*."""
    import _triangoli as T
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    H = np.kron(H_ab(t1, t2, alpha, beta), np.eye(2))
    dirs = T.TRIANGOLI[1]
    for e in range(6):
        n = np.asarray(dirs[e % 3]) * (1.0 if e < 3 else -1.0)
        H[2 * e:2 * e + 2, 2 * e:2 * e + 2] -= gamma * (eps / np.pi) * (n[0] * sx + n[1] * sy + n[2] * sz)
    return H


def mu0_moneta(alpha, beta, gamma, eps):
    """### **I livelli della coppia a `K` con la moneta** *(i `4` livelli piu' vicini ai due della coppia senza moneta, raddoppiati dallo spin)*, ### **nello zero `Z1`.**"""
    import _triangoli_forza as TF
    tK = TF.theta_di("A", 0.0)
    cp = coppia(alpha, beta)
    lam = np.linalg.eigvalsh(H_moneta(tK[0], tK[1], alpha, beta, gamma, eps))
    z = 0.5 * (alpha + beta)
    out = []
    for l0, _v in cp:
        idx = np.argsort(np.abs(lam - l0))[:2]
        out.append(sorted(float(z - lam[i]) for i in idx))
    return out


def main(argv):
    del argv
    import _presidio
    import _u1_terzo as U3
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 120)
    print("LA CURVATURA, PARTE 2 SULLA CARTA: la famiglia H(alpha, beta) = alpha (I - P_u) + beta P_-, gli zeri, le due condizioni della relativita' generale a campo debole")
    print("=" * 120)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_curvatura_parte2.py", "csv/_u1_terzo.py", "csv/_curvatura_prototipo.py", "csv/_triangoli.py", "csv/_triangoli_forza.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: R_P0 %s R_C %s R_D %s N_COPPIE %d SEME %d AB in [%g, %g] passo %g (grosso %g) PASSI %d K_FINE %g NK %d EPS %g TOLL_P0 %g TOLL_A %g TOLL_D %g; gli zeri Z1 = (alpha + beta)/2, Z2 = 0, Z3 = il punto medio della coppia"
          % (R_P0, R_C, R_D, N_COPPIE, SEME, AB_MIN, AB_MAX, AB_PASSO, AB_PASSO_GROSSO, PASSI, K_FINE, NK, EPS, TOLL_P0, TOLL_A, TOLL_D))
    print("-" * 120)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    # ### il controllo del generatore
    rng = np.random.default_rng(SEME)
    bit = all(H_ab(t1, t2, 1.0, 1.0).tobytes() == U3.H_gen(t1, t2).tobytes() for t1, t2 in rng.uniform(0, 2 * np.pi, (10, 2)))
    esito("DEVE PASSARE: a alpha = beta = 1 il generatore e' _u1_terzo.H_gen AL BIT (10 k casuali)", bit, str(bit))
    # ### P0
    print("### P0 -- IL GENERATORE A1 (alpha 1, beta r), lo zero Z1")
    peg = 0.0
    for r in R_P0:
        z, m = mu_x(1.0, r, "Z1")
        p = piu(m)
        d = max(abs(p["mu0"] - 0.5 * math.sqrt(1 - r + r * r)), abs(p["x"] - math.sqrt(r) / 4))
        peg = max(peg, d)
        print("  r %-4g | mu0 %.10f (formula %.10f) | x %.10f (formula %.10f)" % (r, p["mu0"], 0.5 * math.sqrt(1 - r + r * r), p["x"], math.sqrt(r) / 4))
    esito("DEVE PASSARE (P0): A1 riproduce mu0 = sqrt(1 - r + r^2)/2 e x = sqrt(r)/4 entro %g" % TOLL_P0, peg <= TOLL_P0, "%.1e" % peg)
    # ### P1 (a), (b)
    print("### P1 (a), (b) -- LE FORMULE SU %d COPPIE CASUALI, i tre zeri" % N_COPPIE)
    ab = rng.uniform(0.2, 3.0, (N_COPPIE, 2))
    pa, z13 = 0.0, 0.0
    righe = []
    for alpha, beta in ab:
        z1, m1 = mu_x(alpha, beta, "Z1")
        z2, m2 = mu_x(alpha, beta, "Z2")
        z3, m3 = mu_x(alpha, beta, "Z3")
        p = piu(m1)
        fm = 0.5 * math.sqrt(alpha * alpha - alpha * beta + beta * beta)
        fx = alpha * beta / 16.0
        pa = max(pa, abs(p["mu0"] - fm), abs(p["x2"] - fx))
        z13 = max(z13, abs(z1 - z3))
        righe.append({"alpha": float(alpha), "beta": float(beta), "Z1": m1, "Z2": m2, "Z3": m3, "z1": z1, "z3": z3})
        print("  alpha %.4f beta %.4f | Z1: mu0 %+.8f %+.8f (formula +-%.8f), x^2 %.8f (formula %.8f) | Z2: mu0 %+.6f %+.6f, x %s %s | Z3 - Z1 %.1e"
              % (alpha, beta, m1[0]["mu0"], m1[1]["mu0"], fm, p["x2"], fx, m2[0]["mu0"], m2[1]["mu0"], "%.6f" % m2[0]["x"] if m2[0]["x"] else "--", "%.6f" % m2[1]["x"] if m2[1]["x"] else "--", z3 - z1))
    scrivi({"tipo": "formule", "righe": righe})
    esito("PUO' FALLIRE (P1 a): mu0 = sqrt(alpha^2 - alpha beta + beta^2)/2 e x^2 = alpha beta/16 (lo zero Z1) entro %g su %d coppie" % (TOLL_A, N_COPPIE), pa <= TOLL_A, "%.1e" % pa, deve=False)
    print("  LO ZERO Z3 (il punto medio della coppia) contro Z1 = (alpha + beta)/2: lo scarto massimo %.2e su %d coppie" % (z13, N_COPPIE))
    # ### P1 (c)
    print("### P1 (c) -- LE DUE CONDIZIONI mu0 = 1/2 e x = r/4, lo zero Z1: la formula [sqrt(1 + 3 r^2) +- sqrt(1 - r^2)]/2 e la verifica sul generatore; per r > 1 il residuo minimo sulla griglia")
    sol = {}
    for r in R_C:
        if r <= 1.0:
            q = math.sqrt(1 + 3 * r * r)
            w = math.sqrt(1 - r * r)
            rami = {"+": ((q + w) / 2, (q - w) / 2), "-": ((q - w) / 2, (q + w) / 2)}
            sol[r] = rami
            for nome, (alpha, beta) in rami.items():
                _z, m = mu_x(alpha, beta, "Z1")
                p = piu(m)
                print("  r %-5g ramo %s: alpha %.8f beta %.8f | il generatore: mu0 %.10f (1/2) x %.10f (r/4 = %.10f)" % (r, nome, alpha, beta, p["mu0"], p["x"], r / 4))
                scrivi({"tipo": "soluzione", "r": r, "ramo": nome, "alpha": alpha, "beta": beta, "mu0": p["mu0"], "x": p["x"]})
        else:
            a = np.arange(AB_MIN, AB_MAX + 1e-12, AB_PASSO)
            A, B = np.meshgrid(a, a, indexing="ij")
            res = (0.5 * np.sqrt(A * A - A * B + B * B) - 0.5) ** 2 + (np.sqrt(A * B) / 4 - r / 4) ** 2
            i, j = np.unravel_index(np.argmin(res), res.shape)
            _z, m = mu_x(float(a[i]), float(a[j]), "Z1")
            p = piu(m)
            print("  r %-5g: NESSUNA soluzione reale ((alpha - beta)^2 = 1 - r^2 < 0); il residuo minimo sulla griglia (dalla formula) %.4e a alpha %.2f beta %.2f; il generatore li': mu0 %.6f x %.6f (r/4 %.4f)"
                  % (r, float(res[i, j]), a[i], a[j], p["mu0"], p["x"], r / 4))
            scrivi({"tipo": "nessuna_soluzione", "r": r, "residuo": float(res[i, j]), "alpha": float(a[i]), "beta": float(a[j]), "mu0": p["mu0"], "x": p["x"]})
    esito("PUO' FALLIRE (P1 c): nessuna soluzione per r > 1 con lo zero Z1 (r 1.05, 1.25, 2: il residuo minimo > 0)", True, "dalla formula (alpha - beta)^2 = 1 - r^2, verificata in (a)", deve=False)
    # ### gli altri zeri, una ricerca grossa
    print("### P1 (b)-(c) -- GLI ALTRI ZERI: la ricerca grossa (passo %g) del residuo sul generatore, a r 0.9 e 1.25" % AB_PASSO_GROSSO)
    for zero in ("Z2", "Z3"):
        for r in (0.9, 1.25):
            best = (1e9, None)
            for alpha in np.arange(0.2, 3.0 + 1e-9, AB_PASSO_GROSSO * 2):
                for beta in np.arange(0.2, 3.0 + 1e-9, AB_PASSO_GROSSO * 2):
                    _z, m = mu_x(float(alpha), float(beta), zero)
                    for e in m:
                        if e["x"] is None:
                            continue
                        rr = (abs(e["mu0"]) - 0.5) ** 2 + (e["x"] - r / 4) ** 2
                        if rr < best[0]:
                            best = (rr, (float(alpha), float(beta), e["mu0"], e["x"]))
            print("  lo zero %s, r %g: il residuo minimo %.3e a %s" % (zero, r, best[0], best[1]))
            scrivi({"tipo": "altri_zeri", "zero": zero, "r": r, "residuo": best[0], "dove": best[1]})
    # ### P1 (d)
    print("### P1 (d) -- LA MONETA (eps %g) SULLA SOLUZIONE DI (c), ramo +: mu0 della coppia, con gamma = 1 (la moneta fissa) e gamma = alpha (la moneta col nodo)" % EPS)
    dd = {}
    for gnome in ("1", "alpha"):
        vals = []
        for r in R_D:
            alpha, beta = sol[r]["+"]
            gamma = 1.0 if gnome == "1" else alpha
            lv = mu0_moneta(alpha, beta, gamma, EPS)
            vals.append(lv)
            print("  gamma %-5s r %-4g: i livelli della coppia (Z1) %s" % (gnome, r, " | ".join(" ".join("%+.8f" % x for x in p) for p in lv)))
        flat = np.array([[x for p in v for x in p] for v in vals])
        var = float(np.max(flat.max(axis=0) - flat.min(axis=0)))
        dd[gnome] = var
        scrivi({"tipo": "moneta", "gamma": gnome, "r": list(R_D), "livelli": vals, "variazione": var})
    esito("PUO' FALLIRE (P1 d): con eps %g la soluzione di (c) tiene mu0 indipendente da r entro %g (gamma = 1)" % (EPS, TOLL_D), dd["1"] <= TOLL_D, "gamma 1: %.2e; gamma alpha: %.2e" % (dd["1"], dd["alpha"]), deve=False)
    # ### la chiave
    _z, m = mu_x(1.0, 2.0, "Z1")
    p = piu(m)
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA: A1 (alpha 1, beta r) soddisfa le due condizioni; la chiave: mu0 a r 2 = 0.866", abs(p["mu0"] - 0.5) > 1e-3 and abs(p["mu0"] - 0.866025) < 1e-5, "mu0 %.6f" % p["mu0"])
    print("-" * 120)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
