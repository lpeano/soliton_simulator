# -*- coding: utf-8 -*-
r"""**[M1205] I BUCHI DI phi DELLE NASCITE DI C: QUANTI RESTANO** *(DECISIONE DI LUCA, 2026-11-28 12:05, punto 2; la carta `doc/CARTA_mitosi.md`,
«H-1 CHIUSO; LA LETTURA DEI BUCHI DI phi CHE RESTANO»; nessun tick)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/buchi_phi.py > doc/referti_l2/buchi_phi.txt

`|phi|` d'arco = `min |f[a,:]|`; un buco `< 1e-6` *(e `< 1e-3`)*. **B1:** gli stati di `M0026/C` 11500..16250, i nati *(e `n - k`, `n - l`)* contro il
fondo allo stesso raggio, KS a due campioni. **B2:** ogni nascita rigiocata sola sullo stato precedente *(`flusso_nascite.nasci`)*. **Casi noti:**
K-B1 *(la nascita sola nel fresco: 2 su 4, `n - k` e `n - l`)*, K-B2 *(il fresco: 0 buchi)*, K-B3 *(KS sintetico)*.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import flusso_nascite as FN  # noqa: E402

CFM, MR, MR2, RV = FN.CFM, FN.MR, FN.MR2, FN.RV
D_C = FN.D_C
K_DA, K_A, OGNI = 11500, 16250, 250
B6, B3 = 1e-6, 1e-3
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def ampiezze(phi, m):
    f = np.asarray(phi).reshape(m, 2)
    return np.minimum(np.abs(f[:, 0]), np.abs(f[:, 1]))


def main():
    import _presidio
    from scipy.stats import ks_2samp
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "flusso_nascite.py"))
    _presidio.avvia(__file__)
    print("=" * 134)
    print("[M1205] I BUCHI DI phi DELLE NASCITE DI C (M0026/C, da %d a %d): buco |phi| < %.0e (e < %.0e); nessun tick" % (K_DA, K_A, B6, B3))
    print("=" * 134)
    with CFM.V6.GD.TC.scena() as Z:
        nodo0 = np.asarray(Z["mot"].inc.nodo)
        ii0, jj0, n0, L = nodo0[0::2].astype(np.int64), nodo0[1::2].astype(np.int64), int(Z["mot"].inc.n), int(Z["L"])
        m1s, m2s = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        pv = np.asarray(Z["phi_v"]).copy()
        ori0 = RV.ori_toro(Z)
        Z["metti"]()
    a0 = ampiezze(pv, len(ii0))
    esito("(K-B2) il vuoto fresco: 0 buchi", int(np.sum(a0 < B6)) == 0, "|phi| da %.3e a %.3e" % (float(a0.min()), float(a0.max())))
    a = 39123
    i, j, k, l = MR2.indici_nascita_v2(ii0, jj0, ori0, a)
    ii3, jj3, ph3, _m = FN.nasci(ii0, jj0, pv, {"i": i, "j": j, "k": k, "l": l, "n": n0}, a, None)
    an = ampiezze(ph3, len(ii3))[-4:]
    buchi = [int(jj3[len(ii3) - 4 + q]) for q in range(4) if an[q] < B6]
    esito("(K-B1) la nascita sola nel fresco (l'arco %d): 2 archi su 4 sotto 1e-6, e sono n - k, n - l" % a, sorted(buchi) == sorted([k, l]),
          "|phi| %s; i buchi verso %s (k %d, l %d)" % (["%.2e" % v for v in an], buchi, k, l))
    rng = np.random.default_rng(20261128)
    p_s = ks_2samp(rng.normal(0, 1, 2000), rng.normal(0, 1, 2000)).pvalue
    p_d = ks_2samp(rng.normal(0, 1, 2000), rng.normal(0.5, 1, 2000)).pvalue
    esito("(K-B3) KS sintetico: la stessa legge p > 0.01, la legge spostata di 0.5 p < 1e-6", p_s > 0.01 and p_d < 1e-6, "p %.3f e %.2e" % (p_s, p_d))
    print("-" * 134)
    B = json.load(open(os.path.join(D_C, "nascite.json"), encoding="utf-8"))
    print("### B1, gli stati salvati: (k) gli archi dei nati, i buchi < 1e-6 e < 1e-3; n - k, n - l del registro; il fondo; KS nati contro fondo")
    righe, b2 = [], []
    for ks in range(K_DA, K_A + 1, OGNI):
        with np.load(os.path.join(D_C, "stato_%06d.npz" % ks)) as z:
            phi, psi = z["phi_h"], z["psi_h"]
            if "ii" in z.files:
                ii, jj, m1, m2 = z["ii"].astype(np.int64), z["jj"].astype(np.int64), z["m1"], z["m2"]
            else:
                ii, jj, m1, m2 = ii0, jj0, m1s, m2s
        n = len(m1)
        amp = ampiezze(phi, len(ii))
        nodo = np.empty(2 * len(ii), dtype=np.int64)
        nodo[0::2], nodo[1::2] = ii, jj
        rho = np.bincount(nodo, weights=np.sum(np.abs(psi) ** 2, axis=1), minlength=n)
        c1, c2, _x, _y = TO.centro(rho, m1, m2, L)
        dxy = np.asarray(TO.scarti(m1, m2, c1, c2, L))[:, :2]
        rA = np.hypot(*(0.5 * (dxy[ii] + dxy[jj])).T)
        nati = (ii >= n0) | (jj >= n0)
        if nati.any():
            chiave = {(min(x, y), max(x, y)): q for q, (x, y) in enumerate(zip(ii.tolist(), jj.tolist()))}
            kl = [chiave[(min(b["nodi"]["n"], c), max(b["nodi"]["n"], c))] for b in B if b["k"] <= ks for c in (b["nodi"]["k"], b["nodi"]["l"])
                  if (min(b["nodi"]["n"], c), max(b["nodi"]["n"], c)) in chiave]
            kl = np.array(kl, dtype=np.int64)
            fondo = (~nati) & (rA <= float(rA[nati].max()))
            ks2 = ks_2samp(amp[nati], amp[fondo])
            r = (ks, int(nati.sum()), float(np.mean(amp[nati] < B6)), float(np.mean(amp[nati] < B3)), len(kl), float(np.mean(amp[kl] < B6)) if len(kl) else float("nan"),
                 float(np.mean(amp[kl] < B3)) if len(kl) else float("nan"), int(fondo.sum()), float(np.mean(amp[fondo] < B6)), float(np.mean(amp[fondo] < B3)),
                 float(np.median(amp[nati])), float(np.median(amp[fondo])), float(ks2.statistic), float(ks2.pvalue))
            righe.append(r)
            if ks % 1000 == 0 or ks == K_A:
                print("    k %5d: nati %5d archi, buchi %.4f (< 1e-3 %.4f); n-k/n-l %4d, buchi %.4f (< 1e-3 %.4f); fondo %5d, buchi %.4f (< 1e-3 %.4f); mediane %.3e / %.3e; KS D %.3f p %.2e" % r)
        # ### B2: le nascite dell'intervallo rigiocate sole su questo stato
        adj = FN.adiacenza(ii, jj)
        for b in B:
            if not (ks < b["k"] <= ks + OGNI):
                continue
            nd = b["nodi"]
            if nd["j"] not in adj[nd["i"]] or adj[nd["i"]] & adj[nd["j"]] != {nd["k"], nd["l"]}:
                continue
            aa = MR.arco_fra(ii, jj, nd["i"], nd["j"])
            lato = ((nd["i"], nd["k"]), (nd["j"], nd["k"]), (nd["j"], nd["l"]), (nd["i"], nd["l"]))[b["scelto"]] if b["scelto"] >= 0 else None
            ii3, jj3, ph3, m = FN.nasci(ii, jj, phi, {"i": nd["i"], "j": nd["j"], "k": nd["k"], "l": nd["l"], "n": n}, aa, lato)
            if lato is not None and m != nd.get("m"):
                continue
            am = ampiezze(ph3, len(ii3))
            nuovi = (ii3 == n) | (jj3 == n)
            q_kl = [q for q in np.nonzero(nuovi)[0] if {int(ii3[q]), int(jj3[q])} & {nd["k"], nd["l"]}]
            b2.append((int(nuovi.sum()), int(np.sum(am[nuovi] < B6)), int(np.sum(am[nuovi] < B3)), len(q_kl), int(np.sum(am[q_kl] < B6)), float(np.median(am[nuovi]))))
    B2 = np.array(b2, dtype=float)
    print("### B2, subito dopo la nascita (rigiocata sola sullo stato precedente): %d nascite; archi nuovi %d; buchi < 1e-6 %d (%.4f), < 1e-3 %d (%.4f); sugli archi verso k, l %d su %d; la mediana di |phi| sui nuovi %.3e" % (
        len(B2), int(B2[:, 0].sum()), int(B2[:, 1].sum()), B2[:, 1].sum() / B2[:, 0].sum(), int(B2[:, 2].sum()), B2[:, 2].sum() / B2[:, 0].sum(),
        int(B2[:, 4].sum()), int(B2[:, 3].sum()), float(np.median(B2[:, 5]))))
    R = np.array([r[1:] for r in righe], dtype=float)
    print("### B1, la media sugli stati: buchi sui nati %.4f (< 1e-3 %.4f); su n-k/n-l %.4f (< 1e-3 %.4f); sul fondo %.4f (< 1e-3 %.4f); KS p massimo %.2e" % (
        float(R[:, 1].mean()), float(R[:, 2].mean()), float(np.nanmean(R[:, 4])), float(np.nanmean(R[:, 5])), float(R[:, 7].mean()), float(R[:, 8].mean()), float(R[:, 12].max())))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
