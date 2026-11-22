# -*- coding: utf-8 -*-
r"""**[M1631] LE TENUTE, v2: omega PER TICK E LA SEMINA PER PROIEZIONE** *(la decisione di Luca sulla portante; la carta `doc/CARTA_torneo_nonlinearita.md`, sez. `11`; il v1 `torneo_tenuta.py` resta com'e')*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/torneo_tenuta_v2.py corsa --forma L-1 --semina cima --fino 3000      (semina: cima, proiezione_Gamma)
    E:\python\py3132\python.exe doc/referti_l2/torneo_tenuta_v2.py lettura > doc/referti_l2/torneo_tenuta_v2.txt

**La corsa:** quella di `torneo_tenuta.corsa` *(la scena di V0, i `pezzi` del NUCLEO dentro la scena, `materia_vuoto.forma_esplicita`)* **piu' `omega(k) = -arg somma_h psi_h(k-1)^* psi_h(k)` a ogni tick** *(salvata in `omega.npy` accanto agli stati)*. **La semina `proiezione_Gamma`** *(la carta sez. 11)*: `Q` = la base ortonormale *(QR)* del sottospazio della quasi-energia piu' bassa di `A(0)` *(le righe di `torneo_fondo_v2.py`: la risposta lineare di un tick attorno al vuoto, entro `1e-9`)*; `psi(x) = Q Q^dag psi_cima(x)` nodo per nodo, poi UNO scalare perche' la norma sia quella della cima; `phi` quello della cima; **stampa la frazione proiettata.** Gli stati ogni `250` in `E:\soliton_simulator\controllo\M1631\tenuta_v2\<forma>_<semina>`.

**La lettura** *(la carta sez. 10 e 11)*: per ogni corsa, a ogni stato, `w`, i pezzi sopra il `10%`, il picco lisciato, la massa *(le funzioni di `torneo_tenuta`)*; **`omega`** media su `[1, 500]`, `[1000, 1500]`, `[2500, 3000]` e **dove sta** *(i bordi dei gap da `spettro.npz` di 1a)*; **«si scioglie»** al primo stato con `w(k)/w(0)` fuori da `[0.7, 1.3]` o piu' di un pezzo; **K-T** come nella sez. 10. **Il controllo positivo:** `S1_cima` *(500 tick)*: `omega` su `[1, 500]` = `0.6264` entro `1e-3`.
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
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import ripresa_F0_v2 as RF  # noqa: E402
import torneo_tenuta as TT  # noqa: E402

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1631", "tenuta_v2")
SPETTRO = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1446", "spettro.npz")
OMEGA_F0, TOLL_OMEGA = 0.6264, 1e-3
FINESTRE = ((1, 500), (1000, 1500), (2500, 3000))
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "triangolo_chi_v4.py", "ripresa_F0_v2.py", "torneo_tenuta.py", "torneo_fondo_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def base_fondo(Z):
    """### `Q` *(12 x m)* del sottospazio piu' basso di `A(0)`: le righe di `torneo_fondo_v2.py` *(lo stato della scena rimesso con `Z["metti"]()` all'uscita)*."""
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
    Z["metti"]()
    sup = np.nonzero(np.abs(R).reshape(n, -1).max(axis=1) > 0.0)[0]
    G = R[sup].sum(axis=0)                                  # ### A(0) = somma_x R(x)
    lam, V = np.linalg.eig(G)
    E = -np.angle(lam)
    o = np.argsort(E)
    m = int(np.sum(np.abs(E - E[o[0]]) < 1e-9))
    Q, _r = np.linalg.qr(V[:, o[:m]])
    return Q, float(E[o[0]]), m


def corsa(forma, semina, k_fino):
    avvia()
    assert semina in ("cima", "proiezione_Gamma"), semina
    MV, P0 = TT.nucleo()
    assert forma in MV.FORME, "la forma %r non e' nel nucleo %s" % (forma, sorted(MV.FORME))
    _G20, _ia, e0, MT = CL.parametri()
    nome = "%s_%s" % (forma, semina)
    d_out = os.path.join(DIR, nome)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        n = Z["mot"].inc.n
        extra = {}
        if semina == "proiezione_Gamma":
            Q, Ef, m = base_fondo(Z)
        C, info = CL.prepara(Z)
        if semina == "proiezione_Gamma":
            psi = Z["st"]["psi_h"].reshape(n, 12)
            norma = float(np.sum(np.abs(psi) ** 2))
            pr = psi @ Q.conj() @ Q.T                             # ### Q Q^dag psi(x), riga per riga
            fr = float(np.sum(np.abs(pr) ** 2)) / norma
            pr = pr * math.sqrt(norma / float(np.sum(np.abs(pr) ** 2)))
            Z["st"]["psi_h"][...] = pr.reshape(Z["st"]["psi_h"].shape)
            extra = {"E_fondo": Ef, "molteplicita": m, "frazione_proiettata": fr}
            print("### la proiezione a Gamma: E del fondo %+.8f, la molteplicita' %d; la frazione proiettata %.6f; la norma %.6f -> %.6f; ### UN OGGETTO NUOVO, NON IL MATTONE SPOSTATO" % (
                Ef, m, fr, norma, float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2))))
        s = float(Z["s"])
        N = np.ones(n)
        meta = dict(info, forma=forma, semina=semina, s=s, e0=e0, **extra)
        print("### %s: la forma %s, la semina %s; il centro %s; l'impronta di partenza %s; gli stati in %s" % (nome, forma, semina, info["centro"], TT.impronta(Z, C), d_out))
        sys.stdout.flush()

        def salva(k):
            import hashlib
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            h = hashlib.sha1(open(fz, "rb").read()).hexdigest()
            open(fz + ".sha1", "w", encoding="utf-8").write(h + "\n")
            np.save(os.path.join(d_out, "omega.npy"), np.array(om))
            return h

        om = []
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
    print("### %d tick in %.0f s (%.3f s per tick)" % (k_fino, time.time() - t1, (time.time() - t1) / k_fino))
    return 0


def dove(o, gap):
    """### dove sta `omega` *(i bordi di 1a: `gap[i] = (basso, alto, larghezza, centro)`; il terzo gira sul cerchio)*."""
    top, fondo = float(gap[2][0]), float(gap[2][1])
    if abs(o - fondo) <= 1e-3:
        return "AL FONDO (la banda piatta)"
    if o > top or o < fondo:
        return "NEL GAP SOPRA"
    for i in (0, 1):
        if gap[i][0] < o < gap[i][1]:
            return "nel gap interno %d (%.4f, %.4f)" % (i + 1, gap[i][0], gap[i][1])
    return "IN BANDA"


def lettura():
    avvia()
    gap = np.load(SPETTRO)["gap"]
    print("=" * 130)
    print("[M1631] LE TENUTE v2 (la carta sez. 10, 11): w, i pezzi, il picco, la massa ogni 250; omega e dove sta; si scioglie; K-T. I gap di 1a: %s" % "; ".join("(%.6f, %.6f)" % (g[0], g[1]) for g in gap))
    print("=" * 130)
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()
    for nome in sorted(os.listdir(DIR)) if os.path.isdir(DIR) else []:
        d = os.path.join(DIR, nome)
        fs = sorted(f for f in os.listdir(d) if f.startswith("stato_") and f.endswith(".npz"))
        om = np.load(os.path.join(d, "omega.npy")) if os.path.exists(os.path.join(d, "omega.npy")) else np.zeros(0)
        _X, meta = __import__("gravita_due_corpi_misure").leggi(os.path.join(d, fs[0]))
        print("  %s%s" % (nome, "   ### UN OGGETTO NUOVO (la proiezione: la frazione %.6f, la molteplicita' %d), NON IL MATTONE SPOSTATO" % (meta["frazione_proiettata"], meta["molteplicita"]) if "frazione_proiettata" in meta else ""))
        serie = []
        for f in fs:
            k = int(f[6:12])
            w, p, mx, M = TT.misura(os.path.join(d, f), nodo, n, L)
            serie.append((k, w, p, mx, M))
            print("    k %5d: w %.3f, i pezzi %d, il picco lisciato %.4e, la massa %.6f" % (k, w, p, mx, M))
        w0 = serie[0][1]
        sc = [k for k, w, p, _m, _M in serie[1:] if not (0.7 <= w / w0 <= 1.3) or p > 1]
        print("    si scioglie: %s" % ("al k %d (il primo stato fuori)" % sc[0] if sc else "NO, fino a k %d" % serie[-1][0]))
        ks = {k: (w, p) for k, w, p, _m, _M in serie}
        if 500 in ks and 3000 in ks:
            r = ks[3000][0] / ks[500][0]
            print("    K-T: w(3000)/w(500) %.3f, i pezzi a 3000 %d: %s" % (r, ks[3000][1], "REGGE" if 0.7 <= r <= 1.3 and ks[3000][1] == 1 else "### NON REGGE"))
        for a, b in FINESTRE:
            if len(om) >= b:
                x = om[a - 1:b]
                print("    omega [%d, %d]: %+.7f +- %.1e (la deviazione %.1e): %s" % (a, b, float(x.mean()), float(x.std() / math.sqrt(len(x))), float(x.std()), dove(float(x.mean()), gap)))
        if nome == "S1_cima" and len(om) >= 500:
            x = float(om[:500].mean())
            esito("il controllo positivo: omega di F0 alla cima su [1, 500] = %.4f entro %g" % (OMEGA_F0, TOLL_OMEGA), abs(x - OMEGA_F0) <= TOLL_OMEGA, "(%+.6f)" % x)
    print("=" * 130)
    return 0 if all(ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("corsa", "lettura"))
    ap.add_argument("--forma")
    ap.add_argument("--semina", choices=("cima", "proiezione_Gamma"))
    ap.add_argument("--fino", type=int)
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        return corsa(a.forma, a.semina, a.fino)
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
