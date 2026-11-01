# -*- coding: utf-8 -*-
r"""**IL RESPIRO SUL FONDO** *(il mandato di Luca delle `11:22` del `2026-11-01`, punto `2`; NESSUNA MODIFICA AL NUCLEO; [[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]];
il task history `doc/TASK_HISTORY/2026-11-01_energia_e_respiro.md`, `R0`)*: ### **`BG-F` a `s 0.15` di `_vuoto_vivo_B`, continuato DALLA FINE** *(tick `20000`, al bit)*
### **fino a `10000` unita' di tempo**, a pezzi: gli stessi campioni, ### **col libro dei conti col `par` della corsa** *(il termine della moneta)*, e accanto `H_tot` del libro a eps `0`.

    python csv/_respiro_sul_fondo.py --corsa          # un pezzo; si ripete finche' dice "finita"
    python csv/_respiro_sul_fondo.py --referto > doc/referti_l2/respiro_sul_fondo.txt
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

import _vuoto_vivo_B as V                                      # noqa: E402

NOME = "BG-F-0.15"             # ### la corsa di _vuoto_vivo_B che si continua
TAU_FINE = 10000.0             # ### il mandato: fino a 10000 unita' di tempo
DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "respiro_sul_fondo")
DIR_NPZ = os.path.join(RADICE, "db", "respiro_sul_fondo")
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


def corsa():
    """### **Un pezzo di `V.PEZZO` tick;** ### **il primo riparte dallo stato finale di `_vuoto_vivo_B` (al bit), gli altri dal pezzo prima (al bit).**"""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _salti_nel_cuore as SN
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    sol, vuoto, s = V.CORSE[NOME]
    t_fine = int(round(TAU_FINE / s))
    vecchi = V.nomi(NOME)
    testa_v = V.LP.leggi(os.path.join(V.DIR_JSON, vecchi[0]))
    coda_v = V.LP.leggi(os.path.join(V.DIR_JSON, vecchi[-1]))
    fatti = nomi()
    prec = V.LP.leggi(os.path.join(DIR_JSON, fatti[-1])) if fatti else coda_v
    if prec["t1"] >= t_fine or prec["t_dis"] is not None:
        print("  la corsa %s, il respiro: finita (%d pezzi)" % (NOME, len(fatti)))
        return 0
    os.makedirs(DIR_JSON, exist_ok=True)
    os.makedirs(DIR_NPZ, exist_ok=True)
    f_rip = os.path.join(DIR_NPZ, NOME + ".npz") if fatti else os.path.join(V.DIR_NPZ, NOME + ".npz")
    s0 = time.time()
    with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        h = SN.lunghezza_arco(z)
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        p0, info = V.partenza(sol, z, phi0, pK, s)
        e_K = V.e_K_di(z)
        ph, Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        bande = V.LP.ML.Bande(Z, z["L"])
        for k, v in salvato.items():
            z["st"][k][...] = v
        mu = info["mu"]
        assert testa_v["info"]["mu"] == mu and testa_v["w_in"] == w_in and testa_v["e_K"] == e_K, "la scena NON e' quella di _vuoto_vivo_B"
        t0 = prec["t1"]
        with np.load(f_rip) as dati:
            assert int(dati["t"]) == t0, (int(dati["t"]), t0)
            for k in z["st"]:
                if isinstance(z["st"][k], np.ndarray):
                    z["st"][k][...] = dati[k]
        assert V.shas(z) == prec["sha_fine"], "lo stato di ripresa NON e' la fine del pezzo prima (al bit, ogni chiave)"
        vic = z["rr"] <= V.R_VICINO * w_in
        mas = {"vicino": vic, "lontano": ~vic, "totale": np.ones(z["inc"].n, dtype=bool)}
        t1 = min(t0 + V.PEZZO, t_fine)
        camp, dd = [], []
        gpos, gneg = 0.0, 0.0
        t_dis = None
        f_lis0 = testa_v["campioni"][0]["f_liscia"]
        par = z["par"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            conti = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, par)
            prec_d2 = math.fsum(conti["tot"][vic].tolist())
            if not fatti:
                c = V.misura(z, t0, w_in, w0, h, LC, conti, mas)
                c["gA_pos"], c["gA_neg"] = 0.0, 0.0
                c["H_eps0"] = math.fsum(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO)["tot"].tolist())
                camp.append(c)
            for t in range(t0 + 1, t1 + 1):
                TK.percorri_tick(z["st"], z["mot"], par, (), None, len(CM.ORDINE))
                conti = LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO, par)
                d2 = math.fsum(conti["tot"][vic].tolist())
                g = d2 - prec_d2
                prec_d2 = d2
                if g > 0:
                    gpos += g
                else:
                    gneg += g
                if t % V.OGNI == 0:
                    c = V.misura(z, t, w_in, w0, h, LC, conti, mas)
                    c["gA_pos"], c["gA_neg"] = gpos, gneg
                    c["H_eps0"] = math.fsum(LC.conti_per_nodo(z["inc"], z["mot"], z["st"], e_K, V.LAM_ZERO)["tot"].tolist())
                    gpos, gneg = 0.0, 0.0
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
        f_out = os.path.join(DIR_NPZ, NOME + ".npz")
        tmp = f_out.replace(".npz", "_tmp.npz")
        np.savez(tmp, t=t1, **{k: v for k, v in z["st"].items() if isinstance(v, np.ndarray)})
    os.replace(tmp, f_out)
    riga = {"nome": NOME, "sol": sol, "vuoto": vuoto, "s": s, "eps": V.EPS, "N": V.N, "L": V.L, "t0": t0, "t1": t1, "t_fine": t_fine, "t_dis": t_dis,
            "w_in": w_in, "h": h, "e_K": e_K, "info": info, "campioni": camp, "D": dd, "sha_fine": sha_fine, "secondi": time.time() - s0, "libro": "col par della corsa"}
    V.LP.scrivi_nuovo(os.path.join(DIR_JSON, "%s_%06d.jsonl" % (NOME, t0)), riga)
    fl = camp[-1]["f_liscia"]
    print("  la corsa %s, il respiro: il pezzo %d -> %d%s; f_liscia %.5f (all'inizio %.5f), w %.4f, alone %.5f; mu %+.6f; %.0f s"
          % (NOME, t0, t1, ", SCIOLTO (f_liscia sotto meta')" if t_dis is not None else "", fl, f_lis0, camp[-1]["w"], camp[-1]["alone"], mu, time.time() - s0))
    return 0


def pendenza(tt, yy):
    return float(np.polyfit(tt, yy, 1)[0]) if len(tt) >= 3 else float("nan")


def referto():
    sol, vuoto, s = V.CORSE[NOME]
    print("=" * 130)
    print("IL RESPIRO SUL FONDO (Luca 11:22, punto 2): %s di _vuoto_vivo_B (BG, il fondo F0, s %g, eps %g, N %.0e, L %d, il tick intero, cs spento, lo zero conv('simm')) continuato fino a %g; l'unita' N |e_K|"
          % (NOME, s, V.EPS, V.N, V.L, TAU_FINE))
    print("  la configurazione: TAU_FINE %g; di _vuoto_vivo_B: PEZZO %d OGNI %d OGNI_D %d META %g R_VICINO %g LAM_ZERO %g TOLL_NORMA %g; il libro dei conti della continuazione: col par della corsa (eps %g)"
          % (TAU_FINE, V.PEZZO, V.OGNI, V.OGNI_D, V.META, V.R_VICINO, V.LAM_ZERO, V.TOLL_NORMA, V.EPS))
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (r1) il cuore oscilla limitato (il minimo non sotto ~0.38) e l'alone non cresce; (r2) il cuore cala: quanto, dove va; (r3) altro")
    print("=" * 130)
    testa_v, camp_v, dd_v, rr_v = V.serie(NOME)
    rr = [V.LP.leggi(os.path.join(DIR_JSON, n)) for n in nomi()]
    if not rr:
        print("### NESSUN PEZZO")
        return
    prima = rr_v[-1]
    for a, b in zip([prima] + rr, rr):
        assert a["t1"] == b["t0"], "un buco fra i pezzi"
    camp = [c for r in rr for c in r["campioni"]]
    dd = [d for r in rr for d in r["D"]]
    ult = rr[-1]
    fatta = ult["t1"] >= ult["t_fine"] or ult["t_dis"] is not None
    sc = V.N * abs(testa_v["e_K"])
    tt = np.array([c["t"] for c in camp]) * s
    fl = np.array([c["f_liscia"] for c in camp])
    al = np.array([c["alone"] for c in camp])
    ww = np.array([c["w"] for c in camp])
    H = np.array([c["E"]["totale"]["tot"] for c in camp])
    H0 = np.array([c["H_eps0"] for c in camp])
    M = np.array([c["E"]["totale"]["M"] for c in camp])
    Vv = np.array([c["E"]["totale"]["V"] for c in camp])
    M0, V0 = camp_v[0]["E"]["totale"]["M"], camp_v[0]["E"]["totale"]["V"]
    dM = float(np.max(np.abs(M / M0 - 1.0)))
    dV = float(np.max(np.abs(Vv / V0 - 1.0)))
    print("### %s: %s; %d pezzi della continuazione, %d campioni, tempo %.1f .. %.1f, %.0f s"
          % (NOME, ("SCIOLTO a tempo %.1f" % (ult["t_dis"] * s)) if ult["t_dis"] is not None else ("REGGE fino a %g" % (ult["t1"] * s) if fatta else "### NON FINITA"),
             len(rr), len(camp), tt[0], tt[-1], sum(r["secondi"] for r in rr)))
    fl_v = np.array([c["f_liscia"] for c in camp_v])
    print("  fino a 3000 (_vuoto_vivo_B): il cuore liscio %.5f -> %.5f, il minimo %.5f, il massimo %.5f" % (fl_v[0], fl_v[-1], fl_v.min(), fl_v.max()))
    i_min = int(np.argmin(fl))
    print("  la continuazione: il cuore liscio %.5f -> %.5f, il minimo %.5f a tempo %.1f, il massimo %.5f; la pendenza %+.4e per 1000 unita' di tempo"
          % (fl[0], fl[-1], fl.min(), tt[i_min], fl.max(), 1000 * pendenza(tt, fl)))
    for k in range(0, len(tt), max(1, len(tt) // 7)):
        j = min(len(tt) - 1, k + max(1, len(tt) // 7) - 1)
        print("    tempo %7.1f .. %7.1f: il cuore liscio medio %.5f, min %.5f, max %.5f; w medio %.4f; l'alone medio %.5f"
              % (tt[k], tt[j], fl[k:j + 1].mean(), fl[k:j + 1].min(), fl[k:j + 1].max(), ww[k:j + 1].mean(), al[k:j + 1].mean()))
    print("  w %.4f -> %.4f; l'alone %.5f -> %.5f (il massimo %.5f a tempo %.1f), la pendenza %+.4e per 1000; il baricentro si sposta di %.4f"
          % (ww[0], ww[-1], al[0], al[-1], al.max(), tt[int(np.argmax(al))], 1000 * pendenza(tt, al), math.hypot(camp[-1]["x"] - camp[0]["x"], camp[-1]["y"] - camp[0]["y"])))
    c0, cf = camp[0], camp[-1]
    print("  Lambda medio sotto il solitone %.6f -> %.6f; lontano %.6f -> %.6f" % (c0["lam_vicino"], cf["lam_vicino"], c0["lam_lontano"], cf["lam_lontano"]))
    for reg in ("vicino", "lontano", "totale"):
        e0, e1 = c0["E"][reg], cf["E"][reg]
        print("  il libro dei conti (col par), %-8s (fine - inizio della continuazione, in N |e_K|): la materia (cin) %+.4e  il vuoto %+.4e  il legame %+.4e  H_tot %+.4e"
              % (reg, (e1["cin"] - e0["cin"]) / sc, (e1["vuo"] - e0["vuo"]) / sc, (e1["leg"] - e0["leg"]) / sc, (e1["tot"] - e0["tot"]) / sc))
    gp = sum(c["gA_pos"] for c in camp)
    gn = sum(c["gA_neg"] for c in camp)
    print("  la strada A sul disco (in N |e_K|): le entrate %+.4e, le uscite %+.4e, il netto %+.4e" % (gp / sc, gn / sc, (gp + gn) / sc))
    print("  H_tot sul toro, max |H - H(inizio continuazione)|: col par %.4e; il libro a eps 0 %.4e (in N |e_K|)" % (float(np.max(np.abs(H - H[0]))) / sc, float(np.max(np.abs(H0 - H0[0]))) / sc))
    if dd:
        for d in (dd[0], dd[len(dd) // 4], dd[len(dd) // 2], dd[3 * len(dd) // 4], dd[-1]):
            print("  D a tempo %7.1f: |D|/|psi0| %.4e; le bande %s" % (d["t"] * s, d["nD"], " ".join("%s %.4f" % (k, v) for k, v in sorted(d["bande"].items()))))
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE: la corsa arriva a %g o si scioglie" % TAU_FINE, fatta, "")
    esito("DEVE PASSARE: M e V entro %g (rispetto all'inizio di _vuoto_vivo_B)" % V.TOLL_NORMA, dM <= V.TOLL_NORMA and dV <= V.TOLL_NORMA, "dM %.1e dV %.1e" % (dM, dV))
    print("  LETTURA (r1), il fatto: il minimo della continuazione %.5f contro quello visto fino a 3000 (letto dai pezzi di _vuoto_vivo_B) %.5f: %s; la pendenza dell'alone %+.4e per 1000"
          % (fl.min(), fl_v.min(), "NON scende sotto" if fl.min() >= fl_v.min() else "### SCENDE SOTTO", 1000 * pendenza(tt, al)))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--corsa" in argv:
        sys.exit(corsa())
    elif "--referto" in argv:
        referto()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
