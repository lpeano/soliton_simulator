# -*- coding: utf-8 -*-
r"""**[M1253-G] IL GALLEGGIAMENTO: MENTRE IL MATTONE VA VIA, IL VUOTO ATTORNO CADE?** *(la richiesta di Luca delle `12:53`; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `5`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/galleggiamento.py vuoto --var Vg --fino 2000      (il vuoto F3 PURO col gradiente di V1; gli stati in CHI/caduta/vuoto_Vg)
    E:\python\py3132\python.exe doc/referti_l2/galleggiamento.py vuoto --var N1 --fino 500       (il vuoto F3 PURO a N = 1: il deve-fallire)
    E:\python\py3132\python.exe doc/referti_l2/galleggiamento.py lettura > doc/referti_l2/galleggiamento.txt

**Il vuoto puro** *(le righe di `caduta_libera.corsa` senza il francobollo: la scena, `y_c` dal mattone di `k 0`, poi `mattone.vuoto_fresco`, `porto.campi`; il tick `caduta_segno_v2.tick_var` con `cs = s N`)*: **`2000` tick invece dei `500` del mandato**, per avere il riferimento a ogni stato della caduta *(i `500` ci stanno dentro: dichiarato)*. **La lettura** *(la carta sez. `5.2`)*: il centro FISSO = il baricentro del mattone a `k 0`; il disco `r < 40` e l'anello `25-40`; **(a)** il baricentro `y` del disturbo `w = |phi - phi0|^2` *(`porto.dphi_nodi`)* e di `w' = |phi - phi_p|^2` *(`phi_p` il vuoto puro con lo stesso `cs` allo stesso `k`)*, e dell'energia del solo `phi` *(`_libro_dei_conti.conti_per_nodo` su una copia con `psi = 0`, meno il vuoto F3 puro)*; **(b)** `P_m = somma Jy` *(lo strumento di [M0908-M])*, `M v_bari`, `P_v = somma J_phi_y` *(il gemello con `spostamento_scalare`)*; **(c)** la lettura.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import chi_tick as CT  # noqa: E402
import chi_parametri_v2 as CP2  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402

ORDINE = ("V0", "V1", "V2", "V3", "V4", "V1m")
KS = tuple(range(0, 2001, 250))
R_DISCO, R_IN = 40.0, 25.0                      # ### Luca: il disco di raggio 40, l'anello 25-40
PURO = {"V0": "N1", "V1": "Vg", "V2": "Vg", "V3": "N1", "V4": "Vg", "V1m": "Vgm"}     # ### la carta 5.2: il vuoto puro con lo stesso cs
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "gravita_due_corpi_misure.py", "triangolo_chi_v4.py", "chi_tick.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def vuoto(var, k_fino):
    """### il vuoto F3 PURO: `Vg` col gradiente di V1 (`chi x +1`), `N1` a `N = 1`."""
    avvia()
    G20, ia, e0, MT = CL.parametri()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    PO = TC.moduli()[5]
    d_out = os.path.join(CL.BASE, "vuoto_" + var)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        _C, info = CL.prepara(Z)                                            # ### y_c dal mattone di k 0
        MT.vuoto_fresco(Z, t0)
        C = PO.campi(Z, rho_c, e)
        s = float(Z["s"])
        chi, N = CL.campo_N(Z, info, A if var == "Vg" else 0.0, 1.0)
        if var == "N1":
            N = np.ones(n)
        print("### il vuoto puro %s: y_c %.6f, A %.6e, N da %.10f a %.10f; max|psi| %.1e; l'impronta di partenza %s" % (var, info["y_c"], A, float(N.min()), float(N.max()), float(np.max(np.abs(Z["st"]["psi_h"]))), CL.impronta(Z, C)[:12]))

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, chi=chi, N=N)
            np.savez(fz, meta=np.array(json.dumps(dict(info, variante=var, A=A, s=s, e0=e0, k=k))), **dati)
            h = CL.sha1(fz)
            open(fz + ".sha1", "w", encoding="utf-8").write(h + "\n")
            return h
        print("    [stato] k 0 sha1 %s" % salva(0)[:8])
        t1 = time.time()
        for k in range(1, k_fino + 1):
            CS.tick_var(Z["z"], C.campo, s, e0, N, True, +1)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % 250 == 0 or k == k_fino:
                print("    [stato] k %d sha1 %s  (%.0f s)" % (k, salva(k)[:8], time.time() - t1))
                sys.stdout.flush()
        Z["metti"]()
    return 0


def baricentro_y(w, y, m):
    s = float(w[m].sum())
    return float((w[m] * y[m]).sum() / s) if s > 0 else float("nan")


def lettura():
    avvia()
    import _libro_dei_conti as LC
    import _u1_prototipo as U1
    import _vuoto_vivo_B as VB
    from solitone import bordo as BO
    from solitone import porto as POR
    from solitone import toro as TO
    MT = TC.moduli()[0]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    print("=" * 130)
    print("[M1253-G] IL GALLEGGIAMENTO (la carta sez. 5.2): il disco r < %g e l'anello %g-%g dal baricentro del mattone a k 0; gli stati 0 ... 2000" % (R_DISCO, R_IN, R_DISCO))
    print("=" * 130)
    R = {}
    with TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        A1, A2 = TO.vettori()
        vett = np.stack([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2], np.asarray(A1, float)[:2] + np.asarray(A2, float)[:2]])
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        spm, spv = mot.operatori["spostamento_trasporto"], mot.operatori["spostamento_scalare"]
        cs0 = mot.cs
        X0, meta0 = GM.leggi(os.path.join(CL.BASE, "V0", "stato_000000.npz"))
        c = meta0["centro"]
        dxy0 = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2]
        rho0 = np.bincount(nodo, weights=np.sum(np.abs(X0["psi_h"]) ** 2, axis=1), minlength=n)
        b0 = (dxy0 * rho0[:, None]).sum(axis=0) / rho0.sum()
        dxy = dxy0 - b0
        y = dxy[:, 1]
        r = np.hypot(dxy[:, 0], dxy[:, 1])
        disco, anello = r < R_DISCO, (r >= R_IN) & (r < R_DISCO)
        print("### il centro fisso: il nodo %s + il baricentro di k 0 %s; i nodi del disco %d, dell'anello %d" % (c, b0.tolist(), int(disco.sum()), int(anello.sum())))
        cache_E0 = {}

        def E_solo_phi(st_dato, k):
            """### l'energia del solo phi per nodo: conti_per_nodo su una copia con psi = 0, meno il vuoto F3 puro allo stesso tick."""
            cp = {x: st_dato[x].copy() for x in Z["chiavi"]}
            cp["psi_h"][...] = 0.0
            if "psi" in cp:
                cp["psi"][...] = 0.0
            Z["metti"](cp)
            E = LC.conti_per_nodo(Z["z"]["inc"], mot, Z["st"], Z["e_K"], VB.LAM_ZERO, Z["par"])["tot"].copy()
            if k not in cache_E0:
                MT.vuoto_fresco(Z, t0 + k)
                cache_E0[k] = LC.conti_per_nodo(Z["z"]["inc"], mot, Z["st"], Z["e_K"], VB.LAM_ZERO, Z["par"])["tot"].copy()
            Z["metti"]()
            return E - cache_E0[k]

        def flussi(X, cs, segno, e0, N):
            Z["metti"]({x: X[x] for x in Z["chiavi"]})
            cam.A[...] = X["campo_A"]
            mot.cs = cs
            mot.lambda_c = None
            if segno:
                CT.fase_a(mot, Z["st"], float(segno) * e0, N)
            U1.scrivi_U(mot, cam)
            mm = cam.m
            base = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            prima = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
            spm(Z["st"], Z["par"], 0.5)
            Jm = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
            Z["metti"](base)
            pv = np.abs(Z["st"]["phi_h"].reshape(mm, 2)[:, 0]) ** 2
            spv(Z["st"], Z["par"], 0.5)
            Jv = np.abs(Z["st"]["phi_h"].reshape(mm, 2)[:, 0]) ** 2 - pv
            Z["metti"]()
            f = lambda J: (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)
            return f(Jm), f(Jv)

        for nome in ORDINE + ("puro Vg", "puro N1"):
            if nome.startswith("puro"):
                d = os.path.join(CL.BASE, "vuoto_" + nome.split()[1])
                ks = [k for k in KS if os.path.exists(os.path.join(d, "stato_%06d.npz.sha1" % k))]
            else:
                d = os.path.join(CL.BASE, nome)
                ks = list(KS)
            if not ks:
                print("### %s: nessuno stato: saltato" % nome)
                continue
            print("-" * 130)
            serie = {q: [] for q in ("yD", "yDp", "yDa", "yDpa", "yE", "yEa", "Ev", "Pm", "Mv", "Pv", "yb", "M")}
            for k in ks:
                X, meta = GM.leggi(os.path.join(d, "stato_%06d.npz" % k))
                N = X["N"]
                s, e0 = float(meta["s"]), float(meta["e0"])
                cs_N = bool(meta.get("cs_N", True))
                segno = int(meta.get("segno_fase", 1))
                cs = s * N if cs_N else np.full(n, s)
                Z["metti"]({x: X[x] for x in Z["chiavi"]})
                w = POR.dphi_nodi(Z, t0 + k) ** 2
                Z["metti"]()
                pk = PURO.get(nome)
                fp = os.path.join(CL.BASE, "vuoto_" + (pk or ""), "stato_%06d.npz" % k)
                if pk and os.path.exists(fp + ".sha1"):
                    Xp, _mp = GM.leggi(fp)
                    if pk == "Vgm":
                        Xp = None
                else:
                    Xp = None
                if Xp is not None:
                    dp = (X["phi_h"] - Xp["phi_h"])
                    wp = np.sqrt(np.sum(np.abs(dp).reshape(n * 6, -1) ** 2, axis=1))[Z["righe"]]
                    wp = np.sum(wp ** 2, axis=1)
                else:
                    wp = np.full(n, np.nan)
                rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
                Ev = E_solo_phi(X, k)
                Jm, Jv = flussi(X, cs, segno, e0, N)
                serie["yD"].append(baricentro_y(w, y, disco))
                serie["yDa"].append(baricentro_y(w, y, anello))
                serie["yDp"].append(baricentro_y(wp, y, disco) if Xp is not None else float("nan"))
                serie["yDpa"].append(baricentro_y(wp, y, anello) if Xp is not None else float("nan"))
                serie["yE"].append(baricentro_y(np.abs(Ev), y, disco))
                serie["yEa"].append(baricentro_y(np.abs(Ev), y, anello))
                serie["Ev"].append(float((Ev[disco] * y[disco]).sum()))
                serie["Pm"].append(float(Jm[:, 1].sum()))
                serie["Pv"].append(float(Jv[:, 1].sum()))
                serie["M"].append(float(rho.sum()))
                serie["yb"].append(float(((dxy * rho[:, None]).sum(axis=0) / max(rho.sum(), 1e-300))[1]) if rho.sum() > 0 else float("nan"))
                print("  %-8s k %4d: y_D (disco, anello) %+.5f %+.5f; y_D' contro il vuoto puro %+.5f %+.5f; y_E %+.5f %+.5f, somma E_v y %+.4e; P_m %+.4e, P_v %+.4e, la somma %+.4e; y del mattone %+.5f; <w> nel disco %.3e" % (
                    nome, k, serie["yD"][-1], serie["yDa"][-1], serie["yDp"][-1], serie["yDpa"][-1], serie["yE"][-1], serie["yEa"][-1], serie["Ev"][-1],
                    serie["Pm"][-1], serie["Pv"][-1], serie["Pm"][-1] + serie["Pv"][-1], serie["yb"][-1], float(w[disco].mean())))
            mot.cs = cs0
            mot.lambda_c = None
            fit = {}
            for q in ("yD", "yDa", "yDp", "yDpa", "yE", "yEa", "yb"):
                v = np.array(serie[q])
                fit[q] = GM.fit(ks, v) if len(ks) >= 4 and np.all(np.isfinite(v)) else None
            dPm, dPs = np.diff(serie["Pm"]), np.diff(np.array(serie["Pm"]) + np.array(serie["Pv"]))
            print("  %-8s il fit (a): %s; le variazioni fra stati: std di P_m %.4e, di P_m + P_v %.4e" % (
                nome, "; ".join("%s %+.4e +- %.1e" % (q, f[2], f[3]) for q, f in fit.items() if f), float(dPm.std()) if len(dPm) else float("nan"), float(dPs.std()) if len(dPs) else float("nan")))
            R[nome] = (fit, serie, float(meta.get("segno_chi", 1.0)) if not nome.startswith("puro") else 1.0)
        Z["metti"]()
    print("=" * 130)
    print("I CASI NOTI E LA LETTURA")
    print("=" * 130)
    if "V0" in R and R["V0"][0]["yD"]:
        f = R["V0"][0]["yD"]
        esito("G CASO NOTO: in V0 il baricentro del disturbo del vuoto (il disco) non accelera: entro 3 sigma", abs(f[2]) <= 3.0 * f[3], "(%+.3e +- %.1e)" % (f[2], f[3]))
    if "puro Vg" in R and R["puro Vg"][0]["yD"]:
        f = R["puro Vg"][0]["yD"]
        print("  il vuoto PURO col gradiente: il baricentro del disturbo (il disco) a %+.4e +- %.1e (%s)" % (f[2], f[3], "verso +y = VERSO N piu' basso" if f[2] > 0 else "verso -y = VIA"))
    if "puro N1" in R and R["puro N1"][0]["yD"]:
        f = R["puro N1"][0]["yD"]
        print("  il vuoto PURO a N = 1 (il deve-fallire): a %+.4e +- %.1e; <w> nel disco all'ultimo stato %.3e" % (f[2], f[3], float(np.nan)))
        esito("G DEVE FALLIRE: il vuoto puro a N = 1 non si muove (a entro 3 sigma da 0)", abs(f[2]) <= 3.0 * f[3], "(%+.3e +- %.1e)" % (f[2], f[3]))
    if "V0" in R:
        for nome in ORDINE[1:]:
            if nome not in R:
                continue
            fit, serie, sc = R[nome]
            f0 = R["V0"][0]
            out = []
            for q in ("yb", "yD", "yDa", "yDp", "yDpa", "yE", "yEa"):
                if fit.get(q) and f0.get(q):
                    da, sd = fit[q][2] - f0[q][2], math.hypot(fit[q][3], f0[q][3])
                    out.append((q, da, sd))
            print("  %-3s al netto di V0 (a, e il verso: + chi x = VERSO N piu' basso): %s" % (nome, "; ".join("%s %+.3e +- %.1e (%s%s)" % (
                q, da, sd, "VERSO" if da * sc > 0 else "VIA", "" if abs(da) > 2 * sd else ", dentro") for q, da, sd in out)))
            if nome == "V1":
                dd = {q: (da, sd) for q, da, sd in out}
                mv = dd.get("yb")
                vu = dd.get("yDp") or dd.get("yD")
                pm, pv = np.diff(serie["Pm"]).sum(), np.diff(serie["Pv"]).sum()
                gal = bool(mv and vu and mv[0] * sc < 0 and abs(mv[0]) > 2 * mv[1] and vu[0] * sc > 0 and abs(vu[0]) > 2 * vu[1] and pm * pv < 0)
                print("  (c) LA LETTURA (V1): il mattone %s; il vuoto (y_D' contro il vuoto puro, se c'e') %s; gli impulsi cumulati P_m %+.4e, P_v %+.4e (%s): %s" % (
                    "VIA" if mv and mv[0] * sc < 0 else "VERSO", ("VERSO" if vu[0] * sc > 0 else "VIA") + ("" if abs(vu[0]) > 2 * vu[1] else ", dentro l'incertezza") if vu else "-",
                    pm, pv, "segni opposti" if pm * pv < 0 else "stesso segno", "GALLEGGIA" if gal else "NON GALLEGGIA (con questi criteri)"))
    print("-" * 130)
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("vuoto")
    v.add_argument("--var", choices=("Vg", "N1"), required=True)
    v.add_argument("--fino", type=int, required=True)
    sub.add_parser("lettura")
    x = ap.parse_args(argv)
    if x.cmd == "vuoto":
        return vuoto(x.var, x.fino)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
