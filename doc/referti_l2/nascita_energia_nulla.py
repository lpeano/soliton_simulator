# -*- coding: utf-8 -*-
r"""**LA NASCITA NEL GUSCIO A ENERGIA NULLA** *(Luca `2026-11-20` `10:31`, TODO 2; la carta `doc/TASK_HISTORY/2026-11-20_nascita_energia_nulla.md`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/nascita_energia_nulla.py parte K 3      (K = 0, 1, 2)
    E:\python\py3132\python.exe doc/referti_l2/nascita_energia_nulla.py det A          (A = a, b: due processi)
    E:\python\py3132\python.exe doc/referti_l2/nascita_energia_nulla.py referto > doc/referti_l2/nascita_energia_nulla.txt

**La famiglia** *(la carta, 1.2)*: `alpha` = la frazione della norma del padre `i` che passa al nodo nuovo `n`, in unita' di D7: **le estremita' di `i` divise per `sqrt(2/(2 - alpha))`, le `4` di `n` a `sqrt(alpha)` volte quelle di D7**; il resto come `nascita_dentro_fuori.nasci`; **`phi` con FA** *(`regole_fase_F3.regola`)*. **`alpha = 1` = D7; `alpha = 0` = `psi` trasportata senza dividerla.**
**La radice** *(1.4)*: bisezione a `53` passi fissi sul `DH` delle cinque famiglie scritte a mano *(`U = I`)*; alla radice `DH` col conto PIENO *(`nascita_dentro_fuori.famiglie`)*.
**Lo stato:** C2 a `k 3000` *(NON quello allo scatto: dichiarato)*; **i candidati** `candidati.npz` *(`torsione_segmenti.py`)*, nell'ordine di scatto.
**Il caso noto** *(Q-A4)*: a `alpha = 1`, sui primi `20` archi, `psi` e ogni termine di `DH` AL BIT con `regole_fase_F3.nascita(..., "FA")`.
"""
import hashlib
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "mattone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import regole_fase_F3 as RF  # noqa: E402  (aggiunge al percorso csv/, csv/solitone/, primo_ordine/)
import nascita_dentro_fuori as ND  # noqa: E402

PASSI = 53
GRIGLIA = np.linspace(0.0, 1.0, 11)
N_CASO = 20
N_DET = 100
N_FILA = 20
N_SPECCHIO = 200
SOGLIA_SPECCHIO = 1e-10
DIR_T = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "torsione")
DIR_O = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "nascita_nulla")
STATO = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "C2", "stato_03000.npz")
CHIAVI = ("G_psi", "a_psi", "N", "G_phi", "a_phi", "tot")


# ---------------------------------------------------------------------------------------------- la famiglia
def preparo(G, psi, phi, a):
    """### tutto cio' che NON dipende da `alpha`: il grafo, `phi` con FA, e la `psi` prima di D7."""
    ii, jj, nn, vec = G
    with np.errstate(invalid="ignore", divide="ignore"):
        out = ND.nasci(G, psi, phi, a)
        ph = RF.regola("FA", G, phi, a, out)
    G2 = out[0]
    keep = out[4]
    i = int(ii[a])
    m2 = len(G2[0])
    base = m2 - 4
    p0 = np.zeros((2 * m2, 2), dtype=complex)
    e = np.repeat(keep, 2)
    p0[:2 * base] = psi[e]
    p0[2 * (base + 0) + 1] = psi[2 * a]
    p0[2 * (base + 1) + 1] = psi[2 * a + 1]
    hp = np.where(ND.nodo_h(G2[0], G2[1]) == i)[0]
    Np = float(np.sum(np.abs(p0[hp]) ** 2))
    chi = p0[hp].sum(axis=0)
    return {"G2": G2, "ph": ph, "p0": p0, "hp": hp, "Np": Np, "chi": chi, "base": base, "out": out}


def psi_alpha(P, alpha):
    """### `psi` dopo la nascita per `alpha` (a `alpha = 1` le operazioni di D7 nello stesso ordine)."""
    psi2 = P["p0"].copy()
    psi2[P["hp"]] /= math.sqrt(2.0 / (2.0 - alpha))
    nc = np.linalg.norm(P["chi"])
    for q in range(4):
        h = 2 * (P["base"] + q)
        psi2[h] = (math.sqrt(alpha) * (1.0 / math.sqrt(2.0))) * math.sqrt(P["Np"] / 4.0) * P["chi"] / nc if nc > 0 else 0.0
    return psi2


def F_mano(G, psi, phi):
    """### le cinque famiglie di `nascita_dentro_fuori.famiglie` scritte a mano, SENZA il motore (`U = I`)."""
    import energia_pesata as EP
    import materia_vuoto as MV
    ii, jj, nn, _v = G
    nodo = ND.nodo_h(ii, jj)
    Om = EP.OMEGA_H
    d = np.bincount(nodo, minlength=nn).astype(float)
    nrm_psi = np.bincount(nodo, weights=np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2, minlength=nn)
    nrm_phi = np.bincount(nodo, weights=np.abs(phi) ** 2, minlength=nn)
    S2 = np.zeros(nn)
    for c in (0, 1):
        S2 += np.bincount(nodo, weights=psi[:, c].real, minlength=nn) ** 2 + np.bincount(nodo, weights=psi[:, c].imag, minlength=nn) ** 2
    Sf2 = np.bincount(nodo, weights=phi.real, minlength=nn) ** 2 + np.bincount(nodo, weights=phi.imag, minlength=nn) ** 2
    w = psi.reshape(len(ii), 2, 2)
    f = phi.reshape(len(ii), 2)
    F = {"G_psi": float(np.sum(-Om * (0.5 * nrm_psi - S2 / d))),
         "a_psi": float(np.sum(Om * np.real(np.conj(w[:, 0, 0]) * w[:, 1, 0] + np.conj(w[:, 0, 1]) * w[:, 1, 1]))),
         "N": float(np.sum(MV.N(nrm_psi, nrm_phi))),
         "G_phi": float(np.sum(-Om * (0.5 * nrm_phi - Sf2 / d))),
         "a_phi": float(np.sum(Om * np.real(np.conj(f[:, 0]) * f[:, 1])))}
    F["tot"] = F["G_psi"] + F["a_psi"] + F["N"] + F["G_phi"] + F["a_phi"]
    return F


def radice(f, f0, f1):
    """### la bisezione a `PASSI` fissi; `(alpha*, stato)`: `0` la radice, `1` nessuna (lo stesso segno), `2` un estremo esatto."""
    if f0 == 0.0:
        return 0.0, 2
    if f1 == 0.0:
        return 1.0, 2
    if (f0 > 0) == (f1 > 0):
        return float("nan"), 1
    lo, hi, flo = 0.0, 1.0, f0
    for _ in range(PASSI):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm == 0.0:
            return mid, 0
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi), 0


def nascita(G, psi, phi, a, F0m, F0p, pieno=True):
    """### la nascita sull'arco `a` alla radice: il dizionario dei risultati, e `(G2, psi2, ph)` alla radice."""
    P = preparo(G, psi, phi, a)
    G2, ph = P["G2"], P["ph"]
    if not np.all(np.isfinite(ph)):
        return {"stato": 3}, None

    def dh(al):
        return F_mano(G2, psi_alpha(P, al), ph)["tot"] - F0m["tot"]
    g = np.array([dh(float(x)) for x in GRIGLIA])
    al, stato = radice(dh, float(g[0]), float(g[-1]))
    R = {"stato": stato, "DH0": float(g[0]), "DH1": float(g[-1]), "alpha": al,
         "cambi": int(np.sum(np.sign(g[1:]) != np.sign(g[:-1]))), "chi0": bool(np.linalg.norm(P["chi"]) == 0.0)}
    if stato == 1:
        return R, None
    psi2 = psi_alpha(P, al)
    Fm = F_mano(G2, psi2, ph)
    R["DHmano"] = Fm["tot"] - F0m["tot"]
    if pieno:
        Fp = ND.famiglie(G2, psi2, ph)
        Dl = ND.delta(F0p, Fp)
        for k in CHIAVI:
            R["DH_" + k] = Dl[k]
        R["ctrl"] = Fp["ctrl"]
        R["Hp"] = Fp["tot"]
    return R, (G2, psi2, ph)


# ---------------------------------------------------------------------------------------------- lo stato
def carica():
    import _massa_nei_difetti as MD
    import convergenza as CV
    import prova_scatola5 as PS
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        ii, jj, nn, dirs = MD.toro(186)
        assert np.array_equal(np.asarray(Z["mot"].inc.ii), ii) and np.array_equal(np.asarray(Z["mot"].inc.jj), jj), "l'ordine degli archi della scena non e' quello del toro"
        Z["metti"]()
    with np.load(STATO) as d:
        psi, phi = d["psi_h"].copy(), d["phi_h"].copy()
    with np.load(os.path.join(DIR_T, "candidati.npz")) as d:
        archi, r, Tk, centro = d["archi"].copy(), d["r"].copy(), d["T"].copy(), d["centro"].copy()
    o = np.argsort(Tk, kind="stable")
    return (ii, jj, nn, np.asarray(dirs, dtype=float)), psi, phi, archi[o], r[o], Tk[o], centro


CAMPI = ("stato", "DH0", "DH1", "alpha", "cambi", "chi0", "DHmano", "ctrl", "Hp") + tuple("DH_" + k for k in CHIAVI)


def tabella(Rs):
    return {c: np.array([R.get(c, np.nan) for R in Rs], dtype=float) for c in CAMPI}


def sha(T):
    h = hashlib.sha1()
    for c in CAMPI:
        h.update(np.ascontiguousarray(T[c]).tobytes())
    return h.hexdigest()[:12]


def fila(G, psi, phi, archi, F0p):
    """### `N_FILA` nascite in fila alla radice, sugli archi in ordine di scatto; `H` pieno dopo ognuna."""
    righe, saltati = [], {"diviso": 0, "senza_radice": 0, "non_triangolo": 0}
    H = [F0p["tot"]]
    Gc, pc, fc = G, psi, phi
    Fm, Fp = F_mano(Gc, pc, fc), F0p
    for a0 in archi:
        if len(righe) >= N_FILA:
            break
        i, j = int(G[0][a0]), int(G[1][a0])
        q = np.where((Gc[0] == i) & (Gc[1] == j))[0]
        if len(q) == 0:
            saltati["diviso"] += 1
            continue
        try:
            R, nuovo = nascita(Gc, pc, fc, int(q[0]), Fm, Fp)
        except AssertionError:
            saltati["non_triangolo"] += 1
            continue
        if nuovo is None:
            saltati["senza_radice"] += 1
            continue
        Gc, pc, fc = nuovo
        Fp = ND.famiglie(Gc, pc, fc)
        Fm = F_mano(Gc, pc, fc)
        H.append(Fp["tot"])
        righe.append((int(a0), i, j, R["alpha"], R["DH_tot"], abs(H[-1] - H[-2]) / abs(H[-2]), Gc[2]))
    return righe, saltati, np.array(H)


def corri(sel, nome):
    import _presidio
    _presidio.avvia(__file__)
    os.makedirs(DIR_O, exist_ok=True)
    G, psi, phi, archi, r, Tk, centro = carica()
    assert len(archi) == 2929 and max(sel) < len(archi), "i candidati non sono i 2929 di torsione_segmenti.txt"
    F0m, F0p = F_mano(G, psi, phi), ND.famiglie(G, psi, phi)
    print("### %s: %d archi; H dello stato (il conto pieno) %.10e, a mano %.10e" % (nome, len(sel), F0p["tot"], F0m["tot"]))
    Rs, t0 = [], time.time()
    for c, q in enumerate(sel):
        R, _n = nascita(G, psi, phi, int(archi[q]), F0m, F0p)
        Rs.append(R)
        if c % 100 == 0:
            print("    %d su %d (%.0f s)" % (c, len(sel), time.time() - t0))
            sys.stdout.flush()
    T = tabella(Rs)
    extra = {}
    if nome.startswith("det"):
        righe, saltati, H = fila(G, psi, phi, archi, F0p)
        extra = {"fila": np.array([x[:6] for x in righe], dtype=float), "fila_H": H}
        print("### la fila: %d nascite, saltati %s" % (len(righe), saltati))
    np.savez(os.path.join(DIR_O, nome + ".npz"), sel=np.asarray(sel), tempo=time.time() - t0, **T, **extra)
    print("### %s: lo sha1 dei risultati %s; %.0f s" % (nome, sha(T), time.time() - t0))
    return 0


# ---------------------------------------------------------------------------------------------- il referto
def caso_noto(G, psi, phi, archi, F0p, esiti):
    ok_psi, ok_dh = True, True
    for a in archi[:N_CASO]:
        Dl, out = RF.nascita(G, psi, phi, int(a), "FA")
        P = preparo(G, psi, phi, int(a))
        psi2 = psi_alpha(P, 1.0)
        ok_psi &= bool(np.array_equal(psi2, out[1]))
        Dm = ND.delta(F0p, ND.famiglie(P["G2"], psi2, P["ph"]))
        ok_dh &= all(Dm[k] == Dl[k] for k in CHIAVI)
    print("### IL CASO NOTO (alpha = 1 contro regole_fase_F3.nascita FA, i primi %d archi): psi al bit %s; ogni termine di dH al bit %s" % (N_CASO, ok_psi, ok_dh))
    esiti.append(("il caso noto: a alpha = 1 psi e ogni termine di dH = regole_fase_F3.nascita(FA) AL BIT (%d archi)" % N_CASO, ok_psi and ok_dh))
    return ok_psi and ok_dh


def specchio(G, psi, phi, archi, centro, F0m, F0p, esiti):
    import specchio_carta as SC
    from solitone import toro as TO
    ii, jj, nn, _v = G
    L = int(round(math.sqrt(nn)))
    v = np.arange(nn)
    A1, A2 = TO.vettori()
    d30 = 2 * A1 + A2
    ang = math.atan2(d30[1], d30[0])
    p0 = (int(round(float(centro[0]))), int(round(float(centro[1]))))
    sig, scarto, _M = SC.mappa_nodi(L, (v // L).astype(float), (v % L).astype(float), p0, ang)
    assert scarto < 1e-9 and np.array_equal(sig[sig], v), "la mappa dello specchio non e' un'involuzione del reticolo"
    ap, rov = SC.mappa_archi(ii, jj, sig)
    hp = np.empty(2 * len(ap), dtype=int)
    hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
    hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
    nodo = ND.nodo_h(ii, jj)
    assert np.array_equal(nodo[hp], sig[nodo]), "la mappa delle estremita' non porta il nodo giusto"
    psiR = np.empty_like(psi)
    psiR[hp] = psi
    phiR = np.empty_like(phi)
    phiR[hp] = phi
    FRm, FRp = F_mano(G, psiR, phiR), ND.famiglie(G, psiR, phiR)
    dH0 = abs(FRp["tot"] - F0p["tot"]) / abs(F0p["tot"])
    print("### LO SPECCHIO a 30 gradi per il nodo %s (lo scarto %.1e): H dello stato riflesso contro H, relativo %.3e" % (p0, scarto, dH0))
    esiti.append(("il controllo: H dello stato riflesso = H entro %.0e relativo" % SOGLIA_SPECCHIO, dH0 < SOGLIA_SPECCHIO))
    sc = {False: [], True: []}
    nega = []
    for a in archi[:N_SPECCHIO]:
        a = int(a)
        R1, _x = nascita(G, psi, phi, a, F0m, F0p, pieno=False)
        R2, _y = nascita(G, psiR, phiR, int(ap[a]), FRm, FRp, pieno=False)
        R3, _z = nascita(G, psi, phi, int(ap[a]), F0m, F0p, pieno=False)
        if 3 in (R1["stato"], R2["stato"], R3["stato"]):
            sc[bool(rov[a])].append(float("inf"))
            nega.append(float("inf"))
            continue
        scala = max(abs(R1["DH0"]), abs(R1["DH1"]))
        if R1["stato"] == 1 or R2["stato"] == 1:
            d = 0.0 if (R1["stato"] == R2["stato"]) else float("inf")
            dn = 0.0 if (R1["stato"] == R3["stato"]) else float("inf")
        else:
            d = max(abs(R1["alpha"] - R2["alpha"]), abs(R1["DH0"] - R2["DH0"]) / scala, abs(R1["DH1"] - R2["DH1"]) / scala)
            dn = max(abs(R1["alpha"] - R3["alpha"]) if R3["stato"] != 1 else float("inf"), abs(R1["DH0"] - R3["DH0"]) / scala, abs(R1["DH1"] - R3["DH1"]) / scala)
        sc[bool(rov[a])].append(d)
        nega.append(dn)
    for rv in (False, True):
        x = np.array(sc[rv])
        print("    gli archi a verso %s: %d; la differenza (alpha*, DH0 e DH1 relativi) max %.3e, mediana %.3e; sotto %.0e: %d" % (
            "ROVESCIATO" if rv else "conservato", x.size, float(np.max(x)) if x.size else float("nan"), float(np.median(x)) if x.size else float("nan"), SOGLIA_SPECCHIO, int(np.sum(x < SOGLIA_SPECCHIO))))
    x = np.array(nega)
    print("    DEVE FALLIRE, l'arco immagine nello stato NON riflesso: la differenza min %.3e; sotto %.0e: %d su %d" % (float(np.min(x)), SOGLIA_SPECCHIO, int(np.sum(x < SOGLIA_SPECCHIO)), x.size))
    cons = np.array(sc[False])
    esiti.append(("P5 sugli archi a verso conservato: la nascita alla radice equivariante entro %.0e (%d archi)" % (SOGLIA_SPECCHIO, cons.size), bool(cons.size) and bool(np.all(cons < SOGLIA_SPECCHIO))))
    rv = np.array(sc[True])
    esiti.append(("P-Z3, lo specchio su TUTTI i %d archi (anche i rovesciati) entro %.0e" % (N_SPECCHIO, SOGLIA_SPECCHIO), bool(np.all(cons < SOGLIA_SPECCHIO)) and bool(np.all(rv < SOGLIA_SPECCHIO))))
    esiti.append(("DEVE FALLIRE: l'arco immagine nello stato NON riflesso da' un'altra nascita (tutti sopra %.0e)" % SOGLIA_SPECCHIO, bool(np.all(x >= SOGLIA_SPECCHIO))))


def referto():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "regole_fase_F3.py"))
    _presidio.avvia(__file__)
    t00 = time.time()
    print("=" * 130)
    print("LA NASCITA NEL GUSCIO A ENERGIA NULLA (Luca 2026-11-20 10:31); lo stato di C2 a k 3000 (NON quello allo scatto: dichiarato)")
    print("=" * 130)
    G, psi, phi, archi, r, Tk, centro = carica()
    F0m, F0p = F_mano(G, psi, phi), ND.famiglie(G, psi, phi)
    print("### H dello stato: il conto pieno %.10e, a mano %.10e (relativo %.2e); %d candidati, r da %.2f a %.2f" % (
        F0p["tot"], F0m["tot"], abs(F0p["tot"] - F0m["tot"]) / abs(F0p["tot"]), len(archi), float(r.min()), float(r.max())))
    esiti = []
    print("-" * 130)
    if not caso_noto(G, psi, phi, archi, F0p, esiti):
        print("### IL CASO NOTO FALLISCE: FERMO")
    # ------------------------------------------------------------------ le parti
    print("-" * 130)
    parti = sorted(x for x in os.listdir(DIR_O) if x.startswith("parte_"))
    T = {c: np.full(len(archi), np.nan) for c in CAMPI}
    visti = np.zeros(len(archi), dtype=bool)
    tempi = []
    for p in parti:
        with np.load(os.path.join(DIR_O, p)) as d:
            s = d["sel"]
            for c in CAMPI:
                T[c][s] = d[c]
            visti[s] = True
            tempi.append((p, float(d["tempo"]), len(s)))
    print("### LE PARTI: %s; gli archi coperti %d su %d" % ([(p, "%.0f s" % t, n) for p, t, n in tempi], int(visti.sum()), len(archi)))
    st = T["stato"]
    rad = (st == 0) | (st == 2)
    n_rad = int(np.sum(rad))
    print("### ### LA RADICE ESISTE su %d archi su %d (%.2f%%); senza radice (DH(0) e DH(1) dello stesso segno) %d; indefiniti %d; chi = 0 %d" % (
        n_rad, len(archi), 100.0 * n_rad / len(archi), int(np.sum(st == 1)), int(np.sum(st == 3)), int(np.nansum(T["chi0"]))))
    print("    DH(0) (il trasporto): min %+.4e, mediana %+.4e, max %+.4e; DH(1) (D7): min %+.4e, mediana %+.4e, max %+.4e" % (
        np.nanmin(T["DH0"]), np.nanmedian(T["DH0"]), np.nanmax(T["DH0"]), np.nanmin(T["DH1"]), np.nanmedian(T["DH1"]), np.nanmax(T["DH1"])))
    al = T["alpha"][rad]
    if n_rad:
        print("    alpha*: min %.6f, mediana %.6f, max %.6f; strettamente dentro (0, 1): %d; uguale a 0 o 1: %d" % (
            float(al.min()), float(np.median(al)), float(al.max()), int(np.sum((al > 0) & (al < 1))), int(np.sum((al == 0) | (al == 1)))))
        print("    i cambi di segno sugli 11 punti di alpha: %s" % {int(k): int(v) for k, v in zip(*np.unique(T["cambi"][visti], return_counts=True))})
        res = np.abs(T["DH_tot"][rad])
        print("    alla radice, DH col conto PIENO: |DH| max %.3e, mediana %.3e (relativo a |H| %.3e); |conto a mano - pieno| max %.3e; ctrl di famiglie max %.2e" % (
            float(res.max()), float(np.median(res)), float(res.max()) / abs(F0p["tot"]), float(np.max(np.abs(T["DHmano"][rad] - T["DH_tot"][rad]))), float(np.nanmax(T["ctrl"][rad]))))
        print("    DH alla radice per termine (la mediana): " + ", ".join("%s %+.4e" % (k, float(np.median(T["DH_" + k][rad]))) for k in CHIAVI[:-1]))
        print("    LA DISTRIBUZIONE PER ANELLO:")
        for lo in range(10, 24, 2):
            s = (r >= lo) & (r < lo + 2)
            if s.any():
                sr = s & rad
                print("      r %2d-%2d: %4d archi, con la radice %4d; alpha* mediana %s (min %s, max %s); DH(0) mediana %+.4e, DH(1) mediana %+.4e; per termine alla radice: materia %+.3e, vuoto %+.3e, N %+.3e" % (
                    lo, lo + 2, int(s.sum()), int(sr.sum()),
                    "%.4f" % float(np.median(T["alpha"][sr])) if sr.any() else "-", "%.4f" % float(np.min(T["alpha"][sr])) if sr.any() else "-", "%.4f" % float(np.max(T["alpha"][sr])) if sr.any() else "-",
                    float(np.median(T["DH0"][s])), float(np.median(T["DH1"][s])),
                    float(np.median(T["DH_G_psi"][sr] + T["DH_a_psi"][sr])) if sr.any() else float("nan"),
                    float(np.median(T["DH_G_phi"][sr] + T["DH_a_phi"][sr])) if sr.any() else float("nan"),
                    float(np.median(T["DH_N"][sr])) if sr.any() else float("nan")))
    frac = 1.0 - n_rad / len(archi)
    if frac > 0.2:
        print("### ### LA RADICE MANCA SU PIU' DEL 20%% DEGLI ARCHI (%.1f%%): FERMO (il mandato)" % (100 * frac))
    esiti.append(("il mandato: la radice manca su NON piu' del 20%% degli archi (manca sul %.2f%%)" % (100 * frac), frac <= 0.2))
    esiti.append(("P-Z1: la radice esiste su almeno il 95%% degli archi (%.2f%%)" % (100.0 * n_rad / len(archi)), n_rad >= 0.95 * len(archi)))
    esiti.append(("P-Z2: alpha* strettamente dentro (0, 1) sulla maggior parte degli archi", n_rad > 0 and int(np.sum((al > 0) & (al < 1))) > len(archi) / 2.0))
    # ------------------------------------------------------------------ il determinismo
    print("-" * 130)
    D = {}
    for x in ("det_a", "det_b"):
        with np.load(os.path.join(DIR_O, x + ".npz")) as d:
            D[x] = {k: d[k].copy() for k in d.files if k != "tempo"}
    uguali = all(np.array_equal(D["det_a"][k], D["det_b"][k], equal_nan=True) for k in D["det_a"])
    s = D["det_a"]["sel"]
    contro = all(np.array_equal(D["det_a"][c], T[c][s], equal_nan=True) for c in CAMPI)
    print("### IL DETERMINISMO: det_a e det_b (due processi), ogni array AL BIT: %s (lo sha1 %s e %s); contro le parti sugli stessi %d archi: %s" % (
        uguali, sha({c: D["det_a"][c] for c in CAMPI}), sha({c: D["det_b"][c] for c in CAMPI}), len(s), contro))
    esiti.append(("P-Z3, il determinismo: due processi AL BIT (i %d archi e la fila), e uguali alle parti" % N_DET, uguali and contro))
    # ------------------------------------------------------------------ la fila
    print("-" * 130)
    fl, H = D["det_a"]["fila"], D["det_a"]["fila_H"]
    print("### LE %d NASCITE IN FILA alla radice (gli archi in ordine di scatto; il conto pieno dopo ognuna): H prima %.10e" % (len(fl), H[0]))
    for q, x in enumerate(fl):
        print("    %2d: l'arco %6d (%d -> %d): alpha* %.6f; DH alla radice %+.3e; |H(dopo) - H(prima)|/|H| %.3e" % (q + 1, int(x[0]), int(x[1]), int(x[2]), x[3], x[4], x[5]))
    esiti.append(("P-Z4: nelle %d nascite in fila |H(dopo) - H(prima)|/|H| sotto 1e-10 dopo ognuna" % len(fl), len(fl) == N_FILA and bool(np.all(fl[:, 5] < 1e-10))))
    # ------------------------------------------------------------------ lo specchio
    print("-" * 130)
    specchio(G, psi, phi, archi, centro, F0m, F0p, esiti)
    # ------------------------------------------------------------------ il costo
    print("-" * 130)
    t1 = time.time()
    nascita(G, psi, phi, int(archi[0]), F0m, F0p, pieno=False)
    tn = time.time() - t1
    print("### IL COSTO DI UNA NASCITA in questo script (la divisione, FA, %d valutazioni di DH a mano, senza il conto pieno): %.2f s = %.2f tick di C2 (3.690 s, innesco_stima.txt); ### SENZA la CSR e Gauss rifattorizzato: P-Z5 si chiude sul ramo" % (len(GRIGLIA) + PASSI + 1, tn, tn / 3.690))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-118s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("### %.0f s" % (time.time() - t00))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "parte":
        K, NP = int(sys.argv[2]), int(sys.argv[3])
        sys.exit(corri([q for q in range(2929) if q % NP == K], "parte_%d" % K))
    if sys.argv[1] == "det":
        sys.exit(corri(list(range(N_DET)), "det_" + sys.argv[2]))
    sys.exit(referto())
