# -*- coding: utf-8 -*-
r"""**[M1631] GLI AUTOVETTORI DEL FONDO A GAMMA, K, M -- v2: LA DEGENERAZIONE** *(la v1, `torneo_fondo.py` d5746c43, trovo' la piu' bassa DEGENERE ai tre punti: `doc/referti_l2/torneo_fondo.txt`)* *(il passo 4 del torneo, P1; la carta `doc/CARTA_torneo_nonlinearita.md`, sez. `6` e `10`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/torneo_fondo_v2.py > doc/referti_l2/torneo_fondo_v2.txt

**La risposta lineare di UN tick attorno al vuoto** *(le righe di `spettro_gap.bande`: il vuoto fresco, `12` impulsi `+-` su `psi` nel nodo `0`, il tick U con `cs = s`; F0, la scena com'e')*; `A(k) = somma_x R(x) e^{-i k . d(x)}` a **Gamma** `0`, **M** `B0/2`, **K** *(il punto di `|k| = |B0|/sqrt(3)` fra `(2 B0 + B1)/3`, `(B0 + 2 B1)/3`, `(B0 + B1)/3`)*; **l'autovettore della quasi-energia piu' bassa** *(`E = -arg lambda`)*, norma `1`. **I DEVE:** l'energia `-0.4826761` entro `1e-6` *(1a, `spettro_gap_v2.txt`)*; il distacco dalla seconda piu' bassa `> 1e-6` *(non degenere)*; `k` commensurato col toro *(`|e^{i k . L A_j} - 1| < 1e-9`)*; `|A v - lambda v| < 1e-10`. **Salva** `k` e `v(k)` in `E:\soliton_simulator\controllo\M1631\fondo.npz` *(il dato e' il comando)*.

### **LA v2 MISURA LA DEGENERAZIONE** *(nessun DEVE nuovo sulla fisica: e' una lettura)*: **la molteplicita'** `m` *(le quasi-energie entro `1e-9` dalla piu' bassa)*; **se il sottospazio e' un DOPPIETTO DI SPIN** *(invariante sotto una stessa `SU(2)` casuale applicata all'indice di spin di ogni semi-arco: il residuo della proiezione; le componenti `c = 2 h + s`, l'ordine di `psi_h.reshape(n, 12)`)*; **la molteplicita' della CIMA a Gamma**; **lo stampo nel sottospazio del fondo:** per ogni nodo della semina alla cima con `rho > 1e-3 rho_max`, la frazione di `|psi(x) e^{-i k.d}|^2` che cade nel sottospazio, pesata con `rho` *(se e' vicina a `0` la proiezione non e' una semina sensata)*. **Il seme di SU(2):** `20261122`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402

E_FONDO = -0.4826761
DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1631")
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def main():
    import _presidio
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "caduta_segno_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "spettro_gap.py"))
    _presidio.avvia(__file__)
    A_IMP = T4B.A_IMP
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    print("=" * 130)
    print("[M1631] GLI AUTOVETTORI DEL FONDO (la carta sez. 6, 10): A_IMP %g" % A_IMP)
    print("=" * 130)
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
        import caduta_libera as CL
        _C2, info = CL.prepara(Z)
        c = info["centro"]
        stampo = (Z["st"]["psi_h"].reshape(n, 12).copy(), TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L)[:, :2])
        Z["metti"]()
    sup = np.nonzero(np.abs(R).reshape(n, -1).max(axis=1) > 0.0)[0]
    Rs, ds = R[sup], d0[sup]
    A1, A2 = TO.vettori()
    Av = np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]])
    B = 2.0 * np.pi * np.linalg.inv(Av).T
    nb = float(np.linalg.norm(B[0]))
    print("### la risposta di un tick: %d nodi col supporto; |B0| %.6f, |B1| %.6f, B0.B1/|B0|^2 %+.4f; L %d" % (len(sup), nb, float(np.linalg.norm(B[1])), float(B[0] @ B[1]) / nb ** 2, L))

    def A_di(kv):
        return np.einsum("x,xij->ij", np.exp(-1j * (ds @ kv)), Rs)
    candidati = [("(2B0+B1)/3", (2 * B[0] + B[1]) / 3), ("(B0+2B1)/3", (B[0] + 2 * B[1]) / 3), ("(B0+B1)/3", (B[0] + B[1]) / 3)]
    kK = [(nome, k) for nome, k in candidati if abs(np.linalg.norm(k) - nb / np.sqrt(3.0)) < 1e-9]
    esito("K: un candidato con |k| = |B0|/sqrt(3)", len(kK) >= 1, "%s" % [x[0] for x in kK])
    punti = [("Gamma", "0", np.zeros(2)), ("K", kK[0][0], kK[0][1]), ("M", "B0/2", B[0] / 2.0)]
    out = {}
    rng = np.random.default_rng(20261122)
    a = rng.normal(size=4)
    a = a / np.linalg.norm(a)
    SU = np.array([[a[0] + 1j * a[1], a[2] + 1j * a[3]], [-a[2] + 1j * a[3], a[0] - 1j * a[1]]])
    print("### la SU(2) casuale: |det - 1| %.1e, |S S^dag - I| %.1e" % (abs(np.linalg.det(SU) - 1.0), float(np.linalg.norm(SU @ SU.conj().T - np.eye(2)))))
    G0 = A_di(np.zeros(2))
    lam0 = np.linalg.eigvals(G0)
    E0s = np.sort(-np.angle(lam0))
    m_cima = int(np.sum(np.abs(E0s - E0s[-1]) < 1e-9))
    print("### la CIMA a Gamma: E %+.10f, la molteplicita' %d; le 12 quasi-energie a Gamma: %s" % (E0s[-1], m_cima, " ".join("%+.6f" % x for x in E0s)))
    psi_c, dc = stampo
    rho_c = np.sum(np.abs(psi_c) ** 2, axis=1)
    vivi = rho_c > 1e-3 * rho_c.max()
    for nome, forma, kv in punti:
        G = A_di(kv)
        lam, V = np.linalg.eig(G)
        E = -np.angle(lam)
        o = np.argsort(E)
        v = V[:, o[0]] / np.linalg.norm(V[:, o[0]])
        res = float(np.linalg.norm(G @ v - lam[o[0]] * v))
        com = max(abs(np.exp(1j * L * float(kv @ Av[j])) - 1.0) for j in (0, 1))
        print("  %-5s k = %-11s (%+.6f, %+.6f): le due quasi-energie piu' basse %+.8f %+.8f; |lambda| %.12f; il residuo %.2e; |e^{i k.L A_j} - 1| %.2e" % (
            nome, forma, kv[0], kv[1], E[o[0]], E[o[1]], abs(lam[o[0]]), res, com))
        print("        |v| per componente: %s" % " ".join("%.4f" % x for x in np.abs(v)))
        esito("%s: la piu' bassa = %.7f entro 1e-6 (1a)" % (nome, E_FONDO), abs(E[o[0]] - E_FONDO) <= 1e-6, "(%+.8f)" % E[o[0]])
        esito("%s: NON degenere (il distacco dalla seconda > 1e-6)" % nome, E[o[1]] - E[o[0]] > 1e-6, "(%.3e)" % (E[o[1]] - E[o[0]]))
        esito("%s: k commensurato col toro L %d" % (nome, L), com < 1e-9, "(%.2e)" % com)
        esito("%s: autovettore (il residuo < 1e-10)" % nome, res < 1e-10, "(%.2e)" % res)
        m = int(np.sum(np.abs(E - E[o[0]]) < 1e-9))
        Q, _r = np.linalg.qr(V[:, o[:m]])
        P = Q @ Q.conj().T
        Qr = np.einsum("ab,hbm->ham", SU, Q.reshape(6, 2, m)).reshape(12, m)
        inv = float(np.linalg.norm(Qr - P @ Qr))
        fase = np.exp(-1j * (dc[vivi] @ kv))
        y = psi_c[vivi] * fase[:, None]
        fr = float(np.sum(np.abs(y @ Q.conj()) ** 2) / np.sum(np.abs(y) ** 2))
        print("        la molteplicita' %d; il sottospazio sotto SU(2) sullo spin: il residuo %.2e (%s); lo stampo nel sottospazio: la frazione pesata %.4f su %d nodi" % (
            m, inv, "DOPPIETTO DI SPIN" if inv < 1e-10 else "NON invariante", fr, int(vivi.sum())))
        out[nome] = (kv, v, E[o[0]])
    os.makedirs(DIR, exist_ok=True)
    f = os.path.join(DIR, "fondo_v2.npz")
    np.savez(f, **{"k_%s" % x: out[x][0] for x in out}, **{"v_%s" % x: out[x][1] for x in out}, **{"E_%s" % x: out[x][2] for x in out})
    print("### salvato %s" % f)
    print("=" * 130)
    print("  %d DEVE su %d   %s" % (sum(ESITI), len(ESITI), "TUTTI PASSATI" if all(ESITI) else "### CI SONO BUCHI"))
    print("=" * 130)
    return 0 if all(ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
