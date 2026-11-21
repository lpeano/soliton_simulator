# -*- coding: utf-8 -*-
r"""**P5 DELLA REGOLA INTERA CON CHI** *(il ramo `mitosi-chi`; il mandato unico di Luca `2026-11-21` `19:40`, R2; la carta `doc/TASK_HISTORY/2026-11-21_mitosi_chi.md`, sez. `2.3`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_chi_specchio.py parte K 5        (K = 0 .. 4: gli archi q con q mod 5 = K)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_chi_specchio.py raccogli 5 > doc/referti_l2/mitosi_chi_specchio.txt

**`mitosi_specchio_v2.py` riga per riga** *(importato: `mappe`, `specchiato`, `confronta`, `lato_di`, `_rel`, le soglie)*, **con `chi`:** lo stato e' `stato_03000` della corsa con `chi` del ramo `lapse-u` *(`mitosi_chi.apri`: il campo generico)*; **lo specchio permuta anche `chi` e `pi`** *(per nodo: `w[sig] = v`)*; **la regola e' `mitosi_chi.regola_chi`** *(l'energia di `chi_tick.energia_chi` sul motore del candidato)*; **in piu' lo scarto di `chi` del candidato** *(`chi` del nodo nuovo compreso)*.
**Il caso noto:** `energia_chi` dello stato specchiato *(col SUO Laplaciano)* contro quella dello stato, entro `1e-12` relativo. **Le soglie** di `mitosi_specchio_v2` *(`1e-14`; `E` `1e-10`; `H` `1e-12`)*, `chi` come `psi` *(`1e-14`)*; **IL CASO CHE DEVE FALLIRE:** il flip col VERSO.
**I dati** in `E:/soliton_simulator/controllo/mitosi_chi/specchio/` *(un json per parte)*.
"""
import json
import os
import sys
import time
import types

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "mattone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mitosi_chi as MCH  # noqa: E402
import mitosi_specchio_v2 as MS  # noqa: E402
import chi_tick as CT  # noqa: E402

MR, PS = MCH.MR, MCH.PS
N_SPECCHIO = MS.N_SPECCHIO
SOGLIA, SOGLIA_E, SOGLIA_H, SOGLIA_DEVE_FALLIRE = MS.SOGLIA, MS.SOGLIA_E, MS.SOGLIA_H, MS.SOGLIA_DEVE_FALLIRE
DIR_O = os.path.join(MCH.BASE, "specchio")
F3 = os.path.join(MCH.DIR_M, "stato_03000.npz")


def parte(K_, NP):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_chi.py"))
    _presidio.avvia(os.path.join(_QUI, "mitosi_specchio_v2.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    os.makedirs(DIR_O, exist_ok=True)
    with np.load(os.path.join(MR.DIR_T, "candidati.npz")) as d:
        archi, T = d["archi"].copy(), d["T"].copy()
        centro = d["centro"].copy()
    sel = archi[np.argsort(T, kind="stable")][:N_SPECCHIO]
    mie = [int(a) for q, a in enumerate(sel) if q % NP == K_]
    righe = []
    t00 = time.time()
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        P, m0 = MCH.parametri_di(Z)
        C, NS, meta = MCH.apri(Z, F3, True, P, m0)
        K = NS.K
        sig, ap, rov, hp, p0, scarto = MS.mappe(Z, centro)
        Zs, Cs = MS.specchiato(Z, C, sig, ap, rov, hp)
        Xs = {}
        for q in ("chi", "pi"):
            w = np.empty_like(K.X[q])
            w[sig] = K.X[q]
            Xs[q] = w
        Ks = types.SimpleNamespace(P=P, X=Xs)
        H0 = MCH.energia(Z, C, K)[0]
        Hs = CT.energia_chi(Zs["mot"], Zs["st"], Zs["par"], P, CT.Laplaciano(Zs["mot"]), Xs, Cs.campo)[0]
        noto = abs(H0 - Hs) / abs(H0)
        print("### parte %d di %d: %d archi; lo specchio per %s (scarto %.1e); il caso noto con chi: H %.17e, specchiato %.17e (%.1e)" % (K_, NP, len(mie), p0, scarto, H0, Hs, noto))
        sys.stdout.flush()
        N = int(Z["mot"].inc.n) + 1
        sig2 = np.concatenate([sig, [N - 1]])
        for q, a in enumerate(mie):
            t1 = time.time()
            riga = {"a": a, "rov_a": bool(rov[a])}
            for giro in ("stella", "verso"):
                R1, S1 = MCH.regola_chi(Z, C, a, K, giro)
                R2, S2 = MCH.regola_chi(Zs, Cs, int(ap[a]), Ks, giro)
                l1, l2 = MS.lato_di(R1, sig), MS.lato_di(R2)
                d = MS.confronta(S1, S2, sig, N) if l1 == l2 else None
                if d is not None:
                    d["chi"] = MS._rel(S1["chi"], S2["chi"][sig2])
                gir = None
                if R1["scelto"] >= 0:
                    x, y = R1["lati"][R1["scelto"]]
                    gir = bool(rov[MR.arco_fra(C.campo.ii, C.campo.jj, x, y)])
                riga[giro] = {"stesso_lato": l1 == l2, "lato": l1, "d": d, "gap": R1["gap"], "rov_girato": gir}
                del R1, S1, R2, S2
            righe.append(riga)
            rs, rv = riga["stella"], riga["verso"]
            ds = ", ".join("%s %.1e" % (c, rs["d"][c]) for c in ("psi", "phi", "geo", "A", "E", "H", "chi")) if rs["d"] else "### LATI DIVERSI"
            dv = ("max %.1e" % max(rv["d"].values())) if rv["d"] else "lati diversi"
            print("  [%d/%d] l'arco %d (rov %s): stella lato uguale %s, %s; verso lato uguale %s, %s  (%.0f s)" % (
                q + 1, len(mie), a, riga["rov_a"], rs["stesso_lato"], ds, rv["stesso_lato"], dv, time.time() - t1))
            sys.stdout.flush()
        Z["metti"]()
    with open(os.path.join(DIR_O, "parte_%d_di_%d.json" % (K_, NP)), "w", encoding="utf-8") as f:
        json.dump({"noto": noto, "H0": H0, "Hs": Hs, "p0": list(p0), "righe": righe, "t": time.time() - t00}, f)
    print("### fatto in %.0f s" % (time.time() - t00))
    return 0


def raccogli(NP):
    import _presidio
    _presidio.avvia(__file__)
    P_ = []
    for K_ in range(NP):
        with open(os.path.join(DIR_O, "parte_%d_di_%d.json" % (K_, NP)), encoding="utf-8") as f:
            P_.append(json.load(f))
    righe = [r for p in P_ for r in p["righe"]]
    esiti = []
    print("=" * 130)
    print("P5 DELLA REGOLA INTERA CON CHI (Luca 2026-11-21 19:40, R2; la carta del ramo mitosi-chi sez. 2.3): %d archi in %d parti, dallo stato k 3000 della corsa con chi" % (len(righe), NP))
    print("=" * 130)
    noto = max(p["noto"] for p in P_)
    print("### il caso noto: l'energia con chi dello stato specchiato contro quella dello stato, il massimo sulle parti %.2e (H %.17e)" % (noto, P_[0]["H0"]))
    esiti.append(("il caso noto: H con chi dello stato specchiato = H entro 1e-12 relativo", noto <= SOGLIA_H))
    for giro in ("stella", "verso"):
        X = [r[giro] for r in righe]
        uguali = sum(x["stesso_lato"] for x in X)
        Xd = [x for x in X if x["d"]]
        cc = ("psi", "phi", "geo", "A", "E", "H", "chi")
        mx = {c: (max(x["d"][c] for x in Xd) if Xd else float("nan")) for c in cc}
        print("### %s: lo stesso lato su %d archi su %d; gli scarti massimi %s" % (giro.upper(), uguali, len(X), ", ".join("%s %.1e" % (c, v) for c, v in mx.items())))
        for nome, chiave in (("l'arco diviso", "rov_a"), ("l'arco girato", "rov_girato")):
            for cl in (False, True):
                sel = [r[giro] for r in righe if (r[chiave] if chiave == "rov_a" else r[giro]["rov_girato"]) is cl]
                sd = [x for x in sel if x["d"]]
                if sel:
                    print("    %s %s: %d archi, lo stesso lato %d, %s (sui %d con lo stesso lato)" % (
                        nome, "ROVESCIATO" if cl else "conservato", len(sel), sum(x["stesso_lato"] for x in sel),
                        " ".join("%s %.1e" % (c, (max(x["d"][c] for x in sd) if sd else float("nan"))) for c in cc), len(sd)))
        if giro == "stella":
            ok = uguali == len(X) and all(mx[c] <= SOGLIA for c in ("psi", "phi", "geo", "A", "chi")) and mx["E"] <= SOGLIA_E and mx["H"] <= SOGLIA_H
            esiti.append(("P5: la regola intera con chi simmetrica (lo stesso lato; psi, phi, versori, A, chi entro 1e-14; E entro 1e-10; H entro 1e-12)", ok))
        else:
            cade = uguali < len(X) or (bool(Xd) and max(max(x["d"].values()) for x in Xd) > SOGLIA_DEVE_FALLIRE)
            esiti.append(("DEVE FALLIRE: la regola col flip col VERSO (un lato diverso o uno scarto sopra 1e-6)", cade))
    gaps = np.array([r["stella"]["gap"] for r in righe])
    print("### lo scarto fra il migliore e il secondo (stella): la mediana %.2e |H|, il minimo %.2e" % (float(np.median(gaps)), float(gaps.min())))
    print("### il tempo delle parti: %s s" % ["%.0f" % p["t"] for p in P_])
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
