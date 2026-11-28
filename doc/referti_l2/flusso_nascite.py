# -*- coding: utf-8 -*-
r"""**[M1058] H-1: IL DIFETTO DI FLUSSO DELLE NASCITE DI C** *(DECISIONE DI LUCA, 2026-11-28 10:58, punto 1; la carta `doc/CARTA_mitosi.md`,
«H-1, IL CONTO DEL DIFETTO DI FLUSSO DELLE NASCITE DI C»; a costo zero, nessun tick)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/flusso_nascite.py > doc/referti_l2/flusso_nascite.txt

`theta_a = arg(f[a,1] conj f[a,0])` *(G)*; `Phi_p` sui 3-cicli; `delta_p = pi - |Phi_p|`; `tau = 3 rms(delta)` sul vuoto fresco; un difetto e'
`delta_p > tau`. **Casi noti:** K-H1a *(il fresco: 0 difetti)*, K-H1c *(il gauge su phi)*, K-H1n *(DEVE FALLIRE: una fase su un'estremita')*,
K-H1b *(una nascita a mano nel fresco: stampata)*. **M1:** gli stati di `M0026/C` da 11500 a 16250, i nati contro il fondo. **M2:** ogni nascita
rigiocata SOLA sullo stato precedente *(`nasci_array`, `flip_array`)*, i triangoli nuovi contro il fondo; la lettura con 2 e 1 sigma binomiali.
"""
import collections
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import corpo_fuso_mitosi as CFM  # noqa: E402  (### anche il percorso di csv/, per _presidio)

MR, MR2, RV = CFM.MR, CFM.MR2, CFM.RV
CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
D_C = os.path.join(CTRL, "M0026", "C")
K_DA, K_A, OGNI = 11500, 16250, 250
SCARTO = 1e-6
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def adiacenza(ii, jj):
    adj = collections.defaultdict(set)
    for a, b in zip(np.asarray(ii).tolist(), np.asarray(jj).tolist()):
        adj[a].add(b)
        adj[b].add(a)
    return adj


def triangoli(adj, solo=None):
    """### i 3-cicli *(tutti, o solo quelli che contengono un nodo di `solo`)*, come terne ordinate."""
    out = set()
    sorgenti = adj.keys() if solo is None else solo
    for a in sorgenti:
        for b in adj[a]:
            for c in adj[a] & adj[b]:
                out.add(tuple(sorted((a, b, c))))
    return sorted(out)


def delta_di(ii, jj, phi, tri):
    """### `delta_p = pi - |Phi_p|` per le terne `tri`; `nan` se un arco e' scartato."""
    ii, jj = np.asarray(ii), np.asarray(jj)
    m = len(ii)
    f = np.asarray(phi).reshape(m, 2)
    th = np.angle(f[:, 1] * np.conj(f[:, 0]))
    buono = np.minimum(np.abs(f[:, 0]), np.abs(f[:, 1])) >= SCARTO
    chiave = {(min(a, b), max(a, b)): q for q, (a, b) in enumerate(zip(ii.tolist(), jj.tolist()))}

    def t(x, y):
        q = chiave[(min(x, y), max(x, y))]
        return (th[q] if ii[q] == x else -th[q]), buono[q]
    out = np.empty(len(tri))
    for p, (a, b, c) in enumerate(tri):
        (t1, b1), (t2, b2), (t3, b3) = t(a, b), t(b, c), t(c, a)
        out[p] = math.pi - abs(float(np.angle(np.exp(1j * (t1 + t2 + t3))))) if (b1 and b2 and b3) else float("nan")
    return out


def nasci(ii, jj, phi, nodi, a, lato):
    """### la sola nascita *(nessun tick)*: il grafo e `phi` dopo `nasci_array`, poi (se c'e' il lato) `flip_array`. `(ii3, jj3, phi3, m)`."""
    n = nodi["n"]
    keep = np.ones(len(ii), dtype=bool)
    keep[a] = False
    ii2 = np.concatenate([np.asarray(ii)[keep], [n] * 4])
    jj2 = np.concatenate([np.asarray(jj)[keep], [nodi["i"], nodi["j"], nodi["k"], nodi["l"]]])
    phi2 = MR.nasci_array(np.asarray(ii), np.asarray(jj), a, nodi, np.asarray(phi), "ampiezza")
    if lato is None:
        return ii2, jj2, phi2, None
    x, y = lato
    com = MR.vicini(ii2, jj2, x) & MR.vicini(ii2, jj2, y)
    m = int(sorted(com - {n})[0])
    phi3 = MR.flip_array(ii2, jj2, dict(nodi, m=m), x, y, m, phi2, "ampiezza", "stella")
    e = MR.arco_fra(ii2, jj2, x, y)
    k3 = np.ones(len(ii2), dtype=bool)
    k3[e] = False
    return np.concatenate([ii2[k3], [n]]), np.concatenate([jj2[k3], [m]]), phi3, m


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(__file__)
    print("=" * 134)
    print("[M1058] H-1: IL DIFETTO DI FLUSSO DELLE NASCITE DI C (M0026/C, da %d a %d); nessun tick" % (K_DA, K_A))
    print("=" * 134)
    with CFM.V6.GD.TC.scena() as Z:
        mot = Z["mot"]
        nodo0 = np.asarray(mot.inc.nodo)
        ii0, jj0, n0, L = nodo0[0::2].astype(np.int64), nodo0[1::2].astype(np.int64), int(mot.inc.n), int(Z["L"])
        m1s, m2s = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        pv = np.asarray(Z["phi_v"]).copy()
        ori0 = RV.ori_toro(Z)
        Z["metti"]()
    adj0 = adiacenza(ii0, jj0)
    T0 = triangoli(adj0)
    d0 = delta_di(ii0, jj0, pv, T0)
    sigma = float(np.sqrt(np.nanmean(d0 ** 2)))
    tau = 3.0 * sigma
    print("  il vuoto fresco (phi_v, A = 0): %d triangoli; delta: max %.3e, rms (sigma) %.3e; tau = 3 sigma = %.3e" % (len(T0), float(np.nanmax(d0)), sigma, tau))
    esito("(K-H1a) il vuoto fresco: la frazione di difetti (delta > tau) e' 0", int(np.sum(d0 > tau)) == 0, "%d su %d" % (int(np.sum(d0 > tau)), len(T0)))
    rng = np.random.default_rng(20261128)
    chi = rng.uniform(-math.pi, math.pi, n0)
    dg = delta_di(ii0, jj0, pv * np.exp(1j * chi[nodo0]), T0)
    esito("(K-H1c) il gauge su phi (e^{i chi_v} su tutte le estremita' del nodo): delta invariato entro 1e-10", float(np.nanmax(np.abs(dg - d0))) < 1e-10, "%.2e" % float(np.nanmax(np.abs(dg - d0))))
    pn = pv.copy()
    pn[0] = pn[0] * np.exp(0.5j * math.pi)
    dn = delta_di(ii0, jj0, pn, T0)
    esito("(K-H1n) DEVE FALLIRE: pi/2 su UNA estremita': la frazione di difetti NON e' piu' 0", int(np.sum(dn > tau)) > 0, "%d difetti" % int(np.sum(dn > tau)))
    # ### K-H1b: la nascita a mano nel fresco, sull'arco piu' vicino al centro della scena
    mid1 = 0.5 * (m1s[ii0] + m1s[jj0])
    mid2 = 0.5 * (m2s[ii0] + m2s[jj0])
    a = int(np.argmin((mid1 - L / 2) ** 2 + (mid2 - L / 2) ** 2))
    i, j, k, l = MR2.indici_nascita_v2(ii0, jj0, ori0, a)
    nodi = {"i": i, "j": j, "k": k, "l": l, "n": n0}
    for lato in (None, (i, k)):
        ii3, jj3, ph3, m = nasci(ii0, jj0, pv, nodi, a, lato)
        Tn = triangoli(adiacenza(ii3, jj3), solo=[n0])
        dd = delta_di(ii3, jj3, ph3, Tn)
        print("  (K-H1b) la nascita a mano sull'arco %d (%d - %d), %s: i triangoli col nato %s; delta %s; difetti %d su %d" % (
            a, i, j, "senza flip" if lato is None else "col flip %d - %d (m %d)" % (lato[0], lato[1], m), Tn, ["%.3e" % v for v in dd], int(np.sum(dd > tau)), len(dd)))
    print("-" * 134)
    # ### M1 e M2
    B = json.load(open(os.path.join(D_C, "nascite.json"), encoding="utf-8"))
    M1, M2 = [], []
    salt = collections.Counter()
    nuovi_d, attesi = [], []
    for ks in range(K_DA, K_A + 1, OGNI):
        with np.load(os.path.join(D_C, "stato_%06d.npz" % ks)) as z:
            phi, psi = z["phi_h"], z["psi_h"]
            if "ii" in z.files:
                ii, jj, m1, m2 = z["ii"].astype(np.int64), z["jj"].astype(np.int64), z["m1"], z["m2"]
            else:
                ii, jj, m1, m2 = ii0, jj0, m1s, m2s
        n = len(m1)
        nodo = np.empty(2 * len(ii), dtype=np.int64)
        nodo[0::2], nodo[1::2] = ii, jj
        rho = np.bincount(nodo, weights=np.sum(np.abs(psi) ** 2, axis=1), minlength=n)
        c1, c2, _x, _y = TO.centro(rho, m1, m2, L)
        dxy = np.asarray(TO.scarti(m1, m2, c1, c2, L))[:, :2]
        adj = adiacenza(ii, jj)
        T = triangoli(adj)
        Ta = np.array(T)
        dT = delta_di(ii, jj, phi, T)
        tocca = np.any(Ta >= n0, axis=1)
        rT = np.hypot(*dxy[Ta].mean(axis=1).T)
        if tocca.any():
            rmax = float(rT[tocca].max())
            fondo = (~tocca) & (rT <= rmax)
            fN, fF, fT = float(np.nanmean(dT[tocca] > tau)), float(np.nanmean(dT[fondo] > tau)), float(np.nanmean(dT > tau))
            M1.append((ks, int(tocca.sum()), fN, int(fondo.sum()), fF, fT, rmax))
        # ### M2: le nascite dell'intervallo (ks, ks + 250], rigiocate SOLE su questo stato
        for b in B:
            if not (ks < b["k"] <= ks + OGNI):
                continue
            nd = b["nodi"]
            i, j = nd["i"], nd["j"]
            if j not in adj[i] or adj[i] & adj[j] != {nd["k"], nd["l"]}:
                salt["l'arco o la stella non c'e' nello stato"] += 1
                continue
            a = MR.arco_fra(ii, jj, i, j)
            lato = None
            if b["scelto"] >= 0:
                lato = ((i, nd["k"]), (j, nd["k"]), (j, nd["l"]), (i, nd["l"]))[b["scelto"]]
            nodi = {x: nd[x] for x in ("i", "j", "k", "l")}
            nodi["n"] = n
            ii3, jj3, ph3, m = nasci(ii, jj, phi, nodi, a, lato)
            if lato is not None and m != nd.get("m"):
                salt["la m non e' quella registrata"] += 1
                continue
            Tn = triangoli(adiacenza(ii3, jj3), solo=[n])
            dd = delta_di(ii3, jj3, ph3, Tn)
            dp = np.asarray(TO.scarti(np.array([b["pos"][0]]), np.array([b["pos"][1]]), c1, c2, L))[0, :2]
            rb = float(np.hypot(*dp))
            fondo = (~tocca) & (rT <= max(rb, 1.0))
            p = float(np.nanmean(dT[fondo] > tau)) if fondo.any() else float("nan")
            nuovi_d.extend(dd.tolist())
            attesi.extend([p] * len(dd))
            M2.append((b["k"], len(dd), int(np.sum(dd > tau)), p, rb))
    print("### M1, gli stati salvati: (k) le placchette dei nati e la frazione di difetti; il fondo entro lo stesso raggio; tutte")
    for ks, nN, fN, nF, fF, fT, rmax in M1:
        if ks % 1000 == 0 or ks == K_A:
            print("    k %5d: nati %5d placchette, difetti %.4f; fondo (r <= %.1f) %6d, difetti %.4f; tutte %.4f" % (ks, nN, fN, rmax, nF, fF, fT))
    print("### M2, la misura pulita: %d nascite rigiocate su %d del registro fra %d e %d; saltate %s" % (len(M2), sum(1 for b in B if K_DA < b["k"] <= K_A + OGNI), K_DA, K_A + OGNI, dict(salt)))
    nd_ = np.array(nuovi_d)
    pa = np.array(attesi)
    ok = ~np.isnan(nd_) & ~np.isnan(pa)
    oss = float(np.mean(nd_[ok] > tau))
    pm = float(np.mean(pa[ok]))
    sg = math.sqrt(pm * (1 - pm) / ok.sum()) if 0 < pm < 1 else float("nan")
    if sg == sg and sg > 0:
        z = (oss - pm) / sg
    else:
        z = float("inf") if oss > pm else 0.0
    print("  i triangoli nuovi: %d; difetti %.4f; il fondo atteso (entro il raggio della nascita) %.4f; 1 sigma binomiale %.4f; lo scarto %.2f sigma" % (int(ok.sum()), oss, pm, sg, z))
    for x in M2[:5]:
        print("    k %5d: %d triangoli nuovi, %d difetti; fondo %.4f; r %.2f" % x)
    ver = "FA DIFETTI" if z > 2 else ("NON LI FA" if z < 1 else "NON DECIDIBILE")
    print("### H-1, IL VERDETTO (la carta: > 2 sigma FA, < 1 sigma NON LI FA): %s" % ver)
    if M1:
        print("### lo smaltimento: sui nati negli stati salvati la frazione media %.4f (M1), subito dopo la nascita %.4f (M2)" % (float(np.mean([x[2] for x in M1])), oss))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
