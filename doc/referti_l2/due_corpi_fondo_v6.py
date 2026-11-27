# -*- coding: utf-8 -*-
r"""**[M2034-B] LA COPPIA COL VUOTO FRESCO: psi E chi DAL GIRO 3 DI [M0414], phi = c(t) phi_v** *(DECISIONE DI LUCA, 2026-11-26 20:34, dalla posta; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-septendecies`; `due_corpi_fondo_v4.py` e `_v5` sono usati e non si riscrivono)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v6.py noto > doc/referti_l2/due_corpi_fondo_v6_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/due_corpi_fondo_v6.py corsa --quale d1      (d1 due chi on, d2 due chi off, d3 uno chi on; dalla coda)

**La v4, con `costruisci` sostituita in memoria:** `psi` e chi da `M0414/puntofisso_accoppiato/giro_3/partenza_giro_4.npz`; il secondo corpo traslato di `(+24, +48)`; `chi_A + chi_B - chi_fondo` *(la media di chi a `d > 45`)*; **`pi = 0`**; **`phi = c(t) phi_v` FRESCO dappertutto** *(F; `c = bordo.c_di(t, tab_c, K, omega)`)*; `theta_a = 0`; i campi `porto.campi`. **Il tick `t`** dello stato del giro 3 dalla catena *(`t_catena`: la tenuta `t0 + k`, i `k_b` della v2 e della v3b, i `6000` di [M0137] e [M0414])*. Le uscite in `M2034/coppia/<d>/`.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v4 as V4  # noqa: E402

D, F1, PF, CT, CV2, GD = V4.D, V4.F1, V4.PF, V4.CT, V4.CV2, V4.GD
STATO_G3 = os.path.join(PF.CTRL, "M0414", "puntofisso_accoppiato", "giro_3", "partenza_giro_4.npz")
TENUTA = os.path.join(PF.CTRL, "M1658", "tenuta", "L-1_proiezione_K", "stato_003000.npz")
V4.BASE = os.path.join(PF.CTRL, "M2034", "coppia")
FASE = {"c": True}          # ### F: phi = c(t) phi_v; per V3 anche a fase 0 (c = 1)


def t_catena():
    """### `(t, righe)`: il tick assoluto del vuoto di `STATO_G3`, e di `PARTENZA_G4` e della tenuta, dalla catena dei giri."""
    with np.load(TENUTA) as z:
        m = json.loads(str(z["meta"]))
    t = int(m["t0"]) + int(m["k"])
    righe = [("la tenuta (t0 + k)", t)]
    T = {"tenuta": t}
    B = os.path.join(PF.CTRL, "M1330")
    for g in (1, 2):
        kb = int(json.load(open(os.path.join(B, "puntofisso_v2", "giro_%d" % g, "giro.json"), encoding="utf-8"))["periodo"][1])
        t += kb
        righe.append(("v2 giro %d: k_b %d" % (g, kb), t))
    t += 6000
    righe.append(("v2 giro 3: k 6000 (la partenza della v3b)", t))
    for g in (1, 2):
        kb = int(json.load(open(os.path.join(B, "puntofisso_v3b", "giro_%d" % g, "periodo_v3b.json"), encoding="utf-8"))["finestra"][1])
        t += kb
        righe.append(("v3b giro %d: k_b %d" % (g, kb), t))
    t += 6000
    righe.append(("v3b giro 3: k 6000 = PARTENZA_G4", t))
    T["G4"] = t
    for nome in ("M0137 giro 1", "M0137 giro 2", "M0137 giro 3 (k 6000)", "M0414 giro 1", "M0414 giro 2", "M0414 giro 3: partenza_giro_4"):
        t += 6000
        righe.append((nome, t))
    T["G3"] = t
    return T, righe


def c_di(Z, t):
    from solitone import bordo as BO
    return complex(BO.c_di(int(t), Z["tab_c"], Z["K"], Z["omega"]))


def costruisci(Z, quanti, da):
    """### lo stato del tick `0`: `(C, info, X)`."""
    from solitone import porto as PO
    from solitone import toro as TO
    MT = GD.TC.moduli()[0]
    F1.OGGETTO = da
    C, info, dxy, _forma, _X = F1.FS.carica(Z, "K", 3000)
    st, mot = Z["st"], Z["mot"]
    nodo, n, L = np.asarray(mot.inc.nodo), Z["n"], Z["L"]
    with np.load(da) as z:
        chiA = z["chi"].copy()
    T, _r = t_catena()
    c = c_di(Z, T["G3"]) if FASE["c"] else complex(1.0, 0.0)
    info = dict(info, t=T["G3"], c=[c.real, c.imag], fase="c(t)" if FASE["c"] else "0")
    d = np.hypot(dxy[:, 0], dxy[:, 1])
    if quanti == 2:
        psiA = st["psi_h"].copy()
        src, dst = D.trasla_idx(Z, V4.TRASLA)
        psiB = np.zeros_like(psiA)
        psiB[dst] = psiA[src]
        st["psi_h"][...] = psiA + psiB
        v = np.arange(n)
        Tv = ((v // L + V4.TRASLA[0]) % L) * L + (v % L + V4.TRASLA[1]) % L
        cf = float(chiA[d > V4.R_FONDO].mean())
        chiB = np.empty_like(chiA)
        chiB[Tv] = chiA[v]
        chi = chiA + chiB - cf
        info.update(trasla=list(V4.TRASLA), chi_fondo=cf, masse=[float(np.sum(np.abs(psiA) ** 2)), float(np.sum(np.abs(psiB) ** 2))])
    else:
        chi = chiA
    st["phi_h"][...] = c * np.asarray(Z["phi_v"])
    C = PO.campi(Z, MT.rho_c_assoluto(), MT.PB.E_DECISO)
    rho = np.bincount(nodo, weights=np.sum(np.abs(st["psi_h"]) ** 2, axis=1), minlength=n)
    b = TO.centro(rho, Z["m1"], Z["m2"], L)[:2]
    info["centro_coppia"] = [float(b[0]), float(b[1])]
    X = {"chi": np.array(chi, float), "pi": np.zeros(n), "theta_a": np.zeros(mot.inc.m)}
    return C, info, X


V4.costruisci = costruisci


def omega_breve(fase_c, ticks):
    """### d3' per `ticks` tick, chi acceso, `phi` fresco con la fase data: `omega` medio dell'oggetto."""
    FASE["c"] = fase_c
    om = []
    with GD.TC.scena() as Z:
        mot = Z["mot"]
        Lp = CT.Laplaciano(mot)
        C, info, X = costruisci(Z, 1, STATO_G3)
        P, Pon, m0 = D.parametri(Z, C, True)

        def dopo(kk, prima):
            om.append(float(-np.angle(np.vdot(prima, Z["st"]["psi_h"]))))
        D.ciclo(Z, C, P, Lp, X, ticks, dopo)
        Z["metti"]()
    FASE["c"] = True
    return float(np.mean(om)), info


def noto():
    D.avvia()
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "due_corpi_fondo_v4.py"))
    _presidio.avvia(__file__)
    PF.controlla(STATO_G3)
    print("=" * 130)
    print("[M2034-B] I CASI NOTI DELLA COPPIA COL VUOTO FRESCO (la carta sez. 3-septendecies): G, T, K2, V0, V2, V3")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    T, righe = t_catena()
    print("  LA CATENA DEL TICK t: " + "; ".join("%s -> t %d" % r for r in righe))
    with GD.TC.scena() as Z:
        L, n = Z["L"], Z["n"]
        nodo = np.asarray(Z["mot"].inc.nodo)
        pv = np.asarray(Z["phi_v"]).copy()
        # ### (V0): la fase di c(t) contro il fit sui nodi lontani, sulla tenuta e su PARTENZA_G4
        for nome, f, t in (("la tenuta", TENUTA, T["tenuta"]), ("PARTENZA_G4", D.G4.PARTENZA_G4, T["G4"])):
            with np.load(f) as z:
                ph, ps = z["phi_h"], z["psi_h"]
            r = np.bincount(nodo, weights=np.sum(np.abs(ps) ** 2, axis=1), minlength=n)
            b = TO.centro(r, Z["m1"], Z["m2"], L)[:2]
            dd = np.hypot(*np.asarray(TO.scarti(Z["m1"], Z["m2"], b[0], b[1], L))[:, :2].T)
            lon = (dd > V4.R_FONDO)[nodo]
            a = complex(np.sum(np.conj(pv[lon]) * ph[lon]) / np.sum(np.abs(pv[lon]) ** 2))
            c = c_di(Z, t)
            dfa = abs(math.remainder(math.atan2(a.imag, a.real) - math.atan2(c.imag, c.real), 2 * math.pi))
            esito("(V0) %s (t %d): la fase di c(t) = la fase del fit sul vuoto lontano entro 0.05 rad" % (nome, t), dfa < 0.05, "arg a %+.4f (|a| %.4f), arg c %+.4f: |d| %.4f" % (math.atan2(a.imag, a.real), abs(a), math.atan2(c.imag, c.real), dfa))
        # ### G, T, K2, V2
        v = np.arange(n)
        Tv = ((v // L + V4.TRASLA[0]) % L) * L + (v % L + V4.TRASLA[1]) % L
        A1, A2 = TO.vettori()
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        dm = np.stack([((m1[Tv] - m1 + 0.5 * L) % L) - 0.5 * L, ((m2[Tv] - m2 + 0.5 * L) % L) - 0.5 * L], axis=1)
        sp = dm[:, :1] * A1 + dm[:, 1:] * A2
        dx, dy = float(np.max(np.abs(sp[:, 0]))), float(np.max(np.abs(sp[:, 1] - 48.0 * math.sqrt(3.0) / 2.0)))
        esito("(G) lo spostamento di ogni nodo: |dx| < 1e-9 e |dy - 48 sqrt3/2| < 1e-9", dx < 1e-9 and dy < 1e-9, "%.1e %.1e" % (dx, dy))
        imp = {}
        for q in ("d1", "d2"):
            C, info, X = costruisci(Z, 2, STATO_G3)
            P, Pon, m0 = D.parametri(Z, C, V4.QUALI[q][1])
            imp[q] = GD.impronta(Z, C, X)
            if q == "d1":
                ms = info["masse"]
                esito("(T) le masse dei due corpi uguali entro 1e-9 relativo", abs(ms[0] / ms[1] - 1.0) < 1e-9, "%r" % ms)
                cc = complex(*info["c"])
                esito("(V2) phi composto = c(t) phi_v AL BIT, dappertutto", np.array_equal(Z["st"]["phi_h"], cc * pv), "t %d, c %+.6f%+.6fi" % (info["t"], cc.real, cc.imag))
                print("  la coppia: chi_fondo %+.4f; max|chi| %.3f; il centro %s; P on %r; m0 %.6e" % (info["chi_fondo"], float(np.max(np.abs(X["chi"]))), info["centro_coppia"], Pon, m0))
            Z["metti"]()
        esito("(K2) d2' a k 0 = d1' a k 0 AL BIT (l'impronta)", imp["d1"] == imp["d2"], "%s %s" % (imp["d1"][:12], imp["d2"][:12]))
    # ### (V3): d3' 250 tick a fase 0 e a fase c(t)
    t1 = time.time()
    o0, i0 = omega_breve(False, 250)
    oc, ic = omega_breve(True, 250)
    dlt = abs(oc - o0)
    print("  (V3) d3', 250 tick: omega medio a fase 0 %+.9f, a fase c(t) %+.9f; |d| %.3e (%.0f s): %s" % (o0, oc, dlt, time.time() - t1, "LA FASE NON CONTA (entro 1e-6)" if dlt <= 1e-6 else "### LA FASE CONTA (oltre 1e-6): si dichiara; si usa c(t) phi_v"))
    fall = [k for k, v_ in OK.items() if not v_]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa"))
    ap.add_argument("--quale", choices=tuple(V4.QUALI))
    a = ap.parse_args(argv)
    if a.cosa == "noto":
        return noto()
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "due_corpi_fondo_v4.py"))
    _presidio.avvia(__file__)
    return V4.corsa(a.quale, STATO_G3)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
