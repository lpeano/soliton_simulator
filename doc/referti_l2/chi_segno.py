# -*- coding: utf-8 -*-
r"""**IL CAMPO CHI, PARTE A: IL SEGNO DELLA SORGENTE, LA DERIVA ATTESA, `kappa`** *(il mandato unico di Luca `2026-11-21` `15:57`; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `6`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_segno.py > doc/referti_l2/chi_segno.txt

**Solo lettura.** **La scena** come il driver di C2 *(`CV.scena_L(186, ...)`)*; **il vuoto** = `MT.vuoto_fresco(Z, t0)`; **gli stati** `k 3000` *(C2)*, `15000`, `29000` *(il tronco del ramo `mitosi`)*, caricati con `Z["metti"]`, lo sha1 controllato.
**`Q_k`** = la parentesi di `tick_lapse.omega_psi`: `termini_di_h` + `somma_{h in k} d_peso_arco_h per_arco`, **con `cs = s` UNIFORME** *(il primo ordine in `kappa chi`: `dw = 1/2` esatto)*; **`q = Q - Q_vuoto`** *(z1: `Q_vuoto` il valore per nodo nel vuoto uniforme)*.
**IL SEGNO** *(il FERMO del mandato)*: **`q` sommato sul mattone (`r < 25`) POSITIVO, e `psi` al centro positivo** *(se no: FERMO)*. **A2:** `media chi (t) = kappa s C t^2 / (2 n)`, `C = somma q` sul toro. **A3:** `psi = L^+ (q - media q)` *(il solutore di `gauss_riuso`, la `D` del grafo)*, `kappa = sqrt(- ln(1 - a) c_chi^2 / (s psi_c))`, `a = 1 - N(rho)` al nodo del centro di C2, `c_chi = 0.5` *(D-CHI-VELOCITA')*.
**I casi noti per primi:** il vuoto -> `Q` costante AL BIT; **DEVE CAMBIARE:** `psi_h` di un nodo a `1` -> `Q` non costante. **La diagnosi della forma (a)** *(fa1, sez. `6.3`)*: `e0 rho` accanto a `s q`.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
E_ = "E:" + os.sep
STATI = (("C2 k 3000", os.path.join(E_, "soliton_simulator", "controllo", "C2", "stato_03000.npz")),
         ("tronco k 15000", os.path.join(E_, "soliton_simulator", "controllo", "mitosi_rami", "TRONCO", "stato_15000.npz")),
         ("tronco k 29000", os.path.join(E_, "soliton_simulator", "controllo", "mitosi_rami", "TRONCO", "stato_29000.npz")))
C_CHI = 0.5
R_MATTONE = 25.0
ANELLI = list(range(0, 31, 2)) + list(range(35, 81, 5))


def sha1(f):
    import hashlib
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def Q_di(Z, s):
    import energia_pesata as EP
    mot, st = Z["mot"], Z["st"]
    salvo, lc = mot.cs, getattr(mot, "lambda_c", None)
    mot.cs = np.full(mot.inc.n, float(s))
    mot.lambda_c = None
    try:
        pn, pa = EP.termini_di_h(mot, st, Z["par"])
        dw = EP.d_peso_arco(mot)
        arco = np.zeros(mot.inc.n)
        np.add.at(arco, mot.inc.nodo, dw * np.repeat(pa, 2))
        return pn + arco, float(np.sum(pn)) + float(np.sum(pa))
    finally:
        mot.cs, mot.lambda_c = salvo, lc


def rho_di(Z):
    mot = Z["mot"]
    r = np.zeros(mot.inc.n)
    np.add.at(r, mot.inc.nodo, np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1))
    return r


def anello(r, y, R):
    w = (r >= R - 0.5) & (r < R + 0.5)
    return float(y[w].mean()) if w.any() else math.nan


def main():
    import _presidio
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import scipy.sparse as sp
    import scipy.sparse.linalg as spl
    from solitone import toro as TO
    MT, CV = PS.MT, PS.CV
    rho_c, t0, e0 = MT.rho_c_assoluto(), MT.G2.T0, float(MT.G2.eps_top_tl4b())
    print("=" * 150)
    print("IL CAMPO CHI, PARTE A: IL SEGNO DELLA SORGENTE, LA DERIVA ATTESA, KAPPA (Luca 2026-11-21 15:57; il task history del ramo lapse-u, sez. 6)")
    print("=" * 150)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        n = mot.inc.n
        s = float(Z["s"])
        ii, jj = np.asarray(mot.inc.ii, dtype=np.int64), np.asarray(mot.inc.jj, dtype=np.int64)
        m = len(ii)
        a_ = np.arange(m)
        D = sp.csr_matrix((np.concatenate([np.ones(m), -np.ones(m)]), (np.concatenate([jj, ii]), np.concatenate([a_, a_]))), shape=(n, m))
        risolvi = spl.factorized((D @ D.T).tocsc()[1:, 1:])
        print("### la scena: n %d, m %d, s %.12f, rho_c %.10e, e0 (eps_top_tl4b) %.6e, c_chi %.2f" % (n, m, s, rho_c, e0, C_CHI))
        # ---------------------------------------------------------- IL VUOTO E I CASI NOTI
        MT.vuoto_fresco(Z, t0)
        Qv, Hv = Q_di(Z, s)
        costante = bool(np.all(Qv == Qv[0]))
        psi_salvo = Z["st"]["psi_h"].copy()
        Z["st"]["psi_h"][mot.inc.nodo == 17204] = 1.0
        Qx, _ = Q_di(Z, s)
        Z["st"]["psi_h"][...] = psi_salvo
        cambia = not bool(np.all(Qx == Qx[0]))
        print("### IL VUOTO UNIFORME (vuoto_fresco): Q per nodo %s (%+.6e; min %+.6e, max %+.6e); H del vuoto %+.6e -> %s; DEVE CAMBIARE (psi_h di un nodo a 1): %d valori -> %s" % (
            "COSTANTE AL BIT" if costante else "NON costante", Qv[0], Qv.min(), Qv.max(), Hv, "il caso noto PASSA" if costante else "il caso noto NON passa: FERMO",
            len(np.unique(Qx)), "CAMBIA" if cambia else "NON CAMBIA: FERMO"))
        if not (costante and cambia):
            return 1
        q_v = float(Qv[0])
        print("### z1: Q_vuoto = %+.10e per nodo (%s)" % (q_v, "ZERO: z1 automatica" if q_v == 0.0 else "NON zero: il riferimento derivato si sottrae"))
        kappa = None
        ok = True
        for nome, f in STATI:
            assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
            with np.load(f) as d:
                Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
                meta = json.loads(str(d["meta"]))
            c = [float(x) for x in meta["centro"]]
            r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"]).T[:2])
            c0 = int(np.argmin(r))
            Q, H = Q_di(Z, s)
            q = Q - q_v
            rho = rho_di(Z)
            Cn = float(q.sum())
            psi = np.zeros(n)
            psi[1:] = risolvi((q - q.mean())[1:])
            psi -= psi.mean()
            a = 1.0 - 1.0 / (1.0 + rho[c0] / rho_c)
            print("-" * 150)
            print("### %s (k %d): H = somma Q %+.10e; il centro %.4f %.4f, il nodo %d (r %.4f)" % (nome, int(meta["k"]), H, c[0], c[1], c0, r[c0]))
            s12, s25 = float(q[r < 12.4].sum()), float(q[r < R_MATTONE].sum())
            segno = s25 > 0.0 and psi[c0] > 0.0
            print("    ### A1 IL SEGNO: q = Q - Q_vuoto al centro %+.6e; sommato entro r 12.4 %+.6e, entro r 25 (il mattone) %+.6e, sul toro (la carica netta C) %+.6e; psi al centro %+.6e -> %s" % (
                q[c0], s12, s25, Cn, psi[c0], "POSITIVO (il tempo rallenta sul mattone)" if segno else "NON POSITIVO: FERMO"))
            ok &= segno
            print("    ### la forma (a), diagnosi (fa1): e0 rho al centro %.6e contro s q al centro %+.6e (il rapporto %.3e); e0 somma rho %.6e contro s C %+.6e" % (
                e0 * rho[c0], s * q[c0], e0 * rho[c0] / (s * q[c0]) if q[c0] else math.nan, e0 * rho.sum(), s * Cn))
            if kappa is None and segno:
                kappa = math.sqrt(-math.log(1.0 - a) * C_CHI ** 2 / (s * psi[c0]))
                print("    ### A3 KAPPA (UNA volta, qui): a = 1 - N(rho) al centro %.10e; kappa = sqrt(-ln(1 - a) c_chi^2 / (s psi_c)) = %.10e (DERIVATO)" % (a, kappa))
            if kappa is None:
                continue
            chi = kappa * (s / C_CHI ** 2) * psi
            uN = 1.0 - np.exp(-kappa * chi)
            print("    il profilo STATICO (q per anello; 1 - N con N = exp(-kappa chi); accanto 1 - N(rho)):")
            print("      r          q          1 - N (chi)      1 - N(rho)")
            for R in ANELLI:
                v_q = q[c0] if R == 0 else anello(r, q, R)
                v_u = uN[c0] if R == 0 else anello(r, uN, R)
                v_n = (1.0 - 1.0 / (1.0 + rho[c0] / rho_c)) if R == 0 else anello(r, 1.0 - 1.0 / (1.0 + rho / rho_c), R)
                print("    %3d   %+13.6e   %13.6e   %13.6e" % (R, v_q, v_u, v_n))
            print("    1 - N all'anello 60 sul centro: %.4f" % (anello(r, uN, 60) / uN[c0]))
            for t in (3000.0, 1e5):
                cm = kappa * s * Cn * t * t / (2.0 * n)
                rall = 1.0 - math.exp(-kappa * cm)
                print("    ### A2 LA DERIVA a t = %.0e tick: media chi %+.6e, il rallentamento uniforme 1 - exp(-kappa media chi) %+.6e, sul centro (1 - N al centro %.6e): %.4e" % (
                    t, cm, rall, uN[c0], rall / uN[c0]))
    print("=" * 150)
    print("### IL SEGNO SU TUTTI GLI STATI: %s" % ("POSITIVO: si prosegue" if ok else "NON POSITIVO: FERMO"))
    print("=" * 150)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
