# -*- coding: utf-8 -*-
r"""**[M1052-G] [M1052-I] L'ANEMOMETRO: IL FLUSSO DI `chi`, IL FLUSSO DELLA MATERIA, IL DISTURBO DEL VUOTO E L'AGGANCIO DI FASE SUGLI ANELLI** *(il mandato di Luca [M1052], fase 3, e l'aggiunta delle `10:59`; la carta `doc/TASK_HISTORY/2026-11-22_anemometro.md`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/anemometro.py > doc/referti_l2/anemometro.txt

**Gli anelli** `|r - R| < 0.5`, `R = 20, 25, 30, 40, 60`, attorno al baricentro di `rho` dello stato. **Per anello:** `Phi_chi = c2 f 2 pi R dchi/dr` *(`dchi/dr` dalle medie sugli anelli `R +- 1`)* contro `r K1(r/lambda)` e `dchi/dr` contro `K1`, normalizzati a `r 30`, `lambda = sqrt(3/2 c2/m2)`; `Phi_J = 2 pi R <J . r_hat>`; `<|phi - phi0|>` *(`porto.dphi_nodi`)*; **`Gamma`** del vuoto e della materia *(`w = |phi - phi0|`, `theta_mattone` la fase pesata con `rho` entro `r 15`)*; `dGamma/dt` fra stati successivi. **I casi noti:** il punto-sorgente col solutore del codice contro il continuo con le immagini; il vuoto F3 puro; il mescolamento col seme `11`.
"""
import glob
import hashlib
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import chi_tick as CT  # noqa: E402
import caduta_libera as CL  # noqa: E402
import gravita_due_corpi as GD  # noqa: E402
import girandola_chi_v3 as GC  # noqa: E402

RAGGI = (20.0, 25.0, 30.0, 40.0, 60.0)          # ### Luca
R_NUCLEO = 15.0                                  # ### Luca: theta_mattone entro r 15
RHO_MIN = 1e-6                                   # ### Luca: la fase della materia dove rho > 1e-6
MATTONE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "mattone_v2")
K_MATTONE = (2000, 6000, 10000)                  # ### Luca, piu' l'ultimo
VARIANTI = ("V0", "V1", "V2", "V3", "V4", "V1m")
KS_CAD = tuple(range(0, 2001, 250))
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def leggi(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    z = np.load(f)
    X = {x: z[x] for x in z.files}
    return X, json.loads(str(X.pop("meta")))


def lam_di(c2, m2):
    return math.sqrt(1.5 * c2 / m2)


def K1(x):
    from scipy.special import k1
    return float(k1(x))


def flusso_radiale(campo, r, dxy):
    """### per `R` in `RAGGI`: `(media sull'anello, d/dr dalle medie a R +- 1)`."""
    out = {}
    for R in RAGGI:
        a = lambda R_: float(campo[np.abs(r - R_) < 0.5].mean())
        out[R] = (a(R), (a(R + 1.0) - a(R - 1.0)) / 2.0)
    return out


def gamma(theta, w, th0, ring, rng=None):
    th = theta[ring]
    if rng is not None:
        th = rng.permutation(th)
    ww = w[ring]
    s = ww.sum()
    return float(abs(np.sum(ww * np.exp(1j * (th - th0)))) / s) if s > 0 else 0.0


def J_di(Z, X, cam, cs, e0s, N, vett):
    import _u1_prototipo as U1
    mot = Z["mot"]
    n = mot.inc.n
    sp = mot.operatori["spostamento_trasporto"]
    Z["metti"]({x: X[x] for x in Z["chiavi"]})
    cam.A[...] = X["campo_A"]
    mot.cs = cs
    mot.lambda_c = None
    if e0s:
        CT.fase_a(mot, Z["st"], e0s, N)
    U1.scrivi_U(mot, cam)
    mm = cam.m
    prima = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
    sp(Z["st"], Z["par"], 0.5)
    J = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
    Z["metti"]()
    return (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)


def misura(Z, X, k, t0, cs, e0s, N, c2f, cam, vett, rng=None):
    """### un dizionario per anello: `chi`, `Phi_chi`, `dchi/dr`, `Phi_J`, `dphi`, `Gv`, `Gm`, `n`."""
    from solitone import porto as PO
    from solitone import toro as TO
    mot, n, L = Z["mot"], Z["n"], Z["L"]
    nodo = np.asarray(mot.inc.nodo)
    rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
    b = TO.centro(rho, Z["m1"], Z["m2"], L)[:2]
    dxy = TO.scarti(Z["m1"], Z["m2"], b[0], b[1], L)[:, :2]
    r = np.hypot(dxy[:, 0], dxy[:, 1])
    Z["metti"]({x: X[x] for x in Z["chiavi"]})
    dphi = PO.dphi_nodi(Z, t0 + k)
    from solitone import bordo as BO
    phi0 = BO.c_di(t0 + k, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
    zz = np.conj(phi0) * Z["st"]["phi_h"]
    Z["metti"]()
    tv = np.angle(np.bincount(nodo, weights=zz.real, minlength=n) + 1j * np.bincount(nodo, weights=zz.imag, minlength=n))
    pn = GC.fase_dei_nodi(X["psi_h"], nodo)
    comp = int(np.argmax([np.sum(np.abs(pn[r < R_NUCLEO, c]) ** 2) for c in (0, 1)]))
    tm = np.angle(pn[:, comp])
    nuc = r < R_NUCLEO
    tv0 = float(np.angle(np.sum(rho[nuc] * np.exp(1j * tv[nuc]))))
    tm0 = float(np.angle(np.sum(rho[nuc] * np.exp(1j * tm[nuc]))))
    Jn = J_di(Z, X, cam, cs, e0s, N, vett)
    rh = dxy / np.maximum(r, 1e-12)[:, None]
    Jr = (Jn * rh).sum(axis=1)
    fc = flusso_radiale(X["chi"], r, dxy) if "chi" in X else None
    out = {"b": b}
    for R in RAGGI:
        ring = np.abs(r - R) < 0.5
        out[R] = {"n": int(ring.sum()), "dphi": float(dphi[ring].mean()), "Phi_J": float(2.0 * math.pi * R * Jr[ring].mean()),
                  "Gv": gamma(tv, dphi, tv0, ring, rng), "Gm": gamma(tm, dphi, tm0, ring & (rho > RHO_MIN), rng) if np.any(ring & (rho > RHO_MIN)) else float("nan"),
                  "nm": int((ring & (rho > RHO_MIN)).sum())}
        if fc:
            out[R]["chi"], out[R]["dchi"] = fc[R]
            out[R]["Phi_chi"] = c2f * 2.0 * math.pi * R * fc[R][1]
    return out


def stampa(nome, k, M, lam, prec=None, dt=250.0):
    print("    %s k %6d (il baricentro %s):" % (nome, k, ["%.2f" % x for x in M["b"]]))
    for R in RAGGI:
        m = M[R]
        dG = ((m["Gv"] - prec[R]["Gv"]) / dt) if prec else float("nan")
        s = "      R %4.0f (n %4d): <|phi-phi0|> %.4e; Phi_J %+.4e; Gamma vuoto %.4f (dGamma/dt %+.3e), materia %s (n %d)" % (
            R, m["n"], m["dphi"], m["Phi_J"], m["Gv"], dG, ("%.4f" % m["Gm"]) if m["nm"] else "-", m["nm"])
        if "Phi_chi" in m:
            s += "; chi %.6e, dchi/dr %+.4e, Phi_chi %+.4e; Phi_chi/Phi_chi(30) %.4f contro r K1 %.4f; dchi/dr/(30) %.4f contro K1 %.4f" % (
                m["chi"], m["dchi"], m["Phi_chi"], m["Phi_chi"] / M[30.0]["Phi_chi"], R * K1(R / lam) / (30.0 * K1(30.0 / lam)), m["dchi"] / M[30.0]["dchi"], K1(R / lam) / K1(30.0 / lam))
        print(s)


def caso_noto_G():
    """### il punto-sorgente: il solutore del codice contro il continuo con le immagini, lo stesso operatore."""
    from scipy.special import k0
    from solitone import toro as TO
    print("-" * 130)
    print("IL CASO NOTO (G): chi = (c2 L + m2)^-1 delta su S162, contro somma_immagini K0(|x - x_i|/lambda) (|k| <= 2), lo stesso operatore; normalizzati a r 30")
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        Lp = CT.Laplaciano(mot)
        P = CT.Parametri(1.0, 0.0, 0.15, 0.0)
        lam = lam_di(P.c2, P.m2)
        c = [L // 2, L // 2]
        v0 = int(c[0] * L + c[1])
        sor = np.zeros(n)
        sor[v0] = 1.0
        chi = Lp.statico(P, sor)
        dxy = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2]
        r = np.hypot(dxy[:, 0], dxy[:, 1])
        A1, A2 = TO.vettori()
        an = np.zeros(n)
        for k1 in range(-2, 3):
            for k2 in range(-2, 3):
                sh = L * (k1 * np.asarray(A1, float)[:2] + k2 * np.asarray(A2, float)[:2])
                rr = np.hypot(*(dxy - sh).T)
                an += k0(np.maximum(rr, 1e-9) / lam)
        fm, fa = flusso_radiale(chi, r, dxy), flusso_radiale(an, r, dxy)
        Z["metti"]()
    peggio, peggio_log = 0.0, 0.0
    for R in RAGGI:
        qm = R * fm[R][1] / (30.0 * fm[30.0][1])
        qa = R * fa[R][1] / (30.0 * fa[30.0][1])
        qk = R * K1(R / lam) / (30.0 * K1(30.0 / lam))
        print("    R %4.0f: il flusso / quello a r 30: il solutore %.6f, il continuo con le immagini %.6f (lo scarto %+.2e), r K1 nudo %.6f (lo scarto %+.2e); senza massa 1.000000" % (R, qm, qa, qm / qa - 1.0, qk, qm / qk - 1.0))
        peggio = max(peggio, abs(qm / qa - 1.0))
        if R == 60.0:
            peggio_log = abs(qm - 1.0)
    print("    lambda %.4f" % lam)
    esito("G CASO NOTO: il flusso del solutore = il continuo con le immagini entro l'1% a r 20, 25, 40, 60", peggio <= 0.01, "(lo scarto massimo %.2e)" % peggio)
    esito("G DEVE FALLIRE: contro il campo senza massa (il flusso costante) lo scarto a r 60 oltre l'1%", peggio_log > 0.01, "(%.2e)" % peggio_log)
    return lam


def main():
    import _presidio
    from solitone import convergenza as CV
    import prova_scatola5 as PS
    for m in ("chi_tick.py", "caduta_libera.py", "gravita_due_corpi.py", "girandola_chi_v3.py", "triangolo_chi_v4.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    MT = TC.moduli()[0]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    print("=" * 130)
    print("[M1052-G] [M1052-I] L'ANEMOMETRO (la carta 2026-11-22_anemometro.md): gli anelli %s; t0 %r" % (list(RAGGI), t0))
    print("=" * 130)
    lam = caso_noto_G()
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    vett = np.stack([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2], np.asarray(A1, float)[:2] + np.asarray(A2, float)[:2]])
    TAB = {}
    # ### la caduta (S162)
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        cs0 = mot.cs
        # ### (I) il caso noto sul vuoto F3 puro
        print("-" * 130)
        print("IL CASO NOTO (I): il vuoto F3 puro dopo UN tick del tick U (psi = 0)")
        Z["g_e"] = np.zeros_like(Z["g_e"])
        MT.vuoto_fresco(Z, t0)
        PO_ = TC.moduli()[5]
        C = PO_.campi(Z, rho_c, e)
        GD.tick_U(Z["z"], C.campo, float(Z["s"]))
        X = {x: Z["st"][x].copy() for x in Z["chiavi"]}
        X["campo_A"] = C.campo.A.copy()
        X["psi_h"][0, 0] = 1e-30                                     # ### un baricentro definito; rho resta ~0
        Mv = misura(Z, X, 1, t0, np.full(n, float(Z["s"])), 0.0, np.ones(n), 0.0, cam, vett)
        okv = all(Mv[R]["Gv"] <= 3.0 / math.sqrt(Mv[R]["n"]) for R in RAGGI)
        print("    " + "; ".join("R %.0f: <|phi-phi0|> %.2e, Gamma %.4f (3/sqrt(n) %.4f), Phi_J %+.2e" % (R, Mv[R]["dphi"], Mv[R]["Gv"], 3.0 / math.sqrt(Mv[R]["n"]), Mv[R]["Phi_J"]) for R in RAGGI))
        esito("I CASO NOTO: sul vuoto F3 puro Gamma <= 3/sqrt(n) su ogni anello e Phi_J = 0 (entro 1e-25)", okv and all(abs(Mv[R]["Phi_J"]) <= 1e-25 for R in RAGGI))
        Z["metti"]()
        for V in VARIANTI:
            fs = [os.path.join(CL.BASE, V, "stato_%06d.npz" % k) for k in KS_CAD]
            if not all(os.path.exists(f + ".sha1") for f in fs):
                print("### %s: gli stati non ci sono tutti: saltata" % V)
                continue
            print("-" * 130)
            print("LA CADUTA %s (chi IMPOSTO: il suo flusso e' il seno, non il mattone)" % V)
            prec = None
            TAB[V] = []
            for k, f in zip(KS_CAD, fs):
                X, meta = leggi(f)
                N = X["N"]
                s, e0 = float(meta["s"]), float(meta["e0"])
                cs = s * N if meta["cs_N"] else np.full(n, s)
                M = misura(Z, X, k, t0, cs, float(meta["segno_fase"]) * e0, N, 0.0, cam, vett)
                for R in RAGGI:
                    M[R].pop("Phi_chi", None)
                stampa(V, k, M, lam, prec)
                if prec:
                    TAB[V].append((k, M, prec))
                if V == "V1" and k == 2000:
                    rng = np.random.default_rng(11)
                    Ms = misura(Z, X, k, t0, cs, float(meta["segno_fase"]) * e0, N, 0.0, cam, vett, rng=rng)
                    alti = [R for R in RAGGI if M[R]["Gv"] > 0.2]
                    print("    IL DEVE-FALLIRE (I), V1 k 2000, le fasi mescolate (seme 11): %s; gli anelli con Gamma > 0.2 senza mescolare: %s" % (
                        "; ".join("R %.0f %.4f -> %.4f" % (R, M[R]["Gv"], Ms[R]["Gv"]) for R in RAGGI), alti or "NESSUNO (il deve-fallire non ha materia: non lo conto)"))
                    if alti:
                        esito("I DEVE FALLIRE: con le fasi mescolate Gamma < 0.05 dove senza mescolare e' sopra 0.2", all(Ms[R]["Gv"] < 0.05 for R in alti))
                prec = M
        mot.cs = cs0
        mot.lambda_c = None
        Z["metti"]()
    # ### il mattone con chi (L 186)
    ultimo = int(sorted(glob.glob(os.path.join(MATTONE, "stato_*.npz")))[-1][-9:-4])
    ks = list(K_MATTONE) + ([ultimo] if ultimo not in K_MATTONE else [])
    print("-" * 130)
    print("IL MATTONE CON chi (chi-mattone-v2, L 186, il bordo R_A 50: l'anello di r 60 e' DENTRO il bordo): k %s, ciascuno col precedente k - 250" % ks)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot, n = Z["mot"], Z["n"]
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        cs0 = mot.cs
        TAB["mattone"] = []
        for k in ks:
            pr = None
            for kk in (k - 250, k):
                X, meta = leggi(os.path.join(MATTONE, "stato_%05d.npz" % kk))
                pm = meta["parametri"]
                N = np.exp(-float(pm["kappa"]) * X["chi"])
                M = misura(Z, X, kk, t0, float(pm["s"]) * N, float(pm["e0"]), N, float(pm["c2"]) * float(pm["f"]), cam, vett)
                stampa("mattone", kk, M, lam, pr)
                if pr:
                    TAB["mattone"].append((kk, M, pr))
                pr = M
        mot.cs = cs0
        mot.lambda_c = None
        Z["metti"]()
    # ### (c) il confronto
    print("=" * 130)
    print("(c) IL CONFRONTO: Phi_J / Gamma e Phi_J / (dGamma/dt) per anello; il coefficiente di variazione (std/|media|) fra gli anelli 25-60 e fra le varianti V1-V4")
    print("=" * 130)
    ult = {}
    for nome in ("V1", "V2", "V3", "V4", "mattone"):
        if not TAB.get(nome):
            continue
        k, M, prec = TAB[nome][-1]
        q1 = {R: M[R]["Phi_J"] / M[R]["Gv"] if M[R]["Gv"] else float("nan") for R in RAGGI}
        dG = {R: (M[R]["Gv"] - prec[R]["Gv"]) / 250.0 for R in RAGGI}
        q2 = {R: M[R]["Phi_J"] / dG[R] if dG[R] else float("nan") for R in RAGGI}
        ult[nome] = (q1, q2)
        cv = lambda q: float(np.std([q[R] for R in RAGGI[1:]]) / abs(np.mean([q[R] for R in RAGGI[1:]])))
        print("  %-8s k %6d: Phi_J/Gamma %s (cv 25-60 %.3f); Phi_J/(dGamma/dt) %s (cv 25-60 %.3f)" % (
            nome, k, ", ".join("%.0f: %+.3e" % (R, q1[R]) for R in RAGGI), cv(q1), ", ".join("%.0f: %+.3e" % (R, q2[R]) for R in RAGGI), cv(q2)))
    for R in RAGGI[1:]:
        vv = [ult[x][1][R] for x in ("V1", "V2", "V3", "V4") if x in ult]
        if len(vv) >= 2:
            print("  R %.0f: Phi_J/(dGamma/dt) fra le varianti V1-V4 %s: cv %.3f" % (R, ", ".join("%+.3e" % x for x in vv), float(np.std(vv) / abs(np.mean(vv)))))
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
