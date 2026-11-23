# -*- coding: utf-8 -*-
r"""**[M1751-L] S2-S4, S7: LA SCHEDA SPETTRALE DEI MODI NUOVI** *(Luca, 2026-11-23; la carta `doc/CARTA_gradi_di_liberta.md`, sez. `4`: il metodo scritto prima)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe C:/Users/lpeano/wt_mitosi/doc/referti_l2/nascite/gradi_liberta.py scheda --nascita 269        (dopo la ripresa: prima_/dopo_ in M1751/ripresa_<q>; o --nascite 1,2,3 in sequenza, le fatte si saltano)
    E:\python\py3132\python.exe doc/referti_l2/nascite/gradi_liberta.py lettura > doc/referti_l2/nascite/gradi_liberta.txt

**Lo stato** PRIMA e DOPO *(`mitosi_rami_v2.apri` nella scena `L 186` di `ciclo`)*. **Il cammino:** `percorri_tick` dentro `_u1_oggi.avvolto` coi soli `CAMM-MONETA-SPIN`, `CAMM-GROVER`, `CAMM-SPOSTAMENTO` *(saltati il legame, la fase del vuoto, i pezzi del vuoto; fuori anche la fase (a) e la reazione del lapse di `p6_bracci.tick_GU`)*, `mot.cs` = `cs_prec` dello stato. **Il disco:** i nodi entro `12` passi da `{i, j}`; **il muro:** solo il disco. **La sonda:** gruppi a distanza `>= 7`, un tick per gruppo e posto; le risposte nelle palle di raggio `3`; **il residuo fuori DEVE essere zero.** **I modi:** `eig`; **i nuovi:** (1) il conto per finestra di energia *(DOPO meno PRIMA: non abbina niente)*; (2) l'abbinamento ungherese su `|<v_p|v_d>|^2` sulle etichette `(nodo, altro capo, spin)` comuni. **La scheda, S4** come la carta.
"""
import argparse
import contextlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_SU = os.path.dirname(_QUI)
for _p in (_QUI, _SU):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import nascite_lettura as NL  # noqa: E402
import mitosi_rami_v2 as MR2V  # noqa: E402
import ripresa_nascita as RN  # noqa: E402

PS = MR2V.PS
R_DISCO, SEP, R_PALLA = 12, 7, 3
SALTA = ("CAMM-MATERIA-VUOTO", "CAMM-FASE-VUOTO", "CAMM-GROVER-VUOTO", "CAMM-SPOSTAMENTO-VUOTO")
FINESTRE = (("la piatta", -0.4900, -0.4800), ("sotto la piatta", -math.pi, -0.4900), ("fra piatta e striscia", -0.4800, 0.0100),
            ("la striscia", 0.0100, 0.0130), ("il gap sotto la coppia", 0.0130, 0.2440), ("la coppia", 0.2440, 0.4780), ("sopra la coppia", 0.4780, math.pi))
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


@contextlib.contextmanager
def aperto(f):
    MT, CV = PS.MT, PS.CV
    rho_c, e = MT.rho_c_assoluto(), MT.PB.E_DECISO
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, NS, meta, cs = MR2V.apri(Z, f, rho_c, e, True)
        yield Z, C, NS, meta, cs


def cammino(Z, C, cs, psi):
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    mot, st, par = Z["mot"], Z["st"], Z["par"]
    st["psi_h"][...] = psi
    mot.cs = np.asarray(cs, dtype=float).copy()
    mot.lambda_c = None
    with UO.avvolto(mot, C.campo, True):
        TK.percorri_tick(st, mot, par, SALTA, None, len(CM.ORDINE))
    return st["psi_h"].copy()


def matrice(Z, C, cs, centro):
    """### `(M, etichette, righe, residuo, n_tick)`: la matrice del cammino sul disco, col muro."""
    from scipy.sparse import csgraph
    mot = Z["mot"]
    nodo = np.asarray(mot.inc.nodo)
    n = mot.inc.n
    X = {"ii": nodo[0::2].astype(np.int64), "jj": nodo[1::2].astype(np.int64), "n": n}
    A = NL.adiacenza(X)
    dc = csgraph.dijkstra(A, unweighted=True, indices=list(centro), limit=R_DISCO + 0.5, min_only=True)
    D = np.nonzero(np.isfinite(dc))[0]
    inD = np.zeros(n, dtype=bool)
    inD[D] = True
    righe = np.nonzero(inD[nodo])[0]
    pos = -np.ones(len(nodo), dtype=np.int64)
    pos[righe] = np.arange(len(righe))
    Nd = 2 * len(righe)
    per_nodo = {int(v): [] for v in D}
    for h in righe:
        per_nodo[int(nodo[h])].append(int(h))
    dd = csgraph.dijkstra(A, unweighted=True, indices=D, limit=SEP + 0.5)
    dDD = dd[:, D]
    colori = []
    for a_, v in enumerate(D):
        for col in colori:
            if np.all(dDD[a_, col] >= SEP):
                col.append(a_)
                break
        else:
            colori.append([a_])
    palla = {int(D[a_]): np.nonzero(dd[a_] <= R_PALLA)[0] for a_ in range(len(D))}
    M = np.zeros((Nd, Nd), dtype=complex)
    psi0 = np.zeros_like(Z["st"]["psi_h"])
    resid = 0.0
    nt = 0
    smax = 2 * max(len(per_nodo[int(v)]) for v in D)
    for col in colori:
        for s in range(smax):
            chi = [int(D[a_]) for a_ in col if s < 2 * len(per_nodo[int(D[a_])])]
            if not chi:
                continue
            p = psi0.copy()
            for v in chi:
                p[per_nodo[v][s // 2], s % 2] = 1.0
            out = cammino(Z, C, cs, p)
            nt += 1
            dentro = np.zeros(len(nodo), dtype=bool)
            for v in chi:
                hv = np.nonzero(np.isin(nodo, palla[v]))[0]
                dentro[hv] = True
                hd = hv[inD[nodo[hv]]]
                j = 2 * pos[per_nodo[v][s // 2]] + s % 2
                M[2 * pos[hd], j] = out[hd, 0]
                M[2 * pos[hd] + 1, j] = out[hd, 1]
            resid = max(resid, float(np.max(np.abs(out[~dentro]))) if (~dentro).any() else 0.0)
    et = [(int(nodo[h]), int(nodo[h ^ 1]), sp) for h in righe for sp in (0, 1)]
    return M, et, righe, resid, nt, len(colori), D


def scheda(q):
    import _presidio
    _presidio.avvia(os.path.join(_SU, "mitosi_rami_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "ripresa_nascita.py"))
    _presidio.avvia(__file__)
    B = NL.nascite()
    b = B[q - 1]
    k = int(b["k"])
    d = os.path.join(RN.DIR, "ripresa_%03d" % q)
    fp, fd = os.path.join(d, "prima_%05d.npz" % k), os.path.join(d, "dopo_%05d.npz" % k)
    i, j, n = b["nodi"]["i"], b["nodi"]["j"], b["nodi"]["n"]
    print("=" * 130)
    print("[M1751-L] LA SCHEDA della nascita %d (k %d, l'arco %d, i %d, j %d, il nato %d): il disco di raggio %d attorno a {i, j}" % (q, k, b["a"], i, j, n, R_DISCO))
    out = {"nascita": q, "k": k}
    R = {}
    for nome, f in (("prima", fp), ("dopo", fd)):
        t1 = time.time()
        with aperto(f) as (Z, C, NS, meta, cs):
            psi_stato = Z["st"]["psi_h"].copy()
            M, et, righe, resid, nt, ncol, D = matrice(Z, C, cs, (i, j))
            nodo = np.asarray(Z["mot"].inc.nodo)
            vic_n = set(np.asarray(Z["mot"].inc.nodo)[np.nonzero(np.asarray(Z["mot"].inc.nodo) == n)[0] ^ 1].tolist()) if nome == "dopo" else set()
            Z["metti"]()
        w, V = np.linalg.eig(M)
        V = V / np.linalg.norm(V, axis=0)
        R[nome] = {"M": M, "et": et, "w": w, "V": V, "righe": righe, "psi": np.concatenate([psi_stato[righe, 0:1], psi_stato[righe, 1:2]], axis=1).reshape(-1), "nodo_h": nodo[righe], "D": D, "vic_n": vic_n}
        print("  %s: %d nodi nel disco, %d componenti; %d gruppi, %d tick del cammino; il residuo fuori dalle palle %.3e; |lambda| da %.6f a %.6f (%.0f s)" % (
            nome, len(D), M.shape[0], ncol, nt, resid, float(np.abs(w).min()), float(np.abs(w).max()), time.time() - t1))
        esito("%s: la sonda e' locale (il residuo fuori dalle palle di raggio %d = 0)" % (nome, R_PALLA), resid == 0.0, "%.3e" % resid)
        out["%s_dim" % nome] = int(M.shape[0])
    p, dpo = R["prima"], R["dopo"]
    dd = out["dopo_dim"] - out["prima_dim"]
    print("  la dimensione del disco: %d -> %d (%+d; atteso +12 dalle righe: +3 archi x 4)" % (out["prima_dim"], out["dopo_dim"], dd))
    esito("K2 la dimensione cresce di 12", dd == 12, "%+d" % dd)
    Ep, Ed = -np.angle(p["w"]), -np.angle(dpo["w"])
    print("  (1) IL CONTO PER FINESTRA (DOPO meno PRIMA; non abbina niente):")
    cont = {}
    for nm, lo, hi in FINESTRE:
        a_ = int(np.sum((Ep >= lo) & (Ep < hi)))
        b_ = int(np.sum((Ed >= lo) & (Ed < hi)))
        cont[nm] = b_ - a_
        print("    %-24s %5d -> %5d (%+d)" % (nm, a_, b_, b_ - a_))
    out["finestre"] = cont
    from scipy.optimize import linear_sum_assignment
    ip = {e: x for x, e in enumerate(p["et"])}
    com = [(ip[e], y) for y, e in enumerate(dpo["et"]) if e in ip]
    cp, cd = np.array([c[0] for c in com]), np.array([c[1] for c in com])
    O = np.abs(p["V"][cp].conj().T @ dpo["V"][cd]) ** 2
    t1 = time.time()
    r_, c_ = linear_sum_assignment(-O)
    nuovi = np.setdiff1d(np.arange(dpo["V"].shape[1]), c_)
    print("  (2) L'ABBINAMENTO UNGHERESE (%d etichette comuni; %.0f s): la sovrapposizione abbinata la mediana %.4f, il 10%% %.4f; i modi DOPO non abbinati %d" % (
        len(com), time.time() - t1, float(np.median(O[r_, c_])), float(np.percentile(O[r_, c_], 10)), len(nuovi)))
    nodo_h = dpo["nodo_h"]
    nn = len(nodo_h)
    cfs, *_ = np.linalg.lstsq(dpo["V"], dpo["psi"], rcond=None)
    pesi = np.abs(cfs) ** 2
    schede = []
    for m in nuovi:
        v = dpo["V"][:, m]
        a2 = np.abs(v.reshape(nn, 2)) ** 2
        pn = {}
        for h_, x in enumerate(nodo_h):
            pn[int(x)] = pn.get(int(x), 0.0) + float(a2[h_].sum())
        wv = np.array(list(pn.values()))
        PR = float(wv.sum() ** 2 / np.sum(wv ** 2))
        sul_nato = pn.get(int(n), 0.0)
        sui_vicini = sum(pn.get(int(x), 0.0) for x in dpo["vic_n"])
        sz = float(np.sum(a2[:, 0] - a2[:, 1]))
        E_ = float(Ed[m])
        dove = [nm for nm, lo, hi in FINESTRE if lo <= E_ < hi][0]
        schede.append({"E": E_, "abs": float(abs(dpo["w"][m])), "dove": dove, "PR": PR, "nato": sul_nato, "vicini": sui_vicini, "sz": sz, "peso_stato": float(pesi[m])})
    for s_ in sorted(schede, key=lambda x: x["E"]):
        print("    il modo nuovo: E %+.6f (%s), |lambda| %.6f, PR %.1f nodi, sul nato %.4f, sui vicini del nato %.4f, <sigma_z> %+.4f" % (s_["E"], s_["dove"], s_["abs"], s_["PR"], s_["nato"], s_["vicini"], s_["sz"]))
    loc = float(np.mean([s_["PR"] < 20 for s_ in schede])) if schede else float("nan")
    print("  K2: localizzati (PR < 20) %.4f" % loc)
    tot = float(np.sum(pesi))
    fr_n = float(np.sum(pesi[nuovi])) / tot if tot > 0 else float("nan")
    fr_e = float(np.sum(pesi[nuovi] * np.abs(Ed[nuovi]))) / float(np.sum(pesi * np.abs(Ed))) if tot > 0 else float("nan")
    print("  S4: lo stato DOPO nel disco sui modi nuovi: la frazione di norma %.6f, di energia (|E| pesata) %.6f; DH della nascita %+.4f" % (fr_n, fr_e, b["DH"]))
    out.update(nuovi=len(nuovi), schede=schede, localizzati=loc, frazione_norma=fr_n, frazione_energia=fr_e, DH=b["DH"], DEVE={k_: v for k_, v in OK.items()})
    fj = os.path.join(d, "scheda.json")
    with open(fj, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("### la scheda in %s" % fj)
    fall = [k_ for k_, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0 if not fall else 1


def lettura():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1751-L] S2-S4, S7: LE SCHEDE DELLE DIECI NASCITE (la carta sez. 4)")
    print("=" * 130)
    tutte = []
    for q in RN.CAMPIONE:
        fj = os.path.join(RN.DIR, "ripresa_%03d" % q, "scheda.json")
        if not os.path.exists(fj):
            print("  la nascita %d: NON FATTA" % q)
            continue
        S = json.load(open(fj, encoding="utf-8"))
        print("  la nascita %3d (k %d): la dimensione %d -> %d; i nuovi %d; per finestra %s; localizzati %.3f; S4 norma %.4f, energia %.4f, DH %+.3f" % (
            q, S["k"], S["prima_dim"], S["dopo_dim"], S["nuovi"], {x: v for x, v in S["finestre"].items() if v}, S["localizzati"], S["frazione_norma"], S["frazione_energia"], S["DH"]))
        tutte += S["schede"]
    if tutte:
        def classe(s_):
            pr = "PR<5" if s_["PR"] < 5 else ("PR 5-20" if s_["PR"] < 20 else "PR>20")
            return (s_["dove"], pr, "+" if s_["sz"] > 0 else "-")
        from collections import Counter
        cc = Counter(classe(s_) for s_ in tutte)
        tot = sum(cc.values())
        top = sum(v for _c, v in cc.most_common(6))
        print("### S7: %d modi nuovi in %d classi; le 6 piu' frequenti coprono %.4f: %s" % (tot, len(cc), top / tot, cc.most_common(8)))
        print("### K6: %s" % ("SPECIE" if top / tot > 0.8 else "RUMORE (o in mezzo)"))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("scheda", "lettura"))
    ap.add_argument("--nascita", type=int)
    ap.add_argument("--nascite", help="piu' nascite in sequenza, separate da virgole; una scheda gia' fatta (scheda.json) si salta: la ripresa dopo un riavvio")
    a = ap.parse_args(argv)
    if a.cosa == "scheda":
        qs = [int(x) for x in a.nascite.split(",")] if a.nascite else [a.nascita]
        cod = 0
        for q in qs:
            if os.path.exists(os.path.join(RN.DIR, "ripresa_%03d" % q, "scheda.json")):
                print("### la scheda della nascita %d c'e' gia': si salta" % q)
                continue
            OK.clear()
            cod = max(cod, scheda(q))
            sys.stdout.flush()
        return cod
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
