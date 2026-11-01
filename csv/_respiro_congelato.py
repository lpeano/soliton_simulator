# -*- coding: utf-8 -*-
r"""**IL CONTROLLO A VUOTO CONGELATO DEL RESPIRO SUL FONDO** *(il mandato di Luca del `2026-11-01` dopo `1ee60e19`; NESSUNA MODIFICA AL NUCLEO; [[VUOTO-SUL-FONDO]],
[[LIBRO-DEI-CONTI]]; il task history `doc/TASK_HISTORY/2026-11-01_respiro_congelato.md`)*: ### **BG-F-0.15 di `_vuoto_vivo_B` con lo stesso stato iniziale e il vuoto `F0`
CONGELATO** *(`_congelato_lungo.avanza`)* ### **fino a `10000` unita' di tempo**, confrontato con la corsa viva; ### **e la ripartizione dell'energia di `326747d0` col
termine della moneta**, dagli stati iniziale e finale delle `6` corse.

    python csv/_respiro_congelato.py --ripartizione > doc/referti_l2/ripartizione_vuoto_vivo.txt
    python csv/_respiro_congelato.py --corsa          # un pezzo; si ripete finche' dice "finita"
    python csv/_respiro_congelato.py --referto > doc/referti_l2/respiro_congelato.txt
"""
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _energia_vuoto_vivo as EV                               # noqa: E402
import _respiro_sul_fondo as RS                                # noqa: E402

V = EV.V
NOME = "BG-F-0.15"             # ### la corsa viva di cui si fa il controllo
TAU_FINE = 10000.0             # ### il mandato: fino a 10000
BLOCCO = 1000.0                # ### il mandato: a passi di 1000
TRATTO = (5000.0, 10000.0)     # ### il tratto della crescita (respiro_sul_fondo: dopo ~5000)
ISTANTI = (0.0, 2500.0, 5000.0, 7500.0, 10000.0)   # ### il mandato: le bande in 5 istanti
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "respiro_congelato")
DIR_NPZ = os.path.join(RADICE, "db", "respiro_congelato")
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


def nomi():
    pre = "%s_" % NOME
    return sorted(n for n in os.listdir(DIR_JSON) if n.startswith(pre) and n.endswith(".jsonl")) if os.path.isdir(DIR_JSON) else []


# ------------------------------------------------------------------------------------------------ la ripartizione di 326747d0
def ripartizione():
    import _deriva_congelato as DC
    import _libro_dei_conti as LC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    print("=" * 130)
    print("LA RIPARTIZIONE DELL'ENERGIA DI 326747d0 COL TERMINE DELLA MONETA (Luca, il TODO del controllo congelato): le 6 corse di _vuoto_vivo_B, (fine - inizio) per regione, dagli stati iniziale e finale")
    print("  la configurazione: eps %g, N %.0e, L %d, LAM_ZERO %g, R_VICINO %g, lo zero conv('simm'); l'unita' N |e_K|; ### la strada A tick per tick NON si ricalcola senza rigirare" % (V.EPS, V.N, V.L, V.LAM_ZERO, V.R_VICINO))
    print("=" * 130)
    for nome, (sol, vuoto, s) in V.CORSE.items():
        testa, camp, _dd, rr = V.serie(nome)
        with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                w_in = DC.forma(z, rec["larghezza"])[0]
            p0, info, e_K = EV.preparata(z, phi0, pK, sol, s)
            assert w_in == testa["w_in"] and info["mu"] == testa["info"]["mu"] and e_K == testa["e_K"], "la scena NON e' quella della corsa"
            vic = z["rr"] <= V.R_VICINO * w_in
            mas = {"vicino": vic, "lontano": ~vic, "totale": np.ones(z["inc"].n, dtype=bool)}
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                a0 = LC.per_regione(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO), mas)
                b0 = LC.per_regione(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, z["par"]), mas)
                with np.load(os.path.join(V.DIR_NPZ, nome + ".npz")) as dati:
                    assert int(dati["t"]) == rr[-1]["t1"], (int(dati["t"]), rr[-1]["t1"])
                    for k in z["st"]:
                        if isinstance(z["st"][k], np.ndarray):
                            z["st"][k][...] = dati[k]
                assert V.shas(z) == rr[-1]["sha_fine"], "lo stato finale NON e' la fine dell'ultimo pezzo"
                a1 = LC.per_regione(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO), mas)
                b1 = LC.per_regione(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, z["par"]), mas)
        assert camp[0]["t"] == 0 and camp[-1]["t"] == rr[-1]["t1"]
        nullo = all(a0[r][k] == camp[0]["E"][r][k] and a1[r][k] == camp[-1]["E"][r][k] for r in a0 for k in a0[r])
        sc = V.N * abs(e_K)
        print("### %s (tick %d .. %d)" % (nome, 0, rr[-1]["t1"]))
        esito("DEVE PASSARE: %s, il libro a eps 0 all'inizio e alla fine = i campioni committati, AL BIT, ogni regione e ogni conto" % nome, nullo, "")
        for r in ("vicino", "lontano", "totale"):
            print("  %-8s (fine - inizio, in N |e_K|): a eps 0: cin %+.4e vuoto %+.4e legame %+.4e H_tot %+.4e  |  COL TERMINE DELLA MONETA: cin %+.4e vuoto %+.4e legame %+.4e H_tot %+.4e  (la moneta all'inizio %+.4e, alla fine %+.4e)"
                  % (r, (a1[r]["cin"] - a0[r]["cin"]) / sc, (a1[r]["vuo"] - a0[r]["vuo"]) / sc, (a1[r]["leg"] - a0[r]["leg"]) / sc, (a1[r]["tot"] - a0[r]["tot"]) / sc,
                     (b1[r]["cin"] - b0[r]["cin"]) / sc, (b1[r]["vuo"] - b0[r]["vuo"]) / sc, (b1[r]["leg"] - b0[r]["leg"]) / sc, (b1[r]["tot"] - b0[r]["tot"]) / sc,
                     (b0[r]["tot"] - a0[r]["tot"]) / sc, (b1[r]["tot"] - a1[r]["tot"]) / sc))
        print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


# ------------------------------------------------------------------------------------------------ la corsa congelata
def corsa():
    """### **Un pezzo di `V.PEZZO` tick a vuoto CONGELATO** *(`_congelato_lungo.avanza`)*; ### **la ripresa al bit.**"""
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _salti_nel_cuore as SN
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    sol, vuoto, s = V.CORSE[NOME]
    t_fine = int(round(TAU_FINE / s))
    testa_v = V.LP.leggi(os.path.join(V.DIR_JSON, V.nomi(NOME)[0]))
    fatti = nomi()
    prec = V.LP.leggi(os.path.join(DIR_JSON, fatti[-1])) if fatti else None
    if prec is not None and (prec["t1"] >= t_fine or prec["t_dis"] is not None):
        print("  la corsa %s congelata: finita (%d pezzi)" % (NOME, len(fatti)))
        return 0
    os.makedirs(DIR_JSON, exist_ok=True)
    os.makedirs(DIR_NPZ, exist_ok=True)
    f_rip = os.path.join(DIR_NPZ, NOME + ".npz")
    s0 = time.time()
    with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        h = SN.lunghezza_arco(z)
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        p0, info = V.partenza(sol, z, phi0, pK, s)
        e_K = V.e_K_di(z)
        _ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = V.LP.ML.Bande(Z, z["L"])
        for k, v in salvato.items():
            z["st"][k][...] = v
        mu = info["mu"]
        assert testa_v["info"]["mu"] == mu and testa_v["w_in"] == w_in and testa_v["e_K"] == e_K, "la scena NON e' quella di BG-F-0.15"
        par = z["par"]
        assert par["eps"] == V.EPS != 0.0, "il libro dei conti deve passare il par della corsa (eps acceso)"
        if prec is None:
            t0 = 0
            z["st"]["psi_h"][...] = p0
        else:
            t0 = prec["t1"]
            with np.load(f_rip) as dati:
                assert int(dati["t"]) == t0
                for k in z["st"]:
                    if isinstance(z["st"][k], np.ndarray):
                        z["st"][k][...] = dati[k]
            assert V.shas(z) == prec["sha_fine"], "lo stato di ripresa NON e' la fine del pezzo prima (al bit, ogni chiave)"
        vic = z["rr"] <= V.R_VICINO * w_in
        mas = {"vicino": vic, "lontano": ~vic, "totale": np.ones(z["inc"].n, dtype=bool)}
        t1 = min(t0 + V.PEZZO, t_fine)
        camp, dd = [], []
        t_dis = None
        f_lis0 = testa_v["campioni"][0]["f_liscia"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            if t0 == 0:
                camp.append(V.misura(z, 0, w_in, w0, h, LC, LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, par), mas))
            for t in range(t0 + 1, t1 + 1):
                CL.avanza(z, phi0, 1)
                if t % V.OGNI == 0:
                    c = V.misura(z, t, w_in, w0, h, LC, LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, par), mas)
                    camp.append(c)
                    if c["f_liscia"] < V.META * f_lis0:
                        t_dis = t
                if t % V.OGNI_D == 0:
                    D = np.exp(1j * mu * s * t) * z["st"]["psi_h"] - p0
                    cf = bande.coeff(D)
                    pk = np.abs(cf) ** 2
                    tot = float(pk.sum())
                    dd.append({"t": t, "nD": float(np.linalg.norm(D)) / float(np.linalg.norm(p0)), "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}})
                if t_dis is not None:
                    t1 = t
                    break
        sha_fine = V.shas(z)
        tmp = f_rip.replace(".npz", "_tmp.npz")
        np.savez(tmp, t=t1, **{k: v for k, v in z["st"].items() if isinstance(v, np.ndarray)})
    os.replace(tmp, f_rip)
    riga = {"nome": NOME, "sol": sol, "vuoto": vuoto, "s": s, "eps": V.EPS, "N": V.N, "L": V.L, "t0": t0, "t1": t1, "t_fine": t_fine, "t_dis": t_dis,
            "w_in": w_in, "h": h, "e_K": e_K, "info": info, "campioni": camp, "D": dd, "sha_fine": sha_fine, "secondi": time.time() - s0,
            "tick": "congelato (_congelato_lungo.avanza)", "libro": "col par della corsa"}
    V.LP.scrivi_nuovo(os.path.join(DIR_JSON, "%s_%06d.jsonl" % (NOME, t0)), riga)
    print("  la corsa %s congelata: il pezzo %d -> %d%s; f_liscia %.5f (all'inizio %.5f), w %.4f, alone %.5f; mu %+.6f; %.0f s"
          % (NOME, t0, t1, ", SCIOLTO (f_liscia sotto meta')" if t_dis is not None else "", camp[-1]["f_liscia"], f_lis0, camp[-1]["w"], camp[-1]["alone"], mu, time.time() - s0))
    return 0


# ------------------------------------------------------------------------------------------------ il referto
def serie_viva():
    """### **La corsa viva:** i pezzi di `_vuoto_vivo_B` *(0 .. 3000)* e di `_respiro_sul_fondo` *(3000 .. 10000)*; il campione doppio a `3000` si tiene una volta."""
    _t, camp, dd, rr = V.serie(NOME)
    rr2 = [V.LP.leggi(os.path.join(RS.DIR_JSON, n)) for n in RS.nomi()]
    assert rr2 and rr2[0]["t0"] == rr[-1]["t1"], "la continuazione non parte dalla fine"
    visti = {c["t"] for c in camp}
    camp = camp + [c for r in rr2 for c in r["campioni"] if c["t"] not in visti]
    dd = dd + [d for r in rr2 for d in r["D"]]
    return camp, dd


def serie_congelata():
    rr = [V.LP.leggi(os.path.join(DIR_JSON, n)) for n in nomi()]
    for a, b in zip(rr, rr[1:]):
        assert a["t1"] == b["t0"], "un buco fra i pezzi"
    return [c for r in rr for c in r["campioni"]], [d for r in rr for d in r["D"]], rr


def pendenza(x, y):
    return float(np.polyfit(x, y, 1)[0]) if len(x) >= 3 else float("nan")


def blocchi(nome, camp, s):
    tt = np.array([c["t"] for c in camp]) * s
    fl = np.array([c["f_liscia"] for c in camp])
    ww = np.array([c["w"] for c in camp])
    al = np.array([c["alone"] for c in camp])
    xx = np.array([c["x"] for c in camp])
    yy = np.array([c["y"] for c in camp])
    print("### %s, a blocchi di %g (le medie; le pendenze per 1000 unita' di tempo; il baricentro: la distanza dalla posizione iniziale)" % (nome, BLOCCO))
    print("    %-17s %-9s %-9s %-11s %-10s %-14s %-14s %-9s" % ("il tempo", "cuore", "w", "cuore x w", "alone", "pend. alone", "pend. w", "baric."))
    for a in np.arange(0.0, TAU_FINE, BLOCCO):
        m = (tt >= a) & (tt < a + BLOCCO) if a + BLOCCO < TAU_FINE else (tt >= a)
        if not m.any():
            continue
        print("    %7.0f .. %7.0f %.5f   %.4f    %.5f     %.5f    %+.4e    %+.4e    %.4f"
              % (a, a + BLOCCO, fl[m].mean(), ww[m].mean(), (fl[m] * ww[m]).mean(), al[m].mean(), 1000 * pendenza(tt[m], al[m]), 1000 * pendenza(tt[m], ww[m]),
                 math.hypot(xx[m].mean() - xx[0], yy[m].mean() - yy[0])))
    return tt, fl, ww, al


def forma_crescita(nome, tt, y, che):
    m = (tt >= TRATTO[0]) & (tt <= TRATTO[1])
    if m.sum() < 9:
        print("  %s, %s: il tratto %g .. %g non c'e'" % (nome, che, TRATTO[0], TRATTO[1]))
        return
    t, v = tt[m], y[m]
    terzi = np.array_split(np.arange(len(t)), 3)
    p1, p3 = pendenza(t[terzi[0]], v[terzi[0]]), pendenza(t[terzi[2]], v[terzi[2]])
    cl = np.polyfit(t, v, 1)
    rl = float(np.sqrt(np.mean((np.polyval(cl, t) - v) ** 2)))
    if np.all(v > 0):
        ce = np.polyfit(t, np.log(v), 1)
        re = float(np.sqrt(np.mean((np.exp(np.polyval(ce, t)) - v) ** 2)))
        es = "l'esponenziale v = A e^{k t}: k %+.4e per unita' di tempo, residuo RMS %.4e" % (ce[0], re)
    else:
        es = "l'esponenziale: non definito (valori non positivi)"
    print("  %s, %s sul tratto %g .. %g: la pendenza del primo terzo %+.4e, dell'ultimo %+.4e per 1000, il rapporto %.3f; il fit lineare: residuo RMS %.4e; %s"
          % (nome, che, TRATTO[0], TRATTO[1], 1000 * p1, 1000 * p3, p3 / p1 if p1 else float("inf"), rl, es))


def referto():
    sol, vuoto, s = V.CORSE[NOME]
    print("=" * 130)
    print("IL CONTROLLO A VUOTO CONGELATO DEL RESPIRO SUL FONDO (Luca, dopo 1ee60e19): %s (BG, il fondo F0, s %g, eps %g, N %.0e, L %d, cs spento, lo zero conv('simm')) col vuoto VIVO (il tick intero) e CONGELATO (_congelato_lungo.avanza), fino a %g"
          % (NOME, s, V.EPS, V.N, V.L, TAU_FINE))
    print("  la configurazione: TAU_FINE %g BLOCCO %g TRATTO %s ISTANTI %s; di _vuoto_vivo_B: PEZZO %d OGNI %d OGNI_D %d META %g R_VICINO %g LAM_ZERO %g TOLL_NORMA %g; il libro dei conti della corsa congelata col par della corsa"
          % (TAU_FINE, BLOCCO, TRATTO, ISTANTI, V.PEZZO, V.OGNI, V.OGNI_D, V.META, V.R_VICINO, V.LAM_ZERO, V.TOLL_NORMA))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (c1) a vuoto congelato w resta limitato: e' il vuoto vivo; (c2) anche a vuoto congelato w cresce in modo simile: e' del solitone; (c3) altro")
    print("=" * 130)
    cv, dv = serie_viva()
    cc, dc, rc = serie_congelata()
    if not cc:
        print("### NESSUN PEZZO CONGELATO")
        return
    ult = rc[-1]
    fatta = ult["t1"] >= ult["t_fine"] or ult["t_dis"] is not None
    print("### la corsa congelata: %s; %d pezzi, %d campioni, %.0f s" % (("SCIOLTA a tempo %.1f" % (ult["t_dis"] * s)) if ult["t_dis"] is not None else ("REGGE fino a %g" % (ult["t1"] * s) if fatta else "### NON FINITA"),
                                                                   len(rc), len(cc), sum(r["secondi"] for r in rc)))
    R = {}
    for nome, camp in (("VIVO", cv), ("CONGELATO", cc)):
        R[nome] = blocchi(nome, camp, s)
        print("    Lambda medio sotto il solitone %.6f -> %.6f; lontano %.6f -> %.6f" % (camp[0]["lam_vicino"], camp[-1]["lam_vicino"], camp[0]["lam_lontano"], camp[-1]["lam_lontano"]))
    print("-" * 130)
    print("### LA FORMA DELLA CRESCITA")
    for nome in R:
        tt, fl, ww, al = R[nome]
        forma_crescita(nome, tt, ww, "w")
        forma_crescita(nome, tt, al, "l'alone")
    print("-" * 130)
    print("### LE BANDE DI D")
    for nome, dd in (("VIVO", dv), ("CONGELATO", dc)):
        td = np.array([d["t"] for d in dd]) * s
        for ist in ISTANTI:
            d = dd[int(np.argmin(np.abs(td - ist)))]
            print("  %-9s a tempo %7.1f: |D|/|psi0| %.4e; le bande %s" % (nome, d["t"] * s, d["nD"], " ".join("%s %.4f" % (k, v) for k, v in sorted(d["bande"].items()))))
    print("-" * 130)
    print("### L'ESTRAPOLAZIONE DICHIARATA (NON una misura): se il cuore liscio continuasse con la pendenza degli ultimi 3000, il tempo a cui scenderebbe sotto %g volte il valore iniziale (il criterio di dissoluzione delle corse)" % V.META)
    f0 = cv[0]["f_liscia"]
    for nome in R:
        tt, fl, ww, al = R[nome]
        m = tt >= tt[-1] - 3000.0
        p = pendenza(tt[m], fl[m])
        print("  %-9s la pendenza del cuore negli ultimi 3000 %+.4e per 1000; %s" % (nome, 1000 * p, ("sotto %.5f a tempo ~%.0f" % (V.META * f0, tt[-1] + (V.META * f0 - fl[m][-1]) / p)) if p < 0 else "il cuore non cala: nessuna estrapolazione"))
    print("-" * 130)
    print("### I CRITERI")
    M = np.array([c["E"]["totale"]["M"] for c in cc])
    Vv = np.array([c["E"]["totale"]["V"] for c in cc])
    dM, dV = float(np.max(np.abs(M / M[0] - 1.0))), float(np.max(np.abs(Vv / Vv[0] - 1.0)))
    esito("DEVE PASSARE: la corsa congelata arriva a %g o si scioglie" % TAU_FINE, fatta, "")
    esito("DEVE PASSARE: M e V entro %g (la corsa congelata)" % V.TOLL_NORMA, dM <= V.TOLL_NORMA and dV <= V.TOLL_NORMA, "dM %.1e dV %.1e" % (dM, dV))
    esito("DEVE PASSARE: la corsa congelata e' stata fatta col libro col par della corsa", all(r.get("libro") == "col par della corsa" for r in rc), "")
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--ripartizione" in argv:
        ripartizione()
    elif "--corsa" in argv:
        sys.exit(corsa())
    elif "--referto" in argv:
        referto()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
