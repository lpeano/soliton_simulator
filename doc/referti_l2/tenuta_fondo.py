# -*- coding: utf-8 -*-
r"""**[M1658-T] 1b: LA SEMINA AL FONDO DELLA BANDA DELLA MATERIA (IL PUNTO K, `+0.2453`) E LA TENUTA** *(Luca, 2026-11-23; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-bis`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/tenuta_fondo.py casi_noti > doc/referti_l2/tenuta_fondo_casi_noti.txt
    E:\python\py3132\python.exe doc/referti_l2/tenuta_fondo.py corsa --forma L-1 --semina proiezione_K --fino 3000        (semina: stampo_K, proiezione_K)
    E:\python\py3132\python.exe doc/referti_l2/tenuta_fondo.py lettura > doc/referti_l2/tenuta_fondo.txt

**`torneo_tenuta_v2.corsa` riga per riga** *(la scena di `caduta_libera.prepara`, i `pezzi` del NUCLEO, `materia_vuoto.forma_esplicita`, `omega` per tick)* **con due semine:** **`stampo_K`** `psi(x) e^{+i K.d(x)}`; **`proiezione_K`** `Q_K Q_K^dag psi(x) e^{+i K.d(x)}` nodo per nodo, poi la norma. **K** `(B0 + B1)/3`; `Q_K` = la base QR del sottospazio di `A(K)` entro `1e-9` da quello piu' vicino a `+0.2453383`. **Gli stati ogni `250`** in `E:/soliton_simulator/controllo/M1658/tenuta/<forma>_<semina>`.
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
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import torneo_tenuta as TT  # noqa: E402
import ripresa_F0_v2 as RF  # noqa: E402

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658", "tenuta")
DIR_M1631 = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1631", "tenuta_v2")
E_FONDO = 0.2453383
GAP = (0.011870, 0.245338)
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "triangolo_chi_v4.py", "ripresa_F0_v2.py", "torneo_tenuta.py", "torneo_tenuta_v2.py", "torneo_fondo_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def risposta(Z):
    """### `R[sup]`, `d0[sup]`: le righe di `torneo_tenuta_v2.base_fondo` *(lo stato rimesso con `Z["metti"]()`)*."""
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    A_IMP = T4B.A_IMP
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    mot, st = Z["mot"], Z["st"]
    n, L, s = mot.inc.n, Z["L"], float(Z["s"])
    Z["g_e"] = np.zeros_like(Z["g_e"])
    MT.vuoto_fresco(Z, t0)
    C = PO.campi(Z, rho_c, e)
    base = {x: st[x].copy() for x in Z["chiavi"]}
    A0, E0_, U0 = C.campo.A.copy(), C.campo.E.copy(), mot.geo.U.copy()
    R = np.zeros((n, 12, 12), dtype=complex)
    for j in range(12):
        us = []
        for f in (1.0, -1.0):
            for x in Z["chiavi"]:
                st[x][...] = base[x]
            p = np.zeros((n, 12), dtype=complex)
            p[0, j] = f * A_IMP
            st["psi_h"][...] = p.reshape(st["psi_h"].shape)
            C.campo.A[...], C.campo.E[...] = A0, E0_
            mot.geo.U[...] = U0
            mot.lambda_c = None
            CS.tick_var(Z["z"], C.campo, s, e0, np.ones(n), False, 0)
            us.append(st["psi_h"].reshape(n, 12).copy())
        R[:, :, j] = (us[0] - us[1]) / (2 * A_IMP)
    d0 = TO.scarti(Z["m1"], Z["m2"], 0.0, 0.0, L)[:, :2]
    Z["metti"]()
    sup = np.nonzero(np.abs(R).reshape(n, -1).max(axis=1) > 0.0)[0]
    return R[sup], d0[sup]


def base_k(Z, dove):
    """### `(Q, E, m, kv)`: `dove = "Gamma"` *(la piu' bassa di `A(0) = R[sup].sum(axis=0)`, come `torneo_tenuta_v2.base_fondo`)* o `"K"` *(il sottospazio di `A(K)` piu' vicino a `+0.2453383`)*."""
    from solitone import toro as TO
    Rs, ds = risposta(Z)
    if dove == "Gamma":
        G = Rs.sum(axis=0)
        kv = np.zeros(2)
    else:
        A1, A2 = TO.vettori()
        Av = np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]])
        B = 2.0 * np.pi * np.linalg.inv(Av).T
        kv = (B[0] + B[1]) / 3.0
        G = np.einsum("x,xij->ij", np.exp(-1j * (ds @ kv)), Rs)
    lam, V = np.linalg.eig(G)
    E = -np.angle(lam)
    o = np.argsort(E)
    if dove == "Gamma":
        e_b = E[o[0]]
    else:
        e_b = E[int(np.argmin(np.abs(E - E_FONDO)))]
    sel = [i for i in o if abs(E[i] - e_b) < 1e-9]
    Q, _r = np.linalg.qr(V[:, sel])
    return Q, float(e_b), len(sel), kv


def semina(Z, info, sem):
    """### la semina sul mattone di `caduta_libera.prepara`: `extra` per il meta."""
    from solitone import toro as TO
    n, L = Z["mot"].inc.n, Z["L"]
    if sem == "cima":
        return {}
    psi = Z["st"]["psi_h"].reshape(n, 12)
    norma = float(np.sum(np.abs(psi) ** 2))
    if sem == "proiezione_Gamma":
        Q, Ef, m, kv = Z["_base"]
        pr = psi @ Q.conj() @ Q.T
        fr = float(np.sum(np.abs(pr) ** 2)) / norma
        pr = pr * math.sqrt(norma / float(np.sum(np.abs(pr) ** 2)))
        Z["st"]["psi_h"][...] = pr.reshape(Z["st"]["psi_h"].shape)
        return {"E_fondo": Ef, "molteplicita": m, "frazione_proiettata": fr}
    Q, Ef, m, kv = Z["_base"]
    c = info["centro"]
    d = TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2]
    fase = np.exp(1j * (d @ kv))
    y = psi * fase[:, None]
    if sem == "stampo_K":
        Z["st"]["psi_h"][...] = y.reshape(Z["st"]["psi_h"].shape)
        fr = float(np.sum(np.abs(y @ Q.conj()) ** 2)) / norma
        return {"E_K": Ef, "molteplicita": m, "k": kv.tolist(), "frazione_nel_fondo": fr}
    assert sem == "proiezione_K", sem
    pr = y @ Q.conj() @ Q.T
    fr = float(np.sum(np.abs(pr) ** 2)) / norma
    pr = pr * math.sqrt(norma / float(np.sum(np.abs(pr) ** 2)))
    Z["st"]["psi_h"][...] = pr.reshape(Z["st"]["psi_h"].shape)
    return {"E_K": Ef, "molteplicita": m, "k": kv.tolist(), "frazione_proiettata": fr}


def prepara(Z, sem):
    if sem == "proiezione_Gamma":
        Z["_base"] = base_k(Z, "Gamma")
    elif sem in ("stampo_K", "proiezione_K"):
        Z["_base"] = base_k(Z, "K")
    C, info = CL.prepara(Z)
    extra = semina(Z, info, sem)
    Z.pop("_base", None)
    return C, info, extra


def corsa(forma, sem, k_fino, d_out=None, salva_file=True, snap=None):
    avvia()
    MV, P0 = TT.nucleo()
    assert forma in MV.FORME, "la forma %r non e' nel nucleo %s" % (forma, sorted(MV.FORME))
    _G20, _ia, e0, MT = CL.parametri()
    nome = "%s_%s" % (forma, sem)
    d_out = d_out or os.path.join(DIR, nome)
    if salva_file:
        os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        n = Z["mot"].inc.n
        C, info, extra = prepara(Z, sem)
        s = float(Z["s"])
        N = np.ones(n)
        meta = dict(info, forma=forma, semina=sem, s=s, e0=e0, **extra)
        print("### %s: la forma %s, la semina %s; il centro %s; %s; l'impronta di partenza %s" % (nome, forma, sem, info["centro"], json.dumps(extra), TT.impronta(Z, C)))
        sys.stdout.flush()
        om = []

        def salva(k):
            if snap is not None:
                snap[k] = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            if not salva_file:
                return "--------"
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            h = hashlib.sha1(open(fz, "rb").read()).hexdigest()
            open(fz + ".sha1", "w", encoding="utf-8").write(h + "\n")
            np.save(os.path.join(d_out, "omega.npy"), np.array(om))
            return h
        print("    [stato] k 0 sha1 %s" % salva(0)[:8])
        t1 = time.time()
        with RF.col_nucleo(MV, P0), MV.forma_esplicita(forma):
            assert MV.ATTIVA == forma and MV.pezzi is P0
            for k in range(1, k_fino + 1):
                prima = Z["st"]["psi_h"].copy()
                CS.tick_var(Z["z"], C.campo, s, e0, N, False, 0)
                om.append(float(-np.angle(np.vdot(prima, Z["st"]["psi_h"]))))
                if k % MT.OGNI_GAUSS == 0:
                    C.residuo()
                if k % TT.OGNI_STATO == 0 or k == k_fino:
                    print("    [stato] k %d sha1 %s  omega %+.6f  (%.0f s)" % (k, salva(k)[:8], om[-1], time.time() - t1))
                    sys.stdout.flush()
        Z["metti"]()
    print("### %d tick in %.0f s (%.3f s per tick)" % (k_fino, time.time() - t1, (time.time() - t1) / max(k_fino, 1)))
    return 0


def casi_noti():
    import gravita_due_corpi_misure as GM
    print("=" * 130)
    print("[M1658-T] I CASI NOTI DI 1b (in memoria)")
    print("=" * 130)
    S1 = {}
    corsa("L-1", "cima", 250, salva_file=False, snap=S1)
    X, _m = GM.leggi(os.path.join(DIR_M1631, "L-1_cima", "stato_000250.npz"))
    dv = [x for x in S1[250] if not np.array_equal(S1[250][x], X[x])]
    esito("CN1 la semina cima con L-1 a k 250 = M1631/tenuta_v2/L-1_cima AL BIT", not dv, "diversi %s" % dv)
    S2 = {}
    corsa("L-1", "proiezione_Gamma", 0, salva_file=False, snap=S2)
    X, _m = GM.leggi(os.path.join(DIR_M1631, "L-1_proiezione_Gamma", "stato_000000.npz"))
    dv = [x for x in S2[0] if not np.array_equal(S2[0][x], X[x])]
    esito("CN2 la proiezione a Gamma a k 0 = M1631/tenuta_v2/L-1_proiezione_Gamma AL BIT", not dv, "diversi %s" % dv)
    S3 = {}
    corsa("L-1", "stampo_K", 0, salva_file=False, snap=S3)
    X, _m = GM.leggi(os.path.join(DIR_M1631, "L-1_cima", "stato_000000.npz"))
    esito("DEVE FALLIRE: stampo_K a k 0 diverso dalla cima in psi_h", not np.array_equal(S3[0]["psi_h"], X["psi_h"]), "max|d psi_h| %.3e" % float(np.max(np.abs(S3[0]["psi_h"] - X["psi_h"]))))
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0 if not fall else 1


def lettura():
    avvia()
    print("=" * 130)
    print("[M1658-T] 1b: LE TENUTE AL FONDO (K-T v2: w(3000)/w(1500) in [0.7, 1.3] e un pezzo a 3000; omega su [2500, 3000] nel gap %s)" % (GAP,))
    print("=" * 130)
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()
    R = {}
    for nome in ("L-1_stampo_K", "L-1_proiezione_K", "L0_stampo_K", "L0_proiezione_K"):
        d = os.path.join(DIR, nome)
        if not os.path.exists(os.path.join(d, "stato_003000.npz.sha1")):
            print("  %s: NON FINITA" % nome)
            continue
        _X, meta = __import__("gravita_due_corpi_misure").leggi(os.path.join(d, "stato_000000.npz"))
        om = np.load(os.path.join(d, "omega.npy"))
        print("  %s: %s" % (nome, json.dumps({x: meta[x] for x in ("E_K", "molteplicita", "frazione_proiettata", "frazione_nel_fondo") if x in meta})))
        ks = {}
        for k in range(0, 3001, 250):
            w, p, mx, M = TT.misura(os.path.join(d, "stato_%06d.npz" % k), nodo, n, L)
            ks[k] = (w, p, mx, M)
            print("    k %5d: w %.3f, i pezzi %d, il picco lisciato %.4e, la massa %.6f" % (k, w, p, mx, M))
        r = ks[3000][0] / ks[1500][0]
        regge = 0.7 <= r <= 1.3 and ks[3000][1] == 1
        o = om[2499:3000]
        om_m, om_s = float(o.mean()), float(o.std() / math.sqrt(len(o)))
        nel_gap = GAP[0] < om_m < GAP[1]
        R[nome] = (regge, nel_gap)
        print("    K-T v2: w(3000)/w(1500) %.3f, i pezzi a 3000 %d: %s; omega [1, 500] %+.7f, [2500, 3000] %+.7f +- %.1e (la deviazione %.1e): %s" % (
            r, ks[3000][1], "REGGE" if regge else "### NON REGGE", float(om[:500].mean()), om_m, om_s, float(o.std()), "NEL GAP" if nel_gap else "fuori dal gap"))
    print("-" * 130)
    for sem in ("stampo_K", "proiezione_K"):
        a, b = R.get("L-1_%s" % sem), R.get("L0_%s" % sem)
        if a is None or b is None:
            continue
        print("  %s: K3 (L-1 regge e omega nel gap): %s" % (sem, "SI'" if (a[0] and a[1]) else "NO"))
        esito("K1 il controllo negativo: L0 %s NON regge" % sem, not b[0])
    print("=" * 130)
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("casi_noti", "corsa", "lettura"))
    ap.add_argument("--forma")
    ap.add_argument("--semina", choices=("stampo_K", "proiezione_K"))
    ap.add_argument("--fino", type=int, default=3000)
    a = ap.parse_args(argv)
    if a.cosa == "casi_noti":
        return casi_noti()
    if a.cosa == "corsa":
        return corsa(a.forma, a.semina, a.fino)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
