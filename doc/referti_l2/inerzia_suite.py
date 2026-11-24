# -*- coding: utf-8 -*-
r"""**[M0149-E] LE QUATTRO INERZIE E IL COMPOSTO** *(la carta `doc/CARTA_inerzie.md`, sez. 2-4)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/inerzia_suite.py campoE --segno +1          (I2: +1, -1, 0; 1000 tick dallo stato compatto di F0)
    E:\python\py3132\python.exe doc/referti_l2/inerzia_suite.py vuoto --k 0.010 --phi congelato   (I4: k 0 o 0.010; phi congelato o libero)
    E:\python\py3132\python.exe doc/referti_l2/inerzia_suite.py triangolo --k 0.010        (S4: k 0 o 0.010)
    E:\python\py3132\python.exe doc/referti_l2/inerzia_suite.py lettura > doc/referti_l2/inerzie.txt

**La partenza:** `fondo_suite_v2.carica` *(F0 = S1 dallo stato a `k 1500` della tenuta, il campo dal file)*; **il triangolo:** `CHI/triangolo/t000/stato_029250.npz` con la stessa procedura *(`chi` tolto: il tick V0)*. **Il tick** V0 coi `pezzi` del NUCLEO *(`fondo_suite_v2._tick_loop`)*, `1000` tick, il baricentro lungo l'asse 1 ogni `10`. **I2:** `E_a = segno E0 (a . x)` AGGIUNTO a `campo.E`, `e w E0 = 2.0e-05`; il controllo che `w` sia uniforme sugli archi `a1` e che `div` del campo aggiunto sia zero. **I4:** dopo ogni tick `phi_h = c(t0 + 1500 + k) phi_v` *(congelato)*. **La lettura** *(la carta sez. 2-6)*: **I1** dai calci di `fondo_suite_v2` *(`M0133`)*; **I2** `a` dal fit quadratico su `k 200 ... 1000`, meno `a` di `E = 0`, `m_E = (segno e w E0)/a`; **I3** da `caduta_libera.txt` e `orologio_zero.omega`; **I4** `m* = k/v` *(`v` dal fit lineare di `massa_calcio.velocita`)*; **I5** da `omega` e `legge_zeri.txt`; **S4** `m*_tri` contro `m*_mattone`.
"""
import argparse
import json
import math
import os
import re
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import massa_calcio as MC  # noqa: E402
import torneo_tenuta as TT  # noqa: E402
import fondo_suite_v2 as FS  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0149")
TRIANGOLO = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "triangolo", "t000", "stato_029250.npz")
SPINTA = 2.0e-05                                   # ### la carta sez. 2: e w E0 per tick (mia)
C_BANDA, C_SOL = 0.5664, 0.588
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "massa_calcio.py", "torneo_tenuta.py", "fondo_suite_v2.py", "orologio_zero.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def carica_triangolo(Z):
    """### lo stato di t000 *(le chiavi della scena, il campo dal file; `chi` tolto)*; `dxy` dal baricentro dei tre."""
    import gravita_due_corpi_misure as GM
    import _u1_prototipo as U1
    from solitone import toro as TO
    X, meta = GM.leggi(TRIANGOLO)
    C, _info = CL.prepara(Z)
    Z["metti"]({x: X[x] for x in Z["chiavi"]})
    C.campo.A[...] = X["campo_A"]
    C.campo.E[...] = X["campo_E"]
    U1.scrivi_U(Z["mot"], C.campo)
    nodo = np.asarray(Z["mot"].inc.nodo)
    n, L = Z["n"], Z["L"]
    rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
    i = int(np.argmax(TT.lisciata(rho, L)))
    c = (int(Z["m1"][i]), int(Z["m2"][i]))
    d = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2]
    bari = (d * rho[:, None]).sum(axis=0) / rho.sum()
    info = {"centro": list(c), "bari": bari.tolist(), "massa": float(rho.sum()), "file": TRIANGOLO, "k_file": int(meta.get("k", 29250)), "forma": "S1"}
    return C, info, d - bari, "S1", X


def corsa(nome, prepara, k=0.0, segnoE=0, congelato=False):
    from solitone import bordo as BO
    avvia()
    MV, P0 = TT.nucleo()
    MT = TC.moduli()[0]
    d_out = os.path.join(BASE, nome)
    os.makedirs(d_out, exist_ok=True)
    t1 = time.time()
    with TC.scena() as Z:
        mot, n = Z["mot"], Z["n"]
        nodo = np.asarray(mot.inc.nodo)
        C, info, dxy, forma, _X = prepara(Z)
        u = MC.asse_u(1)
        extra = {}
        if k:
            Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * np.exp(1j * float(k) * (dxy @ u))[nodo][:, None]
        if segnoE:
            from solitone import toro as TO
            A1, A2 = TO.vettori()
            a1, a2 = np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]
            proj = np.array([a1 @ u, a2 @ u, (a1 + a2) @ u])
            w = np.asarray(C.campo.w, float)
            assert np.all(w[0::3] == w[0]), "w non e' uniforme sugli archi a1: FERMO"
            e = float(C.campo.e)
            E0 = SPINTA / (e * float(w[0]))
            Eext = segnoE * E0 * np.tile(proj, C.campo.n)
            dv = float(np.max(np.abs(C.campo.div(Eext))))
            assert dv <= 1e-12 * E0 * 3, "il campo aggiunto non ha divergenza nulla (%g): FERMO" % dv
            C.campo.E[...] = C.campo.E + Eext
            extra = {"E0": E0, "e": e, "w": float(w[0]), "proj": proj.tolist(), "div_max": dv}
            print("### il campo uniforme: e %r, w %r, E0 %.6e (e w E0 = %.2e per tick), le proiezioni %s, max |div| %.1e" % (e, float(w[0]), E0, e * float(w[0]) * E0, proj.tolist(), dv))
        print("### %s: %s (k %d), la forma %s; k %g; E %+d; phi %s; l'impronta %s" % (nome, info["file"], info["k_file"], forma, k, segnoE, "CONGELATO" if congelato else "libero", TT.impronta(Z, C)[:12]))
        serie = []

        def misura(kk):
            rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
            b = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
            serie.append((kk, float(b @ u), float(b[0]), float(b[1]), float(rho.sum()), float(rho.max())))

        def dopo(kk, prima):
            if congelato:
                Z["st"]["phi_h"][...] = BO.c_di(MT.G2.T0 + info["k_file"] + kk, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
            if kk % MC.OGNI == 0:
                misura(kk)
            if kk % 250 == 0:
                print("    k %d: lungo l'asse %+.5f (%.0f s)" % (kk, serie[-1][1], time.time() - t1))
                sys.stdout.flush()
        misura(0)
        FS._tick_loop(Z, C, forma, MC.K_FINO, dopo, MV, P0, np.ones(n), False)
        f = os.path.join(d_out, "serie.json")
        open(f, "w", encoding="utf-8").write(json.dumps({"nome": nome, "k": k, "segnoE": segnoE, "congelato": congelato, "serie": serie, "info": info, "extra": extra}))
        open(f + ".sha1", "w", encoding="utf-8").write(CL.sha1(f) + "\n")
        Z["metti"]()
    print("### %d tick in %.0f s" % (MC.K_FINO, time.time() - t1))
    return 0


def _leggi(base, nome):
    f = os.path.join(base, nome, "serie.json")
    if not os.path.exists(f + ".sha1"):
        return None
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CL.sha1(f)
    return json.load(open(f, encoding="utf-8"))


def _acc(serie):
    import gravita_due_corpi_misure as GM
    s = np.array(serie)
    m = s[:, 0] >= MC.K_DA_FIT
    fb = GM.fit(s[m, 0], s[m, 1])
    return fb[2], fb[3]


def lettura():
    import orologio_zero as OZ
    import orologio_mattone_v2 as OM
    avvia()
    print("=" * 130)
    print("[M0149] LE QUATTRO INERZIE E IL COMPOSTO (la carta doc/CARTA_inerzie.md)")
    print("=" * 130)
    out = {}
    # ### I1 dai calci di fondo_suite_v2 (M0133)
    r0 = _leggi(FS.BASE, "calcio_F0_k1500_%s" % MC.nome(0.0, 1))
    r1 = _leggi(FS.BASE, "calcio_F0_k1500_%s" % MC.nome(0.010, 1))
    if r0 and r1:
        v0, s0, _ = MC.velocita(r0["serie"])
        v1, s1, _ = MC.velocita(r1["serie"])
        out["I1"] = (0.010 / v1, abs(0.010 / v1) * s1 / abs(v1))
        print("  I1 la banda (il calcio, F0 compatto k 1500): v0 %+.3e +- %.1e, v %+.3e +- %.1e; m* = k/v %+.3f +- %.3f; k/(v - v0) %+.3f" % (v0, s0, v1, s1, 0.010 / v1, out["I1"][1], 0.010 / (v1 - v0)))
        print("     (dallo stato largo k 0: -19.26, massa_calcio.txt)")
    # ### I2
    rz = _leggi(BASE, "I2_E0")
    if rz:
        az, sz = _acc(rz["serie"])
        vz, svz, _ = MC.velocita(rz["serie"])
        print("  I2 il campo U: E = 0 (il caso noto): v %+.3e +- %.1e (il calcio a k 0: %s); a %+.3e +- %.1e" % (vz, svz, ("%+.3e +- %.1e" % (v0, s0)) if r0 else "?", az, sz))
        if r0:
            esito("K1 I2: E = 0 ridà la deriva v0 del calcio a k 0 entro 3 sigma", abs(vz - v0) <= 3 * math.hypot(svz, s0), "(%+.2e contro %+.2e)" % (vz, v0))
        mE = []
        acc = {}
        for sg in (+1, -1):
            r = _leggi(BASE, "I2_E%+d" % sg)
            if not r:
                continue
            a, sa = _acc(r["serie"])
            da, sda = a - az, math.hypot(sa, sz)
            acc[sg] = (da, sda)
            ex = r["extra"]
            spinta = sg * ex["e"] * ex["w"] * ex["E0"]
            mE.append((spinta / da, abs(spinta / da) * sda / abs(da)))
            print("     E %+d: a %+.3e, a - a(E = 0) %+.3e +- %.1e (%.1f sigma); la spinta %+.2e per tick; m_E = %+.3f +- %.3f" % (sg, a, da, sda, abs(da) / sda, spinta, mE[-1][0], mE[-1][1]))
        if len(acc) == 2:
            ok = acc[1][0] * acc[-1][0] < 0 and all(abs(x[0]) > 3 * x[1] for x in acc.values())
            esito("K2 I2: segni opposti sotto +E e -E, |a| > 3 sigma", ok)
            if ok:
                out["I2"] = (float(np.mean([x[0] for x in mE])), float(np.hypot(*[x[1] for x in mE])) / 2)
    # ### I3 (solo lettura)
    cad = open(os.path.join(_QUI, "caduta_libera.txt"), encoding="utf-8").read()
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    w1, wm2 = OZ.omega("N1"), OZ.omega("NmV2")
    dwdN = (wm2 - w1) / (OM.VAR["NmV2"][0] - 1.0)
    for forma, eps, chi_e in (("V3", e0, "e0 (la fase (a))"), ("V2", abs(dwdN), "|d omega/dN| (l'orologio V2: omega(NmV2) %.8f, omega(N1) %.8f)" % (wm2, w1))):
        m = re.search(r"^\s+%s\s+il baricentro\s+.*?: (VERSO|VIA) .*?\|a - a\(V0\)\| / \(c\^2 \|dN/dy\|\) = ([0-9.]+) \(c = 0\.588 s\)" % forma, cad, re.M)
        X = float(m.group(2)) * (1.0 if m.group(1) == "VERSO" else -1.0)
        mN = eps / (X * (C_SOL * 0.15) ** 2)
        out["I3_" + forma] = (mN, None)
        print("  I3 il tempo, %s: F_N per particella = %s = %.6f |dN/dy|; a/(c_sol^2 |dN/dy|) = %+.3f (%s); m_N = F_N/a = %+.3f (lo stato largo)" % (forma, chi_e, eps, X, m.group(1), mN))
    # ### I4
    rr = {}
    for nm in ("I4_congelato_k0.010", "I4_congelato_k0", "I4_libero_k0.010"):
        r = _leggi(BASE, nm)
        if r:
            rr[nm] = MC.velocita(r["serie"])
    if "I4_libero_k0.010" in rr:
        v, sv, _ = rr["I4_libero_k0.010"]
        print("  I4 il vuoto: phi libero (il caso noto): m* = k/v %+.3f" % (0.010 / v))
        if "I1" in out:
            esito("K1 I4: phi libero ridà I1 entro il 2%", abs((0.010 / v) / out["I1"][0] - 1) <= 0.02, "(%+.3f contro %+.3f)" % (0.010 / v, out["I1"][0]))
    if "I4_congelato_k0.010" in rr:
        v, sv, _ = rr["I4_congelato_k0.010"]
        mc = 0.010 / v
        vc0 = rr.get("I4_congelato_k0", (float("nan"),) * 3)[0]
        print("  I4 phi CONGELATO: v %+.3e +- %.1e; m* = k/v %+.3f; k/(v - v0) %+.3f (v0 congelato %+.3e)" % (v, sv, mc, 0.010 / (v - vc0), vc0))
        if "I4_libero_k0.010" in rr:
            ml = 0.010 / rr["I4_libero_k0.010"][0]
            dm = mc / ml - 1.0
            out["I4"] = (mc, dm)
            print("     Delta m*/m* = %+.4f: %s" % (dm, "IL VUOTO PARTECIPA all'inerzia (> 5%)" if abs(dm) > 0.05 else "il vuoto non partecipa (< 5%)"))
    # ### I5 (solo lettura)
    zeri = open(os.path.join(_QUI, "legge_zeri.txt"), encoding="utf-8").read()
    D1 = float(re.search(r"vuoto LOCALE \(misurato a ogni N\)\s+Delta\(1\) ([0-9.]+)", zeri).group(1))
    for nm, om in (("compatto", 0.625906), ("largo", 0.62644)):
        print("  I5 l'orologio, %s: omega_ass %.6f: omega/c^2 = %.2f (c_sol), %.2f (c_banda)" % (nm, om, om / (C_SOL * 0.15) ** 2, om / (C_BANDA * 0.15) ** 2))
    print("     (omega_psi - omega_phi locale) = Delta(1) %.6f (legge_zeri.txt): /c^2 = %.2f (c_sol), %.2f (c_banda)" % (D1, D1 / (C_SOL * 0.15) ** 2, D1 / (C_BANDA * 0.15) ** 2))
    out["I5"] = (0.625906 / (C_SOL * 0.15) ** 2, None)
    # ### S4
    t1_ = _leggi(BASE, "S4_tri_k0.010")
    t0_ = _leggi(BASE, "S4_tri_k0")
    if t1_ and "I1" in out:
        v, sv, _ = MC.velocita(t1_["serie"])
        vt0 = MC.velocita(t0_["serie"])[0] if t0_ else float("nan")
        mt = 0.010 / v
        rap = mt / out["I1"][0]
        print("  S4 il composto t000: v %+.3e +- %.1e; m*_tri = k/v %+.3f (k/(v - v0) %+.3f); la massa %.3f (il mattone %.3f); M*_tri/(3 M*_mattone) = %.3f: %s" % (
            v, sv, mt, 0.010 / (v - vt0), t1_["info"]["massa"], r1["info"]["massa"] if r1 else float("nan"), rap * t1_["info"]["massa"] / (3 * r1["info"]["massa"]) if r1 else float("nan"), "ADDITIVA" if 0.8 <= rap <= 1.2 else "non additiva"))
    print("-" * 130)
    print("  LA TABELLA S16 (le inerzie per particella, col segno):")
    for k_, (v_, e_) in out.items():
        print("    %-8s %+.4f %s" % (k_, v_, ("+- %.4f" % e_) if isinstance(e_, float) and k_ != "I4" else ("(Delta m*/m* %+.4f)" % e_ if k_ == "I4" else "")))
    if "I1" in out:
        for k_ in ("I2", "I3_V2", "I3_V3"):
            if k_ in out:
                print("    %s / I1 = %+.3f (entro il 15%%: %s)" % (k_, out[k_][0] / out["I1"][0], "SI'" if abs(out[k_][0] / out["I1"][0] - 1) <= 0.15 else "no"))
    print("=" * 130)
    return 0 if all(ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("campoE", "vuoto", "triangolo", "lettura"))
    ap.add_argument("--segno", type=int, choices=(-1, 0, 1))
    ap.add_argument("--k", type=float)
    ap.add_argument("--phi", choices=("congelato", "libero"))
    a = ap.parse_args(argv)
    F0 = lambda Z: FS.carica(Z, "F0", 1500)          # noqa: E731
    if a.cosa == "campoE":
        return corsa("I2_E%+d" % a.segno if a.segno else "I2_E0", F0, 0.0, a.segno, False)
    if a.cosa == "vuoto":
        return corsa("I4_%s_k%s" % (a.phi, "0.010" if a.k else "0"), F0, a.k, 0, a.phi == "congelato")
    if a.cosa == "triangolo":
        return corsa("S4_tri_k%s" % ("0.010" if a.k else "0"), carica_triangolo, a.k, 0, False)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
