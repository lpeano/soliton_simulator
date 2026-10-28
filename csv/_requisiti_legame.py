# -*- coding: utf-8 -*-
r"""**I REQUISITI DEL LEGAME, I CONTI SULLA CARTA** *(il mandato di Luca delle `19:18` del `2026-10-28`; [[DECISIONE-LINEARE]], [[PIANO-2D-3D]];
il task history `doc/TASK_HISTORY/2026-10-28_requisiti_legame.md`)*: ### **nessuna corsa del simulatore; nessun file del nucleo.**

### **(b)** `sigma_eff(x) = d ln(alpha - alpha(0)) / d ln x` per `S1` e `S4`, e la `x` del cuore dei solitoni misurati;
### **(c), (d)** l'equazione dell'inviluppo del risolutore in forma ADIMENSIONALE, `lap v + (alpha(v^2) - alpha(0)) v = nu v` in `d = 2, 3`
*(`xi = r/l`, `l = sqrt(|c|/s)`, `v^2 = x`, `nu = mu/s - alpha(0)`, `n = N/(Lambda0 l^d)`)*: ### **`n(nu)` col TIRO** *(shooting)*, ### **e il segno di `dn/dnu`** *(Vakhitov-Kolokolov)*;
### **R6:** `dbeta/dx + x dalpha/dx = 0` *(`alpha` e `beta` da una sola primitiva)*.

    python csv/_requisiti_legame.py --referto > doc/referti_l2/requisiti_legame.txt
"""
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

P4 = 2.0 / math.pi
FORME = ("S1", "S4")
ALPHA0 = {"S1": 0.0, "S4": -math.pi}
DMAX = {"S1": 1.0, "S4": 2.0 * math.pi}       # ### il tetto di alpha - alpha(0)
X_TAB = tuple(10.0 ** k for k in range(-6, 5))
Q_GRIGLIA = (1e-4, 3e-4, 1e-3, 3e-3, 0.01, 0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99)   # ### nu / DMAX
DIMENSIONI = (2, 3)
XI0 = 1e-6
XI_MAX = 1e4
RTOL = 1e-12
BISEZIONI = 200
TOLL_ESATTA = 1e-6            # ### i controlli con la soluzione esatta
TOLL_RISOLUTORE = 1e-3        # ### il tiro contro i punti del risolutore di bcbd1f40
TOLL_ESPONENTE = 0.02         # ### l'esponente delle potenze pure
LAM0_TRI = 6.0
S_3D = 0.3                    # ### la scala fisica del 3D: un PARAMETRO (la curvatura FCC non e' misurata)
DATI = os.path.join(RADICE, "doc", "referti_l2", "solitoni_triangoli.jsonl")
CL_PUNTI = os.path.join(RADICE, "doc", "referti_l2", "congelato_lungo")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def delta_alpha(forma):
    """### **`alpha(x) - alpha(0)`, dal CODICE** *(`_screening_forme_s3._ab`)*, ### **o le forme di controllo.**"""
    import _screening_forme_s3 as SF
    if forma in FORME:
        a0 = ALPHA0[forma]
        return lambda x: SF._ab(forma, np.maximum(x, 1e-300))[0] - a0
    if forma == "LOG":
        return lambda x: np.log(np.maximum(x, 1e-300)) + 1.0
    if forma.startswith("POT"):
        sg = float(forma[3:])
        return lambda x: np.maximum(x, 0.0) ** sg
    raise AssertionError(forma)


def sigma_chiusa(forma, x):
    return 2.0 / (1.0 + x * x) if forma == "S1" else P4 / (1.0 + x ** P4)


def sigma_codice(forma, x):
    f = delta_alpha(forma)
    h = 1e-4
    return (math.log(f(x * math.exp(h))) - math.log(f(x * math.exp(-h)))) / (2.0 * h)


def tiro(forma, d, nu, v0):
    """### **Un tiro da `v(0) = v0`:** ### **`+1` se attraversa lo zero** *(troppo alto)*, ### **`-1` se risale** *(troppo basso)*; ### **e la soluzione.**"""
    from scipy.integrate import solve_ivp
    f = delta_alpha(forma)
    S = 2.0 * math.pi if d == 2 else 4.0 * math.pi

    def rhs(xi, y):
        v, vp, _n, _m = y
        return [vp, -(d - 1) / xi * vp + (nu - f(v * v)) * v, S * xi ** (d - 1) * v * v, S * xi ** (d + 1) * v * v]

    def zero(xi, y):
        return y[0]
    zero.terminal = True

    def risale(xi, y):
        return y[1]
    risale.terminal = True
    risale.direction = 1
    y0 = [v0, (nu - f(v0 * v0)) * v0 * XI0 / d, 0.0, 0.0]
    so = solve_ivp(rhs, (XI0, XI_MAX), y0, method="DOP853", rtol=RTOL, atol=1e-300, events=(zero, risale))
    if so.t_events[0].size:
        return +1, so
    if so.t_events[1].size:
        return -1, so
    return 0, so


def soluzione(forma, d, nu):
    """### **Il fondamentale a `nu` per bisezione su `ln v0`:** ### **`(n, larghezza in xi, v0, v_taglio/v0)`.**"""
    f = delta_alpha(forma)
    # ### la soglia: f(v0^2) = nu (sotto, il tiro non parte verso il basso)
    a, b = math.log(1e-30), math.log(1e30)
    for _i in range(BISEZIONI):
        m = 0.5 * (a + b)
        if m in (a, b):
            break
        if f(math.exp(2.0 * m)) > nu:
            b = m
        else:
            a = m
    soglia = b
    hi = soglia + 1.0
    while tiro(forma, d, nu, math.exp(hi))[0] != +1:
        hi += 1.0
        assert hi < 70.0, (forma, d, nu)
    a, b = soglia, hi
    ultimo = None
    for _i in range(BISEZIONI):
        m = 0.5 * (a + b)
        if m in (a, b):
            break
        e, so = tiro(forma, d, nu, math.exp(m))
        if e == +1:
            b = m
        else:
            a = m
            ultimo = so
    if ultimo is None:
        ultimo = tiro(forma, d, nu, math.exp(a))[1]
    n, m2 = ultimo.y[2, -1], ultimo.y[3, -1]
    return n, math.sqrt(m2 / n), math.exp(a), abs(ultimo.y[0, -1]) / math.exp(a)


def sezione_b():
    import _solitoni_triangoli as STR
    print("### (b) sigma_eff(x) = d ln(alpha - alpha(0)) / d ln x: la formula chiusa (S1 2/(1+x^2), S4 p/(1+x^p), p = 2/pi) e le differenze finite sul codice; il critico 2/d: 1 in 2D, 2/3 in 3D")
    scarto = 0.0
    for x in X_TAB:
        r = []
        for fo in FORME:
            c, k = sigma_chiusa(fo, x), sigma_codice(fo, x)
            scarto = max(scarto, abs(c - k))
            r.append("%s %.4e" % (fo, k))
        print("  x %8.0e: sigma_eff  %s" % (x, "   ".join(r)))
    esito("DEVE PASSARE: sigma_eff dal codice = la formula chiusa entro 1e-6", scarto < 1e-6, "scarto %.1e" % scarto)
    print("### (b) la x del cuore dei solitoni misurati (x = rho/Lambda al centro) e li' sigma_eff")
    b = [json.loads(y) for y in io.open(DATI, encoding="utf-8") if y.strip()]
    for fo in FORME:
        for x in b:
            if x.get("tipo") == "esistenza" and x.get("griglia") == "triangoli" and x.get("forma") == fo and x.get("s") == 0.3 and x.get("lam0") == LAM0_TRI and x.get("verdetto") == "LEGATO":
                print("  bcbd1f40 %s s 0.3 N %8.0e: larghezza %7.3f archi, x_centro %10.4g, sigma_eff %.3e" % (fo, x["N"], x["larghezza"], x["x_centro"], sigma_chiusa(fo, x["x_centro"])))
    rif = [x for x in b if x.get("tipo") == "esistenza" and x.get("griglia") == "triangoli" and x.get("forma") == "S1" and x.get("s") == 0.3 and x.get("lam0") == LAM0_TRI and x.get("N") == 1e6][0]
    for L in (81, 120):
        a = json.loads(io.open(os.path.join(CL_PUNTI, "L%d_uniforme_00000.jsonl" % L), encoding="utf-8").read())
        z = json.loads(io.open(os.path.join(CL_PUNTI, "L%d_uniforme_08000.jsonl" % L), encoding="utf-8").read())
        x0 = a["punti"][0]["picco"] / (STR.AREA_NODO * LAM0_TRI)
        x1 = z["punti"][-1]["picco"] / (STR.AREA_NODO * LAM0_TRI)
        print("  40061005 S1 L %d: x al picco (picco / (AREA_NODO Lambda0)) al tick 0 %.4g, al tick %d %.4g; sigma_eff %.3e e %.3e; x_centro del risolutore a N 1e6 %.4g (rapporto %.4f)"
              % (L, x0, z["t1"], x1, sigma_chiusa("S1", x0), sigma_chiusa("S1", x1), rif["x_centro"], x0 / rif["x_centro"]))


def controlli_tiro():
    print("### I CONTROLLI DEL TIRO")
    for d in DIMENSIONI:
        for nu in (-1.0, 0.0, 1.0):
            n, w, _v0, q = soluzione("LOG", d, nu)
            es = math.pi ** (d / 2.0) * math.exp(nu - 1.0 + d)
            esito("DEVE PASSARE: il logaritmo, d %d, nu %+.1f: n = pi^(d/2) e^(nu - 1 + d) entro %g" % (d, nu, TOLL_ESATTA), abs(n / es - 1.0) < TOLL_ESATTA,
                  "n %.9g contro %.9g; larghezza %.6f contro %.6f" % (n, es, w, math.sqrt(d / 2.0)))
    n, _w, _v0, _q = soluzione("POT1", 2, 1.0)
    esito("DEVE PASSARE: Townes, d 2, la cubica a nu 1: n = 11.7009 entro 1e-4", abs(n / 11.7009 - 1.0) < 1e-4, "n %.6f" % n)
    for fo, d, att in (("POT1", 3, -0.5), ("POT0.5", 3, 0.5), ("POT2", 2, -0.5)):
        n1, _w, _v, _q = soluzione(fo, d, 0.5)
        n2, _w, _v, _q = soluzione(fo, d, 2.0)
        es = math.log(n2 / n1) / math.log(4.0)
        esito("DEVE PASSARE: la potenza x^%s in d %d: l'esponente di n(nu) = 1/sigma - d/2 = %+.2f entro %g" % (fo[3:], d, att, TOLL_ESPONENTE), abs(es - att) < TOLL_ESPONENTE, "%+.5f" % es)
        if att < 0:
            esito("DEVE RISULTARE INSTABILE (dn/dnu < 0): x^%s in d %d" % (fo[3:], d), n2 < n1, "n %.5g -> %.5g" % (n1, n2))
    b = [json.loads(y) for y in io.open(DATI, encoding="utf-8") if y.strip()]
    peggio = {}
    for x in b:
        if x.get("tipo") == "esistenza" and x.get("griglia") == "triangoli" and x.get("forma") in FORME and x.get("verdetto") == "LEGATO" and x.get("s") in (0.3, 0.99):
            fo, s, c = x["forma"], x["s"], x["c"]
            nu = x["mu"] / s - ALPHA0[fo]
            nd = x["N"] / (x["lam0"] * abs(c) / s)
            n, w, _v0, _q = soluzione(fo, 2, nu)
            e = abs(n / nd - 1.0)
            wl = x["larghezza"] / math.sqrt(abs(c) / s)
            print("  bcbd1f40 %s s %.2f lam0 %g N %8.0e: nu %.6f; n del risolutore %.6g, del tiro %.6g (%.1e); larghezza/l %.4f e %.4f" % (fo, s, x["lam0"], x["N"], nu, nd, n, e, wl, w))
            peggio[fo] = max(peggio.get(fo, 0.0), e)
    esito("DEVE PASSARE: il tiro in 2D contro i punti del risolutore di bcbd1f40 (S1, S4; s 0.3 e 0.99), n entro %g" % TOLL_RISOLUTORE,
          bool(peggio) and all(v < TOLL_RISOLUTORE for v in peggio.values()), "%s" % {k: "%.1e" % v for k, v in peggio.items()})


def sezione_cd():
    import _solitoni_triangoli as STR
    c3, _cy, _w = STR.c_triangoli(S_3D)
    l3 = math.sqrt(abs(c3) / S_3D)
    for d in DIMENSIONI:
        print("### (%s) d %d: n(nu) del fondamentale; VK: stabile se dn/dnu > 0 (la convenzione del risolutore: omega = mu riportato, nu = mu/s - alpha(0))" % ("c" if d == 2 else "d", d))
        for fo in FORME:
            righe = []
            for q in Q_GRIGLIA:
                nu = q * DMAX[fo]
                n, w, v0, qual = soluzione(fo, d, nu)
                righe.append((nu, n, w, v0, qual))
            for i, (nu, n, w, v0, qual) in enumerate(righe):
                if i == 0:
                    seg = "  "
                else:
                    seg = "+ " if n > righe[i - 1][1] else "- "
                extra = ("; N con c %.6f, s %g, Lambda0 6: %.4g" % (c3, S_3D, LAM0_TRI * l3 ** d * n)) if d == 3 else ""
                print("  %s d %d nu %.6e (nu/max %.4f): n %.6e  dn/dnu %s larghezza/l %.4f  v0 %.4e (x0 %.4e, sigma_eff(x0) %.3e)  v_taglio/v0 %.1e%s"
                      % (fo, d, nu, nu / DMAX[fo], n, seg, w, v0, v0 * v0, sigma_chiusa(fo, v0 * v0), qual, extra))
            ns = [r[1] for r in righe]
            i = int(np.argmin(ns))
            print("  %s d %d: n minimo sulla griglia %.6e a nu/max %.4f; dn/dnu < 0 sotto, > 0 sopra: %s" % (fo, d, ns[i], righe[i][0] / DMAX[fo],
                  all(ns[k] > ns[k + 1] for k in range(i)) and all(ns[k] < ns[k + 1] for k in range(i, len(ns) - 1))))


def sezione_r6():
    import _screening_forme_s3 as SF
    print("### R6: alpha e beta da una sola primitiva: dbeta/dx + x dalpha/dx = 0 (differenze finite sul codice);")
    print("    l'arrotondamento stimato: eps |x| / h / |x dalpha/dx| (per S1 a x piccolo beta ~ -2x^3/3 nasce da differenze di termini O(x)); il controllo: il residuo < 1e-6 + 10 volte l'arrotondamento")
    for fo in FORME:
        tutti = True
        for x in X_TAB:
            h = 1e-5 * x
            a1, b1 = SF._ab(fo, np.array([x + h]))
            a0, b0 = SF._ab(fo, np.array([x - h]))
            da, db = (a1 - a0)[0] / (2 * h), (b1 - b0)[0] / (2 * h)
            res = abs(db + x * da) / max(abs(x * da), 1e-300)
            arr = 2.2e-16 * max(x, abs(b1[0]), 1.0 if fo == "S4" else 0.0) / h / max(abs(x * da), 1e-300)
            tutti = tutti and res < 1e-6 + 10.0 * arr
            print("  %s x %8.0e: residuo %.2e, arrotondamento stimato %.2e" % (fo, x, res, arr))
        esito("DEVE PASSARE: R6 per %s, il residuo < 1e-6 + 10 volte l'arrotondamento su x 1e-6..1e4" % fo, tutti, "")
    x, h = 1.0, 1e-5
    da = (SF._ab("S1", np.array([x + h]))[0] - SF._ab("S1", np.array([x - h]))[0])[0] / (2 * h)
    res = abs(0.0 + x * da) / abs(x * da)
    esito("DEVE RISULTARE ROTTO: beta = 0 accanto all'alpha di S1 a x 1 (una beta non dalla primitiva)", res > 1e-6, "residuo %.2e" % res)


def referto():
    print("=" * 130)
    print("I REQUISITI DEL LEGAME, I CONTI SULLA CARTA (Luca 19:18): S1 e S4; l'inviluppo del risolutore in d 2 e 3; nessuna corsa del simulatore")
    print("=" * 130)
    print("  la configurazione: FORME %s ALPHA0 %s DMAX %s Q_GRIGLIA %s DIMENSIONI %s XI0 %g XI_MAX %g RTOL %g BISEZIONI %d TOLL_ESATTA %g TOLL_RISOLUTORE %g TOLL_ESPONENTE %g LAM0_TRI %g S_3D %g"
          % (FORME, ALPHA0, DMAX, Q_GRIGLIA, DIMENSIONI, XI0, XI_MAX, RTOL, BISEZIONI, TOLL_ESATTA, TOLL_RISOLUTORE, TOLL_ESPONENTE, LAM0_TRI, S_3D))
    print("  LE LETTURE, SCRITTE PRIMA: (b) il cuore sotto o sopra 2/d; (c), (d) dn/dnu > 0 stabile, < 0 instabile, ramo per ramo; un n minimo o no")
    print("-" * 130)
    sezione_b()
    print("-" * 130)
    sezione_r6()
    print("-" * 130)
    controlli_tiro()
    print("-" * 130)
    sezione_cd()
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if argv[:1] == ["--referto"]:
        referto()
    else:
        raise SystemExit(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
