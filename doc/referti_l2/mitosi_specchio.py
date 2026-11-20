# -*- coding: utf-8 -*-
r"""**P5 DELLA REGOLA INTERA NELLA CORSA, CON L'ENERGIA DELLA CORSA** *(il ramo `mitosi`; Luca `2026-11-20` `16:37` D-H-CORSA, `17:08` D-VERSORE; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `10.3` e `11`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_specchio.py parte K 5        (K = 0 .. 4: gli archi q con q mod 5 = K)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_specchio.py raccogli 5 > doc/referti_l2/mitosi_specchio.txt

**Lo stato:** C2 a `k 3000` col campo generico *(`mitosi_corsa.campo_generico`)*. **Lo specchio:** a `30` gradi per il nodo piu' vicino al centro di C2 *(`mattone/specchio_carta.mappa_nodi`, `mappa_archi`: come `covariante_e_famiglia.mappa_specchio` del ramo `primo-ordine`)*.
**L'azione sullo stato e' la PERMUTAZIONE** *(la carta sez. `10.3`, dichiarata)*: le estremita' *(`psi`, `phi`, i versori: NON riflessi)*, i nodi *(`rho`, `Lambda`, `h_int`)*, gli archi *(`A`, `E` col segno del verso)*; **il grafo e i vettori d'arco del campo sono quelli del toro** *(lo specchio e' una simmetria del grafo)*.
**Il caso noto:** l'energia della corsa dello stato specchiato contro quella dello stato, entro `1e-12` relativo.
**Per ognuno dei primi `200` archi nell'ordine di scatto** *(`candidati.npz`, il tempo `T`)*: **la regola intera** *(`mitosi_regola.regola`)* **sull'arco e sull'arco immagine nello stato specchiato:** lo stesso lato *(per nodi)*; `psi`, `phi`, i versori, `A` entro `1e-14` *(il massimo dello scarto sul massimo del valore)*; **`E` entro `1e-10`**; `H` entro `1e-12` relativo. **Le classi:** il verso dell'arco diviso e quello dell'arco GIRATO, conservato o rovesciato dallo specchio. **IL CASO CHE DEVE FALLIRE:** la regola col flip col VERSO *(`giro = "verso"`)*: **deve dare scarti sopra `1e-6` o un lato diverso su qualche arco.**
**I dati** in `E:/soliton_simulator/controllo/regola_corsa/` *(un json per parte; non nel repo: il dato e' il comando)*.
"""
import copy
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "mattone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mitosi_regola as MR  # noqa: E402

MC, PS = MR.MC, MR.PS
N_SPECCHIO = 200
SOGLIA, SOGLIA_E, SOGLIA_H, SOGLIA_DEVE_FALLIRE = 1e-14, 1e-10, 1e-12, 1e-6
DIR_O = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "regola_corsa")


def mappe(Z, centro):
    import specchio_carta as SC
    from solitone import toro as TO
    mot = Z["mot"]
    ii, jj = np.asarray(mot.inc.nodo[0::2], dtype=np.int64), np.asarray(mot.inc.nodo[1::2], dtype=np.int64)
    L, nn = int(Z["L"]), int(mot.inc.n)
    v = np.arange(nn)
    A1, A2 = TO.vettori()
    d30 = 2 * A1 + A2
    p0 = (int(round(float(centro[0]))), int(round(float(centro[1]))))
    sig, scarto, _M = SC.mappa_nodi(L, (v // L).astype(float), (v % L).astype(float), p0, math.atan2(d30[1], d30[0]))
    assert scarto < 1e-9 and np.array_equal(sig[sig], v), "lo specchio non e' una involuzione dei nodi"
    ap, rov = SC.mappa_archi(ii, jj, sig)
    hp = np.empty(2 * len(ap), dtype=np.int64)
    hp[0::2] = np.where(rov, 2 * ap + 1, 2 * ap)
    hp[1::2] = np.where(rov, 2 * ap, 2 * ap + 1)
    assert np.array_equal(MR.nodo_h(ii, jj)[hp], sig[MR.nodo_h(ii, jj)]), "la mappa delle estremita' non segue quella dei nodi"
    return sig, ap, rov, hp, p0, scarto


class _C(object):
    def __init__(self, campo, legge):
        self.campo, self.legge = campo, legge


def specchiato(Z, C, sig, ap, rov, hp):
    """### Lo stato specchiato (la permutazione): `(Zs, Cs)` per `mitosi_regola.candidato`."""
    import incidenza as IN
    import motore as MO
    mot, st = Z["mot"], Z["st"]
    ss = {}
    for k, v in st.items():
        if not isinstance(v, np.ndarray):
            ss[k] = v
            continue
        w = np.empty_like(v)
        if v.shape[0] == 2 * mot.inc.m:
            w[hp] = v
        else:
            assert v.shape[0] == mot.inc.n
            w[sig] = v
        ss[k] = w
    g = copy.deepcopy(C.campo)
    sgn = np.where(rov, -1.0, 1.0)
    g.A = np.empty_like(C.campo.A)
    g.E = np.empty_like(C.campo.E)
    g.A[ap] = sgn * C.campo.A
    g.E[ap] = sgn * C.campo.E
    geo = np.empty_like(mot.geo.n)
    geo[hp] = mot.geo.n
    U = np.zeros((mot.inc.m, 2, 2), dtype=complex)
    u = g.u()
    U[:, 0, 0] = u
    U[:, 1, 1] = u
    ii, jj = np.asarray(mot.inc.nodo[0::2]), np.asarray(mot.inc.nodo[1::2])
    inc = IN.Incidenza(ii.astype(IN.INDICE), jj.astype(IN.INDICE), mot.inc.n, capacita=len(ii))
    ms = MO.Motore(inc, MO.Geometria(geo, U), ss, np.asarray(mot.dtau, dtype=float).copy(), mot.sommatoria)
    return {"mot": ms, "st": ss, "e_K": Z["e_K"], "par": Z["par"]}, _C(g, C.legge)


def energia_di(Zx, Cx):
    import _libro_dei_conti as LB
    import _vuoto_vivo_B as V
    m = Zx["mot"]
    return float(np.sum(LB.conti_per_nodo(m.inc, m, Zx["st"], Zx["e_K"], V.LAM_ZERO, Zx["par"])["tot"])) + Cx.campo.K() + Cx.campo.V()


def _rel(a, b):
    s = float(np.max(np.abs(a)))
    return float(np.max(np.abs(a - b))) / s if s > 0 else float(np.max(np.abs(b)))


def confronta(S1, S2, sig, N):
    """### `S1` (sullo stato) mandato dallo specchio contro `S2` (sullo stato specchiato)."""
    sig2 = np.concatenate([sig, [N - 1]])
    i1, j1 = sig2[S1["ii"]], sig2[S1["jj"]]
    i2, j2 = S2["ii"], S2["jj"]
    kA = np.empty(2 * len(i1), dtype=np.int64)
    kA[0::2], kA[1::2] = i1 * N + j1, j1 * N + i1
    kB = np.empty(2 * len(i2), dtype=np.int64)
    kB[0::2], kB[1::2] = i2 * N + j2, j2 * N + i2
    o = np.argsort(kB, kind="stable")
    pos = np.minimum(np.searchsorted(kB[o], kA), len(o) - 1)
    hB = o[pos]
    assert np.array_equal(kB[hB], kA), "i due grafi nati non sono lo specchio l'uno dell'altro"
    aB = hB[0::2] // 2
    sgn = np.where(hB[0::2] % 2 == 0, 1.0, -1.0)                     # ### l'estremita' in ii1 cade in jj2: il verso rovesciato
    g1, g2 = S1["campo"], S2["campo"]
    out = {"psi": _rel(S1["psi"], S2["psi"][hB]), "phi": _rel(S1["phi"], S2["phi"][hB]), "geo": _rel(S1["geo"], S2["geo"][hB]),
           "A": _rel(g1.A, sgn * g2.A[aB]), "E": _rel(g1.E, sgn * g2.E[aB]), "H": abs(S1["H"] - S2["H"]) / abs(S1["H"])}
    return out


def lato_di(R, sig=None):
    if R["scelto"] < 0:
        return None
    x, y = R["lati"][R["scelto"]]
    if sig is not None:
        x, y = int(sig[x]), int(sig[y])
    return tuple(sorted((int(x), int(y))))


def parte(K, NP):
    import _presidio
    MT, CV = PS.MT, PS.CV
    _presidio.avvia(os.path.join(_QUI, "mitosi_regola.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    os.makedirs(DIR_O, exist_ok=True)
    with np.load(os.path.join(MR.DIR_T, "candidati.npz")) as d:
        archi, T = d["archi"].copy(), d["T"].copy()
        centro = d["centro"].copy()
    sel = archi[np.argsort(T, kind="stable")][:N_SPECCHIO]
    mie = [int(a) for q, a in enumerate(sel) if q % NP == K]
    righe = []
    t00 = time.time()
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, meta, cs, s = MC.CSB.riprendi(Z, MC.F_C2, False, rho_c, e)
        PS.PO.accendi(cs)
        try:
            MC.campo_generico(Z, C)
            sig, ap, rov, hp, p0, scarto = mappe(Z, centro)
            Zs, Cs = specchiato(Z, C, sig, ap, rov, hp)
            H0, Hs = MR.energia_corsa(Z, C), energia_di(Zs, Cs)
            noto = abs(H0 - Hs) / abs(H0)
            print("### parte %d di %d: %d archi; lo specchio per %s (scarto %.1e); il caso noto: H %.17e, specchiato %.17e (%.1e)" % (K, NP, len(mie), p0, scarto, H0, Hs, noto))
            sys.stdout.flush()
            N = int(Z["mot"].inc.n) + 1
            for q, a in enumerate(mie):
                t1 = time.time()
                riga = {"a": a, "rov_a": bool(rov[a])}
                for giro in ("stella", "verso"):
                    R1, S1 = MR.regola(Z, C, a, giro)
                    R2, S2 = MR.regola(Zs, Cs, int(ap[a]), giro)
                    l1, l2 = lato_di(R1, sig), lato_di(R2)
                    d = confronta(S1, S2, sig, N)
                    gir = None
                    if R1["scelto"] >= 0:
                        x, y = R1["lati"][R1["scelto"]]
                        ii, jj = C.campo.ii, C.campo.jj
                        gir = bool(rov[MR.arco_fra(ii, jj, x, y)])
                    riga[giro] = {"stesso_lato": l1 == l2, "lato": l1, "d": d, "gap": R1["gap"], "rov_girato": gir}
                    del R1, S1, R2, S2
                righe.append(riga)
                rs = riga["stella"]
                print("  [%d/%d] l'arco %d (rov %s): stella lato uguale %s, psi %.1e phi %.1e geo %.1e A %.1e E %.1e H %.1e; verso lato uguale %s, max %.1e  (%.0f s)" % (
                    q + 1, len(mie), a, riga["rov_a"], rs["stesso_lato"], rs["d"]["psi"], rs["d"]["phi"], rs["d"]["geo"], rs["d"]["A"], rs["d"]["E"], rs["d"]["H"],
                    riga["verso"]["stesso_lato"], max(riga["verso"]["d"].values()), time.time() - t1))
                sys.stdout.flush()
        finally:
            PS.LC.spegni()
    with open(os.path.join(DIR_O, "parte_%d_di_%d.json" % (K, NP)), "w", encoding="utf-8") as f:
        json.dump({"noto": noto, "H0": H0, "Hs": Hs, "p0": list(p0), "righe": righe, "t": time.time() - t00}, f)
    print("### fatto in %.0f s" % (time.time() - t00))
    return 0


def raccogli(NP):
    import _presidio
    _presidio.avvia(__file__)
    P = []
    for K in range(NP):
        with open(os.path.join(DIR_O, "parte_%d_di_%d.json" % (K, NP)), encoding="utf-8") as f:
            P.append(json.load(f))
    righe = [r for p in P for r in p["righe"]]
    esiti = []
    print("=" * 130)
    print("P5 DELLA REGOLA INTERA NELLA CORSA, CON L'ENERGIA DELLA CORSA (Luca 2026-11-20 16:37, 17:08; la carta sez. 10.3, 11): %d archi in %d parti" % (len(righe), NP))
    print("=" * 130)
    noto = max(p["noto"] for p in P)
    print("### il caso noto: l'energia dello stato specchiato contro quella dello stato, il massimo sulle parti %.2e (H %.17e)" % (noto, P[0]["H0"]))
    esiti.append(("il caso noto: H dello stato specchiato = H entro 1e-12 relativo", noto <= SOGLIA_H))
    for giro in ("stella", "verso"):
        X = [r[giro] for r in righe]
        uguali = sum(x["stesso_lato"] for x in X)
        mx = {c: max(x["d"][c] for x in X) for c in ("psi", "phi", "geo", "A", "E", "H")}
        print("### %s: lo stesso lato su %d archi su %d; gli scarti massimi %s" % (giro.upper(), uguali, len(X), ", ".join("%s %.1e" % (c, v) for c, v in mx.items())))
        for nome, chiave in (("l'arco diviso", "rov_a"), ("l'arco girato", "rov_girato")):
            for cl in (False, True):
                sel = [r[giro] for r in righe if (r[chiave] if chiave == "rov_a" else r[giro]["rov_girato"]) is cl]
                if sel:
                    print("    %s %s: %d archi, lo stesso lato %d, psi %.1e phi %.1e geo %.1e A %.1e E %.1e H %.1e" % (
                        nome, "ROVESCIATO" if cl else "conservato", len(sel), sum(x["stesso_lato"] for x in sel),
                        *(max(x["d"][c] for x in sel) for c in ("psi", "phi", "geo", "A", "E", "H"))))
        if giro == "stella":
            ok = uguali == len(X) and all(mx[c] <= SOGLIA for c in ("psi", "phi", "geo", "A")) and mx["E"] <= SOGLIA_E and mx["H"] <= SOGLIA_H
            esiti.append(("P5: la regola intera simmetrica (lo stesso lato; psi, phi, versori, A entro 1e-14; E entro 1e-10; H entro 1e-12)", ok))
        else:
            cade = uguali < len(X) or max(max(x["d"].values()) for x in X) > SOGLIA_DEVE_FALLIRE
            esiti.append(("DEVE FALLIRE: la regola col flip col VERSO (un lato diverso o uno scarto sopra 1e-6)", cade))
    gaps = np.array([r["stella"]["gap"] for r in righe])
    print("### lo scarto fra il migliore e il secondo (stella): la mediana %.2e |H|, il minimo %.2e" % (float(np.median(gaps)), float(gaps.min())))
    print("### il tempo delle parti: %s s" % ["%.0f" % p["t"] for p in P])
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-112s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("parte")
    p.add_argument("K", type=int)
    p.add_argument("NP", type=int)
    r = sub.add_parser("raccogli")
    r.add_argument("NP", type=int)
    x = ap.parse_args(argv)
    if x.cmd == "parte":
        return parte(x.K, x.NP)
    return raccogli(x.NP)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
