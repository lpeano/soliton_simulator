# -*- coding: utf-8 -*-
r"""**[M0908-K] LA CADUTA LIBERA: UN MATTONE SOLO IN `chi` IMPOSTO E FERMO -- LA SCENA, L'AMPIEZZA, IL CASO NOTO, LA CORSA** *(il mandato di Luca [M0908] `2026-11-22` `09:08`; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `2`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_libera.py caso_noto > doc/referti_l2/caduta_libera_caso_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/caduta_libera.py corsa --var V1 --fino 2000 --registro <voce>      (V0, V1, V2, V3, V4, V1m)

**La scena** *(le righe di `gravita_due_corpi.prepara_coppia` con UN francobollo)*: S162, `g_e = 0`, il vuoto fresco a `G2.T0`, `L162_MGU_03000` sul nodo buono piu' vicino a `(L/2, L/2)`, `porto.campi`.
**`chi` IMPOSTO e FERMO** *(la carta sez. `2.1`: lungo `(1, 0)` un seno di periodo `L` non sta su questo toro; lungo `(0, 1)` ci sta un periodo intero `L_y = L sqrt(3)/2`)*: `chi = segno A sin(2 pi (y - y_c)/L_y)`, `y = m2 sqrt(3)/2`, `y_c` la `y` del baricentro di `rho` a `k 0`; `N = exp(-kappa chi)`, `kappa = chi_parametri_v2.KAPPA`; **`A = G20 L_y / (2 pi kappa)`**, `G20 = |N(21) - N(19)|/2` dalle medie sugli anelli dello stato `k 3000` di `chi-mattone-v2`.
**Il tick:** `caduta_segno_v2.tick_var` *(le righe di `chi_tick_v2.tick_chi_v2` senza `chi`)*. **Le varianti:** V0 `N = 1`; V1 `cs = s N` + la fase (a); V2 solo `cs`; V3 solo la fase; V4 `cs` + la fase col segno opposto; V1m V1 con `chi -> -chi`.
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
import chi_parametri_v2 as CP2  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import gravita_due_corpi as GD  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "caduta")
MATTONE_CHI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "mattone_v2", "stato_03000.npz")
VARIANTI = {"V0": (False, False, 0, 0.0), "V1": (True, True, +1, 1.0), "V2": (True, True, 0, 1.0), "V3": (True, False, +1, 1.0),
            "V4": (True, True, -1, 1.0), "V1m": (True, True, +1, -1.0)}       # ### (chi acceso, cs = s N, il segno della fase (a), il segno di chi)
OGNI_STATO = 250
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def ampiezza():
    """### `G20` dallo stato `k 3000` di `chi-mattone-v2` *(lo sha1 controllato)*: `(G20, info)`."""
    from solitone import toro as TO
    assert open(MATTONE_CHI + ".sha1", encoding="utf-8").read().split()[0] == sha1(MATTONE_CHI), "lo sha1 dello stato del mattone con chi NON coincide: FERMO"
    with np.load(MATTONE_CHI) as d:
        chi = d["chi"].copy()
        meta = json.loads(str(d["meta"]))
    n = chi.size
    L = int(round(math.sqrt(n)))
    assert L * L == n
    kappa = float(meta["parametri"]["kappa"])
    assert kappa == CP2.KAPPA, "kappa del meta %r diverso da chi_parametri_v2.KAPPA %r: FERMO" % (kappa, CP2.KAPPA)
    v = np.arange(n)
    c = meta["centro"]
    dxy = TO.scarti(v // L, v % L, c[0], c[1], L)[:, :2]
    r = np.hypot(dxy[:, 0], dxy[:, 1])
    N = np.exp(-kappa * chi)
    anello = {r0: float(N[np.abs(r - r0) < 0.5].mean()) for r0 in (19, 20, 21)}
    G20 = abs(anello[21] - anello[19]) / 2.0
    r_max = float(r[int(np.argmax(chi))])
    return G20, {"file": MATTONE_CHI, "k": int(meta["k"]), "L": L, "centro": c, "kappa": kappa, "N_anelli": anello, "G20": G20, "r_del_massimo_di_chi": r_max,
                 "N_centro": float(N[int(np.argmin(r))]), "chi_max": float(chi.max())}


def centro_buono(fr, L):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    tgt = (0.5 * L, 0.5 * L)
    best = None
    for n1 in range(int(tgt[0]) - 3, int(tgt[0]) + 4):
        for n2 in range(int(tgt[1]) - 3, int(tgt[1]) + 4):
            if (n1 - fr["centro"][0]) % 3 or (n2 - fr["centro"][1]) % 3:
                continue
            p = (n1 - tgt[0]) * np.asarray(A1, float) + (n2 - tgt[1]) * np.asarray(A2, float)
            dd = float(np.hypot(p[0], p[1]))
            if best is None or dd < best[0]:
                best = (dd, [n1, n2])
    return best[1]


def prepara(Z):
    """### lo stato del tick `0`: UN francobollo, SENZA bordo; `(C, info)`."""
    from solitone import toro as TO
    MT, _MTR, _T1, _TRU, TV, PO = TC.moduli()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    st, L = Z["st"], Z["L"]
    fr = TV.francobollo_L162(0)
    c = centro_buono(fr, L)
    Z["g_e"] = np.zeros_like(Z["g_e"])
    MT.vuoto_fresco(Z, t0)
    MT.incolla(Z, fr, c, True)
    C = PO.campi(Z, rho_c, e)
    nodo = np.asarray(Z["mot"].inc.nodo)
    rho = np.bincount(nodo, weights=np.sum(np.abs(st["psi_h"]) ** 2, axis=1), minlength=Z["n"])
    dxy = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2]
    bari = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
    return C, {"centro": c, "bari_k0": bari.tolist(), "y_c": float(c[1] * math.sqrt(3.0) / 2.0 + bari[1]), "massa": float(rho.sum()), "t0": t0}


def campo_N(Z, info, A, segno_chi):
    """### `(chi, N)` per nodo: `chi = segno A sin(2 pi (y - y_c)/L_y)`, `N = exp(-kappa chi)`."""
    L = Z["L"]
    Ly = L * math.sqrt(3.0) / 2.0
    y = np.asarray(Z["m2"], float) * math.sqrt(3.0) / 2.0
    chi = float(segno_chi) * float(A) * np.sin(2.0 * math.pi * (y - info["y_c"]) / Ly)
    return chi, np.exp(-CP2.KAPPA * chi)


def impronta(Z, C):
    h = hashlib.sha1()
    for x in Z["chiavi"]:
        h.update(np.ascontiguousarray(Z["st"][x]).tobytes())
    for a in (C.campo.A, C.campo.E):
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def parametri():
    MT = TC.moduli()[0]
    G20, ia = ampiezza()
    import s5_coppia_lapse as SL
    return G20, ia, float(SL.eps_top_tl4b()), MT


def caso_noto():
    import _presidio
    for m in ("chi_tick.py", "chi_tick_v2.py", "triangolo_chi_v4.py", "gravita_due_corpi.py", "caduta_segno_v2.py", "chi_parametri_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    G20, ia, e0, MT = parametri()
    print("=" * 130)
    print("[M0908-K] IL CASO NOTO DELLA CADUTA LIBERA: 50 tick; V1 con A = 0 contro V0, V0 contro il tick U (gravita_due_corpi.tick_U), AL BIT; DEVE FALLIRE V1 con A vero")
    print("=" * 130)
    print("### L'AMPIEZZA dallo stato %s (k %d, L %d): il centro del meta %s, kappa %r; N medio sugli anelli r 19, 20, 21: %.12f %.12f %.12f; G20 = %.6e; N al centro %.10f; il massimo di chi %.6f a r %.3f dal centro" % (
        ia["file"], ia["k"], ia["L"], ["%.3f" % x for x in ia["centro"]], ia["kappa"], ia["N_anelli"][19], ia["N_anelli"][20], ia["N_anelli"][21], G20, ia["N_centro"], ia["chi_max"], ia["r_del_massimo_di_chi"]))
    esito("K: il massimo di chi dello stato del mattone con chi a meno di 3 dal centro del meta (la convenzione delle coordinate)", ia["r_del_massimo_di_chi"] < 3.0, "(r %.3f)" % ia["r_del_massimo_di_chi"])
    out = {}
    with TC.scena() as Z:
        mot = Z["mot"]
        L = Z["L"]
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        for nome in ("V0", "U", "V1 A = 0", "V1 A vero"):
            C, info = prepara(Z)
            s = float(Z["s"])
            chi, N = campo_N(Z, info, 0.0 if nome == "V1 A = 0" else A, 1.0)
            if nome == "V0":
                N = np.ones(mot.inc.n)
            if nome == "V1 A vero":
                print("### la scena: il centro %s, il baricentro di rho a k 0 (dal centro) %s, y_c %.6f, la massa %.6f; L_y %.4f; A %.6e; N da %.10f a %.10f; |dN/dy| allo zero (kappa A 2 pi/L_y) %.6e" % (
                    info["centro"], ["%.4f" % x for x in info["bari_k0"]], info["y_c"], info["massa"], Ly, A, float(N.min()), float(N.max()), CP2.KAPPA * A * 2.0 * math.pi / Ly))
            print("### %s: l'impronta di partenza %s" % (nome, impronta(Z, C)[:12]))
            for _t in range(50):
                if nome == "U":
                    GD.tick_U(Z["z"], C.campo, s)
                elif nome == "V0":
                    CS.tick_var(Z["z"], C.campo, s, e0, N, False, 0)
                else:
                    CS.tick_var(Z["z"], C.campo, s, e0, N, True, +1)
            out[nome] = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy())
            Z["metti"]()

    def diverse(a, b):
        return [x for x in a[0] if not np.array_equal(a[0][x], b[0][x])] + [q for q, p, r in (("A", a[1], b[1]), ("E", a[2], b[2])) if not np.array_equal(p, r)]
    d0 = diverse(out["V1 A = 0"], out["V0"])
    dU = diverse(out["V0"], out["U"])
    d1 = diverse(out["V1 A vero"], out["V0"])
    print("### V1 A = 0 contro V0: %s; V0 contro U: %s; V1 A vero contro V0: le chiavi diverse %s" % (d0 or "AL BIT", dU or "AL BIT", d1))
    esito("K: V1 con A = 0 = V0 AL BIT dopo 50 tick (ogni chiave, A, E)", not d0)
    esito("K: V0 = il tick U di gravita_due_corpi AL BIT dopo 50 tick", not dU)
    esito("K DEVE FALLIRE: V1 con A vero diversa da V0 dopo 50 tick (psi_h)", "psi_h" in d1)
    print("-" * 130)
    print("ESITO: %d/%d" % (sum(ok for _c, ok in ESITI), len(ESITI)))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def corsa(var, k_fino, reg):
    import _presidio
    for m in ("chi_tick.py", "chi_tick_v2.py", "triangolo_chi_v4.py", "gravita_due_corpi.py", "caduta_segno_v2.py", "chi_parametri_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    from solitone import _registro_corse as RC
    acceso, cs_N, segno, segno_chi = VARIANTI[var]
    G20, ia, e0, MT = parametri()
    d_out = os.path.join(BASE, var)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot = Z["mot"]
        L = Z["L"]
        Ly = L * math.sqrt(3.0) / 2.0
        A = G20 * Ly / (2.0 * math.pi * CP2.KAPPA)
        C, info = prepara(Z)
        s = float(Z["s"])
        chi, N = campo_N(Z, info, A if acceso else 0.0, segno_chi)
        if not acceso:
            N = np.ones(mot.inc.n)
        meta = dict(info, variante=var, acceso=acceso, cs_N=cs_N, segno_fase=segno, segno_chi=segno_chi, A=A, G20=G20, L_y=Ly, kappa=CP2.KAPPA, s=s, e0=e0, ampiezza=dict(ia, N_anelli={str(k): v for k, v in ia["N_anelli"].items()}))
        print("### %s: il centro %s, y_c %.6f, A %.6e (G20 %.6e), kappa %r, s %r, e0 %r; cs %s, la fase (a) %+d, chi x %+g; N da %.10f a %.10f; L'IMPRONTA DI PARTENZA %s; gli stati in %s" % (
            var, info["centro"], info["y_c"], A, G20, CP2.KAPPA, s, e0, "s N" if cs_N else "s", segno, segno_chi, float(N.min()), float(N.max()), impronta(Z, C), d_out))
        sys.stdout.flush()

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, chi=chi, N=N)
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            h = sha1(fz)
            with open(fz + ".sha1", "w", encoding="utf-8") as fh:
                fh.write(h + "\n")
            return h

        print("    [stato] k 0 sha1 %s" % salva(0)[:8])
        t1 = t_tappa = time.time()
        for k in range(1, k_fino + 1):
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % OGNI_STATO == 0 or k == k_fino:
                print("    [stato] k %d sha1 %s  (%.0f s)" % (k, salva(k)[:8], time.time() - t1))
                sys.stdout.flush()
            if reg and time.time() - t_tappa >= 3600.0:
                RC.tappa(reg, "k %d; %.3f s per tick" % (k, (time.time() - t1) / k))
                t_tappa = time.time()
        Z["metti"]()
    print("### %d tick in %.0f s (%.3f s per tick)" % (k_fino, time.time() - t1, (time.time() - t1) / k_fino))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("caso_noto")
    c = sub.add_parser("corsa")
    c.add_argument("--var", choices=tuple(VARIANTI), required=True)
    c.add_argument("--fino", type=int, required=True)
    c.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cmd == "caso_noto":
        return caso_noto()
    return corsa(x.var, x.fino, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
