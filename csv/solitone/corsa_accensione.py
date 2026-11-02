# -*- coding: utf-8 -*-
r"""**L'ACCENSIONE LENTA DEL VUOTO: LE CORSE E IL REFERTO** *(il mandato di Luca delle `01:13` del `2026-11-02`, con le decisioni dopo `25614c34`; il task history
`doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`)*: ### **BG-F-0.15 dalla sua partenza, il vuoto acceso con la rampa `sin^2` su `T_acc`, poi il tick intero;**
### **le misure di `_vuoto_vivo_B` col libro col `par`; `D` rispetto alla partenza e, dopo la rampa, rispetto allo stato a `T_acc`.**

    python csv/solitone/corsa_accensione.py --corsa TA1000     # un pezzo; si ripete finche' dice "finita"
    python csv/solitone/corsa_accensione.py --corsa TA2000
    python csv/solitone/corsa_accensione.py --referto > doc/referti_l2/accensione_lenta.txt
"""
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))

import solitone  # noqa: E402,F401  (i percorsi)

NOME = "BG-F-0.15"             # ### la corsa di _vuoto_vivo_B da cui si parte
CORSE = {"TA1000": (1000.0, 6000.0), "TA2000": (2000.0, 7000.0)}   # ### nome: (T_acc, fine), il mandato; nell'ordine di esecuzione
BLOCCO = 1000.0                # ### i blocchi del confronto (come _respiro_congelato)
META = 0.5                     # ### la vita principale: il cuore liscio a meta' del suo valore a T_acc (Luca)
CODA = 3000.0                  # ### l'estrapolazione dichiarata: la pendenza degli ultimi 3000 (come _respiro_congelato)
DIR_JSON = os.path.join(solitone.RADICE, "doc", "referti_l2", "accensione_lenta")
DIR_NPZ = os.path.join(solitone.RADICE, "db", "accensione_lenta")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def nomi(nome):
    pre = "%s_" % nome
    return sorted(n for n in os.listdir(DIR_JSON) if n.startswith(pre) and n.endswith(".jsonl") and n[len(pre):-6].isdigit()) if os.path.isdir(DIR_JSON) else []


def righe_D(bande, D, n0, t):
    cf = bande.coeff(D)
    pk = np.abs(cf) ** 2
    tot = float(pk.sum())
    return {"t": t, "nD": float(np.linalg.norm(D)) / n0, "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}}


# ------------------------------------------------------------------------------------------------ la corsa
def corsa(nome):
    """### **Un pezzo di `V.PEZZO` tick;** ### **la ripresa al bit** *(ogni chiave di `z["st"]`, e lo stato a `T_acc`)*."""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import misure as MI
    from solitone import protetto as P
    T_acc, tau_fine = CORSE[nome]
    sol, vuoto, s = V.CORSE[NOME]
    K = int(round(T_acc / s))
    t_fine = int(round(tau_fine / s))
    testa_v = V.LP.leggi(os.path.join(V.DIR_JSON, V.nomi(NOME)[0]))
    fatti = nomi(nome)
    testa = V.LP.leggi(os.path.join(DIR_JSON, fatti[0])) if fatti else None
    prec = V.LP.leggi(os.path.join(DIR_JSON, fatti[-1])) if fatti else None
    if prec is not None and (prec["t1"] >= t_fine or prec["t_dis"] is not None):
        print("  la corsa %s: finita (%d pezzi)" % (nome, len(fatti)))
        return 0
    os.makedirs(DIR_JSON, exist_ok=True)
    os.makedirs(DIR_NPZ, exist_ok=True)
    f_rip = os.path.join(DIR_NPZ, nome + ".npz")
    f_acc = os.path.join(DIR_NPZ, nome + "_acc.npz")
    s0 = time.time()
    with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        h = MI.lunghezza_arco(z)
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        p0, info = V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        _ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = MI.Bande(Z, z["L"])
        for k, v in salvato.items():
            z["st"][k][...] = v
        mu = info["mu"]
        assert testa_v["info"]["mu"] == mu and testa_v["w_in"] == w_in, "la scena NON e' quella di BG-F-0.15"
        par = z["par"]
        assert par["eps"] == V.EPS != 0.0, "il libro dei conti deve passare il par della corsa (eps acceso)"
        acc = None
        if prec is None:
            t0 = 0
            z["st"]["psi_h"][...] = p0
        else:
            t0 = prec["t1"]
            assert testa["info"]["mu"] == mu and testa["w_in"] == w_in and testa["e_K"] == e_K, "la scena NON e' quella del primo pezzo"
            with np.load(f_rip) as dati:
                assert int(dati["t"]) == t0
                for k in z["st"]:
                    if isinstance(z["st"][k], np.ndarray):
                        z["st"][k][...] = dati[k]
            assert V.shas(z) == prec["sha_fine"], "lo stato di ripresa NON e' la fine del pezzo prima (al bit, ogni chiave)"
            accs = [r["acc"] for r in (V.LP.leggi(os.path.join(DIR_JSON, n)) for n in fatti) if r.get("acc")]
            if accs:
                acc = dict(accs[0])
                with np.load(f_acc) as dati:
                    acc["psi"] = dati["psi_h"].copy()
                assert SFM.sha(acc["psi"]) == acc["sha"], "lo stato a T_acc NON e' quello registrato"
        vic = z["rr"] <= V.R_VICINO * w_in
        mas = {"vicino": vic, "lontano": ~vic, "totale": np.ones(z["inc"].n, dtype=bool)}
        t1 = min(t0 + V.PEZZO, t_fine)
        camp, dd, da = [], [], []
        t_dis = None
        acc_nuovo = None
        n0 = float(np.linalg.norm(p0))
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            if t0 == 0:
                c = V.misura(z, 0, w_in, w0, h, LC, LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, par), mas)
                c["lam"] = 0.0
                camp.append(c)
            f_lis0 = camp[0]["f_liscia"] if t0 == 0 else testa["campioni"][0]["f_liscia"]
            for t in range(t0 + 1, t1 + 1):
                AC.tick(z, t, K)
                if t == K:
                    mu_a, res_a = AC.mu_rayleigh(z, s)
                    psi_a = z["st"]["psi_h"].copy()
                    acc = {"t": t, "mu": mu_a, "residuo": res_a, "sha": SFM.sha(psi_a), "psi": psi_a}
                    acc_nuovo = acc
                    np.savez(f_acc.replace(".npz", "_tmp.npz"), psi_h=psi_a)
                    os.replace(f_acc.replace(".npz", "_tmp.npz"), f_acc)
                if t % V.OGNI == 0:
                    c = V.misura(z, t, w_in, w0, h, LC, LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, par), mas)
                    c["lam"] = AC.lam_di(t, K)
                    camp.append(c)
                    if c["f_liscia"] < META * f_lis0:
                        t_dis = t
                if t % V.OGNI_D == 0:
                    dd.append(righe_D(bande, np.exp(1j * mu * s * t) * z["st"]["psi_h"] - p0, n0, t))
                    if acc is not None and t > acc["t"]:
                        da.append(righe_D(bande, np.exp(1j * acc["mu"] * s * (t - acc["t"])) * z["st"]["psi_h"] - acc["psi"], float(np.linalg.norm(acc["psi"])), t))
                if t_dis is not None:
                    t1 = t
                    break
        sha_fine = V.shas(z)
        tmp = f_rip.replace(".npz", "_tmp.npz")
        np.savez(tmp, t=t1, **{k: v for k, v in z["st"].items() if isinstance(v, np.ndarray)})
    os.replace(tmp, f_rip)
    riga = {"nome": nome, "da": NOME, "sol": sol, "vuoto": vuoto, "s": s, "eps": V.EPS, "N": V.N, "L": V.L, "T_acc": T_acc, "K": K, "t0": t0, "t1": t1, "t_fine": t_fine,
            "t_dis": t_dis, "w_in": w_in, "h": h, "e_K": e_K, "info": info, "campioni": camp, "D": dd, "D_acc": da, "sha_fine": sha_fine, "secondi": time.time() - s0,
            "acc": {k: v for k, v in acc_nuovo.items() if k != "psi"} if acc_nuovo else None,
            "tick": "accensione (sin^2 su T_acc, poi tick.percorri_tick)", "libro": "col par della corsa", "rampa": "lam_k = sin^2(pi k/(2 K))"}
    V.LP.scrivi_nuovo(os.path.join(DIR_JSON, "%s_%06d.jsonl" % (nome, t0)), riga)
    print("  la corsa %s: il pezzo %d -> %d%s; lam %.4f; f_liscia %.5f (all'inizio %.5f), w %.4f, alone %.5f; %.0f s"
          % (nome, t0, t1, ", SCIOLTO (f_liscia sotto meta')" if t_dis is not None else "", camp[-1]["lam"], camp[-1]["f_liscia"], f_lis0, camp[-1]["w"], camp[-1]["alone"], time.time() - s0))
    return 0


# ------------------------------------------------------------------------------------------------ il referto
def serie(nome):
    rr = [__import__("_vuoto_vivo_B").LP.leggi(os.path.join(DIR_JSON, n)) for n in nomi(nome)]
    for a, b in zip(rr, rr[1:]):
        assert a["t1"] == b["t0"], "un buco fra i pezzi di %s" % nome
    return rr, [c for r in rr for c in r["campioni"]], [d for r in rr for d in r["D"]], [d for r in rr for d in r["D_acc"]]


def pendenza(x, y):
    return float(np.polyfit(x, y, 1)[0]) if len(x) >= 3 else float("nan")


def bande_D(che, dd, s, istanti):
    if not dd:
        return
    td = np.array([d["t"] for d in dd]) * s
    for ist in istanti:
        d = dd[int(np.argmin(np.abs(td - ist)))]
        print("    %-26s a tempo %7.1f: |D|/|psi| %.4e; le bande %s" % (che, d["t"] * s, d["nD"], " ".join("%s %.4f" % (k, v) for k, v in sorted(d["bande"].items()))))


def referto():
    import _respiro_congelato as RC
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import misure as MI
    sol, vuoto, s = V.CORSE[NOME]
    print("=" * 130)
    print("L'ACCENSIONE LENTA DEL VUOTO (Luca 01:13, con le decisioni dopo 25614c34): %s dalla sua partenza, il vuoto acceso con lam = sin^2 su T_acc, poi il tick intero; confrontato con %s vivo"
          % (NOME, NOME))
    print("  la configurazione: CORSE %s BLOCCO %g META %g CODA %g; di _vuoto_vivo_B: PEZZO %d OGNI %d OGNI_D %d R_VICINO %g LAM_ZERO %g TOLL_NORMA %g; s %g eps %g N %.0e L %d; la soglia accessoria %g"
          % (CORSE, BLOCCO, META, CODA, V.PEZZO, V.OGNI, V.OGNI_D, V.R_VICINO, V.LAM_ZERO, V.TOLL_NORMA, s, V.EPS, V.N, V.L, MI.SOGLIA_VITA))
    print("  la vita principale (Luca, la precisazione della decisione 9): il tempo a cui il cuore liscio scende a META' del suo valore a T_acc, misurato o estrapolato (dichiarato); la soglia |D|/|psi| >= %g accessoria" % MI.SOGLIA_VITA)
    print("  ### il libro di BG-F-0.15 vivo e' a eps 0 blocco per blocco (_vuoto_vivo_B.corsa non passa il par): il confronto del libro e' fra conti diversi (Luca: si dichiara)")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (a1) dopo la rampa si assesta e perde piu' lentamente di BG-F; (a2) perde come BG-F: la perdita e' del vuoto vivo; (a3) T_acc 1000 e 2000 diversi: non ancora lenta; (a4) altro")
    print("=" * 130)
    cv, dv = RC.serie_viva()
    print("### %s VIVO (il riferimento: _vuoto_vivo_B + _respiro_sul_fondo)" % NOME)
    tv, flv, wwv, alv = RC.blocchi("VIVO", cv, s)
    res = {}
    for nome, (T_acc, tau_fine) in CORSE.items():
        print("-" * 130)
        rr, camp, dd, da = serie(nome)
        if not rr:
            print("### %s: NESSUN PEZZO" % nome)
            continue
        ult = rr[-1]
        fatta = ult["t1"] >= ult["t_fine"] or ult["t_dis"] is not None
        acc = next((r["acc"] for r in rr if r.get("acc")), None)
        print("### %s (T_acc %g, fino a %g): %s; %d pezzi, %d campioni, %.0f s" % (nome, T_acc, tau_fine, ("SCIOLTO a tempo %.1f" % (ult["t_dis"] * s)) if ult["t_dis"] is not None
                                                                              else ("arriva a %g" % (ult["t1"] * s) if fatta else "### NON FINITA"), len(rr), len(camp), sum(r["secondi"] for r in rr)))
        if acc:
            print("    lo stato a T_acc (tick %d): mu di Rayleigh del tick intero %+.9f (la partenza %+.9f), il residuo per tick %.3e" % (acc["t"], acc["mu"], rr[0]["info"]["mu"], acc["residuo"]))
        tt, fl, ww, al = RC.blocchi(nome, camp, s)
        sciolto_rampa = ult["t_dis"] is not None and ult["t_dis"] <= rr[0]["K"]
        esito("DEVE PASSARE: A6 %s non si scioglie durante la rampa (altrimenti FERMO)" % nome, not sciolto_rampa, "")
        M = np.array([c["E"]["totale"]["M"] for c in camp])
        Vv = np.array([c["E"]["totale"]["V"] for c in camp])
        dM, dV = float(np.max(np.abs(M / M[0] - 1.0))), float(np.max(np.abs(Vv / Vv[0] - 1.0)))
        esito("DEVE PASSARE: A3 %s M e V entro %g" % (nome, V.TOLL_NORMA), dM <= V.TOLL_NORMA and dV <= V.TOLL_NORMA, "dM %.1e dV %.1e" % (dM, dV))
        esito("DEVE PASSARE: A4 %s il libro col par della corsa (eps %g)" % (nome, V.EPS), all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rr), "")
        esito("DEVE PASSARE: %s arriva alla fine o si scioglie" % nome, fatta, "")
        vm = AC.vita_a_meta(tt, fl, T_acc, META, CODA)
        res[nome] = {"vita": vm, "tt": tt, "fl": fl, "al": al, "T_acc": T_acc}
        m = tt >= T_acc
        print("  LA VITA PRINCIPALE: il cuore liscio a T_acc %.5f; sotto %g x: %s; la pendenza del cuore negli ultimi %g %+.4e per 1000"
              % (vm["f0"], META, ("MISURATA a tempo %.1f" % vm["misurata"]) if vm["misurata"] else (("ESTRAPOLATA (non una misura) a tempo ~%.0f" % vm["estrapolata"]) if vm["estrapolata"] else "il cuore non cala: nessuna estrapolazione"), CODA, vm["pendenza"]))
        print("  le pendenze dopo la rampa (%g .. %g), per 1000: il cuore %+.4e, l'alone %+.4e, w %+.4e" % (T_acc, tt[-1], 1000 * pendenza(tt[m], fl[m]), 1000 * pendenza(tt[m], al[m]), 1000 * pendenza(tt[m], ww[m])))
        tdd = np.array([d["t"] for d in dd]) * s
        nd = np.array([d["nD"] for d in dd])
        ram = tdd <= T_acc
        v_r = MI.vita(tdd[ram], nd[ram])
        print("  LA SOGLIA ACCESSORIA (|D|/|psi| >= %g): sulla rampa, D rispetto alla partenza: %s" % (MI.SOGLIA_VITA, ("tempo %.1f" % v_r) if v_r is not None else "mai"))
        if da:
            tda = np.array([d["t"] for d in da]) * s
            nda = np.array([d["nD"] for d in da])
            v_a = MI.vita(tda, nda)
            print("                                         dopo, D rispetto allo stato a T_acc: %s (il primo campione %.4e a tempo %.1f)" % (("tempo %.1f" % v_a) if v_a is not None else "mai", nda[0], tda[0]))
        bande_D("D dalla partenza", dd, s, (0.25 * T_acc, 0.5 * T_acc, T_acc))
        bande_D("D dallo stato a T_acc", da, s, (T_acc + 500.0, T_acc + 2500.0, tau_fine))
    print("-" * 130)
    print("### IL CONFRONTO CON %s VIVO SULLE STESSE FINESTRE (le pendenze per 1000; la vita con lo stesso criterio, dal valore del vivo a T_acc)" % NOME)
    for nome, r in res.items():
        T_acc = r["T_acc"]
        tt = r["tt"]
        mv = (tv >= T_acc) & (tv <= tt[-1])
        vv = AC.vita_a_meta(tv[tv <= tt[-1]], flv[tv <= tt[-1]], T_acc, META, CODA)
        m = tt >= T_acc
        print("  %s, %g .. %g: il cuore %+.4e (VIVO %+.4e); l'alone %+.4e (VIVO %+.4e); la vita a meta': %s (VIVO, dal suo cuore a T_acc %.5f: %s)"
              % (nome, T_acc, tt[-1], 1000 * pendenza(tt[m], r["fl"][m]), 1000 * pendenza(tv[mv], flv[mv]), 1000 * pendenza(tt[m], r["al"][m]), 1000 * pendenza(tv[mv], alv[mv]),
                 ("misurata %.1f" % r["vita"]["misurata"]) if r["vita"]["misurata"] else ("estrapolata ~%.0f" % r["vita"]["estrapolata"]) if r["vita"]["estrapolata"] else "--",
                 vv["f0"], ("misurata %.1f" % vv["misurata"]) if vv["misurata"] else ("estrapolata ~%.0f" % vv["estrapolata"]) if vv["estrapolata"] else "--"))
    vv0 = AC.vita_a_meta(tv, flv, 0.0, META, CODA)
    print("  VIVO dalla partenza (il cuore a 0 %.5f, fino a %g): %s" % (vv0["f0"], tv[-1], ("misurata %.1f" % vv0["misurata"]) if vv0["misurata"] else ("estrapolata ~%.0f" % vv0["estrapolata"]) if vv0["estrapolata"] else "--"))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    for m in ("__init__", "misure", "protetto", "accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    if "--corsa" in argv:
        sys.exit(corsa(argv[argv.index("--corsa") + 1]))
    elif "--referto" in argv:
        referto()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
