# -*- coding: utf-8 -*-
r"""**[M1446-S] LO SPETTRO DEL TICK -- LA V2: LE BANDE, I GAP, LA SIMMETRIA, LA CONVENZIONE VECCHIA, e0 - pi s, IL FIT DI DIRAC** *(il mandato di Luca [M1446], corsia S, e le aggiunte v2, v3 e (iv); la carta `doc/CARTA_E_mc2.md`, sez. `S`, `2`, `3`; `spettro_gap.py` non e' mai girato: questa e' la versione che gira)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/spettro_gap_v2.py > doc/referti_l2/spettro_gap.txt

**Le righe di `spettro_gap.bande`** *(la risposta lineare di un tick sul vuoto della scena di `chi`, ristretta al supporto; `A(k)` su `48 x 48`; la velocita' di gruppo da Hellmann-Feynman; `d2E/dk2` della banda di `q`; i gap sul cerchio)* **e in piu':** **(i)** lo scarto massimo *(la distanza di Hausdorff sul cerchio fra lo spettro a `k` e la sua immagine)* per `eps -> -eps` *(allo stesso `k` e a `-k`)* e per `eps -> eps + pi`; **(ii)** i centri nella convenzione vecchia *(`E - pi s`)*; **(iii)** `e0 - pi s` contro le larghezze dei gap e le distanze fra la cima e gli altri livelli a `Gamma`; **(iv)** il fit `E - E0 = +-sqrt(Delta^2 + c^2 k^2)` sui due rami dei gap attorno alla banda della materia, a `Gamma`, lungo `B_0` e `B_1`, `|k| < 0.3`, `61` punti, le bande seguite per sovrapposizione; la curvatura col segno; DIRAC entro il `5%`. **I dati** in `E:\soliton_simulator\controllo\M1446\spettro.npz` *(per `emc2_v3.py`)*.
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
import spettro_gap as SG  # noqa: E402

GRIGLIA, K_DIRAC, P_DIRAC, TOLL_DIRAC = 48, 0.3, 61, 0.05
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def wrap(x):
    return (np.asarray(x) + np.pi) % (2 * np.pi) - np.pi


def hausdorff(a, b):
    d = np.abs(wrap(a[:, None] - b[None, :]))
    return float(max(d.min(axis=1).max(), d.min(axis=0).max()))


def main():
    import _presidio
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "caduta_segno_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "spettro_gap.py"))
    _presidio.avvia(__file__)
    A_IMP, DK = T4B.A_IMP, T4B.DK
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    print("=" * 130)
    print("[M1446-S] LO SPETTRO DEL TICK, LA V2 (la carta sez. S, 2, 3): la griglia %d x %d; A_IMP %g, DK %g; e0 %.10f" % (GRIGLIA, GRIGLIA, A_IMP, DK, e0))
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

    Es, Vs = np.zeros((GRIGLIA, GRIGLIA, 12)), np.zeros((GRIGLIA, GRIGLIA, 2, 12))
    for i in range(GRIGLIA):
        for j in range(GRIGLIA):
            kv = (i * B[0] + j * B[1]) / GRIGLIA
            lam, V = np.linalg.eig(A_di(kv))
            V = V / np.linalg.norm(V, axis=0)
            Es[i, j] = -np.angle(lam)
            for a, u in enumerate(bh):
                dA = dA_di(kv, u)
                Vs[i, j, a] = [float(np.real(1j * (V[:, b].conj() @ dA @ V[:, b]) / lam[b])) for b in range(12)]
    vmax = float(np.abs(Vs).max())
    print("### le quasi-energie: da %+.6f a %+.6f; |dE/dk| massima %.6f nodi per tick (B0 %.6f, B1 %.6f); 0.588 s = %.6f: il rapporto %.5f" % (
        float(Es.min()), float(Es.max()), vmax, float(np.abs(Vs[:, :, 0]).max()), float(np.abs(Vs[:, :, 1]).max()), 0.588 * s, vmax / (0.588 * s)))
    G0 = A_di(np.zeros(2))
    lam, V = np.linalg.eig(G0)
    EG = -np.angle(lam)
    o = np.argsort(EG)
    print("### i 12 autovalori a Gamma (ordinati): %s" % " ".join("%+.7f" % EG[i] for i in o))

    def segui(v0, u, ts):
        """### la banda che parte dall'autovettore v0 a Gamma, seguita per sovrapposizione lungo u."""
        out, v = [], v0
        for t in ts:
            w, vr = np.linalg.eig(A_di(t * u))
            vr = vr / np.linalg.norm(vr, axis=0)
            b = int(np.argmax(np.abs(vr.conj().T @ v) ** 2))
            out.append(float(-np.angle(w[b])))
            v = vr[:, b]
        return np.array(out)
    q = V[:, o[-1]] / np.linalg.norm(V[:, o[-1]])
    d2 = []
    for u in bh:
        e_ = segui(q, u, (0.0, DK))
        em = segui(q, u, (0.0, -DK))
        d2.append((e_[1] - 2 * e_[0] + em[1]) / DK ** 2)
    print("### la banda di q (la cima, E %.10f): d2E/dk2 lungo B0 %+.6e, lungo B1 %+.6e; m*_banda %+.4f" % (EG[o[-1]], d2[0], d2[1], 1.0 / d2[0]))
    esito("K1-S: d2E/dk2 della banda di q = -0.059 entro l'1% (T-L4: -5.923495e-02)", abs(d2[0] / -5.923495e-02 - 1.0) <= 0.01, "(%+.6e)" % d2[0])
    esito("K1-S: v_max = 0.588 s entro l'1%", abs(vmax / (0.588 * s) - 1.0) <= 0.01, "(%.6f contro %.6f)" % (vmax, 0.588 * s))
    # ### i gap
    tutti = np.sort(wrap(Es.reshape(-1)))
    dkg = np.linalg.norm(B[0]) / GRIGLIA
    soglia = 4.0 * vmax * dkg
    sp = np.diff(np.concatenate([tutti, [tutti[0] + 2 * np.pi]]))
    gap = []
    for i in np.nonzero(sp > soglia)[0]:
        a, w = float(tutti[i]), float(sp[i])
        gap.append((a, float(wrap(a + w)), w, float(wrap(a + w / 2))))
    print("### I GAP (gli spazi sopra 4 v_max dk = %.4e): %d" % (soglia, len(gap)))
    for a, b, w, c in gap:
        print("    da %+.6f a %+.6f: la larghezza %.6f, il centro %+.6f; nella convenzione VECCHIA (E - pi s) il centro %+.6f" % (a, b, w, c, float(wrap(c - math.pi * s))))
    # ### (i) la simmetria
    sm, smk, spi = 0.0, 0.0, 0.0
    for i in range(GRIGLIA):
        for j in range(GRIGLIA):
            ek = Es[i, j]
            emk = Es[(-i) % GRIGLIA, (-j) % GRIGLIA]
            sm = max(sm, hausdorff(ek, -ek))
            smk = max(smk, hausdorff(ek, -emk))
            spi = max(spi, hausdorff(ek, wrap(ek + np.pi)))
    print("### (i) LA SIMMETRIA (lo scarto massimo sul cerchio): eps -> -eps allo stesso k %.3e; eps -> -eps con k -> -k %.3e; eps -> eps + pi %.3e" % (sm, smk, spi))
    centri_sim = []
    if min(sm, smk) <= 1e-6:
        centri_sim += [0.0, math.pi]
        if spi <= 1e-6:
            centri_sim += [math.pi / 2, -math.pi / 2]
    print("    i centri di simmetria trovati (entro 1e-6): %s" % (centri_sim or "nessuno"))
    # ### (iii) e0 - pi s
    dd = e0 - math.pi * s
    print("### (iii) e0 - pi s = %.6f; le larghezze dei gap %s; a Gamma la cima %+.7f e il livello piu' vicino sotto %+.7f (la distanza %.6f)" % (
        dd, ", ".join("%.6f" % g[2] for g in gap), EG[o[-1]], EG[o[-3]], EG[o[-1]] - EG[o[-3]]))
    print("    %s" % ("e0 - pi s COINCIDE (entro il 5%%) con la larghezza di un gap" if any(abs(g[2] / dd - 1) <= 0.05 for g in gap) else "e0 - pi s NON e' la larghezza di nessun gap: e' la distanza fra la cima della banda della materia (e0) e il ritmo del vuoto (pi s), due livelli diversi"))
    # ### (iv) il fit di Dirac ai gap attorno alla banda della materia (a Gamma)
    sopra = o[(np.searchsorted(EG[o], EG[o[-1]], side="right")) % 12]
    sotto = [b for b in o if EG[b] < EG[o[-2]] - 1e-9][-1]
    ts = np.linspace(-K_DIRAC, K_DIRAC, P_DIRAC)
    print("### (iv) I GAP ATTORNO ALLA BANDA DELLA MATERIA, a Gamma, |k| < %g, %d punti" % (K_DIRAC, P_DIRAC))
    for nome, lo, up in (("sopra la materia (la cima %+.6f -> %+.6f)" % (EG[o[-1]], EG[sopra]), o[-1], sopra), ("sotto la materia (%+.6f -> la base della coppia %+.6f)" % (EG[sotto], EG[o[-2]]), sotto, o[-2])):
        Elo0, Eup0 = EG[lo], EG[up]
        if Eup0 < Elo0:
            Eup0 += 2 * np.pi
        Ec, De = 0.5 * (Elo0 + Eup0), 0.5 * (Eup0 - Elo0)
        for a, u in enumerate(bh):
            elo = segui(V[:, lo] / np.linalg.norm(V[:, lo]), u, ts)
            eup = segui(V[:, up] / np.linalg.norm(V[:, up]), u, ts)
            eup = np.where(eup < elo, eup + 2 * np.pi, eup)
            res = {}
            for ramo, ee, sg in (("alto", eup, +1.0), ("basso", elo, -1.0)):
                y = (ee - Ec) ** 2 - De ** 2
                c2 = float(np.sum(ts ** 2 * y) / np.sum(ts ** 4))
                fit = sg * np.sqrt(np.maximum(De ** 2 + c2 * ts ** 2, 0.0))
                err = float(np.max(np.abs((ee - Ec) - fit) / np.maximum(np.abs(ee - Ec), 1e-12)))
                h = ts[1] - ts[0]
                m = P_DIRAC // 2
                curv = float((ee[m + 1] - 2 * ee[m] + ee[m - 1]) / h ** 2)
                res[ramo] = (c2, err, curv)
            ca = math.sqrt(abs(res["alto"][0])) * (1 if res["alto"][0] >= 0 else -1)
            cb = math.sqrt(abs(res["basso"][0])) * (1 if res["basso"][0] >= 0 else -1)
            dirac = res["alto"][0] > 0 and res["basso"][0] > 0 and res["alto"][1] <= TOLL_DIRAC and res["basso"][1] <= TOLL_DIRAC and abs(ca / cb - 1) <= TOLL_DIRAC
            print("    %s, lungo B%d: E0 %+.6f, Delta %.6f; il ramo alto c %+.5f (l'errore relativo massimo %.3f, la curvatura %+.4e); il basso c %+.5f (%.3f, %+.4e); c contro s %.3f, contro 0.588 s %.3f: %s" % (
                nome, a, Ec, De, ca, res["alto"][1], res["alto"][2], cb, res["basso"][1], res["basso"][2], abs(ca) / s, abs(ca) / (0.588 * s), "DIRAC" if dirac else "non Dirac"))
    w1 = SG.OM_omega()
    np.savez(SG.FUORI, E=Es.reshape(-1, 12), gap=np.array(gap), d2=np.array(d2), vmax=vmax, omega=w1, Etop=float(EG[o[-1]]), centri_sim=np.array(centri_sim), s=s, e0=e0)
    print("### omega(N1) %.10f; i dati in %s (sha1 %s)" % (w1, SG.FUORI, SG.sha1(SG.FUORI)[:8]))
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
