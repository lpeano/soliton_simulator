r"""**LA SCALA E LO ZERO: il principio di equivalenza a `s` piccolo, il solitone con `c` proporzionale a `s`, la relazione di Einstein nelle tre convenzioni** *(spettri a `cs` uniforme e risolutore radiale, in memoria)*.

> ### ⛔ **Il task history e' `2026-10-23_scala_e_zero.md`** *(il metodo, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`, l'impronta, la convenzione dei pezzi e il
> nucleo intatti.** ### **Importati, non copiati:** `_massa_vicino_al_cono` *(`matrice`, `rami_seguiti`)*, `_forza_da_cs` *(`rami`, `spazio_del_ramo`, `avvolgi`, `committata`)*,
> `_gravita_collettiva` *(`dproprio`, `convenzione_alternativa`, `solitone`, `gruppi`, `c_di`)*, `_stabilita_lineare` *(`passo`, avvolto in memoria per il controllo un-pezzo-solo)*.

### **PARTE A:** ### **la fase a `k = 0` SEGUITA CON CONTINUITA' da `s` piccolo** *(cammino fine in `s`, vettori propri per sovrapposizione)*, ### **`omega''(0)` dalle fasi esatte
*(Richardson)*, `v`, `E0`, `M`, `D`; `H_eff = i log U / s` a `k = 0` e `pi/8`, `delta(s)`; `Vi(s)` fra specie; gli esponenti.** ### **PARTE B:** ### **il solitone con `c = c0 s`, e
accanto il `D` di `c4efc937`.** ### **PARTE C:** ### **`Q = omega(0) omega''(0)/v^2` nelle tre convenzioni.**

Gira con:  python csv/_scala_e_zero.py > doc/referti_l2/scala_e_zero.txt
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

S_LISTA = (0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99)   # 0.95 aggiunto: lo chiede il controllo (iii) del mandato
EPS_LISTA = (0.0, 0.25, 0.5, 1.0)
LATI = (32, 64)
L_FINE = 16                    # il blocco a k = 0 e a k = pi/8 (m = 1) e' lo stesso al bit a ogni lato (verificato)
PASSO_FINE = 0.005
H = 1e-3
S_RIF = 0.02
FIT_MAX = 0.3
SALTO_MAX = 0.2
TOLL_W = 1e-9
TOLL_ZERO = 1e-6
SB = (0.85, 0.9, 0.95, 0.99, 1.0)
FORME = ("S1", "S3", "S4")
N_LISTA = (1.0, 10.0, 100.0)
LAM0 = 4.0
JSONL = os.path.join(RADICE, "doc", "referti_l2", "scala_e_zero.jsonl")
J_GC = os.path.join(RADICE, "doc", "referti_l2", "gravita_collettiva.jsonl")
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


def f_(x, fmt="%+.4e"):
    return "--" if x is None else fmt % x


# =====================================================================================
#   I BLOCCHI, il controllo un-pezzo-solo, il cammino fine
# =====================================================================================
_PEZZI = [None]


@contextlib.contextmanager
def solo_pezzi(ids):
    """### **Un solo pezzo acceso**: `_stabilita_lineare.passo` avvolto IN MEMORIA, ### **`salta` = tutti gli id dell'ordine tranne `ids`** *(`matrice()` resta quella)*."""
    import _stabilita_lineare as SL
    import composizione as CM
    vero = SL.passo
    via = tuple(sorted({idl for idl, _f, _t in CM.ORDINE} - set(ids)))

    def passo(st, mot, par, acceso, salta, lc):
        return vero(st, mot, par, acceso, via, lc)
    SL.passo = passo
    try:
        yield
    finally:
        SL.passo = vero


def blocchi(s, eps, L=L_FINE):
    import _massa_vicino_al_cono as MV
    A = MV.matrice(L, 1.0, eps, s)
    return A[0, 0, :8, :8].copy(), A[L // 16, 0, :8, :8].copy()


def punti_fini():
    p = set(np.round(np.arange(S_RIF, 0.99 + 1e-9, PASSO_FINE), 10))
    for s in S_LISTA:
        p |= {round(s, 10), round(s * (1.0 - H), 12), round(s * (1.0 + H), 12)}
    return sorted(p)


def cammino(eps):
    """### Le fasi a `k = 0` e `pi/8` lungo `s`: ### **principali al primo punto, poi i vettori per sovrapposizione e le fasi srotolate.**"""
    from scipy.optimize import linear_sum_assignment
    out = {0: {}, 1: {}}
    salto = 0.0
    prec = {0: None, 1: None}
    for s in punti_fini():
        bb = blocchi(s, eps)
        for q in (0, 1):
            lam, V = np.linalg.eig(bb[q])
            w = -np.angle(lam)
            if prec[q] is not None:
                Vp, wp = prec[q]
                ov = np.abs(Vp.conj().T @ V)
                r, c = linear_sum_assignment(-ov)
                o = np.empty(8, dtype=int)
                o[r] = c
                V, w, lam = V[:, o], w[o], lam[o]
                d = np.array([float((w[i] - wp[i] + np.pi) % (2.0 * np.pi) - np.pi) for i in range(8)])
                salto = max(salto, float(np.max(np.abs(d))))
                w = wp + d
            out[q][s] = {"w": w.copy(), "V": V.copy(), "B": bb[q]}
            prec[q] = (V, w)
    return out, salto


def a_(Cq, s):
    """### Il punto del cammino fine a `s` *(la chiave piu' vicina, entro `1e-12`)*."""
    k = min(Cq, key=lambda x: abs(x - s))
    assert abs(k - s) < 1e-12, "il punto %r non e' sul cammino fine" % s
    return Cq[k]


def H_eff(V, w, s):
    return (V @ np.diag(w) @ np.linalg.inv(V)) / s


def delta_di(C, q, versione):
    """### `delta(s)` sui punti della griglia: `||H(s) - H(0.02)|| / ||H(0.02)||`."""
    def Hs(s):
        d = a_(C[q], s)
        if versione == "continua":
            return H_eff(d["V"], d["w"], s)
        lam, V = np.linalg.eig(d["B"])
        return H_eff(V, -np.angle(lam), s)
    H0 = Hs(S_RIF)
    n0 = np.linalg.norm(H0)
    return {s: float(np.linalg.norm(Hs(s) - H0) / n0) for s in S_LISTA}


def esponente(dd, contro_s=False):
    pts = [(s, v) for s, v in dd.items() if S_RIF < s <= FIT_MAX + 1e-12 and v and v > 0]
    if len(pts) < 2:
        return None
    X = np.log([s if contro_s else s - S_RIF for s, _ in pts])
    return float(np.polyfit(X, np.log([v for _, v in pts]), 1)[0])


# =====================================================================================
#   PARTE A -- I RAMI ALLA GRIGLIA
# =====================================================================================
def rami_a(L, s, eps):
    import _forza_da_cs as F
    import _massa_vicino_al_cono as MV
    vero = F.L_SPETTRO
    F.L_SPETTRO = L
    try:
        lista, BB, _ = F.rami(s, eps)
    finally:
        F.L_SPETTRO = vero
    A = MV.matrice(L, 1.0, eps, s)
    ph = MV.rami_seguiti(A, L)
    return lista, ph, A


def curvatura(ph, b, L):
    k1 = 2.0 * np.pi / L
    d1, d2 = ph[1, b] - ph[0, b], ph[2, b] - ph[0, b]
    return float(2.0 * (16.0 * d1 - d2) / (12.0 * k1 * k1))


def livelli(C, s, w0):
    """### I livelli del cammino fine con fase principale `w0` a `s`, e le loro fasi continue."""
    import _forza_da_cs as F
    w = a_(C[0], s)["w"]
    return [i for i in range(8) if abs(F.avvolgi(w[i] - w0)) <= TOLL_W]


def parte_A(cammini):
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    print("### PARTE A -- LA SCALA: i rami (lati %s), omega(0) continua, omega'' dalle fasi esatte, E0, M, D" % (LATI,))
    righe = []
    serv = 0.0
    for eps in EPS_LISTA:
        C = cammini[eps]
        for L in LATI:
            for s in S_LISTA:
                lista, ph, A = rami_a(L, s, eps)
                b0, b1 = blocchi(s, eps)
                serv = max(serv, float(np.abs(A[0, 0, :8, :8] - b0).max()), float(np.abs(A[L // 16, 0, :8, :8] - b1).max()))
                for g in GC.gruppi(lista):
                    b = [r for r in lista if abs(r["omega0"] - g["omega0"]) <= GC.TOLL_DISTINTI and r["omega1"] in g["omega1"]][0]["ramo"]
                    w2 = curvatura(ph, b, L)
                    lv = livelli(C, s, g["omega0"])
                    wc = sorted({round(float(a_(C[0], s)["w"][i]), 9) for i in lv})
                    amb = len(wc) != 1
                    lvl = min(lv) if lv else None
                    if lvl is not None:
                        wcs = [float(a_(C[0], x)["w"][lvl]) for x in (s * (1 - H), s, s * (1 + H))]
                        D = GC.dproprio(wcs[0], wcs[1], wcs[2], s * (1 - H), s, s * (1 + H))
                        w_c = wcs[1]
                    else:
                        D = w_c = None
                    rec = {"tipo": "ramo", "eps": eps, "lato": L, "s": s, "ramo": g["nome"], "copie": g["copie"], "Dt": g["Dt"], "v": g["v"],
                           "segno_fit": g["segno"], "omega0_principale": g["omega0"], "omega0_continua": w_c, "ambiguo": amb, "continue_candidate": wc,
                           "livello": lvl, "omega2": w2, "E0": None if w_c is None else w_c / s, "M": w2 / s, "D": D}
                    righe.append(rec)
                    scrivi(rec)
                    print("  eps %-4g lato %d s %-4g %-24s: w0 princ %+.6f cont %s%s | w'' %+.5f (fit: %+.5f) v %.5f | E0 %s M %+.4f D %s"
                          % (eps, L, s, g["nome"], g["omega0"], f_(w_c, "%+.6f"), " AMBIGUO %s" % wc if amb else "", w2, g["segno"] * g["v"] ** 2 / g["Dt"],
                             g["v"], f_(rec["E0"], "%+.5f"), rec["M"], f_(D, "%+.3e")))
                    sys.stdout.flush()
    return righe, serv


# =====================================================================================
#   PARTE B -- IL SOLITONE CON c PROPORZIONALE A s
# =====================================================================================
def parte_B():
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    lista = rami_a(64, 0.9, 0.0)[0]
    basso = [g for g in GC.gruppi(lista) if abs(g["omega0"]) <= TOLL_W][0]
    c0 = GC.c_di(basso) / 0.9
    print("### PARTE B -- IL SOLITONE CON c = c0 s, c0 = c(0.9)/0.9 = %+.6f (ramo basso, eps 0, lato 64); omega0 = 0" % c0)
    assert F.committata(J_GC), "il jsonl di c4efc937 non e' committato e pulito"
    gc = [json.loads(l) for l in io.open(J_GC, encoding="utf-8")]
    mis = {(r["forma"], r["N"], r["s"]): r for r in gc if r["tipo"] == "livello2" and r["eps"] == 0.0 and abs(r["omega_ramo0"]) <= TOLL_W}
    out = []
    for forma in FORME:
        for N in N_LISTA:
            for s in SB:
                sm, sp = s * (1.0 - H), (None if s >= 1.0 else s * (1.0 + H))
                q0, qm = GC.solitone(forma, c0 * s, s, N, LAM0), GC.solitone(forma, c0 * sm, sm, N, LAM0)
                qp = GC.solitone(forma, c0 * sp, sp, N, LAM0) if sp is not None else None
                ok = all(q is None or (q["stato"] == "CONVERGE" and q["esiste"] == "LEGATO") for q in (q0, qm, qp))
                D = GC.dproprio(qm["mu"], q0["mu"], qp["mu"] if qp else None, sm, s, sp) if ok else None
                m = mis.get((forma, N, s))
                rec = {"tipo": "solitone_c_proporzionale", "forma": forma, "N": N, "s": s, "D": D, "legato": ok, "mu": q0["mu"], "larghezza": q0["larghezza"],
                       "D_c_misurato_c4efc937": None if m is None else m["D"], "esiste_c4efc937": None if m is None else m["esiste"]}
                out.append(rec)
                scrivi(rec)
                print("  %-2s N %-5g s %-4g: %s mu %+.6f larghezza %.3f | D (c = c0 s) %s | D (c misurato, c4efc937) %s"
                      % (forma, N, s, "LEGATO" if ok else q0["esiste"], q0["mu"], q0["larghezza"], f_(D, "%+.3e"),
                         "--" if m is None else "%s (%s)" % (f_(m["D"], "%+.4f"), m["esiste"])))
                sys.stdout.flush()
    return out


# =====================================================================================
#   PARTE C -- LA RELAZIONE DI EINSTEIN
# =====================================================================================
def parte_C(righe):
    import _forza_da_cs as F
    import _gravita_collettiva as GC
    print("### PARTE C -- Q = omega(0) omega''(0) / v^2 nelle tre convenzioni (i oggi, ii exp(-i theta P), iii lo zero a meta' di una coppia)")
    out = []
    serv = 0.0
    for eps in EPS_LISTA:
        for L in LATI:
            for s in S_LISTA:
                rr = [r for r in righe if r["eps"] == eps and r["lato"] == L and r["s"] == s]
                if L == 64:
                    with GC.convenzione_alternativa():
                        vero = F.L_SPETTRO
                        F.L_SPETTRO = L
                        try:
                            alt = F.rami(s, eps)[0]
                        finally:
                            F.L_SPETTRO = vero
                for r in rr:
                    if L == 64 and alt:
                        a = min(alt, key=lambda x: abs(F.avvolgi(x["omega0"] - r["omega0_principale"] - 2.0 * np.pi * s)) + abs(x["Dt"] - r["Dt"]) / r["Dt"])
                        serv = max(serv, abs(F.avvolgi(a["omega0"] - r["omega0_principale"] - 2.0 * np.pi * s)))
                    coppia = [x for x in rr if x is not r and abs(x["Dt"] - r["Dt"]) <= 1e-6 * r["Dt"] and np.sign(x["omega2"]) == -np.sign(r["omega2"])]
                    k = r["omega2"] / r["v"] ** 2
                    wc = r["omega0_continua"]
                    q = {"i_principale": r["omega0_principale"] * k, "i_continua": None if wc is None else wc * k,
                         "ii_principale": F.avvolgi(r["omega0_principale"] + 2.0 * np.pi * s) * k,
                         "ii_continua": None if wc is None else (wc + 2.0 * np.pi * s) * k}
                    if len(coppia) == 1:
                        x = coppia[0]
                        mezzo = r["omega0_principale"] + F.avvolgi(x["omega0_principale"] - r["omega0_principale"]) / 2.0
                        q["iii"] = F.avvolgi(r["omega0_principale"] - mezzo) * k
                        q["coppia"] = x["ramo"]
                    else:
                        q["iii"] = None
                        q["coppia"] = "NESSUNA COPPIA" if not coppia else "PIU' DI UNA (%d)" % len(coppia)
                    rec = dict({"tipo": "einstein", "eps": eps, "lato": L, "s": s, "ramo": r["ramo"]}, **q)
                    out.append(rec)
                    scrivi(rec)
                    print("  eps %-4g lato %d s %-4g %-24s: Q (i) princ %s cont %s | (ii) princ %s cont %s | (iii) %s  [%s]"
                          % (eps, L, s, r["ramo"], f_(q["i_principale"], "%+.4f"), f_(q["i_continua"], "%+.4f"), f_(q["ii_principale"], "%+.4f"),
                             f_(q["ii_continua"], "%+.4f"), f_(q["iii"], "%+.4f"), q["coppia"]))
    return out, serv


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _universalita_massa as UM
    import composizione as CM
    print("=" * 100)
    print("LA SCALA E LO ZERO: il principio di equivalenza a s piccolo, il solitone con c proporzionale a s, la relazione di Einstein nelle tre convenzioni")
    print("=" * 100)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_massa_vicino_al_cono.py", "csv/_universalita_massa.py", "csv/_forza_da_cs.py",
                                     "csv/_stabilita_lineare.py", "csv/_screening_forme_s3.py", "csv/_gravita_collettiva.py", "csv/_scala_e_zero.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); dtau 1, cs = s uniforme in memoria, lambda_c None; i blob nel repo: %s"
          % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: S %s; EPS %s; LATI %s; L_FINE %d; PASSO_FINE %g; H %g; S_RIF %g; FIT_MAX %g; SALTO_MAX %g; TOLL_W %g; TOLL_ZERO %g; SB %s; FORME %s; N %s; LAM0 %g"
          % (S_LISTA, EPS_LISTA, LATI, L_FINE, PASSO_FINE, H, S_RIF, FIT_MAX, SALTO_MAX, TOLL_W, TOLL_ZERO, SB, FORME, N_LISTA, LAM0))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    warnings.simplefilter("ignore")
    # ---------------------------------------------------------------- il cammino fine e delta
    print("### IL CAMMINO FINE (lato %d, passo %g, %d punti) E delta(s)" % (L_FINE, PASSO_FINE, len(punti_fini())))
    cammini, salti, dl = {}, {}, {}
    for eps in EPS_LISTA:
        cammini[eps], salti[eps] = cammino(eps)
        for q, kn in ((0, "k=0"), (1, "k=pi/8")):
            for ver in ("principale", "continua"):
                dd = delta_di(cammini[eps], q, ver)
                dl[(eps, kn, ver)] = dd
                p, ps = esponente(dd), esponente(dd, True)
                scrivi({"tipo": "delta", "eps": eps, "k": kn, "versione": ver, "delta": {str(s): v for s, v in dd.items()}, "esponente": p, "esponente_contro_s": ps})
                print("  eps %-4g %-6s %-10s: delta %s | esponente (s - 0.02) %s, (s) %s"
                      % (eps, kn, ver, " ".join("%g:%.2e" % (s, v) for s, v in dd.items()), f_(p, "%.3f"), f_(ps, "%.3f")))
        sys.stdout.flush()
    print("### IL CONTROLLO UN-PEZZO-SOLO")
    peg = 0.0
    for ids in (("CAMM-GROVER",), ("CAMM-SPOSTAMENTO",)):
        with solo_pezzi(ids):
            C1, _ = {0: {}, 1: {}}, None
            for s in S_LISTA:
                bb = blocchi(s, 0.5)
                C1[0][s], C1[1][s] = {"B": bb[0]}, {"B": bb[1]}
            for q in (0, 1):
                dd = delta_di(C1, q, "principale")
                peg = max(peg, max(dd.values()))
                print("  solo %s, %s: delta %s" % (ids[0], "k=0" if q == 0 else "k=pi/8", " ".join("%g:%.1e" % (s, v) for s, v in dd.items())))
    esito("DEVE PASSARE: un pezzo solo (Grover o spostamento), delta(s) < 1e-12 a ogni s, k = 0 e pi/8", peg < 1e-12, "il peggiore %.2e" % peg)
    d99 = dl[(0.5, "k=pi/8", "principale")][0.99]
    esito("DEVE FALLIRE: <<delta(0.99) < 1e-6>> sul passo intero (k = pi/8, eps 0.5, principale), per la chiave giusta (delta finito)",
          np.isfinite(d99) and not d99 < 1e-6, "delta(0.99) = %.4e" % d99)
    pp = {eps: esponente(dl[(eps, "k=pi/8", "continua")]) for eps in EPS_LISTA}
    esito("PUO' FALLIRE: l'esponente di delta su s <= 0.3 (passo intero, k = pi/8, continua) fra 0.8 e 1.2, ogni eps",
          all(p is not None and 0.8 <= p <= 1.2 for p in pp.values()), "; ".join("eps %g: %s" % (e, f_(p, "%.3f")) for e, p in pp.items()))
    esito("DI SERVIZIO: nessun salto di fase oltre %g sul cammino fine" % SALTO_MAX, max(salti.values()) < SALTO_MAX,
          "il peggiore %.3e" % max(salti.values()))
    # ---------------------------------------------------------------- A: i rami
    righe, serv = parte_A(cammini)
    esito("DI SERVIZIO: i blocchi a k = 0 e pi/8 uguali ai lati 16, 32, 64 entro 1e-12", serv < 1e-12, "il peggiore %.2e" % serv)
    # ---------------------------------------------------------------- A: l'universalita'
    print("### L'UNIVERSALITA': Vi(s) per E0 e per M, fra le specie seguite da s 0.02 (lato 64)")
    spec = {}
    for r in righe:
        if r["lato"] == 64 and r["livello"] is not None:
            spec.setdefault((r["eps"], r["livello"]), {})[r["s"]] = r
    spec = {k: v for k, v in spec.items() if S_RIF in v}
    chiavi = sorted(spec)
    for a in range(len(chiavi)):
        for b in range(a + 1, len(chiavi)):
            i, j = spec[chiavi[a]], spec[chiavi[b]]
            for grand in ("E0", "M"):
                if i[S_RIF][grand] is None or j[S_RIF][grand] is None or abs(j[S_RIF][grand]) <= TOLL_ZERO:
                    continue
                R0 = i[S_RIF][grand] / j[S_RIF][grand]
                if abs(R0) <= TOLL_ZERO:
                    continue
                vv = {s: abs(i[s][grand] / j[s][grand] - R0) / abs(R0) for s in S_LISTA if s in i and s in j and i[s][grand] is not None and abs(j[s][grand] or 0) > TOLL_ZERO}
                p = esponente(vv)
                scrivi({"tipo": "universalita", "i": list(chiavi[a]), "j": list(chiavi[b]), "grandezza": grand, "R0": R0, "Vi": {str(s): v for s, v in vv.items()}, "esponente": p})
                print("  (eps %g, liv %d) / (eps %g, liv %d) %-2s: R0 %+.5f | Vi %s | esponente %s"
                      % (chiavi[a][0], chiavi[a][1], chiavi[b][0], chiavi[b][1], grand, R0, " ".join("%g:%.2e" % (s, v) for s, v in vv.items()), f_(p, "%.3f")))
    # ---------------------------------------------------------------- B
    rb = parte_B()
    leg = [r for r in rb if r["D"] is not None]
    peg = max((abs(r["D"]) for r in leg), default=float("inf"))
    esito("DEVE PASSARE: parte B, c = c0 s, |D| < 1e-6 dove lo stato e' legato (%d punti)" % len(leg), len(leg) > 0 and peg < 1e-6, "il peggiore %.2e" % peg)
    # ---------------------------------------------------------------- C
    rc, serv = parte_C(righe)
    esito("DI SERVIZIO: l'alternativa (convenzione_alternativa) ha omega(0) + 2 pi s, entro 1e-12", serv < 1e-12, "il peggiore %.2e" % serv)
    q3 = [r for r in rc if r["eps"] == 0.0 and r["s"] in (0.9, 0.95, 0.99)]
    vals = [r["iii"] for r in q3]
    esito("PUO' FALLIRE: (iii) |Q - 1| < 0.2 a s 0.9, 0.95, 0.99, eps 0 (%d righe)" % len(q3),
          len(vals) > 0 and all(v is not None and abs(v - 1.0) < 0.2 for v in vals), "; ".join("s %g lato %d %s: %s" % (r["s"], r["lato"], r["ramo"], f_(r["iii"], "%+.4f")) for r in q3))
    print("=" * 100)
    print("LA SCALA E LO ZERO: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
