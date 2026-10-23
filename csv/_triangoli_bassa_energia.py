r"""**I TRIANGOLI, PRIMO GRADINO: gli spettri, dove sta la fisica di bassa energia, la gravita' di Hamilton** *(solo spettri, in memoria; [[DECISIONE-SOLO-TRIANGOLI]])*.

> ### ⛔ **Il task history e' `2026-10-23_triangoli_bassa_energia.md`** *(la geometria, il metodo, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`, l'impronta e il nucleo intatti.**
> ### **Importati, non copiati:** `_triangoli`, `_zero_simmetrico`, `_scala_e_zero`, `_modi_pi_e_solitoni.fase_seguita`, `_gravita_collettiva.dproprio`, `_moneta_massa.fit_massa`,
> `_universalita_massa.blob`. ### **Gli strumenti del quadrato che hanno l'`8 x 8` o il lato `64` scritti dentro** *(`rami_seguiti`, `cammino`, `a_k`)* ### **qui hanno la loro versione per il
> blocco `12 x 12` dei triangoli.**

Gira con:  python csv/_triangoli_bassa_energia.py > doc/referti_l2/triangoli_bassa_energia.txt
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

L = 48
LF = 6
NB = 12
S_LISTA = (0.05, 0.1, 0.3, 0.5, 0.9)
EPS = (0.0, 0.25, 0.5, 1.0)
PUNTI = {"Gamma": (0, 0), "K": (16, 16), "K'": (32, 32), "M1": (24, 0), "M2": (0, 24), "M3": (24, 24)}
LINEE = {"diag": [(i, i) for i in range(33)], "x": [(i, 0) for i in range(25)], "y": [(0, i) for i in range(25)]}
J = np.array([[1.0, 0.0], [-0.5, np.sqrt(3.0) / 2.0]])
DISPERSIVA = 1e-3
TOLL_GRUPPO = 1e-6
TOLL_ISOTROPA = 1e-3            # numerica: lo stencil di Richardson sbaglia di O(k1^4) (annotazione 1)
PIATTA = 1e-6
H = 1e-3
PASSO_S = 0.005
S_RIF = 0.02
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_bassa_energia.jsonl")
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


def av(x):
    return float((x + np.pi) % (2.0 * np.pi) - np.pi)


def conv(nome):
    import _zero_simmetrico as ZS
    return ZS.convenzione_simmetrica() if nome == "simm" else contextlib.nullcontext()


def matrice(eps, s, lato, nome="simm"):
    """### `A(k)` dei triangoli *(`_triangoli.matrice_tick`, `dtau = s`)*, `eps` in `_triangoli.EPS_MONETA` in memoria, la convenzione in memoria."""
    import _triangoli as T
    vero = T.EPS_MONETA
    T.EPS_MONETA = eps
    try:
        with conv(nome):
            return T.matrice_tick(T.TRIANGOLI, lato, s)
    finally:
        T.EPS_MONETA = vero


@contextlib.contextmanager
def un_pezzo(idl):
    """### **Un pezzo solo acceso:** `_triangoli.camminata` avvolta in memoria, ### **`salta` = tutti gli id dell'ordine tranne `idl`.**"""
    import _triangoli as T
    import composizione as CM
    import tick as TK
    vero = T.camminata
    via = tuple(sorted({i for i, _f, _t in CM.ORDINE} - {idl}))
    T.camminata = lambda st, mot, par: TK.percorri_tick(st, mot, par, via, None, len(CM.ORDINE))
    try:
        yield
    finally:
        T.camminata = vero


def segui(A, cammino):
    """### Le `12` bande della materia lungo `cammino`, seguite per sovrapposizione dei vettori propri, srotolate."""
    from scipy.optimize import linear_sum_assignment
    lam, V = np.linalg.eig(A[cammino[0][0], cammino[0][1], :NB, :NB])
    ph, vv = [-np.angle(lam)], [V]
    for (a, b) in cammino[1:]:
        l2, V2 = np.linalg.eig(A[a % L, b % L, :NB, :NB])
        ov = np.abs(V.conj().T @ V2)
        r, c = linear_sum_assignment(-ov)
        o = np.empty(NB, dtype=int)
        o[r] = c
        l2, V2 = l2[o], V2[:, o]
        ph.append(-np.angle(l2))
        vv.append(V2)
        V = V2
    return np.unwrap(np.array(ph), axis=0), vv


def gruppi_dispersivi(ph):
    """### Le bande che DISPERDONO lungo il cammino, raggruppate per fase a `Gamma`."""
    disp = [b for b in range(NB) if float(np.max(ph[:, b]) - np.min(ph[:, b])) > DISPERSIVA]
    out = []
    for b in sorted(disp, key=lambda b: ph[0, b]):
        for g in out:
            if abs(av(ph[0, b] - ph[0, g[0]])) <= TOLL_GRUPPO:
                g.append(b)
                break
        else:
            out.append([b])
    return out


def curvatura(A, m1, m2, w0, Q):
    """### Il tensore della curvatura in `theta` *(dalle fasi esatte ai vicini, il ramo seguito con `_modi_pi_e_solitoni.fase_seguita`)*, in cartesiano, e `v` dal fit lungo `theta_1`."""
    import _modi_pi_e_solitoni as MP
    import _moneta_massa as MM
    k1 = 2.0 * np.pi / L

    def ph(d1, d2):
        return w0 + av(MP.fase_seguita(A[(m1 + d1) % L, (m2 + d2) % L, :NB, :NB], Q)[0] - w0)
    p = {d: ph(*d) for d in ((1, 0), (-1, 0), (2, 0), (-2, 0), (0, 1), (0, -1), (0, 2), (0, -2), (1, 1), (-1, -1), (2, 2), (-2, -2))}

    def rich(a, b, c, d_):
        return (-p[d_] + 16 * p[a] - 30 * w0 + 16 * p[b] - p[c]) / (12 * k1 * k1)
    h11 = rich((1, 0), (-1, 0), (-2, 0), (2, 0))
    h22 = rich((0, 1), (0, -1), (0, -2), (0, 2))
    hdd = rich((1, 1), (-1, -1), (-2, -2), (2, 2))          # ### la derivata seconda lungo (1, 1): h11 + 2 h12 + h22, al quarto ordine
    h12 = 0.5 * (hdd - h11 - h22)
    Ht = np.array([[h11, h12], [h12, h22]])
    Hk = J.T @ Ht @ J
    ev = np.linalg.eigvalsh(Hk)
    vg = ((p[(1, 0)] - p[(-1, 0)]) / (2 * k1), (p[(0, 1)] - p[(0, -1)]) / (2 * k1))
    qq, yv, Qc, wc = [0.0], [0.0], Q, w0
    for m in range(1, 7):
        wm, Vm = MP.fase_seguita(A[(m1 + m) % L, m2, :NB, :NB], Qc)
        wc = wc + av(wm - wc)
        qq.append(m * k1)
        yv.append(wc - w0)
        Qc = Vm
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        Df, vf, sc = MM.fit_massa(np.array(qq), np.array(yv))
    return {"h11": float(h11), "h22": float(h22), "h12": float(h12), "cart_autovalori": [float(x) for x in ev],
            "anisotropia": float(abs(ev[0] - ev[1]) / max(abs(ev[0]), abs(ev[1]), 1e-300)),
            "isotropa": bool(abs(ev[0] - ev[1]) <= TOLL_ISOTROPA * max(abs(ev[0]), abs(ev[1]), 1e-300)),
            "piatta": bool(max(abs(ev[0]), abs(ev[1])) < PIATTA), "v_g": [float(vg[0]), float(vg[1])], "v": float(vf), "Dt_fit": float(Df),
            "scarto_fit": float(sc)}


def continua(eps, s, punto, V0, nome="oggi"):
    """### La fase del ramo a `punto` seguita in `s` **per sovrapposizione del vettore**: ### **scendendo fino a `S_RIF`** *(dove la fase principale e' piccola: e' lo zero continuo)* ### **e
    a `s (1 +- h)`.** ### Il blocco al lato `LF` *(lo stesso al bit che al lato `L` ai punti speciali)*."""
    m1, m2 = punto[0] * LF // L, punto[1] * LF // L

    def blocco(x):
        return matrice(eps, x, LF, nome)[m1, m2, :NB, :NB]

    def passo(B, V):
        lam, VV = np.linalg.eig(B)
        j = int(np.argmax(np.abs(VV.conj().T @ V)[:, 0]))
        return float(-np.angle(lam[j])), VV[:, [j]]
    lam, VV = np.linalg.eig(blocco(s))
    j = int(np.argmax(np.abs(VV.conj().T @ V0)[:, 0]))
    w_s, V_s = float(-np.angle(lam[j])), VV[:, [j]]
    pts = list(np.arange(s, S_RIF - 1e-12, -PASSO_S)[1:]) + [S_RIF]
    w, V = w_s, V_s
    acc = 0.0
    for x in pts:
        wn, V = passo(blocco(x), V)
        acc += av(wn - w)
        w = wn
    w_cont = av(w) - acc                   # ### lo zero continuo: a `S_RIF` la fase principale, poi risalendo le differenze
    out = {"omega_principale": w_s, "omega_cont": float(w_cont)}
    for segno, x in (("piu", s * (1 + H)), ("meno", s * (1 - H))):
        if x > 1.0:
            out[segno] = None
            continue
        wn, _ = passo(blocco(x), V_s)
        out[segno] = float(w_cont + av(wn - w_s))
    return out


def main(argv):
    del argv
    import _gravita_collettiva as GC
    import _presidio
    import _scala_e_zero as Z
    import _triangoli as T
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 100)
    print("I TRIANGOLI, PRIMO GRADINO: gli spettri, dove sta la fisica di bassa energia, la gravita' di Hamilton")
    print("=" * 100)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_triangoli.py", "csv/_zero_simmetrico.py", "csv/_scala_e_zero.py", "csv/_modi_pi_e_solitoni.py",
                                     "csv/_gravita_collettiva.py", "csv/_moneta_massa.py", "csv/_triangoli_bassa_energia.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: L %d; LF %d; S %s; EPS %s; PUNTI %s; DISPERSIVA %g; TOLL_GRUPPO %g; H %g; PASSO_S %g; S_RIF %g" % (L, LF, S_LISTA, EPS, PUNTI, DISPERSIVA, TOLL_GRUPPO, H, PASSO_S, S_RIF))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    warnings.simplefilter("ignore")
    ok_b, ciclo = T.bipartito(*T.toro_spostamenti((L, L), T.TRIANGOLI[0]))
    esito("DEVE FALLIRE: <<la griglia a triangoli e' bipartita>> (per la chiave giusta: il ciclo dispari)", not ok_b and ciclo is not None, "ciclo dispari %s" % (ciclo,))
    c6, serv = 0.0, 0.0
    righe, coppie = [], []
    for eps in EPS:
        for s in S_LISTA:
            A = matrice(eps, s, L, "simm")
            Ao = matrice(eps, s, L, "oggi")
            c6 = max(c6, float(T.scarto_c6(A)), float(T.scarto_c6(Ao)))
            Af = matrice(eps, s, LF, "simm")
            for n, (a, b) in PUNTI.items():
                serv = max(serv, float(np.abs(Af[a * LF // L, b * LF // L] - A[a, b]).max()))
            W = -np.angle(np.linalg.eigvals(A[:, :, :NB, :NB]))
            liv = {}
            for n, (a, b) in PUNTI.items():
                w = np.sort(np.array([av(x) for x in W[a, b]]))
                lv = []
                for x in w:
                    if lv and abs(x - lv[-1][0]) < 1e-9:
                        lv[-1][1] += 1
                    else:
                        lv.append([float(x), 1])
                liv[n] = lv
            scrivi({"tipo": "livelli", "eps": eps, "s": s, "livelli": liv})
            print("### eps %g s %g: i livelli (simmetrica) %s" % (eps, s, " | ".join("%s %s" % (n, " ".join("%+.4f(%d)" % (x, m) for x, m in lv)) for n, lv in liv.items())))
            # ---- le bande lungo le linee, la coppia e il suo salto
            ph = {nl: segui(A, c) for nl, c in LINEE.items()}
            gg = gruppi_dispersivi(ph["diag"][0])
            best = None
            for i in range(len(gg)):
                for j in range(i + 1, len(gg)):
                    for nl, (P, _vv) in ph.items():
                        gi = [b for b in gruppi_dispersivi(P) if abs(av(P[0, b[0]] - ph["diag"][0][0, gg[i][0]])) <= TOLL_GRUPPO]
                        gj = [b for b in gruppi_dispersivi(P) if abs(av(P[0, b[0]] - ph["diag"][0][0, gg[j][0]])) <= TOLL_GRUPPO]
                        if not gi or not gj:
                            continue
                        d = np.abs((P[:, gi[0][0]] - P[:, gj[0][0]] + np.pi) % (2.0 * np.pi) - np.pi)
                        m = int(np.argmin(d))
                        rec = {"i": i, "j": j, "linea": nl, "m": m, "k": list(LINEE[nl][m]), "salto": float(d[m]), "bande": [gi[0], gj[0]],
                               "fasi": [av(P[m, gi[0][0]]), av(P[m, gj[0][0]])]}
                        if best is None or rec["salto"] < best["salto"]:
                            best = rec
            if best is None:
                print("  nessuna coppia di bande dispersive")
                continue
            ks = tuple(best["k"])
            nomek = [n for n, kk in PUNTI.items() if kk == ks]
            scrivi(dict(best, tipo="salto_minimo", eps=eps, s=s, punto=nomek[0] if nomek else None))
            print("  la coppia dispersiva piu' stretta: il salto %.5f (salto/s %.4f) a k = %s (%s), linea %s; le fasi %+.4f %+.4f (il centro/s %+.4f)"
                  % (best["salto"], best["salto"] / s, ks, nomek[0] if nomek else "NON un punto speciale", best["linea"], best["fasi"][0], best["fasi"][1],
                     av(best["fasi"][0] + av(best["fasi"][1] - best["fasi"][0]) / 2.0) / s))
            P, vv = ph[best["linea"]]
            r_c = []
            for q, bb in enumerate(best["bande"]):
                V0 = vv[best["m"]][:, bb]
                Q, _ = np.linalg.qr(V0)
                w0 = best["fasi"][q]
                cu = curvatura(A, ks[0], ks[1], w0, Q)
                if nomek:
                    co = continua(eps, s, ks, vv[best["m"]][:, [bb[0]]], "oggi")
                else:
                    co = None
                rec = {"tipo": "modo", "eps": eps, "s": s, "k": list(ks), "punto": nomek[0] if nomek else None, "banda": q, "fase_simm": w0, **cu}
                simmetrico = bool(nomek) and nomek[0] in ("Gamma", "K", "K'")
                if simmetrico and not cu["piatta"] and not cu["isotropa"]:
                    # ### ⚠ a `Gamma`, `K`, `K'` *(fissi per `120` gradi)* ### **una banda vera e' ISOTROPA: se non lo e', la tracciatura ai vicini ha cambiato banda** *(annotazione `1`)*
                    print("    banda %d: anisotropa (%.1e) in un punto SIMMETRICO (%s): la tracciatura ai vicini NON e' affidabile, Hamilton non si calcola" % (q, cu["anisotropia"], nomek[0]))
                    rec = {"tipo": "modo", "eps": eps, "s": s, "k": list(ks), "punto": nomek[0], "banda": q, "fase_simm": w0, "piatta": True, "non_affidabile": True, **cu}
                    r_c.append(rec)
                    righe.append(rec)
                    scrivi(rec)
                    continue
                if cu["piatta"] or cu["v"] < PIATTA:
                    print("    banda %d: PIATTA a k* (curvatura %s, v %.1e): non e' un modo massivo fermo, Hamilton non si calcola" % (q, ["%+.1e" % x for x in cu["cart_autovalori"]], cu["v"]))
                    rec = {"tipo": "modo", "eps": eps, "s": s, "k": list(ks), "punto": nomek[0] if nomek else None, "banda": q, "fase_simm": w0, "piatta": True, **cu}
                    r_c.append(rec)
                    righe.append(rec)
                    scrivi(rec)
                    continue
                if co is not None and co["piu"] is not None:
                    w_c = co["omega_cont"]
                    dw = (co["piu"] - co["meno"]) / (2.0 * H * s)
                    D = GC.dproprio(co["meno"], w_c, co["piu"], s * (1 - H), s, s * (1 + H))
                    k = cu["h11"] / cu["v"] ** 2 if cu["v"] else None
                    rec.update(oggi={"omega": w_c, "E0": w_c / s, "M": cu["h11"] / s, "E0M_positivo": w_c * cu["h11"] > 0, "D": D, "d_omega_ds": dw,
                                     "H_su_RG": None if k is None else s * k * dw},
                               simm={"omega": w_c + np.pi * s, "E0": w_c / s + np.pi, "M": cu["h11"] / s, "E0M_positivo": (w_c + np.pi * s) * cu["h11"] > 0, "D": D,
                                     "d_omega_ds": dw + np.pi, "H_su_RG": None if k is None else s * k * (dw + np.pi)})
                r_c.append(rec)
                righe.append(rec)
                scrivi(rec)
                q0, q5 = rec.get("oggi"), rec.get("simm")
                print("    banda %d: curvatura (theta) %+.4f %+.4f %+.4f; cartesiana %s %s (%.1e) | v %.4f v_g (%+.1e, %+.1e) | oggi: omega %s E0 %s E0M %s D %s a_H/a_RG %s | simm: E0 %s E0M %s a_H/a_RG %s"
                      % (q, cu["h11"], cu["h22"], cu["h12"], ["%+.4f" % x for x in cu["cart_autovalori"]], "ISOTROPA" if cu["isotropa"] else "anisotropa", cu["anisotropia"], cu["v"],
                         cu["v_g"][0], cu["v_g"][1], f_(q0 and q0["omega"]), f_(q0 and q0["E0"]), "--" if not q0 else ("+" if q0["E0M_positivo"] else "-"), f_(q0 and q0["D"], "%+.2e"),
                         f_(q0 and q0["H_su_RG"]), f_(q5 and q5["E0"]), "--" if not q5 else ("+" if q5["E0M_positivo"] else "-"), f_(q5 and q5["H_su_RG"])))
                sys.stdout.flush()
            if len(r_c) == 2 and all(r.get("oggi") and r["oggi"]["H_su_RG"] is not None for r in r_c) and not any(r.get("piatta") for r in r_c):
                a0, b0 = r_c[0]["oggi"]["H_su_RG"], r_c[1]["oggi"]["H_su_RG"]
                a5, b5 = r_c[0]["simm"]["H_su_RG"], r_c[1]["simm"]["H_su_RG"]
                ma, mb = 2.0 * (a5 - a0), 2.0 * (b5 - b0)
                ls = (b0 - a0) / (ma - mb) if ma != mb else None
                coppie.append({"eps": eps, "s": s, "k": list(ks), "lambda_stella": ls})
                scrivi({"tipo": "lambda_stella", "eps": eps, "s": s, "k": list(ks), "lambda_stella": ls})
                print("    lambda* della coppia a %s: %s" % (ks, f_(ls, "%.8f")))
    esito("DEVE PASSARE: lo spettro invariante per 60 gradi entro 1e-12 (ruota60, ogni eps, s, convenzione)", c6 < 1e-12, "il peggiore %.2e" % c6)
    esito("DI SERVIZIO: il blocco al lato %d = al lato %d ai punti speciali, entro 1e-12" % (LF, L), serv < 1e-12, "il peggiore %.2e" % serv)
    ls = [c["lambda_stella"] for c in coppie if c["lambda_stella"] is not None]
    esito("PUO' FALLIRE: lambda* = 1/2 entro 1e-6 al punto del salto minimo (%d coppie)" % len(ls), len(ls) > 0 and all(abs(x - 0.5) < 1e-6 for x in ls),
          "; ".join("eps %g s %g: %.8f" % (c["eps"], c["s"], c["lambda_stella"]) for c in coppie if c["lambda_stella"] is not None))
    # ---------------------------------------------------------------- il passo: delta(s)
    print("### IL PASSO: delta(s) = ||H_eff(s) - H_eff(%g)|| / ||H_eff(%g)|| a Gamma e a k = (2 pi/16, 0), il logaritmo principale (lato 16)" % (S_RIF, S_RIF))
    SS = (S_RIF,) + tuple(x for x in Z.S_LISTA if x > S_RIF)

    def deltas(eps, pezzo=None):
        out = {}
        for q, (a, b) in (("Gamma", (0, 0)), ("k(1,0)", (1, 0))):
            Hs = {}
            for x in SS:
                if pezzo:
                    with un_pezzo(pezzo):
                        B = matrice(eps, x, 16, "oggi")[a, b, :NB, :NB]
                else:
                    B = matrice(eps, x, 16, "oggi")[a, b, :NB, :NB]
                lam, V = np.linalg.eig(B)
                Hs[x] = Z.H_eff(V, -np.angle(lam), x)
            n0 = np.linalg.norm(Hs[S_RIF])
            out[q] = {x: float(np.linalg.norm(Hs[x] - Hs[S_RIF]) / n0) for x in SS}
        return out
    peg = 0.0
    for pz in ("CAMM-GROVER", "CAMM-SPOSTAMENTO"):
        d = deltas(0.5, pz)
        peg = max(peg, max(max(v.values()) for v in d.values()))
        print("  solo %s: %s" % (pz, " | ".join("%s %s" % (q, " ".join("%g:%.1e" % (x, y) for x, y in v.items())) for q, v in d.items())))
    esito("DEVE PASSARE: un pezzo solo, delta(s) < 1e-12 (Grover o spostamento, Gamma e k(1,0), eps 0.5)", peg < 1e-12, "il peggiore %.2e" % peg)
    esp = []
    for eps in EPS:
        d = deltas(eps)
        for q, v in d.items():
            p, ps = Z.esponente(v), Z.esponente(v, True)
            scrivi({"tipo": "delta", "eps": eps, "k": q, "delta": {str(x): y for x, y in v.items()}, "esponente": p, "esponente_contro_s": ps})
            print("  passo intero eps %g %s: %s | esponente (s - 0.02) %s, (s) %s" % (eps, q, " ".join("%g:%.1e" % (x, y) for x, y in v.items()), f_(p, "%.3f"), f_(ps, "%.3f")))
            if q == "k(1,0)":
                esp.append(ps)
    esito("PUO' FALLIRE: l'esponente di delta(s) del passo intero (k(1,0), contro s, s <= 0.3) fra 1.8 e 2.2, ogni eps", all(e is not None and 1.8 <= e <= 2.2 for e in esp),
          " ".join(f_(e, "%.3f") for e in esp))
    print("=" * 100)
    print("I TRIANGOLI, PRIMO GRADINO: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
