# -*- coding: utf-8 -*-
r"""**[M0037-28] G: «A E' GIA' LA FASE DI phi?» -- LA LETTURA INVARIANTE SULLE PLACCHETTE** *(DECISIONE DI LUCA, 2026-11-28 00:37;
la carta `doc/CARTA_mitosi.md`, sezione G; lettura, nessun tick)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fase_vuoto_vs_A.py > doc/referti_l2/fase_vuoto_vs_A.txt

`f = phi_h.reshape(m, 2)` *(`f[a,0]` in `ii[a]`, `f[a,1]` in `jj[a]`: la carta, G-0 b)*; `theta_a = arg(f[a,1] conj f[a,0])` in `(-pi, pi]`, scartati
gli archi con `min |f| < 1e-6`; `Phi_p = wrap(somma_c S[p,c] theta[P[p,c]])`; `eB_p = e B()[p]` dal campo `_u1_prototipo.Campo` di `porto.campi` con
`A`, `E` dello stato. **Mai A nudo contro theta nudo.** Gli anelli di `8` dal centro di massa periodico di `rho_psi`; la posizione di una placchetta
la media degli scarti dei nodi di partenza dei suoi tre archi; `R = sqrt(somma rho r^2 / somma rho)`. **Casi noti:** K1 (gauge su phi: `Phi_p`
invariato mod `2 pi` entro `1e-10`), K2 (gauge su A: `B` invariato entro `1e-12`), K3 (`A = 0`: «campo nullo», nessuna correlazione),
K4 (il nullo: `|Spearman| < 0.1` in almeno il 95% di 200 permutazioni). **Il verdetto** con le soglie di Luca *(la carta)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
STATI = (("(i) il punto fisso accoppiato, giro 3, l'ultimo stato", os.path.join(CTRL, "M0414", "puntofisso_accoppiato", "giro_3", "stato_006000.npz")),
         ("(ii) la coppia d1 a k 3250 (l'urto; 3230 non e' salvato)", os.path.join(CTRL, "M2034", "coppia", "d1", "stato_003250.npz")),
         ("(ii) la coppia d1L a k 18000", os.path.join(CTRL, "M2034", "coppia", "d1L", "stato_018000.npz")))
SCARTO, ANELLO, NPERM = 1e-6, 8.0, 200
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def wrap(x):
    return np.angle(np.exp(1j * np.asarray(x)))


def ranghi(x):
    r = np.empty(len(x))
    r[np.argsort(x, kind="stable")] = np.arange(len(x))
    return r


def spearman(x, y):
    return float(np.corrcoef(ranghi(x), ranghi(y))[0, 1])


def theta_di(phi_h, m):
    f = np.asarray(phi_h).reshape(m, 2)
    th = wrap(np.angle(f[:, 1] * np.conj(f[:, 0])))
    buoni = np.minimum(np.abs(f[:, 0]), np.abs(f[:, 1])) >= SCARTO
    return th, buoni


def Phi_di(campo, th, buoni):
    P, S = campo.P, campo.S
    tot = th[P[:, 0]] * S[:, 0] + th[P[:, 1]] * S[:, 1] + th[P[:, 2]] * S[:, 2]
    ok = buoni[P[:, 0]] & buoni[P[:, 1]] & buoni[P[:, 2]]
    return wrap(tot), ok


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "triangolo_chi_v4.py"))
    _presidio.avvia(__file__)
    MT, _MTR, _T1, _TRU, _TV, PO = TC.moduli()
    print("=" * 134)
    print("[M0037-28] G: Phi_p (la circolazione dell'angolo d'arco di phi) CONTRO e B_p (il campo U(1)) SULLE PLACCHETTE; la carta, sezione G")
    print("=" * 134)
    rng = np.random.default_rng(20261128)
    esiti_stati = []
    with TC.scena() as Z:
        mot = Z["mot"]
        n, m, L = mot.inc.n, mot.inc.m, Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        ii, jj = nodo[0::2], nodo[1::2]
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
        C = PO.campi(Z, rho_c, e, np.zeros(m), np.zeros(m))
        g = C.campo
        assert np.array_equal(g.ii, ii) and np.array_equal(g.jj, jj), "il campo e il motore NON hanno gli stessi archi"
        pv = np.asarray(Z["phi_v"]).copy()
        # ### (iii) e K3: il vuoto fresco, A = 0
        th, bu = theta_di(pv, m)
        Phi, okp = Phi_di(g, th, bu)
        eB = g.e * g.B()
        print("  (iii) il vuoto fresco (phi_v della scena, A = 0): archi scartati %d; max |Phi| %.3e, rms Phi %.3e; max |eB| %.3e" % (
            int((~bu).sum()), float(np.max(np.abs(Phi[okp]))), float(np.sqrt(np.mean(Phi[okp] ** 2))), float(np.max(np.abs(eB)))))
        nullo = float(np.max(np.abs(eB))) < 1e-6
        esito("(K3) A = 0: «campo nullo», la correlazione NON si calcola", nullo, "max |eB| %.1e" % float(np.max(np.abs(eB))))
        # ### K1 e K2 sul primo stato
        with np.load(STATI[0][1]) as z:
            phi1, A1 = z["phi_h"].copy(), z["campo_A"].copy()
        chi = rng.uniform(-math.pi, math.pi, n)
        th, bu = theta_di(phi1, m)
        Phi, okp = Phi_di(g, th, bu)
        th2, bu2 = theta_di(phi1 * np.exp(1j * chi[nodo]), m)
        Phi2, _ = Phi_di(g, th2, bu2)
        dK1 = float(np.max(np.abs(wrap(Phi2[okp] - Phi[okp]))))
        esito("(K1) gauge su phi: le estremita' di ogni nodo per e^{i chi_v}: Phi_p invariato mod 2 pi entro 1e-10", dK1 < 1e-10, "max %.2e" % dK1)
        g.A[...] = A1
        B1 = g.B().copy()
        g.A[...] = A1 + (chi[jj] - chi[ii])
        dK2 = float(np.max(np.abs(g.B() - B1)))
        esito("(K2) gauge su A: A + (chi_j - chi_i): B invariato entro 1e-12", dK2 < 1e-12, "max %.2e (max |B| %.3e)" % (dK2, float(np.max(np.abs(B1)))))
        # ### gli stati
        for nome, f in STATI:
            with np.load(f) as z:
                phi, A, psi = z["phi_h"].copy(), z["campo_A"].copy(), z["psi_h"].copy()
            g.A[...] = A
            eB = g.e * g.B()
            th, bu = theta_di(phi, m)
            Phi, okp = Phi_di(g, th, bu)
            rho = np.bincount(nodo, weights=np.sum(np.abs(psi) ** 2, axis=1), minlength=n)
            c1, c2, _x, _y = TO.centro(rho, m1, m2, L)
            dxy = np.asarray(TO.scarti(m1, m2, c1, c2, L))[:, :2]
            r = np.hypot(dxy[:, 0], dxy[:, 1])
            R = float(np.sqrt(np.sum(rho * r ** 2) / np.sum(rho)))
            pp = dxy[ii[g.P]].mean(axis=1)
            rp = np.hypot(pp[:, 0], pp[:, 1])
            print("-" * 134)
            print("### %s: %s" % (nome, f))
            print("  PRIMA LE GRANDEZZE: max |eB| %.4e, rms eB %.4e; max |Phi| %.4e, rms Phi %.4e; archi scartati %d su %d; placchette usate %d su %d; R %.3f" % (
                float(np.max(np.abs(eB))), float(np.sqrt(np.mean(eB ** 2))), float(np.max(np.abs(Phi[okp]))), float(np.sqrt(np.mean(Phi[okp] ** 2))),
                int((~bu).sum()), m, int(okp.sum()), len(okp), R))
            if float(np.max(np.abs(eB))) < 1e-6:
                print("  ### campo troppo debole: nessuna correlazione")
                esiti_stati.append((nome, None, None, None))
                continue
            sel = okp
            sp_tutte = spearman(Phi[sel], eB[sel])
            pe_tutte = float(np.corrcoef(Phi[sel], eB[sel])[0, 1])
            dentro = sel & (rp < 2.0 * R)
            sp_2R = spearman(Phi[dentro], eB[dentro])
            perm = np.array([spearman(Phi[dentro], rng.permutation(eB[dentro])) for _ in range(NPERM)])
            mu, sd = float(perm.mean()), float(perm.std())
            print("  tutte le placchette (%d): Pearson %+.4f, Spearman %+.4f" % (int(sel.sum()), pe_tutte, sp_tutte))
            print("  entro 2 R (%d placchette): Spearman %+.4f; il nullo (%d permutazioni): media %+.4f, 2 sigma %.4f -> %s" % (
                int(dentro.sum()), sp_2R, NPERM, mu, 2 * sd, "FUORI dal nullo" if abs(sp_2R - mu) > 2 * sd else "dentro il nullo"))
            frac = float(np.mean(np.abs(perm) < 0.1))
            esito("(K4) %s: il nullo copre, |Spearman| < 0.1 in almeno il 95%% delle permutazioni" % nome[:40], frac >= 0.95, "%.1f%%" % (100 * frac))
            for a in np.arange(0.0, min(4.0 * R, 0.5 * L), ANELLO):
                s = sel & (rp >= a) & (rp < a + ANELLO)
                if s.sum() > 10:
                    print("    l'anello [%5.1f, %5.1f): %5d placchette; Pearson %+.4f, Spearman %+.4f; rms Phi %.3e, rms eB %.3e" % (
                        a, a + ANELLO, int(s.sum()), float(np.corrcoef(Phi[s], eB[s])[0, 1]), spearman(Phi[s], eB[s]), float(np.sqrt(np.mean(Phi[s] ** 2))), float(np.sqrt(np.mean(eB[s] ** 2)))))
            esiti_stati.append((nome, sp_2R, abs(sp_2R - mu) > 2 * sd, sp_tutte))
        Z["metti"]()
    print("=" * 134)
    validi = [x for x in esiti_stati if x[1] is not None]
    si = [x for x in validi if abs(x[1]) > 0.5 and x[2]]
    no = all(abs(x[1]) < 0.2 for x in validi)
    ver = "SI'" if len(si) >= 2 else ("NO" if no else "ALTRO")
    for nome, s2, fuori, st in esiti_stati:
        print("### %s: Spearman entro 2 R %s%s" % (nome, "%+.4f" % s2 if s2 is not None else "-", (" (fuori dal nullo)" if fuori else " (dentro il nullo)") if s2 is not None else ""))
    print("### IL VERDETTO (le soglie di Luca): %s" % ver)
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
