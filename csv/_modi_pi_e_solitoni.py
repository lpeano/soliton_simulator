r"""**I MODI A `k = pi` E I SOLITONI LARGHI: dove sta la fisica a bassa energia, e i solitoni larghi** *(solo misure, in memoria; zero simmetrico dove non detto altro)*.

> ### ⛔ **Il task history e' `2026-10-23_modi_pi_e_solitoni.md`** *(le esplorazioni, il metodo, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`, l'impronta, la convenzione nel
> repo e il nucleo intatti.** ### **Importati, non copiati:** `_segno_gravita`, `_zero_simmetrico`, `_forza_da_cs` *(e la sua `PORTANTE`)*, `_gravita_collettiva` *(`profilo`)*, `_scala_e_zero`,
> `_massa_vicino_al_cono`, `_moneta_massa`, `_universalita_massa`.

### **PARTE A:** ### **le bande lungo le tre linee, il salto minimo di ogni gruppo, il punto `k*`, e a `k*`: fase continua, curvatura (tensore), `v`, `E0`, `M`, `D`, `a_H/a_RG` nelle due
convenzioni, `lambda*`.** ### **PARTE B:** ### **la forza col pacchetto sul modo a `k*`** *(`_forza_da_cs.corsa` con la `PORTANTE`)*. ### **PARTE C.1-C.2:** ### **i solitoni con la scatola in
archi, la tabella delle larghezze, il primo `s` largo `>= 4` archi.** ### **La dinamica dei solitoni** *(C.3)* ### **e' in uno strumento a se'.**

Gira con:  python csv/_modi_pi_e_solitoni.py > doc/referti_l2/modi_pi_e_solitoni.txt
"""
import contextlib
import io
import json
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

S_A = (0.1, 0.3, 0.5, 0.9)
EPS = (0.0, 0.5)
L = 64
H = 1e-3
PUNTI = (("(pi,0)", "x", (32, 0)), ("(0,pi)", "y", (0, 32)), ("(pi,pi)", "d", (32, 32)))
SALTO_NULLO = 1e-6
S0_B = (0.3, 0.5)
ETA_B = (0.0, 5e-4, 1e-3, 5e-3, 1e-2)
LX_B = 256
FORME = ("S1", "S3", "S4")
S_C = (0.3, 0.5, 0.7, 0.9, 0.95, 0.99)
N_C = (10.0, 100.0, 1e3, 1e4, 1e5, 1e6, 1e7)
LAM0 = 4.0
LARGHEZZA_MIN = 4.0
W_MAX = 3000.0
PUNTI_PER_W = 640
CONV = ("oggi", "simm")
J_SG = os.path.join(RADICE, "doc", "referti_l2", "segno_gravita.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "modi_pi_e_solitoni.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


def f_(x, fm="%+.4f"):
    return "--" if x is None else fm % x


def conv(nome):
    import _zero_simmetrico as ZS
    return ZS.convenzione_simmetrica() if nome == "simm" else contextlib.nullcontext()


def av(x):
    return float((x + np.pi) % (2.0 * np.pi) - np.pi)


# =====================================================================================
#   PARTE A -- LE BANDE, IL SALTO, k*
# =====================================================================================
def bande(s, eps, nome):
    """### I gruppi massivi *(da `k = 0`)*, i loro rami, le fasi lungo le tre linee, e la matrice."""
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    import _massa_vicino_al_cono as MV
    with conv(nome):
        lista = F.rami(s, eps)[0]
        A = MV.matrice(L, 1.0, eps, s)
    gg = GC.gruppi(lista)
    idx = [[r["ramo"] for r in lista if abs(r["omega0"] - g["omega0"]) <= GC.TOLL_DISTINTI and r["omega1"] in g["omega1"]] for g in gg]
    D = np.zeros_like(A)
    for m in range(L):
        D[m, 0] = A[m, m]
    ph = {"x": MV.rami_seguiti(A, L), "y": MV.rami_seguiti(A.transpose(1, 0, 2, 3), L), "d": MV.rami_seguiti(D, L)}
    return gg, idx, ph, A


def salto(ph, idx, i):
    """### Il salto del gruppo `i`: la distanza dalla banda piu' vicina NON del suo gruppo, lungo le tre linee, e ai tre punti."""
    a = idx[i][0]
    # ### ⚠ **le bande DEGENERI col gruppo a `k = 0`** *(le sue copie e le bande piatte con la stessa `omega(0)`)* ### **non sono «altre»**: ### **il loro «salto» nullo a `k = 0`
    # ### e' la degenerazione, non un salto** *(visto nella prova a vuoto, annotazione `1`)*
    P0 = ph["x"][0]
    altri = [b for b in range(8) if b not in idx[i] and abs(av(P0[b] - P0[a])) > 1e-9]
    best, ai_punti = None, {}
    for lin, P in ph.items():
        d = np.min(np.abs((P[:, [a]] - P[:, altri] + np.pi) % (2.0 * np.pi) - np.pi), axis=1)
        m = int(np.argmin(d))
        if best is None or d[m] < best["distanza"]:
            best = {"linea": lin, "m": m, "distanza": float(d[m]), "fase": av(P[m, a])}
        for nome, ll, _mm in PUNTI:
            if ll == lin:
                ai_punti[nome] = {"distanza": float(d[L // 2]), "fase": av(P[L // 2, a])}
    return best, ai_punti


def autospazio(B, w):
    lam, V = np.linalg.eig(B)
    sel = [j for j in range(len(lam)) if abs(av(-np.angle(lam[j]) - w)) <= 1e-9]
    Q, _ = np.linalg.qr(V[:, sel])
    return Q


def fase_seguita(B, Q):
    """### La fase dell'autovettore di `B` con la sovrapposizione massima con lo spazio `Q`."""
    lam, V = np.linalg.eig(B)
    ov = np.linalg.norm(Q.conj().T @ V, axis=0)
    j = int(np.argmax(ov))
    return float(-np.angle(lam[j])), V[:, [j]]


def a_k(A, m1, m2, w0, Q):
    """### A `k* = (m1, m2)`: la curvatura (tensore) dalle fasi esatte, `v_g`, e `v` dal fit lungo `x`."""
    import _moneta_massa as MM
    k1 = 2.0 * np.pi / L

    def ph(d1, d2):
        return w0 + av(fase_seguita(A[(m1 + d1) % L, (m2 + d2) % L, :8, :8], Q)[0] - w0)
    p = {d: ph(*d) for d in ((1, 0), (-1, 0), (2, 0), (-2, 0), (0, 1), (0, -1), (0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1))}
    xx = (-p[(2, 0)] + 16 * p[(1, 0)] - 30 * w0 + 16 * p[(-1, 0)] - p[(-2, 0)]) / (12 * k1 * k1)
    yy = (-p[(0, 2)] + 16 * p[(0, 1)] - 30 * w0 + 16 * p[(0, -1)] - p[(0, -2)]) / (12 * k1 * k1)
    xy = (p[(1, 1)] - p[(1, -1)] - p[(-1, 1)] + p[(-1, -1)]) / (4 * k1 * k1)
    vg = ((p[(1, 0)] - p[(-1, 0)]) / (2 * k1), (p[(0, 1)] - p[(0, -1)]) / (2 * k1))
    qq, yv, Qc, wc = [0.0], [0.0], Q, w0
    for m in range(1, 9):
        wm, Vm = fase_seguita(A[(m1 + m) % L, m2, :8, :8], Qc)
        wc = wc + av(wm - wc)
        qq.append(m * k1)
        yv.append(wc - w0)
        Qc = Vm
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        Df, vf, sc = MM.fit_massa(np.array(qq), np.array(yv))
    return {"curv_xx": float(xx), "curv_yy": float(yy), "curv_xy": float(xy), "v_g": [float(vg[0]), float(vg[1])], "v": float(vf), "Dt_fit": float(Df), "scarto_fit": float(sc)}


def cammino_k(eps, m1, m2, nome):
    """### La fase continua da `s` piccolo AL PUNTO `k*`: `_scala_e_zero.cammino` con `blocchi` avvolta in memoria (lato `16`)."""
    import _massa_vicino_al_cono as MV
    import _scala_e_zero as Z
    vero = Z.blocchi

    def blocchi(s, e, Lf=Z.L_FINE):
        A = MV.matrice(Lf, 1.0, e, s)
        b = A[m1 * Lf // L, m2 * Lf // L, :8, :8].copy()
        return b, b
    Z.blocchi = blocchi
    try:
        with conv(nome):
            C, salti = Z.cammino(eps)
    finally:
        Z.blocchi = vero
    return C, salti


def parte_A():
    import _gravita_collettiva as GC
    import _scala_e_zero as Z
    import _zero_simmetrico as ZS
    print("### PARTE A -- I MODI A k = pi (zero simmetrico; s %s; eps %s; lato %d; le linee verso (pi,0), (0,pi), (pi,pi))" % (S_A, EPS, L))
    righe, minimi, cam = [], [], {}
    for eps in EPS:
        for s in S_A:
            gg, idx, ph, A = bande(s, eps, "simm")
            for i, g in enumerate(gg):
                best, pt = salto(ph, idx, i)
                nr = ZS.nome_curv(g)
                kk = {"x": (best["m"], 0), "y": (0, best["m"]), "d": (best["m"], best["m"])}[best["linea"]]
                minimi.append({"eps": eps, "s": s, "ramo": nr, "k_min": [2.0 * kk[0] / L, 2.0 * kk[1] / L], **best})
                scrivi(dict(minimi[-1], tipo="salto_minimo", ai_punti=pt))
                print("  eps %-3g s %-4g %-18s: il salto minimo %.5f a k = (%.3f, %.3f) pi, fase %+.4f | (pi,0) %.4f  (0,pi) %.4f  (pi,pi) %.4f"
                      % (eps, s, nr, best["distanza"], 2.0 * kk[0] / L, 2.0 * kk[1] / L, best["fase"], pt["(pi,0)"]["distanza"], pt["(0,pi)"]["distanza"],
                         pt["(pi,pi)"]["distanza"]))
                cand = sorted((pt[n]["distanza"], n, mm) for n, _l, mm in PUNTI if pt[n]["distanza"] >= SALTO_NULLO)
                scelto = None
                for dist, nk, (m1, m2) in cand:
                    w0 = pt[nk]["fase"]
                    Q = autospazio(A[m1, m2, :8, :8], w0)
                    loc = a_k(A, m1, m2, w0, Q)
                    # ### ⚠ **un punto dove la banda e' PIATTA** *(curvatura o `v` nulli)* ### **non e' un modo massivo fermo: si passa al prossimo** *(annotazione `1`)*
                    if abs(loc["curv_xx"]) >= 1e-6 and loc["v"] >= 1e-6:
                        scelto = (dist, nk, m1, m2, w0, Q, loc)
                        break
                    print("    %s: la banda e' piatta (curvatura %+.1e, v %.1e): non e' un modo massivo fermo" % (nk, loc["curv_xx"], loc["v"]))
                if scelto is None:
                    print("    -> nessun punto a k = pi con salto non nullo e banda non piatta")
                    scrivi({"tipo": "modo_assente", "eps": eps, "s": s, "ramo": nr})
                    continue
                dist, nk, m1, m2, w0, Q, loc = scelto
                rec = {"tipo": "modo", "eps": eps, "s": s, "ramo": nr, "k_star": nk, "salto": dist, "fase_principale": w0, "dim": Q.shape[1], **loc}
                for nome in CONV:
                    key = (eps, m1, m2, nome)
                    if key not in cam:
                        cam[key] = cammino_k(eps, m1, m2, nome)
                    C, salti = cam[key]
                    sh = np.pi * s if nome == "simm" else 0.0
                    w_pr = av(w0 - (np.pi * s) + sh)          # la fase principale in quella convenzione (w0 e' della simmetrica)
                    lv = Z.livelli(C, s, w_pr)
                    if not lv:
                        rec[nome] = None
                        continue
                    lvl = min(lv)
                    w3 = [float(Z.a_(C[0], x)["w"][lvl]) for x in (s * (1 - H), s, s * (1 + H))]
                    D = GC.dproprio(w3[0], w3[1], w3[2], s * (1 - H), s, s * (1 + H))
                    dw = (w3[2] - w3[0]) / (2.0 * H * s)
                    rec[nome] = {"omega_cont": w3[1], "E0": w3[1] / s, "M": loc["curv_xx"] / s, "E0M_positivo": (w3[1] / s) * (loc["curv_xx"] / s) > 0,
                                 "D": D, "d_omega_ds": dw, "H_su_RG": s * loc["curv_xx"] / loc["v"] ** 2 * dw if loc["v"] else None,
                                 "candidati": len(lv), "salto_cammino": salti}
                righe.append(rec)
                scrivi(rec)
                for nome in CONV:
                    q = rec[nome]
                    if q is None:
                        print("    %s a %s: il livello del cammino non trovato" % (nome, nk))
                        continue
                    print("    %s a %s (salto %.4f, dim %d): omega %+.5f E0 %+.4f | curv xx %+.4f yy %+.4f xy %+.4f | v_g (%+.1e, %+.1e) v %.4f | M %+.4f E0 M %s | D %+.3e | a_H/a_RG %s"
                          % (nome, nk, dist, Q.shape[1], q["omega_cont"], q["E0"], loc["curv_xx"], loc["curv_yy"], loc["curv_xy"], loc["v_g"][0], loc["v_g"][1],
                             loc["v"], q["M"], "POSITIVO" if q["E0M_positivo"] else "negativo", q["D"], f_(q["H_su_RG"])))
                sys.stdout.flush()
    print("### lambda* a k* (le coppie di gruppi con lo stesso k* e lo stesso s): a_H/a_RG(lambda) per la retta per lambda 0 e 1/2")
    for eps in EPS:
        for s in S_A:
            rr = [r for r in righe if r["eps"] == eps and r["s"] == s and r["oggi"] and r["simm"] and r["oggi"]["H_su_RG"] is not None and r["simm"]["H_su_RG"] is not None]
            for i in range(len(rr)):
                for j in range(i + 1, len(rr)):
                    if rr[i]["k_star"] != rr[j]["k_star"]:
                        continue
                    a0, a5, b0, b5 = rr[i]["oggi"]["H_su_RG"], rr[i]["simm"]["H_su_RG"], rr[j]["oggi"]["H_su_RG"], rr[j]["simm"]["H_su_RG"]
                    ma, mb = 2.0 * (a5 - a0), 2.0 * (b5 - b0)
                    ls = (b0 - a0) / (ma - mb) if ma != mb else None
                    scrivi({"tipo": "lambda_stella_k", "eps": eps, "s": s, "k_star": rr[i]["k_star"], "rami": [rr[i]["ramo"], rr[j]["ramo"]], "lambda_stella": ls})
                    print("  eps %-3g s %-4g %s / %s a %s: lambda* %s" % (eps, s, rr[i]["ramo"], rr[j]["ramo"], rr[i]["k_star"], f_(ls, "%.6f")))
    return righe, minimi


# =====================================================================================
#   PARTE B -- LA FORZA SUI MODI A k*
# =====================================================================================
def parte_B(righe):
    import _forza_da_cs as F
    print("### PARTE B -- LA FORZA SUL MODO A k* (s0 %s, eta %s, Lx %d, le due convenzioni; la corsa di _forza_da_cs con la PORTANTE)" % (S0_B, ETA_B, LX_B))
    out = []
    for r in [x for x in righe if x["s"] in S0_B]:
        m1, m2 = [mm for n, _l, mm in PUNTI if n == r["k_star"]][0]
        gg, idx, ph, A = bande(r["s"], r["eps"], "oggi")
        w_oggi = av(r["fase_principale"] - np.pi * r["s"])
        Q = autospazio(A[m1, m2, :8, :8], w_oggi)
        corse = {}
        for nome in CONV:
            vero = F.PORTANTE
            F.PORTANTE = (2.0 * np.pi * m1 / L, 2.0 * np.pi * m2 / L)
            try:
                for eta in ETA_B:
                    with conv(nome):
                        corse[(nome, eta)] = F.corsa(LX_B, r["eps"], r["s"], eta, Q)
            finally:
                F.PORTANTE = vero
            q = r[nome]
            for eta in ETA_B:
                c = corse[(nome, eta)]
                scrivi(dict(c, tipo="corsa", convenzione=nome, ramo=r["ramo"], k_star=r["k_star"]))
            for eta in (1e-3, 1e-2):
                c, h = corse[(nome, eta)], corse[(nome, eta / 2.0)]
                lin = c["a"] / h["a"] if c["a"] is not None and h["a"] else None
                dsdx = -r["s"] * eta * 2.0 * np.pi / LX_B
                a_RG = -r["v"] ** 2 * dsdx / r["s"]
                a_H = -r["curv_xx"] * q["d_omega_ds"] * dsdx if q else None
                rec = {"tipo": "forza_k", "convenzione": nome, "eps": r["eps"], "s0": r["s"], "ramo": r["ramo"], "k_star": r["k_star"], "eta": eta, "a_mis": c["a"],
                       "sigma_a": c["sigma_a"], "a_RG": a_RG, "a_H": a_H, "mis_su_RG": None if c["a"] is None else c["a"] / a_RG,
                       "mis_su_H": None if c["a"] is None or not a_H else c["a"] / a_H, "lin": lin, "fuori_max": c["fuori_max"],
                       "leggibile": bool(c["leggibile"] and lin is not None and abs(lin / 2.0 - 1.0) < 0.05)}
                out.append(rec)
                scrivi(rec)
                print("  %-4s eps %-3g s0 %-4g %-18s a %s eta %-5g: a %s (+- %s) | a/a_RG %s a/a_H %s | lin %s | fuori %.3f | %s%s"
                      % (nome, r["eps"], r["s"], r["ramo"], r["k_star"], eta, f_(c["a"], "%+.3e"), f_(c["sigma_a"], "%.1e"), f_(rec["mis_su_RG"], "%+.3f"),
                         f_(rec["mis_su_H"], "%+.3f"), f_(lin, "%.3f"), c["fuori_max"] or 0.0,
                         "--" if c["a"] is None else ("verso cs BASSO" if rec["mis_su_RG"] > 0 else "verso cs ALTO"), "" if rec["leggibile"] else "  ### NON SI LEGGE"))
            z = corse[(nome, 0.0)]
            out.append({"tipo": "zero_k", "convenzione": nome, "eps": r["eps"], "s0": r["s"], "ramo": r["ramo"], "a": z["a"], "sigma_a": z["sigma_a"],
                        "nullo": z["a"] is not None and F.nullo(z)})
            scrivi(out[-1])
    return out


# =====================================================================================
#   PARTE C -- I SOLITONI LARGHI
# =====================================================================================
def largo(forma, c, s, N):
    """### Lo stato legato con la scatola in ARCHI: `R = 10 w`, `dr = w/640`, la partenza larga `w`; ripetuto finche' la larghezza non cambia oltre `1e-3`."""
    import _gravita_collettiva as GC
    sig = np.sqrt(abs(c) / s)
    w = max(sig, 1.0)
    q = None
    for it in range(20):
        dr = w / PUNTI_PER_W
        M = int(np.ceil(10.0 * w / dr))
        q = GC.profilo(forma, c, s, N, LAM0, dr, M, w)[0]
        if q["stato"] != "CONVERGE":
            return dict(q, giri=it + 1, verdetto=q["stato"])
        wn = q["larghezza"]
        if abs(wn - w) / w < 1e-3:
            return dict(q, giri=it + 1, verdetto="LEGATO" if q["esiste"] == "LEGATO" else q["esiste"])
        if wn > W_MAX:
            return dict(q, giri=it + 1, verdetto="DISPERSIONE (oltre %g archi)" % W_MAX)
        w = wn
    return dict(q, giri=20, verdetto="NON STABILE nella scatola")


def parte_C():
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    import _screening_forme_s3 as SF
    print("### PARTE C -- I SOLITONI LARGHI (la scatola in archi: R = 10 w, dr = w/%d; S %s; N %s; eps 0, ramo a curvatura -)" % (PUNTI_PER_W, S_C, N_C))
    vero = SF.pezzi_di

    def log_puro(nome):
        def pz(rho, lam):
            rho = np.asarray(rho, dtype=float)
            al = np.zeros_like(rho)
            v = rho > 0.0
            al[v] = np.log(rho[v] / np.asarray(lam, dtype=float)[v]) + 1.0
            return al, np.zeros_like(rho)
        return pz
    SF.pezzi_di = log_puro
    try:
        q = largo("LOG", -0.8, 0.9, 10.0)
    finally:
        SF.pezzi_di = vero
    ge = GC.gausson(-0.8, 0.9, 10.0, LAM0)
    esito("DEVE PASSARE: la gaussiana esatta col risolutore nuovo (c -0.8, s 0.9, N 10), errore < 1e-6", q["verdetto"] == "LEGATO" and abs(q["mu"] - ge) < 1e-6 * abs(ge),
          "mu %.10f contro %.10f (%.1e); larghezza %.5f contro %.5f" % (q["mu"], ge, abs(q["mu"] - ge) / abs(ge), q["larghezza"], np.sqrt(0.8 / 0.9)))
    tab = []
    for s in S_C:
        g = [x for x in GC.gruppi(F.rami(s, 0.0)[0]) if x["segno"] < 0][0]
        c = GC.c_di(g)
        for forma in FORME:
            for N in N_C:
                q = largo(forma, c, s, N)
                rec = {"tipo": "solitone_largo", "forma": forma, "s": s, "N": N, "c": c, "sigma": float(np.sqrt(abs(c) / s)), **q}
                tab.append(rec)
                scrivi(rec)
                print("  %-2s s %-4g N %-7g: %-28s larghezza %9.3f archi  mu %+.4f  x_centro %.3g  (%d giri, R %.1f)"
                      % (forma, s, N, q["verdetto"][:28], q["larghezza"], q["mu"], q["x_centro"], q["giri"], q["R"]))
                sys.stdout.flush()
    print("### IL PRIMO s CON UNO STATO LEGATO LARGO >= %g ARCHI, e le norme" % LARGHEZZA_MIN)
    primi = {}
    for forma in FORME:
        buoni = [r for r in tab if r["forma"] == forma and r["verdetto"] == "LEGATO" and r["larghezza"] >= LARGHEZZA_MIN]
        if buoni:
            s1 = min(r["s"] for r in buoni)
            nn = sorted(r["N"] for r in buoni if r["s"] == s1)
            primi[forma] = {"s": s1, "N": nn}
        else:
            primi[forma] = None
        scrivi({"tipo": "primo_s", "forma": forma, "primo": primi[forma]})
        print("  %-2s: %s" % (forma, "nessuno" if primi[forma] is None else "s %g, N %s" % (primi[forma]["s"], primi[forma]["N"])))
    return tab, primi


def main(argv):
    del argv
    import _forza_da_cs as F
    import _presidio
    import _segno_gravita as SG
    import _universalita_massa as UM
    import _zero_simmetrico as ZS
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 100)
    print("I MODI A k = pi E I SOLITONI LARGHI: dove sta la fisica a bassa energia, e i solitoni larghi")
    print("=" * 100)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_massa_vicino_al_cono.py", "csv/_universalita_massa.py", "csv/_forza_da_cs.py", "csv/_stabilita_lineare.py",
                                     "csv/_gravita_collettiva.py", "csv/_scala_e_zero.py", "csv/_zero_simmetrico.py", "csv/_segno_gravita.py", "csv/_modi_pi_e_solitoni.py",
                                     "doc/referti_l2/segno_gravita.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); le convenzioni SOLO in memoria; i blob nel repo: %s"
          % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: S_A %s; EPS %s; L %d; H %g; SALTO_NULLO %g; S0_B %s; ETA_B %s; LX_B %d; FORME %s; S_C %s; N_C %s; LAM0 %g; LARGHEZZA_MIN %g; W_MAX %g; PUNTI_PER_W %d"
          % (S_A, EPS, L, H, SALTO_NULLO, S0_B, ETA_B, LX_B, FORME, S_C, N_C, LAM0, LARGHEZZA_MIN, W_MAX, PUNTI_PER_W))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    warnings.simplefilter("ignore")
    # ---------------------------------------------------------------- il controllo a k = 0
    assert F.committata(J_SG), "il jsonl di e31366ec non e' committato e pulito"
    rif = {(r["eps"], r["s0"], r["ramo"]): r["H_su_RG"] for r in (json.loads(l) for l in io.open(J_SG, encoding="utf-8")) if r.get("tipo") == "lambda" and r["eta"] == 1e-3}
    import _gravita_collettiva as GC
    peg, n = 0.0, 0
    for eps in EPS:
        for s0 in (0.3, 0.5):
            for g in GC.gruppi(F.rami(s0, eps)[0]):
                v = rif.get((eps, s0, ZS.nome_curv(g)))
                if v is None:
                    continue
                for lam in ("0.0", "0.5"):
                    x = SG.h_su_rg(float(lam), eps, s0, 1e-3, g)[0]
                    n += 1
                    peg = max(peg, abs(x - v[lam]) / max(abs(v[lam]), 1e-300) if v[lam] else abs(x))
    esito("DEVE PASSARE: a k = 0, a_H/a_RG di s0 0.3 e 0.5, lambda 0 e 1/2 = e31366ec entro 1e-9 (%d valori)" % n, n > 0 and peg < 1e-9, "il peggiore %.2e" % peg)
    # ---------------------------------------------------------------- A
    righe, minimi = parte_A()
    m3 = [m for m in minimi if m["eps"] == 0.0 and m["s"] == 0.3]
    esito("DEVE FALLIRE: <<il salto minimo e' a k = 0 a s 0.3>> (eps 0; per la chiave giusta: il k del minimo stampato)",
          len(m3) > 0 and not all(m["m"] == 0 for m in m3), "; ".join("%s: k = (%.3f, %.3f) pi, distanza %.2e" % (m["ramo"], m["k_min"][0], m["k_min"][1], m["distanza"]) for m in m3))
    r3 = [r for r in righe if r["s"] == 0.3 and r["simm"]]
    esito("PUO' FALLIRE: parte A, E0 M > 0 su almeno un ramo a k* a s 0.3 (simmetrica)", any(r["simm"]["E0M_positivo"] for r in r3),
          "; ".join("eps %g %s a %s: E0 M %s" % (r["eps"], r["ramo"], r["k_star"], "+" if r["simm"]["E0M_positivo"] else "-") for r in r3))
    # ---------------------------------------------------------------- B
    rb = parte_B(righe)
    zz = [r for r in rb if r["tipo"] == "zero_k"]
    esito("DEVE PASSARE: eta 0 nella parte B, |a| sotto il rumore del fit (%d corse)" % len(zz), len(zz) > 0 and all(r["nullo"] for r in zz),
          "; ".join("%s eps %g s0 %g %s: a %s sigma %s" % (r["convenzione"], r["eps"], r["s0"], r["ramo"], f_(r["a"], "%+.1e"), f_(r["sigma_a"], "%.1e")) for r in zz if not r["nullo"]))
    print("  (eps 0.5 a s0 0.1 dopo la correzione del ramo: gia' provato in 6c36b19a, 2 su 2)")
    # ---------------------------------------------------------------- C
    tab, primi = parte_C()
    esito("PUO' FALLIRE: parte C, almeno una forma con uno stato legato largo >= 4 archi a s <= 0.5", any(p is not None and p["s"] <= 0.5 for p in primi.values()),
          "; ".join("%s: %s" % (f, "nessuno" if p is None else "s %g" % p["s"]) for f, p in primi.items()))
    print("### LA PARTE C.3 (la dinamica dei solitoni larghi): in uno strumento a se', ai punti qui sopra")
    print("=" * 100)
    print("I MODI A k = pi E I SOLITONI LARGHI: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
