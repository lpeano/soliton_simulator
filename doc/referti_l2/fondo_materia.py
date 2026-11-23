# -*- coding: utf-8 -*-
r"""**[M1658-S] 1a: IL FONDO DELLA BANDA DELLA MATERIA (`+0.2453`, IL PUNTO K): LA MOLTEPLICITA', CONO O CURVATURA, LO STAMPO** *(Luca, 2026-11-23; la carta `doc/CARTA_fondo_giusto.md`, sez. `2`; in memoria, nessuna corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_materia.py > doc/referti_l2/fondo_materia.txt

**`A(k)`** dalle righe di `torneo_fondo_v2.py` *(= `spettro_gap.bande`: il vuoto fresco, `12` impulsi `+-`, il tick U con `cs = s`)*. **K** `(B0 + B1)/3`, **K'** `(2 B0 + B1)/3`: le quasi-energie, la molteplicita' a `+0.2453383` *(entro `1e-9`)*; **cono o curvatura** lungo `B0`, `B1` e la bisettrice, `delta = 0.0025, 0.005, 0.01, 0.02` *(unita' di `|B0|`)*, l'esponente `p = log2((E(2 delta) - E_K)/(E(delta) - E_K))`; **il doppietto di spin** *(SU(2), il seme `20261122`)*; **lo stampo** nel sottospazio di K e, per confronto, della cima a Gamma.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402

E_FONDO, E_CIMA = 0.2453383, 0.4767266
DELTE = (0.0025, 0.005, 0.01, 0.02)
FIN = (0.20, 0.30)
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def risposta():
    """### `R`, `d0`, lo stampo: le righe di `torneo_fondo_v2.main` fino a `stampo`."""
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    import caduta_libera as CL
    A_IMP = T4B.A_IMP
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    with TC.scena() as Z:
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
        for x in Z["chiavi"]:
            st[x][...] = base[x]
        Z["metti"]()
        _C2, info = CL.prepara(Z)
        c = info["centro"]
        stampo = (Z["st"]["psi_h"].reshape(n, 12).copy(), TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2])
        Z["metti"]()
    return R, d0, stampo, L, s


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "caduta_segno_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "torneo_fondo_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1658-S] 1a: IL FONDO DELLA BANDA DELLA MATERIA (la carta doc/CARTA_fondo_giusto.md, sez. 2)")
    print("=" * 130)
    R, d0, stampo, L, s = risposta()
    sup = np.nonzero(np.abs(R).reshape(R.shape[0], -1).max(axis=1) > 0.0)[0]
    Rs, ds = R[sup], d0[sup]
    A1, A2 = TO.vettori()
    Av = np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]])
    B = 2.0 * np.pi * np.linalg.inv(Av).T
    nb = float(np.linalg.norm(B[0]))

    def A_di(kv):
        return np.einsum("x,xij->ij", np.exp(-1j * (ds @ kv)), Rs)

    def E_di(kv):
        lam, V = np.linalg.eig(A_di(kv))
        E = -np.angle(lam)
        o = np.argsort(E)
        return E[o], V[:, o] / np.linalg.norm(V[:, o], axis=0), lam[o]
    rng = np.random.default_rng(20261122)
    a = rng.normal(size=4)
    a = a / np.linalg.norm(a)
    SU = np.array([[a[0] + 1j * a[1], a[2] + 1j * a[3]], [-a[2] + 1j * a[3], a[0] - 1j * a[1]]])
    psi_c, dc = stampo
    rho_c = np.sum(np.abs(psi_c) ** 2, axis=1)
    vivi = rho_c > 1e-3 * rho_c.max()

    def sottospazio(kv, E, V, E_bers):
        sel = np.nonzero(np.abs(E - E_bers) < 1e-9)[0]
        m = len(sel)
        Q, _r = np.linalg.qr(V[:, sel])
        P = Q @ Q.conj().T
        Qr = np.einsum("ab,hbm->ham", SU, Q.reshape(6, 2, m)).reshape(12, m)
        inv = float(np.linalg.norm(Qr - P @ Qr))
        y = psi_c[vivi] * np.exp(-1j * (dc[vivi] @ kv))[:, None]
        fr = float(np.sum(np.abs(y @ Q.conj()) ** 2) / np.sum(np.abs(y) ** 2))
        return m, inv, fr
    E0, V0, _l = E_di(np.zeros(2))
    mc, invc, frc = sottospazio(np.zeros(2), E0, V0, E0[-1])
    print("### la CIMA a Gamma: E %+.10f, la molteplicita' %d; SU(2) il residuo %.2e; lo stampo nel sottospazio %.4f (%d nodi)" % (E0[-1], mc, invc, frc, int(vivi.sum())))
    esito("K1 la cima a Gamma = %+.7f entro 1e-6 (spettro_gap_v2)" % E_CIMA, abs(E0[-1] - E_CIMA) <= 1e-6, "(%+.8f)" % E0[-1])
    curv = {}
    for nome, kv in (("K", (B[0] + B[1]) / 3.0), ("K'", (2 * B[0] + B[1]) / 3.0)):
        E, V, lam = E_di(kv)
        com = max(abs(np.exp(1j * L * float(kv @ Av[j])) - 1.0) for j in (0, 1))
        print("  %s (%+.6f, %+.6f), |k|/|B0| %.6f; commensurato con L %d: %.1e" % (nome, kv[0], kv[1], np.linalg.norm(kv) / nb, L, com))
        print("    le 12 quasi-energie: %s" % " ".join("%+.7f" % x for x in E))
        j = int(np.argmin(np.abs(E - E_FONDO)))
        Ek = float(E[j])
        m, inv, fr = sottospazio(kv, E, V, Ek)
        print("    il fondo della materia %+.10f; la molteplicita' %d (entro 1e-9); |lambda| %.12f; SU(2) il residuo %.2e (%s); lo stampo nel sottospazio %.6f" % (
            Ek, m, abs(lam[j]), inv, "DOPPIETTO DI SPIN" if inv < 1e-10 else "NON invariante", fr))
        esito("K1 %s: il fondo = %+.7f entro 1e-6 (spettro_gap_v2)" % (nome, E_FONDO), abs(Ek - E_FONDO) <= 1e-6, "(%+.8f)" % Ek)
        dirs = (("B0", B[0] / nb), ("B1", B[1] / np.linalg.norm(B[1])), ("bisettrice", (B[0] + B[1]) / np.linalg.norm(B[0] + B[1])))
        for dn, u in dirs:
            righe = []
            dE = []
            for dl in DELTE:
                Ed, _V, _l = E_di(kv + dl * nb * u)
                w = np.sort(Ed[(Ed > FIN[0]) & (Ed < FIN[1])])
                dE.append(w - Ek)
                righe.append("d %.4f: %s" % (dl, " ".join("%+.4e" % x for x in (w - Ek))))
            print("    lungo %-10s %s" % (dn, "; ".join(righe)))
            for b in range(len(dE[0])):
                p = [math.log2(dE[q + 1][b] / dE[q][b]) if dE[q][b] > 0 and dE[q + 1][b] > 0 else float("nan") for q in range(len(DELTE) - 1)]
                k2 = [2.0 * dE[q][b] / (DELTE[q] * nb) ** 2 for q in range(len(DELTE))]
                tipo = "CURVATURA" if all(abs(x - 2) < 0.2 for x in p[:2]) else ("CONO" if all(abs(x - 1) < 0.2 for x in p[:2]) else "NE' L'UNO NE' L'ALTRO")
                print("      il ramo %d: gli esponenti p %s: %s; 2 dE/dk^2 %s; dE/dk %s" % (b, " ".join("%.3f" % x for x in p), tipo, " ".join("%+.4e" % x for x in k2), " ".join("%+.4e" % (dE[q][b] / (DELTE[q] * nb)) for q in range(len(DELTE)))))
                curv[(nome, dn, b)] = (tipo, k2[0])
        esito("K2 %s: non degenere (la molteplicita' <= 2)" % nome, m <= 2, "(%d)" % m)
    tipi = {v[0] for v in curv.values()}
    pos = all(v[0] == "CURVATURA" and v[1] > 0 for v in curv.values())
    print("### i rami al fondo: %s" % sorted(tipi))
    esito("K2: la curvatura al fondo POSITIVA (ogni ramo, ogni direzione, a K e K')", pos)
    print("=" * 130)
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0


if __name__ == "__main__":
    sys.exit(main())
