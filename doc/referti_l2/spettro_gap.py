# -*- coding: utf-8 -*-
r"""**[M1446-S] [M1446-E] LO SPETTRO DEL TICK: TUTTE LE BANDE, I GAP, I CENTRI; E = m c^2** *(il mandato di Luca [M1446], corsia S; la carta `doc/CARTA_E_mc2.md`, sez. `S`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/spettro_gap.py bande > doc/referti_l2/spettro_gap.txt
    E:\python\py3132\python.exe doc/referti_l2/spettro_gap.py emc2 > doc/referti_l2/E_mc2.txt

**La risposta lineare di UN tick** *(le righe di `caduta_segno_v2.py`: la scena di `chi`, il vuoto fresco, `12` impulsi `+-` su `psi` nel nodo `0`, il tick U con `cs = s`)*, **ristretta ai nodi dove `R` non e' zero** *(la risposta di un tick e' locale)*; `A(k) = somma_x R(x) e^{-i k.d(x)}`, **gli autovalori `e^{-i E}` su una griglia `48 x 48`** della zona di Brillouin; **la velocita' di gruppo** dal teorema di Hellmann-Feynman *(`A` unitaria: `dE/dk = Re(i v^dag (dA/dk) v / lambda)`)* lungo `B_0` e `B_1`; **`d2E/dk2` della banda di `q`** *(la cima a `Gamma`)* con `dk = 0.02` *(di T-L4b)*. **I gap:** gli spazi fra i valori ordinati sul cerchio piu' larghi di `4 v_max dk_griglia` *(il passo della griglia: dichiarato)*; i centri. **`emc2`:** per ogni centro `E0`, `Delta_mat = |omega - E0|` *(sul cerchio)*, `R_E = Delta_mat/(|m*_banda| c^2)` per `c_m = 0.588 s` e `c = s`.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import orologio_mattone as OM  # noqa: E402

GRIGLIA = 48
FUORI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1446", "spettro.npz")
C_MATERIA = 0.588
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def sha1(f):
    import hashlib
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def bande():
    import _presidio
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "caduta_segno_v2.py"))
    _presidio.avvia(__file__)
    A_IMP, DK = T4B.A_IMP, T4B.DK
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    print("=" * 130)
    print("[M1446-S] LO SPETTRO DEL TICK (la carta sez. S): la griglia %d x %d; A_IMP %g, DK %g" % (GRIGLIA, GRIGLIA, A_IMP, DK))
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
    sup = np.nonzero(np.abs(R).reshape(n, -1).max(axis=1) > 0.0)[0]
    Rs, ds = R[sup], d0[sup]
    print("### la risposta di un tick: %d nodi col supporto (il raggio massimo %.3f)" % (len(sup), float(np.hypot(*ds.T).max())))
    A1, A2 = TO.vettori()
    B = 2.0 * np.pi * np.linalg.inv(np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]])).T
    bh = [B[0] / np.linalg.norm(B[0]), B[1] / np.linalg.norm(B[1])]

    def A_di(kv):
        return np.einsum("x,xij->ij", np.exp(-1j * (ds @ kv)), Rs)

    def dA_di(kv, u):
        return np.einsum("x,xij->ij", -1j * (ds @ u) * np.exp(-1j * (ds @ kv)), Rs)

    Es, Vs = [], []
    for i in range(GRIGLIA):
        for j in range(GRIGLIA):
            kv = (i * B[0] + j * B[1]) / GRIGLIA
            G = A_di(kv)
            lam, V = np.linalg.eig(G)
            V = V / np.linalg.norm(V, axis=0)
            E = -np.angle(lam)
            vg = []
            for u in bh:
                dA = dA_di(kv, u)
                vg.append([float(np.real(1j * (V[:, b].conj() @ dA @ V[:, b]) / lam[b])) for b in range(12)])
            Es.append(E)
            Vs.append(np.array(vg))
    Es, Vs = np.array(Es), np.array(Vs)                     # ### (k, 12), (k, 2, 12)
    vmax = float(np.abs(Vs).max())
    print("### le quasi-energie su %d punti: da %+.6f a %+.6f; la velocita' di gruppo massima |dE/dk| %.6f nodi per tick (lungo B0 %.6f, lungo B1 %.6f); contro 0.588 s = %.6f: il rapporto %.5f" % (
        len(Es), float(Es.min()), float(Es.max()), vmax, float(np.abs(Vs[:, 0]).max()), float(np.abs(Vs[:, 1]).max()), C_MATERIA * 0.15, vmax / (C_MATERIA * 0.15)))
    # ### la cima a Gamma e d2E/dk2 lungo i due assi
    G0 = A_di(np.zeros(2))
    lam, V = np.linalg.eig(G0)
    E = -np.angle(lam)
    o = np.argsort(E)
    q = V[:, o[-1]] / np.linalg.norm(V[:, o[-1]])

    def sulla(kv):
        w, vr = np.linalg.eig(A_di(kv))
        vr = vr / np.linalg.norm(vr, axis=0)
        b = int(np.argmax(np.abs(vr.conj().T @ q) ** 2))
        return float(-np.angle(w[b]))
    d2 = [(sulla(DK * u) - 2.0 * sulla(np.zeros(2)) + sulla(-DK * u)) / DK ** 2 for u in bh]
    print("### i 12 autovalori a Gamma (ordinati): %s" % " ".join("%+.7f" % E[i] for i in o))
    print("### la banda di q (la cima a Gamma, E %.10f): d2E/dk2 lungo B0 %+.6e, lungo B1 %+.6e; m*_banda = 1/(d2E/dk2) %+.4f" % (E[o[-1]], d2[0], d2[1], 1.0 / d2[0]))
    esito("K1-S: d2E/dk2 della banda di q = -0.059 entro l'1% (T-L4: -5.923495e-02)", abs(d2[0] / -5.923495e-02 - 1.0) <= 0.01, "(%+.6e)" % d2[0])
    esito("K1-S: v_max = 0.588 s entro l'1%", abs(vmax / (C_MATERIA * 0.15) - 1.0) <= 0.01, "(%.6f contro %.6f)" % (vmax, C_MATERIA * 0.15))
    # ### i gap sul cerchio
    tutti = np.sort(np.mod(Es.reshape(-1) + np.pi, 2 * np.pi) - np.pi)
    dk_g = np.linalg.norm(B[0]) / GRIGLIA
    soglia = 4.0 * vmax * dk_g
    sp = np.diff(np.concatenate([tutti, [tutti[0] + 2 * np.pi]]))
    gi = np.nonzero(sp > soglia)[0]
    gap = []
    for i in gi:
        a, b = tutti[i], tutti[i] + sp[i]
        c = (a + b) / 2.0
        c = (c + np.pi) % (2 * np.pi) - np.pi
        gap.append((float(a), float(b if b <= np.pi else b - 2 * np.pi), float(sp[i]), float(c)))
    print("### I GAP (gli spazi sopra 4 v_max dk = %.4e): %d" % (soglia, len(gap)))
    for a, b, w, c in gap:
        print("    da %+.6f a %+.6f: la larghezza %.6f, IL CENTRO %+.6f" % (a, b, w, c))
    w1 = OM_omega()
    dentro = any((a <= w1 <= b) if a < b else (w1 >= a or w1 <= b) for a, b, _w, _c in gap)
    print("### LA MATERIA: omega(N1) %.10f (l'orologio): %s; il k del mattone: 0 (fermo)" % (w1, "IN UN GAP" if dentro else "IN UNA BANDA"))
    np.savez(FUORI, E=Es, V=Vs, gap=np.array(gap), d2=np.array(d2), vmax=vmax, omega=w1, Etop=float(E[o[-1]]))
    print("### i dati in %s (sha1 %s)" % (FUORI, sha1(FUORI)[:8]))
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def OM_omega():
    f = os.path.join(OM.BASE, "N1", "fase.npy")
    ph = np.unwrap(np.angle(np.load(f)))
    k = np.arange(len(ph), dtype=float)
    m = k >= OM.K_DA_FIT
    A = np.stack([np.ones(m.sum()), k[m]], axis=1)
    b, *_ = np.linalg.lstsq(A, ph[m], rcond=None)
    return -float(b[1])


def emc2():
    import _presidio
    _presidio.avvia(__file__)
    z = np.load(FUORI)
    print("=" * 130)
    print("[M1446-E] E = m c^2 (la carta sez. S): i dati %s (sha1 %s)" % (FUORI, sha1(FUORI)[:8]))
    print("=" * 130)
    w, d2 = float(z["omega"]), float(z["d2"][0])
    ms = abs(1.0 / d2)
    print("### omega(N1) %.10f; m*_banda = 1/(d2E/dk2) = %+.4f" % (w, 1.0 / d2))
    for nome, c in (("c_m = 0.588 s", C_MATERIA * 0.15), ("c = s", 0.15)):
        mc2 = ms * c * c
        print("  %s: |m*| c^2 = %.6f" % (nome, mc2))
        for a, b, wd, E0 in z["gap"]:
            D = abs((w - E0 + np.pi) % (2 * np.pi) - np.pi)
            RE = D / mc2
            print("    il centro %+.6f (il gap da %+.6f a %+.6f): Delta_mat = |omega - E0| %.6f; R_E %.4f: %s; omega %s il centro (%s)" % (
                E0, a, b, D, RE, "VALE" if 0.9 < RE < 1.1 else "non vale", "SOTTO" if ((w - E0 + np.pi) % (2 * np.pi) - np.pi) < 0 else "SOPRA",
                "particella" if ((w - E0 + np.pi) % (2 * np.pi) - np.pi) < 0 else "lacuna"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(bande() if sys.argv[1:] == ["bande"] else emc2())
