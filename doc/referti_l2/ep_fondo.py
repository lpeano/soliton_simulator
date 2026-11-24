# -*- coding: utf-8 -*-
r"""**[M1330-F] E(p): PARTICELLA O LUCE?** *(DECISIONE DI LUCA, 2026-11-24 14:45; la carta `doc/CARTA_fondo_giusto.md`, sez. `4-ter`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/ep_fondo.py calcio --k 0.1        (k 0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5: 1000 tick)
    E:\python\py3132\python.exe doc/referti_l2/ep_fondo.py noto_a                (il caso noto (a): il calcio 0.010 di 1c rifatto)
    E:\python\py3132\python.exe doc/referti_l2/ep_fondo.py lettura > doc/referti_l2/ep_fondo.txt

**L'oggetto:** lo stato `k 300` del giro 1 del punto fisso *(`w` minimo; il punto fisso non ha passato B1)*. **`fondo_1c.calcio` cosi' com'e'**, `OGGETTO` e `BASE` in memoria, e **`fondo_1c.ciclo` avvolta: salva SOLO lo stato finale** *(i pezzi)*. **La lettura:** `p` dalla trasformata per cella *(sei mezzi archi x due componenti)*, `v` del baricentro su `[200, 1000]`, `E_H` = `H(calciato) - H(fermo)` col libro dei conti, `E_w` = `<omega>(calciato) - <omega>(fermo)`; i due fit con `c` libera e `c = 0.084955` per tick; il caso noto (a) al bit, (b) l'onda piana lineare entro `1e-10`.
"""
import argparse
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import tenuta_fondo as TF  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
OGG = os.path.join(CTRL, "M1330", "puntofisso", "giro_1", "stato_000300.npz")
BASE = os.path.join(CTRL, "M1330", "ep")
KK = (0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5)
C_RET = 0.084955          # ### v_max della banda PER TICK (spettro_gap_v2.txt); = 0.566 s, s = 0.15
TOLL_B = 1e-10


def base_k(k):
    return os.path.join(BASE, "k%.3f" % k)


def con_finale():
    vero = F1.ciclo

    def ciclo(Z, C, quanti, dopo, MV, P0, N, cs_N, segno):
        vero(Z, C, quanti, dopo, MV, P0, N, cs_N, segno)
        f = os.path.join(F1.BASE, "stato_finale.npz")
        dati = {x: Z["st"][x] for x in Z["chiavi"]}
        dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
        np.savez(f, meta=np.array(json.dumps({"k": quanti})), **dati)
        import hashlib
        open(f + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(f, "rb").read()).hexdigest() + "\n")
    F1.ciclo = ciclo


def calcio(k):
    import _presidio
    _presidio.avvia(__file__)
    F1.OGGETTO = OGG
    F1.BASE = base_k(k)
    con_finale()
    return F1.calcio(k)


def noto_a():
    import _presidio
    _presidio.avvia(__file__)
    F1.BASE = os.path.join(BASE, "noto_a")
    return F1.calcio(0.010)


def momento(psi_h, n, L, Bv, Kv, u):
    """### `p` = la media di `(k - K) . u` pesata con `|psi~_k|^2`, per cella *(i 12 = sei mezzi archi x due componenti)*."""
    psi = psi_h.reshape(n, 12)
    W = np.zeros((L, L))
    for j in range(12):
        F = psi[:, j].reshape(L, L)
        W += np.abs(np.fft.fft2(F)) ** 2
    a = np.arange(L) / float(L)
    ca, cb = np.meshgrid(a, a, indexing="ij")
    da, db = ca - 1.0 / 3.0, cb - 1.0 / 3.0
    best = None
    for sa in (-2, -1, 0, 1):
        for sb in (-2, -1, 0, 1):
            x = (da + sa)[..., None] * Bv[0] + (db + sb)[..., None] * Bv[1]
            nn = np.hypot(x[..., 0], x[..., 1])
            if best is None:
                best, bn = x.copy(), nn
            else:
                m = nn < bn
                best[m], bn = x[m], np.where(m, nn, bn)
    return float(np.sum(W * (best @ u)) / np.sum(W))


def acca(Z, C):
    from solitone import conti as CO
    return float(np.sum(CO.conti_nodo(Z)["tot"])) + float(C.campo.K() + C.campo.V())


def onda_piana(Bv, Kv):
    """### il caso noto (b): un tick della risposta lineare (`tenuta_fondo.risposta`, `+A`/`-A`) su un'onda piana a `K + B0/L`."""
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    A_IMP = T4B.A_IMP
    with TF.TC.scena() as Z:
        Rs, ds = TF.risposta(Z)
        L, n = Z["L"], Z["mot"].inc.n
        kq = Kv + Bv[0] / float(L)
        G = np.einsum("x,xij->ij", np.exp(-1j * (ds @ kq)), Rs)
        lam, V = np.linalg.eig(G)
        E = -np.angle(lam)
        i = int(np.argmin(np.abs(E - TF.E_FONDO)))
        q = V[:, i] / np.linalg.norm(V[:, i])
        A1, A2 = TO.vettori()
        r = np.asarray(Z["m1"], float)[:, None] * np.asarray(A1, float)[:2] + np.asarray(Z["m2"], float)[:, None] * np.asarray(A2, float)[:2]
        fase = np.exp(1j * (r @ kq))
        p0 = (fase[:, None] * q[None, :]).reshape(-1) / math.sqrt(n)
        MT, PO = TF.TC.moduli()[0], TF.TC.moduli()[5]
        rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
        e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
        st, mot, s = Z["st"], Z["mot"], float(Z["s"])
        Z["g_e"] = np.zeros_like(Z["g_e"])
        MT.vuoto_fresco(Z, t0)
        C = PO.campi(Z, rho_c, e)
        base = {x: st[x].copy() for x in Z["chiavi"]}
        A0, E0_, U0 = C.campo.A.copy(), C.campo.E.copy(), mot.geo.U.copy()
        us = []
        for f in (1.0, -1.0):
            for x in Z["chiavi"]:
                st[x][...] = base[x]
            st["psi_h"][...] = (f * A_IMP * p0).reshape(st["psi_h"].shape)
            C.campo.A[...], C.campo.E[...] = A0, E0_
            mot.geo.U[...] = U0
            mot.lambda_c = None
            F1.CS.tick_var(Z["z"], C.campo, s, e0, np.ones(n), False, 0)
            us.append(st["psi_h"].reshape(-1).copy())
        lin = (us[0] - us[1]) / (2.0 * A_IMP)
        Z["metti"]()
    w = float(-np.angle(np.vdot(p0, lin)))
    return w, float(E[i]), float(abs(np.vdot(p0, lin)))


def lettura():
    import _presidio
    import gravita_due_corpi_misure as GM
    from scipy.optimize import curve_fit
    from solitone import toro as TO
    F1.avvia()
    TF.avvia()
    _presidio.avvia(__file__)
    MC = F1.MC
    print("=" * 130)
    print("[M1330-F] E(p): PARTICELLA O LUCE? (la carta sez. 4-ter): l'oggetto %s; c = %.6f per tick (= 0.566 s)" % (OGG, C_RET))
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    # ### il caso noto (a)
    F1.BASE = os.path.join(BASE, "noto_a")
    ra = F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    F1.BASE = os.path.join(CTRL, "M1658", "c1")
    r1 = F1.leggi("calcio_%s" % MC.nome(0.010, 1))
    if ra is not None:
        esito("(a) il calcio 0.010 di 1c rifatto = M1658/c1 AL BIT (la serie e omega)", ra["serie"] == r1["serie"] and ra["omega"] == r1["omega"])
    else:
        esito("(a) il calcio 0.010 di 1c rifatto: NON FINITO", False)
    # ### il caso noto (b)
    A1, A2 = TO.vettori()
    Av = np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]])
    Bv = 2.0 * np.pi * np.linalg.inv(Av).T
    Kv = (Bv[0] + Bv[1]) / 3.0
    wb, Eb, mod = onda_piana(Bv, Kv)
    esito("(b) l'onda piana lineare a K + B0/L: omega del tick = -arg lambda della banda entro %.0e" % TOLL_B, abs(wb - Eb) <= TOLL_B, "%+.15f contro %+.15f (|d| %.1e; |<p0|lin>| %.15f)" % (wb, Eb, abs(wb - Eb), mod))
    # ### le corse
    u = MC.asse_u(1)
    F1.FS.stato_di = lambda sorgente, kstato: OGG
    R = {}
    with F1.TC.scena() as Z:
        C, info, dxy, _forma, _X = F1.FS.carica(Z, "K", 3000)
        n, L = Z["n"], Z["L"]
        nodo = np.asarray(Z["mot"].inc.nodo)
        psi0 = Z["st"]["psi_h"].copy()
        H0 = acca(Z, C)
        for k in KK:
            Z["st"]["psi_h"][...] = psi0 * np.exp(1j * float(k) * (dxy @ u))[nodo][:, None] if k else psi0
            R[k] = {"p": momento(Z["st"]["psi_h"], n, L, Bv, Kv, u), "H": acca(Z, C) - H0}
        Z["st"]["psi_h"][...] = psi0
        Z["metti"]()
    with F1.TC.scena() as Z:
        nodo2, n2, L2 = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        Z["metti"]()
    dp = R[0.01]["p"] - R[0.0]["p"]
    esito("il controllo di p: p(0.010) - p(0) = 0.010 entro l'1%", abs(dp / 0.010 - 1.0) <= 0.01, "%.6e" % dp)
    righe = []
    for k in KK:
        F1.BASE = base_k(k)
        r = F1.leggi("calcio_%s" % MC.nome(k, 1))
        if r is None:
            print("  k %.3f: NON FINITA" % k)
            continue
        v, sv, _ = MC.velocita(r["serie"])
        om = np.array(r["omega"])
        ff = os.path.join(base_k(k), "stato_finale.npz")
        pz = F1.TT.misura(ff, nodo2, n2, L2)[1] if os.path.exists(ff + ".sha1") else -1
        R[k].update(v=v, sv=sv, w=float(om.mean()), sw=float(om.std() / math.sqrt(len(om))), pezzi=pz)
        righe.append(k)
    if 0.0 not in righe:
        print("### il fermo (k 0) NON FINITO")
        print("=" * 130)
        return 1
    f0 = R[0.0]
    print("  %6s %12s %14s %14s %14s %14s %6s" % ("k", "p", "v", "E_H", "E_w", "+- E_w", "pezzi"))
    for k in righe:
        x = R[k]
        x["Ew"], x["sEw"] = x["w"] - f0["w"], math.hypot(x["sw"], f0["sw"])
        print("  %6.3f %+12.6f %+14.6e %+14.6e %+14.6e %14.1e %6d%s" % (k, x["p"] - f0["p"], x["v"] - f0["v"], x["H"], x["Ew"], x["sEw"], x["pezzi"], "" if x["pezzi"] == 1 else "  ### NON UN PEZZO: il limite"))
    ks = [k for k in righe if k > 0]
    P = np.array([R[k]["p"] - f0["p"] for k in ks])
    Vv = np.array([R[k]["v"] - f0["v"] for k in ks])
    ms = 0.010 / (R[0.01]["v"] - f0["v"]) if 0.01 in righe else float("nan")
    print("  m* del calcio 0.010: %+.4f; m* c = %.4f (il p a cui gamma si fa sentire)" % (ms, ms * C_RET))
    for nomeE, chiave, sig in (("E_H (il libro dei conti)", "H", None), ("E_w (omega, la cima)", "Ew", "sEw")):
        E = np.array([R[k][chiave] for k in ks])
        S = np.array([R[k][sig] for k in ks]) if sig else None
        print("-" * 130)
        print("  %s%s" % (nomeE, "" if sig else "  ### senza barra: i chi quadri NON pesati"))
        tre = np.argsort(np.abs(P))[:3]
        mcurv = float(np.sum(P[tre] ** 4) / (2.0 * np.sum(E[tre] * P[tre] ** 2)))
        print("    m dalla curvatura (E = p^2/2m sui tre p piu' piccoli) %+.4f, contro m* %+.4f" % (mcurv, ms))

        def chi(f, par):
            r_ = E - f(P, *par)
            return float(np.sum((r_ / S) ** 2)) if sig else float(np.sum(r_ ** 2))
        onda = lambda p, c, b: c * p + b  # noqa: E731
        onda_c = lambda p, b: C_RET * p + b  # noqa: E731
        part = lambda p, m, c: np.sqrt((m * c * c) ** 2 + (p * c) ** 2) - m * c * c  # noqa: E731
        part_c = lambda p, m: np.sqrt((m * C_RET ** 2) ** 2 + (p * C_RET) ** 2) - m * C_RET ** 2  # noqa: E731
        for nome, f, p0_ in (("onda E = c p + b, c libera", onda, (C_RET, 0.0)), ("onda, c = 0.084955", onda_c, (0.0,)),
                             ("particella, c libera", part, (abs(ms), C_RET)), ("particella, c = 0.084955", part_c, (abs(ms),))):
            try:
                par, _cov = curve_fit(f, P, E, p0=p0_, sigma=S, absolute_sigma=bool(sig), maxfev=20000)
                print("    %-32s i parametri %s; chi quadro %.4e" % (nome, " ".join("%+.6e" % x for x in par), chi(f, par)))
                if nome == "particella, c libera":
                    m_, c_ = par
                    Et = E + m_ * c_ * c_
                    print("      v(p) contro p c^2/(E + m c^2): " + "; ".join("p %+.4f: %+.4e / %+.4e" % (a, b, a * c_ * c_ / e_) for a, b, e_ in zip(P, Vv, Et)))
                    o = np.argsort(P)
                    dpdv = np.gradient(P[o], Vv[o])
                    g3 = (1.0 / np.sqrt(np.maximum(1.0 - (Vv[o] / c_) ** 2, 1e-300))) ** 3 * m_
                    print("      dp/dv contro gamma^3 m: " + "; ".join("p %+.4f: %+.4e / %+.4e" % (a, b, c) for a, b, c in zip(P[o], dpdv, g3)))
            except Exception as ex:  # noqa: BLE001
                print("    %-32s ### IL FIT NON CONVERGE: %s" % (nome, ex))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("calcio", "noto_a", "lettura"))
    ap.add_argument("--k", type=float, choices=KK)
    a = ap.parse_args(argv)
    if a.cosa == "calcio":
        return calcio(a.k)
    return {"noto_a": noto_a, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
