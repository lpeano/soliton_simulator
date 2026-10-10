r"""IL COLLAUDO DEL BANCO `v3` — **e il primo braccio e' LA REGRESSIONE AL `v2`.**

> ## ⛔ **LA REGOLA DI FONDO DEL MANDATO:** la fisica del `v2` **non si invalida.** Quindi il
> ## primo braccio e' **`(R)`**: con `N` spento e il vuoto presente, lo spinore evolve
> ## ### **AL BIT** come nel `v2`. ### **Se non lo fa, tutto il resto non conta.**

### ⭐ **E LE DERIVATE SI VERIFICANO NUMERICAMENTE, non si assumono:** `dN/dh` contro `G'(x)` e
`dN/dLambda` contro `b(x)`, con una **differenza centrata**. ### **Un conto scritto nel task
history e' una promessa; un conto misurato e' un fatto.**

Gira con:  python proto_camminata/_collauda_banco3.py
"""
import io
import math
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import camminata3 as C3                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import nonlineare2 as N2                                       # noqa: E402
import interferenza3 as I3                                     # noqa: E402
import saturazione3 as S3                                      # noqa: E402
import scena as SC                                             # noqa: E402
import vuoto3 as V3                                            # noqa: E402

EPS = float(np.finfo(float).eps)
NLN = chr(10)
SEME = 11
PASSI = 40
EPS_SPIN = 0.5
FISICA3 = ("vuoto3.py", "saturazione3.py", "camminata3.py", "interferenza3.py",
           "_letture3.py")
CLIP = ("np.clip", ".clip(", "np.maximum", "np.minimum", "np.fmax", "np.fmin")


def main():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DEL BANCO v3 -- IL VUOTO E LA SATURAZIONE")
    print("=" * 100)
    SC._niente_simulatore()

    sc = SC.irregolare()
    uno = np.ones(sc["n"], dtype=float)
    nest = 2 * sc["m"]
    gmax = int(sc["grado"].max())
    st = C3.stato3(sc, SEME)
    tol = PASSI * gmax * EPS * math.sqrt(CM.norma(st["psi"]))
    tolN = PASSI * nest * EPS
    ident = GE.scena_identita(sc)
    gauge = GE.scena_gauge_puro(sc, SEME)
    curva = GE.scena_curva(sc, SEME)
    SCENE = (("identita", ident), ("gauge_puro", gauge), ("curva", curva))

    # ================================================================ (R) REGRESSIONE
    for nome, geo in SCENE:
        a = st["psi"].copy()
        for _ in range(PASSI):
            a = C2.passo2(a, sc, geo, uno, 1.0, EPS_SPIN)
        b = dict(st)
        for _ in range(PASSI):
            b = C3.passo3(b, sc, geo, uno, 1.0, EPS_SPIN, None)
        d = float(np.max(np.abs(b["psi"] - a)))
        esito("### (R) REGRESSIONE al v2, N spento, AL BIT -- %s" % nome, d == 0.0,
              "### max|psi3 - psi2| = %.3g su %d tick: ### il v3 NON invalida il v2"
              % (d, PASSI))

    # ================================================================ LE DERIVATE
    hh, ll, dd = 0.7, 1.3, 1e-6
    dh = (S3.energia(np.array([hh + dd]), np.array([ll]))[0]
          - S3.energia(np.array([hh - dd]), np.array([ll]))[0]) / (2 * dd)
    dl = (S3.energia(np.array([hh]), np.array([ll + dd]))[0]
          - S3.energia(np.array([hh]), np.array([ll - dd]))[0]) / (2 * dd)
    x = hh / ll
    e1 = abs(dh - S3.Gp(x))
    e2 = abs(dl - S3.b(x))
    esito("### le DERIVATE di N, verificate con una differenza centrata",
          e1 < 1e-8 and e2 < 1e-8,
          "### dN/dh contro G'(x): %.3g   dN/dLambda contro b(x): %.3g" % (e1, e2))
    esito("### la SATURAZIONE: `G'` e- LIMITATA e cresce dove deve",
          S3.Gp(0.125) < 0.02 and 0.49 < S3.Gp(1.0) < 0.51 and S3.Gp(64.0) > 0.999,
          "### G'(1/8) = %.4f, G'(1) = %.4f, G'(64) = %.6f: il ginocchio e- a x ~ 1"
          % (S3.Gp(0.125), S3.Gp(1.0), S3.Gp(64.0)))
    al, be = S3.pezzi(np.array([0.5]), np.array([0.0]))
    esito("### il LIMITE Lambda -> 0 e- FINITO e vale il limite analitico",
          abs(al[0] - 1.0) == 0.0 and abs(be[0] + 0.5 * math.pi) < 1e-15,
          "### G' = %.6f (deve essere 1), b = %.6f (deve essere -pi/2 = %.6f)"
          % (al[0], be[0], -0.5 * math.pi))

    # ================================================================ GLI INVARIANTI
    h0 = N2.elicita_nodo(st["psi"], sc, ident)
    l0 = V3.lambda_nodo(st["phi"], sc)
    p1, f1 = S3.flusso(st["psi"], st["phi"], sc, ident, np.full(sc["n"], 0.37))
    dh2 = float(np.max(np.abs(N2.elicita_nodo(p1, sc, ident) - h0)))
    dl2 = float(np.max(np.abs(V3.lambda_nodo(f1, sc) - l0)))
    esito("### GLI INVARIANTI del flusso: `h` e `Lambda` NON cambiano",
          dh2 <= tol and dl2 <= tol,
          "### max|h - h'| = %.3g   max|Lambda - Lambda'| = %.3g (soglia %.3g): ### e- "
          "per questo che il flusso e- in FORMA CHIUSA" % (dh2, dl2, tol))

    # ================================================================ LE NORME
    for nome, geo in SCENE:
        s = dict(st)
        for _ in range(PASSI):
            s = C3.passo3(s, sc, geo, uno, 1.0, EPS_SPIN, S3.flusso)
        dp = abs(CM.norma(s["psi"]) - CM.norma(st["psi"]))
        df = abs(V3.norma_vuoto(s["phi"]) - V3.norma_vuoto(st["phi"]))
        esito("le DUE norme si conservano con N acceso -- %s" % nome,
              dp <= tolN and df <= tolN * V3.norma_vuoto(st["phi"]),
              "### psi %.3g (soglia %.3g)   phi %.3g" % (dp, tolN, df))

    # ================================================================ (V) REVERSIBILITA'
    k = 20
    for nome, geo in (("identita", ident), ("curva", curva)):
        c = dict(st)
        for _ in range(k):
            c = C3.passo3(c, sc, geo, uno, 1.0, EPS_SPIN, S3.flusso)
        for _ in range(k):
            c = C3.passo3_inverso(c, sc, geo, uno, 1.0, EPS_SPIN, S3.flusso)
        dp = float(np.max(np.abs(c["psi"] - st["psi"])))
        df = float(np.max(np.abs(c["phi"] - st["phi"])))
        s5 = 2 * k * nest * EPS
        esito("### (V) REVERSIBILITA-: %d avanti e %d indietro -- %s" % (k, k, nome),
              dp <= s5 and df <= s5,
              "### psi %.3g   phi %.3g   soglia 2k*n_est*eps = %.3g" % (dp, df, s5))

    # ================================================================ LA C ESTESA
    a = C3.coniuga3(C3.passo3(st, sc, ident, uno, 1.0, EPS_SPIN, S3.flusso))
    b = C3.passo3(C3.coniuga3(st), sc, ident, uno, 1.0, EPS_SPIN, S3.flusso)
    dp = float(np.max(np.abs(a["psi"] - b["psi"])))
    df = float(np.max(np.abs(a["phi"] - b["phi"])))
    esito("### la `C` ESTESA commuta col passo INTERO, AL BIT -- identita",
          dp == 0.0 and df == 0.0,
          "### psi %.3g   phi %.3g: `G'` e- PARI e `b` e- DISPARI" % (dp, df))
    for nome, geo in (("gauge_puro", gauge), ("curva", curva)):
        det = np.linalg.det(geo["U"]).reshape(-1, 1, 1)
        gc = dict(geo)
        gc["U"] = geo["U"] / det
        a = C3.coniuga3(C3.passo3(st, sc, geo, uno, 1.0, EPS_SPIN, S3.flusso))
        b = C3.passo3(C3.coniuga3(st), sc, gc, uno, 1.0, EPS_SPIN, S3.flusso)
        d = float(np.max(np.abs(a["psi"] - b["psi"])))
        esito("### e in `%s` manda nella ANTI-camminata" % nome, d <= tol,
              "### max|C U - U_coniugata C| = %.3g (soglia %.3g)" % (d, tol))

    # ================================================================ IL CONTROLLO su rho
    a = C3.coniuga3(C3.passo3(st, sc, ident, uno, 1.0, EPS_SPIN, S3.flusso_su_rho))
    b = C3.passo3(C3.coniuga3(st), sc, ident, uno, 1.0, EPS_SPIN, S3.flusso_su_rho)
    d = float(np.max(np.abs(a["psi"] - b["psi"])))
    esito("### DEVE ROMPERE `C`: la stessa saturazione su `rho` (PARI)", d > 1e-6,
          "### max|C U - U C| = %.3g: ### e- il controllo che DEVE fallire" % d)

    # ================================================================ (G) GAUGE con N
    def ruota(p, g, fi):
        o = np.empty_like(p)
        for e in range(p.shape[0]):
            kk = int(sc["nodo"][e])
            o[e] = np.exp(1j * fi[kk]) * (g[kk] @ p[e])
        return o

    si = dict(st)
    sg = {"psi": ruota(st["psi"], gauge["g"], gauge["fi"]), "phi": st["phi"].copy()}
    for _ in range(PASSI):
        si = C3.passo3(si, sc, ident, uno, 1.0, EPS_SPIN, S3.flusso)
        sg = C3.passo3(sg, sc, gauge, uno, 1.0, EPS_SPIN, S3.flusso)
    dg = float(np.max(np.abs(CM.rho_nodo(si["psi"], sc) - CM.rho_nodo(sg["psi"], sc))))
    esito("### (G) il GAUGE regge anche con il vuoto e `N` accesi", dg <= tol,
          "### max|rho - rho'| = %.3g (soglia %.3g), e il vuoto e- NEUTRO: non si "
          "trasforma" % (dg, tol))

    # ================================================================ (2) IL CONO con N
    d0 = SC.distanze(sc, 0)
    T = max(1, int(d0.max()) // 2)
    e0 = int(np.nonzero(sc["nodo"] == 0)[0][0])
    u1 = {"psi": CM.stato_zero(sc), "phi": V3.vuoto_fondo(sc, V3.LAMBDA0, SEME)}
    u1["psi"][e0, 0] = 1.0
    u2 = {"psi": u1["psi"].copy(), "phi": u1["phi"].copy()}
    u2["psi"][e0, 0] = 1.0 + 1e-3
    for _ in range(T):
        u1 = C3.passo3(u1, sc, curva, uno, 1.0, EPS_SPIN, S3.flusso)
        u2 = C3.passo3(u2, sc, curva, uno, 1.0, EPS_SPIN, S3.flusso)
    dif = np.abs(u1["psi"] - u2["psi"]).sum(axis=1)
    fuori = dif[d0[sc["nodo"]] > T]
    esito("### (2) IL CONO con il vuoto e `N`: oltre %d archi ZERO ESATTO" % T,
          fuori.size > 0 and float(np.max(fuori)) == 0.0,
          "### max fuori = %.3g su %d estremita-"
          % (float(np.max(fuori)) if fuori.size else -1, int(fuori.size)))

    # ================================================================ L-INTERFERENZA
    # ### ⭐ **LA SECONDA CANDIDATA, dall-era 1** *(aggiunta di Luca,
    # ### 2026-10-11)*: `S_k` e- ### **il campo di interferenza locale**, e i bracci qui
    # ### sotto provano le ### **DUE derivazioni** del task history prima di usarla.
    cc = I3.coerenza(st["psi"], sc)
    esito("### MATERIA: la coerenza `c_k` sta in [0,1] e NON e- degenere",
          float(cc.min()) >= 0.0 and float(cc.max()) <= 1.0 and float(cc.max()) > 0.5,
          "### min %.6f  max %.6f: e- la <<coerenza>> dell-era 1, e qui ha una forma ESATTA"
          % (cc.min(), cc.max()))
    hS = I3.elicita_interferenza(st["psi"], sc, ident)
    hSc = I3.elicita_interferenza(C2.coniuga2(st["psi"]), sc, ident)
    esito("### `(D)` l-elicita- dell-INTERFERENZA e- DISPARI sotto `C`, AL BIT",
          float(np.max(np.abs(hSc + hS))) == 0.0,
          "### max|h^S(C psi) + h^S(psi)| = %.3g: la derivazione usava "
          "`sigma_y (sigma.n) sigma_y = -(sigma.n)*`"
          % float(np.max(np.abs(hSc + hS))))
    se = np.sum(np.abs(I3.campo_S(st["psi"], sc)) ** 2, axis=1)
    sec = np.sum(np.abs(I3.campo_S(C2.coniuga2(st["psi"]), sc)) ** 2, axis=1)
    esito("### e `(E)` su `|S|^2` e- PARI sotto `C`, AL BIT",
          float(np.max(np.abs(sec - se))) == 0.0,
          "### max differenza = %.3g: ### e- per questo che DEVE rompere `C`"
          % float(np.max(np.abs(sec - se))))
    ruo = np.empty_like(st["psi"])
    for e in range(2 * sc["m"]):
        kk = int(sc["nodo"][e])
        ruo[e] = np.exp(1j * gauge["fi"][kk]) * (gauge["g"][kk] @ st["psi"][e])
    hg = I3.elicita_interferenza(ruo, sc, gauge)
    hb = I3.elicita_interferenza(ruo, sc, {"n": gauge["n_non_ruotati"]})
    d1 = float(np.max(np.abs(hS - hg)))
    d2 = float(np.max(np.abs(hS - hb)))
    esito("### e `h^S` e- INVARIANTE DI GAUGE", d1 <= tol,
          "### max|h^S - h^S-| = %.3g (soglia %.3g)" % (d1, tol))
    esito("### DEVE FALLIRE: `h^S` senza ruotare i versori NON e- invariante", d2 > 1e-6,
          "### %.3g, cioe- %d ordini sopra: ### **i versori servono anche qui**"
          % (d2, int(round(math.log10(d2 / max(d1, EPS))))))

    # ### \u26d4 **IL PUNTO MEDIO IMPLICITO: converge, conserva, e SI INVERTE.**
    for et, fl, _n in I3.LE_DUE_INTERF:
        p1, f1 = fl(st["psi"], st["phi"], sc, ident, np.full(sc["n"], 0.25))
        p0, f0 = fl(p1, f1, sc, ident, np.full(sc["n"], -0.25))
        dn = abs(CM.norma(p1) - CM.norma(st["psi"]))
        dv = abs(V3.norma_vuoto(f1) - V3.norma_vuoto(st["phi"]))
        dr = float(np.max(np.abs(p0 - st["psi"])))
        esito("### il PUNTO MEDIO `(%s)`: norme ESATTE e ritorno esatto" % et,
              dn <= tolN and dv <= tolN * V3.norma_vuoto(st["phi"]) and dr <= tol,
              "### norma psi %.3g   phi %.3g   ritorno %.3g: `A` e- HERMITIANA, e per "
              "questo la norma e- esatta" % (dn, dv, dr))

    # ### \u26d4 **E SUL PASSO INTERO: `(D)` tiene `C`, `(E)` la ROMPE.**
    for et, fl, _n in I3.LE_DUE_INTERF:
        a = C3.coniuga3(C3.passo3(st, sc, ident, uno, 1.0, EPS_SPIN, fl))
        b = C3.passo3(C3.coniuga3(st), sc, ident, uno, 1.0, EPS_SPIN, fl)
        d = float(np.max(np.abs(a["psi"] - b["psi"])))
        if et == "D":
            esito("### `(D)` tiene la `C` sul passo INTERO", d <= tol,
                  "### max|C U - U C| = %.3g (soglia %.3g)" % (d, tol))
        else:
            esito("### DEVE ROMPERE `C`: `(E)`, il porto letterale", d > 1e-6,
                  "### max|C U - U C| = %.3g: ### il braccio che DEVE fallire" % d)

    # ### \u2705 **E la REGRESSIONE vale anche per loro: con le due spente, e- il v2.**
    for et, fl, _n in I3.LE_DUE_INTERF:
        aa = st["psi"].copy()
        for _ in range(PASSI):
            aa = C2.passo2(aa, sc, ident, uno, 1.0, EPS_SPIN)
        bb = dict(st)
        for _ in range(PASSI):
            bb = C3.passo3(bb, sc, ident, uno, 1.0, EPS_SPIN, None)
        esito("### (R) e con `(%s)` SPENTA resta il v2, AL BIT" % et,
              float(np.max(np.abs(bb["psi"] - aa))) == 0.0,
              "### max|psi3 - psi2| = %.3g" % float(np.max(np.abs(bb["psi"] - aa))))

    # ================================================================ IL BANCO
    testi = {}
    for nome in FISICA3:
        p = os.path.join(_QUI, nome)
        testi[nome] = io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    cattivi = [n for n, t in testi.items()
               if ("import soliton_simulator" in t or "from soliton_simulator" in t)]
    esito("### il banco v3 non IMPORTA il simulatore", not cattivi,
          "### %d file guardati%s" % (len(testi), (": %s" % cattivi) if cattivi else ""))
    trovati = [(n, c) for n, t in testi.items() for c in CLIP if c in t]
    esito("### NESSUN clip nei file di fisica del banco v3", not trovati,
          "### %d forme cercate: il limite Lambda -> 0 e- ANALITICO, non un pavimento%s"
          % (len(CLIP), (": %s" % trovati) if trovati else ""))

    # ================================================================ IL DETERMINISMO
    imp = []
    for _ in range(2):
        pr = subprocess.run([sys.executable, os.path.join(_QUI, "camminata3.py")],
                            cwd=RADICE, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        imp.append((pr.stdout or "").strip())
    esito("### il DETERMINISMO fra DUE PROCESSI: uscita identica",
          len(imp) == 2 and imp[0] == imp[1] and bool(imp[0]),
          "### %d caratteri confrontati" % len(imp[0] if imp else ""))

    print("=" * 100)
    print("IL COLLAUDO DEL BANCO v3: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
